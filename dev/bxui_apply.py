"""11-14: 비스트(키아라) 결말 기록 화면 꾸밈과 조 목록
- 한 사람의 기록 카드: 달로 간 잔(달빛 은청 · BB 분홍 · 초승달) · 다른 조가 끝낸 경우 빛을 줄임 · 단꿈(복숭앗빛 분홍 · 연꽃 만다라) · 결말 이름표
- 성배전쟁 기록 결말 칸 · 지난 생 목록 배지 색을 같은 계열로
- 지난 생 목록: 내가 키아라를 쓰러뜨린 생은 '성배 획득'이 아니라 '그 밖의 결말'에 셈 (요약 줄의 '성배' 숫자도)
- 마지막 한마디: 이름이 붙은 말은 내 서번트의 말만 남긴다
- 조 목록: 수녀 조는 '탈락 통지(거짓)'에서 멈추지 않고 강림과 끝을 이어 적음 · 센티넬이 된 서번트 · 성배로 빨려 든 서번트 표시
시안: 스크래치 bxrec/mock.css → dev/bxui_css.txt
사용: python3 bxui_apply.py <game.html>"""
import sys, os, i18n
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bxui_css.txt'), encoding='utf-8').read()
D = [('달로 간 잔', 'The Cup Gone to the Moon', '月へ行った杯'),
     ('단꿈', 'Sweet Dream', '甘い夢'),
     ('거짓 탈락 통지', 'False elimination notice', '偽りの脱落通知'),
     ('비스트 Ⅲ/R로 강림', 'Descended as Beast III/R', 'ビーストIII/Rとして降臨'),
     ('당신에게 쓰러졌다', 'Fell to you', 'あなたに倒された'),
     ('도시를 단꿈에 잠기게 했다', 'Sank the city into a sweet dream', '街を甘い夢に沈めた'),
     ('센티넬이 되었다', 'Became a Sentinel', 'センチネルになった'),
     ('영기가 성배 쪽으로 빨려 들어갔다', 'Its Spirit Origin was drawn toward the Grail', '霊基が聖杯の方へ吸い込まれた')]
