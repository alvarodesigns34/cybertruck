// Genera docs/component-inventory.md a partir del manifiesto exportado desde Blender.
// Uso: node tools/gen_inventory.mjs
import { readFile, writeFile } from 'node:fs/promises';

// Las etiquetas de los sistemas y de la fidelidad salen del visor (web/src/config.js): una sola fuente,
// antes estaban copiadas aquí y podían divergir (auditoría C20).
import { SYSTEM_LABELS as SYSTEMS, FIDELITY } from '../web/src/config.js';

const FID = Object.fromEntries(Object.entries(FIDELITY).map(([k, v]) => [k, v.label]));

const m = JSON.parse(await readFile('web/models/cybertruck-manifest.json', 'utf8'));
const by = new Map();
for (const c of m.components) {
  const k = c.system || 'OTROS';
  if (!by.has(k)) by.set(k, []);
  by.get(k).push(c);
}
const counts = { V: 0, R: 0, A: 0 };
for (const c of m.components) if (counts[c.fidelity] !== undefined) counts[c.fidelity] += 1;
const totalFaces = m.components.reduce((s, c) => s + (c.faces || 0), 0);

let md = `# Inventario de componentes\n\n`;
md += `> Generado automáticamente con \`node tools/gen_inventory.mjs\` a partir de \`web/models/cybertruck-manifest.json\`, `;
md += `que se exporta desde la escena real de Blender. Solo enumera objetos que existen en el modelo.\n\n`;
md += `- Vehículo: ${m.vehicle}\n- Componentes (nodos con metadatos): **${m.components.length}**\n`;
md += `- Mallas: **${m.components.filter((c) => c.type === 'MESH').length}** · Conjuntos (vacíos con pivote): **${m.components.filter((c) => c.type === 'EMPTY').length}**\n`;
md += `- Caras de malla base (antes de modificadores): ${totalFaces.toLocaleString('es-ES')}\n`;
md += `- Fidelidad: Verificado ${counts.V} · Reconstruido ${counts.R} · Aproximado ${counts.A}\n\n`;
md += `Etapas de explosión: ${Object.entries(m.stages).map(([k, v]) => `${k}. ${v}`).join(' · ')}\n\n`;
for (const [sys, label] of Object.entries(SYSTEMS)) {
  const list = by.get(sys);
  if (!list) continue;
  list.sort((a, b) => a.name.localeCompare(b.name));
  md += `## ${label} (\`${sys}\`) — ${list.length}\n\n| Objeto | Descripción | Tipo | Etapa | Fidelidad |\n|---|---|---|---|---|\n`;
  for (const c of list) {
    md += `| \`${c.name}\` | ${c.label || ''}${c.note ? ` — _${c.note}_` : ''} | ${c.type === 'EMPTY' ? 'Conjunto' : 'Malla'} | ${c.stage ?? ''} | ${FID[c.fidelity] || ''} |\n`;
  }
  md += '\n';
}
await writeFile('docs/component-inventory.md', md, 'utf8');
console.log(`Inventario generado: ${m.components.length} componentes`);
