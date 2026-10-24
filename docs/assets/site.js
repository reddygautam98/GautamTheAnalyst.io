/* Gautam Reddy portfolio v32: theme, mobile menu, project filter, contact form,
   smooth scroll (Lenis), scroll reveals, counters, subtle 3D tilt, flow parallax, role rotator. */
(function(){
var d=document,r=d.documentElement,$=function(s,c){return(c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;

/* theme toggle with SVG icons & meta theme-color sync */
var tb=$('#theme');
var SUN_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
var MOON_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

function paint(t){
  r.dataset.theme=t;
  if(tb){
    tb.setAttribute('aria-pressed',String(t==='dark'));
    tb.setAttribute('aria-label','Dark theme');
    tb.innerHTML=t==='dark'?SUN_ICO:MOON_ICO;
  }
  $$('meta[name="theme-color"]').forEach(function(m){
    m.setAttribute('content',t==='dark'?'#0b0f19':'#f8fafc');
  });
}
paint(r.dataset.theme||'light');
if(tb)tb.addEventListener('click',function(){
  var t=r.dataset.theme==='dark'?'light':'dark';
  paint(t);
  try{localStorage.setItem('gr-theme',t)}catch(e){}
});
try{
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(e){
    if(!localStorage.getItem('gr-theme'))paint(e.matches?'dark':'light');
  });
}catch(_){}

/* scroll reveal: runs immediately so JS never leaves page hidden */
var rvs=$$('.rv');
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('in');
        io.unobserve(e.target);
        countUp(e.target);
      }
    });
  },{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  rvs.forEach(function(el){io.observe(el)});
}else{
  rvs.forEach(function(el){el.classList.add('in');countUp(el)});
}

/* mobile menu with backdrop, scroll-lock & focus trap */
var mb=$('#menu'),nav=$('#nav'),bd=$('#navBackdrop');
function closeMenu(){
  if(nav&&nav.classList.contains('open')){
    nav.classList.remove('open');
    d.body.classList.remove('menu-open');
    if(mb){
      mb.setAttribute('aria-expanded','false');
      mb.setAttribute('aria-label','Menu');
      mb.innerHTML='&#9776;';
    }
    if(lenis)lenis.start();
  }
}
if(bd)bd.addEventListener('click',closeMenu);
if(mb&&nav){
  mb.addEventListener('click',function(){
    var o=nav.classList.toggle('open');
    d.body.classList.toggle('menu-open',o);
    mb.setAttribute('aria-expanded',String(o));
    mb.setAttribute('aria-label',o?'Close menu':'Menu');
    mb.innerHTML=o?'&times;':'&#9776;';
    if(o){
      var firstLink=nav.querySelector('a');
      if(firstLink)firstLink.focus();
    }
    if(lenis){if(o)lenis.stop();else lenis.start();}
  });
  d.addEventListener('keydown',function(e){
    if(!nav.classList.contains('open'))return;
    if(e.key==='Escape'){
      closeMenu();
      mb.focus();
      return;
    }
    if(e.key==='Tab'){
      var f=$$('a,button',nav).concat([tb,mb].filter(Boolean)).filter(function(x){return x&&x.offsetParent!==null});
      if(!f.length)return;
      var first=f[0],last=f[f.length-1];
      if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus()}
      else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus()}
    }
  });
  nav.addEventListener('click',function(e){
    if(e.target.tagName==='A')closeMenu();
  });
  d.addEventListener('click',function(e){
    if(nav.classList.contains('open')&&!nav.contains(e.target)&&!mb.contains(e.target)&&!(tb&&tb.contains(e.target))){
      closeMenu();
    }
  });
  try{
    window.matchMedia('(min-width:961px)').addEventListener('change',function(e){
      if(e.matches)closeMenu();
    });
  }catch(_){}
}

