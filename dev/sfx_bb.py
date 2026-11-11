"""BB 전용 소환 연출 (11-12 시안 3): 평범한 소환을 가로챈다 → 달 위의 얼굴 없는 그림자
실제 시간(tr) 기준: 0~2.6초 기본 소환 그대로(금빛 마법진이 다 그려지고 빛줄기가 오름) · 2.6~3.3초 금빛이 어긋나며 보랏빛으로 · 2.75초~ 달 ·
3.2초~ 달 위의 그림자 · 3.75~4.1초 지시봉 반짝임과 톡 · 4.1초 터짐 · 8.2초 끝. 나머지 연출은 기존 시간표(t)를 1.3초 늦춰 쓴다(t = tr−1.3초, 앞 2.6초는 절반 빠르기).
문 캔서 클래스가 아니라 BB(id)에게만 붙는다. sfx_apply.py 다음에 쓴다. 사용: python3 sfx_bb.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 테마는 복사본으로 쓴다(BB는 프레임마다 금빛 → 보랏빛으로 바뀐다)
    rp("  const K=SFX_TH[h.cls]?h.cls:'base', T=SFX_TH[K];",
       "  const K=SFX_TH[h.cls]?h.cls:'base', T0=SFX_TH[K], T=Object.assign({},T0), BBX=h.id==='bb', TB=SFX_TH.base; if(BBX) T.sound='j_summon_bb';\n"
       "  const mixc=(a,b,m)=>{ const A=a.split(',').map(Number), B=b.split(',').map(Number); return A.map((v,i)=>Math.round(v+(B[i]-v)*m)).join(','); };")
    rp("const sumSndK=()=>{ const h=Sim.hero(); return (SFX_TH[h&&h.cls]||SFX_TH.base).sound; };",
       "const sumSndK=()=>{ const h=Sim.hero(); if(h&&h.id==='bb') return 'j_summon_bb'; return (SFX_TH[h&&h.cls]||SFX_TH.base).sound; };")
    # 프레임 시작: BB는 1.35~2.0초에 금빛에서 보랏빛으로
    rp("    const pre=ss((t-200)/2600), post=t<2800?0:1-ss((t-4200)/2000), glow=t<2800?.15+.6*pre:.55+.45*post, out=1-ss((t-5800)/650);",
       "    const pre=ss((t-200)/2600), post=t<2800?0:1-ss((t-4200)/2000), glow=t<2800?.15+.6*pre:.55+.45*post, out=1-ss((t-5800)/650);\n"
       "    if(BBX){ const m=ss((t-1350)/650); for(const k of ['ln','gl','pt','pl']) T[k]=mixc(TB[k],T0[k],m); }")
    # 달은 가로챈 뒤에 떠오르고, 그 위에 그림자가 선다
    rp("  function moonBack(t,pre,post,out){ const a=(t<2800?.1+.38*pre:.45*post+.4*(1-ss((t-2800)/260)))*out; if(a<=0) return;",
       """  // BB 그림자: 단위 좌표(키 1, 위 가운데가 0,0). 원작 카드 그림을 옮기지 않고 긴 머리 · 긴 소매 코트 · 지시봉만으로 새로 그린 모양
  const BBS=[[[-.08,.04],[-.13,.2],[-.17,.45],[-.19,.68],[-.12,.62],[-.08,.3],[.08,.3],[.12,.62],[.19,.68],[.17,.45],[.13,.2],[.08,.04]], // 긴 머리
    [[-.1,.19],[-.2,.5],[-.26,.82],[-.07,.78],[-.05,.35]], [[.1,.19],[.2,.5],[.26,.82],[.07,.78],[.05,.35]],                     // 코트 두 자락
    [[-.06,.19],[.06,.19],[.09,.48],[.12,.58],[-.12,.58],[-.09,.48]],                                                              // 몸 · 치마
    [[-.085,.58],[-.035,.58],[-.04,.97],[-.075,.97]], [[.035,.58],[.085,.58],[.075,.97],[.04,.97]],                               // 다리
    [[-.1,.2],[-.24,.34],[-.36,.42],[-.4,.5],[-.3,.5],[-.2,.42],[-.1,.32]],                                                         // 지시봉을 든 소매
    [[.1,.21],[.18,.4],[.27,.6],[.2,.62],[.13,.5],[.08,.3]],                                                                        // 내린 소매
    [[.03,.02],[.16,-.05],[.15,.06]], [[.03,.04],[.11,.13],[.02,.11]]];                                                             // 머리 리본
  BBS.forEach(q=>{ let A=0; q.forEach(([x1,y1],i)=>{ const [x2,y2]=q[(i+1)%q.length]; A+=x1*y2-x2*y1; }); if(A<0) q.reverse(); }); // 감는 방향을 맞춰 겹친 곳이 비지 않게
  const BBH=()=>moonR*1.75, BBY=()=>moonY-moonR*.85, BBP=(u,v)=>[cx+u*BBH(),BBY()+v*BBH()], BBT=[-.6,.16]; // 지시봉 끝
  function bbShadow(t){ const a=ss((t-1900)/500)*(t<2800?1:1-ss((t-2800)/280)); if(a<=0) return;
    const P=new Path2D(); for(const poly of BBS){ poly.forEach(([u,v],i)=>{ const [x,y]=BBP(u,v); i?P.lineTo(x,y):P.moveTo(x,y); }); P.closePath(); }
    { const [x,y]=BBP(0,.085); P.moveTo(x+.07*BBH(),y); P.arc(x,y,.07*BBH(),0,6.2832); }
    g.save(); g.fillStyle=`rgba(16,5,26,${.92*a})`; g.shadowColor=`rgba(${T.gl},${.8*a})`; g.shadowBlur=14; g.fill(P); g.shadowBlur=0;
    const [x1,y1]=BBP(-.37,.46), [x2,y2]=BBP(BBT[0],BBT[1]); g.strokeStyle=`rgba(16,5,26,${.92*a})`; g.lineWidth=Math.max(1.5,BBH()*.008); g.beginPath(); g.moveTo(x1,y1); g.lineTo(x2,y2); g.stroke(); g.restore(); }
  function bbTap(t){ if(t<2450||t>3000) return; const [x,y]=BBP(BBT[0],BBT[1]), k=ss((t-2450)/300), f=t<2780?1:1-ss((t-2780)/220), r=4+14*k;
    g2.save(); g2.globalCompositeOperation='lighter'; g2.strokeStyle=`rgba(${T.pl},${.9*f})`; g2.lineWidth=1.4; g2.shadowColor=`rgba(${T.gl},1)`; g2.shadowBlur=12;
    g2.beginPath(); g2.moveTo(x-r,y); g2.lineTo(x+r,y); g2.moveTo(x,y-r); g2.lineTo(x,y+r); g2.stroke();
    if(t>2700){ const q=eo((t-2700)/300); g2.strokeStyle=`rgba(${T.pl},${.8*(1-q)})`; g2.beginPath(); g2.arc(x,y,6+q*moonR*.9,0,6.2832); g2.stroke(); } g2.restore(); }
  function moonBack(t,pre,post,out){ const a=(t<2800?.1+.38*pre:.45*post+.4*(1-ss((t-2800)/260)))*out*(BBX?ss((t-1450)/700):1); if(a<=0) return;""")
    # 달을 그린 뒤 그림자
    rp("    const hz=g.createRadialGradient(cx,y,moonR*.9,cx,y,moonR*1.8); hz.addColorStop(0,`rgba(${T.gl},${.25*a})`); hz.addColorStop(1,`rgba(${T.gl},0)`); g.fillStyle=hz; g.beginPath(); g.arc(cx,y,moonR*1.8,0,6.2832); g.fill(); }",
       "    const hz=g.createRadialGradient(cx,y,moonR*.9,cx,y,moonR*1.8); hz.addColorStop(0,`rgba(${T.gl},${.25*a})`); hz.addColorStop(1,`rgba(${T.gl},0)`); g.fillStyle=hz; g.beginPath(); g.arc(cx,y,moonR*1.8,0,6.2832); g.fill();\n"
       "    if(BBX) bbShadow(t); }")
    # 가로채는 순간의 어긋남
    rp("  function moonGlitch(t,pre){ const I=t<2800?(t>1300?.7*pre*pre:0):t<3350?1-ss((t-2800)/550):0;",
       "  function moonGlitch(t,pre){ let I=t<2800?(t>1300?.7*pre*pre:0):t<3350?1-ss((t-2800)/550):0; if(BBX&&t>1300&&t<2300) I=Math.max(I,.95*ss((t-1300)/120)*(1-ss((t-1750)/550)));")
    # 빛가루: 가로채기 전에는 둥근 금빛
    rp("      else if(K==='moon'){ if(rnd()<.85){", "      else if(K==='moon'&&!(BBX&&t<1500)){ if(rnd()<.85){")
    # 지시봉 반짝임 · 터질 때 그림자가 네모 조각으로
    rp("    g2.globalCompositeOperation='source-over';\n    // 어벤저:", "    g2.globalCompositeOperation='source-over';\n    if(BBX) bbTap(t);\n    // 어벤저:")
    rp("      if(K==='ego'){ for(let k=0;k<3;k++) ripples.push(",
       "      if(BBX) for(let k=0;k<90;k++){ const u=(rnd()-.5)*.5, v=.05+rnd()*.9, [x,y]=BBP(u,v); burst.push({x,y,vx:u*8+(rnd()-.5)*2,vy:-(.5+rnd()*2.5),s:1+rnd()*2,l:1}); }\n"
       "      if(K==='ego'){ for(let k=0;k<3;k++) ripples.push(")
    rp('"j_summon_moon":{"d":8.2},', '"j_summon_moon":{"d":8.2},"j_summon_bb":{"d":8.2},')
    # 시간: BB는 앞 2.6초를 기본 소환으로 길게 보여 준다
    rp("function frame(now){ if(done) return; const t=now-t0;", "function frame(now){ if(done) return; const tr=now-t0, t=BBX?(tr<2600?tr*.5:tr-1300):tr;")
    rp("else circle(t,glow);", "else circle(BBX?tr:t,glow);")
    rp("    const pre=ss((t-200)/2600), post=", "    const pre=BBX?ss((tr-200)/3900):ss((t-200)/2600), post=")
    rp("if(t>1800&&t<3100&&K!=='shadow'&&K!=='avenger'&&K!=='moon'&&K!=='ego'){ const k=ss((t-1800)/1000);",
       "if((t>1800&&t<3100&&K!=='shadow'&&K!=='avenger'&&K!=='moon'&&K!=='ego')||(BBX&&tr>1500&&tr<3100)){ const k=BBX?ss((tr-1500)/900)*(1-ss((tr-2550)/450)):ss((t-1800)/1000);")
    # 가로챌 때 화면 전체가 치직인다: 맨 위 캔버스에 잡음 · 굵은 줄 띠 · 흐르는 줄 · 한 프레임 암전, 그리고 화면이 덜컥 어긋남
    rp("  for(const c of [c1,c2]){ c.width=W*dpr; c.height=H*dpr; } g.setTransform(dpr,0,0,dpr,0,0); g2.setTransform(dpr,0,0,dpr,0,0);",
       "  for(const c of [c1,c2]){ c.width=W*dpr; c.height=H*dpr; } g.setTransform(dpr,0,0,dpr,0,0); g2.setTransform(dpr,0,0,dpr,0,0);\n"
       "  const c3=BBX?document.createElement('canvas'):null, g3=c3&&c3.getContext('2d'), nz=BBX?document.createElement('canvas'):null, nzx=nz&&nz.getContext('2d');\n"
       "  if(c3){ c3.width=W*dpr; c3.height=H*dpr; g3.setTransform(dpr,0,0,dpr,0,0); c2.after(c3); nz.width=192; nz.height=108; }")
    rp("  const pf=fly.querySelector('.pf');",
       """  function bbStatic(tr){ g3.clearRect(0,0,W,H); let I=ss((tr-2560)/110)*(1-ss((tr-2980)/300))*(rnd()<.35?.35:.8); if(Math.abs(tr-2180)<50||Math.abs(tr-2440)<40) I=Math.max(I,.3); if(I<=0) return;
    const d=nzx.createImageData(192,108), a=d.data; for(let i=0;i<a.length;i+=4){ const v=rnd()*255; a[i]=v; a[i+1]=v*(.85+.3*rnd()); a[i+2]=v; a[i+3]=255; } nzx.putImageData(d,0,0);
    g3.save(); g3.imageSmoothingEnabled=false; g3.globalAlpha=.5*I; g3.drawImage(nz,0,0,W,H); g3.globalAlpha=1;
    for(let k=0;k<3+Math.floor(6*I);k++){ const y=rnd()*H, hh=2+rnd()*26*I; g3.fillStyle=rnd()<.5?`rgba(255,255,255,${.28*I})`:`rgba(0,0,0,${.65*I})`; g3.fillRect(0,y,W,hh); }
    const ry=(tr*.9)%H; g3.fillStyle=`rgba(0,0,0,${.5*I})`; g3.fillRect(0,ry,W,H*.07); g3.fillStyle=`rgba(255,255,255,${.18*I})`; g3.fillRect(0,ry-2,W,2);
    if(I>.6&&rnd()<.1){ g3.fillStyle='rgba(0,0,0,.88)'; g3.fillRect(0,0,W,H); }
    g3.restore(); }
  const pf=fly.querySelector('.pf');""")
    rp("    if(BBX) bbTap(t);", "    if(BBX){ bbTap(t); bbStatic(tr); }")
    rp("if(K==='moon'&&t>2780&&t<3300&&rnd()<.45) sx=Math.round((rnd()-.5)*18);",
       "if(K==='moon'&&t>2780&&t<3300&&rnd()<.45) sx=Math.round((rnd()-.5)*18);\n    if(BBX&&tr>2560&&tr<3200&&rnd()<.6){ sx=Math.round((rnd()-.5)*34); sy=Math.round((rnd()-.5)*10); }")
    rp('"j_summon_bb":{"d":8.2}', '"j_summon_bb":{"d":9.5}')
    open(P, 'w', encoding='utf-8').write(s); print('sfx_bb', 'miss', miss)
