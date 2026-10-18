"""Versión 4 · carrocería y exterior por dentro: refuerzos de puertas, faros, mecanismos y conectores.

  Puertas: vigas antiintrusión de acero de ultra alta resistencia con sus soportes y guías del cristal.
  Faros: disipadores de aletas de los módulos LED, placa de control (driver), motor de nivelación y
    respiradero de membrana.
  Cubierta de la caja: motor, tornillo sinfín y piñón de cadena dentro de cada motor de la cubierta.
  Toma de carga: actuador de bloqueo del conector y motor de la tapa.
  Remolque: tomas de 7 y 4 polos junto al receptor del enganche.
  Emblema Cyberbeast: insignia con la cabeza de Cerbero en la parte trasera derecha ([V] hoja de rescate).

Fidelidad: existencia [V] cuando consta en el manual o en la hoja de rescate (toma de carga, emblema) o
imprescindible por función (vigas de puerta, disipadores); forma y posición reconstruidas («Aproximado»).
"""

import math
from mathutils import Vector
import bpy
import ct_v4 as V4
from ct_v4 import (gear, sphere, taper, tube, screw, pcb, coil, fins, box, cyl, ring, disc, hull, beam, bolt, nut,
                   torx, clip)
import build_v4_chasis as CH

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NOTE = "Pieza necesaria por función; forma, dimensiones y posición reconstruidas (no hay planos publicados)"
PCB_MATS = ["pcb_green", "plastic_black", "capacitor", "connector_grey", "solder_tin"]


