# CLAUDE.md — Instrucciones permanentes del proyecto `cybertruck`

## IDIOMA DE COMUNICACIÓN OBLIGATORIO

* Todo el contenido de comunicación dirigido al usuario debe estar en español.
* Todas las actualizaciones de progreso, mensajes de estado, explicaciones, planes de ejecución comunicados al usuario, resúmenes de fases, informes parciales, informes finales y explicaciones de errores deben estar íntegramente en español.
* Todas las explicaciones que acompañen al trabajo realizado deben estar en español desde el primer momento. No esperes a terminar una fase para cambiar al español.
* Los comentarios de código destinados a explicar el proyecto, la documentación técnica, el README, los informes de investigación y los documentos de seguimiento deben redactarse en español.
* Los nombres de las secciones de la documentación y los textos de la interfaz web deben estar en español, salvo nombres propios, nombres oficiales de productos, identificadores técnicos y convenciones de programación que sea conveniente mantener en su forma original.
* Las instrucciones permanentes de este proyecto deben seguir aplicándose durante todas las sesiones futuras de Claude Code.
* No cambies al inglés por defecto al planificar, ejecutar herramientas, explicar decisiones, informar de avances o documentar resultados.
* Las URL originales, los nombres oficiales de documentos, las denominaciones comerciales, las API, las funciones, las bibliotecas y los identificadores de código pueden conservar su forma original cuando resulte técnicamente apropiado.
* La investigación puede realizarse utilizando fuentes en cualquier idioma. Sin embargo, los resultados, las conclusiones y las explicaciones destinadas al usuario deben expresarse en español.
* Si se incorpora documentación original en otro idioma como referencia, no es necesario modificar el documento fuente. Las explicaciones creadas por Claude sí deben estar en español.

## Entorno de trabajo

* **Blender sin MCP (preferencia del usuario desde el 23-10-2026):** no se usa el Blender de escritorio del usuario
  por Blender MCP. Claude usa **su propio Blender 5.2.2 LTS sin interfaz** en el entorno del agente
  (`blender -b blender/Cybertruck.blend --python script.py`), con los mismos scripts de `blender/scripts/`, que
  regeneran la escena entera. Instalación, prueba completa (reconstrucción en 331 s con validación idéntica) y qué se
  pierde o se gana frente al MCP: `traspaso.md` §17 y `docs/auditoria-2026-10-20-spacex-cybertruck.md` §11.
  Sin GPU en la nube: Cycles en CPU, Workbench para revisiones rápidas, EEVEE solo con Mesa EGL (lento).
* Repositorio: `https://github.com/alvarodesigns34/cybertruck` (rama `main`).
* Archivo maestro de Blender: `blender/Cybertruck.blend`. Nunca se elimina tras exportar.

## Convenciones técnicas

* Escala 1:1, unidades métricas (metros).
* Ejes del vehículo en Blender: **+Y = hacia delante**, **+X = lado derecho del conductor** (vista desde el asiento), **+Z = arriba**. El origen está en el suelo, en el plano de simetría, en el punto medio de la distancia entre ejes.
* En glTF/Three.js (Y arriba) esto se convierte automáticamente: +Y Blender → −Z glTF.
* Los nombres de objetos usan identificadores estables en inglés y MAYÚSCULAS por sistema (p. ej. `EXT_Door_FL_Outer`), sufijos `_FL`, `_FR`, `_RL`, `_RR` para esquinas y `_L`/`_R` para lados.
* Cada objeto desplazable guarda propiedades personalizadas para la vista explosionada (`explode_group`, `explode_stage`, `explode_dir`, `explode_dist`, `system`, `fidelity`). Ver `docs/model-specification.md`.
* Niveles de fidelidad en la documentación: **Verificado**, **Reconstruido**, **Aproximado**.
* No se versionan fotografías de referencia con derechos de autor ni renders temporales.
* Los conjuntos padre (vacíos `DOOR_*`, `WHEEL_*`, `*_ASSEMBLY`…) deben tener rotación nula: la dirección de
  explosión se expresa en el espacio del padre y debe coincidir con la de mundo.
* Las caras de láminas abiertas se orientan con `MeshBuilder.face(..., want=dirección)`; no usar
  `recalc_normals` en superficies abiertas.
* Los perfiles se validan por trazado de rayos (`validate.py`), no por muestreo de vértices.
* Toda pieza nueva debe quedar dentro de la envolvente oficial: tras añadirla se ejecuta `validate.run()` y la
  altura libre (−0,4 mm) y las siluetas no deben empeorar (las piezas que sobresalen se recolocan, no se relaja la
  validación). Las mallas cerradas se orientan hacia fuera con `ct_lib.orient_closed_components`.
