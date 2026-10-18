/* Progressive enhancements ported from Gautam_The_Analyst_Futuristic.zip. */
(function(){
  'use strict';
  const root=document.documentElement;
  const $=(s,c=document)=>c.querySelector(s);
  const $$=(s,c=document)=>Array.from(c.querySelectorAll(s));
  const reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer=window.matchMedia&&window.matchMedia('(pointer:fine)').matches;
  const inSamples=/\/samples\//.test(location.pathname);
  const base=inSamples?'../':'';

  /* 1) Shared command palette: Ctrl/Cmd+K or /; Escape closes it. */
  const navLinks=$$('.nav-links a').filter(a=>a.href);
  const commandItems=[
    {title:'Home',hint:'Page',href:base+'index.html'},
    {title:'Services',hint:'Page',href:base+'services.html'},
    {title:'Projects',hint:'Page',href:base+'projects.html'},
    {title:'BA Samples',hint:'Documents & diagrams',href:base+'samples/index.html'},
    {title:'About',hint:'Page',href:base+'about.html'},
    {title:'Resume',hint:'Experience & skills',href:base+'resume.html'},
    {title:'Contact',hint:'Project enquiry',href:base+'contact.html'},
    {title:'Email Gautam',hint:'Direct contact',href:'mailto:reddygautam98@gmail.com'},
    {title:'Toggle light / dark theme',hint:'Appearance',action:'theme'}
  ];
  const themeButton=$('#theme-toggle');
  if(themeButton&&!$('.command-trigger')){
    const trigger=document.createElement('button');
    trigger.type='button';trigger.className='command-trigger';trigger.setAttribute('aria-haspopup','dialog');trigger.setAttribute('aria-controls','site-command-palette');
    trigger.innerHTML='<span class="command-trigger-label">Quick search</span><kbd>Ctrl K</kbd>';
    trigger.addEventListener('click',()=>openPalette());
    themeButton.parentElement.insertBefore(trigger,themeButton);
  }
  let palette=$('#site-command-palette'),paletteInput,activeItems=[],activeIndex=0;
  if(!palette){
    palette=document.createElement('dialog');palette.id='site-command-palette';palette.className='command-palette';palette.setAttribute('aria-label','Site command palette');
    palette.innerHTML='<div class="command-palette-top"><label for="command-palette-input">Navigate or run an action</label><input class="command-palette-input" id="command-palette-input" type="search" autocomplete="off" placeholder="Search pages, projects, actions…"></div><div class="command-palette-list" id="command-palette-list" role="listbox" aria-label="Quick actions"></div><div class="command-palette-bottom"><span>↑ ↓ move · Enter open · Esc close</span><span>Ctrl/⌘ + K or /</span></div>';
    document.body.appendChild(palette);
  }
  paletteInput=$('#command-palette-input',palette);
  const list=$('#command-palette-list',palette);
  function renderPalette(){
    const q=(paletteInput.value||'').trim().toLowerCase();
    activeItems=commandItems.filter(item=>(item.title+' '+item.hint).toLowerCase().includes(q));
    activeIndex=Math.min(activeIndex,Math.max(activeItems.length-1,0));
    list.innerHTML='';
    if(!activeItems.length){list.innerHTML='<div style="padding:16px;color:var(--muted);font-size:12px">No matching pages or actions.</div>';return;}
    activeItems.forEach((item,i)=>{
      const el=document.createElement(item.action?'button':'a');
      if(item.href)el.href=item.href;
      if(item.action)el.type='button';
      el.setAttribute('role','option');el.setAttribute('aria-selected',String(i===activeIndex));
      el.innerHTML='<span>'+item.title.replace(/[&<>"]/g,'')+'</span><small>'+item.hint+'</small>';
      el.addEventListener('mouseenter',()=>{activeIndex=i;updateSelection()});
      el.addEventListener('click',e=>{
        if(item.action==='theme'){e.preventDefault();themeButton?.click();palette.close();}
        else if(item.href){palette.close();}
      });
      list.appendChild(el);
    });
  }
  function updateSelection(){ $$('.command-palette-list [role="option"]',palette).forEach((el,i)=>el.setAttribute('aria-selected',String(i===activeIndex))); }
  function openPalette(){
    if(!palette.open)palette.showModal();
    paletteInput.value='';activeIndex=0;renderPalette();window.setTimeout(()=>paletteInput.focus(),20);
  }
  paletteInput?.addEventListener('input',()=>{activeIndex=0;renderPalette()});
  paletteInput?.addEventListener('keydown',e=>{
    if(e.key==='ArrowDown'){e.preventDefault();activeIndex=Math.min(activeIndex+1,activeItems.length-1);updateSelection();}
    if(e.key==='ArrowUp'){e.preventDefault();activeIndex=Math.max(activeIndex-1,0);updateSelection();}
    if(e.key==='Enter'){e.preventDefault();const item=activeItems[activeIndex];if(!item)return;if(item.action==='theme'){themeButton?.click();palette.close();}else if(item.href){location.href=item.href;}}
  });
  palette?.addEventListener('click',e=>{if(e.target===palette)palette.close()});
  document.addEventListener('keydown',e=>{
    const typing=e.target instanceof HTMLElement&&(e.target.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName));
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openPalette();return;}
    if(e.key==='/'&&!typing&&!e.metaKey&&!e.ctrlKey&&!e.altKey){e.preventDefault();openPalette();}
  });

  /* 2) Animated typed focus line, respecting prefers-reduced-motion. */
  $$('[data-words]').forEach(el=>{
    const words=(el.dataset.words||'').split('|').filter(Boolean);
    if(!words.length)return;
    if(reduced){el.textContent=words[0].replace(/&amp;/g,'&');return;}
    let wi=0,ci=0,deleting=false;
    const tick=()=>{
      const word=words[wi]||'';
      el.textContent=deleting?word.slice(0,ci--):word.slice(0,ci++);
      let delay=deleting?32:55;
      if(!deleting&&ci>word.length){deleting=true;delay=1250;}
      else if(deleting&&ci<0){deleting=false;ci=0;wi=(wi+1)%words.length;delay=240;}
      window.setTimeout(tick,delay);
    };
    tick();
  });

  /* 3) Scroll reveals. Content remains visible if JS/Observer is unavailable. */
  const revealTargets=$$('.section-heading,.service-card,.project-card,.sample-card,.expertise-card,.experience-item,.detail-card,.engagement-grid article,.benefit-card');
  if(!reduced&&'IntersectionObserver'in window){
    revealTargets.forEach(el=>el.classList.add('reveal-pending'));
    root.classList.add('enhancements-ready');
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('reveal-visible');io.unobserve(entry.target);}
    }),{threshold:.08,rootMargin:'0px 0px -20px 0px'});
    revealTargets.forEach(el=>io.observe(el));
  }else{revealTargets.forEach(el=>el.classList.add('reveal-visible'));}

  /* 4) Gentle 3D tilt on the hero illustration, desktop/fine pointer only. */
  const orbit=$('.hero-orbit');
  if(orbit&&finePointer&&!reduced){
    orbit.addEventListener('pointermove',e=>{
      const r=orbit.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5;const y=(e.clientY-r.top)/r.height-.5;
      orbit.style.setProperty('--fx-tilt-x',(y*-2.4).toFixed(2)+'deg');
      orbit.style.setProperty('--fx-tilt-y',(x*3.6).toFixed(2)+'deg');
      orbit.classList.add('is-tilting');
    });
    orbit.addEventListener('pointerleave',()=>{orbit.style.setProperty('--fx-tilt-x','0deg');orbit.style.setProperty('--fx-tilt-y','0deg');orbit.classList.remove('is-tilting');});
  }

  /* 5) Project search and visible result count work together with the existing category filters. */
  const projectGrid=$('.project-grid');
  const projectCards=$$('.project-card',projectGrid||document);
  const search=$('#project-search'),count=$('#project-count');
  const filterButtons=$$('.filter-btn');
  let query='';
  function updateProjects(){
    if(!projectCards.length)return;
    const chosen=($('.filter-btn.active')?.dataset.filter||'All').toLowerCase();
    let shown=0;
    projectCards.forEach(card=>{
      const category=(card.dataset.category||'').toLowerCase();
      const text=(card.textContent||'').toLowerCase();
      const okCategory=chosen==='all'||category===chosen;
      const okQuery=!query||text.includes(query);
      const show=okCategory&&okQuery;
      card.hidden=!show;if(show)shown++;
    });
    if(count)count.textContent=shown+' of '+projectCards.length+' projects';
    const empty=$('#project-empty');
    if(empty)empty.classList.toggle('is-visible',shown===0);
  }
  search?.addEventListener('input',()=>{query=search.value.trim().toLowerCase();updateProjects()});
  filterButtons.forEach(btn=>btn.addEventListener('click',()=>window.setTimeout(updateProjects,0)));
  updateProjects();

  /* 6) Lifecycle explorer with an illustrative, source-grounded PayTrack trace. */
  const lifecycleButtons=$$('.lifecycle-step');
  const detail=$('#lifecycle-detail');
  if(lifecycleButtons.length&&detail){
    const title=$('#lifecycle-detail-title',detail),summary=$('#lifecycle-detail-summary',detail),outputs=$('#lifecycle-detail-outputs',detail),chain=$('#lifecycle-detail-chain',detail),note=$('#lifecycle-detail-note',detail);
    const renderStep=btn=>{
      lifecycleButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));
      if(title)title.textContent=btn.dataset.title||btn.textContent.trim();
      if(summary)summary.textContent=btn.dataset.summary||'';
      if(outputs)outputs.innerHTML=(btn.dataset.outputs||'').split('|').filter(Boolean).map(x=>'<span>'+x.replace(/[&<>"]/g,'')+'</span>').join('');
      if(chain)chain.innerHTML=(btn.dataset.chain||'').split('|').filter(Boolean).map((x,i)=>(i?'<b aria-hidden="true">→</b>':'')+'<span>'+x.replace(/[&<>"]/g,'')+'</span>').join('');
      if(note)note.textContent=btn.dataset.note||'Outputs are examples; the confirmed scope determines the final artifacts.';
    };
    lifecycleButtons.forEach(btn=>btn.addEventListener('click',()=>renderStep(btn)));
    const initial=lifecycleButtons.find(b=>b.getAttribute('aria-pressed')==='true')||lifecycleButtons[0];
    if(initial)renderStep(initial);
  }

  /* 7) Copy actions for public, non-sensitive contact details. */
  $$('[data-copy-text]').forEach(button=>button.addEventListener('click',async()=>{
    const value=button.dataset.copyText||'';
    const status=$('#copy-status',button.closest('.copy-group')||document);
    try{
      if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value);}
      else{
        const textarea=document.createElement('textarea');textarea.value=value;textarea.style.position='fixed';textarea.style.opacity='0';document.body.appendChild(textarea);textarea.select();
        const ok=document.execCommand('copy');textarea.remove();if(!ok)throw new Error('copy unavailable');
      }
      if(status)status.textContent='Copied to clipboard.';
      button.dataset.originalLabel=button.dataset.originalLabel||button.textContent;
      button.textContent='Copied ✓';window.setTimeout(()=>{button.textContent=button.dataset.originalLabel;},1700);
    }catch(_){if(status)status.textContent='Copy unavailable here — please select and copy the text manually.';}
  }));

  /* 8) Count-up for explicitly marked numeric résumé measures only. */
  const counters=$$('[data-count]');
  if(counters.length){
    counters.forEach(el=>{const end=Number(el.dataset.count);if(!Number.isFinite(end))return;const suffix=el.dataset.suffix||'';el.textContent='0'+suffix;});
    const animateCounters=()=>counters.forEach(el=>{
      if(el.dataset.counted)return;el.dataset.counted='true';
      const end=Number(el.dataset.count);if(!Number.isFinite(end))return;
      if(reduced){el.textContent=end.toLocaleString()+ (el.dataset.suffix||'');return;}
      const start=performance.now(),duration=950,suffix=el.dataset.suffix||'';
      const frame=now=>{const p=Math.min(1,(now-start)/duration);const eased=1-Math.pow(1-p,3);el.textContent=Math.round(end*eased).toLocaleString()+suffix;if(p<1)requestAnimationFrame(frame);};
      requestAnimationFrame(frame);
    });
    if('IntersectionObserver'in window){
      const counterObserver=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){animateCounters();counterObserver.disconnect();}});
      counters.forEach(el=>counterObserver.observe(el));
    }else animateCounters();
  }

  /* 9) Safe page-year update; no external services or stored form data. */
  const year=$('#year');if(year)year.textContent=new Date().getFullYear();
})();