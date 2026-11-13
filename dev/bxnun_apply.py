"""11-13: 비스트 Ⅲ/R의 '이름 모를 수녀'(정체는 키아라)를 매장기관 수녀 그대로 쓰지 않게.
- 소원: 직접 말할 땐 겉말(구원) · 정찰로 캐내면 속마음 · 정체가 드러나면 진짜 소원 (쾌락은 달콤함 · 꿈 · 잠으로만)
- 전투 대사, 마스터 이벤트(고해소), 전투 성향 설명을 수녀 전용으로
- '대행자에게 알린다'에서 사도 사냥꾼으로 뽑히지 않게
사용: python3 bxnun_apply.py <game.html>"""
import sys, json, i18n

W = [('길 잃은 이들을 모두 구원하는 것', 'To save every lost soul', '迷える人々をみな救うこと'),
     ('세상의 모든 꿈을 혼자서 달게 꾸는 것', 'To dream every dream in the world, sweetly, all by herself', '世界のすべての夢を、ひとりで甘く見ること'),
     ('세상 모든 것을 녹여, 저 혼자 영원히 달콤한 꿈에 잠기는 것', 'To melt down everything in the world and sink alone, forever, into a sweet dream', '世界のすべてを溶かし、自分ひとりで永遠に甘い夢に沈むこと')]
PURE = ('성배는 맑았다. 수녀는 그 맑은 물에 혼자 오래 잠겨 있었다.', 'The Grail was clear. The nun lay alone in its clear water for a long time.', '聖杯は澄んでいた。修道女はその澄んだ水に、ひとり長く浸っていた。')
DARK = ('그 겨울, 도시는 길고 달콤한 잠에 빠졌다. 깨어난 것은 단 한 사람뿐이었다.', 'That winter, the city fell into a long, sweet sleep. Only one person ever woke.', 'その冬、街は長く甘い眠りに落ちた。目を覚ましたのは、ただひとりだけだった。')
HINT = ('구원을 말하던 수녀의 소원치고는, 그 안에 다른 사람이 없었다.', 'For the wish of a nun who spoke of salvation, there was no one else in it.', '救いを説く修道女の願いにしては、そこに他の誰もいなかった。')
STY = ('밤마다 다른 조를 찾아간다', 'Seeks out a different team every night', '夜ごとに別の組を訪ねていく')
L = {
 'open': [('어머, 길을 잃으셨나요? 괜찮아요, 제가 다 받아 드릴게요.', "Oh my, have you lost your way? It's all right. I'll take all of you in.", 'あら、迷われたのですか？ 大丈夫、私が全部受け止めてさしあげます。'),
          ('이런 밤에 만나다니, 인연이네요.', 'Meeting on a night like this — it must be fate.', 'こんな夜にお会いするなんて、ご縁ですね。'),
          ('기도하러 오셨다면 잘 오셨어요.', 'If you came to pray, you came to the right place.', 'お祈りにいらしたのなら、ようこそ。')],
 'mid': [('아파하지 마세요. 그 얼굴, 저만 보기 아까우니까요.', "Don't be in pain. A face like that is wasted on me alone.", '痛がらないで。その顔、私だけが見るのはもったいないですから。'),
         ('조금만 더 버텨 주세요. 그래야 더 달콤하니까요.', "Hold on a little longer. It's sweeter that way.", 'もう少しだけ耐えてくださいね。そのほうが甘いですから。'),
         ('서두르지 않아도 돼요. 밤은 길어요.', "There's no need to hurry. The night is long.", '急がなくていいんですよ。夜は長いですから。')],
 'low': [('구원이요? 네, 그럼요. …저부터요.', 'Salvation? Yes, of course. …Starting with me.', '救い？ ええ、もちろん。…まずは私から。'),
         ('어머, 옷이 더러워졌네요.', 'Oh dear, my habit is soiled.', 'あら、服が汚れてしまいました。'),
         ('오늘은 이쯤에서 꿈을 깨야겠어요.', 'I suppose I should wake from this dream for tonight.', '今夜はこのあたりで夢から覚めないといけませんね。')],
 'win': [('편히 쉬세요. 좋은 꿈 꾸시고요.', 'Rest easy. Sweet dreams.', 'ゆっくり休んでくださいね。良い夢を。'),
         ('다 끝났어요. 이제 아무것도 걱정하지 마세요.', "It's all over. You needn't worry about anything now.", 'もう終わりましたよ。何も心配しなくていいんです。')],
 'reply': [('저는 그저 길 잃은 분들을 구원하고 싶을 뿐이에요.', 'I only wish to save those who have lost their way.', '私はただ、迷える方々を救いたいだけなんです。'),
           ('소원이요? 모두가 편해지는 거예요. 정말이에요.', 'My wish? For everyone to be at ease. Truly.', '願い？ みんなが楽になることですよ。本当です。'),
           ('저를 의심하시나요? 슬프네요. 조금은 기쁘기도 하고요.', 'You doubt me? How sad. And a little delightful, too.', '私をお疑いですか？ 悲しいです。少しだけ、嬉しくもありますけれど。')]}
EV_T = ('고해소', 'The Confessional', '告解室')
EV_B = ('밤늦은 성당, 고해소 칸막이 너머에서 {0}의 목소리가 들렸다. “고해하러 오셨나요? 무엇이든 들어 드릴게요.”',
        "In the church late at night, {0}'s voice came from behind the confessional screen. “Have you come to confess? I'll listen to anything.”",
        '夜更けの聖堂、告解室の仕切りの向こうから{0}の声がした。「告解にいらしたのですか？ 何でも聞いてさしあげますよ。」')
