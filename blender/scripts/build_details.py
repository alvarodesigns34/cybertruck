"""Accesorios y detalles exteriores: retrovisores, limpiaparabrisas, cámaras, interruptores,
toma de carga, ganchos de remolque, enganche y rejilla inferior con persianas activas.

[V] Existencia/ubicación general: manual de servicio y manual del propietario
    (cámara en aleta, cámara en pilar B, cámara frontal en la fascia, interruptores de puerta en
    pilares B y C, toma de carga en el paso de rueda trasero izquierdo, persianas activas).
[V] Anchura con espejos 2413,3 mm (define la posición exterior de los retrovisores).
[R]/[A] Formas y medidas de detalle reconstruidas a partir de fotografías.
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L
import build_body as B


def _poly_prism(mb, pts, extrude, mat=0):
    a = [Vector(p) for p in pts]
    b = [p + Vector(extrude) for p in a]
    c = sum(a, Vector()) / len(a)
    mb.face([tuple(p) for p in a], mat, want=-Vector(extrude))
    mb.face([tuple(p) for p in b], mat, want=Vector(extrude))
    for i in range(len(a)):
        j = (i + 1) % len(a)
        q = [a[i], a[j], b[j], b[i]]
        cc = sum(q, Vector()) / 4
        mb.face([tuple(p) for p in q], mat, want=cc - (c + Vector(extrude) * 0.5))


def build_mirrors(M):
    objs = []
    y_base, z_base = 1.075, S.z_belt(1.075) + 0.012
    for s, sd in ((1, "R"), (-1, "L")):
        x_out = S.WIDTH_MIRRORS / 2.0
        x_base = S.hw_body(y_base, z_base - 0.02) - 0.01
        asm = L.assembly(f"MIRROR_{sd}", "GLASS_AND_MIRRORS", (s * x_base, y_base, z_base))
        L.explode(asm, (s, 0.2, 0.3), 0.55, 6, "Retrovisores",
                  f"Retrovisor exterior electromecánico ({'derecho' if s > 0 else 'izquierdo'})", "R")
        # Brazo (pie) del retrovisor
        mb = L.MeshBuilder()
        p0 = Vector((s * x_base, y_base + 0.03, z_base - 0.005))
        p1 = Vector((s * (x_out - 0.16), y_base - 0.005, z_base + 0.045))
        w = 0.024
        pts = [p0 + Vector((0, -0.045, 0)), p0 + Vector((0, 0.045, 0)), p1 + Vector((0, 0.03, 0)),
               p1 + Vector((0, -0.03, 0))]
        _poly_prism(mb, pts, (0, 0, w), 0)
        arm = mb.build(f"EXT_Mirror_{sd}_Arm", "GLASS_AND_MIRRORS", M["plastic_black"], parent=asm)
        L.set_smooth_by_angle(arm, 30)
        L.explode(arm, (s, 0, 0), 0.08, 6, "Retrovisores", "Brazo del retrovisor", "A")
        # Carcasa facetada («skull cap»): cuña de sección trapezoidal
        mb = L.MeshBuilder()
        xc_in, xc_out = s * (x_out - 0.215), s * x_out
        zc = z_base + 0.07
        yb = y_base - 0.04            # cara trasera (cristal)
        h, hf = 0.115, 0.07           # altura trasera y frontal
        back = [(xc_in, yb, zc - h / 2), (xc_out, yb, zc - h / 2 + 0.01), (xc_out, yb, zc + h / 2 - 0.004),
                (xc_in, yb, zc + h / 2)]
        yf = yb + 0.105
        front = [(xc_in + s * 0.02, yf, zc - hf / 2), (xc_out - s * 0.03, yf, zc - hf / 2 + 0.01),
                 (xc_out - s * 0.03, yf, zc + hf / 2), (xc_in + s * 0.02, yf, zc + hf / 2)]
        mb.face(back, 0, want=(0, -1, 0))
        mb.face(front, 0, want=(0, 1, 0))
        ctr = sum((Vector(p) for p in back + front), Vector()) / 8
        for i in range(4):
            j = (i + 1) % 4
            q = [back[i], back[j], front[j], front[i]]
            c = sum((Vector(p) for p in q), Vector()) / 4
            mb.face(q, 0, want=c - ctr)
        cap = mb.build(f"EXT_Mirror_{sd}_Housing", "GLASS_AND_MIRRORS", M["plastic_black"], parent=asm)
        L.set_smooth_by_angle(cap, 30)
        L.bevel(cap, 0.004, 2, 30)
        L.explode(cap, (s, 0.4, 0.2), 0.12, 6, "Retrovisores", "Carcasa del retrovisor", "R")
        # Cristal electrocrómico
        mb = L.MeshBuilder()
        ins = 0.008
        g = [(xc_in + s * ins, yb - 0.002, zc - h / 2 + ins + 0.002),
             (xc_out - s * ins, yb - 0.002, zc - h / 2 + ins + 0.01),
             (xc_out - s * ins, yb - 0.002, zc + h / 2 - ins - 0.004),
             (xc_in + s * ins, yb - 0.002, zc + h / 2 - ins)]
        mb.face(g, 0, want=(0, -1, 0))
        gl = mb.build(f"GLS_Mirror_{sd}", "GLASS_AND_MIRRORS", M["mirror"], parent=asm)
        L.solidify(gl, 0.003)
        L.explode(gl, (0, -1, 0), 0.10, 6, "Retrovisores", "Espejo plano electrocrómico", "R")
        objs += [arm, cap, gl]
    return objs


def build_wiper(M):
    """Limpiaparabrisas único de gran longitud, aparcado en la base del parabrisas."""
    y = 1.905
    z = S.z_top(y) + 0.014
    pivot = (0.06, 1.925, S.z_top(1.925) + 0.02)
    asm = L.assembly("WIPER_ASSEMBLY", "GLASS_AND_MIRRORS", pivot)
    L.explode(asm, (0, 0.4, 1), 0.65, 6, "Limpiaparabrisas", "Limpiaparabrisas (brazo y escobilla)", "R")
    mb = L.MeshBuilder()
    x0, x1 = -0.66, 0.60
    L.box(mb, ((x0 + x1) / 2, y, z), (x1 - x0, 0.022, 0.012), 0)
    L.box(mb, ((x0 + x1) / 2, y, z - 0.009), (x1 - x0 - 0.01, 0.006, 0.008), 1)
    blade = mb.build("EXT_Wiper_Blade", "GLASS_AND_MIRRORS", [M["plastic_black"], M["bushing"]], parent=asm)
    blade.rotation_euler = (math.atan(0.33), 0, 0)
    L.explode(blade, (0, 0, 1), 0.10, 6, "Limpiaparabrisas", "Escobilla de ~1,26 m", "A")
    mb = L.MeshBuilder()
    L.box(mb, (0.0, 1.915, S.z_top(1.915) + 0.022), (0.14, 0.03, 0.014), 0)
    L.lathe(mb, [(0.018, 0.0), (0.018, 0.02), (0.0, 0.022)], pivot, (0, 0.3, 1), 20, 0)
    arm = mb.build("EXT_Wiper_Arm", "GLASS_AND_MIRRORS", M["plastic_black"], parent=asm)
    L.explode(arm, (0, 0.3, 1), 0.05, 6, "Limpiaparabrisas", "Brazo y eje del limpiaparabrisas", "A")
    return [blade, arm]


def _small_box_obj(name, system, mat, center, size, edir, dist, label, fid="A", rot=None, stage=6, group="Detalles"):
    mb = L.MeshBuilder()
    L.box(mb, center, size, 0, rot=rot)
    obj = mb.build(name, system, mat)
    L.set_smooth_by_angle(obj, 30)
    L.bevel(obj, min(size) * 0.2, 1, 30)
    L.explode(obj, edir, dist, stage, group, label, fid)
    return obj


def build_cameras_and_switches(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        # Cámara en la aleta delantera (diagonal trasera del paso de rueda)
        y, z = 1.40, 0.86
        x = s * (B.flare_hw(y) + 0.004)
        objs.append(_small_box_obj(f"CAM_FenderFlare_{sd}", "BODY_FASTENERS", M["black_gloss"], (x, y, z),
                                   (0.012, 0.035, 0.022), (s, 0, 0), 0.25, "Cámara de la aleta (repetidor lateral)", "R"))
        # Cámara del pilar B (sobre el aplique negro)
        yb = S.DOOR_B_SEAM_Y + 0.002
        zb = S.z_belt(yb) + 0.10
        xb = s * (S.hw_glass(yb, zb) + 0.006)
        objs.append(_small_box_obj(f"CAM_BPillar_{sd}", "BODY_FASTENERS", M["black_gloss"], (xb, yb, zb),
                                   (0.010, 0.026, 0.030), (s, 0, 0), 0.25, "Cámara del pilar B", "R"))
        # Interruptores exteriores de apertura (pilar B: puerta delantera; pilar C: trasera)
        zs = S.z_belt(yb) + 0.03
        objs.append(_small_box_obj(f"SW_Door_Front_{sd}", "BODY_FASTENERS", M["plastic_black"],
                                   (s * (S.hw_glass(yb + 0.02, zs) + 0.004), yb + 0.02, zs), (0.008, 0.022, 0.016),
                                   (s, 0, 0), 0.22, "Interruptor de apertura de la puerta delantera (pilar B)", "R"))
        yc = S.CAB_REAR_Y - 0.035
        zc = S.z_belt(yc) + 0.03
        objs.append(_small_box_obj(f"SW_Door_Rear_{sd}", "BODY_FASTENERS", M["plastic_black"],
                                   (s * (S.hw_body(yc, zc) + 0.003), yc, zc), (0.008, 0.022, 0.016),
                                   (s, 0, 0), 0.22, "Interruptor de apertura de la puerta trasera (pilar C)", "R"))
    # Cámara frontal en la fascia inferior y cámara de marcha atrás
    objs.append(_small_box_obj("CAM_Front_Fascia", "BODY_FASTENERS", M["black_gloss"], (0.0, 2.692, 0.585),
                               (0.04, 0.012, 0.025), (0, 1, 0), 0.3, "Cámara frontal (fascia delantera)", "R"))
    objs.append(_small_box_obj("CAM_Rear", "BODY_FASTENERS", M["black_gloss"], (0.0, B.tg_y(0.80) - 0.006, 0.80),
                               (0.04, 0.012, 0.025), (0, -1, 0), 0.3, "Cámara trasera", "R"))
    # Módulo de cámaras del parabrisas (interior, parte superior central)
    yw = 0.70
    objs.append(_small_box_obj("CAM_Windshield_Module", "BODY_FASTENERS", M["plastic_black"],
                               (0.0, yw, S.z_top(yw) - 0.04), (0.20, 0.10, 0.04), (0, 0, -1), 0.35,
                               "Módulo de cámaras del parabrisas", "R",
                               rot=Matrix.Rotation(math.atan(0.30), 3, "X")))
    return objs


def build_charge_port(M):
    """Puerta de la toma de carga NACS en la aleta del paso trasero izquierdo."""
    s = -1
    a, b = Vector(B.ARCH_R[0]), Vector(B.ARCH_R[1])        # diagonal delantera de la aleta trasera
    m = a.lerp(b, 0.55)
    d = (b - a).normalized()
    n = Vector((-d.y, d.x))
    pts2 = [m - d * 0.055 + n * 0.012, m + d * 0.055 + n * 0.012, m + d * 0.055 - n * 0.060,
            m - d * 0.055 - n * 0.060]
    mb = L.MeshBuilder()
    cos = [(s * (B.flare_hw(p.x) + 0.006), p.x, p.y) for p in pts2]
    back = [(s * (B.flare_hw(p.x) - 0.004), p.x, p.y) for p in pts2]
    mb.face(cos, 0, want=(s, 0, 0))
    for i in range(4):
        j = (i + 1) % 4
        mb.face([cos[i], cos[j], back[j], back[i]], 0)
    door = mb.build("EXT_ChargePort_Door", "DOORS_AND_HATCHES", M["plastic_textured"])
    L.bevel(door, 0.002, 1, 30)
    L.explode(door, (s, 0, 0.2), 0.35, 6, "Toma de carga", "Puerta de la toma de carga (NACS)", "R")
    # receptáculo
    mb = L.MeshBuilder()
    c = m - n * 0.024
    L.lathe(mb, [(0.0, 0.0), (0.022, 0.0), (0.022, -0.04), (0.0, -0.04)],
            (s * (B.flare_hw(c.x) - 0.006), c.x, c.y), (s, 0, 0), 24, 0)
    inlet = mb.build("EXT_ChargePort_Inlet", "DOORS_AND_HATCHES", M["plastic_black"])
    L.explode(inlet, (s, 0, 0.1), 0.2, 6, "Toma de carga", "Receptáculo de carga", "A")
    return [door, inlet]


def build_tow_and_grille(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        objs.append(_small_box_obj(f"EXT_TowEye_Cap_{sd}", "BODY_FASTENERS", M["plastic_black"],
                                   (s * 0.38, 2.663, 0.455), (0.07, 0.01, 0.045), (0, 1, 0), 0.25,
                                   "Tapa del gancho de remolque delantero", "R"))
    # Rejilla inferior delantera con persianas activas
    mb = L.MeshBuilder()
    yf = S.FRONT_BUMPER["face_y"] - 0.012
    hw = 0.52
    z0, z1 = 0.540, 0.612
    L.box(mb, (0.0, yf - 0.03, (z0 + z1) / 2), (2 * hw, 0.01, z1 - z0), 0)
    for k in range(5):
        zc = z0 + (k + 0.5) * (z1 - z0) / 5
        L.box(mb, (0.0, yf - 0.012, zc), (2 * hw - 0.02, 0.025, 0.004), 1,
              rot=Matrix.Rotation(math.radians(35), 3, "X"))
    for k in range(-6, 7):
        L.box(mb, (k * hw / 6.5, yf - 0.012, (z0 + z1) / 2), (0.004, 0.03, z1 - z0), 1)
    grille = mb.build("EXT_Front_Lower_Grille", "EXTERIOR_PANELS", [M["plastic_black"], M["plastic_textured"]])
    L.explode(grille, (0, 1, -0.1), 0.45, 6, "Rejilla", "Rejilla inferior con persianas activas", "R")
    objs.append(grille)
    # Enganche de remolque trasero (receptor de 2") y tapa
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -2.83, 0.44), (0.0508, 0.29, 0.0508), 0)
    L.box(mb, (0.0, -2.73, 0.44), (0.30, 0.04, 0.06), 0)
    hitch = mb.build("CHS_Tow_Hitch_Receiver", "UNDERBODY", M["steel_black"])
    L.explode(hitch, (0, -1, -0.3), 0.5, 3, "Enganche", "Receptor del enganche de remolque (clase IV)", "R")
    objs.append(hitch)
    return objs


def build_all(M):
    return build_mirrors(M) + build_wiper(M) + build_cameras_and_switches(M) + build_charge_port(M) + \
        build_tow_and_grille(M)
