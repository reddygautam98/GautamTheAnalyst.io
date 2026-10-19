(function(){var s=document.currentScript,root=s?s.src.replace(/assets\/js\/v5\.js.*$/,''):'';
var have='stakeholder management,elicitation,process documentation,acceptance criteria,functional specification,sql,python,pandas,power bi,dax,power query,excel,jira,confluence,figma,brd,frd,fsd,user stories,bdd,rtm,uat,agile,scrum,rest api,api,bpmn,uml,moscow,sla,root cause,as-is,to-be,payment gateway,reconciliation,stakeholder,workshop,regression,change request,raci,gap analysis,data mapping'.split(','),
soon=[];
var d=document.createElement('div');d.className='v5-dock';
d.innerHTML='<a href="'+root+'resume.html">Resume</a><a href="'+root+'assets/T_Gautam_Reddy_BA_Resume.pdf" download>PDF</a><a href="mailto:reddygautam98@gmail.com">Email</a><button type="button" id="v5-fit">JD fit check</button>';
if(/resume\.html/.test(location.pathname)){var b=document.createElement('button');b.type='button';b.textContent='Save as PDF';b.onclick=function(){print()};d.insertBefore(b,d.firstChild)}document.body.appendChild(d);function sc(){d.classList.toggle('v5-show',scrollY>500)}addEventListener('scroll',sc,{passive:true});sc();
var p;d.querySelector('#v5-fit').onclick=function(){if(p){p.remove();p=null;return}
p=document.createElement('div');p.className='v5-panel';p.innerHTML='<h4>Paste a job description</h4><textarea placeholder="Paste JD text..."></textarea><p><button class="btn btn-primary btn-small" type="button">Check fit</button></p><div class="v5-res" aria-live="polite"></div>';
document.body.appendChild(p);p.querySelector('button').onclick=function(){var t=p.querySelector('textarea').value.toLowerCase(),o='';
function chips(a,c){return a.filter(function(k){return t.indexOf(k)>-1}).map(function(k){return '<span class="'+c+'">'+k+'</span>'}).join('')}
var a=chips(have,'v5-ok'),b=chips(soon,'v5-soon');
o=t.length<20?'Paste some JD text first.':'<b>Covered on this site</b><br>'+(a||'none found')+'<br><small>Keyword match only, not a full assessment.</small>';
p.querySelector('.v5-res').innerHTML=o}};
})();
(function(){var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;document.documentElement.classList.add('v5-js');
var els=document.querySelectorAll('.feat-card,.summary li,.metric');
if(!('IntersectionObserver' in window)||rm){els.forEach(function(e){e.classList.add('v5-in')})}else{
var io=new IntersectionObserver(function(l){l.forEach(function(x){if(x.isIntersecting){x.target.classList.add('v5-in');io.unobserve(x.target)}})},{threshold:.12});
els.forEach(function(e,i){e.style.setProperty('--d',(i%6)*70+'ms');io.observe(e)})}
if(!rm&&matchMedia('(hover:hover)').matches){document.querySelectorAll('.pay-card,.feat-card,.metric').forEach(function(el){
el.addEventListener('mousemove',function(e){var r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.setProperty('--tf','perspective(800px) rotateY('+(x*12)+'deg) rotateX('+(-y*12)+'deg) translateZ(8px)')});
el.addEventListener('mouseleave',function(){el.style.removeProperty('--tf')})})}
if(!rm)document.querySelectorAll('.pay-stats b').forEach(function(b){var m=b.textContent.match(/^(\d+)(.*)$/);if(!m)return;var n=+m[1],t0;function f(t){t0=t0||t;var p=Math.min((t-t0)/1200,1);b.textContent=Math.round(n*p)+m[2];if(p<1)requestAnimationFrame(f)}requestAnimationFrame(f)});
})();
