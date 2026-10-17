"""Versión 4 · habitáculo por dentro: asientos, volante, cinturones, pantallas, audio, carga inalámbrica y mazos.

  Asientos delanteros: armazón (largueros del cojín, travesaños, muelles en zigzag, herrajes de reclinado con
    barra de sincronización, armazón del respaldo con malla lumbar), espumas de poliuretano separadas de los
    tapizados y esteras de calefacción/ventilación.
  Banco trasero: armazón tubular de cojines y respaldos, espumas y cierres de los respaldos.
  Volante: alma de magnesio dentro del aro y de los radios, adaptador del buje con tornillo central y muelle
    de reloj (clock spring) para los mandos y el airbag.
  Cinturones: carrete con cinta enrollada, rueda de bloqueo y pretensor pirotécnico de cada enrollador.
  Pantallas: panel LCD con retroiluminación y placa base dentro de las carcasas de las pantallas central y
    trasera.
  Audio: altavoces de puerta (cesta, cono, bobina y imán) detrás de las rejillas.
  Consola: bobinas, ferritas y placas de los cargadores inalámbricos.
  Salpicadero: mazo principal a lo largo de la viga transversal con ramales y conectores.

Fidelidad: piezas imprescindibles para el uso del vehículo; formas y dimensiones reconstruidas («Aproximado»).
"""

import math
from mathutils import Vector, Matrix
import bpy
import ct_specs as S
import ct_v4 as V4
from ct_v4 import (gear, sphere, bearing, taper, tube, screw, pcb, coil, box, cyl, ring, disc, hull, beam, bolt,
                   nut, torx, clip, sweep, hose_clamp)

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NOTE = ("Pieza necesaria para el uso del vehículo; forma, dimensiones y posición reconstruidas (no hay planos "
        "publicados)")
PCB_MATS = ["pcb_green", "plastic_black", "capacitor", "connector_grey", "solder_tin"]


def _zigzag(a, b, amp, n, z_sag=0.0, axis_amp=(1, 0, 0)):
    """Muelle en zigzag (sinuoso) entre a y b."""
    a, b = Vector(a), Vector(b)
    w = Vector(axis_amp)
    pts = []
    for i in range(n * 2 + 1):
        t = i / (n * 2)
        p = a + (b - a) * t
        p += w * (amp if i % 2 else -amp) * (0 if i in (0, n * 2) else 1)
        p.z -= z_sag * math.sin(math.pi * t)
        pts.append(tuple(p))
    return pts


