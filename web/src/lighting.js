// Iluminación y reflejos del visor.
//
// El acero inoxidable satinado del Cybertruck se lee sobre todo por lo que refleja: con el entorno genérico
// (RoomEnvironment) los paneles se veían planos. Aquí se construye un entorno HDR propio por procedimiento
// (sin imágenes externas) con dos ambientes:
//   * «Estudio»: sala oscura con cajas de luz alargadas en el techo y en los laterales, que dibujan reflejos
//     largos y nítidos sobre las facetas, más una caja principal y un contraluz.
//   * «Exterior»: cúpula de cielo con degradado, sol y suelo cálido, para ver el vehículo a la luz del día.
// El suelo recibe además un reflejo plano real (Reflector de three.js) que se desvanece hacia el borde.
import * as THREE from 'three';
import { Reflector } from 'three/addons/objects/Reflector.js';

function emissive(color, k) {
  const m = new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide });
  m.color.multiplyScalar(k);            // valores > 1: el PMREM trabaja en coma flotante (HDR)
  return m;
}

function panel(scene, w, h, pos, look, mat) {
  const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  p.position.set(...pos);
  p.lookAt(new THREE.Vector3(...look));
  scene.add(p);
  return p;
}

function studioScene() {
  const s = new THREE.Scene();
  const room = new THREE.Mesh(new THREE.BoxGeometry(36, 16, 36),
    new THREE.MeshBasicMaterial({ color: 0x0b0c0e, side: THREE.BackSide }));
  room.position.y = 7;
  s.add(room);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(36, 36), new THREE.MeshBasicMaterial({ color: 0x15171a }));
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.95;
  s.add(floor);
  // tres tiras de techo a lo largo del vehículo (eje Z en glTF) y una cruzada
  for (const x of [-3.2, 0, 3.2]) panel(s, 1.1, 18, [x, 13.5, 0], [x, 0, 0], emissive(0xffffff, 5.5));
  panel(s, 14, 0.9, [0, 13.4, -6], [0, 0, -6], emissive(0xfff6ec, 3.5));
  // tiras verticales laterales: reflejos largos en las caras inclinadas
  for (const z of [-5, 1, 7]) {
    panel(s, 0.8, 7, [-16, 4.5, z], [0, 4.5, z], emissive(0xf3f6ff, 3.2));
    panel(s, 0.8, 7, [16, 4.5, z], [0, 4.5, z], emissive(0xfff4ea, 2.4));
  }
  // caja principal (tres cuartos delantera izquierda) y contraluz frío
  panel(s, 7, 4.5, [-11, 6, -12], [0, 1, 0], emissive(0xffffff, 4.0));
  panel(s, 9, 3, [8, 5, 14], [0, 1, 0], emissive(0xdde8ff, 2.2));
  // banda de horizonte tenue (separa el contorno inferior de los paneles)
  const band = new THREE.Mesh(new THREE.CylinderGeometry(17.5, 17.5, 0.6, 64, 1, true), emissive(0x9aa3ad, 0.9));
  band.position.y = 0.6;
  s.add(band);
  return s;
}

function exteriorScene() {
  const s = new THREE.Scene();
  const sky = new THREE.Mesh(new THREE.SphereGeometry(40, 48, 24), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: { zenith: { value: new THREE.Color(0x3d6fb3).multiplyScalar(1.6) },
                horizon: { value: new THREE.Color(0xdfe7ef).multiplyScalar(2.0) },
                ground: { value: new THREE.Color(0x6b6256).multiplyScalar(0.9) } },
    vertexShader: 'varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 zenith; uniform vec3 horizon; uniform vec3 ground; varying vec3 vDir;' +
      'void main(){ float h = vDir.y; vec3 c = h > 0.0 ? mix(horizon, zenith, pow(h, 0.55)) : mix(horizon, ground, pow(-h, 0.35));' +
      ' gl_FragColor = vec4(c, 1.0); }',
  }));
  s.add(sky);
  const sun = new THREE.Mesh(new THREE.SphereGeometry(1.4, 24, 12), emissive(0xfff1dc, 60));
  sun.position.set(-18, 22, -14);
  s.add(sun);
  return s;
}

