// Visor interactivo del Cybertruck con vista explosionada.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { createLighting, createFloorReflector } from './lighting.js';
import {
  MODEL_URL, DRACO_URL, SYSTEM_LABELS, STAGES, STAGE_WINDOWS, FIDELITY, VIEWS,
} from './config.js';
import { enhanceMaterial } from './materials.js';

const $ = (id) => document.getElementById(id);
const state = {
  explode: 0, amp: 1.5, stageMask: { 1: true, 2: true, 3: true, 4: true, 5: true, 6: true },
  parts: [], components: new Map(), selected: null, hiddenSystems: new Set(), playing: false,
  anim: null, tris: 0, meshes: 0, floor: 'glass', env: 'studio', reflections: true,
};

// ---------------------------------------------------------------------------
// Escena
// ---------------------------------------------------------------------------
const canvas = $('viewport');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
// AgX: la misma transformación de vista que usan los renders de Blender (docs/renders)
renderer.toneMapping = THREE.AgXToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
// Equipos de sobremesa: sombras y reflejos a mayor resolución; móviles y tabletas: versión ligera
const HIGH_END = window.matchMedia('(pointer: fine)').matches && window.innerWidth >= 1100;

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(38, 1, 0.05, 200);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 0.4;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.98;
controls.screenSpacePanning = true;

const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(-6, 9, -5);
key.castShadow = true;
key.shadow.mapSize.set(HIGH_END ? 4096 : 2048, HIGH_END ? 4096 : 2048);
Object.assign(key.shadow.camera, { left: -6.5, right: 6.5, top: 6.5, bottom: -6.5, near: 1, far: 30 });
key.shadow.bias = -0.0003;
key.shadow.normalBias = 0.02;
key.shadow.radius = 3;
scene.add(key);
const hemi = new THREE.HemisphereLight(0xdfe6ee, 0x1a1c20, 0.25);
scene.add(hemi);
const lighting = createLighting(renderer, scene, key, hemi);

// Suelo: disco con degradado y receptor de sombras
function groundTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 512;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(256, 256, 10, 256, 256, 256);
  grd.addColorStop(0, '#2a2e34');
  grd.addColorStop(0.55, '#16191d');
  grd.addColorStop(1, '#0d0f12');
  g.fillStyle = grd;
  g.fillRect(0, 0, 512, 512);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
const ground = new THREE.Mesh(new THREE.CircleGeometry(26, 96),
  new THREE.MeshStandardMaterial({ map: groundTexture(), roughness: 0.9, metalness: 0 }));
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.002;
ground.receiveShadow = true;
scene.add(ground);
const grid = new THREE.GridHelper(24, 48, 0x2a2f36, 0x1b1e23);
grid.material.transparent = true;
grid.material.opacity = 0.35;
grid.position.y = 0.0;
scene.add(grid);

// Suelo de cristal: lámina translúcida y ligeramente reflectante que deja ver las piezas que bajan del plano
// del suelo al explosionar (suspensión, tren motriz, batería, bajos). Se desvanece hacia el borde.
function glassFadeTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, '#ffffff');
  grd.addColorStop(0.45, '#bdbdbd');
  grd.addColorStop(1, '#000000');
  g.fillStyle = grd;
  g.fillRect(0, 0, 256, 256);
  return new THREE.CanvasTexture(c);
}
const glassFloor = new THREE.Mesh(new THREE.CircleGeometry(16, 96), new THREE.MeshPhysicalMaterial({
  color: 0x8fa3b6, metalness: 0, roughness: 0.12, transparent: true, opacity: 0.24, alphaMap: glassFadeTexture(),
  clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 1.4, side: THREE.DoubleSide, depthWrite: false,
}));
glassFloor.rotation.x = -Math.PI / 2;
glassFloor.position.y = -0.002;
glassFloor.renderOrder = 2;
scene.add(glassFloor);
// Sombra de contacto sobre el cristal (receptor de sombras invisible salvo la propia sombra)
const shadowCatcher = new THREE.Mesh(new THREE.CircleGeometry(10, 64), new THREE.ShadowMaterial({ opacity: 0.32 }));
shadowCatcher.rotation.x = -Math.PI / 2;
shadowCatcher.position.y = -0.001;
shadowCatcher.receiveShadow = true;
shadowCatcher.renderOrder = 3;
scene.add(shadowCatcher);

