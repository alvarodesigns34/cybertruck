# Traspaso del proyecto `cybertruck` a una sesión nueva

Documento de contexto completo (17-10-2026). Léelo entero junto con `CLAUDE.md` antes de tocar nada. Todo lo que
comuniques al usuario, la documentación y los comentarios de código van **en español** (lo exige `CLAUDE.md`).

> **Actualización (versión 4, 17-10-2026, rama `modelo-v4-coche-completo`).** La hoja de ruta de §3 está
> completada: 189 piezas nuevas con el interior funcional de los conjuntos y tornillería (1.137 objetos),
> texturas nuevas, 26 renders renovados, suelo de cristal / opaco / oculto, entornos HDR propios con reflejo plano
> del suelo y HUD de vidrio líquido. Ver §13 y `CLAUDE.md` (estado). Las cifras de §2 son las de la versión 3.

---

## 1. Qué es el proyecto

Reconstrucción 3D documentada, a escala 1:1, del **Tesla Cybertruck Cyberbeast** (gama de EE. UU., 2026):

- Se modela en **Blender 5.2 (5.2.2 LTS)** conectado por **Blender MCP**; los scripts de `blender/scripts/` regeneran
  la escena entera.
- Incluye una **vista explosionada reversible** (función pura del parámetro `explode`, desviación 0 tras ciclos).
- Hay un **visor web** en Three.js (`web/`), publicado en https://alvarodesigns34.github.io/cybertruck/ mediante
  GitHub Actions (`.github/workflows/pages.yml`, se despliega en cada push a `main` que toque `web/`).
- Repositorio local: `C:\Users\Álvaro\CYBERTRUCK` → GitHub `alvarodesigns34/cybertruck` (rama `main`).
- Propietario: Álvaro (alvarolago2000@gmail.com). Trabaja en español.

Principio rector: **no inventar datos**. Existencia, denominación, cantidad y fijaciones de cada pieza proceden de los
manuales de Tesla; la forma exacta casi siempre es una reconstrucción (no hay planos CAD públicos) y se etiqueta
«Reconstruido» o «Aproximado».

## 2. Estado actual (17-10-2026)

| Dato | Valor |
|---|---|
| Versión | **3** (publicada en `main`, commit de fusión `fa38cc4`; documentación posterior hasta `cb5854b`) |
| Objetos | 948 (909 mallas, 38 conjuntos, 1 raíz); la versión 2 tenía 561, la 1 tenía 309 |
| Triángulos evaluados | 653.442 |
| GLB (`web/models/cybertruck.glb`, Draco + WebP) | 6,97 MB (v2: 5,3 MB) |
| `blender/Cybertruck.blend` | 6,5 MB (comprimido, texturas externas en `blender/textures/`) |
| Fidelidad (objetos) | Reconstruido 876 · Aproximado 51 · Verificado 20 |
| Validación | cotas oficiales intactas (ver §8); explosión con desviación 0 en los 948 objetos |
| Visor | Carga bien en local y en Pages (manifiesto con 947 componentes; ~1.494 mallas de Three.js) |

Historial de commits relevante: `3bf7d14` (inicial) → `2eb91d9` → `5e6569e` → `e4945de` (CLAUDE.md) → `23db7de`
(v2) → `eb39f5e` (ficha técnica + investigación) → `2551519` (v3 en la rama `modelo-v3-piezas-faltantes`) →
`fa38cc4` (fusión en `main`) → `4fa1aad` (hallazgo del suelo) → `cb5854b` (hoja de ruta). La rama
`modelo-v3-piezas-faltantes` también está en GitHub y ya está fusionada (se puede borrar).

## 3. Hoja de ruta acordada (aún sin empezar)

El usuario dijo que seguirá trabajando y que avisará «cuando quiera». Está documentado en `CLAUDE.md` y `README.md`.

1. **Más piezas**: «bastantes más piezas, todas las posibles de manera realista». Candidatas ya identificadas:
   tornillería individual por pieza (hoy va agrupada en un objeto por familia), opciones fuera de serie
   (Terrestrial Armor, barra de luz off-road), espumas y tapicerías de los asientos, mazos y conectores, soportes,
   clips y todo lo pendiente de `docs/ficha-tecnica-piezas.md`. Propuesta que hice y el usuario aceptó como siguiente
   paso: una «versión 3.1» con lo que sí se puede hacer con rigor.
