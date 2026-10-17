"""Construcción de la carrocería exterior del Cybertruck (paneles independientes).

Cada panel se genera a partir de contornos 2D medidos (ver ct_specs) que se proyectan
sobre las facetas reales del vehículo:
  * cara lateral superior (inclinada 6°), cara lateral inferior y faldón,
  * plano del invernadero (inclinado 19°) para cristales, pilares y largueros de techo,
  * superficie superior (capó, parabrisas, techo, cubierta de la caja).
Las juntas entre paneles se materializan como separaciones reales de 3,5 mm.
"""

from mathutils import Vector
import ct_specs as S
import ct_lib as L

GAP = 0.0035
SIDES = ((1, "R"), (-1, "L"))     # +X = derecha (acompañante), -X = izquierda (conductor)
UP, FWD = (0, 0, 1), (0, 1, 0)

# Pendiente del plano del capó prolongado
HOOD_SLOPE = (1.283 - 1.037) / (2.640 - 1.945)


def z_hood(y):
    return 1.037 + (2.640 - y) * HOOD_SLOPE


def side_name(s):
    return "derecha" if s > 0 else "izquierda"


# ---------------------------------------------------------------------------
# Planta del frontal: facetas central, intermedia y de esquina
# ---------------------------------------------------------------------------
FACE_PLAN = [(0.0, 2.668), (0.377, 2.662), (0.622, 2.612)]
CORNER_SLOPE = (2.612 - 2.400) / (0.940 - 0.622)      # dY/dhw de la faceta de esquina


def face_y(hw):
    if hw <= 0.622:
        return S.interp(FACE_PLAN, hw)
    return 2.612 - (hw - 0.622) * CORNER_SLOPE


def corner_hw(z):
    """Semianchura donde la faceta de esquina encuentra la cara lateral a la altura z."""
    hw = S.hw_body(2.40, z)
    for _ in range(6):
        hw = S.hw_body(face_y(hw), z)
    return hw


def corner_y(z):
    return face_y(corner_hw(z))


def face_lean(z):
    """El frontal se inclina 10 mm hacia atrás desde su base hasta la arista superior."""
    return (z - S.FRONT_FACE_BOT_Z) / (1.0 - S.FRONT_FACE_BOT_Z) * 0.010


def face_top_z(hw):
    """Altura de la arista superior del frontal (bajo el chaflán del capó)."""
    return z_hood(face_y(hw)) - 0.037


def corner_top():
    """(semianchura, z) del vértice superior de la faceta de esquina."""
    h = 0.93
    for _ in range(8):
        h = corner_hw(face_top_z(h))
    return h, face_top_z(h)


# ---------------------------------------------------------------------------
# Utilidades de contorno
# ---------------------------------------------------------------------------
def offset_polyline(pts, dist, center):
    """Desplaza una polilínea abierta una distancia hacia un punto central (inglete)."""
    lines = []
    for (a, b) in zip(pts, pts[1:]):
        d = Vector((b[0] - a[0], b[1] - a[1])).normalized()
        n = Vector((-d.y, d.x))
        mid = Vector(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        if (Vector(center) - mid).dot(n) < 0:
            n = -n
        lines.append((Vector(a) + n * dist, d))
    out = [tuple(lines[0][0])]
    for (p0, d0), (p1, d1) in zip(lines, lines[1:]):
        den = d0.x * d1.y - d0.y * d1.x
        if abs(den) < 1e-9:
            out.append(tuple(p1))
            continue
        t = ((p1.x - p0.x) * d1.y - (p1.y - p0.y) * d1.x) / den
        out.append(tuple(p0 + d0 * t))
    p_last, d_last = lines[-1]
    t = (Vector(pts[-1]) - p_last).dot(d_last)
    out.append(tuple(p_last + d_last * t))
    return out


def clip_polyline_y(pts, ymin, ymax):
    """Recorta una polilínea (Y, Z) al intervalo [ymin, ymax] en Y."""
    out = []
    for a, b in zip(pts, pts[1:]):
        seg = [a, b]
        for lim, keep_above in ((ymin, True), (ymax, False)):
            pa, pb = seg
            fa = (pa[0] - lim) if keep_above else (lim - pa[0])
            fb = (pb[0] - lim) if keep_above else (lim - pb[0])
            if fa < 0 and fb < 0:
                seg = None
                break
            if fa < 0 or fb < 0:
                t = fa / (fa - fb)
                p = (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))
                seg = [p, pb] if fa < 0 else [pa, p]
        if seg:
            if not out or (abs(out[-1][0] - seg[0][0]) > 1e-7 or abs(out[-1][1] - seg[0][1]) > 1e-7):
                out.append(seg[0])
            out.append(seg[1])
    return out


def z_on_polyline(pts, y):
    for a, b in zip(pts, pts[1:]):
        lo, hi = min(a[0], b[0]), max(a[0], b[0])
        if lo - 1e-9 <= y <= hi + 1e-9 and abs(b[0] - a[0]) > 1e-9:
            t = (y - a[0]) / (b[0] - a[0])
            return a[1] + t * (b[1] - a[1])
    return None


# Contornos exteriores de las aletas (Y decreciente: delante-abajo -> detrás-abajo)
F, R = S.FLARE_F, S.FLARE_R
ARCH_F = [(2.375, 0.660), (F["y_front"] + 0.008, F["top_z"]), (F["y_rear"], F["top_z"]),
          (1.153, S.Z_ROCKER_TOP)]
ARCH_R = [(-1.160, S.Z_ROCKER_TOP), (R["y_front"], R["top_z"]), (R["y_rear"], R["top_z"]),
          (-2.360, 0.800)]
