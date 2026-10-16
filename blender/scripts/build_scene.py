"""Entorno de renderizado: estudio, iluminación, entorno HDRI y cámaras de inspección.

Las luces y cámaras viven en la colección «STUDIO», separada del vehículo, para que la
exportación web contenga únicamente el Cybertruck.
"""

import math
import os
import bpy
from mathutils import Vector
import ct_lib as L

CAMERAS = {
    # nombre: (posición, objetivo, lente mm, tipo, escala_orto)
    "CAM_3Q_Front": ((-6.6, 6.9, 2.0), (0.0, 0.1, 0.80), 50, "PERSP", 0),
    "CAM_3Q_Rear": ((6.4, -7.6, 2.4), (0.0, -0.5, 0.85), 50, "PERSP", 0),
    "CAM_Side_Profile": ((26.0, -0.15, 0.90), (0.0, -0.15, 0.90), 135, "PERSP", 0),
    "CAM_Front": ((0.0, 16.0, 0.95), (0.0, 0.0, 0.95), 85, "PERSP", 0),
    "CAM_Rear": ((0.0, -16.0, 0.95), (0.0, 0.0, 0.95), 85, "PERSP", 0),
    "CAM_Top": ((0.0, -0.15, 20.0), (0.0, -0.15, 0.0), 50, "ORTHO", 6.6),
    "CAM_Interior": ((0.40, 0.36, 1.22), (-0.34, 1.05, 1.00), 17, "PERSP", 0),
    "CAM_Wheel_Detail": ((-2.6, 2.95, 0.62), (-0.95, 1.82, 0.45), 50, "PERSP", 0),
    "CAM_Underbody": ((-3.6, 5.2, -0.9), (0.0, 0.2, 0.35), 32, "PERSP", 0),
    "CAM_Exploded": ((-9.5, 9.0, 5.5), (0.0, -0.2, 0.9), 40, "PERSP", 0),
}


def studio_collection():
    col = bpy.data.collections.get("STUDIO")
    if col is None:
        col = bpy.data.collections.new("STUDIO")
        bpy.context.scene.collection.children.link(col)
    return col


def _obj(name, data, col):
    old = bpy.data.objects.get(name)
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    o = bpy.data.objects.new(name, data)
    col.objects.link(o)
    return o


