"""11-14: 생의 기록 · 성배전쟁 기록에서 비스트(키아라) 결말이 검은 성배 결말처럼 보이던 것
- 내가 키아라를 쓰러뜨린 결말은 안에서 '성배를 쥠(victor)'과 '성배가 부서짐'을 세우므로
  기록에 '성배를 손에 쥐었다 · 성배는 오염되어 있었다 · 후반 위기 · 검은 성배를 부쉈다'가 나왔다
- 판정용 키(warKey)는 그대로 두고, 보여 주는 문구만 비스트 결말에 맞춘다(이미 저장된 기록도 함께 고쳐 보인다)
  · 결말: 셋쇼인 키아라를 쓰러뜨렸다 / 배지: 키아라 처치
  · 위기 줄: 후반 위기 · 비스트 Ⅲ/R · 키아라를 쓰러뜨렸다 / 다른 조가 키아라를 쓰러뜨렸다 / 도시가 단꿈에 잠겼다
  · 다른 조가 끝낸 경우: '성배를 쥔 것은 ○ 조' → '키아라를 쓰러뜨린 것은 ○ 조'
  · 성배가 맑았는지/오염되었는지 줄은 비스트 생에서 뺀다
- 업적 「성배를 쥔 자」 · 「일주일 안의 기적」 · 「령주 없이」 · 「등 뒤의 칼」 · 「어긋난 짝」은 키아라 결말에서 달성되지 않는다
- 새로 남기는 기록: wd.cx.bx(me/npc/dream) · 비스트 생은 cx.end · cup을 남기지 않는다
사용: python3 bxrec_apply.py <game.html>"""
import sys, i18n
D = [('키아라 처치', 'Kiara defeated', 'キアラ撃破'),
     ('키아라를 쓰러뜨렸다', 'Defeated Kiara', 'キアラを倒した'),
     ('다른 조가 키아라를 쓰러뜨렸다', 'Another team defeated Kiara', '他の陣営がキアラを倒した'),
     ('도시가 단꿈에 잠겼다', 'The city sank into a sweet dream', '街は甘い夢に沈んだ'),
     ]
T = [('키아라를 쓰러뜨린 것은 {0} 조 · {1}', 'Kiara was defeated by the {0} team · {1}', 'キアラを倒したのは{0}陣営 · {1}'),
     ('키아라를 쓰러뜨린 것은 {0} 조', 'Kiara was defeated by the {0} team', 'キアラを倒したのは{0}陣営'),
     ('{0} 조가 키아라를 쓰러뜨렸다', 'The {0} team defeated Kiara', '{0}陣営がキアラを倒した')]
