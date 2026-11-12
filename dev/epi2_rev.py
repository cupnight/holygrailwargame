"""검수 페이지용 목록(data.json)을 만든다. 사용: python3 epi2_rev.py <data.json>"""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import epi2_ev as m1, epi2_ev2 as m2, epi2_ev3 as m3, epi2_ev4 as m4
VN = {'mage': '캐스터(마술사형) 서번트', 'cook': '요리를 하는 서번트', 'sage': '박식한 서번트', 'civil': '싸움이 본업이 아닌 서번트', 'bold': '성향에 야망이 있는 서번트', 'd': '그 밖', 'now': '현대 · 근미래 서번트', 'modern': '근대(19~20세기) 서번트'}
FX = {'bond1': '관계 +1', 'bond2': '관계 +2', 'will1': '정신 +1', 'will2': '정신 +2', 'none': '변화 없음', 'rel4': '인연 +4', 'rel5': '인연 +5', 'rel6': '인연 +6', 'rel8': '인연 +8', 'trust2': '신뢰 +2', 'trust3': '신뢰 +3', 'trust4': '신뢰 +4',
      'health1': '건강 +1', 'health2': '건강 +2', 'wealth1': '재산 +1', 'wealth3': '재산 +3', 'wealth-5': '재산 −5 · 인연 +4', 'lore2': '지식 +2', 'far': '재산 −8 · 인연 +8'}
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'epi2.js'), encoding='utf8').read()
def arr(name): a = js.index('const ' + name + '='); return js[a:js.index(';\n', a)]
day = re.findall(r"'((?:[^'\\]|\\.)*)'", arr('EP2_DAY')); mon = re.findall(r"(\d+):'((?:[^'\\]|\\.)*)'", arr('EP2_MON')); yr = re.findall(r"'((?:[^'\\]|\\.)*)'", arr('EP2_YR'))
def vrows(i, slot, L):
    if isinstance(L, dict): return [dict(id=i + ('' if v == 'd' else '@' + v), slot=slot, L=x, fx=VN[v]) for v, x in L.items()]
    return [dict(id=i, slot=slot, L=L)]
def ev(e):
    note = []
    if e.get('not'): note.append(' · '.join(VN[k].replace(' 서번트', '') for k in [e['not']] if isinstance(k, str)) + ' 제외' if isinstance(e['not'], str) else ' · '.join(VN[k].replace(' 서번트', '') for k in e['not']) + ' 서번트 제외')
    if e.get('only'): note.append(VN[e['only']] + '만')
    if e.get('wish'): note.append('소원이 있는 서번트만')
    if e.get('day'): note.append(f"{e['day']}일째 고정")
    if e.get('mon'): note.append(f"{e['mon'][0]}~{e['mon'][1]}달째")
    if e.get('wed'): note.append('결혼한 뒤')
    rows = []
    for i, b in enumerate(e['b']): rows += vrows(f"{e['id']}.b{i}", f'본문 {i+1}', b)
    for c in e['c']:
        rows.append({'id': f"{e['id']}.{c['key']}.t", 'slot': '선택지', 'L': [c['t']], 'fx': FX[c['fx']] + (' · 애정만' if c.get('love') else ''), 'ch': 1})
        for i, r in enumerate(c['r']): rows += vrows(f"{e['id']}.{c['key']}.r{i}", f'결과 {i+1}', r)
    return {'id': e['id'], 'ph': e['ph'], 't': e['t'], 'note': ' · '.join(note), 'rows': rows}
G = [{'id': 'tags', 'ph': 'A', 't': '서번트 갈래 (문장이 갈리는 기준)', 'note': '', 'rows': [
    {'id': 'tags.sage', 'slot': '박식', 'L': ['아스클레피오스, 파라켈수스, 레오나르도 다 빈치, 니콜라 테슬라, 셜록 홈즈, 솔로몬, 시바의 여왕, 한스 크리스티안 안데르센, 윌리엄 셰익스피어, 멀린, 케이론, 아비케브론, 키르케, 메데이아, 프톨레마이오스, 시황제, 현장 삼장, 니토크리스, 세미라미스, BB']},
    {'id': 'tags.civil', 'slot': '비전투', 'L': ['안데르센, 셰익스피어, 모차르트, 살리에리, 다 빈치, 테슬라, 홈즈, 파라켈수스, 아스클레피오스, 아비케브론, 시바의 여왕, 키르케, 하베트롯, 상송, 현장 삼장, BB, 패션립']},
    {'id': 'tags.cook', 'slot': '요리', 'L': ['에미야, 에미야[얼터], 타마모 캣, 타마모노마에, 부디카, 미나모토노 라이코, 키르케, 로빈 후드, 아라쉬, 아탈란테, 센지 무라마사, 케이론, 레오나르도 다 빈치']},
    {'id': 'tags.now', 'slot': '현대', 'L': ['에미야, 에미야[얼터], 살생원 키아라']},
    {'id': 'tags.modern', 'slot': '근대', 'L': ['니콜라 테슬라, 셜록 홈즈, 히지카타 토시조, 오키타 소지, 안데르센, 암굴왕, 이서문, 잭 더 리퍼']},
    {'id': 'tags.mage', 'slot': '마술사', 'L': ['클래스가 캐스터인 서번트 전원']},
    {'id': 'tags.bold', 'slot': '야망', 'L': ['성향에 「야망」이 있는 서번트 전원 (48명)']}]}]
