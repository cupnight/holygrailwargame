"""11-13: 키아라전의 동행 · 호위를 눈에 보이게
① 전투 카드: 내 쪽에 '함께 싸우는 서번트'(BB · 풀려난 멜트릴리스 · 패션립), 적 쪽에 '키아라를 지키는 센티넬'
② 결전 첫 합의 한마디(BB · 멜트 · 립), BB의 행동 줄(이미 있는 판정 −10을 보여 주는 연출) · 놀리는 한마디, 멜트 · 립이 칠 때 가끔 한마디
③ 강림 뒤 낮마다 동행 하나가 한마디
④ 호위 센티넬의 행동 묘사를 동행 서번트처럼 여러 갈래로(엄호 · 견제 · 협공은 서번트의 공격 방식에 따라)
수치는 바꾸지 않는다. 사용: python3 bxally_apply.py <game.html>"""
import sys, json, i18n
D, T = [], []          # 번역 사전 · 틀
def q(ko, en, ja):     # 따옴표 대사: 사전에 그대로, 따옴표째로도
    D.append((ko, en, ja)); D.append(('“' + ko + '”', '“' + en + '”', '「' + ja.rstrip('。') + '」')); return ko
def n_(ko, en, ja): D.append((ko, en, ja)); return ko
def t_(ko, en, ja): T.append((ko, en, ja)); return ko

BB_START = [q('선배, 이번엔 숨기지 않아요. 제 몫까지 제대로 보여 줄게요.', "Senpai, no more hiding this time. I'll show you everything I've got.", 'センパイ、今度は隠しませんよ。わたしの分まで、ちゃんと見せてあげます。'),
            q('자, 여기서부터는 BB 채널 특별 생방송이에요. 주인공은 물론 선배고요.', 'Okay, from here on it’s a BB Channel live special. And the star is you, of course, Senpai.', 'さあ、ここからはBBチャンネル特別生放送です。主役はもちろんセンパイですよ。')]
BB_ACT = [n_('BB가 키아라의 발밑에 보라색 격자를 깔았다. 키아라의 움직임이 한 박자 늦어졌다.', "BB laid a violet grid beneath Kiara's feet. Kiara's movements fell half a beat behind.", 'BBがキアラの足元に紫の格子を敷いた。キアラの動きが一拍遅れた。'),
          n_('BB가 지휘봉을 휘둘렀다. 키아라 주위의 공간이 잠깐 엉뚱한 방향으로 접혔다.', 'BB swung her baton. The space around Kiara folded the wrong way for a moment.', 'BBが指揮棒を振った。キアラの周りの空間が一瞬あらぬ方向へ折れ曲がった。'),
          n_('BB가 키아라의 그림자에 장난처럼 낙서를 했다. 키아라가 처음으로 불쾌한 얼굴을 했다.', "BB scribbled on Kiara's shadow like a prank. For the first time, Kiara looked displeased.", 'BBがいたずらのようにキアラの影に落書きをした。キアラが初めて不快そうな顔をした。')]
BB_TEASE = [q('어머, 그 몸 무겁지 않아요? 남의 꿈을 그렇게 많이 드시니까요.', "Oh my, isn't that body heavy? You've eaten so many other people's dreams.", 'あら、その体重くありません？ 他人の夢をそんなにたくさん召し上がるから。'),
            q('웃는 얼굴로 버티는 거, 이제 좀 지겹지 않아요?', "Aren't you getting tired of holding on with that smile?", '笑顔で耐えるの、そろそろ飽きてきません？'),
            q('선배, 지금이에요. 제가 열어 둔 틈, 놓치면 혼나요?', "Senpai, now! If you miss the opening I made, you're in trouble, okay?", 'センパイ、今です。わたしが開けた隙、逃したら怒りますよ？')]
MELT_START = [q('따라와. 느린 건 질색이니까.', 'Keep up. I hate slow things.', 'ついてきなさい。遅いのは嫌いなの。'),
              q('빚은 오늘 갚을 거야. 방해하면 너부터 베어 버려.', "I'm repaying that debt today. Get in my way and I'll cut you first.", '借りは今日返すわ。邪魔したらあなたから斬るから。')]
