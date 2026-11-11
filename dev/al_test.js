// 속성 계산 시험: 상세안 표의 값과 맞는지 본다. node dev/al_test.js <game.html>
const fs=require('fs'),vm=require('vm');const src=fs.readFileSync(process.argv[2],'utf8');const a=src.indexOf('<script id="sim">')+17,b=src.indexOf('</script>',a);
let code=src.slice(a,b).replace('  return {cn,ACH:','  globalThis.__T={traitR,crossReact,alR,mixR,lkR,gatherTr,W:()=>S.war,setHero:id=>{S.hero=id;}};\n  return {cn,ACH:');
const ctx={console};ctx.globalThis=ctx;ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code+';globalThis.Sim=Sim;',ctx);
const Sim=ctx.Sim,T=ctx.__T;Sim.setHooks(new Proxy({},{get:()=>()=>{}}));
for(let seed=1;seed<200;seed++){ Sim.newLife({seed,len:20});Sim.start();let g=0;while(Sim.S&&!Sim.S.dead&&g++<400000&&!(Sim.S.phase==='war'&&Sim.S.war&&Sim.S.war.heroAlive)){const S=Sim.S;if(S.pending){Sim.resolve(Sim.autoChoice(S.pending));continue;}Sim.tick(1);} if(Sim.S.phase==='war') break; }
const id=n=>Sim.HEROES.find(h=>h.name===n).id;
const w=T.W(); let bad=0,ok=0;
const cr=(r,al)=>{ w.trust=50; T.crossReact(r,al); return Math.round(w.trust-50); };
const chk=(who,lab,got,exp)=>{ if(got===exp) ok++; else { bad++; console.log('✗',who,lab,'got',got,'exp',exp); } };
const SIX={'알트리아 펜드래곤':0,'레오나르도 다 빈치':1,'여왕 메이브':2,'세미라미스':3,'에미야':4,'길가메시':5};
// 단발 장면 (5-3 바뀌는 예) [라벨, 계산, 기대값 6명]
const single=[
 ['버스 구출',()=>6+T.traitR({연민:3,명예:2,야망:-2},{선:3,악:-3,질서:1}),[9,9,4,4,11,7]],
 ['버스 싸움',()=>T.traitR({연민:-3,명예:-2,야망:1},{선:-3,악:1,질서:-1}),[-3,-3,1,1,-5,-1]],
 ['아이',h=>Math.round(T.mixR(h.traits.includes('연민')?7:3,T.alR({선:7,중용:5,악:3}))),[5,7,3,3,6,5]],
 ['말로',h=>Math.round(T.mixR(h.traits.includes('연민')?4:0,T.alR({선:4,중용:2,악:0}))),[2,4,0,0,3,2]],
 ['결투',h=>Math.round(T.mixR(h.traits.includes('명예')?8:2,T.alR({질서:8}))),[8,2,2,5,8,2]],
 ['저격',h=>Math.round(T.mixR(h.traits.includes('명예')?-6:h.traits.includes('야망')?0:-2,T.alR({선:-4,중용:-2}))),[-5,-3,0,0,-4,-2]],
 ['인질',()=>T.traitR({연민:-4,명예:-2,충성:-1,야망:1},{선:-4,악:1}),[-3,-4,1,2,-6,-1]],
 ['기억',()=>T.traitR({충성:1,연민:1},{질서:4}),[3,1,0,2,1,0]],
 ['그냥',()=>T.traitR({자유:2,충성:-1},{질서:-4,혼돈:2}),[-2,2,2,-2,0,2]],
 ['교회',()=>T.traitR({연민:-3,충성:1},{질서:2,선:-4,악:2}),[0,-3,1,2,-3,-2]],
 ['소집응',()=>T.traitR({충성:2,명예:1,자유:-2},{질서:4,혼돈:-2}),[4,-2,-2,2,1,-2]],
 ['소집무',()=>T.traitR({자유:2,충성:-1},{질서:-2,혼돈:2}),[-1,2,2,-1,0,2]],
 ['고맙다',()=>4+T.traitR({연민:2,명예:2,충성:1,야망:-1},{선:2}),[7,6,3,3,8,5]],
 ['예',()=>3+T.traitR({명예:3,충성:3,연민:1,자유:-2},{질서:3,혼돈:-2}),[8,2,1,5,7,1]],
 ['소원',()=>2+T.traitR({연민:2,야망:3,자유:1,충성:-1},{악:2,혼돈:1}),[1,4,6,6,4,5]],
 ['작전',()=>1+T.traitR({충성:2,야망:2,명예:1,자유:-1},{질서:2,혼돈:-1}),[4,0,1,4,2,1]],
 ['뒷걸음',()=>-3+T.traitR({명예:-2,야망:-2,연민:1},{선:1,악:-1}),[-3,-2,-4,-5,-4,-3]],
];
const cross=[
 ['치료',{명예:4,연민:6,야망:-4,자유:2},{선:6,악:-4},[8,11,-4,-7,15,3]],
 ['끝낸다',{명예:-6,연민:-6,충성:2,야망:6},{선:-6,악:4,질서:-2},[-9,-9,8,8,-18,0]],
 ['건물',{연민:6,명예:4,충성:2,야망:-3},{선:6,악:-2},[9,9,-4,-5,15,2]],
 ['숨김',{연민:-6,명예:-3,야망:3,자유:1},{선:-6,악:4,질서:2},[-5,-8,6,8,-13,-1]],
 ['정면',{명예:6,자유:2,야망:-1},{질서:4},[8,3,2,2,9,2]],
 ['함정',{명예:-7,야망:5,자유:-1},{질서:-6,혼돈:2,악:2},[-10,1,6,3,-10,5]],
 ['밀약',{야망:5,명예:-3,충성:-1},{질서:-2,혼돈:2},[-4,2,5,4,-4,5]],
 ['귀띔',{명예:3,연민:4,야망:-4},{선:4,질서:-2,혼돈:2},[4,8,-1,-6,11,2]],
 ['반납',{명예:5,야망:-4,자유:-2},{질서:6,혼돈:-4},[8,-4,-7,0,8,-7]],
 ['빼냄',{충성:3,자유:3,명예:-2,연민:1},{질서:-6,혼돈:4},[-4,6,5,-4,-1,5]],
 ['정보',{야망:3,명예:-4,연민:-1},{선:-4,악:2},[-6,-4,4,5,-7,-1]],
];
for(const [n,i] of Object.entries(SIX)){ const hid=id(n); T.setHero(hid); const h=Sim.H_BY[hid];
  for(const [lab,f,e] of single) chk(n,lab,f(h),e[i]);
  for(const [lab,r,al,e] of cross) chk(n,lab,cr(r,al),e[i]); }
