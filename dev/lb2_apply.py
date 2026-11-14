"""로비 두 단계 (11-14): ① 배경 + 제목 + 「- Press to Start -」 → 누르면 ② 시작 기능.
- 화면 비율로 배치를 나눈다: 가로가 세로의 1.15배를 넘으면 왼쪽 띠(높이 520 미만이면 압축), 아니면 카드형
- 2단계: 이어하기 · 태어나기(성별) · 인연 소환 · 도감 · 지난 생 · 업적 · 링크 · 처음 화면 · UI 숨기기
- 고풍 스타일: 모서리를 깎은 남색 판 + 은 · 금 이중 테두리 + 모서리 마름모 (어둡게, 질감 옅게)
- 인연 소환: 누르면 바로 전체 목록. 위쪽에 「최근 인연 소환」(폭에 맞춰 최대 8명), 고르면 바로 닫힘. 계약한 서번트가 없으면 잠김으로 보여 준다
- 최근 인연 소환은 8명까지 기억한다(전에는 3명)
사용: python3 lb2_apply.py <game.html>"""
import sys
from urllib.parse import quote


def svg(g1, g2, op, s1, s2, sw, inner, dia, nz):
    x = (f"<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'><defs>"
         f"<linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{g1}' stop-opacity='{op}'/><stop offset='1' stop-color='{g2}' stop-opacity='{op}'/></linearGradient>"
         f"<linearGradient id='s' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{s1}'/><stop offset='.5' stop-color='{s2}'/><stop offset='1' stop-color='{s1}'/></linearGradient>"
         f"<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='3'/><feColorMatrix values='0 0 0 0 .85  0 0 0 0 .78  0 0 0 0 .6  0 0 0 {nz} 0'/><feComposite in2='SourceGraphic' operator='in'/></filter></defs>"
         f"<path d='M7 .7H41L47.3 7V41L41 47.3H7L.7 41V7Z' fill='url(#g)'/>"
         f"<path d='M7 .7H41L47.3 7V41L41 47.3H7L.7 41V7Z' fill='#000' filter='url(#n)'/>"
         f"<path d='M7 .7H41L47.3 7V41L41 47.3H7L.7 41V7Z' fill='none' stroke='url(#s)' stroke-width='{sw}'/>"
         f"<path d='M8.5 3.6H39.5L44.4 8.5V39.5L39.5 44.4H8.5L3.6 39.5V8.5Z' fill='none' stroke='{inner}' stroke-width='.8'/>"
         f"<path d='M3.6 3.6l1.6 1.6-1.6 1.6-1.6-1.6zM44.4 3.6l1.6 1.6-1.6 1.6-1.6-1.6zM3.6 41.2l1.6 1.6-1.6 1.6-1.6-1.6zM44.4 41.2l1.6 1.6-1.6 1.6-1.6-1.6z' fill='{dia}'/></svg>")
    return 'url("data:image/svg+xml,' + quote(x, safe='') + '")'


PL = svg('#0f1426', '#070a15', .9, '#7a7568', '#b9b19c', 1.2, 'rgba(196,164,104,.42)', '#b39660', .035)
PR = svg('#1a2342', '#0d1229', 1, '#968b6e', '#d8cfb4', 1.5, 'rgba(212,180,112,.65)', '#cdb072', .04)
TG = svg('#0e1322', '#070913', .92, '#6c685d', '#a8a08c', 1.05, 'rgba(190,160,100,.32)', '#a08655', .035)
PN = svg('#0c1021', '#060811', .96, '#7a7568', '#b9b19c', 1.2, 'rgba(196,164,104,.4)', '#b39660', .035)


def pc(v, bw, iw):
    return (f"border:{bw}px solid transparent!important;border-image:var({v}) 14 fill / {iw}px / 0 stretch!important;"
            "background:none!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;")


PLc, PRc, TGc, PNc = pc('--lbPL', 10, 14), pc('--lbPR', 10, 14), pc('--lbTG', 7, 12), pc('--lbPN', 12, 16)
UL = "content:'';position:absolute;left:22%;right:22%;bottom:2px;height:1px;background:linear-gradient(90deg,transparent,#d8bd7c,transparent)"
DIA = "background:linear-gradient(135deg,#f2e2b4,#b8975a);box-shadow:0 0 5px rgba(220,190,120,.6)"
NOPL = "border:0!important;border-image:none!important;filter:none!important;"

