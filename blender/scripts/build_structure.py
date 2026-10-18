"""Estructura de la carrocería (carrocería en blanco) del Cybertruck.

Fuentes (docs/research-and-fidelity.md §8):
  [V] Manual de reparación de carrocería de Tesla («Body Structure Materials», «Dimensional
      Specifications», «Cast Front/Rear Under Body Repair Guidelines», «Mast Assembly», «Tailgate
      Tower»): la estructura combina piezas de aluminio fundido (bajos delantero y trasero, «mast»,
      torres del portón), aluminio extruido (insertos de umbral), aceros de alta y ultra alta
      resistencia (anillos de puerta, umbrales, refuerzos del suelo) y paneles exteriores de acero
      inoxidable; uniones con adhesivo estructural, soldadura por puntos y remaches flow-form de
      Ø 8 mm. La pieza fundida trasera se sustituye entera o por mitades.
  [V] Cotas de control (centro a centro): largueros delanteros 1.025 mm; torretas 930/938 mm;
      anchura exterior de torretas 1.577 mm; largueros traseros 1.050 mm; base de los pilares B
      1.549 mm; pared trasera 1.463 / 1.406 mm.
  [R] Formas: reconstruidas a partir de las vistas superior, inferior y de despiece del manual de
      reparación (proporciones), sin planos CAD. Los nervios y bosses son representativos.
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_lib as L
import ct_parts as P

SYS = "BODY_STRUCTURE"


def V(*a):
    return Vector(a)


def box_pts(c, size):
    c = Vector(c)
    hx, hy, hz = (s / 2 for s in size)
    return [c + V(dx * hx, dy * hy, dz * hz) for dx in (-1, 1) for dy in (-1, 1) for dz in (-1, 1)]


def seg_hull(mb, a, b, wa, ha, wb=None, hb=None, mat=0):
    """Envolvente de dos secciones rectangulares (largueros con sección variable)."""
    wb = wa if wb is None else wb
    hb = ha if hb is None else hb
    P.hull(mb, box_pts(a, (wa, 0.001, ha)) + box_pts(b, (wb, 0.001, hb)) if abs(Vector(a).y - Vector(b).y) > 0.01
           else box_pts(a, (0.001, wa, ha)) + box_pts(b, (0.001, wb, hb)), mat)


def rib_grid(mb, origin, u, v, w, h, nu, nv, rib_h=0.012, rib_t=0.004, normal=None, diag=True, mat=0):
    """Nervaduras de fundición sobre una cara plana (retícula con diagonales)."""
    lines = []
    for i in range(nu + 1):
        x = w * i / nu
        lines.append(((x, 0), (x, h)))
    for j in range(nv + 1):
        y = h * j / nv
        lines.append(((0, y), (w, y)))
    if diag:
        for i in range(nu):
            for j in range(nv):
                x0, x1 = w * i / nu, w * (i + 1) / nu
                y0, y1 = h * j / nv, h * (j + 1) / nv
                lines.append(((x0, y0), (x1, y1)) if (i + j) % 2 == 0 else ((x0, y1), (x1, y0)))
    P.ribbed_plate(mb, origin, u, v, [(0, 0), (w, 0), (w, h), (0, h)], 0.004, rib_h, rib_t, lines, normal, mat)


# ---------------------------------------------------------------------------
# Pieza fundida delantera (Front Under Body)
# ---------------------------------------------------------------------------
def front_underbody(M):
    mb = L.MeshBuilder()
    for s in (1, -1):
        # larguero delantero (1.025 mm entre centros) con zona de deformación ondulada
        x = s * 0.5125
        P.rbox(mb, (x, 2.02, 0.54), (0.11, 0.80, 0.16), 0.012, 1, None, 0)
        for i in range(6):
            y = 2.40 - i * 0.075
            P.rbox(mb, (x, y, 0.54), (0.122, 0.022, 0.172), 0.008, 1, None, 0)
        P.rbox(mb, (x, 2.425, 0.54), (0.16, 0.012, 0.19), 0.004, 1, None, 0)      # placa de fijación del paragolpes
        # tramo de unión hacia el umbral (desciende y se abre hacia fuera)
        P.hull(mb, box_pts((x, 1.62, 0.54), (0.11, 0.01, 0.16)) + box_pts((s * 0.80, 1.28, 0.385), (0.12, 0.01, 0.17)), 0)
        # torreta del muelle neumático: pared interior nervada, paredes delantera y trasera, tapa
        xi = s * 0.470
        P.rbox(mb, (xi, 1.92, 0.80), (0.022, 0.66, 0.40), 0.004, 1, None, 0)
        for yy in (1.59, 2.25):
            P.rbox(mb, (s * 0.60, yy, 0.82), (0.26, 0.018, 0.36), 0.004, 1, None, 0)
        P.rbox(mb, (s * 0.595, 1.92, 1.005), (0.27, 0.40, 0.025), 0.006, 1, None, 0)
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.3
            P.cyl(mb, (s * 0.585 + math.cos(a) * 0.05, 1.9175 + math.sin(a) * 0.05, 0.99),
                  (s * 0.585 + math.cos(a) * 0.05, 1.9175 + math.sin(a) * 0.05, 1.025), 0.011, 10, 0)
        rib_grid(mb, (xi - s * 0.011, 1.74, 0.62), (0, 1, 0), (0, 0, 1), 0.36, 0.36, 4, 4,
                 normal=(-s, 0, 0))
        # viga superior del guardabarros (1.577 mm entre las torretas exteriores)
        P.rbox(mb, (s * 0.79, 1.84, 0.93), (0.07, 1.10, 0.09), 0.010, 1, None, 0)
        P.hull(mb, box_pts((s * 0.79, 1.30, 0.93), (0.07, 0.01, 0.09)) + box_pts((s * 0.72, 1.92, 0.99), (0.01, 0.12, 0.05)), 0)
    # travesaño del salpicadero (pared trasera de la pieza) con nervaduras y suelo de unión
    P.rbox(mb, (0, 1.46, 0.53), (1.44, 0.07, 0.18), 0.008, 1, None, 0)
    rib_grid(mb, (-0.70, 1.495, 0.44), (1, 0, 0), (0, 0, 1), 1.40, 0.18, 10, 2, rib_h=0.016, normal=(0, 1, 0))
    P.rbox(mb, (0, 1.55, 0.455), (1.10, 0.20, 0.014), 0.004, 1, None, 0)
    o = P.make(mb, "BODY_Casting_Front_UnderBody", SYS, M["alu_cast"], None, (0, 1, 0.35), 1.25, 3,
               "Estructura de la carrocería",
               "Pieza fundida delantera (largueros, torretas, travesaño del salpicadero)", "R",
               note="Cotas de control del manual de reparación (1.025 / 1.577 mm); forma reconstruida", bevel=0.003)
    return [o]


# ---------------------------------------------------------------------------
# Pieza fundida trasera (Rear Under Body), sustituible por mitades
# ---------------------------------------------------------------------------
def rear_underbody(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        # brazo delantero desde el umbral hacia la torreta
        P.hull(mb, box_pts((s * 0.87, -0.97, 0.36), (0.12, 0.01, 0.13)) + box_pts((s * 0.87, -1.42, 0.40), (0.12, 0.01, 0.15)), 0)
        P.hull(mb, box_pts((s * 0.87, -1.42, 0.40), (0.12, 0.01, 0.15)) + box_pts((s * 0.62, -1.56, 0.56), (0.14, 0.01, 0.16)), 0)
        # torreta del muelle trasero
        xi = s * 0.470
        P.rbox(mb, (xi, -1.92, 0.66), (0.022, 0.66, 0.40), 0.004, 1, None, 0)
        for yy in (-1.59, -2.25):
            P.rbox(mb, (s * 0.60, yy, 0.66), (0.26, 0.018, 0.38), 0.004, 1, None, 0)
        P.rbox(mb, (s * 0.595, -1.92, 0.842), (0.27, 0.40, 0.022), 0.006, 1, None, 0)
        rib_grid(mb, (xi - s * 0.011, -2.10, 0.47), (0, 1, 0), (0, 0, 1), 0.36, 0.35, 4, 4, normal=(-s, 0, 0))
        # larguero trasero (1.050 mm entre centros) hasta el absorbedor de impactos
        x = s * 0.525
        P.rbox(mb, (x, -2.44, 0.54), (0.12, 0.70, 0.16), 0.012, 1, None, 0)
        P.hull(mb, box_pts((x, -2.10, 0.54), (0.12, 0.01, 0.16)) + box_pts((s * 0.60, -1.75, 0.60), (0.14, 0.01, 0.18)), 0)
        # mitad del travesaño delantero y del puente posterior entre torretas
        P.rbox(mb, (s * 0.30, -1.50, 0.51), (0.60, 0.09, 0.08), 0.010, 1, None, 0)
        P.rbox(mb, (s * 0.30, -2.16, 0.77), (0.60, 0.08, 0.12), 0.010, 1, None, 0)
        # nervaduras diagonales de la cara superior (en X, como en la vista inferior del manual)
        lines = [((0.0, 0.0), (0.55, 0.60)), ((0.55, 0.0), (0.0, 0.60)), ((0.0, 0.30), (0.55, 0.30))]
        P.ribbed_plate(mb, (0.0 if s > 0 else -0.55, -2.10, 0.70), (1, 0, 0), (0, 1, 0),
                       [(0, 0), (0.55, 0), (0.55, 0.60), (0, 0.60)], 0.006, 0.020, 0.006,
                       lines if s > 0 else [((0.55 - a[0], a[1]), (0.55 - b[0], b[1])) for a, b in lines], (0, 0, 1))
        side = "derecha" if s > 0 else "izquierda"
        objs.append(P.make(mb, f"BODY_Casting_Rear_UnderBody_{sd}", SYS, M["alu_cast"], None, (s * 0.35, -1, 0.3),
                           1.25, 3, "Estructura de la carrocería",
                           f"Pieza fundida trasera, mitad {side} (torreta, larguero y brazo al umbral)", "R",
                           note="La pieza fundida trasera se repara por mitades (manual de reparación); forma reconstruida",
                           bevel=0.003))
    return objs


# ---------------------------------------------------------------------------
# Umbrales, refuerzos del suelo y pared trasera
# ---------------------------------------------------------------------------
def sills_and_floor(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        mb = L.MeshBuilder()
        # termina en y = 1,14, detrás de la aleta del paso de rueda delantero y del extremo del faldón (y 1,15)
        P.rbox(mb, (s * 0.870, 0.06, 0.345), (0.13, 2.16, 0.11), 0.010, 1, None, 0)
        P.rbox(mb, (s * 0.870, 0.06, 0.404), (0.15, 2.16, 0.010), 0.002, 1, None, 0)      # pestaña superior
        objs.append(P.make(mb, f"BODY_Sill_{sd}", SYS, M["ecoat"], None, (s, 0, -0.3), 0.75, 3,
                           "Estructura de la carrocería", f"Umbral {side} de acero de ultra alta resistencia", "R"))
        mb = L.MeshBuilder()
        P.rbox(mb, (s * 0.870, 0.065, 0.345), (0.10, 2.13, 0.085), 0.004, 1, None, 0)
        for k in range(3):
            P.rbox(mb, (s * 0.870, 0.065, 0.318 + k * 0.027), (0.098, 2.12, 0.004), 0.001, 1, None, 0)
        objs.append(P.make(mb, f"BODY_Sill_Insert_{sd}", SYS, M["alu_machined"], None, (s, 0, -0.6), 1.05, 3,
                           "Estructura de la carrocería", f"Inserto de aluminio extruido del umbral {side}", "R"))
    # Refuerzos en X sobre la batería y travesaño de los asientos delanteros
    mb = L.MeshBuilder()
    for s in (1, -1):
        # interrumpidos a ambos lados del travesaño de los asientos delanteros (y = 0,35..0,51)
        for a, b in (((s * 0.80, 1.20), (s * 0.30, 0.525)), ((s * 0.30, 0.335), (s * 0.80, -0.86))):
            P.beam(mb, (a[0], a[1], 0.468), (b[0], b[1], 0.468), 0.085, 0.022, r=0.004)
    objs.append(P.make(mb, "BODY_Floor_X_Brace", SYS, M["ecoat"], None, (0, 0, -0.6), 0.55, 3,
                       "Estructura de la carrocería", "Refuerzos del suelo en X (acero estampado)", "R"))
    mb = L.MeshBuilder()
    pts = [(-0.82, 0.40, 0.47), (-0.40, 0.44, 0.475), (0.0, 0.46, 0.478), (0.40, 0.44, 0.475), (0.82, 0.40, 0.47)]
    P.sweep(mb, P.catmull(pts, 5), P.rect_profile(0.10, 0.028, 0.005, 2))
    objs.append(P.make(mb, "BODY_Seat_Crossmember_Front", SYS, M["ecoat"], None, (0, 0.2, -0.6), 0.45, 3,
                       "Estructura de la carrocería", "Travesaño de los asientos delanteros", "R"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0, -0.975, 0.56), (1.60, 0.06, 0.18), 0.008, 1, None, 0)
    rib_grid(mb, (-0.78, -1.005, 0.48), (1, 0, 0), (0, 0, 1), 1.56, 0.16, 12, 1, rib_h=0.012, normal=(0, -1, 0))
    objs.append(P.make(mb, "BODY_RearWall_Crossmember", SYS, M["ecoat"], None, (0, -1, -0.2), 0.55, 3,
                       "Estructura de la carrocería", "Travesaño inferior de la pared trasera de la cabina", "R"))
    return objs


# ---------------------------------------------------------------------------
# Anillos de puerta (acero de ultra alta resistencia) y pilares B
# ---------------------------------------------------------------------------
def _side_pt(s, y, z, inset=0.035):
    if z <= S.z_belt(y) + 0.01:
        return (s * (S.hw_body(y, z) - inset), y, z)
    return (s * (S.hw_glass(y, z) - inset * 0.6), y, z)


def door_rings(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        zb = 0.44
        path = []
        # umbral (inferior), pilar C, larguero del techo, pilar A y pilar de bisagras
        for y in (1.17, 0.6, 0.08, -0.5, -0.90):
            path.append(_side_pt(s, y, zb))
        for z in (0.70, 1.00, S.z_belt(-0.90)):
            path.append(_side_pt(s, -0.90, z))
        for y in (-0.88, -0.5, 0.08, 0.5, 0.9, 1.3, 1.70):
            path.append(_side_pt(s, y, S.z_top(y) - 0.045 if y < 1.0 else min(S.z_top(y) - 0.045,
                                                                                    S.z_belt(y) + 0.6)))
        for (y, z) in ((1.80, S.z_belt(1.80) + 0.05), (1.17, S.z_belt(1.17)), (1.17, 0.80)):
            path.append(_side_pt(s, y, z))
        path.append(path[0])
        prof = P.rect_profile(0.055, 0.040, 0.008, 2)
        P.sweep(mb, path, prof, closed_path=False)
        # pilar B
        bp = [_side_pt(s, 0.08, z) for z in (zb, 0.8, 1.1, S.z_belt(0.08), S.z_belt(0.08) + 0.25, S.z_top(0.08) - 0.05)]
        P.sweep(mb, bp, P.rect_profile(0.075, 0.045, 0.008, 2))
        side = "derecho" if s > 0 else "izquierdo"
        objs.append(P.make(mb, f"BODY_DoorRing_{sd}", SYS, M["ecoat"], None, (s, 0, 0.15), 0.55, 3,
                           "Estructura de la carrocería",
                           f"Anillo de puertas {side} de acero de ultra alta resistencia (pilares A, B y C)", "R",
                           smooth=30))
    return objs


# ---------------------------------------------------------------------------
# Caja: «mast» fundido superior, torres del portón; vigas de impacto
# ---------------------------------------------------------------------------
def bed_structure(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        mb = L.MeshBuilder()
        path = []
        for y in (-1.00, -1.40, -1.80, -2.20, -2.60, -2.78):
            z = S.z_top(y) - 0.115
            path.append((s * (S.hw_side(y, z) - 0.042), y, z))
        P.sweep(mb, path, P.rect_profile(0.045, 0.07, 0.006, 2))
        for y in (-1.25, -1.95, -2.55):
            z = S.z_top(y) - 0.15
            x = s * (S.hw_side(y, z) - 0.042)
            P.cyl(mb, (x, y, z), (x, y, z - 0.09), 0.022, 14, 0, r1=0.014)
        objs.append(P.make(mb, f"BODY_Mast_{sd}", SYS, M["alu_cast"], None, (s, 0, 0.6), 0.65, 3,
                           "Estructura de la carrocería", f"«Mast» fundido {side}: larguero superior de la caja", "R"))
        mb = L.MeshBuilder()
        # termina bajo el «mast» y bajo el lateral superior de la caja (z 1,19)
        P.rbox(mb, (s * 0.855, -2.75, 0.955), (0.04, 0.09, 0.47), 0.006, 1, None, 0)
        rib_grid(mb, (s * 0.835, -2.79, 0.74), (0, 1, 0), (0, 0, 1), 0.08, 0.44, 1, 6, rib_h=0.010, normal=(-s, 0, 0))
        objs.append(P.make(mb, f"BODY_Tailgate_Tower_{sd}", SYS, M["alu_cast"], None, (s, -0.5, 0), 0.55, 3,
                           "Estructura de la carrocería", f"Torre fundida del portón {side} (bisagra y cierre)", "R"))
    # viga de impacto delantera con absorbedores
    mb = L.MeshBuilder()
    pts = [(-0.66, 2.52, 0.56), (-0.40, 2.575, 0.56), (0.0, 2.585, 0.56), (0.40, 2.575, 0.56), (0.66, 2.52, 0.56)]
    P.sweep(mb, P.catmull(pts, 5), P.rect_profile(0.05, 0.12, 0.006, 2), up=(0, 0, 1))
    for s in (1, -1):
        P.rbox(mb, (s * 0.53, 2.475, 0.54), (0.08, 0.10, 0.10), 0.008, 1, None, 0)
        for dx in (-0.05, 0.05):
            for dz in (-0.06, 0.06):
                P.hex_nut(mb, (s * 0.53 + dx, 2.426, 0.54 + dz), (0, -1, 0), 0.008, 1)
    objs.append(P.make(mb, "BODY_Front_Bumper_Beam", SYS, [M["alu_machined"], M["zinc"]], None, (0, 1, 0), 0.9, 3,
                       "Estructura de la carrocería",
                       "Viga de impacto delantera con absorbedores (4 tuercas a 30 N·m)", "V"))
    mb = L.MeshBuilder()
    for s in (1, -1):
        P.hull(mb, box_pts((s * 0.525, -2.79, 0.54), (0.12, 0.01, 0.16)) +
               box_pts((s * 0.56, -2.90, 0.55), (0.20, 0.01, 0.14)), 0)
        rib_grid(mb, (s * 0.46, -2.905, 0.48), (1, 0, 0), (0, 0, 1), 0.20, 0.14, 2, 2, rib_h=0.010, normal=(0, -1, 0))
    objs.append(P.make(mb, "BODY_Rear_Energy_Absorbers", SYS, M["alu_cast"], None, (0, -1, 0), 0.75, 3,
                       "Estructura de la carrocería", "Absorbedores de impacto traseros fundidos (izquierdo y derecho)", "V"))
    # Megabeam: travesaño delantero que soporta compresor de A/C y Supermanifold
    mb = L.MeshBuilder()
    P.rbox(mb, (0, 1.69, 0.70), (1.0, 0.05, 0.10), 0.008, 1, None, 0)
    for s in (1, -1):
        P.hull(mb, box_pts((s * 0.50, 1.69, 0.70), (0.01, 0.05, 0.10)) + box_pts((s * 0.47, 1.75, 0.62), (0.03, 0.08, 0.04)), 0)
    rib_grid(mb, (-0.48, 1.715, 0.655), (1, 0, 0), (0, 0, 1), 0.96, 0.09, 8, 1, rib_h=0.010, normal=(0, 1, 0))
    objs.append(P.make(mb, "BODY_Megabeam", SYS, M["alu_cast"], None, (0, 0.6, 0.6), 0.85, 3,
                       "Estructura de la carrocería", "Megabeam: travesaño delantero de equipos térmicos", "V"))
    # viga transversal del salpicadero (Supercarrier) con patas y soporte de la columna
    mb = L.MeshBuilder()
    # tramo central (por encima de la columna de dirección, que cuelga de él) y extremos acodados hacia los
    # pilares A, terminados en sus soportes por delante del larguero del guardabarros (y = 1,20)
    P.cyl(mb, (-0.66, 1.07, 0.985), (0.66, 1.07, 0.985), 0.032, 24, 0)
    for sg in (1, -1):
        P.hose(mb, [(sg * 0.64, 1.07, 0.985), (sg * 0.69, 1.10, 0.985), (sg * 0.72, 1.16, 0.985),
                    (sg * 0.74, 1.20, 0.985)], 0.032, 24, 4, 0, True, None)
    # patas al túnel (x ±0,12), por dentro de los conductos de los pies del climatizador
    for x in (-0.15, 0.15):
        P.beam(mb, (x, 1.07, 0.955), (x * 0.8, 1.02, 0.52), 0.05, 0.025, r=0.004)
    # abrazadera de la columna entre el tubo y el actuador de realimentación: cuña cuya base sigue la generatriz
    # superior del actuador (columna inclinada (0, 1, -0,42), r 48 mm; build_interior_detail) y cuya cara superior
    # se une al tubo
    P.hull(mb, [V(x, y, z) for x in (-0.46, -0.32) for (y, z) in ((1.032, 0.951), (1.08, 0.928), (1.032, 0.966),
                                                                     (1.08, 0.966))], 0)
    for x in (-0.745, 0.745):
        P.disc(mb, (x, 1.20, 0.985), (1, 0, 0), 0.06, 0.006, 20, 0, 0.002)
    objs.append(P.make(mb, "BODY_IP_CrossCar_Beam", SYS, M["steel_black"], None, (0, -0.4, 0.6), 0.55, 3,
                       "Estructura de la carrocería",
                       "Viga transversal del salpicadero (Supercarrier) con soporte de la columna", "R"))
    return objs


def rivets(M):
    """Remaches flow-form (Ø 8 mm) y autoperforantes en las uniones umbral / piezas fundidas."""
    mb = L.MeshBuilder()
    n = 0
    for s in (1, -1):
        for i in range(24):
            y = 1.20 - i * 0.095
            P.rivet(mb, (s * 0.870, y, 0.410), (0, 0, 1), 0.008, 0)
            n += 1
        for i in range(6):
            P.rivet(mb, (s * 0.815, 1.20 - i * 0.03, 0.30 + i * 0.02), (-s, 0, 0), 0.008, 0)
            P.rivet(mb, (s * 0.815, -0.98 - i * 0.03, 0.30 + i * 0.03), (-s, 0, 0), 0.008, 0)
            n += 2
    o = P.make(mb, "BODY_Rivets_FlowForm", SYS, M["zinc"], None, (0, 0, -1), 0.3, 6, "Tornillería",
               f"Remaches flow-form y autoperforantes ({n} uds.) en las uniones de umbrales y piezas fundidas", "R")
    return [o]


def build_all(M):
    out = []
    out += front_underbody(M)
    out += rear_underbody(M)
    out += sills_and_floor(M)
    out += door_rings(M)
    out += bed_structure(M)
    out += rivets(M)
    return [o for o in out if o is not None]
