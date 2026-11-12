/* ---- 비스트 Ⅲ/R 연출 (11-12): 봉인 · 빈 자리 · 강림(+고쳐쓴 카르마) · 키아라 입장 · 단독현현 ---- */
function bxSealFx(fx){ xfxGo(fx.nb?'j_bx_empty':'j_bx_seal',()=>bxSealShow(fx)); }
function bxDescFx(fx){ xfxGo(fx.karma?['j_bx_desc','j_bx_karma']:'j_bx_desc',()=>bxDescShow(fx)); }
const BXF={pink:'255,150,200',pk2:'240,110,180',vio:'190,140,255',gold:'255,214,140'};
// 잔: 금빛 성배(검은 성배와 같은 모양, 색만 다름)
function bxCup(c,cx,base,s){ c.beginPath(); c.moveTo(cx-64*s,base-160*s);
  c.bezierCurveTo(cx-64*s,base-112*s,cx-40*s,base-80*s,cx-10*s,base-72*s); c.bezierCurveTo(cx-7*s,base-58*s,cx-6*s,base-34*s,cx-8*s,base-24*s); c.bezierCurveTo(cx-14*s,base-12*s,cx-40*s,base-9*s,cx-42*s,base);
  c.lineTo(cx+42*s,base); c.bezierCurveTo(cx+40*s,base-9*s,cx+14*s,base-12*s,cx+8*s,base-24*s); c.bezierCurveTo(cx+6*s,base-34*s,cx+7*s,base-58*s,cx+10*s,base-72*s); c.bezierCurveTo(cx+40*s,base-80*s,cx+64*s,base-112*s,cx+64*s,base-160*s); c.closePath(); }
function bxCupDraw(c,cx,base,s,a,D,tint){ if(a<=0) return; c.save(); c.globalAlpha=a; bxCup(c,cx,base,s);
  const g=c.createLinearGradient(cx-64*s,0,cx+64*s,0); g.addColorStop(0,'#c9a45c'); g.addColorStop(.2,'#6b4a1c'); g.addColorStop(.6,'#4a3212'); g.addColorStop(.9,'#a07a3a'); g.addColorStop(1,'#f0d9a0'); c.fillStyle=g; c.fill();
  c.lineWidth=1.3*D; c.strokeStyle='rgba(240,220,170,.6)'; c.stroke();
  const rimY=base-160*s; c.beginPath(); c.ellipse(cx,rimY,63*s,9*s,0,0,Math.PI*2); const rg=c.createRadialGradient(cx,rimY,2*s,cx,rimY,63*s); rg.addColorStop(0,`rgba(${tint||BXF.gold},.95)`); rg.addColorStop(1,'rgba(60,40,20,1)'); c.fillStyle=rg; c.fill();
  c.shadowColor=`rgba(${tint||BXF.gold},1)`; c.shadowBlur=20*D; c.strokeStyle=`rgba(${tint||BXF.gold},.9)`; c.lineWidth=2*D; c.stroke(); c.restore(); }
function bxGlow(c,x,y,r,col,a){ if(a<=.01) return; const g=c.createRadialGradient(x,y,0,x,y,r); g.addColorStop(0,`rgba(${col},${Math.min(1,a)})`); g.addColorStop(1,`rgba(${col},0)`); c.fillStyle=g; c.fillRect(x-r,y-r,r*2,r*2); }
function bxMoon(c,x,y,r,a,D){ if(a<=0) return; bxGlow(c,x,y,r*2.2,'200,150,255',.22*a); const g=c.createRadialGradient(x,y,0,x,y,r); g.addColorStop(0,`rgba(252,246,255,${a})`); g.addColorStop(.75,`rgba(236,214,255,${.9*a})`); g.addColorStop(1,`rgba(210,140,240,${.3*a})`);
  c.fillStyle=g; c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.fill(); c.fillStyle=`rgba(26,8,36,${.18*a})`; for(let yy=y-r;yy<y+r;yy+=4*D) c.fillRect(x-r,yy,r*2,1.2*D); }
// 연꽃: open 0~1, 꽃잎 두 겹
function bxLotus(c,cx,cy,R,open,rot,a,D,mono){ if(a<=0||R<=0) return; c.save(); c.translate(cx,cy); c.rotate(rot);
  for(const [n,len,wid,off,col] of [[12,1,.34,0,mono?'200,190,210':'255,170,210'],[8,.72,.4,Math.PI/8,mono?'230,225,235':'255,205,230']]){
    for(let i=0;i<n;i++){ const ang=i/n*Math.PI*2+off, L=R*len*(.25+.75*open), Wd=R*wid*(.35+.65*open);
      c.save(); c.rotate(ang); c.beginPath(); c.moveTo(0,0); c.bezierCurveTo(Wd,-L*.25,Wd*.8,-L*.8,0,-L); c.bezierCurveTo(-Wd*.8,-L*.8,-Wd,-L*.25,0,0);
      const g=c.createLinearGradient(0,0,0,-L); g.addColorStop(0,`rgba(${col},${.15*a})`); g.addColorStop(.7,`rgba(${col},${.55*a})`); g.addColorStop(1,`rgba(255,240,248,${.8*a})`); c.fillStyle=g; c.fill();
      c.strokeStyle=`rgba(${col},${.8*a})`; c.lineWidth=1*D; c.stroke(); c.restore(); } }
  c.restore(); }
