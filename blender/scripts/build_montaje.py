"""Ajuste final de montaje: elimina las interferencias (piezas que se atraviesan) del vehículo ensamblado.

Se ejecuta con `build_all.run(parts=(..., "v4", "montaje", "explode", ...))`, después de la versión 4 (cuya pasada
`build_v4.fit_internals` ya ajusta los interiores a sus carcasas) y antes de la vista explosionada. Tiene dos
pasadas, ambas reproducibles a partir de la escena construida:

1. **Recortes** (`CARVE`): las pieles y estructuras ocultas sobre las que se montan otras piezas reciben el hueco
   de las piezas que las atraviesan, como en el coche real: la moqueta y las alfombrillas tienen recortes para los
   carriles de los asientos, la consola o los conductos; los anillos de puerta, los alojamientos de bisagras,
   cerraduras, juntas y guarnecidos; las juntas de goma, la huella de lo que las comprime; el raíl de la persiana,
   el canal por el que corren sus lamas. El recorte es una diferencia booleana exacta con las piezas vecinas
   ampliadas `GAP` a lo largo de sus normales, de modo que queda una holgura y no solo un contacto.
2. **Recolocaciones** (`MOVES`, tabla en `montaje_desplazamientos.json`): desplazamientos de accesorios (mazos,
   módulos, soportes) calculados por `resolver()` para que dejen de atravesar a sus vecinos sin crear cruces
   nuevos.

El detector de interferencias está en `interferencias.py`; los criterios y el estado se documentan en
`docs/research-and-fidelity.md` (§11).
"""

import json
import os
import re

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
MOVES_FILE = os.path.join(HERE, "montaje_desplazamientos.json")
GAP = 0.0006            # holgura que deja un recorte (m)

# (patrón del objeto que se recorta, modo, motivo). Modos:
#   "todo":  lo recortan todas las piezas que lo atraviesan (salvo las penetraciones intencionadas).
#   "suelo": piel apoyada en el suelo; la recortan las piezas que están encima o la atraviesan, y las que quedan
#            por debajo (batería, cables) se recortan con ella.
#   "comprimir": pieza blanda (juntas de goma); no se recorta: sus vértices se llevan a la superficie de lo que la
#            comprime (`squash`), como hace la junta real al cerrar la puerta.
CARVE = [
    (r"^BODY_DoorRing_[LR]$", "todo", "alojamientos de bisagras, cerraduras, juntas y guarnecidos en el anillo"),
    (r"^INT_Carpet$", "suelo", "recortes de la moqueta para carriles, consola, conductos y mazos"),
    (r"^INT_Center_Floor_Trim$", "suelo", "recortes del guarnecido central del suelo"),
    (r"^BODY_NVH_Pads$", "todo", "espumas acústicas con el hueco de lo que las atraviesa"),
    (r"^INT_IP_TopPad$", "todo", "aberturas del tablero para la guantera, las pantallas y los conductos"),
    (r"^INT_Cantrail_[LR]$", "todo", "guarnecido del larguero del techo sobre juntas y soportes"),
    (r"^INT_Console_Body$", "todo", "consola: alojamientos de los carriles, hebillas y paso del mazo del salpicadero"),
    (r"^INT_Trim_APillar_[LR]$", "todo", "guarnecido del pilar A sobre el mazo del parabrisas y las grapas"),
    (r"^BRK_(FL|FR|RL|RR)_Shield$", "todo", "escudo de polvo con el recorte de la mangueta, la pinza y la rótula"),
    (r"^CARGO_Bed_Side_Wall_(Upper|Lower)_[LR]$", "todo", "laterales de la caja bajo el «mast» y junto a las torres"),
    (r"^CARGO_Bed_Closeout_Rear_[LR]$", "todo", "remates traseros de la caja sobre cierres, barra de torsión y tirantes"),
    (r"^EXT_Bed_Side_Corner_Brackets_[LR]$", "todo", "soportes de esquina de la caja sobre los cierres del portón"),
    (r"^BODY_(Sail_Datum_Bracket|Mast_Backing_Plates)_[LR]$", "todo", "soportes y placas soldados al «mast»"),
    (r"^INT_DoorTrim_(FL|FR|RL|RR)$", "todo", "guarnecidos de puerta: alojamientos de botón, tira de cintura, juntas y "
     "placas de tuercas"),
    (r"^INT_Overhead_Console$", "todo", "consola de techo con los alojamientos de sensores, cámara y retrovisor"),
    (r"^EXT_Windshield_Glare_Shield$", "todo", "parasol del parabrisas sobre antenas y retrovisor"),
    (r"^INT_IP_Quarter_Panel_[LR]$", "todo", "tapas laterales del salpicadero sobre el extremo de la viga y los pasacables"),
    (r"^CARGO_Tonneau_Rail_[LR]$", "todo", "canal del raíl por el que corren las lamas y los carros"),
    (r"^INT_SteeringWheel_Hub$", "todo", "buje del volante con los alojamientos de los rodillos y botones"),
    (r"^EXT_Fender_Baffle_Front_[LR]$", "todo", "deflector del guardabarros con los huecos de las bisagras y del tirante"),
    (r"^BODY_CPillar_Inner_[LR]$", "todo", "pilar C interior con los alojamientos de la cerradura, del presentador y de "
     "las placas de espárragos de la puerta trasera"),
    (r"^EXT_Grille_Foam_Seals$", "comprimir", "juntas de espuma de la rejilla comprimidas contra la fascia"),
    (r"^BAT_Lid_Seal$", "comprimir", "junta de la tapa de la batería comprimida bajo el travesaño de los asientos"),
    (r"^EXT_Tailgate_Seal(_Side_[LR])?$", "comprimir", "juntas del portón comprimidas contra las torres y las bisagras"),
    (r"^CARGO_Tonneau_Closeout_Foam$", "comprimir", "espuma de cierre de la persiana comprimida por la última lama"),
    (r"^INT_IP_Gap_Hiders$", "comprimir", "cubrejuntas de goma del salpicadero comprimidos entre los paneles"),
    (r"^INT_Door_NVH_Foam_(FL|FR|RL|RR)$", "todo", "espuma acústica de la puerta con los huecos del altavoz y del "
     "tirador de apertura manual"),
    (r"^EXT_Door_Primary_Seals_[LR]$", "comprimir", "juntas primarias comprimidas por la puerta"),
    (r"^EXT_Header_Seal_[LR]$", "comprimir", "junta del larguero comprimida"),
    (r"^EXT_Door_(FL|FR|RL|RR)_Seals$", "comprimir", "juntas de la puerta comprimidas"),
]


# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------
def _vehicle_meshes():
    import build_explode as E
    return [o for o in E.vehicle_objects() if o.type == "MESH" and not o.hide_render]


def _world(o, dg):
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    vs = [ev.matrix_world @ v.co for v in me.vertices]
    me.calc_loop_triangles()
    tris = [tuple(t.vertices) for t in me.loop_triangles]
    ev.to_mesh_clear()
    return vs, tris


class Scene:
    """Árboles BVH y cajas de todas las mallas del vehículo (coordenadas de mundo, explosión a cero)."""

    def __init__(self):
        import build_explode as E
        E.set_explode(0.0)
        bpy.context.view_layer.update()
        self.d = {}
        for o in _vehicle_meshes():
            self.refresh(o.name)

    def refresh(self, name):
        import interferencias as I
        o = bpy.data.objects[name]
        vs, tris = _world(o, bpy.context.evaluated_depsgraph_get())
        if tris:
            vis = I._visible(vs, tris)
            if len(vis) < len(tris):
                tris = [tris[i] for i in vis]      # solo la superficie exterior (ver interferencias._visible)
        if not tris:
            self.d.pop(name, None)
            return
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        self.d[name] = (BVHTree.FromPolygons(vs, tris, epsilon=0.0), vs, tris, mn, mx)

    def partners(self, name, pad=0.0, include_intended=False):
        """Objetos cuya superficie corta la de `name`, sin las penetraciones intencionadas (salvo que se pidan: las
        piezas blandas se comprimen contra todas sus vecinas)."""
        import interferencias as I
        t, _, _, mn, mx = self.d[name]
        out = []
        for k, (tk, _, _, a, b) in self.d.items():
            if k == name:
                continue
            if a.x > mx.x + pad or b.x < mn.x - pad or a.y > mx.y + pad or b.y < mn.y - pad or \
               a.z > mx.z + pad or b.z < mn.z - pad:
                continue
            if t.overlap(tk) and (include_intended or not I.intended(name, k, 0.0)):
                out.append(k)
        return out


def _islands(bm):
    """Partes sueltas de una malla (conjuntos de caras unidas por aristas)."""
    seen = set()
    out = []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, isl = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            isl.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        out.append(isl)
    return out


def _solid_islands(bm, thick=0.003):
    """Convierte cada parte suelta de `bm` en un sólido cerrado: las cerradas se conservan, las láminas (con
    bordes libres) se engruesan `thick` y las que tienen aristas compartidas por más de dos caras (partes que se
    tocan) se sustituyen por su envolvente convexa."""
    bm.faces.index_update()
    bm.verts.index_update()
    out = bmesh.new()
    for isl in _islands(bm):
        edges = {e for f in isl for e in f.edges}
        boundary = any(len(e.link_faces) == 1 for e in edges)
        multi = any(len(e.link_faces) > 2 for e in edges)
        if not boundary and not multi:
            sub = bmesh.new()
            vmap = {}
            for f in isl:
                vs = []
                for v in f.verts:
                    if v.index not in vmap:
                        vmap[v.index] = sub.verts.new(v.co)
                    vs.append(vmap[v.index])
                try:
                    sub.faces.new(vs)
                except ValueError:
                    pass
        elif multi and not boundary:
            sub = _hull_points({v.co.to_tuple(6) for f in isl for v in f.verts})
        else:
            sub = _thicken(isl, thick)
        if sub is None:
            continue
        me = bpy.data.meshes.new("_tmp_s")
        sub.to_mesh(me)
        sub.free()
        out.from_mesh(me)
        bpy.data.meshes.remove(me)
    return out


