"""Biblioteca de materiales físicos del Cybertruck (nodos de Blender, Principled BSDF).

Los parámetros base (color, metalicidad, rugosidad, transmisión, IOR) se exportan a glTF;
los detalles procedurales (cepillado, granulado, microvariación) solo existen en Blender
y el visor web los reinterpreta por nombre de material (ver web/src/materials.js).
"""

import bpy


def _node(nt, kind, loc, **props):
    n = nt.nodes.new(kind)
    n.location = loc
    for k, v in props.items():
        setattr(n, k, v)
    return n


def _inp(node, *names):
    for n in names:
        if n in node.inputs:
            return node.inputs[n]
    raise KeyError(names)


def base_material(name, color, metallic=0.0, roughness=0.5, **extra):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = _node(nt, "ShaderNodeOutputMaterial", (600, 0))
    bsdf = _node(nt, "ShaderNodeBsdfPrincipled", (200, 0))
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    _inp(bsdf, "Base Color").default_value = (*color, 1.0)
    _inp(bsdf, "Metallic").default_value = metallic
    _inp(bsdf, "Roughness").default_value = roughness
    for key, val in extra.items():
        sock = {
            "transmission": ("Transmission Weight", "Transmission"),
            "ior": ("IOR",),
            "coat": ("Coat Weight", "Clearcoat"),
            "coat_roughness": ("Coat Roughness", "Clearcoat Roughness"),
            "emission_strength": ("Emission Strength",),
            "anisotropic": ("Anisotropic",),
            "specular": ("Specular IOR Level", "Specular"),
            "sheen": ("Sheen Weight", "Sheen"),
            "alpha": ("Alpha",),
        }.get(key)
        if key == "emission":
            _inp(bsdf, "Emission Color", "Emission").default_value = (*val, 1.0)
            continue
        if sock:
            _inp(bsdf, *sock).default_value = val
    mat.diffuse_color = (*color, 1.0)
    mat.metallic = metallic
    mat.roughness = roughness
    return mat, nt, bsdf


def add_bump_noise(nt, bsdf, scale=200.0, strength=0.05, distance=0.0005, detail=4.0, rough_mix=None,
                   stretch=None, loc=(-600, -300)):
    """Ruido procedural para microrrelieve y variación de rugosidad (escala física)."""
    tc = _node(nt, "ShaderNodeTexCoord", (loc[0] - 400, loc[1]))
    src = tc.outputs["UV"] if stretch else tc.outputs["Object"]
    if stretch:
        mp = _node(nt, "ShaderNodeMapping", (loc[0] - 200, loc[1]))
        mp.inputs["Scale"].default_value = stretch
        nt.links.new(src, mp.inputs["Vector"])
        src = mp.outputs["Vector"]
    nz = _node(nt, "ShaderNodeTexNoise", loc)
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = detail
    nt.links.new(src, nz.inputs["Vector"])
    bump = _node(nt, "ShaderNodeBump", (loc[0] + 250, loc[1]))
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], _inp(bsdf, "Normal"))
    if rough_mix:
        lo, hi = rough_mix
        mr = _node(nt, "ShaderNodeMapRange", (loc[0] + 250, loc[1] + 220))
        mr.inputs["To Min"].default_value = lo
        mr.inputs["To Max"].default_value = hi
        nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], _inp(bsdf, "Roughness"))
    return nz


