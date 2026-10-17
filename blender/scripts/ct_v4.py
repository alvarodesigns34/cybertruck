"""Formas de alto detalle de la versión 4 («coche completo»).

La versión 4 añade el interior funcional de los conjuntos que hasta la versión 3 eran carcasas cerradas
(motores, reductoras, inversores, juntas homocinéticas, rodamientos, pinzas, actuadores, climatizador,
asientos…) y la tornillería que los une. Amplía la capa declarativa de `ct_v3` con formas mecánicas:

  * engranajes rectos y helicoidales (dentado exterior o interior) y ejes estriados,
  * rodamientos de bolas abiertos (aros, jaula y bolas), esferas y toros,
  * paquetes de chapa magnética del estátor con ranuras, cabezas de bobina de horquillas o de devanado
    distribuido, rotores de jaula de ardilla y de imanes permanentes,
  * placas electrónicas con componentes, muelles helicoidales, tornillos con rosca, abrazaderas,
  * tubos curvados (bastidores de asiento, tuberías rígidas).

Todas las formas se describen en coordenadas de mundo (o en las locales de un objeto existente, con
`frame=`) y, si `mirror=True`, se genera la pareja izquierda reflejando la malla ya construida e invirtiendo
el sentido de sus caras, de modo que las normales siguen hacia fuera.

Criterio de fidelidad (ver docs/research-and-fidelity.md §10): la existencia y la función de estas piezas
son necesarias para que el vehículo funcione y, en muchos casos, constan en el manual de servicio o en los
desmontajes de Munro; su forma, sus dimensiones y el número de dientes, bolas o ranuras son
reconstrucciones de ingeniería («Reconstruido») o interpretaciones («Aproximado») que no proceden de planos.
"""

import math
import random
from mathutils import Vector, Matrix
import ct_lib as L
import ct_parts as P
import ct_v3 as V3

# Formas de la versión 3 reutilizables tal cual
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, rivet, ball, boot, ribs, prism  # noqa: F401

STAGE = V3.STAGE
SIDE_ES = V3.SIDE_ES


# ---------------------------------------------------------------------------
# Constructores de formas nuevas (tuplas; la última posición útil es el material)
# ---------------------------------------------------------------------------
def gear(c, axis, r_root, r_tip, width, teeth, bore=0.0, helix=0.0, m=0, slices=None, phase=0.0):
    """Engranaje de dentado exterior (recto o helicoidal: `helix` en grados)."""
    return ("gear", c, axis, r_root, r_tip, width, teeth, bore, helix, m, slices, phase)


def ring_gear(c, axis, r_out, r_root, r_tip, width, teeth, helix=0.0, m=0, phase=0.0):
    """Corona de dentado interior; también sirve para el paquete de chapas del estátor con ranuras."""
    return ("igear", c, axis, r_out, r_root, r_tip, width, teeth, helix, m, phase)


def spline(c, axis, r, length, teeth=24, depth=0.0012, bore=0.0, m=0):
    """Eje o manguito estriado."""
    return gear(c, axis, r - depth, r, length, teeth, bore, 0.0, m)


def sphere(c, r, seg=10, rings=6, m=0):
    return ("sphere", c, r, seg, rings, m)


def torus(c, axis, R, r, seg=32, seg2=8, m=0):
    return ("torus", c, axis, R, r, seg, seg2, m)


def bearing(c, axis, rin, rout, width, balls=None, m=0, mball=None, rows=1, seals=False):
    """Rodamiento rígido de bolas abierto: aro interior, aro exterior, jaula y bolas."""
    return ("bearing", c, axis, rin, rout, width, balls, m, m if mball is None else mball, rows, seals)


def taper(c, axis, profile, seg=24, m=0, phase=0.0):
    """Sólido de revolución a partir de un perfil (radio, posición axial) cerrado sobre el eje."""
    return ("lathe", c, axis, profile, seg, m, phase)


def coil(c, axis, r, wire, turns, length, seg=8, m=0, ground=True):
    """Muelle helicoidal de compresión (extremos cerrados si `ground`)."""
    return ("coil", c, axis, r, wire, turns, length, seg, m, ground)


def tube(path, r, seg=10, samples=4, m=0, r_in=None):
    """Tubo o varilla curvados por una trayectoria suavizada (sin límite de altura libre)."""
    return ("tube", path, r, seg, samples, m, r_in)


def screw(pos, axis, d=0.008, length=0.025, m=0, head="hex", pitch=None, washer=True):
    """Tornillo con cabeza (hex, torx, allen, flange) y caña roscada (rosca en anillos)."""
    return ("screw", pos, axis, d, length, m, head, pitch, washer)


def pcb(c, size, normal, up, comps=40, seed=1, m_board=0, m_chip=1, m_cap=2, m_conn=3, m_metal=4):
    """Placa de circuito impreso con componentes (chips, condensadores, conectores, bobinas)."""
    return ("pcb", c, size, normal, up, comps, seed, m_board, m_chip, m_cap, m_conn, m_metal)


def stator(c, axis, r_in, r_out, length, slots, slot_depth, m=0):
    """Paquete de chapa magnética con ranuras abiertas hacia el entrehierro."""
    return ring_gear(c, axis, r_out, r_in + slot_depth, r_in, length, slots, 0.0, m)


def hairpins(c, axis, r0, r1, length, count, height, m=0, layers=2, end=1):
    """Cabezas de bobina de horquillas (hairpin) en un extremo del estátor."""
    return ("hairpins", c, axis, r0, r1, length, count, height, m, layers, end)