def _hull_points(pts):
    if len(pts) < 4:
        return None
    hb = bmesh.new()
    for p in pts:
        hb.verts.new(p)
    try:
        res = bmesh.ops.convex_hull(hb, input=hb.verts[:])
    except Exception:
        hb.free()
        return None
    junk = list({id(g): g for g in res["geom_interior"] + res["geom_unused"]
                 if isinstance(g, bmesh.types.BMVert)}.values())
    if junk:
        bmesh.ops.delete(hb, geom=junk, context="VERTS")
    if not hb.faces:
        hb.free()
        return None
    return hb


def _thicken(faces, thick):
    """Lámina -> sólido cerrado de espesor `thick` (caras desplazadas a ambos lados y paredes en los bordes)."""
    sub = bmesh.new()
    vmap = {}
    for f in faces:
        vs = []
        for v in f.verts:
            if v.index not in vmap:
                vmap[v.index] = sub.verts.new(v.co)
            vs.append(vmap[v.index])
        try:
            sub.faces.new(vs)
        except ValueError:
            pass
    sub.normal_update()
    res = bmesh.ops.solidify(sub, geom=sub.faces[:], thickness=thick)
    # centra el espesor sobre la lámina original
    for v in sub.verts:
        v.co += v.normal * (thick / 2)
    del res
    return sub


