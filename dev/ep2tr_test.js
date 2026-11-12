// 에필로그 문장이 번역되는지: 수육 생을 돌려 기록과 사건 문장을 tr()에 넣어 본다. 사용: node ep2tr_test.js [en|ja] [생 수]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const lang=process.argv[2]||'en',N=+process.argv[3]||12;
let s=fs.readFileSync('build/game.html','utf8');s=s.replace('  function finalYears(){\n','  globalThis.__stayGo=()=>grantStay(undefined); globalThis.__rel=()=>relOf();\n  function finalYears(){\n').replace('const _trc=new Map();','globalThis.__tr=s=>tr(s);\nconst _trc=new Map();');fs.writeFileSync('build/_t.html',s);
const b=await chromium.launch();const p=await b.newPage();await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(l=>{globalThis.__FORCE_CRISIS=false;try{localStorage.setItem('cupnight.lang',JSON.stringify(l))}catch(e){}},lang);
await p.goto('file://'+process.cwd()+'/build/_t.html');await p.waitForFunction(()=>typeof Sim==='object'&&Sim.HEROES);
const out=await p.evaluate(N=>{const bad={},H=/[가-힣]/;let tot=0,n=0;for(let t=0;t<N*5&&n<N;t++){Sim.newLife({seed:5100+t,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&!(Sim.S.war&&Sim.S.war.pairs&&Sim.S.war.heroAlive&&Sim.S.war.day>=2)&&g++<200000){const S=Sim.S;if(S.pending)Sim.resolve(Sim.autoChoice(S.pending));else Sim.tick(1);}
 const S=Sim.S;if(!S||S.dead||!S.war||!S.war.heroAlive||!__rel())continue;n++;S.war.trust=80;S.pending=null;S.war.queue=[];S.war.cupPure=true;const t0=S.log.length;__stayGo();let q=0;
 const chk=(x,w)=>{if(!x||!H.test(x))return;tot++;const r=__tr(x);if(H.test(r))bad[x]=w;};
 while(!Sim.S.dead&&q++<6000){const P=Sim.S.pending;if(P){const ph=(Sim.S.epi||{}).ph;if(ph&&ph!=='D'){chk(P.title,'title');(P.body||'').replace(/\uE000\w\uE001[^\uE001]*\uE001([^\uE001]*)\uE001([^\uE002]*)\uE002/g,'\n$1\n$2\n').split('\n').forEach(l=>chk(l.trim(),'body'));P.choices.forEach(c=>chk(c.t,'choice'));}Sim.resolve(Sim.autoChoice(P));}else Sim.tick(1);if(Sim.S.epi&&Sim.S.epi.ph==='D')break;}
 Sim.S.log.slice(t0).forEach(x=>{if(x.k==='n'||x.k==='night'||x.k==='ev'||x.k==='sys')chk(x.t,x.k)});}
 return {tot,bad};},N);
const B=Object.entries(out.bad);console.log(lang,'checked',out.tot,'untranslated',B.length);const by={};B.forEach(([k,w])=>by[w]=(by[w]||0)+1);console.log(JSON.stringify(by));if(process.argv[4])B.slice(0,+process.argv[4]).forEach(([k,w])=>console.log(w,'|',k.slice(0,110)));
fs.unlinkSync('build/_t.html');await b.close()})()