/* smooth scroll (Lenis) */
var lenis=null,header=$('.site-header'),bar=$('.progress');
if(!reduce&&window.Lenis){
  try{lenis=new Lenis({lerp:.085,wheelMultiplier:.95,smoothWheel:true})}catch(e){lenis=null}
}
function onScroll(){
  var y=window.scrollY||r.scrollTop,h=r.scrollHeight-innerHeight;
  if(bar)bar.style.setProperty('--sp',h>0?Math.min(1,y/h):0);
  if(header)header.classList.toggle('scrolled',y>8);
  flows.forEach(function(f){
    var b=f.s.getBoundingClientRect();
    if(b.bottom<-200||b.top>innerHeight+200)return;
    f.el.style.setProperty('--py',((b.top+b.height/2-innerHeight/2)*-.08).toFixed(1)+'px');
  });
  tl.forEach(function(t){
    var b=t.getBoundingClientRect(),p=(innerHeight*.72-b.top)/Math.max(1,b.height);
    t.style.setProperty('--tl',Math.max(.04,Math.min(1,p)).toFixed(3));
  });
}
var flows=$$('.has-flow').map(function(s){var el=$(':scope > .bgflow',s);return el&&!s.classList.contains('cta')?{s:s,el:el}:null}).filter(Boolean);
var tl=reduce?[]:$$('.roles');
var ticking=false;
function throttledScroll(){if(!ticking){ticking=true;requestAnimationFrame(function(){onScroll();ticking=false})}}
if(lenis){lenis.on('scroll',onScroll);(function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(0)}
else addEventListener('scroll',throttledScroll,{passive:true});
addEventListener('resize',throttledScroll);
onScroll();

/* in-page anchors with keyboard focus management */
d.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href^="#"]');
  if(!a||a.getAttribute('href').length<2)return;
  var hash=a.getAttribute('href');
  var t=null;
  try{t=$(hash)}catch(err){t=null}
  if(!t)return;
  e.preventDefault();
  var focusTarget=function(){
    if(!t.hasAttribute('tabindex'))t.setAttribute('tabindex','-1');
    t.focus({preventScroll:true});
    try{history.pushState(null,'',hash)}catch(_){}
  };
  if(lenis){
    lenis.scrollTo(t,{offset:-84,onComplete:focusTarget});
  }else{
    t.scrollIntoView({behavior:reduce?'auto':'smooth'});
    focusTarget();
  }
});

/* deep-link hash scroll and glow */
function checkHash(){
  var h=window.location.hash;
  if(!h||h.length<2)return;
  try{
    var target=$(h);
    if(target){
      setTimeout(function(){
        if(lenis)lenis.scrollTo(target,{offset:-90});
        else target.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});
        target.classList.add('target-glow');
        setTimeout(function(){target.classList.remove('target-glow')},2800);
      },250);
    }
  }catch(err){}
}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',checkHash);else checkHash();
window.addEventListener('hashchange',checkHash);

/* Pause off-screen background animations to save CPU / GPU */
if('IntersectionObserver' in window&&!reduce){
  var animObserver=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      var off=!entry.isIntersecting;
      entry.target.classList.toggle('is-offscreen',off);
      var svgs=entry.target.tagName==='svg'?[entry.target]:$$('svg',entry.target);
      svgs.forEach(function(s){
        try{
          if(off&&s.pauseAnimations)s.pauseAnimations();
          else if(!off&&s.unpauseAnimations&&!reduce&&!r.classList.contains('is-anim-paused'))s.unpauseAnimations();
        }catch(_){}
      });
    });
  },{rootMargin:'100px'});
  $$('.bgflow, .marq-track').forEach(function(el){
    animObserver.observe(el);
  });
}

/* animated counters */
function countUp(root){
  $$('[data-count]',root).concat(root.hasAttribute&&root.hasAttribute('data-count')?[root]:[]).forEach(function(b){
    if(b.dataset.done)return;
    b.dataset.done='1';
    var end=+b.dataset.count,suf=b.dataset.suf||'';
    if(reduce||!end){b.textContent=end+suf;return}
    var t0=performance.now(),dur=1200;
    (function step(t){
      var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,4);
      b.textContent=Math.round(end*e)+suf;
      if(p<1)requestAnimationFrame(step);
    })(t0);
  });
}
window.addEventListener('beforeprint',function(){
  $$('[data-count]').forEach(function(b){
    var end=+b.dataset.count,suf=b.dataset.suf||'';
    b.dataset.done='1';
    b.textContent=end+suf;
  });
});