MELT_HIT = [q('그 웃음, 정말 역겨워.', 'That smile is truly revolting.', 'その笑い、本当に気持ち悪い。'),
            q('녹아내리는 건 네 쪽이야.', "You're the one who'll melt.", '溶けるのはあなたの方よ。'),
            q('흥. 이 정도로 쓰러지면 재미없잖아.', "Hmph. It'd be no fun if you fell to this much.", 'ふん。この程度で倒れたらつまらないじゃない。')]
LIP_START = [q('저, 저도… 힘낼게요. 꽉 쥐면 되는 거죠?', "I-I'll… do my best too. I just have to squeeze tight, right?", 'わ、わたしも……頑張ります。ぎゅっと握ればいいんですよね？'),
             q('이번엔… 제 마음대로 싸울 수 있어요. 그러니까, 잘 봐 주세요.', 'This time… I can fight the way I want. So, please watch me.', '今度は……自分の思うように戦えます。だから、見ててください。')]
LIP_HIT = [q('죄, 죄송해요…! 그래도 안 놓을 거예요.', "I-I'm sorry…! But I won't let go.", 'ご、ごめんなさい……！ でも、離しません。'),
           q('아, 아파요? …그래도 그쪽이 더 나빴어요.', 'D-does it hurt? …Still, you were worse.', 'い、痛いですか？ ……でも、そっちの方がひどかったです。'),
           q('조금만… 조금만 더 세게 쥘게요.', "Just a little… I'll squeeze just a little harder.", 'もう少し……もう少しだけ強く握りますね。')]
DAY = {'bb': [q('그 사람, 지금쯤 배부르게 웃고 있겠죠. …오늘 밤엔 그 웃음 좀 지워 줘요, 선배.', "She's probably smiling with a full belly right about now. …Wipe that smile off her face tonight, Senpai.", 'あの人、今ごろお腹いっぱいで笑ってるんでしょうね。……今夜はその笑顔、消してあげてください、センパイ。'),
              q('선배, 잠은 잤어요? 결전 앞에서 꾸벅꾸벅 졸면 BB가 사진 찍어 둘 거예요.', "Senpai, did you sleep? If you nod off before the final battle, BB will take pictures.", 'センパイ、寝ました？ 決戦の前にうとうとしてたら、BBが写真撮っちゃいますよ。'),
              q('제가 투명인간인 줄 알았죠? 다 보고 있었어요. 선배가 얼마나 무리하는지까지요.', "You thought I was invisible, didn't you? I've been watching everything. Even how hard you've been pushing yourself, Senpai.", 'わたしのこと、透明人間だと思ってました？ 全部見てましたよ。センパイがどれだけ無理してるかまで。')],
       'meltryllis': [q('오늘 밤도 가는 거지? 쉬는 건 지루해.', "We're going again tonight, right? Resting is boring.", '今夜も行くんでしょう？ 休むのは退屈なの。'),
                      q('네 서번트, 생각보다 쓸 만하네. …칭찬 아니야.', "Your Servant is more useful than I thought. …That wasn't a compliment.", 'あなたのサーヴァント、思ったより使えるわね。……褒めてないから。'),
                      q('발끝이 아직 저려. 그 여자가 묶어 둔 자리야. 갚아 줄 거야.', "My toes still tingle. That's where that woman bound me. I'll pay her back.", 'つま先がまだ痺れるの。あの女が縛っていた場所よ。返してあげるわ。')],
       'passionlip': [q('저, 오늘은 다들 무사했으면 좋겠어요. …저도 포함해서요.', "I, um, hope everyone stays safe today. …Me included.", 'わたし、今日はみんな無事だといいなって。……わたしも含めて。'),
                      q('손이 너무 커서… 컵을 또 깨 버렸어요. 죄송해요.', "My hands are too big… I broke a cup again. I'm sorry.", '手が大きすぎて……またコップを割っちゃいました。ごめんなさい。'),
                      q('자유롭게 움직이는 거, 아직 조금 무서워요. 그래도 좋아요.', "Moving freely is still a little scary. But I like it.", '自由に動けるの、まだ少し怖いです。でも、うれしいです。')]}
