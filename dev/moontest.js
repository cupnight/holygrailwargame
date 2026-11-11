// BB · 멜트 · 립 소환 길 시험: node dev/moontest.js <game.html> [N] [vow 0/1]
const fs=require('fs'),vm=require('vm');const file=process.argv[2],N=+(process.argv[3]||20000),vow=+(process.argv[4]||0),send=+(process.argv[5]||0);
const src=fs.readFileSync(file,'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
const code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__M={doSummon,S:()=>S,dayStart};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);const Sim=ctx.Sim,M=ctx.__M;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
const c={full:0,me:{},npc:{},hij:0,n9:0,err:0};let ex=null;
for(let n=0;n<N;n++){ try{ Sim.newLife({seed:300000+n,len:20,moon:!!vow,send:!!send}); const S=M.S(); M.doSummon(null); const w=S.war;
  if(w.fullMoon) c.full++; if(S.flags.bbHijack){ c.hij++; if(!ex) ex=S.log.slice(-3).map(e=>e.t).join(' / '); }
  if(['bb','meltryllis','passionlip'].includes(S.hero)) c.me[S.hero]=(c.me[S.hero]||0)+1;
  for(const p of w.pairs) if(['bb','meltryllis','passionlip'].includes(p.hero)){ const k=p.hero+(w.fullMoon?'@full':'')+(S.hero==='bb'?'@meBB':''); c.npc[k]=(c.npc[k]||0)+1; }
  if(w.pairs.length>7) c.n9++;
 }catch(e){ c.err++; if(c.err<3) console.log(e.stack.split('\n').slice(0,3).join(' | ')); } }
console.log(JSON.stringify(c)); console.log(ex);
// 내 BB 전쟁에서 조각이 끼어드는 비율
let ego=0,tot=0,log1=null;
for(let n=0;n<Math.min(N,600);n++){ Sim.newLife({seed:500000+n,len:20}); const S=M.S(); ctx.__FORCE_HERO='bb'; M.doSummon(null); ctx.__FORCE_HERO=null; const w=S.war; if(w.crisis&&w.crisis.type==='beast3R') continue; if(w.pairs.some(p=>['meltryllis','passionlip'].includes(p.hero))) continue; tot++;
  const L0=S.log.length; for(let d=0;d<10;d++){ try{ M.dayStart(); }catch(e){ console.log('day ERR',e.message); break; } }
  if(w.pairs.some(p=>p.joinDay&&['meltryllis','passionlip'].includes(p.hero))){ ego++; if(!log1) log1=S.log.slice(L0).filter(e=>/조각|떠돌|끼어들|지나던|한숨/.test(e.t)).map(e=>e.t).join(' / '); } }
console.log('egoJoin',ego,'/',tot, log1);
