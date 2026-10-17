"""Versión 4 («coche completo»): interior funcional de los conjuntos, tornillería y piezas que faltaban.

Orquesta los módulos `build_v4_*.py`. Se ejecuta desde `build_all.run(parts=(..., "v3", "v4", ...))`,
después de la versión 3 y antes de la vista explosionada; solo añade objetos a las colecciones de sistema
existentes y ajusta la explosión de algunas carcasas para que se aparten más que su contenido.
"""

import importlib
import sys

MODULES = ["ct_v4", "build_v4_motriz", "build_v4_chasis", "build_v4_energia", "build_v4_habitaculo",
           "build_v4_carroceria", "build_v4_tornilleria"]


def _available():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return [m for m in MODULES if os.path.exists(os.path.join(here, m + ".py"))]


# Interiores de la v4 que deben quedar enteros dentro de su carcasa (interior → carcasa). Los ejes que atraviesan
# una pared por diseño (ejes de rotor y de salida, barras de fase, cables) son piezas aparte y no se ajustan.
FIT = [
    *[(f"DU_F_Inverter_{n}", "DU_F_Inverter") for n in ("ColdPlate", "Power_Modules", "DC_Capacitor",
                                                         "Gate_Driver_PCB", "Control_PCB", "Current_Sensors")],
    *[(f"DU_F_{n}", "DU_F_Motor_Housing") for n in ("Stator_Core", "Stator_Hairpins", "Rotor", "Rotor_Magnets",
                                                     "Rotor_Bearings", "Resolver")],
    *[(f"DU_F_{n}", "DU_F_Gearbox") for n in ("Input_Gear", "Intermediate_Shaft", "Park_Lock", "Differential")],
    *[(f"DU_R_{n}_{s}", f"DU_R_Motor_{s}") for n in ("Stator_Core", "Stator_Winding", "Rotor") for s in "LR"],
    *[(f"DU_R_Gear_Train_{s}", "DU_R_Gearbox") for s in "LR"],
    *[(f"DU_R_Inverter_Internals_{s}", f"DU_R_Inverter_{s}") for s in "LR"],
    ("HV_PCS_Internals", "HV_Power_Conversion_System"), ("HV_ACJB_Internals", "HV_AC_Junction_Box"),
    ("THM_AC_Compressor_Internals", "THM_AC_Compressor"), ("THM_Coolant_Pump_Internals", "THM_Coolant_Pump"),
    ("CHS_Air_Compressor_Internals", "CHS_AirSuspension_Compressor"),
    ("BRK_Booster_Internals", "BRK_Booster_Electromechanical"), ("BRK_HCU_Internals", "BRK_Hydraulic_Control_Unit"),
    ("INT_Car_Computer_Internals", "INT_Car_Computer"), ("INT_HVAC_Internals", "INT_HVAC_Module"),
    ("INT_Display_Center_Internals", "INT_Display_Center_Housing"),
    ("INT_Display_Rear_Internals", "INT_Display_Rear_Housing"),
    ("LV_Battery_48V_Internals", "LV_Battery_48V"), ("BAT_BMS_Controller", "BAT_HV_Header"),
    ("EXT_Wiper_Motor_Internals", "EXT_Wiper_Motor"),
    *[(f"SUS_{c}_Damper_Internals", f"SUS_{c}_Damper") for c in ("FL", "FR", "RL", "RR")],
    *[(f"STR_{a}_{n}", f"STR_{a}_Actuator") for a in "FR" for n in ("Motors_Internals", "Drive_Belts",
                                                                     "Actuator_ECU_PCB")],
    *[(f"CARGO_Tonneau_Motor_{s}_Internals", f"CARGO_Tonneau_Motor_{s}") for s in "LR"],
    *[(f"LGT_Headlamp_{s}_Internals", f"LGT_Headlamp_{s}") for s in "LR"],
    *[(f"LV_Body_Controller_{n}_PCB", f"LV_Body_Controller_{n}") for n in ("LH", "RH", "Rear")],
    ("LV_Trailer_ECU_PCB", "LV_Trailer_ECU"),
]


def fit_internals():
    """Pasada final: cada interior se ajusta a su carcasa (desplazamiento y escala por ejes) o, si no cabe sin
    deformarse demasiado, se recorta con el volumen interior de la carcasa."""
    import ct_v4 as V4
    import build_v4_energia as EN
    pairs = list(FIT) + [(f"{n}_PCB", n) for n in EN.BOARDS]
    out = {}
    for inner, housing in pairs:
        k = V4.fit_inside(inner, housing)
        if k == 0.0:
            # no cabe sin deformarse demasiado: se recorta con el volumen interior de la carcasa
            n = V4.clip_inside(inner, housing)
            k = "recortado" if n else "sin ajustar"
        if k is not None and k != 1.0:
            out[inner] = k
    # espumas dentro de sus tapizados (copias encogidas que asomaban en las zonas cóncavas)
    for foam, cover in KEEP_INSIDE:
        n = V4.keep_inside(foam, cover)
        if n:
            out[foam] = f"{n} vértices dentro"
    global LAST_FIT
    LAST_FIT = out
    return out


KEEP_INSIDE = [(f"INT_Seat{k}_{n}_Foam", f"INT_Seat{k}_{n}") for k in ("F_R", "F_L", "R_L", "R_C", "R_R")
               for n in ("Cushion", "Back")] + [("INT_SteeringWheel_Armature", "INT_SteeringWheel_Rim")]


LAST_FIT = {}


def build_all(M, only=None):
    import bpy
    out = {}
    # las piezas de la v4 se describen a menudo en las coordenadas de objetos ya creados: hay que
    # actualizar las matrices de mundo antes de leerlas
    bpy.context.view_layer.update()
    for name in _available():
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    for name in _available():
        if name == "ct_v4" or (only and name not in only):
            continue
        mod = importlib.import_module(name)
        objs = mod.build(M)
        out[name] = len(objs)
    if not only:
        out["ajustados"] = len(fit_internals())
    return out