# 호위 센티넬 ({0}: 센티넬 · {1}: 내 서번트)
GC = [('${gN}${J(gN,이)} 키아라 앞을 막아서 일격을 대신 받았다.', None),
      ('${gN}${J(gN,이)} 표정 없이 키아라와 ${mN} 사이로 끼어들었다. 대신 피가 튀었다.', t_('{0~이} 표정 없이 키아라와 {1} 사이로 끼어들었다. 대신 피가 튀었다.', '{0} slipped expressionlessly between Kiara and {1}. Blood spattered in her stead.', '{0}は無表情のままキアラと{1}の間に割り込んだ。代わりに血が飛んだ。')),
      ('${gN}${J(gN,이)} 몸을 던져 키아라를 가렸다. 그 가슴께에서 단 냄새가 났다.', t_('{0~이} 몸을 던져 키아라를 가렸다. 그 가슴께에서 단 냄새가 났다.', '{0} threw themself in front of Kiara. A sweet smell rose from their chest.', '{0}は身を投げ出してキアラを庇った。その胸元から甘い匂いがした。'))]
GK = [('${gN}${J(gN,이)} 옆에서 ${mN}의 발을 묶었다.', None),
      ('${gN}${J(gN,이)} ${mN}의 퇴로를 막아섰다. 다음 수가 무뎌진다.', t_('{0~이} {1}의 퇴로를 막아섰다. 다음 수가 무뎌진다.', "{0} cut off {1}'s retreat. The next move will be dulled.", '{0}が{1}の退路を塞いだ。次の一手が鈍る。')),
      ('${gN}${J(gN,이)} 초점 없는 눈으로 ${mN}${J(mN,을)} 따라붙었다. 숨 돌릴 틈이 사라졌다.', t_('{0~이} 초점 없는 눈으로 {1~을} 따라붙었다. 숨 돌릴 틈이 사라졌다.', '{0} clung to {1} with unfocused eyes. There was no room left to breathe.', '{0}は焦点の合わない目で{1}に食らいついた。息をつく隙が消えた。'))]
GA = {'round': [('${gN}${J(gN,이)} 키아라와 함께 ${mN}${J(mN,을)} 쳤다.', None),
                ('${gN}${J(gN,이)} 키아라의 웃음소리에 맞춰 ${mN}${J(mN,을)} 베고 지나갔다.', t_('{0~이} 키아라의 웃음소리에 맞춰 {1~을} 베고 지나갔다.', "{0} cut past {1} in time with Kiara's laughter.", '{0}はキアラの笑い声に合わせて{1}を斬り抜けた。')),
                ('${gN}의 일격이 ${mN}의 옆구리를 때렸다.', t_('{0}의 일격이 {1}의 옆구리를 때렸다.', "{0}'s blow struck {1} in the side.", '{0}の一撃が{1}の脇腹を打った。'))],
      'magic': [('${gN}${J(gN,이)} 입술만 움직여 영창했다. 빛줄기가 ${mN}에게 꽂혔다.', t_('{0~이} 입술만 움직여 영창했다. 빛줄기가 {1}에게 꽂혔다.', '{0} chanted with only their lips moving. A beam of light pierced {1}.', '{0}は唇だけを動かして詠唱した。光の筋が{1}に突き刺さった。')),
                ('${gN}의 마술이 키아라의 손짓을 따라 ${mN}${J(mN,을)} 덮쳤다.', t_('{0}의 마술이 키아라의 손짓을 따라 {1~을} 덮쳤다.', "{0}'s magecraft followed Kiara's gesture and fell upon {1}.", '{0}の魔術がキアラの手振りに従って{1}に襲いかかった。'))],
      'burst': [('${gN}${J(gN,이)} 마력을 터뜨리며 ${mN}에게 부딪쳤다.', t_('{0~이} 마력을 터뜨리며 {1}에게 부딪쳤다.', '{0} slammed into {1} in a burst of mana.', '{0}は魔力を炸裂させながら{1}にぶつかった。')),
                ('${gN}의 일격에 실린 마력이 ${mN}의 어깨에서 터졌다.', t_('{0}의 일격에 실린 마력이 {1}의 어깨에서 터졌다.', "The mana in {0}'s blow burst against {1}'s shoulder.", '{0}の一撃に込められた魔力が{1}の肩で弾けた。'))]}
UI = [n_('함께 싸우는 서번트', 'Servants fighting with you', '共に戦うサーヴァント'), n_('키아라를 지키는 센티넬', 'Sentinels guarding Kiara', 'キアラを守るセンチネル'),
      n_('보구 남음', 'NP ready', '宝具あり'), n_('보구 씀', 'NP used', '宝具使用済み')]

