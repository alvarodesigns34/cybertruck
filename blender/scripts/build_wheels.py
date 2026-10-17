"""Ruedas, neumáticos y frenos del Cybertruck Cyberbeast.

[V] Llanta 20 x 9.0J ET58.5; neumático Pirelli Scorpion ATR 285/65R20 (manual del propietario);
    tuercas de 21 mm a 205 N·m; tapacubos sujeto con 8 grapas sobre un anillo de montaje y
    alineado con el diseño del neumático (manual de servicio, «Wheel Cover - Front - LH»).
[V] Discos ventilados: delantero Ø351 x 32 mm (pinza fija de 4 pistones, 2 tornillos de 24 mm a
    315 N·m); trasero Ø356 x 23 mm (pinza flotante de 1 pistón con freno de estacionamiento
    eléctrico, 2 tornillos de 21 mm a 150 N·m). Pastillas nuevas de 10 / 11 mm (manual de servicio).
[V] Buje atornillado al portamangueta con 4 tornillos; sensor de velocidad de rueda con 1 tornillo
    Torx T30; sensor TPMS en la válvula (manual de servicio).
[R] Tapacubos «Core» de 6 palas facetadas con cubo hexagonal (fotografía del manual de servicio).
[R] Dibujo de la banda: estructura de 5 hileras de tacos (hombros, intermedias y central en
    zigzag) con laminillas y tacos de flanco alternos, característica de los neumáticos
    «all-terrain» como el Scorpion ATR. No se ha copiado el dibujo exacto del fabricante.
[A] Inscripciones del flanco (marca, modelo, medida y marcado T0 de equipo original Tesla) en
    relieve, con una tipografía genérica y posiciones aproximadas.
"""

import math
import bpy
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L
import ct_parts as P

R_TIRE = S.TIRE_RADIUS
R_RIM = S.RIM_RADIUS
HALF_RIM = S.RIM_WIDTH_IN * 0.0254 / 2.0          # 0.1143
HALF_SECTION = S.TIRE_WIDTH / 2.0                  # 0.1425
TREAD_BASE = R_TIRE - 0.0145                       # fondo de los surcos (profundidad ~14,5 mm)

# Perfil exterior del flanco (radio, posición axial) usado también para las inscripciones
SIDEWALL = [(0.262, HALF_RIM + 0.004), (0.272, HALF_RIM + 0.010), (0.300, 0.131), (0.330, 0.139),
            (0.360, HALF_SECTION), (0.390, 0.140), (0.410, 0.133), (0.422, 0.124)]


def cyl(r, theta, a):
    """Coordenadas locales de rueda: eje = +X (a), ángulo en el plano YZ."""
    return (a, r * math.cos(theta), r * math.sin(theta))


def side_a(r):
    """Posición axial de la superficie del flanco exterior en el radio r."""
    return S.interp(SIDEWALL, r)


# ---------------------------------------------------------------------------
# Neumático (malla compartida por las cuatro ruedas)
# ---------------------------------------------------------------------------
def _tread_block(mb, poly_at, r0, r1, inset=0.0016, mat=0):
    """Taco de goma: polígono en coordenadas (axial a, ángulo t) extruido de r0 a r1.

    La cara superior se encoge `inset` hacia el centro (chaflán de desmoldeo).
    """
    n = len(poly_at)
    ca = sum(p[0] for p in poly_at) / n
    ct = sum(p[1] for p in poly_at) / n
    bot = [cyl(r0, t, a) for (a, t) in poly_at]
    top = []
    for (a, t) in poly_at:
        da, dt = ca - a, (ct - t) * r1
        ln = math.hypot(da, dt) or 1.0
        k = min(inset / ln, 0.45)
        top.append(cyl(r1, t + (ct - t) * k, a + da * k))
    cen = Vector(cyl((r0 + r1) / 2, ct, ca))
    mb.face(top, mat, want=Vector(cyl(1.0, ct, 0.0)))
    for i in range(n):
        j = (i + 1) % n
        q = [bot[i], bot[j], top[j], top[i]]
        c = sum((Vector(p) for p in q), Vector()) / 4
        mb.face(q, mat, want=c - cen)


