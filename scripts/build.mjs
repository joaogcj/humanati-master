import { cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const output = join(root, 'dist');
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

for (const directory of ['backgrounds', 'branding', 'dashboard-library', 'design-system', 'glass-ui', 'icons', 'marketing', 'social-media', 'ui-kit', 'website']) {
  await cp(join(root, directory), join(output, directory), { recursive: true });
}

const componentDirectory = join(root, 'design-system', 'components');
const componentFiles = (await readdir(componentDirectory)).filter((name) => name.endsWith('.css')).sort();
const bundle = [];
for (const file of componentFiles) {
  bundle.push(`/* ${file} */\n${await readFile(join(componentDirectory, file), 'utf8')}`);
}
await writeFile(join(output, 'humanati-components.css'), `${bundle.join('\n\n')}\n`);

const manifest = {
  generatedAt: new Date().toISOString(),
  components: componentFiles,
  componentCount: componentFiles.length
};
await writeFile(join(output, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`Build concluído: ${componentFiles.length} componentes CSS.`);
