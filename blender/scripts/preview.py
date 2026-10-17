"""Renders de control rápidos (Workbench/EEVEE) para la verificación iterativa del modelo."""

import math
import os
import bpy
from mathutils import Vector

VIEWS = {
    # nombre: (posición de cámara, objetivo, ortográfica, escala_orto, lente)
    "lateral_izq": ((-12.0, -0.15, 0.9), (0.0, -0.15, 0.9), True, 6.4, 50),
    "lateral_der": ((12.0, -0.15, 0.9), (0.0, -0.15, 0.9), True, 6.4, 50),
    "frontal": ((0.0, 12.0, 0.95), (0.0, 0.0, 0.95), True, 3.6, 50),
    "trasera": ((0.0, -12.0, 0.95), (0.0, 0.0, 0.95), True, 3.6, 50),
    "superior": ((0.0, -0.15, 12.0), (0.0, -0.15, 0.0), True, 6.4, 50),
    "inferior": ((0.0, -0.15, -12.0), (0.0, -0.15, 0.0), True, 6.4, 50),
    "rueda_tras": ((-2.9, -0.9, 0.75), (-0.9, -1.82, 0.5), False, 0, 50),
    "bajos_persp": ((-3.5, 4.5, -1.2), (0.0, 0.0, 0.35), False, 0, 35),
    "tres_cuartos_del": ((-6.2, 6.4, 2.5), (0.0, 0.15, 0.75), False, 0, 45),
    "tres_cuartos_tras": ((6.0, -7.2, 2.7), (0.0, -0.4, 0.8), False, 0, 45),
    "rueda_del": ((-2.9, 2.9, 0.75), (-0.9, 1.82, 0.5), False, 0, 50),
    "interior": ((-0.15, -0.62, 1.32), (-0.12, 1.2, 0.95), False, 0, 16),
    "interior_trasero": ((0.35, 0.55, 1.40), (-0.05, -0.9, 0.80), False, 0, 16),
}


def _camera():
    cam = bpy.data.objects.get("CAM_PREVIEW")
    if cam is None:
        data = bpy.data.cameras.new("CAM_PREVIEW")
        cam = bpy.data.objects.new("CAM_PREVIEW", data)
        col = bpy.data.collections.get("REFERENCE_AND_HELPERS")
        (col or bpy.context.scene.collection).objects.link(cam)
    return cam


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render(view, path, engine="BLENDER_WORKBENCH", res=(1600, 900), samples=16, ortho_scale=None,
           cam_loc=None, cam_target=None, lens=None):
    sc = bpy.context.scene
    cam = _camera()
    loc, tgt, ortho, oscale, lns = VIEWS.get(view, (cam_loc, cam_target, False, 0, 50))
    loc = cam_loc or loc
    tgt = cam_target or tgt
    cam.location = loc
    look_at(cam, tgt)
    if view == "superior":
        cam.rotation_euler = (0.0, 0.0, -math.pi / 2)     # delantero hacia la izquierda
    elif view == "inferior":
        cam.rotation_euler = (math.pi, 0.0, -math.pi / 2)
    cam.data.type = "ORTHO" if ortho else "PERSP"
    cam.data.ortho_scale = ortho_scale or oscale or 6.0
    cam.data.lens = lens or lns
    cam.data.clip_end = 200
    sc.camera = cam
    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    if engine == "BLENDER_WORKBENCH":
        sh = sc.display.shading
        sh.light = "STUDIO"
        sh.color_type = "MATERIAL"
        sh.show_cavity = True
        sh.cavity_type = "BOTH"
        sh.show_object_outline = True
        sh.show_specular_highlight = True
        sc.display.render_aa = "8"
    elif engine == "CYCLES":
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.device = "GPU"
    else:
        try:
            sc.eevee.taa_render_samples = samples
        except Exception:
            pass
    sc.render.filepath = path
    if path.lower().endswith(".jpg"):
        sc.render.image_settings.file_format = "JPEG"
        sc.render.image_settings.quality = 82
    else:
        sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    return path


