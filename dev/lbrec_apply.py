"""로비: 지난 생 · 서번트 도감 · 업적(· 보낸 조)을 「이 밤의 이야기와 규칙」처럼 배경 위에 펼친다 (A안 · 11-13).
보낸 조가 있으면: 소식은 「이 밤의 이야기와 규칙」 옆 작은 알림, 버튼 줄에 「보낸 조」, 알림 켜고 끄기는 보낸 조 탭 머리글 옆.
lobby_apply.py 뒤에 쓴다. 사용: python3 lbrec_apply.py <game.html>"""
import sys
CSS = r'''
/* ---- 기록 화면: 밤하늘 위에 어두운 막을 깔고 띄운다 ---- */
#lbRec{position:fixed;inset:0;z-index:45;overflow:hidden}
#lbRec[hidden]{display:none}
#lbRec .ab-veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,6,14,.80),rgba(6,6,14,.68) 40%,rgba(6,6,14,.88));opacity:0;transition:opacity .45s}
#lbRec.open .ab-veil{opacity:1}
#lbRec .rec-in{position:relative;height:100%;overflow-y:auto;overscroll-behavior:contain;box-sizing:border-box;opacity:0;transform:translateY(12px);transition:opacity .45s,transform .45s}
#lbRec.open .rec-in{opacity:1;transform:none}
#lbRec .past{margin:0 auto;max-width:1180px;background:none;box-sizing:border-box;padding-top:0;padding-bottom:max(56px,calc(env(safe-area-inset-bottom,0px) + 40px));padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
/* 탭은 위에 붙어 따라온다. 닫기는 탭 줄 오른쪽 끝 */
#lbRec .vtabs{position:sticky;top:0;z-index:3;margin:0 -4px 18px;padding:max(16px,calc(env(safe-area-inset-top,0px) + 12px)) 52px 12px 4px;background:linear-gradient(180deg,rgba(9,8,15,.94) 70%,rgba(9,8,15,0))}
#lbRec .ab-x{position:fixed;top:max(14px,calc(env(safe-area-inset-top,0px) + 10px));right:max(14px,calc(env(safe-area-inset-right,0px) + 10px));width:36px;height:36px;border-radius:999px;border:1px solid var(--line);background:rgba(18,16,25,.7);color:var(--dim);font-size:14px;cursor:pointer;z-index:4}
#lbRec .ab-x:hover{color:var(--text)}
/* 카드는 반투명하게: 뒤의 하늘이 살짝 비친다 */
#lbRec .past-item,#lbRec .dx,#lbRec .dex-item,#lbRec .ach,#lbRec .ach-item,#lbRec .sent-item{background:rgba(26,23,36,.74);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
body.lb-rec #intro.lb .lb-screen{opacity:0;transition:opacity .45s;pointer-events:none}

/* 보낸 조: 소식은 「이 밤의 이야기와 규칙」 옆 작은 알림으로, 알림 켜고 끄기는 보낸 조 탭 안으로 */
#intro.lb #ghNews{display:none!important}
#intro.lb .lb-morerow{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-top:12px}
#intro.lb .lb-morerow .lb-more{margin-top:0}
#intro.lb .lb-news{display:inline-flex;align-items:center;gap:7px;padding:4px 11px 4px 9px;border-radius:999px;border:1px solid rgba(201,164,92,.5);background:rgba(30,24,20,.72);color:var(--gold2);font:inherit;font-size:12px;line-height:1.3;cursor:pointer;text-shadow:0 1px 6px #08060e}
#intro.lb .lb-news[hidden]{display:none}
#intro.lb .lb-news:hover{border-color:var(--gold)}
#intro.lb .lb-news i{width:6px;height:6px;flex:none;border-radius:50%;background:var(--seal,#e58b93)}
#intro.lb .lb-news b{font-weight:500;color:var(--text);font-variant-numeric:tabular-nums}
#intro.lb .lb-news .ar{color:var(--dim)}
#intro.lb .lb-row.n4 .btn{font-size:13px;padding-inline:4px}
#paneSent .past-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px}
#paneSent #ghnRow{margin:0 0 0 auto}
#paneSent #ghnRow .pn-btn{font-size:12.5px;padding:5px 12px}
@media (prefers-reduced-motion:reduce){#lbRec .ab-veil,#lbRec .rec-in{transition:none}}
'''
JS = r'''
// ---- 기록 화면(지난 생 · 도감 · 업적 · 보낸 조): 로비 버튼 아래로 붙던 것을 배경 위에 펼친다 ----
(()=>{ const $q=s=>document.querySelector(s), intro=$q('#intro'), pw=$q('#pastWrap'); if(!intro||!pw||typeof LOBBY==='undefined') return;
  const TX={ko:{c:'닫기',t:'지난 기록'},en:{c:'Close',t:'Records'},ja:{c:'閉じる',t:'これまでの記録'}}[typeof LANG==='string'?LANG:'ko']||{c:'닫기',t:'지난 기록'};
  const sec=document.createElement('section'); sec.id='lbRec'; sec.hidden=true; sec.setAttribute('role','dialog'); sec.setAttribute('aria-modal','true'); sec.setAttribute('aria-label',TX.t);
  const veil=document.createElement('div'); veil.className='ab-veil';
  const inn=document.createElement('div'); inn.className='rec-in'; inn.tabIndex=-1;
  const x=document.createElement('button'); x.type='button'; x.className='ab-x'; x.textContent='✕'; x.setAttribute('aria-label',TX.c); x.title=TX.c;
  inn.append(x,pw); sec.append(veil,inn); document.body.appendChild(sec);
  let tm=0, back=null;
  const open=()=>{ if(pw.classList.contains('hidden')) return; clearTimeout(tm); if(sec.hidden) back=document.activeElement; sec.hidden=false; document.body.classList.add('lb-rec'); inn.scrollTop=0;
    requestAnimationFrame(()=>requestAnimationFrame(()=>{ sec.classList.add('open'); inn.focus({preventScroll:true}); })); };
  const close=(now)=>{ if(sec.hidden) return; sec.classList.remove('open'); document.body.classList.remove('lb-rec'); clearTimeout(tm);
    if(now===true){ sec.hidden=true; return; } tm=setTimeout(()=>{ sec.hidden=true; },480); if(back&&back.focus) try{ back.focus({preventScroll:true}); }catch(e){} };
  x.onclick=close; veil.onclick=close;
  addEventListener('keydown',e=>{ if(e.key==='Escape'&&!sec.hidden&&!document.querySelector('.dlg:not(.hidden)')){ e.stopPropagation(); close(); } },true);
  // 로비의 도감 · 지난 생 · 업적 단추, 「새 업적」, 「보낸 조 탭에서 모두 보기」: 원래 하던 일(탭 고르기)을 한 뒤 펼친다
  document.addEventListener('click',e=>{ const t=e.target.closest&&e.target.closest('.lb-row .btn,#achNewBtn,#ghnMore'); if(t&&!intro.classList.contains('hidden')) setTimeout(open,0); },true);
  // 로비를 떠나면 바로 닫는다. 지난 생 카드로 그 생의 기록을 보러 간 것이면, 돌아왔을 때 다시 펼친다
  let reopen=false;
  new MutationObserver(()=>{ if(intro.classList.contains('hidden')){ reopen=!sec.hidden&&!!$q('#ending:not(.hidden)'); close(true); } else if(reopen){ reopen=false; setTimeout(open,30); } }).observe(intro,{attributes:true,attributeFilter:['class']});

  // ---- 보낸 조 (보낸 적이 있는 사람만) ----
  const acts=$q('#intro .lb-acts'), row=$q('#intro .lb-row'), gr=$q('#ghnRow');
  const pill=document.createElement('button'); pill.type='button'; pill.className='lb-news'; pill.hidden=true;
  pill.innerHTML='<i aria-hidden="true"></i><span>다른 성배전쟁에서 온 소식</span><b></b><span class="ar" aria-hidden="true">›</span>';
  // 제목 아래 「이 밤의 이야기와 규칙」 옆에 둔다(버튼 묶음을 밀어내지 않게)
  { const mo=$q('#intro .lb-more'); if(mo){ const r=document.createElement('div'); r.className='lb-morerow'; mo.parentNode.insertBefore(r,mo); r.append(mo,pill); } else if(acts) acts.insertBefore(pill,acts.firstChild); }
  pill.onclick=()=>{ VT='sent'; renderVT(); open(); };
  const sb=document.createElement('button'); sb.type='button'; sb.className='btn'; sb.dataset.v='sent'; sb.textContent='보낸 조'; sb.hidden=true;
  sb.onclick=()=>{ VT='sent'; renderVT(); }; if(row) row.appendChild(sb);
  const upd=()=>{ let n=0, on=false; try{ on=API_OK&&sentOn(); n=API_OK&&!gnQuiet()?GN.list.filter(gnUnseen).length:0; }catch(e){}
    const ph=pill.hidden; pill.hidden=!n; pill.querySelector('b').textContent=n;
    const sh=sb.hidden; sb.hidden=!on; if(row) row.classList.toggle('n4',on);
    if((ph!==pill.hidden||sh!==sb.hidden)&&LOBBY.active) requestAnimationFrame(()=>LOBBY.fit()); };
  // 알림 켜고 끄기: 보낸 조 탭 머리글 옆으로. 탭을 다시 그리면(innerHTML) 빠지므로 그때마다 다시 붙인다
  const ps=$q('#paneSent'); const putGr=()=>{ const hd=ps&&ps.querySelector('.past-head'); if(gr&&hd&&gr.parentNode!==hd){ hd.appendChild(gr); try{ ghNewsRow(); }catch(e){} } };
  if(ps) new MutationObserver(putGr).observe(ps,{childList:true});
  ['#ghNews','#vtabs'].forEach(k=>{ const n=$q(k); if(n) new MutationObserver(upd).observe(n,{childList:true,attributes:true,attributeFilter:['class']}); });
  new MutationObserver(upd).observe(intro,{attributes:true,attributeFilter:['class']});
  if(gr&&ps) ps.appendChild(gr); upd(); putGr();
})();
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    k = s.index('(() => {\nconst $=s=>document.querySelector(s);'); e = s.index('</script>', k); b = s.rindex('})();', k, e)
    s = s[:b] + JS + '\n' + s[b:]
    open(P, 'w', encoding='utf-8').write(s)
    print('lbrec ok')
