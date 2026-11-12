"""로비 새 배경 (11-13): 밤하늘 네 판(무작위) · 도시 불빛 = 살아 본 생 · 영령의 별 = 도감 · 움직임 · 새 배치 · 「이 밤의 이야기와 규칙」 펼침.
원본 시안: dev/lobby/index.html, 배경과 움직임 코드: dev/lobby_rt.js, 하늘 그림: public/assets/lobby/sky1~4.webp
사용: python3 lobby_apply.py <game.html>"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = r'''
/* ---- 로비 새 배경 (lobby_apply) ---- */
#lobbyBg{position:fixed;inset:0;z-index:0;overflow:hidden;background:#121019;pointer-events:none}
#lobbyBg[hidden]{display:none}
#lbStage{position:absolute;left:0;top:0;transform-origin:0 0;opacity:0}
#lbStage.in{opacity:1;transition:opacity 1.2s}
#lbStage .lay{position:absolute;left:0;top:0;width:100%;height:100%;max-width:none}
#lbStage .skyg{position:absolute;left:0;top:0}
#lbStage .small{opacity:0}#lbStage.in .small{opacity:1;transition:opacity 3s .4s}
#lbStage .lights{opacity:0}#lbStage.in .lights{opacity:1;transition:opacity 1.6s .5s}
#lbStage .bloom{opacity:0;mix-blend-mode:screen;transition:opacity 1.6s}#lbStage .bloom.on{opacity:.9}
#lobbyBg .lb-fade{position:absolute;left:0;right:0;bottom:0;top:70%;background:linear-gradient(180deg,rgba(18,16,25,0),rgba(18,16,25,.92) 60px,#121019 110px)}
body.lb-on{background:#121019}
#intro.lb{max-width:none;padding:0}
#intro.lb .intro-grid,#intro.lb .intro-art,#intro.lb .lp-mo,#intro.lb .rules,#intro.lb .agenote,#intro.lb>.lb-hide{display:none}
#intro.lb .lb-screen{position:relative;z-index:1;box-sizing:border-box;min-height:100vh;min-height:100svh;max-width:434px;margin:0 auto;display:flex;flex-direction:column;
  padding-top:max(20px,env(safe-area-inset-top,0px));padding-bottom:max(22px,env(safe-area-inset-bottom,0px));padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
body.lb-wide #intro.lb .lb-screen{max-width:860px}
#intro.lb .lb-top{display:flex;justify-content:space-between;align-items:center;gap:8px}
#intro.lb .lb-top .lang-pick{display:inline-flex;margin:0}
#intro.lb .lb-tools{display:flex;gap:6px;align-items:center}
#intro.lb .lb-ico{width:34px;height:34px;display:grid;place-items:center;border-radius:999px;border:1px solid var(--line);background:rgba(18,16,25,.5);color:var(--dim);cursor:pointer;padding:0}
#intro.lb .lb-ico svg{width:17px;height:17px}#intro.lb .lb-ico[aria-pressed=false]{opacity:.55}
#intro.lb .lb-pickrow{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}#intro.lb .lb-pickrow:empty{display:none}
#intro.lb .eyebrow{margin-top:18px}
#intro.lb .title{font-size:clamp(38px,11vw,46px);line-height:1.12;text-shadow:0 2px 18px rgba(8,6,14,.7)}
body.lb-wide #intro.lb .title{font-size:52px}
#intro.lb .tagline{border:0;padding:0;margin-top:8px;background:none}
#intro.lb .lang-note{margin:10px 0 0;font-size:12px}
#intro.lb .snd-ask{margin:12px 0 0}
#intro.lb .lb-lit{margin-top:14px;font-family:var(--f-story);font-size:13.5px;line-height:1.7;color:var(--text);text-shadow:0 1px 8px #08060e,0 0 14px #08060e}
#intro.lb .lb-lit b{color:var(--gold2);font-weight:400}
#intro.lb .lb-more{align-self:flex-start;margin-top:12px;font:inherit;font-family:var(--f-story);font-size:13px;color:var(--gold2);background:none;border:0;border-bottom:1px solid rgba(227,201,141,.4);padding:2px 0;cursor:pointer;text-shadow:0 1px 8px #08060e}
#intro.lb .lb-sp{flex:1;min-height:36vh}
body.lb-wide #intro.lb .lb-sp{min-height:30vh}
#intro.lb .lb-acts{display:grid;gap:8px}
#intro.lb .lb-acts>*{margin:0}
#intro.lb .lb-acts #contBtn{width:100%}
#intro.lb .lb-acts .bondp{background:rgba(18,16,25,.72)}
#intro.lb .sex-pick{background:rgba(18,16,25,.75)}
#intro.lb .lb-row{display:flex;gap:8px}#intro.lb .lb-row[hidden]{display:none}
#intro.lb .lb-row .btn{flex:1;position:relative;padding-inline:6px;font-size:14px}
#intro.lb .lb-row .lb-dot{position:absolute;top:7px;right:9px;width:6px;height:6px;border-radius:50%;background:#e58b93}
body.lb-wide #intro.lb .lb-acts{grid-template-columns:1fr 1fr;gap:8px 10px;align-items:stretch}
#intro.lb .lb-foot{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:8px;margin-top:14px}
#intro.lb .lb-foot .pn-btn{font-size:12.5px}
#intro.lb .keys{display:none;margin:10px 0 0;text-align:center;font-size:11.5px;line-height:1.8}
body.lb-wide #intro.lb .keys{display:block}
#intro.lb .ghn,#intro.lb #ghnRow{margin-top:10px}
#intro.lb .past{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left,0px)) 96px;background:#121019}
/* 이 밤의 이야기와 규칙: 배경 위에 옅은 검은 막을 깔고 띄운다 */
#lbAbout{position:fixed;inset:0;z-index:60;overflow:hidden}
#lbAbout[hidden]{display:none}
#lbAbout .ab-veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,6,14,.72),rgba(6,6,14,.58) 45%,rgba(6,6,14,.80));opacity:0;transition:opacity .5s}
#lbAbout.open .ab-veil{opacity:1}
#lbAbout .ab-in{position:relative;height:100%;overflow-y:auto;box-sizing:border-box;max-width:640px;margin:0 auto;padding-top:max(64px,calc(env(safe-area-inset-top,0px) + 56px));padding-bottom:max(48px,env(safe-area-inset-bottom,0px));padding-left:max(24px,env(safe-area-inset-left,0px));padding-right:max(24px,env(safe-area-inset-right,0px));opacity:0;transform:translateY(14px);transition:opacity .55s .08s,transform .55s .08s;outline:none}
#lbAbout.open .ab-in{opacity:1;transform:none}
body.lb-wide #lbAbout .ab-in{max-width:880px;padding-top:96px}
#lbAbout .ab-x{position:fixed;top:max(18px,calc(env(safe-area-inset-top,0px) + 14px));right:max(18px,calc(env(safe-area-inset-right,0px) + 14px));width:36px;height:36px;border-radius:999px;border:1px solid var(--line);background:rgba(18,16,25,.5);color:var(--dim);font-size:14px;cursor:pointer;z-index:2}
#lbAbout .ab-h{font-family:var(--f-display);font-weight:400;font-size:34px;line-height:1.15;margin:0 0 18px;color:var(--text)}
#lbAbout .lede p{font-size:15.5px;line-height:1.85;margin:0 0 14px;color:rgba(235,229,216,.92)}
#lbAbout .counter{margin:22px 0;padding:14px 0;border-top:1px solid rgba(235,229,216,.16);border-bottom:1px solid rgba(235,229,216,.16)}
#lbAbout .rules{display:grid;gap:16px;margin:22px 0;padding:0;border:0}
body.lb-wide #lbAbout .rules{grid-template-columns:repeat(3,1fr);gap:22px}
#lbAbout .rules h3{color:var(--gold2)}
#lbAbout .warn,#lbAbout .agenote,#lbAbout .ab-spoil{display:block;font-size:12.5px;color:var(--dim);margin:0 0 6px;text-align:left}
#lbAbout .agenote::before{content:"※ "}
#lbAbout .ab-go{display:block;margin:26px 0 8px;width:100%;max-width:320px}
body.lb-wide #lbAbout .ab-go{margin-inline:auto}
body.lb-reading #intro.lb .lb-screen{opacity:0;transition:opacity .45s}
@media (prefers-reduced-motion:reduce){#lbAbout .ab-veil,#lbAbout .ab-in{transition:none}}
'''
HTML = '''<div id="lobbyBg" hidden aria-hidden="true"><div id="lbStage"></div><div class="lb-fade"></div></div>
'''
RT = open(os.path.join(HERE, 'lobby_rt.js'), encoding='utf-8').read()
LAY = r'''
/* ---- 로비 새 배치: 기존 단추를 그대로 옮겨 쓴다 (기능 · 번역은 그대로) ---- */
(function(){ const $q=s=>document.querySelector(s), intro=$q('#intro'); if(!intro||typeof LOBBY==='undefined') return;
  const TX={ko:{more:'이 밤의 이야기와 규칙',go:'이 밤으로 들어간다',spoil:'※ TYPE-MOON 세계관에 대한 스포일러가 포함될 수 있습니다.',none:'아직 불 켜진 창도,<br>떠오른 별도 없다.',lit:(a,b)=>`<b>${a}번</b>의 생이 불을 켜고,<br><b>${b}명</b>의 영령이 별이 되었다.`,close:'닫기',snd:'소리 켜기 · 끄기',set:'설정'},
    en:{more:'The story and rules of this night',go:'Into the night',spoil:'※ May contain spoilers for the TYPE-MOON universe.',none:'No window is lit yet,<br>and no star has risen.',lit:(a,b)=>`<b>${a}</b> ${a===1?'life has':'lives have'} lit the city,<br><b>${b}</b> Heroic Spirit${b===1?' has':'s have'} become stars.`,close:'Close',snd:'Sound on / off',set:'Settings'},
    ja:{more:'この夜の物語とルール',go:'この夜へ',spoil:'※ TYPE-MOON作品の世界観に関するネタバレを含む場合があります。',none:'まだ灯る窓も、<br>昇る星もない。',lit:(a,b)=>`<b>${a}</b>の生が灯をともし、<br><b>${b}</b>人の英霊が星になった。`,close:'閉じる',snd:'サウンドのオン・オフ',set:'設定'}}[typeof LANG==='string'&&['en','ja'].includes(LANG)?LANG:'ko'];
  const el=(t,c,h)=>{ const e=document.createElement(t); if(c) e.className=c; if(h!=null) e.innerHTML=h; return e; };
  const mv=(p,...s)=>s.forEach(x=>{ const n=typeof x==='string'?$q(x):x; if(n) p.appendChild(n); });
  intro.classList.add('lb');
  { const t=intro.querySelector('h1.title'); if(t) t.innerHTML=t.innerHTML.replace(/<br\s*\/?>/gi,LANG==='ja'?'':' '); }
  const scr=el('div','lb-screen'), top=el('div','lb-top'), tools=el('div','lb-tools'), pr=el('div','lb-pickrow');
  const snd=el('button','lb-ico','<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 8h3l4-3v10l-4-3H4z" fill="currentColor"/><path d="M13.5 7.5a3.5 3.5 0 0 1 0 5M15.5 5.5a6.4 6.4 0 0 1 0 9" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'); snd.type='button'; snd.setAttribute('aria-label',TX.snd); snd.title=TX.snd;
  const sndSt=()=>{ try{ snd.setAttribute('aria-pressed',String(!!Snd.on())); }catch(e){} };
  snd.onclick=()=>{ try{ Snd.enable(!Snd.on()); if(typeof sndBtn==='function') sndBtn(); if(typeof sndSync==='function') sndSync(); }catch(e){} sndSt(); };
  mv(top,'#langPick'); mv(tools,snd,'#setBtn'); top.appendChild(tools); mv(pr,'#pickBtn');
  const lit=el('div','lb-lit'), more=el('button','lb-more',TX.more+' <span aria-hidden="true">›</span>'); more.type='button'; more.setAttribute('aria-expanded','false'); more.setAttribute('aria-controls','lbAbout');
  mv(scr,top,pr,'#sndAsk',intro.querySelector('.eyebrow'),intro.querySelector('h1.title'),intro.querySelector('.tagline'),'#langNote',lit,more,el('div','lb-sp'));
  const acts=el('div','lb-acts'), row=el('div','lb-row');
  [['dex','서번트 도감'],['lives','지난 생'],['ach','업적']].forEach(([k,n])=>{ const b=el('button','btn',n); b.type='button'; b.dataset.v=k; b.onclick=()=>{ VT=k; renderVT(); const v=$q('#vtabs'); v&&v.scrollIntoView({behavior:'smooth',block:'start'}); }; row.appendChild(b); });
  mv(acts,intro.querySelector('.born-row'),'#contBtn','#bondPanel',row);
  const foot=el('div','lb-foot'); mv(foot,'#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#installBtn');
  mv(scr,acts,foot,intro.querySelector('.keys'),'#ghNews','#ghnRow');
  intro.insertBefore(scr,intro.firstChild);
  // 이야기와 규칙: 소개글 · 숫자 · 규칙 · 안내문을 옮겨 담는다
  const ab=el('section'); ab.id='lbAbout'; ab.hidden=true; ab.setAttribute('aria-label',TX.more);
  const veil=el('div','ab-veil'), inn=el('div','ab-in'); inn.tabIndex=-1;
  const x=el('button','ab-x','✕'); x.type='button'; x.setAttribute('aria-label',TX.close);
  const ey=el('div','eyebrow',(intro.querySelector('.eyebrow')||{}).innerHTML||''), h=el('div','ab-h');
  const go=el('button','btn primary ab-go',TX.go); go.type='button';
  mv(inn,x,ey,h,intro.querySelector('.lede'),intro.querySelector('.counter'),intro.querySelector('.rules'),intro.querySelector('.warn'),intro.querySelector('.agenote'),el('p','ab-spoil',TX.spoil),go);
  ab.append(veil,inn); document.body.appendChild(ab);
  let tm=0; const open=()=>{ clearTimeout(tm); const t=$q('#intro h1.title'); h.innerHTML=t?t.innerHTML:''; ab.hidden=false; document.body.classList.add('lb-reading'); more.setAttribute('aria-expanded','true'); requestAnimationFrame(()=>requestAnimationFrame(()=>{ ab.classList.add('open'); inn.focus({preventScroll:true}); })); };
  const close=()=>{ ab.classList.remove('open'); document.body.classList.remove('lb-reading'); more.setAttribute('aria-expanded','false'); tm=setTimeout(()=>{ ab.hidden=true; },550); };
  more.onclick=open; x.onclick=close; go.onclick=close; veil.onclick=close; inn.addEventListener('click',e=>{ if(e.target===inn) close(); });
  addEventListener('keydown',e=>{ if(e.key==='Escape'&&!ab.hidden){ e.stopPropagation(); close(); } },true);
  // 로비에 들어올 때마다: 판을 새로 고르고, 불빛 · 별 수를 다시 센다
  let firstShown=false;
  const stats=()=>{ let lv=0,mt=0; try{ const c=dexLoad(); lv=Math.max(c.lives||0,store.get(K_COUNT)||0,(store.get(K_HIST)||[]).length); mt=dexMetCount(c); }catch(e){} return {lives:lv,met:mt}; };
  const sync=()=>{ const on=!intro.classList.contains('hidden');
    if(!on){ if(LOBBY.active) LOBBY.leave(); return; }
    if(LOBBY.active) return;
    const s=stats(); lit.innerHTML=s.lives===0&&s.met===0?TX.none:TX.lit(s.lives,s.met);
    row.hidden=$q('#pastWrap').classList.contains('hidden'); const an=$q('#achNewBtn'); const ab2=row.querySelector('[data-v=ach]'); ab2.querySelector('.lb-dot')?.remove(); if(an&&!an.classList.contains('hidden')) ab2.appendChild(el('i','lb-dot'));
    sndSt(); LOBBY.enter(s); requestAnimationFrame(()=>LOBBY.fit());
    if(!firstShown){ firstShown=true; let sv=null; try{ sv=store.get(K_SAVE); }catch(e){} if(s.lives===0&&!sv) setTimeout(()=>{ if(!intro.classList.contains('hidden')) open(); },1600); } };
  new MutationObserver(sync).observe(intro,{attributes:true,attributeFilter:['class']});
  ['#contBtn','#pastWrap','#bondPanel','#sndAsk','#ghNews','#langNote'].forEach(s=>{ const n=$q(s); if(n) new MutationObserver(()=>LOBBY.active&&LOBBY.fit()).observe(n,{attributes:true,attributeFilter:['class','hidden']}); });
  sync();
})();
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, cnt=1):
        global s
        if s.count(o) != cnt: miss.append((o[:50], s.count(o))); return
        s = s.replace(o, n)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    rp('<!-- 시작 -->', HTML + '<!-- 시작 -->')
    # 배경 · 움직임은 따로 둔 스크립트에(LOBBY), 배치는 화면 스크립트 안 끝에(그 안의 함수 · 값을 써야 한다)
    k = s.index('(() => {\nconst $=s=>document.querySelector(s);'); e = s.index('</script>', k); b = s.rindex('})();', k, e)
    s = s[:b] + LAY + '\n' + s[b:]
    a = s.rindex('<script>', 0, k); s = s[:a] + '<script>\n' + RT + '\n</script>\n' + s[a:]
    open(P, 'w', encoding='utf-8').write(s); print('lobby miss', miss)
