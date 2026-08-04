import { readFile, readdir, stat } from 'node:fs/promises';
import { extname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const failures = [];
let checked = 0;

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === 'node_modules' || entry.name === 'dist' || entry.name === '.git') continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else files.push(path);
  }
  return files;
}

for (const file of await walk(root)) {
  const extension = extname(file).toLowerCase();
  if (!['.json', '.css', '.svg', '.html', '.js', '.mjs'].includes(extension)) continue;
  checked += 1;
  const content = await readFile(file, 'utf8');
  if (!content.trim()) failures.push(`${relative(root, file)}: arquivo vazio`);
  if (extension === '.json') {
    try { JSON.parse(content); } catch (error) {
      failures.push(`${relative(root, file)}: JSON inválido (${error.message})`);
    }
  }
  if (extension === '.svg' && !content.includes('<svg')) {
    failures.push(`${relative(root, file)}: SVG sem elemento raiz`);
  }
  if (extension === '.css') {
    const opens = [...content].filter((char) => char === '{').length;
    const closes = [...content].filter((char) => char === '}').length;
    if (opens !== closes) failures.push(`${relative(root, file)}: chaves CSS desbalanceadas`);
  }
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`Validação concluída: ${checked} arquivos estruturais verificados.`);
