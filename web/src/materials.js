// Ajuste de materiales para el navegador a partir de los nombres de los materiales de Blender.
// Los nodos procedurales de Blender no existen en glTF; aquí se reinterpretan con
// MeshPhysicalMaterial (anisotropía, transmisión, recubrimiento) y texturas generadas.
import * as THREE from 'three';

function brushedTexture() {
  // Rayado longitudinal fino (U = eje longitudinal del vehículo) para la rugosidad del acero.
  const w = 64, h = 1024;
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const g = c.getContext('2d');
  const img = g.createImageData(w, h);
  let v = 0.5;
  for (let y = 0; y < h; y++) {
    v = 0.85 * v + 0.15 * Math.random();
    const base = 150 + (v - 0.5) * 70 + (Math.random() - 0.5) * 20;
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      const n = base + (Math.random() - 0.5) * 6;
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

function grainTexture(scale = 1) {
  const s = 256;
  const c = document.createElement('canvas');
  c.width = c.height = s;
  const g = c.getContext('2d');
  const img = g.createImageData(s, s);
  for (let i = 0; i < s * s; i++) {
    const n = 128 + (Math.random() - 0.5) * 60;
    img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = n;
    img.data[i * 4 + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(20 * scale, 20 * scale);
  t.colorSpace = THREE.NoColorSpace;
  return t;
}

let BRUSHED = null;
let GRAIN = null;

const PRESETS = {
  CT_Stainless_Steel: (m) => {
    BRUSHED ??= brushedTexture();
    m.color.setRGB(0.60, 0.60, 0.59);
    m.metalness = 1.0;
    m.roughness = 0.34;
    m.roughnessMap = BRUSHED;
    m.anisotropy = 0.55;
    m.anisotropyRotation = 0;
    m.envMapIntensity = 1.1;
  },
  CT_Glass_Windshield: (m) => glass(m, 0xdfe7e5, 0.92),
  CT_Glass_Side: (m) => glass(m, 0x8a9294, 0.80),
  CT_Glass_Roof: (m) => glass(m, 0x23272a, 0.55),
  CT_Lens_Clear: (m) => glass(m, 0xffffff, 0.9),
  CT_Lens_Red: (m) => { glass(m, 0xc8100c, 0.6); m.attenuationColor = new THREE.Color(0xff1a10); },
  CT_Lens_Smoked: (m) => glass(m, 0x1c1c1e, 0.5),
  CT_Mirror_Glass: (m) => { m.metalness = 1; m.roughness = 0.03; m.color.setRGB(0.92, 0.92, 0.92); },
  CT_LED_White: (m) => { m.emissive = new THREE.Color(0xfff6ea); m.emissiveIntensity = 4.0; },
  CT_LED_Red: (m) => { m.emissive = new THREE.Color(0xff1408); m.emissiveIntensity = 3.0; },
  CT_LED_Amber: (m) => { m.emissive = new THREE.Color(0xff7a10); m.emissiveIntensity = 2.0; },
  CT_Screen: (m) => {
    m.color.setRGB(0.01, 0.012, 0.016); m.roughness = 0.08; m.metalness = 0;
    m.emissive = new THREE.Color(0x1d2836); m.emissiveIntensity = 0.9; m.clearcoat = 1;
  },
  CT_Plastic_Textured: (m) => { GRAIN ??= grainTexture(); m.roughness = 0.72; m.roughnessMap = GRAIN; m.color.setRGB(0.028, 0.029, 0.031); },
  CT_Tire_Rubber: (m) => { m.roughness = 0.9; m.color.setRGB(0.03, 0.03, 0.031); },
  CT_Tire_Sidewall: (m) => { m.roughness = 0.82; m.color.setRGB(0.035, 0.035, 0.037); },
  CT_Upholstery_Grey: (m) => { m.roughness = 0.62; m.sheen = 0.3; m.sheenColor = new THREE.Color(0x30343a); },
  CT_Carpet: (m) => { m.roughness = 1.0; m.sheen = 0.6; m.sheenColor = new THREE.Color(0x202226); },
  CT_Headliner: (m) => { m.roughness = 0.95; m.sheen = 0.5; m.sheenColor = new THREE.Color(0x3a3d42); },
};

function glass(m, color, transmission) {
  m.color = new THREE.Color(color);
  m.metalness = 0;
  m.roughness = 0.03;
  m.transmission = transmission;
  m.ior = 1.52;
  m.thickness = 0.005;
  m.transparent = false;
  m.envMapIntensity = 1.2;
  m.specularIntensity = 1.0;
}

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
  const fn = PRESETS[m.name];
  if (fn) fn(m);
  m.userData.__enhanced = true;
  m.needsUpdate = true;
  return m;
}