def winding(c, axis, r0, r1, length, height, m=0, m_lace=1, lacing=24):
    """Cabezas de bobina de devanado distribuido (rotor de inducción) con atado de cordón."""
    return ("winding", c, axis, r0, r1, length, height, m, m_lace, lacing)


def hose_clamp(c, axis, r, w=0.008, m=0):
    """Abrazadera de banda (oreja Oetiker) sobre un fuelle o manguera."""
    return ("hclamp", c, axis, r, w, m)


def fins(c, axis, up, size, n, t=0.0012, m=0):
    """Aletas paralelas (radiadores, disipadores): `size` = (reparto, fondo, alto)."""
    return ("fins", c, axis, up, size, n, t, m)


def belt(c1, r1, c2, r2, axis, width, t=0.003, n=24):
    """Correa cerrada alrededor de dos poleas (envolvente convexa de las dos circunferencias)."""
    c1, c2 = Vector(c1), Vector(c2)
    w = Vector(axis).normalized()
    u = c2 - c1
    u = (u - w * u.dot(w)).normalized()
    v = w.cross(u)
    pts2 = set()
    for c, r in ((c1, r1 + t / 2), (c2, r2 + t / 2)):
        for k in range(n):
            a = 2 * math.pi * k / n
            p = c + (u * math.cos(a) + v * math.sin(a)) * r
            pts2.add((round((p - c1).dot(u), 6), round((p - c1).dot(v), 6)))
    pts2 = sorted(pts2)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts2:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts2):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    path = [tuple(c1 + u * x + v * y) for x, y in lower[:-1] + upper[:-1]]
    return ("belt", path, width, t, tuple(w))


def xf(matrix, shapes):
    """Aplica una matriz 4x4 (local → mundo) a un grupo de formas descritas en coordenadas locales."""
    return ("xf", matrix, shapes)


# ---------------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------------
def _frame(axis):
    return L.frame_from_axis(axis)


def _gear_outline(teeth, r_root, r_tip, phase=0.0, internal=False):
    """Contorno de un engranaje: 4 puntos por diente (pie, cabeza, cabeza, pie)."""
    pts = []
    p = 2 * math.pi / teeth
    # proporciones de un dentado de evolvente aproximado por trapecios
    fr = (0.0, 0.17, 0.33, 0.50) if not internal else (0.0, 0.20, 0.38, 0.58)
    for k in range(teeth):
        a0 = phase + k * p
        for f, r in zip(fr, (r_root, r_tip, r_tip, r_root)):
            pts.append((a0 + f * p, r))
    return pts


def _emit_gear(mb, c, axis, r_root, r_tip, width, teeth, bore, helix, m, slices, phase):
    c = Vector(c)
    u, v, w = _frame(axis)
    outline = _gear_outline(teeth, r_root, r_tip, phase)
    n = len(outline)
    tw = math.tan(math.radians(helix)) * width / max(r_tip, 1e-6) if helix else 0.0
    ns = slices or (4 if helix else 1)
    rings_o, rings_i = [], []
    for i in range(ns + 1):
        t = i / ns
        a_off = tw * (t - 0.5)
        z = -width / 2 + width * t
        rings_o.append([tuple(c + w * z + (u * math.cos(a + a_off) + v * math.sin(a + a_off)) * r)
                        for a, r in outline])
        if bore > 0:
            rings_i.append([tuple(c + w * z + (u * math.cos(a + a_off) + v * math.sin(a + a_off)) * bore)
                            for a, _ in outline])
    for i in range(ns):
        for k in range(n):
            kk = (k + 1) % n
            q = [rings_o[i][k], rings_o[i][kk], rings_o[i + 1][kk], rings_o[i + 1][k]]
            cc = sum((Vector(x) for x in q), Vector()) / 4
            rad = cc - c - w * (cc - c).dot(w)
            mb.face(q, m, want=rad)
            if bore > 0:
                q = [rings_i[i][k], rings_i[i][kk], rings_i[i + 1][kk], rings_i[i + 1][k]]
                mb.face(q, m, want=-rad)
    for i, sg in ((0, -1), (ns, 1)):
        if bore > 0:
            for k in range(n):
                kk = (k + 1) % n
                mb.face([rings_o[i][k], rings_o[i][kk], rings_i[i][kk], rings_i[i][k]], m, want=w * sg)
        else:
            mb.face(rings_o[i], m, want=w * sg)


def _emit_igear(mb, c, axis, r_out, r_root, r_tip, width, teeth, helix, m, phase):
    """Corona interior: contorno exterior circular y dientes hacia el centro (r_tip < r_root)."""
    c = Vector(c)
    u, v, w = _frame(axis)
    inner = _gear_outline(teeth, r_root, r_tip, phase, internal=True)
    n = len(inner)
    tw = math.tan(math.radians(helix)) * width / max(r_out, 1e-6) if helix else 0.0
    ns = 4 if helix else 1
    ro, ri = [], []
    for i in range(ns + 1):
        t = i / ns
        a_off = tw * (t - 0.5)
        z = -width / 2 + width * t
        ri.append([tuple(c + w * z + (u * math.cos(a + a_off) + v * math.sin(a + a_off)) * r) for a, r in inner])
        ro.append([tuple(c + w * z + (u * math.cos(a + a_off) + v * math.sin(a + a_off)) * r_out) for a, _ in inner])
    for i in range(ns):
        for k in range(n):
            kk = (k + 1) % n
            q = [ro[i][k], ro[i][kk], ro[i + 1][kk], ro[i + 1][k]]
            cc = sum((Vector(x) for x in q), Vector()) / 4
            rad = cc - c - w * (cc - c).dot(w)
            mb.face(q, m, want=rad)
            q = [ri[i][k], ri[i][kk], ri[i + 1][kk], ri[i + 1][k]]
            cc = sum((Vector(x) for x in q), Vector()) / 4
            mb.face(q, m, want=-(cc - c - w * (cc - c).dot(w)))
    for i, sg in ((0, -1), (ns, 1)):
        for k in range(n):
            kk = (k + 1) % n
            mb.face([ro[i][k], ro[i][kk], ri[i][kk], ri[i][k]], m, want=w * sg)


