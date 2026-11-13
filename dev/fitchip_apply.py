"""11-13: 궁합 '어긋남' 칩 문구 (A안 · 규칙은 그대로)
같은 장면에서 서번트가 그 선택을 좋게 본 칩(높이 샀다 · 마음에 든 · 눈이 빛났다)이 먼저 나왔으면,
'좀처럼 가까워지지 않는다' 대신 앞의 칩과 이어지는 문구로 바꾼다. '마음을 닫았다'도 같은 결로.
사용: python3 fitchip_apply.py <game.html>"""
import sys, i18n
HALF = ('마음에 들어 했지만, 궁합이 어긋나 거리는 크게 줄지 않았다', 'They liked it, but your mismatch kept the distance from closing much', '気に入ってはいたが、相性が噛み合わず距離はあまり縮まらなかった')
SHUT = ('마음에 들어 했지만, 궁합이 어긋나 오히려 한 걸음 물러섰다', 'They liked it, but your mismatch made them take a step back instead', '気に入ってはいたが、相性が噛み合わず、かえって一歩退いた')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("if(t==='어긋남'){ if(!good&&ch(.25)){ if(CHK) CHK.push({txt:'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; } if(CHK) CHK.push({txt:'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false}); return Math.round(n*.5); }",
       "if(t==='어긋남'){ const liked=!!CHK&&CHK.some(x=>x.ok&&/높이 샀다|마음에 든|눈이 빛났다/.test(x.txt)); // 11-13: 좋게 본 칩 뒤에는 이어지는 문구로\n"
       "        if(!good&&ch(.25)){ if(CHK) CHK.push({txt:liked?'" + SHUT[0] + "':'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; } if(CHK) CHK.push({txt:liked?'" + HALF[0] + "':'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false}); return Math.round(n*.5); }")
    s, nd, nt = i18n.add(s, [HALF, SHUT])
    print('fitchip miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
