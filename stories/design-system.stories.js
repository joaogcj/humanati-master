const modules = import.meta.glob('../design-system/components/*.css', { eager: true, query: '?inline', import: 'default' });

export default { title: 'Humanati/Design System', tags: ['autodocs'] };

export const ComponentCatalog = {
  render: () => {
    const names = Object.keys(modules).map((path) => path.split('/').pop().replace('.css', '')).sort();
    return `<main class="catalog">${names.map((name) => `<article class="catalog-card"><h3>${name}</h3><code>.${name}</code></article>`).join('')}</main>`;
  }
};
