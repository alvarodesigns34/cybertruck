# Interferencias de ensamblaje pendientes

Informe generado con `node tools/gen_interferencias.mjs` a partir del detector `blender/scripts/interferencias.py` sobre la escena construida (explosión a cero). Se listan las parejas de objetos cuyas superficies visibles se cortan con una penetración mayor de 3 mm y que no están en la lista de penetraciones intencionadas. La profundidad se mide cerca de la zona de cruce; la extensión es la diagonal de la caja que envuelve esa zona.

## Resumen

| Penetración | Parejas |
|---|---|
| 3–5 mm | 98 |
| 5–10 mm | 128 |
| 10–30 mm | 52 |
| > 30 mm | 1 |
| **Total pendiente** | **279** |
| Penetraciones intencionadas (no se cuentan) | 230 |

| Zona | Parejas |
|---|---|
| Chasis (suspensión, frenos, dirección, aire) | 58 |
| Habitáculo (salpicadero, consola, guarnecidos) | 48 |
| Carrocería y estructura | 48 |
| Caja de carga, portón y persiana | 45 |
| Alta y baja tensión (batería, módulos y mazos) | 27 |
| Unidades motrices | 25 |
| Gestión térmica | 20 |
| Asientos y cinturones | 8 |

## Detalle por zona

### Chasis (suspensión, frenos, dirección, aire) (58)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `SUS_RL_AirBag` | `SUS_RL_BumpStop_SpringSeat` | 14.5 | 69 | -0.611, -1.855, 0.615 |
| `SUS_RR_AirBag` | `SUS_RR_BumpStop_SpringSeat` | 14.5 | 69 | 0.611, -1.855, 0.615 |
| `EXT_Rocker_Rear_Fairing_L` | `CHS_Air_Line_Bundle_L` | 10.3 | 60.4 | -0.823, -1.118, 0.288 |
| `CHS_Air_Line_Bundle_R` | `EXT_Rocker_Rear_Fairing_R` | 10.3 | 60.5 | 0.823, -1.118, 0.288 |
| `EXT_Rear_Diffuser` | `CHS_Air_Compressor_Exhaust` | 10.2 | 45.5 | -0.11, -2.552, 0.321 |
| `BODY_IP_CrossCar_Beam` | `STR_Steering_Feedback_Actuator` | 9.7 | 86.5 | -0.395, 1.046, 0.932 |
| `CHS_Air_Line_Bundle_L` | `CHS_AirSuspension_ValveBlock` | 9 | 26.8 | 0.345, -2.271, 0.504 |
| `CHS_AirSuspension_ValveBlock` | `CHS_Air_Line_Bundle_R` | 9 | 26.5 | 0.415, -2.271, 0.504 |
| `SUS_FL_LowerArm` | `SUS_FL_ArmBushings` | 8.9 | 601.5 | -0.348, 1.888, 0.303 |
| `SUS_RL_LowerArm` | `SUS_RL_ArmBushings` | 8.9 | 601.5 | -0.348, -1.888, 0.303 |
| `SUS_FR_ArmBushings` | `SUS_FR_LowerArm` | 8.9 | 601.5 | 0.348, 1.888, 0.303 |
| `SUS_RR_ArmBushings` | `SUS_RR_LowerArm` | 8.9 | 601.5 | 0.348, -1.888, 0.303 |
| `CHS_Recovery_Hooks_Front` | `CHS_Active_Grille_Shutter` | 8 | 901.3 | 0, 2.509, 0.47 |
| `SUS_FL_UpperArm` | `SUS_FL_ArmBushings` | 7.8 | 656.7 | -0.467, 1.907, 0.686 |
| `SUS_RL_UpperArm` | `SUS_RL_ArmBushings` | 7.8 | 656.7 | -0.467, -1.907, 0.686 |
| `SUS_FR_ArmBushings` | `SUS_FR_UpperArm` | 7.8 | 656.7 | 0.467, 1.907, 0.686 |
| `SUS_RR_ArmBushings` | `SUS_RR_UpperArm` | 7.8 | 656.7 | 0.467, -1.907, 0.686 |
| `BRK_RR_EPB_Motor` | `BRK_RR_Caliper_Service_Parts` | 7.6 | 26.7 | 0.736, -1.682, 0.57 |
| `SUS_FL_BumpStop_SpringSeat` | `SUS_FL_StabLink` | 7.2 | 52 | -0.628, 1.769, 0.385 |
| `SUS_RL_BumpStop_SpringSeat` | `SUS_RL_StabLink` | 7.2 | 52 | -0.628, -1.769, 0.385 |
| `SUS_FR_BumpStop_SpringSeat` | `SUS_FR_StabLink` | 7.2 | 52 | 0.628, 1.769, 0.385 |
| `SUS_RR_BumpStop_SpringSeat` | `SUS_RR_StabLink` | 7.2 | 52 | 0.628, -1.769, 0.385 |
| `SUS_FL_BumpStop_SpringSeat` | `SUS_F_StabilizerBar` | 6.7 | 36.3 | -0.619, 1.763, 0.386 |
| `SUS_RL_BumpStop_SpringSeat` | `SUS_R_StabilizerBar` | 6.7 | 36.3 | -0.619, -1.763, 0.386 |
| `SUS_F_StabilizerBar` | `SUS_FR_BumpStop_SpringSeat` | 6.7 | 36.3 | 0.619, 1.763, 0.386 |
| `SUS_R_StabilizerBar` | `SUS_RR_BumpStop_SpringSeat` | 6.7 | 36.3 | 0.619, -1.763, 0.386 |
| `SUS_RL_StabLink` | `SUS_R_StabilizerBar` | 6.6 | 42.4 | -0.62, -1.761, 0.394 |
| `SUS_R_StabilizerBar` | `SUS_RR_StabLink` | 6.6 | 42.4 | 0.62, -1.761, 0.394 |
| `BRK_RL_Caliper` | `BRK_RL_Caliper_Internals` | 6.3 | 143.5 | -0.861, -1.684, 0.509 |
| `BRK_RR_Caliper` | `BRK_RR_Caliper_Internals` | 6.3 | 143.4 | 0.861, -1.684, 0.509 |
| `BODY_Casting_Rear_UnderBody_L` | `CHS_AirSuspension_Compressor` | 6.2 | 79.9 | -0.472, -2.28, 0.485 |
| `BRK_Pipes` | `BRK_Hydraulic_Control_Unit` | 6 | 177.4 | 0.32, 2.12, 0.66 |
| `SUS_RR_Knuckle` | `BRK_RR_Pads` | 6 | 68 | 0.87, -1.708, 0.5 |
| `CHS_AirSuspension_ValveBlock` | `CHS_Air_Line_Bundle_Rear` | 5.5 | 18.4 | 0.424, -2.274, 0.506 |
| `SUS_RL_AirBag` | `SUS_RL_Piston` | 5.4 | 129.3 | -0.619, -1.918, 0.538 |
| `SUS_FL_AirBag` | `SUS_FL_Piston` | 5.4 | 129.3 | -0.613, 1.918, 0.626 |
| `SUS_RL_Piston` | `CHS_VOSS_Fittings` | 5.4 | 25.5 | -0.599, -1.877, 0.541 |
| `CHS_VOSS_Fittings` | `SUS_RR_Piston` | 5.4 | 25.5 | 0.599, -1.877, 0.541 |
| `SUS_FR_AirBag` | `SUS_FR_Piston` | 5.4 | 129.3 | 0.613, 1.918, 0.626 |
| `SUS_RR_AirBag` | `SUS_RR_Piston` | 5.4 | 129.3 | 0.619, -1.918, 0.538 |
| `BRK_FL_Caliper_Internals` | `BRK_FL_Pad_Shims` | 5.2 | 120.9 | -0.892, 1.693, 0.509 |
| `SUS_FL_Piston` | `CHS_VOSS_Fittings` | 5.2 | 28.3 | -0.599, 1.88, 0.611 |
| `CHS_VOSS_Fittings` | `SUS_FR_Piston` | 5.2 | 28.3 | 0.599, 1.88, 0.611 |
| `BRK_FR_Caliper_Internals` | `BRK_FR_Pad_Shims` | 5.2 | 120.9 | 0.892, 1.693, 0.509 |
| `STR_F_Motors_Internals` | `CHS_Subframe_F_Ground_Strap` | 5 | 90.1 | 0.204, 1.564, 0.477 |
| `STR_R_Motors_Internals` | `CHS_Subframe_R_Ground_Strap` | 5 | 90 | 0.204, -1.564, 0.477 |
| `STR_F_Motors_Internals` | `STR_F_Drive_Belts` | 4.6 | 118.4 | 0.11, 1.575, 0.435 |
| `CHS_Subframe_R` | `CHS_AirSuspension_Compressor` | 4.1 | 79.3 | -0.464, -2.245, 0.431 |
| `CHS_Active_Grille_Shutter` | `BODY_Front_Energy_Absorber_Bracket_Center` | 4 | 331.7 | 0, 2.5, 0.55 |
| `WHL_FL_Tire` | `WHL_FL_Rim` | 3.8 | 801.4 | -0.886, 1.818, 0.437 |
| `WHL_RL_Tire` | `WHL_RL_Rim` | 3.8 | 801.3 | -0.886, -1.817, 0.437 |
| `WHL_FR_Tire` | `WHL_FR_Rim` | 3.8 | 801.3 | 0.886, 1.818, 0.437 |
| `WHL_RR_Tire` | `WHL_RR_Rim` | 3.8 | 801.4 | 0.886, -1.817, 0.437 |
| `STR_F_Rack_BallNut` | `STR_F_Drive_Belts` | 3.6 | 116.8 | 0.11, 1.646, 0.425 |
| `CHS_Subframe_F` | `SUS_FL_ArmBushings` | 3.1 | 638.5 | -0.34, 1.892, 0.295 |
| `CHS_Subframe_F` | `SUS_FR_ArmBushings` | 3.1 | 638.1 | 0.339, 1.892, 0.293 |
| `CHS_Subframe_R` | `SUS_RL_ArmBushings` | 3.1 | 638.5 | -0.34, -1.892, 0.295 |
| `CHS_Subframe_R` | `SUS_RR_ArmBushings` | 3.1 | 638.1 | 0.339, -1.892, 0.293 |

