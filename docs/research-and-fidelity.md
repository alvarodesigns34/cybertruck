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
  portón «Powergate», frunk motorizado) según el manual de servicio.
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
- **Reconstruido:** puntos H (delantero 0,30/0,80 m y trasero −0,70/0,77 m en Y/Z) derivados de la altura libre
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
| Anchura con espejos | 2.411,1 mm | 2.413,3 mm | −2,2 mm |
| Anchura sin espejos (sobre aletas) | 2.081,7 mm | 2.031,6 mm | +50,1 mm (ver §5.1) |

Comparación de siluetas por trazado de rayos frente a los perfiles medidos en la vista oficial
(excluidas las muestras de los extremos geométricos):

| Perfil | Muestras | Error medio | P95 | Máximo |
|---|---|---|---|---|
| Superior | 125 | 2,9 mm | 6,8 mm | 10,2 mm |
| Semianchura en planta | 49 | 6,7 mm | 19,2 mm | 28,6 mm |
| Trasero | 22 | 9,8 mm | 21,9 mm | 65,1 mm |
| Inferior | 31 | 12,8 mm | 40,3 mm | 121,1 mm |
| Frontal | 34 | 16,2 mm | 51,3 mm | 151,3 mm |

Los máximos del perfil inferior y frontal corresponden al labio inferior de la fascia delantera, que se ha
elevado deliberadamente a 0,266 m para respetar la altura libre oficial (el diagrama muestra 0,252 m).

## 7. Limitaciones y trabajo futuro

1. La sección transversal depende de dos inclinaciones deducidas (6° y 19°); una vista frontal ortográfica a
   escala o un escaneo permitiría verificarlas directamente.
2. El interior, la mecánica y la batería son reconstrucciones plausibles, no geometría OEM.
3. Dibujo del neumático e inscripciones del flanco sin verificar.
4. No se han modelado elementos internos de faros, motores ni electrónica.
5. Los materiales procedurales de Blender se reinterpretan en el visor web (no existe equivalencia exacta en glTF).
