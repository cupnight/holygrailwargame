"""11-14: 정보 창(패치 노트 · 도감 상세 · 도움말 등)의 '닫기'를 창 아래쪽에 늘 떠 있게 — 긴 패치 노트를 끝까지 내리지 않아도 닫을 수 있게
사용: python3 infox_apply.py <game.html>"""
import sys
CSS = ('#info .sheet.info{padding-bottom:0}'
       '#info .sheet.info>.choices{position:sticky;bottom:0;z-index:2;margin:16px -22px 0!important;padding:14px 22px 18px;'
       'background:var(--panel)}'
       '#info .sheet.info>.choices::before{content:"";position:absolute;left:0;right:0;top:-18px;height:18px;background:linear-gradient(to bottom,rgba(26,23,32,0),var(--panel));pointer-events:none}')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    o = ".info .row{display:grid;"
    if s.count(o) != 1: miss.append((o, s.count(o)))
    else: s = s.replace(o, CSS + o)
    print('infox miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
