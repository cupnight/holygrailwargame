"""BB · 멜트릴리스 · 패션립 전용 소환 길 (11-12). 클래스(문 캔서 · 얼터 에고)가 아니라 서번트 셋에 붙는다.
- BB: 소환하는 밤의 달(보름 1/8) · 촉매 없는 보름 밤의 가로채기 2.5% · 달의 약속(키아라를 쓰러뜨린 생이 있으면 ×2) · NPC는 보름 밤에 시작한 전쟁에만
- 멜트 · 립: BB가 있는 전쟁에만 NPC로 · 내가 BB의 마스터면 떠도는 조각이 끼어드는 사건
사용: python3 moon_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
TR, TT = [], []
def k(ko, en, ja):
    (TT if '{' in ko else TR).append((ko, en, ja)); return ko
J = lambda x: json.dumps(x, ensure_ascii=False)

FULL = k('그날 밤, 보름달이 떠 있었다.', 'That night, the moon was full.', 'その夜は満月だった。')
HIJ = k('보름달빛이 마법진 위로 쏟아져 내렸다. 그어 둔 선이 하나씩 낯선 문양으로 고쳐 쓰였다. 빛이 걷히자, 부르지 않은 누군가가 원 한가운데서 웃고 있었다.',
        'Full moonlight poured down onto the circle. One by one, the lines you had drawn were rewritten into unfamiliar patterns. When the light cleared, someone you hadn\'t called was smiling at the centre of the circle.',
        '満月の光が魔法陣の上に降り注いだ。引いた線がひとつずつ見知らぬ紋様へと書き換えられていく。光が晴れると、呼んでいない誰かが円の真ん中で微笑んでいた。')
VOW = k('어딘가 낯익은 웃음이었다.', 'It was a strangely familiar smile.', 'どこか見覚えのある笑みだった。')
RUM = k('도시 어딘가에 서번트가 하나 더 떠돌고 있다는 소문이 돌았다. 마스터도 없이 누군가를 찾아다닌다고 한다.',
        'A rumour went round that one more Servant was wandering somewhere in the city, searching for someone without a Master.',
        '街のどこかに、もう一騎サーヴァントがさまよっているという噂が流れた。マスターも持たずに、誰かを探しているという。')
BBP = k('“…그 아이, 제가 떼어 낸 조각이에요. 결국 여기까지 왔네요. 선배, 마주쳐도 너무 놀라지 마세요.”',
        '“…That girl is a piece I broke off from myself. So she\'s come this far after all. Senpai, try not to be too surprised if you run into her.”',
        '「…あの子、わたしが切り離した欠片です。結局ここまで来ちゃいましたね。センパイ、出くわしてもあまり驚かないでくださいね」')
BBC = k('“…그 아이, 내가 떼어 낸 조각이야. 결국 여기까지 왔네. 마주쳐도 너무 놀라지 마.”',
        '“…That girl is a piece I broke off from myself. So she\'s come this far after all. Don\'t be too surprised if you run into her.”',
        '「…あの子、わたしが切り離した欠片。結局ここまで来たのね。出くわしても、あまり驚かないで」')
BBM = k('{N이} 창밖을 보며 작게 한숨을 쉬었다.', '{N} looked out of the window and gave a small sigh.', '{N}は窓の外を見て、小さくため息をついた。')
JOIN = k('감독관의 통지: 성배가 부르지 않은 조가 하나 끼어들었다. {0} 조.', 'The overseer\'s notice: a team the Grail did not call has forced its way in. The {0} team.', '監督役の通達：聖杯が呼んでいない組が一組、割り込んできた。{0}陣営。')
JOIN2 = k('마스터는 이 도시를 지나던 마술사라고 한다. 서번트 쪽이 먼저 그 사람을 골랐다는 소문이다.',
          'Its Master is said to be a magus who was only passing through the city. The rumour is that the Servant chose them, not the other way round.',
          'マスターはこの街を通りがかった魔術師だという。サーヴァントのほうが先にその人を選んだという噂だ。')
# BBM의 nf 틀은 {0~이}로도 남긴다(번역 틀 형식)
TT.append(('{0~이} 창밖을 보며 작게 한숨을 쉬었다.', '{0} looked out of the window and gave a small sigh.', '{0}は窓の外を見て、小さくため息をついた。'))
TT.remove((BBM, '{N} looked out of the window and gave a small sigh.', '{N}は窓の外を見て、小さくため息をついた。'))

CORE = f"""
  // ---- BB · 멜트릴리스 · 패션립 전용 소환 길 (11-12) ----
  const MOON_GATED=new Set(['bb','meltryllis','passionlip']), MOON_EGO=['meltryllis','passionlip'];
  const moonHijP=()=>.025*(S&&S.moonVow?2:1);   // 촉매 없는 보름 밤, BB가 마법진을 가로챈다 (달의 약속이면 ×2)
  {{ const f0=newLife; newLife=(opt={{}})=>{{ const r=f0(opt); if(S) S.moonVow=!!opt.moon; return r; }}; }}
  // 내가 BB의 마스터면: 떼어 낸 조각(멜트 · 립)이 전쟁 중에 끼어든다 (2~8일차 아침마다 4%, 전쟁에 한 번, 다음 날 합류)
  {{ const f0=dayStart; dayStart=()=>{{ f0(); const w=S&&S.war; if(!w||w.ended||S.dead||S.phase!=='war') return;
      if(w.egoPend&&w.day>=w.egoPend.day){{ const id=w.egoPend.h; w.egoPend=null; if(w.pairs.some(p=>p.hero===id)) return;
        const A=pick(ARCHE.filter(a=>!a.hidden&&!['burial','sibling','exorcist','ghost'].includes(a.id)&&!w.pairs.some(p=>p.aid===a.id))||ARCHE.filter(a=>!a.hidden));
        const taken=new Set(); [S.name,...w.pairs.map(p=>p.mname)].filter(Boolean).forEach(n=>nameParts(n).forEach(x=>taken.add(x)));
        const sx=ch(.5)?'m':'f', q={{i:Math.max(0,...w.pairs.map(p=>p.i))+1,seals:3,aid:A.id,cls:H_BY[id].cls,hero:id,mname:uniqName(sx,undefined,taken),arche:A.n,tac:A.tac,pw:ri(A.pw[0],A.pw[1]),hp:100,alive:true,master:true,stray:0,intel:0,ally:false,revealed:false,foe:0,known:false,usedRevive:false,joinDay:w.day}};
        w.pairs.push(q); log({J(JOIN)}.replace('{{0}}',cn(q)),'notice'); log({J(JOIN2)},'war'); wrec('hint',`${{cn(q)}} 조가 전쟁에 끼어들었다`,{{p:q.i}}); return; }}
      if(!w.egoDone&&S.hero==='bb'&&w.heroAlive&&w.day>=2&&w.day<=8&&!(w.crisis&&w.crisis.type==='beast3R')&&!w.pairs.some(p=>MOON_EGO.includes(p.hero))&&ch(.04)){{
        w.egoDone=1; w.egoPend={{day:w.day+1,h:pick(MOON_EGO)}}; log({J(RUM)},'war'); const h=H_BY.bb; const l=svl(h,{J(BBC)},{J(BBP)},{J(BBM)}); if(l) log(l,'voice'); }} }}; }}
