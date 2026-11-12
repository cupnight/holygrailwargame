"""비스트 Ⅲ/R 연출 2차 (11-12): ⑦ KP 회수 ⑧ 멜트·립 해방 ⑨ 봉인이 갈라짐(고백 · 찢어짐 · 풀기) ⑩ 토벌령 ⑪ 키아라와의 보구 격돌.
화면 코드는 bxfx2.js. bxfx_apply.py 뒤에 쓴다. 사용: python3 bxfx2_apply.py <game.html>"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
HERE = os.path.dirname(os.path.abspath(__file__)); SND = os.path.join(HERE, '..', 'public', 'assets', 'sound')
TR, TT = [], []
def k(ko, en, ja): (TT if '{' in ko else TR).append((ko, en, ja))
k('키아라의 몸이 한 번 크게 일렁였다', "Kiara's body rippled once, violently", 'キアラの身体が一度大きく揺らいだ')
k('익숙하지 않은 단맛이 혀끝에 남았다', 'An unfamiliar sweetness lingered on the tip of your tongue', '慣れない甘さが舌先に残った')
k('이쪽을 보던 시선이 하나 끊겼다', 'One of the gazes watching you was severed', 'こちらを見ていた視線がひとつ途切れた')
k('카르마 파지 다섯 가운데 {0}', '{0} of the five Karma Phages', 'カルマファージ五つのうち{0}')
k('센티넬의 사슬이 끊어졌다', "The Sentinel's chains were broken", 'センチネルの鎖が断ち切られた')
k('제{0}일 · 봉인이 찢어지다', 'Day {0} · The Seal Tears', '{0}日目 · 封印が裂ける')
k('제{0}일 · 봉인을 풀다', 'Day {0} · Releasing the Seal', '{0}日目 · 封印を解く')
k('제{0}일 · 고백', 'Day {0} · Confession', '{0}日目 · 告白')
k('“…미안해요. 끝까지는 못 버텼어요.”', '“…I\'m sorry. I couldn\'t hold out to the end.”', '「…ごめんなさい。最後までは持ちこたえられませんでした」')
k('상자가 소리 없이 열렸다', 'The box opened without a sound', '箱は音もなく開いた')
k('“그 수녀가 키아라예요. 성배를 삼키려고 해요.”', '“That nun is Kiara. She\'s trying to swallow the Grail.”', '「あのシスターがキアラです。聖杯を呑み込もうとしているんです」')
k('감독관의 토벌령', "The Overseer's Subjugation Order", '監督役の討伐令')
k('성배를 가로챈 자', 'The one who seized the Grail', '聖杯を奪った者')
k('당신의 조', 'Your team', 'あなたの組')
k('그 체력을 무너뜨린 조에게 령주 한 획을 준다', 'The team that breaks its strength receives one Command Spell', 'その力を打ち崩した組に令呪一画を与える')
k('토벌', 'Subjugate', '討伐')

CSS = """
.bxkp-sl{display:flex;justify-content:center;gap:12px;margin-top:14px;opacity:0}
.bxkp-sl i{width:9px;height:9px;transform:rotate(45deg);border:1px solid rgba(255,170,215,.75)}
.bxkp-sl i.on{background:rgba(255,170,215,.85);box-shadow:0 0 8px rgba(255,120,190,.9)}
.bxkp-sl i.nw{animation:bxkpN .9s 3.45s ease-out both}
@keyframes bxkpN{0%{transform:rotate(45deg) scale(2.4);background:#fff;box-shadow:0 0 18px #fff}100%{transform:rotate(45deg) scale(1)}}
.bxo{position:absolute;left:50%;top:47%;transform:translate(-50%,-50%);width:min(340px,84vw);box-sizing:border-box;padding:22px 20px 30px;background:linear-gradient(#f2e9da,#e2d3b9);color:#2b1e16;text-align:center;font-family:var(--f-story);box-shadow:0 14px 44px rgba(0,0,0,.65);border:1px solid #b59d78;opacity:0;pointer-events:none}
.bxo::before{content:'';position:absolute;inset:6px;border:1px solid rgba(120,90,60,.45);pointer-events:none}
.bxo-h{font-family:var(--f-display);font-size:13px;letter-spacing:.3em;color:#6b4a2e;margin-bottom:12px}
.bxo-l{font-size:13px;color:#4a3626}
.bxo-t{font-family:var(--f-display);font-size:clamp(20px,5vw,26px);margin:4px 0 10px;color:#1e130c;letter-spacing:.05em;overflow-wrap:anywhere}
.bxo.me .bxo-t{color:#8e1522}
.bxo-s{font-size:12px;color:#5a4433;line-height:1.55;padding:0 40px 0 0}
.bxo-st{position:absolute;right:10px;bottom:6px;width:74px;height:74px;border-radius:50%;border:3px double #b3202a;color:#b3202a;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;font-family:var(--f-display);mix-blend-mode:multiply}
.bxo-st b{font-size:20px;line-height:1}
.bxo-st span{font-size:12px;letter-spacing:.15em;margin-top:2px}
.cfx.kx::before{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 74% 50%,rgba(255,110,185,.3),transparent 62%);animation:kxV var(--d) ease both}
@keyframes kxV{0%{opacity:0}18%{opacity:1}82%{opacity:1}100%{opacity:0}}
.cfx.kx .kx-lo{transform-box:fill-box;transform-origin:center;animation:kxB 1.1s cubic-bezier(.2,.8,.2,1) both}
.cfx.kx .kx-lo.w{animation:kxB 1.1s cubic-bezier(.2,.8,.2,1) both,kxW .9s 1.45s ease-in forwards}
.cfx.kx .kx-lo.l{animation:kxB 1.1s cubic-bezier(.2,.8,.2,1) both,kxL .8s 1.45s ease forwards}
.cfx.kx .kx-lo.o{animation:kxB 1.1s cubic-bezier(.2,.8,.2,1) both,kxO .6s 1.4s ease forwards}
@keyframes kxB{from{transform:scale(.15);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes kxW{to{transform:scale(3.4);opacity:0}}
@keyframes kxL{to{transform:scale(.55) rotate(-25deg);opacity:0;filter:grayscale(1) brightness(.6)}}
@keyframes kxO{to{transform:scale(1.35);opacity:0}}
.cfx.kx .kx-sp{transform-box:fill-box;transform-origin:center;animation:kxS 7s linear infinite}
.cfx.kx .kx-sp.r{animation-duration:14s;animation-direction:reverse}
@keyframes kxS{to{transform:rotate(360deg)}}
.cfx.kx .kx-pt{transform-box:fill-box;transform-origin:center;opacity:0;animation:kxP 1.3s calc(1.5s + var(--dl)) ease-out both}
@keyframes kxP{0%{opacity:0;transform:translate(0,0) rotate(0)}12%{opacity:1}100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(540deg)}}
"""
SNDS = ['j_bx_kp', 'j_bx_free', 'j_bx_conf', 'j_bx_tear', 'j_bx_open', 'j_bx_order', 'j_bx_np']
def dur(n):
    p = os.path.join(SND, n + '.mp3')
    try: return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()), 2)
    except Exception: return 5.0

for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        kk = s.count(o)
        if kk != c: miss.append((o[:70], kk)); return
        s = s.replace(o, n)
    js = open(os.path.join(HERE, 'bxfx2.js'), encoding='utf-8').read()
    rp("/* ---- 서번트를 빼앗기는 연출:", js + "\n/* ---- 서번트를 빼앗기는 연출:")
    rp("bxdesc:bxDescFx};", "bxdesc:bxDescFx,bxkp:bxKpFx,bxfree:bxFreeFx,bxconf:bxConfFx,bxorder:bxOrderFx};")
    rp(".xb-q2{margin-top:12px}", ".xb-q2{margin-top:12px}" + CSS.replace('\n', ''))
    rp('"j_boss2":{"d":2.7}', '"j_boss2":{"d":2.7},' + ','.join(f'"{n}":{{"d":{dur(n)}}}' for n in SNDS))
    # 시뮬레이션: 연출 자리
    rp("가슴께에서 빛 한 조각이 빠져나왔다. KP ${k?k.k:''}.`,'war');", "가슴께에서 빛 한 조각이 빠져나왔다. KP ${k?k.k:''}.`,'war',k?{fx:{t:'bxkp',k:k.k,n:c.kpGot||0}}:undefined);")
    rp("키아라의 몸이 한 번 크게 일렁였다.`,'war');", "키아라의 몸이 한 번 크게 일렁였다.`,'war',by==='me'&&k?{fx:{t:'bxkp',k:k.k,n:c.kpGot||0,g:1}}:undefined);")
    rp("같이 갈게요.”','voice'); }", "같이 갈게요.”','voice',(by==='me'||w.battle)?{fx:{t:'bxfree',h:u.hero}}:undefined); }")
    rp("열세 번째 밤이 지나자, 도시 한가운데의 상자가 안쪽에서 찢어졌다.','war');", "열세 번째 밤이 지나자, 도시 한가운데의 상자가 안쪽에서 찢어졌다.','war',{fx:{t:'bxconf',v:'force',d:w.day}});")
    rp("봉인을 풀었다. 도시 한가운데의 상자가 소리 없이 열렸다.`,'war');", "봉인을 풀었다. 도시 한가운데의 상자가 소리 없이 열렸다.`,'war',{fx:{t:'bxconf',v:'unseal',d:w.day}});")
    rp("성배를 삼키려고 해요.”`,'voice');", "성배를 삼키려고 해요.”`,'voice',{fx:{t:'bxconf',v:'conf',d:w.day}});")
    rp("그 체력을 무너뜨린 조에게 령주 한 획을 준다.`,'notice');", "그 체력을 무너뜨린 조에게 령주 한 획을 준다.`,'notice',{fx:{t:'bxorder',tgt:at==='me'?'':tgt,me:at==='me'?1:0}});")
    rp("const fx={t:'clash',res,me:fM,en:fE,", "const fx={t:'clash',kx:e.bx?1:0,res,me:fM,en:fE,")
    s, nd, nt = i18n.add(s, TR, TT)
    open(P, 'w', encoding='utf-8').write(s); print('bxfx2', 'miss', miss, 'tr', nd, nt)