2. **Hiperrealismo**: «mejorar el modelo en general, todo profundamente centrado en hiperrealismo». Ejes posibles:
   formas exactas de faros, retrovisores, paragolpes y fundiciones; molde real del neumático Scorpion ATR; materiales
   y texturas físicas; biseles, holguras y desgaste creíbles; iluminación y renders. Siempre dentro de las cotas
   oficiales. Cuello de botella: **faltan fuentes de geometría** (escaneos, fotografías ortogonales, figuras del
   manual de reparación). Sin ellas, lo que se añada es cada vez más inventado: dilo al usuario con franqueza.
3. **HUD del visor**: «mejorar bastante más el HUD, más estética tipo Apple, con liquid glass, etc.». Está el skill
   `criterio-de-diseno` disponible (valores de espaciado, tipografía, color y movimiento, anti «aspecto IA»). Textos
   de interfaz en español.
4. **Hallazgo del visor (documentado, sin implementar)**: al explosionar, muchas piezas bajas bajan por debajo del
   suelo (círculo opaco de radio 26 m en `y = −0,002` y rejilla en `y = 0`, `web/src/main.js` líneas ~59–83;
   `controls.maxPolarAngle = π·0,98`) y solo se ven moviendo la cámara a través del suelo. **Propuesta del usuario:
   suelo de cristal semitransparente + opción «ocultar suelo»**. Alternativas que le expuse (por si cambia de idea):
   que el suelo acompañe al despiece, subir el vehículo al explosionar, preset de cámara «Bajos», modo rayos X de la
   carrocería, o cambiar direcciones de explosión (esto último requiere regenerar en Blender). Solo toca el visor.

El usuario fue explícito en una ocasión: *«todavía no cambies nada a nivel de código»* cuando solo quería que se
documentara o se le explicara algo. Respeta esa distinción: documentar ≠ implementar.

## 4. Preferencias y forma de trabajar del usuario

- Español siempre, también en mensajes de progreso y comentarios de código.
- Le gusta que se suba todo a GitHub; sin embargo, **no subas ni publiques sin que lo pida** (en esta sesión pidió
  cada push de forma explícita). Publicar el visor es un push a `main` que modifique `web/`.
- Respuestas directas, con recomendación clara cuando hay varias opciones. Pregunta si realmente es decisión suya.
- Le importa la verdad: pregunta si «faltan muchas piezas»; la respuesta honesta fue que sí (ver §9).
- Al iniciar una edición en un repositorio git, el harness pide proponer rama (`propose_branch`); en esta sesión el
  usuario no eligió y se trabajó en `modelo-v3-piezas-faltantes`. Fusionó a `main` con `--no-ff`.
- Mensajes de commit en español, terminando con la línea de coautoría que indique el sistema.

## 5. Entorno técnico y trampas conocidas

- **No hay Python fuera de Blender.** Node sí está disponible (`tools/*.mjs`). Todo el trabajo de modelado se hace
  ejecutando Python dentro de Blender mediante el MCP (`execute_blender_code`).
- **No hay CLI `gh`.** El token de GitHub está en el gestor de credenciales de Git (`git push` funciona).
- **El MCP de Blender corta las llamadas que duran más de ~100 s** («Request timed out»). Pero **la ejecución en
  Blender continúa** aunque el cliente se rinda: comprueba el resultado mirando los archivos generados o lanzando
  otra llamada trivial. Renderiza en tandas de ≤4–5 planos (~9–15 s cada uno con Cycles GPU a 128 muestras;
  los planos con más geometría tardan más). La regeneración completa del modelo tarda ~10 s; el GLB, ~4 s.
- `execute_blender_code`: el valor devuelto debe asignarse a una variable `result` que sea un **dict** (un str falla).
  Salidas enormes (el exportador glTF imprime mucho) provocan «result exceeds maximum allowed tokens»: redirige
  `stdout` con `contextlib.redirect_stdout`.
- Dentro de Blender hay que añadir `C:\Users\Álvaro\CYBERTRUCK\blender\scripts` a `sys.path`; tras editar scripts,
  `build_all.run(...)` recarga los módulos (`reload_modules`), no hace falta reiniciar Blender.
