"""Texturas físicas generadas por procedimiento (sin fotografías de terceros).

Cada textura se sintetiza con numpy filtrando ruido blanco en el dominio de la frecuencia,
de modo que el resultado es periódico (se repite sin costuras) por construcción. Las texturas
se guardan en `blender/textures/` y se empaquetan en el .blend; el exportador glTF las incluye
en el GLB (WebP), así que el aspecto llega también al visor web.

Convención de densidad de texel: las UV del proyecto valen 1 unidad = 1 m (ver ct_lib.auto_uv).
`TILE_M` indica cuántos metros cubre una repetición de cada textura; el nodo Mapping usa
escala = 1 / TILE_M (se exporta como KHR_texture_transform).

Mapas generados (todos en espacio lineal, «Non-Color», salvo los de color base):
  * *_rough.png  rugosidad ya escalada a su rango físico (se conecta tal cual).
  * *_normal.png mapa de normales en espacio tangente (convención OpenGL, +Y arriba).
  * *_color.png  color base (solo cuando el material lo necesita).
"""

import math
import os
import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TEX_DIR = os.path.normpath(os.path.join(HERE, "..", "textures"))

# Metros que cubre una repetición de cada textura (densidad de texel coherente)
TILE_M = {
    "steel": 0.40,        # 1024 px -> 0,39 mm/px (rayas de cepillado ~0,5-2 mm)
    "rubber": 0.08,       # 512 px -> 0,16 mm/px
    "sidewall": 0.06,
    "plastic": 0.05,      # granulado de plásticos texturizados (~0,1 mm/px)
    "leather": 0.12,      # grano de piel sintética
    "fabric": 0.012,      # tejido del guarnecido de techo y cinturones
    "carpet": 0.04,
    "cast": 0.20,         # superficie de fundición a presión
    "composite": 0.10,    # cubeta compuesta de la caja
    "rotor": 0.12,        # fundición gris torneada
}


# ---------------------------------------------------------------------------
# Ruido periódico
# ---------------------------------------------------------------------------
def _freq(n):
    f = np.fft.fftfreq(n) * n
    return np.meshgrid(f, f)          # (fx, fy) en ciclos por imagen


def spectral(n, sigma_x, sigma_y=None, seed=0, power=None):
    """Ruido gaussiano filtrado (periódico). sigma en ciclos/imagen; anisótropo si sigma_x != sigma_y.

    `power` (opcional) aplica un espectro 1/f^power en lugar del filtro gaussiano.
    """
    rng = np.random.default_rng(seed)
    w = rng.standard_normal((n, n))
    fx, fy = _freq(n)
    if power is not None:
        r = np.sqrt(fx ** 2 + fy ** 2)
        r[0, 0] = 1.0
        filt = 1.0 / r ** power
        filt[0, 0] = 0.0
    else:
        sy = sigma_x if sigma_y is None else sigma_y
        filt = np.exp(-0.5 * ((fx / sigma_x) ** 2 + (fy / sy) ** 2))
    out = np.real(np.fft.ifft2(np.fft.fft2(w) * filt))
    out -= out.mean()
    s = out.std()
    return out / s if s > 0 else out


def cells(n, count, seed=0, jitter=1.0):
    """Celdas de Voronoi periódicas: devuelve (F1, F2) en píxeles (distancias al 1.º y 2.º punto)."""
    rng = np.random.default_rng(seed)
    g = int(math.sqrt(count))
    gy, gx = np.meshgrid(np.arange(g), np.arange(g), indexing="ij")
    pts = (np.stack([gx.ravel(), gy.ravel()], 1) + 0.5 + (rng.random((g * g, 2)) - 0.5) * jitter) * (n / g)
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    f1 = np.full((n, n), 1e9)
    f2 = np.full((n, n), 1e9)
    for px, py in pts:
        dx = np.abs(xx - px)
        dy = np.abs(yy - py)
        dx = np.minimum(dx, n - dx)
        dy = np.minimum(dy, n - dy)
        d = np.sqrt(dx * dx + dy * dy)
        m = d < f1
        f2 = np.where(m, f1, np.minimum(f2, d))
        f1 = np.where(m, d, f1)
    return f1, f2


def blur(a, sigma_px):
    """Desenfoque gaussiano periódico (FFT)."""
    n = a.shape[0]
    fx, fy = _freq(n)
    s = n / (2 * math.pi * sigma_px)
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-0.5 * (fx ** 2 + fy ** 2) / s ** 2)))


