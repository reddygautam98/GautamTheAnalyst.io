/* Lightweight 3D visual layer for Gautam The Analyst. No third-party library required. */
(()=>{'use strict';
const root=document.documentElement,$=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>Array.from(c.querySelectorAll(s));
const reduce=!!(matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
const fine=!!(matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches);
const ptr={x:0,y:0};addEventListener('pointermove',e=>{ptr.x=e.clientX/Math.max(1,innerWidth)*2-1;ptr.y=e.clientY/Math.max(1,innerHeight)*2-1},{passive:true});
const page=(location.pathname.split('/').pop()||'index.html').toLowerCase();
const shape=({'about.html':'torus','services.html':'lattice','projects.html':'icosa','resume.html':'torus','contact.html':'lattice'})[page]||'sphere';
function background(){
 if($('.fx3d-background'))return;
 const host=document.createElement('div');host.className='fx3d-background';host.setAttribute('aria-hidden','true');
 const canvas=document.createElement('canvas');canvas.className='fx3d-starfield';host.append(canvas);
 for(let i=1;i<=3;i++){const o=document.createElement('i');o.className='fx3d-orb fx3d-orb-'+i;host.append(o);}
 for(let i=1;i<=2;i++){const c=document.createElement('i');c.className='fx3d-cube fx3d-cube-'+i;host.append(c);}
 document.body.prepend(host);const ctx=canvas.getContext('2d');if(!ctx)return;
 let w=1,h=1,dpr=1,stars=[],raf=0,visible=true,shot=null,nextShot=0,frameNo=0;
 function resize(){w=innerWidth||1;h=innerHeight||1;dpr=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);stars=Array.from({length:Math.min(120,Math.round(w*h/8500))},()=>({x:Math.random()*w,y:Math.random()*h,z:.2+Math.random()*.8,r:.4+Math.random()*1.15,p:Math.random()*6.28}));draw(performance.now(),true);}
 function draw(t,once=false){ctx.clearRect(0,0,w,h);const dark=root.dataset.theme!=='light';
  for(const s of stars){const dx=reduce?0:ptr.x*7*s.z+Math.sin(t*.00025+s.p)*2;ctx.globalAlpha=(dark?.15:.08)+s.z*(dark?.48:.25);ctx.fillStyle=s.z>.7?(dark?'#b9f4ff':'#277da0'):(dark?'#dbe8ff':'#64748b');ctx.beginPath();ctx.arc((s.x+dx+w)%w,s.y+(reduce?0:Math.sin(t*.0003+s.p)*2),s.r*s.z,0,Math.PI*2);ctx.fill();}
  if(!reduce&&!once){if(!shot&&t>nextShot){shot={x:Math.random()*w*.7,y:Math.random()*h*.5,len:50+Math.random()*75,age:0};nextShot=t+4300+Math.random()*5000;}if(shot){shot.age+=16;ctx.globalAlpha=Math.max(0,1-shot.age/420);const g=ctx.createLinearGradient(shot.x,shot.y,shot.x+shot.len,shot.y+shot.len*.3);g.addColorStop(0,'rgba(56,225,255,0)');g.addColorStop(.7,dark?'rgba(56,225,255,.8)':'rgba(31,125,155,.55)');g.addColorStop(1,'rgba(255,122,53,0)');ctx.strokeStyle=g;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(shot.x,shot.y);ctx.lineTo(shot.x+shot.len,shot.y+shot.len*.3);ctx.stroke();shot.x+=2.4;shot.y+=.7;if(shot.age>420)shot=null;}}
  ctx.globalAlpha=1;if(!reduce&&!once)raf=requestAnimationFrame(draw);else raf=0;
 }
 const start=()=>{if(!raf&&visible&&!document.hidden&&!reduce)raf=requestAnimationFrame(draw)},stop=()=>{if(raf)cancelAnimationFrame(raf);raf=0};
 addEventListener('resize',resize,{passive:true});addEventListener('scroll',()=>{if(!reduce)root.style.setProperty('--fx3d-hue',Math.min(24,scrollY*.012)+'deg')},{passive:true});
 document.addEventListener('visibilitychange',()=>document.hidden?stop():start());
 if('IntersectionObserver'in window)new IntersectionObserver(([e])=>{visible=e.isIntersecting;visible?start():stop()}).observe(host);
 addEventListener('gta-theme',()=>draw(performance.now(),true));resize();if(!reduce)start();
}
function makeMesh(kind){
 const p=[],edges=[],seen=new Set(),link=(a,b)=>{const k=a<b?a+':'+b:b+':'+a;if(!seen.has(k)){seen.add(k);edges.push([a,b]);}};
 if(kind==='torus'){const U=20,V=9,R=.68,r=.28;for(let u=0;u<U;u++)for(let v=0;v<V;v++){let a=u/U*6.283,b=v/V*6.283;p.push([(R+r*Math.cos(b))*Math.cos(a),r*Math.sin(b),(R+r*Math.cos(b))*Math.sin(a)]);}const id=(u,v)=>(u%U)*V+(v%V);for(let u=0;u<U;u++)for(let v=0;v<V;v++){link(id(u,v),id(u+1,v));link(id(u,v),id(u,v+1));}}
 else if(kind==='lattice'){const N=3,id=(x,y,z)=>(x*N+y)*N+z;for(let x=0;x<N;x++)for(let y=0;y<N;y++)for(let z=0;z<N;z++)p.push([(x-1)*.65,(y-1)*.65,(z-1)*.65]);for(let x=0;x<N;x++)for(let y=0;y<N;y++)for(let z=0;z<N;z++){if(x<N-1)link(id(x,y,z),id(x+1,y,z));if(y<N-1)link(id(x,y,z),id(x,y+1,z));if(z<N-1)link(id(x,y,z),id(x,y,z+1));}}
 else if(kind==='icosa'){const q=(1+Math.sqrt(5))/2,raw=[[-1,q,0],[1,q,0],[-1,-q,0],[1,-q,0],[0,-1,q],[0,1,q],[0,-1,-q],[0,1,-q],[q,0,-1],[q,0,1],[-q,0,-1],[-q,0,1]];raw.forEach(a=>{let l=Math.hypot(...a);p.push(a.map(v=>v/l));});p.forEach((a,i)=>p.forEach((b,j)=>{if(j>i&&Math.hypot(a[0]-b[0],a[1]-b[1],a[2]-b[2])<1.07)link(i,j);}));}
 else{const R=9,S=18;for(let r=0;r<R;r++){const lat=(r/(R-1)-.5)*Math.PI;for(let s=0;s<S;s++){const lon=s/S*6.283;p.push([Math.cos(lat)*Math.cos(lon),Math.sin(lat),Math.cos(lat)*Math.sin(lon)]);}}const id=(r,s)=>r*S+s%S;for(let r=0;r<R;r++)for(let s=0;s<S;s++){link(id(r,s),id(r,s+1));if(r<R-1)link(id(r,s),id(r+1,s));}}
 return {p,edges};
}
function solid(canvas,kind){
 const c=canvas.getContext('2d');if(!c)return;const m=makeMesh(kind);let w=1,h=1,dpr=1,raf=0,visible=true,ax=.32,ay=.2,last=0;
 function resize(){const r=canvas.getBoundingClientRect();w=Math.max(1,r.width);h=Math.max(1,r.height);dpr=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);c.setTransform(dpr,0,0,dpr,0,0);draw(performance.now(),true);}
 function draw(t,once=false){c.clearRect(0,0,w,h);const dark=root.dataset.theme!=='light',dt=Math.min(40,t-(last||t-16));last=t;if(!reduce&&!once){ay+=dt*.00017;ax+=Math.sin(t*.0002)*.0005;}
  const a=reduce?.36:ax+ptr.y*.16,b=reduce?.36:ay+ptr.x*.22,sx=Math.sin(a),cx=Math.cos(a),sy=Math.sin(b),cy=Math.cos(b),scale=Math.min(w,h)*.37;
  const out=m.p.map(([x,y,z])=>{const X=x*cy+z*sy,Z=-x*sy+z*cy,Y=y*cx-Z*sx,D=y*sx+Z*cx,k=2.7/(2.7-D*.45);return{x:w/2+X*scale*k,y:h/2+Y*scale*k,z:D};});
  m.edges.forEach(([i,j],n)=>{const p=out[i],q=out[j],d=(p.z+q.z+2)/4;const rgb=dark?['56,225,255','143,125,255','255,122,53'][n%3]:['31,139,163','99,87,197','226,103,44'][n%3];c.strokeStyle='rgba('+rgb+','+(.13+d*.48)+')';c.lineWidth=.55+d*.6;c.beginPath();c.moveTo(p.x,p.y);c.lineTo(q.x,q.y);c.stroke();});
  out.forEach(p=>{c.fillStyle='rgba('+(dark?'190,247,255':'45,121,149')+','+(.16+(p.z+1)*.22)+')';c.beginPath();c.arc(p.x,p.y,1+Math.max(0,p.z),0,6.283);c.fill();});
  if(!reduce&&!once)raf=requestAnimationFrame(draw);else raf=0;
 }
 const start=()=>{if(!raf&&visible&&!document.hidden&&!reduce)raf=requestAnimationFrame(draw)},stop=()=>{if(raf)cancelAnimationFrame(raf);raf=0};
 if('ResizeObserver'in window)new ResizeObserver(resize).observe(canvas);else addEventListener('resize',resize,{passive:true});
 if('IntersectionObserver'in window)new IntersectionObserver(([e])=>{visible=e.isIntersecting;visible?start():stop()}).observe(canvas);
 document.addEventListener('visibilitychange',()=>document.hidden?stop():start());addEventListener('gta-theme',()=>draw(performance.now(),true));resize();if(!reduce)start();
}
function heroObjects(){const orbit=$('.hero-orbit');if(orbit){orbit.classList.add('fx3d-stage');if(!$('.fx3d-hero-canvas',orbit)){const c=document.createElement('canvas');c.className='fx3d-hero-canvas';c.setAttribute('aria-hidden','true');orbit.prepend(c);solid(c,'sphere');}return;}
 const host=$('main .section-heading')||$('.hero .wrap')||$('main .hero');if(host&&!$('.fx3d-subpage-canvas',host)){host.classList.add('fx3d-subpage-stage');const c=document.createElement('canvas');c.className='fx3d-subpage-canvas';c.setAttribute('aria-hidden','true');host.append(c);solid(c,shape);}
}
function toolkitRing(){const host=$('#fx3d-tool-ring'),ring=$('.fx3d-ring',host);if(!host||!ring)return;const items=$$('.fx3d-ring-item',ring);let rot=0,drag=false,x0=0,r0=0,raf=0,last=0;
 const paint=()=>{ring.style.transform='rotateY('+rot+'deg)'};
 function layout(){const radius=Math.max(105,Math.min(220,host.clientWidth*.36));items.forEach((it,i)=>it.style.transform='translate(-50%,-50%) rotateY('+(i*360/items.length)+'deg) translateZ('+radius+'px)');paint();}
 function frame(t){raf=0;if(!document.hidden&&!reduce&&!drag){rot=(rot+Math.min(40,t-(last||t-16))*.0035)%360;paint();}last=t;if(!document.hidden&&!reduce)raf=requestAnimationFrame(frame);}
 function down(e){drag=true;x0=e.clientX;r0=rot;host.classList.add('is-dragging');if(host.setPointerCapture)host.setPointerCapture(e.pointerId);}
 function move(e){if(drag){rot=r0+(e.clientX-x0)*.42;paint();}}
 function up(){drag=false;host.classList.remove('is-dragging');}
 host.addEventListener('pointerdown',down);host.addEventListener('pointermove',move);host.addEventListener('pointerup',up);host.addEventListener('pointercancel',up);host.addEventListener('lostpointercapture',up);
 host.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();rot+=(e.key==='ArrowLeft'?-18:18);paint();}});
 addEventListener('resize',layout,{passive:true});document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelAnimationFrame(raf);else if(!reduce&&!raf)raf=requestAnimationFrame(frame);});layout();if(!reduce)raf=requestAnimationFrame(frame);
}
function cardDepth(){if(reduce||!fine)return;$$('.project-card,.service-card,.benefit-card,.benefit,.metric-card,.detail-card,.lifecycle-step,.contact-info-card,.sample-card,.card').forEach(el=>{el.classList.add('fx3d-card');const glare=document.createElement('span');glare.className='fx3d-glare';glare.setAttribute('aria-hidden','true');el.appendChild(glare);el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/Math.max(1,r.width),y=(e.clientY-r.top)/Math.max(1,r.height);el.style.setProperty('--fx3d-rx',((.5-y)*6).toFixed(2)+'deg');el.style.setProperty('--fx3d-ry',((x-.5)*7).toFixed(2)+'deg');el.style.setProperty('--fx3d-glare-x',(x*100).toFixed(1)+'%');el.style.setProperty('--fx3d-glare-y',(y*100).toFixed(1)+'%');},{passive:true});el.addEventListener('pointerleave',()=>{el.style.setProperty('--fx3d-rx','0deg');el.style.setProperty('--fx3d-ry','0deg');});});}
function init(){background();heroObjects();toolkitRing();cardDepth();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();