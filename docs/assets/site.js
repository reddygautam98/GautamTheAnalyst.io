/* Gautam Reddy portfolio v23: theme, mobile menu, project filter, contact form,
   smooth scroll (Lenis), scroll reveals, counters, subtle 3D tilt, hero scene, flow parallax, role rotator. */
(function(){
var d=document,r=d.documentElement,$=function(s,c){return(c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;

/* theme toggle with SVG icons */
var tb=$('#theme');
var SUN_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
var MOON_ICO='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

function paint(t){
  r.dataset.theme=t;
  if(tb){
    tb.setAttribute('aria-pressed',String(t==='dark'));
    tb.setAttribute('aria-label','Switch to '+(t==='dark'?'light':'dark')+' theme');
    tb.innerHTML=t==='dark'?SUN_ICO:MOON_ICO;
  }
}
paint(r.dataset.theme||'light');
if(tb)tb.addEventListener('click',function(){
  var t=r.dataset.theme==='dark'?'light':'dark';
  paint(t);
  try{localStorage.setItem('gr-theme',t)}catch(e){}
});

/* mobile menu with backdrop & scroll-lock */
var mb=$('#menu'),nav=$('#nav');
function closeMenu(){
  if(nav&&nav.classList.contains('open')){
    nav.classList.remove('open');
    d.body.classList.remove('menu-open');
    if(mb)mb.setAttribute('aria-expanded','false');
    if(lenis)lenis.start();
  }
}
if(mb&&nav){
  mb.addEventListener('click',function(){
    var o=nav.classList.toggle('open');
    d.body.classList.toggle('menu-open',o);
    mb.setAttribute('aria-expanded',String(o));
    if(lenis){if(o)lenis.stop();else lenis.start();}
  });
  d.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&nav.classList.contains('open')){
      closeMenu();
      mb.focus();
    }
  });
  nav.addEventListener('click',function(e){
    if(e.target.tagName==='A')closeMenu();
  });
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

/* in-page anchors */
d.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href^="#"]');
  if(!a||a.getAttribute('href').length<2)return;
  var t=$(a.getAttribute('href'));
  if(!t)return;
  e.preventDefault();
  if(lenis)lenis.scrollTo(t,{offset:-84});
  else t.scrollIntoView({behavior:reduce?'auto':'smooth'});
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

/* scroll reveal */
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
  rvs.forEach(function(el){el.classList.add('in')});
}

/* Pause off-screen background animations to save CPU / GPU */
if('IntersectionObserver' in window&&!reduce){
  var animObserver=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      entry.target.style.animationPlayState = entry.isIntersecting ? 'running' : 'paused';
    });
  },{rootMargin:'100px'});
  $$('.bgflow, .stage, .f3d, .marq-track').forEach(function(el){
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

  /* hero scene follows pointer within gentle ±6deg range */
  var sc=$('[data-scene]');
  if(sc){
    var st=$('.stage',sc);
    sc.addEventListener('pointermove',function(e){
      var b=sc.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;
      st.classList.add('live');
      st.style.setProperty('--ry',(-6+x*12).toFixed(2)+'deg');
      st.style.setProperty('--rx',(3-y*10).toFixed(2)+'deg');
    });
    sc.addEventListener('pointerleave',function(){
      st.classList.remove('live');
      st.style.setProperty('--ry','-6deg');
      st.style.setProperty('--rx','3deg');
    });
  }
}

/* hero keyword rotator */
var rot=$('[data-rot]');
if(rot&&!reduce){
  var ws=$$('span',rot),i=0;
  rot.setAttribute('data-live','1');
  ws[0].classList.add('on');
  setInterval(function(){
    ws[i].classList.remove('on');
    i=(i+1)%ws.length;
    ws[i].classList.add('on');
  },2800);
}

/* marquee pause toggle button */
var mqToggle=$('#marqToggle'),mqWrap=$('.marq-wrap');
if(mqToggle&&mqWrap){
  mqToggle.addEventListener('click',function(){
    var paused=mqWrap.classList.toggle('is-paused');
    mqToggle.setAttribute('aria-pressed',String(paused));
    mqToggle.innerHTML=paused?'&#9654; Play':'&#9646;&#9646; Pause';
  });
}

/* pause decorative SMIL motion when asked to reduce motion */
if(reduce)$$('svg.bgflow').forEach(function(s){try{s.pauseAnimations()}catch(e){}});

/* project filter: choosing an option filters matching cards without disruptive blurring */
var chips=$$('.chip[data-f]');
if(chips.length){
  var cards=$$('[data-cat]'),count=$('#count');
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      var f=c.dataset.f,n=0;
      chips.forEach(function(x){x.setAttribute('aria-pressed',String(x===c))});
      cards.forEach(function(k){
        var match=f==='all'||k.dataset.cat===f;
        if(match)n++;
        k.hidden=!match;
        if(match){k.classList.remove('out')}else{k.classList.add('out')}
      });
      if(count){
        count.setAttribute('aria-live','polite');
        count.textContent=n+(n===1?' project':' projects');
      }
      if(lenis)setTimeout(function(){lenis.resize()},200);
    });
  });
}

/* contact form: validate, then open email draft with fallback focus */
var f=$('#enquiry');
if(f){
  f.setAttribute('novalidate','');
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=true,em=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    $$('[required]',f).forEach(function(i){
      var m=i.parentNode.querySelector('.err'),bad=!i.value.trim()||(i.type==='email'&&!em.test(i.value));
      if(m)m.textContent=bad?(i.type==='email'?'Enter a valid email address.':'This field is required.'):'';
      i.setAttribute('aria-invalid',String(bad));
      if(bad&&ok){i.focus();ok=false}
    });
    if(!ok)return;
    var v=function(n){return(f.elements[n]&&f.elements[n].value||'').trim()};
    var body=['Name: '+v('name'),'Email: '+v('email'),'Company: '+(v('company')||'-'),'Service: '+v('service'),'Engagement: '+v('type'),'Timeline: '+v('timeline'),'Reference: '+(v('ref')||'-'),'','What I need:',v('msg')].join('\n');
    location.href='mailto:gautamreddy098@gmail.com?subject='+encodeURIComponent('Project enquiry: '+v('service'))+'&body='+encodeURIComponent(body);
    var s=$('#sent');
    if(s){
      s.hidden=false;
      s.setAttribute('tabindex','-1');
      s.setAttribute('role','status');
      s.focus();
    }
  });
}

/* clipboard copy helper */
$$('[data-copy]').forEach(function(b){
  b.addEventListener('click',function(){
    var t=b.dataset.copy;
    if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){
      var o=b.textContent;
      b.textContent='Copied';
      setTimeout(function(){b.textContent=o},1500);
    });
  });
});
d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});

/* signature BA traceability hover & focus */
var traceIds = $$('[data-id]');
if(traceIds.length){
  function setTrace(on, row){
    var raw = row.dataset.links || '';
    var set = {};
    raw.split(/\s+/).forEach(function(k){ if(k) set[k] = true; });
    traceIds.forEach(function(el){
      var match = !!set[el.dataset.id];
      if(on && match) el.classList.add('is-linked');
      else el.classList.remove('is-linked');
    });
    if(on) row.classList.add('is-source');
    else row.classList.remove('is-source');
  }
  $$('[data-links]').forEach(function(row){
    row.addEventListener('pointerenter', function(){ setTrace(true, row); });
    row.addEventListener('pointerleave', function(){ setTrace(false, row); });
    row.addEventListener('focusin', function(){ setTrace(true, row); });
    row.addEventListener('focusout', function(){ setTrace(false, row); });
  });
}
})();