### Habitáculo (salpicadero, consola, guarnecidos) (48)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `INT_SteeringWheel_Hub` | `INT_SteeringWheel_Hub_Internals` | 23.6 | 206.5 | -0.395, 0.773, 1.007 |
| `INT_Console_Body` | `INT_Console_Riser_Rails` | 23.6 | 1027 | 0, 0.4, 0.515 |
| `BODY_Super_Cowl` | `INT_Demist_Ducts_Center` | 14.8 | 702.3 | 0, 1.845, 1.209 |
| `INT_IP_Lower_Driver` | `INT_Airbag_Modules` | 14.5 | 267.8 | -0.48, 1.04, 0.69 |
| `LV_Harness_Windshield` | `CAM_Windshield_Module` | 14.3 | 128.9 | -0.043, 0.714, 1.663 |
| `INT_Floor_Duct_L` | `INT_FloorMat_FL` | 12.5 | 529.3 | -0.403, 0.925, 0.526 |
| `INT_Floor_Duct_R` | `INT_FloorMat_FR` | 12.5 | 587.3 | 0.403, 0.985, 0.526 |
| `BODY_DoorRing_R` | `INT_Trim_BPillar_Upper_R` | 11 | 457.6 | 0.792, 0.08, 1.502 |
| `INT_Trim_BPillar_Upper_L` | `BODY_Cantrail_Trim_Bracket_L` | 10.6 | 60.3 | -0.753, 0.056, 1.6 |
| `INT_Trim_BPillar_Upper_R` | `BODY_Cantrail_Trim_Bracket_R` | 10.6 | 60.3 | 0.753, 0.056, 1.6 |
| `LV_Harness_IP_Main` | `INT_IP_Airwave_Module_L` | 10.4 | 204.1 | -0.58, 1.065, 1.035 |
| `LV_Harness_IP_Main` | `INT_IP_Airwave_Module_R` | 10.4 | 207.7 | 0.58, 1.073, 1.035 |
| `INT_FloorMat_FL` | `INT_HVAC_Module` | 10.4 | 181.5 | -0.216, 0.905, 0.526 |
| `INT_HVAC_Module` | `INT_FloorMat_FR` | 10.4 | 186.3 | 0.216, 0.907, 0.526 |
| `BODY_DoorRing_R` | `INT_Trim_CPillar_Upper_R` | 10.2 | 291.7 | 0.821, -0.861, 1.479 |
| `INT_SteeringWheel_Hub` | `INT_SteeringWheel_Controls` | 10 | 315.4 | -0.395, 0.735, 1.007 |
| `INT_SteeringWheel_Hub` | `INT_Airbag_Driver` | 10 | 161 | -0.395, 0.738, 1.009 |
| `INT_DoorSpeaker_FL_Driver` | `EXT_Door_FL_Controller` | 8.4 | 81.1 | -0.83, 0.429, 0.721 |
| `INT_DoorSpeaker_FR_Driver` | `EXT_Door_FR_Controller` | 8.4 | 81.1 | 0.83, 0.429, 0.721 |
| `INT_Trim_APillar_R` | `BODY_DoorRing_R` | 8.2 | 1195.2 | 0.782, 1.178, 1.494 |
| `BODY_Header_Rear_Lower` | `INT_Speakers_Rear_Header` | 8 | 1061.3 | 0, -0.9, 1.594 |
| `INT_Steering_Column_Shroud_Lower` | `STR_Steering_Column_Control_Module` | 7.9 | 86.7 | -0.39, 0.931, 0.935 |
| `INT_SteeringWheel_Hub_Internals` | `INT_Airbag_Driver` | 7.5 | 133.6 | -0.395, 0.749, 1.013 |
| `BODY_IP_CrossCar_Beam` | `INT_HVAC_Module` | 7.4 | 447.1 | 0, 1.027, 0.581 |
| `INT_Windshield_Shades` | `BODY_Header_Front_Lower` | 7 | 1440 | 0, 0.495, 1.655 |
| `INT_Footrest` | `INT_Floor_Duct_L` | 6.9 | 73.3 | -0.685, 1.135, 0.516 |
| `ELE_Antennas` | `INT_HVAC_Sensors` | 6 | 32.2 | 0, 0.635, 1.677 |
| `INT_Rearview_Mirror` | `INT_Rearview_Beauty_Cover` | 5.7 | 65.4 | 0, 0.669, 1.688 |
| `INT_Trim_CPillar_Upper_L` | `BODY_CPillar_Inner_L` | 5.5 | 228.5 | -0.812, -0.853, 1.45 |
| `BODY_CPillar_Inner_R` | `INT_Trim_CPillar_Upper_R` | 5.5 | 228.5 | 0.812, -0.853, 1.45 |
| `INT_SteeringWheel_Rim` | `INT_SteeringWheel_Hub` | 5.1 | 353.3 | -0.395, 0.74, 1.005 |
| `INT_Center_Floor_Trim` | `INT_Floor_Duct_L` | 5 | 1151.3 | -0.43, 0.7, 0.525 |
| `INT_Center_Floor_Trim` | `INT_Floor_Duct_R` | 5 | 350.1 | 0.148, 0.375, 0.517 |
| `ELE_Antennas` | `INT_Rearview_Beauty_Cover` | 5 | 51.2 | 0, 0.635, 1.684 |
| `INT_DoorSpeaker_FL_Driver` | `INT_Door_NVH_Foam_FL` | 4.6 | 126.8 | -0.816, 0.459, 0.745 |
| `INT_DoorSpeaker_RL_Driver` | `INT_Door_NVH_Foam_RL` | 4.6 | 126.8 | -0.801, -0.539, 0.745 |
| `INT_Door_NVH_Foam_RR` | `INT_DoorSpeaker_RR_Driver` | 4.6 | 126.8 | 0.801, -0.539, 0.745 |
| `INT_Door_NVH_Foam_FR` | `INT_DoorSpeaker_FR_Driver` | 4.6 | 126.8 | 0.816, 0.459, 0.745 |
| `INT_Door_Manual_Release_FL` | `INT_Door_NVH_Foam_FL` | 4.5 | 67.4 | -0.816, 0.443, 0.857 |
| `INT_Door_Manual_Release_RL` | `INT_Door_NVH_Foam_RL` | 4.5 | 67.4 | -0.801, -0.557, 0.857 |
| `INT_Door_Manual_Release_RR` | `INT_Door_NVH_Foam_RR` | 4.5 | 67.4 | 0.801, -0.557, 0.857 |
| `INT_Door_Manual_Release_FR` | `INT_Door_NVH_Foam_FR` | 4.5 | 67.4 | 0.816, 0.443, 0.857 |
| `INT_IP_Gap_Hiders` | `INT_IP_Center_Shroud_Service_Panel` | 4 | 300.3 | 0, 0.959, 0.995 |
| `INT_IP_Mid_Panel` | `INT_IP_Glovebox` | 4 | 175 | 0.215, 0.975, 0.942 |
| `INT_FloorMat_FR` | `LV_Harness_Seat_R` | 4 | 220.7 | 0.282, 0.928, 0.526 |
| `BODY_IP_CrossCar_Beam` | `INT_FloorMat_FL` | 3.7 | 61.2 | -0.194, 1.014, 0.527 |
| `BODY_IP_CrossCar_Beam` | `INT_FloorMat_FR` | 3.7 | 68.9 | 0.194, 1.021, 0.53 |
| `INT_FloorMat_FL` | `LV_Harness_Seat_L` | 3.3 | 94.1 | -0.304, 0.884, 0.521 |

