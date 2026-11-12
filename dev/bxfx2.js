/* ---- 비스트 Ⅲ/R 연출 2차 (11-12): ⑦ KP 회수 · ⑧ 멜트·립 해방 · ⑨ 봉인이 갈라짐(고백 · 찢어짐 · 풀기) · ⑩ 토벌령 · ⑪ 키아라와의 보구 격돌 ---- */
function bxKpFx(fx){ xfxGo('j_bx_kp',()=>bxKpShow(fx)); }
function bxFreeFx(fx){ xfxGo('j_bx_free',()=>bxFreeShow(fx)); }
function bxConfFx(fx){ const k=fx.v==='force'?'j_bx_tear':fx.v==='unseal'?'j_bx_open':'j_bx_conf'; xfxGo(k,()=>bxConfShow(fx)); }
function bxOrderFx(fx){ xfxGo('j_bx_order',()=>bxOrderShow(fx)); }
// 제목 · 줄 · 부제 (봉인 연출과 같은 결)
function bxTxtH(title,sub,extra){ return `<div class="xd-txt"><div class="xd-d${[...title].length>8?' long':''}">${[...title].map(ch=>`<span>${ch===' '?'&nbsp;':esc(ch)}</span>`).join('')}</div><div class="xd-rule bx"></div><div class="xd-s">${esc(sub)}</div>${extra||''}</div>`; }
function bxTxtF(V,TA,TO){ const {seg,oc}=XF, chars=[...V.o.querySelectorAll('.xd-d span')], rule=V.o.querySelector('.xd-rule'), subEl=V.o.querySelector('.xd-s');
  return t=>{ const gap=Math.min(.07,1.1/Math.max(1,chars.length)), out=seg(t,TO,TO+.7);
    chars.forEach((el,i)=>{ const k=seg(t,TA+i*gap,TA+i*gap+.5), o=oc(k)*(1-out); el.style.opacity=o.toFixed(3); el.style.filter=`blur(${((1-k)*8+out*5).toFixed(2)}px)`; });
    const r=oc(seg(t,TA+.4,TA+1))*(1-out); rule.style.width=(r*Math.min(260,innerWidth*.6))+'px'; rule.style.opacity=r;
    const s=oc(seg(t,TA+.55,TA+1.1))*(1-out); subEl.style.opacity=s; return s; }; }
// 봉인 상자(7일차 봉인과 같은 모양)
const BXC_E=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]], BXC_F=[[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]];
function bxCubeP(cx,cy,R,rot){ const P=[]; for(const [a,b,cc] of [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]]){ const x=a*Math.cos(rot)-cc*Math.sin(rot), z=a*Math.sin(rot)+cc*Math.cos(rot), y=b*Math.cos(.35)-z*Math.sin(.35), zz=b*Math.sin(.35)+z*Math.cos(.35), k=1+zz*.12; P.push([cx+x*R*.75*k,cy+y*R*.75*k]); } return P; }
function bxFacePt(P,f,u,v){ const [a,b,c,d]=BXC_F[f].map(i=>P[i]); return [(1-u)*(1-v)*a[0]+u*(1-v)*b[0]+u*v*c[0]+(1-u)*v*d[0],(1-u)*(1-v)*a[1]+u*(1-v)*b[1]+u*v*c[1]+(1-u)*v*d[1]]; }

