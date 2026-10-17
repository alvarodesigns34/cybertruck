"""Versión 3 · electrónica de 48 V, cámaras, antenas, conectividad y mazos.

Fuentes (docs/ficha-tecnica-piezas.md §3.6; manual de servicio «SM», manual del propietario «OM»):
  [V] Denominación, cantidad y fijaciones (ELE-xxx). Las posiciones de las antenas y de las tomas de 48 V no
      constan en los manuales: se marcan «Aproximado».
  [R] Forma y recorrido de los mazos: reconstruidos sin planos; no hay longitudes ni masas publicadas.
"""

from mathutils import Vector
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip, ball

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend
    B, T, FA = "BATTERY_ASSEMBLY", "INTERIOR_TRIM", "BODY_FASTENERS"

    # --- Controladores y 48 V -------------------------------------------------------------------------------------
    A(V3.part(M, "LV_MV_Locking_Covers", B, ["plastic_black", "zinc", "connector_blue"], [
        box((-0.62, 1.30, 0.895), (0.10, 0.060, 0.016), 0.003), box((0.62, 1.30, 0.895), (0.10, 0.060, 0.016), 0.003),
        box((0.0, -1.025, 1.035), (0.10, 0.060, 0.016), 0.003),
        [bolt((x, y, z), Z, 0.008, 1) for (x, y, z) in ((-0.65, 1.30, 0.905), (0.65, 1.30, 0.905), (0.03, -1.025, 1.045))],
        [box((x, y, z), (0.020, 0.008, 0.012), 0.001, 2) for (x, y, z) in ((-0.58, 1.34, 0.88), (0.58, 1.34, 0.88), (-0.04, -1.06, 1.03))],
    ], "Cubiertas cautivas de bloqueo MV de los controladores de carrocería (8 mm a 6 N·m) y conectores azules de 48 V",
        edir=(0, 0, 1), dist=0.35, stage=6))
    A(V3.part(M, "LV_Trailer_ECU", B, ["plastic_black", "zinc", "connector_grey"], [
        box((0.34, -2.85, 0.64), (0.10, 0.045, 0.07), 0.004),
        line(nut, (0.30, -2.85, 0.68), (0.38, -2.85, 0.68), 2, axis=Z, d=0.012, stud=0.0),
        box((0.34, -2.89, 0.65), (0.035, 0.012, 0.030), 0.002, 2),
    ], "ECU de remolque tras la fascia trasera (2 tuercas 10 mm a 9 N·m, conector con palanca)", edir=(0, -1, 0),
        dist=0.45, stage=5))
    A(V3.part(M, "LV_MV_Maintainer", B, ["plastic_black", "connector_blue", "zinc"], [
        box((0.52, 1.93, 0.80), (0.10, 0.07, 0.06), 0.004),
        box((0.57, 1.975, 0.80), (0.030, 0.012, 0.030), 0.002, 1),
        bolt((0.49, 1.93, 0.835), Z, 0.008, 2),
    ], "Mantenedor de media tensión (MV) de 48 V", edir=(0.5, 0.3, 0.6), dist=0.4, stage=5))
    A(V3.part(M, "LV_MV_Jump_Post", B, ["plastic_black", "copper"], [
        cyl((-0.40, 1.96, 0.97), (-0.40, 1.96, 1.01), 0.010, seg=12, m=1), cyl((-0.40, 1.96, 1.01), (-0.40, 1.96, 1.04), 0.014, seg=14, m=0),
    ], "Poste de arranque (jump post) del frunk entre el depósito de frenos y el frunk", edir=(0, 0.2, 1), dist=0.35,
        stage=6))
    A(V3.part(M, "LV_Backbone_Clips", B, ["plastic_black", "harness"], [
        line(clip, (0.78, 0.95, 0.50), (0.78, -0.95, 0.50), 6, axis=Z, d=0.012, m=0),
        line(clip, (0.70, 1.15, 0.50), (0.62, 1.30, 0.80), 3, axis=Z, d=0.012, m=0),
        [box((0.78, y, 0.502), (0.040, 0.050, 0.003), 0.001, 1) for y in (0.60, 0.0, -0.60)],
    ], "Clips y cintas de abrasión del mazo troncal de 48 V (6 traseros + 3 delanteros; PN 1879451-99-A, 1908543-99-A)",
        edir=(0, 0, -1), dist=0.3, stage=6))
    for nm, es, pts, r, m in (
            ("Fascia", "de la fascia delantera", [(0.30, 2.60, 0.62), (0.35, 2.30, 0.70), (0.45, 1.90, 0.95)], 0.007, "harness"),
            ("Seat_L", "del asiento izquierdo", [(-0.40, 0.50, 0.54), (-0.30, 0.90, 0.52), (-0.58, 1.26, 0.74)], 0.006, "harness"),
            ("Seat_R", "del asiento derecho", [(0.40, 0.50, 0.54), (0.30, 0.90, 0.52), (0.58, 1.26, 0.74)], 0.006, "harness"),
            ("Rear_Subframe", "del subchasis trasero (Tri Motor)", [(-0.30, -1.50, 0.40), (0.0, -2.00, 0.34), (0.30, -1.55, 0.40)], 0.008, "harness"),
            ("Cowl_Speaker", "del altavoz del cowl", [(-0.50, 1.90, 1.22), (0.0, 1.88, 1.20), (0.50, 1.90, 1.22)], 0.004, "harness"),
            ("Ancillary", "de la bahía auxiliar", [(-0.40, -1.20, 0.62), (0.0, -1.15, 0.72), (0.40, -1.20, 0.64)], 0.007, "harness"),
            ("Shunt_Jumper", "puente de derivación (shunt) del pack", [(0.10, -1.32, 0.63), (0.20, -1.25, 0.70), (0.35, -1.30, 0.66)], 0.006, "hv_orange")):
        A(V3.part(M, f"LV_Harness_{nm}", B, [m, "connector_grey"], [
            hose(pts, r, 8, 5, 0), box(pts[0], (0.020, 0.016, 0.014), 0.002, 1), box(pts[-1], (0.020, 0.016, 0.014), 0.002, 1),
        ], f"Mazo {es}", edir=(0, 0, 1), dist=0.3, stage=6, fid="A",
            note="Recorrido reconstruido: los manuales no publican longitudes ni trazado"))
    A(V3.part(M, "LV_Ferrite_Core_Coax", B, ["plastic_black", "hose", "connector_blue"], [
        cyl((0.0, -1.36, 0.72), (0.0, -1.30, 0.72), 0.018, seg=14, m=0),
        hose([(0.0, 2.60, 0.58), (0.10, 2.10, 0.80), (0.30, 1.50, 1.00)], 0.0025, 6, 5, 1),
        hose([(0.0, 0.62, 1.70), (0.20, 0.90, 1.30), (0.40, 1.30, 1.00)], 0.0025, 6, 5, 1),
    ], "Núcleo de ferrita del clúster de dispositivos y cables coaxiales (cámara de fascia, antena GPS)",
        edir=(0, 0, 1), dist=0.3, stage=6))

    # --- Cámaras y sensores ---------------------------------------------------------------------------------------
    A(V3.part(M, "CAM_Rear", "LIGHTING", ["plastic_black", "glass_lens", "zinc"], [
        box((0.0, -2.915, 1.255), (0.045, 0.030, 0.040), 0.004),
        cyl((0.0, -2.93, 1.255), (0.0, -2.9385, 1.255), 0.008, seg=12, m=1),
        torx((-0.02, -2.90, 1.28), Y, 0.004, 2), torx((0.02, -2.90, 1.28), Y, 0.004, 2),
    ], "Cámara trasera del portón (HW4; soporte y cámara con 2 tornillos T10 a 0,7 N·m)", edir=(0, -1, 0.3),
        dist=0.4, stage=6))
    A(V3.part(M, "CAM_Windshield_Fan", FA, ["plastic_black", "rubber", "zinc"], [
        cyl((0.14, 0.70, 1.655), (0.14, 0.70, 1.672), 0.016, seg=16, m=0),
        [torx((0.14 + dx, 0.70 + dy, 1.673), Z, 0.003, 2) for dx, dy in ((0.012, 0.0), (-0.006, 0.010), (-0.006, -0.010))],
        [cyl((0.14 + dx, 0.70 + dy, 1.650), (0.14 + dx, 0.70 + dy, 1.656), 0.003, seg=8, m=1) for dx, dy in ((0.012, 0.0), (-0.006, 0.010), (-0.006, -0.010))],
    ], "Ventilador de la cámara del parabrisas (3 tornillos T6 a 0,12 N·m, 3 calzos antirruido)", edir=(0, 0, -1),
        dist=0.3, stage=6))
    A(V3.part(M, "EXT_Windshield_Glare_Shield", FA, ["plastic_black", "rubber"], [
        box((0.0, 0.64, 1.690), (0.34, 0.060, 0.012), 0.003),
        box((0.0, 0.575, 1.700), (1.30, 0.012, 0.008), 0.002, 1),
        line(clip, (-0.10, 0.64, 1.685), (0.10, 0.64, 1.685), 2, axis=(0, 0, -1), d=0.010, m=0),
    ], "Visera antideslumbrante del parabrisas (2 clips) y tira separadora de goma", edir=(0, 0, -1), dist=0.3,
        stage=6))
    A(V3.part(M, "ELE_Antennas", FA, ["plastic_black", "zinc"], [
        box((0.0, 0.625, 1.680), (0.050, 0.030, 0.012), 0.002), torx((0.0, 0.625, 1.687), Z, 0.004, 1),
        box((0.55, 0.60, 1.695), (0.040, 0.012, 0.004), 0.001), box((0.30, -0.82, 1.645), (0.060, 0.040, 0.012), 0.003),
        box((-0.30, -0.82, 1.645), (0.060, 0.040, 0.012), 0.003),
    ], "Antenas: GPS (en el glare shield, 1 tornillo T10 a 0,8 N·m), AM/FM/HD, Wi-Fi y radio por satélite",
        edir=(0, 0, 1), dist=0.3, stage=6, fid="A",
        note="Nombres y existencia en el manual de servicio; cantidad y posición exactas no publicadas"))
    A(V3.part(M, "ELE_FM_HD_Tuner", FA, ["plastic_black", "connector_grey"], [
        box((0.50, 0.60, 1.685), (0.070, 0.040, 0.020), 0.003), box((0.50, 0.58, 1.685), (0.016, 0.006, 0.010), 0.001, 1),
    ], "Sintonizador FM/HD y amplificador de antena FM", edir=(0, 0, 1), dist=0.3, stage=6, fid="A"))
    A(V3.part(M, "ELE_BLE_EndPoints", FA, ["plastic_black", "zinc"], [
        box((0.25, 2.55, 0.62), (0.030, 0.025, 0.018), 0.002), box((0.0, -2.80, 0.76), (0.030, 0.025, 0.018), 0.002),
        box((0.0, 0.20, 0.545), (0.030, 0.025, 0.018), 0.002), box((0.15, -2.80, 0.60), (0.030, 0.025, 0.018), 0.002),
        [box((s * 0.56, y, 0.70), (0.030, 0.025, 0.018), 0.002) for s in (1, -1) for y in (1.35, -1.35)],
        [torx((s * 0.56, y, 0.712), Z, 0.004, 1) for s in (1, -1) for y in (1.35, -1.35)],
    ], "Puntos finales Bluetooth LE de la llave del teléfono (fascia, interior, trasera y pasos de rueda; T20 a 1,5 N·m)",
        edir=(0, 0, 1), dist=0.3, stage=6, fid="A",
        note="Unos 8 puntos según el manual de servicio; las posiciones exactas no están publicadas"))
    A(V3.part(M, "ELE_Powershare_48V_Outlets", FA, ["plastic_black", "connector_grey"], [
        box((0.40, 2.30, 1.152), (0.060, 0.050, 0.014), 0.003), box((0.0, -0.90, 1.615), (0.060, 0.050, 0.014), 0.003),
    ], "Tomas de 48 V de 400 W (frunk y techo; fuente secundaria)", edir=(0, 0, 1), dist=0.3, stage=6, fid="A",
        note="Fuente secundaria; el manual de servicio no las describe"))
    A(V3.part(M, "EXT_Wiper_Motor_Controller", "GLASS_AND_MIRRORS", ["plastic_black", "zinc"], [
        box((0.25, 1.94, 1.25), (0.060, 0.050, 0.040), 0.004),
        box((0.285, 1.94, 1.25), (0.012, 0.020, 0.020), 0.002, 1), bolt((0.23, 1.94, 1.273), Z, 0.007, 1),
    ], "Controlador del motor del limpiaparabrisas (48 V)", edir=(0.3, 0.3, 1), dist=0.35, stage=6))
    A(V3.part(M, "STR_Steering_Column_Control_Module", "STEERING", ["plastic_black", "zinc", "connector_grey"], [
        box((-0.39, 0.92, 0.935), (0.070, 0.050, 0.050), 0.004),
        box((-0.39, 0.945, 0.96), (0.030, 0.012, 0.014), 0.002, 2),
    ], "Módulo de control de la columna de dirección (SCCM; conectores X0012–X0014 al controlador izquierdo)",
        edir=(0, -0.5, 0.3), dist=0.35, stage=2))
    A(V3.part(M, "INT_TCU_Bracket", T, ["plastic_black", "steel_black", "zinc"], [
        box((0.30, 0.63, 1.676), (0.10, 0.060, 0.020), 0.003),
        box((0.30, 0.63, 1.693), (0.12, 0.070, 0.006), 0.002, 1),
        torx((0.27, 0.63, 1.665), (0, 0, -1), 0.005, 2), torx((0.33, 0.63, 1.665), (0, 0, -1), 0.005, 2),
        line(clip, (0.26, 0.60, 1.699), (0.34, 0.66, 1.699), 4, axis=Z, d=0.010, m=0),
    ], "Unidad de control de telemática (TCU) con soporte (2 tornillos T25 a 3 N·m, 4 + 2 clips)",
        edir=(0.2, 0, 1), dist=0.35, stage=6))
    return [o for o in out if o is not None]
