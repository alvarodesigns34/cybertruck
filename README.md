# Cybertruck — reconstrucción 3D documentada

Reconstrucción 3D a escala 1:1 del **Tesla Cybertruck Cyberbeast** (gama comercial vigente en EE. UU.),
construida en **Blender 5.2** a partir de la documentación oficial de Tesla y de mediciones sobre sus vistas
ortográficas, con **vista explosionada reversible** y un **visor web interactivo** en Three.js.

**Visor en línea:** https://alvarodesigns34.github.io/cybertruck/

![Tres cuartos delantera](docs/renders/01_tres_cuartos_delantera.jpg)

| | |
|---|---|
| ![Exterior de día](docs/renders/11_exterior_dia.jpg) | ![Atardecer](docs/renders/12_atardecer.jpg) |
| ![Chasis y tren motriz](docs/renders/14_chasis_y_tren_motriz.jpg) | ![Vista explosionada](docs/renders/10_vista_explosionada.jpg) |
| ![Batería 4680](docs/renders/16_bateria.jpg) | ![Suspensión delantera](docs/renders/17_suspension_delantera.jpg) |
| ![Unidad trasera tri-motor](docs/renders/18_unidad_trasera_trimotor.jpg) | ![Estructura de carrocería](docs/renders/15_estructura_carroceria.jpg) |
| ![Asientos y costuras](docs/renders/19_asientos_y_costuras.jpg) | ![Caja, tonneau y portón](docs/renders/21_caja_tonneau_y_porton.jpg) |
| ![Rueda y freno](docs/renders/08_rueda_y_freno.jpg) | ![Faro y barra de luz](docs/renders/20_faro_y_barra_de_luz.jpg) |
| ![Motor delantero por dentro](docs/renders/22_motor_delantero_por_dentro.jpg) | ![Unidad trasera por dentro](docs/renders/23_unidad_trasera_por_dentro.jpg) |
| ![Pinza por dentro](docs/renders/24_pinza_por_dentro.jpg) | ![Asiento por dentro](docs/renders/25_asiento_por_dentro.jpg) |

Los 26 planos de `docs/renders/` se renderizan con Cycles bajo cuatro iluminaciones (estudio, cielo físico de
día, atardecer y cielo cubierto); los cinco últimos muestran el interior funcional de la versión 4 con las
carcasas ocultas.

## Qué contiene (versión 4)

- **1.139 objetos** (versión 4.2; 1.137 en la 4.0) en 20 colecciones de sistema, frente a 948 en la versión 3, 561
  en la 2 y 309 en la 1.
- **Versión 4, «coche completo» (+189 objetos):** el interior funcional de los conjuntos que antes eran carcasas
  cerradas: estátores con devanado de horquillas o distribuido, rotores de imanes y de jaula de cobre, ejes,
  rodamientos y resolvers de los tres motores; trenes de engranajes helicoidales, diferencial delantero y
  reductoras traseras independientes; inversores con módulos de potencia, condensador y placas; juntas
  homocinéticas, rodamientos de buje, pistones de las pinzas, interior de amortiguadores, actuadores de dirección,
  servofreno, bomba de freno, HCU y compresor de aire; placas BMB, BMS y barras de la batería, PCS, ACJB, batería
  de 48 V y placas de 33 módulos electrónicos; climatizador, compresor de espiral y ventiladores por dentro;
  armazones, muelles y espumas de los asientos, alma del volante, enrolladores, pantallas y altavoces; vigas de
  puerta, interior de faros, tomas de remolque, emblema Cyberbeast y 21 juegos de tornillería individual. Las
  piezas internas son reconstrucciones etiquetadas «Aproximado» (ver [§10](docs/research-and-fidelity.md)).
- **Hiperrealismo:** texturas nuevas de placa de circuito, espuma, fieltro, mecanizado y zincado (78
  materiales). Muchas mallas agrupan piezas repetidas (1.344 celdas, tornillería, grapas, remaches), por lo que el número
  de piezas físicas representadas es muy superior.
