"""Ruedas, neumáticos y frenos del Cybertruck Cyberbeast.

[V] Llanta 20 x 9.0J ET58.5; neumático Pirelli Scorpion ATR 285/65R20 (manual).
[V] Discos ventilados: delantero Ø351 x 32 mm (pinza fija de 4 pistones); trasero Ø356 x 23 mm
    (pinza flotante de 1 pistón con freno de estacionamiento eléctrico).
[R] Tapacubos aerodinámico «Core» de 6 palas facetadas (fotografías del configurador).
[A] Dibujo de la banda de rodadura: patrón todoterreno genérico de bloques (no se ha podido
    verificar el dibujo exacto del Scorpion ATR); sin inscripciones en el flanco.
"""

import math
import bpy
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L

R_TIRE = S.TIRE_RADIUS
R_RIM = S.RIM_RADIUS
HALF_RIM = S.RIM_WIDTH_IN * 0.0254 / 2.0          # 0.1143
HALF_SECTION = S.TIRE_WIDTH / 2.0                  # 0.1425
TREAD_BASE = R_TIRE - 0.0145                       # fondo de los surcos (profundidad ~14,5 mm)


def cyl(r, theta, a):
    """Coordenadas locales de rueda: eje = +X (a), ángulo en el plano YZ."""
    return (a, r * math.cos(theta), r * math.sin(theta))


# ---------------------------------------------------------------------------
# Neumático (malla compartida por las cuatro ruedas)
# ---------------------------------------------------------------------------
def tire_mesh():
    name = "MESH_Tire_285_65R20"
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    seg = 128
    # Perfil de la carcasa (radio, posición axial) desde el talón exterior al interior
    prof = [(0.262, HALF_RIM + 0.004), (0.272, HALF_RIM + 0.010), (0.300, 0.131), (0.330, 0.139),
            (0.360, HALF_SECTION), (0.390, 0.140), (0.410, 0.133), (0.422, 0.124), (TREAD_BASE + 0.002, 0.118),
            (TREAD_BASE, 0.100), (TREAD_BASE + 0.0015, 0.0), (TREAD_BASE, -0.100),
            (TREAD_BASE + 0.002, -0.118), (0.422, -0.124), (0.410, -0.133), (0.390, -0.140),
            (0.360, -HALF_SECTION), (0.330, -0.139), (0.300, -0.131), (0.272, -(HALF_RIM + 0.010)),
            (0.262, -(HALF_RIM + 0.004))]
    rings = []
    for (r, a) in prof:
        rings.append([cyl(r, 2 * math.pi * k / seg, a) for k in range(seg)])
    for i in range(len(rings) - 1):
        mat = 0 if abs(prof[i][1]) < 0.119 and abs(prof[i + 1][1]) < 0.119 else 1
        mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=mat,
                      want_fn=lambda c: Vector((0, c.y, c.z)) if abs(c.x) < 0.125 else Vector((c.x, 0, 0)))
    # interior del talón (cierra la carcasa contra la llanta)
    mb.quad_strip(rings[-1], rings[0], closed=True, mat=1, want_fn=lambda c: Vector((0, -c.y, -c.z)))

    def block(a0, a1, t0, t1, r0, r1, bevel_top=0.0025):
        """Bloque de goma sobre la banda de rodadura (8 vértices + chaflán superior)."""
        bot = [cyl(r0, t0, a0), cyl(r0, t1, a0), cyl(r0, t1, a1), cyl(r0, t0, a1)]
        dt = bevel_top / r1
        top = [cyl(r1, t0 + dt, a0 + bevel_top), cyl(r1, t1 - dt, a0 + bevel_top),
               cyl(r1, t1 - dt, a1 - bevel_top), cyl(r1, t0 + dt, a1 - bevel_top)]
        mid = 0.5 * (t0 + t1)
        out = Vector(cyl(1.0, mid, 0.0))
        mb.face(top, 0, want=out)
        for i in range(4):
            j = (i + 1) % 4
            q = [bot[i], bot[j], top[j], top[i]]
            c = sum((Vector(p) for p in q), Vector()) / 4
            cen = Vector(cyl((r0 + r1) / 2, mid, (a0 + a1) / 2))
            mb.face(q, 0, want=c - cen)

    pitches = 60
    dp = 2 * math.pi / pitches
    rt = R_TIRE
    for k in range(pitches):
        t = k * dp
        stag = 0.5 * dp if k % 2 else 0.0
        # bloques de hombro (escalonados) con prolongación hacia el flanco
        block(0.072, 0.120, t + 0.06 * dp, t + 0.80 * dp, TREAD_BASE, rt)
        block(-0.120, -0.072, t + 0.06 * dp + 0.5 * dp, t + 0.80 * dp + 0.5 * dp, TREAD_BASE, rt)
        # bloques centrales en zigzag
        block(0.010, 0.064, t + 0.12 * dp + stag * 0.4, t + 0.86 * dp + stag * 0.4, TREAD_BASE, rt - 0.0005)
        block(-0.064, -0.010, t + 0.62 * dp - stag * 0.4, t + 1.36 * dp - stag * 0.4, TREAD_BASE, rt - 0.0005)
        # tacos del flanco superior (característicos de los neumáticos todoterreno)
        if k % 2 == 0:
            for sgn in (1, -1):
                a0, a1 = sgn * 0.124, sgn * 0.140
                bot = [cyl(0.405, t + 0.1 * dp, a0), cyl(0.405, t + 1.1 * dp, a0),
                       cyl(0.425, t + 1.1 * dp, a0), cyl(0.425, t + 0.1 * dp, a0)]
                top = [cyl(0.405, t + 0.15 * dp, a1), cyl(0.405, t + 1.05 * dp, a1),
                       cyl(0.422, t + 1.05 * dp, a1 - sgn * 0.004), cyl(0.422, t + 0.15 * dp, a1 - sgn * 0.004)]
                mb.face(top, 1, want=(sgn, 0, 0))
                for i in range(4):
                    j = (i + 1) % 4
                    q = [bot[i], bot[j], top[j], top[i]]
                    mb.face(q, 1)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(40))
    return me


