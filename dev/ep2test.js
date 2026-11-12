// 에필로그 시간 흐름 시험: 수육 결말로 바로 넘겨 끝까지 돌린다. 사용: node ep2test.js [생 수] [love|friend]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{
const N=+process.argv[2]||30, TR=process.argv[3]||'';
let s=fs.readFileSync('build/game.html','utf8');const a="  function finalYears(){\n";
s=s.replace(a,"  globalThis.__stayGo=()=>grantStay(undefined); globalThis.__rel=()=>relOf();\n"+a);fs.writeFileSync('build/_t.html',s);
const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e)));await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
await p.addInitScript(()=>{globalThis.__FORCE_CRISIS=false});
await p.goto('file://'+process.cwd()+'/build/_t.html');await p.waitForFunction(()=>typeof Sim==='object'&&Sim.HEROES);
const out=await p.evaluate(([N,TR])=>{const R=[];let tries=0;while(R.length<N&&tries++<N*6){Sim.newLife({seed:5000+tries,len:20});Sim.start();let g=0;
 while(Sim.S&&!Sim.S.dead&&!(Sim.S.war&&Sim.S.war.pairs&&Sim.S.war.heroAlive&&Sim.S.war.day>=2)&&g++<200000){const S=Sim.S;if(S.pending)Sim.resolve(Sim.autoChoice(S.pending));else Sim.tick(1);}
 const S=Sim.S;if(!S||S.dead||!S.war||!S.war.heroAlive)continue;const r=__rel();if(!r)continue;if(TR&&r.track!==TR)continue;
 S.war.trust=70+(tries%3)*10;r.open=1;r.pt=20+(tries%4)*20;r.stage=Math.min(3,Math.floor(r.pt/30));S.pending=null;S.war.queue=[];S.war.cupPure=true;
 const age0=S.age;try{__stayGo();}catch(e){R.push({err:'go '+e.message});continue;}
 const st={age0,track:r.track,st0:r.stage,ev:{A:0,B:0,C:0,D:0,x:0},ids:[],steps:0,t0:S.log.length};let q=0,lastPh=null;
 try{while(!Sim.S.dead&&q++<400000){const S=Sim.S;if(S.pending){const E=S.epi||{};const ph=E.ph||'x';st.ev[ph]=(st.ev[ph]||0)+1;st.ids.push(ph+':'+S.pending.title);
     if(/결혼|작은 식/.test(S.pending.title)&&!st.wed0)st.wed0=[S.age,ph];
     Sim.resolve(Sim.autoChoice(S.pending));}else Sim.tick(1);
   const f=Sim.S.flags;if(f.relWed&&!st.wed)st.wed=[Sim.S.age,(Sim.S.epi||{}).ph];if(f.relKid!=null&&!st.kid)st.kid=[Sim.S.age,(Sim.S.epi||{}).ph];if(f.relNight&&!st.night)st.night=[Sim.S.age,(Sim.S.epi||{}).ph,(Sim.S.epi||{}).m];
   const rr=__rel();if(rr&&rr.stage>=3&&!st.s3)st.s3=[Sim.S.age,(Sim.S.epi||{}).ph,(Sim.S.epi||{}).d,(Sim.S.epi||{}).m];}
 }catch(e){st.err=e.message+' @'+(Sim.S.pending&&Sim.S.pending.title);}
 st.ageEnd=Sim.S.age;st.dead=Sim.S.dead;st.E=Sim.S.epi&&{ph:Sim.S.epi.ph,d:Sim.S.epi.d,m:Sim.S.epi.m,cy:Sim.S.epi.cy};
 st.heads=Sim.S.log.slice(st.t0).filter(x=>x.k==='night').map(x=>x.t).slice(0,40);
 if(R.length===0)st.sample=Sim.S.log.slice(st.t0,st.t0+60).map(x=>(x.k||'')+'|'+(x.t||''));
 R.push(st);}
 return R;},[N,TR]);
const ok=out.filter(x=>!x.err);const avg=k=>(ok.reduce((a,x)=>a+x.ev[k],0)/ok.length).toFixed(1);
console.log('lives',out.length,'errs',out.filter(x=>x.err).map(x=>x.err).slice(0,5),'pageerr',errs.slice(0,3));
console.log('events/phase A',avg('A'),'B',avg('B'),'C',avg('C'),'D',avg('D'),'| not dead',ok.filter(x=>!x.dead).length);
const pct=k=>ok.filter(x=>x[k]).length;const yrs=k=>ok.filter(x=>x[k]).map(x=>x[k][0]-x.age0+(x[k][1]||'')).join(' ');
console.log('track',JSON.stringify(ok.reduce((a,x)=>(a[x.track]=(a[x.track]||0)+1,a),{})),'s3',pct('s3'),'|',yrs('s3'));
console.log('night',pct('night'),yrs('night'),'\nwed',pct('wed'),yrs('wed'),'\nkid',pct('kid'),yrs('kid'));
console.log('final ph',JSON.stringify(ok.reduce((a,x)=>(a[x.E&&x.E.ph]=(a[x.E&&x.E.ph]||0)+1,a),{})));
if(process.argv[4]){console.log(out[0].sample.join('\n'));console.log(out[0].ids.join(' / '));}
fs.unlinkSync('build/_t.html');await b.close()})()