def _union_islands(ob, max_islands=80):
    """Une con el solver MANIFOLD las partes sueltas solapadas de `ob` (sólidos cerrados), para que el objeto sea
    un único sólido sin autointersecciones, que es lo que exige ese solver. Con más de `max_islands` partes se
    deja como está."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.index_update()
    bm.verts.index_update()
    isl = _islands(bm)
    if len(isl) < 2 or len(isl) > max_islands:
        bm.free()
        return False
    meshes = []
    for faces in isl:
        sub = bmesh.new()
        vmap = {}
        for f in faces:
            vs = []
            for v in f.verts:
                if v.index not in vmap:
                    vmap[v.index] = sub.verts.new(v.co)
                vs.append(vmap[v.index])
            try:
                sub.faces.new(vs)
            except ValueError:
                pass
        me = bpy.data.meshes.new("_tmp_isl")
        sub.to_mesh(me)
        sub.free()
        meshes.append(me)
    bm.free()
    base = bpy.data.objects.new("_tmp_union", meshes[0])
    bpy.context.scene.collection.objects.link(base)
    for me in meshes[1:]:
        tmp = bpy.data.objects.new("_tmp_isl", me)
        bpy.context.scene.collection.objects.link(tmp)
        mod = base.modifiers.new("_u", "BOOLEAN")
        mod.operation = "UNION"
        mod.solver = "MANIFOLD"
        mod.object = tmp
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        new = bpy.data.meshes.new_from_object(base.evaluated_get(dg), depsgraph=dg)
        base.modifiers.remove(mod)
        old = base.data
        if len(new.polygons):
            base.data = new
            if old.users == 0:
                bpy.data.meshes.remove(old)
        else:
            bpy.data.meshes.remove(new)
        bpy.data.objects.remove(tmp, do_unlink=True)
        bpy.data.meshes.remove(me)
    old = ob.data
    ob.data = base.data
    bpy.data.objects.remove(base, do_unlink=True)
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return True


def _cutter_object(names, grow):
    """Objeto temporal con la unión de las mallas `names` ampliadas `grow` por sus normales. Las partes que no son
    sólidos cerrados se convierten en sólidos (`_solid_islands`) y las partes solapadas se unen (`_union_islands`)
    para que el solver MANIFOLD pueda usarlo. Devuelve (objeto, es_cerrado)."""
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    for n in names:
        o = bpy.data.objects[n]
        b2 = bmesh.new()
        b2.from_object(o, dg)
        b2.transform(o.matrix_world)
        if not all(e.is_manifold for e in b2.edges):
            h = _solid_islands(b2)
            b2.free()
            b2 = h
        # normales hacia fuera (las envolventes convexas y los engrosados pueden salir invertidos)
        bmesh.ops.recalc_face_normals(b2, faces=b2.faces[:])
        b2.normal_update()
        if grow:
            for v in b2.verts:
                v.co += v.normal * grow
        me = bpy.data.meshes.new("_tmp")
        b2.to_mesh(me)
        b2.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    closed = bool(bm.faces) and all(e.is_manifold for e in bm.edges)
    me = bpy.data.meshes.new("_tmp_cutter")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("_tmp_cutter", me)
    bpy.context.scene.collection.objects.link(ob)
    if closed:
        _union_islands(ob)
    return ob, closed


def _box_object(mn, mx):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    c = (mn + mx) / 2
    s = mx - mn
    for v in bm.verts:
        v.co = Vector((c.x + v.co.x * s.x, c.y + v.co.y * s.y, c.z + v.co.z * s.z))
    me = bpy.data.meshes.new("_tmp_box")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("_tmp_box", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def trim_below(part, skin, sc):
    """Recorta lo que de `part` (debajo de la piel `skin`, p. ej. la batería bajo la moqueta) asoma por encima de
    la cara inferior de la piel: plano horizontal a la menor altura de esa cara sobre la huella de la pieza."""
    _, _, _, mn, mx = sc.d[part]
    tree = sc.d[skin][0]
    zs = []
    for i in range(6):
        for j in range(6):
            x = mn.x + (mx.x - mn.x) * (i + 0.5) / 6
            y = mn.y + (mx.y - mn.y) * (j + 0.5) / 6
            hit = tree.ray_cast(Vector((x, y, mn.z - 0.5)), Vector((0, 0, 1)))[0]
            if hit is not None:
                zs.append(hit.z)
    if not zs:
        return 0
    z0 = min(zs) - GAP
    if z0 <= mn.z + 0.002:
        return 0
    o = bpy.data.objects[part]
    _bake(o)
    box = _box_object(Vector((mn.x - 0.01, mn.y - 0.01, z0)), Vector((mx.x + 0.01, mx.y + 0.01, mx.z + 0.01)))
    mod = o.modifiers.new("_trim", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "MANIFOLD" if all(e.is_manifold for e in _bm_of(o).edges) else "EXACT"
    mod.object = box
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    o.modifiers.remove(mod)
    me = box.data
    bpy.data.objects.remove(box, do_unlink=True)
    bpy.data.meshes.remove(me)
    if len(new.polygons) < 0.3 * max(1, len(o.data.polygons)):
        bpy.data.meshes.remove(new)
        return 0
    old = o.data
    new.name = old.name
    o.data = new
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return 1


def _bm_of(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    return bm


def _bake(o):
    """Aplica los modificadores de `o` a su malla (los recortes trabajan sobre la geometría final)."""
    if not len(o.modifiers) and o.data.users == 1:
        return
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    for m in list(o.modifiers):
        o.modifiers.remove(m)
    old = o.data
    new.name = old.name
    o.data = new
    if old.users == 0:
        bpy.data.meshes.remove(old)


def _solidify_sheet(o, thick=0.004):
    """Si `o` es una lámina abierta (moqueta, alfombrilla, guarnecido de chapa), la convierte en un sólido fino
    cerrado (modificador Solidify aplicado, espesor hacia el lado contrario a sus normales) para que los recortes
    booleanos sean limpios. Las piezas ya cerradas no se tocan."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    sheet = any(e.is_boundary for e in bm.edges)
    bm.free()
    if not sheet:
        return False
    mod = o.modifiers.new("_solid", "SOLIDIFY")
    mod.thickness = thick
    mod.offset = -1.0
    mod.use_rim = True
    mod.use_even_offset = True
    _bake(o)
    return True


def _tree(o):
    vs, tris = _world(o, bpy.context.evaluated_depsgraph_get())
    return BVHTree.FromPolygons(vs, tris, epsilon=0.0) if tris else None