/* 3D tilt on featured cards only (subtle range) */
if(fine&&!reduce){
  $$('[data-tilt]').forEach(function(el){
    var max=el.classList.contains('cta')?5:6;
    el.addEventListener('pointermove',function(e){
      var b=el.getBoundingClientRect(),x=(e.clientX-b.left)/b.width,y=(e.clientY-b.top)/b.height;
      el.classList.add('tilting');
      el.style.setProperty('--ry',((x-.5)*2*max).toFixed(2)+'deg');
      el.style.setProperty('--rx',((.5-y)*2*max).toFixed(2)+'deg');
      el.style.setProperty('--mx',(x*100).toFixed(1)+'%');
      el.style.setProperty('--my',(y*100).toFixed(1)+'%');
    });
    el.addEventListener('pointerleave',function(){
      el.classList.remove('tilting');
      el.style.setProperty('--rx','0deg');
      el.style.setProperty('--ry','0deg');
    });
  });
}

/* hero keyword rotator with accessible aria-hidden tracking */
var rot=$('[data-rot]');
if(rot&&!reduce){
  var ws=$$('span',rot),rotIdx=0;
  if(ws.length){
    rot.setAttribute('data-live','1');
    ws.forEach(function(w,idx){
      w.setAttribute('aria-hidden',idx===0?'false':'true');
    });
    ws[0].classList.add('on');
    setInterval(function(){
      if(d.hidden||r.classList.contains('is-anim-paused'))return;
      ws[rotIdx].classList.remove('on');
      ws[rotIdx].setAttribute('aria-hidden','true');
      rotIdx=(rotIdx+1)%ws.length;
      ws[rotIdx].classList.add('on');
      ws[rotIdx].setAttribute('aria-hidden','false');
    },3200);
  }
}

/* site-wide animation & marquee pause toggle button (WCAG 2.2.2) */
var mqToggle=$('#marqToggle'),mqWrap=$('.marq-wrap');
var PAUSE_ICO='<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>';
var PLAY_ICO='<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"/></svg>';
if(mqToggle){
  mqToggle.addEventListener('click',function(){
    var paused=r.classList.toggle('is-anim-paused');
    if(mqWrap)mqWrap.classList.toggle('is-paused',paused);
    mqToggle.setAttribute('aria-pressed',String(paused));
    mqToggle.setAttribute('aria-label',paused?'Resume animations':'Pause animations');
    mqToggle.innerHTML=paused?PLAY_ICO:PAUSE_ICO;
    $$('svg.bgflow').forEach(function(s){
      try{if(paused)s.pauseAnimations();else if(!reduce)s.unpauseAnimations();}catch(_){}
    });
  });
}

/* pause decorative SMIL motion when asked to reduce motion */
if(reduce)$$('svg.bgflow').forEach(function(s){try{s.pauseAnimations()}catch(e){}});