CSS = f'''
/* ---- 로비 두 단계 · 고풍 스타일 (lb2_apply) ---- */
:root{{--lbPL:{PL};--lbPR:{PR};--lbTG:{TG};--lbPN:{PN};--lbF:'Gowun Batang','Nanum Myeongjo',serif}}
#intro.lb #bondPanel{{display:none!important}}
html[lang=ko] #lb2,html[lang=ko] #lbBond,html[lang=ko] .lb-press{{word-break:keep-all}}
.lb-xo{{position:absolute;left:50%;width:58px;height:9px;transform:translateX(-50%);pointer-events:none;z-index:2;background:linear-gradient(90deg,transparent,rgba(216,189,124,.9) 38%,transparent 38%,transparent 62%,rgba(216,189,124,.9) 62%,transparent) center/100% 1px no-repeat}}
.lb-xo::after{{content:'';position:absolute;left:50%;top:50%;width:7px;height:7px;transform:translate(-50%,-50%) rotate(45deg);{DIA}}}
.lb-xo.t{{top:-15px}}.lb-xo.b{{bottom:-15px}}
/* 1단계 */
.lb-press{{display:none}}
body.lb-on.lb-s1 .lb-press{{display:block;position:fixed;left:0;right:0;bottom:calc(9vh + env(safe-area-inset-bottom,0px));z-index:2;text-align:center;pointer-events:none;color:#f1e6cf}}
body.lb-reading .lb-press,body.lb-rec .lb-press{{display:none!important}}
body.lb-wide .lb-press{{bottom:7vh}}
.lb-press .t{{display:block;font:400 15px var(--lbF);letter-spacing:.34em;text-shadow:0 0 12px rgba(230,200,138,.55),0 2px 6px #000;animation:lbBlink 3.2s ease-in-out infinite}}
body.lb-wide .lb-press .t{{font-size:17px}}
.lb-press small{{display:block;margin-top:8px;font:11px var(--f-ui);letter-spacing:.1em;color:#bdb2c2;text-shadow:0 1px 3px #000}}
.lb-press .xl{{display:block;width:240px;max-width:70vw;height:9px;margin:0 auto 12px;position:relative;background:linear-gradient(90deg,transparent,rgba(216,189,124,.85) 42%,transparent 47%,transparent 53%,rgba(216,189,124,.85) 58%,transparent) center/100% 1px no-repeat}}
.lb-press .xl::after{{content:'';position:absolute;left:50%;top:50%;width:7px;height:7px;transform:translate(-50%,-50%) rotate(45deg);{DIA}}}
@keyframes lbBlink{{0%,100%{{opacity:.22}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.lb-press .t{{animation:none}}}}
#intro.lb .lb-go{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;padding:0;margin:0}}
body.lb-s1 #intro.lb .lb-acts,body.lb-s1 #intro.lb .lb-foot,body.lb-s1 #intro.lb .keys{{display:none!important}}
body.lb-s1 #intro.lb .lb-sp{{min-height:0}}
body.lb-s2 #intro.lb .lb-screen{{display:none!important}}
body.lb-glide #lbStage{{transition:opacity 1.2s,transform .7s cubic-bezier(.3,.7,.2,1)!important}}
body.lb-glide #lbStage .skyg{{transition:transform .7s cubic-bezier(.3,.7,.2,1)}}
body.lb-glide #lobbyBg .lb-fade{{transition:top .7s cubic-bezier(.3,.7,.2,1)}}
/* 1단계 위쪽 단추 */
body.lb-on #intro.lb .lb-top .lang-pick{{{TGc}padding:0 2px!important;filter:drop-shadow(0 2px 4px rgba(0,0,0,.55))}}
body.lb-on #intro.lb .lb-top .lang-pick button{{position:relative;border-radius:0;background:none!important;font-family:var(--lbF);color:#a39c8a}}
body.lb-on #intro.lb .lb-top .lang-pick button.on{{color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.5)}}
body.lb-on #intro.lb .lb-top .lang-pick button.on::after{{{UL}}}
body.lb-on #intro.lb .lb-ico,body.lb-on #intro.lb .lb-top #setBtn,body.lb-on .snd-ask .pn-btn{{{TGc}color:#ddd3bb!important;font-family:var(--lbF);filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
body.lb-on #intro.lb .lb-ico{{width:auto;height:auto;padding:3px!important}}
body.lb-on #intro.lb .lb-ico[aria-pressed=true]{{color:#e6cd8f!important}}
body.lb-on #intro.lb .lb-top #setBtn{{padding:4px 10px!important}}
body.lb-on #intro.lb .lb-top .lang-pick button,body.lb-on #intro.lb .lb-top #setBtn{{white-space:nowrap}}
@media (max-width:400px){{body.lb-on #intro.lb .lb-top .lang-pick button{{padding:4px 8px}}body.lb-on #intro.lb .lb-top #setBtn{{padding:4px 8px!important}}}}
body.lb-on .snd-ask .pn-btn{{padding:3px 12px!important}}
body.lb-on .snd-ask{{{PLc}padding:4px 8px!important;font-family:var(--lbF);color:#d8cfdb}}
/* 2단계 */
#lb2{{display:none}}
body.lb-on.lb-s2 #lb2{{display:block;position:fixed;inset:0;z-index:3;color:var(--text);font-family:var(--lbF)}}
#lb2 button{{font-family:var(--lbF)}}
#lb2 svg{{flex:none}}
#lb2 .l2-ui{{position:absolute;inset:0;transition:opacity .4s}}
#lb2 .l2-dim{{position:absolute;inset:0;pointer-events:none;transition:opacity .4s;background:linear-gradient(180deg,rgba(9,7,13,.38),rgba(9,7,13,.30) 35%,rgba(9,7,13,.52) 75%,rgba(9,7,13,.62))}}
body.lb-wide #lb2 .l2-dim{{display:none}}
body.lb-rec #lb2 .l2-ui,body.lb-reading #lb2 .l2-ui,body.lb-hideui #lb2 .l2-ui,body.lb-hideui #lb2 .l2-dim{{opacity:0;pointer-events:none}}
#lb2 .l2-show{{display:none}}
body.lb-hideui #lb2 .l2-show{{display:flex;align-items:center;gap:6px;position:fixed;z-index:4;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));{TGc}padding:2px 10px 2px 6px!important;color:#ddd3bb;font-size:12.5px;cursor:pointer;filter:drop-shadow(0 2px 4px rgba(0,0,0,.6))}}
#lb2 .l2-show svg{{width:16px;height:16px;color:#d8bd7c}}
#lb2 .l2-tools{{position:absolute;z-index:2;top:calc(14px + env(safe-area-inset-top,0px));right:max(16px,env(safe-area-inset-right,0px));display:flex;gap:6px;align-items:center}}
#lb2 .l2-lang{{display:flex;{TGc}padding:0 2px!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
#lb2 .l2-lang button{{position:relative;background:none;border:0;color:#a39c8a;font-size:12px;padding:5px 8px;cursor:pointer}}
#lb2 .l2-lang button.on{{color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.5)}}
#lb2 .l2-lang button.on::after{{{UL}}}
#lb2 .l2-ib{{display:grid;place-items:center;{TGc}padding:4px!important;color:#d8bd7c;cursor:pointer;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
#lb2 .l2-ib svg{{width:17px;height:17px}}
#lb2 .l2-snd[aria-pressed=false]{{color:#8f8878}}
#lb2 .l2-main{{position:absolute;inset:0;overflow-y:auto;overscroll-behavior:contain;box-sizing:border-box;padding:calc(14px + env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) calc(20px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}}
#lb2 .l2-in{{max-width:440px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
#lb2 .l2-in>*{{min-width:0}}
#lb2 .l2-back{{display:inline-flex;align-items:center;gap:6px;align-self:flex-start;{TGc}padding:2px 9px 2px 5px!important;color:#ddd3bb;font-size:12.5px;cursor:pointer;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
#lb2 .l2-back svg{{width:15px;height:15px;color:#d8bd7c}}
#lb2 .l2-back.p{{display:none}}
#lb2 .l2-back.m{{order:0}}#lb2 .l2-head{{order:1}}#lb2 .l2-slot{{order:2;display:contents}}#lb2 .l2-born{{order:3}}#lb2 .l2-cont{{order:4}}#lb2 .l2-bond{{order:5}}#lb2 .l2-menu{{order:6}}#lb2 .lb-news{{order:7}}#lb2 .l2-links{{order:8}}
#lb2 .l2-bondw,#lb2 .l2-newsw,#lb2 .l2-foot{{display:contents}}
#lb2 .l2-slot>*{{order:2}}
#lb2 .l2-ey,#lb2 .l2-lit{{display:none}}
#lb2 .l2-title{{margin:6px 0 0;font:700 24px/1.25 var(--lbF);color:#f3ead8;letter-spacing:.02em;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
#lb2 .l2-title em{{font-style:normal;color:var(--gold)}}
#lb2 .l2-sub{{margin-top:2px;font-size:12px;color:#d4c9d6;text-shadow:0 1px 4px #000}}
#lb2 .lb-pickrow{{display:flex;flex-wrap:wrap;gap:8px}}
#lb2 .lb-pickrow:not(:has(.pn-btn:not(.hidden))){{display:none}}
#lb2 .l2-born{{position:relative;display:grid;justify-items:center;text-align:center;gap:8px;{PRc}padding:6px 10px 10px!important;margin:8px 0 6px;color:#f6edd3;cursor:pointer;filter:drop-shadow(0 3px 7px rgba(0,0,0,.6)) drop-shadow(0 0 8px rgba(220,190,120,.13))}}
#lb2 .l2-bk{{font-size:10.5px;letter-spacing:.24em;color:#c9ad72}}
#lb2 .l2-bd{{font-size:12px;line-height:1.5;color:#cbbf9f}}
#lb2 #startBtn{{position:relative;background:none!important;border:0!important;box-shadow:none!important;border-radius:0!important;padding:0!important;margin:0!important;width:auto!important;min-width:0!important;height:auto!important;font:700 25px/1.3 var(--lbF)!important;letter-spacing:.18em!important;color:#f6edd3!important;text-shadow:0 1px 0 rgba(0,0,0,.75),0 0 12px rgba(230,200,140,.4);cursor:pointer;transform:none!important}}
#lb2 #startBtn::before,#lb2 #startBtn::after{{content:'✦';display:inline;position:static;inset:auto;width:auto;height:auto;background:none;opacity:1;font-size:.5em;color:#d8bd7c;vertical-align:middle;margin:0 .7em;text-shadow:0 0 6px rgba(220,190,120,.6);animation:none;transform:none}}
#lb2 #startBtn .lb-xo{{display:none}}
#lb2 #sexPick{{display:inline-flex;gap:0;{TGc}padding:0 2px!important;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}}
#lb2 #sexPick button{{position:relative;height:auto;padding:5px 14px;font-size:12.5px;line-height:1.4;color:#a39c8a;background:none!important;border-radius:0;font-family:var(--lbF)}}
#lb2 #sexPick button[aria-pressed=true]{{color:#f3e8cb;text-shadow:0 0 8px rgba(230,200,140,.5)}}
#lb2 #sexPick button[aria-pressed=true]::after{{{UL}}}
#lb2 .l2-cont{{position:relative;display:flex;align-items:center;gap:12px;{PLc}padding:2px 4px!important;color:inherit;font-size:inherit;text-align:left;cursor:pointer;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}}
#lb2 .l2-cont[hidden]{{display:none}}
#lb2 .l2-face{{flex:none;width:42px;height:42px;border-radius:3px;border:1px solid rgba(216,189,124,.6);background:#18141f center/cover no-repeat}}
#lb2 .l2-face[hidden]{{display:none}}
#lb2 .l2-cont .t{{flex:1;min-width:0;display:grid;line-height:1.38}}
#lb2 .l2-cont .k{{font-size:10.5px;letter-spacing:.18em;color:#a39c8a}}
#lb2 .l2-cont b{{font-size:15px;font-weight:700;color:#ece3cc;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
#lb2 .l2-cont small{{font-size:11.5px;color:#c9ad72;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
#lb2 .l2-cont .go,#lb2 .l2-bond .go{{font-size:18px;color:#d8bd7c}}
#lb2 .l2-bond{{position:relative;display:flex;align-items:center;gap:12px;width:100%;box-sizing:border-box;{PLc}padding:2px 6px!important;color:inherit;font-size:inherit;text-align:left;cursor:pointer;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}}
#lb2 .l2-bond>svg{{width:22px;height:22px;color:#d8bd7c}}
#lb2 .l2-bond .t{{flex:1;min-width:0;display:grid;line-height:1.38}}
#lb2 .l2-bond .t b{{font-size:15px;font-weight:700;color:#e2c98e}}
#lb2 .l2-bond .t small{{font-size:11.5px;color:#8f8878}}
#lb2 .l2-bond .pick{{display:grid;justify-items:center;gap:2px;max-width:92px;text-align:center;font-size:10.5px;line-height:1.25;color:#ddd3bb}}
#lb2 .l2-bond .pick .p{{color:#8f8878}}#lb2 .l2-bond .pick .p.s{{color:#e6cd8f}}
#lb2 .l2-bond .r{{display:none}}
#lb2 .l2-bond.lock{{cursor:default}}
#lb2 .l2-bond.lock>svg{{color:#6f6676}}#lb2 .l2-bond.lock .t b{{color:#8f8878}}
#lb2 .l2-bond.lock .r{{display:flex;align-items:center;gap:4px;font-size:11px;color:#7f7685;white-space:nowrap}}
#lb2 .l2-bond.lock .r svg{{width:13px;height:13px}}
#lb2 .l2-bond .r .pc{{display:none}}
#lb2 .lbf{{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#18141f center/cover no-repeat;border:1.5px solid #6b6150;box-shadow:0 0 0 2px rgba(10,12,22,.9),0 0 0 3px rgba(196,164,104,.35);font-style:normal;color:#8f8878;font-size:14px;box-sizing:border-box}}
#lb2 .lbf.on,#lbBond .lbf.on{{border-color:#e6cd8f;box-shadow:0 0 0 2px rgba(10,12,22,.9),0 0 0 3px rgba(230,205,143,.85),0 0 14px rgba(230,200,138,.45)}}
#lb2 .l2-menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}}
#lb2 .l2-menu.n4{{grid-template-columns:repeat(4,minmax(0,1fr))}}
#lb2 .l2-mi{{position:relative;display:grid;justify-items:center;align-content:start;gap:5px;{PLc}padding:6px 2px 4px!important;color:#ece3cc;font-size:13px;line-height:1.3;cursor:pointer;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}}
#lb2 .l2-menu.n4 .l2-mi{{font-size:12px}}
#lb2 .l2-mi svg{{width:24px;height:24px;color:#d8bd7c}}
#lb2 .l2-mi small{{font-size:10.5px;color:#8f8878}}
#lb2 .l2-mi .d{{position:absolute;top:0;right:2px;width:7px;height:7px;border-radius:50%;background:#d2454f}}
#lb2 .l2-mi:disabled{{opacity:.45;cursor:default}}
#lb2 .lb-news{{display:flex;align-items:center;gap:8px;width:100%;box-sizing:border-box;{TGc}padding:4px 10px!important;color:#e2c98e;font-size:13px;text-align:left;cursor:pointer;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
#lb2 .lb-news[hidden]{{display:none}}
#lb2 .lb-news i{{width:7px;height:7px;flex:none;border-radius:50%;background:#d2454f}}
#lb2 .lb-news b{{font-weight:400;color:#ece3cc}}#lb2 .lb-news .ar{{margin-left:auto;color:#d8bd7c}}
#lb2 .l2-links{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}
#lb2 .l2-links .pn-btn{{position:relative;{TGc}padding:3px 8px!important;gap:5px;font-family:var(--lbF);font-size:12px;color:#ddd3bb;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}}
#lb2 .l2-links .pn-btn::before{{background:#d8bd7c}}
#lb2 .l2-links .pn-btn .h{{display:none}}
#lb2 .l2-links .pn-btn.hidden{{display:none}}
#lb2 .l2-keys,#lb2 .l2-ver{{display:none}}
@media (max-width:370px){{#lb2 .l2-lang button{{padding:5px 6px}}#lb2 .l2-tools{{gap:4px}}#lb2 .l2-links .pn-btn{{font-size:11.5px;padding:3px 6px!important}}}}
/* 2단계 · 넓은 화면: 왼쪽 띠 */
body.lb-wide #lb2 .l2-main{{inset:0 auto 0 0;width:380px;padding:40px 34px 28px max(40px,env(safe-area-inset-left,0px));background:linear-gradient(90deg,rgba(6,8,16,.96) 0,rgba(6,8,16,.92) 84%,rgba(6,8,16,0) 100%)}}
body.lb-wide #lb2 .l2-ui::before{{content:'';position:absolute;top:0;bottom:0;left:357px;width:1px;pointer-events:none;background:linear-gradient(180deg,transparent,rgba(216,189,124,.5) 18%,rgba(216,189,124,.5) 82%,transparent)}}
body.lb-wide #lb2 .l2-ui::after{{content:'';position:absolute;left:353.5px;top:50%;width:8px;height:8px;transform:rotate(45deg);pointer-events:none;{DIA}}}
body.lb-wide #lb2 .l2-in{{max-width:none;margin:0;min-height:100%;gap:0}}
body.lb-wide #lb2 .l2-in>*,body.lb-wide #lb2 .l2-bond,body.lb-wide #lb2 .lb-news,body.lb-wide #lb2 .l2-links{{order:0}}
body.lb-wide #lb2 .l2-back.m{{display:none}}
body.lb-wide #lb2 .l2-ey{{display:block;font-size:10.5px;letter-spacing:.26em;color:#a99fad}}
body.lb-wide #lb2 .l2-title{{margin:4px 0 0;font-size:38px;line-height:1.12}}
body.lb-wide #lb2 .l2-sub{{display:none}}
body.lb-wide #lb2 .l2-lit{{display:block;margin-top:10px;font:13px/1.6 var(--f-story);color:#d8cfdb}}
body.lb-wide #lb2 .l2-lit b{{color:var(--gold2);font-weight:400}}
body.lb-wide #lb2 .l2-slot>*{{margin-top:12px}}
body.lb-wide #lb2 .l2-cont{{margin-top:28px;padding:0 6px!important}}
body.lb-wide #lb2 .l2-face{{width:46px;height:46px}}
body.lb-wide #lb2 .l2-cont .t{{display:block}}
body.lb-wide #lb2 .l2-cont .k{{display:block;font-size:16px;font-weight:700;letter-spacing:0;color:#f1e6cf}}
body.lb-wide #lb2 .l2-cont b,body.lb-wide #lb2 .l2-cont small{{display:inline;font-size:11.5px;font-weight:400;color:#c9ad72;white-space:normal}}
body.lb-wide #lb2 .l2-cont small::before{{content:' · '}}
body.lb-wide #lb2 .l2-cont .go{{display:none}}
body.lb-wide #lb2 .l2-born{{{NOPL}padding:0!important;margin:24px 0 0;gap:12px;cursor:default;justify-items:stretch}}
body.lb-wide #lb2 .l2-bk,body.lb-wide #lb2 .l2-bd,body.lb-wide #lb2 .l2-born>.lb-xo{{display:none}}
body.lb-wide #lb2 #startBtn{{{PRc}width:100%!important;box-sizing:border-box;padding:3px 6px!important;font-size:17px!important;filter:drop-shadow(0 3px 6px rgba(0,0,0,.6)) drop-shadow(0 0 7px rgba(220,190,120,.14))}}
body.lb-wide #lb2 #startBtn .lb-xo{{display:block}}
body.lb-wide #lb2 #sexPick{{justify-self:center}}
body.lb-wide #lb2 .l2-bond,body.lb-wide #lb2 .l2-mi{{{NOPL}display:flex;align-items:center;gap:12px;padding:10px 8px!important;border-bottom:1px solid rgba(196,164,104,.13)!important;font-size:16px;line-height:1.3;color:#e4dccb;text-align:left}}
body.lb-wide #lb2 .l2-bond{{margin-top:14px}}
body.lb-wide #lb2 .l2-bond:hover,body.lb-wide #lb2 .l2-mi:not(:disabled):hover{{background:linear-gradient(90deg,rgba(216,189,124,.14),rgba(216,189,124,0))!important;box-shadow:inset 2px 0 0 #d8bd7c!important}}
body.lb-wide #lb2 .l2-bond>svg,body.lb-wide #lb2 .l2-mi svg{{width:20px;height:20px}}
body.lb-wide #lb2 .l2-bond .t{{flex:none}}
body.lb-wide #lb2 .l2-bond .t b{{font-size:16px;font-weight:400;color:#e4dccb}}
body.lb-wide #lb2 .l2-bond .t small{{display:none}}
body.lb-wide #lb2 .l2-bond .pick{{margin-left:auto;display:flex;align-items:center;gap:6px;max-width:190px;font-size:12px;color:#8f8878;text-align:left}}
body.lb-wide #lb2 .l2-bond .pick .lbf{{width:24px;height:24px;font-size:10px;border-width:1px;box-shadow:none}}
body.lb-wide #lb2 .l2-bond .pick .n{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
body.lb-wide #lb2 .l2-bond .pick .p{{flex:none}}body.lb-wide #lb2 .l2-bond .pick .p::before{{content:'· '}}
body.lb-wide #lb2 .l2-bond .go{{display:none}}
body.lb-wide #lb2 .l2-bond.lock{{flex-wrap:wrap;align-items:center}}
body.lb-wide #lb2 .l2-bond.lock .t{{flex:1}}
body.lb-wide #lb2 .l2-bond.lock .t b{{color:#7f7685}}
body.lb-wide #lb2 .l2-bond.lock .t small{{display:block;margin-top:3px;font-size:11px;line-height:1.5}}
body.lb-wide #lb2 .l2-bond.lock .r{{align-self:flex-start;margin-top:3px}}
body.lb-wide #lb2 .l2-bond.lock .r .m{{display:none}}body.lb-wide #lb2 .l2-bond.lock .r .pc{{display:inline}}
body.lb-wide #lb2 .l2-menu,body.lb-wide #lb2 .l2-menu.n4{{display:grid;grid-template-columns:none;gap:0}}
body.lb-wide #lb2 .l2-mi small{{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12px}}
body.lb-wide #lb2 .l2-mi .d{{position:static}}
body.lb-wide #lb2 .lb-news{{margin-top:12px}}
body.lb-wide #lb2 .l2-foot{{display:flex;flex-direction:column;align-items:flex-start;gap:14px;margin-top:auto;padding-top:18px}}
body.lb-wide #lb2 .l2-links{{justify-content:flex-start;gap:10px}}
body.lb-wide #lb2 .l2-links .pn-btn{{font-size:0!important;padding:3px!important;gap:0}}
body.lb-wide #lb2 .l2-links .pn-btn::before{{width:16px;height:16px}}
body.lb-wide #lb2 .l2-links .pn-btn .mono{{display:none}}
body.lb-wide #lb2 .l2-links .pn-btn .dot{{position:absolute;top:-5px;right:-5px}}
body.lb-wide #lb2 .l2-back.p{{display:inline-flex}}
body.lb-wide #lb2 .l2-keys{{display:block;position:absolute;right:max(16px,env(safe-area-inset-right,0px));bottom:34px;max-width:min(780px,calc(100vw - 420px));text-align:right;pointer-events:none}}
body.lb-wide #lb2 .l2-keys .keys{{display:block!important;margin:0;font-size:11px;line-height:1.8;color:rgba(233,226,214,.55)}}
body.lb-wide #lb2 .l2-ver{{display:block;position:absolute;right:max(16px,env(safe-area-inset-right,0px));bottom:14px;font:11px var(--f-mono);color:rgba(233,226,214,.55)}}
@media (max-height:519px){{
 body.lb-wide #lb2 .l2-main{{width:300px;padding:12px 18px 10px max(18px,env(safe-area-inset-left,0px))}}
 body.lb-wide #lb2 .l2-ui::before{{left:285px}}body.lb-wide #lb2 .l2-ui::after{{left:281.5px}}
 body.lb-wide #lb2 .l2-ey,body.lb-wide #lb2 .l2-lit,body.lb-wide #lb2 .l2-keys{{display:none}}
 body.lb-wide #lb2 .l2-title{{font-size:22px;margin:0}}
 body.lb-wide #lb2 .l2-cont{{margin-top:12px;border-width:8px!important;padding:0 4px!important;gap:9px}}
 body.lb-wide #lb2 .l2-face{{width:30px;height:30px}}
 body.lb-wide #lb2 .l2-cont .k{{font-size:13.5px}}body.lb-wide #lb2 .l2-cont b,body.lb-wide #lb2 .l2-cont small{{font-size:10.5px}}
 body.lb-wide #lb2 .l2-born{{margin-top:12px;gap:7px}}
 body.lb-wide #lb2 #startBtn{{font-size:14.5px!important;padding:0 4px!important;border-width:8px!important}}
 body.lb-wide #lb2 #sexPick button{{padding:2px 10px;font-size:11px}}
 body.lb-wide #lb2 .l2-bond,body.lb-wide #lb2 .l2-mi{{padding:3px 6px!important;font-size:14px;gap:10px}}
 body.lb-wide #lb2 .l2-bond .t b{{font-size:14px}}
 body.lb-wide #lb2 .l2-bond{{margin-top:8px}}
 body.lb-wide #lb2 .l2-bond>svg,body.lb-wide #lb2 .l2-mi svg{{width:17px;height:17px}}
 body.lb-wide #lb2 .l2-bond.lock .t small{{display:none}}
 body.lb-wide #lb2 .lb-news{{margin-top:6px;padding:2px 8px!important;font-size:12px}}
 body.lb-wide #lb2 .l2-foot{{flex-direction:row;align-items:center;gap:8px;padding-top:6px}}
 body.lb-wide #lb2 .l2-links{{gap:8px}}
 body.lb-wide #lb2 .l2-links .pn-btn{{padding:2px!important}}
 body.lb-wide #lb2 .l2-back.p{{margin-left:auto;padding:0 8px 0 4px!important}}
 body.lb-wide #lb2 .l2-tools{{top:10px}}body.lb-wide #lb2 .l2-ib{{padding:3px!important}}body.lb-wide #lb2 .l2-lang button{{padding:4px 7px}}
 body.lb-wide #lb2 .l2-ver{{bottom:8px}}
}}
/* 인연 소환 목록 */
#lbBond{{position:fixed;inset:0;z-index:50}}
#lbBond[hidden]{{display:none}}
#lbBond .bd-veil{{position:absolute;inset:0;background:rgba(4,5,10,.66);opacity:0;transition:opacity .25s}}
#lbBond.open .bd-veil{{opacity:1}}
#lbBond .bd-in{{position:absolute;left:0;right:0;bottom:0;top:9vh;max-width:600px;margin:0 auto;display:flex;flex-direction:column;box-sizing:border-box;{PNc}padding:6px 8px 0!important;color:var(--text);font-family:var(--lbF);outline:none;opacity:0;transform:translateY(16px);transition:opacity .25s,transform .25s;filter:drop-shadow(0 12px 28px rgba(0,0,0,.55))}}
#lbBond.open .bd-in{{opacity:1;transform:none}}
body.lb-wide #lbBond .bd-in{{left:50%;top:50%;bottom:auto;right:auto;width:min(760px,calc(100vw - 32px));max-width:none;max-height:84vh;margin:0;transform:translate(-50%,calc(-50% + 16px))}}
body.lb-wide #lbBond.open .bd-in{{transform:translate(-50%,-50%)}}
#lbBond button{{font-family:var(--lbF)}}
#lbBond .bd-hd{{flex:none;display:flex;align-items:center;gap:10px}}
#lbBond .bd-hd h3{{margin:0;font:700 17px var(--lbF);color:#e2c98e}}
#lbBond .bd-n{{flex:1;min-width:0;font-size:12px;color:#8f8878}}
#lbBond .pn-help{{width:26px;height:26px}}
#lbBond .bd-x{{background:none;border:0;color:#d8bd7c;font-size:17px;line-height:1;cursor:pointer;padding:6px}}
#lbBond .bd-tip{{flex:none;margin:6px 0 0;font:12px/1.55 var(--f-ui);color:#a39c8a}}
#lbBond .bd-rec{{flex:none;margin-top:12px;padding:10px 12px 8px;background:linear-gradient(180deg,rgba(216,189,124,.07),rgba(216,189,124,.02));border:1px solid rgba(196,164,104,.22)}}
#lbBond .bd-rec[hidden]{{display:none}}
#lbBond .bd-sec{{display:flex;align-items:center;gap:10px;font-size:12px;letter-spacing:.12em;color:#c9ad72}}
#lbBond .bd-sec::before{{content:'';flex:none;width:6px;height:6px;transform:rotate(45deg);background:linear-gradient(135deg,#f2e2b4,#b8975a)}}
#lbBond .bd-sec::after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(216,189,124,.4),rgba(216,189,124,0))}}
#lbBond .bd-sec small{{letter-spacing:0;font-size:11px;color:#8f8878}}
#lbBond .bd-all{{flex:none;margin-top:14px}}
#lbBond .bd-rrow{{display:flex;gap:10px;margin-top:10px;overflow:hidden}}
#lbBond .bd-rrow button{{flex:none;width:66px;display:grid;justify-items:center;align-content:start;gap:3px;padding:2px 0;background:none;border:0;color:#ddd3bb;font-size:11px;line-height:1.25;text-align:center;cursor:pointer}}
#lbBond .bd-rrow small{{font-size:10px;color:#8f8878}}#lbBond .bd-rrow small.s,#lbBond .bd-rrow button.on small{{color:#e6cd8f}}
#lbBond .lbf{{display:grid;place-items:center;width:50px;height:50px;border-radius:50%;background:#18141f center/cover no-repeat;border:1.5px solid #6b6150;box-shadow:0 0 0 2px rgba(10,12,22,.9),0 0 0 3px rgba(196,164,104,.35);font-style:normal;color:#8f8878;font-size:16px;box-sizing:border-box}}
#lbBond .bd-ctl{{flex:none;display:flex;gap:6px;margin-top:10px;align-items:center}}
#lbBond .bd-q{{flex:1;min-width:0;padding:8px 12px;border-radius:0;border:1px solid rgba(196,164,104,.3);background:rgba(5,7,14,.55);color:var(--text);font:13px var(--f-ui)}}
#lbBond select{{flex:none;padding:8px 6px;border-radius:0;border:1px solid rgba(196,164,104,.3);background:#0a0d18;color:#d8cfdb;font:12.5px var(--f-ui)}}
#lbBond .bd-sure{{flex:none;display:flex;align-items:center;gap:5px;font-size:12px;color:#d8cfdb;white-space:nowrap;cursor:pointer}}
#lbBond .bd-sure input{{accent-color:#d8bd7c;margin:0}}
#lbBond .bd-cls{{flex:none;display:flex;gap:5px;margin-top:10px;overflow-x:auto;padding-bottom:2px}}
#lbBond .bd-cls button{{flex:none;padding:5px 11px;border:1px solid rgba(196,164,104,.25);border-radius:0;background:none;color:#a39c8a;font-size:12px;cursor:pointer}}
#lbBond .bd-cls button[aria-pressed=true]{{background:rgba(216,189,124,.1);border-color:#d8bd7c;color:#f3e8cb}}
#lbBond .bd-cls .mono{{font-size:11px;opacity:.7}}
#lbBond .bd-grid{{flex:1;min-height:0;overflow-y:auto;margin-top:12px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;align-content:start;padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))}}
body.lb-wide #lbBond .bd-grid{{grid-template-columns:repeat(4,minmax(0,1fr))}}
#lbBond .bd-card{{display:grid;grid-template-columns:44px minmax(0,1fr);column-gap:10px;align-items:center;padding:8px;border:1px solid rgba(196,164,104,.15);border-radius:0;background:rgba(6,9,18,.55);color:var(--text);text-align:left;cursor:pointer;line-height:1.35}}
#lbBond .bd-card:hover{{border-color:rgba(216,189,124,.45)}}
#lbBond .bd-card .lbf{{grid-row:1/4;width:44px;height:44px;font-size:14px}}
#lbBond .bd-card b{{font-size:12.5px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
#lbBond .bd-card small{{font-size:11px;color:#8f8878}}#lbBond .bd-card small em{{font-style:normal}}#lbBond .bd-card small em.s{{color:#e6cd8f}}
#lbBond .bd-card u{{text-decoration:none;font-size:10.5px;color:#7f7685}}
#lbBond .bd-card.on{{border-color:#d8bd7c;background:rgba(216,189,124,.08);box-shadow:inset 0 0 0 1px rgba(216,189,124,.25)}}
#lbBond .bd-card.on .lbf{{border-color:#e6cd8f}}
#lbBond .bd-empty{{grid-column:1/-1;color:#8f8878;font-size:13px;padding:6px 2px}}
@media (max-height:519px){{
 body.lb-wide #lbBond .bd-in{{top:10px;max-height:calc(100vh - 20px);overflow-y:auto;transform:translate(-50%,16px)}}
 body.lb-wide #lbBond.open .bd-in{{transform:translateX(-50%)}}
 body.lb-wide #lbBond .bd-grid{{flex:none;overflow:visible}}
 body.lb-wide #lbBond .bd-tip{{display:none}}
 body.lb-wide #lbBond .bd-rec{{margin-top:8px;padding:6px 10px 4px}}
 body.lb-wide #lbBond .bd-rrow{{margin-top:6px}}
 body.lb-wide #lbBond .bd-rrow button{{width:56px;font-size:10px}}
 body.lb-wide #lbBond .bd-rrow .lbf{{width:38px;height:38px}}
 body.lb-wide #lbBond .bd-rrow small{{display:none}}
}}
'''

