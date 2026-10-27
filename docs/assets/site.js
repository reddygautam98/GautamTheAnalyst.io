/* Gautam Reddy portfolio: theme, mobile menu, project filter, contact form,
   smooth scroll (Lenis), scroll reveals, counters, subtle 3D tilt, flow parallax, role rotator. */
(function(){
var d=document,r=d.documentElement,$=function(s,c){return(c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
var SCROLL_OFFSET = -84;

/* theme toggle with SVG icons & meta theme-color sync */
var tb=$('#theme');
var SUN_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
var MOON_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

function paint(t){
  r.dataset.theme=t;
  if(tb){
    tb.setAttribute('aria-pressed',String(t==='dark'));
    tb.setAttribute('aria-label','Toggle dark theme');
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

/* mobile menu with backdrop, scroll-lock & focus trap (GL-7) */
var mb=$('#menu'),nav=$('#nav'),bd=$('#navBackdrop'),header=$('.site-header');
var MENU_ICO='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
var CLOSE_ICO='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';

function closeMenu(){
  if(nav&&nav.classList.contains('open')){
    nav.classList.remove('open');
    d.body.classList.remove('menu-open');
    if(mb){
      mb.setAttribute('aria-expanded','false');
      mb.setAttribute('aria-label','Open navigation menu');
      mb.innerHTML=MENU_ICO;
    }
  }
}
if(bd)bd.addEventListener('click',closeMenu);
if(mb&&nav){
  mb.addEventListener('click',function(e){
    if(e&&e.stopPropagation)e.stopPropagation();
    var o=nav.classList.toggle('open');
    d.body.classList.toggle('menu-open',o);
    mb.setAttribute('aria-expanded',String(o));
    mb.setAttribute('aria-label',o?'Close navigation menu':'Open navigation menu');
    mb.innerHTML=o?CLOSE_ICO:MENU_ICO;
    if(o){
      var firstLink=nav.querySelector('a');
      if(firstLink)firstLink.focus();
    }
  });
  d.addEventListener('keydown',function(e){
    if(!nav.classList.contains('open'))return;
    if(e.key==='Escape'){
      closeMenu();
      mb.focus();
      return;
    }
    if(e.key==='Tab'&&header){
      var f=$$('a,button,[tabindex]:not([tabindex="-1"])',header).filter(function(x){
        return x&&x.offsetParent!==null&&!x.closest('[hidden]');
      });
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
    var inMb = (mb && mb.contains(e.target)) || (e.target && e.target.closest && e.target.closest('#menu')) || (e.composedPath && e.composedPath().indexOf(mb) !== -1);
    if(nav.classList.contains('open')&&!nav.contains(e.target)&&!inMb&&!(tb&&tb.contains(e.target))){
      closeMenu();
    }
  });
  try{
    window.matchMedia('(min-width:961px)').addEventListener('change',function(e){
      if(e.matches)closeMenu();
    });
  }catch(_){}
}

/* scroll progress & parallax tracking */
var bar=$('.progress');
function onScroll(){
  var y=window.scrollY||r.scrollTop,h=r.scrollHeight-innerHeight;
  if(bar)bar.style.setProperty('--sp',h>0?Math.min(1,y/h):0);

  /* Batch layout reads to eliminate layout thrashing during scroll */
  var fUpdates=[], i, f, b, py;
  for(i=0; i<flows.length; i++){
    f=flows[i];
    b=f.s.getBoundingClientRect();
    if(b.bottom>=-160 && b.top<=innerHeight+160){
      py=((b.top+b.height/2-innerHeight/2)*-.08).toFixed(1)+'px';
      fUpdates.push(f.el, py);
    }
  }
  var tlUpdates=[], j, t, tb, p;
  for(j=0; j<tl.length; j++){
    t=tl[j];
    tb=t.getBoundingClientRect();
    p=(innerHeight*.72-tb.top)/Math.max(1,tb.height);
    tlUpdates.push(t, Math.max(.04,Math.min(1,p)).toFixed(3));
  }

  /* Batch style writes */
  for(i=0; i<fUpdates.length; i+=2){
    fUpdates[i].style.setProperty('--py', fUpdates[i+1]);
  }
  for(j=0; j<tlUpdates.length; j+=2){
    tlUpdates[j].style.setProperty('--tl', tlUpdates[j+1]);
  }

  if(header)header.classList.toggle('scrolled',y>8);
}
var flows=$$('.has-flow').map(function(s){var el=$(':scope > .bgflow',s);return el&&!s.classList.contains('cta')?{s:s,el:el}:null}).filter(Boolean);
var tl=reduce?[]:$$('.roles');
var ticking=false;
function throttledScroll(){if(!ticking){ticking=true;requestAnimationFrame(function(){onScroll();ticking=false})}}
addEventListener('scroll',throttledScroll,{passive:true});
addEventListener('resize',throttledScroll);
onScroll();

/* in-page anchors with keyboard focus management (GL-5) */
d.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button!==0||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
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
  var targetY = t.getBoundingClientRect().top + (window.pageYOffset || r.scrollTop) + SCROLL_OFFSET;
  window.scrollTo({ top: targetY, behavior: reduce ? 'auto' : 'smooth' });
  focusTarget();
});

/* deep-link hash scroll and glow (GL-5) */
function checkHash(){
  var h=window.location.hash;
  if(!h||h.length<2)return;
  try{
    var target=$(h);
    if(target){
      var rect=target.getBoundingClientRect();
      if(Math.abs(rect.top - 84) < 16) return;
      setTimeout(function(){
        var targetY = target.getBoundingClientRect().top + (window.pageYOffset || r.scrollTop) + SCROLL_OFFSET;
        window.scrollTo({ top: targetY, behavior: reduce ? 'auto' : 'smooth' });
        target.classList.add('target-glow');
        setTimeout(function(){target.classList.remove('target-glow')},2800);
      },250);
    }
  }catch(err){}
}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',checkHash);else checkHash();
window.addEventListener('hashchange',checkHash);

/* Pause off-screen background animations to save CPU / GPU (GL-1) */
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

/* animated counters with smooth ease-out, scroll cascade, and hover replay */
function animateCounter(b, delay, customDur){
  var end=+b.dataset.count;
  if(isNaN(end))return;
  var suf=b.dataset.suf||'';
  var pre=b.dataset.pre||'';
  var dec=b.dataset.dec?parseInt(b.dataset.dec,10):0;
  if(reduce){
    b.textContent=pre+(dec>0?end.toFixed(dec):end)+suf;
    return;
  }
  var dur=customDur||(end>100?1400:end>15?1100:850);
  delay=delay||0;

  if(b._countRaf){cancelAnimationFrame(b._countRaf);b._countRaf=null;}
  if(b._countTimer){clearTimeout(b._countTimer);b._countTimer=null;}

  // Reset to 0 when starting so user clearly witnesses the counting
  b.textContent=pre+'0'+suf;

  b._countTimer=setTimeout(function(){
    b.classList.add('is-counting');
    var t0=performance.now();

    (function step(now){
      var p=Math.min(1,(now-t0)/dur);
      // Quintic ease-out deceleration
      var ease=1-Math.pow(1-p,4);
      var currentVal;
      if(dec>0){
        currentVal=(end*ease).toFixed(dec);
      }else{
        currentVal=Math.round(end*ease);
      }
      b.textContent=pre+currentVal+suf;

      if(p<1){
        b._countRaf=requestAnimationFrame(step);
      }else{
        b.textContent=pre+(dec>0?end.toFixed(dec):end)+suf;
        b.classList.remove('is-counting');
        b.classList.add('count-settled');
        setTimeout(function(){b.classList.remove('count-settled')},500);
        b._countRaf=null;
      }
    })(t0);
  },delay);
}

function countUp(root){
  var targets=$$('[data-count]',root).concat(root.hasAttribute&&root.hasAttribute('data-count')?[root]:[]);
  targets.forEach(function(b,idx){
    if(b.dataset.done)return;
    b.dataset.done='1';
    animateCounter(b, idx*100);
  });
}

// Hover and touch replay on metric cards
if(fine&&!reduce){
  var lastHoverMap=new WeakMap();
  $$('.proof-card, .proof > div, .hfs-item, .step-card').forEach(function(card){
    card.addEventListener('mouseenter',function(){
      var now=performance.now();
      var last=lastHoverMap.get(card)||0;
      if(now-last<450)return; // throttle repeat triggers
      lastHoverMap.set(card,now);
      $$('[data-count]',card).forEach(function(b){
        animateCounter(b,0,800);
      });
    });
    card.addEventListener('touchstart',function(){
      $$('[data-count]',card).forEach(function(b){
        animateCounter(b,0,800);
      });
    },{passive:true});
  });
}

window.addEventListener('beforeprint',function(){
  $$('[data-count]').forEach(function(b){
    var end=+b.dataset.count,suf=b.dataset.suf||'',pre=b.dataset.pre||'';
    b.dataset.done='1';
    b.textContent=pre+end+suf;
  });
  $$('.role li').forEach(function(b){
    b.classList.remove('is-dimmed','is-highlighted');
  });
});

/* 3D tilt with rAF throttle, untransformed coordinates, no CTA tilt (GL-11) */
if(fine&&!reduce){
  var tiltEls=$$('[data-tilt]:not(.cta)');
  tiltEls.forEach(function(el){
    var max=2.0,rafId=null;
    el.addEventListener('pointermove',function(e){
      if(rafId)return;
      rafId=requestAnimationFrame(function(){
        rafId=null;
        var b=el.getBoundingClientRect();
        var x=(e.clientX-b.left)/Math.max(1,b.width);
        var y=(e.clientY-b.top)/Math.max(1,b.height);
        el.classList.add('tilting');
        el.style.setProperty('--ry',((x-.5)*2*max).toFixed(2)+'deg');
        el.style.setProperty('--rx',((.5-y)*2*max).toFixed(2)+'deg');
        el.style.setProperty('--mx',(x*100).toFixed(1)+'%');
        el.style.setProperty('--my',(y*100).toFixed(1)+'%');
      });
    });
    el.addEventListener('pointerleave',function(){
      if(rafId){cancelAnimationFrame(rafId);rafId=null;}
      el.classList.remove('tilting');
      el.style.setProperty('--rx','0deg');
      el.style.setProperty('--ry','0deg');
    });
  });
}

/* site-wide animation pause toggle (GL-1, GL-3, GL-4) */
var animToggle=$('#animToggle');
var mqToggle=$('#marqToggle'),mqWrap=$('.marq-wrap');
var PAUSE_ICO='<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>';
var PLAY_ICO='<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"/></svg>';

function setMotionPaused(paused){
  r.classList.toggle('is-anim-paused',paused);
  if(animToggle){
    animToggle.setAttribute('aria-pressed',String(paused));
    animToggle.setAttribute('aria-label',paused?'Resume animations':'Pause motion');
    animToggle.setAttribute('title',paused?'Resume animations':'Pause motion');
    animToggle.innerHTML=paused?PLAY_ICO:PAUSE_ICO;
  }
  /* only unpause SVGs that are currently onscreen (GL-1) */
  $$('svg.bgflow').forEach(function(s){
    try{
      if(paused)s.pauseAnimations();
      else if(!reduce&&!s.classList.contains('is-offscreen'))s.unpauseAnimations();
    }catch(_){}
  });
  try{localStorage.setItem('gr-motion',paused?'paused':'running')}catch(_){}
}
if(animToggle)animToggle.addEventListener('click',function(){
  setMotionPaused(!r.classList.contains('is-anim-paused'));
});

/* Marquee pause control (GL-3): scope strictly to marquee track */
if(mqToggle&&mqWrap){
  mqToggle.addEventListener('click',function(){
    var isP=mqWrap.classList.toggle('is-paused');
    mqToggle.setAttribute('aria-pressed',String(isP));
    mqToggle.setAttribute('aria-label','Toggle marquee animation');
    mqToggle.innerHTML=isP?PLAY_ICO:PAUSE_ICO;
  });
}

/* Respond dynamically to OS reduced motion changes (GL-4) */
try{
  var motionMQL=window.matchMedia('(prefers-reduced-motion: reduce)');
  motionMQL.addEventListener('change',function(e){
    reduce=e.matches;
    setMotionPaused(e.matches);
  });
  if(reduce)setMotionPaused(true);
  else{
    try{if(localStorage.getItem('gr-motion')==='paused')setMotionPaused(true)}catch(_){}
  }
}catch(_){}

/* project filter: sliding pill indicator, URL hash sync (PJ-2) & FLIP animation */
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
      try{
        var targetHash = (f === 'all') ? '' : ('#' + f);
        history.replaceState(null, '', location.pathname + targetHash);
      }catch(_){}

      /* FLIP Animation */
      var firstRects=new Map();
      cards.forEach(function(k){firstRects.set(k,k.getBoundingClientRect())});

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

      if(!reduce){
        cards.forEach(function(k){
          if(k.hidden)return;
          var first=firstRects.get(k);
          if(!first||first.width===0||first.height===0){
            k.style.opacity='0';
            requestAnimationFrame(function(){
              k.style.transition='opacity 0.35s ease';
              k.style.opacity='1';
              setTimeout(function(){k.style.transition=''},380);
            });
            return;
          }
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
        count.textContent='Showing '+n+' of '+cards.length+(cards.length===1?' project':' projects');
      }
    });
  });
  var filterFromHash=function(){
    var qf='';
    try{
      var sp=new URLSearchParams(location.search);
      qf=sp.get('filter')||'';
    }catch(_){}
    var h=(qf||(location.hash||'').slice(1)).replace(/[^a-z0-9_-]/gi,'');
    if(!h)return;
    var chip=$('.chip[data-f="'+h+'"]');
    if(chip){
      chip.click();
      var pgrid=$('#pgrid')||$('.filters');
      if(pgrid){
        setTimeout(function(){
          var pgridY = pgrid.getBoundingClientRect().top + (window.pageYOffset || r.scrollTop) + SCROLL_OFFSET;
          window.scrollTo({ top: pgridY, behavior: reduce ? 'auto' : 'smooth' });
        },100);
      }
    }
  };
  filterFromHash();
  addEventListener('hashchange',filterFromHash);
  addEventListener('popstate',filterFromHash);
}

/* contact form: validate required, email & optional URL, draft flow (CT-1 to CT-5) */
var f=$('#enquiry');
if(f){
  f.setAttribute('novalidate','');
  var isValidUrl=function(str){
    if(!str)return true;
    try{
      var u=new URL(str);
      return u.protocol==='http:'||u.protocol==='https:';
    }catch(_){return false;}
  };

  /* clear errors and manage float label state */
  $$('input, textarea, select',f).forEach(function(i){
    var updateValState=function(){
      i.setAttribute('aria-invalid','false');
      var errSpan=$('#err-'+i.name,f)||(i.parentNode&&i.parentNode.querySelector('.err'));
      if(errSpan)errSpan.textContent='';
      if(i.tagName==='SELECT')i.classList.toggle('has-val',!!i.value);
    };
    i.addEventListener('input',updateValState);
    i.addEventListener('change',updateValState);
    i.addEventListener('animationstart',updateValState);
    if(i.tagName==='SELECT'&&i.value)i.classList.add('has-val');
  });

  /* prefill service from query parameter (SV-2) */
  try{
    var q=new URLSearchParams(location.search).get('service');
    var sField=$('#enquiry-service')||f.elements['service'];
    if(q&&sField){
      var cleanQ=q.trim().toLowerCase();
      var matched=false;
      [].some.call(sField.options,function(o){
        if(o.text.trim().toLowerCase()===cleanQ||o.value.trim().toLowerCase()===cleanQ){
          sField.value=o.value||o.text;
          sField.classList.add('has-val');
          matched=true;
          return true;
        }
      });
      if(!matched&&sField.options.length){
        sField.value='Custom BA scope & advisory';
        sField.classList.add('has-val');
      }
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
    var recipient=f.dataset.email||'gautamreddy098@gmail.com';
    var body=['Name: '+v('name'),'Email: '+v('email'),'Company: '+(v('company')||'-'),'Service: '+v('service'),'Engagement: '+v('type'),'Timeline: '+v('timeline'),'Reference: '+(v('ref')||'-'),'','What I need:',v('msg')].join('\n');
    
    /* Populate fallback panel (CT-5) */
    var fbText=$('#fallbackTextarea');
    var fbCard=$('#fallbackCard');
    var openGmailBtn=$('#openGmailBtn');
    if(fbText)fbText.value=body;
    if(openGmailBtn){
      openGmailBtn.href='https://mail.google.com/mail/?view=cm&fs=1&to='+encodeURIComponent(recipient)+'&su='+encodeURIComponent('Project enquiry: '+v('service'))+'&body='+encodeURIComponent(body);
    }
    if(fbCard){
      fbCard.hidden=false;
      try{ fbCard.scrollIntoView({behavior:'smooth',block:'nearest'}); }catch(_){}
    }

    /* Truthful draft flow & clipboard copy (CT-2) */
    var s=$('#sent');
    if(navigator.clipboard&&window.isSecureContext){
      navigator.clipboard.writeText(body).then(function(){
        if(s){
          s.innerHTML='I have opened your email client and copied the message text to your clipboard. If your email application does not launch automatically, you can paste the message into a direct email to <a href="mailto:'+recipient+'">'+recipient+'</a>.';
          s.hidden=false;
          s.focus();
        }
      }).catch(function(){
        if(s){
          s.innerHTML='Opening your email client draft. If your email application does not launch, copy the text from the backup box below and email <a href="mailto:'+recipient+'">'+recipient+'</a>.';
          s.hidden=false;
          s.focus();
        }
      });
    }else{
      if(s){
        s.innerHTML='Opening your email client draft. You can also copy the prepared text below and send it directly to <a href="mailto:'+recipient+'">'+recipient+'</a>.';
        s.hidden=false;
        s.focus();
      }
    }

    location.href='mailto:'+recipient+'?subject='+encodeURIComponent('Project enquiry: '+v('service'))+'&body='+encodeURIComponent(body);
  });

  /* copy message helper for enquiries with reliable fallback (CT-1) */
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

/* Fallback copy helper (CT-5) */
var copyFallbackBtn=$('#copyFallbackBtn'),fallbackTextarea=$('#fallbackTextarea');
if(copyFallbackBtn&&fallbackTextarea){
  copyFallbackBtn.addEventListener('click',function(){
    var val=fallbackTextarea.value;
    if(!val)return;
    var orig=copyFallbackBtn.innerHTML;
    function done(){
      copyFallbackBtn.innerHTML='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="display:inline-block;vertical-align:middle;margin-right:4px"><polyline points="20 6 9 17 4 12"/></svg> Copied!';
      setTimeout(function(){copyFallbackBtn.innerHTML=orig},1800);
    }
    if(navigator.clipboard&&window.isSecureContext){
      navigator.clipboard.writeText(val).then(done).catch(function(){
        fallbackTextarea.select();
        done();
      });
    }else{
      fallbackTextarea.select();
      try{d.execCommand('copy');done()}catch(_){}
    }
  });
}

/* Generic clipboard copy helper (CT-1: exclude bespoke buttons) */
$$('[data-copy], .copy-btn').forEach(function(b){
  if(b.id==='copyEnquiryBtn'||b.id==='copyFallbackBtn')return;
  b.addEventListener('click',function(){
    var t=b.dataset.copy||b.getAttribute('data-value');
    if(!t){
      var targetId=b.dataset.target;
      if(targetId){
        var targetEl=$(targetId);
        if(targetEl)t=targetEl.value||targetEl.textContent;
      }
    }
    if(!t)return;
    var origHtml=b.innerHTML;
    var liveRegion=$('#copyStatusLive');
    function done(){
      b.classList.add('is-copied');
      b.innerHTML='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="display:inline-block;vertical-align:middle;margin-right:4px"><polyline points="20 6 9 17 4 12"/></svg> Copied!';
      if(liveRegion)liveRegion.textContent='Copied to clipboard';
      setTimeout(function(){
        b.classList.remove('is-copied');
        b.innerHTML=origHtml;
        if(liveRegion)liveRegion.textContent='';
      },1500);
    }
    function fallback(){
      try{
        var ta=d.createElement('textarea');
        ta.value=t;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;opacity:0';
        d.body.appendChild(ta);ta.select();
        var ok=d.execCommand('copy');d.body.removeChild(ta);
        if(ok)done();
      }catch(_){}
    }
    if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(done).catch(fallback);
    else fallback();
  });
});
d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});

/* signature BA traceability table: hover, tap, keyboard Enter/Space (HM-11) */
var traceRows=$$('[data-links]');
if(traceRows.length){
  var traceIds=$$('[data-id]');
  var setTrace=function(on,row){
    var set={};
    (row.dataset.links||'').split(/\s+/).forEach(function(k){if(k)set[k]=true});
    traceIds.forEach(function(el){el.classList.toggle('is-linked',on&&!!set[el.dataset.id])});
    row.classList.toggle('is-source',on);
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
    row.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){
        if(e.target.closest('a'))return;
        e.preventDefault();
        var on=!row.classList.contains('is-source');
        clearAll(row);
        setTrace(on,row);
      }
    });
  });
}

