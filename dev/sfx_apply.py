"""소환 연출: 문 캔서(BB) · 얼터 에고(멜트릴리스 · 패션립) (11-12 시안)
- 문 캔서: 뒤로 달이 떠오르고, 마법진이 줄 단위로 어긋나며 고쳐 쓰인다. 터지면 화면이 한 번 다시 그려지고(주사선 · 색 어긋남) 초상이 위에서 아래로 한 줄씩 그려진다.
- 얼터 에고: 마법진이 둘로 겹쳐 그려지다 하나로 합쳐진다. 세 빛깔(세 여신)의 흐름이 소용돌이쳐 모이고, 터지면 물결이 번지고 유리 조각이 흩어진다. 초상은 두 빛의 잔상이 하나로 겹친다.
사용: python3 sfx_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("sound:'j_summon_avenger'}};",
       "sound:'j_summon_avenger'},\n"
       "  moon:{ln:'206,150,255',gl:'232,96,214',pt:'255,176,240',pl:'250,226,255',nm:'#fbeefe',ng:'232,110,224',cl:'#dca8f4',pg:'232,120,236',sound:'j_summon_moon'},\n"
       "  ego:{ln:'160,206,240',gl:'120,172,255',pt:'196,226,255',pl:'236,246,255',nm:'#eef6ff',ng:'140,190,255',cl:'#aecbee',pg:'150,192,255',sound:'j_summon_ego'}};\n"
       "const EGO_C=['255,172,216','138,226,246','212,200,255']; // 얼터 에고: 세 여신의 빛깔")
    # 준비: 문 캔서의 화면 복사본 · 얼터 에고의 물결
    rp("  // 마법진: 층마다 진행만큼 선을 따라 그린다.",
       "  const gcv=K==='moon'?document.createElement('canvas'):null, gcx=gcv&&gcv.getContext('2d'); if(gcv){ gcv.width=c1.width; gcv.height=c1.height; }\n"
       "  let ripples=[];\n"
       "  // 마법진: 층마다 진행만큼 선을 따라 그린다.")
    rp("  const pf=fly.querySelector('.pf');",
       """  // 문 캔서: 마법진 뒤로 떠오르는 달 (위로 갈수록 주사선)
  const moonY=H*(low?.24:.3), moonR=Math.min(W*.42,H*.27);
  function moonBack(t,pre,post,out){ const a=(t<2800?.1+.38*pre:.45*post+.4*(1-ss((t-2800)/260)))*out; if(a<=0) return; const y=moonY+(1-eo(t/2600))*H*.08;
    const gr=g.createRadialGradient(cx,y,0,cx,y,moonR); gr.addColorStop(0,`rgba(252,246,255,${a})`); gr.addColorStop(.72,`rgba(236,216,255,${.9*a})`); gr.addColorStop(.9,`rgba(222,140,240,${.55*a})`); gr.addColorStop(1,'rgba(200,100,230,0)');
    g.fillStyle=gr; g.beginPath(); g.arc(cx,y,moonR,0,6.2832); g.fill();
    g.fillStyle=`rgba(26,8,36,${.22*a})`; for(let yy=y-moonR;yy<y+moonR;yy+=4) g.fillRect(cx-moonR,yy,moonR*2,1.2);
    const hz=g.createRadialGradient(cx,y,moonR*.9,cx,y,moonR*1.8); hz.addColorStop(0,`rgba(${T.gl},${.25*a})`); hz.addColorStop(1,`rgba(${T.gl},0)`); g.fillStyle=hz; g.beginPath(); g.arc(cx,y,moonR*1.8,0,6.2832); g.fill(); }
  // 문 캔서: 그려진 마법진을 줄 단위로 어긋나게 다시 쓴다
  function moonGlitch(t,pre){ const I=t<2800?(t>1300?.7*pre*pre:0):t<3350?1-ss((t-2800)/550):0; if(I<=0||rnd()>.18+.82*I) return;
    gcx.setTransform(1,0,0,1,0,0); gcx.clearRect(0,0,gcv.width,gcv.height); gcx.drawImage(c1,0,0);
    g.save(); g.setTransform(1,0,0,1,0,0); const n=Math.floor(2+9*I);
    for(let k=0;k<n;k++){ const y=Math.floor(rnd()*H)*dpr, hh=Math.floor((3+rnd()*18)*dpr), dx=Math.round((rnd()-.5)*70*I)*dpr;
      g.clearRect(0,y,c1.width,hh); g.globalCompositeOperation='source-over'; g.globalAlpha=1; g.drawImage(gcv,0,y,c1.width,hh,dx,y,c1.width,hh);
      g.globalCompositeOperation='lighter'; g.globalAlpha=.4; g.drawImage(gcv,0,y,c1.width,hh,dx+6*dpr,y,c1.width,hh); }
    g.restore(); }
  const pf=fly.querySelector('.pf');""")
    # 그리기 순서: 달 → (얼터 에고는 겹친 두 마법진) → 어긋남
    rp("bg.style.opacity=out; c1.style.opacity=out; c2.style.opacity=out; circle(t,glow);",
       "bg.style.opacity=out; c1.style.opacity=out; c2.style.opacity=out;\n"
       "    if(K==='moon') moonBack(t,pre,post,out);\n"
       "    if(K==='ego'&&t<2800){ const d=G.rx*.3*(1-ss((t-200)/2450)), x0=G.cx, ln0=T.ln, gl0=T.gl, m=ss((t-2200)/500); g.globalAlpha=.65+.35*m; G.cx=x0-d; if(m<1){ T.ln=EGO_C[1]; T.gl=EGO_C[1]; } circle(t,glow); G.cx=x0+d; if(m<1){ T.ln=EGO_C[0]; T.gl=EGO_C[0]; } circle(t,glow); T.ln=ln0; T.gl=gl0; G.cx=x0; g.globalAlpha=1; } else circle(t,glow);\n"
       "    if(K==='moon') moonGlitch(t,pre);")
    # 흔들림: 문 캔서는 터질 때 화면이 툭툭 어긋난다
    rp("c1.style.transform=c2.style.transform=`translate(${sx}px,${sy}px)`;",
       "if(K==='moon'&&t>2780&&t<3300&&rnd()<.45) sx=Math.round((rnd()-.5)*18);\n"
       "    c1.style.transform=c2.style.transform=`translate(${sx}px,${sy}px)`;")
    # 모이는 기운: 문 캔서는 네모난 빛 조각, 얼터 에고는 세 빛깔의 흐름
    rp("parts.push({a:rnd()*6.2832,r:1.05,v:.004+rnd()*.006,z:0,s:(K==='shadow'?8+rnd()*16:1+rnd()*1.6)});",
       "parts.push({a:rnd()*6.2832,r:1.05,v:.004+rnd()*.006,z:0,s:(K==='shadow'?8+rnd()*16:1+rnd()*1.6),c:k%3});")
    rp("p.a+=K==='shadow'?.006:.012; p.z+=(K==='berserk'?.6:.25)+pre*(K==='berserk'?2:1);",
       "p.a+=K==='shadow'?.006:K==='ego'?.028:.012; p.z+=K==='ego'?.05:(K==='berserk'?.6:.25)+pre*(K==='berserk'?2:K==='moon'?1.6:1);")
    rp("      else { g2.fillStyle=`rgba(${T.pt},${.25+.6*(1-p.r)})`; g2.beginPath(); g2.arc(x,y-p.z,p.s,0,6.2832); g2.fill(); } return true; });",
       "      else if(K==='moon'){ if(rnd()<.85){ const q=Math.max(2,Math.round(p.s*1.8)); g2.fillStyle=`rgba(${T.pt},${(.3+.6*(1-p.r))*(.5+.5*rnd())})`; g2.fillRect(Math.round(x/3)*3,Math.round((y-p.z)/3)*3,q,q); } }\n"
       "      else if(K==='ego'){ g2.fillStyle=`rgba(${EGO_C[p.c]},${.3+.6*(1-p.r)})`; g2.beginPath(); g2.arc(x,y-p.z,p.s*1.2,0,6.2832); g2.fill(); }\n"
       "      else { g2.fillStyle=`rgba(${T.pt},${.25+.6*(1-p.r)})`; g2.beginPath(); g2.arc(x,y-p.z,p.s,0,6.2832); g2.fill(); } return true; });")
    # 오르는 빛줄기 · 빛기둥은 기본 · 버서커만. 새 두 클래스는 따로
    rp("if(t>1800&&t<3100&&K!=='shadow'&&K!=='avenger'){", "if(t>1800&&t<3100&&K!=='shadow'&&K!=='avenger'&&K!=='moon'&&K!=='ego'){")
    rp("    if(K!=='shadow'&&K!=='avenger'&&t>2650){",
       """    // 문 캔서: 깜박이는 세로 줄 빛(데이터 기둥)과 위에서 아래로 훑는 줄
    if(K==='moon'&&t>2650&&t<4600){ const k=t<2800?ss((t-2650)/150):1-ss((t-2950)/1500); g2.globalCompositeOperation='lighter';
      for(let i=0;i<13;i++){ const h1=((i*7919)%97)/97, h2=((i*104729)%89)/89; if(rnd()<.25) continue; const x=G.cx+(h1-.5)*G.rx*(.25+.75*k), w=1.5+h2*12*k;
        const gr=g2.createLinearGradient(0,0,0,G.cy); gr.addColorStop(0,`rgba(${T.pl},0)`); gr.addColorStop(.5,`rgba(${T.pl},${.55*k})`); gr.addColorStop(1,`rgba(${T.pt},${.75*k})`); g2.fillStyle=gr; g2.fillRect(x-w/2,0,w,G.cy+G.ry*.3); }
      if(t>2800&&t<3700){ const yy=H*eo((t-2800)/900); g2.fillStyle=`rgba(${T.pl},${.5*(1-ss((t-3300)/400))})`; g2.fillRect(0,yy,W,2); }
      g2.globalCompositeOperation='source-over'; }
    // 얼터 에고: 세 빛깔의 띠가 서로 감기며 솟는다
    if(K==='ego'&&t>1900&&t<4500){ const k=t<2800?ss((t-1900)/900):1-ss((t-3000)/1500), top=G.cy-(G.cy-ey+D*.6)*eo((t-1900)/1000);
      g2.globalCompositeOperation='lighter'; g2.lineCap='round'; g2.shadowBlur=14;
      for(let j=0;j<3;j++){ g2.strokeStyle=`rgba(${EGO_C[j]},${.7*k})`; g2.shadowColor=`rgba(${EGO_C[j]},.9)`; g2.lineWidth=2.6; g2.beginPath();
        for(let y=G.cy;y>=top;y-=5){ const u=(G.cy-y)/Math.max(1,G.cy-top), x=G.cx+Math.sin(y*.024-t*.007+j*2.094)*G.rx*.26*(1-.6*u); y===G.cy?g2.moveTo(x,y):g2.lineTo(x,y); } g2.stroke(); }
      g2.shadowBlur=0; g2.globalCompositeOperation='source-over'; }
    if(K!=='shadow'&&K!=='avenger'&&K!=='moon'&&K!=='ego'&&t>2650){""")
    # 터짐: 얼터 에고는 물결 · 유리 조각
    rp("      if(K==='berserk') for(let k=0;k<34;k++){",
       "      if(K==='ego'){ for(let k=0;k<3;k++) ripples.push({r:.15,d:k*180,l:1}); for(let k=0;k<26;k++){ const a=rnd()*6.2832, r=.1+rnd()*.5; rocks.push({x:G.cx+Math.cos(a)*G.rx*r,y:G.cy+Math.sin(a)*G.ry*r-D*.2,vx:(rnd()-.5)*9,vy:-(3+rnd()*7),s:3+rnd()*6,r:rnd()*6,vr:(rnd()-.5)*.2,g:1,c:k%3}); } }\n"
       "      if(K==='berserk') for(let k=0;k<34;k++){")
    rp("burst=burst.filter(p=>{ p.x+=p.vx; p.y+=p.vy; p.vy*=.985; p.l-=.006; if(p.l<=0) return false; g2.fillStyle=`rgba(${T.pt},${.8*p.l})`; g2.beginPath(); g2.arc(p.x,p.y,p.s,0,6.2832); g2.fill(); return true; });",
       "burst=burst.filter(p=>{ p.x+=p.vx; p.y+=p.vy; p.vy*=.985; p.l-=.006; if(p.l<=0) return false; g2.fillStyle=`rgba(${K==='ego'?EGO_C[Math.floor(p.s*7)%3]:T.pt},${.8*p.l})`;\n"
       "      if(K==='moon'){ if(rnd()<.8){ const q=Math.round(p.s*2); g2.fillRect(Math.round(p.x/3)*3,Math.round(p.y/3)*3,q,q); } } else { g2.beginPath(); g2.arc(p.x,p.y,p.s,0,6.2832); g2.fill(); } return true; });\n"
       "    ripples=ripples.filter(p=>{ if(t-2800<p.d) return true; p.r+=.012; p.l-=.008; if(p.l<=0) return false; g2.strokeStyle=`rgba(${T.pl},${.6*p.l})`; g2.lineWidth=1.6; g2.beginPath(); g2.ellipse(G.cx,G.cy,G.rx*p.r,G.ry*p.r,0,0,6.2832); g2.stroke(); return true; });")
    rp("g2.fillStyle='#3a2622'; g2.strokeStyle=`rgba(${T.gl},.7)`;",
       "g2.fillStyle=p.g?`rgba(${EGO_C[p.c]},.28)`:'#3a2622'; g2.strokeStyle=p.g?`rgba(${T.pl},.8)`:`rgba(${T.gl},.7)`;")
    rp("p.vy+=.45; p.r+=p.vr;", "p.vy+=p.g?.22:.45; p.r+=p.vr;")
    # 섬광
    rp("    else { fl.style.background=K==='berserk'?",
       "    else if(K==='moon'){ fl.style.background='repeating-linear-gradient(0deg,rgba(255,255,255,0) 0 2px,rgba(40,0,56,.4) 2px 3px),radial-gradient(ellipse at 50% 38%,#ffffff 0%,#f4b0ff 30%,rgba(200,80,230,0) 75%)'; fl.style.opacity=t<2780?0:t<2850?(t-2780)/70*.95:t<2990?.95*(1-ss((t-2850)/140)):t<3060?.55:.55*(1-ss((t-3060)/600)); }\n"
       "    else if(K==='ego'){ fl.style.background='radial-gradient(ellipse at 50% 55%,#f6fbff 0%,#b8dcff 32%,rgba(150,190,255,0) 75%)'; fl.style.opacity=t<2780?0:t<2860?(t-2780)/80*.9:.9*(1-ss((t-2860)/800)); }\n"
       "    else { fl.style.background=K==='berserk'?")
    # 초상: 문 캔서는 위에서 아래로 한 줄씩 그려지고 색이 어긋났다 맞춰진다. 얼터 에고는 두 잔상이 하나로 겹친다
    rp("      fly.style.opacity=K==='shadow'?ss((t-2850)/500):ss((t-2760)/250);",
       "      fly.style.opacity=K==='shadow'?ss((t-2850)/500):ss((t-2760)/250);\n"
       "      fly.style.clipPath=K==='moon'&&t<3400?`inset(0 0 ${100-Math.floor(ss((t-2790)/560)*14)/14*100}% 0)`:'';")
    rp("      :`brightness(${1+2.2*(1-col)}) ${K==='berserk'?`sepia(${.6*(1-col)}) hue-rotate(${-25*(1-col)}deg) `:''}saturate(${.4+.6*col}) drop-shadow(",
       "      :`brightness(${1+2.2*(1-col)}) ${K==='berserk'?`sepia(${.6*(1-col)}) hue-rotate(${-25*(1-col)}deg) `:''}saturate(${.4+.6*col}) ${K==='moon'?(d=>`drop-shadow(${-d}px 0 rgba(255,60,200,.85)) drop-shadow(${d}px 0 rgba(80,220,255,.85)) `)(Math.round(9*(1-ss((t-2800)/800))*(rnd()<.7?1:2))):K==='ego'?(d=>`drop-shadow(${-d}px 0 rgba(${EGO_C[1]},.75)) drop-shadow(${d}px 0 rgba(${EGO_C[0]},.75)) `)(Math.round(18*(1-ss((t-2780)/1000)))):''}drop-shadow(")
    rp("const n=Math.floor(2+pre*(K==='shadow'?3:6));", "const n=Math.floor(2+pre*(K==='shadow'?3:K==='ego'?10:6));")
    rp('"j_summon_avenger":{"d":8.2},', '"j_summon_avenger":{"d":8.2},"j_summon_moon":{"d":8.2},"j_summon_ego":{"d":8.2},')
    open(P, 'w', encoding='utf-8').write(s); print('sfx', 'miss', miss)