def _sidewall_text(mb, text, size, r_center, theta_center, relief=0.0008, mat=2, track=1.0):
    """Inscripción en relieve curvada sobre el flanco exterior (lectura desde fuera)."""
    verts, faces = P.text_outline(text, size=size, extrude=relief / 2)
    if not verts:
        return
    xs = [v.x for v in verts]
    ys = [v.y for v in verts]
    xm = 0.5 * (min(xs) + max(xs))
    ym = 0.5 * (min(ys) + max(ys))
    mapped = []
    for v in verts:
        r = r_center + (v.y - ym)
        th = theta_center - (v.x - xm) * track / r_center
        a = side_a(r) + (v.z + relief / 2)
        mapped.append(cyl(r, th, a))
    for f in faces:
        mb.face([mapped[i] for i in f], mat)


def tire_mesh():
    name = "MESH_Tire_285_65R20"
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    seg = 160
    # Carcasa: perfil desde el talón exterior al interior
    prof = list(SIDEWALL) + [(TREAD_BASE + 0.002, 0.118), (TREAD_BASE, 0.100), (TREAD_BASE + 0.0015, 0.0),
                             (TREAD_BASE, -0.100), (TREAD_BASE + 0.002, -0.118)]
    prof += [(r, -a) for (r, a) in reversed(SIDEWALL)]
    rings = [[cyl(r, 2 * math.pi * k / seg, a) for k in range(seg)] for (r, a) in prof]
    for i in range(len(rings) - 1):
        mat = 0 if abs(prof[i][1]) < 0.119 and abs(prof[i + 1][1]) < 0.119 else 1
        mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=mat,
                      want_fn=lambda c: Vector((0, c.y, c.z)) if abs(c.x) < 0.125 else Vector((c.x, 0, 0)))
    mb.quad_strip(rings[-1], rings[0], closed=True, mat=1, want_fn=lambda c: Vector((0, -c.y, -c.z)))

    # Dibujo de la banda (56 pasos): hombros, intermedias con laminilla y central en zigzag
    pitches = 56
    dp = 2 * math.pi / pitches
    rt, rb = R_TIRE, TREAD_BASE - 0.0005
    sipe = 0.0012 / rt                       # anchura angular de las laminillas (~1,2 mm)
    for k in range(pitches):
        t = k * dp
        alt = 1 if k % 2 else -1
        # --- hilera central: bloques en chevron alternados
        t0 = t + 0.10 * dp + alt * 0.10 * dp
        t1 = t0 + 0.62 * dp
        ch = 0.10 * dp
        _tread_block(mb, [(-0.020, t0), (0.0, t0 + ch), (0.020, t0), (0.020, t1), (0.0, t1 + ch), (-0.020, t1)],
                     rb, rt - 0.0004)
        # --- hileras intermedias: paralelogramos inclinados partidos por una laminilla
        for sg in (1, -1):
            a0, a1 = sg * 0.028, sg * 0.074
            sk = 0.22 * dp * sg                       # inclinación (desplazamiento angular a lo ancho)
            base = t + (0.55 if sg > 0 else 0.05) * dp
            tm = base + 0.36 * dp
            for (ta, tb) in ((base, tm - sipe), (tm + sipe, base + 0.74 * dp)):
                poly = [(a0, ta), (a1, ta + sk), (a1, tb + sk), (a0, tb)]
                _tread_block(mb, poly if sg > 0 else poly[::-1], rb, rt)
        # --- hombros: bloques anchos con escalón y prolongación alterna hacia el flanco
        for sg in (1, -1):
            off = 0.0 if sg > 0 else 0.5 * dp
            ta, tb = t + off + 0.06 * dp, t + off + 0.80 * dp
            a0, a1 = sg * 0.081, sg * 0.121
            poly = [(a0, ta + 0.05 * dp), (a1, ta), (a1, tb), (a0, tb - 0.05 * dp)]
            _tread_block(mb, poly if sg > 0 else poly[::-1], rb + 0.001, rt)
            # escalón lateral («stone ejector») en el hombro
            _tread_block(mb, [(sg * 0.121, ta + 0.1 * dp), (sg * 0.128, ta + 0.12 * dp),
                              (sg * 0.128, tb - 0.12 * dp), (sg * 0.121, tb - 0.1 * dp)][::sg],
                         0.418, rt - 0.006)
            # tacos del flanco superior: uno largo y uno corto alternados
            if (k + (0 if sg > 0 else 1)) % 2 == 0:
                rlo = 0.398
            else:
                rlo = 0.410
            a_in, a_out = sg * 0.124, sg * 0.137
            bot = [cyl(rlo, ta + 0.08 * dp, a_in), cyl(rlo, tb - 0.08 * dp, a_in),
                   cyl(0.426, tb - 0.04 * dp, a_in), cyl(0.426, ta + 0.04 * dp, a_in)]
            top = [cyl(rlo + 0.004, ta + 0.12 * dp, a_out), cyl(rlo + 0.004, tb - 0.12 * dp, a_out),
                   cyl(0.420, tb - 0.08 * dp, a_out - sg * 0.004), cyl(0.420, ta + 0.08 * dp, a_out - sg * 0.004)]
            cen = sum((Vector(p) for p in bot + top), Vector()) / 8
            mb.face(top, 1, want=(sg, 0, 0))
            for i in range(4):
                j = (i + 1) % 4
                q = [bot[i], bot[j], top[j], top[i]]
                c = sum((Vector(p) for p in q), Vector()) / 4
                mb.face(q, 1, want=c - cen)

    # Inscripciones del flanco exterior (dos veces cada una, como en un neumático real)
    for base_t in (math.pi / 2, -math.pi / 2):
        _sidewall_text(mb, "PIRELLI", 0.030, 0.386, base_t, relief=0.0009, track=1.12)
        _sidewall_text(mb, "SCORPION ATR", 0.019, 0.386, base_t + math.pi / 2, relief=0.0008, track=1.08)
        _sidewall_text(mb, "285/65 R20", 0.011, 0.300, base_t + 0.22, relief=0.0006)
        _sidewall_text(mb, "T0", 0.013, 0.300, base_t - 0.30, relief=0.0006)
    _sidewall_text(mb, "M+S", 0.010, 0.300, math.pi + 0.55, relief=0.0006)
    _sidewall_text(mb, "TUBELESS", 0.008, 0.300, 0.65, relief=0.0005)

    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
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
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(35))
    return me