def _emit_sphere(mb, c, r, seg, rings, m):
    prof = [(r * math.sin(math.pi * i / rings), -r * math.cos(math.pi * i / rings)) for i in range(rings + 1)]
    _lathe_out(mb, prof, c, (0, 0, 1), seg, m)


def _lathe_out(mb, profile, c, axis, seg, m, phase=0.0, closed=False):
    """Revolución con caras orientadas hacia fuera del eje (perfiles abiertos sobre el eje)."""
    c = Vector(c)
    u, v, w = _frame(axis)
    rings = []
    for (r, a) in profile:
        rings.append([tuple(c + w * a + (u * math.cos(phase + 2 * math.pi * k / seg) +
                                         v * math.sin(phase + 2 * math.pi * k / seg)) * r) for k in range(seg)])
    # centro del perfil para orientar las caras de un perfil cerrado
    pc_r = sum(p[0] for p in profile) / len(profile)
    pc_a = sum(p[1] for p in profile) / len(profile)
    pairs = list(zip(range(len(rings) - 1), range(1, len(rings))))
    if closed:
        pairs.append((len(rings) - 1, 0))
    for i, j in pairs:
        (r0, a0), (r1, a1) = profile[i], profile[j]
        # normal 2D del segmento del perfil (dr, da) girada; se orienta lejos del centro del perfil
        dr, da = r1 - r0, a1 - a0
        nr, na = da, -dr
        # perfiles convexos: la normal se aleja del centro del perfil en el plano (radio, eje)
        mr, ma = (r0 + r1) / 2 - pc_r, (a0 + a1) / 2 - pc_a
        if nr * mr + na * ma < 0:
            nr, na = -nr, -na
        for k in range(seg):
            kk = (k + 1) % seg
            q = [rings[i][k], rings[i][kk], rings[j][kk], rings[j][k]]
            ang = phase + 2 * math.pi * (k + 0.5) / seg
            radial = u * math.cos(ang) + v * math.sin(ang)
            mb.face(q, m, want=radial * nr + w * na)


def _emit_torus(mb, c, axis, R, r, seg, seg2, m):
    c = Vector(c)
    u, v, w = _frame(axis)
    rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        d = u * math.cos(a) + v * math.sin(a)
        rings.append([tuple(c + d * (R + r * math.cos(2 * math.pi * k / seg2)) + w * r * math.sin(2 * math.pi * k / seg2))
                      for k in range(seg2)])
    for i in range(seg):
        j = (i + 1) % seg
        a = 2 * math.pi * (i + 0.5) / seg
        d = u * math.cos(a) + v * math.sin(a)
        for k in range(seg2):
            kk = (k + 1) % seg2
            b = 2 * math.pi * (k + 0.5) / seg2
            mb.face([rings[i][k], rings[i][kk], rings[j][kk], rings[j][k]], m,
                    want=d * math.cos(b) + w * math.sin(b))


def _emit_bearing(mb, c, axis, rin, rout, width, balls, m, mball, rows, seals):
    c = Vector(c)
    w = Vector(axis).normalized()
    t = (rout - rin) * 0.28
    rp = (rin + rout) / 2
    rb = (rout - rin) * 0.26
    P.tube_ring(mb, c, w, rin, rin + t, width, 32, m)
    P.tube_ring(mb, c, w, rout - t, rout, width, 32, m)
    n = balls or max(6, int(2 * math.pi * rp / (rb * 2.6)))
    u, v, _ = _frame(w)
    offs = [0.0] if rows == 1 else [-width * 0.24, width * 0.24]
    for ri, off in enumerate(offs):
        for k in range(n):
            a = 2 * math.pi * (k + 0.5 * ri) / n
            p = c + w * off + (u * math.cos(a) + v * math.sin(a)) * rp
            _emit_sphere(mb, p, rb, 8, 5, mball)
        # jaula: dos anillos finos a ambos lados de cada hilera de bolas
        for sg in (-1, 1):
            P.tube_ring(mb, c + w * (off + sg * rb * 0.95), w, rp - rb * 0.35, rp + rb * 0.35, rb * 0.25, 32, m)
    if seals:
        for sg in (-1, 1):
            P.tube_ring(mb, c + w * sg * (width / 2 - 0.0006), w, rin + t, rout - t, 0.001, 32, m)


