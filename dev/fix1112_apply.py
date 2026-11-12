"""11-12 문의 반영. ① 교회의 의뢰: 사도 마스터를 암살해도 령주 한 획을 받는다 ② 우정 3단계 이름 「죽마고우」 → 「지기」(EN Sworn Friends · JA 無二の友).
빌드 맨 끝에 쓴다. 사용: python3 fix1112_apply.py <game.html>"""
import sys
EN = [("If a witch's lifelong friend cries", "If a witch's sworn friend cries"),
      ("We're friends for life, aren't we? Only grieve for one day, okay?", "We're sworn friends, aren't we? Only grieve for one day, okay?"),
      ("In life I had lots of friends, but never a lifelong one.", "In life I had lots of friends, but never a sworn one."),
      ("I can't stand to see my oldest friend in tears.", "I can't stand to see my sworn friend in tears."),
      ("So this is what a lifelong friend is. Parting with a smile.", "So this is what a sworn friend is. Parting with a smile."),
      ("That you're my lifelong friend.", "That you're my sworn friend."),
      ("Kept the Day of the Oath with your lifelong friend", "Kept the Day of the Oath with your sworn friend"),
      ('":"Lifelong Friends"', '":"Sworn Friends"'),
      ("Close Friends → Lifelong Friends)", "Close Friends → Sworn Friends)"),
      ("A lifelong friend crying is an ugly sight.", "A sworn friend crying is an ugly sight."),
      ("'Lifelong friend' — didn't get it at first", "'Sworn friend' — didn't get it at first"),
      ("have become “Lifelong Friends.”", "have become “Sworn Friends.”"),
      ('"Lifelong friends with {0}"', '"Sworn friends with {0}"')]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:60], k)); return
        s = s.replace(o, n)
    # ① 교회의 의뢰
    PAY = "W().churchQuest=-1; W().seals++; log('며칠 뒤 신부가 찾아와 당신 손등에 령주 한 획을 그려 주었다. “약속드린 보답입니다.”','seal');"
    rp("    e.master=false; e.mDied=true; e.byMe=true; S.flags.killedMaster=S.flags.killedMaster||1;\n",
       "    e.master=false; e.mDied=true; e.byMe=true; S.flags.killedMaster=S.flags.killedMaster||1;\n"
       "    if(W().churchQuest===e.i){ " + PAY + " }   // 사도는 마스터 쪽이다: 암살로 끝내도 의뢰는 이루어진 것\n")
    # ② 죽마고우 → 지기
    n = s.count('죽마고우'); s = s.replace('죽마고우', '지기'); m = s.count('竹馬の友'); s = s.replace('竹馬の友', '無二の友')
    for o, x in EN: rp(o, x)
    open(P, 'w', encoding='utf-8').write(s); print('fix1112 miss', miss, 'ko', n, 'ja', m)
