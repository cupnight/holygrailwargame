// 비스트 위기 요약 시험: node dev/bxsim.js <game.html> N '{"hero":"id","seed":1,"show":0}'
const fs=require('fs'),vm=require('vm');const file=process.argv[2],N=+(process.argv[3]||50),opt=JSON.parse(process.argv[4]||'{}');
const src=fs.readFileSync(file,'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;ctx.__FORCE_CRISIS='beast';if(opt.bxk)ctx.__BXK=opt.bxk;if(opt.hero)ctx.__FORCE_HERO=opt.hero;vm.createContext(ctx);
vm.runInContext(src.slice(a,b)+';globalThis.Sim=Sim;',ctx);const Sim=ctx.Sim;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
const T={},cnt=(k,v)=>{T[k]=T[k]||{};T[k][v]=(T[k][v]||0)+1;};let err=0,errs=[];const sum={};const add=(k,v)=>{sum[k]=(sum[k]||0)+v;};
for(let n=0;n<N;n++){ const seed=(opt.seed||1)*1000+n; try{ Sim.newLife({seed,len:20});Sim.start();let g=0;
  while(Sim.S&&!Sim.S.dead&&g++<400000){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);if(S.phase!=='war'&&S.war&&S.war.ended&&!opt.full)break;}
  const S=Sim.S,w=S.war,c=w&&w.crisis; if(!c){cnt('none','x');continue;}
  cnt('bb',c.bb?c.bb.at:'pre7'); cnt('how',c.revealHow||'-'); cnt('stage',c.stage); cnt('nunKills',c.nunKills);
  cnt('end',S.flags.bxEnd?'kiara down by '+S.flags.bxEnd:S.flags.bxDream?'dream':c.done?'done?':'open');
  cnt('kpGot',c.kpGot||0); cnt('kpMe',c.kpMe||0); cnt('meAlive@end',w.heroAlive?1:0);
  if(c.descD) add('descD',c.descD),add('nDesc',1); if(c.revealD) add('revD',c.revealD),add('nRev',1);
  cnt('guardsDead',(c.units||[]).filter(u=>u.cx==='sent'&&u.guard&&!u.alive).length); cnt('guards@desc',(c.units||[]).filter(u=>u.cx==='sent'&&u.guard).length);
  if(opt.show&&n<opt.show) console.log(S.log.filter(e=>/키아라|센티넬|BB|수녀|봉인|토벌령|KP/.test(e.t)).map(e=>`[${e.k}] ${e.t}`).slice(0,80).join('\n'),'\n-----');
 }catch(e){err++;if(errs.length<5)errs.push(seed+': '+String(e.stack||e).split('\n').slice(0,5).join(' | '));}}
console.log(JSON.stringify({N,err,descD:(sum.descD/sum.nDesc).toFixed(1),revD:(sum.revD/sum.nRev).toFixed(1)}));for(const k in T)console.log(k,JSON.stringify(T[k]));errs.forEach(x=>console.log(x));
