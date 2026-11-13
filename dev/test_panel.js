/* ===== 테스트 조절판 (테스트용 HTML에만 들어간다 · mktest.py) =====
   전투 보정 · 마스터 스탯 · 서번트 상태 · 시작 조건(서번트 · 위기 고정) · 빠른 배속.
   설정은 이 브라우저에만 남는다(cupnight.test.v1). */
(()=>{
const K='cupnight.test.v1', D={pow:0,dmgIn:1,dmgOut:1,hero:'',crisis:'nat'};
let T=Object.assign({},D); try{ Object.assign(T,JSON.parse(localStorage.getItem(K)||'{}')); }catch(e){}
const save=()=>{ try{ const {hook:_,...o}=T; localStorage.setItem(K,JSON.stringify(o)); }catch(e){} apply(); };
function apply(){ T.hook=hook; window.__TEST=T; window.__FORCE_HERO=T.hero||undefined; window.__FORCE_CRISIS=T.crisis==='nat'?undefined:T.crisis==='off'?false:T.crisis; badge(); }
const on=()=>T.pow!==0||T.dmgIn!==1||T.dmgOut!==1||!!T.hero||T.crisis!=='nat';
// 받는 피해 · 주는 피해: 전투 중 체력이 줄어드는 만큼에 배율을 곱한다
function wrapHp(o,kind){ if(!o||o.__tw||typeof o.hp!=='number') return; let v=o.hp; Object.defineProperty(o,'__tw',{value:1,enumerable:false});
  Object.defineProperty(o,'hp',{enumerable:true,configurable:true,get(){ return v; },set(n){ const w=Sim.S&&Sim.S.war;
    if(w&&w.battle&&typeof n==='number'&&n<v){ if(kind==='me'&&T.dmgIn!==1) n=Math.max(0,v-(v-n)*T.dmgIn); else if(kind==='e'&&w.battle.e===o&&T.dmgOut!==1) n=Math.max(0,v-(v-n)*T.dmgOut); }
    v=n; }}); }
const wrapAll=()=>{ if(T.dmgIn===1&&T.dmgOut===1) return; const S=Sim.S, w=S&&S.war; if(!w) return; wrapHp(w,'me'); (w.pairs||[]).forEach(p=>wrapHp(p,'e')); ((w.crisis&&w.crisis.units)||[]).forEach(u=>wrapHp(u,'e')); };
setInterval(wrapAll,250);
// 엔진이 합마다 부른다: 이번 합의 나와 상대에 배율을 걸어 둔다
const hook=(w,e)=>{ if(T.dmgIn===1&&T.dmgOut===1) return; wrapHp(w,'me'); wrapHp(e,'e'); };
// ---- 화면 ----
const st=document.createElement('style'); st.textContent=`
#tpBtn{position:fixed;left:max(10px,env(safe-area-inset-left,0px));bottom:max(10px,env(safe-area-inset-bottom,0px));z-index:2147482000;font:600 12px/1 system-ui,sans-serif;padding:8px 11px;border-radius:999px;border:1px solid #6b5a8a;background:#1d1828ee;color:#d8cdf0;cursor:pointer}
#tpBtn.on{border-color:#e3c98d;color:#e3c98d}#tpBtn.on::after{content:" · 보정 켜짐"}
#tpPan{position:fixed;left:max(10px,env(safe-area-inset-left,0px));bottom:calc(max(10px,env(safe-area-inset-bottom,0px)) + 40px);z-index:2147482000;width:min(320px,calc(100vw - 20px));max-height:min(78vh,640px);overflow:auto;box-sizing:border-box;padding:12px 14px;border-radius:12px;border:1px solid #4a3f5e;background:#16121fef;color:#e8e2f2;font:13px/1.5 system-ui,-apple-system,'Malgun Gothic',sans-serif;box-shadow:0 10px 30px #0008}
#tpPan[hidden]{display:none}#tpPan h4{margin:12px 0 6px;font-size:12px;letter-spacing:.08em;color:#b6a8d4}#tpPan h4:first-child{margin-top:0}
#tpPan label{display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:center;margin:4px 0}#tpPan label input[type=range]{grid-column:1/-1;width:100%}
#tpPan b{font-weight:600;color:#e3c98d;font-variant-numeric:tabular-nums}
#tpPan .g{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px}#tpPan .g label{grid-template-columns:1fr 64px}
#tpPan input[type=number],#tpPan select{width:100%;box-sizing:border-box;background:#0f0c16;color:#eee;border:1px solid #3d3450;border-radius:6px;padding:3px 6px;font:inherit}
#tpPan .row{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}#tpPan button{font:inherit;font-size:12px;padding:4px 10px;border-radius:7px;border:1px solid #4a3f5e;background:#221c30;color:#e8e2f2;cursor:pointer}#tpPan button:hover{border-color:#e3c98d}
#tpPan .note{font-size:11.5px;color:#9b90b0;margin:4px 0 0}#tpPan .dim{opacity:.45;pointer-events:none}`;
document.head.appendChild(st);
const btn=document.createElement('button'); btn.id='tpBtn'; btn.type='button'; btn.textContent='테스트'; btn.setAttribute('data-notr','');
const pan=document.createElement('div'); pan.id='tpPan'; pan.hidden=true; pan.setAttribute('data-notr','');
const STL={mana:'마력',lore:'지식',will:'정신',bond:'관계',health:'건강'};
const HO=()=>Sim.HEROES.slice().sort((a,b)=>a.name.localeCompare(b.name,'ko')).map(h=>`<option value="${h.id}">${h.name} (${(Sim.CLS[h.cls]||{}).n||h.cls})</option>`).join('');
pan.innerHTML=`<h4>전투</h4>
<label>내 판정 보정 <b id="tpPowN"></b><input id="tpPow" type="range" min="-40" max="60" step="5"></label>
<label>내 서번트가 받는 피해 <b id="tpInN"></b><input id="tpIn" type="range" min="0" max="2" step="0.1"></label>
<label>적에게 주는 피해 <b id="tpOutN"></b><input id="tpOut" type="range" min="0.5" max="3" step="0.1"></label>
<h4>마스터</h4><div class="g" id="tpSt"></div>
<h4>서번트</h4><div id="tpSv"><div class="row"><button type="button" id="tpFill">체력 · 마력 가득</button></div><div class="g"><label>신뢰 <input type="number" id="tpTrust" min="0" max="100"></label><label>령주 <input type="number" id="tpSeals" min="0" max="3"></label></div></div><p class="note" id="tpSvNote">성배전쟁 중에만 바꿀 수 있습니다.</p>
<h4>시작 조건 (다음 생부터)</h4>
<label style="grid-template-columns:1fr">소환될 서번트<select id="tpHero"><option value="">고정하지 않음</option>${HO()}</select></label>
<label style="grid-template-columns:1fr">후반 위기<select id="tpCx"><option value="nat">자연 (설정대로)</option><option value="off">없음</option><option value="black">검은 성배</option><option value="beast3R">비스트 Ⅲ/R</option></select></label>
<h4>진행</h4><div class="row"><button type="button" data-sp="16">×16</button><button type="button" data-sp="32">×32</button><button type="button" data-sp="1">×1로</button></div>
<div class="row"><button type="button" id="tpReset">보정 모두 끄기</button></div>
<p class="note">이 조절판은 테스트용 파일에만 있습니다. 보정을 켠 채로 얻은 업적 · 기록도 이 브라우저에 그대로 남습니다.</p>`;
document.body.append(btn,pan);
const $=s=>pan.querySelector(s);
const fmt=()=>{ $('#tpPowN').textContent=(T.pow>0?'+':'')+T.pow; $('#tpInN').textContent='×'+(+T.dmgIn).toFixed(1); $('#tpOutN').textContent='×'+(+T.dmgOut).toFixed(1); };
function badge(){ btn.classList.toggle('on',on()); }
function fill(){ $('#tpPow').value=T.pow; $('#tpIn').value=T.dmgIn; $('#tpOut').value=T.dmgOut; $('#tpHero').value=T.hero||''; $('#tpCx').value=T.crisis; fmt(); live(); }
function live(){ const S=Sim.S; const g=$('#tpSt');
  if(!g.children.length) g.innerHTML=Object.entries(STL).map(([k,n])=>`<label>${n} <input type="number" data-k="${k}" min="0" max="100"></label>`).join('')+`<label>재산 <input type="number" data-k="wealth" min="0"></label>`;
  g.querySelectorAll('input').forEach(i=>{ if(document.activeElement===i) return; const k=i.dataset.k; i.value=!S?'':k==='wealth'?Math.round(S.wealth||0):Math.round((S.st||{})[k]||0); });
  const w=S&&S.war, wa=!!(w&&S.phase==='war'); $('#tpSv').classList.toggle('dim',!wa); $('#tpSvNote').hidden=wa;
  if(wa){ if(document.activeElement!==$('#tpTrust')) $('#tpTrust').value=Math.round(w.trust||0); if(document.activeElement!==$('#tpSeals')) $('#tpSeals').value=w.seals||0; } }
btn.onclick=()=>{ pan.hidden=!pan.hidden; if(!pan.hidden) fill(); };
setInterval(()=>{ if(!pan.hidden) live(); },800);
$('#tpPow').oninput=e=>{ T.pow=+e.target.value; fmt(); save(); };
$('#tpIn').oninput=e=>{ T.dmgIn=+e.target.value; fmt(); save(); };
$('#tpOut').oninput=e=>{ T.dmgOut=+e.target.value; fmt(); save(); };
$('#tpHero').onchange=e=>{ T.hero=e.target.value; save(); };
$('#tpCx').onchange=e=>{ T.crisis=e.target.value; save(); };
$('#tpSt').addEventListener('change',e=>{ const i=e.target, S=Sim.S; if(!S||!i.dataset.k) return; const v=Math.max(0,+i.value||0); if(i.dataset.k==='wealth') S.wealth=v; else S.st[i.dataset.k]=Math.min(100,v); });
$('#tpFill').onclick=()=>{ const w=Sim.S&&Sim.S.war; if(!w) return; w.hp=100; w.sm=100; live(); };
$('#tpTrust').onchange=e=>{ const w=Sim.S&&Sim.S.war; if(w) w.trust=Math.max(0,Math.min(100,+e.target.value||0)); };
$('#tpSeals').onchange=e=>{ const w=Sim.S&&Sim.S.war; if(w) w.seals=Math.max(0,Math.min(3,+e.target.value||0)); };
pan.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{ if(Sim.S) Sim.S.speed=+b.dataset.sp; });
$('#tpReset').onclick=()=>{ T=Object.assign({},D); save(); fill(); };
apply();
})();