def _find_lc(lc, name):
    if lc.name == name:
        return lc
    for c in lc.children:
        r = _find_lc(c, name)
        if r:
            return r
    return None


def set_excluded(names, value):
    """Excluye/incluye colecciones de la capa de vista (afecta también al render)."""
    root = bpy.context.view_layer.layer_collection
    for n in names:
        lc = _find_lc(root, n)
        if lc:
            lc.exclude = value


EXTERIOR = ["EXTERIOR_PANELS", "DOORS_AND_HATCHES", "GLASS_AND_MIRRORS", "BODY_STRUCTURE", "LIGHTING",
            "CARGO_BED", "INTERIOR_TRIM", "BODY_FASTENERS"]


ALL_COLS = ["EXTERIOR_PANELS", "DOORS_AND_HATCHES", "GLASS_AND_MIRRORS", "LIGHTING", "CARGO_BED", "BODY_STRUCTURE",
            "BODY_FASTENERS", "UNDERBODY", "FRONT_WHEELS_AND_BRAKES", "REAR_WHEELS_AND_BRAKES", "FRONT_SUSPENSION",
            "REAR_SUSPENSION", "STEERING", "BATTERY_ASSEMBLY", "DRIVE_UNITS", "INTERIOR_DASHBOARD", "INTERIOR_CONTROLS",
            "INTERIOR_SEATS", "INTERIOR_DOORS", "INTERIOR_TRIM"]

BODY_COLS = ["EXTERIOR_PANELS", "DOORS_AND_HATCHES", "GLASS_AND_MIRRORS", "LIGHTING", "CARGO_BED",
             "INTERIOR_DASHBOARD", "INTERIOR_CONTROLS", "INTERIOR_SEATS", "INTERIOR_DOORS", "INTERIOR_TRIM",
             "BODY_FASTENERS"]

