// 그날 밤 · 결혼 · 아이가 언제 오는지. 애정 갈래, 전쟁이 끝날 때의 인연 단계별. 사용: node ep2when.js [단계마다 생 수]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const N=+process.argv[2]||40;
let s=fs.readFileSync('build/game.html','utf8');s=s.replace('  function finalYears(){\n','  globalThis.__stayGo=()=>grantStay(undefined); globalThis.__rel=()=>relOf();\n  function finalYears(){\n');fs.writeFileSync('build/_t.html',s);
const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e)));await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(()=>{globalThis.__FORCE_CRISIS=false});
await p.goto('file://'+process.cwd()+'/build/_t.html');await p.waitForFunction(()=>typeof Sim==='object'&&Sim.HEROES);
const ST=(process.argv[3]?[[3,92,95]]:[[0,65,10],[1,70,35],[2,80,65],[3,92,95]]);
for(const [st,tr,pt] of ST){
 const R=await p.evaluate(([N,st,tr,pt])=>{const R=[];let t=0;while(R.length<N&&t++<N*12){Sim.newLife({seed:9000+(st%3)*1000+t+(st===3?500:0),len:20});Sim.start();let g=0;
  while(Sim.S&&!Sim.S.dead&&!(Sim.S.war&&Sim.S.war.pairs&&Sim.S.war.heroAlive&&Sim.S.war.day>=2)&&g++<200000){const S=Sim.S;if(S.pending)Sim.resolve(Sim.autoChoice(S.pending));else Sim.tick(1);}
  const S=Sim.S;if(!S||S.dead||!S.war||!S.war.heroAlive)continue;const r=__rel();if(!r||r.track!=='love')continue;
  S.war.trust=tr;r.open=1;r.pt=pt;r.stage=st;S.pending=null;S.war.queue=[];S.war.cupPure=true;const a0=S.age,y0=S.year;__stayGo();
  const o={a0,s3:null,night:null,wed:null,kid:null};let q=0;const mo=()=>{const E=Sim.S.epi||{};return E.ph==='A'?E.d/30:E.ph==='B'?E.m:(Sim.S.year-y0)*12;};
  while(!Sim.S.dead&&q++<400000){if(Sim.S.pending)Sim.resolve(Sim.autoChoice(Sim.S.pending));else Sim.tick(1);const f=Sim.S.flags,rr=__rel();
   if(rr&&rr.stage>=3&&o.s3==null)o.s3=mo();if(f.relNight&&o.night==null)o.night=mo();if(f.relWed&&o.wed==null){o.wed=mo();o.wedAge=Sim.S.age;}if(f.relKid!=null&&o.kid==null){o.kid=mo();o.kidAge=Sim.S.age;}}
  o.end=Sim.S.age;R.push(o);}return R;},[N,st,tr,pt]);
 const f=k=>{const v=R.filter(x=>x[k]!=null).map(x=>x[k]).sort((a,b)=>a-b);if(!v.length)return '없음';const med=v[Math.floor(v.length/2)],avg=v.reduce((a,b)=>a+b,0)/v.length;
  const fmt=m=>m<1?Math.round(m*30)+'일':m<=12?Math.round(m)+'달':(m/12).toFixed(1)+'년';return `${v.length}/${R.length}생 · 중앙 ${fmt(med)} · 평균 ${fmt(avg)} · 첫 해 안 ${v.filter(x=>x<=12).length} · 10년 안 ${v.filter(x=>x<=120).length}`;};
 const age=k=>{const v=R.filter(x=>x[k]!=null).map(x=>x[k]);return v.length?(v.reduce((a,b)=>a+b,0)/v.length).toFixed(1):'-';};
 console.log(`\n[전쟁 끝 ${st}단계 · 신뢰 ${tr}] 시작 나이 평균 ${(R.reduce((a,x)=>a+x.a0,0)/R.length).toFixed(1)}`);
 console.log('  연인(3단계):',f('s3'));console.log('  그날 밤   :',f('night'));console.log('  결혼      :',f('wed'),'· 평균 나이',age('wedAge'));console.log('  아이      :',f('kid'),'· 평균 나이',age('kidAge'));
}
console.log('errs',errs.length);fs.unlinkSync('build/_t.html');await b.close()})()
