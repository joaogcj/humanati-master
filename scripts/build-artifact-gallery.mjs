import { readdir, stat, writeFile } from 'node:fs/promises';
import { extname, join, relative, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const output = join(root, 'artifact-gallery', 'artifacts.json');
const ignored = new Set(['.git', 'node_modules', 'dist', 'storybook-static', 'artifact-gallery']);

const areaLabels = {
  archives: 'Pacotes históricos',
  backgrounds: 'Backgrounds',
  branding: 'Branding',
  'dashboard-library': 'Dashboards',
  'design-system': 'Design System',
  devops: 'DevOps',
  documentation: 'Documentação',
  'glass-ui': 'Glass UI',
  icons: 'Ícones',
  marketing: 'Marketing',
  'social-media': 'Social Media',
  stories: 'Storybook',
  'ui-kit': 'UI Kit',
  website: 'Website'
};
areaLabels['product-monihook'] = 'MoniHook';
areaLabels['product-vane'] = 'VANE';
areaLabels['product-wic'] = 'WIC';
areaLabels.supplemental = 'Acervo adicional';

const previewKinds = {
  '.png': 'image', '.jpg': 'image', '.jpeg': 'image', '.gif': 'image', '.webp': 'image', '.svg': 'image', '.ico': 'image',
  '.html': 'page', '.pdf': 'document',
  '.md': 'text', '.txt': 'text', '.json': 'text', '.csv': 'text', '.css': 'text', '.js': 'text', '.mjs': 'text',
  '.yml': 'text', '.yaml': 'text', '.tf': 'text', '.conf': 'text', '.dockerignore': 'text', '.gitignore': 'text'
};

const featuredPatterns = [
  /branding\/reference-boards/i,
  /marketing\/presentations/i,
  /documentation\/(BRAND_MANUAL|ARCHITECTURE|COMPLETION_REPORT)/i,
  /website\/master-package\/pages\/(index|dashboard|monihook|vane|wic)\.html/i,
  /ui-kit\/index\.html/i,
  /glass-ui\/index\.html/i,
  /dashboard-library\/index\.html/i
];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.isDirectory() && ignored.has(entry.name)) continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else files.push(path);
  }
  return files;
}

const artifacts = [];
for (const file of await walk(root)) {
  const path = relative(root, file).replaceAll('\\', '/');
  const pathParts = path.split('/');
  const [top] = pathParts;
  const area = top === 'branding' && pathParts[1] === 'products'
    ? `product-${pathParts[2]}`
    : top === 'archives' && pathParts[1] === 'sx'
      ? 'supplemental'
      : top === 'branding' && pathParts[1] === 'reference-boards' && pathParts[2] === 'supplemental'
        ? 'supplemental'
        : top;
  if (!areaLabels[area]) continue;
  const fileName = basename(file);
  const packageName = top === 'archives'
    ? (pathParts[1] === 'extracted' && pathParts.length > 3
      ? pathParts[2]
      : pathParts[1] === 'source-packages' || pathParts[1] === 'supplemental-sources'
        ? fileName.replace(/\.zip$/i, '')
        : pathParts[1] === 'sx' && pathParts[2] === 'a12'
          ? 'Humanati_12_Outros_Artefatos_e_Variacoes'
          : pathParts[1] === 'sx' && pathParts[2] === 'all'
            ? 'Humanati_Todos_Artefatos_Disponiveis'
            : null)
    : null;
  const extension = extname(file).toLowerCase() || basename(file).toLowerCase();
  const info = await stat(file);
  artifacts.push({
    id: artifacts.length + 1,
    name: fileName,
    title: fileName.replace(/[-_]/g, ' ').replace(/\.[^.]+$/, ''),
    path,
    url: `../${path.split('/').map(encodeURIComponent).join('/')}`,
    area,
    areaLabel: areaLabels[area],
    packageName,
    sourceKind: top === 'archives' ? (pathParts[1] === 'extracted' && pathParts.length > 3 || pathParts[1] === 'sx' ? 'extracted' : pathParts[1].includes('sources') ? 'package' : 'archive-index') : 'consolidated',
    extension: extname(file).toLowerCase().replace('.', '') || 'arquivo',
    bytes: info.size,
    preview: previewKinds[extname(file).toLowerCase()] || previewKinds[extension] || 'download',
    featured: featuredPatterns.some(pattern => pattern.test(path))
  });
}

artifacts.sort((a, b) => Number(b.featured) - Number(a.featured) || a.areaLabel.localeCompare(b.areaLabel, 'pt-BR') || a.title.localeCompare(b.title, 'pt-BR'));

await writeFile(output, `${JSON.stringify({ generatedAt: new Date().toISOString(), count: artifacts.length, artifacts }, null, 2)}\n`);
console.log(`Galeria atualizada: ${artifacts.length} artefatos.`);
