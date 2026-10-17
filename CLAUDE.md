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

* Blender 5.2 (5.2.2 LTS) conectado mediante Blender MCP. El modelado se hace sobre la escena real de Blender; los scripts de `blender/scripts/` complementan ese trabajo y permiten regenerar la escena.
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
2. En Blender (MCP): `build_all.run(parts=("body","wheels","lights","details","interior","chassis","v3","explode","scene"))`.
   Las piezas de la versión 3 se escriben con `ct_v3.part` (formas en coordenadas de mundo del lado derecho,
   `mirror=True` para la pareja izquierda) en los módulos `build_v3_*.py`.
3. Validar: `validate.run()` y `build_explode.verify_roundtrip()`; inspeccionar con `preview.py` o las cámaras `CAM_*`.
4. Exportar con `export_web.export(...)`, guardar `blender/Cybertruck.blend` y ejecutar `node tools/gen_inventory.mjs`.
5. Probar el visor con `node tools/serve.mjs web 8080` y publicar con *push* a `main` (GitHub Actions → Pages).

## Estado y puntos de continuación

* Estado al 17-10-2026 (versión 3): 948 objetos (909 mallas), ~653 mil triángulos, 61 materiales con texturas
  físicas generadas (`ct_textures.py`, WebP en `blender/textures/`), GLB de 7,0 MB; validado (cotas sin cambios,
  explosión con desviación 0 en los 948 objetos), exportado al visor. La versión 2 (16-10-2026, 561 objetos) está
  publicada en https://alvarodesigns34.github.io/cybertruck/; la 3 se publica al fusionar la rama
  `modelo-v3-piezas-faltantes` en `main`.
  Módulos: `ct_parts.py`, `build_structure.py`, `build_mechanics.py`, `build_exterior.py`,
  `build_interior_detail.py` (v2) y `ct_v3.py`, `build_v3.py`, `build_v3_estructura/exterior/chasis/motriz/interior/
  electronica/complemento.py` (v3, 387 piezas del backlog de `docs/ficha-tecnica-piezas.md`). Renders de validación:
  `preview.render_shot` (21 planos, 4 iluminaciones; los de `docs/renders/` son de la versión 2).
* Versión 3: se corrigieron las normales invertidas de 51 mallas cerradas y varias etiquetas que discrepaban de
  los manuales (ver `docs/research-and-fidelity.md` §9).
* Criterio de fidelidad: «Verificado» solo si la geometría procede de medidas o planos; las piezas cuya
  existencia y fijaciones constan en el manual pero cuya forma es reconstruida se marcan «Reconstruido»
  (`ct_parts.make` lo aplica automáticamente).
* Hallazgo pendiente del visor (17-10-2026, aún sin implementar): al explosionar, muchas piezas de la parte baja
  (suspensión, tren motriz, batería, bajos) descienden por debajo del suelo (`web/src/main.js`: círculo opaco de
  radio 26 m en y = −0,002 y rejilla en y = 0) y solo se ven si la cámara atraviesa el suelo. Es coherente con la
  fórmula de explosión (`explode_dir` hacia −Z en los conjuntos bajos), pero dificulta ver el despiece. Propuesta
  acordada con el usuario: **suelo de cristal semitransparente** (se ve a través de él lo que queda debajo) y una
  **opción para ocultar el suelo**. Solo toca el visor: no cambia el modelo, las direcciones de explosión ni
  Blender. Ver `README.md` (Limitaciones principales).
* Mejoras pendientes más valiosas: forma exacta de faros, retrovisores, paragolpes y piezas fundidas (requiere
  escaneo o fotografías ortogonales); molde real del Scorpion ATR; carga progresiva del GLB por sistemas (ya 7,0 MB);
  verificación de la sección transversal con una vista frontal a escala; leer las figuras del manual de reparación
  (cotas de control y mapa de materiales por pieza) y las páginas Tri Motor del manual de servicio; opciones fuera
  de serie (Terrestrial Armor, barra de luz off-road); renovar los renders de `docs/renders/` con las piezas nuevas.
