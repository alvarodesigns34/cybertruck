# Inventario de componentes

> Generado automáticamente con `node tools/gen_inventory.mjs` a partir de `web/models/cybertruck-manifest.json`, que se exporta desde la escena real de Blender. Solo enumera objetos que existen en el modelo.

- Vehículo: Tesla Cybertruck Cyberbeast (EE. UU., gama 2026)
- Componentes (nodos con metadatos): **560**
- Mallas: **522** · Conjuntos (vacíos con pivote): **38**
- Caras de malla base (antes de modificadores): 235.992
- Fidelidad: Verificado 23 · Reconstruido 497 · Aproximado 40

Etapas de explosión: 1. Paneles exteriores y elementos de apertura · 2. Conjuntos interiores · 3. Estructura de carrocería y bajos · 4. Suspensión, ruedas y frenos · 5. Batería y tren motriz · 6. Componentes pequeños y herrajes

## Paneles exteriores (`EXTERIOR_PANELS`) — 23

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `EXT_BedSide_L` | Lateral de la caja con vela (izquierda) | Malla | 1 | Reconstruido |
| `EXT_BedSide_R` | Lateral de la caja con vela (derecha) | Malla | 1 | Reconstruido |
| `EXT_Cowl_Wiper_Applique` | Aplique del limpiaparabrisas | Malla | 6 | Reconstruido |
| `EXT_Fender_FL` | Aleta delantera izquierda | Malla | 1 | Reconstruido |
| `EXT_Fender_FR` | Aleta delantera derecha | Malla | 1 | Reconstruido |
| `EXT_Flare_FL` | Aleta del paso de rueda delantero (izquierda) | Malla | 1 | Reconstruido |
| `EXT_Flare_FR` | Aleta del paso de rueda delantero (derecha) | Malla | 1 | Reconstruido |
| `EXT_Flare_RL` | Aleta del paso de rueda trasero (izquierda) | Malla | 1 | Reconstruido |
| `EXT_Flare_RR` | Aleta del paso de rueda trasero (derecha) | Malla | 1 | Reconstruido |
| `EXT_Front_Bumper` | Fascia inferior delantera (paragolpes) | Malla | 1 | Reconstruido |
| `EXT_Front_End_Carrier` | Soporte frontal de plástico (6 tornillos de 10 mm a 5 N·m y 2 de 13 mm) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 1 | Reconstruido |
| `EXT_Front_Fascia_Upper` | Frontal superior de acero inoxidable | Malla | 1 | Reconstruido |
| `EXT_Front_Lower_Grille` | Rejilla inferior con persianas activas | Malla | 6 | Reconstruido |
| `EXT_License_Plate_Rear` | Placa de matrícula trasera (genérica, sin texto) | Malla | 6 | Aproximado |
| `EXT_MudFlap_FL` | Faldilla delantera (2 tornillos y 2 grapas) | Malla | 6 | Reconstruido |
| `EXT_MudFlap_FR` | Faldilla delantera (2 tornillos y 2 grapas) | Malla | 6 | Reconstruido |
| `EXT_MudFlap_RL` | Faldilla trasera (2 tornillos y 2 grapas) | Malla | 6 | Reconstruido |
| `EXT_MudFlap_RR` | Faldilla trasera (2 tornillos y 2 grapas) | Malla | 6 | Reconstruido |
| `EXT_Pedestrian_Speaker_Horn` | Altavoz de aviso a peatones (3 tornillos T25) y bocina de tono grave — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Rear_Bumper` | Fascia trasera con escalón integrado | Malla | 1 | Reconstruido |
| `EXT_Rear_Diffuser` | Difusor trasero con aletas (14 tornillos, 12 grapas) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 1 | Reconstruido |
| `EXT_Rocker_L` | Faldón lateral (izquierda) | Malla | 1 | Reconstruido |
| `EXT_Rocker_R` | Faldón lateral (derecha) | Malla | 1 | Reconstruido |

## Puertas y portones (`DOORS_AND_HATCHES`) — 60

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `DOOR_FL` | Puerta delantera izquierda | Conjunto | 1 | Reconstruido |
| `DOOR_FL_InnerStructure` | Estructura interior de la puerta (chapa interior y refuerzos) | Malla | 6 | Aproximado |
| `DOOR_FR` | Puerta delantera derecha | Conjunto | 1 | Reconstruido |
| `DOOR_FR_InnerStructure` | Estructura interior de la puerta (chapa interior y refuerzos) | Malla | 6 | Aproximado |
| `DOOR_RL` | Puerta trasera izquierda | Conjunto | 1 | Reconstruido |
| `DOOR_RL_InnerStructure` | Estructura interior de la puerta (chapa interior y refuerzos) | Malla | 6 | Aproximado |
| `DOOR_RR` | Puerta trasera derecha | Conjunto | 1 | Reconstruido |
| `DOOR_RR_InnerStructure` | Estructura interior de la puerta (chapa interior y refuerzos) | Malla | 6 | Aproximado |
| `EXT_ChargePort_Door` | Puerta de la toma de carga (NACS) | Malla | 6 | Reconstruido |
| `EXT_ChargePort_ECU` | Controlador de la toma de carga (Gen 4, 1 tornillo y 3 conectores) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_ChargePort_Inlet` | Receptáculo NACS con 5 contactos y anillo de luz | Malla | 6 | Reconstruido |
| `EXT_Door_FL_CheckStrap` | Tirante de retención de la puerta (3 fijaciones; 35 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Controller` | Controlador electrónico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_GlassFrame` | Marco y aplique negro del cristal | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Hinges` | Bisagras superior e inferior con placas de espárragos (25/38 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Latch` | Cierre eléctrico de la puerta (13 N·m) y presentador de apertura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Regulator` | Elevalunas con motor Q de 48 V — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Seals` | Burlete secundario (26 grapas) y juntas de cintura interior y exterior — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Skin` | Piel exterior de acero de la puerta | Malla | 6 | Reconstruido |
| `EXT_Door_FL_Striker` | Percutor del cierre en el pilar — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_CheckStrap` | Tirante de retención de la puerta (3 fijaciones; 35 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Controller` | Controlador electrónico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_GlassFrame` | Marco y aplique negro del cristal | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Hinges` | Bisagras superior e inferior con placas de espárragos (25/38 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Latch` | Cierre eléctrico de la puerta (13 N·m) y presentador de apertura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Regulator` | Elevalunas con motor Q de 48 V — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Seals` | Burlete secundario (26 grapas) y juntas de cintura interior y exterior — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Skin` | Piel exterior de acero de la puerta | Malla | 6 | Reconstruido |
| `EXT_Door_FR_Striker` | Percutor del cierre en el pilar — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_Primary_Seals_L` | Burletes primarios de la carrocería (huecos de puertas delantera y trasera) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_Primary_Seals_R` | Burletes primarios de la carrocería (huecos de puertas delantera y trasera) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_CheckStrap` | Tirante de retención de la puerta (3 fijaciones; 35 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Controller` | Controlador electrónico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_GlassFrame` | Marco y aplique negro del cristal | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Hinges` | Bisagras superior e inferior con placas de espárragos (25/38 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Latch` | Cierre eléctrico de la puerta (13 N·m) y presentador de apertura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Regulator` | Elevalunas con motor Q de 48 V — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Seals` | Burlete secundario (26 grapas) y juntas de cintura interior y exterior — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Skin` | Piel exterior de acero de la puerta | Malla | 6 | Reconstruido |
| `EXT_Door_RL_Striker` | Percutor del cierre en el pilar — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_CheckStrap` | Tirante de retención de la puerta (3 fijaciones; 35 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Controller` | Controlador electrónico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_GlassFrame` | Marco y aplique negro del cristal | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Hinges` | Bisagras superior e inferior con placas de espárragos (25/38 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Latch` | Cierre eléctrico de la puerta (13 N·m) y presentador de apertura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Regulator` | Elevalunas con motor Q de 48 V — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Seals` | Burlete secundario (26 grapas) y juntas de cintura interior y exterior — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Skin` | Piel exterior de acero de la puerta | Malla | 6 | Reconstruido |
| `EXT_Door_RR_Striker` | Percutor del cierre en el pilar — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Frunk_Hinges` | Bisagras del frunk (Powergate Hinge, 2 tornillos a 58 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Frunk_Latch` | Cierre del frunk con actuador y 2 cables de apertura (2 tornillos a 9 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Frunk_Lid` | Tapa del maletero delantero (frunk) | Malla | 1 | Reconstruido |
| `EXT_Frunk_Seal` | Junta perimetral del frunk — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Frunk_Struts` | Amortiguadores del frunk (Hood Strut LH/RH) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Tailgate` | Portón trasero con bisagras laterales y luz superior | Malla | 1 | Reconstruido |
| `EXT_Tailgate_Cinch_Latches` | Cierres del portón con acercamiento eléctrico (2 tornillos T40 a 25 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Tailgate_Damper_Straps` | Amortiguador del portón, correas de cable y topes — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Tailgate_Hinges` | Bisagras laterales del portón (Body Side Hinge) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Tailgate_Seal` | Junta aerodinámica inferior del portón — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Tailgate_Torsion_Rod` | Barra de torsión de asistencia del portón (55/80 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |

## Cristales y retrovisores (`GLASS_AND_MIRRORS`) — 25

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `EXT_Mirror_L_Actuator` | Motor de ajuste y plegado eléctrico | Malla | 6 | Aproximado |
| `EXT_Mirror_L_Arm` | Base y pie del retrovisor con 3 tornillos T40 | Malla | 6 | Reconstruido |
| `EXT_Mirror_L_Housing` | Carcasa facetada del retrovisor («skull cap») | Malla | 6 | Reconstruido |
| `EXT_Mirror_R_Actuator` | Motor de ajuste y plegado eléctrico | Malla | 6 | Aproximado |
| `EXT_Mirror_R_Arm` | Base y pie del retrovisor con 3 tornillos T40 | Malla | 6 | Reconstruido |
| `EXT_Mirror_R_Housing` | Carcasa facetada del retrovisor («skull cap») | Malla | 6 | Reconstruido |
| `EXT_Washer_Hose` | Tubo del lavaparabrisas hasta los surtidores del brazo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Washer_Tank` | Depósito del lavaparabrisas con bomba, sensor de nivel y boca (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `EXT_Wiper_Arm` | Brazo, eje y surtidores del limpiaparabrisas (45 N·m) | Malla | 6 | Reconstruido |
| `EXT_Wiper_Blade` | Escobilla de ~1,26 m con deflector y goma | Malla | 6 | Reconstruido |
| `EXT_Wiper_Motor` | Motor del limpiaparabrisas (3 tornillos a 24 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `GLS_Door_FL` | Cristal móvil de la puerta | Malla | 6 | Reconstruido |
| `GLS_Door_FR` | Cristal móvil de la puerta | Malla | 6 | Reconstruido |
| `GLS_Door_RL` | Cristal móvil de la puerta | Malla | 6 | Reconstruido |
| `GLS_Door_RR` | Cristal móvil de la puerta | Malla | 6 | Reconstruido |
| `GLS_Mirror_L` | Espejo plano electrocrómico — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `GLS_Mirror_R` | Espejo plano electrocrómico — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `GLS_Rear_Window` | Ventana trasera eléctrica de la cabina | Malla | 1 | Reconstruido |
| `GLS_Roof` | Techo de cristal fijo | Malla | 1 | Reconstruido |
| `GLS_Seals_Roof_Backlite` | Junta trasera del techo de cristal y marco de la luneta trasera — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `GLS_Windshield` | Parabrisas laminado | Malla | 1 | Reconstruido |
| `GLS_Windshield_Edge_Seal` | Junta del borde delantero del parabrisas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `MIRROR_L` | Retrovisor exterior electromecánico (izquierdo; 3 tornillos T40 a 18 N·m) | Conjunto | 6 | Verificado |
| `MIRROR_R` | Retrovisor exterior electromecánico (derecho; 3 tornillos T40 a 18 N·m) | Conjunto | 6 | Verificado |
| `WIPER_ASSEMBLY` | Limpiaparabrisas único (brazo y escobilla) | Conjunto | 6 | Reconstruido |

## Iluminación (`LIGHTING`) — 24

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `LGT_Bed_Strip_L` | Luz lateral de la caja a lo largo | Malla | 6 | Reconstruido |
| `LGT_Bed_Strip_R` | Luz lateral de la caja a lo largo | Malla | 6 | Reconstruido |
| `LGT_Front_Lightbar_Housing` | Embellecedor y soporte de la barra de luz | Malla | 6 | Reconstruido |
| `LGT_Front_Lightbar_LED` | Barra de luz delantera (DRL LED) | Malla | 6 | Reconstruido |
| `LGT_Front_Lightbar_Lens` | Lente de la barra de luz delantera | Malla | 6 | Reconstruido |
| `LGT_Front_Lightbar_Mounts` | Grapas, centradores y tuercas de la barra de luz (fijada al frunk) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `LGT_Front_Lightbar_Optics` | Fila de 64 LED de la barra de luz delantera | Malla | 6 | Aproximado |
| `LGT_Headlamp_L` | Carcasa del faro izquierdo (2 tornillos; desmontaje desde el frunk) — _Ubicación verificada en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `LGT_Headlamp_L_DRL` | Guía de luz de posición/diurna del faro | Malla | 6 | Aproximado |
| `LGT_Headlamp_L_Projectors` | Proyectores LED de cruce y carretera con disipadores | Malla | 6 | Aproximado |
| `LGT_Headlamp_R` | Carcasa del faro derecho (2 tornillos; desmontaje desde el frunk) — _Ubicación verificada en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `LGT_Headlamp_R_DRL` | Guía de luz de posición/diurna del faro | Malla | 6 | Aproximado |
| `LGT_Headlamp_R_Projectors` | Proyectores LED de cruce y carretera con disipadores | Malla | 6 | Aproximado |
| `LGT_License_Plate_Lamp` | Luz de matrícula | Malla | 6 | Aproximado |
| `LGT_Rear_Lightbar_Housing` | Carcasa de la luz del portón (8 tornillos a 5 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `LGT_Rear_Lightbar_LED` | Barra de luz trasera (LED rojo) | Malla | 6 | Reconstruido |
| `LGT_Rear_Lightbar_Lens` | Lente de la barra de luz trasera | Malla | 6 | Reconstruido |
| `LGT_Rear_Lightbar_Optics` | Segmentos LED de la barra de luz trasera | Malla | 6 | Aproximado |
| `LGT_RearMarker_L` | Catadióptrico / luz de posición lateral trasera | Malla | 6 | Aproximado |
| `LGT_RearMarker_R` | Catadióptrico / luz de posición lateral trasera | Malla | 6 | Aproximado |
| `LGT_Reverse_L` | Luz de marcha atrás | Malla | 6 | Aproximado |
| `LGT_Reverse_R` | Luz de marcha atrás | Malla | 6 | Aproximado |
| `LGT_TailLamp_BodySide_L` | Piloto lateral de la carrocería (izquierdo) | Malla | 6 | Aproximado |
| `LGT_TailLamp_BodySide_R` | Piloto lateral de la carrocería (derecho) | Malla | 6 | Aproximado |

## Estructura de carrocería (`BODY_STRUCTURE`) — 33

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `BODY_Cabin_Floor` | Suelo de la cabina | Malla | 3 | Aproximado |
| `BODY_Cabin_RearWall` | Pared trasera de la cabina | Malla | 3 | Aproximado |
| `BODY_Casting_Front_UnderBody` | Pieza fundida delantera (largueros, torretas, travesaño del salpicadero) — _Cotas de control del manual de reparación (1.025 / 1.577 mm); forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_Casting_Rear_UnderBody_L` | Pieza fundida trasera, mitad izquierda (torreta, larguero y brazo al umbral) — _La pieza fundida trasera se repara por mitades (manual de reparación); forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_Casting_Rear_UnderBody_R` | Pieza fundida trasera, mitad derecha (torreta, larguero y brazo al umbral) — _La pieza fundida trasera se repara por mitades (manual de reparación); forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_DoorRing_L` | Anillo de puertas izquierdo de acero de ultra alta resistencia (pilares A, B y C) | Malla | 3 | Reconstruido |
| `BODY_DoorRing_R` | Anillo de puertas derecho de acero de ultra alta resistencia (pilares A, B y C) | Malla | 3 | Reconstruido |
| `BODY_Firewall` | Mamparo delantero (salpicadero) | Malla | 3 | Aproximado |
| `BODY_Floor_X_Brace` | Refuerzos del suelo en X (acero estampado) | Malla | 3 | Reconstruido |
| `BODY_Front_Bumper_Beam` | Viga de impacto delantera con absorbedores (4 tuercas a 30 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_Frunk_Tub` | Cubeta del maletero delantero (200 l) | Malla | 3 | Reconstruido |
| `BODY_IP_CrossCar_Beam` | Viga transversal del salpicadero (Supercarrier) con soporte de la columna | Malla | 3 | Reconstruido |
| `BODY_Mast_L` | «Mast» fundido izquierdo: larguero superior de la caja | Malla | 3 | Reconstruido |
| `BODY_Mast_R` | «Mast» fundido derecho: larguero superior de la caja | Malla | 3 | Reconstruido |
| `BODY_Megabeam` | Megabeam: travesaño delantero de equipos térmicos — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_Rear_Energy_Absorbers` | Absorbedores de impacto traseros fundidos (izquierdo y derecho) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `BODY_RearWall_Crossmember` | Travesaño inferior de la pared trasera de la cabina | Malla | 3 | Reconstruido |
| `BODY_Rivets_FlowForm` | Remaches flow-form y autoperforantes (72 uds.) en las uniones de umbrales y piezas fundidas | Malla | 6 | Reconstruido |
| `BODY_Seat_Crossmember_Front` | Travesaño de los asientos delanteros | Malla | 3 | Reconstruido |
| `BODY_Sill_Insert_L` | Inserto de aluminio extruido del umbral izquierdo | Malla | 3 | Reconstruido |
| `BODY_Sill_Insert_R` | Inserto de aluminio extruido del umbral derecho | Malla | 3 | Reconstruido |
| `BODY_Sill_L` | Umbral izquierdo de acero de ultra alta resistencia | Malla | 3 | Reconstruido |
| `BODY_Sill_R` | Umbral derecho de acero de ultra alta resistencia | Malla | 3 | Reconstruido |
| `BODY_Tailgate_Tower_L` | Torre fundida del portón izquierdo (bisagra y cierre) | Malla | 3 | Reconstruido |
| `BODY_Tailgate_Tower_R` | Torre fundida del portón derecho (bisagra y cierre) | Malla | 3 | Reconstruido |
| `BODY_WheelLiner_FL` | Paso de rueda interior (cubre-ruedas de plástico) | Malla | 3 | Aproximado |
| `BODY_WheelLiner_FR` | Paso de rueda interior (cubre-ruedas de plástico) | Malla | 3 | Aproximado |
| `BODY_WheelLiner_RL` | Paso de rueda interior (cubre-ruedas de plástico) | Malla | 3 | Aproximado |
| `BODY_WheelLiner_RR` | Paso de rueda interior (cubre-ruedas de plástico) | Malla | 3 | Aproximado |
| `EXT_Roof_Header_Front` | Travesaño delantero del techo | Malla | 3 | Aproximado |
| `EXT_Roof_Header_Rear` | Travesaño trasero del techo | Malla | 3 | Aproximado |
| `EXT_RoofRail_L` | Pilar A y larguero de techo (izquierda) | Malla | 3 | Reconstruido |
| `EXT_RoofRail_R` | Pilar A y larguero de techo (derecha) | Malla | 3 | Reconstruido |

## Caja de carga (`CARGO_BED`) — 36

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `CARGO_Bed_Outlets` | Tomas de corriente de 120 V y 240 V de la caja — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Bed_Tub` | Cubeta compuesta de la caja (sin necesidad de protector) | Malla | 6 | Reconstruido |
| `CARGO_BED_TUB` | Caja de carga compuesta (6' x 4') | Conjunto | 3 | Reconstruido |
| `CARGO_Gear_Locker` | Compartimento inferior Gear Locker (97 l) | Malla | 6 | Reconstruido |
| `CARGO_Tiedowns` | Anclajes forjados de la caja (suelo y laterales) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Applique` | Embellecedor superior de la cubierta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Cassette` | Casete plano donde se recogen las lamas (Flat Cassette) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Chain_L` | Eslabones de cadena de arrastre de las lamas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Chain_R` | Eslabones de cadena de arrastre de las lamas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Motor_L` | Motor izquierdo de la cubierta (2 tornillos a 11 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Motor_R` | Motor derecho de la cubierta (2 tornillos a 11 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Rail_L` | Raíl «horizon» izquierdo de aluminio extruido — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Rail_R` | Raíl «horizon» derecho de aluminio extruido — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_01` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_02` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_03` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_04` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_05` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_06` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_07` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_08` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_09` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_10` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_11` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_12` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_13` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_14` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_15` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_16` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_17` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_18` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_19` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_20` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_21` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `CARGO_Tonneau_Slat_22` | Lama de aluminio extruido con articulación y casquillos (Mid Slat) | Malla | 6 | Reconstruido |
| `TONNEAU_ASSEMBLY` | Cubierta rígida motorizada (tonneau) | Conjunto | 1 | Reconstruido |

## Ruedas y frenos delanteros (`FRONT_WHEELS_AND_BRAKES`) — 22

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `BRAKE_FL` | Freno delantero izquierdo | Conjunto | 4 | Reconstruido |
| `BRAKE_FR` | Freno delantero derecho | Conjunto | 4 | Reconstruido |
| `BRK_FL_Caliper` | Pinza fija de 4 pistones (2 tornillos de 24 mm, 315 N·m) | Malla | 6 | Verificado |
| `BRK_FL_Pads` | Pastillas de freno (10 mm de material nuevo) | Malla | 6 | Reconstruido |
| `BRK_FL_Rotor` | Disco ventilado Ø351 mm | Malla | 6 | Verificado |
| `BRK_FL_Shield` | Protector de polvo del disco | Malla | 6 | Aproximado |
| `BRK_FR_Caliper` | Pinza fija de 4 pistones (2 tornillos de 24 mm, 315 N·m) | Malla | 6 | Verificado |
| `BRK_FR_Pads` | Pastillas de freno (10 mm de material nuevo) | Malla | 6 | Reconstruido |
| `BRK_FR_Rotor` | Disco ventilado Ø351 mm | Malla | 6 | Verificado |
| `BRK_FR_Shield` | Protector de polvo del disco | Malla | 6 | Aproximado |
| `WHEEL_FL` | Conjunto de rueda delantera izquierda | Conjunto | 4 | Verificado |
| `WHEEL_FR` | Conjunto de rueda delantera derecha | Conjunto | 4 | Verificado |
| `WHL_FL_Cover_Core` | Tapacubos aerodinámico «Core» 20" (8 grapas sobre anillo de montaje) | Malla | 6 | Reconstruido |
| `WHL_FL_LugNuts` | Tuercas de rueda (6), llave de 21 mm, 205 N·m | Malla | 6 | Reconstruido |
| `WHL_FL_Rim` | Llanta de aleación 20 x 9.0J ET58.5 (Stealth Black) | Malla | 6 | Reconstruido |
| `WHL_FL_Tire` | Neumático Pirelli Scorpion ATR 285/65R20 (T0) — _Medidas verificadas; dibujo de 5 hileras reconstruido; inscripciones aproximadas_ | Malla | 6 | Reconstruido |
| `WHL_FL_Valve_TPMS` | Válvula con sensor de presión TPMS | Malla | 6 | Reconstruido |
| `WHL_FR_Cover_Core` | Tapacubos aerodinámico «Core» 20" (8 grapas sobre anillo de montaje) | Malla | 6 | Reconstruido |
| `WHL_FR_LugNuts` | Tuercas de rueda (6), llave de 21 mm, 205 N·m | Malla | 6 | Reconstruido |
| `WHL_FR_Rim` | Llanta de aleación 20 x 9.0J ET58.5 (Stealth Black) | Malla | 6 | Reconstruido |
| `WHL_FR_Tire` | Neumático Pirelli Scorpion ATR 285/65R20 (T0) — _Medidas verificadas; dibujo de 5 hileras reconstruido; inscripciones aproximadas_ | Malla | 6 | Reconstruido |
| `WHL_FR_Valve_TPMS` | Válvula con sensor de presión TPMS | Malla | 6 | Reconstruido |

## Ruedas y frenos traseros (`REAR_WHEELS_AND_BRAKES`) — 22

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `BRAKE_RL` | Freno trasero izquierdo | Conjunto | 4 | Reconstruido |
| `BRAKE_RR` | Freno trasero derecho | Conjunto | 4 | Reconstruido |
| `BRK_RL_Caliper` | Pinza flotante de 1 pistón con freno de estacionamiento eléctrico (EPB) | Malla | 6 | Verificado |
| `BRK_RL_Pads` | Pastillas de freno (11 mm de material nuevo) | Malla | 6 | Reconstruido |
| `BRK_RL_Rotor` | Disco ventilado Ø356 mm | Malla | 6 | Verificado |
| `BRK_RL_Shield` | Protector de polvo del disco | Malla | 6 | Aproximado |
| `BRK_RR_Caliper` | Pinza flotante de 1 pistón con freno de estacionamiento eléctrico (EPB) | Malla | 6 | Verificado |
| `BRK_RR_Pads` | Pastillas de freno (11 mm de material nuevo) | Malla | 6 | Reconstruido |
| `BRK_RR_Rotor` | Disco ventilado Ø356 mm | Malla | 6 | Verificado |
| `BRK_RR_Shield` | Protector de polvo del disco | Malla | 6 | Aproximado |
| `WHEEL_RL` | Conjunto de rueda trasera izquierda | Conjunto | 4 | Verificado |
| `WHEEL_RR` | Conjunto de rueda trasera derecha | Conjunto | 4 | Verificado |
| `WHL_RL_Cover_Core` | Tapacubos aerodinámico «Core» 20" (8 grapas sobre anillo de montaje) | Malla | 6 | Reconstruido |
| `WHL_RL_LugNuts` | Tuercas de rueda (6), llave de 21 mm, 205 N·m | Malla | 6 | Reconstruido |
| `WHL_RL_Rim` | Llanta de aleación 20 x 9.0J ET58.5 (Stealth Black) | Malla | 6 | Reconstruido |
| `WHL_RL_Tire` | Neumático Pirelli Scorpion ATR 285/65R20 (T0) — _Medidas verificadas; dibujo de 5 hileras reconstruido; inscripciones aproximadas_ | Malla | 6 | Reconstruido |
| `WHL_RL_Valve_TPMS` | Válvula con sensor de presión TPMS | Malla | 6 | Reconstruido |
| `WHL_RR_Cover_Core` | Tapacubos aerodinámico «Core» 20" (8 grapas sobre anillo de montaje) | Malla | 6 | Reconstruido |
| `WHL_RR_LugNuts` | Tuercas de rueda (6), llave de 21 mm, 205 N·m | Malla | 6 | Reconstruido |
| `WHL_RR_Rim` | Llanta de aleación 20 x 9.0J ET58.5 (Stealth Black) | Malla | 6 | Reconstruido |
| `WHL_RR_Tire` | Neumático Pirelli Scorpion ATR 285/65R20 (T0) — _Medidas verificadas; dibujo de 5 hileras reconstruido; inscripciones aproximadas_ | Malla | 6 | Reconstruido |
| `WHL_RR_Valve_TPMS` | Válvula con sensor de presión TPMS | Malla | 6 | Reconstruido |

## Suspensión delantera (`FRONT_SUSPENSION`) — 31

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `SUS_F_StabilizerBar` | Barra estabilizadora delantera con soportes y casquillos — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `SUS_FL_AirBag` | Fuelle neumático de lóbulo enrollable | Malla | 6 | Reconstruido |
| `SUS_FL_AirSpring` | Módulo de muelle neumático (3 tuercas superiores; 2 tornillos al brazo inferior) | Conjunto | 4 | Verificado |
| `SUS_FL_BrakeHose` | Latiguillo de freno con tornillo hueco (42 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FL_Damper` | Amortiguador adaptativo (CDC) monotubo | Malla | 6 | Reconstruido |
| `SUS_FL_Damper_Rod` | Vástago del amortiguador | Malla | 6 | Reconstruido |
| `SUS_FL_Hub` | Buje motriz con rodamiento y 6 espárragos (4 tornillos al portamangueta, 105 N·m) | Malla | 6 | Reconstruido |
| `SUS_FL_Knuckle` | Portamangueta de aluminio fundido (rodamiento, rótulas, brazo de dirección, orejetas de pinza) | Malla | 6 | Reconstruido |
| `SUS_FL_LCA_AeroShield` | Deflector aerodinámico del brazo inferior (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FL_LowerArm` | Brazo inferior delantero con rótula (tornillos de 24 mm al subchasis) | Malla | 6 | Reconstruido |
| `SUS_FL_Piston` | Pistón de rodadura de aluminio | Malla | 6 | Reconstruido |
| `SUS_FL_StabLink` | Bieleta de la barra estabilizadora (275 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FL_TopMount` | Copela superior con 3 espárragos, racor de aire y conector | Malla | 6 | Reconstruido |
| `SUS_FL_UpperArm` | Brazo superior en A (4 tuercas a la carrocería, rótula a 80 N·m) | Malla | 6 | Reconstruido |
| `SUS_FL_WheelSpeedSensor` | Sensor de velocidad de rueda (ABS) y cable — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FR_AirBag` | Fuelle neumático de lóbulo enrollable | Malla | 6 | Reconstruido |
| `SUS_FR_AirSpring` | Módulo de muelle neumático (3 tuercas superiores; 2 tornillos al brazo inferior) | Conjunto | 4 | Verificado |
| `SUS_FR_BrakeHose` | Latiguillo de freno con tornillo hueco (42 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FR_Damper` | Amortiguador adaptativo (CDC) monotubo | Malla | 6 | Reconstruido |
| `SUS_FR_Damper_Rod` | Vástago del amortiguador | Malla | 6 | Reconstruido |
| `SUS_FR_Hub` | Buje motriz con rodamiento y 6 espárragos (4 tornillos al portamangueta, 105 N·m) | Malla | 6 | Reconstruido |
| `SUS_FR_Knuckle` | Portamangueta de aluminio fundido (rodamiento, rótulas, brazo de dirección, orejetas de pinza) | Malla | 6 | Reconstruido |
| `SUS_FR_LCA_AeroShield` | Deflector aerodinámico del brazo inferior (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FR_LowerArm` | Brazo inferior delantero con rótula (tornillos de 24 mm al subchasis) | Malla | 6 | Reconstruido |
| `SUS_FR_Piston` | Pistón de rodadura de aluminio | Malla | 6 | Reconstruido |
| `SUS_FR_StabLink` | Bieleta de la barra estabilizadora (275 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_FR_TopMount` | Copela superior con 3 espárragos, racor de aire y conector | Malla | 6 | Reconstruido |
| `SUS_FR_UpperArm` | Brazo superior en A (4 tuercas a la carrocería, rótula a 80 N·m) | Malla | 6 | Reconstruido |
| `SUS_FR_WheelSpeedSensor` | Sensor de velocidad de rueda (ABS) y cable — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUSP_FL` | Suspensión delantera izquierda | Conjunto | 4 | Reconstruido |
| `SUSP_FR` | Suspensión delantera derecha | Conjunto | 4 | Reconstruido |

## Suspensión trasera (`REAR_SUSPENSION`) — 36

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `AIR_SUPPLY` | Suministro de aire de la suspensión | Conjunto | 4 | Reconstruido |
| `CHS_AirSuspension_Compressor` | Compresor de la suspensión neumática con soporte (3 tuercas) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_AirSuspension_Lines` | Conductos de aire a los cuatro módulos de muelle — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_AirSuspension_Reservoir` | Depósito de aire (4 racores VOSS, 2 tuercas) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_AirSuspension_ValveBlock` | Bloque de válvulas (5 conductos de aire) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_R_StabilizerBar` | Barra estabilizadora trasera (abrazaderas de banda sobre aislantes; 4 tornillos a 50 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `SUS_RL_AirBag` | Fuelle neumático de lóbulo enrollable | Malla | 6 | Reconstruido |
| `SUS_RL_AirSpring` | Módulo de muelle neumático (3 tuercas superiores; 2 tornillos al brazo inferior) | Conjunto | 4 | Verificado |
| `SUS_RL_BrakeHose` | Latiguillo de freno con tornillo hueco (42 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RL_Damper` | Amortiguador adaptativo (CDC) monotubo | Malla | 6 | Reconstruido |
| `SUS_RL_Damper_Rod` | Vástago del amortiguador | Malla | 6 | Reconstruido |
| `SUS_RL_Hub` | Buje motriz con rodamiento y 6 espárragos (4 tornillos al portamangueta, 105 N·m) | Malla | 6 | Reconstruido |
| `SUS_RL_Knuckle` | Portamangueta de aluminio fundido (rodamiento, rótulas, brazo de dirección, orejetas de pinza) | Malla | 6 | Reconstruido |
| `SUS_RL_LCA_AeroShield` | Deflector aerodinámico del brazo inferior (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RL_LowerArm` | Brazo inferior trasero soldado (4 tornillos de 21 mm a 185 N·m) | Malla | 6 | Reconstruido |
| `SUS_RL_Piston` | Pistón de rodadura de aluminio | Malla | 6 | Reconstruido |
| `SUS_RL_StabLink` | Bieleta de la barra estabilizadora (275 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RL_TopMount` | Copela superior con 3 espárragos, racor de aire y conector | Malla | 6 | Reconstruido |
| `SUS_RL_UpperArm` | Brazo superior en A (4 tuercas a la carrocería, rótula a 80 N·m) | Malla | 6 | Reconstruido |
| `SUS_RL_WheelSpeedSensor` | Sensor de velocidad de rueda (ABS) y cable — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RR_AirBag` | Fuelle neumático de lóbulo enrollable | Malla | 6 | Reconstruido |
| `SUS_RR_AirSpring` | Módulo de muelle neumático (3 tuercas superiores; 2 tornillos al brazo inferior) | Conjunto | 4 | Verificado |
| `SUS_RR_BrakeHose` | Latiguillo de freno con tornillo hueco (42 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RR_Damper` | Amortiguador adaptativo (CDC) monotubo | Malla | 6 | Reconstruido |
| `SUS_RR_Damper_Rod` | Vástago del amortiguador | Malla | 6 | Reconstruido |
| `SUS_RR_Hub` | Buje motriz con rodamiento y 6 espárragos (4 tornillos al portamangueta, 105 N·m) | Malla | 6 | Reconstruido |
| `SUS_RR_Knuckle` | Portamangueta de aluminio fundido (rodamiento, rótulas, brazo de dirección, orejetas de pinza) | Malla | 6 | Reconstruido |
| `SUS_RR_LCA_AeroShield` | Deflector aerodinámico del brazo inferior (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RR_LowerArm` | Brazo inferior trasero soldado (4 tornillos de 21 mm a 185 N·m) | Malla | 6 | Reconstruido |
| `SUS_RR_Piston` | Pistón de rodadura de aluminio | Malla | 6 | Reconstruido |
| `SUS_RR_StabLink` | Bieleta de la barra estabilizadora (275 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUS_RR_TopMount` | Copela superior con 3 espárragos, racor de aire y conector | Malla | 6 | Reconstruido |
| `SUS_RR_UpperArm` | Brazo superior en A (4 tuercas a la carrocería, rótula a 80 N·m) | Malla | 6 | Reconstruido |
| `SUS_RR_WheelSpeedSensor` | Sensor de velocidad de rueda (ABS) y cable — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `SUSP_RL` | Suspensión trasera izquierda | Conjunto | 4 | Reconstruido |
| `SUSP_RR` | Suspensión trasera derecha | Conjunto | 4 | Reconstruido |

## Dirección (`STEERING`) — 12

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `INT_Steering_Column_Shroud` | Cubierta de la columna y actuador de realimentación | Malla | 6 | Reconstruido |
| `INT_SteeringWheel_Controls` | Botonera de los radios (intermitentes, luces, bocina) y rodillos de desplazamiento — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SteeringWheel_Hub` | Buje con módulo de airbag del conductor y radios | Malla | 6 | Reconstruido |
| `INT_SteeringWheel_Rim` | Aro del volante | Malla | 6 | Reconstruido |
| `STEERING_WHEEL` | Volante «squircle» (dirección por cable) | Conjunto | 2 | Reconstruido |
| `STR_F_Actuator` | Actuador de dirección delantero (steer-by-wire, dos motores, 4 conectores) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `STR_FL_TieRod` | Bieleta de dirección exterior (170 N·m al portamangueta) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `STR_FR_TieRod` | Bieleta de dirección exterior (170 N·m al portamangueta) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `STR_R_Actuator` | Actuador de dirección trasero (convergencia de las ruedas traseras, 4 tornillos a 120 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `STR_RL_TieRod` | Bieleta de convergencia trasera (170/180 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `STR_RR_TieRod` | Bieleta de convergencia trasera (170/180 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `STR_Steering_Feedback_Actuator` | Actuador de realimentación del volante (steer-by-wire) y soporte de la columna — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |

## Batería y alta tensión (`BATTERY_ASSEMBLY`) — 49

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `ANCILLARY_BAY` | Bahía auxiliar de alta tensión (accesible desde la caja de carga) | Conjunto | 5 | Reconstruido |
| `BAT_Block_1_Busbars` | Colectores de corriente sobre las celdas | Malla | 6 | Reconstruido |
| `BAT_Block_1_Cells` | Bloque 1: 336 celdas cilíndricas 4680 (7 columnas x 48) — _Recuento 1.344 verificado (pasaporte); disposición 4 x 7 x 48 según el desmontaje de Munro_ | Malla | 6 | Reconstruido |
| `BAT_Block_1_Coolers` | Refrigeradores en serpentín y colectores del bloque — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_1_Foam` | Espuma estructural que fija las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_1_Mica` | Lámina de mica (barrera térmica) sobre las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_2_Busbars` | Colectores de corriente sobre las celdas | Malla | 6 | Reconstruido |
| `BAT_Block_2_Cells` | Bloque 2: 336 celdas cilíndricas 4680 (7 columnas x 48) — _Recuento 1.344 verificado (pasaporte); disposición 4 x 7 x 48 según el desmontaje de Munro_ | Malla | 6 | Reconstruido |
| `BAT_Block_2_Coolers` | Refrigeradores en serpentín y colectores del bloque — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_2_Foam` | Espuma estructural que fija las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_2_Mica` | Lámina de mica (barrera térmica) sobre las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_3_Busbars` | Colectores de corriente sobre las celdas | Malla | 6 | Reconstruido |
| `BAT_Block_3_Cells` | Bloque 3: 336 celdas cilíndricas 4680 (7 columnas x 48) — _Recuento 1.344 verificado (pasaporte); disposición 4 x 7 x 48 según el desmontaje de Munro_ | Malla | 6 | Reconstruido |
| `BAT_Block_3_Coolers` | Refrigeradores en serpentín y colectores del bloque — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_3_Foam` | Espuma estructural que fija las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_3_Mica` | Lámina de mica (barrera térmica) sobre las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_4_Busbars` | Colectores de corriente sobre las celdas | Malla | 6 | Reconstruido |
| `BAT_Block_4_Cells` | Bloque 4: 336 celdas cilíndricas 4680 (7 columnas x 48) — _Recuento 1.344 verificado (pasaporte); disposición 4 x 7 x 48 según el desmontaje de Munro_ | Malla | 6 | Reconstruido |
| `BAT_Block_4_Coolers` | Refrigeradores en serpentín y colectores del bloque — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_4_Foam` | Espuma estructural que fija las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Block_4_Mica` | Lámina de mica (barrera térmica) sobre las celdas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Chinstrap_Front` | Correa delantera (chinstrap) y tomas de refrigerante — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Enclosure_Lid` | Tapa estructural (suelo del habitáculo) con anclajes de los asientos delanteros | Malla | 6 | Reconstruido |
| `BAT_Enclosure_Tray` | Bandeja estructural con brida perimetral (44 tornillos a los largueros) | Malla | 6 | Reconstruido |
| `BAT_HV_Header` | Cabecera de conectores de alta tensión (unidad delantera, carga rápida) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Internal_Beams` | Vigas extruidas entre bloques | Malla | 6 | Reconstruido |
| `BAT_Pyro_Fuses` | Pirofusibles primario y secundario (2 tornillos cada uno) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BAT_Thermal_Vent_FloodPorts` | Respiradero térmico (tapa naranja, apagallamas), puertos de inundación y respiradero — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `BATTERY_PACK` | Batería estructural de alta tensión (~123 kWh, 1.344 celdas 4680, ~800 V) | Conjunto | 5 | Reconstruido |
| `HV_AC_Junction_Box` | Caja de conexiones de CA (ACJB) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `HV_Ancillary_Cover` | Cubierta de la bahía auxiliar — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `HV_Cables` | Cables de alta tensión (unidad delantera, compresor, inversores traseros) | Malla | 5 | Reconstruido |
| `HV_Device_Cluster` | Clúster de dispositivos (contactores y fusibles) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `HV_Last_Mile_Busbar` | Barra colectora «last mile» hacia la toma de carga — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `HV_Power_Conversion_System` | Sistema de conversión de potencia (cargador de a bordo y CC/CC de 48 V) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `LV_Battery_48V` | Batería de media tensión de 48 V (2 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `LV_Body_Controller_LH` | Controlador de carrocería izquierdo (4 tuercas al mamparo) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `LV_Body_Controller_Rear` | Controlador trasero (media tensión) (4 tuercas al mamparo) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `LV_Body_Controller_RH` | Controlador de carrocería derecho (4 tuercas al mamparo) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `LV_Harness_Bed_L` | Mazo izquierdo de la caja (luces, tomas, motor de la cubierta) | Malla | 6 | Reconstruido |
| `LV_Harness_Bed_R` | Mazo derecho de la caja | Malla | 6 | Reconstruido |
| `LV_Harness_Door_FL` | Mazo de la puerta delantera izquierda | Malla | 6 | Reconstruido |
| `LV_Harness_Door_FR` | Mazo de la puerta delantera derecha | Malla | 6 | Reconstruido |
| `LV_Harness_Door_RL` | Mazo de la puerta trasera izquierda | Malla | 6 | Reconstruido |
| `LV_Harness_Door_RR` | Mazo de la puerta trasera derecha | Malla | 6 | Reconstruido |
| `LV_Harness_Frunk` | Mazo del frunk, faros y fascia delantera | Malla | 6 | Reconstruido |
| `LV_Harness_MV_Backbone` | Mazo principal de 48 V con anillo Ethernet redundante | Malla | 5 | Reconstruido |
| `LV_Harness_Tailgate` | Mazo del portón (luz, cámara, cierres) | Malla | 6 | Reconstruido |
| `LV_Harness_Windshield` | Mazo del parabrisas y del módulo de cámaras (por el pilar A) | Malla | 6 | Reconstruido |

## Unidades motrices (`DRIVE_UNITS`) — 22

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `DRIVE_UNIT_FRONT` | Unidad motriz delantera (motor síncrono de imanes permanentes, inversor integrado) | Conjunto | 5 | Verificado |
| `DRIVE_UNIT_REAR` | Unidad motriz trasera tri-motor: dos motores de inducción con vectorización de par | Conjunto | 5 | Verificado |
| `DU_F_Gearbox` | Reductora de una velocidad (15,02:1) con diferencial y bloqueo electromagnético | Malla | 6 | Reconstruido |
| `DU_F_HeatExchanger` | Intercambiador aceite-refrigerante de la unidad delantera — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_F_Inverter` | Inversor integrado de la unidad delantera con cabecera de alta tensión | Malla | 6 | Reconstruido |
| `DU_F_Motor_Housing` | Carcasa del motor de imanes permanentes (estátor de horquillas) | Malla | 6 | Reconstruido |
| `DU_F_Mounts` | Soportes elásticos y trenza de masa | Malla | 6 | Reconstruido |
| `DU_F_NVH_Cover` | Cubierta acústica (NVH) del motor delantero — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_F_OilPump_Filter` | Bomba de aceite eléctrica, filtro de aceite y respiradero — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_Halfshaft_FL` | Semieje delantero con juntas homocinéticas (tornillo central de 24 mm a 300 N·m) | Malla | 5 | Reconstruido |
| `DU_Halfshaft_FR` | Semieje delantero con juntas homocinéticas (tornillo central de 24 mm a 300 N·m) | Malla | 5 | Reconstruido |
| `DU_Halfshaft_RL` | Semieje trasero con juntas homocinéticas (tornillo central de 24 mm a 300 N·m) | Malla | 5 | Reconstruido |
| `DU_Halfshaft_RR` | Semieje trasero con juntas homocinéticas (tornillo central de 24 mm a 300 N·m) | Malla | 5 | Reconstruido |
| `DU_R_Gearbox` | Carcasa común de las dos reductoras independientes (15,02:1), desplazadas hacia atrás | Malla | 6 | Reconstruido |
| `DU_R_Inverter_L` | Inversor del motor trasero izquierdo (montado en su parte posterior) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_Inverter_R` | Inversor del motor trasero derecho (montado en su parte posterior) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_Motor_L` | Motor de inducción trasero izquierdo (rotor de cobre) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_Motor_R` | Motor de inducción trasero derecho (rotor de cobre) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_Mounts` | Soportes de la unidad trasera y trenza de masa | Malla | 6 | Reconstruido |
| `DU_R_OilPump_Filter` | Bomba de aceite (LH, tri-motor) y filtro — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_PlateCooler_L` | Refrigerador de placa aceite-refrigerante sobre el motor — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `DU_R_PlateCooler_R` | Refrigerador de placa aceite-refrigerante sobre el motor — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |

## Bajos y subchasis (`UNDERBODY`) — 23

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `BRK_Booster_Electromechanical` | Servofreno electromecánico (3 tuercas al pedalier) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `BRK_Hydraulic_Control_Unit` | Unidad hidráulica ABS/ESC (HCU, 3 tuercas al soporte) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `BRK_Pipes` | Tubos rígidos de freno desde la HCU a las cuatro esquinas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 4 | Reconstruido |
| `BRK_Remote_Reservoir` | Depósito remoto del líquido de frenos (DOT4) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_Active_Grille_Shutter` | Persianas activas de la rejilla (7 lamas) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_Aeroshield_Front` | Deflector aerodinámico delantero (11 tornillos de 10 mm) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `CHS_Aeroshield_Mid` | Deflector central bajo la batería (6 grapas y 10 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `CHS_Aeroshield_Rear` | Deflector aerodinámico trasero — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `CHS_Cooling_Fan_Module` | Módulo de ventiladores (CFM, 6 tornillos de 10 Nm) con dos rotores — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `CHS_Radiator` | Radiador de baja temperatura con depósitos laterales | Malla | 6 | Reconstruido |
| `CHS_Recovery_Hooks_Front` | Ganchos de rescate delanteros (4 tornillos a 78 N·m cada uno) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `CHS_Skid_Plate_Front` | Placa de protección delantera (8 tuercas de 15 mm y 2 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 3 | Reconstruido |
| `CHS_Subframe_F` | Subchasis delantero (AWD): brazos inferiores, actuador de dirección y unidad delantera | Malla | 3 | Reconstruido |
| `CHS_Subframe_R` | Subchasis trasero tri-motor: brazos inferiores, actuador trasero y unidad trasera | Malla | 3 | Reconstruido |
| `CHS_Tow_Hitch_Receiver` | Receptor del enganche de remolque (clase IV) | Malla | 3 | Reconstruido |
| `THERMAL_FRONT` | Gestión térmica delantera (Supermanifold y CFM) | Conjunto | 3 | Reconstruido |
| `THM_AC_Compressor` | Compresor eléctrico de A/C (scroll) sobre la Megabeam (3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `THM_AC_Compressor_Acoustic_Cover` | Cubierta acústica del compresor — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `THM_AC_Lines` | Tuberías de aspiración y descarga del refrigerante R1234yf — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `THM_Battery_Coolant_Hoses` | Mangueras de impulsión y retorno de la batería — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `THM_Powertrain_Hose_Bundle` | Haz de mangueras del tren motriz (impulsión y retorno) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 5 | Reconstruido |
| `THM_Radiator_Hoses` | Mangueras radiador ↔ Supermanifold — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `THM_Supermanifold` | Supermanifold con Octovalve, bombas, enfriador, condensador y botella (2 tornillos de 15 mm) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |

## Salpicadero (`INTERIOR_DASHBOARD`) — 12

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `INT_Airbag_Modules` | Módulos de airbag del acompañante y de rodillas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Car_Computer` | Ordenador del vehículo (infoentretenimiento y Autopilot) con disipador — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_HVAC_Module` | Módulo de climatización (ventilador, filtro HEPA, compuertas) y conductos al suelo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_IP_Airwave_Vent` | Salida de aire continua (Airwave) | Malla | 6 | Reconstruido |
| `INT_IP_Ambient_Light` | Tira de luz ambiental | Malla | 6 | Aproximado |
| `INT_IP_Defrost_Panel` | Panel de desempañado del parabrisas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_IP_Glovebox` | Guantera (5 tornillos T20) con luz de cortesía — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_IP_Lower_Driver` | Panel inferior del conductor (protección de rodillas) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_IP_Quarter_Panel_L` | Panel lateral del salpicadero con salida de desempañado lateral — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_IP_Quarter_Panel_R` | Panel lateral del salpicadero con salida de desempañado lateral — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_IP_TopPad` | Panel superior del salpicadero (Tactical Grey) | Malla | 2 | Reconstruido |
| `IP_ASSEMBLY` | Conjunto del salpicadero | Conjunto | 2 | Reconstruido |

## Mandos y pantallas (`INTERIOR_CONTROLS`) — 21

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `CONSOLE_ASSEMBLY` | Consola central | Conjunto | 2 | Reconstruido |
| `DISPLAY_CENTER` | Pantalla táctil central de 18,5" | Conjunto | 2 | Verificado |
| `INT_Console_Armrest` | Reposabrazos (tapa del compartimento de almacenamiento) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Console_Armrest_Stitching` | Costuras del reposabrazos | Malla | 6 | Reconstruido |
| `INT_Console_Body` | Estructura de la consola central | Malla | 6 | Reconstruido |
| `INT_Console_Cupholder_1` | Portavasos | Malla | 6 | Aproximado |
| `INT_Console_Cupholder_2` | Portavasos | Malla | 6 | Aproximado |
| `INT_Console_Decor_Top` | Embellecedor superior de la consola — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Console_Side_Panel_L` | Panel lateral exterior de la consola — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Console_Side_Panel_R` | Panel lateral exterior de la consola — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Console_USB_Ports` | Puertos USB-C delanteros y traseros (concentrador USB) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Console_Wireless_Charger_1` | Cargador inalámbrico de 15 W con superficie antideslizante — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Console_Wireless_Charger_2` | Cargador inalámbrico de 15 W con superficie antideslizante — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Display_Center_Housing` | Carcasa de la pantalla central | Malla | 6 | Reconstruido |
| `INT_Display_Center_Mount` | Soporte de la pantalla | Malla | 6 | Aproximado |
| `INT_Display_Center_Screen` | Panel de 18,5" (409,6 x 230,4 mm) | Malla | 6 | Verificado |
| `INT_Display_Rear_Housing` | Carcasa de la pantalla trasera | Malla | 2 | Reconstruido |
| `INT_Display_Rear_Screen` | Pantalla trasera de 9,4" | Malla | 2 | Verificado |
| `INT_Pedal_Accelerator` | Pedal del acelerador articulado en el suelo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Pedal_Brake` | Pedal de freno (al servofreno electromecánico) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Restraint_Control_Module` | Módulo de control de airbags (RCM, 3 tuercas a 10 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |

## Asientos y cinturones (`INTERIOR_SEATS`) — 37

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `INT_Seatbelt_Buckles` | Hebillas de los cinturones (delanteras con pretensor de cadera) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Seatbelt_FL` | Cinturón de tres puntos: cinta, guía, lengüeta, enrollador con pretensor y anclaje — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Seatbelt_FR` | Cinturón de tres puntos: cinta, guía, lengüeta, enrollador con pretensor y anclaje — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Seatbelt_RL` | Cinturón de tres puntos: cinta, guía, lengüeta, enrollador con pretensor y anclaje — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Seatbelt_RR` | Cinturón de tres puntos: cinta, guía, lengüeta, enrollador con pretensor y anclaje — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Back` | Respaldo con reposacabezas integrado | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Back_Shell` | Carcasa trasera del respaldo | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Base` | Base, guías y carcasas laterales del asiento | Malla | 2 | Aproximado |
| `INT_SeatF_L_Buttons` | Mandos de ajuste del cojín, del reclinado y lumbar de 8 vías — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Cushion` | Cojín con refuerzos laterales | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Side_Shield` | Escudo lateral exterior del asiento — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Stitching` | Costuras dobles de los paneles del asiento | Malla | 6 | Reconstruido |
| `INT_SeatF_L_Tracks` | Guías eléctricas y elevadores del asiento (4 tornillos T45P a 34 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Back` | Respaldo con reposacabezas integrado | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Back_Shell` | Carcasa trasera del respaldo | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Base` | Base, guías y carcasas laterales del asiento | Malla | 2 | Aproximado |
| `INT_SeatF_R_Buttons` | Mandos de ajuste del cojín, del reclinado y lumbar de 8 vías — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Cushion` | Cojín con refuerzos laterales | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Side_Shield` | Escudo lateral exterior del asiento — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Stitching` | Costuras dobles de los paneles del asiento | Malla | 6 | Reconstruido |
| `INT_SeatF_R_Tracks` | Guías eléctricas y elevadores del asiento (4 tornillos T45P a 34 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_Armrest` | Reposabrazos central trasero (abatible) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_Armrest_Cupholders` | Portavasos del reposabrazos trasero (embellecedor) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_Base` | Estructura de la banqueta | Malla | 2 | Aproximado |
| `INT_SeatR_C_Back` | Respaldo de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_C_Cushion` | Cojín abatible de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_C_Headrest` | Reposacabezas trasero con varillas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_L_Back` | Respaldo de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_L_Cushion` | Cojín abatible de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_L_Headrest` | Reposacabezas trasero con varillas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_R_Back` | Respaldo de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_R_Cushion` | Cojín abatible de la banqueta | Malla | 6 | Reconstruido |
| `INT_SeatR_R_Headrest` | Reposacabezas trasero con varillas — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_SeatR_Stitching` | Costuras de los cojines traseros | Malla | 6 | Reconstruido |
| `SEAT_FRONT_L` | Asiento delantero del conductor | Conjunto | 2 | Reconstruido |
| `SEAT_FRONT_R` | Asiento delantero del acompañante | Conjunto | 2 | Reconstruido |
| `SEAT_REAR` | Banqueta trasera de tres plazas | Conjunto | 2 | Reconstruido |

## Paneles de puerta (`INTERIOR_DOORS`) — 32

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `INT_Door_Beltline_FL` | Moldura de cintura (Beltline) con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Beltline_FR` | Moldura de cintura (Beltline) con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Beltline_RL` | Moldura de cintura (Beltline) con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Beltline_RR` | Moldura de cintura (Beltline) con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Lamps_FL` | Luz de cortesía inferior y catadióptrico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Lamps_FR` | Luz de cortesía inferior y catadióptrico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Lamps_RL` | Luz de cortesía inferior y catadióptrico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Lamps_RR` | Luz de cortesía inferior y catadióptrico de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Window_Switches_FL` | Interruptores de ventanilla (botonera del conductor) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Window_Switches_FR` | Interruptores de ventanilla — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Window_Switches_RL` | Interruptores de ventanilla — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Door_Window_Switches_RR` | Interruptores de ventanilla — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorArmrest_FL` | Reposabrazos acolchado de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorArmrest_FR` | Reposabrazos acolchado de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorArmrest_RL` | Reposabrazos acolchado de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorArmrest_RR` | Reposabrazos acolchado de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorButton_FL` | Pulsador interior de apertura | Malla | 2 | Reconstruido |
| `INT_DoorButton_FR` | Pulsador interior de apertura | Malla | 2 | Reconstruido |
| `INT_DoorButton_RL` | Pulsador interior de apertura | Malla | 2 | Reconstruido |
| `INT_DoorButton_RR` | Pulsador interior de apertura | Malla | 2 | Reconstruido |
| `INT_DoorPocket_FL` | Bolsillo con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorPocket_FR` | Bolsillo con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorPocket_RL` | Bolsillo con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorPocket_RR` | Bolsillo con luz ambiental — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorSpeaker_FL` | Rejilla del subwoofer de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorSpeaker_FR` | Rejilla del subwoofer de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorSpeaker_RL` | Rejilla del altavoz de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorSpeaker_RR` | Rejilla del altavoz de la puerta — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_DoorTrim_FL` | Panel de guarnecido de la puerta (14 grapas y 3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_DoorTrim_FR` | Panel de guarnecido de la puerta (14 grapas y 3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_DoorTrim_RL` | Panel de guarnecido de la puerta (14 grapas y 3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_DoorTrim_RR` | Panel de guarnecido de la puerta (14 grapas y 3 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |

## Guarnecidos interiores (`INTERIOR_TRIM`) — 28

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `INT_Cabin_Radar` | Radar de habitáculo (detección de ocupantes) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Cantrail_L` | Guarnecido del larguero del techo | Malla | 2 | Reconstruido |
| `INT_Cantrail_R` | Guarnecido del larguero del techo | Malla | 2 | Reconstruido |
| `INT_Carpet` | Moqueta del habitáculo | Malla | 2 | Reconstruido |
| `INT_Coathook_Maplight_L` | Gancho de abrigo y luz de lectura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Coathook_Maplight_R` | Gancho de abrigo y luz de lectura — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_FloorMat_FL` | Alfombrilla para todo tipo de clima con nervios y reborde — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_FloorMat_FR` | Alfombrilla para todo tipo de clima con nervios y reborde — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_FloorMat_R` | Alfombrilla para todo tipo de clima con nervios y reborde — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Footrest` | Reposapiés del conductor | Malla | 2 | Reconstruido |
| `INT_Overhead_Console` | Consola de techo delantera (luces de lectura) | Malla | 2 | Reconstruido |
| `INT_Rearview_Mirror` | Retrovisor interior sin marco con brazo (2 N·m) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Rearview_Mirror_Glass` | Espejo electrocrómico del retrovisor interior — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Speakers_Rear_Header` | Altavoces del larguero trasero — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 6 | Reconstruido |
| `INT_Subwoofer_CPillar_L` | Subwoofer del pilar C izquierdo (2 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Subwoofer_CPillar_R` | Subwoofer del pilar C derecho (2 tornillos) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_SunVisor_L` | Parasol con espejo y cortinilla (2 tornillos de 10 mm) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_SunVisor_R` | Parasol con espejo y cortinilla (2 tornillos de 10 mm) — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_APillar_L` | Guarnecido del pilar A izquierdo con altavoz de rango completo de 60 mm — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_APillar_R` | Guarnecido del pilar A derecho con altavoz de rango completo de 60 mm — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_BPillar_Lower_L` | Guarnecido inferior del pilar B izquierdo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_BPillar_Lower_R` | Guarnecido inferior del pilar B derecho — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_BPillar_Upper_L` | Guarnecido superior del pilar B izquierdo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_BPillar_Upper_R` | Guarnecido superior del pilar B derecho — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_CPillar_Lower_L` | Guarnecido inferior del pilar C izquierdo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_CPillar_Lower_R` | Guarnecido inferior del pilar C derecho — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_CPillar_Upper_L` | Guarnecido superior del pilar C izquierdo — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |
| `INT_Trim_CPillar_Upper_R` | Guarnecido superior del pilar C derecho — _Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida_ | Malla | 2 | Reconstruido |

## Cámaras, sensores y herrajes (`BODY_FASTENERS`) — 12

| Objeto | Descripción | Tipo | Etapa | Fidelidad |
|---|---|---|---|---|
| `CAM_BPillar_L` | Cámara del pilar B | Malla | 6 | Reconstruido |
| `CAM_BPillar_R` | Cámara del pilar B | Malla | 6 | Reconstruido |
| `CAM_FenderFlare_L` | Cámara de la aleta (repetidor lateral) | Malla | 6 | Reconstruido |
| `CAM_FenderFlare_R` | Cámara de la aleta (repetidor lateral) | Malla | 6 | Reconstruido |
| `CAM_Front_Fascia` | Cámara frontal (fascia delantera) | Malla | 6 | Reconstruido |
| `CAM_Windshield_Module` | Módulo de cámaras del parabrisas | Malla | 6 | Reconstruido |
| `EXT_TowEye_Cap_L` | Tapa del gancho de remolque delantero | Malla | 6 | Reconstruido |
| `EXT_TowEye_Cap_R` | Tapa del gancho de remolque delantero | Malla | 6 | Reconstruido |
| `SW_Door_Front_L` | Interruptor de apertura de la puerta delantera (pilar B) | Malla | 6 | Reconstruido |
| `SW_Door_Front_R` | Interruptor de apertura de la puerta delantera (pilar B) | Malla | 6 | Reconstruido |
| `SW_Door_Rear_L` | Interruptor de apertura de la puerta trasera (pilar C) | Malla | 6 | Reconstruido |
| `SW_Door_Rear_R` | Interruptor de apertura de la puerta trasera (pilar C) | Malla | 6 | Reconstruido |

