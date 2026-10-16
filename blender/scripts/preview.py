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


def render_set(folder, views, **kw):
    os.makedirs(folder, exist_ok=True)
    out = []
    for v in views:
        out.append(render(v, os.path.join(folder, f"{v}.png"), **kw))
    return out