WHEEL_F = (S.Y_FRONT_AXLE, S.WHEEL_CENTER_Z)
WHEEL_R = (S.Y_REAR_AXLE, S.WHEEL_CENTER_Z)
ARCH_F_CUT = offset_polyline(ARCH_F, 0.030, WHEEL_F)     # borde de chapa oculto bajo la aleta
ARCH_R_CUT = offset_polyline(ARCH_R, 0.030, WHEEL_R)
ARCH_F_IN = offset_polyline(ARCH_F, S.FLARE_BAND, WHEEL_F)   # borde interior de la aleta
ARCH_R_IN = offset_polyline(ARCH_R, S.FLARE_BAND, WHEEL_R)

# Semianchura de las aletas en planta (medida) [R]
FLARE_PLAN = [(2.40, 0.975), (2.33, 0.985), (2.21, 1.005), (2.14, 1.029), (2.04, 1.042),
              (1.80, 1.040), (1.48, 1.037), (1.25, 1.012), (1.10, 0.990),
              (-1.12, 0.990), (-1.29, 1.004), (-1.43, 1.021), (-1.54, 1.042), (-1.80, 1.040),
              (-2.15, 1.029), (-2.21, 0.998), (-2.40, 0.985)]


def flare_hw(y):
    return S.interp(FLARE_PLAN, y)


def tg_y(z):
    """Y de la cara exterior del portón trasero a la altura z."""
    return S.interp([(p[1], p[0]) for p in reversed(S.TAILGATE_FACE)], z)


# ---------------------------------------------------------------------------
# Constructores de facetas
# ---------------------------------------------------------------------------
def map_side(y, z, s, surface):
    x = S.hw_glass(y, z) if surface == "glass" else S.hw_body(y, z)
    return (s * x, y, z)


def side_faces(mb, poly, s, surface="body", mat=0, offset=0.0):
    """Proyecta un contorno (Y, Z) sobre la superficie lateral, dividiéndolo por facetas."""
    poly = L.dedupe(poly)
    if len(poly) < 3:
        return
    pieces = [poly]
    if surface == "body":
        pieces = [p for _, p in L.split_by_levels(poly, [S.Z_ROCKER_TOP, S.Z_CREASE], axis=1)]
        yl = [S.REAR_TAPER[0][0], S.REAR_TAPER[1][0]]
        pieces = [q for p in pieces for _, q in L.split_by_levels(p, yl, axis=0)]
    for p in pieces:
        p = L.dedupe(p)
        if len(p) < 3:
            continue
        cos = []
        for (y, z) in p:
            x, yy, zz = map_side(y, z, s, surface)
            cos.append((x + s * offset, yy, zz))
        mb.face(cos, mat, want=(s, 0, 0))


def top_faces(mb, y_breaks, hw_left, hw_right, mat=0, dz=0.0, want=UP):
    """Superficie superior entre dos funciones de semianchura, troceada en los vértices del perfil."""
    ys = sorted(set(round(y, 6) for y in y_breaks), reverse=True)
    for y0, y1 in zip(ys, ys[1:]):
        a = (hw_left(y0), y0, S.z_top(y0) + dz)
        b = (hw_right(y0), y0, S.z_top(y0) + dz)
        c = (hw_right(y1), y1, S.z_top(y1) + dz)
        d = (hw_left(y1), y1, S.z_top(y1) + dz)
        mb.face([a, b, c, d], mat, want=want)


def profile_breaks(y_from, y_to, extra=()):
    ys = [y_from, y_to] + [p[0] for p in S.TOP_PROFILE if y_to < p[0] < y_from]
    ys += [p[0] for p in S.REAR_TAPER if y_to < p[0] < y_from] + list(extra)
    return sorted(set(y for y in ys if y_to <= y <= y_from), reverse=True)


def finish_panel(obj, thickness=0.0025, bevel_w=0.0018, smooth_angle=35.0, segments=2, offset=-1.0):
    L.set_smooth_by_angle(obj, smooth_angle)
    if thickness:
        L.solidify(obj, thickness, offset=offset)
    if bevel_w:
        L.bevel(obj, bevel_w, segments=segments, angle=smooth_angle)
    L.weighted_normals(obj)
    return obj


# ---------------------------------------------------------------------------
# Capó (tapa del frunk)
# ---------------------------------------------------------------------------
def hood_edge_hw(y):
    split = S.hood_side_split_y()
    if y > split:
        return S.hw_body(y, z_hood(y)) - GAP
    return S.hw_glass(y, z_hood(y)) - GAP


def build_hood(M):
    mb = L.MeshBuilder()
    y_rear = 1.945 + GAP
    hw_c = 0.9
    for _ in range(30):
        hw_c = hood_edge_hw(face_y(hw_c) - 0.028)
    front_pts = [(hw, face_y(hw) - 0.028) for hw in (0.0, 0.377, 0.622, hw_c)]
    yc = front_pts[-1][1]
    side_ys = sorted({y for y in (2.35, S.hood_side_split_y(), 2.2, 2.1, 2.0) if y_rear < y < yc},
                     reverse=True) + [y_rear]
    right = front_pts + [(hood_edge_hw(y), y) for y in side_ys]
    ring = right + [(-x, y) for (x, y) in reversed(right[1:])]
    mb.face([(x, y, z_hood(y)) for (x, y) in ring], 0, want=UP)
    # Chaflán frontal: del borde del capó a la arista superior del frontal
    for i in range(len(front_pts) - 1):
        for sg in (1, -1):
            (h0, y0), (h1, y1) = front_pts[i], front_pts[i + 1]
            quad = [(sg * h0, y0, z_hood(y0)), (sg * h1, y1, z_hood(y1)),
                    (sg * h1, face_y(h1) - face_lean(face_top_z(h1)), face_top_z(h1)),
                    (sg * h0, face_y(h0) - face_lean(face_top_z(h0)), face_top_z(h0))]
            mb.face(quad, 0, want=(0, 1, 1))
    hinge = (0.0, y_rear, z_hood(y_rear))
    obj = mb.build("EXT_Frunk_Lid", "DOORS_AND_HATCHES", M["steel"], origin=hinge)
    finish_panel(obj, 0.003, 0.002)
    L.explode(obj, (0, 0.35, 1), 0.9, 1, "Tapa del frunk", "Tapa del maletero delantero (frunk)", "R")
    obj["pivot_es"] = "Bisagra trasera junto a la base del parabrisas"
    return obj


