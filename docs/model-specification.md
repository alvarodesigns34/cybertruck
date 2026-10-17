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
| `THM_` | Gestión térmica (Supermanifold, compresor de A/C, mangueras) |
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
  0 → 0,33 → 1 → 0,5 → 0 → 1 → 0, la desviación máxima de las matrices de mundo es **0** en los 948 objetos (561 en la versión 2).

## 5. Materiales

Biblioteca en `ct_materials.py` (61 materiales exportados). Desde la versión 2 los detalles de superficie
proceden de **texturas físicas generadas** por `ct_textures.py` (ruido filtrado en frecuencia, periódico,
guardado en WebP en `blender/textures/`), conectadas con nodos que el exportador glTF reconoce, de modo que
Blender y el visor web muestran el mismo material:

| Textura | Metros por repetición | Uso principal |
|---|---|---|
| `steel` (1024 px) | 0,40 | Acero inoxidable satinado (rayas longitudinales, bandas de laminado, microrrayas) |
| `rubber`, `sidewall` | 0,08 / 0,06 | Banda de rodadura, flancos, casquillos, mangueras, burletes |
| `plastic` | 0,05 | Granulado de aletas, faldones, fascias y plásticos interiores |
| `leather` (1024 px) | 0,08 | Piel sintética Tactical Grey (grano abombado) |
| `fabric`, `carpet` | 0,012 / 0,04 | Guarnecido de techo, cinturones, cinta de mazos, rejillas, moqueta |
| `cast`, `rotor`, `composite` | 0,20 / 0,12 / 0,10 | Fundición de aluminio, discos de freno, cubeta de la caja |

| Material | Uso | Notas |
|---|---|---|
| `CT_Stainless_Steel` (+ `_B`, `_C`) | Exoesqueleto | Metálico, anisotropía 0,55 con tangente UV (KHR_materials_anisotropy), tres variantes por panel (tono y desfase del satinado) |
| `CT_Glass_*`, `CT_Lens_*`, `CT_Mirror_Glass` | Cristales y ópticas | Transmisión con tintes diferenciados |
| `CT_LED_*`, `CT_Screen` | Iluminación y pantallas | Emisivos |
| `CT_Tire_*`, `CT_Wheel_*`, `CT_Brake_*` | Ruedas y frenos | Inscripciones del flanco con rugosidad propia; pastillas con material de fricción |
| `CT_Aluminium_Cast/Forged/Machined`, `CT_Steel_*`, `CT_Busbar_Aluminium`, `CT_Copper` | Mecánica | Fundido, forjado, mecanizado, acero negro, zincado |
| `CT_Battery_*`, `CT_Cell_4680`, `CT_Mica_Sheet`, `CT_HV_Orange` | Batería y alta tensión | Espuma estructural verde, mica |
| `CT_Harness_Tape`, `CT_Connector_*`, `CT_Radiator_Core` | Electricidad y refrigeración | |
| `CT_Upholstery_*`, `CT_Stitching`, `CT_Interior_*`, `CT_Headliner`, `CT_Carpet`, `CT_Seatbelt`, `CT_Speaker_Grille` | Interior | Decoración «Tactical Grey» con costuras |
| `CT_Rubber_Seal_EPDM` | Juntas | Burletes primario y secundario, juntas de cintura y de cristales |

Las UV se generan por proyección alineada con los ejes (1 unidad UV = 1 m; U = eje longitudinal). El canal B
del mapa de rugosidad codifica la metalicidad (convención glTF). El visor solo completa parámetros que glTF no
describe (`web/src/materials.js`) sin sustituir los mapas exportados.

## 6. Canal de producción

