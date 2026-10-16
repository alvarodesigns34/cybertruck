// Visor interactivo del Cybertruck con vista explosionada.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import {
  MODEL_URL, MANIFEST_URL, DRACO_URL, SYSTEM_LABELS, STAGES, STAGE_WINDOWS, FIDELITY, VIEWS,
} from './config.js';
import { enhanceMaterial } from './materials.js';

const $ = (id) => document.getElementById(id);
const state = {
  explode: 0, amp: 1.5, stageMask: { 1: true, 2: true, 3: true, 4: true, 5: true, 6: true },
  parts: [], components: new Map(), selected: null, hiddenSystems: new Set(), playing: false,
  anim: null, tris: 0, meshes: 0,
};

// ---------------------------------------------------------------------------
// Escena
// ---------------------------------------------------------------------------
const canvas = $('viewport');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d0f12);
scene.fog = new THREE.Fog(0x0d0f12, 22, 60);

const pmrem = new THREE.PMREMGenerator(renderer);
const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environment = envTex;
scene.environmentIntensity = 0.85;

const camera = new THREE.PerspectiveCamera(38, 1, 0.05, 200);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 0.4;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.98;
controls.screenSpacePanning = true;

const key = new THREE.DirectionalLight(0xffffff, 1.6);
key.position.set(-6, 9, -5);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -7, right: 7, top: 7, bottom: -7, near: 1, far: 30 });
key.shadow.bias = -0.0004;
key.shadow.normalBias = 0.02;
scene.add(key);
scene.add(new THREE.HemisphereLight(0xdfe6ee, 0x1a1c20, 0.35));

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
  $('status').innerHTML =
    `<span>${pct === 0 ? 'Ensamblado' : pct === 100 ? 'Totalmente explosionado' : 'Explosión ' + pct + ' %'}</span>` +
    `<span>Etapas activas: ${active.length ? active.join(', ') : 'ninguna'}</span>` +
    `<span>Seleccionado: ${sel}</span>` +
    `<span>${state.meshes} mallas · ${(state.tris / 1000).toFixed(0)} k triángulos</span>`;
  $('explode-out').textContent = `${pct} %`;
  $('explode').style.setProperty('--p', `${state.explode * 100}%`);
  document.querySelectorAll('.stage').forEach((el) => {
    const s = el.dataset.stage;
    el.classList.toggle('on', state.explode > STAGE_WINDOWS[s][0] && state.stageMask[s]);
    el.classList.toggle('masked', !state.stageMask[s]);
  });
}

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

