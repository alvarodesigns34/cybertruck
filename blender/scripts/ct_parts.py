"""Primitivas paramétricas para piezas mecánicas, herrajes y guarnecidos (coordenadas de mundo).

Complementa a ct_lib.MeshBuilder con formas habituales en automoción:
  * envolventes convexas (carcasas fundidas, portamanguetas, soportes),
  * cajas redondeadas y achaflanadas,
  * barridos de un perfil 2D a lo largo de una trayectoria (juntas, burletes, perfiles en U/omega),
  * mangueras y mazos de cables con trayectoria suavizada (Catmull-Rom),
  * tornillería: tornillos con brida hexagonal, tuercas, tornillos Torx de cabeza alomada,
    grapas de empuje y remaches.
Todas las caras se orientan explícitamente (want=...) para no depender de recalc_normals.
"""

import math
import bpy
import bmesh
from mathutils import Vector, Matrix
import ct_lib as L


# ---------------------------------------------------------------------------
# Geometría básica
# ---------------------------------------------------------------------------
def hull(mb, points, mat=0):
    """Envolvente convexa de una nube de puntos (forma maciza cerrada)."""
    bm = bmesh.new()
    for p in points:
        bm.verts.new(Vector(p))
    res = bmesh.ops.convex_hull(bm, input=bm.verts)
    for g in res.get("geom_interior", []) + res.get("geom_unused", []):
        if isinstance(g, bmesh.types.BMVert) and g.is_valid and not g.link_faces:
            pass
    c = Vector((0, 0, 0))
    for v in bm.verts:
        c += v.co
    c /= max(1, len(bm.verts))
    for f in bm.faces:
        cos = [tuple(v.co) for v in f.verts]
        fc = f.calc_center_median()
        mb.face(cos, mat, want=fc - c)
    bm.free()


def corner_points(c, size, r, seg=2, rot=None):
    """Puntos de las ocho esquinas redondeadas de una caja (para hull)."""
    c = Vector(c)
    hx, hy, hz = (s * 0.5 - r for s in size)
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                base = Vector((sx * hx, sy * hy, sz * hz))
                for i in range(seg + 1):
                    for j in range(seg + 1):
                        a = (math.pi / 2) * i / seg
                        b = (math.pi / 2) * j / seg
                        d = Vector((sx * math.cos(a) * math.cos(b), sy * math.sin(a) * math.cos(b), sz * math.sin(b)))
                        p = base + d * r
                        if rot is not None:
                            p = rot @ p
                        pts.append(c + p)
    return pts


def rbox(mb, c, size, r=0.004, seg=2, rot=None, mat=0):
    """Caja de aristas redondeadas (radio r)."""
    r = min(r, min(size) * 0.49)
    hull(mb, corner_points(c, size, r, seg, rot), mat)


def basis(axis, up=None):
    """Matriz 3x3 cuyas columnas son (u, v, w) con w = eje; u perpendicular a `up` si se da."""
    w = Vector(axis).normalized()
    if up is not None:
        u = Vector(up).cross(w)
        if u.length < 1e-6:
            u, v, w = L.frame_from_axis(w)
        else:
            u.normalize()
            v = w.cross(u).normalized()
    else:
        u, v, w = L.frame_from_axis(w)
    return Matrix((u, v, w)).transposed()


def beam(mb, a, b, w, h, up=(0, 0, 1), r=0.0, mat=0):
    """Viga de sección rectangular w x h entre a y b (h en la dirección de `up`)."""
    a, b = Vector(a), Vector(b)
    d = b - a
    rot = basis(d, up)
    c = (a + b) * 0.5
    # columnas: u (ancho), v (alto), w (longitud)
    rot2 = Matrix((rot.col[0], rot.col[1], rot.col[2])).transposed()
    if r > 0:
        rbox(mb, c, (w, h, d.length), r, 1, rot2, mat)
    else:
        L.box(mb, tuple(c), (w, h, d.length), mat, rot=rot2)


