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


  /* 10) Restrained cursor spotlights, rotated borders, and resilient project previews. */
  const spotlightTargets=$('.service-card,.project-card,.sample-card,.sample-feature-card,.lifecycle-detail,.contact-info-card,.contact-form-card,.detail-card');
  spotlightTargets.forEach(el=>{
    el.classList.add('fx-spotlight');
    el.addEventListener('pointermove',e=>{
      if(!finePointer||reduced)return;
      const r=el.getBoundingClientRect();
      el.style.setProperty('--fx-spot-x',Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100))+'%');
      el.style.setProperty('--fx-spot-y',Math.max(0,Math.min(100,(e.clientY-r.top)/r.height*100))+'%');
    });
  });
  $('.lifecycle-detail,.contact-form-card,.sample-feature-card').forEach(el=>el.classList.add('fx-gradient-border'));
  $('img').forEach(img=>{
    img.addEventListener('error',()=>{
      if(img.dataset.fallbackHandled)return;
      img.dataset.fallbackHandled='true';
      const link=img.closest('a.snapshot-open');
      const fallback=document.createElement('div');
      fallback.className='preview-fallback';
      fallback.innerHTML='<strong>Preview unavailable</strong><span>The source image could not be loaded.</span>';
      if(link)link.replaceWith(fallback);else img.replaceWith(fallback);
    },{once:true});
  });

  /* 9) Safe page-year update; no external services or stored form data. */
  const year=$('#year');if(year)year.textContent=new Date().getFullYear();
  /* Load the shared 3D effects layer on every page (including BA Samples). */
  const fx3dScript=document.createElement('script');
  fx3dScript.src=base+'assets/js/fx3d.js';
  fx3dScript.defer=true;
  document.head.appendChild(fx3dScript);

})();


