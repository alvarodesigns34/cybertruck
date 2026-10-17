"""Detalle exterior: ópticas, retrovisores, limpiaparabrisas y lavaparabrisas, herrajes y juntas de
puertas, frunk («Powergate» en el manual de servicio), portón, cubierta de la caja, toma de carga,
faldillas, difusor, soporte frontal, juntas de cristales y equipamiento de la caja.

[V] Existencia, denominación y fijaciones (manual de servicio de Cybertruck):
    retrovisor electromecánico con cristal electrocrómico (3 tornillos Torx T40 a 18 N·m);
    faro (2 tornillos a 5 N·m, desmontaje desde el frunk); barra de luz delantera fijada al frunk
    (2 tuercas, 2 tornillos, 3 grapas y 3 centradores); motor del limpiaparabrisas (3 tornillos a
    24 N·m); depósito del lavaparabrisas (3 tornillos) con bomba, sensor de nivel y boca;
    bisagras superior e inferior de cada puerta; cierre, percutor, presentador de apertura y
    tirante de retención; burletes primario y secundario (26 grapas) y juntas de cintura;
    bisagras y amortiguadores del frunk, cierre con 2 cables; portón con bisagras laterales,
    barra de torsión, cierres con acercamiento eléctrico, amortiguador y correas; cubierta de la
    caja con raíles «horizon», motores izquierdo y derecho (2 tornillos a 11 N·m), casete plano y
    eslabones de cadena; luz del portón (8 tornillos); difusor trasero (14 tornillos, 12 grapas);
    faldillas delanteras y traseras (2 tornillos y 2 grapas); anclajes forjados de la caja;
    tomas de corriente de la caja; altavoz de aviso a peatones (3 tornillos).
[R]/[A] Formas y posiciones exactas: reconstruidas a partir de fotografías del manual; los
    interiores de faros y mecanismos son representativos.
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L
import ct_parts as P
import build_body as B


def V(*a):
    return Vector(a)


def fpt(hw, z, fwd=0.0):
    """Punto sobre las facetas del frontal (semianchura con signo)."""
    h = abs(hw)
    return V(hw, B.face_y(h) - B.face_lean(z) + fwd, z)


# ---------------------------------------------------------------------------
# Iluminación delantera
# ---------------------------------------------------------------------------
def headlamps(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        # carcasa negra con pestañas de fijación (2 tornillos de 10 mm)
        mb = L.MeshBuilder()
        pts = []
        for h in (0.43, 0.79):
            zc = B.face_top_z(h) - 0.060
            for dz in (-0.032, 0.040):
                for back in (0.006, 0.150):
                    pts.append(fpt(s * h, zc + dz, -back))
        P.hull(mb, pts, 0)
        for h in (0.47, 0.75):
            c = fpt(s * h, B.face_top_z(h) - 0.02, -0.10)
            P.rbox(mb, c, (0.03, 0.03, 0.006), 0.003, 1, None, 0)
            P.flange_bolt(mb, c + V(0, 0, 0.003), (0, 0, 1), 0.006, 1)
        P.rbox(mb, fpt(s * 0.62, B.face_top_z(0.62) - 0.06, -0.165), (0.05, 0.03, 0.03), 0.004, 1, None, 2)
        objs.append(P.make(mb, f"LGT_Headlamp_{sd}", "LIGHTING", [M["lamp_housing"], M["zinc"], M["connector_grey"]],
                           None, (s * 0.3, 1, 0.5), 0.55, 6, "Iluminación",
                           f"Carcasa del faro {side} (2 tornillos; desmontaje desde el frunk)", "R",
                           note="Ubicación verificada en el manual de servicio; forma reconstruida"))
        # módulos de proyección LED (cruce, carretera y auxiliar) con disipadores
        mb = L.MeshBuilder()
        for k, h in enumerate((0.50, 0.61, 0.72)):
            zc = B.face_top_z(h) - 0.062
            c = fpt(s * h, zc, -0.012)
            L.lathe(mb, [(0.0, 0.0), (0.020, -0.002), (0.024, -0.010), (0.024, -0.016)], tuple(c), (0, 1, 0), 24, 0)
            L.lathe(mb, [(0.024, -0.016), (0.028, -0.030), (0.034, -0.060), (0.020, -0.075)], tuple(c), (0, 1, 0),
                    24, 1)
            for i in range(6):
                P.rbox(mb, c + V(-0.025 + i * 0.01, -0.095, 0.0), (0.003, 0.03, 0.05), 0.001, 1, None, 2)
        objs.append(P.make(mb, f"LGT_Headlamp_{sd}_Projectors", "LIGHTING",
                           [M["glass_lens"], M["reflector"], M["alu_machined"]], None, (s * 0.3, 1, 0.5), 0.75, 6,
                           "Iluminación", "Proyectores LED de cruce y carretera con disipadores", "A"))
        # guía de luz de la luz diurna sobre los proyectores y cubierta exterior ahumada
        mb = L.MeshBuilder()
        for h0, h1 in ((0.45, 0.78),):
            for t in range(10):
                h = h0 + (h1 - h0) * t / 9
                c = fpt(s * h, B.face_top_z(h) - 0.030, -0.010)
                P.rbox(mb, c, (0.028, 0.006, 0.004), 0.001, 1, None, 0)
        objs.append(P.make(mb, f"LGT_Headlamp_{sd}_DRL", "LIGHTING", M["led_white"], None, (s * 0.3, 1, 0.5), 0.65, 6,
                           "Iluminación", "Guía de luz de posición/diurna del faro", "A"))
    return objs


def lightbar_optics(M):
    """Óptica interior de la barra de luz delantera (fila de LED) y de la trasera, con soportes."""
    objs = []
    hc, _ = B.corner_top()
    hw_end = min(0.88, hc - 0.03)
    mb = L.MeshBuilder()
    n = 64
    for i in range(n):
        h = -hw_end + 2 * hw_end * (i + 0.5) / n
        z = B.face_top_z(abs(h)) - 0.028
        P.rbox(mb, fpt(h, z, 0.0026), (0.010, 0.0012, 0.003), 0.0004, 1, None, 0)
    objs.append(P.make(mb, "LGT_Front_Lightbar_Optics", "LIGHTING", M["led_white"], None, (0, 1, 0.2), 0.38, 6,
                       "Iluminación", "Fila de LED de la barra de luz delantera (el número de LED no consta en las fuentes)", "A"))
    mb = L.MeshBuilder()
    for h in (-0.55, 0.0, 0.55):
        z = B.face_top_z(abs(h)) - 0.028
        c = fpt(h, z, -0.05)
        P.rbox(mb, c, (0.04, 0.03, 0.02), 0.003, 1, None, 0)
    for h in (-0.30, 0.30):
        z = B.face_top_z(abs(h)) - 0.028
        P.hex_nut(mb, fpt(h, z + 0.012, -0.05), (0, -1, 0), 0.006, 1)
    objs.append(P.make(mb, "LGT_Front_Lightbar_Mounts", "LIGHTING", [M["plastic_black"], M["zinc"]], None,
                       (0, 1, 0.3), 0.28, 6, "Iluminación",
                       "Grapas, centradores y tuercas de la barra de luz (fijada al frunk)", "V"))
    # barra trasera: segmentos LED y carcasa
    mb = L.MeshBuilder()
    z = 1.316
    for i in range(48):
        x = -0.80 + 1.60 * (i + 0.5) / 48
        P.rbox(mb, (x, B.tg_y(z) + 0.006, z), (0.022, 0.004, 0.010), 0.001, 1, None, 0)
    objs.append(P.make(mb, "LGT_Rear_Lightbar_Optics", "LIGHTING", M["led_red"], None, (0, -1, 0.3), 0.36, 6,
                       "Iluminación", "Segmentos LED de la barra de luz trasera", "A"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0, B.tg_y(z) + 0.022, z), (1.66, 0.03, 0.040), 0.004, 1, None, 0)
    for i in range(8):
        x = -0.75 + i * 1.5 / 7
        P.flange_bolt(mb, (x, B.tg_y(z) + 0.038, z), (0, 1, 0), 0.006, 1)
    objs.append(P.make(mb, "LGT_Rear_Lightbar_Housing", "LIGHTING", [M["lamp_housing"], M["zinc"]], None,
                       (0, -1, 0.3), 0.24, 6, "Iluminación", "Carcasa de la luz del portón (8 tornillos a 5 N·m)", "V"))
    return objs


# ---------------------------------------------------------------------------
# Retrovisores
# ---------------------------------------------------------------------------
def mirrors(M):
    objs = []
    y_base, z_base = 1.075, S.z_belt(1.075) + 0.012
    x_out = S.WIDTH_MIRRORS / 2.0
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        asm = bpy_get_or_assembly(f"MIRROR_{sd}", (s * (S.hw_body(y_base, z_base - 0.02) - 0.01), y_base, z_base))
        L.explode(asm, (s, 0.2, 0.3), 0.55, 6, "Retrovisores",
                  f"Retrovisor exterior electromecánico ({side}; 3 tornillos T40 a 18 N·m)", "V")
        xb = s * (S.hw_body(y_base, z_base - 0.02) - 0.012)
        # base triangular sobre la puerta y pie
        mb = L.MeshBuilder()
        P.hull(mb, [V(xb, y_base + 0.07, z_base - 0.01), V(xb, y_base - 0.05, z_base - 0.01),
                    V(xb, y_base + 0.04, z_base + 0.07), V(xb + s * 0.025, y_base + 0.06, z_base - 0.005),
                    V(xb + s * 0.025, y_base - 0.03, z_base - 0.005), V(xb + s * 0.025, y_base + 0.03, z_base + 0.05)], 0)
        p0 = V(xb + s * 0.02, y_base + 0.01, z_base + 0.025)
        p1 = V(s * (x_out - 0.222), y_base - 0.010, z_base + 0.050)      # termina en la cara de la carcasa
        P.hull(mb, [p0 + V(0, -0.035, -0.012), p0 + V(0, 0.035, -0.012), p0 + V(0, 0.02, 0.012), p0 + V(0, -0.03, 0.012),
                    p1 + V(0, -0.025, -0.010), p1 + V(0, 0.03, -0.010), p1 + V(0, 0.02, 0.010), p1 + V(0, -0.02, 0.010)], 0)
        for k in range(3):
            P.torx_screw(mb, V(xb - s * 0.004, y_base + 0.04 - k * 0.04, z_base - 0.012), (0, 0, -1), 0.005, 1)
        objs.append(P.make(mb, f"EXT_Mirror_{sd}_Arm", "GLASS_AND_MIRRORS", [M["plastic_textured"], M["zinc"]], asm,
                           (s, 0, 0), 0.08, 6, "Retrovisores", "Base y pie del retrovisor con 3 tornillos T40", "R"))
        # carcasa facetada («skull cap»): cuña con aristas vivas
        mb = L.MeshBuilder()
        xi, xo = s * (x_out - 0.225), s * x_out
        zc = z_base + 0.075
        yb = y_base - 0.045
        pts = [V(xi, yb, zc - 0.058), V(xo, yb, zc - 0.050), V(xo, yb, zc + 0.054), V(xi, yb, zc + 0.058),
               V(xi + s * 0.012, yb + 0.060, zc - 0.044), V(xo - s * 0.010, yb + 0.050, zc - 0.036),
               V(xo - s * 0.016, yb + 0.050, zc + 0.030), V(xi + s * 0.012, yb + 0.068, zc + 0.036),
               V(xi + s * 0.045, yb + 0.105, zc - 0.012), V(xo - s * 0.060, yb + 0.090, zc - 0.006),
               V(xi + s * 0.045, yb + 0.105, zc + 0.010)]
        P.hull(mb, pts, 0)
        objs.append(P.make(mb, f"EXT_Mirror_{sd}_Housing", "GLASS_AND_MIRRORS", M["plastic_black"], asm,
                           (s, 0.4, 0.2), 0.12, 6, "Retrovisores", "Carcasa facetada del retrovisor («skull cap»)", "R",
                           smooth=15))
        # marco y cristal electrocrómico plano
        mb = L.MeshBuilder()
        ins = 0.007
        g = [(xi + s * ins, zc - 0.058 + ins), (xo - s * ins, zc - 0.050 + ins), (xo - s * ins, zc + 0.054 - ins),
             (xi + s * ins, zc + 0.058 - ins)]
        P.prism(mb, [(p[0], p[1]) for p in g], (0, yb - 0.001, 0), (1, 0, 0), (0, 0, 1), 0.004, (0, 1, 0))
        objs.append(P.make(mb, f"GLS_Mirror_{sd}", "GLASS_AND_MIRRORS", M["mirror"], asm, (0, -1, 0), 0.10, 6,
                           "Retrovisores", "Espejo plano electrocrómico", "V"))
        mb = L.MeshBuilder()
        P.rbox(mb, ((xi + xo) / 2, yb + 0.03, zc), (0.09, 0.04, 0.05), 0.006, 1, None, 0)
        objs.append(P.make(mb, f"EXT_Mirror_{sd}_Actuator", "GLASS_AND_MIRRORS", M["connector_grey"], asm,
                           (s, 0.3, 0.6), 0.16, 6, "Retrovisores", "Motor de ajuste y plegado eléctrico", "A"))
    return objs


def bpy_get_or_assembly(name, loc):
    return L.assembly(name, "GLASS_AND_MIRRORS", loc)


# ---------------------------------------------------------------------------
# Limpiaparabrisas y lavaparabrisas
# ---------------------------------------------------------------------------
def wiper_and_washer(M):
    objs = []
    pivot = V(0.06, 1.925, S.z_top(1.925) + 0.02)
    asm = L.assembly("WIPER_ASSEMBLY", "GLASS_AND_MIRRORS", tuple(pivot))
    L.explode(asm, (0, 0.4, 1), 0.65, 6, "Limpiaparabrisas", "Limpiaparabrisas único (brazo y escobilla)", "R")
    slope = math.atan(0.33)
    y = 1.902
    z = S.z_top(y) + 0.014
    up = V(0, -math.sin(slope), math.cos(slope))
    # escobilla de ~1,26 m: armazón con deflector, goma y adaptador central
    mb = L.MeshBuilder()
    path = [V(x, y, z) for x in (-0.66, -0.3, 0.0, 0.3, 0.60)]
    P.sweep(mb, path, [(-0.011, 0.0), (0.011, 0.0), (0.008, 0.008), (0.0, 0.013), (-0.008, 0.008)], up=tuple(up), mat=0)
    P.sweep(mb, [p - up * 0.006 for p in path], P.rect_profile(0.005, 0.010), up=tuple(up), mat=1)
    P.rbox(mb, V(0.03, y, z + 0.008), (0.06, 0.024, 0.016), 0.004, 1, None, 0)
    objs.append(P.make(mb, "EXT_Wiper_Blade", "GLASS_AND_MIRRORS", [M["plastic_black"], M["bushing"]], asm,
                       (0, 0, 1), 0.10, 6, "Limpiaparabrisas", "Escobilla con deflector y goma (longitud en conflicto: 62 in, ~50 in o ~1,22 m según la fuente)", "R"))
    # brazo con resorte y tapa del eje
    mb = L.MeshBuilder()
    a = pivot + V(0, 0, 0.012)
    b = V(0.03, y + 0.004, z + 0.020)
    P.beam(mb, a, b, 0.030, 0.012, up=tuple(up), r=0.003)
    P.beam(mb, a + V(0, 0.0, 0.0), V(-0.30, y + 0.006, z + 0.016), 0.016, 0.008, up=tuple(up), r=0.002)
    L.lathe(mb, [(0.0, 0.0), (0.022, 0.0), (0.022, 0.016), (0.012, 0.024), (0.0, 0.025)], tuple(pivot), (0, -0.3, 1),
            24, 0)
    for x in (-0.20, 0.25):
        P.cyl(mb, V(x, y + 0.006, z + 0.022), V(x, y + 0.006, z + 0.030), 0.004, 8, 1)       # surtidores
    objs.append(P.make(mb, "EXT_Wiper_Arm", "GLASS_AND_MIRRORS", [M["plastic_black"], M["plastic_black"]], asm,
                       (0, 0.3, 1), 0.05, 6, "Limpiaparabrisas", "Brazo, eje y surtidores del limpiaparabrisas (45 N·m)",
                       "R"))
    # motor y articulación bajo la cubierta (3 tornillos de 13 mm a 24 N·m)
    mb = L.MeshBuilder()
    c = pivot + V(0.0, 0.02, -0.08)
    P.cyl(mb, c, c + V(0.12, 0, 0), 0.040, 24, 0)
    P.rbox(mb, c + V(-0.03, 0, 0), (0.07, 0.07, 0.07), 0.008, 1, None, 0)
    P.rbox(mb, c + V(-0.02, 0, 0.05), (0.18, 0.04, 0.012), 0.003, 1, None, 1)
    for dx in (-0.08, 0.04, 0.12):
        P.flange_bolt(mb, c + V(dx, 0, 0.055), (0, 0, 1), 0.008, 2)
    objs.append(P.make(mb, "EXT_Wiper_Motor", "GLASS_AND_MIRRORS", [M["alu_cast"], M["steel_black"], M["zinc"]], None,
                       (0, 0.4, 0.8), 0.45, 6, "Limpiaparabrisas", "Motor del limpiaparabrisas (3 tornillos a 24 N·m)",
                       "V"))
    # depósito del lavaparabrisas con bomba, sensor de nivel, boca y tapón
    mb = L.MeshBuilder()
    # por encima de la viga del paragolpes y de sus soportes, bajo la tapa del frunk
    t = V(0.62, 2.30, 0.78)
    P.rbox(mb, t, (0.14, 0.16, 0.20), 0.022, 2, None, 0)
    P.cyl(mb, t + V(-0.03, 0.04, 0.10), t + V(-0.05, 0.02, 0.21), 0.018, 16, 0)
    P.disc(mb, t + V(-0.051, 0.019, 0.215), (0, 0, 1), 0.024, 0.016, 16, 1, 0.003)
    P.cyl(mb, t + V(0.07, -0.05, -0.06), t + V(0.10, -0.05, -0.06), 0.014, 12, 2)
    P.rbox(mb, t + V(0.075, 0.04, -0.06), (0.012, 0.02, 0.03), 0.003, 1, None, 2)
    objs.append(P.make(mb, "EXT_Washer_Tank", "GLASS_AND_MIRRORS", [M["plastic_liner"], M["connector_blue"],
                       M["connector_grey"]], None, (1, 0.5, 0), 0.5, 6, "Limpiaparabrisas",
                       "Depósito del lavaparabrisas con bomba, sensor de nivel y boca (3 tornillos)", "V"))
    mb = L.MeshBuilder()
    P.hose(mb, [t + V(0.10, -0.08, -0.08), t + V(0.0, -0.25, 0.20), V(0.30, 2.00, 1.05), pivot + V(0.05, 0.02, -0.07)],
           0.0035, 6, 6, 0)
    objs.append(P.make(mb, "EXT_Washer_Hose", "GLASS_AND_MIRRORS", M["hose"], None, (0.5, 0.5, 0.5), 0.35, 6,
                       "Limpiaparabrisas", "Tubo del lavaparabrisas hasta los surtidores del brazo", "V"))
    return objs


# ---------------------------------------------------------------------------
# Puertas: bisagras, cierres, presentadores, tirantes, elevalunas, juntas
# ---------------------------------------------------------------------------
DOORS = {
    "F": {"y_front": 1.186, "y_rear": 0.081, "z_top": 1.20},
    "R": {"y_front": 0.078, "y_rear": -0.916, "z_top": 1.26},
}


def door_hardware(M):
    objs = []
    for pos, d in DOORS.items():
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{pos}{sd}"
            door = L.assembly(f"DOOR_{tag}", "DOORS_AND_HATCHES", tuple(bpy_loc(f"DOOR_{tag}")))
            yf, yr = d["y_front"], d["y_rear"]
            xin = s * 0.80                       # cara interior de la estructura de la puerta
            xpin = s * 0.905
            # bisagras superior e inferior (hoja de carrocería + hoja de puerta + pasador)
            mb = L.MeshBuilder()
            for z in (0.62, 1.02):
                P.rbox(mb, (xpin, yf + 0.045, z), (0.05, 0.06, 0.07), 0.006, 1, None, 0)
                P.rbox(mb, (xpin - s * 0.02, yf - 0.03, z), (0.05, 0.06, 0.06), 0.006, 1, None, 0)
                P.cyl(mb, (xpin + s * 0.012, yf + 0.005, z - 0.045), (xpin + s * 0.012, yf + 0.005, z + 0.045), 0.009,
                      14, 1)
                for dz in (-0.018, 0.018):
                    P.hex_nut(mb, (xpin - s * 0.02, yf + 0.076, z + dz), (0, 1, 0), 0.008, 1)
                    P.flange_bolt(mb, (xpin - s * 0.03, yf - 0.061, z + dz), (0, -1, 0), 0.010, 1)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Hinges", "DOORS_AND_HATCHES", [M["steel_black"], M["zinc"]], door,
                               (s * 0.3, 0.6, 0), 0.20, 6, "Puertas",
                               "Bisagras superior e inferior con placas de espárragos (2 fijaciones por bisagra a 38 N·m)", "V"))
            # tirante de retención (puertas delanteras) / correa (traseras)
            mb = L.MeshBuilder()
            P.beam(mb, (s * 0.88, yf + 0.06, 0.82), (s * 0.86, yf - 0.16, 0.82), 0.012, 0.03, r=0.003)
            P.rbox(mb, (s * 0.86, yf - 0.17, 0.82), (0.05, 0.05, 0.06), 0.006, 1, None, 0)
            P.flange_bolt(mb, (s * 0.88, yf + 0.07, 0.82), (0, 1, 0), 0.013, 1)
            objs.append(P.make(mb, f"EXT_Door_{tag}_CheckStrap", "DOORS_AND_HATCHES", [M["steel_black"], M["zinc"]],
                               door, (s * 0.3, 0.2, 0), 0.26, 6, "Puertas",
                               "Tirante de retención de la puerta (perno T40 a 23 N·m)", "V"))
            # cierre eléctrico y presentador de apertura en el canto trasero
            mb = L.MeshBuilder()
            P.rbox(mb, (s * 0.88, yr + 0.035, 0.90), (0.07, 0.05, 0.11), 0.006, 1, None, 0)
            P.rbox(mb, (s * 0.88, yr + 0.035, 0.78), (0.05, 0.04, 0.08), 0.006, 1, None, 1)
            for dz in (-0.03, 0.03):
                P.torx_screw(mb, (s * 0.88, yr + 0.004, 0.90 + dz), (0, -1, 0), 0.006, 2)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Latch", "DOORS_AND_HATCHES",
                               [M["alu_cast"], M["connector_grey"], M["zinc"]], door, (s * 0.2, -0.6, 0), 0.24, 6,
                               "Puertas", "Cierre eléctrico de la puerta (13 N·m) y presentador de apertura", "V"))
            # elevalunas de 48 V (motor Q) con dos guías
            mb = L.MeshBuilder()
            yc = 0.5 * (yf + yr)
            for dy in (-0.20, 0.20):
                P.beam(mb, (s * 0.86, yc + dy, 0.52), (s * 0.85, yc + dy * 0.9, d["z_top"] - 0.02), 0.012, 0.03, r=0.003)
            P.cyl(mb, (s * 0.86, yc, 0.56), (s * 0.82, yc, 0.56), 0.040, 20, 1)
            P.hose(mb, [(s * 0.85, yc - 0.20, 0.53), (s * 0.85, yc, 0.58), (s * 0.85, yc + 0.20, 0.53)], 0.002, 6, 4, 2)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Regulator", "DOORS_AND_HATCHES",
                               [M["zinc"], M["steel_black"], M["zinc"]], door, (s * 0.6, 0, -0.3), 0.30, 6, "Puertas",
                               "Elevalunas con motor Q de 48 V", "V"))
            # controlador de la puerta
            mb = L.MeshBuilder()
            P.rbox(mb, (s * 0.83, yc - 0.25, 0.70), (0.03, 0.14, 0.10), 0.005, 1, None, 0)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Controller", "DOORS_AND_HATCHES", M["alu_cast"], door,
                               (s * 0.6, 0, 0.2), 0.36, 6, "Puertas", "Controlador electrónico de la puerta", "V"))
            # burlete secundario (en la puerta, 26 grapas) y juntas de cintura interior y exterior
            mb = L.MeshBuilder()
            zb = 0.45
            pth = [(s * 0.805, yf - 0.02, zb), (s * 0.805, yr + 0.02, zb), (s * 0.805, yr + 0.02, d["z_top"] - 0.02),
                   (s * 0.805, yf - 0.02, d["z_top"] - 0.02), (s * 0.805, yf - 0.02, zb)]
            P.sweep(mb, pth, P.circle_profile(0.008, 8), mat=0)
            yb0, yb1 = yr + 0.01, (yf - 0.01 if pos == "R" else S.GLASS_TIP_Y - 0.05)
            for x_off in (0.0, -0.030):
                pth = []
                for t in range(9):
                    yy = yb1 + (yb0 - yb1) * t / 8
                    zz = S.z_belt(yy) + 0.003
                    xx = S.hw_side(yy, zz) - B.GAP - 0.012 + x_off
                    pth.append((s * xx, yy, zz))
                P.sweep(mb, pth, P.rect_profile(0.008, 0.012, 0.003, 1), mat=0)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Seals", "DOORS_AND_HATCHES", M["rubber_seal"], door,
                               (s * 0.6, 0, 0.2), 0.12, 6, "Juntas",
                               "Burlete secundario (26 grapas) y juntas de cintura interior y exterior", "V"))
            # percutor en el pilar (carrocería)
            mb = L.MeshBuilder()
            yst = yr - 0.012
            P.rbox(mb, (s * 0.88, yst, 0.90), (0.05, 0.010, 0.07), 0.003, 1, None, 0)
            L.lathe(mb, [(0.006, 0.0), (0.006, 0.025), (0.0, 0.026)], (s * 0.88, yst, 0.90), (0, 1, 0), 10, 0)
            objs.append(P.make(mb, f"EXT_Door_{tag}_Striker", "DOORS_AND_HATCHES", M["zinc"], None, (s, 0, 0), 0.18, 6,
                               "Puertas", "Percutor del cierre en el pilar", "V"))
        # burletes primarios de la carrocería (alrededor de cada hueco de puerta)
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        for pos, d in DOORS.items():
            yf, yr = d["y_front"] - 0.012, d["y_rear"] + 0.012
            pth = []
            for (yy, zz) in ((yf, 0.44), (yr, 0.44), (yr, S.z_belt(yr)), (yr, S.z_top(yr) - 0.06),
                             (yf, S.z_top(yf) - 0.06 if pos == "R" else S.z_belt(yf) + 0.30), (yf, 0.44)):
                xx = (S.hw_body(yy, zz) if zz <= S.z_belt(yy) else S.hw_glass(yy, zz)) - 0.05
                pth.append((s * xx, yy, zz))
            P.sweep(mb, pth, [(-0.006, -0.006), (0.006, -0.006), (0.008, 0.002), (0.0, 0.009), (-0.008, 0.002)], mat=0)
        objs.append(P.make(mb, f"EXT_Door_Primary_Seals_{sd}", "DOORS_AND_HATCHES", M["rubber_seal"], None,
                           (s, 0, 0.1), 0.40, 6, "Juntas",
                           "Burletes primarios de la carrocería (huecos de puertas delantera y trasera)", "V"))
    return objs


def bpy_loc(name):
    import bpy
    o = bpy.data.objects.get(name)
    return o.matrix_world.translation.copy() if o else V(0, 0, 0)


# ---------------------------------------------------------------------------
# Frunk motorizado («Powergate» en el manual de servicio)
# ---------------------------------------------------------------------------
def frunk_hardware(M):
    import bpy
    objs = []
    lid = bpy.data.objects.get("EXT_Frunk_Lid")
    mb = L.MeshBuilder()
    for s in (1, -1):
        base = V(s * 0.40, 1.95, 1.16)
        P.rbox(mb, base, (0.05, 0.06, 0.04), 0.006, 1, None, 0)
        pth = [base + V(0, 0.0, 0.02), base + V(0, 0.06, 0.06), base + V(0, 0.12, 0.05)]
        P.sweep(mb, P.catmull(pth, 4), P.rect_profile(0.014, 0.008, 0.002, 1), mat=0)
        P.cyl(mb, base + V(-0.03, 0, 0.0), base + V(0.03, 0, 0.0), 0.007, 10, 1)
        for dy in (-0.015, 0.015):
            P.flange_bolt(mb, base + V(0, dy, -0.02), (0, 0, -1), 0.008, 1)
    objs.append(P.make(mb, "EXT_Frunk_Hinges", "DOORS_AND_HATCHES", [M["steel_black"], M["zinc"]], lid,
                       (0, -0.3, 1), 0.30, 6, "Frunk", "Bisagras del frunk (Powergate Hinge, 2 tornillos a 58 N·m)", "V"))
    mb = L.MeshBuilder()
    for s in (1, -1):
        a = V(s * 0.50, 2.02, 0.96)
        b = V(s * 0.48, 2.30, 1.12)
        P.cyl(mb, a, a.lerp(b, 0.55), 0.011, 14, 0)
        P.cyl(mb, a.lerp(b, 0.5), b, 0.0045, 10, 1)
        for p in (a, b):
            P.disc(mb, p, (1, 0, 0), 0.010, 0.012, 12, 0, 0.002)
    objs.append(P.make(mb, "EXT_Frunk_Struts", "DOORS_AND_HATCHES", [M["steel_black"], M["chrome"]], lid,
                       (0, 0.3, 1), 0.40, 6, "Frunk", "Amortiguadores del frunk (Hood Strut LH/RH)", "V"))
    mb = L.MeshBuilder()
    c = V(0.0, 2.60, 0.94)
    P.rbox(mb, c, (0.09, 0.05, 0.07), 0.006, 1, None, 0)
    for dx in (-0.03, 0.03):
        P.flange_bolt(mb, c + V(dx, 0.026, 0.0), (0, 1, 0), 0.006, 1)
    P.hose(mb, [c + V(-0.04, -0.02, -0.02), c + V(-0.25, -0.10, -0.04), V(-0.50, 2.30, 0.92)], 0.003, 6, 5, 2)
    P.hose(mb, [c + V(0.04, -0.02, -0.02), c + V(0.20, -0.10, -0.05), V(0.38, 2.40, 0.90)], 0.003, 6, 5, 2)
    objs.append(P.make(mb, "EXT_Frunk_Latch", "DOORS_AND_HATCHES", [M["alu_cast"], M["zinc"], M["harness"]], None,
                       (0, 1, -0.2), 0.40, 6, "Frunk",
                       "Cierre del frunk con actuador y 2 cables de apertura (2 tornillos a 9 N·m)", "V"))
    mb = L.MeshBuilder()
    hw, y0, y1, zt = 0.455, 2.58, 1.98, 1.04
    pth = [(-hw, y0, zt), (hw, y0, zt), (hw, y1, zt + 0.15), (-hw, y1, zt + 0.15), (-hw, y0, zt)]
    P.sweep(mb, pth, [(-0.007, 0.0), (0.007, 0.0), (0.006, 0.010), (0.0, 0.014), (-0.006, 0.010)], up=(0, 0, 1))
    objs.append(P.make(mb, "EXT_Frunk_Seal", "DOORS_AND_HATCHES", M["rubber_seal"], None, (0, 0.3, 1), 0.6, 6,
                       "Frunk", "Junta perimetral del frunk", "V"))
    return objs


# ---------------------------------------------------------------------------
# Portón trasero
# ---------------------------------------------------------------------------
def tailgate_hardware(M):
    import bpy
    objs = []
    tg = bpy.data.objects.get("EXT_Tailgate")
    zh, yh = 0.745, -2.86
    mb = L.MeshBuilder()
    for s in (1, -1):
        P.rbox(mb, (s * 0.875, yh + 0.03, zh + 0.02), (0.04, 0.07, 0.09), 0.006, 1, None, 0)
        P.cyl(mb, (s * 0.85, yh, zh), (s * 0.90, yh, zh), 0.012, 14, 1)
        for dz in (-0.0, 0.04):
            P.flange_bolt(mb, (s * 0.895, yh + 0.04, zh + dz), (s, 0, 0), 0.008, 1)
    objs.append(P.make(mb, "EXT_Tailgate_Hinges", "DOORS_AND_HATCHES", [M["steel_black"], M["zinc"]], None,
                       (0, -0.6, -0.3), 0.40, 6, "Portón trasero", "Bisagras laterales del portón (Body Side Hinge)", "V"))
    mb = L.MeshBuilder()
    P.cyl(mb, (-0.84, yh + 0.025, zh + 0.035), (0.84, yh + 0.025, zh + 0.035), 0.008, 12, 0)
    for s in (1, -1):
        P.rbox(mb, (s * 0.80, yh + 0.025, zh + 0.04), (0.03, 0.03, 0.05), 0.004, 1, None, 1)
    objs.append(P.make(mb, "EXT_Tailgate_Torsion_Rod", "DOORS_AND_HATCHES", [M["steel_black"], M["zinc"]], tg,
                       (0, -0.6, 0.6), 0.30, 6, "Portón trasero",
                       "Barra de torsión de asistencia del portón (55/80 N·m)", "V"))
    mb = L.MeshBuilder()
    for s in (1, -1):
        c = V(s * 0.845, -2.865, 1.24)          # alojados en el portón, frente a los percutores de las torres
        P.rbox(mb, c, (0.04, 0.05, 0.10), 0.006, 1, None, 0)
        P.rbox(mb, c + V(0, 0.0, -0.08), (0.035, 0.05, 0.05), 0.005, 1, None, 1)
        for dz in (-0.03, 0.03):
            P.torx_screw(mb, c + V(-s * 0.021, 0, dz), (-s, 0, 0), 0.007, 2)
    objs.append(P.make(mb, "EXT_Tailgate_Cinch_Latches", "DOORS_AND_HATCHES",
                       [M["alu_cast"], M["connector_grey"], M["zinc"]], None, (0, -0.4, 0.6), 0.40, 6,
                       "Portón trasero", "Cierres del portón con acercamiento eléctrico (2 tornillos T40 a 25 N·m)", "V"))
    mb = L.MeshBuilder()
    a, b = V(-0.83, -2.80, 0.98), V(-0.86, -2.84, 0.80)
    P.cyl(mb, a, a.lerp(b, 0.6), 0.010, 12, 0)
    P.cyl(mb, a.lerp(b, 0.55), b, 0.004, 8, 1)
    for s in (1, -1):
        P.hose(mb, [(s * 0.84, -2.79, 1.15), (s * 0.82, -2.82, 1.05), (s * 0.84, -2.85, 0.95)], 0.003, 6, 4, 2)
        P.rbox(mb, (s * 0.84, -2.795, 0.86), (0.02, 0.02, 0.03), 0.004, 1, None, 3)
    objs.append(P.make(mb, "EXT_Tailgate_Damper_Straps", "DOORS_AND_HATCHES",
                       [M["steel_black"], M["chrome"], M["steel_black"], M["bushing"]], None, (0, -0.5, 0.3), 0.35, 6,
                       "Portón trasero", "Amortiguador del portón, correas de cable y topes", "V"))
    mb = L.MeshBuilder()
    P.sweep(mb, [(-0.86, yh + 0.07, zh - 0.005), (0.86, yh + 0.07, zh - 0.005)], P.rect_profile(0.012, 0.012, 0.004, 1))
    objs.append(P.make(mb, "EXT_Tailgate_Seal", "DOORS_AND_HATCHES", M["rubber_seal"], None, (0, -0.5, -0.3), 0.25, 6,
                       "Juntas", "Junta aerodinámica inferior del portón", "V"))
    return objs


# ---------------------------------------------------------------------------
# Cubierta motorizada de la caja (tonneau)
# ---------------------------------------------------------------------------
def tonneau_mechanism(M):
    import bpy
    objs = []
    asm = bpy.data.objects.get("TONNEAU_ASSEMBLY")
    s0 = bpy.data.objects.get("CARGO_Tonneau_Slat_01")
    s22 = bpy.data.objects.get("CARGO_Tonneau_Slat_22")
    for name in ("CARGO_Tonneau_Rail_L", "CARGO_Tonneau_Rail_R"):
        o = bpy.data.objects.get(name)
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        mb = L.MeshBuilder()
        pth = []
        for i in range(12):
            y = -0.99 - i * (1.88 / 11)
            z = S.z_top(y) - 0.030
            hw = 0.790 if y > -2.0 else 0.790 - (y + 2.0) * -0.025
            pth.append((s * (hw + 0.012), y, z))
        prof = [(-0.016, -0.020), (0.016, -0.020), (0.016, 0.018), (0.006, 0.018), (0.006, -0.010), (-0.006, -0.010),
                (-0.006, 0.006), (-0.016, 0.006)]
        if s < 0:
            prof = [(-x, y) for (x, y) in reversed(prof)]
        P.sweep(mb, pth, prof, up=(0, 0, 1), mat=0)
        objs.append(P.make(mb, f"CARGO_Tonneau_Rail_{sd}", "CARGO_BED", M["anodized_dark"], asm, (s, 0, 0.2), 0.25, 6,
                           "Cubierta de la caja", f"Raíl «horizon» {side} de aluminio extruido", "V"))
        mb = L.MeshBuilder()
        for p in pth[:-1]:
            P.rbox(mb, V(*p) + V(-s * 0.002, 0, 0.002), (0.008, 0.10, 0.008), 0.002, 1, None, 0)
        objs.append(P.make(mb, f"CARGO_Tonneau_Chain_{sd}", "CARGO_BED", M["steel_black"], asm, (s, 0, 0.4), 0.18, 6,
                           "Cubierta de la caja", "Eslabones de cadena de arrastre de las lamas", "V"))
        mb = L.MeshBuilder()
        c = V(s * 0.70, -1.10, 1.30)
        P.cyl(mb, c, c + V(0, 0.0, 0.10), 0.035, 20, 0)
        P.rbox(mb, c + V(0, -0.05, 0.05), (0.06, 0.06, 0.12), 0.006, 1, None, 0)
        P.rbox(mb, c + V(0, 0.04, 0.10), (0.04, 0.03, 0.02), 0.003, 1, None, 1)
        for dz in (0.02, 0.09):
            P.flange_bolt(mb, c + V(s * 0.04, -0.05, dz), (s, 0, 0), 0.008, 2)
        objs.append(P.make(mb, f"CARGO_Tonneau_Motor_{sd}", "CARGO_BED",
                           [M["alu_cast"], M["connector_grey"], M["zinc"]], None, (s * 0.5, 0.3, 0.6), 0.45, 6,
                           "Cubierta de la caja", f"Motor {side} de la cubierta (2 tornillos a 11 N·m)", "V"))
    # lamas: perfiles de aluminio extruido con gancho y ranura de articulación (sustituyen a las placas)
    for i in range(1, 23):
        name = f"CARGO_Tonneau_Slat_{i:02d}"
        old = bpy.data.objects.get(name)
        if old is None or old.type != "MESH" or len(old.data.vertices) < 3:
            continue
        mw = L.world_matrix(old)
        ws = [mw @ v.co for v in old.data.vertices]
        keys = {k: old[k] for k in old.keys() if k.startswith(("explode", "label", "fidelity", "note"))}
        xs = [w.x for w in ws]
        cy = sum(w.y for w in ws) / len(ws)
        cz = sum(w.z for w in ws) / len(ws)
        p0 = old.data.polygons[0]
        nrm = (mw.to_3x3() @ p0.normal).normalized()
        if nrm.z < 0:
            nrm = -nrm
        a, b = V(min(xs), cy, cz), V(max(xs), cy, cz)
        prof = [(-0.040, -0.018), (0.034, -0.018), (0.034, -0.010), (0.043, -0.010), (0.043, -0.002),
                (0.030, -0.002), (0.030, 0.002), (-0.032, 0.002), (-0.032, -0.006), (-0.040, -0.006)]
        mb = L.MeshBuilder()
        P.sweep(mb, [a, b], prof, up=tuple(nrm), mat=0)
        for xx in (a.x + 0.012, b.x - 0.012):
            P.cyl(mb, V(xx, cy, cz) - nrm * 0.008 - V(0.008, 0, 0), V(xx, cy, cz) - nrm * 0.008 + V(0.008, 0, 0), 0.006, 10, 1)
        bpy.data.objects.remove(old, do_unlink=True)
        o = P.make(mb, name, "CARGO_BED", [M["anodized_dark"], M["bushing"]], asm, tuple(keys.get("explode_dir", (0, 0, 1))),
                   float(keys.get("explode_dist", 0.1)), int(keys.get("explode_stage", 6)), keys.get("explode_group", ""),
                   "Lama de aluminio extruido con articulación y casquillos (Mid Slat)", "R")
        objs.append(o)
    mb = L.MeshBuilder()
    # entre los motores de la cubierta (x ±0,665), sobre la barrera NVH y detrás de la pared de la caja
    P.rbox(mb, (0, -1.0775, 1.49), (1.28, 0.085, 0.18), 0.03, 2, None, 0)
    objs.append(P.make(mb, "CARGO_Tonneau_Cassette", "CARGO_BED", M["plastic_liner"], None, (0, 0.2, 0.6), 0.75, 6,
                       "Cubierta de la caja", "Casete plano donde se recogen las lamas (Flat Cassette)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0, -1.00, 1.60), (1.58, 0.04, 0.05), 0.006, 1, None, 0)
    objs.append(P.make(mb, "CARGO_Tonneau_Applique", "CARGO_BED", M["plastic_textured"], None, (0, 0.2, 1), 0.55, 6,
                       "Cubierta de la caja", "Embellecedor superior de la cubierta", "V"))
    return objs


# ---------------------------------------------------------------------------
# Toma de carga NACS, faldillas, difusor, soporte frontal y altavoz de peatones
# ---------------------------------------------------------------------------
def charge_port(M):
    s = -1
    a, b = Vector(B.ARCH_R[0]), Vector(B.ARCH_R[1])
    m = a.lerp(b, 0.55)
    d = (b - a).normalized()
    n = Vector((-d.y, d.x))
    c = m - n * 0.024
    x = s * (B.flare_hw(c.x) - 0.006)
    objs = []
    mb = L.MeshBuilder()
    base = V(x, c.x, c.y)
    L.lathe(mb, [(0.0, 0.0), (0.030, 0.0), (0.030, -0.045), (0.0, -0.045)], tuple(base), (s, 0, 0), 32, 0)
    # cara con los cinco contactos NACS (2 de potencia, 2 de señal, 1 de tierra)
    for (dy, dz, r) in ((-0.011, 0.004, 0.0055), (0.011, 0.004, 0.0055), (0.0, -0.014, 0.0035),
                        (-0.008, -0.010, 0.0025), (0.008, -0.010, 0.0025)):
        p = base + V(s * 0.001, dy, dz)
        L.lathe(mb, [(r, 0.0), (r, -0.012), (0.0, -0.012)], tuple(p), (-s, 0, 0), 12, 1)
    P.tube_ring(mb, base + V(s * 0.002, 0, 0), (1, 0, 0), 0.028, 0.032, 0.003, 32, 2)
    objs.append(P.make(mb, "EXT_ChargePort_Inlet", "DOORS_AND_HATCHES", [M["plastic_black"], M["copper"], M["led_white"]],
                       None, (s, 0, 0.1), 0.2, 6, "Toma de carga",
                       "Receptáculo NACS con 5 contactos y anillo de luz", "R"))
    mb = L.MeshBuilder()
    P.rbox(mb, base + V(-s * 0.08, 0.0, 0.0), (0.10, 0.10, 0.08), 0.008, 1, None, 0)
    P.rbox(mb, base + V(-s * 0.08, 0.06, 0.0), (0.04, 0.02, 0.03), 0.003, 1, None, 1)
    objs.append(P.make(mb, "EXT_ChargePort_ECU", "DOORS_AND_HATCHES", [M["alu_cast"], M["connector_grey"]], None,
                       (s, 0.2, 0.3), 0.35, 6, "Toma de carga",
                       "Controlador de la toma de carga (Gen 4, 1 tornillo y 3 conectores)", "V"))
    return objs


def mud_flaps_diffuser_carrier(M):
    objs = []
    for axle, y in (("F", 1.215), ("R", -2.255)):
        for s, sd in ((1, "R"), (-1, "L")):
            mb = L.MeshBuilder()
            xo = B.flare_hw(y) - 0.028
            poly = [(0.86, 0.30), (xo - 0.004, 0.30), (xo, 0.43), (0.86, 0.43)]
            P.prism(mb, [(s * px, pz) for px, pz in poly], (0, y, 0), (1, 0, 0), (0, 0, 1), 0.006, (0, -1, 0))
            for pz in (0.40, 0.33):
                P.flange_bolt(mb, (s * 0.92, y - 0.006, pz), (0, -1, 0), 0.006, 1)
            where = "delantera" if axle == "F" else "trasera"
            objs.append(P.make(mb, f"EXT_MudFlap_{axle}{sd}", "EXTERIOR_PANELS", [M["plastic_textured"], M["zinc"]],
                               None, (s, -0.3, -0.3), 0.30, 6, "Faldillas",
                               f"Faldilla {where} (2 tornillos y 2 grapas)", "R"))
    mb = L.MeshBuilder()
    # el difusor sigue el perfil inferior trasero medido (no altera la silueta oficial)
    prof = [(y, z + 0.006) for (y, z) in S.REAR_UNDER if -2.84 <= y <= -2.34]
    for (ya, za), (yb, zb) in zip(prof, prof[1:]):
        P.hull(mb, [(-0.70, ya, za), (0.70, ya, za), (-0.70, yb, zb), (0.70, yb, zb),
                    (-0.70, ya, za + 0.010), (0.70, ya, za + 0.010), (-0.70, yb, zb + 0.010), (0.70, yb, zb + 0.010)], 0)
    for i in range(6):
        x = -0.55 + i * 0.22
        for (ya, za), (yb, zb) in zip(prof, prof[1:]):
            P.hull(mb, [(x - 0.004, ya, za + 0.004), (x + 0.004, ya, za + 0.004), (x - 0.004, yb, zb + 0.004),
                        (x + 0.004, yb, zb + 0.004), (x - 0.004, ya, za + 0.03), (x + 0.004, ya, za + 0.03),
                        (x - 0.004, yb, zb + 0.03), (x + 0.004, yb, zb + 0.03)], 0)
    for i in range(14):
        x = -0.65 + i * 0.10
        P.flange_bolt(mb, (x, prof[-1][0] - 0.02, S.interp(prof, prof[-1][0] - 0.02) + 0.010), (0, 0, 1), 0.006, 1)
    objs.append(P.make(mb, "EXT_Rear_Diffuser", "EXTERIOR_PANELS", [M["plastic_textured"], M["zinc"]], None,
                       (0, -0.6, -1), 0.45, 1, "Paragolpes", "Difusor trasero con aletas (14 tornillos, 12 grapas)", "V"))
    # soporte frontal de plástico (front end carrier) que sujeta fascia, faros y barra de luz
    mb = L.MeshBuilder()
    hws = [-0.86, -0.70, -0.55, -0.30, 0.0, 0.30, 0.55, 0.70, 0.86]
    for zz in (0.74, 0.90):
        P.sweep(mb, [fpt(h, zz, -0.075) for h in hws], P.rect_profile(0.03, 0.04, 0.004, 1), up=(0, 0, 1))
    for h in hws:
        P.beam(mb, fpt(h, 0.74, -0.075), fpt(h, 0.90, -0.075), 0.03, 0.03, up=(0, 1, 0), r=0.003)
    for h in (-0.62, -0.24, 0.24, 0.62):
        P.hull(mb, [fpt(h - 0.06, 0.745, -0.075), fpt(h + 0.06, 0.745, -0.075), fpt(h, 0.895, -0.075),
                    fpt(h - 0.06, 0.745, -0.06), fpt(h + 0.06, 0.745, -0.06), fpt(h, 0.895, -0.06)], 0)
    for h in (-0.70, -0.30, 0.30, 0.70):
        P.flange_bolt(mb, fpt(h, 0.82, -0.058), (0, 1, 0), 0.007, 1)
    objs.append(P.make(mb, "EXT_Front_End_Carrier", "EXTERIOR_PANELS", [M["plastic_black"], M["zinc"]], None,
                       (0, 1, 0.2), 0.60, 1, "Frontal",
                       "Soporte frontal de plástico (6 tornillos de 10 mm a 5 N·m y 2 de 13 mm)", "V"))
    mb = L.MeshBuilder()
    c = V(-0.62, 2.48, 0.60)
    L.lathe(mb, [(0.0, 0.0), (0.045, 0.0), (0.050, 0.03), (0.0, 0.035)], tuple(c), (0, 1, 0), 24, 0)
    for k in range(3):
        a = 2 * math.pi * k / 3
        P.torx_screw(mb, c + V(math.cos(a) * 0.05, 0.0, math.sin(a) * 0.05), (0, -1, 0), 0.004, 1)
    for s in (1,):
        c2 = V(0.62, 2.47, 0.62)
        L.lathe(mb, [(0.0, 0.0), (0.04, 0.0), (0.045, 0.03), (0.02, 0.06), (0.0, 0.06)], tuple(c2), (0, 1, 0), 20, 0)
    objs.append(P.make(mb, "EXT_Pedestrian_Speaker_Horn", "EXTERIOR_PANELS", [M["plastic_black"], M["zinc"]], None,
                       (0, 1, -0.2), 0.40, 6, "Frontal",
                       "Altavoz de aviso a peatones (3 tornillos T25) y bocina de tono grave", "V"))
    return objs


# ---------------------------------------------------------------------------
# Juntas de cristales y equipamiento de la caja
# ---------------------------------------------------------------------------
def glass_seals(M):
    objs = []
    mb = L.MeshBuilder()
    # junta trasera del techo de cristal y junta de la luneta trasera eléctrica
    P.sweep(mb, [(-0.775, -0.866, S.z_top(-0.866) - 0.005), (0.775, -0.866, S.z_top(-0.866) - 0.005)],
            P.rect_profile(0.012, 0.006, 0.002, 1))
    rw = [(-0.56, -0.960, 1.31), (0.56, -0.960, 1.31), (0.56, -0.960, 1.53), (-0.56, -0.960, 1.53), (-0.56, -0.960, 1.31)]
    P.sweep(mb, rw, P.rect_profile(0.012, 0.010, 0.003, 1), up=(0, -1, 0))
    objs.append(P.make(mb, "GLS_Seals_Roof_Backlite", "GLASS_AND_MIRRORS", M["rubber_seal"], None, (0, -0.3, 0.6), 0.30,
                       6, "Juntas", "Junta trasera del techo de cristal y marco de la luneta trasera", "V"))
    # junta del borde inferior del parabrisas (cowl)
    mb = L.MeshBuilder()
    y = 1.924
    P.sweep(mb, [(-0.86, y, S.z_top(y) - 0.002), (0.86, y, S.z_top(y) - 0.002)], P.rect_profile(0.014, 0.006, 0.002, 1))
    objs.append(P.make(mb, "GLS_Windshield_Edge_Seal", "GLASS_AND_MIRRORS", M["rubber_seal"], None, (0, 0.4, 0.6),
                       0.30, 6, "Juntas", "Junta del borde delantero del parabrisas", "V"))
    return objs


def bed_equipment(M):
    objs = []
    zf = S.BED_FLOOR_Z
    mb = L.MeshBuilder()
    for (x, y) in ((-0.70, -1.10), (0.70, -1.10), (-0.70, -2.72), (0.70, -2.72), (-0.79, -1.80), (0.79, -1.80)):
        sx = 1 if x > 0 else -1
        if abs(x) > 0.75:
            c = V(x, y, zf + 0.30)
            P.rbox(mb, c, (0.012, 0.06, 0.04), 0.004, 1, None, 0)
            P.sweep(mb, [c + V(-sx * 0.006, -0.025, 0.0), c + V(-sx * 0.04, -0.02, 0.0), c + V(-sx * 0.05, 0.0, 0.0),
                         c + V(-sx * 0.04, 0.02, 0.0), c + V(-sx * 0.006, 0.025, 0.0)], P.circle_profile(0.005, 8), mat=0)
        else:
            c = V(x, y, zf + 0.004)
            P.rbox(mb, c, (0.06, 0.04, 0.008), 0.003, 1, None, 0)
            P.sweep(mb, [c + V(-0.02, 0, 0.004), c + V(-0.02, 0, 0.03), c + V(0.0, 0, 0.04), c + V(0.02, 0, 0.03),
                         c + V(0.02, 0, 0.004)], P.circle_profile(0.005, 8), mat=0)
    objs.append(P.make(mb, "CARGO_Tiedowns", "CARGO_BED", M["alu_forged"], None, (0, 0, 1), 0.35, 6, "Caja de carga",
                       "Anclajes forjados de la caja (suelo y laterales)", "V"))
    mb = L.MeshBuilder()
    for (y, kind) in ((-1.25, 0), (-1.40, 1)):
        c = V(-0.808, y, zf + 0.20)
        P.rbox(mb, c, (0.010, 0.09, 0.07), 0.006, 1, None, 0)
        P.rbox(mb, c + V(0.006, 0, 0), (0.004, 0.06, 0.045), 0.003, 1, None, 1)
    objs.append(P.make(mb, "CARGO_Bed_Outlets", "CARGO_BED", [M["plastic_black"], M["connector_grey"]], None,
                       (1, 0, 0.3), 0.30, 6, "Caja de carga", "Tomas de corriente de 120 V y 240 V de la caja", "V"))
    return objs


def build_all(M):
    out = []
    out += headlamps(M)
    out += lightbar_optics(M)
    out += mirrors(M)
    out += wiper_and_washer(M)
    out += door_hardware(M)
    out += frunk_hardware(M)
    out += tailgate_hardware(M)
    out += tonneau_mechanism(M)
    out += charge_port(M)
    out += mud_flaps_diffuser_carrier(M)
    out += glass_seals(M)
    out += bed_equipment(M)
    return [o for o in out if o is not None]
