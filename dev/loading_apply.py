"""로딩 화면 (11-13). 하늘에서 금빛 줄기가 졸졸 떨어져 성배를 채우고, 넘쳐 쏟아진 뒤 성배와 검은 배경이 픽셀로 흩어지며 로비가 드러난다.
<body> 바로 뒤에 넣어 문서를 읽는 동안에도 가장 먼저 그려지게 한다. lobby_apply.py 뒤에 쓴다(LOBBY.onReady를 쓴다).
사용: python3 loading_apply.py <game.html>"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
JS = open(os.path.join(HERE, 'loading_rt.js'), encoding='utf-8').read()
CSS = r'''
/* ---- 로딩 화면 ---- */
#ldScr{position:fixed;inset:0;z-index:2147483000;background:#07060b;pointer-events:auto}
#ldScr[hidden]{display:none}
#ldScr canvas{position:absolute;inset:0;width:100%;height:100%}
#ldTxt{position:absolute;left:0;right:0;top:calc(46% + min(5.67vh,10.33vw,50px) + 22px);margin:0;text-align:center;font-family:'Gowun Batang',Georgia,serif;font-size:13px;letter-spacing:.12em;color:rgba(235,214,170,.72);padding-inline:16px}
#ldTxt b{display:block;margin-top:6px;font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace;font-weight:400;font-size:11px;letter-spacing:.2em;color:rgba(227,201,141,.6);font-variant-numeric:tabular-nums}
body.ld-on #intro{opacity:0!important}
#intro{transition:opacity .9s}
'''
# 문구는 게임과 같은 규칙으로 언어를 고른다(저장된 언어 → 브라우저 언어). 번역기는 이 상자를 건드리지 않는다(data-notr)
HTML = r'''<div id="ldScr" data-notr role="status" aria-live="polite"><canvas id="ldBg"></canvas><canvas id="ldCup"></canvas><p id="ldTxt"><span></span><b>0%</b></p></div>
<script>
(()=>{let L='ko';try{const v=JSON.parse(localStorage.getItem('cupnight.lang')||'null');if(['ko','en','ja'].includes(v))L=v;else{const n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').toLowerCase();L=n.startsWith('ko')?'ko':n.startsWith('ja')?'ja':'en'}}catch(e){}
 document.querySelector('#ldTxt span').textContent={ko:'성배에 마력이 차오른다',en:'Mana is filling the Grail',ja:'聖杯に魔力が満ちていく'}[L];})();
''' + JS + '''
</script>
'''
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    if 'id="ldScr"' in s: print('loading: already'); continue
    i = s.index('</style>'); s = s[:i] + CSS + s[i:]
    if s.count('<body>') != 1: miss.append(('<body>', s.count('<body>')))
    else: s = s.replace('<body>', '<body>\n' + HTML, 1)
    print('loading miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