function bxMandala(c,cx,cy,R,t,a,D){ if(a<=0) return; c.save(); c.strokeStyle=`rgba(255,170,215,${.55*a})`; c.lineWidth=1*D;
  for(const [k,sp,dash] of [[1,.15,[2,7]],[1.18,-.1,[10,6]],[1.36,.07,[1,10]]]){ c.save(); c.translate(cx,cy); c.rotate(t*sp); c.setLineDash(dash.map(x=>x*D)); c.beginPath(); c.arc(0,0,R*k,0,Math.PI*2); c.stroke(); c.restore(); }
  c.setLineDash([]); c.fillStyle=`rgba(255,200,230,${.7*a})`; for(let i=0;i<16;i++){ const an=i/16*Math.PI*2-t*.2; c.beginPath(); c.arc(cx+Math.cos(an)*R*1.27,cy+Math.sin(an)*R*1.27,1.8*D,0,Math.PI*2); c.fill(); } c.restore(); }
// 수녀(키아라) 그림자: 단위 좌표(키 1, 위 가운데가 0,0)
const BXN=[[[-.075,.07],[-.06,.01],[0,-.025],[.06,.01],[.075,.07],[.13,.2],[.2,.36],[.12,.34],[.08,.2],[-.08,.2],[-.12,.34],[-.2,.36],[-.13,.2]],   // 베일
  [[-.09,.17],[-.17,.5],[-.25,.98],[.25,.98],[.17,.5],[.09,.17]],                                                     // 수도복
  [[-.08,.2],[-.16,.3],[-.11,.4],[-.02,.36],[-.04,.3]], [[.08,.2],[.16,.3],[.11,.4],[.02,.36],[.04,.3]]];               // 모은 두 소매
BXN.forEach(q=>{ let A=0; q.forEach(([x1,y1],i)=>{ const [x2,y2]=q[(i+1)%q.length]; A+=x1*y2-x2*y1; }); if(A<0) q.reverse(); });
// 비스트 그림자: 베일이 벗겨지고 머리칼이 크게 퍼진다 · 머리 양옆으로 휜 뿔 · 두 팔은 안아 들이듯 벌린다 · 옷자락 끝은 꽃잎처럼 갈라진다 (오른쪽 반만 적고 접어 만든다)
const BXB=(()=>{ const mir=h=>[...h,...h.slice(1,-1).reverse().map(([x,y])=>[-x,y])], neg=q=>q.map(([x,y])=>[-x,y]);
  const hair=mir([[0,-.012],[.055,0],[.09,.06],[.11,.15],[.13,.27],[.18,.4],[.26,.52],[.35,.64],[.28,.62],[.31,.74],[.23,.685],[.23,.8],[.155,.69],[.1,.45],[0,.3]]);
  const horn=[[.03,.03],[.08,-.002],[.15,-.035],[.205,-.09],[.225,-.175],[.248,-.1],[.228,-.035],[.16,.018],[.07,.062]];
  const body=mir([[0,.14],[.05,.155],[.07,.22],[.06,.32],[.09,.45],[.15,.62],[.22,.78],[.31,.9],[.24,.88],[.22,.975],[.15,.9],[.11,.995],[.06,.935],[0,1]]);
  const arm=[[.045,.16],[.14,.215],[.26,.245],[.37,.235],[.43,.205],[.455,.19],[.44,.225],[.465,.23],[.425,.255],[.38,.285],[.27,.3],[.14,.29],[.06,.25]];
  return [hair,horn,neg(horn),body,arm,neg(arm)]; })();
for(const L of [BXN,BXB]) L.forEach(q=>{ let A=0; q.forEach(([x1,y1],i)=>{ const [x2,y2]=q[(i+1)%q.length]; A+=x1*y2-x2*y1; }); if(A<0) q.reverse(); });
function bxSilP(L,cx,top,h,hr){ const P=new Path2D(); for(const q of L){ q.forEach(([u,v],i)=>{ const x=cx+u*h, y=top+v*h; i?P.lineTo(x,y):P.moveTo(x,y); }); P.closePath(); }
  P.moveTo(cx+hr*h,top+.08*h); P.arc(cx,top+.08*h,hr*h,0,Math.PI*2); return P; }
function bxSil(c,L,cx,top,h,a,rim,D,col){ if(a<=0) return; const P=bxSilP(L,cx,top,h,L===BXB?.055:.06);
  c.save(); c.fillStyle=col||`rgba(14,5,18,${.95*a})`; if(!col){ c.shadowColor=`rgba(${rim||BXF.pink},${.9*a})`; c.shadowBlur=(L===BXB?26:18)*D; } c.fill(P); c.restore(); }
function bxNun(c,cx,top,h,a,rim,D){ bxSil(c,BXN,cx,top,h,a,rim,D); }
// 그림자가 바뀌는 순간: 가로 띠마다 옛 모습과 새 모습이 뒤섞이고 어긋나며, 색이 갈라진다 (k: 새 모습 쪽으로 넘어간 정도)
function bxSilSwap(c,cx,top,h,a,k,D){ const n=14, y0=top-.16*h, hh=1.2*h/n;
  for(let i=0;i<n;i++){ const y=y0+i*hh, B=Math.random()<k, dx=(Math.random()<.45?(Math.random()-.5)*.12*h:0);
    c.save(); c.beginPath(); c.rect(0,y,c.canvas.width,hh+1); c.clip(); c.translate(dx,0);
    if(Math.random()<.5){ bxSil(c,B?BXB:BXN,cx-5*D,top,h,a,null,D,`rgba(255,60,200,${.45*a})`); bxSil(c,B?BXB:BXN,cx+5*D,top,h,a,null,D,`rgba(80,220,255,${.4*a})`); }
    bxSil(c,B?BXB:BXN,cx,top,h,a,BXF.pink,D); c.restore(); } }