/* ⑦ KP 회수: 쓰러진 센티넬의 가슴께에서 빛 조각이 빠져나와 손으로 내려앉고, 위에서 이쪽을 보던 눈 하나가 갈라져 닫힌다 (4.8초) */
const BXKP={Body:'255,150,190',Site:'200,150,255',Mouth:'255,140,150',Spice:'255,200,130',Organ:'235,90,140'};
function bxKpShow(fx){
  const {seg,io,oc}=XF, T=4.8, col=BXKP[fx.k]||BXF.pink, n=Math.max(0,Math.min(5,fx.n|0)), g=!!fx.g, rnd=XF.rng(41);
  const title=`KP · ${fx.k||'?'}`, sub=tr(g?'키아라의 몸이 한 번 크게 일렁였다':n<=1?'익숙하지 않은 단맛이 혀끝에 남았다':'이쪽을 보던 시선이 하나 끊겼다');
  const slots=`<div class="bxkp-sl" aria-label="${esc(tr(`카르마 파지 다섯 가운데 ${n}`))}">${[0,1,2,3,4].map(i=>`<i class="${i<n?'on':''}${i===n-1?' nw':''}"></i>`).join('')}</div>`;
  const V=xfxOpen('dsc bxs',`${title} · ${sub}`,bxTxtH(title,sub,slots),T,frame); fxSnd(V.o,'j_bx_kp');
  const text=bxTxtF(V,2.8,T-.8), sl=V.o.querySelector('.bxkp-sl'), TC=2.62;
  let SP=null, TR=[];
  const crys=(c,x,y,r,rot,a,D)=>{ if(a<=0) return; const Q=[[0,-1.4],[.6,-.3],[.45,.9],[0,1.3],[-.45,.9],[-.6,-.3]]; c.save(); c.translate(x,y); c.rotate(rot); c.globalAlpha=a;
    bxGlow(c,0,0,r*3,col,.55); c.beginPath(); Q.forEach(([u,v],i)=>i?c.lineTo(u*r,v*r):c.moveTo(u*r,v*r)); c.closePath();
    const gr=c.createLinearGradient(-r,-r,r,r); gr.addColorStop(0,'rgba(255,250,252,1)'); gr.addColorStop(.5,`rgba(${col},.95)`); gr.addColorStop(1,'rgba(90,30,70,.95)'); c.fillStyle=gr; c.fill();
    c.strokeStyle='rgba(255,240,248,.9)'; c.lineWidth=1*D; c.stroke(); c.beginPath(); c.moveTo(0,-1.4*r); c.lineTo(0,1.3*r); c.moveTo(-.6*r,-.3*r); c.lineTo(.45*r,.9*r); c.moveTo(.6*r,-.3*r); c.lineTo(-.45*r,.9*r); c.strokeStyle='rgba(255,240,248,.35)'; c.stroke(); c.restore(); };
  function eye(c,ex,ey,ew,eh,ap,lookX,a,D){ if(a<=0||ap<=0) return; c.save(); c.globalAlpha=a;
    const P=new Path2D(); P.moveTo(ex-ew,ey); P.quadraticCurveTo(ex,ey-eh*2*ap,ex+ew,ey); P.quadraticCurveTo(ex,ey+eh*2*ap,ex-ew,ey); P.closePath();
    c.fillStyle='rgba(20,6,18,.95)'; c.shadowColor=`rgba(${BXF.pk2},.9)`; c.shadowBlur=22*D; c.fill(P); c.shadowBlur=0; c.save(); c.clip(P);
    const ix=ex+lookX, ir=eh*.95, ig=c.createRadialGradient(ix,ey,ir*.1,ix,ey,ir); ig.addColorStop(0,'rgba(255,230,245,1)'); ig.addColorStop(.45,`rgba(${BXF.pk2},.95)`); ig.addColorStop(1,'rgba(80,20,60,.9)');
    c.fillStyle=ig; c.beginPath(); c.arc(ix,ey,ir,0,Math.PI*2); c.fill(); c.fillStyle='rgba(12,2,10,.95)'; c.beginPath(); c.ellipse(ix,ey,ir*.17,ir*.78,0,0,Math.PI*2); c.fill();
    c.strokeStyle='rgba(255,190,225,.35)'; c.lineWidth=1*D; for(let k=0;k<14;k++){ const an=k/14*Math.PI*2; c.beginPath(); c.moveTo(ix+Math.cos(an)*ir*.3,ey+Math.sin(an)*ir*.3); c.lineTo(ix+Math.cos(an)*ir*.9,ey+Math.sin(an)*ir*.9); c.stroke(); }
    c.restore(); c.strokeStyle=`rgba(255,170,215,.95)`; c.lineWidth=1.6*D; c.stroke(P); c.restore(); }
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, out=io(seg(t,T-.7,T));
    const dark=io(seg(t,0,.4))*(1-out); c.fillStyle=`rgba(9,3,11,${.9*dark})`; c.fillRect(0,0,W,H);
    const ex=cx, ey=H*.2, ew=150*s, eh=ew*.36, oy=H*.43, hy=H*.62;
    // 조각의 자리: 떠오름(0.5~1.1) → 머묾 → 손으로(1.8~2.45)
    const em=oc(seg(t,.5,1.1)), fly=io(seg(t,1.8,2.45)), fy=oy-26*s*em+(hy-(oy-26*s*em))*fly+Math.sin(t*3)*4*s*(1-fly), fr=26*s*(.4+.6*em)*(1-.4*fly), fa=em*(1-seg(t,2.42,2.5));
    // 눈: 0.2초부터 뜨고, 조각을 따라 눈동자가 움직이다 2.62초에 갈라진다
    const ap=io(seg(t,.2,.9)), lookX=Math.sin(t*1.7)*eh*.25*(1-em);
    const cut=seg(t,TC,TC+.7), ea=oc(seg(t,.15,.6))*(1-out);
    if(t<TC) eye(c,ex,ey,ew,eh,ap,lookX,ea,D);
    else { const d=io(cut)*26*s, a=ea*(1-cut); for(const [sg,dy] of [[-1,-d],[1,d]]){ c.save(); c.beginPath(); c.rect(0,sg<0?0:ey,W,sg<0?ey:H-ey); c.clip(); c.translate((Math.random()-.5)*6*D*(1-cut),dy); eye(c,ex,ey,ew,eh,ap,lookX,a,D); c.restore(); } }
    const sl_=Math.exp(-Math.pow((t-TC-.03)/.05,2)); if(sl_>.01){ c.save(); c.fillStyle=`rgba(255,240,250,${.95*sl_})`; c.shadowColor='rgba(255,180,220,1)'; c.shadowBlur=20*D; c.fillRect(ex-ew*1.6,ey-1.5*D,ew*3.2,3*D); c.restore(); }
    const sI=seg(t,TC,TC+.08)*(1-seg(t,TC+.15,TC+.35)); if(sI>0) bxStatic(c,W,H,D,sI*.45,t);
    // 손: 금빛 고리가 기다리다 조각을 받는다
    const ha=oc(seg(t,1.5,2.0))*(1-out), ab=seg(t,2.42,3.3); if(ha>0){ c.save(); c.strokeStyle=`rgba(${BXF.gold},${.6*ha*(1-.5*ab)})`; c.lineWidth=1.4*D; c.shadowColor=`rgba(${BXF.gold},1)`; c.shadowBlur=12*D; c.beginPath(); c.ellipse(cx,hy,52*s,13*s,0,0,Math.PI*2); c.stroke(); c.restore(); }
    if(ab>0&&ab<1){ c.save(); c.strokeStyle=`rgba(${col},${.8*(1-ab)})`; c.lineWidth=2*D; c.beginPath(); c.ellipse(cx,hy,(52+150*io(ab))*s,(13+38*io(ab))*s,0,0,Math.PI*2); c.stroke(); c.restore(); bxGlow(c,cx,hy,90*s,BXF.gold,.7*(1-ab)); }
    // 빠져나올 때 튀는 불티
    if(!SP&&t>.55){ SP=[...Array(36)].map(()=>{ const a=rnd()*Math.PI*2, v=(60+rnd()*220)*D; return {x:cx,y:oy,vx:Math.cos(a)*v,vy:Math.sin(a)*v-60*D,l:.6+rnd()*.7}; }); }
    if(SP) for(const p of SP){ p.x+=p.vx*dt; p.y+=p.vy*dt; p.vx*=.96; p.vy*=.96; p.l-=dt; if(p.l<=0) continue; c.fillStyle=`rgba(${col},${Math.min(1,p.l)*(1-out)})`; c.fillRect(p.x,p.y,2*D,2*D); }
    if(fly>0&&fly<1&&Math.random()<.9) TR.push({x:cx+(Math.random()-.5)*fr,y:fy,l:.5}); TR=TR.filter(p=>(p.l-=dt)>0);
    for(const p of TR){ c.fillStyle=`rgba(${col},${p.l*1.4})`; c.fillRect(p.x,p.y,1.6*D,1.6*D); }
    crys(c,cx,fy,fr,Math.sin(t*1.3)*.2,fa*(1-out),D);
    text(t); if(sl) sl.style.opacity=(oc(seg(t,3.4,3.9))*(1-seg(t,T-.8,T-.1))).toFixed(3); }
}