def carve(target, cutters, grow=GAP):
    """Diferencia booleana, un cortador cada vez: `target` pierde el volumen de cada pieza de `cutters` (ampliada
    `grow` por sus normales). Se usa el solver MANIFOLD de Blender, rápido y estable, que exige sólidos cerrados:
    los cortadores abiertos (láminas) se omiten. Cada paso se conserva solo si el resultado no degenera y corta
    menos a esa pieza que antes. Devuelve el número de cortadores aplicados."""
    o = bpy.data.objects.get(target)
    if o is None or not cutters:
        return None
    _bake(o)
    _solidify_sheet(o)
    # el objetivo también debe ser un único sólido sin autointersecciones para el solver MANIFOLD
    bm = bmesh.new()
    bm.from_mesh(o.data)
    closed_t = all(e.is_manifold for e in bm.edges)
    bm.free()
    if closed_t:
        _union_islands(o)
    done = 0
    failed = []
    # primera vuelta solo con MANIFOLD; los que fallan se reintentan al final con el solver exacto (si las mallas
    # son pequeñas), porque su resultado puede dejar de ser «manifold» y entonces MANIFOLD ya no recorta nada más
    queue = [(c, 0) for c in cutters]
    while queue:
        c, rnd = queue.pop(0)
        oc = bpy.data.objects.get(c)
        if oc is None:
            continue
        tc = _tree(oc)
        t0 = _tree(o)
        if tc is None or t0 is None:
            continue
        before = len(t0.overlap(tc))
        if not before:
            continue
        cut, closed = _cutter_object([c], grow)
        if not closed:
            me = cut.data
            bpy.data.objects.remove(cut, do_unlink=True)
            bpy.data.meshes.remove(me)
            _log(f"    {c}: abierto, se omite")
            continue
        _log(f"    {c}")
        ok = False
        # primero MANIFOLD (rápido); si no mejora (p. ej. cortadores formados por sólidos que se solapan entre sí),
        # el solver exacto con autointersección, solo para cortadores de tamaño moderado
        # MANIFOLD primero; el exacto (autointersección) solo con mallas pequeñas y cerradas: con mallas grandes o
        # abiertas puede cerrar Blender
        small = len(cut.data.polygons) <= EXACT_MAX_FACES and len(o.data.polygons) <= EXACT_MAX_FACES
        for solver in (("MANIFOLD",) if rnd == 0 else (("MANIFOLD", "EXACT") if small else ("MANIFOLD",))):
            _log(f"      {solver}")
            mod = o.modifiers.new("_carve", "BOOLEAN")
            mod.operation = "DIFFERENCE"
            mod.solver = solver
            mod.object = cut
            if solver == "EXACT":
                mod.use_self = True
            bpy.context.view_layer.update()
            dg = bpy.context.evaluated_depsgraph_get()
            new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
            o.modifiers.remove(mod)
            if len(new.polygons) < 0.3 * max(1, len(o.data.polygons)):
                _log(f"      degenerado ({len(new.polygons)} caras)")
                bpy.data.meshes.remove(new)
                continue
            old = o.data
            o.data = new
            bpy.context.view_layer.update()
            t1 = _tree(o)
            after = len(t1.overlap(tc)) if t1 else before
            if after >= before:
                _log(f"      no mejora ({before} -> {after})")
                o.data = old
                bpy.data.meshes.remove(new)
                continue
            new.name = old.name
            if old.users == 0:
                bpy.data.meshes.remove(old)
            ok = True
            break
        me = cut.data
        bpy.data.objects.remove(cut, do_unlink=True)
        bpy.data.meshes.remove(me)
        if ok:
            done += 1
            _log("      aceptado")
        elif rnd == 0:
            queue.append((c, 1))
        else:
            failed.append(c)
    if failed:
        _log(f"  sin recortar: {failed}")
    return done


UP = Vector((0.0123, 0.0217, 1.0)).normalized()


def _inside(tree, p):
    n, o = 0, p.copy()
    for _ in range(64):
        hit = tree.ray_cast(o, UP)[0]
        if hit is None:
            break
        n += 1
        o = hit + UP * 1e-5
    return n % 2 == 1


def squash(target, partners, gap=GAP, reach=0.03, rounds=2):
    """Comprime una pieza blanda (junta de goma, espuma): sus vértices que quedan dentro de una pieza vecina se
    llevan a la superficie de esta, más una holgura `gap`. Las vecinas cerradas se prueban por paridad de rayos;
    las láminas abiertas, por el lado de su normal y hasta `reach` de profundidad. Devuelve los vértices movidos."""
    import interferencias as I
    o = bpy.data.objects.get(target)
    if o is None or not partners:
        return None
    dg = bpy.context.evaluated_depsgraph_get()
    if len(o.modifiers):
        new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        for m in list(o.modifiers):
            o.modifiers.remove(m)
        old = o.data
        new.name = old.name
        o.data = new
        if old.users == 0:
            bpy.data.meshes.remove(old)
    elif o.data.users > 1:
        o.data = o.data.copy()
    trees = []
    for n in partners:
        vs, tris = _world(bpy.data.objects[n], dg)
        if tris:
            trees.append((BVHTree.FromPolygons(vs, tris, epsilon=0.0), I._closed(tris)))
    mw = o.matrix_world
    inv = mw.inverted()
    moved = 0
    for _ in range(rounds):
        changed = 0
        for v in o.data.vertices:
            p = mw @ v.co
            for tree, closed in trees:
                loc, nor, _i, d = tree.find_nearest(p, reach)
                if loc is None:
                    continue
                if closed:
                    if not _inside(tree, p):
                        continue
                elif (p - loc).dot(nor) >= 0:
                    continue
                p = loc + nor * gap
                changed += 1
            v.co = inv @ p
        moved += changed
        if not changed:
            break
    o.data.update()
    return moved