def stainless_steel():
    """Acero inoxidable laminado en frío del exoesqueleto (acabado satinado/cepillado).

    Referencias fotográficas: reflejo difuso y alargado en sentido longitudinal, sin
    efecto espejo; tono gris neutro ligeramente cálido. Rugosidad efectiva ~0,25-0,32.
    """
    mat, nt, bsdf = base_material("CT_Stainless_Steel", (0.62, 0.62, 0.61), 1.0, 0.28,
                                  anisotropic=0.55)
    # Tangente alineada con U (eje longitudinal del vehículo) para el cepillado
    tan = _node(nt, "ShaderNodeTangent", (-200, -500))
    tan.direction_type = "UV_MAP"
    nt.links.new(tan.outputs["Tangent"], _inp(bsdf, "Tangent"))
    # Microrrayado direccional: ruido muy estirado en U (rayas de ~0,1 mm a lo largo de Y)
    tc = _node(nt, "ShaderNodeTexCoord", (-1100, 100))
    mp = _node(nt, "ShaderNodeMapping", (-900, 100))
    mp.inputs["Scale"].default_value = (2.0, 1400.0, 1.0)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    nz = _node(nt, "ShaderNodeTexNoise", (-700, 100))
    nz.inputs["Scale"].default_value = 1.0
    nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.6
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    # Variación lenta de rugosidad entre zonas del panel (marcas de laminado)
    nz2 = _node(nt, "ShaderNodeTexNoise", (-700, 350))
    nz2.inputs["Scale"].default_value = 1.6
    nz2.inputs["Detail"].default_value = 2.0
    tc2 = _node(nt, "ShaderNodeTexCoord", (-900, 350))
    nt.links.new(tc2.outputs["Object"], nz2.inputs["Vector"])
    mix = _node(nt, "ShaderNodeMath", (-450, 250), operation="MULTIPLY_ADD")
    mix.inputs[1].default_value = 0.06
    mix.inputs[2].default_value = 0.22
    add = _node(nt, "ShaderNodeMath", (-250, 250), operation="MULTIPLY_ADD")
    add.inputs[1].default_value = 0.08
    nt.links.new(nz2.outputs["Fac"], mix.inputs[0])
    nt.links.new(nz.outputs["Fac"], add.inputs[0])
    nt.links.new(mix.outputs["Value"], add.inputs[2])
    nt.links.new(add.outputs["Value"], _inp(bsdf, "Roughness"))
    bump = _node(nt, "ShaderNodeBump", (-250, -250))
    bump.inputs["Strength"].default_value = 0.025
    bump.inputs["Distance"].default_value = 0.0001
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], _inp(bsdf, "Normal"))
    mat["web_preset"] = "stainless"
    return mat


def glass(name, tint, roughness=0.02, ior=1.52, preset="glass"):
    mat, nt, bsdf = base_material(name, tint, 0.0, roughness, transmission=1.0, ior=ior)
    mat.blend_method = "BLEND" if hasattr(mat, "blend_method") else None
    try:
        mat.surface_render_method = "BLENDED"
    except Exception:
        pass
    mat["web_preset"] = preset
    return mat


def emissive(name, color, strength, base=(0.9, 0.9, 0.9), roughness=0.15, preset="emissive"):
    mat, nt, bsdf = base_material(name, base, 0.0, roughness, emission=color, emission_strength=strength)
    mat["web_preset"] = preset
    return mat