def _emit_coil(mb, c, axis, r, wire, turns, length, seg, m, ground):
    c = Vector(c)
    u, v, w = _frame(axis)
    steps = max(12, int(turns * 16))
    path = []
    for i in range(steps + 1):
        t = i / steps
        a = 2 * math.pi * turns * t
        # extremos cerrados: los dos últimos cuartos de vuelta con paso casi nulo
        if ground:
            e = 0.75 / turns
            if t < e:
                z = wire * 1.05 * (t / e) * 0.5
            elif t > 1 - e:
                z = length - wire * 1.05 * ((1 - t) / e) * 0.5
            else:
                z = wire * 0.53 + (length - wire * 1.06) * (t - e) / (1 - 2 * e)
        else:
            z = length * t
        path.append(c + w * z + (u * math.cos(a) + v * math.sin(a)) * r)
    P.sweep(mb, path, P.circle_profile(wire / 2, seg), mat=m)


def _emit_tube(mb, path, r, seg, samples, m, r_in):
    pts = P.catmull([Vector(p) for p in path], samples) if len(path) > 2 and samples > 1 else [Vector(p) for p in path]
    if r_in:
        prof_o = P.circle_profile(r, seg)
        P.sweep(mb, pts, prof_o, mat=m, caps=False)
        prof_i = P.circle_profile(r_in, seg)
        # pared interior: caras hacia el eje del tubo
        fr = P.frames(pts)
        rings_o, rings_i = [], []
        for p, (tt, nn, bb) in zip(pts, fr):
            rings_o.append([tuple(p + bb * x + nn * y) for x, y in prof_o])
            rings_i.append([tuple(p + bb * x + nn * y) for x, y in prof_i])
        for i in range(len(pts) - 1):
            for k in range(seg):
                kk = (k + 1) % seg
                q = [rings_i[i][k], rings_i[i][kk], rings_i[i + 1][kk], rings_i[i + 1][k]]
                cc = sum((Vector(x) for x in q), Vector()) / 4
                mb.face(q, m, want=(pts[i] + pts[i + 1]) * 0.5 - cc)
        for idx, sgn in ((0, -1), (-1, 1)):
            for k in range(seg):
                kk = (k + 1) % seg
                mb.face([rings_o[idx][k], rings_o[idx][kk], rings_i[idx][kk], rings_i[idx][k]], m,
                        want=fr[idx][0] * sgn)
    else:
        P.sweep(mb, pts, P.circle_profile(r, seg), mat=m)


def _emit_screw(mb, pos, axis, d, length, m, head, pitch, washer):
    p = Vector(pos)
    w = Vector(axis).normalized()        # eje = sentido hacia fuera de la cabeza
    hexr = d * 1.6 / math.sqrt(3)
    z = 0.0
    if washer:
        P.tube_ring(mb, p + w * d * 0.09, w, d * 0.55, d * 1.05, d * 0.18, 16, m)
        z = d * 0.18
    if head == "hex":
        L.lathe(mb, [(0.0, z), (hexr, z), (hexr, z + d * 0.62), (hexr * 0.86, z + d * 0.68), (0.0, z + d * 0.68)],
                tuple(p), tuple(w), 6, m, phase=math.pi / 6)
    elif head == "flange":
        P.flange_bolt(mb, p + w * z, w, d, m)
    elif head == "allen":
        L.lathe(mb, [(0.0, z), (d * 0.75, z), (d * 0.75, z + d * 0.95), (d * 0.42, z + d * 1.0),
                     (d * 0.42, z + d * 0.55), (0.0, z + d * 0.5)], tuple(p), tuple(w), 16, m)
    else:   # torx de cabeza alomada
        P.torx_screw(mb, p + w * z, w, d, m)
    if length > 0:
        pitch = pitch or max(0.0005, d * 0.15)
        nthr = int(length / pitch)
        prof = [(0.0, 0.0), (d * 0.5, 0.0)]
        if nthr <= 40:
            for i in range(nthr):
                prof.append((d * 0.43, -(i + 0.5) * pitch))
                prof.append((d * 0.5, -(i + 1) * pitch))
        else:
            prof.append((d * 0.5, -length))
        prof += [(d * 0.38, -length - d * 0.08), (0.0, -length - d * 0.08)]
        L.lathe(mb, prof, tuple(p), tuple(w), 10, m)


def _emit_pcb(mb, c, size, normal, up, comps, seed, mb_, mchip, mcap, mconn, mmetal):
    c = Vector(c)
    n = Vector(normal).normalized()
    upv = Vector(up)
    uu = upv.cross(n).normalized()       # ancho de la placa
    vv = n.cross(uu).normalized()        # alto de la placa
    rot = Matrix((uu, vv, n)).transposed()
    lx, ly, th = size
    L.box(mb, tuple(c), (lx, ly, th), mb_, rot=rot)
    rnd = random.Random(seed)
    top = c + n * th / 2
    placed = []
    for i in range(comps):
        kind = rnd.random()
        for _ in range(12):
            x = (rnd.random() - 0.5) * (lx - 0.012)
            y = (rnd.random() - 0.5) * (ly - 0.012)
            if kind < 0.30:
                sx, sy, sz, mm = rnd.choice(((0.014, 0.014, 0.0015), (0.010, 0.010, 0.0012), (0.020, 0.020, 0.002),
                                              (0.008, 0.005, 0.0012))) + (mchip,)
            elif kind < 0.55:
                sx, sy, sz, mm = 0.0032, 0.0016, 0.0009, mmetal
            elif kind < 0.75:
                sx, sy, sz, mm = 0.0, 0.0, 0.0, mcap
            elif kind < 0.88:
                sx, sy, sz, mm = 0.012, 0.012, 0.007, mchip          # bobina de potencia
            else:
                sx, sy, sz, mm = rnd.choice(((0.024, 0.010, 0.010), (0.030, 0.012, 0.012))) + (mconn,)
            rr = max(sx, sy, 0.008) * 0.75
            if all((x - px) ** 2 + (y - py) ** 2 > (rr + pr) ** 2 for px, py, pr in placed):
                placed.append((x, y, rr))
                break
        else:
            continue
        base = top + uu * x + vv * y
        if mm == mcap:
            r = rnd.choice((0.003, 0.004, 0.005))
            h = rnd.choice((0.006, 0.008, 0.010))
            P.cyl(mb, base, base + n * h, r, 12, mcap)
            L.lathe(mb, [(r * 0.98, h), (r * 0.6, h + 0.0004), (0.0, h + 0.0004)], tuple(base), tuple(n), 12, mmetal)
        else:
            L.box(mb, tuple(base + n * sz / 2), (sx, sy, sz), mm, rot=rot)
    return rot