- **Versión 3 (+387 objetos, +1,7 MB de GLB):** se han añadido las piezas del backlog de
  [`docs/ficha-tecnica-piezas.md`](docs/ficha-tecnica-piezas.md) §8.3: soportes y refuerzos de la carrocería en
  blanco (Super Cowl, Aerobracket, cabeceras, pared trasera, pasos de rueda, placas y tapones, remaches por
  familia), apliques y juntas exteriores, caja y tonneau (paredes, travesaños, cierres, bloques de leva), casquillos,
  rótulas, topes, fuelles de semieje, espárragos y sensores de altura, circuito de aire (SCUBA, racores VOSS, haces
  de líneas), Octovalve, bomba, enfriador, LCCR y botella de refrigerante, contactores y fusibles de la bahía auxiliar,
  arneses HV, cámaras y antenas, mazos de 48 V, motores y soplador de los asientos, airbags individuales, sensores de
  impacto y de ocupación, conductos de climatización, grapas y espuma de los paneles de puerta. Se corrigieron
  además fallos del modelo (normales invertidas, etiquetas y pares que discrepaban de los manuales).
- **Estructura de carrocería** con las cotas de control del manual de reparación: piezas fundidas delantera y
  trasera (esta por mitades), umbrales de acero UHSS con inserto extruido, refuerzos del suelo, anillos de
  puertas, «mast» y torres del portón fundidos, vigas de impacto, Megabeam, viga del salpicadero y remaches
  flow-form.
- **Mecánica**: suspensión de doble horquilla con portamanguetas, brazos con casquillos y rótulas, módulos de
  muelle neumático desglosados (amortiguador, vástago, fuelle, pistón, copela), estabilizadoras, actuadores de
  dirección por cable con dos motores, unidades motrices con carcasas aleteadas, inversores, intercambiadores,
  bombas de aceite y soportes, semiejes con juntas y fuelles, subchasis, Supermanifold/Octovalve, compresor de
  A/C, módulo de ventiladores, persianas activas, servofreno electromecánico, HCU, tubos de freno, compresor,
  depósito y bloque de válvulas de la suspensión, batería de 48 V, controladores zonales, mazos de cables y
  deflectores inferiores.
- **Batería** de 4 bloques de 7 × 48 celdas 4680 con espuma estructural, refrigeradores en serpentín, mica,
  colectores, pirofusibles, respiradero térmico y bahía auxiliar (ACJB, PCS, clúster de dispositivos).
- **Exterior**: faros con proyectores y disipadores, fila de 64 LED en la barra de luz, retrovisores facetados con
  cristal electrocrómico, limpiaparabrisas completo con motor y lavaparabrisas, bisagras, cierres, presentadores,
  elevalunas, controladores y burletes de las puertas, herrajes del frunk y del portón, cubierta con raíles,
  motores, casete y lamas extruidas, toma NACS con contactos, faldillas, difusor y soporte frontal.
- **Ruedas**: neumático con dibujo «all-terrain» de 5 hileras, tacos de flanco e inscripciones en relieve,
  tapacubos Core facetado, válvula con TPMS, buje con espárragos, pinzas detalladas y pastillas.
- **Interior**: volante con botonera y rodillos, actuador de realimentación, consola esculpida con cargadores
  inalámbricos y USB-C, guantera, desempañado, guarnecidos de pilares con altavoces, paneles de puerta completos con
  luz ambiental, asientos con guías, mandos y costuras proyectadas, cinturones con enrolladores y hebillas,
  climatización, ordenador, airbags y alfombrillas.
- **Materiales con texturas físicas** generadas (acero satinado anisótropo, caucho, granulado, piel, tejido,
  moqueta, fundición) que viajan al GLB (WebP + KHR_texture_transform), por lo que el visor web muestra el
  mismo aspecto que Blender.
