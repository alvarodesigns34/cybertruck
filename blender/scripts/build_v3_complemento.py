"""Versión 3 · complemento: piezas menores del backlog que quedaban fuera de los módulos por sistema.

Fuentes: docs/ficha-tecnica-piezas.md (EXT-006, EXT-008, EXT-018, EXT-032, EXT-041, EXT-051, EXT-108, EXT-116,
EST-042, EST-043/044, EST-050, TRN-025, TRN-034, TRN-049, INT-037, INT-042, INT-056, INT-087).
Existencia, denominación y fijaciones son «Verificado» en el manual de servicio; forma y posición, reconstruidas.
"""

from mathutils import Vector
import ct_specs as S
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, rivet

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend

    # --- Frontal: juntas de espuma y cubierta de cámara ---------------------------------------------------------
    A(V3.part(M, "EXT_Grille_Foam_Seals", "EXTERIOR_PANELS", ["rubber"], [
        box((0, 2.60, 0.632), (1.00, 0.020, 0.014), 0.002), box((0, 2.60, 0.518), (1.00, 0.020, 0.014), 0.002),
        box((0.52, 2.60, 0.575), (0.014, 0.020, 0.100), 0.002), box((-0.52, 2.60, 0.575), (0.014, 0.020, 0.100), 0.002),
    ], "Juntas de espuma superior, inferior y laterales de la rejilla delantera", edir=(0, 1, 0), dist=0.4,
        stage=6))
    A(V3.part(M, "EXT_Camera_Cover_Lower_Fascia", "EXTERIOR_PANELS", ["plastic_black", "zinc"], [
        box((0, 2.680, 0.585), (0.072, 0.006, 0.062), 0.002),
        torx((-0.030, 2.684, 0.585), Y, 0.005, 1), torx((0.030, 2.684, 0.585), Y, 0.005, 1),
    ], "Cubierta de la cámara de la fascia inferior (2 tornillos PH1 a 2 N·m)", edir=(0, 1, 0), dist=0.35, stage=6))
    # --- Trasera y caja: soportes -----------------------------------------------------------------------------------
    A(V3.part(M, "EXT_Rear_Fascia_Step_Bracket", "EXTERIOR_PANELS", ["steel_black", "zinc"], [
        box((0.30, -2.88, 0.56), (0.10, 0.060, 0.10), 0.003),
        line(bolt, (0.27, -2.915, 0.56), (0.33, -2.915, 0.56), 2, axis=(0, -1, 0), d=0.013),
    ], "Soporte {lado} del escalón de la fascia trasera (2 pernos 13 mm a 16 N·m del enganche)", mirror=True,
        edir=(0.2, -1, 0), dist=0.4))
    A(V3.part(M, "EXT_Rear_Absorber_Fascia_Bracket_Center", "EXTERIOR_PANELS", ["steel_black", "zinc"], [
        box((0, -2.88, 0.54), (0.20, 0.05, 0.08), 0.003),
        line(bolt, (-0.06, -2.907, 0.54), (0.06, -2.907, 0.54), 2, axis=(0, -1, 0), d=0.013),
    ], "Soporte central del escalón del absorbedor trasero", edir=(0, -1, 0), dist=0.4))
    A(V3.part(M, "EXT_Bed_Side_Corner_Brackets", "EXTERIOR_PANELS", ["steel_black", "zinc"], [
        box((0.83, -2.84, 1.20), (0.060, 0.060, 0.060), 0.003), box((0.84, -2.82, 1.28), (0.050, 0.050, 0.040), 0.003),
        torx((0.80, -2.84, 1.20), (-1, 0, 0), 0.006, 1),
    ], "Soportes {lado}s del aplique de la esquina de la caja y del escalón del piloto", mirror=True,
        edir=(0.6, -0.4, 0.2), dist=0.4, stage=6))
    A(V3.part(M, "EXT_Dash_Absorber", "EXTERIOR_PANELS", ["rubber"], [
        box((0.50, 1.80, 1.12), (0.30, 0.060, 0.060), 0.004),
    ], "Absorbedor {lado} del salpicadero (Dash Absorber)", mirror=True, edir=(0.3, 0.5, 0.6), dist=0.4, stage=6))
    A(V3.part(M, "CARGO_Tonneau_Corner_Bracket", "CARGO_BED", ["steel_black", "zinc"], [
        box((0.78, -2.84, 1.335), (0.050, 0.050, 0.040), 0.003), bolt((0.78, -2.84, 1.357), Z, 0.010, 1),
    ], "Soporte de esquina {lado} de la cubierta (1 perno a 9 N·m)", mirror=True, edir=(0.5, -0.5, 0.5), dist=0.35,
        stage=6))
    # --- Puertas: placas de espárragos de las bisagras y junta guía de la luna ------------------------------------
    for s, sd in ((1, "R"), (-1, "L")):
        side = "derecho" if s > 0 else "izquierdo"
        A(V3.part(M, f"EXT_Door_Hinge_Stud_Plates_{sd}", "DOORS_AND_HATCHES", ["steel_black", "zinc"], [
            [box((s * 0.84, y, z), (0.020, 0.14, 0.070), 0.003) for (y, z) in
             ((1.195, 0.62), (1.195, 1.02), (-0.885, 0.62), (-0.885, 1.02))],
            [cyl((s * 0.85, y + dy, z), (s * 0.868, y + dy, z), 0.005, seg=8, m=1) for (y, z) in
             ((1.195, 0.62), (1.195, 1.02), (-0.885, 0.62), (-0.885, 1.02)) for dy in (-0.04, 0.04)],
        ], f"Placas de espárragos de las bisagras de puerta, lado {side} (4 por lado)", edir=(s, 0, 0), dist=0.4,
            stage=6))
        A(V3.part(M, f"EXT_Glass_Run_Seal_APillar_{sd}", "DOORS_AND_HATCHES", ["rubber_seal"], [
            sweep([(s * (S.hw_glass(1.78, 1.24) - 0.01), 1.78, 1.24), (s * (S.hw_glass(1.2, 1.50) - 0.01), 1.2, 1.50),
                   (s * (S.hw_roof_edge(0.6) - 0.01), 0.6, S.z_top(0.6) - 0.04)], 0.014, 0.012, 0.002, 4),
        ], f"Guía de cristal del pilar A {side} (Glass Run Seal Front Door)", edir=(s, 0.3, 0.4), dist=0.3))
        A(V3.part(M, f"LGT_Side_Repeater_{sd}", "LIGHTING", ["led_amber", "lamp_housing"], [
            box((s * 1.0365, 1.46, 0.86), (0.006, 0.040, 0.012), 0.0008),
            box((s * 1.034, 1.46, 0.86), (0.004, 0.046, 0.018), 0.0008, 1),
        ], f"Repetidor lateral {side} (integrado junto a la cámara de la aleta)", edir=(s, 0.2, 0), dist=0.3,
            stage=6))
    # --- Lavado ----------------------------------------------------------------------------------------------------
    A(V3.part(M, "EXT_Washer_Pump_Hoses", "GLASS_AND_MIRRORS", ["plastic_black", "hose", "zinc"], [
        # bomba en la cara delantera del depósito; mangueras por delante y por encima de él
        cyl((0.62, 2.38, 0.70), (0.62, 2.43, 0.70), 0.020, seg=16, m=0),
        hose([(0.62, 2.43, 0.72), (0.62, 2.42, 0.92), (0.55, 2.20, 0.95), (0.10, 1.84, 1.06), (0.0, 1.90, 1.22)],
             0.0035, 6, 5, 1),
        hose([(0.62, 2.43, 0.69), (0.40, 2.52, 0.685), (0.20, 2.58, 0.68)], 0.0030, 6, 5, 1),
        hose([(0.61, 2.43, 0.74), (0.60, 2.41, 0.93), (0.58, 2.10, 0.97), (0.30, 1.84, 1.10), (0.22, 1.92, 1.30)],
             0.0030, 6, 5, 1),
        clip((0.55, 2.20, 0.97), Z, 0.010, 2),
    ], "Bomba del lavaparabrisas y mangueras (Megabeam, limpiaparabrisas y boquilla de la cámara; 2 clips)",
        edir=(0.4, 0.5, 0.4), dist=0.4, stage=6))
    # --- Estructura -------------------------------------------------------------------------------------------------
    A(V3.part(M, "BODY_Rear_Rail_Backing_Plate", "BODY_STRUCTURE", ["alu_cast", "zinc"], [
        box((0.525, -2.62, 0.60), (0.10, 0.30, 0.012), 0.002),
        line(rivet, (0.525, -2.75, 0.608), (0.525, -2.49, 0.608), 8, axis=Z, d=0.0065),
    ], "Placa trasera {lado} del larguero trasero fundido (15 remaches de brida de 6,5 mm)", mirror=True,
        edir=(0.4, -0.4, -0.6), dist=0.45, stage=3))
    pl = []
    for y in (-1.30, -1.75, -2.15, -2.55):
        z = S.z_top(y) - 0.115
        pl.append(box((S.hw_side(y, z) - 0.062, y, z), (0.006, 0.12, 0.075), 0.002))
    A(V3.part(M, "BODY_Mast_Backing_Plates", "BODY_STRUCTURE", ["alu_cast", "zinc"], [pl],
              "Placas de refuerzo {lado}s del «mast» (superior, superior-media, inferior-media e inferior)",
              mirror=True, edir=(0.5, 0, 0.5), dist=0.4, stage=3))
    A(V3.part(M, "BODY_Rear_Energy_Absorber_Center_Bracket", "BODY_STRUCTURE", ["alu_cast", "zinc"], [
        box((0, -2.88, 0.60), (0.30, 0.050, 0.12), 0.004),
        line(bolt, (-0.10, -2.905, 0.60), (0.10, -2.905, 0.60), 3, axis=(0, -1, 0), d=0.018),
    ], "Soporte central del absorbedor trasero (2 pernos 18 mm a 90 N·m por lado)", edir=(0, -1, 0), dist=0.5,
        stage=3))
    # --- Tren motriz / térmica / alta tensión -----------------------------------------------------------------
    A(V3.part(M, "THM_Pack_Pressurization_Line", "UNDERBODY", ["hose", "valve_brass"], [
        # por detrás del compresor de la suspensión y por debajo de él
        hose([(-0.30, -2.355, 0.50), (-0.30, -2.37, 0.38), (-0.34, -1.95, 0.36), (-0.30, -1.50, 0.38)], 0.006, 8, 5, 0),
        [cyl(p, (p[0], p[1], p[2] + 0.02), 0.009, seg=10, m=1) for p in ((-0.30, -2.355, 0.50), (-0.30, -1.50, 0.38))],
    ], "Línea de presurización del pack (Wade/Scuba; 2 racores VOSS 12 mm a 8 N·m)", edir=(0, -0.3, -0.8),
        dist=0.4, stage=6))
    A(V3.part(M, "HV_ACJB_Harnesses", "BATTERY_ASSEMBLY", ["hv_orange", "connector_grey"], [
        # por encima de las cajas: los conectores se apoyan en las tapas de la ACJB, la PCS y el clúster
        hose([(-0.31, -1.20, 0.6865), (-0.05, -1.17, 0.735), (0.20, -1.20, 0.714)], 0.012, 12, 5, 0),
        hose([(-0.30, -1.30, 0.683), (-0.15, -1.33, 0.69), (-0.03, -1.30, 0.678)], 0.010, 12, 5, 0),
        box((-0.31, -1.20, 0.6865), (0.04, 0.04, 0.03), 0.003, 1), box((0.20, -1.20, 0.714), (0.04, 0.04, 0.03), 0.003, 1),
    ], "Arneses HV de la caja de CA (ACJB) a la PCS y al cabezal de carga rápida", edir=(0, -0.2, 1), dist=0.4,
        stage=5))
    A(V3.part(M, "THM_Supermanifold_Controller_Sensors", "UNDERBODY", ["plastic_black", "valve_brass", "connector_grey"], [
        box((0.42, 1.82, 1.045), (0.060, 0.040, 0.030), 0.003),
        box((0.455, 1.82, 1.045), (0.012, 0.020, 0.016), 0.002, 2),
        cyl((0.30, 1.74, 1.02), (0.30, 1.74, 1.05), 0.008, seg=10, m=1), cyl((0.35, 1.74, 1.02), (0.35, 1.74, 1.05), 0.008, seg=10, m=1),
        cyl((0.50, 1.80, 0.86), (0.50, 1.80, 0.94), 0.020, seg=14, m=0),
    ], "Controlador y sensores de presión del Supermanifold, válvulas antirretorno y botella desecante",
        edir=(0.4, 0.2, 1), dist=0.4, stage=6))
    # --- Interior ----------------------------------------------------------------------------------------------------
    A(V3.part(M, "INT_Gear_Selector_Buttons", "INTERIOR_TRIM", ["plastic_black", "led_white"], [
        [box((-0.075 + 0.05 * k, 0.62, 1.646), (0.036, 0.040, 0.006), 0.002) for k in range(4)],
        [box((-0.075 + 0.05 * k, 0.62, 1.643), (0.020, 0.012, 0.002), 0.0005, 1) for k in range(4)],
    ], "Botones P-R-N-D del selector de marcha en la consola del techo (sin palanca)", edir=(0, 0, -1), dist=0.3,
        stage=6))
    A(V3.part(M, "INT_Console_Airwave_Rear", "INTERIOR_CONTROLS", ["int_plastic", "plastic_black"], [
        box((0.0, -0.165, 0.775), (0.26, 0.030, 0.035), 0.003),
        [box((x, -0.182, 0.775), (0.006, 0.004, 0.022), 0.0008, 1) for x in (-0.09, -0.045, 0.0, 0.045, 0.09)],
    ], "Conjunto «Airwave» trasero de la consola y su tapa", edir=(0, -1, 0.4), dist=0.35, stage=6))
    A(V3.part(M, "INT_SeatR_Release_Straps", "INTERIOR_SEATS", ["seatbelt", "plastic_black"], [
        box((0.22, -0.80, 0.715), (0.030, 0.006, 0.060), 0.001), box((-0.22, -0.80, 0.715), (0.030, 0.006, 0.060), 0.001),
        box((0.22, -0.80, 0.680), (0.040, 0.012, 0.014), 0.002, 1), box((-0.22, -0.80, 0.680), (0.040, 0.012, 0.014), 0.002, 1),
    ], "Correas de liberación de las hebillas del asiento trasero", edir=(0, -0.3, 0.6), dist=0.3, stage=6))
    A(V3.part(M, "INT_Windshield_Shades", "INTERIOR_TRIM", ["headliner"], [
        box((0.38, -0.15, 1.655), (0.74, 1.30, 0.004), 0.001), box((-0.38, -0.15, 1.655), (0.74, 1.30, 0.004), 0.001),
    ], "Cortinillas del techo de cristal fijo (par)", edir=(0, 0, 1), dist=0.45, stage=2))
    return [o for o in out if o is not None]
