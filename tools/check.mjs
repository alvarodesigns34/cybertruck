// Comprobación del visor y del modelo exportado, sin dependencias ni navegador (auditoría del 20-10-2026, C10).
// La ejecuta el CI antes de publicar: una exportación con un extra perdido, un manifiesto desfasado, una
// dependencia de CDN o un error de sintaxis ya no llegan a producción sin aviso.
// Uso: node tools/check.mjs
import { readFile, readdir, stat } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';

let failed = 0;
const report = (ok, name, detail = '') => {
  console.log(`${ok ? 'OK   ' : 'FALLO'} ${name}${detail ? ` — ${detail}` : ''}`);
  if (!ok) failed++;
};

async function readGlb(path) {
  const buf = await readFile(path);
  if (buf.readUInt32LE(0) !== 0x46546c67) throw new Error(`${path}: no es un glTF binario`);
  const len = buf.readUInt32LE(12);
  return { json: JSON.parse(buf.subarray(20, 20 + len).toString('utf8')), bytes: buf.length };
}

// ---- El GLB: extensiones, árbol y extras de cada pieza.
const { json, bytes } = await readGlb('web/models/cybertruck.glb');
{
  const CAN = new Set(['KHR_draco_mesh_compression', 'KHR_texture_transform', 'EXT_texture_webp']);
  const extra = (json.extensionsRequired ?? []).filter((e) => !CAN.has(e));
  report(!extra.length, 'extensiones requeridas que el visor sabe leer', extra.length ? `sin soporte: ${extra.join(', ')}` : (json.extensionsRequired ?? []).join(', '));
  const roots = json.scenes[json.scene ?? 0].nodes.map((i) => json.nodes[i]);
  report(roots.length === 1 && roots[0].name === 'CYBERTRUCK_ROOT', 'una sola raíz, CYBERTRUCK_ROOT', roots.map((r) => r.name).join(', '));
  const names = json.nodes.map((n) => n.name);
  report(new Set(names).size === names.length, 'nombres de nodo únicos', `${names.length} nodos`);
  const windows = roots[0].extras?.explode_stage_windows ?? {};
  const stages = Object.keys(windows).map(Number);
  const parts = json.nodes.filter((n) => n !== roots[0]);
  const wrong = [];
  for (const n of parts) {
    const x = n.extras ?? {}, d = x.explode_dir ?? [];
    if (!x.system) wrong.push(`${n.name}: system`);
    else if (!stages.includes(x.explode_stage)) wrong.push(`${n.name}: explode_stage`);
    else if (d.length !== 3 || Math.abs(Math.hypot(...d) - 1) > 1e-3) wrong.push(`${n.name}: explode_dir`);
    else if (!(x.explode_dist > 0)) wrong.push(`${n.name}: explode_dist`);
    else if (!['V', 'R', 'A'].includes(x.fidelity)) wrong.push(`${n.name}: fidelity`);
    else if (!x.label_es) wrong.push(`${n.name}: label_es`);
  }
  report(stages.length === 6 && !wrong.length, 'cada pieza lleva sistema, etapa, dirección y distancia de explosión, fidelidad y etiqueta',
    wrong.length ? `${wrong.length} mal: ${wrong.slice(0, 4).join('; ')}` : `${parts.length} piezas`);
  const rotated = json.nodes.filter((n) => n.children?.length && n.rotation && Math.abs(n.rotation[3]) < 1 - 1e-9);
  report(!rotated.length, 'los conjuntos padre no tienen rotación (regla de CLAUDE.md)', rotated.map((n) => n.name).slice(0, 5).join(', ') || 'ninguno');
  // Texturas con texCoord −1 (primitivas sin UV que el validador de Khronos rechaza: C21).
  const negTex = [];
  for (const m of json.materials ?? []) {
    const walk = (o, path) => {
      if (!o || typeof o !== 'object') return;
      if (Object.prototype.hasOwnProperty.call(o, 'index') && o.texCoord !== undefined && o.texCoord < 0) negTex.push(`${m.name}.${path}`);
      for (const [k, v] of Object.entries(o)) walk(v, path ? `${path}.${k}` : k);
    };
    walk(m, '');
  }
  report(!negTex.length, 'ninguna textura con texCoord negativo (todas las piezas texturadas tienen UV)', negTex.length ? `${negTex.length}: ${negTex.slice(0, 3).join(', ')}` : 'ninguna');
  report(true, 'tamaño del GLB', `${(bytes / 1e6).toFixed(2)} MB`);

  // ---- El manifiesto, coherente con el GLB (lo usan el inventario y las herramientas).
  const man = JSON.parse(await readFile('web/models/cybertruck-manifest.json', 'utf8'));
  const byName = new Map(parts.map((n) => [n.name, n.extras]));
  const diff = man.components.filter((c) => {
    const x = byName.get(c.name);
    return !x || x.system !== c.system || x.fidelity !== c.fidelity || x.explode_stage !== c.stage || x.label_es !== c.label
      || x.explode_dist !== c.explode_dist || JSON.stringify(x.explode_dir) !== JSON.stringify(c.explode_dir_blender);
  });
  report(man.components.length === parts.length && !diff.length, 'el manifiesto coincide con el GLB (nombre, sistema, fidelidad, etapa, etiqueta y explosión)',
    diff.length ? `${diff.length} diferencias: ${diff.slice(0, 3).map((c) => c.name).join(', ')}` : `${man.components.length} componentes`);
}