/* project filter: sliding pill indicator and FLIP reflow animation */
var chips=$$('.chip[data-f]');
if(chips.length){
  var cards=$$('[data-cat]'),count=$('#count'),pill=$('#filterPill'),filterGroup=$('.filters');
  function setPill(activeChip){
    if(!pill||!activeChip)return;
    pill.style.width=activeChip.offsetWidth+'px';
    pill.style.height=activeChip.offsetHeight+'px';
    pill.style.transform='translate('+activeChip.offsetLeft+'px, '+activeChip.offsetTop+'px)';
  }
  var initActive=$('.chip[data-f].is-active')||chips[0];
  if(initActive){
    setPill(initActive);
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){setPill($('.chip[data-f].is-active')||chips[0])});
    setTimeout(function(){setPill($('.chip[data-f].is-active')||chips[0])},60);
  }
  window.addEventListener('resize',function(){var a=$('.chip[data-f][aria-pressed=true]')||$('.chip[data-f].is-active');if(a)setPill(a)});
  if('ResizeObserver' in window&&filterGroup){
    new ResizeObserver(function(){var a=$('.chip[data-f][aria-pressed=true]')||$('.chip[data-f].is-active');if(a)setPill(a)}).observe(filterGroup);
  }

  chips.forEach(function(c){
    c.addEventListener('click',function(){
      var f=c.dataset.f,n=0;
      chips.forEach(function(x){
        var active=x===c;
        x.setAttribute('aria-pressed',String(active));
        x.classList.toggle('is-active',active);
      });
      setPill(c);

      /* FLIP Animation: First */
      var firstRects=new Map();
      cards.forEach(function(k){firstRects.set(k,k.getBoundingClientRect())});

      /* Apply visibility */
      cards.forEach(function(k){
        var match=f==='all'||k.dataset.cat===f;
        if(match){
          n++;
          k.hidden=false;
          k.classList.remove('out');
        }else{
          k.hidden=true;
          k.classList.add('out');
        }
      });

      /* FLIP Animation: Last, Invert, Play */
      if(!reduce){
        cards.forEach(function(k){
          if(k.hidden)return;
          var first=firstRects.get(k);
          if(!first)return;
          var last=k.getBoundingClientRect();
          var dx=first.left-last.left,dy=first.top-last.top;
          if(dx!==0||dy!==0){
            k.style.transform='translate('+dx+'px, '+dy+'px)';
            k.style.transition='none';
            requestAnimationFrame(function(){
              k.style.transition='transform 0.4s cubic-bezier(0,0,0.2,1)';
              k.style.transform='';
              setTimeout(function(){k.style.transition=''},420);
            });
          }
        });
      }

      if(count){
        count.textContent=n+(n===1?' project':' projects');
      }
      if(lenis)setTimeout(function(){lenis.resize()},200);
    });
  });
  var filterFromHash=function(){
    var h=(location.hash||'').slice(1).replace(/[^a-z0-9_-]/gi,'');
    if(!h)return;
    var chip=$('.chip[data-f="'+h+'"]');
    if(chip){
      chip.click();
      var pgrid=$('#pgrid')||$('.filters');
      if(pgrid){
        setTimeout(function(){
          if(lenis)lenis.scrollTo(pgrid,{offset:-90});
          else pgrid.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
        },100);
      }
    }
  };
  filterFromHash();
  addEventListener('hashchange',filterFromHash);
}