// 화면 잡음(가로채기와 같은 결): 낮은 해상도 잡음을 늘려 덮고 굵은 띠 몇 줄
function bxStatic(c,W,H,D,I,t){ if(I<=0) return; const nw=160, nh=90; if(!bxStatic.cv){ bxStatic.cv=document.createElement('canvas'); bxStatic.cv.width=nw; bxStatic.cv.height=nh; }
  const x=bxStatic.cv.getContext('2d'), d=x.createImageData(nw,nh), A=d.data; for(let i=0;i<A.length;i+=4){ const v=Math.random()*255; A[i]=v; A[i+1]=v*.9; A[i+2]=v; A[i+3]=255; } x.putImageData(d,0,0);
  c.save(); c.imageSmoothingEnabled=false; c.globalAlpha=.45*I; c.drawImage(bxStatic.cv,0,0,W,H); c.globalAlpha=1;
  for(let k=0;k<2+Math.floor(5*I);k++){ const y=Math.random()*H, hh=(2+Math.random()*22*I)*D; c.fillStyle=Math.random()<.5?`rgba(255,255,255,${.25*I})`:`rgba(0,0,0,${.6*I})`; c.fillRect(0,y,W,hh); } c.restore(); }

/* 7일차 봉인: 달빛이 내려와 성배를 상자째 가둔다 · 잠그기 직전 성배가 한 번 일렁이고 분홍 실오라기가 빠져나간다 (복선). BB가 없는 생은 성배가 사라지고 빈 자리만 남는다 */
function bxSealShow(fx){
  const {seg,io,oc}=XF, nb=!!fx.nb, T=nb?6.3:6.7;
  const title=tr(nb?`제${fx.d}일 · 빈 자리`:`제${fx.d}일 · 봉인`), sub=tr(nb?'성배가 있던 자리가 텅 비어 있었다':'누군가 성배를 통째로 봉인했다');
  const V=xfxOpen('dsc bxs',`${title} · ${sub}`,`<div class="xd-txt"><div class="xd-d${[...title].length>8?' long':''}">${[...title].map(ch=>`<span>${ch===' '?'&nbsp;':esc(ch)}</span>`).join('')}</div><div class="xd-rule bx"></div><div class="xd-s">${esc(sub)}</div></div>`,T,frame);
  fxSnd(V.o,nb?'j_bx_empty':'j_bx_seal');
  const chars=[...V.o.querySelectorAll('.xd-d span')], rule=V.o.querySelector('.xd-rule'), subEl=V.o.querySelector('.xd-s'), TA=nb?2.4:2.8, TO=T-.8;
  const EDG=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
  let dust=null;
  function text(t){ const gap=Math.min(.07,1.1/Math.max(1,chars.length));
    chars.forEach((el,i)=>{ const k=seg(t,TA+i*gap,TA+i*gap+.5), out=seg(t,TO,TO+.7), o=oc(k)*(1-out); el.style.opacity=o.toFixed(3); el.style.filter=`blur(${((1-k)*8+out*5).toFixed(2)}px)`; });
    const r=oc(seg(t,TA+.4,TA+1))*(1-seg(t,TO,TO+.7)); rule.style.width=(r*Math.min(260,innerWidth*.6))+'px'; rule.style.opacity=r;
    const s=oc(seg(t,TA+.55,TA+1.1))*(1-seg(t,TO,TO+.7)); subEl.style.opacity=s; }
  function frame(t,dt){ const {c,W,H,D}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, base=H*.6, out=io(seg(t,T-.7,T));
    const dark=io(seg(t,0,.4))*(1-out); c.fillStyle=`rgba(7,3,12,${.88*dark})`; c.fillRect(0,0,W,H);
    const mx=cx, my=H*.16, mr=Math.min(W,H)*.075;
    if(!nb){ bxMoon(c,mx,my,mr,oc(seg(t,.2,.9))*(1-out),D);
      const beam=seg(t,.9,1.4)*(1-seg(t,2.6,3.4))*(1-out); if(beam>0){ const g=c.createLinearGradient(0,my,0,base); g.addColorStop(0,`rgba(${BXF.vio},${.35*beam})`); g.addColorStop(1,`rgba(${BXF.vio},${.08*beam})`); c.fillStyle=g;
        c.beginPath(); c.moveTo(mx-mr*.7,my); c.lineTo(mx+mr*.7,my); c.lineTo(cx+110*s,base); c.lineTo(cx-110*s,base); c.closePath(); c.fill(); } }
    // 잔: 일렁임(2.2~2.5초) · 빈 자리면 흩어진다
    const wob=Math.exp(-Math.pow((t-2.35)/.12,2)), cupA=oc(seg(t,.2,.8))*(nb?1-io(seg(t,1.4,2.4)):1)*(1-out), jx=Math.sin(t*80)*6*D*wob;
    bxGlow(c,cx,base-110*s,170*s,BXF.gold,.35*cupA*(1-(nb?0:.6*seg(t,2.6,3)))); bxCupDraw(c,cx+jx,base,s,cupA,D,wob>.2?BXF.pink:null);
    // 분홍 실오라기: 잔의 입구에서 한 줄기 빠져나간다
    const wk=seg(t,nb?1.0:2.25,nb?2.0:3.1); if(wk>0&&wk<1){ c.save(); c.strokeStyle=`rgba(${BXF.pink},${.8*(1-wk)})`; c.lineWidth=1.6*D; c.shadowColor=`rgba(${BXF.pk2},1)`; c.shadowBlur=10*D; c.beginPath(); const y0=base-160*s;
      for(let i=0;i<=30;i++){ const u=i/30*wk; const x=cx+Math.sin(u*9+t*3)*20*s*u+u*W*.35, y=y0-u*H*.35; i?c.lineTo(x,y):c.moveTo(x,y); } c.stroke(); c.restore(); }
    if(nb){ if(!dust&&t>1.4){ const r=XF.rng(7); dust=[...Array(60)].map(()=>({x:cx+(r()-.5)*120*s,y:base-r()*160*s,vx:(r()-.5)*40*D,vy:-(20+r()*60)*D,l:1+r()})); }
      if(dust) for(const p of dust){ p.x+=p.vx*dt; p.y+=p.vy*dt; p.l-=dt*.6; if(p.l<=0) continue; c.fillStyle=`rgba(${BXF.gold},${.7*Math.min(1,p.l)*(1-out)})`; c.fillRect(p.x,p.y,2*D,2*D); }
      const ring=seg(t,2.0,2.6)*(1-out); c.strokeStyle=`rgba(200,180,220,${.45*ring})`; c.lineWidth=1.2*D; c.beginPath(); c.ellipse(cx,base,90*s,14*s,0,0,Math.PI*2); c.stroke(); }
    else { // 상자: 모서리 12줄이 하나씩 그어지고, 2.6초에 면이 채워지며 잠긴다
      const R=150*s, cy=base-80*s, rot=t*.25+.6, P=[]; for(const [a,b,cc] of [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]]){ const x=a*Math.cos(rot)-cc*Math.sin(rot), z=a*Math.sin(rot)+cc*Math.cos(rot), y=b*Math.cos(.35)-z*Math.sin(.35), zz=b*Math.sin(.35)+z*Math.cos(.35), k=1+zz*.12; P.push([cx+x*R*.75*k,cy+y*R*.75*k]); }
      const lock=seg(t,2.6,2.75), shut=1-.12*io(seg(t,2.6,3.0)), la=(1-out);
      c.save(); c.translate(cx,cy); c.scale(shut,shut); c.translate(-cx,-cy); c.lineCap='round';
      EDG.forEach(([a,b],i)=>{ const k=seg(t,1.1+i*.1,1.25+i*.1); if(k<=0) return; const [x1,y1]=P[a], [x2,y2]=P[b]; c.strokeStyle=`rgba(${BXF.vio},${.85*la})`; c.lineWidth=(1.4+lock*1.2)*D; c.shadowColor=`rgba(${BXF.vio},1)`; c.shadowBlur=12*D;
        c.beginPath(); c.moveTo(x1,y1); c.lineTo(x1+(x2-x1)*k,y1+(y2-y1)*k); c.stroke(); });
      if(lock>0){ c.shadowBlur=0; for(const f of [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]){ c.beginPath(); f.forEach((i,j)=>j?c.lineTo(P[i][0],P[i][1]):c.moveTo(P[i][0],P[i][1])); c.closePath(); c.fillStyle=`rgba(150,100,230,${.09*lock*la})`; c.fill();
        // 면마다 가는 격자
        c.strokeStyle=`rgba(${BXF.vio},${.25*lock*la})`; c.lineWidth=.8*D; for(let g=1;g<3;g++){ const u=g/3, A=P[f[0]],B=P[f[1]],C=P[f[2]],E=P[f[3]]; c.beginPath(); c.moveTo(A[0]+(B[0]-A[0])*u,A[1]+(B[1]-A[1])*u); c.lineTo(E[0]+(C[0]-E[0])*u,E[1]+(C[1]-E[1])*u); c.moveTo(A[0]+(E[0]-A[0])*u,A[1]+(E[1]-A[1])*u); c.lineTo(B[0]+(C[0]-B[0])*u,B[1]+(C[1]-B[1])*u); c.stroke(); } } }
      c.restore();
      const fl=Math.exp(-Math.pow((t-2.65)/.08,2)); if(fl>.01){ c.fillStyle=`rgba(235,215,255,${.55*fl})`; c.fillRect(0,0,W,H); } }
    text(t); }
}

