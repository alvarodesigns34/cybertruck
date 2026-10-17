"""Detalle interior del habitáculo (decoración Tactical Grey).

[V] Piezas y fijaciones según el manual de servicio: volante con botonera en los radios
    (sin palancas), actuador de realimentación de la dirección (3 tornillos de 13 mm), consola
    con dos cargadores inalámbricos (4 tornillos T20), portavasos, concentrador USB, reposabrazos,
    paneles laterales y salida «Airwave»; guantera (5 tornillos T20) con luz; panel de desempañado;
    altavoces de rango completo de 60 mm en el guarnecido superior del pilar A (3 tornillos T15),
    subwoofers en las puertas delanteras y en el pilar C, altavoces del larguero trasero;
    guarnecidos de pilares A (delantero, medio, superior, inferior), B y C (superior e inferior);
    paneles de puerta con luz ambiental del bolsillo, luz de cortesía, catadióptrico, interruptores
    de ventanilla e interruptor interior de apertura (14 grapas y 3 tornillos); asientos delanteros
    con guías, elevadores, botones de ajuste lumbar, de cojín y de reclinado y escudos laterales
    (4 tornillos T45P a 34 N·m); asiento trasero con reposabrazos y portavasos; enrolladores,
    hebillas y guías de cinturón; parasoles con cortinilla; retrovisor interior y cámara de
    habitáculo; módulo de control de los airbags (RCM, 3 tuercas); ordenador del vehículo.
[R]/[A] Formas y posiciones: reconstruidas con las cotas interiores del manual del propietario y
    fotografías; las costuras se proyectan sobre la tapicería real del modelo por trazado de rayos.
"""

import math
import bpy
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
import ct_specs as S
import ct_lib as L
import ct_parts as P
import build_body as B

FLOOR_Z = 0.505
H_FRONT = (0.30, 0.80)
H_REAR = (-0.63, 0.77)
REAR_TILT = 15
SEAT_X = 0.395
WHEEL_C = Vector((-0.395, 0.735, 1.02))


def V(*a):
    return Vector(a)


def rot_x(deg):
    return Matrix.Rotation(math.radians(deg), 3, "X")


def obj(name):
    return bpy.data.objects.get(name)


# ---------------------------------------------------------------------------
# Volante, columna y actuador de realimentación
# ---------------------------------------------------------------------------
def steering_wheel_detail(M):
    objs = []
    asm = obj("STEERING_WHEEL")
    col_dir = V(0, 1, -0.42).normalized()
    u = V(1, 0, 0)
    v = col_dir.cross(u).normalized()
    if v.z < 0:
        v = -v
    c = WHEEL_C
    rot = Matrix((u, v, col_dir)).transposed()
    mb = L.MeshBuilder()
    # cojín central (airbag) de forma rectangular redondeada y radios horizontales
    P.rbox(mb, c + col_dir * 0.025, (0.130, 0.095, 0.050), 0.018, 3, rot, 0)
    for sg in (1, -1):
        P.rbox(mb, c + u * sg * 0.115 + col_dir * 0.018 - v * 0.012, (0.120, 0.050, 0.026), 0.010, 2, rot, 0)
    objs.append(P.make(mb, "INT_SteeringWheel_Hub", "STEERING", M["int_plastic"], asm, (0, -1, 0.3), 0.05, 6,
                       "Dirección", "Buje con módulo de airbag del conductor y radios", "R"))
    mb = L.MeshBuilder()
    for sg in (1, -1):
        base = c + u * sg * 0.115 - v * 0.012 + col_dir * 0.004
        # rodillo de desplazamiento y cuatro botones por radio (intermitentes, luces, bocina, voz)
        P.cyl(mb, base + u * sg * 0.010 - u * 0.004 + v * 0.002, base + u * sg * 0.010 + u * 0.004 + v * 0.002, 0.011,
              18, 1)
        for k, (dx, dy) in enumerate(((-0.030, 0.012), (-0.030, -0.012), (0.035, 0.012), (0.035, -0.012))):
            P.rbox(mb, base + u * sg * dx + v * dy - col_dir * 0.002, (0.018, 0.010, 0.006), 0.002, 1, rot, 0)
    objs.append(P.make(mb, "INT_SteeringWheel_Controls", "STEERING", [M["int_grey"], M["alu_trim"]], asm,
                       (0, -1, 0.5), 0.12, 6, "Dirección",
                       "Botonera de los radios (intermitentes, luces, bocina) y rodillos de desplazamiento", "V"))
    # actuador de realimentación de la dirección (por cable: sin unión mecánica con las ruedas)
    mb = L.MeshBuilder()
    p0 = c + col_dir * 0.30
    P.cyl(mb, p0, p0 + col_dir * 0.16, 0.048, 28, 0)     # cuelga bajo la viga del salpicadero
    P.rbox(mb, p0 + col_dir * 0.08 - v * 0.07, (0.10, 0.06, 0.12), 0.006, 1, rot, 0)
    for k in range(3):
        a = 2 * math.pi * k / 3
        P.flange_bolt(mb, p0 + (u * math.cos(a) + v * math.sin(a)) * 0.045, -col_dir, 0.008, 1)
    P.rbox(mb, p0 + col_dir * 0.20 - v * 0.03, (0.16, 0.05, 0.08), 0.006, 1, rot, 0)
    objs.append(P.make(mb, "STR_Steering_Feedback_Actuator", "STEERING", [M["alu_cast"], M["zinc"]], asm,
                       (0, 1, -0.4), 0.30, 6, "Dirección",
                       "Actuador de realimentación del volante (steer-by-wire) y soporte de la columna", "V"))
    return objs