# ---------------------------------------------------------------------------
# Llanta de aleación 20 x 9.0J (barril, pestañas, radios estructurales, buje)
# ---------------------------------------------------------------------------
def rim_mesh(name):
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    seg = 96
    # Perfil del barril (radio, axial): exterior (+X) a interior (-X)
    prof = [(0.268, HALF_RIM + 0.012), (0.272, HALF_RIM + 0.004), (0.262, HALF_RIM - 0.004),
            (0.256, HALF_RIM - 0.012), (0.250, 0.080), (0.236, 0.050), (0.236, -0.040),
            (0.250, -0.070), (0.256, -(HALF_RIM - 0.012)), (0.262, -(HALF_RIM - 0.004)),
            (0.272, -(HALF_RIM + 0.004)), (0.268, -(HALF_RIM + 0.012)),
            (0.258, -(HALF_RIM + 0.006)), (0.244, -0.06), (0.226, -0.03), (0.226, 0.045),
            (0.240, 0.075), (0.250, HALF_RIM)]
    L.lathe(mb, prof, (0, 0, 0), (1, 0, 0), seg, 0, closed_profile=True)
    # Disco central y radios estructurales (ocultos parcialmente por el tapacubos)
    hub_face = S.RIM_OFFSET
    L.lathe(mb, [(0.105, hub_face + 0.004), (0.105, hub_face - 0.035), (0.034, hub_face - 0.035),
                 (0.034, hub_face + 0.004)], (0, 0, 0), (1, 0, 0), 48, 0, closed_profile=True)
    for k in range(6):
        t = 2 * math.pi * k / 6 + math.pi / 6
        w = 0.032
        pts = []
        for (r, a, ww) in ((0.10, hub_face, w), (0.235, 0.050, w * 0.8)):
            tt = w / r
            pts.append((r, a, tt))
        a0, a1 = pts
        quad = []
        for (r, a, tt) in (a0, a1):
            quad += [cyl(r, t - tt, a), cyl(r, t + tt, a)]
        top = [quad[0], quad[1], quad[3], quad[2]]
        bot = [tuple(Vector(p) - Vector((0.03, 0, 0))) for p in top]
        mb.face(top, 0, want=(1, 0, 0))
        mb.face(bot, 0, want=(-1, 0, 0))
        for i in range(4):
            j = (i + 1) % 4
            mb.face([top[i], top[j], bot[j], bot[i]], 0)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(35))
    return me