### Carrocería y estructura (48)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `EXT_Pedestrian_Speaker_Horn` | `BODY_Front_Bumper_Beam` | 16.6 | 1317.6 | 0, 2.513, 0.586 |
| `BODY_Casting_Front_UnderBody` | `BODY_Front_Body_Bridge_Reinforcement` | 14.9 | 1655.9 | 0, 1.74, 0.955 |
| `BODY_Super_Cowl` | `EXT_Dash_Absorber_L` | 11 | 301 | -0.5, 1.825, 1.139 |
| `BODY_Super_Cowl` | `EXT_Dash_Absorber_R` | 11 | 301 | 0.5, 1.825, 1.139 |
| `BODY_Header_Front_Gusset_L` | `BODY_Header_Front_Lower` | 10 | 61.6 | -0.71, 0.525, 1.665 |
| `BODY_Rear_Fascia_Bracket_L` | `BODY_Rear_Energy_Absorbers` | 10 | 74.9 | -0.655, -2.893, 0.585 |
| `BODY_Header_Front_Lower` | `BODY_Header_Front_Gusset_R` | 10 | 61.6 | 0.71, 0.525, 1.665 |
| `BODY_Rear_Energy_Absorbers` | `BODY_Rear_Fascia_Bracket_R` | 10 | 78.8 | 0.656, -2.895, 0.586 |
| `EXT_Door_FL_Hinges` | `EXT_Fender_Baffle_Front_L` | 9.1 | 118 | -0.905, 1.232, 0.628 |
| `EXT_Door_FR_Hinges` | `EXT_Fender_Baffle_Front_R` | 9.1 | 118 | 0.905, 1.232, 0.628 |
| `EXT_Door_R_Presenter_L` | `EXT_Door_Hinge_Stud_Plates_L` | 9 | 77.5 | -0.842, -0.842, 1.029 |
| `EXT_Door_Hinge_Stud_Plates_R` | `EXT_Door_R_Presenter_R` | 9 | 77.5 | 0.842, -0.842, 1.029 |
| `EXT_Front_Bumper` | `EXT_Grille_Foam_Seals` | 6.9 | 1061.9 | 0, 2.6, 0.575 |
| `EXT_Rocker_L` | `EXT_Rocker_Rear_Fairing_L` | 6.9 | 192 | -0.885, -1.127, 0.335 |
| `EXT_Rocker_R` | `EXT_Rocker_Rear_Fairing_R` | 6.9 | 192 | 0.885, -1.127, 0.335 |
| `EXT_Door_RL_Latch` | `BODY_CPillar_Inner_L` | 6.8 | 220.9 | -0.855, -0.879, 0.847 |
| `EXT_Door_R_Presenter_L` | `BODY_CPillar_Inner_L` | 6.8 | 101.9 | -0.851, -0.844, 1.046 |
| `BODY_Super_Cowl` | `EXT_Frunk_Underhood_Apron_Rear` | 6.8 | 1500.1 | 0, 1.953, 1.1 |
| `BODY_CPillar_Inner_R` | `EXT_Door_R_Presenter_R` | 6.8 | 101.9 | 0.851, -0.844, 1.046 |
| `BODY_CPillar_Inner_R` | `EXT_Door_RR_Latch` | 6.8 | 220.9 | 0.855, -0.879, 0.847 |
| `BODY_CPillar_Inner_L` | `EXT_Door_Hinge_Stud_Plates_L` | 6.7 | 448.5 | -0.85, -0.86, 0.835 |
| `BODY_CPillar_Inner_R` | `EXT_Door_Hinge_Stud_Plates_R` | 6.7 | 448.5 | 0.85, -0.86, 0.835 |
| `BODY_DoorRing_R` | `EXT_Trim_Cantrail_R` | 6.4 | 1387 | 0.761, -0.19, 1.7 |
| `EXT_Fender_Baffle_Front_L` | `EXT_Door_FL_CheckStrap` | 6.2 | 24.6 | -0.887, 1.261, 0.82 |
| `EXT_Door_FR_CheckStrap` | `EXT_Fender_Baffle_Front_R` | 6.2 | 24.6 | 0.887, 1.261, 0.82 |
| `EXT_Door_Primary_Seals_R` | `DOOR_FR_InnerStructure` | 5.4 | 1365.6 | 0.858, 0.634, 0.848 |
| `EXT_Frunk_Underhood_Apron_Rear` | `EXT_Washer_Hose` | 5 | 38.6 | 0.236, 1.984, 1.1 |
| `EXT_Underhood_Apron_R` | `EXT_Washer_Tank` | 4.5 | 68.6 | 0.569, 2.319, 0.985 |
| `EXT_Wiper_Blade` | `EXT_Wiper_Arm` | 4.3 | 379.1 | -0.11, 1.904, 1.328 |
| `EXT_Rocker_L` | `BODY_Sill_L` | 4 | 2175.1 | -0.887, 0.065, 0.351 |
| `BODY_Sill_Insert_L` | `BODY_XM_Bash_Plate_L` | 4 | 953.2 | -0.823, 0, 0.341 |
| `EXT_Door_FL_Latch` | `EXT_Door_FL_Striker` | 4 | 16.6 | -0.88, 0.091, 0.9 |
| `EXT_Door_RL_Latch` | `EXT_Door_RL_Striker` | 4 | 16.6 | -0.88, -0.906, 0.9 |
| `BODY_Sill_R` | `EXT_Rocker_R` | 4 | 2175.1 | 0.887, 0.065, 0.351 |
| `BODY_XM_Bash_Plate_R` | `BODY_Sill_Insert_R` | 4 | 953.2 | 0.823, 0, 0.341 |
| `EXT_Door_FR_Latch` | `EXT_Door_FR_Striker` | 4 | 16.6 | 0.88, 0.091, 0.9 |
| `EXT_Door_RR_Latch` | `EXT_Door_RR_Striker` | 4 | 16.6 | 0.88, -0.906, 0.9 |
| `EXT_Flare_RL` | `EXT_Rocker_Rear_Fairing_L` | 3.7 | 58.2 | -0.931, -1.18, 0.39 |
| `EXT_Door_Primary_Seals_L` | `EXT_Door_FL_Striker` | 3.7 | 16 | -0.881, 0.091, 0.9 |
| `EXT_Washer_Pump_Hoses` | `EXT_Underhood_Apron_R` | 3.7 | 62.9 | 0.546, 2.053, 0.985 |
| `EXT_Door_Primary_Seals_R` | `EXT_Door_FR_Striker` | 3.7 | 16.3 | 0.881, 0.091, 0.9 |
| `EXT_Mirror_L_Arm` | `EXT_Door_FL_Seals` | 3.6 | 88.6 | -0.905, 1.074, 1.229 |
| `EXT_Door_FR_Seals` | `EXT_Mirror_R_Arm` | 3.6 | 88.6 | 0.905, 1.074, 1.229 |
| `EXT_Door_FL_Seals` | `EXT_Door_FL_GlassFrame` | 3.3 | 23.6 | -0.898, 0.101, 1.296 |
| `EXT_Door_RL_Seals` | `EXT_Door_RL_GlassFrame` | 3.3 | 977 | -0.894, -0.419, 1.328 |
| `EXT_Door_FR_GlassFrame` | `EXT_Door_FR_Seals` | 3.3 | 23.6 | 0.898, 0.101, 1.296 |
| `EXT_Door_RR_GlassFrame` | `EXT_Door_RR_Seals` | 3.3 | 977 | 0.894, -0.419, 1.328 |
| `EXT_Door_Primary_Seals_R` | `BODY_CPillar_Inner_R` | 3.2 | 467.8 | 0.802, -0.851, 1.4 |

