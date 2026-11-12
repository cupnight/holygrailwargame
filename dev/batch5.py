# 신규 서번트 5차: 에미야[얼터](아처) — 2026-11-12
# 모든 문장은 (한국어, 영어, 일본어). 원작 대사를 옮기지 않고 새로 쓴 문장이다. 호칭(마스터) · 1인칭(나 / オレ) · 냉소적으로 짧게 끊는 말투만 빌렸다.
# 관계 대사는 키아라와만 잇는다(ea_apply.py). 다른 서번트와의 만남 대사 · 짝 대사는 만들지 않는다(사용자 결정).
T = lambda ko, en, ja: (ko, en, ja)
N = '에미야[얼터]'
B = []
B.append(dict(
 id='emiya_alter', cls='bow', name=T(N,'EMIYA (Alter)','エミヤ〔オルタ〕'), title=T('이상을 버린 수호자','The Guardian Who Discarded His Ideal','理想を捨てた守護者'),
 frm=T('무참히 실추된 집행자','The Executor, Fallen in Ruin','無惨に失墜した執行者'), hint=T('이상을 잃은 끝에 남은 사내의 이야기','The tale of the man left over after his ideal was lost','理想を失った果てに残った男の話'),
 s=['C','D','B','B','E'],
 art=dict(n=T('무한의 검제','Unlimited Lost Works','無限の剣製'), d=T('상대의 몸 안에서 터지는 검의 황야','A wasteland of swords that bursts open inside the target','相手の体内で弾ける剣の荒野')),
 traits=['자유','야망'],
 wish=T('없음. 받은 일을 끝까지 치우는 것뿐','None. Only to see the job he took through to the end','なし。請けた仕事を最後まで片づけることだけ'),
 relic=T('칼날이 붙은 권총에서 나온 빈 탄피 하나','A single spent casing from a bladed pistol','刃のついた拳銃から出た空薬莢ひとつ'),
 frags=[
  T('한때는 누군가를 구하겠다고 설쳤던 모양이야. 기억은 없어. 남은 건 방아쇠를 당기는 순서뿐이지.',"Seems I once ran around trying to save someone. I don't remember it. All that's left is the order in which to pull the trigger.",'昔は誰かを救うだのと息巻いていたらしい。覚えはない。残っているのは引き金を引く順番だけだ。'),
  T('한 여자를 쫓았다. 구원을 판다는 여자였지. 그 여자 하나를 막겠다고 죄 없는 놈들까지 쐈어. 그때부터 나는 정의의 편이 아니라 청소부야.',"I hunted a woman. One who claimed to sell salvation. To stop that one woman, I shot people who'd done nothing. Since then I haven't been an ally of justice. I'm a cleaner.",'ある女を追った。救いを売るという女だ。その女ひとりを止めるために、罪のない連中まで撃った。あれ以来オレは正義の味方じゃない。掃除屋だ。'),
  T('기억이 자꾸 빠져나가. 어제 먹은 것도, 네 얼굴도 언젠가 흐려지겠지. 그러니 중요한 건 지금 말해 둬. 잊기 전에 끝내 줄 테니.',"My memory keeps draining away. What I ate yesterday, your face — it'll all blur someday. So tell me what matters now. I'll finish it before I forget.",'記憶がどんどん抜けていく。昨日食ったものも、お前の顔も、いずれ霞むだろう。だから大事なことは今言っておけ。忘れる前に片づけてやる。')],
 voice=dict(reg='plain', ord=0,
  greet=T('아처. 진명 같은 건 쓸모없으니 됐어. 일이 있어서 부른 거겠지, 마스터. 표적만 말해.',"Archer. Skip the true name, it's useless. You called because there's a job, Master. Just name the target.",'アーチャーだ。真名なんぞ役に立たん、いい。仕事があるから呼んだんだろう、マスター。標的だけ言え。'),
  bow=T('인사는 됐어. 고개 숙일 시간에 탄창이나 세어 두지.','Skip the greetings. Count your magazines instead of bowing.','挨拶はいい。頭を下げる暇があるなら弾倉でも数えておけ。'),
  wish=T('소원? 없어. 받은 일을 끝내는 게 전부야. 성배는 네가 알아서 써.',"A wish? None. Finishing the job is all there is. Use the Grail however you like.",'願い？ない。請けた仕事を終わらせる、それだけだ。聖杯はお前が好きに使え。'),
  order=T('명령이군. 좋아, 그게 제일 편해. 이유는 안 물어.',"An order. Good, that's easiest. I won't ask why.",'命令か。いい、それが一番楽だ。理由は訊かん。'),
  plan=T('작전은 단순할수록 좋아. 약한 놈부터, 등 뒤에서. 불만 있나?','The simpler the plan, the better. Weakest first, from behind. Any complaints?','作戦は単純なほどいい。弱い奴から、背後から。文句はあるか？'),
  naive=T('아무것도 모르고 날 불렀다고? 운도 없군. 성배전쟁이야. 일곱 조가 서로 죽이고, 남은 한 조가 소원을 가져가. 설명은 여기까지.',"You summoned me knowing nothing? Rotten luck. It's the Holy Grail War. Seven pairs kill each other, and the last one standing takes the wish. That's the whole briefing.",'何も知らずにオレを呼んだだと？運のない奴だ。聖杯戦争だ。七組が殺し合い、残った一組が願いを持っていく。説明は以上だ。'),
  thanks=T('감사는 필요 없어. 대가는 마력으로 받고 있으니까. …뭐, 나쁜 기분은 아니군.',"No need for thanks. I'm already paid in mana. ...Well. It doesn't feel bad.",'礼は要らん。対価は魔力で受け取っている。……まあ、悪い気はしないな。'),
  flee=T('물러나자고? 현명해. 질 싸움에 남는 건 바보나 영웅이야. 나는 둘 다 아니고.',"Fall back? Smart. Only fools and heroes stay in a losing fight. I'm neither.",'退くだと？賢明だ。負け戦に残るのは馬鹿か英雄だけだ。オレはどちらでもない。'),
  seals0=T('령주가 바닥났군. 걱정 마. 사슬이 없어도 받은 일은 끝내. 그게 내 유일한 장점이라서.',"Out of Command Spells. Don't worry. Chain or no chain, I finish the job. It's my one virtue.",'令呪が尽きたか。心配するな。鎖がなくても請けた仕事は終わらせる。それがオレの唯一の取り柄でな。'),
  dawn=T('해가 떴어. 밤새 접근한 놈은 없다. 눈 좀 붙였으면 움직이지, 마스터.',"Sun's up. Nobody came near in the night. If you got some sleep, we move, Master.",'日が昇った。夜の間に近づいた奴はいない。少しは眠れたなら動くぞ、マスター。'),
  refuse=T('그래, 네 판단이니까. 결과도 네 몫이야. 나는 뒷정리만 하지.',"Fine, it's your call. The outcome's yours too. I just clean up after.",'そうか、お前の判断だ。結果もお前の取り分だ。オレは後始末だけする。'),
  grailNo=T('이 잔은 썩었어. 냄새로 알아. …이런 걸 치우는 게 원래 내 일이었지. 물러서, 마스터.',"This cup is rotten. I can tell by the smell. ...Clearing out things like this was my job to begin with. Step back, Master.",'この杯は腐っている。臭いで分かる。……こういうものを片づけるのが、元々オレの仕事だった。下がれ、マスター。'),
  grailYes=T('끝났군. 살아남았으면 이긴 거야. 잔은 네 거다. 나는 받은 일을 끝낸 걸로 충분해.',"It's over. If you're alive, you won. The cup is yours. Finishing the job is enough for me.",'終わったな。生き残ったなら勝ちだ。杯はお前のものだ。オレは請けた仕事を終えた、それで十分だ。'),
  cold=T('…너도 날 도구로만 쓰는군. 상관없어. 도구는 불평하지 않으니까.',"...So you use me as a tool too. Doesn't matter. Tools don't complain.",'……お前もオレを道具としてしか使わんか。構わん。道具は文句を言わない。'),
  askWish=T('하나 묻지. 넌 그 잔에 뭘 빌 건가. …아니, 대답하지 마. 들으면 쏘기 어려워질지도 모르니.',"One question. What will you wish on that cup? ...No, don't answer. Hearing it might make it harder to shoot.",'ひとつ訊く。お前はあの杯に何を願う。……いや、答えるな。聞けば撃ちにくくなるかもしれん。'),
  bye=[T('계약은 여기까지다. 내 얼굴은 잊어. 나도 곧 잊을 테니까.',"The contract ends here. Forget my face. I'll forget yours soon enough.",'契約はここまでだ。オレの顔は忘れろ。オレもすぐに忘れる。'),
       T('…이상하군. 이번 일은 잊고 싶지 않아. 잘 있어, 마스터.',"...Strange. This is one job I don't want to forget. Take care, Master.",'……妙だな。今回の仕事は忘れたくない。達者でな、マスター。')]),
 hline=[T('표적 확인.','Target confirmed.','標的、確認。'), T('안쪽에서부터 부서져라.','Break apart from the inside.','内側から砕けろ。'), T('정의 같은 건 탄창에 안 들어가.',"Justice doesn't fit in a magazine.",'正義なんてものは弾倉に入らん。')],
 hday=[T(N+'는 창가에 앉아 권총을 분해하고 닦았다. 다 끝나자 처음부터 다시 닦았다.','EMIYA (Alter) sat by the window, stripping and cleaning his pistols. When he finished, he started over from the beginning.','エミヤ〔オルタ〕は窓辺に座り、拳銃を分解して磨いた。終わると、また最初から磨き直した。'),
       T(N+'는 냉장고 앞에 한참 서 있다가 그냥 닫았다. 무엇을 만들려 했는지 잊은 얼굴이었다.','EMIYA (Alter) stood in front of the refrigerator for a long while, then simply closed it. He had the look of a man who had forgotten what he meant to make.','エミヤ〔オルタ〕は冷蔵庫の前にしばらく立ち、そのまま閉めた。何を作るつもりだったのか忘れた顔だった。'),
       T(N+'는 옥상에서 도시를 내려다보며 접근로를 손가락으로 세고 있었다.','EMIYA (Alter) looked down on the city from the rooftop, counting approach routes on his fingers.','エミヤ〔オルタ〕は屋上から街を見下ろし、接近経路を指で数えていた。')],
 talk=dict(t=[T('밥은 먹었나. …아니, 걱정이 아니라 전력 관리야. 굶은 마스터는 마력이 달려.',"Have you eaten? ...No, that's not concern. It's asset management. A starving Master runs short on mana.",'飯は食ったか。……いや、心配じゃない。戦力管理だ。飢えたマスターは魔力が足りなくなる。'),
              T('가끔 부엌에 서면 손이 먼저 움직여. 뭘 만들던 손인지는 몰라. 맛은… 네가 판단해.',"Sometimes when I stand in a kitchen, my hands move first. I don't know what they used to make. The taste... you be the judge.",'たまに台所に立つと、手が先に動く。何を作っていた手なのかは分からん。味は……お前が判断しろ。')],
           w=[T(N+'는 당신보다 반 걸음 뒤에서 걸었다. 골목마다 지붕과 창을 훑었다. "산책이라. 표적이 되기 좋은 버릇이군." 그래도 걸음은 당신에게 맞추고 있었다.','EMIYA (Alter) walked half a step behind you, scanning the roofs and windows of every alley. "A stroll. A fine habit for getting shot." Even so, he kept his pace matched to yours.','エミヤ〔オルタ〕はあなたの半歩後ろを歩いた。路地ごとに屋根と窓を見渡した。「散歩か。標的になるにはいい癖だ」それでも、歩調はあなたに合わせていた。')]),
 weak=T('닳아 없어져 가는 기억','Memories wearing away to nothing','擦り切れて消えていく記憶'),
 lastw=[T('…여기까지군. 받은 일을 못 끝냈어. 미안하다고는 안 해.',"...So this is it. I didn't finish the job. I won't say I'm sorry.",'……ここまでか。請けた仕事を終えられなかった。すまないとは言わん。'),
        T('아, 그래. 네 이름… 아직 기억나. 다행이군.',"Ah, right. Your name... I still remember it. Good.",'ああ、そうだ。お前の名前……まだ覚えている。よかった。')],
 artx=dict(n=T('무한의 검제 - 언리미티드 로스트 웍스','Unlimited Lost Works','無限の剣製 - アンリミテッド・ロストワークス'), r='E~A++', k=T('대인보구','Anti-Unit','対人宝具'),
           x=T('총구로 쏘아 넣은 칼날 속에서 검의 황야를 터뜨린다. 이상을 잃은 자의 고유결계는 더 이상 세계를 덮지 않고, 상대의 몸 안에서만 펼쳐진다.','From a blade fired in through the muzzle, a wasteland of swords bursts open. The Reality Marble of a man who lost his ideal no longer covers the world; it unfolds only inside his target.','銃口から撃ち込んだ刃の中から、剣の荒野を炸裂させる。理想を失った者の固有結界はもう世界を覆わず、相手の体内でのみ展開される。')),
 sk=[['대마력','D',1],['단독행동','A',1],['방탄 가공','A'],['비웃는 철심','A'],['투영 마술','C']],
 npr='Ap', hx='냉소 혼돈 악', hal='CE',
 npi=T('상대의 대마력·회피나 결계의 보호에 깎이지 않고 피해가 그대로 닿는다','Damage lands in full, not reduced by Magic Resistance, evasion, or the protection of a field','相手の対魔力・回避や結界の守りに削られず、ダメージがそのまま届く'),
))
SKX = {
 '방탄 가공': ('fort', T('몸을 단단히 가공해 총탄과 칼날을 받아 낸다','A body reinforced to take bullets and blades','体を固く加工し、銃弾と刃を受け止める')),
 '비웃는 철심': ('insight', T('스스로를 비웃는 차가운 마음. 흔들림 없이 싸움을 계산한다','A cold heart that sneers at itself. It calculates the fight without wavering','自らを嗤う冷たい心。揺らぐことなく戦いを計算する')),
 '투영 마술': ('power', T('무기를 투영해 꺼내 쓴다. 싸움이 길어질수록 손에 쥘 것이 늘어난다','Projects weapons to hand. The longer the fight, the more he has to draw on','武器を投影して取り出す。戦いが長引くほど手にするものが増える')),
}
SKN = {'방탄 가공': ('Bulletproof Treatment','防弾加工'), '비웃는 철심': ('Sneering Iron Heart','嗤う鉄心'), '투영 마술': ('Projection Magecraft','投影魔術')}
RIVAL = []
