"""Biblioteca de materiales físicos del Cybertruck (nodos de Blender, Principled BSDF).

Desde la versión 2 los detalles de superficie (cepillado del acero, granulado de plásticos,
grano de la piel, tejido, caucho, fundición...) proceden de texturas periódicas generadas por
`ct_textures.py` y conectadas con nodos que el exportador glTF reconoce:

    Coordenadas UV -> Mapping (escala = 1 / metros por repetición) -> Imagen
        imagen de rugosidad  -> Roughness          (metallicRoughnessTexture)
        imagen de normales   -> Normal Map -> Normal (normalTexture)
        imagen de color      -> Base Color          (baseColorTexture, cuando existe)

El nodo Mapping se exporta como KHR_texture_transform, de modo que la densidad de texel es la
misma en Blender y en el visor. La anisotropía del acero se exporta como
KHR_materials_anisotropy. El visor web solo ajusta parámetros por nombre (web/src/materials.js).
"""

import bpy
import ct_textures as TX


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
            "anisotropic_rotation": ("Anisotropic Rotation",),
            "specular": ("Specular IOR Level", "Specular"),
            "sheen": ("Sheen Weight", "Sheen"),
            "sheen_roughness": ("Sheen Roughness",),
            "alpha": ("Alpha",),
            "subsurface": ("Subsurface Weight",),
        }.get(key)
        if key == "emission":
            _inp(bsdf, "Emission Color", "Emission").default_value = (*val, 1.0)
            continue
        if key == "sheen_tint":
            _inp(bsdf, "Sheen Tint").default_value = (*val, 1.0)
            continue
        if key == "sheen":
            # Peso 1 con tinte = intensidad: equivalente en Cycles y exportable como sheenColorFactor
            _inp(bsdf, "Sheen Weight").default_value = 1.0
            _inp(bsdf, "Sheen Tint").default_value = (val, val, val, 1.0)
            continue
        if sock:
            _inp(bsdf, *sock).default_value = val
    mat.diffuse_color = (*color, 1.0)
    mat.metallic = metallic
    mat.roughness = roughness
    return mat, nt, bsdf


# Texturas cargadas una vez por construcción (ver build_library)
TEX = {}


def textured(nt, bsdf, key, rough=True, normal=True, color=False, normal_strength=1.0,
             tile=None, offset=(0.0, 0.0), rotation=0.0, loc=(-900, 0)):
    """Conecta las texturas generadas `key` al BSDF con una cadena exportable a glTF."""
    maps = TEX.get(key)
    if not maps:
        return None
    tile = tile or TX.TILE_M[key]
    tc = _node(nt, "ShaderNodeTexCoord", (loc[0] - 400, loc[1]))
    mp = _node(nt, "ShaderNodeMapping", (loc[0] - 200, loc[1]))
    mp.inputs["Scale"].default_value = (1.0 / tile, 1.0 / tile, 1.0)
    mp.inputs["Location"].default_value = (offset[0], offset[1], 0.0)
    mp.inputs["Rotation"].default_value = (0.0, 0.0, rotation)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    y = loc[1] + 300
    if rough and "rough" in maps:
        im = _node(nt, "ShaderNodeTexImage", (loc[0], y))
        im.image = maps["rough"]
        nt.links.new(mp.outputs["Vector"], im.inputs["Vector"])
        sep = _node(nt, "ShaderNodeSeparateColor", (loc[0] + 300, y))
        nt.links.new(im.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Green"], _inp(bsdf, "Roughness"))      # G = rugosidad
        nt.links.new(sep.outputs["Blue"], _inp(bsdf, "Metallic"))        # B = metalicidad
        y -= 300
    if normal and "normal" in maps:
        im = _node(nt, "ShaderNodeTexImage", (loc[0], y))
        im.image = maps["normal"]
        nt.links.new(mp.outputs["Vector"], im.inputs["Vector"])
        nm = _node(nt, "ShaderNodeNormalMap", (loc[0] + 300, y))
        nm.inputs["Strength"].default_value = normal_strength
        nt.links.new(im.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], _inp(bsdf, "Normal"))
        y -= 300
    if color and "color" in maps:
        im = _node(nt, "ShaderNodeTexImage", (loc[0], y))
        im.image = maps["color"]
        nt.links.new(mp.outputs["Vector"], im.inputs["Vector"])
        nt.links.new(im.outputs["Color"], _inp(bsdf, "Base Color"))
    return mp