### Caja de carga, portón y persiana (45)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `EXT_Rear_Bumper` | `CARGO_Gear_Locker` | 15.8 | 860.4 | 0, -2.79, 0.708 |
| `BRK_Booster_Electromechanical` | `BRK_Master_Cylinder` | 11 | 113.1 | -0.37, 1.855, 0.95 |
| `CARGO_Tonneau_Cam_Block_L` | `CARGO_Tonneau_Slat_22` | 10.5 | 31.1 | -0.76, -2.793, 1.357 |
| `CARGO_Tonneau_Slat_22` | `CARGO_Tonneau_Cam_Block_R` | 10.5 | 31.1 | 0.76, -2.793, 1.357 |
| `CARGO_Bed_Front_Wall` | `LV_MV_Locking_Covers` | 10.4 | 107.3 | 0, -1.012, 1.039 |
| `EXT_Applique_Sail_L` | `BODY_Cabin_RearWall` | 10 | 101 | -0.85, -0.955, 1.329 |
| `BODY_Cabin_RearWall` | `EXT_Applique_Sail_R` | 10 | 101 | 0.85, -0.955, 1.329 |
| `BODY_Mast_L` | `EXT_Applique_Sail_L` | 9.6 | 202.4 | -0.854, -1.082, 1.519 |
| `BODY_Mast_R` | `EXT_Applique_Sail_R` | 9.6 | 202.4 | 0.854, -1.082, 1.519 |
| `CARGO_Tonneau_Cam_Block_L` | `CARGO_Tonneau_Slat_21` | 9.4 | 27.6 | -0.761, -2.767, 1.36 |
| `CARGO_Tonneau_Slat_21` | `CARGO_Tonneau_Cam_Block_R` | 9.4 | 27.6 | 0.761, -2.767, 1.36 |
| `CARGO_Tonneau_Hinge_Pivot_Applique_L` | `CARGO_Tonneau_Cam_Block_L` | 7 | 28.7 | -0.79, -1.037, 1.38 |
| `CARGO_Tonneau_Cam_Block_R` | `CARGO_Tonneau_Hinge_Pivot_Applique_R` | 7 | 28.7 | 0.79, -1.037, 1.38 |
| `CARGO_Bed_Side_Wall_Upper_R` | `BODY_Tailgate_Tower_R` | 7 | 99.5 | 0.835, -2.75, 1.22 |
| `BODY_Mast_L` | `BODY_Tailgate_Tower_L` | 5.9 | 75.1 | -0.842, -2.742, 1.232 |
| `BODY_Mast_R` | `BODY_Tailgate_Tower_R` | 5.9 | 75.1 | 0.842, -2.742, 1.232 |
| `BODY_Mast_L` | `EXT_Sail_Baffle_L` | 5.8 | 61.9 | -0.827, -1, 1.527 |
| `BODY_Mast_R` | `EXT_Sail_Baffle_R` | 5.8 | 61.9 | 0.827, -1, 1.527 |
| `BODY_Tailgate_Tower_L` | `EXT_Tailgate_Seal` | 5.7 | 42.3 | -0.84, -2.789, 0.74 |
| `EXT_Tailgate_Seal` | `BODY_Tailgate_Tower_R` | 5.7 | 42.3 | 0.84, -2.789, 0.74 |
| `BODY_Tailgate_Tower_L` | `CARGO_Bed_Side_Wall_Upper_L` | 5.6 | 97.4 | -0.835, -2.751, 1.22 |
| `LV_Harness_Tailgate` | `BODY_Tailgate_Tower_R` | 5.5 | 96.2 | 0.836, -2.752, 0.812 |
| `LV_Harness_Tailgate` | `LV_Harness_Bed_R` | 5.2 | 37.7 | 0.797, -2.6, 0.848 |
| `EXT_Tailgate_Hinges` | `EXT_Tailgate_Seal_Side_L` | 5 | 34.5 | -0.861, -2.8, 0.795 |
| `EXT_Tailgate_Hinges` | `EXT_Tailgate_Seal_Side_R` | 5 | 34.5 | 0.861, -2.8, 0.795 |
| `BODY_Sail_Panel_Bracket_L` | `CARGO_Tonneau_Cam_Block_L` | 5 | 56.1 | -0.782, -1.05, 1.382 |
| `EXT_Sail_Baffle_L` | `CARGO_Tonneau_Hinge_Pivot_Applique_L` | 5 | 52.4 | -0.812, -0.998, 1.4 |
| `CARGO_Bed_Front_Wall` | `BODY_Tonneau_Attachment_Bracket_L` | 5 | 89.4 | -0.72, -1.011, 1.28 |
| `CARGO_Bed_Front_Wall` | `BODY_Tonneau_Attachment_Bracket_R` | 5 | 89.4 | 0.72, -1.011, 1.28 |
| `CARGO_Tonneau_Cam_Block_R` | `BODY_Sail_Panel_Bracket_R` | 5 | 56.1 | 0.782, -1.05, 1.382 |
| `CARGO_Tonneau_Hinge_Pivot_Applique_R` | `EXT_Sail_Baffle_R` | 5 | 52.4 | 0.812, -0.998, 1.4 |
| `CARGO_Tonneau_Motor_R_Internals` | `CARGO_Tonneau_Water_Seal_Center_R` | 4.3 | 20.7 | 0.7, -1.157, 1.36 |
| `CARGO_Tiedowns` | `BODY_TieDown_Nut_Plate_L` | 4 | 49.3 | -0.714, -2.72, 0.868 |
| `CARGO_Tiedowns` | `BODY_TieDown_Nut_Plate_R` | 4 | 49.3 | 0.714, -2.72, 0.868 |
| `CARGO_Tonneau_Motor_L_Internals` | `CARGO_Tonneau_Water_Seal_Center_L` | 3.8 | 20.7 | -0.7, -1.157, 1.36 |
| `CARGO_Tonneau_Slat_15` | `CARGO_Tonneau_Chain_L` | 3.5 | 26.9 | -0.795, -2.224, 1.439 |
| `CARGO_Tonneau_Slat_15` | `CARGO_Tonneau_Chain_R` | 3.5 | 26.9 | 0.795, -2.224, 1.439 |
| `CARGO_Tonneau_Slat_13` | `CARGO_Tonneau_Chain_L` | 3.5 | 26.9 | -0.8, -2.053, 1.465 |
| `CARGO_Tonneau_Slat_13` | `CARGO_Tonneau_Chain_R` | 3.5 | 26.9 | 0.8, -2.053, 1.465 |
| `CARGO_Tonneau_Chain_L` | `CARGO_Tonneau_Slat_11` | 3.5 | 26.6 | -0.8, -1.882, 1.492 |
| `CARGO_Tonneau_Chain_L` | `CARGO_Tonneau_Slat_17` | 3.5 | 26.9 | -0.791, -2.395, 1.413 |
| `CARGO_Tonneau_Slat_11` | `CARGO_Tonneau_Chain_R` | 3.5 | 26.6 | 0.8, -1.882, 1.492 |
| `CARGO_Tonneau_Slat_17` | `CARGO_Tonneau_Chain_R` | 3.5 | 26.9 | 0.791, -2.395, 1.413 |
| `CARGO_Tonneau_Slat_22` | `CARGO_Tonneau_Closeout_Foam` | 3.2 | 1500.3 | 0, -2.84, 1.354 |
| `CARGO_Bed_Tub` | `WHL_RR_Tire` | 3.1 | 234 | 0.781, -1.814, 0.868 |

