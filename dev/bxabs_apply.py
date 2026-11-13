"""11-13: 봉인 중(2단계)에 쓰러진 서번트가 KP 자리가 없어 키아라에게 흡수될 때, 조용히 지나가지 않게 단서 한 줄을 남긴다 (A안).
- 내가 본 경우(내 서번트 · 내 전투의 상대): 그 자리에서 바로
- 다른 조끼리의 싸움: 다음 날 소문으로
키아라의 이름은 드러내지 않고 '성배가 있던 쪽'으로만 가리킨다.
사용: python3 bxabs_apply.py <game.html>"""
import sys, i18n
SEEN = ('{0}의 영기가 흩어지지 않고 어딘가로 빨려 들어갔다. 성배가 있던 쪽이었다.',
        "{0}'s spirit did not scatter. It was drawn away somewhere — toward where the Grail had been.",
        '{0}の霊基は散らず、どこかへ吸い込まれていった。聖杯があった方角だった。')
RUMOR = ('어젯밤 쓰러진 서번트의 빛이 흩어지지 않고 한쪽으로 흘러갔다는 소문이 돌았다. 성배가 있던 쪽이었다.',
         "Word spread that the light of a Servant who fell last night did not scatter, but flowed off in one direction — toward where the Grail had been.",
         '昨夜倒れたサーヴァントの光が散らず、一方へ流れていったという噂が立った。聖杯があった方角だった。')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    o = "    c.absorbed=(c.absorbed||0)+1; if(c.stage===3) log(`쓰러진 ${H_BY[hid].name}의 영기가 키아라에게 녹아들었다.`,'war'); }"
    n = ("    c.absorbed=(c.absorbed||0)+1; if(c.stage===3) log(`쓰러진 ${H_BY[hid].name}의 영기가 키아라에게 녹아들었다.`,'war');\n"
         "    else if(c.stage===2){ const w=W(), src=o&&o.src, seen=!!(o&&o.mine)||!!(src&&w.battle&&w.battle.e===src)||!!(src&&src.out&&src.out.by==='me'); // 11-13: 봉인 중 흡수도 단서로\n"
         "      const nm=o&&o.mine?H_BY[hid].name:src?pName(src):H_BY[hid].name;\n"
         "      if(seen) log(`${nm}의 영기가 흩어지지 않고 어딘가로 빨려 들어갔다. 성배가 있던 쪽이었다.`,'war'); else bxLater(1,'" + RUMOR[0] + "'); } }")
    rp(o, n)
    s, nd, nt = i18n.add(s, [RUMOR], [SEEN])
    print('bxabs miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
