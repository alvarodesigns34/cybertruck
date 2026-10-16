"""Validación dimensional y de silueta del modelo frente a la ficha oficial y los perfiles medidos.

Se evalúa la geometría final (con modificadores aplicados) en estado ensamblado.
"""

import json
import os
import statistics
import bpy
import numpy as np
import ct_specs as S
import build_explode as E

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "reference_data", "official_side_profile.json")


def world_vertices(filter_fn=None):
    dg = bpy.context.evaluated_depsgraph_get()
    chunks = []
    for o in E.vehicle_objects():
        if o.type != "MESH" or (filter_fn and not filter_fn(o)):
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        n = len(me.vertices)
        if n:
            co = np.empty(n * 3, dtype=np.float64)
            me.vertices.foreach_get("co", co)
            co = co.reshape(-1, 3)
            m = np.array(ev.matrix_world)
            co = co @ m[:3, :3].T + m[:3, 3]
            chunks.append(co)
        ev.to_mesh_clear()
    return np.concatenate(chunks) if chunks else np.zeros((0, 3))


def _is_mirror(o):
    return "Mirror" in o.name and o.name.startswith(("EXT_", "GLS_"))


def _is_wheelish(o):
    return o.name.startswith(("WHL_", "BRK_", "SUS_", "STR_", "DU_Halfshaft"))


def dims():
    E.set_explode(0.0)
    allv = world_vertices()
    nomirror = world_vertices(lambda o: not _is_mirror(o))
    body = world_vertices(lambda o: not _is_mirror(o) and not _is_wheelish(o))
    fl = bpy.data.objects["WHEEL_FL"].matrix_world.translation
    rl = bpy.data.objects["WHEEL_RL"].matrix_world.translation
    fr = bpy.data.objects["WHEEL_FR"].matrix_world.translation
    out = {
        "longitud": (float(allv[:, 1].max() - allv[:, 1].min()), S.LENGTH),
        "anchura_sin_espejos": (float(nomirror[:, 0].max() - nomirror[:, 0].min()), S.WIDTH_BODY),
        "anchura_con_espejos": (float(allv[:, 0].max() - allv[:, 0].min()), S.WIDTH_MIRRORS),
        "altura_medium": (float(allv[:, 2].max() - min(0.0, allv[:, 2].min())), S.HEIGHT_MEDIUM),
        "batalla": (float(fl.y - rl.y), S.WHEELBASE),
        "via": (float(fr.x - fl.x), S.TRACK),
        "voladizo_delantero": (float(allv[:, 1].max() - fl.y), S.OVERHANG_F),
        "voladizo_trasero": (float(rl.y - allv[:, 1].min()), S.OVERHANG_R),
        "altura_libre_medium": (float(body[:, 2].min()), S.GROUND_CLEAR_MEDIUM),
        "diametro_neumatico": (2 * float(world_vertices(lambda o: o.name == "WHL_FL_Tire")[:, 2].max()
                                         - fl.z), 2 * S.TIRE_RADIUS),
        "z_minimo_neumatico": (float(world_vertices(lambda o: o.name.endswith("_Tire"))[:, 2].min()), 0.0),
    }
    return {k: {"modelo": round(v[0], 4), "oficial": round(v[1], 4), "desviacion_mm": round((v[0] - v[1]) * 1000, 1)}
            for k, v in out.items()}


def _profile(verts, axis_s, axis_v, s_vals, band, mode):
    res = []
    s = verts[:, axis_s]
    for sv in s_vals:
        sel = verts[np.abs(s - sv) < band]
        if len(sel) == 0:
            res.append(None)
            continue
        vals = sel[:, axis_v]
        res.append(float(vals.max() if mode == "max" else vals.min()))
    return res


def bvh(filter_fn=None):
    """Árbol BVH con todos los triángulos evaluados (coordenadas de mundo)."""
    from mathutils.bvhtree import BVHTree
    dg = bpy.context.evaluated_depsgraph_get()
    verts, polys = [], []
    for o in E.vehicle_objects():
        if o.type != "MESH" or (filter_fn and not filter_fn(o)):
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        base = len(verts)
        verts.extend(mw @ v.co for v in me.vertices)
        polys.extend([base + i for i in p.vertices] for p in me.polygons)
        ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys)


def _rays(tree, origins, direction):
    from mathutils import Vector
    hits = []
    d = Vector(direction)
    for o in origins:
        loc, _, _, _ = tree.ray_cast(Vector(o), d, 20.0)
        hits.append(loc)
    return [h for h in hits if h is not None]