### Alta y baja tensión (batería, módulos y mazos) (27)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `LV_Harness_MV_Backbone` | `LV_Body_Controller_RH` | 16.7 | 114.9 | 0.528, 1.365, 0.741 |
| `BODY_IP_CrossCar_Beam` | `LV_Harness_IP_Main` | 15.2 | 1324 | 0, 1.041, 0.974 |
| `EXT_ChargePort_Inlet` | `EXT_ChargePort_ECU` | 15 | 84.9 | -0.971, -1.314, 0.776 |
| `HV_Charge_Port_Busbar` | `EXT_ChargePort_ECU` | 14.4 | 62.9 | -0.951, -1.314, 0.753 |
| `BAT_HV_Header` | `BAT_BMS_Controller` | 13.5 | 210.6 | -0.01, 1.191, 0.494 |
| `BAT_Internal_Beams` | `STR_Rear_Steer_Jumper_Harness` | 10.9 | 83.5 | 0.37, -1.173, 0.379 |
| `LV_Harness_MV_Backbone` | `LV_Body_Controller_LH` | 10.5 | 105.1 | -0.536, 1.315, 0.743 |
| `BODY_Ramp_Bracket_CPillar_L` | `LV_Harness_MV_Backbone` | 10.3 | 60.3 | -0.801, -0.9, 0.666 |
| `STR_Steering_Jumper_Harness` | `THM_Battery_Coolant_Hoses` | 10.1 | 41.1 | -0.352, 1.422, 0.548 |
| `BODY_CPillar_Lower_Nut_Plate_L` | `LV_Harness_MV_Backbone` | 8.1 | 82.1 | -0.791, -0.851, 0.518 |
| `CHS_Active_Grille_Shutter` | `LV_Ferrite_Core_Coax` | 7.8 | 7.1 | 0.02, 2.49, 0.63 |
| `LV_Harness_Rear_Subframe` | `STR_R_Motors_Internals` | 6.4 | 73.8 | 0.264, -1.577, 0.366 |
| `CHS_Cooling_Fan_Module` | `LV_Ferrite_Core_Coax` | 6.3 | 58.9 | 0.039, 2.385, 0.678 |
| `BODY_HV_Battery_Support_Bracket_L` | `BAT_Enclosure_Tray` | 6 | 2201.2 | -0.816, 0, 0.425 |
| `BAT_Enclosure_Tray` | `BODY_HV_Battery_Support_Bracket_R` | 6 | 2201.2 | 0.816, 0, 0.425 |
| `BODY_Casting_Rear_UnderBody_R` | `BODY_HV_Battery_Support_Bracket_R` | 5.8 | 149.2 | 0.832, -1.033, 0.418 |
| `BODY_Casting_Rear_UnderBody_L` | `BODY_HV_Battery_Support_Bracket_L` | 5.5 | 149.2 | -0.832, -1.033, 0.418 |
| `HV_Cables` | `THM_Battery_Coolant_Hoses` | 5.3 | 60.3 | -0.131, 1.597, 0.673 |
| `BAT_Thermal_Vent_FloodPorts` | `STR_Rear_Steer_Jumper_Harness` | 5.3 | 52.2 | 0.199, -1.409, 0.352 |
| `HV_AC_Junction_Box` | `HV_DPDT_Switch` | 5 | 94.3 | -0.2, -1.12, 0.67 |
| `HV_Cables` | `HV_Harness_FDU` | 4.7 | 442.5 | 0.081, 1.446, 0.568 |
| `LV_Harness_Fascia` | `THM_Coolant_Bottle` | 4.6 | 27.3 | 0.496, 2.109, 0.846 |
| `BAT_Coolant_Manifolds` | `BAT_Block_1_BMB` | 4.5 | 140.8 | -0.597, 1.114, 0.366 |
| `BAT_Enclosure_Lid` | `WHL_RR_Tire` | 4.3 | 22 | 0.775, -1.382, 0.447 |
| `BAT_Coolant_Manifolds` | `BAT_Block_3_BMB` | 4 | 54.6 | 0.27, 1.113, 0.367 |
| `BAT_Block_3_Coolers` | `STR_Rear_Steer_Jumper_Harness` | 3.9 | 28.3 | 0.348, -1.21, 0.366 |
| `BODY_Seat_Crossmember_Front` | `BAT_Lid_Seal` | 3.4 | 1640.1 | 0, 0.4, 0.458 |

