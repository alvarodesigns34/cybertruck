// Genera docs/interferencias-pendientes.md a partir del JSON del detector (blender/scripts/interferencias.py).
// Uso: node tools/gen_interferencias.mjs <interf.json> [profundidad_minima_mm]
import fs from 'node:fs';

const src = process.argv[2];
const dmin = Number(process.argv[3] || 3);
const r = JSON.parse(fs.readFileSync(src, 'utf8'));
const pend = r.filter(x => x.profundidad_mm > dmin && !x.intencionado);
const intenc = r.filter(x => x.intencionado);

const zona = (x) => {
  const n = x.a + ' ' + x.b;
  if (/INT_Seat|Headrest|Seatbelt/.test(n)) return 'Asientos y cinturones';
  if (/INT_|Airbag|CAM_Windshield|ELE_Antennas/.test(n)) return 'Habitáculo (salpicadero, consola, guarnecidos)';
  if (/CARGO_|Bed_|Tailgate|Mast|Sail|Tonneau/.test(n)) return 'Caja de carga, portón y persiana';
  if (/DU_|Gear|Inverter|Motor_|Rotor|Stator/.test(n)) return 'Unidades motrices';
  if (/BAT_|HV_|LV_|ChargePort|Busbar|Harness|Cables/.test(n)) return 'Alta y baja tensión (batería, módulos y mazos)';
  if (/THM_|Radiator|Cooling|Coolant|Chiller|AC_/.test(n)) return 'Gestión térmica';
  if (/SUS_|BRK_|WHL_|STR_|CHS_/.test(n)) return 'Chasis (suspensión, frenos, dirección, aire)';
  return 'Carrocería y estructura';
};

const groups = {};
for (const x of pend) (groups[zona(x)] ||= []).push(x);
const bins = [[3, 5], [5, 10], [10, 30], [30, 1e9]];
const hist = bins.map(([a, b]) => pend.filter(x => x.profundidad_mm > a && x.profundidad_mm <= b).length);

let md = `# Interferencias de ensamblaje pendientes\n\n`;
md += `Informe generado con \`node tools/gen_interferencias.mjs\` a partir del detector \`blender/scripts/interferencias.py\` `;
md += `sobre la escena construida (explosión a cero). Se listan las parejas de objetos cuyas superficies visibles se cortan con una `;
md += `penetración mayor de ${dmin} mm y que no están en la lista de penetraciones intencionadas. La profundidad se mide cerca `;
md += `de la zona de cruce; la extensión es la diagonal de la caja que envuelve esa zona.\n\n`;
md += `## Resumen\n\n| Penetración | Parejas |\n|---|---|\n`;
md += `| 3–5 mm | ${hist[0]} |\n| 5–10 mm | ${hist[1]} |\n| 10–30 mm | ${hist[2]} |\n| > 30 mm | ${hist[3]} |\n`;
md += `| **Total pendiente** | **${pend.length}** |\n| Penetraciones intencionadas (no se cuentan) | ${intenc.length} |\n`;
// cruces por debajo del umbral (holguras de contacto de 1–3 mm): solo informativos
const low = (lo, hi) => r.filter(x => !x.intencionado && x.profundidad_mm > lo && x.profundidad_mm <= hi).length;
md += `| Cruces por debajo del umbral, 1–2 mm (informativo) | ${low(1, 2)} |\n`;
md += `| Cruces por debajo del umbral, 2–${dmin} mm (informativo) | ${low(2, dmin)} |\n\n`;
md += `| Zona | Parejas |\n|---|---|\n`;
for (const [k, v] of Object.entries(groups).sort((a, b) => b[1].length - a[1].length)) md += `| ${k} | ${v.length} |\n`;
md += `\n## Detalle por zona\n\n`;
for (const [k, v] of Object.entries(groups).sort((a, b) => b[1].length - a[1].length)) {
  md += `### ${k} (${v.length})\n\n| Pieza A | Pieza B | Penetración (mm) | Extensión (mm) | Centro (x, y, z) m |\n|---|---|---|---|---|\n`;
  for (const x of v.sort((a, b) => b.profundidad_mm - a.profundidad_mm))
    md += `| \`${x.a}\` | \`${x.b}\` | ${x.profundidad_mm} | ${x.extension_mm} | ${x.centro.join(', ')} |\n`;
  md += `\n`;
}
const motivos = {};
for (const x of intenc) motivos[x.intencionado] = (motivos[x.intencionado] || 0) + 1;
md += `## Penetraciones intencionadas reconocidas\n\n| Motivo | Parejas |\n|---|---|\n`;
for (const [k, v] of Object.entries(motivos).sort((a, b) => b[1] - a[1])) md += `| ${k} | ${v} |\n`;
fs.writeFileSync('docs/interferencias-pendientes.md', md);
console.log(`pendientes ${pend.length}, intencionadas ${intenc.length}`);
