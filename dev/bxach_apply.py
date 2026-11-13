"""비스트 Ⅲ/R 위기 업적 17개 (11-13). 기록이 없던 것은 새로 남긴다.
덤: 검은 성배 업적 「홀로 선 성배 앞」 · 「그림자 사냥꾼」이 키아라 · 센티넬로도 풀리던 것을 막는다.
사용: python3 bxach_apply.py <game.html>"""
import sys, i18n
A = [  # id, 분류, 이름, 설명, 판정, 영어 이름, 영어 설명, 일본어 이름, 일본어 설명
 ('bxwinter','성배전쟁의 끝','단꿈의 겨울','키아라가 강림한 성배전쟁을 겪었다',"!!bxAC()&&bxAC().stage>=3",
  'Winter of Sweet Dreams','Lived through a Holy Grail War in which Kiara descended','甘い夢の冬','キアラが降臨した聖杯戦争を経験した'),
 ('bxname','성배전쟁의 끝','이름을 캐낸 자','키아라가 강림하기 전에 수녀의 이름을 알아냈다',"!!bxAC()&&!!bxAC().nunEarly",
  'The One Who Dug Up a Name','Learned the nun\'s name before Kiara descended','名を掘り当てた者','キアラが降臨する前に修道女の名を突き止めた'),
 ('bxother','성배전쟁의 끝','남이 끝낸 겨울','다른 조가 키아라를 쓰러뜨린 겨울을 살아남았다',"S.flags.bxEnd==='npc'&&!S.dead",
  'A Winter Ended by Others','Survived a winter in which another team defeated Kiara','他人が終わらせた冬','他の組がキアラを倒した冬を生き延びた'),
 ('bxconf','성배전쟁의 끝','달의 고백','직접 BB를 몰아붙여 진실을 들었다',"!!bxAC()&&bxAC().revealHow==='me'",
  'Confession from the Moon','Cornered BB yourself and heard the truth','月の告白','自らBBを追い詰め、真実を聞いた'),
 ('bxdoor','성배전쟁의 끝','문을 연 날','BB의 마스터로 봉인을 풀게 하고, 그 결전에서 키아라를 쓰러뜨렸다',"!!bxAC()&&bxAC().revealHow==='unseal'&&S.flags.bxEnd==='me'",
  'The Day the Door Opened','As BB\'s Master, had her break the seal and defeated Kiara in that final battle','扉を開いた日','BBのマスターとして封印を解かせ、その決戦でキアラを倒した'),
 ('bxvillain','성배전쟁의 끝','악역의 편','BB의 마스터로 토벌령을 받고, 쳐들어온 조를 막아 냈다',"!!bxAC()&&(bxAC().bbHeld||0)>=1",
  'On the Villain\'s Side','As BB\'s Master under a subjugation order, held off a team that came for you','悪役の味方','BBのマスターとして討伐令を受け、攻め込んできた組を退けた'),
 ('bxfirst','성배전쟁의 끝','첫 조각','센티넬을 처음 쓰러뜨려 카르마 파지를 거두었다',"!!bxAC()&&(bxAC().shadowKills||0)>=1",
  'The First Fragment','Defeated a Sentinel for the first time and recovered a Karma Phage','最初のかけら','初めてセンチネルを倒し、カルマファージを回収した'),
 ('bxfreed','성배전쟁의 끝','풀려난 아이들','한 전쟁에서 멜트릴리스와 패션립을 모두 풀어 주었다',"['meltryllis','passionlip'].every(h=>(S.flags.egoFreed||[]).includes(h))",
  'The Freed Children','Freed both Meltryllis and Passionlip in a single war','解き放たれた子たち','一つの戦争でメルトリリスとパッションリップの両方を解放した'),
 ('bxguard','성배전쟁의 끝','호위를 걷어 내다','호위 센티넬을 모두 걷어 내고 키아라를 쓰러뜨렸다',"!!bxAC()&&!!bxAC().guardAll&&S.flags.bxEnd==='me'",
  'Clearing the Guard','Defeated Kiara after every Sentinel guarding her had fallen','護衛を払いのけて','護衛のセンチネルをすべて退け、キアラを倒した'),
 ('bxbare','성배전쟁의 끝','다섯 감각 그대로','카르마 파지를 하나도 거두지 못한 채 키아라를 쓰러뜨렸다',"!!bxAC()&&S.flags.bxEnd==='me'&&!(bxAC().kpGot||0)",
  'All Five Senses Intact','Defeated Kiara without a single Karma Phage recovered','五感そのままに','カルマファージを一つも回収しないままキアラを倒した'),
 ('bxsolo','성배전쟁의 끝','홀로 맞선 짐승','함께 싸우는 조 없이 키아라를 쓰러뜨렸다',"!!bxAC()&&!!bxAC().soloBoss&&S.flags.bxEnd==='me'",
  'Alone Against the Beast','Defeated Kiara without any allied team fighting alongside','独り挑んだ獣','共に戦う組なしでキアラを倒した'),
 ('bx13','성배전쟁의 끝','열사흘째 밤','13일째에 봉인이 억지로 깨진 뒤 키아라를 쓰러뜨렸다',"!!bxAC()&&bxAC().revealHow==='force'&&S.flags.bxEnd==='me'",
  'The Thirteenth Night','Defeated Kiara after the seal was forced open on the 13th day','十三日目の夜','十三日目に封印が無理やり破られた後、キアラを倒した'),
 ('bxnobb','성배전쟁의 끝','차오른 잔','BB가 없는 성배전쟁에서 키아라를 쓰러뜨렸다',"!!bxAC()&&!!bxAC().noBB&&S.flags.bxEnd==='me'",
  'The Brimming Cup','Defeated Kiara in a Holy Grail War without BB','満ちた杯','BBのいない聖杯戦争でキアラを倒した'),
 ('bxkama','서번트와 나','같은 이름의 짐승','카마와 함께 키아라를 쓰러뜨렸다',"S.flags.bxEnd==='me'&&S.hero==='kama'",
  'A Beast of the Same Name','Defeated Kiara together with Kama','同じ名の獣','カーマと共にキアラを倒した'),
 ('bxego','서번트와 나','떨어져 나온 아이','멜트릴리스나 패션립을 서번트로 데리고 키아라를 쓰러뜨렸다',"S.flags.bxEnd==='me'&&['meltryllis','passionlip'].includes(S.hero)",
  'The Child Who Broke Away','Defeated Kiara with Meltryllis or Passionlip as your Servant','切り離された子','メルトリリスかパッションリップをサーヴァントとしてキアラを倒した'),
 ('bxsweet','삶','뿌리친 단맛','그 겨울의 단꿈이 세 번 찾아왔고, 세 번 모두 뿌리쳤다',"!!S.flags.bxFree",
  'Sweetness Refused','The sweet dream of that winter came three times, and you refused it all three times','振り払った甘さ','あの冬の甘い夢が三度訪れ、三度とも振り払った'),
 ('bxmoonnews','삶','달에서 온 소식','달로 간 BB에게서 소식이 왔다',"!!S.flags.bxMoon",
  'News from the Moon','Received word from BB, who went to the Moon','月からの便り','月へ行ったBBから便りが届いた'),
]
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    # 기록: 반전 전에 이름을 알아냈다
    rp("if((t.intel||0)>=70){ c.nunKnown=1;", "if((t.intel||0)>=70){ c.nunKnown=1; if((c.stage||0)<3) c.nunEarly=1;")
    # 기록: 내가 이긴 결전 끝에 호위가 모두 쓰러져 있었다
    rp("S.flags.bxEnd=c.bossDown==='me'?'me':'npc';",
       "{ const G=(c.units||[]).filter(u=>u.cx==='sent'&&u.guard); c.guardAll=G.length>0&&G.every(u=>!u.alive)?1:0; }\n    S.flags.bxEnd=c.bossDown==='me'?'me':'npc';")
    # 기록: 봉인 중, BB의 마스터로 쳐들어온 조를 막아 냈다
    rp("    if(b&&b.ctx.defend&&!b.ctx.claim&&w.heroAlive&&b.e&&b.e.alive) b.e.fortRead",
       "    if(b&&w.heroAlive&&b.ctx.defend&&b.e&&!b.e.cx&&['win','fled','asn','talk'].includes(b.res)){ const c=w.crisis; if(c&&c.type==='beast3R'&&c.stage===2&&c.bb&&c.bb.at==='me') c.bbHeld=(c.bbHeld||0)+1; }\n"
       "    if(b&&b.ctx.defend&&!b.ctx.claim&&w.heroAlive&&b.e&&b.e.alive) b.e.fortRead")
    # 기록: 달의 소식을 받았다
    rp("{t:'달을 올려다본다',auto:true,f:()=>{ add({will:2});", "{t:'달을 올려다본다',auto:true,f:()=>{ S.flags.bxMoon=1; add({will:2});")
    # 검은 성배 업적이 비스트 위기로 풀리지 않게
    rp("t:()=>!!(WV().crisis&&WV().crisis.soloBoss)}", "t:()=>!!(WV().crisis&&WV().crisis.soloBoss&&WV().crisis.type!=='beast3R')}")
    rp("t:()=>((WV().crisis||{}).shadowKills||0)>=2}", "t:()=>(WV().crisis||{}).type!=='beast3R'&&((WV().crisis||{}).shadowKills||0)>=2}")
    # 업적 목록
    anchor = "{id:'bxfive',cat:'성배전쟁의 끝',n:'다섯 조각',d:'카르마 파지 다섯을 모두 거두었다',t:()=>!!WV().crisis&&WV().crisis.type==='beast3R'&&(WV().crisis.kpGot||0)>=5},"
    new = anchor + "\n" + "\n".join(f"    {{id:'{a[0]}',cat:'{a[1]}',n:'{a[2]}',d:'{a[3]}',t:()=>{a[4]}}}," for a in A)
    rp(anchor, new)
    rp("  const ACH=[", "  const bxAC=()=>{ const c=WV().crisis; return c&&c.type==='beast3R'?c:null; }; // 비스트 위기 업적이 보는 위기 기록\n  const ACH=[")
    s, nd, nt = i18n.add(s, [(a[2], a[5], a[7]) for a in A] + [(a[3], a[6], a[8]) for a in A])
    print('bxach miss', miss, 'tr', nd)
    open(P, 'w', encoding='utf-8').write(s)
