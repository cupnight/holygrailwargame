"""② 비스트 Ⅲ/R 최종전 패배 뒤의 에필로그 (11-12): 단맛의 유혹 3단 · 연작 「단꿈의 도시」 · 도시 · 사람 · 서번트 · 키아라의 흔적 · 마지막 한 입.
한 생에 키아라 패배 사건은 연작 포함 6개까지. 사용: python3 bxe_apply.py <game.html>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

TR = []  # (ko, en, ja) — 이름 없는 문장
TT = []  # 틀(이름 · 수가 들어가는 문장)
def k(ko, en, ja):
    (TT if '{' in ko else TR).append((ko, en, ja)); return ko
J = lambda x: json.dumps(x, ensure_ascii=False)

# ---- A. 단맛의 유혹 ----
SW1 = [k('가게 앞에서 시식용 과자를 하나 받아 먹었다. 혀끝에 닿는 순간 그 겨울의 단맛이 그대로 돌아왔다. 눈을 감으면 그 꿈으로 돌아갈 수 있을 것 같았다.',
         'You took a free sample of a sweet in front of a shop. The moment it touched your tongue, the sweetness of that winter came back whole. If you closed your eyes, it felt like you could go back to that dream.',
         '店先で試食の菓子をひとつもらった。舌先に触れた瞬間、あの冬の甘さがそのまま戻ってきた。目を閉じれば、あの夢へ帰れる気がした。'),
       k('낮잠에서 깨기 직전, 누군가 귓가에서 웃었다. 깨어난 뒤에도 입안이 달았다. 다시 눈을 감고 싶었다.',
         'Just before you woke from a nap, someone laughed beside your ear. Even after waking, your mouth tasted sweet. You wanted to close your eyes again.',
         '昼寝から覚める直前、誰かが耳元で笑った。目覚めたあとも口の中が甘かった。もう一度目を閉じたかった。'),
       k('길에서 스친 낯선 사람이 미소 지었다. 그 미소가 그 겨울의 수녀를 닮아 있었다. 그 순간 온몸이 나른해졌다.',
         'A stranger you passed in the street smiled at you. The smile looked like that winter\'s nun. In that instant your whole body went slack.',
         '道ですれ違った見知らぬ人が微笑んだ。その笑みが、あの冬の修道女に似ていた。その瞬間、全身がけだるくなった。')]
SW2D = k('그 단맛이 또 찾아왔다. 이번에는 눈을 감은 채 하루가 통째로 지나갔다. 깨어 보니 해가 지고 있었다. 다시 감으면 이번에는 더 오래 머물 수 있을 것 같다.',
         'The sweetness came again. This time a whole day passed with your eyes closed. When you woke, the sun was setting. If you closed them again, you felt you could stay even longer.',
         'あの甘さがまたやってきた。今度は目を閉じたまま一日がまるごと過ぎた。目覚めると日が暮れかけていた。もう一度閉じれば、今度はもっと長くいられそうだ。')
SW2N = k('몇 해 만에 그 단맛이 다시 혀끝에 돌아왔다. 지난번보다 조금 더 짙었다.', 'For the first time in years, that sweetness returned to the tip of your tongue. It was a little stronger than last time.', '数年ぶりに、あの甘さが舌先に戻ってきた。前よりも少し濃かった。')
SW3 = k('꿈속에서 그 목소리가 다정하게 말했다. “이제 오셔도 돼요. 다들 여기 있어요.”', 'In a dream, that voice spoke gently. “You may come now. Everyone is here.”', '夢の中で、あの声が優しく言った。「もう来てもいいのですよ。皆、ここにいます」')
LIGHT = k('그래도 예전만큼 짙지는 않았다.', 'Still, it was not as strong as it used to be.', 'それでも、以前ほど濃くはなかった。')
FREE = k('단맛은 더는 돌아오지 않았다.', 'The sweetness never came back.', '甘さは、もう戻ってこなかった。')
T_SW = k('단맛', 'Sweetness', '甘さ'); T_SW2 = k('짙어지는 단맛', 'A Deepening Sweetness', '濃くなる甘さ'); T_SW3 = k('이제 오셔도 돼요', 'You May Come Now', 'もう来てもいいのですよ')
C = {}
C['close'] = k('눈을 감는다', 'Close your eyes', '目を閉じる'); C['shake'] = k('뿌리친다', 'Shake it off', '振り払う')
C['close2'] = k('다시 눈을 감는다', 'Close your eyes again', 'もう一度目を閉じる'); C['window'] = k('창문을 연다', 'Open the window', '窓を開ける'); C['call'] = k('누군가를 부른다', 'Call someone', '誰かを呼ぶ')
C['follow'] = k('따라간다', 'Follow it', 'ついていく'); C['awake'] = k('끝까지 깨어 있는다', 'Stay awake to the end', '最後まで起きている')
R = {}
R['close'] = k('한참 뒤 눈을 떴을 때, 무엇을 보았는지 기억나지 않았다. 단맛만 오래 남았다.', 'When you opened your eyes long after, you couldn\'t remember what you\'d seen. Only the sweetness lingered.', 'しばらくして目を開けたとき、何を見たのか覚えていなかった。甘さだけが長く残った。')
R['shake'] = k('찬물에 얼굴을 씻었다. 단맛이 조금씩 옅어졌다.', 'You washed your face in cold water. The sweetness faded little by little.', '冷たい水で顔を洗った。甘さが少しずつ薄れていった。')
R['close2'] = k('눈을 떴을 때 달력이 이틀 넘어가 있었다. 아무도 그 이틀을 묻지 않았다.', 'When you opened your eyes, the calendar had moved two days on. No one asked about those two days.', '目を開けると、暦が二日進んでいた。誰もその二日のことを尋ねなかった。')
R['window'] = k('찬 바람이 들어왔다. 단맛이 바람에 쓸려 나갔다.', 'Cold air came in. The sweetness was swept away on the wind.', '冷たい風が入ってきた。甘さは風にさらわれていった。')
R['call'] = k('전화를 걸어 아무 이야기나 했다. 통화가 끝날 무렵 단맛은 사라져 있었다.', 'You made a call and talked about nothing in particular. By the time you hung up, the sweetness was gone.', '電話をかけて、とりとめのない話をした。電話を切るころには甘さは消えていた。')
R['follow'] = k('한 계절이 꿈처럼 지나갔다. 깨어난 뒤에도 자주 멍하니 웃었다.', 'A season passed like a dream. Even after you woke, you often caught yourself smiling blankly.', 'ひと季節が夢のように過ぎた。目覚めたあとも、よくぼんやりと笑っていた。')
R['awake'] = k('밤새 불을 켜 두고 앉아 있었다. 새벽이 되자 목소리는 멀어졌다.', 'You sat up all night with the light on. By dawn the voice had drifted away.', '一晩じゅう明かりをつけて座っていた。明け方になると、声は遠ざかっていった。')

# ---- B. 연작 「단꿈의 도시」 ----
W1 = [k('그 겨울 잠든 사람들이 한 병동에 모여 있다는 기사가 났다. 몇 해째 웃는 얼굴로 잠들어 있다고 한다. 명단에 아는 이름이 있었다.',
        'An article said that the people who fell asleep that winter had been gathered in a single ward. They have slept for years, smiling. There was a name you knew on the list.',
        'あの冬に眠りについた人々が、ひとつの病棟に集められているという記事が出た。何年も笑顔のまま眠っているという。名簿に知っている名前があった。'),
      k('병원 꼭대기 층에 불이 꺼지지 않는 병동이 있다고 들었다. 그 겨울 잠든 사람들이 아직 거기 있다. 그중 하나는 예전 이웃이었다.',
        'You heard there is a ward on the top floor of the hospital whose lights never go out. The people who fell asleep that winter are still there. One of them used to be your neighbour.',
        '病院の最上階に、明かりの消えない病棟があると聞いた。あの冬に眠った人々が今もそこにいる。そのひとりはかつての隣人だった。'),
      k('그 겨울 잠든 사람들의 가족 모임 소식지가 우편함에 들어 있었다. 한 장짜리 명단에서 낯익은 이름을 찾았다.',
        'A newsletter from the families of those who fell asleep that winter was in your mailbox. On the one-page list, you found a familiar name.',
        'あの冬に眠った人々の家族会の会報が郵便受けに入っていた。一枚きりの名簿に、見覚えのある名前を見つけた。')]
W2 = [k('그 겨울 잠들었던 사람 하나가 몇 년 만에 깨어났다. 그 사람이 당신을 보자마자 말했다. “거기가 더 좋았어요. 왜 깨운 거예요?”',
        'One of the people who fell asleep that winter woke after several years. The moment they saw you, they said, “It was better there. Why did you wake me?”',
        'あの冬に眠った人のひとりが、数年ぶりに目を覚ました。その人はあなたを見るなり言った。「あっちのほうがよかった。どうして起こしたの?」'),
      k('병동에서 본 그 사람이 깨어났다는 연락이 왔다. 찾아가자 그 사람은 창밖을 보며 말했다. “거기가 더 좋았어요.”',
        'Word came that the person you saw in the ward had woken. When you visited, they looked out the window and said, “It was better there.”',
        '病棟で見たあの人が目を覚ましたと連絡があった。訪ねると、その人は窓の外を見ながら言った。「あっちのほうがよかった」'),
      k('깨어난 사람들의 모임에 초대받았다. 한 사람이 조용히 손을 들었다. “다시 돌아가고 싶은 사람, 저만 그런가요?”',
        'You were invited to a gathering of those who had woken. One person quietly raised a hand. “Am I the only one who wants to go back?”',
        '目覚めた人々の集まりに招かれた。ひとりが静かに手を挙げた。「もう一度戻りたいのは、わたしだけですか」')]
W3 = [k('잠든 사람이 많은 동네부터 비어 갔다. 불 꺼진 창이 한 집 건너 한 집이다.', 'The neighbourhoods with the most sleepers emptied first. Every other window was dark.', '眠った人が多い町から空になっていった。灯りの消えた窓が一軒おきに並ぶ。'),
      k('동네 가게가 하나둘 문을 닫았다. 주인들이 그 겨울 잠든 채 깨어나지 않았다고 한다.', 'The shops in the neighbourhood closed one by one. Their owners, they say, fell asleep that winter and never woke.', '近所の店がひとつ、またひとつと閉まった。店主たちはあの冬に眠ったまま目覚めなかったという。'),
      k('같은 층의 집이 다 비었다. 엘리베이터에서 마주치는 사람이 없다.', 'Every flat on your floor stands empty. There\'s no one to run into in the lift anymore.', '同じ階の部屋がすべて空いた。エレベーターで誰とも会わない。')]
T_W1 = k('깨어나지 않는 병동', 'The Ward That Never Wakes', '目覚めない病棟'); T_W2 = k('잠에서 깬 사람', 'The One Who Woke', '眠りから覚めた人'); T_W3 = k('텅 빈 거리', 'Empty Streets', '空っぽの通り')
C['visit'] = k('찾아간다', 'Go and see them', '会いに行く'); C['novisit'] = k('가지 않는다', 'Don\'t go', '行かない')
R['visit'] = k('병상 옆에 앉았다. 그 사람은 웃고 있었다. 무슨 꿈인지 묻고 싶었다.', 'You sat by the bed. They were smiling. You wanted to ask what they were dreaming.', 'ベッドのそばに座った。その人は笑っていた。どんな夢なのか尋ねたかった。')
R['novisit'] = k('기사를 접었다. 그 이름은 오래 머릿속에 남았다.', 'You folded the paper away. The name stayed in your head for a long time.', '記事を畳んだ。その名前は長く頭に残った。')
C['stay'] = k('곁에 있어 준다', 'Stay by their side', 'そばにいてあげる'); C['argue'] = k('그래도 여기가 낫다고 말한다', 'Tell them it\'s still better here', 'それでもここのほうがいいと言う'); C['mute'] = k('아무 말도 못 한다', 'You can\'t say a thing', '何も言えない')
R['stay'] = k('아무 말 없이 곁에 앉아 있었다. 그 사람은 한참 울다가 잠들었다. 이번에는 평범한 잠이었다.', 'You sat beside them without a word. They cried for a long while, then fell asleep. This time it was an ordinary sleep.', '何も言わずにそばに座っていた。その人はしばらく泣いてから眠った。今度は、ふつうの眠りだった。')
R['argue'] = k('그 사람은 대답하지 않았다. 며칠 뒤, 처음으로 창문을 열었다고 들었다.', 'They didn\'t answer. A few days later, you heard they\'d opened their window for the first time.', 'その人は答えなかった。数日後、初めて窓を開けたと聞いた。')
R['mute'] = k('그 말이 틀렸다고 말할 자신이 없었다.', 'You weren\'t sure enough to tell them they were wrong.', 'その言葉が間違っていると言い切る自信がなかった。')
C['move'] = k('이사한다', 'Move away', '引っ越す'); C['remain'] = k('남는다', 'Stay', '残る')
R['move'] = k('짐을 쌌다. 새 동네의 밤은 시끄러웠다. 그게 반가웠다.', 'You packed your things. Nights in the new neighbourhood were noisy. You were glad of it.', '荷物をまとめた。新しい町の夜はうるさかった。それがありがたかった。')
R['remain'] = k('남은 이웃끼리 반찬을 나누기 시작했다. 몇 해 사이 이웃은 셋으로 줄었지만, 그 셋과는 가족처럼 지냈다.', 'The neighbours who remained began sharing food. Over the years they dwindled to three, but you lived with those three like family.', '残った隣人どうしでおかずを分け合うようになった。数年のうちに隣人は三人に減ったが、その三人とは家族のように過ごした。')

# ---- 도시 · 사람 · 서번트 · 흔적 · 마지막 ----
E = {}
E['vigil'] = (k('그 겨울의 묵념', 'A Moment of Silence for That Winter', 'あの冬の黙祷'),
  [k('해마다 그 겨울의 밤이 오면, 도시는 잠든 사람들을 위해 한 시간 동안 불을 끈다.', 'Every year when that winter night comes round, the city turns off its lights for an hour for those who sleep.', '毎年あの冬の夜が来ると、街は眠る人々のために一時間だけ灯りを消す。'),
   k('올해도 그 밤이 왔다. 방송에서 잠든 사람들의 수를 읽어 내려간다. 숫자는 해마다 조금씩 줄어든다.', 'That night came again this year. The broadcast reads out the number of sleepers. The number shrinks a little every year.', '今年もあの夜が来た。放送が眠る人々の数を読み上げる。数は年ごとに少しずつ減っていく。'),
   k('그 겨울의 밤, 도시 곳곳에서 촛불이 켜졌다. 누가 시작했는지는 아무도 모른다.', 'On that winter\'s night, candles were lit all over the city. No one knows who started it.', 'あの冬の夜、街のあちこちで蝋燭が灯された。誰が始めたのかは誰も知らない。')],
  [('out', k('거리에 나간다', 'Go out into the street', '通りに出る'), k('촛불을 든 사람들 사이에 섰다. 아무도 이유를 말하지 않았다.', 'You stood among people holding candles. No one said why they were there.', '蝋燭を持つ人々の間に立った。誰も理由を口にしなかった。'), {'bond': 2}),
   ('home', k('집에서 불을 끈다', 'Turn off the lights at home', '家で灯りを消す'), k('불을 끄고 창가에 앉았다. 도시 전체가 숨을 죽였다.', 'You switched off the lights and sat by the window. The whole city held its breath.', '灯りを消して窓辺に座った。街じゅうが息をひそめた。'), {'will': 1}),
   ('away', k('외면한다', 'Look away', '目をそらす'), k('불을 켜 둔 채 일을 했다. 창밖이 너무 어두웠다.', 'You kept working with the light on. It was too dark outside the window.', '灯りをつけたまま仕事をした。窓の外が暗すぎた。'), {'will': -2})])
E['kids'] = (k('아이들의 놀이', 'A Children\'s Game', '子どもたちの遊び'),
  [k('{0~이} 학교에서 유행하는 놀이를 배워 왔다. 누가 더 오래 웃으면서 자는지 겨루는 놀이라고 했다.', '{0} brought home a game that was popular at school. A game to see who could sleep the longest while smiling.', '{0}が学校で流行っている遊びを覚えてきた。誰がいちばん長く笑ったまま眠れるかを競う遊びだという。'),
   k('{0~이} 친구들과 눈을 감고 누워 키득거리고 있었다. 먼저 웃음을 멈추는 쪽이 진다고 했다.', '{0} was lying with eyes closed among friends, giggling. Whoever stopped smiling first would lose, they said.', '{0}が友達と目を閉じて寝転がり、くすくす笑っていた。先に笑うのをやめたほうが負けだという。'),
   k('{0~이} 잠든 척하며 입꼬리를 올리고 있었다. 요즘 아이들 사이에서 유행하는 놀이라고 했다.', '{0} was pretending to sleep, lips curled into a smile. A game that\'s popular among kids these days, they said.', '{0}は眠ったふりをして口角を上げていた。最近子どもたちの間で流行っている遊びだという。')],
  [('stop', k('말린다', 'Stop them', 'やめさせる'), k('그 놀이는 하지 말자고 했다. 아이는 이유를 묻지 않고 고개를 끄덕였다.', 'You asked them not to play that game. The child nodded without asking why.', 'その遊びはやめようと言った。子どもは理由を聞かずに頷いた。'), {'bond': 2}),
   ('let', k('모른 척한다', 'Pretend not to notice', '見ないふりをする'), k('아이는 그날 밤 웃으며 잠들었다. 오래 그 얼굴을 지켜보았다.', 'That night the child fell asleep smiling. You watched that face for a long time.', 'その夜、子どもは笑いながら眠った。長いことその顔を見守った。'), {'will': -2})])
E['family'] = (k('깨어난 가족', 'Family Who Woke', '目覚めた家族'),
  [k('그 겨울 잠들었던 {0~이} 깨어났다. 다 나은 줄 알았는데, 가끔 멍하니 단 것을 찾는다.', '{0}, who fell asleep that winter, has woken. You thought they were well, but now and then they stare into space and reach for something sweet.', 'あの冬に眠っていた{0}が目を覚ました。すっかり治ったと思っていたのに、ときどきぼんやりと甘いものを探す。'),
   k('{0~이} 그 겨울 몇 주 동안 깨어나지 않았던 일을 이제야 털어놓았다. 거기가 아주 따뜻했다고 했다.', '{0} finally confessed to those few weeks that winter when they didn\'t wake. It was very warm there, they said.', '{0}が、あの冬に数週間目覚めなかったことをようやく打ち明けた。そこはとても温かかったと。'),
   k('{0}의 찻잔에 설탕이 자꾸 늘어난다. 그 겨울 잠들었다 깬 뒤로 생긴 버릇이다.', 'There\'s more and more sugar in {0}\'s tea. A habit since they woke from that winter\'s sleep.', '{0}のお茶に入る砂糖がどんどん増えていく。あの冬の眠りから覚めて以来の癖だ。')],
  [('tend', k('곁을 지킨다', 'Stay close', 'そばについている'), k('단 것 대신 따뜻한 차를 끓였다. 함께 마시는 차는 쓰지 않았다.', 'You made warm tea instead of something sweet. Drunk together, it wasn\'t bitter.', '甘いものの代わりに温かいお茶を淹れた。一緒に飲むお茶は苦くなかった。'), {'bond': 3, 'will': -1}),
   ('clinic', k('함께 병원에 다닌다', 'Go to the hospital together', '一緒に病院へ通う'), k('의사는 원인을 찾지 못했다. 그래도 둘이 함께 다니는 길은 나쁘지 않았다.', 'The doctors couldn\'t find a cause. Still, the walks there together weren\'t so bad.', '医者は原因を見つけられなかった。それでも、二人で通う道は悪くなかった。'), {'bond': 2, 'wealth': -5})])
E['allyl'] = (k('동맹의 편지', 'A Letter from an Ally', '同盟者からの手紙'),
  [k('그 겨울의 동맹 {0}에게서 편지가 왔다. 요즘도 같은 꿈을 꾼다고 했다.', 'A letter came from {0}, your ally that winter. They still dream the same dream these days, it said.', 'あの冬の同盟者、{0}から手紙が来た。今も同じ夢を見るという。'),
   k('{0}에게서 짧은 메시지가 왔다. “너도 그 단맛, 아직 기억나?”', 'A short message came from {0}. “Do you still remember that sweetness too?”', '{0}から短いメッセージが届いた。「あの甘さ、お前もまだ覚えてるか?」'),
   k('{0}에게서 소포가 왔다. 쓴 커피 한 봉지와 쪽지. “단 건 이제 질렸어.”', 'A parcel came from {0}: a bag of bitter coffee and a note. “I\'m sick of sweet things.”', '{0}から小包が届いた。苦いコーヒーがひと袋とメモ。「甘いのはもう飽きた」')],
  [('meet', k('만나서 이야기한다', 'Meet and talk', '会って話す'), k('둘은 그 꿈 이야기를 처음으로 소리 내어 했다. 말하고 나니 조금 옅어졌다.', 'For the first time, the two of you spoke of that dream out loud. Once said, it faded a little.', 'ふたりはあの夢の話を初めて声に出した。口にしてみると、少し薄れた。'), {'bond': 3, 'will': 2, 'light': 1}),
   ('write', k('답장만 한다', 'Just write back', '返事だけ書く'), k('“나도 그래.” 짧게 적어 보냈다.', '“Me too.” You wrote just that and sent it.', '「俺もだ」と短く書いて送った。'), {'bond': 1})])
E['burial'] = (k('매장기관의 방문', 'A Visit from the Burial Agency', '埋葬機関の訪問'),
  [k('매장기관의 수녀복을 입은 사람이 찾아왔다. 그 겨울 이 도시에 있던 수녀의 행방을 묻는다.', 'Someone in a Burial Agency habit came to your door, asking where the nun who was in this city that winter went.', '埋葬機関の修道服を着た人が訪ねてきた。あの冬この街にいた修道女の行方を尋ねる。'),
   k('비 오는 저녁, 검은 우산을 쓴 사람이 문 앞에 서 있었다. 매장기관이라고만 밝히고, 그 겨울의 수녀에 대해 물었다.', 'On a rainy evening, someone under a black umbrella stood at your door. They said only that they were from the Burial Agency, and asked about that winter\'s nun.', '雨の夕方、黒い傘の人が戸口に立っていた。埋葬機関とだけ名乗り、あの冬の修道女について尋ねた。'),
   k('교회 앞에서 낯선 신부가 말을 걸었다. 그 겨울 키아라라는 수녀를 본 적이 있느냐고.', 'A strange priest spoke to you outside a church. Had you ever seen a nun named Kiara that winter, he asked.', '教会の前で見知らぬ神父に声をかけられた。あの冬、キアラという修道女を見たことはないかと。')],
  [('tell', k('아는 것을 다 말한다', 'Tell them everything you know', '知っていることを全部話す'), k('기억나는 것을 전부 말했다. 그 사람은 끝까지 표정을 바꾸지 않았다.', 'You told them everything you remembered. Their expression never changed.', '覚えていることを全部話した。その人は最後まで表情を変えなかった。'), {'lore': 2, 'told': 1}),
   ('deny', k('모른다고 한다', 'Say you don\'t know', '知らないと言う'), k('그 사람은 고개를 숙이고 돌아갔다. 문을 닫고 나서야 손이 떨렸다.', 'They bowed and left. Only after you closed the door did your hands start to shake.', 'その人は頭を下げて帰っていった。扉を閉めてから、手が震えた。'), {})])
E['priest'] = (k('감독관의 사과', 'The Overseer\'s Apology', '監督役の謝罪'),
  [k('그 겨울의 감독관이었던 신부가 지팡이를 짚고 찾아왔다. “토벌령을 내린 것은 나였소. 그 수녀의 말만 믿고.” 신부는 깊이 고개를 숙였다.', 'The priest who was that winter\'s overseer came on a cane. “It was I who issued that subjugation order. I took that nun at her word.” He bowed his head low.', 'あの冬の監督役だった神父が杖をついて訪ねてきた。「討伐令を出したのは私だ。あの修道女の言葉だけを信じて」神父は深く頭を下げた。'),
   k('늙은 신부에게서 편지가 왔다. 그 겨울 자신이 무엇에 속았는지 이제야 안다고, 미안하다고 적혀 있었다.', 'A letter came from the old priest. He knew now what he had been deceived by that winter, it said, and he was sorry.', '年老いた神父から手紙が届いた。あの冬、自分が何に騙されていたのかようやく分かった、すまないと書かれていた。'),
   k('성당 고해실 너머에서 낯익은 목소리가 들렸다. 그 겨울의 감독관이었다. 이번에는 그가 고해하고 있었다.', 'Beyond the confessional screen you heard a familiar voice: that winter\'s overseer. This time, he was the one confessing.', '告解室の向こうから聞き覚えのある声がした。あの冬の監督役だ。今度は彼のほうが告解していた。')],
  [('forgive', k('용서한다', 'Forgive him', '許す'), k('신부는 한참 그대로 있다가, 고맙다는 말 대신 성호를 그었다.', 'The priest stayed as he was for a long while, then made the sign of the cross instead of saying thank you.', '神父はしばらくそのままでいたが、礼の言葉の代わりに十字を切った。'), {'will': 3}),
   ('refuse', k('받아들이지 않는다', 'Don\'t accept it', '受け入れない'), k('신부는 아무 말 없이 돌아갔다. 그 등이 생각보다 작았다.', 'The priest left without a word. His back looked smaller than you remembered.', '神父は何も言わずに帰っていった。その背中は思っていたより小さかった。'), {'will': -1})])
E['relic'] = (k('남은 물건', 'What Was Left Behind', '残された物'),
  [k('{0}의 물건 하나를 정리하다 손을 멈췄다. 아직 그 겨울 냄새가 난다.', 'Sorting through one of {0}\'s things, your hands stopped. It still smells of that winter.', '{0}の持ち物をひとつ片付けていて、手が止まった。まだあの冬の匂いがする。'),
   k('서랍 깊은 곳에서 {0~이} 쓰던 물건이 나왔다. 그 겨울 이후 한 번도 열지 않은 서랍이었다.', 'From the back of a drawer came something {0} used to use. A drawer you hadn\'t opened since that winter.', '引き出しの奥から、{0}が使っていた物が出てきた。あの冬以来、一度も開けなかった引き出しだった。'),
   k('이사 짐 사이에서 {0}의 물건이 나왔다. 손에 쥐자 그 겨울 밤공기가 떠올랐다.', 'Among the moving boxes you found something of {0}\'s. Holding it, you remembered the night air of that winter.', '引っ越しの荷物の間から{0}の物が出てきた。手に取ると、あの冬の夜気がよみがえった。')],
  [('keep', k('간직한다', 'Keep it', 'しまっておく'), k('서랍 깊은 곳에 다시 넣어 두었다. 가끔 꺼내 보기로 했다.', 'You put it back deep in the drawer. You decided to take it out now and then.', '引き出しの奥にしまい直した。ときどき取り出して見ることにした。'), {'will': 1, 'bond': 1}),
   ('bury', k('묻어 준다', 'Bury it', '埋めてやる'), k('그 겨울 함께 걷던 길가에 묻었다. 작은 돌을 하나 얹었다.', 'You buried it beside the road you walked together that winter, and set a small stone on top.', 'あの冬に一緒に歩いた道端に埋めた。小さな石をひとつ載せた。'), {'will': 2})])
E['church'] = (k('비어 있는 성당', 'The Empty Church', '空っぽの聖堂'),
  [k('수녀가 머물던 성당은 몇 해째 비어 있다. 지나가다 보니 문이 조금 열려 있었다.', 'The church where the nun stayed has been empty for years. Passing by, you noticed the door was slightly open.', '修道女がいた聖堂は何年も空いたままだ。通りがかると、扉が少し開いていた。'),
   k('비어 있는 성당에서 밤마다 오르간 소리가 난다는 소문이 돌았다.', 'Rumour had it that organ music came from the empty church every night.', '空っぽの聖堂から毎晩オルガンの音がするという噂が流れた。'),
   k('그 성당이 헐린다는 공고가 붙었다. 마지막으로 한번 들여다볼 수 있는 날이었다.', 'A notice went up that the church would be demolished. It was the last day you could look inside.', 'あの聖堂が取り壊されるという告知が貼られた。最後に一度中を覗ける日だった。')],
  [('enter', k('들어가 본다', 'Go inside', '入ってみる'), k('제단 위에 염주 하나가 놓여 있었다. 손에 쥐자 달콤한 향이 났다. 그 자리에 다시 내려놓았다.', 'A string of prayer beads lay on the altar. When you held it, it smelled sweet. You set it back where it was.', '祭壇の上に数珠がひとつ置かれていた。手に取ると甘い香りがした。元の場所に戻した。'), {'will': -1, 'lore': 2}),
   ('pass', k('지나친다', 'Walk past', '通り過ぎる'), k('걸음을 서둘렀다. 등 뒤에서 종이 한 번 울린 것 같았다.', 'You hurried on. Behind you, it seemed a bell rang once.', '足を速めた。背後で鐘が一度鳴った気がした。'), {})])
E['far'] = (k('먼 도시의 잠', 'Sleep in a Distant City', '遠い街の眠り'),
  [k('먼 나라의 도시에서 원인 모를 깊은 잠이 번지고 있다는 뉴스가 나왔다. 잠든 사람들이 하나같이 웃고 있다고 했다.', 'The news reported a deep sleep of unknown cause spreading through a city in a faraway country. Every sleeper was smiling, it said.', '遠い国の街で原因不明の深い眠りが広がっているというニュースが流れた。眠った人々は皆、笑っているという。'),
   k('바다 건너 항구 도시에서 한 동네가 통째로 잠들었다는 짧은 기사가 났다. 사진 속 얼굴들이 모두 웃고 있었다.', 'A short article said that an entire neighbourhood in a port city across the sea had fallen asleep. Every face in the photo was smiling.', '海の向こうの港町で、ひとつの町がまるごと眠りについたという短い記事が出た。写真の顔は皆笑っていた。'),
   k('외국 뉴스 한구석에, 깨어나지 않는 사람들과 그 곁에서 기도하는 수녀 이야기가 실렸다.', 'In a corner of the foreign news was a story about people who wouldn\'t wake and a nun praying by their side.', '海外ニュースの片隅に、目覚めない人々と、そのそばで祈る修道女の話が載っていた。')],
  [('off', k('뉴스를 끈다', 'Turn off the news', 'ニュースを消す'), k('화면이 꺼지고도 그 웃는 얼굴들이 눈앞에 남았다.', 'Even after the screen went dark, those smiling faces stayed before your eyes.', '画面が消えても、あの笑顔が目の前に残った。'), {}),
   ('call', k('매장기관에 연락한다', 'Contact the Burial Agency', '埋葬機関に連絡する'), k('짧은 답장이 왔다. “알고 있습니다. 이번에는 늦지 않겠습니다.”', 'A short reply came. “We know. This time we will not be late.”', '短い返事が来た。「承知しています。今度は遅れません」'), {'lore': 1, 'need': 'told'})])
E['ward'] = (k('단꿈을 막는 결계', 'A Barrier Against Sweet Dreams', '甘い夢を防ぐ結界'),
  [k('그 겨울의 단맛을 막는 결계를 짤 수 있을 것 같다. 다만 그러려면 그 맛을 다시 떠올려야 한다.', 'You think you could weave a barrier against that winter\'s sweetness. But to do it, you\'d have to recall the taste.', 'あの冬の甘さを防ぐ結界を組めそうだ。ただ、そのためにはあの味をもう一度思い出さなければならない。'),
   k('오래된 마술서에서 꿈을 거르는 술식을 찾았다. 그 겨울의 단꿈에도 들을지는 해 봐야 안다.', 'In an old grimoire you found a formula for filtering dreams. Whether it works on that winter\'s sweet dream, you\'ll only know by trying.', '古い魔術書で夢を濾す術式を見つけた。あの冬の甘い夢にも効くかは、試してみないと分からない。'),
   k('잠든 사람들의 병동에서 마술의 흔적을 느꼈다. 그것을 거꾸로 짜면 막는 결계가 될지도 모른다.', 'In the sleepers\' ward you sensed traces of magecraft. Woven in reverse, they might become a barrier against it.', '眠る人々の病棟で魔術の痕跡を感じた。それを逆に組めば、防ぐ結界になるかもしれない。')],
  [('study', k('연구한다', 'Research it', '研究する'), k('몇 달 동안 그 단맛을 되새기며 술식을 짰다. 완성된 결계 안에서는 꿈이 조용했다.', 'For months you wove the formula, recalling that sweetness. Inside the finished barrier, your dreams were quiet.', '数か月、あの甘さを思い返しながら術式を組んだ。完成した結界の中では、夢が静かだった。'), {'lore': 4, 'will': -2, 'light': 1}),
   ('leave', k('손대지 않는다', 'Leave it alone', '手をつけない'), k('그 맛은 떠올리지 않는 편이 낫다고 생각했다.', 'You decided it was better not to recall that taste.', 'あの味は思い出さないほうがいいと思った。'), {})])
# 서번트 꿈 · 다른 목소리 · 마지막 한 입
SVD_T = k('꿈속의 서번트', 'The Servant in the Dream', '夢の中のサーヴァント')
SVD_B = [k('꿈에 {0~이} 나왔다. 그 겨울 키아라에게 녹아든 모습 그대로였다.', '{0} appeared in a dream, just as they were when they melted into Kiara that winter.', '夢に{0}が出てきた。あの冬、キアラに溶け込んだときの姿のままだった。'),
         k('잠결에 {0}의 목소리를 들었다. 눈을 뜨지 않으면 계속 들릴 것 같았다.', 'Half asleep, you heard {0}\'s voice. As long as you didn\'t open your eyes, you felt you could keep hearing it.', 'まどろみの中で{0}の声を聞いた。目を開けなければ、ずっと聞こえていそうだった。'),
         k('꿈속의 그 겨울 거리에서 {0~이} 뒤돌아보았다.', 'On the winter street of your dream, {0} turned to look back at you.', '夢の中のあの冬の通りで、{0}が振り返った。')]
SVD_L = {'love': (k('“여기는 괜찮아. 아프지도 않아. …그래도 너는 오지 마.”', '“It\'s all right here. It doesn\'t hurt. …But don\'t you come.”', '「ここは大丈夫だ。痛くもない。…でも、お前は来るな」'),
                  k('“여기는 괜찮습니다. 아프지도 않아요. …그래도 당신은 오지 마세요.”', '“It is all right here. It doesn\'t hurt. …But please, don\'t you come.”', '「ここは大丈夫です。痛くもありません。…でも、あなたは来ないでください」'),
                  k('{0~은} 웃으며 손을 흔들었다. 오라는 손짓인지, 가라는 손짓인지 알 수 없었다.', '{0} smiled and waved. You couldn\'t tell if it meant come or go.', '{0}は笑って手を振った。来いという合図なのか、行けという合図なのか分からなかった。')),
         'friend': (k('“이쪽은 걱정 마. 다들 웃고 있어. …너는 거기 있어.”', '“Don\'t worry about this side. Everyone\'s smiling. …You stay there.”', '「こっちは心配するな。皆笑ってる。…お前はそこにいろ」'),
                    k('“이쪽은 걱정 마세요. 다들 웃고 있습니다. …당신은 그곳에 있어 주세요.”', '“Don\'t worry about this side. Everyone is smiling. …Please stay where you are.”', '「こちらは心配いりません。皆、笑っています。…あなたはそこにいてください」'),
                    k('{0~은} 고개를 저으며 당신 쪽을 가리켰다. 거기 있으라는 뜻 같았다.', '{0} shook their head and pointed back toward you. It seemed to mean: stay there.', '{0}は首を振って、あなたのほうを指さした。そこにいろという意味らしかった。')),
         'none': (k('“…아직 그쪽에 있었군.”', '“…So you\'re still over there.”', '「…まだそっちにいたのか」'),
                  k('“…아직 그쪽에 계셨군요.”', '“…So you are still over there.”', '「…まだそちらにいらしたのですね」'),
                  k('{0~은} 잠시 당신을 바라보다가 등을 돌렸다.', '{0} looked at you for a moment, then turned away.', '{0}はしばらくあなたを見つめ、背を向けた。'))}
C['wantstay'] = k('함께 있고 싶다고 말한다', 'Say you want to stay with them', '一緒にいたいと言う'); C['goback'] = k('돌아가라고 말한다', 'Tell them to go back', '戻れと言う')
R['wantstay'] = k('꿈은 아침까지 이어졌다. 깨어나니 베개가 젖어 있었다.', 'The dream went on until morning. When you woke, your pillow was wet.', '夢は朝まで続いた。目覚めると枕が濡れていた。')
R['goback'] = k('{0~은} 고개를 끄덕이고 등을 돌렸다. 꿈은 거기서 끝났다.', '{0} nodded and turned away. The dream ended there.', '{0}は頷いて背を向けた。夢はそこで終わった。')
MIM_T = k('다른 목소리', 'A Different Voice', '違う声')
MIM_B = k('꿈속에서 {0~이} 이리 오라고 불렀다. 그런데 말끝이 어딘가 달랐다. {1~은} 그런 식으로 부르지 않는다.', 'In a dream, {0} called you to come over. But something was off about the way the words ended. {1} never called you like that.', '夢の中で{0}がこっちへ来いと呼んだ。けれど語尾がどこか違った。{1}はそんなふうには呼ばない。')
C['notice'] = k('알아챈다', 'See through it', '見抜く'); C['goanyway'] = k('그래도 따라간다', 'Follow anyway', 'それでもついていく')
R['notice'] = k('“당신은 그 사람이 아니야.” 그렇게 말하자 꿈이 녹아내렸다. 단맛이 한결 옅어졌다.', '“You are not them.” As you said it, the dream melted away. The sweetness grew much fainter.', '「あなたはあの人じゃない」そう言うと、夢が溶け落ちた。甘さがずいぶん薄くなった。')
R['goanyway'] = k('알면서도 걸어갔다. 깨어난 뒤 오래 그 목소리를 생각했다.', 'You walked toward it knowing. After you woke, you thought about that voice for a long time.', '分かっていて歩いていった。目覚めたあと、長いことあの声のことを考えた。')
LAST_T = k('마지막 한 입', 'One Last Taste', '最後のひと口')
LAST_B = k('어느 밤, 그 목소리가 아주 가까이에서 들렸다. “약속대로, 마지막에 맛보러 왔어요.”', 'One night, that voice came from very close by. “As promised, I have come for one last taste.”', 'ある夜、あの声がすぐ近くで聞こえた。「約束どおり、最後に味わいに参りました」')
C['lastgo'] = k('목소리 쪽으로 손을 뻗는다', 'Reach toward the voice', '声のほうへ手を伸ばす'); C['lastno'] = k('불을 켠다', 'Turn on the light', '灯りをつける')
R['lastgo'] = k('목소리 쪽으로 손을 뻗었다. 따뜻하고, 달았다.', 'You reached toward the voice. It was warm, and sweet.', '声のほうへ手を伸ばした。温かくて、甘かった。')
R['lastno'] = k('불을 켰다. 목소리는 한참 머물다가, 아쉽다는 듯 웃으며 멀어졌다.', 'You turned on the light. The voice lingered a long while, then drifted off with a regretful laugh.', '灯りをつけた。声はしばらく留まっていたが、名残惜しそうに笑って遠ざかった。')
END = {'follow': k('마지막 순간, 입가에 단맛이 번졌다. 웃는 얼굴로 잠들었다.', 'In the last moment, sweetness spread across your lips. You fell asleep smiling.', '最期の瞬間、口元に甘さが広がった。笑顔のまま眠りについた。'),
       'awake': k('그 목소리가 다시 찾아왔지만, 끝까지 눈을 뜨고 있었다.', 'That voice came again, but you kept your eyes open to the end.', 'あの声がまた訪れたが、最後まで目を開けていた。'),
       'free': k('마지막 밤, 아무것도 찾아오지 않았다.', 'On the last night, nothing came.', '最後の夜、何も訪れなかった。')}

def ev(key, need):
    t, bodies, chs = E[key]
    cs = []
    for code, ct, rt, fx in chs:
        eff = {kk: v for kk, v in fx.items() if kk in ('bond', 'will', 'lore', 'wealth', 'health')}
        extra = ''
        if fx.get('light'): extra += 'S.flags.bxLight=(S.flags.bxLight||0)+1;'
        if fx.get('told'): extra += 'S.flags.bxTold=S.year;'
        off = "off:!S.flags.bxTold," if fx.get('need') == 'told' else ''
        cs.append(f"{{t:{J(ct)},{off}{'auto:true,' if code == chs[0][0] else ''}f:()=>{{ {('add(' + J(eff) + ');') if eff else ''}{extra} return {J(rt)}; }}}}")
    return t, bodies, ',\n        '.join(cs)

def evjs(id_, w, cond, key, bodyExpr=None):
    t, bodies, cs = ev(key, None)
    b = bodyExpr or f"pick({J(bodies)})"
    return f"    {{id:'{id_}',w:{w},c:()=>bxEp()&&{cond},f:()=>{{ if(!({cond})) return; decide({{title:{J(t)},body:{b},choices:[\n        {cs}]}}); }}}},"

CORE = f"""  // ---- 비스트 Ⅲ/R 최종전 패배 뒤 (11-12): 단맛의 유혹 · 단꿈의 도시 · 사람 · 서번트 · 키아라의 흔적 · 마지막 한 입 ----
  // 한 생에 연작 포함 6개까지. 유혹은 앞서 눈을 감을수록(bxDeep) 짙어지고, 결계 · 동맹 · 알아챔(bxLight)으로 옅어진다
  const bxEpN=()=>((S.epi&&S.epi.used)||[]).filter(x=>/^bx_|^arc_dream/.test(x)&&x!=='bx_moon').length;
  // 단꿈의 생은 에필로그 사건 자리가 둘 더 있다 (자리 수가 정해진 뒤 처음 고를 때 한 번)
  const bxEp=()=>{{ if(!S.flags.bxDream) return false; const E=S.epi; if(E&&E.n&&!E.bxN){{ E.bxN=1; E.n+=2; }} return bxEpN()<6; }};
  const bxYrs=()=>S.year-S.warYear;
  const bxSwOk=n=>(S.flags.bxSwN||0)===n-1&&bxYrs()>=0&&(n===1||!/^bx_sw/.test(((S.epi&&S.epi.used)||[]).slice(-1)[0]||''));
  const bxSw=(acc,will)=>{{ S.flags.bxSwN=(S.flags.bxSwN||0)+1; S.flags.bxSwY=S.year; if(acc) S.flags.bxDeep=(S.flags.bxDeep||0)+1; const lt=(S.flags.bxLight||0)>0;
    add({{will:acc&&lt?Math.round(will/2):will}}); if(S.flags.bxSwN>=3&&!S.flags.bxDeep) S.flags.bxFree=1; }};
  const bxCaller=()=>!!(S.fam&&((S.fam.spouse&&S.fam.spouse.alive)||(S.fam.kids||[]).length))||!!ally();
  const bxKin=()=>{{ const F=S.fam||{{}}; if(F.spouse&&F.spouse.alive) return F.spouse.name; if(F.mother&&F.mother.alive) return '어머니'; if(F.father&&F.father.alive) return '아버지'; return null; }};
  const bxKid=()=>((S.fam&&S.fam.kids)||[]).find(k=>k.age>=5&&k.age<=14)||null;
  const bxSvL=h=>{{ const r=relOf(), t=r&&r.stage?r.track:'none', L={J(SVD_L)}[t]; return svl(h,L[0],L[1],L[2].replace('{{0~은}}',은(h.name))); }};
  {{ const f0=die; die=cause=>{{ if(S.flags&&S.flags.bxDream&&S.phase!=='war'){{ const k=S.flags.bxLast||(S.flags.bxFree?'free':null); const L={J(END)}; if(k&&L[k]) log(L[k],'n'); }} return f0(cause); }}; }}