export const ENVIRONMENTS = {
  studio: { label: 'Estudio', background: 0x0d0f12, fog: [0x0d0f12, 22, 60], exposure: 1.0, envIntensity: 1.0,
            key: { color: 0xffffff, intensity: 2.2, pos: [-6, 9, -5] }, hemi: 0.25 },
  exterior: { label: 'Exterior', background: 0xb9c7d6, fog: [0xb9c7d6, 30, 90], exposure: 0.72, envIntensity: 0.9,
              key: { color: 0xfff1dc, intensity: 3.2, pos: [-9, 11, -7] }, hemi: 0.45 },
};

/** Crea los mapas de entorno prefiltrados (uno por ambiente) y devuelve una función para aplicarlos. */
export function createLighting(renderer, scene, keyLight, hemiLight) {
  const pmrem = new THREE.PMREMGenerator(renderer);
  const maps = {
    studio: pmrem.fromScene(studioScene(), 0.015).texture,
    exterior: pmrem.fromScene(exteriorScene(), 0.02).texture,
  };
  pmrem.dispose();
  function apply(name) {
    const e = ENVIRONMENTS[name] || ENVIRONMENTS.studio;
    scene.environment = maps[name] || maps.studio;
    scene.environmentIntensity = e.envIntensity;
    scene.background = new THREE.Color(e.background);
    scene.fog = new THREE.Fog(...e.fog);
    renderer.toneMappingExposure = e.exposure;
    keyLight.color.set(e.key.color);
    keyLight.intensity = e.key.intensity;
    keyLight.position.set(...e.key.pos);
    hemiLight.intensity = e.hemi;
    return e;
  }
  function dispose() { for (const t of Object.values(maps)) t.dispose(); }
  return { apply, dispose, maps };
}

/** Reflejo plano del suelo, translúcido y desvanecido hacia el borde. */
export function createFloorReflector(radius = 14, quality = 0.5) {
  const dpr = Math.min(window.devicePixelRatio, 2);
  const geo = new THREE.CircleGeometry(radius, 96);
  const refl = new Reflector(geo, {
    textureWidth: Math.round(window.innerWidth * dpr * quality),
    textureHeight: Math.round(window.innerHeight * dpr * quality),
    color: 0xffffff,
    clipBias: 0.002,
    shader: {
      name: 'ReflectorDesvanecido',
      uniforms: {
        color: { value: null }, tDiffuse: { value: null }, textureMatrix: { value: null },
        strength: { value: 0.28 }, fadeRadius: { value: radius },
      },
      vertexShader: 'uniform mat4 textureMatrix; varying vec4 vUv; varying vec3 vPos;' +
        'void main(){ vUv = textureMatrix * vec4(position, 1.0); vPos = position;' +
        ' gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
      fragmentShader: /* glsl */`
        uniform vec3 color;
        uniform sampler2D tDiffuse;
        uniform float strength;
        uniform float fadeRadius;
        varying vec4 vUv;
        varying vec3 vPos;
        void main() {
          vec4 base = texture2DProj(tDiffuse, vUv);
          float r = length(vPos.xy) / fadeRadius;
          float a = strength * (1.0 - smoothstep(0.25, 1.0, r));
          gl_FragColor = vec4(base.rgb * color, a);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`,
    },
  });
  refl.material.transparent = true;
  refl.material.depthWrite = false;
  refl.rotation.x = -Math.PI / 2;
  refl.position.y = -0.0015;
  refl.renderOrder = 1;
  refl.setStrength = (k) => { refl.material.uniforms.strength.value = k; };
  refl.resize = (w, h) => {
    refl.getRenderTarget().setSize(Math.round(w * dpr * quality), Math.round(h * dpr * quality));
  };
  return refl;
}