def valve_mesh(name):
    """Válvula de aluminio con sensor TPMS (fijado por dentro de la llanta) y tapón."""
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    t = math.radians(95.0)
    base = Vector(cyl(0.240, t, HALF_RIM - 0.020))
    tip = Vector(cyl(0.250, t, HALF_RIM + 0.020))
    ax = (tip - base).normalized()
    L.lathe(mb, [(0.0045, 0.0), (0.0045, 0.030), (0.0040, 0.032), (0.0040, 0.040)], tuple(base), tuple(ax), 12, 0)
    L.lathe(mb, [(0.0052, 0.040), (0.0052, 0.052), (0.0045, 0.054), (0.0, 0.055)], tuple(base), tuple(ax), 12, 1)
    # sensor TPMS en el interior del barril
    c = Vector(cyl(0.236, t, HALF_RIM - 0.045))
    P.rbox(mb, c, (0.040, 0.024, 0.018), 0.004, 1, P.basis(Vector(cyl(1.0, t, 0.0)), (1, 0, 0)), 2)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = True
    return me


# ---------------------------------------------------------------------------
# Tapacubos aerodinámico «Core»: cubo hexagonal, 6 palas facetadas y bolsillos entre palas
# ---------------------------------------------------------------------------
def _polar(r, phi, a):
    return Vector((a, r * math.cos(phi), r * math.sin(phi)))


def _frustum(mb, poly2d_bot, poly2d_top, a_bot, a_top, mat_top, mat_side):
    """Prisma facetado entre dos polígonos (y, z) a alturas axiales distintas (chaflanes)."""
    bot = [Vector((a_bot, y, z)) for (y, z) in poly2d_bot]
    top = [Vector((a_top, y, z)) for (y, z) in poly2d_top]
    c = (sum(bot, Vector()) + sum(top, Vector())) / (len(bot) + len(top))
    mb.face([tuple(p) for p in top], mat_top, want=(1, 0, 0))
    mb.face([tuple(p) for p in bot], mat_side, want=(-1, 0, 0))
    n = len(bot)
    for i in range(n):
        j = (i + 1) % n
        q = [bot[i], bot[j], top[j], top[i]]
        mb.face([tuple(p) for p in q], mat_side, want=(sum(q, Vector()) / 4) - c)


