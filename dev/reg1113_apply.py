"""11-13: 갈림길 평가 한마디(TR_POS · TR_NEG)와 싸우지 않을 때 재촉 · 다쳐서 쉴 때(RST · RST_HURT)를 서번트 말투(존댓말 · 왕의 말투 · 말 없음)에 맞게.
반말 서번트는 원래 문장 그대로. 말 없음은 「{이름}은 …했다.」로 쓴다.
사용: python3 reg1113_apply.py <game.html>"""
import sys, json, i18n
# (묶음, 성향, 말투, 한국어, 영어, 일본어)
R = []
def add(g, t, reg, rows):
    for ko, en, ja in rows: R.append((g, t, reg, ko, en, ja))
# ---- 갈림길: 좋게 봤을 때 ----
add('pos','명예','polite',[('그것이 옳은 길입니다.','That is the right path.','それが正しい道です。'),('네, 그래야지요.','Yes, that is how it should be.','ええ、そうあるべきです。'),('부끄럽지 않은 선택입니다.','A choice to be proud of.','恥じることのない選択です。')])
add('pos','명예','royal',[('그것이 옳은 길이니라.','That is the righteous path.','それこそ正しき道ぞ。'),('그래, 마땅히 그래야 하느니라.','Aye, so it ought to be.','うむ、そうでなくてはならぬ。'),('부끄럽지 않은 선택이로다.','A choice without shame.','恥じることなき選択よ。')])
add('pos','명예','mute',[('천천히 고개를 끄덕였다.','nodded slowly.','ゆっくりと頷いた。'),('가슴에 손을 얹었다.','placed a hand on their chest.','胸に手を当てた。'),('눈빛이 조금 부드러워졌다.','their gaze softened a little.','眼差しが少しやわらいだ。')])
add('pos','연민','polite',[('잘하셨습니다. 정말로.','You did well. Truly.','よくやりました。本当に。'),('그 사람들이 무사해서 다행입니다.','I am glad those people are safe.','あの人たちが無事でよかったです。'),('당신은 상냥한 분이군요.','You are a kind person.','あなたは優しい方ですね。')])
add('pos','연민','royal',[('잘하였구나. 참으로.','Well done. Truly.','よくやった。まことにな。'),('그 백성들이 무사하니 다행이로다.','It is well that those people are safe.','あの民が無事でなによりよ。'),('그대는 상냥하구나.','You are kind.','そなたは優しいのう。')])
add('pos','연민','mute',[('구해 낸 사람들 쪽을 오래 바라보았다.','looked toward the people you had saved for a long time.','救い出した人々のほうを長く見つめた。'),('어깨에서 힘이 조금 빠졌다.','their shoulders eased a little.','肩の力が少し抜けた。'),('당신의 손등을 가만히 내려다보았다.','looked quietly down at the back of your hand.','あなたの手の甲を静かに見下ろした。')])
add('pos','충성','polite',[('당신 곁에 서길 잘했습니다.','I am glad I stand at your side.','あなたの隣に立ててよかったです。'),('그 판단, 따르겠습니다.','I will follow that judgment.','その判断に従います。'),('믿을 수 있는 마스터시군요.','You are a Master I can trust.','信頼できるマスターですね。')])
add('pos','충성','royal',[('그대 곁에 선 보람이 있구나.','Standing at your side has proven worthwhile.','そなたの隣に立った甲斐があったのう。'),('그 판단, 짐도 따르겠노라.','We shall follow that judgment.','その判断、余も従おう。'),('믿을 만한 주인이로다.','A master worthy of trust.','信ずるに足る主よ。')])
add('pos','충성','mute',[('당신 옆으로 한 걸음 다가와 섰다.','stepped up to stand beside you.','あなたの隣へ一歩寄って立った。'),('짧게 고개를 숙였다.','bowed their head briefly.','短く頭を下げた。'),('당신의 등 뒤를 지키듯 자리를 잡았다.','took up a place as if to guard your back.','あなたの背を守るように位置を取った。')])
add('pos','야망','polite',[('좋습니다. 이겨야 의미가 있지요.','Good. Only winning gives it meaning.','いいですね。勝ってこそ意味があります。'),('그렇게 나오셔야지요.','That is the way to play it.','そう来なくては。'),('역시 제 마스터답습니다.','That is just like my Master.','さすがは私のマスターです。')])
add('pos','야망','royal',[('좋다. 이겨야 의미가 있느니라.','Good. Only victory gives it meaning.','よい。勝ってこそ意味があるのだ。'),('그렇게 나와야 하느니라.','That is how one must act.','そうでなくてはならぬ。'),('쓸 만한 주인이로구나.','A master of some use after all.','使える主ではないか。')])
add('pos','야망','mute',[('이를 드러내며 웃었다.','bared their teeth in a grin.','歯を見せて笑った。'),('주먹을 쥐어 보였다.','raised a clenched fist.','拳を握ってみせた。'),('눈이 번뜩였다.','their eyes flashed.','目がぎらりと光った。')])
add('pos','자유','polite',[('마음 가는 대로 하시는 편이 좋습니다.','It is better to do as your heart says.','心のままにするほうがいいですよ。'),('네, 묶여 있을 필요는 없지요.','Yes, there is no need to be bound.','ええ、縛られる必要はありません。'),('시원하네요.','How refreshing.','すっきりしますね。')])
add('pos','자유','royal',[('그대 뜻대로 하는 것이 좋으니라.','It is best that you follow your own will.','そなたの思うままにするがよい。'),('그래, 얽매일 까닭이 없느니라.','Aye, there is no reason to be fettered.','うむ、縛られる謂れはない。'),('시원하구나.','How refreshing.','清々しいのう。')])
add('pos','자유','mute',[('어깨를 활짝 폈다.','threw their shoulders back.','肩を大きく開いた。'),('바람이 부는 쪽으로 얼굴을 돌렸다.','turned their face toward the wind.','風の吹くほうへ顔を向けた。'),('발걸음이 가벼워졌다.','their steps grew lighter.','足取りが軽くなった。')])
# ---- 갈림길: 언짢게 봤을 때 ----
add('neg','명예','polite',[('…그건 정당한 싸움이 아닙니다.','…That is not a fair fight.','…それは正当な戦いではありません。'),('그런 승리는 원하지 않습니다.','I do not want a victory like that.','そんな勝利は望みません。'),('실망했습니다, 마스터.','I am disappointed, Master.','失望しました、マスター。')])
add('neg','명예','royal',[('…그것은 정당한 싸움이 아니니라.','…That is no fair fight.','…それは正当な戦いではない。'),('그런 승리는 짐이 바라지 않노라.','We desire no such victory.','そのような勝利、余は望まぬ。'),('실망이로다, 마스터.','How disappointing, Master.','失望したぞ、マスター。')])
add('neg','명예','mute',[('고개를 돌렸다.','turned their head away.','顔を背けた。'),('무기를 쥔 손에 힘을 주었다.','tightened their grip on their weapon.','武器を握る手に力を込めた。'),('한동안 당신을 쳐다보지 않았다.','did not look at you for some time.','しばらくあなたを見ようとしなかった。')])
add('neg','연민','polite',[('…그 사람들은 어떻게 되는 겁니까.','…What happens to those people?','…あの人たちはどうなるのですか。'),('그렇게까지 하셔야 했습니까.','Did you have to go that far?','そこまでする必要があったのですか。'),('차가운 분이군요.','You are a cold one.','冷たい方ですね。')])
add('neg','연민','royal',[('…그 백성들은 어찌 되느냐.','…What becomes of those people?','…あの民はどうなるのだ。'),('그렇게까지 해야 했느냐.','Was it necessary to go so far?','そこまでせねばならなかったのか。'),('차갑구나, 그대는.','You are cold.','冷たいのう、そなたは。')])
add('neg','연민','mute',[('뒤를 돌아보았다.','looked back over their shoulder.','後ろを振り返った。'),('입술을 깨물었다.','bit their lip.','唇を噛んだ。'),('당신에게서 한 걸음 물러섰다.','took a step back from you.','あなたから一歩下がった。')])
add('neg','충성','polite',[('저를 믿지 못하시는 겁니까.','Do you not trust me?','私を信じられないのですか。'),('그래서야 등을 맡길 수 없습니다.','I cannot entrust my back to you like this.','それでは背中を預けられません。'),('…알겠습니다. 그런 분이시군요.','…I see. So that is the kind of person you are.','…わかりました。そういう方なのですね。')])
add('neg','충성','royal',[('짐을 믿지 못하는 것이냐.','Do you not trust Us?','余を信じられぬのか。'),('그래서야 등을 맡길 수 없느니라.','We cannot entrust Our back to you like this.','それでは背中は預けられぬ。'),('…알겠노라. 그대는 그런 자로구나.','…We see. So that is what you are.','…わかった。そなたはそういう者か。')])
add('neg','충성','mute',[('당신을 물끄러미 바라보았다.','stared at you blankly.','あなたをじっと見つめた。'),('당신과 거리를 두고 섰다.','stood at a distance from you.','あなたと距離を置いて立った。'),('등을 돌린 채 한참 서 있었다.','stood with their back turned for a long while.','背を向けたまま長く立っていた。')])
add('neg','야망','polite',[('무르시군요. 그래서는 이길 수 없습니다.','Too soft. You cannot win like that.','甘いですね。それでは勝てません。'),('기회를 버리시다니요.','To throw away a chance like that.','好機を捨てるなんて。'),('한심하군요.','Pathetic.','情けないですね。')])
add('neg','야망','royal',[('무르구나. 그래서야 이길 수 없느니라.','Too soft. One cannot win like that.','甘いのう。それでは勝てぬ。'),('기회를 버리다니.','To cast away an opportunity.','好機を捨てるとは。'),('한심하도다.','Pathetic.','嘆かわしい。')])
add('neg','야망','mute',[('코웃음을 쳤다.','snorted.','鼻で笑った。'),('혀를 차는 듯한 소리를 냈다.','made a sound like a click of the tongue.','舌打ちのような音を立てた。'),('당신을 외면했다.','looked away from you.','あなたから目を逸らした。')])
add('neg','자유','polite',[('숨이 막히는군요.','This is suffocating.','息が詰まりますね。'),('저를 사슬로 묶어 두시겠다는 겁니까.','Do you mean to keep me in chains?','私を鎖で繋いでおくつもりですか。'),('…답답합니다.','…This is stifling.','…窮屈です。')])
add('neg','자유','royal',[('숨이 막히는구나.','This is suffocating.','息が詰まるのう。'),('짐을 사슬로 묶어 두겠다는 것이냐.','Do you mean to keep Us in chains?','余を鎖で繋いでおくつもりか。'),('…답답하도다.','…How stifling.','…窮屈よ。')])
add('neg','자유','mute',[('목을 문지르듯 손을 올렸다.','raised a hand as if rubbing their neck.','首をさするように手を上げた。'),('창밖을 오래 바라보았다.','gazed out the window for a long time.','窓の外を長く眺めた。'),('가만히 한숨을 내쉬었다.','let out a quiet sigh.','静かにため息をついた。')])
# ---- 싸우지 않을 때 재촉 ----
add('rst','명예','polite',[('언제까지 이 안에 계실 생각입니까. 싸움은 기다린다고 오지 않습니다.','How long do you intend to stay in here? A fight will not come just because you wait.','いつまでここに籠もるおつもりですか。戦いは待っていても来ません。'),('숨어 있는 것과 등을 보이는 것은 다르지 않습니다.','Hiding is no different from turning your back.','隠れていることは背を見せることと変わりません。'),('저를 부르신 건 지키라고가 아니라 이기라고였을 텐데요.','Surely you summoned me to win, not to guard.','私を喚んだのは守るためではなく勝つためだったはずです。')])
add('rst','명예','royal',[('언제까지 이 안에 틀어박혀 있을 셈이냐. 싸움은 기다린다고 오지 않느니라.','How long do you mean to shut yourself in here? Battle does not come to those who wait.','いつまでここに籠もっているつもりだ。戦は待っていても来ぬぞ。'),('숨는 것과 등을 보이는 것은 다르지 않느니라.','To hide is no different from turning one\'s back.','隠れることと背を見せることは変わらぬ。'),('짐을 부른 것은 지키라고가 아니라 이기라고였을 터인데.','You summoned Us to conquer, not to guard.','余を喚んだのは守るためではなく勝つためであったはずだがな。')])
add('rst','명예','mute',[('문 쪽을 몇 번이고 돌아보았다.','kept glancing toward the door.','何度も扉のほうを振り返った。'),('무기를 손질하다 말고 당신을 쳐다보았다.','stopped tending their weapon and looked at you.','武器の手入れの手を止めてあなたを見た。'),('닫힌 창 너머를 오래 노려보았다.','glared through the closed window for a long time.','閉じた窓の向こうを長く睨んだ。')])
add('rst','야망','polite',[('기다리기만 해서는 아무것도 손에 들어오지 않습니다, 마스터.','Nothing comes into your hands by waiting alone, Master.','待っているだけでは何も手に入りません、マスター。'),('다른 조가 먼저 차지하는 걸 보고만 계실 겁니까.','Will you just watch while other teams take it first?','他の組が先に手にするのを、ただ見ているおつもりですか。'),('겁쟁이의 서번트로 기억되고 싶지는 않군요.','I would rather not be remembered as a coward\'s Servant.','臆病者のサーヴァントとして記憶されたくはありませんね。')])
add('rst','야망','royal',[('기다리기만 해서는 아무것도 손에 들어오지 않느니라, 마스터.','Nothing falls into one\'s hands by waiting, Master.','待つだけでは何も手に入らぬぞ、マスター。'),('다른 자들이 먼저 차지하는 것을 보고만 있을 셈이냐.','Will you merely watch as others seize it first?','他の者が先に手にするのを、ただ眺めているつもりか。'),('겁쟁이의 서번트로 기억되고 싶지는 않구나.','We have no wish to be remembered as a coward\'s Servant.','臆病者のサーヴァントとして名を残すのは御免だ。')])
add('rst','야망','mute',[('지도 위 다른 조의 거처를 손가락으로 두드렸다.','tapped the other teams\' hideouts on the map.','地図の上の他の組の拠点を指で叩いた。'),('초조하게 방 안을 서성였다.','paced the room restlessly.','苛立たしげに部屋の中を歩き回った。'),('당신을 보고 짧게 콧김을 내뿜었다.','looked at you and snorted shortly.','あなたを見て短く鼻を鳴らした。')])
# ---- 다쳐서 쉴 때 ----
add('rsth','명예','polite',[('이 상처로 검을 들면 이길 싸움도 집니다. 오늘 밤은 숨을 고르지요.','If I take up my sword with these wounds, I will lose even a fight I could win. Let us catch our breath tonight.','この傷で剣を取れば、勝てる戦いも負けます。今夜は息を整えましょう。'),('물러서는 게 아닙니다. 다시 서기 위해 잠시 앉아 있는 것뿐입니다.','I am not retreating. I am only sitting a while so I can stand again.','退くのではありません。もう一度立つため、少し座っているだけです。'),('상처가 아물면 그때 이 빚을 갚으러 가지요.','Once these wounds heal, we will go repay this debt.','傷が癒えたら、そのときこの借りを返しに行きましょう。')])
add('rsth','명예','royal',[('이 상처로 칼을 들면 이길 싸움도 지느니라. 오늘 밤은 숨을 고르마.','To take up the blade with these wounds is to lose even a winnable fight. Tonight, We shall rest.','この傷で刃を取れば、勝てる戦も落とす。今宵は息を整えるとしよう。'),('물러서는 것이 아니다. 다시 서기 위해 잠시 앉아 있는 것뿐이니라.','This is no retreat. We merely sit a while so that We may stand again.','退くのではない。再び立つため、しばし腰を下ろすだけのこと。'),('상처가 아물면 그때 이 빚을 갚으러 가자꾸나.','When these wounds have healed, let us go and repay this debt.','傷が癒えたら、この借りを返しに参ろうぞ。')])
add('rsth','명예','mute',[('상처를 감싼 채 벽에 기대어 눈을 감았다.','leaned against the wall with their wounds bound and closed their eyes.','傷を押さえたまま壁にもたれ、目を閉じた。'),('무기를 내려놓고 조용히 앉았다.','set down their weapon and sat quietly.','武器を置いて静かに座った。'),('아문 자리를 확인하듯 팔을 몇 번 움직여 보았다.','moved their arm a few times as if testing the healing.','傷の具合を確かめるように腕を何度か動かしてみた。')])
add('rsth','야망','polite',[('다친 몸으로 덤비는 건 야망이 아니라 어리석음입니다. 회복이 먼저예요.','Charging in wounded is not ambition but foolishness. Recovery comes first.','傷ついた身で挑むのは野心ではなく愚かさです。回復が先ですよ。'),('지금은 쉬어 두겠습니다. 차지할 때는 온전한 몸이어야 하니까요.','I will rest for now. When we claim it, I must be whole.','今は休んでおきます。手にするときは万全でなければいけませんから。'),('서두를 것 없습니다. 성배는 마지막에 서 있는 자의 것이니까요.','There is no need to hurry. The Grail belongs to whoever is standing at the end.','急ぐ必要はありません。聖杯は最後に立っている者のものですから。')])
add('rsth','야망','royal',[('다친 몸으로 덤비는 것은 야망이 아니라 어리석음이니라. 회복이 먼저다.','To charge in wounded is not ambition but folly. Recovery comes first.','傷を負った身で挑むは野心にあらず、愚かさよ。まずは癒えることだ。'),('지금은 쉬어 두마. 차지할 때는 온전한 몸이어야 하니.','We shall rest for now. One must be whole when one seizes the prize.','今は休んでおこう。手にするときは万全でなければな。'),('서두를 것 없느니라. 성배는 마지막에 서 있는 자의 것이니.','There is no need for haste. The Grail belongs to the one left standing at the end.','急くことはない。聖杯は最後に立つ者のものよ。')])
add('rsth','야망','mute',[('상처를 매만지며 낮게 숨을 골랐다.','tended their wounds and breathed low and even.','傷をさすりながら低く息を整えた。'),('몸을 웅크리고 잠들었다.','curled up and fell asleep.','身を丸めて眠った。'),('한쪽 눈만 뜬 채 바깥 기척에 귀를 기울였다.','listened for movement outside with one eye open.','片目だけを開けたまま、外の気配に耳を澄ませた。')])

