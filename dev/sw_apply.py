"""⑤ 에필로그 애정 전환 — 「에필로그 애정 전환 상세안」(11-10, 19세 · 사별 3년 · 한 번만 묻기). 사용: python3 sw_apply.py <game.html>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

# 서번트 대답: 존댓말 p · 반말 c · 왕 말투 r · 친근한 반말 k · 서번트별 x · 말이 없는 서번트 m(지문)
SW = {
 'grow': {'p': '“…그렇군요. 이제 당신을 아이로 보지는 않겠습니다. 천천히, 처음부터 다시 걸어가도 될까요.”',
          'c': '“…그래. 이제 너를 꼬마 취급할 수는 없겠군. 서두르지 말고, 천천히 가자.”',
          'r': '“…그런가. 그대는 이제 어엿한 어른이로구나. 서두르지 않으마. 천천히 와라.”',
          'k': '“…헤헤, 그렇구나. 이제 진짜 어른이네. 그럼 우리, 천천히 가 보자.”',
          'x': {'teach': '“…허어, 그렇습니까. 이제 꼬마 취급은 못 하겠군요. 서두르지 말고, 천천히 가 보입지요.”',
                'sigurd': '“…그렇군. 귀하는 이제 아이가 아니다. 서두르지 않겠다. 천천히, 처음부터 걸어가자.”',
                'shuten': '“…그렇나. 인자 니를 아 취급은 몬 하겠네. 서두르지 말고, 천천히 가 보자.”'},
          'm': '{N은} 한참 당신을 바라보다가, 조심스럽게 손을 내밀었다. 처음 만났을 때와는 다른 손길이었다.'},
 'spring': {'p': '“…그분의 자리를 대신하려는 게 아닙니다. 당신 곁의 다른 자리라면, 기꺼이 앉겠습니다.”',
          'c': '“…그 사람 자리를 빼앗을 생각은 없다. 네 옆에 다른 자리 하나면 충분해.”',
          'r': '“…그대가 사랑한 이의 자리를 넘보지는 않으마. 다만 그 곁에 서는 것은 허락해 다오.”',
          'k': '“…그 사람 대신은 못 해. 그래도 네 옆자리라면, 내가 맡을게.”',
          'x': {'teach': '“…그분 자리를 넘볼 생각은 없습지요. 다만 옆자리 하나라면, 소생이 맡겠습니다요.”',
                'sigurd': '“…그분의 자리를 대신하지는 않겠다. 귀하 곁의 다른 자리라면, 기꺼이 서겠다.”',
                'shuten': '“…그 사람 자리를 뺏을 생각은 없다. 니 옆자리 하나면 충분하다 아이가.”'},
          'm': '{N은} 말없이 당신 곁에 앉았다. 그 사람이 앉던 자리가 아니라, 그 옆이었다.'}}
import json
J_ = lambda x: json.dumps(x, ensure_ascii=False)

CODE = """  // ---- 에필로그 애정 전환 (「달라진 거리」 · 「다시 찾아온 봄」) ----
  // 우정으로 정해진 이유가 미성년(minor) · 배우자(spouse)였던 생에서, 곁에 남은 서번트와 한 번만 묻는다. 서번트가 먼저 고백하지 않는다
  const SW_LN=__SW__;
  function swLine(h,k){ const L=SW_LN[k], r=VREG(h); if(r==='mute') return nf(L.m,h); let l=L.x[h.id]||(r==='polite'?L.p:r==='royal'?L.r:CAS_V.has(h.id)?L.k:L.c); if(r==='royal') l=meSw(h,l); return spkQ(h,l); }
  function relSwOk(r,why){ if(!stayHome()||S.flags.stayDied||!r||r.track!=='friend'||r.why!==why||r.swAsked||r.stage<1||S.war.trust<75) return false;
    const sp=S.fam&&S.fam.spouse;
    if(why==='minor') return S.age>=19&&S.age-S.warAge>=2&&!(sp&&sp.alive);
    if(!sp||sp.alive) return false; if(sp.died==null) sp.died=S.age; return S.age-sp.died>=3; }
  function relSwitch(why){ const r=relOf(), h=H_BY[S.hero], sp=S.fam&&S.fam.spouse, n=Math.max(1,S.year-S.warYear); r.swAsked=1; S.epi.relUsed=(S.epi.relUsed||[]).concat(why==='minor'?'sw_grow':'sw_spring');
    const go=()=>{ r.mx=r.mx||{}; r.mx.friend=Math.max(r.mx.friend||0,r.stage); r.track='love'; r.why=null; r.sw={from:why,y:S.age}; r.stage=1; r.wait=0; r.mx.love=Math.max(r.mx.love||0,1); r.pt=Math.max(30,Math.min(59,Math.round(r.pt/2))); r.open=1; mark('joy');
      return `${swLine(h,why==='minor'?'grow':'spring')} ${h.name}${J(h.name,과)}의 인연이 애정으로 바뀌었다. 「호감」`; };
    const stay=()=>{ r.why='stay'; return why==='minor'?`${h.name}${J(h.name,은)} 웃으며 고개를 끄덕였다. 둘은 여전히, 서로에게 가장 가까운 친구였다.`:`${h.name}${J(h.name,은)} 말없이 찻잔을 하나 더 내려놓았다. 셋이 함께 앉던 자리였다.`; };
    if(why==='minor') decide({title:'달라진 거리',body:`${h.name}${J(h.name,과)} 함께 산 지 ${n}년. 처음 만났을 때 당신은 열일곱이었다. 오늘 ${h.name}${J(h.name,은)} 무심코 당신을 아이 부르듯 부르려다, 말끝을 삼켰다. 당신도 알고 있었다. 친구라고 부르기에는, 마음이 조금 달라졌다는 것을.`,choices:[
      {t:'마음을 말한다',auto:true,f:go},{t:'지금 이대로가 좋다',f:stay}]});
    else decide({title:'다시 찾아온 봄',body:`${sp?sp.name:'그 사람'}${J(sp?sp.name:'그 사람',을)} 떠나보낸 지 ${Math.max(3,S.age-(sp&&sp.died!=null?sp.died:S.age-3))}년. 그동안 ${h.name}${J(h.name,은)} 한 번도 그 이름을 잊으라고 하지 않았다. 오늘 아침, 당신은 처음으로 ${h.name}의 웃는 얼굴에 오래 눈이 머물렀다.`,choices:[
      {t:'곁에 있어 달라고 말한다',auto:true,f:go},{t:'그 사람을 마음에 둔 채로 지낸다',f:stay}]}); }
