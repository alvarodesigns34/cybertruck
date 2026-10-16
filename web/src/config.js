// Etiquetas en español y parámetros del visor.

export const MODEL_URL = 'models/cybertruck.glb';
export const MANIFEST_URL = 'models/cybertruck-manifest.json';
export const DRACO_URL = 'https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/libs/draco/gltf/';

export const SYSTEM_LABELS = {
  EXTERIOR_PANELS: 'Paneles exteriores',
  DOORS_AND_HATCHES: 'Puertas y portones',
  GLASS_AND_MIRRORS: 'Cristales y retrovisores',
  LIGHTING: 'Iluminación',
  BODY_STRUCTURE: 'Estructura de carrocería',
  CARGO_BED: 'Caja de carga',
  FRONT_WHEELS_AND_BRAKES: 'Ruedas y frenos delanteros',
  REAR_WHEELS_AND_BRAKES: 'Ruedas y frenos traseros',
  FRONT_SUSPENSION: 'Suspensión delantera',
  REAR_SUSPENSION: 'Suspensión trasera',
  STEERING: 'Dirección',
  BATTERY_ASSEMBLY: 'Batería y alta tensión',
  DRIVE_UNITS: 'Unidades motrices',
  UNDERBODY: 'Bajos y subchasis',
  INTERIOR_DASHBOARD: 'Salpicadero',
  INTERIOR_CONTROLS: 'Mandos y pantallas',
  INTERIOR_SEATS: 'Asientos y cinturones',
  INTERIOR_DOORS: 'Paneles de puerta',
  INTERIOR_TRIM: 'Guarnecidos interiores',
  BODY_FASTENERS: 'Cámaras, sensores y herrajes',
};

export const STAGES = {
  1: 'Paneles y aperturas',
  2: 'Interior',
  3: 'Estructura y bajos',
  4: 'Suspensión y ruedas',
  5: 'Batería y tren motriz',
  6: 'Piezas pequeñas',
};

export const STAGE_WINDOWS = {
  1: [0.00, 0.40], 2: [0.12, 0.52], 3: [0.24, 0.64],
  4: [0.36, 0.76], 5: [0.48, 0.88], 6: [0.60, 1.00],
};

export const FIDELITY = {
  V: { label: 'Verificado', cls: 'fid-V' },
  R: { label: 'Reconstruido', cls: 'fid-R' },
  A: { label: 'Aproximado', cls: 'fid-A' },
};

// Cámaras predefinidas (coordenadas glTF: +Y arriba, -Z hacia delante del vehículo)
export const VIEWS = {
  front34: { pos: [-6.4, 2.1, -6.9], target: [0, 0.75, -0.1] },
  rear34: { pos: [6.2, 2.4, 7.4], target: [0, 0.8, 0.5] },
  side: { pos: [-10.5, 0.95, 0.15], target: [0, 0.85, 0.15] },
  top: { pos: [0.001, 11.5, 0.15], target: [0, 0, 0.15] },
  interior: { pos: [-0.36, 1.40, 0.52], target: [0.02, 1.05, -1.2] },
  under: { pos: [-3.4, -1.1, -4.8], target: [0, 0.35, -0.2] },
  exploded: { pos: [-9.0, 5.2, -8.6], target: [0, 0.8, 0.2] },
};
