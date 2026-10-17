# Cybertruck (2024-2026, foco Cyberbeast): cotas oficiales y huecos de chasis, estructura e interior (ronda 2)

Fecha de la investigación: 2026-10-17. Etiquetas: **[V]** Verified (texto primario de Tesla leído directamente), **[R]** Reported (fuente secundaria o no verificable en Tesla), **[I]** Inferred (deducción mía). Variantes: **[CB]** Cyberbeast / Tri-Motor, **[AWD]** Premium AWD / Dual Motor, **[LR]** Long Range, **[Todas]**.

## Cómo conseguir las fuentes primarias (resultado del desbloqueo de 403)

### Takeaway
tesla.com devuelve 403 a WebFetch y a curl (probados: manual HTML, /cybertruck, /firstresponders, /support), pero el **espejo tesla.cn sirve el Owner's Manual completo** (HTML por GUID y PDF de 16 MB, "Software version 2026.20, North America") y service.tesla.com sirve Service Manual y Collision Repair en HTML estático con curl.

### Cited Findings
- [V] Manual completo PDF (17.178 líneas de texto, extraído con pdftotext), Software 2026.20, North America — [Owners_Manual.pdf en tesla.cn](https://www.tesla.cn/ownersmanual/cybertruck/en_us/Owners_Manual.pdf). Existe también la misma ruta en tesla.com, pero da 403 desde mi entorno.
- [V] Páginas por GUID leídas vía tesla.cn: Dimensions, Weights, and Cargo Capacity (GUID-12A976DD...), Wheel and Tire Specifications (GUID-9284C9F2...) y Subsystems (GUID-32CD64C8...) — p. ej. [Dimensiones](https://www.tesla.cn/ownersmanual/cybertruck/en_us/GUID-12A976DD-EB60-431B-AFF1-5A37E95006DB.html). Pie de página © 2026.
- [V] Service Manual accesible con curl y User-Agent de navegador: índice (1.079 enlaces) en [Fluid Capacities](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-136927CC-901C-4C28-987F-1074223AC781.html). WebFetch resume mal estas páginas (solo ve la navegación); hay que extraer el bloque `<h1 class="title topictitle1">`.
- [V] Collision Repair: [índice](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html), © Tesla 2026; 99 páginas descargadas (componentes, guías y listas de piezas).
- [V] Rescue Sheet oficial (1 PDF de 4 páginas): [Cybertruck-Rescue-Sheet.pdf](https://digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf), ID TESLA-2023CA-001, versión 02 (metadatos PDF: creado 2023-07-14, modificado 2023-11-09). Tesla lo publica como "Rescue Sheet", no "Emergency Response Guide"; listado en [tesla.com/firstresponders/vehicles-charging](https://www.tesla.com/firstresponders/vehicles-charging) (solo vía resultado de búsqueda, la página da 403).

### Inferences
- [I] Para futuras rondas, usar tesla.cn con la ruta /ownersmanual/cybertruck/en_us/ y el PDF; no se probaron es_es, de_de ni en_gb porque el en_us de tesla.cn ya cubre todo.

### Gaps
- tesla.com/cybertruck, la página de diseño y la de specs devuelven 403; tesla.cn/cybertruck responde 200 pero es una SPA sin texto (59 caracteres tras quitar scripts). No hay fuente primaria de Tesla para tamaños de pantalla, número de altavoces ni color "Tactical Grey".

## 1. Dimensiones, pesos, capacidades (Owner's Manual, "Dimensions, Weights, and Cargo Capacity")

### Takeaway
El manual da cotas exteriores al centésimo de pulgada, altura y distancia al suelo por cada ajuste de suspensión, volúmenes de carga y tabla completa de pesos por variante. **No publica ángulos de ataque, ventral ni salida** (solo dice que Extract/Very High los aumentan).

### Cited Findings
Fuente de todo este bloque: [Dimensions, Weights, and Cargo Capacity (tesla.cn, en_us, © 2026)](https://www.tesla.cn/ownersmanual/cybertruck/en_us/GUID-12A976DD-EB60-431B-AFF1-5A37E95006DB.html), confirmado con el PDF del manual (pág. 237 y ss.). Todos [V].

Exteriores [Todas salvo indicación]:
- Longitud 223,74 in / 5.682,9 mm; ancho con retrovisores 95,01 in / 2.413,3 mm; retrovisores plegados 86,64 in / 2.200,7 mm; sin retrovisores 79,98 in / 2.031,6 mm.
- Batalla 143,11 in / 3.635,0 mm; voladizo delantero 34,58 in / 878,3 mm; trasero 46,05 in / 1.169,6 mm.
- Vía delantera y trasera 69,76 in / 1.772,0 mm (ver conflicto abajo con el Service Manual).
- Altura [CB/AWD] por ajuste: Entry 68,46 in / 1.738,8 mm; Low 69,05 / 1.753,8; Medium 70,62 / 1.793,8; High 72,98 / 1.853,8; Very High 74,56 / 1.893,8; Extract 76,53 in / 1.943,8 mm. [LR] 18" All Season: 70,07 in / 1.779,8 mm.
- Distancia al suelo [CB/AWD]: Entry 7,95 in / 202 mm; Low 8,54 / 217; Medium 10,12 / 257; High 12,48 / 317; Very High 14,05 / 357; Extract 16,02 in / 407 mm. [LR] 9,57 in / 243 mm.
- Caja [CB/AWD]: altura máx. delante 28,66 in / 727,9 mm, detrás 19,84 in / 503,8 mm; ancho en suelo 51,00 in / 1.295,4 mm; largo en suelo 71,84 in / 1.824,6 mm. [LR]: 29,92 / 759,9 y 20,81 / 528,6 (mismo ancho y largo).
- Habitáculo (delante / detrás): altura libre 41,69 / 39,05 in (1.058,8 / 991,9 mm); espacio piernas 41,09 / 40,90 in (1.043,6 / 1.038,8 mm); hombros 63,31 / 62,06 in (1.608,0 / 1.576,4 mm); caderas 57,22 / 57,22 in (1.453,3 / 1.453,5 mm).

Alturas de suspensión respecto a Medium (Owner's Manual PDF, sección Suspension, pág. 94) [V]: High +2,4 in (6 cm); Low -1,6 in (4 cm); Entry -2,2 in (5,5 cm); Very High +3,9 in (10 cm); Extract +5,9 in (15 cm). Extract limita la velocidad a 10 mph (16 km/h); Very High a 25 mph (40 km/h). Modo Wade: profundidad máxima aproximada 32 in (815 mm) medida desde la parte inferior del neumático, máx. 30 min, ride height Very High, batería HV presurizada (pág. 105-106) [V].

Pesos [V] (lb / kg), columnas Cyberbeast AS (neumático all-season) / AT (all-terrain); AWD = Premium AWD:
- Peso en vacío total: [CB] 6.863 / 3.113 (AS) y 6.898 / 3.129 (AT); [AWD] 6.634 / 3.009 (AS) y 6.669 / 3.025 (AT); [LR] 6.118 / 2.775.
- Eje delantero/trasero en vacío: [CB AS] 3.336 / 1.513 y 3.527 / 1.600; [CB AT] 3.353 / 1.521 y 3.545 / 1.608.
- Carga útil: [CB] 2.000 lb / 907 kg (AS), 2.270 / 1.030 (AT); [AWD] 2.200 / 998 (AS), 2.500 / 1.134 (AT); [LR] 2.006 / 910.
- GVWR total: [CB AS] 8.863 / 4.020; [CB AT] 9.169 / 4.159; [AWD AS] 8.834 / 4.007; [AWD AT] 9.169 / 4.159; [LR] 8.199 / 3.719.
- GVWR por eje [CB AS]: delante 4.019 / 1.823, detrás 4.844 / 2.197; [CB AT]: 4.160 / 1.887 y 5.009 / 2.272.
- GAWR [CB]: delantero 4.255 / 1.930; trasero 5.009 / 2.272 (AS) o 5.247 / 2.380 (AT).
- Remolque máximo: [CB/AWD] 11.000 lb / 4.990 kg; [LR] 7.500 / 3.402. Tongue weight máx.: 1.100 lb / 499 kg (20" x 9J) y 750 lb / 340 kg en LR (manual PDF, pág. 112, "Towing a Trailer").
- Límites de carga: frunk 441 lb / 200 kg; compartimento bajo la caja [CB/AWD] 220 lb / 100 kg; baca 220 lb / 100 kg por juego de 2 travesaños (en cabina y/o en caja).
- Volúmenes [CB/AWD] (ft³ / L): frunk 7,1 / 200; caja cerrada sobre el piso 56,1 / 1.589; compartimento inferior 3,4 / 97; cabina detrás de asientos delanteros 54,1 / 1.533; total con cinco pasajeros 66,6 / 1.885; con dos 120,7 / 3.418. [LR]: caja 58,1 / 1.646, cabina 54,4 / 1.540, total 65,2 / 1.845 y 119,6 / 3.385 (sin compartimento inferior).
- Service Manual, tabla de peso máximo en vacío (incluye opciones más pesadas y todos los fluidos) [V]: Tri Motor 6.918 lb / 3.137 kg; Dual Motor 6.669 lb / 3.025 kg; GVWR ambas 9.169 lb / 4.158 kg — [Vehicle Weight Information and Lifting Precautions](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B8B4D7C3-E26D-46B2-B09A-E1B6BC0BBBCF.html). Elevadores de 2 postes: se exige 10.000 lb (4.535 kg) para vehículos modificados.
- Alineación (Service Manual, actualizado 2026-08-19) [V]: ancho de vía a la altura del centro de rueda delante 1.777 mm, detrás 1.772 mm; batalla 3.635 mm; altura de chasis Medium (suspensión neumática) 265 ± 5 mm sin Terrestrial Armor y 250 ± 5 mm con ella; en muelles helicoidales, 18": 264/262 mm (del./tras.) y 20": 274/272 mm sin Terrestrial Armor (249/247 y 259/257 con ella). Camber delantero -0,50° ± 0,45°, trasero -1,00° ± 1,00°; caster 3,60° ± 1,00°; toe individual delantero Out 0,05°, trasero In 0,20° — [Wheel Alignment](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4.html).

Conflictos:
- Vía: el Owner's Manual da 1.772 mm delante y detrás; el Service Manual da 1.777 mm delante y 1.772 mm detrás. Diferencia de 5 mm; probablemente medidas en puntos distintos [I].
- Distancia al suelo Medium 257 mm (Owner's Manual) frente a "altura de chasis" 265 mm (Service Manual): son magnitudes distintas (la segunda es una cota de referencia de alineación) [I].
- Tensión nominal HV: Owner's Manual 700 V DC nominal; Rescue Sheet muestra "800V Li-Ion" en la leyenda de energía almacenada ([ver sección 5](#5-emergency-response--rescue-sheet-componentes-y-ubicaciones)).

### Inferences
- [I] La altura de techo Medium de 1.793,8 mm menos la distancia al suelo 257 mm da 1.536,8 mm de altura de carrocería sobre el suelo en Medium; usable como referencia de modelado.
- [I] Delta Extract-Medium en altura (1.943,8 - 1.793,8 = 150 mm) coincide con los +5,9 in de la tabla de suspensión; los datos son internamente coherentes.

### Gaps
- Ángulos de ataque, ventral y de salida: no figuran en el manual (verificado por búsqueda de "approach", "departure", "breakover" en las 17.178 líneas). Una web de terceros cita 35° y 28° pero no es verificable [R] (resultado de búsqueda de basenor.com, sin contrastar con Tesla).
- Cotas de sección del habitáculo más allá de las cuatro anteriores, radio de giro por eje, y anchura de puertas: no publicadas en el manual.

## 2. Ruedas, neumáticos, presiones y subsistemas (Wheel and Tire, Subsystems)

### Takeaway
El manual y el Service Manual dan llantas 20x9.0J ET58.5 (y 18x9.0J), 6 tuercas de 21 mm a 205 Nm, tres medidas de neumático, presiones de 50 psi (65 psi AT con carga máxima o remolque), dirección steer-by-wire de 0,94 vueltas tope a tope y diámetro de giro 13,25 m.

### Cited Findings
- [V] Llantas de fábrica: 20 x 9.0J ET58.5 (todas las variantes) y 18 x 9.0J ET58.5; par de tuercas 151 lb·ft (205 Nm), llave de 21 mm — [Wheel and Tire Specifications](https://www.tesla.cn/ownersmanual/cybertruck/en_us/GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7.html) y [Wheels (Service Manual)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-69690B5B-7C41-40FD-A6D3-FC17B5FBDB66.html).
- [V] Neumáticos de fábrica (manual PDF, pág. 217): 285/65R20 all season (Hard Metric); LT285/65R20 Pirelli Scorpion ATR all terrain (Light Truck); 285/70R18 Goodyear Wrangler Territory RT/HT all season. Presiones recomendadas en la etiqueta del pilar central; el manual no imprime el número en la sección de especificaciones.
- [V] Presiones (manual PDF, pág. 211 y Towing): carga normal 50 psi en 20" AS, 20" AT y 18" AS; con carga hasta GVWR, 20" AT sube a 65 psi (los otros se quedan en 50 psi). Remolcando: 18" AS 50 psi, 20" AS 50 psi, 20" AT 65 psi (reemplazan a la etiqueta). Pérdida de aprox. 1 psi por cada 10 °F (6 °C) de descenso. Cadenas solo en neumáticos traseros. Sistema TPMS se reinicia tras 10 min a más de 15 mph (25 km/h).
- [V] Motores: [CB] delantero 1 motor síncrono de imanes permanentes, trasero 2 motores de inducción, todos refrigerados por líquido; [AWD] delantero 1 inducción, trasero 1 imanes permanentes; [LR] trasero 1 imanes permanentes. Relación de transmisión global 15,02:1, marcha única; marcha atrás limitada a 15 mph (24 km/h) — [Subsystems](https://www.tesla.cn/ownersmanual/cybertruck/en_us/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html).
- [V] Dirección: "4-wheel directional steer-by-wire", 0,94 vueltas tope a tope (340°), diámetro de giro bordillo a bordillo aprox. 43,5 ft (13,25 m). Rear Steer configurable Off/Auto en la app Off-Road ("tighter turn radius") — mismas fuentes.
- [V] Frenos: ABS de 4 ruedas con EBD, pinzas delanteras de 4 pistones fijas y traseras de 1 pistón flotantes; discos ventilados delantero 13,8 in (351 mm) y trasero 14 in (356 mm); espesor disco delantero nuevo 32 mm / límite 30 mm, trasero nuevo 23 mm / límite 21 mm; pastillas delanteras nuevas 10 mm / límite 3 mm, traseras 11 mm / límite 2 mm; descentrado lateral 0,050 mm, circular 0,040 mm, variación de espesor 0,010 mm; freno de estacionamiento eléctrico en pinza — [Brakes (Service Manual)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-1D03EF6F-5DD6-4539-A664-9C784492A8E2.html).
- [V] Suspensión: independiente, doble horquilla delante y detrás, muelle neumático coaxial, barra estabilizadora (Service Manual, [Suspension](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A7180897-7F9B-48B2-869D-525BB3DAF07F.html)). Límites de casquillos: rechazo si pérdida de rigidez >= 20 %.
- [V] Batería de baja tensión 48 V, 4 Ah. Batería HV de iones de litio refrigerada por líquido, 700 V DC nominal; no exponer a más de 65 °C (149 °F) o menos de -30 °C (-22 °F) durante más de 24 h (manual PDF, pág. 243-244).
- [V] Fluidos y capacidades — [Fluid Capacities](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-136927CC-901C-4C28-987F-1074223AC781.html) y [Fluids](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A86EE40B-CA89-494E-A084-B855E34AC574.html): líquido de frenos DOT 4 BASF Hydraulan 404 (1190 mL llenado desde seco); aceite de reductor KAF1 / KAF1 (V1.2), llenado hasta rebosar; refrigerante HTF-LS naranja 50/50 (G-48 azul en producción temprana), 23,5 L Tri-Motor y 22,5 L Dual Motor; refrigerante A/C R1234yf 1.020 g; aceite POE RB100EV 250 g. Revisión de líquido de frenos cada 4 años (manual PDF, Maintenance).
- [V] Air suspension: reservorio a aprox. 16 bar (Service Manual, [SCUBA Valve Block](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-707B2753-C49B-40E9-92D8-BE90EA4FE140.html), nota del paso de presurización).
- [V] Enchufes: 120 V a 20 A máx. en consola y bajo la pantalla trasera; en la caja 2 x 120 V y 1 x 240 V (manual PDF, Interior Electronics y Cargo Bed).

### Inferences
- [I] Los tres neumáticos citados cubren la selección de modelado: AT 285/65R20 con diámetro aprox. 0,285*0,65*2 + 20*0,0254 = 0,878 m (cálculo mío, no es dato Tesla).
- [I] El Owner's Manual PDF rotula "Vehicles with Coil Spring Suspension" con "air spring" y "Adaptive Air" con "coil spring" en las tablas de suspensión (títulos invertidos, error aparente de maquetación). El Service Manual, que sí añade una tabla de alineación para "Coil Suspension" (2026-08-19), confirma que existen versiones con muelle helicoidal; probablemente [LR] aunque el texto no lo dice.

### Gaps
- Ángulo máximo de las ruedas traseras y ángulo físico de steer: no publicados (solo "Rear Steer Off/Auto" y la cifra de giro tope a tope 340° del volante). Se encontró un procedimiento de par para el actuador trasero pero no el recorrido.
- El Service Manual de Tire Pressures solo remite a la etiqueta del pilar B (no da psi).

## 3. Chasis: subchasis trasero, cuna del motor trasero, estabilizadoras, tirantes, aire (Service Manual)

### Takeaway
El Service Manual está accesible y da pares de apriete concretos para subchasis delantero/trasero, brazos, tirantes de convergencia, barras estabilizadoras y todo el sistema de aire (compresor, depósito, bloque de válvulas). Los procedimientos del subchasis trasero Tri-Motor (Cyberbeast) están completos.

### Cited Findings
Todos [V]; fecha de lectura 2026-10-17. Pares en Nm (lb·ft cuando el manual los da). [CB] = procedimiento Tri Motor.

Subchasis trasero [CB] — [Subframe - Rear (Tri Motor) (Remove and Replace)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A4F3E974-4AB0-4101-989A-21DDF99202FB.html) (tiempo oficial 3,84 h; procedimiento marcado DRAFT):
- Subchasis a carrocería: 4 pernos de 24 mm a 355 Nm (261,8 lb·ft); 3 clavijas (dowels) de posicionado; se baja con elevador de tren motriz.
- Motor trasero (RDU) al subchasis: 4 tuercas de 18 mm a 85 Nm y 2 tuercas de 21 mm a 115 Nm.
- Brazos de control (conjunto brazo + semieje + mangueta): 4 pernos de 21 mm a 185 Nm por lado.
- Barra estabilizadora trasera con bieletas: 6 pernos de 15 mm a 50 Nm; soportes del arnés HV del RDU: 4 pernos de 10 mm a 12 Nm; cinta de masa 1 perno de 10 mm a 10 Nm.
- Actuador de dirección trasera (RSA) con tirantes: 4 pernos de 18 mm a 120 Nm.
- Escudos: aero escudo central 3 pernos de 15 mm a 42 Nm, 5 de 13 mm a 28 Nm, 2 de 10 mm a 6 Nm; escudo aero trasero 5 pernos de 10 mm a 6 Nm; difusor trasero 6 pernos de 10 mm y 8 T30 a 6 Nm; ménsulas del difusor 6 pernos de 13 mm a 30 Nm.
- Rueda: 6 tuercas de 21 mm a 205 Nm; pinza trasera 2 pernos de 21 mm a 150 Nm; tubo de freno al brazo superior 1 perno de 10 mm a 10 Nm.
- Seguridad: tras desconectar el conector HV del RDU hay que medir con pinza amperimétrica (si la corriente es mayor de 0,5 A no se desconecta); la puerta de enlace (gateway) se desbloquea 90 minutos.
- Variante Dual Motor: [Subframe - Rear (Dual Motor)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-39E00821-017A-482A-AA05-1FC7B003275C.html). Subchasis trasero Dual y Tri comparten los mismos pernos de carrocería (355 Nm según "Inspect Underbody Fastener Torque").

Brazos y enlaces traseros:
- Brazo inferior trasero: 4 pernos de 21 mm a 185 Nm (136,4 lb·ft), reutilizables — [Control Arm - Lower - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A86B108E-9A2B-42B8-AD4D-832C2FCE07B5.html).
- Brazo superior trasero: tuerca a mangueta 150 Nm (reemplazar); pernos al vehículo 350 Nm (27 mm); tirante a actuador 180 Nm; actuador a subchasis 4 pernos 120 Nm — [Control Arm - Upper - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-9BDBAF7A-BB1F-4C85-846C-EA41A4458A17.html).
- Toe link trasero: a mangueta 170 Nm (tuerca nyloc nueva, 21 mm); a actuador 180 Nm (18 mm) — [Toe Link - Rear - LH](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5FDE24EE-24CE-4721-8C77-2E23AF3EDBE1.html).
- Barra estabilizadora trasera: 4 pernos de 15 mm a 50 Nm (36,9 lb·ft); orientación con extremos por encima de los soportes (nota de 2024-11-12) — [Stabilizer Bar - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-6FDF63DE-13D1-4FCC-9F64-6206AC233A9D.html).
- Módulo de muelle neumático trasero: 3 tuercas al vehículo 70 Nm (18 mm), 2 tuercas al brazo inferior 140 Nm (21 mm, de un solo uso) — [Module - Air Spring - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-BAACC9E3-8DFB-462B-9BBC-23C87ED3AB47.html).

Delantero [AWD/CB/LR]:
- Subchasis delantero (AWD) — [Subframe - Front (AWD)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-794CE60D-61DE-4B22-A99B-6DB0A31A8590.html) (actualizado 2024-10-16): travesaño delantero 2 pernos de 18 mm a 90 Nm; soportes del motor delantero (FDU gearcase) 2 pernos de 18 mm a 110 Nm; brazo inferior al subchasis 2 pernos de 21 mm a 175 Nm y 1 de 24 mm a 300 Nm (nuevos); brazo inferior a mangueta tuerca 24 mm a 190 Nm (nueva); bieleta estabilizadora a brazo inferior 275 Nm; bieleta de dirección (tie rod) a mangueta 170 Nm; módulo neumático 2 pernos a 140 Nm; escudo del brazo 3 pernos a 7 Nm.
- Estructura delantera al vehículo ("Inspect Underbody Fastener Torque", [página](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-F37882B9-9E45-4F3C-9452-7BF9DDC0FC81.html)): 2 pernos de 24 mm a 220 Nm; 4 tuercas de 24 mm a 215 Nm; 4 pernos de 21 mm a 220 Nm; batería HV: 16 pernos de 15 mm a 62 Nm y 6 pernos de 18 mm a 115 Nm; estructura trasera 4 pernos de 24 mm a 355 Nm; skid plate 50 Nm.
- Ganchos de recuperación delanteros (recovery hooks): 4 pernos de 15 mm a 78 Nm, nuevos en cada montaje — [Recovery Hook - Pair](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-753930B8-ADC1-4C5C-89E8-34BEA21AA9AE.html).

Sistema de aire (Air Suspension, sección 3110; "TAS"):
- Compresor — [Compressor - Air Suspension](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-51C72CFF-62A1-4F17-8180-4129F9E573C9.html) (actualizado 2026-10-05): ubicado bajo el piso de la caja (se retira "bed floor assembly"); soporte al cuerpo 3 tuercas de 13 mm a 12 Nm; soporte al compresor 3 tornillos T30 a 5,5 Nm; línea de aire 3 Nm; escape del compresor se retira al sustituir el compresor. Tiempo 0,84 h.
- Depósito — [Reservoir - Air Suspension](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-620A7266-D2F1-4118-B379-1BBE57869216.html): 2 tuercas de 13 mm a 33 Nm; 4 líneas de aire con racores VOSS (3 Nm; 7 Nm con 14 mm, 5 Nm con 10 mm); bloque de válvulas del "pressurized pack" fijado con 1 perno de 10 mm a 5 Nm.
- Bloque de válvulas — [Valve Block](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5F6BC136-4578-417B-B24A-638E63353871.html): 5 líneas de aire, 3 gomas de sujeción, se manipula desde la caja bajo el piso. Bloque SCUBA/pack presurizado: racores VOSS a 8 Nm.
- Depósito y válvulas viven bajo el piso de la caja (acceso retirando "Bed Floor Assembly") [V]; la ubicación exacta (lateral) no está en el texto [I].

Dirección trasera:
- Actuador de dirección trasera (RSA) en subchasis: 4 pernos de 18 mm a 120 Nm (2 por lado); tirante 180 Nm — [Steering Actuator - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-C75A9806-3F4E-4D6B-9466-72F15106C035.html) y [Steering Gear - Rear (Standard)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-2C9F1065-2896-42D6-BDAD-E3BCB65E81A6.html). Hay variante "Rear Steer (Long Range)" con arnés distinto, lo que implica que LR también lleva dirección trasera [I].

Ganchos y enganche:
- Enganche trasero (tow hitch): 6 pernos de 18 mm al casting trasero a 198 Nm (146,0 lb·ft, nuevos) según [Tow Hitch](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-BD1223F7-BA44-4CD9-852C-7CABC4382CB2.html) (2024-09-16), frente a 178 Nm según [Rear Energy Absorber - Cast Bumper](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-450C3E03-BCC1-4AFC-8996-C47D23FFEDF4.html); 4 pernos superiores de 15 mm a 44 Nm; 2 de 13 mm a 16 Nm. **Conflicto interno de Tesla** (198 frente a 178 Nm).
- Parachoques trasero fundido (cast bumper) por lado: 2 pernos de 18 mm a 90 Nm.
- Parachoques delantero ("Front Energy Absorber - Front Bumper Beam Assembly"): 4 tuercas de 13 mm a 30 Nm — [página](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-3F3AB49B-DFD2-4F7F-A969-64AA4141EE5C.html).
- Megabeam: 8 pernos al vehículo (EP14 a 18 Nm y 21 mm a 165 Nm; el texto no desglosa cuántos de cada tipo); supermanifold a Megabeam 2 pernos de 15 mm a 33 Nm — [Front Inner Panels - Megabeam](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5C533F8C-3E30-4EE2-9794-21D406893407.html).
- Skid plate delantera (undertray): 8 pernos de 10 mm y 4 clips a 4 Nm, 8 pestañas — [Skid Plate](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B0F7244F-0D90-4781-A7C4-C4279FC261D9.html). Skid plate trasera / aeroescudo: 3 pernos de 15 mm a 70 Nm, 3 de 13 mm a 28 Nm, 2 de 10 mm a 6 Nm, 8 pernos y 6 clips en total — [Skid Plate - Rear](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-855C1F35-5C9B-45C9-8268-94AC3AA811DF.html). Escudo aero delantero: 11 pernos de 10 mm a 6 Nm (con Loctite 222).
- Cuñas del frunk: 6 pernos de 10 mm a 12 Nm.

### Inferences
- [I] El subchasis trasero Tri-Motor es un bastidor atornillado (4 pernos M-grande a 355 Nm, 3 dowels) que lleva dos motores de inducción más RSA, barra estabilizadora y brazos; la "cuna del motor trasero" es ese mismo subchasis (no hay otra cuna).
- [I] Si el modelo 3D incluye pernos, los diámetros de llave (24/21/18/15/13/10 mm) sugieren tamaños M16/M14/M12/M10/M8/M6 pero el manual no da la métrica de cada perno; solo para los de Collision Repair (M8, M10, M12) está documentada.

### Gaps
- No se leyeron los procedimientos de subchasis trasero Dual Motor "Remove and Replace" (GUID-AEB42835) en detalle, ni el cableado HV; los pares clave coinciden con Tri-Motor según la comprobación de torques del subchasis.
- Presiones de trabajo del sistema de aire distintas de ~16 bar del depósito: no encontradas. Volumen del depósito: no publicado.
- Ubicación exacta del compresor/depósito/válvulas respecto a ejes: el texto solo indica "bajo el piso de la caja".

## 4. Estructura de carrocería: materiales, secciones y piezas (Collision Repair Manual)

### Takeaway
El texto de la Collision Repair no asigna material pieza por pieza (el mapa de materiales y las dimensiones son imágenes); sí da la tabla de materiales y límites de reparación, las listas de piezas con remaches/pernos y pares por componente, y criterios de reparación de las piezas fundidas (Front/Rear Under Body, Mast, Tailgate Tower).

### Cited Findings
Todos [V] salvo indicación; fuente base [Collision Repair index (© Tesla 2026)](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html).

Materiales y operaciones permitidas — [Body Structure Materials and Allowed Operations](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B4A61C9E-4CE2-4D9A-B9B3-B6D74EEFE038.html):
- Siete materiales: aluminio 6xxx, aluminio extruido, aluminio fundido, acero suave, acero de alta resistencia (HSS), acero de ultra alta resistencia (UHSS) y acero inoxidable.
- Aluminio 6xxx: límite elástico 230-280 MPa; temperatura máxima 100 °C (212 °F); reparación por soldadura GMA de desgarros de hasta 75 mm; agujeros en paneles de cierre (puertas, capó, portón) hasta 12 mm y en Body Side Outer hasta 8 mm; sin paneles por debajo; soldadura solo en paneles de 1,2 mm o menos.
- Acero suave: resistencia a tracción menor de 270 MPa; calor máx. 650 °C (1200 °F), 90 s, 2 veces. HSS: 300-700 MPa; mismas reglas de calor. UHSS: mayor de 800 MPa; broca de carburo de tungsteno o boro; reparación solo si lo permite la guía de cada pieza. Acero inoxidable: no se permite soldar; solo refinado por lijado.
- No calentar un panel adhesivado por encima de 100 °C (212 °F); paneles con sensores de choque no se reparan; si la unión adhesiva de fábrica se daña se sustituye el panel.
- Tesla no admite tirar ni empujar de componentes con bancadas de estirado — [Structural Repair Guidelines](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C73E4B36-F7F0-4CA0-87F4-705A45D7D788.html).

Seccionado — [Sectioning Guidelines](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-50A9DAFE-D84D-48C6-810C-AE3B7BB95D05.html): no cortar a menos de 25 mm del centro de un agujero de perno; no cortar paneles subyacentes; las uniones a tope solo se sueldan por GMA si el procedimiento lo indica, nunca en bridas (solo adhesivo estructural).

Piezas fundidas — guías de reparación:
- Front Under Body (fundido): zonas azules (pestañas) se sueldan; verdes: soldadura de daños hasta 50 mm; amarillas: hasta 30 mm sin refuerzo, 30-50 mm con placa de refuerzo P/N 1076938-E0-B, más de 50 mm consultar a Tesla; rayones o gubias menores de 5 mm se pueden lijar; nervios doblados se enderezan en frío y deben quedar a 1,5 mm de la posición original — [Cast Front Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C1914222-086E-4604-809F-1ECB9A0F6F53.html).
- Rear Under Body (fundido): zonas azul, rosa, cian, verde, etc., con los mismos umbrales 30/50 mm y placa 1076938-E0-B — [Cast Rear Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-A839FDF1-F60E-44E5-ADFB-5B7A220C945C.html). Mast Assembly (fundido) y Tailgate Tower: mismos umbrales (la torre admite grietas de hasta 30 mm con placa) — [Mast](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-112E876E-DB80-4614-8B4E-F6F54AA9C4F8.html), [Tailgate Tower](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-9CD66714-3A98-49BC-B31C-06938B4D6DA6.html).
- Paneles exteriores de acero inoxidable: refinado con lijadora orbital de 6", órbita 3/16 in; se refina todo el plano (zona plana) afectado y el mismo plano en todos los paneles del lateral — [Stainless Steel Refinishing](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-D33D78C9-9BCD-46CB-885C-52B4F482852C.html).
- Rescue Sheet: paneles exteriores de acero inoxidable; estructura interior de pilares A, B y C en UHSS; larguero superior delantero de acero de alta resistencia (ver sección 5).

Listas de piezas (cantidades de remaches por componente; HS = remache estructural de alta resistencia 6,5 mm; FF = remache flow form):
- Front Under Body completo: 30 HS, 4 FF S18, 8 pernos M12x35, 10 pernos M12x43, 2 pernos M10x33, 2 tapones P/N 1870761-00; pares 67 y 90 Nm.
- Front Under Body (sección pequeña): 4 plantillas de línea de corte (P/N 2031072-00 ext. izq., 2031074-00 ext. der., 2031073-00 int. izq., 2031075-00 int. der.), 7 remaches de brida estructural, 2 pernos M10-1.5x41, 1 perno M8x28; pares 28 y 64 Nm.
- Dash Reinforcement: 61 HS, 4 FF S18, 2 M12x35, 10 M12x43. Front Body Bridge Reinforcement: 18 HS (izq.) o 20 (der.), 4 FF, 1 M12x35, 5 M12x43.
- Rear Under Body completo: 10 HS, 6 pernos M10x33, 4 tapones, par 90 Nm; sección: 13 HS, 4 de brida, 3 M10x33; Frame Rail Section: casting de riel trasero + placa trasera + 15 remaches de brida.
- Body Side Outer: 17 HS, 1 CSK corto, 2 CSK largos, 5 FF S18, FF S08/S28/S48/S58 (1 de cada), 4 pernos M12x35; par 90 Nm. Body Side completo: 46 HS, 6 FF S18, 4 M12x35, entre otros.
- Mast Assembly (fundido): 19 HS, 1 perno T2K 10x38 a 27 Nm; sección: 4 placas de refuerzo y 13 HS. Tailgate Tower: 7 HS. Rear Wall Assembly: 48 HS, 38 FF S18, 2 FF S28, 2 pernos T2K 10x38 a 37 Nm.
- Rear Seat Stanchion: 7 HS, 1 remache 4,8 mm; braces: 6 HS más 2 remaches de 4,8 mm. C-Pillar Inner: 33 HS, 2 pernos M10x33 (90 Nm). Side Sill Insert (extrusión): 4 remaches de 4,8 mm, 2 M10x33 (90 Nm), 2 M8x25 (26 Nm). Rocker Support Bracket: 4 por vehículo, 12 remaches de 4,8 mm cada uno. HV Battery Support Bracket: 22 HS.
- Front Drive Unit Mount (cada lado): 3 pernos M10x41 a 65 Nm. Fender Beam: 3 pernos M8x28 a 28 Nm. Bumper Beam Mount: 3 pernos M8x28 a 21 Nm. Front Quarter Window: 1 perno M12x35 a 70 Nm. Remache FF = flow form; ver [Using Flow Form Rivets](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-251653EC-9283-4E1C-B1BB-7C2E60A02EA5.html).
- Pestañas: ganchos de remolque delanteros cuadrados ("square tow hooks beneath the front fascia"), uno o ambos utilizables para el cabrestante; trasero: cabrestante a los recortes a cada lado del enganche (manual PDF, Instructions for Transporters, pág. 246-247).
- Dimensional Specifications: página con 5 figuras (laterales, pilar A-A y B-B, bajo capó, trasera, superior); todas las cotas son imágenes; texto solo indica que están en mm, centro a centro y simétricas salvo indicación — [Dimensional Specifications](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C5797770-FD0F-4A21-90C1-FC4E47976C95.html).

### Inferences
- [I] "Cast Front/Rear Under Body", "Mast" y casting del parachoques trasero son las piezas de aluminio fundido del Cybertruck (el manual enumera "cast aluminum" como material y estas piezas se llaman "cast"); la aleación concreta no figura.
- [I] El "Side Sill Insert" se describe como extrusión (nombre de pieza "SIDE SILL EXTRUSION"), consistente con aluminio extruido; el material no se indica en texto.
- [I] Los "crush cans" no aparecen con ese nombre; la función equivalente la cumplen el "Front Energy Absorber - Front Bumper Beam" (4 tuercas, 30 Nm) y el "Rear Energy Absorber - Cast Bumper" (2 pernos por lado, 90 Nm).

### Gaps
- Material por pieza: no hay tabla en texto (solo imagen). No se encontró la alusión a Megabeam como material; solo pares de montaje.
- Cotas de control (dimensional specifications): son imágenes; no se extrajo ninguna cota numérica de ahí. Haría falta visualizar las figuras (no intentado).
- No se leyó el detalle de cada guía de sección (cortes) por posición salvo Front Under Body pequeña (la distancia de corte depende de plantillas).

## 5. Emergency Response / Rescue Sheet: componentes y ubicaciones

### Takeaway
La guía oficial es una Rescue Sheet de 4 páginas, sobre todo pictogramas; el texto confirma corte doble del "first responder loop" bajo el capó (frunk), cable negativo de 48 V solo si es necesario, ubicación de pilares de UHSS y que el logo de la cabeza de Cerbero en la parte trasera derecha identifica el Tri-Motor.

### Cited Findings
Fuente: [Cybertruck Rescue Sheet](https://digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf), ID TESLA-2023CA-001, v02, "From 2023-Present", 4 puertas, 5 asientos. Todos [V]:
- "A Cerberus head emblem on the right rear of Cybertruck indicates a tri-motor performance vehicle"; el nombre del modelo no aparece en el exterior.
- Desactivación: abrir el capó (frunk), cortar dos veces el lazo de primera respuesta, cortar el cable negativo de la batería de 48 V solo si es necesario; no abrir la batería HV; no todos los componentes HV están etiquetados; cables HV con aislamiento naranja.
- Almacenamiento de energía: leyenda "48V Li-Ion" y "800V Li-Ion"; refrigerante azul o naranja. Elementos pictografiados: módulo SRS de airbag, inflador de gas almacenado, pretensor de cinturón, muelle de gas precargado, depósito de aire, batería de baja tensión, batería HV, cable HV, componentes HV, zona de cable de alta resistencia.
- Carrocería: paneles exteriores de acero inoxidable con estructura interior de acero de ultra alta resistencia; infraestructura de pilares A, B y C en UHSS; riel superior delantero de acero de alta resistencia; parabrisas, techo y vidrio móvil de las puertas son laminados; luneta trasera y ventanas delanteras de cuarto, templadas.
- Acceso: puertas con motor eléctrico, pueden no desbloquearse desde fuera tras una colisión; liberación mecánica interior (manual PDF pág. 257 y Rear door mechanical release).
- Incendio: no sumergir el vehículo; refrigerar la carcasa de la batería desde la parte inferior; vigilar la temperatura de la batería HV como mínimo 24 h; reignición posible; almacenar a 50 ft (15 m) de otros vehículos; sumergido: elevar el frente unos 30 cm (1 ft) para drenar. Remolque solo con plataforma.
- Contacto: firstrespondersafety@tesla.com.
- Airbags (Owner's Manual, pág. 48-49, [V]): hay airbags frontales de conductor y pasajero, de rodilla de conductor y pasajero, airbags montados en el asiento (laterales; el asiento del conductor tiene además uno en el lado interior que protege la cabeza y el torso) y airbags de cortina en ambos lados; sensor de ocupación del pasajero con indicador "Passenger Airbag OFF".

### Inferences
- [I] Cuenta mínima de airbags por categorías listadas: 2 frontales + 2 de rodilla + 2 de cortina + al menos 2 laterales de asiento = 8 como mínimo; el manual no da un total y no lo afirmo como dato.
- [I] La leyenda "800V" de la Rescue Sheet y los 700 V nominales del Owner's Manual no son necesariamente contradictorios (tensión de pack máxima frente a nominal), pero Tesla no lo explica. **Conflicto sin resolver.**

### Gaps
- Las posiciones concretas de componentes en la Rescue Sheet son iconos; no hay texto con ubicaciones (el corte del lazo se sitúa "bajo el capó", sin cota). No se encontró otra "Emergency Response Guide" más larga para el Cybertruck; tesla.com/firstresponders da 403.

## 6. Interior: pantallas, audio, asientos, selector de marchas, Cyberbeast Tactical Grey

### Takeaway
El manual confirma una pantalla táctil frontal, una pantalla táctil trasera opcional, selector de marchas por barra táctil más botones P-R-N-D en la consola del techo, asientos de "vegan leather", pero **no da tamaños de pantalla ni número de altavoces ni el color Tactical Grey**; esas cifras (18,5", 9,4", 15 altavoces) solo salen de fichas de concesionarios y prensa.

### Cited Findings
- [V] Pantalla frontal ("touchscreen") y pantalla trasera ("rear touchscreen", si está equipada) con funciones: ventilador, climatización, asientos (calefactores traseros y mover el asiento del pasajero delantero), multimedia, vídeo, arcade, navegación; auriculares Bluetooth (hasta dos) — manual PDF, págs. 6-12, [Rear Touchscreen]. No se declara el tamaño en pulgadas.
- [V] No existe cuadro de instrumentos separado: estado del vehículo, velocidad y avisos aparecen en la pantalla ("Vehicle status") — manual PDF pág. 14.
- [V] Selector de marchas: barra de modo de conducción en la pantalla (deslizar arriba = Drive, abajo = Reverse, pulsar = Park; Neutral desde Controls) y selector secundario en la consola del techo con botones P, R, N y D con LED; se activa también pulsando a la vez las dos ruedas de desplazamiento del volante (pág. 74-75). Freno de estacionamiento eléctrico.
- [V] Altavoces: el manual menciona sliders de subwoofer, 5 bandas de ecualización, "Immersive Sound" con audio premium, altavoz del sistema de aviso a peatones (PWS) y altavoz (si está equipado) junto a la luz de ángulo muerto; no da recuento.
- [R] 18,5" (pantalla central) y 9,4" (trasera): ficha de concesionario Dilawri ([2024 Cybertruck](https://www.dilawri.ca/en/inventory/tesla/cybertruck/2024-tesla-cybertruck-id37546864)) y Top Gear ([interior](https://www.topgear.com/car-reviews/tesla/cybertruck/interior)) vía resultado de búsqueda; no confirmado en Tesla.
- [R] Altavoces: 15 según la mayoría de fichas (una con 2 subwoofers) y 13 según otra ficha de concesionario y CarGurus — [CarGurus 2025](https://jobs.cargurus.com/research/articles/2025-tesla-cybertruck-pricing-specs-release-date) (el recuento difiere; conflicto).
- [R] Color interior "Tactical Grey" en una ficha de Cyberbeast ([automanager Cyberbeast](https://clients.automanager.com/7c0c23dee9d84201a364705868e6a182/vehicle-details/2024-tesla-cybertruck-cyberbeast-truck-4816efcfa99143849ef1133e9a7fbd9d)); no hay confirmación de Tesla de que sea estándar en Cyberbeast.
- [V] Asientos: "custom, sustainable, vegan leather" (limpieza del manual, pág. de Cleaning); cinco plazas; los asientos delanteros llevan airbags montados en el asiento; las filas traseras tienen anclajes LATCH/ISOFIX; el asiento del pasajero puede moverse desde la pantalla trasera.
- [V] Dos enchufes de 120 V en cabina (consola y bajo la pantalla trasera), puertos USB-C, cargadores inalámbricos y lector de tarjeta llave en consola (págs. 5-6, 20).

### Inferences
- [I] El selector táctil + botones del techo implica que no hay palanca de cambios ni columna de selector; en el modelado, el control de marcha es la barra de pantalla y el panel de techo.
- [I] Que Tesla no cite pulgadas en el manual impide etiquetar 18,5" y 9,4" como Verified; se mantienen como Reported hasta ver la página de Tesla.

### Gaps
- Tamaños de pantalla, número de altavoces y color Tactical Grey: sin fuente primaria de Tesla (tesla.com da 403). Dimensiones de los asientos (anchura, reposacabezas) no publicadas.

## Resumen de conflictos y avisos para el redactor
- Vía: 1.772 mm (Owner's Manual) frente a 1.777 mm delantera / 1.772 mm trasera (Service Manual alineación).
- Par del enganche trasero: 198 Nm (Tow Hitch) frente a 178 Nm (Rear Energy Absorber).
- Tensión HV: 700 V nominal (Owner's Manual) frente a "800V Li-Ion" (Rescue Sheet).
- Owner's Manual: títulos de tabla de suspensión (coil frente a air) invertidos respecto al texto.
- Altavoces 15 frente a 13 en fichas de concesionarios.
- Procedimiento de subchasis trasero Tri-Motor marcado "DRAFT" por Tesla; valores validados pero advertencias pueden faltar.
- Datos de variante: el Owner's Manual PDF es para Norteamérica (Software 2026.20); otros mercados pueden diferir.