# ---------------------------------------------------------------------------
# Consola central
# ---------------------------------------------------------------------------
def console_detail(M):
    objs = []
    asm = obj("CONSOLE_ASSEMBLY")
    for name in ("INT_Console_Body", "INT_Console_Tray", "INT_Console_Armrest"):
        o = obj(name)
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
    zt = 0.80
    # cuerpo: sección trapecial que se estrecha hacia abajo, con frontal inclinado bajo la pantalla
    mb = L.MeshBuilder()
    pts = []
    for (y, ztop, wt, wb) in ((0.95, 0.80, 0.135, 0.120), (0.55, zt, 0.135, 0.125), (0.05, zt, 0.135, 0.125),
                              (-0.14, zt - 0.02, 0.130, 0.120)):
        pts += [V(-wt, y, ztop), V(wt, y, ztop), V(-wb, y, FLOOR_Z + 0.01), V(wb, y, FLOOR_Z + 0.01)]
    P.hull(mb, pts, 0)
    objs.append(P.make(mb, "INT_Console_Body", "INTERIOR_CONTROLS", M["int_plastic"], asm, (0, 0, 1), 0.05, 6,
                       "Consola central", "Estructura de la consola central", "R", bevel=0.012))
    for sg, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        P.hull(mb, [V(sg * 0.136, 0.93, 0.79), V(sg * 0.136, -0.12, 0.78), V(sg * 0.125, 0.93, FLOOR_Z + 0.03),
                    V(sg * 0.125, -0.12, FLOOR_Z + 0.03), V(sg * 0.146, 0.90, 0.77), V(sg * 0.146, -0.10, 0.76),
                    V(sg * 0.134, 0.90, FLOOR_Z + 0.05), V(sg * 0.134, -0.10, FLOOR_Z + 0.05)], 0)
        objs.append(P.make(mb, f"INT_Console_Side_Panel_{sd}", "INTERIOR_CONTROLS", M["int_grey"], asm,
                           (sg, 0, 0), 0.20, 2, "Consola central", "Panel lateral exterior de la consola", "V",
                           bevel=0.006))
    # bandeja superior de los cargadores inalámbricos (2 x 4 tornillos T20)
    mb = L.MeshBuilder()
    P.rbox(mb, (0, 0.73, zt + 0.004), (0.25, 0.40, 0.012), 0.004, 1, None, 0)
    objs.append(P.make(mb, "INT_Console_Decor_Top", "INTERIOR_CONTROLS", M["int_grey"], asm, (0, 0, 1), 0.12, 2,
                       "Consola central", "Embellecedor superior de la consola", "V"))
    for k, y in enumerate((0.83, 0.64)):
        mb = L.MeshBuilder()
        P.rbox(mb, (0, y, zt + 0.011), (0.20, 0.15, 0.004), 0.003, 1, None, 0)
        for i in range(9):
            P.rbox(mb, (0, y - 0.06 + i * 0.015, zt + 0.0135), (0.17, 0.003, 0.002), 0.0008, 1, None, 1)
        objs.append(P.make(mb, f"INT_Console_Wireless_Charger_{k + 1}", "INTERIOR_CONTROLS",
                           [M["int_plastic"], M["bushing"]], asm, (0, 0, 1), 0.18 + 0.04 * k, 6, "Consola central",
                           "Cargador inalámbrico de 15 W con superficie antideslizante", "V"))
    # reposabrazos con tapa y costura
    mb = L.MeshBuilder()
    P.rbox(mb, (0, 0.11, zt + 0.032), (0.25, 0.42, 0.055), 0.022, 3, None, 0)
    objs.append(P.make(mb, "INT_Console_Armrest", "INTERIOR_CONTROLS", M["leather"], asm, (0, 0, 1), 0.18, 6,
                       "Consola central", "Reposabrazos (tapa del compartimento de almacenamiento)", "V"))
    mb = L.MeshBuilder()
    P.sweep(mb, [(-0.112, -0.09, zt + 0.051), (-0.112, 0.31, zt + 0.051)], P.circle_profile(0.0012, 6), mat=0)
    P.sweep(mb, [(0.112, -0.09, zt + 0.051), (0.112, 0.31, zt + 0.051)], P.circle_profile(0.0012, 6), mat=0)
    objs.append(P.make(mb, "INT_Console_Armrest_Stitching", "INTERIOR_CONTROLS", M["stitch"], asm, (0, 0, 1), 0.22, 6,
                       "Consola central", "Costuras del reposabrazos", "R"))
    # puertos USB-C (delanteros y traseros) y luz de cortesía
    mb = L.MeshBuilder()
    for y, dy in ((0.952, 1), (-0.145, -1)):
        for x in (-0.03, 0.03):
            P.rbox(mb, (x, y, 0.70), (0.012, 0.004, 0.005), 0.0015, 1, None, 0)
    objs.append(P.make(mb, "INT_Console_USB_Ports", "INTERIOR_CONTROLS", M["alu_trim"], asm, (0, 0, -1), 0.10, 6,
                       "Consola central", "Puertos USB-C delanteros y traseros (concentrador USB)", "V"))
    return objs


