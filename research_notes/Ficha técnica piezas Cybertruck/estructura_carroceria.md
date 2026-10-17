# Estructura de carrocería (body-in-white) y subestructura del Tesla Cybertruck (EE. UU., 2024-2026, Cyberbeast)

Convenciones de este fichero:
- Base URL del manual (todas las filas "GUID" se refieren a ella): `https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-<GUID>.html`. Índice: [Cybertruck Collision Repair Manual](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html). Las páginas llevan fecha 2026-08-10.
- Confianza: **V** = Verified (texto del manual oficial de Tesla), **R** = Reported (prensa/teardown de terceros), **I** = Inferred (deducción mía, ver sección Inferences).
- El manual de Tesla NO publica material/grado por pieza en texto (el mapa de materiales está en figuras-imagen) ni valores de cotas de control (están en imágenes). Lo que sí da en texto: cantidades de fijaciones, pares de apriete, números de pieza de tornillería, cotas de colocación de remaches, límites de reparación de fundición.
- Los datos del manual no distinguen Cyberbeast de otras versiones salvo "HV Battery (AWD)", "Subframe, Rear (Dual Motor)" y "Bed Side Outer Assembly (Long Range)" en las listas de desmontaje; para el modelado, la estructura de carrocería es común a todas las variantes.

---

## 1. ¿Qué lista el manual de reparación de carrocería de Tesla (materiales, uniones, secciones sustituibles, puntos de control)?

### Takeaway
El manual oficial da la lista completa de piezas estructurales sustituibles (≈55 procedimientos), con cantidades exactas de remaches/tornillos, pares y números de pieza de tornillería, pero el mapa de materiales por pieza y las cotas de control están solo en imágenes (no extraíbles como texto). Unión dominante: adhesivo estructural + remaches estructurales de 6,5 mm / flow-form (S08-S68) + tornillos, con soldadura por puntos solo en piezas de acero concretas; el acero inoxidable no admite soldadura.

### Cited Findings

