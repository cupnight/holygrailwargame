"""비스트 위기 전투 배경음악(11-12): 키아라(보스, bx)와 싸우는 동안 kiara.mp3, BB(달에서 온 유닛 · 봉인을 쥔 NPC 조)와 싸우는 동안 bbfight.mp3를 튼다. 에미야 · 에미야[얼터]로 키아라와 싸울 때는 kiara.mp3 대신 emiyafight.mp3. 사용: python3 kiara_bgm_apply.py <game.html>"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n):
        global s
        if s.count(o) != 1: miss.append((o[:60], s.count(o))); return
        s = s.replace(o, n)
    rp('"boss":{"d":88.01,"ls":10.07,"le":87.51}', '"boss":{"d":88.01,"ls":10.07,"le":87.51},"kiara":{"d":40.89,"ls":16.41,"le":40.39},"bbfight":{"d":119.97,"ls":56.47,"le":119.47},"emiyafight":{"d":155.77,"ls":91.27,"le":155.27}')
    rp("if(b&&b.e){ if(b.e.cx==='boss') return 'boss';", "if(b&&b.e){ if(b.e.cx==='boss') return b.e.bx?(['emiya','emiya_alter'].includes(S.hero)?'emiyafight':'kiara'):'boss'; if(b.e.cx==='bb'||b.e.bxBB) return 'bbfight';")
    open(P, 'w', encoding='utf-8').write(s); print('kiara_bgm miss', miss)