TRV = {}
for g, t, reg, ko, en, ja in R: TRV.setdefault(g, {}).setdefault(t, {}).setdefault(reg, []).append(ko)
JS_HELP = ("const TRV=" + json.dumps(TRV, ensure_ascii=False, separators=(',', ':')) + ";\n"
  "  // 서번트 말투에 맞는 한마디: 반말은 원래 묶음(B), 존댓말 · 왕의 말투는 따옴표 말, 말 없음은 「이름은 …했다」\n"
  "  const trLine=(h,g,t,B)=>{ const v=VREG(h), L=v!=='plain'&&TRV[g]&&TRV[g][t]&&TRV[g][t][v]; if(!L) return `${h.name}: ${pick(B[t])}`; const l=pick(L); return v==='mute'?`${h.name}${J(h.name,은)} ${l}`:`${h.name}: “${l}”`; };\n  ")
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("const TRJ={명예:'를',연민:'을',충성:'을',야망:'을',자유:'를'};", JS_HELP + "const TRJ={명예:'를',연민:'을',충성:'을',야망:'을',자유:'를'};")
    rp("if(lead) log(`${h.name}: ${pick((r[lead]>0?TR_POS:TR_NEG)[lead])}`,'voice');", "if(lead) log(trLine(h,r[lead]>0?'pos':'neg',lead,r[lead]>0?TR_POS:TR_NEG),'voice');")
    rp("log(`${h.name}: ${pick(amb?RST_HURT.야망:RST_HURT.명예)}`,'voice');", "log(trLine(h,'rsth',amb?'야망':'명예',RST_HURT),'voice');")
    rp("log(`${h.name}: ${pick(amb?RST.야망:RST.명예)}`,'voice');", "log(trLine(h,'rst',amb?'야망':'명예',RST),'voice');")
    D = []; T = []
    for g, t, reg, ko, en, ja in R:
        if reg == 'mute':
            T.append(('{0~은} ' + ko, ("{0}'s " + en[6:]) if en.startswith('their ') else '{0} ' + en, '{0}は' + ja))
        else:
            D.append((ko, en, ja)); D.append(('“' + ko + '”', '“' + en + '”', '「' + ja.rstrip('。') + '」'))
    s, nd, nt = i18n.add(s, D, T)
    print('reg1113 miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
