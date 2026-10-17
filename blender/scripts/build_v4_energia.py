"""Versión 4 · energía y climatización: batería, alta tensión, 48 V, electrónica y gestión térmica por dentro.

  Batería: placas de supervisión de celdas (BMB) por bloque con sus circuitos flexibles de medida, barras
    principales del pack hasta la cabecera, controlador BMS, junta perimetral de la tapa y colectores de
    refrigerante de los serpentines.
  Bahía auxiliar: interior del PCS (cargador embarcado y convertidor CC-CC: transformadores, condensadores,
    placa y placa fría) y de la caja de conexiones de alterna (barras y placa).
  48 V: celdas cilíndricas, placa BMS y tiras de conexión de la batería de baja tensión; placas de los tres
    controladores de carrocería, del ordenador de a bordo y de la ECU de remolque.
  Térmica: ventiladores del módulo de refrigeración (hélices, cubos y motores), compresor de A/C de espiral
    (motor, espirales fija y orbitante, placa del inversor), rodete y motor de la bomba de refrigerante,
    interior del climatizador (soplante centrífuga con motor, evaporador, condensador interior de la bomba
    de calor, compuertas de mezcla y de modo, desagüe).
  Limpiaparabrisas: motor con tornillo sinfín y rueda dentada.

Fidelidad: la existencia de estos componentes consta en el manual de servicio (PCS, ACJB, controladores,
compresor, bomba, climatizador, 48 V) o es imprescindible para el funcionamiento; su interior no se publica y
se reconstruye («Aproximado»). El número de celdas de la batería de 48 V no consta en las fuentes.
"""

import math
from mathutils import Vector, Matrix
import ct_specs as S
import ct_v4 as V4
from ct_v4 import (gear, ring_gear, spline, sphere, bearing, taper, tube, screw, pcb, stator, winding, coil,
                   fins, box, cyl, ring, disc, hull, beam, bolt, nut, torx, sweep)
import build_v4_chasis as CH

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NOTE = ("Componente necesario para el funcionamiento; su interior no se publica y se ha reconstruido "
        "(forma, dimensiones y número de elementos aproximados)")
PCB_MATS = ["pcb_green", "plastic_black", "capacitor", "connector_grey", "solder_tin"]
BLOCK_X = (-0.555, -0.185, 0.185, 0.555)


