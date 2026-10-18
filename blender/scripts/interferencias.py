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
        out[o.name] = (surf, vs, tris, mn, mx, full, [tris[i] for i in vis], _island_trees(vs, tris))
    return out


def _island_trees(vs, tris, max_islands=800):
    """Árboles BVH de cada sólido (parte suelta) de un objeto. Con varios sólidos solapados la paridad de un rayo
    contra la malla entera no indica si un punto está dentro (dos paredes solapadas suman un corte par), así que la
    prueba se hace sólido a sólido. Devuelve None si el objeto tiene una sola parte o demasiadas."""
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
    for t in tris:
        isl.setdefault(find(t[0]), []).append(t)
    if len(isl) < 2 or len(isl) > max_islands:
        return None
    out = []
    for sub in isl.values():
        pts = [vs[j] for t in sub for j in t]
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        out.append((BVHTree.FromPolygons(vs, sub, epsilon=0.0), mn, mx))
    return out


def _inside_obj(other, p):
    """¿Está `p` dentro del objeto cerrado `other`? (en alguno de sus sólidos, si tiene varios)."""
    isl = other[7]
    if isl is None:
        return _inside(other[5], p)
    for tree, mn, mx in isl:
        if mn.x <= p.x <= mx.x and mn.y <= p.y <= mx.y and mn.z <= p.z <= mx.z and _inside(tree, p):
            return True
    return False


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
    # (versión 4.2)
    (r"^DU_F_(?:Input_Gear|Intermediate_Shaft)$", r"^DU_F_(?:Intermediate_Shaft|Differential)$", 12.0,
     "dientes en toma entre piñón y rueda (dentado simplificado, sin fase entre los dientes)"),
    (r"_Rotor_Shaft(_[LR])?$", r"^DU_\w_Rotor(_[LR])?$", None,
     "eje prensado en el taladro del paquete de chapas del rotor"),
    (r"^WHL_(\w\w)_Tire$", r"^WHL_(\w\w)_Rim$", 5.0, "talones del neumático asentados en los asientos de la llanta"),
    (r"^SUS_(\w\w)_ArmBushings$", r"^SUS_(\w\w)_(?:Lower|Upper)Arm$", 10.0,
     "casquillos prensados en los ojos de los brazos"),
    (r"^SUS_[FR](\w)_ArmBushings$", r"^CHS_Subframe_[FR]$", 4.0,
     "casquillos de los brazos apretados entre las orejetas del subchasis"),
    (r"^SUS_(\w\w)_AirBag$", r"^SUS_(\w\w)_Piston$", 7.0, "extremo del fuelle neumático engastado en el pistón de rodadura"),
    (r"^SUS_(\w)\w_StabLink$", r"^SUS_(\w)_StabilizerBar$", 8.0,
     "rótula inferior de la bieleta atornillada en el ojo de la barra estabilizadora"),
    (r"^EXT_Door_(\w\w)_Latch$", r"^EXT_Door_(\w\w)_Striker$", 6.0,
     "el cerradero entra en la horquilla de la cerradura (puerta cerrada)"),
    (r"^EXT_Door_Primary_Seals_[LR]$", r"^EXT_Door_\w\w_Striker$", 6.0,
     "el cerradero atraviesa la junta primaria por su escotadura"),
    (r"^EXT_Door_Primary_Seals_[LR]$", r"^LV_Harness_Door_\w\w$", 5.0,
     "mazo de la puerta por el fuelle pasamuros junto a la junta primaria"),
    (r"^EXT_Grille_Foam_Seals$", r"^(?:EXT_Front_Bumper|BODY_Front_Bumper_Beam)$", 8.0,
     "espuma de la rejilla comprimida entre la fascia y la viga del paragolpes"),
    (r"^BRK_(R\w)_Caliper_Internals$", r"^BRK_(R\w)_Caliper$", 8.0,
     "pistón y pasadores de la pinza trasera asomando a la ranura del disco, donde empujan las pastillas"),
    (r"^EXT_Door_(\w\w)_Seals$", r"^EXT_Door_(\w\w)_GlassFrame$", 4.0,
     "junta de la puerta abrazada a la pestaña del marco del cristal"),
    (r"^EXT_Wiper_Blade$", r"^EXT_Wiper_Arm$", 6.0, "escobilla enganchada en el gancho del brazo"),
    (r"^CARGO_Tonneau_Slat_\d+$", r"^CARGO_Tonneau_Chain_[LR]$", 5.0,
     "lamas enganchadas a los eslabones de la cadena de arrastre"),
    (r"^CARGO_Tiedowns$", r"^BODY_TieDown_Nut_Plate_[LR]$|^CARGO_Bed_Tub$", 6.0,
     "anclajes de amarre encastrados en el suelo de la caja y atornillados a sus placas de tuercas"),
    (r"^INT_Seatbelt_R([LR])$", r"^INT_Trim_CPillar_Lower_([LR])$", 15.0,
     "cinta del cinturón trasero por la ranura del guarnecido del pilar C"),
    (r"^CHS_Air_Line_Bundle_", r"^CHS_AirSuspension_ValveBlock$", 10.0,
     "racores de las líneas de aire roscados en la cara del bloque de válvulas"),
    (r"^BRK_Pipes$", r"^BRK_Hydraulic_Control_Unit$", 8.0, "tubos de freno roscados en las bocas de la HCU"),
    (r"^INT_Seatbelt_Buckles$", r"^INT_SeatF_[LR]_Cushion$", 12.0,
     "pie de la hebilla delantera hundido en el costado blando del cojín, entre este y la consola"),
    (r"^INT_Rearview_Mirror$", r"^INT_Rearview_Beauty_Cover$", 8.0,
     "brazo y base del retrovisor por la abertura de su cubierta decorativa"),
    (r"^EXT_Washer_Tank$", r"^EXT_Underhood_Apron_R$", 8.0,
     "boca de llenado del depósito del lavaparabrisas por su abertura del faldón bajo el capó"),
    (r"^EXT_Washer_Hose$", r"^EXT_Frunk_Underhood_Apron_Rear$", 8.0,
     "tubo del lavaparabrisas por el pasamuros del faldón trasero bajo el capó"),
    (r"^STR_[FR]_Drive_Belts$", r"^STR_[FR]_(Motors_Internals|Rack_BallNut)$", 6.0,
     "correas abrazadas a las poleas de los motores y de la tuerca de bolas del actuador"),
    (r"^EXT_(?:Door_Primary_Seals_[LR]|Door_\w\w_Seals|Tailgate_Seal_Side_[LR]|Grille_Foam_Seals)$",
     r"^(?:EXT_Door_\w\w_Hinges|EXT_Tailgate_Hinges|EXT_Mirror_[LR]_Arm|BODY_Header_Front_Lower|DOOR_\w\w_InnerStructure|"
     r"BODY_CPillar_Inner_[LR])$", 6.0,
     "junta de goma o espuma comprimida contra la pieza que la aprieta (la compresión de montaje mueve sus vértices "
     "hasta la superficie de la vecina; queda el resto de las caras grandes)"),
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
        ta, va, _fa, mna, mxa, _ta, fa, _ia = D[a]
        for b in order[i + 1:]:
            tb, vb, _fb, mnb, mxb, _tb, fb, _ib = D[b]
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
    """Profundidad máxima a la que vértices de un objeto quedan dentro de otro objeto cerrado: distancia a la
    superficie visible del otro de los vértices que están dentro de alguno de sus sólidos."""
    tree = other[0]
    cand = [p for p in vs if mn.x <= p.x <= mx.x and mn.y <= p.y <= mx.y and mn.z <= p.z <= mx.z]
    if len(cand) > cap:
        st = len(cand) // cap + 1
        cand = cand[::st]
    best = 0.0
    for p in cand:
        loc, nor, _, d = tree.find_nearest(p)
        if loc is None or d <= best or d < 0.0005:
            continue
        if _inside_obj(other, p):
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
