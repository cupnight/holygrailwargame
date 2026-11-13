"""11-14: 패치 노트에 버전 번호 — 첫 공개(2026.10.22)를 v1.00, 그 뒤로 0.01씩 (앞자리를 올릴 때는 사용자가 따로 정한다)
- 항목마다 n:'1.xx'를 적어 둔다(개수로 계산하면 앞자리를 올릴 때 꼬인다). 적지 않은 항목은 순서로 채운다
- 목록: 버전(금색) · 날짜(흐리게, '-2' 없이) · 제목. 휴대폰에서는 날짜를 버전 아래로 쌓아 '＋'가 줄을 넘지 않게
- 로비 버튼: 날짜 대신 버전
- '봤는지'(NEW · 빨간 점)는 예전처럼 날짜 키(p.v)로 판단한다
사용: python3 pnver_apply.py <game.html>"""
import sys, re
CSS = ('.pn summary{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:baseline;column-gap:10px;flex-wrap:nowrap}'
       '.pn summary .vd{display:flex;gap:10px;align-items:baseline}.pn summary .d{font-size:11.5px;color:var(--dim)}.pn summary .tt{min-width:0}'
       '.pn summary .tt .new{margin-left:6px;vertical-align:1px}.pn summary::after{margin-left:0}'
       '@media (max-width:480px){.pn summary .vd{flex-direction:column;gap:0;line-height:1.25}.pn summary .d{font-size:10.5px}}')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 항목마다 버전 번호 (가장 오래된 것이 1.00)
    a = s.index('const PATCH=['); b = s.index('const K_PATCH=', a); blk = s[a:b]
    heads = list(re.finditer(r"\n \{v:(['\"])(\d{4}\.\d\d\.\d\d(?:-\d+)?)\1,", blk))
    N = len(heads)
    for j, m in reversed(list(enumerate(heads))):
        if re.match(r"\n \{v:['\"][^'\"]+['\"],n:", blk[m.start():m.end() + 4]): continue
        ver = '%.2f' % (1 + (N - 1 - j) * 0.01)
        blk = blk[:m.end()] + "n:'" + ver + "'," + blk[m.end():]
    s = s[:a] + blk + s[b:]
    rp("const K_PATCH='cupnight.patch.v1';", "const K_PATCH='cupnight.patch.v1';\nconst pnN=(p,i)=>p.n||(1+(PATCH.length-1-i)*0.01).toFixed(2); // 11-14: 패치 버전")
    rp("$('#patchVer').textContent=v.slice(5).replace('-','.');", "$('#patchVer').textContent='v'+pnN(PATCH[0],0);")
    rp("<summary><span class=\"v mono\">'+p.v+'</span><span class=\"t\">'+esc(p.t)+'</span>'+(i===0&&seen!==p.v?'<span class=\"new\">NEW</span>':'')+'</summary>",
       "<summary><span class=\"vd\"><span class=\"v mono\">v'+pnN(p,i)+'</span><span class=\"d mono\">'+p.v.replace(/-\\d+$/,'')+'</span></span><span class=\"tt\"><span class=\"t\">'+esc(p.t)+'</span>'+(i===0&&seen!==p.v?'<span class=\"new\">NEW</span>':'')+'</span></summary>")
    rp(".pn summary::after{content:'＋';margin-left:auto;color:var(--faint);font-size:13px}", ".pn summary::after{content:'＋';margin-left:auto;color:var(--faint);font-size:13px}" + CSS)
    print('pnver miss', miss, 'entries', N)
    open(P, 'w', encoding='utf-8').write(s)