# ---------------------------------------------------------------------------
# pasada 1: recortes
# ---------------------------------------------------------------------------
# ruta opcional de un registro de progreso (diagnóstico de booleanos lentos o que cierran Blender); también se
# puede activar con la variable de entorno CT_MONTAJE_LOG, que sobrevive a la recarga de los módulos
LOG_FILE = os.environ.get("CT_MONTAJE_LOG")
EXACT_MAX_FACES = 4000   # el solver exacto (respaldo) solo con mallas pequeñas: con mallas grandes puede colgarse


def _log(msg):
    if LOG_FILE:
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(msg + "\n")
            fh.flush()


def carve_all(sc=None, only=None):
    sc = sc or Scene()
    log = {}
    for pat, mode, _why in CARVE:
        rx = re.compile(pat)
        for name in sorted(k for k in sc.d if rx.search(k)):
            if only and not re.search(only, name):
                continue
            _log(f"objetivo {name}")
            parts = sc.partners(name, include_intended=(mode == "comprimir"))
            if not parts:
                continue
            cutters, below = parts, []
            if mode == "suelo":
                top = sc.d[name][4].z
                cz = (sc.d[name][3].z + top) / 2
                cutters = [p for p in parts if (sc.d[p][3].z + sc.d[p][4].z) / 2 >= cz]
                below = [p for p in parts if p not in cutters]
            _log(f"  cortadores {cutters}")
            if mode == "comprimir":
                n = squash(name, cutters)
                sc.refresh(name)
                log[name] = {"comprimida_por": len(cutters), "vertices": n}
                _log(f"  hecho {n}")
                continue
            n = carve(name, cutters) if cutters else None
            if n is not None:
                sc.refresh(name)
            for b in below:
                _log(f"  debajo {b}")
                if trim_below(b, name, sc):
                    sc.refresh(b)
            _log(f"  hecho {n}")
            log[name] = {"cortadores": len(cutters), "aplicados": n, "recortadas_debajo": below}
    return log


