(function(){

  // Light/dark color theme, persisted across portfolio pages.
  const themeButton = document.querySelector('#theme-toggle');
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const safeThemeRead = () => { try { return localStorage.getItem('gta-theme'); } catch (_) { return null; } };
  const applyTheme = (theme, persist = false) => {
    const current = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.dataset.theme = current;
    if (persist) { try { localStorage.setItem('gta-theme', current); } catch (_) {} }
    if (themeButton) {
      const isDark = current === 'dark';
      themeButton.setAttribute('aria-pressed', String(isDark));
      themeButton.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} theme`);
      themeButton.setAttribute('title', `Switch to ${isDark ? 'light' : 'dark'} theme`);
      const icon = themeButton.querySelector('.theme-toggle-icon');
      const label = themeButton.querySelector('.theme-toggle-label');
      if (icon) icon.textContent = isDark ? '☀' : '☾';
      if (label) label.textContent = isDark ? 'Light theme' : 'Dark theme';
    }
    if (themeMeta) themeMeta.setAttribute('content', current === 'dark' ? '#0b1220' : '#fbfcfe');
  };
  applyTheme(document.documentElement.dataset.theme || safeThemeRead() || 'light');
  themeButton?.addEventListener('click', () => applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark', true));

 const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.nav-links');
 if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false')}));}
 const buttons=document.querySelectorAll('.filter-btn');const cards=document.querySelectorAll('.project-card');
 buttons.forEach(button=>button.addEventListener('click',()=>{buttons.forEach(b=>{b.classList.remove('active');b.setAttribute('aria-pressed','false')});button.classList.add('active');button.setAttribute('aria-pressed','true');const category=button.dataset.filter;cards.forEach(card=>{card.hidden=category!=='All'&&card.dataset.category!==category});}));
 if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&window.matchMedia('(pointer:fine)').matches){document.querySelectorAll('.project-card').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5;const y=(e.clientY-r.top)/r.height-.5;card.style.transform='translateY(-4px) rotateY('+(x*3)+'deg) rotateX('+(-y*2)+'deg)';});card.addEventListener('pointerleave',()=>card.style.transform='');});}
 const serviceSelect=document.getElementById('service-interest');
 if(serviceSelect){
  const requestedService=new URLSearchParams(window.location.search).get('service');
  const normalize=value=>(value||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  if(requestedService){
   const query=normalize(requestedService);
   const options=[...serviceSelect.options];
   const match=options.find(option=>option.value && (normalize(option.text)===query || normalize(option.text).includes(query) || query.includes(normalize(option.text))));
   if(match) serviceSelect.value=match.value || match.text;
  }
 }
 document.querySelectorAll('[data-service]').forEach(link=>link.addEventListener('click',()=>{if(serviceSelect){const wanted=link.dataset.service.toLowerCase();const options=[...serviceSelect.options];let found=options.find(option=>wanted.includes('business analysis')&&option.text.toLowerCase().startsWith('business analysis'));if(!found&&wanted.includes('data analytics'))found=options.find(option=>option.text.toLowerCase().startsWith('data analytics'));if(!found&&wanted.includes('sql'))found=options.find(option=>option.text.toLowerCase().startsWith('sql analysis'));if(!found&&wanted.includes('data engineering'))found=options.find(option=>option.text.toLowerCase().startsWith('data engineering'));if(!found&&wanted.includes('ai'))found=options.find(option=>option.text.toLowerCase().startsWith('ai and rag'));if(!found&&wanted.includes('uat'))found=options.find(option=>option.text.toLowerCase().startsWith('uat'));if(found)serviceSelect.value=found.value;}}));
 const form=document.getElementById('project-enquiry-form');
 if(form){form.addEventListener('submit',event=>{event.preventDefault();const data=new FormData(form);const get=name=>(data.get(name)||'Not provided').toString().trim();const subject='Project enquiry: '+get('service');const body=['Hello Gautam,','','I would like to discuss a project with you.','','Name: '+get('name'),'Work email: '+get('email'),'Company / organisation: '+get('company'),'Service: '+get('service'),'Preferred engagement: '+get('engagement'),'Desired timeline: '+get('timeline'),'Reference link: '+get('reference'),'','Project summary:',get('summary'),'','Please let me know the next steps.'].join('\n');const status=document.getElementById('form-status');status.textContent='Opening your email application with the project brief. Review it and press Send to contact Gautam.';window.location.href='mailto:reddygautam98@gmail.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);});}
 const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();
 const sections=document.querySelectorAll('main section[id]');const links=document.querySelectorAll('.nav-links a[href^="#"]');
 if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){links.forEach(link=>link.classList.toggle('active',link.getAttribute('href')==='#'+entry.target.id));}}),{rootMargin:'-35% 0px -55% 0px'});sections.forEach(section=>observer.observe(section));}
})();