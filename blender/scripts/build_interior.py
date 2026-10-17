"""Habitáculo del Cybertruck (decoración Tactical Grey).

Cotas de referencia [V] (manual): altura libre delantera 1058,8 mm y trasera 991,9 mm;
espacio para piernas 1043,6 / 1038,8 mm; anchura a la altura de hombros 1608,0 / 1576,4 mm;
anchura a la altura de cadera 1453,3 mm. Pantalla central 18,5" y trasera 9,4".

Derivaciones [R]: punto H delantero (0,30; 0,80) y trasero (-0,70; 0,77) en (Y, Z), obtenidos de
la altura libre (criterio SAE con 102 mm de holgura) y del techo del modelo.
Formas de asientos, salpicadero y consola reconstruidas a partir de fotografías; los mecanismos
internos de los asientos no se modelan (no visibles) [A].
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L
import build_body as B

FLOOR_Z = 0.505
H_FRONT = (0.30, 0.80)
H_REAR = (-0.63, 0.77)       # adelantado 7 cm en la v4: ni atraviesa la pared trasera ni choca con la consola
REAR_TILT = 15               # reclinado del respaldo trasero (grados)
SEAT_X = 0.395            # semiseparación de los asientos delanteros
WHEEL_C = (-0.395, 0.735, 1.02)


def rot_x(deg):
    return Matrix.Rotation(math.radians(deg), 3, "X")


def soft_box(name, system, mat, center, size, bevel_w=0.025, segments=3, rot=None, parent=None,
             edir=(0, 0, 1), dist=0.2, stage=2, group="Interior", label=None, fid="R"):
    mb = L.MeshBuilder()
    L.box(mb, center, size, 0, rot=rot)
    obj = mb.build(name, system, mat, parent=parent)
    L.bevel(obj, bevel_w, segments, 60, harden=False)
    m = obj.modifiers[-1]
    m.limit_method = "NONE"
    for p in obj.data.polygons:
        p.use_smooth = True
    L.explode(obj, edir, dist, stage, group, label or name, fid)
    return obj


# ---------------------------------------------------------------------------
# Estructura interior de la cabina (suelo, salpicadero estructural, pared trasera)
# ---------------------------------------------------------------------------
def build_cabin_shell(M):
    objs = []
    # Suelo del habitáculo (sobre la batería estructural)
    mb = L.MeshBuilder()
    y0, y1 = 1.40, -0.955
    hw = 0.86
    mb.face([(-hw, y0, FLOOR_Z - 0.02), (hw, y0, FLOOR_Z - 0.02), (hw, y1, FLOOR_Z - 0.02), (-hw, y1, FLOOR_Z - 0.02)],
            0, want=(0, 0, 1))
    floor = mb.build("BODY_Cabin_Floor", "BODY_STRUCTURE", M["ecoat"])
    L.solidify(floor, 0.004)
    L.explode(floor, (0, 0, -1), 0.30, 3, "Estructura de la cabina", "Suelo de la cabina", "A")
    objs.append(floor)
    # Mamparo delantero (salpicadero estructural) y túnel de reposapiés
    mb = L.MeshBuilder()
    yd = 1.42
    prof = [(FLOOR_Z - 0.02, yd - 0.02), (0.70, yd + 0.02), (0.95, yd + 0.10), (1.15, yd + 0.30), (1.24, 1.80)]
    for (za, ya), (zb, yb) in zip(prof, prof[1:]):
        mb.face([(-0.86, ya, za), (0.86, ya, za), (0.86, yb, zb), (-0.86, yb, zb)], 0, want=(0, -1, 0.3))
    fw = mb.build("BODY_Firewall", "BODY_STRUCTURE", M["ecoat"])
    L.solidify(fw, 0.004)
    L.explode(fw, (0, 1, 0), 0.35, 3, "Estructura de la cabina", "Mamparo delantero (salpicadero)", "A")
    objs.append(fw)
    # Pared trasera de la cabina con ventana trasera eléctrica
    yr = S.CAB_REAR_Y - 0.035
    mb = L.MeshBuilder()
    zt = S.z_top(yr) - 0.03
    hw_top = S.hw_glass(yr, zt) - 0.02
    pts = [(-0.86, yr, FLOOR_Z - 0.02), (0.86, yr, FLOOR_Z - 0.02), (0.86, yr, 1.30), (hw_top, yr, zt),
           (-hw_top, yr, zt), (-0.86, yr, 1.30)]
    mb.face(pts, 0, want=(0, 1, 0))
    wall = mb.build("BODY_Cabin_RearWall", "BODY_STRUCTURE", M["ecoat"])
    L.solidify(wall, 0.004)
    L.explode(wall, (0, -1, 0), 0.30, 3, "Estructura de la cabina", "Pared trasera de la cabina", "A")
    objs.append(wall)
    mb = L.MeshBuilder()
    L.box(mb, (0.0, yr - 0.006, 1.42), (1.10, 0.006, 0.20), 0)
    rw = mb.build("GLS_Rear_Window", "GLASS_AND_MIRRORS", M["glass_side"])
    L.explode(rw, (0, -1, 0.2), 0.45, 1, "Cristales", "Ventana trasera eléctrica de la cabina", "R")
    objs.append(rw)
    return objs


# ---------------------------------------------------------------------------
# Salpicadero
# ---------------------------------------------------------------------------
def build_dashboard(M):
    objs = []
    asm = L.assembly("IP_ASSEMBLY", "INTERIOR_DASHBOARD", (0.0, 1.20, 1.0))
    L.explode(asm, (0, 1, 0.25), 0.75, 2, "Salpicadero", "Conjunto del salpicadero", "R")
    # Parte superior plana: de la cara del salpicadero a la base del parabrisas
    mb = L.MeshBuilder()
    hw = 0.70           # por dentro de los paneles de puerta (x 0,765); las tapas laterales cierran los extremos
    top = [(0.955, 1.092), (1.20, 1.110), (1.55, 1.150), (1.80, 1.215), (1.90, 1.262)]
    rows = [[(x, y, z) for (y, z) in top] for x in (-hw, hw)]
    for j in range(len(top) - 1):
        mb.face([rows[0][j], rows[1][j], rows[1][j + 1], rows[0][j + 1]], 0, want=(0, 0, 1))
    # cara vertical hacia los ocupantes, con la salida de aire continua
    face = [(0.955, 1.092), (0.948, 1.060), (0.950, 0.985), (0.990, 0.900), (1.10, 0.80)]
    rows2 = [[(x, y, z) for (y, z) in face] for x in (-hw, hw)]
    for j in range(len(face) - 1):
        mat = 1 if j == 1 else 0
        mb.face([rows2[0][j], rows2[1][j], rows2[1][j + 1], rows2[0][j + 1]], mat, want=(0, -1, 0.2))
    for sgn in (1, -1):
        side = [(sgn * hw, y, z) for (y, z) in face] + [(sgn * hw, y, z) for (y, z) in reversed(top)]
        mb.face(side, 0, want=(sgn, 0, 0))
    top_pad = mb.build("INT_IP_TopPad", "INTERIOR_DASHBOARD", [M["int_grey"], M["int_plastic"]], parent=asm)
    L.solidify(top_pad, 0.01)
    L.bevel(top_pad, 0.006, 2, 40)
    L.set_smooth_by_angle(top_pad, 40)
    L.explode(top_pad, (0, 0.6, 1), 0.25, 2, "Salpicadero", "Panel superior del salpicadero (Tactical Grey)", "R")
    objs.append(top_pad)
    # Rejilla de la salida de aire a lo ancho (Airwave)
    mb = L.MeshBuilder()
    for k in range(3):
        L.box(mb, (0.0, 0.944, 1.067 - k * 0.010), (1.38, 0.006, 0.0025), 0)
    vent = mb.build("INT_IP_Airwave_Vent", "INTERIOR_DASHBOARD", M["int_plastic"], parent=asm)
    L.explode(vent, (0, -1, 0), 0.12, 6, "Salpicadero", "Salida de aire continua (Airwave)", "R")
    objs.append(vent)
    # Tira de luz ambiental
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 0.946, 1.040), (1.56, 0.004, 0.003), 0)
    amb = mb.build("INT_IP_Ambient_Light", "INTERIOR_DASHBOARD", M["led_white"], parent=asm)
    L.explode(amb, (0, -1, 0), 0.10, 6, "Salpicadero", "Tira de luz ambiental", "A")
    objs.append(amb)
    # Panel inferior (rodillas) y guantera
    objs.append(soft_box("INT_IP_Lower_Driver", "INTERIOR_DASHBOARD", M["int_plastic"], (-0.42, 1.10, 0.72),
                         (0.62, 0.20, 0.22), 0.02, 2, parent=asm, edir=(0, 1, -0.3), dist=0.2,
                         label="Panel inferior del conductor"))
    objs.append(soft_box("INT_IP_Glovebox", "INTERIOR_DASHBOARD", M["int_plastic"], (0.42, 1.08, 0.80),
                         (0.58, 0.22, 0.20), 0.02, 2, parent=asm, edir=(0, 1, -0.3), dist=0.2,
                         label="Guantera"))
    # Pantalla central de 18,5" (16:9 -> 409,6 x 230,4 mm) con carcasa
    scr = L.assembly("DISPLAY_CENTER", "INTERIOR_CONTROLS", (0.0, 0.93, 1.21), parent=asm)
    L.explode(scr, (0, -0.5, 1), 0.45, 2, "Pantallas", "Pantalla táctil central de 18,5\" (tamaño según fuentes secundarias)", "R")
    tilt = rot_x(-14)
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 0.935, 1.215), (0.432, 0.030, 0.252), 0, rot=tilt)
    shell = mb.build("INT_Display_Center_Housing", "INTERIOR_CONTROLS", M["int_plastic"], parent=scr)
    L.bevel(shell, 0.008, 3, 60)
    L.explode(shell, (0, 1, 0), 0.06, 6, "Pantallas", "Carcasa de la pantalla central", "R")
    mb = L.MeshBuilder()
    c = Vector((0.0, 0.935, 1.215)) + tilt @ Vector((0, -0.0155, 0))
    L.box(mb, tuple(c), (0.4096, 0.002, 0.2304), 0, rot=tilt)
    glass = mb.build("INT_Display_Center_Screen", "INTERIOR_CONTROLS", M["screen"], parent=scr)
    L.explode(glass, (0, -1, 0), 0.05, 6, "Pantallas", "Panel de 18,5\" (409,6 x 230,4 mm; tamaño según fuentes secundarias)", "R")
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 0.975, 1.115), (0.10, 0.06, 0.06), 0)
    stand = mb.build("INT_Display_Center_Mount", "INTERIOR_CONTROLS", M["int_plastic"], parent=scr)
    L.explode(stand, (0, 1, -0.5), 0.05, 6, "Pantallas", "Soporte de la pantalla", "A")
    objs += [shell, glass, stand]
    # Columna y volante «squircle»
    objs += build_steering_wheel(M, asm)
    # Pedales
    for nm, x, w in (("Accelerator", -0.29, 0.06), ("Brake", -0.43, 0.11)):
        mb = L.MeshBuilder()
        L.box(mb, (x, 1.28, 0.64), (w, 0.012, 0.10 if nm == "Brake" else 0.20), 0, rot=rot_x(-25))
        L.box(mb, (x, 1.33, 0.73), (0.02, 0.10, 0.02), 0)
        o = mb.build(f"INT_Pedal_{nm}", "INTERIOR_CONTROLS", [M["int_plastic"]])
        L.explode(o, (0, 1, 0), 0.25, 2, "Mandos", "Pedal del acelerador" if nm == "Accelerator" else "Pedal de freno", "R")
        objs.append(o)
    return objs


def build_steering_wheel(M, parent):
    objs = []
    col_dir = Vector((0, 1, -0.42)).normalized()      # columna inclinada ~23°
    c = Vector(WHEEL_C)
    asm = L.assembly("STEERING_WHEEL", "STEERING", tuple(c), parent=parent)
    L.explode(asm, (0, -1, 0.3), 0.40, 2, "Dirección", "Volante «squircle» (dirección por cable)", "R")
    u = Vector((1, 0, 0))
    v = col_dir.cross(u).normalized()
    if v.z < 0:
        v = -v
    # Aro de forma «squircle» (superelipse) de 0,36 x 0,30 m
    mb = L.MeshBuilder()
    a, b, n = 0.180, 0.150, 4.0
    seg, rseg, rr = 72, 10, 0.017
    ring = []
    for k in range(seg):
        t = 2 * math.pi * k / seg
        ct, st = math.cos(t), math.sin(t)
        x = a * math.copysign(abs(ct) ** (2 / n), ct)
        y = b * math.copysign(abs(st) ** (2 / n), st)
        ring.append(c + u * x + v * y)
    rings = []
    for k in range(seg):
        p, q = ring[k], ring[(k + 1) % seg]
        tng = (q - ring[k - 1]).normalized()
        nrm = (p - c).normalized()
        bin_ = tng.cross(nrm).normalized()
        rings.append([tuple(p + (nrm * math.cos(2 * math.pi * j / rseg) + bin_ * math.sin(2 * math.pi * j / rseg))
                            * rr * (1.0 if math.sin(2 * math.pi * j / rseg) >= 0 else 0.85))
                      for j in range(rseg)])
    for k in range(seg):
        mb.quad_strip(rings[k], rings[(k + 1) % seg], closed=True)
    rim = mb.build("INT_SteeringWheel_Rim", "STEERING", M["leather"], parent=asm)
    L.recalc_normals(rim)
    for p in rim.data.polygons:
        p.use_smooth = True
    L.explode(rim, (0, -1, 0.3), 0.10, 6, "Dirección", "Aro del volante", "R")
    # Radios horizontales y buje (con rodillos de desplazamiento)
    mb = L.MeshBuilder()
    rot = Matrix((u, v, col_dir)).transposed()
    L.box(mb, tuple(c + col_dir * 0.01), (0.32, 0.055, 0.03), 0, rot=rot)
    L.box(mb, tuple(c + col_dir * 0.02), (0.12, 0.10, 0.05), 0, rot=rot)
    hub = mb.build("INT_SteeringWheel_Hub", "STEERING", M["int_plastic"], parent=asm)
    L.bevel(hub, 0.008, 2, 60)
    L.explode(hub, (0, -1, 0.3), 0.05, 6, "Dirección", "Buje y radios con controles", "R")
    # Columna y cubierta
    mb = L.MeshBuilder()
    # empieza detrás del buje del volante (que ocupa 0–0,05 m a lo largo de la columna)
    L.lathe(mb, [(0.045, 0.055), (0.055, 0.10), (0.060, 0.26), (0.0, 0.27)], tuple(c), tuple(col_dir), 20, 0)
    col = mb.build("INT_Steering_Column_Shroud", "STEERING", M["int_plastic"], parent=asm)
    L.explode(col, (0, 1, -0.4), 0.15, 6, "Dirección", "Cubierta de la columna y actuador de realimentación", "R")
    objs += [rim, hub, col]
    return objs


# ---------------------------------------------------------------------------
# Consola central y pantalla trasera
# ---------------------------------------------------------------------------
def build_console(M):
    objs = []
    asm = L.assembly("CONSOLE_ASSEMBLY", "INTERIOR_CONTROLS", (0.0, 0.40, 0.70))
    L.explode(asm, (0, 0, 1), 0.70, 2, "Consola central", "Consola central", "R")
    objs.append(soft_box("INT_Console_Body", "INTERIOR_CONTROLS", M["int_plastic"], (0.0, 0.40, 0.66),
                         (0.27, 1.10, 0.30), 0.03, 3, parent=asm, edir=(0, 0, 1), dist=0.05,
                         label="Cuerpo de la consola central"))
    objs.append(soft_box("INT_Console_Armrest", "INTERIOR_CONTROLS", M["leather"], (0.0, 0.10, 0.835),
                         (0.25, 0.42, 0.06), 0.025, 3, parent=asm, edir=(0, 0, 1), dist=0.18,
                         label="Reposabrazos (tapa del compartimento)"))
    objs.append(soft_box("INT_Console_Tray", "INTERIOR_CONTROLS", M["int_grey"], (0.0, 0.66, 0.818),
                         (0.25, 0.42, 0.02), 0.008, 2, parent=asm, edir=(0, 0, 1), dist=0.12,
                         label="Bandeja de cargadores inalámbricos"))
    for k in range(2):
        mb = L.MeshBuilder()
        L.lathe(mb, [(0.0, 0.0), (0.040, 0.0), (0.040, -0.07), (0.0, -0.072)], (0.0, 0.43 - k * 0.09, 0.83),
                (0, 0, 1), 24, 0)
        o = mb.build(f"INT_Console_Cupholder_{k + 1}", "INTERIOR_CONTROLS", M["int_plastic"], parent=asm)
        L.explode(o, (0, 0, 1), 0.10, 6, "Consola central", "Portavasos", "A")
        objs.append(o)
    # Pantalla trasera de 9,4" (16:9 aprox. 208 x 117 mm) en la parte posterior de la consola
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -0.152, 0.74), (0.225, 0.016, 0.135), 0, rot=rot_x(-12))
    rs_h = mb.build("INT_Display_Rear_Housing", "INTERIOR_CONTROLS", M["int_plastic"], parent=asm)
    L.bevel(rs_h, 0.006, 2, 60)
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -0.161, 0.742), (0.208, 0.002, 0.117), 0, rot=rot_x(-12))
    rs = mb.build("INT_Display_Rear_Screen", "INTERIOR_CONTROLS", M["screen"], parent=asm)
    L.explode(rs_h, (0, -1, 0.2), 0.25, 2, "Pantallas", "Carcasa de la pantalla trasera", "R")
    L.explode(rs, (0, -1, 0.2), 0.30, 2, "Pantallas", "Pantalla trasera de 9,4\" (tamaño según fuentes secundarias)", "R")
    objs += [rs_h, rs]
    return objs


# ---------------------------------------------------------------------------
# Asientos esculpidos (secciones solevadas + subdivisión)
# ---------------------------------------------------------------------------
def _section(half_w, bolster, depth, front_bulge=0.0):
    """Sección cerrada del respaldo/cojín: cara delantera con laterales y cara trasera."""
    xs = [0.0, 0.45, 0.62, 0.78, 0.92, 1.0]
    ds = [front_bulge, front_bulge * 0.8 + 0.004, 0.028, 0.058, 0.040, 0.0]
    front = []
    for x, d in zip(xs, ds):
        dd = d * bolster if x >= 0.6 else d
        front.append((x * half_w, dd))
    right = front[1:]
    ring = [(-x, d) for (x, d) in reversed(right)] + front + []
    ring = [(-p[0], p[1]) for p in reversed(right)] + [front[0]] + right
    back = [(half_w * 0.98, -depth), (half_w * 0.5, -depth - 0.006), (0.0, -depth - 0.008),
            (-half_w * 0.5, -depth - 0.006), (-half_w * 0.98, -depth)]
    return ring + back


def _loft_closed(mb, rings):
    """Solevado cerrado con orientación coherente.

    Las caras se generan con el orden de los anillos (sin reorientación por cara, que invertía
    las caras de las laderas interiores de los laterales y creaba pliegues al subdividir) y las
    tapas en abanico desde el centroide (sin n-gonos cóncavos). Si el volumen resulta negativo se
    invierten todas las caras para que las normales apunten hacia fuera.
    """
    start = len(mb.faces)
    for i in range(len(rings) - 1):
        mb.quad_strip(rings[i], rings[i + 1], closed=True)
    for ring, fwd in ((rings[0], False), (rings[-1], True)):
        c = tuple(sum((Vector(p) for p in ring), Vector()) / len(ring))
        n = len(ring)
        for i in range(n):
            a, b = ring[i], ring[(i + 1) % n]
            mb.face([c, a, b] if fwd else [c, b, a], 0)
    vol = 0.0
    for f in mb.faces[start:]:
        p0 = Vector(mb.verts[f[0]])
        for k in range(1, len(f) - 1):
            vol += p0.dot(Vector(mb.verts[f[k]]).cross(Vector(mb.verts[f[k + 1]])))
    if vol < 0:
        for i in range(start, len(mb.faces)):
            mb.faces[i] = list(reversed(mb.faces[i]))


def sculpted_back(name, system, mat, base, width, levels, depth, tilt_deg, parent, label, edir, dist):
    """Respaldo: `levels` = [(altura, escala_anchura, factor_lateral, abombado)]."""
    mb = L.MeshBuilder(merge=1e-7)
    rot = rot_x(tilt_deg)          # reclinado hacia atrás (-Y)
    b = Vector(base)
    rings = []
    for (h, sc, bol, bulge) in levels:
        sec = _section(width / 2 * sc, bol, depth, bulge)
        rings.append([tuple(b + rot @ Vector((x, d, h))) for (x, d) in sec])
    _loft_closed(mb, rings)
    obj = mb.build(name, system, mat, parent=parent)
    for p in obj.data.polygons:
        p.use_smooth = True
    L.subsurf(obj, 2, 2)
    L.explode(obj, edir, dist, 6, "Asientos", label, "R")
    return obj


def sculpted_cushion(name, system, mat, center, width, length, thick, parent, label, edir, dist, bol=1.0):
    """Cojín: secciones a lo largo de la profundidad con laterales elevados y morro redondeado."""
    mb = L.MeshBuilder(merge=1e-7)
    c = Vector(center)
    rings = []
    steps = [(-0.50, 0.97, 0.7, 0.00), (-0.42, 1.0, 1.0, 0.0), (0.0, 1.0, 1.0, 0.0), (0.38, 0.98, 0.8, -0.006),
             (0.47, 0.95, 0.4, -0.02), (0.50, 0.90, 0.2, -0.04)]
    for (t, sc, b, dz) in steps:
        sec = _section(width / 2 * sc, b * bol, thick, 0.0)
        # en el cojín la «profundidad» de la sección es la altura (Z) y la posición en Y es t·longitud
        rings.append([tuple(c + Vector((x, t * length, d + dz))) for (x, d) in sec])
    _loft_closed(mb, rings)
    obj = mb.build(name, system, mat, parent=parent)
    for p in obj.data.polygons:
        p.use_smooth = True
    L.subsurf(obj, 2, 2)
    L.explode(obj, edir, dist, 6, "Asientos", label, "R")
    return obj


FRONT_BACK_LEVELS = [(0.00, 1.00, 0.6, 0.010), (0.22, 1.00, 1.0, 0.018), (0.42, 0.97, 1.0, 0.012),
                     (0.54, 0.88, 0.5, 0.006), (0.60, 0.60, 0.1, 0.004), (0.645, 0.54, 0.25, 0.008),
                     (0.78, 0.56, 0.3, 0.010), (0.845, 0.50, 0.2, 0.004)]
REAR_BACK_LEVELS = [(0.00, 1.00, 0.4, 0.006), (0.20, 1.00, 0.6, 0.012), (0.42, 0.98, 0.5, 0.008),
                    (0.52, 0.90, 0.3, 0.004)]


def front_seat(M, side):
    s = 1 if side == "R" else -1
    hx, hz = H_FRONT
    x = s * SEAT_X
    asm = L.assembly(f"SEAT_FRONT_{side}", "INTERIOR_SEATS", (x, hx, hz))
    L.explode(asm, (s * 0.6, 0.1, 1), 0.95, 2, "Asientos",
              f"Asiento delantero {'del acompañante' if s > 0 else 'del conductor'}", "R")
    objs = [
        sculpted_cushion(f"INT_SeatF_{side}_Cushion", "INTERIOR_SEATS", M["leather"], (x, hx + 0.225, hz + 0.03),
                         0.52, 0.50, 0.11, asm, "Cojín con refuerzos laterales", (0, 0.3, 1), 0.08),
        sculpted_back(f"INT_SeatF_{side}_Back", "INTERIOR_SEATS", M["leather"], (x, hx - 0.04, hz - 0.02),
                      0.54, FRONT_BACK_LEVELS, 0.09, 22, asm, "Respaldo con reposacabezas integrado",
                      (0, -1, 0.3), 0.10),
        # bandeja del cojín (chapa) entre los mecanismos de debajo y el cojín: no es un bloque macizo, para que
        # guías, motores y soplador queden a la vista y sin atravesarse
        soft_box(f"INT_SeatF_{side}_Base", "INTERIOR_SEATS", M["int_plastic"], (x, hx + 0.21, 0.655),
                 (0.43, 0.48, 0.018), 0.006, 2, parent=asm, edir=(0, 0, -1), dist=0.08,
                 label="Bandeja del cojín del asiento", fid="A"),
    ]
    return objs


def rear_bench(M):
    hy, hz = H_REAR
    asm = L.assembly("SEAT_REAR", "INTERIOR_SEATS", (0.0, hy, hz))
    L.explode(asm, (0, -0.3, 1), 1.05, 2, "Asientos", "Banqueta trasera de tres plazas", "R")
    objs = []
    for k, nm in ((-1, "L"), (0, "C"), (1, "R")):
        w = 0.46 if k else 0.42
        x = k * 0.45
        objs.append(sculpted_cushion(f"INT_SeatR_{nm}_Cushion", "INTERIOR_SEATS", M["leather"],
                                     (x, hy + 0.21, hz + 0.02), w, 0.48, 0.10, asm,
                                     "Cojín abatible de la banqueta", (0, 0.3, 1), 0.08, bol=0.5))
        objs.append(sculpted_back(f"INT_SeatR_{nm}_Back", "INTERIOR_SEATS", M["leather"], (x, hy - 0.06, hz - 0.02),
                                  w, REAR_BACK_LEVELS, 0.10, REAR_TILT, asm, "Respaldo de la banqueta", (0, -1, 0.3), 0.10))
        tilt = rot_x(REAR_TILT)
        ch = Vector((x, hy - 0.06, hz - 0.02)) + tilt @ Vector((0, -0.03, 0.62))
        objs.append(soft_box(f"INT_SeatR_{nm}_Headrest", "INTERIOR_SEATS", M["leather"], tuple(ch),
                             (0.25, 0.09, 0.15), 0.04, 3, rot=tilt, parent=asm, edir=(0, -0.3, 1), dist=0.15,
                             label="Reposacabezas trasero"))
    objs.append(soft_box("INT_SeatR_Base", "INTERIOR_SEATS", M["int_plastic"], (0.0, hy + 0.21, 0.635),
                         (1.38, 0.48, 0.018), 0.006, 2, parent=asm, edir=(0, 0, -1), dist=0.08,
                         label="Bandeja de los cojines de la banqueta", fid="A"))
    return objs


def build_seatbelts(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        for row, yb in (("F", S.DOOR_B_SEAM_Y - 0.035), ("R", S.CAB_REAR_Y + 0.05)):
            # Cinturón recogido: del anclaje superior del pilar al enrollador inferior
            x = s * (0.80 if row == "F" else 0.76)
            top = Vector((x, yb, 1.50 if row == "F" else 1.42))
            low = Vector((x, yb, FLOOR_Z + 0.12))
            mb = L.MeshBuilder()
            L.box(mb, tuple((top + low) / 2), (0.004, 0.048, (top - low).length), 0)
            L.box(mb, tuple(top + Vector((0, 0, 0.02))), (0.02, 0.06, 0.05), 1)
            L.box(mb, tuple(low), (0.05, 0.08, 0.10), 1)
            o = mb.build(f"INT_Seatbelt_{row}{sd}", "INTERIOR_SEATS", [M["seatbelt"], M["int_plastic"]])
            L.explode(o, (0, 0, 1), 0.3, 6, "Cinturones", "Cinturón de seguridad de tres puntos", "A")
            objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Paneles de puerta, guarnecidos y techo
# ---------------------------------------------------------------------------
def build_door_trims(M):
    import bpy
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        for key, (yf, yr) in (("F", (S.DOOR_F_FRONT_Y - 0.02, S.DOOR_B_SEAM_Y + 0.01)),
                              ("R", (S.DOOR_B_SEAM_Y - 0.01, S.DOOR_R_REAR_Y + 0.01))):
            door = bpy.data.objects.get(f"DOOR_{key}{sd}")
            x_in = s * (S.SHOULDER_F / 2.0 if key == "F" else S.SHOULDER_R / 2.0)
            zt = S.z_belt((yf + yr) / 2) - 0.02
            mb = L.MeshBuilder()
            pts = [(yf, FLOOR_Z + 0.03), (yr, FLOOR_Z + 0.03), (yr, zt), (yf, zt)]
            if key == "F":
                pts = [(yf - 0.12, FLOOR_Z + 0.03), (yr, FLOOR_Z + 0.03), (yr, zt), (yf - 0.12, zt)]
            mb.face([(x_in, y, z) for (y, z) in pts], 0, want=(-s, 0, 0))
            panel = mb.build(f"INT_DoorTrim_{key}{sd}", "INTERIOR_DOORS", M["int_grey"], parent=door)
            L.solidify(panel, 0.04, offset=-1.0)
            L.bevel(panel, 0.01, 2, 40)
            L.explode(panel, (-s, 0, 0), 0.30, 2, "Paneles de puerta", "Guarnecido interior de la puerta", "R")
            objs.append(panel)
            # Reposabrazos, bolsillo y altavoz
            ym = (yf + yr) / 2
            objs.append(soft_box(f"INT_DoorArmrest_{key}{sd}", "INTERIOR_DOORS", M["leather"],
                                 (x_in - s * 0.05, ym, 0.86), (0.08, (yf - yr) * 0.55, 0.05), 0.02, 2,
                                 parent=door, edir=(-s, 0, 0), dist=0.40, label="Reposabrazos de la puerta"))
            objs.append(soft_box(f"INT_DoorPocket_{key}{sd}", "INTERIOR_DOORS", M["int_plastic"],
                                 (x_in - s * 0.04, ym + 0.05, 0.62), (0.06, (yf - yr) * 0.7, 0.10), 0.01, 2,
                                 parent=door, edir=(-s, 0, -0.3), dist=0.38, label="Bolsillo de la puerta"))
            mb = L.MeshBuilder()
            L.lathe(mb, [(0.0, 0.0), (0.075, 0.0), (0.075, 0.006), (0.0, 0.006)],
                    (x_in - s * 0.042, ym - 0.12, 0.66), (-s, 0, 0), 32, 0)
            spk = mb.build(f"INT_DoorSpeaker_{key}{sd}", "INTERIOR_DOORS", M["int_plastic"], parent=door)
            L.explode(spk, (-s, 0, 0), 0.42, 6, "Paneles de puerta", "Rejilla del altavoz", "A")
            objs.append(spk)
            # Pulsador de apertura y botonera de ventanillas
            objs.append(soft_box(f"INT_DoorButton_{key}{sd}", "INTERIOR_DOORS", M["alu_trim"],
                                 (x_in - s * 0.02, yf - 0.10, 0.96), (0.02, 0.05, 0.02), 0.005, 2,
                                 parent=door, edir=(-s, 0, 0.3), dist=0.45, label="Pulsador interior de apertura"))
    return objs


def build_headliner_and_trims(M):
    objs = []
    # Guarnecidos laterales del techo (cantrail) y consola de techo delantera
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        ys = [0.85, 0.55, 0.25, -0.1, -0.5, -0.88]
        inner = [(s * (B.roof_hw(y) - 0.06), y, S.z_top(y) - 0.035) for y in ys]
        outer = [(s * (B.roof_hw(y) + 0.02), y, S.z_top(y) - 0.10) for y in ys]
        mb.quad_strip(inner, outer, want_fn=lambda c: Vector((-s * 0.3, 0, -1)))
        o = mb.build(f"INT_Cantrail_{sd}", "INTERIOR_TRIM", M["headliner"])
        L.solidify(o, 0.008)
        L.explode(o, (s * 0.3, 0, 1), 0.35, 2, "Guarnecidos", "Guarnecido del larguero del techo", "R")
        objs.append(o)
        # Parasoles
        objs.append(soft_box(f"INT_SunVisor_{sd}", "INTERIOR_TRIM", M["headliner"],
                             (s * 0.40, 0.90, S.z_top(0.90) - 0.06), (0.36, 0.17, 0.02), 0.008, 2,
                             rot=rot_x(16), edir=(0, 0, 1), dist=0.30, label="Parasol con cortinilla"))
    objs.append(soft_box("INT_Overhead_Console", "INTERIOR_TRIM", M["int_plastic"], (0.0, 0.62, S.z_top(0.62) - 0.045),
                         (0.30, 0.10, 0.03), 0.01, 2, rot=rot_x(16), edir=(0, 0, 1), dist=0.35,
                         label="Consola de techo delantera (luces de lectura)"))
    # Retrovisor interior
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 0.66, S.z_top(0.66) - 0.115), (0.26, 0.03, 0.065), 0)
    L.box(mb, (0.0, 0.672, S.z_top(0.66) - 0.07), (0.02, 0.02, 0.06), 0)
    rm = mb.build("INT_Rearview_Mirror", "INTERIOR_TRIM", M["int_plastic"])
    L.bevel(rm, 0.008, 2, 60)
    L.explode(rm, (0, -0.3, 1), 0.4, 2, "Guarnecidos", "Retrovisor interior", "R")
    objs.append(rm)
    # Moqueta del suelo y alfombrillas
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 0.22, FLOOR_Z + 0.006), (1.68, 2.30, 0.012), 0)
    carpet = mb.build("INT_Carpet", "INTERIOR_TRIM", M["carpet"])
    L.explode(carpet, (0, 0, -1), 0.15, 2, "Guarnecidos", "Moqueta del habitáculo", "R")
    objs.append(carpet)
    for nm, (x, y, w, l) in (("FL", (-0.40, 0.92, 0.55, 0.55)), ("FR", (0.40, 0.92, 0.55, 0.55)),
                             ("R", (0.0, -0.20, 1.40, 0.45))):
        mb = L.MeshBuilder()
        L.box(mb, (x, y, FLOOR_Z + 0.016), (w, l, 0.008), 0)
        mat = mb.build(f"INT_FloorMat_{nm}", "INTERIOR_TRIM", M["composite"])
        L.bevel(mat, 0.003, 1, 60)
        L.explode(mat, (0, 0, 1), 0.12, 6, "Guarnecidos", "Alfombrilla para todo tipo de clima", "A")
        objs.append(mat)
    return objs


def build_all(M):
    out = []
    out += build_cabin_shell(M)
    out += build_dashboard(M)
    out += build_console(M)
    out += front_seat(M, "L") + front_seat(M, "R") + rear_bench(M)
    out += build_seatbelts(M)
    out += build_door_trims(M)
    out += build_headliner_and_trims(M)
    return out