/* ⑧ 멜트릴리스 · 패션립 해방: 가시 돋은 분홍 실이 빛을 꽁꽁 묶고 있다가 하나씩 끊어지고, 빛이 제 빛깔로 피어난다 (4.4초) */
function bxFreeShow(fx){
  const {seg,io,oc}=XF, T=4.4, rnd=XF.rng(fx.h==='meltryllis'?51:52), melt=fx.h==='meltryllis', col=melt?'138,226,246':'255,172,216', col2='212,200,255';
  const HB=(Sim.H_BY||{})[fx.h], nm=(HB&&HB.name)||'', title=tr(nm), sub=tr('센티넬의 사슬이 끊어졌다');
  const V=xfxOpen('dsc bxs',`${title} · ${sub}`,bxTxtH(title,sub),T,frame); fxSnd(V.o,'j_bx_free');
  const text=bxTxtF(V,2.55,T-.8), NT=9;
  const TH=[...Array(NT)].map((_,i)=>({a:i/NT*Math.PI*2+rnd()*.4,w:rnd()*6,ts:1.25+[3,7,1,5,8,0,4,2,6][i]*.1,bk:.45+rnd()*.2,ph:rnd()*6}));
  let SP=[], SH=null;
  function thread(c,x0,y0,x1,y1,u0,u1,ph,a,D,s){ if(a<=0||u1<=u0) return; const dx=x1-x0, dy=y1-y0, L=Math.hypot(dx,dy), nx=-dy/L, ny=dx/L, N=40;
    c.beginPath(); for(let k=0;k<=N;k++){ const u=u0+(u1-u0)*k/N, wv=Math.sin(u*14+ph)*6*s*(1-u*.5); const x=x0+dx*u+nx*wv, y=y0+dy*u+ny*wv; k?c.lineTo(x,y):c.moveTo(x,y); }
    c.strokeStyle=`rgba(${BXF.pk2},${.85*a})`; c.lineWidth=1.8*D; c.shadowColor=`rgba(${BXF.pk2},1)`; c.shadowBlur=8*D; c.stroke(); c.shadowBlur=0;
    c.fillStyle=`rgba(255,160,210,${.8*a})`; for(let u=Math.ceil(u0*12)/12;u<u1;u+=1/12){ const wv=Math.sin(u*14+ph)*6*s*(1-u*.5), x=x0+dx*u+nx*wv, y=y0+dy*u+ny*wv; c.beginPath(); c.moveTo(x+nx*5*s,y+ny*5*s); c.lineTo(x+dx/L*3*s,y+dy/L*3*s); c.lineTo(x-dx/L*3*s,y-dy/L*3*s); c.closePath(); c.fill(); } }
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, cy=H*.4, out=io(seg(t,T-.7,T));
    const dark=io(seg(t,0,.4))*(1-out); c.fillStyle=`rgba(8,4,14,${.9*dark})`; c.fillRect(0,0,W,H);
    const free=seg(t,2.15,2.5), bloom=io(seg(t,2.2,3.0)), cr=30*s*(1+.5*bloom)*(1+.04*Math.sin(t*9)*(1-free));
    // 빛(묶여 흐릿 → 제 빛깔로)
    bxGlow(c,cx,cy,cr*3.4*(1+bloom),col,(.25+.55*bloom)*(1-out)); bxGlow(c,cx,cy,cr*2.2,col2,(.15+.4*bloom)*(1-out));
    c.save(); c.fillStyle=`rgba(${melt?'225,250,255':'255,235,246'},${(.35+.65*bloom)*(1-out)})`; c.shadowColor=`rgba(${col},1)`; c.shadowBlur=30*D; c.beginPath(); c.arc(cx,cy,cr*.55,0,Math.PI*2); c.fill(); c.restore();
    // 실: 0.2~0.9초에 바깥에서 감겨 들고, 1.25초부터 하나씩 끊어진다
    const R0=Math.max(W,H)*.75, R1=cr*.75;
    for(const h of TH){ const x0=cx+Math.cos(h.a)*R0, y0=cy+Math.sin(h.a)*R0, x1=cx+Math.cos(h.a)*R1, y1=cy+Math.sin(h.a)*R1, grow=io(seg(t,.2+h.w*.02,.9+h.w*.02)), a=oc(seg(t,.2,.5))*(1-out);
      const tight=1-.02*Math.sin(t*20+h.ph)*(t<h.ts?1:0);
      if(t<h.ts) thread(c,x0,y0,x1*tight+cx*(1-tight),y1*tight+cy*(1-tight),1-grow,1,h.ph,a,D,s);
      else { const k=seg(t,h.ts,h.ts+.55), e=io(k); const bx=x0+(x1-x0)*h.bk, by=y0+(y1-y0)*h.bk;
        if(!h.sp){ h.sp=1; for(let j=0;j<10;j++){ const an=rnd()*Math.PI*2, v=(80+rnd()*200)*D; SP.push({x:bx,y:by,vx:Math.cos(an)*v,vy:Math.sin(an)*v,l:.5+rnd()*.4}); } }
        // 바깥 토막은 튕겨 나가고, 안쪽 토막은 빛 쪽으로 오그라든다
        const ox=Math.cos(h.a)*e*80*s, oy=Math.sin(h.a)*e*80*s; thread(c,x0+ox,y0+oy,bx+ox,by+oy,0,1,h.ph,a*(1-k),D,s);
        thread(c,bx,by,x1,y1,0,1-.9*e,h.ph,a*(1-k),D,s); } }
    for(const p of SP){ p.x+=p.vx*dt; p.y+=p.vy*dt; p.l-=dt; if(p.l<=0) continue; c.fillStyle=`rgba(255,200,230,${Math.min(1,p.l*2)})`; c.fillRect(p.x,p.y,2*D,2*D); }
    // 피어남: 물결 셋 · 유리 조각
    for(let k=0;k<3;k++){ const r=seg(t,2.25+k*.18,3.3+k*.18); if(r<=0||r>=1) continue; c.save(); c.strokeStyle=`rgba(${k%2?col2:col},${.7*(1-r)})`; c.lineWidth=(2.2-k*.5)*D; c.beginPath(); c.ellipse(cx,cy,(cr+260*s*io(r)),(cr+260*s*io(r))*.55,0,0,Math.PI*2); c.stroke(); c.restore(); }
    if(!SH&&t>2.25){ SH=[...Array(26)].map(()=>{ const an=rnd()*Math.PI*2, v=(120+rnd()*360)*D; return {x:cx,y:cy,vx:Math.cos(an)*v,vy:Math.sin(an)*v,r:rnd()*6,vr:(rnd()-.5)*8,s:(4+rnd()*9)*s*2,l:1.1,c:rnd()<.5?col:col2}; }); }
    if(SH) for(const q of SH){ q.x+=q.vx*dt; q.y+=q.vy*dt; q.vx*=.985; q.vy*=.985; q.r+=q.vr*dt; q.l-=dt*.75; if(q.l<=0) continue; c.save(); c.translate(q.x,q.y); c.rotate(q.r); c.globalAlpha=Math.min(1,q.l)*(1-out); c.fillStyle=`rgba(${q.c},.35)`; c.strokeStyle=`rgba(${q.c},.95)`; c.lineWidth=1*D; c.fillRect(-q.s/2,-q.s/5,q.s,q.s/2.5); c.strokeRect(-q.s/2,-q.s/5,q.s,q.s/2.5); c.restore(); }
    const fl=Math.exp(-Math.pow((t-2.3)/.08,2)); if(fl>.01){ c.fillStyle=`rgba(${melt?'225,248,255':'255,232,244'},${.5*fl})`; c.fillRect(0,0,W,H); }
    text(t); }
}