/* hero multi-deliverable slider with pause control & swipe (HM-1, HM-2, HM-10) */
var slider=$('#heroSlider');
if(slider){
  var tabs=$$('.slider-tab',slider),
      slides=$$('.slider-slide',slider),
      dots=$$('.s-dot',slider),
      prevBtn=$('#slidePrev',slider),
      nextBtn=$('#slideNext',slider),
      pauseBtn=$('#slidePauseBtn',slider),
      countEl=$('#slideCount',slider),
      tablist=$('.slider-tabs',slider),
      currIdx=0,
      totalSlides=slides.length,
      sliderOffscreen=false,
      sliderUserPaused=false;

  var showSlide=function(idx,explicitDir){
    if(idx<0)idx=totalSlides-1;
    if(idx>=totalSlides)idx=0;
    var dir=explicitDir;
    if(!dir){
      if(currIdx===totalSlides-1&&idx===0)dir='next';
      else if(currIdx===0&&idx===totalSlides-1)dir='prev';
      else dir=idx>currIdx?'next':(idx<currIdx?'prev':'');
    }
    currIdx=idx;
    tabs.forEach(function(t,i){
      var active=i===currIdx;
      t.classList.toggle('is-active',active);
      t.setAttribute('aria-selected',active?'true':'false');
      t.setAttribute('tabindex',active?'0':'-1');
    });
    dots.forEach(function(d,i){
      var active=i===currIdx;
      d.classList.toggle('is-active',active);
      d.setAttribute('aria-pressed',String(active));
    });
    slides.forEach(function(s,i){
      var active=i===currIdx;
      s.classList.remove('slide-from-right','slide-from-left','is-active');
      if(active){
        s.hidden=false;
        void s.offsetWidth; /* force reflow before adding animation class */
        s.classList.add('is-active');
        if(dir==='next')s.classList.add('slide-from-right');
        else if(dir==='prev')s.classList.add('slide-from-left');
        /* Clean up animation class once finished to allow re-triggering */
        s.addEventListener('animationend', function() {
          s.classList.remove('slide-from-right','slide-from-left');
        }, { once: true });
      }else{
        s.hidden=true;
      }
    });
    if(countEl)countEl.textContent=(currIdx+1)+' / '+totalSlides;
  };

  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){showSlide(i)});
  });
  dots.forEach(function(d,i){
    d.addEventListener('click',function(){showSlide(i)});
  });
  if(prevBtn)prevBtn.addEventListener('click',function(){showSlide(currIdx-1,'prev')});
  if(nextBtn)nextBtn.addEventListener('click',function(){showSlide(currIdx+1,'next')});

  /* WAI-ARIA tablist keyboard navigation */
  if(tablist){
    tablist.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'||e.key==='ArrowDown'){
        e.preventDefault();
        var next=(currIdx+1)%totalSlides;
        showSlide(next,'next');
        tabs[next].focus();
      }else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){
        e.preventDefault();
        var prev=(currIdx-1+totalSlides)%totalSlides;
        showSlide(prev,'prev');
        tabs[prev].focus();
      }else if(e.key==='Home'){
        e.preventDefault();
        showSlide(0,'prev');
        tabs[0].focus();
      }else if(e.key==='End'){
        e.preventDefault();
        showSlide(totalSlides-1,'next');
        tabs[totalSlides-1].focus();
      }
    });
  }

  /* Observer to pause slider when offscreen (HM-1) */
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(entries){
      entries.forEach(function(en){sliderOffscreen=!en.isIntersecting});
    }).observe(slider);
  }

  /* Auto-slide rotation with pause controls (HM-1) */
  var slideTimer=null;
  var startSlideTimer=function(){
    if(!reduce&&!sliderUserPaused){
      stopSlideTimer();
      slideTimer=setInterval(function(){
        if(d.hidden||r.classList.contains('is-anim-paused')||sliderOffscreen||sliderUserPaused)return;
        showSlide(currIdx+1,'next');
      },6500);
    }
  };
  var stopSlideTimer=function(){
    if(slideTimer){clearInterval(slideTimer);slideTimer=null;}
  };

  if(pauseBtn){
    pauseBtn.addEventListener('click',function(){
      sliderUserPaused=!sliderUserPaused;
      pauseBtn.setAttribute('aria-pressed',String(sliderUserPaused));
      pauseBtn.setAttribute('aria-label',sliderUserPaused?'Play slide rotation':'Pause slide rotation');
      pauseBtn.innerHTML=sliderUserPaused?PLAY_ICO:PAUSE_ICO;
      if(sliderUserPaused)stopSlideTimer();else startSlideTimer();
    });
  }
  slider.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')stopSlideTimer()});
  slider.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'&&!sliderUserPaused)startSlideTimer()});
  slider.addEventListener('focusin',stopSlideTimer);
  slider.addEventListener('focusout',function(){if(!sliderUserPaused)startSlideTimer()});
  startSlideTimer();
}

