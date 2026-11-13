"""11-13: 에필로그 사건 거르기
- 검은 성배 전용 「cx_j1~5」(감독관의 은퇴 · 검은 성배 논문 · 일기 · 그림자 기록 · 진흙)가 비스트 생에 나오던 것을 막는다
- 키아라에게 진 생(단꿈 · A안: 대부분 잠들고 일부만 깨어나며, 도시 밖 세상은 그대로)에서
  도시가 평소처럼 굴러가는 걸 전제로 한 일반 사건을 뺀다
- 「그 뒤의 길」 일상 갈래 문장을 단꿈 생에서는 빈 지하철로
사용: python3 epi1113_apply.py <game.html>"""
import sys, json, i18n
DREAM_NO = ['other_master', 'lookalike', 'redevelop', 'memorial', 'overseer', 'marked_child', 'judge_eye', 'ward_house', 'host_saved', 'friend_key']
SUB = ('반쯤 빈 출근길 지하철에서, 그 겨울이 꿈이었던 것처럼 느껴지는 아침이 늘어 갔다.',
       'On the half-empty subway to work, there were more and more mornings when that winter felt like a dream.',
       '半分空いた通勤の地下鉄で、あの冬が夢だったように感じる朝が増えていった。')
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("  const epiUsed=id=>((S.epi||{}).used||[]).includes(id);",
       "  const epiUsed=id=>((S.epi||{}).used||[]).includes(id);\n"
       "  // 11-13: 검은 성배 전용 사건은 비스트 생에서 빼고, 단꿈의 생에서는 도시가 평소처럼 굴러가는 사건을 뺀다\n"
       "  const EPI_DREAM_NO=" + json.dumps(DREAM_NO) + ";\n"
       "  const epiBlock=id=>(/^cx_j\\d$/.test(id)&&((S.war||{}).crisis||{}).type==='beast3R')||(!!S.flags.bxDream&&EPI_DREAM_NO.includes(id));")
    rp("&&x.c()); if(c.length){ sc=wpick", "&&x.c()&&!epiBlock(x.id)); if(c.length){ sc=wpick")
    rp("&&!E.used.includes(x.id)&&x.c()).map(x=>({x,w:x.w||1,rel:0}))", "&&!E.used.includes(x.id)&&x.c()&&!epiBlock(x.id)).map(x=>({x,w:x.w||1,rel:0}))")
    rp("return '출근길 지하철에서, 그 겨울이 꿈이었던 것처럼 느껴지는 아침이 늘어 갔다.'",
       "return S.flags.bxDream?" + json.dumps(SUB[0], ensure_ascii=False) + ":'출근길 지하철에서, 그 겨울이 꿈이었던 것처럼 느껴지는 아침이 늘어 갔다.'")
    s, nd, nt = i18n.add(s, [SUB])
    print('epi1113 miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