# ---------------------------------------------------------------------------
# Frontal superior de acero
# ---------------------------------------------------------------------------
def build_front_fascia(M):
    mb = L.MeshBuilder()
    zb = S.FRONT_FACE_BOT_Z
    hc_t, zc_t = corner_top()
    hc_b = corner_hw(zb)

    def bot(h):
        return (h, face_y(abs(h)) - face_lean(zb), zb)

    def top(h, z=None):
        z = face_top_z(abs(h)) if z is None else z
        return (h, face_y(abs(h)) - face_lean(z), z)

    for s in (1, -1):
        cols_b = [0.0, 0.377, 0.622, hc_b - GAP]
        cols_t = [0.0, 0.377, 0.622, hc_t - GAP]
        for i in range(3):
            a, b = bot(s * cols_b[i]), bot(s * cols_b[i + 1])
            zt_i1 = zc_t if i == 2 else None
            c, d = top(s * cols_t[i + 1], zt_i1), top(s * cols_t[i])
            mb.face([a, b, c, d], 0, want=(s * (0.2 if i < 2 else 0.6), 1, 0))
    obj = mb.build("EXT_Front_Fascia_Upper", "EXTERIOR_PANELS", M["steel"])
    finish_panel(obj, 0.003, 0.0015)
    L.explode(obj, (0, 1, 0.1), 0.75, 1, "Frontal", "Frontal superior de acero inoxidable", "R")
    return obj


# ---------------------------------------------------------------------------
# Aletas delanteras (guardabarros) con hombro superior
# ---------------------------------------------------------------------------
def build_fenders(M):
    objs = []
    y_door = S.DOOR_F_FRONT_Y + GAP / 2
    split = S.hood_side_split_y()
    hc_t, zc_t = corner_top()
    for s, side in SIDES:
        mb = L.MeshBuilder()
        cut = clip_polyline_y(ARCH_F_CUT, y_door, 2.6)
        z0 = cut[0][1]
        poly = [(corner_y(z0) - GAP / 2, z0)]
        for k in range(1, 5):
            z = z0 + (zc_t - z0) * k / 4
            poly.append((corner_y(z) - GAP / 2, z))
        yc = face_y(hc_t) - 0.028
        poly.append((yc, z_hood(yc)))
        for y in (2.35, 2.33):
            if split < y < yc:
                poly.append((y, z_hood(y)))
        poly.append((split, S.z_belt(split)))
        for y in (2.1, 1.9, 1.6, 1.3):
            poly.append((y, S.z_belt(y)))
        poly.append((y_door, S.z_belt(y_door)))
        poly.append((y_door, z_on_polyline(ARCH_F_CUT, y_door)))
        for p in reversed(cut):
            if p[0] > y_door + 1e-6:
                poly.append(p)
        side_faces(mb, poly, s, "body", 0)
        # Hombro superior (plano del invernadero) entre la cintura y el borde del capó
        sh = [(S.GLASS_TIP_Y, S.z_belt(S.GLASS_TIP_Y)), (2.1, S.z_belt(2.1)), (split, S.z_belt(split))]
        for y in (2.2, 2.1, 2.0, 1.945):
            if y < split:
                sh.append((y, z_hood(y)))
        sh.append((1.930, S.z_top(1.930)))
        sh.append((S.GLASS_TIP_Y, S.z_top(S.GLASS_TIP_Y)))
        side_faces(mb, sh, s, "glass", 0)
        obj = mb.build(f"EXT_Fender_F{side}", "EXTERIOR_PANELS", M["steel"])
        finish_panel(obj)
        L.explode(obj, (s, 0.25, 0.1), 0.7, 1, "Aletas delanteras", f"Aleta delantera {side_name(s)}", "R")
        objs.append(obj)
    return objs


# ---------------------------------------------------------------------------
# Puertas
# ---------------------------------------------------------------------------
def glass_top_z(y):
    band = S.interp([(1.876, S.z_top(1.876) - S.z_belt(1.876)), (0.378, 0.081), (-0.92, 0.078)], y)
    return S.z_top(y) - band


