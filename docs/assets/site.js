/* Gautam Reddy portfolio v17: theme, menu, project filter, contact form,
   smooth scroll (Lenis), scroll reveals, counters, 3D tilt, hero scene, flow parallax, role rotator. */
(function(){
var d=document,r=d.documentElement,$=function(s,c){return(c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;

/* theme */
var tb=$('#theme');
function paint(t){r.dataset.theme=t;if(tb){tb.setAttribute('aria-pressed',String(t==='dark'));tb.setAttribute('aria-label','Switch to '+(t==='dark'?'light':'dark')+' theme');tb.textContent=t==='dark'?'☀':'☾'}}
paint(r.dataset.theme||'light');
if(tb)tb.addEventListener('click',function(){var t=r.dataset.theme==='dark'?'light':'dark';paint(t);try{localStorage.setItem('gr-theme',t)}catch(e){}});

/* mobile menu */
var mb=$('#menu'),nav=$('#nav');
if(mb&&nav){mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',String(o))});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.focus()}});}

/* smooth scroll */
var lenis=null,header=$('.site-header'),bar=$('.progress');
if(!reduce&&window.Lenis){
  try{lenis=new Lenis({lerp:.085,wheelMultiplier:.95,smoothWheel:true})}catch(e){lenis=null}
}
function onScroll(){
  var y=window.scrollY||r.scrollTop,h=r.scrollHeight-innerHeight;
  if(bar)bar.style.setProperty('--sp',h>0?Math.min(1,y/h):0);
  if(header)header.classList.toggle('scrolled',y>8);
  flows.forEach(function(f){var b=f.s.getBoundingClientRect();if(b.bottom<-200||b.top>innerHeight+200)return;f.el.style.setProperty('--py',((b.top+b.height/2-innerHeight/2)*-.08).toFixed(1)+'px')});
  tl.forEach(function(t){var b=t.getBoundingClientRect(),p=(innerHeight*.72-b.top)/Math.max(1,b.height);t.style.setProperty('--tl',Math.max(.04,Math.min(1,p)).toFixed(3))});
}
var flows=$$('.has-flow').map(function(s){var el=$(':scope > .bgflow',s);return el&&!s.classList.contains('cta')?{s:s,el:el}:null}).filter(Boolean);
var tl=reduce?[]:$$('.roles');
if(lenis){lenis.on('scroll',onScroll);(function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(0)}
else addEventListener('scroll',onScroll,{passive:true});
addEventListener('resize',onScroll);
onScroll();
/* in-page anchors */
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||a.getAttribute('href').length<2)return;var t=$(a.getAttribute('href'));if(!t)return;e.preventDefault();if(lenis)lenis.scrollTo(t,{offset:-84});else t.scrollIntoView({behavior:reduce?'auto':'smooth'})});
/* deep-link hash scroll and glow */
function checkHash(){var h=window.location.hash;if(!h||h.length<2)return;try{var target=$(h);if(target){setTimeout(function(){if(lenis)lenis.scrollTo(target,{offset:-90});else target.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});target.classList.add('target-glow');setTimeout(function(){target.classList.remove('target-glow')},2800)},250)}}catch(err){}}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',checkHash);else checkHash();
window.addEventListener('hashchange',checkHash);

/* scroll reveal */
var rvs=$$('.rv');
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);countUp(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  rvs.forEach(function(el){io.observe(el)});
}else{rvs.forEach(function(el){el.classList.add('in')})}

/* animated counters */
function countUp(root){
  $$('[data-count]',root).concat(root.hasAttribute&&root.hasAttribute('data-count')?[root]:[]).forEach(function(b){
    if(b.dataset.done)return;b.dataset.done='1';var end=+b.dataset.count,suf=b.dataset.suf||'';
    if(reduce||!end){b.textContent=end+suf;return}
    var t0=performance.now(),dur=1400;
    (function step(t){var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,4);b.textContent=Math.round(end*e)+suf;if(p<1)requestAnimationFrame(step)})(t0);
  });
}