# ---------------------------------------------------------------------------
# pasada 2: recolocaciones
# ---------------------------------------------------------------------------
def load_moves():
    if not os.path.exists(MOVES_FILE):
        return {}
    with open(MOVES_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def apply_moves(moves=None):
    """Desplaza la malla de cada objeto de la tabla (en coordenadas de mundo) sin tocar su origen ni su
    jerarquía, de modo que la explosión y los pivotes no cambian."""
    moves = load_moves() if moves is None else moves
    n = 0
    for name, rec in moves.items():
        o = bpy.data.objects.get(name)
        if o is None or o.type != "MESH":
            continue
        d = Vector(rec["d"])
        if o.data.users > 1:
            o.data = o.data.copy()
        inv = o.matrix_world.to_3x3().inverted()
        dl = inv @ d
        for v in o.data.vertices:
            v.co += dl
        o.data.update()
        n += 1
    return n


# Jerarquía de recolocación: cuando dos piezas se atraviesan se mueve la de rango mayor (la más «accesoria»);
# a igualdad de rango, la de menor tamaño. Las de rango 0 no se mueven nunca: estructura, carrocería y todo lo
# exterior visible, puertas, vidrios, ruedas, frenos, suspensión, dirección, motores, batería, caja de carga,
# asientos, volante, pantallas, cámaras y piezas grandes del habitáculo (sus posiciones proceden de cotas, planos o
# del punto H). Las placas y los interiores de la v4 tampoco: ya se ajustan a su carcasa en `build_v4`.
RANK2 = re.compile(r"Harness|Hose|_Lines?(_|$)|Cable|Bundle|Bracket|Sensor|Fitting|Duct|Pipe|Tube|Grommet|"
                   r"Connector|Jumper|Strap|Shunt|Pyro|Fuse|Relay|Clip|Wiring")
RANK0 = re.compile(r"^(BODY_|DOOR_|GLS_|WHL_|SUS_|BRK_|DU_|BAT_|STR_|LGT_|CARGO_|CAM_|SW_|EXT_|"
                   r"INT_(Seat|SteeringWheel|Display|IP_(TopPad|Lower|Glovebox|Mid|Quarter)|Console_(Body|Armrest)|"
                   r"DoorTrim|Trim_|Headliner|Carpet|FloorMat|Airbag|Door_Beltline|Steering_Column))|"
                   r"_PCB$|Internals")
# Solo se recolocan automáticamente piezas ocultas: módulos y conducciones de alta y baja tensión, térmica,
# chasis y electrónica, y los módulos que quedan tras el salpicadero o los guarnecidos.
MOVABLE = re.compile(r"^(HV_|LV_|THM_|CHS_|ELE_)|^INT_(HVAC|Car_Computer|Restraint|Cabin_Radar|TCU|Amplifier|"
                     r"Subwoofer|Speakers?_|DoorSpeaker_.*_Driver|Floor_Duct|Demist|Airwave_Duct|Footwell_Duct)")
STEPS = (0.002, 0.004, 0.006, 0.009, 0.012, 0.016, 0.020, 0.025, 0.030)
MAX_MOVE = {1: 0.015, 2: 0.030}


def rank(name):
    if not MOVABLE.search(name) and not (name.startswith("EXT_") and RANK2.search(name)):
        return 0
    if RANK0.search(name) and not (name.startswith("EXT_") and RANK2.search(name)):
        return 0
    if RANK2.search(name):
        return 2
    return 1


def _conflicts(sc, name, vs, tris, others):
    """Pares de triángulos que cortan `others` con la malla (vs, tris) del objeto `name` en otra posición."""
    import interferencias as I
    t = BVHTree.FromPolygons(vs, tris, epsilon=0.0)
    out = {}
    for k in others:
        if I.intended(name, k, 0.0):
            continue
        n = len(t.overlap(sc.d[k][0]))
        if n:
            out[k] = n
    return out


def resolver(min_depth_mm=1.5, max_moves=400, write=True):
    """Calcula la tabla de recolocaciones a partir de las interferencias actuales y la aplica a la escena.

    Para cada pieza a mover (la de mayor rango de cada pareja), prueba desplazamientos de 2 a 50 mm en los seis
    ejes y en la dirección que la aleja de los cruces, y se queda con el menor que elimina sus cruces con piezas
    de rango igual o menor sin crear cruces nuevos con ninguna otra pieza. Si ninguno los elimina del todo,
    acepta el menor que los reduce a menos de un tercio sin crear cruces nuevos. Devuelve la tabla y la escribe en
    `montaje_desplazamientos.json` (acumulando la anterior)."""
    import interferencias as I
    sc = Scene()
    pairs = [x for x in I.run() if x["profundidad_mm"] > min_depth_mm and not x["intencionado"]]
    movers = {}
    for x in pairs:
        a, b = x["a"], x["b"]
        ra, rb = rank(a), rank(b)
        if ra == 0 and rb == 0:
            continue
        if ra != rb:
            m = a if ra > rb else b
        else:
            va = (sc.d[a][4] - sc.d[a][3]).length
            vb = (sc.d[b][4] - sc.d[b][3]).length
            m = a if va <= vb else b
        movers.setdefault(m, []).append((x["profundidad_mm"], a if m == b else b, Vector(x["centro"])))
    order = sorted(movers, key=lambda m: -max(d for d, _, _ in movers[m]))[:max_moves]
    table = load_moves()
    done = {}
    for m in order:
        if m not in sc.d:
            continue
        _, vs, tris, mn, mx = sc.d[m]
        pad = 0.06
        near = [k for k, (_, _, _, a, b) in sc.d.items() if k != m and not (
            a.x > mx.x + pad or b.x < mn.x - pad or a.y > mx.y + pad or b.y < mn.y - pad or
            a.z > mx.z + pad or b.z < mn.z - pad)]
        base = _conflicts(sc, m, vs, tris, near)
        rm = rank(m)
        must = {k for k in base if rank(k) <= rm}
        if not must:
            continue
        cen = (mn + mx) / 2
        away = Vector()
        for _, _, c in movers[m]:
            away += (cen - c)
        dirs = [Vector(v) for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
        if away.length > 1e-6:
            dirs.insert(0, away.normalized())
        best = None
        smax = MAX_MOVE[rm]
        for d in dirs:
            # se avanza en esta dirección mientras no aparezca ningún cruce nuevo en el recorrido: una pieza no
            # puede «saltar» a través de una pared
            for s in STEPS:
                if s > smax + 1e-9 or (best and best[0][0] == 0 and s >= best[0][1]):
                    break
                sh = d * s
                c2 = _conflicts(sc, m, [p + sh for p in vs], tris, near)
                if any(k not in base for k in c2) or any(c2.get(k, 0) > base[k] for k in base):
                    break
                left = sum(c2.get(k, 0) for k in must)
                score = (left, s)
                if best is None or score < best[0]:
                    best = (score, sh)
                if left == 0:
                    break
        if best is None:
            continue
        (left, s), sh = best
        if left and left > sum(base[k] for k in must) / 3:
            continue
        apply_moves({m: {"d": list(sh)}})
        sc.refresh(m)
        prev = Vector(table.get(m, {}).get("d", (0, 0, 0)))
        tot = prev + sh
        table[m] = {"d": [round(tot.x, 4), round(tot.y, 4), round(tot.z, 4)],
                    "motivo": "deja de atravesar " + ", ".join(sorted(must))}
        done[m] = [round(sh.x * 1000, 1), round(sh.y * 1000, 1), round(sh.z * 1000, 1), left]
    if write:
        with open(MOVES_FILE, "w", encoding="utf-8") as fh:
            json.dump(dict(sorted(table.items())), fh, ensure_ascii=False, indent=1)
    return done


def _grid(radius, step):
    n = int(round(radius / step))
    pts = [Vector((i * step, j * step, k * step)) for i in range(-n, n + 1) for j in range(-n, n + 1)
           for k in range(-n, n + 1)]
    pts = [p for p in pts if 0 < p.length <= radius + 1e-9]
    pts.sort(key=lambda p: (round(p.length, 6), -p.z))
    return pts


def place_free(sc, m, radius=0.05, step=0.01, ignore=None):
    """Menor desplazamiento (rejilla 3D de paso `step`, hasta `radius`) con el que la pieza `m` no corta a
    ninguna otra (salvo las penetraciones intencionadas y las que casan con la expresión `ignore`).
    Devuelve el vector o None."""
    _, vs, tris, mn, mx = sc.d[m]
    pad = radius + 0.01
    near = [k for k, (_, _, _, a, b) in sc.d.items() if k != m and not (
        a.x > mx.x + pad or b.x < mn.x - pad or a.y > mx.y + pad or b.y < mn.y - pad or
        a.z > mx.z + pad or b.z < mn.z - pad) and not (ignore and re.search(ignore, k))]
    for sh in _grid(radius, step):
        if not _conflicts(sc, m, [p + sh for p in vs], tris, near):
            return sh
    return None


def placer(min_depth_mm=1.5, radius=0.05, step=0.01, write=True):
    """Segunda estrategia de recolocación, para módulos y accesorios ocultos (rango >= 1) que atraviesan piezas de
    rango menor: busca la posición libre más cercana en una rejilla 3D (`place_free`). Acumula en la tabla."""
    import interferencias as I
    sc = Scene()
    pairs = [x for x in I.run() if x["profundidad_mm"] > min_depth_mm and not x["intencionado"]]
    movers = {}
    for x in pairs:
        a, b = x["a"], x["b"]
        ra, rb = rank(a), rank(b)
        if ra == rb == 0:
            continue
        m = a if (ra, -(sc.d[a][4] - sc.d[a][3]).length) > (rb, -(sc.d[b][4] - sc.d[b][3]).length) else b
        movers[m] = max(movers.get(m, 0), x["profundidad_mm"])
    table = load_moves()
    done = {}
    for m in sorted(movers, key=lambda k: -movers[k]):
        if m not in sc.d or (sc.d[m][4] - sc.d[m][3]).length > 0.9:
            continue          # piezas largas (mazos troncales): se tienden a mano
        sh = place_free(sc, m, radius, step)
        if sh is None:
            continue
        apply_moves({m: {"d": list(sh)}})
        sc.refresh(m)
        prev = Vector(table.get(m, {}).get("d", (0, 0, 0)))
        tot = prev + sh
        table[m] = {"d": [round(tot.x, 4), round(tot.y, 4), round(tot.z, 4)],
                    "motivo": "posición libre más cercana (rejilla 3D)"}
        done[m] = [round(sh.x * 1000), round(sh.y * 1000), round(sh.z * 1000)]
    if write:
        with open(MOVES_FILE, "w", encoding="utf-8") as fh:
            json.dump(dict(sorted(table.items())), fh, ensure_ascii=False, indent=1)
    return done


# Alojamientos por caja: piezas que en la realidad son carcasas huecas modeladas como sólidos (la consola central),
# a las que se quita un volumen prismático por donde no se ven, para alojar lo que va dentro. (objeto, mínimo,
# máximo, motivo); coordenadas de mundo.
POCKETS = [
    ("INT_Console_Body", (-0.108, -0.105, 0.47), (0.108, 0.905, 0.562),
     "hueco inferior de la consola (carcasa hueca) para la base y los raíles del suelo"),
]


def pockets():
    out = {}
    for name, mn, mx, _why in POCKETS:
        o = bpy.data.objects.get(name)
        if o is None:
            continue
        _bake(o)
        box = _box_object(Vector(mn), Vector(mx))
        mod = o.modifiers.new("_pocket", "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.solver = "MANIFOLD"
        mod.object = box
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        o.modifiers.remove(mod)
        me = box.data
        bpy.data.objects.remove(box, do_unlink=True)
        bpy.data.meshes.remove(me)
        if len(new.polygons) < 0.3 * max(1, len(o.data.polygons)):
            bpy.data.meshes.remove(new)
            out[name] = "descartado"
            continue
        old = o.data
        new.name = old.name
        o.data = new
        if old.users == 0:
            bpy.data.meshes.remove(old)
        out[name] = len(new.polygons)
    return out


def build_all(M=None):
    bpy.context.view_layer.update()
    out = {}
    out["huecos"] = pockets()
    out["recortes"] = carve_all()
    out["desplazados"] = apply_moves()
    return out