def build_doors(M):
    """Puertas con piel exterior, estructura interior, cristal móvil y marco negro."""
    out = {}
    yF = S.DOOR_F_FRONT_Y - GAP / 2
    yB1 = S.DOOR_B_SEAM_Y + GAP / 2
    yB2 = S.DOOR_B_SEAM_Y - GAP / 2
    yR = S.DOOR_R_REAR_Y + GAP / 2
    da, db = Vector(ARCH_F[2]), Vector(ARCH_F[3])   # diagonal trasera de la aleta delantera

    def diag_y(z):
        t = (z - da.y) / (db.y - da.y)
        return da.x + t * (db.x - da.x) - 0.008

    def diag_z(y):
        t = (y + 0.008 - da.x) / (db.x - da.x)
        return da.y + t * (db.y - da.y)

    zbot = S.Z_ROCKER_TOP + GAP / 2
    specs = {
        "F": dict(front=yF, rear=yB1, notch=True, glass_front=S.GLASS_TIP_Y,
                  glass_rear=S.GLASS_F_REAR_Y, frame_rear=yB1),
        "R": dict(front=yB2, rear=yR, notch=False, glass_front=S.GLASS_R_FRONT_Y,
                  glass_rear=S.GLASS_R_REAR_Y, frame_rear=yR),
    }
    for s, side in SIDES:
        for key, sp in specs.items():
            name = f"{key}{side}"
            hy = sp["front"] - 0.02
            hinge = (s * (S.hw_body(hy, 0.9) - 0.03), hy, 0.85)
            door = L.assembly(f"DOOR_{name}", "DOORS_AND_HATCHES", hinge)
            door["pivot_es"] = "Eje de bisagras vertical junto al borde delantero"
            L.explode(door, (s, 0.12, 0.02), 0.95, 1, "Puertas",
                      f"Puerta {'delantera' if key == 'F' else 'trasera'} {side_name(s)}", "R")
            # Piel exterior
            mb = L.MeshBuilder()
            poly = [(sp["rear"], zbot)]
            if sp["notch"]:
                poly += [(diag_y(zbot), zbot), (sp["front"], diag_z(sp["front"]))]
            else:
                poly += [(sp["front"], zbot)]
            poly += [(sp["front"], S.z_belt(sp["front"])), (sp["rear"], S.z_belt(sp["rear"]))]
            side_faces(mb, poly, s, "body", 0)
            skin = mb.build(f"EXT_Door_{name}_Skin", "DOORS_AND_HATCHES", M["steel"], parent=door)
            finish_panel(skin, 0.0025, 0.0016)
            L.explode(skin, (s, 0, 0), 0.22, 6, "Puertas", "Piel exterior de acero de la puerta", "R")
            # Estructura interior (prisma retranqueado de chapa interior)
            mb = L.MeshBuilder()
            z_lo = zbot + 0.02
            pts = [(sp["rear"] + 0.012, z_lo), (sp["front"] - 0.012, z_lo + (0.07 if sp["notch"] else 0)),
                   (sp["front"] - 0.012, S.z_belt(sp["front"]) - 0.03),
                   (sp["rear"] + 0.012, S.z_belt(sp["rear"]) - 0.03)]
            ring_o = [(s * (S.hw_body(y, z) - 0.008), y, z) for (y, z) in pts]
            ring_i = [(s * (S.hw_body(y, z) - 0.125), y, z) for (y, z) in pts]
            ctr = sum((Vector(p) for p in ring_o + ring_i), Vector()) / 8
            mb.quad_strip(ring_o, ring_i, closed=True, want_fn=lambda c: c - ctr)
            mb.face(ring_i, 0, want=(-s, 0, 0))
            inner = mb.build(f"DOOR_{name}_InnerStructure", "DOORS_AND_HATCHES", M["ecoat"], parent=door)
            L.set_smooth_by_angle(inner, 30)
            L.explode(inner, (-s, 0, 0), 0.20, 6, "Puertas",
                      "Estructura interior de la puerta (chapa interior y refuerzos)", "A")
            # Cristal móvil
            mb = L.MeshBuilder()
            gf, gr = sp["glass_front"], sp["glass_rear"]
            gp = [(gr, S.z_belt(gr) + 0.004)]
            if key == "F":
                gp.append((gf - 0.02, S.z_belt(gf - 0.02) + 0.004))
                gp += [(y, glass_top_z(y) - 0.006) for y in (1.4, 0.95, 0.71, 0.378)]
            else:
                gp += [(gf, S.z_belt(gf) + 0.004), (gf, glass_top_z(gf) - 0.006)]
                gp += [(y, glass_top_z(y) - 0.006) for y in (0.0, -0.505) if gr < y < gf]
            gp.append((gr, glass_top_z(gr) - 0.006))
            side_faces(mb, gp, s, "glass", 0)
            glass = mb.build(f"GLS_Door_{name}", "GLASS_AND_MIRRORS", M["glass_side"], parent=door)
            L.solidify(glass, 0.0045, offset=-1.0)
            L.explode(glass, (s * 0.3, 0, 1), 0.35, 6, "Cristales", "Cristal móvil de la puerta", "R")
            # Marco negro (guía superior y apliques de pilar B / C) sobre el plano del invernadero
            mb = L.MeshBuilder()
            fr = sp["frame_rear"]
            ys_top = [y for y in (gf, 1.4, 0.95, 0.71, 0.378, 0.0, -0.505, gr) if gr <= y <= gf]
            if key == "R":
                ys_top = [sp["front"]] + ys_top
            ys_top = ys_top + [fr]
            top_in = [(y, glass_top_z(y) - 0.006) for y in ys_top]
            top_out = [(y, glass_top_z(y) + 0.012) for y in reversed(ys_top)]
            side_faces(mb, top_in + top_out, s, "glass", 0)
            side_faces(mb, [(gr, S.z_belt(gr)), (fr, S.z_belt(fr)), (fr, glass_top_z(fr) - 0.006),
                            (gr, glass_top_z(gr) - 0.006)], s, "glass", 0)
            if key == "R":
                side_faces(mb, [(sp["front"], S.z_belt(sp["front"])), (gf, S.z_belt(gf)),
                                (gf, glass_top_z(gf) - 0.006), (sp["front"], glass_top_z(sp["front"]) - 0.006)],
                           s, "glass", 0)
            frame = mb.build(f"EXT_Door_{name}_GlassFrame", "DOORS_AND_HATCHES", M["black_gloss"], parent=door)
            finish_panel(frame, 0.004, 0.001, offset=1.0)
            L.explode(frame, (s, 0, 0.3), 0.16, 6, "Puertas", "Marco y aplique negro del cristal", "R")
            out[name] = door
    return out


