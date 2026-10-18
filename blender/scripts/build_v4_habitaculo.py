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
def _rotx(deg):
    return Matrix.Rotation(math.radians(deg), 3, "X")


def _back_frame(b0, tilt_deg):
    """Funciones (local → mundo, mundo → local) del respaldo: x lateral, d hacia delante, h hacia arriba."""
    R = _rotx(tilt_deg)
    Ri = R.inverted()
    b0 = Vector(b0)
    to_w = lambda x, d, h: tuple(b0 + R @ Vector((x, d, h)))
    to_l = lambda p: Ri @ (Vector(p) - b0)
    return to_w, to_l, R, b0


def _foam_back(b0, tilt_deg, d_cut, k_front=0.85, k_x=0.94):
    """Espuma del respaldo: el tapizado recortado por detrás (sitio para el armazón) y algo encogido."""
    to_w, to_l, R, b = _back_frame(b0, tilt_deg)

    def fn(p):
        q = to_l(p)
        d = max(q.y, d_cut)
        d = d_cut + (d - d_cut) * k_front
        return to_w(q.x * k_x, d, q.z * 0.965 + 0.012)
    return fn


def _foam_cushion(xc, yc, z0, k_z=0.92, k_x=0.95, k_y=0.96):
    """Espuma del cojín: el tapizado encogido hacia su base (queda dentro de la funda)."""
    def fn(p):
        return (xc + (p.x - xc) * k_x, yc + (p.y - yc) * k_y, z0 + 0.004 + (p.z - z0) * k_z)
    return fn