/* About BA Console: Interactive Tab Navigation (AB-2) */
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

/* Selected Work: PayTrack Wireframe Row Cycling with IntersectionObserver & Pause/Loop Controls (HM-16, WCAG 2.2.2) */
var wfRows=$$('.wf-row-cycle'),wfTable=$('#wireframeTable'),wfPauseBtn=$('#wfPauseBtn');
if(wfRows.length&&!reduce){
  var wfIdx=0,wfPaused=false,wfOffscreen=false,wfCycles=0,MAX_CYCLES=wfRows.length*3;
  if('IntersectionObserver' in window&&wfTable){
    new IntersectionObserver(function(entries){
      entries.forEach(function(en){wfOffscreen=!en.isIntersecting});
    }).observe(wfTable);
  }
  if(wfTable){
    wfTable.addEventListener('pointerenter',function(){wfPaused=true});
    wfTable.addEventListener('pointerleave',function(){if(!wfPauseBtn||wfPauseBtn.getAttribute('aria-pressed')!=='true')wfPaused=false});
    wfTable.addEventListener('focusin',function(){wfPaused=true});
    wfTable.addEventListener('focusout',function(){if(!wfPauseBtn||wfPauseBtn.getAttribute('aria-pressed')!=='true')wfPaused=false});
  }
  if(wfPauseBtn){
    wfPauseBtn.addEventListener('click',function(){
      wfPaused=!wfPaused;
      wfPauseBtn.setAttribute('aria-pressed',String(wfPaused));
      wfPauseBtn.textContent=wfPaused?'Resume cycle':'Pause cycle';
    });
  }
  var wfTimer=setInterval(function(){
    if(d.hidden||r.classList.contains('is-anim-paused')||wfPaused||wfOffscreen)return;
    /* Clear all rows, then activate only the current index */
    wfRows.forEach(function(rw,i){
      rw.classList.toggle('is-active-row',i===wfIdx);
    });
    wfIdx=(wfIdx+1)%wfRows.length;
    wfCycles++;
    if(wfCycles>=MAX_CYCLES){
      clearInterval(wfTimer);
      /* Ensure clean state at end */
      wfRows.forEach(function(rw){rw.classList.remove('is-active-row')});
      if(wfPauseBtn){
        wfPauseBtn.textContent='Restart cycle';
        wfPauseBtn.setAttribute('aria-pressed','true');
        wfPauseBtn.onclick=function(){
          wfCycles=0;
          wfIdx=0;
          wfPaused=false;
          wfPauseBtn.textContent='Pause cycle';
          wfPauseBtn.setAttribute('aria-pressed','false');
        };
      }
    }
  },2400);
}