/* contact form: validate required, email & optional URL, clear on input, truthful draft flow */
var f=$('#enquiry');
if(f){
  f.setAttribute('novalidate','');
  var isValidUrl=function(str){
    if(!str)return true;
    try{
      var u=new URL(str);
      return u.protocol==='http:'||u.protocol==='https:';
    }catch(_){
      return false;
    }
  };

  /* clear errors and manage float state on input */
  $$('input, textarea, select',f).forEach(function(i){
    var clear=function(){
      i.setAttribute('aria-invalid','false');
      var errSpan=$('#err-'+i.name,f)||(i.parentNode&&i.parentNode.querySelector('.err'));
      if(errSpan)errSpan.textContent='';
      if(i.tagName==='SELECT')i.classList.toggle('has-val',!!i.value);
    };
    i.addEventListener('input',clear);
    i.addEventListener('change',clear);
  });

  /* prefill service from query parameter */
  try{
    var q=new URLSearchParams(location.search).get('service');
    var sField=$('#enquiry-service')||f.elements['service'];
    if(q&&sField){
      var cleanQ=q.trim().toLowerCase();
      [].some.call(sField.options,function(o){
        if(o.text.trim().toLowerCase()===cleanQ||o.value.trim().toLowerCase()===cleanQ){
          sField.value=o.value||o.text;
          sField.classList.add('has-val');
          return true;
        }
      });
    }
  }catch(_){}

  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=true,em=/^[^\s@]+@[^\s@]+\.[^\s@]+$/,errCount=0;
    var errBox=$('#form-errors');
    $$('[required]',f).forEach(function(i){
      var errSpan=$('#err-'+i.name,f)||(i.parentNode&&i.parentNode.querySelector('.err')),
          bad=!i.value.trim()||(i.type==='email'&&!em.test(i.value.trim()));
      if(errSpan)errSpan.textContent=bad?(i.type==='email'?'Please enter a valid email address.':'This field is required.'):'';
      i.setAttribute('aria-invalid',String(bad));
      if(bad){
        errCount++;
        if(ok){i.focus();ok=false}
      }
    });

    var refInput=f.elements['ref'];
    if(refInput&&refInput.value.trim()){
      var urlBad=!isValidUrl(refInput.value.trim());
      var refErr=$('#err-ref',f)||(refInput.parentNode&&refInput.parentNode.querySelector('.err'));
      if(refErr)refErr.textContent=urlBad?'Please enter a valid URL starting with https:// or http://':'';
      refInput.setAttribute('aria-invalid',String(urlBad));
      if(urlBad){
        errCount++;
        if(ok){refInput.focus();ok=false}
      }
    }

    if(errBox){
      if(errCount>0){
        errBox.textContent='Please correct '+errCount+' error'+(errCount===1?'':'s')+' below before submitting.';
        errBox.hidden=false;
      }else{
        errBox.hidden=true;
      }
    }

    if(!ok)return;
    var v=function(n){return(f.elements[n]&&f.elements[n].value||'').trim()};
    var body=['Name: '+v('name'),'Email: '+v('email'),'Company: '+(v('company')||'-'),'Service: '+v('service'),'Engagement: '+v('type'),'Timeline: '+v('timeline'),'Reference: '+(v('ref')||'-'),'','What I need:',v('msg')].join('\n');
    location.href='mailto:gautamreddy098@gmail.com?subject='+encodeURIComponent('Project enquiry: '+v('service'))+'&body='+encodeURIComponent(body);
    var s=$('#sent');
    if(s){
      s.hidden=false;
      s.setAttribute('tabindex','-1');
      s.focus();
    }
  });

  /* copy message helper for enquiries with reliable fallback */
  var copyEnquiryBtn=$('#copyEnquiryBtn');
  if(copyEnquiryBtn){
    copyEnquiryBtn.addEventListener('click',function(){
      var v=function(n){return(f.elements[n]&&f.elements[n].value||'').trim()};
      var body=['Name: '+v('name'),'Email: '+v('email'),'Company: '+(v('company')||'-'),'Service: '+v('service'),'Engagement: '+v('type'),'Timeline: '+v('timeline'),'Reference: '+(v('ref')||'-'),'','What I need:',v('msg')].join('\n');
      if(!v('name')&&!v('msg')){
        copyEnquiryBtn.textContent='Fill form first';
        setTimeout(function(){copyEnquiryBtn.textContent='Copy message'},2000);
        return;
      }
      var orig=copyEnquiryBtn.textContent;
      function done(msg){
        copyEnquiryBtn.textContent=msg;
        setTimeout(function(){copyEnquiryBtn.textContent=orig},2000);
      }
      function fallback(){
        try{
          var ta=d.createElement('textarea');
          ta.value=body;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;opacity:0';
          d.body.appendChild(ta);ta.select();
          var ok=d.execCommand('copy');d.body.removeChild(ta);
          done(ok?'Copied!':'Press Ctrl+C');
        }catch(_){done('Press Ctrl+C')}
      }
      if(navigator.clipboard&&window.isSecureContext){
        navigator.clipboard.writeText(body).then(function(){done('Copied!')}).catch(fallback);
      }else fallback();
    });
  }
}

/* clipboard copy helper */
$$('[data-copy]').forEach(function(b){
  b.addEventListener('click',function(){
    var t=b.dataset.copy,o=b.textContent;
    function done(msg){b.textContent=msg;setTimeout(function(){b.textContent=o},1800)}
    function fallback(){
      try{
        var ta=d.createElement('textarea');
        ta.value=t;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;opacity:0';
        d.body.appendChild(ta);ta.select();
        var ok=d.execCommand('copy');d.body.removeChild(ta);
        done(ok?'Copied':'Press Ctrl+C');
      }catch(err){done('Press Ctrl+C')}
    }
    if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(function(){done('Copied')},fallback);
    else fallback();
  });
});
d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});