- **Cotas oficiales intactas** también en la versión 4: longitud +2,0 mm, batalla y vía exactas, altura libre
  −0,4 mm, altura +2,9 mm, anchura con espejos exacta (0,0 mm). Detalles en [`docs/research-and-fidelity.md`](docs/research-and-fidelity.md).
- **Metadatos y vista explosionada** en 6 etapas para cada pieza; desviación 0 tras ciclos repetidos en Blender
  (1.139 objetos) y funcionamiento comprobado en el navegador. Las carcasas se apartan más que su contenido,
  como en un despiece de taller.

## Estructura del repositorio

```
CLAUDE.md                       Normas permanentes del proyecto (idioma español, convenciones)
blender/Cybertruck.blend        Escena maestra de Blender (no se elimina nunca)
blender/scripts/                Scripts de construcción, validación y exportación (Python/bpy)
blender/reference_data/         Perfiles medidos sobre la vista oficial (datos derivados)
blender/textures/               Texturas físicas generadas por script (WebP)
web/                            Visor web estático (GitHub Pages)
web/models/                     cybertruck.glb (Draco) y manifiesto de componentes
docs/                           Investigación, especificación, inventario, validación, renders y auditorías
web/vendor/                     Three.js r170, el decodificador Draco y las tipografías (sin CDN)
tools/                          Servidor local, inventario, comprobación (check.mjs) y validador de Khronos (validate_glb.mjs)
.github/workflows/pages.yml     Validación y despliegue automático del visor
```

## Abrir la escena de Blender

1. Abrir `blender/Cybertruck.blend` con Blender 5.2 o posterior.
2. La colección **CYBERTRUCK** contiene el vehículo; **STUDIO**, el estudio, las luces y las 10 cámaras de
   inspección (`CAM_3Q_Front`, `CAM_Side_Profile`, `CAM_Interior`, `CAM_Underbody`, `CAM_Exploded`, …).
3. **Vista explosionada:** seleccionar `CYBERTRUCK_ROOT` y modificar su propiedad personalizada `explode`
   (Propiedades del objeto → Propiedades personalizadas) entre 0 y 1. Los controladores usan expresiones simples,
   por lo que funcionan sin habilitar la ejecución automática de scripts.

### Regenerar el modelo desde los scripts

**Desde el 23-10-2026, Claude trabaja con su propio Blender sin interfaz, no con el del usuario por Blender MCP**
(preferencia del usuario). Es Blender 5.2.2 LTS para Linux, en el entorno del agente:
`blender -b blender/Cybertruck.blend --python script.py`. La instalación, un script de ejemplo y lo que cambia frente al
MCP están en `traspaso.md` §17. Se comprobó el 23-10: la reconstrucción completa tarda 331 s en 4 núcleos sin GPU y
la validación sale idéntica.

En la consola de Python de Blender (o en un script con `blender -b`):

```python
import sys; sys.path.insert(0, r"<ruta-del-repo>/blender/scripts")
import build_all
build_all.run(parts=("body", "wheels", "lights", "details", "interior", "chassis", "v3", "v4", "montaje", "explode", "scene"))
import validate; print(validate.run())            # cotas y siluetas
import export_web
export_web.export(r"<ruta-del-repo>/web/models/cybertruck.glb",
                  r"<ruta-del-repo>/web/models/cybertruck-manifest.json")
```

`build_all.run` solo elimina y regenera la colección CYBERTRUCK; el resto de la escena se conserva. La parte
`"montaje"` (`build_montaje.py`) es el ajuste final que elimina interferencias de ensamblaje (recortes y juntas
comprimidas) y tarda unos minutos; `import interferencias; interferencias.run()` lista las piezas que se siguen
atravesando (informe en `docs/interferencias-pendientes.md`, generado con `node tools/gen_interferencias.mjs`).

## Visor web