function highlight(obj, on) {
  forEachMesh(obj, (m) => {
    if (on) {
      if (!m.userData.__orig) {
        m.userData.__orig = m.material;
        const h = m.material.clone();
        h.emissive = HL.clone();
        h.emissiveIntensity = 0.35;
        m.material = h;
      }
    } else if (m.userData.__orig) {
      m.material.dispose();
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
    $('info-fid').className = 'badge ' + f.cls;
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
  document.querySelectorAll('.views .chip').forEach((b) => b.classList.toggle('active', b.dataset.view === view));
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
function buildUI(manifest) {
  // Etapas
  const st = $('stages');
  st.innerHTML = '';
  for (const [k, label] of Object.entries(STAGES)) {
    const d = document.createElement('div');
    d.className = 'stage';
    d.dataset.stage = k;
    d.title = 'Pulsa para incluir o excluir esta etapa de la explosión';
    d.textContent = `${k}. ${label}`;
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
  for (const sys of systems) {
    const chip = document.createElement('button');
    chip.className = 'sys';
    chip.innerHTML = `<span class="dot"></span>${SYSTEM_LABELS[sys] || sys}`;
    chip.addEventListener('click', () => toggleSystem(sys, chip));
    chip.dataset.sys = sys;
    sysBox.appendChild(chip);

    const det = document.createElement('details');
    const items = bySystem.get(sys).sort((a, b) => (a.userData.label_es || a.name).localeCompare(b.userData.label_es || b.name, 'es'));
    det.innerHTML = `<summary><span>${SYSTEM_LABELS[sys] || sys}</span><span class="n">${items.length}</span></summary>`;
    for (const obj of items) {
      const it = document.createElement('div');
      it.className = 'item';
      it.dataset.name = obj.name;
      it.dataset.search = `${obj.name} ${obj.userData.label_es || ''}`.toLowerCase();
      const f = FIDELITY[obj.userData.fidelity];
      it.innerHTML = `<span class="label" title="${obj.name}">${obj.userData.label_es || obj.name}</span>` +
        (f ? `<span class="fid ${f.cls}" title="${f.label}">${obj.userData.fidelity}</span>` : '') +
        `<button class="eye" title="Mostrar u ocultar">◉</button>`;
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
  document.querySelectorAll('.sys').forEach((c) => c.classList.remove('off'));
  syncTreeVisibility();
}

function isolate(obj) {
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
async function load() {
  const draco = new DRACOLoader().setDecoderPath(DRACO_URL);
  const loader = new GLTFLoader().setDRACOLoader(draco);
  let manifest = null;
  try {
    manifest = await fetch(MANIFEST_URL).then((r) => (r.ok ? r.json() : null));
  } catch { manifest = null; }
  const gltf = await loader.loadAsync(MODEL_URL, (ev) => {
    if (ev.lengthComputable) {
      const p = Math.round((ev.loaded / ev.total) * 100);
      $('bar-fill').style.width = `${p}%`;
      $('loader-text').textContent = `${p} % · ${(ev.loaded / 1e6).toFixed(2)} MB`;
    }
  });
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
  window.__ct = { state, applyExplode, select, isolate, showAll, camera, controls, THREE };
  buildUI(manifest);
  flyTo('front34', 1);
  applyExplode();
  $('loader').classList.add('done');
  setTimeout(() => $('loader').remove(), 500);
}

// ---------------------------------------------------------------------------
// Controles
// ---------------------------------------------------------------------------
$('explode').addEventListener('input', (ev) => {
  state.playing = false; $('btn-play').textContent = '▶ Animar';
  state.explode = Number(ev.target.value) / 100;
  applyExplode();
});
$('amp').addEventListener('input', (ev) => { state.amp = Number(ev.target.value); applyExplode(); });
$('btn-assemble').addEventListener('click', () => {
  state.playing = false; $('btn-play').textContent = '▶ Animar';
  animateExplodeTo(0);
});
let playDir = 1;
$('btn-play').addEventListener('click', () => {
  state.playing = !state.playing;
  $('btn-play').textContent = state.playing ? '❚❚ Pausa' : '▶ Animar';
  playDir = state.explode >= 1 ? -1 : 1;
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
$('btn-reset-view').addEventListener('click', () => flyTo(state.explode > 0.3 ? 'exploded' : 'front34'));
$('btn-show-all').addEventListener('click', showAll);
$('btn-panel').addEventListener('click', () => $('panel').classList.toggle('open'));
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
  if (ev.target.tagName === 'INPUT') return;
  if (ev.key === 'Escape') select(null);
  if (ev.key === 'r' || ev.key === 'R') flyTo('front34');
});

// ---------------------------------------------------------------------------
// Bucle de render
// ---------------------------------------------------------------------------
function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
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
window.addEventListener('pagehide', () => {
  renderer.setAnimationLoop(null);
  scene.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) {
      for (const k of Object.keys(m)) if (m[k] && m[k].isTexture) m[k].dispose();
      m.dispose();
    }
  });
  envTex.dispose();
  pmrem.dispose();
  renderer.dispose();
});

load().catch((err) => {
  console.error(err);
  $('loader').classList.add('error');
  $('loader').querySelector('.loader-title').textContent = 'No se pudo cargar el modelo';
  $('loader-text').textContent = String(err && err.message ? err.message : err);
});