// Reflejo plano real sobre el suelo (vuelve a dibujar la escena reflejada: se puede desactivar)
const reflector = createFloorReflector(14, HIGH_END ? 0.5 : 0.35);
scene.add(reflector);

function savePref(k, v) { try { localStorage.setItem(k, v); } catch { /* almacenamiento no disponible */ } }
function loadPref(k) { try { return localStorage.getItem(k); } catch { return null; } }

const groundMap = ground.material.map;
function setEnvironment(name) {
  const e = lighting.apply(name);
  state.env = name;
  // suelo opaco: degradado oscuro de estudio o pavimento claro al aire libre
  ground.material.map = name === 'exterior' ? null : groundMap;
  ground.material.color.set(name === 'exterior' ? 0x8b9096 : 0xffffff);
  ground.material.needsUpdate = true;
  glassFloor.material.color.set(name === 'exterior' ? 0xc7d3de : 0x8fa3b6);
  document.querySelectorAll('[data-env]').forEach((b) => {
    const on = b.dataset.env === name;
    b.classList.toggle('active', on);
    b.setAttribute('aria-pressed', String(on));
  });
  // el HUD sigue al ambiente: vidrio oscuro en el estudio y vidrio claro al aire libre
  document.body.dataset.env = name;
  const meta = document.querySelector('meta[name=theme-color]');
  if (meta) meta.setAttribute('content', name === 'exterior' ? '#b9c7d6' : '#0b0d10');
  savePref('ct-env', name);
  syncSegs();
  return e;
}

function setReflections(on) {
  state.reflections = !!on;
  updateReflector();
  document.querySelectorAll('[data-refl]').forEach((b) => {
    const act = (b.dataset.refl === 'on') === state.reflections;
    b.classList.toggle('active', act);
    b.setAttribute('aria-pressed', String(act));
  });
  savePref('ct-refl', state.reflections ? 'on' : 'off');
  syncSegs();
}

function updateReflector() {
  reflector.visible = state.reflections && state.floor !== 'hidden';
  reflector.setStrength(state.floor === 'glass' ? 0.24 : 0.14);
}

const FLOOR_MODES = ['glass', 'opaque', 'hidden'];
function setFloor(mode) {
  if (!FLOOR_MODES.includes(mode)) mode = 'glass';
  state.floor = mode;
  ground.visible = mode === 'opaque';
  glassFloor.visible = mode === 'glass';
  shadowCatcher.visible = mode === 'glass';
  grid.visible = mode !== 'hidden';
  grid.material.opacity = mode === 'glass' ? 0.22 : 0.35;
  updateReflector();
  // Con el suelo transparente u oculto la cámara puede rodear el vehículo también por debajo
  controls.maxPolarAngle = mode === 'opaque' ? Math.PI * 0.98 : Math.PI;
  document.querySelectorAll('[data-floor]').forEach((b) => {
    const on = b.dataset.floor === mode;
    b.classList.toggle('active', on);
    b.setAttribute('aria-pressed', String(on));
  });
  savePref('ct-floor', mode);
  syncSegs();
}

// ---------------------------------------------------------------------------
// Utilidades
// ---------------------------------------------------------------------------
const smoothstep = (a, b, x) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
// Blender (+X, +Y delante, +Z arriba) -> glTF (+X, +Y arriba, -Z delante)
const b2g = (v) => new THREE.Vector3(v[0], v[2], -v[1]);