for n_, a in enumerate(m1.ALT['lv_morning']):
    pre = 'alt.lv_morning' + ('' if n_ == 0 else '.' + a['tag']); rows = [{'id': f'{pre}.b{i}', 'slot': f'본문 {i+1}', 'L': b} for i, b in enumerate(a['b'])]
    for k, t in (('cook', '아침을 차려 준다'), ('together', '같이 차린다')):
        rows.append({'id': f'{pre}.{k}.t', 'slot': '선택지', 'L': [t], 'fx': '원래 선택지 그대로', 'ch': 1}); rows += [{'id': f'{pre}.{k}.r{i}', 'slot': f'결과 {i+1}', 'L': x} for i, x in enumerate(a['r'][k])]
    G.append({'id': 'alt_lv_morning_' + a['tag'], 'ph': 'A', 't': '첫 번째 아침 (기존 사건 · ' + VN[a['tag']] + ' 변형)', 'note': '', 'rows': rows})
def nar(key, src, V):
    rs = []
    for i, x in src:
        r = {'id': f'{key}.{i}', 'slot': str(i + 1) if key != 'n_mon' else f'{i}달째', 'L': [x]}; rs.append(r)
        if i in V:
            r['fx'] = VN['d']; seen = {}
            for v, t in V[i].items():
                if t in seen: seen[t]['fx'] += ' · ' + VN[v]; continue
                seen[t] = {'id': f'{key}.{i}@{v}', 'slot': r['slot'], 'L': [t], 'fx': VN[v]}; rs.append(seen[t])
    return rs
G.append({'id': 'n_day', 'ph': 'A', 't': '매일 묘사 (열나흘)', 'note': '날마다 한 줄. 14번은 14일째 고정', 'rows': nar('n_day', list(enumerate(day)), m1.DAYV) + sum(([dict({'id': f'n_day2.{i}', 'slot': str(15 + i), 'L': [x]}, **({'fx': VN['d']} if i in m4.DAY2V else {}))] + [{'id': f'n_day2.{i}@{v}', 'slot': str(15 + i), 'L': [t], 'fx': VN[v]} for v, t in m4.DAY2V.get(i, {}).items()] for i, x in enumerate(m4.DAY2)), [])})
mr = []
for k, x in mon:
    k = int(k); mr.append({'id': f'n_mon.{k}', 'slot': f'{k}달째', 'L': [x]}); mr += [{'id': f'n_mon2.{k}.{j}', 'slot': f'{k}달째', 'L': [t]} for j, t in enumerate(m4.MON2.get(k, []))]
G.append({'id': 'n_mon', 'ph': 'B', 't': '매달 묘사 (첫 해)', 'note': '달마다 셋 가운데 하나', 'rows': mr})
G.append({'id': 'n_yr', 'ph': 'C', 't': '해마다 묘사 (열 해)', 'note': '', 'rows': nar('n_yr', list(enumerate(yr)), m1.YRV) + [{'id': f'n_yr2.{i}', 'slot': str(10 + i), 'L': [x]} for i, x in enumerate(m4.YR2)]})
for e in m1.EV + m2.EV + m3.EV + m4.EV: G.append(ev(e))
G.sort(key=lambda g: (0 if g['id'] == 'tags' or g['id'].startswith('alt_') else 1, 'ABC'.index(g['ph']), 0 if g['id'].startswith('n_') else 1))
if __name__ == '__main__':
    json.dump(G, open(sys.argv[1], 'w', encoding='utf8'), ensure_ascii=False); print(len(G), sum(len(g['rows']) for g in G))
