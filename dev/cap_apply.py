"""11-14: 결과 화면 — 조 목록 초상화 · 캡처하기
- 성배전쟁 기록의 조 목록 이름 왼쪽에 서번트 얼굴(PC 36px · 휴대폰 30px), 쓰러진 조는 흐린 회색
- 캡처하기: 한 사람의 기록(지난 생) · 성배전쟁 기록 · 날짜별로 보기 포함을 골라 폭 680px 이미지 한 장으로
  PC는 PNG 내려받기, 휴대폰은 공유 창. html2canvas(public/assets/js, MIT)는 처음 누를 때만 불러온다
  html2canvas가 못 그리는 것(마름모 초상화 · 초승달 · 만다라)은 캡처할 때만 그림으로 바꿔 넣는다
사용: python3 cap_apply.py <game.html>"""
import sys, i18n
D = [('캡처하기', 'Capture', 'キャプチャ'),
     ('기록 캡처', 'Capture Record', '記録をキャプチャ'),
     ('날짜별로 보기 포함', 'Include day-by-day view', '日付ごとの記録を含める'),
     ('고른 부분을 이미지 한 장으로 저장합니다.', 'Saves the selected parts as a single image.', '選んだ部分を一枚の画像として保存します。'),
     ('이미지 저장', 'Save image', '画像を保存'),
     ('만드는 중…', 'Creating…', '作成中…'),
     ('이미지를 만들지 못했습니다', 'Could not create the image', '画像を作成できませんでした'),
     ('이미지를 저장했습니다', 'Image saved', '画像を保存しました'),
     ('닫기', 'Close', '閉じる')]
MOON = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 44 44'%3E%3Cdefs%3E%3Cmask id='m'%3E"
        "%3Crect width='44' height='44' fill='white'/%3E%3Ccircle cx='11' cy='29' r='21' fill='black'/%3E%3C/mask%3E%3C/defs%3E"
        "%3Ccircle cx='22' cy='22' r='22' fill='%23e8ecff' fill-opacity='.75' mask='url(%23m)'/%3E%3C/svg%3E\") center/contain no-repeat")
CSS = ('.pairs-t .pr{display:flex;gap:10px;align-items:flex-start}.pairs-t .pr .pf{--s:36px!important;margin-top:2px}.pairs-t .pr-b{min-width:0}'
       '.pairs-t .pr.off .pf{filter:grayscale(.7);opacity:.6}'
       '@media (max-width:480px){.pairs-t .pr{gap:8px}.pairs-t .pr .pf{--s:30px!important}}'
       '.cap-ov{position:fixed;inset:0;z-index:80;display:grid;place-items:center;background:rgba(8,6,12,.72);padding:16px}'
       '.cap-box{width:min(380px,100%);background:var(--panel);border:1px solid var(--line);border-top:2px solid var(--gold);border-radius:var(--r);padding:20px 20px 16px;display:grid;gap:10px}'
       '.cap-box h3{margin:0 0 4px;font-family:var(--f-display);font-size:20px}'
       '.cap-box label{display:flex;gap:10px;align-items:center;font-size:14.5px;cursor:pointer}.cap-box label.sub{margin-left:26px;font-size:13.5px;color:var(--dim)}'
       '.cap-box input{accent-color:var(--gold);width:16px;height:16px}.cap-box .note{margin:2px 0 0;font-size:12.5px;color:var(--dim)}'
       '.cap-box .row{display:flex;gap:8px;justify-content:flex-end;margin-top:6px}'
       '.cap-stage{position:fixed;left:-20000px;top:0;width:680px;padding:28px 24px 18px;background:var(--bg);display:grid;gap:0}'
       '.cap-stage .record,.cap-stage .report{max-width:none;margin-left:0;margin-right:0}.cap-stage .record::after{animation:none!important}'
       '.cap-stage .record.rmoon{background:var(--panel);border:1px solid rgba(207,214,255,.42);border-top:2px solid #e86aa8}'
       '.cap-stage .record::after{content:none!important}.cap-stage .deco{position:absolute;z-index:0;pointer-events:none}'
       '.cap-ft{margin-top:16px;text-align:center;font-family:var(--f-mono);font-size:11.5px;letter-spacing:.08em;color:var(--dim)}.cap-ft b{color:var(--gold2);font-weight:500}')