JS = r'''
/* ---- 로비 두 단계 (lb2_apply): ① 배경과 제목 → 누르면 ② 시작 기능 · 인연 소환 목록 ---- */
(()=>{ const $q=s=>document.querySelector(s), intro=$q('#intro'), body=document.body; if(!intro||typeof LOBBY==='undefined'||!$q('#intro .lb-screen')) return;
  const LG=typeof LANG==='string'&&['en','ja'].includes(LANG)?LANG:'ko';
  const TX={
   ko:{tap:'화면을 누르면 시작합니다',enter:'시작하기',back:'처음 화면',snd:'소리 켜기 · 끄기',set:'설정',hide:'UI 숨기기',show:'UI 보이기',cont:'이어하기',
    age:n=>`${n}세`,war:(y,d,h)=>`${y}년 · 성배전쟁 ${d}일째${h?' · '+h:''}`,year:y=>`${y}년`,
    sub:(a,b)=>`${a}번의 생 · 영령이 된 별 ${b}`,first:'첫 생을 기다리는 밤',newLife:'새로운 생',bornDesc:'어느 도시, 무작위로 정해진 집에서 한 번뿐인 삶이 시작된다.',
    bond:'인연 소환',bondSub:n=>`계약했던 서번트 ${n}명 중에서 고르기`,none:'고르지 않음',grail:'성배가 고른다',sure:'반드시',pct:n=>`약 ${n}%`,
    locked:'잠김',lockedPc:'첫 계약 뒤 열림',lockHint:'서번트와 계약하고 생을 마치면 열립니다. 그 서번트를 골라 두면, 소환할 때 다시 부를 수 있습니다.',
    dex:'서번트 도감',lives:'지난 생',ach:'업적',sent:'보낸 조',livesN:n=>`${n}번의 생`,
    contracted:n=>`계약했던 서번트 ${n}명`,tip:'지난 생에 계약했던 서번트를 골라 두면, 소환할 때 촉매 대신 그 서번트를 부를 수 있습니다.',
    recent:'최근 인연 소환',recentSub:'최근에 불렀던 순',all:'계약했던 서번트',nP:n=>`${n}명`,q:'이름으로 찾기',sort:'정렬',sRecent:'최근 함께한 순',sP:'닿을 확률 순',sName:'이름 순',
    sureOnly:'반드시만',cls:'클래스',allCls:'전체',help:'인연 소환 도움말',close:'닫기',empty:'조건에 맞는 서번트가 없습니다.',lastLife:'지난 생',ago:n=>`${n}생 전`,
    title:'성배가 차는 <em>밤</em>'},
   en:{tap:'Tap anywhere to begin',enter:'Start',back:'Title screen',snd:'Sound on / off',set:'Settings',hide:'Hide UI',show:'Show UI',cont:'Continue',
    age:n=>`Age ${n}`,war:(y,d,h)=>`${y} · Grail War, day ${d}${h?' · '+h:''}`,year:y=>`${y}`,
    sub:(a,b)=>`${a} ${a===1?'life':'lives'} · ${b} ${b===1?'star':'stars'} risen`,first:'A night awaiting its first life',newLife:'A new life',bornDesc:'In a certain city, in a home chosen at random, a life you only get once begins.',
    bond:'Bond Summoning',bondSub:n=>`Choose from ${n} contracted Servant${n===1?'':'s'}`,none:'None chosen',grail:'The Grail chooses',sure:'Always',pct:n=>`about ${n}%`,
    locked:'Locked',lockedPc:'Opens after your first contract',lockHint:'Opens once you finish a life after contracting a Servant. Choose that Servant here to call them again when you summon.',
    dex:'Servant Codex',lives:'Past lives',ach:'Achievements',sent:'Sent teams',livesN:n=>`${n} ${n===1?'life':'lives'}`,
    contracted:n=>`${n} contracted Servant${n===1?'':'s'}`,tip:'Choose a Servant you contracted in a past life, and when you summon you can call them instead of using a catalyst.',
    recent:'Recent bond summons',recentSub:'Most recently called first',all:'Contracted Servants',nP:n=>`${n}`,q:'Search by name',sort:'Sort',sRecent:'Most recent together',sP:'Highest chance',sName:'By name',
    sureOnly:'Guaranteed only',cls:'Class',allCls:'All',help:'Bond Summoning help',close:'Close',empty:'No Servants match.',lastLife:'Last life',ago:n=>`${n} lives ago`,
    title:'The Night the Grail <em>Fills</em>'},
   ja:{tap:'画面をタップして始める',enter:'はじめる',back:'タイトル画面',snd:'サウンドのオン・オフ',set:'設定',hide:'UIを隠す',show:'UIを表示',cont:'続きから',
    age:n=>`${n}歳`,war:(y,d,h)=>`${y}年・聖杯戦争${d}日目${h?'・'+h:''}`,year:y=>`${y}年`,
    sub:(a,b)=>`${a}の生・星になった英霊 ${b}`,first:'最初の生を待つ夜',newLife:'新しい生',bornDesc:'ある街の、無作為に決まる家で、一度きりの人生が始まる。',
    bond:'縁の召喚',bondSub:n=>`契約したサーヴァント${n}騎から選ぶ`,none:'選ばない',grail:'聖杯が選ぶ',sure:'必ず',pct:n=>`約${n}%`,
    locked:'ロック中',lockedPc:'初契約後に解放',lockHint:'サーヴァントと契約して生を終えると解放されます。そのサーヴァントを選んでおけば、召喚のときにまた呼べます。',
    dex:'サーヴァント図鑑',lives:'過去の人生',ach:'実績',sent:'送った組',livesN:n=>`${n}の生`,
    contracted:n=>`契約したサーヴァント ${n}騎`,tip:'前世に契約したサーヴァントを選んでおくと、召喚のとき触媒の代わりにそのサーヴァントを呼べます。',
    recent:'最近の縁の召喚',recentSub:'最近呼んだ順',all:'契約したサーヴァント',nP:n=>`${n}騎`,q:'名前で探す',sort:'並び替え',sRecent:'最近共にした順',sP:'届く確率順',sName:'名前順',
    sureOnly:'確定のみ',cls:'クラス',allCls:'すべて',help:'縁の召喚のヘルプ',close:'閉じる',empty:'条件に合うサーヴァントがいません。',lastLife:'前の生',ago:n=>`${n}つ前の生`,
    title:'聖杯が満ちる<em>夜</em>'}}[LG];
  const T=x=>typeof tr==='function'?tr(x):x;
  const P=p=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
  const I={back:P('<path d="M15 5l-7 7 7 7"/>'),eye:P('<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.8"/>'),
   eyeoff:P('<path d="M3 3l18 18"/><path d="M10.6 6.1A10.6 10.6 0 0 1 12 6c6.4 0 10 6 10 6a17 17 0 0 1-3.1 3.7M6.5 7.6C3.8 9.3 2 12 2 12s3.6 6 10 6c1.6 0 3-.4 4.2-.9"/>'),
   snd:P('<path d="M4 10h4l5-4v12l-5-4H4z"/><path d="M16 9c1.5 1.5 1.5 4.5 0 6M18.5 7c3 3 3 7 0 10"/>'),gear:P('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>'),
   link:P('<circle cx="8" cy="12" r="4"/><circle cx="16" cy="12" r="4"/>'),lock:P('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'),
   dex:P('<path d="M12 3l8 9-8 9-8-9z"/><path d="M12 8l3.5 4L12 16l-3.5-4z"/>'),lives:P('<path d="M12 3c-1.5 3 2 4 0 7-1 1.5-3 1-3-1"/><path d="M8 13a4 4 0 0 0 8 0c0-3-2-4-2-6"/><path d="M6 21h12"/>'),
   ach:P('<path d="M7 4h10v4a5 5 0 0 1-10 0z"/><path d="M7 6H4v1a3 3 0 0 0 3 3M17 6h3v1a3 3 0 0 1-3 3M12 13v4M8 21h8M9 17h6"/>'),sent:P('<path d="M21 3 3 10.5l7 2.5 2.5 7z"/><path d="M10 13l5-5"/>')};
  const el=(t,c,h)=>{ const e=document.createElement(t); if(c) e.className=c; if(h!=null) e.innerHTML=h; return e; };
  const E=x=>typeof esc==='function'?esc(x):String(x);
  const face=(id,on)=>id&&typeof FACE_I!=='undefined'&&FACE_I[id]!=null?`<i class="lbf${on?' on':''}" style="background-image:url(assets/portraits/${id}.webp)"></i>`:`<i class="lbf${on?' on':''}">${id?'?':'×'}</i>`;
  const pct=p=>p>=1?TX.sure:TX.pct(Math.round(p*100));
  const wideNow=()=>innerWidth/innerHeight>1.15;
  let stage=1;
  // 배경의 도시 아랫줄: 1단계는 제목 아래로 넓게, 2단계는 화면 아래 끝으로
  window.__lbLine=(vw,vh)=>{ const w=vw/vh>1.15; return stage===1?vh*(w?.86:.80):vh*(w?.97:1); };

  // ① 1단계: 「- Press to Start -」
  const press=el('div','lb-press','<i class="xl"></i><span class="t">- Press to Start -</span><small></small>'); press.setAttribute('aria-hidden','true'); press.querySelector('small').textContent=TX.tap; body.appendChild(press);
  const go=el('button','lb-go'); go.type='button'; go.textContent=TX.enter; go.onclick=()=>setStage(2); { const mo=$q('#intro .lb-more'); if(mo) mo.after(go); }

  // ② 2단계
  const lb2=el('div'); lb2.id='lb2';
  lb2.innerHTML=`<div class="l2-dim"></div><div class="l2-ui">
   <div class="l2-tools"><div class="l2-lang" role="group" aria-label="Language" data-notr>${['ko','en','ja'].map(l=>`<button type="button" data-l="${l}" lang="${l}"${l===LG?' class="on" aria-pressed="true"':' aria-pressed="false"'}>${{ko:'한',en:'EN',ja:'日'}[l]}</button>`).join('')}</div><button type="button" class="l2-ib l2-snd">${I.snd}</button><button type="button" class="l2-ib l2-set">${I.gear}</button><button type="button" class="l2-ib l2-hide">${I.eyeoff}</button></div>
   <div class="l2-main"><div class="l2-in">
    <button type="button" class="l2-back m">${I.back}<span></span></button>
    <div class="l2-head"><div class="l2-ey"></div><h2 class="l2-title" data-notr>${TX.title}</h2><div class="l2-sub"></div><div class="l2-lit"></div></div>
    <div class="l2-slot"></div>
    <button type="button" class="l2-cont" hidden><i class="l2-face"></i><span class="t"><span class="k"></span><b></b><small></small></span><span class="go" aria-hidden="true">›</span><i class="lb-xo t"></i></button>
    <div class="l2-born"><i class="lb-xo t"></i><i class="lb-xo b"></i><span class="l2-bk"></span><span class="l2-bd"></span></div>
    <div class="l2-bondw"></div>
    <div class="l2-menu"></div>
    <div class="l2-newsw"></div>
    <div class="l2-foot"><div class="l2-links"></div><button type="button" class="l2-back p">${I.back}<span></span></button></div>
   </div></div>
   <div class="l2-keys"></div><div class="l2-ver"></div>
  </div><button type="button" class="l2-show">${I.eye}<span></span></button>`;
  const $2=s=>lb2.querySelector(s);
  lb2.querySelectorAll('.l2-back span').forEach(s=>s.textContent=TX.back); $2('.l2-show span').textContent=TX.show;
  $2('.l2-cont .k').textContent=TX.cont; $2('.l2-bk').textContent=TX.newLife; $2('.l2-bd').textContent=TX.bornDesc;
  [['.l2-snd',TX.snd],['.l2-set',TX.set],['.l2-hide',TX.hide]].forEach(([s,t])=>{ const b=$2(s); b.title=t; b.setAttribute('aria-label',t); });
  { const ey=$q('#intro .lb-screen .eyebrow'); if(ey) $2('.l2-ey').innerHTML=ey.innerHTML; }
  try{ $2('.l2-ver').textContent='v'+PATCH[0].n; }catch(e){}
  // 원래 단추를 그대로 옮겨 쓴다(기능 · 번역 · 상태는 그대로)
  const born=$2('.l2-born'), sb=$q('#startBtn'), sp=$q('#sexPick');
  if(sb){ born.insertBefore(sb,$2('.l2-bd')); sb.insertAdjacentHTML('beforeend','<i class="lb-xo t"></i><i class="lb-xo b"></i>'); }
  if(sp) born.appendChild(sp);
  born.addEventListener('click',e=>{ if(e.target.closest('#sexPick,#startBtn')) return; const b=$q('#startBtn'); if(b) b.click(); });
  const links=$2('.l2-links');
  ['#patchBtn','#scnBtn','#achNewBtn','#fbBtn','#installBtn'].forEach(s=>{ const n=$q(s); if(n){ links.appendChild(n); if(!n.title) n.title=(n.textContent||'').replace(/\s+/g,' ').trim(); } });
  { const n=$q('#intro .lb-news'); if(n) $2('.l2-newsw').appendChild(n); }
  { const k=$q('#intro .keys'); if(k) $2('.l2-keys').appendChild(k); }
  body.appendChild(lb2);

  // 단계 바꾸기
  const slot=$2('.l2-slot'), lbTop=$q('#intro .lb-top'), pr=$q('#intro .lb-pickrow'), ask=$q('#sndAsk');
  let glideT=0;
  function setStage(n){ const was=stage; stage=n; body.classList.toggle('lb-s1',n===1); body.classList.toggle('lb-s2',n===2); body.classList.remove('lb-hideui');
    const mv=[pr,ask].filter(Boolean);
    if(n===2){ slot.append(...mv); refresh(); } else { if(lbTop) lbTop.after(...mv); bondClose(true); }
    try{ scrollTo(0,0); }catch(e){} $2('.l2-main').scrollTop=0;
    if(LOBBY.active){ if(was!==n){ body.classList.add('lb-glide'); clearTimeout(glideT); glideT=setTimeout(()=>body.classList.remove('lb-glide'),800); } requestAnimationFrame(()=>LOBBY.fit()); }
  }
  const busy=()=>body.classList.contains('lb-reading')||body.classList.contains('lb-rec')||!!$q('.dlg:not(.hidden)')||!$q('#lbBond').hidden;
  const onLobby=()=>!intro.classList.contains('hidden')&&LOBBY.active;
  document.addEventListener('click',e=>{ if(!onLobby()) return;
    if(stage===2&&body.classList.contains('lb-hideui')){ if(!e.target.closest('.dlg,#lbRec,#lbAbout')){ body.classList.remove('lb-hideui'); e.preventDefault(); } return; }
    if(stage!==1||busy()) return;
    if(e.target.closest('button,a,input,select,textarea,label,[role=group],[role=dialog],#lbAbout,#lbRec,.dlg,.snd-ask')) return;
    setStage(2); });
  addEventListener('keydown',e=>{ if(!onLobby()||busy()) return;
    if(stage===2&&body.classList.contains('lb-hideui')&&(e.key==='Escape'||e.key==='Enter'||e.key===' ')){ e.preventDefault(); body.classList.remove('lb-hideui'); return; }
    if(stage!==1||(e.key!=='Enter'&&e.key!==' ')) return; const a=document.activeElement; if(a&&a!==body&&a.matches('button,a,input,select,textarea,[contenteditable]')) return;
    e.preventDefault(); setStage(2); });

  // 2단계 단추
  lb2.querySelectorAll('.l2-lang button').forEach(b=>b.onclick=()=>{ if(b.dataset.l!==LG&&typeof setLang==='function') setLang(b.dataset.l); });
  const sndUpd=()=>{ try{ $2('.l2-snd').setAttribute('aria-pressed',String(!!Snd.on())); }catch(e){} };
  { const o=window.__lbSndSt; window.__lbSndSt=()=>{ try{ o&&o(); }catch(e){} sndUpd(); }; }
  $2('.l2-snd').onclick=()=>{ const s=$q('#intro .lb-ico'); if(s) s.click(); sndUpd(); };
  $2('.l2-set').onclick=()=>{ const s=$q('#setBtn'); if(s) s.click(); };
  $2('.l2-hide').onclick=e=>{ e.stopPropagation(); body.classList.add('lb-hideui'); };
  $2('.l2-show').onclick=e=>{ e.stopPropagation(); body.classList.remove('lb-hideui'); };
  lb2.querySelectorAll('.l2-back').forEach(b=>b.onclick=()=>setStage(1));
  $2('.l2-cont').onclick=()=>{ const c=$q('#contBtn'); if(c) c.click(); };
  $2('.l2-menu').addEventListener('click',e=>{ const m=e.target.closest('.l2-mi'); if(!m||m.disabled) return; const b=$q(`#intro .lb-row .btn[data-v="${m.dataset.v}"]`); if(b) b.click(); });

  // 2단계 내용 채우기
  function stats(){ let lives=0,met=0,got=0; try{ const c=dexLoad(), h=store.get(K_HIST)||[]; lives=Math.max(c.lives||0,store.get(K_COUNT)||0,h.length); met=dexMetCount(c); got=Sim.ACH.filter(a=>c.ach[a.id]).length; }catch(e){} return {lives,met,got}; }
  function refresh(){ const st=stats();
    $2('.l2-sub').textContent=st.lives||st.met?TX.sub(st.lives,st.met):TX.first;
    { const lit=$q('#intro .lb-lit'); $2('.l2-lit').innerHTML=lit?lit.innerHTML.replace(/<br\s*\/?>/gi,' '):''; }
    // 이어하기
    const cb=$q('#contBtn'), cc=$2('.l2-cont'); let sv=null; try{ sv=store.get(K_SAVE); }catch(e){}
    cc.hidden=!sv||!cb||cb.classList.contains('hidden');
    if(!cc.hidden){ const hid=sv.hero&&Sim.H_BY&&Sim.H_BY[sv.hero]?sv.hero:null, hn=hid?T(Sim.H_BY[hid].name):'', fc=$2('.l2-face');
      fc.hidden=!(hid&&typeof FACE_I!=='undefined'&&FACE_I[hid]!=null); if(!fc.hidden) fc.style.backgroundImage=`url(assets/portraits/${hid}.webp)`;
      cc.querySelector('b').textContent=`${T(sv.name||'')} · ${TX.age(sv.age)}`;
      cc.querySelector('small').textContent=sv.phase==='war'&&sv.war&&sv.war.day?TX.war(sv.year,sv.war.day,hn):TX.year(sv.year); }
    bondRow(); menu(st); sndUpd(); }
  function bondRow(){ const w=$2('.l2-bondw'); let L=[]; try{ L=bondList(); }catch(e){}
    if(!L.length){ w.innerHTML=`<div class="l2-bond lock" aria-disabled="true">${I.lock}<span class="t"><b></b><small></small></span><span class="r">${I.lock}<span class="m"></span><span class="pc"></span></span></div>`;
      w.querySelector('b').textContent=TX.bond; w.querySelector('small').textContent=TX.lockHint; w.querySelector('.r .m').textContent=TX.locked; w.querySelector('.r .pc').textContent=TX.lockedPc; return; }
    const id=bondPick(), p=id?bondChance(id):0;
    w.innerHTML=`<button type="button" class="l2-bond" aria-haspopup="dialog">${I.link}<span class="t"><b></b><small></small></span><span class="pick">${face(id,!!id)}<span class="n"></span><span class="p${p>=1?' s':''}"></span></span><span class="go" aria-hidden="true">›</span></button>`;
    w.querySelector('b').textContent=TX.bond; w.querySelector('.t small').textContent=TX.bondSub(L.length);
    w.querySelector('.n').textContent=id?T(Sim.H_BY[id].name):TX.none; w.querySelector('.pick .p').textContent=id?pct(p):TX.grail;
    w.querySelector('button').onclick=bondOpen; }
  const MI={dex:[I.dex,TX.dex],lives:[I.lives,TX.lives],ach:[I.ach,TX.ach],sent:[I.sent,TX.sent]};
  function menu(st){ const row=$q('#intro .lb-row'), off=!row||row.hidden, sent=row&&row.querySelector('[data-v=sent]'), ks=['dex','lives','ach'].concat(sent&&!sent.hidden?['sent']:[]);
    const val={dex:`${st.met} / ${(Sim.HEROES||[]).length}`,lives:TX.livesN(st.lives),ach:`${st.got} / ${(Sim.ACH||[]).length}`,sent:''};
    const an=$q('#achNewBtn'), dot=an&&!an.classList.contains('hidden'), m=$2('.l2-menu');
    m.innerHTML=ks.map(k=>`<button type="button" class="l2-mi" data-v="${k}"${off?' disabled':''}>${MI[k][0]}<span class="l">${E(MI[k][1])}</span><small>${k==='ach'&&dot?'<i class="d"></i>':''}${E(val[k])}</small></button>`).join('');
    m.classList.toggle('n4',ks.length===4); }
  let rq=0; const later=()=>{ if(rq) return; rq=requestAnimationFrame(()=>{ rq=0; if(body.classList.contains('lb-on')) refresh(); }); };
  [['#contBtn',{attributes:true,attributeFilter:['class']}],['#pastWrap',{attributes:true,attributeFilter:['class']}],['#achNewBtn',{attributes:true,attributeFilter:['class']}],
   ['#intro .lb-row',{attributes:true,subtree:true,attributeFilter:['hidden']}],['#bpCur',{childList:true,characterData:true,subtree:true}],['#intro .lb-lit',{childList:true}]].forEach(([s,o])=>{ const n=$q(s); if(n) new MutationObserver(later).observe(n,o); });

  // 인연 소환 목록: 누르면 바로 열린다. 위에 최근 인연 소환(폭에 맞는 만큼, 최대 8명), 고르면 바로 닫힌다
  const bd=el('section'); bd.id='lbBond'; bd.hidden=true; bd.setAttribute('role','dialog'); bd.setAttribute('aria-modal','true'); bd.setAttribute('aria-label',TX.bond);
  bd.innerHTML=`<div class="bd-veil"></div><div class="bd-in" tabindex="-1"><i class="lb-xo t"></i>
   <div class="bd-hd"><h3></h3><span class="bd-n"></span><button type="button" class="pn-help">?</button><button type="button" class="bd-x">✕</button></div>
   <p class="bd-tip"></p>
   <div class="bd-rec"><div class="bd-sec"><span class="a"></span><small></small></div><div class="bd-rrow"></div></div>
   <div class="bd-sec bd-all"><span class="a"></span><small></small></div>
   <div class="bd-ctl"><input type="search" class="bd-q" autocomplete="off" spellcheck="false"><select class="bd-sort"><option value="recent"></option><option value="p"></option><option value="name"></option></select><label class="bd-sure"><input type="checkbox"><span></span></label></div>
   <div class="bd-cls" role="group"></div>
   <div class="bd-grid"></div></div>`;
  const $b=s=>bd.querySelector(s);
  $b('h3').textContent=TX.bond; $b('.bd-tip').textContent=TX.tip; $b('.bd-rec .a').textContent=TX.recent; $b('.bd-rec small').textContent=TX.recentSub; $b('.bd-all .a').textContent=TX.all;
  $b('.bd-q').placeholder=TX.q; $b('.bd-sort').setAttribute('aria-label',TX.sort); [TX.sRecent,TX.sP,TX.sName].forEach((t,i)=>$b('.bd-sort').options[i].textContent=t); $b('.bd-sure span').textContent=TX.sureOnly;
  $b('.bd-cls').setAttribute('aria-label',TX.cls); $b('.pn-help').setAttribute('aria-label',TX.help); $b('.pn-help').title=TX.help; $b('.bd-x').setAttribute('aria-label',TX.close); $b('.bd-x').title=TX.close;
  body.appendChild(bd);
  const ago=()=>{ const m={}; try{ (store.get(K_HIST)||[]).forEach((x,i)=>{ if(!(x.hero&&x.wd&&x.wd.my)) return; const id=hidOf(x.wd.my.id,x.hero.name); if(id&&m[id]==null) m[id]=i; }); }catch(e){} return m; };
  function bdRender(){ let all=[]; try{ all=bondList(); }catch(e){} const cur=bondPick(), q=BP.q.trim().toLowerCase();
    $b('.bd-n').textContent=TX.contracted(all.length); $b('.bd-all small').textContent=TX.nP(all.length);
    const R=(store.get(K_BOND_RECENT)||[]).filter(id=>all.some(x=>x.id===id)), rec=$b('.bd-rec'), row=$b('.bd-rrow');
    rec.hidden=!R.length||!!q;
    if(!rec.hidden){ row.innerHTML=''; const iw=wideNow()&&innerHeight<520?56:66, n=Math.max(1,Math.min(R.length,8,Math.floor((row.clientWidth+10)/(iw+10))));
      row.innerHTML=R.slice(0,n).map(id=>{ const p=bondChance(id); return `<button type="button" data-b="${id}"${cur===id?' class="on" aria-pressed="true"':''}>${face(id,cur===id)}<span>${E(T(Sim.H_BY[id].name))}</span><small class="${p>=1?'s':''}">${E(pct(p))}</small></button>`; }).join(''); }
    const cls=[...new Set(all.map(x=>x.cls))], CO=['sword','lance','bow','rider','caster','shadow','berserk','judge','avenger','moon','ego'];
    if(BP.cls!=='all'&&!cls.includes(BP.cls)) BP.cls='all';
    $b('.bd-cls').innerHTML=[['all',TX.allCls,all.length],...CO.filter(k=>cls.includes(k)).map(k=>[k,T(Sim.CLS[k].n),all.filter(x=>x.cls===k).length])].map(([k,n,v])=>`<button type="button" data-c="${k}" aria-pressed="${BP.cls===k}">${E(n)} <span class="mono">${v}</span></button>`).join('');
    const nm=x=>(x.name+' '+T(x.name)).toLowerCase();
    let L=all.filter(x=>(BP.cls==='all'||x.cls===BP.cls)&&(!q||nm(x).includes(q))&&(!BP.sure||bondChance(x.id)>=1));
    if(BP.sort==='p') L.sort((a,b)=>bondChance(b.id)-bondChance(a.id)||bondLastTs(b.id)-bondLastTs(a.id));
    else if(BP.sort==='name') L.sort((a,b)=>T(a.name).localeCompare(T(b.name)));
    else L.sort((a,b)=>bondLastTs(b.id)-bondLastTs(a.id));
    const AG=ago(), none=`<button type="button" class="bd-card${cur?'':' on'}" data-b="">${face(null,!cur)}<b>${E(TX.none)}</b><small>${E(TX.grail)}</small></button>`;
    $b('.bd-grid').innerHTML=(q||BP.sure||BP.cls!=='all'?'':none)+(L.length?L.map(x=>{ const p=bondChance(x.id), a=AG[x.id]; return `<button type="button" class="bd-card${cur===x.id?' on':''}" data-b="${x.id}"${cur===x.id?' aria-pressed="true"':''}>${face(x.id,cur===x.id)}<b>${E(T(x.name))}</b><small>${E(T(Sim.CLS[x.cls].n))} · <em class="${p>=1?'s':''}">${E(pct(p))}</em></small>${a!=null?`<u>${E(a===0?TX.lastLife:TX.ago(a+1))}</u>`:''}</button>`; }).join(''):`<div class="bd-empty">${E(TX.empty)}</div>`); }
  let bdT=0, back=null;
  function bondOpen(){ let L=[]; try{ L=bondList(); }catch(e){} if(!L.length) return; clearTimeout(bdT); back=document.activeElement;
    $b('.bd-q').value=BP.q; $b('.bd-sort').value=BP.sort; $b('.bd-sure input').checked=!!BP.sure;
    bd.hidden=false; bdRender(); $b('.bd-grid').scrollTop=0; $b('.bd-in').scrollTop=0;
    requestAnimationFrame(()=>requestAnimationFrame(()=>{ bd.classList.add('open'); try{ $b('.bd-in').focus({preventScroll:true}); }catch(e){} })); }
  function bondClose(now){ if(bd.hidden) return; bd.classList.remove('open'); clearTimeout(bdT);
    if(now===true){ bd.hidden=true; return; } bdT=setTimeout(()=>{ bd.hidden=true; },260); if(back&&back.isConnected) try{ back.focus({preventScroll:true}); }catch(e){} }
  bd.addEventListener('click',e=>{ if(e.target.classList.contains('bd-veil')||e.target.closest('.bd-x')){ bondClose(); return; }
    if(e.target.closest('.pn-help')){ if(typeof showHelp==='function') showHelp('bond'); return; }
    const b=e.target.closest('[data-b]'); if(b){ bondSet(b.dataset.b||null); refresh(); bondClose(); return; }
    const t=e.target.closest('[data-c]'); if(t){ BP.cls=t.dataset.c; bdRender(); } });
  $b('.bd-q').addEventListener('input',e=>{ BP.q=e.target.value; bdRender(); });
  $b('.bd-sort').addEventListener('change',e=>{ BP.sort=e.target.value; bdRender(); });
  $b('.bd-sure input').addEventListener('change',e=>{ BP.sure=e.target.checked; bdRender(); });
  addEventListener('keydown',e=>{ if(e.key==='Escape'&&!bd.hidden&&!$q('.dlg:not(.hidden)')){ e.stopPropagation(); e.preventDefault(); bondClose(); } },true);
  let rz=0; addEventListener('resize',()=>{ clearTimeout(rz); rz=setTimeout(()=>{ if(!bd.hidden) bdRender(); },120); });

  // 로비에 들어올 때마다 1단계부터. 기록 화면이 열리면(돌아와서 다시 펼칠 때 등) 2단계로
  let vis=!intro.classList.contains('hidden');
  new MutationObserver(()=>{ const v=!intro.classList.contains('hidden'); if(v&&!vis) setStage(1); if(!v){ bondClose(true); body.classList.remove('lb-hideui'); } vis=v; }).observe(intro,{attributes:true,attributeFilter:['class']});
  { const rc=$q('#lbRec'); if(rc) new MutationObserver(()=>{ if(!rc.hidden&&stage===1&&onLobby()) setStage(2); }).observe(rc,{attributes:true,attributeFilter:['hidden']}); }
  setStage(1);
})();
'''

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, cnt=1):
        global s
        if s.count(o) != cnt: miss.append((o[:60], s.count(o))); return
        s = s.replace(o, n)
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    # 배경의 도시 아랫줄: 단계에 따라 정한 높이를 먼저 쓴다
    rp("acts=qs('#intro .lb-acts'),top=acts?Math.min(vh,acts.getBoundingClientRect().top+scrollY):vh*.7",
       "acts=qs('#intro .lb-acts'),LN=typeof window.__lbLine==='function'?window.__lbLine(vw,vh):null,top=LN!=null?LN:acts?Math.min(vh,acts.getBoundingClientRect().top+scrollY):vh*.7")
    # 최근 인연 소환은 8명까지 기억
    rp("store.set(K_BOND_RECENT,R.slice(0,3));", "store.set(K_BOND_RECENT,R.slice(0,8));")
    k = s.index('(() => {\nconst $=s=>document.querySelector(s);'); e = s.index('</script>', k); b = s.rindex('})();', k, e)
    s = s[:b] + JS + '\n' + s[b:]
    open(P, 'w', encoding='utf-8').write(s); print('lb2 miss', miss)