function setStatus() {
  const pct = Math.round(state.explode * 100);
  const active = Object.entries(STAGE_WINDOWS)
    .filter(([s, [a]]) => state.explode > a && state.stageMask[s]).map(([s]) => s);
  const sel = state.selected ? state.selected.userData.label_es || state.selected.name : '—';
  // Con textContent: la etiqueta de una pieza es texto del modelo, no HTML (auditoría C8).
  $('status').replaceChildren(...[
    pct === 0 ? 'Ensamblado' : pct === 100 ? 'Totalmente explosionado' : `Explosión ${pct} %`,
    `Etapas activas: ${active.length ? active.join(', ') : 'ninguna'}`,
    `Seleccionado: ${sel}`,
    `${state.meshes} mallas · ${(state.tris / 1000).toFixed(0)} k triángulos`,
  ].map((t) => Object.assign(document.createElement('span'), { textContent: t })));
  $('explode-out').textContent = `${pct} %`;
  $('explode').style.setProperty('--p', `${state.explode * 100}%`);
  document.querySelectorAll('.stage').forEach((el) => {
    const s = el.dataset.stage;
    const [a, b] = STAGE_WINDOWS[s];
    // relleno de cada etapa = su avance dentro de la ventana de explosión
    el.style.setProperty('--k', state.stageMask[s] ? smoothstep(a, b, state.explode).toFixed(3) : 0);
    el.classList.toggle('on', state.explode > a && state.stageMask[s]);
    el.classList.toggle('masked', !state.stageMask[s]);
    el.setAttribute('aria-pressed', String(!!state.stageMask[s]));
  });
}

// Controles segmentados: el indicador se desliza bajo el botón activo
function syncSeg(seg) {
  const ind = seg.querySelector('.seg-ind');
  const act = seg.querySelector('.seg-btn.active');
  if (!ind) return;
  if (!act || !act.offsetWidth) { ind.classList.remove('ready'); return; }
  // la primera colocación (o tras estar oculto) es inmediata; los cambios posteriores se deslizan
  const first = !ind.classList.contains('ready');
  if (first) ind.style.transition = 'none';
  ind.style.width = `${act.offsetWidth}px`;
  ind.style.transform = `translateX(${act.offsetLeft}px)`;
  ind.classList.add('ready');
  if (first) { void ind.offsetWidth; ind.style.transition = ''; }
}
function syncSegs() { document.querySelectorAll('.seg').forEach(syncSeg); }

// ---------------------------------------------------------------------------
// Vista explosionada: posición = base + dirección · distancia · amplitud · suavizado(etapa)
// Es una función pura del parámetro: no acumula error al mover el control repetidamente.
// ---------------------------------------------------------------------------
function applyExplode() {
  const e = state.explode;
  for (const p of state.parts) {
    const [a, b] = STAGE_WINDOWS[p.stage] || [0, 1];
    const k = state.stageMask[p.stage] ? smoothstep(a, b, e) * p.dist * state.amp : 0;
    p.obj.position.copy(p.base).addScaledVector(p.dir, k);
  }
  setStatus();
}

// ---------------------------------------------------------------------------
// Selección y resaltado
// ---------------------------------------------------------------------------
const HL = new THREE.Color(0xff8a3d);
function forEachMesh(obj, fn) { obj.traverse((o) => { if (o.isMesh) fn(o); }); }

// Una copia resaltada por material de origen, compartida y reutilizada: clonar uno por malla en cada
// selección recompilaba sombreadores y daba un tirón al elegir conjuntos grandes (auditoría C12).
const highlights = new Map();
function highlighted(src) {
  let h = highlights.get(src);
  if (!h) {
    h = src.clone();
    h.emissive = HL.clone();
    h.emissiveIntensity = 0.35;
    highlights.set(src, h);
  }
  return h;
}
function highlight(obj, on) {
  forEachMesh(obj, (m) => {
    if (on) {
      if (!m.userData.__orig) {
        m.userData.__orig = m.material;
        m.material = Array.isArray(m.material) ? m.material.map(highlighted) : highlighted(m.material);
      }
    } else if (m.userData.__orig) {
      m.material = m.userData.__orig;
      delete m.userData.__orig;
    }
  });
}

function componentOf(o) {
  let c = o;
  while (c && !(c.userData && (c.userData.label_es || c.userData.explode_dir))) c = c.parent;
  return c;
}

