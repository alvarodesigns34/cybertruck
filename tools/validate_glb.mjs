// Valida web/models/cybertruck.glb con el validador oficial de Khronos (gltf-validator) y falla si hay errores.
// Hasta la exportación del 23-10-2026 daba 17 (texCoord −1 en ruedas y frenos sin UV: auditoría C21).
// Necesita el paquete, que no se versiona: npm i --no-save gltf-validator@2.0.0-dev.3.10
// Uso: node tools/validate_glb.mjs [ruta.glb]
import { readFileSync } from 'node:fs';

let validator;
try {
  validator = (await import('gltf-validator')).default;
} catch {
  console.error('Falta gltf-validator: npm i --no-save gltf-validator@2.0.0-dev.3.10');
  process.exit(2);
}
const file = process.argv[2] ?? 'web/models/cybertruck.glb';
const r = await validator.validateBytes(new Uint8Array(readFileSync(file)), { maxIssues: 5000 });
const errors = r.issues.messages.filter((m) => m.severity === 0);
const byCode = {};
for (const m of errors) byCode[m.code] = (byCode[m.code] ?? 0) + 1;
console.log(`${file}: ${r.issues.numErrors} errores, ${r.issues.numWarnings} avisos, ${r.issues.numInfos} informativos`);
for (const [code, n] of Object.entries(byCode)) console.log(`  ${code}: ${n}`);
for (const m of errors.slice(0, 10)) console.log(`  ${m.pointer ?? ''} ${m.message}`);
process.exit(r.issues.numErrors ? 1 : 0);
