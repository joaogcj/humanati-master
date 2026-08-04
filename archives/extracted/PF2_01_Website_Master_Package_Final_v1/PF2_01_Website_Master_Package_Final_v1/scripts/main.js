document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
document.querySelectorAll('[data-menu]').forEach(btn=>btn.addEventListener('click',()=>document.body.classList.toggle('menu-open')));
