/* ===== 로딩 화면 (11-13): 하늘에서 금빛 줄기가 졸졸 떨어져 성배를 채우고, 넘쳐 쏟아진 뒤 성배와 검은 배경이 픽셀로 흩어진다 =====
   게임 HTML 맨 앞(<body> 바로 뒤)에 들어가 가장 먼저 그려진다. 문서가 다 불러와지고 로비 배경까지 그려지면 끝난다. */
(()=>{
const ld=document.getElementById('ldScr'),cb=document.getElementById('ldBg'),cc=document.getElementById('ldCup'),tx=document.getElementById('ldTxt');
const bx=cb.getContext('2d'),cx=cc.getContext('2d');

let run=null,DPR=1,VW=0,VH=0;
const rand=Math.random,clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2,eo=t=>1-Math.pow(1-t,3);
const hs=(x,y)=>{let n=Math.imul(x|0,374761393)+Math.imul(y|0,668265263);n=Math.imul(n^n>>>13,1274126177);return((n^n>>>16)>>>0)/4294967296};
const vn=(x,y)=>{const xi=Math.floor(x),yi=Math.floor(y),fx=x-xi,fy=y-yi,u=fx*fx*(3-2*fx),v=fy*fy*(3-2*fy);return(hs(xi,yi)*(1-u)+hs(xi+1,yi)*u)*(1-v)+(hs(xi,yi+1)*(1-u)+hs(xi+1,yi+1)*u)*v};
function size(){DPR=Math.min(2,devicePixelRatio||1);VW=innerWidth;VH=innerHeight;for(const c of [cb,cc]){c.width=Math.round(VW*DPR);c.height=Math.round(VH*DPR)}}
/* --- 성배 모양 (단위: 높이 240) --- */
const bz=(p0,p1,p2,p3,t)=>{const u=1-t;return u*u*u*p0+3*u*u*t*p1+3*u*t*t*p2+t*t*t*p3};
// 몸통 바깥선: 테두리(72,0) → 바닥(13,100)
const BOWL=[[72,0],[73,58],[40,94],[13,100]];
const bowlW=y=>{if(y<=0)return 72;if(y>=100)return 13;let lo=0,hi=1;for(let i=0;i<18;i++){const m=(lo+hi)/2;bz(BOWL[0][1],BOWL[1][1],BOWL[2][1],BOWL[3][1],m)<y?lo=m:hi=m}return bz(BOWL[0][0],BOWL[1][0],BOWL[2][0],BOWL[3][0],lo)};
// 몸통 · 마디 · 대 · 받침의 반폭 (흘러내리는 줄기가 겉면을 따라가게)
const outW=y=>y<=100?bowlW(y):y<=108?13-(y-100)*.6:y<=128?8+10*Math.sin(Math.PI*(y-108)/20):y<=184?7+ (y-128)*.004:y<=214?7+43*eo((y-184)/30):50;
function cupPath(c){c.beginPath();c.moveTo(-72,0);c.bezierCurveTo(-73,58,-40,94,-13,100);c.lineTo(-8,106);c.bezierCurveTo(-20,110,-20,126,-8,130);c.lineTo(-7,184);c.bezierCurveTo(-12,200,-36,210,-52,214);c.bezierCurveTo(-56,222,56,222,52,214);c.bezierCurveTo(36,210,12,200,7,184);c.lineTo(8,130);c.bezierCurveTo(20,126,20,110,8,106);c.lineTo(13,100);c.bezierCurveTo(40,94,73,58,72,0);c.closePath()}
function bowlPath(c,inset=0){c.beginPath();c.moveTo(-72+inset,0);c.bezierCurveTo(-73+inset,58,-40+inset*.6,94-inset,-13,100-inset);c.lineTo(13,100-inset);c.bezierCurveTo(40-inset*.6,94-inset,73-inset,58,72-inset,0);c.closePath()}
/* --- 한 판 그리기 --- */
function geom(){const H=Math.min(VH*.34,VW*.62,300)/3,S=H/240;return{S,X:VW/2,Y:VH*.46-H*.52,H}}
function drawCup(c,g,st,T){  // st: p(차오름 0..1), ov(넘침 시작 뒤 초), glow
  const {S,X,Y}=g;c.save();c.translate(X,Y);c.scale(S,S);
  const p=st.p,ov=st.ov,lvl=ov>=0?-2:100-p*96;
  // 뒤쪽 기운
  const gl=.18+.42*p+(ov>=0?.5*clamp(ov/.35)*(1-.35*clamp((ov-.6)/1.2)):0);
  let rg=c.createRadialGradient(0,60,0,0,60,Math.min(270,130+60*p+(ov>=0?80*eo(clamp(ov/.6)):0)));rg.addColorStop(0,`rgba(255,196,96,${.55*gl})`);rg.addColorStop(.35,`rgba(240,150,50,${.22*gl})`);rg.addColorStop(1,'rgba(200,110,30,0)');
  c.fillStyle=rg;c.fillRect(-300,-240,600,620);
  // 넘친 기운이 바닥에 고인다
  if(ov>=0){const k=eo(clamp((ov-.25)/1.1));const pr=c.createRadialGradient(0,222,0,0,222,40+110*k);pr.addColorStop(0,`rgba(255,214,130,${.75*k})`);pr.addColorStop(.5,`rgba(240,160,60,${.35*k})`);pr.addColorStop(1,'rgba(220,120,40,0)');c.save();c.scale(1,.22);c.fillStyle=pr;c.beginPath();c.arc(0,222/.22,40+110*k,0,7);c.fill();c.restore()}
  // 잔 몸체: 속이 비치지 않는 금속 잔
  cupPath(c);const bd=c.createLinearGradient(-72,0,72,0);bd.addColorStop(0,'#2a1c0e');bd.addColorStop(.28,'#6e4c22');bd.addColorStop(.43,'#c69a55');bd.addColorStop(.52,'#8a6430');bd.addColorStop(.75,'#4a321a');bd.addColorStop(1,'#1d130a');c.fillStyle=bd;c.fill();
  c.save();cupPath(c);c.clip();const sh=c.createLinearGradient(0,0,0,222);sh.addColorStop(0,'rgba(0,0,0,0)');sh.addColorStop(1,'rgba(10,6,3,.45)');c.fillStyle=sh;c.fillRect(-80,0,160,224);
  // 차오를수록 잔 겉이 안쪽에서 데워지듯 은은하게 달아오른다
  c.globalCompositeOperation='lighter';const wm=c.createRadialGradient(0,30,0,0,30,80);wm.addColorStop(0,`rgba(255,170,70,${.28*p})`);wm.addColorStop(1,'rgba(255,140,40,0)');c.fillStyle=wm;c.fillRect(-80,-10,160,140);c.restore();
  // 잔 입구: 위에서 내려다보이는 안쪽에만 금빛이 고인다
  c.beginPath();c.ellipse(0,0,70,9,0,0,7);c.fillStyle='#0b0705';c.fill();
  if(p>0){c.save();c.beginPath();c.ellipse(0,0,70,9,0,0,7);c.clip();c.globalCompositeOperation='lighter';const sr=c.createRadialGradient(0,1,0,0,1,70);sr.addColorStop(0,`rgba(255,236,170,${.95*Math.min(1,p*1.3)})`);sr.addColorStop(.55,`rgba(250,190,90,${.75*p})`);sr.addColorStop(1,`rgba(200,120,40,${.35*p})`);c.fillStyle=sr;c.save();c.scale(1,9/70);c.beginPath();c.arc(0,1*70/9,70,0,7);c.fill();c.restore();
    for(let k=0;k<3;k++){c.strokeStyle=`rgba(255,245,210,${.25*p})`;c.lineWidth=.8;c.beginPath();const r=((T*.9+k/3)%1)*60;c.ellipse(0,0,r,r*9/70,0,0,7);c.stroke()}c.restore()}
  // 테두리 · 새김선
  c.lineWidth=1.4/S*1.1;c.strokeStyle=`rgba(232,186,104,${.55+.35*p})`;cupPath(c);c.stroke();
  c.lineWidth=1.2/S;c.strokeStyle=`rgba(232,186,104,${.35+.3*p})`;[[18,.8],[30,.6]].forEach(([y,a])=>{const w=bowlW(y);c.beginPath();c.ellipse(0,y,w,w*.13,0,0,Math.PI);c.globalAlpha=a;c.stroke()});c.globalAlpha=1;
  c.beginPath();c.ellipse(0,118,17,4,0,0,Math.PI);c.stroke();
  // 입구 고리: 넘칠 때 하얗게 달아오른다
  const hot=ov>=0?clamp(ov/.25):p*.4;c.lineWidth=(1.6+2.2*hot)/S*1.2;c.strokeStyle=`rgba(${255},${Math.round(206+40*hot)},${Math.round(130+100*hot)},${.7+.3*hot})`;c.beginPath();c.ellipse(0,0,72,9.5,0,0,7);c.stroke();
  // 넘침 ① 잔 겉면을 타고 금빛이 흘러내린다 (앞자락이 군데군데 길게 늘어진다)
  if(ov>=0){const D=eo(clamp(ov/1.3))*235;c.save();cupPath(c);c.clip();
    const cg=c.createLinearGradient(0,0,0,230);cg.addColorStop(0,'rgba(255,236,170,.95)');cg.addColorStop(.4,'rgba(248,190,90,.9)');cg.addColorStop(1,'rgba(200,120,40,.85)');c.fillStyle=cg;
    c.beginPath();c.moveTo(-90,-12);c.lineTo(90,-12);for(let x=90;x>=-90;x-=2){let dr=0;for(const q of st.drips)dr+=q.h*Math.exp(-((x-q.x)*(x-q.x))/(2*q.s*q.s));c.lineTo(x,Math.min(240,D*(.78+.22*Math.sin(x*.05+1.3))+dr*clamp(ov/.8)+3*Math.sin(x*.3+T*4)))}c.closePath();c.fill();
    // 겉면의 결: 흐르는 빛줄기 몇 가닥
    c.globalCompositeOperation='lighter';c.strokeStyle='rgba(255,240,200,.35)';c.lineWidth=1.2;for(let k=0;k<5;k++){const f=-.7+k*.35,ph=(T*1.6+k*.37)%1;c.beginPath();for(let y=4;y<Math.min(D,225);y+=6){const w=outW(y);c.lineTo(f*w*.9,y)}c.setLineDash([10,26]);c.lineDashOffset=-ph*36;c.stroke()}c.setLineDash([]);c.restore();
  // 넘침 ② 테두리 양끝에서 바닥으로 쏟아지는 줄기
    c.save();c.globalCompositeOperation='lighter';c.lineCap='round';
    st.falls.forEach(f=>{const t=clamp(ov-f.d,0,4);if(t<=0)return;const tl=Math.max(0,t-.55-f.d);const N=26;let pts=[];for(let k=0;k<=N;k++){const u=tl+(t-tl)*k/N,y=Math.min(222,.5*f.g*u*u),x=f.s*(73+f.vx*u+2.5*Math.sin(u*9+f.ph));pts.push([x,y]);}
      const hy=pts[pts.length-1][1];if(hy>=221&&ov<.65&&rand()<.5)st.pt.push({x:g.X+pts[pts.length-1][0]*g.S,y:g.Y+222*g.S,vx:f.s*(20+rand()*50),vy:-(40+rand()*90),g:420,l:0,L:.35+rand()*.3,r:.8+rand()*1.2});
      for(const [lw,a] of [[f.w*3.6,.16],[f.w,.92]]){c.lineWidth=lw;const lg=c.createLinearGradient(0,pts[0][1],0,hy+1);lg.addColorStop(0,`rgba(255,226,150,${a})`);lg.addColorStop(1,`rgba(255,170,70,${a*.35})`);c.strokeStyle=lg;c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.stroke()}});
    c.restore()}
  c.restore()}
/* --- 하늘에서 졸졸 떨어지는 금빛 줄기 --- */
function drawStream(c,g,st,T,dt){const {X,Y,S}=g,G=900;const t=(performance.now()-st.t0)/1000;
  const head=Math.min(Y,.5*G*t*t),tail=st.ov>=0?Math.min(Y,.5*G*st.ov*st.ov):0;st.hit=head>=Y&&tail<Y;if(tail>=Y)return;
  const xa=y=>X+1.1*Math.sin(y*.035-T*7)*(1-y/Y*.8);
  c.save();c.globalCompositeOperation='lighter';c.lineCap='round';
  const path=()=>{c.beginPath();for(let y=tail;y<=head;y+=6)c.lineTo(xa(y),y);c.lineTo(xa(head),head)};
  const lg=(a0,a1)=>{const q=c.createLinearGradient(0,0,0,Y);q.addColorStop(0,`rgba(255,220,150,${a0})`);q.addColorStop(1,`rgba(255,226,160,${a1})`);return q};
  c.lineWidth=6;c.strokeStyle=lg(.02,.14);path();c.stroke();
  c.lineWidth=1;c.strokeStyle=lg(.08,.5);path();c.stroke();
  // 끊어질 듯 이어지는 물방울 줄: 아래로 흘러간다
  c.lineWidth=1.8;c.strokeStyle=lg(.25,.95);c.setLineDash([9,7,4,9]);c.lineDashOffset=-(T*320)%29;path();c.stroke();c.setLineDash([]);
  // 굵은 방울이 이따금 떨어진다
  st.beads=st.beads||[];if(st.ov<0&&rand()<dt*9)st.beads.push({y:0,v:120+rand()*120,r:1.3+rand()*1});
  for(let i=st.beads.length-1;i>=0;i--){const q=st.beads[i];q.v+=G*dt*.6;q.y+=q.v*dt;if(q.y>=Y){st.beads.splice(i,1);continue}const a=.25+.7*q.y/Y;c.fillStyle=`rgba(255,236,180,${a})`;c.beginPath();c.ellipse(xa(q.y),q.y,q.r*.8,q.r*1.8,0,0,7);c.fill()}
  c.restore()}
/* --- 불티 --- */
function sparks(st,g,dt,T){const {S,X,Y}=g;const P=st.pt;
  const rate=st.ov>=0?(st.ov<.65?120:0):(st.hit?26:0); // 픽셀로 흩어지기 시작하면 새 불티는 더 만들지 않는다let n=rate*dt;while(n>0){if(rand()<n){if(st.ov>=0){const f=(rand()*2-1);P.push({x:X+f*72*S,y:Y+(9*Math.sqrt(1-f*f))*S,vx:f*60*S/2.4*(.5+rand()),vy:-20*S*rand(),g:260*S,l:0,L:.8+rand()*.6,r:(.8+rand()*1.4)})}else{const sg=rand()<.5?-1:1;P.push({x:X+sg*rand()*2,y:Y,vx:sg*(15+rand()*45),vy:-(40+rand()*90),g:520,l:0,L:.28+rand()*.3,r:.5+rand()*.9})}}n--}
  for(let i=P.length-1;i>=0;i--){const q=P[i];q.l+=dt;if(q.l>q.L){P.splice(i,1);continue}q.vy+=q.g*dt;q.x+=q.vx*dt;q.y+=q.vy*dt}}
function drawSparks(c,st){c.save();c.globalCompositeOperation='lighter';for(const q of st.pt){const a=1-q.l/q.L;c.fillStyle=`rgba(255,${200+Math.round(40*a)},${120+Math.round(80*a)},${a})`;c.beginPath();c.arc(q.x,q.y,q.r,0,7);c.fill()}c.restore()}
/* --- 픽셀로 지우기: 칸마다 사라지는 순서를 정해 두고, 지난 칸은 지우개 판에 쌓는다 --- */
function cells(x0,y0,w,h,cs,thrF){const L=[];for(let y=y0;y<y0+h;y+=cs)for(let x=x0;x<x0+w;x+=cs)L.push({x,y,t:thrF(x+cs/2,y+cs/2)});L.sort((a,b)=>a.t-b.t);return{L,i:0,cs}}
function eraseTo(m,mc,t){const c=mc.getContext('2d');c.fillStyle='#000';const out=[];while(m.i<m.L.length&&m.L[m.i].t<=t){const q=m.L[m.i++];c.fillRect(q.x*DPR,q.y*DPR,m.cs*DPR+.5,m.cs*DPR+.5);out.push(q)}return out}
/* --- 진행 --- */
const ui=document.body,RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
ui.classList.add('ld-on');
let ready=false,readyAt=0;
function finish(){if(ready)return;ready=true;readyAt=performance.now()}
// 끝나는 조건: 문서와 그 안의 그림 · 글꼴이 다 불러와지고, 로비라면 배경까지 그려졌을 때. 무슨 일이 있어도 15초 뒤엔 끝낸다
(function wait(){const lobby=()=>{if(typeof LOBBY!=='undefined'&&LOBBY.active&&LOBBY.onReady)LOBBY.onReady(finish);else finish()};
  const go=()=>setTimeout(lobby,120);if(document.readyState==='complete')go();else addEventListener('load',go,{once:true});setTimeout(finish,15000)})();
function play(){size();
  const st={p:0,ov:-1,pt:[],t0:performance.now(),phase:'fill'};
  st.drips=Array.from({length:6},()=>({x:(rand()*2-1)*60,h:20+rand()*55,s:4+rand()*6}));st.falls=[];[-1,1].forEach(sg=>{for(let k=0;k<2;k++)st.falls.push({s:sg,d:.08+k*.14+rand()*.1,g:430+rand()*140,vx:28+rand()*30,w:2+rand()*2.2,ph:rand()*6})});
  run=st;let lastT=performance.now();
  let g=geom();
  addEventListener('resize',()=>{if(ld.hidden)return;size();g=geom();if(st.cm){st.cm=null;st.bm=null}});
  // 움직임 줄이기: 줄기 · 넘침 · 픽셀 없이, 다 차면 조용히 걷힌다
  if(RM){(function f(now){if(run!==st)return;st.p=ready?1:.6;cx.setTransform(1,0,0,1,0,0);cx.clearRect(0,0,cc.width,cc.height);cx.setTransform(DPR,0,0,DPR,0,0);drawCup(cx,g,st,0);bx.setTransform(DPR,0,0,DPR,0,0);bx.fillStyle='#07060b';bx.fillRect(0,0,VW,VH);tx.querySelector('b').textContent=Math.round(st.p*100)+'%';
    if(ready&&now-readyAt>300){ui.classList.remove('ld-on');ld.style.transition='opacity .4s';ld.style.opacity=0;setTimeout(()=>{ld.hidden=true},450);return}requestAnimationFrame(f)})(performance.now());return}
  function frame(now){if(run!==st)return;const dt=Math.min(.05,(now-lastT)/1000);lastT=now;const T=(now-st.t0)/1000;
    // 차오름: 줄기가 잔에 닿은 뒤부터. 준비가 덜 됐으면 85% 근처에서 기다리고, 준비되면 마저 채운다(적어도 1.4초는 차오른다)
    if(st.phase==='fill'){const hd=Math.sqrt(2*g.Y/900),tt=Math.max(0,T-hd);
      const base=.85*(1-Math.exp(-tt/1.6));
      if(!ready){st.p=base}else{if(st.pr0===undefined){st.pr0=Math.min(st.p,base);st.prT=now}const k=clamp((now-st.prT)/700);st.p=Math.max(st.p,st.pr0+(1-st.pr0)*ease(k));if(k>=1&&tt>=1.4&&st.p>=.999){st.phase='over';st.ovT=now}}}
    if(st.phase!=='fill')st.ov=(now-st.ovT)/1000;
    // 지우기 준비: 넘치기 시작하고 잠시 뒤
    const DS=.65,DD=1.5;
    if(st.ov>=DS&&!st.cm){const R=Math.min(VW,VH);st.cbox=[Math.max(0,g.X-300*g.S),Math.max(0,g.Y-240*g.S),600*g.S,620*g.S];const cs=Math.max(2,Math.round(g.S*4));
      const [x0,y0,w0,h0]=st.cbox;st.cm=cells(Math.floor(x0/cs)*cs,Math.floor(y0/cs)*cs,w0+cs,h0+cs,cs,(x,y)=>.55*rand()+.45*vn(x/(cs*7),y/(cs*7)));st.cmk=document.createElement('canvas');st.cmk.width=cc.width;st.cmk.height=cc.height;
      try{st.samp=cx.getImageData(0,0,cc.width,cc.height)}catch(e){st.samp=null}
      const bs=Math.max(8,Math.round(R/34));st.bm=cells(0,0,VW+bs,VH+bs,bs,(x,y)=>{const d=Math.hypot(x-g.X,y-(g.Y+60*g.S))/Math.hypot(VW,VH)*1.6;return .5*clamp(d)+.5*rand()});st.bmk=document.createElement('canvas');st.bmk.width=cb.width;st.bmk.height=cb.height}
    // 성배
    sparks(st,g,dt,T);cx.setTransform(1,0,0,1,0,0);cx.clearRect(0,0,cc.width,cc.height);cx.setTransform(DPR,0,0,DPR,0,0);drawCup(cx,g,st,T);drawStream(cx,g,st,T,dt);
    let dk=st.cm?clamp((st.ov-DS)/DD):0;
    if(st.cm){const gone=eraseTo(st.cm,st.cmk,dk);
      // 지워진 칸 가운데 그림이 있던 칸은 금빛 조각으로 잠깐 떠오른다
      if(st.samp)for(const q of gone){const px=Math.round((q.x+st.cm.cs/2)*DPR),py=Math.round((q.y+st.cm.cs/2)*DPR);if(px<0||py<0||px>=cc.width||py>=cc.height)continue;const o=(py*cc.width+px)*4,a=st.samp.data[o+3];if(a>60&&rand()<.35)st.pt.push({x:q.x+st.cm.cs/2,y:q.y+st.cm.cs/2,vx:(rand()-.5)*30,vy:-(30+rand()*70),g:-20,l:0,L:.5+rand()*.5,r:st.cm.cs*.45,sq:1,c:[st.samp.data[o],st.samp.data[o+1],st.samp.data[o+2]]})}
      cx.setTransform(1,0,0,1,0,0);cx.globalCompositeOperation='destination-out';cx.drawImage(st.cmk,0,0);cx.globalCompositeOperation='source-over';cx.setTransform(DPR,0,0,DPR,0,0)}
    // 불티와 조각
    const pf=1-clamp((st.ov-(DS+DD))/.5);cx.save();cx.globalCompositeOperation='lighter';for(const q of st.pt){const a=(1-q.l/q.L)*pf;if(q.sq){cx.fillStyle=`rgba(${q.c[0]},${q.c[1]},${q.c[2]},${a})`;cx.fillRect(q.x-q.r,q.y-q.r,q.r*2,q.r*2)}else{cx.fillStyle=`rgba(255,${200+Math.round(40*a)},${120+Math.round(80*a)},${a})`;cx.beginPath();cx.arc(q.x,q.y,q.r,0,7);cx.fill()}}cx.restore();
    // 글자
    tx.style.opacity=st.phase==='fill'?1:Math.max(0,1-st.ov/.3);tx.querySelector('b').textContent=Math.round(st.p*100)+'%';
    // 배경
    bx.setTransform(DPR,0,0,DPR,0,0);
    bx.globalCompositeOperation='source-over';bx.fillStyle='#07060b';bx.fillRect(0,0,VW,VH);
    if(!st.bgOff){st.bgOff=1;ld.style.background='none'} // 첫 장을 그린 뒤부터는 캔버스가 검은 바탕을 맡는다
    if(st.bm){eraseTo(st.bm,st.bmk,clamp((st.ov-DS-.1)/DD));bx.setTransform(1,0,0,1,0,0);bx.globalCompositeOperation='destination-out';bx.drawImage(st.bmk,0,0);bx.globalCompositeOperation='source-over'}
    // 끝: 화면 단추들이 서서히 나타난다
    if(st.ov>DS+DD*.75)ui.classList.remove('ld-on');
    if(st.ov>DS+DD+.6){st.pt.length=0;run=null;ld.hidden=true;ld.remove();return} // 끝나면 남은 불티까지 모두 걷어 낸다
    st.raf=requestAnimationFrame(frame)}
  st.raf=requestAnimationFrame(frame)}
play();
})();