- La escena de Blender que abre el MCP puede estar vacía (3 objetos por defecto, sin archivo): regenerar con
  `build_all.run(...)` la deja completa. `blender/Cybertruck.blend` se guarda con
  `bpy.ops.wm.save_as_mainfile(filepath=..., compress=True)` y **nunca se elimina**.
- El visor se prueba con `node tools/serve.mjs web 8080` (el `.claude/launch.json` del repo define la configuración
  `visor-cybertruck`, pero la herramienta de previsualización solo lo encuentra si la sesión tiene el repo como
  directorio de trabajo; si no, arranca el servidor con Bash en segundo plano y abre `http://localhost:8080/` con
  `preview_start` + `url`). **Detén el servidor al terminar** (proceso `node … serve.mjs`).
- Los renders de comprobación rápida usaron un pequeño ayudante (`qshot.py`) que excluye colecciones y renderiza con
  Workbench; **no está en el repo** (vivía en la carpeta temporal). Se recrea en 20 líneas con `preview.render` y
  `preview.set_excluded`. Los planos de documentación usan `preview.render_shot(nombre, carpeta, samples=128)`.
- En Windows, la herramienta Write no escribió en la carpeta temporal del sistema aunque devolviera éxito; para
  archivos auxiliares usa Bash (`cat > … <<'EOF'`).
- Para parchear muchos textos en los scripts se usó `node` con reemplazos exactos (cuidado con las comillas).

## 6. Estructura del repositorio

```
CLAUDE.md                       Normas permanentes (idioma, convenciones, flujo, estado y pendientes)
traspaso.md                     Este documento
README.md                       Qué contiene, estructura, regeneración, visor, despliegue, limitaciones, próximos pasos
blender/Cybertruck.blend        Escena maestra
blender/scripts/                Scripts (ver §7)
blender/reference_data/         official_side_profile.json (perfiles medidos; datos derivados)
blender/textures/               Texturas físicas generadas (WebP)
web/                            Visor (index.html, src/main.js, src/config.js, src/materials.js, src/style.css, models/)
docs/                           research-and-fidelity.md, model-specification.md, component-inventory.md (generado),
                                ficha-tecnica-piezas.md, validation-results.json, renders/ (21 JPG)
reports/, research_notes/       Informe y notas de la investigación (ver §10)
tools/                          serve.mjs (servidor estático), gen_inventory.mjs (genera docs/component-inventory.md)
.github/workflows/pages.yml     Despliegue del visor
.claude/launch.json             Configuración de previsualización del visor
```

Documentación a leer, por este orden: `CLAUDE.md` → este archivo → `README.md` → `docs/model-specification.md`
(coordenadas, jerarquía, explosión, materiales, canal) → `docs/research-and-fidelity.md` (fuentes, método de
medición, V/R/A, validación, §8 investigación v2, §9 versión 3) → `docs/ficha-tecnica-piezas.md` (ficha de ~1.400
líneas: cotas consolidadas, tablas por sistema, conflictos de fuentes, backlog) → `docs/component-inventory.md`.

## 7. Scripts de `blender/scripts/`

