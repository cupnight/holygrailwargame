"""11-14: 비스트(키아라) 결말에 안 맞는 에필로그 사건 정리
- 내가 키아라를 쓰러뜨린 결말(달로 간 잔)은 brokeCup을 세우므로 검은 성배의 '내가 성배를 부쉈다' 사건(cx_e1~5 · 부서진 잔의 행방 · 성배 조각 이야기)이 나오던 것 → 비스트 생에서는 cx_ 사건 · 조각 이야기를 모두 뺀다
- 승자의 이름 · 남은 세 획: '성배를 쥔' → 비스트 생에서는 '의식을 끝낸'
- 끝까지 남은 사람: 다른 조가 키아라를 쓰러뜨린 결말은 '성배는 달로 갔다', 검은 성배를 다른 조가 부순 결말은 '부쉈다' · 단꿈 생에서는 나오지 않음(서번트가 마지막 밤 흡수되므로 '며칠 앞두고 쓰러졌다'가 틀림)
- 끝까지 남은 사람: 키아라와의 결전에서 서번트가 쓰러진 경우 '마지막 밤, 결전에서 쓰러졌다'
- 먼저 떠난 서번트: 키아라에게 흡수된 경우 '녹아 사라진 그 밤'
- 물러난 겨울: 비스트 생에서는 '성배가 누구에게 갔는지' 대신 '그 겨울이 어떻게 끝났는지'
사용: python3 epi1114_apply.py <game.html>"""
import sys, i18n
BX = "((S.war||{}).crisis||{}).type==='beast3R'"
D = [
 ('마술협회에서 편지가 왔다. 그 겨울 의식을 끝낸 마술사의 증언을 기록으로 남기고 싶다고 했다. 사례는 넉넉하다.',
  "A letter came from the Mage's Association. They want to record the testimony of the magus who ended the ritual that winter. The compensation is generous.",
  '魔術協会から手紙が届いた。あの冬に儀式を終わらせた魔術師の証言を記録に残したいという。謝礼は十分だ。'),
 ('의식을 끝내고도 령주 세 획이 그대로 남았다. 성당교회가 그것을 회수하고 싶어 한다.',
  'Even after the ritual ended, all three strokes of the Command Spells remained. The Holy Church wants to recover them.',
  '儀式を終えても、令呪三画はそのまま残った。聖堂教会はそれを回収したがっている。'),
 ('키아라는 다른 조가 쓰러뜨렸고, 성배는 달로 갔다. 그래도 당신과 서번트는 마지막 밤까지 살아남았다. 그 사실을 아는 사람은 거의 없다.',
  'Another team brought Kiara down, and the Grail went to the moon. Even so, you and your Servant survived until the last night. Almost no one knows that.',
  'キアラを倒したのは他の陣営で、聖杯は月へ行った。それでもあなたとサーヴァントは最後の夜まで生き延びた。そのことを知る人はほとんどいない。'),
 ('성배는 다른 조가 부쉈다. 그래도 당신과 서번트는 마지막 밤까지 살아남았다. 그 사실을 아는 사람은 거의 없다.',
  'Another team destroyed the Grail. Even so, you and your Servant survived until the last night. Almost no one knows that.',
  '聖杯を壊したのは他の陣営だった。それでもあなたとサーヴァントは最後の夜まで生き延びた。そのことを知る人はほとんどいない。'),
 ('그 겨울 끝까지 가지 않고 물러났다. 그 겨울이 어떻게 끝났는지는 신문 한 줄로 알았다.',
  'That winter, you withdrew instead of going to the end. You learned how that winter ended from a single line in the newspaper.',
  'あの冬、最後まで行かずに退いた。あの冬がどう終わったのかは新聞の一行で知った。'),
 ('찾아보았지만, 감독관의 기록에는 ‘의식 종료’라는 한 줄뿐이었다.',
  'You looked into it, but the overseer\'s record held only one line: "Ritual concluded."',
  '調べてみたが、監督役の記録には「儀式終了」の一行しかなかった。'),
]
T = [('{0}{1} 녹아 사라진 그 밤', 'the night {0} melted away', '{0}が溶けて消えたあの夜'),
     ('{0~은} 마지막 밤, 키아라와의 결전에서 쓰러졌다. 그래도 당신은 그 겨울의 끝까지 버텼다. 그 사실을 아는 사람은 거의 없다.',
      '{0} fell on the final night, in the last battle against Kiara. Even so, you held out to the end of that winter. Almost no one knows that.',
      '{0}は最後の夜、キアラとの決戦で倒れた。それでもあなたはあの冬の終わりまで耐え抜いた。そのことを知る人はほとんどいない。')]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 비스트 생: 검은 성배 사건(cx_) 모두 빼기 · '내가 부쉈다' 판정에서 비스트 제외(조각 이야기도 함께 빠짐)
    rp("const epiBlock=id=>(/^cx_j\\d$/.test(id)&&", "const epiBlock=id=>(/^cx_/.test(id)&&")
    rp("const cxMeBreak=()=>!!(WV().crisis&&S.flags.brokeCup&&", "const cxMeBreak=()=>!!(WV().crisis&&WV().crisis.type!=='beast3R'&&S.flags.brokeCup&&")
    # 승자의 이름
    rp("body:'마술협회에서 편지가 왔다. 그 겨울 성배를 쥔 마술사의 증언을 기록으로 남기고 싶다고 했다. 사례는 넉넉하다.'",
       "body:" + BX + "?" + repr(D[0][0]) + ":'마술협회에서 편지가 왔다. 그 겨울 성배를 쥔 마술사의 증언을 기록으로 남기고 싶다고 했다. 사례는 넉넉하다.'")
    # 남은 세 획
    rp("body:'성배를 쥐고도 령주 세 획이 그대로 남았다. 성당교회가 그것을 회수하고 싶어 한다.'",
       "body:" + BX + "?" + repr(D[1][0]) + ":'성배를 쥐고도 령주 세 획이 그대로 남았다. 성당교회가 그것을 회수하고 싶어 한다.'")
    # 끝까지 남은 사람
    rp("{id:'survivor',w:2,c:()=>S.flags.war==='survived'||", "{id:'survivor',w:2,c:()=>!S.flags.bxDream&&S.flags.war==='survived'||!S.flags.bxDream&&")
    rp(":'성배는 다른 이에게 갔다. 그래도 당신과 서번트는 마지막 밤까지 살아남았다. 그 사실을 아는 사람은 거의 없다.',",
       ":S.flags.bxNpc?" + repr(D[2][0]) + ":S.flags.cxNpcBreak?" + repr(D[3][0]) + ":'성배는 다른 이에게 갔다. 그래도 당신과 서번트는 마지막 밤까지 살아남았다. 그 사실을 아는 사람은 거의 없다.',")
    # 키아라와의 결전에서 쓰러진 경우: '며칠 앞두고'가 아니라 마지막 밤
    rp("const late=S.flags.war!=='survived', h=H_BY[S.hero];", "const late=S.flags.war!=='survived', h=H_BY[S.hero], bxL=late&&" + BX + "&&(WV().myOut||{}).by==='boss';")
    rp("body:late?`${h.name}${J(h.name,은)} 마지막 밤을 며칠 앞두고", "body:bxL?`${h.name}${J(h.name,은)} 마지막 밤, 키아라와의 결전에서 쓰러졌다. 그래도 당신은 그 겨울의 끝까지 버텼다. 그 사실을 아는 사람은 거의 없다.`:late?`${h.name}${J(h.name,은)} 마지막 밤을 며칠 앞두고")
    rp("return late?`14일을 공책 두 권에 적었다. 마지막 며칠은", "return late&&!bxL?`14일을 공책 두 권에 적었다. 마지막 며칠은")
    # 먼저 떠난 서번트
    rp(":/빼앗/.test(why)?`${h.name}${RO(h.name)} 빼앗긴 그 밤`:", ":/빼앗/.test(why)?`${h.name}${RO(h.name)} 빼앗긴 그 밤`:/키아라에게 흡수/.test(why)?`${h.name}${RI(h.name)} 녹아 사라진 그 밤`:")
    # 물러난 겨울
    rp("body:'그 겨울 끝까지 가지 않고 물러났다. 성배가 누구에게 갔는지는 신문 한 줄로 알았다.'",
       "body:" + BX + "?" + repr(D[4][0]) + ":'그 겨울 끝까지 가지 않고 물러났다. 성배가 누구에게 갔는지는 신문 한 줄로 알았다.'")
    rp("return p?`성배를 쥔 것은 ${p.mname}였다.", "return " + BX + "?" + repr(D[5][0]) + ":p?`성배를 쥔 것은 ${p.mname}였다.")
    s, nd, nt = i18n.add(s, D, T)
    print('epi1114 miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
