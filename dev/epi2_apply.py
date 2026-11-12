"""에필로그 시간 흐름 개편 1 · 2단계 (11-12): 구간 틀 · 걸음 · 날짜 표시 · 예전 사건 옮기기. 화면 코드는 epi2.js.
새 사건(A · B 구간)과 영어 · 일본어는 검수 뒤에 넣는다. 사용: python3 epi2_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    js = open(os.path.join(HERE, 'epi2.js'), encoding='utf-8').read()
    # 새 사건 데이터 (epi2_ev.py): 본문 · 결과는 RLEP에, 조건 · 효과는 EP2_EV에
    import json, re, importlib, epi2_ev, epi2_ev2, epi2_ev3, epi2_ev4
    for m_ in (epi2_ev, epi2_ev2, epi2_ev3, epi2_ev4): importlib.reload(m_)
    ALLEV = epi2_ev.EV + epi2_ev2.EV + epi2_ev3.EV + epi2_ev4.EV
    fixN = lambda t: re.sub(r'\{N(의|에게서|에게는|에게|에|도)\}', r'{N}\1', t)
    def fx(x): return {k: [fixN(t) for t in v] for k, v in x.items()} if isinstance(x, dict) else [fixN(t) for t in x]
    RL, EVD = {}, []
    for e in ALLEV:
        RL[e['id']] = {'t': e['t'], 'b': [fx(b) for b in e['b']], 'c': [{'key': c['key'], 't': c['t'], 'r': [fx(r) for r in c['r']]} for c in e['c']]}
        d = {'id': e['id'], 'ph': e['ph'], 'fx': {c['key']: c['fx'] for c in e['c']}, 'love': [c['key'] for c in e['c'] if c.get('love')]}
        for k in ('not', 'only', 'wish', 'day', 'mon', 'wed', 'kid', 'track'):
            if e.get(k): d[k] = e[k]
        EVD.append(d)
    ALT = {k: [{'tag': v['tag'], 'b': [fx(b) for b in v['b']], 'r': {ck: [fx(r) for r in rr] for ck, rr in v['r'].items()}} for v in L] for k, L in epi2_ev.ALT.items()}
    J = lambda o: json.dumps(o, ensure_ascii=False)
    js = ("  Object.assign(RLEP," + J(RL) + ");\n  const EP2_EV=" + J(EVD) + ";\n  const EP2_TAGS=" + J(epi2_ev.TAGS) + ";\n  const EP2_ALT=" + J(ALT)
          + ";\n  const EP2_DAY2=" + J([fixN(x) for x in epi2_ev4.DAY2]) + ", EP2_MON2=" + J({str(k): [fixN(x) for x in v] for k, v in epi2_ev4.MON2.items()}) + ", EP2_YR2=" + J([fixN(x) for x in epi2_ev4.YR2])
          + ", EP2_DAY2V=" + J({str(k): {t: fixN(x) for t, x in v.items()} for k, v in epi2_ev4.DAY2V.items()})
          + ";\n  const EP2_DAYV=" + J({str(k): v for k, v in epi2_ev.DAYV.items()}) + ", EP2_YRV=" + J({str(k): v for k, v in epi2_ev.YRV.items()}) + ";\n") + js
    rp("f:()=>epRel('lv_night',{fx:{", "f:()=>epRel('lv_night',{b:ep2NightB(),fx:{")
    rp("f:()=>epRel('lv_morning',{fx:{", "f:()=>epRel('lv_morning',{b:ep2Alt('lv_morning','b'),r:ep2Alt('lv_morning','r'),fx:{")
    rp("  function finalYears(){\n", js + "  function finalYears(){\n")
    # 걸음: 구간마다 기다리는 시간이 다르고, A · B · C는 ep2Step이 먼저 본다
    rp("    S.clock+=sp; if(S.clock<epiGap()) return; S.clock=0;\n    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);\n",
       "    S.clock+=sp; if(S.clock<epiGap()*ep2Gap()) return; S.clock=0;\n    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);\n    if(ep2Step()) return; if(S.dead||S.pending) return;\n")
    rp("if(S.phase==='epi') return Math.min(1,S.clock/(LEN[S.len].spy*1.3));", "if(S.phase==='epi') return Math.min(1,S.clock/(LEN[S.len].spy*1.3*ep2Gap()));")
    rp("  function passYears(n){\n    if(n<=0) return;\n", "  function passYears(n){\n    if(n>1&&S.epi&&S.epi.ph==='C') n=1;   // 열 해 구간: 한 해씩\n    if(n<=0) return;\n")
    # 기다림: A · B 구간에서는 해가 아니라 걸음으로 센다
    rp("else if(c.wait){ r.wait=war?S.war.day+3:S.year+2; if(st>=3) r.waited=1; }", "else if(c.wait){ if(ep2Tight()){ r.wait=0; S.epi.relK=S.epi.k+3; } else r.wait=war?S.war.day+3:S.year+2; if(st>=3) r.waited=1; }")
    rp("    return r.pt>=REL_PT[r.stage+1]&&S.war.trust>=REL_REQ[r.stage+1]; }", "    if(S.phase==='epi'&&S.epi&&S.epi.ph&&S.epi.ph!=='D'&&(S.epi.k||0)<(S.epi.relK||0)) return false;\n    return r.pt>=REL_PT[r.stage+1]&&S.war.trust>=REL_REQ[r.stage+1]; }")
    rp("later:()=>{S.flags.relNightWait=S.year+2;}", "later:()=>{ if(ep2Tight()) S.epi.nightK=S.epi.k+3; else S.flags.relNightWait=S.year+2; }")
    rp("&&!S.flags.relNight&&S.year>=(S.flags.relNightWait||0),once:0,", "&&!S.flags.relNight&&S.year>=(S.flags.relNightWait||0)&&!(S.epi&&(S.epi.k||0)<(S.epi.nightK||0)),once:0,")
    # 저장 → 불러오기: 떠 있던 사건을 다시 띄우고, 같은 나이 안에서도 걸음마다 난수 줄기가 달라지게 한다
    rp("    if(r==='ev'&&S.resumeEv&&S.resumeEv.src==='ART') return showArt(S.resumeEv.id);", "    if(r==='ev'&&S.resumeEv&&S.resumeEv.src==='EP2') return ep2Resume();\n    if(r==='ev'&&S.resumeEv&&S.resumeEv.src==='ART') return showArt(S.resumeEv.id);")
    rp("R=mulberry((data.seed+data.age*7919)|0); S.pending=null;", "R=mulberry((data.seed+data.age*7919+((data.epi&&data.epi.ph&&data.epi.ph!=='D'&&data.epi.k)||0)*31337)|0); S.pending=null;")
    # 화면: 날짜
    rp("stay:stayHome(),away:!!S.flags.stayAway&&!S.flags.stayDied,", "when:ep2When(),stay:stayHome(),away:!!S.flags.stayAway&&!S.flags.stayDied,")
    rp("newLife,start,tick,", "newLife,start,tick,ep2When,")
    rp("S.dead?'끝':S.phase==='epi'?'에필로그':'삶';", "S.dead?'끝':S.phase==='epi'?((w2=>w2?(w2.u==='d'?`봄 · ${w2.n}일째`:`첫 해 · ${w2.n}달째`):'에필로그')(Sim.ep2When())):'삶';")
    rp(":v.yrs>=1?`수육 · 함께 산 지 ${v.yrs}년`:'수육 · 함께 살기 시작함';", ":v.when?(v.when.u==='d'?`수육 · 함께 산 지 ${v.when.n}일`:`수육 · 함께 산 지 ${v.when.n}달`):v.yrs>=1?`수육 · 함께 산 지 ${v.yrs}년`:'수육 · 함께 살기 시작함';")
    # 번역: 줄 번호(검수 페이지와 같다) → 문장 틀. 이름이 들어간 문장은 I18N_TPL에, 아니면 I18N_DICT에
    import glob, epi2_rev, i18n; importlib.reload(epi2_rev)
    ROW = {r['id']: r['L'] for g in epi2_rev.G for r in g['rows']}
    TRS, UIT, UID = {}, [], []
    for f in sorted(glob.glob(os.path.join(HERE, 'epi2_tr*.py'))):
        ns = {}; exec(open(f, encoding='utf-8').read(), ns); TRS.update(ns.get('TR', {})); UIT += ns.get('UI', []); UID += ns.get('UID', [])
    PT = {'은': '은', '이': '이', '을': '을', '과': '과', '으로': '으로'}
    def kt(t): t = fixN(t); t = re.sub(r'\{N(은|이|을|과|으로)\}', r'{0~\1}', t); return t.replace('{N}', '{0}')
    DI, TP, bad = [], [], []
    for i, v in TRS.items():
        L = ROW.get(i)
        if not L: bad.append(i); continue
        V = [v] if isinstance(v, tuple) else v
        if len(V) != len(L): bad.append(i); continue
        for ko, (en, ja) in zip(L, V):
            k = kt(ko)
            if '{0' in k: TP.append((k, en.replace('{N}', '{0}'), ja.replace('{N}', '{0}')))
            else: DI.append((ko, en, ja))
    # 해체(반말) 판: CAS_V 서번트가 쓰는 줄. 따옴표 안만 바꾸고, 영어는 같은 문장, 일본어는 따옴표 안만 바꾼다
    import epi2_cas; importlib.reload(epi2_cas); CS, cbad = {}, []
    for i, qs in epi2_cas.CAS.items():
        L, v = ROW.get(i), TRS.get(i)
        if not L or not isinstance(v, list) or len(re.findall(r'“[^”]*”', L[0])) != len(qs) or len(re.findall(r'「[^」]*」', v[0][1])) != len(qs): cbad.append(i); continue
        it = iter(qs); ko = re.sub(r'“[^”]*”', lambda m: '“' + next(it)[0] + '”', L[0])
        it = iter(qs); ja = re.sub(r'「[^」]*」', lambda m: '「' + next(it)[1] + '」', v[0][1])
        CS[L[0]] = ko; k = kt(ko)
        if '{0' in k: TP.append((k, v[0][0].replace('{N}', '{0}'), ja.replace('{N}', '{0}')))
        else: DI.append((ko, v[0][0], ja))
    m2 = re.search(r'const CASL=\{', s)
    if m2 and CS: s = s[:m2.end()] + json.dumps(CS, ensure_ascii=False)[1:-1] + ', ' + s[m2.end():]
    else: miss.append('CASL')
    if cbad: print('해체 판 안 맞는 줄', cbad)
    s, nd, _ = i18n.add(s, DI + UID, [])
    m_, T = i18n._blk(s, 'I18N_TPL'); nt = 0
    for ko, en, ja in TP:
        for lang, v in (('en', en), ('ja', ja)):
            if not any(x[0] == ko for x in T[lang]): T[lang].append([ko, v, 1]); nt += 1
    for ko, en, ja in UIT:
        for lang, v in (('en', en), ('ja', ja)):
            if not any(x[0] == ko for x in T[lang]): T[lang].append([ko, v]); nt += 1
    s = s[:m_.start(1)] + json.dumps(T, ensure_ascii=False, separators=(',', ':')) + s[m_.end(1):]
    todo = [i for i in ROW if i not in TRS and not i.startswith('tags.')]
    open(P, 'w', encoding='utf-8').write(s); print('epi2 miss', miss, '| 번역 dict', nd, 'tpl', nt, '잘못된 번호', bad[:5], '남은 줄', len(todo))
