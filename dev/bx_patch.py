"""② 비스트 위기 본체를 게임 파일에 넣는다. 사용: python3 bx_patch.py <game.html>"""
import sys, os, re, json
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
import i18n

CORE = open(os.path.join(D0, 'bx_core.js'), encoding='utf-8').read()

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)

    # 1) 본체: 위기 블록 바로 뒤
    rp("  function dayStart(){\n", CORE + "\n  function dayStart(){\n")

    # 2) 능력치: 수녀(숨김 보정) · 봉인 중의 BB(▲2) · 센티넬(KP) · 키아라(끌어올리지 않음)
    rp("""    if(p.cx==='shadow') o=o.map((r,i)=>i===0||i===2?rankShift(r,1):i===4?'E':r); else if(p.cx==='boss') o=cxBossStats(h);""",
       """    if(p.bxNun&&!p.bxFake) o=bxNunStats(p,o);
    if(p.cx==='sent') o=bxSentStats(p,o);
    if(p.cx==='shadow') o=o.map((r,i)=>i===0||i===2?rankShift(r,1):i===4?'E':r); else if(p.cx==='boss') o=p.bx?bxKiaraStats(h.s):cxBossStats(h);
    if((p.cx==='bb'||p.bxBB)&&bxSealing()) o=o.map(r=>r==='-'?r:r+' ▲2');""")
    rp("""    const out=h.s.map((r,i)=> rankShift(r, i<4? m[i]+(starved&&(i===0||i===1)?-1:0) : luck));
    return {p:up(npCurse('me',out)),tier:t,starved,luck};""",
       """    let out=h.s.map((r,i)=> rankShift(r, i<4? m[i]+(starved&&(i===0||i===1)?-1:0) : luck));
    if(h.id==='bb'&&bxSealing()&&!sb) out=out.map(r=>r==='-'?r:r+' ▲2'); // 문 셀의 백업
    return {p:up(npCurse('me',out)),tier:t,starved,luck};""")
    # 3) 판정: 키아라 (나와의 결전 −56 · NPC −25)
    rp("""if(p.cx==='boss'&&bt&&W().battle.ctx.descent&&!_key) v+=CXB.desc+cxBossAdj(W().battle.ctx); else if(p.cx==='boss'&&!bt) v+=CXB.nd;""",
       """if(p.bx) v+=bxPow(p,!!bt); else if(p.cx==='boss'&&bt&&W().battle.ctx.descent&&!_key) v+=CXB.desc+cxBossAdj(W().battle.ctx); else if(p.cx==='boss'&&!bt) v+=CXB.nd;""")
    # 4) 로고스 이터: 주는 피해 ×1.25
    rp("""*npTakeM(b,'me')*npDealM(b,'en');""", """*npTakeM(b,'me')*npDealM(b,'en')*(e.bx?BXK.logos:1);""")
    rp("""const dmgSp=x=>{ const id=x.h.id, o=x.o.h, hp=x.p.hp; let m=1;""", """const dmgSp=x=>{ const id=x.h.id, o=x.o.h, hp=x.p.hp; let m=x.p.bx?BXK.logos:1;""")
    # 5) NPC끼리의 싸움: 수녀 · 봉인 중의 BB는 쓰러지지 않는다 / 키아라의 마지막 밤은 끝까지 / 보구 회복 / 암살 불가
    rp("""    const hit=(x,v)=>{ v=Math.max(0,v*K); x.p.hp=clamp(x.p.hp-v);""",
       """    const keep=x=>x.p.bxNun&&!x.p.bxFake||(x.p.cx==='bb'||x.p.bxBB)&&bxSealing();
    const hit=(x,v)=>{ v=Math.max(0,v*K); if(keep(x)) v=Math.min(v,Math.max(0,x.p.hp-1)); x.p.hp=clamp(x.p.hp-v);""")
    rp("""      if(a.hp<=0||b.hp<=0) break;
      if(!final){ const fl=""", """      if(a.hp<=0||b.hp<=0) break;
      if([A,B].some(x=>keep(x)&&x.p.hp<30)) break;
      if(!final&&!(a.bxHunt||b.bxHunt)){ const fl=""")
    rp("""maxR=final?12:a.cx||b.cx?40:ri(5,6);""", """maxR=final?(a.bx||b.bx?99:12):a.bxHunt||b.bxHunt?12:a.cx||b.cx?40:ri(5,6);""")
    rp("""    if(final) lose.hp=0;""", """    if(final&&!(lose.bxNun&&!lose.bxFake)) lose.hp=0;""")
    rp("""      // 5) 합이 끝날 때\n""", """      if(a.bx||b.bx) bxDuelRound(A,B,r,h0,fire,final,hit); // 키아라전: 호위 · 함께 간 조\n      // 5) 합이 끝날 때\n""")
    rp("""const pw=x=>{ let v=npcPower(x.p,false,r,x===A&&init)+""", """const pw=x=>{ let v=npcPower(x.p,false,r,x===A&&init)+(x.bxCh&&x.bxCh.r===r?x.bxCh.v:0)+""")
    rp("""      for(const x of [A,B]) if(fire.get(x)&&x.h.id==='georgios'&&x.o.p.hp<h0.get(x.o)) x.o.dragon=1;""",
       """      for(const x of [A,B]) if(fire.get(x)&&x.h.id==='georgios'&&x.o.p.hp<h0.get(x.o)) x.o.dragon=1;
      for(const x of [A,B]) if(fire.get(x)&&x.p.bx) bxNpHeal(x.p);""")
    rp("""if(asnWin||x.h.cls!=='shadow'||x.asnTried||!x.p.master||!x.o.p.master) continue;""",
       """if(asnWin||x.h.cls!=='shadow'||x.asnTried||!x.p.master||!x.o.p.master||x.o.p.bxNun) continue;""")
    # 6) 밤: 수녀 조의 사냥 · 수녀의 마스터는 노릴 수 없다
    rp("""    const done=new Set(); let reported=0;""", """    const done=new Set(); let reported=0; bxNunHunt(avail,done);""")
    rp("""if(lose.master&&ch(mHunt(win))){""", """if(lose.master&&!lose.bxNun&&ch(mHunt(win))){""", 2)
    rp("""    const others=a=>cs.filter(x=>x!==a&&x.alive&&x.master&&!(x.ally&&a.ally));""",
       """    const others=a=>cs.filter(x=>x!==a&&x.alive&&x.master&&!(x.ally&&a.ally)&&!x.bxNun);""")
    # 7) 플레이어 전투: 물러나는 수녀 · BB전
    rp("""    if(w.hp<=0&&e.hp<=0){
      log(pickNR([`${mN}${J(mN,과)} ${eN}${J(eN,이)} 동시에 무너졌다.""", """    if(bxHold(b)) return endBattle();
    if(w.hp<=0&&e.hp<=0){
      log(pickNR([`${mN}${J(mN,과)} ${eN}${J(eN,이)} 동시에 무너졌다.""")
    rp("""    const intro = ctx.cx? (e.cx==='boss'?""", """    const intro = BXW()&&bxIntro(e,ctx)? bxIntro(e,ctx) : ctx.cx? (e.cx==='boss'?""")
    rp("w.myOut={d:w.day,tod:w.tod,why:e?`${cn(e)} 조와 싸우다 쓰러졌다`:'쓰러졌다',", "w.myOut={d:w.day,tod:w.tod,why:e?(e.bx?'셋쇼인 키아라와 싸우다 쓰러졌다':e.cx==='sent'?'센티넬과 싸우다 쓰러졌다':`${cn(e)} 조와 싸우다 쓰러졌다`):'쓰러졌다',")
    # 8) 이름 · 말
    rp("""  const cn=x=>{ if(x&&x.cx) return (x.cx==='boss'?'검은 성배의 ':'검은 그림자의 ')+CLS[x.cls].n;""",
       """  const cn=x=>{ if(x&&x.cx==='sent') return '센티넬 '+CLS[x.cls].n; if(x&&x.cx==='bb') return CLS[x.cls].n; if(x&&x.bx) return CLS[x.cls].n; if(x&&x.cx) return (x.cx==='boss'?'검은 성배의 ':'검은 그림자의 ')+CLS[x.cls].n;""")
    rp("""    if(e.cx){ if(first||ch(.4)) log(pickNR(CX_LINE[e.cx],'cx'+e.cx).slice(1,-1),'enemy'); return; }""",
       """    if(e.cx){ const k_=e.bx?'kiara':e.cx; if(CX_LINE[k_]&&(first||ch(.4))) log(pickNR(CX_LINE[k_],'cx'+k_).slice(1,-1),'enemy'); return; }""")
    rp("""  const cxBossLine=(u,k)=>{""", """  CX_LINE.sent=['(센티넬은 말이 없었다. 어디선가 단 냄새가 났다.)','(텅 빈 눈이 이쪽을 보았다. 그 너머에서 누군가 웃고 있는 것 같았다.)','(입술이 움직였지만, 나온 것은 다른 사람의 숨소리였다.)'];
  CX_LINE.bb=['(BB가 지휘봉을 빙글 돌렸다. “자, 한 곡 더 할까요?”)','(BB는 웃고 있었지만, 눈은 도시 쪽을 보고 있었다.)','(“선배, 생각보다 끈질기네요.”)'];
  CX_LINE.kiara=['(키아라가 두 손을 모았다. “괴로워하지 마세요. 곧 편안해집니다.”)','(“아아, 그 눈빛. 정말로 맛있어 보이네요.”)','(키아라의 웃음소리가 도시 전체에서 동시에 울렸다.)'];
  CX_BOSS_LINE.kiara={new:'어서 오세요. 이 도시는 이미 제 안에 있답니다. 남은 것은 당신뿐이에요.',final:'마지막 밤이네요. 모두 함께 녹아드는 것만큼 큰 구원은 없지요.',p2:'아아, 이 아픔마저 이토록 달콤하다니요.'};
  const cxBossLine=(u,k)=>{""")
    # 9) 키아라 데이터 (소환되지 않는 보스 · 도감 밖)
    KI = """  // ---- 셋쇼인 키아라 (비스트 Ⅲ/R · 보스 전용, 소환되지 않는다) ----
  H_BY.kiara={id:'kiara',fem:1,cls:'beast',name:'셋쇼인 키아라',title:'비스트 Ⅲ/R',from:'달의 뒷면',s:['C','B','EX','EX','A'],art:{n:'쾌락천・태장만다라',d:'모든 것을 녹이는 쾌락의 바다'},traits:['야망'],wish:'모든 것을 녹여 자신의 쾌락으로 삼는 것',relic:'',frags:[]};
  ARTX.kiara={n:'쾌락천・태장만다라',r:'EX',k:'대인보구',x:'닿는 모든 것을 녹여 단꿈으로 바꾼다. 쓸 때마다 키아라의 상처가 아문다.'};
  SK.kiara=[['짐승의 권능','A'],['단독현현','B'],['로고스 이터','A'],['네가 세이버','A'],['카르마 파지','EX'],['만색유체','EX']];
  SKX['짐승의 권능']=SKX['짐승의 권능']||{k:'power',x:'인류를 해치는 짐승의 힘'}; SKX['네가 세이버']=SKX['네가 세이버']||{k:'power',x:'구세주를 거꾸로 선 자. 짐승의 권능을 키우고 마주한 자를 매료한다'};
  SKX['단독현현']=SKX['단독현현']||{k:'ind',x:'홀로 나타나 쓰러져도 한 번 다시 빚어진다'}; SKX['로고스 이터']=SKX['로고스 이터']||{k:'div',x:'인간을 먹는 자. 주는 피해가 커진다'};
  SKX['카르마 파지']=SKX['카르마 파지']||{k:'regen',x:'다섯 감각의 쾌락을 떼어 남에게 심는다'}; SKX['만색유체']=SKX['만색유체']||{k:'mr',x:'마주한 자의 정신을 단꿈으로 흔든다'};
  NPR.kiara={r:'A',s:'a'}; MAGIC_X.kiara=1;
"""
    rp("  // ---- 에필로그 연작", KI + "  // ---- 에필로그 연작")
    # 10) 업적 · 에필로그
    rp("""{id:'cxwinter',cat:'성배전쟁의 끝',n:'검은 겨울',d:'성배가 검게 물든 성배전쟁을 겪었다',t:()=>!!WV().crisis&&WV().crisis.stage>=2}""",
       """{id:'cxwinter',cat:'성배전쟁의 끝',n:'검은 겨울',d:'성배가 검게 물든 성배전쟁을 겪었다',t:()=>!!WV().crisis&&WV().crisis.type!=='beast'&&WV().crisis.stage>=2},
    {id:'bxmoon',cat:'성배전쟁의 끝',n:'달로 간 잔',d:'셋쇼인 키아라를 쓰러뜨렸다. 성배는 BB와 함께 달로 갔다',t:()=>S.flags.bxEnd==='me'},
    {id:'bxleft',cat:'성배전쟁의 끝',n:'남겨진 사람',d:'키아라에게 지고 살아남았다',t:()=>!!S.flags.bxDream&&!S.dead},
    {id:'bxfive',cat:'성배전쟁의 끝',n:'다섯 조각',d:'카르마 파지 다섯을 모두 거두었다',t:()=>!!WV().crisis&&WV().crisis.type==='beast'&&(WV().crisis.kpGot||0)>=5}""")
    rp("""    {id:'arc_crest',arc:1,w:2,""", """    {id:'bx_sweet',w:2,c:()=>!!S.flags.bxDream&&S.year-S.warYear>=2,f:()=>decide({title:'단맛',body:'그 겨울의 단맛이 문득 혀끝에 돌아왔다. 깨어나지 않는 꿈으로 돌아가고 싶다는 생각이 든다.',choices:[
      {t:'눈을 감는다',f:()=>{ add({will:-4}); return '한참 뒤 눈을 떴을 때, 무엇을 보았는지 기억나지 않았다. 단맛만 오래 남았다.'; }},
      {t:'뿌리친다',auto:true,f:()=>{ add({will:3}); return '찬물에 얼굴을 씻었다. 단맛이 조금씩 옅어졌다.'; }}]})},
    {id:'bx_moon',w:1.5,c:()=>!!S.flags.bxEnd&&S.year-S.warYear>=1,f:()=>decide({title:'달의 소식',body:'달이 유난히 밝은 밤, 휴대폰에 발신자 없는 메시지가 왔다. “잘 지내요? 이쪽은 성배랑 둘이서 좀 심심해요. 가끔은 위를 봐 줘요. ―BB”',choices:[
      {t:'달을 올려다본다',auto:true,f:()=>{ add({will:2}); return '달 한가운데가 한 번, 윙크하듯 깜박였다.'; }}]})},
    {id:'arc_crest',arc:1,w:2,""")
    # 11) BB의 조사: 비비 → BB는 · BB가
    rp("""  const lastH=w=>{for(let i=w.length-1;i>=0;i--){const c=w.charCodeAt(i);if(c>=0xac00&&c<=0xd7a3)return c;if(/[0-9A-Za-z]/.test(w[i]))return 0;}return 0};""",
       """  const lastH=w=>{for(let i=w.length-1;i>=0;i--){const c=w.charCodeAt(i);if(c>=0xac00&&c<=0xd7a3)return c;if(/[0-9A-Za-z]/.test(w[i]))return /BB$/.test(w.slice(0,i+1))?0xBE44:0;}return 0};""")

    import bx_tr
    DD=[x for x in bx_tr.D]+[x for x in bx_tr.T if '{' not in x[0]]; TT=[x for x in bx_tr.T if '{' in x[0]]
    s, nd, nt = i18n.add(s, DD, TT)
    open(P, 'w', encoding='utf-8').write(s)
    print(os.path.basename(P), 'miss', miss, 'tr', nd, nt)