function select(obj) {
  if (state.selected) highlight(state.selected, false);
  state.selected = obj || null;
  document.querySelectorAll('.item.sel').forEach((el) => el.classList.remove('sel'));
  if (obj) {
    highlight(obj, true);
    const ud = obj.userData;
    const f = FIDELITY[ud.fidelity] || { label: 'Sin clasificar', cls: '' };
    $('info-fid').textContent = f.label;
    $('info-fid').className = 'pill ' + f.cls;
    $('info-title').textContent = ud.label_es || obj.name;
    $('info-name').textContent = obj.name;
    $('info-system').textContent = SYSTEM_LABELS[ud.system] || ud.system || '—';
    $('info-group').textContent = ud.explode_group || '—';
    $('info-stage').textContent = ud.explode_stage ? `${ud.explode_stage} · ${STAGES[ud.explode_stage]}` : '—';
    $('info-note').textContent = ud.note_es || ({
      V: 'Respaldado por documentación oficial (dimensiones o especificación).',
      R: 'Reconstruido a partir de vistas oficiales y fotografías coherentes entre sí.',
      A: 'Interpretación razonada: la geometría exacta no está documentada públicamente.',
    })[ud.fidelity] || '';
    $('info').classList.remove('hidden');
    const el = document.querySelector(`.item[data-name="${CSS.escape(obj.name)}"]`);
    if (el) { el.classList.add('sel'); el.scrollIntoView({ block: 'nearest' }); }
  } else {
    $('info').classList.add('hidden');
  }
  setStatus();
}

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
let downAt = null;
canvas.addEventListener('pointerdown', (ev) => { downAt = [ev.clientX, ev.clientY]; });
canvas.addEventListener('pointerup', (ev) => {
  if (!downAt || Math.hypot(ev.clientX - downAt[0], ev.clientY - downAt[1]) > 5) return;
  const r = canvas.getBoundingClientRect();
  pointer.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(vehicle ? [vehicle] : [], true).filter((h) => h.object.visible && isVisible(h.object));
  select(hits.length ? componentOf(hits[0].object) : null);
});
function isVisible(o) { while (o) { if (!o.visible) return false; o = o.parent; } return true; }

// ---------------------------------------------------------------------------
// Cámara
// ---------------------------------------------------------------------------
function flyTo(view, ms = 900) {
  const v = VIEWS[view];
  if (!v) return;
  const p0 = camera.position.clone(), t0 = controls.target.clone();
  const p1 = new THREE.Vector3(...v.pos), t1 = new THREE.Vector3(...v.target);
  // En pantallas verticales (tabletas, móviles) se aleja la cámara para encuadrar el vehículo
  if (!v.fov && camera.aspect < 1.3) {
    p1.sub(t1).multiplyScalar(Math.pow(1.3 / camera.aspect, 0.85)).add(t1);
  }
  const f0 = camera.fov, f1 = v.fov || 38;
  const start = performance.now();
  state.anim = (now) => {
    const k = smoothstep(0, 1, (now - start) / ms);
    camera.position.lerpVectors(p0, p1, k);
    controls.target.lerpVectors(t0, t1, k);
    camera.fov = f0 + (f1 - f0) * k;
    camera.updateProjectionMatrix();
    if (k >= 1) state.anim = null;
  };
  document.querySelectorAll('[data-view]').forEach((b) => b.classList.toggle('active', b.dataset.view === view));
  syncSegs();
}

function focusOn(obj) {
  const box = new THREE.Box3().setFromObject(obj);
  if (box.isEmpty()) return;
  const c = box.getCenter(new THREE.Vector3());
  const r = Math.max(0.25, box.getSize(new THREE.Vector3()).length() * 0.9);
  const dir = camera.position.clone().sub(controls.target).normalize();
  const p0 = camera.position.clone(), t0 = controls.target.clone();
  const p1 = c.clone().addScaledVector(dir, r * 1.6);
  const start = performance.now();
  state.anim = (now) => {
    const k = smoothstep(0, 1, (now - start) / 700);
    camera.position.lerpVectors(p0, p1, k);
    controls.target.lerpVectors(t0, c, k);
    if (k >= 1) state.anim = null;
  };
}

