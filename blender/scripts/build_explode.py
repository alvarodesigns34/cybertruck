"""Vista explosionada reversible dentro de Blender.

Cada componente con metadatos `explode_dir` / `explode_dist` / `explode_stage` recibe tres
controladores (drivers) sobre `delta_location`:

    delta = dir * dist * smoothstep(t0, t1, explode)

donde `explode` es la propiedad personalizada de CYBERTRUCK_ROOT (0 = ensamblado, 1 = explosionado)
y [t0, t1] es la ventana temporal de la etapa lógica del componente. La transformación base
(`location`) nunca se modifica, por lo que el ensamblado se recupera exactamente en explode = 0 y
el resultado no depende del historial de movimientos del control (sin deriva acumulada).
La dirección se expresa en el espacio del padre; todos los conjuntos padre carecen de rotación,
de modo que coincide con la dirección de mundo registrada.
"""

import bpy
import ct_lib as L

# Ventanas de cada etapa (solapadas para un movimiento continuo)
STAGE_WINDOWS = {
    1: (0.00, 0.40),   # paneles exteriores y elementos de apertura
    2: (0.12, 0.52),   # conjuntos interiores
    3: (0.24, 0.64),   # estructura y bajos
    4: (0.36, 0.76),   # suspensión, ruedas y frenos
    5: (0.48, 0.88),   # batería y tren motriz
    6: (0.60, 1.00),   # componentes pequeños y herrajes
}


def vehicle_objects():
    top = bpy.data.collections.get("CYBERTRUCK")
    if not top:
        return []
    objs = set()
    for c in [top] + list(top.children_recursive):
        objs.update(c.objects)
    return sorted(objs, key=lambda o: o.name)


def clear_drivers(obj):
    if obj.animation_data:
        for fc in list(obj.animation_data.drivers):
            if fc.data_path == "delta_location":
                obj.animation_data.drivers.remove(fc)
    obj.delta_location = (0, 0, 0)


def setup_drivers():
    root = L.root()
    root["explode"] = 0.0
    root["explode_stage_windows"] = {str(k): list(v) for k, v in STAGE_WINDOWS.items()}
    n = 0
    for obj in vehicle_objects():
        clear_drivers(obj)
        if "explode_dir" not in obj.keys() or obj == root:
            continue
        d = list(obj["explode_dir"])
        dist = float(obj.get("explode_dist", 0.0))
        t0, t1 = STAGE_WINDOWS.get(int(obj.get("explode_stage", 1)), (0.0, 1.0))
        for i in range(3):
            if abs(d[i]) < 1e-6:
                continue
            fc = obj.driver_add("delta_location", i)
            drv = fc.driver
            drv.type = "SCRIPTED"
            var = drv.variables.new()
            var.name = "e"
            var.type = "SINGLE_PROP"
            var.targets[0].id_type = "OBJECT"
            var.targets[0].id = root
            var.targets[0].data_path = '["explode"]'
            drv.expression = f"{d[i] * dist:.5f}*smoothstep({t0:.3f}, {t1:.3f}, e)"
            n += 1
    return n


def set_explode(value):
    root = L.root()
    root["explode"] = float(value)
    root.update_tag()
    bpy.context.view_layer.update()


def verify_roundtrip(steps=(0.0, 0.33, 1.0, 0.5, 0.0, 1.0, 0.0), tol=1e-6):
    """Mueve el factor varias veces y comprueba que en 0 todo vuelve a su posición exacta."""
    base = {o.name: o.matrix_world.copy() for o in vehicle_objects()}
    worst = 0.0
    for v in steps:
        set_explode(v)
    set_explode(0.0)
    dg = bpy.context.evaluated_depsgraph_get()
    for o in vehicle_objects():
        m = o.evaluated_get(dg).matrix_world
        diff = max(abs(a - b) for ra, rb in zip(m, base[o.name]) for a, b in zip(ra, rb))
        worst = max(worst, diff)
    return {"objects": len(base), "max_deviation": worst, "ok": worst < tol}