def front_seats(M):
    out = []
    A = out.extend
    for sd in ("R", "L"):
        V4.set_explode(f"INT_SeatF_{sd}_Cushion", None, 0.34, 6)
        V4.set_explode(f"INT_SeatF_{sd}_Back", None, 0.36, 6)
    # Lado derecho; la pareja izquierda se refleja. Respaldo: base b0 = (x, 0,26, 0,78), reclinado 22°.
    xc = 0.395
    to_w, _, R, _ = _back_frame((xc, 0.26, 0.78), 22)
    d_fr = -0.070                                     # plano del armazón (por detrás de la espuma)
    side = [(0.200, 0.06), (0.200, 0.46), (0.120, 0.58), (0.100, 0.74)]
    shp = [
        # cojín: largueros laterales, travesaños bajo la bandeja y muelles sinuosos sobre ella
        [beam((x, 0.30, 0.640), (x, 0.745, 0.640), 0.008, 0.040, up=(0, 0, 1), r=0.002) for x in (0.175, 0.615)],
        [tube([(0.175, y, 0.634), (0.615, y, 0.634)], 0.0115, 14, 1, 0) for y in (0.305, 0.735)],
        [tube(_zigzag((x, 0.31, 0.676), (x, 0.725, 0.676), 0.016, 8, 0.0), 0.0021, 6, 1, 1)
         for x in (0.25, 0.34, 0.44, 0.53)],
        # herrajes de reclinado en el hueco entre el cojín y el respaldo, con barra de sincronización
        disc((0.675, 0.235, 0.72), X, 0.036, 0.014, 32, 0),
        gear((0.675, 0.235, 0.72), X, 0.026, 0.029, 0.016, 30, 0.0, 0.0, 0),
        # el interior, por fuera del panel lateral de la consola (|x| <= 0,146)
        disc((0.160, 0.235, 0.72), X, 0.030, 0.010, 28, 0),
        tube([(0.160, 0.235, 0.72), (0.675, 0.235, 0.72)], 0.007, 10, 1, 0),
        # respaldo: tubos laterales y superior, chapa inferior y malla lumbar, en el plano del armazón
        [tube([to_w(sg * x, d_fr, h) for x, h in side], 0.011, 14, 4, 0) for sg in (1, -1)],
        tube([to_w(-0.10, d_fr, 0.74), to_w(0.0, d_fr, 0.755), to_w(0.10, d_fr, 0.74)], 0.011, 14, 4, 0),
        beam(to_w(-0.200, d_fr, 0.10), to_w(0.200, d_fr, 0.10), 0.060, 0.006, up=tuple(R @ Vector((0, 1, 0))),
             r=0.0),
        [tube([to_w(-0.200, -0.062, h), to_w(0.0, -0.060, h), to_w(0.200, -0.062, h)], 0.0022, 6, 3, 1)
         for h in (0.22, 0.29, 0.36, 0.43)],
        [tube([to_w(x, -0.061, 0.18), to_w(x, -0.061, 0.45)], 0.0022, 6, 1, 1) for x in (-0.09, 0.09)],
    ]
    A(V4.part(M, "INT_SeatF_Frame", "INTERIOR_SEATS", ["seat_frame", "spring_steel"], shp,
              "Armazón del asiento delantero {lado}: largueros, travesaños, muelles sinuosos, herrajes de reclinado "
              "con barra de sincronización y armazón del respaldo con malla lumbar", mirror=True,
              parent="SEAT_FRONT_R", edir=(0.2, 0, -1), dist=0.10, stage=6, group="Asientos", fid="A", note=NOTE))
    for sd, s in (("R", 1), ("L", -1)):
        lado = "derecho" if s > 0 else "izquierdo"
        A(V4.derived(M, f"INT_SeatF_{sd}_Cushion", f"INT_SeatF_{sd}_Cushion_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma de poliuretano moldeada del cojín delantero {lado}",
                     xform=_foam_cushion(s * xc, 0.525, 0.684), evaluated=True, parent=f"SEAT_FRONT_{sd}",
                     edir=(0, 0.287, 0.958), dist=0.17, stage=6, group="Asientos", fid="A", note=NOTE))
        A(V4.derived(M, f"INT_SeatF_{sd}_Back", f"INT_SeatF_{sd}_Back_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma de poliuretano moldeada del respaldo delantero {lado}",
                     xform=_foam_back((s * xc, 0.26, 0.78), 22, -0.045), evaluated=True,
                     parent=f"SEAT_FRONT_{sd}", edir=(0, -0.958, 0.287), dist=0.18, stage=6, group="Asientos",
                     fid="A", note=NOTE))
    # esteras de calefacción y ventilación dentro de la espuma (cojín) y en el plano medio del respaldo
    A(V4.part(M, "INT_SeatF_Heat_Vent_Mats", "INTERIOR_SEATS", ["felt", "copper"], [
        box((xc, 0.52, 0.80), (0.36, 0.36, 0.0015), 0.0, 0),
        [box((xc, 0.37 + 0.03 * k, 0.8012), (0.33, 0.0015, 0.0006), 0.0, 1) for k in range(11)],
        beam(to_w(0.0, -0.020, 0.12), to_w(0.0, -0.020, 0.50), 0.30, 0.0015, up=tuple(R @ Vector((0, 1, 0))),
             r=0.0, m=0),
    ], "Esteras de calefacción (hilo resistivo) y de ventilación del asiento delantero {lado}", mirror=True,
        parent="SEAT_FRONT_R", edir=(0, 0.3, 1), dist=0.26, stage=6, group="Asientos", fid="A", note=NOTE))
    return out