// ---- El visor: nada de CDN, y lo que importa existe en web/vendor/.
{
  const files = [];
  const walk = async (dir) => {
    for (const e of await readdir(dir, { withFileTypes: true })) {
      const p = join(dir, e.name);
      if (e.isDirectory()) { if (p !== join('web', 'vendor')) await walk(p); } else if (/\.(html|js|css)$/.test(e.name)) files.push(p);
    }
  };
  await walk('web');
  const cdn = [];
  for (const f of files) {
    const t = await readFile(f, 'utf8');
    if (/https?:\/\/(cdn\.|unpkg|fonts\.googleapis|fonts\.gstatic|esm\.sh|ga\.jspm)/.test(t)) cdn.push(f);
  }
  report(!cdn.length, 'el visor no carga nada de CDN (Three.js, Draco y tipografías en web/vendor/)', cdn.join(', ') || `${files.length} archivos revisados`);
  const need = ['three/build/three.module.js', 'three/examples/jsm/controls/OrbitControls.js', 'three/examples/jsm/loaders/GLTFLoader.js',
    'three/examples/jsm/loaders/DRACOLoader.js', 'three/examples/jsm/objects/Reflector.js', 'three/examples/jsm/utils/BufferGeometryUtils.js',
    'three/examples/jsm/libs/draco/gltf/draco_decoder.wasm', 'three/examples/jsm/libs/draco/gltf/draco_wasm_wrapper.js', 'fonts/fonts.css'];
  const missing = [];
  for (const f of need) if (!(await stat(join('web', 'vendor', f)).catch(() => null))) missing.push(f);
  report(!missing.length, 'las dependencias del visor están en web/vendor/', missing.join(', ') || `${need.length} archivos`);
  const css = await readFile('web/vendor/fonts/fonts.css', 'utf8');
  const fontsMissing = [];
  for (const [, f] of css.matchAll(/url\(\.\/([^)]+)\)/g)) if (!(await stat(join('web', 'vendor', 'fonts', f)).catch(() => null))) fontsMissing.push(f);
  report(!fontsMissing.length, 'cada tipografía de fonts.css existe', fontsMissing.join(', ') || 'todas');
  // Sintaxis de cada módulo propio (node --check analiza sin ejecutar).
  const bad = [];
  for (const f of [...files.filter((f) => f.endsWith('.js')), ...(await readdir('tools')).filter((f) => f.endsWith('.mjs')).map((f) => join('tools', f))]) {
    try { execFileSync(process.execPath, ['--check', f], { stdio: 'pipe' }); } catch (e) { bad.push(`${f}: ${String(e.stderr).split('\n').find((l) => /Error/.test(l)) ?? 'error'}`); }
  }
  report(!bad.length, 'sin errores de sintaxis en el visor ni en tools/', bad.join(' | ') || 'todo correcto');
}

process.exit(failed ? 1 : 0);
