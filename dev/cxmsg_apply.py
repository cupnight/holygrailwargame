"""11-13: 비스트 위기 유닛의 전투 종료 메시지 · 적 카드 · 정보창 문구
- 멜트릴리스 · 패션립 센티넬을 쓰러뜨리면 '상대 소멸' 대신 '상대 풀려남'
- 적 카드의 주인 자리: 센티넬(반전 전 알 수 없음 · 뒤 셋쇼인 키아라) · BB(주인 없음) · 키아라(비스트 Ⅲ/R)
- 조 목록에서 누른 정보창: 설명 · 주인 · 상태 · 안내를 비스트 유닛에 맞게
사용: python3 cxmsg_apply.py <game.html>"""
import sys, i18n
T = {
 'free': ('상대 풀려남', 'Enemy freed', '相手が解放された'),
 'gone': ('풀려남', 'Freed', '解放'),
 'van': ('소멸', 'Vanished', '消滅'),
 'none': ('없음', 'None', 'なし'),
 'd_boss': ('성배를 삼킨 비스트', 'The Beast who swallowed the Grail', '聖杯を呑んだビースト'),
 'd_bb': ('성배를 봉인한 문 캔서', 'The Moon Cancer who sealed the Grail', '聖杯を封印したムーンキャンサー'),
 'd_sent': ('KP를 품은 센티넬', 'A Sentinel holding a KP', 'KPを抱くセンチネル'),
 'h_boss': ('두 번 쓰러뜨려야 한다. 키아라 쪽에 남은 KP가 많을수록 단단하다.', 'Must be brought down twice. The more KP remain on Kiara\'s side, the tougher she is.', '二度倒さねばならない。キアラ側に残るKPが多いほど硬い。'),
 'h_bb': ('토벌령의 표적. 봉인을 지키는 동안은 쉽게 쓰러지지 않는다.', 'The target of the subjugation order. While she holds the seal, she does not fall easily.', '討伐令の標的。封印を守っている間は容易には倒れない。'),
 'd_bb3': ('성배를 봉인했던 문 캔서', 'The Moon Cancer who once sealed the Grail', '聖杯を封印していたムーンキャンサー'),
 'h_bb3': ('봉인은 깨졌다. 지금은 키아라와 맞서는 쪽에 섰다.', 'The seal is broken. Now she stands against Kiara.', '封印は破られた。今はキアラに立ち向かう側にいる。'),
 'h_guard': ('키아라 곁을 지킨다. 결전에서만 만난다.', 'Guards Kiara\'s side. You will only meet it in the decisive battle.', 'キアラの傍らを守る。決戦でのみ相見える。'),
 'h_sent': ('마스터가 없어 동맹 · 휴전 · 암살의 대상이 되지 않는다. 쓰러뜨리면 KP를 회수하고, 감독관이 령주 한 획을 준다.', 'Having no Master, it cannot be allied with, offered a truce, or assassinated. Defeat it to recover its KP, and the overseer will grant you one Command Seal.', 'マスターがいないため、同盟・休戦・暗殺の対象にならない。倒せばKPを回収し、監督役が令呪を一画与える。'),
}
K = {k: v[0] for k, v in T.items()}
HELP = (
 "// 11-13: 후반 위기 유닛의 주인 · 설명 · 상태 · 안내 (비스트 Ⅲ/R은 따로)\n"
 "const cxBx=()=>{ const c=Sim.S&&Sim.S.war&&Sim.S.war.crisis; return c&&c.type==='beast3R'?c:null; };\n"
 "const cxOwner=(u,info)=>{ const c=cxBx(); if(!c) return '검은 성배'; if(u.cx==='boss') return info?'" + K['none'] + "':'비스트 Ⅲ/R'; if(u.cx==='bb') return info?'" + K['none'] + "':'주인 없음'; return c.stage>=3?'셋쇼인 키아라':'알 수 없음'; };\n"
 "const cxGone=u=>u.cx==='sent'&&u.ego?'" + K['gone'] + "':'" + K['van'] + "';\n"
 "const cxDesc=u=>{ if(!u.alive) return cxGone(u); if(!cxBx()) return u.cx==='boss'?'검은 성배가 부른 복수자':'검은 성배에 물든 그림자'; return u.cx==='boss'?'" + K['d_boss'] + "':u.cx==='bb'?(cxBx().stage>=3?'" + K['d_bb3'] + "':'" + K['d_bb'] + "'):'" + K['d_sent'] + "'; };\n"
 "const cxHint=u=>{ if(!cxBx()) return u.cx==='boss'?'두 번 쓰러뜨려야 한다. 성배 앞에서는 더 강해진다. 쓰러뜨린 조가 성배 앞에 선다.':'마스터가 없어 동맹 · 휴전 · 암살의 대상이 되지 않는다. 쓰러뜨리면 감독관이 령주 한 획을 준다.';\n"
 "  return u.cx==='boss'?'" + K['h_boss'] + "':u.cx==='bb'?(cxBx().stage>=3?'" + K['h_bb3'] + "':'" + K['h_bb'] + "'):u.guard?'" + K['h_guard'] + "':'" + K['h_sent'] + "'; };\n"
 "function render(){")
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 시뮬레이션: 전투 종료 메시지
    rp("const foe=!e.alive?'상대 소멸'", "const foe=!e.alive?(e.cx==='sent'&&e.ego?'" + K['free'] + "':'상대 소멸')")
    rp("b.res==='mutual'?'동귀어진':'상대 소멸');", "b.res==='mutual'?'동귀어진':e.cx==='sent'&&e.ego?'" + K['free'] + "':'상대 소멸');")
    rp("${e.alive?`상대 ${hpWord(e.hp)}`:'상대 소멸'}", "${e.alive?`상대 ${hpWord(e.hp)}`:e.cx==='sent'&&e.ego?'" + K['free'] + "':'상대 소멸'}")
    # 화면
    rp("function render(){", HELP)
    rp("<span>${e.cx?'검은 성배':e.master?esc(e.mname):'주인 없음'}</span>", "<span>${e.cx?cxOwner(e):e.master?esc(e.mname):'주인 없음'}</span>")
    rp("${p.alive?(p.cx==='boss'?'검은 성배가 부른 복수자':'검은 성배에 물든 그림자'):'소멸'}", "${cxDesc(p)}")
    rp("<dt>주인</dt><dd>검은 성배</dd>", "<dt>주인</dt><dd>${cxOwner(p,1)}</dd>")
    rp(":'소멸'}</dd></dl>", ":cxGone(p)}</dd></dl>")
    rp("<p class=\"hint\">${p.cx==='boss'?'두 번 쓰러뜨려야 한다. 성배 앞에서는 더 강해진다. 쓰러뜨린 조가 성배 앞에 선다.':'마스터가 없어 동맹 · 휴전 · 암살의 대상이 되지 않는다. 쓰러뜨리면 감독관이 령주 한 획을 준다.'}</p>", "<p class=\"hint\">${cxHint(p)}</p>")
    s, nd, nt = i18n.add(s, list(T.values()))
    print('cxmsg miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