# ---------------------------------------------------------------------------
# Batería de alta tensión
# ---------------------------------------------------------------------------
def battery(M):
    out = []
    A = out.extend
    for i, bx in enumerate(BLOCK_X, start=1):
        A(V4.part(M, f"BAT_Block_{i}_BMB", "BATTERY_ASSEMBLY", PCB_MATS + ["copper", "nylon"], [
            pcb((bx, 1.105, 0.400), (0.30, 0.075, 0.0016), Y, Z, 45, 50 + i),
            # circuito flexible de medida de tensión y temperatura a lo largo del bloque
            box((bx, -0.085, 0.4033), (0.030, 2.24, 0.0005), 0.0, 6),
            [box((bx + sg * 0.165, -0.085, 0.4031), (0.010, 2.24, 0.0004), 0.0, 6) for sg in (-1, 1)],
            [box((bx + sg * 0.165, -1.20 + 0.0466 * 6 * k, 0.4035), (0.012, 0.010, 0.0008), 0.0, 5)
             for sg in (-1, 1) for k in range(8)],
            box((bx, 1.08, 0.415), (0.040, 0.030, 0.012), 0.002, 3),
        ], f"Placa de supervisión de celdas (BMB) del bloque {i} con circuito flexible de medida de tensión y "
           "temperatura", parent="BATTERY_PACK", edir=(0, 0.4, 1), dist=0.80, stage=6, group="Batería", fid="A",
            note=NOTE))
    A(V4.part(M, "BAT_Main_Busbars", "BATTERY_ASSEMBLY", ["busbar_alu", "nylon", "zinc"], [
        beam((-0.70, 1.10, 0.430), (-0.12, 1.16, 0.470), 0.040, 0.004, up=(0, 0, 1)),
        beam((0.70, 1.10, 0.430), (0.12, 1.16, 0.470), 0.040, 0.004, up=(0, 0, 1)),
        [beam((bx - 0.12, 1.06, 0.428), (bx + 0.12, 1.06, 0.428), 0.030, 0.004, up=(0, 0, 1)) for bx in BLOCK_X[1:3]],
        [box((x, 1.10, 0.425), (0.050, 0.030, 0.006), 0.001, 1) for x in (-0.6, -0.3, 0.3, 0.6)],
        [bolt((x, 1.10, 0.434), Z, 0.008, 2) for x in (-0.66, -0.40, 0.40, 0.66)],
    ], "Barras colectoras principales del pack (serie entre bloques y polos + / − hasta la cabecera de alta tensión)",
        parent="BATTERY_PACK", edir=(0, 0.3, 1), dist=0.95, stage=6, group="Batería", fid="A", note=NOTE))
    A(V4.part(M, "BAT_BMS_Controller", "BATTERY_ASSEMBLY", PCB_MATS + ["alu_cast"], [
        pcb((0.0, 1.205, 0.492), (0.20, 0.085, 0.0016), Z, X, 45, 61),
        box((0.0, 1.205, 0.486), (0.21, 0.095, 0.004), 0.001, 5),
    ], "Controlador del sistema de gestión de la batería (BMS) dentro de la cabecera de alta tensión",
        parent="BATTERY_PACK", edir=(0, 0.3, 1), dist=0.70, stage=6, group="Batería", fid="A", note=NOTE))
    # junta perimetral de la tapa (cordón de elastómero sobre la brida)
    path = [(-0.815, -1.385, 0.457), (0.815, -1.385, 0.457), (0.815, 1.235, 0.457), (-0.815, 1.235, 0.457)]
    pts = []
    for a, b in zip(path, path[1:] + path[:1]):
        for k in range(6):
            t = k / 6
            pts.append(tuple(Vector(a) + (Vector(b) - Vector(a)) * t))
    A(V4.part(M, "BAT_Lid_Seal", "BATTERY_ASSEMBLY", ["rubber_seal"], [tube(pts + [pts[0]], 0.0035, 8, 1, 0)],
              "Junta perimetral de estanqueidad entre la bandeja y la tapa (sellado para vadeo)",
              parent="BATTERY_PACK", edir=(0, 0, 1), dist=1.05, stage=6, group="Batería", fid="A", note=NOTE))
    A(V4.part(M, "BAT_Coolant_Manifolds", "BATTERY_ASSEMBLY", ["alu_machined", "rubber_seal", "steel_bare"], [
        tube([(-0.73, 1.085, 0.338), (0.0, 1.085, 0.338), (0.73, 1.085, 0.338)], 0.009, 14, 1, 0),
        tube([(-0.73, 1.118, 0.360), (0.0, 1.118, 0.360), (0.73, 1.118, 0.360)], 0.009, 14, 1, 0),
        [cyl((bx + dx, 1.075, 0.338), (bx + dx, 1.075, 0.326), 0.006, seg=10, m=0) for bx in BLOCK_X
         for dx in (-0.12, 0.12)],
        [cyl((x, 1.118, 0.360), (x, 1.27, 0.360), 0.010, seg=14, m=0) for x in (-0.32, 0.32)],
        [ring((x, 1.255, 0.360), Y, 0.010, 0.016, 0.010, 16, 1) for x in (-0.32, 0.32)],
        [V4.hose_clamp((x, 1.262, 0.360), Y, 0.0165, 0.006, 2) for x in (-0.32, 0.32)],
    ], "Colectores de refrigerante de los serpentines (entrada y salida, conexiones al frontal de la bandeja)",
        parent="BATTERY_PACK", edir=(0, 1, 0.3), dist=0.60, stage=6, group="Batería", fid="A", note=NOTE))
    return out