def norm01(a):
    lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.5)
    return np.clip((a - lo) / (hi - lo + 1e-9), 0.0, 1.0)


def normal_from_height(h, strength):
    """Mapa de normales tangente (OpenGL) a partir de una altura periódica."""
    dx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * 0.5 * strength
    dy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * 0.5 * strength
    nx, ny, nz = -dx, -dy, np.ones_like(h)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    return np.stack([nx / ln * 0.5 + 0.5, ny / ln * 0.5 + 0.5, nz / ln * 0.5 + 0.5], -1)


# ---------------------------------------------------------------------------
# Recetas (alturas y rugosidades físicamente plausibles)
# ---------------------------------------------------------------------------
def recipe_steel(n=1024):
    """Acero inoxidable laminado en frío con acabado satinado: rayas finas longitudinales (eje U),
    bandas de laminado más anchas y microrrayas cruzadas muy débiles (manipulación)."""
    fine = spectral(n, sigma_x=2.0, sigma_y=420.0, seed=11)       # rayas a lo largo de U (eje x de la imagen)
    mid = spectral(n, sigma_x=1.0, sigma_y=60.0, seed=12)
    band = spectral(n, sigma_x=0.6, sigma_y=6.0, seed=13)
    cross = spectral(n, sigma_x=220.0, sigma_y=3.0, seed=14) * (spectral(n, 3.0, seed=15) > 1.6)
    h = fine * 0.62 + mid * 0.26 + band * 0.04 + cross * 0.08
    rough = 0.25 + 0.025 * norm01(band) + 0.035 * norm01(fine) + 0.015 * norm01(mid)
    return {"rough": rough, "normal": normal_from_height(h, 0.35)}


def recipe_rubber(n=512):
    """Caucho de banda de rodadura: microporosidad del molde y abrasión."""
    h = spectral(n, 90.0, seed=21) * 0.6 + spectral(n, 25.0, seed=22) * 0.4
    pores = (spectral(n, 120.0, seed=23) > 2.3).astype(float)
    h -= pores * 1.2
    rough = 0.80 + 0.12 * norm01(spectral(n, 8.0, seed=24))
    col = 0.030 + 0.012 * norm01(spectral(n, 6.0, seed=25))
    return {"rough": rough, "normal": normal_from_height(h, 1.6), "color": np.stack([col, col, col * 1.03], -1)}


def recipe_sidewall(n=512):
    """Flanco: acabado del molde algo más satinado con estrías radiales muy finas."""
    h = spectral(n, 4.0, 160.0, seed=31) * 0.5 + spectral(n, 60.0, seed=32) * 0.5
    rough = 0.66 + 0.10 * norm01(spectral(n, 5.0, seed=33))
    return {"rough": rough, "normal": normal_from_height(h, 0.9)}


def recipe_plastic(n=512):
    """Granulado tipo «piel de naranja» de plásticos texturizados (aletas, faldones, fascias)."""
    f1, f2 = cells(n, 900, seed=41)
    grain = norm01(blur(np.tanh((f2 - f1) / 3.0), 1.0))
    h = grain * 0.8 + spectral(n, 70.0, seed=42) * 0.15
    rough = 0.52 + 0.16 * (1.0 - grain)
    return {"rough": rough, "normal": normal_from_height(h, 2.2)}


def recipe_leather(n=1024):
    """Piel sintética (Tactical Grey): poros y pliegues de grano irregular."""
    f1, f2 = cells(n, 1300, seed=51)
    ridge = norm01(blur(np.tanh((f2 - f1) / 3.5), 1.2))    # granos abombados con surcos en los bordes
    wr = spectral(n, 4.0, seed=52)
    h = np.sqrt(ridge) * 0.85 + wr * 0.08 + spectral(n, 200.0, seed=53) * 0.05
    rough = 0.42 + 0.20 * (1.0 - ridge) + 0.04 * norm01(wr)
    col = 0.050 + 0.012 * norm01(spectral(n, 3.0, seed=54)) + 0.006 * ridge
    return {"rough": rough, "normal": normal_from_height(h, 2.6),
            "color": np.stack([col, col * 1.01, col * 1.08], -1)}


def recipe_fabric(n=512):
    """Tejido de calada (guarnecido de techo, cinturón): trama y urdimbre."""
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    k = 2 * math.pi * 32 / n
    warp = np.sin(xx * k) * (np.sin(yy * k * 0.5) > 0)
    weft = np.sin(yy * k) * (np.sin(xx * k * 0.5) <= 0)
    h = norm01(np.abs(warp) + np.abs(weft)) + spectral(n, 40.0, seed=61) * 0.08
    rough = 0.85 + 0.1 * norm01(spectral(n, 30.0, seed=62))
    return {"rough": rough, "normal": normal_from_height(h, 1.5)}