# ---------------------------------------------------------------------------
# Pilares A y largueros del techo
# ---------------------------------------------------------------------------
def build_roof_rails(M):
    objs = []
    for s, side in SIDES:
        mb = L.MeshBuilder()
        y0, y1 = S.GLASS_TIP_Y, S.CAB_REAR_Y
        ys = [y for y in (y0, 1.4, 0.95, 0.71, 0.45, 0.378, 0.33, 0.19, 0.0, -0.505, y1) if y1 <= y <= y0]
        lower = [(y, glass_top_z(y) + 0.012 + GAP) for y in ys]
        upper = [(y, S.z_top(y)) for y in reversed(ys)]
        side_faces(mb, lower + upper, s, "glass", 0)
        obj = mb.build(f"EXT_RoofRail_{side}", "BODY_STRUCTURE", M["steel"])
        finish_panel(obj, 0.003, 0.0015)
        L.explode(obj, (s, 0, 0.5), 0.55, 3, "Estructura del techo",
                  f"Pilar A y larguero de techo ({side_name(s)})", "R")
        objs.append(obj)
    return objs


def roof_hw(y, inset=0.0):
    return S.hw_roof_edge(y) - inset


# ---------------------------------------------------------------------------
# Superficie superior acristalada
# ---------------------------------------------------------------------------
def build_top_glass(M):
    objs = []
    frit = 0.055

    def glass_panel(name, y0, y1, mat, extra, label, edir):
        mb = L.MeshBuilder()
        ys = profile_breaks(y0, y1, extra)
        top_faces(mb, ys, lambda y: -roof_hw(y, 0.006), lambda y: -roof_hw(y, frit), 1, 0.001)
        top_faces(mb, ys, lambda y: -roof_hw(y, frit), lambda y: roof_hw(y, frit), 0, 0.001)
        top_faces(mb, ys, lambda y: roof_hw(y, frit), lambda y: roof_hw(y, 0.006), 1, 0.001)
        obj = mb.build(name, "GLASS_AND_MIRRORS", [mat, M["glass_frit"]])
        L.solidify(obj, 0.0055, offset=-1.0)
        L.explode(obj, edir, 0.95, 1, "Cristales", label, "R")
        objs.append(obj)

    glass_panel("GLS_Windshield", 1.930, 0.600, M["glass_windshield"], (1.6, 1.2, 0.8),
                "Parabrisas laminado", (0, 0.45, 1))
    glass_panel("GLS_Roof", 0.550, -0.860, M["glass_roof"], (0.4, 0.25, -0.25, -0.6),
                "Techo de cristal fijo", (0, -0.1, 1))

    def steel_strip(name, y0, y1, label, edir):
        mb = L.MeshBuilder()
        top_faces(mb, profile_breaks(y0, y1), lambda y: -roof_hw(y, 0.004), lambda y: roof_hw(y, 0.004), 0)
        obj = mb.build(name, "BODY_STRUCTURE", M["steel"])
        finish_panel(obj, 0.003, 0.001)
        L.explode(obj, edir, 0.75, 3, "Estructura del techo", label, "A")
        objs.append(obj)

    steel_strip("EXT_Roof_Header_Front", 0.600 - GAP, 0.550 + GAP, "Travesaño delantero del techo", (0, 0.2, 1))
    steel_strip("EXT_Roof_Header_Rear", -0.860 - GAP, S.CAB_REAR_Y - 0.06, "Travesaño trasero del techo",
                (0, -0.3, 1))
    # Aplique del limpiaparabrisas (escalón entre capó y parabrisas)
    mb = L.MeshBuilder()
    yh = 1.945
    mb.face([(-roof_hw(yh, 0.004), yh, z_hood(yh) - 0.004), (roof_hw(yh, 0.004), yh, z_hood(yh) - 0.004),
             (roof_hw(1.930, 0.004), 1.930, S.z_top(1.930)), (-roof_hw(1.930, 0.004), 1.930, S.z_top(1.930))],
            0, want=(0, 1, 0.5))
    cowl = mb.build("EXT_Cowl_Wiper_Applique", "EXTERIOR_PANELS", M["plastic_black"])
    finish_panel(cowl, 0.004, 0.001)
    L.explode(cowl, (0, 0.6, 1), 0.55, 6, "Limpiaparabrisas", "Aplique del limpiaparabrisas", "R")
    objs.append(cowl)
    return objs