/* ⑨ 봉인이 갈라짐: 7일차의 보랏빛 상자. 고백 — 금이 번지다 깨져 분홍 빛이 터진다 · 찢어짐 — 안에서 부풀어 찢긴다 · 풀기 — 모서리가 하나씩 풀려 떠오른다 (5초, 뒤이어 강림) */
function bxConfShow(fx){
  const {seg,io,oc}=XF, v=fx.v||'conf', T=5.0, rnd=XF.rng(31), BRK=v==='force'?2.3:2.8;
  const title=tr(v==='force'?`제${fx.d}일 · 봉인이 찢어지다`:v==='unseal'?`제${fx.d}일 · 봉인을 풀다`:`제${fx.d}일 · 고백`);
  const sub=tr(v==='force'?'“…미안해요. 끝까지는 못 버텼어요.”':v==='unseal'?'상자가 소리 없이 열렸다':'“그 수녀가 키아라예요. 성배를 삼키려고 해요.”');
  const V=xfxOpen('dsc bxs',`${title} · ${sub}`,bxTxtH(title,sub),T,frame); fxSnd(V.o,v==='force'?'j_bx_tear':v==='unseal'?'j_bx_open':'j_bx_conf');
  const text=bxTxtF(V,v==='unseal'?2.4:BRK+.2,T-.8);
  const CR=[...Array(16)].map(()=>({f:Math.floor(rnd()*6),u0:.25+rnd()*.5,v0:.25+rnd()*.5,st:[...Array(6)].map(()=>[(rnd()-.5)*.36,(rnd()-.5)*.36]),d:rnd()}));
  const WS=[...Array(7)].map(()=>({a:-Math.PI/2+(rnd()-.5)*2.6,w:rnd()*6,l:.6+rnd()*.5}));
  let SH=null;
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, cy=H*.4, out=io(seg(t,T-.7,T));
    const dark=io(seg(t,0,.4))*(1-out); c.fillStyle=`rgba(7,3,12,${.88*dark})`; c.fillRect(0,0,W,H);
    const ca=oc(seg(t,.1,.6))*(1-out), br=t>=BRK;
    const shk=v==='unseal'||br?0:seg(t,v==='force'?.5:1.3,BRK), jx=(Math.random()-.5)*10*D*shk, jy=(Math.random()-.5)*6*D*shk;
    const bulge=v==='force'?1+.14*io(seg(t,.5,BRK))+.03*Math.sin(t*18)*seg(t,1.2,BRK):1;
    const R=150*s*bulge, rot=.6+t*(v==='unseal'?.12:.25), P=bxCubeP(cx+jx,cy+jy,R,rot);
    const glow=v==='unseal'?0:seg(t,v==='force'?.5:1.1,BRK);
    if(v==='unseal'){ const r=io(seg(t,1.6,3.0)); bxGlow(c,cx,cy+30*s,170*s,BXF.gold,.45*r*(1-out)); bxCupDraw(c,cx,cy+80*s,s*.62,r*(1-out),D,null); }
    bxGlow(c,cx,cy,R*(1+glow),BXF.pk2,(.12+.6*glow)*ca*(br?1-seg(t,BRK,BRK+1.4):1));
    if(!br||v==='unseal'){ const op=v==='unseal'?1-io(seg(t,1.3,3.0)):1; c.save(); c.lineCap='round';
      for(const f of BXC_F){ c.beginPath(); f.forEach((i,j)=>j?c.lineTo(P[i][0],P[i][1]):c.moveTo(P[i][0],P[i][1])); c.closePath(); c.fillStyle=`rgba(150,100,230,${(.09+.08*glow)*ca*op})`; c.fill();
        c.strokeStyle=`rgba(${BXF.vio},${.25*ca*op})`; c.lineWidth=.8*D; const A=P[f[0]],B=P[f[1]],C=P[f[2]],E=P[f[3]]; for(let g=1;g<3;g++){ const u=g/3; c.beginPath(); c.moveTo(A[0]+(B[0]-A[0])*u,A[1]+(B[1]-A[1])*u); c.lineTo(E[0]+(C[0]-E[0])*u,E[1]+(C[1]-E[1])*u); c.moveTo(A[0]+(E[0]-A[0])*u,A[1]+(E[1]-A[1])*u); c.lineTo(B[0]+(C[0]-B[0])*u,B[1]+(C[1]-B[1])*u); c.stroke(); } }
      BXC_E.forEach(([a,b],i)=>{ let [x1,y1]=P[a], [x2,y2]=P[b], ea=op;
        if(v==='unseal'){ const k=io(seg(t,1.0+i*.08,2.4+i*.08)), mx=(x1+x2)/2-cx, my=(y1+y2)/2-cy, L=Math.hypot(mx,my)||1, dd=k*90*s; x1+=mx/L*dd; x2+=mx/L*dd; y1+=my/L*dd-k*50*s; y2+=my/L*dd-k*50*s; ea=1-k; }
        c.strokeStyle=`rgba(${BXF.vio},${.85*ca*ea})`; c.lineWidth=2*D; c.shadowColor=`rgba(${BXF.vio},1)`; c.shadowBlur=12*D; c.beginPath(); c.moveTo(x1,y1); c.lineTo(x2,y2); c.stroke(); });
      if(v!=='unseal'){ const ck=seg(t,v==='force'?.7:1.0,BRK); c.shadowColor=`rgba(${BXF.pink},1)`; c.shadowBlur=10*D; c.strokeStyle=`rgba(255,205,232,${.95*ca})`; c.lineWidth=1.5*D;
        for(const k of CR){ const L=Math.max(0,Math.min(1,(ck-k.d*.55)*2.2)); if(L<=0) continue; let u=k.u0, w=k.v0, p=bxFacePt(P,k.f,u,w); c.beginPath(); c.moveTo(p[0],p[1]);
          const nn=L*k.st.length; for(let j=0;j<nn;j++){ const f=Math.min(1,nn-j); u=Math.max(0,Math.min(1,u+k.st[j][0]*f)); w=Math.max(0,Math.min(1,w+k.st[j][1]*f)); p=bxFacePt(P,k.f,u,w); c.lineTo(p[0],p[1]); } c.stroke(); } }
      c.restore(); }
    if(br&&v!=='unseal'){ // 깨짐: 면 조각이 흩어지고 분홍 실오라기가 터져 나온다
      if(!SH){ SH=[]; for(let f=0;f<6;f++) for(let j=0;j<6;j++){ const p=bxFacePt(P,f,rnd(),rnd()), a=Math.atan2(p[1]-cy,p[0]-cx), sp=(180+rnd()*520)*D; SH.push({x:p[0],y:p[1],vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-90*D,r:rnd()*6,vr:(rnd()-.5)*10,s:(5+rnd()*12)*s*2,l:1.3}); } }
      for(const q of SH){ q.x+=q.vx*dt; q.y+=q.vy*dt; q.vy+=340*D*dt; q.r+=q.vr*dt; q.l-=dt*.8; if(q.l<=0) continue; c.save(); c.translate(q.x,q.y); c.rotate(q.r); c.globalAlpha=Math.min(1,q.l)*(1-out); c.fillStyle='rgba(170,130,240,.45)'; c.strokeStyle=`rgba(${BXF.vio},.95)`; c.lineWidth=1*D; c.beginPath(); c.moveTo(-q.s/2,-q.s/3); c.lineTo(q.s/2,-q.s/4); c.lineTo(0,q.s/2); c.closePath(); c.fill(); c.stroke(); c.restore(); }
      const wk=seg(t,BRK,BRK+1.4); if(wk<1){ c.save(); c.lineWidth=1.8*D; c.shadowColor=`rgba(${BXF.pk2},1)`; c.shadowBlur=12*D;
        for(const w of WS){ c.strokeStyle=`rgba(${BXF.pink},${.85*(1-wk)})`; c.beginPath(); const len=Math.min(W,H)*w.l*io(Math.min(1,wk*1.6));
          for(let i=0;i<=30;i++){ const u=i/30, x=cx+Math.cos(w.a)*len*u+Math.sin(u*7+t*3+w.w)*42*s*u, y=cy+Math.sin(w.a)*len*u; i?c.lineTo(x,y):c.moveTo(x,y); } c.stroke(); } c.restore(); }
      const fl=Math.exp(-Math.pow((t-BRK-.04)/.09,2)); if(fl>.01){ c.fillStyle=`rgba(255,215,238,${.6*fl})`; c.fillRect(0,0,W,H); } }
    if(G) G.style.transform=shk>0?`translate(${(jx/D*.5).toFixed(1)}px,0)`:'';
    text(t); }
}