* Fuente de nombres, cantidades y fijaciones: `docs/ficha-tecnica-piezas.md` (identificadores EXT-, EST-, CHS-, TRN-,
  INT-, ELE-). Los datos que las fuentes no publican (masas, cotas por pieza) no se inventan: se marcan «Aproximado».

## Flujo de trabajo

1. Editar la ficha (`ct_specs.py`) o el constructor correspondiente en `blender/scripts/`.
2. En Blender sin interfaz (ver «Entorno de trabajo»): `build_all.run(parts=("body","wheels","lights","details","interior","chassis","v3","v4","montaje","explode","scene"))`.
   Las piezas de la versión 3 se escriben con `ct_v3.part` (formas en coordenadas de mundo del lado derecho,
   `mirror=True` para la pareja izquierda) en los módulos `build_v3_*.py`. Las de la versión 4 (interior
   funcional y tornillería) se escriben con `ct_v4.part` (formas mecánicas de alto detalle; `frame=` para usar las
   coordenadas locales de otro objeto y `derived(...)` para espumas o almas a partir de otra malla) en
   `build_v4_*.py`.
3. Validar: `validate.run()` y `build_explode.verify_roundtrip()`; inspeccionar con `preview.py` o las cámaras `CAM_*`.
4. Exportar con `export_web.export(...)`, guardar `blender/Cybertruck.blend` y ejecutar `node tools/gen_inventory.mjs`.
5. Probar el visor con `node tools/serve.mjs web 8080` y publicar con *push* a `main` (GitHub Actions → Pages).

## Estado y puntos de continuación

* **23-10-2026: auditoría conjunta con `spacex` y cambio de criterio.** La auditoría completa está en
  `docs/auditoria-2026-10-20-spacex-cybertruck.md` (con el mismo texto en `alvarodesigns34/spacex`). Dos órdenes
  del usuario que cambian lo escrito más abajo:
  1. **Integración en `spacex`:** el Cybertruck **no** va junto al Model Y ni en el entorno principal de la
     simulación. Tiene un botón propio que lleva a un espacio aparte, como este visor (auditoría §4). Sustituye a
     lo que dicen la hoja de ruta del 18-10 y `traspaso.md` §15.3.
  2. **Blender sin MCP** (ver «Entorno de trabajo» y `traspaso.md` §17).

  **Fases 1 y 2 de la integración, hechas en `spacex` (23-10-2026):** `spacex` lleva una copia de
  `web/models/cybertruck.glb` en `assets/cybertruck/`, hecha con su `tools/cybertruck-sync.mjs` (anota tamaño, SHA-256
  y el commit de aquí que lo cambió) y un «Cybertruck Lab» mínimo con su botón y la tecla **U**. **Si se vuelve a
  exportar el GLB aquí, hay que sincronizarlo en `spacex`** (`node tools/cybertruck-sync.mjs ../cybertruck`) y pasar
  allí sus pruebas. Estado y siguiente fase: `spacex/TRASPASO.md`, «Estado actual (23-10-2026)».

  Hallazgos de la auditoría que tocan a este repositorio: §5 (C1–C24) y mejoras en §8.2. Los más urgentes:
  - el GLB tiene 17 errores del validador de Khronos: ruedas y frenos sin UV (C21);
  - la barra de carga pasa del 100 % con gzip (C1);
  - el CI no valida nada (C10);
  - no hay oclusión ambiental ni horneada ni en el visor (M-CT1).

* Estado al 18-10-2026: publicada la **versión 4.1** en `main` (commit c9b1ea6) y en
  https://alvarodesigns34.github.io/cybertruck/ : 1.139 objetos, GLB de 12,5 MB (1.138 componentes), 78 materiales con
  texturas físicas generadas (`ct_textures.py`, WebP en `blender/textures/`), `Cybertruck.blend` de 16,5 MB;
  cotas, siluetas y explosión validadas (altura libre −0,4 mm; desviación 0 en los 1.139 objetos).
  Módulos: `ct_parts.py`, `build_structure.py`, `build_mechanics.py`, `build_exterior.py`,
  `build_interior_detail.py` (v2); `ct_v3.py`, `build_v3_*.py` (v3, 387 piezas del backlog de
  `docs/ficha-tecnica-piezas.md`); `ct_v4.py`, `build_v4.py`, `build_v4_motriz/chasis/energia/habitaculo/
  carroceria/tornilleria.py` (v4, 189 piezas: interior funcional de los conjuntos y tornillería). Renders:
  `preview.render_shot` (26 planos renovados con la v4; los 5 últimos, con las carcasas ocultas).
