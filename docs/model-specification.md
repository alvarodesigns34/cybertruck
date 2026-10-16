# Especificación del modelo

## 1. Unidades y sistema de coordenadas

- Escala 1:1, sistema métrico, 1 unidad de Blender = 1 m.
- **Blender:** +X = lado derecho del vehículo (acompañante en EE. UU.), **+Y = hacia delante**, +Z = arriba.
- **Origen:** sobre el suelo, en el plano de simetría y en el punto medio de la batalla.
  Eje delantero en Y = +1,8175 m, eje trasero en Y = −1,8175 m; centros de rueda en X = ±0,886 m, Z = 0,437 m.
- **Altura de suspensión de referencia:** «Medium» del manual (altura total 1.793,8 mm, altura libre 257 mm).
- **glTF / Three.js:** +Y arriba y −Z hacia delante. Conversión: `(x, y, z)_Blender → (x, z, −y)_glTF`.

## 2. Organización de la escena

```
Scene Collection
├── CYBERTRUCK                       (todo el vehículo; único contenido exportado)
│   ├── CYBERTRUCK_ROOT              (vacío raíz; propiedad «explode» 0–1)
│   ├── EXTERIOR_PANELS · DOORS_AND_HATCHES · GLASS_AND_MIRRORS · LIGHTING
│   ├── BODY_STRUCTURE · CARGO_BED · BODY_FASTENERS · UNDERBODY
│   ├── FRONT_WHEELS_AND_BRAKES · REAR_WHEELS_AND_BRAKES
│   ├── FRONT_SUSPENSION · REAR_SUSPENSION · STEERING
│   ├── BATTERY_ASSEMBLY · DRIVE_UNITS
│   └── INTERIOR_DASHBOARD · INTERIOR_CONTROLS · INTERIOR_SEATS · INTERIOR_DOORS · INTERIOR_TRIM
├── STUDIO                           (ciclorama, luces y cámaras de render; no se exporta)
├── REFERENCE_AND_HELPERS            (cámara de control CAM_PREVIEW)
└── ESCENA_ORIGINAL                  (objetos que existían al empezar; conservados y excluidos)
```

Solo se crean colecciones con contenido real. El inventario completo de objetos está en
[`component-inventory.md`](component-inventory.md).

### Convención de nombres

| Prefijo | Significado |
|---|---|
| `EXT_` | Panel o accesorio exterior |
| `GLS_` | Cristal o espejo |
| `LGT_` | Componente de iluminación |
| `DOOR_`, `WHEEL_`, `BRAKE_`, `SUSP_`, `SEAT_`, `MIRROR_`, `*_ASSEMBLY` | Conjuntos (vacíos con pivote significativo) |
| `WHL_`, `BRK_` | Rueda (neumático, llanta, tapacubos, tuercas) y freno (disco, pinza, protector) |
| `SUS_`, `STR_` | Suspensión y dirección |
| `DU_`, `BAT_`, `HV_`, `LV_` | Unidades motrices, batería, alta y baja tensión |
| `CHS_`, `BODY_`, `CARGO_` | Chasis/bajos, estructura de carrocería, caja de carga |
| `INT_` | Interior |
| `CAM_`, `SW_` | Cámaras del vehículo e interruptores exteriores |
| Sufijos `FL/FR/RL/RR`, `L/R`, `F/R` | Esquina, lado y eje |

### Pivotes

- Puertas: vacío `DOOR_xx` en el eje vertical de bisagras junto al borde delantero.
- Tapa del frunk: origen en la bisagra trasera (base del parabrisas). Portón: origen en las bisagras inferiores.
- Ruedas: vacío `WHEEL_xx` en el centro de rueda (eje de giro = X local). Neumáticos, llantas y tuercas comparten
  malla entre las cuatro ruedas (instancias); los tapacubos izquierdos usan una malla reflejada.
- Asientos, salpicadero, consola, retrovisores, suspensión y unidades motrices: vacíos de conjunto con
  rotación nula (requisito del sistema de explosión).

## 3. Metadatos por componente

Cada objeto relevante lleva propiedades personalizadas que viajan al glTF como `extras`:

| Propiedad | Descripción |
|---|---|
| `system` | Colección de sistema a la que pertenece |
| `label_es` | Descripción en español |
| `fidelity` | `V` (verificado), `R` (reconstruido) o `A` (aproximado) |
| `note_es` | Nota de fidelidad (opcional) |
| `explode_dir` | Dirección de separación (vector unitario, espacio del padre = mundo) |
| `explode_dist` | Distancia de separación en metros |
| `explode_stage` | Etapa lógica de desmontaje (1–6) |
| `explode_group` | Agrupación descriptiva |
| `pivot_es` | Descripción del pivote (en elementos móviles) |

## 4. Sistema de vista explosionada

### Etapas

| Etapa | Contenido | Ventana del parámetro |
|---|---|---|
| 1 | Paneles exteriores y elementos de apertura | 0,00 – 0,40 |
| 2 | Conjuntos interiores | 0,12 – 0,52 |
| 3 | Estructura de carrocería y bajos | 0,24 – 0,64 |
| 4 | Suspensión, ruedas y frenos | 0,36 – 0,76 |
| 5 | Batería y tren motriz | 0,48 – 0,88 |
| 6 | Componentes pequeños y herrajes | 0,60 – 1,00 |

### Formulación

