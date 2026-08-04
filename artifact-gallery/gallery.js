const requestedArea = new URLSearchParams(location.search).get('area');
const state = { artifacts: [], area: requestedArea || 'all', type: 'all', packageName: 'all', query: '', sort: 'featured', list: false };

const elements = {
  areaNav: document.querySelector('#areaNav'), artifactGrid: document.querySelector('#artifactGrid'), emptyState: document.querySelector('#emptyState'),
  search: document.querySelector('#searchInput'), type: document.querySelector('#typeFilter'), package: document.querySelector('#packageFilter'), sort: document.querySelector('#sortFilter'),
  total: document.querySelector('#totalCount'), sidebarCount: document.querySelector('#sidebarCount'), resultCount: document.querySelector('#resultCount'),
  activeArea: document.querySelector('#activeAreaLabel'), clear: document.querySelector('#clearFilters'), view: document.querySelector('#viewToggle'),
  dialog: document.querySelector('#previewDialog'), previewArea: document.querySelector('#previewArea'), previewTitle: document.querySelector('#previewTitle'),
  previewPath: document.querySelector('#previewPath'), previewStage: document.querySelector('#previewStage'), previewMeta: document.querySelector('#previewMeta'),
  open: document.querySelector('#openArtifact'), download: document.querySelector('#downloadArtifact'), close: document.querySelector('#closePreview'),
  theme: document.querySelector('#themeToggle')
};

const formatBytes = bytes => bytes < 1024 ? `${bytes} B` : bytes < 1048576 ? `${(bytes / 1024).toFixed(1)} KB` : `${(bytes / 1048576).toFixed(1)} MB`;
const escapeHtml = value => value.replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

function filteredArtifacts() {
  const query = state.query.trim().toLocaleLowerCase('pt-BR');
  const filtered = state.artifacts.filter(item =>
    (state.area === 'all' || item.area === state.area) &&
    (state.type === 'all' || item.extension === state.type) &&
    (state.packageName === 'all' || item.packageName === state.packageName) &&
    (!query || `${item.title} ${item.path} ${item.areaLabel} ${item.extension}`.toLocaleLowerCase('pt-BR').includes(query))
  );
  return filtered.sort((a,b) => state.sort === 'name'
    ? a.title.localeCompare(b.title,'pt-BR')
    : state.sort === 'newest'
      ? b.bytes - a.bytes
      : Number(b.featured) - Number(a.featured) || a.title.localeCompare(b.title,'pt-BR'));
}

function buildNavigation() {
  const counts = state.artifacts.reduce((map,item) => map.set(item.area,(map.get(item.area)||0)+1),new Map());
  const areas = [...new Map(state.artifacts.map(item => [item.area,item.areaLabel])).entries()].sort((a,b)=>a[1].localeCompare(b[1],'pt-BR'));
  elements.areaNav.innerHTML = [['all','Todos',state.artifacts.length],...areas.map(([id,label])=>[id,label,counts.get(id)])]
    .map(([id,label,count])=>`<button class="area-button${id===state.area?' active':''}" data-area="${id}" type="button"><span>${label}</span><span>${count}</span></button>`).join('');
  elements.areaNav.querySelectorAll('[data-area]').forEach(button => button.addEventListener('click',()=>{state.area=button.dataset.area;buildNavigation();render();}));
}

function cardPreview(item) {
  if (item.preview === 'image') return `<img src="${item.url}" alt="" loading="lazy">`;
  return `<span class="file-glyph">${escapeHtml(item.extension)}</span>`;
}

function render() {
  const items = filteredArtifacts();
  const areaLabel = state.area === 'all' ? 'Todos os artefatos' : (state.artifacts.find(item=>item.area===state.area)?.areaLabel || 'Artefatos');
  elements.activeArea.textContent = areaLabel;
  elements.resultCount.textContent = `${items.length} ${items.length===1?'resultado':'resultados'}`;
  elements.artifactGrid.classList.toggle('list',state.list);
  elements.view.textContent = state.list ? '▦' : '☷';
  elements.emptyState.hidden = items.length > 0;
  elements.artifactGrid.innerHTML = items.map(item => `<article class="artifact-card">
    <div class="card-preview">${item.featured?'<span class="featured-tag">Destaque</span>':''}${cardPreview(item)}</div>
    <div class="card-body"><div class="card-meta"><span>${escapeHtml(item.areaLabel)}</span><span>${escapeHtml(item.extension)} · ${formatBytes(item.bytes)}</span></div>
    <h3 title="${escapeHtml(item.name)}">${escapeHtml(item.title)}</h3><p class="card-path" title="${escapeHtml(item.path)}">${escapeHtml(item.path)}</p>
    <div class="card-actions"><button class="preview-button" data-preview="${item.id}" type="button">Visualizar</button><a href="${item.url}" target="_blank" rel="noopener">Abrir</a></div></div></article>`).join('');
  elements.artifactGrid.querySelectorAll('[data-preview]').forEach(button=>button.addEventListener('click',()=>openPreview(Number(button.dataset.preview))));
}