BXE = "const be=bxEndOf(r);"
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 기록 남기기: 비스트 결말 갈래 · 오염 여부/검은 성배 결말은 남기지 않음
    rp("cup:(S.flags.war==='victor'||S.flags.war==='shared')?(w.cupPure?'pure':'dark'):null,",
       "cup:(S.flags.war==='victor'||S.flags.war==='shared')&&!(w.crisis&&w.crisis.type==='beast3R')?(w.cupPure?'pure':'dark'):null,")
    rp("cx:w.crisis?{type:w.crisis.type,st:w.crisis.stage,sk:w.crisis.shadowKills||0,end:S.flags.cupSealed",
       "cx:w.crisis?{type:w.crisis.type,st:w.crisis.stage,sk:w.crisis.shadowKills||0,bx:w.crisis.type==='beast3R'?(S.flags.bxEnd||(S.flags.bxDream?'dream':'')):undefined,end:w.crisis.type==='beast3R'?null:S.flags.cupSealed")
    # 보여 주기 도우미
    rp("const wkey=r=>r.warKey||WRK[r.war]||'none';",
       "const wkey=r=>r.warKey||WRK[r.war]||'none';\n"
       "// 11-14: 비스트(키아라) 결말 — me/npc/dream · 예전 기록은 r.bx와 결말 키로 짐작\n"
       "const bxEndOf=r=>{ const x=r&&r.wd&&r.wd.cx; if(!x||x.type!=='beast3R') return ''; return x.bx||(r.bx==='dream'?'dream':r.bx==='moon'?(wkey(r)==='victor'?'me':'npc'):''); };\n"
       "const warTxt=r=>bxEndOf(r)==='me'&&wkey(r)==='victor'?'셋쇼인 키아라를 쓰러뜨렸다':r.war;\n"
       "const rlab=(r,k)=>bxEndOf(r)==='me'&&k==='victor'?'키아라 처치':(RLAB[k]||'');")
    # 성배전쟁 기록
    rp("  const win=wd.winner?P[wd.winner]:null;\n  let verdictSub = k==='victor'?`소원 · ${esc(wd.wish||r.wish||'')}${wd.cup?",
       "  const win=wd.winner?P[wd.winner]:null; " + BXE + "\n  let verdictSub = k==='victor'?`${be?'':'소원 · '}${esc(wd.wish||r.wish||'')}${wd.cup&&!be?")
    rp(": win?`성배를 쥔 것은 ${esc(pLab(win))} 조${win.mname?",
       ": win?`${be?'키아라를 쓰러뜨린':'성배를 쥔'} 것은 ${esc(pLab(win))} 조${win.mname?")
    rp("  if(wd.cx){ const t={seal:", "  if(wd.cx&&wd.cx.type==='beast3R'){ const t=(be==='me'&&k==='victor')||(be==='npc'&&win)?'':({me:'키아라를 쓰러뜨렸다',npc:'다른 조가 키아라를 쓰러뜨렸다',dream:'도시가 단꿈에 잠겼다'}[be]||''); verdictSub=(verdictSub?verdictSub+' · ':'')+`후반 위기 · 비스트 Ⅲ/R${t?' · '+t:''}`; }\n  else if(wd.cx){ const t={seal:")
    rp("const pst=p=>{ if(wd.winner===p.i) return '<span class=\"st win\">성배를 쥐었다</span>';",
       "const pst=p=>{ if(wd.winner===p.i) return `<span class=\"st win\">${be?'키아라를 쓰러뜨렸다':'성배를 쥐었다'}</span>`;")
    rp("${my.alive&&RGRP(k)==='grail'?'<span class=\"st win\">성배를 쥐었다</span>':",
       "${my.alive&&RGRP(k)==='grail'?`<span class=\"st win\">${be==='me'?'키아라를 쓰러뜨렸다':'성배를 쥐었다'}</span>`:")
    rp("const endTxt={victor:'성배를 손에 쥐었다',", "const endTxt={victor:warTxt(r),")
    rp("|| (win?`${pLab(win)} 조가 성배를 쥐었다`:'');", "|| (win?`${pLab(win)} 조가 ${be?'키아라를 쓰러뜨렸다':'성배를 쥐었다'}`:'');")
    rp("<div class=\"verdict\">${esc(RLAB[k]==='전사'?'전쟁 중에 숨을 거두었다':r.war)}", "<div class=\"verdict\">${esc(RLAB[k]==='전사'?'전쟁 중에 숨을 거두었다':warTxt(r))}")
    # 한 사람의 기록 · 복사 글 · 지난 생 목록 배지
    rp(" 함께. `:''}${r.war}${r.wish?", " 함께. `:''}${warTxt(r)}${r.wish?")
    rp("+' 함께, ':''}${r.war}${r.wish?", "+' 함께, ':''}${warTxt(r)}${r.wish?")
    rp("<span class=\"badge\">${RLAB[k]||''}</span>", "<span class=\"badge\">${rlab(r,k)}</span>")
    # 성배를 손에 쥐어야 하는 업적은 키아라 결말에서 빼기 (성배는 BB가 달로 가져갔다)
    for aid in ('grail','fast','noseal','backstab','misfit'):
        import re as _re
        m = _re.search(r"\{id:'" + aid + r"',cat:'[^']*',n:'[^']*',d:'[^']*',t:\(\)=>GRAIL\(\)", s)
        if not m: miss.append(('ach ' + aid, 0)); continue
        s = s[:m.end()] + "&&!S.flags.bxEnd" + s[m.end():]
    s, nd, nt = i18n.add(s, D, T)
    print('bxrec miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
