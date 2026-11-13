"""11-13: 봉인 1~2일 뒤 BB의 쪽지 — 센티넬을 잡으면 나중에 이롭다는 걸 이유는 숨긴 채 돌려 말한다 (상세안 18-M: BB는 직접 말하지 못한다)
- BB가 내 서번트가 아닐 때(달에서 온 유닛 · NPC 조), 봉인 중이고 BB와 내 서번트가 살아 있을 때만
- 이미 센티넬을 잡았으면 문구가 달라진다
사용: python3 bxnote_apply.py <game.html>"""
import sys, json, i18n
A = ('한밤중, 창틀에 분홍색 쪽지가 끼워져 있었다. “선배, 술래잡기 좋아해요? 밤마다 돌아다니는 그 아이들, 하나씩 잡아 주면… 나중에 선배가 덜 아플 거예요. 왜냐고요? 비밀♪ — BB”',
     'Late at night, a pink note was tucked into your window frame. “Senpai, do you like playing tag? Those kids wandering around every night — if you catch them one by one… it’ll hurt you less later. Why, you ask? It’s a secret♪ — BB”',
     '真夜中、窓枠にピンク色のメモが挟まっていた。「センパイ、鬼ごっこは好きですか？ 夜な夜なうろついてるあの子たち、一人ずつ捕まえてくれたら……あとでセンパイが痛い思いをしなくて済みますよ。なんでかって？ ヒミツです♪ ——BB」')
B = ('한밤중, 창틀에 분홍색 쪽지가 끼워져 있었다. “선배, 벌써 술래잡기 시작했네요? 그 아이들, 남김없이 잡아 주면… 나중에 선배가 덜 아플 거예요. 왜냐고요? 비밀♪ — BB”',
     'Late at night, a pink note was tucked into your window frame. “Senpai, you’ve already started playing tag? If you catch every last one of those kids… it’ll hurt you less later. Why, you ask? It’s a secret♪ — BB”',
     '真夜中、窓枠にピンク色のメモが挟まっていた。「センパイ、もう鬼ごっこ始めてたんですね？ あの子たち、残らず捕まえてくれたら……あとでセンパイが痛い思いをしなくて済みますよ。なんでかって？ ヒミツです♪ ——BB」')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    o = "    if(at!=='me') bxLater([2,3],'BB가 센티넬을 막아서는 걸 봤다는 사람이 있다.');"
    rp(o, o + "\n    if(at!=='me') bxLater([1,2],()=>{ const w=W(); return c.stage===2&&!c.revealD&&w.heroAlive&&bxBBP()?((c.kpMe||0)>0?" + json.dumps(B[0], ensure_ascii=False) + ":" + json.dumps(A[0], ensure_ascii=False) + "):''; },'voice'); // 11-13: BB의 쪽지")
    s, nd, nt = i18n.add(s, [A, B])
    print('bxnote miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