def silhouette():
    """Compara los perfiles del modelo (trazado de rayos) con los perfiles oficiales medidos."""
    E.set_explode(0.0)
    ref = json.load(open(REF, encoding="utf-8"))
    t_all = bvh(lambda o: not _is_mirror(o) and not o.name.startswith(("EXT_Wiper", "CHS_Tow")))
    t_body = bvh(lambda o: not _is_mirror(o) and not _is_wheelish(o))
    xs = [x / 20.0 for x in range(-21, 22)]
    zs = [0.20 + z * 0.02 for z in range(0, 85)]
    report = {}

    def stats(name, ref_pts, model_vals, skip=None):
        devs = []
        for (a, b), m in zip(ref_pts, model_vals):
            if m is None or (skip and skip(a, b)):
                continue
            devs.append(abs(m - b))
        if not devs:
            return
        devs.sort()
        report[name] = {"muestras": len(devs), "media_mm": round(1000 * statistics.mean(devs), 1),
                        "p95_mm": round(1000 * devs[int(0.95 * (len(devs) - 1))], 1),
                        "max_mm": round(1000 * devs[-1], 1)}

    def top(y):
        h = _rays(t_all, [(x, y, 5.0) for x in xs], (0, 0, -1))
        return max(p.z for p in h) if h else None

    def bottom(y):
        h = _rays(t_body, [(x, y, -2.0) for x in xs], (0, 0, 1))
        return min(p.z for p in h) if h else None

    def front(z):
        h = _rays(t_all, [(x, 6.0, z) for x in xs], (0, -1, 0))
        return max(p.y for p in h) if h else None

    def rear(z):
        h = _rays(t_all, [(x, -6.0, z) for x in xs], (0, 1, 0))
        return min(p.y for p in h) if h else None

    def plan(y):
        h = _rays(t_all, [(6.0, y, z) for z in zs], (-1, 0, 0))
        return max(p.x for p in h) if h else None

    ends = lambda y, v: y > 2.655 or y < -2.975   # muestras de borde (punta delantera y trasera)
    stats("perfil_superior", ref["top"], [top(p[0]) for p in ref["top"]], skip=ends)
    stats("perfil_inferior", ref["bot"], [bottom(p[0]) for p in ref["bot"]])
    stats("perfil_frontal", [(p[1], p[0]) for p in ref["front"]], [front(p[1]) for p in ref["front"]])
    stats("perfil_trasero", [(p[1], p[0]) for p in ref["rear"]], [rear(p[1]) for p in ref["rear"]],
          skip=lambda z, y: z < 0.30)
    stats("planta_semianchura", ref["plan_half_width"], [plan(p[0]) for p in ref["plan_half_width"]], skip=ends)
    return report


def _unused_vertex_silhouette():
    ref = json.load(open(REF, encoding="utf-8"))
    all_nomirror = world_vertices(lambda o: not _is_mirror(o) and not o.name.startswith("EXT_Wiper"))
    body = world_vertices(lambda o: not _is_mirror(o) and not _is_wheelish(o))
    report = {}

    def stats(name, ref_pts, model_vals, skip=None):
        devs = []
        for (a, b), m in zip(ref_pts, model_vals):
            if m is None or (skip and skip(a, b)):
                continue
            devs.append(abs(m - b))
        if not devs:
            return
        devs.sort()
        report[name] = {"muestras": len(devs), "media_mm": round(1000 * statistics.mean(devs), 1),
                        "p95_mm": round(1000 * devs[int(0.95 * (len(devs) - 1))], 1),
                        "max_mm": round(1000 * devs[-1], 1)}

    top = ref["top"]
    stats("perfil_superior", top, _profile(all_nomirror, 1, 2, [p[0] for p in top], 0.006, "max"))
    bot = ref["bot"]
    # el perfil inferior excluye las ruedas (la referencia se tomó fuera de ellas)
    stats("perfil_inferior", bot, _profile(body, 1, 2, [p[0] for p in bot], 0.006, "min"))
    fr = ref["front"]
    stats("perfil_frontal", fr, _profile(all_nomirror, 2, 1, [p[1] for p in fr], 0.004, "max"))
    rr = ref["rear"]
    stats("perfil_trasero", rr, _profile(all_nomirror, 2, 1, [p[1] for p in rr], 0.004, "min"),
          skip=lambda a, b: b < 0.30)
    pl = ref["plan_half_width"]
    absx = all_nomirror.copy()
    absx[:, 0] = np.abs(absx[:, 0])
    stats("planta_semianchura", pl, _profile(absx, 1, 0, [p[0] for p in pl], 0.006, "max"))
    return report


def run():
    return {"dimensiones": dims(), "silueta": silhouette()}