| Módulo | Función |
|---|---|
| `ct_specs.py` | Ficha dimensional maestra y funciones de perfil/sección (`z_top`, `z_belt`, `hw_body`, `hw_glass`, `hw_side`, `hw_roof_edge`, `front_plan_y`, `interp`…) |
| `ct_lib.py` | `MeshBuilder`, `mesh_object`, colecciones, `explode(...)`, `lathe`, `box`, `prism`, `tube`, **`orient_closed_components`** |
| `ct_parts.py` | Primitivas: `hull`, `rbox`, `beam`, `cyl`, `tube_ring`, `disc`, `sweep`, `hose`, `corrugated`, tornillería (`flange_bolt`, `hex_nut`, `torx_screw`, `push_clip`, `rivet`), `ball_joint`, `boot`, `prism`, `ribbed_plate`, `text_outline`, y `make(...)` (crea el objeto, suaviza, aplica bisel y metadatos) |
| `ct_textures.py` · `ct_materials.py` | Texturas generadas y biblioteca de materiales (`build_library()` devuelve el dict `M`) |
| `build_body.py` … `build_details.py`, `build_lights.py`, `build_wheels.py`, `build_interior*.py`, `build_mechanics.py`, `build_structure.py`, `build_exterior.py`, `build_chassis.py` | Constructores de la versión 1 y 2 |
| **`ct_v3.py`** | Capa declarativa de la versión 3: `part(M, nombre, sistema, materiales, formas, etiqueta, mirror=…, edir, dist, stage, fid, note…)` y constructores de formas `box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, rivet, ball, boot, ribs, prism` |
| **`build_v3.py`** | Orquesta los módulos de la v3 (se ejecuta con `parts=(…, "v3", …)`, antes de `explode`) |
| **`build_v3_estructura/exterior/chasis/motriz/interior/electronica/complemento.py`** | 387 piezas nuevas de la v3 (cada módulo expone `build(M)`) |
| `build_scene.py` | Estudio, iluminaciones (`studio`, `exterior`, `sunset`, `overcast`) y cámaras `CAM_*` |
| `build_explode.py` | Controladores de la explosión; `verify_roundtrip()`, `set_explode()`, `vehicle_objects()` |
| `validate.py` | Cotas oficiales y siluetas por trazado de rayos (BVH) |
| `export_web.py` | GLB (Draco + WebP) y manifiesto de componentes |
| `preview.py` | Renders de control (`render`, `render_shot`, `SHOTS`, `set_excluded`) |
| `build_all.py` | Orquestador: `run(parts=(...))`; solo regenera la colección `CYBERTRUCK` |

### Cómo escribir una pieza nueva (patrón v3)

```python
from ct_v3 import box, cyl, bolt, rivet            # + el resto de formas
import ct_v3 as V3
V3.part(M, "BODY_Nombre", "BODY_STRUCTURE", ["ecoat", "zinc"], [
    box((0.45, 1.20, 0.80), (0.10, 0.20, 0.05), 0.003),                 # centro, tamaño, radio de bisel, material (0)
    bolt((0.45, 1.20, 0.83), (0, 0, 1), 0.010, 1),                      # posición, eje, diámetro, material (1)
], "Soporte {lado} de lo que sea (3 tornillos a 10 N·m)", mirror=True,   # genera _R y _L reflejando COORDENADAS
   edir=(1, 0, 0.3), dist=0.4, stage=3)                                   # explosión: dirección, metros, etapa
```

- Las coordenadas son de mundo, del lado derecho (+X). Con `mirror=True` se refleja la entrada, no la malla, así las
  normales quedan bien.
- `mats` son **nombres** de la biblioteca; el índice de material de cada forma se recorta al número de materiales.
- Si `edir` es `None` se calcula una dirección por defecto desde el centroide. La etapa por defecto sale de la
  colección (`STAGE` en `ct_v3.py`).
- Materiales disponibles (`M`): alu_cast, alu_forged, alu_machined, alu_trim, anodized_dark, battery, black_gloss,
  brake_pad, busbar_alu, bushing, caliper, carpet, cell, chrome, composite, connector_blue, connector_grey, copper,
  ecoat, fastener_black, foam_green, glass_frit, glass_lens(_red/_smoke), glass_roof/side/windshield, ground,
  harness, headliner, hose, hv_orange, int_grey, int_plastic, lamp_housing, leather(_light), led_amber/pcb/red/white,
  mica, mirror, pcb_green, plastic_black/liner/textured, radiator, reflector, rotor, rubber(_seal/_side), screen,
  seatbelt, speaker_mesh, steel(_b/_bare/_black/_c), stitch, tire_letters, valve_brass, wheel_alloy/cover(_edge),
  zinc.
- Colecciones de sistema válidas (nombres exactos): EXTERIOR_PANELS, DOORS_AND_HATCHES, GLASS_AND_MIRRORS, LIGHTING,
  CARGO_BED, BODY_STRUCTURE, BODY_FASTENERS, UNDERBODY, FRONT/REAR_WHEELS_AND_BRAKES, FRONT/REAR_SUSPENSION,
  STEERING, BATTERY_ASSEMBLY, DRIVE_UNITS, INTERIOR_DASHBOARD/CONTROLS/SEATS/DOORS/TRIM.

## 8. Convenciones técnicas y validación