def cyl(mb, p0, p1, r, seg=24, mat=0, caps=True, r1=None):
    """Cilindro (o tronco de cono si r1) entre p0 y p1."""
    p0, p1 = Vector(p0), Vector(p1)
    ax = p1 - p0
    r1 = r if r1 is None else r1
    L.lathe(mb, [(r, 0.0), (r1, ax.length)], tuple(p0), tuple(ax.normalized()), seg, mat,
            cap_start=caps, cap_end=caps)


def tube_ring(mb, center, axis, r_in, r_out, length, seg=24, mat=0):
    """Casquillo o anillo (tubo corto de pared gruesa)."""
    c = Vector(center)
    ax = Vector(axis).normalized()
    p0 = c - ax * length / 2
    L.lathe(mb, [(r_in, 0.0), (r_out, 0.0), (r_out, length), (r_in, length)], tuple(p0), tuple(ax), seg, mat,
            closed_profile=True)


def disc(mb, center, axis, r, thick, seg=24, mat=0, chamfer=0.0):
    c = Vector(center)
    ax = Vector(axis).normalized()
    p0 = c - ax * thick / 2
    ch = min(chamfer, thick * 0.45, r * 0.45)
    prof = [(0.0, 0.0), (r - ch, 0.0), (r, ch), (r, thick - ch), (r - ch, thick), (0.0, thick)]
    L.lathe(mb, prof, tuple(p0), tuple(ax), seg, mat)


# ---------------------------------------------------------------------------
# Trayectorias y barridos
# ---------------------------------------------------------------------------
def catmull(points, samples=6, closed=False):
    """Interpola una polilínea con Catmull-Rom (centrípeta) para trayectorias suaves."""
    pts = [Vector(p) for p in points]
    if len(pts) < 3:
        return pts
    out = []
    n = len(pts)
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0] * 2 - pts[1]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1] * 2 - pts[-2]
        for k in range(samples):
            t = k / samples
            t2, t3 = t * t, t * t * t
            p = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                       (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
            out.append(p)
    if not closed:
        out.append(pts[-1])
    return out


def frames(path, up=None, closed=False):
    """Marcos de transporte paralelo a lo largo de una trayectoria: lista de (t, n, b)."""
    pts = [Vector(p) for p in path]
    n = len(pts)
    tans = []
    for i in range(n):
        if closed:
            t = pts[(i + 1) % n] - pts[i - 1]
        elif i == 0:
            t = pts[1] - pts[0]
        elif i == n - 1:
            t = pts[-1] - pts[-2]
        else:
            t = pts[i + 1] - pts[i - 1]
        tans.append(t.normalized())
    ref = Vector(up) if up is not None else (Vector((0, 0, 1)) if abs(tans[0].z) < 0.9 else Vector((1, 0, 0)))
    nrm = (ref - tans[0] * ref.dot(tans[0])).normalized()
    out = []
    for i in range(n):
        if i > 0:
            if up is not None:
                nrm = (ref - tans[i] * ref.dot(tans[i]))
                if nrm.length < 1e-6:
                    nrm = out[-1][1]
                nrm.normalize()
            else:
                axis = tans[i - 1].cross(tans[i])
                if axis.length > 1e-9:
                    ang = tans[i - 1].angle(tans[i])
                    nrm = Matrix.Rotation(ang, 3, axis.normalized()) @ nrm
                nrm = (nrm - tans[i] * nrm.dot(tans[i])).normalized()
        out.append((tans[i], nrm, tans[i].cross(nrm)))
    return out


def sweep(mb, path, profile, closed_path=False, closed_profile=True, mat=0, up=None, caps=True, scale=None):
    """Barre un perfil 2D (x = binormal, y = normal) a lo largo de una trayectoria 3D.

    `profile` se recorre en sentido antihorario; las caras se orientan hacia fuera del perfil.
    `scale` (opcional): función i -> factor de escala del perfil en cada punto.
    """
    pts = [Vector(p) for p in path]
    fr = frames(pts, up, closed_path)
    rings = []
    cen = []
    for i, (p, (t, nrm, b)) in enumerate(zip(pts, fr)):
        s = scale(i) if scale else 1.0
        ring = [tuple(p + b * (x * s) + nrm * (y * s)) for (x, y) in profile]
        rings.append(ring)
        cen.append(p + sum(((b * x + nrm * y) * s for (x, y) in profile), Vector()) / len(profile))
    m = len(profile)
    np_ = len(rings)
    rng = range(np_) if closed_path else range(np_ - 1)
    for i in rng:
        j = (i + 1) % np_
        ra, rb = rings[i], rings[j]
        ka = range(m) if closed_profile else range(m - 1)
        for k in ka:
            kk = (k + 1) % m
            q = [ra[k], ra[kk], rb[kk], rb[k]]
            c = sum((Vector(x) for x in q), Vector()) / 4
            mid = (cen[i] + cen[j]) * 0.5
            mb.face(q, mat, want=c - mid)
    if caps and closed_profile and not closed_path:
        mb.face(rings[0], mat, want=-fr[0][0])
        mb.face(rings[-1], mat, want=fr[-1][0])


def circle_profile(r, seg=10):
    return [(r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg)) for k in range(seg)]