async function openPreview(id) {
  const item = state.artifacts.find(artifact=>artifact.id===id);
  if (!item) return;
  elements.previewArea.textContent=item.areaLabel;
  elements.previewTitle.textContent=item.title;
  elements.previewPath.textContent=item.path;
  elements.previewMeta.textContent=`${item.extension.toUpperCase()} · ${formatBytes(item.bytes)}`;
  elements.open.href=item.url;
  elements.download.href=item.url;
  elements.download.download=item.name;
  elements.previewStage.replaceChildren();
  if (item.preview==='image') {
    const image=document.createElement('img'); image.src=item.url; image.alt=item.title; elements.previewStage.append(image);
  } else if (item.preview==='page' || item.preview==='document') {
    const frame=document.createElement('iframe'); frame.src=item.url; frame.title=`Visualização de ${item.title}`; elements.previewStage.append(frame);
  } else if (item.preview==='text') {
    const pre=document.createElement('pre'); pre.textContent='Carregando…'; elements.previewStage.append(pre);
    try { const response=await fetch(item.url); pre.textContent=(await response.text()).slice(0,120000); } catch { pre.textContent='Não foi possível carregar a prévia textual.'; }
  } else {
    elements.previewStage.innerHTML=`<div class="download-preview"><span class="file-glyph">${escapeHtml(item.extension)}</span><h3>Pré-visualização externa</h3><p>Este formato deve ser aberto no aplicativo correspondente. Use os botões abaixo para abrir ou baixar o arquivo original.</p></div>`;
  }
  elements.dialog.showModal();
}

elements.search.addEventListener('input',event=>{state.query=event.target.value;render();});
elements.type.addEventListener('change',event=>{state.type=event.target.value;render();});
elements.package.addEventListener('change',event=>{state.packageName=event.target.value;if(event.target.value!=='all'){state.area='archives';buildNavigation();}render();});
elements.sort.addEventListener('change',event=>{state.sort=event.target.value;render();});
elements.view.addEventListener('click',()=>{state.list=!state.list;render();});
elements.clear.addEventListener('click',()=>{state.area='all';state.type='all';state.packageName='all';state.query='';elements.search.value='';elements.type.value='all';elements.package.value='all';buildNavigation();render();});
elements.close.addEventListener('click',()=>elements.dialog.close());
elements.dialog.addEventListener('click',event=>{if(event.target===elements.dialog)elements.dialog.close();});
elements.theme.addEventListener('click',()=>{const light=document.documentElement.dataset.theme==='light';document.documentElement.dataset.theme=light?'dark':'light';localStorage.setItem('humanati-gallery-theme',light?'dark':'light');});

const savedTheme=localStorage.getItem('humanati-gallery-theme'); if(savedTheme)document.documentElement.dataset.theme=savedTheme;

try {
  const response=await fetch('artifacts.json');
  const payload=await response.json();
  state.artifacts=payload.artifacts;
  if (state.area !== 'all' && !state.artifacts.some(item => item.area === state.area)) state.area = 'all';
  elements.total.textContent=payload.count.toLocaleString('pt-BR');
  elements.sidebarCount.textContent=payload.count.toLocaleString('pt-BR');
  const extensions=[...new Set(state.artifacts.map(item=>item.extension))].sort();
  elements.type.insertAdjacentHTML('beforeend',extensions.map(ext=>`<option value="${escapeHtml(ext)}">.${escapeHtml(ext)}</option>`).join(''));
  const packages=[...new Set(state.artifacts.map(item=>item.packageName).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  elements.package.insertAdjacentHTML('beforeend',packages.map(name=>`<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join(''));
  buildNavigation(); render();
} catch (error) {
  elements.artifactGrid.innerHTML='<div class="empty-state"><strong>O catálogo não pôde ser carregado.</strong><p>Atualize a página para tentar novamente.</p></div>';
  console.error(error);
}