# Planos de documentación: (iluminación, cámara (pos, objetivo, lente | 'CAM_*'), exposición EV,
#                           colecciones excluidas, prefijos ocultos, factor de explosión)
SHOTS = {
    "01_tres_cuartos_delantera": ("studio", "CAM_3Q_Front", 0.0, [], [], 0.0),
    "02_tres_cuartos_trasera": ("studio", "CAM_3Q_Rear", 0.0, [], [], 0.0),
    "03_perfil_lateral": ("studio", "CAM_Side_Profile", 0.0, [], [], 0.0),
    "04_frontal": ("studio", "CAM_Front", 0.0, [], [], 0.0),
    "05_trasera": ("studio", "CAM_Rear", 0.0, [], [], 0.0),
    "06_superior": ("studio", "CAM_Top", 0.0, [], [], 0.0),
    "07_interior": ("studio", ((0.40, 0.36, 1.22), (-0.34, 1.05, 1.00), 17), 1.6, [], [], 0.0),
    "08_rueda_y_freno": ("studio", ((-2.2, 2.45, 0.55), (-0.9, 1.82, 0.44), 50), 0.3, [], [], 0.0),
    "09_bajos": ("studio", ((-3.4, 4.6, -0.55), (0.0, 0.3, 0.38), 30), 0.8, [], ["STUDIO_Cyclorama"], 0.0),
    "10_vista_explosionada": ("studio", "CAM_Exploded", 0.0, [], [], 1.0),
    "11_exterior_dia": ("exterior", ((-6.6, 6.9, 1.6), (0.0, 0.1, 0.80), 50), 0.0, [], [], 0.0),
    "12_atardecer": ("sunset", ((6.0, -7.4, 1.5), (0.0, -0.4, 0.85), 50), 0.0, [], [], 0.0),
    "13_cielo_cubierto": ("overcast", ((-8.5, -2.5, 1.3), (0.0, -0.2, 0.85), 50), 0.0, [], [], 0.0),
    "14_chasis_y_tren_motriz": ("studio", ((-4.4, 4.2, 2.9), (0.0, 0.0, 0.55), 30), 0.3, BODY_COLS,
                                ["BODY_Cabin", "BODY_Firewall", "BODY_Frunk", "BODY_WheelLiner", "EXT_Roof",
                                 "BODY_Casting", "BODY_Sill", "BODY_DoorRing", "BODY_Mast", "BODY_Tailgate",
                                 "BODY_Floor", "BODY_Seat", "BODY_RearWall", "BODY_IP", "BODY_Megabeam",
                                 "BODY_Rivets", "BODY_Front_Bumper", "BODY_Rear_Energy"], 0.0),
    "15_estructura_carroceria": ("studio", ((-4.6, 4.4, 3.3), (0.0, -0.1, 0.70), 30), 0.3, BODY_COLS + [
        "BATTERY_ASSEMBLY", "DRIVE_UNITS", "FRONT_SUSPENSION", "REAR_SUSPENSION", "STEERING", "UNDERBODY",
        "FRONT_WHEELS_AND_BRAKES", "REAR_WHEELS_AND_BRAKES"], ["BODY_Cabin", "BODY_Firewall", "BODY_Frunk",
                                                               "BODY_WheelLiner", "EXT_Roof"], 0.0),
    "16_bateria": ("studio", ((-1.7, 1.5, 1.6), (0.0, 0.0, 0.40), 32), 0.4, BODY_COLS,
                   ["BAT_Enclosure_Lid", "HV_Ancillary_Cover", "BODY_", "EXT_Roof", "INT_", "LV_Harness", "BAT_Block_1_Mica", "BAT_Block_2_Mica", "BAT_Block_3_Mica", "BAT_Block_4_Mica", "BAT_Block_3_Busbars", "BAT_Block_4_Busbars"], 0.0),
    "17_suspension_delantera": ("studio", ((-1.85, 2.55, 0.95), (-0.62, 1.82, 0.55), 35), 0.5, BODY_COLS,
                                ["WHL_FL", "BODY_", "EXT_Roof"], 0.0),
    "18_unidad_trasera_trimotor": ("studio", ((-1.1, -3.2, 1.3), (0.0, -1.95, 0.50), 30), 0.5, BODY_COLS,
                                   ["BODY_", "EXT_Roof", "WHL_RL", "WHL_RR", "CARGO_", "CHS_Aeroshield_Rear"], 0.0),
    "19_asientos_y_costuras": ("studio", ((-0.05, 0.95, 1.30), (-0.42, 0.40, 0.85), 24), 1.6, [], [], 0.0),
    "20_faro_y_barra_de_luz": ("studio", ((-1.9, 3.6, 1.45), (-0.55, 2.45, 1.0), 40), 0.0, [], [], 0.0),
    "21_caja_tonneau_y_porton": ("studio", ((2.6, -5.2, 2.7), (0.0, -2.0, 1.1), 35), 0.0, [], [], 0.0),
    # --- Versión 4: el interior funcional de los conjuntos (carcasas ocultas)
    "22_motor_delantero_por_dentro": ("studio", ((-0.95, 2.95, 1.05), (-0.02, 1.95, 0.50), 40), 0.6,
                                      [c for c in ALL_COLS if c != "DRIVE_UNITS"],
                                      ["DU_F_Motor_Housing", "DU_F_Gearbox$", "DU_F_NVH_Cover", "DU_F_Inverter$",
                                       "DU_R_", "DU_Halfshaft_R", "DU_Halfshaft_FR", "DU_F_HeatExchanger"], 0.0),
    "23_unidad_trasera_por_dentro": ("studio", ((1.25, -3.25, 1.30), (0.0, -1.95, 0.48), 34), 0.6,
                                     [c for c in ALL_COLS if c != "DRIVE_UNITS"],
                                     ["DU_R_Motor_L", "DU_R_Motor_R", "DU_R_Gearbox", "DU_R_NVH", "DU_R_Inverter_L$",
                                      "DU_R_Inverter_R$", "DU_F_", "DU_Halfshaft_F", "DU_R_PlateCooler", "DU_R_Mounts"],
                                     0.0),
    "24_pinza_por_dentro": ("studio", ((-1.30, 1.22, 0.80), (-0.89, 1.70, 0.50), 50), 0.5,
                            [c for c in ALL_COLS if c != "FRONT_WHEELS_AND_BRAKES"],
                            ["WHL_FL", "BRK_FL_Caliper$", "BRK_FL_Shield", "WHEEL_FR", "WHL_FR", "BRK_FR", "WHL_R", "BRK_R"],
                            0.0),
    "25_asiento_por_dentro": ("studio", ((1.55, 1.45, 1.35), (0.40, 0.32, 0.92), 34), 0.8,
                              [c for c in ALL_COLS if c != "INTERIOR_SEATS"],
                              ["INT_SeatF_R_Cushion$", "INT_SeatF_R_Back$", "INT_SeatF_R_Back_Shell", "INT_SeatF_R_Covers",
                               "INT_SeatF_R_Side_Shield", "INT_SeatF_L", "INT_SeatF_Frame_L", "INT_SeatF_Heat_Vent_Mats_L",
                               "INT_SeatR", "INT_Seatbelt", "INT_Airbag_Seat"], 0.0),
    "26_climatizador_y_electronica": ("studio", ((1.25, 0.05, 1.55), (0.12, 1.05, 0.82), 34), 0.8,
                                      [c for c in ALL_COLS if c not in ("INTERIOR_DASHBOARD", "INTERIOR_CONTROLS")],
                                      ["INT_HVAC_Module", "INT_IP_", "INT_Display_Center_Housing", "INT_Display_Center_Screen",
                                       "INT_Car_Computer$", "INT_Airbag", "INT_Demist", "INT_Floor_Duct", "INT_Footwell",
                                       "INT_Console", "INT_Display_Rear", "INT_Pedal", "BRK_Pedal", "INT_Restraint",
                                       "INT_Cabin_Outlets", "INT_Gear", "DISPLAY", "INT_Ethernet", "INT_Puddle",
                                       "INT_Tweeter", "INT_HVAC_Sensors", "INT_HVAC_Blend"], 0.0),
}