- Metros, escala 1:1. **+Y delante, +X derecha, +Z arriba**; origen en el suelo, plano de simetría, mitad de la
  batalla. En glTF: `(x, y, z)_Blender → (x, z, −y)_glTF`. El conductor va a la **izquierda** (x negativa): el
  volante está en x ≈ −0,39.
- Nombres estables en inglés y MAYÚSCULAS por sistema; sufijos `_FL/_FR/_RL/_RR`, `_L/_R`, `_F/_R`.
- Los conjuntos padre (vacíos `DOOR_*`, `WHEEL_*`, `*_ASSEMBLY`…) **sin rotación**: la dirección de explosión se
  expresa en el espacio del padre.
- Láminas abiertas: `MeshBuilder.face(..., want=dirección)`; **no** `recalc_normals`. Mallas cerradas: la función
  `ct_lib.orient_closed_components` las orienta hacia fuera (propaga sentido coherente y corrige volumen negativo).
- Cada objeto tiene propiedades `explode_dir/dist/stage/group`, `system`, `fidelity`, `label_es`, `note_es`.
  `ct_parts.make` convierte «V» en «R» (criterio: «Verificado» solo si la geometría procede de medidas o planos).
- Coordenadas de referencia útiles: ejes en y = ±1,8175; ruedas en x = ±0,886, z = 0,437; suelo de cabina z = 0,48;
  tapa de la batería z = 0,47 (bandeja 0,28–0,46; x ±0,84, y −1,40…+1,25); salpicadero y 0,95–1,90; asientos
  delanteros y −0,15…0,72; banco trasero y −1,08…−0,30; mamparo y 1,40; frunk y 1,98–2,58; caja y −2,87…−0,98, suelo
  z = 0,865; portón y ≈ −2,94; techo máximo z = 1,7935; capó/cowl y ≈ 1,93, z ≈ 1,28; puertas: juntas en y = +1,188 /
  +0,080 / −0,918; toma de carga en el lado **izquierdo** (x ≈ −1,0, y ≈ −1,3).
- **Cada pieza nueva debe quedar dentro de la envolvente oficial.** Tras añadir piezas se ejecuta
  `validate.run()` y la altura libre (−0,4 mm) y las siluetas no deben empeorar. Tabla base actual (v3):

| Cota | Modelo | Oficial | Desviación |
|---|---|---|---|
| Longitud | 5.684,9 mm | 5.682,9 | +2,0 mm |
| Altura («Medium») | 1.796,7 | 1.793,8 | +2,9 |
| Batalla / vía | 3.635,0 / 1.772,0 | idem | 0 |
| Altura libre | 256,6 | 257,0 | −0,4 |
| Anchura con espejos | 2.413,3 | 2.413,3 | 0 |
| Anchura sin espejos | 2.081,7 | 2.031,6 | +50,1 (discrepancia conocida) |

Siluetas por trazado de rayos (media / máx., mm): superior 2,9 / 13,3 · inferior 13,3 / 121,1 · frontal 16,0 / 151,3 ·
trasero 9,2 / 65,1 · planta 6,7 / 29,3.

- **Truco de diagnóstico que funcionó:** si una cota empeora tras añadir piezas, calcula los mismos rayos con y sin
  los objetos nuevos (dos `validate.bvh(...)`, uno filtrando por nombres de la versión previa) y compara muestra a
  muestra; así se localizaron la fascia, los sellos de espuma, el reflector del hueco del paragolpes, etc.
- Errores típicos al colocar piezas: sobresalir de la planta frontal (que se estrecha: x = 0,62 a y = 2,61), de la
  muesca trasera del paragolpes (y = −2,80 a z = 0,68–0,72), de la línea del techo (`z_top(y)` es la línea central;
  en el parabrisas las piezas interiores deben quedar ≥ 20 mm por debajo) o bajar de la altura libre (z < 0,257 en
  piezas de carrocería).

## 9. Qué falta (respuesta honesta que se le dio al usuario)

- Hay 948 objetos, muchos agrupando piezas físicas (celdas, filas de remaches, grapas). La ficha estima 1.100–1.450
  piezas con nombre propio (sin tornillería ni celdas); un Cybertruck real tiene varios miles de piezas más la
  tornillería. La lista de piezas con nombre está cubierta en su mayor parte, **no entera**.
