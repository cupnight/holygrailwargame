"""에필로그 시간 흐름 개편 1 · 2단계 (11-12): 구간 틀 · 걸음 · 날짜 표시 · 예전 사건 옮기기. 화면 코드는 epi2.js.
새 사건(A · B 구간)과 영어 · 일본어는 검수 뒤에 넣는다. 사용: python3 epi2_apply.py <game.html>"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    js = open(os.path.join(HERE, 'epi2.js'), encoding='utf-8').read()
    rp("  function finalYears(){\n", js + "  function finalYears(){\n")
    # 걸음: 구간마다 기다리는 시간이 다르고, A · B · C는 ep2Step이 먼저 본다
    rp("    S.clock+=sp; if(S.clock<epiGap()) return; S.clock=0;\n    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);\n",
       "    S.clock+=sp; if(S.clock<epiGap()*ep2Gap()) return; S.clock=0;\n    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);\n    if(ep2Step()) return; if(S.dead||S.pending) return;\n")
    rp("if(S.phase==='epi') return Math.min(1,S.clock/(LEN[S.len].spy*1.3));", "if(S.phase==='epi') return Math.min(1,S.clock/(LEN[S.len].spy*1.3*ep2Gap()));")
    rp("  function passYears(n){\n    if(n<=0) return;\n", "  function passYears(n){\n    if(n>1&&S.epi&&S.epi.ph==='C') n=1;   // 열 해 구간: 한 해씩\n    if(n<=0) return;\n")
    # 기다림: A · B 구간에서는 해가 아니라 걸음으로 센다
    rp("else if(c.wait){ r.wait=war?S.war.day+3:S.year+2; if(st>=3) r.waited=1; }", "else if(c.wait){ if(ep2Tight()){ r.wait=0; S.epi.relK=S.epi.k+3; } else r.wait=war?S.war.day+3:S.year+2; if(st>=3) r.waited=1; }")
    rp("    return r.pt>=REL_PT[r.stage+1]&&S.war.trust>=REL_REQ[r.stage+1]; }", "    if(S.phase==='epi'&&S.epi&&S.epi.ph&&S.epi.ph!=='D'&&(S.epi.k||0)<(S.epi.relK||0)) return false;\n    return r.pt>=REL_PT[r.stage+1]&&S.war.trust>=REL_REQ[r.stage+1]; }")
    rp("later:()=>{S.flags.relNightWait=S.year+2;}", "later:()=>{ if(ep2Tight()) S.epi.nightK=S.epi.k+3; else S.flags.relNightWait=S.year+2; }")
    rp("&&!S.flags.relNight&&S.year>=(S.flags.relNightWait||0),once:0,", "&&!S.flags.relNight&&S.year>=(S.flags.relNightWait||0)&&!(S.epi&&(S.epi.k||0)<(S.epi.nightK||0)),once:0,")
    # 화면: 날짜
    rp("stay:stayHome(),away:!!S.flags.stayAway&&!S.flags.stayDied,", "when:ep2When(),stay:stayHome(),away:!!S.flags.stayAway&&!S.flags.stayDied,")
    rp("newLife,start,tick,", "newLife,start,tick,ep2When,")
    rp("S.dead?'끝':S.phase==='epi'?'에필로그':'삶';", "S.dead?'끝':S.phase==='epi'?((w2=>w2?(w2.u==='d'?`봄 · ${w2.n}일째`:`첫 해 · ${w2.n}달째`):'에필로그')(Sim.ep2When())):'삶';")
    rp(":v.yrs>=1?`수육 · 함께 산 지 ${v.yrs}년`:'수육 · 함께 살기 시작함';", ":v.when?(v.when.u==='d'?`수육 · 함께 산 지 ${v.when.n}일`:`수육 · 함께 산 지 ${v.when.n}달`):v.yrs>=1?`수육 · 함께 산 지 ${v.yrs}년`:'수육 · 함께 살기 시작함';")
    open(P, 'w', encoding='utf-8').write(s); print('epi2 miss', miss)
