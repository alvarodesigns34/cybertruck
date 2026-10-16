"""Ficha dimensional maestra del Tesla Cybertruck Cyberbeast (configuración 2026, EE. UU.).

Módulo de Python puro (sin bpy). Todas las cotas están en metros y en el sistema de
coordenadas del proyecto:

    +Y = hacia delante, +X = lado derecho (acompañante en EE. UU.), +Z = arriba.
    Origen: suelo, plano de simetría, punto medio de la batalla.
    Altura de suspensión de referencia: «Medium» (manual del propietario).

Procedencia de los datos (ver docs/research-and-fidelity.md):
  * [V] Verificado: manual del propietario de Tesla (dimensiones, ruedas, frenos).
  * [R] Reconstruido: medido sobre las vistas ortográficas oficiales del manual
        (imagen GUID-9B40DE41..., vista lateral y planta) con escala calibrada a partir
        de la batalla oficial (8,178 mm/px) y validada con voladizos y altura libre.
  * [A] Aproximado: interpretación razonada sin medición directa.
"""

import math

# ---------------------------------------------------------------------------
# Cotas oficiales [V] (manual del propietario, «Dimensions, Weights, and Cargo Capacity»)
# ---------------------------------------------------------------------------
LENGTH = 5.6829            # longitud total
WIDTH_BODY = 2.0316        # anchura sin espejos
WIDTH_MIRRORS = 2.4133     # anchura con espejos desplegados
WIDTH_FOLDED = 2.2007      # anchura con espejos plegados
HEIGHT_MEDIUM = 1.7938     # altura total, suspensión «Medium»
WHEELBASE = 3.6350
TRACK = 1.7720             # vía delantera y trasera (en el centro de la rueda)
OVERHANG_F = 0.8783
OVERHANG_R = 1.1696
GROUND_CLEAR_MEDIUM = 0.2570
BED_FLOOR_LENGTH = 1.8246
BED_FLOOR_WIDTH = 1.2954
BED_HEIGHT_FRONT = 0.7279
BED_HEIGHT_REAR = 0.5038

# Alturas de suspensión neumática (desplazamiento respecto a «Medium») [V]
RIDE_HEIGHTS = {
    "entry_exit": -0.055, "low": -0.040, "medium": 0.0,
    "high": 0.060, "very_high": 0.100, "extract": 0.150,
}

# Posiciones derivadas [V]
Y_FRONT_AXLE = WHEELBASE / 2.0           # +1.8175
Y_REAR_AXLE = -WHEELBASE / 2.0           # -1.8175
Y_FRONT_END = Y_FRONT_AXLE + OVERHANG_F  # +2.6958
Y_REAR_END = Y_REAR_AXLE - OVERHANG_R    # -2.9871
X_WHEEL = TRACK / 2.0                    # 0.886

# ---------------------------------------------------------------------------
# Ruedas y neumáticos [V]: llanta 20 x 9.0J ET58.5; Pirelli Scorpion ATR 285/65R20
# ---------------------------------------------------------------------------
RIM_DIAM_IN = 20.0
RIM_WIDTH_IN = 9.0
RIM_OFFSET = 0.0585
TIRE_WIDTH = 0.285
TIRE_ASPECT = 0.65
TIRE_SIDEWALL = TIRE_WIDTH * TIRE_ASPECT            # 0.18525
RIM_RADIUS = RIM_DIAM_IN * 0.0254 / 2.0             # 0.254
TIRE_RADIUS = RIM_RADIUS + TIRE_SIDEWALL            # 0.43925 (Ø 878,5 mm)
WHEEL_CENTER_Z = 0.437                              # radio estático bajo carga (aplastamiento ~2 mm) [A]
LUG_COUNT = 6                                       # [A] 6 tuercas, llave de 21 mm [V]
LUG_TORQUE_NM = 205

# Frenos [V] (manual, «Subsystems»)
FRONT_ROTOR_D = 0.351
FRONT_ROTOR_T = 0.032
REAR_ROTOR_D = 0.356
REAR_ROTOR_T = 0.023