/* 강림: 수녀가 성배를 마시고, 연꽃이 피며 이름이 「킷쇼인 → 셋쇼인」으로 고쳐 쓰인다. 호위가 될 센티넬이 빨려 든다. 고쳐쓴 카르마면 마지막에 화면이 치직이며 덮어쓰인다 */
function bxDescShow(fx){
  const pre=typeof bxDarkAt!=='undefined'&&performance.now()-bxDarkAt<1500?(bxDarkV==='unseal'?'u':'p'):''; if(pre) bxDarkAt=0;
  const {seg,io,oc}=XF, K=!!fx.karma, T=K?9.6:7.8, KA=6.7, rnd=XF.rng(23), NG=Math.max(0,Math.min(5,fx.g|0));
  const n0=tr('킷쇼인 키아라'), n1=tr('셋쇼인 키아라'), day=tr(`제${fx.d}일 · 강림`), cls=tr('비스트 Ⅲ/R'), km=tr('고쳐쓴 카르마');
  const html=`<div class="bxd"><div class="bxd-day">${esc(day)}</div><div class="bxd-nm"><span class="a">${esc(n0)}</span><span class="b">${esc(n1)}</span></div><div class="bxd-cls">${esc(cls)}</div>${K?`<div class="bxd-km">${esc(km)}</div>`:''}</div>`;
  const V=xfxOpen('bxdx',`${day} · ${n1} · ${cls}${K?' · '+km:''}`,html,T,frame);
  fxSnd(V.o,'j_bx_desc'); if(K) fxSnd(V.o,'j_bx_karma',{at:KA});
  const q=k=>V.o.querySelector(k), E={day:q('.bxd-day'),a:q('.bxd-nm .a'),b:q('.bxd-nm .b'),cls:q('.bxd-cls'),km:q('.bxd-km')};
  const PET=[...Array(40)].map(()=>({x:rnd(),y:rnd(),v:.04+rnd()*.08,r:rnd()*6,s:3+rnd()*5,w:rnd()*6}));
  const ORB=[...Array(NG)].map((_,i)=>({a0:rnd()*6.28,d:i*.18}));
  if(pre) frame(0,0); // 앞 연출에서 넘어올 때: 첫 화면을 바로 그려 한 프레임 비는 틈을 없앤다
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, out=io(seg(t,T-.8,T));
    const dark=(pre?1:io(seg(t,0,.4)))*(1-out); c.fillStyle=`rgba(10,3,10,${.9*dark})`; c.fillRect(0,0,W,H);
    const nh=Math.min(290*s,H*.5), ntop=H*.12, cyc=ntop+nh*.45;
    if(pre&&pre!=='u'){ const k=1-io(seg(t,0,1.4)); if(k>0) bxGlow(c,cx,H*.4,300*s,BXF.pk2,.16*k); } // 앞 연출에서 남은 분홍 빛을 이어받아 잦아들게 한다
    // 연꽃 · 만다라 (2.6초부터 핀다)
    const bl=oc(seg(t,2.55,3.6)), la=bl*(1-out), sc=seg(t,K?KA+.3:99,K?KA+1.3:99);
    bxGlow(c,cx,cyc,nh*1.2,BXF.pk2,.35*la); bxMandala(c,cx,cyc,nh*.62,t,la,D); bxLotus(c,cx,cyc,nh*.6,bl,t*.05,la,D,false);
    if(sc>0){ // 고쳐쓴 카르마: 위에서 아래로 훑는 줄이 지나간 자리는 빛을 잃는다
      const yy=(cyc-nh*.8)+nh*1.6*sc; c.save(); c.beginPath(); c.rect(0,0,W,yy); c.clip(); c.fillStyle=`rgba(20,10,30,${.55*la})`; c.fillRect(0,0,W,H); bxLotus(c,cx,cyc,nh*.6,bl,t*.05,.6*la,D,true); c.restore();
      c.fillStyle=`rgba(${BXF.vio},${.9*(1-out)})`; c.fillRect(0,yy-1*D,W,2*D); }
    const up=io(seg(t,1.2,2.0)), drink=seg(t,2.0,2.5), cupA=oc(seg(t,.2,.7))*(1-io(seg(t,2.3,2.7)));
    // 수녀
    const na=oc(seg(t,.5,1.3))*(1-out), swS=seg(t,4.2,4.6);
    if(swS<=0) bxNun(c,cx,ntop,nh,na,drink>0||t>2.5?BXF.pink:'120,90,140',D);
    else if(swS<1) bxSilSwap(c,cx,ntop,nh,na,io(swS),D);
    else { const k=seg(t,4.6,5.2); bxGlow(c,cx,ntop+nh*.35,nh*.7,BXF.pk2,.3*(1-k)*na); bxSil(c,BXB,cx,ntop,nh,na,BXF.pink,D); }
    // 성배: 수녀 앞에 떠 있다가 입가로 올라가고, 빛이 수녀에게 흘러든다(1.3~2.5초)
    const cb=H*.7-(H*.7-(ntop+nh*.3))*up, cs=s*.62*(1-.4*up);
    bxGlow(c,cx,cb-110*cs,150*cs,BXF.gold,.4*cupA); bxCupDraw(c,cx,cb,cs,cupA*(1-out),D,drink>0?BXF.pink:null);
    if(drink>0&&drink<1){ bxGlow(c,cx,ntop+nh*.1,nh*.4,BXF.pink,.6*Math.sin(Math.PI*drink)); }
    // 센티넬(호위): 화면 끝에서 빛 덩이로 빨려 와 둘레를 돈다
    for(const o of ORB){ const k=io(seg(t,3.0+o.d,3.9+o.d)); if(k<=0) continue; const ang=o.a0+t*.8, r0=Math.max(W,H)*.7, r=r0+(nh*.75-r0)*k, x=cx+Math.cos(ang)*r, y=cyc+Math.sin(ang)*r*.55;
      bxGlow(c,x,y,22*D,BXF.pk2,.9*(1-out)); c.fillStyle=`rgba(255,230,245,${.9*(1-out)})`; c.beginPath(); c.arc(x,y,3*D,0,Math.PI*2); c.fill(); }
    // 꽃잎이 흩날린다
    const pa=seg(t,2.7,3.4)*(1-out); if(pa>0) for(const p of PET){ const y=((p.y+t*p.v)%1.2-.1)*H, x=p.x*W+Math.sin(t*1.2+p.w)*24*D; c.save(); c.translate(x,y); c.rotate(p.r+t); c.fillStyle=`rgba(${BXF.pink},${.55*pa})`; c.beginPath(); c.ellipse(0,0,p.s*D,p.s*.5*D,0,0,Math.PI*2); c.fill(); c.restore(); }
    const fl=Math.exp(-Math.pow((t-2.6)/.09,2)); if(fl>.01){ c.fillStyle=`rgba(255,210,235,${.5*fl})`; c.fillRect(0,0,W,H); }
    const sh=Math.max(0,1-Math.abs(t-2.62)/.25,(1-Math.abs(t-4.4)/.2)*.7); if(G) G.style.transform=sh>0?`translate(${(Math.sin(t*90)*4*sh).toFixed(1)}px,0)`:'';
    const swI=Math.max(0,1-Math.abs(t-4.4)/.22); if(swI>0) bxStatic(c,W,H,D,swI*.55*(Math.random()<.4?.35:1),t);
    if(K){ const I=seg(t,KA,KA+.15)*(1-seg(t,KA+1.0,KA+1.5))*(Math.random()<.35?.4:.85); bxStatic(c,W,H,D,I*(1-out),t); }
    // 글자: 날짜 → 「킷쇼인 키아라」 → 첫 글자가 깨지며 「셋쇼인 키아라」 → 비스트 Ⅲ/R
    const tout=1-io(seg(t,T-1.0,T-.3));
    E.day.style.opacity=oc(seg(t,2.9,3.3))*tout;
    const aIn=oc(seg(t,3.1,3.6)), sw=seg(t,4.25,4.55), gl=sw>0&&sw<1;
    E.a.style.opacity=(aIn*(1-sw))*tout; E.b.style.opacity=sw*tout;
    const jx=gl?((Math.random()-.5)*14).toFixed(1):0; E.a.style.transform=`translateX(${jx}px)`; E.b.style.transform=`translateX(${gl?-jx:0}px)`;
    E.a.style.filter=gl?`drop-shadow(-4px 0 rgba(255,60,200,.9)) drop-shadow(4px 0 rgba(80,220,255,.9))`:''; E.b.style.filter=gl?`drop-shadow(4px 0 rgba(255,60,200,.9))`:'';
    if(gl&&Math.random()<.5){ c.fillStyle='rgba(255,170,215,.35)'; const r=E.a.getBoundingClientRect(); c.fillRect(r.left*D,(r.top+Math.random()*r.height)*D,r.width*D,(2+Math.random()*5)*D); }
    E.cls.style.opacity=oc(seg(t,4.6,5.0))*tout;
    if(E.km){ const k=oc(seg(t,KA+.7,KA+1.1)); E.km.style.opacity=k*tout; E.km.style.clipPath=`inset(0 ${(100-100*seg(t,KA+.7,KA+1.2)).toFixed(1)}% 0 0)`; } }
}