def recipe_carpet(n=512):
    """Moqueta de bucle cortado: fibras de alta frecuencia con mechones."""
    h = spectral(n, 180.0, seed=71) * 0.6 + spectral(n, 40.0, seed=72) * 0.4
    rough = 0.88 + 0.1 * norm01(spectral(n, 10.0, seed=73))
    col = 0.026 + 0.012 * norm01(h)
    return {"rough": rough, "normal": normal_from_height(h, 2.0), "color": np.stack([col, col, col * 1.04], -1)}


def recipe_cast(n=512):
    """Aluminio fundido a presión (piezas de gran formato): piel de fundición, poros y marcas de molde."""
    h = spectral(n, 70.0, seed=81) * 0.6 + spectral(n, 8.0, seed=82) * 0.06
    pits = (spectral(n, 110.0, seed=83) > 2.6).astype(float)
    flow = spectral(n, 1.5, 12.0, seed=84)
    h -= pits * 1.0
    rough = 0.44 + 0.14 * norm01(spectral(n, 6.0, seed=85)) + 0.05 * pits
    col = 0.55 + 0.06 * norm01(flow) - 0.04 * pits
    return {"rough": rough, "normal": normal_from_height(h, 1.2), "color": np.stack([col, col, col * 0.985], -1)}


def recipe_composite(n=512):
    """Cubeta de material compuesto de la caja: superficie gofrada mate."""
    f1, f2 = cells(n, 400, seed=91)
    h = norm01(f1) * 0.6 + spectral(n, 60.0, seed=92) * 0.2
    rough = 0.66 + 0.14 * norm01(h)
    return {"rough": rough, "normal": normal_from_height(h, 1.4)}


def recipe_rotor(n=512):
    """Disco de freno de fundición gris: torneado concéntrico aproximado como rayado en U."""
    h = spectral(n, 1.5, 250.0, seed=101) * 0.7 + spectral(n, 30.0, seed=102) * 0.3
    rough = 0.36 + 0.14 * norm01(spectral(n, 2.0, 40.0, seed=103))
    return {"rough": rough, "normal": normal_from_height(h, 0.8)}


# ---------------------------------------------------------------------------
# Versión 4: recetas del hiperrealismo (interior de los conjuntos y acabados)
# ---------------------------------------------------------------------------
def _draw_rect(a, x0, y0, x1, y1, val, mode="max"):
    n = a.shape[0]
    xs = np.arange(int(x0), int(x1) + 1) % n
    ys = np.arange(int(y0), int(y1) + 1) % n
    if mode == "max":
        a[np.ix_(ys, xs)] = np.maximum(a[np.ix_(ys, xs)], val)
    else:
        a[np.ix_(ys, xs)] = val


