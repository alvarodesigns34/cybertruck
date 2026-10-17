"""Versión 3 · chasis: suspensión, dirección, frenos, ruedas, subchasis y circuito de aire.

Fuentes (docs/ficha-tecnica-piezas.md §3.3 y §3.4.1):
  [V] Denominación, cantidades y pares (CHS-xxx): manual de servicio (módulos de muelle, brazos, mangueta,
      pinzas, buje, sensores de altura, bloque de válvulas, depósito, compresor, actuadores de dirección).
  [R] Forma y puntos duros reconstruidos coherentes con los brazos, mangueta y buje de la versión 2; las
      fuentes públicas no publican la geometría de casquillos, topes ni rótulas.
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, ball, boot

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
CORNERS = (("FR", 1, 1), ("FL", -1, 1), ("RR", 1, -1), ("RL", -1, -1))
ES = {"FR": "delantera derecha", "FL": "delantera izquierda", "RR": "trasera derecha", "RL": "trasera izquierda"}


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def _bbox(name):
    import bpy
    bpy.context.view_layer.update()
    o = bpy.data.objects[name]
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))),
            Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))))


def _top(name, x, y, default):
    """Altura de la cara superior de un objeto en (x, y) por un rayo vertical descendente."""
    import bpy
    from mathutils.bvhtree import BVHTree
    o = bpy.data.objects[name]
    ev = o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    mw = ev.matrix_world
    tree = BVHTree.FromPolygons([mw @ v.co for v in me.vertices], [p.vertices[:] for p in me.polygons])
    ev.to_mesh_clear()
    hit = tree.ray_cast(Vector((x, y, 5.0)), Vector((0, 0, -1)))[0]
    return default if hit is None else hit.z


def build(M):
    out = []
    A = out.extend
    cy_axle = S.Y_FRONT_AXLE

    for tag, s, f in CORNERS:
        ax = "F" if f > 0 else "R"
        sus = "FRONT_SUSPENSION" if f > 0 else "REAR_SUSPENSION"
        whl = "FRONT_WHEELS_AND_BRAKES" if f > 0 else "REAR_WHEELS_AND_BRAKES"
        cy = f * cy_axle
        es = ES[tag]
        # Sensor de altura (rótula de varilla al brazo superior; 1 tuerca 15 mm a 50 N·m)
        A(V3.part(M, f"SUS_{tag}_RideHeightSensor", sus, ["plastic_black", "zinc"], [
            box((s * 0.50, cy - f * 0.04, 0.745), (0.05, 0.035, 0.040), 0.004),
            cyl((s * 0.50, cy - f * 0.04, 0.725), (s * 0.55, cy - f * 0.04, 0.680), 0.003, seg=8, m=1),
            ball((s * 0.55, cy - f * 0.04, 0.680), (0, 0, -1), 0.007, 1, 0),
            nut((s * 0.50, cy - f * 0.04, 0.765), Z, 0.008, 1, 0.5),
        ], f"Sensor de altura {es} con varilla articulada al brazo superior (1 tuerca 15 mm a 50 N·m)",
            edir=(s, 0, 0.3), dist=0.4))
        # Tope de rebote y asiento del muelle neumático
        A(V3.part(M, f"SUS_{tag}_BumpStop_SpringSeat", sus, ["rubber", "steel_black"], [
            cyl((s * 0.61, cy + f * 0.02, 0.56), (s * 0.61, cy + f * 0.02, 0.64), 0.032, 0.022, 16, 0),
            ring((s * 0.61, cy, 0.385), Z, 0.040, 0.062, 0.016, 24, 1),
        ], f"Tope de rebote y asiento del muelle neumático {es}", edir=(s, 0, 0.2), dist=0.35))
        # Rótulas (superior e inferior) del portamanguetas
        A(V3.part(M, f"SUS_{tag}_BallJoints", sus, ["steel_black", "bushing"], [
            ball((s * 0.80, cy, 0.665), (0, 0, 1), 0.022, 0, 1),
            ball((s * 0.80, cy, 0.315), (0, 0, -1), 0.026, 0, 1),
        ], f"Rótulas superior e inferior de la mangueta {es} (tuercas 18 mm a 80 N·m y 24 mm a 190 N·m)",
            edir=(s, 0, 0.1), dist=0.4))
        # Casquillos de los brazos (pivotes a lo largo de Y)
        A(V3.part(M, f"SUS_{tag}_ArmBushings", sus, ["bushing", "steel_black"], [
            ring((s * 0.46, cy - f * 0.215, 0.675), Y, 0.010, 0.026, 0.070, 20, 0),
            ring((s * 0.46, cy + f * 0.395, 0.675), Y, 0.010, 0.026, 0.070, 20, 0),
            ring((s * 0.34, cy - f * 0.205, 0.295), Y, 0.012, 0.030, 0.075, 20, 0),
            ring((s * 0.34, cy + f * 0.355, 0.295), Y, 0.012, 0.030, 0.075, 20, 0),
        ], f"Casquillos de los brazos superior e inferior {es}", edir=(-s, 0, 0.1), dist=0.4))
        # Semieje: juntas homocinéticas y fuelles
        A(V3.part(M, f"DU_Halfshaft_{tag}_Joints_Boots", "DRIVE_UNITS", ["steel_black", "rubber", "zinc"], [
            cyl((s * 0.27, cy, 0.44), (s * 0.31, cy, 0.44), 0.048, seg=20, m=0),
            boot((s * 0.31, cy, 0.44), (s * 0.43, cy, 0.44), 0.046, 0.026, 5, 20, 1),
            cyl((s * 0.74, cy, 0.44), (s * 0.78, cy, 0.44), 0.050, seg=20, m=0),
            boot((s * 0.63, cy, 0.44), (s * 0.74, cy, 0.44), 0.026, 0.046, 5, 20, 1),
            nut((s * 0.835, cy, 0.44), X, 0.024, 2, 0.0),
        ], f"Juntas homocinéticas y fuelles del semieje {es} (perno central 24 mm a 300 N·m, siempre nuevo)",
            edir=(s, 0, 0), dist=0.5))
        # Espárragos de rueda (6 × M14×1,5 sobre Ø139,7 mm)
        studs = []
        for k in range(6):
            a = 2 * math.pi * k / 6
            yy, zz = cy + 0.0699 * math.cos(a), 0.437 + 0.0699 * math.sin(a)
            studs.append(cyl((s * 0.935, yy, zz), (s * 0.985, yy, zz), 0.007, seg=10, m=0))
        A(V3.part(M, f"WHL_{tag}_Studs", whl, ["steel_black"], [studs],
                  f"Espárragos M14×1,5 de la rueda {es} (6 uds., tuercas de 21 mm a 205 N·m)",
                  edir=(s, 0, 0), dist=0.45, stage=6))
        # Contrapesos de equilibrado
        A(V3.part(M, f"WHL_{tag}_BalanceWeights", whl, ["steel_bare"], [
            box((s * 0.80, cy, 0.437 + 0.232), (0.030, 0.050, 0.006), 0.001),
            box((s * 0.80, cy, 0.437 - 0.232), (0.030, 0.050, 0.006), 0.001),
        ], f"Contrapesos adhesivos de equilibrado de la rueda {es}", edir=(s, 0, 0), dist=0.3, stage=6))
        # Purgador, botas y muelles de retorno de la pinza
        # se colocan sobre la cara superior de la pinza (rayo vertical), no a cotas fijas que caían en el disco
        cmn, cmx = _bbox(f"BRK_{tag}_Caliper")
        ycal = (cmn.y + cmx.y) / 2
        xb = s * (min(abs(cmn.x), abs(cmx.x)) + 0.022)          # mitad interior de la pinza (cilindros)
        zb = _top(f"BRK_{tag}_Caliper", xb, ycal, cmx.z) - 0.003
        xs = (cmn.x + cmx.x) / 2
        zs = [_top(f"BRK_{tag}_Caliper", xs, ycal + d, cmx.z) for d in (-0.03, 0.03)]
        A(V3.part(M, f"BRK_{tag}_Caliper_Service_Parts", whl, ["zinc", "rubber"], [
            cyl((xb, ycal, zb), (xb, ycal, zb + 0.020), 0.006, 0.004, 8, 0),
            cyl((xb, ycal, zb + 0.020), (xb, ycal, zb + 0.032), 0.008, seg=10, m=1),
            box((xs, ycal - 0.03, zs[0] + 0.0025), (0.050, 0.010, 0.004), 0.001),
            box((xs, ycal + 0.03, zs[1] + 0.0025), (0.050, 0.010, 0.004), 0.001),
        ], f"Purgador con capuchón, botas y muelles de retorno de la pinza {es}", edir=(s, 0, 0.3), dist=0.4,
            stage=6))
        # Extremo exterior de la bieleta de dirección (rótula y contratuerca)
        ty = f * 1.65
        A(V3.part(M, f"STR_{tag}_TieRod_End", "STEERING", ["steel_black", "zinc"], [
            ball((s * 0.815, ty, 0.41), (s, 0, 0), 0.016, 0, 1),
            nut((s * 0.78, ty, 0.41), X, 0.016, 1, 0.0),
        ], f"Extremo exterior de la bieleta de dirección {es} (contratuerca 24 mm a 90 N·m, tuerca a mangueta 170 N·m)",
            edir=(s, 0, -0.1), dist=0.45))
        if f < 0:
            # el motor EPB forma parte de la malla de la pinza trasera; aquí, su conector y su mazo, por debajo
            # del brazo superior (z >= 0,618) y por dentro de él (x < 0,439) hasta el bastidor
            A(V3.part(M, f"BRK_{tag}_EPB_Motor", whl, ["steel_black", "plastic_black"], [
                box((s * 0.725, cy + 0.14, 0.57), (0.030, 0.030, 0.020), 0.003, 1),
                hose([(s * 0.725, cy + 0.14, 0.57), (s * 0.60, cy + 0.16, 0.585), (s * 0.45, cy + 0.15, 0.60),
                      (s * 0.40, cy + 0.15, 0.78)], 0.0035, 6, 4, 0),
            ], f"Conector y mazo del motor del freno de estacionamiento eléctrico (EPB) de la pinza {es}",
                edir=(s, 0, 0.5), dist=0.45))

    # --- Ejes: estabilizadoras, subchasis, tornillería ---------------------------------------------------------
    for ax, f, sus in (("F", 1, "FRONT_SUSPENSION"), ("R", -1, "REAR_SUSPENSION")):
        yb = f * 1.60
        A(V3.part(M, f"SUS_{ax}_Stabilizer_Bushings", sus, ["bushing", "steel_black", "zinc"], [
            ring((0.43, yb, 0.37), X, 0.014, 0.027, 0.045, 20, 0), ring((-0.43, yb, 0.37), X, 0.014, 0.027, 0.045, 20, 0),
            box((0.43, yb, 0.403), (0.050, 0.040, 0.012), 0.002, 1), box((-0.43, yb, 0.403), (0.050, 0.040, 0.012), 0.002, 1),
            bolt((0.43, yb, 0.409), Z, 0.008, 2), bolt((-0.43, yb, 0.409), Z, 0.008, 2),
        ], f"Casquillos y abrazaderas de la barra estabilizadora {'delantera' if f > 0 else 'trasera'} (4 pernos 15 mm a 50 N·m)",
            edir=(0, f * 0.2, -0.6), dist=0.4))
        A(V3.part(M, f"SUS_{ax}_Ankle_Catchers", sus, ["steel_black", "zinc"], [
            box((0.62, f * 1.75, 0.29), (0.07, 0.07, 0.022), 0.003), box((-0.62, f * 1.75, 0.29), (0.07, 0.07, 0.022), 0.003),
            bolt((0.62, f * 1.75, 0.301), Z, 0.018, 1), bolt((-0.62, f * 1.75, 0.301), Z, 0.018, 1),
        ], f"«Ankle catchers» de las bieletas estabilizadoras {'delanteras' if f > 0 else 'traseras'} (4 pernos 18 mm a 110 N·m)",
            edir=(0, 0, -1), dist=0.4, stage=6))
        zs = 0.47
        bolts = [bolt((sx * 0.46, f * yy, zs), Z, 0.022, 1) for sx in (1, -1) for yy in (1.40, 2.22)]
        bolts += [bolt((sx * 0.50, f * yy, zs), Z, 0.022, 1) for sx in (1, -1) for yy in (1.62, 2.02)]
        A(V3.part(M, f"CHS_Subframe_{ax}_Bolts", sus, ["zinc"], [bolts],
                  f"Pernos del subchasis {'delantero' if f > 0 else 'trasero'} (8 principales; 24 mm 215–355 N·m)",
                  edir=(0, 0, 1), dist=0.35, stage=6))
        A(V3.part(M, f"CHS_Subframe_{ax}_Ground_Strap", sus, ["copper", "zinc"], [
            hose([(0.30, f * 1.45, 0.44), (0.25, f * 1.52, 0.50), (0.18, f * 1.58, 0.46)], 0.004, 8, 4, 0),
            bolt((0.30, f * 1.45, 0.44), Z, 0.010, 1), bolt((0.18, f * 1.58, 0.46), Z, 0.010, 1),
        ], f"Cinta de masa del subchasis {'delantero' if f > 0 else 'trasero'} (1 perno 10 mm a 10 N·m)",
            edir=(0, f * 0.3, -0.5), dist=0.3, stage=6))
    A(V3.part(M, "CHS_Subframe_R_Locating_Pins", "REAR_SUSPENSION", ["steel_bare"], [
        cyl((0.48, -1.38, 0.30), (0.48, -1.38, 0.265), 0.008, 0.004, 10, 0),
        cyl((-0.48, -1.38, 0.30), (-0.48, -1.38, 0.265), 0.008, 0.004, 10, 0),
        cyl((0.0, -2.26, 0.30), (0.0, -2.26, 0.265), 0.008, 0.004, 10, 0),
    ], "Clavijas de posicionado del subchasis trasero (3 uds.)", edir=(0, 0, -1), dist=0.3, stage=6))

    # --- Circuito de aire de la suspensión ------------------------------------------------------------------------
    A(V3.part(M, "CHS_Air_Compressor_Carrier", "REAR_SUSPENSION", ["steel_black", "zinc", "rubber"], [
        box((-0.31, -2.285, 0.388), (0.38, 0.14, 0.012), 0.003),
        line(nut, (-0.46, -2.285, 0.394), (-0.16, -2.285, 0.394), 3, axis=Z, d=0.010, stud=0.0),
        cyl((-0.31, -2.34, 0.46), (-0.31, -2.40, 0.46), 0.018, 0.012, 14, 2),
    ], "Soporte del compresor de aire (3 tuercas 13 mm a 12 N·m) y conducto de escape", edir=(0, -0.3, -1),
        dist=0.4))
    A(V3.part(M, "CHS_Air_Compressor_Exhaust", "REAR_SUSPENSION", ["rubber", "plastic_black"], [
        hose([(-0.30, -2.34, 0.47), (-0.30, -2.47, 0.40), (-0.12, -2.55, 0.34)], 0.010, 10, 4, 0),
        cyl((-0.12, -2.55, 0.34), (-0.02, -2.55, 0.34), 0.026, seg=14, m=1),
    ], "Escape y silenciador del compresor de aire (collar a presión)", edir=(0, -1, -0.3), dist=0.4, stage=6))
    A(V3.part(M, "CHS_SCUBA_Valve_Block", "REAR_SUSPENSION", ["alu_machined", "valve_brass", "zinc"], [
        box((0.52, -2.30, 0.50), (0.09, 0.07, 0.07), 0.004),
        cyl((0.52, -2.30, 0.535), (0.52, -2.30, 0.575), 0.012, seg=12, m=1),
        line(nut, (0.48, -2.335, 0.50), (0.56, -2.335, 0.50), 3, axis=(0, -1, 0), d=0.010, stud=0.0),
    ], "Bloque de válvulas SCUBA y puerto de llenado del pack presurizado (racores VOSS 12 mm a 8 N·m)",
        edir=(0.5, -0.4, -0.3), dist=0.4))
    A(V3.part(M, "CHS_Air_Fill_Port", "REAR_SUSPENSION", ["valve_brass", "plastic_black"], [
        cyl((-0.55, -2.45, 0.50), (-0.55, -2.45, 0.54), 0.010, seg=12, m=0),
        cyl((-0.55, -2.45, 0.54), (-0.55, -2.45, 0.56), 0.012, seg=12, m=1),
    ], "Puerto de llenado de aire con tapón", edir=(0, -0.3, -1), dist=0.3, stage=6))
    for nm, es, pts in (
            # salen de la cara delantera del bloque de válvulas; por fuera del inversor trasero, por dentro de la
            # rueda trasera y bajo el umbral (z = 0,283), junto a las líneas de freno
            ("Rear", "trasero", [(0.43, -2.267, 0.50), (0.50, -2.20, 0.50), (0.56, -2.05, 0.56), (0.58, -1.92, 0.60)]),
            # puntos de control densos bajo el umbral para que la curva no baje de la altura libre oficial
            ("R", "derecho", [(0.415, -2.267, 0.50), (0.50, -2.12, 0.42), (0.58, -1.70, 0.33), (0.62, -1.50, 0.31),
                              (0.66, -1.30, 0.296), (0.78, -1.15, 0.289), (0.895, -1.00, 0.2855),
                              (0.895, -0.50, 0.2855), (0.895, 0.0, 0.2855), (0.895, 0.60, 0.2855),
                              (0.89, 1.10, 0.288), (0.88, 1.30, 0.30), (0.78, 1.55, 0.42), (0.66, 1.80, 0.62)]),
            ("L", "izquierdo", [(0.345, -2.267, 0.50), (0.10, -2.22, 0.45), (-0.20, -2.20, 0.45), (-0.50, -2.12, 0.42),
                                (-0.58, -1.70, 0.33), (-0.62, -1.50, 0.31), (-0.66, -1.30, 0.296),
                                (-0.78, -1.15, 0.289), (-0.895, -1.00, 0.2855), (-0.895, -0.50, 0.2855),
                                (-0.895, 0.0, 0.2855), (-0.895, 0.60, 0.2855), (-0.89, 1.10, 0.288),
                                (-0.88, 1.30, 0.30), (-0.78, 1.55, 0.42), (-0.66, 1.80, 0.62)])):
        A(V3.part(M, f"CHS_Air_Line_Bundle_{nm}", "REAR_SUSPENSION", ["hose", "zinc"], [
            hose(pts, 0.0045, 8, 5, 0, zmin=0.282),
            [nut(p, Z, 0.012, 1, 0.0) for p in (pts[0], pts[-1])],
        ], f"Haz de líneas de aire {es} (racores VOSS codificados por color)", edir=(0, 0, -1), dist=0.3,
            stage=6))
    A(V3.part(M, "CHS_Air_Inlet_Valve_Block", "REAR_SUSPENSION", ["alu_machined", "valve_brass"], [
        box((0.38, -2.40, 0.50), (0.07, 0.05, 0.05), 0.004),
        cyl((0.38, -2.40, 0.525), (0.38, -2.40, 0.560), 0.010, seg=12, m=1),
    ], "Bloque de válvula de admisión de aire (racor VOSS a 4 N·m)", edir=(0.3, -0.5, -0.3), dist=0.35, stage=6))
    A(V3.part(M, "CHS_VOSS_Fittings", "REAR_SUSPENSION", ["valve_brass", "zinc"], [
        [cyl((x, y, z), (x, y, z + 0.022), 0.007, seg=10, m=0) for (x, y, z) in
         ((0.61, 1.92, 0.945), (-0.61, 1.92, 0.945), (0.62, -1.92, 0.865), (-0.62, -1.92, 0.865),
          (0.60, 1.88, 0.60), (-0.60, 1.88, 0.60), (0.60, -1.88, 0.53), (-0.60, -1.88, 0.53),
          # sobre la generatriz superior del depósito (r = 66 mm) y en la tapa del bloque de válvulas
          (-0.05, -2.36, 0.567), (0.05, -2.36, 0.567), (0.15, -2.36, 0.567), (0.25, -2.36, 0.567),
          (0.345, -2.30, 0.561), (0.37, -2.30, 0.561), (0.395, -2.30, 0.561), (0.42, -2.30, 0.561))],
        [nut((x, y, z), Z, 0.014, 1, 0.0) for (x, y, z) in
         ((0.61, 1.92, 0.945), (-0.61, 1.92, 0.945), (0.62, -1.92, 0.865), (-0.62, -1.92, 0.865))],
    ], "Racores VOSS del sistema de aire (≥ 16 uds., 2–8 N·m)", edir=(0, 0, 1), dist=0.3, stage=6))

    # --- Dirección y frenos: soportes, sensores y mazos ------------------------------------------------------------
    for ax, f in (("F", 1), ("R", -1)):
        A(V3.part(M, f"STR_{ax}_Actuator_Controller", "STEERING", ["plastic_black", "connector_grey", "zinc"], [
            box((0.20, f * 1.59, 0.545), (0.18, 0.14, 0.050), 0.004),
            box((-0.20, f * 1.59, 0.545), (0.18, 0.14, 0.050), 0.004),
            [box((x, f * 1.59, 0.578), (0.030, 0.020, 0.018), 0.002, 1) for x in (-0.28, -0.24, 0.24, 0.28)],
            [bolt((x, f * 1.65, 0.572), Z, 0.008, 2) for x in (-0.12, 0.12)],
        ], f"Controladores y sensores de posición triple redundantes del actuador de dirección "
           f"{'delantero' if f > 0 else 'trasero'} (4 conectores con bloqueo)", edir=(0, f * 0.2, 1), dist=0.45))
    A(V3.part(M, "STR_Steering_Jumper_Harness", "STEERING", ["harness", "connector_grey"], [
        hose([(-0.39, 0.98, 0.88), (-0.42, 1.20, 0.70), (-0.38, 1.40, 0.56), (-0.20, 1.50, 0.52)], 0.007, 8, 5, 0),
        box((-0.39, 0.98, 0.88), (0.025, 0.020, 0.020), 0.002, 1),
    ], "Mazo puente de la dirección (Harness - Steering Jumper)", edir=(0, 0, 1), dist=0.3, stage=6))
    A(V3.part(M, "STR_Rear_Steer_Jumper_Harness", "STEERING", ["harness", "connector_grey"], [
        hose([(0.46, -0.98, 0.46), (0.30, -1.30, 0.34), (0.10, -1.50, 0.40), (0.20, -1.55, 0.52)], 0.006, 8, 5, 0),
    ], "Mazo puente de la dirección trasera (Harness - Jumper - Rear Steer)", edir=(0, 0, -1), dist=0.3, stage=6))
    A(V3.part(M, "BRK_HCU_Bracket", "UNDERBODY", ["steel_black", "zinc"], [
        box((0.46, 2.205, 0.585), (0.14, 0.22, 0.015), 0.003),
        box((0.395, 2.205, 0.64), (0.012, 0.22, 0.12), 0.002),
        line(bolt, (0.42, 2.12, 0.60), (0.50, 2.29, 0.60), 3, axis=Z, d=0.010),
    ], "Soporte de la unidad hidráulica (HCU) del ABS/ESC", edir=(0.2, 0.3, -1), dist=0.4))
    A(V3.part(M, "BRK_Pedal_Support_Bracket", "INTERIOR_CONTROLS", ["steel_black", "zinc"], [
        box((-0.44, 1.30, 0.58), (0.16, 0.12, 0.030), 0.003),
        beam((-0.44, 1.36, 0.60), (-0.44, 1.32, 0.88), 0.07, 0.020, 0.002),
        line(nut, (-0.50, 1.30, 0.60), (-0.38, 1.30, 0.60), 2, axis=Z, d=0.013, stud=0.0),
    ], "Soporte de los pedales (acelerador: 2 tuercas 13 mm a 10 N·m)", edir=(0, 0.4, -0.6), dist=0.4, stage=2))
    return [o for o in out if o is not None]