- Sin modelar: opciones fuera de serie (Terrestrial Armor, barra de luz off-road), piezas propias de otras variantes
  (Long Range, Dual Motor), «secciones de reparación», muchos soportes, espumas, tapicerías y conectores sueltos,
  mazos reales, tornillos individuales, e interiores de los componentes grandes (motores, inversores, reductoras,
  BMS, barras colectoras, interior de faros), que los manuales no publican.
- La forma y la posición de las piezas nuevas son reconstrucciones. Para afinarlas hacen falta escaneos, planos o
  las figuras del manual de reparación (cotas de control y mapa de materiales por pieza), que están en **imagen**.
- Páginas sin leer: las de **Tri Motor (Cyberbeast)** del manual de servicio (RDU LH/RH, inversores, bomba de aceite
  LH, arneses HV, pack «Standard») y ~200 procedimientos de exterior.

## 10. Investigación: fuentes y cómo acceder

La investigación se hizo con el skill `deep-research` (subagentes) y está en `research_notes/Ficha técnica piezas
Cybertruck/` (10 archivos: 7 de primera ronda y 3 `ronda2_…`), el informe en `reports/Ficha técnica piezas
Cybertruck.md` y la ficha consolidada en `docs/ficha-tecnica-piezas.md`.

- **Manual de servicio** (`service.tesla.com/docs/Cybertruck/ServiceManual/en-us/…`): `WebFetch` solo ve la
  navegación; **`curl` extrae el cuerpo** de cada página (GUID en el Anexo A de la ficha). Todas las páginas están
  marcadas DRAFT; las páginas largas se truncan a ~100.000 caracteres.
- **Manual de reparación de carrocería** (`…/BodyRepair/BodyRepairProcedures/en-us/`): igual; cotas de control y
  materiales por pieza son imágenes.
- **Manual del propietario**: `tesla.com` devuelve **403**; el espejo `https://www.tesla.cn/ownersmanual/cybertruck/en_us/`
  sirve el HTML por GUID y el PDF completo (`Owners_Manual.pdf`, ~16 MB, software 2026.20).
- **Hoja de rescate** (4 páginas): `digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf`
  (no «Emergency Response Guide»).
- Fuentes secundarias (marcar «Reconstruido»): Munro & Associates y sus teardowns (Autopian, Lean Design), Basenor,
  InsideEVs, Electrek, Design News, Wikipedia (cuidado con la fiabilidad).
- **Conflictos de fuentes** (30 en la ficha, §6): vía 1.772 vs 1.777 mm; tensión del pack 700 V (manual) vs 800 V
  (hoja de rescate); par del enganche 198 vs 178 N·m; altavoces 15 vs 13; longitud de la escobilla (62 in, ~50 in,
  ~1,22 m); espesor del acero (1,4–1,8 mm vs ~3 mm); etiquetas «coil/air» de la suspensión invertidas en el manual.
  Abiertas sin resolver: reductor trasero (carcasa común vs páginas LH/RH Tri Motor) y fundición trasera (dos mitades
  vs un componente con «Half Section»).

## 11. Qué se hizo en la versión 3 (resumen)

1. Se creó `ct_v3.py` y siete módulos `build_v3_*.py` (387 objetos): estructura en blanco (Super Cowl, Aerobracket,
   cabeceras, pared trasera, pasos de rueda, soportes, placas, tapones, remaches por familia), exterior y caja
   (apliques, juntas, paredes, travesaños, tonneau), chasis (casquillos, rótulas, topes, fuelles, espárragos,
   sensores de altura, circuito de aire), motriz y térmica (Octovalve, bomba, chiller, LCCR, botella, contactores,
   fusibles, arneses HV, pernos del pack), interior (motores y soplador de asientos, airbags, conductos, consola,
   grapas y espuma de puertas), electrónica (cámaras, antenas, BLE, mazos de 48 V, ECU de remolque, TCU).
2. **Fallos corregidos:** 51 mallas cerradas con normales invertidas (`ct_lib.box` y los lathe de perfil cerrado);
   mallas con sentido mixto (carriles de la cubierta); etiquetas y pares que discrepaban de los manuales (tirante
   de puerta 23 N·m, bisagras 38 N·m, controlador trasero con 3 fijaciones, bandeja de batería, número de lamas,
   persianas y LED sin fuente, escobilla, tensión del pack, tamaño de pantallas «Reconstruido»).