/* Experience: Collapsible Role Metrics Tray (HM-8) */
$$('.role-expander').forEach(function(btn){
  btn.addEventListener('click',function(){
    var metrics=btn.nextElementSibling;
    if(!metrics)return;
    var isHidden=metrics.hidden;
    metrics.hidden=!isHidden;
    btn.setAttribute('aria-expanded',String(isHidden));
  });
});

/* Print Resume Button (RS-1) */
var printBtn=$('#printResumeBtn');
if(printBtn){
  printBtn.addEventListener('click',function(){
    window.print();
  });
}

/* Document Preview Drawer Modal with focus trap, scroll lock & inert background (GL-5, GL-6) */
var pdDrawer=$('#previewDrawer'),pdBackdrop=$('#pdBackdrop'),pdClose=$('#pdClose'),pdPanel=$('.pd-panel');
var lastActiveElement=null;
var mainEl=$('#main'),hdrEl=$('.site-header'),ftrEl=$('.site-footer');
function openDrawer(tabName){
  if(!pdDrawer)return;
  if(typeof closeSpotlight==="function")closeSpotlight();
  lastActiveElement=d.activeElement;
  pdDrawer.hidden=false;
  d.body.style.overflow='hidden';
  if(mainEl)mainEl.inert=true;
  if(hdrEl)hdrEl.inert=true;
  if(ftrEl)ftrEl.inert=true;
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
  if(mainEl)mainEl.inert=false;
  if(hdrEl)hdrEl.inert=false;
  if(ftrEl)ftrEl.inert=false;
  if(lastActiveElement&&lastActiveElement.focus)lastActiveElement.focus();
}
if(pdBackdrop)pdBackdrop.addEventListener('click',closeDrawer);
if(pdClose)pdClose.addEventListener('click',closeDrawer);
d.addEventListener('keydown',function(e){
  if(!pdDrawer||pdDrawer.hidden)return;
  if(e.key==='Escape'){closeDrawer();return;}
  if(e.key==='Tab'&&pdPanel){
    var focusables=$$('a,button,[tabindex]:not([tabindex="-1"])',pdPanel).filter(function(x){
      return !x.closest('[hidden]')&&(x.offsetWidth>0||x.offsetHeight>0||x.getClientRects().length>0);
    });
    if(!focusables.length)return;
    var first=focusables[0],last=focusables[focusables.length-1];
    if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus();}
  }
});
$$('[data-preview]').forEach(function(btn){
  btn.addEventListener('click',function(){openDrawer(btn.dataset.preview)});
});
var pdTabs=$$('.pd-tab'),pdPanes=$$('.pd-pane'),pdTablist=$('.pd-tabs');
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
if(pdTablist){
  pdTablist.addEventListener('keydown',function(e){
    var tabsArr=Array.prototype.slice.call(pdTabs);
    var actIdx=tabsArr.indexOf(d.activeElement);
    if(actIdx<0)return;
    var nextTab=-1;
    if(e.key==='ArrowRight'||e.key==='ArrowDown')nextTab=(actIdx+1)%tabsArr.length;
    else if(e.key==='ArrowLeft'||e.key==='ArrowUp')nextTab=(actIdx-1+tabsArr.length)%tabsArr.length;
    else if(e.key==='Home')nextTab=0;
    else if(e.key==='End')nextTab=tabsArr.length-1;
    if(nextTab>=0){
      e.preventDefault();
      tabsArr[nextTab].focus();
      tabsArr[nextTab].click();
    }
  });
}