def lit(lines): return '[' + ','.join('`' + a + '`' for a, _ in lines) + ']'
js = lambda x: json.dumps(x, ensure_ascii=False)
HELP = ("  // 11-13: 키아라전의 동행(BB · 멜트 · 립)과 호위의 말 · 행동\n"
        "  const BXA={bbS:" + js(BB_START) + ",bbA:" + js(BB_ACT) + ",bbT:" + js(BB_TEASE) + ",mS:" + js(MELT_START) + ",mH:" + js(MELT_HIT) + ",lS:" + js(LIP_START) + ",lH:" + js(LIP_HIT) + ",day:" + js(DAY) + "};\n"
        "  const bxBBOn=()=>{ const c=BXW(); return !!(c&&c.bbAlly&&S.hero!=='bb'&&bxBBP()); };\n"
        "  const bxEgoN=id=>H_BY[id].name;\n"
        "  function bxAllyRound(b){ const c=BXW(), w=W(); if(!c||!w.heroAlive) return;\n"
        "    if(!b.bxHi){ b.bxHi=1; if(bxBBOn()) log(`BB: “${pick(BXA.bbS)}”`,'voice');\n"
        "      for(const id of (c.freed||[])) log(`${bxEgoN(id)}: “${pick(id==='meltryllis'?BXA.mS:BXA.lS)}”`,'voice'); return; }\n"
        "    if(bxBBOn()){ b.bxBBn=b.bxBBn||0; if(b.bxBBn<2&&ch(.3)){ b.bxBBn++; log(pickNR(BXA.bbA,'bxbbA'),'war'); } else if(!b.bxBBt&&ch(.15)){ b.bxBBt=1; log(`BB: “${pickNR(BXA.bbT,'bxbbT')}”`,'voice'); } } }\n"
        "  function bxAllyDay(c,w){ if(c.stage!==3||!w.heroAlive||!(w.day>c.descD)||c.allyDayD===w.day) return; c.allyDayD=w.day; if(!ch(.7)) return;\n"
        "    const who=[...(bxBBOn()?['bb']:[]),...(c.freed||[])]; if(!who.length) return; const id=pick(who);\n"
        "    log(`${id==='bb'?'BB':bxEgoN(id)}: “${pickNR(BXA.day[id],'bxday'+id)}”`,'voice'); }\n")
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("  // 키아라전의 합마다: 호위 · 풀려난 멜트릴리스와 패션립\n", HELP + "  // 키아라전의 합마다: 호위 · 풀려난 멜트릴리스와 패션립\n")
    # 합마다: 첫 합 인사 · BB
    rp("const k0=b.bxK0!=null?b.bxK0:e.hp, lost=Math.max(0,k0-e.hp), m=bxMult(false); let cov=false;",
       "const k0=b.bxK0!=null?b.bxK0:e.hp, lost=Math.max(0,k0-e.hp), m=bxMult(false); let cov=false; bxAllyRound(b); const mN=hero().name;")
    # 호위의 행동 묘사
    rp("log(`${gN}${J(gN,이)} 키아라 앞을 막아서 일격을 대신 받았다.`,'war');", "log(pickNR(" + lit(GC) + ",'bxgC'),'war');")
    rp("log(`${gN}${J(gN,이)} 옆에서 ${hero().name}의 발을 묶었다.`,'war');", "log(pickNR(" + lit(GK) + ",'bxgK'),'war');")
    rp("log(`${gN}${J(gN,이)} 키아라와 함께 ${hero().name}${J(hero().name,을)} 쳤다.`,'war');",
       "const gh=H_BY[g.hero], GP=npcParams(g).p, mh=hero(), MP=myParams().p; let gk='round', gv=-9; for(const kk of atkKinds(gh)){ const v=atkVal(kk,gh,GP,mh,MP,w.tod==='밤'); if(v>gv+.02){ gv=v; gk=kk; } }\n"
       "        const GA={round:" + lit(GA['round']) + ",magic:" + lit(GA['magic']) + ",burst:" + lit(GA['burst']) + "}; log(pickNR(GA[gk]||GA.round,'bxgA'+gk),'war');")
    # 멜트 · 립이 칠 때 가끔 한마디
    rp("log(`${nm}${J(nm,이)} 옆에서 키아라에게 일격을 보탰다.`,'war'); }",
       "log(`${nm}${J(nm,이)} 옆에서 키아라에게 일격을 보탰다.`,'war'); if(ch(.35)) log(`${nm}: “${pickNR(id==='meltryllis'?BXA.mH:BXA.lH,'bxeH'+id)}”`,'voice'); }")
    # 낮마다
    rp("function bxDay(){ const w=W(), c=BXW(); if(!c||c.done) return false; bxFix();", "function bxDay(){ const w=W(), c=BXW(); if(!c||c.done) return false; bxFix(); bxAllyDay(c,w);")
    # 화면: 전투 카드
    rp("function compHtml(w){",
       "// 11-13: 키아라전 카드 — 함께 싸우는 서번트(BB · 멜트 · 립) · 키아라를 지키는 센티넬\n"
       "function bxCardRows(w,e,side){ const c=w&&w.crisis; if(!c||c.type!=='beast3R'||!e||!e.bx) return ''; const hw=v=>v>70?'멀쩡함':v>40?'다침':'크게 다침';\n"
       "  const chip=(id,t,unk)=>`<span class=\"cf\">${faceHtml(id,20,{unk})}${esc(t)}</span>`;\n"
       "  if(side==='me'){ const L=[]; if(c.bbAlly&&Sim.S.hero!=='bb'){ const u=c.units.find(x=>x.cx==='bb'&&x.alive)||(c.bb&&c.bb.at==='npc'?w.pairs.find(p=>p.i===c.bb.i&&p.alive):null); if(u) L.push(chip('bb',`BB · ${hw(u.hp)}`)); }\n"
       "    for(const id of (c.freed||[])) L.push(chip(id,`${Sim.H_BY[id].name} · ${(c.egoNP||{})[id]?'보구 씀':'보구 남음'}`));\n"
       "    return L.length?`<div class=\"comp\"><small>함께 싸우는 서번트</small>${L.join('')}</div>`:''; }\n"
       "  const gs=c.units.filter(u=>u.cx==='sent'&&u.alive&&u.guard); if(!gs.length) return '';\n"
       "  return `<div class=\"comp\"><small>키아라를 지키는 센티넬 ${gs.length}</small>${gs.map(u=>chip(u.hero,`${u.revealed?Sim.H_BY[u.hero].name:Sim.cn(u)} · KP ${u.kp} · ${hw(u.hp)}`,!u.revealed)).join('')}</div>`; }\n"
       "function compHtml(w){")
    rp("${compHtml(w)}${MD?modsHtml(MD.me,'me'):''}</div>`;", "${compHtml(w)}${bxCardRows(w,e,'me')}${MD?modsHtml(MD.me,'me'):''}</div>`;")
    rp("<div class=\"np2\">보구 ${e.artKnown?`${esc(eArt.n)} · ${eArt.r}`:'모름'}</div>${MD?modsHtml(MD.en,'en'):''}</div>`;",
       "<div class=\"np2\">보구 ${e.artKnown?`${esc(eArt.n)} · ${eArt.r}`:'모름'}</div>${bxCardRows(w,e,'foe')}${MD?modsHtml(MD.en,'en'):''}</div>`;")
    # 11-13: 함께 싸우는 조도 같은 모양으로(얼굴 · 상태 · 보구 남음/씀)
    rp("return `<div class=\"comp\"><small>함께 싸우는 조</small>${b.ctx.comp.map(i=>{ const p=w.pairs.find(x=>x.i===i); if(!p) return ''; const st=!p.alive?'쓰러짐':out.includes(i)?'물러남':hw(p.hp); return `<span class=\"${!p.alive||out.includes(i)?'off':''}\">${esc(Sim.pName(p))} · ${st}</span>`; }).join('')}</div>`; }",
       "const np=b.compNP||[]; return `<div class=\"comp\"><small>함께 싸우는 조</small>${b.ctx.comp.map(i=>{ const p=w.pairs.find(x=>x.i===i); if(!p) return ''; const gone=!p.alive||out.includes(i), st=!p.alive?'쓰러짐':out.includes(i)?'물러남':hw(p.hp); return `<span class=\"cf${gone?' off':''}\">${faceHtml(p.hero,20,{unk:!p.revealed})}${esc(Sim.pName(p))} · ${st}${gone?'':` · ${np.includes(i)?'보구 씀':'보구 남음'}`}</span>`; }).join('')}</div>`; }")
    rp(".comp{margin-top:5px;", ".comp .cf{display:inline-flex;align-items:center;gap:4px}.comp .cf .pf{flex:none}.comp .cf.off .pf{opacity:.45}.comp{margin-top:5px;")
    s, nd, nt = i18n.add(s, D, T)
    print('bxally miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