# ---------------------------------------------------------------------------
# Tapacubos aerodinámico «Core» (6 palas facetadas desplazadas)
# ---------------------------------------------------------------------------
def cover_mesh(name, mirror=False):
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    seg = 96
    face_a = HALF_RIM + 0.012          # plano exterior del borde de la llanta
    # Disco base ligeramente cóncavo con borde exterior
    prof = [(0.262, face_a + 0.002), (0.252, face_a + 0.010), (0.235, face_a + 0.004), (0.150, face_a - 0.012),
            (0.075, face_a - 0.010), (0.060, face_a + 0.004), (0.000, face_a + 0.004)]
    rings = L.lathe(mb, prof[:-1], (0, 0, 0), (1, 0, 0), seg, 0)
    mb.face(rings[-1][::-1] if False else rings[-1], 0, want=(1, 0, 0))
    # cara trasera del disco
    back = [cyl(0.262, 2 * math.pi * k / seg, face_a - 0.02) for k in range(seg)]
    mb.quad_strip(rings[0], back, closed=True, mat=0, want_fn=lambda c: Vector((0, c.y, c.z)))
    mb.face(back, 0, want=(-1, 0, 0))
    # Palas: tablones planos y anchos con un chaflán lateral (6 por rueda)
    sgn = -1 if mirror else 1

    def disc_a(r):
        """Altura axial del disco base (cóncavo) en el radio r."""
        return S.interp([(0.06, face_a + 0.004), (0.075, face_a - 0.010), (0.150, face_a - 0.012),
                         (0.235, face_a + 0.004)], r)

    for k in range(6):
        t0 = 2 * math.pi * k / 6

        def P(r, off, h):
            # desplazamiento tangencial progresivo (barrido de la pala)
            return cyl(r, t0 + sgn * (off / r + 0.10 * (r - 0.065) / 0.18), disc_a(r) + h)
        r0, r1 = 0.064, 0.246
        w0, w1 = 0.024, 0.062          # semianchura de la pala en el centro y en el borde
        h0, h1 = 0.020, 0.012          # resalte sobre el disco
        ch = 0.016                     # anchura del chaflán lateral
        base = [P(r0, -w0, -0.004), P(r1, -w1, -0.004), P(r1, w1, -0.004), P(r0, w0, -0.004)]
        top = [P(r0, -w0 + ch * 0.5, h0), P(r1, -w1 + ch, h1), P(r1, w1, h1), P(r0, w0, h0)]
        mb.face(top, 1, want=(1, 0, 0))
        for i in range(4):
            j = (i + 1) % 4
            q = [base[i], base[j], top[j], top[i]]
            c = sum((Vector(p) for p in q), Vector()) / 4
            ctr = sum((Vector(p) for p in top), Vector()) / 4
            mb.face(q, 1, want=(c - ctr) * Vector((0.2, 1, 1)) + Vector((0.6, 0, 0)))
    # Tapa central
    L.lathe(mb, [(0.058, face_a + 0.006), (0.052, face_a + 0.014), (0.0, face_a + 0.016)], (0, 0, 0),
            (1, 0, 0), 48, 2)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(25))
    return me