# ---------------------------------------------------------------------------
# Bahía auxiliar y electrónica de 48 V
# ---------------------------------------------------------------------------
def electronics(M):
    out = []
    A = out.extend
    # PCS: cargador embarcado + convertidor CC-CC
    cx, cy, cz = 0.32, -1.20, 0.643
    A(V4.part(M, "HV_PCS_Internals", "BATTERY_ASSEMBLY", ["alu_cast", "elec_steel", "copper_enamel", "capacitor",
                                                          "pcb_green", "plastic_black", "connector_grey", "solder_tin"], [
        box((cx, cy, 0.598), (0.38, 0.32, 0.006), 0.002, 0),
        [box((cx - 0.10 + 0.10 * k, cy + 0.08, 0.622), (0.050, 0.040, 0.040), 0.002, 1) for k in range(3)],
        [ring((cx - 0.10 + 0.10 * k, cy + 0.08, 0.622), Z, 0.012, 0.024, 0.018, 20, 2) for k in range(3)],
        [cyl((cx - 0.15 + 0.035 * k, cy - 0.10, 0.601), (cx - 0.15 + 0.035 * k, cy - 0.10, 0.650), 0.014, seg=18, m=3)
         for k in range(6)],
        pcb((cx + 0.02, cy - 0.02, 0.660), (0.34, 0.28, 0.0016), Z, X, 80, 71, 4, 5, 3, 6, 7),
    ], "Interior del PCS: cargador embarcado y convertidor CC-CC (transformadores planos, bobinas, condensadores, "
       "placa de potencia y placa fría)", parent="ANCILLARY_BAY", edir=(0.3, -0.3, 1), dist=0.55, stage=6,
        group="Alta tensión", fid="A", note=NOTE))
    A(V4.part(M, "HV_ACJB_Internals", "BATTERY_ASSEMBLY", ["busbar_alu", "copper", "nylon"] + PCB_MATS, [
        [beam((-0.55, -1.22 + 0.04 * k, 0.615), (-0.18, -1.22 + 0.04 * k, 0.615), 0.022, 0.004, up=(0, 0, 1),
              m=k % 2) for k in range(4)],
        [box((-0.36 + 0.09 * k, -1.20, 0.607), (0.03, 0.17, 0.008), 0.001, 2) for k in range(3)],
        pcb((-0.36, -1.32, 0.640), (0.30, 0.05, 0.0016), Z, X, 25, 72, 3, 4, 5, 6, 7),
    ], "Interior de la caja de conexiones de alterna (ACJB): barras, soportes aislantes y placa de medida",
        parent="ANCILLARY_BAY", edir=(-0.3, -0.3, 1), dist=0.55, stage=6, group="Alta tensión", fid="A", note=NOTE))
    # batería de 48 V
    cells = []
    for k in range(13):
        x = 0.445 + 0.0225 * (k % 7) + (0.011 if k >= 7 else 0.0)
        y = 1.70 if k < 7 else 1.74
        cells.append(cyl((x, y, 0.735), (x, y, 0.805), 0.0105, seg=16, m=0))
        cells.append(disc((x, y, 0.806), Z, 0.0045, 0.002, 12, 1))
    # la caja se trasladó contra el cortafuegos (build_mechanics): el interior la acompaña
    off48 = Matrix.Translation((0.34 - 0.52, 1.60 - 1.74, 0.86 - 0.80))
    A(V4.part(M, "LV_Battery_48V_Internals", "BATTERY_ASSEMBLY", ["cell", "steel_bare", "nylon"] + PCB_MATS, [V4.xf(off48, cells + [
        [box((0.52, y, 0.809), (0.17, 0.008, 0.0008), 0.0, 1) for y in (1.70, 1.74)],
        box((0.52, 1.72, 0.733), (0.17, 0.07, 0.004), 0.001, 2),
        pcb((0.52, 1.78, 0.80), (0.17, 0.06, 0.0016), (0, 1, 0), Z, 30, 73, 3, 4, 5, 6, 7),
    ])], "Interior de la batería de 48 V: celdas cilíndricas en serie, tiras de conexión, soporte y placa BMS",
        edir=(0.4, 0.3, 1), dist=0.45, stage=6, group="Baja tensión", fid="A",
        note=NOTE + ". El número de celdas (13 en serie) es una estimación a partir de la tensión nominal"))
    for nm, c, nrm, sd in (("LV_Body_Controller_LH", (-0.585, 1.296, 0.80), (0, 1, 0), 81),
                           ("LV_Body_Controller_RH", (0.585, 1.351, 0.80), (0, 1, 0), 82),
                           ("LV_Body_Controller_Rear", (0.0, -0.994, 0.755), (0, -1, 0), 83)):
        A(V4.part(M, nm + "_PCB", "BATTERY_ASSEMBLY", PCB_MATS, [
            pcb(c, (0.20, 0.13, 0.0016), nrm, Z, 70, sd),
        ], f"Placa del controlador de carrocería ({nm.split('_')[-1]}): eFuses, microcontrolador y Ethernet",
            edir=(0, nrm[1] * 0.5, 1), dist=0.85, stage=6, group="Baja tensión", fid="A", note=NOTE))
    A(V4.part(M, "INT_Car_Computer_Internals", "INTERIOR_DASHBOARD", PCB_MATS + ["alu_machined", "copper"], [
        pcb((0.42, 1.20, 1.012), (0.27, 0.17, 0.0016), Z, X, 90, 91),
        [box((0.36 + 0.12 * k, 1.20, 1.020), (0.045, 0.045, 0.006), 0.001, 5) for k in range(2)],
        box((0.42, 1.20, 1.032), (0.27, 0.17, 0.006), 0.002, 5),
    ], "Interior del ordenador de a bordo: placa base con los dos procesadores, disipadores y placa fría líquida",
        parent="IP_ASSEMBLY", edir=(0.3, 0, 1), dist=0.45, stage=6, group="Electrónica", fid="A", note=NOTE))
    A(V4.part(M, "LV_Trailer_ECU_PCB", "BATTERY_ASSEMBLY", PCB_MATS, [
        pcb((0.34, -2.861, 0.648), (0.09, 0.07, 0.0016), Z, X, 18, 92),
    ], "Placa de la ECU de remolque (salidas de luces y freno eléctrico)", edir=(0, -1, 0.4), dist=0.65, stage=6,
        group="Baja tensión", fid="A", note=NOTE))
    return out


