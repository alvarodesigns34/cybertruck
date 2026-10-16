"""Orquestador de la construcción completa del Cybertruck en la escena de Blender.

Uso desde Blender (consola de Python o Blender MCP):

    import sys; sys.path.insert(0, r"<repo>/blender/scripts")
    import build_all; build_all.run(parts=("body", "wheels", ...))

Solo se elimina y regenera el contenido de la colección «CYBERTRUCK». Cualquier otro
contenido de la escena se conserva (los objetos iniciales se trasladan a la colección
«ESCENA_ORIGINAL», excluida de la capa de vista, sin borrarlos).
"""

import importlib
import sys
import bpy

MODULES = ["ct_specs", "ct_lib", "ct_parts", "ct_textures", "ct_materials", "build_body", "build_wheels",
           "build_lights", "build_details", "build_exterior", "build_structure", "build_interior",
           "build_interior_detail", "build_mechanics", "build_chassis", "build_scene", "build_explode"]


def reload_modules():
    for name in MODULES:
        if name in sys.modules:
            importlib.reload(sys.modules[name])


def setup_scene():
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.length_unit = "METERS"
    sc.unit_settings.scale_length = 1.0
    # Conserva los objetos que ya existían en la escena
    keep = [o for o in sc.objects if not any(c.name == "CYBERTRUCK" or c.name in _ct_children()
                                             for c in o.users_collection)]
    if keep:
        orig = bpy.data.collections.get("ESCENA_ORIGINAL") or bpy.data.collections.new("ESCENA_ORIGINAL")
        if orig.name not in [c.name for c in sc.collection.children]:
            sc.collection.children.link(orig)
        for o in keep:
            if o.name.startswith(("CAM_", "LGT_STUDIO", "STUDIO_")):
                continue
            for c in list(o.users_collection):
                if c.name in ("ESCENA_ORIGINAL", "STUDIO"):
                    continue
                c.objects.unlink(o)
            if orig not in o.users_collection:
                orig.objects.link(o)
        lc = bpy.context.view_layer.layer_collection.children.get("ESCENA_ORIGINAL")
        if lc:
            lc.exclude = True
    empty = bpy.data.collections.get("Collection")
    if empty and not empty.objects and not empty.children:
        bpy.data.collections.remove(empty)


def _ct_children():
    top = bpy.data.collections.get("CYBERTRUCK")
    if not top:
        return set()
    names = set()
    stack = [top]
    while stack:
        c = stack.pop()
        names.add(c.name)
        stack.extend(c.children)
    return names


def clear_vehicle(systems=None):
    """Elimina los objetos generados (todo o solo algunas colecciones de sistema)."""
    top = bpy.data.collections.get("CYBERTRUCK")
    if not top:
        return 0
    n = 0
    cols = [c for c in top.children_recursive] + [top]
    for c in cols:
        if systems is not None and c.name not in systems:
            continue
        for o in list(c.objects):
            if systems is None or o.name != "CYBERTRUCK_ROOT":
                data = o.data
                bpy.data.objects.remove(o, do_unlink=True)
                if data is not None and getattr(data, "users", 1) == 0 and isinstance(data, bpy.types.Mesh):
                    bpy.data.meshes.remove(data)
                n += 1
    return n


def run(parts=("body",), clear=True):
    reload_modules()
    import ct_lib as L
    import ct_materials
    setup_scene()
    if clear:
        clear_vehicle()
    L.root()
    M = ct_materials.build_library()
    stats = {}
    if "body" in parts:
        import build_body
        build_body.build_all(M)
        ct_materials.assign_steel_variants(M)
    if "wheels" in parts:
        import build_wheels
        build_wheels.build_all(M)
    if "lights" in parts:
        import build_lights
        build_lights.build_all(M)
    if "details" in parts:
        import build_details
        build_details.build_all(M)
        import build_exterior
        build_exterior.build_all(M)
    if "interior" in parts:
        import build_interior
        build_interior.build_all(M)
        import build_interior_detail
        build_interior_detail.build_all(M)
    if "chassis" in parts:
        import build_chassis
        build_chassis.build_all(M)
    if "explode" in parts:
        import build_explode
        build_explode.setup_drivers()
    if "scene" in parts:
        import build_scene
        build_scene.build_all(M)
    bpy.context.view_layer.update()
    objs = [o for o in bpy.data.objects if any(c.name in _ct_children() for c in o.users_collection)]
    stats["objects"] = len(objs)
    stats["meshes"] = sum(1 for o in objs if o.type == "MESH")
    return stats
