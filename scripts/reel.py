#!/usr/bin/env python3
"""reel.py - speed-ramp an AI video reel around its voice-over and fit every cut to the beat of a song.

Subcommands (all paths in project.json are relative to the project file):
  measure  CLIP.mp4 [--start S --end E]   voice windows (Demucs vocal stem) + shot cuts + motion -> JSON to paste in project.json
  song     SONG.wav [--lyrics]            beat grid, drop candidates, Demucs stems, optional Whisper word timings
  ramps    project.json                   ramped scenes (video + scene audio), voice kept at 1x, cuts landed on target frames
  music    project.json                   instrumental from the song + sung lines moved by whole beats into the gaps between voices
  assemble project.json OUT.mp4           ramped scenes + tail pieces + music ducked under the voice, -14 LUFS, limiter

Needs: python 3.10+, ffmpeg on PATH, numpy, scipy, soundfile, opencv-python, librosa. Optional: demucs, openai-whisper.
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np

SR = 44100

# ---------------------------------------------------------------- helpers
def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)

def load_project(path):
    p = json.load(open(path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(path))
    p["_base"] = base
    p["_build"] = os.path.join(base, p.get("build_dir", "build"))
    os.makedirs(p["_build"], exist_ok=True)
    return p

def P(p, rel):
    return rel if os.path.isabs(rel) else os.path.join(p["_base"], rel)

def extract_wav(video, out, sr=SR):
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "2", "-ar", str(sr), out])

def demucs_vocals(wav, outdir):
    run([sys.executable, "-m", "demucs", "-n", "htdemucs_ft", "--two-stems", "vocals", "-o", outdir, wav], stdout=sys.stderr)
    name = os.path.splitext(os.path.basename(wav))[0]
    d = os.path.join(outdir, "htdemucs_ft", name)
    return os.path.join(d, "vocals.wav"), os.path.join(d, "no_vocals.wav")

def voice_windows(vocals_wav, floor_db=30, min_len=0.15, gap=0.3):
    import librosa
    y, sr = librosa.load(vocals_wav, sr=16000, mono=True)
    hop = 160
    db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=640, hop_length=hop)[0] + 1e-9)
    on = db > db.max() - floor_db
    regs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            a, b = i * hop / sr, j * hop / sr
            if regs and a - regs[-1][1] < gap: regs[-1][1] = b
            else: regs.append([a, b])
            i = j
        else: i += 1
    return [[round(a, 2), round(b, 2)] for a, b in regs if b - a > min_len]

def shot_cuts(video):
    import cv2
    cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    prev, d, mot, pg = None, [], [], None
    while True:
        ok, f = cap.read()
        if not ok: break
        small = cv2.resize(f, (135, 240))
        h = cv2.calcHist([cv2.cvtColor(small, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        h = cv2.normalize(h, h).flatten()
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)
        d.append(0 if prev is None else cv2.compareHist(prev, h, cv2.HISTCMP_BHATTACHARYYA))
        mot.append(0 if pg is None else float(np.abs(g - pg).mean()))
        prev, pg = h, g
    d = np.array(d)
    cuts = [round(i / fps, 2) for i in range(1, len(d)) if d[i] > 0.25 and d[i] > 3 * np.median(d[max(0, i - 6):i + 6])]
    return cuts, np.array(mot), fps

# ---------------------------------------------------------------- measure
def cmd_measure(a):
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "scene.wav"); extract_wav(a.clip, wav)
    try:
        voc, _ = demucs_vocals(wav, tmp); voice = voice_windows(voc)
    except Exception as e:
        print("Demucs not available or failed (%s): fill \"voice\" by hand." % e, file=sys.stderr); voice = []
    cuts, mot, fps = shot_cuts(a.clip)
    s = a.start if a.start is not None else 0.0
    e = a.end if a.end is not None else len(mot) / fps
    bounds = [s] + [c for c in cuts if s < c < e] + [e]
    shots = []
    for x, y in zip(bounds[:-1], bounds[1:]):
        m = mot[int(x * fps):int(y * fps)].mean() if y > x else 0
        peak = 3.2 if m < 8 else 2.6 if m < 14 else 2.0          # static shots can go faster
        shots.append([round(x, 3), round(y, 3), "c", peak])
    print(json.dumps({"video": a.clip, "start": s, "end": round(e, 3), "voice": voice, "shots": shots}, indent=1))

# ---------------------------------------------------------------- song
def cmd_song(a):
    import librosa
    out = os.path.splitext(a.song)[0] + "_analysis.json"
    stems = os.path.join(os.path.dirname(os.path.abspath(a.song)), "stems")
    try:
        voc, ins = demucs_vocals(a.song, stems)
    except Exception as e:
        print("Demucs failed (%s): analysing the full mix." % e, file=sys.stderr); voc, ins = None, a.song
    y, sr = librosa.load(ins, sr=22050)
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
    tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, hop_length=256, units="time")
    rms = librosa.feature.rms(y=y, hop_length=512)[0]; t = librosa.times_like(rms, sr=sr, hop_length=512)
    db = 20 * np.log10(rms + 1e-6)
    # drop candidates: biggest jump of loudness from the previous 2 s to the next 1 s, snapped to a beat
    cand = []
    for b in beats:
        pre = db[(t > b - 2) & (t < b)]; post = db[(t >= b) & (t < b + 1)]
        if len(pre) and len(post): cand.append((float(post.mean() - pre.mean()), float(b)))
    cand = sorted(cand, reverse=True)[:5]
    beat = float(np.polyfit(np.arange(len(beats)), beats, 1)[0])     # slope over all beats: steadier than the median gap
    res = {"tempo": 60 / beat, "beat": beat,
           "beats": [round(float(x), 3) for x in beats], "drop_candidates": [{"time": round(b, 3), "jump_db": round(j, 1)} for j, b in cand],
           "vocals": voc, "instrumental": ins}
    if a.lyrics and voc:
        import whisper
        r = whisper.load_model("small").transcribe(voc, word_timestamps=True, language=a.language)
        res["lines"] = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(),
                         "words": [[w["word"].strip(), round(w["start"], 2), round(w["end"], 2)] for w in s.get("words", [])]} for s in r["segments"]]
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("tempo %.1f BPM, beat %.4f s" % (res["tempo"], res["beat"]))
    print("drop candidates:", res["drop_candidates"])
    for l in res.get("lines", []): print("%6.2f-%6.2f %s" % (l["start"], l["end"], l["text"]))
    print("->", out)

# ---------------------------------------------------------------- ramps
def smooth(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def speed_curve(sc, tau, edge):
    s = np.ones_like(tau)
    for a, b, mode, pk in sc["shots"]:
        m = (tau >= a) & (tau < b); u = (tau[m] - a) / (b - a); bump = np.sin(np.pi * u) ** 2
        if mode == "n": s[m] = 1.0                                        # real speed (people walking!)
        elif mode == "k": s[m] = np.maximum(1.0, edge + (pk - edge) * (1 - bump))   # slow at the key moment
        else: s[m] = edge + (pk - edge) * bump                              # "c": fast in the middle
    w = np.zeros_like(tau)
    for va, vb in sc.get("voice", []):
        va -= .12; vb += .08
        w = np.maximum(w, np.where(tau < va, smooth(1 - (va - tau) / .35), np.where(tau > vb, smooth(1 - (tau - vb) / .35), 1)))
    return 1 + (s - 1) * (1 - w) * sc.get("_g", 1.0)

def time_map(sc, fps, edge):
    taus = np.arange(sc["start"], sc["end"], 1 / 2400)
    sp = speed_curve(sc, taus, edge)
    tout = np.concatenate([[0], np.cumsum((1 / 2400) / sp[:-1])])
    n = int(round(tout[-1] * fps))
    tau_s = np.interp(np.arange(int(round(n / fps * SR))) / SR, tout, taus)
    tau_f = np.interp(np.arange(n + 1) / fps, tout, taus)
    return tau_s, tau_f, n

def render_video(path_in, tau_f, n, fps, w, h, path_out):
    import cv2
    cap = cv2.VideoCapture(path_in); total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); src_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    cache, nxt = {}, [0]
    def get(k):
        k = min(k, total - 1)
        while nxt[0] <= k:
            ok, f = cap.read()
            if not ok: break
            if f.shape[1] != w or f.shape[0] != h: f = cv2.resize(f, (w, h), interpolation=cv2.INTER_LANCZOS4)
            cache[nxt[0]] = f; nxt[0] += 1
        for old in [x for x in cache if x < k - 6]: del cache[old]
        return cache[max(x for x in cache if x <= k)]
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", path_out], stdin=subprocess.PIPE)
    for i in range(n):
        k0, k1 = tau_f[i] * src_fps, tau_f[i + 1] * src_fps
        ks = list(range(int(round(k0)), max(int(round(k0)) + 1, int(round(k1)))))[:4]
        if k1 - k0 <= 1.5 or len(ks) == 1: fr = get(int(round(k0)))
        else: fr = np.mean([get(k).astype(np.float32) for k in ks], axis=0).astype(np.uint8)   # motion blur
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

def ramp_audio(wav, tau_s, curve):
    import soundfile as sf
    from scipy.signal import butter, sosfiltfilt
    y, sr = sf.read(wav, always_2d=True)
    if sr != SR: raise SystemExit(f"{wav}: expected {SR} Hz")
    lp = sosfiltfilt(butter(6, 6000, fs=SR, output="sos"), y, axis=0)
    pos, idx = tau_s * SR, np.arange(len(y))
    full = np.stack([np.interp(pos, idx, y[:, c]) for c in range(y.shape[1])], 1)
    soft = np.stack([np.interp(pos, idx, lp[:, c]) for c in range(y.shape[1])], 1)
    k = np.clip((curve - 1.2) / 0.8, 0, 1)[:, None]          # roll off the highs while speeding up
    return full * (1 - k) + soft * k

def cmd_ramps(a):
    import soundfile as sf
    p = load_project(a.project); fps, w, h = p.get("fps", 24), p.get("width", 1080), p.get("height", 1920)
    edge = p.get("edge_speed", 1.3); info, auds, t = [], [], 0.0
    for i, sc in enumerate(p["scenes"]):
        vid = P(p, sc["video"])
        wav = P(p, sc["audio"]) if sc.get("audio") else os.path.join(p["_build"], f"scene{i + 1}.wav")
        if not sc.get("audio"): extract_wav(vid, wav)
        target = sc.get("target_frames")
        if target:   # bisection on the ramp intensity until the scene is exactly `target` frames long
            lo, hi = 0.3, 3.0
            for _ in range(40):
                sc["_g"] = (lo + hi) / 2; n = time_map(sc, fps, edge)[2]
                if n == target: break
                lo, hi = (sc["_g"], hi) if n > target else (lo, sc["_g"])
        tau_s, tau_f, n = time_map(sc, fps, edge)
        if target and n != target: print(f"scene {i + 1}: could not reach {target} frames (got {n}); change peaks or shots", file=sys.stderr)
        out = os.path.join(p["_build"], f"scene{i + 1}_ramp.mp4"); render_video(vid, tau_f, n, fps, w, h, out)
        auds.append(ramp_audio(wav, tau_s, speed_curve(sc, tau_s, edge)))
        tf = np.arange(n + 1) / fps
        vo = [[round(t + float(np.interp(va, tau_f, tf)), 3), round(t + float(np.interp(vb, tau_f, tf)), 3)] for va, vb in sc.get("voice", [])]
        info.append({"file": out, "start": round(t, 3), "frames": n, "voice": vo}); t += n / fps
        print(f"scene {i + 1}: {sc['end'] - sc['start']:.2f}s -> {n / fps:.2f}s ({n} frames), voice at {vo}")
    sf.write(os.path.join(p["_build"], "scenes_ramp.wav"), np.concatenate(auds), SR)
    json.dump({"scenes": info, "end": round(t, 3)}, open(os.path.join(p["_build"], "ramps.json"), "w"), indent=1)
    print(f"ramped scenes end at {t:.3f}s")

# ---------------------------------------------------------------- music
def cmd_music(a):
    import soundfile as sf
    p = load_project(a.project); m = p["music"]
    r = json.load(open(os.path.join(p["_build"], "ramps.json")))
    total = r["end"] + sum(tail_seconds(p, x) for x in p.get("tail", []))
    ins, sr = sf.read(P(p, m["instrumental"]), always_2d=True)
    voc, _ = sf.read(P(p, m["vocals"]), always_2d=True)
    off = m["song_drop"] - m.get("reel_drop", r["end"])          # song second that plays at reel 0
    n = int(round(total * sr)); a0 = int(round(off * sr))
    out = np.zeros((n, ins.shape[1])); seg = ins[a0:a0 + n]; out[:len(seg)] = seg
    fo = int(0.45 * sr); out[-fo:] *= (np.linspace(1, 0, fo) ** 2)[:, None]
    voices = [v for s in r["scenes"] for v in s["voice"]]
    k = int(0.025 * sr); ramp = np.linspace(0, 1, k)[:, None]
    for ln in m.get("lines", []):
        s0, s1, beats = ln["start"], ln["end"], ln["shift_beats"]
        piece = voc[int(s0 * sr):int(s1 * sr)].copy(); piece[:k] *= ramp; piece[-k:] *= ramp[::-1]
        t = s0 + beats * m["beat"] - off; i = int(round(t * sr)); j = min(n, i + len(piece))
        if i < 0 or i >= n: print("line outside the reel:", ln, file=sys.stderr); continue
        out[i:j] += piece[:j - i]
        clash = [v for v in voices if not (t + (s1 - s0) <= v[0] or t >= v[1])]
        print(f"{ln.get('text', '')[:40]:42s} reel {t:6.2f}-{t + s1 - s0:6.2f}" + (f"  CLASHES WITH VOICE {clash}" if clash else ""))
    sf.write(os.path.join(p["_build"], "music.wav"), out, sr)
    print(f"music.wav {total:.2f}s (song {off:.3f}s plays at reel 0)")

# ---------------------------------------------------------------- assemble
def tail_seconds(p, x):
    fps = p.get("fps", 24)
    return x["frames"] / fps

def cmd_assemble(a):
    p = load_project(a.project); fps, w, h = p.get("fps", 24), p.get("width", 1080), p.get("height", 1920)
    r = json.load(open(os.path.join(p["_build"], "ramps.json")))
    inputs, vf, af, lab, alab = [], [], [], [], []
    def add(path, *pre):
        inputs.extend([*pre, "-i", path]); return inputs.count("-i") - 1
    for s in r["scenes"]:
        i = add(s["file"]); vf.append(f"[{i}:v]setpts=PTS-STARTPTS,setsar=1[v{i}]"); lab.append(f"[v{i}]")
    ia = add(os.path.join(p["_build"], "scenes_ramp.wav"))
    af.append(f"[{ia}:a]asetpts=PTS-STARTPTS[sc0]"); alab.append("[sc0]")
    t = r["end"]
    for x in p.get("tail", []):
        n = x["frames"]
        if "images" in x:                                  # e.g. an end card rendered as a PNG sequence
            i = add(P(p, x["images"]), "-framerate", str(fps))
            vf.append(f"[{i}:v]trim=end_frame={n},scale={w}:{h},format=yuv420p,setsar=1[v{i}]")
        else:                                              # a piece of a clip, optionally slowed down with a push-in
            i = add(P(p, x["video"])); slow = x.get("slow", 1); push = x.get("push_in", 0)
            f0 = round(x["start"] * fps); need = int(np.ceil(n / slow)) + 1
            chain = f"[{i}:v]fps={fps},trim=start_frame={f0}:end_frame={f0 + need},setpts={slow}*(PTS-STARTPTS),fps={fps},trim=end_frame={n},scale={w}:{h}"
            if push: chain += f",scale=w='trunc({w}*(1+{push}*n/{n})/2)*2':h=-2:eval=frame,crop={w}:{h}:'(iw-{w})*0.5':'(ih-{h})*0.5'"
            vf.append(chain + f",setsar=1[v{i}]")
            vol = x.get("volume", 1.0)
            if vol > 0 and slow == 1:
                af.append(f"[{i}:a]atrim={x['start']:.4f}:{x['start'] + n / fps:.4f},asetpts=PTS-STARTPTS,volume={vol},aresample={SR},"
                          f"adelay={round(t * 1000)}|{round(t * 1000)}[a{i}]"); alab.append(f"[a{i}]")
        lab.append(f"[v{i}]"); t += n / fps
    vf.append("".join(lab) + f"concat=n={len(lab)}:v=1:a=0,format=yuv420p[vout]")
    af.append("".join(alab) + f"amix=inputs={len(alab)}:normalize=0,apad,atrim=0:{t:.4f}[sc]")
    music = os.path.join(p["_build"], "music.wav")
    duck = 1 - 10 ** (-p.get("duck_db", 14) / 20)
    if os.path.exists(music):
        voices = [v for s in r["scenes"] for v in s["voice"]]
        expr = "+".join(f"max(0,min(1,min((t-{va - 0.25:.2f})/0.2,({vb + 0.3:.2f}-t)/0.3)))" for va, vb in voices) or "0"
        im = add(music)
        af.append(f"[{im}:a]aresample={SR},atrim=0:{t:.4f},volume='{p.get('music_gain', 0.85)}*(1-{duck:.3f}*min(1,{expr}))':eval=frame[mus]")
        af.append("[mus][sc]amix=inputs=2:normalize=0[mix]")
    else:
        af.append("[sc]anull[mix]")
    af.append("[mix]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:attack=1:release=60:level=disabled[aout]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(vf + af), "-map", "[vout]", "-map", "[aout]",
         "-r", str(fps), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", a.out])
    print(f"{a.out}  {t:.2f}s")

# ---------------------------------------------------------------- cli
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure"); m.add_argument("clip"); m.add_argument("--start", type=float); m.add_argument("--end", type=float)
    s = sub.add_parser("song"); s.add_argument("song"); s.add_argument("--lyrics", action="store_true"); s.add_argument("--language", default=None)
    for name in ("ramps", "music"):
        x = sub.add_parser(name); x.add_argument("project")
    x = sub.add_parser("assemble"); x.add_argument("project"); x.add_argument("out")
    a = ap.parse_args()
    {"measure": cmd_measure, "song": cmd_song, "ramps": cmd_ramps, "music": cmd_music, "assemble": cmd_assemble}[a.cmd](a)