/* Resume skills match filter by data-skills attribute with live announcement (RS-5) */
var skillChips=$$('.skill-filter-chip');
if(skillChips.length){
  var roleBullets=$$('.role li');
  var sfLive=$('#skillFilterLive');
  skillChips.forEach(function(chip){
    chip.addEventListener('click',function(){
      var s=chip.dataset.skill||'all';
      skillChips.forEach(function(c){
        var on=c===chip;
        c.classList.toggle('is-active',on);
        c.setAttribute('aria-pressed',String(on));
      });
      var sfCount=$('#sfCount');
      if(s==='all'){
        roleBullets.forEach(function(b){b.classList.remove('is-dimmed','is-highlighted')});
        if(sfLive)sfLive.textContent='Showing all experience bullets';
        if(sfCount)sfCount.textContent='Showing '+roleBullets.length+' of '+roleBullets.length+' bullets';
        return;
      }
      var count=0;
      roleBullets.forEach(function(b){
        var skills=(b.dataset.skills||'').toLowerCase().split(/\s+/);
        var match=skills.indexOf(s)!==-1;
        if(match)count++;
        b.classList.toggle('is-highlighted',match);
        b.classList.toggle('is-dimmed',!match);
      });
      if(sfLive)sfLive.textContent=count+' bullets highlighted for '+chip.textContent.trim();
      if(sfCount)sfCount.textContent='Showing '+count+' of '+roleBullets.length+' bullets';
    });
  });
}