/* 키아라 입장: 분홍 안개가 스며들고 연꽃 만다라가 열려 이름이 새겨진다. 끝에서 연꽃이 꽃잎으로 흩어진다 (처음 · 최후의 밤 6.6초, 다시 2.5초) */
function bxBossShow(fx){
  const {seg,io,oc}=XF, rnd=XF.rng(29), full=!!fx.full, rep=!!fx.reply, X=(full?(rep?1.0:0):(rep||fx.line?1.4:0))+(full?1.4:.7), T=(full?5.2:1.8)+X;
  const comp=fx.comp||[];
  const html=`<div class="xb-card bx">${fx.final?`<div class="xb-night">${esc(tr('최후의 밤'))}</div>`:''}<div class="xb-nm">${esc(tr('비스트 Ⅲ/R'))}</div><div class="xb-tn">${esc(tr(fx.name||'정체 불명'))}</div>${fx.line?`<div class="xb-q">“${esc(tr(fx.line))}”</div>`:''}${rep?`<div class="xb-r"><small>${esc(tr(fx.replyName||''))}</small>“${esc(tr(fx.reply))}”</div>`:''}
    <div class="xb-cp"><small>${comp.length?esc(tr('함께 싸우는 조')):''}</small>${comp.length?comp.map(n=>`<span>${esc(tr(n))}</span>`).join(''):`<span>${esc(tr('홀로'))}</span>`}</div></div>`;
  const V=xfxOpen('bfx bxb',[fx.final?tr('최후의 밤'):'',tr('비스트 Ⅲ/R'),tr(fx.name||'정체 불명'),fx.line?tr(fx.line):'',rep?`${tr(fx.replyName||'')}: ${tr(fx.reply)}`:''].filter(Boolean).join(' · '),html,T,frame);
  const brk=(full?4.55:1.4)+X; fxSnd(V.o,full?'j_bx_in':'j_bx_in_s'); fxSnd(V.o,full?'j_bx_brk':'j_bx_brk_s',{at:brk});
  const q=k=>V.o.querySelector(k), E={night:q('.xb-night'),nm:q('.xb-nm'),tn:q('.xb-tn'),q:q('.xb-q'),r:q('.xb-r'),cp:q('.xb-cp'),card:q('.xb-card')};
  const cpItems=[...E.cp.querySelectorAll('span')], cpLab=E.cp.querySelector('small');
  const HZ=[...Array(5)].map(()=>({x:rnd(),y:rnd(),r:.25+rnd()*.3,p:rnd()*6}));
  let pet=null;
  function card(t,a,compAt,outA,outB){ const o=1-io(seg(t,outA,outB));
    if(E.night) E.night.style.opacity=oc(seg(t,a-.15,a+.25))*o;
    const w=oc(seg(t,a,a+.55)); E.nm.style.clipPath=`inset(0 ${(100-w*100).toFixed(1)}% 0 0)`; E.nm.style.filter=`blur(${((1-w)*3).toFixed(1)}px)`; E.nm.style.opacity=o;
    const tn=oc(seg(t,a+.35,a+.75)); E.tn.style.opacity=tn*o; E.tn.style.transform=`translateY(${((1-tn)*6).toFixed(1)}px)`;
    if(E.q) E.q.style.opacity=oc(seg(t,a+.6,a+1.0))*o;
    if(E.r){ const ra=a+(full?1.3:.9), k=oc(seg(t,ra,ra+.45)); E.r.style.opacity=k*o; E.r.style.transform=`translateY(${((1-k)*6).toFixed(1)}px)`; }
    cpLab.style.opacity=oc(seg(t,compAt-.1,compAt+.2))*o;
    cpItems.forEach((el,i)=>{ const k=oc(seg(t,compAt+i*.14,compAt+i*.14+.3)); el.style.opacity=k*o; el.style.transform=`translateY(${((1-k)*14).toFixed(1)}px)`; }); }
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H);
    const r=E.nm.getBoundingClientRect(), R=Math.min(W,H,800*D)*(full?.3:.26), cx=W/2, cy=(r.top+r.height/2)*D-R*.27, out=full?io(seg(t,4.6+X,5.2+X)):io(seg(t,1.45+X,1.8+X));
    if(full&&G){ const g=.5*seg(t,0,.35)*(1-out); G.style.filter=`saturate(${(1-g).toFixed(2)}) brightness(${(1-.3*seg(t,0,.35)*(1-out)).toFixed(2)})`; }
    c.fillStyle=`rgba(14,4,12,${(full?.8*seg(t,0,.35):.72*seg(t,0,.15))*(1-out)})`; c.fillRect(0,0,W,H);
    // 분홍 안개
    const hz=(full?oc(seg(t,.1,1.0)):oc(seg(t,0,.35))*.7)*(1-out); for(const h of HZ) bxGlow(c,(h.x*.8+.1)*W+Math.sin(t*.6+h.p)*30*D,(h.y*.8+.1)*H,Math.max(W,H)*h.r,BXF.pk2,.22*hz);
    { const cr=E.card.getBoundingClientRect(), ca=(full?seg(t,1.1,1.5):seg(t,0,.15))*(1-out), my=(cr.top+cr.height/2)*D, rh=Math.max(cr.height*.75*D,R); const vg=c.createRadialGradient(cx,my,0,cx,my,Math.max(W*.6,rh)); vg.addColorStop(0,`rgba(12,3,10,${.7*ca})`); vg.addColorStop(.6,`rgba(12,3,10,${.4*ca})`); vg.addColorStop(1,'rgba(12,3,10,0)'); c.fillStyle=vg; c.fillRect(0,0,W,H); }
    if(t<brk){ const open=full?oc(seg(t,.6,1.5)):oc(seg(t,0,.35)), a=(full?seg(t,.5,.8):seg(t,0,.12))*(1-out); bxMandala(c,cx,cy,R*.8*(.4+.6*open),t,a,D); bxLotus(c,cx,cy,R*.75,open,t*.08,a*.8,D,false); }
    else if(!pet){ const r2=XF.rng(31); pet=[]; for(let i=0;i<80;i++){ const an=r2()*Math.PI*2, v=(160+r2()*420)*D; pet.push({x:cx+Math.cos(an)*R*.6,y:cy+Math.sin(an)*R*.6,vx:Math.cos(an)*v,vy:Math.sin(an)*v-80*D,r:r2()*6,s:(3+r2()*5)*D}); } }
    if(pet) for(const p of pet){ p.vy+=260*D*dt; p.vx*=.99; p.x+=p.vx*dt; p.y+=p.vy*dt; p.r+=dt*4; c.save(); c.translate(p.x,p.y); c.rotate(p.r); c.fillStyle=`rgba(${BXF.pink},${.8*(1-out)})`; c.beginPath(); c.ellipse(0,0,p.s,p.s*.5,0,0,Math.PI*2); c.fill(); c.restore(); }
    if(full) card(t,1.3,2.05+(rep?.6:0),4.6+X,5.05+X); else card(t,.12,.45+(rep?.9:fx.line?.5:0),1.45+X,1.7+X); }
}

