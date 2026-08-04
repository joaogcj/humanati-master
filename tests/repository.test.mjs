import assert from 'node:assert/strict';
import { access, readFile, readdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = new URL('..', import.meta.url);

test('preserva todos os 32 pacotes-fonte', async () => {
  const packages = (await readdir(new URL('archives/source-packages/', root))).filter((name) => name.endsWith('.zip'));
  assert.equal(packages.length, 32);
});

test('contém os 24 registros de lote do Design System', async () => {
  const docs = (await readdir(new URL('design-system/docs/lotes/', root))).filter((name) => name.endsWith('.md'));
  for (let lot = 1; lot <= 24; lot += 1) {
    const id = String(lot).padStart(3, '0');
    assert.ok(docs.some((name) => name.startsWith(`lote${id}`)), `lote ${id} ausente`);
  }
});

test('mantém o pacote final do website como referência canônica', async () => {
  await access(new URL('website/master-package/pages/index.html', root));
  const manifest = JSON.parse(await readFile(new URL('website/master-package/docs/manifest.json', root), 'utf8'));
  assert.ok(manifest);
});

test('tokens JSON são válidos', async () => {
  const names = (await readdir(new URL('design-system/tokens/', root))).filter((name) => name.endsWith('.json'));
  assert.ok(names.length >= 40);
  for (const name of names) JSON.parse(await readFile(new URL(`design-system/tokens/${name}`, root), 'utf8'));
});

test('as 16 páginas canônicas não possuem referências locais quebradas', async () => {
  const pagesDirectory = fileURLToPath(new URL('website/master-package/pages/', root));
  const pages = (await readdir(pagesDirectory)).filter((name) => name.endsWith('.html'));
  assert.equal(pages.length, 16);
  for (const name of pages) {
    const page = join(pagesDirectory, name);
    const html = await readFile(page, 'utf8');
    for (const match of html.matchAll(/(?:href|src)=["']([^"']+)["']/g)) {
      const reference = match[1];
      if (/^(?:https?:|mailto:|tel:|#)/.test(reference)) continue;
      await access(join(dirname(page), reference));
    }
  }
});

test('bibliotecas visuais essenciais possuem demos executáveis', async () => {
  for (const directory of ['backgrounds', 'dashboard-library', 'glass-ui', 'ui-kit']) {
    await access(new URL(`${directory}/index.html`, root));
  }
  await access(new URL('icons/sprite.svg', root));
});

test('pacote de marketing cobre canais e formatos prometidos', async () => {
  for (const file of [
    'marketing/strategy.md',
    'marketing/campaign-matrix.csv',
    'marketing/ads/meta-ads.csv',
    'marketing/ads/google-ads.csv',
    'marketing/ads/linkedin-ads.csv',
    'marketing/presentations/Humanati_Institucional_v1.pptx',
    'social-media/content-calendar.csv',
    'social-media/copy-bank.md',
    'social-media/templates/feed-1080x1080.svg',
    'social-media/templates/story-1080x1920.svg',
    'social-media/templates/linkedin-1200x627.svg'
  ]) await access(new URL(file, root));
});