def _emit_hairpins(mb, c, axis, r0, r1, length, count, height, m, layers, end):
    """Horquillas: cada una sale de una ranura, sube y salta 1/count·paso a la ranura vecina."""
    c = Vector(c)
    u, v, w = _frame(axis)
    base = c + w * (length / 2) * end
    span = 2 * math.pi * 6 / count       # paso de bobina (6 ranuras)
    for L_ in range(layers):
        r = r0 + (r1 - r0) * (L_ + 0.5) / layers
        hh = height * (0.75 + 0.25 * (L_ + 1) / layers)
        for k in range(count):
            a0 = 2 * math.pi * k / count + L_ * 0.5 * 2 * math.pi / count
            a1 = a0 + span
            pts = []
            for i in range(7):
                t = i / 6
                a = a0 + (a1 - a0) * t
                z = hh * math.sin(math.pi * t) ** 0.6
                rr = r + (0.002 if L_ % 2 else -0.002) * math.sin(math.pi * t)
                pts.append(base + w * z * end + (u * math.cos(a) + v * math.sin(a)) * rr)
            P.sweep(mb, pts, P.rect_profile(0.0035, 0.0020, 0.0, 0), mat=m)


def _emit_winding(mb, c, axis, r0, r1, length, height, m, m_lace, lacing):
    c = Vector(c)
    u, v, w = _frame(axis)
    for end in (-1, 1):
        a = end * length / 2
        prof = [(r0, a), (r0 - 0.002, a + end * height * 0.5), (r0 + (r1 - r0) * 0.15, a + end * height),
                (r1 - (r1 - r0) * 0.15, a + end * height), (r1 + 0.002, a + end * height * 0.5), (r1, a)]
        _lathe_out(mb, prof if end > 0 else list(reversed(prof)), c, w, 48, m, closed=True)
        # atado de cordón de las cabezas de bobina
        for k in range(lacing):
            ang = 2 * math.pi * k / lacing
            d = u * math.cos(ang) + v * math.sin(ang)
            mid = c + w * (a + end * height * 0.55) + d * (r0 + r1) / 2
            P.cyl(mb, mid - w * 0.003 * end - d * (r1 - r0) * 0.62, mid - w * 0.003 * end + d * (r1 - r0) * 0.62,
                  0.0012, 6, m_lace)


def _emit_hclamp(mb, c, axis, r, wdt, m):
    c = Vector(c)
    w = Vector(axis).normalized()
    P.tube_ring(mb, c, w, r, r + 0.0012, wdt, 32, m)
    u, v, _ = _frame(w)
    P.rbox(mb, c + v * (r + 0.003), (0.006, 0.006, 0.006), 0.0015, 1,
           Matrix((u, v, w)).transposed(), m)


def _emit_fins(mb, c, axis, up, size, n, t, m):
    """`size` = (longitud del reparto a lo largo de `axis`, fondo de cada aleta, alto según `up`)."""
    c = Vector(c)
    a = Vector(axis).normalized()          # dirección en la que se reparten las aletas
    upv = Vector(up).normalized()
    side = upv.cross(a).normalized()
    rot = Matrix((a, side, upv)).transposed()
    total, depth, hh = size
    for i in range(n):
        x = -total / 2 + total * (i + 0.5) / n
        L.box(mb, tuple(c + a * x), (t, depth, hh), m, rot=rot)


def emit(mb, sh):
    k = sh[0]
    if k == "gear":
        _emit_gear(mb, *sh[1:])
    elif k == "igear":
        _emit_igear(mb, *sh[1:])
    elif k == "sphere":
        _, c, r, seg, rings, m = sh
        _emit_sphere(mb, c, r, seg, rings, m)
    elif k == "torus":
        _emit_torus(mb, *sh[1:])
    elif k == "bearing":
        _emit_bearing(mb, *sh[1:])
    elif k == "lathe":
        _, c, axis, prof, seg, m, phase = sh
        L.lathe(mb, prof, tuple(c), tuple(axis), seg, m, phase=phase)
    elif k == "coil":
        _emit_coil(mb, *sh[1:])
    elif k == "tube":
        _emit_tube(mb, *sh[1:])
    elif k == "screw":
        _emit_screw(mb, *sh[1:])
    elif k == "pcb":
        _emit_pcb(mb, *sh[1:])
    elif k == "hairpins":
        _emit_hairpins(mb, *sh[1:])
    elif k == "winding":
        _emit_winding(mb, *sh[1:])
    elif k == "hclamp":
        _emit_hclamp(mb, *sh[1:])
    elif k == "fins":
        _emit_fins(mb, *sh[1:])
    elif k == "mb":
        src = sh[1]
        for f, mi in zip(src.faces, src.mats):
            mb.face([src.verts[i] for i in f], mi)
    elif k == "belt":
        _, path, width, t, w = sh
        P.sweep(mb, [Vector(p) for p in path], P.rect_profile(t, width, 0.0, 0), closed_path=True, up=w)
    elif k == "xf":
        _, mat, shapes = sh
        # las formas locales se generan en un constructor aparte y se transforman al copiarlas
        sub = L.MeshBuilder()
        for s in V3._flat(shapes):
            emit(sub, s)
        mat = Matrix(mat)
        for f, mi in zip(sub.faces, sub.mats):
            mb.face([tuple(mat @ Vector(sub.verts[i])) for i in f], mi)
    else:
        V3._emit(mb, sh, False)


