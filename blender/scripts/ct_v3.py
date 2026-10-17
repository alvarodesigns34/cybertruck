"""Ayudas declarativas para las piezas añadidas en la versión 3.

Cada pieza se describe como una lista de formas elementales (cajas, cilindros, envolventes, barridos,
tornillería…) en coordenadas de mundo del lado derecho (+X). Con `mirror=True` se genera además la pareja
izquierda reflejando las coordenadas de entrada (no la malla), de modo que las normales quedan bien
orientadas sin depender de `recalc_normals`.

Los datos proceden de `docs/ficha-tecnica-piezas.md` (identificadores EXT-, EST-, CHS-, TRN-, INT-, ELE-).
Existencia, denominación y fijaciones son «Verificado» en los manuales; la forma es siempre reconstruida
(`ct_parts.make` clasifica así los «V» como «R»).
"""

import math
from mathutils import Vector
import ct_lib as L
import ct_parts as P

# Etapa de explosión por defecto según el sistema (ver docs/model-specification.md §4)
STAGE = {
    "EXTERIOR_PANELS": 1, "DOORS_AND_HATCHES": 1, "GLASS_AND_MIRRORS": 1, "LIGHTING": 1, "CARGO_BED": 1,
    "INTERIOR_DASHBOARD": 2, "INTERIOR_CONTROLS": 2, "INTERIOR_SEATS": 2, "INTERIOR_DOORS": 2,
    "INTERIOR_TRIM": 2, "BODY_STRUCTURE": 3, "UNDERBODY": 3, "FRONT_SUSPENSION": 4, "REAR_SUSPENSION": 4,
    "STEERING": 4, "FRONT_WHEELS_AND_BRAKES": 4, "REAR_WHEELS_AND_BRAKES": 4, "BATTERY_ASSEMBLY": 5,
    "DRIVE_UNITS": 5, "BODY_FASTENERS": 6,
}
SIDE_ES = {"R": "derecho", "L": "izquierdo"}


# ---------------------------------------------------------------------------
# Constructores de formas (tuplas inmutables; la última posición es el índice de material)
# ---------------------------------------------------------------------------
def box(c, s, r=0.003, m=0):
    return ("box", c, s, r, m)


def cyl(p0, p1, r, r1=None, seg=16, m=0, caps=True):
    return ("cyl", p0, p1, r, r1, seg, m, caps)


def ring(c, axis, rin, rout, length, seg=24, m=0):
    return ("ring", c, axis, rin, rout, length, seg, m)


def disc(c, axis, r, t, seg=24, m=0):
    return ("disc", c, axis, r, t, seg, m)


def hull(pts, m=0):
    return ("hull", pts, m)


def beam(a, b, w, h, r=0.003, up=(0, 0, 1), m=0):
    return ("beam", a, b, w, h, r, up, m)


def sweep(path, w, h, r=0.003, samples=5, up=None, m=0):
    return ("sweep", path, w, h, r, samples, up, m)


def hose(path, r, seg=10, samples=5, m=0, zmin=None):
    return ("hose", path, r, seg, samples, m, zmin)


def bolt(pos, axis, d=0.010, m=0, shank=0.0):
    return ("bolt", pos, axis, d, m, shank)


def nut(pos, axis, d=0.010, m=0, stud=0.0):
    return ("nut", pos, axis, d, m, stud)


def torx(pos, axis, d=0.006, m=0):
    return ("torx", pos, axis, d, m)


def clip(pos, axis, d=0.012, m=0):
    return ("clip", pos, axis, d, m)


def rivet(pos, axis, d=0.008, m=0):
    return ("rivet", pos, axis, d, m)


def ball(c, axis, r=0.020, m=0, mboot=1):
    """Rótula con guardapolvos (carcasa, fuelle y espárrago)."""
    return ("ball", c, axis, r, m, mboot)


def boot(p0, p1, r0, r1, folds=6, seg=20, m=0):
    """Fuelle de goma (junta homocinética, cremallera)."""
    return ("boot", p0, p1, r0, r1, folds, seg, m)


def ribs(origin, u, v, w, h, nu, nv, normal, rib_h=0.010, rib_t=0.004, m=0):
    return ("ribs", origin, u, v, w, h, nu, nv, normal, rib_h, rib_t, m)


def prism(poly, origin, u, v, depth, m=0):
    return ("prism", poly, origin, u, v, depth, m)


def rowx(fn, xs, y, z, **kw):
    """Repite una forma elemental (bolt, clip, rivet…) en una fila a lo largo de X."""
    return [fn((x, y, z), **kw) for x in xs]


def rowy(fn, x, ys, z, **kw):
    return [fn((x, y, z), **kw) for y in ys]


def rowz(fn, x, y, zs, **kw):
    return [fn((x, y, z), **kw) for z in zs]


# ---------------------------------------------------------------------------
# Generación de la malla
# ---------------------------------------------------------------------------
def _flat(shapes):
    out = []
    for s in shapes:
        if isinstance(s, list):
            out.extend(_flat(s))
        else:
            out.append(s)
    return out


def _mx(p):
    return (-p[0], p[1], p[2])