EV_C = [('고해한다', 'Confess', '告解する'), ('무엇을 위해 싸우는지 묻는다', 'Ask what she fights for', '何のために戦うのか尋ねる')]
EV_R = [('칸막이 너머의 수녀는 끝까지 조용히 들었다. 다 듣고 나서 작게 웃었다. “어머, 정말 달콤한 고민이네요.” 그 목소리는 죄를 듣는 사람이 아니라 맛을 보는 사람의 것이었다.',
         'The nun behind the screen listened quietly to the end. When it was over, she laughed softly. “Oh my, what a sweet worry.” It was the voice not of someone hearing sins, but of someone tasting them.',
         '仕切りの向こうの修道女は最後まで静かに聞いていた。聞き終えると小さく笑った。「あら、本当に甘いお悩みですね。」その声は罪を聞く者ではなく、味わう者のものだった。'),
        ('“구원이요. 길 잃은 분들을 모두.” 대답에는 막힘이 없었다. 칸막이 너머에서 사탕을 굴리는 듯한 소리가 났다.',
         '“Salvation. For everyone who has lost their way.” The answer came without a pause. From behind the screen came a sound like a candy rolling on a tongue.',
         '「救いです。迷える方々みんなの。」答えに淀みはなかった。仕切りの向こうから、飴玉を転がすような音がした。'),
        ('성당 문을 나설 때까지 등 뒤에서 콧노래가 들렸다.', 'Humming followed you until you were out the church door.', '聖堂の扉を出るまで、背後から鼻歌が聞こえていた。')]

js = lambda x: json.dumps(x, ensure_ascii=False)
MLX_BXN = {k: [r[0] for r in v] for k, v in L.items()}
HELP = f"""
  // 수녀(키아라)의 소원: 직접 말할 땐 겉말(구원) · 정찰로 캐내면 속마음 · 정체가 드러나면 진짜 소원 (11-13)
  const BXN_W={js([w[0] for w in W])};
  const bxNunLv=p=>{{ const c=BXW(); return c&&(c.nunKnown||c.stage>=3)?2:p&&p.bxWishTrue?1:0; }};
  const bxAR=p=>({{...ARCHE.find(a=>a.id==='burial'),wish:BXN_W[bxNunLv(p)],pure:{js(PURE[0])},dark:{js(DARK[0])}}});
  const MLX_BXN={js(MLX_BXN)};
  const BXN_EV=[{{c:p=>true,f:p=>decide({{title:{js(EV_T[0])},body:`{EV_B[0].replace('{0}', '${p.mname}')}`,war:true,choices:[
      {{t:{js(EV_C[0][0])},auto:true,f:()=>{{addIntel(p,30,'talk');return {js(EV_R[0][0])}}}}},
      {{t:{js(EV_C[1][0])},f:()=>{{addIntel(p,15,'talk');return {js(EV_R[1][0])}}}}},
      {{t:'자리를 뜬다',f:()=>{js(EV_R[2][0])}}}]}})}}];"""

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("  const bxNunP=()=>{ const c=BXW(); return c&&c.nun?pairBy(c.nun):null; };",
       "  const bxNunP=()=>{ const c=BXW(); return c&&c.nun?pairBy(c.nun):null; };" + HELP)
    rp("const AR=p=>ARCHE.find(a=>a.id===p.aid)||ARCHE[0];", "const AR=p=>p&&p.bxNun?bxAR(p):ARCHE.find(a=>a.id===p.aid)||ARCHE[0];")
    rp("if(loc&&!t.wishKnown&&t.intel>=50){ t.wishKnown=true; log(`${t.mname}의 소원은 ‘${AR(t).wish}’이라고 한다.`,'n'); }",
       "if(loc&&(!t.wishKnown||t.bxNun&&!t.bxWishTrue)&&t.intel>=50){ t.wishKnown=true; if(t.bxNun) t.bxWishTrue=1; log(`${t.mname}의 소원은 ‘${AR(t).wish}’이라고 한다.`,'n'); if(t.bxNun&&bxNunLv(t)<2) log(" + js(HINT[0]) + ",'n'); }")
    rp("log(`${e.mname}의 소원은 ‘${ar.wish}’이라고 했다.`,'n');", "log(`${e.mname}의 소원은 ‘${e.bxNun?BXN_W[0]:ar.wish}’이라고 했다.`,'n');")
    rp("    const X=MLX[e.aid];", "    const X=e.bxNun?MLX_BXN:MLX[e.aid];")
    rp("(MLX[e.aid]&&MLX[e.aid].reply)", "((e.bxNun?MLX_BXN:MLX[e.aid])||{}).reply")
    rp("MASTER_EV[p.aid]", "(p.bxNun?BXN_EV:MASTER_EV[p.aid])", 3)
    rp("const h=alivePairs().find(x=>x.aid==='executor'||x.aid==='burial');", "const h=alivePairs().find(x=>(x.aid==='executor'||x.aid==='burial')&&!x.bxNun);")
    rp("STYLE:()=>STYLE,", "STYLE:()=>STYLE, AR,")
    rp("const ar=Sim.ARCHE.find(a=>a.id===p.aid)||{};", "const ar=(Sim.AR?Sim.AR(p):Sim.ARCHE.find(a=>a.id===p.aid))||{};")
    rp("(Sim.STYLE()[p.aid]||{}).d||''", "(p.bxNun?" + js(STY[0]) + ":(Sim.STYLE()[p.aid]||{}).d||'')")
    D = list(W) + [PURE, DARK, HINT, STY, EV_T] + EV_C + EV_R
    for v in L.values():
        for ko, en, ja in v:
            D.append((ko, en, ja)); D.append(('“' + ko + '”', '“' + en + '”', '「' + ja.rstrip('。') + '」'))
    s, nd, nt = i18n.add(s, D, [EV_B])
    print('bxnun miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