def cover_mesh(name, mirror=False):
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    fa = HALF_RIM + 0.012                  # plano exterior de la pestaña de la llanta
    sgn = 1                                # la versión izquierda se obtiene por simetría
    seg = 96
    # Disco base (fondo de los bolsillos) ligeramente cóncavo, con labio exterior
    prof = [(0.264, fa - 0.004), (0.262, fa + 0.004), (0.244, fa + 0.007), (0.236, fa + 0.002),
            (0.150, fa - 0.006), (0.070, fa - 0.002), (0.0, fa - 0.002)]
    rings = L.lathe(mb, prof[:-1], (0, 0, 0), (1, 0, 0), seg, 0)
    mb.face(rings[-1], 0, want=(1, 0, 0))
    back = [cyl(0.264, 2 * math.pi * k / seg, fa - 0.022) for k in range(seg)]
    mb.quad_strip(rings[0], back, closed=True, mat=0, want_fn=lambda c: Vector((0, c.y, c.z)))
    mb.face(back, 0, want=(-1, 0, 0))

    def pt(r, phi):
        return (r * math.cos(phi), r * math.sin(phi))

    sweep = 0.20                           # barrido angular de las palas entre el cubo y el borde
    for k in range(6):
        phi = 2 * math.pi * k / 6 + math.pi / 6
        # --- pala: tablón ancho y plano con chaflán claro (material 3)
        def ang(r):
            return phi + sgn * sweep * (r - 0.07) / 0.18
        r0, r1 = 0.070, 0.252
        w0, w1 = 0.026, 0.040
        bot = [pt(r0, ang(r0) - w0 / r0), pt(r1, ang(r1) - w1 / r1), pt(r1, ang(r1) + w1 / r1),
               pt(r0, ang(r0) + w0 / r0)]
        ins = 0.007
        top = [pt(r0 + ins, ang(r0) - (w0 - ins) / r0), pt(r1 - 0.004, ang(r1) - (w1 - ins) / r1),
               pt(r1 - 0.004, ang(r1) + (w1 - ins) / r1), pt(r0 + ins, ang(r0) + (w0 - ins) / r0)]
        _frustum(mb, bot, top, fa - 0.003, fa + 0.0125, 1, 3)
        # --- panel del sector (nivel intermedio) entre esta pala y la siguiente
        phi2 = phi + 2 * math.pi / 6
        def ang2(r):
            return phi2 + sgn * sweep * (r - 0.07) / 0.18
        ra, rb = 0.080, 0.236
        pa = [pt(ra, ang(ra) + 0.026 / ra), pt(rb, ang(rb) + 0.040 / rb),
              pt(rb, 0.5 * (ang(rb) + ang2(rb)) - 0.01), pt(0.14, 0.5 * (ang(0.14) + ang2(0.14)))]
        pt_in = [(p[0] * 0.985, p[1] * 0.985) for p in pa]
        _frustum(mb, pa, pt_in, fa - 0.003, fa + 0.0075, 1, 3)
        # --- bolsillo triangular oscuro (abertura de ventilación del freno)
        mid = 0.5 * (ang(0.2) + ang2(0.2))
        tri = [pt(0.125, mid + 0.08), pt(0.226, mid + 0.02), pt(0.226, mid + 0.34)]
        tri_top = [(p[0] * 0.995, p[1] * 0.995) for p in tri]
        _frustum(mb, tri, tri_top, fa - 0.004, fa + 0.0035, 2, 2)
    # Cubo hexagonal con tapa central escalonada
    hexo = [pt(0.078, math.pi / 6 + k * math.pi / 3) for k in range(6)]
    hexm = [pt(0.068, math.pi / 6 + k * math.pi / 3) for k in range(6)]
    _frustum(mb, hexo, hexm, fa - 0.002, fa + 0.0155, 1, 3)
    hexi = [pt(0.050, k * math.pi / 3) for k in range(6)]
    hexi2 = [pt(0.046, k * math.pi / 3) for k in range(6)]
    _frustum(mb, hexi, hexi2, fa + 0.0155, fa + 0.0175, 2, 3)
    verts, faces = mb.verts, mb.faces
    if mirror:
        verts = [(x, -y, z) for (x, y, z) in verts]
        faces = [list(reversed(f)) for f in faces]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], L.orient_closed_components(verts, faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = False
    return me


def hub_mesh(name, driven=True):
    """Buje con brida de 6 espárragos (PCD 135 mm), rodamiento y anillo del sensor ABS."""
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    a_face = S.RIM_OFFSET - 0.004          # cara de apoyo del disco/llanta
    # brida de 6 lóbulos
    L.lathe(mb, [(0.035, a_face), (0.086, a_face), (0.086, a_face - 0.012), (0.060, a_face - 0.016),
                 (0.058, a_face - 0.040), (0.072, a_face - 0.042), (0.072, a_face - 0.075),
                 (0.050, a_face - 0.080), (0.040, a_face - 0.080)], (0, 0, 0), (1, 0, 0), 48, 0)
    # centrador y estriado del semieje
    L.lathe(mb, [(0.035, a_face), (0.035, a_face + 0.012), (0.030, a_face + 0.014), (0.0 if not driven else 0.016,
                 a_face + 0.014)], (0, 0, 0), (1, 0, 0), 32, 1)
    if driven:
        L.lathe(mb, [(0.016, a_face + 0.014), (0.016, a_face + 0.004), (0.0, a_face + 0.004)], (0, 0, 0),
                (1, 0, 0), 6, 2, phase=math.pi / 6)
    # espárragos de rueda (6 x M14)
    for k in range(6):
        c = Vector(cyl(0.135 / 2, 2 * math.pi * k / 6, a_face))
        L.lathe(mb, [(0.0068, -0.010), (0.0068, 0.055), (0.005, 0.058), (0.0, 0.058)], tuple(c), (1, 0, 0), 10, 2)
    # anillo codificador del sensor de velocidad (lado interior)
    P.tube_ring(mb, (a_face - 0.083, 0, 0), (1, 0, 0), 0.050, 0.066, 0.006, 40, 2)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(35))
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
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
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
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
    return me