### Unidades motrices (25)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `DU_F_Intermediate_Shaft` | `DU_F_Input_Gear` | 21.7 | 35.7 | 0.04, 1.994, 0.449 |
| `DU_R_Gearbox` | `DU_R_Gear_Train_L` | 15 | 96.2 | -0.166, -1.817, 0.437 |
| `DU_R_Gearbox` | `DU_R_Gear_Train_R` | 15 | 81.5 | 0.166, -1.809, 0.437 |
| `BODY_Dash_FUB_Gutter_Connector_R` | `THM_FDU_Coolant_Hoses` | 14.7 | 55.2 | 0.256, 1.799, 0.52 |
| `DU_F_Inverter_Power_Modules` | `DU_F_Inverter_DC_Capacitor` | 12 | 190.3 | 0.12, 1.892, 0.607 |
| `DU_R_Mounts` | `STR_R_Actuator` | 10.6 | 94 | 0.001, -1.682, 0.405 |
| `DU_F_Differential` | `BODY_Dash_FUB_Gutter_Connector_R` | 10 | 54.6 | 0.135, 1.786, 0.511 |
| `HV_Cables` | `THM_RDU_Coolant_Hoses` | 9 | 152.3 | 0.256, -1.72, 0.641 |
| `DU_F_Inverter_ColdPlate` | `DU_F_OilPump_Filter` | 9 | 25.1 | 0.05, 1.837, 0.595 |
| `HV_Cables` | `HV_Harness_RDU_R` | 8.7 | 181.6 | 0.232, -1.672, 0.655 |
| `HV_Cables` | `HV_Harness_RDU_L` | 8.3 | 199.1 | -0.176, -1.568, 0.648 |
| `DU_F_Intermediate_Shaft` | `DU_F_Differential` | 8 | 61.2 | 0.027, 1.856, 0.426 |
| `CHS_AirSuspension_Lines` | `DU_R_Inverter_R` | 7.7 | 175.2 | 0.253, -2.199, 0.608 |
| `DU_F_Mounts` | `DU_F_Stator_Core` | 7.1 | 47.1 | -0.229, 2.037, 0.357 |
| `STR_R_Actuator` | `DU_R_OilPump_Filter` | 5.8 | 26.8 | -0.1, -1.683, 0.367 |
| `EXT_Wiper_Motor_Internals` | `EXT_Washer_Hose` | 5.2 | 41.6 | 0.126, 1.947, 1.236 |
| `DU_F_Inverter_ColdPlate` | `DU_F_Inverter_DC_Capacitor` | 5.1 | 263.5 | 0.16, 1.878, 0.604 |
| `DU_R_NVH_Cover_L` | `DU_R_Inverter_L` | 5 | 66.9 | -0.2, -2.156, 0.704 |
| `DU_F_Motor_Housing` | `DU_F_Inverter` | 5 | 76.1 | -0.012, 2.006, 0.595 |
| `DU_F_NVH_Cover` | `DU_F_Inverter` | 5 | 123.7 | -0.023, 2.017, 0.598 |
| `DU_R_NVH_Cover_R` | `DU_R_Inverter_R` | 5 | 66.9 | 0.2, -2.156, 0.704 |
| `DU_F_Gearbox` | `BODY_Dash_FUB_Gutter_Connector_R` | 4.5 | 106.9 | 0.173, 1.785, 0.52 |
| `DU_Halfshaft_FR_Joints_Boots` | `SUS_FR_Hub_Bearing` | 4 | 21.4 | 0.836, 1.817, 0.462 |
| `DU_Halfshaft_RR_Joints_Boots` | `SUS_RR_Hub_Bearing` | 4 | 21.4 | 0.836, -1.817, 0.462 |
| `DU_F_OilPump_Filter` | `DU_F_Intermediate_Shaft` | 3.2 | 31.2 | 0.038, 1.888, 0.327 |