```
desplazamiento = explode_dir · explode_dist · smoothstep(t0, t1, e)
```

- En **Blender**, `e` es la propiedad `explode` de `CYBERTRUCK_ROOT`. Cada objeto tiene tres controladores
  (drivers) de expresión simple sobre `delta_location`, por lo que **`location` nunca se modifica** y no hace
  falta habilitar la ejecución automática de scripts. Para usarlo: seleccionar `CYBERTRUCK_ROOT` y cambiar
  la propiedad «explode» (0 = ensamblado, 1 = explosionado) en el panel de propiedades del objeto.
- En el **visor web**, la misma fórmula se aplica a `position = base + dir · dist · amplitud · smoothstep`, con
  la dirección convertida a coordenadas glTF y un factor de amplitud ajustable (por defecto 1,5).
- Los conjuntos padre no tienen rotación, de modo que los desplazamientos jerárquicos se suman de forma
  intencionada (p. ej., la rueda sale y después el neumático se separa de la llanta) sin multiplicarse ni anularse.
- Es una función pura del parámetro: no hay estado acumulado. Verificación automática
  (`build_explode.verify_roundtrip` y prueba equivalente en el navegador): tras recorrer
  0 → 0,33 → 1 → 0,5 → 0 → 1 → 0, la desviación máxima de las matrices de mundo es **0** en los 309 objetos.

## 5. Materiales

| Material | Uso | Notas |
|---|---|---|
| `CT_Stainless_Steel` | Exoesqueleto de acero inoxidable | Metálico, rugosidad ~0,28 con microrrayado direccional longitudinal (tangente por UV, anisotropía 0,55) y variación lenta de rugosidad |
| `CT_Plastic_Textured` | Aletas, faldones, paragolpes | Granulado fino por relieve procedural |
| `CT_Glass_Windshield` / `Side` / `Roof` / `Frit` | Cristales | Transmisión con tintes diferenciados (parabrisas claro, laterales medios, techo oscuro) y serigrafía negra |
| `CT_Lens_*`, `CT_LED_*`, `CT_Reflector_Chrome` | Ópticas | Lentes transparentes, LED emisivos de intensidad moderada |
| `CT_Tire_Rubber` / `Sidewall` | Neumático | Banda y flanco con rugosidades distintas |
| `CT_Wheel_Cover`, `CT_Wheel_Alloy`, `CT_Brake_*` | Rueda y freno | |
| `CT_Aluminium_Cast`, `CT_Steel_Black`, `CT_Battery_Enclosure`, `CT_HV_Orange`, `CT_Cell_4680`, `CT_Copper` | Mecánica y alta tensión | |
| `CT_Upholstery_*`, `CT_Interior_*`, `CT_Headliner`, `CT_Carpet`, `CT_Screen`, `CT_Composite_Bed` | Interior y caja | Decoración «Tactical Grey» |

Las UV se generan por proyección alineada con los ejes (1 unidad UV = 1 m; U = eje longitudinal en las caras
laterales y superiores), con densidad de texel uniforme. El visor web reinterpreta los nodos procedurales con
`MeshPhysicalMaterial` (anisotropía, transmisión, brillo de tejido) en `web/src/materials.js`.

## 6. Canal de producción

| Script (`blender/scripts/`) | Función |
|---|---|
| `ct_specs.py` | Ficha dimensional maestra y funciones de perfil/sección |
| `ct_lib.py` | Utilidades de malla, colecciones, modificadores y metadatos |
| `ct_materials.py` | Biblioteca de materiales |
| `build_body.py` | Carrocería, puertas, cristales superiores, aletas, caja, portón, tonneau, paragolpes |
| `build_wheels.py` | Neumáticos, llantas, tapacubos, tuercas, discos, pinzas |
| `build_lights.py` · `build_details.py` | Iluminación; retrovisores, limpiaparabrisas, cámaras, toma de carga, enganche |
| `build_interior.py` | Habitáculo |
| `build_chassis.py` | Batería, unidades motrices, suspensión, dirección, estructura y bajos |
| `build_scene.py` | Estudio, HDRI, luces y cámaras |
| `build_explode.py` | Controladores de la vista explosionada y verificación |
| `validate.py` | Cotas y comparación de siluetas por trazado de rayos |
| `export_web.py` | Exportación GLB (Draco) y manifiesto de componentes |
| `preview.py` | Renders de control |
| `build_all.py` | Orquestador (solo regenera la colección CYBERTRUCK) |

### Cámaras incluidas (colección STUDIO)

`CAM_3Q_Front`, `CAM_3Q_Rear`, `CAM_Side_Profile` (teleobjetivo 135 mm para minimizar la distorsión),
`CAM_Front`, `CAM_Rear` (85 mm), `CAM_Top` (ortográfica), `CAM_Interior`, `CAM_Wheel_Detail`, `CAM_Underbody`,
`CAM_Exploded`.

## 7. Cifras del activo

| Métrica | Valor |
|---|---|
| Objetos en la colección del vehículo | 309 (277 mallas, 31 conjuntos, 1 raíz) |
| Triángulos evaluados (con modificadores) | 174.862 |
| `blender/Cybertruck.blend` (comprimido) | 1,12 MB |
| `web/models/cybertruck.glb` (Draco) | 1,07 MB |
| `web/models/cybertruck-manifest.json` | ~0,12 MB |
