# Ficha técnica de piezas del Tesla Cybertruck Cyberbeast (EE. UU., producción actual)

> Referencia para ampliar el modelo 3D 1:1. Fecha de consolidación: 2026-10-17. Todo el texto está en español; los nombres oficiales de pieza, las URL y los identificadores técnicos se conservan en inglés.

## 1. Resumen y alcance

**Hallazgo principal.** Las fuentes públicas permiten nombrar, contar y fijar (tornillería y par) varios cientos de piezas del Cybertruck, pero **no permiten dimensionarlas ni asignarles material pieza a pieza**: el Service Manual (SM), el Collision Repair Manual (CR) y el Owner's Manual (OM) de Tesla son la única fuente primaria útil, y entregan nombres oficiales, cantidades de fijaciones, pares, números de pieza de tornillería y cotas exteriores globales, pero las cotas de control del CR y los mapas de material están solo en imágenes. No existe BOM, CAD ni catálogo de piezas accesible. Un modelo 1:1 con más piezas debe apoyarse en (a) la nomenclatura y la tornillería del SM/CR, y (b) fotos, patentes y teardowns de Munro para la forma.

**Fuentes consideradas.** Se sintetizan 10 ficheros de notas (los 7 de primera ronda: exterior, estructura, chasis, tren motriz/batería/térmica, interior, electrónica/48 V y cotas/fuentes/variantes; y los 3 `ronda2_`: cotas oficiales y huecos, motriz/batería del manual de servicio, electrónica/exterior del manual de servicio). El encargo hablaba de 11 ficheros; en la carpeta solo hay 10. Además se leyó el inventario del modelo actual (`docs/component-inventory.md`, 560 nodos con metadatos; el modelo declara 561 objetos al contar la raíz) y los extractos de `docs/model-specification.md` y `docs/research-and-fidelity.md`.

**Cómo acceder a las fuentes primarias.** `tesla.com` devuelve HTTP 403 a las herramientas automáticas; el espejo `tesla.cn` sirve el Owner's Manual completo (HTML por GUID y PDF, Software 2026.20, North America) y `service.tesla.com` sirve el SM y el CR en HTML estático con `curl` y User-Agent de navegador (ver sección 7).

**Tamaño de lo documentado (según las notas).**

| Bloque | Cifra documentada | Naturaleza |
|---|---|---|
| Exterior/cierres/vidrio/luces (SM 10xx, 11xx, 12xx, 17xx) | ~250 títulos de procedimiento distintos | Nombres oficiales; fijaciones solo en ~75 páginas leídas |
| Estructura (CR) | ~55 procedimientos de piezas estructurales + 8 guías de reparabilidad | Cantidades de remaches/tornillos, pares, números de pieza de tornillería |
| Chasis (SM 31xx–34xx) | 161 filas en la tabla consolidada de las notas | Nombre + cantidad + par; sin dimensiones ni material |
| Tren motriz, batería, térmica (SM 16xx, 18xx, 3xxx) | ~230 filas de fijación/par | Sin masa de ninguna unidad |
| Interior (SM 13xx–21xx) | >170 piezas con nombre oficial | Varias con clips/tornillos y par |
| Electrónica/48 V/sensores | 73 líneas (~100+ piezas físicas expandidas) + ~190 entradas de fijación | Sin números de pieza ni masas |

**Qué falta.** Dimensiones y masa de casi todas las piezas, material por pieza, números de pieza (solo tornillería, cintas de abrasión y herramientas), cotas de control del CR (imágenes), huecos de panel (el SM remite a un documento interno «Inspection Standards»), ángulos de ataque/ventral/salida, tamaños de pantalla y número de altavoces confirmados por Tesla. Ver secciones 6 y 7.

### 1.1 Cómo leer la confianza

Las notas usan tres etiquetas de origen. El encargo pide mapearlas a las etiquetas del modelo (`Verificado / Reconstruido / Aproximado`) así:

| Etiqueta de las notas | Significado en las notas | Etiqueta en esta ficha | Abrev. |
|---|---|---|---|
| Verified | Texto primario de Tesla (SM, CR, OM, Rescue Sheet) leído directamente | **Verificado** | V |
| Reported | Fuente secundaria (prensa, teardown de terceros, agregadores, fichas de concesionario), o resumen de buscador de una página de Tesla no abierta | **Reconstruido** | R |
| Inferred | Deducción del investigador, no escrita en ninguna fuente | **Aproximado** | A |

Reglas de lectura:

- La etiqueta se refiere al **dato de la fila** (existencia, nombre, cantidad, par). Una pieza «V» por nombre en el índice del SM no está verificada en forma, material ni dimensiones; esos campos valen «—» o llevan su propia etiqueta.
- La definición del repositorio (`docs/research-and-fidelity.md`) es algo distinta: «Reconstruido» = inferido a partir de varias referencias coherentes; «Aproximado» = insuficientemente documentado. El mapeo del encargo coloca «Reported» en Reconstruido y «Inferred» en Aproximado; se respeta aquí, pero al volcar la ficha al modelo conviene reetiquetar según esa definición.
- Cuando una fila lleva dos etiquetas (p. ej. «V/A»), la primera es la existencia/nombre y la segunda la cantidad o el lado RH deducido.
- `†` en cantidad = el lado RH (o la pareja) se **supone** simétrico porque el manual documenta solo el lado LH («RH similar»). Es dato A para ese número.
- Todas las páginas del SM están marcadas «DRAFT» por Tesla («Warnings and Cautions might be missing»). Las cifras de varias páginas fueron extraídas por un resumidor automático; las notas señalan dos páginas con discrepancias internas visibles (ver sección 6).

### 1.2 Convenciones de fuente

Las filas citan códigos mnemónicos (p. ej. `SM-Headlamp`). La URL completa de cada código está en el **Registro de fuentes (Anexo A)**: base + GUID. Bases:

- `SM` = `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-<guid>.html`
- `CR` = `https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-<guid>.html`
- `OM` = `https://www.tesla.cn/ownersmanual/cybertruck/en_us/GUID-<guid>.html` (espejo de tesla.com)

### 1.3 Etiquetas de variante (columna «Var.»)

