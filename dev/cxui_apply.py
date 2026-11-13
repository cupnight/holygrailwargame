"""후반 위기 현판(11-13): 조 목록 맨 위의 위기 줄을 위기마다 컨셉을 살린 작은 현판으로, 위기 쪽 조 목록도 같은 색으로.
검은 성배: 검은 잔 · 흘러내리는 진흙 · 진흙 방울 / 비스트 봉인: BB의 육각 봉인 · 주사선 · 모서리 괄호 / 비어 있는 성배: 점선 잔 / 비스트 강림: 연꽃 · 분홍 빛무리
bxscn_apply.py 뒤에 쓴다. 사용: python3 cxui_apply.py <game.html>"""
import sys, i18n
CSS = r'''
/* ---- 후반 위기 현판 ---- */
#pairs .cxb{grid-column:1/-1;display:flex;align-items:center;gap:10px;margin:0 0 8px;padding:9px 12px;border-radius:10px;position:relative;overflow:hidden}
#pairs .cxb svg{width:26px;height:26px;flex:none}
#pairs .cxb .t{display:grid;gap:1px;min-width:0}#pairs .cxb .n{font-size:14px;letter-spacing:.02em}#pairs .cxb .ph{font-size:11.5px;letter-spacing:.12em;opacity:.8}
#pairs .cxb .mt{margin-left:auto;display:flex;gap:4px;align-items:center}
/* 검은 성배: 아래로 흘러내리는 진흙 */
#pairs .cxb.k-black{background:linear-gradient(180deg,#1b0d1c,#120812);border:1px solid #4a1a30;box-shadow:inset 0 -10px 18px -10px #000}
#pairs .cxb.k-black .n{font-family:var(--f-display,serif);color:#e4a9b9;text-shadow:0 0 10px rgba(160,30,70,.55)}#pairs .cxb.k-black .ph{color:#b06a82}
#pairs .cxb.k-black::after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:9px;background:radial-gradient(5px 7px at 12% 0,#0a0409 98%,transparent),radial-gradient(4px 9px at 31% 0,#0a0409 98%,transparent),radial-gradient(6px 6px at 58% 0,#0a0409 98%,transparent),radial-gradient(3px 8px at 77% 0,#0a0409 98%,transparent),radial-gradient(5px 6px at 92% 0,#0a0409 98%,transparent);opacity:.9}
#pairs .cxb.k-black .mt i{width:8px;height:11px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;clip-path:polygon(50% 0,100% 62%,92% 88%,50% 100%,8% 88%,0 62%);background:#2a1522;border:1px solid #5a2238}
#pairs .cxb.k-black .mt i.on{background:linear-gradient(180deg,#7a1838,#230712);border-color:#b23a62;box-shadow:0 0 6px rgba(178,58,98,.6)}
/* 봉인된 성배: BB의 봉인 — 보랏빛 육각 · 모서리 괄호 · 주사선 */
#pairs .cxb.k-seal{background:repeating-linear-gradient(0deg,rgba(201,155,255,.05) 0 1px,transparent 1px 3px),linear-gradient(135deg,#1c1430,#140f22);border:1px solid #5b3f8c}
#pairs .cxb.k-seal::before,#pairs .cxb.k-seal::after{content:'';position:absolute;width:10px;height:10px;border-color:#c99bff;border-style:solid}
#pairs .cxb.k-seal::before{left:4px;top:4px;border-width:1.5px 0 0 1.5px}#pairs .cxb.k-seal::after{right:4px;bottom:4px;border-width:0 1.5px 1.5px 0}
#pairs .cxb.k-seal .n{font-family:var(--f-mono,monospace);color:#e3cdff;letter-spacing:.08em}#pairs .cxb.k-seal .ph{color:#a88bd4}
#pairs .cxb.k-seal .mt i,#pairs .cxb.k-empty .mt i{width:10px;height:11px;clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);background:#33285a}
#pairs .cxb.k-seal .mt i.on{background:#b98cff;box-shadow:0 0 6px #b98cff}
/* 비어 있는 성배: 옅은 점선 */
#pairs .cxb.k-empty{background:linear-gradient(135deg,#221626,#17111d);border:1px dashed #8f5b78}
#pairs .cxb.k-empty .n{color:#f0c4da}#pairs .cxb.k-empty .ph{color:#b98aa3}#pairs .cxb.k-empty .mt i.on{background:#f0a6c8}
/* 비스트 Ⅲ/R: 연꽃 · 분홍 빛무리 */
#pairs .cxb.k-beast{background:radial-gradient(120% 140% at 0% 50%,rgba(255,160,205,.22),transparent 60%),linear-gradient(135deg,#2a1528,#1a0f1d);border:1px solid #a85a86;box-shadow:0 0 18px -6px rgba(255,140,200,.55)}
#pairs .cxb.k-beast .n{font-family:var(--f-display,serif);color:#ffd3e8;text-shadow:0 0 10px rgba(255,150,205,.7)}#pairs .cxb.k-beast .ph{color:#e7a3c4}
#pairs .cxb.k-beast .mt i{width:9px;height:12px;border-radius:50% 50% 50% 50%/70% 70% 30% 30%;background:#4b2440}
#pairs .cxb.k-beast .mt i.on{background:linear-gradient(180deg,#ffd6ea,#ff8fc2);box-shadow:0 0 6px #ff9ccb}
/* 위기 쪽 조 목록 */
#pairs .pair-sep.k-black{color:#c27088}#pairs .pair-sep.k-seal{color:#b597e6;font-family:var(--f-mono,monospace)}#pairs .pair-sep.k-beast,#pairs .pair-sep.k-empty{color:#f0a6c8}
#pairs .pair.cxu.k-black{border-left:3px solid #7a1838;background:linear-gradient(90deg,rgba(60,10,30,.35),transparent 40%)}
#pairs .pair.cxu.k-seal{border-left:3px solid #8a5cd6;background:linear-gradient(90deg,rgba(110,70,190,.18),transparent 40%)}
#pairs .pair.cxu.k-beast,#pairs .pair.cxu.k-empty{border-left:3px solid #e07fb0;background:linear-gradient(90deg,rgba(230,110,170,.16),transparent 40%)}
'''
HELP = r'''const CX_IC={
 black:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h14c0 5-2.6 8.2-6 9v4.2c2 .3 3.6 1.3 3.6 2.6H7.4c0-1.3 1.6-2.3 3.6-2.6V12C7.6 11.2 5 8 5 3z" fill="#0d0710" stroke="#a03657" stroke-width="1.2"/><path d="M8.2 6.5c.2 2.4 1.6 4 3.8 4.4" fill="none" stroke="#5a1a33" stroke-width="1"/><path d="M15.6 9.6c.6 1.2.9 2.4.9 3.4a1.2 1.2 0 0 1-2.4 0c0-.9.6-2.1 1.5-3.4z" fill="#3a0a1e" stroke="#a03657" stroke-width=".8"/></svg>',
 seal:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l8.2 4.75v9.5L12 21.5l-8.2-4.75v-9.5z" fill="none" stroke="#c99bff" stroke-width="1.3"/><path d="M12 6l5.2 3v6L12 18l-5.2-3V9z" fill="rgba(170,110,255,.16)" stroke="#c99bff" stroke-width=".7" stroke-dasharray="1.6 1.4"/><circle cx="12" cy="11" r="1.6" fill="#e9d6ff"/><path d="M11.2 12.2h1.6l.5 3h-2.6z" fill="#e9d6ff"/></svg>',
 empty:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h14c0 5-2.6 8.2-6 9v4.2c2 .3 3.6 1.3 3.6 2.6H7.4c0-1.3 1.6-2.3 3.6-2.6V12C7.6 11.2 5 8 5 3z" fill="none" stroke="#f0b6d2" stroke-width="1.2" stroke-dasharray="2 1.6"/></svg>',
 beast:'<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="rgba(255,170,210,.22)" stroke="#ffb3d6" stroke-width="1"><path d="M12 4c2 2.4 2.4 5.6 0 9.2C9.6 9.6 10 6.4 12 4z"/><path d="M5 8.4c3 .3 5.4 2.3 6.4 5.6C8 13.6 5.8 11.6 5 8.4z"/><path d="M19 8.4c-3 .3-5.4 2.3-6.4 5.6 3.4-.4 5.6-2.4 6.4-5.6z"/><path d="M3.6 14.4c2.8-.8 5.8 0 8 1.8-2.8 1.3-6 .8-8-1.8z"/><path d="M20.4 14.4c-2.8-.8-5.8 0-8 1.8 2.8 1.3 6 .8 8-1.8z"/></g><path d="M7 19.5h10" stroke="#ffb3d6" stroke-width="1" stroke-linecap="round"/></svg>'};
const cxKind=c=>c.type!=='beast3R'?'black':c.stage>=3?'beast':c.noBB?'empty':'seal';
// 조 목록 맨 위의 위기 현판: 상징 · 이름 · 단계 · 진행 표시 세 칸
function cxBanner(w){ const c=w.crisis; if(!c||!c.stage||!(w.cupKnown||c.stage>=2)) return ''; const k=cxKind(c);
  const nm={black:'검은 성배',seal:'봉인된 성배',empty:'비어 있는 성배',beast:'비스트 Ⅲ/R'}[k];
  const ph=k==='black'?['','징조','범람','강림'][c.stage]+(c.zones&&c.zones.length?` · 오염 구역 ${c.zones.join(', ')}`:''):k==='beast'?'강림':k==='seal'?'봉인 중':'성배가 차오르는 중';
  return `<div class="cxb k-${k}">${CX_IC[k]}<span class="t"><span class="n">${nm}</span><span class="ph">${ph}</span></span><span class="mt" aria-label="${c.stage}/3">${[1,2,3].map(i=>`<i class="${c.stage>=i?'on':''}"></i>`).join('')}</span></div>`; }
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    rp('function render(){', HELP + 'function render(){')
    a = s.index('    { const cxl=(()=>{ const c=w.crisis;'); b = s.index('// 후반 위기 줄은 조 목록 맨 위에', a) + len('// 후반 위기 줄은 조 목록 맨 위에')
    s = s[:a] + "    { const cxl=cxBanner(w); if(cxl) rowsP.unshift(cxl); } // 후반 위기 현판은 조 목록 맨 위에" + s[b:]
    rp("""rowsP.push(`<div class="pair-sep">${bx?""", """const kk=cxKind(w.crisis); rowsP.push(`<div class="pair-sep k-${kk}">${bx?""")
    rp("""rowsP.push(`<button class="pair cxu ${u.alive?'':'out'}" data-i="${u.i}">""", """rowsP.push(`<button class="pair cxu k-${kk} ${u.alive?'':'out'}" data-i="${u.i}">""")
    s, nd, nt = i18n.add(s, [('봉인 중','Sealed','封印中'),('성배가 차오르는 중','The Grail is filling','聖杯が満ちつつある')])
    print('cxui miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
