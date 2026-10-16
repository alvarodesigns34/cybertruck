"""Iluminación exterior del Cybertruck.

[V] Existencia y denominación de piezas: manual de servicio (Lightbar - Front, Headlamp Assembly,
    Tail Lamp - Body Side, Lamp - Reverse, Lamp - Rear Marker, Lamp - License Plate,
    Lamp - Tailgate, Top Applique - Tailgate).
[R] Barra de luz delantera a lo ancho de ~86 % de la anchura, siguiendo la arista superior del
    frontal (vista frontal oficial: sube ~5 cm hacia los extremos).
[A] Faros: módulos alojados tras los extremos de la barra de luz (procedimiento de servicio:
    se desmontan desde el frunk, sobre la fascia). Formas internas aproximadas.
"""

import math
from mathutils import Vector
import ct_specs as S
import ct_lib as L
import build_body as B


def _face_pt(hw, z, fwd=0.0):
    """Punto sobre el frontal (facetas) en semianchura con signo y altura z."""
    h = abs(hw)
    return (hw, B.face_y(h) - B.face_lean(z) + fwd, z)


def _strip_on_face(mb, hws, z_of, half_h, fwd, mat=0, depth=0.012):
    """Tira (caja fina) que sigue las facetas del frontal."""
    rows_f, rows_b = [], []
    for hw in hws:
        zc = z_of(abs(hw))
        rows_f.append((_face_pt(hw, zc - half_h, fwd), _face_pt(hw, zc + half_h, fwd)))
        rows_b.append((_face_pt(hw, zc - half_h, fwd - depth), _face_pt(hw, zc + half_h, fwd - depth)))
    for i in range(len(hws) - 1):
        (a0, a1), (b0, b1) = rows_f[i], rows_f[i + 1]
        mb.face([a0, b0, b1, a1], mat, want=(0, 1, 0))
        (c0, c1), (d0, d1) = rows_b[i], rows_b[i + 1]
        mb.face([a1, b1, d1, c1], mat, want=(0, 0, 1))
        mb.face([a0, b0, d0, c0], mat, want=(0, 0, -1))
    for idx, sgn in ((0, -1), (-1, 1)):
        (a0, a1), (c0, c1) = rows_f[idx], rows_b[idx]
        mb.face([a0, a1, c1, c0], mat, want=(sgn, 0, 0))


def lightbar_center_z(h):
    return B.face_top_z(h) - 0.028


def build_front(M):
    objs = []
    hc, _ = B.corner_top()
    hw_end = min(0.88, hc - 0.03)
    base = [0.0, 0.2, 0.377, 0.5, 0.622, 0.75, hw_end]
    hws = [-h for h in reversed(base)] + base[1:]
    mb = L.MeshBuilder()
    _strip_on_face(mb, hws, lightbar_center_z, 0.0045, 0.002, 0, depth=0.008)
    led = mb.build("LGT_Front_Lightbar_LED", "LIGHTING", M["led_white"])
    L.explode(led, (0, 1, 0.2), 0.30, 6, "Iluminación", "Barra de luz delantera (DRL LED)", "R")
    objs.append(led)
    mb = L.MeshBuilder()
    _strip_on_face(mb, hws, lightbar_center_z, 0.012, 0.007, 0, depth=0.012)
    lens = mb.build("LGT_Front_Lightbar_Lens", "LIGHTING", M["glass_lens"])
    L.set_smooth_by_angle(lens, 30)
    L.explode(lens, (0, 1, 0.2), 0.45, 6, "Iluminación", "Lente de la barra de luz delantera", "R")
    objs.append(lens)
    # Carcasa negra (embellecedor de la barra de luz)
    mb = L.MeshBuilder()
    _strip_on_face(mb, hws, lightbar_center_z, 0.016, 0.003, 0, depth=0.040)
    hous = mb.build("LGT_Front_Lightbar_Housing", "LIGHTING", M["plastic_black"])
    L.explode(hous, (0, 1, 0.2), 0.20, 6, "Iluminación", "Embellecedor y soporte de la barra de luz", "R")
    objs.append(hous)
    # Faros (detrás de los extremos de la barra de luz)
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        for k, h in enumerate((0.48, 0.60, 0.72)):
            zc = lightbar_center_z(h) - 0.004
            c = Vector(_face_pt(s * h, zc, -0.03))
            L.lathe(mb, [(0.0, 0.0), (0.016, 0.0), (0.020, -0.010), (0.024, -0.050), (0.0, -0.052)],
                    c, (0, 1, 0), 20, 0)
        # cuerpo del faro
        h0, h1 = 0.42, 0.80
        zc0, zc1 = lightbar_center_z(h0), lightbar_center_z(h1)
        p = [_face_pt(s * h0, zc0 - 0.03, -0.035), _face_pt(s * h1, zc1 - 0.03, -0.035),
             _face_pt(s * h1, zc1 + 0.02, -0.035), _face_pt(s * h0, zc0 + 0.02, -0.035)]
        back = [(q[0], q[1] - 0.10, q[2]) for q in p]
        mb.face(p, 1)
        mb.face(back, 1)
        for i in range(4):
            j = (i + 1) % 4
            mb.face([p[i], p[j], back[j], back[i]], 1)
        hl = mb.build(f"LGT_Headlamp_{sd}", "LIGHTING", [M["reflector"], M["plastic_black"]])
        L.explode(hl, (s * 0.3, 1, 0.5), 0.55, 6, "Iluminación",
                  f"Faro {'derecho' if s > 0 else 'izquierdo'} (tras la barra de luz)", "A",
                  note="Ubicación según el procedimiento de servicio; geometría interna aproximada")
        objs.append(hl)
    return objs


