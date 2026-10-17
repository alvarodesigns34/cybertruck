"""Versión 3 · tren motriz, alta tensión, batería y gestión térmica: piezas desglosadas del backlog P2.

Fuentes (docs/ficha-tecnica-piezas.md §3.4; manual de servicio «SM» y teardowns de Munro, citados allí):
  [V] Denominación, cantidad y pares de apriete (TRN-xxx).
  [R] Posición y forma: reconstruidas junto a las envolventes que ya tenía el modelo (Supermanifold,
      unidades motrices, bahía auxiliar); los manuales no publican masas ni dimensiones de estas piezas.
"""

from mathutils import Vector
import ct_v3 as V3
from ct_v3 import box, cyl, ring, disc, hull, beam, sweep, hose, bolt, nut, torx, clip

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def line(fn, a, b, n, **kw):
    a, b = Vector(a), Vector(b)
    kw.setdefault("m", 1)
    return [fn(tuple(a + (b - a) * (i / max(1, n - 1))), **kw) for i in range(n)]


def build(M):
    out = []
    A = out.extend

    # --- Gestión térmica (hoy agrupada en THM_Supermanifold) -------------------------------------------------
    A(V3.part(M, "THM_Octovalve", "UNDERBODY", ["alu_machined", "plastic_black", "zinc"], [
        # sobre la placa de asiento de la Octovalve en la tapa del Supermanifold
        box((0.30, 1.83, 0.935), (0.10, 0.12, 0.10), 0.006),
        cyl((0.30, 1.83, 0.985), (0.30, 1.83, 1.035), 0.032, seg=16, m=1),
        line(torx, (0.26, 1.79, 0.987), (0.34, 1.87, 0.987), 4, axis=Z, d=0.006),
    ], "Octovalve (4 tornillos T25 a 7 N·m, 7 clips de resorte, 4 conectores)", edir=(0.5, 0.3, 0.5), dist=0.45,
        stage=5))
    A(V3.part(M, "THM_Coolant_Pump", "UNDERBODY", ["alu_cast", "zinc"], [
        cyl((0.39, 1.734, 0.70), (0.39, 1.834, 0.70), 0.040, 0.036, 20, 0),
        line(torx, (0.36, 1.839, 0.72), (0.42, 1.839, 0.68), 4, axis=Y, d=0.005),
    ], "Bomba de refrigerante del Supermanifold (4 tornillos T20 a 2 N·m, giro de purga 3.500–6.500 rpm)",
        edir=(0.5, -0.3, 0.3), dist=0.45, stage=5))
    A(V3.part(M, "THM_Chiller", "UNDERBODY", ["alu_machined", "plastic_black", "zinc"], [
        # entre el Supermanifold, la HCU, el larguero de la fundición (x = 0,45) y la pared trasera del frunk
        box((0.412, 1.93, 0.74), (0.07, 0.08, 0.16), 0.005),
        [box((0.412, 1.93, 0.66 + 0.04 * k), (0.078, 0.088, 0.003), 0.001) for k in range(1, 4)],
        line(nut, (0.385, 1.90, 0.825), (0.44, 1.96, 0.825), 4, axis=Z, d=0.008, stud=0.0),
        box((0.412, 1.88, 0.70), (0.05, 0.020, 0.040), 0.003, 1),
    ], "Enfriador (chiller) de la batería (4 tuercas 8 mm a 7 N·m, controlador 3 pernos a 4 N·m, 9 conectores)",
        edir=(0.5, 0.4, 0), dist=0.45, stage=5))
    A(V3.part(M, "THM_LCCR_Condenser", "UNDERBODY", ["alu_machined", "plastic_black", "zinc"], [
        box((0.412, 1.93, 0.95), (0.07, 0.08, 0.10), 0.005),
        line(nut, (0.385, 1.90, 1.005), (0.44, 1.96, 1.005), 4, axis=Z, d=0.008, stud=0.0),
        cyl((0.39, 1.89, 0.95), (0.39, 1.86, 0.95), 0.009, seg=10, m=1), cyl((0.435, 1.89, 0.95), (0.435, 1.86, 0.95), 0.009, seg=10, m=1),
    ], "Condensador refrigerado por líquido (LCCR; 4 tuercas 8 mm a 7 N·m, 2 tapas de puerto A/C)",
        edir=(0.5, 0.4, 0.4), dist=0.45, stage=5))
    A(V3.part(M, "THM_Coolant_Bottle", "UNDERBODY", ["plastic_textured", "plastic_black"], [
        # por fuera del larguero de la fundición, sobre el brazo superior
        cyl((0.53, 2.14, 0.84), (0.53, 2.14, 1.00), 0.050, 0.046, 24, 0),
        cyl((0.53, 2.14, 1.00), (0.53, 2.14, 1.03), 0.030, seg=16, m=1),
    ], "Botella de refrigerante con tapón (nivel entre NOM y MAX; recarga al vacío 60–70 cmHg)",
        edir=(0.5, 0.2, 0.8), dist=0.45, stage=5))
    A(V3.part(M, "THM_Expansion_Valves", "UNDERBODY", ["alu_machined", "copper", "plastic_black"], [
        cyl((0.12, 1.84, 1.02), (0.12, 1.84, 1.07), 0.016, seg=12, m=0),
        cyl((0.12, 1.84, 1.07), (0.12, 1.84, 1.09), 0.020, seg=14, m=1),
        cyl((0.26, 1.84, 1.02), (0.26, 1.84, 1.07), 0.016, seg=12, m=0),
        cyl((0.26, 1.84, 1.07), (0.26, 1.84, 1.09), 0.020, seg=14, m=1),
    ], "Válvulas de expansión con bobinas (Supermanifold)", edir=(0, 0.3, 1), dist=0.4, stage=6))
    A(V3.part(M, "THM_AC_Service_Ports", "UNDERBODY", ["valve_brass", "plastic_black"], [
        cyl((-0.10, 1.86, 0.90), (-0.10, 1.86, 0.94), 0.008, seg=10, m=0), cyl((-0.10, 1.86, 0.94), (-0.10, 1.86, 0.96), 0.011, seg=12, m=1),
        cyl((-0.04, 1.86, 0.90), (-0.04, 1.86, 0.94), 0.008, seg=10, m=0), cyl((-0.04, 1.86, 0.94), (-0.04, 1.86, 0.96), 0.011, seg=12, m=1),
    ], "Puertos de servicio de A/C con válvulas Schrader y tapones (alta y baja presión)", edir=(0, 0, 1), dist=0.35,
        stage=6))
    A(V3.part(M, "THM_Penta_HVAC_Line", "UNDERBODY", ["hose", "alu_machined"], [
        hose([(0.25, 1.72, 0.86), (0.14, 1.58, 0.85), (0.04, 1.46, 0.84)], 0.012, 12, 5, 0),
        cyl((0.25, 1.72, 0.86), (0.28, 1.72, 0.86), 0.016, seg=12, m=1),
    ], "Línea Penta de climatización (1 tuerca 13 mm a 36 N·m, arandelas lubricadas con RB100EV)",
        edir=(0, -0.4, 0.8), dist=0.4, stage=6))
    A(V3.part(M, "THM_Car_Computer_Coolant_Hoses", "UNDERBODY", ["hose", "zinc"], [
        hose([(0.35, 1.72, 0.95), (0.38, 1.60, 1.00), (0.38, 1.46, 1.02)], 0.007, 10, 5, 0),
        hose([(0.30, 1.72, 0.93), (0.32, 1.58, 0.97), (0.31, 1.46, 0.99)], 0.007, 10, 5, 0),
        clip((0.35, 1.58, 1.01), Z, 0.012, 1),
    ], "Mangueras de refrigerante del ordenador del coche (2) con pasamuros", edir=(0, -0.4, 0.8), dist=0.4,
        stage=6))

    # --- Alta tensión ----------------------------------------------------------------------------------------------
    A(V3.part(M, "HV_Contactors", "BATTERY_ASSEMBLY", ["plastic_black", "copper", "hv_orange"], [
        box((-0.45, -1.12, 0.695), (0.07, 0.05, 0.04), 0.004), box((-0.33, -1.12, 0.695), (0.07, 0.05, 0.04), 0.004),
        [cyl((x, -1.12, 0.715), (x, -1.12, 0.730), 0.008, seg=10, m=1) for x in (-0.47, -0.43, -0.35, -0.31)],
    ], "Contactores del pack en la caja de CA (ACJB; prueba de gripado de contactor)", edir=(0, -0.2, 1), dist=0.4))
    A(V3.part(M, "HV_DPDT_Switch", "BATTERY_ASSEMBLY", ["plastic_black", "copper"], [
        box((-0.20, -1.12, 0.68), (0.08, 0.05, 0.03), 0.003),
        [cyl((x, -1.12, 0.695), (x, -1.12, 0.710), 0.007, seg=10, m=1) for x in (-0.23, -0.17)],
    ], "Interruptor DPDT 800 V / 400 V del pack (conmuta dos bloques en serie o paralelo)", edir=(0, -0.2, 1),
        dist=0.4))
    A(V3.part(M, "HV_Ancillary_Fuses", "BATTERY_ASSEMBLY", ["plastic_black", "copper", "zinc"], [
        box((0.0, -1.10, 0.69), (0.060, 0.030, 0.030), 0.003), box((0.07, -1.10, 0.69), (0.060, 0.030, 0.030), 0.003),
        line(bolt, (-0.02, -1.10, 0.705), (0.09, -1.10, 0.705), 4, axis=Z, d=0.007),
    ], "Fusibles Eaton EVK22-60-T (60 A / 1000 VDC) y Littelfuse 828-30 de la bahía auxiliar (2 × 8 mm a 6 N·m)",
        edir=(0, -0.2, 1), dist=0.4))
    A(V3.part(M, "HV_First_Responder_Loop", "BATTERY_ASSEMBLY", ["harness", "plastic_black"], [
        hose([(-0.28, 2.02, 0.95), (-0.34, 2.06, 1.02), (-0.28, 2.10, 1.00), (-0.24, 2.05, 0.95)], 0.004, 6, 4, 0),
        box((-0.26, 2.02, 0.945), (0.040, 0.030, 0.025), 0.003, 1),
    ], "Lazo de primera respuesta (desconexión MV; esperar 2 min tras cortar)", edir=(0, 0.3, 1), dist=0.45,
        stage=6))
    A(V3.part(M, "HV_Pyro_Access_Cover", "BATTERY_ASSEMBLY", ["plastic_black", "zinc"], [
        box((0.36, 1.20, 0.527), (0.22, 0.070, 0.012), 0.003),
        line(torx, (0.27, 1.20, 0.533), (0.45, 1.20, 0.533), 4, axis=Z, d=0.006),
    ], "Cubierta de acceso a los pirofusibles (4 tornillos E-Torx a 10 N·m)", edir=(0, 0, 1), dist=0.4))
    A(V3.part(M, "HV_Harness_FDU", "BATTERY_ASSEMBLY", ["hv_orange", "connector_grey", "zinc"], [
        # termina en la cara trasera del inversor delantero (y = 1,697 m)
        hose([(0.0, 1.26, 0.50), (0.10, 1.50, 0.58), (0.20, 1.655, 0.64)], 0.014, 12, 5, 0),
        box((0.20, 1.675, 0.64), (0.05, 0.040, 0.04), 0.004, 1), bolt((0.20, 1.675, 0.665), Z, 0.010, 2),
    ], "Arnés de alta tensión de la unidad motriz delantera (1 perno 10 mm a 10 N·m)", edir=(0.2, 0.4, 0.8),
        dist=0.45, stage=5))
    for s, sd in ((1, "R"), (-1, "L")):
        A(V3.part(M, f"HV_Harness_RDU_{sd}", "BATTERY_ASSEMBLY", ["hv_orange", "connector_grey", "zinc"], [
            # de la cara trasera del clúster de dispositivos a la cara delantera del inversor (sobre el motor)
            hose([(s * 0.05, -1.373, 0.63), (s * 0.12, -1.47, 0.64), (s * 0.28, -1.75, 0.66), (s * 0.30, -2.09, 0.655)],
                 0.012, 12, 5, 0),
            box((s * 0.30, -2.112, 0.655), (0.05, 0.04, 0.04), 0.004, 1),
            line(bolt, (s * 0.28, -2.112, 0.678), (s * 0.32, -2.112, 0.678), 2, axis=Z, d=0.010, m=2),
        ], f"Arnés de alta tensión del motor trasero {'derecho' if s > 0 else 'izquierdo'} (Tri Motor; 4 pernos 10 mm a 4 N·m)",
            edir=(s * 0.3, -0.6, 0.8), dist=0.45, stage=5))
    A(V3.part(M, "HV_Charge_Port_Busbar", "BATTERY_ASSEMBLY", ["copper", "zinc"], [
        sweep([(-0.99, -1.31, 0.78), (-0.86, -1.31, 0.69), (-0.62, -1.20, 0.66)], 0.030, 0.006, 0.0, 4),
        bolt((-0.99, -1.31, 0.785), X, 0.010, 1), bolt((-0.62, -1.20, 0.666), Z, 0.010, 1),
    ], "Barra colectora de la toma de carga NACS al cabezal HV (2 pernos 9 N·m; resistencia 0,050–0,195 mΩ)",
        edir=(-1, -0.3, 0), dist=0.45, stage=5))
    perim = []
    for k in range(8):
        y = 1.05 - k * 0.30
        perim += [bolt((0.805, y, 0.275), (0, 0, -1), 0.015, 0), bolt((-0.805, y, 0.275), (0, 0, -1), 0.015, 0)]
    perim += [bolt((x, 1.255, 0.35), Y, 0.018, 0) for x in (-0.6, -0.36, -0.12, 0.12, 0.36, 0.6)]
    perim += [bolt((x, -1.405, 0.36), (0, -1, 0), 0.021, 0) for x in (-0.60, -0.20, 0.20, 0.60)]
    perim += [bolt((s * x, 1.12, 0.475), Z, 0.024, 0) for s in (1, -1) for x in (0.58, 0.66, 0.74)]
    perim += [bolt((s * x, y, 0.475), Z, 0.013, 0) for s in (1, -1) for x in (0.50, 0.70) for y in (-0.95, -1.10)]
    A(V3.part(M, "BAT_Mounting_Bolts", "BATTERY_ASSEMBLY", ["zinc"], [perim],
              "Pernos de fijación del pack (laterales 16 × 15 mm, delanteros 6 × 18 mm y 6 × 24 mm, "
              "traseros 4 × 21 mm y 8 × 13 mm)", edir=(0, 0, -1), dist=0.5, stage=6))

    # --- Unidades motrices -----------------------------------------------------------------------------------------
    A(V3.part(M, "DU_F_Breather_Ground_Plugs", "DRIVE_UNITS", ["plastic_black", "copper", "zinc"], [
        cyl((0.10, 1.92, 0.57), (0.10, 1.92, 0.64), 0.012, seg=12, m=0),
        hose([(0.00, 1.78, 0.40), (0.06, 1.70, 0.46), (0.12, 1.68, 0.52)], 0.004, 8, 4, 1),
        bolt((0.10, 2.10, 0.335), (0, 0, -1), 0.015, 2), bolt((0.10, 1.74, 0.335), (0, 0, -1), 0.015, 2),
        disc((0.245, 1.8175, 0.44), X, 0.036, 0.008, 18, 1),
    ], "Respiradero, trenza de masa, tapones de llenado y vaciado (Allen 8 mm a 15 N·m) y retén de salida de la "
       "unidad delantera", edir=(0.4, 0.3, 0.6), dist=0.45, stage=6))
    A(V3.part(M, "DU_R_Breather_Plugs_Seals", "DRIVE_UNITS", ["plastic_black", "zinc"], [
        cyl((0.0, -1.90, 0.57), (0.0, -1.90, 0.64), 0.012, seg=12, m=0),
        bolt((0.0, -2.08, 0.335), (0, 0, -1), 0.015, 1), bolt((0.0, -1.74, 0.335), (0, 0, -1), 0.015, 1),
        disc((0.205, -1.8175, 0.44), X, 0.036, 0.008, 18, 1), disc((-0.205, -1.8175, 0.44), X, 0.036, 0.008, 18, 1),
    ], "Respiradero, tapones de llenado y vaciado y retenes de salida de la unidad trasera", edir=(0, -0.4, 0.6),
        dist=0.45, stage=6))
    for s, sd in ((1, "R"), (-1, "L")):
        A(V3.part(M, f"DU_R_NVH_Cover_{sd}", "DRIVE_UNITS", ["rubber", "zinc"], [
            box((s * 0.31, -2.00, 0.705), (0.30, 0.34, 0.012), 0.004),
            line(clip, (s * 0.20, -1.86, 0.712), (s * 0.42, -2.14, 0.712), 5, axis=Z),
        ], f"Cubierta acústica (NVH) del motor trasero {'derecho' if s > 0 else 'izquierdo'} (5 clips)",
            edir=(s * 0.3, -0.3, 1), dist=0.45, stage=5))
    A(V3.part(M, "DU_R_Inverter_Mount_RH", "DRIVE_UNITS", ["alu_cast", "zinc"], [
        # placa detrás del inversor y pata por fuera de la tapa del motor
        box((0.40, -2.234, 0.575), (0.10, 0.04, 0.12), 0.004), box((0.502, -1.95, 0.50), (0.10, 0.18, 0.08), 0.004),
        line(nut, (0.37, -2.259, 0.61), (0.43, -2.259, 0.61), 3, axis=(0, -1, 0), d=0.012, stud=0.0),
        line(bolt, (0.472, -1.89, 0.545), (0.532, -2.01, 0.545), 4, axis=Z, d=0.010),
    ], "Soporte del inversor derecho y del motor trasero derecho (3 × EP14 35 N·m + 55°; 4 × E14 35 N·m + 55°)",
        edir=(0.5, -0.4, -0.5), dist=0.45, stage=5))
    # Mangueras de refrigerante de las unidades motrices y de la batería
    A(V3.part(M, "THM_FDU_Coolant_Hoses", "UNDERBODY", ["hose", "zinc"], [
        # alimentación: del lado derecho de la reductora a la base del Supermanifold; inversor -> enfriador
        hose([(0.240, 1.80, 0.45), (0.27, 1.80, 0.58), (0.30, 1.82, 0.715)], 0.011, 10, 5, 0),
        hose([(0.248, 1.95, 0.63), (0.33, 1.95, 0.63), (0.41, 1.93, 0.648)], 0.011, 10, 5, 0),
        clip((0.27, 1.80, 0.58), (0, 0, 1), 0.014, 1), clip((0.33, 1.95, 0.63), (0, 0, 1), 0.014, 1),
    ], "Mangueras de refrigerante de la unidad motriz delantera (alimentación en línea e inversor–intercambiador)",
        edir=(0.3, 0.3, 0.3), dist=0.4, stage=5))
    A(V3.part(M, "THM_RDU_Coolant_Hoses", "UNDERBODY", ["hose", "zinc"], [
        hose([(0.30, -1.55, 0.60), (0.25, -1.70, 0.64), (0.31, -1.90, 0.62)], 0.011, 10, 5, 0),
        hose([(-0.30, -1.55, 0.60), (-0.25, -1.70, 0.64), (-0.31, -1.90, 0.62)], 0.011, 10, 5, 0),
        clip((0.25, -1.70, 0.65), (0, 0, 1), 0.014, 1), clip((-0.25, -1.70, 0.65), (0, 0, 1), 0.014, 1),
    ], "Mangueras de refrigerante de la unidad motriz trasera (alimentación y retorno de los dos refrigeradores de placa)",
        edir=(0, -0.4, 0.4), dist=0.4, stage=5))
    A(V3.part(M, "THM_Chiller_Battery_Hoses", "UNDERBODY", ["hose", "zinc"], [
        # desde los conectores de la cara trasera del enfriador, por debajo de la bomba de refrigerante
        hose([(0.395, 1.869, 0.70), (0.39, 1.848, 0.60), (0.34, 1.75, 0.50), (0.20, 1.46, 0.44)], 0.012, 10, 5, 0),
        hose([(0.43, 1.869, 0.70), (0.425, 1.85, 0.58), (0.415, 1.75, 0.48), (0.30, 1.46, 0.42)], 0.012, 10, 5, 0),
        clip((0.34, 1.75, 0.53), (0, 0, 1), 0.014, 1), clip((0.42, 1.75, 0.51), (0, 0, 1), 0.014, 1),
    ], "Mangueras del enfriador a la batería (suministro y retorno; 2 clips + 2 clips de borde)",
        edir=(0.3, 0, -0.5), dist=0.4, stage=5))
    return [o for o in out if o is not None]
