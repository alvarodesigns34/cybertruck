"""Versión 3 · exterior, cierres, caja, tonneau y luces: apliques, carenados, juntas, soportes y actuadores.

Fuentes (docs/ficha-tecnica-piezas.md §3.1; manual de servicio «SM» y manual del propietario «OM»):
  [V] Denominación, cantidad y fijaciones (EXT-xxx).
  [R] Forma y posición reconstruidas dentro de la envolvente oficial; no hay planos de estas piezas.
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, rivet, ribs

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend

    # --- Frontal ----------------------------------------------------------------------------------------
    A(V3.part(M, "EXT_Powergate_Fascia", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((0, 2.600, 1.010), (1.10, 0.060, 0.012), 0.003),
        line(clip, (-0.46, 2.600, 1.016), (0.46, 2.600, 1.016), 6, axis=Z, d=0.012),
    ], "Fascia del Powergate (cubierta del borde delantero del capó, se retira antes de la barra de luz)",
        edir=(0, 0.6, 1), dist=0.55))
    A(V3.part(M, "EXT_Front_Center_Applique", "EXTERIOR_PANELS", ["plastic_black"], [
        box((0, 2.655, 0.80), (0.56, 0.016, 0.22), 0.004),
    ], "Aplique central delantero (se retira para acceder al faro)", edir=(0, 1, 0.2), dist=0.5))
    A(V3.part(M, "EXT_Front_Fascia_Fairing", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((0.50, 2.592, 0.66), (0.22, 0.04, 0.13), 0.004),
        bolt((0.44, 2.570, 0.66), Y, 0.007, 1, 0.0),
    ], "Carenado {lado} de la fascia delantera", mirror=True, edir=(0.5, 1, 0), dist=0.45))
    A(V3.part(M, "EXT_Lightbar_Beauty_Cover", "EXTERIOR_PANELS", ["plastic_black"], [
        box((0.83, S.front_plan_y(0.83) - 0.012, 0.975), (0.10, 0.012, 0.045), 0.003),
    ], "Embellecedor {lado} de la barra de luz delantera", mirror=True, edir=(0.4, 1, 0.3), dist=0.4))
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        # soportes de aleta (Fore/Aft de pasos delanteros y traseros)
        A(V3.part(M, f"EXT_Flare_Carrier_{sd}", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
            box((s * 0.965, 2.10, 0.93), (0.05, 0.10, 0.09), 0.003),
            box((s * 0.965, 1.50, 0.90), (0.05, 0.10, 0.09), 0.003),
            box((s * 0.965, -1.50, 0.93), (0.05, 0.10, 0.09), 0.003),
            box((s * 0.965, -2.14, 0.90), (0.05, 0.10, 0.09), 0.003),
            [bolt((s * 0.94, y, 0.93), (-s, 0, 0), 0.007, 1) for y in (2.10, 1.50, -1.50, -2.14)],
        ], f"Soportes {side}s de las aletas de paso de rueda (Fore/Aft delanteros y traseros; 2 y 6 pernos a 7 N·m)",
            edir=(s, 0, 0.3), dist=0.4))
        A(V3.part(M, f"EXT_Fender_Baffle_Front_{sd}", "EXTERIOR_PANELS", ["rubber"], [
            # por detrás de las bisagras (y <= 1,274) y del tirante de la puerta
            box((s * 0.905, 1.345, 0.74), (0.035, 0.13, 0.30), 0.004),
        ], f"Deflector de la aleta delantera {side}", edir=(s, 0.3, 0), dist=0.35))
        A(V3.part(M, f"EXT_Underhood_Apron_{sd}", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
            box((s * 0.68, 2.14, 0.985), (0.32, 0.42, 0.010), 0.002),
            line(clip, (s * 0.54, 1.98, 0.99), (s * 0.54, 2.30, 0.99), 4, axis=Z),
        ], f"Faldón {side} bajo el capó (Underhood Apron)", edir=(s * 0.4, 0, 1), dist=0.4))
        A(V3.part(M, f"EXT_Rocker_Rear_Fairing_{sd}", "EXTERIOR_PANELS", ["plastic_black"], [
            # detrás del extremo del faldón (y -1,13), por encima de las líneas de aire y las mangueras que pasan del
            # umbral a la rueda trasera (z <= 0,30) y por debajo de la aleta (z >= 0,367)
            hull([(s * 0.80, -1.13, 0.318), (s * 0.95, -1.13, 0.318), (s * 0.80, -1.20, 0.325), (s * 0.95, -1.20, 0.325),
                  (s * 0.80, -1.13, 0.365), (s * 0.95, -1.13, 0.365), (s * 0.80, -1.20, 0.365), (s * 0.95, -1.20, 0.365)]),
        ], f"Carenado trasero del faldón {side}", edir=(s, -0.3, -0.3), dist=0.4))
        A(V3.part(M, f"EXT_Rocker_Step_Reinforcement_{sd}", "EXTERIOR_PANELS", ["steel_black", "zinc"], [
            # alojados dentro del inserto extruido del umbral, entre sus nervios
            box((s * 0.87, 1.02, 0.3315), (0.08, 0.16, 0.021), 0.002),
            box((s * 0.87, -0.92, 0.3315), (0.08, 0.16, 0.021), 0.002),
            [bolt((s * 0.87, y + dy, 0.342), Z, 0.010, 1) for y in (1.02, -0.92) for dy in (-0.05, 0.0, 0.05)],
        ], f"Refuerzos {side}s del escalón del faldón (delantero y trasero; 3 pernos 10 mm a 15 N·m cada uno)",
            edir=(s, 0, -0.6), dist=0.4))

    # --- Cristal, juntas y apliques laterales ------------------------------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecha" if s > 0 else "izquierda"
        path = [(s * (S.hw_glass(y, S.z_belt(y)) + 0.002), y, S.z_belt(y) + 0.004) for y in (1.20, 1.45, 1.70, 1.86)]
        A(V3.part(M, f"GLS_Quarter_Glass_Seal_{sd}", "GLASS_AND_MIRRORS", ["rubber_seal"], [
            sweep(path, 0.012, 0.010, 0.002, 4),
        ], f"Junta del vidrio fijo delantero de cuarto {side}", edir=(s, 0.3, 0.2), dist=0.35))
        for tag, inset, es in (("Outer", 0.0, "exterior"), ("Inner", 0.045, "interior")):
            for dn, y0, y1 in (("Front", 0.12, 1.19), ("Rear", -0.90, 0.05)):
                pth = [(s * (S.hw_side(y, S.z_belt(y)) - 0.004 - inset), y, S.z_belt(y) - 0.012)
                       for y in (y0, (y0 + y1) / 2, y1)]
                A(V3.part(M, f"EXT_Waist_Seal_{tag}_{dn}_{sd}", "DOORS_AND_HATCHES", ["rubber_seal"], [
                    sweep(pth, 0.014, 0.012, 0.002, 4),
                ], f"Junta de cintura {es} de la puerta {'delantera' if dn == 'Front' else 'trasera'} {side}",
                    edir=(s, 0, 0.3), dist=0.3))
        pth = [(s * (S.hw_roof_edge(y) + 0.004), y, S.z_top(y) - 0.020) for y in (0.50, 0.15, -0.20, -0.55, -0.88)]
        A(V3.part(M, f"EXT_Trim_Cantrail_{sd}", "EXTERIOR_PANELS", ["plastic_black"], [
            sweep(pth, 0.026, 0.014, 0.003, 5),
        ], f"Moldura exterior del larguero de techo {side}", edir=(s, 0, 1), dist=0.4))
        A(V3.part(M, f"EXT_Header_Seal_{sd}", "DOORS_AND_HATCHES", ["rubber_seal"], [
            sweep([(s * (S.hw_roof_edge(y) - 0.03), y, S.z_top(y) - 0.045) for y in (1.0, 0.5, 0.0, -0.5, -0.88)],
                  0.016, 0.014, 0.003, 5),
        ], f"Junta de cabecera {side}", edir=(s, 0, 0.8), dist=0.3))
        A(V3.part(M, f"EXT_Applique_BPillar_{sd}", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
            box((s * 0.925, 0.0797, 1.10), (0.022, 0.075, 0.62), 0.003),
            bolt((s * 0.94, 0.0797, 0.72), (s, 0, 0), 0.010, 1),
        ], f"Aplique del pilar B {side} (1 perno 10 mm a 6 N·m, 2 conectores, 3 clips)",
            edir=(s, 0, 0.2), dist=0.45))
        A(V3.part(M, f"EXT_Applique_Sail_{sd}", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
            # placa inclinada a 6 mm por dentro de la piel exterior de la vela (x 0,913 a z 1,28 y 0,884 a z 1,55),
            # por fuera del «mast», de la caja y de la pared trasera de la cabina (|x| <= 0,86)
            hull([(s * x, y, z) for y in (-1.17, -0.93) for (x, z) in ((0.9066, 1.28), (0.8986, 1.28), (0.8805, 1.53),
                                                                       (0.8725, 1.53))]),
            line(clip, (s * 0.894, -1.16, 1.31), (s * 0.894, -0.94, 1.31), 6, axis=(-s, 0, 0)),
            line(clip, (s * 0.871, -1.16, 1.53), (s * 0.871, -0.94, 1.53), 6, axis=(-s, 0, 0)),
        ], f"Aplique de la vela {side} (17 clips + 1 datum + 1 clip de arnés + 1 conector)",
            edir=(s, -0.3, 0.3), dist=0.5))
        A(V3.part(M, f"EXT_Sail_Baffle_{sd}", "EXTERIOR_PANELS", ["rubber"], [
            # entre la pared trasera de la cabina (y -0,953) y el extremo delantero del «mast» (y -0,994)
            box((s * 0.82, -0.9725, 1.45), (0.02, 0.025, 0.22), 0.003),
        ], f"Deflector (baffle) de la vela {side}", edir=(s, -0.3, 0.3), dist=0.35))
        A(V3.part(M, f"EXT_Applique_CPillar_{sd}", "EXTERIOR_PANELS", ["plastic_black"], [
            box((s * 0.945, -0.915, 1.02), (0.020, 0.030, 0.58), 0.003),
        ], f"Aplique del pilar C {side}", edir=(s, -0.3, 0.2), dist=0.4))
        A(V3.part(M, f"EXT_Mirror_SkullCap_{sd}", "GLASS_AND_MIRRORS", ["plastic_black", "zinc"], [
            box((s * 1.10, 1.08, 1.388), (0.20, 0.080, 0.012), 0.003),
            [torx((s * (1.04 + 0.04 * k), 1.08, 1.394), Z, 0.006, 1) for k in range(3)],
        ], f"Carcasa superior (skull cap) del retrovisor {side}", edir=(s, 0.3, 0.6), dist=0.4))
        for door, y0, y1, yp in (("F", 0.12, 1.17, 0.19), ("R", -0.89, 0.06, -0.82)):
            nm = ("F" if door == "F" else "R")
            A(V3.part(M, f"EXT_Door_{nm}_Presenter_{sd}", "DOORS_AND_HATCHES", ["steel_black", "zinc"], [
                box((s * 0.86, yp, 1.04), (0.050, 0.10, 0.075), 0.004),
                bolt((s * 0.86, yp - 0.03, 1.082), Z, 0.008, 1), bolt((s * 0.86, yp + 0.03, 1.082), Z, 0.008, 1),
            ], f"Presentador de la puerta {'delantera' if door == 'F' else 'trasera'} {side} "
               f"(2 pernos T30 a 13 N·m, 1 conector)", edir=(s, 0, 0.2), dist=0.45))
            A(V3.part(M, f"EXT_Door_{nm}_Closeout_{sd}", "DOORS_AND_HATCHES", ["plastic_black"], [
                box((s * 0.832, (y0 + y1) / 2, 0.84), (0.006, (y1 - y0) - 0.10, 0.54), 0.002),
            ], f"Panel de cierre (closeout) de la puerta {'delantera' if door == 'F' else 'trasera'} {side}",
                edir=(s, 0, 0), dist=0.35))
            A(V3.part(M, f"EXT_Door_{nm}_Regulator_Motor_{sd}", "DOORS_AND_HATCHES", ["steel_black", "zinc"], [
                cyl((s * 0.85, (y0 + y1) / 2 - 0.05, 0.70), (s * 0.85, (y0 + y1) / 2 + 0.07, 0.70), 0.028, seg=16),
                bolt((s * 0.85, (y0 + y1) / 2 - 0.05, 0.742), Z, 0.007, 1),
            ], f"Motor Q de 48 V del elevalunas de la puerta {'delantera' if door == 'F' else 'trasera'} {side} "
               f"(3 pernos T25 a 4 N·m)", edir=(s, 0, -0.2), dist=0.4))

    # --- Powergate (frunk) y portón ------------------------------------------------------------------------
    A(V3.part(M, "EXT_Frunk_Striker", "DOORS_AND_HATCHES", ["steel_black", "zinc"], [
        box((0, 2.595, 0.935), (0.10, 0.04, 0.012), 0.002),
        cyl((-0.025, 2.595, 0.94), (-0.025, 2.595, 0.99), 0.005, seg=8),
        cyl((0.025, 2.595, 0.94), (0.025, 2.595, 0.99), 0.005, seg=8),
        cyl((-0.025, 2.595, 0.99), (0.025, 2.595, 0.99), 0.005, seg=8),
        torx((-0.04, 2.595, 0.941), Z, 0.007, 1), torx((0.04, 2.595, 0.941), Z, 0.007, 1),
    ], "Percutor del Powergate (2 pernos T40 a 15 N·m)", edir=(0, 1, 0.2), dist=0.45))
    A(V3.part(M, "EXT_Frunk_Manual_Release", "DOORS_AND_HATCHES", ["rubber", "zinc"], [
        cyl((-0.34, 2.15, 0.88), (-0.34, 2.15, 0.93), 0.012, seg=12),
        hose([(-0.34, 2.15, 0.88), (-0.30, 2.22, 0.84), (-0.20, 2.32, 0.88), (-0.05, 2.40, 0.92)], 0.003, 6, 4, 1),
    ], "Liberación manual del Powergate (cable y tirador en el frunk)", edir=(0, 0.5, 1), dist=0.35))
    hood_hw = lambda y: min(0.935, S.interp([(yy, hw) for hw, yy in S.FRONT_PLAN], y) - 0.02)
    A(V3.part(M, "EXT_Frunk_Aero_Seal", "DOORS_AND_HATCHES", ["rubber_seal"], [
        sweep([(hood_hw(y), y, S.z_top(y) - 0.024) for y in (1.99, 2.15, 2.30, 2.42, 2.52, 2.60)], 0.016, 0.014,
              0.003, 3),
    ], "Junta aerodinámica {lado} del Powergate", mirror=True, edir=(1, 0.3, 0.5), dist=0.35))
    A(V3.part(M, "EXT_Frunk_Access_Panel", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((0, 2.28, 0.80), (0.42, 0.30, 0.016), 0.003),
        line(torx, (-0.17, 2.18, 0.808), (0.17, 2.18, 0.808), 3, axis=Z, d=0.006),
        line(torx, (-0.17, 2.38, 0.808), (0.17, 2.38, 0.808), 3, axis=Z, d=0.006),
    ], "Panel de acceso del frunk (cubre la cubeta y el conjunto del frunk)", edir=(0, 0, -1), dist=0.45,
        stage=2))
    A(V3.part(M, "LGT_Frunk_Lamp", "LIGHTING", ["lamp_housing", "led_white"], [
        box((0.22, 2.08, 1.158), (0.09, 0.035, 0.014), 0.003),
        box((0.22, 2.08, 1.150), (0.07, 0.025, 0.004), 0.001, 1),
    ], "Luz del frunk", edir=(0, 0, 1), dist=0.3))
    A(V3.part(M, "EXT_Frunk_Switches", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((-0.20, 2.12, 1.15), (0.03, 0.02, 0.02), 0.002), box((0.34, 2.14, 1.15), (0.03, 0.02, 0.02), 0.002),
    ], "Interruptor de seguridad e interruptor del frunk", edir=(0, 0, 1), dist=0.3, stage=6))
    A(V3.part(M, "EXT_Frunk_Bolt_Caps_Bumpstops", "EXTERIOR_PANELS", ["rubber", "plastic_black"], [
        disc((-0.30, 2.40, 0.78), Z, 0.012, 0.006, 16, 1), disc((0.30, 2.40, 0.78), Z, 0.012, 0.006, 16, 1),
        cyl((-0.42, 2.08, 1.115), (-0.42, 2.08, 1.135), 0.009, seg=12), cyl((0.42, 2.08, 1.115), (0.42, 2.08, 1.135), 0.009, seg=12),
    ], "Tapas de los 6 pernos del frunk (2 visibles) y topes de goma del capó", edir=(0, 0, 1), dist=0.3,
        stage=6))
    A(V3.part(M, "EXT_Frunk_Underhood_Apron_Rear", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        # por delante del Super Cowl (y <= 1,957)
        box((0, 1.993, 1.10), (1.50, 0.07, 0.020), 0.003),
        line(clip, (-0.66, 1.993, 1.112), (0.66, 1.993, 1.112), 9, axis=Z),
    ], "Faldón trasero bajo el capó (9 clips)", edir=(0, 0.3, 1), dist=0.4))
    A(V3.part(M, "EXT_Tailgate_Inner_Cover", "DOORS_AND_HATCHES", ["plastic_black", "zinc"], [
        box((0, -2.812, 1.05), (1.56, 0.008, 0.55), 0.002),
        line(clip, (-0.66, -2.805, 0.80), (0.66, -2.805, 0.80), 8, axis=(0, 1, 0)),
        line(clip, (-0.66, -2.805, 1.30), (0.66, -2.805, 1.30), 8, axis=(0, 1, 0)),
    ], "Cubierta interior del portón", edir=(0, 1, 0.2), dist=0.45, stage=2))
    A(V3.part(M, "EXT_Tailgate_Manual_Release_Cap", "DOORS_AND_HATCHES", ["rubber"], [
        disc((0.50, -2.808, 0.90), Y, 0.014, 0.006, 16, 0),
        hose([(0.50, -2.80, 0.90), (0.62, -2.80, 0.84), (0.80, -2.80, 0.80)], 0.0025, 6, 3, 0),
    ], "Tapa y cable de liberación manual del portón", edir=(0, 1, 0), dist=0.3, stage=6))
    A(V3.part(M, "EXT_Tailgate_Bumpstops", "DOORS_AND_HATCHES", ["rubber"], [
        cyl((0.55, -2.80, 0.76), (0.55, -2.84, 0.76), 0.010, seg=12), cyl((-0.55, -2.80, 0.76), (-0.55, -2.84, 0.76), 0.010, seg=12),
    ], "Topes del portón", edir=(0, -1, 0), dist=0.3, stage=6))
    A(V3.part(M, "EXT_Tailgate_Seal_Side", "DOORS_AND_HATCHES", ["rubber_seal"], [
        sweep([(0.86, -2.80, 0.78), (0.87, -2.80, 1.00), (0.88, -2.80, 1.26)], 0.012, 0.012, 0.002, 4),
    ], "Junta lateral {lado} del portón", mirror=True, edir=(1, -0.5, 0.2), dist=0.3))
    A(V3.part(M, "EXT_Trailer_Hitch_Cover", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((0, -2.964, 0.44), (0.12, 0.012, 0.10), 0.003),
        cyl((-0.04, -2.970, 0.44), (-0.04, -2.9725, 0.44), 0.012, seg=12, m=1), cyl((0.04, -2.970, 0.44), (0.04, -2.9725, 0.44), 0.012, seg=12, m=1),
    ], "Tapa del enganche (cierres de cuarto de vuelta, 4 pestañas)", edir=(0, -1, 0), dist=0.45))
    A(V3.part(M, "LGT_Reflector_Rear", "LIGHTING", ["glass_lens_red"], [
        box((0.80, -2.982, 0.65), (0.09, 0.006, 0.04), 0.002),
    ], "Catadióptrico trasero {lado}", mirror=True, edir=(0.4, -1, 0), dist=0.3))

    # --- Caja de carga y cubierta tonneau -----------------------------------------------------------------
    A(V3.part(M, "CARGO_Bed_Side_Wall_Lower", "CARGO_BED", ["composite", "zinc"], [
        box((0.835, -1.92, 1.02), (0.014, 1.84, 0.30), 0.003),
        line(bolt, (0.82, -2.70, 0.95), (0.82, -1.20, 0.95), 6, axis=(-1, 0, 0), d=0.010),
    ], "Pared lateral inferior {lado} de la caja (1 perno 15 mm 46 N·m, 4 pernos 10 mm 11 N·m…)", mirror=True,
        edir=(0.6, 0, 0), dist=0.45))
    A(V3.part(M, "CARGO_Bed_Side_Wall_Upper", "CARGO_BED", ["composite", "zinc"], [
        box((0.835, -1.92, 1.26), (0.014, 1.84, 0.12), 0.003),
        line(clip, (0.82, -2.70, 1.26), (0.82, -1.20, 1.26), 8, axis=(-1, 0, 0)),
    ], "Pared lateral superior {lado} de la caja (8 clips)", mirror=True, edir=(0.6, 0, 0.3), dist=0.45))
    A(V3.part(M, "CARGO_Bed_Front_Wall", "CARGO_BED", ["composite"], [
        box((0, -1.012, 1.10), (1.64, 0.030, 0.42), 0.004),
    ], "Pared delantera de la caja (Front Wall Assembly Truck Bed)", edir=(0, 1, 0.2), dist=0.5))
    A(V3.part(M, "CARGO_Bed_False_Wall", "CARGO_BED", ["composite", "zinc"], [
        box((0, -1.05, 1.07), (1.60, 0.025, 0.36), 0.004),
        bolt((-0.30, -1.065, 1.07), (0, -1, 0), 0.015, 1), bolt((0.30, -1.065, 1.07), (0, -1, 0), 0.015, 1),
        nut((-0.55, -1.065, 1.07), (0, -1, 0), 0.013, 1), nut((0.55, -1.065, 1.07), (0, -1, 0), 0.013, 1),
    ], "Pared falsa de la caja (2 pernos 15 mm a 45 N·m + 4 tuercas 13 mm a 30 N·m)", edir=(0, 1, 0), dist=0.5))
    A(V3.part(M, "CARGO_Bed_XMember", "CARGO_BED", ["steel_black", "zinc"], [
        beam((-0.80, -1.90, 0.835), (0.80, -1.90, 0.835), 0.07, 0.035, 0.003),
        beam((-0.80, -2.40, 0.835), (0.80, -2.40, 0.835), 0.06, 0.035, 0.003),
        line(bolt, (-0.60, -2.40, 0.8525), (0.60, -2.40, 0.8525), 2, axis=Z, d=0.010),
    ], "Travesaño en X y travesaño inferior de la cubeta (2 pernos 13 mm a 36 N·m)", edir=(0, 0, -1), dist=0.45,
        stage=3))
    A(V3.part(M, "CARGO_Bed_Closeout_Rear", "CARGO_BED", ["plastic_black", "zinc"], [
        box((0.83, -2.855, 1.05), (0.040, 0.040, 0.50), 0.003),
        line(clip, (0.81, -2.855, 0.85), (0.81, -2.855, 1.25), 4, axis=(-1, 0, 0)),
    ], "Cierre trasero {lado} de la caja (Bed Closeout Rear)", mirror=True, edir=(0.6, -0.4, 0), dist=0.4))
    A(V3.part(M, "CARGO_Bed_Cargo_Tub_Lid", "CARGO_BED", ["composite", "rubber_seal"], [
        box((0, -2.52, 0.872), (0.88, 0.58, 0.012), 0.003),
        sweep([(-0.44, -2.81, 0.882), (0.44, -2.81, 0.882), (0.44, -2.23, 0.882), (-0.44, -2.23, 0.882),
               (-0.44, -2.81, 0.882)], 0.010, 0.006, 0.0, 1, m=1),
        cyl((0.40, -2.30, 0.80), (0.36, -2.40, 0.90), 0.008, seg=10),
    ], "Tapa, junta y amortiguador del compartimento bajo la caja (97 L, límite 220 lb)", edir=(0, 0, 1), dist=0.5))
    A(V3.part(M, "CARGO_Bed_Outlet_Door", "CARGO_BED", ["plastic_black", "zinc"], [
        box((-0.822, -1.325, 1.065), (0.012, 0.22, 0.095), 0.003),
        torx((-0.826, -1.40, 1.07), (-1, 0, 0), 0.005, 1), torx((-0.826, -1.25, 1.07), (-1, 0, 0), 0.005, 1),
    ], "Tapa (puerta) del módulo de tomas de la caja (2 tornillos T25R a 1,5 N·m + 1 perno a 10 N·m)",
        edir=(-1, 0, 0.2), dist=0.4))
    A(V3.part(M, "CARGO_Tonneau_Cam_Block", "CARGO_BED", ["steel_black", "zinc"], [
        # bajo el aplique del pivote y el soporte de la vela (z >= 1,375) y bajo las dos últimas lamas
        box((0.775, -1.05, 1.353), (0.040, 0.050, 0.040), 0.003), box((0.775, -2.78, 1.331), (0.040, 0.050, 0.040), 0.003),
    ], "Bloques de leva {lado}s de la cubierta (Cam Block)", mirror=True, edir=(0.6, 0, 0.4), dist=0.35))
    A(V3.part(M, "CARGO_Tonneau_Hinge_Pivot_Applique", "CARGO_BED", ["plastic_black"], [
        box((0.80, -1.02, 1.40), (0.030, 0.060, 0.050), 0.003),
    ], "Aplique del pivote {lado} de la cubierta", mirror=True, edir=(0.6, 0, 0.4), dist=0.35))
    A(V3.part(M, "CARGO_Tonneau_Deflector_Clip", "CARGO_BED", ["plastic_black"], [
        line(clip, (0.74, -1.40, 1.33), (0.74, -2.50, 1.33), 5, axis=Z, d=0.010, m=0),
    ], "Clips {lado}s del deflector de la cubierta", mirror=True, edir=(0.4, 0, 0.8), dist=0.3, stage=6))
    A(V3.part(M, "CARGO_Tonneau_NVH_Barrier", "CARGO_BED", ["rubber", "zinc"], [
        box((0, -1.075, 1.27), (1.50, 0.020, 0.16), 0.003),
        line(bolt, (-0.66, -1.087, 1.27), (0.66, -1.087, 1.27), 10, axis=(0, -1, 0), d=0.008),
    ], "Barrera NVH del casete (10 pernos de 8 mm a 5 N·m)", edir=(0, 1, 0.2), dist=0.4))
    A(V3.part(M, "CARGO_Tonneau_Water_Seal_Center", "CARGO_BED", ["rubber_seal", "plastic_black"], [
        # empieza detrás de la caja del motor de la cubierta (y >= -1,18)
        sweep([(0.70, -1.185, 1.36), (0.70, -1.80, 1.34), (0.70, -2.45, 1.32)], 0.012, 0.010, 0.002, 4),
        clip((0.70, -1.80, 1.345), Z, 0.010, 1),
    ], "Junta {lado} de gestión de agua del tonneau (1 clip)", mirror=True, edir=(0.4, 0, 0.6), dist=0.3))
    A(V3.part(M, "CARGO_Tonneau_Closeout_Foam", "CARGO_BED", ["rubber"], [
        box((0, -1.08, 1.39), (1.20, 0.060, 0.012), 0.002), box((0, -2.84, 1.35), (1.50, 0.020, 0.030), 0.002),
    ], "Junta de cierre y almohadilla de espuma de referencia (datum) de la cubierta", edir=(0, 0.4, 1), dist=0.3,
        stage=6))
    A(V3.part(M, "CARGO_Tonneau_Manual_Release", "CARGO_BED", ["rubber", "zinc"], [
        cyl((0.10, -1.045, 1.30), (0.10, -1.045, 1.34), 0.010, seg=12),
        hose([(0.10, -1.045, 1.30), (0.30, -1.055, 1.28), (0.62, -1.055, 1.31)], 0.003, 6, 4, 1),
    ], "Liberación manual de las lamas del tonneau", edir=(0, 0.3, 1), dist=0.3, stage=6))

    # --- Clips y revestimientos de pasos de rueda -----------------------------------------------------
    for tag, cy in (("F", 1.8175), ("R", -1.8175)):
        for s, sd in ((1, "R"), (-1, "L")):
            pts = []
            n = 14 if tag == "F" else 19
            for i in range(n):
                a = math.radians(15 + 150 * i / (n - 1))
                pts.append((s * 0.545, cy + 0.50 * math.cos(a), 0.437 + 0.50 * math.sin(a)))
            A(V3.part(M, f"BODY_WheelLiner_Clips_{tag}{sd}", "BODY_FASTENERS", ["plastic_black"], [
                [clip(p, (s, 0, 0), 0.012, 0) for p in pts],
            ], f"Clips a presión del pasarruedas {'delantero' if tag == 'F' else 'trasero'} {'derecho' if s > 0 else 'izquierdo'} "
               f"({n} clips)", edir=(s, 0, 0.3), dist=0.3, stage=6))
    A(V3.part(M, "BODY_Mudflap_Fasteners", "BODY_FASTENERS", ["zinc"], [
        line(bolt, (0.90, 1.21, 0.38), (0.93, 1.21, 0.36), 2, axis=Y, d=0.010),
        line(bolt, (-0.90, 1.21, 0.38), (-0.93, 1.21, 0.36), 2, axis=Y, d=0.010),
        line(bolt, (0.90, -2.27, 0.38), (0.93, -2.27, 0.36), 4, axis=(0, -1, 0), d=0.010),
        line(bolt, (-0.90, -2.27, 0.38), (-0.93, -2.27, 0.36), 4, axis=(0, -1, 0), d=0.010),
    ], "Pernos profundos de las faldillas (delanteras 2 × 1,8 N·m; traseras 4 × 2,2 N·m)", edir=(0, 0, -1),
        dist=0.3, stage=6))
    return [o for o in out if o is not None]