# ---------------------------------------------------------------------------
# Gestión térmica
# ---------------------------------------------------------------------------
def _fan(c, axis, r, blades, hub_r, m_blade=0, m_hub=1, pitch_deg=32):
    """Hélice axial: cubo y palas inclinadas (cada pala, envolvente de su perfil torcido)."""
    c = Vector(c)
    w = Vector(axis).normalized()
    u, v, _ = L_frame(w)
    shp = [cyl(tuple(c - w * 0.022), tuple(c + w * 0.022), hub_r, seg=24, m=m_hub)]
    for k in range(blades):
        a0 = 2 * math.pi * k / blades
        pts = []
        for rr, sweep_a, chord in ((hub_r * 0.95, 0.0, 0.040), (r * 0.6, 0.12, 0.060), (r, 0.30, 0.070)):
            a = a0 + sweep_a
            d = u * math.cos(a) + v * math.sin(a)
            tdir = -u * math.sin(a) + v * math.cos(a)
            pt = math.radians(pitch_deg)
            for s_ in (-0.5, 0.5):
                base = c + d * rr + (tdir * math.cos(pt) + w * math.sin(pt)) * chord * s_
                pts.append(tuple(base + w * 0.0012))
                pts.append(tuple(base - w * 0.0012))
        shp.append(hull(pts, m_blade))
    return shp


def L_frame(w):
    import ct_lib as L
    return L.frame_from_axis(w)


