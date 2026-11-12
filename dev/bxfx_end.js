  // ---- 비스트 Ⅲ/R 결말 ----
  // 달로 간 잔: 키아라가 시든 연꽃처럼 꽃잎으로 흩어지고, 성배만 남는다. BB가 어디 있었느냐에 따라 성배가 달로 가는 모습이 다르다
  SCN.bxmoon={HOLD:7.2,init(){ const v=fx.k.slice(4); this.v=v; this.P=null; this.S=null;
     setText('달로 간 잔',{me:'BB가 성배를 품에 안고 달로 돌아갔다.',live:'BB가 남은 성배를 품에 안고 달로 데려갔다.',nobb:'성배는 달빛 속으로 가라앉듯 사라졌다.',voice:'흩어졌던 목소리가 성배를 달로 데려갔다.'}[v]||'','아무도 소원을 빌지 않았다.','rgba(200,150,255,.95)'); OUT=99; },
   frame(t,dt){ const s=S_(), cx=W/2, inA=io(seg(t,0,.45)), base=H*.64, mx=cx, my=H*.15, mr=Math.min(W,H)*.075, v=this.v;
    dim(inA); bxMoon(c,mx,my,mr,inA*(.55+.45*seg(t,2,3)),D);
    const mb=seg(t,1.6,2.4)*inA; if(mb>0){ const g=c.createLinearGradient(0,my,0,base); g.addColorStop(0,`rgba(${BXF.vio},${.28*mb})`); g.addColorStop(1,`rgba(${BXF.vio},${.04*mb})`); c.fillStyle=g; c.beginPath(); c.moveTo(mx-mr*.6,my); c.lineTo(mx+mr*.6,my); c.lineTo(cx+120*s,base); c.lineTo(cx-120*s,base); c.closePath(); c.fill(); }
    const melt=seg(t,.2,1.5); if(melt<1) bxLotus(c,cx,base-100*s,130*s,1-melt*.8,t*.1,inA*(1-melt),D,false);
    if(!this.P&&t>.35){ const R=rng(5); this.P=[...Array(80)].map(()=>({x:cx+(R()-.5)*240*s,y:base-100*s+(R()-.5)*170*s,vx:(R()-.5)*30*D,vy:-(30+R()*90)*D,r:R()*6,sz:(2+R()*4)*D,l:1.4+R()*1.6})); }
    if(this.P) for(const p of this.P){ p.x+=p.vx*dt; p.y+=p.vy*dt; p.r+=dt*2; p.l-=dt; if(p.l<=0) continue; c.save(); c.translate(p.x,p.y); c.rotate(p.r); c.fillStyle=`rgba(${BXF.pink},${.6*Math.min(1,p.l)*inA})`; c.beginPath(); c.ellipse(0,0,p.sz,p.sz*.5,0,0,Math.PI*2); c.fill(); c.restore(); }
    let cX=cx, cB=base, cS=s*.75, cA=oc(seg(t,1.0,1.8))*inA;
    if(v==='me'||v==='live'){ const fa=oc(seg(t,1.7,2.5)), take=io(seg(t,2.5,3.1)), rise=io(seg(t,3.2,5.4)), h=Math.min(210*s,H*.42), fx0=cx+80*s;
      const fX=fx0+(mx-fx0)*rise, fTop=(base-h)+(my-mr*.4-(base-h))*rise, k=1-.88*rise; 
      cX=cx+(fx0-12*s-cx)*take+(mx-(fx0-12*s))*rise; cB=base+((base-h*.32)-base)*take+((my+mr*.2)-(base-h*.32))*rise; cS=s*.75*(1-.35*take)*k;
      bxBBSil(c,fX,fTop,h*k,fa*inA*(1-seg(t,5.0,5.6)),D); cA*=1-seg(t,5.0,5.6);
      const sp=Math.exp(-Math.pow((t-5.45)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp); }
    else if(v==='nobb'){ const sink=io(seg(t,2.4,4.6)); cB=base+150*s*sink; const pool=seg(t,1.8,2.4)*inA;
      bxGlow(c,cx,base+6*s,190*s,BXF.vio,.35*pool); c.strokeStyle=`rgba(${BXF.vio},${.5*pool})`; c.lineWidth=1.2*D; c.beginPath(); c.ellipse(cx,base,160*s,18*s,0,0,Math.PI*2); c.stroke();
      for(let k=0;k<3;k++){ const q=seg(t,2.6+k*.5,4.0+k*.5); if(q>0&&q<1){ c.strokeStyle=`rgba(${BXF.vio},${.5*(1-q)})`; c.beginPath(); c.ellipse(cx,base,(60+q*220)*s,(7+q*24)*s,0,0,Math.PI*2); c.stroke(); } }
      c.save(); c.beginPath(); c.rect(0,0,W,base); c.clip(); bxCupDraw(c,cX,cB,cS,cA,D,BXF.vio); c.restore(); cA=0; }
    else { const bm=seg(t,2.6,3.0); cA*=1-bm; const ba=bm*(1-seg(t,3.3,4.4))*inA; if(ba>0){ c.save(); c.strokeStyle=`rgba(240,225,255,${ba})`; c.shadowColor=`rgba(${BXF.vio},1)`; c.shadowBlur=20*D; c.lineWidth=(2+4*(1-bm))*D; c.beginPath(); c.moveTo(cx,base-110*s); c.lineTo(mx,my); c.stroke(); c.restore(); }
      const sp=Math.exp(-Math.pow((t-3.05)/.12,2)); if(sp>.01) bxGlow(c,mx,my,mr*2.5,'255,240,255',.9*sp); }
    if(cA>0){ bxGlow(c,cX,cB-110*cS,150*cS,BXF.gold,.4*cA); bxCupDraw(c,cX,cB,cS,cA,D); }
    text(t,3.6,4.5); }};
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