def rear_bench(M):
    out = []
    A = out.extend
    for p in ("L", "C", "R"):
        V4.set_explode(f"INT_SeatR_{p}_Cushion", None, 0.34, 6)
        V4.set_explode(f"INT_SeatR_{p}_Back", None, 0.36, 6)
    hy = -0.63                                         # build_interior.H_REAR (v4)
    shp = [
        # bastidor bajo la bandeja (z 0,626…0,644), muelles sinuosos sobre ella
        [beam((x, hy + 0.0, 0.600), (x, hy + 0.43, 0.600), 0.008, 0.030, up=(0, 0, 1), r=0.002)
         for x in (-0.67, -0.21, 0.21, 0.67)],
        [tube([(-0.67, y, 0.612), (0.67, y, 0.612)], 0.013, 14, 1, 0) for y in (hy + 0.0, hy + 0.43)],
        [tube(_zigzag((x, hy + 0.02, 0.649), (x, hy + 0.41, 0.649), 0.015, 7, 0.0), 0.0021, 6, 1, 1)
         for x in (-0.58, -0.44, -0.30, -0.10, 0.10, 0.30, 0.44, 0.58)],
    ]
    # armazón de cada respaldo, en su plano trasero (b0 = (x, −0,69, 0,75), reclinado 15°)
    for xs, w in ((-0.45, 0.46), (0.0, 0.42), (0.45, 0.46)):
        to_w, _, R, _ = _back_frame((xs, hy - 0.06, 0.75), 15)
        hw = w / 2 - 0.06
        shp += [tube([to_w(-hw, -0.075, 0.06), to_w(-hw, -0.075, 0.38), to_w(-hw * 0.7, -0.075, 0.42),
                      to_w(hw * 0.7, -0.075, 0.42), to_w(hw, -0.075, 0.38), to_w(hw, -0.075, 0.06)], 0.010, 12, 3, 0),
                tube([to_w(-hw, -0.075, 0.22), to_w(hw, -0.075, 0.22)], 0.008, 10, 1, 0),
                box(to_w(hw * 0.8, -0.068, 0.40), (0.030, 0.016, 0.020), 0.003, 2)]
    A(V4.part(M, "INT_SeatR_Frame", "INTERIOR_SEATS", ["seat_frame", "spring_steel", "connector_grey"], shp,
              "Armazón de la banqueta trasera: bastidor, muelles sinuosos y armazones de los respaldos con cierres",
              parent="SEAT_REAR", edir=(0, 0, -1), dist=0.10, stage=6, group="Asientos", fid="A", note=NOTE))
    for p, xs, es in (("L", -0.45, "izquierda"), ("C", 0.0, "central"), ("R", 0.45, "derecha")):
        A(V4.derived(M, f"INT_SeatR_{p}_Cushion", f"INT_SeatR_{p}_Cushion_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma del cojín trasero ({es})", xform=_foam_cushion(xs, hy + 0.21, 0.653), evaluated=True,
                     parent="SEAT_REAR", edir=(0, 0.287, 0.958), dist=0.17, stage=6, group="Asientos", fid="A",
                     note=NOTE))
        A(V4.derived(M, f"INT_SeatR_{p}_Back", f"INT_SeatR_{p}_Back_Foam", "INTERIOR_SEATS", ["foam_pu"],
                     f"Espuma del respaldo trasero ({es})", xform=_foam_back((xs, hy - 0.06, 0.75), 15, -0.055),
                     evaluated=True, parent="SEAT_REAR", edir=(0, -0.958, 0.287), dist=0.18, stage=6,
                     group="Asientos", fid="A", note=NOTE))
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
    # mismos ejes que el buje de build_interior_detail (columna inclinada (0, 1, -0,42)): el interior va dentro del
    # cojín central (0–50 mm a lo largo de la columna desde el centro del volante) y de sus radios
    c = Vector((-0.395, 0.735, 1.02))
    ax = -Vector((0, 1, -0.42)).normalized()
    u = Vector((1, 0, 0))
    v = ax.cross(u).normalized()
    out += V4.part(M, "INT_SteeringWheel_Hub_Internals", "STEERING", ["magnesium", "plastic_black", "copper",
                                                                       "zinc", "steel_black"], [
        # radios centrados en el espesor de los radios del buje, por fuera del módulo del airbag (±55 mm) y sin llegar
        # al aro; muelle de reloj con el paso del tornillo central detrás del airbag; adaptador estriado dentro del
        # tubo de la cubierta de la columna (radio interior 45 mm)
        [beam(tuple(c + u * sg * 0.060 - v * 0.012 - ax * 0.018), tuple(c + u * sg * 0.160 - v * 0.012 - ax * 0.018),
              0.024, 0.010, up=tuple(ax), r=0.003) for sg in (-1, 1)],
        ring(tuple(c + ax * -0.039), tuple(ax), 0.018, 0.034, 0.014, 36, 1),
        ring(tuple(c + ax * -0.039), tuple(ax), 0.026, 0.033, 0.016, 36, 2),
        taper(tuple(c + ax * -0.084), tuple(ax), [(0.0, 0.0), (0.030, 0.0), (0.034, 0.018), (0.020, 0.030), (0.0, 0.030)],
              28, 4),
        screw(tuple(c + ax * -0.048), tuple(ax), 0.014, 0.045, 3, "allen"),
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
        # dentro de la carcasa del enrollador (build_interior_detail.seatbelts: 36 × 80 × 110 mm)
        for row, yb, xr in (("F", S.DOOR_B_SEAM_Y - 0.035, 0.728), ("R", S.CAB_REAR_Y + 0.05, 0.724)):
            low = Vector((s * xr, yb + 0.02, BID.FLOOR_Z + 0.10))
            out += V4.part(M, f"INT_Seatbelt_{row}{sd}_Retractor", "INTERIOR_SEATS",
                           ["steel_bare", "seatbelt", "gear_steel", "steel_black", "hv_orange"], [
                               cyl(tuple(low + Vector((0, -0.032, -0.010))), tuple(low + Vector((0, 0.032, -0.010))),
                                   0.0060, seg=12, m=0),
                               cyl(tuple(low + Vector((0, -0.024, -0.010))), tuple(low + Vector((0, 0.024, -0.010))),
                                   0.0145, seg=24, m=1),
                               gear(tuple(low + Vector((0, 0.030, -0.010))), Y, 0.0125, 0.0145, 0.004, 24, 0.0062, 0.0, 2),
                               tube([tuple(low + Vector((s * 0.007, -0.034, -0.035))),
                                     tuple(low + Vector((s * 0.009, -0.034, 0.020))),
                                     tuple(low + Vector((0, -0.034, 0.035)))], 0.0040, 8, 4, 3),
                               cyl(tuple(low + Vector((s * 0.007, -0.034, -0.032))),
                                   tuple(low + Vector((s * 0.007, -0.034, -0.048))), 0.0065, seg=12, m=4),
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
    """Altavoz de cada puerta, detrás del panel de guarnecido y alineado con su rejilla (build_interior_detail)."""
    out = []
    for s, sd in ((1, "R"), (-1, "L")):
        for key, (yf, yr) in (("F", (S.DOOR_F_FRONT_Y - 0.02, S.DOOR_B_SEAM_Y + 0.01)),
                              ("R", (S.DOOR_B_SEAM_Y - 0.01, S.DOOR_R_REAR_Y + 0.01))):
            door = f"{key}{sd}"
            xw = 0.805 if key == "F" else 0.790          # cara exterior del panel (contra la estructura)
            yfa = yf - (0.10 if key == "F" else 0.0)
            ym = (yfa + yr) / 2
            c = Vector((s * (xw + 0.004), ym - 0.12, 0.744))
            w = Vector((s, 0, 0))
            out += V4.part(M, f"INT_DoorSpeaker_{door}_Driver", "INTERIOR_DOORS",
                           ["plastic_black", "felt", "copper_enamel", "elec_steel", "steel_bare"], [
                               ring(tuple(c + w * 0.003), tuple(w), 0.046, 0.054, 0.006, 40, 0),
                               taper(tuple(c + w * 0.003), tuple(w), [(0.046, 0.0), (0.043, 0.004), (0.016, 0.026),
                                                                     (0.014, 0.030), (0.0, 0.030)], 40, 1),
                               taper(tuple(c + w * 0.005), tuple(w), [(0.0, 0.0), (0.014, 0.0), (0.014, 0.010),
                                                                     (0.0, 0.010)], 24, 0),
                               cyl(tuple(c + w * 0.030), tuple(c + w * 0.040), 0.010, seg=20, m=2),
                               cyl(tuple(c + w * 0.035), tuple(c + w * 0.055), 0.026, seg=32, m=3),
                               [beam(tuple(c + w * 0.003 + Vector((0, math.cos(a), math.sin(a))) * 0.050),
                                     tuple(c + w * 0.035 + Vector((0, math.cos(a), math.sin(a))) * 0.026), 0.006,
                                     0.002, up=(0, math.cos(a), math.sin(a)), r=0.0, m=4) for a in (0.4, 2.0, 3.6, 5.2)],
                           ], f"Altavoz de la puerta {door}: cesta, cono, guardapolvo, bobina móvil e imán de ferrita",
                           parent=f"DOOR_{door}", edir=(s, 0, 0.2), dist=0.30, stage=6, group="Audio", fid="A",
                           note=NOTE)
    return out


def console_and_ip(M):
    out = []
    out += V4.part(M, "INT_Console_Wireless_Charger_Coils", "INTERIOR_CONTROLS", ["copper_enamel", "elec_steel"] + PCB_MATS, [
        [V4.torus((x, 0.83, 0.792), Z, rr, 0.0011, 40, 6, 0) for x in (-0.045, 0.045) for rr in (0.010, 0.014, 0.018, 0.022)],
        box((0.0, 0.83, 0.788), (0.19, 0.13, 0.002), 0.0, 1),
        pcb((0.0, 0.83, 0.783), (0.18, 0.12, 0.0016), Z, X, 30, 120, 2, 3, 4, 5, 6),
    ], "Bobinas Qi, ferritas y placa de los dos cargadores inalámbricos de la consola",
        parent="CONSOLE_ASSEMBLY", edir=(0, 0, 1), dist=0.30, stage=6, group="Consola", fid="A", note=NOTE)
    # mazo principal del salpicadero
    # tronco apoyado sobre la viga transversal (eje y = 1,07, z = 0,985, radio 32 mm) y ramales que bajan por
    # detrás de ella hasta la cara de conexión de cada módulo (sin entrar en las cajas)
    trunk = [(-0.76, 1.00, 0.97), (-0.70, 1.02, 1.00), (-0.62, 1.07, 1.031), (0.0, 1.07, 1.031), (0.62, 1.07, 1.031),
             (0.70, 1.02, 1.00), (0.76, 1.00, 0.97)]
    branches = [
        [(-0.62, 1.024, 1.0), (-0.63, 1.02, 0.93), (-0.645, 1.12, 0.88), (-0.66, 1.236, 0.85)],
        # lado derecho: por detrás de la guantera (y > 1,10) hasta el controlador, retrasado tras el soplador
        [(0.62, 1.07, 1.031), (0.63, 1.13, 1.0), (0.645, 1.18, 0.90), (0.66, 1.291, 0.85)],
        [(0.0, 1.07, 1.031), (0.0, 1.03, 1.06), (0.0, 1.0, 1.072)],
        [(0.30, 1.07, 1.031), (0.32, 1.078, 1.028), (0.33, 1.084, 1.025)],
        [(-0.36, 1.024, 1.0), (-0.33, 1.02, 0.94), (-0.32, 1.06, 0.88)],
        [(0.10, 1.024, 1.0), (0.10, 1.02, 0.94), (0.10, 1.02, 0.905)],
        [(-0.05, 1.024, 1.0), (-0.10, 0.98, 0.80), (-0.12, 0.90, 0.62), (-0.10, 0.70, 0.56), (-0.05, 0.45, 0.58)],
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