# ---------------------------------------------------------------------------
# Perfil superior en el plano de simetría [R] (Y, Z) — medido y simplificado
# ---------------------------------------------------------------------------
TOP_PROFILE = [
    (2.668, 1.000),    # arista superior del frontal
    (2.640, 1.037),    # chaflán frontal -> capó (tapa del maletero delantero)
    (1.945, 1.283),    # extremo trasero del capó (pendiente 19,5°)
    (1.930, 1.300),    # escalón del alojamiento del limpiaparabrisas
    (1.400, 1.480),    # parabrisas, tramo inferior (18,8°)
    (0.950, 1.613),
    (0.710, 1.688),
    (0.450, 1.771),
    (0.330, 1.7935),   # vértice (zona redondeada)
    (0.190, 1.7935),
    (0.000, 1.776),
    (-0.505, 1.721),
    (-0.971, 1.652),   # fin de la cabina / inicio de la cubierta de la caja
    (-2.942, 1.349),   # arista superior trasera
]

# Perfil frontal (Y en función de Z) [R]
FRONT_FACE_TOP_Z = 1.000
LIGHTBAR_Z = (0.958, 0.986)         # barra de luz delantera
FRONT_FACE_Y_TOP = 2.672
FRONT_FACE_Y_BOT = 2.662
FRONT_FACE_BOT_Z = 0.690
FRONT_BUMPER = {
    "recess_y": 2.617, "recess_z": (0.645, 0.680),
    "face_y": 2.6958, "face_z": (0.525, 0.630),
    "under_y": 2.605, "under_z": (0.424, 0.515),
    "lip_y": 2.640, "lip_z": (0.398, 0.420),
}
# Rampa de ataque (Y, Z) del borde inferior delantero [R]
FRONT_UNDER = [(2.640, 0.398), (2.559, 0.350), (2.484, 0.318), (2.386, 0.290), (2.367, 0.266)]

# Perfil trasero [R]
REAR_TOP = (-2.945, 1.345)
TAILGATE_FACE = [(-2.945, 1.345), (-2.929, 1.070), (-2.901, 0.751), (-2.885, 0.727)]
REAR_BUMPER = {
    "notch_y": -2.800, "notch_z": (0.678, 0.718),
    "top_z": 0.669, "face_y": Y_REAR_END, "face_z": (0.629, 0.669),
}
REAR_UNDER = [(-2.986, 0.629), (-2.969, 0.506), (-2.918, 0.375), (-2.830, 0.350),
              (-2.812, 0.310), (-2.558, 0.291), (-2.345, 0.269)]

# ---------------------------------------------------------------------------
# Secciones transversales [R]
# ---------------------------------------------------------------------------
Z_CREASE = 0.588           # pliegue lateral inferior (anchura máxima de la carrocería)
HW_CREASE = 0.988          # semianchura de la carrocería en el pliegue
SIDE_LEAN_DEG = 6.0        # inclinación hacia dentro de la cara lateral superior
Z_ROCKER_TOP = 0.405       # arista superior del faldón inferior oscuro
HW_ROCKER = 0.952
Z_ROCKER_BOT = 0.262
GLASS_LEAN_DEG = 19.0      # inclinación del invernadero (cristales laterales)
BELT_LEDGE = 0.017         # retranqueo del cristal respecto a la arista de cintura

TAN_SIDE = math.tan(math.radians(SIDE_LEAN_DEG))
TAN_GLASS = math.tan(math.radians(GLASS_LEAN_DEG))

# Línea de cintura (borde inferior de los cristales laterales) [R]
# Z = 1.1927 + (1.6867 - Y) * 0.0618  (asciende 3,5° hacia atrás)
BELT_Z0, BELT_Y0, BELT_SLOPE = 1.1927, 1.6867, 0.0618
GLASS_TIP_Y = 1.876        # punta delantera del cristal de la puerta delantera
CAB_REAR_Y = -0.918        # borde trasero de la puerta trasera / pilar C

# Juntas de puertas [R]
DOOR_F_FRONT_Y = 1.1876
DOOR_B_SEAM_Y = 0.0797
DOOR_R_REAR_Y = -0.918
GLASS_F_REAR_Y = 0.112     # borde trasero del cristal delantero
GLASS_R_FRONT_Y = 0.047    # borde delantero del cristal trasero
GLASS_R_REAR_Y = -0.897

# Pasos de rueda (borde exterior de las aletas negras) [R]
FLARE_F = {"top_z": 1.025, "y_front": 2.130, "y_rear": 1.486,
           "front_angle": 50.0, "rear_angle": 56.0, "bottom_front_z": 0.660,
           "bottom_rear_z": Z_ROCKER_TOP}
