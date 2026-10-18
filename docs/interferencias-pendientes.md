# Interferencias de ensamblaje pendientes

Informe generado con `node tools/gen_interferencias.mjs` a partir del detector `blender/scripts/interferencias.py` sobre la escena construida (explosión a cero). Se listan las parejas de objetos cuyas superficies visibles se cortan con una penetración mayor de 3 mm y que no están en la lista de penetraciones intencionadas. La profundidad se mide cerca de la zona de cruce; la extensión es la diagonal de la caja que envuelve esa zona.

## Resumen

| Penetración | Parejas |
|---|---|
| 3–5 mm | 0 |
| 5–10 mm | 0 |
| 10–30 mm | 0 |
| > 30 mm | 0 |
| **Total pendiente** | **0** |
| Penetraciones intencionadas (no se cuentan) | 320 |
| Cruces por debajo del umbral, 1–2 mm (informativo) | 157 |
| Cruces por debajo del umbral, 2–3 mm (informativo) | 83 |

| Zona | Parejas |
|---|---|

## Detalle por zona

## Penetraciones intencionadas reconocidas

| Motivo | Parejas |
|---|---|
| tornillo, remache o grapa que entra en la pieza que fija | 155 |
| junta de goma o espuma comprimida contra la pieza que la aprieta (la compresión de montaje mueve sus vértices hasta la superficie de la vecina; queda el resto de las caras grandes) | 19 |
| celdas embebidas en la espuma estructural y los refrigeradores | 12 |
| lamas enganchadas a los eslabones de la cadena de arrastre | 12 |
| mazo que atraviesa el mamparo o el suelo por su pasacables | 10 |
| eje o barra que atraviesa la pared de su carcasa (por un retén o un pasamuros) | 9 |
| vástago de la válvula por su taladro de la llanta y del tapacubos | 8 |
| casquillos prensados en los ojos de los brazos | 8 |
| espárragos y centrador del buje por los taladros de la campana del disco y de la llanta | 8 |
| varillas del reposacabezas en sus guías del respaldo | 6 |
| casquillos de los soportes encajados en los ojales de la carcasa | 5 |
| rótula inferior de la bieleta atornillada en el ojo de la barra estabilizadora | 4 |
| extremo del fuelle neumático engastado en el pistón de rodadura | 4 |
| el cerradero entra en la horquilla de la cerradura (puerta cerrada) | 4 |
| talones del neumático asentados en los asientos de la llanta | 4 |
| el cerradero atraviesa la junta primaria por su escotadura | 4 |
| junta de la puerta abrazada a la pestaña del marco del cristal | 4 |
| casquillos de los brazos apretados entre las orejetas del subchasis | 4 |
| portavasos encastrado en la consola | 3 |
| eje prensado en el taladro del paquete de chapas del rotor | 3 |
| racores de las líneas de aire roscados en la cara del bloque de válvulas | 3 |
| anclajes de amarre encastrados en el suelo de la caja y atornillados a sus placas de tuercas | 3 |
| extremo de la viga del salpicadero alojado en su soporte | 2 |
| barras y cables que entran en el cabezal HV por sus pasamuros | 2 |
| bomba de aceite y filtro roscados en la carcasa de la reductora | 2 |
| cinta del cinturón trasero por la ranura del guarnecido del pilar C | 2 |
| pie de la hebilla delantera hundido en el costado blando del cojín, entre este y la consola | 2 |
| dientes en toma entre piñón y rueda (dentado simplificado, sin fase entre los dientes) | 2 |
| espuma de la rejilla comprimida entre la fascia y la viga del paragolpes | 2 |
| pistón y pasadores de la pinza trasera asomando a la ranura del disco, donde empujan las pastillas | 2 |
| correas abrazadas a las poleas de los motores y de la tuerca de bolas del actuador | 2 |
| mazo de la puerta por el fuelle pasamuros junto a la junta primaria | 2 |
| eje del rotor estriado en el piñón de entrada | 2 |
| colectores de refrigerante por los pasos de las vigas interiores | 1 |
| tubos de freno roscados en las bocas de la HCU | 1 |
| brazo y base del retrovisor por la abertura de su cubierta decorativa | 1 |
| boca de llenado del depósito del lavaparabrisas por su abertura del faldón bajo el capó | 1 |
| escobilla enganchada en el gancho del brazo | 1 |
| tubo del lavaparabrisas por el pasamuros del faldón trasero bajo el capó | 1 |