# ---------------------------------------------------------------------------
# Laterales de la caja (vela, escalón del pilar C y remate superior)
# ---------------------------------------------------------------------------
def build_bed_sides(M):
    objs = []
    y_front = S.CAB_REAR_Y - GAP / 2
    y_end = tg_y(1.345) + 0.010
    z_rock = S.Z_ROCKER_TOP + GAP / 2
    top_ys = profile_breaks(y_front, y_end, extra=(-1.4, -1.9, -2.4))
    for s, side in SIDES:
        mb = L.MeshBuilder()
        poly = [(y_front, z_rock)]
        poly += [(y, S.z_top(y)) for y in top_ys]
        for z in (1.30, 1.070, 0.751, 0.715):
            y = tg_y(z) + 0.010
            poly.append((y, z))
        poly.append((-2.60, 0.735))
        for p in reversed(ARCH_R_CUT):
            poly.append(p)
        poly.append((ARCH_R_CUT[0][0], z_rock))
        side_faces(mb, poly, s, "body", 0)
        # Escalón del pilar C (cara orientada hacia delante)
        zs = [S.z_belt(y_front) + 0.002, 1.45, 1.55, S.z_top(y_front)]
        for z0, z1 in zip(zs, zs[1:]):
            mb.face([(s * S.hw_glass(y_front, z0), y_front, z0), (s * S.hw_body(y_front, z0), y_front, z0),
                     (s * S.hw_body(y_front, z1), y_front, z1), (s * S.hw_glass(y_front, z1), y_front, z1)],
                    0, want=FWD)
        # Remate superior de la vela

        def hw_out(y):
            return S.hw_body(y, S.z_top(y))

        def hw_in(y):
            return hw_out(y) - 0.055
        if s > 0:
            top_faces(mb, top_ys, hw_in, hw_out, 0)
        else:
            top_faces(mb, top_ys, lambda y: -hw_out(y), lambda y: -hw_in(y), 0)
        obj = mb.build(f"EXT_BedSide_{side}", "EXTERIOR_PANELS", M["steel"])
        finish_panel(obj)
        L.explode(obj, (s, -0.1, 0.15), 0.85, 1, "Laterales de la caja",
                  f"Lateral de la caja con vela ({side_name(s)})", "R")
        objs.append(obj)
    return objs


# ---------------------------------------------------------------------------
# Aletas de los pasos de rueda
# ---------------------------------------------------------------------------
def build_flares(M):
    objs = []
    for (arch, arch_in, tag, y_lim, wheel) in (
            (ARCH_F, ARCH_F_IN, "F", (1.10, 2.37), WHEEL_F),
            (ARCH_R, ARCH_R_IN, "R", (-2.40, -1.10), WHEEL_R)):
        outer = clip_polyline_y(arch, *y_lim)
        inner = clip_polyline_y(arch_in, *y_lim)
        n = min(len(outer), len(inner))
        outer, inner = outer[:n], inner[:n]
        for s, side in SIDES:
            mb = L.MeshBuilder()
            wc = Vector((0, wheel[0], wheel[1]))

            def P(p, d=0.0):
                return (s * (flare_hw(p[0]) - d), p[0], p[1])

            for i in range(n - 1):
                a, b, c, d = outer[i], outer[i + 1], inner[i + 1], inner[i]
                mb.face([P(a), P(b), P(c), P(d)], 0, want=(s, 0, 0))
                # pestaña exterior hacia la carrocería
                ba = (s * (S.hw_body(a[0], a[1]) - 0.012), a[0], a[1])
                bb = (s * (S.hw_body(b[0], b[1]) - 0.012), b[0], b[1])
                cen = Vector(P(a)) + Vector(P(b))
                mb.face([P(a), P(b), bb, ba], 0,
                        want=tuple((cen / 2 - wc).normalized() * Vector((0, 1, 1)) if True else (0, 0, 1)))
                # labio interior hacia el paso de rueda
                mb.face([P(d), P(c), P(c, 0.11), P(d, 0.11)], 0,
                        want=tuple((wc - (Vector(P(d)) + Vector(P(c))) / 2) * Vector((0, 1, 1))))
            # tapas de los extremos
            for (o, ii) in ((outer[0], inner[0]), (outer[-1], inner[-1])):
                mb.face([P(o), P(ii), P(ii, 0.11), (s * (S.hw_body(o[0], o[1]) - 0.012), o[0], o[1])], 0)
            obj = mb.build(f"EXT_Flare_{tag}{side}", "EXTERIOR_PANELS", M["plastic_textured"])
            L.set_smooth_by_angle(obj, 30)
            L.solidify(obj, 0.004, offset=-1.0)
            L.bevel(obj, 0.003, 2, 30)
            L.weighted_normals(obj)
            L.explode(obj, (s, 0.0, 0.25), 0.6, 1, "Aletas de pasos de rueda",
                      f"Aleta del paso de rueda {'delantero' if tag == 'F' else 'trasero'} ({side_name(s)})", "R")
            objs.append(obj)
    return objs


def build_wheel_liners(M):
    """Pasos de rueda interiores de plástico que cierran visualmente la carrocería."""
    objs = []
    for arch_in, tag, wheel in ((ARCH_F_IN, "F", WHEEL_F), (ARCH_R_IN, "R", WHEEL_R)):
        for s, side in SIDES:
            mb = L.MeshBuilder()
            x_out, x_in = 0.965, 0.49
            ring_o = [(s * x_out, y, z) for (y, z) in arch_in]
            ring_i = [(s * x_in, y, z) for (y, z) in arch_in]
            wc = Vector((0, wheel[0], wheel[1]))
            mb.quad_strip(ring_o, ring_i, closed=False,
                          want_fn=lambda c: (wc - c) * Vector((0, 1, 1)))
            zb = min(p[1] for p in arch_in) - 0.02
            wall = ring_i + [(s * x_in, arch_in[-1][0], zb), (s * x_in, arch_in[0][0], zb)]
            mb.face(wall, 0, want=(s, 0, 0))
            obj = mb.build(f"BODY_WheelLiner_{tag}{side}", "BODY_STRUCTURE", M["plastic_liner"])
            L.solidify(obj, 0.003, offset=-1.0)
            L.explode(obj, (s, 0, 0.1), 0.35, 3, "Pasos de rueda interiores",
                      "Paso de rueda interior (cubre-ruedas de plástico)", "A")
            objs.append(obj)
    return objs