### Gestión térmica (20)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `THM_AC_Compressor` | `THM_AC_Compressor_Internals` | 32.5 | 165.1 | -0.234, 1.82, 0.862 |
| `THM_AC_Compressor` | `THM_AC_Lines` | 19.4 | 133.8 | -0.102, 1.836, 0.786 |
| `BODY_Dash_FUB_Gutter_Connector_R` | `THM_Chiller_Battery_Hoses` | 18.9 | 124.2 | 0.385, 1.785, 0.52 |
| `THM_AC_Lines` | `THM_Supermanifold` | 18.6 | 195.5 | 0.035, 1.813, 0.807 |
| `THM_Radiator_Hoses` | `THM_Supermanifold` | 13.9 | 105.9 | 0.295, 1.957, 0.756 |
| `BODY_Casting_Front_UnderBody` | `CHS_Radiator` | 12.5 | 910.1 | 0, 2.425, 0.54 |
| `THM_Powertrain_Hose_Bundle` | `CHS_Air_Line_Bundle_L` | 12.3 | 2282.3 | -0.864, 0.023, 0.287 |
| `THM_Powertrain_Hose_Bundle` | `CHS_AirSuspension_Lines` | 9.7 | 2502 | -0.828, -0.066, 0.285 |
| `THM_Radiator_Hoses` | `BRK_Pipes` | 9.5 | 33.9 | 0.221, 2.083, 0.702 |
| `BODY_Sill_L` | `THM_Powertrain_Hose_Bundle` | 8.1 | 2168.4 | -0.854, 0.067, 0.302 |
| `STR_F_Motors_Internals` | `THM_Chiller_Battery_Hoses` | 7.9 | 92.3 | 0.254, 1.574, 0.462 |
| `THM_Pack_Pressurization_Line` | `CHS_Air_Compressor_Exhaust` | 7.5 | 49 | -0.3, -2.377, 0.452 |
| `THM_Powertrain_Hose_Bundle` | `THM_Battery_Coolant_Hoses` | 6.2 | 155.7 | 0.031, 1.699, 0.733 |
| `THM_Chiller_Battery_Hoses` | `THM_Chiller` | 6.1 | 54.7 | 0.412, 1.875, 0.69 |
| `THM_Expansion_Valves` | `THM_Octovalve` | 5.9 | 26.8 | 0.272, 1.837, 1.027 |
| `BODY_Front_Body_Bridge_Reinforcement` | `THM_Supermanifold_Controller_Sensors` | 5 | 67.2 | 0.325, 1.74, 1.045 |
| `THM_Supermanifold` | `THM_Penta_HVAC_Line` | 4.8 | 31.5 | 0.265, 1.732, 0.862 |
| `EXT_Rocker_Rear_Fairing_L` | `THM_Powertrain_Hose_Bundle` | 4.5 | 112.7 | -0.854, -1.143, 0.283 |
| `BODY_Casting_Front_UnderBody` | `THM_Battery_Coolant_Hoses` | 3.8 | 190.4 | -0.291, 1.47, 0.579 |
| `STR_F_Actuator_ECU_PCB` | `THM_Chiller_Battery_Hoses` | 3.5 | 38 | 0.229, 1.515, 0.451 |

