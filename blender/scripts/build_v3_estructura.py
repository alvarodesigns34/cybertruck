"""Versión 3 · carrocería en blanco: soportes, refuerzos, cabeceras, tapones y remachado por familias.

Fuentes (docs/ficha-tecnica-piezas.md §3.2, manual de reparación de carrocería «CR» y manual de servicio):
  [V] Denominación, cantidad y fijaciones de cada pieza (identificadores EST-xxx / INT-xxx).
  [R] Posición y forma: reconstruidas dentro del hueco que deja la estructura de la versión 2; el CR no
      publica cotas en texto (están en imágenes).
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v3 as V3
from ct_v3 import box, cyl, disc, hull, beam, sweep, bolt, nut, torx, clip, rivet, ribs, rowx, rowy, rowz

SYS = "BODY_STRUCTURE"
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def line(fn, a, b, n, **kw):
    """n formas repetidas (tornillería) entre los puntos a y b."""
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend

    # --- Salpicadero y parte delantera -----------------------------------------------------------------
    A(V3.part(M, "BODY_Super_Cowl", SYS, ["ecoat", "zinc"], [
        box((0, 1.885, 1.17), (1.64, 0.10, 0.075), 0.006),
        box((0, 1.945, 1.17), (1.64, 0.016, 0.17), 0.004),
        ribs((-0.80, 1.835, 1.13), X, Z, 1.60, 0.085, 10, 1, (0, -1, 0), rib_h=0.012),
        line(rivet, (-0.74, 1.955, 1.10), (0.74, 1.955, 1.10), 14, axis=Y),
    ], "Super Cowl: travesaño del cowl bajo el parabrisas", edir=(0, 0.4, 1), dist=0.55, stage=3))
    A(V3.part(M, "BODY_Aerobracket", SYS, ["alu_cast", "zinc"], [
        box((0, 1.74, 1.10), (0.46, 0.07, 0.09), 0.005),
        bolt((-0.17, 1.74, 1.146), Z, 0.008, 1), bolt((0.17, 1.74, 1.146), Z, 0.008, 1),
    ], "Soporte aerodinámico (Aerobracket) del salpicadero", edir=(0, 0.5, 1), dist=0.5, stage=3))
    A(V3.part(M, "BODY_IP_Display_Bracket", SYS, ["steel_black", "zinc"], [
        box((0.19, 1.04, 1.19), (0.035, 0.10, 0.24), 0.003),
        box((0.19, 1.04, 1.07), (0.10, 0.10, 0.025), 0.003),
        bolt((0.19, 1.04, 1.085), Z, 0.007, 1), torx((0.19, 1.09, 1.25), Y, 0.005, 1),
    ], "Soporte {lado} de la pantalla central", mirror=True, edir=(0, -0.4, 1), dist=0.45, stage=3))
    A(V3.part(M, "BODY_IP_Downleg_Bracket", SYS, ["steel_black", "zinc"], [
        # el pie apoya sobre la moqueta (cara superior z 0,517)
        # (entre el filtro HEPA, y <= 1,09, y la tapa de acceso a los pirofusibles, y >= 1,165)
        beam((0.45, 1.10, 0.93), (0.46, 1.1275, 0.523), 0.05, 0.03, 0.003),
        box((0.46, 1.1275, 0.523), (0.10, 0.07, 0.012), 0.002),
        bolt((0.43, 1.1275, 0.535), Z, 0.008, 1), bolt((0.49, 1.1275, 0.535), Z, 0.008, 1),
    ], "Pata {lado} del salpicadero (Downleg Bracket)", mirror=True, edir=(0, -0.3, -1), dist=0.4, stage=3))
    A(V3.part(M, "BODY_IP_Beam_Bracket", SYS, ["steel_black", "zinc"], [
        # por delante del larguero del guardabarros (y >= 1,248) y por dentro de la fundición
        box((0.773, 1.20, 0.985), (0.050, 0.09, 0.15), 0.003),
        line(rivet, (0.750, 1.17, 0.94), (0.750, 1.23, 1.03), 6, axis=(-1, 0, 0)),
    ], "Soporte {lado} de la viga del salpicadero (6 remaches HS o soldadura de tapón)", mirror=True,
        edir=(1, 0, 0.3), dist=0.35, stage=3))
    A(V3.part(M, "BODY_Steering_Column_Bracket", SYS, ["steel_black", "zinc"], [
        # detrás del actuador del volante, colgado de la viga transversal
        box((-0.39, 1.25, 1.00), (0.14, 0.04, 0.12), 0.004),
        torx((-0.34, 1.228, 1.03), (0, -1, 0), 0.006, 1), torx((-0.44, 1.228, 1.03), (0, -1, 0), 0.006, 1),
        torx((-0.34, 1.228, 0.97), (0, -1, 0), 0.006, 1), torx((-0.44, 1.228, 0.97), (0, -1, 0), 0.006, 1),
    ], "Soporte de la columna de dirección en el salpicadero (4 tuercas a 18 N·m)", edir=(-0.3, -0.6, 0.2),
        dist=0.4, stage=3))
    A(V3.part(M, "BODY_Front_Body_Bridge_Reinforcement", SYS, ["ecoat", "zinc"], [
        box((0, 1.74, 1.08), (1.66, 0.06, 0.07), 0.005),
        hull([(-0.83, 1.71, 1.045), (-0.83, 1.77, 1.045), (-0.70, 1.71, 1.045), (-0.70, 1.77, 1.045),
              (-0.83, 1.71, 0.88), (-0.83, 1.77, 0.88)]),
        hull([(0.83, 1.71, 1.045), (0.83, 1.77, 1.045), (0.70, 1.71, 1.045), (0.70, 1.77, 1.045),
              (0.83, 1.71, 0.88), (0.83, 1.77, 0.88)]),
        line(rivet, (-0.60, 1.74, 1.116), (0.60, 1.74, 1.116), 9, axis=Z),
    ], "Refuerzo del puente delantero (Front Body Bridge): 18 remaches HS izq. / 20 der.", edir=(0, 0.5, 1),
        dist=0.5, stage=3))
    A(V3.part(M, "BODY_Dash_Reinforcement", SYS, ["ecoat", "zinc"], [
        ribs((-0.74, 1.43, 0.58), X, Z, 1.48, 0.28, 8, 2, (0, -1, 0), rib_h=0.012),
        line(rivet, (-0.70, 1.436, 0.60), (0.70, 1.436, 0.60), 13, axis=(0, -1, 0)),
        line(rivet, (-0.70, 1.436, 0.82), (0.70, 1.436, 0.82), 13, axis=(0, -1, 0)),
    ], "Refuerzo del mamparo (Dash Reinforcement): 61 remaches HS + 4 flow-form S18", edir=(0, -0.6, 0.4),
        dist=0.55, stage=3))
    A(V3.part(M, "BODY_Dash_FUB_Gutter_Connector", SYS, ["ecoat", "zinc"], [
        # solo en el tramo exterior, junto al larguero: por fuera de la unidad motriz delantera y de sus mangueras
        box((0.615, 1.785, 0.52), (0.21, 0.05, 0.04), 0.003),
        line(rivet, (0.525, 1.785, 0.542), (0.705, 1.785, 0.542), 8, axis=Z, d=0.0048),
    ], "Conector {lado} de canaleta salpicadero–fundición (8 remaches de 4,8 mm + adhesivo)", mirror=True,
        edir=(0.4, 0.3, 0.5), dist=0.4, stage=3))
    A(V3.part(M, "BODY_CFM_Bracket", SYS, ["alu_cast", "zinc"], [
        box((0, 2.375, 0.385), (0.96, 0.035, 0.045), 0.004),
        rivet((-0.30, 2.375, 0.362), (0, 0, -1)), rivet((0.30, 2.375, 0.362), (0, 0, -1)),
    ], "Soporte del módulo de ventiladores (2 remaches HS 6,5 mm + adhesivo)", edir=(0, 0.6, -0.6), dist=0.45,
        stage=3))
    A(V3.part(M, "BODY_Bumper_Beam_Mount", SYS, ["alu_machined", "zinc"], [
        box((0.53, 2.425, 0.54), (0.14, 0.03, 0.17), 0.004),
        rowx(bolt, (0.49, 0.53, 0.57), 2.405, 0.54, axis=(0, 1, 0), d=0.008, m=1),
    ], "Soporte {lado} de la viga del paragolpes (3 tornillos HF M8×28 a 21 N·m + adhesivo)", mirror=True,
        edir=(0.3, 1, 0), dist=0.5, stage=3))
    A(V3.part(M, "BODY_Fender_Beam", SYS, ["ecoat", "zinc"], [
        beam((0.80, 1.25, 1.03), (0.76, 2.12, 1.06), 0.05, 0.05, 0.004),
        line(bolt, (0.80, 1.40, 1.057), (0.77, 2.00, 1.087), 3, axis=Z, d=0.008, m=1),
    ], "Viga superior {lado} de la aleta (3 tornillos HF M8×28 a 28 N·m)", mirror=True, edir=(0.8, 0.2, 0.5),
        dist=0.45, stage=3))
    A(V3.part(M, "BODY_FDU_Mount", SYS, ["alu_cast", "zinc"], [
        box((0.40, 1.93, 0.47), (0.12, 0.16, 0.09), 0.004),
        line(bolt, (0.37, 1.89, 0.515), (0.43, 1.97, 0.515), 3, axis=Z, d=0.010, m=1),
    ], "Soporte {lado} de la unidad motriz delantera (3 tornillos HHL M10×41 a 65 N·m)", mirror=True,
        edir=(0.5, 0, -0.6), dist=0.5, stage=3))

    # --- Laterales, pilares y cabecera -----------------------------------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        y = -0.86
        pts = [(s * (S.hw_body(y, 0.50) - 0.10), y, 0.50), (s * (S.hw_body(y, 0.95) - 0.10), y, 0.95),
               (s * (S.hw_glass(y, 1.30) - 0.06), y, 1.30), (s * (S.hw_glass(y, 1.62) - 0.05), y + 0.02, 1.62)]
        A(V3.part(M, f"BODY_CPillar_Inner_{sd}", SYS, ["ecoat", "zinc"], [
            sweep(pts, 0.085, 0.014, 0.004, 4),
            line(rivet, (pts[0][0] - s * 0.012, y, 0.55), (pts[2][0] - s * 0.012, y, 1.28), 11,
                 axis=(-s, 0, 0)),
        ], f"Pilar C interior {'derecho' if s > 0 else 'izquierdo'} (33 remaches HS + 2 tornillos M10×33 a 90 N·m)",
            edir=(s, -0.3, 0.3), dist=0.5, stage=3))
    A(V3.part(M, "BODY_HV_Battery_Support_Bracket", SYS, ["steel_black", "zinc"], [
        # repisa soldada sobre la pestaña superior del umbral (z 0,409), bajo la pestaña de la bandeja de la batería
        # (z ~0,435, hasta x 0,837) y por fuera de su pared (x 0,80); por delante de la fundición trasera (y > -0,965)
        box((0.826, 0.075, 0.4155), (0.048, 2.05, 0.013), 0.002),
        line(rivet, (0.83, -0.90, 0.423), (0.83, 1.05, 0.423), 11, axis=Z),
    ], "Soporte {lado} de la batería HV (22 remaches HS + soldadura por puntos)", mirror=True,
        edir=(1, 0, -0.2), dist=0.5, stage=3))
    A(V3.part(M, "BODY_Rocker_Support_Bracket", SYS, ["steel_black", "zinc"], [
        box((0.86, 0.55, 0.34), (0.12, 0.10, 0.09), 0.003),
        box((0.86, -0.55, 0.34), (0.12, 0.10, 0.09), 0.003),
        line(rivet, (0.805, 0.53, 0.31), (0.805, 0.57, 0.37), 4, axis=(-1, 0, 0), d=0.0048),
        line(rivet, (0.805, -0.57, 0.31), (0.805, -0.53, 0.37), 4, axis=(-1, 0, 0), d=0.0048),
    ], "Soportes {lado} del umbral (2 por lado; 12 remaches de 4,8 mm cada uno)", mirror=True,
        edir=(1, 0, -0.5), dist=0.45, stage=3))
    A(V3.part(M, "BODY_XM_Bash_Plate", SYS, ["steel_black", "zinc"], [
        # dentro del umbral, entre su pared interior (x 0,805) y el inserto extruido (x >= 0,82)
        box((0.813, 0.0, 0.34), (0.012, 0.95, 0.08), 0.002),
        line(rivet, (0.812, -0.42, 0.34), (0.812, 0.42, 0.34), 8, axis=(-1, 0, 0), d=0.0048),
    ], "Placa de protección XM {lado} del umbral (remachada 4,8 mm o soldada)", mirror=True, edir=(1, 0, -1),
        dist=0.4, stage=3))
    A(V3.part(M, "BODY_Sail_Panel_Bracket", SYS, ["steel_black", "zinc"], [
        box((0.80, -1.05, 1.42), (0.06, 0.14, 0.08), 0.003),
        line(rivet, (0.80, -1.10, 1.462), (0.80, -1.00, 1.462), 3, axis=Z),
    ], "Soporte superior {lado} del panel de la vela (3 remaches HS)", mirror=True, edir=(1, -0.3, 0.6),
        dist=0.4, stage=3))
    A(V3.part(M, "BODY_Sail_Datum_Bracket", SYS, ["steel_black", "plastic_black"], [
        box((0.82, -1.20, 1.45), (0.05, 0.10, 0.10), 0.003),
        clip((0.80, -1.22, 1.50), Z, 0.012, 1), clip((0.80, -1.18, 1.50), Z, 0.012, 1),
    ], "Soporte {lado} de datum de la vela (2 clips de borde 1518812-00 + 2 bridas)", mirror=True,
        edir=(1, -0.3, 0.6), dist=0.4, stage=6))
    A(V3.part(M, "BODY_Cantrail_Stud_Plate", SYS, ["zinc"], [
        box((0.73, 0.55, 1.575), (0.05, 0.10, 0.012), 0.002), box((0.73, -0.55, 1.575), (0.05, 0.10, 0.012), 0.002),
        cyl((0.73, 0.55, 1.58), (0.73, 0.55, 1.61), 0.004, seg=8), cyl((0.73, -0.55, 1.58), (0.73, -0.55, 1.61),
                                                                  0.004, seg=8),
    ], "Placas {lado}s de espárragos del larguero de techo (1 avellanado estructural de 6,5 mm)", mirror=True,
        edir=(0.4, 0, 1), dist=0.45, stage=6))
    A(V3.part(M, "BODY_Cantrail_Trim_Bracket", SYS, ["steel_black"], [
        # en el larguero del techo, por fuera de los guarnecidos de los pilares y por debajo de la silueta del techo
        box((0.80, 0.80, 1.63), (0.03, 0.05, 0.04), 0.002), box((0.80, 0.05, 1.63), (0.03, 0.05, 0.04), 0.002),
        box((0.80, -0.70, 1.63), (0.03, 0.05, 0.04), 0.002),
    ], "Soportes {lado}s de la moldura del cantrail (soldadura por puntos + adhesivo)", mirror=True,
        edir=(0.4, 0, 1), dist=0.4, stage=6))
    A(V3.part(M, "BODY_CPillar_Lower_Nut_Plate", SYS, ["zinc"], [
        # contra el pilar C interior, por fuera del paso del mazo troncal de 48 V (x <= 0,786)
        box((0.802, -0.84, 0.56), (0.03, 0.10, 0.10), 0.003),
        rivet((0.787, -0.84, 0.56), (-1, 0, 0), 0.0048),
    ], "Placa {lado} de tuercas inferior del pilar C", mirror=True, edir=(1, -0.3, 0), dist=0.35, stage=6))
    A(V3.part(M, "BODY_Ramp_Bracket_CPillar", SYS, ["steel_black"], [
        hull([(0.786, -0.82, 0.62), (0.846, -0.82, 0.62), (0.786, -0.90, 0.62), (0.846, -0.90, 0.62),
              (0.786, -0.90, 0.78), (0.846, -0.90, 0.78)]),
    ], "Soporte de rampa {lado} del pilar C", mirror=True, edir=(1, -0.3, 0), dist=0.35, stage=6))
    A(V3.part(M, "BODY_Front_Quarter_Window_Frame", SYS, ["ecoat", "zinc"], [
        hull([(0.80, 1.40, 1.22), (0.84, 1.40, 1.22), (0.80, 1.62, 1.30), (0.84, 1.62, 1.30),
              (0.80, 1.40, 1.10), (0.84, 1.40, 1.10), (0.80, 1.62, 1.18), (0.84, 1.62, 1.18)]),
        line(rivet, (0.79, 1.42, 1.15), (0.79, 1.60, 1.24), 8, axis=(-1, 0, 0)),
    ], "Marco {lado} del vidrio fijo delantero de cuarto (8 remaches HS + 3 avellanados + 2 flow-form S18)",
        mirror=True, edir=(1, 0.4, 0.4), dist=0.4, stage=3))

    # Cabeceras de techo (acero; chapa soldada por puntos y pegada)
    A(V3.part(M, "BODY_Header_Front_Upper", SYS, ["ecoat", "zinc"], [
        beam((-0.72, 0.52, 1.715), (0.72, 0.52, 1.715), 0.05, 0.035, 0.003),
        line(rivet, (-0.60, 0.52, 1.735), (0.60, 0.52, 1.735), 12, axis=Z),
    ], "Cabecera delantera superior (4 avellanados largos + 12 flow-form S18)", edir=(0, 0.3, 1), dist=0.45,
        stage=3))
    A(V3.part(M, "BODY_Header_Front_Lower", SYS, ["ecoat"], [
        beam((-0.72, 0.52, 1.665), (0.72, 0.52, 1.665), 0.06, 0.03, 0.003),
    ], "Cabecera delantera inferior (soldadura por puntos y adhesivo)", edir=(0, 0.3, 0.6), dist=0.35, stage=3))
    A(V3.part(M, "BODY_Header_Front_Gusset", SYS, ["ecoat", "zinc"], [
        # bajo el extremo de la cabecera (z >= 1,65), a la que se remacha
        hull([(0.70, 0.50, 1.647), (0.76, 0.50, 1.647), (0.70, 0.56, 1.647), (0.76, 0.56, 1.647),
              (0.76, 0.50, 1.585), (0.76, 0.56, 1.585)]),
        line(rivet, (0.705, 0.52, 1.68), (0.745, 0.54, 1.68), 3, axis=Z, d=0.0048),
    ], "Cartela {lado} de la cabecera delantera", mirror=True, edir=(0.6, 0, 0.6), dist=0.35, stage=3))
    A(V3.part(M, "BODY_Header_Rear_Lower", SYS, ["ecoat", "zinc"], [
        beam((-0.74, -0.90, 1.60), (0.74, -0.90, 1.60), 0.05, 0.03, 0.003),
        line(rivet, (-0.60, -0.90, 1.617), (0.60, -0.90, 1.617), 10, axis=Z),
    ], "Cabecera trasera inferior (REAR WALL HEADER INNER; 6 remaches HS o 20 flow-form S18)",
        edir=(0, -0.4, 1), dist=0.45, stage=3))
    A(V3.part(M, "BODY_Header_Rear_Upper", SYS, ["ecoat", "zinc"], [
        beam((-0.76, -0.92, 1.635), (0.76, -0.92, 1.635), 0.06, 0.025, 0.003),
        line(rivet, (-0.65, -0.92, 1.65), (0.65, -0.92, 1.65), 16, axis=Z),
    ], "Cabecera trasera superior (32 flow-form S18)", edir=(0, -0.4, 1), dist=0.5, stage=3))

    # --- Pared trasera de la cabina ---------------------------------------------------------------------
    A(V3.part(M, "BODY_RearWall_Upper_Glove", SYS, ["ecoat", "zinc"], [
        # pegada a la pared trasera (y = -0,953), por detrás de los reposacabezas traseros
        box((0, -0.939, 1.42), (1.50, 0.028, 0.07), 0.004),
        line(rivet, (-0.66, -0.939, 1.458), (0.66, -0.939, 1.458), 11, axis=Z),
    ], "Funda del travesaño superior de la pared trasera (11 remaches HS + 3 FF S18 + 2 FF S38)",
        edir=(0, -1, 0.3), dist=0.55, stage=3))
    A(V3.part(M, "BODY_RearWall_Lower_Glove", SYS, ["ecoat", "zinc"], [
        box((0, -0.93, 0.735), (1.50, 0.05, 0.09), 0.004),
        line(rivet, (-0.68, -0.93, 0.78), (0.68, -0.93, 0.78), 12, axis=Z),
    ], "Funda del travesaño inferior de la pared trasera (24 remaches HS)", edir=(0, -1, -0.2), dist=0.55,
        stage=3))
    A(V3.part(M, "BODY_Rear_Seat_Stanchion", SYS, ["steel_black", "zinc"], [
        # contra la pared trasera (y = −0,955), por detrás del respaldo y por encima de la funda inferior
        box((0.45, -0.940, 0.95), (0.08, 0.026, 0.30), 0.004),
        beam((0.45, -0.940, 0.82), (0.62, -0.940, 1.00), 0.020, 0.04, 0.002),
        line(rivet, (0.45, -0.953, 0.82), (0.45, -0.953, 1.08), 7, axis=(0, -1, 0)),
    ], "Montante {lado} del asiento trasero y riostra (7 remaches HS + 1 de 4,8 mm; riostra 6 + 2)",
        mirror=True, edir=(0.4, -1, 0.3), dist=0.5, stage=3))
    A(V3.part(M, "BODY_Tonneau_Attachment_Bracket", SYS, ["steel_black", "zinc"], [
        # entre la pared delantera de la caja (y -0,997) y la pared trasera de la cabina (y -0,957), remachados a la
        # primera
        box((0.72, -0.977, 1.30), (0.06, 0.038, 0.10), 0.003),
        box((0.72, -0.977, 1.43), (0.06, 0.038, 0.07), 0.003),
        rivet((0.72, -0.997, 1.30), (0, -1, 0)), rivet((0.72, -0.997, 1.43), (0, -1, 0)),
    ], "Soportes {lado}s de fijación de la cubierta (inferior: 1 HS + 2 avellanados; superior: 3 HS + 1)",
        mirror=True, edir=(0.5, -0.5, 0.6), dist=0.4, stage=3))
    A(V3.part(M, "BODY_Bed_Bridge_Bracket", SYS, ["steel_black", "zinc"], [
        box((0, -1.10, 0.97), (0.42, 0.06, 0.07), 0.004),
        line(rivet, (-0.14, -1.10, 1.006), (0.14, -1.10, 1.006), 3, axis=Z),
    ], "Soporte del puente trasero de la caja (3 remaches HS)", edir=(0, -0.3, 1), dist=0.4, stage=3))
    A(V3.part(M, "BODY_Rear_Fascia_Bracket", SYS, ["steel_black", "zinc"], [
        # por fuera del extremo de los absorbedores traseros (|x| <= 0,662)
        box((0.72, -2.88, 0.60), (0.10, 0.06, 0.10), 0.003),
        line(rivet, (0.69, -2.915, 0.60), (0.75, -2.915, 0.60), 3, axis=(0, -1, 0)),
    ], "Soporte {lado} de la fascia trasera (3 remaches HS)", mirror=True, edir=(0.5, -1, 0), dist=0.4,
        stage=3))
    A(V3.part(M, "BODY_TieDown_Nut_Plate", SYS, ["zinc"], [
        box((0.74, -2.70, 0.868), (0.08, 0.08, 0.008), 0.002), box((0.74, -1.30, 0.868), (0.08, 0.08, 0.008), 0.002),
        rivet((0.74, -2.70, 0.872), Z, 0.0065), rivet((0.74, -1.30, 0.872), Z, 0.0065),
    ], "Placas {lado}s de tuercas de los anclajes de carga (1 avellanado estructural 6,5 mm)", mirror=True,
        edir=(0.3, 0, 1), dist=0.4, stage=6))
    A(V3.part(M, "BODY_Tailgate_Tower_Support_Plate", SYS, ["alu_machined", "zinc"], [
        box((0.80, -2.72, 0.98), (0.015, 0.12, 0.40), 0.002),
        line(rivet, (0.79, -2.72, 0.82), (0.79, -2.72, 1.14), 5, axis=(-1, 0, 0), d=0.0048),
    ], "Placa {lado} de soporte de la torre del portón (5 avellanados largos de 4,8 mm)", mirror=True,
        edir=(0.6, -0.6, 0.3), dist=0.4, stage=3))
    for s, sd in ((1, "R"), (-1, "L")):
        cy, cz, R = -1.8175, 0.437, 0.53
        path = [(s * 0.50, cy + R * math.cos(math.radians(a)), cz + R * math.sin(math.radians(a)))
                for a in range(10, 171, 20)]
        A(V3.part(M, f"BODY_Rear_Wheel_Arch_{sd}", SYS, ["ecoat", "zinc"], [
            sweep(path, 0.07, 0.012, 0.003, 4, up=(s, 0, 0)),
            line(rivet, path[1], path[-2], 5, axis=(-s, 0, 0)),
        ], f"Paso de rueda trasero {'derecho' if s > 0 else 'izquierdo'} (4 remaches HS + 5 de 4,8 mm + 2 avellanados)",
            edir=(s, -0.2, 0.7), dist=0.5, stage=3))
        A(V3.part(M, f"BODY_Rear_Wheel_Arch_Extension_{sd}", SYS, ["ecoat", "zinc"], [
            box((s * 0.55, -1.30, 0.80), (0.05, 0.12, 0.32), 0.003),
            line(rivet, (s * 0.52, -1.30, 0.68), (s * 0.52, -1.30, 0.92), 6, axis=(-s, 0, 0), d=0.0048),
        ], f"Extensión delantera del paso de rueda trasero {'derecho' if s > 0 else 'izquierdo'} (6 remaches de 4,8 mm)",
            edir=(s, 0.2, 0.5), dist=0.45, stage=3))

    # --- Tapones, almohadillas NVH y remaches por familia ---------------------------------------------
    plug = lambda p, ax: disc(p, ax, 0.0145, 0.004, 20, 0)
    A(V3.part(M, "BODY_Access_Plugs_1870761", SYS, ["plastic_black"], [
        plug((-0.20, 1.463, 0.53), Y), plug((0.20, 1.463, 0.53), Y),
        plug((0.45, -1.52, 0.58), Z), plug((-0.45, -1.52, 0.58), Z), plug((0.50, -2.30, 0.62), Z),
        plug((-0.50, -2.30, 0.62), Z),
        plug((0.84, 0.30, 0.74), X), plug((-0.84, 0.30, 0.74), X), plug((0.84, -0.40, 0.70), X),
    ], "Tapones de taladro de acceso Ø29 mm 1870761-00 (2 FUB, 4 RUB, 3 lateral) con sellante", edir=(0, 0, 1),
        dist=0.3, stage=6))
    A(V3.part(M, "BODY_NVH_Pads", SYS, ["rubber"], [
        box((0, 1.405, 0.95), (1.50, 0.012, 0.50), 0.003),
        box((0, 1.89, 1.18), (1.50, 0.02, 0.07), 0.003),
        box((0, -0.945, 1.00), (1.46, 0.012, 0.52), 0.003),
    ], "Almohadillas NVH (mamparo, cowl y pared trasera)", edir=(0, 0.6, 0.4), dist=0.35, stage=6))
    A(V3.part(M, "BODY_Rivets_Structural_6p5", SYS, ["zinc"], [
        line(rivet, (-0.52, 1.46, 0.60), (0.52, 1.46, 0.60), 15, axis=(0, -1, 0), d=0.0065),
        line(rivet, (-0.52, 1.46, 0.46), (0.52, 1.46, 0.46), 15, axis=(0, -1, 0), d=0.0065),
        line(rivet, (-0.62, -1.50, 0.62), (0.62, -1.50, 0.62), 15, axis=Z, d=0.0065),
        line(rivet, (-0.62, -2.20, 0.84), (0.62, -2.20, 0.84), 15, axis=Z, d=0.0065),
    ], "Remaches estructurales de 6,5 mm (HS 1454538-00-A) de las piezas fundidas", edir=(0, 0, -1), dist=0.3,
        stage=6))
    A(V3.part(M, "BODY_Rivets_Countersunk_4p8", SYS, ["zinc"], [
        line(rivet, (0.805, -0.88, 0.45), (0.805, 1.12, 0.45), 20, axis=(-1, 0, 0), d=0.0048),
        line(rivet, (-0.805, -0.88, 0.45), (-0.805, 1.12, 0.45), 20, axis=(1, 0, 0), d=0.0048),
    ], "Remaches avellanados de 4,8 mm (1028719-00-A) de laterales y soportes", edir=(0, 0, -1), dist=0.3,
        stage=6))
    A(V3.part(M, "BODY_Rivets_FlowForm_S18", SYS, ["zinc"], [
        line(rivet, (-0.60, -0.93, 1.50), (0.60, -0.93, 1.50), 14, axis=(0, -1, 0)),
        line(rivet, (-0.60, 0.52, 1.74), (0.60, 0.52, 1.74), 10, axis=Z),
        line(rivet, (0.76, 1.50, 1.27), (0.76, 1.58, 1.20), 4, axis=(-1, 0, 0)),
        line(rivet, (-0.76, 1.50, 1.27), (-0.76, 1.58, 1.20), 4, axis=(1, 0, 0)),
    ], "Remaches flow-form S18 (1069329-00-A; cuerpo y taladro Ø8 mm) de pared trasera, cabeceras y marcos",
        edir=(0, 0, 1), dist=0.3, stage=6))
    A(V3.part(M, "BODY_Rivets_SPR_5mm", SYS, ["zinc"], [
        line(rivet, (0.842, -0.80, 0.50), (0.842, 1.05, 0.50), 12, axis=(-1, 0, 0), d=0.0055),
        line(rivet, (-0.842, -0.80, 0.50), (-0.842, 1.05, 0.50), 12, axis=(1, 0, 0), d=0.0055),
    ], "Remaches autoperforantes SPR Ø5 (1026936-00-A y familia) en el anillo de puertas", edir=(0, 0, -1),
        dist=0.3, stage=6))
    # Soportes del absorbedor delantero (Support Bracket Center y LH/RH)
    A(V3.part(M, "BODY_Front_Energy_Absorber_Bracket_Center", SYS, ["alu_cast", "zinc"], [
        box((0, 2.49, 0.55), (0.30, 0.040, 0.14), 0.004),
        line(bolt, (-0.10, 2.468, 0.55), (0.10, 2.468, 0.55), 3, axis=(0, -1, 0), d=0.010),
    ], "Soporte central del absorbedor delantero", edir=(0, 1, 0), dist=0.5, stage=3))
    A(V3.part(M, "BODY_Front_Energy_Absorber_Bracket", SYS, ["alu_cast", "zinc"], [
        box((0.53, 2.44, 0.54), (0.12, 0.030, 0.12), 0.004),
        line(nut, (0.49, 2.42, 0.50), (0.57, 2.42, 0.58), 4, axis=(0, -1, 0), d=0.010, stud=0.0),
    ], "Soporte {lado} del absorbedor delantero (4 tuercas 13 mm a 30 N·m)", mirror=True, edir=(0.3, 1, 0),
        dist=0.5, stage=3))
    return [o for o in out if o is not None]