// ---------------------------------------------------------------------------
// Interfaz: sistemas, árbol, ficha
// ---------------------------------------------------------------------------
function buildUI() {
  // Etapas
  const st = $('stages');
  st.innerHTML = '';
  for (const [k, label] of Object.entries(STAGES)) {
    const d = document.createElement('button');
    d.className = 'stage';
    d.dataset.stage = k;
    d.title = `${label}: pulsa para incluir o excluir esta etapa de la explosión`;
    d.setAttribute('aria-label', `Etapa ${k}, ${label}`);
    d.innerHTML = `<b>${k}</b><span>${label}</span>`;
    d.addEventListener('click', () => { state.stageMask[k] = !state.stageMask[k]; applyExplode(); });
    st.appendChild(d);
  }
  // Agrupación por sistema
  const bySystem = new Map();
  for (const [name, obj] of state.components) {
    const sys = obj.userData.system || 'OTROS';
    if (!bySystem.has(sys)) bySystem.set(sys, []);
    bySystem.get(sys).push(obj);
  }
  const order = Object.keys(SYSTEM_LABELS);
  const systems = [...bySystem.keys()].sort((a, b) => order.indexOf(a) - order.indexOf(b));
  const sysBox = $('systems');
  sysBox.innerHTML = '';
  const tree = $('tree');
  tree.innerHTML = '';
  for (const [si, sys] of systems.entries()) {
    const chip = document.createElement('button');
    chip.className = 'sys';
    // un tono por sistema, repartido por el círculo cromático
    chip.style.setProperty('--c', `hsl(${Math.round((si * 360) / systems.length + 18) % 360} 72% 62%)`);
    chip.setAttribute('aria-pressed', 'true');
    chip.append(Object.assign(document.createElement('span'), { className: 'dot' }), Object.assign(document.createElement('span'), { textContent: SYSTEM_LABELS[sys] || sys }));
    chip.addEventListener('click', () => toggleSystem(sys, chip));
    chip.dataset.sys = sys;
    sysBox.appendChild(chip);

    const det = document.createElement('details');
    const items = bySystem.get(sys).sort((a, b) => (a.userData.label_es || a.name).localeCompare(b.userData.label_es || b.name, 'es'));
    const sum = document.createElement('summary');
    sum.append(Object.assign(document.createElement('span'), { textContent: SYSTEM_LABELS[sys] || sys }), Object.assign(document.createElement('span'), { className: 'n', textContent: String(items.length) }));
    det.appendChild(sum);
    for (const obj of items) {
      const it = document.createElement('div');
      it.className = 'item';
      it.dataset.name = obj.name;
      it.dataset.search = `${obj.name} ${obj.userData.label_es || ''}`.toLowerCase();
      const f = FIDELITY[obj.userData.fidelity];
      // Nodos creados uno a uno y textos con textContent: una comilla en una etiqueta ya no rompe el HTML (C8).
      const label = Object.assign(document.createElement('span'), { className: 'label', title: obj.name, textContent: obj.userData.label_es || obj.name });
      it.appendChild(label);
      if (f) it.appendChild(Object.assign(document.createElement('span'), { className: `fid ${f.cls}`, title: f.label, textContent: obj.userData.fidelity }));
      const eye = Object.assign(document.createElement('button'), { className: 'eye', title: 'Mostrar u ocultar' });
      eye.setAttribute('aria-label', `Mostrar u ocultar ${obj.userData.label_es || obj.name}`);
      eye.innerHTML = '<svg><use href="#i-eye"/></svg>';
      it.appendChild(eye);
      it.querySelector('.label').addEventListener('click', () => { select(obj); });
      it.querySelector('.eye').addEventListener('click', (ev) => {
        ev.stopPropagation();
        obj.visible = !obj.visible;
        it.classList.toggle('hiddenpart', !obj.visible);
      });
      det.appendChild(it);
    }
    tree.appendChild(det);
  }
  $('count').textContent = `${state.components.size}`;
  $('search').addEventListener('input', (ev) => {
    const q = ev.target.value.trim().toLowerCase();
    tree.querySelectorAll('details').forEach((d) => {
      let any = false;
      d.querySelectorAll('.item').forEach((it) => {
        const ok = !q || it.dataset.search.includes(q);
        it.style.display = ok ? '' : 'none';
        any ||= ok;
      });
      d.style.display = any ? '' : 'none';
      if (q) d.open = any;
    });
  });
}