def _arc_body(mb, r_in, r_out, a0, a1, t0, t1, nseg=10, mat=0, round_out=0.0):
    """Cuerpo en arco (sector anular extruido axialmente) con el borde exterior redondeado."""
    rings = []
    for i in range(nseg + 1):
        t = t0 + (t1 - t0) * i / nseg
        e = math.sin(math.pi * i / nseg) ** 0.35 if round_out else 1.0
        ro = r_in + (r_out - r_in) * (0.82 + 0.18 * e) if round_out else r_out
        rings.append([cyl(r_in, t, a0), cyl(ro, t, a0), cyl(ro, t, a1), cyl(r_in, t, a1)])
    cen_t = 0.5 * (t0 + t1)
    for i in range(nseg):
        for k in range(4):
            kk = (k + 1) % 4
            q = [rings[i][k], rings[i][kk], rings[i + 1][kk], rings[i + 1][k]]
            c = sum((Vector(p) for p in q), Vector()) / 4
            tm = t0 + (t1 - t0) * (i + 0.5) / nseg
            mid = Vector(cyl(0.5 * (r_in + r_out), tm, 0.5 * (a0 + a1)))
            mb.face(q, mat, want=c - mid)
    mb.face(rings[0], mat, want=Vector(cyl(1, t0, 0)) - Vector(cyl(1, cen_t, 0)))
    mb.face(rings[-1], mat, want=Vector(cyl(1, t1, 0)) - Vector(cyl(1, cen_t, 0)))


