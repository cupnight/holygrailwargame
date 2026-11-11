import json, re, sys, importlib
sys.path.insert(0, '/tmp/claude-0/-home-claude/3b7fc538-eed0-54bc-a02e-74418e7d1e17/scratchpad/new')
mod = importlib.import_module(sys.argv[1])
TAG = sys.argv[2]  # 블록 표시 (예: '1차')
P = sys.argv[3] if len(sys.argv)>3 else '/home/claude/holygrailwargame/public/index.html'
s = open(P, encoding='utf-8').read()
TR = []  # (ko,en,ja)
def k(t):
    TR.append(t); return t[0]
J = lambda x: json.dumps(x, ensure_ascii=False)

# 1) HEROES 배열 끝에 추가
heroes = []
for h in mod.B:
    o = {'id': h['id']}
    if h.get('fem'): o['fem'] = 1
    o.update(cls=h['cls'], name=k(h['name']), title=k(h['title']), **{'from': k(h['frm'])}, s=h['s'],
             art={'n': k(h['art']['n']), 'd': k(h['art']['d'])}, traits=h['traits'], wish=k(h['wish']), relic=k(h['relic']),
             frags=[k(x) for x in h['frags']])
    if h.get('sp'): o['sp'] = h['sp']
    heroes.append('    ' + J(o) + ',')
i = s.index('  const HEROES = [')
j = s.index('\n  ];', i)
s = s[:j] + '\n    // ---- 신규 서번트 ' + TAG + ' ----\n' + '\n'.join(heroes) + s[j:]

# 2) 표 보강 블록
L = ['  // ---- 신규 서번트 ' + TAG + ': 대사·보구·스킬·전투 특례 ----']
for h in mod.B:
    id = h['id']; v = h['voice']
    vo = {'reg': v['reg'], 'ord': v['ord']}
    for key in ['greet','bow','wish','order','plan','naive','thanks','flee','seals0','dawn','refuse','grailNo','grailYes','soul']:
        if key in v: vo[key] = k(v[key])
    vo['bye'] = [k(x) for x in v['bye']]; vo['cold'] = k(v['cold']); vo['askWish'] = k(v['askWish'])
    L.append(f'  VOICE[{J(id)}]={J(vo)};')
    L.append(f'  HLINE[{J(id)}]={J([k(x) for x in h["hline"]])};')
    L.append(f'  HDAY[{J(id)}]={J([k(x) for x in h["hday"]])};')
    L.append(f'  TALKX[{J(id)}]={J({"t":[k(x) for x in h["talk"]["t"]],"w":[k(x) for x in h["talk"]["w"]]})};')
    L.append(f'  WEAK[{J(id)}]={J(k(h["weak"]))}; LASTW[{J(id)}]={J([k(x) for x in h["lastw"]])};')
    a = h['artx']
    L.append(f'  ARTX[{J(id)}]={J({"n":k(a["n"]),"r":a["r"],"k":k(a["k"]),"x":k(a["x"])})};')
    L.append(f'  SK[{J(id)}]={J(h["sk"])};')
    r = h['npr']; L.append(f'  NPR[{J(id)}]={{r:{J(r[0])},s:{J(r[1])}}};')
    kx, p, al = h['hx'].split(' '); L.append(f'  HX[{J(id)}]={{k:{J(kx)},p:{J(p)},a:{J(al)}}};')
    if h.get('hint'): L.append(f'  HINT_SRC[{J(h["frm"][0])}]={J(k(h["hint"]))};')
    if h.get('dragon'): L.append(f'  DRAGON[{J(id)}]=1;')
    if h.get('field'): L.append(f'  FIELD_SP[{J(id)}]={J(h["field"])};')
    if h.get('sup'): L.append(f'  SUP_SP[{J(id)}]={J(h["sup"])};')
    if h.get('wall'): L.append(f'  WALL_SP[{J(id)}]={J(h["wall"])};')
    if h.get('varsc'): L.append(f'  VAR_SC[{J(id)}]={J(h["varsc"])};')
    if h.get('snipe'): L.append(f'  SNIPE[{J(id)}]={h["snipe"]};')
    if h.get('ambush'): L.append(f'  AMBUSH[{J(id)}]={h["ambush"]};')
    if h.get('npi'):
        tbl = {'A':'NPI_A','F':'NPI_F','D':'NPI_D','S':'NPI_S','H':'NPI_S','B':'NPI_S','W':'NPI_S','X':'NPI_A'}[r[0]]
        L.append(f'  {tbl}[{J(id)}]={J(k(h["npi"]))};')
for n, (kind, t) in mod.SKX.items():
    L.append(f'  SKX[{J(n)}]={{k:{J(kind)},x:{J(k(t))}}};')
    if n in getattr(mod, 'SKN', {}): TR.append((n,) + tuple(mod.SKN[n]))
for a, b_, t in mod.RIVAL:
    L.append(f'  RIVAL[{J(a)}]=Object.assign(RIVAL[{J(a)}]||{{}},{{{J(b_)}:{J(k(t))}}});')
block = '\n'.join(L) + '\n'
anchor = '  // ---- 에필로그 연작'
assert s.count(anchor) == 1
s = s.replace(anchor, block + anchor)

# 3) 번역
m = re.search(r'const I18N_DICT=(\{.*?\});\n', s, re.S); D = json.loads(m.group(1))
add = 0
for ko, en, ja in TR:
    if ko in D['en'] and D['en'][ko] != en: continue  # 이미 있는 번역은 그대로
    D['en'][ko] = en; D['ja'][ko] = ja; add += 1
s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
open(P, 'w', encoding='utf-8').write(s)
print('heroes', len(heroes), 'lines', len(L), 'tr added', add, 'of', len(TR))

