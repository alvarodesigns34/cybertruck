// Prueba de humo del visor en Chromium (auditoría del 20-10-2026, C10). Sirve web/ con el GLB comprimido con gzip y
// Content-Length comprimido, como GitHub Pages, y comprueba: consola sin errores, ninguna petición fuera del sitio,
// barra de carga sin pasar del 100 %, las 1.138 piezas, explosión reversible (desviación 0), dibujo bajo demanda
// (cero fotogramas en reposo) y aperturas sobre sus pivotes.
// Necesita Playwright, que no se versiona: npm i --no-save playwright@1.56.1 && npx playwright install chromium
// Uso: node tools/smoke.mjs
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { gzipSync } from 'node:zlib';
import { extname, isAbsolute, join, normalize, relative, resolve } from 'node:path';

let chromium;
try { ({ chromium } = await import('playwright')); } catch {
  console.error('Falta Playwright: npm i --no-save playwright@1.56.1 && npx playwright install chromium');
  process.exit(2);
}

const root = resolve('web');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.glb': 'model/gltf-binary',
  '.wasm': 'application/wasm', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.webp': 'image/webp' };
const server = http.createServer(async (req, res) => {
  const file = normalize(join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
  const rel = relative(root, file);
  if (rel.startsWith('..') || isAbsolute(rel)) { res.writeHead(403).end(); return; }
  try {
    let data = await readFile(file.endsWith('/') || rel === '' ? join(file, 'index.html') : file);
    const headers = { 'Content-Type': types[extname(file)] || 'text/html' };
    if (file.endsWith('.glb')) { data = gzipSync(data); headers['Content-Encoding'] = 'gzip'; }
    headers['Content-Length'] = data.length;
    res.writeHead(200, headers).end(data);
  } catch { res.writeHead(404).end(); }
});
await new Promise((r) => server.listen(8823, '127.0.0.1', r));

let failed = 0;
const report = (ok, name, detail = '') => { console.log(`${ok ? 'OK   ' : 'FALLO'} ${name}${detail ? ` — ${detail}` : ''}`); if (!ok) failed++; };
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
try {
  const page = await (await browser.newContext({ viewport: { width: 900, height: 600 } })).newPage();
  page.setDefaultTimeout(240000);
  const errors = [], external = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('request', (r) => { const u = r.url(); if (!u.startsWith('http://127.0.0.1') && !u.startsWith('blob:') && !u.startsWith('data:')) external.push(u); });
  await page.addInitScript(() => {
    window.__bar = [];
    new MutationObserver(() => { const t = document.getElementById('loader-text')?.textContent; if (t) window.__bar.push(t); })
      .observe(document, { subtree: true, childList: true, characterData: true });
  });
  await page.goto('http://127.0.0.1:8823/');
  await page.waitForFunction(() => window.__ct, null, { timeout: 300000 });
  const bar = await page.evaluate(() => window.__bar);
  const pct = bar.map((t) => Number(/(\d+) %/.exec(t)?.[1] ?? 0));
  report(Math.max(0, ...pct) <= 100, 'la barra de carga no pasa del 100 % con el GLB servido con gzip', `${bar.length} lecturas · última «${bar.at(-1) ?? ''}»`);
  report(!external.length, 'ninguna petición fuera del sitio (sin CDN)', external.slice(0, 3).join(' '));
  const r = await page.evaluate(async () => {
    const c = window.__ct, s = c.state;
    const frames = (n) => new Promise((res) => { let k = 0; const t = () => (++k >= n ? res() : requestAnimationFrame(t)); requestAnimationFrame(t); });
    const out = { comps: s.components.size, parts: s.parts.length };
    const dev = () => s.parts.reduce((m, p) => Math.max(m, p.obj.position.distanceTo(p.base)), 0);
    for (const k of [1, 0.37, 0.8, 0]) { s.explode = k; c.applyExplode(); await frames(1); }
    out.dev = dev();
    // Reposo: tras asentarse la cámara, ningún fotograma nuevo.
    for (let i = 0; i < 50; i++) { const f = c.frames; await frames(5); if (c.frames === f) break; }
    const f0 = c.frames; await frames(20); out.idle = c.frames - f0;
    // Aperturas.
    const door = c.OPENINGS.doors.items.find((it) => it.node.name === 'DOOR_FL'), tail = c.OPENINGS.tailgate.items[0];
    c.setOpening('doors', true); c.setOpening('tailgate', true);
    for (let i = 0; i < 300 && (c.OPENINGS.doors.k < 1 || c.OPENINGS.tailgate.k < 1); i++) await frames(1);
    const ang = (it) => THREE_ANGLE(it.node.quaternion);
    function THREE_ANGLE(q) { return 2 * Math.acos(Math.min(1, Math.abs(q.w))) * 180 / Math.PI; }
    out.door = ang(door); out.tail = ang(tail); out.drawnOpening = c.frames - f0;
    c.setOpening('doors', false); c.setOpening('tailgate', false);
    for (let i = 0; i < 300 && (c.OPENINGS.doors.k > 0 || c.OPENINGS.tailgate.k > 0); i++) await frames(1);
    out.closed = Math.max(ang(door), ang(tail));
    return out;
  });
  report(r.comps === 1138 && r.parts === 1138, 'las 1.138 piezas, todas con su explosión', `${r.comps} componentes · ${r.parts} explosionables`);
  report(r.dev === 0, 'la explosión vuelve exacta tras 1 → 0,37 → 0,8 → 0', `desviación ${r.dev} m`);
  report(r.idle === 0, 'en reposo no dibuja (dibujo bajo demanda)', `${r.idle} fotogramas en 20`);
  report(Math.abs(r.door - 65) < 0.5 && Math.abs(r.tail - 90) < 0.5 && r.closed < 1e-6 && r.drawnOpening > 0, 'las puertas (≈65°) y el portón (90°) abren y cierran sobre sus pivotes',
    `puerta ${r.door.toFixed(1)}° · portón ${r.tail.toFixed(1)}° · cerrados ${r.closed.toFixed(3)}°`);
  report(!errors.length, 'consola sin errores', errors.slice(0, 3).join(' | '));
} catch (e) {
  report(false, 'la prueba terminó', e.message.split('\n')[0]);
} finally {
  await browser.close();
  server.close();
}
process.exit(failed ? 1 : 0);