def mat_tex(name, color, metallic, roughness, key, preset, rough=True, normal=True, color_map=False,
            normal_strength=1.0, tile=None, **extra):
    m, nt, b = base_material(name, color, metallic, roughness, **extra)
    textured(nt, b, key, rough=rough, normal=normal, color=color_map, normal_strength=normal_strength, tile=tile)
    m["web_preset"] = preset
    return m


def stainless_steel(name="CT_Stainless_Steel", tint=(0.62, 0.62, 0.61), offset=(0.0, 0.0)):
    """Acero inoxidable austenítico laminado en frío, sin pintar, con acabado satinado.

    El exoesqueleto se fabrica con chapa de acero inoxidable de gran espesor que se pliega pero no
    se embute (por eso las superficies son planas con aristas vivas). El acabado de fábrica es un
    satinado direccional: rayas finas longitudinales (eje U = Y del vehículo) que producen un
    reflejo alargado (anisotropía). Rugosidad efectiva ~0,25-0,33.
    """
    mat, nt, bsdf = base_material(name, tint, 1.0, 0.28, anisotropic=0.55)
    tan = _node(nt, "ShaderNodeTangent", (-200, -500))
    tan.direction_type = "UV_MAP"
    nt.links.new(tan.outputs["Tangent"], _inp(bsdf, "Tangent"))
    textured(nt, bsdf, "steel", normal_strength=0.22, offset=offset)
    mat["web_preset"] = "stainless"
    return mat


def glass(name, tint, roughness=0.02, ior=1.52, preset="glass"):
    mat, nt, bsdf = base_material(name, tint, 0.0, roughness, transmission=1.0, ior=ior)
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


def simple(name, color, metallic, roughness, preset, **extra):
    m, nt, b = base_material(name, color, metallic, roughness, **extra)
    m["web_preset"] = preset
    return m


