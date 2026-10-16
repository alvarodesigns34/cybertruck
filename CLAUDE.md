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

## Flujo de trabajo

1. Editar la ficha (`ct_specs.py`) o el constructor correspondiente en `blender/scripts/`.
2. En Blender (MCP): `build_all.run(parts=("body","wheels","lights","details","interior","chassis","explode","scene"))`.
3. Validar: `validate.run()` y `build_explode.verify_roundtrip()`; inspeccionar con `preview.py` o las cámaras `CAM_*`.
4. Exportar con `export_web.export(...)`, guardar `blender/Cybertruck.blend` y ejecutar `node tools/gen_inventory.mjs`.
5. Probar el visor con `node tools/serve.mjs web 8080` y publicar con *push* a `main` (GitHub Actions → Pages).

## Estado y puntos de continuación

* Estado al 16-10-2026: modelo completo (309 objetos), validado, exportado y publicado en
  https://alvarodesigns34.github.io/cybertruck/. Detalle en `README.md` y `docs/`.
* Mejoras pendientes más valiosas: dibujo real del Scorpion ATR e inscripciones; forma exacta de faros,
  retrovisores y paragolpes inferior; detalle del interior (costuras, mandos, paneles de puerta) y de la
  mecánica (piezas fundidas, brazos); verificación de la sección transversal con una vista frontal a escala.
