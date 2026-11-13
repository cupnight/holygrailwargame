"""11-13 문의 반영. 인질 구출전과 결투장.
① 구출전에서 말로 싸움을 끝내도(상대가 먼저 무기를 거둠) 인질을 데려온다. 예전엔 결과가 비어 있어 '구출 실패'로 셌다.
   덤으로 그 싸움 기록이 '— undefined'로 남던 것도 '대화로 끝남'으로 바로잡힌다.
② 인질 사건이 난 날에는 마스터들의 사연(결투장 · 면전의 도발 등 '오늘 밤 결판' 약속)이 같이 오지 않는다.
   예전엔 같은 날 둘 다 받으면 구출이 먼저고 결투는 말없이 다음 밤으로 밀렸다.
사용: python3 fix1113_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # ① 말로 끝낸 싸움에 결과를 남긴다
    rp("      return endBattle(); }\n    if(ch(.45-bd/250)){",
       "      b.res='talk'; return endBattle(); }\n    if(ch(.45-bd/250)){")
    rp("const ok=w.heroAlive&&(['win','fled','asn'].includes(b.res)",
       "const ok=w.heroAlive&&(['win','fled','asn','talk'].includes(b.res)")
    # ② 인질 사건이 난 날은 마스터 사연을 쉬어 간다
    rp("w.hostDone=true; w.host={id:who.id,g:who.g,n:who.n,i:p.i,d:w.day};",
       "w.hostDone=true; w.hostDay=w.day; w.host={id:who.id,g:who.g,n:who.n,i:p.i,d:w.day};")
    rp("    const w=W(); if(w.ended||!w.heroAlive||S.pending||S.dead) return;\n    if(!force&&!ch(.42)) return;",
       "    const w=W(); if(w.ended||!w.heroAlive||S.pending||S.dead) return;\n    if(w.hostDay===w.day) return; // 인질 사건이 난 날: 그날 밤은 구출 하나로 정해져 있으니 '오늘 밤 결판' 약속이 겹치지 않게\n    if(!force&&!ch(.42)) return;")
    print('fix1113 miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
