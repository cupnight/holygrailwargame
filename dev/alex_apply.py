"""이스칸다르의 소원을 수육으로 (11-12). 소원 문구 · 소원 대사 · 성배 앞 「소원을 빈다」(맑은 성배 + 신뢰 60 이상이면 수육 결말, 모자라면 몸을 얻지 못하고 떠난다) · 에필로그 「그의 소원」.
오케아노스는 '꿈'으로 남긴다. 사용: python3 alex_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
W0, W1 = '세계의 끝에 있다는 바다를 보는 것', '제 몸을 얻어 이 세계에 다시 서는 것'
V0 = '짐의 소원 말이냐? 세계의 끝, 오케아노스의 바다를 이 눈으로 보는 것이다!'
V1 = '짐의 소원 말이냐? 몸이다! 피가 돌고 배가 고픈 제 몸으로 이 땅을 다시 밟는 것이다. 정복도 오케아노스도, 그 다음에 짐의 발로 이룰 일이니라!'
N1 = '성배가 빛났다. 그러나 빛은 이스칸다르의 몸에 머물지 못하고 흩어졌다. 그를 이 세계에 붙들어 둘 인연이 아직 모자랐다.'
N2 = '이스칸다르: “하하, 닻이 모자랐구나! 좋다, 이 몸은 다음 원정에서 얻으마. 그때까지 잘 있거라, 마스터!”'
E1 = '이스칸다르가 몸을 얻은 뒤로 미뤄 둔 꿈, ‘세계의 끝에 있다는 바다를 보는 것’을 이제 제 발로 해 보겠다고 한다.'
TR = [(W1, 'To gain a body of his own and stand in this world once more', '己の肉体を得て、この世界に再び立つこと'),
      (V1, 'Our wish, you ask? A body! To tread this earth again in flesh of our own, with blood that runs and a belly that hungers. Conquest and Okeanos both come after — on our own two feet!',
       '余の願いか？肉体よ！血が巡り腹の減る己の体で、この大地を再び踏むことだ。征服もオケアノスも、その後に余の足で成すことよ！'),
      (N1, "The Grail shone. But its light could not stay in Iskandar's body, and scattered. The bond to hold him in this world was not yet enough.",
       '聖杯が輝いた。だが光はイスカンダルの身体に留まれず、散っていった。彼をこの世界に繋ぎ止める縁が、まだ足りなかった。'),
      (N2, 'Iskandar: “Haha, so it was the anchor that fell short! Very well, we shall win this body on the next campaign. Until then, be well, Master!”',
       'イスカンダル: 「ははは、錨が足りなんだか！よい、この体は次の遠征で手に入れるとしよう。それまで達者でな、マスター！」'),
      (E1, 'Iskandar says that the dream he set aside until he had a body — “To see the sea that lies at the end of the world” — he will now pursue on his own two feet.',
       'イスカンダルは、肉体を得るまで後回しにしていた夢――「世界の果てにあるという海を見ること」を、今こそ己の足で果たすと言う。')]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:60], k)); return
        s = s.replace(o, n)
    rp("traits:['야망','자유'],wish:'" + W0 + "'", "traits:['야망','자유'],wish:'" + W1 + "'")
    rp("      wish:'" + V0 + "',", "      wish:'" + V1 + "',")
    # 성배 앞: 맑은 성배 + 신뢰 60 이상이면 소원이 곧 수육
    rp("f:()=>{S.flags.wishText=`${h.name}의 소원 — ${h.wish}`;grantHero(shared)}});",
       "f:()=>{S.flags.wishText=`${h.name}의 소원 — ${h.wish}`; if(h.id==='alexander'&&w.cupPure&&w.trust>=STAY_NEED) grantStay(shared); else grantHero(shared)}});")
    rp("    else if(pure){ log(`성배가 빛났다. ${h.name}${J(h.name,은)} 오래 눈을 감았다가 떴다.`,'voice');",
       "    else if(pure&&h.id==='alexander'){ log('" + N1 + "','voice'); log('" + N2 + "','voice'); add({bond:6}); }\n"
       "    else if(pure){ log(`성배가 빛났다. ${h.name}${J(h.name,은)} 오래 눈을 감았다가 떴다.`,'voice');")
    # 에필로그 「그의 소원」: 몸은 이미 얻었다. 미뤄 둔 꿈을 꺼낸다
    rp(":`${h.name}${J(h.name,이)} 그 겨울 성배에 빌려던 소원, ‘${h.wish}’${J(h.wish,을)} 이 세계에서 직접 해 보겠다고 한다.`,choices:[",
       ":h.id==='alexander'?'" + E1 + "':`${h.name}${J(h.name,이)} 그 겨울 성배에 빌려던 소원, ‘${h.wish}’${J(h.wish,을)} 이 세계에서 직접 해 보겠다고 한다.`,choices:[")
    s, nd, nt = i18n.add(s, TR, [])
    open(P, 'w', encoding='utf-8').write(s); print('alex miss', miss, 'tr', nd)
