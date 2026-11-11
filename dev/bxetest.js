// 키아라 패배 뒤 에필로그 시험: node dev/bxetest.js <game.html> [lang] [N]
// 1) 사건 하나하나를 직접 불러 모든 선택지를 고른다  2) 단꿈 생 N개를 에필로그 끝까지 돌려 사건 분포를 센다
const fs=require('fs'),vm=require('vm');const file=process.argv[2],lang=process.argv[3]||'ko',N=+(process.argv[4]||200);
const src=fs.readFileSync(file,'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
const code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__E={EPI_POOL,ARC,S:()=>S,die,epiTick};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim,E=ctx.__E;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
const toEpi=(seed)=>{ Sim.newLife({seed,len:20});Sim.start();let g=0; while(Sim.S&&!Sim.S.dead&&g++<400000){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;} if(S.phase==='epi'&&S.hero)break; Sim.tick(1);} return Sim.S; };
let S=null; for(let s=1;s<400&&!(S&&S.phase==='epi'&&S.hero&&!S.dead);s++) S=toEpi(5000+s);
console.log('hero',S.hero,'age',S.age,'kids',(S.fam&&S.fam.kids||[]).map(k=>k.age).join(','),'spouse',!!(S.fam&&S.fam.spouse&&S.fam.spouse.alive));
const snap=JSON.stringify(S);
const ids=E.EPI_POOL.filter(x=>/^bx_|^arc_dream/.test(x.id)).map(x=>x.id);
let errs=0;
const reset=()=>{ const o=JSON.parse(snap); for(const k of Object.keys(S)) delete S[k]; Object.assign(S,o); S.flags.bxDream=1; S.warYear=S.year-9; S.epi.used=[]; S.pending=null; };
for(const id of ids){ const x=E.EPI_POOL.find(e=>e.id===id);
  for(let ci=0;ci<4;ci++){ reset();
    if(id==='bx_sw2') S.flags.bxSwN=1, S.flags.bxSwY=S.year-5, S.flags.bxDeep=ci%2;
    if(id==='bx_sw3') S.flags.bxSwN=2, S.flags.bxSwY=S.year-5, S.flags.bxLight=ci%2;
    if(id==='bx_sw1') S.flags.bxSwN=0;
    if(id==='bx_mimic') S.flags.bxSwN=1, S.war.trust=80;
    if(id==='bx_last') S.age=75;
    if(id==='bx_far'&&ci===1) S.flags.bxTold=S.year;
    if(id==='bx_kids'){ S.fam=S.fam||{}; S.fam.kids=[{name:'하루',age:8}]; }
    if(id==='bx_family'){ S.fam=S.fam||{}; S.fam.mother={alive:true}; }
    if(id==='bx_allyl'&&!E.S().flags) {}
    let ok; try{ ok=x.c(); }catch(e){ console.log(id,'c ERR',e.message); errs++; break; }
    if(!ok){ if(ci===0) console.log(id,'(조건 안 맞음)'); break; }
    const L0=S.log.length;
    try{ x.f(); let step=0;
      while(step++<6){ const P=S.pending; if(!P) break; const cs=P.choices.filter(c=>!c.off); if(ci>=cs.length){ ci=9; break; } if(ci===0||step>1) {} Sim.resolve(P.choices.indexOf(cs[Math.min(ci,cs.length-1)]));
        if(S.epi.arc&&id==='arc_dream'){ const a=S.epi.arc; E.ARC[a.id][a.st](); } }
    }catch(e){ console.log(id,ci,'ERR',e.stack.split('\n').slice(0,3).join(' | ')); errs++; }
    if(ci===9) break;
    const out=S.log.slice(L0).map(e=>e.t).filter(Boolean);
    console.log(`— ${id}[${ci}]`, out.join(' / ').slice(0,lang==='ko'?400:600), JSON.stringify({sw:S.flags.bxSwN,deep:S.flags.bxDeep,light:S.flags.bxLight,free:S.flags.bxFree,last:S.flags.bxLast}));
  }
}
// 죽음 줄
for(const k of ['follow','awake','free']){ reset(); if(k==='free') S.flags.bxFree=1; else S.flags.bxLast=k; const L0=S.log.length; try{ E.die('노환'); }catch(e){ console.log('die ERR',e.message); errs++; } console.log('die',k,S.log.slice(L0,L0+2).map(e=>e.t).join(' / ')); }
// 분포
const cnt={}; let lives=0,bxN=[];
for(let n=0;n<N;n++){ const S2=toEpi(7000+n); if(!S2||S2.phase!=='epi'||S2.dead) continue; S2.flags.bxDream=1; S2.warYear=S2.year; lives++;
  let g=0; try{ while(!S2.dead&&g++<200000){ if(S2.pending){Sim.resolve(Sim.autoChoice(S2.pending));continue;} Sim.tick(1);} }catch(e){ errs++; console.log('life ERR',(S2.epi.used||[]).slice(-2),S2.fam&&JSON.stringify(S2.fam).slice(0,300),e.stack.split('\n').slice(0,3).join(' | ')); }
  const u=(S2.epi.used||[]).filter(x=>/^bx_|^arc_dream/.test(x)); bxN.push(u.length); u.forEach(x=>cnt[x]=(cnt[x]||0)+1); }
console.log('lives',lives,'bx per life avg',(bxN.reduce((a,b)=>a+b,0)/Math.max(1,lives)).toFixed(2),'max',Math.max(...bxN),JSON.stringify(cnt),'errs',errs);