# ---------------------------------------------------------------------------
# Creación de piezas
# ---------------------------------------------------------------------------
def _mirror_mb(mb):
    out = L.MeshBuilder()
    for f, mi in zip(mb.faces, mb.mats):
        out.face([(-mb.verts[i][0], mb.verts[i][1], mb.verts[i][2]) for i in reversed(f)], mi)
    return out


def part(M, name, system, mats, shapes, label, mirror=False, edir=None, dist=None, stage=None,
         group=None, fid="R", note=None, bevel=0.0, smooth=35, parent=None, origin=None, frame=None):
    """Crea una pieza (o la pareja R/L) con formas de la versión 3 o 4.

    `frame`: matriz 4x4 (p. ej. `obj.matrix_world`) si las formas están en coordenadas locales de otro objeto.
    `parent`: nombre u objeto padre (conjunto) para que la pieza acompañe al conjunto en la explosión.
    """
    import bpy
    mats = [mats] if isinstance(mats, str) else list(mats)
    materials = [M[n] for n in mats]
    shapes = V3._flat(shapes)
    base = L.MeshBuilder()
    for sh in shapes:
        emit(base, sh)
    if frame is not None:
        fm = Matrix(frame)
        nb = L.MeshBuilder()
        for f, mi in zip(base.faces, base.mats):
            nb.face([tuple(fm @ Vector(base.verts[i])) for i in f], mi)
        base = nb
    if isinstance(parent, str):
        parent = bpy.data.objects.get(parent)
    objs = []
    for mir in ((False, True) if mirror else (False,)):
        mb = _mirror_mb(base) if mir else base
        if not mb.faces:
            continue
        mb.mats = [min(i, len(materials) - 1) for i in mb.mats]
        side = "L" if mir else "R"
        nm = f"{name}_{side}" if mirror else name
        lb = label.replace("{lado}", SIDE_ES[side]) if mirror else label
        d = Vector(edir) if edir is not None else V3._default_dir(mb)
        if edir is not None and mir:
            d.x = -d.x
        dd = dist if dist is not None else 0.30
        st = stage if stage is not None else STAGE.get(system, 6)
        par = parent
        if mir and parent is not None and parent.name.endswith("_R"):
            par = bpy.data.objects.get(parent.name[:-2] + "_L") or parent
        o = P.make(mb, nm, system, materials, par, tuple(d), dd, st, group or system.replace("_", " ").title(),
                   lb, fid, note=note, smooth=smooth, bevel=bevel, origin=origin)
        objs.append(o)
    return objs


def _mesh_world(name, evaluated=False):
    """Vértices (mundo) y caras de un objeto de malla existente (con modificadores si `evaluated`)."""
    import bpy
    o = bpy.data.objects.get(name)
    if o is None or o.type != "MESH":
        return None, None
    if evaluated:
        dg = bpy.context.evaluated_depsgraph_get()
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        verts = [mw @ v.co for v in me.vertices]
        faces = [list(p.vertices) for p in me.polygons]
        ev.to_mesh_clear()
        return verts, faces
    mw = o.matrix_world
    verts = [mw @ v.co for v in o.data.vertices]
    faces = [list(p.vertices) for p in o.data.polygons]
    return verts, faces


def derived(M, src, name, system, mats, label, scale=(0.9, 0.9, 0.9), offset=(0, 0, 0), core=None, xform=None,
            evaluated=False, **kw):
    """Pieza derivada de la malla de otra (espumas dentro de tapizados, almas dentro de aros…).

    `scale`: factor por eje respecto al centro de la caja del original (espuma interior).
    `core`: (eje, factor) para contraer la sección de un aro hacia su línea media (alma del volante).
    `xform`: función punto → punto (mundo) para transformaciones a medida (p. ej. recortar el espesor de una
    espuma por detrás para dejar sitio al armazón). `evaluated`: partir de la malla con modificadores.
    """
    verts, faces = _mesh_world(src, evaluated)
    if verts and xform is not None:
        verts = [Vector(xform(p)) for p in verts]
        mb = L.MeshBuilder(merge=1e-7)
        for f in faces:
            mb.face([tuple(verts[i]) for i in f], 0)
        return part(M, name, system, mats, [("mb", mb)], label, **kw)
    if not verts:
        return []
    mn = Vector((min(v.x for v in verts), min(v.y for v in verts), min(v.z for v in verts)))
    mx = Vector((max(v.x for v in verts), max(v.y for v in verts), max(v.z for v in verts)))
    c = (mn + mx) / 2 + Vector(offset)
    if core is not None:
        axis, fac = core
        w = Vector(axis).normalized()
        u, v, _ = _frame(w)
        bins = 96
        acc = [[0.0, 0.0, 0] for _ in range(bins)]       # radio medio, altura media, n
        pol = []
        for p in verts:
            d = p - c
            a = math.atan2(d.dot(v), d.dot(u))
            r = (d - w * d.dot(w)).length
            h = d.dot(w)
            k = int((a + math.pi) / (2 * math.pi) * bins) % bins
            acc[k][0] += r
            acc[k][1] += h
            acc[k][2] += 1
            pol.append((a, k))
        new = []
        for p, (a, k) in zip(verts, pol):
            n = max(1, acc[k][2])
            rm, hm = acc[k][0] / n, acc[k][1] / n
            centre = c + (u * math.cos(a) + v * math.sin(a)) * rm + w * hm
            new.append(centre + (p - centre) * fac)
        verts = new
    else:
        verts = [c + Vector(((p - c).x * scale[0], (p - c).y * scale[1], (p - c).z * scale[2])) for p in verts]
    mb = L.MeshBuilder(merge=1e-7)
    for f in faces:
        mb.face([tuple(verts[i]) for i in f], 0)
    return part(M, name, system, mats, [("mb", mb)], label, **kw)