function toggleSystem(sys, chip) {
  const off = !state.hiddenSystems.has(sys);
  if (off) state.hiddenSystems.add(sys); else state.hiddenSystems.delete(sys);
  chip.classList.toggle('off', off);
  chip.setAttribute('aria-pressed', String(!off));
  for (const obj of state.components.values()) {
    if (obj.userData.system === sys) obj.visible = !off;
  }
  syncTreeVisibility();
}

function syncTreeVisibility() {
  document.querySelectorAll('.item').forEach((it) => {
    const o = state.components.get(it.dataset.name);
    it.classList.toggle('hiddenpart', o && !o.visible);
  });
}

function showAll() {
  for (const o of state.components.values()) o.visible = true;
  state.hiddenSystems.clear();
  document.querySelectorAll('.sys').forEach((c) => { c.classList.remove('off'); c.setAttribute('aria-pressed', 'true'); });
  syncTreeVisibility();
}

function isolate(obj) {
  // Aislar sustituye a lo que se hubiera ocultado por sistema: los chips lo reflejan (auditoría C11).
  state.hiddenSystems.clear();
  document.querySelectorAll('.sys').forEach((c) => { c.classList.remove('off'); c.setAttribute('aria-pressed', 'true'); });
  for (const o of state.components.values()) o.visible = false;
  // el objeto, sus antepasados y sus descendientes permanecen visibles
  let p = obj;
  while (p) { p.visible = true; p = p.parent; }
  obj.traverse((o) => { o.visible = true; });
  syncTreeVisibility();
  focusOn(obj);
}

// ---------------------------------------------------------------------------
// Carga del modelo
// ---------------------------------------------------------------------------
let vehicle = null;

/**
 * Descarga el GLB en una sola petición, leída como flujo. GitHub Pages lo sirve comprimido con gzip,
 * y entonces Content-Length es el tamaño comprimido (9,2 de 12,5 MB) mientras el flujo entrega los
 * bytes ya descomprimidos: la barra llegaba al 136 % (auditoría C1). Con una codificación de
 * transferencia no hay total fiable, así que la barra pasa a indeterminada y el texto da los MB.
 */
async function fetchModel() {
  const res = await fetch(MODEL_URL);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const length = Number(res.headers.get('content-length')) || 0;
  const encoded = !!res.headers.get('content-encoding');
  const total = encoded ? 0 : length;
  $('loader').classList.toggle('indeterminate', !total);
  if (!res.body) return res.arrayBuffer();
  const reader = res.body.getReader(), chunks = [];
  let got = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    got += value.length;
    const mb = `${(got / 1e6).toFixed(2)} MB`;
    if (total) {
      const p = Math.min(100, Math.round((got / total) * 100));
      $('bar-fill').style.width = `${p}%`;
      $('loader-text').textContent = `${p} % · ${mb}`;
    } else $('loader-text').textContent = `${mb} recibidos`;
  }
  const data = new Uint8Array(got);
  let o = 0;
  for (const c of chunks) { data.set(c, o); o += c.length; }
  $('loader').classList.remove('indeterminate');
  $('bar-fill').style.width = '100%';
  $('loader-text').textContent = 'Descomprimiendo la geometría…';
  return data.buffer;
}

