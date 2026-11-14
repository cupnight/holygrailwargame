"""11-14: 넓은 로비에서 인연 소환 칸을 펼치면 같은 줄의 「태어나기」 · 성별 칸이 함께 길게 늘어나던 것
- 펼친 동안에는 오른쪽 칸 전체를 인연 소환이 쓰고, 왼쪽은 태어나기 · 이어하기 · 도감/지난 생/업적을 원래 높이로 차례로 쌓는다
- 접었을 때와 좁은 화면은 그대로
사용: python3 lbbond_apply.py <game.html>   (lobby_apply 뒤에)"""
import sys
CSS = ('body.lb-wide #intro.lb .lb-acts:has(#bpHead[aria-expanded=true]){align-items:start;grid-template-rows:repeat(4,auto) 1fr}'
       'body.lb-wide #intro.lb .lb-acts:has(#bpHead[aria-expanded=true])>*{grid-column:1}'
       'body.lb-wide #intro.lb .lb-acts:has(#bpHead[aria-expanded=true])>.bondp{grid-column:2;grid-row:1/-1}')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    o = "body.lb-wide #intro.lb .lb-acts{grid-template-columns:1fr 1fr;gap:8px 10px;align-items:stretch}"
    if s.count(o) != 1: miss.append((o[:50], s.count(o)))
    else: s = s.replace(o, o + "\n" + CSS)
    print('lbbond miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