No requiere compilación: es HTML + módulos ES con Three.js 0.170. Desde el 23-10-2026 todo se sirve desde el
repositorio (`web/vendor/`: Three.js, `DRACOLoader`, el decodificador Draco, `Reflector` y las tipografías Inter y
JetBrains Mono, con sus licencias); antes dependía de jsDelivr y de Google Fonts, y si fallaban el visor no arrancaba.

```bash
node tools/serve.mjs web 8080
```

Abrir `http://localhost:8080/`. Funciones:

- **HUD de vidrio líquido** al estilo de Apple: cápsulas y paneles translúcidos con desenfoque y brillo especular,
  controles segmentados con indicador deslizante, tema oscuro con la luz de estudio y claro con la exterior,
  adaptado a tabletas y móviles, accesible con teclado (R restablece la vista, espacio anima, Esc cierra) y con
  movimiento reducido si el sistema lo pide.
- Rotación, zoom y desplazamiento con ratón o gestos táctiles; cámaras predefinidas y botón «Restablecer vista».
- **Barra «Vista explosionada» 0–100 %**, animación automática y botón «Ensamblar»; cada etapa muestra su avance
  y al pulsarla se excluye o incluye de la explosión (exploración selectiva).
- **Ajustes de escena** (botón del sol): suelo **de cristal** semitransparente (por defecto), **opaco** u
  **oculto**; luz de **estudio** o **exterior** (entornos HDR propios generados por procedimiento, mapeo de tonos
  AgX como en Blender); **reflejo plano** del suelo (activado en equipos de sobremesa) y amplitud de la explosión.
  Las preferencias se recuerdan en el navegador.
- Clic en una pieza: resaltado y ficha con sistema, conjunto, etapa, nivel de fidelidad y nota; acciones
  **Aislar**, **Ocultar** y **Encuadrar**.
- **Aperturas** (menú de escena): puertas, frunk y portón sobre sus bisagras (ángulos de puertas y frunk ≈).
- Panel con pestañas: sistemas (mostrar u ocultar por sistema) y árbol de componentes con búsqueda y ocultación
  individual.

Tras modificar el modelo en Blender, regenerar el inventario con `node tools/gen_inventory.mjs` y comprobar con
`node tools/check.mjs` (contrato del GLB, coherencia con el manifiesto, visor sin CDN y sintaxis) y
`node tools/validate_glb.mjs` (validador oficial de Khronos; necesita `npm i --no-save gltf-validator@2.0.0-dev.3.10`).
La prueba de humo con navegador es `node tools/smoke.mjs` (necesita `npm i --no-save playwright@1.56.1`).
El GLB también va a la simulación `alvarodesigns34/spacex`, que guarda una copia: después de exportarlo, hay que
sincronizarla allí (`node tools/cybertruck-sync.mjs ../cybertruck`).

### Correcciones de la auditoría del 20-10-2026 (hechas el 23-10-2026)

- **C1, barra de carga:** pasaba del 100 % (hasta el 136 %) porque Pages sirve el GLB con gzip y `Content-Length`
  es entonces el tamaño comprimido. Ahora la descarga se lee como flujo y, si hay codificación de transferencia,
  la barra es indeterminada y el texto da los megabytes recibidos. Nunca se pide el archivo dos veces.
- **C2, sin CDN:** Three.js, Draco, `Reflector` y las tipografías están en `web/vendor/`.
- **C3:** el manifiesto ya no se descarga en el visor, que no lo usaba: todo sale de los extras del GLB.
- **C4:** `pagehide` solo libera los recursos si la página no se queda en la caché de ida y vuelta.
- **C7:** el servidor local comprueba la contención con una ruta relativa (una carpeta hermana `web2/` ya no pasa).
- **C8:** las etiquetas del modelo se escriben con `textContent`, no con `innerHTML`.
- **C9, accesibilidad:** las pestañas siguen el patrón WAI-ARIA (una sola en el orden de tabulación, flechas, Inicio y
  Fin) y la lista de componentes ya no se declara `role="tree"` sin elementos `treeitem`: es un grupo de
  `details`, accesibles por sí mismos.