def lug_mesh(name):
    """Seis tuercas M14 (llave de 21 mm) en un círculo de 135 mm [R]."""
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    pcd = 0.135 / 2
    a0 = S.RIM_OFFSET + 0.001
    for k in range(6):
        t = 2 * math.pi * k / 6
        c = Vector(cyl(pcd, t, 0))
        # hexágono 21 mm entre caras
        hexr = 0.021 / math.sqrt(3)
        prof = [(hexr, a0), (hexr, a0 + 0.018), (hexr * 0.7, a0 + 0.024), (0.0, a0 + 0.026)]
        L.lathe(mb, prof, c, (1, 0, 0), 6, 0, phase=math.pi / 6)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    return me


# ---------------------------------------------------------------------------
# Frenos
# ---------------------------------------------------------------------------
def rotor_mesh(name, diam, thick, vanes=40):
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    ro, ri = diam / 2, diam / 2 - 0.072
    plate = thick * 0.30
    seg = 96
    for sgn in (1, -1):
        a_out = sgn * thick / 2
        a_in = sgn * (thick / 2 - plate)
        L.lathe(mb, [(ri, a_in), (ro, a_in), (ro, a_out), (ri, a_out)], (0, 0, 0), (1, 0, 0), seg, 0,
                closed_profile=True)
    # álabes de ventilación entre las dos pistas
    for k in range(vanes):
        t = 2 * math.pi * k / vanes
        w = 0.0035
        a0, a1 = -(thick / 2 - plate), thick / 2 - plate
        pts = [cyl(ri + 0.004, t - w / ri, a0), cyl(ro - 0.004, t - w / ro + 0.06, a0),
               cyl(ro - 0.004, t + w / ro + 0.06, a0), cyl(ri + 0.004, t + w / ri, a0)]
        top = [(a1, p[1], p[2]) for p in pts]
        mb.face(pts, 0)
        mb.face(top, 0)
        for i in range(4):
            j = (i + 1) % 4
            mb.face([pts[i], pts[j], top[j], top[i]], 0)
    # campana (sombrero) hacia el buje, en el lado exterior
    L.lathe(mb, [(ri + 0.002, thick / 2), (0.090, thick / 2 + 0.002), (0.088, thick / 2 + 0.040),
                 (0.034, thick / 2 + 0.040), (0.034, thick / 2 + 0.034), (0.082, thick / 2 + 0.034),
                 (0.084, thick / 2 + 0.006), (ri, thick / 2 - 0.002)], (0, 0, 0), (1, 0, 0), 72, 1,
            closed_profile=True)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
    return me


def caliper_mesh(name, diam, thick, front=True):
    """Pinza: fija de 4 pistones (delante) o flotante de 1 pistón con motor EPB (detrás)."""
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    ro = diam / 2
    span = 0.62 if front else 0.48                 # arco angular cubierto (rad)
    rc_in, rc_out = ro - 0.060, ro + 0.020
    gap = thick / 2 + 0.006
    body_w = 0.040 if front else 0.032
    t_c = 0.0                                       # centrada en la parte trasera superior del disco
    nseg = 8
    # Dos mitades (exterior e interior) unidas por un puente sobre el disco
    for sgn in (1, -1):
        if not front and sgn > 0:
            w = 0.018                              # dedo exterior de la pinza flotante
        else:
            w = body_w
        a0, a1 = sgn * gap, sgn * (gap + w)
        rings = []
        for i in range(nseg + 1):
            t = t_c - span / 2 + span * i / nseg
            rings.append([cyl(rc_in, t, a0), cyl(rc_out, t, a0), cyl(rc_out, t, a1), cyl(rc_in, t, a1)])
        for i in range(nseg):
            mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=0,
                          want_fn=lambda c: Vector((c.x * 2, c.y, c.z)) * 1.0)
        mb.face(rings[0], 0)
        mb.face(rings[-1][::-1], 0)
    # puente sobre el borde del disco
    rings = []
    for i in range(nseg + 1):
        t = t_c - span * 0.42 + span * 0.84 * i / nseg
        rings.append([cyl(ro + 0.004, t, -gap - body_w), cyl(rc_out, t, -gap - body_w),
                      cyl(rc_out, t, gap + 0.018), cyl(ro + 0.004, t, gap + 0.018)])
    for i in range(nseg):
        mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=0)
    mb.face(rings[0], 0)
    mb.face(rings[-1][::-1], 0)
    # pistones visibles (tapas) en la cara interior
    npist = 2 if front else 1
    for k in range(npist):
        t = t_c + (k - (npist - 1) / 2) * span * 0.45
        c = Vector(cyl(ro - 0.022, t, -(gap + body_w)))
        L.lathe(mb, [(0.021, 0.0), (0.021, -0.012), (0.0, -0.014)], c, (1, 0, 0), 20, 0)
    if not front:
        # motor del freno de estacionamiento eléctrico
        c = Vector(cyl(ro - 0.02, t_c + 0.08, -(gap + body_w + 0.01)))
        L.lathe(mb, [(0.026, 0.0), (0.026, -0.085), (0.020, -0.092), (0.0, -0.093)], c, (-1, 0, 0.0), 24, 0)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(40))
    return me