def build_rear(M):
    objs = []
    tg = S.TAILGATE_FACE
    z0, z1 = 1.302, 1.330

    def ty(z):
        return B.tg_y(z) - 0.002

    def hw(z):
        return S.hw_body(-2.92, z) - B.GAP - 0.004

    for name, mat, za, zb, d, label in (
            ("LGT_Rear_Lightbar_Lens", M["glass_lens_red"], z0 - 0.004, z1 + 0.003, 0.006, "Lente de la barra de luz trasera"),
            ("LGT_Rear_Lightbar_LED", M["led_red"], z0 + 0.006, z1 - 0.008, 0.002, "Barra de luz trasera (LED rojo)")):
        mb = L.MeshBuilder()
        hws = [-hw(za), -0.5, 0.0, 0.5, hw(za)]
        f = [(x, ty(za) - d, za) for x in hws]
        t = [(x if abs(x) < 0.6 else (hw(zb) if x > 0 else -hw(zb)), ty(zb) - d, zb) for x in hws]
        bf = [(p[0], p[1] + 0.012, p[2]) for p in f]
        bt = [(p[0], p[1] + 0.012, p[2]) for p in t]
        for i in range(len(hws) - 1):
            mb.face([f[i], f[i + 1], t[i + 1], t[i]], 0, want=(0, -1, 0))
            mb.face([t[i], t[i + 1], bt[i + 1], bt[i]], 0, want=(0, 0, 1))
            mb.face([f[i], f[i + 1], bf[i + 1], bf[i]], 0, want=(0, 0, -1))
        mb.face([f[0], t[0], bt[0], bf[0]], 0, want=(-1, 0, 0))
        mb.face([f[-1], t[-1], bt[-1], bf[-1]], 0, want=(1, 0, 0))
        obj = mb.build(name, "LIGHTING", mat)
        L.explode(obj, (0, -1, 0.3), 0.30 if "LED" in name else 0.45, 6, "Iluminación", label, "R")
        objs.append(obj)
    # Pilotos laterales en las esquinas de la caja (continuación de la barra)
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        ya, yb = B.tg_y(z0) + 0.012, B.tg_y(z0) + 0.150
        pts = [(ya, z0), (yb, z0 + 0.004), (yb, z1 - 0.004), (ya, z1)]
        cos = [(s * (S.hw_body(y, z) + 0.004), y, z) for (y, z) in pts]
        inner = [(s * (S.hw_body(y, z) - 0.008), y, z) for (y, z) in pts]
        mb.face(cos, 0, want=(s, 0, 0))
        for i in range(4):
            j = (i + 1) % 4
            mb.face([cos[i], cos[j], inner[j], inner[i]], 0)
        obj = mb.build(f"LGT_TailLamp_BodySide_{sd}", "LIGHTING", M["glass_lens_red"])
        L.explode(obj, (s, -0.4, 0.2), 0.35, 6, "Iluminación",
                  f"Piloto lateral de la carrocería ({'derecho' if s > 0 else 'izquierdo'})", "A")
        objs.append(obj)
    # Luces de marcha atrás y catadióptricos en el paragolpes trasero
    for s, sd in ((1, "R"), (-1, "L")):
        mb = L.MeshBuilder()
        L.box(mb, (s * 0.70, S.Y_REAR_END + 0.007, 0.648), (0.16, 0.012, 0.016), 0)
        obj = mb.build(f"LGT_Reverse_{sd}", "LIGHTING", M["glass_lens"])
        L.explode(obj, (0, -1, -0.2), 0.40, 6, "Iluminación", "Luz de marcha atrás", "A")
        objs.append(obj)
        mb = L.MeshBuilder()
        L.box(mb, (s * 0.932, -2.86, 0.55), (0.012, 0.08, 0.035), 0)
        obj = mb.build(f"LGT_RearMarker_{sd}", "LIGHTING", M["glass_lens_red"])
        L.explode(obj, (s, -0.2, 0), 0.35, 6, "Iluminación", "Catadióptrico / luz de posición lateral trasera", "A")
        objs.append(obj)
    # Placa de matrícula y su luz
    mb = L.MeshBuilder()
    y = -2.962
    L.box(mb, (0.0, y, 0.545), (0.305, 0.004, 0.152), 0)
    plate = mb.build("EXT_License_Plate_Rear", "EXTERIOR_PANELS", M["ecoat"])
    plate.rotation_euler = (math.radians(-12), 0, 0)
    L.explode(plate, (0, -1, 0), 0.5, 6, "Matrícula", "Placa de matrícula trasera (genérica, sin texto)", "A")
    objs.append(plate)
    mb = L.MeshBuilder()
    L.box(mb, (0.0, -2.960, 0.632), (0.10, 0.012, 0.008), 0)
    obj = mb.build("LGT_License_Plate_Lamp", "LIGHTING", M["led_white"])
    L.explode(obj, (0, -1, 0.1), 0.45, 6, "Iluminación", "Luz de matrícula", "A")
    objs.append(obj)
    return objs


def build_all(M):
    return build_front(M) + build_rear(M)
