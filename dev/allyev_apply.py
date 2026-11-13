"""11-14 문의: 전투 중 대화로 이미 동맹이 된 조가, 마스터 사건에서 다시 동맹을 걸어오던 것
- 동맹을 제안하는 마스터 사건(편의점 앞 · 떠난 신부 · 몰락 가문의 막내 · 다른 겨울의 사람 · 지난 겨울의 사람 · 형제 · 민주주의파 · 밤의 손님)에 표시(al:1)
- 그 조와 이미 동맹이면 그 사건은 건너뛰고 다음 사건으로 넘어간다 (다른 조와 동맹 중일 때는 지금처럼 동맹 선택지만 막힌 채 나온다)
사용: python3 allyev_apply.py <game.html>"""
import sys, re
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    a = s.index('const MASTER_EV = {'); b = s.index('function masterEvent(', a); blk = s[a:b]
    st = [m.start() for m in re.finditer(r"\{(?:opt:1,)?c:p=>", blk)] + [len(blk)]
    hit = []
    for i in reversed(range(len(st) - 1)):
        seg = blk[st[i]:st[i + 1]]
        if 'p.ally=true' in seg and not seg.startswith('{al:1,'):
            blk = blk[:st[i]] + '{al:1,' + blk[st[i] + 1:]; hit.append(i)
    s = s[:a] + blk + s[b:]
    if len(hit) != 8: miss.append(('al count', len(hit)))
    o = "      if(p.arc<arc.length&&arc[p.arc].c(p)) opts.push(p); }"
    if s.count(o) != 1: miss.append((o[:60], s.count(o)))
    else: s = s.replace(o, "      while(p.arc<arc.length&&arc[p.arc].al&&p.ally) p.arc++; // 이미 동맹인 조: 동맹을 걸어오는 사건은 건너뛴다 (11-14 문의)\n" + o)
    print('allyev miss', miss, 'marked', len(hit))
    open(P, 'w', encoding='utf-8').write(s)
