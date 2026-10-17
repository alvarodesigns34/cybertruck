"""Versión 4 · interior funcional del chasis: frenos, amortiguadores, dirección por cable y aire comprimido.

  Pinzas: pistones (4 delante, 1 detrás [V]), juntas de sección cuadrada, guardapolvos, pasadores y muelle
    antirruido de las pastillas, láminas antirruido; detrás, husillo y tuerca del freno de estacionamiento
    eléctrico dentro del pistón.
  Amortiguadores: vástago interior, pistón con láminas de válvula, guía del vástago con retén y pistón
    flotante de la cámara de gas (monotubo, [R]).
  Actuadores de dirección delantero y trasero ([V] dos motores redundantes): cremallera, tuerca de bolas
    con recirculación, poleas y correas dentadas, estátores y rotores de los dos motores, placa de control.
  Servofreno electromecánico: motor sin escobillas, husillo de bolas y varilla de empuje; bomba de freno
    tándem con dos pistones y muelles (el depósito remoto ya existía).
  HCU (ABS/ESC): bloque de válvulas con 12 electroválvulas, bomba de pistones con su motor y placa de control.
  Compresor de la suspensión: motor, cigüeñal, biela, pistón y cartucho secador.

Fidelidad: piezas necesarias para el funcionamiento; número de pistones y fijaciones [V] cuando constan en el
manual de servicio, forma y dimensiones interiores «Aproximado».
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v4 as V4
import build_mechanics as BM
from ct_v4 import (gear, ring_gear, spline, sphere, bearing, taper, tube, screw, pcb, stator, winding, coil,
                   hose_clamp, box, cyl, ring, disc, hull, beam, bolt, nut, torx)

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
WZ = S.WHEEL_CENTER_Z
NOTE = ("Pieza interior necesaria para el funcionamiento; forma y dimensiones reconstruidas (no hay planos "
        "publicados)")


def wc(r, t, a):
    """Coordenadas locales de rueda/pinza (eje = X local), como `build_wheels.cyl`."""
    return (a, r * math.cos(t), r * math.sin(t))


def _small_motor(c, axis, r_can, length, m_steel=0, m_cu=1, m_shaft=2, slots=12):
    """Interior de un motor eléctrico pequeño (estátor ranurado, devanado, rotor, eje y rodamientos)."""
    c = Vector(c)
    w = Vector(axis).normalized()
    rs = r_can * 0.86
    return [
        stator(tuple(c), tuple(w), rs * 0.55, rs, length * 0.55, slots, rs * 0.18, m_steel),
        winding(tuple(c), tuple(w), rs * 0.58, rs * 0.80, length * 0.55, length * 0.10, m_cu, m_cu, 12),
        cyl(tuple(c - w * length * 0.28), tuple(c + w * length * 0.28), rs * 0.52, seg=24, m=m_steel),
        cyl(tuple(c - w * length * 0.48), tuple(c + w * length * 0.52), rs * 0.16, seg=12, m=m_shaft),
        bearing(tuple(c - w * length * 0.40), tuple(w), rs * 0.16, rs * 0.38, length * 0.08, 7, m=m_shaft),
        bearing(tuple(c + w * length * 0.40), tuple(w), rs * 0.16, rs * 0.38, length * 0.08, 7, m=m_shaft),
    ]


# ---------------------------------------------------------------------------
# Pinzas de freno
# ---------------------------------------------------------------------------
def calipers(M):
    out = []
    for axle in ("F", "R"):
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{axle}{sd}"
            fr = V4.obj_frame(f"BRK_{tag}_Caliper")
            if fr is None:
                continue
            whl = "FRONT_WHEELS_AND_BRAKES" if axle == "F" else "REAR_WHEELS_AND_BRAKES"
            es = f"{'delantera' if axle == 'F' else 'trasera'} {'derecha' if s > 0 else 'izquierda'}"
            cdir = (s * 0.4, -0.6 if axle == "F" else 0.6, 0.6)
            if axle == "F":
                ro, th = S.FRONT_ROTOR_D / 2, S.FRONT_ROTOR_T
                gap = th / 2 + 0.012
                span = 0.66
                face = th / 2 + 0.0005 + 0.0095 + 0.005 + 0.0008
                shp = []
                for sg in (1, -1):
                    for k in (-1, 1):
                        t = k * span * 0.24
                        c = wc(ro - 0.030, t, sg * face)
                        shp.append(taper(c, (sg, 0, 0), [(0.0, 0.0), (0.0205, 0.0), (0.0205, 0.024), (0.0165, 0.026),
                                                          (0.0165, 0.006), (0.0, 0.006)], 28, 0))
                        shp.append(ring(wc(ro - 0.030, t, sg * (face + 0.003)), X, 0.0205, 0.0255, 0.004, 24, 2))
                        shp.append(ring(wc(ro - 0.030, t, sg * (face + 0.014)), X, 0.0207, 0.0232, 0.003, 24, 2))
                # pasadores de las pastillas y muelle antirruido en cruz
                for t in (-0.06, 0.06):
                    shp.append(cyl(wc(ro + 0.007, t, -gap - 0.040), wc(ro + 0.007, t, gap + 0.040), 0.0028, seg=10, m=1))
                    shp.append(disc(wc(ro + 0.007, t, gap + 0.041), X, 0.0045, 0.003, 10, 1))
                shp.append(beam(wc(ro + 0.0105, -0.10, 0.0), wc(ro + 0.0105, 0.10, 0.0), 0.006, 0.0012, up=(0, 1, 0), r=0.0, m=1))
                shp.append(beam(wc(ro + 0.0105, 0.0, -0.035), wc(ro + 0.0105, 0.0, 0.035), 0.010, 0.0012, up=(0, 1, 0), r=0.0, m=1))
                lbl = f"Interior de la pinza {es}: 4 pistones con juntas y guardapolvos, pasadores y muelle antirruido"
            else:
                ro, th = S.REAR_ROTOR_D / 2, S.REAR_ROTOR_T
                gap = th / 2 + 0.012
                face = th / 2 + 0.0005 + 0.011 * 0.95 + 0.005 + 0.0008
                c = wc(ro - 0.026, 0.0, -face)
                shp = [taper(c, (-1, 0, 0), [(0.0, 0.0), (0.027, 0.0), (0.027, 0.034), (0.022, 0.036),
                                             (0.022, 0.006), (0.0, 0.006)], 32, 0),
                       ring(wc(ro - 0.026, 0.0, -face - 0.003), X, 0.027, 0.032, 0.004, 28, 2),
                       ring(wc(ro - 0.026, 0.0, -face - 0.018), X, 0.0272, 0.030, 0.003, 28, 2),
                       # husillo y tuerca del freno de estacionamiento (dentro del pistón)
                       cyl(wc(ro - 0.026, 0.0, -face - 0.008), wc(ro - 0.026, 0.0, -face - 0.075), 0.0065, seg=12, m=1),
                       gear(wc(ro - 0.026, 0.0, -face - 0.014), X, 0.012, 0.0145, 0.016, 12, 0.0066, 0.0, 1),
                       # clips de apoyo de las pastillas sobre el soporte
                       box(wc(ro - 0.030, -0.27, 0.0), (0.050, 0.004, 0.014), 0.0005, 1),
                       box(wc(ro - 0.030, 0.27, 0.0), (0.050, 0.004, 0.014), 0.0005, 1)]
                lbl = (f"Interior de la pinza {es}: pistón Ø54 mm con junta y guardapolvos, husillo y tuerca del "
                       "freno de estacionamiento eléctrico, clips de apoyo")
            out += V4.part(M, f"BRK_{tag}_Caliper_Internals", whl, ["chrome", "steel_bare", "rubber_seal"], shp, lbl,
                           frame=fr, parent=f"BRAKE_{tag}", edir=cdir, dist=0.34, stage=6, group="Frenos", fid="A",
                           note=NOTE)
            # láminas antirruido (shims) y avisador de desgaste sobre las pastillas
            pfr = V4.obj_frame(f"BRK_{tag}_Pads")
            span = 0.56 if axle == "F" else 0.42
            fr_t = 0.010 if axle == "F" else 0.011
            th = S.FRONT_ROTOR_T if axle == "F" else S.REAR_ROTOR_T
            ro = (S.FRONT_ROTOR_D if axle == "F" else S.REAR_ROTOR_D) / 2
            shp = []
            for sg in (1, -1):
                a = sg * (th / 2 + 0.0005 + fr_t * 0.95 + 0.0055)
                for k in range(9):
                    t0 = -span / 2 + span * k / 9
                    t1 = -span / 2 + span * (k + 1) / 9
                    shp.append(hull([wc(ro - 0.056, t0, a), wc(ro - 0.004, t0, a), wc(ro - 0.056, t1, a),
                                     wc(ro - 0.004, t1, a), wc(ro - 0.056, t0, a + sg * 0.0008),
                                     wc(ro - 0.004, t0, a + sg * 0.0008), wc(ro - 0.056, t1, a + sg * 0.0008),
                                     wc(ro - 0.004, t1, a + sg * 0.0008)], 0))
            shp.append(box(wc(ro - 0.002, span / 2 - 0.02, th / 2 + 0.008), (0.010, 0.004, 0.012), 0.0005, 1))
            out += V4.part(M, f"BRK_{tag}_Pad_Shims", whl, ["steel_bare", "zinc"], shp,
                           f"Láminas antirruido de las pastillas {es} y avisador acústico de desgaste",
                           frame=pfr, parent=f"BRAKE_{tag}", edir=cdir, dist=0.42, stage=6, group="Frenos", fid="A",
                           note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Amortiguadores
# ---------------------------------------------------------------------------
def dampers(M):
    out = []
    for axle in ("F", "R"):
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{axle}{sd}"
            hp = BM.hardpoints(axle, s)
            bot, top = hp["spr_bot"], hp["spr_top"]
            ax = (top - bot).normalized()
            ln = (top - bot).length
            sysn = "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION"
            p = lambda f: tuple(bot + ax * ln * f)
            shp = [
                cyl(p(0.20), p(0.555), 0.011, seg=16, m=0),
                disc(p(0.20), tuple(ax), 0.0285, 0.014, 32, 1),
                [disc(tuple(bot + ax * (ln * 0.20 + sg * (0.0085 + 0.0006 * i))), tuple(ax), 0.024 - 0.0025 * i,
                      0.0005, 24, 2) for sg in (-1, 1) for i in range(4)],
                nut(tuple(bot + ax * (ln * 0.20 - 0.012)), tuple(-ax), 0.010, 2, 0.0),
                ring(p(0.52), tuple(ax), 0.011, 0.0285, 0.022, 28, 1),
                ring(p(0.535), tuple(ax), 0.011, 0.016, 0.006, 20, 3),
                disc(p(0.08), tuple(ax), 0.0285, 0.016, 32, 1),
                ring(p(0.08), tuple(ax), 0.0275, 0.0290, 0.004, 28, 3),
            ]
            out += V4.part(M, f"SUS_{tag}_Damper_Internals", sysn, ["chrome", "alu_machined", "spring_steel",
                                                                    "rubber_seal"], shp,
                           f"Interior del amortiguador monotubo {tag}: vástago, pistón con láminas de válvula, guía "
                           "con retén y pistón flotante de la cámara de gas",
                           parent=f"SUS_{tag}_AirSpring", edir=tuple(ax), dist=0.42, stage=6, group="Suspensión",
                           fid="A", note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Actuadores de dirección (steer-by-wire)
# ---------------------------------------------------------------------------
def steering(M):
    out = []
    for axle in ("F", "R"):
        y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
        f = 1 if axle == "F" else -1
        yr, zr = y - f * 0.17, 0.425
        half = 0.27 if axle == "F" else 0.22
        V4.set_explode(f"STR_{axle}_Actuator", (0, -f, -0.5), 1.05, 4)
        es = "delantero" if axle == "F" else "trasero"
        rack = [
            cyl((-half + 0.005, yr, zr), (half - 0.005, yr, zr), 0.0125, seg=20, m=0),
            # dentado helicoidal de la tuerca de bolas (husillo) en el tramo central
            gear((0.06, yr, zr), X, 0.0118, 0.0135, 0.11, 10, 0.0, 55.0, 0, 10),
            # tuerca de bolas con tubo de recirculación y polea conducida
            ring((0.06, yr, zr), X, 0.0140, 0.026, 0.055, 32, 1),
            [sphere((0.06 + 0.012 * k, yr + 0.0195 * math.cos(1.1 * k), zr + 0.0195 * math.sin(1.1 * k)), 0.0035, 8, 5, 2)
             for k in range(-2, 3)],
            tube([(0.035, yr, zr + 0.027), (0.06, yr, zr + 0.034), (0.085, yr, zr + 0.027)], 0.0035, 8, 3, 1),
            # polea conducida doble (una pista por motor)
            gear((0.1105, yr, zr), X, 0.038, 0.040, 0.044, 60, 0.026, 0.0, 1),
            bearing((0.143, yr, zr), X, 0.026, 0.040, 0.014, 12, m=2),
            [disc((sg * (half - 0.004), yr, zr), X, 0.020, 0.008, 20, 3) for sg in (-1, 1)],
        ]
        motors = []
        belts = []
        for k, dz in enumerate((0.055, -0.035)):
            xb = 0.100 + 0.021 * k          # cada motor arrastra su propia pista de la polea doble
            cm = (0.235, yr - f * 0.075, zr + dz)
            motors += _small_motor(cm, X, 0.042, 0.14, 0, 1, 2, 12)
            motors.append(cyl((0.165, yr - f * 0.075, zr + dz), (0.090, yr - f * 0.075, zr + dz), 0.0065, seg=12, m=2))
            motors.append(gear((xb, yr - f * 0.075, zr + dz), X, 0.0120, 0.0135, 0.018, 18, 0.0066, 0.0, 2))
            # radio medio de la correa = punta del dentado + holgura + medio espesor (no toca los dientes)
            belts.append(V4.belt((xb, yr, zr), 0.0425, (xb, yr - f * 0.075, zr + dz), 0.0160, X, 0.016))
        out += V4.part(M, f"STR_{axle}_Rack_BallNut", "STEERING", ["gear_steel", "steel_bare", "bearing_steel",
                                                                     "rubber_seal"], rack,
                       f"Cremallera, tuerca de bolas con recirculación y polea del actuador {es}",
                       edir=(0, -f, -0.5), dist=0.55, stage=6, group="Dirección", fid="A", note=NOTE)
        out += V4.part(M, f"STR_{axle}_Motors_Internals", "STEERING", ["elec_steel", "copper_enamel", "gear_steel"],
                       motors, f"Estátores, rotores y piñones de los dos motores redundantes del actuador {es}",
                       edir=(0.4, -f, -0.3), dist=0.70, stage=6, group="Dirección", fid="A", note=NOTE)
        out += V4.part(M, f"STR_{axle}_Drive_Belts", "STEERING", ["bushing"], belts,
                       f"Correas dentadas de los dos motores a la tuerca de bolas (actuador {es})",
                       edir=(0.2, -f, -0.4), dist=0.62, stage=6, group="Dirección", fid="A", note=NOTE)
        out += V4.part(M, f"STR_{axle}_Actuator_ECU_PCB", "STEERING", ["pcb_green", "plastic_black", "capacitor",
                                                                         "connector_grey", "solder_tin"], [
            pcb((0.20, yr - f * 0.128, zr + 0.01), (0.20, 0.115, 0.0016), (0, -f, 0), Z, 55, 31 + f),
        ], f"Placa de control redundante del actuador {es} (dos canales, sensores de posición y par)",
            edir=(0, -f, -0.2), dist=0.80, stage=6, group="Dirección", fid="A", note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Servofreno electromecánico y bomba de freno
# ---------------------------------------------------------------------------
def brake_actuation(M):
    out = []
    c = Vector((-0.37, 1.66, 0.95))      # mismo origen que el servofreno (build_mechanics)
    V4.set_explode("BRK_Booster_Electromechanical", (-0.5, 0.6, 0.5), 0.85, 4)
    out += V4.part(M, "BRK_Booster_Internals", "UNDERBODY", ["elec_steel", "copper_enamel", "gear_steel", "bearing_steel",
                                                             "steel_black"], [
        _small_motor(tuple(c + Vector((0.13, 0.07, -0.02))), X, 0.040, 0.10, 0, 1, 2, 12),
        gear(tuple(c + Vector((0.035, 0.07, -0.02))), X, 0.010, 0.012, 0.016, 14, 0.004, 0.0, 2),
        gear(tuple(c + Vector((0.0, 0.07, 0.0))), Y, 0.050, 0.054, 0.016, 56, 0.012, 0.0, 2),
        # husillo de bolas y varilla de empuje
        cyl(tuple(c + Vector((0, -0.02, 0))), tuple(c + Vector((0, 0.15, 0))), 0.010, seg=16, m=2),
        ring(tuple(c + Vector((0, 0.10, 0))), Y, 0.011, 0.022, 0.035, 24, 3),
        bearing(tuple(c + Vector((0, 0.045, 0))), Y, 0.012, 0.030, 0.012, 9, m=3),
        coil(tuple(c + Vector((0, 0.11, 0))), Y, 0.030, 0.003, 5, 0.055, 8, 4),
    ], "Interior del servofreno electromecánico: motor sin escobillas, engranajes, husillo de bolas, muelle de "
       "retorno y varilla de empuje del pedal", edir=(-0.5, 0.6, 0.5), dist=0.55, stage=6, group="Frenos",
        fid="A", note=NOTE)
    m0 = c + Vector((0, 0.195, 0))
    out += V4.part(M, "BRK_Master_Cylinder", "UNDERBODY", ["alu_machined", "zinc", "plastic_black"], [
        disc(tuple(m0), Y, 0.040, 0.010, 28, 0),
        cyl(tuple(m0), tuple(m0 + Vector((0, 0.12, 0))), 0.026, seg=24, m=0),
        [cyl(tuple(m0 + Vector((0, 0.03 + 0.05 * k, 0.020))), tuple(m0 + Vector((0, 0.03 + 0.05 * k, 0.040))), 0.009,
             seg=12, m=2) for k in range(2)],
        [cyl(tuple(m0 + Vector((0.020, 0.04 + 0.05 * k, 0))), tuple(m0 + Vector((0.038, 0.04 + 0.05 * k, 0))), 0.007,
             seg=6, m=1) for k in range(2)],
        [nut(tuple(m0 + Vector((sx * 0.032, -0.011, 0))), (0, 1, 0), 0.010, 1, 0.0) for sx in (-1, 1)],
    ], "Bomba de freno tándem (2 circuitos, 2 tuercas al servofreno, conexiones al depósito y a la HCU)",
        edir=(-0.3, 1, 0.4), dist=0.70, stage=4, group="Frenos", fid="R",
        note="La bomba de freno es necesaria con servofreno electromecánico; forma reconstruida")
    out += V4.part(M, "BRK_Master_Cylinder_Internals", "UNDERBODY", ["chrome", "spring_steel", "rubber_seal"], [
        [cyl(tuple(m0 + Vector((0, 0.010 + 0.05 * k, 0))), tuple(m0 + Vector((0, 0.040 + 0.05 * k, 0))), 0.0115,
             seg=20, m=0) for k in range(2)],
        [ring(tuple(m0 + Vector((0, 0.012 + 0.05 * k + 0.026 * j, 0))), Y, 0.0105, 0.0122, 0.003, 20, 2)
         for k in range(2) for j in range(2)],
        [coil(tuple(m0 + Vector((0, 0.040 + 0.05 * k, 0))), Y, 0.007, 0.0016, 5, 0.020 if k == 0 else 0.03, 6, 1)
         for k in range(2)],
    ], "Pistones primario y secundario de la bomba de freno con copelas y muelles",
        edir=(-0.3, 1, 0.4), dist=1.00, stage=6, group="Frenos", fid="A", note=NOTE)
    # pedal → varilla de empuje
    out += V4.part(M, "BRK_Pedal_Pushrod", "INTERIOR_CONTROLS", ["zinc", "rubber_seal"], [
        cyl((-0.40, 1.42, 0.83), tuple(c + Vector((0, -0.12, 0))), 0.0055, seg=10, m=0),
        V4.boot((-0.40, 1.47, 0.86), (-0.40, 1.53, 0.89), 0.018, 0.010, 4, 14, 1),
    ], "Varilla de empuje del pedal de freno con fuelle del mamparo",
        edir=(0, -1, -0.2), dist=0.40, stage=6, group="Frenos", fid="A", note=NOTE)

    # HCU (ABS/ESC)
    h = Vector((0.32, 2.125, 0.66))      # mismo origen que la HCU (build_mechanics)
    V4.set_explode("BRK_Hydraulic_Control_Unit", (0.5, 0.5, 0.6), 0.85, 4)
    out += V4.part(M, "BRK_HCU_Internals", "UNDERBODY", ["alu_machined", "copper_enamel", "elec_steel", "pcb_green",
                                                         "plastic_black", "capacitor", "connector_grey", "solder_tin"], [
        [cyl(tuple(h + Vector((-0.045 + 0.03 * (k % 4), 0.045, -0.035 + 0.035 * (k // 4)))),
             tuple(h + Vector((-0.045 + 0.03 * (k % 4), 0.062, -0.035 + 0.035 * (k // 4)))), 0.010, seg=14, m=1)
         for k in range(12)],
        [cyl(tuple(h + Vector((-0.045 + 0.03 * (k % 4), 0.062, -0.035 + 0.035 * (k // 4)))),
             tuple(h + Vector((-0.045 + 0.03 * (k % 4), 0.066, -0.035 + 0.035 * (k // 4)))), 0.005, seg=10, m=2)
         for k in range(12)],
        pcb(tuple(h + Vector((0, 0.069, 0))), (0.11, 0.09, 0.0016), (0, 1, 0), Z, 35, 41, 3, 4, 5, 6, 7),
        _small_motor(tuple(h + Vector((0, -0.075, 0))), Y, 0.034, 0.045, 2, 1, 0, 8),
        cyl(tuple(h + Vector((-0.04, 0, -0.02))), tuple(h + Vector((0.04, 0, -0.02))), 0.006, seg=12, m=0),
    ], "Interior de la HCU: 12 electroválvulas, motor de la bomba de pistones y placa de control",
        edir=(0.5, 0.5, 0.6), dist=0.50, stage=6, group="Frenos", fid="A", note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Compresor de la suspensión neumática
# ---------------------------------------------------------------------------
def air_compressor(M):
    c = Vector((-0.42, -2.28, 0.48))
    V4.set_explode("CHS_AirSuspension_Compressor", (-1, -0.3, 0), 0.70, 6)
    return V4.part(M, "CHS_Air_Compressor_Internals", "REAR_SUSPENSION", ["elec_steel", "copper_enamel",
                                                                           "gear_steel", "alu_machined", "nylon"], [
        _small_motor(tuple(c + Vector((0.10, 0, 0))), X, 0.050, 0.16, 0, 1, 2, 10),
        disc(tuple(c + Vector((0.205, 0, 0))), X, 0.022, 0.010, 20, 2),
        cyl(tuple(c + Vector((0.212, 0, 0.012))), tuple(c + Vector((0.230, 0, 0.040))), 0.006, seg=10, m=2),
        cyl(tuple(c + Vector((0.230, 0, 0.040))), tuple(c + Vector((0.236, 0, 0.040))), 0.022, seg=24, m=3),
        cyl(tuple(c + Vector((-0.012, 0, 0))), tuple(c + Vector((-0.055, 0, 0))), 0.024, seg=20, m=4),
    ], "Interior del compresor: motor, excéntrica, biela, pistón y cartucho secador",
        parent="AIR_SUPPLY", edir=(0, -0.3, 1), dist=0.35, stage=6, group="Suspensión", fid="A", note=NOTE)


def build(M):
    out = []
    out += calipers(M)
    out += dampers(M)
    out += steering(M)
    out += brake_actuation(M)
    out += air_compressor(M)
    return out