def thermal(M):
    out = []
    A = out.extend
    A(V4.part(M, "CHS_Cooling_Fans", "UNDERBODY", ["plastic_black", "plastic_black", "elec_steel", "copper_enamel"], [
        _fan((sx * 0.225, 2.332, 0.565), Y, 0.130, 7, 0.045) for sx in (-1, 1)
    ] + [CH._small_motor((sx * 0.225, 2.315, 0.565), Y, 0.040, 0.035, 2, 3, 2, 9) for sx in (-1, 1)],
        "Hélices de 7 palas, cubos y motores sin escobillas de los dos ventiladores del módulo de refrigeración",
        parent="THERMAL_FRONT", edir=(0, -1, 0.3), dist=0.30, stage=6, group="Refrigeración", fid="A", note=NOTE))
    # Compresor de A/C eléctrico de espiral (eje X)
    c = Vector((-0.225, 1.82, 0.795))
    scrolls = []
    for k, ph in ((0, 0.0), (1, math.pi)):
        xs = -0.165 - 0.018 * k
        path = []
        for i in range(60):
            th = 0.6 + i * 0.22
            rr = 0.0042 * th
            if rr > 0.050:
                break
            a = th + ph
            path.append((xs, c.y + rr * math.cos(a) + (0.004 if k else 0.0), c.z + rr * math.sin(a)))
        scrolls.append(sweep(path, 0.003, 0.016, 0.0, 1, up=(1, 0, 0), m=0))
        scrolls.append(disc((xs - 0.010 + 0.020 * k, c.y, c.z), X, 0.054, 0.006, 40, 0))
    A(V4.part(M, "THM_AC_Compressor_Internals", "UNDERBODY", ["alu_machined", "elec_steel", "copper_enamel",
                                                             "gear_steel"] + PCB_MATS, scrolls + [
        CH._small_motor((-0.27, c.y, c.z), X, 0.062, 0.10, 1, 2, 3, 12),
        cyl((-0.33, c.y, c.z), (-0.15, c.y, c.z), 0.008, seg=12, m=3),
        pcb((-0.245, c.y, 0.875), (0.18, 0.10, 0.0016), Z, X, 40, 93, 4, 5, 6, 7, 8),
    ], "Interior del compresor eléctrico de A/C: espirales fija y orbitante, motor y placa del inversor",
        parent="THERMAL_FRONT", edir=(-0.6, 0, 1), dist=0.40, stage=6, group="Refrigeración", fid="A", note=NOTE))
    A(V4.part(M, "THM_Coolant_Pump_Internals", "UNDERBODY", ["plastic_black", "elec_steel", "copper_enamel",
                                                            "gear_steel"], [
        disc((0.45, 1.79, 0.78), Y, 0.026, 0.004, 24, 0),
        [hull([(0.45 + rr * math.cos(a + d), 1.792 + h, 0.78 + rr * math.sin(a + d))
               for rr, d in ((0.008, 0.0), (0.024, 0.5)) for h in (0.0, 0.010)], 0)
         for a in [2 * math.pi * k / 7 for k in range(7)]],
        CH._small_motor((0.45, 1.735, 0.78), Y, 0.032, 0.055, 1, 2, 3, 9),
    ], "Rodete de 7 álabes y motor de rotor húmedo de la bomba de refrigerante",
        edir=(0.6, -0.4, 0.4), dist=0.70, stage=6, group="Refrigeración", fid="A", note=NOTE))
    # Climatizador (HVAC): todo dentro de la caja de build_interior_detail (x -0,22…0,34, y 1,13…1,37,
    # z 0,645…0,915) y de la voluta del soplante (cilindro r 0,085 en x 0,42, y 1,24, z 0,76…0,90)
    blow = Vector((0.42, 1.24, 0.835))
    blades = []
    for k in range(36):
        a = 2 * math.pi * k / 36
        d = Vector((math.cos(a), math.sin(a), 0))
        t = Vector((-math.sin(a), math.cos(a), 0))
        p0 = blow + d * 0.056
        p1 = blow + d * 0.069 + t * 0.007
        blades.append(beam(tuple(p0), tuple(p1), 0.0012, 0.050, up=(0, 0, 1), r=0.0, m=0))
    A(V4.part(M, "INT_HVAC_Internals", "INTERIOR_DASHBOARD", ["plastic_black", "radiator", "alu_machined",
                                                              "elec_steel", "copper_enamel", "gear_steel", "rubber_seal",
                                                              "felt"], blades + [
        disc(tuple(blow + Vector((0, 0, -0.026))), Z, 0.071, 0.003, 36, 0),
        ring(tuple(blow + Vector((0, 0, 0.026))), Z, 0.054, 0.071, 0.003, 36, 0),
        CH._small_motor((0.42, 1.24, 0.785), Z, 0.036, 0.034, 3, 4, 5, 10),
        # evaporador: núcleo de placas y aletas con colectores
        box((0.06, 1.320, 0.78), (0.46, 0.034, 0.21), 0.002, 1),
        [box((0.06, 1.320, 0.672 + 0.216 * k), (0.47, 0.038, 0.006), 0.001, 2) for k in range(2)],
        [cyl((-0.17, 1.320 + dy, 0.70), (-0.205, 1.320 + dy, 0.70), 0.007, seg=12, m=2) for dy in (-0.009, 0.009)],
        # condensador interior (bomba de calor)
        box((0.04, 1.225, 0.78), (0.38, 0.028, 0.19), 0.002, 1),
        [box((0.04, 1.225, 0.682 + 0.196 * k), (0.39, 0.032, 0.006), 0.001, 2) for k in range(2)],
        # compuertas de mezcla y de modo (aletas con eje)
        [box((0.06, 1.165, 0.81 + 0.05 * k), (0.40, 0.004, 0.040), 0.001, 0) for k in range(2)],
        [cyl((-0.16, 1.165, 0.83 + 0.05 * k), (0.28, 1.165, 0.83 + 0.05 * k), 0.004, seg=8, m=5) for k in range(2)],
        box((0.06, 1.165, 0.71), (0.40, 0.004, 0.05), 0.001, 0),
        # desagüe del evaporador a través del mamparo y aislante del fondo de la caja
        cyl((0.06, 1.30, 0.660), (0.06, 1.34, 0.610), 0.008, seg=10, m=6),
        box((0.06, 1.25, 0.665), (0.48, 0.20, 0.004), 0.0, 7),
    ], "Interior del climatizador: soplante centrífuga de 36 álabes con motor, evaporador, condensador interior de "
       "la bomba de calor, compuertas de mezcla y de modo, desagüe y aislante",
        parent="IP_ASSEMBLY", edir=(0.3, 0, 1), dist=0.70, stage=6, group="Climatización", fid="A", note=NOTE))
    # Motor del limpiaparabrisas: sinfín y corona
    A(V4.part(M, "EXT_Wiper_Motor_Internals", "GLASS_AND_MIRRORS", ["gear_steel", "nylon", "elec_steel",
                                                                   "copper_enamel"], [
        gear((0.12, 1.945, 1.25), Y, 0.030, 0.034, 0.012, 40, 0.006, 0.0, 1),
        gear((0.07, 1.945, 1.218), X, 0.006, 0.0075, 0.040, 6, 0.0, 60.0, 0, 8),
        CH._small_motor((0.01, 1.945, 1.218), X, 0.024, 0.06, 2, 3, 0, 8),
    ], "Interior del motor del limpiaparabrisas: tornillo sinfín, corona de nailon y motor",
        edir=(0.3, 0.3, 1), dist=0.65, stage=6, group="Limpiaparabrisas", fid="A", note=NOTE))
    return out


