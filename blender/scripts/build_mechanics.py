"""Mecánica detallada del Cyberbeast: suspensión, dirección por cable, unidades motrices, semiejes,
batería estructural, subchasis, refrigeración, frenos hidráulicos, aire comprimido, baja tensión y bajos.

Fuentes (ver docs/research-and-fidelity.md §8):
  [V] Manual de servicio de Cybertruck: denominación y número de fijaciones de cada pieza
      (p. ej. módulo de muelle neumático delantero: 3 tuercas superiores de 18 mm a 105 N·m y
      2 tornillos al brazo inferior a 140 N·m; brazo superior: 4 tuercas a la carrocería;
      actuador de dirección delantero: 2 tornillos al subchasis a 175 N·m y 4 conectores;
      actuador trasero: 4 tornillos a 120 N·m; buje: 4 tornillos a 105 N·m).
  [V] Manual de servicio, «Wheel Alignment»: caída delantera −0,50°, trasera −1,00°,
      avance 3,60°; vía delantera 1.777 mm y trasera 1.772 mm en el centro de rueda.
  [V] Munro & Associates (vía The Autopian): unidad trasera con dos motores de inducción idénticos,
      cada uno con su inversor en la parte posterior y dos refrigeradores de placa encima;
      reductoras desplazadas hacia atrás para acercar las salidas; unidad delantera de imanes
      permanentes con el inversor integrado al final de la reductora; brazo inferior trasero
      soldado; estabilizadora trasera sujeta con abrazaderas de banda sobre aislantes de goma.
  [V] Batería (Munro vía The Autopian): 4 bloques de 7 x 48 celdas 4680 (1.344), sin módulos
      reemplazables, espuma estructural verde, lámina de mica sobre las celdas, refrigerador en
      serpentín entre hileras, canal de desgasificación inferior de ~33 mm y respiradero de un uso.
  [R]/[A] Formas de carcasas, brazos y soportes: reconstrucciones coherentes con los puntos de
      anclaje, el centro de rueda y los espacios libres; no son geometría OEM.
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_lib as L
import ct_parts as P

WZ = S.WHEEL_CENTER_Z
FLOOR_Z = 0.505


def V(*a):
    return Vector(a)


# ---------------------------------------------------------------------------
# Geometría de cada esquina (puntos duros)
# ---------------------------------------------------------------------------
def hardpoints(axle, s):
    y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
    f = 1 if axle == "F" else -1
    hp = {
        "y": y, "f": f, "s": s,
        "hub": V(s * S.X_WHEEL, y, WZ),
        "bearing": V(s * 0.848, y, WZ),
        "lbj": V(s * 0.795, y, 0.262),
        "ubj": V(s * 0.770, y - f * 0.02, 0.665),
        "tie_out": V(s * 0.790, y - f * 0.165, 0.420),
        "tie_in": V(s * 0.335, y - f * 0.17, 0.425),
        "lca_f": V(s * 0.360, y + f * 0.32, 0.315),
        "lca_r": V(s * 0.360, y - f * 0.18, 0.315),
        "uca_f": V(s * 0.500, y + f * 0.38, 0.705),
        "uca_r": V(s * 0.500, y - f * 0.20, 0.705),
        "spr_bot": V(s * (0.640 if axle == "F" else 0.630), y + f * 0.10, 0.300),
        "spr_top": V(s * (0.585 if axle == "F" else 0.605), y + f * 0.10, 0.960 if axle == "F" else 0.820),
        "stab_low": V(s * 0.620, y - f * 0.05, 0.288),
        "stab_up": V(s * 0.620, y - f * 0.05, 0.395),
    }
    return hp


def _lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------------------
# Suspensión de doble horquilla
# ---------------------------------------------------------------------------
def knuckle(M, hp, name, sysname, parent):
    """Portamangueta de aluminio fundido: alojamiento del rodamiento, cuello alto hasta la rótula
    superior, brazo de dirección, orejetas de la pinza y soporte del sensor de velocidad."""
    s, f = hp["s"], hp["f"]
    mb = L.MeshBuilder()
    b = hp["bearing"]
    # alojamiento del rodamiento (brida de 4 tornillos)
    P.tube_ring(mb, b, (1, 0, 0), 0.050, 0.082, 0.048, 32, 0)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        c = b + V(s * 0.026, 0, 0) + V(0, math.cos(a), math.sin(a)) * 0.072
        P.flange_bolt(mb, c, (s, 0, 0), 0.012, 1)
    # cuello superior (dos tramos convexos) hacia la rótula superior
    ub, lb = hp["ubj"], hp["lbj"]
    neck0 = b + V(-s * 0.012, 0, 0.06)
    neck1 = _lerp(neck0, ub, 0.55) + V(-s * 0.02, 0, 0)
    for (p0, p1, w0, w1) in ((neck0, neck1, 0.050, 0.038), (neck1, ub + V(0, 0, -0.02), 0.038, 0.030)):
        pts = []
        for p, w in ((p0, w0), (p1, w1)):
            for dx in (-1, 1):
                for dy in (-1, 1):
                    pts.append(p + V(dx * 0.022, dy * w, 0))
        P.hull(mb, pts, 0)
    # brazo inferior hacia la rótula inferior
    pts = []
    for p, w in ((b + V(-s * 0.01, 0, -0.05), 0.052), (lb + V(0, 0, 0.025), 0.034)):
        for dx in (-1, 1):
            for dy in (-1, 1):
                pts.append(p + V(dx * 0.024, dy * w, 0))
    P.hull(mb, pts, 0)
    # brazo de dirección hacia la rótula de la bieleta
    t = hp["tie_out"]
    pts = []
    for p, w in ((b + V(-s * 0.02, -f * 0.04, -0.01), 0.030), (t + V(0, 0, 0.012), 0.020)):
        for dx in (-1, 1):
            for dz in (-1, 1):
                pts.append(p + V(dx * 0.018, 0, dz * w))
    P.hull(mb, pts, 0)
    # orejetas de la pinza (radiales, detrás/delante del eje según el eje)
    ang = math.radians(150 if hp["f"] > 0 else 30)
    for d in (-0.35, 0.35):
        a = ang + d
        cdir = V(0, math.cos(a), math.sin(a))      # misma orientación en ambos lados (ver build_wheels)
        c = b + V(s * 0.012, 0, 0) + cdir * 0.118
        P.hull(mb, P.corner_points(c, (0.030, 0.040, 0.040), 0.006, 1) + [tuple(b + cdir * 0.07)], 0)
    o = P.make(mb, name, sysname, [M["alu_cast"], M["zinc"]], parent, (s, 0, 0.25), 0.35, 6, "Suspensión",
               "Portamangueta de aluminio fundido (rodamiento, rótulas, brazo de dirección, orejetas de pinza)", "R",
               bevel=0.003)
    return o


def control_arm_lower(M, hp, name, sysname, parent, rear=False):
    """Brazo inferior en A: dos brazos de sección en I, alma central nervada, casquillos y rótula."""
    s, f = hp["s"], hp["f"]
    mb = L.MeshBuilder()
    lbj = hp["lbj"]
    for piv in (hp["lca_f"], hp["lca_r"]):
        a = piv + V(s * 0.03, 0, 0)
        b = lbj + V(-s * 0.03, 0, 0.004)
        P.beam(mb, a, b, 0.046, 0.038, up=(0, 0, 1), r=0.008)
        # alas superior e inferior de la sección en I (realzan la forma forjada/soldada)
        for dz in (0.019, -0.019):
            P.beam(mb, a + V(0, 0, dz), b + V(0, 0, dz), 0.060, 0.006, up=(0, 0, 1))
    # alma triangular con nervaduras (une los dos brazos cerca de la rótula)
    pf = _lerp(hp["lca_f"], lbj, 0.45)
    pr = _lerp(hp["lca_r"], lbj, 0.45)
    P.hull(mb, [pf + V(0, 0, 0.008), pr + V(0, 0, 0.008), lbj + V(-s * 0.04, 0, 0.008),
                pf + V(0, 0, -0.004), pr + V(0, 0, -0.004), lbj + V(-s * 0.04, 0, -0.004)], 0)
    P.beam(mb, _lerp(pf, lbj, 0.1), _lerp(pr, lbj, 0.1), 0.012, 0.028, up=(0, 0, 1))
    # soporte del módulo de muelle (horquilla con dos tornillos de 21 mm) y de la bieleta
    sb = hp["spr_bot"]
    P.rbox(mb, sb + V(0, 0, -0.012), (0.075, 0.07, 0.030), 0.006, 1, None, 0)
    for dy in (-0.028, 0.028):
        P.flange_bolt(mb, sb + V(s * 0.04, dy, -0.004), (s, 0, 0), 0.014, 2)
    P.rbox(mb, hp["stab_low"] + V(0, 0, -0.008), (0.03, 0.04, 0.026), 0.004, 1, None, 0)
    # casquillos interiores (manguito de acero + goma) y tornillos de 24 mm al subchasis
    for piv in (hp["lca_f"], hp["lca_r"]):
        P.tube_ring(mb, piv, (0, 1, 0), 0.018, 0.034, 0.060, 20, 0)
        P.tube_ring(mb, piv, (0, 1, 0), 0.010, 0.018, 0.070, 16, 1)
        P.flange_bolt(mb, piv + V(0, 0.036 * (1 if piv.y > lbj.y else -1), 0), (0, 1 if piv.y > lbj.y else -1, 0),
                      0.016, 2)
    # rótula inferior
    P.ball_joint(mb, lbj, (0, 0, 1), 0.024, 0, 1)
    label = ("Brazo inferior trasero soldado (4 tornillos de 21 mm a 185 N·m)" if rear
             else "Brazo inferior delantero con rótula (tornillos de 24 mm al subchasis)")
    return P.make(mb, name, sysname, [M["alu_forged"], M["bushing"], M["zinc"]], parent, (s, 0, -0.6), 0.32, 6,
                  "Suspensión", label, "R", bevel=0.002)


def control_arm_upper(M, hp, name, sysname, parent):
    s = hp["s"]
    mb = L.MeshBuilder()
    ubj = hp["ubj"]
    for piv in (hp["uca_f"], hp["uca_r"]):
        P.beam(mb, piv + V(s * 0.02, 0, 0), ubj + V(-s * 0.025, 0, 0.005), 0.032, 0.030, up=(0, 0, 1), r=0.007)
        P.tube_ring(mb, piv, (0, 1, 0), 0.016, 0.028, 0.050, 18, 0)
        P.tube_ring(mb, piv, (0, 1, 0), 0.009, 0.016, 0.058, 14, 1)
        # soporte atornillado a la carrocería (2 tuercas de 15 mm por soporte)
        P.rbox(mb, piv + V(-s * 0.035, 0, 0.0), (0.016, 0.075, 0.07), 0.003, 1, None, 0)
        for dz in (-0.022, 0.022):
            P.hex_nut(mb, piv + V(-s * 0.045, 0, dz), (-s, 0, 0), 0.010, 2)
    P.beam(mb, _lerp(hp["uca_f"], ubj, 0.55), _lerp(hp["uca_r"], ubj, 0.55), 0.020, 0.018, up=(0, 0, 1), r=0.004)
    P.ball_joint(mb, ubj, (0, 0, -1), 0.020, 0, 1)
    return P.make(mb, name, sysname, [M["alu_forged"], M["bushing"], M["zinc"]], parent, (s, 0, 0.7), 0.30, 6,
                  "Suspensión", "Brazo superior en A (4 tuercas a la carrocería, rótula a 80 N·m)", "R", bevel=0.002)


def air_spring(M, hp, prefix, sysname, parent, rear=False):
    """Módulo de muelle neumático coaxial con amortiguador adaptativo, separado en sus piezas."""
    s = hp["s"]
    bot, top = hp["spr_bot"], hp["spr_top"]
    ax = (top - bot).normalized()
    ln = (top - bot).length
    asm = L.assembly(f"{prefix}_AirSpring", sysname, tuple(bot + ax * ln * 0.5), parent=parent)
    L.explode(asm, (s * 0.3, 0, 1), 0.55, 4, "Suspensión",
              "Módulo de muelle neumático (3 tuercas superiores; 2 tornillos al brazo inferior)", "V")
    objs = []
    # cuerpo del amortiguador monotubo con ojo inferior y válvula de amortiguación variable
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.0, -0.010), (0.022, -0.010), (0.030, 0.020), (0.030, ln * 0.50), (0.034, ln * 0.52),
                 (0.034, ln * 0.55), (0.0, ln * 0.55)], tuple(bot), tuple(ax), 24, 0)
    P.tube_ring(mb, bot + V(0, 0, -0.004), (0, 1, 0), 0.010, 0.026, 0.050, 18, 0)
    P.rbox(mb, bot + ax * 0.12 + V(s * 0.036, 0, 0), (0.030, 0.034, 0.05), 0.005, 1, None, 1)
    objs.append(P.make(mb, f"{prefix}_Damper", sysname, [M["steel_black"], M["connector_grey"]], asm,
                       (s * 0.2, 0, -1), 0.25, 6, "Suspensión", "Amortiguador adaptativo (CDC) monotubo", "R"))
    # vástago cromado y fuelle guardapolvos
    mb = L.MeshBuilder()
    P.cyl(mb, bot + ax * ln * 0.55, bot + ax * ln * 0.80, 0.011, 14, 0)
    objs.append(P.make(mb, f"{prefix}_Damper_Rod", sysname, M["chrome"], asm, (s * 0.2, 0, -1), 0.12, 6,
                       "Suspensión", "Vástago del amortiguador", "R"))
    # fuelle de goma de lóbulo enrollable sobre pistón de aluminio
    mb = L.MeshBuilder()
    r_bag = 0.080 if not rear else 0.075
    a0 = ln * (0.48 if not rear else 0.44)
    prof = [(0.040, a0), (0.046, a0 + 0.01), (0.050, a0 + 0.06), (r_bag * 0.94, a0 + 0.08),
            (r_bag, a0 + 0.13), (r_bag * 0.98, a0 + 0.20), (r_bag * 0.90, ln * 0.92), (0.066, ln * 0.95)]
    L.lathe(mb, prof, tuple(bot), tuple(ax), 32, 0)
    objs.append(P.make(mb, f"{prefix}_AirBag", sysname, M["bushing"], asm, (s * 0.6, 0, 0.3), 0.18, 6,
                       "Suspensión", "Fuelle neumático de lóbulo enrollable", "R"))
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.034, a0 - 0.05), (0.044, a0 - 0.05), (0.046, a0 + 0.02), (0.040, a0 + 0.04), (0.034, a0 + 0.04)],
            tuple(bot), tuple(ax), 28, 0, closed_profile=True)
    objs.append(P.make(mb, f"{prefix}_Piston", sysname, M["alu_machined"], asm, (s * 0.2, 0, -1), 0.18, 6,
                       "Suspensión", "Pistón de rodadura de aluminio", "R"))
    # copela superior con tres espárragos y tuercas (18 mm, 105 N·m), conector y racor de aire
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.0, ln * 0.94), (0.070, ln * 0.94), (0.074, ln * 0.97), (0.060, ln), (0.0, ln)],
            tuple(bot), tuple(ax), 32, 0)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.3
        u, v, _ = L.frame_from_axis(ax)
        c = top + (u * math.cos(a) + v * math.sin(a)) * 0.050
        P.hex_nut(mb, c, ax, 0.012, 1)
    P.cyl(mb, top + ax * 0.0 + V(s * 0.04, 0, -0.01), top + V(s * 0.065, 0, -0.01), 0.006, 10, 1)
    objs.append(P.make(mb, f"{prefix}_TopMount", sysname, [M["alu_cast"], M["zinc"]], asm, (s * 0.1, 0, 1), 0.20, 6,
                       "Suspensión", "Copela superior con 3 espárragos, racor de aire y conector", "R"))
    return [asm] + objs


def build_corner(M, axle, s):
    hp = hardpoints(axle, s)
    sd = "R" if s > 0 else "L"
    tag = f"{axle}{sd}"
    sysname = "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION"
    side = "derecha" if s > 0 else "izquierda"
    asm = L.assembly(f"SUSP_{tag}", sysname, (s * 0.65, hp["y"], WZ))
    L.explode(asm, (s, 0.0, 0.0), 0.55, 4, "Suspensión",
              f"Suspensión {'delantera' if axle == 'F' else 'trasera'} {side}", "R")
    objs = [asm]
    objs.append(knuckle(M, hp, f"SUS_{tag}_Knuckle", sysname, asm))
    objs.append(control_arm_lower(M, hp, f"SUS_{tag}_LowerArm", sysname, asm, rear=(axle == "R")))
    objs.append(control_arm_upper(M, hp, f"SUS_{tag}_UpperArm", sysname, asm))
    objs += air_spring(M, hp, f"SUS_{tag}", sysname, asm, rear=(axle == "R"))
    # bieleta de la estabilizadora con rótulas en ambos extremos
    mb = L.MeshBuilder()
    P.cyl(mb, hp["stab_low"] + V(0, 0, 0.012), hp["stab_up"] - V(0, 0, 0.012), 0.008, 12, 0)
    for p, d in ((hp["stab_low"], 1), (hp["stab_up"], -1)):
        P.disc(mb, p, (1, 0, 0), 0.016, 0.026, 16, 0, 0.003)
        P.hex_nut(mb, p + V(s * 0.013, 0, 0), (s, 0, 0), 0.010, 1)
    objs.append(P.make(mb, f"SUS_{tag}_StabLink", sysname, [M["steel_black"], M["zinc"]], asm, (s, 0, 0.3),
                       0.35, 6, "Suspensión", "Bieleta de la barra estabilizadora (275 N·m)", "V"))
    # bieleta de dirección o de convergencia con rótula exterior
    mb = L.MeshBuilder()
    ti, to = hp["tie_in"], hp["tie_out"]
    P.cyl(mb, ti, to - (to - ti).normalized() * 0.035, 0.0115, 14, 0)
    P.hex_nut(mb, _lerp(ti, to, 0.7), (to - ti).normalized(), 0.016, 0, stud=0)
    P.ball_joint(mb, to, (0, 0, -1), 0.018, 0, 1)
    rear = axle == "R"
    objs.append(P.make(mb, f"STR_{tag}_TieRod", "STEERING", [M["zinc"], M["bushing"]], asm,
                       (s, hp["f"] * -0.3, 0), 0.40, 6, "Dirección",
                       "Bieleta de convergencia trasera (170/180 N·m)" if rear
                       else "Bieleta de dirección exterior (170 N·m al portamangueta)", "V"))
    # sensor de velocidad de rueda (1 tornillo Torx T30, 8 N·m) con su cable
    mb = L.MeshBuilder()
    b = hp["bearing"]
    c = b + V(-s * 0.035, -hp["f"] * 0.03, 0.058)
    P.cyl(mb, c, c + V(-s * 0.03, 0, 0.0), 0.009, 12, 0)
    P.rbox(mb, c + V(-s * 0.02, 0, 0.012), (0.012, 0.03, 0.012), 0.003, 1, None, 0)
    P.hose(mb, [c + V(-s * 0.03, 0, 0), c + V(-s * 0.06, 0, 0.06), hp["ubj"] + V(-s * 0.06, 0, -0.08),
                hp["uca_r"] + V(0, 0, -0.04)], 0.0035, 8, 5, 1)
    objs.append(P.make(mb, f"SUS_{tag}_WheelSpeedSensor", sysname, [M["connector_grey"], M["harness"]], asm,
                       (s * 0.3, 0, 0.6), 0.25, 6, "Frenos", "Sensor de velocidad de rueda (ABS) y cable", "V"))
    # latiguillo de freno: del portamangueta al tubo rígido de la carrocería
    mb = L.MeshBuilder()
    cp = b + V(-s * 0.03, -hp["f"] * 0.10, 0.10)
    P.hose(mb, [cp, cp + V(-s * 0.05, 0, 0.10), hp["uca_f"] + V(s * 0.02, -hp["f"] * 0.25, 0.04),
                hp["uca_f"] + V(-s * 0.08, -hp["f"] * 0.28, 0.06)], 0.0055, 10, 5, 0)
    P.flange_bolt(mb, cp, (0, -hp["f"], 0), 0.010, 1)
    objs.append(P.make(mb, f"SUS_{tag}_BrakeHose", sysname, [M["hose"], M["zinc"]], asm, (s * 0.4, 0, 0.6), 0.28, 6,
                       "Frenos", "Latiguillo de freno con tornillo hueco (42 N·m)", "V"))
    return objs


def stabilizer_bar(M, axle):
    """Barra estabilizadora tubular con brazos, casquillos y abrazaderas."""
    y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
    f = 1 if axle == "F" else -1
    sysname = "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION"
    mb = L.MeshBuilder()
    yc = y - f * 0.36
    path = [(-0.620, y - f * 0.05, 0.395), (-0.60, y - f * 0.14, 0.385), (-0.50, yc + f * 0.02, 0.365),
            (-0.40, yc, 0.360), (0.40, yc, 0.360), (0.50, yc + f * 0.02, 0.365), (0.60, y - f * 0.14, 0.385),
            (0.620, y - f * 0.05, 0.395)]
    P.hose(mb, path, 0.0145, 14, 5, 0)
    for x in (-0.40, 0.40):
        P.tube_ring(mb, (x, yc, 0.360), (1, 0, 0), 0.0145, 0.026, 0.045, 18, 1)
        # abrazadera (de banda detrás, de soporte delante)
        if axle == "R":
            P.tube_ring(mb, (x, yc, 0.360), (1, 0, 0), 0.026, 0.030, 0.030, 18, 2)
        else:
            P.hull(mb, P.corner_points((x, yc, 0.375), (0.040, 0.075, 0.010), 0.004, 1), 2)
            for dy in (-0.03, 0.03):
                P.flange_bolt(mb, (x, yc + dy, 0.381), (0, 0, 1), 0.010, 2)
    label = ("Barra estabilizadora trasera (abrazaderas de banda sobre aislantes; 4 tornillos a 50 N·m)" if axle == "R"
             else "Barra estabilizadora delantera con soportes y casquillos")
    return P.make(mb, f"SUS_{axle}_StabilizerBar", sysname, [M["steel_black"], M["bushing"], M["zinc"]], None,
                  (0, -f * 0.4, 0.3), 0.6, 4, "Suspensión", label, "V")


# ---------------------------------------------------------------------------
# Dirección por cable
# ---------------------------------------------------------------------------
def steering_actuator(M, axle):
    """Actuador de dirección: carcasa tubular de aluminio, dos motores eléctricos redundantes,
    electrónica con 4 conectores, fuelles y rótulas axiales."""
    y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
    f = 1 if axle == "F" else -1
    yr, zr = y - f * 0.17, 0.425
    mb = L.MeshBuilder()
    half = 0.27 if axle == "F" else 0.22
    P.cyl(mb, (-half, yr, zr), (half, yr, zr), 0.033, 28, 0)
    for x in (-half, half):
        P.disc(mb, (x, yr, zr), (1, 0, 0), 0.040, 0.018, 28, 0, 0.004)
    # carcasa central del husillo de bolas y dos motores paralelos (redundancia)
    P.hull(mb, P.corner_points((0.06, yr - f * 0.02, zr + 0.01), (0.18, 0.13, 0.12), 0.02, 2), 0)
    for k, dz in enumerate((0.055, -0.035)):
        c0 = V(0.16, yr - f * 0.075, zr + dz)
        P.cyl(mb, c0, c0 + V(0.15, 0, 0), 0.042, 28, 0)
        P.disc(mb, c0 + V(0.15, 0, 0), (1, 0, 0), 0.040, 0.012, 28, 0, 0.004)
    # unidad electrónica con aletas y 4 conectores
    P.rbox(mb, (0.20, yr - f * 0.135, zr + 0.01), (0.22, 0.04, 0.13), 0.006, 1, None, 0)
    for i in range(7):
        P.rbox(mb, (0.11 + i * 0.03, yr - f * 0.158, zr + 0.01), (0.006, 0.012, 0.11), 0.002, 1, None, 0)
    for i in range(4):
        P.rbox(mb, (0.12 + i * 0.05, yr - f * 0.115, zr + 0.085), (0.034, 0.03, 0.022), 0.003, 1, None, 3)
    # soportes al subchasis (2 delante a 175 N·m; 4 detrás a 120 N·m)
    xs = (-half + 0.06, 0.02) if axle == "F" else (-half + 0.05, -half + 0.12, half - 0.12, half - 0.05)
    for x in xs:
        P.rbox(mb, (x, yr + f * 0.03, zr - 0.035), (0.05, 0.05, 0.03), 0.006, 1, None, 0)
        P.flange_bolt(mb, (x, yr + f * 0.03, zr - 0.05), (0, 0, -1), 0.014, 2)
    # fuelles y rótulas axiales
    for sg in (1, -1):
        P.boot(mb, (sg * half, yr, zr), (sg * (half + 0.065), yr, zr), 0.030, 0.014, 6, 20, 1)
        P.cyl(mb, (sg * (half + 0.065), yr, zr), (sg * 0.335, yr, zr), 0.011, 12, 2)
    name = f"STR_{axle}_Actuator"
    lbl = ("Actuador de dirección delantero (steer-by-wire, dos motores, 4 conectores)" if axle == "F"
           else "Actuador de dirección trasero (convergencia de las ruedas traseras, 4 tornillos a 120 N·m)")
    return P.make(mb, name, "STEERING", [M["alu_cast"], M["bushing"], M["zinc"], M["connector_grey"]], None,
                  (0, -f, -0.5), 0.75, 4, "Dirección", lbl, "V", bevel=0.002)


# ---------------------------------------------------------------------------
# Unidades motrices
# ---------------------------------------------------------------------------
def _motor_housing(mb, x0, x1, yc, zc, r, mat=0, bolts_mat=1, fins=14):
    """Carcasa de motor eléctrico: cilindro con aletas axiales, tapa trasera atornillada."""
    sg = 1 if x1 > x0 else -1
    P.cyl(mb, (x0, yc, zc), (x1, yc, zc), r, 40, mat)
    for k in range(fins):
        a = 2 * math.pi * k / fins + 0.1
        d = V(0, math.cos(a), math.sin(a))
        c0 = V(x0 + sg * 0.02, yc, zc) + d * (r + 0.006)
        c1 = V(x1 - sg * 0.03, yc, zc) + d * (r + 0.006)
        P.beam(mb, c0, c1, 0.006, 0.014, up=tuple(d))
    P.disc(mb, (x1, yc, zc), (1, 0, 0), r + 0.012, 0.020, 40, mat, 0.005)
    for k in range(8):
        a = 2 * math.pi * k / 8
        c = V(x1 + sg * 0.010, yc + math.cos(a) * (r - 0.004), zc + math.sin(a) * (r - 0.004))
        P.flange_bolt(mb, c, (sg, 0, 0), 0.008, bolts_mat)


def _gear_housing(mb, x0, x1, lobes, mat=0, ribs=6):
    """Carcasa de reductora: envolvente de lóbulos circulares (ejes paralelos a X) con nervios."""
    pts = []
    for (yc, zc, r) in lobes:
        for k in range(16):
            a = 2 * math.pi * k / 16
            for x in (x0, x1):
                pts.append(V(x, yc + math.cos(a) * r, zc + math.sin(a) * r))
    P.hull(mb, pts, mat)
    yc0 = min(l[0] - l[2] for l in lobes)
    yc1 = max(l[0] + l[2] for l in lobes)
    zs = [l[1] for l in lobes]
    for i in range(ribs):
        y = yc0 + (yc1 - yc0) * (i + 0.5) / ribs
        P.rbox(mb, ((x0 + x1) / 2, y, sum(zs) / len(zs)), (abs(x1 - x0) + 0.012, 0.008, 0.16), 0.003, 1, None, mat)


def drive_unit_front(M):
    yf = S.Y_FRONT_AXLE
    asm = L.assembly("DRIVE_UNIT_FRONT", "DRIVE_UNITS", (0.0, yf, WZ))
    L.explode(asm, (0, 0.6, -1), 1.1, 5, "Unidades motrices",
              "Unidad motriz delantera (motor síncrono de imanes permanentes, inversor integrado)", "V")
    objs = [asm]
    ym, zm = yf + 0.20, 0.465
    mb = L.MeshBuilder()
    _motor_housing(mb, 0.0, -0.33, ym, zm, 0.125)
    objs.append(P.make(mb, "DU_F_Motor_Housing", "DRIVE_UNITS", [M["alu_cast"], M["zinc"]], asm, (-1, 0.3, 0), 0.30, 6,
                       "Unidades motrices", "Carcasa del motor de imanes permanentes (estátor de horquillas)", "R"))
    mb = L.MeshBuilder()
    # el cuarto lóbulo envuelve la rueda del eje intermedio (versión 4: interior de la reductora)
    _gear_housing(mb, 0.0, 0.205, [(yf, WZ, 0.115), (ym, zm, 0.105), (yf + 0.08, 0.36, 0.06), (yf + 0.11, 0.40, 0.094)])
    for x in (0.0, 0.205):
        P.disc(mb, (x + (-0.012 if x == 0 else 0.012), yf, WZ), (1, 0, 0), 0.050, 0.022, 28, 0, 0.004)
    for k in range(10):
        a = 2 * math.pi * k / 10
        P.flange_bolt(mb, (0.205 + 0.004, yf + 0.06 + math.cos(a) * 0.15, 0.45 + math.sin(a) * 0.12), (1, 0, 0),
                      0.008, 1)
    objs.append(P.make(mb, "DU_F_Gearbox", "DRIVE_UNITS", [M["alu_cast"], M["zinc"]], asm, (1, 0, 0), 0.25, 6,
                       "Unidades motrices",
                       "Reductora de una velocidad (15,02:1) con diferencial y bloqueo electromagnético", "R"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0.10, yf + 0.10, 0.625), (0.25, 0.34, 0.075), 0.012, 2, None, 0)
    for i in range(9):
        P.rbox(mb, (0.10, yf - 0.04 + i * 0.035, 0.666), (0.22, 0.006, 0.010), 0.002, 1, None, 0)
    P.rbox(mb, (0.20, yf + 0.25, 0.64), (0.07, 0.06, 0.05), 0.006, 1, None, 1)
    P.rbox(mb, (0.02, yf + 0.26, 0.62), (0.06, 0.05, 0.04), 0.005, 1, None, 2)
    for x in (0.0, 0.05):
        P.cyl(mb, (x, yf - 0.07, 0.63), (x, yf - 0.12, 0.63), 0.009, 12, 0)
    objs.append(P.make(mb, "DU_F_Inverter", "DRIVE_UNITS", [M["alu_cast"], M["hv_orange"], M["connector_grey"]], asm,
                       (0, 0, 1), 0.35, 6, "Unidades motrices",
                       "Inversor integrado de la unidad delantera con cabecera de alta tensión", "R"))
    mb = L.MeshBuilder()
    P.rbox(mb, (-0.10, ym + 0.13, 0.36), (0.16, 0.05, 0.10), 0.006, 1, None, 0)
    for i in range(6):
        P.rbox(mb, (-0.10, ym + 0.157, 0.32 + i * 0.016), (0.15, 0.006, 0.006), 0.002, 1, None, 0)
    for x in (-0.15, -0.05):
        P.cyl(mb, (x, ym + 0.15, 0.41), (x, ym + 0.15, 0.45), 0.010, 12, 0)
    objs.append(P.make(mb, "DU_F_HeatExchanger", "DRIVE_UNITS", M["alu_machined"], asm, (0, 1, 0.2), 0.30, 6,
                       "Refrigeración", "Intercambiador aceite-refrigerante de la unidad delantera", "V"))
    mb = L.MeshBuilder()
    P.cyl(mb, (0.15, yf - 0.05, 0.335), (0.15, yf - 0.115, 0.335), 0.030, 24, 0)
    P.rbox(mb, (0.15, yf - 0.08, 0.305), (0.07, 0.05, 0.03), 0.005, 1, None, 1)
    P.cyl(mb, (0.03, yf + 0.04, 0.33), (0.03, yf + 0.04, 0.29), 0.035, 24, 0)
    P.cyl(mb, (0.05, yf + 0.02, 0.58), (0.05, yf + 0.02, 0.64), 0.008, 10, 0)
    objs.append(P.make(mb, "DU_F_OilPump_Filter", "DRIVE_UNITS", [M["alu_cast"], M["connector_grey"]], asm,
                       (0.3, -0.3, -1), 0.30, 6, "Unidades motrices",
                       "Bomba de aceite eléctrica, filtro de aceite y respiradero", "V"))
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.140, -0.02), (0.140, -0.31)], (0.0, ym, zm), (1, 0, 0), 40, 0)
    objs.append(P.make(mb, "DU_F_NVH_Cover", "DRIVE_UNITS", M["harness"], asm, (-1, 0.6, 0.6), 0.45, 6,
                       "Unidades motrices", "Cubierta acústica (NVH) del motor delantero", "V"))
    mb = L.MeshBuilder()
    for p in ((-0.25, ym + 0.02, 0.33), (0.18, yf - 0.02, 0.33), (0.08, yf + 0.30, 0.38)):
        P.tube_ring(mb, p, (0, 1, 0), 0.012, 0.035, 0.045, 18, 0)
        P.rbox(mb, V(*p) + V(0, 0, -0.035), (0.08, 0.06, 0.02), 0.004, 1, None, 1)
    P.hose(mb, [(-0.30, ym, 0.36), (-0.36, ym - 0.05, 0.32), (-0.40, ym - 0.10, 0.31)], 0.006, 6, 4, 2)
    objs.append(P.make(mb, "DU_F_Mounts", "DRIVE_UNITS", [M["bushing"], M["steel_black"], M["copper"]], asm,
                       (0, 0, -1), 0.20, 6, "Unidades motrices", "Soportes elásticos y trenza de masa", "R"))
    return objs


def drive_unit_rear(M):
    yr = S.Y_REAR_AXLE
    asm = L.assembly("DRIVE_UNIT_REAR", "DRIVE_UNITS", (0.0, yr, WZ))
    L.explode(asm, (0, -0.6, -1), 1.15, 5, "Unidades motrices",
              "Unidad motriz trasera tri-motor: dos motores de inducción con vectorización de par", "V")
    objs = [asm]
    ym, zm = yr - 0.19, 0.470
    mb = L.MeshBuilder()
    _gear_housing(mb, -0.165, 0.165, [(yr, WZ, 0.11), (ym, zm, 0.10), (yr - 0.09, 0.36, 0.06), (yr - 0.11, 0.40, 0.094)],
                  ribs=8)
    for x in (-0.165, 0.165):
        P.disc(mb, (x + (0.012 if x > 0 else -0.012), yr, WZ), (1, 0, 0), 0.050, 0.022, 28, 0, 0.004)
    objs.append(P.make(mb, "DU_R_Gearbox", "DRIVE_UNITS", [M["alu_cast"], M["zinc"]], asm, (0, -0.4, -0.2), 0.30, 6,
                       "Unidades motrices",
                       "Carcasa común de las dos reductoras independientes (15,02:1), desplazadas hacia atrás", "R"))
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        mb = L.MeshBuilder()
        _motor_housing(mb, s * 0.165, s * 0.43, ym, zm, 0.118)
        objs.append(P.make(mb, f"DU_R_Motor_{sd}", "DRIVE_UNITS", [M["alu_cast"], M["zinc"]], asm, (s, -0.2, 0),
                           0.32, 6, "Unidades motrices", f"Motor de inducción trasero {side} (rotor de cobre)", "V"))
        mb = L.MeshBuilder()
        # cara delantera a y = ym - 0,130: libre de la carcasa del motor (radio ~0,13 m) en toda su altura
        P.rbox(mb, (s * 0.30, ym - 0.165, 0.575), (0.24, 0.07, 0.17), 0.010, 2, None, 0)
        for i in range(7):
            P.rbox(mb, (s * 0.30, ym - 0.201, 0.505 + i * 0.022), (0.22, 0.008, 0.008), 0.002, 1, None, 0)
        P.rbox(mb, (s * 0.20, ym - 0.165, 0.685), (0.06, 0.06, 0.05), 0.006, 1, None, 1)
        objs.append(P.make(mb, f"DU_R_Inverter_{sd}", "DRIVE_UNITS", [M["alu_cast"], M["hv_orange"]], asm,
                           (s * 0.3, -0.6, 0.6), 0.36, 6, "Unidades motrices",
                           f"Inversor del motor trasero {side} (montado en su parte posterior)", "V"))
        mb = L.MeshBuilder()
        P.rbox(mb, (s * 0.30, ym + 0.02, zm + 0.135), (0.20, 0.14, 0.030), 0.006, 1, None, 0)
        for i in range(8):
            P.rbox(mb, (s * 0.30, ym - 0.04 + i * 0.017, zm + 0.152), (0.19, 0.004, 0.006), 0.001, 1, None, 0)
        for dx in (-0.06, 0.06):
            P.cyl(mb, (s * 0.30 + dx, ym + 0.09, zm + 0.135), (s * 0.30 + dx, ym + 0.14, zm + 0.135), 0.009, 12, 0)
        objs.append(P.make(mb, f"DU_R_PlateCooler_{sd}", "DRIVE_UNITS", M["alu_machined"], asm, (s * 0.2, 0, 1),
                           0.30, 6, "Refrigeración", "Refrigerador de placa aceite-refrigerante sobre el motor", "V"))
    mb = L.MeshBuilder()
    P.cyl(mb, (-0.10, yr + 0.07, 0.34), (-0.10, yr + 0.14, 0.34), 0.030, 24, 0)
    P.rbox(mb, (-0.10, yr + 0.105, 0.31), (0.06, 0.05, 0.03), 0.005, 1, None, 1)
    P.cyl(mb, (0.06, yr + 0.02, 0.33), (0.06, yr + 0.02, 0.29), 0.035, 24, 0)
    objs.append(P.make(mb, "DU_R_OilPump_Filter", "DRIVE_UNITS", [M["alu_cast"], M["connector_grey"]], asm,
                       (0, 0.3, -1), 0.30, 6, "Unidades motrices", "Bomba de aceite (LH, tri-motor) y filtro", "V"))
    mb = L.MeshBuilder()
    # soportes laterales por fuera de las tapas de los motores (|x| > 0,447)
    for p in ((-0.475, ym - 0.05, 0.36), (0.475, ym - 0.05, 0.36), (0.0, yr + 0.12, 0.40)):
        P.tube_ring(mb, p, (0, 1, 0), 0.012, 0.035, 0.045, 18, 0)
        P.rbox(mb, V(*p) + V(0, 0, -0.035), (0.08, 0.06, 0.02), 0.004, 1, None, 1)
    P.hose(mb, [(0.40, ym, 0.40), (0.46, ym + 0.05, 0.37), (0.50, ym + 0.12, 0.36)], 0.006, 6, 4, 2)
    objs.append(P.make(mb, "DU_R_Mounts", "DRIVE_UNITS", [M["bushing"], M["steel_black"], M["copper"]], asm,
                       (0, 0, -1), 0.20, 6, "Unidades motrices", "Soportes de la unidad trasera y trenza de masa", "R"))
    return objs


def halfshafts(M):
    objs = []
    for axle, y, x_in in (("F", S.Y_FRONT_AXLE, {1: 0.230, -1: -0.035}), ("R", S.Y_REAR_AXLE, {1: 0.190, -1: -0.190})):
        for s, sd in ((1, "R"), (-1, "L")):
            mb = L.MeshBuilder()
            xi, xo = x_in[s], s * 0.835
            P.cyl(mb, (xi, y, WZ), (xi + s * 0.075, y, WZ), 0.047, 24, 0)
            P.boot(mb, (xi + s * 0.075, y, WZ), (xi + s * 0.165, y, WZ), 0.044, 0.016, 6, 20, 1)
            P.cyl(mb, (xi + s * 0.16, y, WZ), (xo - s * 0.15, y, WZ), 0.0155, 16, 0)
            P.boot(mb, (xo - s * 0.155, y, WZ), (xo - s * 0.075, y, WZ), 0.016, 0.040, 5, 20, 1)
            L.lathe(mb, [(0.040, 0.0), (0.046, 0.02), (0.046, 0.05), (0.030, 0.075), (0.020, 0.075)],
                    (xo - s * 0.075, y, WZ), (s, 0, 0), 24, 0)
            where = "delantero" if axle == "F" else "trasero"
            o = P.make(mb, f"DU_Halfshaft_{axle}{sd}", "DRIVE_UNITS", [M["steel_black"], M["bushing"]], None,
                       (s, 0, -0.3), 0.55, 5, "Semiejes",
                       f"Semieje {where} con juntas homocinéticas (tornillo central de 24 mm a 300 N·m)", "R")
            objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Batería estructural (cell-to-pack)
# ---------------------------------------------------------------------------
BAT_Y0, BAT_Y1, BAT_HW, BAT_ZB, BAT_ZT = 1.25, -1.40, 0.80, 0.285, 0.455
COL_PITCH = 0.0490          # separación entre columnas (Ø46 + cinta de refrigeración)
ROW_PITCH = 0.0466          # separación a lo largo de cada columna
BLOCK_X = (-0.555, -0.185, 0.185, 0.555)   # centros de los 4 bloques de 7 columnas


def build_battery(M):
    yc = (BAT_Y0 + BAT_Y1) / 2
    asm = L.assembly("BATTERY_PACK", "BATTERY_ASSEMBLY", (0.0, yc, (BAT_ZB + BAT_ZT) / 2))
    L.explode(asm, (0, 0, -1), 1.35, 5, "Batería",
              "Batería estructural de alta tensión (~123 kWh, 1.344 celdas 4680; 700 V nominales según el manual del propietario, 800 V según la hoja de rescate)", "R")
    objs = [asm]
    ln = BAT_Y0 - BAT_Y1
    # --- bandeja: fondo, paredes y brida perimetral atornillada a los largueros laterales
    mb = L.MeshBuilder()
    P.rbox(mb, (0, yc, BAT_ZB + 0.008), (2 * BAT_HW, ln, 0.016), 0.004, 1, None, 0)
    for sg in (1, -1):
        P.rbox(mb, (sg * (BAT_HW - 0.012), yc, (BAT_ZB + BAT_ZT) / 2), (0.024, ln, BAT_ZT - BAT_ZB), 0.004, 1, None, 0)
        P.rbox(mb, (sg * (BAT_HW + 0.012), yc, BAT_ZT - 0.012), (0.05, ln, 0.012), 0.002, 1, None, 0)
    for yy in (BAT_Y0 - 0.012, BAT_Y1 + 0.012):
        P.rbox(mb, (0, yy, (BAT_ZB + BAT_ZT) / 2), (2 * BAT_HW, 0.024, BAT_ZT - BAT_ZB), 0.004, 1, None, 0)
    # nervios del fondo (canal de desgasificación inferior)
    for i in range(9):
        y = BAT_Y1 + 0.15 + i * (ln - 0.3) / 8
        P.rbox(mb, (0, y, BAT_ZB + 0.020), (2 * BAT_HW - 0.06, 0.012, 0.010), 0.002, 1, None, 0)
    for i in range(22):
        y = BAT_Y1 + 0.06 + i * (ln - 0.12) / 21
        for sg in (1, -1):
            P.flange_bolt(mb, (sg * (BAT_HW + 0.022), y, BAT_ZT - 0.006), (0, 0, 1), 0.010, 1)
    objs.append(P.make(mb, "BAT_Enclosure_Tray", "BATTERY_ASSEMBLY", [M["battery"], M["zinc"]], asm, (0, 0, -1), 0.25, 6,
                       "Batería", "Bandeja estructural con brida perimetral (unos 22 pernos exteriores + 14 interiores + 4 al fundido trasero; el recuento varía según la página del manual)", "R"))
    # --- tapa estructural (suelo del habitáculo): los asientos delanteros se atornillan a ella
    mb = L.MeshBuilder()
    P.rbox(mb, (0, yc, BAT_ZT - 0.006), (2 * BAT_HW - 0.03, ln - 0.03, 0.012), 0.003, 1, None, 0)
    for i in range(12):
        y = BAT_Y1 + 0.12 + i * (ln - 0.24) / 11
        P.rbox(mb, (0, y, BAT_ZT + 0.002), (2 * BAT_HW - 0.12, 0.010, 0.004), 0.001, 1, None, 0)
    for x in (-0.58, -0.22, 0.22, 0.58):
        for y in (0.62, 0.10):
            P.cyl(mb, (x, y, BAT_ZT), (x, y, BAT_ZT + 0.018), 0.016, 14, 1)
    objs.append(P.make(mb, "BAT_Enclosure_Lid", "BATTERY_ASSEMBLY", [M["battery"], M["alu_machined"]], asm, (0, 0, 1),
                       0.55, 6, "Batería",
                       "Tapa estructural (suelo del habitáculo) con anclajes de los asientos delanteros", "R"))
    # --- cuatro bloques de 7 x 48 celdas
    z0 = BAT_ZB + 0.033                 # canal de desgasificación de ~33 mm bajo las celdas
    y_start = yc + (47 * ROW_PITCH) / 2
    for bi, bx in enumerate(BLOCK_X):
        mb = L.MeshBuilder(merge=1e-7)
        for c in range(7):
            x = bx + (c - 3) * COL_PITCH
            off = (ROW_PITCH / 2) if c % 2 else 0.0
            for r in range(48):
                y = y_start - r * ROW_PITCH - off
                L.lathe(mb, [(S.CELL_D / 2, 0.0), (S.CELL_D / 2, S.CELL_H - 0.002), (S.CELL_D / 2 - 0.002, S.CELL_H),
                             (0.0, S.CELL_H)], (x, y, z0), (0, 0, 1), 10, 0)
        objs.append(P.make(mb, f"BAT_Block_{bi + 1}_Cells", "BATTERY_ASSEMBLY", M["cell"], asm,
                           (bx, 0, 0.4), 0.30, 6, "Batería",
                           f"Bloque {bi + 1}: 336 celdas cilíndricas 4680 (7 columnas x 48)", "R",
                           note="Recuento 1.344 verificado (pasaporte); disposición 4 x 7 x 48 según el desmontaje de Munro",
                           smooth=30))
        # espuma estructural verde que inmoviliza las celdas
        mb = L.MeshBuilder()
        P.rbox(mb, (bx, yc - ROW_PITCH / 4, z0 + 0.030), (7 * COL_PITCH + 0.01, 48 * ROW_PITCH + 0.03, 0.058),
               0.004, 1, None, 0)
        objs.append(P.make(mb, f"BAT_Block_{bi + 1}_Foam", "BATTERY_ASSEMBLY", M["foam_green"], asm,
                           (bx, 0, -0.4), 0.18, 6, "Batería", "Espuma estructural que fija las celdas", "V"))
        # refrigeradores en serpentín entre parejas de columnas
        mb = L.MeshBuilder()
        for c in (0, 2, 4):
            xm = bx + (c - 3 + 0.5) * COL_PITCH
            path = []
            for r in range(97):
                y = y_start - r * ROW_PITCH / 2 - ROW_PITCH / 4
                path.append((xm + 0.0045 * math.sin(r * math.pi / 2), y, z0 + 0.040))
            P.sweep(mb, path, P.rect_profile(0.0022, 0.064), mat=0)
        # colectores de refrigerante en los extremos de cada bloque
        for yy in (y_start + 0.04, y_start - 47 * ROW_PITCH - 0.04):
            P.cyl(mb, (bx - 0.17, yy, z0 + 0.05), (bx + 0.17, yy, z0 + 0.05), 0.010, 12, 0)
        objs.append(P.make(mb, f"BAT_Block_{bi + 1}_Coolers", "BATTERY_ASSEMBLY", M["busbar_alu"], asm,
                           (bx, 0, 0.55), 0.24, 6, "Refrigeración",
                           "Refrigeradores en serpentín y colectores del bloque", "V"))
        # barras colectoras sobre las celdas (conexión celda a celda) y lámina de mica
        mb = L.MeshBuilder()
        for c in range(7):
            x = bx + (c - 3) * COL_PITCH
            P.rbox(mb, (x, yc - ROW_PITCH / 4, z0 + S.CELL_H + 0.002), (0.010, 48 * ROW_PITCH, 0.002), 0.0005, 1,
                   None, 0)
        for r in range(0, 48, 6):
            y = y_start - r * ROW_PITCH
            P.rbox(mb, (bx, y, z0 + S.CELL_H + 0.0035), (7 * COL_PITCH, 0.006, 0.0015), 0.0005, 1, None, 0)
        objs.append(P.make(mb, f"BAT_Block_{bi + 1}_Busbars", "BATTERY_ASSEMBLY", M["busbar_alu"], asm,
                           (bx, 0, 1), 0.42, 6, "Batería", "Colectores de corriente sobre las celdas", "R"))
        mb = L.MeshBuilder()
        P.rbox(mb, (bx, yc - ROW_PITCH / 4, z0 + S.CELL_H + 0.008), (7 * COL_PITCH + 0.01, 48 * ROW_PITCH + 0.02, 0.0015),
               0.0005, 1, None, 0)
        objs.append(P.make(mb, f"BAT_Block_{bi + 1}_Mica", "BATTERY_ASSEMBLY", M["mica"], asm, (bx, 0, 1), 0.62, 6,
                           "Batería", "Lámina de mica (barrera térmica) sobre las celdas", "V"))
    # --- vigas longitudinales entre bloques y travesaños extremos
    mb = L.MeshBuilder()
    for x in (-0.37, 0.0, 0.37):
        P.rbox(mb, (x, yc, BAT_ZB + 0.075), (0.022, ln - 0.06, 0.12), 0.003, 1, None, 0)
    objs.append(P.make(mb, "BAT_Internal_Beams", "BATTERY_ASSEMBLY", M["alu_cast"], asm, (0, 0, 0.6), 0.35, 6,
                       "Batería", "Vigas extruidas entre bloques", "R"))
    # --- extremo delantero: cabecera de conectores de AT, pirofusibles, correa delantera, refrigerante
    mb = L.MeshBuilder()
    yf = BAT_Y0 - 0.06
    P.rbox(mb, (0.0, yf, BAT_ZT + 0.03), (0.50, 0.09, 0.06), 0.008, 2, None, 0)
    for x in (-0.12, 0.12):
        P.rbox(mb, (x, yf + 0.055, BAT_ZT + 0.03), (0.07, 0.04, 0.05), 0.006, 1, None, 1)
    objs.append(P.make(mb, "BAT_HV_Header", "BATTERY_ASSEMBLY", [M["battery"], M["hv_orange"]], asm, (0, 0.4, 1), 0.45, 6,
                       "Alta tensión", "Cabecera de conectores de alta tensión (unidad delantera, carga rápida)", "V"))
    mb = L.MeshBuilder()
    for x in (0.30, 0.42):
        P.rbox(mb, (x, yf, BAT_ZT + 0.025), (0.06, 0.05, 0.05), 0.006, 1, None, 0)
        for dx in (-0.02, 0.02):
            P.flange_bolt(mb, (x + dx, yf, BAT_ZT + 0.05), (0, 0, 1), 0.008, 1)
    objs.append(P.make(mb, "BAT_Pyro_Fuses", "BATTERY_ASSEMBLY", [M["hv_orange"], M["zinc"]], asm, (1, 0.3, 1), 0.40, 6,
                       "Alta tensión", "Pirofusibles primario y secundario (2 tornillos cada uno)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0.0, BAT_Y0 + 0.012, BAT_ZB + 0.06), (1.30, 0.02, 0.10), 0.004, 1, None, 0)
    for x in (-0.55, -0.2, 0.2, 0.55):
        P.flange_bolt(mb, (x, BAT_Y0 + 0.022, BAT_ZB + 0.06), (0, 1, 0), 0.012, 1)
    for x in (-0.36, -0.30):
        P.hose(mb, [(x, BAT_Y0 - 0.02, BAT_ZT + 0.02), (x, BAT_Y0 + 0.05, BAT_ZT + 0.04), (x, BAT_Y0 + 0.14, 0.52)],
               0.013, 12, 4, 2)
    objs.append(P.make(mb, "BAT_Chinstrap_Front", "BATTERY_ASSEMBLY", [M["steel_black"], M["zinc"], M["hose"]], asm,
                       (0, 1, 0), 0.30, 6, "Batería", "Correa delantera (chinstrap) y tomas de refrigerante", "V"))
    # --- extremo trasero: respiradero térmico de un solo uso, puertos de inundación y respiradero de presión
    mb = L.MeshBuilder()
    yb = BAT_Y1 - 0.01
    P.rbox(mb, (0.25, yb, BAT_ZB + 0.08), (0.14, 0.03, 0.10), 0.006, 1, None, 0)
    P.rbox(mb, (0.25, yb - 0.02, BAT_ZB + 0.08), (0.12, 0.015, 0.08), 0.005, 1, None, 1)
    for x in (-0.35, -0.15):
        P.cyl(mb, (x, yb, BAT_ZB + 0.08), (x, yb - 0.025, BAT_ZB + 0.08), 0.016, 16, 2)
    P.cyl(mb, (0.55, yb, BAT_ZB + 0.12), (0.55, yb - 0.02, BAT_ZB + 0.12), 0.012, 12, 2)
    objs.append(P.make(mb, "BAT_Thermal_Vent_FloodPorts", "BATTERY_ASSEMBLY",
                       [M["battery"], M["hv_orange"], M["connector_grey"]], asm, (0, -1, 0), 0.30, 6, "Batería",
                       "Respiradero térmico (tapa naranja, apagallamas), puertos de inundación y respiradero", "V"))
    return objs


def build_ancillary_bay(M):
    """Bahía auxiliar bajo el suelo delantero de la caja: caja de conexiones de CA, sistema de
    conversión de potencia (PCS), clúster de dispositivos y barra colectora «last mile»."""
    asm = L.assembly("ANCILLARY_BAY", "BATTERY_ASSEMBLY", (0.0, -1.22, 0.64))
    L.explode(asm, (0, -0.4, 1), 1.0, 5, "Alta tensión",
              "Bahía auxiliar de alta tensión (accesible desde la caja de carga)", "R")
    objs = [asm]
    mb = L.MeshBuilder()
    # entre las paredes interiores de los pasos de rueda traseros (|x| = 0,494 m desde y = -1,262 m)
    P.rbox(mb, (0.0, -1.22, 0.53), (0.96, 0.34, 0.12), 0.01, 2, None, 0)
    objs.append(P.make(mb, "HV_Ancillary_Cover", "BATTERY_ASSEMBLY", M["battery"], asm, (0, 0, 1), 0.55, 6,
                       "Alta tensión", "Cubierta de la bahía auxiliar", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (-0.31, -1.22, 0.63), (0.32, 0.28, 0.08), 0.008, 2, None, 0)
    for i in range(3):
        P.rbox(mb, (-0.42 + i * 0.10, -1.07, 0.64), (0.05, 0.03, 0.04), 0.004, 1, None, 1)
    objs.append(P.make(mb, "HV_AC_Junction_Box", "BATTERY_ASSEMBLY", [M["battery"], M["hv_orange"]], asm,
                       (-1, 0, 1), 0.45, 6, "Alta tensión", "Caja de conexiones de CA (ACJB)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0.295, -1.22, 0.64), (0.35, 0.30, 0.10), 0.008, 2, None, 0)
    for i in range(10):
        P.rbox(mb, (0.295, -1.34 + i * 0.026, 0.693), (0.33, 0.006, 0.008), 0.002, 1, None, 0)
    for x in (0.20, 0.26):
        P.cyl(mb, (x, -1.06, 0.62), (x, -1.03, 0.62), 0.010, 12, 0)
    objs.append(P.make(mb, "HV_Power_Conversion_System", "BATTERY_ASSEMBLY", M["alu_cast"], asm, (1, 0, 1), 0.45, 6,
                       "Alta tensión", "Sistema de conversión de potencia (cargador de a bordo y CC/CC de 48 V)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0.0, -1.30, 0.63), (0.16, 0.12, 0.07), 0.006, 1, None, 0)
    objs.append(P.make(mb, "HV_Device_Cluster", "BATTERY_ASSEMBLY", M["connector_grey"], asm, (0, -1, 1), 0.40, 6,
                       "Alta tensión", "Clúster de dispositivos (contactores y fusibles)", "V"))
    mb = L.MeshBuilder()
    # de la cara exterior de la ACJB al empalme con la barra de la toma de carga (por delante del paso de rueda)
    P.sweep(mb, [(-0.474, -1.15, 0.63), (-0.53, -1.16, 0.64), (-0.58, -1.18, 0.65), (-0.62, -1.20, 0.66)],
            P.rect_profile(0.04, 0.006), mat=0)
    objs.append(P.make(mb, "HV_Last_Mile_Busbar", "BATTERY_ASSEMBLY", M["copper"], asm, (-1, -0.5, 0.5), 0.40, 6,
                       "Alta tensión", "Barra colectora «last mile» hacia la toma de carga", "V"))
    return objs


# ---------------------------------------------------------------------------
# Subchasis delantero y trasero (cuna tri-motor)
# ---------------------------------------------------------------------------
def subframe(M, axle):
    y = S.Y_FRONT_AXLE if axle == "F" else S.Y_REAR_AXLE
    f = 1 if axle == "F" else -1
    mb = L.MeshBuilder()
    z = 0.318
    yf_, yr_ = y + f * 0.44, y - f * 0.46
    # largueros laterales de sección cerrada con soportes en horquilla de los brazos inferiores
    for s in (1, -1):
        P.beam(mb, (s * 0.33, yf_, z), (s * 0.33, yr_, z), 0.075, 0.060, r=0.010)
        for yy in (y + f * 0.32, y - f * 0.18):
            for dy in (-0.036, 0.036):
                P.rbox(mb, (s * 0.37, yy + dy, 0.315), (0.07, 0.008, 0.07), 0.003, 1, None, 0)
        # torres de fijación a la carrocería (4 puntos) con tornillos de 18 mm
        for yy in (yf_ - f * 0.02, yr_ + f * 0.02):
            P.beam(mb, (s * 0.33, yy, z + 0.01), (s * 0.48, yy, z + 0.01), 0.05, 0.05, r=0.008)
            P.cyl(mb, (s * 0.48, yy, z - 0.02), (s * 0.48, yy, 0.458), 0.032, 20, 0)
            P.flange_bolt(mb, (s * 0.48, yy, z - 0.021), (0, 0, -1), 0.014, 1)
    # travesaños delantero y trasero, y diagonales
    for yy in (yf_, yr_):
        P.beam(mb, (-0.33, yy, z), (0.33, yy, z), 0.060, 0.055, r=0.009)
    for s in (1, -1):
        P.beam(mb, (s * 0.33, y - f * 0.05, z - 0.005), (s * 0.08, yr_ + f * 0.02, z - 0.005), 0.040, 0.035, r=0.006)
    # cartelas en las esquinas
    for s in (1, -1):
        for yy in (yf_, yr_):
            P.hull(mb, [(s * 0.33, yy, z + 0.02), (s * 0.24, yy, z + 0.02), (s * 0.33, yy - f * 0.09 * (1 if yy == yf_ else -1), z + 0.02),
                        (s * 0.33, yy, z - 0.02), (s * 0.24, yy, z - 0.02),
                        (s * 0.33, yy - f * 0.09 * (1 if yy == yf_ else -1), z - 0.02)], 0)
    name = f"CHS_Subframe_{axle}"
    lbl = ("Subchasis delantero (AWD): brazos inferiores, actuador de dirección y unidad delantera" if axle == "F"
           else "Subchasis trasero tri-motor: brazos inferiores, actuador trasero y unidad trasera")
    o = P.make(mb, name, "UNDERBODY", [M["steel_black"], M["zinc"]], None, (0, f * 0.3, -1), 0.95, 3, "Subchasis", lbl,
               "R", bevel=0.002)
    return o


def lca_shields(M):
    objs = []
    for axle, y in (("F", S.Y_FRONT_AXLE), ("R", S.Y_REAR_AXLE)):
        for s, sd in ((1, "R"), (-1, "L")):
            hp = hardpoints(axle, s)
            mb = L.MeshBuilder()
            pts = [hp["lca_f"] + V(0, 0, -0.04), hp["lca_r"] + V(0, 0, -0.04), hp["lbj"] + V(-s * 0.05, 0, -0.02)]
            P.prism(mb, [(p.x, p.y) for p in pts], (0, 0, pts[0].z - 0.004), (1, 0, 0), (0, 1, 0), 0.003, (0, 0, 1))
            for p in pts:
                P.flange_bolt(mb, p + V(0, 0, -0.005), (0, 0, -1), 0.008, 1)
            objs.append(P.make(mb, f"SUS_{axle}{sd}_LCA_AeroShield", "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION",
                               [M["plastic_textured"], M["zinc"]], None, (s * 0.3, 0, -1), 0.35, 6, "Bajos",
                               "Deflector aerodinámico del brazo inferior (3 tornillos)", "V"))
    return objs


# ---------------------------------------------------------------------------
# Gestión térmica
# ---------------------------------------------------------------------------
def build_thermal(M):
    objs = []
    asm = L.assembly("THERMAL_FRONT", "UNDERBODY", (0.0, 2.10, 0.65))
    L.explode(asm, (0, 0.8, 0.3), 1.0, 3, "Refrigeración", "Gestión térmica delantera (Supermanifold y CFM)", "R")
    objs.append(asm)
    # Módulo de ventilador de refrigeración (CFM): radiador, depósitos, ventiladores y persianas activas
    mb = L.MeshBuilder()
    yc, zc = 2.43, 0.565
    # entre los soportes de la viga del paragolpes (|x| >= 0,46)
    P.rbox(mb, (0, yc, zc), (0.79, 0.032, 0.27), 0.004, 1, None, 0)
    for sg in (1, -1):
        P.rbox(mb, (sg * 0.42, yc, zc), (0.05, 0.05, 0.29), 0.008, 1, None, 1)
    objs.append(P.make(mb, "CHS_Radiator", "UNDERBODY", [M["radiator"], M["plastic_black"]], asm, (0, 1, 0), 0.6, 6,
                       "Refrigeración", "Radiador de baja temperatura con depósitos laterales", "R"))
    mb = L.MeshBuilder()
    # carcasa del módulo; los rotores (hélices, cubos y motores) son CHS_Cooling_Fans (build_v4_energia), detrás
    P.rbox(mb, (0, yc - 0.045, zc), (0.82, 0.05, 0.30), 0.01, 1, None, 0)
    objs.append(P.make(mb, "CHS_Cooling_Fan_Module", "UNDERBODY", [M["plastic_black"], M["connector_grey"]], asm,
                       (0, -0.2, 1), 0.45, 6, "Refrigeración",
                       "Carcasa del módulo de ventiladores (CFM, 6 tornillos de 10 Nm)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0, yc + 0.07, zc - 0.02), (0.90, 0.02, 0.22), 0.004, 1, None, 0)
    for i in range(7):
        z = zc - 0.115 + i * 0.032
        P.beam(mb, (-0.43, yc + 0.085, z), (0.43, yc + 0.085, z), 0.028, 0.003, up=(0, 0.5, 1))
    objs.append(P.make(mb, "CHS_Active_Grille_Shutter", "UNDERBODY", M["plastic_black"], asm, (0, 1, -0.2), 0.75, 6,
                       "Refrigeración", "Persianas activas de la rejilla (número de lamas no publicado; 12 pestañas de bloqueo + 2 clips)", "R"))
    # Supermanifold con Octovalve, bombas, enfriador, condensador refrigerado por líquido y botella
    mb = L.MeshBuilder()
    c = V(0.20, 1.83, 0.80)
    P.rbox(mb, c, (0.34, 0.20, 0.14), 0.012, 2, None, 0)
    P.cyl(mb, c + V(-0.05, 0.0, 0.07), c + V(-0.05, 0.0, 0.20), 0.065, 28, 1)          # botella de refrigerante
    P.disc(mb, c + V(-0.05, 0.0, 0.205), (0, 0, 1), 0.030, 0.02, 20, 2, 0.003)
    for dx in (0.06, 0.13):
        # bombas: no pasan de la pared trasera del frunk (y = 1,976)
        P.cyl(mb, c + V(dx, 0.10, -0.03), c + V(dx, 0.135, -0.03), 0.030, 20, 0)
    P.cyl(mb, c + V(0.0, -0.10, 0.0), c + V(0.15, -0.10, 0.0), 0.040, 20, 0)          # enfriador
    P.rbox(mb, c + V(-0.12, -0.02, -0.05), (0.08, 0.16, 0.10), 0.006, 1, None, 0)    # condensador LCC
    P.rbox(mb, c + V(0.0, 0.0, 0.075), (0.12, 0.12, 0.02), 0.004, 1, None, 3)        # Octovalve
    objs.append(P.make(mb, "THM_Supermanifold", "UNDERBODY", [M["connector_grey"], M["plastic_black"],
                       M["plastic_black"], M["alu_cast"]], asm, (0.5, 0.5, 1), 0.55, 6, "Refrigeración",
                       "Supermanifold con Octovalve, bombas, enfriador, condensador y botella (2 tornillos de 15 mm)", "V"))
    mb = L.MeshBuilder()
    c = V(-0.22, 1.82, 0.78)
    P.cyl(mb, c + V(-0.13, 0, 0), c + V(0.12, 0, 0), 0.068, 28, 0)
    P.rbox(mb, c + V(0.05, 0, 0.07), (0.12, 0.10, 0.06), 0.006, 1, None, 0)
    for dx in (-0.06, 0.02):
        P.cyl(mb, c + V(dx, 0, 0.068), c + V(dx, 0, 0.11), 0.012, 12, 1)
    objs.append(P.make(mb, "THM_AC_Compressor", "UNDERBODY", [M["alu_cast"], M["zinc"]], asm, (-0.5, 0.5, 0.5), 0.5, 6,
                       "Refrigeración", "Compresor eléctrico de A/C (scroll) sobre la Megabeam (3 tornillos)", "V"))
    mb = L.MeshBuilder()
    L.lathe(mb, [(0.080, -0.14), (0.080, 0.13)], tuple(c), (1, 0, 0), 32, 0)
    objs.append(P.make(mb, "THM_AC_Compressor_Acoustic_Cover", "UNDERBODY", M["harness"], asm, (-0.5, 0.6, 0.8), 0.65, 6,
                       "Refrigeración", "Cubierta acústica del compresor", "V"))
    # Tuberías de refrigerante (aspiración y descarga) y mangueras del Supermanifold al radiador
    mb = L.MeshBuilder()
    P.hose(mb, [(-0.10, 1.82, 0.84), (0.0, 1.76, 0.88), (0.06, 1.74, 0.84)], 0.009, 10, 4, 0)
    P.hose(mb, [(-0.12, 1.84, 0.73), (-0.02, 1.90, 0.74), (0.06, 1.86, 0.76)], 0.007, 10, 4, 0)
    objs.append(P.make(mb, "THM_AC_Lines", "UNDERBODY", M["alu_machined"], asm, (0, 0.3, 1), 0.45, 6,
                       "Refrigeración", "Tuberías de aspiración y descarga del refrigerante R1234yf", "V"))
    mb = L.MeshBuilder()
    # salen de las bombas del Supermanifold con un codo hacia abajo (bajo el suelo del frunk, z < 0,736) y van a
    # los depósitos laterales del radiador: la derecha por el pasillo entre la HCU y el larguero de la fundición, la
    # izquierda por delante de la unidad motriz
    P.hose(mb, [(0.33, 1.97, 0.77), (0.33, 1.972, 0.715), (0.405, 2.02, 0.70), (0.418, 2.12, 0.68),
                (0.43, 2.25, 0.63), (0.442, 2.395, 0.58)], 0.016, 14, 6, 0)
    P.hose(mb, [(0.26, 1.97, 0.77), (0.26, 1.972, 0.715), (0.235, 2.06, 0.70), (0.10, 2.24, 0.66),
                (-0.32, 2.27, 0.62), (-0.43, 2.32, 0.60), (-0.442, 2.395, 0.58)], 0.016, 14, 6, 0)
    objs.append(P.make(mb, "THM_Radiator_Hoses", "UNDERBODY", M["hose"], asm, (0, 0.6, 0.6), 0.5, 6,
                       "Refrigeración", "Mangueras radiador ↔ Supermanifold", "V"))
    # Haz de mangueras del tren motriz a lo largo del lateral izquierdo (bajo el faldón)
    mb = L.MeshBuilder()
    for i, dx in enumerate((0.0, -0.034)):
        # bajo el umbral izquierdo; sube por delante del guardabarros trasero y por detrás del faldón delantero
        P.hose(mb, [(0.10 + dx, 1.72, 0.74), (-0.55 + dx, 1.45, 0.50), (-0.78 + dx, 1.15, 0.30),
                    (-0.85 + dx, 1.00, 0.282), (-0.85 + dx, -0.95, 0.282), (-0.75 + dx, -1.30, 0.30),
                    (-0.55 + dx, -1.45, 0.45), (-0.32 + dx, -1.62, 0.56)], 0.014, 12, 6, 0)
    objs.append(P.make(mb, "THM_Powertrain_Hose_Bundle", "UNDERBODY", M["hose"], None, (-1, 0, -0.3), 0.6, 5,
                       "Refrigeración", "Haz de mangueras del tren motriz (impulsión y retorno)", "V"))
    mb = L.MeshBuilder()
    for dx in (0.0, 0.05):
        P.hose(mb, [(-0.36 + dx, BAT_Y0 + 0.14, 0.52), (-0.30 + dx, 1.50, 0.62), (0.05 + dx, 1.72, 0.76)],
               0.013, 12, 5, 0)
    objs.append(P.make(mb, "THM_Battery_Coolant_Hoses", "UNDERBODY", M["hose"], None, (0, 0.3, 0.6), 0.45, 5,
                       "Refrigeración", "Mangueras de impulsión y retorno de la batería", "V"))
    return objs


# ---------------------------------------------------------------------------
# Frenos hidráulicos, aire comprimido y baja tensión
# ---------------------------------------------------------------------------
def build_brake_hydraulics(M):
    objs = []
    mb = L.MeshBuilder()
    # 30 mm por dentro del larguero izquierdo de la fundición (x = -0,45 m)
    c = V(-0.37, 1.66, 0.95)
    P.cyl(mb, c, c + V(0, 0.14, 0), 0.075, 28, 0)
    P.rbox(mb, c + V(0.0, 0.17, 0.0), (0.12, 0.05, 0.12), 0.01, 1, None, 0)
    P.cyl(mb, c + V(0.08, 0.07, -0.02), c + V(0.18, 0.07, -0.02), 0.040, 20, 1)
    objs.append(P.make(mb, "BRK_Booster_Electromechanical", "UNDERBODY", [M["alu_cast"], M["steel_black"]], None,
                       (-0.5, 0.6, 0.5), 0.6, 4, "Frenos", "Servofreno electromecánico (3 tuercas al pedalier)", "V"))
    mb = L.MeshBuilder()
    # sobre el servofreno, por detrás del refuerzo del puente delantero (y < 1,71) y bajo el absorbedor
    P.rbox(mb, c + V(0.0, 0.0, 0.125), (0.14, 0.07, 0.08), 0.008, 1, None, 0)
    P.disc(mb, c + V(0.0, 0.0, 0.175), (0, 0, 1), 0.022, 0.02, 16, 1, 0.003)
    objs.append(P.make(mb, "BRK_Remote_Reservoir", "UNDERBODY", [M["plastic_black"], M["plastic_black"]], None,
                       (-0.3, 0.4, 1), 0.6, 6, "Frenos", "Depósito remoto del líquido de frenos (DOT4)", "V"))
    mb = L.MeshBuilder()
    # por dentro del larguero derecho de la fundición y bajo el frunk
    h = V(0.32, 2.125, 0.66)
    P.rbox(mb, h, (0.13, 0.10, 0.12), 0.008, 1, None, 0)
    P.cyl(mb, h + V(0.0, -0.05, 0.0), h + V(0.0, -0.10, 0.0), 0.035, 20, 1)
    P.rbox(mb, h + V(0, 0.06, 0), (0.12, 0.02, 0.10), 0.004, 1, None, 2)
    objs.append(P.make(mb, "BRK_Hydraulic_Control_Unit", "UNDERBODY", [M["alu_machined"], M["steel_black"],
                       M["connector_grey"]], None, (0.5, 0.5, 0.6), 0.55, 4, "Frenos",
                       "Unidad hidráulica ABS/ESC (HCU, 3 tuercas al soporte)", "V"))
    mb = L.MeshBuilder()
    paths = [
        [h + V(-0.05, 0, 0.06), (0.10, 2.0, 0.70), c + V(0.06, 0.17, 0.0)],
        [h + V(0.06, 0, 0.0), (0.62, 2.0, 0.66), hardpoints("F", 1)["uca_f"] + V(-0.08, -0.28, 0.06)],
        [h + V(-0.06, 0, -0.02), (-0.20, 2.10, 0.58), hardpoints("F", -1)["uca_f"] + V(0.08, -0.28, 0.06)],
        [h + V(-0.02, 0, -0.06), (0.30, 1.90, 0.40), (0.86, 1.20, 0.282), (0.86, -1.00, 0.282),
         hardpoints("R", 1)["uca_f"] + V(-0.08, 0.28, 0.06)],
        [h + V(0.02, 0, -0.06), (0.26, 1.90, 0.40), (0.875, 1.20, 0.282), (0.875, -1.00, 0.282), (-0.20, -1.60, 0.62),
         hardpoints("R", -1)["uca_f"] + V(0.08, 0.28, 0.06)],
    ]
    for pth in paths:
        P.hose(mb, pth, 0.0024, 6, 6, 0)
    objs.append(P.make(mb, "BRK_Pipes", "UNDERBODY", M["zinc"], None, (0, 0, -1), 0.5, 4, "Frenos",
                       "Tubos rígidos de freno desde la HCU a las cuatro esquinas", "V"))
    return objs


def build_air_supply(M):
    objs = []
    asm = L.assembly("AIR_SUPPLY", "REAR_SUSPENSION", (-0.30, -2.30, 0.50))
    L.explode(asm, (-0.3, -0.6, -1), 0.8, 4, "Suspensión", "Suministro de aire de la suspensión", "R")
    objs.append(asm)
    mb = L.MeshBuilder()
    c = V(-0.42, -2.28, 0.48)
    P.cyl(mb, c, c + V(0.20, 0, 0), 0.050, 24, 0)
    P.rbox(mb, c + V(0.24, 0, 0), (0.08, 0.10, 0.10), 0.008, 1, None, 0)
    P.cyl(mb, c + V(-0.01, 0, 0.0), c + V(-0.06, 0, 0.0), 0.030, 16, 1)
    P.rbox(mb, c + V(0.10, 0, -0.07), (0.30, 0.12, 0.012), 0.003, 1, None, 2)
    objs.append(P.make(mb, "CHS_AirSuspension_Compressor", "REAR_SUSPENSION", [M["alu_cast"], M["plastic_black"],
                       M["steel_black"]], asm, (-1, -0.3, 0), 0.4, 6, "Suspensión",
                       "Compresor de la suspensión neumática con soporte (3 tuercas)", "V"))
    mb = L.MeshBuilder()
    c2 = V(0.10, -2.36, 0.50)
    L.lathe(mb, [(0.0, -0.20), (0.050, -0.19), (0.066, -0.16), (0.066, 0.16), (0.050, 0.19), (0.0, 0.20)], tuple(c2),
            (1, 0, 0), 28, 0)
    objs.append(P.make(mb, "CHS_AirSuspension_Reservoir", "REAR_SUSPENSION", M["alu_machined"], asm, (1, -0.3, 0), 0.4, 6,
                       "Suspensión", "Depósito de aire (4 racores VOSS, 2 tuercas)", "V"))
    mb = L.MeshBuilder()
    c3 = V(0.38, -2.30, 0.52)
    P.rbox(mb, c3, (0.10, 0.06, 0.08), 0.006, 1, None, 0)
    objs.append(P.make(mb, "CHS_AirSuspension_ValveBlock", "REAR_SUSPENSION", M["plastic_black"], asm, (1, 0, 0.3), 0.3, 6,
                       "Suspensión", "Bloque de válvulas (5 conductos de aire)", "V"))
    mb = L.MeshBuilder()
    # cada conducto sale de su racor VOSS en la tapa del bloque de válvulas (no del interior del bloque)
    fit_x = {("F", 1): 0.42, ("F", -1): 0.345, ("R", 1): 0.395, ("R", -1): 0.37}
    for axle in ("F", "R"):
        for s in (1, -1):
            top = hardpoints(axle, s)["spr_top"] + V(s * 0.065, 0, -0.01)
            st = V(fit_x[(axle, s)], c3.y, 0.583)
            if axle == "R":
                pth = [st, st + V(s * 0.02, 0.03, 0.03), st + V(s * 0.1, 0.1, 0.05), top + V(-s * 0.15, -0.2, 0.0), top]
            else:
                pth = [st, V(st.x, c3.y + 0.04, 0.60), (0.5 * s, -1.9, 0.40), (0.84 * s, -1.0, 0.282),
                       (0.84 * s, 1.2, 0.282), top + V(-s * 0.05, -0.25, -0.1), top]
            P.hose(mb, pth, 0.003, 6, 6, 0)
    # compresor (salida en la cara +X de su caja) -> extremo del depósito -> cara trasera del bloque
    P.hose(mb, [c + V(0.285, 0, 0), c + V(0.30, -0.04, 0.01), c2 + V(-0.205, 0, 0)], 0.004, 6, 4, 0)
    P.hose(mb, [c2 + V(0.205, 0, 0), (0.335, -2.345, 0.51), (0.355, c3.y - 0.034, 0.52)], 0.004, 6, 4, 0)
    objs.append(P.make(mb, "CHS_AirSuspension_Lines", "REAR_SUSPENSION", M["plastic_black"], asm, (0, 0, -1), 0.3, 6,
                       "Suspensión", "Conductos de aire a los cuatro módulos de muelle", "V"))
    return objs


def build_electrical(M):
    objs = []
    # Batería de media tensión (48 V, 4 Ah) en el maletero delantero
    mb = L.MeshBuilder()
    # contra el cortafuegos, detrás del megabeam (lado derecho); conector en la cara delantera
    P.rbox(mb, (0.34, 1.60, 0.86), (0.20, 0.14, 0.16), 0.012, 2, None, 0)
    P.rbox(mb, (0.34, 1.68, 0.91), (0.05, 0.02, 0.03), 0.004, 1, None, 1)
    objs.append(P.make(mb, "LV_Battery_48V", "BATTERY_ASSEMBLY", [M["plastic_black"], M["connector_grey"]], None,
                       (1, 0.3, 0.3), 0.6, 5, "Baja tensión", "Batería de media tensión de 48 V (2 tornillos)", "V"))
    # Controladores de carrocería (izquierdo, derecho y trasero)
    # izquierdo y derecho por dentro de los paneles laterales del salpicadero (|x| <= 0,70)
    for name, p, lbl in (("LV_Body_Controller_LH", (-0.585, 1.30, 0.80), "Controlador de carrocería izquierdo"),
                         ("LV_Body_Controller_RH", (0.585, 1.355, 0.80), "Controlador de carrocería derecho"),
                         # entre la pared trasera de la cabina (y = -0,957) y el travesaño, bajo el suelo de la caja
                         ("LV_Body_Controller_Rear", (0.0, -0.99, 0.755), "Controlador trasero (media tensión)")):
        mb = L.MeshBuilder()
        P.rbox(mb, p, (0.22, 0.05, 0.15), 0.006, 1, None, 0)
        for i in range(4):
            P.rbox(mb, V(*p) + V(-0.075 + i * 0.05, -0.03, 0.05), (0.035, 0.02, 0.03), 0.003, 1, None, 1)
        for i in range(8):
            P.rbox(mb, V(*p) + V(-0.09 + i * 0.026, 0.028, -0.01), (0.006, 0.008, 0.11), 0.002, 1, None, 0)
        objs.append(P.make(mb, name, "BATTERY_ASSEMBLY", [M["alu_cast"], M["connector_grey"]], None,
                           (0, 0.5 if p[1] > 0 else -0.5, 1), 0.5, 5, "Baja tensión",
                           lbl + (" (3 fijaciones: 2 tuercas de 13 N·m + 1 perno de 10 N·m)" if name.endswith("Rear")
                                  else " (4 tuercas de 10 mm a 14 N·m)"), "V"))
    # Mazos de cables principales: columna vertebral de media tensión y Ethernet
    mb = L.MeshBuilder()
    # junto al umbral izquierdo sobre el suelo (bajo la moqueta) y, detrás, por encima del travesaño de la pared
    # trasera hasta la cara lateral del controlador trasero
    P.corrugated(mb, [(-0.585, 1.30, 0.714), (-0.66, 1.20, 0.60), (-0.775, 1.05, 0.53), (-0.79, 0.80, 0.497),
                      (-0.79, -0.80, 0.497), (-0.80, -0.90, 0.68), (-0.70, -0.985, 0.72), (-0.30, -0.99, 0.74),
                      (-0.122, -0.99, 0.755)], 0.011, 10, 0.010, 0)
    P.corrugated(mb, [(0.585, 1.355, 0.714), (0.30, 1.40, 0.80), (0.0, 1.45, 0.86), (-0.30, 1.40, 0.82),
                      (-0.585, 1.30, 0.714)], 0.010, 10, 0.010, 0)
    objs.append(P.make(mb, "LV_Harness_MV_Backbone", "BATTERY_ASSEMBLY", M["harness"], None, (-1, 0, 0.4), 0.5, 5,
                       "Baja tensión", "Mazo principal de 48 V con anillo Ethernet redundante", "R"))
    # Cables de alta tensión: batería → unidad delantera, compresor de A/C; bahía auxiliar → inversores traseros
    mb = L.MeshBuilder()
    for dx in (-0.12, 0.12):
        # terminan en la cara trasera del inversor delantero (y = 1,697 m), no dentro de él
        P.hose(mb, [(dx, BAT_Y0 - 0.005, BAT_ZT + 0.03), (dx * 1.2, BAT_Y0 + 0.12, 0.50),
                    (0.10 + dx * 0.5, 1.55, 0.60), (0.10 + dx * 0.5, 1.683, 0.63)], 0.012, 12, 5, 0)
    # al compresor de A/C: termina en su cara trasera
    P.hose(mb, [(0.0, BAT_Y0 - 0.005, BAT_ZT + 0.05), (-0.10, 1.50, 0.62), (-0.16, 1.70, 0.72),
                (-0.17, 1.743, 0.74)], 0.007, 10, 5, 0)
    # de la cara trasera de la ACJB a la cara delantera de cada inversor trasero, entre el refrigerador de placa
    # y la cubierta acústica del motor
    for s in (1, -1):
        xs = -0.30 if s > 0 else -0.40
        for dz in (0.0, 0.026):
            P.hose(mb, [(xs, -1.373, 0.615 + dz), (xs, -1.45, 0.62 + dz), (s * 0.22, -1.62, 0.64 + dz),
                        (s * 0.235, -1.90, 0.645 + dz), (s * 0.24, S.Y_REAR_AXLE - 0.307, 0.645 + dz)],
                   0.011, 12, 5, 0)
    objs.append(P.make(mb, "HV_Cables", "BATTERY_ASSEMBLY", M["hv_orange"], None, (0, 0, -1), 1.0, 5, "Alta tensión",
                       "Cables de alta tensión (unidad delantera, compresor, inversores traseros)", "R"))
    return objs


def harness_branches(M):
    """Ramales del cableado de 48 V / Ethernet (nombres del manual: Harness - Door, Bed, Tailgate,
    Frunk, Windshield, Roof Accessory...) con protectores corrugados y conectores."""
    objs = []
    routes = {
        # los ramales salen de las caras de los controladores de carrocería (x = ±0,475..0,695, y = 1,275..1,325)
        "LV_Harness_Door_FL": ([(-0.712, 1.30, 0.80), (-0.80, 1.20, 0.86), (-0.86, 1.10, 0.90)], "Mazo de la puerta delantera izquierda"),
        "LV_Harness_Door_FR": ([(0.712, 1.355, 0.80), (0.80, 1.20, 0.86), (0.86, 1.10, 0.90)], "Mazo de la puerta delantera derecha"),
        "LV_Harness_Door_RL": ([(-0.79, 0.20, 0.50), (-0.83, 0.10, 0.70), (-0.86, 0.02, 0.86)], "Mazo de la puerta trasera izquierda"),
        "LV_Harness_Door_RR": ([(0.79, 0.20, 0.50), (0.83, 0.10, 0.70), (0.86, 0.02, 0.86)], "Mazo de la puerta trasera derecha"),
        "LV_Harness_Frunk": ([(0.585, 1.394, 0.80), (0.56, 1.62, 0.86), (0.40, 2.10, 0.80), (0.0, 2.50, 0.78),
                              (-0.45, 2.45, 0.85)], "Mazo del frunk, faros y fascia delantera"),
        # bajo el suelo de la caja (z < 0,859), por dentro de la pared del paso de rueda (|x| = 0,494)
        "LV_Harness_Bed_L": ([(-0.05, -1.044, 0.805), (-0.40, -1.06, 0.80), (-0.48, -1.30, 0.83), (-0.48, -2.40, 0.83),
                              (-0.80, -2.60, 0.85)],
                             "Mazo izquierdo de la caja (luces, tomas, motor de la cubierta)"),
        "LV_Harness_Bed_R": ([(0.05, -1.044, 0.805), (0.40, -1.06, 0.80), (0.48, -1.30, 0.83), (0.48, -2.40, 0.83),
                              (0.80, -2.60, 0.85)],
                             "Mazo derecho de la caja"),
        "LV_Harness_Tailgate": ([(0.80, -2.60, 0.85), (0.84, -2.80, 0.80), (0.70, -2.86, 0.80), (-0.70, -2.86, 0.80)],
                                "Mazo del portón (luz, cámara, cierres)"),
        "LV_Harness_Windshield": ([(-0.62, 1.30, 0.886), (-0.72, 1.20, 1.20), (-0.70, 0.95, 1.55), (0.0, 0.70, 1.67)],
                                  "Mazo del parabrisas y del módulo de cámaras (por el pilar A)"),
    }
    for name, (pts, lbl) in routes.items():
        mb = L.MeshBuilder()
        P.corrugated(mb, pts, 0.0065, 8, 0.008, 0)
        for p in (pts[0], pts[-1]):
            P.rbox(mb, p, (0.03, 0.025, 0.02), 0.003, 1, None, 1)
        o = P.make(mb, name, "BATTERY_ASSEMBLY", [M["harness"], M["connector_grey"]], None,
                   (0, 0, 1) if "Bed" in name or "Tailgate" in name else (0, 0.3, 0.6), 0.40, 6, "Baja tensión", lbl, "R")
        objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Bajos: deflectores, placas de protección, difusor y ganchos de remolque
# ---------------------------------------------------------------------------
def build_underbody(M):
    objs = []
    specs = [
        ("CHS_Aeroshield_Front", (2.30, 1.55), 0.272, 0.92, "Deflector aerodinámico delantero (11 tornillos de 10 mm)", 11),
        ("CHS_Aeroshield_Mid", (1.20, -1.30), 0.268, 1.56, "Deflector central bajo la batería (6 grapas y 10 tornillos)", 10),
        ("CHS_Aeroshield_Rear", (-1.42, -2.20), 0.272, 1.20, "Deflector aerodinámico trasero", 8),
    ]
    for name, (y0, y1), z, w, lbl, nb in specs:
        mb = L.MeshBuilder()
        P.rbox(mb, (0, (y0 + y1) / 2, z), (w, abs(y0 - y1), 0.006), 0.002, 1, None, 0)
        for i in range(nb):
            t = i / max(1, nb - 1)
            for sg in (1, -1):
                if nb > 6 and sg < 0 and i % 2:
                    continue
                P.flange_bolt(mb, (sg * (w / 2 - 0.03), y0 + (y1 - y0) * t, z - 0.003), (0, 0, -1), 0.008, 1)
        # nervios de rigidez
        for i in range(5):
            x = -w / 2 + w * (i + 1) / 6
            P.rbox(mb, (x, (y0 + y1) / 2, z - 0.004), (0.02, abs(y0 - y1) * 0.85, 0.004), 0.001, 1, None, 0)
        objs.append(P.make(mb, name, "UNDERBODY", [M["plastic_textured"], M["zinc"]], None, (0, 0, -1), 0.6, 3, "Bajos",
                           lbl, "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0, 2.05, 0.276), (0.70, 0.42, 0.006), 0.002, 1, None, 0)
    for i in range(8):
        P.hex_nut(mb, (-0.30 + (i % 4) * 0.2, 1.86 + (i // 4) * 0.38, 0.273), (0, 0, -1), 0.010, 1, stud=0)
    objs.append(P.make(mb, "CHS_Skid_Plate_Front", "UNDERBODY", [M["alu_forged"], M["zinc"]], None, (0, 0.2, -1), 0.7, 3,
                       "Bajos", "Placa de protección delantera (8 tuercas de 15 mm y 2 tornillos)", "V"))
    mb = L.MeshBuilder()
    for sg in (1, -1):
        # por delante del radiador (cara delantera y = 2,455)
        c = V(sg * 0.42, 2.53, 0.47)
        P.beam(mb, c + V(0, -0.06, 0), c + V(0, 0.04, 0), 0.04, 0.03, r=0.006)
        L.lathe(mb, [(0.012, 0.0), (0.040, 0.0), (0.040, 0.016), (0.012, 0.016)], tuple(c + V(0, 0.05, 0)), (1, 0, 0),
                20, 0, closed_profile=True)
        for k in range(2):
            P.flange_bolt(mb, c + V(sg * 0.022, -0.04 + k * 0.05, 0), (sg, 0, 0), 0.012, 1)
    objs.append(P.make(mb, "CHS_Recovery_Hooks_Front", "UNDERBODY", [M["steel_black"], M["zinc"]], None, (0, 1, 0), 0.6, 3,
                       "Bajos", "Ganchos de rescate delanteros (4 tornillos a 78 N·m cada uno)", "V"))
    return objs


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
def build_all(M):
    out = []
    out += build_battery(M)
    out += build_ancillary_bay(M)
    out += drive_unit_front(M)
    out += drive_unit_rear(M)
    out += halfshafts(M)
    for axle in ("F", "R"):
        for s in (1, -1):
            out += build_corner(M, axle, s)
        out.append(stabilizer_bar(M, axle))
        out.append(steering_actuator(M, axle))
        out.append(subframe(M, axle))
    out += lca_shields(M)
    out += build_thermal(M)
    out += build_brake_hydraulics(M)
    out += build_air_supply(M)
    out += build_electrical(M)
    out += harness_branches(M)
    out += build_underbody(M)
    return [o for o in out if o is not None]