3. Se regeneraron GLB, manifiesto, inventario, `validation-results.json` y los 21 renders de `docs/renders/`.
4. Pendiente menor conocido: 7 láminas abiertas (faldillas de aleta, paragolpes delantero, puerta de la toma de
   carga, piloto lateral) conservan 3–16 aristas con caras de sentido discontinuo (no afectan a cotas ni explosión).
   El perfil superior tiene un máximo de 13,3 mm (v2: 10,2) sin localizar con precisión.

## 12. Flujo de trabajo recomendado para continuar

1. Leer `CLAUDE.md`, este archivo y la documentación indicada. Confirmar con `git status` y `git log --oneline -5`
   que `main` está en `cb5854b` o posterior y que no hay cambios pendientes.
2. Proponer rama (`propose_branch`) antes de la primera edición, salvo que el usuario diga otra cosa.
3. Si se modela: editar el módulo correspondiente → `build_all.run(parts=("body","wheels","lights","details",
   "interior","chassis","v3","v4","explode","scene"))` → `validate.run()` + `build_explode.verify_roundtrip()` →
   inspeccionar con renders (Workbench rápido o `render_shot`) → `export_web.export(...)` → guardar el `.blend` →
   `node tools/gen_inventory.mjs` → probar el visor → documentar → commit.
4. Si se toca el visor (`web/`): probarlo en local (explosión 0→100 %, selección, árbol, cámaras, móvil), mantener los
   textos en español y comprobar que no hay errores de consola. Un push a `main` que cambie `web/` despliega Pages
   (tarda ~1 minuto; se puede verificar comparando `…/models/cybertruck-manifest.json` publicado).
5. Mantener actualizados `CLAUDE.md` (estado y pendientes), `README.md`, `docs/model-specification.md` (cifras),
   `docs/research-and-fidelity.md` (validación y novedades) y `docs/ficha-tecnica-piezas.md` (§8.4 estado).
6. No publicar ni hacer `push` sin que el usuario lo pida; no inventar datos de las fuentes; informar con franqueza de
   lo que no se pudo verificar.

## 13. Versión 4 (17-10-2026): coche completo, suelo, luz y HUD

- **Modelo:** `blender/scripts/ct_v4.py` (formas mecánicas de alto detalle; `part(..., frame=)` y `derived(...)`)
  y `build_v4_motriz/chasis/energia/habitaculo/carroceria/tornilleria.py`, orquestados por `build_v4.py`
  (`parts=(…, "v3", "v4", "explode", "scene")`). 189 objetos nuevos, todos «Aproximado» salvo el tornillo central
  del buje («Reconstruido»). Detalle y criterio en `docs/research-and-fidelity.md` §10 y en la ficha §8.5.
- **Validación:** cotas y siluetas idénticas a la v3; explosión con desviación 0 en 1.137 objetos; 1,19 M
  triángulos; GLB 12,0 MB; `.blend` 14,7 MB.
- **Renders:** 26 planos en `docs/renders/` (los 22–26 enseñan el interior con las carcasas ocultas; `preview.SHOTS`
  admite nombres exactos terminados en «$» en la lista de ocultos).
- **Visor:** `web/src/lighting.js` (entornos «Estudio» y «Exterior» por procedimiento, reflejo plano con
  `Reflector`), suelo de cristal / opaco / oculto en `main.js`, HUD nuevo en `index.html` y `style.css` (vidrio
  líquido, tema claro con la luz exterior, menú de escena, pestañas, indicadores deslizantes, adaptado a móvil).
- **Trampas nuevas:** llamar a `bpy.context.view_layer.update()` antes de leer `matrix_world` de objetos recién
  creados; comprobar que las piezas internas no asoman (renders y rayos contra la tapa del frunk); al escribir
  archivos con `node -e "…"` desde Bash, las comillas invertidas se interpretan como sustitución de órdenes (usar
  el editor o un heredoc con comillas simples).
- **Pendiente:** fusionar y publicar (solo cuando el usuario lo pida), formas exactas con fuentes de geometría,
  carga progresiva del GLB y el resto de §9.