# Módulos electrónicos cerrados que reciben su placa interior (nombre del módulo → descripción)
BOARDS = {
    "CAM_BPillar_L": "cámara del pilar B izquierdo (sensor de imagen)",
    "CAM_BPillar_R": "cámara del pilar B derecho (sensor de imagen)",
    "CAM_FenderFlare_L": "cámara de la aleta izquierda (sensor de imagen)",
    "CAM_FenderFlare_R": "cámara de la aleta derecha (sensor de imagen)",
    "CAM_Front_Fascia": "cámara de la fascia delantera (sensor de imagen)",
    "CAM_Windshield_Module": "módulo de cámaras del parabrisas (sensores de imagen y calefactor)",
    "ELE_FM_HD_Tuner": "sintonizador FM/HD",
    "EXT_ChargePort_ECU": "controlador de la toma de carga",
    "EXT_Door_FL_Controller": "controlador de la puerta delantera izquierda",
    "EXT_Door_FR_Controller": "controlador de la puerta delantera derecha",
    "EXT_Door_RL_Controller": "controlador de la puerta trasera izquierda",
    "EXT_Door_RR_Controller": "controlador de la puerta trasera derecha",
    "EXT_Wiper_Motor_Controller": "controlador del limpiaparabrisas",
    "INT_Cabin_Radar": "radar de habitáculo (antena impresa y transceptor)",
    "INT_Console_USB_Controller_Hub": "concentrador USB de la consola",
    "INT_Restraint_Control_Module": "módulo de control de airbags (acelerómetros y condensador de reserva)",
    "INT_TCU_Bracket": "unidad telemática (módem LTE, GNSS, Wi-Fi y Bluetooth)",
    "LV_MV_Maintainer": "mantenedor de 48 V",
    "STR_F_Actuator_Controller": "controlador del actuador de dirección delantero",
    "STR_R_Actuator_Controller": "controlador del actuador de dirección trasero",
    "STR_Steering_Column_Control_Module": "módulo de control de la columna (mandos del volante)",
    "STR_Steering_Feedback_Actuator": "actuador de realimentación del volante (sensor de ángulo y par)",
    "THM_Supermanifold_Controller_Sensors": "controlador del Supermanifold",
    "INT_Impact_Sensor_BPillar_L": "sensor de impacto del pilar B izquierdo",
    "INT_Impact_Sensor_BPillar_R": "sensor de impacto del pilar B derecho",
    "INT_Impact_Sensor_Fender_L": "sensor de impacto de la aleta izquierda",
    "INT_Impact_Sensor_Fender_R": "sensor de impacto de la aleta derecha",
    "INT_Impact_Sensor_FrontEnd_L": "sensor de impacto frontal izquierdo",
    "INT_Impact_Sensor_FrontEnd_R": "sensor de impacto frontal derecho",
}


