"""Detección de interferencias de ensamblaje: piezas cuyas superficies se atraviesan en el vehículo ensamblado.

Para cada pareja de objetos de malla cuyas cajas se solapan, se cruzan sus árboles BVH (geometría evaluada,
coordenadas de mundo, explode = 0) y se cuentan los pares de triángulos que se cortan. Una pieza contenida
entera dentro de otra (un estátor dentro de su carcasa) no se cuenta: solo los cruces de superficie, que son
lo que se ve como «piezas que se atraviesan».

Medidas por pareja:
  * `pares`: pares de triángulos que se cortan.
  * `extension_mm`: diagonal de la caja que envuelve la zona de cruce (tamaño visible del defecto).

Uso en Blender:  import interferencias; r = interferencias.run(min_ext_mm=5)
"""

import bpy
from mathutils import Vector, geometry
from mathutils.bvhtree import BVHTree
import build_explode as E


def _data(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    out = {}
    for o in objs:
        if o.type != "MESH" or o.hide_render:
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        vs = [mw @ v.co for v in me.vertices]
        tris = []
        me.calc_loop_triangles()
        for t in me.loop_triangles:
            tris.append(tuple(t.vertices))
        ev.to_mesh_clear()
        if not tris:
            continue
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        full = BVHTree.FromPolygons(vs, tris, epsilon=0.0)
        vis = _visible(vs, tris)
        surf = full if len(vis) == len(tris) else BVHTree.FromPolygons(vs, [tris[i] for i in vis], epsilon=0.0)
        out[o.name] = (surf, vs, tris, mn, mx, full, [tris[i] for i in vis])
    return out


# Penetraciones intencionadas: en el modelo las piezas son sólidos sin taladros, así que un tornillo, un eje o una
# varilla que en la realidad pasa por un agujero aparece aquí como cruce. (patrón A, patrón B, profundidad máxima
# en mm o None, motivo). El orden de A y B es indiferente.
import re as _re
INTENDED = [
    (r"Fasteners|Bolts|Rivets|Clips|_Nuts|Studs|LugNuts|Plugs|Locating_Pins|Webguides|Hub_Bolt", r".", 15.0,
     "tornillo, remache o grapa que entra en la pieza que fija"),
    (r"BAT_Block_(\d)", r"BAT_Block_(\d)", None, "celdas embebidas en la espuma estructural y los refrigeradores"),
    (r"Rotor_Shaft|Output_Shaft|DU_Halfshaft|Phase_Busbars", r"Gearbox|Differential|Motor_|Housing|Inverter",
     None, "eje o barra que atraviesa la pared de su carcasa (por un retén o un pasamuros)"),
    (r"Headrest", r"_Back(_Foam)?$", None, "varillas del reposacabezas en sus guías del respaldo"),
    (r"Cupholder", r"Console_Body|Console_Armrest", None, "portavasos encastrado en la consola"),
    (r"Valve_TPMS", r"Cover_Core|_Rim$", None, "vástago de la válvula por su taladro de la llanta y del tapacubos"),
    (r"LV_Harness|HV_Cables|HV_Harness|Coax", r"^BODY_(Firewall|Cabin_Floor|Cabin_RearWall|Dash|RearWall)", 15.0,
     "mazo que atraviesa el mamparo o el suelo por su pasacables"),
    (r"BAT_Main_Busbars|HV_Cables", r"BAT_HV_Header", None, "barras y cables que entran en el cabezal HV por sus pasamuros"),
    (r"BAT_Coolant_Manifolds", r"BAT_Internal_Beams", None, "colectores de refrigerante por los pasos de las vigas interiores"),
    (r"DU_[FR]_OilPump_Filter", r"DU_[FR]_Gearbox", 25.0, "bomba de aceite y filtro roscados en la carcasa de la reductora"),
    (r"DU_[FR]_Mounts", r"DU_[FR]_Gearbox|DU_[FR]_Motor", 12.0, "casquillos de los soportes encajados en los ojales de la carcasa"),
    (r"IP_CrossCar_Beam", r"IP_Beam_Bracket", None, "extremo de la viga del salpicadero alojado en su soporte"),
    (r"DU_R_Rotor_Shaft_([LR])", r"DU_R_Gear_Train_([LR])", None, "eje del rotor estriado en el piñón de entrada"),
    (r"^SUS_(\w\w)_Hub$", r"^(?:BRK|WHL)_(\w\w)_(?:Rotor|Rim)$", None,
     "espárragos y centrador del buje por los taladros de la campana del disco y de la llanta"),
]


def intended(a, b, depth):
    for pa, pb, dmax, why in INTENDED:
        for x, y in ((a, b), (b, a)):
            ma, mb = _re.search(pa, x), _re.search(pb, y)
            if ma and mb and (dmax is None or depth <= dmax):
                if ma.groups() and mb.groups() and ma.groups() != mb.groups():
                    continue
                return why
    return None


def _edge_tri(p, q, a, b, c):
    d = q - p
    ln = d.length
    if ln < 1e-9:
        return None
    h = geometry.intersect_ray_tri(a, b, c, d / ln, p, True)
    if h is not None and (h - p).length <= ln:
        return h
    return None


def _seg(va, ta, vb, tb):
    """Puntos del segmento de corte entre dos triángulos (aristas de cada uno contra el otro)."""
    A = [va[i] for i in ta]
    B = [vb[i] for i in tb]
    out = []
    for P, Q in ((A, B), (B, A)):
        for i in range(3):
            h = _edge_tri(P[i], P[(i + 1) % 3], Q[0], Q[1], Q[2])
            if h is not None:
                out.append(h)
    return out


def run(min_ext_mm=0.0, names=None, ignore_pairs=None):
    """Devuelve la lista de interferencias ordenada por extensión (mayor primero)."""
    E.set_explode(0.0)
    bpy.context.view_layer.update()
    objs = [o for o in E.vehicle_objects() if names is None or o.name in names]
    D = _data(objs)
    CLOSED.clear()
    for k, v in D.items():
        CLOSED[k] = _closed(v[2])
    keys = sorted(D)
    res = []
    # barrido por X para no comparar todas las parejas
    order = sorted(keys, key=lambda k: D[k][3].x)
    for i, a in enumerate(order):
        ta, va, _fa, mna, mxa, _ta, fa = D[a]
        for b in order[i + 1:]:
            tb, vb, _fb, mnb, mxb, _tb, fb = D[b]
            if mnb.x > mxa.x:
                break
            if mnb.y > mxa.y or mxb.y < mna.y or mnb.z > mxa.z or mxb.z < mna.z:
                continue
            if ignore_pairs and ((a, b) in ignore_pairs or (b, a) in ignore_pairs):
                continue
            hits = ta.overlap(tb)
            if not hits:
                continue
            step = max(1, len(hits) // 600)
            pts = []
            for ia, ib in hits[::step]:
                pts += _seg(va, fa[ia], vb, fb[ib])
            if not pts:
                continue
            lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
            hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
            ext = (hi - lo).length * 1000
            if ext < min_ext_mm:
                continue
            c = (lo + hi) / 2
            # profundidad medida cerca de la zona de cruce (no en toda la pieza: una pieza contenida en otra que
            # asoma un poco no debe contar como penetración profunda)
            zl, zh = lo - Vector((0.03, 0.03, 0.03)), hi + Vector((0.03, 0.03, 0.03))
            dep = max(_depth(va, D[b], zl, zh) if CLOSED.get(b) else 0.0,
                      _depth(vb, D[a], zl, zh) if CLOSED.get(a) else 0.0)
            res.append({"a": a, "b": b, "pares": len(hits), "extension_mm": round(ext, 1),
                        "profundidad_mm": round(dep * 1000, 1),
                        "centro": [round(c.x, 3), round(c.y, 3), round(c.z, 3)],
                        "intencionado": intended(a, b, dep * 1000)})
    res.sort(key=lambda r: -r["profundidad_mm"])
    return res


CLOSED = {}
UP = Vector((0.0123, 0.0217, 1.0)).normalized()     # dirección de prueba ligeramente inclinada (evita aristas)


def _inside(tree, p):
    """Paridad de cortes de un rayo: impar = el punto está dentro de la malla cerrada."""
    n = 0
    o = p.copy()
    for _ in range(64):
        loc, nor, idx, d = tree.ray_cast(o, UP)
        if loc is None:
            break
        n += 1
        o = loc + UP * 1e-5
    return n % 2 == 1


def _depth(vs, other, mn, mx, cap=500):
    """Profundidad máxima a la que vértices de un objeto quedan dentro de otro objeto cerrado."""
    tree = other[5]
    cand = [p for p in vs if mn.x <= p.x <= mx.x and mn.y <= p.y <= mx.y and mn.z <= p.z <= mx.z]
    if len(cand) > cap:
        st = len(cand) // cap + 1
        cand = cand[::st]
    best = 0.0
    for p in cand:
        loc, nor, _, d = tree.find_nearest(p)
        if loc is None or d <= best or d < 0.0005:
            continue
        if _inside(tree, p):
            best = d
    return best


def _visible(vs, tris, max_islands=800):
    """Triángulos de la superficie exterior de un objeto. Muchas piezas se modelan como varios sólidos cerrados
    solapados (lóbulos, nervios, tapas); las caras de un sólido que quedan dentro de otro sólido del mismo objeto
    no se ven nunca, así que no cuentan como cruce. Devuelve la lista de índices de triángulos visibles."""
    n = len(tris)
    parent = list(range(len(vs)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for t in tris:
        ra = find(t[0])
        for v in t[1:]:
            rb = find(v)
            if rb != ra:
                parent[rb] = ra
    isl = {}
    for i, t in enumerate(tris):
        isl.setdefault(find(t[0]), []).append(i)
    groups = list(isl.values())
    if len(groups) < 2 or len(groups) > max_islands:
        return list(range(n))
    cen = [(vs[t[0]] + vs[t[1]] + vs[t[2]]) / 3 for t in tris]
    hidden = set()
    for g in groups:
        sub = [tris[i] for i in g]
        if not _closed(sub):
            continue
        pts = [vs[j] for t in sub for j in t]
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        gs = set(g)
        cand = [i for i in range(n) if i not in gs and i not in hidden and
                mn.x < cen[i].x < mx.x and mn.y < cen[i].y < mx.y and mn.z < cen[i].z < mx.z]
        if not cand:
            continue
        tree = BVHTree.FromPolygons(vs, sub, epsilon=0.0)
        for i in cand:
            if _inside(tree, cen[i]):
                hidden.add(i)
    return [i for i in range(n) if i not in hidden]


def _closed(faces):
    edges = {}
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            k = (a, b) if a < b else (b, a)
            edges[k] = edges.get(k, 0) + 1
    return all(v == 2 for v in edges.values())
