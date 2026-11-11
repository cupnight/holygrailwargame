  /* ---------- 후반 위기 · 비스트 Ⅲ/R (셋쇼인 키아라) ----------
     「후반 위기 비스트 상세안」 16판. 검은 성배 위기의 틀(유닛 · 결전 · 공동전 · 마지막 밤)을 빌려 쓰고, 다른 곳은 갈래를 단다.
     c.type==='beast' · c.stage 0 시작 · 1 휩쓸기 · 2 봉인 · 3 강림
     유닛: cx 'sent' 센티넬(KP를 품음, 강림 뒤 guard=1 호위) · 'bb' 달에서 온 BB · 'boss'(bx=1) 키아라 */
  // 수치 (상세안 16판 · 17 · 18장)
  const BXK={pw:92, kpT:[0,.5,1.25,2.25,3.5,5], hpD:.05, hpA:.02, wdM:.85, npM:2, hp2:50, desc:-56, nd:-41, bbAdj:-10, relAdj:-.4,
    heal:15, healSm:20, npHeal:15, logos:1.25, nwD:11, nwR:.7, sentR:.7, bbHit:[10,15], gAct:.3, gCap:99, gMin:0, gMinMe:0, gCover:.6, gChip:.2, nunKeep:30, bbKeep:30};
  if(typeof globalThis!=='undefined'&&globalThis.__BXK) Object.assign(BXK,globalThis.__BXK); // 시험용 덮어쓰기
  const KP_N=['Body','Site','Mouth','Spice','Organ'];
  const KP_STAT={Body:2,Site:1,Mouth:0,Spice:3};
  const BXW=()=>{ const c=CXW(); return c&&c.type==='beast'?c:null; };
  const bxOn=()=>{ const c=BXW(); return !!(c&&!c.done); };
  const bxNunP=()=>{ const c=BXW(); return c&&c.nun?pairBy(c.nun):null; };
  const bxSents=()=>cxUnits().filter(u=>u.cx==='sent'&&u.alive&&!u.guard);
  const bxGuards=()=>cxUnits().filter(u=>u.cx==='sent'&&u.alive&&u.guard);
  const bxBBU=()=>cxUnits().find(u=>u.cx==='bb'&&u.alive)||null;
  const bxKiara=()=>{ const u=cxUnits().find(u=>u.cx==='boss'&&u.bx); return u&&u.alive?u:null; };
  const bxNunName=()=>{ const c=BXW(); return !c?'':c.stage>=3?'셋쇼인 키아라':c.nunKnown?'키아라 킷쇼인':'이름 모를 수녀'; };
  // BB가 어디에 있나: 'me' 플레이어의 서번트 · 'npc' NPC 조 · 'moon' 달에서 온 유닛 · 'none' 없음
  function bxBBWhere(){ const w=W(); if(w.heroAlive&&S.hero==='bb') return 'me'; const p=w.pairs.find(p=>p.hero==='bb'&&p.alive&&p.master); if(p) return 'npc';
    if(w.pairs.some(p=>p.hero==='bb')||S.hero==='bb') return 'none'; return 'moon'; }
  const bxBBP=()=>{ const c=BXW(); if(!c||!c.bb) return null; if(c.bb.at==='npc') { const p=pairBy(c.bb.i); return p&&p.alive?p:null; } if(c.bb.at==='moon') return bxBBU(); return null; };
  const bxSealing=()=>{ const c=BXW(); return !!(c&&c.stage===2&&c.bb&&c.bb.at!=='none'); };
  const bxKpLeft=()=>{ const c=BXW(); return c?c.kp.filter(k=>k.at!=='got').length:0; };
  // 키아라의 체력 배율: 남은 KP · 봉인이 버틴 날 · 흡수한 서번트 · 고쳐쓴 카르마 · 플레이어가 없는 싸움
  function bxMult(vsNpc){ const c=BXW(); if(!c) return 1; const kp=Math.min(5,bxKpLeft());
    let m=1+BXK.kpT[kp]+(c.sealDays||0)*BXK.hpD+(c.absorbed||0)*BXK.hpA; if(c.karma) m*=BXK.wdM; if(vsNpc) m*=BXK.npM; return m; }
  // 키아라가 받는 피해만 배율로 나눈다(체력은 0~100 그대로). 피해를 넣는 곳이 많아 hp 자체를 가로챈다
  function bxArmor(u){ if(!u||u._bxA) return; const d=Object.getOwnPropertyDescriptor(u,'hp'); let v=d&&'value' in d?d.value:(u._hp??100);
    Object.defineProperty(u,'_bxA',{value:1,enumerable:false,configurable:true});
    Object.defineProperty(u,'hp',{enumerable:true,configurable:true,get(){ return v; },set(n){ n=+n||0; if(n<v&&u.alive!==false){ let dmg=v-n; if(n<=0) dmg=Math.max(dmg,10); const w=S.war, mine=!!(w&&w.battle&&w.battle.e===u); n=Math.max(0,v-dmg/bxMult(!mine)); if(n>0&&n<.5) n=.5; } v=n; }}); }
  const bxFix=()=>{ const k=cxUnits().find(u=>u.cx==='boss'&&u.bx); if(k) bxArmor(k); };
  // 단서를 며칠 뒤에 흘린다 (6-1: 그 순간 · 며칠 뒤 · 반전 때)
  function bxLater(days,t,k){ const c=BXW(); (c.clues=c.clues||[]).push({d:W().day+(Array.isArray(days)?ri(days[0],days[1]):days),t,k:k||'war'}); }
  function bxClues(){ const c=BXW(), w=W(); if(!c.clues) return; const now=c.clues.filter(x=>x.d<=w.day); c.clues=c.clues.filter(x=>x.d>w.day);
    for(const x of now){ const t=typeof x.t==='function'?x.t():x.t; if(t) log(t,x.k); } }

  // ---- 시작: 수녀 조 ----
  function bxSetup(c,pairs){ const w=W(); c.type='beast'; c.kp=KP_N.map(k=>({k,at:'kiara'})); c.clues=[]; c.nunKills=0; c.sealDays=0; c.absorbed=0;
    const ok=p=>p&&!p.ghost&&p.aid!=='sibling'&&!['bb','meltryllis','passionlip'].includes(p.hero)&&!CLS[p.cls].sp;
    let p=pairs.find(p=>p.aid==='burial'&&ok(p))||pick(pairs.filter(ok));
    if(!p) p=pairs.find(p=>!p.ghost)||pairs[0];
    const a=ARCHE.find(a=>a.id==='burial');
    if(['bb','meltryllis','passionlip'].includes(p.hero)){ const used=new Set([S.hero,...pairs.map(x=>x.hero)]); const hs=HEROES.filter(x=>x.cls===p.cls&&!used.has(x.id)&&!['bb','meltryllis','passionlip'].includes(x.id)); if(hs.length) p.hero=pick(hs).id; }
    Object.assign(p,{aid:'burial',arche:a.n,tac:a.tac,pw:BXK.pw,mname:'이름 모를 수녀',bxNun:1});
    c.nun=p.i; c.nunHero=p.hero; return c; }
  // 숨김 보정: 수녀의 서번트는 맞붙는 상대 능력치보다 세 단계 위로 맞춘다(센티넬이 되기 전까지)
  let BX_VS=null;
  function bxNunStats(p,o){ const opp=BX_VS&&BX_VS[0]===p?BX_VS[1]:BX_VS&&BX_VS[1]===p?BX_VS[0]:null;
    let ref=null; if(opp&&!opp.bxNun) ref=npcParams(opp).p; else if(S.war&&S.war.battle&&S.war.battle.e===p&&S.war.heroAlive) ref=myParams().p;
    if(!ref) return o; return o.map((r,i)=>{ const t=rankShift(String(ref[i]).split(' ')[0],3); return PV(t)>PV(r)?t:r; }); }

  // ---- 낮의 진행 ----
  function bxDay(){ const w=W(), c=BXW(); if(!c||c.done) return false; bxFix();
    // 키아라는 날이 바뀔 때 회복한다 (두 번째 몸은 50까지)
    const k=bxKiara(); if(k&&w.day>c.descD){ k.hp=Math.min(k.phase2?BXK.hp2:100,k.hp+BXK.heal); k.sm=clamp(npcSmOf(k)+BXK.healSm); }
    if(c.stage<1&&(c.nunKills>=2||w.day>=4)){ c.stage=1; c.d1=w.day; c.kamaHint=w.day+ri(2,3);
      if(w.heroAlive&&S.hero==='bb') bxLater(1,()=>W().heroAlive&&c.stage<2?`${hero().name}${J(hero().name,이)} 수녀 조의 소문을 듣고 무언가 말하려다 그만두었다. “그 사람… 아, 아니에요. 아무것도.”`:'','voice'); bxLater([2,3],()=>bxNunP()&&!w.heroAlive?'':'한 조가 밤마다 다른 조를 찾아다닌다는 소문이 돌았다. 그 조와 싸운 쪽은 하나같이 돌아오지 못했다고 한다.'); }
    if(c.stage===1&&c.d1===w.day-1&&w.heroAlive) bxLater([0,2],()=>{ const n=bxNunP(); return n&&n.alive&&c.stage<2?`다른 조의 사역마가 쪽지를 떨어뜨리고 갔다. “${cn(n)} 조에는 손대지 마라. 그 수녀는 지는 법을 모른다.”`:''; });
    if(c.stage<2&&w.day>=7) bxSeal();
    else if(c.stage===2) bxSealDay();
    bxClues();
    if(c.revealD===w.day&&c.stage===2) bxReveal();
    if(c.stage===3) bxPostDay();
    if(!w.heroAlive) return false;
    if(c.bbAsk===w.day){ c.bbAsk=0; bxBBAsk(); return true; }
    if(c.kamaHint===w.day&&S.hero==='kama'){ log(`${hero().name}: “그 수녀, 조금 지켜보는 게 좋겠어요. …이유요? 글쎄요. 같은 냄새가 나서, 라고 해 둘까요.”`,'voice'); }
    const inv=c.stage===3?cxPlan():null; if(inv&&inv.alive){ cxInvite(inv); return true; }
    return false; }

  // ---- 7일차: 봉인 ----
  function bxSeal(){ const w=W(), c=BXW(), at=bxBBWhere(); c.stage=2; c.d2=w.day; c.sealD=w.day; c.bb={at};
    const n=bxNunP();
    if(at==='none'){ bxNoBB(); return; }
    log('자정, 도시 한가운데서 성배의 기척이 한순간 끊겼다. 누군가 성배를 통째로 봉인했다.','war',{fx:{t:'descent',d:w.day,g:CX().grail}});
    log('봉인되는 순간 성배가 한 번 크게 일렁였다.','war');
    bxLater(2,'그날 밤 성배 쪽에서 무언가 새어 나가는 걸 봤다는 사람이 있다.');
    if(at==='moon'){ const u={i:c.seq++,cx:'bb',hero:'bb',cls:'moon',hp:100,sm:100,pw:80,tac:'grail',aid:'moon',mname:'달의 이레귤러',master:false,alive:true,seals:0,revealed:true,clsKnown:true,known:true,intel:40,artKnown:false};
      c.units.push(u); c.bb.i=u.i;
      log(`감독관의 통지: 성배를 봉인한 것은 일곱 조 바깥의 이레귤러, ${pName(u)}. 달에서 왔다고 한다.`,'notice'); }
    else if(at==='npc'){ const p=w.pairs.find(p=>p.hero==='bb'&&p.alive&&p.master); c.bb.i=p.i; p.bxBB=1; revealPair(p,''); p.known=true;
      log(`감독관의 통지: 성배를 봉인한 것은 ${pName(p)} 조. 성배를 독차지한 조로 본다.`,'notice'); }
    else { c.bb.me=1; log(`${hero().name}${J(hero().name,이)} 손을 펼쳤다. 도시 한가운데의 성배가 보이지 않는 상자에 갇혔다.`,'voice'); c.bbAsk=w.day; }
    log('문 셀의 백업: 봉인을 쥔 BB는 모든 능력치가 령주를 쓴 것처럼 한 단계씩 버틴다.','war');
    // 수녀 조의 거짓 탈락 통지
    if(n&&n.alive){ n.alive=false; n.bxFake=1; n.revealed=true; pairOut(n,'탈락 통지(거짓)'); log(`감독관의 통지: ${cn(n)} 조 탈락.`,'notice');
      bxLater(3,'그 조가 쓰러진 자리에서 아무것도 수습되지 않았다는 이야기를 들었다.'); }
    // 토벌령: 수녀가 매장기관 신분으로 감독관을 움직였다
    const tgt=at==='me'?'당신의 조':at==='npc'?`${pName(pairBy(c.bb.i))} 조`:pName(bxBBU());
    log(`감독관의 토벌령: 성배를 가로챈 ${tgt}${at==='me'?'를':J(tgt,을)} 쓰러뜨려라. 그 체력을 무너뜨린 조에게 령주 한 획을 준다.`,'notice');
    bxSusp(); bxSentStart();
    bxLater([2,3],'원인 모를 깊은 잠에 빠진 사람이 늘고 있다고 아침 뉴스가 전했다.');
    bxLater([2,3],'센티넬이 다녀간 골목마다 깊이 잠든 사람이 나온다는 소문이 돌았다.');
    if(at!=='me') bxLater([2,3],'BB가 센티넬을 막아서는 걸 봤다는 사람이 있다.');
    bxLater([3,4],()=>{ const q=contracted().find(p=>(p.bxSus||0)>=70); return q&&c.stage===2?`${q.known?q.mname:cn(q)+' 조의 마스터'}에게서 짧은 전갈이 왔다. “토벌령이 내려지기 전날 밤, 교회에 매장기관 사람이 드나들었다더군. …BB의 파수꾼이라면서, 정작 BB를 제일 먼저 노리는 게 그것들이더군.”`:''; });
    bxLater(4,'잠든 사람이 늘수록, 도시 한가운데의 무언가가 무거워진다고 한다.');
    wrec('hint','성배가 봉인되었다 · BB에게 토벌령'); }
  // BB가 없는 생: 성배가 차는 밤 (18-J)
  function bxNoBB(){ const w=W(), c=BXW(), n=bxNunP();
    log('자정, 성배가 있던 자리가 텅 비어 있었다. 감독관은 성배가 아직 차지 않았으니 전쟁은 이어진다고만 알렸다.','notice');
    if(n&&n.alive){ n.alive=false; n.bxFake=1; n.revealed=true; pairOut(n,'탈락 통지(거짓)'); log(`감독관의 통지: ${cn(n)} 조 탈락.`,'notice'); }
    c.noBB=1; c.descAt=BXK.nwD; bxSentStart();
    // 남은 자리: 7일차 전에 탈락한 서번트를 최근 순으로 (봉인이 없어 성배째 삼켰다)
    const fell=w.pairs.filter(p=>!p.alive&&!p.bxFake&&p.hero!=='bb'&&!p.bxSentUsed).sort((a,b)=>((b.out&&b.out.d)||0)-((a.out&&a.out.d)||0));
    for(const p of fell){ if(!bxFreeKp()) break; bxMkSent(p.hero,{src:p}); }
    bxLater(1,'쓰러진 서번트를 닮은 그림자들이 밤마다 마스터를 사냥한다는 소문이 돌았다.');
    bxLater(3,()=>c.stage===2?'성배가 있던 자리 아래에서 밤마다 무언가 차오르는 소리가 난다고 한다. 곧 넘칠 거라고 했다.':'');
    bxLater([2,3],'원인 모를 깊은 잠에 빠진 사람이 늘고 있다고 아침 뉴스가 전했다.');
    bxSusp(); wrec('hint','성배가 있던 자리가 비었다'); }
  const bxFreeKp=()=>BXW().kp.find(k=>k.at==='kiara')||null;
  // 센티넬: 수녀의 서번트 → (BB가 쥔 하나) → 소환되지 않은 멜트릴리스 · 패션립 → 7일차 이후 탈락하는 서번트
  function bxSentStart(){ const w=W(), c=BXW();
    bxMkSent(c.nunHero,{nun:true});
    if(c.bb.at!=='none'){ const k=bxFreeKp(); if(k){ if(c.bb.at==='me'){ k.at='got'; c.kpGot=(c.kpGot||0)+1; c.kpMe=(c.kpMe||0)+1; } else k.at='bb'; } }
    const summoned=new Set([S.hero,...w.pairs.map(p=>p.hero)]);
    for(const id of ['meltryllis','passionlip']) if(!summoned.has(id)) bxMkSent(id,{ego:true}); }
  function bxMkSent(hid,o){ const c=BXW(), k=bxFreeKp(); if(!k) return null; const hh=H_BY[hid];
    const u={i:c.seq++,cx:'sent',hero:hid,kp:k.k,cls:hh.cls,hp:100,sm:100,pw:75,tac:'grail',aid:'kiara',mname:'',master:false,alive:true,seals:0,revealed:!!(o.src&&o.src.revealed)||!!o.ego||!!o.mine,clsKnown:true,known:true,intel:30,artKnown:o.src?!!o.src.artKnown:false,ego:!!o.ego,nunS:!!o.nun,mine:!!o.mine};
    k.at='s'+u.i; if(o.src) o.src.bxSentUsed=1; c.units.push(u);
    if(c.stage>=2&&!o.nun&&!o.ego&&c.stage<3){ if(o.mine) log(`당신의 서번트였던 ${hh.name}${J(hh.name,이)} 다시 일어섰다. 눈빛이 낯설었다.`,'war'); else bxLater([2,3],'탈락했다던 서번트를 다시 봤다는 사람이 있다.'); }
    return u; }
  // 의심 점수 (9장 · 17장: 토벌령 자체의 수상함 +20)
  const BX_KNOW=['elder','atlas','detective','prodigy','retired','wanderer'], BX_CHURCHA=['executor','eighth'];
  function bxSusp(){ const c=BXW(), al=id=>alAx(id);
    for(const p of contracted()){ const ax=al(p.hero)||[];
      let v=p.pw/2+({cunning:20,defensive:10,hunter:0,grail:0,proud:-10,desperate:-10,reckless:-15,naive:-20}[p.tac]||0)
        +(BX_KNOW.includes(p.aid)?15:BX_CHURCHA.includes(p.aid)?-15:p.aid==='priest'?10:0)+(ax[0]==='질서'?-10:ax[0]==='혼돈'?10:0)+(npcKnowOf(p,c.nun)/4)+20;
      if(p.hero==='kama') v+=30; p.bxSus=Math.round(v); } }
  const npcKnowOf=(p,i)=>{ try{ const t=pairBy(i); return t?npcKnow(p,t)||0:0; }catch(e){ return 0; } };
  const bxBelieve=p=>(p.bxSus||0)<50&&!p.ally&&!p.truce;
  // ---- 봉인 중의 낮 ----
  function bxSealDay(){ const w=W(), c=BXW(); c.sealDays=w.day-c.sealD;
    if(c.noBB){ if(w.day>=c.descAt||cxTeams()<=2) { c.revealHow='none'; bxDescend(); } return; }
    if(w.day>=13&&!c.revealD){ c.revealHow='force'; c.revealD=w.day; }
    if(c.d2+4===w.day) log('도시 한가운데서 밤마다 무언가가 문을 두드린다는 소문이 돌았다.','war'); }

  // ---- 밤 ----
  function bxNight(){ const w=W(), c=BXW(); if(!c||c.done||w.ended) return; bxFix();
    const busy=new Set(((w.cxWent&&w.cxWent.d===w.day)?w.cxWent.ids:[]));
    if(c.stage===2){
      // 센티넬: BB 쪽을 먼저(70%), 나머지는 도시를 돈다. BB가 없는 생은 70%로 사냥에 나선다
      let atBB=0;
      for(const u of bxSents()){ if(!u.alive) continue; const bb=bxBBP(), me=c.bb.at==='me'&&w.heroAlive;
        if(!c.noBB&&(bb||me)&&ch(BXK.sentR)){ if(me){ if(!w.cxHit) w.cxHit=u.i; continue; } atBB++; continue; }
        if(!ch(c.noBB?BXK.nwR:.3)) continue;
        const pool=[...(w.heroAlive&&!w.cxHit&&c.bb.at!=='me'?[{me:true}]:[]),...contracted().filter(p=>!busy.has(p.i)&&!p.bxBB)]; if(!pool.length) continue;
        const t=pick(pool); if(t.me){ w.cxHit=u.i; continue; } busy.add(t.i); bxNpcVsSent(t,u); }
      if(atBB&&!c.revealD) bxHitBB(bxBBP(),ri(BXK.bbHit[0],BXK.bbHit[1])+(atBB-1)*2,'sent'); // 센티넬이 많을수록 더 깎인다(밤마다 10~15)
      // NPC: 수녀를 의심하는 조는 센티넬을 사냥하고, 토벌령을 믿는 조는 BB를 친다
      for(const p of contracted()){ if(busy.has(p.i)||p.halt>0||p.bxBB) continue;
        if((p.bxSus||0)>=70&&bxSents().length&&ch(.25)){ busy.add(p.i); bxNpcVsSent(p,pick(bxSents())); continue; }
        if(!c.noBB&&bxBelieve(p)&&p.hp>=50&&ch(.3)){ const bb=bxBBP(); busy.add(p.i);
          if(bb){ bxNpcVsBB(p,bb); } else if(c.bb.at==='me'&&w.heroAlive){ p.provoked=Math.max(p.provoked||0,1); w.hunted=true; } } }
    }
    for(const u of c.units) if(u.alive&&u.cx==='sent'){ u.hp=clamp(u.hp+(u.guard?10:8)+(u.kp==='Organ'?12:0)); u.sm=clamp(npcSmOf(u)+15); }
    const bb=bxBBU(); if(bb) bb.sm=clamp(npcSmOf(bb)+15);
    if(c.stage===3) bxPostNight(busy); }
  // NPC와 센티넬의 싸움 (플레이어가 없는 곳)
  function bxNpcVsSent(p,u){ const w=W(); BX_VS=[p,u]; const r=npcFight(p,u,false); BX_VS=null;
    if(u.hp<=0) bxUnitDown(u,p);
    if(p.hp<=0&&p.alive){ const lh=H_BY[p.hero]; if(lh.sp==='revive'&&!p.usedRevive){ p.usedRevive=true; p.hp=45; return; }
      p.alive=false; p.revealed=true; pairOut(p,'센티넬에게 쓰러졌다'); log(`감독관의 통지: ${cn(p)} 조 탈락.`,'notice'); if(p.ally) log(`동맹 ${p.mname}의 조가 무너졌다.`,'loss'); } }
  // BB와 싸움: 체력 30 아래면 봉인이 흔들린다(서번트는 쓰러지지 않는다)
  function bxNpcVsBB(p,bb){ BX_VS=[p,bb]; npcFight(p,bb,false); BX_VS=null; if(p.hp<1) p.hp=1;
    if(bb.hp<BXK.bbKeep) bxBBBroken(p); }
  function bxHitBB(bb,d,by){ if(!bb) return; bb.hp=clamp(bb.hp-d); if(bb.hp<BXK.bbKeep) bxBBBroken(by); }
  function bxBBBroken(by){ const c=BXW(), w=W(); if(c.revealD) return; const bb=bxBBP(); if(bb) bb.hp=Math.max(1,bb.hp);
    c.revealD=w.day+1; c.revealHow=by==='me'?'me':by==='sent'?'sent':'npc';
    if(by==='me'){ w.seals++; log('토벌 보상: 감독관의 사자가 찾아와 당신 손등에 령주 한 획을 그려 주었다.','seal'); bxKpTake('me','bb'); }
    else if(by&&by.i){ by.seals=(by.seals||0)+1; bxKpTake(by,'bb'); }
    else { const k=c.kp.find(k=>k.at==='bb'); if(k) k.at='kiara'; } }
  function bxKpTake(by,from){ const c=BXW(); const k=c.kp.find(k=>k.at===from); if(!k) return; k.at='got'; c.kpGot=(c.kpGot||0)+1; if(by==='me') c.kpMe=(c.kpMe||0)+1;
    const w=W(), n=c.kpGot;
    if(by==='me') log(n<=1?'익숙하지 않은 단맛이 혀끝에 남았다.':'회수할 때마다, 누군가 이쪽을 보고 있던 시선이 하나씩 끊긴다.','war');
    else if(by) bxLater(1,`어젯밤 ${pick(CX().sites)}에서 서번트 둘이 싸웠다. 한쪽은 아침에 흔적도 없었다.`);
    if(c.stage===2) bxLater(1,'깊은 잠에 빠졌던 사람 몇이 밤사이 깨어났다고 아침 뉴스가 전했다.'); }
  // 탈락한 서번트: 봉인 중이면 센티넬로, 강림 뒤에는 빈 KP가 있으면 호위로, 없으면 흡수
  function bxFallen(hid,o){ const c=BXW(); if(!c||c.done||c.stage<2||hid==='bb') return;
    if(bxFreeKp()){ const u=bxMkSent(hid,o); if(u&&c.stage===3){ u.guard=1; log(`${H_BY[hid].name}${J(H_BY[hid].name,이)} 키아라 곁으로 걸어가 무릎을 꿇었다. 호위가 하나 늘었다.`,'war'); } return; }
    c.absorbed=(c.absorbed||0)+1; if(c.stage===3) log(`쓰러진 ${H_BY[hid].name}의 영기가 키아라에게 녹아들었다.`,'war'); }

  // ---- 플레이어의 BB: 7일차의 부탁 · 봉인을 풀게 한다 ----
  function bxBBAsk(){ const w=W(), h=hero();
    decide({title:'BB의 부탁',body:`${h.name}${J(h.name,이)} 평소처럼 웃지 않았다. “선배, 잘 들어요. 성배는 제가 봉인했어요. 그 수녀… 매장기관의 그 사람이 성배를 노려요. …말하면 들리거든요. 그 사람은 지금 배를 채우느라 서두르지 않을 뿐이에요. 눈치채면 도시에 풀어 둔 걸 전부 불러들이고 바로 나와 버려요. 그러니 아무한테도 설명 못 하고, 지금부터는 다들 우리를 노릴 거예요. …제가 문을 열면, 남은 아이들은 전부 그쪽으로 돌아가 버려요. 너무 오래 끌어도 안 되고요.”`,war:true,choices:[
      {t:'믿는다',auto:true,f:()=>{ w.trust=clamp(w.trust+5); w.queue.push(()=>dayDecision()); return `“…역시 선배예요. 그럼 버텨 봐요, 우리 둘이서.”`; }},
      {t:'말없이 고개를 끄덕인다',f:()=>{ w.queue.push(()=>dayDecision()); return '“대답은 행동으로 해 줘요.”'; }}]}); }
  function bxDayActs(ch_){ const w=W(), c=BXW(); if(!bxOn()||!w.heroAlive) return;
    if(c.stage===2&&c.bb.at==='me'&&!c.revealD){ const sn=bxSents().length, got=c.kpGot||0, pc=contracted().filter(p=>p.ally||p.truce).map(p=>pName(p));
      ch_.unshift({t:'BB에게 봉인을 풀게 한다',d:`오늘 밤 결전을 연다 · 남은 센티넬 ${sn} · 거둔 KP ${got}/5 · 함께 갈 조 ${pc.length?pc.join(', '):'없음'}`,auto:sn===0&&w.hp>=60&&w.sm>=45,f:()=>{ c.revealHow='unseal'; c.unsealGo=w.day; bxReveal(); return `${hero().name}${J(hero().name,이)} 숨을 고르고 손을 들어 올렸다. “…좋아요. 열게요.”`; }});
      if(ch_[0].auto) ch_.slice(1).forEach(x=>x.auto=false); }
  }
  function bxNightActs(ch_){ const w=W(), c=BXW(); if(!bxOn()||!w.heroAlive) return; const h=hero();
    const sn=bxSents(); if(c.stage===2&&sn.length&&w.sm>=20) ch_.push({t:'센티넬을 사냥한다',d:'도시를 헤매는 센티넬 하나를 쓰러뜨린다. 쓰러뜨리면 감독관이 령주 한 획을 준다',auto:w.hp>60&&w.sm>=40,f:()=>bxHuntPick()});
    const bb=bxBBP(); if(c.stage===2&&bb&&!c.revealD&&c.bb.at!=='me'&&w.sm>=20) ch_.push({t:'토벌령을 따른다',d:`${pName(bb)}${J(pName(bb),과)} 싸운다. 체력을 무너뜨리면 령주 한 획`,f:()=>{ w.queue.push(()=>battle(bb,{attack:true,cx:bb.cx?true:undefined,bxBB:true})); }});
  }
  function bxHuntPick(){ const w=W(), sh=bxSents();
    decide({title:'센티넬을 사냥한다',body:'도시를 헤매는 센티넬들. 어느 쪽을 쫓을 것인가.',war:true,choices:[...sh.map(u=>({t:`${pName(u)}`,d:hpWord(u.hp),f:()=>{ w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:2,자유:1},{선:2}));
      const comp=contracted().filter(p=>(p.bxSus||0)>=70&&!(p.halt>0)&&ch(.25)||p.ally&&ch(.5)).map(p=>p.i); w.queue.unshift(()=>{ if(comp.length) log(`${comp.map(i=>pName(pairBy(i))).join(', ')} 조도 같은 센티넬을 쫓고 있었다. 오늘 밤은 함께 싸운다.`,'war'); battle(u,{attack:true,cx:true,joint:comp.length,comp}); }); }})),{...BACK}]}); }

  // ---- 반전 · 강림 ----
  const BX_CONF='…도시의 센티넬은 전부 그 사람의 눈과 귀예요. 그 아이들이 밤마다 도시의 단꿈을 그 사람에게 날라요. 그래서 그 사람은 서두르지 않았어요. 배가 부를 때까지 봉인 안에서 기다리면 되니까요. 하지만 누가 그 아이들을 노린다는 걸 알았다면, 그 자리에서 전부 불러들이고 봉인을 찢었을 거예요. 그래서 돌려 말할 수밖에 없었어요.';
  function bxReveal(){ const w=W(), c=BXW(); if(c.stage!==2) return; const how=c.revealHow||'force'; const bb=bxBBP();
    if(how==='force'){ log('열세 번째 밤이 지나자, 도시 한가운데의 상자가 안쪽에서 찢어졌다.','war');
      if(c.bb.at==='moon'&&bb){ bb.alive=false; bb.hp=0; } else if(c.bb.at==='npc'&&bb){ bb.alive=false; bb.revealed=true; pairOut(bb,'봉인이 찢어질 때 쓰러졌다'); log(`감독관의 통지: ${cn(bb)} 조 탈락.`,'notice'); }
      if(c.bb.at!=='me') log(`BB: “${BX_CONF.split('. ')[0]}. …미안해요. 끝까지는 못 버텼어요.” 마지막 말을 남기고 BB의 모습이 흩어졌다.`,'voice');
      const k=c.kp.find(k=>k.at==='bb'); if(k) k.at='kiara'; }
    else if(how==='unseal'){ log(`${hero().name}${J(hero().name,이)} 봉인을 풀었다. 도시 한가운데의 상자가 소리 없이 열렸다.`,'war'); }
    else { const where=how==='me'?'싸움이 끝난 자리에서':'새벽녘, 상처 입은 BB가 당신의 거처로 숨어들었다.';
      log(how==='me'?`BB가 무릎을 꿇은 채 웃었다. “…아, 됐어요. 이제는 말해도 되겠네요.”`:where,'war');
      log(`BB: “${BX_CONF} …그 수녀, 매장기관의 수녀가 키아라예요. 성배를 삼키려고 해요.”`,'voice');
      if(c.bb.at==='npc'&&bb){ bb.ally=true; bb.truce=true; bb.bxAlly=1; } c.bbAlly=c.bb.at!=='me'; }
    c.karma=['me','npc','sent','unseal'].includes(how);
    bxDescend(); }
  function bxDescend(){ const w=W(), c=BXW(); if(c.stage>=3) return; const nb=!!c.noBB; c.stage=3; c.d3=w.day; c.descD=w.day; c.sealDays=nb?0:Math.max(0,w.day-c.sealD); if(nb) c.sealDays=Math.max(0,w.day-c.sealD);
    if(!c.zones.includes(CX().grail)) c.zones.push(CX().grail);
    log(nb?`자정, 성배가 가득 찼다. 그 앞에 쓰러진 줄 알았던 수녀가 서 있었다. 수녀는 성배를 두 손으로 받쳐 들고, 남김없이 마셨다.`:`쓰러진 줄 알았던 수녀가 ${CX().grail}에 나타났다. 수녀는 열린 성배를 두 손으로 받쳐 들고, 남김없이 마셨다.`,'war',{fx:{t:'descent',d:w.day,g:CX().grail}});
    log('“킷쇼인”이라는 이름이 녹아내렸다. 그 자리에 선 것은 셋쇼인 키아라. 비스트 Ⅲ/R.','war');
    const n=bxNunP(); if(n) n.mname='셋쇼인 키아라';
    const u={i:c.seq++,cx:'boss',bx:1,how:'new',hero:'kiara',cls:'beast',hp:100,sm:100,phase2:false,pw:BXK.pw,tac:'grail',aid:'kiara',mname:'셋쇼인 키아라',master:false,alive:true,seals:3,revealed:true,clsKnown:true,known:true,intel:60,artKnown:false};
    c.units.push(u); bxArmor(u);
    // 남은 센티넬은 KP를 쥔 채 성배 앞으로 모여 호위가 된다
    const gs=bxSents(); gs.forEach(g=>{ g.guard=1; });
    if(gs.length) log(`센티넬 ${['','하나가','둘이','셋이','넷이','다섯이'][gs.length]} ${CX().grail}${J(CX().grail,으로)} 모여들어 키아라를 둘러섰다. 키아라의 손에 KP ${bxKpLeft()}개가 남았다.`,'war');
    else log(bxKpLeft()?`키아라의 손에 KP ${bxKpLeft()}개가 남았다.`:'키아라에게 돌아올 눈은 하나도 남아 있지 않았다.','war');
    if(c.sealDays>0) log(`키아라: “${c.sealDays}일 동안 이 도시를 맛보았답니다. 교회는 참 고분고분하지요. 반쪽 몸으로는 그 아이의 문을 열 수 없었으니까요.”`,'enemy');
    else log('키아라: “기다린 보람이 있었습니다. 이 잔은 처음부터 저를 위해 차오르고 있었지요.”','enemy');
    if(c.karma){ log('봉인이 갈라지는 순간, BB가 마지막 힘으로 C.C.C.를 펼쳐 키아라를 고쳐 썼다. 키아라가 처음으로 얼굴을 찌푸렸다.','war'); log('고쳐쓴 카르마: 키아라의 카르마 파지가 예전만큼 듣지 않는다.','war'); }
    if(c.bb.at!=='none'&&c.revealHow!=='force'){ const g=c.kpGot||0; log(g>=3?'BB: “…많이 거둬 줬네요. 고마워요. 이 정도면 그 사람, 배가 덜 불렀을 거예요.”':g<=1?'BB: “…조금만 더 시간이 있었으면 좋았을 텐데요.”':'BB: “할 수 있는 만큼은 했어요. 남은 건 같이 해요.”','voice'); }
    for(const p of contracted()){ p.cxKnow=true; p.cxStance='break'; }
    bxVoice('desc');
    wrec('hint',`셋쇼인 키아라가 강림했다 — 남은 KP ${bxKpLeft()}`); }
  function bxPostDay(){ }
  // 강림 뒤의 밤: 성배로 가는 NPC 조는 한 번만 싸운다(가장 강한 조가 이끌고, 나머지는 함께 간다)
  function bxPostNight(busy){ const w=W(), c=BXW(), k=bxKiara(); if(!k) return;
    const pact=w.cxPact&&w.cxPact.d===w.day?w.cxPact.i:0;
    if(pact){ const p=pairBy(pact); w.cxPact=null; if(p&&p.alive&&!busy.has(p.i)){ busy.add(p.i); p.cxGo=0; log(`${pName(p)} 조는 약속한 자리에서 한참 기다리다 돌아갔다고 한다.`,'war'); if(w.heroAlive) cxTraitEnd({명예:-3,충성:-1,연민:-1},{질서:-4}); } }
    const last=contracted().length+(w.heroAlive?1:0)<=1;
    const grp=contracted().filter(p=>!busy.has(p.i)&&!(p.halt>0)&&(w.heroAlive?p.cxGo===w.day&&p.hp>=40:(last&&ch(.7)||p.hp>=55&&ch(.5))));
    if(grp.length) bxNpcJoint(grp,false);
    grp.forEach(p=>busy.add(p.i)); }
  // NPC 공동전 (18-G · 18-I): 가장 강한 조가 이끌고, 나머지 조는 합마다 함께 움직인다. 마지막 밤에는 이끄는 조가 쓰러지면 다음 조가 이어받는다
  let BX_COMP=null;
  function bxNpcJoint(grp,final){ const k=bxKiara(); if(!k||!grp.length) return;
    const order=grp.slice().sort((a,b)=>npcPower(b,false,1)-npcPower(a,false,1)), out=[];
    for(let i=0;i<order.length&&k.alive;i++){ const p=order[i]; if(!p.alive||out.includes(p.i)) continue;
      const comp=order.filter(q=>q!==p&&q.alive&&!out.includes(q.i)); bxNpcVsKiara(p,final,comp,out);
      if(!final) break; } }
  const bxFreed=()=>{ const c=BXW(); return c?(c.freed||[]).length:0; };
  function bxNpcVsKiara(p,final,comp,out){ const k=bxKiara(); if(!k) return; out=out||[];
    BX_VS=[p,k]; BX_COMP={lead:p,comp:comp||[],out,np:[],final:!!final}; p.cxAssist=5*bxFreed(); // 풀려난 멜트릴리스 · 패션립은 판정 보정으로만 붙는다
    try{ npcFight(p,k,!!final); } finally{ BX_VS=null; BX_COMP=null; p.cxAssist=0; }
    if(k.hp<=0) bxUnitDown(k,p);
    for(const q of [p,...(comp||[])]) bxNpcFall(q); }
  function bxNpcFall(p){ if(!p||!p.alive||p.hp>0) return; const lh=H_BY[p.hero]; if(lh.sp==='revive'&&!p.usedRevive){ p.usedRevive=true; p.hp=45; return; }
    p.alive=false; p.revealed=true; pairOut(p,'키아라 앞에서 쓰러졌다'); log(`감독관의 통지: ${cn(p)} 조 탈락. 키아라 앞에서.`,'notice'); if(p.ally) log(`동맹 ${p.mname}의 조가 무너졌다.`,'loss'); }
  // NPC끼리 키아라와 싸우는 합마다 (npcDuel 안에서 부른다): 호위의 엄호 · 견제 · 협공, 함께 간 조의 휘말림 · 보구 · 엄호 · 견제 · 협공
  // X: 키아라와 맞선 조(대표) · K: 키아라. h0: 합이 시작될 때의 체력 · fire: 이번 합에 보구를 쏜 쪽
  const BX_AOE=/대군|대성|대계|대국|대왕|대마/;
  function bxDuelRound(A,B,r,h0,fire,final,hit){ const K=A.p.bx?A:B.p.bx?B:null; if(!K||!K.p.alive) return; const X=K.o, k=K.p, x=X.p, C=BX_COMP&&BX_COMP.lead===x?BX_COMP:null;
    const m=Math.min(bxMult(true),BXK.gCap), kLost=()=>Math.max(0,h0.get(K)-k.hp), xLost=()=>Math.max(0,h0.get(X)-x.hp), weakG=()=>bxGuards().sort((a,b)=>a.hp-b.hp)[0];
    const gHit=(g,d,by)=>{ g.hp=clamp(g.hp-Math.round(d)); if(g.hp<=0){ bxUnitDown(g,by||x); bxLater(1,`밤사이 ${CX().grail}에서 ${pName(g)}${J(pName(g),이)} 쓰러졌다고 한다.`); } };
    // 대표 조의 범위 보구는 호위를 휩쓴다
    if(fire.get(X)&&BX_AOE.test(artOf(X.h).k||'')) for(const g of bxGuards()) gHit(g,kLost()*m*.5);
    // 호위: 합마다 하나당 30%(체력 비례)로 엄호 60% · 견제 20% · 협공 20%
    let cov=false;
    for(const g of bxGuards()){ if(!ch(BXK.gAct*Math.max(.2,g.hp/100))) continue; const t=rnd();
      if(t<BXK.gCover){ const l=kLost(); if(l>0&&l>=BXK.gMin&&!cov){ cov=true; const a=Math.round(l*(.4+rnd()*.2)); k.hp=Math.min(k.phase2?BXK.hp2:100,k.hp+a); gHit(g,a*m); } }
      else if(t<BXK.gCover+BXK.gChip) K.bxCh={r:r+1,v:ri(3,6)};
      else hit(X,Math.max(1,(4+ri(0,5))*.6)); }
    if(!C) return;
    // 함께 간 조
    for(const q of C.comp){ if(!q.alive||C.out.includes(q.i)) continue; const qh=H_BY[q.hero];
      if(ch(.3)) q.hp=clamp(q.hp-ri(3,8)); // 휘말림
      { const cost=Math.round(npCostM(qh)*(22+npRV(qh)*3)), sm=npcSmOf(q);
        if(!C.np.includes(q.i)&&q.hp>20&&sm>=cost&&(k.hp<=35||x.hp<=35||r>=2&&ch(.15))&&ch(.7)){ C.np.push(q.i); q.sm=Math.max(0,sm-cost);
          const k0=k.hp, d=Math.max(3,Math.round(npDmg(qh,H_BY[k.hero],false,false,npcParams(q).p)*CXB.np)); k.hp=Math.max(0,k.hp-d);
          if(BX_AOE.test(artOf(qh).k||'')) for(const g of bxGuards()) gHit(g,(k0-k.hp)*m*.5,q); continue; } }
      const act=Math.max(.3,Math.min(.85,.5+(npcPower(q,false,1)-CXB.ref)*.01))*(.5+.5*q.hp/100);
      if(ch(act)){ const l=xLost();
        if(l>=6&&ch(Math.min(.9,cxTacP(q,1)))){ const a=Math.round(l*(.35+rnd()*.2)); x.hp=clamp(x.hp+a); q.hp=clamp(q.hp-Math.round(a*1.2)); }
        else if(ch(.25)) K.bxCh={r:r+1,v:-ri(6,10)};
        else { const PP=npcParams(q).p, EP=npcParams(k).p; if(!ch(dodgeP(EP[1],PP[1]))){ const d=Math.max(2,Math.round((4+ri(0,5))*CXB.ad*(.6+.4*q.hp/100))); const g=bxGuards().length&&ch(.4)?weakG():null; if(g) gHit(g,d*m,q); else k.hp=Math.max(0,k.hp-d); } } }
      if(q.hp<=0){ C.out.push(q.i); continue; }
      if(!final&&q.hp<25&&ch(cxTacP(q,2))) C.out.push(q.i); } }
  // ---- 유닛이 쓰러질 때 ----
  function bxUnitDown(u,by){ const w=W(), c=BXW();
    if(u.cx==='boss'){ if(!u.phase2){ u.phase2=true; u._phase=1; const inB=w.battle&&w.battle.e===u; log('키아라의 몸이 한 번 녹아내렸다가, 웃음소리와 함께 다시 빚어졌다. 단독현현.','war',inB?{fx:{t:'bossp2',line:'아아, 이 아픔마저 이토록 달콤하다니요.'}}:undefined); u.hp=BXK.hp2; if(inB) log('키아라: “아아, 이 아픔마저 이토록 달콤하다니요.”','enemy'); return false; }
      u.alive=false; u.hp=0; c.bossDown=by==='me'?'me':by&&by.i?by.i:'npc'; if(by==='me'){ c.bossComp=w.battle&&w.battle.e===u?((w.battle.ctx||{}).comp||[]).length:0; if(!c.bossComp) c.soloBoss=1; }
      log('키아라는 끝까지 웃고 있었다. “이것도 하나의 쾌락이었습니다.” 그 몸이 단꿈처럼 녹아 사라졌다.','war'); if(!w.battle) w.queue.unshift(()=>checkEnd()); return true; }
    u.alive=false; u.hp=0;
    if(u.cx==='bb'){ return true; }
    if(u.cx==='sent'){ const k=c.kp.find(k=>k.at==='s'+u.i); const nm=H_BY[u.hero].name;
      if(k){ k.at='got'; c.kpGot=(c.kpGot||0)+1; if(by==='me') c.kpMe=(c.kpMe||0)+1; }
      if(u.guard) log(`센티넬 ${nm}${J(nm,이)} 무릎을 꿇었다. 키아라의 몸이 한 번 크게 일렁였다.`,'war');
      else if(by==='me'||(w.battle&&w.battle.e===u)) log(`${pName(u)}${J(pName(u),이)} 무너졌다. 가슴께에서 빛 한 조각이 빠져나왔다. KP ${k?k.k:''}.`,'war');
      if(by==='me'){ w.seals++; c.shadowKills++; log('다음 날 감독관의 사자가 찾아와 당신 손등에 령주 한 획을 그려 주었다.','seal'); if(k) log((c.kpMe||0)<=1?'익숙하지 않은 단맛이 혀끝에 남았다.':'회수할 때마다, 누군가 이쪽을 보고 있던 시선이 하나씩 끊긴다.','war'); }
      else if(by&&by.i){ by.seals=(by.seals||0)+1; if(c.stage===2) bxLater(1,`어젯밤 ${pick(CX().sites)}에서 서번트 둘이 싸웠다. 한쪽은 아침에 흔적도 없었다.`); }
      if(c.stage===2) bxLater(1,'깊은 잠에 빠졌던 사람 몇이 밤사이 깨어났다고 아침 뉴스가 전했다.');
      if(u.ego){ (c.freed=c.freed||[]).push(u.hero); log(u.hero==='meltryllis'?'멜트릴리스가 가슴께를 짚었다. “…흥. 이제야 숨이 쉬어지네. 그 여자에게 갚을 게 생겼어.”':'패션립이 두 손을 꼭 모았다. “…아, 아파요. 그래도… 이제 제 마음대로 움직일 수 있어요. 같이 갈게요.”','voice'); }
      return true; }
    return true; }

  // ---- 전쟁의 끝 ----
  function bxForceDesc(){ const c=BXW(); if(c.stage<2) bxSeal(); if(c.stage===2){ if(c.noBB){ c.revealHow='none'; bxDescend(); } else { c.revealHow=c.revealHow||'force'; bxReveal(); } } }
  function bxCheckEnd(){ const w=W(), c=BXW(); if(!c||c.done||w.ended||S.dead) return false;
    if(c.bossDown){ if(w.battle||S.pending) return true; bxAfterBoss(); return true; }
    const others=contracted().filter(p=>!p.ally);
    if(w.heroAlive&&!others.length){ if(w.battle||S.pending) return true;
      if(c.stage<3) bxForceDesc();
      const k=bxKiara(); if(k){ if(!c.finalDay){ c.finalDay=Math.min(14,w.day+2); log(`남은 것은 ${CX().grail}의 셋쇼인 키아라뿐이다. 성배가 이틀 안에 넘치려 하고 있다.`,'war'); } return true; }
      return false; }
    if(!w.heroAlive&&others.length<=1){ if(c.stage<3) bxForceDesc(); if(!bxKiara()) return false;
      if(!contracted().length){ c.done=true; w.ended=true; w.queue=[]; bxDream(); } return true; }
    return false; }
  function bxFinalNight(){ const w=W(), k=bxKiara(), c=BXW(); if(!bxOn()) return false; if(!k){ if(c.stage<3){ bxForceDesc(); } if(!bxKiara()) return false; }
    const kk=bxKiara(); w.final=true;
    log(`제${w.day}일 · 마지막 밤`,'night'); log(`자정, 살아 있는 모든 조가 ${CX().grail}${J(CX().grail,으로)} 끌려갔다. 키아라가 두 팔을 벌리고 기다리고 있었다.`,'war');
    const all=contracted(), led=w.heroAlive, rest=()=>{ if(w.ended||S.dead||c.done) return; if(kk.alive&&!led) bxNpcJoint(contracted(),true);
      if(!bxCheckEnd()&&kk.alive){ c.done=true; w.ended=true; w.queue=[]; bxDream(); } };
    if(w.heroAlive){ w.queue.push(()=>battle(kk,{final:true,cx:true,descent:true,cxBoss:true,joint:all.length,comp:all.map(p=>p.i)}),rest); return true; }
    rest(); return true; }
  function bxAfterBoss(){ const w=W(), c=BXW(); c.done=true; w.ended=true; w.queue=[];
    const me=c.bossDown==='me'||w.heroAlive&&(w.cxWent&&w.cxWent.d===w.day);
    log(S.hero==='bb'&&w.heroAlive?`${hero().name}${J(hero().name,이)} 봉인한 성배를 품에 안았다. “이건 제가 가져갈게요. 달은 꽤 멀지만, 금방이에요.”`:'BB가 남은 성배를 품에 안았다. “이건 제가 가져갈게요. 이 도시에 두기엔, 아직 좀 달거든요.”','war');
    log('성배는 달로 갔다. 아무도 소원을 빌지 않았다. 수녀가 머물던 성당은 비어 있었다.','joy');
    S.flags.bxEnd=c.bossDown==='me'?'me':'npc'; if((c.kpGot||0)>=5) S.flags.bxFive=1;
    if(c.bossDown==='me'&&w.heroAlive){ S.flags.war='victor'; mark('war'); S.flags.wishText='BB가 성배를 달로 가져갔다'; S.flags.brokeCup=1; add({will:8,lore:4}); wrec('mine','셋쇼인 키아라를 쓰러뜨렸다'); farewell(); return; }
    const p=pairBy(c.bossDown); if(p){ p.revealed=true; w.winner=p.i; log(`감독관의 통지: 의식 종료. ${pName(p)} 조가 셋쇼인 키아라를 쓰러뜨렸다.`,'notice'); }
    S.flags.bxNpc=1; warOver(); }
  // 키아라가 남았다: 도시는 단꿈에 잠기고, 마스터는 남겨진다 (12-1 · A안)
  function bxDream(){ const w=W(); S.flags.bxDream=1; S.flags.cxFlood=0;
    log(`새벽이 오기 전에 ${cityN()} 전체가 키아라의 쾌락에 녹아들었다. 사람들은 웃는 얼굴로, 깨어나지 않는 단꿈에 잠겼다.`,'loss');
    log('키아라: “이 얼마나 달콤한 구원인지요. …당신은 마지막에 맛보겠습니다.” 키아라는 당신을 남겨 두고 떠났다.','enemy');
    if(w.heroAlive){ log(`${hero().name}${J(hero().name,이)} 손을 뻗었지만, 그 손끝부터 녹아 키아라에게 흘러들었다.`,'loss'); w.heroAlive=false; w.hp=0; w.myOut={d:w.day,tod:w.tod,why:'키아라에게 흡수되었다',by:'boss'}; }
    wrec('mine','그 겨울, 도시는 한 사람의 쾌락이 되었다');
    add({will:-20,health:-10,bond:-8}); if(S.flags.war==='survived') S.flags.war='lost'; warOver(); }
  function bxRep(){ return null; }

  // ---- 전투 ----
  function bxIntro(e,ctx){ const c=BXW(); if(!c) return '';
    if(e.cx==='sent'&&!c.sentSeen){ c.sentSeen=1; bxVoice('sent'); }
    if(e.cx==='sent') return ctx.defend?`${pName(e)}${J(pName(e),이)} 결계 바깥에 서 있었다. 어디선가 본 듯한 서번트였다.`:`${pick(CX().sites)}. ${pName(e)}${J(pName(e),이)} 천천히 돌아보았다. 어디선가 본 듯한 서번트였다.`;
    if(e.cx==='bb') return `${CX().grail} 위, 보이지 않는 상자 앞에 ${pName(e)}${J(pName(e),이)} 걸터앉아 있었다. “어머, 선배. 토벌하러 오셨어요?”`;
    if(e.bx) return `${CX().grail}. 녹아내린 성배를 등지고 셋쇼인 키아라가 미소 짓고 있었다.${bxGuards().length?` 그 곁을 센티넬 ${['','하나가','둘이','셋이','넷이','다섯이'][bxGuards().length]} 지킨다.`:''}`;
    return ''; }
  // 수녀 · 봉인 중의 BB는 쓰러지지 않는다: 30 아래면 물러나고, 한 번에 크게 받아도 1에서 멈춘다. BB전에서는 우리 서번트도 쓰러지지 않는다
  function bxHold(b){ const w=W(), e=b.e, c=BXW(); if(!c) return false;
    if(e.bxNun&&!e.bxFake&&e.hp<BXK.nunKeep){ e.hp=Math.max(1,e.hp); log(`${e.mname}${J(e.mname,이)} 웃으며 손을 들었다. “오늘은 여기까지 하지요.” 서번트가 수녀를 안고 물러났다.`,'enemy'); b.res='fled'; return true; }
    const isBB=e.cx==='bb'||e.bxBB&&bxSealing();
    if(isBB&&(e.hp<BXK.bbKeep||w.hp<=0)){ e.hp=Math.max(1,e.hp); if(w.hp<=0){ w.hp=1; log(`BB가 손가락을 튕겼다. 쓰러지려던 ${hero().name}의 몸이 고쳐 쓰인 것처럼 멈췄다. “이 싸움에서 누가 사라지면 곤란하거든요.”`,'enemy'); b.res='draw'; return true; }
      log('BB의 윤곽이 크게 흔들렸다. 도시 한가운데의 상자에 금이 가는 소리가 났다.','war'); b.res='win'; bxBBBroken('me'); return true; }
    if(isBB&&ch(.2)&&!b.bxSaid){ b.bxSaid=1; log(pick(['BB: “…아, 됐어요. 어차피 말 못 하니까.”','BB: “저랑 놀 시간에, 밤거리를 걷는 쪽부터 정리하는 게 좋을 텐데요.”']),'enemy'); }
    return false; }
  // 키아라전의 합마다: 호위 · 풀려난 멜트릴리스와 패션립
  function bxRound(b,hp0){ const w=W(), e=b.e, c=BXW(); if(!c||!e||!e.bx||!e.alive||!w.heroAlive) return;
    const k0=b.bxK0!=null?b.bxK0:e.hp, lost=Math.max(0,k0-e.hp), m=bxMult(false); let cov=false;
    // 네가 세이버: 마력 A 이하 상대를 합마다 15%로 매료한다
    if(PV(myParams().p[3])<=5&&ch(.15)){ b.bxCharm=b.round+1; log(`키아라가 손을 내밀었다. ${hero().name}의 손끝이 한순간 그쪽으로 끌려갔다. 매료.`,'war'); }
    for(const g of bxGuards()){ if(!ch(BXK.gAct*Math.max(.2,g.hp/100))) continue; const gN=pName(g), r=rnd();
      if(r<BXK.gCover){ if(lost>0&&lost>=BXK.gMinMe&&!cov){ cov=true; const a=Math.round(lost*(.4+rnd()*.2)); e.hp=Math.min(100,e.hp+a); g.hp=clamp(g.hp-Math.round(a*Math.min(m,BXK.gCap))); log(`${gN}${J(gN,이)} 키아라 앞을 막아서 일격을 대신 받았다.`,'war'); if(g.hp<=0) bxUnitDown(g,'me'); } }
      else if(r<BXK.gCover+BXK.gChip){ b.bxChip={r:b.round+1,v:ri(3,6)}; log(`${gN}${J(gN,이)} 옆에서 ${hero().name}의 발을 묶었다.`,'war'); }
      else { const d=Math.max(1,Math.round((4+ri(0,5))*.6)); w.hp=clamp(w.hp-d); log(`${gN}${J(gN,이)} 키아라와 함께 ${hero().name}${J(hero().name,을)} 쳤다.`,'war'); } }
    for(const id of (c.freed||[])){ const nm=H_BY[id].name; c.egoNP=c.egoNP||{};
      if(!c.egoNP[id]&&(e.hp<=40||b.round>=2)&&ch(.25)){ c.egoNP[id]=1; const d=ri(14,22); e.hp=Math.max(0,e.hp-d); log(id==='meltryllis'?`보구 해방 — 멜트릴리스의 「사라스바티 멜트아웃」. 키아라의 몸이 단숨에 녹아내렸다.`:`보구 해방 — 패션립의 「브륀힐드 로만시아」. 키아라가 거대한 손톱 사이에 끼었다.`,'allynp'); continue; }
      if(ch(.45)){ const gs=bxGuards(); if(gs.length&&ch(.4)){ const g=gs.sort((a,b)=>a.hp-b.hp)[0]; g.hp=clamp(g.hp-ri(5,10)); log(`${nm}${J(nm,이)} ${pName(g)}에게 달려들었다.`,'war'); if(g.hp<=0) bxUnitDown(g,'me'); }
        else { e.hp=Math.max(0,e.hp-ri(4,9)); log(`${nm}${J(nm,이)} 옆에서 키아라에게 일격을 보탰다.`,'war'); } } } }
  // 키아라의 힘: 플레이어 결전 · NPC 결전
  function bxPow(p,bt){ const c=BXW(), w=W(), b=w.battle; if(!c) return 0;
    if(bt){ let v=BXK.desc+(c.bbAlly?BXK.bbAdj:0)-5*bxFreed()+BXK.relAdj*bxFreed(); if(b){ if(b.bxChip&&b.bxChip.r===b.round) v+=b.bxChip.v; if(b.bxCharm===b.round) v+=10; if(b.bxMan) v+=5; } return v; }
    return BXK.nd; }
  function bxBattleStart(e,ctx){ const w=W(), c=BXW(); if(!c||!e||!e.bx) return; const b=w.battle; if(!b||b.bxMS) return; b.bxMS=1;
    if(!chk('정신',S.st.will+ri(0,40),55)){ add({will:-3}); b.bxMan=1; log('만색유체. 키아라의 목소리가 머릿속까지 스며들었다. 생각이 자꾸 단 쪽으로 미끄러진다.','war'); } }
  // 센티넬의 능력치: 원래 서번트 위에 KP 한 단계 · 키아라: 남은 KP 둘마다 가장 낮은 능력치 한 단계
  function bxSentStats(p,o){ const i=KP_STAT[p.kp]; return i==null?o:o.map((r,j)=>j===i?rankShift(r,1):r); }
  function bxKiaraStats(o){ o=o.slice(); const n=Math.floor(Math.min(5,bxKpLeft())/2); for(let t=0;t<n;t++){ let bi=-1,bv=99; o.forEach((r,i)=>{ if(r==='-'||r==='EX') return; const v=PV(r); if(v<bv){ bv=v; bi=i; } }); if(bi<0) break; o[bi]=rankShift(o[bi],1); } return o; }
  // 키아라 보구: 쓸 때마다 체력 +15
  function bxNpHeal(u){ if(u&&u.bx&&u.alive){ u.hp=Math.min(u.phase2?BXK.hp2:100,u.hp+BXK.npHeal); } }

  // ---- 서번트별 반응 (13장) ----
  function bxVoice(k){ const w=W(); if(!w.heroAlive) return; const h=hero(), c=BXW();
    const L={bb:{desc:'“…나왔네요, 그 사람. 선배, 이제부터는 숨김없이 갈게요.”'},
      meltryllis:{desc:'“저 여자… 처음 봤을 때부터 피부가 따끔거렸어. 역시 그런 거였구나.”',sent:'“…저 아이들, 나랑 같은 냄새가 나. 싫은 냄새.”'},
      passionlip:{desc:'“무, 무서워요… 그래도, 저 사람만은 놔두면 안 될 것 같아요.”',sent:'“저기… 저 아이들, 아파 보여요.”'},
      kama:{desc:'“역시. 어쩐지 마음에 안 들더라니.”'}};
    const t=(L[h.id]||{})[k]; if(t) log(`${h.name}: ${t}`,'voice'); }

  // ---- 1~3일차: 수녀 조는 밤마다 사냥을 나간다 (두 조를 쓰러뜨리면 멈춘다) ----
  function bxNunHunt(avail,done){ const w=W(), c=BXW(); if(!c||c.stage>=2||w.day>3||c.nunKills>=2) return; const n=bxNunP(); if(!n||!n.alive||n.halt>0) return;
    const ts=avail.filter(x=>x!==n&&!done.has(x)&&x.alive&&x.master); if(!ts.length) return; const t=pick(ts); done.add(n); done.add(t); n.nAct='out';
    n.bxHunt=1; const {win,lose}=npcFight(n,t,false,true); n.bxHunt=0; w.nf.push([n.i,t.i]);
    if(t.hp<=0&&t.alive){ const lh=H_BY[t.hero]; if(lh.sp==='revive'&&!t.usedRevive){ t.usedRevive=true; t.hp=45; return; }
      t.alive=false; t.revealed=true; pairOut(t,'다른 조에게 쓰러졌다'); log(`감독관의 통지: ${cn(t)} 조 탈락.`,'notice'); if(t.ally){ log(`동맹 ${t.mname}의 조가 무너졌다.`,'loss'); S.flags.allyName=t.mname; } c.nunKills++; }
    n.hp=Math.max(n.hp,40); }
  // 수녀 조의 정보가 70에 닿으면 이름이 드러난다(직접 캐낸 보상)
  function bxIntelCheck(t){ const c=BXW(); if(!c||c.nunKnown||!t||!t.bxNun) return; if((t.intel||0)>=70){ c.nunKnown=1; t.mname='키아라 킷쇼인'; log('기록을 맞춰 보다가 수녀의 이름을 찾아냈다. 키아라 킷쇼인. 매장기관의 수녀다. …왜인지 그 이름이 자꾸 혀끝에 걸렸다.','war'); } }

  // ---- 기존 갈래에 비스트를 단다 ----
  CRISIS.list.push({id:'beast',w:1,wAv:1});
  { const f0=crisisRoll; crisisRoll=(h,pairs)=>{ const f=typeof globalThis!=='undefined'?globalThis.__FORCE_CRISIS:undefined; let c=f0(h,pairs); if(!c) return c;
      if(f==='beast'||f==='black') c.type=f; return c.type==='beast'?bxSetup(c,pairs):c; }; }
  { const f0=crisisDay; crisisDay=()=>BXW()?bxDay():f0(); }
  { const f0=crisisNight; crisisNight=()=>BXW()?bxNight():f0(); }
  { const f0=cxNightActs; cxNightActs=ch_=>{ if(BXW()){ const c=BXW(); if(c.stage<3) return bxNightActs(ch_); const k=bxKiara(); if(!k||!W().heroAlive) return; const w=W(), pc=cxNightComp(), pact=w.cxPact&&w.cxPact.d===w.day&&pc.some(p=>p.i===w.cxPact.i);
      ch_.unshift({t:'키아라에게 간다',d:`${CX().grail}의 셋쇼인 키아라와 결판을 낸다${pc.length?` · 오늘 밤 함께 가는 조 ${pc.map(p=>pName(p)).join(', ')}`:' · 오늘 밤 함께 가는 조는 없다'}${pact?' · 약속한 밤이다':''}${bxGuards().length?` · 호위 ${bxGuards().length}`:''}`,auto:pact||w.hp>=55&&w.sm>=40,f:()=>{ w.trust=clamp(w.trust+traitR({충성:1,연민:2,명예:3,야망:-1,자유:1},{선:2})); w.queue.push(()=>cxBossGo(pc)); }}); if(ch_[0].auto) ch_.slice(1).forEach(x=>x.auto=false); return; } return f0(ch_); }; }
  { const f0=cxDayActs; cxDayActs=ch_=>BXW()?bxDayActs(ch_):f0(ch_); }
  { const f0=cxCheckEnd; cxCheckEnd=()=>BXW()?bxCheckEnd():f0(); }
  { const f0=cxFinalNight; cxFinalNight=()=>BXW()?bxFinalNight():f0(); }
  { const f0=cxZoneBattle; cxZoneBattle=ctx=>BXW()?null:f0(ctx); }
  { const f0=cxUnitDown; cxUnitDown=(u,by)=>BXW()?bxUnitDown(u,by):f0(u,by); }
  { const f0=cxRep; cxRep=()=>BXW()?bxRep():f0(); }
  { const f0=cxThreat; cxThreat=()=>{ if(!BXW()) return f0(); const w=W(); if(!w.cxHit) return false; const u=cxUnit(w.cxHit); w.cxHit=null; if(!u||!u.alive||!w.heroAlive) return false;
      log(`결계 바깥에서 낯선 기척이 났다. ${pName(u)}${J(pName(u),이)} 이쪽을 찾아왔다.`,'war'); battle(u,{defend:true,cx:true}); return true; }; }
  { const f0=cxNpcVs; cxNpcVs=(p,u,withMe)=>{ if(BXW()&&u&&u.bx){ bxNpcVsKiara(p,W().final,[],[]); if(withMe&&u.alive&&p.alive) log(`${pName(p)}${J(pName(p),이)} 키아라를 한 차례 몰아붙였다.`,'war'); return; } return f0(p,u,withMe); }; }
  { const f0=cxCompRound; cxCompRound=(b,hp0)=>{ f0(b,hp0); if(b&&b.e&&b.e.bx) bxRound(b,hp0); }; }
  { const f0=battleRound; battleRound=()=>{ const b=W()&&W().battle; if(b&&b.e&&b.e.bx){ b.bxK0=b.e.hp; bxBattleStart(b.e,b.ctx); } return f0(); }; }
  { const f0=npcDuel; npcDuel=(a,b,f,i)=>{ const keep=BX_VS; if(!BX_VS) BX_VS=[a,b]; try{ return f0(a,b,f,i); } finally{ BX_VS=keep; } }; }
  { const f0=npcFire; npcFire=(b,r)=>{ const v=f0(b,r); if(b&&b.e&&b.e.bx) bxNpHeal(b.e); return v; }; }
  { const f0=masterKilled; masterKilled=e=>{ if(e&&e.bxNun){ log('수녀의 몸은 매장기관의 것이었다. 치명상이어야 할 상처가 눈앞에서 닫혔다.','war'); e.mHurt=1; return; } return f0(e); }; }
  { const f0=addIntel; addIntel=(t,g,why)=>{ const r=f0(t,g,why); bxIntelCheck(t); return r; }; }
  { const f0=pairOut; pairOut=(p,why,by,quiet)=>{ const had=!!(p&&p.out); f0(p,why,by,quiet); const c=BXW(); if(!had&&c&&!c.done&&c.stage>=2&&p&&!p.bxFake&&!p.bxSentUsed&&p.hero!=='bb') bxFallen(p.hero,{src:p}); }; }
  { const f0=myHeroDown; myHeroDown=e=>{ const r=f0(e); const c=BXW(), w=W(); if(c&&!c.done&&c.stage>=2&&!w.heroAlive&&!c.meFell&&S.hero!=='bb'){ c.meFell=1; bxFallen(S.hero,{mine:true}); } return r; }; }