def world(hdri="studio.exr", strength=0.55, rotation=0.0):
    w = bpy.data.worlds.get("CT_World") or bpy.data.worlds.new("CT_World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    folder = bpy.utils.system_resource("DATAFILES", path="studiolights/world")
    path = os.path.join(folder, hdri) if folder else None
    if path and os.path.exists(path):
        tex = nt.nodes.new("ShaderNodeTexEnvironment")
        tex.image = bpy.data.images.load(path, check_existing=True)
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Rotation"].default_value = (0, 0, rotation)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
        nt.links.new(tex.outputs["Color"], bg.inputs["Color"])
    else:
        bg.inputs["Color"].default_value = (0.05, 0.05, 0.055, 1)
    # La cámara ve un fondo neutro oscuro; reflejos e iluminación proceden del HDRI
    cam_bg = nt.nodes.new("ShaderNodeBackground")
    cam_bg.inputs["Color"].default_value = (0.020, 0.021, 0.024, 1)
    cam_bg.inputs["Strength"].default_value = 1.0
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
    nt.links.new(bg.outputs["Background"], mix.inputs[1])
    nt.links.new(cam_bg.outputs["Background"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return w


def cyclorama(col, M):
    """Suelo con curva de fondo (ciclorama) para un estudio fotográfico."""
    mb = L.MeshBuilder()
    W, D, R = 30.0, 30.0, 4.0
    prof = [(-D, 0.0), (6.0, 0.0)]
    for k in range(1, 9):
        a = (math.pi / 2) * k / 8
        prof.append((6.0 + R * math.sin(a), R - R * math.cos(a)))
    prof.append((6.0 + R, 12.0))
    rows = [[(x, -y, z) for (y, z) in prof] for x in (-W, W)]
    for j in range(len(prof) - 1):
        mb.face([rows[0][j], rows[0][j + 1], rows[1][j + 1], rows[1][j]], 0, want=(0, 0.5, 1))
    me = bpy.data.meshes.new("STUDIO_Cyclorama")
    me.from_pydata(mb.verts, [], mb.faces)
    for p in me.polygons:
        p.use_smooth = True
    o = _obj("STUDIO_Cyclorama", me, col)
    o.rotation_euler = (0, 0, math.radians(-90))
    mat = bpy.data.materials.get("CT_Studio_Floor") or bpy.data.materials.new("CT_Studio_Floor")
    mat.use_nodes = True
    b = mat.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (0.075, 0.075, 0.08, 1)
    b.inputs["Roughness"].default_value = 0.38
    me.materials.append(mat)
    return o


def area_light(col, name, loc, target, size, energy, color=(1, 1, 1), shape="RECTANGLE", size_y=None):
    data = bpy.data.lights.get(name) or bpy.data.lights.new(name, "AREA")
    data.shape = shape
    data.size = size
    if size_y:
        data.size_y = size_y
    data.energy = energy
    data.color = color
    o = _obj(name, data, col)
    o.location = loc
    d = Vector(target) - Vector(loc)
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o


def lights(col, preset="studio"):
    for o in [o for o in col.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(o, do_unlink=True)
    if preset == "studio":
        area_light(col, "LGT_STUDIO_Top", (0, 0, 6.5), (0, 0, 0), 4.0, 1300, size_y=9.0)
        area_light(col, "LGT_STUDIO_Key", (-6.0, 5.0, 3.5), (0, 0, 0.8), 3.0, 900, size_y=1.5)
        area_light(col, "LGT_STUDIO_Rim", (6.0, -6.0, 3.0), (0, 0, 0.8), 3.0, 800, size_y=1.5)
        area_light(col, "LGT_STUDIO_Strip_L", (-5.0, 0.0, 1.6), (0, 0, 1.0), 0.4, 380, size_y=8.0)
        area_light(col, "LGT_STUDIO_Strip_R", (5.0, 0.0, 1.6), (0, 0, 1.0), 0.4, 380, size_y=8.0)
    elif preset == "exterior":
        sun = bpy.data.lights.get("LGT_STUDIO_Sun") or bpy.data.lights.new("LGT_STUDIO_Sun", "SUN")
        sun.energy = 4.0
        sun.angle = math.radians(1.5)
        o = _obj("LGT_STUDIO_Sun", sun, col)
        o.rotation_euler = (math.radians(50), 0, math.radians(-140))


def cameras(col):
    out = {}
    for name, (loc, tgt, lens, kind, oscale) in CAMERAS.items():
        data = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
        data.lens = lens
        data.type = kind
        if kind == "ORTHO":
            data.ortho_scale = oscale
        data.clip_start = 0.05
        data.clip_end = 300
        o = _obj(name, data, col)
        o.location = loc
        d = Vector(tgt) - Vector(loc)
        o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        if name == "CAM_Top":
            o.rotation_euler = (0, 0, -math.pi / 2)
        out[name] = o
    bpy.context.scene.camera = out["CAM_3Q_Front"]
    return out


def render_settings(engine="CYCLES", samples=128):
    sc = bpy.context.scene
    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.exposure = -0.6
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    if engine == "CYCLES":
        sc.cycles.device = "GPU"
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.max_bounces = 10
        sc.cycles.transmission_bounces = 10
        sc.cycles.glossy_bounces = 6


def build_all(M, preset="studio", hdri="studio.exr"):
    col = studio_collection()
    world(hdri)
    cyclorama(col, M)
    lights(col, preset)
    cams = cameras(col)
    render_settings()
    return cams
