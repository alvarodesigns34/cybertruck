"""Versión 3 · interior: salpicadero, consola, asientos, seguridad pasiva, climatización, audio y guarnecidos.

Fuentes (docs/ficha-tecnica-piezas.md §3.5; manual de servicio «SM» y manual del propietario «OM»):
  [V] Denominación, cantidad y fijaciones (INT-xxx).
  [R] Forma y posición reconstruidas dentro de los volúmenes que ya definía el modelo; no hay planos del
      interior (las figuras del manual no son legibles en texto).
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, rivet

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
DOORS = (("F", 0.11, 1.17), ("R", -0.89, 0.06))


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend
    D, C, CT, SE, DR, TR = ("INTERIOR_DASHBOARD", "INTERIOR_CONTROLS", "STEERING", "INTERIOR_SEATS",
                            "INTERIOR_DOORS", "INTERIOR_TRIM")

    # --- Salpicadero ---------------------------------------------------------------------------------------------
    A(V3.part(M, "INT_IP_Mid_Panel", D, ["int_plastic", "zinc"], [
        # entre el panel inferior del conductor (x <= -0,24) y la guantera (x >= 0,14)
        box((-0.05, 0.975, 0.905), (0.372, 0.030, 0.17), 0.004),
        line(clip, (-0.20, 0.958, 0.86), (0.10, 0.958, 0.86), 4, axis=(0, -1, 0)),
    ], "Panel medio del salpicadero (Mid Panel Assembly)", edir=(0, -1, 0.1), dist=0.45))
    A(V3.part(M, "INT_IP_Center_Shroud_Service_Panel", D, ["int_plastic"], [
        box((0, 0.965, 1.025), (0.30, 0.020, 0.070), 0.003),
    ], "Panel de servicio del embellecedor central", edir=(0, -1, 0.3), dist=0.4))
    A(V3.part(M, "INT_Display_Shroud", C, ["plastic_black"], [
        box((0, 0.905, 1.355), (0.48, 0.030, 0.020), 0.003), box((0, 0.905, 1.080), (0.48, 0.030, 0.020), 0.003),
        box((-0.235, 0.905, 1.218), (0.020, 0.030, 0.270), 0.003), box((0.235, 0.905, 1.218), (0.020, 0.030, 0.270), 0.003),
    ], "Marco (Display Shroud) de la pantalla central", edir=(0, -1, 0.3), dist=0.4))
    A(V3.part(M, "INT_Footwell_Cover", D, ["int_grey", "zinc"], [
        box((-0.45, 1.15, 0.525), (0.30, 0.22, 0.016), 0.003),
        bolt((-0.45, 1.15, 0.533), Z, 0.007, 1),
    ], "Cubierta de la zona de pies del conductor (1 perno a 3 N·m, se retira al sacar el pack)", edir=(0, 0, 1),
        dist=0.35, stage=6))
    A(V3.part(M, "INT_IP_Gap_Hiders", D, ["rubber"], [
        # el superior, interrumpido en la columna de dirección (x -0,395 ± 0,075) y hasta la guantera (x 0,14)
        box((-0.545, 0.957, 0.982), (0.21, 0.012, 0.012), 0.002), box((-0.095, 0.957, 0.982), (0.45, 0.012, 0.012), 0.002),
        box((0, 0.957, 0.80), (1.30, 0.012, 0.012), 0.002),
    ], "Cubrejuntas del salpicadero (superior e inferior)", edir=(0, -1, 0), dist=0.3, stage=6))
    A(V3.part(M, "INT_Puddle_Lamps", D, ["lamp_housing", "led_white"], [
        box((0.44, 1.00, 0.795), (0.05, 0.010, 0.012), 0.001, 1),
        box((0.55, 1.18, 0.54), (0.05, 0.020, 0.010), 0.001, 1), box((-0.55, 1.18, 0.54), (0.05, 0.020, 0.010), 0.001, 1),
    ], "Luces de cortesía de la guantera y de las zonas de pies", edir=(0, -0.3, -0.5), dist=0.3, stage=6))
    A(V3.part(M, "INT_Ethernet_Diagnostic_RJ45", D, ["plastic_black", "connector_grey"], [
        box((0.62, 1.005, 0.78), (0.040, 0.020, 0.030), 0.002), box((0.62, 0.994, 0.78), (0.022, 0.006, 0.016), 0.001, 1),
    ], "Módulo de diagnóstico Ethernet (RJ45)", edir=(0, -1, 0), dist=0.3, stage=6))
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        A(V3.part(M, f"INT_IP_Airwave_Module_{sd}", D, ["int_plastic", "zinc"], [
            # por encima del tronco del mazo del salpicadero (z <= 1,043 sobre la viga transversal)
            box((s * 0.58, 1.03, 1.077), (0.20, 0.08, 0.05), 0.004),
            beam((s * 0.62, 1.07, 1.077), (s * 0.62, 1.50, 1.02), 0.06, 0.04, 0.003),
            line(torx, (s * 0.50, 0.99, 1.077), (s * 0.66, 0.99, 1.077), 3, axis=(0, -1, 0), d=0.005),
        ], f"Módulo y conducto del «Airwave» {side}", edir=(0, -0.5, 0.5), dist=0.4))
        A(V3.part(M, f"INT_Demist_Duct_Side_{sd}", D, ["int_plastic"], [
            beam((s * 0.76, 1.50, 1.18), (s * 0.78, 1.75, 1.22), 0.04, 0.035, 0.003),
        ], f"Conducto de desempañado de la ventanilla lateral {side}", edir=(s, 0.3, 0.5), dist=0.35))
        A(V3.part(M, f"INT_Floor_Duct_{sd}", D, ["int_plastic"], [
            # sobre el guarnecido central del suelo (z 0,5175); el exterior acaba antes del reposapiés (y 1,11) y el
            # interior va junto al panel lateral de la consola (|x| <= 0,146)
            beam((s * 0.68, 0.98, 0.530), (s * 0.68, 0.60, 0.530), 0.07, 0.025, 0.003),
            beam((s * 0.168, 1.00, 0.530), (s * 0.168, 0.20, 0.530), 0.04, 0.025, 0.003),
        ], f"Conductos de suelo {side}s (exterior e interior)", edir=(s, 0, -0.6), dist=0.35))
        A(V3.part(M, f"INT_Tweeter_{sd}", D, ["speaker_mesh", "plastic_black"], [
            cyl((s * 0.72, 1.52, 1.255), (s * 0.72, 1.52, 1.268), 0.022, seg=16, m=0),
            ring((s * 0.72, 1.52, 1.25), Z, 0.022, 0.030, 0.012, 16, 1),
        ], f"Tweeter {side} del salpicadero", edir=(s, 0.3, 1), dist=0.35, stage=6))
        A(V3.part(M, f"INT_Telephony_Mic_{sd}", TR, ["plastic_black"], [
            disc((s * 0.40, 0.62, 1.69), Z, 0.009, 0.004, 12, 0),
        ], f"Micrófono de telefonía {side}", edir=(0, 0, -1), dist=0.3, stage=6))
    A(V3.part(M, "INT_Demist_Ducts_Center", D, ["int_plastic"], [
        # por detrás del Super Cowl (y < 1,819), bajo la boca del tablero
        beam((-0.35, 1.745, 1.215), (-0.15, 1.745, 1.225), 0.14, 0.03, 0.003),
        beam((0.35, 1.745, 1.215), (0.15, 1.745, 1.225), 0.14, 0.03, 0.003),
    ], "Conductos de desempañado del parabrisas (conductor y acompañante)", edir=(0, 0.4, 1), dist=0.35))
    A(V3.part(M, "INT_Super_Horn", "UNDERBODY", ["plastic_black", "zinc"], [
        cyl((0.35, 2.26, 0.56), (0.35, 2.26, 0.62), 0.040, seg=18, m=0),
        cyl((-0.60, 2.28, 0.55), (-0.60, 2.28, 0.61), 0.030, seg=18, m=0),
        bolt((0.35, 2.26, 0.625), Z, 0.007, 1), bolt((-0.60, 2.28, 0.615), Z, 0.007, 1),
    ], "Bocina «Super Horn» y bocina de tono bajo izquierda", edir=(0, 0.5, 0.2), dist=0.4, stage=6))

    # --- Climatización -------------------------------------------------------------------------------------------
    A(V3.part(M, "INT_HVAC_Blend_Door_Actuator", D, ["plastic_black", "zinc"], [
        box((0.10, 1.12, 0.62), (0.06, 0.05, 0.045), 0.003), cyl((0.10, 1.095, 0.62), (0.10, 1.075, 0.62), 0.010, seg=10, m=1),
    ], "Actuador de la compuerta de mezcla del climatizador", edir=(0, 0.3, -0.3), dist=0.35, stage=6))
    A(V3.part(M, "INT_HVAC_HEPA_Filter", D, ["plastic_black", "carpet", "zinc"], [
        # bajo el soplador, por fuera del conducto derecho al suelo; tapa hacia el hueco de los pies
        box((0.45, 1.03, 0.60), (0.20, 0.12, 0.18), 0.004),
        box((0.45, 0.963, 0.60), (0.22, 0.014, 0.20), 0.003, 0),
        line(torx, (0.37, 0.955, 0.67), (0.53, 0.955, 0.67), 3, axis=(0, -1, 0), d=0.005),
    ], "Filtro HEPA con cubierta (3 tornillos T20 a 1 N·m en el soplador)", edir=(0, -1, -0.3), dist=0.4, stage=6))
    A(V3.part(M, "INT_HVAC_Sensors", D, ["plastic_black"], [
        box((0.30, 1.00, 1.01), (0.028, 0.012, 0.022), 0.002), box((-0.30, 1.00, 1.01), (0.028, 0.012, 0.022), 0.002),
        box((0.0, 0.64, 1.67), (0.030, 0.020, 0.020), 0.002),
    ], "Sensores de climatización (temperatura y humedad de cabina, ventilado, parabrisas)", edir=(0, -0.5, 0.3),
        dist=0.3, stage=6))
    A(V3.part(M, "INT_Air_Extractor", TR, ["plastic_black", "rubber"], [
        box((0.60, -0.935, 0.62), (0.22, 0.020, 0.080), 0.003),
        [box((0.60, -0.947, 0.595 + 0.025 * k), (0.20, 0.005, 0.010), 0.001, 1) for k in range(3)],
    ], "Extractor de aire de la pared trasera", edir=(0, -1, 0), dist=0.4, stage=6))

    # --- Consola central -----------------------------------------------------------------------------------------
    A(V3.part(M, "INT_Console_Riser_Rails", C, ["steel_black", "int_plastic", "zinc"], [
        # dentro del hueco inferior de la consola (build_montaje.POCKETS: x ±0,108, y -0,105…0,905, hasta z 0,562),
        # apoyada sobre el guarnecido central del suelo (z 0,52)
        box((0, 0.40, 0.527), (0.21, 0.90, 0.012), 0.003, 1),
        beam((-0.085, -0.095, 0.541), (-0.085, 0.895, 0.541), 0.030, 0.016, 0.002), beam((0.085, -0.095, 0.541), (0.085, 0.895, 0.541), 0.030, 0.016, 0.002),
        line(bolt, (-0.085, -0.05, 0.549), (0.085, 0.85, 0.549), 6, axis=Z, d=0.008, m=2),
    ], "Base (riser) y raíles del suelo central de la consola (2 pernos traseros + 4 delanteros a 5 N·m)",
        edir=(0, 0, -1), dist=0.45, stage=2))
    A(V3.part(M, "INT_Console_USB_Controller_Hub", C, ["plastic_black", "connector_grey"], [
        box((0, 0.85, 0.665), (0.10, 0.07, 0.032), 0.003),
        [box((x, 0.808, 0.67), (0.014, 0.006, 0.008), 0.001, 1) for x in (-0.03, 0.0, 0.03)],
    ], "Controlador y concentrador USB de la consola (USB-C de 65 W)", edir=(0, 0.3, 0.5), dist=0.35, stage=6))
    A(V3.part(M, "INT_Console_Harness_Lamp", C, ["harness", "led_white", "connector_grey"], [
        # por encima del módulo de airbags (RCM, z <= 0,575)
        hose([(0.0, 0.85, 0.62), (0.0, 0.40, 0.60), (0.0, -0.05, 0.62)], 0.006, 8, 5, 0),
        box((0.0, 0.02, 0.775), (0.040, 0.020, 0.008), 0.001, 1),
    ], "Mazo de la consola y luz de cortesía de la consola", edir=(0, 0, -1), dist=0.35, stage=6))
    A(V3.part(M, "INT_Cabin_Outlets_120V", C, ["plastic_black", "connector_grey"], [
        box((0.0, 0.64, 0.735), (0.060, 0.012, 0.040), 0.002), box((0.0, -0.17, 0.735), (0.060, 0.012, 0.040), 0.002),
        [box((x, 0.633, 0.735), (0.006, 0.004, 0.016), 0.0005, 1) for x in (-0.012, 0.012)],
    ], "Tomas de 120 V de la cabina (NEMA 5-20; 20 A compartidos)", edir=(0, 0.3, 0.5), dist=0.3, stage=6))
    A(V3.part(M, "INT_Console_Rear_Panel_Clips", C, ["plastic_black"], [
        line(clip, (-0.11, -0.14, 0.62), (0.11, -0.14, 0.62), 10, axis=(0, -1, 0), d=0.010, m=0),
    ], "Clips del panel trasero de la consola (10 + 3 pestañas)", edir=(0, -1, 0), dist=0.3, stage=6))

    # --- Asientos ---------------------------------------------------------------------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        xc = s * 0.40
        A(V3.part(M, f"INT_SeatF_{sd}_Motors", SE, ["steel_black", "plastic_black", "zinc"], [
            cyl((xc - 0.06, 0.20, 0.70), (xc + 0.06, 0.20, 0.70), 0.026, seg=16, m=0),
            cyl((xc - 0.06, 0.55, 0.585), (xc + 0.06, 0.55, 0.585), 0.026, seg=16, m=0),
            cyl((xc - 0.06, 0.28, 0.575), (xc + 0.06, 0.28, 0.575), 0.024, seg=16, m=0),
            box((xc, 0.42, 0.545), (0.10, 0.06, 0.040), 0.004, 1),
            [bolt((xc + dx, 0.42, 0.567), Z, 0.007, 2) for dx in (-0.04, 0.04)],
        ], f"Motores del asiento delantero {side}: reclinado, altura, inclinación y puente de carril (Bridge Track)",
            edir=(s * 0.3, 0, -1), dist=0.4))
        A(V3.part(M, f"INT_SeatF_{sd}_Blower", SE, ["plastic_black", "speaker_mesh"], [
            cyl((xc, 0.40, 0.600), (xc, 0.40, 0.640), 0.045, seg=20, m=0),
            disc((xc, 0.40, 0.642), Z, 0.032, 0.004, 14, 1),
        ], f"Soplador de ventilación del cojín del asiento delantero {side}", edir=(s * 0.3, 0, -1), dist=0.35))
        A(V3.part(M, f"INT_SeatF_{sd}_Covers", SE, ["int_plastic", "zinc"], [
            box((s * 0.205, 0.46, 0.6085), (0.036, 0.55, 0.023), 0.003),
            box((s * 0.585, 0.46, 0.6085), (0.036, 0.55, 0.023), 0.003),
            [disc((s * x, y, 0.6215), Z, 0.007, 0.003, 10, 1) for x in (0.205, 0.585) for y in (0.26, 0.64)],
        ], f"Cubiertas de carril y de tornillos del asiento delantero {side} (4 pernos T45P a 34 N·m, desechables)",
            edir=(s * 0.5, 0, 0.3), dist=0.35, stage=6))
        A(V3.part(M, f"INT_Airbag_Seat_Side_{sd}", SE, ["int_plastic", "stitch"], [
            box((s * 0.682, 0.05, 0.95), (0.040, 0.10, 0.28), 0.005),
        ], f"Airbag lateral montado en el respaldo del asiento delantero {side}", edir=(s, 0, 0.3), dist=0.4,
            group="Seguridad"))
        A(V3.part(M, f"INT_Airbag_Curtain_{sd}", TR, ["int_plastic", "stitch"], [
            box((s * 0.725, 0.0, 1.50), (0.040, 1.70, 0.060), 0.006),
        ], f"Airbag de cortina {side} (techo y pilares)", edir=(s, 0, -0.5), dist=0.4, group="Seguridad"))
        A(V3.part(M, f"INT_Impact_Sensor_BPillar_{sd}", TR, ["plastic_black", "connector_grey"], [
            box((s * 0.725, 0.10, 0.90), (0.020, 0.040, 0.030), 0.002),
        ], f"Sensor de impacto del pilar B {side}", edir=(s, 0, 0), dist=0.3, stage=6, group="Seguridad"))
        A(V3.part(M, f"INT_Impact_Sensor_Fender_{sd}", "BODY_FASTENERS", ["plastic_black", "connector_grey"], [
            box((s * 0.88, 1.90, 0.80), (0.020, 0.040, 0.030), 0.002),
        ], f"Sensor de impacto de la aleta {side}", edir=(s, 0.3, 0), dist=0.3, stage=6, group="Seguridad"))
        A(V3.part(M, f"INT_Impact_Sensor_FrontEnd_{sd}", "BODY_FASTENERS", ["plastic_black", "connector_grey"], [
            box((s * 0.55, 2.50, 0.56), (0.040, 0.020, 0.030), 0.002),
        ], f"Sensor de impacto del módulo frontal {side}", edir=(s * 0.3, 1, 0), dist=0.3, stage=6, group="Seguridad"))
        A(V3.part(M, f"INT_Door_Pressure_Sensors_{sd}", "BODY_FASTENERS", ["plastic_black", "connector_grey"], [
            box((s * 0.86, 0.65, 0.66), (0.020, 0.030, 0.030), 0.002), box((s * 0.86, -0.45, 0.66), (0.020, 0.030, 0.030), 0.002),
        ], f"Sensores de presión de las puertas {side}s (delantera y trasera)", edir=(s, 0, 0), dist=0.3, stage=6,
            group="Seguridad"))
        A(V3.part(M, f"INT_Seatbelt_Webguides_{sd}", TR, ["plastic_black", "seatbelt"], [
            box((s * 0.690, 0.08, 1.32), (0.020, 0.050, 0.060), 0.003), box((s * 0.690, -0.88, 1.25), (0.020, 0.050, 0.060), 0.003),
        ], f"Guías de cinta de los cinturones {side}s (pilares B y C)", edir=(s, 0, 0.3), dist=0.3, stage=6))
        A(V3.part(M, f"INT_Rear_Seat_Underbelly_{sd}", SE, ["int_plastic", "plastic_black"], [
            box((s * 0.35, -0.55, 0.515), (0.50, 0.40, 0.014), 0.003),
            beam((s * 0.12, -0.20, 0.525), (s * 0.30, -0.70, 0.525), 0.05, 0.022, 0.002),
        ], f"Carenado inferior (underbelly) y conducto en Y del suelo del asiento trasero {side}",
            edir=(s * 0.3, -0.3, -1), dist=0.35, stage=2))
        A(V3.part(M, f"INT_Rear_Shoulder_Cover_{sd}", SE, ["int_plastic", "zinc"], [
            # por detrás de la esquina superior exterior del respaldo (que en la v4 queda delante de la pared)
            box((s * 0.65, -0.932, 1.172), (0.08, 0.03, 0.10), 0.004),
            line(clip, (s * 0.64, -0.917, 1.135), (s * 0.64, -0.917, 1.215), 7, axis=(0, 1, 0)),
        ], f"Cubierta de hombro del respaldo trasero {side} (7 clips + 1 datum)", edir=(s * 0.4, -0.5, 0.5),
            dist=0.35, stage=6))
    A(V3.part(M, "INT_SeatF_L_Position_Sensor", SE, ["plastic_black"], [
        box((-0.45, 0.30, 0.545), (0.030, 0.020, 0.012), 0.002),
    ], "Sensor de posición del carril del asiento del conductor", edir=(-0.3, 0, -1), dist=0.3, stage=6))
    A(V3.part(M, "INT_SeatF_R_Occupancy_Sensor", SE, ["plastic_black", "connector_grey"], [
        box((0.40, 0.50, 0.668), (0.34, 0.34, 0.004), 0.001), box((0.52, 0.36, 0.636), (0.040, 0.030, 0.016), 0.002, 1),
    ], "Sensor de clasificación de ocupación del acompañante (umbrales ≈20 lb y 51–103 lb)", edir=(0.3, 0, 1),
        dist=0.3, stage=6, group="Seguridad"))
    # dentro del cojín central del buje (ejes de la columna inclinada (0, 1, -0,42)), delante del muelle de reloj
    wc, wd = Vector((-0.395, 0.735, 1.02)), Vector((0, 1, -0.42)).normalized()
    wv = Vector((0, -wd.z, wd.y))
    A(V3.part(M, "INT_Airbag_Driver", CT, ["int_plastic", "zinc", "stitch"], [
        hull([tuple(wc + wd * t + wv * b + Vector((a, 0, 0))) for a in (-0.055, 0.055) for b in (-0.036, 0.036)
              for t in (0.007, 0.028)]),
        [clip(tuple(wc + wd * 0.030 + Vector((dx, 0, 0))), tuple(wd), 0.008, 1) for dx in (-0.045, 0.045)],
    ], "Airbag del conductor en el centro del volante (2 clips de resorte + 1 conector)", edir=(0, -1, 0.3),
        dist=0.4, group="Seguridad"))

    # --- Cámara, retrovisor y carenados del parabrisas ---------------------------------------------------------
    A(V3.part(M, "INT_Interior_Camera", TR, ["plastic_black", "glass_lens", "zinc"], [
        box((0.0, 0.60, 1.695), (0.045, 0.030, 0.030), 0.004),
        cyl((0.0, 0.584, 1.695), (0.0, 0.578, 1.695), 0.007, seg=12, m=1),
        torx((-0.02, 0.60, 1.680), (0, 0, -1), 0.004, 2), torx((0.02, 0.60, 1.680), (0, 0, -1), 0.004, 2),
    ], "Cámara interior de la cabina sobre el retrovisor (2 tornillos T10 a 0,8 N·m)", edir=(0, -0.3, 0.8),
        dist=0.35, stage=6))
    A(V3.part(M, "INT_Rearview_Beauty_Cover", TR, ["plastic_black"], [
        box((0.0, 0.655, 1.688), (0.20, 0.050, 0.014), 0.003),
    ], "Cubierta decorativa del retrovisor interior (beauty cover)", edir=(0, 0, 1), dist=0.3, stage=6))

    # --- Puertas: grapas, espuma NVH y cable de liberación manual ---------------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        for d, y0, y1 in DOORS:
            nm = f"{d}{sd}"
            dn = "delantera" if d == "F" else "trasera"
            side = "derecha" if s > 0 else "izquierda"
            pts = []
            for i in range(14):
                t = i / 13.0
                if t < 0.25:
                    p = (y0 + 0.03, 0.62 + t * 2.2 * 0.58)
                elif t < 0.5:
                    p = (y0 + 0.03 + (t - 0.25) * 4 * (y1 - y0 - 0.06), 1.16)
                elif t < 0.75:
                    p = (y1 - 0.03, 1.16 - (t - 0.5) * 4 * 0.50)
                else:
                    p = (y1 - 0.03 - (t - 0.75) * 4 * (y1 - y0 - 0.06), 0.58)
                pts.append(p)
            xw = 0.805 if d == "F" else 0.790      # cara exterior del panel (build_interior_detail)
            A(V3.part(M, f"INT_DoorTrim_Clips_{nm}", DR, ["plastic_black"], [
                [clip((s * xw, y, z), (s, 0, 0), 0.012, 0) for (y, z) in pts],
            ], f"14 grapas del panel de la puerta {dn} {side}", edir=(-s, 0, 0), dist=0.3, stage=6))
            A(V3.part(M, f"INT_Door_NVH_Foam_{nm}", DR, ["rubber"], [
                box((s * (xw + 0.006), (y0 + y1) / 2, 0.86), (0.010, (y1 - y0) - 0.16, 0.46), 0.003),
            ], f"Espuma NVH de la puerta {dn} {side}", edir=(s, 0, 0), dist=0.3, stage=2))
            A(V3.part(M, f"INT_Door_Manual_Release_{nm}", DR, ["plastic_black", "hose"], [
                # tirador por delante del panel, sobre el reposabrazos; el cable discurre por detrás del panel
                box((s * (xw - 0.046), y0 + 0.14, 0.866), (0.016, 0.040, 0.020), 0.003),
                hose([(s * (xw + 0.006), y0 + 0.14, 0.86), (s * (xw + 0.008), y0 + 0.25, 0.90),
                      (s * (xw + 0.010), y0 + 0.36, 0.84)], 0.002, 6, 4, 1),
            ], f"Cable y tirador de liberación manual de la puerta {dn} {side}", edir=(-s, 0, 0.3), dist=0.3,
                stage=6))

    # --- Pilares, cabeceras y suelo ---------------------------------------------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        a = (s * (S.hw_glass(1.75, 1.26) - 0.05), 1.75, 1.26)
        b = (s * (S.hw_roof_edge(0.60) - 0.04), 0.60, S.z_top(0.60) - 0.06)
        A(V3.part(M, f"INT_Trim_APillar_Clips_{sd}", TR, ["plastic_black"], [
            line(clip, a, b, 13, axis=(-s, 0, 0), d=0.010, m=0),
        ], f"Grapas del guarnecido del pilar A {side} (4 delanteras, 8 superiores, 1 central)", edir=(-s, 0, 0.3),
            dist=0.3, stage=6))
    A(V3.part(M, "INT_Header_Front_Clips", TR, ["plastic_black", "steel_black"], [
        line(clip, (-0.66, 0.59, 1.700), (0.66, 0.59, 1.700), 19, axis=Z, d=0.010, m=0),
        box((0.0, 0.61, 1.695), (0.012, 0.012, 0.006), 0.001, 1),
    ], "19 grapas e imán de la moldura de cabecera delantera", edir=(0, 0, -1), dist=0.3, stage=6))
    A(V3.part(M, "INT_Carpet_Clips_RH", TR, ["plastic_black"], [
        line(clip, (0.40, 1.28, 0.505), (0.80, 1.28, 0.505), 8, axis=Z, d=0.010, m=0),
        [disc((0.45 + 0.10 * k, 1.24, 0.503), Z, 0.006, 0.003, 10, 0) for k in range(4)],
    ], "8 grapas y 4 datums de la alfombra derecha", edir=(0, 0, 1), dist=0.3, stage=6))
    A(V3.part(M, "INT_Center_Floor_Trim", TR, ["int_grey", "plastic_black"], [
        box((0.0, 0.20, 0.515), (0.30, 0.70, 0.012), 0.003),
        box((0.0, -0.935, 0.60), (1.40, 0.012, 0.16), 0.003, 1),
        box((-0.72, 1.18, 0.60), (0.020, 0.30, 0.16), 0.003, 1),
    ], "Molduras del suelo central, de la pared trasera inferior y lateral de los pedales", edir=(0, 0, -1),
        dist=0.3, stage=2))
    # Carcasas de la columna de dirección y embellecedores de conductos
    # coaxial con la columna (eje (0, 1, -0,42) desde el centro del volante) y por fuera de su cubierta principal
    # (r <= 60 mm); el módulo de control de la columna (SCCM) queda dentro
    wc, wd = Vector((-0.395, 0.735, 1.02)), Vector((0, 1, -0.42)).normalized()
    wv = Vector((0, -wd.z, wd.y))
    A(V3.part(M, "INT_Steering_Column_Shroud_Lower", CT, ["int_plastic", "zinc"], [
        cyl(tuple(wc + wd * 0.11), tuple(wc + wd * 0.215), 0.064, 0.066, 24, 0, caps=False),
        clip(tuple(wc + wd * 0.12 - wv * 0.064), tuple(-wv), 0.010, 1),
    ], "Carcasa inferior de la columna (Lower Column Shroud) y su clip", edir=(0, -0.5, -0.5), dist=0.35,
        stage=2))
    A(V3.part(M, "INT_Duct_Bezel_Carpet_Rear", TR, ["carpet", "plastic_black"], [
        box((0.0, -0.30, 0.512), (0.18, 0.14, 0.006), 0.002),
    ], "Embellecedor del conducto trasero en la alfombra", edir=(0, 0, 1), dist=0.3, stage=6))
    return [o for o in out if o is not None]
