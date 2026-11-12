  // ---- 비스트 Ⅲ/R 결말 ----
  // 달로 간 잔 (11-12 2판): 키아라가 꽃잎으로 흩어지고 성배만 남는다. BB가 어디 있었느냐에 따라 다르게 달로 간다
  //  me    — ① 달의 뒷면에서 끼어드는 '긴급 방송'으로 시작 · BB가 성배를 안고 오른다 · ⑤ 달에서 장난스러운 인사, 한 박자 뒤 작게 진심 한 줄
  //  live  — ② BB의 그림자가 바닥에서 번져 성배를 감싸 삼키고 · ③ 그림자째 네모난 빛 조각으로 풀려 달로 올라간다
  //  nobb  — ③ 성배만 빛 조각으로 풀려 달로 올라간다(장난 없음)
  //  voice — ① 방송이 끼어들다 지직거리며 끊기고, 끊긴 목소리 한 줄 · 성배에서 달로 빛줄기
  //  공통  — ④ 마지막에 도시 아래쪽 불빛이 다시 켜지고 속보: 깊은 잠에 빠졌던 시민들이 깨어난다(없던 일로 고쳐 쓴 흔적)
  SCN.bxmoon={HOLD:7.2,init(){ const v=fx.k.slice(4); this.v=v; this.P=null; this.Q=null; this.L=null;
     setText('달로 간 잔',{me:'BB가 성배를 품에 안고 달로 돌아갔다.',live:'BB가 남은 성배를 품에 안고 달로 데려갔다.',nobb:'성배는 빛 조각으로 풀려 달로 올라갔다.',voice:'흩어졌던 목소리가 성배를 달로 데려갔다.'}[v]||'','아무도 소원을 빌지 않았다.','rgba(200,150,255,.95)'); OUT=99;
     this.HOLD={me:9.4,live:8.2,nobb:7.4,voice:7.8}[v]||7.4; this.TK={me:7.9,live:6.6,nobb:5.8,voice:6.2}[v]||6;
     TX.tickS.textContent=tr(`${opt.city} 전역에서 깊은 잠에 빠졌던 시민들 일제히 깨어나 · 밤사이 일을 기억하는 사람은 없어`);
     const tv=document.createElement('div'); tv.className='bxm-tv'; tv.innerHTML=`<i>● LIVE</i><span></span>`; o.appendChild(tv); this.tv=tv; this.tvS=tv.querySelector('span');
     const ms=document.createElement('div'); ms.className='bxm-msg'; ms.innerHTML=`<p class="a"></p><p class="b"></p>`; o.appendChild(ms); this.ma=ms.querySelector('.a'); this.mb=ms.querySelector('.b');
     // 결말 곡: 제목이 뜰 무렵 본 곡이 들어오는 자리부터 아주 작게 시작해 7초에 걸쳐 커진다(연출 끝 무렵 또렷해짐). 닫을 때까지 반복하고, 닫으면 3초 넘게 서서히 줄어 꺼진다
     this.MU={me:4.0,live:4.6,nobb:3.8,voice:3.8}[v]||4;
     try{ const h=Snd.cue('end_f',{at:this.MU,loop:true,off:26.3,fin:7,sync:true}); (o._snd=o._snd||[]).push({stop:tt=>h.stop(Math.max(tt||0,3.2))}); }catch(e){}
     this.CAP=tr('달의 뒷면에서 · 긴급 방송'); this.M1=tr(v==='voice'?'…배, 들려요…? 이건 제가…':'선배, 그럼 이만! 이건 제가 달에 잘 넣어 둘게요.'); this.M2=tr('…고마웠어요. 이번엔 진심이에요.'); },
   frame(t,dt){ const s=S_(), cx=W/2, inA=io(seg(t,0,.45)), base=H*.62, mx=cx, my=H*.15, mr=Math.min(W,H)*.075, v=this.v, R=rng(3);
    const type=(el,str,a,b)=>{ const n=Math.round([...str].length*seg(t,a,b)); el.textContent=[...str].slice(0,n).join(''); };
    dim(inA); bxMoon(c,mx,my,mr,inA*(.55+.45*seg(t,2,3)),D);
    // ① 끼어드는 방송 (me · voice)
    const BC=v==='me'||v==='voice', cut=v==='voice'?1.35:1.75;
    if(BC){ const sI=Math.max(Math.exp(-Math.pow((t-.25)/.12,2)),v==='voice'?seg(t,cut-.15,cut)*(1-seg(t,cut+.25,cut+.6))*(Math.random()<.4?.5:1):Math.exp(-Math.pow((t-cut)/.08,2))*.7); if(sI>.02) bxStatic(c,W,H,D,sI*inA,t);
      const on=seg(t,.35,.5)*(1-seg(t,cut,cut+.06)); this.tv.style.opacity=(on*inA).toFixed(3); this.tv.style.transform=`translate(-50%,0) translateX(${(t>cut-.25&&t<cut&&Math.random()<.5?(Math.random()-.5)*14:0).toFixed(1)}px)`;
      const str=v==='voice'?[...this.CAP].slice(0,Math.ceil([...this.CAP].length*.75)).join('')+'…':this.CAP; type(this.tvS,str,.5,v==='voice'?1.1:1.2);
      if(v==='voice'&&t>cut&&t<cut+.08){ c.fillStyle='rgba(0,0,0,.92)'; c.fillRect(0,0,W,H); } }
    else this.tv.style.opacity=0;
    // 키아라가 꽃잎으로 흩어진다
    const melt=seg(t,.2,1.5); if(melt<1) bxLotus(c,cx,base-100*s,130*s,1-melt*.8,t*.1,inA*(1-melt),D,false);
    if(!this.P&&t>.35){ const Rp=rng(5); this.P=[...Array(80)].map(()=>({x:cx+(Rp()-.5)*240*s,y:base-100*s+(Rp()-.5)*170*s,vx:(Rp()-.5)*30*D,vy:-(30+Rp()*90)*D,r:Rp()*6,sz:(2+Rp()*4)*D,l:1.4+Rp()*1.6})); }
    if(this.P) for(const p of this.P){ p.x+=p.vx*dt; p.y+=p.vy*dt; p.r+=dt*2; p.l-=dt; if(p.l<=0) continue; c.save(); c.translate(p.x,p.y); c.rotate(p.r); c.fillStyle=`rgba(${BXF.pink},${.6*Math.min(1,p.l)*inA})`; c.beginPath(); c.ellipse(0,0,p.sz,p.sz*.5,0,0,Math.PI*2); c.fill(); c.restore(); }
    let cX=cx, cB=base, cS=s*.75, cA=oc(seg(t,1.0,1.8))*inA, cut0=0, tint=null;
    const h=Math.min(210*s,H*.42), fx0=cx+80*s;
    // ③ 네모 조각으로 풀려 달로 (live · nobb): 위에서부터 한 줄씩 풀린다
    const DS=v==='live'?3.6:v==='nobb'?2.4:0;
    const shards=(x0,top,bot,wid,a0,dur,col)=>{ if(!this.Q){ const Rq=rng(21), g=7*D; this.Q=[]; for(let y=top;y<bot;y+=g) for(let x=x0-wid;x<x0+wid;x+=g) if(Rq()<.55) this.Q.push({x,y,u:(y-top)/(bot-top),j:Rq(),sz:(2+Rq()*4)*D}); }
      for(const q of this.Q){ const k=seg(t,a0+q.u*dur*.55+q.j*.25,a0+q.u*dur*.55+q.j*.25+dur*.55); if(k<=0||k>=1) continue; const e=io(k), x=q.x+(mx-q.x)*e+Math.sin(k*7+q.j*6)*14*s*(1-e), y=q.y+(my-q.y)*e;
        c.fillStyle=`rgba(${col},${(1-k*.6)*inA})`; c.fillRect(x-q.sz/2,y-q.sz/2,q.sz*(1-.5*e),q.sz*(1-.5*e)); } };
    if(v==='me'){ const fa=oc(seg(t,1.7,2.5)), take=io(seg(t,2.5,3.1)), rise=io(seg(t,3.2,5.4));
      const fX=fx0+(mx-fx0)*rise, fTop=(base-h)+(my-mr*.4-(base-h))*rise, k=1-.88*rise;
      cX=cx+(fx0-12*s-cx)*take+(mx-(fx0-12*s))*rise; cB=base+((base-h*.32)-base)*take+((my+mr*.2)-(base-h*.32))*rise; cS=s*.75*(1-.35*take)*k;
      bxBBSil(c,fX,fTop,h*k,fa*inA*(1-seg(t,5.0,5.6)),D); cA*=1-seg(t,5.0,5.6);
      const sp=Math.exp(-Math.pow((t-5.45)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp);
      // ⑤ 달에서 온 말: 장난스러운 인사 → 한 박자 쉬고 작게 진심
      type(this.ma,this.M1,5.7,6.6); this.ma.style.opacity=(seg(t,5.6,5.8)*inA).toFixed(3);
      this.mb.textContent=this.M2; this.mb.style.opacity=(oc(seg(t,7.2,7.9))*inA).toFixed(3); this.mb.style.filter=`blur(${((1-seg(t,7.2,7.9))*3).toFixed(1)}px)`; }
    else if(v==='live'){ const fa=oc(seg(t,1.7,2.5))*(1-seg(t,4.6,5.4)), sh=io(seg(t,2.4,3.1)), wrap=io(seg(t,2.9,3.6));
      // ② 그림자: BB의 발밑에서 번져 성배까지 · 촉수처럼 솟아 감싼다
      if(sh>0){ c.save(); const gx=fx0+(cx-fx0)*.5; const gg=c.createRadialGradient(gx,base,0,gx,base,180*s*sh); gg.addColorStop(0,`rgba(4,0,8,${.95*inA})`); gg.addColorStop(.75,`rgba(30,8,50,${.8*inA})`); gg.addColorStop(1,'rgba(30,8,50,0)');
        c.fillStyle=gg; c.beginPath(); c.ellipse(gx,base,190*s*sh,26*s*sh,0,0,Math.PI*2); c.fill(); c.restore(); }
      if(wrap>0){ const top=base-160*cS*1.05, gone=seg(t,DS,DS+1.2); c.save(); c.lineCap='round'; c.shadowColor=`rgba(${BXF.vio},.9)`; c.shadowBlur=10*D;
        for(let i=0;i<6;i++){ const sx=cx+(i-2.5)*34*s, side=i<3?-1:1, L=wrap*(1-gone); if(L<=0) continue; c.strokeStyle=`rgba(6,1,12,${.95*inA*(1-gone)})`; c.lineWidth=(9-Math.abs(i-2.5)*1.6)*D;
          c.beginPath(); c.moveTo(sx,base); const ex=cx+side*20*s*(1-L), ey=base-(base-top)*L; c.bezierCurveTo(sx+side*40*s,base-40*s*L,cx-side*70*s*L,ey+60*s*L+Math.sin(t*3+i)*6*s,ex,ey); c.stroke(); }
        c.restore(); tint=BXF.vio; }
      cut0=seg(t,DS,DS+1.4); bxBBSil(c,fx0,base-h,h,fa*inA,D);
      shards(cx,base-160*cS,base,64*cS,DS,1.8,BXF.vio);
      const sp=Math.exp(-Math.pow((t-5.6)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp); }
    else if(v==='nobb'){ const pool=seg(t,1.8,2.4)*inA*(1-seg(t,4.2,5));
      bxGlow(c,cx,base+6*s,190*s,BXF.vio,.3*pool); c.strokeStyle=`rgba(${BXF.vio},${.45*pool})`; c.lineWidth=1.2*D; c.beginPath(); c.ellipse(cx,base,150*s,16*s,0,0,Math.PI*2); c.stroke();
      cut0=seg(t,DS,DS+1.6); shards(cx,base-160*cS,base,64*cS,DS,2.0,BXF.gold);
      const sp=Math.exp(-Math.pow((t-4.7)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp); }
    else { // voice: 끊긴 목소리 한 줄 → 빛줄기
      type(this.ma,this.M1,1.9,2.6); this.ma.style.opacity=(seg(t,1.85,1.95)*(1-seg(t,3.6,4.2))*inA).toFixed(3); this.ma.style.transform=`translateX(${(t>2.3&&t<2.7&&Math.random()<.4?(Math.random()-.5)*10:0).toFixed(1)}px)`;
      const bm=seg(t,2.6,3.0); cA*=1-bm; const ba=bm*(1-seg(t,3.3,4.4))*inA; if(ba>0){ c.save(); c.strokeStyle=`rgba(240,225,255,${ba})`; c.shadowColor=`rgba(${BXF.vio},1)`; c.shadowBlur=20*D; c.lineWidth=(2+4*(1-bm))*D; c.beginPath(); c.moveTo(cx,base-110*s); c.lineTo(mx,my); c.stroke(); c.restore(); }
      const sp=Math.exp(-Math.pow((t-3.05)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp); }
    if(cA>0&&cut0<1){ const top=cB-160*cS-12*cS, ky=top+(cB-top)*cut0; bxGlow(c,cX,cB-110*cS,150*cS,tint||BXF.gold,.4*cA*(1-cut0)); c.save(); c.beginPath(); c.rect(0,ky,W,H); c.clip(); bxCupDraw(c,cX,cB,cS,cA*(tint?.85:1),D,tint); c.restore(); }
    // ④ 도시의 불빛이 다시 켜진다 · 속보
    const TK=this.TK; if(t>TK-.6){ if(!this.L){ const Rl=rng(33); this.L=[...Array(110)].map(()=>{ const x=Rl(); return {x:x*W,y:H*(.7+Rl()*.16),d:Math.abs(x-.5)+Rl()*.15}; }); }
      for(const L of this.L){ const a=oc(seg(t,TK-.6+L.d*1.6,TK-.3+L.d*1.6))*inA; if(a<=0) continue; c.fillStyle=`rgba(255,214,150,${.75*a})`; c.fillRect(L.x-1.2*D,L.y-1.2*D,2.4*D,2.4*D); } }
    TX.tick.style.opacity=seg(t,TK,TK+.3)*(1-io(seg(t,OUT,OUT+.9))); TX.tickS.style.clipPath=`inset(0 ${(100-100*seg(t,TK+.2,TK+1.3)).toFixed(1)}% 0 0)`;
    text(t,v==='me'?3.6:v==='live'?4.2:3.6,4.5); }};
  // 단꿈: 도시의 불빛이 분홍으로 물들며 가운데서부터 하나씩 꺼진다. 한 점만 남는다 → 속보
  SCN.bxdream={HOLD:7.6,init(){ o.classList.add('flood'); setText('단꿈','그 겨울, 도시는 한 사람의 쾌락이 되었다.','당신만이 남겨졌다.','rgba(255,150,200,.95)');
     TX.tickS.textContent=tr(`${opt.city} 전역 원인 모를 깊은 잠 확산 · 깨어나지 않는 시민 수십만 명 · 모두 웃는 얼굴로 잠들어`); OUT=99;
     const R=rng(77), g=Math.max(26,Math.min(W,H)/16); this.L=[]; for(let y=0;y<H;y+=g/2) for(let x=0;x<W;x+=g/2) if(R()<.3) this.L.push({x:x+g*.25*R(),y:y+g*.25*R(),d:Math.hypot(x/W-.5,(y/H-.5)*.8)+R()*.12});
     const far=this.L.filter(L=>L.d>.35&&L.y>H*.35); this.me=far.length?far[Math.floor(R()*far.length)]:this.L[0]; this.P=null; },
   frame(t,dt){ const inA=io(seg(t,0,.45)), sp=io(seg(t,.8,3.8));
    dim(inA); map(t,.9*inA,0,false,'flood');
    glow(W/2,H/2,Math.max(W,H)*.8*sp+1,'255,130,195',.3*sp*inA); bxLotus(c,W/2,H/2,Math.min(W,H)*.25*sp,sp,t*.05,.22*inA*sp,D,false);
    for(const L of this.L){ const me=L===this.me, at=.8+L.d*3.3, pk=seg(t,at,at+.25), off=me?0:seg(t,at+.25,at+.6), a=(me?.75+.25*Math.sin(t*3):1-off)*inA; if(a<=0) continue;
      c.fillStyle=me?`rgba(255,214,140,${a})`:`rgba(255,${Math.round(214-70*pk)},${Math.round(140+70*pk)},${.85*a})`; c.fillRect(L.x-1.4*D,L.y-1.4*D,2.8*D,2.8*D); }
    if(t>3.8) glow(this.me.x,this.me.y,34*D,'255,214,140',.45*inA*seg(t,3.8,4.4));
    if(!this.P&&t>1.0){ const R=rng(9); this.P=[...Array(50)].map(()=>({x:R()*W,y:R()*H,v:(10+R()*30)*D,r:R()*6,sz:(2+R()*3.5)*D})); }
    if(this.P) for(const p of this.P){ p.y+=p.v*dt; p.r+=dt; if(p.y>H) p.y=-10; c.save(); c.translate(p.x+Math.sin(t+p.r)*10*D,p.y); c.rotate(p.r); c.fillStyle=`rgba(${BXF.pink},${.45*sp*inA})`; c.beginPath(); c.ellipse(0,0,p.sz,p.sz*.5,0,0,Math.PI*2); c.fill(); c.restore(); }
    text(t,3.4,4.6); const tk=seg(t,4.8,5.1)*(1-io(seg(t,OUT,OUT+.9))); TX.tick.style.opacity=tk; TX.tickS.style.clipPath=`inset(0 ${(100-100*seg(t,5.0,6.1)).toFixed(1)}% 0 0)`; }};