def build_rockers(M):
    objs = []
    y0, y1 = 1.150, -1.155
    zt, zb = S.Z_ROCKER_TOP, S.Z_ROCKER_BOT
    prof = [(S.HW_ROCKER - 0.014, zt - 0.002), (S.HW_ROCKER, zt - 0.02), (S.HW_ROCKER - 0.006, zb + 0.03),
            (S.HW_ROCKER - 0.035, zb), (0.80, zb + 0.005)]
    for s, side in SIDES:
        mb = L.MeshBuilder()
        ra = [(s * hw, y0, z) for (hw, z) in prof]
        rb = [(s * hw, y1, z) for (hw, z) in prof]
        mb.quad_strip(ra, rb, closed=False, want_fn=lambda c: Vector((c.x - s * 0.80, 0, c.z - 0.36)))
        mb.face(ra, 0, want=FWD)
        mb.face(rb, 0, want=(0, -1, 0))
        obj = mb.build(f"EXT_Rocker_{side}", "EXTERIOR_PANELS", M["plastic_textured"])
        L.set_smooth_by_angle(obj, 30)
        L.bevel(obj, 0.004, 2, 30)
        L.weighted_normals(obj)
        L.explode(obj, (s, 0, -0.35), 0.5, 1, "Faldones", f"Faldón lateral ({side_name(s)})", "R")
        objs.append(obj)
    return objs


# ---------------------------------------------------------------------------
# Portón trasero
# ---------------------------------------------------------------------------
def build_tailgate(M):
    tg = S.TAILGATE_FACE
    depth = 0.075

    def hw(z):
        return S.hw_body(-2.92, z) - GAP

    mb = L.MeshBuilder()
    outer = [(p[0], p[1]) for p in tg]
    for (y0, z0), (y1, z1) in zip(outer, outer[1:]):
        mb.face([(-hw(z0), y0, z0), (-hw(z1), y1, z1), (hw(z1), y1, z1), (hw(z0), y0, z0)], 0, want=(0, -1, 0))
    yt, zt = outer[0]
    yb, zb = outer[-1]
    top_in = (yt + depth, zt - 0.004)
    mb.face([(-hw(zt), yt, zt), (hw(zt), yt, zt), (hw(zt), top_in[0], top_in[1]),
             (-hw(zt), top_in[0], top_in[1])], 0, want=UP)
    mb.face([(-hw(zt) + 0.01, top_in[0], top_in[1]), (hw(zt) - 0.01, top_in[0], top_in[1]),
             (hw(zb) - 0.01, yb + depth, zb), (-hw(zb) + 0.01, yb + depth, zb)], 0, want=FWD)
    for sg in (1, -1):
        pts = [(sg * hw(z), y, z) for (y, z) in outer] + \
              [(sg * (hw(zb) - 0.01), yb + depth, zb), (sg * (hw(zt) - 0.01), top_in[0], top_in[1])]
        mb.face(pts, 0, want=(sg, 0, 0))
    mb.face([(-hw(zb), yb, zb), (hw(zb), yb, zb), (hw(zb) - 0.01, yb + depth, zb),
             (-hw(zb) + 0.01, yb + depth, zb)], 0, want=(0, 0, -1))
    hinge = (0.0, yb + 0.03, zb + 0.01)
    obj = mb.build("EXT_Tailgate", "DOORS_AND_HATCHES", M["steel"], origin=hinge)
    finish_panel(obj, 0.0, 0.002)
    L.explode(obj, (0, -1, -0.15), 0.95, 1, "Portón trasero", "Portón trasero con bisagras laterales y luz superior", "R")
    obj["pivot_es"] = "Bisagras inferiores, apertura hacia abajo"
    return obj


# ---------------------------------------------------------------------------
# Cubierta rígida (tonneau)
# ---------------------------------------------------------------------------
def build_tonneau(M):
    objs = []
    y0 = -0.985
    y1 = tg_y(1.345) + 0.080

    def hw_rail_out(y):
        return S.hw_body(y, S.z_top(y)) - 0.055 - GAP

    def hw_rail_in(y):
        return hw_rail_out(y) - 0.028

    ymid = (y0 + y1) / 2
    root = L.assembly("TONNEAU_ASSEMBLY", "CARGO_BED", (0, ymid, S.z_top(ymid)))
    L.explode(root, (0, 0, 1), 0.7, 1, "Cubierta de la caja", "Cubierta rígida motorizada (tonneau)", "R")
    for s, side in SIDES:
        mb = L.MeshBuilder()
        ys = profile_breaks(y0, y1)
        if s > 0:
            top_faces(mb, ys, hw_rail_in, hw_rail_out, 0, -0.004)
        else:
            top_faces(mb, ys, lambda y: -hw_rail_out(y), lambda y: -hw_rail_in(y), 0, -0.004)
        rail = mb.build(f"CARGO_Tonneau_Rail_{side}", "CARGO_BED", M["anodized_dark"], parent=root)
        finish_panel(rail, 0.012, 0.001)
        L.explode(rail, (s, 0, 0.2), 0.25, 6, "Cubierta de la caja", "Carril lateral de la cubierta", "R")
        objs.append(rail)
    n = 22
    pitch = (y0 - y1) / n
    for i in range(n):
        ya = y0 - i * pitch - 0.0015
        yb = ya - pitch + 0.003
        mb = L.MeshBuilder()
        top_faces(mb, profile_breaks(ya, yb), lambda y: -hw_rail_in(y) + 0.002,
                  lambda y: hw_rail_in(y) - 0.002, 0, -0.002)
        slat = mb.build(f"CARGO_Tonneau_Slat_{i + 1:02d}", "CARGO_BED", M["anodized_dark"], parent=root)
        finish_panel(slat, 0.010, 0.0012)
        L.explode(slat, (0, -0.1, 1), 0.06 + 0.014 * i, 6, "Cubierta de la caja",
                  f"Lama {i + 1} de la cubierta (el número de lamas no consta en las fuentes)", "A")
        objs.append(slat)
    return objs