/* Universal Image Lightbox with focus trap & clean removal (GL-2) */
var ilb=$('#imageLightbox'),ilbImg=$('#ilbImg'),ilbTitle=$('#ilbTitle'),ilbCaption=$('#ilbCaption'),ilbClose=$('#ilbClose'),ilbBackdrop=$('#ilbBackdrop');
var lastActiveImgEl=null;

function openImgLightbox(src,title,caption){
  if(!ilb||!src)return;
  lastActiveImgEl=d.activeElement;
  if(ilbImg){
    ilbImg.src=src;
    ilbImg.alt=title||'Project image preview';
  }
  if(ilbTitle)ilbTitle.textContent=title||'Image preview';
  if(ilbCaption){
    ilbCaption.textContent=caption||'';
    ilbCaption.hidden=!caption;
  }
  ilb.hidden=false;
  d.body.style.overflow='hidden';
  if(mainEl)mainEl.inert=true;
  if(hdrEl)hdrEl.inert=true;
  if(ftrEl)ftrEl.inert=true;
  if(typeof lenis!=='undefined'&&lenis)lenis.stop();
  if(ilbClose)ilbClose.focus();
}

function closeImgLightbox(){
  if(ilb&&!ilb.hidden){
    ilb.hidden=true;
    if(ilbImg)ilbImg.removeAttribute('src');
    d.body.style.overflow='';
    if(mainEl)mainEl.inert=false;
    if(hdrEl)hdrEl.inert=false;
    if(ftrEl)ftrEl.inert=false;
    if(typeof lenis!=='undefined'&&lenis)lenis.start();
    if(lastActiveImgEl&&lastActiveImgEl.focus)lastActiveImgEl.focus();
  }
}

