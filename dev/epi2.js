  /* ---------- 에필로그 시간 흐름 (11-12): 수육한 서번트와 함께 사는 생 ----------
     A 봄의 열나흘(하루씩) → B 첫 해(한 달씩, 2~12달째) → C 열 해(한 해씩, 2~10년째) → D 그 뒤(예전 방식)
     S.epi.ph='A'|'B'|'C'|'D' · d=날 · m=달 · cy=C에서 지난 해 · k=걸음(일 · 달 · 해 모두 1) */
  const EP2_N={A:14,B:12,C:9};
  // 사건이 나오는 구간 (예전 사건을 옮긴 것). 적히지 않은 사건은 C부터 예전 방식으로 나온다
  const EP2_PH={lv_morning:'A',fr_drink:'A',st_ask:'AB',stay_morning:'A',stay_watch:'AB',stay_ask:'AB',stay_family:'B',
    lv_anniv:'B',lv_night:'B',lv_wed:'B',fr_job:'B',fr_family:'B',stay_name:'B',stay_quarrel:'B',st_quarrel:'B',sw_grow:'B',sw_spring:'B'};
  const EP2_RATE={A:.7,B:.75,C:.75};
  const EP2_MS=['stay_name','lv_night','lv_wed','lv_anniv','sw_grow','sw_spring'];
  const ep2Tight=()=>!!(S&&S.phase==='epi'&&S.epi&&(S.epi.ph==='A'||S.epi.ph==='B'));
  const ep2Gap=()=>{ const p=S.epi&&S.epi.ph; return p==='A'?.5:p==='B'?.7:1; };
  const EP2_DAY=[
    '도시는 아무 일도 없었다는 듯 아침을 맞았다. 무너진 담장 앞에 공사 안내판이 섰다.',
    '{N은} 신호등 앞에서 한참을 서 있었다. 초록불이 두 번 지나간 뒤에야 건넜다.',
    '손등의 자국이 어제보다 옅어졌다. {N이} 그것을 오래 들여다보았다.',
    '뉴스는 그 겨울의 일을 가스 사고라고 불렀다. {N은} 채널을 돌리지 않고 끝까지 보았다.',
    '빨래를 널었다. {N이} 옷걸이를 무기 쥐듯 쥐고 있어서 한 번 웃었다.',
    '비가 왔다. {N은} 창가에 앉아 빗소리를 들었다. 싸울 일이 없는 비는 처음이라고 했다.',
    '{N이} 편의점에서 돌아왔다. 봉지 안에는 같은 삼각김밥이 일곱 개 들어 있었다.',
    '밤이 조용했다. 조용한 밤에 익숙해지는 데에도 시간이 걸린다는 걸 알았다.',
    '{N이} 현관에 신발을 가지런히 놓았다. 당신 것 옆에, 반 뼘쯤 떨어뜨려서.',
    '전쟁이 있던 골목에 다시 가게들이 문을 열었다. {N은} 간판을 하나하나 소리 내어 읽었다.',
    '{N이} 낮잠을 잤다. 서번트일 때는 잠들 필요가 없었다고, 깨어나서 멋쩍게 말했다.',
    '저녁을 먹고 둘이서 설거지를 했다. 그릇 하나가 깨졌고, 아무도 죽지 않았다.',
    '아침에 {N의} 기척에 먼저 눈이 떠졌다. 경계가 아니라 그냥 사람의 기척이었다.',
    '열나흘째 밤이었다. 그 겨울과 꼭 같은 길이를, 이번에는 아무도 잃지 않고 보냈다.'];
  const EP2_MON={2:'벚꽃이 피었다 졌다. {N은} 꽃잎이 떨어지는 속도를 한참 지켜보았다.',3:'낮이 길어졌다. {N의} 옷장에 반소매가 생겼다.',4:'장마가 시작되었다. 현관에 우산이 두 개 나란히 걸렸다.',
    5:'매미가 울었다. {N은} 선풍기 앞을 좀처럼 떠나지 않았다.',6:'여름의 끝, 불꽃놀이 소리가 멀리서 들렸다. {N은} 한 번 움찔했다가 웃었다.',7:'바람이 선선해졌다. 장 보는 길에 {N이} 먼저 장바구니를 들었다.',
    8:'은행잎이 떨어졌다. {N이} 이 동네 길을 당신보다 잘 알게 되었다.',9:'첫서리가 내렸다. 둘이서 겨울 이불을 꺼냈다.',10:'다시 겨울이 왔다. 손등이 조금 시렸지만, 그뿐이었다.',
    11:'그 겨울로부터 한 해가 가까워졌다. 달력의 그 날짜에 {N이} 작은 동그라미를 쳐 두었다.',12:'한 해가 지났다. 눈이 녹고, 손등의 자국은 이제 햇빛 아래서만 보였다.'};
  const EP2_YR=['{N과} 맞는 봄이 하나 더 지났다.','집 안의 물건들이 조금씩 둘의 것이 되어 갔다.','{N은} 이제 전철 노선도를 보지 않고 갈아탔다.','동네 사람들은 {N을} 이름으로 불렀다. 이 세계에서 쓰는 이름으로.',
    '그 겨울 이야기를 꺼내는 날이 한 해에 한두 번으로 줄었다.','현관의 신발이 몇 번 바뀌었다. 놓이는 자리는 그대로였다.','{N이} 생전의 일을 농담처럼 말하게 되었다.','사진첩이 한 권 찼다.','평범한 해였다. 그게 얼마나 드문 일인지 둘 다 알고 있었다.'];
  const ep2N=(s)=>{ const h=H_BY[S.hero]; return nf(s.replace(/\{N의\}/g,h.name+'의'),h); };
  // 서번트 갈래: 현대 > 근대 > 박식 > 비전투 > 야망 순으로 먼저 맞는 변형을 쓴다
  const ep2Tags=h=>['now','modern','sage','civil'].filter(k=>EP2_TAGS[k].includes(h.id)).concat((h.traits||[]).includes('야망')?['bold']:[]);
  const ep2V=(x,h)=>{ if(Array.isArray(x)) return x; const k=ep2Tags(h).find(k=>x[k]); return k?x[k]:x.d; };
  const ep2Alt=(id,part)=>{ const a=EP2_ALT[id], h=H_BY[S.hero]; return a&&ep2Tags(h).includes(a.tag)?a[part]:undefined; };
  const EP2_FX={bond1:()=>add({bond:1}),bond2:()=>add({bond:2}),will1:()=>add({will:1}),will2:()=>add({will:2}),none:()=>{},rel4:()=>relGain(4),rel5:()=>relGain(5),rel6:()=>relGain(6),rel8:()=>relGain(8),
    trust2:()=>add({trust:2}),trust3:()=>add({trust:3}),trust4:()=>add({trust:4}),health1:()=>add({health:1}),health2:()=>add({health:2}),wealth1:()=>add({wealth:1}),wealth3:()=>add({wealth:3}),'wealth-5':()=>{add({wealth:-5});relGain(4);},lore2:()=>add({lore:2})};
  const ep2Wish=()=>!/^(없|딱히 없|아무것도)/.test(H_BY[S.hero].wish||'없');
  function ep2EvOk(e,r){ const E=S.epi, h=H_BY[S.hero], T=ep2Tags(h);
    if(e.ph!==E.ph||(E.relUsed||[]).includes(e.id)) return false;
    if(e.not&&[].concat(e.not).some(k=>T.includes(k))) return false; if(e.only&&!T.includes(e.only)) return false;
    if(e.wish&&!ep2Wish()) return false; if(e.day&&E.d!==e.day) return false; if(e.mon&&(E.m<e.mon[0]||E.m>e.mon[1])) return false; return true; }
  function ep2EvGo(e){ const h=H_BY[S.hero], D=RLEP[e.id], r=relOf(), fx={}, R={};
    for(const c of D.c){ fx[c.key]=EP2_FX[e.fx[c.key]]; R[c.key]=c.r.map(x=>ep2V(x,h)); }
    epRel(e.id,{b:D.b.map(x=>ep2V(x,h)),r:R,fx,hide:k=>(e.love||[]).includes(k)&&!(r&&r.track==='love')}); }

  const ep2NV=(v,d)=>{ if(!v) return d; const k=ep2Tags(H_BY[S.hero]).find(k=>v[k]); return k?v[k]:d; };
  function ep2Start(){ const E=S.epi; E.ph='A'; E.d=0; E.m=1; E.cy=0; E.k=0; E.n=ri(7,9); E.dayU=[]; }
  // A · B 구간의 사건 하나: 인연 장면 → 이어지는 장면 → 그 구간의 사건
  function ep2Pick(){ const E=S.epi, r=relOf(), ph=E.ph; if(S.pending) return true;
    if(r&&relDue()){ E.relK=E.k+(ph==='A'?2:1); relScene(); return true; }
    const fixed=EP2_EV.find(e=>(e.day||0)===E.d&&ph==='A'&&e.day&&ep2EvOk(e,r)); if(r&&fixed){ ep2EvGo(fixed); return true; }   // 날짜가 정해진 사건
    if(!r||!ch(EP2_RATE[ph])) return false;
    const used=E.relUsed||[]; E.used=E.used||[];
    const c=EP_REL.filter(x=>(EP2_PH[x.id]||'').includes(ph)&&x.w>0&&!used.includes(x.id)&&x.c(r)).map(x=>({x,w:x.w,rel:1}))
      .concat(EPI_POOL.filter(x=>(EP2_PH[x.id]||'').includes(ph)&&!E.used.includes(x.id)&&x.c()).map(x=>({x,w:x.w||1,rel:0})))
      .concat(EP2_EV.filter(e=>!e.day&&ep2EvOk(e,r)).map(e=>({x:{id:e.id,f:()=>ep2EvGo(e)},w:3,rel:1})));
    if(!c.length) return false;
    const ms=c.filter(o=>EP2_MS.includes(o.x.id));   // 서류 · 그날 밤 · 결혼 같은 고비는 먼저 챙긴다
    const p=ms.length&&ch(.6)?wpick(ms,o=>o.w):wpick(c,o=>o.w); if(!p.rel) E.used.push(p.x.id); p.x.f(); return true; }
  // 한 걸음. true면 이 걸음을 여기서 처리했다
  function ep2Step(){ const E=S.epi; if(!E) return false;
    if(!E.ph){ if(E.i===1&&stayHome()&&relOf()) ep2Start(); else return false; }
    if(E.ph==='D') return false;
    if(!stayHome()){ E.ph='D'; return false; }   // 곁을 떠났거나 먼저 보냈다: 예전 방식으로
    const tick=()=>{ E.k++; relGain(STAY_YG); stayTrust(); relTick(); };
    if(E.ph==='A'){
      if(E.d>=EP2_N.A){ E.ph='B'; log('열나흘이 지났다. 이제 달이 지나간다.','sys'); return ep2Step(); }
      E.d++; tick(); log(`봄 · ${E.d}일째`,'night');
      const pool=EP2_DAY.map((_,i)=>i).filter(i=>i<EP2_DAY.length-1&&!E.dayU.includes(i)); const i=E.d>=EP2_N.A?EP2_DAY.length-1:pick(pool); E.dayU.push(i); log(ep2N(ep2NV(EP2_DAYV[i],EP2_DAY[i])),'n');
      ep2Pick(); H.change(); return true; }
    if(E.ph==='B'){
      if(E.m>=EP2_N.B){ E.ph='C'; log('한 해가 지났다. 이제 해가 지나간다.','sys'); return ep2Step(); }
      E.m++; tick(); log(`첫 해 · ${E.m}달째`,'night'); log(ep2N(EP2_MON[E.m]),'n');
      if(E.m===EP2_N.B){ S.age++; S.year++; mark('calm'); if(S.age>=40) add({health:-ageWear()}); famYear(); if(S.pending) S.pending=null; }   // 첫 해의 끝: 한 살을 먹는다 (이 구간에는 사망 판정이 없다)
      ep2Pick(); H.change(); return true; }
    // C: 예전 방식 그대로, 한 해씩만 흐른다 (passYears가 1로 줄인다). 넷에 한 번은 사건 없는 해
    if(E.cy>=EP2_N.C){ E.ph='D'; return false; }
    E.cy++; E.k++;
    if(ch(1-EP2_RATE.C)&&!E.arc&&!E.relNext&&!relDue()){ passYears(1); if(!S.dead){ const i=ri(0,EP2_YR.length-1); log(ep2N(ep2NV(EP2_YRV[i],EP2_YR[i])),'n'); } return true; }
    return false; }
  // 화면에 보일 때: A · B 구간의 날짜
  function ep2When(){ const E=S&&S.epi; if(!E||!E.ph||S.phase!=='epi') return null; return E.ph==='A'?{u:'d',n:Math.max(1,E.d)}:E.ph==='B'?{u:'m',n:E.m}:null; }