- **C10, el CI valida:** `tools/check.mjs` y el validador de Khronos corren en cada *push* (también en las ramas
  `claude/**` y en las peticiones de cambios), y el despliegue desde `main` espera a que pasen.
- **C11 y C12:** aislar una pieza vuelve a encender los chips de sistema; el resaltado usa una copia compartida por
  material en vez de clonar uno por malla en cada selección.
- **C13:** el rayado de respaldo del acero usa un generador de semilla fija.
- **C20:** las etiquetas de sistemas y de fidelidad del inventario salen de `web/src/config.js` (antes, copiadas).
- **C21, UV de ruedas y frenos:** 17 mallas compartidas (neumático, discos, pinzas, pastillas, bujes, protectores,
  tapacubos, tuercas y válvula) se creaban sin UV y salían con `texCoord −1`. Eran los 17 errores del validador de
  Khronos, y en la web esas piezas perdían sus texturas. `export_web.prepare_meshes` les da al exportar la proyección
  por caja del proyecto (1 unidad UV = 1 m). Resultado: **0 errores**, el neumático muestra su dibujo y el GLB pasa
  de 83 a 78 materiales, los de `ct_materials.py` (el exportador duplicaba cinco). Pesa 12,62 MB (+0,14 MB de UV).
  Se exportó desde el `.blend` tal cual, sin reconstruir, así que la geometría no cambia (el manifiesto sale
  idéntico byte a byte).
- **M-CT9, dibujo bajo demanda:** el visor solo dibuja cuando algo cambia (cámara, explosión, selección,
  visibilidad, aperturas, suelo, luz o tamaño) y rehace el mapa de sombras solo si cambió algo que proyecta o recibe
  sombra. En reposo, cero fotogramas. Antes dibujaba ≈2.090 mallas, sus sombras y el reflejo en cada fotograma.
- **M-CT4, aperturas:** el menú de escena tiene *Puertas*, *Frunk* y *Portón*, que giran sobre los pivotes que trae
  el GLB (el origen de cada nodo es su bisagra). Tesla no publica los ángulos de apertura: las puertas (65°) y el
  frunk (55°) son **aproximados**; el portón baja hasta quedar horizontal (90°). Las alturas de la suspensión
  neumática quedan pendientes: hacen falta los brazos articulados en Blender para no inventar cómo se mueve.
- **Prueba de humo** (`tools/smoke.mjs`, en el CI): sirve el GLB con gzip como Pages y comprueba la barra, que no
  haya peticiones externas, las 1.138 piezas, la explosión reversible, cero fotogramas en reposo y las aperturas.
- **C24:** las 24 mallas con el nombre temporal `_tmp_isl.NNN` de `build_montaje.py` toman al exportar el nombre de
  su objeto.

## Despliegue

El flujo `.github/workflows/pages.yml` valida el modelo y el visor (`tools/check.mjs` y el validador de Khronos) y,
si pasan, publica la carpeta `web/` en GitHub Pages en cada *push* a `main` que modifique el visor o las herramientas
(también se puede lanzar manualmente). En las ramas `claude/**` y en las peticiones de cambios solo valida. Requiere que Pages esté configurado con
«Source: GitHub Actions» en los ajustes del repositorio.

## Documentación

- [Investigación y registro de fidelidad](docs/research-and-fidelity.md) — fuentes, método de medición,
  ficha técnica, categorías V/R/A por conjunto, discrepancias y resultados de validación.
- [Especificación del modelo](docs/model-specification.md) — coordenadas, jerarquía, metadatos, sistema de
  explosión, materiales y canal de producción.
- [Inventario de componentes](docs/component-inventory.md) — generado a partir de los objetos reales.
- [Resultados de validación](docs/validation-results.json).

## Próximos pasos

