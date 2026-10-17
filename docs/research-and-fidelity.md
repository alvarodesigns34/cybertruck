# Investigación y registro de fidelidad

Este documento recoge las fuentes, las mediciones y el grado de certeza de cada conjunto del modelo.
Se usan tres categorías:

- **Verificado (V):** respaldado directamente por mediciones, diagramas o documentación técnica fiable.
- **Reconstruido (R):** inferido a partir de varias referencias coherentes y de relaciones de ingeniería.
- **Aproximado (A):** insuficientemente documentado; se representa con la interpretación mejor fundamentada disponible.

Ningún componente reconstruido o aproximado debe considerarse una pieza OEM exacta.

---

## 1. Vehículo de referencia

**Configuración elegida: Tesla Cybertruck Cyberbeast, mercado de EE. UU., gama comercial vigente (consulta del configurador el 16-10-2026).**

| Dato | Valor | Fuente | Categoría |
|---|---|---|---|
| Gama disponible en el configurador | Dual Motor All-Wheel Drive (74.990 USD), Premium All-Wheel Drive (84.990 USD), Cyberbeast (99.990 USD) | [Configurador oficial](https://www.tesla.com/cybertruck/design) | V |
| Cyberbeast: tracción | «Tri-motor all-wheel drive», vectorización de par trasera, modo de salida | Configurador oficial | V |
| Cyberbeast: prestaciones anunciadas | 320 mi (est.), 11.000 lb de remolque, 0-60 mph en 2,6 s | Configurador oficial | V |
| Cyberbeast: ruedas de serie | 20" «Core Wheels» con neumáticos para todas las estaciones | Configurador oficial | V |
| Cyberbeast: interior | Decoración «Tactical Grey» | Configurador oficial | V |
| Año de modelo | El configurador no muestra el año de modelo; las fuentes secundarias consultadas describen la gama como 2026 | [Autoblog](https://www.autoblog.com/cars/tesla/cybertruck/2026), [Cars.com](https://www.cars.com/research/tesla-cybertruck-2026/) | R |

Motivo de la elección: el Cyberbeast es la versión de mayor equipamiento disponible, comparte carrocería, cotas y
suspensión neumática con el Premium AWD (según el manual) y añade el tren motriz tri-motor, más interesante
para la vista explosionada. **No se han mezclado especificaciones de otras versiones**: las cotas de altura y
altura libre utilizadas son las del bloque «Premium All-Wheel Drive and Cyberbeast» del manual.

## 2. Fuentes principales

| Fuente | Uso |
|---|---|
| [Manual del propietario — Dimensions, Weights, and Cargo Capacity](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-12A976DD-EB60-431B-AFF1-5A37E95006DB.html) | Cotas exteriores, alturas de suspensión, caja de carga, cotas interiores, masas |
| [Manual del propietario — Wheel and Tire Specifications](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7.html) | Llantas 20 x 9.0J ET58.5, neumático 285/65R20, par de apriete |
| [Manual del propietario — Subsystems](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html) | Motores, relación de transmisión, dirección, frenos, suspensión, baterías |
| [Manual del propietario — Exterior](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-E051122B-2E44-444A-9E48-4F180882D05D.html) | Distribución de elementos exteriores (barra de luz, cámaras, botones de puerta, toma de carga) |
| [Manual de servicio de Cybertruck](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html) | Despiece y denominación de piezas (fascia, faros, tonneau por lamas, subchasis tri-motor, módulos de muelle neumático, actuadores de dirección delantero y trasero, cámaras, interruptores de pilar B y C) |
| [Manual de servicio — Headlamp Assembly](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AA106AB5-27B0-48B1-86CA-A64E9D18F205.html) | Ubicación del faro (sobre la fascia, accesible desde el frunk) |
| Análisis de desmontaje de Munro & Associates ([batería](https://electrek.co/2024/04/09/tesla-cybertruck-teardown-battery-pack-is-half-empty-confused/), [módulo trasero Cyberbeast](https://leandesign.com/tesla-cyberbeast-motor-teardown-review/)) | Disposición en una sola capa de celdas 4680 organizadas en módulos; unidad trasera con dos motores |
| [InsideEVs — pasaporte de batería](https://insideevs.com/news/724981/tesla-cybertruck-battery-passport-4680cell/) | 1.344 celdas 4680, 123 kWh |
| Foro Cybertruck Owners Club ([sustitución de faro](https://www.cybertruckownersclub.com/forum/threads/headlight-replacement-now-that-i-finally-got-it-diy-install-process-after-hitting-deer.38840/), [toma de carga](https://driveteslacanada.ca/?p=41592)) | Confirmación complementaria de ubicaciones (fuente secundaria) |

Las imágenes de Tesla y de terceros se consultaron como referencia **sin copiarlas al repositorio**. Solo se
conservan datos derivados (perfiles medidos) en `blender/reference_data/official_side_profile.json`.

## 3. Método de medición sobre las vistas oficiales

El manual del propietario incluye una ilustración con **vista lateral y vista superior ortográficas** del vehículo
de producción (PNG con fondo transparente, 760 x 538 px). Se extrajeron los contornos por canal alfa y las
transiciones de luminancia con un lienzo del navegador (sin descargar la imagen):

1. **Calibración horizontal:** ajuste por círculos de los dos neumáticos → centros en x = 115,0 px y 559,5 px.
   Con la batalla oficial (3.635 mm) se obtiene **8,178 mm/px**.
2. **Validación cruzada:** con esa escala, el voladizo trasero medido es 1.169 mm (oficial 1.169,6 mm) y la longitud
   total 5.667 mm (oficial 5.682,9 mm; diferencia atribuible al antialiasing del paragolpes).
3. **Calibración vertical:** se adopta la misma escala (píxeles cuadrados) y un desplazamiento de −21,7 mm para
   que la altura máxima coincida con la cota oficial en «Medium» (1.793,8 mm). Validación independiente: la cara
   inferior central medida queda a 0,260 m del suelo frente a la altura libre oficial de 0,257 m.
4. Los perfiles (superior, inferior, frontal, trasero y semianchura en planta) se simplificaron con
   Douglas-Peucker (3-4 mm) y las facetas se ajustaron por mínimos cuadrados.

Rasgos medidos de este modo (**R**): pendiente del capó 19,5°, escalón del limpiaparabrisas de ~3 cm, parabrisas
curvado de 18,8° a 15,9°, vértice redondeado (radio equivalente ~1,3 m), caída trasera 8,2-8,7°, línea de
cintura ascendente 3,5° hacia atrás, punta de la ventanilla delantera sobre el eje delantero, juntas de
puertas (Y = +1,188 / +0,080 / −0,918 m), pasos de rueda trapezoidales, pliegue lateral a 0,588 m, faldón entre
0,262 y 0,405 m, inclinación del portón y escalón del paragolpes trasero.

La **sección transversal** se dedujo combinando planta y alzado: cara lateral inclinada 6° hacia dentro e
invernadero (cristales laterales) inclinado 19°. Con estas dos reglas, la semianchura calculada de la arista del
techo coincide con la planta medida (0,722 m frente a 0,728 m en el vértice; 0,777 m frente a 0,80 m en el pilar C).

## 4. Ficha técnica utilizada

| Magnitud | Valor | Categoría |
|---|---|---|
| Longitud total | 5.682,9 mm | V |
| Anchura con espejos / plegados / sin espejos | 2.413,3 / 2.200,7 / 2.031,6 mm | V |
| Altura total (Cyberbeast) por altura de suspensión | 1.738,8 (entrada) · 1.753,8 (Low) · **1.793,8 (Medium, usada)** · 1.853,8 (High) · 1.893,8 (Very High) · 1.943,8 mm (Extract) | V |
| Batalla | 3.635,0 mm | V |
| Vía delantera y trasera (centro de rueda) | 1.772,0 mm | V |
| Voladizos delantero / trasero | 878,3 / 1.169,6 mm | V |
| Altura libre (Medium) | 257,0 mm | V |
| Caja de carga: longitud / anchura en el suelo | 1.824,6 / 1.295,4 mm | V |
| Caja de carga: altura máxima delante / detrás | 727,9 / 503,8 mm | V |
| Altura libre interior delantera / trasera | 1.058,8 / 991,9 mm | V |
| Espacio para piernas delantero / trasero | 1.043,6 / 1.038,8 mm | V |
| Anchura a la altura de hombros delantera / trasera | 1.608,0 / 1.576,4 mm | V |
| Llanta | 20 x 9.0J, ET58.5; tuercas de 21 mm a 205 N·m | V |
| Neumático | Pirelli Scorpion ATR 285/65R20 (Ø calculado 878,5 mm) | V |
| Frenos delanteros | Disco ventilado Ø351 x 32 mm, pinza fija de 4 pistones | V |
| Frenos traseros | Disco ventilado Ø356 x 23 mm, pinza flotante de 1 pistón, freno de estacionamiento eléctrico | V |
| Suspensión | Independiente de doble horquilla delante y detrás, muelle neumático, amortiguador adaptativo, barra estabilizadora | V |
| Dirección | Por cable en las 4 ruedas, 0,94 vueltas entre topes, diámetro de giro 13,25 m | V |
| Motores Cyberbeast | Delantero: síncrono de imanes permanentes; traseros: dos de inducción; relación 15,02:1 | V |
| Batería | Iones de litio refrigerada por líquido, ~700 V nominales; 1.344 celdas 4680, 123 kWh | V (manual) / V (pasaporte, fuente secundaria) |
| Baja tensión | 48 V, 4 Ah | V |
| Masa en orden de marcha (Cyberbeast All Season) | 3.113 kg | V (no modelada) |

## 5. Registro por conjuntos

### 5.1 Carrocería exterior
- **Verificado:** longitud, batalla, voladizos, altura en «Medium», vía, posiciones de los ejes.
- **Reconstruido:** todo el perfil lateral y la planta (medición sobre la vista oficial, §3); facetas frontales en
  planta (central, intermedia y esquina a ~34°); arista superior del frontal que asciende ~7 cm hacia las esquinas
  (la vista frontal oficial muestra que la barra de luz sube ~5,5 cm en los extremos); pasos de rueda y aletas;
  vela y escalón del pilar C; portón inclinado y más estrecho arriba (cara lateral inclinada 6°).
- **Aproximado:** espesores de chapa (2,5-3 mm), radios de biseles (1,5-2 mm), holgura entre paneles (3,5 mm),
  pliegues exactos de la fascia inferior, forma de los laterales del paragolpes trasero.
- **Discrepancia conocida:** la anchura «sin espejos» oficial (2.031,6 mm) es menor que la anchura física de los
  neumáticos (vía 1.772 + 285 = 2.057 mm). La planta oficial muestra las aletas a ~±1,04 m, que es lo que
  reproduce el modelo (2.081,7 mm). Se interpreta que la cota oficial no incluye aletas ni flancos.
- **Mejoraría la fidelidad:** fotogrametría o escaneo 3D del vehículo real; planos de reparación de carrocería
  con cotas de puntos de control (manual de reparación de carrocería, acceso parcial).

### 5.2 Puertas, portones y cristales
- **Verificado:** existencia y denominación de piezas (puertas con cristal móvil, sellos, tonneau por lamas,
  portón trasero, frunk motorizado —denominado «Powergate» en el manual de servicio—) según el manual de servicio.
- **Reconstruido:** contornos de puertas y cristales, pilar B negro, punta delantera del cristal, frunk con
  bisagra trasera, portón con bisagras inferiores, 22 lamas de la cubierta.
- **Aproximado:** estructura interior de las puertas (prisma de chapa interior), bisagras, mecanismos del tonneau,
  tintado exacto de los cristales.

### 5.3 Iluminación
- **Verificado:** barra de luz delantera, faros, pilotos laterales de carrocería, luces de marcha atrás, de
  matrícula y catadióptricos existen como piezas separadas (manual de servicio).
- **Reconstruido:** barra de luz delantera a lo ancho (~86 % de la anchura) siguiendo la arista del frontal; barra
  trasera roja en la parte superior del portón con continuación en las esquinas.
- **Aproximado:** los faros se modelan como módulos con proyectores alojados tras los extremos de la barra de luz:
  el procedimiento de servicio indica que se extraen desde el frunk, por encima de la fascia, pero no se ha
  verificado su forma exterior. Posición exacta de luces de marcha atrás y catadióptricos.

### 5.4 Ruedas, neumáticos y frenos
- **Verificado:** dimensiones de llanta, neumático, discos y tipo de pinzas.
- **Reconstruido:** tapacubos «Core» de 6 palas planas facetadas (fotografías del configurador); disco desplazado
  hacia dentro respecto al plano de montaje (ET58.5).
- **Aproximado:** dibujo de la banda de rodadura (patrón todoterreno genérico, no el del Scorpion ATR), sin
  inscripciones en el flanco; patrón de 6 tuercas a 135 mm; forma de las pinzas y del motor del freno eléctrico.

### 5.5 Habitáculo
- **Verificado:** pantallas de 18,5" y 9,4", cinco plazas, consola central con cargadores inalámbricos,
  salida de aire continua («Airwave»), retrovisor interior, parasoles con cortinilla, cotas interiores.
- **Reconstruido:** puntos H (delantero 0,30/0,80 m y trasero −0,63/0,77 m en Y/Z, respaldo trasero a 15°; en la v4.1 se adelantó 7 cm para que la banqueta no
  atravesara la pared trasera) derivados de la altura libre
  (criterio SAE con 102 mm) y del techo del modelo; salpicadero plano; volante «squircle» de 360 x 300 mm.
- **Aproximado:** formas de asientos, consola, paneles de puerta y guarnecidos; cinturones representados recogidos.
- **Mejoraría la fidelidad:** fotografías ortogonales del habitáculo o datos de la guía de rescate.

### 5.6 Chasis, bajos, suspensión y dirección
- **Verificado:** arquitectura (doble horquilla delante y detrás, muelle neumático coaxial con amortiguador,
  estabilizadoras con bieletas, actuadores de dirección delantero y trasero, subchasis delantero y trasero,
  deflectores y placas de protección).
- **Aproximado:** geometría de brazos, portamanguetas, piezas fundidas, subchasis y puntos de anclaje. Se han
  situado de forma coherente con la vía, el centro de rueda y la altura libre, pero no proceden de planos.

### 5.7 Propulsión y alta tensión
- **Verificado:** número y tipo de motores del Cyberbeast (manual), relación 15,02:1, 1.344 celdas 4680.
- **Reconstruido:** unidad delantera en el eje delantero con inversor superior; unidad trasera con dos motores y
  engranajes independientes; batería de una sola capa organizada en módulos.
- **Aproximado:** envolvente de la batería (2,70 x 1,60 x 0,17 m), cuatro módulos de 336 celdas, vigas internas,
  barras colectoras, recorridos de cables de alta tensión y tubos de refrigerante. **No se han inventado
  bobinados ni electrónica interna.**
- **Discrepancia de fuentes:** algunos análisis atribuyen al Cyberbeast un motor delantero de imanes permanentes y
  otros uno de inducción; se sigue el manual del propietario (delantero de imanes permanentes, traseros de
  inducción). La tabla de suspensión del manual intercambia las etiquetas «coil» y «air»; se adopta la
  suspensión neumática, coherente con el resto del manual y con el configurador.

## 6. Resultados de validación (geometría evaluada en Blender)

Datos completos en [`validation-results.json`](validation-results.json).

| Cota | Modelo | Oficial | Desviación |
|---|---|---|---|
| Longitud | 5.684,9 mm | 5.682,9 mm | +2,0 mm |
| Altura («Medium», incl. 2,2 mm de aplastamiento del neumático) | 1.796,7 mm | 1.793,8 mm | +2,9 mm |
| Batalla | 3.635,0 mm | 3.635,0 mm | 0 |
| Vía | 1.772,0 mm | 1.772,0 mm | 0 |
| Voladizo delantero / trasero | 880,5 / 1.169,4 mm | 878,3 / 1.169,6 mm | +2,2 / −0,2 mm |
| Altura libre | 256,6 mm | 257,0 mm | −0,4 mm |
| Diámetro del neumático | 878,4 mm | 878,5 mm | −0,1 mm |
| Anchura con espejos (retrovisores v2) | 2.413,3 mm | 2.413,3 mm | 0,0 mm |
| Anchura sin espejos (sobre aletas) | 2.081,7 mm | 2.031,6 mm | +50,1 mm (ver §5.1) |

Comparación de siluetas por trazado de rayos frente a los perfiles medidos en la vista oficial
(excluidas las muestras de los extremos geométricos):

| Perfil | Muestras | Error medio | P95 | Máximo |
|---|---|---|---|---|
| Superior | 125 | 2,9 mm | 7,2 mm | 13,3 mm (v2: 10,2) |
| Semianchura en planta | 49 | 6,7 mm | 19,2 mm | 29,3 mm |
| Trasero | 22 | 9,2 mm (v2: 9,8) | 21,0 mm | 65,1 mm |
| Inferior | 31 | 12,5 mm | 40,3 mm | 121,1 mm |
| Frontal | 34 | 16,0 mm | 51,3 mm | 151,3 mm |

Las cotas y siluetas anteriores se revalidaron tras la versión 3 (948 objetos): las dimensiones oficiales no
cambian y los perfiles quedan dentro de ±0,6 mm de media (ver §9).

Los máximos del perfil inferior y frontal corresponden al labio inferior de la fascia delantera, que se ha
elevado deliberadamente a 0,266 m para respetar la altura libre oficial (el diagrama muestra 0,252 m).

## 7. Limitaciones y trabajo futuro

1. La sección transversal depende de dos inclinaciones deducidas (6° y 19°); una vista frontal ortográfica a
   escala o un escaneo permitiría verificarlas directamente.
2. Mecánica, batería, piezas fundidas e interior se han detallado (v2) con la denominación, el número de
   fijaciones y las cotas de control de los manuales, pero sus **formas** siguen siendo reconstrucciones: no
   existen planos CAD públicos.
3. El dibujo del neumático reproduce la arquitectura de un «all-terrain» de 5 hileras, no el molde exacto del
   Pirelli Scorpion ATR; las inscripciones usan una tipografía genérica.
4. Los interiores de faros, motores, inversores y electrónica son representativos (carcasas, disipadores,
   conectores), sin bobinados ni placas reales.
5. Las texturas son sintéticas (ruido filtrado), físicamente plausibles pero no medidas sobre muestras reales.

## 8. Investigación de la versión 2 (16-10-2026)

### 8.1 Nuevas fuentes consultadas

| Fuente | Contenido aprovechado | Categoría |
|---|---|---|
| [Manual de servicio — índice](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html) (980 procedimientos) | Inventario de piezas reales: fascias, soporte frontal, persianas activas, absorbedores de impacto, bisagras, cierres, presentadores, tirantes, burletes primario y secundario, juntas de cintura, frunk «Powergate», portón (barra de torsión, cierres con acercamiento, amortiguador, correas), cubierta (raíles «horizon», motores, casete plano, eslabones), subchasis tri-motor, brazos, módulos de muelle neumático, compresor, depósito y bloque de válvulas, actuadores de dirección, HCU, servofreno electromecánico, unidades motrices, inversores, intercambiadores, bahía auxiliar (ACJB, PCS, clúster de dispositivos, barra «last mile»), pirofusibles, Supermanifold/Octovalve, CFM, Megabeam, mazos de cables, asientos, salpicadero, consola, guarnecidos y altavoces | V (existencia y denominación) |
| Manual de servicio — procedimientos individuales (≈120 leídos) | Número, tipo y par de las fijaciones (p. ej. retrovisor 3 × T40 a 18 N·m; faro 2 tornillos; módulo de muelle 3 tuercas a 105 N·m + 2 tornillos a 140 N·m; brazo superior 4 tuercas a 50 N·m; brazo inferior trasero 4 tornillos a 185 N·m; pinza delantera 2 × 24 mm a 315 N·m; trasera 2 × 21 mm a 150 N·m; buje 4 × 105 N·m; actuador trasero 4 × 120 N·m; tapacubos 8 grapas; deflector delantero 11 tornillos; difusor 14 tornillos; panel de puerta 14 grapas + 3 tornillos; burlete secundario 26 grapas) | V |
| [Manual de servicio — Wheel Alignment](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4.html) y fichas «Brakes», «Wheels», «Paint Codes» | Alineación (caída −0,50° / −1,00°, avance 3,60°), vía 1.777 / 1.772 mm, altura de chasis 265 mm (Medium), pastillas 10 / 11 mm, límites de disco 30 / 21 mm, llanta y tapacubos «Stealth Black» NEU-208E | V |
| [Manual de reparación de carrocería](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html) | Materiales (aluminio 6xxx, extruido y fundido; aceros dulce, HSS, UHSS e inoxidable), uniones (adhesivo estructural, soldadura por puntos, remaches flow-form Ø 8 mm), refinado del inoxidable por planos con abrasivo no tejido, piezas fundidas delantera y trasera (la trasera sustituible por mitades), «Mast Assembly» y torres del portón fundidos, y **cotas de control**: largueros delanteros 1.025 mm, torretas 930 / 938 mm y 1.577 mm exteriores, largueros traseros 1.050 mm, base de pilares B 1.549 mm, pared trasera 1.463 / 1.406 mm | V |
| [Manual del propietario — Wheel and Tire Specifications](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7.html) | Pirelli Scorpion ATR como neumático de serie y Goodyear Wrangler Territory RT LT285/65R20 como opción «all-terrain» | V |
| [The Autopian — desmontaje de la batería (Munro)](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/) | 4 bloques de 7 × 48 celdas (≈1.344), «cell-to-pack», espuma estructural verde, lámina de mica, refrigerador en serpentín, canal de desgasificación de ~33 mm, respiradero de un solo uso, puertos de inundación, modo «Scuba» | R (fuente secundaria) |
| [The Autopian — motores (Munro)](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/) | Delantero de imanes permanentes con inversor integrado al final de la reductora y bloqueo electromagnético; traseros de inducción idénticos con su inversor en la parte posterior | R |
| [The Autopian — cuna trasera (Munro)](https://theautopian.com/latest-cybertruck-teardown-reveals-teslas-odd-sway-bar-decisions-clever-packaging) | Dos refrigeradores de placa sobre los motores, reductoras desplazadas hacia atrás, brazo inferior trasero soldado, brazos superiores a la pieza fundida, estabilizadora con abrazaderas de banda | R |
| [Munro — prospecto del informe 2024](https://leandesign.com/wp-content/uploads/2024/11/Munro-2024-Cybertruck-Report-Prospectus-Oct-2024.pdf), [Basenor — 48 V y steer-by-wire](https://www.basenor.com/blogs/news/cybertrucks-engineering-firsts-48v-steer-by-wire-explained) | 48 V con anillo Ethernet redundante, dirección por cable con dos motores en la cremallera, frenado por cable | R |
| [InsideEVs — Giga Press de 9.000 t](https://insideevs.com/news/589457/elon-musk-confirms-tesla-cybertruck-massive-giga-press/) | Fundición de gran formato para la parte trasera | R |

Las imágenes de los manuales se consultaron únicamente como referencia temporal y **no se han copiado al
repositorio**.

### 8.2 Fabricación y ensamblaje (síntesis aplicada al modelo)

- **Exoesqueleto de acero inoxidable**: chapa gruesa laminada en frío, plegada en líneas rectas (no embutida),
  sin pintura, con acabado satinado direccional; los arañazos se reparan refinando planos completos. En el
  modelo: facetas planas con biseles de 1,5-2 mm y tres variantes del material por panel.
- **Carrocería en blanco mixta**: piezas fundidas de aluminio en los extremos, anillos de puertas y umbrales de
  acero de ultra alta resistencia con insertos de aluminio extruido, adhesivo estructural y remaches flow-form.
- **Batería estructural**: celdas 4680 «cell-to-pack» en una bandeja que forma el suelo; los asientos
  delanteros se atornillan a la tapa; brida perimetral atornillada a los umbrales.
- **48 V y Ethernet**: mazos más finos y controladores zonales (izquierdo, derecho y trasero).
- **Dirección por cable**: actuador de realimentación en el volante y actuadores delantero y trasero.

### 8.3 Fidelidad de los conjuntos añadidos en la versión 2

| Conjunto | Verificado | Reconstruido | Aproximado |
|---|---|---|---|
| Estructura | Existencia, materiales, uniones y cotas de control | Piezas fundidas, umbrales, anillos de puerta, «mast», torres | Nervaduras, bosses, espesores |
| Suspensión y dirección | Arquitectura, fijaciones y pares, alineación | Puntos duros, brazos, portamanguetas, muelles | Secciones y radios |
| Tren motriz | Tipo de motores, inversores, intercambiadores, bombas | Disposición de carcasas y refrigeradores | Formas exteriores, aletas |
| Batería | 1.344 celdas, 4 × 7 × 48, espuma, mica, serpentín, pirofusibles, respiradero | Bandeja, tapa, vigas, bahía auxiliar | Barras colectoras, conductos |
| Exterior | Piezas y fijaciones (faro, retrovisor, bisagras, cierres, juntas, tonneau, portón, difusor) | Retrovisor, faros, soportes, raíles, lamas | Interiores de faros y mecanismos |
| Ruedas | Medidas, fijaciones, grapas del tapacubos, pastillas | Tapacubos Core, arquitectura del dibujo | Inscripciones del flanco |
| Interior | Piezas, botoneras, altavoces, cinturones, airbags, RCM | Consola, paneles, guarnecidos | Trazado de las costuras |

### 8.4 Materiales y texturas

Las texturas se generan en `blender/scripts/ct_textures.py` filtrando ruido blanco en el dominio de la
frecuencia (periódicas por construcción) y se guardan en WebP en `blender/textures/`. Densidad de texel:
UV de 1 unidad = 1 m y una repetición por material (acero 0,40 m → 0,39 mm/px; caucho 0,08 m; plástico
granulado 0,05 m; piel 0,08 m; tejido 0,012 m; fundición 0,20 m). El mapa de rugosidad codifica la
metalicidad en el canal B (convención glTF), de modo que Blender y el visor usan los mismos datos.

## 9. Versión 3 (17-10-2026): piezas del backlog y correcciones

### 9.1 Método

1. La investigación de la versión 3 se consolidó en [`ficha-tecnica-piezas.md`](ficha-tecnica-piezas.md): nombres
   oficiales, cantidades, fijaciones y pares del manual de servicio, del manual de reparación de carrocería, del
   manual del propietario y de la hoja de rescate, con 30 conflictos de fuentes señalados.
2. Cada pieza nueva se programó con `ct_v3.py` en los módulos `build_v3_*.py`, dentro del hueco que dejaba la
   geometría de la versión 2. Las piezas simétricas se generan reflejando las **coordenadas** de entrada (no la
   malla), de modo que las normales quedan hacia fuera.
3. Se revalidó con `validate.run()` (cotas oficiales y siluetas por trazado de rayos) y con
   `build_explode.verify_roundtrip()`; los desajustes que introdujeron piezas nuevas (altura libre, perfil frontal,
   trasero y de planta) se corrigieron recolocando esas piezas, no relajando la validación.

### 9.2 Resultado y fidelidad

- 387 objetos nuevos (948 en total). Etiquetado: «Verificado» solo para nombre, cantidad y fijaciones en el
  manual (`ct_parts.make` los clasifica «Reconstruido» porque la forma es reconstruida); las antenas, puntos BLE,
  tomas de 48 V y mazos son «Aproximado» (existencia en el manual de servicio, posición no publicada).
- Sin cota ni masa por pieza: las fuentes públicas no las publican (el mapa de materiales y las cotas de control del
  manual de reparación son imágenes). Los espesores y materiales nuevos son interpretaciones razonadas.
- No se modelaron las opciones fuera de serie (Terrestrial Armor, barra de luz off-road), las piezas propias de las
  variantes Long Range/Dual Motor ni las «secciones de reparación» (Section, Half Section), que no son piezas del
  vehículo.

### 9.3 Fallos corregidos

| Fallo | Corrección |
|---|---|
| 51 mallas cerradas con las normales hacia dentro (cajas de `ct_lib.box`, llantas, protectores de disco, portavasos, pantallas, asientos…) | `ct_lib.box` orienta las caras hacia fuera y `ct_lib.orient_closed_components` (usada por `mesh_object` y por las mallas de ruedas) propaga un sentido coherente y invierte las componentes de volumen negativo; las láminas abiertas no se tocan |
| Mallas cerradas con sentido mixto de caras (carriles de la cubierta) | La misma función las deja coherentes |
| Par del tirante de puerta 35 N·m (el manual indica un perno T40 a 23 N·m) | Etiqueta corregida |
| Bisagras «25/38 N·m» (25 N·m es la barra de torsión izquierda del portón) | 2 fijaciones por bisagra a 38 N·m |
| Controlador trasero de 48 V con «4 tuercas» | 3 fijaciones: 2 tuercas de 13 N·m + 1 perno de 10 N·m; controladores delanteros: 4 tuercas de 10 mm a 14 N·m |
| Bandeja de la batería con «44 tornillos» | Recuento aproximado y variable según la página del manual |
| Persianas activas «7 lamas», barra de luz «64 LED», 22 lamas del tonneau | Se declara que el número no consta en las fuentes (Aproximado) |
| Escobilla «~1,26 m» | Se declara el conflicto de fuentes: 62 in, ~50 in o ~1,22 m |
| Batería «~800 V» | 700 V nominales (manual del propietario); 800 V según la hoja de rescate |
| Pantallas de 18,5" y 9,4" etiquetadas «Verificado» | «Reconstruido»: el tamaño solo consta en fuentes secundarias |

Pendiente: 7 láminas abiertas (faldillas de aleta, paragolpes delantero, puerta de la toma de carga, piloto
lateral) conservan 3–16 aristas con caras de sentido discontinuo; no afectan a las cotas ni a la explosión.

## 10. Versión 4 (17-10-2026): «coche completo» por dentro e hiperrealismo

### 10.1 Objetivo y criterio

El objetivo acordado con el usuario es que el modelo contenga **todas las piezas que necesita un vehículo
para funcionar**, sin simplificar, aunque muchas no puedan copiarse del Cybertruck real. Hasta la versión 3 los
conjuntos grandes (motores, reductoras, inversores, pinzas, actuadores, climatizador, asientos…) eran
carcasas cerradas. La versión 4 añade lo que hay dentro y la tornillería que los une.

Criterio de fidelidad aplicado (sin cambios respecto al proyecto):

- **Existencia y función:** [V] cuando la pieza consta en el manual de servicio, el manual del propietario o la
  hoja de rescate (p. ej. motor de imanes permanentes delante e inducción detrás, 4 pistones delante y 1 detrás,
  dos motores redundantes en los actuadores de dirección, PCS, ACJB, emblema de Cerbero); [R] cuando procede de
  los desmontajes de Munro; imprescindible por ingeniería en el resto (rodamientos, juntas homocinéticas,
  bomba de freno, armazón de los asientos…).
- **Forma, dimensiones y recuentos interiores** (dientes, ranuras, bolas, celdas de la batería de 48 V,
  componentes de las placas): reconstrucciones de ingeniería. Las 189 piezas nuevas se etiquetan
  **«Aproximado»** con la nota correspondiente; ninguna se presenta como dato de Tesla.
- La relación global 15,02:1 [V] **no** se reproduce con los radios de los engranajes dibujados: están limitados
  por la carcasa reconstruida de la reductora. El número de celdas de la batería de 48 V (13 en serie) es una
  estimación a partir de la tensión nominal.
- La posición de cada tornillo de los juegos de tornillería es reconstruida; la cantidad, la llave y el par
  proceden del manual de servicio (`docs/ficha-tecnica-piezas.md`).

### 10.2 Qué se añadió (189 objetos, 1.137 en total)

| Sistema | Piezas nuevas |
|---|---|
| Unidad motriz delantera | Estátor de chapa magnética de 48 ranuras con devanado de horquillas, barras de fase, rotor de imanes en V con placas de equilibrado, imanes de NdFeB, eje hueco estriado, rodamientos, resolver, piñón de entrada, eje intermedio, bloqueo electromagnético, diferencial abierto (corona, caja, satélites y planetarios), ejes de salida y retenes, tornillos de la tapa; inversor: placa fría, módulos de potencia de SiC, condensador del bus de continua, placas de excitación y de control, sensores de corriente |
| Unidad motriz trasera (por lado) | Estátor de 60 ranuras con devanado distribuido, rotor de jaula de ardilla de cobre, eje con rodamientos y resolver, reductora independiente de dos etapas sin diferencial, interior del inversor |
| Semiejes y bujes | Juntas homocinéticas de trípode y Rzeppa de 6 bolas, abrazaderas de los fuelles, tornillo central de 24 mm, rodamientos de buje de doble hilera |
| Frenos | Interior de las 4 pinzas (pistones, juntas, guardapolvos, pasadores, muelle antirruido, husillo del freno de estacionamiento), láminas antirruido y avisador de desgaste, interior del servofreno electromecánico, bomba de freno tándem con sus pistones, varilla de empuje, interior de la HCU |
| Suspensión y dirección | Interior de los 4 amortiguadores, cremallera con tuerca de bolas, poleas y correas, motores redundantes y placa de los dos actuadores, interior del compresor de aire |
| Batería y alta tensión | Placas BMB y circuitos flexibles de los 4 bloques, barras principales, controlador BMS, junta de la tapa, colectores de refrigerante, interior del PCS y de la ACJB |
| Baja tensión y electrónica | Interior de la batería de 48 V, placas de los controladores de carrocería, del ordenador de a bordo, de la ECU de remolque y de 29 módulos cerrados (cámaras, controladores de puerta, airbags, telemática, radar, sintonizador, sensores de impacto…), mazo principal del salpicadero |
| Térmica y climatización | Hélices y motores de los ventiladores, compresor de A/C de espiral, rodete de la bomba de refrigerante, interior del climatizador (soplante, evaporador, condensador interior, compuertas, desagüe), interior del motor del limpiaparabrisas |
| Habitáculo | Armazones, muelles, herrajes de reclinado y esteras de los asientos delanteros, armazón del banco trasero, espumas de los 10 cojines y respaldos, alma de magnesio del volante, radios, muelle de reloj y tornillo central, enrolladores con pretensor, interior de las pantallas, altavoces de puerta, bobinas de carga inalámbrica |
| Carrocería y exterior | Vigas antiintrusión y guías del cristal de las 4 puertas, interior de los faros, motores de la cubierta, actuador de la toma de carga, tomas de remolque de 7 y 4 polos, emblema Cyberbeast |
| Tornillería | 21 juegos de tornillos individuales (aletas, faros, retrovisores, lavaparabrisas, limpiaparabrisas, frunk, raíles de la cubierta, suelo de la caja, luces traseras, fascias, difusor, barra de luz, soportes de las unidades motrices) |

Las carcasas de motores, reductoras, inversores y actuadores se apartan ahora más que su contenido en la vista
explosionada (despiece de taller), y los tapizados de los asientos se separan de sus espumas.

### 10.3 Hiperrealismo

- **Texturas nuevas** (`ct_textures.py`): placa de circuito impreso (máscara, pistas de cobre rectas y a 45°,
  pads estañados con metalicidad propia, vías y serigrafía), espuma de poliuretano de celda abierta, fieltro no
  tejido, marcas de mecanizado y rectificado, recubrimiento de zinc de la tornillería.
- **Materiales nuevos** (78 en total): chapa magnética, cobre esmaltado, imanes niquelados, acero de rodamientos y
  de engranajes, espuma, fieltro, condensadores de película, sustrato cerámico, interfaz térmica, estañado,
  nailon, grasa, acero de muelles fosfatado, armazón de asiento y magnesio inyectado.
- Se probó añadir huellas y velos de manipulación al acero inoxidable y **se descartó**: con una textura que se
  repite cada 40 cm el patrón se veía en mosaico. Unas huellas creíbles exigen mapas únicos por panel.
- **Límite honesto:** la forma exacta de faros, retrovisores, paragolpes, fundiciones y del dibujo del Scorpion
  ATR sigue sin poder mejorarse con rigor: hacen falta escaneos, planos o fotografías ortogonales a escala.

### 10.4 Validación

| Comprobación | Resultado |
|---|---|
| Cotas oficiales | Sin cambios respecto a la v3 (longitud +2,0 mm, altura +2,9 mm, altura libre −0,4 mm, batalla, vía y anchura con espejos exactas) |
| Siluetas por trazado de rayos | Sin cambios (superior 2,9 / 13,3 mm; inferior 13,3 / 121,1; frontal 16,0 / 151,3; trasero 9,2 / 65,1; planta 6,7 / 29,3) |
| Vista explosionada | Desviación 0 tras ciclos repetidos en los 1.137 objetos |
| Piezas que asomaban | Detectadas con renders y rayos verticales contra la tapa del frunk (tornillos de la cubeta del frunk, de la fascia trasera, de los raíles y del limpiaparabrisas) y recolocadas |
| Peso del activo | 1,19 millones de triángulos; GLB 12,0 MB (Draco + WebP); `Cybertruck.blend` 14,7 MB |

### 10.5 Qué sigue faltando

- Piezas internas no modeladas por falta total de referencia o porque no son piezas separables: estructura
  interna del neumático (talones, lonas, cinturones), interior de las celdas, bobinados reales, placas con
  componentes reales, mazos completos con cada conector, todos los clips de los guarnecidos.
- Tornillería: hay juegos individuales en las uniones del manual que no la tenían; muchas uniones siguen con los
  tornillos integrados en la malla de su pieza.
- Formas exactas de las piezas visibles (ver §10.3).

## 11. Versión 4.1 (17-10-2026): interferencias de ensamblaje

### 11.1 Problema

Tras publicar la v4, el usuario detectó decenas o cientos de **errores de ensamblaje**: piezas mal posicionadas que
se atraviesan entre sí, por fuera, por dentro y en los asientos. La causa es que cada constructor coloca sus piezas
con cotas propias (muchas reconstruidas) sin comprobar lo que ya ocupa ese espacio.

### 11.2 Detector (`blender/scripts/interferencias.py`)

- Para cada pareja de mallas cuyas cajas se solapan se cruzan sus árboles BVH (geometría evaluada, coordenadas de
  mundo, explosión a cero) y se calculan los segmentos de corte entre triángulos.
- **Superficie visible:** muchas piezas se modelan como varios sólidos cerrados solapados (lóbulos, nervios, tapas).
  Las caras de un sólido que quedan dentro de otro sólido del mismo objeto no se ven nunca y no cuentan
  (`_visible`). Esto eliminó falsos positivos como el tren de engranajes dentro de los lóbulos de su carcasa.
- **Profundidad:** penetración máxima de los vértices de una pieza dentro de la otra (paridad de rayos y punto más
  cercano), medida solo cerca de la zona de cruce.
- **Penetraciones intencionadas** (`INTENDED`), que no se cuentan porque en la realidad pasan por un taladro, una
  guía o un pasamuros:
  - tornillos, remaches, grapas, espárragos y tuercas (hasta 15 mm);
  - celdas en su espuma;
  - ejes que atraviesan la carcasa por su retén;
  - varillas de los reposacabezas;
  - portavasos en la consola;
  - válvula del neumático;
  - espárragos y centrador del buje en el disco y la llanta;
  - extremo de la viga del salpicadero en su soporte;
  - eje del rotor en el piñón;
  - mazos que cruzan mamparos y suelo (hasta 15 mm);
  - barras y cables que entran en el cabezal HV;
  - colectores de la batería por las vigas;
  - filtro roscado en la reductora;
  - casquillos de los soportes del motor (hasta 12 mm).

### 11.3 Estrategias de corrección

1. **Recolocación en los constructores**: la corrección principal, en el código fuente y con sus conexiones.
   - Pila de rueda coherente: brida del buje, campana del disco y cara de apoyo de la llanta en ET 58,5. Disco
     central de la llanta hacia fuera, radios por fuera de la pinza, tuercas sobre la nueva cara y tapacubos dentro
     de la pestaña.
   - Bahía de alta tensión trasera dentro de las paredes de los pasos de rueda. Inversores traseros detrás del
     motor. Cables y arneses que terminan en las caras de conexión, no dentro de las cajas.
   - Vano delantero:
     - batería de 48 V contra el cortafuegos;
     - HCU, Octovalve, bomba, enfriador, condensador y botella fuera del larguero de la fundición y del frunk;
     - mangueras con recorridos libres.
   - Viga del salpicadero sobre la columna de dirección y extremos por delante del larguero del guardabarros.
     Controladores de carrocería fuera de las tapas laterales y del soplador. Mazo principal sobre la viga.
   - Suspensión neumática:
     - conductos que salen de racores reales;
     - haces bajo el umbral y por dentro de la rueda trasera;
     - controlador trasero entre la pared de la cabina y la caja.
   - Alfombrillas con el contorno real del hueco de los pies. Filtro HEPA junto al soplador. Volante y cubierta de
     la columna coherentes. Placas electrónicas dentro de la carcasa principal de cada módulo.
2. **Interiores en sus carcasas** (`build_v4.fit_internals`):
   - Ajuste anisótropo en los ejes de la carcasa (desplazamiento si chocan por un solo lado, reducción del eje que
     choca, con un límite del 60 %).
   - Si no basta, recorte booleano con el volumen interior de la carcasa (`ct_v4.clip_inside`).
   - Las espumas se fuerzan a quedar dentro de su tapizado (`ct_v4.keep_inside`).
3. **Pasada de montaje** (`build_montaje.py`, parte `"montaje"` de `build_all.run`), para las piezas que en la
   realidad llevan el alojamiento de lo que se monta en ellas:
   - **Recortes**: anillos de puerta, moqueta, guarnecido central, espumas acústicas, tablero, tapas laterales del
     salpicadero, consola, guarnecidos de puerta y de pilares, escudos de freno, laterales y remates de la caja,
     soportes del «mast», consola de techo y raíles de la persiana. Las láminas se engruesan antes; los cortadores
     se unen y se amplían 0,6 mm; se usa el solver `MANIFOLD`. Cada recorte se acepta solo si reduce el cruce.
   - **Compresión** de las juntas de goma, que se deforman contra lo que las comprime.
   - **Recolocación automática** (`resolver`, `placer`): solo para módulos ocultos, con tope de 15–30 mm. Se probó
     y se dejó desactivada para la publicación porque movía piezas visibles. La tabla
     `montaje_desplazamientos.json` queda vacía.

### 11.4 Lecciones

- El solver booleano `EXACT` con mallas grandes o abiertas (juntas, anillos de puerta) **cierra Blender**. En los
  recortes se usa `MANIFOLD`, y el exacto solo como respaldo con mallas cerradas de menos de 4.000 caras. El recorte
  de interiores sí lo usa, porque ahí ha sido estable.
- `MANIFOLD` exige sólidos cerrados sin autointersecciones. Las partes solapadas de un cortador se unen antes
  (`_union_islands`) y las láminas se engruesan (`_solidify_sheet`).
- Recortar láminas abiertas sin engrosarlas destroza la malla (se vio en las alfombrillas). Las alfombrillas se
  corrigieron con su contorno, no con recortes.
- La reconstrucción completa con la pasada de montaje tarda unos 5 minutos. Las llamadas MCP cortan a los ~100 s,
  así que conviene lanzarla en un temporizador de Blender y leer el resultado de un fichero.

### 11.5 Resultado y validación

| Comprobación | Resultado |
|---|---|
| Parejas que se atraviesan > 3 mm (sin las intencionadas) | ~1.110 al empezar → **279** |
| Parejas > 10 mm | ~300 → **53** |
| Parejas > 30 mm | ~33 → **1** |
| Penetraciones intencionadas reconocidas | 230 parejas (tornillería, pasamuros, guías…) |
| Cotas oficiales | Sin cambios (altura libre −0,4 mm; batalla, vía y anchura con espejos exactas) |
| Siluetas | Sin empeorar; perfil trasero ligeramente mejor (media 8,7 mm) |
| Vista explosionada | Desviación 0 en los 1.139 objetos |
| Activo web | GLB de 12,5 MB, 1.138 componentes; `Cybertruck.blend` de 16,5 MB |

### 11.6 Qué falta (pendiente)

La lista completa, pareja por pareja y con su posición, está en `docs/interferencias-pendientes.md`. Por zonas:

- **Chasis (58):**
  - escudos de freno contra la mangueta, la pinza y la rótula (el recorte no siempre se acepta);
  - motor EPB y brazos;
  - fuelles de los amortiguadores neumáticos frente a los asientos de los topes;
  - haces de aire frente al bloque de válvulas y al inversor;
  - soportes de la unidad trasera frente al actuador de dirección.
- **Habitáculo (48):**
  - viga del salpicadero frente a la tapa lateral derecha y al mazo principal;
  - interiores del volante;
  - conductos de desempañado frente al «super cowl»;
  - módulos de airbag frente a los paneles inferiores;
  - consola de techo, antenas y sensores;
  - mazos de puerta junto a los guarnecidos.
- **Carrocería y estructura (48):**
  - fundición delantera frente al refuerzo del puente y a los soportes de la viga;
  - altavoz del peatón frente a la viga del paragolpes;
  - toma de carga frente a su ECU;
  - soportes de esquina y de fascia;
  - pilares C frente a guarnecidos.
- **Caja de carga (45):**
  - esquinas traseras (cierres del portón, remates, torres, soportes);
  - «mast» frente a los laterales y al aplique del sail;
  - lamas de la persiana frente a los carros;
  - suelo de la caja sobre la rueda trasera (el hueco del paso de rueda queda 8 mm corto).
- **Alta y baja tensión (27):**
  - mazo troncal frente a los controladores y mazos de la caja;
  - cabezal HV y BMS;
  - cubiertas de bloqueo;
  - mazos que rozan módulos.
- **Unidades motrices (25):** interiores de inversores y reductoras que aún asoman unos milímetros por su carcasa,
  y soportes.
- **Gestión térmica (20):**
  - líneas de A/C frente al compresor y al Supermanifold;
  - mangueras del enfriador y de la unidad delantera frente al conector del canal del salpicadero.
- **Asientos (8):**
  - cinturones traseros frente a los guarnecidos del pilar C;
  - restos de espuma frente al tapizado.

La forma de abordarlas está en `traspaso.md` §14.
