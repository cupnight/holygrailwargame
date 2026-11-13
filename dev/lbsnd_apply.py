"""11-14: 로비 위쪽 소리 아이콘 — 켜져 있으면 금색(게임 안 소리 버튼과 같은 색) · 다른 곳(소리 묻기 · 설정 · M키)에서 켜고 꺼도 바로 맞춘다
사용: python3 lbsnd_apply.py <game.html>   (lobby_apply 뒤에)"""
import sys
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("#intro.lb .lb-ico[aria-pressed=false]{opacity:.55}",
       "#intro.lb .lb-ico[aria-pressed=false]{opacity:.55}#intro.lb .lb-ico[aria-pressed=true]{color:var(--gold2);border-color:rgba(201,164,92,.55)}")
    rp("const sndSt=()=>{ try{ snd.setAttribute('aria-pressed',String(!!Snd.on())); }catch(e){} };",
       "const sndSt=()=>{ try{ snd.setAttribute('aria-pressed',String(!!Snd.on())); }catch(e){} }; window.__lbSndSt=sndSt;")
    rp("function sndQuick(){ const q=$('#sndQ');", "function sndQuick(){ try{ window.__lbSndSt&&window.__lbSndSt(); }catch(e){} const q=$('#sndQ');")
    print('lbsnd miss', miss)
    open(P, 'w', encoding='utf-8').write(s)