/* ⑩ 토벌령: 교회 종이 두 번 울리고, 감독관의 공문이 내려앉아 붉은 도장이 찍힌다 (3.8초) */
function bxOrderShow(fx){
  const {seg,io,oc,ob}=XF, T=3.8, me=!!fx.me, ST=1.55;
  const h=tr('감독관의 토벌령'), l1=tr('성배를 가로챈 자'), who=me?tr('당신의 조'):tr(fx.tgt||''), l2=tr('그 체력을 무너뜨린 조에게 령주 한 획을 준다'), stp=tr('토벌');
  const html=`<div class="bxo${me?' me':''}"><div class="bxo-h">${esc(h)}</div><div class="bxo-l">${esc(l1)}</div><div class="bxo-t">${esc(who)}</div><div class="bxo-s">${esc(l2)}</div><div class="bxo-st" aria-hidden="true"><b>†</b><span>${esc(stp)}</span></div></div>`;
  const V=xfxOpen('dsc bxo-x',`${h} · ${l1} ${who}`,html,T,frame); fxSnd(V.o,'j_bx_order');
  const card=V.o.querySelector('.bxo'), st=V.o.querySelector('.bxo-st'); let INK=null;
  function bell(c,x,y,sz,sw,a,D){ c.save(); c.translate(x,y); c.rotate(sw); c.globalAlpha=a; c.fillStyle='rgba(30,20,22,.95)'; c.strokeStyle='rgba(230,200,150,.8)'; c.lineWidth=1.4*D;
    c.beginPath(); c.moveTo(-sz*.18,0); c.bezierCurveTo(-sz*.2,sz*.35,-sz*.32,sz*.62,-sz*.52,sz*.78); c.lineTo(sz*.52,sz*.78); c.bezierCurveTo(sz*.32,sz*.62,sz*.2,sz*.35,sz*.18,0); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.arc(0,sz*.86,sz*.08,0,Math.PI*2); c.fill(); c.stroke(); c.beginPath(); c.moveTo(0,0); c.lineTo(0,-sz*.18); c.stroke(); c.restore(); }
  function frame(t,dt){ const {c,W,H,D,G}=V; c.clearRect(0,0,W,H); const s=Math.min(W,H,640*D)/520, cx=W/2, out=io(seg(t,T-.6,T));
    const dark=io(seg(t,0,.35))*(1-out); c.fillStyle=`rgba(10,5,6,${.82*dark})`; c.fillRect(0,0,W,H);
    // 종: 0.15 · 0.85초에 울린다
    const by=H*.08, bs=58*s, sw=Math.sin(t*5.2)*.32*Math.exp(-t*.6)*(t>.05?1:0);
    bell(c,cx,by,bs,sw,oc(seg(t,0,.3))*(1-out),D);
    for(const t0 of [.15,.85]){ for(let k=0;k<3;k++){ const r=seg(t,t0+k*.12,t0+k*.12+1.4); if(r<=0||r>=1) continue; c.strokeStyle=`rgba(235,205,160,${.45*(1-r)*(1-out)})`; c.lineWidth=1.4*D; c.beginPath(); c.arc(cx,by+bs*.6,(30+420*io(r))*s,.15*Math.PI,.85*Math.PI); c.stroke(); } }
    // 공문이 내려앉는다
    const ci=io(seg(t,.35,.85)); card.style.opacity=(ci*(1-out)).toFixed(3); card.style.transform=`translate(-50%,calc(-50% + ${((1-ci)*-24).toFixed(1)}px))`;
    // 도장: 1.55초에 쾅
    const k=seg(t,ST-.14,ST), sc=t<ST-.14?0:t<ST?2.4-1.4*io(k):1; st.style.opacity=t<ST-.14?0:(Math.min(1,k*2)*(1-out)).toFixed(3); st.style.transform=`rotate(-14deg) scale(${sc.toFixed(3)})`;
    const hit=Math.max(0,1-Math.abs(t-ST)/.18); if(G) G.style.transform=hit>0?`translate(${((Math.random()-.5)*8*hit).toFixed(1)}px,${((Math.random()-.5)*5*hit).toFixed(1)}px)`:'';
    card.style.translate=hit>0?`${((Math.random()-.5)*5*hit).toFixed(1)}px ${((Math.random()-.5)*3*hit).toFixed(1)}px`:'0 0';
    if(t>=ST&&!INK){ const r=st.getBoundingClientRect(), R=XF.rng(9); INK=[...Array(16)].map(()=>{ const a=R()*Math.PI*2, d=(r.width*.55+R()*28)*D; return {x:(r.left+r.width/2)*D+Math.cos(a)*d,y:(r.top+r.height/2)*D+Math.sin(a)*d,r:(1+R()*2.6)*D}; }); }
    if(INK){ const a=Math.min(1,seg(t,ST,ST+.1))*(1-out); c.fillStyle=`rgba(170,24,36,${.75*a})`; for(const p of INK){ c.beginPath(); c.arc(p.x,p.y,p.r,0,Math.PI*2); c.fill(); } }
    const fl=Math.exp(-Math.pow((t-ST-.02)/.06,2)); if(fl>.01){ c.fillStyle=`rgba(255,235,225,${.25*fl})`; c.fillRect(0,0,W,H); } }
}

