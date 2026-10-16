"""Chasis: cubeta del maletero delantero, caja de carga y orquestación de la mecánica detallada.

Desde la versión 2 la mecánica (batería, unidades motrices, suspensión, dirección, subchasis,
refrigeración, frenos hidráulicos, aire comprimido, baja tensión y bajos) se construye en
build_mechanics.py; las notas de fuentes siguientes se conservan como referencia.

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
# Cubeta del maletero delantero (frunk, 200 l)
# ---------------------------------------------------------------------------
def build_frunk(M):
    objs = []
    # Cubeta del maletero delantero (frunk, 200 l)
    mb = L.MeshBuilder()
    y0, y1, hw, zb, zt = 2.58, 1.98, 0.455, 0.74, 1.04
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
    L.box(mb, (0.0, -2.52, zf - 0.13), (0.88, 0.60, 0.24), 0)
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
    import build_mechanics
    import build_structure
    out = build_mechanics.build_all(M)
    out += build_structure.build_all(M)
    out += build_frunk(M)
    out += build_cargo_bed(M)
    return out
