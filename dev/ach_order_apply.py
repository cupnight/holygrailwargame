"""업적 화면: 분류 안에서 업데이트된 순서(오래된 것 → 새것)로, 분류 순서는 고정 (11-13).
ACH_SINCE는 업적이 처음 게임에 들어간 날(저장소 기록 기준. 10-30은 저장소 이전부터 있던 것). 같은 날은 원래 목록 순서.
새 업적을 더할 때 ACH_SINCE에 넣지 않으면 가장 새것으로 맨 뒤에 붙는다.
사용: python3 ach_order_apply.py <game.html>"""
import sys, json
ACH_SINCE = {"grail": "2026-10-30","shared": "2026-10-30","yield": "2026-10-30","stay": "2026-10-30","dark": "2026-10-30","fast": "2026-10-30","refused": "2026-10-30","kill1": "2026-10-30","kill4": "2026-10-30","noseal": "2026-10-30","coal": "2026-10-30","siege": "2026-10-30","backstab": "2026-10-30","bond": "2026-10-30","frags": "2026-10-30","misfit": "2026-10-30","mend": "2026-10-30","recontract": "2026-10-30","names": "2026-10-30","century": "2026-10-30","kids2": "2026-10-30","putdown": "2026-10-30","novel": "2026-10-30","nextwar": "2026-10-30","seven": "2026-10-30","lives10": "2026-10-30","halfdex": "2026-10-30","h_vanish": "2026-10-30","h_taint": "2026-10-30","h_rite": "2026-10-30","h_master": "2026-10-30","h_sibling": "2026-10-30","h_verdict": "2026-10-30","h_mad": "2026-10-30","cxseal": "2026-10-31","cxkey": "2026-10-31","cxflood": "2026-10-31","cxwinter": "2026-11-02","cxbreak": "2026-11-02","cxcall": "2026-11-02","cxmud": "2026-11-02","cxsolo": "2026-11-02","cxhunt": "2026-11-02","cxguard": "2026-11-02","selfpath": "2026-11-06","threeways": "2026-11-06","bodyart": "2026-11-06","familyname": "2026-11-06","untaught": "2026-11-06","baptnight": "2026-11-06","beyondarc": "2026-11-06","arts10": "2026-11-06","eyes5": "2026-11-06","h_jewel": "2026-11-06","h_word": "2026-11-06","rl_friend": "2026-11-09","rl_call": "2026-11-09","rl_fest": "2026-11-09","rl_wed": "2026-11-09","rl_blood": "2026-11-09","rl_oath": "2026-11-09","rl_autumn": "2026-11-09","rl_dream": "2026-11-09","rl_meet": "2026-11-09","rel10": "2026-11-09","h_jeal": "2026-11-09","h_late": "2026-11-09","bxmoon": "2026-11-12","bxleft": "2026-11-12","bxfive": "2026-11-12","bxwinter": "2026-11-13","bxname": "2026-11-13","bxother": "2026-11-13","bxconf": "2026-11-13","bxdoor": "2026-11-13","bxvillain": "2026-11-13","bxfirst": "2026-11-13","bxfreed": "2026-11-13","bxguard": "2026-11-13","bxbare": "2026-11-13","bxsolo": "2026-11-13","bx13": "2026-11-13","bxnobb": "2026-11-13","bxkama": "2026-11-13","bxego": "2026-11-13","bxsweet": "2026-11-13","bxmoonnews": "2026-11-13"}
CATS = ['성배전쟁의 끝','싸움','서번트와 나','삶','기록','숨겨진 업적']
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("function renderAch(c){ const cats=[...new Set(Sim.ACH.map(a=>a.cat))].filter(k=>!SK_CAT.has(k)),",
       "const ACH_SINCE=" + json.dumps(ACH_SINCE, ensure_ascii=False, separators=(',',':')) + ", ACH_CATS=" + json.dumps(CATS, ensure_ascii=False) + ";\n"
       "// 분류 안에서는 처음 들어간 날 순서(오래된 것 → 새것), 같은 날은 원래 목록 순서. 날이 없으면 가장 새것\n"
       "const achSorted=L=>L.map((a,i)=>[a,ACH_SINCE[a.id]||'9999',i]).sort((x,y)=>x[1]<y[1]?-1:x[1]>y[1]?1:x[2]-y[2]).map(x=>x[0]);\n"
       "const achCatRank=k=>{ const i=ACH_CATS.indexOf(k); return i<0?99:i; };\n"
       "function renderAch(c){ const cats=[...new Set(Sim.ACH.map(a=>a.cat))].filter(k=>!SK_CAT.has(k)).sort((x,y)=>achCatRank(x)-achCatRank(y)),")
    rp("...cats.map(cat=>[cat,Sim.ACH.filter(a=>a.cat===cat)])]", "...cats.map(cat=>[cat,achSorted(Sim.ACH.filter(a=>a.cat===cat))])]")
    print('achorder miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