/* signature BA traceability: hover (mouse), tap/click and keyboard focus */
var traceRows=$$('[data-links]');
if(traceRows.length){
  var traceIds=$$('[data-id]'),stage=$('.stage');
  var setTrace=function(on,row){
    var set={};
    (row.dataset.links||'').split(/\s+/).forEach(function(k){if(k)set[k]=true});
    traceIds.forEach(function(el){el.classList.toggle('is-linked',on&&!!set[el.dataset.id])});
    row.classList.toggle('is-source',on);
    if(stage)stage.toggleAttribute('data-trace-on',on);
  };
  var clearAll=function(except){
    traceRows.forEach(function(r){if(r!==except&&r.classList.contains('is-source'))setTrace(false,r)});
  };
  traceRows.forEach(function(row){
    row.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse'){clearAll(row);setTrace(true,row)}});
    row.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')setTrace(false,row)});
    row.addEventListener('focusin',function(){clearAll(row);setTrace(true,row)});
    row.addEventListener('focusout',function(e){
      if(e.relatedTarget&&row.contains(e.relatedTarget))return;
      setTrace(false,row);
    });
    row.addEventListener('click',function(e){
      if(e.target.closest&&e.target.closest('a'))return;
      var on=!row.classList.contains('is-source');
      clearAll(row);
      setTrace(on,row);
    });
  });
}

/* hero multi-deliverable slider with WAI-ARIA tablist accessibility */
var slider=$('#heroSlider');
if(slider){
  var tabs=$$('.slider-tab',slider),
      slides=$$('.slider-slide',slider),
      prevBtn=$('#slidePrev',slider),
      nextBtn=$('#slideNext',slider),
      countEl=$('#slideCount',slider),
      tablist=$('.slider-tabs',slider),
      currIdx=0,
      totalSlides=slides.length;

  var showSlide=function(idx){
    if(idx<0)idx=totalSlides-1;
    if(idx>=totalSlides)idx=0;
    currIdx=idx;
    tabs.forEach(function(t,i){
      var active=i===currIdx;
      t.classList.toggle('is-active',active);
      t.setAttribute('aria-selected',active?'true':'false');
      t.setAttribute('tabindex',active?'0':'-1');
    });
    slides.forEach(function(s,i){
      var active=i===currIdx;
      s.classList.toggle('is-active',active);
      s.hidden=!active;
    });
    if(countEl)countEl.textContent=(currIdx+1)+' / '+totalSlides;
  };

  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){showSlide(i)});
  });
  if(prevBtn)prevBtn.addEventListener('click',function(){showSlide(currIdx-1)});
  if(nextBtn)nextBtn.addEventListener('click',function(){showSlide(currIdx+1)});

  /* WAI-ARIA tablist keyboard navigation on tabs */
  if(tablist){
    tablist.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'||e.key==='ArrowDown'){
        e.preventDefault();
        var next=(currIdx+1)%totalSlides;
        showSlide(next);
        tabs[next].focus();
      }else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){
        e.preventDefault();
        var prev=(currIdx-1+totalSlides)%totalSlides;
        showSlide(prev);
        tabs[prev].focus();
      }else if(e.key==='Home'){
        e.preventDefault();
        showSlide(0);
        tabs[0].focus();
      }else if(e.key==='End'){
        e.preventDefault();
        showSlide(totalSlides-1);
        tabs[totalSlides-1].focus();
      }
    });
  }

  /* touch swipe navigation */
  var touchX=0;
  slider.addEventListener('touchstart',function(e){
    if(e.touches&&e.touches.length===1)touchX=e.touches[0].clientX;
  },{passive:true});
  slider.addEventListener('touchend',function(e){
    if(e.changedTouches&&e.changedTouches.length===1){
      var dx=e.changedTouches[0].clientX-touchX;
      if(Math.abs(dx)>40){
        if(dx<0)showSlide(currIdx+1);
        else showSlide(currIdx-1);
      }
    }
  },{passive:true});
}

/* About BA Console: Interactive Tab Navigation with Home/End support */
var abConsole=$('.about-console');
if(abConsole){
  var abTabs=$$('.console-tab',abConsole),
      abPanels=$$('.console-panel',abConsole);
  if(abTabs.length&&abPanels.length){
    abTabs.forEach(function(tab,idx){
      tab.addEventListener('click',function(){
        abTabs.forEach(function(t,i){
          var sel=i===idx;
          t.classList.toggle('is-active',sel);
          t.setAttribute('aria-selected',sel?'true':'false');
          t.tabIndex=sel?0:-1;
        });
        abPanels.forEach(function(p,i){
          var sel=i===idx;
          p.classList.toggle('is-active',sel);
          p.hidden=!sel;
        });
      });
      tab.addEventListener('keydown',function(e){
        var next=-1;
        if(e.key==='ArrowRight'||e.key==='ArrowDown')next=(idx+1)%abTabs.length;
        else if(e.key==='ArrowLeft'||e.key==='ArrowUp')next=(idx-1+abTabs.length)%abTabs.length;
        else if(e.key==='Home')next=0;
        else if(e.key==='End')next=abTabs.length-1;
        if(next>=0){
          e.preventDefault();
          abTabs[next].focus();
          abTabs[next].click();
        }
      });
    });
  }
}

