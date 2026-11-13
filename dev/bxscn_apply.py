"""11-13: 비스트 Ⅲ/R 위기의 화면 표시 · 시나리오 설정 분리.
① 현황판 위기 줄 · 조 목록 칸 이름을 비스트용으로(반전 전 「봉인된 성배」/「비어 있는 성배」, 강림 뒤 「비스트 Ⅲ/R」), 이름표 센티넬 · BB · 비스트
② 화면 효과: 검은 성배 효과(cx1~3)는 검은 성배에서만. 비스트는 bx1~3 칸만 달아 둔다(효과는 따로)
③ 배경음악: 비스트 위기의 봉인 · 강림 동안 검은 성배 곡 대신 평소 낮 · 밤 곡(비스트 곡은 따로)
④ 시나리오 설정에 「비스트 Ⅲ/R」 줄을 따로 둔다(강림을 한 번 겪으면 열림). 위기마다 자연 발생 · 항상 · 끄기
⑤ 비스트 생이 검은 성배 통계(cx_lives)로 섞여 들어가던 것을 막는다
사용: python3 bxscn_apply.py <game.html>"""
import sys, i18n
D = [
 ('봉인된 성배','The Sealed Grail','封印された聖杯'),('비어 있는 성배','The Empty Grail','空の聖杯'),('비스트 Ⅲ/R · 강림','Beast III/R · Descent','ビーストIII/R · 降臨'),('비스트','Beast','ビースト'),
 ('비스트 Ⅲ/R','Beast III/R','ビーストIII/R'),
 ('매장기관의 수녀가 성배를 노리고, 달에서 온 BB가 성배를 봉인합니다. 반전 끝에 셋쇼인 키아라가 강림합니다.','A nun of the Burial Agency targets the Grail, and BB from the Moon seals it away. After the twist, Sessyoin Kiara descends.','埋葬機関の修道女が聖杯を狙い、月から来たBBが聖杯を封印します。反転の果てに殺生院キアラが降臨します。'),
 ('열 번에 한 번꼴로 찾아옵니다. 어벤저가 낀 전쟁이면 조금 더 자주.','Comes about once in every ten wars — a little more often when an Avenger is involved.','およそ十回に一度訪れます。アヴェンジャーが加わる戦争では少し多めに。'),
 ('열 번에 한 번꼴로 찾아옵니다.','Comes about once in every ten wars.','およそ十回に一度訪れます。'),
 ('모든 성배전쟁에서 키아라가 성배를 노립니다.','Kiara targets the Grail in every Holy Grail War.','すべての聖杯戦争でキアラが聖杯を狙います。'),
 ('키아라는 나타나지 않습니다.','Kiara never appears.','キアラは現れません。'),
 ('두 위기가 모두 「항상」이면 생마다 둘 중 하나가 찾아옵니다.','If both crises are set to “Always”, one of the two comes in each life.','二つの危機がどちらも「常に」なら、生ごとにどちらか一方が訪れます。'),
 ('첫 화면의 「시나리오」에서 비스트 Ⅲ/R을 다시 만날지 정할 수 있습니다.','From “Scenarios” on the title screen, you can choose whether to meet Beast III/R again.','タイトル画面の「シナリオ」で、ビーストIII/Rにもう一度出会うかどうかを決められます。'),
]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # ---- 엔진: 위기마다 따로 정하는 시나리오 ----
    rp("""function crisisRoll(h,pairs){ const av=h.cls==='avenger'||pairs.some(p=>p.cls==='avenger'), f=typeof globalThis!=='undefined'?globalThis.__FORCE_CRISIS:undefined, m=(S.scn&&S.scn.black)||'nat'; if(f===false||(f===undefined&&m==='off')) return null; if(!f&&m!=='always'&&!ch(av?CRISIS.pAv:CRISIS.p)) return null;
    const t=wpick(CRISIS.list,x=>av?x.wAv:x.w);""",
       """function crisisRoll(h,pairs){ const av=h.cls==='avenger'||pairs.some(p=>p.cls==='avenger'), f=typeof globalThis!=='undefined'?globalThis.__FORCE_CRISIS:undefined, sc=S.scn||{};
    // 시나리오 설정은 위기마다 따로(검은 성배 black · 비스트 beast): 끈 위기는 빠지고, 「항상」이 있으면 그 가운데서, 아니면 자연 발생 몫만큼 굴린다
    const md=x=>(x.id==='black'?sc.black:x.id==='beast3R'?sc.beast:null)||'nat', wt=x=>av?x.wAv:x.w;
    let L=CRISIS.list; if(f===false) return null;
    if(f===undefined){ L=L.filter(x=>md(x)!=='off'); if(!L.length) return null; const al=L.filter(x=>md(x)==='always');
      if(al.length) L=al; else { const all=CRISIS.list.reduce((a,x)=>a+wt(x),0), on=L.reduce((a,x)=>a+wt(x),0); if(!ch((av?CRISIS.pAv:CRISIS.p)*on/all)) return null; } }
    const t=wpick(L,wt);""")
    rp("function cxRep(){ const w=S.war, c=w&&w.crisis; if(!c) return null;", "function cxRep(){ const w=S.war, c=w&&w.crisis; if(!c||c.type==='beast3R') return null; // 검은 성배 통계(cx_lives)에만 보낸다")
    rp("cx:w.crisis?{st:w.crisis.stage,sk:w.crisis.shadowKills||0,", "cx:w.crisis?{type:w.crisis.type,st:w.crisis.stage,sk:w.crisis.shadowKills||0,")
    # ---- 화면: 시나리오 설정이 열리는 조건 · 기록 화면 안내 ----
    rp("if(r.wd&&r.wd.cx&&r.wd.cx.st>=2&&scnUnlock('black')) r.scnNew='black';",
       "{ const x=r.wd&&r.wd.cx; if(x){ const bx=x.type==='beast3R'; if(bx?x.st>=3:x.st>=2){ const k=bx?'beast':'black'; if(scnUnlock(k)) r.scnNew=k; } } }")
    rp("<b>시나리오 설정이 열렸습니다.</b> 첫 화면의 「시나리오」에서 검은 성배를 다시 만날지 정할 수 있습니다.</div>",
       "<b>시나리오 설정이 열렸습니다.</b> ${r.scnNew==='beast'?'첫 화면의 「시나리오」에서 비스트 Ⅲ/R을 다시 만날지 정할 수 있습니다.':'첫 화면의 「시나리오」에서 검은 성배를 다시 만날지 정할 수 있습니다.'}</div>")
    # ---- 화면: 시나리오 설정 창 ----
    rp("""<p class="scn-st" id="scnStBlack"></p></div></div></div>""",
       """<p class="scn-st" id="scnStBlack"></p></div><div class="scn-sec" id="scnBeast"><div class="scn-t">비스트 Ⅲ/R <span class="scn-new hidden" id="scnNewBeast">NEW</span></div><div class="scn-seg" role="group" aria-label="비스트 Ⅲ/R"><button type="button" data-k="beast" data-m="nat">자연 발생</button><button type="button" class="al" data-k="beast" data-m="always">항상</button><button type="button" data-k="beast" data-m="off">끄기</button></div><p>매장기관의 수녀가 성배를 노리고, 달에서 온 BB가 성배를 봉인합니다. 반전 끝에 셋쇼인 키아라가 강림합니다.</p><p class="scn-st" id="scnStBeast"></p></div><p class="scn-st hidden" id="scnBoth" style="font-size:12.5px;color:var(--dim);margin:12px 0 0">두 위기가 모두 「항상」이면 생마다 둘 중 하나가 찾아옵니다.</p></div></div>""")
    rp("const SCN_ST={nat:'다섯 번에 한 번꼴로 찾아옵니다. 어벤저가 낀 전쟁이면 조금 더 자주.',",
       "const SCN_STX={nat:'열 번에 한 번꼴로 찾아옵니다.',always:'모든 성배전쟁에서 키아라가 성배를 노립니다.',off:'키아라는 나타나지 않습니다.'};\nconst SCN_ST={nat:'열 번에 한 번꼴로 찾아옵니다. 어벤저가 낀 전쟁이면 조금 더 자주.',")
    rp("return {black:u.black&&SCN_MODES.includes(m.black)?m.black:'nat'}; }",
       "return {black:u.black&&SCN_MODES.includes(m.black)?m.black:'nat',beast:u.beast&&SCN_MODES.includes(m.beast)?m.beast:'nat'}; }\nfunction scnStSync(){ const c=scnFor(); $('#scnStBlack').textContent=SCN_ST[c.black]; $('#scnStBeast').textContent=SCN_STX[c.beast]; const u=scnU(); $('#scnBoth').classList.toggle('hidden',!(u.black&&u.beast&&c.black==='always'&&c.beast==='always')); }")
    rp("""  $('#scnBlack').classList.toggle('hidden',!u.black); $('#scnNewBlack').classList.toggle('hidden',!u.black||!!seen.black);""",
       """  $('#scnBlack').classList.toggle('hidden',!u.black); $('#scnNewBlack').classList.toggle('hidden',!u.black||!!seen.black);
  $('#scnBeast').classList.toggle('hidden',!u.beast); $('#scnNewBeast').classList.toggle('hidden',!u.beast||!!seen.beast);""")
    rp("""  $('#scnStBlack').textContent=SCN_ST[cur.black]; }""", """  scnStSync(); }""")
    rp("""x.setAttribute('aria-pressed',String(x===b))); $('#scnStBlack').textContent=SCN_ST[scnFor().black]; });""",
       """x.setAttribute('aria-pressed',String(x===b))); scnStSync(); });""")
    # ---- 화면: 현황판 위기 줄 · 조 목록 ----
    rp("""return `<p class="hint cxl">검은 성배 · ${['','징조','범람','강림'][c.stage]} <span""",
       """return `<p class="hint cxl">${c.type==='beast3R'?(c.stage>=3?'비스트 Ⅲ/R · 강림':c.noBB?'비어 있는 성배':'봉인된 성배'):`검은 성배 · ${['','징조','범람','강림'][c.stage]}`} <span""")
    rp("""rowsP.push(`<div class="pair-sep">검은 성배</div>`); w.crisis.units.forEach(u=>{ rowsP.push(`<button class="pair cxu ${u.alive?'':'out'}" data-i="${u.i}"><span class="c">${u.cx==='boss'?'성배':'그림자'}</span>""",
       """const bx=w.crisis.type==='beast3R'; rowsP.push(`<div class="pair-sep">${bx?(w.crisis.stage>=3?'비스트 Ⅲ/R':w.crisis.noBB?'비어 있는 성배':'봉인된 성배'):'검은 성배'}</div>`); w.crisis.units.forEach(u=>{ rowsP.push(`<button class="pair cxu ${u.alive?'':'out'}" data-i="${u.i}"><span class="c">${u.cx==='boss'?(bx?'비스트':'성배'):u.cx==='sent'?'센티넬':u.cx==='bb'?'BB':'그림자'}</span>""")
    # ---- 화면 효과 칸 · 배경음악 ----
    rp("""{ const c=war&&S.war.crisis, st=c&&!c.done?c.stage:0; for(const k of [1,2,3]) $('#game').classList.toggle('cx'+k,st===k); }""",
       """{ const c=war&&S.war.crisis, st=c&&!c.done?c.stage:0, bx=!!(c&&c.type==='beast3R'); for(const k of [1,2,3]){ $('#game').classList.toggle('cx'+k,!bx&&st===k); $('#game').classList.toggle('bx'+k,bx&&st===k); } }""")
    rp("""  if(w.crisis&&w.crisis.stage>=2&&!w.ended) return 'black';""",
       """  if(w.crisis&&w.crisis.stage>=2&&!w.ended&&w.crisis.type!=='beast3R') return 'black'; // 비스트 위기는 전용 곡이 생기기 전까지 평소 낮 · 밤 곡""")
    rp("""${c.zones&&c.zones.length?` · 오염 구역 ${c.zones.join(', ')}`:''}</p>`; })()}""", """${c.type!=='beast3R'&&c.zones&&c.zones.length?` · 오염 구역 ${c.zones.join(', ')}`:''}</p>`; })()}""")
    s, nd, nt = i18n.add(s, D)
    print('bxscn miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
