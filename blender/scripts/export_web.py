"""Exportación del Cybertruck para el visor web (glTF binario + manifiesto de componentes).

* Solo se exporta la jerarquía de CYBERTRUCK_ROOT (sin estudio, cámaras ni referencias).
* Los modificadores (espesor, biseles, normales ponderadas) se aplican en la exportación.
* Las propiedades personalizadas (explode_dir, explode_dist, explode_stage, explode_group,
  label_es, fidelity, system...) viajan como `extras` de cada nodo.
* Se exporta siempre en estado ensamblado (explode = 0).
* Conversión de ejes: Blender (+Y delante, +Z arriba) -> glTF (+Y arriba, -Z delante).
"""

import json
import os
import bpy
import build_explode as E
import ct_specs as S


def _textured(me):
    """¿Alguno de sus materiales lee una imagen? (sin UV, glTF le pone texCoord −1)."""
    for m in me.materials:
        if m and m.use_nodes and any(n.type == "TEX_IMAGE" and n.image for n in m.node_tree.nodes):
            return True
    return False


def _box_uv(me):
    """La proyección por caja de ct_lib.auto_uv (1 unidad UV = 1 m, U longitudinal), en las coordenadas
    de la propia malla: sirve para las mallas compartidas por varios objetos (ruedas, frenos)."""
    uvl = me.uv_layers.new(name="UVMap").data
    for p in me.polygons:
        n = p.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if ax == 0:
                u, v = co.y, co.z
            elif ax == 2:
                u, v = co.y, co.x
            else:
                u, v = co.x, co.z
            uvl[li].uv = (u, v)


def prepare_meshes(objs):
    """Antes de exportar (auditoría del 20-10-2026):

    * C21: las mallas texturadas sin UV (neumático, discos, pinzas, pastillas, bujes, protectores,
      tapacubos, tuercas y válvula, que son mallas compartidas creadas sin ct_lib.auto_uv) salían con
      texCoord −1: 17 errores del validador de Khronos, y sin sus texturas en la web. Reciben la
      proyección por caja del proyecto.
    * C24: las mallas que conservan el nombre temporal de build_montaje (``_tmp_isl.NNN``) toman el de
      su objeto, para que quien busque por nombre de malla las encuentre.
    """
    done, uv, renamed = set(), [], []
    for o in objs:
        if o.type != "MESH" or o.data in done:
            continue
        me = o.data
        done.add(me)
        if not me.uv_layers and me.polygons and _textured(me):
            _box_uv(me)
            uv.append(me.name)
        if me.name.startswith("_tmp") and me.users == 1:
            me.name = o.name
            renamed.append(o.name)
    return {"uv": uv, "renamed": renamed}


def export(glb_path, manifest_path, draco=True):
    E.set_explode(0.0)
    objs = E.vehicle_objects()
    prepared = prepare_meshes(objs)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    # Asegura visibilidad para la exportación
    for o in objs:
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects.get("CYBERTRUCK_ROOT")
    os.makedirs(os.path.dirname(glb_path), exist_ok=True)
    kw = dict(
        filepath=glb_path, export_format="GLB", use_selection=True, export_apply=True,
        export_extras=True, export_yup=True, export_cameras=False, export_lights=False,
        export_animations=False, export_materials="EXPORT", export_texcoords=True,
        export_normals=True, export_tangents=False,
    )
    if draco:
        kw.update(export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6,
                  export_draco_position_quantization=14, export_draco_normal_quantization=10,
                  export_draco_texcoord_quantization=12)
    bpy.ops.export_scene.gltf(**kw)
    # Manifiesto de componentes
    comps = []
    for o in objs:
        if o.name == "CYBERTRUCK_ROOT":
            continue
        d = o.get("explode_dir")
        comps.append({
            "name": o.name,
            "type": o.type,
            "parent": o.parent.name if o.parent else None,
            "system": o.get("system"),
            "label": o.get("label_es", o.name),
            "group": o.get("explode_group"),
            "stage": o.get("explode_stage"),
            "fidelity": o.get("fidelity"),
            "note": o.get("note_es"),
            "explode_dir_blender": list(d) if d is not None else None,
            "explode_dist": o.get("explode_dist"),
            "faces": len(o.data.polygons) if o.type == "MESH" else 0,
        })
    manifest = {
        "vehicle": "Tesla Cybertruck Cyberbeast (EE. UU., gama 2026)",
        "units": "metros",
        "axes": {"blender": "+X derecha, +Y delante, +Z arriba",
                 "gltf": "+X derecha, +Y arriba, -Z delante"},
        "stage_windows": {str(k): v for k, v in E.STAGE_WINDOWS.items()},
        "stages": {
            "1": "Paneles exteriores y elementos de apertura", "2": "Conjuntos interiores",
            "3": "Estructura de carrocería y bajos", "4": "Suspensión, ruedas y frenos",
            "5": "Batería y tren motriz", "6": "Componentes pequeños y herrajes"},
        "dimensions": {"length": S.LENGTH, "width_body": S.WIDTH_BODY, "width_mirrors": S.WIDTH_MIRRORS,
                       "height_medium": S.HEIGHT_MEDIUM, "wheelbase": S.WHEELBASE, "track": S.TRACK,
                       "ground_clearance_medium": S.GROUND_CLEAR_MEDIUM},
        "components": comps,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    return {"glb_mb": round(os.path.getsize(glb_path) / 1e6, 2), "components": len(comps), "prepared": prepared}