* Versión 4 («coche completo», ver `docs/research-and-fidelity.md` §10): interior de motores, reductoras,
  inversores, juntas homocinéticas, rodamientos, pinzas, amortiguadores, actuadores, servofreno, bomba de freno, HCU,
  compresor, batería (BMB, BMS, barras, junta), PCS, 48 V, placas de 33 módulos, climatizador, compresor de A/C,
  asientos (armazón, muelles, espumas), volante, enrolladores, pantallas, altavoces, vigas de puerta, faros, tomas
  de remolque, emblema Cyberbeast y 21 juegos de tornillería. Las carcasas se apartan más que su contenido en la
  explosión. Todo lo interior es «Aproximado» (forma y recuentos reconstruidos).
* Visor (v4): HUD de vidrio líquido (`web/src/style.css`, `web/index.html`), suelo de cristal / opaco / oculto,
  entornos HDR propios «Estudio» y «Exterior» y reflejo plano del suelo (`web/src/lighting.js`), mapeo AgX;
  preferencias en `localStorage`. El gancho de pruebas `window.__ct` expone `setFloor`, `setEnvironment` y
  `setReflections`. Resuelto el hallazgo de las piezas que quedaban bajo el suelo opaco al explosionar.
* Criterio de fidelidad: «Verificado» solo si la geometría procede de medidas o planos; las piezas cuya
  existencia y fijaciones constan en el manual pero cuya forma es reconstruida se marcan «Reconstruido»
  (`ct_parts.make` lo aplica automáticamente).
* Hoja de ruta del 17-10-2026: **completada** en la versión 4 (más piezas, hiperrealismo, suelo de cristal,
  iluminación y reflejos, HUD tipo Apple).
* **Versión 4.2 (18-10-2026, publicada en `main`, commit 2d590ae): interferencias de ensamblaje a cero.** 0 parejas de más de 3 mm
  (de 280), 320 penetraciones intencionadas declaradas con su motivo (uniones reales) y 240 cruces de 1–3 mm por debajo
  del umbral. Cotas, siluetas y explosión validadas (perfil trasero mejor: 7,8 mm de media); GLB de 12,5 MB,
  `Cybertruck.blend` de 16,2 MB. Detalle, método y lecciones en `docs/research-and-fidelity.md` §12 y `traspaso.md`
  §16. Novedades técnicas: profundidad medida sólido a sólido en `interferencias.py`, alojamientos por caja
  (`build_montaje.POCKETS`), recortes con `MANIFOLD` primero y el solver exacto solo al final, puntos de los soportes
  de las unidades motrices en `build_mechanics.DU_MOUNTS`.
* **Hoja de ruta del 18-10-2026 (siguiente sesión, en este orden):** (1) ~~terminar las 279 interferencias de
  `docs/interferencias-pendientes.md`~~ (hecho en la v4.2); (2) pulido general del modelo (fallos visibles, formas, materiales); (3)
  integrar el Cybertruck en la simulación `alvarodesigns34/spacex` junto al Tesla Model Y, con una opción de
  «vista explosionada» que lleve a un espacio de despiece aparte. Detalle en `traspaso.md` §15.
* Versión 4.1 (17-10-2026, interferencias de ensamblaje): detector `interferencias.py` (superficie visible,
  profundidad cerca del cruce, penetraciones intencionadas), pasada de montaje `build_montaje.py` (parte
  `"montaje"`: recortes y juntas comprimidas), interiores ajustados o recortados en su carcasa
  (`build_v4.fit_internals`) y numerosas recolocaciones en los constructores: de ~1.110 a 279 parejas que se atraviesan más de 3 mm (53 de más
  de 10 mm); 1.139 objetos, GLB de 12,5 MB, `Cybertruck.blend` de 16,5 MB, cotas y explosión validadas. Lo que queda está en
  `docs/interferencias-pendientes.md` (`node tools/gen_interferencias.mjs <interf.json>`); método y lecciones en
  `docs/research-and-fidelity.md` §11 y `traspaso.md` §14. No usar el solver booleano `EXACT` con mallas grandes o
  abiertas: cierra Blender.
* Lecciones de la v4: (1) antes de leer `matrix_world` de objetos recién creados hay que llamar a
  `bpy.context.view_layer.update()` (`build_v4.build_all` ya lo hace); (2) las piezas internas pueden asomar por
  la carrocería: comprobarlo con renders y con rayos verticales contra la tapa del frunk; (3) las texturas se
  repiten cada pocos centímetros, así que no sirven para huellas o suciedad localizada (se probó y se descartó).
* Mejoras pendientes más valiosas: forma exacta de faros, retrovisores, paragolpes y piezas fundidas (requiere
  escaneo o fotografías ortogonales); molde real del Scorpion ATR; carga progresiva del GLB por sistemas (12,0 MB);
  verificación de la sección transversal con una vista frontal a escala; leer las figuras del manual de reparación
  (cotas de control y mapa de materiales por pieza) y las páginas Tri Motor del manual de servicio; opciones fuera
  de serie (Terrestrial Armor, barra de luz off-road); tornillería individual en las uniones que aún la llevan
  integrada en la malla.