T = [('제{0}일 비스트 Ⅲ/R로 강림', 'Descended as Beast III/R on day {0}', '{0}日目にビーストIII/Rとして降臨'),
     ('{0} 조에게 쓰러졌다', 'Fell to the {0} team', '{0}陣営に倒された')]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 기록에 남길 것: 수녀 조 · 센티넬이 된 서번트 · 빨려 든 서번트 · 강림한 날
    rp("const lab=p=>({i:p.i,", "const lab=p=>({bxn:p.bxNun?1:undefined,sent:p.bxSentUsed?1:undefined,abs:p.bxAbs?1:undefined,i:p.i,")
    rp("c.absorbed=(c.absorbed||0)+1;", "c.absorbed=(c.absorbed||0)+1; if(o&&o.src) o.src.bxAbs=1;")
    rp("bx:w.crisis.type==='beast3R'?(", "dd:w.crisis.type==='beast3R'?(w.crisis.descD||undefined):undefined,bx:w.crisis.type==='beast3R'?(")
    # 꾸밈
    rp(".record.grail.dark{", CSS + ".record.grail.dark{")
    rp("const rlab=(r,k)=>", "const rgrp=r=>{ const k=wkey(r); return bxEndOf(r)==='me'&&k==='victor'?'out':RGRP(k); }; // 11-14: 키아라를 쓰러뜨린 생은 '그 밖의 결말'\n"
       "const rkc=r=>{ const be=bxEndOf(r); return be?(be==='dream'?'bxd':'bxm'):RGRP(wkey(r)); };\nconst rlab=(r,k)=>")
    # 지난 생 목록
    rp("grail=hist.filter(r=>RGRP(wkey(r))==='grail').length", "grail=hist.filter(r=>rgrp(r)==='grail').length")
    rp("const cnt=k=>k==='all'?hist.length:hist.filter(r=>RGRP(wkey(r))===k).length;", "const cnt=k=>k==='all'?hist.length:hist.filter(r=>rgrp(r)===k).length;")
    rp("const list=hist.filter(r=>pastF==='all'||RGRP(wkey(r))===pastF);", "const list=hist.filter(r=>pastF==='all'||rgrp(r)===pastF);")
    rp("b.className='past-item hf rk-'+RGRP(k);", "b.className='past-item hf rk-'+rkc(r);")
    # 한 사람의 기록 카드
    rp("<div class=\"record${cup?' grail'+(cup==='dark'?' dark':''):''}\">",
       "<div class=\"record${bxEndOf(r)?(bxEndOf(r)==='dream'?' rdream':' rmoon'+(bxEndOf(r)==='npc'?' far':'')):cup?' grail'+(cup==='dark'?' dark':''):''}\">")
    rp("<div class=\"eyebrow\">${fromHistory?'지난 생':'한 사람의 기록'}</div>",
       "<div class=\"eyebrow\">${fromHistory?'지난 생':'한 사람의 기록'}${bxEndOf(r)?`<span class=\"endtag\">${bxEndOf(r)==='dream'?'단꿈':'달로 간 잔'}</span>`:''}</div>")
    # 성배전쟁 기록
    rp("return `<div class=\"report rk-${RGRP(k)}\">", "return `<div class=\"report rk-${rkc(r)}\">")
    rp("if(p.out){ const by=p.out.by?P[p.out.by]:null; return `<span class=\"st\">제${p.out.d}일 ${p.out.tod} · ${esc(p.out.why)}${by?` (${esc(pLab(by))} 조)`:''}</span>`; }",
       "if(p.out&&be&&(p.bxn||p.out.why==='탈락 통지(거짓)')){ const fin=be==='me'?'당신에게 쓰러졌다':be==='npc'?(win?`${esc(pLab(win))} 조에게 쓰러졌다`:'다른 조에게 쓰러졌다'):'도시를 단꿈에 잠기게 했다';"
       " return `<span class=\"st\">제${p.out.d}일 ${p.out.tod} · 거짓 탈락 통지 · ${wd.cx&&wd.cx.dd?`제${wd.cx.dd}일 비스트 Ⅲ/R로 강림`:'비스트 Ⅲ/R로 강림'} · ${fin}</span>`; }\n"
       "    if(p.out){ const by=p.out.by?P[p.out.by]:null; return `<span class=\"st\">제${p.out.d}일 ${p.out.tod} · ${esc(p.out.why)}${by?` (${esc(pLab(by))} 조)`:''}${p.sent?' · 센티넬이 되었다':p.abs?' · 영기가 성배 쪽으로 빨려 들어갔다':''}</span>`; }")
    # 마지막 한마디: 다른 서번트(BB · 멜트 · 립 등)의 말이 내 서번트의 마지막 말로 남던 것
    rp("if(inW&&k==='voice'&&(t.includes('“')||t.startsWith('(')))S.war.lastVoice=t;",
       "if(inW&&k==='voice'&&(t.includes('“')||t.startsWith('('))&&lvMine(t))S.war.lastVoice=t;")
    rp("  function log(t,k='n',x){", "  const lvMine=t=>{ const h=S.hero&&H_BY[S.hero], m=t.match(/^([^:“”\\n]{1,40}): [“(]/); if(m) return !!h&&m[1]===h.name; if(/— BB”$/.test(t)) return false; const m2=t.match(/^(.{1,30}?)(?:이|가|은|는) /); if(m2&&h&&m2[1]!==h.name){ if(!lvMine.N) lvMine.N=new Set(Object.values(H_BY).map(x=>x.name)); if(lvMine.N.has(m2[1])) return false; } return true; }; // 11-14\n  function log(t,k='n',x){")
    s, nd, nt = i18n.add(s, D, T)
    print('bxui miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
