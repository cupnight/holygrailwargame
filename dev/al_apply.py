"""⓪ 서번트 속성(Fate 공식 속성)·취향 — 「서번트 속성(공식 성향) 상세안」 6판을 게임 파일에 넣는다.
사용: python3 al_apply.py <게임 html> [...]"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from al_data import AL, AL_NEW, LK
import i18n

J = lambda x: json.dumps(x, ensure_ascii=False)

def hero_ids(s):
    i = s.index('  const HEROES = ['); j = s.index('\n  ];', i); b = s[i:j]
    ids = re.findall(r"""[{,]\s*"?id"?\s*:\s*['"]([a-z0-9_]+)['"]""", b)
    names = re.findall(r"""[{,]\s*"?name"?\s*:\s*['"]([^'"]+)['"]""", b)
    return list(zip(ids, names))

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:60], k)); return
        s = s.replace(o, n)

    H = hero_ids(s); by = {n: i for i, n in H}
    hal = {}
    for code, names in AL.items():
        for n in [x.strip() for x in names.split(',')]:
            hal[by[n]] = code
    order = [i for i, _ in H]
    hal_s = ','.join(f"{i}:'{hal[i]}'" for i in order if i in hal)
    hal_s += ',' + ','.join(f"{i}:'{c}'" for i, c in AL_NEW.items() if i not in hal)
    hlk_s = ','.join(f"{by[n]}:{{{','.join(f'{k}:{v}' for k, v in d.items())}}}" for n, d in LK)

    # 1) 데이터와 계산 함수
    CORE = f"""  // ---- 서번트 속성(Fate 공식 속성, FGO 기준) · 취향 — 성격(성향)과 반반으로 반응을 정한다 ----
  const HAL={{{hal_s}}};
  const HLK={{{hlk_s}}};
  const AL_L={{L:'질서',N:'중립',C:'혼돈'}}, AL_M={{G:'선',B:'중용',E:'악',M:'광'}};
  const alAx=id=>{{ const c=HAL[id]; return c?[AL_L[c[0]],AL_M[c[1]]]:null; }};
  const alName=id=>{{ const a=alAx(id); return a?a.join('·'):''; }};
  // 속성 몫: 선택의 속성 표에서 서번트의 두 축 값을 더한다. 어느 축도 표에 없으면 null(반응 없음 → 성격대로)
  function alR(t,k){{ const h=hero(); const ax=t&&h&&alAx(h.id); if(!ax) return null; k=k||1; let hit=false, sum=0;
    for(const a of ax){{ if(!(a in t)) continue; hit=true; const v=t[a]*k; sum+=v;
      if(Math.abs(v)>=3&&CHK) CHK.push(v>0?{{txt:`「${{a}}」 속성의 서번트가 그 선택을 높이 샀다`,ok:true}}:{{txt:`「${{a}}」 속성의 서번트가 그 선택을 못마땅해했다`,ok:false}}); }}
    return hit?sum:null; }}
  const mixR=(p,a)=>a==null?p:(p+a)/2;
  // 취향: 엄청 좋아함 +6 · 좋아함 +3 · 싫어함 −3 · 엄청 싫어함 −6. '-태그'는 그 취향을 거스르는 선택
  function lkR(tg){{ const h=hero(); const L=h&&HLK[h.id]; if(!tg||!L) return 0; let s=0;
    for(const x of [].concat(tg)){{ const neg=x[0]==='-', k=neg?x.slice(1):x; const v=(L[k]||0)*(neg?-1:1); if(!v) continue; s+=v*3;
      if(CHK) CHK.push(v>=2?{{txt:'서번트의 눈이 빛났다. 바로 이런 걸 바랐다는 얼굴이다',ok:true}}:v>0?{{txt:'서번트는 그 선택이 꽤 마음에 든 눈치였다',ok:true}}:v<=-2?{{txt:'서번트는 그 선택만은 참을 수 없다는 얼굴이었다',ok:false}}:{{txt:'서번트는 그 선택이 영 마음에 들지 않는 눈치였다',ok:false}}); }}
    return s; }}
  const trA=n=>{{ const w=W(); if(w&&w.heroAlive&&n) w.trust=clamp(w.trust+n); }};
  // 마력 수집 · 시민 제물: 성격 몫(지금 규칙)과 속성 몫을 반반, 희생 취향을 더한다
  function gatherTr(big){{ const h=hero(); const p=h.traits.includes('명예')||h.traits.includes('연민')?(big?-6:-3):h.traits.includes('야망')?3:-1;
    const A=alR(big?{{선:-6,중용:-3,악:3,광:0,질서:-2,중립:0,혼돈:1}}:{{선:-3,중용:-1,악:1,광:0,질서:-1,중립:0,혼돈:0}});
    const tr=Math.round(mixR(p,A))+lkR('희생'), L=HLK[h.id]||{{}};
    const line=tr<0?`${{h.name}}${{J(h.name,은)}} 일을 마치고 당신과 눈을 마주치지 않았다.`:tr>0?(L.희생>=2?`${{h.name}}${{J(h.name,은)}} 황홀한 얼굴이었다.`:`${{h.name}}${{J(h.name,은)}} 만족스러운 얼굴이었다.`):'';
    return {{tr,line}}; }}
  const alGood=()=>{{ const a=hero()&&alAx(hero().id); return !!a&&a[1]==='선'; }}, alEvil=()=>{{ const a=hero()&&alAx(hero().id); return !!a&&a[1]==='악'; }};
"""
    rp("  function fitScore(h,match){", CORE + "  function fitScore(h,match){")

    # 다 빈치 성향: 야망·자유 → 자유·연민 (11-10 속성 작업에서 함께 고침 · 시트 '서번트 설정'과 같게)
    rp("id:'davinci',fem:1,cls:'caster',name:'레오나르도 다 빈치',title:'만능의 천재',from:'르네상스 미술사',s:['E','C','E','A+','B'],art:{n:'워모 우니베르살레',d:'만능인'},traits:['야망','자유'],",
       "id:'davinci',fem:1,cls:'caster',name:'레오나르도 다 빈치',title:'만능의 천재',from:'르네상스 미술사',s:['E','C','E','A+','B'],art:{n:'워모 우니베르살레',d:'만능인'},traits:['자유','연민'],")

    # 2) 공통 판정 함수
    rp("""  function fitT(n,wish){ const w=W(); if(!w||!n) return n; const t=fitTier(w);""",
       """  function fitT(n,wish,good){ const w=W(); if(!w||!n) return n; const t=fitTier(w); // good: 선 서번트가 반긴 일이라 마음을 닫지 않는다""")
    rp("""      if(t==='어긋남'){ if(ch(.25)){ if(CHK) CHK.push({txt:'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; }""",
       """      if(t==='어긋남'){ if(!good&&ch(.25)){ if(CHK) CHK.push({txt:'궁합이 어긋나 서번트가 마음을 닫았다',ok:false}); return -2; }""")
    rp("""  function traitR(r){ const h=hero(); const ts=h.traits.filter(t=>t in TRJ); const raw=ts.reduce((a,t)=>a+(r[t]||0),0)*(ts.length===1?1.5:1);""",
       """  function traitR(r,a,tg){ const h=hero(); const ts=h.traits.filter(t=>t in TRJ); const raw=ts.reduce((a,t)=>a+(r[t]||0),0)*(ts.length===1?1.5:1);""")
    rp("""    for(const t of ts){ const v=r[t]||0; if(Math.abs(v)<2) continue; if(CHK) CHK.push(v>0?{txt:`서번트가 「${t}」${TRJ[t]} 높이 샀다`,ok:true}:{txt:`「${t}」${TRJ[t]} 중시하는 서번트가 고개를 돌렸다`,ok:false}); }
    return Math.round(raw); }""",
       """    for(const t of ts){ const v=r[t]||0; if(Math.abs(v)<2) continue; if(CHK) CHK.push(v>0?{txt:`서번트가 「${t}」${TRJ[t]} 높이 샀다`,ok:true}:{txt:`「${t}」${TRJ[t]} 중시하는 서번트가 고개를 돌렸다`,ok:false}); }
    return Math.round(mixR(Math.round(raw),a?alR(a):null))+lkR(tg); }""")
    rp("""  function crossReact(r){ const w=W(), h=hero(); if(!w.heroAlive) return;
    const ts=h.traits.filter(t=>t in TRJ); let raw=ts.reduce((a,t)=>a+(r[t]||0),0)*(ts.length===1?1.5:1)*1.5;
    if(raw<0&&w.trust>=70) raw*=.7; if(raw>0&&w.trust<DIST) raw*=.5;""",
       """  function crossReact(r,a,tg){ const w=W(), h=hero(); if(!w.heroAlive) return;
    const ts=h.traits.filter(t=>t in TRJ); let raw=ts.reduce((a,t)=>a+(r[t]||0),0)*(ts.length===1?1.5:1)*1.5;
    raw=mixR(raw,a?alR(a,1.5):null);
    if(raw<0&&w.trust>=70) raw*=.7; if(raw>0&&w.trust<DIST) raw*=.5; raw+=lkR(tg);""")
    rp("""crossReact(c.r); return r; }}));""", """crossReact(c.r,c.al,c.tg); return r; }}));""")
    rp("""  function cxTraitEnd(r){ const w=W(); if(!w.heroAlive) return; const r2={}; for(const k in r) r2[k]=r[k]*2; w.trust=clamp(w.trust+traitR(r2)); }""",
       """  function cxTraitEnd(r,a){ const w=W(); if(!w.heroAlive) return; const r2={}, a2=a?{}:null; for(const k in r) r2[k]=r[k]*2; if(a) for(const k in a) a2[k]=a[k]*2; w.trust=clamp(w.trust+traitR(r2,a2)); }""")

    # 3) 갈림길 14가지 (5-4장)
    CR = [
     ("{t:'상처를 치료해 돌려보낸다',r:{명예:4,연민:6,야망:-4,자유:2},", "al:{선:6,악:-4},tg:['구조','-무자비'],"),
     ("{t:'지금 끝낸다',r:{명예:-6,연민:-6,충성:2,야망:6},", "al:{선:-6,악:4,질서:-2},tg:'무자비',"),
     ("{t:'서번트에게 구하라고 한다',r:{연민:6,명예:4,충성:2,야망:-3},", "al:{선:6,악:-2},tg:'구조',"),
     ("{t:'직접 구하고, 서번트는 경계를 선다',r:{연민:4,충성:4},", "al:{선:4},tg:'구조',"),
     ("{t:'정체를 숨기고 떠난다',r:{연민:-6,명예:-3,야망:3,자유:1},", "al:{선:-6,악:4,질서:2},tg:'-구조',"),
     ("{t:'정면으로 응한다',r:{명예:6,자유:2,야망:-1},", "al:{질서:4},tg:'정면승부',"),
     ("{t:'응하는 척 함정을 판다',r:{명예:-7,야망:5,자유:-1},", "al:{질서:-6,혼돈:2,악:2},tg:['계략','-정면승부'],"),
     ("{t:'무시한다',r:{명예:-3,자유:1},", "tg:'-정면승부',"),
     ("{t:'받아들인다',r:{야망:5,명예:-3,충성:-1},", "al:{질서:-2,혼돈:2},tg:'계략',"),
     ("{t:'거절한다',r:{명예:4,충성:2,야망:-2},", "al:{질서:2},"),
     ("{t:'표적이 된 조에게 귀띔한다',r:{명예:3,연민:4,야망:-4},", "al:{선:4,질서:-2,혼돈:2},"),
     ("{t:'뜻대로 하게 둔다',r:{자유:6,연민:3,충성:2,명예:1,야망:1},", "al:{혼돈:4},"),
     ("{t:'명령으로 막는다',d:'서번트의 뜻을 꺾는다 · 대신 몸을 숨기고 거처를 다진다',r:{자유:-7,연민:-3,명예:-2,충성:-1,야망:-1},", "al:{혼돈:-6,질서:2},"),
     ("{t:'함께 머문다',r:{연민:4,충성:4,자유:2,명예:1,야망:1},", "al:{선:2},"),
     ("{t:'감독관에게 반납한다',r:{명예:5,야망:-4,자유:-2},", "al:{질서:6,혼돈:-4},tg:'규율',"),
     ("{t:'솔직하게 말한다',r:{명예:4,충성:3,연민:2},", "al:{선:2},"),
     ("{t:'듣기 좋은 거짓말을 한다',r:{명예:-5,야망:2,자유:-2,충성:-2},", "al:{선:-2,질서:-2},tg:'계략',"),
     ("{t:'맡긴다',r:{자유:6,충성:2},", "al:{혼돈:4,질서:-2},"),
     ("{t:'집까지 데려다준다',r:{연민:6,명예:3,야망:-3},", "al:{선:6,악:-2},tg:'구조',"),
     ("{t:'사역마를 붙잡아 정보를 캔다',r:{연민:-6,명예:-4,야망:5},", "al:{선:-6,악:4},"),
     ("{t:'교회에 맡긴다',r:{연민:2,충성:2},", "al:{질서:4},"),
     ("{t:'병원을 찾아가 몰래 보상한다',r:{연민:6,명예:3},", "al:{선:6,질서:-2},tg:'구조',"),
     ("{t:'흔적을 지운다',r:{명예:-4,야망:3,연민:-3},", "al:{질서:4,선:-4},"),
     ("{t:'신경 쓰지 않는다',r:{연민:-6,명예:-3,자유:2},", "al:{선:-6,악:2},tg:'-구조',"),
     ("{t:'서번트를 믿고 맡긴다',r:{충성:4,자유:4,명예:2},", "al:{혼돈:4},"),
     ("{t:'더 나은 조건을 약속한다',r:{야망:5,명예:-3,충성:-2},", "al:{질서:-2,악:2},"),
     ("{t:'몰래 빼내 서번트에게 돌려준다',r:{충성:3,자유:3,명예:-2,연민:1},", "al:{질서:-6,혼돈:4},tg:'-규율',"),
     ("{t:'정당하게 사들인다',r:{명예:4,충성:2},", "al:{질서:6,혼돈:-2},tg:'규율',"),
     ("{t:'팔아서 전쟁 자금으로 쓴다',r:{야망:3,명예:-3,충성:-4},", "al:{선:-2,악:2},"),
     ("{t:'거절하고 끝까지 싸운다',r:{명예:3,충성:3,자유:3},", "al:{혼돈:2},"),
     ("{t:'받아들이는 척 보상만 챙긴다',r:{야망:4,명예:-5},", "al:{질서:-6,악:2},tg:'계략',"),
     ("{t:'다른 조의 정보를 넘기고 편의를 얻는다',r:{야망:3,명예:-4,연민:-1},", "al:{선:-4,악:2},tg:'계략',"),
     ("{t:'내 마력을 나눠 상처를 메운다',r:{연민:3,충성:4},", "al:{선:2},"),
    ]
    i0 = s.index('  const CROSS=['); i1 = s.index('  function crossTry()', i0)
    blk = s[i0:i1]
    for o, add in CR:
        k = blk.count(o)
        if k != 1: miss.append(('CROSS ' + o[:40], k)); continue
        blk = blk.replace(o, o + add)
    s = s[:i0] + blk + s[i1:]

    # 4) 단발 장면 (5-3장)
    # 첫 만남
    rp("""tr(4+traitR({연민:2,명예:2,충성:1,야망:-1}));return sayV(h,'thanks');""", """tr(4+traitR({연민:2,명예:2,충성:1,야망:-1},{선:2}));return sayV(h,'thanks');""")
    rp("""tr(-3+traitR({명예:-2,야망:-2,연민:1}));add({will:-1});return sayV(h,'flee');""", """tr(-3+traitR({명예:-2,야망:-2,연민:1},{선:1,악:-1}));add({will:-1});return sayV(h,'flee');""")
    rp("""tr(3+traitR({명예:3,충성:3,연민:1,자유:-2}));return sayV(h,'bow');""", """tr(3+traitR({명예:3,충성:3,연민:1,자유:-2},{질서:3,혼돈:-2}));return sayV(h,'bow');""")
    rp("""traitR({연민:2,야망:3,자유:1,충성:-1}));return sayV(h,'wish');""", """traitR({연민:2,야망:3,자유:1,충성:-1},{악:2,혼돈:1}));return sayV(h,'wish');""")
    rp("""tr(1+traitR({충성:2,야망:2,명예:1,자유:-1}));""", """tr(1+traitR({충성:2,야망:2,명예:1,자유:-1},{질서:2,혼돈:-1}));""")
    # 마력 수집
    rp("""    const tr=h.traits.includes('명예')||h.traits.includes('연민')?(big?-6:-3):h.traits.includes('야망')?3:-1; w.trust=clamp(w.trust+tr);""",
       """    const G=gatherTr(big), tr=G.tr; w.trust=clamp(w.trust+tr);""")
    rp("""    if(tr<0) s+=` ${h.name}${J(h.name,은)} 일을 마치고 당신과 눈을 마주치지 않았다.`; else if(tr>0) s+=` ${h.name}${J(h.name,은)} 만족스러운 얼굴이었다.`;""",
       """    if(G.line) s+=' '+G.line;""")
    # 시민 제물
    rp("""w.sacr=(w.sacr||0)+1; add({will:-6}); lean('cruel',1);
      log(pick(['다음 날 아침, 원인 모를 집단 실신 사고가 보도되었다. 몇 명은 깨어나지 못했다.','골목 하나가 통째로 조용해졌다. 서번트의 상처가 아물었다.']),'loss');""",
       """w.sacr=(w.sacr||0)+1; add({will:-6}); lean('cruel',1);
      log(pick(['다음 날 아침, 원인 모를 집단 실신 사고가 보도되었다. 몇 명은 깨어나지 못했다.','골목 하나가 통째로 조용해졌다. 서번트의 상처가 아물었다.']),'loss');
      if(w.heroAlive){ const G=gatherTr(true); w.trust=clamp(w.trust+G.tr); if(G.line) log(G.line,'voice'); }""")
    # 멈춰 선 버스
    rp("""{t:'승객부터 구한다',auto:true,f:()=>{w.hp=clamp(w.hp-10);w.trust=clamp(w.trust+fitT(6));w.exposure=clamp(w.exposure+expUp(8));lean('judge',1);return byBody(hero(),{normal:'서번트가 버스를 통째로 들어 골목으로 옮겼다. 그사이 적의 일격을 등으로 받았다.',beast:'늑대가 버스 옆구리를 들이받아 골목으로 밀어냈다. 그사이 적의 일격을 등으로 받았다.'})}},
      {t:'싸움에 집중한다',f:()=>{add({will:-3});w.civ=(w.civ||0)+1;return '버스 쪽에서 비명이 들렸다. 돌아보지 않았다.'}}]});}},""",
       """{t:'승객부터 구한다',auto:true,f:()=>{w.hp=clamp(w.hp-10);w.trust=clamp(w.trust+fitT(6+traitR({연민:3,명예:2,야망:-2},{선:3,악:-3,질서:1},'구조'),false,alGood()));w.exposure=clamp(w.exposure+expUp(8));lean('judge',1);const n=hero().name;return byBody(hero(),{normal:'서번트가 버스를 통째로 들어 골목으로 옮겼다. 그사이 적의 일격을 등으로 받았다.',beast:'늑대가 버스 옆구리를 들이받아 골목으로 밀어냈다. 그사이 적의 일격을 등으로 받았다.'})+(alEvil()?` ${n}${J(n,은)} 굳이 그럴 필요가 있었냐는 얼굴이었다.`:'')}},
      {t:'싸움에 집중한다',f:()=>{add({will:-3});w.civ=(w.civ||0)+1;w.trust=clamp(w.trust+fitT(traitR({연민:-3,명예:-2,야망:1},{선:-3,악:1,질서:-1},'-구조')));return '버스 쪽에서 비명이 들렸다. 돌아보지 않았다.'}}]});}},""")
    # 밤길의 아이
    rp("""{t:'집까지 데려다준다',auto:true,f:()=>{ W().trust=clamp(W().trust+(hero().traits.includes('연민')?7:3));""",
       """{t:'집까지 데려다준다',auto:true,f:()=>{ W().trust=clamp(W().trust+Math.round(mixR(hero().traits.includes('연민')?7:3,alR({선:7,중용:5,악:3})))+lkR('구조'));""")
    # 말로 싸움을 멈춤
    rp("""      w.trust=clamp(w.trust+(h.traits.includes('연민')?4:0));""", """      w.trust=clamp(w.trust+Math.round(mixR(h.traits.includes('연민')?4:0,alR({선:4,중용:2,악:0}))));""")
    # 결투 응낙
    rp("""W().duel=p;W().trust=clamp(W().trust+(hero().traits.includes('명예')?8:2));""",
       """W().duel=p;W().trust=clamp(W().trust+Math.round(mixR(hero().traits.includes('명예')?8:2,alR({질서:8})))+lkR('정면승부'));""")
    # 마스터 저격
    rp("""    const tr=h.traits.includes('명예')?-6:h.traits.includes('야망')?0:-2; w.trust=clamp(w.trust+tr);""",
       """    const tr=Math.round(mixR(h.traits.includes('명예')?-6:h.traits.includes('야망')?0:-2,alR({선:-4,중용:-2})))+lkR('무자비'); w.trust=clamp(w.trust+tr);""")
    # 인질
    rp("""if(!tried){ w.trust=clamp(w.trust+traitR({연민:-4,명예:-2,충성:-1,야망:1})); lean('avenger',1); }""",
       """if(!tried){ w.trust=clamp(w.trust+traitR({연민:-4,명예:-2,충성:-1,야망:1},{선:-4,악:1},'-구조')); lean('avenger',1); }""")
    # 목격자
    rp("""auto:true,f:()=>{ if(artLv('mind')>=1){ W().exposure=clamp(W().exposure-5);""",
       """auto:true,f:()=>{ trA(traitR({충성:1,연민:1},{질서:4},'규율')); if(artLv('mind')>=1){ W().exposure=clamp(W().exposure-5);""")
    rp("""{t:'강제의 마안으로 돌려보낸다',d:'건강 −4 · 노출 −8',f:()=>{ add({health:-4});""",
       """{t:'강제의 마안으로 돌려보낸다',d:'건강 −4 · 노출 −8',f:()=>{ trA(traitR({},{질서:2})); add({health:-4});""")
    rp("""      {t:'그냥 둔다',f:()=>{W().exposure=clamp(W().exposure+expUp(15));""",
       """      {t:'그냥 둔다',f:()=>{trA(traitR({자유:2,충성:-1},{질서:-4,혼돈:2}));W().exposure=clamp(W().exposure+expUp(15));""")
    rp("""      {t:'성당교회에 넘긴다',f:()=>{add({bond:-2});""",
       """      {t:'성당교회에 넘긴다',f:()=>{trA(traitR({연민:-3,충성:1},{질서:2,선:-4,악:2}));add({bond:-2});""")
    # 감독관의 소집
    rp("""{t:'소집에 응한다',d:'오늘 밤 토벌에 합류할 수 있다',auto:true,f:()=>{ hn.joinOk=true;""",
       """{t:'소집에 응한다',d:'오늘 밤 토벌에 합류할 수 있다',auto:true,f:()=>{ trA(traitR({충성:2,명예:1,자유:-2},{질서:4,혼돈:-2},'규율')); hn.joinOk=true;""")
    rp("""{t:'응하지 않는다',d:'감독관의 평가가 내려간다',f:()=>{ w.supCold=true;""",
       """{t:'응하지 않는다',d:'감독관의 평가가 내려간다',f:()=>{ trA(traitR({자유:2,충성:-1},{질서:-2,혼돈:2},'-규율')); w.supCold=true;""")
    # 검은 성배
    rp("""w.cxPact={d:night,i:p.i}; w.trust=clamp(w.trust+traitR({명예:2,연민:1,충성:1}));""",
       """w.cxPact={d:night,i:p.i}; w.trust=clamp(w.trust+traitR({명예:2,연민:1,충성:1},{질서:2}));""")
    rp("""if(w.heroAlive) cxTraitEnd({명예:-3,충성:-1,연민:-1}); }""", """if(w.heroAlive) cxTraitEnd({명예:-3,충성:-1,연민:-1},{질서:-4}); }""")
    rp("""w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:3,야망:-1,자유:1}));""", """w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:3,야망:-1,자유:1},{선:2}));""", 2)
    rp("""w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:2,자유:1}));""", """w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:2,자유:1},{선:2}));""")
    rp("""    if(CX_TR[k]) cxTraitEnd(CX_TR[k]);""", """    if(CX_TR[k]) cxTraitEnd(CX_TR[k],{break:{선:3},sealbreak:{선:3}}[k]);""")
    rp("""    if(ch(p)){ cxTraitEnd({충성:1,연민:3,명예:2,야망:-2});""", """    if(ch(p)){ cxTraitEnd({충성:1,연민:3,명예:2,야망:-2},{선:3});""")
    rp("""cxTraitEnd({연민:3,명예:3,야망:-4,자유:2});
    log(`${h.name}${J(h.name,이)} 성배에 손을 얹었다.""", """cxTraitEnd({연민:3,명예:3,야망:-4,자유:2},{선:3});
    log(`${h.name}${J(h.name,이)} 성배에 손을 얹었다.""")
    # 동맹이 습격당함
    rp("""crossReact({충성:6,명예:4,연민:3,야망:-3});""", """crossReact({충성:6,명예:4,연민:3,야망:-3},{질서:4,선:2});""")
    rp("""crossReact({충성:-7,명예:-4,야망:3});""", """crossReact({충성:-7,명예:-4,야망:3},{질서:-4});""")
    rp("""crossReact({야망:5,충성:-8,자유:2});""", """crossReact({야망:5,충성:-8,자유:2},{질서:-6,혼돈:2,악:2});""")

    # 5) 영혼 포식 사건과 soul 대사를 지운다 (5-2장)
    m = re.search(r"\n    \{w:2,c:\(\)=>W\(\)\.sm<35&&!!VO\(hero\(\),'soul'\).*?return '다음 날 뉴스에서 원인 모를 집단 실신 사고가 보도되었다\. 몇 명은 깨어나지 못했다\.'\}\}\]\}\);\}\},", s, re.S)
    if m and m.group(0).count('\n    {w:') == 1: s = s[:m.start()] + s[m.end():]
    else: miss.append(('soul event', 0))
    n0 = len(re.findall(r",\n      soul:'[^'\n]*'\}", s))
    s = re.sub(r",\n      soul:'[^'\n]*'\}", "}", s)
    if n0 != 9: miss.append(('soul lines', n0))

    # 6) 도감 · 내보내기
    rp("""<dt>성향</dt><dd>${x.traits.map(t=>'「'+esc(t)+'」').join(' ')}</dd><dt>소원</dt>""",
       """<dt>성향</dt><dd>${x.traits.map(t=>'「'+esc(t)+'」').join(' ')}</dd>${Sim.alName(x.id)?`<dt>속성</dt><dd>${esc(Sim.alName(x.id))}</dd>`:''}<dt>소원</dt>""")
    rp("""    pickup:()=>({live:pickupLive(),""", """    alName:id=>alName(id), pickup:()=>({live:pickupLive(),""")

    # 7) 번역
    AX = [('질서','Lawful','秩序'),('중립','Neutral','中立'),('혼돈','Chaotic','混沌'),('선','Good','善'),('중용','Balanced','中庸'),('악','Evil','悪'),('광','Mad','狂')]
    ax = {k: (e, j) for k, e, j in AX}
    D = [('속성','Alignment','属性')] + AX
    for a in ['질서','중립','혼돈']:
        for b in ['선','중용','악']:
            D.append((f'{a}·{b}', f'{ax[a][0]} {ax[b][0]}', f'{ax[a][1]}・{ax[b][1]}'))
    D += [('질서·광','Lawful Mad','秩序・狂'),('혼돈·광','Chaotic Mad','混沌・狂')]
    D += [('서번트의 눈이 빛났다. 바로 이런 걸 바랐다는 얼굴이다','Your Servant\'s eyes lit up. This was exactly what they wanted','サーヴァントの目が輝いた。まさにこれを望んでいたという顔だ'),
          ('서번트는 그 선택이 꽤 마음에 든 눈치였다','Your Servant seemed rather pleased with that choice','サーヴァントはその選択がなかなか気に入ったようだった'),
          ('서번트는 그 선택만은 참을 수 없다는 얼굴이었다','Your Servant looked as if that was the one thing they could not stand','サーヴァントはそれだけは我慢ならないという顔をした'),
          ('서번트는 그 선택이 영 마음에 들지 않는 눈치였다','Your Servant did not seem to like that choice at all','サーヴァントはその選択がどうにも気に入らないようだった')]
    T = [('「{0}」 속성의 서번트가 그 선택을 높이 샀다','The {0} Servant approved of that choice','「{0}」のサーヴァントはその選択を高く買った'),
         ('「{0}」 속성의 서번트가 그 선택을 못마땅해했다','The {0} Servant disliked that choice','「{0}」のサーヴァントはその選択を快く思わなかった'),
         ('{0~은} 황홀한 얼굴이었다.','{0} looked enraptured.','{0}は恍惚とした顔をしていた。'),
         ('{0~은} 굳이 그럴 필요가 있었냐는 얼굴이었다.','{0} looked as if to ask whether that had really been necessary.','{0}は、わざわざそこまでする必要があったのかという顔をしていた。')]
    s, nd, nt = i18n.add(s, D, T)
    open(P, 'w', encoding='utf-8').write(s)
    print(os.path.basename(P), 'HAL', len(hal) + len(AL_NEW), 'tr', nd, nt, 'miss', miss)