def build_library():
    TEX.clear()
    TEX.update(TX.build_textures())
    M = {}
    # --- Exoesqueleto: tres variantes por panel (lotes de bobina y orientación del satinado)
    M["steel"] = stainless_steel()
    M["steel_b"] = stainless_steel("CT_Stainless_Steel_B", (0.605, 0.607, 0.600), (0.37, 0.11))
    M["steel_c"] = stainless_steel("CT_Stainless_Steel_C", (0.632, 0.630, 0.618), (0.71, 0.53))

    # --- Plásticos exteriores
    M["plastic_textured"] = mat_tex("CT_Plastic_Textured", (0.020, 0.021, 0.023), 0.0, 0.6, "plastic",
                                    "plastic_textured", normal_strength=0.22)
    M["plastic_black"] = simple("CT_Plastic_Black", (0.018, 0.018, 0.02), 0.0, 0.45, "plastic")
    M["plastic_liner"] = mat_tex("CT_Plastic_Liner", (0.025, 0.025, 0.027), 0.0, 0.85, "composite",
                                 "plastic_rough", tile=0.05)
    M["black_gloss"] = simple("CT_Black_Gloss", (0.01, 0.01, 0.012), 0.0, 0.06, "black_gloss",
                              coat=1.0, coat_roughness=0.03)
    M["anodized_dark"] = mat_tex("CT_Anodized_Dark", (0.06, 0.062, 0.066), 1.0, 0.42, "cast",
                                 "anodized", rough=False, normal_strength=0.3, tile=0.08)
    M["ecoat"] = mat_tex("CT_Body_Ecoat", (0.20, 0.205, 0.21), 0.0, 0.55, "cast", "ecoat",
                         rough=False, normal_strength=0.25)

    # --- Cristales (laminado y templado; tintes medidos por apariencia)
    M["glass_windshield"] = glass("CT_Glass_Windshield", (0.86, 0.90, 0.89), 0.01, preset="glass_clear")
    M["glass_side"] = glass("CT_Glass_Side", (0.42, 0.45, 0.45), 0.015, preset="glass_tint")
    M["glass_roof"] = glass("CT_Glass_Roof", (0.10, 0.11, 0.115), 0.02, preset="glass_dark")
    M["glass_frit"] = simple("CT_Glass_Frit", (0.005, 0.005, 0.006), 0.0, 0.25, "frit")
    M["glass_lens"] = glass("CT_Lens_Clear", (0.95, 0.95, 0.95), 0.03, ior=1.49, preset="lens")
    M["glass_lens_red"] = glass("CT_Lens_Red", (0.75, 0.02, 0.02), 0.05, ior=1.49, preset="lens_red")
    M["glass_lens_smoke"] = glass("CT_Lens_Smoked", (0.08, 0.08, 0.085), 0.03, ior=1.49, preset="lens_smoke")
    M["mirror"] = simple("CT_Mirror_Glass", (0.95, 0.95, 0.95), 1.0, 0.02, "mirror")

    # --- Iluminación
    M["led_white"] = emissive("CT_LED_White", (1.0, 0.97, 0.92), 6.0, preset="led_white")
    M["led_red"] = emissive("CT_LED_Red", (1.0, 0.02, 0.01), 5.0, base=(0.4, 0.0, 0.0), preset="led_red")
    M["led_amber"] = emissive("CT_LED_Amber", (1.0, 0.45, 0.02), 3.0, base=(0.5, 0.25, 0.0), preset="led_amber")
    M["reflector"] = simple("CT_Reflector_Chrome", (0.85, 0.85, 0.85), 1.0, 0.12, "chrome")
    M["lamp_housing"] = simple("CT_Lamp_Housing", (0.012, 0.012, 0.014), 0.0, 0.35, "plastic")
    M["led_pcb"] = simple("CT_LED_Board", (0.02, 0.05, 0.03), 0.2, 0.4, "plastic")

    # --- Ruedas y frenos
    M["rubber"] = mat_tex("CT_Tire_Rubber", (0.014, 0.014, 0.015), 0.0, 0.86, "rubber", "rubber",
                          color_map=True, normal_strength=0.9)
    M["rubber_side"] = mat_tex("CT_Tire_Sidewall", (0.018, 0.018, 0.019), 0.0, 0.70, "sidewall",
                               "rubber_sidewall", normal_strength=0.6)
    M["tire_letters"] = simple("CT_Tire_Lettering", (0.022, 0.022, 0.023), 0.0, 0.48, "rubber_letters")
    M["wheel_cover"] = mat_tex("CT_Wheel_Cover", (0.045, 0.047, 0.05), 0.0, 0.40, "plastic",
                               "wheel_cover", rough=False, normal_strength=0.15, coat=0.4, coat_roughness=0.2)
    M["wheel_cover_edge"] = simple("CT_Wheel_Cover_Edge", (0.30, 0.31, 0.32), 0.6, 0.35, "wheel_cover_edge")
    M["wheel_alloy"] = simple("CT_Wheel_Alloy", (0.10, 0.10, 0.105), 1.0, 0.35, "wheel_alloy")
    M["rotor"] = mat_tex("CT_Brake_Rotor", (0.42, 0.42, 0.41), 1.0, 0.45, "rotor", "cast_iron")
    M["caliper"] = simple("CT_Brake_Caliper", (0.05, 0.05, 0.055), 0.0, 0.35, "caliper",
                          coat=0.6, coat_roughness=0.2)
    M["brake_pad"] = mat_tex("CT_Brake_Pad", (0.08, 0.075, 0.07), 0.2, 0.8, "cast", "pad",
                             rough=False, normal_strength=1.0, tile=0.05)
    M["zinc"] = simple("CT_Steel_Zinc", (0.55, 0.56, 0.57), 1.0, 0.38, "zinc")
    M["fastener_black"] = simple("CT_Fastener_Black", (0.03, 0.03, 0.032), 0.8, 0.42, "fastener")
    M["valve_brass"] = simple("CT_Valve_Brass", (0.80, 0.62, 0.33), 1.0, 0.3, "brass")

    # --- Mecánica
    M["alu_cast"] = mat_tex("CT_Aluminium_Cast", (0.58, 0.58, 0.57), 1.0, 0.48, "cast", "aluminium_cast", normal_strength=0.15,
                            color_map=True)
    M["alu_forged"] = mat_tex("CT_Aluminium_Forged", (0.66, 0.66, 0.65), 1.0, 0.36, "cast", "aluminium_forged",
                              rough=False, normal_strength=0.15, tile=0.3)
    M["alu_machined"] = simple("CT_Aluminium_Machined", (0.80, 0.80, 0.79), 1.0, 0.22, "aluminium_machined",
                               anisotropic=0.4)
    M["steel_black"] = mat_tex("CT_Steel_Black", (0.025, 0.025, 0.027), 0.6, 0.48, "cast", "steel_black",
                               rough=False, normal_strength=0.15)
    M["steel_bare"] = simple("CT_Steel_Bare", (0.48, 0.48, 0.47), 1.0, 0.40, "steel_bare")
    M["bushing"] = mat_tex("CT_Rubber_Bushing", (0.02, 0.02, 0.02), 0.0, 0.7, "rubber", "rubber",
                           normal_strength=0.4)
    M["chrome"] = simple("CT_Damper_Chrome", (0.8, 0.8, 0.8), 1.0, 0.1, "chrome")
    M["hv_orange"] = simple("CT_HV_Orange", (0.85, 0.28, 0.02), 0.0, 0.45, "hv_orange")
    M["battery"] = mat_tex("CT_Battery_Enclosure", (0.36, 0.37, 0.38), 0.85, 0.5, "cast", "battery",
                           rough=False, normal_strength=0.2)
    M["hose"] = mat_tex("CT_Coolant_Hose", (0.02, 0.02, 0.022), 0.0, 0.6, "rubber", "rubber",
                        normal_strength=0.3)
    M["copper"] = simple("CT_Copper", (0.85, 0.45, 0.28), 1.0, 0.3, "copper")
    M["cell"] = simple("CT_Cell_4680", (0.12, 0.13, 0.15), 0.6, 0.35, "cell")
    M["foam_green"] = simple("CT_Battery_Foam", (0.18, 0.42, 0.10), 0.0, 0.85, "foam")
    M["mica"] = simple("CT_Mica_Sheet", (0.42, 0.36, 0.26), 0.1, 0.55, "mica")
    M["busbar_alu"] = simple("CT_Busbar_Aluminium", (0.75, 0.76, 0.77), 1.0, 0.3, "aluminium_machined")
    M["harness"] = mat_tex("CT_Harness_Tape", (0.012, 0.012, 0.013), 0.0, 0.75, "fabric", "fabric",
                           rough=False, normal_strength=0.8, tile=0.01)
    M["connector_grey"] = simple("CT_Connector_Grey", (0.12, 0.12, 0.13), 0.0, 0.45, "plastic")
    M["connector_blue"] = simple("CT_Connector_Blue", (0.05, 0.15, 0.55), 0.0, 0.4, "plastic")
    M["pcb_green"] = simple("CT_PCB", (0.03, 0.18, 0.08), 0.1, 0.35, "plastic")
    M["radiator"] = mat_tex("CT_Radiator_Core", (0.62, 0.62, 0.60), 1.0, 0.5, "fabric", "radiator",
                            rough=False, normal_strength=1.5, tile=0.004)

    # --- Interior (decoración Tactical Grey)
    M["leather"] = mat_tex("CT_Upholstery_Grey", (0.055, 0.056, 0.06), 0.0, 0.55, "leather", "leather",
                           color_map=True, normal_strength=0.7, tile=0.08, sheen=0.15)
    M["leather_light"] = mat_tex("CT_Upholstery_Light", (0.16, 0.16, 0.165), 0.0, 0.6, "leather",
                                 "leather_light", normal_strength=0.7, tile=0.08, sheen=0.2)
    M["stitch"] = simple("CT_Stitching", (0.10, 0.10, 0.105), 0.0, 0.7, "fabric", sheen=0.5)
    M["int_plastic"] = mat_tex("CT_Interior_Plastic", (0.035, 0.036, 0.04), 0.0, 0.5, "plastic",
                               "interior_plastic", normal_strength=0.5)
    M["int_grey"] = mat_tex("CT_Interior_Tactical_Grey", (0.13, 0.135, 0.14), 0.0, 0.45, "plastic",
                            "interior_grey", rough=False, normal_strength=0.35)
    M["headliner"] = mat_tex("CT_Headliner", (0.11, 0.11, 0.115), 0.0, 0.92, "fabric", "fabric",
                             normal_strength=0.8, sheen=0.4)
    M["carpet"] = mat_tex("CT_Carpet", (0.03, 0.03, 0.032), 0.0, 0.95, "carpet", "carpet",
                          color_map=True, normal_strength=1.0, sheen=0.5)
    M["alu_trim"] = simple("CT_Aluminium_Trim", (0.6, 0.6, 0.6), 1.0, 0.3, "aluminium_trim", anisotropic=0.4)
    M["screen"] = simple("CT_Screen", (0.004, 0.004, 0.005), 0.0, 0.05, "screen", coat=1.0,
                         coat_roughness=0.02, emission=(0.10, 0.13, 0.17), emission_strength=0.6)
    M["seatbelt"] = mat_tex("CT_Seatbelt", (0.03, 0.03, 0.033), 0.0, 0.8, "fabric", "fabric",
                            normal_strength=0.8, tile=0.008, sheen=0.3)
    M["speaker_mesh"] = mat_tex("CT_Speaker_Grille", (0.02, 0.02, 0.022), 0.4, 0.5, "fabric", "plastic",
                                rough=False, normal_strength=2.0, tile=0.006)
    M["rubber_seal"] = mat_tex("CT_Rubber_Seal_EPDM", (0.012, 0.012, 0.013), 0.0, 0.62, "sidewall",
                               "rubber", normal_strength=0.4)
    M["composite"] = mat_tex("CT_Composite_Bed", (0.045, 0.046, 0.048), 0.0, 0.7, "composite", "composite",
                             normal_strength=1.0)
    M["ground"] = simple("CT_Floor_Ground", (0.30, 0.30, 0.30), 0.0, 0.6, "ground")
    return M


# Asignación de variantes de acero por panel (lote/orientación de la bobina)
STEEL_VARIANTS = {
    "EXT_Door_FL_Skin": "steel_b", "EXT_Door_FR_Skin": "steel_b",
    "EXT_Door_RL_Skin": "steel_c", "EXT_Door_RR_Skin": "steel_c",
    "EXT_Fender_FL": "steel_c", "EXT_Fender_FR": "steel_c",
    "EXT_BedSide_L": "steel_b", "EXT_BedSide_R": "steel_b",
    "EXT_Tailgate": "steel_c",
}


def assign_steel_variants(M):
    """Asigna a cada panel de acero su variante (cambia el reflejo entre paneles contiguos)."""
    n = 0
    for name, key in STEEL_VARIANTS.items():
        o = bpy.data.objects.get(name)
        if o is None or o.type != "MESH":
            continue
        for i, m in enumerate(o.data.materials):
            if m is not None and m.name == "CT_Stainless_Steel":
                o.data.materials[i] = M[key]
                n += 1
    return n
