"""키아라 전투 배경음악(11-12): 비스트 Ⅲ/R의 키아라(보스, bx)와 싸우는 동안 검은 성배 보스 곡 대신 kiara.mp3를 튼다. 사용: python3 kiara_bgm_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:60], s.count(o))); return
        s = s.replace(o, n)
    rp('"boss":{"d":88.01,"ls":10.07,"le":87.51}', '"boss":{"d":88.01,"ls":10.07,"le":87.51},"kiara":{"d":40.89,"ls":16.41,"le":40.39}')
    rp("if(b&&b.e){ if(b.e.cx==='boss') return 'boss';", "if(b&&b.e){ if(b.e.cx==='boss') return b.e.bx?'kiara':'boss';")
    open(P, 'w', encoding='utf-8').write(s); print('kiara_bgm miss', miss)