""".replace('__SW__', J_(SW))

TR_D = [('달라진 거리', 'A Different Distance', '変わった距離'), ('다시 찾아온 봄', 'Spring Comes Again', 'ふたたび訪れた春'),
 ('마음을 말한다', 'Say what you feel', '気持ちを伝える'), ('지금 이대로가 좋다', 'You like things as they are', '今のままがいい'),
 ('곁에 있어 달라고 말한다', 'Ask them to stay by your side', 'そばにいてほしいと言う'), ('그 사람을 마음에 둔 채로 지낸다', 'Live on with that person still in your heart', 'あの人を心に置いたまま暮らす'),
 ('우정 · 이대로 친구로 지내기로 함', 'Friendship · Chose to stay friends', '友情 · このまま友として過ごすことにした'),
 ('“…그렇군요. 이제 당신을 아이로 보지는 않겠습니다. 천천히, 처음부터 다시 걸어가도 될까요.”', '“…I see. I will no longer see you as a child. May we walk it again, slowly, from the beginning?”', '「…そうですか。もうあなたを子どもとは見ません。ゆっくり、最初からもう一度歩いてもいいでしょうか」'),
 ('“…그래. 이제 너를 꼬마 취급할 수는 없겠군. 서두르지 말고, 천천히 가자.”', '“…Right. I can\'t treat you like a kid anymore. No rush. Let\'s take it slow.”', '「…そうか。もうお前を子ども扱いはできないな。急がず、ゆっくり行こう」'),
 ('“…그런가. 그대는 이제 어엿한 어른이로구나. 서두르지 않으마. 천천히 와라.”', '“…Is that so. You have become a proper adult. I shall not hurry. Come to me slowly.”', '「…そうか。そなたはもう立派な大人なのだな。急かしはせぬ。ゆるりと来るがよい」'),
 ('“…헤헤, 그렇구나. 이제 진짜 어른이네. 그럼 우리, 천천히 가 보자.”', '“…Heh, I see. You\'re a real grown-up now. Then let\'s take it slow, the two of us.”', '「…へへ、そっか。もう本当に大人なんだね。じゃあ、ゆっくり行ってみよう」'),
 ('“…허어, 그렇습니까. 이제 꼬마 취급은 못 하겠군요. 서두르지 말고, 천천히 가 보입지요.”', '“…Well, well, is that so. I can\'t be treating you like a brat anymore. No hurry—let\'s take it slow, eh.”', '「…ほう、そうですかい。もうガキ扱いはできませんな。急がず、ゆっくり参りましょうや」'),
 ('“…그렇군. 귀하는 이제 아이가 아니다. 서두르지 않겠다. 천천히, 처음부터 걸어가자.”', '“…I see. You are no longer a child. I will not rush. Let us walk slowly, from the beginning.”', '「…そうか。貴殿はもう子どもではない。急ぎはしない。ゆっくり、最初から歩いていこう」'),
 ('“…그렇나. 인자 니를 아 취급은 몬 하겠네. 서두르지 말고, 천천히 가 보자.”', '“…That so? Can\'t go treatin\' ya like a little one no more. No rush. Let\'s take it slow.”', '「…そうなん。もうあんたを子ども扱いはでけへんなぁ。急がんと、ゆっくり行こか」'),
 ('“…그분의 자리를 대신하려는 게 아닙니다. 당신 곁의 다른 자리라면, 기꺼이 앉겠습니다.”', '“…I do not mean to take their place. But if there is another place at your side, I will gladly take it.”', '「…その方の代わりになろうというのではありません。あなたの隣の別の席なら、喜んで座ります」'),
 ('“…그 사람 자리를 빼앗을 생각은 없다. 네 옆에 다른 자리 하나면 충분해.”', '“…I won\'t take their place. One other seat beside you is enough.”', '「…その人の場所を奪う気はない。お前の隣に、別の席がひとつあれば十分だ」'),
 ('“…그대가 사랑한 이의 자리를 넘보지는 않으마. 다만 그 곁에 서는 것은 허락해 다오.”', '“…I shall not covet the place of the one you loved. But allow me to stand beside it.”', '「…そなたが愛した者の座を望みはせぬ。ただ、その傍らに立つことは許してくれ」'),
 ('“…그 사람 대신은 못 해. 그래도 네 옆자리라면, 내가 맡을게.”', '“…I can\'t replace them. But the seat beside you—I\'ll take that one.”', '「…その人の代わりはできないよ。でも、君の隣の席なら、わたしが引き受ける」'),
 ('“…그분 자리를 넘볼 생각은 없습지요. 다만 옆자리 하나라면, 소생이 맡겠습니다요.”', '“…I\'d never presume to take their place. But a seat beside you, now—that this humble one will gladly take.”', '「…その方の座を狙うつもりはありやせん。ただ隣の席ひとつなら、小生がお引き受けしやす」'),
 ('“…그분의 자리를 대신하지는 않겠다. 귀하 곁의 다른 자리라면, 기꺼이 서겠다.”', '“…I will not take their place. If there is another place at your side, I will gladly stand there.”', '「…その方の代わりにはならない。貴殿の傍らの別の場所なら、喜んで立とう」'),
 ('“…그 사람 자리를 뺏을 생각은 없다. 니 옆자리 하나면 충분하다 아이가.”', '“…Ain\'t gonna steal their spot. A seat next to ya is plenty, ain\'t it.”', '「…その人の場所を取る気はあらへん。あんたの隣ひとつで十分やろ」')]
TR_T = [('{0~은} 한참 당신을 바라보다가, 조심스럽게 손을 내밀었다. 처음 만났을 때와는 다른 손길이었다.', '{0} looked at you for a long while, then carefully held out a hand. It was a different touch from the day you first met.', '{0}は長いことあなたを見つめ、そっと手を差し出した。初めて会ったときとは違う手つきだった。'),
 ('{0~은} 말없이 당신 곁에 앉았다. 그 사람이 앉던 자리가 아니라, 그 옆이었다.', '{0} sat down beside you without a word. Not in the seat that person used to take, but next to it.', '{0}は黙ってあなたの隣に座った。あの人が座っていた席ではなく、その隣に。'),
 ('{0~과}의 인연이 애정으로 바뀌었다. 「호감」', 'Your bond with {0} turned to affection. “Fondness”', '{0}との縁が愛情に変わった。「好感」'),
 ('{0~은} 웃으며 고개를 끄덕였다. 둘은 여전히, 서로에게 가장 가까운 친구였다.', '{0} smiled and nodded. The two of you were still each other\'s closest friend.', '{0}は笑って頷いた。ふたりは今も、互いにいちばん近い友だった。'),
 ('{0~은} 말없이 찻잔을 하나 더 내려놓았다. 셋이 함께 앉던 자리였다.', '{0} quietly set down one more teacup. It was where the three of you used to sit together.', '{0}は黙ってティーカップをもうひとつ置いた。三人で一緒に座っていた席だった。'),
 ('{0~과} 함께 산 지 {1}년. 처음 만났을 때 당신은 열일곱이었다. 오늘 {2~은} 무심코 당신을 아이 부르듯 부르려다, 말끝을 삼켰다. 당신도 알고 있었다. 친구라고 부르기에는, 마음이 조금 달라졌다는 것을.',
  '{1} years since you began living with {0}. You were seventeen when you first met. Today {2} almost called you the way one calls a child, then swallowed the words. You knew it too. Your heart had changed a little too much to call this just friendship.',
  '{0}と暮らして{1}年。初めて会ったとき、あなたは十七だった。今日、{2}は何気なく子どもを呼ぶようにあなたを呼びかけて、言葉を飲み込んだ。あなたにも分かっていた。友と呼ぶには、心が少し変わってしまったことを。'),
 ('{0~을} 떠나보낸 지 {1}년. 그동안 {2~은} 한 번도 그 이름을 잊으라고 하지 않았다. 오늘 아침, 당신은 처음으로 {3}의 웃는 얼굴에 오래 눈이 머물렀다.',
  '{1} years since you said goodbye to {0}. In all that time {2} never once told you to forget that name. This morning, for the first time, your eyes lingered on {3}\'s smile.',
  '{0}を見送って{1}年。そのあいだ{2}は一度もその名を忘れろとは言わなかった。今朝、あなたは初めて{3}の笑顔に長く目を留めた。')]

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:60], k)); return
        s = s.replace(o, n)
    rp("  const EP_REL=[\n", CODE + """  const EP_REL=[
    // 애정 전환: 우정으로 정해진 이유가 미성년 · 배우자였던 생 (한 번만 묻는다)
    {id:'sw_grow',w:6,c:(r)=>relSwOk(r,'minor'),f:()=>relSwitch('minor')},
    {id:'sw_spring',w:5,c:(r)=>relSwOk(r,'spouse'),f:()=>relSwitch('spouse')},
""")
    rp("if(F.spouse&&F.spouse.alive){ F.spouse.age++; if(ch(Math.min(.5,baseQ(F.spouse.age)))){F.spouse.alive=false;",
       "if(F.spouse&&F.spouse.alive){ F.spouse.age++; if(ch(Math.min(.5,baseQ(F.spouse.age)))){F.spouse.alive=false;F.spouse.died=S.age;")
    rp("else if(x.id==='spouse'&&F.spouse) F.spouse.alive=false;", "else if(x.id==='spouse'&&F.spouse){ F.spouse.alive=false; F.spouse.died=S.age; }")
    rp("const REL_WHY={spouse:'우정 · 배우자가 있어 우정으로 발전',minor:'우정 · 미성년이라 우정으로 발전',only:'우정 · 이 서번트와는 우정으로만 발전'};",
       "const REL_WHY={spouse:'우정 · 배우자가 있어 우정으로 발전',minor:'우정 · 미성년이라 우정으로 발전',only:'우정 · 이 서번트와는 우정으로만 발전',stay:'우정 · 이대로 친구로 지내기로 함'};")
    s, nd, nt = i18n.add(s, TR_D, TR_T)
    open(P, 'w', encoding='utf-8').write(s); print(os.path.basename(P), 'miss', miss, 'tr', nd, nt)