def rect_profile(w, h, r=0.0, seg=2):
    if r <= 0:
        return [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    pts = []
    for cx, cy, a0 in ((w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
                       (-w / 2 + r, -h / 2 + r, 180)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def hose(mb, points, r, seg=12, samples=6, mat=0, caps=True, zmin=0.262):
    """Manguera o cable con trayectoria suavizada (sin bajar de zmin + r: altura libre oficial)."""
    path = catmull(points, samples)
    if zmin is not None:
        for p in path:
            p.z = max(p.z, zmin + r)
    sweep(mb, path, circle_profile(r, seg), mat=mat, caps=caps)
    return path


def corrugated(mb, points, r, seg=12, pitch=0.008, mat=0):
    """Tubo corrugado (protector de mazo de cables)."""
    path = catmull(points, 8)
    # remuestreo a paso constante
    res = [path[0]]
    acc = 0.0
    for a, b in zip(path, path[1:]):
        d = (b - a).length
        acc += d
        if acc >= pitch / 2:
            res.append(b)
            acc = 0.0
    if (res[-1] - path[-1]).length > 1e-6:
        res.append(path[-1])
    sweep(mb, res, circle_profile(r, seg), mat=mat, scale=lambda i: 1.0 if i % 2 == 0 else 0.86)


# ---------------------------------------------------------------------------
# Tornillería y fijaciones
# ---------------------------------------------------------------------------
def flange_bolt(mb, pos, axis, d=0.010, mat=0, shank=0.0):
    """Tornillo de cabeza hexagonal con brida (cabeza de 0,65·d sobre brida Ø2,1·d)."""
    p = Vector(pos)
    ax = Vector(axis).normalized()
    s = d * 1.5                                   # entrecaras de la cabeza (M10 -> 15 mm aprox.)
    hexr = s / math.sqrt(3)
    L.lathe(mb, [(0.0, 0.0), (d * 1.05, 0.0), (d * 1.05, d * 0.12), (d * 0.9, d * 0.18)], tuple(p), tuple(ax), 16, mat)
    L.lathe(mb, [(hexr, d * 0.18), (hexr, d * 0.75), (hexr * 0.85, d * 0.82), (0.0, d * 0.82)], tuple(p),
            tuple(ax), 6, mat, phase=math.pi / 6)
    if shank > 0:
        L.lathe(mb, [(d / 2, 0.0), (d / 2, -shank), (0.0, -shank - d * 0.1)], tuple(p), tuple(ax), 10, mat)


def hex_nut(mb, pos, axis, d=0.010, mat=0, stud=0.6):
    """Tuerca hexagonal con brida y extremo de espárrago saliente."""
    p = Vector(pos)
    ax = Vector(axis).normalized()
    s = d * 1.5
    hexr = s / math.sqrt(3)
    L.lathe(mb, [(0.0, 0.0), (d * 1.0, 0.0), (d * 1.0, d * 0.12)], tuple(p), tuple(ax), 16, mat)
    L.lathe(mb, [(hexr, d * 0.12), (hexr, d * 0.9), (d * 0.5, d * 0.95)], tuple(p), tuple(ax), 6, mat,
            phase=math.pi / 6)
    if stud > 0:
        L.lathe(mb, [(d * 0.45, d * 0.9), (d * 0.45, d * (0.9 + stud)), (0.0, d * (0.95 + stud))], tuple(p),
                tuple(ax), 10, mat)


def torx_screw(mb, pos, axis, d=0.006, mat=0):
    """Tornillo Torx de cabeza alomada con hueco hexalobular aproximado."""
    p = Vector(pos)
    ax = Vector(axis).normalized()
    L.lathe(mb, [(0.0, 0.0), (d * 1.0, 0.0), (d * 0.95, d * 0.25), (d * 0.7, d * 0.45), (d * 0.38, d * 0.5),
                 (d * 0.38, d * 0.25), (0.0, d * 0.22)], tuple(p), tuple(ax), 12, mat)


def push_clip(mb, pos, axis, d=0.012, mat=0):
    """Grapa de empuje (cabeza abombada de plástico)."""
    p = Vector(pos)
    ax = Vector(axis).normalized()
    L.lathe(mb, [(0.0, 0.0), (d * 0.5, 0.0), (d * 0.48, d * 0.08), (d * 0.36, d * 0.16), (d * 0.12, d * 0.2),
                 (0.0, d * 0.2)], tuple(p), tuple(ax), 12, mat)


def rivet(mb, pos, axis, d=0.008, mat=0):
    """Cabeza de remache autoperforante / flow-form (Ø 8 mm según el manual de reparación)."""
    p = Vector(pos)
    ax = Vector(axis).normalized()
    L.lathe(mb, [(0.0, 0.0), (d * 0.8, 0.0), (d * 0.75, d * 0.12), (d * 0.5, d * 0.2), (0.0, d * 0.22)],
            tuple(p), tuple(ax), 10, mat)


def ball_joint(mb, center, axis, r=0.026, mat_body=0, mat_boot=1):
    """Rótula con guardapolvos de goma: carcasa + fuelle + espárrago."""
    c = Vector(center)
    ax = Vector(axis).normalized()
    L.lathe(mb, [(0.0, -r * 0.9), (r * 1.1, -r * 0.8), (r * 1.15, -r * 0.2), (r * 0.95, 0.0)], tuple(c), tuple(ax),
            20, mat_body)
    L.lathe(mb, [(r * 0.95, 0.0), (r * 1.05, r * 0.4), (r * 0.8, r * 0.8), (r * 0.9, r * 1.0), (r * 0.45, r * 1.3)],
            tuple(c), tuple(ax), 20, mat_boot)
    L.lathe(mb, [(r * 0.4, r * 1.3), (r * 0.35, r * 2.2), (r * 0.3, r * 2.3), (0.0, r * 2.35)], tuple(c),
            tuple(ax), 12, mat_body)


def boot(mb, p0, p1, r0, r1, folds=6, seg=20, mat=0):
    """Fuelle de goma (guardapolvos de cremallera o de junta homocinética)."""
    p0, p1 = Vector(p0), Vector(p1)
    ax = p1 - p0
    lg = ax.length
    prof = []
    for k in range(folds * 2 + 1):
        t = k / (folds * 2)
        r = r0 + (r1 - r0) * t
        prof.append((r * (1.0 if k % 2 == 0 else 1.22), lg * t))
    L.lathe(mb, prof, tuple(p0), tuple(ax.normalized()), seg, mat)


def prism(mb, poly2d, origin, u, v, depth, normal=None, mat=0, cap=True):
    """Extrusión de un polígono 2D con caras orientadas hacia fuera."""
    o, u, v = Vector(origin), Vector(u), Vector(v)
    n = Vector(normal).normalized() if normal is not None else u.cross(v).normalized()
    a = [o + u * p[0] + v * p[1] for p in poly2d]
    b = [p + n * depth for p in a]
    c = sum(a, Vector()) / len(a) + n * depth * 0.5
    m = len(a)
    for i in range(m):
        j = (i + 1) % m
        q = [a[i], a[j], b[j], b[i]]
        mb.face([tuple(x) for x in q], mat, want=(a[i] + a[j]) * 0.5 + n * depth * 0.5 - c)
    if cap:
        mb.face([tuple(x) for x in a], mat, want=-n)
        mb.face([tuple(x) for x in b], mat, want=n)


# ---------------------------------------------------------------------------
# Piezas fundidas: placa con nervaduras
# ---------------------------------------------------------------------------
def ribbed_plate(mb, origin, u, v, poly2d, thick, rib_h, rib_t, rib_lines, normal=None, mat=0):
    """Placa poligonal (en el plano origen+u,v) con nervaduras rectas sobre una de sus caras.

    rib_lines: lista de segmentos ((x0, y0), (x1, y1)) en coordenadas del plano.
    """
    o, u, v = Vector(origin), Vector(u).normalized(), Vector(v).normalized()
    n = Vector(normal).normalized() if normal is not None else u.cross(v).normalized()
    prism(mb, poly2d, o, u, v, thick, normal=n, mat=mat)
    for (x0, y0), (x1, y1) in rib_lines:
        a = o + u * x0 + v * y0 + n * thick
        b = o + u * x1 + v * y1 + n * thick
        d = b - a
        if d.length < 1e-4:
            continue
        side = d.normalized().cross(n).normalized()
        q0 = [a + side * rib_t / 2, b + side * rib_t / 2, b - side * rib_t / 2, a - side * rib_t / 2]
        q1 = [p + n * rib_h for p in q0]
        mb.face([tuple(p) for p in q1], mat, want=n)
        for i in range(4):
            j = (i + 1) % 4
            mb.face([tuple(q0[i]), tuple(q0[j]), tuple(q1[j]), tuple(q1[i])], mat,
                    want=((q0[i] + q0[j]) * 0.5 - (a + b) * 0.5))


# ---------------------------------------------------------------------------
# Texto en relieve (inscripciones del neumático, rótulos)
# ---------------------------------------------------------------------------
def text_outline(text, size=0.01, extrude=0.0, font=None, align="CENTER", resolution=3):
    """Convierte un texto en malla y devuelve (verts, faces) en el plano XY (Z = relieve)."""
    cu = bpy.data.curves.new("__txt", "FONT")
    cu.body = text
    cu.size = size
    cu.extrude = extrude
    cu.align_x = align
    cu.resolution_u = resolution
    if font is not None:
        cu.font = font
    ob = bpy.data.objects.new("__txt", cu)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    me = ob.evaluated_get(dg).to_mesh()
    verts = [v.co.copy() for v in me.vertices]
    faces = [list(p.vertices) for p in me.polygons]
    ob.evaluated_get(dg).to_mesh_clear()
    bpy.data.objects.remove(ob)
    bpy.data.curves.remove(cu)
    return verts, faces


# ---------------------------------------------------------------------------
# Creación de objetos
# ---------------------------------------------------------------------------
def make(mb, name, system, mats, parent=None, edir=(0, 0, 1), dist=0.2, stage=6, group="", label="",
         fid="A", note=None, smooth=35, bevel=0.0, origin=None):
    """Crea el objeto, suaviza por ángulo, aplica bisel opcional y registra la explosión."""
    if not mb.faces:
        return None
    if fid == "V":
        # Criterio del proyecto: «Verificado» exige que la geometría proceda de medidas o planos.
        # En estas piezas lo verificado es la existencia, la denominación y las fijaciones (manual
        # de servicio); la forma es una reconstrucción, por lo que se clasifican como «Reconstruido».
        fid = "R"
        note = note or "Existencia, denominación y fijaciones verificadas en el manual de servicio; forma reconstruida"
    o = mb.build(name, system, mats, parent=parent, origin=origin)
    L.set_smooth_by_angle(o, smooth)
    if bevel:
        L.bevel(o, bevel, 2, 40)
    L.explode(o, edir, dist, stage, group, label or name, fid, note=note)
    return o
