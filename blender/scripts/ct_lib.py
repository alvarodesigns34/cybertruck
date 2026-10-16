"""Utilidades de construcción para la escena del Cybertruck en Blender (bpy).

Funciones para crear mallas a partir de polígonos, organizar colecciones, asignar
materiales y registrar los metadatos de la vista explosionada en cada objeto.
"""

import math
import bpy
import bmesh
from mathutils import Vector, Matrix

ROOT_NAME = "CYBERTRUCK_ROOT"

# Etapas lógicas de desmontaje (ver docs/model-specification.md)
STAGES = {
    1: "Paneles exteriores y elementos de apertura",
    2: "Conjuntos interiores",
    3: "Estructura de carrocería y bajos",
    4: "Suspensión, ruedas y frenos",
    5: "Batería y tren motriz",
    6: "Componentes pequeños y herrajes",
}

SYSTEM_COLLECTIONS = [
    "BODY_STRUCTURE", "EXTERIOR_PANELS", "DOORS_AND_HATCHES", "GLASS_AND_MIRRORS",
    "LIGHTING", "FRONT_WHEELS_AND_BRAKES", "REAR_WHEELS_AND_BRAKES", "FRONT_SUSPENSION",
    "REAR_SUSPENSION", "STEERING", "BATTERY_ASSEMBLY", "DRIVE_UNITS", "UNDERBODY",
    "INTERIOR_DASHBOARD", "INTERIOR_SEATS", "INTERIOR_DOORS", "INTERIOR_CONTROLS",
    "INTERIOR_TRIM", "CARGO_BED", "BODY_FASTENERS", "REFERENCE_AND_HELPERS",
]


# ---------------------------------------------------------------------------
# Colecciones
# ---------------------------------------------------------------------------
def ensure_collection(name, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
    parent = parent or bpy.context.scene.collection
    if col.name not in [c.name for c in parent.children]:
        parent.children.link(col)
    return col


def vehicle_collection(system):
    top = ensure_collection("CYBERTRUCK")
    return ensure_collection(system, top)


def link_only(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


# ---------------------------------------------------------------------------
# Raíz y conjuntos
# ---------------------------------------------------------------------------
def world_matrix(obj):
    """Matriz de mundo calculada a partir de la cadena de padres (sin depender del depsgraph)."""
    if obj is None:
        return Matrix.Identity(4)
    m = obj.matrix_basis.copy()
    if obj.parent is not None:
        m = world_matrix(obj.parent) @ obj.matrix_parent_inverse @ m
    return m


def parent_keep_world(obj, parent, world_location):
    """Asigna el padre y coloca el objeto en una posición de mundo dada (padres sin rotación)."""
    obj.parent = parent
    obj.matrix_parent_inverse = Matrix.Identity(4)
    pw = world_matrix(parent)
    obj.location = pw.inverted() @ Vector(world_location)

def root():
    obj = bpy.data.objects.get(ROOT_NAME)
    if obj is None:
        obj = bpy.data.objects.new(ROOT_NAME, None)
        obj.empty_display_type = "ARROWS"
        obj.empty_display_size = 0.5
        link_only(obj, ensure_collection("CYBERTRUCK"))
        obj["explode"] = 0.0
        ui = obj.id_properties_ui("explode")
        ui.update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
                  description="Factor de vista explosionada (0 = ensamblado, 1 = explosionado)")
    return obj


def assembly(name, system, location=(0, 0, 0), parent=None):
    """Crea (o reutiliza) un vacío que agrupa un subconjunto con pivote significativo."""
    obj = bpy.data.objects.get(name)
    if obj is None:
        obj = bpy.data.objects.new(name, None)
        obj.empty_display_type = "PLAIN_AXES"
        obj.empty_display_size = 0.15
    link_only(obj, vehicle_collection(system))
    parent_keep_world(obj, parent or root(), location)
    obj["system"] = system
    return obj


# ---------------------------------------------------------------------------
# Mallas
# ---------------------------------------------------------------------------
def _remove_existing(name):
    old = bpy.data.objects.get(name)
    if old is not None:
        data = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if data is not None and data.users == 0:
            if isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)


