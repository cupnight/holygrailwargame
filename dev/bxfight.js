// 키아라 혼자 결전 승률: node dev/bxfight.js <game.html> N '{"left":[0,1,2,3],"karma":1,"days":3,"guards":0}'
const fs=require('fs'),vm=require('vm');const file=process.argv[2],N=+(process.argv[3]||100),opt=JSON.parse(process.argv[4]||'{}');
const src=fs.readFileSync(file,'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
const code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__B={bxSeal,bxReveal,BXW,bxKiara,battle,cxUnits,W:()=>S.war};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;ctx.__FORCE_CRISIS='beast';if(opt.bxk)ctx.__BXK=opt.bxk;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim,B=ctx.__B;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
for(const L of (opt.left||[0,1,2,3])){ let win=0,tot=0;
 for(let n=0;n<N;n++){ Sim.newLife({seed:91000+n*7,len:20});Sim.start();let g=0;
  while(Sim.S&&!Sim.S.dead&&g++<400000){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}if(S.phase==='war'&&S.war.heroAlive&&S.war.day>=1&&S.war.tod==='낮')break;Sim.tick(1);}
  const S=Sim.S,w=S.war;if(!w||!w.heroAlive||S.hero==='bb')continue; S.pending=null; w.queue=[];
  w.day=10; const keepP=opt.npc?w.pairs.filter(p=>!p.bxNun&&p.hero!=='bb').slice(0,2):[]; for(const p of w.pairs){ if(keepP.includes(p)){ p.hp=90; p.sm=100; continue; } p.alive=false; p.out={d:1}; } const c=B.BXW(); if(!c) continue; c.stage=1;
  B.bxSeal(); if(c.bb.at==='none') continue;
  // KP: 남은 L개는 키아라 쪽(호위 guards개는 센티넬로, 나머지는 몸에), 나머지는 거둔 것
  const sents=B.cxUnits().filter(u=>u.cx==='sent'); let keep=0;
  for(const k of c.kp){ const isS=/^s/.test(k.at); if(keep<L){ keep++; if(isS){ const u=sents.find(u=>'s'+u.i===k.at); if(keep>(opt.guards??0)){ u.alive=false; k.at='kiara'; } } else k.at='kiara'; } else { if(isS){ const u=sents.find(u=>'s'+u.i===k.at); u.alive=false; } k.at='got'; } }
  c.kpGot=5-L; c.sealD=w.day-(opt.days??3); c.revealHow=opt.karma?'sent':'force'; c.freed=[];
  B.bxReveal(); const k=B.bxKiara(); if(!k) continue; w.hp=100; w.sm=100; w.trust=70; w.seals=opt.seals??1; S.pending=null; w.queue=[];
  if(opt.npc){ w.heroAlive=false; w.hp=0; w.out=true; for(const p of keepP){ p.cxKnow=true; p.cxStance='break'; } }
  if(opt.war||opt.npc){ w.queue=[]; g=0; while(g++<200000&&!w.ended&&!S.dead){ if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;} Sim.tick(1); } tot++; if(opt.npc?(c.bossDown&&c.bossDown!=='me'):c.bossDown==='me') win++; if(opt.logs&&c.bossDown!=='me'&&!opt._shown){ opt._shown=1; console.log(S.log.slice(-90).map(e=>`[${e.k}] ${e.t}`).join('\n')); } if(opt.dbg&&n<opt.dbg) console.log(L,'tries',c.tries,'win',c.bossDown,'k',Math.round(k.hp),k.phase2,'me',w.heroAlive,w.myOut&&w.myOut.why,'day',w.day,'bt',JSON.stringify(w.bt)); continue; }
  B.battle(k,{final:true,cx:true,descent:true,cxBoss:true,joint:0,comp:[]}); g=0;
  while(g++<20000&&(w.battle||S.pending)){ if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;} Sim.tick(1); if(!w.battle&&!S.pending)break; }
  tot++; if(!k.alive) win++; }
 console.log(`left ${L} karma ${opt.karma?1:0} guards ${opt.guards||0}: ${win}/${tot} = ${(100*win/tot).toFixed(0)}%`); }