// 마력 수집 (5-1) — 캐스터 17명
const G=[['메데이아',5,6],['멀린',-2,-4],['파라켈수스',-3,-5],['질 드 레',5,5],['타마모노마에',-1,-1],['한스 크리스티안 안데르센',-2,-5],['윌리엄 셰익스피어',1,0],['레오나르도 다 빈치',-3,-5],['니토크리스',-3,-7],['볼프강 아마데우스 모차르트',-3,-6],['현장 삼장',-3,-7],['키르케',-2,-4],['아비케브론',1,-1],['프랑수아 프렐라티',5,7],['솔로몬',-3,-7],['시바의 여왕',0,-1],['아스클레피오스',-2,-4]];
for(const [n,s1,s2] of G){ T.setHero(id(n)); chk(n,'수집 조금',T.gatherTr(false).tr,s1); chk(n,'수집 크게',T.gatherTr(true).tr,s2); }
// 취향
T.setHero(id('쿠 훌린')); chk('쿠 훌린','결투+취향',Math.round(T.mixR(8,T.alR({질서:8})))+T.lkR('정면승부'),14);
T.setHero(id('에미야')); chk('에미야','버스 싸움+취향',T.traitR({연민:-3,명예:-2,야망:1},{선:-3,악:1,질서:-1},'-구조'),-11);
console.log('ok',ok,'bad',bad);