async function load() {
  const draco = new DRACOLoader().setDecoderPath(DRACO_URL);
  const loader = new GLTFLoader().setDRACOLoader(draco);
  // El manifiesto ya no se descarga: la interfaz lee todo de los extras del GLB (auditoría C3).
  const gltf = await loader.parseAsync(await fetchModel(), '');
  draco.dispose();
  vehicle = gltf.scene;
  const matCache = new Map();
  vehicle.traverse((o) => {
    if (o.isMesh) {
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      const out = mats.map((m) => {
        if (!matCache.has(m.uuid)) matCache.set(m.uuid, enhanceMaterial(m));
        return matCache.get(m.uuid);
      });
      o.material = Array.isArray(o.material) ? out : out[0];
      const transparent = out.some((m) => m.transmission > 0);
      o.castShadow = !transparent;
      o.receiveShadow = true;
      state.meshes += 1;
      const g = o.geometry;
      state.tris += (g.index ? g.index.count : g.attributes.position.count) / 3;
    }
    const ud = o.userData;
    if (ud && (ud.label_es || ud.explode_dir)) {
      state.components.set(o.name, o);
      if (ud.explode_dir && ud.explode_dist) {
        state.parts.push({
          obj: o, base: o.position.clone(), dir: b2g(ud.explode_dir).normalize(),
          dist: Number(ud.explode_dist), stage: Number(ud.explode_stage) || 1,
        });
      }
    }
  });
  scene.add(vehicle);
  // Gancho de inspección para pruebas automatizadas (solo lectura del estado y utilidades)
  window.__ct = { state, applyExplode, select, isolate, showAll, setFloor, setEnvironment, setReflections, camera,
    controls, THREE };
  buildUI();
  flyTo('front34', 1);
  applyExplode();
  $('loader').classList.add('done');
  setTimeout(() => $('loader').remove(), 500);
}

// ---------------------------------------------------------------------------
// Controles
// ---------------------------------------------------------------------------
function setPlaying(on) {
  state.playing = on;
  const b = $('btn-play');
  b.querySelector('use').setAttribute('href', on ? '#i-pause' : '#i-play');
  b.setAttribute('aria-label', on ? 'Pausar la animación' : 'Animar la explosión');
  b.setAttribute('aria-pressed', String(on));
}
$('explode').addEventListener('input', (ev) => {
  setPlaying(false);
  state.explode = Number(ev.target.value) / 100;
  applyExplode();
});
const fmtAmp = (v) => `${v.toFixed(2).replace(/0$/, '').replace('.', ',')}×`;
$('amp').addEventListener('input', (ev) => {
  state.amp = Number(ev.target.value);
  $('amp').style.setProperty('--p', `${((state.amp - 0.6) / 1.8) * 100}%`);
  $('amp-out').textContent = fmtAmp(state.amp);
  applyExplode();
});
$('amp').style.setProperty('--p', `${((state.amp - 0.6) / 1.8) * 100}%`);
$('btn-assemble').addEventListener('click', () => {
  setPlaying(false);
  animateExplodeTo(0);
});
let playDir = 1;
$('btn-play').addEventListener('click', () => {
  setPlaying(!state.playing);
  playDir = state.explode >= 1 ? -1 : 1;
});

// Panel lateral: abierto en pantallas amplias, recogido en tabletas y móviles
function setPanel(open) {
  $('panel').classList.toggle('open', open);
  $('btn-panel').setAttribute('aria-expanded', String(open));
  if (open) requestAnimationFrame(syncSegs);
}
setPanel(window.innerWidth > 1180);
document.querySelectorAll('.tabs .seg-btn').forEach((t) => t.addEventListener('click', () => {
  document.querySelectorAll('.tabs .seg-btn').forEach((o) => {
    const on = o === t;
    o.classList.toggle('active', on);
    o.setAttribute('aria-selected', String(on));
    $(o.dataset.tab).classList.toggle('hidden', !on);
  });
  syncSegs();
  if (t.dataset.tab === 'components-tab') $('search').focus({ preventScroll: true });
}));