if(ilbClose)ilbClose.addEventListener('click',closeImgLightbox);
if(ilbBackdrop)ilbBackdrop.addEventListener('click',closeImgLightbox);

d.addEventListener('keydown',function(e){
  if(!ilb||ilb.hidden)return;
  if(e.key==='Escape'){closeImgLightbox();return;}
  if(e.key==='Tab'){
    var focusables=$$('a,button,[tabindex]:not([tabindex="-1"])',ilb).filter(function(x){
      return !x.closest('[hidden]')&&(x.offsetWidth>0||x.offsetHeight>0);
    });
    if(!focusables.length)return;
    var first=focusables[0],last=focusables[focusables.length-1];
    if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus()}
  }
});

/* Bind image triggers across projects and samples */
$$('.zoomable-img, .img-zoom-btn, [data-full]').forEach(function(el){
  el.addEventListener('click',function(e){
    e.preventDefault();
    var full=el.dataset.full||(el.tagName==='IMG'?el.src:el.getAttribute('href'));
    var title=el.dataset.title||el.getAttribute('aria-label')||(el.tagName==='IMG'?el.alt:'Image Preview');
    var cap=el.dataset.caption||'';
    openImgLightbox(full,title,cap);
  });
});

/* Samples Stepper / Phase Filter with section visibility and live announcements (SM-1, SM-4) */
var ptSteps=$$('.pt-step'),sItems=$$('.file-item'),fileSections=$$('.file-sec'),samplesLive=$('#samplesLive');
if(ptSteps.length&&sItems.length){
  ptSteps.forEach(function(btn){
    btn.addEventListener('click',function(){
      var phase=btn.dataset.phase||'all';
      ptSteps.forEach(function(b){
        var on=b===btn;
        b.classList.toggle('is-active',on);
        b.setAttribute('aria-pressed',String(on));
      });
      var matchCount=0;
      sItems.forEach(function(item){
        var itemPhase=item.dataset.phase||'all';
        var match=(phase==='all'||itemPhase===phase||itemPhase==='all');
        item.hidden=!match;
        if(match)matchCount++;
      });
      /* Hide section headers if section has no visible items (SM-4) */
      fileSections.forEach(function(sec){
        var visibleChildren=$$('.file-item:not([hidden])',sec);
        sec.hidden=(visibleChildren.length===0);
      });
      if(samplesLive){
        samplesLive.textContent='Showing '+matchCount+' deliverables for '+(btn.textContent.trim());
      }
    });
  });
}