/* 3D tilt on cards (mouse only) */
if(fine&&!reduce){
  $$('[data-tilt]').forEach(function(el){
    var max=el.classList.contains('cta')?6:(el.classList.contains('step-card')?12:(el.classList.contains('rbody')?8:11));
    el.addEventListener('pointermove',function(e){
      var b=el.getBoundingClientRect(),x=(e.clientX-b.left)/b.width,y=(e.clientY-b.top)/b.height;
      el.classList.add('tilting');
      el.style.setProperty('--ry',((x-.5)*2*max).toFixed(2)+'deg');
      el.style.setProperty('--rx',((.5-y)*2*max).toFixed(2)+'deg');
      el.style.setProperty('--mx',(x*100).toFixed(1)+'%');el.style.setProperty('--my',(y*100).toFixed(1)+'%');
    });
    el.addEventListener('pointerleave',function(){el.classList.remove('tilting');el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg')});
  });
  /* hero scene follows the pointer */
  var sc=$('[data-scene]');
  if(sc){var st=$('.stage',sc);
    sc.addEventListener('pointermove',function(e){var b=sc.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;st.classList.add('live');st.style.setProperty('--ry',(-11+x*26).toFixed(2)+'deg');st.style.setProperty('--rx',(5-y*20).toFixed(2)+'deg')});
    sc.addEventListener('pointerleave',function(){st.classList.remove('live');st.style.setProperty('--ry','-11deg');st.style.setProperty('--rx','5deg')});
  }
}

/* hero keyword rotator */
var rot=$('[data-rot]');
if(rot&&!reduce){
  var ws=$$('span',rot),i=0;rot.setAttribute('data-live','1');ws[0].classList.add('on');
  setInterval(function(){ws[i].classList.remove('on');i=(i+1)%ws.length;ws[i].classList.add('on')},2600);
}

/* pause decorative SMIL motion when asked to reduce motion */
if(reduce)$$('svg.bgflow').forEach(function(s){try{s.pauseAnimations()}catch(e){}});

/* project filter: choosing an option highlights that option and blurs all other cards */
var chips=$$('.chip[data-f]');
if(chips.length){var cards=$$('[data-cat]'),count=$('#count');
chips.forEach(function(c){c.addEventListener('click',function(){var f=c.dataset.f,n=0;chips.forEach(function(x){x.setAttribute('aria-pressed',String(x===c))});
cards.forEach(function(k){var match=f==='all'||k.dataset.cat===f;if(match)n++;
  if(f==='all'||match){k.classList.remove('filter-blur');k.hidden=false;requestAnimationFrame(function(){k.classList.remove('out')})}
  else{k.classList.add('filter-blur');k.classList.add('out')}});
if(count)count.textContent=n+(n===1?' project':' projects');
if(lenis)setTimeout(function(){lenis.resize()},360)})})}

/* Interactive Card Choice / Selection: click to focus an option and blur others; click outside to reset */
d.addEventListener('click',function(e){
  var card=e.target.closest('.card, .pcard, .proof > div, .steps li, .file-list li');
  if(e.target.closest('a, button, input, textarea, select'))return;
  if(!card){
    $$('.card-active-focus').forEach(function(el){el.classList.remove('card-active-focus')});
    $$('.card-dimmed-by-focus').forEach(function(el){el.classList.remove('card-dimmed-by-focus')});
    return;
  }
  var container=card.closest('.grid, .pgrid, .proof, .steps, .file-list');
  if(!container)return;
  var wasActive=card.classList.contains('card-active-focus');
  $$('.card-active-focus',container).forEach(function(el){el.classList.remove('card-active-focus')});
  $$('.card-dimmed-by-focus',container).forEach(function(el){el.classList.remove('card-dimmed-by-focus')});
  if(!wasActive){
    card.classList.add('card-active-focus');
    var sibs=$$(':scope > .card, :scope > .pcard, :scope > div, :scope > li',container);
    sibs.forEach(function(s){if(s!==card)s.classList.add('card-dimmed-by-focus')});
  }
});

/* contact form: validate, then open an email draft (nothing is stored or sent by this site) */
var f=$('#enquiry');
if(f){f.setAttribute('novalidate','');
f.addEventListener('submit',function(e){e.preventDefault();var ok=true,em=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;
$$('[required]',f).forEach(function(i){var m=i.parentNode.querySelector('.err'),bad=!i.value.trim()||(i.type==='email'&&!em.test(i.value));if(m)m.textContent=bad?(i.type==='email'?'Enter a valid email address.':'This field is required.'):'';i.setAttribute('aria-invalid',String(bad));if(bad&&ok){i.focus();ok=false}});
if(!ok)return;var v=function(n){return(f.elements[n]&&f.elements[n].value||'').trim()};
var body=['Name: '+v('name'),'Email: '+v('email'),'Company: '+(v('company')||'-'),'Service: '+v('service'),'Engagement: '+v('type'),'Timeline: '+v('timeline'),'Reference: '+(v('ref')||'-'),'','What I need:',v('msg')].join('\n');
location.href='mailto:trkr725@gmail.com?subject='+encodeURIComponent('Project enquiry: '+v('service'))+'&body='+encodeURIComponent(body);
var s=$('#sent');if(s)s.hidden=false})}

$$('[data-copy]').forEach(function(b){b.addEventListener('click',function(){var t=b.dataset.copy;if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){var o=b.textContent;b.textContent='Copied';setTimeout(function(){b.textContent=o},1500)})})});
d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});
})();

