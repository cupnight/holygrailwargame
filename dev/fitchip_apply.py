"""11-13: 궁합 '어긋남'
① 칩 문구 (A안): 같은 장면에서 서번트가 그 선택을 좋게 본 칩(높이 샀다 · 마음에 든 · 눈이 빛났다)이 먼저 나왔으면
   앞의 칩과 이어지는 문구로. '마음을 닫았다'도 같은 결로.
② 인연 단계가 깊을수록 어긋남의 감점을 줄인다
   | 인연 | 오를 때 | 오히려 −2 · 말다툼 | 깎일 때 |
   | 없음 | ×0.5 | 25% | ×1.2 |
   | 1 호감 · 전우 | ×0.65 | 15% | ×1.15 |
   | 2 연모 · 절친 | ×0.8 | 5% | ×1.1 |
   | 3 연인 · 지기 | ×1 | 0% | ×1 |
   인연 1~2단계는 회색 칩 '궁합은 어긋나도, 쌓인 인연 덕에 조금씩 가까워진다', 3단계는 칩 없음.
사용: python3 fitchip_apply.py <game.html>"""
import sys, i18n
HALF = ('마음에 들어 했지만, 궁합이 어긋나 거리는 크게 줄지 않았다', 'They liked it, but your mismatch kept the distance from closing much', '気に入ってはいたが、相性が噛み合わず距離はあまり縮まらなかった')
SHUT = ('마음에 들어 했지만, 궁합이 어긋나 오히려 한 걸음 물러섰다', 'They liked it, but your mismatch made them take a step back instead', '気に入ってはいたが、相性が噛み合わず、かえって一歩退いた')
REL = ('궁합은 어긋나도, 쌓인 인연 덕에 조금씩 가까워진다', 'Your temperaments clash, but the bond you have built still draws you closer', '相性は噛み合わなくても、積み重ねた縁のおかげで少しずつ近づいていく')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 단계별 표
    rp("  const fitTier=w=>", "  // 11-13: 인연 단계(0~3)가 깊을수록 궁합 어긋남의 감점이 줄어든다\n"
       "  const FIT_UP=[.5,.65,.8,1], FIT_SHUT=[.25,.15,.05,0], FIT_DN=[1.2,1.15,1.1,1];\n"
       "  const fitRel=()=>{ const r=relOf(); return r&&r.stage?Math.min(3,r.stage):0; };\n"
       "  const fitTier=w=>")
    # 이벤트 · 령주로 오르는 신뢰
    rp("if(t==='어긋남'){ if(!good&&ch(.25)){ if(CHK) CHK.push({txt:'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; } if(CHK) CHK.push({txt:'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false}); return Math.round(n*.5); }",
       "if(t==='어긋남'){ const rs=fitRel(); if(rs>=3) return n;\n"
       "        const liked=!rs&&!!CHK&&CHK.some(x=>x.ok&&/높이 샀다|마음에 든|눈이 빛났다/.test(x.txt)); // 좋게 본 칩 뒤에는 이어지는 문구로\n"
       "        if(!good&&ch(FIT_SHUT[rs])){ if(CHK) CHK.push({txt:liked?'" + SHUT[0] + "':'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; }\n"
       "        if(CHK) CHK.push(rs?{txt:'" + REL[0] + "',eq:true}:{txt:liked?'" + HALF[0] + "':'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false}); return Math.round(n*FIT_UP[rs]); }")
    rp("return t==='잘 맞음'?Math.round(n*.8):t==='어긋남'?Math.round(n*1.2):n; }", "return t==='잘 맞음'?Math.round(n*.8):t==='어긋남'?Math.round(n*FIT_DN[fitRel()]):n; }")
    # 대화 · 외출
    rp("if(t==='어긋남'&&ch(.25)){ if(CHK) CHK.push({txt:'이야기가 어긋나 말다툼이 났다',ok:false}); return null; }",
       "const rs=fitRel(); if(t==='어긋남'&&ch(FIT_SHUT[rs])){ if(CHK) CHK.push({txt:'이야기가 어긋나 말다툼이 났다',ok:false}); return null; }")
    rp("    if(t==='어긋남'&&CHK) CHK.push({txt:'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false});\n    return Math.max(0,Math.round(base*(t==='잘 맞음'?1.2:t==='어긋남'?.5:1))+pref); }",
       "    if(t==='어긋남'&&CHK&&rs<3) CHK.push(rs?{txt:'" + REL[0] + "',eq:true}:{txt:'궁합이 어긋나 좀처럼 가까워지지 않는다',ok:false});\n    return Math.max(0,Math.round(base*(t==='잘 맞음'?1.2:t==='어긋남'?FIT_UP[rs]:1))+pref); }")
    s, nd, nt = i18n.add(s, [HALF, SHUT, REL])
    print('fitchip miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