def _emit(mb, sh, mir):
    f = _mx if mir else (lambda p: tuple(p))
    k = sh[0]
    if k == "box":
        _, c, s, r, m = sh
        if r and r > 0:
            P.rbox(mb, f(c), s, r, 1, None, m)
        else:
            L.box(mb, f(c), s, m)
    elif k == "cyl":
        _, p0, p1, r, r1, seg, m, caps = sh
        P.cyl(mb, f(p0), f(p1), r, seg, m, caps, r1)
    elif k == "ring":
        _, c, ax, rin, rout, ln, seg, m = sh
        P.tube_ring(mb, f(c), f(ax), rin, rout, ln, seg, m)
    elif k == "disc":
        _, c, ax, r, t, seg, m = sh
        P.disc(mb, f(c), f(ax), r, t, seg, m, min(0.002, t * 0.3))
    elif k == "hull":
        _, pts, m = sh
        P.hull(mb, [f(p) for p in pts], m)
    elif k == "beam":
        _, a, b, w, h, r, up, m = sh
        P.beam(mb, f(a), f(b), w, h, f(up), r, m)
    elif k == "sweep":
        _, path, w, h, r, smp, up, m = sh
        pth = P.catmull([f(p) for p in path], smp) if smp > 1 and len(path) > 2 else [Vector(f(p)) for p in path]
        P.sweep(mb, pth, P.rect_profile(w, h, r, 1 if r else 0), mat=m, up=f(up) if up else None)
    elif k == "hose":
        _, path, r, seg, smp, m, zmin = sh
        P.hose(mb, [f(p) for p in path], r, seg, smp, m, True, zmin)
    elif k == "bolt":
        _, pos, ax, d, m, sk = sh
        P.flange_bolt(mb, f(pos), f(ax), d, m, sk)
    elif k == "nut":
        _, pos, ax, d, m, st = sh
        P.hex_nut(mb, f(pos), f(ax), d, m, st)
    elif k == "torx":
        _, pos, ax, d, m = sh
        P.torx_screw(mb, f(pos), f(ax), d, m)
    elif k == "clip":
        _, pos, ax, d, m = sh
        P.push_clip(mb, f(pos), f(ax), d, m)
    elif k == "rivet":
        _, pos, ax, d, m = sh
        P.rivet(mb, f(pos), f(ax), d, m)
    elif k == "ball":
        _, c, ax, r, m, mb2 = sh
        P.ball_joint(mb, f(c), f(ax), r, m, mb2)
    elif k == "boot":
        _, p0, p1, r0, r1, folds, seg, m = sh
        P.boot(mb, f(p0), f(p1), r0, r1, folds, seg, m)
    elif k == "ribs":
        _, o, u, v, w, h, nu, nv, n, rh, rt, m = sh
        lines = []
        for i in range(nu + 1):
            lines.append(((w * i / nu, 0), (w * i / nu, h)))
        for j in range(nv + 1):
            lines.append(((0, h * j / nv), (w, h * j / nv)))
        for i in range(nu):
            for j in range(nv):
                x0, x1, y0, y1 = w * i / nu, w * (i + 1) / nu, h * j / nv, h * (j + 1) / nv
                lines.append(((x0, y0), (x1, y1)) if (i + j) % 2 == 0 else ((x0, y1), (x1, y0)))
        P.ribbed_plate(mb, f(o), f(u), f(v), [(0, 0), (w, 0), (w, h), (0, h)], 0.004, rh, rt, lines, f(n), m)
    elif k == "prism":
        _, poly, o, u, v, depth, m = sh
        P.prism(mb, poly, f(o), f(u), f(v), depth, None, m)
    else:
        raise ValueError(f"forma desconocida: {k}")


def _default_dir(mb):
    xs = [v[0] for v in mb.verts]
    ys = [v[1] for v in mb.verts]
    zs = [v[2] for v in mb.verts]
    c = Vector((sum(xs) / len(xs), sum(ys) / len(ys), sum(zs) / len(zs)))
    d = Vector((c.x * 1.0, c.y * 0.25, (c.z - 0.75) * 1.2))
    if d.length < 0.12:
        d = Vector((0, 0.2, 1.0))
    return d


def part(M, name, system, mats, shapes, label, mirror=False, edir=None, dist=None, stage=None,
         group=None, fid="R", note=None, bevel=0.0, smooth=35, parent=None, origin=None):
    """Crea una pieza (o la pareja R/L si mirror=True) y registra sus metadatos de explosión.

    `mats`: nombres de materiales de la biblioteca (ct_materials) o un único nombre.
    `label`: descripción en español; admite «{lado}» cuando mirror=True.
    """
    mats = [mats] if isinstance(mats, str) else list(mats)
    materials = [M[n] for n in mats]
    shapes = _flat(shapes)
    objs = []
    for mir in ((False, True) if mirror else (False,)):
        mb = L.MeshBuilder()
        for sh in shapes:
            _emit(mb, sh, mir)
        if not mb.faces:
            continue
        mb.mats = [min(i, len(materials) - 1) for i in mb.mats]
        side = "L" if mir else "R"
        nm = f"{name}_{side}" if mirror else name
        lb = label.replace("{lado}", SIDE_ES[side]) if mirror else label
        d = Vector(edir) if edir is not None else _default_dir(mb)
        if edir is not None and mir:
            d.x = -d.x
        dd = dist if dist is not None else 0.35
        st = stage if stage is not None else STAGE.get(system, 6)
        o = P.make(mb, nm, system, materials, parent, tuple(d), dd, st, group or system.replace("_", " ").title(),
                   lb, fid, note=note, smooth=smooth, bevel=bevel, origin=origin)
        objs.append(o)
    return objs
