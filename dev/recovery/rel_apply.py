# 신규 6명 관계 대사(RLU) · 짝 대사(PAIRV) · 번역 · 연인 허용 · 키아라 짝 대사 훅
import json, re, sys, runpy, os
H = os.path.dirname(os.path.abspath(__file__))
R = runpy.run_path(H + '/rel6.py')['R']
IDS = ['bb', 'meltryllis', 'passionlip', 'suzuka', 'tamamocat']
PAIRS = json.load(open(H + '/reltr/pairs.json', encoding='utf8'))

def parts(l):
    l = l.strip(); m = re.fullmatch(r'\(([^()]*)\)', l)
    if m: return m.group(1).strip(), None
    m = re.match(r'^\(([^()]*)\)\s*(.+)$', l)
    if m: return m.group(1).strip(), m.group(2).strip()
    return None, l
isT = lambda k: '{M}' in k or '{K}' in k
T = lambda x: x.replace('{M}', '{1}').replace('{K}', '{1}')

Dd, Tt, bad = {}, {}, []
def put(ko, en, ja):
    a, b, c = parts(ko), parts(en), parts(ja)
    if [x is None for x in a] != [x is None for x in b] or [x is None for x in a] != [x is None for x in c]:
        bad.append(ko); return
    for x, y, z in zip(a, b, c):
        if not x: continue
        if isT(x): Tt[T(x)] = [T(y), T(z)]
        else: Dd[x] = [y, z]

RLU_NEW = {}
for hid in IDS:
    tr = json.load(open(f'{H}/reltr/{hid}.json', encoding='utf8'))
    RLU_NEW[hid] = {}
    for track in ('love', 'friend'):
        d = R[hid][track]; RLU_NEW[hid][track] = d
        for slot, arr in d.items():
            for i, ko in enumerate(arr):
                k = f'{track}.{slot}.{i}'
                if k not in tr: bad.append('missing ' + hid + ' ' + k); continue
                en, ja = tr[k]
                if ko.count('{M}') != en.count('{M}') or ko.count('{K}') != en.count('{K}') or ko.count('{M}') != ja.count('{M}') or ko.count('{K}') != ja.count('{K}'):
                    bad.append('placeholder ' + hid + ' ' + k)
                put(ko, en, ja)
    extra = set(tr) - {f'{t}.{s}.{i}' for t in ('love', 'friend') for s, a in R[hid][t].items() for i in range(len(a))}
    if extra: bad.append(('extra', hid, sorted(extra)[:3]))
PV = {}
for key, v in PAIRS.items():
    PV[key] = {hid: {k: x[0] for k, x in sl.items()} for hid, sl in v.items()}
    for hid, sl in v.items():
        for k, (ko, en, ja) in sl.items(): put(ko, en, ja)
print('번역 조각', len(Dd), '틀', len(Tt), '문제', bad[:5])
if bad: sys.exit(1)
json.dump({'D': Dd, 'T': Tt}, open(H + '/../kr/b5_tr.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)

for p in sys.argv[1:]:
    s = open(p, encoding='utf8').read(); miss = []
    def R_(o, n, opt=False):
        global s
        c = s.count(o)
        if c != 1:
            if not opt: miss.append((o[:50], c))
            return
        s = s.replace(o, n)
    # RLU
    m = re.search(r'  const RLU=(\{.*?\});\n', s, re.S); U = json.loads(m.group(1)); U.update(RLU_NEW)
    s = s[:m.start(1)] + json.dumps(U, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    # PAIRV (기준 파일에는 짝 대사 체계가 없다)
    m = re.search(r'const PAIRV=(\{.*?\});\n', s)
    if m:
        P = json.loads(m.group(1)); P.update(PV)
        s = s[:m.start(1)] + json.dumps(P, ensure_ascii=False) + s[m.end(1):]
        # 짝 대사가 생긴 세 쌍의 예전 한 줄 대사는 뺀다
        for a, b in [('bb','meltryllis'),('bb','passionlip'),('meltryllis','bb'),('meltryllis','passionlip'),('passionlip','bb'),('passionlip','meltryllis')]:
            s, n = re.subn(r'  RIVAL\["%s"\]=Object\.assign\(RIVAL\["%s"\]\|\|\{\},\{"%s":"[^"]*"\}\);\n' % (a, a, b), '', s)
            if n != 1: miss.append(('RIVAL', a, b, n))
        # 키아라: 위기 유닛이지만 짝 대사를 쓴다
        R_("function pairMeet(e){ const h=hero(); if(!h||e.cx||!e.hero||e.pairMet) return false;",
           "function pairMeet(e){ const h=hero(); if(!h||(e.cx&&e.hero!=='kiara')||!e.hero||e.pairMet) return false;")
        R_("if(e.cx){ const dead=cxUnitDown(e,by==='우리'?'me':null); if(dead&&by==='우리'&&W().battle){ W().battle.res='win'; mark(); } return; }",
           "if(e.cx){ const kh=e.cx==='boss'&&e.hero==='kiara'&&e.phase2&&by==='우리'&&W().battle&&W().heroAlive&&H_BY.kiara?hero():null, kf=kh&&pairL('kiara',kh.id,'fall'); if(kf) log(voiceLine(H_BY.kiara,kf),'enemy');   // 짝 대사: 키아라가 마지막으로 쓰러질 때\n"
           "      const dead=cxUnitDown(e,by==='우리'?'me':null); if(dead&&kf){ const kw=pairL(kh.id,'kiara','win'); if(kw) log(voiceLine(kh,kw),'voice'); }\n"
           "      if(dead&&by==='우리'&&W().battle){ W().battle.res='win'; mark(); } return; }")
        R_("eh=e&&!e.cx&&e.hero?H_BY[e.hero]:null", "eh=e&&(!e.cx||e.hero==='kiara')&&e.hero?H_BY[e.hero]:null")
        # BB · 멜트릴리스 · 패션립도 연인이 될 수 있다
        R_("'hessian','bb','meltryllis','passionlip'];", "'hessian'];")
    open(p, 'w', encoding='utf8').write(s); print(p[-22:], 'miss', miss)