### Asientos y cinturones (8)

| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |
|---|---|---|---|---|
| `INT_Trim_CPillar_Lower_L` | `INT_Seatbelt_RL` | 12 | 125 | -0.72, -0.848, 0.599 |
| `INT_Seatbelt_RR` | `INT_Trim_CPillar_Lower_R` | 12 | 125 | 0.72, -0.848, 0.599 |
| `INT_Seatbelt_Buckles` | `INT_Console_Armrest` | 9.2 | 253.6 | 0, 0.306, 0.827 |
| `INT_SeatF_R_Tracks` | `LV_Harness_Seat_R` | 6.2 | 48.7 | 0.313, 0.77, 0.528 |
| `INT_SeatF_Frame_L` | `INT_Console_Side_Panel_L` | 5.1 | 84.9 | -0.144, 0.235, 0.72 |
| `INT_Console_Side_Panel_R` | `INT_SeatF_Frame_R` | 5.1 | 84.9 | 0.144, 0.235, 0.72 |
| `INT_Seatbelt_Buckles` | `INT_Console_Side_Panel_L` | 3.1 | 191.8 | -0.132, 0.328, 0.691 |
| `INT_Seatbelt_Buckles` | `INT_Console_Side_Panel_R` | 3.1 | 191.8 | 0.132, 0.328, 0.691 |

## Penetraciones intencionadas reconocidas

| Motivo | Parejas |
|---|---|
| tornillo, remache o grapa que entra en la pieza que fija | 158 |
| celdas embebidas en la espuma estructural y los refrigeradores | 12 |
| mazo que atraviesa el mamparo o el suelo por su pasacables | 11 |
| eje o barra que atraviesa la pared de su carcasa (por un retén o un pasamuros) | 10 |
| vástago de la válvula por su taladro de la llanta y del tapacubos | 8 |
| espárragos y centrador del buje por los taladros de la campana del disco y de la llanta | 8 |
| varillas del reposacabezas en sus guías del respaldo | 6 |
| casquillos de los soportes encajados en los ojales de la carcasa | 5 |
| portavasos encastrado en la consola | 3 |
| eje del rotor estriado en el piñón de entrada | 2 |
| extremo de la viga del salpicadero alojado en su soporte | 2 |
| barras y cables que entran en el cabezal HV por sus pasamuros | 2 |
| bomba de aceite y filtro roscados en la carcasa de la reductora | 2 |
| colectores de refrigerante por los pasos de las vigas interiores | 1 |