/* Portfolio patterns 2026 (v4). No new libraries; all controls remain keyboard reachable. */
(function(){
  'use strict';
  const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>Array.from(c.querySelectorAll(s));
  const reduce=!!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const fine=!!(window.matchMedia&&window.matchMedia('(hover: hover) and (pointer: fine)').matches);

  /* Giant wordmark shared by every page footer; add only once. */
  const footer=$('footer.site-footer')||$('footer');
  if(footer&&!$('.mega-word',footer)){
    const word=document.createElement('div');
    word.className='mega-word';word.setAttribute('aria-hidden','true');word.textContent='GAUTAM · THE ANALYST';
    footer.insertBefore(word,footer.firstChild);
  }

  /* Kinetic, word-by-word headline entrance. Preserve inline accent spans and normal spacing. */
  if(!reduce){
    let wordIndex=0;
    const skipTags=new Set(['SCRIPT','STYLE','SVG','PATH','BUTTON','INPUT','TEXTAREA','SELECT','CODE','KBD']);
    const makeKinetic=(heading)=>{
      if(heading.dataset.kineticReady==='1')return;
      heading.dataset.kineticReady='1';
      const walker=document.createTreeWalker(heading,NodeFilter.SHOW_TEXT,{
        acceptNode(node){
          if(!node.nodeValue||!node.nodeValue.trim())return NodeFilter.FILTER_REJECT;
          let el=node.parentElement;
          while(el&&el!==heading){if(skipTags.has(el.tagName)||el.closest('.typed,.toolkit-ticker,.visually-hidden'))return NodeFilter.FILTER_REJECT;el=el.parentElement;}
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
      nodes.forEach(node=>{
        const parts=node.nodeValue.split(/(\s+)/);if(!parts.some(x=>x.trim()))return;
        const frag=document.createDocumentFragment();
        parts.forEach(part=>{
          if(/^\s+$/.test(part)||!part){frag.append(document.createTextNode(part));return;}
          const span=document.createElement('span');span.className='kinetic-word';span.style.setProperty('--p26-i',Math.min(wordIndex++,16));span.textContent=part;frag.append(span);
        });
        node.parentNode.replaceChild(frag,node);
      });
    };
    $$('h1,.section-heading h2').forEach(makeKinetic);
  }

  /* Subtle magnetic movement on primary CTA buttons. */
  if(fine&&!reduce){
    $$('.btn-primary').forEach(btn=>{
      btn.classList.add('magnetic');
      btn.addEventListener('pointermove',e=>{
        const r=btn.getBoundingClientRect(),dx=(e.clientX-r.left-r.width/2)/Math.max(1,r.width/2),dy=(e.clientY-r.top-r.height/2)/Math.max(1,r.height/2);
        btn.style.setProperty('--p26-mx',(dx*4).toFixed(1)+'px');
        btn.style.setProperty('--p26-my',(dy*3).toFixed(1)+'px');
      },{passive:true});
      btn.addEventListener('pointerleave',()=>{btn.style.setProperty('--p26-mx','0px');btn.style.setProperty('--p26-my','0px');});
    });
  }

  /* Home-only scroll-synced marquee and section position indicator. */
  const isHome=!!$('#home');
  if(isHome){
    if(!$('.mq')){
      const marquee=document.createElement('div');marquee.className='mq';marquee.setAttribute('aria-hidden','true');
      marquee.innerHTML='<div class="mq-row"><span>BUSINESS ANALYSIS</span><b>·</b><span>DATA-DRIVEN DELIVERY</span><i>·</i><span>REQUIREMENTS TO RESULTS</span><b>·</b><span>BUSINESS ANALYSIS</span><i>·</i></div>';
      (footer||$('main')).before(marquee);
    }
    const targets=[
      ['home','Start'],['proof','Evidence'],['lifecycle','Lifecycle'],['case-studies','Case studies'],['ba-samples','BA samples'],['process','Handover'],['contact','Contact']
    ].filter(([id])=>$('#'+id));
    if(targets.length>1&&!$('.dots')){
      const nav=document.createElement('nav');nav.className='dots';nav.setAttribute('aria-label','Section navigation');
      targets.forEach(([id,label],i)=>{const a=document.createElement('a');a.href='#'+id;a.setAttribute('aria-label',label);if(i===0)a.classList.add('on');const span=document.createElement('span');span.textContent=label;a.append(span);nav.append(a);});
      document.body.append(nav);
      if('IntersectionObserver'in window){
        const observer=new IntersectionObserver(entries=>{
          entries.forEach(entry=>{if(entry.isIntersecting)$$('.dots a',nav).forEach(a=>a.classList.toggle('on',a.hash==='#'+entry.target.id));});
        },{rootMargin:'-38% 0px -48% 0px',threshold:0});
        targets.forEach(([id])=>observer.observe($('#'+id)));
      }
    }
  }

  /* Build a view switch next to the existing search; preserve the current filter/search logic. */
  const tools=$('.project-tools'),projectGrid=$('#project-grid');
  if(tools&&projectGrid&&!$('.view-toggle',tools)){
    const toggle=document.createElement('div');toggle.className='view-toggle';toggle.setAttribute('role','group');toggle.setAttribute('aria-label','Project layout');
    toggle.innerHTML='<button type="button" class="vt" data-view="grid" aria-pressed="true">▦ Grid</button><button type="button" class="vt" data-view="list" aria-pressed="false">☰ List</button>';
    const search=$('.project-search-wrap',tools);tools.insertBefore(toggle,search||tools.firstChild);
    toggle.addEventListener('click',e=>{
      const button=e.target.closest('button[data-view]');if(!button)return;
      const list=button.dataset.view==='list';projectGrid.classList.toggle('list',list);
      $$('button[data-view]',toggle).forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    });
  }

  /* Sticky resume snapshot is generated from existing verified resume metrics. */
  const experienceCard=$('.experience-section .experience-card');
  if(experienceCard&&!$('.resume-evidence-layout')){
    const layout=document.createElement('div');layout.className='resume-evidence-layout';
    const aside=document.createElement('aside');aside.className='resume-snapshot-2026';
    aside.innerHTML='<span class="detail-kicker">DELIVERY SNAPSHOT</span><h3>Business Analyst</h3><p>Requirements, data analysis, API integration, Agile delivery and UAT coordination.</p><div class="chip-cloud"><span>BRD / FRD</span><span>User stories</span><span>RTM</span><span>SQL</span><span>Power BI</span><span>UAT</span></div><div class="resume-snapshot-stats"><span><b>100K+</b>records analyzed</span><span><b>350+</b>test cases</span><span><b>2</b>integrations</span><span><b>20+</b>workshops</span></div><p style="margin-top:14px"><a href="contact.html#project-enquiry">Discuss a role or project ↗</a></p>';
    const parent=experienceCard.parentNode;parent.insertBefore(layout,experienceCard);layout.append(aside,experienceCard);
  }

  /* Progress-fill the scroll-told process; add depth to the sticky case stack. */
  let raf=0;
  const paintScrollPatterns=()=>{
    raf=0;
    $$('.process-grid').forEach(grid=>{
      const r=grid.getBoundingClientRect(),h=Math.max(1,r.height);
      const p=Math.max(0,Math.min(1,(innerHeight*.86-r.top)/(h+innerHeight*.24)));
      grid.style.setProperty('--p',p.toFixed(3));
    });
    if(!reduce)$$('.case-stack .case').forEach((card,i)=>{
      const r=card.getBoundingClientRect();
      if(r.top<112){
        const depth=Math.max(0,Math.min(1,(112-r.top)/Math.max(140,r.height)));
        const scale=Math.max(.91,1-(i*.018)-(depth*.025));
        card.style.setProperty('--case-depth',depth.toFixed(3));
        card.style.transform='scale('+scale.toFixed(3)+')';
        card.style.filter='saturate('+(1-depth*.1).toFixed(3)+')';
      }else{card.style.transform='';card.style.filter='';}
    });
    const row=$('.mq-row');
    if(row&&!reduce){const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);row.style.transform='translate3d('+(-Math.min(.4,scrollY/max*.4)*100).toFixed(2)+'%,0,0)';}
  };
  const requestScrollPaint=()=>{if(!raf)raf=requestAnimationFrame(paintScrollPatterns);};
  addEventListener('scroll',requestScrollPaint,{passive:true});
  addEventListener('resize',requestScrollPaint,{passive:true});
  requestScrollPaint();

  /* Reduced-motion users still get all content and static layout, not animation. */
  if(reduce){
    $$('.kinetic-word').forEach(span=>{span.style.opacity='1';span.style.transform='none';});
    $$('.case').forEach(card=>{card.style.transform='none';card.style.filter='none';});
  }
})();