def mesh_object(name, verts, faces, system, material=None, parent=None, origin=None,
                smooth=False, uv="auto"):
    """Crea un objeto de malla a partir de vértices (mundo) y caras.

    El origen se coloca en `origin` (coordenadas de mundo) o en el centro de la caja
    delimitadora, de modo que la transformación del objeto sea significativa.
    """
    _remove_existing(name)
    vs = [Vector(v) for v in verts]
    if origin is None:
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        origin = (mn + mx) * 0.5
    origin = Vector(origin)
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v - origin) for v in vs], [], [tuple(f) for f in faces])
    me.validate(clean_customdata=False)
    me.update()
    obj = bpy.data.objects.new(name, me)
    link_only(obj, vehicle_collection(system))
    parent_keep_world(obj, parent or root(), origin)
    obj["system"] = system
    if material is not None:
        assign_material(obj, material)
    for p in me.polygons:
        p.use_smooth = smooth
    if uv == "auto":
        auto_uv(obj)
    return obj


def bm_object(name, bm, system, material=None, parent=None, origin=None, smooth=False,
              uv="auto"):
    """Convierte un bmesh (en coordenadas de mundo) en objeto."""
    verts = [v.co.copy() for v in bm.verts]
    bm.verts.index_update()
    faces = [[v.index for v in f.verts] for f in bm.faces]
    mats = [f.material_index for f in bm.faces]
    obj = mesh_object(name, verts, faces, system, material, parent, origin, smooth, uv)
    if any(mats):
        for p, mi in zip(obj.data.polygons, mats):
            p.material_index = mi
    return obj


def assign_material(obj, mat):
    mats = mat if isinstance(mat, (list, tuple)) else [mat]
    obj.data.materials.clear()
    for m in mats:
        obj.data.materials.append(m)


def auto_uv(obj, scale=1.0):
    """Proyección UV por caja alineada con los ejes del vehículo (U = longitudinal).

    Mantiene una densidad de texel coherente (1 unidad UV = 1 m) y orienta el
    cepillado del acero inoxidable en dirección longitudinal.
    """
    me = obj.data
    if not me.polygons:
        return
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    uvl = me.uv_layers.active.data
    loc = world_matrix(obj).translation
    for p in me.polygons:
        n = p.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co + loc
            if ax == 0:      # cara lateral: U = Y, V = Z
                u, v = co.y, co.z
            elif ax == 2:    # cara superior/inferior: U = Y, V = X
                u, v = co.y, co.x
            else:            # cara frontal/trasera: U = X, V = Z
                u, v = co.x, co.z
            uvl[li].uv = (u * scale, v * scale)


def solidify(obj, thickness, offset=-1.0, even=True, rim=True):
    m = obj.modifiers.new("Espesor", "SOLIDIFY")
    m.thickness = thickness
    m.offset = offset
    m.use_even_offset = even
    m.use_rim = rim
    m.use_quality_normals = True
    return m


def bevel(obj, width, segments=2, angle=30.0, harden=True, profile=0.5):
    m = obj.modifiers.new("Bisel", "BEVEL")
    m.width = width
    m.segments = segments
    m.limit_method = "ANGLE"
    m.angle_limit = math.radians(angle)
    m.harden_normals = harden
    m.profile = profile
    m.miter_outer = "MITER_ARC"
    return m


def weighted_normals(obj):
    m = obj.modifiers.new("Normales", "WEIGHTED_NORMAL")
    m.keep_sharp = True
    m.weight = 50
    return m


def subsurf(obj, levels=1, render=None):
    m = obj.modifiers.new("Subdivision", "SUBSURF")
    m.levels = levels
    m.render_levels = levels if render is None else render
    return m


def set_smooth_by_angle(obj, angle=30.0):
    """Sombreado suave con aristas vivas por ángulo (Blender 4.1+)."""
    me = obj.data
    for p in me.polygons:
        p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(angle))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Metadatos de vista explosionada
# ---------------------------------------------------------------------------
def explode(obj, direction, distance, stage, group, label=None, fidelity="R", note=None):
    """Registra la dirección y la distancia de separación de un componente.

    La dirección se expresa en coordenadas de mundo de Blender y se normaliza.
    `fidelity`: V (verificado), R (reconstruido) o A (aproximado).
    """
    d = Vector(direction)
    if d.length > 1e-9:
        d.normalize()
    obj["explode_dir"] = [round(d.x, 5), round(d.y, 5), round(d.z, 5)]
    obj["explode_dist"] = float(distance)
    obj["explode_stage"] = int(stage)
    obj["explode_group"] = group
    obj["fidelity"] = fidelity
    if label:
        obj["label_es"] = label
    if note:
        obj["note_es"] = note
    return obj