# ---------------------------------------------------------------------------
# Asientos
# ---------------------------------------------------------------------------
def front_seats(M):
    out = []
    A = out.extend
    for sd in ("R", "L"):
        V4.set_explode(f"INT_SeatF_{sd}_Cushion", None, 0.34, 6)
        V4.set_explode(f"INT_SeatF_{sd}_Back", None, 0.36, 6)
    x0, x1 = 0.17, 0.62
    shp = [
        # largueros del cojín (chapa embutida) y travesaños tubulares
        [beam((x, 0.30, 0.662), (x, 0.745, 0.672), 0.008, 0.050, up=(0, 0, 1), r=0.002) for x in (x0, x1)],
        tube([(x0, 0.735, 0.672), (x1, 0.735, 0.672)], 0.0115, 14, 1, 0),
        tube([(x0, 0.305, 0.660), (x1, 0.305, 0.660)], 0.0115, 14, 1, 0),
        # muelles sinuosos del cojín
        [tube(_zigzag((x, 0.31, 0.672), (x, 0.725, 0.682), 0.016, 8, 0.012), 0.0021, 6, 1, 1)
         for x in (0.25, 0.34, 0.44, 0.53)],
        # herrajes de reclinado y barra de sincronización
        [disc((x, 0.272, 0.765), X, 0.036, 0.014, 32, 0) for x in (x0 - 0.012, x1 + 0.012)],
        [gear((x, 0.272, 0.765), X, 0.026, 0.029, 0.016, 30, 0.0, 0.0, 0) for x in (x0 - 0.012, x1 + 0.012)],
        tube([(x0 - 0.02, 0.272, 0.765), (x1 + 0.02, 0.272, 0.765)], 0.007, 10, 1, 0),
        # armazón del respaldo
        [tube([(x, 0.255, 0.775), (x, 0.10, 1.10), (x + (0.015 if x < 0.4 else -0.015), -0.08, 1.46)], 0.012, 14, 4, 0)
         for x in (x0, x1)],
        tube([(x0 + 0.015, -0.08, 1.46), (0.395, -0.095, 1.49), (x1 - 0.015, -0.08, 1.46)], 0.012, 14, 4, 0),
        beam((x0, 0.22, 0.83), (x1, 0.22, 0.83), 0.060, 0.004, up=(0, 0.9, 0.45), r=0.0),
        # malla lumbar de alambre
        [tube([(x0, 0.16 - 0.06 * k, 0.95 + 0.11 * k), (0.395, 0.17 - 0.06 * k, 0.95 + 0.11 * k),
               (x1, 0.16 - 0.06 * k, 0.95 + 0.11 * k)], 0.0022, 6, 3, 1) for k in range(4)],
        [tube([(x, 0.16, 0.95), (x, -0.02, 1.28)], 0.0022, 6, 1, 1) for x in (0.30, 0.49)],
        # tornillos del armazón a las guías (4 por asiento, sobre la tapa de la batería)
        [screw((x, y, 0.600), Z, 0.010, 0.030, 2, "flange") for x in (x0 + 0.01, x1 - 0.01) for y in (0.20, 0.74)],
    ]
    A(V4.part(M, "INT_SeatF_Frame", "INTERIOR_SEATS", ["seat_frame", "spring_steel", "zinc"], shp,
              "Armazón del asiento delantero {lado}: largueros, travesaños, muelles en zigzag, herrajes de reclinado, "
              "armazón del respaldo con malla lumbar y 4 tornillos a las guías", mirror=True,
              parent="SEAT_FRONT_R", edir=(0.2, 0, -1), dist=0.10, stage=6, group="Asientos", fid="A", note=NOTE))
    for sd in ("R", "L"):
        A(V4.derived(M, f"INT_SeatF_{sd}_Cushion", f"INT_SeatF_{sd}_Cushion_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma de poliuretano moldeada del cojín delantero {'derecho' if sd == 'R' else 'izquierdo'}",
                     scale=(0.93, 0.93, 0.84), offset=(0, 0, -0.008), parent=f"SEAT_FRONT_{sd}",
                     edir=(0, 0.287, 0.958), dist=0.17, stage=6, group="Asientos", fid="A", note=NOTE))
        A(V4.derived(M, f"INT_SeatF_{sd}_Back", f"INT_SeatF_{sd}_Back_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma de poliuretano moldeada del respaldo delantero {'derecho' if sd == 'R' else 'izquierdo'}",
                     scale=(0.93, 0.86, 0.95), parent=f"SEAT_FRONT_{sd}",
                     edir=(0, -0.958, 0.287), dist=0.18, stage=6, group="Asientos", fid="A", note=NOTE))
    A(V4.part(M, "INT_SeatF_Heat_Vent_Mats", "INTERIOR_SEATS", ["felt", "copper", "connector_grey"], [
        box((0.395, 0.52, 0.872), (0.40, 0.38, 0.0015), 0.0, 0),
        [box((0.395, 0.36 + 0.03 * k, 0.8732), (0.36, 0.0015, 0.0006), 0.0, 1) for k in range(11)],
        beam((0.395, 0.24, 0.86), (0.395, -0.03, 1.40), 0.36, 0.0015, up=(0, 0.958, 0.287), r=0.0, m=0),
        box((0.60, 0.30, 0.70), (0.03, 0.02, 0.012), 0.002, 2),
    ], "Esteras de calefacción (hilo resistivo) y de ventilación del asiento delantero {lado}", mirror=True,
        parent="SEAT_FRONT_R", edir=(0, 0.3, 1), dist=0.26, stage=6, group="Asientos", fid="A", note=NOTE))
    return out