def bbox(name):
    o = bpy.data.objects.get(name)
    if o is None:
        return None
    dg = bpy.context.evaluated_depsgraph_get()
    mw = o.evaluated_get(dg).matrix_world
    pts = [mw @ Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def doors(M):
    out = []
    for door in ("FL", "FR", "RL", "RR"):
        bb = bbox(f"DOOR_{door}_InnerStructure")
        if bb is None:
            continue
        mn, mx = bb
        s = 1 if mx.x > 0 else -1
        xo = (mx.x - 0.045) if s > 0 else (mn.x + 0.045)
        # soportes en los extremos de la viga, a 120 mm de los bordes de la puerta: más cerca caerían sobre la
        # pestaña del anillo de la puerta de la carrocería
        y0, y1 = mn.y + 0.12, mx.y - 0.12
        za, zb = mn.z + 0.30, mn.z + 0.22
        shp = [
            tube([(xo, y1, za), (xo, y0, zb)], 0.0175, 18, 1, 0),
            [box((xo - s * 0.010, y, z), (0.012, 0.070, 0.090), 0.003, 1) for y, z in ((y1, za), (y0, zb))],
            [screw((xo - s * 0.018, y + dy, z + dz), (-s, 0, 0), 0.008, 0.02, 2, "flange")
             for y, z in ((y1, za), (y0, zb)) for dy, dz in ((0.0, 0.03), (0.0, -0.03))],
            # guías del cristal (canales delantero y trasero)
            [beam((xo - s * 0.035, y, mn.z + 0.12), (xo - s * 0.035, y, mx.z - 0.06), 0.022, 0.016, up=(1, 0, 0), r=0.002,
                  m=3) for y in (mn.y + 0.10, mx.y - 0.10)],
        ]
        side = "delantera" if door[0] == "F" else "trasera"
        out += V4.part(M, f"EXT_Door_{door}_Intrusion_Beam", "DOORS_AND_HATCHES",
                       ["steel_black", "ecoat", "zinc", "plastic_black"], shp,
                       f"Viga antiintrusión de acero de ultra alta resistencia de la puerta {side} {door[1]} con soportes, "
                       "tornillos y guías del cristal", parent=f"DOOR_{door}", edir=(-s, 0, -0.4), dist=0.30, stage=6,
                       group="Puertas", fid="A", note=NOTE)
    return out


def headlamps(M):
    out = []
    for sd, s in (("L", -1), ("R", 1)):
        bb = bbox(f"LGT_Headlamp_{sd}")
        if bb is None:
            continue
        mn, mx = bb
        cx = (mn.x + mx.x) / 2
        yb = mn.y + 0.03
        zc = (mn.z + mx.z) / 2
        out += V4.part(M, f"LGT_Headlamp_{sd}_Internals", "LIGHTING",
                       ["alu_cast", "elec_steel", "copper_enamel", "gear_steel", "nylon"] + PCB_MATS + ["felt"], [
                           [fins((cx + dx, yb, zc), X, Z, (0.09, 0.040, 0.075), 12, 0.0018, 0) for dx in (-0.08, 0.05)],
                           [box((cx + dx, yb + 0.022, zc), (0.095, 0.004, 0.080), 0.001, 0) for dx in (-0.08, 0.05)],
                           pcb((mn.x + 0.06 if s < 0 else mx.x - 0.06, yb + 0.01, zc - 0.03),
                               (0.08, 0.05, 0.0016), (0, -1, 0), Z, 25, 130 + s, 5, 6, 7, 8, 9),
                           CH._small_motor((cx, yb + 0.005, mn.z + 0.025), X, 0.012, 0.03, 1, 2, 3, 6),
                           cyl((mx.x - 0.03 if s < 0 else mn.x + 0.03, mn.y + 0.006, mx.z - 0.03),
                               (mx.x - 0.03 if s < 0 else mn.x + 0.03, mn.y - 0.004, mx.z - 0.03), 0.008, seg=14, m=10),
                       ], f"Interior del faro {'izquierdo' if s < 0 else 'derecho'}: disipadores de los módulos LED, placa de "
                          "control, motor de nivelación y respiradero", edir=(0, -1, 0.3), dist=0.40, stage=6,
                       group="Iluminación", fid="A", note=NOTE)
    return out


def tonneau_motors(M):
    out = []
    for sd in ("L", "R"):
        bb = bbox(f"CARGO_Tonneau_Motor_{sd}")
        if bb is None:
            continue
        mn, mx = bb
        c = (mn + mx) / 2
        s = 1 if c.x > 0 else -1
        out += V4.part(M, f"CARGO_Tonneau_Motor_{sd}_Internals", "CARGO_BED", ["elec_steel", "copper_enamel",
                                                                              "gear_steel", "nylon"], [
            CH._small_motor((c.x, c.y - 0.02, c.z + 0.02), Y, 0.026, 0.07, 0, 1, 2, 8),
            gear((c.x, c.y + 0.035, c.z + 0.02), Y, 0.004, 0.0055, 0.025, 4, 0.0, 65.0, 2, 8),
            gear((c.x - s * 0.015, c.y + 0.035, c.z - 0.012), X, 0.022, 0.025, 0.010, 30, 0.004, 0.0, 3),
            gear((c.x + s * 0.03, c.y + 0.035, c.z - 0.012), X, 0.018, 0.022, 0.008, 14, 0.006, 0.0, 2),
        ], f"Interior del motor {'izquierdo' if s < 0 else 'derecho'} de la cubierta de la caja: motor, sinfín, corona "
           "y piñón de la cadena", edir=(s, 0, 1), dist=0.40, stage=6, group="Cubierta", fid="A", note=NOTE)
    return out


def charge_port(M):
    """Actuador de bloqueo y motor de la tapa, encima del controlador de la toma (sin tocar barras ni toma)."""
    bb = bbox("EXT_ChargePort_ECU")
    if bb is None:
        return []
    mn, mx = bb
    c = (mn + mx) / 2
    s = 1 if c.x > 0 else -1
    zt = mx.z + 0.004
    return V4.part(M, "EXT_ChargePort_Lock_Actuator", "DOORS_AND_HATCHES", ["plastic_black", "elec_steel",
                                                                             "copper_enamel", "steel_bare",
                                                                             "connector_grey"], [
        box((c.x, c.y - 0.035, zt + 0.014), (0.030, 0.030, 0.028), 0.003, 0),
        cyl((c.x - s * 0.016, c.y - 0.035, zt + 0.014), (c.x - s * 0.036, c.y - 0.035, zt + 0.014), 0.004, seg=10, m=3),
        CH._small_motor((c.x, c.y + 0.030, zt + 0.014), Y, 0.012, 0.035, 1, 2, 3, 6),
        box((c.x, c.y - 0.005, zt + 0.006), (0.016, 0.014, 0.010), 0.002, 4),
    ], "Actuador de bloqueo del conector de carga y motor de la tapa de la toma NACS",
        edir=(s, 0, 0.6), dist=0.35, stage=6, group="Carga", fid="A", note=NOTE)


def trailer_sockets(M):
    bb = bbox("CHS_Tow_Hitch_Receiver")
    if bb is None:
        return []
    mn, mx = bb
    c = (mn + mx) / 2
    p7 = Vector((c.x + 0.12, mn.y + 0.02, c.z + 0.01))
    p4 = Vector((c.x + 0.20, mn.y + 0.02, c.z + 0.01))
    shp = [cyl(tuple(p7), tuple(p7 + Vector((0, 0.05, 0))), 0.034, seg=28, m=0),
           disc(tuple(p7 - Vector((0, 0.004, 0))), Y, 0.036, 0.008, 28, 1),
           box(tuple(p4 + Vector((0, 0.02, 0))), (0.030, 0.040, 0.016), 0.003, 0),
           box(tuple(p4 - Vector((0, 0.004, 0))), (0.034, 0.008, 0.020), 0.002, 1)]
    for k in range(6):
        a = 2 * math.pi * k / 6
        shp.append(cyl(tuple(p7 + Vector((0.020 * math.cos(a), -0.005, 0.020 * math.sin(a)))),
                       tuple(p7 + Vector((0.020 * math.cos(a), 0.010, 0.020 * math.sin(a)))), 0.0025, seg=8, m=2))
    shp.append(cyl(tuple(p7 + Vector((0, -0.005, 0))), tuple(p7 + Vector((0, 0.010, 0))), 0.0025, seg=8, m=2))
    return V4.part(M, "CHS_Trailer_Sockets", "UNDERBODY", ["plastic_black", "rubber_seal", "valve_brass"], shp,
                   "Tomas eléctricas de remolque de 7 polos (SAE J2863) y 4 polos con tapas",
                   edir=(0, -1, -0.3), dist=0.40, stage=6, group="Remolque", fid="A", note=NOTE)


def cyberbeast_emblem(M):
    bb = bbox("EXT_Tailgate")
    if bb is None:
        return []
    mn, mx = bb
    c = Vector((mx.x - 0.16, mn.y - 0.0015, mn.z + 0.12))
    shp = [taper(tuple(c), (0, -1, 0), [(0.0, 0.0), (0.028, 0.0), (0.030, 0.0015), (0.028, 0.003), (0.0, 0.003)], 40, 0)]
    for k, dx in enumerate((-0.014, 0.0, 0.014)):
        shp.append(hull([(c.x + dx + ex, c.y - 0.003 - ey, c.z + ez) for ex in (-0.006, 0.006) for ey in (0.0, 0.002)
                         for ez in ((-0.010, 0.010) if k == 1 else (-0.008, 0.008))], 1))
    return V4.part(M, "EXT_Cyberbeast_Emblem", "EXTERIOR_PANELS", ["black_gloss", "alu_trim"], shp,
                   "Emblema Cyberbeast (cabeza de Cerbero) en la parte trasera derecha", edir=(0, -1, 0), dist=0.35,
                   stage=6, group="Exterior", fid="A",
                   note="Existencia y lado según la hoja de rescate de Tesla; forma y posición exactas aproximadas")


def build(M):
    out = []
    out += doors(M)
    out += headlamps(M)
    out += tonneau_motors(M)
    out += charge_port(M)
    out += trailer_sockets(M)
    out += cyberbeast_emblem(M)
    return out