def caliper_mesh(name, diam, thick, front=True):
    """Pinza fija de 4 pistones (delante) o flotante de 1 pistón con motor EPB (detrás).

    Materiales: 0 cuerpo, 1 tornillería y purgadores, 2 guardapolvos.
    """
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    ro = diam / 2
    gap = thick / 2 + 0.012                      # holgura para las pastillas
    if front:
        span = 0.66
        # mitad exterior e interior (fijas), con el borde exterior redondeado
        for sg in (1, -1):
            a0, a1 = sg * gap, sg * (gap + 0.034)
            _arc_body(mb, ro - 0.066, ro + 0.014, min(a0, a1), max(a0, a1), -span / 2, span / 2, 12, 0, 1)
            # abultamientos de los dos cilindros de pistón en cada mitad
            for k in (-1, 1):
                t = k * span * 0.24
                c = Vector(cyl(ro - 0.030, t, sg * (gap + 0.034)))
                L.lathe(mb, [(0.0, 0.0), (0.026, 0.0), (0.026, 0.006), (0.020, 0.010), (0.0, 0.011)], tuple(c),
                        (sg, 0, 0), 24, 0)
        # puentes sobre el disco en los extremos (las pastillas quedan visibles por la ventana central)
        for tt in (-span / 2, span / 2 - 0.14):
            _arc_body(mb, ro + 0.003, ro + 0.016, -gap - 0.034, gap + 0.034, tt, tt + 0.14, 3, 0)
        # tornillos de los puentes y purgadores en la mitad interior
        for tt in (-span / 2 + 0.07, span / 2 - 0.07):
            P.flange_bolt(mb, cyl(ro + 0.016, tt, 0.0), cyl(1, tt, 0.0), 0.008, 1)
            P.cyl(mb, cyl(ro + 0.010, tt * 0.8, -gap - 0.020), cyl(ro + 0.026, tt * 0.8, -gap - 0.020), 0.004, 8, 1)
        # orejetas de fijación radial al portamangueta (2 tornillos de 24 mm)
        for tt in (-span / 2 - 0.02, span / 2 + 0.02):
            _arc_body(mb, ro - 0.076, ro - 0.030, -gap - 0.050, -gap - 0.014, tt - 0.05, tt + 0.05, 2, 0)
            P.flange_bolt(mb, cyl(ro - 0.053, tt, -gap - 0.050), (-1, 0, 0), 0.014, 1)
    else:
        span = 0.50
        # soporte (carrier) con brazos sobre el disco
        _arc_body(mb, ro - 0.060, ro + 0.006, -gap - 0.010, gap + 0.010, -span / 2 - 0.08, -span / 2 + 0.02, 3, 0)
        _arc_body(mb, ro - 0.060, ro + 0.006, -gap - 0.010, gap + 0.010, span / 2 - 0.02, span / 2 + 0.08, 3, 0)
        # alojamiento interior del pistón y dedo exterior
        _arc_body(mb, ro - 0.062, ro + 0.016, -gap - 0.046, -gap, -span / 2, span / 2, 10, 0, 1)
        _arc_body(mb, ro - 0.046, ro + 0.016, gap, gap + 0.016, -span * 0.42, span * 0.42, 8, 0, 1)
        _arc_body(mb, ro + 0.004, ro + 0.018, -gap - 0.046, gap + 0.016, -span * 0.38, span * 0.38, 6, 0)
        # pistón único (Ø ~ 54 mm) y motor del freno de estacionamiento eléctrico
        c = Vector(cyl(ro - 0.026, 0.0, -gap - 0.046))
        L.lathe(mb, [(0.0, 0.0), (0.033, 0.0), (0.033, 0.012), (0.028, 0.018), (0.0, 0.019)], tuple(c),
                (-1, 0, 0), 28, 0)
        c = Vector(cyl(ro - 0.022, 0.10, -gap - 0.060))
        L.lathe(mb, [(0.0, 0.0), (0.026, 0.0), (0.026, -0.082), (0.022, -0.090), (0.0, -0.091)], tuple(c),
                (1, 0, 0), 24, 0)
        P.rbox(mb, c + Vector((-0.04, 0, 0)) + Vector(cyl(0.03, 0.10, 0)), (0.05, 0.03, 0.03), 0.004, 1, None, 2)
        # pasadores guía con guardapolvos y tornillos al portamangueta (21 mm)
        for tt in (-span / 2 - 0.03, span / 2 + 0.03):
            P.boot(mb, cyl(ro - 0.040, tt, -gap - 0.012), cyl(ro - 0.040, tt, -gap - 0.050), 0.008, 0.008, 3, 12, 2)
            P.flange_bolt(mb, cyl(ro - 0.040, tt, -gap - 0.052), (-1, 0, 0), 0.012, 1)
        P.cyl(mb, cyl(ro + 0.010, 0.18, -gap - 0.030), cyl(ro + 0.026, 0.18, -gap - 0.030), 0.004, 8, 1)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(40))
    return me