def rear_bench(M):
    out = []
    A = out.extend
    for p in ("L", "C", "R"):
        V4.set_explode(f"INT_SeatR_{p}_Cushion", None, 0.34, 6)
        V4.set_explode(f"INT_SeatR_{p}_Back", None, 0.36, 6)
    shp = [
        tube([(-0.67, -0.30, 0.655), (0.67, -0.30, 0.655)], 0.013, 14, 1, 0),
        tube([(-0.67, -0.72, 0.650), (0.67, -0.72, 0.650)], 0.013, 14, 1, 0),
        [beam((x, -0.30, 0.655), (x, -0.72, 0.650), 0.008, 0.035, up=(0, 0, 1), r=0.002) for x in (-0.67, -0.21, 0.21, 0.67)],
        [tube(_zigzag((x, -0.32, 0.662), (x, -0.70, 0.660), 0.015, 7, 0.010), 0.0021, 6, 1, 1)
         for x in (-0.58, -0.44, -0.30, -0.10, 0.10, 0.30, 0.44, 0.58)],
        # armazón de los respaldos (60/40) con bisagras y cierres
        [tube([(x0, -0.745, 0.72), (x0 + 0.0, -0.93, 1.20), (x1, -0.93, 1.20), (x1, -0.745, 0.72)], 0.012, 14, 1, 0)
         for x0, x1 in ((-0.67, -0.22), (-0.20, 0.67))],
        [tube([(x0, -0.84, 0.96), (x1, -0.84, 0.96)], 0.010, 12, 1, 0) for x0, x1 in ((-0.67, -0.22), (-0.20, 0.67))],
        [disc((x, -0.745, 0.72), X, 0.030, 0.012, 24, 0) for x in (-0.68, -0.21, 0.68)],
        [box((x, -0.93, 1.21), (0.040, 0.030, 0.030), 0.004, 2) for x in (-0.60, 0.60)],
        [screw((x, y, 0.600), Z, 0.010, 0.030, 2, "flange") for x in (-0.66, 0.66) for y in (-0.33, -0.70)],
    ]
    A(V4.part(M, "INT_SeatR_Frame", "INTERIOR_SEATS", ["seat_frame", "spring_steel", "connector_grey", "zinc"], shp,
              "Armazón del banco trasero: travesaños, muelles en zigzag, armazones de respaldo 60/40 con bisagras, "
              "cierres y tornillos al suelo", parent="SEAT_REAR", edir=(0, 0, -1), dist=0.10, stage=6,
              group="Asientos", fid="A", note=NOTE))
    for p, es in (("L", "izquierda"), ("C", "central"), ("R", "derecha")):
        A(V4.derived(M, f"INT_SeatR_{p}_Cushion", f"INT_SeatR_{p}_Cushion_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma del cojín trasero ({es})", scale=(0.93, 0.93, 0.82), offset=(0, 0, -0.006),
                     parent="SEAT_REAR", edir=(0, 0.287, 0.958), dist=0.17, stage=6, group="Asientos", fid="A",
                     note=NOTE))
        A(V4.derived(M, f"INT_SeatR_{p}_Back", f"INT_SeatR_{p}_Back_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma del respaldo trasero ({es})", scale=(0.93, 0.84, 0.94),
                     parent="SEAT_REAR", edir=(0, -0.958, 0.287), dist=0.18, stage=6, group="Asientos", fid="A",
                     note=NOTE))
    return out


