"""Chasis, bajos, batería, tren motriz, suspensión y dirección del Cyberbeast.

[V] (manual del propietario, «Subsystems»): suspensión independiente de doble horquilla delante y
    detrás con muelle neumático, amortiguador adaptativo y barra estabilizadora; dirección por cable
    en las cuatro ruedas (actuadores delantero y trasero); motor delantero síncrono de imanes
    permanentes y dos motores de inducción traseros; relación 15,02:1; batería de iones de litio
    refrigerada por líquido de ~700 V nominales; batería de baja tensión de 48 V.
[V] (manual de servicio): subchasis delantero y trasero (tri-motor), módulos de muelle neumático,
    bieletas de estabilizadora, bieletas de convergencia traseras, intercambiador de calor de la
    unidad delantera, deflectores aerodinámicos y placas de protección inferiores.
[V]/[A] Batería: 1.344 celdas 4680 (Ø46 x 80 mm, 123 kWh), una sola capa organizada en módulos
    (desmontaje de Munro). Envolvente y distribución de módulos aproximadas.
[A] Geometría exacta de brazos, piezas fundidas y carcasas: reconstrucción plausible con escala y
    puntos de anclaje coherentes con ruedas, vías y alturas verificadas.
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L

FLOOR_Z = 0.505
WZ = S.WHEEL_CENTER_Z


def _obj(mb, name, system, mat, edir, dist, stage, group, label, fid="A", parent=None, smooth=35,
         bevel=0.0, note=None):
    o = mb.build(name, system, mat, parent=parent)
    L.set_smooth_by_angle(o, smooth)
    if bevel:
        L.bevel(o, bevel, 2, 40)
    L.explode(o, edir, dist, stage, group, label, fid, note=note)
    return o


def chamfer_box(mb, center, size, ch, mat=0):
    """Caja con aristas achaflanadas (24 caras) para carcasas fundidas."""
    cx, cy, cz = center
    sx, sy, sz = (s / 2 for s in size)
    pts = []
    import itertools
    verts = {}
    for dx, dy, dz in itertools.product((-1, 1), repeat=3):
        for ax in range(3):
            p = [dx * sx, dy * sy, dz * sz]
            q = [dx * sx, dy * sy, dz * sz]
            q[ax] -= [dx, dy, dz][ax] * ch
            verts[(dx, dy, dz, ax)] = (cx + q[0], cy + q[1], cz + q[2])
    import bmesh
    # se aproxima con la envolvente convexa de los 24 puntos
    bm = bmesh.new()
    for v in verts.values():
        bm.verts.new(v)
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.verts.index_update()
    for f in bm.faces:
        mb.face([tuple(v.co) for v in f.verts], mat, want=f.normal)
    bm.free()


def cylinder(mb, p0, p1, r, seg=24, mat=0, caps=True):
    p0, p1 = Vector(p0), Vector(p1)
    ax = p1 - p0
    L.lathe(mb, [(r, 0.0), (r, ax.length)], tuple(p0), tuple(ax.normalized()), seg, mat,
            cap_start=caps, cap_end=caps)


def arm(mb, a, b, w, h, mat=0):
    """Brazo de sección rectangular entre dos puntos (pieza de suspensión fundida/estampada)."""
    a, b = Vector(a), Vector(b)
    d = (b - a)
    u, v, wv = L.frame_from_axis(d)
    rot = Matrix((u, v, wv)).transposed()
    c = (a + b) / 2
    L.box(mb, tuple(c), (w, h, d.length), mat, rot=rot)


# ---------------------------------------------------------------------------
# Batería
# ---------------------------------------------------------------------------
def build_battery(M):
    objs = []
    y0, y1 = 1.25, -1.45
    hw = 0.80
    zb, zt = 0.285, 0.455
    asm = L.assembly("BATTERY_PACK", "BATTERY_ASSEMBLY", (0.0, (y0 + y1) / 2, (zb + zt) / 2))
    L.explode(asm, (0, 0, -1), 1.35, 5, "Batería",
              "Batería de alta tensión (~123 kWh, 1.344 celdas 4680, ~700 V)", "R")
    # Bandeja inferior (envolvente) y tapa superior
    mb = L.MeshBuilder()
    chamfer_box(mb, (0.0, (y0 + y1) / 2, zb + 0.055), (2 * hw, y0 - y1, 0.11), 0.03)
    objs.append(_obj(mb, "BAT_Enclosure_Tray", "BATTERY_ASSEMBLY", M["battery"], (0, 0, -1), 0.25, 6,
                     "Batería", "Bandeja estructural de la batería", parent=asm))
    mb = L.MeshBuilder()
    chamfer_box(mb, (0.0, (y0 + y1) / 2, zt - 0.006), (2 * hw - 0.02, y0 - y1 - 0.02, 0.012), 0.004)
    objs.append(_obj(mb, "BAT_Enclosure_Lid", "BATTERY_ASSEMBLY", M["battery"], (0, 0, 1), 0.55, 6,
                     "Batería", "Tapa superior de la batería", parent=asm))
    # Módulos de celdas 4680 (cuatro bloques de 336 celdas en disposición hexagonal)
    pitch_x, pitch_y = 0.0475, 0.0475 * math.sqrt(3) / 2
    nx, ny = 16, 21
    module_centers = [(-0.40, 0.48), (0.40, 0.48), (-0.40, -0.48), (0.40, -0.48)]
    yc0 = (y0 + y1) / 2
    for mi, (mx, my) in enumerate(module_centers):
        mb = L.MeshBuilder(merge=1e-7)
        for j in range(ny):
            for i in range(nx):
                x = mx + (i - (nx - 1) / 2) * pitch_x + (pitch_x / 2 if j % 2 else 0) - pitch_x / 4
                y = yc0 + my + (j - (ny - 1) / 2) * pitch_y
                z0 = zb + 0.035
                L.lathe(mb, [(S.CELL_D / 2, 0.0), (S.CELL_D / 2, S.CELL_H), (0.0, S.CELL_H + 0.001)],
                        (x, y, z0), (0, 0, 1), 8, 0)
        objs.append(_obj(mb, f"BAT_Module_{mi + 1}_Cells", "BATTERY_ASSEMBLY", M["cell"],
                         (mx, my, 0.4), 0.30, 6, "Batería",
                         f"Módulo {mi + 1}: 336 celdas cilíndricas 4680 (Ø46 x 80 mm)", "A", parent=asm,
                         note="Recuento total verificado (1.344); disposición en módulos aproximada"))
        # Barras colectoras de cobre sobre cada módulo
        mb = L.MeshBuilder()
        for j in range(0, ny, 3):
            y = yc0 + my + (j - (ny - 1) / 2) * pitch_y
            L.box(mb, (mx, y, zb + 0.035 + S.CELL_H + 0.004), (nx * pitch_x, 0.012, 0.003), 0)
        objs.append(_obj(mb, f"BAT_Module_{mi + 1}_Busbars", "BATTERY_ASSEMBLY", M["copper"],
                         (mx, my, 1), 0.42, 6, "Batería", "Barras colectoras del módulo", "A", parent=asm))
    # Travesaños interiores que separan los módulos
    mb = L.MeshBuilder()
    L.box(mb, (0.0, yc0, zb + 0.08), (0.04, y0 - y1 - 0.08, 0.10), 0)
    for yy in (yc0 + 1.02, yc0, yc0 - 1.02):
        L.box(mb, (0.0, yy, zb + 0.08), (2 * hw - 0.08, 0.04, 0.10), 0)
    objs.append(_obj(mb, "BAT_Internal_Beams", "BATTERY_ASSEMBLY", M["alu_cast"], (0, 0, 0.6), 0.35, 6,
                     "Batería", "Vigas internas entre módulos", parent=asm))
    # Unidad de conexión de alta tensión (delantera) y conectores
    mb = L.MeshBuilder()
    chamfer_box(mb, (0.0, y0 - 0.12, zt + 0.045), (0.60, 0.20, 0.09), 0.015)
    objs.append(_obj(mb, "BAT_HV_Junction", "BATTERY_ASSEMBLY", M["battery"], (0, 0.4, 1), 0.45, 6, "Batería",
                     "Caja de conexiones de alta tensión de la batería", parent=asm))
    return objs


# ---------------------------------------------------------------------------
# Unidades motrices y semiejes
# ---------------------------------------------------------------------------
def build_drive_units(M):
    objs = []
    yf, yr = S.Y_FRONT_AXLE, S.Y_REAR_AXLE
    # Delantera: un motor síncrono de imanes permanentes con reductora e inversor
    du = L.assembly("DRIVE_UNIT_FRONT", "DRIVE_UNITS", (0.0, yf, WZ))
    L.explode(du, (0, 0.6, -1), 1.1, 5, "Unidades motrices",
              "Unidad motriz delantera (motor síncrono de imanes permanentes)", "V")
    mb = L.MeshBuilder()
    cylinder(mb, (-0.30, yf + 0.16, WZ + 0.02), (0.06, yf + 0.16, WZ + 0.02), 0.125, 32)
    objs.append(_obj(mb, "DU_F_Motor_Housing", "DRIVE_UNITS", M["alu_cast"], (-1, 0.3, 0), 0.30, 6,
                     "Unidades motrices", "Carcasa del motor delantero", parent=du))
    mb = L.MeshBuilder()
    chamfer_box(mb, (0.08, yf + 0.02, WZ + 0.0), (0.24, 0.38, 0.30), 0.04)
    objs.append(_obj(mb, "DU_F_Gearbox", "DRIVE_UNITS", M["alu_cast"], (1, 0, 0), 0.25, 6,
                     "Unidades motrices", "Reductora de una velocidad (15,02:1) y diferencial", parent=du))
    mb = L.MeshBuilder()
    chamfer_box(mb, (-0.10, yf + 0.13, WZ + 0.20), (0.36, 0.24, 0.10), 0.02)
    objs.append(_obj(mb, "DU_F_Inverter", "DRIVE_UNITS", M["battery"], (0, 0, 1), 0.35, 6,
                     "Unidades motrices", "Inversor de la unidad delantera", parent=du))
    # Trasera: dos motores de inducción, cada uno con su reductora (vectorización de par)
    du_r = L.assembly("DRIVE_UNIT_REAR", "DRIVE_UNITS", (0.0, yr, WZ))
    L.explode(du_r, (0, -0.6, -1), 1.15, 5, "Unidades motrices",
              "Unidad motriz trasera con dos motores de inducción", "V")
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        cylinder(mb, (s * 0.03, yr - 0.17, WZ + 0.03), (s * 0.34, yr - 0.17, WZ + 0.03), 0.13, 32)
        objs.append(_obj(mb, f"DU_R_Motor_{sd}", "DRIVE_UNITS", M["alu_cast"], (s, -0.2, 0), 0.32, 6,
                         "Unidades motrices",
                         f"Motor de inducción trasero {'derecho' if s > 0 else 'izquierdo'}", "V", parent=du_r))
        mb = L.MeshBuilder()
        chamfer_box(mb, (s * 0.20, yr + 0.03, WZ), (0.22, 0.30, 0.28), 0.04)
        objs.append(_obj(mb, f"DU_R_Gearset_{sd}", "DRIVE_UNITS", M["alu_cast"], (s, 0.2, 0), 0.28, 6,
                         "Unidades motrices", "Engranaje reductor independiente (15,02:1)", "R", parent=du_r))
        mb = L.MeshBuilder()
        chamfer_box(mb, (s * 0.19, yr - 0.14, WZ + 0.21), (0.30, 0.26, 0.10), 0.02)
        objs.append(_obj(mb, f"DU_R_Inverter_{sd}", "DRIVE_UNITS", M["battery"], (s * 0.3, 0, 1), 0.36, 6,
                         "Unidades motrices", "Inversor de motor trasero", parent=du_r))
    # Semiejes con juntas homocinéticas
    for axle, y, sysname in (("F", yf, "DRIVE_UNITS"), ("R", yr, "DRIVE_UNITS")):
        for s, sd in ((1, "R"), (-1, "L")):
            mb = L.MeshBuilder()
            xi, xo = s * 0.24, s * 0.80
            cylinder(mb, (xi, y, WZ), (xo, y, WZ), 0.016, 16)
            for xc in (xi + s * 0.04, xo - s * 0.05):
                L.lathe(mb, [(0.02, -0.05), (0.045, -0.035), (0.038, -0.02), (0.046, -0.005), (0.038, 0.01),
                             (0.046, 0.025), (0.03, 0.05)], (xc, y, WZ), (s, 0, 0), 20, 1)
            o = mb.build(f"DU_Halfshaft_{axle}{sd}", sysname, [M["steel_black"], M["bushing"]])
            L.set_smooth_by_angle(o, 40)
            L.explode(o, (s, 0, -0.3), 0.55, 5, "Semiejes",
                      f"Semieje {'delantero' if axle == 'F' else 'trasero'} con juntas homocinéticas", "R")
            objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Suspensión de doble horquilla y dirección por cable
# ---------------------------------------------------------------------------
def build_corner(M, axle, s):
    objs = []
    y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
    sd = "R" if s > 0 else "L"
    sysname = "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION"
    fwd = 1 if axle == "F" else -1
    asm = L.assembly(f"SUSP_{axle}{sd}", sysname, (s * 0.65, y, WZ))
    L.explode(asm, (s, 0.0, 0.0), 0.55, 4, "Suspensión",
              f"Suspensión {'delantera' if axle == 'F' else 'trasera'} {'derecha' if s > 0 else 'izquierda'}", "R")
    lbj = Vector((s * 0.795, y, 0.255))
    ubj = Vector((s * 0.765, y - fwd * 0.02, 0.665))
    # Portamangueta (mangueta) con buje
    mb = L.MeshBuilder()
    arm(mb, lbj, ubj, 0.055, 0.075)
    cylinder(mb, (s * 0.78, y, WZ), (s * 0.885, y, WZ), 0.075, 28)
    arm(mb, (s * 0.80, y, WZ), (s * 0.78, y - fwd * 0.15, WZ - 0.02), 0.04, 0.05)
    objs.append(_obj(mb, f"SUS_{axle}{sd}_Knuckle", sysname, M["alu_cast"], (s, 0, 0.2), 0.35, 6, "Suspensión",
                     "Portamangueta de aluminio con buje y rodamiento", parent=asm, bevel=0.006))
    # Brazo inferior (horquilla en A) y brazo superior
    mb = L.MeshBuilder()
    for dy in (0.20, -0.20):
        arm(mb, (s * 0.36, y + dy, 0.31), lbj, 0.05, 0.035)
    arm(mb, (s * 0.36, y + 0.20, 0.31), (s * 0.36, y - 0.20, 0.31), 0.06, 0.04)
    for dy in (0.20, -0.20):
        L.lathe(mb, [(0.034, -0.03), (0.034, 0.03)], (s * 0.36, y + dy, 0.31), (0, 1, 0), 16, 1,
                cap_start=True, cap_end=True)
    lca = mb.build(f"SUS_{axle}{sd}_LowerArm", sysname, [M["alu_cast"], M["bushing"]], parent=asm)
    L.set_smooth_by_angle(lca, 40)
    L.bevel(lca, 0.006, 2, 40)
    L.explode(lca, (s, 0, -0.6), 0.32, 6, "Suspensión", "Brazo inferior (horquilla) de aluminio", "R")
    objs.append(lca)
    mb = L.MeshBuilder()
    for dy in (0.15, -0.15):
        arm(mb, (s * 0.50, y + dy, 0.70), ubj, 0.035, 0.028)
    lathe_pts = [(0.026, -0.025), (0.026, 0.025)]
    for dy in (0.15, -0.15):
        L.lathe(mb, lathe_pts, (s * 0.50, y + dy, 0.70), (0, 1, 0), 14, 1, cap_start=True, cap_end=True)
    uca = mb.build(f"SUS_{axle}{sd}_UpperArm", sysname, [M["alu_cast"], M["bushing"]], parent=asm)
    L.set_smooth_by_angle(uca, 40)
    L.explode(uca, (s, 0, 0.7), 0.30, 6, "Suspensión", "Brazo superior (horquilla)", "R")
    objs.append(uca)
    # Módulo de muelle neumático coaxial con amortiguador adaptativo
    bot = Vector((s * 0.64, y + fwd * 0.07, 0.30))
    top = Vector((s * 0.58, y + fwd * 0.10, 0.96))
    ax = (top - bot).normalized()
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.030, 0.0), (0.030, 0.30), (0.046, 0.30), (0.046, 0.33)], tuple(bot), tuple(ax), 20, 0,
            cap_start=True)
    L.lathe(mb, [(0.012, 0.30), (0.012, 0.48)], tuple(bot), tuple(ax), 12, 1)
    L.lathe(mb, [(0.050, 0.33), (0.082, 0.36), (0.088, 0.44), (0.082, 0.52), (0.060, 0.56), (0.060, 0.62),
                 (0.075, 0.64), (0.0, 0.66)], tuple(bot), tuple(ax), 28, 2)
    spring = mb.build(f"SUS_{axle}{sd}_AirSpring_Module", sysname, [M["steel_black"], M["chrome"], M["bushing"]],
                      parent=asm)
    L.set_smooth_by_angle(spring, 40)
    L.explode(spring, (s * 0.3, 0, 1), 0.55, 6, "Suspensión",
              "Módulo de muelle neumático con amortiguador adaptativo", "V")
    objs.append(spring)
    # Bieleta de la barra estabilizadora
    mb = L.MeshBuilder()
    cylinder(mb, (s * 0.60, y - fwd * 0.12, 0.32), (s * 0.56, y - fwd * 0.20, 0.50), 0.010, 10)
    o = _obj(mb, f"SUS_{axle}{sd}_StabLink", sysname, M["zinc"], (s, 0, 0.3), 0.35, 6, "Suspensión",
             "Bieleta de la barra estabilizadora", parent=asm)
    objs.append(o)
    # Bieleta de dirección (convergencia) hacia el actuador de dirección por cable
    mb = L.MeshBuilder()
    cylinder(mb, (s * 0.30, y - fwd * 0.14, WZ - 0.01), (s * 0.78, y - fwd * 0.15, WZ - 0.02), 0.012, 12)
    L.lathe(mb, [(0.0, 0.0), (0.022, 0.0), (0.022, 0.02), (0.0, 0.025)], (s * 0.78, y - fwd * 0.15, WZ - 0.02),
            (0, 0, 1), 12, 0)
    o = _obj(mb, f"STR_{axle}{sd}_TieRod", "STEERING", M["zinc"], (s, -fwd * 0.3, 0), 0.40, 6, "Dirección",
             "Bieleta de dirección" if axle == "F" else "Bieleta de convergencia (dirección trasera)", "R",
             parent=asm)
    objs.append(o)
    return objs


def build_suspension_and_steering(M):
    objs = []
    for axle in ("F", "R"):
        for s in (1, -1):
            objs += build_corner(M, axle, s)
        y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
        fwd = 1 if axle == "F" else -1
        sysname = "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION"
        # Barra estabilizadora
        mb = L.MeshBuilder()
        path = [(-0.56, y - fwd * 0.20, 0.50), (-0.48, y - fwd * 0.30, 0.52), (-0.30, y - fwd * 0.32, 0.56),
                (0.30, y - fwd * 0.32, 0.56), (0.48, y - fwd * 0.30, 0.52), (0.56, y - fwd * 0.20, 0.50)]
        L.tube(mb, path, 0.014, 12)
        o = _obj(mb, f"SUS_{axle}_StabilizerBar", sysname, M["steel_black"], (0, -fwd * 0.4, 0.3), 0.6, 4,
                 "Suspensión", "Barra estabilizadora", "V")
        objs.append(o)
        # Actuador de dirección (cremallera electromecánica sin unión mecánica con el volante)
        mb = L.MeshBuilder()
        cylinder(mb, (-0.32, y - fwd * 0.14, WZ - 0.01), (0.32, y - fwd * 0.14, WZ - 0.01), 0.032, 24)
        chamfer_box(mb, (0.10, y - fwd * 0.20, WZ + 0.02), (0.16, 0.12, 0.12), 0.02)
        for x in (-0.32, 0.32):
            L.lathe(mb, [(0.02, 0.0), (0.035, 0.02), (0.028, 0.04), (0.035, 0.06), (0.02, 0.08)],
                    (x, y - fwd * 0.14, WZ - 0.01), (1 if x > 0 else -1, 0, 0), 16, 1)
        o = mb.build(f"STR_{axle}_Actuator", "STEERING", [M["alu_cast"], M["bushing"]])
        L.set_smooth_by_angle(o, 40)
        L.explode(o, (0, -fwd, -0.5), 0.75, 4, "Dirección",
                  "Actuador de dirección delantero (steer-by-wire)" if axle == "F"
                  else "Actuador de dirección trasero (convergencia de las ruedas traseras)", "V")
        objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Estructura: subchasis, piezas fundidas, frunk, caja de carga y bajos
# ---------------------------------------------------------------------------
def build_structure(M):
    objs = []
    for axle, y, fwd in (("F", S.Y_FRONT_AXLE, 1), ("R", S.Y_REAR_AXLE, -1)):
        mb = L.MeshBuilder()
        for s in (1, -1):
            arm(mb, (s * 0.40, y + fwd * 0.48, 0.33), (s * 0.40, y - fwd * 0.45, 0.33), 0.08, 0.07)
        for dy in (0.42, 0.0, -0.40):
            arm(mb, (-0.40, y + fwd * dy, 0.31), (0.40, y + fwd * dy, 0.31), 0.06, 0.07)
        o = _obj(mb, f"CHS_Subframe_{axle}", "UNDERBODY", M["steel_black"], (0, fwd * 0.3, -1), 0.95, 3,
                 "Subchasis", f"Subchasis {'delantero' if axle == 'F' else 'trasero'}", "R", bevel=0.008)
        objs.append(o)
    # Piezas de fundición (gigacasting) delantera y trasera: largueros y torretas de suspensión
    for axle, y, fwd in (("F", S.Y_FRONT_AXLE, 1), ("R", S.Y_REAR_AXLE, -1)):
        mb = L.MeshBuilder()
        for s in (1, -1):
            arm(mb, (s * 0.62, y + fwd * 0.75, 0.62), (s * 0.62, y - fwd * 0.55, 0.62), 0.12, 0.16)
            chamfer_box(mb, (s * 0.58, y + fwd * 0.10, 0.92), (0.20, 0.26, 0.22), 0.04)
        arm(mb, (-0.62, y + fwd * 0.75, 0.62), (0.62, y + fwd * 0.75, 0.62), 0.10, 0.14)
        o = _obj(mb, f"BODY_Casting_{axle}", "BODY_STRUCTURE", M["alu_cast"], (0, fwd * 0.5, 0.4), 1.25, 3,
                 "Estructura de la carrocería",
                 f"Pieza fundida {'delantera' if axle == 'F' else 'trasera'} (largueros y torretas)", "A",
                 bevel=0.01, note="Arquitectura de piezas fundidas documentada públicamente; forma aproximada")
        objs.append(o)
    # Cubeta del maletero delantero (frunk, 200 l)
    mb = L.MeshBuilder()
    y0, y1, hw, zb, zt = 2.58, 1.98, 0.56, 0.74, 1.04
    rim = [(-hw, y0, zt), (hw, y0, zt), (hw, y1, zt + 0.15), (-hw, y1, zt + 0.15)]
    bot = [(-hw + 0.06, y0 - 0.05, zb), (hw - 0.06, y0 - 0.05, zb), (hw - 0.06, y1 + 0.04, zb), (-hw + 0.06, y1 + 0.04, zb)]
    mb.face(bot, 0, want=(0, 0, 1))
    for i in range(4):
        j = (i + 1) % 4
        q = [rim[i], rim[j], bot[j], bot[i]]
        c = sum((Vector(p) for p in q), Vector()) / 4
        mb.face(q, 0, want=Vector((0, 2.28, 0.95)) - c)
    o = _obj(mb, "BODY_Frunk_Tub", "BODY_STRUCTURE", M["composite"], (0, 0.5, 1), 1.05, 3,
             "Maletero delantero", "Cubeta del maletero delantero (200 l)", "R")
    L.solidify(o, 0.004)
    objs.append(o)
    # Intercambiador de calor delantero tras la rejilla inferior
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 2.47, 0.58), (0.90, 0.05, 0.26), 0)
    o = _obj(mb, "CHS_Heat_Exchanger_Front", "UNDERBODY", M["alu_cast"], (0, 1, 0), 0.8, 3, "Refrigeración",
             "Intercambiador de calor delantero", "A")
    objs.append(o)
    # Caja de carga compuesta con pasos de rueda y compartimento inferior (Gear locker)
    objs += build_cargo_bed(M)
    # Protecciones inferiores
    for nm, (y0, y1), lbl in (("Front", (2.35, 1.30), "Deflector aerodinámico delantero"),
                              ("Rear", (-1.48, -2.30), "Deflector aerodinámico trasero")):
        mb = L.MeshBuilder()
        L.box(mb, (0.0, (y0 + y1) / 2, 0.268), (1.30, abs(y0 - y1), 0.006), 0)
        o = _obj(mb, f"CHS_Aeroshield_{nm}", "UNDERBODY", M["plastic_textured"], (0, 0, -1), 0.6, 3,
                 "Bajos", lbl, "R")
        objs.append(o)
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -0.10, 0.278), (1.62, 2.62, 0.008), 0)
    o = _obj(mb, "CHS_Battery_Skid_Plate", "UNDERBODY", M["zinc"], (0, 0, -1), 1.75, 3, "Bajos",
             "Placa de protección inferior de la batería", "R")
    objs.append(o)
    # Cableado de alta tensión (naranja) y tubos de refrigerante
    mb = L.MeshBuilder()
    L.tube(mb, [(0.10, 1.13, 0.50), (0.10, 1.35, 0.55), (0.0, 1.60, 0.65), (-0.10, 1.75, 0.70)], 0.014, 10)
    L.tube(mb, [(-0.10, 1.13, 0.50), (-0.10, 1.35, 0.55), (-0.18, 1.60, 0.65), (-0.20, 1.80, 0.70)], 0.014, 10)
    L.tube(mb, [(0.0, -1.46, 0.40), (0.0, -1.55, 0.50), (0.12, -1.75, 0.66)], 0.014, 10)
    L.tube(mb, [(0.0, -1.46, 0.40), (0.0, -1.55, 0.50), (-0.12, -1.75, 0.66)], 0.014, 10)
    o = _obj(mb, "HV_Cables", "BATTERY_ASSEMBLY", M["hv_orange"], (0, 0, -1), 1.0, 5, "Alta tensión",
             "Cables de alta tensión entre batería e inversores", "A")
    objs.append(o)
    mb = L.MeshBuilder()
    L.tube(mb, [(0.35, 2.45, 0.50), (0.35, 2.10, 0.45), (0.30, 1.40, 0.47), (0.30, 1.25, 0.47)], 0.012, 10)
    L.tube(mb, [(-0.35, 2.45, 0.50), (-0.35, 2.10, 0.45), (-0.30, 1.90, 0.55)], 0.012, 10)
    L.tube(mb, [(0.28, -1.46, 0.42), (0.28, -1.60, 0.50), (0.25, -1.72, 0.55)], 0.012, 10)
    o = _obj(mb, "CHS_Coolant_Hoses", "UNDERBODY", M["hose"], (0, 0, -1), 0.7, 5, "Refrigeración",
             "Tubos de refrigerante (batería, inversores e intercambiador)", "A")
    objs.append(o)
    # Batería de baja tensión de 48 V y compresor de la suspensión neumática
    mb = L.MeshBuilder()
    chamfer_box(mb, (0.42, 1.55, 0.72), (0.20, 0.12, 0.16), 0.01)
    objs.append(_obj(mb, "LV_Battery_48V", "BATTERY_ASSEMBLY", M["plastic_black"], (1, 0.3, 0.3), 0.6, 5,
                     "Baja tensión", "Batería de baja tensión de 48 V", "A"))
    mb = L.MeshBuilder()
    cylinder(mb, (-0.55, 2.22, 0.50), (-0.30, 2.22, 0.50), 0.05, 20)
    chamfer_box(mb, (-0.42, 2.30, 0.50), (0.18, 0.08, 0.10), 0.01)
    objs.append(_obj(mb, "CHS_AirSuspension_Compressor", "UNDERBODY", M["alu_cast"], (-1, 0.5, 0), 0.6, 4,
                     "Suspensión", "Compresor de la suspensión neumática", "A"))
    return objs


def build_cargo_bed(M):
    objs = []
    y0, y1 = S.BED_FRONT_Y, S.BED_TAILGATE_INNER_Y
    zf = S.BED_FLOOR_Z
    hw_in = 0.80
    asm = L.assembly("CARGO_BED_TUB", "CARGO_BED", (0.0, (y0 + y1) / 2, zf))
    L.explode(asm, (0, -0.2, 1), 1.55, 3, "Caja de carga", "Caja de carga compuesta (6' x 4')", "R")
    mb = L.MeshBuilder()
    mb.face([(-hw_in, y0, zf), (hw_in, y0, zf), (hw_in, y1, zf), (-hw_in, y1, zf)], 0, want=(0, 0, 1))
    for i in range(1, 12):
        x = -hw_in + i * 2 * hw_in / 12
        L.box(mb, (x, (y0 + y1) / 2, zf + 0.006), (0.03, abs(y1 - y0) - 0.06, 0.012), 0)
    for sgn in (1, -1):
        wall = [(sgn * hw_in, y0, zf), (sgn * hw_in, y1, zf), (sgn * (hw_in + 0.05), y1, 1.30),
                (sgn * (hw_in + 0.05), y0, 1.60)]
        mb.face(wall, 0, want=(-sgn, 0, 0))
        # paso de rueda dentro de la caja (deja 1.295 mm libres entre ellos)
        wy0, wy1 = S.Y_REAR_AXLE + 0.48, S.Y_REAR_AXLE - 0.48
        xw = sgn * S.BED_FLOOR_WIDTH / 2
        pts = [(xw, wy0, zf), (xw, wy1, zf), (xw, wy1 - 0.06, zf + 0.10), (xw, wy1 - 0.03, zf + 0.26),
               (xw, wy0 + 0.03, zf + 0.26), (xw, wy0 + 0.06, zf + 0.10)]
        L.MeshBuilder.face(mb, pts, 0, want=(-sgn, 0, 0))
        top = [(xw, wy1 - 0.03, zf + 0.26), (xw, wy0 + 0.03, zf + 0.26),
               (sgn * hw_in, wy0 + 0.03, zf + 0.26), (sgn * hw_in, wy1 - 0.03, zf + 0.26)]
        mb.face(top, 0, want=(0, 0, 1))
    mb.face([(-hw_in, y0, zf), (hw_in, y0, zf), (hw_in, y0, 1.60), (-hw_in, y0, 1.60)], 0, want=(0, -1, 0))
    o = mb.build("CARGO_Bed_Tub", "CARGO_BED", M["composite"], parent=asm)
    L.solidify(o, 0.006)
    L.explode(o, (0, 0, 1), 0.05, 6, "Caja de carga", "Cubeta compuesta de la caja (sin necesidad de protector)", "R")
    objs.append(o)
    # Compartimento inferior (Gear Locker) bajo el suelo de la caja
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -2.52, zf - 0.13), (1.10, 0.60, 0.24), 0)
    o = mb.build("CARGO_Gear_Locker", "CARGO_BED", M["composite"], parent=asm)
    L.bevel(o, 0.01, 2, 40)
    L.explode(o, (0, 0, -1), 0.45, 6, "Caja de carga", "Compartimento inferior Gear Locker (97 l)", "R")
    objs.append(o)
    # Luces de la caja a lo largo de ambos laterales
    for sgn in (1, -1):
        mb = L.MeshBuilder()
        L.box(mb, (sgn * (hw_in + 0.02), (y0 + y1) / 2, 1.28), (0.006, abs(y1 - y0) - 0.2, 0.012), 0)
        o = mb.build(f"LGT_Bed_Strip_{'R' if sgn > 0 else 'L'}", "LIGHTING", M["led_white"], parent=asm)
        L.explode(o, (sgn, 0, 0.3), 0.25, 6, "Iluminación", "Luz lateral de la caja a lo largo", "R")
        objs.append(o)
    return objs


def build_all(M):
    out = []
    out += build_battery(M)
    out += build_drive_units(M)
    out += build_suspension_and_steering(M)
    out += build_structure(M)
    return out