def shield_mesh(name, diam):
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    ro = diam / 2 + 0.012
    L.lathe(mb, [(0.07, -0.030), (ro, -0.030), (ro, -0.045), (ro - 0.006, -0.047), (0.07, -0.044)],
            (0, 0, 0), (1, 0, 0), 64, 0, closed_profile=True)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], mb.faces)
    me.validate()
    return me


def instance(name, mesh, system, parent, world_loc, rot_z=0.0, mats=None, rot_x=0.0):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    obj = bpy.data.objects.new(name, mesh)
    L.link_only(obj, L.vehicle_collection(system))
    L.parent_keep_world(obj, parent, world_loc)
    obj.rotation_euler = (rot_x, 0.0, rot_z)
    obj["system"] = system
    if mats is not None and not mesh.materials:
        for m in mats:
            mesh.materials.append(m)
    return obj


def build_all(M):
    tire = tire_mesh()
    tire.materials.append(M["rubber"])
    tire.materials.append(M["rubber_side"])
    rim = rim_mesh("MESH_Rim_20x9")
    rim.materials.append(M["wheel_alloy"])
    lugs = lug_mesh("MESH_LugNuts_6x")
    lugs.materials.append(M["zinc"])
    covers = {}
    for sd, mir in (("R", False), ("L", True)):
        cm = cover_mesh(f"MESH_WheelCover_Core_{sd}", mirror=mir)
        cm.materials.append(M["wheel_cover"])
        cm.materials.append(M["wheel_cover"])
        cm.materials.append(M["plastic_black"])
        covers[sd] = cm
    rot_f = rotor_mesh("MESH_Rotor_Front_351x32", S.FRONT_ROTOR_D, S.FRONT_ROTOR_T)
    rot_r = rotor_mesh("MESH_Rotor_Rear_356x23", S.REAR_ROTOR_D, S.REAR_ROTOR_T)
    for m in (rot_f, rot_r):
        m.materials.append(M["rotor"])
        m.materials.append(M["rotor"])
    cal_f = caliper_mesh("MESH_Caliper_Front_4P", S.FRONT_ROTOR_D, S.FRONT_ROTOR_T, True)
    cal_r = caliper_mesh("MESH_Caliper_Rear_1P_EPB", S.REAR_ROTOR_D, S.REAR_ROTOR_T, False)
    for m in (cal_f, cal_r):
        m.materials.append(M["caliper"])
    sh_f = shield_mesh("MESH_BrakeShield_F", S.FRONT_ROTOR_D)
    sh_r = shield_mesh("MESH_BrakeShield_R", S.REAR_ROTOR_D)
    for m in (sh_f, sh_r):
        m.materials.append(M["zinc"])

    out = {}
    for axle, y, sysname in (("F", S.Y_FRONT_AXLE, "FRONT_WHEELS_AND_BRAKES"),
                             ("R", S.Y_REAR_AXLE, "REAR_WHEELS_AND_BRAKES")):
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{axle}{sd}"
            x = s * S.X_WHEEL
            c = (x, y, S.WHEEL_CENTER_Z)
            rz = 0.0 if s > 0 else math.pi
            wheel = L.assembly(f"WHEEL_{tag}", sysname, c)
            wheel["pivot_es"] = "Centro de rueda (eje de giro = X local)"
            L.explode(wheel, (s, 0, 0), 0.9, 4, "Ruedas",
                      f"Conjunto de rueda {'delantera' if axle == 'F' else 'trasera'} "
                      f"{'derecha' if s > 0 else 'izquierda'}", "V")
            t = instance(f"WHL_{tag}_Tire", tire, sysname, wheel, c, rz)
            L.explode(t, (s, 0, 0), 0.30, 6, "Ruedas", "Neumático Pirelli Scorpion ATR 285/65R20", "R",
                      note="Medidas verificadas; dibujo de la banda aproximado")
            r = instance(f"WHL_{tag}_Rim", rim, sysname, wheel, c, rz)
            L.explode(r, (s, 0, 0), 0.10, 6, "Ruedas", "Llanta de aleación 20 x 9.0J ET58.5", "R")
            cv = instance(f"WHL_{tag}_Cover_Core", covers[sd], sysname, wheel, c, rz if s > 0 else math.pi)
            if s < 0:
                cv.rotation_euler = (0, 0, math.pi)
            L.explode(cv, (s, 0, 0), 0.55, 6, "Ruedas", "Tapacubos aerodinámico «Core» 20\"", "R")
            lg = instance(f"WHL_{tag}_LugNuts", lugs, sysname, wheel, c, rz)
            L.explode(lg, (s, 0, 0), 0.40, 6, "Tornillería", "Tuercas de rueda (6), par 205 N·m", "R")
            # Frenos (unidos al portamangueta, no a la rueda)
            brake = L.assembly(f"BRAKE_{tag}", sysname, c)
            L.explode(brake, (s, 0, 0), 0.45, 4, "Frenos",
                      f"Freno {'delantero' if axle == 'F' else 'trasero'} "
                      f"{'derecho' if s > 0 else 'izquierdo'}", "R")
            # el disco queda dentro de la llanta, desplazado hacia dentro respecto al plano de montaje
            hub_x = x + s * (S.RIM_OFFSET - 0.052)
            rotor = rot_f if axle == "F" else rot_r
            ro = instance(f"BRK_{tag}_Rotor", rotor, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            L.explode(ro, (s, 0, 0), 0.12, 6, "Frenos",
                      f"Disco ventilado Ø{int(S.FRONT_ROTOR_D * 1000) if axle == 'F' else int(S.REAR_ROTOR_D * 1000)} mm",
                      "V")
            cal = cal_f if axle == "F" else cal_r
            # pinza detrás del eje (delante) / delante del eje (detrás), en la parte superior
            ang = math.radians(150 if axle == "F" else 30)
            cl = instance(f"BRK_{tag}_Caliper", cal, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            cl.rotation_euler = (ang if s > 0 else -ang + math.pi, 0, rz) if False else (0, 0, rz)
            cl.rotation_mode = "XYZ"
            cl.rotation_euler = (ang, 0, rz) if s > 0 else (math.pi - ang, 0, rz)
            L.explode(cl, (s * 0.4, -0.6 if axle == "F" else 0.6, 0.6), 0.22, 6, "Frenos",
                      "Pinza fija de 4 pistones" if axle == "F" else "Pinza flotante de 1 pistón con EPB", "V")
            shd = sh_f if axle == "F" else sh_r
            sh = instance(f"BRK_{tag}_Shield", shd, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            L.explode(sh, (-s, 0, 0), 0.10, 6, "Frenos", "Protector de polvo del disco", "A")
            out[tag] = wheel
    return out