def _hidden_by(name, hide):
    """Prefijos de ocultación; los que terminan en «$» exigen el nombre exacto."""
    return any(name == h[:-1] if h.endswith("$") else name.startswith(h) for h in hide)


def render_shot(name, folder, samples=128, res=(1600, 900)):
    """Renderiza un plano de documentación con Cycles y lo guarda como JPEG."""
    import build_scene
    import build_explode
    light, cam, ev, excl, hide, explode = SHOTS[name]
    build_scene.lighting(light)
    sc = bpy.context.scene
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.exposure = -0.6 + ev
    set_excluded(excl, True)
    hidden = []
    for o in bpy.data.objects:
        if hide and _hidden_by(o.name, hide) and not o.hide_render:
            o.hide_render = True
            hidden.append(o)
    build_explode.set_explode(explode)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name + ".jpg")
    try:
        if isinstance(cam, str):
            c = bpy.data.objects[cam]
            sc.camera = c
            sc.render.engine = "CYCLES"
            sc.render.resolution_x, sc.render.resolution_y = res
            sc.render.resolution_percentage = 100
            sc.cycles.samples = samples
            sc.cycles.use_denoising = True
            sc.cycles.device = "GPU"
            sc.render.filepath = path
            sc.render.image_settings.file_format = "JPEG"
            sc.render.image_settings.quality = 82
            bpy.ops.render.render(write_still=True)
        else:
            loc, tgt, lens = cam
            render("x", path, engine="CYCLES", res=res, samples=samples, cam_loc=loc, cam_target=tgt, lens=lens)
    finally:
        for o in hidden:
            o.hide_render = False
        set_excluded(excl, False)
        build_explode.set_explode(0.0)
        sc.view_settings.exposure = -0.6
    return path


def render_set(folder, views, **kw):
    os.makedirs(folder, exist_ok=True)
    out = []
    for v in views:
        out.append(render(v, os.path.join(folder, f"{v}.png"), **kw))
    return out