| Etiqueta | Significado |
|---|---|
| CB | Cyberbeast / Tri Motor confirmado en la página o en el título |
| TM | Página «Tri Motor» (se asume Cyberbeast; el mapeo es A) |
| DM / AWD | Dual Motor / Premium AWD (no Cyberbeast) |
| LR | Long Range (RWD, muelles helicoidales, llanta de acero de 18"): no es Cyberbeast |
| Todas | El OM/SM dice que es común a todas las variantes |
| S/E | Sin etiqueta de variante en la página: probable común, **no confirmado para Cyberbeast** |
| Opc | Opción o accesorio (Terrestrial Armor, Off-Road Lightbar, etc.) |
| fecha | Etiqueta de fecha de producción («Post 11/4/2024», «Post-April 2024», etc.) |
| Std / Gen 4 / HW4 | Etiquetas literales de la página («Standard», «Gen 4», cámaras «HW4»); no equivalen a Cyberbeast |

Las notas advierten que el SM «no etiqueta Cyberbeast de forma explícita» en casi ninguna página; el mapeo Cyberbeast = «Tri Motor» y «sin etiqueta» es una inferencia (A).

---

## 2. Cotas y especificaciones oficiales consolidadas

La fuente de referencia es el OM (espejo tesla.cn, «Dimensions, Weights, and Cargo Capacity», © 2026, y PDF del manual) [`OM-Dimensions`], todo **V**. Los valores de fuentes secundarias se listan solo para señalar conflictos.

### 2.1 Exteriores

| Parámetro | Valor oficial (V) | Otras fuentes (R) | Conflicto / nota |
|---|---|---|---|
| Longitud | 223,74 in / 5.682,9 mm | 223,7 in / 5.683 mm ([Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck), [Basenor](https://www.basenor.com/pages/cybertruck-dimensions)) | Coincide |
| Ancho con retrovisores | 95,01 in / 2.413,3 mm | ~95,0 in ([evspecifications](https://www.evspecifications.com/en/model/60e52d4)) | Coincide |
| Ancho con retrovisores plegados | 86,64 in / 2.200,7 mm | — | Solo OM |
| Ancho sin retrovisores | 79,98 in / 2.031,6 mm | 79,99 in / 2.032 mm (Wikipedia) | Coincide |
| Batalla | 143,11 in / 3.635,0 mm | 143,1 in (Wikipedia); SM alineación 3.635 mm (V) | Coincide |
| Voladizo delantero / trasero | 34,58 in / 878,3 mm; 46,05 in / 1.169,6 mm | — | Solo OM |
| Vía delantera / trasera | 69,76 in / 1.772,0 mm (ambas) | SM alineación: 1.777 mm del. / 1.772 mm tras. (V) | **Conflicto OM vs SM de 5 mm** (probablemente puntos de medida distintos, A) |
| Altura (CB/AWD, ajuste Medium) | 70,62 in / 1.793,8 mm | Wikipedia 70,7 in / 1.796 mm (R) | Usar OM |
| Altura por ajuste (CB/AWD) | Entry 1.738,8; Low 1.753,8; Medium 1.793,8; High 1.853,8; Very High 1.893,8; Extract 1.943,8 mm | — | Coherente con la tabla de deltas (A) |
| Distancia al suelo (CB/AWD) | Entry 202; Low 217; Medium 257; High 317; Very High 357; Extract 407 mm | Concesionarios 201 mm mín. / 406 mm máx. (R); Basenor 9,5 in autopista / 17,4 in off-road (R) | OM y concesionarios coinciden en extremos; Basenor discrepa. «Altura de chasis» Medium 265 ± 5 mm del SM es una cota de referencia de alineación, no la misma magnitud |
| Altura de chasis Medium (alineación, aire) | 265 ± 5 mm (250 ± 5 mm con Terrestrial Armor) | — | `SM-ALIGN` (V); versiones con muelle helicoidal: 18" 264/262 mm; 20" 274/272 mm (con Armor 249/247 y 259/257) |
| Deltas de suspensión respecto a Medium | High +2,4 in; Low −1,6 in; Entry −2,2 in; Very High +3,9 in; Extract +5,9 in | Basenor: Entry 2,2 in (R) | OM PDF pág. 94 (V). Extract limita a 10 mph; Very High a 25 mph |
| Modo Wade | ~32 in (815 mm) desde la base del neumático, máx. 30 min, ride height Very High, batería HV presurizada | Wikipedia 2,5 ft (0,76 m) (R) | OM PDF pág. 105-106 (V); la cifra de Wikipedia difiere |
| Ángulos de ataque / ventral / salida | **No publicados en el OM** (verificado por búsqueda en las 17.178 líneas) | Concesionarios 40°/26°/28°; Basenor 35°/—/28° (R) | **Conflicto 35° vs 40° en ataque**; sin fuente primaria |
| Caja: altura delante/detrás (CB/AWD) | 28,66 in / 727,9 mm; 19,84 in / 503,8 mm | Basenor «72,9 x 51 x 28,66/19,89 in» (R) | Coincide en alturas |
| Caja: ancho / largo en suelo | 51,00 in / 1.295,4 mm; 71,84 in / 1.824,6 mm | Wikipedia: 6 ft x 4 ft (R) | Basenor 72,9 in vs OM 71,84 in |
| Caja LR | 29,92 in / 759,9 mm; 20,81 in / 528,6 mm | — | No es Cyberbeast |

### 2.2 Interiores y volúmenes (OM, V)

| Parámetro | Delante / detrás | Notas |
|---|---|---|
| Altura libre | 41,69 in (1.058,8 mm) / 39,05 in (991,9 mm) | Coincide con iSeeCars/concesionarios (R) |
| Espacio piernas | 41,09 in (1.043,6 mm) / 40,90 in (1.038,8 mm) | |
| Hombros | 63,31 in (1.608,0 mm) / 62,06 in (1.576,4 mm) | |
| Caderas | 57,22 in (1.453,3 mm) / 57,22 in (1.453,5 mm) | |

Volúmenes (CB/AWD, ft³ / L): frunk 7,1 / 200; caja cerrada sobre el piso 56,1 / 1.589; compartimento inferior 3,4 / 97; cabina detrás de asientos delanteros 54,1 / 1.533; total con cinco pasajeros 66,6 / 1.885; con dos pasajeros 120,7 / 3.418 (V). Otras fuentes: sub-maletero ~17 ft³ / 481 L ([Basenor](https://www.basenor.com/pages/cybertruck-dimensions), R) frente a 3,4 ft³ del OM: **conflicto**; Wikipedia 67 ft³ totales (incluye el sub-maletero) frente a 66,6 ft³ del OM (compatibles). No hay cotas de sección más allá de las cuatro anteriores, radio de giro por eje, anchura de puertas (no publicadas).

### 2.3 Masas, cargas y remolque (OM y SM, V)

| Parámetro | Cyberbeast | Premium AWD | LR | Conflictos |
|---|---|---|---|---|
| Peso en vacío (AS = all-season) | 6.863 lb / 3.113 kg | 6.634 lb / 3.009 kg | 6.118 lb / 2.775 kg | Cyberbeast: 6.901 lb (Wikipedia, Basenor, Car and Driver), 6.898 lb (iFixit), 6.843 lb (medido por Munro, [Autopian](https://theautopian.com/latest-cybertruck-teardown-reveals-teslas-odd-sway-bar-decisions-clever-packaging)), 6.863 lb (KBB 2025) |
| Peso en vacío (AT = all-terrain) | 6.898 lb / 3.129 kg | 6.669 lb / 3.025 kg | — | — |
| Eje del./tras. en vacío (CB AS) | Del. 3.336 lb / 1.513 kg; tras. 3.527 lb / 1.600 kg (CB AT: 3.353 / 1.521 y 3.545 / 1.608) | — | — | — |
| Peso máximo en vacío del SM (con opciones y fluidos) | Tri Motor 6.918 lb / 3.137 kg | Dual Motor 6.669 lb / 3.025 kg | — | `SM-WeightInfo`; GVWR ambas 9.169 lb / 4.158 kg |
| Carga útil | 2.000 lb / 907 kg (AS); 2.270 / 1.030 (AT) | 2.200 / 998 (AS); 2.500 / 1.134 (AT) | 2.006 / 910 | Wikipedia/Basenor dan ~2.500 lb para AWD y CB: no coincide con el OM para CB |
| GVWR | AS 8.863 lb / 4.020 kg; AT 9.169 lb / 4.159 kg | AS 8.834 / 4.007; AT 9.169 / 4.159 | 8.199 / 3.719 | — |
| GAWR delantero / trasero | 4.255 lb / 1.930 kg; 5.009 / 2.272 (AS) o 5.247 / 2.380 (AT) | — | — | — |
| Remolque máximo | 11.000 lb / 4.990 kg | 11.000 lb | 7.500 lb / 3.402 kg | Coincide con Basenor |
| Tongue weight máx. | 1.100 lb / 499 kg (20" x 9J) | — | 750 lb / 340 kg | OM PDF pág. 112 |
| Límites de carga | Frunk 441 lb / 200 kg; compartimento bajo caja 220 lb / 100 kg; baca 220 lb / 100 kg por juego de 2 travesaños | — | — | Basenor frunk 420 lb (R) |

### 2.4 Ruedas, frenos, dirección, suspensión, fluidos (V salvo indicación)

| Parámetro | Valor | Fuente | Nota |
|---|---|---|---|
| Llanta | 20 x 9.0J ET58.5 (todas) y 18 x 9.0J ET58.5; 6 tuercas, llave 21 mm, 205 Nm (151 lb·ft) | `OM-Wheel`, `SM-Wheel` | Patrón 6x139,7, buje 84 mm, espárrago M14x1,5, rueda 35,2 lb: solo [Unplugged Performance](https://unpluggedperformance.com/cybertruck/wheel-and-tire-guide/) (R); EVANNEX da 6x139,5 / 84,15 (R, probable errata) |
| Neumáticos de fábrica | 285/65R20 all season (Hard Metric); LT285/65R20 Pirelli Scorpion ATR all terrain; 285/70R18 Goodyear Wrangler Territory RT/HT all season | OM PDF pág. 217 | Las notas de chasis atribuyen el Scorpion ATR a la medida 285/65R20 «Hard-metric» y el Goodyear Wrangler Territory RT a la LT285/65R20 AT: **la atribución marca/medida difiere entre notas** |
| Diámetro exterior 285/65R20 | ~878,5 mm | cálculo de las notas | Aritmética, no dato Tesla (A) |
| Presiones | 50 psi (20" AS, 20" AT, 18" AS); 65 psi en 20" AT a carga GVWR/remolque | OM PDF pág. 211 | TPMS se reinicia tras 10 min a >15 mph |
| Tracción Cyberbeast | Motor delantero síncrono de imanes permanentes + 2 traseros de inducción, líquido-refrigerados; reducción global 15,02:1, una marcha; marcha atrás limitada a 15 mph | `OM-Subsystems` | Tabla del OM para Premium AWD aparece con motores invertidos y relación «2»: errata aparente |
| Dirección | Steer-by-wire en 4 ruedas, 0,94 vueltas tope a tope (340°), giro bordillo a bordillo ~13,25 m (43,5 ft); Rear Steer Off/Auto | `OM-Subsystems` | Basenor da 200° o 340° y 3° (futuro 10°) de dirección trasera (R, baja confianza) |
| Frenos | Pinzas delanteras fijas de 4 pistones; traseras flotantes de 1 pistón con EPB; discos ventilados Ø351 mm (del.) / Ø356 mm (tras.); espesor nuevo/límite: 32/30 mm del., 23/21 mm tras.; pastilla nueva/límite: 10/3 mm del., 11/2 mm tras.; descentrado lateral 0,050 mm, circular 0,040 mm, variación de espesor 0,010 mm | `SM-BRK` | Diámetro de pistones: no publicado |
| Suspensión | Independiente, doble horquilla delante y detrás, muelle neumático coaxial, barra estabilizadora; aire adaptativo en CB/AWD | `SM-Susp` | Depósito de aire a ~16 bar (`SM-SCUBA`); volumen no publicado |
| Alineación (aire, 2026-08-19) | Camber del. −0,50° ± 0,45°, tras. −1,00° ± 1,00°; caster 3,60° ± 1,00°; toe individual del. Out 0,05°, tras. In 0,20° | `SM-ALIGN` | Variante muelle helicoidal: camber −0,37°/−0,95°, caster 3,45°, toe 0,04°/0,19°. Un extracto anterior mostraba camber −0,70° y toe ±0,15° (página revisada) |
| Batería de baja tensión | 48 V, 4 Ah (OM) | `OM-Subsystems` | InsideEVs: ~192 Wh (R); el SM no da capacidad |
| Batería HV | Ion-litio refrigerada por líquido, **700 V DC nominal** (OM); límites −30 °C a 65 °C más de 24 h | OM PDF pág. 243-244 | **Conflicto**: Rescue Sheet «800V Li-Ion»; Autopian/Munro «800 V nominal» (R); 192 × 3,6 V = 691 V apoya los 700 V (A) |
| Capacidad HV | 123 kWh total / 111,9 kWh útil (agregador), 1.344 celdas 4680 | [ArenaEV](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php), [InsideEVs](https://insideevs.com/news/724981/tesla-cybertruck-battery-passport-4680cell/) (R) | Masa del pack 1.590 lb / 720 kg solo en Wikipedia (R); ninguna página del SM la da |
| Prestaciones Cyberbeast | 845 hp (621 kW), 10.296 lb·ft de par en rueda, 0-60 mph 2,6 s | ArenaEV, Autopian (R) | Sin cifra primaria de Tesla en las notas |
| Carga | AC 11,5 kW (240 V / 48 A); DC hasta 250 kW (400 V) / 350 kW (800 V); NACS; V2L 9,6 kW; V2H 11,5 kW | Wikipedia, Notebookcheck (R) | — |
| Fluidos | Líquido de frenos DOT 4 BASF Hydraulan 404 (1.190 mL llenado desde seco; revisión cada 4 años); aceite del reductor KAF1; refrigerante HTF-LS naranja 50/50 (G-48 azul en producción temprana), 23,5 L Tri-Motor y 22,5 L Dual Motor; refrigerante A/C R1234yf 1.020 g; aceite POE RB100EV 250 g | `SM-FluidCap`, `SM-Fluids` | Una nota de motriz dice que la carga de refrigerante «no figura»: las páginas Fluid Capacities (ronda 2, cotas) sí la dan; prevalece la ronda 2. Volumen de aceite del reductor: «hasta rebosar», sin litros |
| Enchufes | 120 V a 20 A máx. en consola y bajo la pantalla trasera; en caja 2 × 120 V y 1 × 240 V | OM PDF | Basenor: 240 V/40 A NEMA 14-50 en caja (R) |
| Chapa exterior | Inox serie 300 «30X» laminado en frío: 1,8 mm puertas, 1,4 mm resto (Wikipedia citando a Lars Moravy, [Design News](https://www.designnews.com/automotive-engineering/video-how-tesla-stamps-cybertruck-stainless-steel)) | R | **Conflicto**: ~3 mm (Musk vía [SAE](https://www.sae.org/site/news/2020/06/tesla-cybertruck-stainless-steel)); el grado «30X» no verificado en fuente primaria |
| Seguridad | NHTSA 5 estrellas global (vuelco 4); IIHS Top Safety Pick+ (crew cab 2025) | [IIHS](https://www.iihs.org/ratings/vehicle/tesla/cybertruck-crew-cab-pickup/2025), [Notebookcheck](https://www.notebookcheck.net/2025-Tesla-Cybertruck-crash-test-results-NHTSA-ratings-more-positive-than-IIHS.1116349.0.html) (R) | Otra fuente cita «poor» en small overlap (versión previa, A) |

No obtenidos de ninguna fuente: Cx, grosor de vidrios, voladizos distintos de los dos del OM, radio de giro por eje, ángulo físico de las ruedas traseras.

---
## 3. Tablas de piezas por sistema

**Columnas.** ID · Pieza (EN oficial) · Nombre ES · Cant. (por vehículo; `†` = pareja RH supuesta) · Ubicación · Material · Dimensiones/masa · Fijaciones/par · Var. · Conf. (V/R/A) · Fuente (código del Anexo A).

**Reglas.** Material y dimensiones valen «—» salvo que una nota los dé. Los pares están en Nm. «Código de corrección» y FRT (tiempo oficial de mano de obra) no se transcriben salvo que sirvan para localizar la página. Las listas de piezas con nombre pero sin dato de fijación se dan por nombre oficial (V de existencia).

### 3.1 Exterior, cierres, vidrio y luces

Contexto: los paneles exteriores son de acero inoxidable (Rescue Sheet, V) pegados a una estructura interior; ver sección 3.2 para el material y los espesores.

#### 3.1.1 Fascias, frontal y aletas

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-001 | Front Fascia | Fascia delantera | 1 | Frontal | — | — | 4 pernos 10 mm 4 Nm + 1 perno lateral LH y 1 RH 10 mm 6 Nm; 3 conectores RH; 4 clips al paso de rueda por lado | S/E | V | `SM-FrontFascia` |
| EXT-002 | Front Fascia Fairing Assembly LH/RH | Carenado de fascia delantera | 2 | Frontal | — | — | — | S/E | V | `SM-Bumper1001` |
| EXT-003 | Front Center Applique Assembly | Aplique central delantero | 1 | Frontal | — | — | Se retira para acceder al faro | S/E | V | `SM-Bumper1001`, `SM-Headlamp` |
| EXT-004 | Front Lower Grille | Rejilla inferior delantera | 1 | Fascia | — | — | — | S/E | V | `SM-Bumper1001` |
| EXT-005 | Active Grille Shutter | Persiana activa de rejilla | 1 | Rejilla | — | Nº de lamas: no publicado | 12 pestañas de bloqueo + 2 clips; acceso: travesaño delantero 2 pernos 18 mm 90 Nm, valance inferior 6 pernos 6 Nm, aeroshield 11 pernos 6 Nm, CFM | S/E | V | `SM-GrilleShutter` |
| EXT-006 | Foam Seal Upper / Lower / Side Front Grille | Juntas de espuma de la rejilla | 3 (nombres) | Rejilla | Espuma | — | — | S/E | V | `SM-Bumper1001` |
| EXT-007 | Front End Carrier Plastic Assembly | Portador frontal de plástico | 1 | Frontal | Plástico | — | — | S/E | V | `SM-Bumper1001` |
| EXT-008 | Cover-Camera-Lower-Fascia-Front | Cubierta de la cámara de fascia | 1 | Fascia | — | — | 2 tornillos PH1 2 Nm | S/E | V | `SM-FasciaCam` |
| EXT-009 | Front Fascia Lower Dummy LP Cover | Cubierta simulada de matrícula | 1 | Fascia | — | — | Se retira para acceder a la cámara | S/E | V | `SM-BodyPanels1010` |
| EXT-010 | Front License Plate Assembly; Front Bracket (retrofit) | Placa/soporte de matrícula delantera | 1 + 1 | Fascia | — | — | — | S/E | V | `SM-Fittings12` |
| EXT-011 | Lower Tow Eye Cap LH/RH | Tapa del ojal de remolque | 2 | Fascia delantera | — | — | 4 pernos 10 mm 4 Nm (tapas de ganchos) | S/E | V | `SM-Bumper1001`, `SM-SFF` |
| EXT-012 | Powergate Fascia | Fascia del Powergate (capó) | 1 | Capó | — | — | Se retira antes de la barra de luz | S/E | V | `SM-BodyPanels1010`, `SM-Lightbar` |
| EXT-013 | Fender Assembly Front LH/RH | Aleta delantera | 2 | Pilar A / viga superior de aleta | — | Orificio de montaje Ø8 mm con E-coat | 3 pernos al pilar A + 2 a la viga superior, todos 30 Nm (13 mm); 2 clips de arnés | S/E | V | `SM-Fender` |
| EXT-014 | Fender Flare Carrier (Fore-Front, Aft-Front, Fore-Rear, Aft-Rear; cada uno LH/RH) | Soporte de la aleta de paso de rueda | 8 | Pasos de rueda | — | — | Trasero LH: aft 2 pernos 7 Nm, fore 6 pernos 7 Nm | S/E | V | `SM-Fittings12`, `SM-ChgBus` |
| EXT-015 | Fender Flares Fore / Aft Rear | Aleta de paso de rueda trasero (tramos delantero y trasero) | — | Pasos de rueda traseros | — | — | — | S/E | V | `SM-Fittings12` |
| EXT-016 | Baffle Fender Front | Deflector de aleta delantera | — | Aleta | — | — | — | S/E | V | `SM-Fittings12` |
| EXT-017 | Rear Fascia | Fascia trasera | 1 | Trasera | — | — | 2 pernos centrales 10 mm 6 Nm; 9 pernos de difusor 10 mm 6 Nm; 16 pestañas; 5 clips de liner por lado; 1 conector | S/E | V | `SM-RearFascia` |
| EXT-018 | Step Bracket Center LH/RH Rear Fascia; Body Side Bracket LH Rear Fascia; Rear Energy Absorber Fascia Step Bracket Center | Soportes de la fascia trasera / escalón | — | Trasera | — | — | Tow hitch: 2 pernos de soporte de escalón 13 mm 16 Nm | S/E | V | `SM-Bumper1001`, `SM-TowHitch` |
| EXT-019 | Trailer Hitch Cover | Tapa del enganche | 1 | Trasera | — | — | Cierres de cuarto de vuelta; 4 pestañas | S/E | V | `SM-HitchCover` |
| EXT-020 | Rocker Panel Assembly; Rocker Panel Rear Fairing | Faldón lateral; carenado trasero del faldón | 2 + 2† | Umbrales | — | — | Cubierta de faldón a ski 6 pernos 10 mm 10 Nm por lado; 1 perno 10 mm 4 Nm en 4 puntos | S/E | V | `SM-Fittings12`, `SM-HVBattLR` |
| EXT-021 | Rocker Step Reinforcement Front / Rear | Refuerzo de escalón del faldón | 3 por posición | Umbrales | — | — | 3 pernos 10 mm 15 Nm por posición | S/E | V | `SM-HVBattLR` |
| EXT-022 | Structural Off-Road Rocker | Faldón estructural off-road | 2† | Umbrales | — | — | Ver Terrestrial Armor | Opc | V | `SM-Fittings12`, `SM-TerrArmor` |
| EXT-023 | Mud Flap Front LH/RH | Faldilla delantera | 2 | Pasos de rueda del. | — | — | 2 clips al liner + 2 pernos 10 mm profundos 1,8 Nm al faldón | S/E | V | `SM-MudFlapF` |
| EXT-024 | Mud Flap Rear LH/RH | Faldilla trasera | 2 | Pasos de rueda tras. | — | — | 4 pernos 10 mm profundos 2,2 Nm (1 al difusor + 3 al liner); modelos anteriores con clips; tuercas en U añadidas 2025-11-17 | fecha | V | `SM-MudFlapR` |
| EXT-025 | Sail Applique LH/RH (dos generaciones); Sail Applique Set (retrofit); Applique Sail Baffle; Closeout Sail Baffle | Aplique de la vela (pilar C-caja) y deflector | 2 + 2 | Vela trasera | — | — | 17 clips + 1 datum + 1 clip de arnés + 1 conector por lado; reutilizable máx. 5 ciclos; PN 1741538-XX-X (LH) / 1741539-XX-X (RH) antiguo, 2009390-00-A (LH) tras 4-nov-2024 | fecha | V | `SM-TonneauRail`, `SM-SlatSystem` |
| EXT-026 | Applique B-Pillar LH/RH; Closeout Applique B-Pillar | Aplique del pilar B | 2 | Pilar B | — | — | 1 perno 10 mm 6 Nm; 2 conectores (punto BLE + cámara); 3 clips | S/E | V | `SM-ApplBPillar` |
| EXT-027 | Applique C-Pillar; Closeout Applique C-Pillar | Aplique del pilar C | 2† | Pilar C | — | — | — | S/E | V | `SM-Fittings12` |
| EXT-028 | Applique Backlite; Applique Closeout Lamp Rear; Applique Roof (+ Bracket Applique Roof); Applique Upper Fascia; Applique Wiper; Top Applique Tailgate | Apliques exteriores (luneta, piloto, techo, fascia superior, limpia, portón) | — | Varias | — | — | Aplique del limpiaparabrisas: 2 clips + 2 datums | S/E | V | `SM-Fittings12`, `SM-Windshield` |
| EXT-029 | Beauty Cover Lightbar LH/RH (+ bracket) | Embellecedor de la barra de luz | 2 | Frontal | — | — | — | S/E | V | `SM-Fittings12` |
| EXT-030 | Trim Cantrail Roof Rail LH/RH | Moldura del larguero de techo | 2 | Techo | — | — | — | S/E | V | `SM-BodyPanels1010` |
| EXT-031 | Bed Side Outer Assembly LH/RH (variantes Long Range y estándar) | Panel exterior lateral de la caja | 2 | Caja | — | — | Estructura: ver Body Side Outer (3.2) | S/E | V | `SM-BodyPanels1010` |
| EXT-032 | Bed Side Applique Corner Bracket LH/RH; Rear Under Body Rear Fascia Bracket LH/RH; Lamp Step Bracket LH/RH; Dash Absorber LH/RH | Soportes y absorbedor del salpicadero | 2 c/u | Varias | — | — | — | S/E | V | `SM-BodyPanels1010` |
| EXT-033 | Underhood Apron LH/RH; Underhood Apron Rear | Faldón de bajo capó | 2 + 1 | Cowl / frunk | — | — | Apron trasero: 9 clips | S/E | V | `SM-Fittings12`, `SM-Windshield` |

#### 3.1.2 Puertas, vidrio móvil y retrovisores (por puerta salvo indicación)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-040 | Door Front LH/RH; Door Rear LH/RH | Puerta delantera / trasera | 4 | Laterales | Piel de inox 1,8 mm (R, [Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck)) | — | 2 fijaciones de bisagra 38 Nm (15 mm perfil bajo); perno del tirante 23 Nm (T40); pasamuros de arnés en pilar A | S/E | V (pieza) / R (espesor) | `SM-FrontDoor`, `SM-BodyPanels1010` |
| EXT-041 | Hinge Upper / Lower Front and Rear door; Stud Plate Hinge Upper/Lower | Bisagras superior e inferior; placas de espárragos | 8 bisagras; placas: 4 por lado (marcadas «NEW») | Pilares A/B/C | — | — | 38 Nm (2 fijaciones por bisagra, puerta delantera) | S/E | V | `SM-Closures1133`, `SM-BodyPanels1010` |
| EXT-042 | Check Strap Front / Rear | Tirante de retención | 4 | Puertas | — | — | Perno 23 Nm (T40, delantero) | S/E | V | `SM-FrontDoor` |
| EXT-043 | Door Latch Front / Rear | Cierre eléctrico de puerta | 4 | Puertas | — | — | T30 13 Nm, nº de tornillos no indicado | S/E | V | `SM-DoorLatch` |
| EXT-044 | Door Presenter Front / Rear | Presentador de puerta (empuje motorizado) | 4 | Tras el closeout de puerta | — | — | 2 pernos T30 13 Nm; 1 conector | S/E | V | `SM-DoorPresenter` |
| EXT-045 | Door Striker Rear (y delantero) | Percutor | 4† | Pilares | — | — | — | S/E | V (trasero) / A (delantero) | `SM-Closures1133` |
| EXT-046 | Closeout Panel Front / Rear door | Panel de cierre de puerta | 4 | Puertas | — | — | — | S/E | V | `SM-DoorGlass1150` |
| EXT-047 | Window Regulator Front / Rear door; Window Regulator, 48V Q-Motor | Elevalunas; motor Q de 48 V | 4 + 4 motores | Puertas | — | — | Motor Q: 3 pernos T25 4 Nm; 1 conector; calibración con interruptor 15 s abajo/arriba | S/E | V | `SM-WinRegQ`, `SM-WinRegFL` |
| EXT-048 | Moving Glass Door Front LH/RH and Rear LH/RH | Vidrio móvil de puerta | 4 | Puertas | Laminado (Rescue Sheet) | Grosor: — | — | S/E | V | `SM-Glass1020`, `RS` |
| EXT-049 | Primary Seal door front/rear; Secondary Seal front/rear | Burletes primario y secundario | 4 + 4 | Huecos de puerta | Elastómero | — | Secundario: 26 grapas (dato del modelo, no está en las notas) | S/E | V (nombres) | `SM-Seals1170` |
| EXT-050 | Waist Belt Seal Inner and Outer, Front and Rear | Junta de cintura interior/exterior | 8 | Línea de cintura | — | — | 3 tapones de retención en la junta del retrovisor | S/E | V | `SM-Seals1170`, `SM-Mirror` |
| EXT-051 | Glass Run Seal Front Door A-Pillar; Seal Header LH/RH | Guía de cristal; junta de cabecera | 1† + 2 | Pilar A / techo | — | — | — | S/E | V | `SM-Seals1170`, `SM-Glass1020` |
| EXT-052 | Exterior Door Switch Front (B-pillar) / Rear (C-pillar) | Pulsador exterior de puerta | 4† | Pilares B y C | — | — | Delantero 2 pernos T20 3 Nm, 1 conector, 1 pasamuros; trasero 2 tornillos T20 3 Nm | S/E | V | `SM-DoorSwF`, `SM-DoorSwR` |
| EXT-053 | Exterior door handles (sección 1145) | Manillas exteriores | 0 | — | — | — | La sección no tiene procedimientos: no hay manilla mecánica (A) | — | R | `SM-Handles1145` |
| EXT-054 | Exterior Mirror Assembly Electromechanical LH/RH | Retrovisor exterior electromecánico | 2 | Puertas delanteras | — | Ancho total con retrovisores 2.413,3 mm (OM) | 3 pernos T40 18 Nm, PN 1857466-00-B, de un solo uso; 3 tapones de retención en la junta; tapón del panel de puerta; 1 conector | S/E | V | `SM-Mirror` |
| EXT-055 | Mirror Glass Flat Electrochromic Dimming LH/RH; Skull Cap LH/RH | Luna plana electrocrómica; carcasa | 2 + 2 | Retrovisores | — | — | — | S/E | V | `SM-Fittings12` |

#### 3.1.3 Powergate (capó/frunk), portón y caja

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-060 | Powergate Hood | Tapa del frunk («capó») | 1 | Frontal | — | — | 4 tuercas 13 mm 18 Nm; 1 conector; 6 clips de arnés; 14 clips + 6 clips/tuercas a carrocería; liner RH: 2 pernos 6 Nm a chinstrap + 1 clip | S/E | V | `SM-PowergateHood` |
| EXT-061 | Powergate Hinge LH/RH | Bisagra del Powergate | 2 | Base del parabrisas | — | — | 2 pernos 13 mm 58 Nm por lado; 1 clip del amortiguador | S/E | V | `SM-PGHinge` |
| EXT-062 | Hood Strut LH/RH | Amortiguador del Powergate | 2 | Powergate | — | — | Clips de resorte; 1 conector; sujetar el capó con ayudante | S/E | V | `SM-HoodStrut` |
| EXT-063 | Hood Latch (Powergate latch) + latch actuator | Cierre del capó y actuador | 1 | Powergate | — | — | 2 pernos 10 mm 9 Nm; 2 clips + 2 cables; 1 conector | S/E | V | `SM-HoodLatch` |
| EXT-064 | Powergate Striker | Percutor del Powergate | 1 | Carrocería | — | — | 2 pernos T40 15 Nm | S/E | V | `SM-PGStriker` |
| EXT-065 | Powergate manual release; Aero Seal Powergate LH/RH | Liberación manual; junta aerodinámica | 1 + 2 | Frunk | — | — | — | S/E | V | `SM-BodyPanels1010`, `SM-Seals1170` |
| EXT-066 | Frunk Assembly; Frunk Access Panel; Frunk Lamp; Safety Lock Switch; Frunk Seal; Frunk Switch | Cubeta, panel de acceso, luz, interruptor de seguridad, junta e interruptor | 1 c/u | Frunk | — | Volumen 7,1 ft³ / 200 L (OM); límite 441 lb | Frunk assembly 6 pernos 10 mm 12 Nm; 2 tapas de perno + 2 topes | S/E | V | `SM-Fittings12`, `SM-Pentaport`, `SM-HoseHV` |
| EXT-067 | Tailgate Assembly | Portón trasero | 1 | Trasera | — | — | Perno de barra de torsión LH 25 Nm (13 mm); RH T45 50 Nm; 2 conectores + 1 clip; se retira inclinándolo ~45° | S/E | V | `SM-Tailgate` |
| EXT-068 | Tailgate Hinge Body Side LH/RH; Tailgate Latch and Striker | Bisagra de portón en carrocería | 2 | Torres de portón | — | — | 2 pernos 15 mm 75 Nm por lado (antes 50 Nm; cambio 2024-07-10); 1 clip | fecha | V | `SM-TGLatchHinge` |
| EXT-069 | Tailgate Cinching Latch LH/RH | Cierre con acercamiento eléctrico | 2 | Portón | — | — | 2 pernos T40 25 Nm; 1 conector; cable de liberación manual | S/E | V | `SM-CinchLatch` |
| EXT-070 | Tailgate Torsion Rod LH/RH | Barra de torsión del portón | 2 | Portón | — | — | Perno de soporte 15 mm 55 Nm (no retirar); perno de barra 13 mm 80 Nm | S/E | V | `SM-TorsionRod` |
| EXT-071 | Tailgate Strut Damper (LH); Bumpstop; Cable Strap | Amortiguador, tope y cable del portón | 1 + — | Portón | — | — | Solo clips de resorte | S/E | V | `SM-StrutDamper`, `SM-Closures1133` |
| EXT-072 | Seal Tailgate LH/RH; Inner Tailgate Cover; Manual Release Cap Tailgate Cover; Manual Release Tailgate | Juntas, cubierta interior y liberación manual del portón | 2 + 1 + 1 + 1 | Portón | — | — | — | S/E | V | `SM-Seals1170`, `SM-Fittings12` |
| EXT-073 | Bed Floor Assembly | Suelo de la caja | 1 | Caja | — | — | 10 pernos cortos (página LR) o 12 cortos (otras páginas) de 15 mm 56 Nm + 2 largos 46 Nm | S/E | V | `SM-HVBattLR`, `SM-PCS-LR` |
| EXT-074 | Bed Side Wall LH/RH (+ Upper, + Lower, variantes Long Range); Front Wall Assembly Truck Bed; False Wall Bed | Paredes de la caja | 2 + 1 + 1 | Caja | — | Caja: 71,84 x 51,00 in en suelo (OM) | Pared lateral inferior 1 perno 15 mm 46 Nm, 2 pernos 36 Nm, 4 pernos 10 mm 11 Nm, 2 tuercas 7 Nm, 1 perno 10 Nm; false wall 2 pernos 15 mm 45 Nm + 4 tuercas 13 mm 30 Nm | S/E (LR para Upper/Lower) | V | `SM-Fittings12`, `SM-TonneauMotor`, `SM-TonneauLower` |
| EXT-075 | Bed Closeout Rear LH/RH; Bracket Upper Bed; Bumpstops Bed Cargo Tub; Damper Reinforcement Assembly Bed; X-Member Bed; Lower Tub Crossmember | Cierres y refuerzos de la caja | 2 + — | Caja | — | — | Lower Tub Crossmember 2 pernos 13 mm 36 Nm | S/E | V | `SM-Fittings12`, `SM-RMotorMount` |
| EXT-076 | Bed Tiedown Assembly Fore LH/RH; Forged Bed Tiedown Assembly | Anclajes de carga | 2 + — | Caja | Forjado (un tipo) | — | — | S/E | V | `SM-Fittings12` |
| EXT-077 | Lid Bed Cargo Tub; Seal Bed Cargo Tub; Under Bed Storage Assembly; Strut Bed Cargo Tub | Tapa, junta, almacenamiento bajo caja y amortiguador | 1 c/u | Caja inferior | — | Compartimento 97 L / 3,4 ft³, límite 220 lb (OM) | — | S/E | V | `SM-Fittings12`, `SM-Tonneau1120` |
| EXT-078 | Door-Outlet-Bed; Bed Outlet Assembly | Puerta y módulo de tomas de la caja | 1 + 1 | Caja | — | 2 × 120 V + 1 × 240 V (OM) | 2 tornillos T25R 1,5 Nm + 1 perno 10 mm 10 Nm; 3 conectores con bloqueo | S/E | V | `SM-BedOutlet` |
| EXT-079 | Bed Light LH/RH (dos variantes) | Luz de la caja | 2 | Pared lateral | — | — | 3 pernos T20 2,5 Nm; 4 fijaciones pared inferior 10 mm 11 Nm; 1 conector; 8 clips de pared superior | S/E | V | `SM-BedLight` |

#### 3.1.4 Tonneau (cubierta de caja motorizada, de serie en AWD y Cyberbeast según Wikipedia, R)

El SM la describe como sistema de motores + cadena + lamas (Chain Link, Cam Block). El número de lamas **no figura** en las notas.

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-090 | Tonneau Motor Assembly LH/RH | Motor de la cubierta | 2 | Tras la pared inferior de la caja | — | — | 2 pernos 10 mm 11 Nm por motor; 1 conector | Std | V (LH) / A (RH†) | `SM-TonneauMotor` |
| EXT-091 | Flat Cassette Assembly LH/RH | Casete plano | 2 | Caja | — | — | Motor 2 pernos 10 mm 11 Nm; lower tonneau 1 tuerca 10 mm 6 + 1 perno 10 mm 6 + 1 perno 13 mm 20; soporte 2 tuercas + 1 perno 13 mm 30; 8 tornillos de brazo T30 5 Nm; 8 tornillos de travesaño T25 5 Nm; aplique 2 pernos T30 9 Nm | S/E | V | `SM-FlatCassette` |
| EXT-092 | Horizon Rail Assembly LH/RH; Tonneau Horizontal Rail LH/RH; Tonneau Rail LH/RH (post 4-nov-2024) | Carriles de la cubierta | 2 + 2 + 2 | Caja | — | — | Rail: 9 pernos 10 mm 9 Nm; corner bracket 1 perno 9 Nm; Horizon Rail (LR): 9 fijaciones (4 × 8 mm + 5 × 10 mm) 10 Nm | fecha / LR | V | `SM-TonneauRail`, `SM-HorizonRail` |
| EXT-093 | Slat System - Tonneau (Mid Slat, Sealing Slat, Bushing Slat and Seal) | Sistema de lamas | n.º de lamas no indicado | Caja | — | Holgura de 2 mm entre datum deslizante y extremo del raíl | Topes: 3 pernos 10 mm 9 Nm por lado; marco de transferencia 8 fijaciones (PN 1999662-00-A) | S/E | V | `SM-SlatSystem`, `SM-Tonneau1120` |
| EXT-094 | Chain Link; Cam Block LH/RH; Deflector Clip LH/RH; Hinge Pivot Applique LH/RH; Corner Bracket LH/RH; Closeout Seal; Foam Datum Pad | Cadena, bloques de leva, clips, aplique de pivote, soportes y juntas | — | Caja | — | — | — | S/E | V (nombres) | `SM-Tonneau1120` |
| EXT-095 | Tonneau Lower Assembly (Standard); Tonneau Lower Assembly; Tonneau Applique; Applique Lower/Upper Tonneau | Conjunto inferior y apliques de la cubierta | 1 + — | Pared trasera de cabina | — | — | 2 pernos 13 mm 20 Nm; false wall 2 pernos 15 mm 45 + 4 tuercas 13 mm 30; soportes 4 tuercas + 2 pernos 13 mm 30; pilar A 1 perno 10 mm 6; cantrail 3 pernos T30 6; calibración ODIN PROC_EGGREAR1_TONNEAU-CALIBRATE | Std | V | `SM-TonneauLower` |
| EXT-096 | NVH Barrier Assembly (tonneau) | Barrera NVH | 1 | Casete | — | — | Antes de abr-2024: 11 × T25 5 Nm; después: 10 × 8 mm 5 Nm; después de oct-2024: pieza de 2 partes, 18 × Allen 4 mm 5 Nm | fecha | V | `SM-HVBattAWD`, `SM-FlatCassette` |
| EXT-097 | Water Management Seal Tonneau Center LH/RH | Junta de gestión de agua | 2 | Caja | — | — | 1 clip | S/E | V | `SM-Seals1170`, `SM-TonneauRail` |
| EXT-098 | Manual release (slats) | Liberación manual de lamas | 1 | Caja | — | — | — | S/E | V | `SM-Tonneau1120` |

#### 3.1.5 Vidrio, limpiaparabrisas y lavado

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-100 | Windshield Assembly (+ variante «w/ Off Road Lightbar») | Parabrisas | 1 | Frontal | Laminado (Rescue Sheet); calefactado | Cordón de uretano con boquilla 8 × 14 mm | Pegado con uretano (4 tubos + imprimación); 4 sellos de borde + 2 datums | S/E / Opc | V | `SM-Windshield`, `RS` |
| EXT-101 | Fixed Glass Roof Assembly; Roof glass rear edge seal; Edge Seal Rear Roof Glass | Techo de cristal fijo; juntas | 1 + 2 | Techo | Laminado | — | — | S/E | V | `SM-Glass1020`, `SM-Seals1170`, `RS` |
| EXT-102 | Fixed Backlite Glass | Luneta trasera | 1 | Cabina trasera | Templado (Rescue Sheet) | — | — | S/E | V | `SM-Glass1020`, `RS` |
| EXT-103 | Quarter Glass Front LH/RH; Seal Quarter Glass Front | Vidrio fijo delantero de cuarto | 2 + 2 | Pilar A | Templado | — | Estructura: Front Quarter Window Assembly (3.2) | S/E | V | `SM-Glass1020`, `RS` |
| EXT-104 | Glare shield; rubber separator strip (parabrisas) | Visera antideslumbrante; tira separadora | 1 + 1 | Parabrisas | — | — | Glare shield: 2 clips | S/E | V | `SM-Windshield` |
| EXT-105 | Motor - Wiper - Windshield | Motor del limpiaparabrisas (48 V, R) | 1 | Cowl | — | — | 3 pernos 13 mm 24 Nm; 1 conector; manguera en 2 clips; se desliza hacia delante | S/E | V | `SM-WiperMotor` |
| EXT-106 | Wiper Arm and Blade | Brazo y escobilla únicos | 1 | Cowl | Base fundida a presión (R) | Longitud: **62 in** ([Autopian](https://theautopian.com/if-you-were-a-fly-sitting-at-the-tip-of-the-tesla-cybertrucks-enormous-wiper-heres-how-fast-youd-be-traveling-when-it-wipes)), ~50 in de brazo ([InsideEVs](https://insideevs.com/news/718267/cybertruck-windshield-wiper-teardown/)), ~4 ft / 1,22 m ([Drive Tesla Canada](https://driveteslacanada.ca/?p=83026)) — **conflicto** (R); barrido ~90° | 1 tuerca 18 mm 45 Nm; herramienta PN 2004428-00-A; holgura brazo-carcasa **5,5 ± 1 mm** (`SM-WiperArm`) vs **3 ± 1 mm** (`SM-Windshield`) — conflicto | S/E | V / R | `SM-WiperArm`, `SM-Windshield` |
| EXT-107 | Washer Tank Assembly (+ cap, tank neck, level sensor, bomba) | Depósito del lavaparabrisas | 1 | Frunk | — | Capacidad no publicada | 3 pernos 10 mm 8 Nm; 2 clips de arnés; conectores de bomba y sensor | S/E | V | `SM-WasherTank`, `SM-Washer1750` |
| EXT-108 | Pump - Washer - Windshield; megabeam hose; wiper hose; camera nozzle hose | Bomba y mangueras | 1 + 3 | Frunk / Megabeam | — | — | Sin tornillos; 1 conector + 2 mangueras con clip | S/E | V | `SM-WasherPump`, `SM-Washer1750` |

#### 3.1.6 Iluminación exterior

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-110 | Headlamp Assembly LH/RH | Faro | 2 | Esquinas delanteras | — | — | 2 pernos 10 mm 5 Nm; 1 datum; 1 conector (no pulsar la pestaña); ajuste por método de pared; acceso retirando apron trasero, Frunk Assembly y aplique central | S/E | V | `SM-Headlamp` |
| EXT-111 | Lightbar Front | Barra de luz delantera | 1 | Powergate (se abre con el capó) | — | Longitud: no publicada | 2 tuercas 3 Nm + 2 pernos 4 Nm (10 mm); 3 clips; 3 datums; 1 conector | S/E | V | `SM-Lightbar` |
| EXT-112 | Tail Lamp Body Side LH/RH | Piloto lateral | 2 | Caja | — | — | 2 tornillos T30 5 Nm; 1 conector; datums; acceso retirando aplique de piloto y closeout de caja | S/E | V | `SM-TailLamp` |
| EXT-113 | Lamp - Tailgate | Luz del portón (barra trasera, A) | 1 | Portón | — | — | 8 pernos T30 5 Nm; 2 conectores; 2 clips | S/E | V | `SM-LampTailgate` |
| EXT-114 | Lamp - Reverse LH/RH; Lamp - Rear Marker LH/RH; Lamp - License Plate | Marcha atrás; posición trasera; matrícula | 2 + 2 + 1 | Trasera | — | — | Reverse 3 tornillos T25 5 Nm; marker 2 clips sin tornillos; plate lamp sin tornillos (pestaña) | S/E | V | `SM-ReverseLamp`, `SM-RearMarker`, `SM-LPLamp` |
| EXT-115 | Off-Road Lightbar (accesorio) | Barra de luz off-road | 1 | Techo/cabecera | — | — | Páginas no leídas | Opc | R | `SM-Windshield`, `SM-Index` |
| EXT-116 | Side repeaters | Repetidores laterales | 2 | Aleta | — | — | La función reside en la cámara de la aleta; sin procedimiento propio | S/E | R | `SM-1710`, `SM-FlareCam` |

#### 3.1.7 Bajos exteriores, protecciones y revestimientos de rueda

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-120 | Aeroshield Front | Escudo aerodinámico delantero | 1 | Bajos del. | — | — | **11** pernos 10 mm 6 Nm + Loctite 222 (SM exterior/FDU) vs **17** pernos (página de batería LR) — conflicto | S/E | V | `SM-AeroFront`, `SM-FDU`, `SM-HVBattLR` |
| EXT-121 | Aeroshield Rear | Escudo aerodinámico trasero | 1 | Bajos tras. | — | — | **7** pernos 6 Nm + Loctite 222 (página Aeroshield Rear) vs **5** pernos 10 mm + 2 guías 6 Nm (página RDU) — conflicto | S/E | V | `SM-AeroRear`, `SM-RDU-RI` |
| EXT-122 | Skid Plate (front) | Protector delantero | 1 | Bajos del. | — | — | **8 pernos + 4 clips a presión, 10 mm, 4 Nm; 8 pestañas** (`SM-SkidFront`) vs **8 tuercas 15 mm + 2 pernos 11 mm, 50 Nm** (FDU, batería, torque de bajos) — conflicto probable de dos piezas (Skid Plate / Skid Plate Stamping) | S/E | V | `SM-SkidFront`, `SM-FDU`, `SM-UnderbodyTorque` |
| EXT-123 | Skid Plate Rear (describe el mid aeroshield); Skid Plate Stamping | Protector central/trasero | 1 + 1 | Bajos | — | — | 3 pernos 15 mm 70 Nm, 3 pernos 13 mm 28 Nm, 2 pernos 10 mm 6 Nm, 6 clips (`SM-SkidRear`); la página RDU da 3 × 15 mm **42** Nm y 5 × 13 mm 28 Nm — conflicto | S/E | V | `SM-SkidRear`, `SM-RDU-RI` |
| EXT-124 | Rear Diffuser | Difusor trasero | 1 | Trasera | — | — | 14 pernos 6 Nm (6 × 10 mm + 8 × T30), 12 clips, 16 pestañas; soportes 6 pernos 13 mm 30 Nm | S/E | V | `SM-Diffuser`, `SM-RDU-RI` |
| EXT-125 | Wheel Liner Front LH/RH | Pasarruedas delantero | 2 | Pasos de rueda | — | — | 2 pernos 10 mm 6 Nm; 6 tuercas a presión; 1 + 14 clips | S/E | V | `SM-WheelLiner` |
| EXT-126 | Wheel Liner Rear LH/RH | Pasarruedas trasero | 2 | Pasos de rueda | — | — | 19 clips a presión + 5 tuercas a presión por lado (desechables) | S/E | V | `SM-ASMR` |
| EXT-127 | Aeroshield of rear lower control arm; LCA shield front | Deflector del brazo inferior | 4† | Brazos inferiores | — | — | 3 pernos 10 mm 7 Nm por unidad | S/E | V | `SM-ASMR`, `SM-SFF` |
| EXT-128 | Recovery Hook (front) – Pair | Gancho de recuperación delantero | 2 | Delante | — | — | 4 pernos 15 mm 78 Nm, nuevos en cada montaje | S/E | V | `SM-RecoveryHook` |

#### 3.1.8 Opciones y paquetes

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EXT-130 | Terrestrial Armor | Paquete de blindaje off-road | 1 juego | Umbrales y batería | — | Reduce la altura de chasis Medium de 265 a 250 mm | Faldón a portador 2 pernos 4 Nm; portador a faldón estructural 5 pernos 13 Nm; faldón a anillos de puerta 2 pernos 14 Nm; faldón a soportes 6 + 6 pernos EP10 13 Nm; faldón a bajos 5 pernos 28 Nm (el más delantero 15 mm más largo); armadura a ski de batería 4 pernos 15 mm 26 Nm; armadura a batería 4 del. + 5 tras. pernos 13 mm 28 Nm; 24 tuercas en U | Opc | V | `SM-TerrArmor` |

Accesorios documentados pero no desglosados: cubierta tonneau motorizada (patente US20210155086A1) y barra de luz. **No hay fuentes** en las notas sobre Cybertent, aletas guardabarros, rack Overland ni fundas.

#### 3.1.9 Piezas pequeñas y ocultas del exterior (sub-tabla)

| ID | Pieza | Nombre ES | Cant. | Ubicación | Dato | Conf. | Fuente |
|---|---|---|---|---|---|---|---|
| EXT-S01 | Sail applique clips | Clips del aplique de la vela | 17 por lado | Vela | + 1 datum + 1 clip de arnés + 1 conector + 1 perno de soporte de esquina (9 Nm) por lado | V | `SM-TonneauRail` |
| EXT-S02 | Front header trim clips | Clips de moldura de cabecera delantera | 19 | Cabecera | + 1 imán + 1 conector + 1 clip de arnés | V | `SM-Windshield`, `SM-Header` |
| EXT-S03 | Rear underhood apron clips | Clips del apron trasero | 9 | Cowl | — | V | `SM-Windshield`, `SM-CALR` |
| EXT-S04 | A-pillar trim clips | Clips de guarnecido de pilar A | 4 (delantero) + 1 guía; 8 (superior); 1 + 3 pestañas (medio), por lado | Pilar A | — | V | `SM-Windshield` |
| EXT-S05 | Wheel liner push clips/nuts | Clips y tuercas a presión del liner | Delantero 1 + 14 + 6; trasero 19 clips + 5 tuercas | Pasos de rueda | — | V | `SM-PowergateHood`, `SM-ASMR` |
| EXT-S06 | Lightbar clips/datums | Clips y datums de la barra de luz | 3 clips + 3 datums | Powergate | — | V | `SM-Lightbar` |
| EXT-S07 | Headlamp, tail lamp datums | Datums de faro y piloto | 1 (faro); varios (piloto) | Lámparas | — | V | `SM-Headlamp`, `SM-TailLamp` |
| EXT-S08 | Skid plate tabs/clips | Pestañas y clips del protector | 8 pestañas + 4 clips | Bajos | — | V | `SM-SkidFront` |
| EXT-S09 | Mirror retaining plugs, door panel plug | Tapones de retención del retrovisor | 3 + 1 | Puerta | PN tornillo 1857466-00-B | V | `SM-Mirror` |
| EXT-S10 | Windshield edge seals, datums, separator strip | Sellos de borde, datums y tira separadora | 4 + 2 + 1 | Parabrisas | Uretano: 4 tubos | V | `SM-Windshield` |
| EXT-S11 | Fender flare cover clips | Clips de la cubierta de aleta (cámara) | 11 clips + 3 datums | Aleta | — | V | `SM-FlareCam` |
| EXT-S12 | A-pillar harness grommet; door check strap bolt | Pasamuros de arnés en pilar A | 1 por puerta | Pilar A | — | V | `SM-FrontDoor` |
| EXT-S13 | Frunk bolt caps and bumpstops | Tapas de pernos y topes del frunk | 2 + 2 | Frunk | — | V | `SM-HoseHV`, `SM-Pentaport` |
| EXT-S14 | Tonneau deflector clips, foam datum pad, NVH barrier, closeout seal, water-management seal clip | Clips y juntas de la cubierta | — | Caja | — | V (nombres) | `SM-Tonneau1120`, `SM-TonneauRail` |
| EXT-S15 | Hitch trailer connector socket + harness clips; trailer ECU; rear center bracket | Toma de remolque y soporte central | 1 + 1 + 1 | Trasera | — | V | `SM-TowHitch` |
| EXT-S16 | Tow hitch bolts | Pernos del enganche | 6 × 18 mm 198 Nm (nuevos) + 4 × 15 mm 44 Nm + 2 × 13 mm 16 Nm = 12 | Casting trasero | 178 Nm en `SM-RearEA` — conflicto | V | `SM-TowHitch`, `SM-RearEA` |

Pendientes ocultos sin fuente (A, no documentados en el SM leído): tapones/grommets de drenaje de caja y frunk, botas de arnés del portón, tornillos de matrícula, boquilla del lavacámara, antenas, almohadillas adhesivas de emblemas, clips de burlete, líneas de lavado, actuador y luz de la toma de carga. «Badges and Films» no tiene procedimientos publicados.

---
### 3.2 Estructura de carrocería

**Qué dicen las fuentes.** El CR (Collision Repair Manual, © Tesla 2026) lista ~55 procedimientos de piezas estructurales con cantidades de remaches/tornillos de repuesto, pares y números de pieza de tornillería; **no da material ni cotas de control en texto** (están en imágenes). La carrocería es un «exoesqueleto» de piel de acero inoxidable pegada sobre una estructura interior ([Repairer Driven News](https://www.repairerdrivennews.com/2019/11/22/tesla-cybertruck-uses-stainless-steel-exoskeleton-rather-than-traditional-body-on-frame/), R); según Munro hay un body-in-white interior de acero con pilares A y B de acero al boro, una gran fundición delantera y fundiciones traseras ([LeanDesign/Munro](https://leandesign.com/cybertruck-structural-design-analysis/), R, de segunda mano).

#### 3.2.1 Materiales y reglas de reparación (CR, V)

| Material | Dato | Fuente |
|---|---|---|
| Categorías de la estructura | Aluminio 6xxx; aluminio extruido; aluminio fundido; acero suave; acero de alta resistencia (HSS); acero de ultra alta resistencia (UHSS); acero inoxidable | `CR-MatAllowed` |
| Aluminio 6xxx | Límite elástico 230-280 MPa; calor máx. 100 °C; soldadura GMA solo en paneles ≤1,2 mm; orificios hasta 12 mm en cierres (puertas, capó, portón) y 8 mm en Body Side Outer | `CR-MatAllowed` |
| Acero suave / HSS / UHSS | Tracción <270 MPa / 300-700 MPa / >800 MPa; calor máx. 650 °C (90 s, 2 veces); UHSS: broca de carburo de tungsteno o boro, no reparable salvo guía | `CR-MatAllowed` |
| Acero inoxidable | Soldadura no permitida; solo refinado por lijado (lijadora orbital 6", órbita 3/16 in; se refina todo el plano) | `CR-MatAllowed`, `CR-Stainless` |
| Adhesivo | No calentar por encima de 100 °C | `CR-MatAllowed` |
| Pilares A, B, C (interior) | UHSS (Rescue Sheet); riel superior delantero HSS; paneles exteriores de inox | `RS` |
| Piel exterior | 1,8 mm puertas y 1,4 mm resto (Wikipedia/Moravy, R) frente a ~3 mm (Musk/SAE, R) | [Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck) |
| Aro de puerta | Acero al boro estampado en caliente («el mayor de la industria») y mitad trasera en una sola fundición (R) | [Design News](https://www.designnews.com/automotive-engineering/video-tesla-s-head-of-vehicle-engineering-discusses-the-cybertruck-s-castings-and-stampings) |
| Fundiciones | «Cast»: Front Under Body, Rear Under Body, Mast, Tailgate Tower, Rear Energy Absorber Cast Bumper. Aleación no indicada; que sean aluminio es A | `CR-FUBcast`, `CR-RUBcast`, `CR-Mast`, `CR-TGTowerGuide` |
| Prensa de fundición | IDRA 9.000 t (Musk: carrocería trasera; otras fuentes: delantera) (R, contradictorias) | [autoevolution](https://www.autoevolution.com/news/idra-s-9000-ton-giga-press-is-ready-to-cast-tesla-cybertruck-s-underbody-190206.html), [Tesla Oracle](https://www.teslaoracle.com/2022/06/03/idra-groups-9000-ton-giga-casting-machine-is-for-the-cybertruck-unibody-confirms-elon-musk/), [Tesmanian](https://www.tesmanian.com/blogs/tesmanian-blog/sla-cybertruck-to-be-manufactured-by-idras-9-000-ton-giga-press) |

Técnicas de unión: adhesivo estructural + remaches estructurales de 6,5 mm (HS) / flow-form (S08-S68) + tornillos; soldadura por puntos (STRS), GMA, plug y butt joint solo en piezas de acero concretas.

#### 3.2.2 Estructura delantera

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EST-001 | Front Under Body (Complete) — «ASY FRONT UNDER BODY COMPLETE» | Fundición delantera | 1 | Delante | Fundición (aleación no indicada) | Orificio de acceso Ø29 mm en el centro | 30 remaches HS 6,5 mm + 4 flow-form S18; 8 tornillos M12x35 (1089657-00) y 2 M10x33 (1851387-00) a 90 Nm; 10 M12x43 (1882229-00) a 67 Nm; 2 tapones 1870761-00; adhesivo | S/E | V | `CR-FUB` |
| EST-002 | Front Under Body (Small Section) | Sección pequeña de la fundición delantera | 1 | Delante | — | Holgura máx. 3 mm; clips de arnés 48 mm (nueva) / 60 mm (original) | 7 remaches de brida 6,5 mm; 2 tornillos HF M10-1,5x41 (1622577-00) a 64 Nm; 1 M8x28 (1112247-00) a 28 Nm; 4 plantillas de corte PN 2031072-00 (ext. LH), 2031073-00 (int. LH), 2031074-00 (ext. RH), 2031075-00 (int. RH) | S/E | V | `CR-FUBsmall` |
| EST-003 | Dash Reinforcement Assembly; Front Body Bridge Reinforcement Assembly | Refuerzos del salpicadero y del puente delantero | 1 + 1 | Mamparo | — | — | Se suministran con el FUB Complete: 61 remaches HS + 4 flow-form S18 + 2 M12x35 + 10 M12x43 (par no dado); Front Body Bridge (izq. 18 / der. 20 remaches HS, 4 FF, 1 M12x35, 5 M12x43) | S/E | V (Dash) / gap (Bridge, 403) | `CR-Dash`, `CR-FBBR` |
| EST-004 | Front Drive Unit Mount (Left / Right) | Soporte de la unidad motriz delantera | 2 | Delante | — | — | 3 tornillos HHL M10x41 (1623242-00) 65 Nm + adhesivo | S/E | V (LH) / A (RH†) | `CR-FDUMountL`, `CR-FDUMountR` |
| EST-005 | Fender Beam LH/RH | Viga superior de aleta | 2 | Aletas | — | — | 3 tornillos HF M8x28 (1112247-00) 28 Nm por lado; Loctite en tornillos de ajuste | S/E | V | `CR-FenderBeam` |
| EST-006 | Bumper Beam Mount | Soporte de la viga del paragolpes | 1 por lado (A) | Delante | — | — | 3 tornillos HF M8x28 21 Nm + adhesivo | S/E | V | `CR-BumperBeamMount` |
| EST-007 | Dash to FUB Gutter Connector | Conector de canaleta salpicadero-fundición | 1 | Mamparo | — | — | 8 remaches de 4,8 mm + adhesivo | S/E | V | `CR-Gutter` |
| EST-008 | CFM Bracket | Soporte del módulo de ventiladores | 1 | Delante | — | — | 2 remaches HS 6,5 mm + adhesivo | S/E | V | `CR-CFMBracket` |
| EST-009 | Front Energy Absorber / Front Bumper Beam Assembly («Front Inner Panels - Megabeam»; FRT 0,48) | Viga de impacto delantera con absorbedores | 1 | Delante | — | Material no indicado | 4 tuercas 13 mm 30 Nm (SM); sin procedimiento de reparación en CR | S/E | V | `SM-BumperBeam`, `CR-Gutter` |
| EST-010 | Megabeam («Front Inner Panels - Megabeam») | Megabeam (travesaño delantero de equipos térmicos) | 1 | Delante | — | — | 8 pernos al vehículo (EP14 18 Nm y 21 mm 165 Nm; sin desglose); supermanifold 2 pernos 15 mm 33 Nm | S/E | V | `SM-Megabeam` |
| EST-011 | Support Bracket Center and LH/RH Front Energy Absorber | Soportes del absorbedor delantero | 1 + 2 | Delante | — | — | — | S/E | V | `SM-Bumper1001` |
| EST-012 | Super Cowl Assembly; Supercarrier Assembly; Aerobracket Assembly | Super Cowl; viga transversal del salpicadero (A); soporte aero | 1 c/u | Salpicadero | — | — | Citados como adyacentes en el CR | S/E | V (nombres) / A («supercarrier» = viga del IP) | `CR-FUB`, `SM-IP` |
| EST-013 | Front Quarter Window Assembly (Complete / Outer) | Conjunto del vidrio fijo delantero de cuarto | 2 | Pilar A | — | — | 8 remaches HS + 3 avellanados 4,8 + 2 FF S18 + 1 tornillo M12x35 70 Nm; soldadura por puntos (Outer: no leída) | S/E | V (Complete) / gap (Outer) | `CR-FQW`, `CR-FQWOuter` |

#### 3.2.3 Laterales, pilares y umbral

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EST-020 | Body Side (Complete) — «ASY FRONT BODY COMPLETE» | Lateral de carrocería completo | 2 | Laterales | — (inox exterior, UHSS interior según RS) | Cotas de remache C=49, D=13 mm | 46 remaches HS; 5 avellanados 4,8 cortos + 2 largos; FF S08x1, S18x6, S28x1, S48x1, S58x1; 4 M12x35 + 4 M10x35 + 5 M12x43; 3 tapones; soldadura por puntos; 90 / 90 / 67 Nm | S/E | V | `CR-BodySide` |
| EST-021 | Body Side Outer | Panel exterior lateral | 2 | Laterales | — (regla Al 6xxx: orificios hasta 8 mm) | — | 17 remaches HS; 1 avellanado corto + 2 largos 4,8; FF S08x1, S18x5, S28x1, S48x1, S58x1; 4 M12x35 90 Nm; soldadura por puntos | S/E | V | `CR-BSO` |
| EST-022 | C-Pillar Inner | Pilar C interior | 2 | Pilar C | — | Cotas A=49, B=19, C=64, D=12, E=6, F=8 mm | 33 remaches HS; 2 tornillos M10x33 90 Nm | S/E | V | `CR-CPillarInner` |
| EST-023 | C-Pillar Lower Nut Plate | Placa de tuercas inferior del pilar C | 2 | Pilar C | — | — | 1 avellanado 4,8 corto + adhesivo | S/E | V | `CR-CPillarNut` |
| EST-024 | Cantrail Stud Plate (delantera y trasera) | Placa de espárragos del larguero de techo | 2+ | Cantrail | — | — | 1 avellanado estructural 6,5 mm | S/E | V | `CR-CantrailStud` |
| EST-025 | Cantrail Trim Bracket | Soporte de moldura de cantrail | 2 | Cantrail | — | — | Soldadura por puntos + adhesivo | S/E | V | `CR-CantrailTrimBkt` |
| EST-026 | HV Battery Support Bracket | Soporte de la batería HV | 2 | Laterales | — (piezas de acero, A) | Cotas A=24 mm (remache), B=26 mm (punto de soldadura) | 22 remaches HS; soldadura por puntos; adhesivo | S/E | V | `CR-HVBracket` |
| EST-027 | IP Beam Bracket | Soporte de la viga del salpicadero | 2 | Salpicadero | — | Soldadura de tapón Ø10 mm | 6 remaches HS o soldadura de tapón; GMA permitida | S/E | V | `CR-IPBeamBkt` |
| EST-028 | Power Gate Strut Mount | Soporte del amortiguador del Powergate | 2 | Powergate | — | — | 3 remaches de brida 6,5 mm | S/E | V | `CR-PGStrutMount` |
| EST-029 | Rocker Support Bracket | Soporte del umbral | 4 por vehículo (según listado) | Umbrales | — | — | 12 remaches de 4,8 mm cada uno (páginas: 403 en CR; dato de lista de piezas de la ronda 2) | S/E | gap (403) / V (lista) | `CR-RockerSupport` |
| EST-030 | Sail Panel Bracket (Upper) | Soporte superior del panel de la vela | 2 | Vela | — | — | 3 remaches HS | S/E | V | `CR-SailPanelBkt` |
| EST-031 | Side Sill Insert («ASY SIDE SILL EXTRUSION») | Inserto extruido del umbral | 2 | Umbrales | Extrusión (aluminio, A) | — | 4 remaches 4,8 mm; 2 tornillos M10x33 90 Nm; 2 HF M8-1,25x25 (1008571-00) 26 Nm; adhesivo; «XM Bash Plates» remachadas 4,8 o soldadas | S/E | V | `CR-SideSill` |

#### 3.2.4 Inferior trasero, caja y torres

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EST-040 | Rear Under Body (Complete) — «ASY REAR UNDERBODY» | Fundición trasera | 1 | Trasera | Fundición (el resumen de la herramienta dijo «steel»: errata probable, A) | Orificio Ø29 mm; punto de acceso 155 mm (+5 mm si marca 150) | 10 remaches HS; 6 tornillos M10x33 90 Nm; 4 tapones; adhesivo | S/E | V | `CR-RUB` |
| EST-041 | Rear Under Body (Section): Half Section + Top Stamping + Bottom Stamping | Media sección trasera + estampaciones superior e inferior | 1 + 1 + 1 | Trasera | — | Holgura máx. 3 mm | 13 remaches HS + 4 de brida; 3 tornillos M10x33; 2 tapones | S/E | V | `CR-RUBsection` |
| EST-042 | Rear Under Body (Frame Rail Section): Rear Rail Casting + Rear Rail Section Backing Plate | Larguero trasero fundido + placa trasera | 1 + 1 | Trasera | Fundición | 19 cotas A-S (23, 40, 129, 27, 73, 31, 20, 62, 22, 18, 29, 72, 46, 70, 160, 17, 66, 19, 10 mm); el significado de cada letra está en la figura | 15 remaches de brida 6,5 mm; adhesivo | S/E | V (valores) / gap (significado) | `CR-RUBrail` |
| EST-043 | Mast Assembly (Complete) — «ASY MAST CASTING» | Mástil fundido | 2 (A) | Caja | Fundición | — | 19 remaches HS; 1 tornillo T2K HHN 10x38 (1893805-00) 27 Nm; adhesivo; SPR de fábrica | S/E | V | `CR-MastAsm` |
| EST-044 | Mast Assembly (Section) + 4 placas de refuerzo (Top, Top Middle, Bottom Middle, Bottom Backing Plate) | Sección del mástil | 1 | Caja | — | Holgura máx. 3 mm | 13 remaches HS | S/E | V | `CR-MastSect` |
| EST-045 | Tailgate Tower; Tailgate Tower Support Plate | Torre del portón; placa de soporte | 2 + 2 | Caja trasera | Fundición (torre; implícito por su guía de reparación) | — | Torre: 7 remaches HS + adhesivo; placa: 5 avellanados 4,8 largos | S/E | V | `CR-TGTower`, `CR-TGTowerPlate` |
| EST-046 | Rear Wheel Arch — «ASY WHEELHOUSE ARCH»; Rear Wheel Arch (Rear Section); Rear Wheel Arch Extension (Front) | Paso de rueda trasero y extensión | 2 + 2 + 2 | Trasera | — | Cotas A=90, B=185, C=11, D=246, E=62 mm | Arch: 4 remaches HS + 5 de 4,8 + 2 avellanados largos; Extension: 6 remaches 4,8 + adhesivo; Rear Section: gap | S/E | V / gap | `CR-RWArch`, `CR-RWArchRear`, `CR-RWArchExt` |
| EST-047 | Bed Bridge Bracket — «ASY REAR BED BRIDGE BRKT»; Rear Fascia Bracket | Soporte puente de caja; soporte de fascia trasera | 1-2; 2 | Caja | — | — | 3 remaches HS cada uno | S/E | V | `CR-BedBridge`, `CR-RFasciaBkt` |
| EST-048 | Sail Datum Bracket | Soporte de datum de la vela | — (se retira, no se repone) | Vela | — | Cotas A=105, B=195, C=78, D=53 mm | 2 Band Edge Clip 1518812-00 + 2 bridas 1015391-00 | S/E | V | `CR-SailDatum` |
| EST-049 | Tie-Down Nut Plate (Rear) — «ASY REAR TIEDOWN NUT PLATE» | Placa de tuercas del anclaje trasero | 2+ | Caja | — | — | 1 avellanado estructural 6,5 mm | S/E | V | `CR-TiedownPlate` |
| EST-050 | Rear Energy Absorber, Cast Bumper Assembly LH/RH; Rear Energy Absorber Center Bracket | Parachoques trasero fundido con absorbedor | 2 + 1 | Trasera | Fundición (nombre «cast», A) | — | 2 pernos 18 mm 90 Nm por lado; enganche 6 pernos 18 mm **178 Nm** aquí frente a 198 Nm en Tow Hitch | S/E | V | `SM-RearEA`, `SM-TowHitch` |
| EST-051 | Tow Hitch | Enganche de remolque (receptor de 2 in) | 1 | Trasera | — | Remolque 11.000 lb (CB/AWD) | 6 pernos 18 mm 198 Nm (nuevos) + 4 pernos 15 mm 44 Nm + 2 pernos 13 mm 16 Nm | S/E | V | `SM-TowHitch` |

#### 3.2.5 Pared trasera y cabecera de techo

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| EST-060 | Rear Wall Assembly — «ASY REAR WALL COMPLETE» | Pared trasera de la cabina | 1 | Cabina trasera | — | Cotas A=49, B=13 mm | 48 remaches HS + 38 FF S18 + 2 FF S28; 2 tornillos T2K 10x38 (1893805-00) 37 Nm; adhesivo; Ramp Bracket C-Pillar | S/E | V | `CR-RearWall` |
| EST-061 | Rear Wall Lower Crossmember Glove | Funda del travesaño inferior | 1 | Cabina | — | A=13, B=6, C=50 mm | 24 remaches HS | S/E | V | `CR-RWLowerGlove` |
| EST-062 | Rear Wall Upper Crossmember Glove | Funda del travesaño superior | 1 | Cabina | — | A=69, B=31 mm | 11 remaches HS + 3 FF S18 + 2 FF S38 + 1 tornillo 10x38 27 Nm | S/E | V | `CR-RWUpperGlove` |
| EST-063 | Rear Seat Stanchion; Rear Seat Stanchion Brace(s) | Montante y riostras del asiento trasero | 2 + 2 | Cabina | — | — | Stanchion 7 remaches HS + 1 de 4,8; brace 6 HS (trasero) + 2 de 4,8 (delantero) | S/E | V | `CR-Stanchion`, `CR-StanchionBrace` |
| EST-064 | Tonneau Attachment Bracket (Lower / Upper) | Soportes de fijación de la cubierta | 2 + 2 | Pared trasera | — | Lower A=31, B=12, C=23, D=96; Upper A=17 mm | Lower 1 HS + 1 avellanado corto + 1 largo 4,8; Upper 3 HS + 1 de 4,8 | S/E | V | `CR-TonneauBktL`, `CR-TonneauBktU` |
| EST-065 | Front Header Upper / Lower / Gusset | Cabecera delantera superior, inferior y cartelas | 1 + 1 + 2 | Techo | Acero (soldadura por puntos, A) | Cartela A=17, B=14 mm | Upper: 4 avellanados 4,8 largos + 12 FF S18; Gusset: 5 avellanados 4,8 cortos + 2 FF S18; soldadura por puntos; adhesivo | S/E | V | `CR-HdrFU`, `CR-HdrFL`, `CR-HdrGusset` |
| EST-066 | Rear Header Lower («REAR WALL HEADER INNER») / Upper | Cabecera trasera inferior y superior | 1 + 1 | Techo | — | — | Lower: 6 remaches HS o 20 FF S18; Upper: 32 FF S18 | S/E | V | `CR-HdrRL`, `CR-HdrRU` |

#### 3.2.6 Tornillería, adhesivos y sellantes del CR (V)

Fuente: `CR-Fasteners`, `CR-FlowForm`, `CR-Chemicals`.

| Familia | PN / especificación |
|---|---|
| Remache 4,8 mm | 1028719-00-A |
| Remache estructural 6,5 mm | corto 1028408-00-A; medio 1062559-00-A; largo 1028409-00-A; alta resistencia 1454538-00-A; pop 5/32 in aluminio 1003668-00-C |
| Avellanados | 4,8 corto 1069308-00-A o 2046255-00-A; 4,8 largo estructural 1069326-00-A; 6,5 estructural 1069327-00-A; bulb 6,5 mm (paneles ≤4,5 mm) 1063943-00-A; brida 6,5 mm 1062558-00-A; brida alta resistencia 1116094-00-A; estructural 8 mm 1058710-00-A |
| SPR Ø5 | 5x4 1026936-00-A; 5x4,5 1026938-00-A; 5x5 1026939-00-A; 5x6 H4 1026940-00-A; 5x6 H2 1026941-00-A; 5x6,5 1026942-00-A; 5x7 1026943-00-A; 5x8 SKR 1026944-00-A; 5x8 SK 1026945-00-A; 5x9 1028629-00-A |
| Flow-form (cuerpo Ø8 mm, taladro Ø8 mm) | S08 1,3-2,5 mm 1069328-00-A; S18 2,3-3,5 1069329; S28 3,35-4,10 1069330; S38 4,0-5,15 1069331; S48 5,0-6,1 1069332; S58 6,0-7,2 1069333; S68 7,1-8,3 1069334. Remachadoras: XPress 800 y TKR PNP 90 a 60 kN; ProSpot PR-5 y Böllhoff HTF 50 a 50 kN |
| Otros | BOM 5/16 in 1062555-00-A; NeoBolt 3/4 in corto 1599680-00-A / largo 1599681-00-A (collar 1599682-00-A); NeoBolt 5/8 in 1599677-00-A (collar 1599679-00-A); AV Bolt 5/8 in 1600794-00; pin y collar 1/4 in 1062557-00-A, 5/16 in 1062556-00-A |
| Tornillos estructurales recurrentes | HF M12x35 1089657-00; HHL M10x33/M10x35 1851387-00; HHL M12x43 1882229-00; HF M8x28 1112247-00; HHL M10x41 1623242-00; HF M10-1,5x41 1622577-00; T2K HHN 10x38 1893805-00; HF M8-1,25x25 1008571-00; tapón de acceso 1870761-00 |
| Refuerzo de fundiciones | Placa 1076938-E0-B (adhesivo, sin soldar); espárrago doble autorroscante 1463292-00-C (5 Nm) |
| Adhesivo estructural | DuPont BETAMATE 2098 (Crash Durable); Parker LORD Fusor 2098 (Norteamérica); 3M 07333 |
| Sellantes | 3M 08308 (insonorizante); uretanos 3M 08360/08361/08362/08364/08365/08367/08368; epoxi 3M 08528/08522; Henkel MS 9120/9320 SF; LORD Fusor 122 EZ/123 SL/123 Medium/123 Fast; LORD Fusor 231 |
| Espumas | LORD Fusor 121/124 (flexible), 130 (acústica rígida); 3M 08463; SEM 39357; Wurth 089391070 |
| Otros químicos | Cera de cavidades 3M 08852/38854; antigravilla 3M 08889, Henkel WT R2000/S3000, SEM 52000; imprimación de soldadura 3M 05917; adhesivos de luna DuPont Betaseal Express+ (Norteamérica), Betaprime 5504G |

#### 3.2.7 Límites de reparación de las fundiciones (útiles para saber zonas críticas)

| Pieza | Regla | Fuente |
|---|---|---|
| Front Under Body fundido | Zonas azul (pestañas, soldables), verde (hasta 50 mm), amarillo (hasta 30 mm sin placa; 30-50 mm con placa 1076938-E0-B; >50 mm consultar a Tesla), naranja (hasta 30 mm con placa), rojo (sin reparación); arañazos <5 mm lijables; alma doblada restaurable en frío dentro de 1,5 mm; taladro de espárrago Ø5,5 x 22 mm | `CR-FUBcast` |
| Rear Under Body fundido | Mismos umbrales 30/50 mm, zonas rosa/cian/etc., «spring pocket» (arañazos <1 mm lijables), espárrago Ø5,5 x 12 mm | `CR-RUBcast` |
| Mast; Tailgate Tower | Mismos umbrales; la torre admite grietas hasta 30 mm con placa | `CR-Mast`, `CR-TGTowerGuide` |
| Seccionado | No cortar a <25 mm del centro de un taladro de tornillo; sin cortar paneles subyacentes; las uniones a tope solo se sueldan por GMA si lo indica el procedimiento | `CR-Sectioning` |
| Tracción con bancada | Tesla no admite tirar ni empujar de componentes con bancada de estirado | `CR-Structural` |

#### 3.2.8 Datos de prensa sobre la estructura (R)

- Los pilares A y B son de acero al boro bajo la piel inox; los paneles inox van pegados, no remachados ni soldados ([LeanDesign/Munro](https://leandesign.com/cybertruck-structural-design-analysis/)).
- Subchasis (cuna) trasero Cyberbeast: aloja el módulo motriz con dos motores, inversores y la cremallera de dirección trasera; se baja sin los brazos superiores traseros, que van a la gran fundición trasera, no a la cuna ([The Autopian](https://theautopian.com/latest-cybertruck-teardown-reveals-teslas-odd-sway-bar-decisions-clever-packaging)).
- Prelanzamiento: la zona trasera se compone de ~5 grandes piezas (una fundición inferior de caja y cuatro laterales) ([InsideEVs](https://insideevs.com/news/670702/tesla-cybertruck-rear-castings-spotted/), baja confianza); probablemente corresponden a Mast ×2 + Tailgate Tower ×2 + Rear Under Body (A).
- Pack estructural: puntos de fijación desde paneles de cabina hasta caja y umbrales ([LeanDesign/Munro](https://leandesign.com/?p=2995), baja). Extricación: cabina, pilares, umbrales y largueros de acero; fundiciones de aluminio; sin bastidor de acero ([Boron Extrication](https://boronextrication.com/2024/04/23/tesla-cybertruck-body-structure/), no accesible).
- Moravy: no contó las piezas; estima un 20-30 % menos que un vehículo anterior sin contar celdas ([Design News](https://www.designnews.com/automotive-engineering/video-tesla-s-head-of-vehicle-engineering-discusses-the-cybertruck-s-castings-and-stampings)). Cableado: −2/3 de cable transversal frente al Model 3 y +50 % de puntos finales ([Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck)).
- Peso del body-in-white, de las fundiciones y dimensiones L×A×H de las fundiciones: no publicados.

#### 3.2.9 Piezas pequeñas y ocultas de la estructura (sub-tabla)

| ID | Pieza | Nombre ES | Cant. | Dato | Conf. | Fuente |
|---|---|---|---|---|---|---|
| EST-S01 | Access-hole plug 1870761-00 | Tapón de taladro de acceso (Ø29 mm) | 2 (FUB) / 4 (RUB) / 3 (Body Side) / 2 (RUB sección) | Con sellante en la cara inferior | V | `CR-FUB`, `CR-RUB`, `CR-BodySide` |
| EST-S02 | Reinforcement plate 1076938-E0-B | Placa de refuerzo de fundición | según daño | Pegada, sin soldar | V | `CR-FUBcast` |
| EST-S03 | Double-ended self-tapping stud 1463292-00-C | Espárrago autorroscante | según reparación | 5 Nm; taladro Ø5,5 mm | V | `CR-FUBcast` |
| EST-S04 | Band Edge Clip 1518812-00; cable tie 1015391-00 | Clip de borde y brida de cable | 2 + 2 | Sail Datum Bracket | V | `CR-SailDatum` |
| EST-S05 | Cutting templates 2031072/73/74/75-00 | Plantillas de corte | 4 | FUB Small Section | V | `CR-FUBsmall` |
| EST-S06 | XM Bash Plates | Placas de protección del umbral | — | Remachadas 4,8 o soldadas | V (nombre) | `CR-SideSill` |
| EST-S07 | Ramp Bracket - C-Pillar | Soporte de rampa del pilar C | — | Citado en Rear Wall | V (nombre) | `CR-RearWall` |
| EST-S08 | NVH Pad (general) y NVH Pad - Rear Wall; Dash Absorber | Almohadillas NVH | — | Espesor/ubicación no publicados | V (nombre) | `CR-FUB`, `SM-BodyPanels1010` |
| EST-S09 | HV chinstrap | Correa delantera de la batería | 1 | Liner RH: 2 pernos 6 Nm; correa a masa 1 perno 10 Nm | V | `SM-PowergateHood`, `SM-FDU` |

Faltan, sin fuente: protectores de torre de suspensión, almohadillas NVH dimensionadas, barras antivuelco, puntos de anclaje de asientos delanteros, gomas de cavidades.

---

### 3.3 Chasis: suspensión, dirección, frenos y ruedas

**Qué dicen las fuentes.** El SM indexa un procedimiento por módulo (alineación 3100, suspensión delantera 3101, trasera 3103, aire 3110, dirección 3201/3205, frenos 3301-3325, ruedas 3401-3404). Hay cantidades y pares abundantes, **sin dimensiones, material, casquillos, rodamientos ni números de pieza**. Suspensión de Cyberbeast y AWD: independiente de doble horquilla, muelle neumático coaxial adaptativo; el LR usa muelles helicoidales, llantas de acero de 18" y hubs delanteros no motrices (A para los nombres «Long Range»).

#### 3.3.1 Suspensión delantera

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-001 | Control Arm - Lower - Front LH/RH | Brazo inferior delantero | 2 | Subchasis → mangueta | — | Largo (Munro: «brazos inferiores más largos», R) | Al subchasis: 2 pernos 21 mm 175 Nm + 1 perno 24 mm 300 Nm (nuevos); a mangueta: tuerca 24 mm 190 Nm (nueva; tabla dice reutilizar, pasos dicen descartar); 3 pernos de escudo 10 mm 7 Nm | Std + LR | V | `SM-LCAF`, `SM-LCAF-LR` |
| CHS-002 | Control Arm - Upper - Front LH/RH | Brazo superior delantero | 2 | Carrocería → mangueta | — | — | A mangueta: tuerca 18 mm **80 Nm** (UCAF, halfshaft) vs **85 Nm** (FDU) — conflicto; a carrocería: 4 tuercas 15 mm 50 Nm (pasos dicen 3); sensor de altura: 1 tuerca 15 mm 50 Nm | S/E | V | `SM-UCAF`, `SM-FDU`, `SM-HalfshaftFL` |
| CHS-003 | Ball joints delanteros (outer) UCA/LCA | Rótulas del brazo | 4 | Mangueta | — | — | No hay procedimiento de rótula delantera: posible remachada al brazo (A) | S/E | A | `SM-UCAF` |
| CHS-004 | Knuckle - Front (LR y estándar) | Mangueta delantera | 2 | Delante | — | — | Tirante de dirección tuerca 21 mm 170 Nm; pinza 2 pernos 24 mm 315 Nm; soporte latiguillo 1 perno 10 mm 10 Nm; 2 clips de arnés; 6 tuercas de rueda 205 Nm | S/E | V | `SM-KNF` |
| CHS-005 | Driven Hub - Front; Non-Driven Hub - Front (LR) | Buje delantero motriz / no motriz | 2 | Delante | — | — | Perno central de semieje 24 mm 300 Nm (sin tuerca de eje); el buje trasero sí tiene 4 pernos a 105 Nm (CHS-023), el delantero no figura | S/E / LR | V (nombre) | `SM-Index`, `SM-KNF` |
| CHS-006 | Halfshafts - LH and RH - Front | Semiejes delanteros | 2 | Delante | — | — | Perno central 300 Nm, siempre nuevo; circlip «click» en la FDU | S/E | V | `SM-HalfshaftFL`, `SM-HalfshaftsFront` |
| CHS-007 | Module - Air Spring - Front LH/RH | Módulo de muelle neumático delantero | 2 | Delante | — | Vástago, fuelle y amortiguador adaptativo no desglosados | 3 tuercas 18 mm 105 Nm al vehículo (nuevas); 2 pernos 21 mm 140 Nm al brazo inferior (reutilizables); racor de aire VOSS 14 mm 8 Nm (nuevo); 2 conectores; 2 clips de arnés; 4 clips de cubierta | CB/AWD | V | `SM-ASMF` |
| CHS-008 | Coil Spring Assembly - Front (LR y estándar) | Muelle helicoidal delantero | 2 | Variante LR | — | — | Se comprime con 2 abrazaderas | LR | V | `SM-Index` |
| CHS-009 | Stabilizer Bar - Front; Link - Stabilizer Bar - Front | Barra estabilizadora y bieletas | 1 + 2 | Subchasis | — | — | Bieletas 275 Nm 21 mm (contrasujeción; otra versión PN «-00-C»: 210 ± 10 Nm solo el perno superior); 4 pernos «ankle catcher» 18 mm 110 Nm; sin datos de casquillos | S/E | V | `SM-SBF`, `SM-LCAF` |
| CHS-010 | Subframe - Front (AWD) | Subchasis delantero | 1 | Delante | — | — | 8 pernos principales: 2 × 24 mm 220 Nm, 2 × 21 mm 220 Nm, 4 × 24 mm con espárrago 215 Nm; travesaño delantero 2 pernos 18 mm 90 Nm; soportes de la unidad 2 pernos 18 mm 110 Nm; CFM 2 + 2 pernos 10 mm 10 Nm | AWD | V | `SM-SFF`, `SM-FDU` |
| CHS-011 | Front ride height sensor (LH) | Sensor de altura delantero | 2† | Brazo superior | — | — | 1 tuerca 15 mm 50 Nm (nueva); 1 conector; rótula de varilla en el UCA | S/E | V | `SM-RideHF`, `SM-UCAF` |
| CHS-012 | Aeroshield / LCA shield front | Deflector del brazo inferior | 2 | Brazo inferior | — | — | 3 pernos 10 mm 7 Nm | S/E | V | `SM-SFF` |

#### 3.3.2 Suspensión trasera y subchasis trasero

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-020 | Control Arm - Upper - Rear LH/RH | Brazo superior trasero | 2 | Fundición trasera → mangueta | — | — | Mangueta: tuerca 21 mm 150 Nm (nueva; fijar en Medium); carrocería: 4 fijaciones 27 mm 350 Nm (tabla: pernos; pasos: tuercas); tirante a actuador 180 Nm; línea de freno 1 perno 10 mm 10 Nm | S/E | V | `SM-UCAR` |
| CHS-021 | Control Arm - Lower - Rear LH/RH | Brazo inferior trasero | 2 | Subchasis | — | — | 4 pernos 21 mm 185 Nm (reutilizables); hay que retirar la mangueta | S/E | V | `SM-LCAR` |
| CHS-022 | Knuckle - Rear; rear knuckle/hub and bearing/upper ball joint assembly; … lower ball joint assembly | Mangueta trasera con rótulas | 2 + 2 + 2 | Trasera | — | — | Las rótulas y el rodamiento son conjuntos reparables en la trasera | S/E | V | `SM-Index` |
| CHS-023 | Hub - Rear | Buje trasero | 2 | Trasera | — | — | 4 pernos 18 mm 105 Nm (reutilizables); perno de semieje 24 mm 300 Nm; sensor de rueda 1 perno T30 8 Nm; 2 clips; escudo con inserto de orientación | S/E | V | `SM-HUBR` |
| CHS-024 | Halfshaft rear LH/RH | Semieje trasero | 2 | Trasera | — | — | Perno 24 mm 300 Nm; unión al RDU mediante abrazadera en U con 2 tuercas de 10 mm | S/E | V | `SM-RHalfshaft`, `SM-RDU-RI` |
| CHS-025 | Module - Air Spring - Rear LH/RH | Módulo de muelle neumático trasero | 2 | Trasera | — | — | 3 tuercas 18 mm 70 Nm (nuevas); 2 tuercas 21 mm 140 Nm (nuevas; nylon-lock o cinch moleteada); racor 14 mm 2 Nm; 2 conectores + 2 clips; escudo de brazo 3 pernos 7 Nm | CB/AWD | V | `SM-ASMR` |
| CHS-026 | Stabilizer Bar - Rear; Link - Stabilizer Bar - Rear | Barra estabilizadora trasera y bieletas | 1 + 2 | Subchasis trasero | — | Orientación: extremos por encima de los soportes | 4 pernos 15 mm 50 Nm (`SM-SBR`) vs 6 pernos 15 mm 50 Nm incl. bieletas (subchasis) — conflicto; abrazaderas de banda sobre aislantes (modelo del repo) | S/E | V | `SM-SBR`, `SM-Subframe-R-TM` |
| CHS-027 | Toe Link - Rear LH/RH | Tirante de convergencia trasero | 2 | Actuador → mangueta | — | — | Mangueta: tuerca 21 mm 170 Nm nylon-lock nueva; actuador: perno 18 mm 180 Nm; rótula con contrasujeción | S/E | V | `SM-ToeLink`, `SM-SAR` |
| CHS-028 | Subframe - Rear (Tri Motor) | Subchasis trasero Tri Motor | 1 | Trasera | — | Procedimiento marcado DRAFT; 3,84 h | A carrocería: 4 pernos 24 mm 355 Nm + 3 clavijas de posicionado; motor trasero: 4 tuercas 18 mm 85 Nm + 2 tuercas 21 mm 115 Nm; brazos 4 pernos 21 mm 185 Nm por lado; arnés HV del RDU 4 pernos 10 mm 12 Nm; masa 1 perno 10 mm 10 Nm | TM | V | `SM-Subframe-R-TM` |
| CHS-029 | Subframe - Rear (Dual Motor) | Subchasis trasero Dual Motor | — | Trasera | — | — | Comparte los pernos de carrocería (355 Nm) | DM | V | `SM-Subframe-R-DM`, `SM-UnderbodyTorque` |
| CHS-030 | Rear ride height sensor (LH) | Sensor de altura trasero | 2† | Cerca del actuador/subchasis | — | Referencia de altura: 31,8 cm (espárrago de pasarrueda a soporte de la bieleta, Medium) | 1 tuerca 27 mm 350 Nm; 1 conector | S/E | V | `SM-RideHR`, `SM-SAR` |
| CHS-031 | Coil Spring Assembly - Rear (LR) | Muelle helicoidal trasero | 2 | Variante LR | — | — | — | LR | V | `SM-Index` |
| CHS-032 | Rear suspension aeroshield | Escudo aerodinámico del brazo inferior trasero | 2 | Brazo inferior | — | — | 3 pernos 10 mm 7 Nm | S/E | V | `SM-ASMR` |

#### 3.3.3 Sistema de aire (3110, «TAS»)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-040 | Compressor - Air Suspension | Compresor de la suspensión neumática | 1 | Bajo el suelo de la caja | — | — | Soporte al cuerpo 3 tuercas 13 mm 12 Nm; soporte al compresor 3 tornillos T30 5,5 Nm; línea de aire 3 Nm; fijación 12 mm 4 Nm (cantidad no indicada); 3 conectores; 4 clips; escape separado | S/E | V | `SM-CMP` |
| CHS-041 | Compressor carrier bracket; air compressor exhaust assembly | Soporte del compresor y escape | 1 + 1 | Caja inferior | — | — | Escape: collar a presión | S/E | V | `SM-CMP` |
| CHS-042 | Reservoir - Air Suspension («pressurize pack») | Depósito de aire | 1 | Bajo el suelo de la caja | — | Presión ~16 bar; volumen no publicado | 2 tuercas 13 mm 33 Nm; 4 líneas con 4 racores VOSS (3, 5 o 7 Nm según página); 1 perno 10 mm 5 Nm al bloque; 2 clips «fir-tree»; 1 brida; 1 conector | S/E | V | `SM-RSV` |
| CHS-043 | Valve Block - Air Suspension | Bloque de válvulas | 1 | Caja inferior | — | — | Sin tornillos: 3 grommets de goma (2 giran al soporte); 5 líneas VOSS codificadas por color; 1 conector | S/E | V | `SM-VB` |
| CHS-044 | SCUBA valve block assembly; Fill port; Pressurize pack lines | Bloque SCUBA, puerto de llenado y líneas del pack | 1 + 1 + 2 | Pack/caja | — | — | Racores VOSS 12 mm 8 Nm | S/E | V (nombres) | `SM-SCUBA`, `SM-HVBattAWD` |
| CHS-045 | Airline bundles LH / RH / Rear; Airline inlet valve block | Haces de líneas de aire | 3 + 1 | Carrocería | — | — | Entrada al bloque: VOSS 4 Nm | S/E | V | `SM-AIN`, `SM-Index` |
| CHS-046 | VOSS fittings (sistema de aire) | Racores VOSS | ≥15 (A) | Varias | — | — | 2-8 Nm | S/E | V (par) / A (nº) | `SM-RSV`, `SM-AIN` |

#### 3.3.4 Dirección (steer-by-wire en las 4 ruedas)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-050 | Steering Actuator - Front | Actuador de dirección delantero (cremallera con motores) | 1 | Subchasis delantero | — | Doble motor (Munro, R) | 2 pernos al subchasis 175 Nm (cabeza 18/19/21 mm según fecha de fabricación); 4 conectores con bloqueo; hay que vaciar el refrigerante antes | S/E | V | `SM-SAF`, `SM-SFF` |
| CHS-051 | Tie Rod - Inner - Front LH; Tie Rod - Outer - Front LH | Bieletas de dirección interior y exterior | 2 + 2 | Cremallera → mangueta | — | — | Interior: 105 Nm (llave de pie de 38 mm); contratuerca exterior 90 Nm (24 mm); tuerca a mangueta 170 Nm | S/E | R (resumen de buscador) | `SM-TRI` |
| CHS-052 | Steering Actuator - Rear / Steering Gear - Rear (Standard y Long Range) | Actuador/cremallera trasera | 1 | Subchasis trasero | — | Ángulo máx. 3° (R, futuro 10°); sin cifra primaria | 4 pernos 18 mm 120 Nm (2 por lado); tirante 180 Nm; conector; 2 clips «fir-tree» | TM/DM/LR | V | `SM-SAR`, `SM-SteerGearRear` |
| CHS-053 | Steering Feedback Actuator | Actuador de realimentación del volante | 1 | Columna tras el IP | — | — | 3 pernos 13 mm 20 Nm; 2 tornillos prisioneros de 3 mm 7 Nm (con fijador); columna 4 tuercas 13 mm 18 Nm; 3 conectores del IP + 2 del actuador; calibración PROC_X_SBW-FIND-CENTER-AND-COMMISSION | S/E | V | `SM-SFA` |
| CHS-054 | Harness - Steering Jumper; Harness - Jumper - Rear Steer (Long Range) | Mazos de dirección | 1 + 1 | Columna / trasera | — | — | — | S/E / LR | V (nombres) | `SM-SteerJumper`, `SM-RearSteerJumperLR` |
| CHS-055 | Position sensors/ECU de dirección | Sensores de posición (triple) y controladores | n.q. | Actuadores | — | — | Redundancia triple y doble alimentación | S/E | R | [Basenor SBW](https://www.basenor.com/blogs/news/how-cybertrucks-steer-by-wire-and-rear-steering-work) |

Los componentes de columna y volante (SCCM, volante, airbag, carcasas) están en 3.5 (interior).

#### 3.3.5 Frenos

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-060 | Brake Caliper Front LH/RH | Pinza delantera fija de 4 pistones | 2 | Delante | — | Ø de pistón no publicado | 2 pernos 24 mm 315 Nm a la mangueta; tornillo hueco del latiguillo 11 mm 42 Nm; perno de soporte 10 Nm; kits de bota, muelles y purgador | S/E | V | `SM-CALF` |
| CHS-061 | Brake Caliper Rear LH/RH (con EPB) | Pinza trasera flotante de 1 pistón con freno de estacionamiento | 2 | Trasera | — | — | 2 pernos 21 mm 150 Nm; tornillo hueco 42 Nm; perno de deslizamiento 14 mm 40 Nm; 2 pastillas + 2 muelles de retorno; conector EPB con bloqueo; servicio PROC_EPBL_START-SERVICE-MODE | S/E | V | `SM-CALR` |
| CHS-062 | Brake Rotor Front / Rear | Disco ventilado delantero / trasero | 2 + 2 | Ruedas | — | Ø351 mm (13,8 in) / Ø356 mm (14 in); espesor nuevo/límite 32/30 mm del., 23/21 mm tras. | Sin tornillo de retención (trasero) | S/E | V | `SM-BRK`, `SM-ROTR` |
| CHS-063 | Front pad kit / Rear pad kit | Pastillas | 4 + 4 | Pinzas | — | Material nuevo/límite: 10/3 mm del., 11/2 mm tras. | — | S/E | V | `SM-BRK` |
| CHS-064 | Brake Hose Front / Rear | Latiguillos | 2 + 2 | Mangueta / UCA → pinza | — | — | Perno del soporte 10 Nm; trasero: perno al UCA 10 Nm | S/E | V | `SM-CALF`, `SM-UCAR` |
| CHS-065 | Brake pipe assembly front; Brake tube pipe assembly LH; HCU brake pipe assembly | Tuberías rígidas | 1 + 1 + 1 | Carrocería | — | — | — | S/E | V (nombres) | `SM-Index` |
| CHS-066 | Hydraulic Control Unit (HCU) + HCU bracket assembly | Unidad hidráulica ABS/ESC y soporte | 1 + 1 | Frunk/mamparo (A) | — | — | La fijación LH de la FDU pasa por el agujero del soporte de la HCU | S/E | V (nombre) / A (ubicación) | `SM-Index`, `SM-FDU` |
| CHS-067 | Brake booster assembly (electromecánico); remote reservoir; remote reservoir tube | Servofreno electromecánico, depósito remoto y tubo | 1 + 1 + 1 | Frunk | — | Líquido DOT 4 BASF Hydraulan 404, 1.190 mL | Perno del depósito a la Megabeam 10 mm 8 Nm | S/E | V | `SM-Index`, `SM-ASMF`, `SM-FluidCap` |
| CHS-068 | Brake pedal (option); Accelerator pedal; Pedal support bracket | Pedales y soporte | 1 + 1 + 1 | Cabina | — | — | Acelerador: 2 tuercas 13 mm 10 Nm (página de batería AWD) | S/E | V | `SM-Index`, `SM-HVBattAWD` |
| CHS-069 | Wheel speed sensor front / rear | Sensor de velocidad de rueda | 2 + 2 | Mangueta | — | — | Delantero: sin fijación listada; trasero: 1 perno T30 8 Nm | S/E | V | `SM-KNF`, `SM-HUBR` |
| CHS-070 | Front brake shield; rear brake shield | Protectores de disco | 2 + 2 | Mangueta | — | — | — | S/E | V (nombre) | `SM-Index` |
| CHS-071 | Caliper bleed screws (front kit, rear); pad return springs; caliper boots | Purgadores, muelles y botas | 2 + 2 | Pinzas | — | — | — | S/E | V (nombres) | `SM-Index`, `SM-CALR` |

#### 3.3.6 Ruedas y neumáticos

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| CHS-080 | Wheel (20 x 9.0J ET58.5 / 18 x 9.0J ET58.5) | Llanta | 4 | Ruedas | — | 35,2 lb (R); patrón 6x139,7, buje 84 mm (R) | 6 tuercas 21 mm 205 Nm | Todas | V | `OM-Wheel`, `SM-Wheel` |
| CHS-081 | Steel Wheel (Long Range) | Llanta de acero | 4 | Variante LR | Acero | — | — | LR | V (nombre) | `SM-Index` |
| CHS-082 | Tire 285/65R20 (AS), LT285/65R20 Pirelli Scorpion ATR (AT), 285/70R18 Goodyear Wrangler Territory RT/HT | Neumático | 4 | Ruedas | — | Pirelli ATR 285/65R20 116H XL: profundidad de dibujo 12/32 in (TireSize) o 10/32 in (Discount Tire); ~45-46 lb; carga máx. 2.756-2.760 lb; presión máx. 50-51 psi; Ø ~878,5 mm (A) | — | Todas | V (medida) / R (resto) | `OM-Wheel`, [TireSize](https://tiresize.com/tires/Pirelli/Scorpion-ATR-285-65R20.htm), [Discount Tire](https://www.discounttire.com/buy-tires/pirelli-scorpion-atr/p/180908) |
| CHS-083 | Wheel Cover (con mounting ring); Wheel Cap (LR) | Tapacubos aerodinámico y tapa central | 4 + 4 | Ruedas | — | Patente de diseño D980147 (concedida mar-2023, presentada 21-nov-2019) | Retención por clips con anillo de montaje; ~4 lb el tapacubos (R) | Todas / LR | V (nombre) / R | `SM-Wheel`, [InsideEVs](https://insideevs.com/news/656332/tesla-cybertuck-wheel-cover-patent/) |
| CHS-084 | TPMS sensor | Sensor TPMS | 4 | Ruedas | — | Dos tipos: morado (original) y negro (actualizado, 2025-02-06) | Tuerca 11 mm 8 Nm; núcleo de válvula a mano; rodillo superior ~100 mm por delante del vástago | fecha | V | `SM-TPMS` |
| CHS-085 | Wheel studs | Espárragos de rueda | 24 | Bujes | — | M14x1,5 (R, [Unplugged](https://unpluggedperformance.com/cybertruck/wheel-and-tire-guide/)) | — | Todas | A / R | — |
| CHS-086 | Lug nuts | Tuercas de rueda | 24 | Ruedas | — | — | 21 mm 205 Nm | Todas | V | `OM-Wheel` |
| CHS-087 | Valve stems; balance weights | Válvulas y contrapesos | 4 + juegos | Ruedas | — | — | — | Todas | A | — |
| CHS-088 | Spare tire | Rueda de repuesto | 0 | — | — | — | El OM tiene una página «Installing a Spare Tire» pero no hay repuesto de serie (A) | — | A | [OM spare](https://www.tesla.cn/ownersmanual/cybertruck/en_ae/GUID-C482029E-58E5-47A8-A748-8265A502A57C.html) |

#### 3.3.7 Piezas pequeñas y ocultas del chasis (sub-tabla)

| ID | Pieza | Cant. | Dato | Conf. | Fuente |
|---|---|---|---|---|---|
| CHS-S01 | Pasarruedas trasero: clips a presión + tuercas a presión | 19 + 5 por lado | Desechables | V | `SM-ASMR` |
| CHS-S02 | Cubierta del módulo de muelle delantero | 4 clips por módulo | — | V | `SM-ASMF` |
| CHS-S03 | Clips de arnés del módulo delantero / trasero | 2 + 2 por módulo | — | V | `SM-ASMF`, `SM-ASMR` |
| CHS-S04 | Clips de arnés puente en mangueta delantera | 2 | — | V | `SM-KNF` |
| CHS-S05 | Clips de arnés del sensor de rueda trasero | 2 | — | V | `SM-HUBR` |
| CHS-S06 | Clips «fir-tree» y brida del depósito de aire | 2 + 1 | — | V | `SM-RSV` |
| CHS-S07 | Grommets del bloque de válvulas | 3 | — | V | `SM-VB` |
| CHS-S08 | Inserto de orientación del escudo del buje trasero | 1 por buje | — | V | `SM-HUBR` |
| CHS-S09 | Rótula de varilla del sensor de altura | 1 por sensor | — | V | `SM-UCAF` |
| CHS-S10 | Clavijas de posicionado del subchasis trasero | 3 | — | V | `SM-Subframe-R-TM` |
| CHS-S11 | Tuercas nylon-lock o moleteadas de la brida del módulo trasero | 2 por módulo | — | V | `SM-ASMR` |
| CHS-S12 | Tornillos de pinza, de latiguillo (tornillo hueco), deslizadores | ver CHS-060/061 | — | V | `SM-CALF`, `SM-CALR` |
| CHS-S13 | Cinta de masa del subchasis | 1 | 1 perno 10 mm 10 Nm | V | `SM-Subframe-R-TM` |

Probables, sin fuente (A): casquillos de brazos y estabilizadora, topes de rebote, asientos de muelle, fuelles de rótulas y de semiejes, pasadores de tuercas de bieletas, abrazaderas P de tubos de freno, pasadores y botas de deslizamiento de pinza, tapas de sensores.

---
### 3.4 Tren motriz, batería de alta tensión y gestión térmica

**Advertencia de variante.** Cyberbeast = Tri Motor: 1 motor delantero de imanes permanentes (PMSM) + 2 motores traseros de inducción, reducción fija 15,02:1 (`OM-Subsystems`, V). Las páginas del SM leídas son de «Front Drive Unit» (sin variante), «Rear Drive Unit (Dual Motor)», batería «Long Range» y «AWD», y PCS «Long Range». Las páginas Tri Motor (RDU LH/RH, inversores LH/RH, bomba de aceite LH, arnés HV LH/RH) **existen en el índice pero no se leyeron**. Por tanto, el par de apriete trasero que sigue es de Dual Motor y solo se supone aplicable al Cyberbeast (A).

#### 3.4.1 Unidades motrices

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| TRN-001 | Front Drive Unit (FDU) | Unidad motriz delantera | 1 | Subchasis delantero | Carcasa fundida (R) | **Masa no publicada** en ninguna página; izado con eslinga de 3 ganchos | Soporte gearcase 2 pernos 18 mm 110 Nm; perno RH E18 (o 16 mm temprano) 85 Nm; perno LH E18 85 Nm (pasa por el agujero del soporte de la HCU); arnés HV 1 perno 10 mm 10 Nm | S/E | V | `SM-FDU` |
| TRN-002 | Front motor (PMSM) | Motor síncrono de imanes permanentes delantero | 1 | FDU | Imanes monobloque (no segmentados); estátor de horquillas («hairpin»); placa de aluminio parcial en el rotor | kW por motor: no publicado | — | CB | V (tipo, OM) / R (detalles, [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)) | `OM-Subsystems` |
| TRN-003 | Front inverter | Inversor delantero integrado | 1 | Extremo del tren de engranajes | — | — | — | S/E | R / V (título en índice) | Autopian, `SM-Index` |
| TRN-004 | Front gearset / gearcase | Reductor delantero (15,02:1) con embrague electromagnético de bloqueo | 1 | FDU | Carcasa fundida con pasador que sujeta la pista exterior de rodamientos | — | — | S/E | R | Autopian |
| TRN-005 | Front electric oil pump | Bomba de aceite eléctrica delantera | 1 | FDU | Junta tórica verde | — | 2 pernos External Torx Plus EP10 5 Nm + 20°; tapón de llenado 8 mm Allen 15 Nm; fluido KAF1; cubierta acústica RH: 2 clips inferiores + 2 a la FDU | S/E | V | `SM-FOilPump` |
| TRN-006 | Heat exchanger (FDU oil cooler) | Intercambiador de aceite de la FDU | 1 | FDU | — | — | 2 pernos EP10 5 Nm; tapón de llenado Allen 8 mm 15 Nm; clips de resorte 2 (mangueras FDU) + 1 (entrada radiador) + 1 (radiador-manifold) | S/E | V | `SM-FHeatEx` |
| TRN-007 | Front gearbox fluid | Aceite del reductor delantero (KAF1) | — | FDU | KAF1; no mezclar | Llenar hasta rebosar; si se añaden >500 mL (una nota anterior decía 300 mL) diagnosticar | Tapones de llenado y vaciado 15 Nm (Allen 8 mm); el vaciado está «en desarrollo», solo reposición | S/E | V | `SM-FGearFluid` |
| TRN-008 | Oil filter FDU / RDU; breather housing; ground strap; output axle seal; NVH covers (inversor y motor); phase-out covers | Filtro, respiradero, trenza de masa, retén de salida, cubiertas NVH | — | FDU/RDU | — | — | Páginas no leídas | S/E | V (títulos) | `SM-FOilFilter`, `SM-ROilFilter` |
| TRN-009 | Rear Drive Unit (Dual Motor) | Unidad motriz trasera Dual Motor (caso de referencia) | 1 | Subchasis trasero | — | Masa no publicada | Subchasis a carrocería 4 pernos 24 mm 355 Nm; soporte gearcase 2 pernos 18 mm 110 Nm; fijación del RDU 2 pernos E18 85 Nm; cable HV del RDU 4 pernos 10 mm 4 Nm; el nuevo RDU llega prellenado de aceite | DM | V | `SM-RDU-RI`, `SM-RDU-RR` |
| TRN-010 | Rear motors LH/RH (inducción) | Motores traseros de inducción | 2 | Trasera | Rotor sin imanes; canales rectangulares en el rotor (¿refrigeración por aceite?, no confirmado); ejes de cabeza fría | — | — | CB | V (tipo, OM) / R (Autopian) | `OM-Subsystems` |
| TRN-011 | Rear inverters LH/RH (Tri-Motor) | Inversores traseros | 2 | Parte trasera de cada motor | — | — | Páginas Tri Motor no leídas | TM | R / V (título) | Autopian, `SM-Index` |
| TRN-012 | Rear motor mount / inverter mount (RH) | Soportes del motor trasero RH e inversor | 1 + 1 | Trasera | — | — | Soporte RH al subchasis 1 perno 16 mm o E18 85 Nm; inversor 3 × EP14 35 Nm + 55°; soporte a RDU 4 × E14 35 Nm + 55°; Lower Tub Crossmember 2 × 13 mm 36 Nm; cubierta acústica 5 clips; subchasis Revisión D sin masa NVH | S/E | V | `SM-RMotorMount` |
| TRN-013 | Rear electric oil pump (LH) | Bomba de aceite trasera | 1 | RDU LH | — | — | 2 pernos EP10 5 Nm + 20°; tapón de vaciado y llenado 8 mm Allen 15 Nm; cubierta acústica 3 clips inferiores + 2 al RDU; prueba ODIN TEST-SELF_DIF_X_OIL-PUMP-PRESSURE | S/E (existe página Tri Motor) | V | `SM-ROilPump`, `SM-ROilPumpTM` |
| TRN-014 | Halfshafts (4) | Semiejes | 4 | Ejes | — | — | Delantero: circlip click en la FDU, perno central 300 Nm; trasero: abrazadera en U con 2 tuercas 10 mm | S/E | V | `SM-HalfshaftFL`, `SM-RHalfshaft` |
| TRN-015 | HV harness FDU; HV harness RDU Dual Motor; HV harness RDU LH / RH Tri Motor | Arneses de alta tensión de las unidades | 1 + 1 + 2 | Pack → unidades | Aislamiento naranja | — | RDU DM: 4 pernos 10 mm 4 Nm | FDU: S/E; RDU TM: TM | V (títulos) | `SM-HVHarnessFDU`, `SM-HVHarnessRDU`, `SM-HVHarnessRDU-L`, `SM-HVHarnessRDU-R` |
| TRN-016 | Front/rear coolant hoses of drive units | Mangueras de refrigerante de las unidades | — | Subchasis | — | — | FDU supply inline, FDU inverter-to-heat-exchanger, RDU supply/return | S/E | V (títulos) | `SM-Index` |

Rendimiento declarado (R): 845 hp (621 kW), 10.296 lb·ft, 2,6 s 0-60 mph ([ArenaEV](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php)). Comunalidad (R, ingenieros de Tesla vía Munro): una sola pareja rotor/estátor PM, una de inducción, un diseño de inversor y un solo juego de engranajes para todas las variantes; el motor PM es muy parecido al del Model Y Performance ([Autopian](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)). Munro estima que el motor delantero cuesta tanto como los dos traseros juntos (opinión).

#### 3.4.2 Batería de alta tensión (pack)

Variante leída: «HV Battery (Long Range)» y «HV Battery (AWD)»; **página Cyberbeast/Tri Motor del pack: no leída** (existe «HV Battery (Standard)»). Fuentes de detalle interno: teardown de Munro vía Autopian (R).

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| TRN-020 | HV Battery (pack estructural) | Batería de alta tensión | 1 | Bajos de la cabina y la caja | Bandeja/tapa: material no publicado | 123 kWh; **masa y dimensiones exteriores no publicadas** (Wikipedia 1.590 lb / 720 kg, R); separación al suelo bajo las celdas ~1,3 in / 33 mm (R) | Mounts exteriores delanteros 6 × 18 mm 115 Nm; laterales 16 × 15 mm 62 Nm (remoción) / 60 Nm (montaje); al RUB 4 × 21 mm 119/115 Nm; interiores delanteros 3 × 24 mm 160 Nm por lado (6); interiores traseros 4 × 13 mm 60 Nm por lado (8); cinta de masa delantera 1 perno 10 mm 10 Nm; 4 varillas de alineación (2 grandes + 2 pequeñas); 4 adaptadores de elevación | LR y AWD | V | `SM-HVBattLR`, `SM-HVBattAWD` |
| TRN-021 | Cells 4680 | Celdas cilíndricas 4680 | ~1.344 | Pack | Celdas pegadas con espuma (cell-to-pack) | ~48 celdas de largo, 4 bloques, 7 de ancho (192S7P) o 224S6P (alternativa); 4,2 V lleno / 3,4 V vacío / 3,6 V nominal; ~91,5 Wh/celda; segunda generación («Cybercell»), lata más delgada, tapa soldada, sin pestañas | — | CB | R | [Autopian pack](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/), [InsideEVs passport](https://insideevs.com/news/724981/tesla-cybertruck-battery-passport-4680cell/), [Lean Design](https://leandesign.com/?p=3390), [Notebookcheck](https://www.notebookcheck.net/First-Cybertruck-4680-battery-teardown-shows-how-Tesla-managed-to-increase-its-energy-density.875816.0.html) |
| TRN-022 | Structural foam; mica sheet | Espuma estructural verde; lámina de mica | 1 + 1 | Pack | Espuma rígida; mica sobre el canal de ventilación | — | — | S/E | R | Autopian pack |
| TRN-023 | Cooling channel | Canal de refrigeración | 1 | Borde de filas | — | — | Un solo canal; «ribbon» no confirmado | S/E | R | Autopian pack |
| TRN-024 | Top vent (single-use); breather vent; flood ports | Respiradero superior de un solo uso (tapa naranja), respiradero y puertos de inundación | 1 + 1 + 2 | Pack/penthouse | Obleas apiladas que absorben humedad | — | — | S/E | R / V (flood port en índice 1630) | Autopian pack, `SM-1630` |
| TRN-025 | Pressurized pack line (Wade/Scuba) | Línea de presurización del pack | 1 | Compresor → pack | — | — | 2 racores VOSS 12 mm 8 Nm | S/E | R / V | Autopian pack, `SM-HVBattAWD` |
| TRN-026 | HV battery support brackets; chinstrap; internal beams | Soportes, correa delantera, vigas internas | — | Pack | — | — | Ver EST-026/EST-S09 | S/E | V / A | `CR-HVBracket` |
| TRN-027 | Seat track patch bolts; rocker covers; footwell cover; HV outlet to console panel; bed floor bolts | Fijaciones accesorias al desmontar el pack | — | Interior/caja | — | — | Patch de asiento 2 por carril T45P 34 Nm; footwell cover 1 perno 3 Nm; salida HV a consola 2 × T20 1 Nm; consola 4 + 2 pernos 10 mm 5 Nm; asientos 8 × 13 mm 40 Nm (AWD) | LR/AWD | V | `SM-HVBattLR`, `SM-HVBattAWD` |

Tensión nominal: **700 V (OM) vs 800 V (Rescue Sheet y Munro)**; el DPDT (interruptor de doble polo y doble tiro) conmuta dos bloques en serie (800 V) o paralelo (400 V) para el Supercharger (R, Baglino/Autopian). Cabezal HV del pack: no hay entrada de BMS en la sección 1630.

#### 3.4.3 Bahía auxiliar, PCS, fusibles y carga

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| TRN-030 | Power Conversion System (PCS) | Sistema de conversión de potencia (cargador y DC-DC, A) | 1 | Bahía auxiliar sobre el pack (A) | — | Masa y kW no publicados | 6 × E10 5 lóbulos 6 Nm; pigtail MV 1 × EP10 6 Nm; cabezal MV 2 × EP10 6 Nm; cubierta auxiliar 22 × E10 6 Nm; test de fuga de refrigerante 50 psi (Δ máx. 0,35 psi) | LR | V | `SM-PCS-LR`, `SM-PCS-RR` |
| TRN-031 | Primary pyro fuse; Secondary pyro fuse; Pyro access cover | Pirofusibles primario y secundario y cubierta | 1 + 1 + 1 | Bahía auxiliar | — | Sin valores eléctricos | 2 pernos 13 mm 5 Nm + 60° cada uno; cubierta 4 × E-Torx 5 lóbulos 10 Nm | S/E | V | `SM-Pyro` |
| TRN-032 | PCS fuse; HV compressor fuse; Fuse 60A 1000VDC Eaton EVK22-60-T (Ancillary); Fuse Littelfuse 828-30 | Fusibles | 1 c/u | Bahía auxiliar | — | 60 A / 1000 VDC (Eaton, por el título) | PCS y compresor HV 2 × 8 mm 6 Nm c/u; cabecera de baja tensión 2 × EP10 6 Nm; doblador de cabecera de carga rápida 2 × E10 10 Nm | LR / Std | V | `SM-Fuses`, `SM-AncFuse`, `SM-PCSFuse` |
| TRN-033 | Last Mile Busbar Assembly | Barra colectora «last mile» | 1 | Bahía auxiliar | Cobre/aluminio no indicado | — | 3 × 10 mm 10 Nm + 3 × T55 cautivos 5 Nm + 60°; cabeceras LHRDU/FDU/RHRDU 6 × 5 lóbulos 10 mm 10 Nm; cabecera 2x4 4 × 6 Nm; PCS a ancillary 6 × 8 mm cautivos 6 Nm; cluster 4 × Torx Plus 55 5 Nm + 60°; 4 × E10 6 Nm; refrigerante PCS 2 × EP10 6 Nm; coverbox 8 × T25 5 Nm | S/E | V | `SM-LastMile` |
| TRN-034 | Device cluster assembly; AC junction box (ACJB); shunt jumper harness; DC input header/busbar; contactor seize check; positive/negative DC inlet; ACJB-to-FC and ACJB-to-PCS HV harnesses | Clúster de dispositivos, caja de CA y arneses del pack | 1 c/u | Bahía auxiliar | — | — | — | LR / Std | V (títulos) | `SM-1630` |
| TRN-035 | Charge Port (NACS) busbar; charge port | Toma de carga NACS y barra | 1 | Cuarto trasero LH | — | Acero inox: advertencia de gripado | Puerto al cuerpo 2 × 10 mm 6 Nm; puerto a vela 1 perno 6,5 Nm; cable de masa 1 perno 6,5 Nm; kit de barra a cabecera HV 2 × 9 Nm; resistencia HV Hioki 0,050-0,195 mΩ | LR | V | `SM-ChgBus` |
| TRN-036 | Door - Charge Port; Charge Port Controller ECU (Gen 4); charge port voltage check | Puerta de la toma de carga y ECU | 1 + 1 + — | Cuarto trasero LH | — | — | Puerta 1 perno 10 mm 6 Nm, 1 conector; ECU 1 perno 8 mm 5 Nm + 3 conectores | Gen 4 | V | `SM-ChargeDoor`, `SM-ChgPortECU`, `SM-ChgVoltCheck` |
| TRN-037 | HV junction/connectors, joint paste | Juntas HV | — | Pack | — | — | Penetrox A-13, ~2 gotas por junta; Hioki 0,050-0,195 mΩ | S/E | V | `SM-HVBattLR` |

#### 3.4.4 Gestión térmica

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| TRN-040 | Supermanifold | Supermanifold (válvulas, bomba, enfriador, condensador) | 1 | Delante, sobre la Megabeam | — | — | 2 pernos 15 mm 33 Nm a la Megabeam + 2 pernos 33 Nm al vehículo; línea Penta 1 tuerca 13 mm 36 Nm; línea A/C 1 perno 13 mm 22 Nm; soporte 1 perno 10 mm 8 Nm; perno del depósito de frenos 8 Nm | S/E | V | `SM-HoseHV`, `SM-Pentaport`, `SM-FluidCap` |
| TRN-041 | Octovalve | Octovalve | 1 | Supermanifold | — | — | 4 × T25 7 Nm; 7 clips de resorte; 4 conectores; 5 arandelas en línea Penta + 2 en línea del compresor | S/E | V | `SM-Octovalve` |
| TRN-042 | Coolant pump (supermanifold) | Bomba de refrigerante | 1 | Supermanifold | — | Giro de purga 3.500-6.500 rpm (7.000 = bloqueo de aire) | 4 tornillos T20 2 Nm; 1 junta tórica; 1 conector | S/E | V | `SM-CoolPump`, `SM-CoolantDrain` |
| TRN-043 | Chiller | Enfriador (chiller) | 1 | Supermanifold | — | Pérdida >30 mL de aceite activa el artículo 353700 | 4 tuercas 8 mm 7 Nm; controlador 3 pernos 4 Nm; soporte de arnés 3 pernos 8 Nm; 9 conectores | S/E | V | `SM-Chiller` |
| TRN-044 | Liquid cooled condenser (LCCR) | Condensador refrigerado por líquido | 1 | Supermanifold | — | — | 4 tuercas 8 mm 7 Nm; 3 clips; 2 tapas de puerto A/C; requiere Heat Pump Commissioning | S/E | V | `SM-LCCR` |
| TRN-045 | A/C compressor | Compresor de A/C (eléctrico, HV) | 1 | Megabeam | — | Ejemplo del SM: ~7 kg en seco (A, cifra ilustrativa) | 3 pernos 10 mm 5 Nm; 2 tuercas 13 mm 22 Nm; trenza de masa 1 perno 10 mm 16 Nm (7 Nm en la página del supermanifold — conflicto); conector HV con bloqueo rojo y palanca negra; aceite POE RB100EV | S/E | V | `SM-ACComp`, `SM-Refrigerant`, `SM-Flush` |
| TRN-046 | Cooling Fan Module (CFM) LH/RH + radiador | Módulo de ventiladores y radiador | 2 módulos | Delante | — | Radiador con 1 entrada y 1 salida (clips de resorte) | Superior 4 × 10 mm 10 Nm; inferior 2 × 10 mm 10 Nm; travesaño 2 × 18 mm 90 Nm; arnés 5 clips + 1 grommet. Otras páginas: 2 + 2 pernos | S/E | V | `SM-CFM`, `SM-HoseHV` |
| TRN-047 | Hoses: battery supply/return, powertrain supply/bypass, chiller-to-battery (×2), radiator inlet/outlet, radiator-to-manifold, car computer coolant hoses (×2) + grommet | Mangueras de refrigerante | — | Supermanifold | — | — | Haz de batería: 2 clips + 2 edge clips; detrás de la FDU | S/E | V | `SM-HoseHV`, `SM-Pentaport` |
| TRN-048 | Penta HVAC line; A/C line assembly; Suction Discharge Lines; Schrader valves (2); A/C service ports (2) with caps | Líneas Penta y A/C, válvulas Schrader y puertos | 1 + 1 + 1 + 2 + 2 | Delante | — | — | Junta de arandelas lubricada con RB100EV | S/E | V | `SM-Pentaport` |
| TRN-049 | Coolant bottle; expansion valve coils/cores; desiccant; ACC/chiller/LCCR filters; check valves; powertrain pressure sensors (high/low); supermanifold controller | Botella de refrigerante y componentes del supermanifold (sección 1840, 20 procedimientos) | — | Supermanifold | — | Relleno al vacío 60-70 cmHg; nivel entre NOM y MAX; ≥15 L de contenedor | — | S/E | V (títulos) | `SM-Thermal-1840`, `SM-Pentaport` |

Datos de fluidos y térmica: refrigerante A/C R1234yf, carga 1.020 g, aceite POE RB100EV 250 g; descarga máx. 26 bar, aspiración mín. 1,15 bar; refrigerante de motor HTF-LS 50/50 (23,5 L Tri-Motor, 22,5 L Dual Motor); ~20 L se drenan por el lado de la batería HV (`SM-FluidCap`, `SM-Refrigerant`, `SM-CoolantDrain`, V). No existe procedimiento separado de radiador, condensador o bomba de batería en la sección 1830 (solo «Radiator Clean»). Gestión de la batería: sin entrada separada de convertidor DC-DC (integrado en el PCS, A).

---

### 3.5 Interior

**Nota de lectura.** Los nombres proceden de los índices del SM (V). Las cantidades «RH» son A salvo que se diga. Se leyó solo hasta ~100.000 de ~125.000 caracteres por página del SM y las figuras no son legibles. Los prefijos GUID (8 caracteres) se dan donde la nota original no recogió el GUID completo; se resuelven en el índice del SM. No hay cuadro de instrumentos separado (`SM-2107`, `OM-Touchscreen`).

#### 3.5.1 Salpicadero (1405)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-001 | Top Pad Assembly | Tapa superior del salpicadero | 1 | IP | — | — | — | S/E | V | `SM-IP/5DEA8399` |
| INT-002 | Super Cowl Assembly | Super cowl | 1 | Bajo parabrisas | — | — | — | S/E | V | `SM-IP/785E798B` |
| INT-003 | Supercarrier Assembly | Portador/viga del IP (A) | 1 | IP | — | — | — | S/E | V / A | `SM-IP/06350585` |
| INT-004 | Aerobracket Assembly | Soporte aero | 1 | IP | — | — | — | S/E | V | `SM-IP/17013F52` |
| INT-005 | Display Bracket LH (+RH†) | Soporte de la pantalla | 2 | IP | — | — | — | S/E | V / A | `SM-IP/3641449A` |
| INT-006 | Display Shroud | Marco de pantalla | 1 | IP | — | — | — | S/E | V | `SM-IP/F08480B2` |
| INT-007 | Downleg Bracket LH (+RH†) | Patas del IP | 2 | IP | — | — | — | S/E | V / A | `SM-IP/029B92DA` |
| INT-008 | Steering Column Bracket | Soporte de columna | 1 | IP | — | — | — | S/E | V | `SM-IP/5C1BFE82` |
| INT-009 | Mid Panel Assembly | Panel medio | 1 | IP | — | — | — | S/E | V | `SM-IP/2166115B` |
| INT-010 | Lower Assembly - Instrument Panel | Panel inferior (cubre airbags de rodilla y guantera) | 1 | IP | — | — | — | S/E | V | `SM-IP/08EBBA12` |
| INT-011 | Quarter Panel Assembly LH (+RH†) | Panel lateral del IP | 2 | IP | — | — | — | S/E | V / A | `SM-IP/5646B2F5` |
| INT-012 | Center Shroud Service Panel; Footwell Cover | Panel de servicio central; cubierta de zona de pies | 1 + 1 | IP | — | — | Cubierta de pies: 1 perno 3 Nm (al retirar pack) | S/E | V | `SM-IP/E86A9772`, `SM-IP/FCAC8D7A`, `SM-HVBattLR` |
| INT-013 | Glovebox Assembly | Guantera | 1 | IP | — | — | 5 tornillos T20 2 Nm; 1 clip EPP RH; 1 conector USB-A; 1 clip de arnés; 1 conector eléctrico | S/E | V | `SM-Glovebox` |
| INT-014 | Glovebox Puddle Lamp; Footwell Puddle Lamp | Luces de cortesía | 1 + 1+ | IP | — | — | — | S/E | V | `SM-IP/D2B8ADD4`, `SM-IP/292DB366` |
| INT-015 | Ethernet Diagnostic Module (RJ45) | Módulo de diagnóstico Ethernet | 1 | IP | — | — | — | S/E | V | `SM-IP/FC390461` |
| INT-016 | Airwave Module LH (+RH†); Airwave Panel Duct LH (+RH†) | Salida de aire continua «Airwave» | 2 + 2 | IP | — | — | — | S/E | V / A | `SM-IP/CE10436D`, `SM-IP/BB132E1D` |
| INT-017 | Defrost Panel; Demist Duct Driver; Demist Duct Front Passenger; Demist Duct Side Window LH (+RH†); Floor Duct Outboard LH (+RH†) | Desempañado y conductos | 1 + 1 + 1 + 2 + 2 | IP | — | — | — | S/E | V / A | `SM-IP/2BDFEC2F`, `SM-IP/EDD520DD`, `SM-IP/7A94A7F0`, `SM-IP/CCF65A98`, `SM-IP/C5ED2A07` |
| INT-018 | Instrument Panel Gap Hider; Lower Instrument Panel Gap Hider | Cubrejuntas del IP | 1 + 1 | IP | — | — | — | S/E | V | `SM-IP/D6045590`, `SM-IP/DA1168FD` |

#### 3.5.2 Pantallas, cámara de cabina y ordenador (21xx)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-020 | Touchscreen - Center Display Assembly | Pantalla táctil central | 1 | IP | — | **18,5"** (R: Dilawri, Top Gear, SlashGear; el OM no da tamaño) | — | S/E | V (pieza) / R (tamaño) | `SM-IP/F6BAB956`, [Dilawri](https://www.dilawri.ca/en/inventory/tesla/cybertruck/2024-tesla-cybertruck-id37546864), [Top Gear](https://www.topgear.com/car-reviews/tesla/cybertruck/interior), [SlashGear](https://www.slashgear.com/1275680/coolest-features-tesla-cybertruck-interior) |
| INT-021 | Touchscreen - Rear Display | Pantalla trasera | 1 | Consola trasera | — | **9,4"** (R) | Pantalla+Airwave a consola: 8 tornillos T20 5 Nm + 1 + 4 tornillos display-airwave; 2 clips; 5 conectores (1 coaxial azul); 2 clips de arnés | S/E | V (pieza) / R (tamaño) | `SM-RearDisplay` |
| INT-022 | Car Computer; Car Computer Drip Guard | Ordenador del coche y protector de goteo | 1 + 1 | IP (acceso por guantera/pilares) | — | Refrigerado por líquido | 1 perno + 3 tuercas + 1 perno de masa, 10 mm, 13 Nm; soporte antikick 13 Nm; 4 + 9 conectores; 2 mangueras de refrigerante; 2 clips del protector; 2 clips de arnés; alfombra RH 8 clips + 4 datums | S/E | V | `SM-CarComputer` |
| INT-023 | USB Drive (Dispose) | Unidad USB del sistema | 1 | — | — | — | — | S/E | V | `SM-IP/9E8C1FB9` |
| INT-024 | Telematics Control Unit (TCU) + Bracket | TCU y soporte | 1 + 1 | Soporte del cristal de techo (bajo la moldura de cabecera delantera) | — | — | 2 tornillos T25 3 Nm; 2 conectores; 4 clips al soporte del vidrio + 2 clips soporte-unidad | S/E | V | `SM-TCU` |
| INT-025 | FM/HD Tuner; FM Amplifier Antenna; GPS Antenna | Sintonizador y antenas | 1 c/u | Parabrisas | — | — | Antena GPS dentro del glare shield: 1 tornillo T10 0,8 Nm + 1 conector; antena FM: página «en desarrollo» | S/E | V | `SM-GPSAnt`, `SM-FMAnt` |
| INT-026 | Interior Camera | Cámara de cabina | 1 | Sobre el retrovisor interior (cubierta decorativa) | — | — | 2 tornillos T10 0,8 Nm; 1 clip de arnés | S/E | V | `SM-IntCam`, `OM-Cameras` |
| INT-027 | Radar - Cabin | Radar de cabina (presencia de ocupantes) | 1 | Bajo la moldura de cabecera delantera | — | — | 1 perno 10 mm 10 Nm; 1 conector; 1 clip | S/E | V | `SM-RadarCabin` |

#### 3.5.3 Volante y columna (steer-by-wire)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-030 | Steering Wheel (yoke/«squircle»); Steering Wheel PUR heated; Switch Bezel | Volante y bisel | 1 | Cabina | PUR calefactado | Tamaño no publicado | Botones capacitivos con háptica; sin palancas; rueda de desplazamiento L/R | S/E | V | `OM-SteeringWheel`, `SM-Index` |
| INT-031 | Steering Column Control Module (SCCM) | Módulo de control de columna | 1 | Columna | — | — | Conectores X0012-X0014 en Body Controller LH | S/E | V | `SM-IP/5ED2D89E` |
| INT-032 | Steering Wheel Harness; Steering Jumper Harness | Mazos del volante | 1 + 1 | Columna | — | — | — | S/E | V | `SM-IP/B917A880`, `SM-SteerJumper` |
| INT-033 | Upper Steering Wheel Shroud; Upper Column Shroud; Lower Column Shroud; Lower Column Shroud Clip | Carcasas | 3 + 1 | Columna | — | — | — | S/E | V | `SM-IP/1C10967F`, `SM-IP/2C90C2E8`, `SM-IP/A4BE610D`, `SM-IP/9BC969E9` |
| INT-034 | Driver Airbag | Airbag del conductor | 1 | Volante | — | — | 2 clips de resorte + 1 conector, sin tornillos | S/E | V | `SM-DriverAirbag` |
| INT-035 | Steering Feedback Actuator | (ver CHS-053) | 1 | Columna | — | — | — | S/E | V | `SM-SFA` |
| INT-036 | Accelerator Pedal; Brake Pedal - Option; Support Bracket - Accelerator Pedal | Pedales | 1 + 1 + 1 | Suelo | — | — | — | S/E | V | `SM-IP/18A00B65`, `SM-IP/0B91EB74`, `SM-IP/637FC840` |
| INT-037 | Gear selector | Selector de marcha | — | Pantalla + 4 botones P-R-N-D en la consola del techo; también las dos ruedas del volante | — | — | Sin palanca ni selector de columna (A) | S/E | V (OM) | `OM-Touchscreen` |

#### 3.5.4 Consola central (1519)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-040 | Center Console Assembly (Long Range / estándar) | Consola central | 1 | Entre asientos | — | — | 2 pernos traseros + 4 delanteros 10 mm 5 Nm; panel trasero 10 clips + 3 pestañas + 3 conectores; 2 conectores de arnés | LR / Std | V | `SM-ConsoleRI`, `SM-Console` |
| INT-041 | Armrest Assembly - Center Console; Cap - Armrest; Cupholder; Decor - Top; External Panel LH (+RH†); Panel - Front; Panel - Rear (LR y estándar) | Reposabrazos y paneles | 1 + 1 + 1 + 1 + 2 + 1 + 1 | Consola | — | — | — | LR / Std | V | `SM-Console` |
| INT-042 | Airwave Assembly - Center Console; Cap - Airwave | Rejillas traseras | 1 + 1 | Consola | — | — | — | S/E | V | `SM-Console` |
| INT-043 | Controller - USB; Hub - USB; Wireless Charger | Controlador y concentrador USB, cargador inalámbrico | 1 + 1 + 2 pads | Consola | — | USB-C 65 W (3: 1 consola + 2 traseros), USB-A en guantera, Qi 15 W ×2 | — | S/E | V | `SM-Console`, `OM-InteriorElec` |
| INT-044 | Puddle Lamp - Center Console; Center Console harness; Riser; Rail - Center Floor LH/RH | Luz, mazo, base y raíles | 1 + 1 + 1 + 2 | Consola | — | — | Cantrail; Bracket - Upper - Center Floor | S/E | V | `SM-Console` |
| INT-045 | NEMA 5-20 outlets (cabin) | Tomas 120 V en cabina | 2 | Consola y bajo la pantalla trasera | — | 20 A compartidos | Módulo HV de salida: ver TRN-027 | S/E | V | `OM-InteriorElec` |

#### 3.5.5 Asientos y cinturones

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-050 | Seat Assembly - 1st Row (Frame - Seat Cushion; Seatback Assembly; Riser Inboard/Outboard; Cover - Crossmember Riser; Track Cover) | Asiento delantero | 2 | Delante | «Vegan leather» (OM) | Dimensiones no publicadas | 4 pernos (2 + 2) Torx Plus T45 34 Nm, desechables; 1 conector; enlace del cinturón al pretensor (prueba de tracción ≥15 lb) | S/E | V | `SM-Seats`, `SM-Seat1`, `OM-Seats` |
| INT-051 | Bridge - Track Motor; Motor - Recline; Motor - Seat Height; Motor - Seat Tilt | Motores del asiento | 1 + 1 + 1 + 1 por asiento | Asientos delanteros | — | — | — | S/E | V | `SM-Seats` |
| INT-052 | Button - 8WY/Lumbar; Button - Cushion Adjust; Button - Recline | Mandos | 1 c/u por asiento | Asientos delanteros | — | — | — | S/E | V | `SM-Seats` |
| INT-053 | Blower - Cushion (ventilación); Foam - Seat Cushion/Back (with Ventilation); Trim - Seat Cushion/Back; Side Shield Inboard/Outboard; Screw Cover | Ventilación, espumas, tapicería y escudos | 1 c/u por asiento | Asientos delanteros | — | — | — | Premium/CB (ventilación) | V | `SM-Seats`, [Lemonade](https://www.lemonade.com/car/explained/cyberbeast-vs-cybertruck-awd-specs-price-review/) |
| INT-054 | Position Sensor - Seat Track - Driver | Sensor de posición de carril | 1 | Asiento conductor | — | — | — | S/E | V | `SM-Seats` |
| INT-055 | Seat Assembly - 2nd Row (Cushion Assembly LH/RH; Seat Back Assembly LH/RH; Substrate - Back Rest LH/RH; Bolster Inboard/Outboard; Foam/Trim - Back Rest Insert) | Banco trasero bipartido | 1 conjunto (2 cojines, 2 respaldos) | Atrás | — | — | Respaldo a pared trasera 4 pernos 9 Nm + 2 pernos 7 Nm (10 mm); cojín a pared 8 pernos 15 mm 50 Nm; hebillas 2 pernos 40 Nm; asiento a estructura 4 pernos 50 Nm; cubiertas de hombro 7 clips + 1 datum cada una | S/E | V | `SM-Seat2` |
| INT-056 | Headrest - Center; Armrest - 2nd Row (Closeout, Mounting Bracket, Back Lumbar, Bezel - Cupholder); A-Cover Front Outboard; B-Cover Outboard; Cap/Shoulder Cover; Strap - Release Buckle; Underbelly - 2nd Row LH/RH; Buckle Closeout; Duct On Rails; Floor Y Duct | Reposacabezas central, reposabrazos, cubiertas, conductos | 1 / 1 / 2+2 / 2 / 1+ / 2 / 3 / 1 + 1 | Atrás | — | Reposacabezas central extraíble (OM) | Cinturón central con 1 botón | S/E | V | `SM-Seat2`, `OM-Seats` |
| INT-057 | Seat belt retractors (Driver; Outboard 2nd Row; Center 2nd Row); Buckles (1st row; 2nd row); Webguide Seat Belt; Pretensioner - Lap - Driver | Cinturones | 1 + 2 + 1; 2 + 3; 4+ (A); 1 (+ pasajero A) | Todas las plazas | — | — | — | S/E | V | `SM-Safety20` |

#### 3.5.6 Seguridad pasiva (grupo 20)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-060 | Airbag - Driver; Airbag - Front Passenger | Airbags frontales | 1 + 1 | Volante; IP | — | — | Conductor: ver INT-034 | S/E | V | `SM-Safety20`, `OM-Airbags` |
| INT-061 | Airbag - Knee - Driver; Airbag - Knee - Front Passenger | Airbags de rodilla | 1 + 1 | Panel inferior | — | — | 6 pernos desechables EP10 8 Nm (conductor) | S/E | V | `SM-Safety20` |
| INT-062 | Airbag - Curtain - Driver (+ lado pasajero†) | Airbags de cortina | 2 | Techo/pilares | — | — | — | S/E | V / A | `SM-Safety20` |
| INT-063 | Seat-mounted (side) airbags | Airbags laterales montados en asiento | 2 (A: uno por asiento delantero; el OM dice que el del conductor interior protege también cabeza y torso, lo que sugiere un 2.º) | Asientos delanteros | — | — | Sin entrada en el SM leído | S/E | V (OM) / A (cantidad) | `OM-Airbags` |
| INT-064 | Restraint Control Module (RCM) | Módulo de control de retención | 1 | Soporte inferior del suelo central (ubicación no declarada) | — | — | 3 tuercas 10 mm 10 Nm (desechables); 2 conectores; 4 clips; con software ≥2025.44.3: PROC_RCM_DISARM/ARM | S/E | V | `SM-RCM` |
| INT-065 | Impact Sensor - B-Pillar LH (+RH†); Impact Sensor - Fender LH (+RH†); Impact Sensor - Front End Module LH/RH; Sensor - Pressure - Door - Front LH (+RH†) | Sensores de impacto y de presión de puerta | 2 + 2 + 2 + 2 | Pilares B, aletas, frontal, puertas | — | — | — | S/E | V / A | `SM-Safety20` |
| INT-066 | Occupancy classification sensor (pasajero) | Sensor de ocupación | 1 | Asiento pasajero | — | Umbrales ~20 lb y 51-103 lb | Indicador «Passenger Airbag OFF» | S/E | V (OM) | `OM-Airbags` |

Recuento de airbags: el OM muestra seis ubicaciones (rodilla pasajero, frontal pasajero, asiento, cortina, rodilla conductor, frontal conductor), sin airbags traseros y sin total oficial; el mínimo por categorías es 8 (A).

#### 3.5.7 Guarnecidos de puerta (por puerta ×4)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-070 | Panel - Door Trim - Front / Rear | Panel de guarnecido | 4 | Puertas | — | — | Delantero: 14 clips, 3 pernos 7 Nm con vaso 8 mm (primeras unidades: 4 pernos de 10 mm), 2 guías de arnés, 1 conector, cable de liberación manual | S/E | V | `SM-DoorTrimF` |
| INT-071 | Beltline Assembly - Door Panel; Ambient Light - Map Pocket; Puddle Lamp - Door Panel | Moldura de cintura, luz ambiental y de cortesía | 4 + 4 + 4 | Puertas | — | — | — | S/E | V | `SM-Index` |
| INT-072 | Interior Door Switch Front/Rear; Switch - Window; Interior door handles (1140) | Interruptores interiores y manillas | 4 + 3-4 + 4 | Puertas | — | — | — | S/E | V | `SM-Index` |
| INT-073 | NVH Foam - Door; Reflector - Door - Front; Manual release cable + cable lock | Espuma NVH, reflector y cable de liberación manual | 4 + 2 + 4 | Puertas | — | — | — | S/E | V | `SM-DoorTrimF` |
| INT-074 | Subwoofer - Front Door | Subwoofer de puerta delantera | 2 | Puertas del. | — | — | — | S/E | V (nombre) | `SM-Audio2121` |

#### 3.5.8 Pilares, techo y suelo

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-080 | Trim - A-Pillar Forward / Upper / Mid / Lower | Guarnecidos del pilar A | 8 | Pilares A | — | — | Por lado: Forward 4 clips + 1 guía; Upper 8 clips; Mid 1 clip + 3 pestañas; perno del A-pillar superior 6 Nm | S/E | V | `SM-Windshield` |
| INT-081 | Trim - B-Pillar Upper / Lower; Bezel - Trim - B-Pillar - Upper | Guarnecidos del pilar B | 6 | Pilares B | — | — | — | S/E | V | `SM-Index` |
| INT-082 | Trim - C-Pillar Upper / Lower; Ramp Bracket - C-Pillar | Guarnecidos del pilar C | 6 | Pilares C | — | — | — | S/E | V | `SM-Index` |
| INT-083 | Trim - Cantrail LH (+RH†); Trim - Header - Front; Trim - Header - Rear | Cantrail y cabeceras | 2 + 1 + 1 | Techo | — | — | Header delantero: 19 clips + 1 imán + 1 conector + 1 clip de arnés; sin tornillos | S/E | V | `SM-Header` |
| INT-084 | Coathook and Maplight LH (+RH†); Maplight - Front; Spot Lamp LH - Headliner (Long Range); Overhead Console Assembly - Front | Colgador/luz de lectura y consola de techo | 2 + 1 + 2 + 1 | Techo | — | — | — | S/E / LR (spot lamp) | V | `SM-Index` |
| INT-085 | Rearview Mirror; Beauty Cover; Glare Shield | Retrovisor interior | 1 + 1 + 1 | Parabrisas | — | — | 1 tornillo T20 2 Nm | S/E | V | `SM-Windshield` |
| INT-086 | Sun Visor LH / Sunvisor and Curtain Assembly | Parasol | 2 | Techo | — | — | 2 pernos 6 Nm cada uno | S/E | V | `SM-Windshield` |
| INT-087 | Fixed Glass Roof Assembly; Windshield shades | Techo de cristal fijo; cortinillas | 1; 1 par | Techo | — | — | — | S/E | V | `SM-Index` |
| INT-088 | Carpet Assembly - Driver / Front Passenger / Rear; Floor Mat Kit | Alfombras | 3 + 1 | Suelo | — | — | — | S/E | V | `SM-Index` |
| INT-089 | NVH Pad - Cowl / Dash / Rear Wall; Trim - Center Floor - Lower; Trim - Lower - Rear Wall; Side Trim - Pedal; Bracket/Rail - Center Floor; Bezel - Duct - Carpet - Rear | Aislamiento y molduras de suelo | 3 + 1 + 1 + 2 + 1/2 + 1 | Suelo | — | — | — | S/E | V | `SM-Index` |

#### 3.5.9 Audio y HVAC

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-090 | Speaker (Full Range) LH; Speaker - Header - Rear LH; Tweeter LH | Altavoces de rango completo, de cabecera trasera y tweeters | 2 + 2 + 2 | Pilares A, cabecera, etc. | — | **15 altavoces + 2 subwoofers** (Tesla vía prensa, R); 13 según otra ficha y CarGurus (R) — conflicto | — | S/E | V (nombres) / R (recuento) | `SM-Audio2121`, [Inverse](https://inverse.com/tech/tesla-cybertruck-sound-system-speakers-features), [CarGurus](https://jobs.cargurus.com/research/articles/2025-tesla-cybertruck-pricing-specs-release-date) |
| INT-091 | Subwoofer - Front Door LH; Subwoofer - C-Pillar LH | Subwoofers | 2 + 2 | Puertas del. / pilar C | — | Un foro (R) los sitúa bajo el banco trasero (2 de 8"): discrepancia | Subwoofer RH: 2 pernos 13 mm 8 Nm; 4 pernos 13 mm 8 Nm (página batería AWD) | S/E | V (nombres) | `SM-Audio2121`, `SM-BodyCtrlRear`, `SM-HVBattAWD`, [CTOC](https://www.cybertruckownersclub.com/forum/threads/speaker-locations-sizes-types.23715/post-403124) |
| INT-092 | Speaker - Super Horn; Horn - Low Tone LH; Telephony Microphone LH; Pedestrian Warning Speaker | Bocinas y micrófonos | 1 + 1 + 1-2 + 1 | Exterior/cabina | — | — | PWS: 3 tornillos T25 2 Nm, 1 conector | S/E | V | `SM-Audio2121`, `SM-PedSpk` |
| INT-093 | Blower - HVAC; Wet Side - HVAC; HVAC Distribution; Actuator - Blend Door - HVAC; HEPA Filter + Cover; Air Extractor | Climatizador | 1 c/u | Bajo el IP | — | — | Soplador: 3 tornillos T20 1 Nm + cubierta 3 tornillos | S/E | V | `SM-HVAC1810`, `SM-Blower` |
| INT-094 | Demist Duct - Quarter Glass LH; Floor Duct - Inboard LH/RH; Jumper Floor Duct; Panel Duct - RH; Jumper/Riser Duct - Center Console; Pentaport AC Lines; Suction Discharge Lines | Conductos | — | Cabina | — | — | — | S/E | V (nombres) | `SM-HVAC1810` |
| INT-095 | Sensor - Cabin HVAC - RH and Temp; Sensor - Cabin Temperature, Fan Driven; Sensor - Windshield - Temperature and RH | Sensores de clima | 1 c/u | Cabina/parabrisas | — | — | — | S/E | V | `SM-HVAC1810` |

#### 3.5.10 Piezas pequeñas e interiores ocultas (sub-tabla)

| ID | Pieza | Cant. | Dato | Conf. | Fuente |
|---|---|---|---|---|---|
| INT-S01 | Clips de panel de puerta delantera | 14 por puerta | + 3 pernos 7 Nm, 2 guías de arnés | V | `SM-DoorTrimF` |
| INT-S02 | Clips del panel trasero de la consola | 10 + 3 pestañas | 3 conectores | V | `SM-ConsoleRI` |
| INT-S03 | Clips de la moldura de cabecera delantera + imán | 19 + 1 | — | V | `SM-Header` |
| INT-S04 | Cubiertas de hombro trasero | 7 clips + 1 datum cada una | — | V | `SM-Seat2` |
| INT-S05 | Clips de alfombra RH | 8 + 4 datums | — | V | `SM-CarComputer` |
| INT-S06 | Clip EPP de la guantera | 1 | — | V | `SM-Glovebox` |
| INT-S07 | Cubiertas de tornillos del asiento (Screw Cover) y de carril | varios | — | V (nombres) | `SM-Seats` |
| INT-S08 | Lower Column Shroud Clip; Webguide; Strap - Release Buckle; Reflector - Door; Glare Shield | 1; 4+; 1+; 2; 1 | — | V (nombres) | `SM-Index` |
| INT-S09 | Mazos, conectores amarillos/negros, clips de arnés | — | Alta dependencia de mazos (asientos calefactados y ventilados, volante calefactado) | A | — |

Sin fuente (no afirmar): extintor/triángulo, luz ambiental fuera de «Ambient Light - Map Pocket», sensor UV, paso cabina-caja, compartimento bajo asiento trasero, headliner como pieza.

---

### 3.6 Electrónica, 48 V y sensores

**Arquitectura (V).** El SM llama «mid voltage (MV)» a la red de **48 V**; el Cybertruck no lleva batería principal de 12 V. Un convertidor «switched-tank» detecta si la fuente es 12 V o 48 V (arranque con cables) (R, Pete Bannon vía Autopian). Los controladores de zona escalonan a 12 V localmente (R, [Autoline](https://www.autoline.tv/?p=91080)). Conectores y cintas azules para 48 V (R, [Basenor](https://www.basenor.com/blogs/news/cybertrucks-engineering-firsts-48v-steer-by-wire-explained)). Red troncal Ethernet «etherloop» de Gigabit bidireccional (R). Cableado: 155 cables frente a 490 del Model 3, 368 puntos finales frente a 273 (+50 %), −68 % de cable por el etherloop y −84 % de masa de arneses de alta potencia (R, [Assembly Magazine](https://assemblymag.com/articles/98504-teslas-new-cybertruck-features-modular-wiring)).

#### 3.6.1 Controladores, 48 V y red

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| ELE-001 | Battery - Mid-Voltage | Batería de media tensión (48 V, ion-litio) | 1 | Bajo el apron trasero/frunk; se desliza hacia delante | Ion-litio | **4 Ah** (OM y InsideEVs, R: ~192 Wh); el SM no da capacidad | 2 pernos 10 mm 8 Nm | S/E | V (pieza) / V-R (capacidad) | `SM-MVBattery`, `OM-Subsystems`, [InsideEVs](https://insideevs.com/news/704749/tesla-cybertruck-low-voltage-battery-48v-4ah/) |
| ELE-002 | Maintainer - Mid-Voltage; MV power disconnect (First Responder Loop connector + MV battery connector) | Mantenedor y desconexión MV | 1 + 1 | Apron trasero; poste de arranque / perno entre depósito de frenos y frunk | — | Espera de 2 min tras desconectar | Rojo/azul/negro; FRL temprano negro | S/E | V | `SM-MVMaintainer`, `SM-MVPower`, `SM-MV1702` |
| ELE-003 | Body Controller LH | Controlador de carrocería izquierdo | 1 | Mamparo LH | — | — | 4 tuercas 10 mm 14 Nm; 1 perno de cubierta seca 8 mm 6 Nm + 1 húmeda 6 Nm; 2+2 conectores + dirección + X0012/13/14; 5 clips de arnés | S/E | V | `SM-BodyCtrlLH` |
| ELE-004 | Body Controller RH | Controlador de carrocería derecho | 1 | Mamparo RH | — | — | 2 pernos de cubierta 8 mm 6 Nm; 4 tuercas 10 mm 14 Nm; 7 conectores + SFA (pestaña roja) + 2 bulkhead; 7 + 1 clips | S/E | V | `SM-BodyCtrlRH` |
| ELE-005 | Body Controller Rear | Controlador trasero | 1 | Pared trasera inferior | — | — | 1 perno cautivo 8 mm 6 Nm; 3 fijaciones 10 mm (2 tuercas 13 Nm + 1 perno 10 Nm); conectores J3 X0052 + 3 + etherloop; cintas PN 1879451-99-A y 1879451-00-B | S/E | V | `SM-BodyCtrlRear` |
| ELE-006 | Door Controller Front/Rear LH (+RH†) | Controlador de puerta | 4 | Puertas | — | — | 1 perno T20 (par no indicado); direccionado con Toolbox 3 | S/E | V (LH) / A (RH†) | `SM-DoorCtrl` |
| ELE-007 | MV Controller (rear, Long Range); MV Locking Cover Circlip | Controlador MV trasero (LR) y circlip | 1 + 1 | Trasera | — | — | Página 403 | LR | V (título) | `SM-Index` |
| ELE-008 | Harness - MV Backbone | Mazo troncal de 48 V | 1 | Controlador RH ↔ controlador trasero, por el suelo RH | — | Cintas de abrasión: 50x150 mm PN 1879451-99-A y 25,4x235 mm PN 1908543-99-A; VHB 1879451-00-B | 2 pernos de cubierta 8 mm 6 Nm; 6 clips traseros + 3 delanteros + 1 de conducto RH 2.ª fila + 1 de fundición delantera (se descarta) | S/E | V | `SM-MVBackbone` |
| ELE-009 | Car Computer | (ver INT-022) | 1 | IP | — | — | — | S/E | V | `SM-CarComputer` |
| ELE-010 | Gateway | Gateway | 1 | — | — | Sin procedimiento de hardware; solo «Gateway (Unlock)» 90 min | — | S/E | V | `SM-FlareCam` |
| ELE-011 | ECU Trailer | ECU de remolque | 1 | Tras la fascia trasera | — | — | 2 tuercas 10 mm 9 Nm; 1 conector con palanca | S/E | V (ubicación A) | `SM-TrailerECU` |
| ELE-012 | Restraint Control Module | (ver INT-064) | 1 | Cabina | — | — | — | S/E | V | `SM-RCM` |
| ELE-013 | Charge Port Controller (Gen 4) | (ver TRN-036) | 1 | Cuarto trasero LH | — | — | — | Gen 4 | V | `SM-ChgPortECU` |
| ELE-014 | Supermanifold controller; Device Cluster; Steering Column Control Module; TCU; USB controller + hub | Controladores varios | 1 c/u | Varias | — | — | — | S/E / Std | V (nombres) | `SM-Index` |
| ELE-015 | Harnesses: ancillary, LV device cluster, steering jumper, rear subframe (dual/tri motor), seat, door, fascia, windshield, LH/RH frunk, tailgate, cowl speaker, shunt jumper; ferrite core; coax cables (side repeater, front LH/RH, jumper) | Mazos | — | Varias | — | Longitudes/masas: no publicadas | Ferrite core en device cluster | TM (rear subframe) | V (títulos) | `SM-TOC` |

#### 3.6.2 Cámaras y sensores (Cyberbeast: sin ultrasonidos ni radar frontal en el SM/OM)

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| ELE-020 | Bi-Cam - Forward Facing | Módulo de dos cámaras del parabrisas | 1 (2 cámaras) | Tras el retrovisor, soporte del parabrisas | — | Calibración de cabeceo: diana a 91,4 cm del suelo, cinta roja a 165 cm, 106 cm libres | 4 tornillos T10 1 Nm; 3 conectores (GNSS + 2 cámaras) | S/E | V | `SM-BiCam`, `OM-Cameras` |
| ELE-021 | Camera - Forward Facing - Front Fascia | Cámara frontal de fascia (calefactada) | 1 | Fascia delantera | — | — | Cubierta 2 × PH1 2 Nm; cámara 2 × T8 0,7 Nm; conector de calefactor + coaxial | S/E | V | `SM-FasciaCam` |
| ELE-022 | Camera - B-Pillar LH/RH («trinity») | Cámara del pilar B | 2 | Pilares B | — | — | 2 tornillos T8 0,8 Nm; junta tórica | S/E | V (LH) / A (RH†) | `SM-BPillarCam` |
| ELE-023 | Camera - Fender Flare LH/RH («trinity») | Cámara de la aleta | 2 | Aletas | — | — | 2 tornillos T8 0,8 Nm; cubierta con 11 clips + 3 datums; conector de repetidor | S/E | V (LH) / A (RH†) | `SM-FlareCam` |
| ELE-024 | Camera - Rear | Cámara trasera (HW4) | 1 | Portón, tras la cubierta interior | — | Resolución HW4 hasta 2880x1876, 45 fps (R, no específico del Cybertruck) | Soporte 2 tornillos T10 0,7 Nm; cámara 2 tornillos T10 0,7 Nm | HW4 | V | `SM-RearCam`, [notateslaapp](https://www.notateslaapp.com/news/1298/cc593c6f-ff77-4eb7-b604-d3c0f7cbf2d9) |
| ELE-025 | Interior Camera | (ver INT-026) | 1 | Cabina | — | — | — | S/E | V | `SM-IntCam` |
| ELE-026 | Fan - Camera - Windshield | Ventilador de la cámara del parabrisas | 1 | Parabrisas | — | — | 3 tornillos T6 0,12 Nm; 3 calzos antirruido; 1 + 3 conectores; 4 clips | S/E | V | `SM-CamFan` |
| ELE-027 | Radar - Cabin | (ver INT-027) | 1 | Cabina | — | — | — | S/E | V | `SM-RadarCabin` |
| ELE-028 | TPMS sensor | (ver CHS-084) | 4 | Ruedas | — | — | — | fecha | V | `SM-TPMS` |
| ELE-029 | Ride height sensors; wheel speed sensors | (ver CHS-011/030/069) | 4 + 4 | Chasis | — | — | — | S/E | V | `SM-RideHF`, `SM-RideHR` |

Cuenta de cámaras: **9** (rear 1 + B-pillar 2 + fender flare 2 + fascia 1 + bi-cam 2 + cabina 1). El OM lista también 9 ubicaciones (portón, 2 pilares, 2 parabrisas, 2 ruedas delanteras, 1 parachoques, 1 cabina). Los lados RH no se leyeron (A). No se encuentra radar frontal ni ultrasonidos en el SM ni en el OM (ausencia, A).

#### 3.6.3 Antenas, conectividad y otros

| ID | Pieza (EN oficial) | Nombre ES | Cant. | Ubicación | Material | Dim./masa | Fijaciones / par | Var. | Conf. | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| ELE-040 | Antenna - GPS; Antenna - Wi-Fi; Antenna - AM/FM/HD; Antenna - Satellite Radio; Antennas and Amplifiers | Antenas | 1 c/u | GPS: glare shield; resto: n.q. | — | Cantidad/posición: no publicadas | GPS 1 tornillo T10 0,8 Nm | S/E | V (nombres) | `SM-GPSAnt`, `SM-TOC` |
| ELE-041 | BLE End Point - Front/Rear, Interior, Rear, Wheel Well front LH/RH, Wheel Well rear LH/RH; B-pillar BLE (compartido con la cámara) | Puntos finales Bluetooth LE (llave del teléfono) | ~8 | Fascia, interior, pasos de rueda, pilar B | — | — | Trasero: 2 tornillos T25 5 Nm (tras fascia trasera); paso de rueda del. LH: 2 pernos T20 1,5 Nm (desechables) | S/E | V | `SM-BLERear`, `SM-BLEWell` |
| ELE-042 | Key Card; UWB | Tarjeta llave; UWB | 1+; — | Consola | — | UWB no figura en ninguna fuente | — | S/E | V (tarjeta) | `SM-TOC` |
| ELE-043 | Window regulator 48 V Q-Motor | (ver EXT-047) | 4 | Puertas | — | — | — | S/E | V | `SM-WinRegQ` |
| ELE-044 | Windshield wiper motor | (ver EXT-105; 48 V, R) | 1 | Cowl | — | — | Recall del controlador del motor (NHTSA) | S/E | V / R | `SM-WiperMotor`, [The Drive](https://www.thedrive.com/news/tech/nearly-every-tesla-cybertruck-has-been-recalled-again-this-time-for-sketchy-windshield-wipers) |
| ELE-045 | Outlets (Powershare): 2 × 120 V/20 A cabina, 2 × 120 V/20 A caja, 1 × 240 V caja; 48 V 400 W en techo y frunk | Tomas y alimentaciones de 48 V | 5 + 2 | Cabina / caja / techo / frunk | — | 9,6 kW continuos combinados; hogar 11,5 kW | Bed Outlet: ver EXT-078 | AWD / CB | R | [Basenor](https://www.basenor.com/blogs/news/cybertruck-powershare-explained-every-outlet-and-what-it-can-do), [InsideEVs](https://insideevs.com/news/704749/tesla-cybertruck-low-voltage-battery-48v-4ah/) |
| ELE-046 | Washer pump; wiper-motor controller; tonneau motors; door presenters | Actuadores 48 V | — | — | — | — | Ver EXT | S/E | V | varios |

#### 3.6.4 Piezas pequeñas de electrónica (sub-tabla)

| ID | Pieza | Dato | Conf. | Fuente |
|---|---|---|---|---|
| ELE-S01 | Cubiertas cautivas de bloqueo MV («locking cover») | 8 mm 6 Nm, común a todos los controladores y al backbone | V | `SM-BodyCtrlLH`, `SM-MVBackbone` |
| ELE-S02 | Conectores con 2 pestañas/bloqueo de pestaña roja o amarilla y palanca negra | Todos los conectores de controladores | V | `SM-BodyCtrlRH` |
| ELE-S03 | Cintas de abrasión y VHB del arnés | PN 1879451-99-A, 1908543-99-A, 1879451-00-B | V | `SM-MVBackbone` |
| ELE-S04 | Coaxial azul de la pantalla trasera; coaxiales de cámaras | — | V | `SM-RearDisplay`, `SM-FasciaCam` |
| ELE-S05 | Conectores sin carcasa plástica en la placa del controlador principal | Pines soldados a la placa (R) | R | [Autopian](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/) |
| ELE-S06 | Racores de A/C, Schrader, tapas | Ver TRN-048 | V | `SM-Pentaport` |
| ELE-S07 | Busbars del cargador y cabecera HV doblador | Ver TRN-033/035 | V | `SM-LastMile`, `SM-ChgBus` |

No hay lista de fusibles/relés de 12 V ni de eFuse: la protección de zona posiblemente es de estado sólido (A). Ver los «gaps» en la sección 6.

---
## 4. Resumen estimado del recuento de piezas por sistema

**Método y límite.** No existe BOM ni recuento oficial: Moravy dijo que no había contado las piezas ([Design News](https://www.designnews.com/automotive-engineering/video-tesla-s-head-of-vehicle-engineering-discusses-the-cybertruck-s-castings-and-stampings)). Las cifras de las dos primeras columnas proceden de las notas (títulos de procedimiento, filas consolidadas); la tercera columna es una **estimación propia (A)** que expande LH/RH y ×4 puertas sobre esos nombres; no es un dato de Tesla.

| Sistema | Nombres / procedimientos documentados (notas) | Filas de esta ficha | Instancias físicas estimadas (A) | Piezas pequeñas nombradas (clips, tapones, sellos, soportes) | Objetos en el modelo actual (reasignados por prefijo) |
|---|---|---|---|---|---|
| Exterior, cierres, vidrio, luces (incl. caja y tonneau) | ~250 títulos de procedimiento (SM 10xx, 11xx, 12xx, 17xx) | 104 (algunas agrupan varios nombres) | ~350-450 | Decenas: p. ej. 17 clips por vela, 19 del header, 9 del apron, 14+6+1 del liner delantero | 168 |
| Estructura de carrocería | ~55 procedimientos CR + ~25 piezas estructurales del SM + 8 guías de reparabilidad | 47 | ~100-130 | Tapones 1870761-00, plantillas, placas de tuercas, espárragos, remaches por PN (7 familias de remache + 7 flow-form + 10 SPR) | 33 |
| Chasis (suspensión, dirección, frenos, ruedas) | 161 filas en la tabla consolidada de las notas (>150 ítems distintos) | ~100 | ~160-190 (4 esquinas, 24 tuercas de rueda, 24 espárragos) | ~13 tipos de clips, grommets, escudos | 135 |
| Tren motriz, batería HV, térmica | ~230 filas de fijación/par; térmica: 1820 (5 proc.), 1830 (20), 1840 (20); batería 1630 (44 títulos) | ~50 | ~120-160 (sin contar 1.344 celdas) | Arandelas, clips de resorte, tapones, grommets | 68 |
| Interior (incl. seguridad pasiva, audio, HVAC) | >170 piezas con nombre oficial | ~85 | ~300-350 | Clips: 14 por puerta, 19+1 header, 10+3 consola, etc. | 130 |
| Electrónica, 48 V, sensores | 73 líneas (~100+ piezas físicas), ~190 entradas de fijación | ~45 | ~100-130 | Cubiertas MV, cintas, conectores | ~24 (más 2 tapas de ojal de remolque en exterior) |
| **Total (orden de magnitud)** | — | — | **~1.100-1.450 piezas físicas nombradas (A), sin tornillería ni celdas** | Con tornillería y clips, varios miles | **560 nodos con metadatos (el modelo declara 561 objetos)** |

Recuentos exactos que sí aportan las notas (V):

- Estructura: Front Under Body completo = 34 remaches (30 HS + 4 FF) + 20 tornillos (8 M12x35 + 10 M12x43 + 2 M10x33); Body Side completo = 46 HS + 7 avellanados + 10 flow-form + 13 tornillos; Rear Wall = 48 HS + 40 flow-form + 2 tornillos; Rear Header Upper = 32 flow-form.
- Batería (LR): ~22 mounts exteriores (6 + 16) + 14 interiores (6 + 8) + 4 al RUB = ~40 fijaciones estructurales (suma de filas V, A como total).
- Enganche: 12 fijaciones (6 + 4 + 2).
- Cámaras: 9 (8 exteriores contando el bi-cam como 2 + 1 de cabina).
- Frenos: 4 pinzas (2 de 4 pistones + 2 de 1 pistón con EPB), 4 discos, 8 pastillas; ruedas: 24 tuercas.
- Moravy: 20-30 % menos piezas que un vehículo anterior (sin celdas) y mitad trasera en una sola fundición (R); sin cifra absoluta.

---

## 5. Variantes y diferencias entre acabados

### 5.1 Cyberbeast frente al resto (lo confirmado)

| Aspecto | Cyberbeast (Tri-Motor) | Premium / Dual Motor AWD | Long Range (RWD) | Conf. | Fuente |
|---|---|---|---|---|---|
| Motores | Delantero PMSM + 2 traseros de inducción | Delantero inducción + trasero imanes permanentes según la tabla del OM (posible errata) | 1 trasero de imanes permanentes | V (OM) | `OM-Subsystems` |
| Relación | 15,02:1, una marcha | 15,02:1 (tabla con «2» en el trasero: errata aparente) | 15,02:1 | V | `OM-Subsystems` |
| Suspensión | Aire adaptativo | Aire adaptativo | Muelles helicoidales (nombres «Long Range» en el SM) | V / A | `SM-Index`, `SM-ALIGN` |
| Llanta/neumático de fábrica | 20" «Core» all-season (configurador, repo) o 20" AT; 18" disponible en el OM | 20"/18" | 18" (acero «Steel Wheel (Long Range)») | V (OM) | `OM-Wheel` |
| Altura/distancia al suelo (Medium) | 1.793,8 / 257 mm | idem | 1.779,8 mm (18" AS) / 243 mm | V | `OM-Dimensions` |
| Masa en vacío / carga útil | 6.863 lb / 2.000 lb (AS) | 6.634 lb / 2.200 lb | 6.118 lb / 2.006 lb | V | `OM-Dimensions` |
| Remolque | 11.000 lb | 11.000 lb | 7.500 lb | V | `OM-Dimensions` |
| Emblema | Cabeza de Cerbero en la parte trasera derecha | No | No | V | `RS` |
| Subchasis trasero | «Subframe, Rear (Tri Motor)» | «Subframe, Rear (Dual Motor)» | (LR: página propia de dirección trasera) | V (títulos) | `SM-Subframe-R-TM`, `SM-Subframe-R-DM` |
| Dirección trasera | Sí (actuador trasero) | Sí | Sí (hay mazo «Rear Steer (Long Range)») | V / A | `SM-SAR`, `SM-RearSteerJumperLR` |
| Tonneau motorizado | De serie (Wikipedia) | De serie | No (R) | R | [Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck) |
| Asientos ventilados, 15 altavoces, pantalla trasera | Sí | Sí (Premium) | No | R | [Lemonade](https://www.lemonade.com/car/explained/cyberbeast-vs-cybertruck-awd-specs-price-review/) |
| Tomas de a bordo (Powershare) | 5 tomas, 9,6 kW | 5 tomas | Sin tomas (R) | R | [Basenor](https://www.basenor.com/blogs/news/cybertruck-powershare-explained-every-outlet-and-what-it-can-do) |
| Barra de luz off-road (parabrisas «w/ Off Road Lightbar») | Opción | Opción | — | Opc | `SM-Glass1020` |
| Terrestrial Armor | Opción (altura de chasis −15 mm) | Opción | — | Opc | `SM-TerrArmor`, `SM-ALIGN` |

Etiquetas de fecha de producción halladas: «Post 11/4/2024» (nuevo aplique de vela y raíl de tonneau); NVH barrier «pre-April 2024 / post-April 2024 / post-October 2024»; bisagra de portón 75 Nm desde 2024-07-10; hose bundle de refrigerante mejorado para vehículos anteriores a 2023-12-22; TPMS negro desde 2025-02-06; tuercas en U en la faldilla trasera desde 2025-11-17; refrigerante G-48 azul en producción temprana. Foundation Series (2023-24, ventas finalizadas en enero de 2025), RWD Long Range (2025, descontinuado en septiembre de 2025), range extender cancelado (depósitos reembolsados en mayo de 2025). Recalls relevantes a la geometría: panel/embellecedor (marzo de 2025), barra de luces off-road (octubre de 2025), desprendimiento de rueda del modelo económico (mayo de 2026) ([Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck), R).

Nombres comerciales de gama: las notas (Wikipedia, R) hablan de AWD, Premium AWD y Cyberbeast con un AWD a 59.990 USD desde febrero de 2026 (la fuente dice «entregas desde abril de 2027», probable errata); `docs/research-and-fidelity.md` registra el configurador del 2026-10-16 con «Dual Motor AWD 74.990, Premium AWD 84.990, Cyberbeast 99.990 USD», decoración «Tactical Grey» y 20" «Core Wheels» de serie en Cyberbeast (V en ese documento, no verificable con las notas). **Conflicto de precios no resuelto**; no afecta a la geometría.

### 5.2 Notas y filas que NO están confirmadas para Cyberbeast

Esta ficha etiqueta cada fila con su variante. Estas son las familias cuyas fuentes **no son Cyberbeast**:

- Todas las páginas «(Long Range)»: HV Battery (LR), PCS (LR), Fuses (LR), Charge port busbar (LR), Horizon Rail (LR), Bed Side Wall Upper/Lower (LR), Spot Lamp (LR), Non-Driven Hub (LR), Steel Wheel (LR), Coil Spring (LR), Knuckle Assembly Front (LR), MV Controller (LR), Rear Steer (LR).
- Todas las páginas «Dual Motor / AWD»: Rear Drive Unit (Dual Motor) con su par, Subframe Front (AWD), HV Battery (AWD).
- Todas las páginas sin etiqueta («S/E»): se asumen comunes, pero el SM no marca Cyberbeast en casi ninguna.
- Las páginas «Tri Motor» (RDU LH/RH, inversores LH/RH, bomba de aceite LH, arnés HV LH/RH, subchasis trasero): **solo se leyó** el subchasis trasero Tri Motor; el resto se conoce solo por título.
- Datos de prensa sobre el «Foundation Series» tri-motor de Munro: su teardown fue de un Foundation Series, no de un Cyberbeast.
- Fichas de concesionarios: variable de trim no garantizada.
- OM: el PDF es de Norteamérica (Software 2026.20); otros mercados pueden diferir.
- Estructura de carrocería: «común a todas las variantes» según el CR; solo «HV Battery (AWD)», «Subframe, Rear (Dual Motor)» y «Bed Side Outer Assembly (Long Range)» aparecen etiquetadas.

---

## 6. Conflictos entre fuentes y huecos abiertos

### 6.1 Conflictos (ordenados por impacto en el modelo)

| # | Tema | Valores en conflicto | Dato recomendado para el modelo | Observación |
|---|---|---|---|---|
| 1 | Chapa exterior: espesor | 1,8 mm puertas / 1,4 mm resto (Wikipedia citando a Moravy) frente a ~3 mm (Musk, SAE) | 1,4-1,8 mm si se modela espesor (R) | «30X» sin fuente primaria; el CR dice que el inox no se suelda y solo se refina |
| 2 | Tensión de la batería HV | OM 700 V DC nominal; Rescue Sheet «800V»; Autopian 800 V | 700 V nominal en las etiquetas del modelo (V, OM); 800 V como clase de arquitectura (A) | El modelo declara «~800 V» en `BATTERY_PACK` |
| 3 | Vía | OM 1.772/1.772 mm; SM 1.777/1.772 mm | Usar el OM; diferencia de 5 mm | Probables puntos de medida distintos (A) |
| 4 | Distancia al suelo y alturas | OM 257 mm Medium; SM «altura de chasis» 265 ± 5 mm; concesionarios 201/406 mm; Basenor 9,5/17,4 in | OM por ajuste | El modelo usa Medium 1.793,8/257 mm |
| 5 | Ángulos de ataque/ventral/salida | Sin dato primario; 35° o 40°, 26°, 28° (R) | No fijar; medir sobre el modelo | Dependen del ajuste de altura |
| 6 | Masa en vacío del Cyberbeast | 6.863 / 6.898 (OM); 6.901; 6.898 (iFixit); 6.843 (Munro); 6.918 (máx. SM) | 6.863 lb (OM, AS) | — |
| 7 | Neumático (marca/medida) | OM PDF: 285/65R20 AS; LT285/65R20 Pirelli Scorpion ATR AT; 285/70R18 Goodyear. Notas de chasis: Pirelli ATR = 285/65R20 «hard metric» AS; Goodyear Wrangler Territory RT = LT285/65R20 AT | Verificar contra la etiqueta del pilar B | El modelo usa «Pirelli Scorpion ATR 285/65R20 (T0)» |
| 8 | Tow hitch: par | 198 Nm (Tow Hitch) frente a 178 Nm (Rear Energy Absorber) | 198 Nm (nuevos) con la página específica | Conflicto interno de Tesla |
| 9 | UCA delantero: tuerca a mangueta | 80 Nm (UCAF y halfshaft) frente a 85 Nm (FDU); un paso dice 190/24 mm | 80 Nm | Tabla «reutilizar» vs paso «descartar» |
| 10 | UCA delantero a carrocería | Tabla 4 tuercas; pasos «x3» | 4 (tabla) | — |
| 11 | Barra estabilizadora trasera | 4 pernos (SBR) frente a 6 (subchasis, con bieletas) | 4 + bieletas | — |
| 12 | Skid plate delantera | 8 pernos 10 mm + 4 clips 4 Nm frente a 8 tuercas 15 mm + 2 pernos 11 mm 50 Nm | Probables dos piezas | Skid Plate vs Skid Plate Stamping (A) |
| 13 | Aeroshield delantero / trasero / skid central | 11 vs 17 pernos; 7 vs 5 pernos; 3 × 15 mm 70 vs 42 Nm | Usar la página propia de cada pieza | — |
| 14 | Holgura brazo limpiaparabrisas-carcasa | 3 ± 1 mm (Windshield) vs 5,5 ± 1 mm (Wiper Arm) | 5,5 mm (página específica) | — |
| 15 | Longitud del limpiaparabrisas | 62 in; ~50 in (brazo); ~4 ft (1,22 m) | No fijado; el modelo usa ~1,26 m | Conflicto (R) |
| 16 | Torques del portón | Barras de torsión: 25/50 Nm (Tailgate) frente a 55/80 Nm (Torsion Rod) | 55 / 80 Nm (página Torsion Rod, la específica); 25 / 50 Nm quedan como pernos de extremo de barra (LH / RH) en la página Tailgate | Las notas señalan que son fijaciones distintas pero lo marcan como posible inconsistencia |
| 17 | Compresor: trenza de masa | 16 Nm (A/C Compressor) frente a 7 Nm (Supermanifold) | 16 Nm | — |
| 18 | VOSS del depósito de aire | 3, 5 o 7 Nm | 3 Nm (fitting estándar) | Varía por tamaño (14/10 mm) |
| 19 | Altavoces | 15 + 2 subwoofers (Tesla/Inverse) frente a 13 (otra ficha y CarGurus); el SM nombra subwoofers de puerta delantera y pilar C, un foro los sitúa bajo el banco | 15 + 2 (R) | Posiciones: usar nombres del SM |
| 20 | Tamaños de pantalla | 18,5" y 9,4" (R); el OM no da tamaño | R | El modelo los marca «Verificado» en `DISPLAY_CENTER` |
| 21 | Dirección | OM: 0,94 vueltas / 340° (V); Basenor: 200° o 340°; ángulo trasero 3° o 10° (R) | OM | — |
| 22 | Celdas | 192S7P (Lean Design) frente a 224S6P (filtraciones regulatorias); 4 bloques de 7 × 48 | 1.344 celdas; 192S7P | R |
| 23 | Capacidad del pack | 123 kWh / 111,9 kWh útiles (R); «medio vacío» (Munro); extender de ~+50 kWh (iFixit) cancelado | 123 kWh | R |
| 24 | Carga de refrigerante A/C | «Carga no figura» (ronda motriz) frente a 1.020 g (Fluid Capacities, ronda cotas) | 1.020 g | Prevalece la ronda 2 (cotas) |
| 25 | Rear Under Body | El resumen de la herramienta dijo «steel component» | Fundición (A) | Errata probable |
| 26 | Prensa 9.000 t | Musk: trasera; IDRA 8.000 t: subestructuras; otra: delantera | No relevante a la geometría | R, contradictorio |
| 27 | Motor delantero/trasero en Premium AWD (tabla del OM) | Aparece invertido respecto a la prensa | Solo afecta a AWD | No relevante a Cyberbeast |
| 28 | Páginas con extracción dudosa | Dos páginas con discrepancias internas visibles (resumidas automáticamente) | Revalidar con `curl` y `<h1 class="title topictitle1">` | Notas de la ronda 2 |
| 29 | Rescue Sheet: texto | Una nota dice que no se pudo extraer el texto; otra lo leyó con `pdftotext` | Prevalece la lectura completa | La ES difiere en el corte del negativo de 48 V |
| 30 | Recuento 560 vs 561 | El inventario lista 560 nodos con metadatos; el modelo declara 561 objetos | Cuadra al contar la raíz | — |

### 6.2 Huecos abiertos, ordenados por importancia para el modelo 3D

| Rango | Hueco | Por qué importa | Cómo cerrarlo |
|---|---|---|---|
| 1 | Material y dimensiones por pieza (mapa de materiales y cotas del CR en imágenes) | Sin cotas de control no se puede validar la forma de la estructura | Abrir las 5 figuras de `CR-Dimensional` y las 4 figuras de materiales de `CR-MatAllowed` en un navegador; leer a ojo con zoom |
| 2 | Huecos y enrases de paneles | Define las juntas entre puertas, capó y portón | El SM remite a «Inspection Standards» (interno de Tesla); medir sobre fotos y patente D-design |
| 3 | Ángulos de ataque, ventral y de salida; radio de giro; ángulo físico de las ruedas traseras | Postura y encaje en la vista | Medir sobre el modelo a cada altura; OM no los publica |
| 4 | Páginas con datos de Tri Motor no leídas (RDU LH/RH, inversores, bomba de aceite LH, arnés HV LH/RH, subchasis dual) | Es la variante que se modela | Leer los GUID de `SM-HVHarnessRDU-L/-R`, `SM-ROilPumpTM`, `SM-Subframe-R-DM` |
| 5 | Rear Under Body (esquina): significado de las cotas A-S; Mast/Torre/Absorbedor: geometría | Fundiciones traseras | Figuras del CR (`CR-RUBrail`); teardown de Munro |
| 6 | Número de lamas del tonneau; longitud del cassette; cadena | Geometría visible de la caja | El modelo usa 22 lamas sin fuente en las notas; contar en fotos y vídeo de Munro |
| 7 | Tamaños de pantalla, número y posición de altavoces, color Tactical Grey | Detalles de interior | tesla.com/cybertruck (403): abrir en navegador |
| 8 | Masas de unidades motrices, batería, castings, BIW | Equilibrio y animaciones | Rescue Sheet, Munro, EPC; ninguna página del SM las da |
| 9 | Casquillos, topes de rebote, asientos de muelle, fuelles, rótulas delanteras | Detalle de suspensión | Fotos de teardown; Munro |
| 10 | Antenas (cantidad y posición), BLE (posiciones exactas), UWB | Lista de sensores | Páginas de SM 2135/1745 |
| 11 | Páginas con HTTP 403: Front Body Bridge Reinforcement, Rocker Support Bracket, Rear Wheel Arch (Rear Section), Front Quarter Window (Outer), Front Drive Unit Mount (Right), MV Controller Rear (LR), tonneau cam block / mid slat / sealing slat / chain link, Rear Energy Absorber, Front Plate Bracket, Fender Flare, Rocker Panel, Powergate Fascia, charge port | Piezas citadas pero no dimensionadas | Reintentar con `curl` y User-Agent de navegador |
| 12 | Fusibles/relés 12 V, eFuse, DC-DC, nodos del etherloop | Árbol eléctrico | Páginas SM 1702/1710/21xx; patente del backbone |
| 13 | Catálogo de piezas oficial (epc.tesla.com) | Números de pieza, BOM, explosionados | Necesita acceso; la Wikipedia enlaza `catalogs/2816` (sección eléctrica) |
| 14 | Licencias de modelos 3D de terceros (Sketchfab/GrabCAD), fotogrametría, blueprints | Referencias de forma | No evaluado |

---

## 7. Directorio de fuentes, por orden de utilidad, y cómo leerlas

### 7.1 Fuentes primarias de Tesla

| Rango | Fuente | URL | Aporta | Cómo leerla / límites |
|---|---|---|---|---|
| 1 | **Service Manual (SM)** Cybertruck, en-us | `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html` | Nomenclatura oficial por procedimiento (~1.079 enlaces en el índice), fijaciones, pares, clips, conectores, variantes, tiempos oficiales | Accesible con `curl` y User-Agent de navegador; el cuerpo útil está en `<h1 class="title topictitle1">`; WebFetch resume mal (solo ve la navegación). Páginas «DRAFT» («Warnings and Cautions might be missing»). LH documentado, RH «similar». Etiquetas entre paréntesis = variante: «(Long Range)», «(Standard)», «(Dual Motor)», «(Tri Motor)», «(AWD)». FRT = tiempo oficial; correction code = código de la operación. Las imágenes contienen las vistas despiezadas |
| 2 | **Collision Repair Manual (CR)** | `https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html` | Lista de piezas estructurales, remaches/tornillos por PN, pares, límites de reparación de fundiciones, productos químicos, 99 páginas | Las cotas de control y el mapa de materiales son **imágenes**; abrir en navegador. Fechas 2026-08-10 |
| 3 | **Owner's Manual (OM)**, espejo tesla.cn | `https://www.tesla.cn/ownersmanual/cybertruck/en_us/Owners_Manual.pdf` (17.178 líneas con `pdftotext`; Software 2026.20, North America) y páginas HTML por GUID bajo `/ownersmanual/cybertruck/en_us/` | Cotas exteriores al centésimo de pulgada, alturas por ajuste, pesos por variante, ruedas, motores, frenos, dirección, airbags | `tesla.com` da 403; usar `tesla.cn`. Regiones `en_ca`, `en_kr`, `en_ae` también existen. Errata aparentes en las tablas de suspensión y de motores del Premium AWD |
| 4 | **Rescue Sheet** | `https://digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf` (ID TESLA-2023CA-001, v02, 4 páginas); versión ES: `https://digitalassets.tesla.com/tesla-contents/image/upload/First-Responders-Cybertruck-Rescue_Sheet-ES.pdf` | Materiales (inox, UHSS en pilares, HSS), cristal laminado/templado, lazo de primera respuesta, energía almacenada, emblema Cerbero | Es sobre todo pictogramas; los iconos no llevan texto de ubicación. Listada en `https://www.tesla.com/firstresponders/vehicles-charging` (403 al acceder) |
| 5 | **Catálogo de piezas (EPC)** | `epc.tesla.com` (Wikipedia enlaza `/en-US/catalogs/2816`, sección eléctrica) | Números de pieza, explosionados | No accesible; número de catálogo de Cybertruck por confirmar |
| 6 | Configurador y páginas de especificaciones | `https://www.tesla.com/cybertruck` | Tamaños de pantalla, número de altavoces, color | 403 a herramientas; `tesla.cn/cybertruck` es una SPA sin texto |

### 7.2 Fuentes secundarias útiles

| Rango | Fuente | URL | Aporta | Límites |
|---|---|---|---|---|
| 7 | Teardown de Munro & Associates (Sandy Munro, Tom Prucha) | [The Drive](https://www.thedrive.com/news/the-tesla-cybertruck-engineering-teardown-is-finally-happening), [Design News DesignCon 2025](https://www.designnews.com/automotive-engineering/learn-the-secrets-of-the-tesla-cybertruck-at-designcon-2025), [Lean Design](https://leandesign.com/?p=2341), [prospecto del informe, oct-2024](https://leandesign.com/wp-content/uploads/2024/11/Munro-2024-Cybertruck-Report-Prospectus-Oct-2024.pdf), [MarkLines](https://www.marklines.com/en/teardown/munro-tesla-cybertruck?rf=prtimes) | Estructura, batería, motores, tolerancias; el vehículo era un Foundation Series tri-motor de ~121.000 USD | Muchos datos tras vídeo o suscripción; lista de episodios no verificada; Sandy Munro declaró haber tenido acciones de Tesla |
| 8 | Ingeniería de Tesla: Lars Moravy, Pete Bannon | [Design News (fundiciones y estampados)](https://www.designnews.com/automotive-engineering/video-tesla-s-head-of-vehicle-engineering-discusses-the-cybertruck-s-castings-and-stampings), [Design News (estampado inox)](https://www.designnews.com/automotive-engineering/video-how-tesla-stamps-cybertruck-stainless-steel), [Autopian: entrevista](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/), [Autopian: motores](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/), [Autopian: batería](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/) | 48 V, etherloop, grosores, procesos, motores, batería | Segunda mano |
| 9 | Patentes | Diseño de carrocería (julio de 2021, nº USD sin confirmar) — [Electrek](https://electrek.co/2021/07/27/tesla-cybertruck-design-influences-new-patent/); **D980147** (tapacubos aerodinámicos, concedida marzo de 2023, presentada 21-nov-2019, diseñador Franz von Holzhausen) — [InsideEVs](https://insideevs.com/news/656332/tesla-cybertuck-wheel-cover-patent/); **US11938796B2** (paneles exoesqueleto) y **US20210155086A1** (cubierta tonneau) — [GreyB](https://insights.greyb.com/tesla-cybertruck-patents/) | Seis vistas ortográficas de la forma y de los tapacubos | Números sin comprobar en USPTO; las patentes de diseño son dibujos de líneas |
| 10 | IIHS / NHTSA | [IIHS](https://www.iihs.org/ratings/vehicle/tesla/cybertruck-crew-cab-pickup/2025), [Notebookcheck](https://www.notebookcheck.net/2025-Tesla-Cybertruck-crash-test-results-NHTSA-ratings-more-positive-than-IIHS.1116349.0.html) | Fotos de choque, estructura | Acceso no probado |
| 11 | iFixit | [Topic](https://ts.ifixit.com/Topic/Tesla_Cybertruck), [Device](https://www.ifixit.com/Device/Tesla_Cybertruck) | Teardown y masa | Contenido no revisado |
| 12 | Prensa de especificaciones y agregadores | [Wikipedia](https://en.wikipedia.org/wiki/Tesla_Cybertruck), [Basenor](https://www.basenor.com/pages/cybertruck-dimensions), [ArenaEV](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php), [KBB](https://www.kbb.com/tesla/cybertruck/2026/specs/), [greencarscompare](https://greencarscompare.com/cars/tesla-cybertruck-tri-motor-awd/faq/) | Contraste de cotas | Varias discrepancias; usarlas solo como contraste |
| 13 | Foros y concesionarios | [Cybertruck Owners Club](https://www.cybertruckownersclub.com/forum/threads/speaker-locations-sizes-types.23715/post-403124), fichas de concesionarios | Posiciones de altavoces y cifras de equipamiento | Baja fiabilidad |
| — | No evaluados | GrabCAD, Sketchfab, Euro NCAP (el Cybertruck no se vende en Europa), blueprints, canales de talleres de carrocería | — | Pendiente |

### 7.3 Dónde mirar a continuación (por orden de rendimiento)

1. **Imágenes del CR**: las 5 figuras de `CR-Dimensional` (Side Body, A-B pillar, Under Hood, Rear Body, Top) y los 4 mapas de materiales de `CR-MatAllowed`; abrirlas a mano.
2. **SM Tri Motor**: RDU LH/RH, inversores LH/RH, bomba LH, arneses HV LH/RH, subchasis trasero Dual Motor «Remove and Replace» (GUID AEB42835…).
3. **SM exterior pendiente**: Panel Alignment (ya leída: sin números), Active Grille Shutter y fascias ya leídas; faltan fender flare, rocker, Powergate Fascia, cam block, mid slat, sealing slat, chain link y tonneau motor «Long Range».
4. **SM interior**: leer el 20 % final de cada página (solo se leyó hasta ~100.000 de ~125.000 caracteres) y las secciones de pilares/cinturones para pares.
5. **OM**: secciones de exterior, cámaras, cinturones, almacenamiento (algunas solo vía resumen de buscador) y el PDF completo con `pdftotext`.
6. **Rescue Sheet**: releerla con herramienta de PDF para las ubicaciones de iconos; compararla con la versión ES.
7. **Teardown de Munro**: contar lamas de tonneau, ver casquillos y topes, medir fundiciones, material de la Megabeam y grados de UHSS.
8. **Patentes**: comprobar números en USPTO (D980147, US11938796B2, US20210155086A1) y descargar las seis vistas.
9. **EPC**: localizar el catálogo del Cybertruck (probable acceso con login).

---

## 8. Cobertura del modelo actual y backlog priorizado

### 8.1 Cobertura por sistema (según `docs/component-inventory.md`)

| Sistema de esta ficha | Colecciones del modelo | Objetos | Qué ya está | Qué claramente falta |
|---|---|---|---|---|
| Exterior, cierres, luces | `EXTERIOR_PANELS` 23, `DOORS_AND_HATCHES` 60, `GLASS_AND_MIRRORS` 25, `LIGHTING` 24, `CARGO_BED` 36 | 168 | Aletas, flares, fascias, mud flaps, difusor; 4 puertas con piel, bisagras, cierre/presentador, regulador, juntas, tirante, controlador y percutor; Powergate con bisagras, cierre, amortiguadores y junta; portón con bisagras, cierres, barra de torsión, amortiguador, junta; cristales, retrovisores, limpiaparabrisas, lavado; faros, barras de luz, pilotos; tonneau con 22 lamas, motores, raíles, casete, cadenas; tomas de la caja, anclajes, Gear Locker | Quarter glass delantero; Powergate Fascia, Front Center Applique y front fascia fairings; apliques B/C/techo/backlite/sail baffle; fender flare carriers y baffle de aleta; rocker step reinforcements y Terrestrial Armor (opción); Underhood Apron LH/RH/Rear; Frunk Access Panel, Frunk Lamp, interruptores del frunk, tapas de pernos y topes; Trailer Hitch Cover, matrícula delantera simulada; paredes de caja (Upper/Lower), false wall, front wall, X-member, bed closeouts, Inner Tailgate Cover; cam blocks, hinge pivot appliques, deflector clips, NVH barrier, water-management seals del tonneau; Off-Road Lightbar (opción); glare shield y tira separadora; 8+ clips de bed side wall |
| Estructura | `BODY_STRUCTURE` 33 | 33 | Fundiciones delantera y trasera (mitades L/R), Mast y torres, anillos de puerta UHSS, umbrales e insertos, mamparo, viga del IP, megabeam, viga y absorbedores, travesaños, 72 remaches flow-form genéricos, liners, headers | Super Cowl, Aerobracket; CFM Bracket, Bumper Beam Mount, Fender Beam, Front Drive Unit Mount; Dash Reinforcement y Front Body Bridge Reinforcement; Dash to FUB Gutter Connector; Body Side Outer y C-Pillar Inner como piezas propias; HV Battery Support Bracket, IP Beam Bracket, Power Gate Strut Mount, Rocker Support Bracket, Sail Panel/Datum Bracket, Cantrail Stud Plate y Trim Bracket, C-Pillar Lower Nut Plate; Rear Wall Assembly con crossmember gloves, Rear Seat Stanchion y braces, Tonneau Attachment Brackets; Rear Wheel Arch y extensión, Bed Bridge Bracket, Tie-Down Nut Plate, Tailgate Tower Support Plate, XM Bash Plates; tapones 1870761-00 y remaches clasificados por PN |
| Chasis | `FRONT_WHEELS_AND_BRAKES` 22, `REAR_WHEELS_AND_BRAKES` 22, `FRONT_SUSPENSION` 31, `REAR_SUSPENSION` 36, `STEERING` 12 + parte de `UNDERBODY` | ~135 | Ruedas con llantas, neumáticos, tapacubos, tuercas, TPMS; 4 pinzas, discos, pastillas, escudos; brazos, mangueta, buje, módulos de muelle neumático (fuelle, pistón, amortiguador, copela), bieletas, estabilizadoras, latiguillos, sensores de rueda; subchasis F y R; compresor, depósito, bloque de válvulas, líneas; actuadores de dirección delantero y trasero, tirantes, actuador de realimentación; HCU, servofreno, tubos, depósito remoto | Sensores de altura (4); topes de rebote, casquillos, asientos de muelle; semiejes completos con juntas y botas (hay 4 «halfshaft» pero sin detalle); rótulas y rodamiento traseros como conjuntos; ankle catchers; SCUBA valve block y fill port; haces de líneas LH/RH/Rear; escape del compresor y soporte; muelles de retorno, botas, purgadores de pinza; EPB como motor visible; espárragos como piezas; contrapesos; Skid Plate Stamping |
| Tren motriz, batería, térmica | `BATTERY_ASSEMBLY` 49 (35 de HV), `DRIVE_UNITS` 22, parte de `UNDERBODY` (térmica) | ~68 | Pack con 4 bloques de celdas 4680, espuma, mica, refrigeradores, tapa/bandeja, pirofusibles, vent y flood ports, ACJB, device cluster, last-mile busbar, PCS; FDU y RDU con motor, inversor, caja de engranajes, bomba, filtro, intercambiador, mounts, NVH, semiejes; Supermanifold, compresor A/C, líneas, mangueras, CFM, radiador | Octovalve, bomba de refrigerante, chiller, LCCR, botella de refrigerante y válvulas de expansión como piezas propias (hoy agrupadas en `THM_Supermanifold`); contactores, primer-responder loop, FRL, conectores HV; ground straps, retenes, respiraderos, filtros del reductor; fusibles Eaton EVK22-60-T y Littelfuse 828-30; Schrader/puertos A/C y arandelas; cubiertas NVH por lado; arneses HV LH/RH del RDU y de la FDU como cables separados; mount del inversor RH |
| Interior | `INTERIOR_DASHBOARD` 12, `INTERIOR_CONTROLS` 21, `INTERIOR_SEATS` 37, `INTERIOR_DOORS` 32, `INTERIOR_TRIM` 28 | 130 | IP con top pad, guantera, Airwave, panel inferior, quarter panels; pantallas central y trasera; consola con reposabrazos, portavasos, cargadores Qi, USB; volante, pedales; asientos delanteros y banco; cinturones; guarnecidos de puerta; pilares, cantrails, alfombras, parasoles, retrovisor interior, radar de cabina, subwoofers, altavoces de pilar y cabecera | Super Cowl/Aerobracket/Display Bracket/Downleg Brackets; Airwave Module/Panel Duct, demist y floor ducts; motores del asiento (recline, altura, inclinación), blower de ventilación, espumas, Bridge Track Motor, covers de riel; airbags individuales (pasajero, rodilla ×2, cortina ×2, laterales de asiento) en lugar de `INT_Airbag_Modules`; sensores de impacto (B-pillar, fender, front end, presión en puerta) y de ocupación; cámara interior; TCU y antenas; micrófono de telefonía; Super Horn; tweeters; consola: riser, rails, USB controller, hub; carpet supports; NVH pads; Display Shroud; Footwell Cover; Ethernet diagnostic RJ45 |
| Electrónica, 48 V, sensores | `BATTERY_ASSEMBLY` (LV, 14), `BODY_FASTENERS` 12 | ~24 | Batería de 48 V, 3 controladores de carrocería, 10 mazos, 5 cámaras (B-pillar ×2, flare ×2, fascia) + módulo del parabrisas, 4 interruptores de pilar, cap de ojal de remolque, controladores de puerta | Cámara trasera; cámara interior; ventilador de cámara; Trailer ECU; Gateway (sin hardware propio); MV Controller trasero (LR); Backbone con todos sus clips y cintas; BLE end points (~8); antenas GPS/Wi-Fi/AM-FM/satélite; coaxiales y ferrite core; cubiertas MV con circlip; MV maintainer/jump post; sensores de altura; módulo de salidas |

### 8.2 Posibles discrepancias del modelo con las notas (a revisar)

| Objeto del modelo | Dato del modelo | Dato en las notas | Acción |
|---|---|---|---|
| `EXT_Door_*_CheckStrap` | 3 fijaciones; 35 N·m | Perno del tirante de 23 Nm (Torx T40) | Revisar par |
| `EXT_Door_*_Hinges` | «25/38 N·m» | 2 fijaciones de bisagra a 38 Nm (puerta delantera); 25 Nm es la barra de torsión LH del portón | Revisar |
| `LV_Body_Controller_Rear` | 4 tuercas | 3 fijaciones (2 tuercas 13 Nm + 1 perno 10 Nm) | Corregir |
| `BAT_Enclosure_Tray` | 44 tornillos | ~22 exteriores + 14 interiores + 4 al RUB (LR) | Revisar |
| `CARGO_Tonneau_Slat_01..22` | 22 lamas | El número de lamas no figura en las fuentes | Contar en fotos/Munro |
| `CHS_Active_Grille_Shutter` | 7 lamas | Sin dato (12 pestañas + 2 clips) | Sin fuente |
| `LGT_Front_Lightbar_Optics` | 64 LED | Sin dato | Sin fuente |
| `EXT_Wiper_Blade` | ~1,26 m | 62 in, ~50 in o ~1,22 m según fuente | Marcar R |
| `WHL_*_Tire` | Pirelli Scorpion ATR 285/65R20 | Atribución marca/medida discrepante entre notas | Verificar etiqueta |
| `BATTERY_PACK` | «~800 V» | OM 700 V nominal | Etiquetar nominal 700 V |
| `DISPLAY_CENTER`, `INT_Display_Rear_Screen` | «Verificado» (18,5" / 9,4") | En las notas son R (el OM no da tamaño) | Reetiquetar a R o justificar |
| `EXT_Door_*_Seals` | 26 grapas | Sin dato en las notas | Sin fuente |
| `DU_R_Gearbox` | Carcasa común de dos reductoras | El SM tiene páginas LH/RH de RDU Tri Motor; Autopian habla de un módulo con dos motores | Aclarar |
| `BODY_Casting_Rear_UnderBody_L/R` | Dos mitades | El CR trata el Rear Under Body como un componente con «Half Section» para reparación | Revisar interpretación |

### 8.3 Backlog priorizado de piezas ausentes del modelo

| Prioridad | Bloque | Piezas (rango de ID de esta ficha) | Por qué | Esfuerzo / riesgo |
|---|---|---|---|---|
| P1 | Estructura visible desde fuera (vistas explosionadas) | Super Cowl, Aerobracket, Body Side Outer, C-Pillar Inner, Rear Wall con gloves, Rear Seat Stanchion, Rear Wheel Arch, HV Battery Support Bracket, FDU Mount (EST-003...EST-064) | Son la mayor laguna entre estructura (33) y la lista oficial (~55); nombres y fijaciones V | Medio; forma A (sin cotas) |
| P1 | Cámaras y sensores exteriores | Rear camera, interior camera, camera fan, ride height ×4, BLE ×8, antenas, TCU, Trailer ECU (ELE-020...ELE-041, CHS-011/030) | V por nombre y fijación; piezas pequeñas visibles al abrir | Bajo; forma A |
| P1 | Apliques y carenados exteriores | Powergate Fascia, Front Center Applique, front fascia fairings, apliques B/C/techo/backlite/sail baffle, quarter glass delantero, rocker reinforcement (EXT-003, EXT-012, EXT-025...EXT-028, EXT-103) | Visibles; V por nombre | Medio |
| P2 | Caja y tonneau | Paredes de caja, false wall, front wall, X-member, closeouts, inner tailgate cover, cam blocks, hinge pivot appliques, NVH barrier, water-management seals, deflector clips (EXT-074...EXT-098) | Coherencia de la caja; confirmar 22 lamas | Medio |
| P2 | Interior detallado | Motores y ventilación de asientos, airbags individuales, sensores de impacto, ducts HVAC, IP substructure, consola interna, speakers, TCU/antenas (INT-001...INT-095) | Más de 170 nombres V; el modelo tiene 130 objetos | Alto por volumen |
| P2 | Tren motriz y térmica desglosados | Octovalve, bomba, chiller, LCCR, botella, contactores, FRL, fusibles, ground straps, respiraderos, filtros, NVH covers (TRN-005...TRN-049) | Hoy agrupados; nombres y pares V | Medio |
| P3 | Suspensión: casquillos y topes | Bushings, bump stops, spring seats, boots, rótulas (CHS-003, CHS-S) | Sin fuente de forma; A | Bajo valor sin fotos |
| P3 | Opciones | Terrestrial Armor, Off-Road Lightbar, tonneau variantes | No son de serie | Solo si se quiere modelar la gama |
| P4 | Clips, tapones, grommets y tornillería con PN | Tapones 1870761-00, clips de belt, cintas de abrasión, remaches por familia, grommets de válvulas | Fidelidad máxima; nombres y cantidades V | Alto volumen; instancias en lote |
| P4 | Variantes de fecha | Sail applique nuevo, NVH barrier 2 piezas, TPMS negro | Solo si se modela una versión concreta | Bajo |

Orden sugerido de trabajo: (1) cerrar los huecos 1-4 de la sección 6.2 en los manuales; (2) resolver las discrepancias de 8.2; (3) añadir P1; (4) validar en el visor y regenerar `docs/component-inventory.md`.

---

## Anexo A. Registro de fuentes

Cada código del texto se resuelve como `base + GUID + .html`. Los GUID que acaban en `…` están truncados en las notas originales; los códigos `SM-IP/xxxxxxxx` llevan solo el prefijo de 8 caracteres y se localizan en el índice del SM.

**Bases**

- `SM`: `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/`
- `CR`: `https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/`
- `OM`: `https://www.tesla.cn/ownersmanual/cybertruck/en_us/`
- `RS` (Rescue Sheet): `https://digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf`
- `OM-PDF`: `https://www.tesla.cn/ownersmanual/cybertruck/en_us/Owners_Manual.pdf`

**Service Manual: índices y secciones**

| Código | GUID |
|---|---|
| SM-Index | `index.html` (sin GUID) |
| SM-TOC | `GUID-2390C88D-E2A0-4DDB-814D-C03532250D36` |
| SM-Bumper1001 | `GUID-A76646E7-DF66-4716-BFE4-8770F4D37695` |
| SM-BodyPanels1010 | `GUID-03E5CC62-C5C2-49FA-A3BE-6E9C1310C0E8` |
| SM-Glass1020 | `GUID-79DFDD24-B74D-4765-BA26-995C9D75BA3B` |
| SM-Tonneau1120 | `GUID-D284C287-577D-42B9-9D6D-6E33E689938D` |
| SM-Closures1133 | `GUID-CA414463-1C4F-4F5E-82E8-F714AD66BEE9` |
| SM-DoorGlass1150 | `GUID-830DA2E9-792D-40E7-ACCB-FC090D619987` |
| SM-Seals1170 | `GUID-CA7A555B-BAC8-4B28-9BD0-1B110F79C1CC` |
| SM-Fittings12 | `GUID-B1EC1800-938E-4623-8459-B4723361D57C` |
| SM-Handles1145 | `GUID-764B4AA2-CB1A-4FCA-826D-121768FCD2AE` |
| SM-1630 | `GUID-5DA3FE21-AC08-47AA-9DC3-B57AB94474F3` |
| SM-1710 | `GUID-AE3DBEBE-CE1D-49E6-8569-ABA5D438C7A1` |
| SM-MV1702 | `GUID-CAD6C7F5-D10C-45DE-AD50-1A1DA7ABD7C9` |
| SM-Thermal-1840 | tres páginas de índice térmico: `GUID-F1BA8698-924F-458F-A2F4-AD55234544AE`, `GUID-B2A8FCB0-28AB-4002-9192-2B6EBF4EF5E8`, `GUID-C4D37B9C-F199-437B-BFA0-5DE846CAEFC8` (las notas no dicen cuál es cada sección) |
| SM-Washer1750 | `GUID-C05A63F9-2772-49CA-B675-AFA4A1F5BE43` |
| SM-Cameras (1722) | `GUID-95D5F24D-9C59-47A6-9720-7EE0D836E59D` |
| SM-2107 | `GUID-2BF7DFB6-ABB3-44F4-95E8-45FDDB50E85C` |
| SM-Safety20 | `GUID-0267F40C-5BC9-4B29-9700-435FAF6F9C73` |
| SM-Audio2121 | `GUID-2C54A736-E145-4604-88E1-FAFF9F1429CF` |
| SM-HVAC1810 | `GUID-CE9B07AA-9C0A-47CB-B102-99C8295C165D` |
| SM-Seats | `GUID-35238824-6CAA-42C1-BEDA-D8EDCB543972` |
| SM-IP/… | prefijos de 8 caracteres citados en 3.5.1-3.5.3 (índice del SM) |

**Service Manual: exterior**

| Código | GUID |
|---|---|
| SM-Lightbar | `GUID-4A605514-9F14-4377-A650-E152662396B1` |
| SM-Headlamp | `GUID-AA106AB5-27B0-48B1-86CA-A64E9D18F205` |
| SM-Windshield | `GUID-28743D4C-E164-4741-8C95-D09F014DC857` |
| SM-PowergateHood | `GUID-95384AD1-EF10-4818-8AAB-D95BD4C0E3BF` |
| SM-Tailgate | `GUID-FF063878-877C-49EC-BFE0-B51DAEF02984` |
| SM-FrontDoor | `GUID-BDD33A91-1786-46E8-82C6-2AA75334F500` |
| SM-DoorPresenter | `GUID-41B57474-80F4-47A5-8370-DAAA820F286F` |
| SM-Mirror | `GUID-E5FC5791-2CCB-49E2-A210-2300460B0063` |
| SM-TailLamp | `GUID-6A31AA5F-83BD-4CE3-B32C-DDDB56EA87F5` |
| SM-TowHitch | `GUID-BD1223F7-BA44-4CD9-852C-7CABC4382CB2` |
| SM-Fender | `GUID-BF8EBD82-4585-425A-9A61-117B82361D68` |
| SM-TonneauRail | `GUID-5A374D49-E188-4AB9-B8CC-75B48347C047` |
| SM-MudFlapF | `GUID-5070A3E5-A51D-4A86-B72F-10A852F30172` |
| SM-MudFlapR | `GUID-0677EC66-A005-4CA2-A48C-22F5845532EA` |
| SM-SkidFront | `GUID-B0F7244F-0D90-4781-A7C4-C4279FC261D9` |
| SM-SkidRear | `GUID-855C1F35-5C9B-45C9-8268-94AC3AA811DF` |
| SM-FrontFascia | `GUID-A16857F8-F171-4E7A-B9FF-EBDCFC404662` |
| SM-RearFascia | `GUID-7E9F0603-DD47-4BA8-9416-2B7BB71F93BA` |
| SM-BumperBeam | `GUID-3F3AB49B-DFD2-4F7F-A969-64AA4141EE5C` |
| SM-GrilleShutter | `GUID-52FFCD97-8084-4A6F-815E-4778CD86F3C8` |
| SM-HitchCover | `GUID-C993F318-E005-4F54-8022-1B6552A33E89` |
| SM-AeroFront | `GUID-6BFCB7BA-2709-49A1-A389-1725AAD0B5B4` |
| SM-AeroRear | `GUID-3B8ECAC7-00E6-4C36-9FFA-A8DA35321DAF` |
| SM-Diffuser | `GUID-4E1B894F-F5A8-4D08-B7D2-5EE2E7443E49` |
| SM-WheelLiner | `GUID-423EB6D6-17F0-4D29-ADE2-355DFDE99317` |
| SM-TerrArmor | `GUID-06478A14-27E7-4B37-BB36-DFB1C9D022EF` |
| SM-WiperMotor | `GUID-8FE8CAF6-8AFD-44EF-87A7-04B6D4C2E85E` |
| SM-WiperArm | `GUID-BD6E78E3-9B88-4F20-940F-068717D81EA2` |
| SM-WasherTank | `GUID-69839958-98A2-422C-8010-F77FEF0266CB` |
| SM-WasherPump | `GUID-DE8BE048-BCDD-4023-AE83-26EE110C0598` |
| SM-ChargeDoor | `GUID-FF433CAC-486B-4783-AE82-346E0E5B592B` |
| SM-BedOutlet | `GUID-AF2D2AF9-6B4D-48BA-BB0A-F9C382952D99` |
| SM-WinRegQ | `GUID-2639676F-C24B-4B71-903A-7499FB5C81F4` |
| SM-WinRegFL | `GUID-CAC872D6-ADA7-4A31-9806-4C2EAF0C2523` |
| SM-DoorLatch | `GUID-0A5DA3B2-6220-47CF-87F9-879DEA217CB8` |
| SM-DoorSwF | `GUID-4FC2DC9E-08BC-4932-88AD-27729199DB10` |
| SM-DoorSwR | `GUID-6A148722-9FD0-4A90-AE04-28C5A07063D1` |
| SM-ApplBPillar | `GUID-DB61B43D-3A22-4C69-AA6A-F7DCC6BF217D` |
| SM-PGHinge | `GUID-9CAEF904-8AD2-43CB-B822-01D0DE09F064` |
| SM-HoodLatch | `GUID-1B45E27F-8045-496F-BDF7-EB1CBF52C107` |
| SM-PGStriker | `GUID-E141B157-8103-4350-A558-D30D5151138B` |
| SM-HoodStrut | `GUID-8ABA2C08-0DDB-414F-9A2B-EC843EE8ACF5` |
| SM-TGLatchHinge | `GUID-94424E41-666D-4895-9C68-4CE1EF984200` |
| SM-CinchLatch | `GUID-D3D1B511-E395-449E-9FC0-8BE998DEF1D5` |
| SM-TorsionRod | `GUID-0AC61785-B118-4F84-9E20-83D08BFAF351` |
| SM-StrutDamper | `GUID-19C43AF3-E8DB-415D-8CA1-9F9E782615AD` |
| SM-TonneauMotor | `GUID-A1ABAD22-5BC1-493C-BE53-45E6F69EB5A5` |
| SM-HorizonRail | `GUID-A46B3B20-99B0-4D0F-BA20-F5E84C2A46AB` |
| SM-FlatCassette | `GUID-A1806587-2D81-4459-B4F6-E3BD90ACC325` |
| SM-SlatSystem | `GUID-D62653D5-6BC1-4228-8CE6-3B3A214F14C2` |
| SM-TonneauLower | `GUID-1F4DCB6D-2EED-4E16-9A58-8C44576EF370` |
| SM-BedLight | `GUID-8A286466-7C40-4935-BEAE-6530BEE1E957` |
| SM-LampTailgate | `GUID-9EBA9FBD-50F5-4152-AD09-A74D630E327C` |
| SM-ReverseLamp | `GUID-4D8BC614-1684-4E8E-9F0D-D6842026AA22` |
| SM-RearMarker | `GUID-71A94B92-2E99-46E5-8BFC-FE835E5DCEF0` |
| SM-LPLamp | `GUID-DE238748-9246-457D-9BC0-CE3FADB13BFD` |

**Service Manual: chasis**

| Código | GUID |
|---|---|
| SM-LCAF | `GUID-435FE15C-197E-4FA9-804D-A74A81C2C81E` |
| SM-LCAF-LR | `GUID-49C2A2E5-C111-4A9C-AE11-5D3B09B32B3C` |
| SM-UCAF | `GUID-EB40116C-759A-4065-B13D-14F96194C2E1` |
| SM-UCAR | `GUID-9BDBAF7A-BB1F-4C85-846C-EA41A4458A17` |
| SM-LCAR | `GUID-A86B108E-9A2B-42B8-AD4D-832C2FCE07B5` |
| SM-ASMF | `GUID-B4C471DC-4443-441D-ADDF-D905AA3EF3C7` |
| SM-ASMR | `GUID-BAACC9E3-8DFB-462B-9BBC-23C87ED3AB47` |
| SM-KNF | `GUID-029EBAA8-D2FD-4B4A-BB16-A78EC560321E` |
| SM-HUBR | `GUID-C1E25DA8-92F9-4A7E-80B3-4C53F0E288A8` |
| SM-SBF | `GUID-2BF0E977-6CDF-439D-9DD4-17A49DEA6632` |
| SM-SBR | `GUID-6FDF63DE-13D1-4FCC-9F64-6206AC233A9D` |
| SM-SFF | `GUID-794CE60D-61DE-4B22-A99B-6DB0A31A8590` |
| SM-SAF | `GUID-31B58FA2-A075-4A5E-BA95-72E24C8F7BE4` |
| SM-SAR | `GUID-C75A9806-3F4E-4D6B-9466-72F15106C035` |
| SM-SteerGearRear | `GUID-2C9F1065-2896-42D6-BDAD-E3BCB65E81A6` |
| SM-SFA | `GUID-0CA501BB-0F16-4991-998F-2A0A9543FA45` |
| SM-TRI | `GUID-2009256A-26B5-4EF7-AD4D-C0E7A191986C` |
| SM-ToeLink | `GUID-5FDE24EE-24CE-4721-8C77-2E23AF3EDBE1` |
| SM-SteerJumper | `GUID-1345E3F0-EEA6-4715-8543-496962FCD4B9` |
| SM-RearSteerJumperLR | `GUID-1A0458EA-151E-458D-A1B2-69F3C00C2B1A` |
| SM-CALF | `GUID-8CD379E5-9703-4951-9B67-60C3171129AF` |
| SM-CALR | `GUID-A122A921-BF45-4A89-B5D2-41364B38779D` |
| SM-ROTR | `GUID-8DA0BAEA-7807-4F7F-ACF9-FB3D3FF40A7B` |
| SM-BRK | `GUID-1D03EF6F-5DD6-4539-A664-9C784492A8E2` |
| SM-CMP | `GUID-51C72CFF-62A1-4F17-8180-4129F9E573C9` |
| SM-VB | `GUID-5F6BC136-4578-417B-B24A-638E63353871` |
| SM-RSV | `GUID-620A7266-D2F1-4118-B379-1BBE57869216` |
| SM-SCUBA | `GUID-707B2753-C49B-40E9-92D8-BE90EA4FE140` |
| SM-AIN | `GUID-581F76D7-4DB4-4CE5-93D1-87B37AAC45B8` |
| SM-ALIGN | `GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4` |
| SM-Susp | `GUID-A7180897-7F9B-48B2-869D-525BB3DAF07F` |
| SM-Wheel | `GUID-69690B5B-7C41-40FD-A6D3-FC17B5FBDB66` |
| SM-Subframe-R-TM | `GUID-A4F3E974-4AB0-4101-989A-21DDF99202FB` |
| SM-Subframe-R-DM | `GUID-39E00821-017A-482A-AA05-1FC7B003275C` |
| SM-UnderbodyTorque | `GUID-F37882B9-9E45-4F3C-9452-7BF9DDC0FC81` |
| SM-RecoveryHook | `GUID-753930B8-ADC1-4C5C-89E8-34BEA21AA9AE` |
| SM-RearEA | `GUID-450C3E03-BCC1-4AFC-8996-C47D23FFEDF4` |
| SM-Megabeam | `GUID-5C533F8C-3E30-4EE2-9794-21D406893407` |
| SM-FluidCap | `GUID-136927CC-901C-4C28-987F-1074223AC781` |
| SM-Fluids | `GUID-A86EE40B-CA89-494E-A084-B855E34AC574` |
| SM-WeightInfo | `GUID-B8B4D7C3-E26D-46B2-B09A-E1B6BC0BBBCF` |
| SM-RideHF | `GUID-682854E8-4212-4E90-826C-94FF09EDBE4F` |
| SM-RideHR | `GUID-1C0B0820-0C85-493E-9678-78434EAE5522` |
| SM-TPMS | `GUID-99EA70AC-F1F9-43B3-9428-C747C03AAE5A` |

**Service Manual: tren motriz, batería, térmica**

| Código | GUID |
|---|---|
| SM-FDU | `GUID-47A039C2-5509-47BA-83A1-2058CF3C67A2` |
| SM-HalfshaftFL | `GUID-9216B93E-5C78-49C4-A0F6-068666761C08` |
| SM-HalfshaftsFront | `GUID-FFC01D33-7140-43C3-8291-39E9BE351CE0` |
| SM-FOilPump | `GUID-DB3DCC55-1004-4B1E-ADF1-8577ECB06EDE` |
| SM-FHeatEx | `GUID-566F0C00-FA93-4D89-851A-815B36A5463F` |
| SM-FGearFluid | `GUID-8130467F-7764-4BF8-82E6-319EDBAE36D1` |
| SM-RDU-RI | `GUID-AD6E7236-3510-49ED-9B80-6382667074CA` |
| SM-RDU-RR | `GUID-B38C881E-1281-466E-A66E-2DF3CA573C49` |
| SM-RHalfshaft | `GUID-8B961BB8-A23B-4B5E-9BAC-FAFDA52BF4DF` |
| SM-RMotorMount | `GUID-B9080049-BD89-46E8-B378-54EB8558D668` |
| SM-ROilPump | `GUID-6ED50306-498C-4269-A688-B7A7ED1E5244` |
| SM-ROilPumpTM | `GUID-F05C97C5-00E2-4D06-A52C-2C81ED6D927C` |
| SM-FOilFilter | `GUID-058DE3A8-DB38-4CDA-AB5F-33AFD2FE85A8` |
| SM-ROilFilter | `GUID-AA7647B7-A4C7-4B9D-9AA5-DAD3D994FEE9` |
| SM-HVHarnessFDU | `GUID-49C49CBB-B604-4716-A8FD-9022E3EA8217` |
| SM-HVHarnessRDU | `GUID-C7E99D5B-D1E1-4EF3-B4B9-B764A6BE1BE4` |
| SM-HVHarnessRDU-L | `GUID-F4491A6D-98C2-43B9-B403-25C16385CB70` |
| SM-HVHarnessRDU-R | `GUID-B6956D4A-C680-4A0F-BA74-6131B48FE29C` |
| SM-HVBattLR | `GUID-D3E09C6D-D7C0-4B32-99DC-978163028DEF` |
| SM-HVBattAWD | `GUID-D6F2FED3-46D3-4915-8D55-C47633D5739C` |
| SM-Pyro | `GUID-828B37BC-A40A-440C-BA7D-7B6E622ACD9D` |
| SM-Fuses | `GUID-640D91ED-4713-4A2E-A12F-40854CBF2F99` |
| SM-AncFuse | `GUID-45986159-E5DF-45C1-ABF6-96E6999ACF44` |
| SM-PCSFuse | `GUID-8C4618B2-87C6-422E-8CF8-4571C08ECCED` |
| SM-LastMile | `GUID-CA82FD25-8997-4FD2-8EF8-8C0F82F1C53A` |
| SM-ChgBus | `GUID-3BF96D09-6DF7-401C-BA93-F2AC82564EC0` |
| SM-ChgVoltCheck | `GUID-D32D2226-FCF5-4FA4-9BB7-8666B594BFEB` |
| SM-PCS-LR | `GUID-A78D3394-E837-4960-9EBF-41BC37F7A51A` |
| SM-PCS-RR | `GUID-8F133FA6-44FC-4D62-9BD3-03C92951B916` |
| SM-Refrigerant | `GUID-9D760C9C-F95C-4D58-AF74-AFFC330168B0` |
| SM-Flush | `GUID-B1831D39-D817-485C-8ED8-4C32042A1BA5` |
| SM-ACComp | `GUID-EC799465-6989-44B2-B722-EE04F7F533C8` |
| SM-Octovalve | `GUID-12EE5DD0-FB31-4EDA-8F2D-D28A1DC00CB6` |
| SM-CoolPump | `GUID-B4481962-AD1D-404E-9087-F5BE7DF2E100` |
| SM-Chiller | `GUID-D131CB52-2E0F-441F-B46B-3B880EAF5728` |
| SM-LCCR | `GUID-FAC16ECE-F2C6-48CC-879C-666C2A9DD363` |
| SM-CFM | `GUID-CE0EE886-A065-442E-8944-97429812878B` |
| SM-CoolantDrain | `GUID-572AEDB1-54B5-4DF4-89EF-A8B53E4D28E1` y `GUID-F1AD9C0B-AB56-4423-AB30-70C85E855F46` |
| SM-HoseHV | `GUID-34BAA5A1-C6A0-4463-9B21-B3BA3CA5D154` |
| SM-Pentaport | `GUID-38F1B41A-55D7-497E-902D-F27700522487` |

**Service Manual: electrónica e interior (GUID completos disponibles)**

| Código | GUID |
|---|---|
| SM-BodyCtrlLH | `GUID-FD1546CE-ACC3-4AEF-9A51-34EE83B74A11` |
| SM-BodyCtrlRH | `GUID-7681A5AD-6E93-48D9-8924-861417E85FBC` |
| SM-BodyCtrlRear | `GUID-4F31E5D8-E90F-4FB4-9C48-85273C55D2A9` |
| SM-DoorCtrl | `GUID-541FC373-4447-4C5B-8137-AD1A130D5580` |
| SM-TrailerECU | `GUID-4F16A681-C61F-4AE1-9F9D-28DCB4EB38E0` |
| SM-ChgPortECU | `GUID-F6CFA714-2B06-46CA-B00A-E5EEF98CC2C8` |
| SM-CarComputer | `GUID-31C827EA-9774-4DA2-8C78-62AA54921A26` |
| SM-TCU | `GUID-92242BB9-667A-4844-AAB8-F777DEB7D34E` |
| SM-RCM | `GUID-ABCBBC20-08DF-4C69-974D-358ABD420EE8` |
| SM-RadarCabin | `GUID-7D971414-00EB-4276-B6B1-C075B08D5E5B` |
| SM-MVBattery | `GUID-F6BB141A-3615-41DE-A7C7-4DDF405C9C21` |
| SM-MVMaintainer | `GUID-4FB4FC9C-2C92-47C8-9678-2995E0AE02F1` |
| SM-MVPower | `GUID-A399E8AE-5DCF-4095-91FA-AF0148503F3B` |
| SM-MVBackbone | `GUID-46127373-87F7-4A12-83EF-CD31253C10FB` |
| SM-BiCam | `GUID-D7DBFAB2-B822-4051-9200-A1414928D25C` |
| SM-FasciaCam | `GUID-07DCD57C-0730-43B1-9CB7-0B186735EEA8` |
| SM-BPillarCam | `GUID-E6C8E548-643C-4084-96ED-03604774BCA4` |
| SM-FlareCam | `GUID-95E55C49-6B1C-40FE-AA1C-BAAC70041ABE` |
| SM-RearCam | `GUID-062E2BE8-FA1E-41BE-8262-63BEA29EB7AE` |
| SM-IntCam | `GUID-517B6C63-EA55-49A6-BB38-4B2D43648DB4` |
| SM-CamFan | `GUID-43665804-4C50-4E53-A925-8662960EE074` |
| SM-GPSAnt | `GUID-28C15B60-B608-4404-A4A9-6E5425A6F5B9` |
| SM-FMAnt | `GUID-26F6BEB6-B751-409B-AF47-ADD3062B3B94` |
| SM-BLERear | `GUID-1E2BC0A1-95F3-4AEF-B6A9-3FB7A4DC5700` |
| SM-BLEWell | `GUID-942C7956-ADEF-4501-A5DC-BA5437F8BEA1` |
| SM-PedSpk | `GUID-A7818764-BE16-466F-8D8C-F90E86D28927` |
| SM-Glovebox | `GUID-D8CCB803-F5A5-4B72-8BE8-16E498EA98CA` |
| SM-Console | `GUID-BAEBEF6F-9265-43F8-88FE-1CCB145EAAC6` |
| SM-ConsoleRI | `GUID-583518A9-ED30-48E1-AFCB-6112343020FB` |
| SM-Seat1 | `GUID-3D275EB4-0894-41D7-A709-125A36EE8491` |
| SM-Seat2 | `GUID-38DF85AE-F0DA-4B85-820B-157A6B00986A` |
| SM-DoorTrimF | `GUID-5FF58081-E522-4ED4-AAAE-227408A5133D` |
| SM-Header | `GUID-98CEF5F5-26A4-41CA-8E5F-3011E9644607` |
| SM-Blower | `GUID-D7D1314F-DC25-4808-8125-99F9D2E90A18` |
| SM-RearDisplay | `GUID-246FEAA1-B833-4044-818F-F2D26B2042AB` |
| SM-DriverAirbag | `GUID-3DA963E4-87CA-423A-8155-02EF2B103505` |

**Collision Repair (CR)**

| Código | GUID |
|---|---|
| CR-MatAllowed | `GUID-B4A61C9E-4CE2-4D9A-B9B3-B6D74EEFE038` |
| CR-Structural | `GUID-C73E4B36-F7F0-4CA0-87F4-705A45D7D788` |
| CR-Sectioning | `GUID-50A9DAFE-D84D-48C6-810C-AE3B7BB95D05` |
| CR-FUBcast | `GUID-C1914222-086E-4604-809F-1ECB9A0F6F53` |
| CR-RUBcast | `GUID-A839FDF1-F60E-44E5-ADFB-5B7A220C945C` |
| CR-Mast | `GUID-112E876E-DB80-4614-8B4E-F6F54AA9C4F8` |
| CR-TGTowerGuide | `GUID-9CD66714-3A98-49BC-B31C-06938B4D6DA6` |
| CR-Stainless | `GUID-D33D78C9-9BCD-46CB-885C-52B4F482852C` |
| CR-FUB | `GUID-B113826C-1A8D-4AA3-BE16-40B3FB83870A` |
| CR-FUBsmall | `GUID-3E9AE471-00F8-4351-99EF-455E3CC3DA0A` |
| CR-Dash | `GUID-73B5ACF2-CC64-4A29-A5C6-400913CC2986` |
| CR-FBBR | `GUID-28FA070F-B8F6-4625-8A6F-C7C50EBBA965` |
| CR-FDUMountL | `GUID-6E692237-B0BE-419E-8AE3-53847CB3A206` |
| CR-FDUMountR | `GUID-72BD8A48-571B-4A18-8EA9-C8CF434E29EB` |
| CR-FenderBeam | `GUID-195D0181-D206-4C0E-A0AA-A6CD30208D43` |
| CR-BumperBeamMount | `GUID-98A44CFE-8761-45CD-AE86-EEEC49C8D17B` |
| CR-Gutter | `GUID-C9399BA0-1711-4022-AB57-F0EC9D36CC6D` |
| CR-CFMBracket | `GUID-259A7A0D-31D3-459D-930A-4EEB449BA004` |
| CR-BodySide | `GUID-AAE3C22B-CBF5-4CF0-8427-F960A41E3DE9` |
| CR-BSO | `GUID-F83C624F-13D4-4C3C-99A3-AD52857C3403` |
| CR-CPillarInner | `GUID-FB686750-7B16-45B2-876D-375981FBC53E` |
| CR-CPillarNut | `GUID-D4B984A6-1365-4D57-BE72-18344C2C6938` |
| CR-CantrailStud | `GUID-EBA81A11-429A-40C9-A356-277BE584F4B8` |
| CR-CantrailTrimBkt | `GUID-58814D7C-1184-4609-9BEE-01051F987EBC` |
| CR-FQW | `GUID-0CBA4CBC-FC0F-4163-8778-89712C248EFF` |
| CR-FQWOuter | `GUID-E6455D9C-A0C1-4FFE-87E6-1D8D1D68E7A1` |
| CR-HVBracket | `GUID-B4CAB3E6-3556-40E8-8586-10744989795C` |
| CR-IPBeamBkt | `GUID-4EBD56B6-558A-41C0-8CA3-DF81B20D358B` |
| CR-PGStrutMount | `GUID-79118AE1-30C8-4666-8E63-FF4575B1300C` |
| CR-RockerSupport | `GUID-C2530069-89E2-4CBC-8F0B-FC80226516EF` |
| CR-SailPanelBkt | `GUID-2DB1CB43-1C29-4E03-AD36-F06D51E2D20D` |
| CR-SideSill | `GUID-F7FF4CF8-DDC8-439F-B656-453CC21A05C5` |
| CR-RUB | `GUID-B0B31EF5-A87A-4AAD-AC35-B4B268807556` |
| CR-RUBsection | `GUID-949F33FC-FA69-442B-B895-69F6ABD44792` |
| CR-RUBrail | `GUID-0611074E-4F3C-417E-86AB-5BBC588393CC` |
| CR-MastAsm | `GUID-5E2DE223-5642-43AE-899E-29A771447B13` |
| CR-MastSect | `GUID-48F9633A-45C7-4E76-861D-B91CF99A58C5` |
| CR-TGTower | `GUID-2CEAA19D-88FC-4AB4-AD97-5CD8388E0E6B` |
| CR-TGTowerPlate | `GUID-38C1CCF5-3D33-442D-A074-25130395BE97` |
| CR-RWArch | `GUID-C987B794-5A9C-46BD-9C4F-69C56586E44B` |
| CR-RWArchRear | `GUID-7AEB114C-42D5-47EF-BB6D-0DA5DF876EB3` |
| CR-RWArchExt | `GUID-73A9B0D4-0779-447E-A3EC-C67528B68A8D` |
| CR-BedBridge | `GUID-DFA8DD4B-7757-4810-9901-A81CFA4CAE2A` |
| CR-RFasciaBkt | `GUID-BBE01AF0-636B-4644-9D69-EC8297FB7D0D` |
| CR-SailDatum | `GUID-CE8950DB-EF5C-4874-91C1-4F5DAA65B890` |
| CR-TiedownPlate | `GUID-C4480139-50C0-4305-A017-4341ECB376F4` |
| CR-RearWall | `GUID-D3BE5950-43B3-4EE0-8ECF-A84C33722A1C` |
| CR-RWLowerGlove | `GUID-26CC2A21-B159-46FC-801D-9A67EC476A5F` |
| CR-RWUpperGlove | `GUID-FE53D38B-462F-4C54-AE07-8B6E01F5F189` |
| CR-Stanchion | `GUID-8AE6D991-4847-47B4-BD6B-D42A9D505B2C` |
| CR-StanchionBrace | `GUID-2E4068B7-0AD8-4026-8D7E-60E23E87B347` |
| CR-TonneauBktL | `GUID-F268886D-FA6F-4CCD-B8E2-D591DDE288F3` |
| CR-TonneauBktU | `GUID-A4FE7F64-93AB-4DF7-9D35-65545A3267D1` |
| CR-HdrFU | `GUID-B3CA601A-40FE-4E62-86C2-81BF946E66D3` |
| CR-HdrFL | `GUID-E5612BBC-CF8B-4B6B-81D7-2D46575DE42B` |
| CR-HdrGusset | `GUID-AA25756A-C263-457B-BBAE-85C174F454F2` |
| CR-HdrRL | `GUID-35720B29-7A65-44CB-A14C-12F9123F2434` |
| CR-HdrRU | `GUID-AB678C76-3D94-4D47-BC0B-C1217F79C104` |
| CR-Fasteners | `GUID-02989E68-695F-4E9B-8C94-BBD580C5E4D0` |
| CR-FlowForm | `GUID-251653EC-9283-4E1C-B1BB-7C2E60A02EA5` |
| CR-Chemicals | `GUID-EF1DD38B-6C21-4850-BF26-1B09ECB62454` |
| CR-Dimensional | `GUID-C5797770-FD0F-4A21-90C1-FC4E47976C95` |

**Owner's Manual (OM)**

| Código | GUID |
|---|---|
| OM-Dimensions | `GUID-12A976DD-EB60-431B-AFF1-5A37E95006DB` |
| OM-Wheel | `GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7` |
| OM-Subsystems | `GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB` |
| OM-Cameras | `GUID-60A2EFBA-78D7-47BB-BCDE-77582529EB48` |
| OM-InteriorElec | `GUID-7B00E438-94C4-4B66-BBEB-0C39C70777DC` |
| OM-Touchscreen | `GUID-9A3B88F2-55FA-46C7-9ACA-6236EB8487F8` |
| OM-SteeringWheel | `GUID-46420EE2-F6B0-4E95-88D5-E50CB3061101` |
| OM-Seats | `GUID-05848570-CDFC-466F-9479-FE3F29DB893A` |
| OM-Airbags | `GUID-F023E8E7-C077-4C75-B7EB-D1A133E41938` |

*Ficha generada a partir de las notas de investigación del 2026-10-17 y del inventario del modelo; todas las cifras proceden de ellas y no se han añadido datos nuevos.*