def fit_inside(inner, housing, margin=0.0015, k_min=0.6, max_iter=90):
    """Ajusta `inner` dentro de `housing` para que su superficie deje de cortar la de la carcasa (mallas
    evaluadas, árboles BVH en coordenadas de mundo). Devuelve el menor factor de escala aplicado en un eje
    (1.0 si ya cabía, 0.0 si no se consigue sin bajar de `k_min`).

    Se usa para los interiores de la versión 4 (placas, bobinados, engranajes…), cuyas formas son
    reconstrucciones. El ajuste es anisótropo y se hace en los ejes propios de la carcasa: en cada paso se miran
    los triángulos del interior que cortan la pared y se clasifican por eje y sentido respecto al centro del
    interior; si chocan por un solo lado, el interior se desplaza hacia el otro (estaba descentrado); si chocan
    por los dos, se reduce solo ese eje. Así una placa delgada en una carcasa inclinada solo pierde espesor.
    """
    import bpy
    from mathutils.bvhtree import BVHTree
    oi, oh = bpy.data.objects.get(inner), bpy.data.objects.get(housing)
    if oi is None or oh is None:
        return None
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()

    def world(o):
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        vs = [ev.matrix_world @ v.co for v in me.vertices]
        me.calc_loop_triangles()
        tris = [tuple(t.vertices) for t in me.loop_triangles]
        ev.to_mesh_clear()
        return vs, tris

    hv, ht = world(oh)
    htree = BVHTree.FromPolygons(hv, ht, epsilon=0.0)
    iv, it = world(oi)
    if not iv or not it:
        return None
    R = oh.matrix_world.to_3x3().normalized()
    Ri = R.transposed()
    loc = [Ri @ p for p in iv]                      # coordenadas en los ejes de la carcasa
    mn = Vector((min(v.x for v in loc), min(v.y for v in loc), min(v.z for v in loc)))
    mx = Vector((max(v.x for v in loc), max(v.y for v in loc), max(v.z for v in loc)))
    c = (mn + mx) / 2
    half = [max((mx[i] - mn[i]) / 2, 1e-4) for i in range(3)]
    rel = [p - c for p in loc]
    k = [1.0, 1.0, 1.0]
    t = Vector((0.0, 0.0, 0.0))
    tmax = [0.30 * h + 0.006 for h in half]

    def place(kk, tt, extra=0.0):
        g = [kk[i] * (1.0 + extra / half[i]) for i in range(3)]
        return [R @ (c + tt + Vector((q.x * g[0], q.y * g[1], q.z * g[2]))) for q in rel]

    def hits(kk, tt):
        vs = place(kk, tt, margin)
        return vs, BVHTree.FromPolygons(vs, it, epsilon=0.0).overlap(htree)

    vs, ov = hits(k, t)
    if not ov:
        return 1.0
    for _ in range(max_iter):
        cnt = {}
        step = max(1, len(ov) // 300)
        for ia, _ib in ov[::step]:
            a, b, cc = (Ri @ vs[j] for j in it[ia])
            q = (a + b + cc) / 3 - (c + t)
            i = max(range(3), key=lambda j: abs(q[j]) / half[j])
            key = (i, 1 if q[i] > 0 else -1)
            cnt[key] = cnt.get(key, 0) + 1
        (i, sg), n = max(cnt.items(), key=lambda kv: kv[1])
        opp = cnt.get((i, -sg), 0)
        moved = False
        if opp < 0.25 * n and abs(t[i] - sg * 0.0015) <= tmax[i]:
            t[i] -= sg * 0.0015
            moved = True
        if not moved:
            if k[i] * 0.97 < k_min:
                return 0.0
            k[i] *= 0.97
        vs, ov = hits(k, t)
        if not ov:
            break
    else:
        return 0.0
    mw = oi.matrix_world
    inv = mw.inverted()
    final = place(k, t)
    # se aplica la misma transformación a los vértices originales (sin modificadores)
    base = [Ri @ (mw @ v.co) for v in oi.data.vertices]
    for v, p in zip(oi.data.vertices, base):
        q = p - c
        v.co = inv @ (R @ (c + t + Vector((q.x * k[0], q.y * k[1], q.z * k[2]))))
    oi.data.update()
    del final
    return round(min(k), 3)


def keep_inside(inner, outer, gap=0.003, rounds=2):
    """Lleva dentro de `outer` (malla evaluada, cerrada) los vértices de `inner` que quedan fuera o a menos de
    `gap` de su superficie: se proyectan sobre ella y se retiran `gap` hacia dentro. Para espumas dentro de sus
    tapizados, cuya forma (copia encogida) asoma en las zonas cóncavas. Devuelve los vértices movidos."""
    import bpy
    from mathutils.bvhtree import BVHTree
    oi, oo = bpy.data.objects.get(inner), bpy.data.objects.get(outer)
    if oi is None or oo is None:
        return None
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = oo.evaluated_get(dg)
    me = ev.to_mesh()
    vs = [ev.matrix_world @ v.co for v in me.vertices]
    me.calc_loop_triangles()
    tree = BVHTree.FromPolygons(vs, [tuple(t.vertices) for t in me.loop_triangles], epsilon=0.0)
    ev.to_mesh_clear()
    up = Vector((0.0123, 0.0217, 1.0)).normalized()

    def inside(p):
        n, o = 0, p.copy()
        for _ in range(64):
            hit = tree.ray_cast(o, up)[0]
            if hit is None:
                break
            n += 1
            o = hit + up * 1e-5
        return n % 2 == 1
    if oi.data.users > 1:
        oi.data = oi.data.copy()
    mw = oi.matrix_world
    inv = mw.inverted()
    moved = 0
    for _ in range(rounds):
        ch = 0
        for v in oi.data.vertices:
            p = mw @ v.co
            loc, nor, _i, d = tree.find_nearest(p)
            if loc is None:
                continue
            if inside(p) and d >= gap:
                continue
            v.co = inv @ (loc - nor * gap)
            ch += 1
        moved += ch
        if not ch:
            break
    oi.data.update()
    return moved


def clip_inside(inner, housing, margin=0.0015):
    """Recorta `inner` con el volumen interior de `housing` (intersección booleana contra una copia de la carcasa
    desplazada `margin` hacia dentro a lo largo de sus normales). Es el último recurso de
    `build_v4.fit_internals` cuando el ajuste por escala no converge (carcasas con nervios, placas o tabiques
    interiores): el interior conserva su tamaño y solo se corta donde asomaría por la pared. Se prueba primero el
    solver MANIFOLD y, si no mejora, el exacto con autointersección; el resultado se acepta solo si corta menos la
    carcasa que antes. Devuelve el número de caras resultante (0 si se descartó)."""
    import bpy
    from mathutils.bvhtree import BVHTree
    import build_montaje as BM
    oi, oh = bpy.data.objects.get(inner), bpy.data.objects.get(housing)
    if oi is None or oh is None:
        return None

    def tree(o):
        dg = bpy.context.evaluated_depsgraph_get()
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        vs = [ev.matrix_world @ v.co for v in me.vertices]
        me.calc_loop_triangles()
        tr = [tuple(t.vertices) for t in me.loop_triangles]
        ev.to_mesh_clear()
        return BVHTree.FromPolygons(vs, tr, epsilon=0.0) if tr else None

    BM._bake(oi)
    th = tree(oh)
    before = len(tree(oi).overlap(th))
    if not before:
        return len(oi.data.polygons)
    cut, _closed = BM._cutter_object([housing], -margin)
    n = 0
    # MANIFOLD primero y, si no mejora, el exacto (en los interiores, mallas cerradas y moderadas, es estable)
    for solver in ("MANIFOLD", "EXACT"):
        BM._log(f"clip {inner} {solver}")
        mod = oi.modifiers.new("_clip", "BOOLEAN")
        mod.operation = "INTERSECT"
        mod.solver = solver
        mod.object = cut
        if solver == "EXACT":
            mod.use_self = True
            mod.use_hole_tolerant = True
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        new = bpy.data.meshes.new_from_object(oi.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        oi.modifiers.remove(mod)
        if len(new.polygons) < 0.15 * max(1, len(oi.data.polygons)):
            bpy.data.meshes.remove(new)
            continue
        old = oi.data
        oi.data = new
        bpy.context.view_layer.update()
        t1 = tree(oi)
        after = len(t1.overlap(th)) if t1 else before
        if after >= before:
            oi.data = old
            bpy.data.meshes.remove(new)
            continue
        new.name = old.name
        if old.users == 0:
            bpy.data.meshes.remove(old)
        n = len(new.polygons)
        break
    me = cut.data
    bpy.data.objects.remove(cut, do_unlink=True)
    bpy.data.meshes.remove(me)
    return n


def obj_frame(name):
    """Matriz de mundo de un objeto ya construido (para describir piezas en sus coordenadas locales)."""
    import bpy
    o = bpy.data.objects.get(name)
    if o is None:
        return None
    return o.matrix_world.copy()


def set_explode(name, edir=None, dist=None, stage=None):
    """Ajusta la explosión de un objeto existente (p. ej. carcasas que deben apartarse más que su interior)."""
    import bpy
    o = bpy.data.objects.get(name)
    if o is None:
        return None
    if edir is not None:
        d = Vector(edir).normalized()
        o["explode_dir"] = [round(d.x, 5), round(d.y, 5), round(d.z, 5)]
    if dist is not None:
        o["explode_dist"] = float(dist)
    if stage is not None:
        o["explode_stage"] = int(stage)
    return o
