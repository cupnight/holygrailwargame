"""에미야[얼터] 덧붙임 (11-12): 보구 특례(오키타와 같은 틀: 대마력·회피·결계에 깎이지 않음) · 키아라와의 관계 대사 넷.
batch5 주입과 bx_patch 뒤에 쓴다. 사용: python3 ea_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
ID = 'emiya_alter'
L1 = '에미야[얼터]: “그 수녀… 어디서 본 얼굴이야. 기억은 안 나는데 손가락이 방아쇠를 찾아. 마스터, 저건 가까이 두지 마.”'
L2 = '“역시 그 여자였나. 머리는 잊어도 총은 기억하고 있었군. 이번에야말로 끝낸다.”'
K3 = '어머, 또 당신인가요. 닳고 닳아도 저를 쫓아오시다니, 그것도 사랑이랍니다.'
R4 = '구원 타령은 됐어. 네가 삼킨 것들 값은 납으로 받지.'
L5 = '에미야[얼터]: “…끝났다. 몇 번을 쫓았는지도 잊었는데. 이제 잊어도 되겠군.”'
TR = [(L1, 'EMIYA (Alter): “That nun... I\'ve seen her face somewhere. I can\'t remember, but my finger keeps looking for the trigger. Master, don\'t let that one get close.”', 'エミヤ〔オルタ〕: 「あのシスター……どこかで見た顔だ。思い出せんが、指が引き金を探している。マスター、あれは近づけるな」'),
      ('에미야[얼터]: ' + L2, 'EMIYA (Alter): “So it was that woman after all. My head forgot, but the gun remembered. This time I end it.”', 'エミヤ〔オルタ〕: 「やはりあの女だったか。頭は忘れても銃は覚えていたらしい。今度こそ終わらせる」'),
      (K3, 'Oh my, you again. Worn down to nothing and still chasing me. That, too, is love, you know.', 'あら、またあなたですか。擦り切れてもなお私を追っていらっしゃるなんて、それも愛ですのよ。'),
      (R4, "Spare me the salvation talk. I'll collect for everything you swallowed, in lead.", '救いの講釈は結構だ。お前が呑み込んだものの代金は、鉛で払ってもらう。'),
      (L5, 'EMIYA (Alter): “...It\'s done. I\'d even forgotten how many times I chased her. Now I can let it go.”', 'エミヤ〔オルタ〕: 「……終わった。何度追ったかも忘れていたが。もう忘れていい」')]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:60], s.count(o))); return
        s = s.replace(o, n)
    # 보구 특례: 오키타와 같은 처리 세 곳
    rp("att.sp==='gate'||att.id==='okita'?1:", "att.sp==='gate'||att.id==='okita'||att.id==='emiya_alter'?1:")
    rp("(side==='me'?b.e.hero:hero().id)==='okita') return m;", "['okita','emiya_alter'].includes(side==='me'?b.e.hero:hero().id)) return m;")
    rp("x.o.h.id==='gilgamesh'||x.o.h.id==='okita') return m;", "x.o.h.id==='gilgamesh'||x.o.h.id==='okita'||x.o.h.id==='emiya_alter') return m;")
    # 키아라: 수녀 조의 소문(강림 전) · 강림 · 결전 입장 · 쓰러뜨렸을 때
    rp("if(c.kamaHint===w.day&&S.hero==='kama'){", "if(c.kamaHint===w.day&&S.hero==='emiya_alter') log(" + repr(L1) + ",'voice');\n    if(c.kamaHint===w.day&&S.hero==='kama'){")
    rp("kama:{desc:'“역시. 어쩐지 마음에 안 들더라니.”'}};", "kama:{desc:'“역시. 어쩐지 마음에 안 들더라니.”'},\n      emiya_alter:{desc:" + repr(L2) + "}};")
    rp("    const comp=(ctx.comp||[]).map(i=>pairBy(i)).filter(p=>p&&p.alive).map(p=>pName(p));\n    return {line,reply,fx:{t:'boss',",
       "    if(e.bx&&first&&!fin&&w.heroAlive&&h&&h.id==='emiya_alter'){ line=" + repr(K3) + "; reply=" + repr(R4) + "; }\n    const comp=(ctx.comp||[]).map(i=>pairBy(i)).filter(p=>p&&p.alive).map(p=>pName(p));\n    return {line,reply,fx:{t:'boss',")
    rp("그 몸이 단꿈처럼 녹아 사라졌다.','war');", "그 몸이 단꿈처럼 녹아 사라졌다.','war'); if(by==='me'&&w.heroAlive&&S.hero==='emiya_alter') log(" + repr(L5) + ",'voice');")
    s, nd, nt = i18n.add(s, TR, [])
    open(P, 'w', encoding='utf-8').write(s); print('ea miss', miss, 'tr', nd)