/* Selected Work: PayTrack Wireframe Active Row Cycling */
var wfRows=$$('.wf-row-cycle');
if(wfRows.length&&!reduce){
  var wfIdx=0;
  setInterval(function(){
    if(d.hidden||r.classList.contains('is-anim-paused'))return;
    wfRows.forEach(function(r,i){
      r.classList.toggle('is-active-row',i===wfIdx);
    });
    wfIdx=(wfIdx+1)%wfRows.length;
  },2400);
}

/* Experience: Collapsible Role Metrics Tray with constant accessible label */
$$('.role-expander').forEach(function(btn){
  btn.addEventListener('click',function(){
    var metrics=btn.nextElementSibling;
    if(!metrics)return;
    var isHidden=metrics.hidden;
    metrics.hidden=!isHidden;
    btn.setAttribute('aria-expanded',String(isHidden));
    if(lenis)setTimeout(function(){lenis.resize()},150);
  });
});

/* Print Resume Button */
var printBtn=$('#printResumeBtn');
if(printBtn){
  printBtn.addEventListener('click',function(){
    window.print();
  });
}

/* Samples: In-Page Document Preview Drawer Modal with focus trap & scroll lock */
var pdDrawer=$('#previewDrawer'),pdBackdrop=$('#pdBackdrop'),pdClose=$('#pdClose'),pdPanel=$('.pd-panel');
var lastActiveElement=null;
function openDrawer(tabName){
  if(!pdDrawer)return;
  lastActiveElement=d.activeElement;
  if(lenis)lenis.stop();
  pdDrawer.hidden=false;
  d.body.style.overflow='hidden';
  var targetTab=(tabName&&tabName!=='bundle')?tabName:'brd';
  var pdTitle=$('#pdTitle');
  if(pdTitle){
    pdTitle.textContent=(tabName==='bundle')?'PayTrack BA Deliverables Bundle':'Document Preview';
  }
  showPdTab(targetTab);
  if(pdClose)pdClose.focus();
}
function closeDrawer(){
  if(!pdDrawer)return;
  pdDrawer.hidden=true;
  d.body.style.overflow='';
  if(lenis)lenis.start();
  if(lastActiveElement&&lastActiveElement.focus)lastActiveElement.focus();
}
if(pdBackdrop)pdBackdrop.addEventListener('click',closeDrawer);
if(pdClose)pdClose.addEventListener('click',closeDrawer);
d.addEventListener('keydown',function(e){
  if(!pdDrawer||pdDrawer.hidden)return;
  if(e.key==='Escape'){closeDrawer();return;}
  if(e.key==='Tab'&&pdPanel){
    var focusables=$$('a,button,[tabindex]:not([tabindex="-1"])',pdPanel).filter(function(x){return x.offsetParent!==null});
    if(!focusables.length)return;
    var first=focusables[0],last=focusables[focusables.length-1];
    if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus();}
  }
});
$$('[data-preview]').forEach(function(btn){
  btn.addEventListener('click',function(){openDrawer(btn.dataset.preview)});
});
var pdTabs=$$('.pd-tab'),pdPanes=$$('.pd-pane');
function showPdTab(name){
  pdTabs.forEach(function(t){
    var on=t.dataset.pdtab===name;
    t.classList.toggle('is-active',on);
    t.setAttribute('aria-selected',String(on));
    t.setAttribute('tabindex',on?'0':'-1');
  });
  pdPanes.forEach(function(p){
    var on=p.id==='pd-'+name;
    p.hidden=!on;
  });
}
pdTabs.forEach(function(t){
  t.addEventListener('click',function(){showPdTab(t.dataset.pdtab)});
});

})();