def _main_island(o):
    """Vértices (coordenadas locales) de la parte suelta de mayor volumen de caja de la malla de `o`."""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(o.data)
    best, best_v = None, -1.0
    seen = set()
    for v0 in bm.verts:
        if v0.index in seen:
            continue
        stack, isl = [v0], []
        seen.add(v0.index)
        while stack:
            v = stack.pop()
            isl.append(v.co.copy())
            for e in v.link_edges:
                w = e.other_vert(v)
                if w.index not in seen:
                    seen.add(w.index)
                    stack.append(w)
        mn = Vector((min(p.x for p in isl), min(p.y for p in isl), min(p.z for p in isl)))
        mx = Vector((max(p.x for p in isl), max(p.y for p in isl), max(p.z for p in isl)))
        d = mx - mn
        vol = d.x * d.y * d.z
        if vol > best_v:
            best, best_v = isl, vol
    bm.free()
    return best or [v.co for v in o.data.vertices]


def embedded_boards(M):
    """Placa electrónica dentro de cada módulo cerrado, en las coordenadas locales del módulo."""
    import bpy
    out = []
    for k, (nm, desc) in enumerate(sorted(BOARDS.items())):
        o = bpy.data.objects.get(nm)
        if o is None or o.type != "MESH" or not o.data.vertices:
            continue
        # la placa va en la mayor de las partes sueltas del módulo (su carcasa): en los módulos de varias piezas
        # (caja, válvulas, botella…) la caja del objeto entero dejaría la placa flotando entre ellas
        vs = _main_island(o)
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        size = mx - mn
        c = (mn + mx) / 2
        thin = min(range(3), key=lambda i: size[i])
        nrm = [0, 0, 0]
        nrm[thin] = 1
        upv = (0, 0, 1) if thin != 2 else (0, 1, 0)
        # ancho según el eje «u» que usa `pcb` (up × normal) y alto según «up»
        u_axis = Vector(upv).cross(Vector(nrm))
        uw = abs(u_axis.x) * size.x + abs(u_axis.y) * size.y + abs(u_axis.z) * size.z
        vh = abs(upv[0]) * size.x + abs(upv[1]) * size.y + abs(upv[2]) * size.z
        p = Vector(c)
        ncomp = max(4, min(60, int(uw * vh / 0.0004)))
        out += V4.part(M, f"{nm}_PCB", o.get("system", "BODY_FASTENERS"), PCB_MATS, [
            pcb(tuple(p), (uw * 0.66, vh * 0.62, 0.0012 if min(uw, vh) < 0.05 else 0.0016), tuple(nrm), upv, ncomp,
                200 + k),
        ], f"Placa electrónica del {desc}", frame=o.matrix_world.copy(),
            parent=o.parent.name if o.parent is not None and o.parent.name != "CYBERTRUCK_ROOT" else None,
            edir=tuple(o.get("explode_dir", (0, 0, 1))), dist=float(o.get("explode_dist", 0.3)) * 0.6, stage=6,
            group="Electrónica", fid="A", note=NOTE)
    return out


def build(M):
    out = []
    out += battery(M)
    out += electronics(M)
    out += thermal(M)
    out += embedded_boards(M)
    return out