# ---------------------------------------------------------------------------
# Salpicadero: guantera, rodillera, desempañado, cuartos laterales, módulos ocultos
# ---------------------------------------------------------------------------
def dashboard_detail(M):
    objs = []
    asm = obj("IP_ASSEMBLY")
    for name in ("INT_IP_Glovebox", "INT_IP_Lower_Driver"):
        o = obj(name)
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
    mb = L.MeshBuilder()
    P.hull(mb, [V(0.14, 0.955, 0.985), V(0.69, 0.955, 0.985), V(0.14, 0.99, 0.90), V(0.69, 0.99, 0.90),
                V(0.14, 1.07, 0.80), V(0.69, 1.07, 0.80), V(0.14, 1.10, 0.80), V(0.69, 1.10, 0.80),
                V(0.14, 1.00, 0.985), V(0.69, 1.00, 0.985)], 0)
    objs.append(P.make(mb, "INT_IP_Glovebox", "INTERIOR_DASHBOARD", M["int_plastic"], asm, (0.3, -1, -0.3), 0.25, 2,
                       "Salpicadero", "Guantera (5 tornillos T20) con luz de cortesía", "V", bevel=0.006))
    mb = L.MeshBuilder()
    # por debajo del actuador del volante y de la columna (z ≥ 0,76), delante de la pata del salpicadero
    P.hull(mb, [V(-0.69, 0.955, 0.760), V(-0.24, 0.955, 0.760), V(-0.69, 1.00, 0.70), V(-0.24, 1.00, 0.70),
                V(-0.69, 1.08, 0.62), V(-0.24, 1.08, 0.62), V(-0.69, 1.10, 0.62), V(-0.24, 1.10, 0.62),
                V(-0.69, 1.00, 0.760), V(-0.24, 1.00, 0.760)], 0)
    objs.append(P.make(mb, "INT_IP_Lower_Driver", "INTERIOR_DASHBOARD", M["int_plastic"], asm, (-0.3, -1, -0.3), 0.25,
                       2, "Salpicadero", "Panel inferior del conductor (protección de rodillas)", "V", bevel=0.006))
    # rejilla de desempañado a lo ancho de la base del parabrisas
    mb = L.MeshBuilder()
    for i in range(40):
        x = -0.70 + i * 1.40 / 39
        P.rbox(mb, (x, 1.86, 1.249), (0.012, 0.06, 0.004), 0.001, 1, None, 0)
    objs.append(P.make(mb, "INT_IP_Defrost_Panel", "INTERIOR_DASHBOARD", M["int_plastic"], asm, (0, 0.3, 1), 0.20, 6,
                       "Salpicadero", "Panel de desempañado del parabrisas", "V"))
    # cuartos laterales del salpicadero (tapas extremas) con salida de desempañado lateral
    for sg, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        # tapa del extremo del salpicadero, por dentro del panel de la puerta delantera
        P.hull(mb, [V(sg * 0.700, 0.95, 1.10), V(sg * 0.755, 0.98, 1.10), V(sg * 0.700, 1.30, 1.16),
                    V(sg * 0.755, 1.30, 1.16), V(sg * 0.700, 0.98, 0.80), V(sg * 0.755, 1.00, 0.80),
                    V(sg * 0.700, 1.30, 0.80), V(sg * 0.755, 1.30, 0.80)], 0)
        P.rbox(mb, V(sg * 0.757, 1.02, 1.06), (0.004, 0.06, 0.03), 0.002, 1, None, 1)
        objs.append(P.make(mb, f"INT_IP_Quarter_Panel_{sd}", "INTERIOR_DASHBOARD", [M["int_grey"], M["int_plastic"]],
                           asm, (sg, -0.3, 0), 0.25, 2, "Salpicadero",
                           "Panel lateral del salpicadero con salida de desempañado lateral", "V", bevel=0.005))
    # módulo de climatización (HVAC) detrás del salpicadero y conductos al suelo
    mb = L.MeshBuilder()
    # caja central entre la guantera (delante), la viga transversal (encima) y el mamparo (detrás)
    P.rbox(mb, (0.06, 1.25, 0.78), (0.56, 0.24, 0.27), 0.02, 2, None, 0)
    P.cyl(mb, (0.42, 1.24, 0.76), (0.42, 1.24, 0.90), 0.085, 28, 0)
    for sg in (1, -1):
        P.hose(mb, [(sg * 0.17, 1.15, 0.67), (sg * 0.20, 1.00, 0.56), (sg * 0.22, 0.80, 0.53)], 0.03, 12, 5, 1)
    objs.append(P.make(mb, "INT_HVAC_Module", "INTERIOR_DASHBOARD", [M["plastic_black"], M["plastic_liner"]], asm,
                       (0, 1, 0.3), 0.45, 2, "Climatización",
                       "Módulo de climatización (ventilador, filtro HEPA, compuertas) y conductos al suelo", "V"))
    # ordenador del vehículo (infoentretenimiento y conducción asistida) con protección antigoteo
    mb = L.MeshBuilder()
    P.rbox(mb, (0.42, 1.20, 1.02), (0.30, 0.20, 0.05), 0.006, 1, None, 0)
    for i in range(12):
        P.rbox(mb, (0.30 + i * 0.022, 1.20, 1.050), (0.006, 0.18, 0.010), 0.002, 1, None, 0)
    objs.append(P.make(mb, "INT_Car_Computer", "INTERIOR_DASHBOARD", M["alu_cast"], asm, (0.5, 0.5, 0.6), 0.40, 2,
                       "Electrónica", "Ordenador del vehículo (infoentretenimiento y Autopilot) con disipador", "V"))
    # módulos de airbag del acompañante y de rodillas, y RCM bajo la consola
    mb = L.MeshBuilder()
    # airbag del acompañante en la parte alta del salpicadero, bajo el parabrisas
    P.rbox(mb, (0.40, 1.45, 1.085), (0.26, 0.12, 0.05), 0.008, 1, None, 0)
    # rodilleras: la del conductor dentro del panel inferior; la del acompañante bajo la guantera
    P.rbox(mb, (-0.48, 1.04, 0.69), (0.26, 0.04, 0.05), 0.008, 1, None, 0)
    P.rbox(mb, (0.42, 1.03, 0.755), (0.26, 0.05, 0.05), 0.008, 1, None, 0)
    objs.append(P.make(mb, "INT_Airbag_Modules", "INTERIOR_DASHBOARD", M["plastic_black"], asm, (0, 0.5, 0.5), 0.35, 2,
                       "Seguridad", "Módulos de airbag del acompañante y de rodillas", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, (0.0, 0.35, FLOOR_Z + 0.03), (0.12, 0.14, 0.04), 0.004, 1, None, 0)
    for k in range(3):
        P.hex_nut(mb, (-0.05 + k * 0.05, 0.42, FLOOR_Z + 0.05), (0, 0, 1), 0.006, 1)
    objs.append(P.make(mb, "INT_Restraint_Control_Module", "INTERIOR_CONTROLS", [M["alu_cast"], M["zinc"]], None,
                       (0, 0, 1), 0.65, 2, "Seguridad", "Módulo de control de airbags (RCM, 3 tuercas a 10 N·m)", "V"))
    # pedales: acelerador articulado en el suelo y pedal de freno colgante
    for name in ("INT_Pedal_Accelerator", "INT_Pedal_Brake"):
        o = obj(name)
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
    mb = L.MeshBuilder()
    P.rbox(mb, V(-0.29, 1.27, 0.62), (0.075, 0.016, 0.20), 0.006, 2, rot_x(-28), 0)
    for i in range(7):
        P.rbox(mb, V(-0.29, 1.262 + i * 0.0, 0.55 + i * 0.022) + V(0, -0.006 + i * 0.012 * 0.0, 0), (0.06, 0.004, 0.004),
               0.001, 1, rot_x(-28), 1)
    P.rbox(mb, V(-0.29, 1.34, 0.535), (0.08, 0.06, 0.02), 0.004, 1, None, 0)
    objs.append(P.make(mb, "INT_Pedal_Accelerator", "INTERIOR_CONTROLS", [M["int_plastic"], M["bushing"]], asm,
                       (0, 1, 0), 0.25, 2, "Mandos", "Pedal del acelerador articulado en el suelo", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, V(-0.44, 1.25, 0.66), (0.12, 0.014, 0.075), 0.006, 2, rot_x(-22), 1)
    P.beam(mb, V(-0.44, 1.255, 0.68), V(-0.44, 1.36, 0.93), 0.016, 0.024, r=0.003)
    objs.append(P.make(mb, "INT_Pedal_Brake", "INTERIOR_CONTROLS", [M["steel_black"], M["bushing"]], asm,
                       (0, 1, 0), 0.25, 2, "Mandos", "Pedal de freno (al servofreno electromecánico)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, V(-0.70, 1.18, 0.58), (0.09, 0.03, 0.20), 0.006, 2, rot_x(-35), 0)
    objs.append(P.make(mb, "INT_Footrest", "INTERIOR_TRIM", M["bushing"], None, (0, 1, 0), 0.25, 2, "Guarnecidos",
                       "Reposapiés del conductor", "R"))
    return objs


# ---------------------------------------------------------------------------
# Guarnecidos de pilares, techo, parasoles, retrovisor y altavoces
# ---------------------------------------------------------------------------
def pillar_trims(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        # pilar A (a lo largo del borde del parabrisas) con altavoz de 60 mm
        mb = L.MeshBuilder()
        path = []
        for y in (1.80, 1.55, 1.30, 1.05, 0.80, 0.62):
            z = S.z_top(y) - 0.045
            path.append((s * (S.hw_glass(y, z) - 0.045), y, z))
        P.sweep(mb, path, P.rect_profile(0.075, 0.025, 0.010, 2), mat=0)
        sp = V(*path[2]) + V(-s * 0.01, 0, -0.03)
        L.lathe(mb, [(0.0, 0.0), (0.030, 0.0), (0.030, 0.004), (0.0, 0.004)], tuple(sp), (-s, 0, -0.6), 24, 1)
        objs.append(P.make(mb, f"INT_Trim_APillar_{sd}", "INTERIOR_TRIM", [M["headliner"], M["speaker_mesh"]], None,
                           (-s * 0.5, 0.3, 0.6), 0.35, 2, "Guarnecidos",
                           f"Guarnecido del pilar A {side} con altavoz de rango completo de 60 mm", "V"))
        # pilar B superior e inferior (con guía del cinturón)
        mb = L.MeshBuilder()
        yb = S.DOOR_B_SEAM_Y
        zb0, zb1 = S.z_belt(yb), S.z_top(yb) - 0.06
        P.hull(mb, [V(s * (S.hw_glass(yb, zb0) - 0.05), yb - 0.05, zb0), V(s * (S.hw_glass(yb, zb0) - 0.05), yb + 0.05, zb0),
                    V(s * (S.hw_glass(yb, zb1) - 0.04), yb - 0.04, zb1), V(s * (S.hw_glass(yb, zb1) - 0.04), yb + 0.04, zb1),
                    V(s * (S.hw_glass(yb, zb0) - 0.01), yb, zb0), V(s * (S.hw_glass(yb, zb1) - 0.005), yb, zb1)], 0)
        objs.append(P.make(mb, f"INT_Trim_BPillar_Upper_{sd}", "INTERIOR_TRIM", M["headliner"], None,
                           (-s, 0, 0.4), 0.35, 2, "Guarnecidos", f"Guarnecido superior del pilar B {side}", "V"))
        mb = L.MeshBuilder()
        P.hull(mb, [V(s * 0.700, yb - 0.06, FLOOR_Z + 0.05), V(s * 0.700, yb + 0.06, FLOOR_Z + 0.05),
                    V(s * 0.705, yb - 0.05, zb0), V(s * 0.705, yb + 0.05, zb0),
                    V(s * 0.748, yb - 0.06, FLOOR_Z + 0.05), V(s * 0.748, yb + 0.06, FLOOR_Z + 0.05),
                    V(s * 0.748, yb - 0.05, zb0), V(s * 0.748, yb + 0.05, zb0)], 0)
        objs.append(P.make(mb, f"INT_Trim_BPillar_Lower_{sd}", "INTERIOR_TRIM", M["int_plastic"], None,
                           (-s, 0, 0), 0.30, 2, "Guarnecidos", f"Guarnecido inferior del pilar B {side}", "V"))
        # pilar C superior e inferior y subwoofer del pilar C
        mb = L.MeshBuilder()
        yc = S.CAB_REAR_Y + 0.05
        zc0, zc1 = S.z_belt(yc), S.z_top(yc) - 0.06
        P.hull(mb, [V(s * 0.700, yc - 0.03, FLOOR_Z + 0.05), V(s * 0.700, yc + 0.10, FLOOR_Z + 0.05),
                    V(s * 0.700, yc - 0.03, zc0), V(s * 0.700, yc + 0.10, zc0), V(s * 0.748, yc - 0.03, FLOOR_Z + 0.05),
                    V(s * 0.748, yc + 0.10, FLOOR_Z + 0.05), V(s * 0.748, yc - 0.03, zc0), V(s * 0.748, yc + 0.10, zc0)], 0)
        objs.append(P.make(mb, f"INT_Trim_CPillar_Lower_{sd}", "INTERIOR_TRIM", M["int_plastic"], None,
                           (-s, 0.3, 0), 0.30, 2, "Guarnecidos", f"Guarnecido inferior del pilar C {side}", "V"))
        mb = L.MeshBuilder()
        P.hull(mb, [V(s * (S.hw_glass(yc, zc0) - 0.05), yc - 0.03, zc0), V(s * (S.hw_glass(yc, zc0) - 0.05), yc + 0.10, zc0),
                    V(s * (S.hw_glass(yc, zc1) - 0.04), yc - 0.03, zc1), V(s * (S.hw_glass(yc, zc1) - 0.04), yc + 0.06, zc1),
                    V(s * (S.hw_glass(yc, zc0) - 0.005), yc - 0.03, zc0), V(s * (S.hw_glass(yc, zc1) - 0.005), yc - 0.03, zc1)], 0)
        objs.append(P.make(mb, f"INT_Trim_CPillar_Upper_{sd}", "INTERIOR_TRIM", M["headliner"], None,
                           (-s, 0.3, 0.4), 0.35, 2, "Guarnecidos", f"Guarnecido superior del pilar C {side}", "V"))
        mb = L.MeshBuilder()
        # alojado en el guarnecido del pilar C, con la rejilla sobre su cara interior
        c = V(s * 0.724, yc + 0.04, 0.745)
        P.rbox(mb, c, (0.040, 0.11, 0.16), 0.010, 2, None, 0)
        L.lathe(mb, [(0.0, 0.0), (0.045, 0.0), (0.045, 0.004), (0.0, 0.004)], tuple(c + V(-s * 0.0245, 0, 0)), (-s, 0, 0),
                24, 1)
        objs.append(P.make(mb, f"INT_Subwoofer_CPillar_{sd}", "INTERIOR_TRIM", [M["int_plastic"], M["speaker_mesh"]],
                           None, (-s, 0.3, 0), 0.40, 2, "Audio", f"Subwoofer del pilar C {side} (2 tornillos)", "V"))
    return objs


def roof_details(M):
    objs = []
    for name in ("INT_SunVisor_L", "INT_SunVisor_R", "INT_Rearview_Mirror"):
        o = obj(name)
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        c = V(s * 0.40, 0.90, S.z_top(0.90) - 0.055)
        P.rbox(mb, c, (0.37, 0.17, 0.022), 0.010, 2, rot_x(16), 0)
        P.cyl(mb, c + V(-s * 0.19, 0.07, 0.02), c + V(-s * 0.19, 0.07, 0.05), 0.006, 10, 1)
        P.rbox(mb, c + V(0, -0.002, -0.012), (0.20, 0.10, 0.003), 0.002, 1, rot_x(16), 2)
        objs.append(P.make(mb, f"INT_SunVisor_{sd}", "INTERIOR_TRIM", [M["headliner"], M["int_plastic"], M["mirror"]],
                           None, (0, 0, 1), 0.30, 2, "Guarnecidos",
                           "Parasol con espejo y cortinilla (2 tornillos de 10 mm)", "V"))
        # guarnecido del larguero, gancho de abrigo y luz de lectura trasera
        mb = L.MeshBuilder()
        p = V(s * (B.roof_hw(-0.55) - 0.07), -0.55, S.z_top(-0.55) - 0.09)
        P.rbox(mb, p, (0.03, 0.05, 0.03), 0.008, 2, None, 0)
        P.rbox(mb, p + V(0, 0.08, 0.0), (0.03, 0.06, 0.015), 0.005, 1, None, 1)
        objs.append(P.make(mb, f"INT_Coathook_Maplight_{sd}", "INTERIOR_TRIM", [M["int_plastic"], M["led_white"]],
                           None, (-s * 0.3, 0, 1), 0.30, 6, "Guarnecidos", "Gancho de abrigo y luz de lectura", "V"))
    # retrovisor interior sin marco con brazo y cámara de habitáculo
    mb = L.MeshBuilder()
    c = V(0.0, 0.64, S.z_top(0.64) - 0.12)
    P.rbox(mb, c, (0.25, 0.022, 0.065), 0.014, 3, None, 0)
    P.cyl(mb, c + V(0, 0.01, 0.03), c + V(0, 0.03, 0.10), 0.009, 12, 0)
    P.rbox(mb, c + V(0, 0.036, 0.11), (0.06, 0.03, 0.03), 0.006, 1, None, 0)
    objs.append(P.make(mb, "INT_Rearview_Mirror", "INTERIOR_TRIM", M["int_plastic"], None, (0, -0.3, 1), 0.40, 2,
                       "Guarnecidos", "Retrovisor interior sin marco con brazo (2 N·m)", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, c + V(0, -0.012, -0.0), (0.24, 0.003, 0.058), 0.010, 2, None, 0)
    objs.append(P.make(mb, "INT_Rearview_Mirror_Glass", "INTERIOR_TRIM", M["mirror"], None, (0, -1, 0.5), 0.45, 6,
                       "Guarnecidos", "Espejo electrocrómico del retrovisor interior", "V"))
    mb = L.MeshBuilder()
    P.rbox(mb, c + V(0, 0.05, 0.075), (0.05, 0.03, 0.025), 0.006, 1, None, 0)
    L.lathe(mb, [(0.0, 0.0), (0.006, 0.0), (0.006, 0.004), (0.0, 0.005)], tuple(c + V(0, 0.034, 0.075)), (0, -1, 0),
            12, 1)
    objs.append(P.make(mb, "CAM_Interior", "BODY_FASTENERS", [M["plastic_black"], M["glass_lens_smoke"]], None,
                       (0, -0.3, 1), 0.45, 6, "Cámaras", "Cámara interior del habitáculo", "V"))
    # radar de habitáculo y altavoces del larguero trasero
    mb = L.MeshBuilder()
    P.rbox(mb, (0.0, -0.40, S.z_top(-0.40) - 0.04), (0.09, 0.06, 0.015), 0.004, 1, None, 0)
    objs.append(P.make(mb, "INT_Cabin_Radar", "INTERIOR_TRIM", M["int_plastic"], None, (0, 0, 1), 0.30, 6,
                       "Electrónica", "Radar de habitáculo (detección de ocupantes)", "V"))
    mb = L.MeshBuilder()
    for x in (-0.45, 0.45):
        c2 = V(x, -0.90, S.z_top(-0.90) - 0.07)
        P.rbox(mb, c2, (0.16, 0.05, 0.035), 0.008, 1, None, 0)
        P.rbox(mb, c2 + V(0, 0.026, -0.005), (0.13, 0.003, 0.025), 0.004, 1, None, 1)
    objs.append(P.make(mb, "INT_Speakers_Rear_Header", "INTERIOR_TRIM", [M["headliner"], M["speaker_mesh"]], None,
                       (0, -0.3, 1), 0.30, 6, "Audio", "Altavoces del larguero trasero", "V"))
    return objs


# ---------------------------------------------------------------------------
# Paneles de puerta completos
# ---------------------------------------------------------------------------
def door_trim_detail(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        for key, (yf, yr) in (("F", (S.DOOR_F_FRONT_Y - 0.02, S.DOOR_B_SEAM_Y + 0.01)),
                              ("R", (S.DOOR_B_SEAM_Y - 0.01, S.DOOR_R_REAR_Y + 0.01))):
            tag = f"{key}{sd}"
            door = obj(f"DOOR_{tag}")
            for name in (f"INT_DoorTrim_{tag}", f"INT_DoorArmrest_{tag}", f"INT_DoorPocket_{tag}",
                         f"INT_DoorSpeaker_{tag}"):
                o = obj(name)
                if o is not None:
                    bpy.data.objects.remove(o, do_unlink=True)
            xw = s * (0.805 if key == "F" else 0.790)          # cara interior de la estructura
            zt = S.z_belt((yf + yr) / 2) - 0.02
            yfa = yf - (0.10 if key == "F" else 0.0)
            ym = (yfa + yr) / 2
            ln = abs(yfa - yr)
            # panel principal: zona superior (cintura), panel medio y parte inferior con bolsillo
            mb = L.MeshBuilder()
            P.hull(mb, [V(xw, yfa, FLOOR_Z + 0.04), V(xw, yr, FLOOR_Z + 0.04), V(xw, yfa, zt), V(xw, yr, zt),
                        V(xw - s * 0.030, yfa - 0.01 * s * 0, FLOOR_Z + 0.06), V(xw - s * 0.030, yr, FLOOR_Z + 0.06),
                        V(xw - s * 0.040, yfa, zt - 0.10), V(xw - s * 0.040, yr, zt - 0.10),
                        V(xw - s * 0.022, yfa, zt - 0.01), V(xw - s * 0.022, yr, zt - 0.01)], 0)
            objs.append(P.make(mb, f"INT_DoorTrim_{tag}", "INTERIOR_DOORS", M["int_grey"], door, (-s, 0, 0), 0.30, 2,
                               "Paneles de puerta", "Panel de guarnecido de la puerta (14 grapas y 3 tornillos)", "V",
                               bevel=0.008))
            # moldura de cintura con tira de luz ambiental
            mb = L.MeshBuilder()
            P.rbox(mb, V(xw - s * 0.030, ym, zt - 0.035), (0.020, ln - 0.02, 0.05), 0.006, 2, None, 0)
            P.rbox(mb, V(xw - s * 0.041, ym, zt - 0.062), (0.003, ln - 0.06, 0.004), 0.001, 1, None, 1)
            objs.append(P.make(mb, f"INT_Door_Beltline_{tag}", "INTERIOR_DOORS", [M["leather"], M["led_white"]], door,
                               (-s, 0, 0.3), 0.36, 6, "Paneles de puerta",
                               "Moldura de cintura (Beltline) con luz ambiental", "V"))
            # reposabrazos con botonera de ventanillas y pulsador de apertura
            mb = L.MeshBuilder()
            P.rbox(mb, V(xw - s * 0.0815, ym - 0.03, 0.83), (0.09, ln * 0.55, 0.045), 0.018, 3, None, 0)
            objs.append(P.make(mb, f"INT_DoorArmrest_{tag}", "INTERIOR_DOORS", M["leather"], door, (-s, 0, 0), 0.40, 6,
                               "Paneles de puerta", "Reposabrazos acolchado de la puerta", "V"))
            mb = L.MeshBuilder()
            nsw = 4 if (key == "F" and s < 0) else 1
            for k in range(nsw):
                P.rbox(mb, V(xw - s * 0.09, ym + 0.10 - k * 0.032, 0.857), (0.026, 0.024, 0.010), 0.003, 1, None, 0)
            objs.append(P.make(mb, f"INT_Door_Window_Switches_{tag}", "INTERIOR_DOORS", M["int_plastic"], door,
                               (-s, 0, 0.5), 0.45, 6, "Paneles de puerta",
                               "Interruptores de ventanilla" + (" (botonera del conductor)" if nsw > 1 else ""), "V"))
            # bolsillo con luz ambiental, rejilla del altavoz, luz de cortesía y catadióptrico
            mb = L.MeshBuilder()
            P.rbox(mb, V(xw - s * 0.059, ym + 0.05, FLOOR_Z + 0.12), (0.05, ln * 0.70, 0.11), 0.008, 2, None, 0)
            P.rbox(mb, V(xw - s * 0.0855, ym + 0.05, FLOOR_Z + 0.16), (0.003, ln * 0.62, 0.003), 0.001, 1, None, 1)
            objs.append(P.make(mb, f"INT_DoorPocket_{tag}", "INTERIOR_DOORS", [M["int_plastic"], M["led_white"]], door,
                               (-s, 0, -0.3), 0.38, 6, "Paneles de puerta", "Bolsillo con luz ambiental", "V"))
            mb = L.MeshBuilder()
            L.lathe(mb, [(0.0, 0.0), (0.055, 0.0), (0.055, 0.006), (0.0, 0.008)],
                    (xw - s * 0.0345, ym - 0.12, 0.744), (-s, 0, 0), 40, 0)
            objs.append(P.make(mb, f"INT_DoorSpeaker_{tag}", "INTERIOR_DOORS", M["speaker_mesh"], door, (-s, 0, 0),
                               0.42, 6, "Audio",
                               "Rejilla del subwoofer de la puerta" if key == "F" else "Rejilla del altavoz de la puerta",
                               "V"))
            mb = L.MeshBuilder()
            P.rbox(mb, V(xw - s * 0.0335, ym, FLOOR_Z + 0.055), (0.003, 0.08, 0.008), 0.001, 1, None, 0)
            P.rbox(mb, V(xw - s * 0.0335, yr + 0.03, FLOOR_Z + 0.12), (0.003, 0.03, 0.05), 0.001, 1, None, 1)
            objs.append(P.make(mb, f"INT_Door_Lamps_{tag}", "INTERIOR_DOORS", [M["led_white"], M["glass_lens_red"]], door,
                               (-s, 0, -0.5), 0.32, 6, "Paneles de puerta",
                               "Luz de cortesía inferior y catadióptrico de la puerta", "V"))
    return objs


# ---------------------------------------------------------------------------
# Asientos: guías, laterales con botones, carcasas traseras, costuras proyectadas
# ---------------------------------------------------------------------------
def _bvh(o):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    verts = [mw @ v.co for v in me.vertices]
    polys = [list(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys)


def _project_line(tree, a, b, ray_dir, n=24, lift=0.0008):
    """Proyecta un segmento sobre la superficie a lo largo de ray_dir y devuelve la polilínea."""
    a, b, d = Vector(a), Vector(b), Vector(ray_dir).normalized()
    out = []
    for i in range(n + 1):
        p = a.lerp(b, i / n)
        hit, nrm, _, _ = tree.ray_cast(p - d * 0.3, d, 0.8)
        if hit is not None:
            out.append(hit + nrm * lift)
    return out


def seat_details(M):
    objs = []
    bpy.context.view_layer.update()
    for s, sd in ((1, "R"), (-1, "L")):
        asm = obj(f"SEAT_FRONT_{sd}")
        x = s * SEAT_X
        hy, hz = H_FRONT
        # guías del asiento (2 carriles), elevadores y 4 tornillos T45P
        mb = L.MeshBuilder()
        for dx in (-0.19, 0.19):
            P.rbox(mb, (x + dx, hy + 0.16, FLOOR_Z + 0.03), (0.03, 0.62, 0.035), 0.004, 1, None, 0)
            P.rbox(mb, (x + dx, hy + 0.16, FLOOR_Z + 0.065), (0.02, 0.50, 0.035), 0.004, 1, None, 1)
            for dy in (-0.14, 0.44):
                P.torx_screw(mb, (x + dx, hy + dy, FLOOR_Z + 0.048), (0, 0, 1), 0.007, 2)
        P.rbox(mb, (x, hy + 0.47, FLOOR_Z + 0.02), (0.42, 0.04, 0.03), 0.004, 1, None, 1)
        objs.append(P.make(mb, f"INT_SeatF_{sd}_Tracks", "INTERIOR_SEATS", [M["steel_black"], M["steel_bare"], M["zinc"]],
                           asm, (0, 0, -1), 0.18, 6, "Asientos",
                           "Guías eléctricas y elevadores del asiento (4 tornillos T45P a 34 N·m)", "V"))
        # escudo lateral exterior con botones de ajuste (cojín, respaldo, lumbar)
        mb = L.MeshBuilder()
        xo = x + s * 0.255
        # bajo el cojín (z ≤ 0,675): cubre el costado de la bandeja y los mecanismos
        P.hull(mb, [V(xo, hy + 0.48, FLOOR_Z + 0.09), V(xo, hy - 0.05, FLOOR_Z + 0.09), V(xo, hy + 0.46, 0.675),
                    V(xo, hy - 0.06, 0.675), V(xo - s * 0.025, hy + 0.48, FLOOR_Z + 0.09),
                    V(xo - s * 0.025, hy - 0.05, FLOOR_Z + 0.09), V(xo - s * 0.025, hy + 0.46, 0.675),
                    V(xo - s * 0.025, hy - 0.06, 0.675)], 0)
        objs.append(P.make(mb, f"INT_SeatF_{sd}_Side_Shield", "INTERIOR_SEATS", M["int_plastic"], asm, (s, 0, 0), 0.20, 6,
                           "Asientos", "Escudo lateral exterior del asiento", "V", bevel=0.005))
        mb = L.MeshBuilder()
        P.rbox(mb, V(xo + s * 0.005, hy + 0.25, 0.640), (0.010, 0.14, 0.022), 0.006, 2, None, 0)
        P.rbox(mb, V(xo + s * 0.005, hy + 0.05, 0.635), (0.010, 0.02, 0.06), 0.006, 2, None, 0)
        P.rbox(mb, V(xo + s * 0.005, hy + 0.10, 0.635), (0.010, 0.035, 0.035), 0.010, 2, None, 0)
        objs.append(P.make(mb, f"INT_SeatF_{sd}_Buttons", "INTERIOR_SEATS", M["alu_trim"], asm, (s, 0, 0), 0.30, 6,
                           "Asientos", "Mandos de ajuste del cojín, del reclinado y lumbar de 8 vías", "V"))
        # carcasa trasera rígida del respaldo
        back = obj(f"INT_SeatF_{sd}_Back")
        if back is not None:
            tilt = rot_x(22)
            b0 = V(x, hy - 0.04, hz - 0.02)
            mb = L.MeshBuilder()
            pts = []
            for (h, w) in ((0.14, 0.24), (0.45, 0.25), (0.62, 0.16), (0.82, 0.14)):
                for sg in (1, -1):
                    for dd in (-0.118, -0.098):        # por detrás del tapizado (que el subsurf encoge)
                        pts.append(b0 + tilt @ V(sg * w, dd, h))
            P.hull(mb, pts, 0)
            objs.append(P.make(mb, f"INT_SeatF_{sd}_Back_Shell", "INTERIOR_SEATS", M["int_plastic"], asm,
                               (0, -1, 0.2), 0.16, 6, "Asientos", "Carcasa trasera del respaldo", "R", bevel=0.006))
        # costuras proyectadas sobre el cojín y el respaldo (dobles pespuntes de los paneles)
        mb = L.MeshBuilder()
        cush = obj(f"INT_SeatF_{sd}_Cushion")
        if cush is not None:
            tree = _bvh(cush)
            cy = hy + 0.225
            for dx in (-0.13, -0.122, 0.122, 0.13):
                line = _project_line(tree, (x + dx, cy - 0.22, hz + 0.3), (x + dx, cy + 0.22, hz + 0.3), (0, 0, -1))
                if len(line) > 3:
                    P.sweep(mb, line, P.circle_profile(0.0011, 5), mat=0)
            for yy in (cy + 0.05, cy - 0.10):
                line = _project_line(tree, (x - 0.12, yy, hz + 0.3), (x + 0.12, yy, hz + 0.3), (0, 0, -1), 16)
                if len(line) > 3:
                    P.sweep(mb, line, P.circle_profile(0.0011, 5), mat=0)
        if back is not None:
            tree = _bvh(back)
            tilt = rot_x(22)
            b0 = V(x, hy - 0.04, hz - 0.02)
            fwd = tilt @ V(0, 1, 0)
            for dx in (-0.13, -0.122, 0.122, 0.13):
                a = b0 + tilt @ V(dx, 0.3, 0.06)
                b = b0 + tilt @ V(dx * 0.85, 0.3, 0.52)
                line = _project_line(tree, a, b, -fwd)
                if len(line) > 3:
                    P.sweep(mb, line, P.circle_profile(0.0011, 5), mat=0)
            for h in (0.24, 0.40):
                a = b0 + tilt @ V(-0.12, 0.3, h)
                b = b0 + tilt @ V(0.12, 0.3, h)
                line = _project_line(tree, a, b, -fwd, 16)
                if len(line) > 3:
                    P.sweep(mb, line, P.circle_profile(0.0011, 5), mat=0)
        o = P.make(mb, f"INT_SeatF_{sd}_Stitching", "INTERIOR_SEATS", M["stitch"], asm, (0, 0.2, 1), 0.12, 6, "Asientos",
                   "Costuras dobles de los paneles del asiento", "R")
        if o is not None:
            objs.append(o)
    # asiento trasero: reposabrazos central con portavasos, reposacabezas y costuras
    asm = obj("SEAT_REAR")
    hy, hz = H_REAR
    mb = L.MeshBuilder()
    tilt = rot_x(REAR_TILT)
    # reposabrazos plegado: apoyado delante del respaldo central (no dentro de él)
    c = V(0.0, hy - 0.06, hz - 0.02) + tilt @ V(0, 0.045, 0.35)
    P.rbox(mb, c, (0.20, 0.06, 0.30), 0.02, 2, tilt, 0)
    objs.append(P.make(mb, "INT_SeatR_Armrest", "INTERIOR_SEATS", M["leather"], asm, (0, -0.3, 1), 0.25, 6, "Asientos",
                       "Reposabrazos central trasero (abatible)", "V"))
    mb = L.MeshBuilder()
    for dx in (-0.045, 0.045):
        L.lathe(mb, [(0.0, 0.0), (0.035, 0.0), (0.037, 0.004), (0.035, -0.06), (0.0, -0.062)],
                tuple(c + tilt @ V(dx, 0.032, 0.08)), tuple(tilt @ V(0, 1, 0)), 20, 0)
    objs.append(P.make(mb, "INT_SeatR_Armrest_Cupholders", "INTERIOR_SEATS", M["int_plastic"], asm, (0, -0.3, 1), 0.32, 6,
                       "Asientos", "Portavasos del reposabrazos trasero (embellecedor)", "V"))
    for nm in ("L", "C", "R"):
        o = obj(f"INT_SeatR_{nm}_Headrest")
        if o is not None:
            loc = o.matrix_world.translation.copy()
            bpy.data.objects.remove(o, do_unlink=True)
            mb = L.MeshBuilder()
            P.rbox(mb, loc, (0.25, 0.085, 0.15), 0.035, 3, tilt, 0)
            for dx in (-0.06, 0.06):
                P.cyl(mb, loc + tilt @ V(dx, 0, -0.07), loc + tilt @ V(dx, 0, -0.12), 0.006, 10, 1)
            objs.append(P.make(mb, f"INT_SeatR_{nm}_Headrest", "INTERIOR_SEATS", [M["leather"], M["alu_trim"]], asm,
                               (0, -0.3, 1), 0.15, 6, "Asientos", "Reposacabezas trasero con varillas", "V"))
    mb = L.MeshBuilder()
    for nm, xs in (("L", -0.45), ("C", 0.0), ("R", 0.45)):
        cush = obj(f"INT_SeatR_{nm}_Cushion")
        if cush is None:
            continue
        tree = _bvh(cush)
        cy = hy + 0.21
        for dx in (-0.12, 0.12):
            line = _project_line(tree, (xs + dx, cy - 0.20, hz + 0.3), (xs + dx, cy + 0.20, hz + 0.3), (0, 0, -1))
            if len(line) > 3:
                P.sweep(mb, line, P.circle_profile(0.0011, 5), mat=0)
    o = P.make(mb, "INT_SeatR_Stitching", "INTERIOR_SEATS", M["stitch"], asm, (0, 0.2, 1), 0.12, 6, "Asientos",
               "Costuras de los cojines traseros", "R")
    if o is not None:
        objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Cinturones de seguridad
# ---------------------------------------------------------------------------
def seatbelts(M):
    objs = []
    for s, sd in ((1, "R"), (-1, "L")):
        # enrollador alojado en el guarnecido del pilar (x 0,700…0,748) y cinta por delante de su cara interior
        for row, yb, xr in (("F", S.DOOR_B_SEAM_Y - 0.035, 0.728), ("R", S.CAB_REAR_Y + 0.05, 0.724)):
            o = obj(f"INT_Seatbelt_{row}{sd}")
            if o is not None:
                bpy.data.objects.remove(o, do_unlink=True)
            xw = s * 0.697
            top = V(xw, yb, 1.48 if row == "F" else 1.40)
            low = V(s * xr, yb + 0.02, FLOOR_Z + 0.10)
            mb = L.MeshBuilder()
            # cinta recogida a lo largo del pilar, guía superior (webguide) y lengüeta
            P.sweep(mb, [V(xw, yb + 0.02, FLOOR_Z + 0.16), top + V(0, 0, -0.02)], P.rect_profile(0.048, 0.0015),
                    up=(s, 0, 0), mat=0)
            P.rbox(mb, top + V(-s * 0.010, 0, 0.012), (0.018, 0.06, 0.045), 0.006, 2, None, 1)
            P.rbox(mb, top + V(-s * 0.006, 0, -0.07), (0.008, 0.05, 0.07), 0.004, 1, None, 2)
            # enrollador con pretensor (oculto dentro del guarnecido) y anclaje inferior
            P.rbox(mb, low, (0.036, 0.08, 0.11), 0.006, 1, None, 1)
            P.flange_bolt(mb, low + V(-s * 0.018, 0, 0.03), (-s, 0, 0), 0.010, 3)
            objs.append(P.make(mb, f"INT_Seatbelt_{row}{sd}", "INTERIOR_SEATS",
                               [M["seatbelt"], M["int_plastic"], M["alu_trim"], M["zinc"]], None, (0, 0, 1), 0.3, 6,
                               "Cinturones",
                               "Cinturón de tres puntos: cinta, guía, lengüeta, enrollador con pretensor y anclaje", "V"))
    # hebillas: delanteras en el lado interior del asiento, traseras sobre el cojín
    mb = L.MeshBuilder()
    for s in (1, -1):
        b = V(s * (SEAT_X - 0.27), H_FRONT[0] + 0.02, H_FRONT[1] - 0.02)
        P.beam(mb, b + V(0, 0.02, -0.18), b, 0.03, 0.012, up=(1, 0, 0), r=0.003)
        P.rbox(mb, b + V(0, -0.005, 0.03), (0.022, 0.04, 0.07), 0.006, 2, None, 0)
    for x in (-0.62, -0.30, -0.15, 0.15, 0.30, 0.62):
        b = V(x, H_REAR[0] + 0.02, H_REAR[1] - 0.04)
        P.rbox(mb, b, (0.020, 0.035, 0.06), 0.006, 2, None, 0)
    o = P.make(mb, "INT_Seatbelt_Buckles", "INTERIOR_SEATS", M["int_plastic"], None, (0, 0, 1), 0.35, 6, "Cinturones",
               "Hebillas de los cinturones (delanteras con pretensor de cadera)", "V")
    objs.append(o)
    return objs


# ---------------------------------------------------------------------------
# Alfombrillas para todo tipo de clima
# ---------------------------------------------------------------------------
def floor_mats(M):
    """Alfombrillas con el contorno del hueco de los pies: las delanteras entre el umbral y la consola, delante de
    los carriles del asiento y detrás de las tapas del suelo (reposapiés, tapa de pirofusibles); la trasera en U,
    con escotadura para el final de la consola y por delante del bajo de la banqueta."""
    objs = []
    # (nombre, piezas rectangulares (x, y, ancho, largo))
    mats = (("FL", [(-0.42, 0.925, 0.52, 0.21)]),
            ("FR", [(0.42, 0.985, 0.52, 0.33)]),
            ("R", [(0.43, -0.025, 0.54, 0.31), (-0.43, -0.025, 0.54, 0.31), (0.0, -0.165, 0.32, 0.03)]))
    for nm, pieces in mats:
        o = obj(f"INT_FloorMat_{nm}")
        if o is not None:
            bpy.data.objects.remove(o, do_unlink=True)
        mb = L.MeshBuilder()
        for (x, y, w, l) in pieces:
            P.rbox(mb, (x, y, FLOOR_Z + 0.016), (w, l, 0.008), 0.003, 1, None, 0)
            if l < 0.08:
                continue
            nrib = int(w / 0.045)
            for i in range(nrib):
                xx = x - w / 2 + 0.03 + i * (w - 0.06) / max(1, nrib - 1)
                P.rbox(mb, (xx, y, FLOOR_Z + 0.022), (0.010, l - 0.08, 0.005), 0.002, 1, None, 0)
            P.sweep(mb, [(x - w / 2 + 0.01, y - l / 2 + 0.01, FLOOR_Z + 0.024), (x + w / 2 - 0.01, y - l / 2 + 0.01, FLOOR_Z + 0.024),
                         (x + w / 2 - 0.01, y + l / 2 - 0.01, FLOOR_Z + 0.024), (x - w / 2 + 0.01, y + l / 2 - 0.01, FLOOR_Z + 0.024),
                         (x - w / 2 + 0.01, y - l / 2 + 0.01, FLOOR_Z + 0.024)], P.rect_profile(0.012, 0.012, 0.003, 1))
        objs.append(P.make(mb, f"INT_FloorMat_{nm}", "INTERIOR_TRIM", M["composite"], None, (0, 0, 1), 0.12, 6,
                           "Guarnecidos", "Alfombrilla para todo tipo de clima con nervios y reborde", "V"))
    return objs


def build_all(M):
    out = []
    out += steering_wheel_detail(M)
    out += console_detail(M)
    out += dashboard_detail(M)
    out += pillar_trims(M)
    out += roof_details(M)
    out += door_trim_detail(M)
    out += seat_details(M)
    out += seatbelts(M)
    out += floor_mats(M)
    return [o for o in out if o is not None]