def mirror_object(src, name):
    """Duplica un objeto reflejado en X (lado izquierdo <-> derecho) con malla propia."""
    _remove_existing(name)
    me = src.data.copy()
    me.name = name
    mirror = Matrix.Scale(-1, 4, (1, 0, 0))
    me.transform(mirror)
    me.flip_normals()
    obj = bpy.data.objects.new(name, me)
    for c in src.users_collection:
        c.objects.link(obj)
    obj.parent = src.parent
    obj.matrix_parent_inverse = Matrix.Identity(4)
    bpy.context.view_layer.update()
    obj.matrix_world = mirror @ src.matrix_world @ mirror
    for k in src.keys():
        if k.startswith("explode_dir"):
            d = src[k]
            obj[k] = [-d[0], d[1], d[2]]
        elif k not in ("_RNA_UI",):
            obj[k] = src[k]
    for m in src.modifiers:
        nm = obj.modifiers.new(m.name, m.type)
        for attr in dir(m):
            if attr.startswith("_") or attr in ("name", "type", "rna_type", "is_override_data",
                                                "persistent_uid", "show_expanded"):
                continue
            try:
                setattr(nm, attr, getattr(m, attr))
            except Exception:
                pass
    return obj


# ---------------------------------------------------------------------------
# Geometría 2D auxiliar
# ---------------------------------------------------------------------------
def clip_polygon(poly, a, b, c):
    """Sutherland–Hodgman: conserva la parte de `poly` con a*x + b*y + c >= 0."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] + c
        fq = a * q[0] + b * q[1] + c
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def split_by_levels(poly, levels, axis=1):
    """Divide un polígono 2D en bandas horizontales (axis=1) o verticales (axis=0)."""
    levels = sorted(levels)
    bounds = [-1e9] + levels + [1e9]
    pieces = []
    for lo, hi in zip(bounds, bounds[1:]):
        if axis == 1:
            p = clip_polygon(poly, 0, 1, -lo)
            p = clip_polygon(p, 0, -1, hi) if p else p
        else:
            p = clip_polygon(poly, 1, 0, -lo)
            p = clip_polygon(p, -1, 0, hi) if p else p
        if len(p) >= 3:
            pieces.append(((lo + hi) * 0.5 if abs(hi) < 1e8 and abs(lo) < 1e8 else (lo if abs(lo) < 1e8 else hi), p))
    return pieces


def dedupe(poly, eps=1e-6):
    out = []
    for p in poly:
        if not out or (abs(p[0] - out[-1][0]) > eps or abs(p[1] - out[-1][1]) > eps):
            out.append(p)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < eps and abs(out[0][1] - out[-1][1]) < eps:
        out.pop()
    return out


def polygon_area(poly):
    a = 0.0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        a += x0 * y1 - x1 * y0
    return 0.5 * a


def newell(pts):
    """Normal de un polígono (método de Newell), robusta para n-gonos."""
    n = Vector((0.0, 0.0, 0.0))
    for i in range(len(pts)):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % len(pts)]
        n.x += (y0 - y1) * (z0 + z1)
        n.y += (z0 - z1) * (x0 + x1)
        n.z += (x0 - x1) * (y0 + y1)
    return n


class MeshBuilder:
    """Acumula vértices y caras (con fusión de vértices coincidentes)."""

    def __init__(self, merge=1e-5):
        self.verts = []
        self.faces = []
        self.mats = []
        self._index = {}
        self.merge = merge

    def v(self, co):
        key = tuple(round(c / self.merge) for c in co)
        idx = self._index.get(key)
        if idx is None:
            idx = len(self.verts)
            self.verts.append(tuple(co))
            self._index[key] = idx
        return idx

    def face(self, cos, mat=0, flip=False, want=None):
        """Añade una cara. `want` orienta la normal hacia la dirección indicada."""
        idx = [self.v(c) for c in cos]
        clean = []
        for i in idx:
            if not clean or clean[-1] != i:
                clean.append(i)
        if len(clean) > 1 and clean[0] == clean[-1]:
            clean.pop()
        if len(set(clean)) < 3:
            return
        if want is not None:
            n = newell([self.verts[i] for i in clean])
            if n.dot(Vector(want)) < 0:
                clean.reverse()
        elif flip:
            clean.reverse()
        self.faces.append(clean)
        self.mats.append(mat)

    def quad_strip(self, ring_a, ring_b, closed=False, mat=0, flip=False, want_fn=None):
        """Une dos anillos con cuadriláteros. `want_fn(centro)` devuelve la normal deseada."""
        n = len(ring_a)
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            j = (i + 1) % n
            q = [ring_a[i], ring_a[j], ring_b[j], ring_b[i]]
            if want_fn is not None:
                c = sum((Vector(p) for p in q), Vector()) / 4.0
                self.face(q, mat, want=want_fn(c))
            else:
                self.face(q, mat, flip)

    def build(self, name, system, material=None, parent=None, origin=None, smooth=False):
        obj = mesh_object(name, self.verts, self.faces, system, material, parent, origin, smooth)
        if any(self.mats):
            for p, mi in zip(obj.data.polygons, self.mats):
                p.material_index = mi
        return obj


def recalc_normals(obj, inside=False):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if inside:
        for f in bm.faces:
            f.normal_flip()
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


# ---------------------------------------------------------------------------
# Primitivas paramétricas (en coordenadas de mundo)
# ---------------------------------------------------------------------------
def frame_from_axis(axis):
    """Devuelve una base ortonormal (u, v, w) con w = eje dado."""
    w = Vector(axis).normalized()
    ref = Vector((0, 0, 1)) if abs(w.z) < 0.9 else Vector((1, 0, 0))
    u = w.cross(ref).normalized()
    v = w.cross(u).normalized()
    return u, v, w


def lathe(mb, profile, center, axis, segments=48, mat=0, closed_profile=False, phase=0.0,
          cap_start=False, cap_end=False):
    """Revoluciona un perfil (radio, posición axial) alrededor de un eje."""
    c = Vector(center)
    u, v, w = frame_from_axis(axis)
    rings = []
    for (r, a) in profile:
        ring = []
        for k in range(segments):
            t = phase + 2 * math.pi * k / segments
            ring.append(tuple(c + w * a + (u * math.cos(t) + v * math.sin(t)) * r))
        rings.append(ring)
    for i in range(len(rings) - 1):
        mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=mat)
    if closed_profile:
        mb.quad_strip(rings[-1], rings[0], closed=True, mat=mat)
    if cap_start:
        mb.face(list(reversed(rings[0])), mat)
    if cap_end:
        mb.face(rings[-1], mat)
    return rings


def box(mb, center, size, mat=0, rot=None):
    """Caja orientada (rot: matriz 3x3 opcional)."""
    c = Vector(center)
    sx, sy, sz = (s * 0.5 for s in size)
    corners = []
    for dz in (-1, 1):
        for dy in (-1, 1):
            for dx in (-1, 1):
                p = Vector((dx * sx, dy * sy, dz * sz))
                if rot is not None:
                    p = rot @ p
                corners.append(tuple(c + p))
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for q in f:
        mb.face([corners[i] for i in q], mat)


def prism(mb, poly2d, plane_origin, u, v, depth, normal=None, mat=0, cap=True):
    """Extruye un polígono 2D definido en el plano (origen, u, v) una profundidad dada."""
    o = Vector(plane_origin)
    u, v = Vector(u), Vector(v)
    n = Vector(normal) if normal is not None else u.cross(v).normalized()
    a = [tuple(o + u * p[0] + v * p[1]) for p in poly2d]
    b = [tuple(Vector(p) + n * depth) for p in a]
    mb.quad_strip(a, b, closed=True, mat=mat)
    if cap:
        mb.face(list(reversed(a)), mat)
        mb.face(b, mat)


def tube(mb, path, radius, segments=10, mat=0, cap=True):
    """Tubo a lo largo de una polilínea 3D (cables, conductos, barras)."""
    pts = [Vector(p) for p in path]
    rings = []
    for i, p in enumerate(pts):
        if i == 0:
            t = (pts[1] - pts[0]).normalized()
        elif i == len(pts) - 1:
            t = (pts[-1] - pts[-2]).normalized()
        else:
            t = ((pts[i + 1] - pts[i]).normalized() + (pts[i] - pts[i - 1]).normalized()).normalized()
        u, v, _ = frame_from_axis(t)
        rings.append([tuple(p + (u * math.cos(2 * math.pi * k / segments) +
                                 v * math.sin(2 * math.pi * k / segments)) * radius)
                      for k in range(segments)])
    for i in range(len(rings) - 1):
        mb.quad_strip(rings[i], rings[i + 1], closed=True, mat=mat)
    if cap:
        mb.face(list(reversed(rings[0])), mat)
        mb.face(rings[-1], mat)
