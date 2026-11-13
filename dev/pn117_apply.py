"""11-14: 패치 노트 v2.00 (사용자 확정 문구 · 원래 v1.17로 쓰던 것을 2.00으로 올림) · 영어 · 일본어
사용: python3 pn117_apply.py <game.html>   (pnver_apply 뒤에)"""
import sys, json, i18n
V, N, T = '2026.11.14', '2.00', '달에서 온 이레귤러'
G = [
 ('새 후반 위기', [
   ('새로운 후반 위기가 추가됩니다. 성배가 봉인되고, 밤마다 도시를 떠도는 것들이 나타납니다.', [
     '마스터는 봉인한 쪽을 몰아붙이거나, 떠도는 것들을 쫓거나, 진실을 파헤칠 수 있습니다. 어떤 길을 고르느냐에 따라 결전의 모습이 달라집니다.']),
   '위기 배너가 위기마다 다른 아이콘, 색, 단계로 표시됩니다.']),
 ('새 클래스와 서번트', [
   '새 클래스 문 캔서와 얼터 에고가 추가됩니다.',
   ('새 서번트: BB, 멜트릴리스, 패션립, 스즈카 고젠, 타마모 캣, 에미야[얼터]', [
     'BB, 멜트릴리스, 패션립은 평소의 소환과는 다른 길로 나타납니다.',
     '새 서번트 모두 인연 대사, 짝 대사, 얼굴 이미지가 들어갑니다.']),
   '문 캔서와 얼터 에고 전용 소환 연출이 추가됩니다.']),
 ('서번트 속성과 취향', [
   '서번트마다 Fate 공식 속성(질서·중립·혼돈 × 선·중용·악)이 생겼습니다. 도감에서 확인할 수 있습니다.',
   '서번트는 이제 성향과 속성을 함께 따져 마스터의 선택에 반응합니다. 질서의 서번트는 약속과 규칙을, 혼돈의 서번트는 자기 뜻을, 선의 서번트는 무고한 사람을 중히 여깁니다.',
   '일부 서번트는 원전에 따라 특정 선택을 유난히 좋아하거나 싫어합니다.',
   '영혼 포식 사건을 없앴습니다. 민간인에게서 마력을 얻는 길은 마력 수집으로 남아 있습니다.']),
 ('궁합', [
   ('인연이 깊을수록 궁합이 어긋날 때의 감점이 줄어듭니다.', [
     "인연 1~2단계에서는 '쌓인 인연 덕에 조금씩 가까워진다'는 회색 칩이 붙고, 3단계에서는 궁합 어긋남 칩이 붙지 않습니다."]),
   '서번트가 선택을 마음에 들어 했는데 궁합이 어긋난 경우, 칩 문구가 그 흐름에 맞게 이어집니다.']),
 ('에필로그', [
   ('시간이 흐르는 방식이 바뀝니다. 처음 14일은 하루씩, 첫 1년은 한 달씩, 그 뒤 10년은 1년씩 흐릅니다.', [
     '구간마다 그 시기의 일상 묘사가 나옵니다.',
     '새 사건 81개가 추가됩니다.',
     '현재 에필로그 구성 상, 중년에 결혼 등의 이벤트가 진행되는 경우가 많아 개선하게 되었습니다.']),
   '우정으로 정해진 경우에도, 에필로그에서 성인이 된 뒤나 배우자와 사별한 뒤 한 번 애정으로 바꿀 수 있는 장면이 나옵니다.',
   '사건 도중에 저장했다가 불러오면 같은 사건이 다시 뜹니다.']),
 ('이스칸다르', [
   '이스칸다르의 소원이 수육으로 바뀝니다. 소원 문구, 대사, 성배 앞 선택, 에필로그 사건이 이에 맞게 바뀝니다.']),
 ('전투 화면', [
   '함께 싸우는 조가 얼굴, 상태, 보구를 썼는지와 함께 표시됩니다.']),
 ('로비와 로딩', [
   '로비의 구성이 변경됩니다.',
   ('도시의 밤을 배경으로 한 구성으로 변경됩니다.', [
     '지난 생, 서번트 도감, 업적이 배경 위에 펼쳐집니다.',
     "'움직임 줄이기'를 켠 기기에서도 배경이 움직이되, 1초에 30번 그립니다."]),
   '게임이 로딩 중인 경우, 로딩 화면이 추가됩니다.']),
 ('결과 화면', [
   '성배전쟁 기록의 조 목록에 서번트 얼굴이 표시됩니다.',
   '결과 화면을 이미지로 저장하는 「캡처하기」가 추가됩니다.']),
 ('서번트 대사 말투', [
   '갈림길에서의 평가, 싸우지 않을 때의 재촉, 다쳐서 쉴 때의 한마디가 서번트 말투에 맞게 바뀝니다.']),
 ('업적과 패치 노트', [
   '신규 위기 업적 18개가 추가됩니다.',
   '업적 화면은 분류 안에서 최근에 추가된 업적 순서로 정렬됩니다.']),
 ('수정', [
   ('인질을 구하는 날에 결투장 사건이 겹치던 문제를 수정했습니다.', [
     '인질 구출전을 대화로 끝내도 구출한 것으로 칩니다.']),
   '교회 의뢰를 받은 뒤 사도 마스터를 암살로 처리해도 보상을 받습니다.',
   '우정 3단계의 이름이 「죽마고우」에서 「지기」로 바뀝니다.',
   '성유물을 다시 뽑던 문제를 수정했습니다.',
   '선택 창이 뜬 직후 0.3초 동안은 터치를 받지 않아, 실수로 선택지를 누르는 일을 막습니다.',
   '랭크가 한 단계 내려갈 때 +가 그대로 남습니다. (예: A+ → B+)',
   '전투 중 대화로 이미 동맹을 맺은 조가 사건으로 다시 동맹을 제안하던 문제를 수정했습니다.']),
]
TR = {
 '달에서 온 이레귤러': ('The Irregular from the Moon', '月から来たイレギュラー'),
 '새 후반 위기': ('New late-war crisis', '新たな後半の危機'),
 '새로운 후반 위기가 추가됩니다. 성배가 봉인되고, 밤마다 도시를 떠도는 것들이 나타납니다.': ('A new late-war crisis has been added. The Grail is sealed, and things begin to wander the city every night.', '新たな後半の危機が追加されます。聖杯が封印され、夜ごと街をさまようものたちが現れます。'),
 '마스터는 봉인한 쪽을 몰아붙이거나, 떠도는 것들을 쫓거나, 진실을 파헤칠 수 있습니다. 어떤 길을 고르느냐에 따라 결전의 모습이 달라집니다.': ('As a Master, you can press whoever sealed it, hunt the wanderers, or dig for the truth. The final battle changes depending on the path you choose.', 'マスターは封印した側を追い詰めることも、さまようものたちを追うことも、真実を暴くこともできます。どの道を選ぶかで決戦の姿が変わります。'),
 '위기 배너가 위기마다 다른 아이콘, 색, 단계로 표시됩니다.': ('The crisis banner now shows a different icon, color, and stage for each crisis.', '危機バナーが危機ごとに異なるアイコン、色、段階で表示されます。'),
 '새 클래스와 서번트': ('New classes and Servants', '新クラスとサーヴァント'),
 '새 클래스 문 캔서와 얼터 에고가 추가됩니다.': ('New classes Moon Cancer and Alter Ego have been added.', '新クラス、ムーンキャンサーとアルターエゴが追加されます。'),
 '새 서번트: BB, 멜트릴리스, 패션립, 스즈카 고젠, 타마모 캣, 에미야[얼터]': ('New Servants: BB, Meltryllis, Passionlip, Suzuka Gozen, Tamamo Cat, EMIYA (Alter)', '新サーヴァント：BB、メルトリリス、パッションリップ、鈴鹿御前、タマモキャット、エミヤ〔オルタ〕'),
 'BB, 멜트릴리스, 패션립은 평소의 소환과는 다른 길로 나타납니다.': ('BB, Meltryllis, and Passionlip appear through paths different from the usual summoning.', 'BB、メルトリリス、パッションリップは、いつもの召喚とは違う道で現れます。'),
 '새 서번트 모두 인연 대사, 짝 대사, 얼굴 이미지가 들어갑니다.': ('All new Servants come with bond lines, pair lines, and face images.', '新サーヴァントにはすべて、縁の台詞、組み合わせ台詞、顔画像が入ります。'),
 '문 캔서와 얼터 에고 전용 소환 연출이 추가됩니다.': ('Dedicated summoning effects for Moon Cancer and Alter Ego have been added.', 'ムーンキャンサーとアルターエゴ専用の召喚演出が追加されます。'),
 '서번트 속성과 취향': ('Servant alignments and tastes', 'サーヴァントの属性と好み'),
 '서번트마다 Fate 공식 속성(질서·중립·혼돈 × 선·중용·악)이 생겼습니다. 도감에서 확인할 수 있습니다.': ("Each Servant now has an official Fate alignment (Lawful/Neutral/Chaotic × Good/Balanced/Evil). You can check it in the Servant Codex.", 'サーヴァントごとにFate公式の属性（秩序・中立・混沌 × 善・中庸・悪）が付きました。図鑑で確認できます。'),
 '서번트는 이제 성향과 속성을 함께 따져 마스터의 선택에 반응합니다. 질서의 서번트는 약속과 규칙을, 혼돈의 서번트는 자기 뜻을, 선의 서번트는 무고한 사람을 중히 여깁니다.': ("Servants now weigh both their disposition and alignment when reacting to your choices. Lawful Servants value promises and rules, Chaotic Servants value their own will, and Good Servants value innocent people.", 'サーヴァントは性向と属性の両方を踏まえて、マスターの選択に反応するようになります。秩序のサーヴァントは約束と規則を、混沌のサーヴァントは自らの意志を、善のサーヴァントは罪なき人を重んじます。'),
 '일부 서번트는 원전에 따라 특정 선택을 유난히 좋아하거나 싫어합니다.': ('Some Servants especially like or dislike certain choices, based on their source material.', '一部のサーヴァントは原典に沿って、特定の選択をことさら好んだり嫌ったりします。'),
 '영혼 포식 사건을 없앴습니다. 민간인에게서 마력을 얻는 길은 마력 수집으로 남아 있습니다.': ('The soul-devouring event has been removed. Gathering mana from civilians remains possible through mana collection.', '魂喰いのイベントを削除しました。民間人から魔力を得る道は魔力収集として残っています。'),
 '궁합': ('Compatibility', '相性'),
 '인연이 깊을수록 궁합이 어긋날 때의 감점이 줄어듭니다.': ('The deeper your bond, the smaller the penalty when compatibility clashes.', '縁が深いほど、相性が噛み合わないときの減点が小さくなります。'),
 "인연 1~2단계에서는 '쌓인 인연 덕에 조금씩 가까워진다'는 회색 칩이 붙고, 3단계에서는 궁합 어긋남 칩이 붙지 않습니다.": ("At bond stages 1–2, a grey chip reading 'growing a little closer thanks to the bond you've built' appears, and at stage 3 no compatibility-clash chip appears.", '縁1～2段階では「積み重ねた縁のおかげで少しずつ近づく」という灰色のチップが付き、3段階では相性のずれのチップが付きません。'),
 '서번트가 선택을 마음에 들어 했는데 궁합이 어긋난 경우, 칩 문구가 그 흐름에 맞게 이어집니다.': ('When a Servant liked your choice but your compatibility clashes, the chip text now follows on naturally.', 'サーヴァントが選択を気に入ったのに相性が噛み合わない場合、チップの文言がその流れに合わせてつながります。'),
 '에필로그': ('Epilogue', 'エピローグ'),
 '시간이 흐르는 방식이 바뀝니다. 처음 14일은 하루씩, 첫 1년은 한 달씩, 그 뒤 10년은 1년씩 흐릅니다.': ('Time now flows differently: the first 14 days pass one day at a time, the first year one month at a time, and the following 10 years one year at a time.', '時間の流れ方が変わります。最初の14日は一日ずつ、最初の1年はひと月ずつ、その後の10年は1年ずつ流れます。'),
 '구간마다 그 시기의 일상 묘사가 나옵니다.': ('Each stretch shows descriptions of everyday life for that period.', '区間ごとに、その時期の日常の描写が出ます。'),
 '새 사건 81개가 추가됩니다.': ('81 new events have been added.', '新しい出来事が81個追加されます。'),
 '현재 에필로그 구성 상, 중년에 결혼 등의 이벤트가 진행되는 경우가 많아 개선하게 되었습니다.': ('This was changed because, with the previous epilogue structure, events like marriage often happened in middle age.', 'これまでのエピローグの構成では、結婚などの出来事が中年になってから進むことが多かったため、改善しました。'),
 '우정으로 정해진 경우에도, 에필로그에서 성인이 된 뒤나 배우자와 사별한 뒤 한 번 애정으로 바꿀 수 있는 장면이 나옵니다.': ('Even if your bond was set to friendship, a scene may appear in the epilogue, after you come of age or lose your spouse, that lets you change it to love once.', '友情に決まっていた場合でも、エピローグで成人した後や配偶者と死別した後に、一度だけ愛情に変えられる場面が出ます。'),
 '사건 도중에 저장했다가 불러오면 같은 사건이 다시 뜹니다.': ('If you save in the middle of an event and load later, the same event appears again.', '出来事の途中でセーブしてロードすると、同じ出来事がもう一度表示されます。'),
 '이스칸다르': ('Iskandar', 'イスカンダル'),
 '이스칸다르의 소원이 수육으로 바뀝니다. 소원 문구, 대사, 성배 앞 선택, 에필로그 사건이 이에 맞게 바뀝니다.': ("Iskandar's wish is now incarnation. His wish text, lines, choices before the Grail, and epilogue events have changed to match.", 'イスカンダルの願いが受肉に変わります。願いの文言、台詞、聖杯の前での選択、エピローグの出来事もそれに合わせて変わります。'),
 '전투 화면': ('Battle screen', '戦闘画面'),
 '함께 싸우는 조가 얼굴, 상태, 보구를 썼는지와 함께 표시됩니다.': ('Teams fighting alongside you are now shown with their faces, condition, and whether they have used their Noble Phantasm.', '共に戦う組が、顔、状態、宝具を使ったかどうかと一緒に表示されます。'),
 '로비와 로딩': ('Lobby and loading', 'ロビーとロード'),
 '로비의 구성이 변경됩니다.': ('The lobby layout has changed.', 'ロビーの構成が変わります。'),
 '도시의 밤을 배경으로 한 구성으로 변경됩니다.': ('It now uses a layout set against the city at night.', '街の夜を背景にした構成に変わります。'),
 '지난 생, 서번트 도감, 업적이 배경 위에 펼쳐집니다.': ('Past lives, the Servant Codex, and achievements open up over the background.', '過去の人生、サーヴァント図鑑、実績が背景の上に広がります。'),
 "'움직임 줄이기'를 켠 기기에서도 배경이 움직이되, 1초에 30번 그립니다.": ("Even on devices with 'Reduce motion' turned on, the background moves, drawn 30 times per second.", '「動きを減らす」をオンにした端末でも背景は動きますが、1秒に30回描画します。'),
 '게임이 로딩 중인 경우, 로딩 화면이 추가됩니다.': ('A loading screen has been added while the game is loading.', 'ゲームの読み込み中にロード画面が表示されるようになります。'),
 '결과 화면': ('Result screen', '結果画面'),
 '성배전쟁 기록의 조 목록에 서번트 얼굴이 표시됩니다.': ("Servant faces are now shown in the team list of the Holy Grail War record.", '聖杯戦争の記録の組一覧に、サーヴァントの顔が表示されます。'),
 '결과 화면을 이미지로 저장하는 「캡처하기」가 추가됩니다.': ('A 「Capture」 button has been added to save the result screen as an image.', '結果画面を画像として保存する「キャプチャ」が追加されます。'),
 '서번트 대사 말투': ('Servant speech style', 'サーヴァントの台詞の口調'),
 '갈림길에서의 평가, 싸우지 않을 때의 재촉, 다쳐서 쉴 때의 한마디가 서번트 말투에 맞게 바뀝니다.': ("Servants' comments at crossroads, their urging when you aren't fighting, and their remarks while resting from injuries now match each Servant's speech style.", '分かれ道での評価、戦わないときの催促、負傷して休むときのひと言が、サーヴァントの口調に合わせて変わります。'),
 '업적과 패치 노트': ('Achievements and patch notes', '実績とパッチノート'),
 '신규 위기 업적 18개가 추가됩니다.': ('18 new crisis achievements have been added.', '新しい危機の実績が18個追加されます。'),
 '업적 화면은 분류 안에서 최근에 추가된 업적 순서로 정렬됩니다.': ('Within each category, the achievement screen is now sorted by when achievements were added.', '実績画面は、分類の中で追加された順に並ぶようになります。'),
 '수정': ('Fixes', '修正'),
 '인질을 구하는 날에 결투장 사건이 겹치던 문제를 수정했습니다.': ('Fixed an issue where a duel event could overlap with the day you rescue a hostage.', '人質を救う日に決闘の出来事が重なっていた問題を修正しました。'),
 '인질 구출전을 대화로 끝내도 구출한 것으로 칩니다.': ('Ending a hostage rescue through talk now counts as a rescue.', '人質救出戦を対話で終えても、救出したものとみなします。'),
 '교회 의뢰를 받은 뒤 사도 마스터를 암살로 처리해도 보상을 받습니다.': ("After accepting the Church's request, you now receive the reward even if you deal with the Apostle Master by assassination.", '教会の依頼を受けた後、使徒のマスターを暗殺で片付けても報酬を受け取れます。'),
 '우정 3단계의 이름이 「죽마고우」에서 「지기」로 바뀝니다.': ('Friendship stage 3 has been renamed to 「Sworn Friends」.', '友情3段階の名前が「無二の友」に変わります。'),
 '성유물을 다시 뽑던 문제를 수정했습니다.': ('Fixed an issue where the relic was drawn again.', '聖遺物を引き直していた問題を修正しました。'),
 '선택 창이 뜬 직후 0.3초 동안은 터치를 받지 않아, 실수로 선택지를 누르는 일을 막습니다.': ('Choice windows now ignore touches for 0.3 seconds after appearing, to prevent accidental taps.', '選択ウィンドウが出た直後の0.3秒はタッチを受け付けず、誤って選択肢を押すのを防ぎます。'),
 '전투 중 대화로 이미 동맹을 맺은 조가 사건으로 다시 동맹을 제안하던 문제를 수정했습니다.': ('Fixed an issue where a team you had already allied with through talk in battle would propose an alliance again in an event.', '戦闘中の対話ですでに同盟を結んだ組が、出来事で再び同盟を持ちかけてきた問題を修正しました。'),
 '랭크가 한 단계 내려갈 때 +가 그대로 남습니다. (예: A+ → B+)': ('When a rank drops by one step, the + now remains. (e.g. A+ → B+)', 'ランクが一段階下がるとき、＋がそのまま残ります。（例：A+ → B+）'),
}
def js(x): return json.dumps(x, ensure_ascii=False)
def item(it):
    if isinstance(it, tuple): return '[' + js(it[0]) + ',[' + ','.join(js(x) for x in it[1]) + ']]'
    return js(it)
ENTRY = " {v:" + js(V) + ",n:'" + N + "',t:" + js(T) + ",g:[" + ','.join('[' + js(h) + ', [' + ', '.join(item(i) for i in its) + ']]' for h, its in G) + "]},"
def walk():
    yield T
    for h, its in G:
        yield h
        for i in its:
            if isinstance(i, tuple): yield i[0]; yield from i[1]
            else: yield i
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    if ('{v:"' + V + '",n:\'' + N + "'") in s: print('pn117 already'); continue
    o = 'const PATCH=[\n'
    if s.count(o) != 1: miss.append(('PATCH', s.count(o)))
    else: s = s.replace(o, o + ENTRY + '\n', 1)
    lack = [k for k in walk() if k not in TR]
    if lack: miss.append(('tr', lack))
    s, nd, nt = i18n.add(s, [(k, TR[k][0], TR[k][1]) for k in walk() if k in TR])
    print('pn117 miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