/* ⑪ 키아라와의 보구 격돌: 상대 쪽 빛이 분홍으로 물들고, 키아라 뒤에서 연꽃 만다라가 핀다. 키아라가 꿰뚫으면 연꽃이 화면을 덮으며 꽃잎이 이쪽으로 흩날린다 · 우리가 꿰뚫으면 연꽃이 잿빛으로 시든다 */
function bxKxSvg(fx){ const res=fx.res; let p='', p2='', d='', pet='';
  for(let i=0;i<12;i++) p+=`<path d="M0 0 C11 -11 10 -36 0 -50 C-10 -36 -11 -11 0 0Z" transform="rotate(${i*30})" fill="url(#kxpg)" stroke="#ff9ccc" stroke-width=".8"/>`;
  for(let i=0;i<8;i++) p2+=`<path d="M0 0 C8 -8 7 -25 0 -34 C-7 -25 -8 -8 0 0Z" transform="rotate(${i*45+22.5})" fill="#ffd6ea" fill-opacity=".6"/>`;
  for(let i=0;i<16;i++){ const a=i/16*Math.PI*2; d+=`<circle cx="${(Math.cos(a)*68).toFixed(1)}" cy="${(Math.sin(a)*68).toFixed(1)}" r="1.6" fill="#ffc8e2"/>`; }
  return `<defs><radialGradient id="kxpg" cx="50%" cy="100%" r="110%"><stop offset="0" stop-color="#ff6fae" stop-opacity=".25"/><stop offset="1" stop-color="#ffeaf4" stop-opacity=".9"/></radialGradient></defs>
  <g class="kx-bg" transform="translate(300 128)"><g class="kx-lo ${res==='en'?'w':res==='me'?'l':'o'}"><g class="kx-sp"><circle r="60" fill="none" stroke="#ff9ccc" stroke-width=".8" stroke-dasharray="2 6"/><circle r="72" fill="none" stroke="#ff9ccc" stroke-opacity=".7" stroke-width=".8" stroke-dasharray="10 5"/>${d}</g><g class="kx-sp r">${p}</g>${p2}<circle r="9" fill="#fff1f8"/></g></g>`; }
function bxKxPet(fx){ let pet=''; if(fx.res==='en') for(let k=0;k<20;k++){ const dx=-(150+(k*53)%170), dy=(k*37)%140-70; pet+=`<ellipse class="kx-pt" cx="300" cy="128" rx="4.5" ry="2.2" fill="#ffb3d6" style="--dx:${dx}px;--dy:${dy}px;--dl:${(k%7)*45}ms"/>`; } return pet; }
{ const f0=clashShow; clashShow=function(fx){ if(!fx||!fx.kx||fx.t!=='clash') return f0(fx); const c0=CFX_C.en; CFX_C.en=['#ffe9f4','#ff9ccc','#e0559c'];
    try{ f0(fx); } finally{ CFX_C.en=c0; }
    const o=$('#cfx'); if(!o) return; o.classList.add('kx'); const sv=o.querySelector('svg'); if(sv){ sv.insertAdjacentHTML('afterbegin',bxKxSvg(fx)); sv.insertAdjacentHTML('beforeend',bxKxPet(fx)); } fxSnd(o,'j_bx_np'); }; }
