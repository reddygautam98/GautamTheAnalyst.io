(function(){
 const toggle=document.querySelector('.menu-toggle');
 const nav=document.querySelector('.nav-links');
 if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false')}));}
 const buttons=document.querySelectorAll('.filter-btn');
 const cards=document.querySelectorAll('.project-card');
 buttons.forEach(button=>button.addEventListener('click',()=>{buttons.forEach(b=>b.classList.remove('active'));button.classList.add('active');const category=button.dataset.filter;cards.forEach(card=>{card.hidden=category!=='All'&&card.dataset.category!==category});}));
 if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&window.matchMedia('(pointer:fine)').matches){document.querySelectorAll('.project-card').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5;const y=(e.clientY-r.top)/r.height-.5;card.style.transform='translateY(-4px) rotateY('+(x*3)+'deg) rotateX('+(-y*2)+'deg)';});card.addEventListener('pointerleave',()=>card.style.transform='');});}
 const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();
 const sections=document.querySelectorAll('main section[id]');const links=document.querySelectorAll('.nav-links a[href^="#"]');
 if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){links.forEach(link=>{link.classList.toggle('active',link.getAttribute('href')==='#'+entry.target.id);});}}),{rootMargin:'-35% 0px -55% 0px'});sections.forEach(section=>observer.observe(section));}
})();