"""

POOL = "\n".join([
 # A. 단맛의 유혹
 f"""    {{id:'bx_sw1',w:8,c:()=>bxEp()&&bxSwOk(1),f:()=>decide({{title:{J(T_SW)},body:pick({J(SW1)}),choices:[
        {{t:{J(C['close'])},f:()=>{{ bxSw(true,-4); return {J(R['close'])}; }}}},
        {{t:{J(C['shake'])},auto:true,f:()=>{{ bxSw(false,3); return {J(R['shake'])}; }}}}]}})}},""",
 f"""    {{id:'bx_sw2',w:12,c:()=>bxEp()&&bxSwOk(2),f:()=>decide({{title:{J(T_SW2)},body:jn(S.flags.bxDeep?{J(SW2D)}:{J(SW2N)},(S.flags.bxLight||0)>0?{J(LIGHT)}:''),choices:[
        {{t:{J(C['close2'])},f:()=>{{ bxSw(true,-6); return {J(R['close2'])}; }}}},
        {{t:{J(C['window'])},auto:true,f:()=>{{ bxSw(false,3); return {J(R['window'])}; }}}},
        ...(bxCaller()?[{{t:{J(C['call'])},f:()=>{{ bxSw(false,2); add({{bond:3}}); return {J(R['call'])}; }}}}]:[])]}})}},""",
 f"""    {{id:'bx_sw3',w:14,c:()=>bxEp()&&bxSwOk(3),f:()=>decide({{title:{J(T_SW3)},body:jn({J(SW3)},(S.flags.bxLight||0)>0?{J(LIGHT)}:''),choices:[
        {{t:{J(C['follow'])},f:()=>{{ bxSw(true,-12); add({{health:-5}}); return {J(R['follow'])}; }}}},
        {{t:{J(C['awake'])},auto:true,f:()=>{{ bxSw(false,5); return jn({J(R['awake'])},S.flags.bxFree?{J(FREE)}:''); }}}}]}})}},""",
 # B. 연작
 "    {id:'arc_dream',arc:1,w:3,c:()=>bxEp()&&bxYrs()>=3,f:()=>arcStart('dream')},",
 # 도시
 evjs('bx_vigil', 2, 'bxYrs()>=1', 'vigil'),
 evjs('bx_kids', 2, '!!bxKid()', 'kids', "pick(%s).replace('{0~이}',이(bxKid().name))" % J(E['kids'][1])),
 # 사람
 evjs('bx_family', 2, '!!bxKin()', 'family', "(()=>{ const n=bxKin(); return pick(%s).replace('{0~이}',이(n)).replace('{0}',n); })()" % J(E['family'][1])),
 evjs('bx_allyl', 2, '!!ally()', 'allyl', "pick(%s).replace('{0}',ally())" % J(E['allyl'][1])),
 evjs('bx_burial', 2, 'bxYrs()>=2', 'burial'),
 evjs('bx_priest', 1.5, 'bxYrs()>=8', 'priest'),
 # 서번트
 f"""    {{id:'bx_svdream',w:2.5,c:()=>bxEp()&&!!S.hero&&bxYrs()>=1,f:()=>{{ if(!S.hero||!H_BY[S.hero]) return; const h=H_BY[S.hero]; decide({{title:{J(SVD_T)},body:jn(pick({J(SVD_B)}).replace('{{0~이}}',이(h.name)).replace('{{0}}',h.name),bxSvL(h).replace(/\\{{0~은\\}}/,은(h.name))),choices:[
        {{t:{J(C['wantstay'])},f:()=>{{ add({{will:-3}}); S.flags.bxDeep=(S.flags.bxDeep||0)+1; return {J(R['wantstay'])}; }}}},
        {{t:{J(C['goback'])},auto:true,f:()=>{{ add({{will:2}}); return {J(R['goback'])}.replace('{{0~은}}',은(h.name)); }}}}]}}); }}}},""",
 f"""    {{id:'bx_mimic',w:2,c:()=>bxEp()&&!!S.hero&&(S.flags.bxSwN||0)>=1&&(WV().trust||0)>=60,f:()=>{{ if(!S.hero||!H_BY[S.hero]) return; const h=H_BY[S.hero], n=h.name; decide({{title:{J(MIM_T)},body:{J(MIM_B)}.replace('{{0~이}}',이(n)).replace('{{1~은}}',은(n)),choices:[
        {{t:{J(C['notice'])},auto:true,f:()=>{{ add({{will:4}}); S.flags.bxLight=(S.flags.bxLight||0)+1; return {J(R['notice'])}; }}}},
        {{t:{J(C['goanyway'])},f:()=>{{ add({{will:-5}}); S.flags.bxDeep=(S.flags.bxDeep||0)+1; return {J(R['goanyway'])}; }}}}]}}); }}}},""",
 evjs('bx_relic', 1.5, '!!S.hero', 'relic', "(()=>{ const n=H_BY[S.hero].name; return pick(%s).replace('{0~이}',이(n)).replace('{0}',n); })()" % J(E['relic'][1])),
 # 키아라의 흔적
 evjs('bx_church', 1.5, 'bxYrs()>=2', 'church'),
 evjs('bx_far', 2, "bxYrs()>=4", 'far').replace("w:2,","get w(){ return S.flags.bxTold?3:.8; },"),
 evjs('bx_ward', 2, '(typeof isMage==="function"?isMage():true)&&!S.flags.mundane&&bxYrs()>=2', 'ward'),
 # 마지막 한 입
 f"""    {{id:'bx_last',w:6,c:()=>!!S.flags.bxDream&&S.age>=70&&!S.flags.bxFree,f:()=>decide({{title:{J(LAST_T)},body:{J(LAST_B)},choices:[
        {{t:{J(C['lastgo'])},f:()=>{{ S.flags.bxLast='follow'; return {J(R['lastgo'])}; }}}},
        {{t:{J(C['lastno'])},auto:true,f:()=>{{ S.flags.bxLast='awake'; add({{will:3}}); return {J(R['lastno'])}; }}}}]}})}},""",
])

ARC = f"""  // 키아라 패배 뒤의 연작: 깨어나지 않는 병동 → 잠에서 깬 사람 → 텅 빈 거리
  dream:[
    ()=>decide({{title:{J(T_W1)},body:pick({J(W1)}),choices:[
      {{t:{J(C['visit'])},f:()=>{{ AP().visit=1; add({{bond:2,will:-2}}); arcSet(1); return {J(R['visit'])}; }}}},
      {{t:{J(C['novisit'])},auto:true,f:()=>{{ arcSet(1); return {J(R['novisit'])}; }}}}]}}),
    ()=>decide({{title:{J(T_W2)},body:AP().visit?{J(W2[1])}:pick([{J(W2[0])},{J(W2[2])}]),choices:[
      {{t:{J(C['stay'])},auto:true,f:()=>{{ add({{bond:3}}); arcSet(2); return {J(R['stay'])}; }}}},
      {{t:{J(C['argue'])},f:()=>{{ add({{will:2}}); arcSet(2); return {J(R['argue'])}; }}}},
      {{t:{J(C['mute'])},f:()=>{{ add({{will:-2}}); S.flags.bxDeep=(S.flags.bxDeep||0)+1; arcSet(2); return {J(R['mute'])}; }}}}]}}),
    ()=>decide({{title:{J(T_W3)},body:pick({J(W3)}),choices:[
      {{t:{J(C['move'])},f:()=>{{ add({{wealth:-8,will:2}}); arcEnd(); return {J(R['move'])}; }}}},
      {{t:{J(C['remain'])},auto:true,f:()=>{{ add({{bond:2,will:-1}}); arcEnd(); return {J(R['remain'])}; }}}}]}})],
"""

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        kk = s.count(o)
        if kk != c: miss.append((o[:60], kk)); return
        s = s.replace(o, n)
    # 예전의 「단맛」 한 건은 3단 유혹으로 바꾼다
    import re
    s, n0 = re.subn(r"    \{id:'bx_sweet',.*?\]\}\)\},\n(?=    \{id:'bx_moon')", '', s, flags=re.S)
    if n0 != 1: miss.append(('bx_sweet', n0))
    rp("  const ARC={\n", CORE + "  const ARC={\n" + ARC)
    rp("    {id:'bx_moon',", POOL + "\n    {id:'bx_moon',")
    s, nd, nt = i18n.add(s, TR, TT)
    open(P, 'w', encoding='utf-8').write(s); print(os.path.basename(P), 'miss', miss, 'tr', nd, nt)