// Menú emergente de escena (suelo, luz, reflejos y amplitud), anclado al botón que lo abre
function placePopover() {
  const pop = $('scene-pop'), btn = $('btn-scene');
  const r = btn.getBoundingClientRect();
  const dock = document.querySelector('.dock').getBoundingClientRect();
  const w = pop.offsetWidth, h = pop.offsetHeight, m = 10;
  // encima de la base, alineado con el botón que lo abre
  pop.style.left = `${Math.max(m, Math.min(window.innerWidth - w - m, r.right + 12 - w))}px`;
  pop.style.top = `${Math.max(m, dock.top - h - 10)}px`;
}
function setPopover(open) {
  $('scene-pop').classList.toggle('hidden', !open);
  $('btn-scene').setAttribute('aria-expanded', String(open));
  if (open) { placePopover(); syncSegs(); }
}
$('btn-scene').addEventListener('click', (ev) => {
  ev.stopPropagation();
  setPopover($('scene-pop').classList.contains('hidden'));
});
document.addEventListener('pointerdown', (ev) => {
  if ($('scene-pop').classList.contains('hidden')) return;
  if (!$('scene-pop').contains(ev.target) && !$('btn-scene').contains(ev.target)) setPopover(false);
});
let tween = null;
function animateExplodeTo(target, ms = 900) {
  const from = state.explode, start = performance.now();
  tween = (now) => {
    const k = smoothstep(0, 1, (now - start) / ms);
    state.explode = from + (target - from) * k;
    $('explode').value = state.explode * 100;
    applyExplode();
    if (k >= 1) tween = null;
  };
}
document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => flyTo(b.dataset.view)));
document.querySelectorAll('[data-floor]').forEach((b) => b.addEventListener('click', () => setFloor(b.dataset.floor)));
document.querySelectorAll('[data-env]').forEach((b) => b.addEventListener('click', () => setEnvironment(b.dataset.env)));
document.querySelectorAll('[data-refl]').forEach((b) => b.addEventListener('click', () => setReflections(b.dataset.refl === 'on')));
setEnvironment(loadPref('ct-env') || 'studio');
setFloor(loadPref('ct-floor') || 'glass');
setReflections((loadPref('ct-refl') || (HIGH_END ? 'on' : 'off')) === 'on');
$('btn-reset-view').addEventListener('click', () => flyTo(state.explode > 0.3 ? 'exploded' : 'front34'));
$('btn-show-all').addEventListener('click', showAll);
$('btn-panel').addEventListener('click', () => setPanel(!$('panel').classList.contains('open')));
$('info-close').addEventListener('click', () => select(null));
$('btn-isolate').addEventListener('click', () => state.selected && isolate(state.selected));
$('btn-hide').addEventListener('click', () => {
  if (!state.selected) return;
  const o = state.selected;
  select(null);
  o.visible = false;
  syncTreeVisibility();
});
$('btn-focus').addEventListener('click', () => state.selected && focusOn(state.selected));
window.addEventListener('keydown', (ev) => {
  if (ev.key === 'Escape') {
    if (!$('scene-pop').classList.contains('hidden')) { setPopover(false); $('btn-scene').focus(); return; }
    select(null);
    return;
  }
  if (ev.target.tagName === 'INPUT' || ev.target.tagName === 'BUTTON') return;
  if (ev.key === 'r' || ev.key === 'R') flyTo('front34');
  if (ev.key === ' ') { ev.preventDefault(); $('btn-play').click(); }
});
document.fonts?.ready.then(syncSegs);

// ---------------------------------------------------------------------------
// Bucle de render
// ---------------------------------------------------------------------------
function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  reflector.resize(w, h);
  syncSegs();
  if (!$('scene-pop').classList.contains('hidden')) placePopover();
}
window.addEventListener('resize', resize);
resize();

let last = performance.now();
renderer.setAnimationLoop((now) => {
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;
  if (state.anim) state.anim(now);
  if (tween) tween(now);
  if (state.playing) {
    state.explode = Math.min(1, Math.max(0, state.explode + playDir * dt / 4.0));
    if (state.explode >= 1 || state.explode <= 0) playDir *= -1;
    $('explode').value = state.explode * 100;
    applyExplode();
  }
  controls.update();
  renderer.render(scene, camera);
});

// Liberación de recursos al abandonar la página
// Solo si la página no queda en la caché de ida y vuelta: si vuelve con «Atrás» (persisted), debe
// seguir con su bucle y sus recursos, no con un lienzo negro (auditoría C4).
window.addEventListener('pagehide', (ev) => {
  if (ev.persisted) return;
  renderer.setAnimationLoop(null);
  scene.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) {
      for (const k of Object.keys(m)) if (m[k] && m[k].isTexture) m[k].dispose();
      m.dispose();
    }
  });
  lighting.dispose();
  reflector.dispose();
  renderer.dispose();
});

load().catch((err) => {
  console.error(err);
  $('loader').classList.add('error');
  $('loader').querySelector('.loader-title').textContent = 'No se pudo cargar el modelo';
  $('loader-text').textContent = String(err && err.message ? err.message : err);
});