/* 단독현현: 분홍으로 번쩍이고 몸이 녹아내렸다 다시 빚어진다. 체력 막대 위로 꽃잎이 차오른다 (4.0초) */
function bxP2Show(fx){
  const {seg,io,oc}=XF, rnd=XF.rng(41);
  const head=tr('단독현현'), html=`<div class="xb-card b2 bx"><div class="xb-again">${esc(head)}</div>${fx.line?`<div class="xb-q2">“${esc(tr(fx.line))}”</div>`:''}</div>`;
  const V=xfxOpen('b2fx bxb',[head,fx.line?tr(fx.line):''].filter(Boolean).join(' · '),html,4.0,frame); fxSnd(V.o,'j_bx_p2');
  const ag=V.o.querySelector('.xb-again'), q2=V.o.querySelector('.xb-q2'), bar=$('.side.foe .hb');
  const DR=[...Array(28)].map(()=>({x:rnd(),l:.3+rnd()*.7,w:2+rnd()*5,d:rnd()*.3}));
  function frame(t){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H);
    const fl=Math.exp(-Math.pow((t-.28)/.08,2)); if(fl>.01){ c.fillStyle=`rgba(255,150,205,${.45*fl})`; c.fillRect(0,0,W,H); }
    const sh=Math.max(0,1-Math.abs(t-.3)/.2); if(G) G.style.transform=sh>0?`translate(${(Math.sin(t*90)*4*sh).toFixed(1)}px,${(Math.cos(t*70)*3*sh).toFixed(1)}px)`:'';
    // 녹아내림(0.3~1.0) → 거꾸로 다시 차오름(1.0~1.7)
    const melt=seg(t,.3,1.0), back=seg(t,1.0,1.7), k=melt*(1-back);
    if(k>0) for(const d of DR){ const L=d.l*H*.45*io(Math.max(0,(k-d.d)/(1-d.d))); if(L<=0) continue; const x=d.x*W; const g=c.createLinearGradient(0,0,0,L); g.addColorStop(0,`rgba(${BXF.pk2},.7)`); g.addColorStop(1,`rgba(${BXF.pink},0)`); c.fillStyle=g; c.fillRect(x-d.w*D/2,0,d.w*D,L); c.beginPath(); c.arc(x,L,d.w*D*.8,0,Math.PI*2); c.fillStyle=`rgba(${BXF.pink},.6)`; c.fill(); }
    const a=oc(seg(t,.35,.6))*(1-io(seg(t,3.6,4.0))); ag.style.opacity=a; ag.style.filter=`blur(${((1-a)*4).toFixed(1)}px)`; if(q2) q2.style.opacity=oc(seg(t,.75,1.1))*(1-io(seg(t,3.6,4.0)));
    c.fillStyle=`rgba(14,4,12,${.45*a})`; c.fillRect(0,0,W,H);
    const ra=ag.getBoundingClientRect(), rq=(q2||ag).getBoundingClientRect(), y0=(ra.top+rq.bottom)/2*D, bh=((rq.bottom-ra.top)/2+28)*D;
    const g=c.createLinearGradient(0,y0-bh,0,y0+bh); g.addColorStop(0,'rgba(12,3,10,0)'); g.addColorStop(.3,`rgba(12,3,10,${.85*a})`); g.addColorStop(.7,`rgba(12,3,10,${.85*a})`); g.addColorStop(1,'rgba(12,3,10,0)'); c.fillStyle=g; c.fillRect(0,y0-bh,W,bh*2);
    bxLotus(c,W/2,y0,bh*1.3,oc(seg(t,1.0,1.7)),t*.1,.35*a,D,false);
    c.fillStyle=`rgba(${BXF.pink},${.5*a})`; c.fillRect(W*.2,y0-bh+12*D,W*.6,1*D); c.fillRect(W*.2,y0+bh-12*D,W*.6,1*D);
    if(bar&&t>.4){ const r=bar.getBoundingClientRect(); if(r.width>0&&r.bottom>0&&r.top<innerHeight){ const fill=io(seg(t,1.0,1.7)), gl2=1-io(seg(t,3.6,4.0)), bx=r.left*D, by=r.top*D, bw=r.width*D*.3*fill, bhh=Math.max(4,r.height)*D;
      if(bw>0){ c.save(); c.shadowColor=`rgba(${BXF.pk2},${.9*gl2})`; c.shadowBlur=16*D; const lg=c.createLinearGradient(bx,0,bx+bw,0); lg.addColorStop(0,`rgba(120,40,90,${gl2})`); lg.addColorStop(1,`rgba(255,170,215,${gl2})`); c.fillStyle=lg; c.fillRect(bx,by,bw,bhh); c.restore(); } } } }
}
// BB 그림자(가로채는 소환과 같은 모양): 단위 좌표(키 1, 위 가운데가 0,0)
const BXBB=[[[-.08,.04],[-.13,.2],[-.17,.45],[-.19,.68],[-.12,.62],[-.08,.3],[.08,.3],[.12,.62],[.19,.68],[.17,.45],[.13,.2],[.08,.04]],
  [[-.1,.19],[-.2,.5],[-.26,.82],[-.07,.78],[-.05,.35]],[[.1,.19],[.2,.5],[.26,.82],[.07,.78],[.05,.35]],[[-.06,.19],[.06,.19],[.09,.48],[.12,.58],[-.12,.58],[-.09,.48]],
  [[-.085,.58],[-.035,.58],[-.04,.97],[-.075,.97]],[[.035,.58],[.085,.58],[.075,.97],[.04,.97]],[[-.1,.2],[-.2,.36],[-.12,.46],[-.02,.42],[-.05,.32]],[[.1,.2],[.2,.36],[.12,.46],[.02,.42],[.05,.32]],
  [[.03,.02],[.16,-.05],[.15,.06]],[[.03,.04],[.11,.13],[.02,.11]]];
BXBB.forEach(q=>{ let A=0; q.forEach(([x1,y1],i)=>{ const [x2,y2]=q[(i+1)%q.length]; A+=x1*y2-x2*y1; }); if(A<0) q.reverse(); });
function bxBBSil(c,cx,top,h,a,D){ if(a<=0) return; const P=new Path2D(); for(const q of BXBB){ q.forEach(([u,v],i)=>{ const x=cx+u*h, y=top+v*h; i?P.lineTo(x,y):P.moveTo(x,y); }); P.closePath(); }
  P.moveTo(cx+.07*h,top+.085*h); P.arc(cx,top+.085*h,.07*h,0,Math.PI*2);
  c.save(); c.fillStyle=`rgba(30,12,48,${.92*a})`; c.shadowColor=`rgba(${BXF.vio},${a})`; c.shadowBlur=18*D; c.fill(P); c.restore(); }