| Script (`blender/scripts/`) | Función |
|---|---|
| `ct_specs.py` | Ficha dimensional maestra y funciones de perfil/sección |
| `ct_lib.py` | Utilidades de malla, colecciones, modificadores y metadatos |
| `ct_parts.py` | Primitivas: envolventes convexas, cajas redondeadas, barridos de perfil, mangueras, tornillería, texto en relieve |
| `ct_textures.py` · `ct_materials.py` | Texturas generadas y biblioteca de materiales |
| `build_body.py` | Carrocería, puertas, cristales superiores, aletas, caja, portón, tonneau, paragolpes |
| `build_wheels.py` | Neumático con dibujo de 5 hileras e inscripciones, llanta, tapacubos Core, válvula/TPMS, buje, discos, pinzas y pastillas |
| `build_lights.py` · `build_details.py` | Barras de luz, pilotos, cámaras, interruptores, enganche |
| `build_exterior.py` | Faros, ópticas, retrovisores, limpiaparabrisas y lavaparabrisas, herrajes y juntas de puertas, frunk, portón, mecanismo del tonneau, toma NACS, faldillas, difusor, soporte frontal, juntas de cristales, equipamiento de la caja |
| `build_interior.py` · `build_interior_detail.py` | Habitáculo base y detalle (volante, consola, salpicadero, guarnecidos, paneles de puerta, asientos con costuras proyectadas, cinturones, alfombrillas, climatización, ordenador, airbags) |
| `build_mechanics.py` | Suspensión, dirección por cable, unidades motrices, semiejes, batería, bahía auxiliar, subchasis, gestión térmica, frenos hidráulicos, aire comprimido, baja tensión y bajos |
| `build_structure.py` | Carrocería en blanco: piezas fundidas, umbrales, refuerzos, anillos de puerta, «mast», torres, vigas de impacto, Megabeam, remaches |
| `build_chassis.py` | Orquestación de la mecánica, frunk y caja de carga |
| `ct_v3.py` | Ayudas declarativas de la versión 3: cada pieza es una lista de formas elementales (cajas, cilindros, envolventes, barridos, tornillería, rótulas, fuelles) del lado derecho; `mirror=True` genera la pareja izquierda reflejando las coordenadas de entrada (no la malla) |
| `build_v3.py` | Orquesta los módulos de la versión 3 (`build_all.run(parts=(…, "v3", …))`, antes de la vista explosionada) |
| `build_v3_estructura.py` · `build_v3_exterior.py` · `build_v3_chasis.py` · `build_v3_motriz.py` · `build_v3_interior.py` · `build_v3_electronica.py` · `build_v3_complemento.py` | Piezas añadidas a partir de `docs/ficha-tecnica-piezas.md` (identificadores EXT-, EST-, CHS-, TRN-, INT-, ELE-): estructura, exterior y caja, chasis y circuito de aire, tren motriz, térmica y alta tensión, interior, electrónica de 48 V y piezas menores |
| `build_scene.py` | Estudio, iluminaciones (`studio`, `exterior`, `sunset`, `overcast`) y cámaras |
| `build_explode.py` | Controladores de la vista explosionada y verificación |
| `validate.py` | Cotas y comparación de siluetas por trazado de rayos |
| `export_web.py` | Exportación GLB (Draco + WebP) y manifiesto de componentes |
| `preview.py` | Renders de control y planos de documentación (`render_shot`) |
| `build_all.py` | Orquestador (solo regenera la colección CYBERTRUCK) |

### Calidad de malla

- Las mallas cerradas se orientan hacia fuera de forma automática (`ct_lib.orient_closed_components`); las
  láminas abiertas se orientan con `MeshBuilder.face(..., want=dirección)`. No se usa `recalc_normals`.
- Cada pieza de la versión 3 declara sus formas en coordenadas de mundo del lado derecho y, si es simétrica, se
  refleja con `mirror=True` (`ct_v3.part`); el nombre lleva el sufijo `_R`/`_L`.
- Comprobación de volumen con signo: ninguna malla cerrada de las 909 tiene volumen negativo.

### Cámaras incluidas (colección STUDIO)

`CAM_3Q_Front`, `CAM_3Q_Rear`, `CAM_Side_Profile` (teleobjetivo 135 mm para minimizar la distorsión),
`CAM_Front`, `CAM_Rear` (85 mm), `CAM_Top` (ortográfica), `CAM_Interior`, `CAM_Wheel_Detail`, `CAM_Underbody`,
`CAM_Exploded`. Los 21 planos de `docs/renders/` se definen en `preview.SHOTS`.

## 7. Cifras del activo

| Métrica | v1 | v2 | v3 |
|---|---|---|---|
| Objetos en la colección del vehículo | 309 | 561 (522 mallas, 38 conjuntos, 1 raíz) | **948** (909 mallas, 38 conjuntos, 1 raíz) |
| Triángulos evaluados (con modificadores) | 174.862 | 498.396 | 653.442 |
| Materiales | 39 | 61 (10 juegos de texturas) | 61 (sin cambios) |
| `blender/Cybertruck.blend` (comprimido, texturas externas) | 1,12 MB | 4,5 MB | 6,5 MB |
| `blender/textures/` (WebP) | — | 1,6 MB | 1,6 MB |
| `web/models/cybertruck.glb` (Draco + WebP) | 1,07 MB | 5,3 MB | 7,0 MB |
| `web/models/cybertruck-manifest.json` | ~0,12 MB | ~0,24 MB | ~0,41 MB |
