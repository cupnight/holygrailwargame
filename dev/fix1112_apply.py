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
    # ③ 사건 본문과 성유물을 저장해 두었다가, 시작 화면에 다녀와도 그대로 다시 보여 준다
    rp("    S.resumeEv={src:'GROW',id:e.id};\n", "    const K0=S.resumeEv&&S.resumeEv.src==='GROW'&&S.resumeEv.id===e.id&&S.resumeEv.body?S.resumeEv:null; if(K0&&K0.rel) S._rel=K0.rel;\n    S.resumeEv={src:'GROW',id:e.id};\n")
    rp("    decide({title:`${S.age}세`,body:orf(e.txt()),choices});\n  }\n  function rollEvent(){", "    const body=K0?K0.body:orf(e.txt()); S.resumeEv.body=body; S.resumeEv.rel=S._rel||null;\n    decide({title:`${S.age}세`,body,choices});\n  }\n  function rollEvent(){")
    rp("    S.resumeEv={src:'EV',id:e.id};\n    const body=orf(e.txt());\n", "    const K0=S.resumeEv&&S.resumeEv.src==='EV'&&S.resumeEv.id===e.id&&S.resumeEv.body?S.resumeEv:null; if(K0&&K0.rel) S._rel=K0.rel;\n    S.resumeEv={src:'EV',id:e.id};\n    const body=K0?K0.body:orf(e.txt()); S.resumeEv.body=body; S.resumeEv.rel=S._rel||null;\n")
    # ④ 선택 창: 제자리에서 밝아지기만 한다 · 뜬 직후 0.3초는 터치(마우스)를 받지 않는다(키보드 · 자동 결정은 그대로)
    rp("@keyframes rise{from{transform:translateY(12px);opacity:.6}to{transform:none;opacity:1}}", "@keyframes rise{from{opacity:.6}to{opacity:1}}")
    rp("function showDecision(d){\n", "function showDecision(d){\n  if(window.__dD!==d){ window.__dD=d; window.__dT=performance.now(); }\n")
    rp("function choose(i){ clearTimeout(autoTimer); const d=Sim.S.pending; if(!d) return;", "function choose(i){ { const ev=window.event; if(ev&&ev.isTrusted&&ev.type==='click'&&ev.detail>0&&performance.now()-(window.__dT||0)<300) return; } clearTimeout(autoTimer); const d=Sim.S.pending; if(!d) return;")
    # ⑤ 행운도 마력 공급을 따른다 (마스터의 정신과는 무관). 상대 조도 같다
    rp("const TIER_MOD={S:[.5,0,.5,1],A:[0,0,0,.5],B:[0,0,0,0],C:[-1,0,0,-1],D:[-1,-1,-1,-1]};", "const TIER_MOD={S:[.5,0,.5,1,.5],A:[0,0,0,.5,0],B:[0,0,0,0,0],C:[-1,0,0,-1,0],D:[-1,-1,-1,-1,-1]};")
    rp("    const luck = S.st.will>=65? .5 : S.st.will<25? -1 : 0;\n", "    const luck = m[4];\n")
    rp("    let o=h.s.map((r,i)=> i<4? rankShift(r,TIER_MOD[t][i]) : r);", "    let o=h.s.map((r,i)=> rankShift(r,TIER_MOD[t][i]));")
    # ⑥ 랭크를 한 단계 내릴 때 +는 그대로 둔다 (A+ → B+). 전에는 +까지 사라져 한 단계 반이 깎였다
    rp("    else { if(plus) { plus=0; if(d<=-1){ if(i>0) i--; else minus=true; } } else if(i>0) i--; else minus=true; }",
       "    else if(d<=-1){ if(i>0) i--; else if(plus) plus=0; else minus=true; }\n    else { if(plus) plus=0; else if(i>0) i--; else minus=true; }")
    # ② 죽마고우 → 지기
    n = s.count('죽마고우'); s = s.replace('죽마고우', '지기'); m = s.count('竹馬の友'); s = s.replace('竹馬の友', '無二の友')
    for o, x in EN: rp(o, x)
    open(P, 'w', encoding='utf-8').write(s); print('fix1112 miss', miss, 'ko', n, 'ja', m)
