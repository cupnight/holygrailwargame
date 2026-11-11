import sys,json,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import i18n
for p in sys.argv[1:]:
    s=open(p).read(); miss=[]
    def rp(o,n,c=1):
        global s
        k=s.count(o)
        if k!=c: miss.append((o[:50],k)); return
        s=s.replace(o,n)
    rp("""    judge:{n:'룰러',d:'일곱 자리 바깥의 서번트. 상대의 정체를 꿰뚫고 판결을 내린다.',sp:1},
  };""","""    judge:{n:'룰러',d:'일곱 자리 바깥의 서번트. 상대의 정체를 꿰뚫고 판결을 내린다.',sp:1},
    moon:{n:'문 캔서',d:'일곱 자리 바깥의 서번트. 달의 권능으로 도시의 기록을 고쳐 쓴다.',sp:1},
    ego:{n:'알터 에고',d:'일곱 자리 바깥의 서번트. 여러 신성을 합친 몸이라, 쓰러뜨린 상대의 힘을 빨아들인다.',sp:1},
    beast:{n:'비스트',d:'인류가 스스로 낳은 재앙. 소환되지 않는다.',sp:1,boss:1},
  };""")
    rp("SPECIAL=Object.keys(CLS).filter(c=>CLS[c].sp);","SPECIAL=Object.keys(CLS).filter(c=>CLS[c].sp&&!CLS[c].boss);")
    rp("const k=wpick(['avenger','judge'],x=>A[x]+.5);","const k=wpick(['avenger','judge','moon','ego'],x=>A[x]!=null?A[x]+.5:.3);",2)
    rp("const CLS_ORD=['sword','lance','bow','rider','caster','shadow','berserk','judge','avenger']","const CLS_ORD=['sword','lance','bow','rider','caster','shadow','berserk','judge','avenger','moon','ego']")
    # 속성(HAL)은 al_apply.py에서 신규 서번트까지 함께 넣는다
    m=re.search(r'const CAS_V=new Set\(\[',s)
    if m: s=s[:m.end()]+'"meltryllis", '+s[m.end():]
    else: miss.append('CAS_V')
    # 문 캔서 낮 행동
    rp("""    if(h.cls==='shadow') ch_.push({t:'거처에 잠입한다',""","""    if(h.cls==='moon'){ const cd=w.moonD!=null&&w.day-w.moonD<3; ch_.push({t:'기록을 고쳐 쓴다',d:cd?`다시 쓰려면 ${3-(w.day-w.moonD)}일 더 기다려야 한다`:'노출을 지우고, 다른 조 하나의 단서를 읽어 낸다 · 사흘에 한 번',off:cd,auto:!cd&&w.exposure>=30,f:()=>{ w.moonD=w.day; w.queue.push(()=>log(moonDo(),'war')); }}); }
    if(h.cls==='shadow') ch_.push({t:'거처에 잠입한다',""")
    rp("""  // 정찰 클래스 보정: 선택지 배지와 결과 칩으로 보여 준다""","""  // 문 캔서: 도시의 기록을 고쳐 쓴다 (노출 −20, 아직 정체를 모르는 조 하나의 단서 +25)
  function moonDo(){ const w=W(), h=hero(); w.exposure=clamp(w.exposure-20); const t=pick(alivePairs().filter(p=>!p.revealed));
    if(t) addIntel(t,25);
    return `${h.name}${J(h.name,이)} 도시의 기록을 조용히 고쳐 썼다. 감시 카메라와 목격담에서 우리 흔적이 지워졌다.${t?` ${pName(t)} 조에 대한 단서도 하나 건져 냈다.`:''}`; }
  // 정찰 클래스 보정: 선택지 배지와 결과 칩으로 보여 준다""")
    rp("""  function npcFight(a,b,final,init){ const r=npcDuel(a,b,final,init); addKnow(a,b,20); addKnow(b,a,20); famSeeFight(a,b); return r; }""",
       """  function npcFight(a,b,final,init){ const r=npcDuel(a,b,final,init); addKnow(a,b,20); addKnow(b,a,20); famSeeFight(a,b);
    if(r&&r.win&&r.lose&&r.lose.hp<=0&&!r.win.cx&&H_BY[r.win.hero]&&H_BY[r.win.hero].cls==='ego') r.win.hp=clamp(r.win.hp+15); // 알터 에고: 쓰러뜨린 상대의 힘을 빨아들인다
    return r; }""")
    rp("""    if(e.cx){ const dead=cxUnitDown(e,by==='우리'?'me':null);""","""    if(by==='우리'&&W().heroAlive&&hero().cls==='ego'){ const w=W(); w.hp=clamp(w.hp+15); w.sm=clamp(w.sm+15); log(`${hero().name}${J(hero().name,이)} 쓰러진 상대의 힘을 빨아들였다. 체력 +15 · 서번트 마력 +15`,'war'); }
    if(e.cx){ const dead=cxUnitDown(e,by==='우리'?'me':null);""")
    D=[('문 캔서','Moon Cancer','ムーンキャンサー'),('알터 에고','Alter Ego','アルターエゴ'),('비스트','Beast','ビースト'),
       ('일곱 자리 바깥의 서번트. 달의 권능으로 도시의 기록을 고쳐 쓴다.','A Servant outside the seven seats. With the power of the Moon, it rewrites the city\'s records.','七騎の外のサーヴァント。月の権能で街の記録を書き換える。'),
       ('일곱 자리 바깥의 서번트. 여러 신성을 합친 몸이라, 쓰러뜨린 상대의 힘을 빨아들인다.','A Servant outside the seven seats. A body fused from several divinities, it drinks in the strength of those it fells.','七騎の外のサーヴァント。複数の神性を束ねた身ゆえ、倒した相手の力を吸い上げる。'),
       ('인류가 스스로 낳은 재앙. 소환되지 않는다.','A calamity humanity bore of itself. It cannot be summoned.','人類が自ら生んだ災厄。召喚されることはない。'),
       ('기록을 고쳐 쓴다','Rewrite the records','記録を書き換える'),
       ('노출을 지우고, 다른 조 하나의 단서를 읽어 낸다 · 사흘에 한 번','Erase your exposure and read a clue on one other team · once every three days','露見を消し、他の組ひとつの手がかりを読み取る · 三日に一度')]
    T=[('다시 쓰려면 {0}일 더 기다려야 한다','{0} more day(s) before you can rewrite again','もう一度書き換えるには、あと{0}日待たねばならない'),
       ('{0~이} 도시의 기록을 조용히 고쳐 썼다. 감시 카메라와 목격담에서 우리 흔적이 지워졌다. {1} 조에 대한 단서도 하나 건져 냈다.','{0} quietly rewrote the city\'s records. Every trace of you vanished from the cameras and the witness accounts. A clue on the {1} team turned up as well.','{0}は街の記録を静かに書き換えた。監視カメラからも目撃談からも、こちらの痕跡が消えた。{1}の組についての手がかりもひとつ拾い上げた。'),
       ('{0~이} 도시의 기록을 조용히 고쳐 썼다. 감시 카메라와 목격담에서 우리 흔적이 지워졌다.','{0} quietly rewrote the city\'s records. Every trace of you vanished from the cameras and the witness accounts.','{0}は街の記録を静かに書き換えた。監視カメラからも目撃談からも、こちらの痕跡が消えた。'),
       ('{0~이} 쓰러진 상대의 힘을 빨아들였다. 체력 +15 · 서번트 마력 +15','{0} drank in the strength of the fallen foe. HP +15 · Servant mana +15','{0}は倒れた相手の力を吸い上げた。体力 +15 · サーヴァント魔力 +15')]
    s,nd,nt=i18n.add(s,D,T)
    open(p,'w').write(s); print(p[-25:],'miss',miss,'tr',nd,nt)