# ---------------------------------------------------------------------------
# Volante
# ---------------------------------------------------------------------------
def steering_wheel(M):
    out = []
    ax = Vector((0, -0.958, 0.287))
    V4.set_explode("INT_SteeringWheel_Rim", tuple(ax), 0.40, 6)
    out += V4.derived(M, "INT_SteeringWheel_Rim", "INT_SteeringWheel_Armature", "STEERING", ["magnesium"],
                      "Alma de magnesio inyectado del aro del volante (bajo la espuma y el tapizado)",
                      core=(tuple(ax), 0.38), parent="STEERING_WHEEL", edir=tuple(ax), dist=0.20, stage=6,
                      group="Volante", fid="A", note=NOTE)
    c = Vector((-0.395, 0.7365, 1.02))
    u = Vector((1, 0, 0))
    v = ax.cross(u).normalized()
    out += V4.part(M, "INT_SteeringWheel_Hub_Internals", "STEERING", ["magnesium", "plastic_black", "copper",
                                                                       "zinc", "steel_black"], [
        [beam(tuple(c + u * sg * 0.035), tuple(c + u * sg * 0.180 + v * -0.01), 0.030, 0.010, up=tuple(ax), r=0.003)
         for sg in (-1, 1)],
        disc(tuple(c + ax * -0.045), tuple(ax), 0.060, 0.022, 36, 1),
        ring(tuple(c + ax * -0.045), tuple(ax), 0.030, 0.056, 0.008, 36, 2),
        taper(tuple(c + ax * -0.070), tuple(ax), [(0.0, 0.0), (0.030, 0.0), (0.034, 0.018), (0.020, 0.030), (0.0, 0.030)],
              28, 4),
        screw(tuple(c + ax * -0.032), tuple(ax), 0.014, 0.045, 3, "allen"),
    ], "Radios de magnesio, muelle de reloj (clock spring), adaptador estriado del buje y tornillo central del volante",
        parent="STEERING_WHEEL", edir=tuple(ax), dist=0.30, stage=6, group="Volante", fid="A", note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Cinturones: interior de los enrolladores
# ---------------------------------------------------------------------------
def seatbelt_retractors(M):
    import build_interior_detail as BID
    out = []
    for s, sd in ((1, "R"), (-1, "L")):
        for row, yb, xb in (("F", S.DOOR_B_SEAM_Y - 0.035, 0.80), ("R", S.CAB_REAR_Y + 0.05, 0.76)):
            low = Vector((s * xb - s * 0.01, yb + 0.02, BID.FLOOR_Z + 0.10))
            out += V4.part(M, f"INT_Seatbelt_{row}{sd}_Retractor", "INTERIOR_SEATS",
                           ["steel_bare", "seatbelt", "gear_steel", "steel_black", "hv_orange"], [
                               cyl(tuple(low + Vector((0, -0.030, -0.010))), tuple(low + Vector((0, 0.030, -0.010))),
                                   0.0075, seg=12, m=0),
                               cyl(tuple(low + Vector((0, -0.025, -0.010))), tuple(low + Vector((0, 0.025, -0.010))),
                                   0.022, seg=24, m=1),
                               gear(tuple(low + Vector((0, 0.033, -0.010))), Y, 0.020, 0.023, 0.004, 24, 0.008, 0.0, 2),
                               tube([tuple(low + Vector((s * 0.01, -0.034, -0.035))),
                                     tuple(low + Vector((s * 0.015, -0.034, 0.020))),
                                     tuple(low + Vector((0, -0.034, 0.035)))], 0.0045, 8, 4, 3),
                               cyl(tuple(low + Vector((s * 0.01, -0.034, -0.035))),
                                   tuple(low + Vector((s * 0.01, -0.034, -0.050))), 0.007, seg=12, m=4),
                           ], f"Interior del enrollador del cinturón {row}{sd}: carrete con cinta, rueda de bloqueo y "
                              "pretensor pirotécnico", edir=(-s, 0, 0.2), dist=0.30, stage=6, group="Cinturones",
                           fid="A", note=NOTE)
    return out


# ---------------------------------------------------------------------------
# Pantallas, audio y carga inalámbrica
# ---------------------------------------------------------------------------
def displays(M):
    out = []
    for nm, label in (("INT_Display_Center_Housing", "central de 18,5\""), ("INT_Display_Rear_Housing", "trasera de 9,4\"")):
        o = bpy.data.objects.get(nm)
        if o is None:
            continue
        fr = o.matrix_world.copy()
        d = o.data
        xs = [v.co.x for v in d.vertices]
        ys = [v.co.y for v in d.vertices]
        zs = [v.co.z for v in d.vertices]
        sx, sy, sz = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
        cx, cy, cz = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2
        thin = min((sx, 0), (sy, 1), (sz, 2))[1]
        nrm = [0, 0, 0]
        nrm[thin] = 1
        upv = (0, 0, 1) if thin != 2 else (0, 1, 0)
        size = [sx, sy, sz]
        wid = [size[i] for i in range(3) if i != thin]
        t = size[thin]

        def at(off):
            p = [cx, cy, cz]
            p[thin] += off
            return tuple(p)
        lcd = [0.0, 0.0, 0.0]
        lcd[thin] = 0.004
        for i in range(3):
            if i != thin:
                lcd[i] = size[i] * 0.94
        lcd2 = list(lcd)
        lcd2[thin] = 0.003
        shp = [box(at(-t * 0.30), tuple(lcd), 0.0, 0), box(at(-t * 0.18), tuple(lcd2), 0.0, 1),
               pcb(at(t * 0.10), (wid[0] * 0.70, wid[1] * 0.55, 0.0016), tuple(nrm), upv, 60, 100 + len(out), 2, 3, 4, 5, 6),
               box(at(t * 0.30), tuple(s * 0.9 if i != thin else 0.003 for i, s in enumerate(size)), 0.0, 7)]
        out += V4.part(M, nm.replace("_Housing", "_Internals"), "INTERIOR_CONTROLS",
                       ["screen", "led_white", "pcb_green", "plastic_black", "capacitor", "connector_grey", "solder_tin",
                        "alu_machined"], shp,
                       f"Interior de la pantalla {label}: panel LCD, retroiluminación, placa base y chapa de disipación",
                       frame=fr, parent=o.parent.name if o.parent else None, edir=(0, -0.5, 1), dist=0.22, stage=6,
                       group="Pantallas", fid="A", note=NOTE)
    return out


def door_speakers(M):
    out = []
    for door, x_grill, y0, y1 in (("FL", -0.765, 0.379, 0.539), ("FR", 0.765, 0.379, 0.539),
                                  ("RL", -0.750, -0.619, -0.459), ("RR", 0.750, -0.619, -0.459)):
        s = 1 if x_grill > 0 else -1
        c = Vector((x_grill + s * 0.006, (y0 + y1) / 2, 0.66))
        w = Vector((s, 0, 0))
        out += V4.part(M, f"INT_DoorSpeaker_{door}_Driver", "INTERIOR_DOORS",
                       ["plastic_black", "felt", "copper_enamel", "elec_steel", "steel_bare"], [
                           ring(tuple(c + w * 0.004), tuple(w), 0.070, 0.078, 0.006, 40, 0),
                           taper(tuple(c + w * 0.004), tuple(w), [(0.070, 0.0), (0.066, 0.004), (0.022, 0.030),
                                                                   (0.020, 0.034), (0.0, 0.034)], 40, 1),
                           taper(tuple(c + w * 0.006), tuple(w), [(0.0, 0.0), (0.020, 0.0), (0.020, 0.012), (0.0, 0.012)],
                                 24, 0),
                           cyl(tuple(c + w * 0.034), tuple(c + w * 0.046), 0.013, seg=20, m=2),
                           cyl(tuple(c + w * 0.040), tuple(c + w * 0.062), 0.034, seg=32, m=3),
                           [beam(tuple(c + w * 0.004 + Vector((0, math.cos(a), math.sin(a))) * 0.072),
                                 tuple(c + w * 0.040 + Vector((0, math.cos(a), math.sin(a))) * 0.034), 0.006, 0.002,
                                 up=(0, math.cos(a), math.sin(a)), r=0.0, m=4) for a in (0.4, 2.0, 3.6, 5.2)],
                       ], f"Altavoz de la puerta {door}: cesta, cono, guardapolvo, bobina móvil e imán de ferrita",
                       parent=f"DOOR_{door}", edir=(s, 0, 0.2), dist=0.30, stage=6, group="Audio", fid="A", note=NOTE)
    return out


def console_and_ip(M):
    out = []
    out += V4.part(M, "INT_Console_Wireless_Charger_Coils", "INTERIOR_CONTROLS", ["copper_enamel", "elec_steel"] + PCB_MATS, [
        [V4.torus((x, 0.83, 0.804), Z, rr, 0.0011, 40, 6, 0) for x in (-0.045, 0.045) for rr in (0.010, 0.014, 0.018, 0.022)],
        box((0.0, 0.83, 0.800), (0.19, 0.13, 0.002), 0.0, 1),
        pcb((0.0, 0.83, 0.795), (0.18, 0.12, 0.0016), Z, X, 30, 120, 2, 3, 4, 5, 6),
    ], "Bobinas Qi, ferritas y placa de los dos cargadores inalámbricos de la consola",
        parent="CONSOLE_ASSEMBLY", edir=(0, 0, 1), dist=0.30, stage=6, group="Consola", fid="A", note=NOTE)
    # mazo principal del salpicadero
    trunk = [(-0.76, 1.06, 0.97), (-0.40, 1.05, 0.985), (0.0, 1.05, 0.99), (0.40, 1.05, 0.985), (0.76, 1.06, 0.97)]
    branches = [
        [(-0.62, 1.06, 0.97), (-0.64, 1.20, 0.90), (-0.62, 1.29, 0.85)],
        [(0.62, 1.06, 0.97), (0.64, 1.20, 0.90), (0.62, 1.29, 0.85)],
        [(0.0, 1.05, 0.99), (0.0, 1.00, 1.06), (0.0, 0.97, 1.10)],
        [(0.30, 1.05, 0.985), (0.33, 1.15, 1.00), (0.33, 1.22, 1.00)],
        [(-0.39, 1.05, 0.985), (-0.39, 1.08, 0.93), (-0.39, 1.12, 0.90)],
        [(0.10, 1.05, 0.99), (0.10, 1.05, 0.93), (0.10, 1.02, 0.90)],
        [(-0.05, 1.05, 0.99), (-0.10, 0.98, 0.80), (-0.12, 0.90, 0.62), (-0.12, 0.60, 0.55), (-0.05, 0.36, 0.55)],
    ]
    shp = [tube(trunk, 0.012, 12, 4, 0)]
    for br in branches:
        shp.append(tube(br, 0.006, 8, 4, 0))
        e = Vector(br[-1])
        shp.append(box(tuple(e), (0.030, 0.022, 0.016), 0.002, 1))
    shp += [V4.clip(p, (0, 0, 1), 0.012, 2) for p in ((-0.55, 1.05, 0.972), (-0.20, 1.05, 0.977), (0.20, 1.05, 0.977),
                                                       (0.55, 1.05, 0.972))]
    out += V4.part(M, "LV_Harness_IP_Main", "INTERIOR_DASHBOARD", ["harness", "connector_grey", "nylon"], shp,
                   "Mazo principal del salpicadero: tronco a lo largo de la viga transversal con ramales a pantalla, "
                   "ordenador, climatizador, actuador del volante, controladores y módulo de airbags",
                   parent="IP_ASSEMBLY", edir=(0, 0.6, 1), dist=0.45, stage=6, group="Baja tensión", fid="A", note=NOTE)
    return out


def build(M):
    out = []
    out += front_seats(M)
    out += rear_bench(M)
    out += steering_wheel(M)
    out += seatbelt_retractors(M)
    out += displays(M)
    out += door_speakers(M)
    out += console_and_ip(M)
    return out
