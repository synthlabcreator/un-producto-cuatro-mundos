// Cartón final «Un producto, cuatro mundos» · Remotion · 1080×1920 · 24 fps
// Render: npx remotion render src/index.ts Cierre out/cierre --sequence --image-format=png
// Después, reel.py lo añade como `tail.images`.
// Pon en public/: logo.png (archivo OFICIAL de la marca, en blanco y con fondo transparente) y la fuente.
import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, Easing} from 'remotion';

export const FPS = 24;
const W = 1080;
const cl = (x: number) => Math.max(0, Math.min(1, x));
const easeOut = Easing.bezier(0.22, 0.9, 0.3, 1);
const easeIO = Easing.bezier(0.6, 0, 0.25, 1);

// ---- ajusta esto ----
const ACENTO = '#CEFF00';
const BEAT = 0.4026;                      // pulso de la canción (reel.py song)
const T = {                               // segundos desde que empieza el cartón: un golpe cada 2 pulsos
  logo: 0,
  eslogan: 2 * BEAT,
  l1: 4 * BEAT,
  l2: 6 * BEAT,
  l3: 7 * BEAT,
  guarda: 8 * BEAT,
};
export const CIERRE_DUR = 5.5;
const LOGO = {w: 640, h: 224, x: 220, y: 560};        // posición final del logo
const LOGO0 = {w: 650, x: 0, y: 905};                 // dónde estaba el logo del producto en el último plano (se mide)
const ESLOGAN: string | null = null;                  // eslogan oficial (texto o imagen del archivo de la marca), o null
const LINEAS = ['¿QUIERES SABER CÓMO SE HACE?', 'TE DEJO LA SKILL EN GITHUB.', 'ENLACE EN EL COMENTARIO.'];
const FUENTE = 'Archivo Narrow';                     // condensada y gruesa; carga la fuente que quieras

const Word: React.FC<{t: number; t0: number; children: React.ReactNode}> = ({t, t0, children}) => {
  const k = easeOut(cl((t - t0) / 0.3));
  return (
    <span style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', paddingBottom: '0.06em'}}>
      <span style={{display: 'inline-block', transform: `translateY(${(1 - k) * 110}%)`}}>{children}</span>
    </span>
  );
};

const Line: React.FC<{t: number; text: string; t0: number; size: number; color: string; y: number}> = ({t, text, t0, size, color, y}) => (
  <div style={{position: 'absolute', top: y, width: W, textAlign: 'center', fontFamily: FUENTE, fontWeight: 800,
    fontSize: size, color, lineHeight: 1}}>
    {text.split(' ').map((w, i) => (
      <React.Fragment key={i}>{i > 0 ? ' ' : ''}<Word t={t} t0={t0 + i * 0.07}>{w}</Word></React.Fragment>
    ))}
  </div>
);

export const Cierre: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const m = easeIO(cl((t - T.logo) / 0.42));
  const wipe = 0.35 + 0.65 * easeOut(cl((t - T.logo) / 0.22));
  const lw = LOGO0.w + (LOGO.w - LOGO0.w) * m;
  const lx = LOGO0.x + (LOGO.x - LOGO0.x) * m;
  const ly = LOGO0.y + (LOGO.y - LOGO0.y) * m;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse 85% 60% at 50% 42%, #141416 0%, #070708 60%, #030303 100%)'}}>
      <Img src={staticFile('logo.png')} style={{position: 'absolute', left: lx, top: ly, width: lw,
        height: lw * (LOGO.h / LOGO.w), clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`}} />
      {ESLOGAN && <Line t={t} text={ESLOGAN} t0={T.eslogan} size={120} color="#FFFFFF" y={844} />}
      <Line t={t} text={LINEAS[0]} t0={T.l1} size={64} color="#EBEBEB" y={1139} />
      <Line t={t} text={LINEAS[1]} t0={T.l2} size={64} color="#EBEBEB" y={1221} />
      <Line t={t} text={LINEAS[2]} t0={T.l3} size={64} color="#EBEBEB" y={1303} />
      <Line t={t} text="¡GUÁRDALO!" t0={T.guarda} size={132} color={ACENTO} y={1425} />
    </AbsoluteFill>
  );
};

// Root.tsx:
// <Composition id="Cierre" component={Cierre} durationInFrames={Math.round(CIERRE_DUR * FPS)} fps={FPS} width={1080} height={1920} />
