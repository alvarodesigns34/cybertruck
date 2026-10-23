"""Oclusión ambiental horneada para la web (auditoría del 20-10-2026, M-CT1).

El GLB no tenía ninguna: 0 materiales con textura de oclusión y ninguna primitiva con segundo juego de UV, y el visor
no tiene pasada de oclusión en pantalla. Sin ella los primeros planos se leen como maquetas de plástico.

Método (el de `spacex/blender/common/webfinish.py`, que ya usan el Model Y, el Porsche y la H2R):

* cada malla (una vez, aunque la compartan varios objetos) se desenvuelve con Smart UV Project en un segundo juego de
  UV llamado ``ao`` y recibe un cuadrado del atlas proporcional a su superficie, con el mismo tamaño de texel en todas;
* Cycles hornea la oclusión en el atlas y se conecta a cada material como textura de oclusión de glTF (en three.js,
  ``aoMap`` sobre el canal de UV 1), que solo atenúa la luz indirecta.

**Con el coche explosionado** (``explode = 1``): hornearlo montado sería un error en un modelo que se despieza, porque
cada pieza llevaría la sombra de vecinas que al explosionar ya no están (la auditoría lo advierte), y lo interior de
cada carcasa saldría negro. Explosionado, las carcasas se apartan más que su contenido y, con una distancia corta, cada
pieza se lleva sobre todo su propia oclusión: pliegues, juntas, rebajes. El contacto entre piezas montadas queda para
una oclusión en pantalla.

Los vidrios y las lentes (transmisión) no reciben oclusión y se ocultan mientras se hornea, para no oscurecer lo que
hay detrás. Las mallas que no tenían UV reciben antes la proyección por caja del proyecto (``export_web.prepare_meshes``),
para que su primer juego de UV no quede vacío.

Uso (Blender sin interfaz; en la nube, en CPU):

    blender -b blender/Cybertruck.blend --python blender/scripts/bake_ao.py -- <repo> [tamaño=4096] [muestras=32]

Hornea, exporta el GLB y el manifiesto y no guarda el .blend (el horneado se repite con este script).
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
import numpy as np  # noqa: E402

import build_explode as E  # noqa: E402
import export_web  # noqa: E402

AO_LAYER = "ao"
SKIP_PREFIXES = ("CT_Glass", "CT_Lens")


def _skip(o):
    return any(s.material and s.material.name.startswith(SKIP_PREFIXES) for s in o.material_slots)


def _shelf(sizes, size):
    order = sorted(range(len(sizes)), key=lambda i: -sizes[i])
    out, x, y, sh = [None] * len(sizes), 0.0, 0.0, 0.0
    lim = 1 - 6 / size
    for i in order:
        s = sizes[i]
        if x + s > lim:
            x, y, sh = 0.0, y + sh, 0.0
        if y + s > lim:
            return None
        out[i] = (x, y)
        x += s
        sh = max(sh, s)
    return out


def unwrap_atlas(objs, size):
    """Cada malla desenvuelta por separado y escalada a su cuadrado del atlas (texel igual en todas)."""
    uniq, seen = [], set()
    for o in objs:
        if o.data.name in seen or not o.data.polygons:
            continue
        seen.add(o.data.name)
        uniq.append(o)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    tiles = []
    for o in uniq:
        me = o.data
        if AO_LAYER not in me.uv_layers:
            me.uv_layers.new(name=AO_LAYER)
        me.uv_layers.active = me.uv_layers[AO_LAYER]
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.0, scale_to_bounds=False)
        bpy.ops.uv.select_all(action="SELECT")
        bpy.ops.uv.pack_islands(margin=0.003, rotate=True, shape_method="CONCAVE")
        bpy.ops.object.mode_set(mode="OBJECT")
        o.select_set(False)
        area = sum(p.area for p in me.polygons)
        uvd = me.uv_layers[AO_LAYER].data
        co = np.empty(len(uvd) * 2)
        uvd.foreach_get("uv", co)
        co = co.reshape(-1, 2)
        cov = 0.0
        for p in me.polygons:
            q = co[p.loop_start:p.loop_start + p.loop_total]
            cov += 0.5 * abs(np.sum(q[:, 0] * np.roll(q[:, 1], 1) - np.roll(q[:, 0], 1) * q[:, 1]))
        tiles.append((o, (area / max(cov, 1e-9)) ** 0.5))
    pad = 3.0 / size
    lo, hi = 0.0, 10.0
    for _ in range(40):
        k = (lo + hi) / 2
        if _shelf([t * k + pad for _, t in tiles], size) is None:
            hi = k
        else:
            lo = k
    corners = _shelf([t * lo + pad for _, t in tiles], size)
    for (o, t), (x, y) in zip(tiles, corners):
        uvd = o.data.uv_layers[AO_LAYER].data
        co = np.empty(len(uvd) * 2)
        uvd.foreach_get("uv", co)
        co = co.reshape(-1, 2)
        uvd.foreach_set("uv", (np.array([x, y]) + pad / 2 + co * t * lo).ravel())
        o.data.uv_layers.active = o.data.uv_layers[0]
    texel_mm = 1 / (lo * size) * 1000
    print(f"atlas de oclusión: {len(tiles)} mallas, texel ≈{texel_mm:.1f} mm")
    return uniq, texel_mm


def _occlusion_group():
    g = bpy.data.node_groups.get("glTF Material Output")
    if g is None:
        g = bpy.data.node_groups.new("glTF Material Output", "ShaderNodeTree")
        g.interface.new_socket("Occlusion", in_out="INPUT", socket_type="NodeSocketFloat")
        g.interface.new_socket("Thickness", in_out="INPUT", socket_type="NodeSocketFloat")
    return g


def bake(objs, size=4096, samples=32, distance=0.08, out_dir="/tmp"):
    hidden = [o for o in objs if _skip(o)]
    for o in hidden:
        o.hide_render = True
    baked, texel = unwrap_atlas([o for o in objs if o not in hidden], size)
    image = bpy.data.images.new("CT_AO_Atlas", size, size, alpha=False)
    image.colorspace_settings.name = "Non-Color"
    group = _occlusion_group()
    for m in {s.material for o in baked for s in o.material_slots if s.material}:
        if m.name.startswith(SKIP_PREFIXES):
            continue
        m.use_nodes = True
        nt = m.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.name = tex.label = "ao-bake"
        tex.image = image
        uvn = nt.nodes.new("ShaderNodeUVMap")
        uvn.uv_map = AO_LAYER
        nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tex.outputs["Color"], sep.inputs["Color"])
        g = nt.nodes.new("ShaderNodeGroup")
        g.node_tree = group
        nt.links.new(sep.outputs[0], g.inputs["Occlusion"])
        nt.nodes.active = tex
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = samples
    if s.world is None:
        s.world = bpy.data.worlds.new("bake-world")
    s.world.light_settings.distance = distance
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in baked:
        o.select_set(True)
    bpy.context.view_layer.objects.active = baked[0]
    bpy.ops.object.bake(type="AO", uv_layer=AO_LAYER, margin=8, use_clear=True)
    for o in hidden:
        o.hide_render = False
    path = os.path.join(out_dir, "CT_AO_Atlas.jpg")
    image.filepath_raw = path
    image.file_format = "JPEG"
    s.render.image_settings.quality = 90
    image.save()
    return {"meshes": len(baked), "texel_mm": round(texel, 2), "hidden": len(hidden), "atlas": path}


def run(repo, size=4096, samples=32):
    import time
    t0 = time.time()
    objs = [o for o in E.vehicle_objects() if o.type == "MESH"]
    # Solo el vehículo da sombra: el estudio (ciclorama, luces) fuera del horneado.
    studio = bpy.data.collections.get("STUDIO")
    if studio:
        for o in studio.all_objects:
            o.hide_render = True
    export_web.prepare_meshes(objs)
    E.set_explode(1.0)
    # El atlas va dentro del GLB: el JPEG intermedio no se versiona.
    info = bake(objs, size, samples, out_dir=tempfile.gettempdir())
    E.set_explode(0.0)
    res = export_web.export(os.path.join(repo, "web/models/cybertruck.glb"), os.path.join(repo, "web/models/cybertruck-manifest.json"))
    info.update(res, seconds=round(time.time() - t0))
    return info


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    repo = args[0] if args else os.getcwd()
    size = int(args[1]) if len(args) > 1 else 4096
    samples = int(args[2]) if len(args) > 2 else 32
    print("RESULT", run(repo, size, samples))