def recipe_pcb(n=1024):
    """Placa de circuito impreso: máscara de soldadura verde, pistas de cobre bajo la máscara (rectas y a 45°),
    pads estañados, vías y serigrafía blanca. 1 px ≈ 0,08 mm."""
    rng = np.random.default_rng(301)
    trace = np.zeros((n, n))
    pads = np.zeros((n, n))
    silk = np.zeros((n, n))
    vias = np.zeros((n, n))
    for _ in range(420):
        x, y = rng.integers(0, n, 2)
        w = rng.choice((2, 3, 4, 6))
        for _seg in range(rng.integers(2, 6)):
            d = rng.choice(4)
            ln = int(rng.integers(20, 160))
            if d == 0:
                _draw_rect(trace, x, y - w // 2, x + ln, y + w // 2, 1.0)
                x += ln
            elif d == 1:
                _draw_rect(trace, x - w // 2, y, x + w // 2, y + ln, 1.0)
                y += ln
            else:
                sg = 1 if d == 2 else -1
                for k in range(ln // 2):
                    _draw_rect(trace, x + k - w // 2, y + sg * k - w // 2, x + k + w // 2, y + sg * k + w // 2, 1.0)
                x += ln // 2
                y += sg * (ln // 2)
        if rng.random() < 0.6:
            _draw_rect(vias, x - 4, y - 4, x + 4, y + 4, 1.0)
    for _ in range(160):
        x, y = rng.integers(0, n, 2)
        cols, rows = rng.integers(1, 9), rng.integers(1, 3)
        pw, ph = rng.choice(((8, 14), (12, 6), (6, 6), (16, 10)))
        for i in range(cols):
            for j in range(rows):
                _draw_rect(pads, x + i * (pw + 5), y + j * (ph + 30), x + i * (pw + 5) + pw, y + j * (ph + 30) + ph, 1.0)
    for _ in range(90):
        x, y = rng.integers(0, n, 2)
        L_ = int(rng.integers(12, 60))
        for k in range(0, L_, 7):
            if rng.random() < 0.8:
                _draw_rect(silk, x + k, y, x + k + 4, y + 7, 1.0)
        if rng.random() < 0.3:
            _draw_rect(silk, x - 4, y - 4, x + L_ + 4, y - 3, 1.0)
            _draw_rect(silk, x - 4, y + 10, x + L_ + 4, y + 11, 1.0)
    trace = np.clip(blur(trace, 0.7), 0, 1)
    h = trace * 0.5 + pads * 0.7 + silk * 0.25 - vias * 0.6 + spectral(n, 120.0, seed=302) * 0.02
    mask = np.array([0.020, 0.140, 0.055])
    copper_under = np.array([0.045, 0.200, 0.065])
    tin = np.array([0.72, 0.72, 0.70])
    white = np.array([0.80, 0.80, 0.78])
    col = mask[None, None, :] * (1 - trace[..., None]) + copper_under[None, None, :] * trace[..., None]
    col = col * (1 - pads[..., None]) + tin[None, None, :] * pads[..., None]
    col = col * (1 - silk[..., None]) + white[None, None, :] * silk[..., None]
    col = col * (1 - vias[..., None] * 0.6)
    rough = 0.30 + 0.06 * norm01(spectral(n, 6.0, seed=303)) + 0.25 * silk - 0.10 * pads
    metal = np.clip(pads, 0, 1)
    return {"rough": rough, "normal": normal_from_height(h, 1.4), "color": col, "metal": metal}


def recipe_foam(n=512):
    """Espuma de poliuretano moldeado de celda abierta (superficie de corte con poros)."""
    f1, f2 = cells(n, 2500, seed=311)
    wall = norm01(blur(np.tanh((f2 - f1) / 2.0), 0.8))
    pores = (f1 > np.percentile(f1, 70)).astype(float)
    h = wall * 0.7 - pores * 0.6 + spectral(n, 30.0, seed=312) * 0.1
    rough = 0.90 + 0.08 * norm01(h)
    col = 0.55 + 0.06 * norm01(spectral(n, 4.0, seed=313)) - 0.10 * pores
    return {"rough": rough, "normal": normal_from_height(h, 2.2),
            "color": np.stack([col * 1.0, col * 0.80, col * 0.42], -1)}


def recipe_felt(n=512):
    """Fieltro no tejido (aislantes NVH, guarnecidos ocultos): fibras cortas orientadas al azar."""
    rng = np.random.default_rng(321)
    h = np.zeros((n, n))
    for _ in range(5000):
        x, y = rng.integers(0, n, 2)
        a = rng.random() * math.pi
        ln = rng.integers(8, 30)
        for k in range(ln):
            h[int(y + k * math.sin(a)) % n, int(x + k * math.cos(a)) % n] += 1.0
    h = blur(h, 0.6) + spectral(n, 20.0, seed=322) * 0.3
    rough = 0.92 + 0.06 * norm01(h)
    return {"rough": rough, "normal": normal_from_height(norm01(h), 1.6)}


def recipe_machined(n=512):
    """Aluminio y acero mecanizados o rectificados: marcas de herramienta paralelas finas y regulares."""
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    marks = np.sin(yy * 2 * math.pi * 96 / n + spectral(n, 2.0, seed=331) * 0.6)
    h = marks * 0.35 + spectral(n, 1.5, 300.0, seed=332) * 0.5 + spectral(n, 80.0, seed=333) * 0.06
    rough = 0.16 + 0.06 * norm01(spectral(n, 1.0, 40.0, seed=334)) + 0.03 * norm01(marks)
    return {"rough": rough, "normal": normal_from_height(h, 0.5)}


def recipe_zinc(n=512):
    """Recubrimiento de zinc-níquel de la tornillería: textura fina y velado irregular."""
    h = spectral(n, 120.0, seed=341) * 0.5 + spectral(n, 12.0, seed=342) * 0.2
    rough = 0.30 + 0.14 * norm01(spectral(n, 5.0, seed=343)) + 0.05 * norm01(h)
    col = 0.54 + 0.05 * norm01(spectral(n, 3.0, seed=344))
    return {"rough": rough, "normal": normal_from_height(h, 0.6), "color": np.stack([col, col * 1.01, col * 1.03], -1)}


# Metalicidad codificada en el canal B del mapa de rugosidad (coherente con su uso en ct_materials)
METAL = {"steel": 1.0, "cast": 1.0, "rotor": 1.0, "machined": 1.0, "zinc": 1.0}

RECIPES = {
    "steel": (recipe_steel, 1024), "rubber": (recipe_rubber, 512), "sidewall": (recipe_sidewall, 512),
    "plastic": (recipe_plastic, 512), "leather": (recipe_leather, 1024), "fabric": (recipe_fabric, 512),
    "carpet": (recipe_carpet, 512), "cast": (recipe_cast, 512), "composite": (recipe_composite, 512),
    "rotor": (recipe_rotor, 512),
    "pcb": (recipe_pcb, 1024), "foam": (recipe_foam, 512), "felt": (recipe_felt, 512),
    "machined": (recipe_machined, 512), "zinc": (recipe_zinc, 512),
}
TILE_M.update({"pcb": 0.08, "foam": 0.03, "felt": 0.03, "machined": 0.03, "zinc": 0.02})


# ---------------------------------------------------------------------------
# Imágenes de Blender
# ---------------------------------------------------------------------------
def _to_image(name, arr, colorspace="Non-Color"):
    """Crea/actualiza una imagen de Blender a partir de un array (n, n) o (n, n, 3) en [0, 1]."""
    n = arr.shape[0]
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], -1)
    rgba = np.concatenate([np.clip(arr, 0, 1), np.ones((n, n, 1))], -1).astype(np.float32)
    tmp = bpy.data.images.new("__tmp_tex", n, n, alpha=False, float_buffer=False)
    tmp.colorspace_settings.name = colorspace
    tmp.pixels.foreach_set(rgba.ravel())
    os.makedirs(TEX_DIR, exist_ok=True)
    path = os.path.join(TEX_DIR, name + ".webp")
    # WebP con pérdida ligera: ~10 veces menor que PNG y sin artefactos visibles en estos mapas
    tmp.filepath_raw = path
    tmp.file_format = "WEBP"
    tmp.save(filepath=path, quality=92)
    bpy.data.images.remove(tmp)
    return load_image(name, path, colorspace)


def load_image(name, path, colorspace):
    """Carga (o recarga) una textura externa con ruta relativa al .blend (sin empaquetar)."""
    img = bpy.data.images.get(name)
    if img is None:
        img = bpy.data.images.load(path, check_existing=False)
        img.name = name
    else:
        if img.packed_file is not None:
            img.unpack(method="REMOVE")
        img.source = "FILE"
        img.filepath = path
        img.reload()
    if bpy.data.filepath:
        try:
            img.filepath = bpy.path.relpath(path)
        except ValueError:
            pass
    img.colorspace_settings.name = colorspace
    return img


def _srgb(c):
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(np.clip(c, 0, None), 1 / 2.4) - 0.055)


def build_textures(force=False, force_keys=()):
    """Genera (o reutiliza) todas las texturas. Devuelve {clave: {mapa: imagen}}.

    `force_keys`: claves que se regeneran aunque ya existan (tras cambiar su receta).
    """
    out = {}
    for key, (fn, n) in RECIPES.items():
        names = {m: f"T_{key}_{m}" for m in ("rough", "normal", "color")}
        paths = {m: os.path.join(TEX_DIR, nm + ".webp") for m, nm in names.items()}
        if not (force or key in force_keys) and os.path.exists(paths["normal"]):
            out[key] = {m: load_image(names[m], p, "sRGB" if m == "color" else "Non-Color")
                        for m, p in paths.items() if os.path.exists(p)}
            continue
        maps = fn(n)
        # Canales según glTF (metallicRoughnessTexture): G = rugosidad, B = metalicidad
        r = maps["rough"]
        metal = maps.get("metal", np.full_like(r, METAL.get(key, 0.0)))
        orm = np.stack([np.ones_like(r), r, metal], -1)
        res = {"rough": _to_image(names["rough"], orm),
               "normal": _to_image(names["normal"], maps["normal"])}
        if "color" in maps:
            # el color base se guarda en sRGB (convención glTF)
            res["color"] = _to_image(names["color"], _srgb(maps["color"]), colorspace="sRGB")
        out[key] = res
    return out