def pads_mesh(name, diam, thick, front=True):
    """Pastillas: placa de acero + material de fricción (10 mm delante, 11 mm detrás, nuevas)."""
    me = bpy.data.meshes.get(name)
    if me:
        bpy.data.meshes.remove(me)
    mb = L.MeshBuilder(merge=1e-6)
    ro = diam / 2
    span = 0.56 if front else 0.42
    fr = 0.010 if front else 0.011
    for sg in (1, -1):
        a_f0 = sg * (thick / 2 + 0.0005)
        a_f1 = sg * (thick / 2 + 0.0005 + fr * 0.95)
        _arc_body(mb, ro - 0.058, ro - 0.004, min(a_f0, a_f1), max(a_f0, a_f1), -span / 2, span / 2, 8, 1)
        a_b1 = sg * (abs(a_f1) + 0.005)
        _arc_body(mb, ro - 0.062, ro + 0.002, min(a_f1, a_b1), max(a_f1, a_b1), -span / 2 - 0.02, span / 2 + 0.02, 8, 0)
    me = bpy.data.meshes.new(name)
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
    me.validate()
    for p, mi in zip(me.polygons, mb.mats):
        p.material_index = mi
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
    me.from_pydata(mb.verts, [], L.orient_closed_components(mb.verts, mb.faces))
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
    for k in ("rubber", "rubber_side", "tire_letters"):
        tire.materials.append(M[k])
    rim = rim_mesh("MESH_Rim_20x9")
    rim.materials.append(M["wheel_alloy"])
    lugs = lug_mesh("MESH_LugNuts_6x")
    lugs.materials.append(M["zinc"])
    valve = valve_mesh("MESH_Valve_TPMS")
    for k in ("alu_machined", "plastic_black", "plastic_black"):
        valve.materials.append(M[k])
    covers = {}
    for sd, mir in (("R", False), ("L", True)):
        cm = cover_mesh(f"MESH_WheelCover_Core_{sd}", mirror=mir)
        for k in ("wheel_cover", "wheel_cover", "plastic_black", "wheel_cover_edge"):
            cm.materials.append(M[k])
        covers[sd] = cm
    rot_f = rotor_mesh("MESH_Rotor_Front_351x32", S.FRONT_ROTOR_D, S.FRONT_ROTOR_T)
    rot_r = rotor_mesh("MESH_Rotor_Rear_356x23", S.REAR_ROTOR_D, S.REAR_ROTOR_T)
    for m in (rot_f, rot_r):
        m.materials.append(M["rotor"])
        m.materials.append(M["rotor"])
    cal_f = caliper_mesh("MESH_Caliper_Front_4P", S.FRONT_ROTOR_D, S.FRONT_ROTOR_T, True)
    cal_r = caliper_mesh("MESH_Caliper_Rear_1P_EPB", S.REAR_ROTOR_D, S.REAR_ROTOR_T, False)
    for m in (cal_f, cal_r):
        for k in ("caliper", "zinc", "bushing"):
            m.materials.append(M[k])
    pad_f = pads_mesh("MESH_BrakePads_Front", S.FRONT_ROTOR_D, S.FRONT_ROTOR_T, True)
    pad_r = pads_mesh("MESH_BrakePads_Rear", S.REAR_ROTOR_D, S.REAR_ROTOR_T, False)
    for m in (pad_f, pad_r):
        m.materials.append(M["steel_black"])
        m.materials.append(M["brake_pad"])
    sh_f = shield_mesh("MESH_BrakeShield_F", S.FRONT_ROTOR_D)
    sh_r = shield_mesh("MESH_BrakeShield_R", S.REAR_ROTOR_D)
    for m in (sh_f, sh_r):
        m.materials.append(M["zinc"])
    hub_f = hub_mesh("MESH_Hub_Front_Driven", True)
    hub_r = hub_mesh("MESH_Hub_Rear_Driven", True)
    for m in (hub_f, hub_r):
        for k in ("steel_bare", "alu_machined", "zinc"):
            m.materials.append(M[k])

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
            L.explode(t, (s, 0, 0), 0.30, 6, "Ruedas", "Neumático Pirelli Scorpion ATR 285/65R20 (T0)", "R",
                      note="Medidas verificadas; dibujo de 5 hileras reconstruido; inscripciones aproximadas")
            r = instance(f"WHL_{tag}_Rim", rim, sysname, wheel, c, rz)
            L.explode(r, (s, 0, 0), 0.10, 6, "Ruedas", "Llanta de aleación 20 x 9.0J ET58.5 (Stealth Black)", "R")
            cv = instance(f"WHL_{tag}_Cover_Core", covers[sd], sysname, wheel, c, rz)
            L.explode(cv, (s, 0, 0), 0.55, 6, "Ruedas",
                      "Tapacubos aerodinámico «Core» 20\" (8 grapas sobre anillo de montaje)", "R")
            lg = instance(f"WHL_{tag}_LugNuts", lugs, sysname, wheel, c, rz)
            L.explode(lg, (s, 0, 0), 0.40, 6, "Tornillería", "Tuercas de rueda (6), llave de 21 mm, 205 N·m", "R")
            vl = instance(f"WHL_{tag}_Valve_TPMS", valve, sysname, wheel, c, rz)
            L.explode(vl, (s, 0, 0.5), 0.22, 6, "Ruedas", "Válvula con sensor de presión TPMS", "R")
            # Frenos (unidos al portamangueta, no a la rueda)
            brake = L.assembly(f"BRAKE_{tag}", sysname, c)
            L.explode(brake, (s, 0, 0), 0.45, 4, "Frenos",
                      f"Freno {'delantero' if axle == 'F' else 'trasero'} "
                      f"{'derecho' if s > 0 else 'izquierdo'}", "R")
            hub_x = x + s * (S.RIM_OFFSET - 0.052)
            rotor = rot_f if axle == "F" else rot_r
            ro = instance(f"BRK_{tag}_Rotor", rotor, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            L.explode(ro, (s, 0, 0), 0.12, 6, "Frenos",
                      f"Disco ventilado Ø{int(S.FRONT_ROTOR_D * 1000) if axle == 'F' else int(S.REAR_ROTOR_D * 1000)} mm",
                      "V")
            ang = math.radians(150 if axle == "F" else 30)
            rot = (ang, 0, rz) if s > 0 else (math.pi - ang, 0, rz)
            cal = cal_f if axle == "F" else cal_r
            cl = instance(f"BRK_{tag}_Caliper", cal, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            cl.rotation_euler = rot
            cdir = (s * 0.4, -0.6 if axle == "F" else 0.6, 0.6)
            L.explode(cl, cdir, 0.22, 6, "Frenos",
                      "Pinza fija de 4 pistones (2 tornillos de 24 mm, 315 N·m)" if axle == "F"
                      else "Pinza flotante de 1 pistón con freno de estacionamiento eléctrico (EPB)", "V")
            pads = instance(f"BRK_{tag}_Pads", pad_f if axle == "F" else pad_r, sysname, brake,
                            (hub_x, y, S.WHEEL_CENTER_Z), rz)
            pads.rotation_euler = rot
            L.explode(pads, cdir, 0.36, 6, "Frenos",
                      f"Pastillas de freno ({'10' if axle == 'F' else '11'} mm de material nuevo)", "R")
            shd = sh_f if axle == "F" else sh_r
            sh = instance(f"BRK_{tag}_Shield", shd, sysname, brake, (hub_x, y, S.WHEEL_CENTER_Z), rz)
            L.explode(sh, (-s, 0, 0), 0.10, 6, "Frenos", "Protector de polvo del disco", "A")
            hb = instance(f"SUS_{tag}_Hub", hub_f if axle == "F" else hub_r,
                          "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION", brake, c, rz)
            L.explode(hb, (s, 0, 0.2), 0.20, 6, "Suspensión",
                      "Buje motriz con rodamiento y 6 espárragos (4 tornillos al portamangueta, 105 N·m)", "R")
            out[tag] = wheel
    return out
