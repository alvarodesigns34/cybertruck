// Ajuste de materiales en el navegador.
// Desde la versión 2, el GLB incluye texturas físicas generadas en Blender (rugosidad/metalicidad,
// normales y color; WebP con KHR_texture_transform) y extensiones KHR (anisotropía, transmisión,
// brillo de tejido, recubrimiento). Aquí solo se completan los parámetros que glTF no describe
// (intensidad del entorno, espesor de los cristales, emisión de pantallas) sin sustituir los mapas
// exportados. Los presets se eligen por prefijo del nombre de material de Blender.
import * as THREE from 'three';

function brushedTexture() {
  // Respaldo: rayado longitudinal fino si el GLB no trae mapa de rugosidad (modelos antiguos).
  // Con un generador de semilla fija (mulberry32), no Math.random: la misma textura en cada carga (auditoría C13).
  let seed = 0x5eed1234;
  const random = () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const w = 64, h = 1024;
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const g = c.getContext('2d');
  const img = g.createImageData(w, h);
  let v = 0.5;
  for (let y = 0; y < h; y++) {
    v = 0.85 * v + 0.15 * random();
    const base = 150 + (v - 0.5) * 70 + (random() - 0.5) * 20;
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      const n = base + (random() - 0.5) * 6;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = Math.max(0, Math.min(255, n));
      img.data[i + 3] = 255;
    }
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(0.5, 4.0);
  t.colorSpace = THREE.NoColorSpace;
  t.anisotropy = 8;
  return t;
}

let BRUSHED = null;

function glass(m, color, transmission, thickness = 0.005) {
  m.color = new THREE.Color(color);
  m.metalness = 0;
  m.roughness = Math.min(m.roughness ?? 0.03, 0.05);
  m.transmission = transmission;
  m.ior = 1.52;
  m.thickness = thickness;
  m.transparent = false;
  m.envMapIntensity = 1.2;
  m.specularIntensity = 1.0;
}

function sharpenMaps(m) {
  // Filtrado anisótropo alto para las texturas repetidas vistas en ángulo rasante.
  for (const k of ['map', 'normalMap', 'roughnessMap', 'metalnessMap']) {
    if (m[k]) m[k].anisotropy = 8;
  }
}

// [prefijo, función]: se aplica el primero que coincida
const PRESETS = [
  ['CT_Stainless_Steel', (m) => {
    if (!m.roughnessMap) {
      BRUSHED ??= brushedTexture();
      m.roughnessMap = BRUSHED;
      m.roughness = 0.34;
    }
    m.metalness = 1.0;
    if (!m.anisotropy) m.anisotropy = 0.55;
    m.envMapIntensity = 1.15;
  }],
  ['CT_Glass_Windshield', (m) => glass(m, 0xdfe7e5, 0.92, 0.0055)],
  ['CT_Glass_Side', (m) => glass(m, 0x8a9294, 0.80, 0.004)],
  ['CT_Glass_Roof', (m) => glass(m, 0x23272a, 0.55, 0.006)],
  ['CT_Lens_Clear', (m) => glass(m, 0xffffff, 0.9, 0.003)],
  ['CT_Lens_Red', (m) => { glass(m, 0xc8100c, 0.6, 0.003); m.attenuationColor = new THREE.Color(0xff1a10); }],
  ['CT_Lens_Smoked', (m) => glass(m, 0x1c1c1e, 0.5, 0.003)],
  ['CT_Mirror_Glass', (m) => { m.metalness = 1; m.roughness = 0.03; m.color.setRGB(0.92, 0.92, 0.92); }],
  ['CT_LED_White', (m) => { m.emissive = new THREE.Color(0xfff6ea); m.emissiveIntensity = 4.0; }],
  ['CT_LED_Red', (m) => { m.emissive = new THREE.Color(0xff1408); m.emissiveIntensity = 3.0; }],
  ['CT_LED_Amber', (m) => { m.emissive = new THREE.Color(0xff7a10); m.emissiveIntensity = 2.0; }],
  ['CT_Screen', (m) => {
    m.color.setRGB(0.01, 0.012, 0.016); m.roughness = 0.08; m.metalness = 0;
    m.emissive = new THREE.Color(0x1d2836); m.emissiveIntensity = 0.9; m.clearcoat = 1;
  }],
  ['CT_Upholstery', (m) => { m.sheenRoughness = 0.6; m.envMapIntensity = 0.8; }],
  ['CT_Headliner', (m) => { m.sheenRoughness = 0.8; m.envMapIntensity = 0.7; }],
  ['CT_Carpet', (m) => { m.sheenRoughness = 0.9; m.envMapIntensity = 0.6; }],
  ['CT_Tire', (m) => { m.envMapIntensity = 0.7; }],
  ['CT_Aluminium', (m) => { m.envMapIntensity = 1.05; }],
];

export function enhanceMaterial(mat) {
  if (!mat || mat.userData.__enhanced) return mat;
  let m = mat;
  if (!m.isMeshPhysicalMaterial) {
    const p = new THREE.MeshPhysicalMaterial();
    THREE.MeshStandardMaterial.prototype.copy.call(p, m);
    p.name = m.name;
    m.dispose();
    m = p;
  }
  const hit = PRESETS.find(([prefix]) => m.name && m.name.startsWith(prefix));
  if (hit) hit[1](m);
  sharpenMaps(m);
  m.userData.__enhanced = true;
  m.needsUpdate = true;
  return m;
}
