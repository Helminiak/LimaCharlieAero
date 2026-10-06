// Establish the mobile layout before first paint; keep navigation working when
// the separate form/measurement script cannot load. With JS disabled, show nav.
document.documentElement.classList.add('js');
document.addEventListener('DOMContentLoaded',()=>{
 const toggle=document.querySelector('[data-menu]'),nav=document.querySelector('#site-nav');
 if(!toggle||!nav)return;
 toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'Close':'Menu';nav.classList.toggle('open',open)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='Menu';toggle.focus()}});
});