# ---------------------------------------------------------------------------
# Paragolpes
# ---------------------------------------------------------------------------
def _profile_shell(mb, prof, hws, plan_offset, outward_sign):
    """Barre un perfil (Y, Z) a lo largo de la anchura con retroceso en planta."""
    rows = []
    signed = [-h for h in reversed(hws)] + list(hws[1:])
    for hw in signed:
        h = abs(hw)
        rows.append([(hw, y - outward_sign * plan_offset(h, y, z), z) for (y, z) in prof])
    for i in range(len(rows) - 1):
        for j in range(len(prof) - 1):
            (y0, z0), (y1, z1) = prof[j], prof[j + 1]
            want = (0, outward_sign * -(z1 - z0), outward_sign * (y1 - y0)) if outward_sign > 0 else \
                   (0, (z1 - z0), -(y1 - y0))
            mb.face([rows[i][j], rows[i][j + 1], rows[i + 1][j + 1], rows[i + 1][j]], 0, want=want)
    mb.face(rows[0], 0, want=(-1, 0, 0))
    mb.face(rows[-1], 0, want=(1, 0, 0))


def build_bumpers(M):
    objs = []
    fb = S.FRONT_BUMPER
    prof = [(S.FRONT_FACE_Y_BOT - 0.006, S.FRONT_FACE_BOT_Z - GAP),
            (fb["recess_y"], fb["recess_z"][1]), (fb["recess_y"], fb["recess_z"][0]),
            (fb["face_y"] - 0.006, fb["face_z"][1]), (fb["face_y"], fb["face_z"][1] - 0.012),
            (fb["face_y"], fb["face_z"][0] + 0.010), (fb["face_y"] - 0.025, fb["face_z"][0]),
            (fb["under_y"], fb["under_z"][1]), (fb["under_y"], fb["under_z"][0]),
            (fb["lip_y"], fb["lip_z"][1]), (fb["lip_y"] - 0.004, fb["lip_z"][0])] + list(S.FRONT_UNDER[1:])
    bplan = [(0.0, 0.0), (0.12, 0.012), (0.38, 0.037), (0.622, 0.090), (0.80, 0.200), (0.94, 0.300),
             (0.985, 0.370)]

    def front_off(h, y, z):
        off = S.interp(bplan, h)
        if y < 2.45:                       # la rampa inferior se acorta sin rebasar su posición
            off = max(0.0, off - (2.60 - y) * 0.8)
        return off
    mb = L.MeshBuilder()
    _profile_shell(mb, prof, [0.0, 0.12, 0.38, 0.622, 0.80, 0.94, 0.985], front_off, 1)
    front = mb.build("EXT_Front_Bumper", "EXTERIOR_PANELS", M["plastic_textured"])
    L.set_smooth_by_angle(front, 30)
    L.solidify(front, 0.004)
    L.bevel(front, 0.003, 2, 30)
    L.weighted_normals(front)
    L.explode(front, (0, 1, -0.2), 0.8, 1, "Paragolpes", "Fascia inferior delantera (paragolpes)", "R")
    objs.append(front)

    rb = S.REAR_BUMPER
    prof = [(rb["notch_y"] + 0.02, rb["notch_z"][1] - 0.002), (rb["notch_y"], rb["notch_z"][1] - 0.004),
            (rb["notch_y"], rb["notch_z"][0]), (rb["face_y"] + 0.012, rb["top_z"]),
            (rb["face_y"], rb["top_z"] - 0.010)] + list(S.REAR_UNDER[1:])
    rplan = [(0.0, 0.0), (0.5, 0.0), (0.80, 0.012), (0.930, 0.045)]

    def rear_off(h, y, z):
        return S.interp(rplan, h)
    mb = L.MeshBuilder()
    _profile_shell(mb, prof, [0.0, 0.5, 0.80, 0.930], rear_off, -1)
    # Laterales del paragolpes: de la esquina trasera al borde posterior del paso de rueda
    wing = [(-2.360, 0.790), (-2.335, 0.300), (-2.558, 0.291), (-2.812, 0.310), (-2.830, 0.350),
            (-2.918 + 0.045, 0.375), (-2.969 + 0.045, 0.506), (-2.986 + 0.045, 0.629),
            (-2.900, 0.712), (-2.600, 0.731), (-2.380, 0.752)]
    for s in (1, -1):
        mb.face([(s * 0.934, y, z) for (y, z) in wing], 0, want=(s, 0, 0))
    rear = mb.build("EXT_Rear_Bumper", "EXTERIOR_PANELS", M["plastic_textured"])
    L.set_smooth_by_angle(rear, 30)
    L.solidify(rear, 0.004)
    L.bevel(rear, 0.003, 2, 30)
    L.weighted_normals(rear)
    L.explode(rear, (0, -1, -0.2), 0.8, 1, "Paragolpes", "Fascia trasera con escalón integrado", "R")
    objs.append(rear)
    return objs


def build_all(M):
    out = {}
    out["hood"] = build_hood(M)
    out["fascia"] = build_front_fascia(M)
    out["fenders"] = build_fenders(M)
    out["doors"] = build_doors(M)
    out["rails"] = build_roof_rails(M)
    out["top"] = build_top_glass(M)
    out["bed_sides"] = build_bed_sides(M)
    out["flares"] = build_flares(M)
    out["liners"] = build_wheel_liners(M)
    out["rockers"] = build_rockers(M)
    out["tailgate"] = build_tailgate(M)
    out["tonneau"] = build_tonneau(M)
    out["bumpers"] = build_bumpers(M)
    return out