JS = r'''
/* ---- 결과 화면 캡처 ---- */
let H2C=null;
function h2cLoad(){ if(window.html2canvas) return Promise.resolve(window.html2canvas); if(H2C) return H2C;
  H2C=new Promise((ok,no)=>{ const sc=document.createElement('script'); sc.src='assets/js/html2canvas.min.js'; sc.onload=()=>ok(window.html2canvas); sc.onerror=()=>{ H2C=null; no(new Error('load')); }; document.head.appendChild(sc); }); return H2C; }
function capOpen(r,fromHistory){
  const ov=document.createElement('div'); ov.className='cap-ov'; ov.setAttribute('role','dialog'); ov.setAttribute('aria-modal','true');
  const war=!!(r.hero&&r.wd);
  ov.innerHTML=`<div class="cap-box"><h3>기록 캡처</h3>
    <label><input type="checkbox" id="capRec" checked> ${fromHistory?'지난 생':'한 사람의 기록'}</label>
    ${war?`<label><input type="checkbox" id="capWar" checked> 성배전쟁 기록</label><label class="sub"><input type="checkbox" id="capTl"> 날짜별로 보기 포함</label>`:''}
    <p class="note">고른 부분을 이미지 한 장으로 저장합니다.</p>
    <div class="row"><button class="btn" id="capNo" type="button">닫기</button><button class="btn primary" id="capGo" type="button">이미지 저장</button></div></div>`;
  document.body.appendChild(ov);
  const q=s=>ov.querySelector(s), close=()=>{ ov.remove(); document.removeEventListener('keydown',esc_); }, esc_=e=>{ if(e.key==='Escape') close(); };
  document.addEventListener('keydown',esc_); ov.onclick=e=>{ if(e.target===ov) close(); }; q('#capNo').onclick=close;
  const sync=()=>{ const w=q('#capWar'), t=q('#capTl'); if(w&&t){ t.disabled=!w.checked; t.closest('label').style.opacity=w.checked?1:.45; } q('#capGo').disabled=!(q('#capRec').checked||(w&&w.checked)); };
  ov.querySelectorAll('input').forEach(i=>i.onchange=sync); sync(); q('#capGo').focus();
  q('#capGo').onclick=async()=>{ const b=q('#capGo'); b.disabled=true; b.textContent='만드는 중…';
    try{ await capMake(r,{rec:q('#capRec').checked,war:!!(q('#capWar')&&q('#capWar').checked),tl:!!(q('#capTl')&&q('#capTl').checked)}); close(); }
    catch(e){ console.error(e); b.disabled=false; b.textContent='이미지 저장'; toast('이미지를 만들지 못했습니다'); } };
}
const CAP_MOON="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='44' viewBox='0 0 44 44'%3E%3Cdefs%3E%3Cmask id='m'%3E%3Crect width='44' height='44' fill='white'/%3E%3Ccircle cx='11' cy='29' r='21' fill='black'/%3E%3C/mask%3E%3C/defs%3E%3Ccircle cx='22' cy='22' r='22' fill='%23e8ecff' fill-opacity='.75' mask='url(%23m)'/%3E%3C/svg%3E";
const capImgC={};
function capImg(u){ return capImgC[u]||(capImgC[u]=new Promise(ok=>{ const im=new Image(); im.onload=()=>ok(im); im.onerror=()=>ok(null); im.src=u; })); }
// html2canvas는 clip-path를 그리지 못하므로, 원본 초상화를 캔버스에 마름모로 그려 <img>로 바꿔 넣는다
async function capFaces(src,dst){ const S=[...src.querySelectorAll('.pf')], D=[...dst.querySelectorAll('.pf')]; if(S.length!==D.length) return;
  for(let k=0;k<S.length;k++){ const a=S[k], b=D[k], s=Math.round(a.getBoundingClientRect().width)||0; if(!s) continue;
    const cv=document.createElement('canvas'), q=3; cv.width=cv.height=s*q; const x=cv.getContext('2d'); x.scale(q,q);
    const dia=o=>{ x.beginPath(); x.moveTo(s/2,o); x.lineTo(s-o,s/2); x.lineTo(s/2,s-o); x.lineTo(o,s/2); x.closePath(); };
    const cs=getComputedStyle(a); if(/grayscale/.test(cs.filter)) x.filter=cs.filter; x.fillStyle=cs.backgroundColor; dia(0); x.fill();
    const i=a.querySelector('i'); if(i){ const ic=getComputedStyle(i), pad=Math.max(2,s*.035), w=s-2*pad; x.save(); dia(pad); x.clip(); x.fillStyle=ic.backgroundColor; x.fillRect(0,0,s,s);
      const m=ic.backgroundImage.match(/url\("?([^")]+)"?\)/), im=m?await capImg(m[1]):null;
      if(im){ if(ic.backgroundSize==='cover'){ const z=Math.max(w/im.width,w/im.height), dw=im.width*z, dh=im.height*z; x.drawImage(im,pad+(w-dw)/2,pad+(w-dh)/2,dw,dh); }
        else { const sz=ic.backgroundSize.split(' ').map(v=>parseFloat(v)/100), bw=w*sz[0], bh=w*(sz[1]||sz[0]), ps=ic.backgroundPosition.split(' ').map(v=>parseFloat(v)/100); x.drawImage(im,pad+(w-bw)*ps[0],pad+(w-bh)*ps[1],bw,bh); } }
      x.restore(); }
    const img=new Image(); img.src=cv.toDataURL(); img.width=img.height=s; img.style.cssText='width:'+s+'px;height:'+s+'px;display:block;flex:none;opacity:'+cs.opacity+';margin-top:'+cs.marginTop; b.replaceWith(img); } }
async function capMake(r,o){
  const h2c=await h2cLoad(); const E=$('#ending'), st=document.createElement('div'); st.className='cap-stage'; const src=[];
  if(o.rec){ const a=E.querySelector('.record'); src.push(a); const k=a.cloneNode(true); st.appendChild(k);
    // ::after 장식(초승달 · 만다라)은 html2canvas가 크기를 못 맞추므로 실제 그림으로 바꿔 넣는다
    if(a.classList.contains('rmoon')){ const m=document.createElement('img'); m.className='deco'; m.src=CAP_MOON; m.style.cssText='right:30px;top:26px;width:44px;height:44px;opacity:'+(a.classList.contains('far')?.5:1); k.prepend(m); }
    if(a.classList.contains('rdream')){ const u=(getComputedStyle(a,'::after').backgroundImage.match(/url\("?(.+?)"?\)$/)||[])[1]; if(u){ const m=document.createElement('img'); m.className='deco'; m.src=u.replace("viewBox=","width='330' height='330' viewBox="); m.style.cssText='right:-90px;top:-80px;width:330px;height:330px;opacity:.1'; k.prepend(m); } } }
  if(o.war){ const c=E.querySelector('.report'); if(c){ src.push(c); const k=c.cloneNode(true); k.querySelectorAll('.gh-rep').forEach(x=>x.remove());
    const d=k.querySelector('details'); if(d){ if(o.tl) d.open=true; else { const h=d.previousElementSibling; if(h&&h.tagName==='H4') h.remove(); d.remove(); } } st.appendChild(k); } }
  const ft=document.createElement('div'); ft.className='cap-ft'; ft.innerHTML='<b>성배가 차는 밤</b> · holygrailwargame.cupnight.workers.dev'; st.appendChild(ft);
  document.body.appendChild(st);
  try{ await (document.fonts&&document.fonts.ready);
    const kids=[...st.children]; for(let j=0;j<src.length;j++) await capFaces(src[j],kids[j]);
    const h=st.scrollHeight, sc=Math.max(1,Math.min(2,14000/h));
    const bg=getComputedStyle(document.body).backgroundColor||'#0e0c12';
    const cv=await h2c(st,{backgroundColor:bg,scale:sc,logging:false,useCORS:true,windowWidth:680});
    const blob=await new Promise(ok=>cv.toBlob(ok,'image/png'));
    const nm=`cupnight_${r.born||''}-${r.died||''}_${(r.ts||Date.now()).toString(36).slice(-4)}.png`; // 한글 파일 이름은 일부 브라우저가 'download'로 바꿔 버린다
    const f=new File([blob],nm,{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[f]})&&matchMedia('(pointer:coarse)').matches){ try{ await navigator.share({files:[f]}); return; }catch(e){ if(e&&e.name==='AbortError') return; } }
    const u=URL.createObjectURL(blob), a=document.createElement('a'); a.href=u; a.download=nm; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(u),4000); toast('이미지를 저장했습니다');
  } finally { st.remove(); }
}
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp(".pairs-t .st.alive{color:var(--moss)}", ".pairs-t .st.alive{color:var(--moss)}" + CSS)
    rp('const rows=`<tr class="me"><td class="c">${esc(my.cls)}</td><td>${esc(my.name)}<br><span class="st">당신</span></td>',
       'const pf=(id,nm)=>{ const hid=nm?hidOf(id,nm):null; return faceHtml(hid,36,{unk:!hid}); };\n  const rows=`<tr class="me"><td class="c">${esc(my.cls)}</td><td><div class="pr${my.alive?\'\':\' off\'}">${pf(my.id,my.name)}<div class="pr-b">${esc(my.name)}<br><span class="st">당신</span></div></div></td>')
    rp('return `<tr><td class="c">${esc(p.cls)}</td><td>${p.hero?esc(p.hero)',
       'return `<tr><td class="c">${esc(p.cls)}</td><td><div class="pr${p.alive?\'\':\' off\'}">${pf(p.id,p.hero)}<div class="pr-b">${p.hero?esc(p.hero)')
    rp(":''}</span>`:''}</td><td>${pst(p)}</td></tr>`", ":''}</span>`:''}</div></div></td><td>${pst(p)}</td></tr>`")
    rp('<button class="btn" id="copyBtn">기록 복사</button>', '<button class="btn" id="copyBtn">기록 복사</button><button class="btn" id="capBtn">캡처하기</button>')
    rp("  $('#homeBtn').onclick=showIntro;\n", "  $('#homeBtn').onclick=showIntro;\n  $('#capBtn').onclick=()=>capOpen(r,fromHistory);\n")
    rp("let TOAST_QUIET=false;", JS.strip('\n') + "\nlet TOAST_QUIET=false;")
    s, nd, nt = i18n.add(s, D)
    print('cap miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
