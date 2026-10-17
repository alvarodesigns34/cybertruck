"""Versión 4 · interior del tren motriz: motores, reductoras, inversores, semiejes y rodamientos de buje.

Hasta la versión 3 las unidades motrices eran carcasas cerradas. Aquí se añade lo que las hace funcionar,
colocado dentro de esas carcasas y con su propia dirección de explosión (las carcasas se apartan más que
su contenido, como en un despiece de taller):

  Unidad delantera (motor síncrono de imanes permanentes, [V] manual del propietario):
    estátor de chapa magnética con devanado de horquillas, rotor de imanes, eje, rodamientos, resolver,
    tren de engranajes helicoidales de dos etapas, diferencial abierto con satélites y planetarios,
    rodamientos, retenes, ejes de salida estriados, bloqueo electromagnético y fase de potencia.
  Unidad trasera (dos motores de inducción con reductoras independientes, [R] Munro vía The Autopian):
    por lado, estátor con devanado distribuido, rotor de jaula de cobre, eje, rodamientos, tren de dos
    etapas sin diferencial (vectorización de par) y eje de salida.
  Inversores: placa fría, módulos de potencia sobre sustrato cerámico, condensador del bus de continua,
    placas de excitación y de control, barras de fase con sensores de corriente.
  Semiejes: juntas homocinéticas interior (trípode) y exterior (Rzeppa de 6 bolas), abrazaderas de los
    fuelles y tornillo central de 24 mm a 300 N·m [V].
  Bujes: rodamiento de doble hilera de bolas dentro del portamangueta.

Fidelidad: existencia y función [V]/[R]; número de dientes, ranuras, bolas y dimensiones interiores son
reconstrucciones de ingeniería («Aproximado»): no hay planos ni cifras publicadas de estas piezas internas.
La relación global 15,02:1 [V] no se reproduce con los radios dibujados, que están limitados por la carcasa
reconstruida.
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v4 as V4
from ct_v4 import (gear, ring_gear, spline, sphere, bearing, taper, tube, screw, pcb, stator, hairpins,
                   winding, hose_clamp, fins, box, cyl, ring, disc, hull, beam, bolt, nut, torx)

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
WZ = S.WHEEL_CENTER_Z
NOTE_INT = ("Pieza interior necesaria para el funcionamiento; forma, dimensiones y número de dientes/ranuras "
            "reconstruidos (no hay planos publicados)")


def _yz(y, z, x):
    return (x, y, z)


# ---------------------------------------------------------------------------
# Unidad motriz delantera
# ---------------------------------------------------------------------------
def front_unit(M):
    out = []
    A = out.extend
    yf = S.Y_FRONT_AXLE
    ym, zm = yf + 0.20, 0.465                       # eje del motor (igual que la carcasa de la v2)
    yi, zi = yf + 0.11, 0.400                       # eje intermedio
    yd, zd = yf, WZ                                 # eje del diferencial (= eje de rueda)
    par = "DRIVE_UNIT_FRONT"
    sysn = "DRIVE_UNITS"
    grp = "Unidad motriz delantera"

    # Las carcasas se apartan más que su contenido (despiece de taller)
    V4.set_explode("DU_F_Motor_Housing", (-1, 0.15, 0.1), 0.62, 5)
    V4.set_explode("DU_F_NVH_Cover", (-1, 0.6, 0.6), 0.75, 5)
    V4.set_explode("DU_F_Gearbox", (1, 0, 0.05), 0.55, 5)
    V4.set_explode("DU_F_Inverter", (0, 0, 1), 0.62, 5)

    # --- motor síncrono de imanes permanentes ------------------------------------------------------------
    xc, Ls = -0.16, 0.150
    A(V4.part(M, "DU_F_Stator_Core", sysn, ["elec_steel"], [
        stator((xc, ym, zm), X, 0.068, 0.112, Ls, 48, 0.024),
        # ranuras de las soldaduras longitudinales del paquete (4 cordones exteriores)
        [beam((xc - Ls / 2, ym + 0.112 * math.cos(a), zm + 0.112 * math.sin(a)),
              (xc + Ls / 2, ym + 0.112 * math.cos(a), zm + 0.112 * math.sin(a)), 0.006, 0.003,
              up=(0, math.cos(a), math.sin(a)), r=0.0) for a in (0.4, 2.0, 3.5, 5.1)],
    ], "Paquete de chapa magnética del estátor (48 ranuras, chapas de acero al silicio soldadas)",
        parent=par, edir=(-1, 0, 0), dist=0.30, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Stator_Hairpins", sysn, ["copper_enamel", "copper", "nylon"], [
        hairpins((xc, ym, zm), X, 0.074, 0.090, Ls, 48, 0.030, 0, 2, 1),
        hairpins((xc, ym, zm), X, 0.074, 0.090, Ls, 48, 0.022, 0, 2, -1),
        # terminales de las tres fases soldados a las barras de salida
        [box((xc + Ls / 2 + 0.028, ym + 0.02 * k, zm + 0.092), (0.012, 0.010, 0.016), 0.002, 1) for k in (-1, 0, 1)],
        # aislante de ranura (papel de aramida) asomando en los extremos
        ring((xc + Ls / 2 + 0.002, ym, zm), X, 0.068, 0.092, 0.004, 48, 2),
        ring((xc - Ls / 2 - 0.002, ym, zm), X, 0.068, 0.092, 0.004, 48, 2),
    ], "Devanado de horquillas de cobre esmaltado (cabezas de bobina, terminales de fase y aislantes de ranura)",
        parent=par, edir=(-1, 0, 0), dist=0.30, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Phase_Busbars", sysn, ["copper", "nylon", "zinc"], [
        [beam((xc + Ls / 2 + 0.028, ym + 0.02 * k, zm + 0.100), (0.03, ym - 0.03 + 0.03 * k, 0.600), 0.010, 0.004,
              up=(1, 0, 0)) for k in (-1, 0, 1)],
        box((0.03, ym - 0.03, 0.585), (0.04, 0.11, 0.020), 0.003, 1),
        [bolt((0.03, ym - 0.03 + 0.03 * k, 0.602), Z, 0.006, 2) for k in (-1, 0, 1)],
    ], "Barras de fase del motor al inversor (3 fases, pasamuros aislante y tornillos de 10 mm)",
        parent=par, edir=(0, 0, 1), dist=0.38, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Rotor", sysn, ["elec_steel", "alu_machined", "magnet"], [
        cyl((xc - Ls / 2, ym, zm), (xc + Ls / 2, ym, zm), 0.0665, seg=48, m=0),
        disc((xc - Ls / 2 - 0.004, ym, zm), X, 0.064, 0.008, 48, 1),
        disc((xc + Ls / 2 + 0.004, ym, zm), X, 0.064, 0.008, 48, 1),
        # agujeros de equilibrado (taladros de material retirado en las placas extremas)
        [cyl((xc + Ls / 2 + 0.0081, ym + 0.048 * math.cos(a), zm + 0.048 * math.sin(a)),
             (xc + Ls / 2 + 0.0083, ym + 0.048 * math.cos(a), zm + 0.048 * math.sin(a)), 0.0035, seg=10, m=2)
         for a in (0.3, 0.9)],
    ], "Rotor de imanes permanentes (chapas con imanes de NdFeB en V y placas extremas de equilibrado)",
        parent=par, edir=(-1, 0, 0), dist=0.46, stage=6, group=grp, fid="A", note=NOTE_INT))
    # imanes en V (8 polos x 2), dentro del paquete del rotor
    mags = []
    for k in range(8):
        a = 2 * math.pi * k / 8
        for sg in (-1, 1):
            b = a + sg * 0.16
            d = Vector((0, math.cos(b), math.sin(b)))
            c = Vector((xc, ym, zm)) + d * 0.050
            # imán orientado en V: largo = paquete, ancho tangencial 17 mm, espesor radial 4,5 mm
            mags.append(beam(tuple(c - Vector((Ls / 2 - 0.002, 0, 0))), tuple(c + Vector((Ls / 2 - 0.002, 0, 0))),
                             0.017, 0.0045, up=tuple(d)))
    A(V4.part(M, "DU_F_Rotor_Magnets", sysn, ["magnet"], mags,
              "Imanes permanentes de NdFeB niquelados del rotor (8 polos en V)",
              parent=par, edir=(-1, 0, 0), dist=0.46, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Rotor_Shaft", sysn, ["gear_steel", "bearing_steel"], [
        cyl((-0.315, ym, zm), (0.075, ym, zm), 0.0175, seg=24, m=0),
        cyl((xc - Ls / 2 - 0.01, ym, zm), (xc + Ls / 2 + 0.01, ym, zm), 0.024, seg=24, m=0),
        spline((0.07, ym, zm), X, 0.0175, 0.012, 22, 0.0011, 0.0, 0),
        # canal de aceite axial (boca del rociador en el extremo)
        ring((-0.317, ym, zm), X, 0.006, 0.0175, 0.004, 16, 1),
    ], "Eje del rotor hueco con estriado de salida (refrigeración por aceite interior)",
        parent=par, edir=(-1, 0, 0), dist=0.40, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Rotor_Bearings", sysn, ["bearing_steel", "nylon"], [
        bearing((-0.018, ym, zm), X, 0.0175, 0.034, 0.017, 10),
        bearing((-0.296, ym, zm), X, 0.0175, 0.031, 0.014, 9),
    ], "Rodamientos del rotor (lado reductora y lado tapa; aislados contra corrientes de eje)",
        parent=par, edir=(-1, 0, 0.25), dist=0.52, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Resolver", sysn, ["elec_steel", "copper_enamel", "connector_grey"], [
        ring((-0.307, ym, zm), X, 0.032, 0.050, 0.010, 32, 0),
        ring((-0.307, ym, zm), X, 0.0176, 0.026, 0.010, 24, 0),
        [box((-0.307, ym + 0.041 * math.cos(2 * math.pi * k / 12), zm + 0.041 * math.sin(2 * math.pi * k / 12)),
             (0.012, 0.006, 0.006), 0.001, 1) for k in range(12)],
        box((-0.307, ym, zm + 0.058), (0.012, 0.022, 0.012), 0.002, 2),
    ], "Resolver de posición del rotor (estátor bobinado y rotor de chapas)",
        parent=par, edir=(-1, 0, 0.4), dist=0.58, stage=6, group=grp, fid="A", note=NOTE_INT))

    # --- reductora de dos etapas y diferencial -----------------------------------------------------------
    A(V4.part(M, "DU_F_Input_Gear", sysn, ["gear_steel"], [
        gear((0.040, ym, zm), X, 0.0255, 0.0290, 0.038, 19, 0.0172, 24.0),
        ring((0.040, ym, zm), X, 0.0172, 0.022, 0.044, 24, 0),
    ], "Piñón de entrada helicoidal (19 dientes, sobre el estriado del rotor)",
        parent=par, edir=(1, 0, 0.3), dist=0.22, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Intermediate_Shaft", sysn, ["gear_steel", "bearing_steel"], [
        gear((0.040, yi, zi), X, 0.0790, 0.0830, 0.034, 53, 0.020, -24.0),
        gear((0.118, yi, zi), X, 0.0255, 0.0300, 0.050, 17, 0.0, 22.0),
        cyl((0.006, yi, zi), (0.199, yi, zi), 0.018, seg=24, m=0),
        bearing((0.012, yi, zi), X, 0.018, 0.034, 0.016, 10, m=1),
        bearing((0.192, yi, zi), X, 0.018, 0.034, 0.016, 10, m=1),
    ], "Eje intermedio: rueda helicoidal de 53 dientes, piñón de 17 dientes y rodamientos",
        parent=par, edir=(1, 0.2, -0.3), dist=0.30, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Park_Lock", sysn, ["gear_steel", "steel_black", "copper_enamel", "connector_grey"], [
        gear((0.165, yi, zi), X, 0.036, 0.045, 0.016, 16, 0.018, 0.0),
        box((0.165, yi + 0.040, zi - 0.048), (0.014, 0.060, 0.012), 0.002, 1),
        cyl((0.165, yi + 0.075, zi - 0.06), (0.165, yi + 0.075, zi - 0.035), 0.004, seg=10, m=1),
        cyl((0.150, yi + 0.105, zi - 0.10), (0.215, yi + 0.105, zi - 0.10), 0.019, seg=20, m=2),
        box((0.228, yi + 0.105, zi - 0.10), (0.018, 0.026, 0.026), 0.003, 3),
    ], "Bloqueo electromagnético: rueda de bloqueo, trinquete y solenoide con conector",
        parent=par, edir=(1, 0.3, -0.5), dist=0.36, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Differential", sysn, ["gear_steel", "alu_cast", "bearing_steel"], [
        gear((0.118, yd, zd), X, 0.0820, 0.0860, 0.044, 61, 0.050, -22.0),
        # caja del diferencial abierta: brida, cubos y dos montantes que sujetan el eje de satélites
        disc((0.095, yd, zd), X, 0.060, 0.010, 40, 1),
        cyl((0.036, yd, zd), (0.095, yd, zd), 0.030, 0.034, 32, 1),
        cyl((0.150, yd, zd), (0.194, yd, zd), 0.044, 0.030, 32, 1),
        [beam((0.095, yd, zd + sg * 0.052), (0.150, yd, zd + sg * 0.046), 0.022, 0.010, up=(0, 0, 1)) for sg in (-1, 1)],
        cyl((0.124, yd, zd - 0.052), (0.124, yd, zd + 0.052), 0.0075, seg=14, m=0),
        # satélites (cónicos) y planetarios
        [taper((0.124, yd, zd + sg * 0.020), (0, 0, sg),
               [(0.0, 0.0), (0.016, 0.0), (0.024, 0.016), (0.017, 0.026), (0.0, 0.026)], 20, 0) for sg in (-1, 1)],
        [taper((0.124 + sg * 0.012, yd, zd), (sg, 0, 0),
               [(0.0, 0.0), (0.020, 0.0), (0.030, 0.020), (0.022, 0.030), (0.0, 0.030)], 24, 0) for sg in (-1, 1)],
        bearing((0.022, yd, zd), X, 0.030, 0.050, 0.018, 12, m=2),
        bearing((0.194, yd, zd), X, 0.030, 0.050, 0.018, 12, m=2),
    ], "Diferencial abierto: corona de 61 dientes, caja, eje y satélites, planetarios y rodamientos de rodillos",
        parent=par, edir=(1, -0.2, -0.4), dist=0.36, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Output_Shafts", sysn, ["gear_steel", "rubber_seal"], [
        cyl((-0.040, yd, zd), (0.105, yd, zd), 0.0165, seg=22, m=0),
        spline((-0.024, yd, zd), X, 0.0165, 0.030, 26, 0.0012, 0.0, 0),
        cyl((0.148, yd, zd), (0.240, yd, zd), 0.0165, seg=22, m=0),
        spline((0.226, yd, zd), X, 0.0165, 0.030, 26, 0.0012, 0.0, 0),
        ring((-0.004, yd, zd), X, 0.0170, 0.034, 0.008, 28, 1),
        ring((0.209, yd, zd), X, 0.0170, 0.034, 0.008, 28, 1),
    ], "Ejes de salida estriados y retenes de aceite (izquierdo y derecho)",
        parent=par, edir=(0.2, 0, -1), dist=0.30, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Gearbox_Cover_Bolts", sysn, ["zinc"], [
        [screw((0.209, yf + 0.06 + math.cos(2 * math.pi * k / 14) * 0.17, 0.45 + math.sin(2 * math.pi * k / 14) * 0.13),
               X, 0.008, 0.030, 0, "flange") for k in range(14)],
    ], "Tornillos de la tapa de la reductora (14 × M8 con brida)",
        parent=par, edir=(1, 0, 0.05), dist=0.75, stage=6, group=grp, fid="A", note=NOTE_INT))

    # --- inversor integrado -----------------------------------------------------------------------------
    xi0, yi0, zi0 = 0.10, yf + 0.10, 0.625
    A(V4.part(M, "DU_F_Inverter_ColdPlate", sysn, ["alu_cast", "zinc", "hose"], [
        box((xi0, yi0, 0.597), (0.225, 0.31, 0.008), 0.002, 0),
        fins((xi0, yi0, 0.591), Y, Z, (0.28, 0.20, 0.004), 22, 0.0015, 0),
        [cyl((xi0 + sx * 0.08, yi0 - 0.16, 0.600), (xi0 + sx * 0.08, yi0 - 0.20, 0.600), 0.008, seg=12, m=0) for sx in (-1, 1)],
    ], "Placa fría del inversor con aletas de aceite/refrigerante y racores",
        parent=par, edir=(0, 0, 1), dist=0.10, stage=6, group=grp, fid="A", note=NOTE_INT))
    mods = []
    for k in range(3):
        yy = yi0 - 0.10 + k * 0.075
        mods += [box((xi0 - 0.03, yy, 0.6025), (0.085, 0.060, 0.003), 0.0005, 0),
                 [box((xi0 - 0.06 + 0.02 * (j % 4), yy - 0.015 + 0.03 * (j // 4), 0.6045), (0.008, 0.008, 0.0008),
                      0.0, 1) for j in range(8)],
                 [beam((xi0 - 0.06 + 0.02 * (j % 4), yy - 0.015 + 0.03 * (j // 4), 0.6052),
                       (xi0 - 0.06 + 0.02 * (j % 4) + 0.006, yy - 0.015 + 0.03 * (j // 4) + 0.008, 0.6052),
                       0.0006, 0.0006, r=0.0, m=2) for j in range(8)],
                 box((xi0 + 0.025, yy, 0.607), (0.022, 0.040, 0.010), 0.001, 3)]
    A(V4.part(M, "DU_F_Inverter_Power_Modules", sysn, ["ceramic", "plastic_black", "alu_machined", "copper"], mods,
              "Módulos de potencia (3 semipuentes de SiC sobre sustrato cerámico con hilos de conexión)",
              parent=par, edir=(0, 0, 1), dist=0.20, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Inverter_DC_Capacitor", sysn, ["capacitor", "copper", "plastic_black"], [
        box((xi0 + 0.06, yi0, 0.618), (0.08, 0.27, 0.036), 0.003, 0),
        [box((xi0 + 0.02, yi0 - 0.10 + 0.075 * k, 0.612), (0.030, 0.024, 0.003), 0.0005, 1) for k in range(3)],
        box((xi0 + 0.06, yi0 + 0.15, 0.630), (0.05, 0.03, 0.012), 0.002, 2),
    ], "Condensador del bus de continua (película, encapsulado) con barras de conexión",
        parent=par, edir=(0, 0, 1), dist=0.27, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Inverter_Gate_Driver_PCB", sysn, ["pcb_green", "plastic_black", "capacitor", "connector_grey",
                                                         "solder_tin"], [
        pcb((xi0, yi0, 0.640), (0.21, 0.29, 0.0016), Z, X, 70, 11),
    ], "Placa de excitación de puerta (drivers aislados y fuentes de alimentación)",
        parent=par, edir=(0, 0, 1), dist=0.34, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Inverter_Control_PCB", sysn, ["pcb_green", "plastic_black", "capacitor", "connector_grey",
                                                     "solder_tin"], [
        pcb((xi0, yi0 + 0.02, 0.652), (0.18, 0.22, 0.0016), Z, X, 55, 12),
    ], "Placa de control del inversor (microcontrolador, CAN y conector de baja tensión)",
        parent=par, edir=(0, 0, 1), dist=0.42, stage=6, group=grp, fid="A", note=NOTE_INT))
    A(V4.part(M, "DU_F_Inverter_Current_Sensors", sysn, ["elec_steel", "copper", "connector_grey"], [
        [ring((xi0 - 0.085, yi0 - 0.10 + 0.075 * k, 0.612), Z, 0.008, 0.017, 0.010, 20, 0) for k in range(3)],
        [beam((xi0 - 0.085, yi0 - 0.10 + 0.075 * k, 0.604), (xi0 - 0.085, yi0 - 0.10 + 0.075 * k, 0.622), 0.010,
              0.004, up=(1, 0, 0), m=1) for k in range(3)],
        box((xi0 - 0.085, yi0 + 0.08, 0.612), (0.02, 0.04, 0.010), 0.002, 2),
    ], "Sensores de corriente de fase (núcleos de ferrita con efecto Hall)",
        parent=par, edir=(0, 0, 1), dist=0.22, stage=6, group=grp, fid="A", note=NOTE_INT))
    return out


# ---------------------------------------------------------------------------
# Unidad motriz trasera (dos motores de inducción, reductoras independientes)
# ---------------------------------------------------------------------------
def rear_unit(M):
    out = []
    A = out.extend
    yr = S.Y_REAR_AXLE
    ym, zm = yr - 0.19, 0.470
    yi, zi = yr - 0.11, 0.400
    yd, zd = yr, WZ
    par = "DRIVE_UNIT_REAR"
    sysn = "DRIVE_UNITS"
    grp = "Unidad motriz trasera"
    for sd, s in (("R", 1), ("L", -1)):
        V4.set_explode(f"DU_R_Motor_{sd}", (s, -0.15, 0.1), 0.62, 5)
        V4.set_explode(f"DU_R_Inverter_{sd}", (s * 0.2, -1, 0.5), 0.60, 5)
        V4.set_explode(f"DU_R_NVH_Cover_{sd}", (s, -0.5, 0.6), 0.75, 5)
    V4.set_explode("DU_R_Gearbox", (0, 0.3, -1), 0.50, 5)

    xc, Ls = 0.290, 0.150
    kw = dict(mirror=True, parent=par, stage=6, group=grp, fid="A", note=NOTE_INT)
    A(V4.part(M, "DU_R_Stator_Core", sysn, ["elec_steel"], [
        stator((xc, ym, zm), X, 0.066, 0.106, Ls, 60, 0.022),
        [beam((xc - Ls / 2, ym + 0.106 * math.cos(a), zm + 0.106 * math.sin(a)),
              (xc + Ls / 2, ym + 0.106 * math.cos(a), zm + 0.106 * math.sin(a)), 0.006, 0.003,
              up=(0, math.cos(a), math.sin(a))) for a in (0.4, 2.0, 3.5, 5.1)],
    ], "Paquete de chapa del estátor del motor de inducción {lado} (60 ranuras)", edir=(1, 0, 0), dist=0.30, **kw))
    A(V4.part(M, "DU_R_Stator_Winding", sysn, ["copper_enamel", "nylon", "copper"], [
        winding((xc, ym, zm), X, 0.070, 0.098, Ls, 0.034, 0, 1, 24),
        [box((xc + Ls / 2 + 0.03, ym + 0.022 * k, zm + 0.099), (0.012, 0.012, 0.022), 0.002, 2) for k in (-1, 0, 1)],
    ], "Devanado distribuido del motor de inducción {lado} (cabezas de bobina atadas y terminales de fase)",
        edir=(1, 0, 0), dist=0.30, **kw))
    A(V4.part(M, "DU_R_Rotor", sysn, ["elec_steel", "copper", "alu_machined"], [
        cyl((xc - Ls / 2, ym, zm), (xc + Ls / 2, ym, zm), 0.0645, seg=48, m=0),
        # jaula de ardilla de cobre: anillos de cortocircuito y extremos de las barras
        ring((xc - Ls / 2 - 0.007, ym, zm), X, 0.030, 0.0635, 0.014, 48, 1),
        ring((xc + Ls / 2 + 0.007, ym, zm), X, 0.030, 0.0635, 0.014, 48, 1),
        [box((xc + sg * (Ls / 2 + 0.0005), ym + 0.058 * math.cos(2 * math.pi * k / 40),
              zm + 0.058 * math.sin(2 * math.pi * k / 40)), (0.002, 0.005, 0.005), 0.0, 1)
         for k in range(40) for sg in (-1, 1)],
        # aros de retención (acero de alta resistencia) sobre los anillos de cobre
        ring((xc - Ls / 2 - 0.007, ym, zm), X, 0.0635, 0.0660, 0.014, 48, 2),
        ring((xc + Ls / 2 + 0.007, ym, zm), X, 0.0635, 0.0660, 0.014, 48, 2),
    ], "Rotor de jaula de ardilla de cobre {lado} (barras, anillos de cortocircuito y aros de retención)",
        edir=(1, 0, 0), dist=0.46, **kw))
    A(V4.part(M, "DU_R_Rotor_Shaft", sysn, ["gear_steel", "bearing_steel"], [
        cyl((0.090, ym, zm), (0.432, ym, zm), 0.0170, seg=24, m=0),
        cyl((xc - Ls / 2 - 0.016, ym, zm), (xc + Ls / 2 + 0.016, ym, zm), 0.0225, seg=24, m=0),
        spline((0.105, ym, zm), X, 0.0170, 0.028, 22, 0.0011, 0.0, 0),
        bearing((0.180, ym, zm), X, 0.0170, 0.033, 0.016, 10, m=1),
        bearing((0.412, ym, zm), X, 0.0170, 0.031, 0.014, 9, m=1),
        ring((0.426, ym, zm), X, 0.032, 0.046, 0.008, 28, 0),
    ], "Eje del rotor {lado} con estriado, rodamientos y resolver", edir=(1, 0, 0.2), dist=0.54, **kw))
    A(V4.part(M, "DU_R_Gear_Train", sysn, ["gear_steel", "bearing_steel", "rubber_seal"], [
        gear((0.118, ym, zm), X, 0.0250, 0.0285, 0.036, 19, 0.0170, 24.0),
        gear((0.118, yi, zi), X, 0.0760, 0.0800, 0.032, 51, 0.020, -24.0),
        gear((0.058, yi, zi), X, 0.0260, 0.0300, 0.046, 17, 0.0, 22.0),
        cyl((0.014, yi, zi), (0.150, yi, zi), 0.018, seg=24, m=0),
        bearing((0.020, yi, zi), X, 0.018, 0.034, 0.014, 10, m=1),
        bearing((0.146, yi, zi), X, 0.018, 0.034, 0.014, 10, m=1),
        gear((0.058, yd, zd), X, 0.0820, 0.0860, 0.042, 61, 0.030, -22.0),
        cyl((0.010, yd, zd), (0.150, yd, zd), 0.0175, seg=22, m=0),
        bearing((0.018, yd, zd), X, 0.0175, 0.036, 0.016, 11, m=1),
        bearing((0.110, yd, zd), X, 0.030, 0.050, 0.018, 12, m=1),
        ring((0.130, yd, zd), X, 0.031, 0.040, 0.008, 28, 2),
        ring((0.165, yd, zd), X, 0.0178, 0.034, 0.008, 28, 2),
    ], "Reductora independiente {lado}: piñón de entrada, eje intermedio, rueda de salida, ejes y rodamientos "
       "(sin diferencial: vectorización de par)", edir=(0.4, 0.3, -1), dist=0.34, **kw))
    A(V4.part(M, "DU_R_Output_Shaft", sysn, ["gear_steel", "rubber_seal"], [
        cyl((0.140, yd, zd), (0.200, yd, zd), 0.0175, seg=22, m=0),
        spline((0.186, yd, zd), X, 0.0175, 0.030, 26, 0.0012, 0.0, 0),
    ], "Eje de salida estriado {lado} (atraviesa la carcasa por su retén hacia el semieje)",
        edir=(0.6, 0, -0.6), dist=0.36, **kw))
    xv, yv, zv = 0.30, ym - 0.14, 0.56
    A(V4.part(M, "DU_R_Inverter_Internals", sysn, ["alu_cast", "ceramic", "plastic_black", "capacitor", "copper",
                                                   "pcb_green", "connector_grey", "solder_tin"], [
        box((xv, yv + 0.024, zv), (0.215, 0.006, 0.150), 0.002, 0),
        [box((xv - 0.06 + 0.06 * k, yv + 0.019, zv - 0.03), (0.050, 0.003, 0.070), 0.0005, 1) for k in range(3)],
        [box((xv - 0.07 + 0.06 * k + 0.012 * (j % 2), yv + 0.017, zv - 0.05 + 0.03 * (j // 2)),
             (0.008, 0.0008, 0.008), 0.0, 2) for k in range(3) for j in range(4)],
        box((xv, yv + 0.004, zv + 0.045), (0.20, 0.024, 0.045), 0.003, 3),
        [box((xv - 0.06 + 0.06 * k, yv + 0.010, zv - 0.072), (0.020, 0.004, 0.020), 0.0005, 4) for k in range(3)],
        pcb((xv, yv - 0.015, zv), (0.20, 0.14, 0.0016), (0, -1, 0), Z, 60, 21, 5, 2, 3, 6, 7),
    ], "Interior del inversor trasero {lado}: placa fría, módulos de potencia, condensador, barras y placa de control",
        edir=(0.1, -1, 0.5), dist=0.30, **kw))
    return out


# ---------------------------------------------------------------------------
# Semiejes: juntas homocinéticas, abrazaderas y tornillo central
# ---------------------------------------------------------------------------
def halfshaft_internals(M):
    out = []
    A = out.extend
    for axle, y, x_in in (("F", S.Y_FRONT_AXLE, {1: 0.230, -1: -0.035}), ("R", S.Y_REAR_AXLE, {1: 0.190, -1: -0.190})):
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{axle}{sd}"
            xi, xo = x_in[s], s * 0.835
            side = "derecho" if s > 0 else "izquierdo"
            where = "delantero" if axle == "F" else "trasero"
            # Junta interior de trípode: araña con tres muñones y rodillos de agujas
            ct = Vector((xi + s * 0.040, y, WZ))
            shp = [cyl(tuple(ct - Vector((s * 0.012, 0, 0))), tuple(ct + Vector((s * 0.012, 0, 0))), 0.016, seg=20)]
            for k in range(3):
                a = 2 * math.pi * k / 3 + 0.5
                d = Vector((0, math.cos(a), math.sin(a)))
                shp.append(cyl(tuple(ct), tuple(ct + d * 0.030), 0.0075, seg=12))
                shp.append(V4.torus(tuple(ct + d * 0.026), tuple(d), 0.0115, 0.0045, 20, 8, 1))
                shp.append(ring(tuple(ct + d * 0.026), tuple(d), 0.0075, 0.0115, 0.008, 16, 2))
            shp.append(spline(tuple(ct + Vector((s * 0.030, 0, 0))), X, 0.0155, 0.040, 24, 0.001, 0.0, 0))
            A(V4.part(M, f"DU_Halfshaft_{tag}_Tripod_Joint", "DRIVE_UNITS", ["gear_steel", "bearing_steel", "nylon"],
                      shp, f"Junta homocinética interior de trípode del semieje {where} {side} (araña, rodillos "
                           "de agujas y estriado)", edir=(0, 0.2 if axle == "F" else -0.2, -1), dist=0.30, stage=6,
                      group="Semiejes", fid="A", note=NOTE_INT))
            # Junta exterior Rzeppa: nuez, jaula y 6 bolas
            co = Vector((xo - s * 0.040, y, WZ))
            shp = [taper(tuple(co - Vector((s * 0.018, 0, 0))), (s, 0, 0),
                         [(0.0, 0.0), (0.020, 0.0), (0.026, 0.018), (0.020, 0.036), (0.0, 0.036)], 24, 0),
                   ring(tuple(co), X, 0.0285, 0.0325, 0.020, 32, 1)]
            for k in range(6):
                a = 2 * math.pi * k / 6
                shp.append(sphere((co.x, co.y + 0.0305 * math.cos(a), co.z + 0.0305 * math.sin(a)), 0.0085, 12, 7, 2))
            A(V4.part(M, f"DU_Halfshaft_{tag}_Rzeppa_Joint", "DRIVE_UNITS", ["gear_steel", "steel_bare", "bearing_steel"],
                      shp, f"Junta homocinética exterior Rzeppa del semieje {where} {side} (nuez, jaula y 6 bolas)",
                      edir=(0, -0.2 if axle == "F" else 0.2, -1), dist=0.30, stage=6, group="Semiejes", fid="A",
                      note=NOTE_INT))
            # Abrazaderas de los fuelles (acompañan al semieje)
            A(V4.part(M, f"DU_Halfshaft_{tag}_Boot_Clamps", "DRIVE_UNITS", ["steel_bare"], [
                hose_clamp((xi + s * 0.080, y, WZ), X, 0.0445, 0.009),
                hose_clamp((xi + s * 0.160, y, WZ), X, 0.0165, 0.007),
                hose_clamp((xo - s * 0.150, y, WZ), X, 0.0165, 0.007),
                hose_clamp((xo - s * 0.080, y, WZ), X, 0.0405, 0.009),
            ], f"Abrazaderas de oreja de los fuelles del semieje {where} {side} (4)", edir=(s, 0, -0.3), dist=0.55,
                stage=5, group="Semiejes", fid="A", note=NOTE_INT))
            # Tornillo central del buje (24 mm, 300 N·m) con arandela
            hx = s * (S.X_WHEEL + S.RIM_OFFSET - 0.004 + 0.016)
            A(V4.part(M, f"DU_Halfshaft_{tag}_Hub_Bolt", "DRIVE_UNITS", ["zinc"], [
                screw((hx, y, WZ), (s, 0, 0), 0.016, 0.060, 0, "hex", 0.0015, True),
            ], f"Tornillo central del buje {where} {side} (24 mm, 300 N·m; de un solo uso)", edir=(s, 0, 0), dist=1.25,
                stage=6, group="Tornillería", fid="R",
                note="Par y llave del manual de servicio; longitud de la caña reconstruida"))
    return out


def hub_bearings(M):
    out = []
    for axle, y in (("F", S.Y_FRONT_AXLE), ("R", S.Y_REAR_AXLE)):
        for s, sd in ((1, "R"), (-1, "L")):
            tag = f"{axle}{sd}"
            where = "delantero" if axle == "F" else "trasero"
            out += V4.part(M, f"SUS_{tag}_Hub_Bearing", "FRONT_SUSPENSION" if axle == "F" else "REAR_SUSPENSION",
                           ["bearing_steel", "nylon", "rubber_seal"], [
                               bearing((s * 0.848, y, WZ), X, 0.0265, 0.0495, 0.046, 15, rows=2),
                               ring((s * 0.8255, y, WZ), X, 0.034, 0.0420, 0.002, 32, 2),
                               ring((s * 0.8705, y, WZ), X, 0.034, 0.0420, 0.002, 32, 2),
                           ], f"Rodamiento de buje {where} de doble hilera de bolas con retenes",
                           parent=f"SUSP_{tag}", edir=(s, 0, 0.1), dist=0.14, stage=6, group="Suspensión",
                           fid="A", note=NOTE_INT)
    return out


def build(M):
    out = []
    out += front_unit(M)
    out += rear_unit(M)
    out += halfshaft_internals(M)
    out += hub_bearings(M)
    return out