var viewList=$('#viewList'),viewGrid=$('#viewGrid'),fileLists=$$('.file-list');
if(viewList&&viewGrid&&fileLists.length){
  var setSamplesView=function(mode){
    var isGrid=mode==='grid';
    viewGrid.classList.toggle('is-active',isGrid);
    viewGrid.setAttribute('aria-pressed',String(isGrid));
    viewList.classList.toggle('is-active',!isGrid);
    viewList.setAttribute('aria-pressed',String(!isGrid));
    fileLists.forEach(function(l){l.classList.toggle('file-list-grid',isGrid)});
    try{localStorage.setItem('gr-samples-view',mode)}catch(_){}
  };
  try{
    var savedView=localStorage.getItem('gr-samples-view');
    if(savedView==='grid'||savedView==='list')setSamplesView(savedView);
  }catch(_){}
  viewList.addEventListener('click',function(){setSamplesView('list')});
  viewGrid.addEventListener('click',function(){setSamplesView('grid')});
}

/* Magic Card pointer spotlight tracker (GL-11) */
var magicCards=$$('.magic-card');
if(magicCards.length&&fine&&!reduce){
  magicCards.forEach(function(card){
    var raf=null;
    card.addEventListener('pointermove',function(e){
      if(raf)return;
      raf=requestAnimationFrame(function(){
        raf=null;
        var b=card.getBoundingClientRect();
        card.style.setProperty('--mx',(e.clientX-b.left)+'px');
        card.style.setProperty('--my',(e.clientY-b.top)+'px');
      });
    });
  });
}

/* Toolkit tiles mobile tap / click evidence expansion & accessible controls (HM-6, HM-7) */
$$('.tk-tile').forEach(function(tile){
  var toggleBtn=tile.querySelector('.tk-toggle')||tile;
  function toggle(){
    var isOpen=tile.classList.toggle('is-open');
    if(toggleBtn)toggleBtn.setAttribute('aria-expanded',String(isOpen));
  }
  tile.addEventListener('click',function(e){
    if(e.target.closest&&e.target.closest('a'))return;
    toggle();
  });
  tile.addEventListener('keydown',function(e){
    if(e.target.closest&&e.target.closest('a'))return;
    if(e.key==='Enter'||e.key===' '){
      if(e.target!==tile&&e.target!==toggleBtn)return;
      e.preventDefault();
      toggle();
    }
  });
});

/* Lens magnifier on screenshots for pointer devices (GL-11, PJ-4) */
if(fine&&!reduce){
  $$('.has-lens, .feat-img').forEach(function(wrap){
    var img=wrap.querySelector('img');
    if(!img)return;
    var glass=wrap.querySelector('.lens-glass');
    if(!glass){
      glass=d.createElement('div');
      glass.className='lens-glass';
      wrap.style.position='relative';
      wrap.appendChild(glass);
    }
    var fullSrc=wrap.dataset.full||img.src;
    glass.style.backgroundImage='url('+fullSrc+')';
    glass.style.backgroundRepeat='no-repeat';
    
    var glassW=120,glassH=120,lensRaf=null;
    wrap.addEventListener('pointermove',function(e){
      if(lensRaf)return;
      lensRaf=requestAnimationFrame(function(){
        lensRaf=null;
        var rRect=wrap.getBoundingClientRect();
        var x=e.clientX-rRect.left,y=e.clientY-rRect.top;
        glass.style.left=x+'px';
        glass.style.top=y+'px';
        var z=2.0;
        var bgW=rRect.width*z,bgH=rRect.height*z;
        glass.style.backgroundSize=bgW+'px '+bgH+'px';
        glass.style.backgroundPosition=(-(x*z-glassW/2))+'px '+(-(y*z-glassH/2))+'px';
      });
    });
  });
}

/* One-time hero traceability row sweep demonstration */
var firstTraceRow=$('.trace tbody tr');
if(firstTraceRow&&!reduce){
  setTimeout(function(){
    firstTraceRow.classList.add('trace-sweep');
    setTimeout(function(){
      firstTraceRow.classList.remove('trace-sweep');
    },1800);
  },800);
}

/* Resume clear filter helper */
var sfClear=$('#sfClear');
if(sfClear){
  sfClear.addEventListener('click',function(){
    var allBtn=$('.skill-filter-chip[data-skill="all"]');
    if(allBtn)allBtn.click();
    sfClear.hidden=true;
  });
  $$('.skill-filter-chip').forEach(function(chip){
    chip.addEventListener('click',function(){
      if(sfClear)sfClear.hidden=(chip.dataset.skill==='all');
    });
  });
}

/* Services Peek Card touch expand toggle (SV-touch) */
$$('.peek-card').forEach(function(card){
  card.addEventListener('click', function(e){
    if(e.target.closest('a')) return;
    var expanded = card.classList.toggle('is-expanded');
    card.setAttribute('aria-expanded', String(expanded));
  });
});


})();