FLARE_R = {"top_z": 1.060, "y_front": -1.480, "y_rear": -2.158,
           "front_angle": 54.0, "rear_angle": 53.0, "bottom_front_z": Z_ROCKER_TOP,
           "bottom_rear_z": 0.640}
FLARE_BAND = 0.088         # anchura visible de la aleta
FLARE_HW = 1.040           # semianchura exterior de las aletas (planta)

# Planta del frontal: (semianchura, Y) [R]
FRONT_PLAN = [(0.000, 2.668), (0.377, 2.662), (0.622, 2.612), (0.710, 2.562),
              (0.940, 2.400), (0.975, 2.330)]
# Estrechamiento trasero en planta: (Y, semianchura en el pliegue) [R]
REAR_TAPER = [(-2.220, HW_CREASE), (-2.656, 0.940), (-2.983, 0.931)]

# Caja de carga [R]/[A]
BED_FLOOR_Z = 0.865
BED_FRONT_Y = -0.985
BED_TAILGATE_INNER_Y = -2.870

# Habitáculo [V] cotas interiores del manual
HEADROOM_F = 1.0588
HEADROOM_R = 0.9919
LEGROOM_F = 1.0436
LEGROOM_R = 1.0388
SHOULDER_F = 1.6080
SHOULDER_R = 1.5764
HIP_F = 1.4533

# Batería [V]/[A]: 1.344 celdas 4680 (Ø46 x 80 mm), 123 kWh, ~700 V nominal (manual)
CELL_D = 0.046
CELL_H = 0.080
CELL_COUNT = 1344


def interp(points, x):
    """Interpolación lineal sobre una lista de (x, y) con x monótona (creciente o decreciente)."""
    pts = points if points[0][0] <= points[-1][0] else list(reversed(points))
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = 0.0 if x1 == x0 else (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]


def z_top(y):
    """Altura de la superficie superior (capó, parabrisas, techo, cubierta) en Y."""
    return interp(TOP_PROFILE, y)


def z_belt(y):
    """Altura de la línea de cintura en Y."""
    return BELT_Z0 + (BELT_Y0 - y) * BELT_SLOPE


def hw_crease(y):
    """Semianchura en el pliegue, con el estrechamiento trasero en planta."""
    if y < REAR_TAPER[0][0]:
        return interp([(p[0], p[1]) for p in REAR_TAPER], y)
    return HW_CREASE


def hw_side(y, z):
    """Semianchura de la cara lateral superior (por encima del pliegue)."""
    return hw_crease(y) - (z - Z_CREASE) * TAN_SIDE


def hw_lower(y, z):
    """Semianchura de la cara lateral inferior (entre faldón y pliegue)."""
    t = (z - Z_ROCKER_TOP) / (Z_CREASE - Z_ROCKER_TOP)
    hw_r = HW_ROCKER - (HW_CREASE - hw_crease(y))
    return hw_r + t * (hw_crease(y) - hw_r)


def hw_body(y, z):
    """Semianchura exterior de la carrocería en (Y, Z)."""
    if z >= Z_CREASE:
        return hw_side(y, z)
    if z >= Z_ROCKER_TOP:
        return hw_lower(y, z)
    return HW_ROCKER - (HW_CREASE - hw_crease(y))


def hw_glass(y, z):
    """Semianchura del plano del invernadero (cristales laterales y pilares)."""
    zb = z_belt(y)
    return hw_side(y, zb) - BELT_LEDGE - (z - zb) * TAN_GLASS


def hw_roof_edge(y):
    """Semianchura de la arista superior del invernadero."""
    return hw_glass(y, z_top(y))


def hood_side_split_y():
    """Y a partir de la cual el capó queda por debajo de la línea de cintura (sin hombro)."""
    lo, hi = 1.9, 2.66
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if z_top(mid) > z_belt(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def front_plan_y(hw):
    """Y del frontal en planta para una semianchura dada."""
    return interp(FRONT_PLAN, hw)


def summary():
    return {
        "length": LENGTH, "wheelbase": WHEELBASE, "track": TRACK,
        "front_end": Y_FRONT_END, "rear_end": Y_REAR_END,
        "height_medium": HEIGHT_MEDIUM, "max_profile_z": max(p[1] for p in TOP_PROFILE),
        "tire_diameter": 2 * TIRE_RADIUS, "hood_split_y": hood_side_split_y(),
        "roof_edge_hw_apex": hw_roof_edge(0.26), "roof_edge_hw_cab_rear": hw_roof_edge(-0.80),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
