// 에필로그 구간 한가운데에서 저장 → 불러오기 해도 같은 생이 이어지는지. 사용: node ep2save.js [생 수]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const N=+process.argv[2]||10;
let s=fs.readFileSync('build/game.html','utf8');s=s.replace('  function finalYears(){\n','  globalThis.__stayGo=()=>grantStay(undefined); globalThis.__rel=()=>relOf();\n  function finalYears(){\n');fs.writeFileSync('build/_t.html',s);
const b=await chromium.launch();const p=await b.newPage();await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.addInitScript(()=>{globalThis.__FORCE_CRISIS=false});
await p.goto('file://'+process.cwd()+'/build/_t.html');await p.waitForFunction(()=>typeof Sim==='object'&&Sim.HEROES);
const out=await p.evaluate(N=>{const res=[];let n=0;
 const toWar=seed=>{Sim.newLife({seed,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&!(Sim.S.war&&Sim.S.war.pairs&&Sim.S.war.heroAlive&&Sim.S.war.day>=2)&&g++<200000){const S=Sim.S;if(S.pending)Sim.resolve(Sim.autoChoice(S.pending));else Sim.tick(1);}const S=Sim.S;if(!S||S.dead||!S.war||!S.war.heroAlive||!__rel())return false;S.war.trust=80;S.pending=null;S.war.queue=[];S.war.cupPure=true;__stayGo();return true;};
 for(let t=0;t<N*6&&n<N;t++){const seed=7300+t;if(!toWar(seed))continue;n++;let q=0;const seen={};const o={seed,ev:[]};
  try{while(!Sim.S.dead&&q++<8000){const E=Sim.S.epi||{};if(E.ph==='D'&&(o.dn=(o.dn||0)+1)>60)break;const P=Sim.S.pending;
   if(P){ if(E.ph&&!seen[P.title]&&(o.pn=(o.pn||0)+1)%2===0){seen[P.title]=1;const k0=E.k,t0=P.title,w0=JSON.stringify(Sim.ep2When()),L0=Sim.S.log.length,tr0=Sim.S.war.trust;const sv=Sim.snapshot();
      if(!sv){o.ev.push(E.ph+' snapshot null');}else{Sim.load(JSON.parse(JSON.stringify(sv)));const E1=Sim.S.epi;const k1=E1.k,L1=Sim.S.log.length;let g=0;while(!Sim.S.pending&&!Sim.S.dead&&g++<50)Sim.tick(1);const P1=Sim.S.pending;
       const same=P1&&P1.title===t0&&g<=1&&k1===k0&&L1===L0;o.tot=(o.tot||0)+1;if(same){o.ok=(o.ok||0)+1}else o.ev.push(`${E.ph} k ${k0}→${k1}→${Sim.S.epi.k} when ${w0}→${JSON.stringify(Sim.ep2When())} log ${L0}→${L1} trust ${tr0}→${Sim.S.war.trust} | ${t0} → ${P1?P1.title:'(없음)'} ticks ${g}`);}
      continue;}
     Sim.resolve(Sim.autoChoice(P));}else Sim.tick(1);}}catch(e){o.err=String(e&&e.stack||e).slice(0,300);}
  res.push(o);}
 return res;},N);
out.forEach(r=>{console.log(r.seed,'다시 뜸',r.ok||0,'/',r.tot||0,r.err||'');r.ev.forEach(x=>console.log('  ',x))});console.log('page errors',errs.length,errs.slice(0,2));
fs.unlinkSync('build/_t.html');await b.close()})()