#### 1.1 Materiales y operaciones permitidas
- Categorías de material de la estructura: aluminio 6xxx, aluminio extruido, aluminio fundido, acero suave, acero de alta resistencia (HSS), acero de ultra alta resistencia (UHSS), acero inoxidable. — [Body Structure Materials and Allowed Operations](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B4A61C9E-4CE2-4D9A-B9B3-B6D74EEFE038.html) (V)
- Aluminio 6xxx: límite elástico 230-280 MPa; calor máx. 212 °F (100 °C); reparaciones soldadas en paneles de espesor <= 1,2 mm; agujeros GMA hasta 12 mm en cierres (puertas, capós, portones) y 8 mm en Body Side Outer. Aluminio extruido y fundido: calor máx. 100 °C, reparaciones solo según procedimiento de cada componente. — misma fuente (V)
- Acero suave: resistencia a tracción < 270 MPa; HSS: 300-700 MPa; UHSS: > 800 MPa (no reparable salvo que lo permita la guía de reparabilidad; taladrar con brocas de carburo de tungsteno o boro). Acero inoxidable: soldadura NO permitida; solo refinishing de arañazos. Calor máx. acero 1200 °F (650 °C), 2 aplicaciones/90 s. — misma fuente (V)
- Adhesivo: no calentar por encima de 100 °C (212 °F) salvo para retirar el panel. — misma fuente (V)
- Piezas con sensor de impacto acoplado: se sustituyen, no se reparan. — misma fuente (V)
- No se permite tirar/empujar con bancada de estirado piezas unidas (adhesivo, soldadura, remache). Prohibidas piezas usadas/recicladas/aftermarket. — [National Collision Repairer](https://www.nationalcollisionrepairer.com.au/tesla-releases-cybertruck-repair-procedures/) (R)
- Nota de seccionado: no cortar a menos de 25 mm del centro de un taladro de tornillo. — [Sectioning Guidelines](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-50A9DAFE-D84D-48C6-810C-AE3B7BB95D05.html) (V)
- El manual lista cuatro métodos de soldadura en su tabla: Spot Welding (STRS), GMA Welding, Plug, Butt Joint; la soldadura solo la hacen técnicos con formación Tesla y tras el procedimiento de desactivación HV. — [Body Structure Materials](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B4A61C9E-4CE2-4D9A-B9B3-B6D74EEFE038.html), [Body Side Complete](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-AAE3C22B-CBF5-4CF0-8427-F960A41E3DE9.html) (V)

#### 1.2 Tabla de componentes estructurales (procedimientos del manual)
Columnas: Nombre oficial (manual) | Cant. | Fijaciones de repuesto (cantidades) | Par / cotas citadas | GUID | Conf.
(Material: ver nota 1.1; el manual no lo da por pieza salvo indicación. "ASY" = ensamblaje en catálogo.)

**Front Inner Panels / subestructura delantera**
| Pieza | Cant. | Unión / fijaciones | Par / cotas | GUID | Conf. |
|---|---|---|---|---|---|
| Front Under Body (Complete) = fundición delantera ("FUB", ASY FRONT UNDER BODY COMPLETE) | 1 | 30 remaches estruct. HS 6,5 mm + 4 flow-form S18; 8 tornillos M12x35 (1089657-00), 2 M10x33 (1851387-00), 10 M12x43 (1882229-00); 2 tapones (1870761-00); adhesivo estructural | M12x35 y M10x33: 90 Nm; M12x43: 67 Nm; taladro de acceso Ø29 mm (1 1/8 in) en centro de pieza | B113826C-1A8D-4AA3-BE16-40B3FB83870A | V |
| Front Under Body (Small Section) = "FUB Small Section" | 1 | 7 remaches estruct. brida 6,5 mm; 2 tornillos HF M10-1.5x41 (1622577-00), 1 M8x28 (1112247-00); 4 plantillas de corte (Outboard LH 2031072-00, Inboard LH 2031073-00, Outboard RH 2031074-00, Inboard RH 2031075-00) | M10x41: 64 Nm; M8x28: 28 Nm; holgura máx. 3 mm; clips de arnés 48 mm (nueva) / 60 mm (original) | 3E9AE471-00F8-4351-99EF-455E3CC3DA0A | V |
| Dash Reinforcement Assembly + Front Body Bridge Reinforcement (se suministran con FUB Complete) | 1+1 | 61 remaches HS 6,5 mm + 4 flow-form S18; 2 tornillos M12x35, 10 M12x43 | (par no dado en esta página) | 73B5ACF2-CC64-4A29-A5C6-400913CC2986 | V |
| Front Body Bridge Reinforcement Assembly | 1 | (página no accesible, 403) | — | 28FA070F-B8F6-4625-8A6F-C7C50EBBA965 | gap |
| Front Drive Unit Mount (Left) / (Right) | 1 + 1 | 3 tornillos HHL M10x41 (1623242-00) + adhesivo | 65 Nm | 6E692237-B0BE-419E-8AE3-53847CB3A206 (LH); RH: 72BD8A48-571B-4A18-8EA9-C8CF434E29EB | V (LH); RH I |
| Fender Beam (LH y RH) | 2 (1 por lado) | 3 tornillos HF M8x28 (1112247-00) cada uno; Loctite en tornillos de ajuste | 28 Nm | 195D0181-D206-4C0E-A0AA-A6CD30208D43 | V |
| Bumper Beam Mount | 1 por lado (I) | 3 tornillos HF M8x28 (1112247-00) + adhesivo | 21 Nm | 98A44CFE-8761-45CD-AE86-EEEC49C8D17B | V |
| Dash to FUB Gutter Connector ("gutter connector, dash to casting") | 1 | 8 remaches 4,8 mm + adhesivo | — | C9399BA0-1711-4022-AB57-F0EC9D36CC6D | V |
| CFM Bracket (soporte módulo ventilador de refrigeración) | 1 | 2 remaches HS 6,5 mm + adhesivo | — | 259A7A0D-31D3-459D-930A-4EEB449BA004 | V |
| Front Energy Absorber / Front Bumper Beam Assembly (viga paragolpes "Megabeam", referida como "Front Inner Panels - Megabeam" FRT 0,48) | 1 | Se desmonta como conjunto; no hay procedimiento de reparación propio en el manual | — | (referencia en C9399BA0-1711-4022-AB57-F0EC9D36CC6D) | V (existencia); material gap |

**Body Side Panels**
| Pieza | Cant. | Unión / fijaciones | Par / cotas | GUID | Conf. |
|---|---|---|---|---|---|
| Body Side (Complete) ("ASY FRONT BODY COMPLETE") | 2 (LH/RH) | 46 remaches HS 6,5 mm; 5 avellanados 4,8 corto + 2 largos; flow-form S08x1, S18x6, S28x1, S48x1, S58x1; 4 tornillos M12x35, 4 M10x35 (1851387-00), 5 M12x43; 3 tapones; soldadura por puntos en puntos de instalación | 90/90/67 Nm; cotas rivet C=49, D=13 mm; Rear Rocker Step Reinforcement recorte 7 y 32 mm | AAE3C22B-CBF5-4CF0-8427-F960A41E3DE9 | V |
| Body Side Outer | 2 | 17 remaches HS 6,5; 1 avellanado corto + 2 largos 4,8; flow-form S08x1, S18x5, S28x1, S48x1, S58x1; 4 tornillos M12x35; soldadura por puntos | 90 Nm | F83C624F-13D4-4C3C-99A3-AD52857C3403 | V |
| C-Pillar Inner (pilar C interior) | 2 | 33 remaches HS 6,5; 2 tornillos M10x33 | 90 Nm; cotas A=49, B=19, C=64, D=12, E=6, F=8 mm | FB686750-7B16-45B2-876D-375981FBC53E | V |
| C-Pillar Lower Nut Plate | 2 | 1 avellanado 4,8 corto + adhesivo | — | D4B984A6-1365-4D57-BE72-18344C2C6938 | V |
| Cantrail Stud Plate (delantera y trasera, por lado) | 2+ | 1 remache avellanado estruct. 6,5 mm | — | EBA81A11-429A-40C9-A356-277BE584F4B8 | V |
| Cantrail Trim Bracket | 2 | soldadura por puntos + adhesivo | — | 58814D7C-1184-4609-9BEE-01051F987EBC | V |
| Front Quarter Window Assembly (Complete) | 2 | 8 remaches HS 6,5; 3 avellanados 4,8; 2 flow-form S18; 1 tornillo M12x35; soldadura por puntos | 70 Nm | 0CBA4CBC-FC0F-4163-8778-89712C248EFF | V |
| Front Quarter Window Assembly (Outer) | 2 | — (no consultada) | — | E6455D9C-A0C1-4FFE-87E6-1D8D1D68E7A1 | gap |
| HV Battery Support Bracket | 2 (LH/RH) | 22 remaches HS 6,5; soldadura por puntos; adhesivo | cotas A=24 mm (remache), B=26 mm (punto de soldadura) | B4CAB3E6-3556-40E8-8586-10744989795C | V |
| IP Beam Bracket (soporte viga transversal del salpicadero) | 2 | 6 remaches HS 6,5 o soldadura de tapón (taladro Ø10 mm); GMA permitida | Ø10 mm plug weld | 4EBD56B6-558A-41C0-8CA3-DF81B20D358B | V |
| Power Gate Strut Mount | 2 | 3 remaches brida 6,5 mm | — | 79118AE1-30C8-4666-8E63-FF4575B1300C | V |
| Rocker Support Bracket | 2 | (403, no consultada) | — | C2530069-89E2-4CBC-8F0B-FC80226516EF | gap |
| Sail Panel Bracket (Upper) | 2 | 3 remaches HS 6,5 | — | 2DB1CB43-1C29-4E03-AD36-F06D51E2D20D | V |
| Side Sill Insert ("ASY SIDE SILL EXTRUSION") = inserto extruido de umbral | 2 | 4 remaches 4,8 mm; 2 tornillos M10x33 (90 Nm); 2 tornillos HF M8-1.25x25 (1008571-00, 26 Nm); adhesivo; "XM Bash Plates" remachadas 4,8 o soldadas | 90 / 26 Nm | F7FF4CF8-DDC8-439F-B656-453CC21A05C5 | V |

**Rear Under Body / cama**
| Pieza | Cant. | Unión / fijaciones | Par / cotas | GUID | Conf. |
|---|---|---|---|---|---|
| Rear Under Body (Complete) = fundición trasera (ASY REAR UNDERBODY) | 1 | 10 remaches HS 6,5; 6 tornillos M10x33 (1851387-00); 4 tapones; adhesivo | 90 Nm; taladro Ø29 mm; punto de acceso trasero 155 mm (+5 mm si marca 150); recorte Rear Rocker Step Reinforcement 7 y 32 mm | B0B31EF5-A87A-4AAD-AC35-B4B268807556 | V |
| Rear Under Body (Section) = media sección trasera (Half Section) + Top Stamping + Bottom Stamping | 1+1+1 | 13 remaches HS 6,5; 4 remaches brida 6,5; 3 tornillos M10x33; 2 tapones | 90 Nm; holgura máx. 3 mm | 949F33FC-FA69-442B-B895-69F6ABD44792 | V |
| Rear Under Body (Frame Rail Section) = "Rear Rail Casting" + Rear Rail Section Backing Plate | 1+1 | 15 remaches brida 6,5 mm; adhesivo en huecos | 19 cotas A-S: A=23, B=40, C=129, D=27, E=73, F=31, G=20, H=62, I=22, J=18, K=29, L=72, M=46, N=70, O=160, P=17, Q=66, R=19, S=10 mm (etiquetas de figura no incluidas); holgura 3 mm | 0611074E-4F3C-417E-86AB-5BBC588393CC | V (valores) / significado de letras gap |
| Mast Assembly (Complete) ("ASY MAST CASTING") | 2? (LH/RH, I; el manual lo trata como "un componente" por lado con operaciones solo LH para busbar de carga) | 19 remaches HS 6,5; 1 tornillo T2K HHN 10x38 (1893805-00); adhesivo; SPR de fábrica | 27 Nm | 5E2DE223-5642-43AE-899E-29A771447B13 | V |
| Mast Assembly (Section) | 1 | fundición + 4 placas de refuerzo (Top, Top Middle, Bottom Middle, Bottom Backing Plate); 13 remaches HS 6,5; seccionado solo detrás de la línea de corte elevada | holgura máx. 3 mm | 48F9633A-45C7-4E76-861D-B91CF99A58C5 | V |
| Tailgate Tower | 2 (LH/RH) | 7 remaches HS 6,5; adhesivo | — | 2CEAA19D-88FC-4AB4-AD97-5CD8388E0E6B | V |
| Tailgate Tower Support Plate | 2 | 5 remaches avellanados 4,8 largos | — | 38C1CCF5-3D33-442D-A074-25130395BE97 | V |
| Rear Wheel Arch (ASY WHEELHOUSE ARCH) | 2 | 4 remaches HS 6,5; 5 remaches 4,8; 2 avellanados 4,8 largos | cotas A=90, B=185, C=11, D=246, E=62 mm | C987B794-5A9C-46BD-9C4F-69C56586E44B | V |
| Rear Wheel Arch (Rear Section) | 2 | no consultada | — | 7AEB114C-42D5-47EF-BB6D-0DA5DF876EB3 | gap |
| Rear Wheel Arch Extension (Front) | 2 | 6 remaches 4,8 + adhesivo | — | 73A9B0D4-0779-447E-A3EC-C67528B68A8D | V |
| Bed Bridge Bracket (ASY REAR BED BRIDGE BRKT) | 1-2 | 3 remaches HS 6,5 | — | DFA8DD4B-7757-4810-9901-A81CFA4CAE2A | V |
| Rear Fascia Bracket | 2 | 3 remaches HS 6,5 | — | BBE01AF0-636B-4644-9D69-EC8297FB7D0D | V |
| Sail Datum Bracket (se retira y no se repone; clips relocalizados) | — | 2 Band Edge Clip (1518812-00) + 2 bridas cable (1015391-00) | cotas A=105, B=195, C=78, D=53 mm | CE8950DB-EF5C-4874-91C1-4F5DAA65B890 | V |
| Tie-Down Nut Plate (Rear) (ASY REAR TIEDOWN NUT PLATE) | 2+ | 1 remache avellanado estruct. 6,5 | — | C4480139-50C0-4305-A017-4341ECB376F4 | V |

**Rear End Panels (pared trasera/asientos traseros)**
| Pieza | Cant. | Unión / fijaciones | Par / cotas | GUID | Conf. |
|---|---|---|---|---|---|
| Rear Wall Assembly (ASY REAR WALL COMPLETE) | 1 | 48 remaches HS 6,5; 38 flow-form S18; 2 flow-form S28; 2 tornillos T2K HHN 10x38 (1893805-00); adhesivo | 37 Nm; cotas A=49, B=13 mm | D3BE5950-43B3-4EE0-8ECF-A84C33722A1C | V |
| Rear Wall Lower Crossmember Glove | 1 | 24 remaches HS 6,5 | cotas A=13, B=6, C=50 mm | 26CC2A21-B159-46FC-801D-9A67EC476A5F | V |
| Rear Wall Upper Crossmember Glove | 1 | 11 remaches HS 6,5; 3 flow-form S18; 2 S38; 1 tornillo 10x38 | 27 Nm; A=69, B=31 mm | FE53D38B-462F-4C54-AE07-8B6E01F5F189 | V |
| Rear Seat Stanchion | 2 | 7 remaches HS 6,5 + 1 de 4,8 | — | 8AE6D991-4847-47B4-BD6B-D42A9D505B2C | V |
| Rear Seat Stanchion Brace(s) ("Crossbrace RR Seat Stanchion") | 2 | 6 remaches HS 6,5 (trasero); 2 remaches 4,8 (delantero) | — | 2E4068B7-0AD8-4026-8D7E-60E23E87B347 | V |
| Tonneau Attachment Bracket (Lower) | 2 | 1 remache HS 6,5; 1 avellanado corto + 1 largo 4,8 | A=31, B=12, C=23, D=96 mm | F268886D-FA6F-4CCD-B8E2-D591DDE288F3 | V |
| Tonneau Attachment Bracket (Upper) | 2 | 3 remaches HS 6,5; 1 de 4,8 | A=17 mm | A4FE7F64-93AB-4DF7-9D35-65545A3267D1 | V |

**Roof Panels (cabeceras de techo)**
| Pieza | Cant. | Unión / fijaciones | GUID | Conf. |
|---|---|---|---|---|
| Front Header Upper | 1 | 4 avellanados 4,8 largos + 12 flow-form S18; soldadura por puntos; adhesivo | B3CA601A-40FE-4E62-86C2-81BF946E66D3 | V |
| Front Header Lower | 1 | soldadura por puntos + adhesivo | E5612BBC-CF8B-4B6B-81D7-2D46575DE42B | V |
| Front Header Gusset | 2 | 5 avellanados 4,8 cortos + 2 flow-form S18; soldadura por puntos; cotas A=17, B=14 mm | AA25756A-C263-457B-BBAE-85C174F454F2 | V |
| Rear Header Lower ("REAR WALL HEADER INNER") | 1 | 6 remaches HS 6,5 o 20 flow-form S18 (ambas opciones listadas) | 35720B29-7A65-44CB-A14C-12F9123F2434 | V |
| Rear Header Upper | 1 | 32 flow-form S18 | AB678C76-3D94-4D47-BC0B-C1217F79C104 | V |

#### 1.3 Fijaciones (números de pieza Tesla) — [Approved Fasteners](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-02989E68-695F-4E9B-8C94-BBD580C5E4D0.html) (V)
- Remache 4,8 mm: 1028719-00-A. Remaches estructurales 6,5 mm: corto 1028408-00-A, medio 1062559-00-A, largo 1028409-00-A, alta resistencia 1454538-00-A. Pop 5/32 in aluminio: 1003668-00-C.
- Avellanados: 4,8 corto 1069308-00-A o 2046255-00-A; 4,8 largo estruct. 1069326-00-A; 6,5 estruct. 1069327-00-A. Bulb 6,5 mm (paneles finos <= 4,5 mm): 1063943-00-A. Brida 6,5 mm: 1062558-00-A; brida alta resistencia 1116094-00-A. Remache estructural 8 mm (5/16): 1058710-00-A.
- SPR (remaches autoperforantes) Ø5: 5x4 1026936-00-A, 5x4,5 1026938-00-A, 5x5 1026939-00-A, 5x6 H4 1026940-00-A, 5x6 H2 1026941-00-A, 5x6,5 1026942-00-A, 5x7 1026943-00-A, 5x8 SKR 1026944-00-A, 5x8 SK 1026945-00-A, 5x9 1028629-00-A.
- Flow-form (cuerpo Ø8 mm, taladro Ø8 mm): S08 1,3-2,5 mm (1069328-00-A); S18 2,3-3,5 (1069329); S28 3,35-4,10 (1069330); S38 4,0-5,15 (1069331); S48 5,0-6,1 (1069332); S58 6,0-7,2 (1069333); S68 7,1-8,3 (1069334) — [Using Flow Form Rivets](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-251653EC-9283-4E1C-B1BB-7C2E60A02EA5.html). Remachadoras: XPress 800 y TKR PNP 90 a 60 kN; ProSpot PR-5 y Böllhoff HTF 50 a 50 kN. (V)
- BOM 5/16 in (grip 7,95-11,1 mm): 1062555-00-A. NeoBolt 3/4 in corto 1599680-00-A / largo 1599681-00-A (collar 1599682-00-A); NeoBolt 5/8 in 1599677-00-A (collar 1599679-00-A); AV Bolt 5/8 in 1600794-00. Pin y collar 1/4 in 1062557-00-A, 5/16 in 1062556-00-A. (V)
- Tornillos estructurales recurrentes: HF M12x35 1089657-00; HHL M10x33/M10x35 1851387-00; HHL M12x43 1882229-00; HF M8x28 1112247-00; HHL M10x41 1623242-00; HF M10-1.5x41 1622577-00; T2K HHN 10x38 1893805-00; HF M8-1.25x25 1008571-00. Tapón de acceso 1870761-00. (V, las páginas de procedimiento arriba)
- Estructuras de refuerzo de fundición: placa de refuerzo 1076938-E0-B (adhesivo, sin soldar); espárrago doble extremo autorroscante 1463292-00-C (par 5 Nm). — [Cast Rear Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-A839FDF1-F60E-44E5-ADFB-5B7A220C945C.html), [Cast Front Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C1914222-086E-4604-809F-1ECB9A0F6F53.html) (V)

#### 1.4 Adhesivos, sellantes y espumas — [Approved Chemicals](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-EF1DD38B-6C21-4850-BF26-1B09ECB62454.html) (V)
- Adhesivo estructural: DuPont BETAMATE 2098 (Crash Durable), Parker LORD Fusor 2098 (lento, Norteamérica), 3M 07333.
- Sellantes de juntas: 3M 08308 (insonorizante), uretanos 3M 08360/08361/08362/08364/08365/08367/08368, epoxi OEM 3M 08528/08522, Henkel MS 9120/9320 SF, LORD Fusor 122 EZ / 123 SL / 123 Medium / 123 Fast; material insonorizante LORD Fusor 231.
- Espumas: LORD Fusor 121/124 (flexible), Fusor 130 (acústica rígida), 3M 08463, SEM 39357, Wurth 089391070 (anti-vibración).
- Cera de cavidades 3M 08852 / 38854; recubrimientos anti-gravilla (3M 08889 rocker, Henkel WT R2000/S3000, SEM 52000); imprimación de soldadura 3M 05917.
- Adhesivos de luna: DuPont Betaseal Express+ (Norteamérica), Betaprime 5504G.

#### 1.5 Límites de reparación de fundiciones (útiles para saber qué zonas son críticas)
- Front Under Body fundido: zonas azul/verde/amarillo/naranja/rojo; soldadura permitida hasta 50 mm (verde), 30 mm sin placa (amarillo), 30-50 mm con placa, naranja hasta 30 mm con placa; rojo = sin reparación; alma doblada se restaura en frío dentro de 1,5 mm; arañazos < 5 mm de profundidad se pueden lijar; taladro de espárrago Ø5,5 mm x 22 mm. — [Cast Front Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C1914222-086E-4604-809F-1ECB9A0F6F53.html) (V)
- Rear Under Body fundido: igual lógica más zonas rosa/cian, "spring pocket" (arañazos < 1 mm lijables), espárrago Ø5,5 x 12 mm. El texto del resumen indica "steel component" pero esto es casi seguro un error de la herramienta de resumen (las fundiciones se reportan como aluminio; ver 2). — [Cast Rear Under Body](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-A839FDF1-F60E-44E5-ADFB-5B7A220C945C.html) (V para límites; material = conflicto)
- Mast Assembly: zonas azul/verde/amarillo con los mismos límites 30/50 mm; placa 1076938-E0-B. — [Mast Assembly Repair Guidelines](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-112E876E-DB80-4614-8B4E-F6F54AA9C4F8.html) (V)
- Tailgate Tower: zonas verde/amarillo/naranja; soldadura hasta 50/30 mm; naranja crack <= 30 mm con placa. — [Tailgate Tower Repair Guidelines](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-9CD66714-3A98-49BC-B31C-06938B4D6DA6.html) (V). Esto implica que la torre del portón también es una fundición.

#### 1.6 Dimensional Specifications
- Unidades mm, medidas centro a centro, simétricas salvo indicación. Cinco figuras: Side Body, A-Pillar a A-Pillar / B-Pillar a B-Pillar, Under Hood, Rear Body, Top. Los valores numéricos están en imágenes, no en texto. — [Dimensional Specifications](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C5797770-FD0F-4A21-90C1-FC4E47976C95.html) (V)

### Inferences
- Los "Under Body" delantero y trasero son las dos grandes fundiciones de aluminio; Mast y Tailgate Tower son fundiciones adicionales (zonas por color, soldables, placas de refuerzo con adhesivo). (I)
- Las cantidades de remaches por procedimiento son para la pieza de repuesto completa y por lado; para modelar, duplicar LH/RH las piezas "LH only/RH" y no contar dos veces la pieza central (Rear Wall, headers). (I)
- La mezcla remaches 6,5 mm HS + flow-form S18 + adhesivo en techo/pared trasera sugiere paneles de acero/aluminio finos unidos en frío; la soldadura por puntos aparece solo en Body Side, cabeceras delanteras, soportes de cantrail y batería (piezas de acero). (I)
- Los 2 tapones (1870761-00) por taladro de acceso Ø29 mm aparecen en los taladros de corte de las fundiciones y del Body Side: son tapones visibles en un modelo detallado. (I)

### Gaps
- Material/grado por pieza (mapa de materiales Figuras 1-4 son imágenes): no extraíble en texto. Hay que verlo en el sitio original.
- Valores de las cinco figuras de Dimensional Specifications (cotas de control): solo en imágenes.
- Páginas no consultadas por error 403: Front Body Bridge Reinforcement Assembly, Rocker Support Bracket; no consultadas por límite de llamadas: Front Quarter Window (Outer), Rear Wheel Arch (Rear Section), Front Drive Unit Mount (Right), Approved Wheel Repairs, Front Bumper Fascia Repair, Windshield/Roof Glass.
- Cantidad exacta de piezas por vehículo (el manual da procedimientos, no BOM).
- El manual describe que el texto de Dash/Front Body Bridge se "separa" del FUB Complete, lo que sugiere que están integrados como parte del conjunto; el número de pieza real no está en texto.

---

## 2. ¿Qué revelan desguaces (Munro), entrevistas y prensa sobre dimensiones de fundiciones, nº de piezas, pesos y rasgos estructurales inusuales?

### Takeaway
Fuentes públicas accesibles dan pocos números duros: Munro describe un "inner body-in-white" convencional bajo la piel inoxidable (pilares A/B de acero boro), una fundición grande delantera y dos traseras, y paneles de inoxidable pegados; no encontré masas ni dimensiones de las fundiciones. La Giga Press de 9.000 t existe pero no hay confirmación independiente de qué pieza fabrica.

### Cited Findings
- Munro: bajo la piel de acero inoxidable hay un body-in-white interno con pilares A y B de acero al boro, similar al Model Y; el inoxidable aporta rigidez pero no es el "exoesqueleto puro". — [LeanDesign/Munro](https://leandesign.com/cybertruck-structural-design-analysis/) (R; la URL redirige al sitio de Munro y el resumen es de segunda mano)
- Munro reporta una fundición delantera única que integra pasos de rueda y zonas de deformación, y dos fundiciones traseras laterales formando una estructura transversal; reducen piezas, soldaduras y peso. — misma fuente (R)
- Paneles inoxidables pegados con adhesivo (no remachados ni soldados) sobre estructura interna de acero estampado de alta resistencia. — misma fuente (R)
- Prensa de 9.000 t IDRA para el Cybertruck; Musk: para la carrocería trasera (cama larga); el director general de IDRA dijo que la de 8.000 t era para fundiciones de subestructura grandes; fuentes discrepan sobre si es delantera o trasera. — [autoevolution](https://www.autoevolution.com/news/idra-s-9000-ton-giga-press-is-ready-to-cast-tesla-cybertruck-s-underbody-190206.html), [Tesla Oracle](https://www.teslaoracle.com/2022/06/03/idra-groups-9000-ton-giga-casting-machine-is-for-the-cybertruck-unibody-confirms-elon-musk/); en contradicción parcial con [Tesmanian](https://www.tesmanian.com/blogs/tesmanian-blog/sla-cybertruck-to-be-manufactured-by-idras-9-000-ton-giga-press) (R)
- Pre-lanzamiento: la parte trasera se compone de ~5 grandes piezas (una fundición inferior de cama y cuatro laterales) según piezas vistas y foto filtrada. — [InsideEVs](https://insideevs.com/news/670702/tesla-cybertruck-rear-castings-spotted/) (R, baja confianza)
- Foro/extricación: cabina, pilares, umbrales y largueros de acero; fundiciones de aluminio; no hay bastidor de acero bajo la carrocería. — [Boron Extrication](https://boronextrication.com/2024/04/23/tesla-cybertruck-body-structure/) vía búsqueda (R; página no accesible por 403)
- Subbastidor trasero (cradle) Cyberbeast tri-motor: aloja módulo de accionamiento eléctrico con dos motores, inversores y cremallera de dirección trasera; se puede bajar sin los brazos superiores traseros; los brazos de control superiores traseros se montan a la gran fundición trasera (no al cradle); peso en vacío medido 6.843 lb (~3.104 kg). — [The Autopian](https://theautopian.com/latest-cybertruck-teardown-reveals-teslas-odd-sway-bar-decisions-clever-packaging) (R)
- Batería estructural: pack integrado en la rigidez del chasis con puntos de fijación desde paneles de cabina hasta cama y umbrales (opinión de artículo). — [LeanDesign/Munro](https://leandesign.com/?p=2995) (R, baja)
- Pre-lanzamiento: Munro estimó ~6.800 lb (3,4 t); no medida. — [InsideEVs](https://insideevs.com/news/679572/tesla-cybtertruck-weight-predictions-munro/) (R)
- Nota del manual: el pack HV está soportado por los HV Battery Support Brackets y se retira para cambiar Front/Rear Under Body, y el "Subframe, Rear (Dual Motor)" existe como pieza separada. — [Rear Under Body (Complete)](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B0B31EF5-A87A-4AAD-AC35-B4B268807556.html) (V)
- "Megabeam": el manual lo menciona como "Front Inner Panels - Megabeam" (FRT 0,48), en el procedimiento del Dash to FUB Gutter Connector. — [Dash to FUB Gutter Connector](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-C9399BA0-1711-4022-AB57-F0EC9D36CC6D.html) (V)
- Otros procedimientos citan "Rear Energy Absorber, Cast Bumper Assembly" (parachoques trasero fundido con absorbedor de energía). — [Tailgate Tower](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-2CEAA19D-88FC-4AB4-AD97-5CD8388E0E6B.html) (V)

### Inferences
- "Cast Bumper Assembly" trasero = otra fundición (nombre manual), probablemente alojamiento del enganche/tow hitch. (I)
- Las fundiciones traseras vistas pre-lanzamiento (cuatro laterales) probablemente corresponden a Mast (x2) y Tailgate Tower (x2) del manual actual, más la gran Rear Under Body. (I, baja-media)
- El eje del conflicto "steel vs aluminum" para el Rear Under Body es probable error del resumen de herramienta; tratar como aluminio fundido salvo comprobación. (I)

### Gaps
- No encontré: dimensiones (L x A x H) de fundiciones, masas de fundiciones, material exacto (aleación) de fundiciones, grado de UHSS en pilares/umbrales, material del Megabeam, grado del acero inoxidable (reportado como 30X en prensa general pero no verificado en esta búsqueda), peso del body-in-white.
- No encontré fuente específica (Lars Moravy, Franz, Q&A Tesla, Autopian, Electrek) con numérica de estructura más allá de lo anterior; el sitio de Munro redirige y gran parte está tras vídeo/suscripción.
- Estructura de la cama: no hay descripción de teardown más allá de nombres del manual (Bed Bridge Bracket, Tie-Down Nut Plate, Tonneau brackets, Body Side Outer = panel exterior de cama "Bed Side Outer Assembly").

---

## 3. ¿Cuántas piezas de carrocería en total? ¿Pesos de fundiciones y estructuras clave?

### Takeaway
No hay recuento total ni pesos de estructura en fuentes que pude verificar. El único dato de masa fiable es el peso en vacío del Cyberbeast desmontado (6.843 lb).

### Cited Findings
- Curb weight del Cyberbeast medido por Munro: 6.843 lb. — [The Autopian](https://theautopian.com/latest-cybertruck-teardown-reveals-teslas-odd-sway-bar-decisions-clever-packaging) (R)
- Procedimientos de piezas estructurales publicados en el manual: ~55 entradas (7 categorías de Front Inner Panels..., 14 Body Side, 14 Rear Under Body, 7 Rear End, 5 Roof, más 8 guías de reparabilidad). — [Índice del manual](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/index.html) (V)
- Fijaciones sumadas en los procedimientos "Complete" principales (solo las que el manual dicta como repuesto): Front Under Body: 34 remaches + 20 tornillos; Body Side Complete: 46 HS + 7 avellanados + 10 flow-form + 13 tornillos; Rear Wall: 48 HS + 40 flow-form + 2 tornillos; Rear Header Upper: 32 flow-form. (V; ver tablas 1.2)

### Inferences
- Una estimación total de piezas de carrocería sería > 100 componentes estructurales con las entradas LH/RH, pero no hay BOM publicado: no usar como dato duro. (I)

### Gaps
- Masa de Front Under Body, Rear Under Body, Mast, Tailgate Tower, BIW completo, batería (excepto especificación de capacidad). No publicados en fuentes accesibles.

---

## 4. ¿Qué soportes, clips y tapones pequeños necesita un modelo completo?

### Takeaway
El manual permite identificar con nombre y cantidad la mayoría de los pequeños soportes estructurales y la tornillería; faltan elementos de aislamiento NVH y paneles inferiores (aerodinámicos) que el manual de carrocería solo cita por referencia.

### Cited Findings
- Soportes/placas nombradas: CFM Bracket; Bumper Beam Mount; Dash-to-FUB Gutter Connector; IP Beam Bracket; Cantrail Stud Plate; Cantrail Trim Bracket; C-Pillar Lower Nut Plate; Sail Panel Bracket (Upper); Power Gate Strut Mount; Rocker Support Bracket; HV Battery Support Bracket; Rear Fascia Bracket; Bed Bridge Bracket; Tie-Down Nut Plate (Rear); Tonneau Attachment Brackets (Upper/Lower); Rear Seat Stanchion Brace; Rear Wall Upper/Lower Crossmember Glove; Tailgate Tower Support Plate; Sail Datum Bracket; "XM Bash Plates" (placas de protección ligadas al inserto de umbral); Ramp Bracket - C-Pillar (rampa de cama). — páginas del manual indicadas en 1.2; XM Bash Plates en [Side Sill Insert](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-F7FF4CF8-DDC8-439F-B656-453CC21A05C5.html); Ramp Bracket en [Rear Wall Assembly](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-D3BE5950-43B3-4EE0-8ECF-A84C33722A1C.html) (V)
- Elementos adyacentes citados (componentes funcionales ligados): Supercarrier Assembly, Super Cowl, "NVH Pad" (general) y "NVH Pad - Rear Wall", Rear Energy Absorber/Cast Bumper, Under Bed Storage Assembly, Tonneau Lower Assembly, Tow Hitch, Subframe Rear (Dual Motor), Air Suspension Compressor y Reservoir, Wheel Liner delantero/trasero, Front End Carrier Plastic Assembly, cuna de motor delantero ("front drive unit"). — [Front Under Body (Complete)](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B113826C-1A8D-4AA3-BE16-40B3FB83870A.html), [Rear Under Body (Complete)](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-B0B31EF5-A87A-4AAD-AC35-B4B268807556.html), [Tailgate Tower](https://service.tesla.com/docs/Cybertruck/BodyRepair/BodyRepairProcedures/en-us/GUID-2CEAA19D-88FC-4AB4-AD97-5CD8388E0E6B.html) (V)
- Tapones de taladro de acceso (1870761-00) con sellante en la cara inferior; arnés: Band Edge Clip 1518812-00, bridas 1015391-00. (V, tablas 1.2)

### Inferences
- Para un modelo completo hay que añadir (no verificados individualmente): amortiguador/refuerzos de torre de suspensión, protectores inferiores (underbody shields/aero panels), absorbedores de impacto delanteros (crush cans), ganchos de remolque, enganche, almohadillas NVH. (I; solo existe cita por nombre en procedimientos, no dimensiones)

### Gaps
- Dimensiones y geometría de todas las piezas pequeñas, protectores inferiores/aero, crush cans, ganchos de remolque y enganche, aislamiento NVH (espesor/ubicación), barras antivuelco, puntos de anclaje de asientos delanteros: no encontrados en fuentes accesibles.
- Subbastidor delantero y "tri-motor cradle": el manual solo cita "Subframe, Rear (Dual Motor)" y "front drive unit"; no hay descripción estructural de masa/material para el Cyberbeast.
- Cybertruck-specific: ausencia de umbral de acero UHSS + extrusión de aluminio verificada; el manual confirma un inserto de umbral descrito como extrusión ("SIDE SILL EXTRUSION") pero no el grado.