"""

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        kk = s.count(o)
        if kk != c: miss.append((o[:70], kk)); return
        s = s.replace(o, n)
    # 소환하는 밤의 달
    rp("  function doSummon(id){\n    const A=S.aff||{avenger:0,judge:0};",
       "  function doSummon(id){\n    const A=S.aff||{avenger:0,judge:0};\n    const full=ch(1/8); if(full) log(" + J(FULL) + ",'war');")
    # 보름 밤의 가로채기: 촉매 · 인연 소환이 없을 때만
    rp("    else if(ch(pSp)){ const k=wpick(['avenger','judge'],x=>A[x]+.5); h=pick(HEROES.filter(x=>x.cls===k)); }",
       "    else if(full&&ch(moonHijP())){ h=H_BY.bb; S.flags.bbHijack=1; log(" + J(HIJ) + "+(S.moonVow?' '+" + J(VOW) + ":''),'war'); }\n"
       "    else if(ch(pSp)){ const k=wpick(['avenger','judge'],x=>A[x]+.5); h=pick(HEROES.filter(x=>x.cls===k&&!MOON_GATED.has(x.id))); }")
    rp("const k=wpick(['avenger','judge'],x=>A[x]+.5); h=pick(HEROES.filter(x=>x.cls===k)); log(",
       "const k=wpick(['avenger','judge'],x=>A[x]+.5); h=pick(HEROES.filter(x=>x.cls===k&&!MOON_GATED.has(x.id))); log(")
    # NPC 특수 자리: BB는 보름 밤에 시작한 전쟁에만 · 멜트 · 립은 BB가 있는 전쟁에만
    rp("    const extra = ch(.12)? pick(SPECIAL.filter(c=>c!==h.cls)) : null;\n    if(extra) others.splice(ri(0,others.length),0,extra);",
       """    const fq=[]; let extra=null;
    if(ch(.12)){ const gen=SPECIAL.filter(c=>c!==h.cls&&HEROES.some(x=>x.cls===c&&!MOON_GATED.has(x.id))); let xh=null;
      if(h.id==='bb'&&ch(.5)) xh=pick(MOON_EGO.filter(x=>x!==h.id));                       // 내 BB: 특수 자리의 절반은 떼어 낸 조각
      else if(full&&h.id!=='bb'&&ch(1/(gen.length+1))) xh='bb';                             // 보름 밤: BB도 특수 자리 후보
      extra=xh?H_BY[xh].cls:pick(gen); if(xh) fq.push(xh); others.splice(ri(0,others.length),0,extra);
      if(xh==='bb'&&ch(.5)){ const e2=pick(MOON_EGO.filter(x=>x!==h.id)); fq.push(e2); others.splice(ri(0,others.length),0,H_BY[e2].cls); } }   // NPC BB를 따라온 조각""")
    rp("      const hs=HEROES.filter(x=>x.cls===c&&!used.has(x.id)); const hh=pick(hs); used.add(hh.id);",
       "      const fh=fq.find(id=>H_BY[id].cls===c&&!used.has(id)); const hs=fh?[H_BY[fh]]:HEROES.filter(x=>x.cls===c&&!used.has(x.id)&&!MOON_GATED.has(x.id)); const hh=pick(hs); used.add(hh.id);")
    rp("    S.war.bt={n:0,win:0,lose:0,ret:0,fled:0,draw:0,asn:0};", "    S.war.fullMoon=full; S.war.bt={n:0,win:0,lose:0,ret:0,fled:0,draw:0,asn:0};")
    rp("  return {cn,ACH:", CORE + "  return {cn,ACH:")
    # 화면 쪽: 달의 약속 기록(키아라를 쓰러뜨린 생) · 새 생에 넘기기. 도감 ach 칸에 숨은 표시로 둔다(기기 연결로 함께 옮겨진다)
    rp("r.newDex={newC:m.newC,newM:m.newM}; LIFE_NEW=[]; }",
       "r.newDex={newC:m.newC,newM:m.newM}; LIFE_NEW=[]; if(Sim.S&&Sim.S.flags&&Sim.S.flags.bxEnd&&!c.ach._bbmoon){ c.ach._bbmoon={t:Date.now(),n}; store.set(K_CODEX,c); } }")
    rp("bond:bid?{id:bid,p:bondChance(bid)}:null})", "bond:bid?{id:bid,p:bondChance(bid)}:null,moon:moonVow()})")
    rp("function birth(){", "function moonVow(){ try{ const c=dexLoad(); return !!(c&&c.ach&&c.ach._bbmoon); }catch(e){ return false; } }\nfunction birth(){")
    s, nd, nt = i18n.add(s, TR, TT)
    open(P, 'w', encoding='utf-8').write(s); print(os.path.basename(P), 'miss', miss, 'tr', nd, nt)