def build_library():
    M = {}
    M["steel"] = stainless_steel()

    m, nt, b = base_material("CT_Plastic_Textured", (0.020, 0.021, 0.023), 0.0, 0.58)
    add_bump_noise(nt, b, scale=900.0, strength=0.12, distance=0.0003, rough_mix=(0.55, 0.70))
    m["web_preset"] = "plastic_textured"
    M["plastic_textured"] = m

    m, nt, b = base_material("CT_Plastic_Black", (0.018, 0.018, 0.02), 0.0, 0.45)
    m["web_preset"] = "plastic"
    M["plastic_black"] = m

    m, nt, b = base_material("CT_Plastic_Liner", (0.025, 0.025, 0.027), 0.0, 0.85)
    add_bump_noise(nt, b, scale=300.0, strength=0.2, distance=0.0008)
    m["web_preset"] = "plastic_rough"
    M["plastic_liner"] = m

    m, nt, b = base_material("CT_Black_Gloss", (0.01, 0.01, 0.012), 0.0, 0.06, coat=1.0, coat_roughness=0.03)
    m["web_preset"] = "black_gloss"
    M["black_gloss"] = m

    m, nt, b = base_material("CT_Anodized_Dark", (0.06, 0.062, 0.066), 1.0, 0.42)
    add_bump_noise(nt, b, scale=600.0, strength=0.04, distance=0.0002)
    m["web_preset"] = "anodized"
    M["anodized_dark"] = m

    m, nt, b = base_material("CT_Body_Ecoat", (0.20, 0.205, 0.21), 0.0, 0.55)
    m["web_preset"] = "ecoat"
    M["ecoat"] = m

    M["glass_windshield"] = glass("CT_Glass_Windshield", (0.86, 0.90, 0.89), 0.01, preset="glass_clear")
    M["glass_side"] = glass("CT_Glass_Side", (0.42, 0.45, 0.45), 0.015, preset="glass_tint")
    M["glass_roof"] = glass("CT_Glass_Roof", (0.10, 0.11, 0.115), 0.02, preset="glass_dark")
    m, nt, b = base_material("CT_Glass_Frit", (0.005, 0.005, 0.006), 0.0, 0.25)
    m["web_preset"] = "frit"
    M["glass_frit"] = m
    M["glass_lens"] = glass("CT_Lens_Clear", (0.95, 0.95, 0.95), 0.03, ior=1.49, preset="lens")
    M["glass_lens_red"] = glass("CT_Lens_Red", (0.75, 0.02, 0.02), 0.05, ior=1.49, preset="lens_red")
    M["glass_lens_smoke"] = glass("CT_Lens_Smoked", (0.08, 0.08, 0.085), 0.03, ior=1.49, preset="lens_smoke")
    m, nt, b = base_material("CT_Mirror_Glass", (0.95, 0.95, 0.95), 1.0, 0.02)
    m["web_preset"] = "mirror"
    M["mirror"] = m

    M["led_white"] = emissive("CT_LED_White", (1.0, 0.97, 0.92), 6.0, preset="led_white")
    M["led_red"] = emissive("CT_LED_Red", (1.0, 0.02, 0.01), 5.0, base=(0.4, 0.0, 0.0), preset="led_red")
    M["led_amber"] = emissive("CT_LED_Amber", (1.0, 0.45, 0.02), 3.0, base=(0.5, 0.25, 0.0), preset="led_amber")
    m, nt, b = base_material("CT_Reflector_Chrome", (0.85, 0.85, 0.85), 1.0, 0.12)
    m["web_preset"] = "chrome"
    M["reflector"] = m

    # Ruedas y frenos
    m, nt, b = base_material("CT_Tire_Rubber", (0.014, 0.014, 0.015), 0.0, 0.86)
    add_bump_noise(nt, b, scale=1500.0, strength=0.15, distance=0.0002, rough_mix=(0.75, 0.9))
    m["web_preset"] = "rubber"
    M["rubber"] = m
    m, nt, b = base_material("CT_Tire_Sidewall", (0.018, 0.018, 0.019), 0.0, 0.70)
    add_bump_noise(nt, b, scale=2500.0, strength=0.08, distance=0.0001)
    m["web_preset"] = "rubber_sidewall"
    M["rubber_side"] = m
    m, nt, b = base_material("CT_Wheel_Cover", (0.045, 0.047, 0.05), 0.0, 0.40, coat=0.4, coat_roughness=0.2)
    m["web_preset"] = "wheel_cover"
    M["wheel_cover"] = m
    m, nt, b = base_material("CT_Wheel_Alloy", (0.10, 0.10, 0.105), 1.0, 0.35)
    m["web_preset"] = "wheel_alloy"
    M["wheel_alloy"] = m
    m, nt, b = base_material("CT_Brake_Rotor", (0.42, 0.42, 0.41), 1.0, 0.45)
    add_bump_noise(nt, b, scale=400.0, strength=0.05, distance=0.0002, rough_mix=(0.38, 0.55))
    m["web_preset"] = "cast_iron"
    M["rotor"] = m
    m, nt, b = base_material("CT_Brake_Caliper", (0.05, 0.05, 0.055), 0.0, 0.35, coat=0.6, coat_roughness=0.2)
    m["web_preset"] = "caliper"
    M["caliper"] = m
    m, nt, b = base_material("CT_Steel_Zinc", (0.55, 0.56, 0.57), 1.0, 0.38)
    m["web_preset"] = "zinc"
    M["zinc"] = m

    # Mecánica
    m, nt, b = base_material("CT_Aluminium_Cast", (0.58, 0.58, 0.57), 1.0, 0.48)
    add_bump_noise(nt, b, scale=350.0, strength=0.08, distance=0.0003, rough_mix=(0.42, 0.56))
    m["web_preset"] = "aluminium_cast"
    M["alu_cast"] = m
    m, nt, b = base_material("CT_Steel_Black", (0.025, 0.025, 0.027), 0.6, 0.48)
    m["web_preset"] = "steel_black"
    M["steel_black"] = m
    m, nt, b = base_material("CT_Rubber_Bushing", (0.02, 0.02, 0.02), 0.0, 0.7)
    m["web_preset"] = "rubber"
    M["bushing"] = m
    m, nt, b = base_material("CT_Damper_Chrome", (0.8, 0.8, 0.8), 1.0, 0.1)
    m["web_preset"] = "chrome"
    M["chrome"] = m
    m, nt, b = base_material("CT_HV_Orange", (0.85, 0.28, 0.02), 0.0, 0.45)
    m["web_preset"] = "hv_orange"
    M["hv_orange"] = m
    m, nt, b = base_material("CT_Battery_Enclosure", (0.36, 0.37, 0.38), 0.85, 0.5)
    add_bump_noise(nt, b, scale=200.0, strength=0.04, distance=0.0002)
    m["web_preset"] = "battery"
    M["battery"] = m
    m, nt, b = base_material("CT_Coolant_Hose", (0.02, 0.02, 0.022), 0.0, 0.6)
    m["web_preset"] = "rubber"
    M["hose"] = m
    m, nt, b = base_material("CT_Copper", (0.85, 0.45, 0.28), 1.0, 0.3)
    m["web_preset"] = "copper"
    M["copper"] = m
    m, nt, b = base_material("CT_Cell_4680", (0.12, 0.13, 0.15), 0.6, 0.35)
    m["web_preset"] = "cell"
    M["cell"] = m

    # Interior (decoración Tactical Grey)
    m, nt, b = base_material("CT_Upholstery_Grey", (0.055, 0.056, 0.06), 0.0, 0.55, sheen=0.15)
    add_bump_noise(nt, b, scale=4000.0, strength=0.12, distance=0.0002, rough_mix=(0.5, 0.62))
    m["web_preset"] = "leather"
    M["leather"] = m
    m, nt, b = base_material("CT_Upholstery_Light", (0.16, 0.16, 0.165), 0.0, 0.6, sheen=0.2)
    add_bump_noise(nt, b, scale=4000.0, strength=0.12, distance=0.0002)
    m["web_preset"] = "leather_light"
    M["leather_light"] = m
    m, nt, b = base_material("CT_Interior_Plastic", (0.035, 0.036, 0.04), 0.0, 0.5)
    add_bump_noise(nt, b, scale=1800.0, strength=0.06, distance=0.0001)
    m["web_preset"] = "interior_plastic"
    M["int_plastic"] = m
    m, nt, b = base_material("CT_Interior_Tactical_Grey", (0.13, 0.135, 0.14), 0.0, 0.45)
    add_bump_noise(nt, b, scale=1500.0, strength=0.05, distance=0.0001)
    m["web_preset"] = "interior_grey"
    M["int_grey"] = m
    m, nt, b = base_material("CT_Headliner", (0.11, 0.11, 0.115), 0.0, 0.92, sheen=0.4)
    add_bump_noise(nt, b, scale=2500.0, strength=0.15, distance=0.0003)
    m["web_preset"] = "fabric"
    M["headliner"] = m
    m, nt, b = base_material("CT_Carpet", (0.03, 0.03, 0.032), 0.0, 0.95, sheen=0.5)
    add_bump_noise(nt, b, scale=3000.0, strength=0.3, distance=0.0008)
    m["web_preset"] = "carpet"
    M["carpet"] = m
    m, nt, b = base_material("CT_Aluminium_Trim", (0.6, 0.6, 0.6), 1.0, 0.3, anisotropic=0.4)
    m["web_preset"] = "aluminium_trim"
    M["alu_trim"] = m
    m, nt, b = base_material("CT_Screen", (0.004, 0.004, 0.005), 0.0, 0.05, coat=1.0, coat_roughness=0.02,
                             emission=(0.10, 0.13, 0.17), emission_strength=0.6)
    m["web_preset"] = "screen"
    M["screen"] = m
    m, nt, b = base_material("CT_Seatbelt", (0.03, 0.03, 0.033), 0.0, 0.8, sheen=0.3)
    m["web_preset"] = "fabric"
    M["seatbelt"] = m
    m, nt, b = base_material("CT_Composite_Bed", (0.045, 0.046, 0.048), 0.0, 0.7)
    add_bump_noise(nt, b, scale=700.0, strength=0.2, distance=0.0004, rough_mix=(0.62, 0.78))
    m["web_preset"] = "composite"
    M["composite"] = m
    m, nt, b = base_material("CT_Floor_Ground", (0.30, 0.30, 0.30), 0.0, 0.6)
    M["ground"] = m
    return M