- **Auditoría del 20-10-2026 (revisada el 23-10):** `docs/auditoria-2026-10-20-spacex-cybertruck.md`, conjunta con la
  simulación `spacex`. Contiene la integración del Cybertruck en un espacio aparte con su botón (ya no «junto al
  Model Y»), los hallazgos de este repositorio (C1–C24), las mejoras propuestas (§8.2) y el trabajo con Blender sin
  MCP (§11).
- **Sesión del 18-10-2026:** interferencias de ensamblaje a cero (versión 4.2, hecho); siguen el pulido general del
  modelo y su integración en la simulación [`alvarodesigns34/spacex`](https://github.com/alvarodesigns34/spacex)
  (desde el 20-10, sin aparecer en su entorno principal: un botón lleva a un espacio de despiece aparte). Ver
  `traspaso.md` §15–§17 y la auditoría.

La hoja de ruta acordada el 17-10-2026 (más piezas, hiperrealismo, suelo de cristal, iluminación y reflejos, HUD)
se completó en la versión 4. Lo que queda, por orden de valor:

- **Formas exactas** de faros, retrovisores, paragolpes, fundiciones y del molde del Scorpion ATR: requieren
  escaneos, planos o fotografías ortogonales a escala.
- **Carga progresiva** del GLB por sistemas (12,6 MB de una vez).
- Opciones fuera de serie (Terrestrial Armor, barra de luz off-road) y tornillería individual en las uniones que
  todavía la llevan integrada en la malla de su pieza.
- Leer las figuras del manual de reparación y las páginas Tri Motor del manual de servicio.

## Limitaciones principales

- **Interferencias de ensamblaje:** desde la versión 4.2 no queda ninguna pareja de piezas que se atraviese más de
  3 mm (eran unas 1.110 en la v4 y 279 en la v4.1). Quedan 320 penetraciones intencionadas, todas uniones reales
  (tornillos, casquillos prensados, pasamuros, juntas comprimidas…), y 240 contactos de 1–3 mm por debajo del
  umbral. Ver `docs/interferencias-pendientes.md` y `docs/research-and-fidelity.md` §11–§12.

- La carrocería exterior está reconstruida con gran precisión dimensional, pero la sección transversal depende de
  dos inclinaciones deducidas (6° y 19°) que no se han podido medir en una vista frontal a escala.
- Mecánica, batería, piezas fundidas e interior respetan la denominación, las fijaciones y las cotas de control
  de los manuales, pero sus formas son reconstrucciones (no hay planos CAD públicos).
- El dibujo del neumático sigue la arquitectura de un «all-terrain» de 5 hileras, no el molde exacto del Scorpion
  ATR; las inscripciones usan una tipografía genérica.
- La anchura «sin espejos» oficial (2.031,6 mm) no es compatible con la anchura de los neumáticos; el modelo
  sigue la planta oficial, con aletas a ±1,04 m (2.081,7 mm).
- Las texturas son sintéticas (no escaneadas); el GLB pesa 12,6 MB y se carga de una vez.
- Las piezas de la versión 3 tienen nombre, cantidad y fijaciones verificados en los manuales de Tesla, pero su
  forma y posición exactas son reconstrucciones (no hay planos); los manuales no publican masas ni cotas por pieza.
  Las piezas interiores de la versión 4 (engranajes, rodamientos, bobinados, placas, espumas…) son
  reconstrucciones de ingeniería etiquetadas «Aproximado»: existen y cumplen su función, pero su forma, sus
  dimensiones y sus recuentos no proceden de Tesla.
  Quedan fuera las opciones no incluidas de serie (Terrestrial Armor, barra de luz off-road) y las piezas de
  variantes que no son Cyberbeast.

## Créditos y derechos

Proyecto de reconstrucción independiente, sin afiliación con Tesla, Inc. «Tesla», «Cybertruck» y «Cyberbeast» son
marcas de Tesla, Inc. No se incluyen fotografías ni imágenes de terceros: solo datos de medición derivados.
