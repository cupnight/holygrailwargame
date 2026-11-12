"""비스트 Ⅲ/R 연출 (11-12): ① 7일차 봉인 · 빈 자리 ② 강림 + 고쳐쓴 카르마 ③ 키아라 입장 ④ 단독현현 ⑤ 결말 · 달로 간 잔(네 갈래) ⑥ 결말 · 단꿈
검은 성배 연출을 빌려 쓰던 자리를 비스트 전용으로 바꾼다. 화면 코드는 bxfx.js · bxfx_end.js. 사용: python3 bxfx_apply.py <game.html>"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n
HERE = os.path.dirname(os.path.abspath(__file__)); SND = os.path.join(HERE, '..', 'public', 'assets', 'sound')
TR, TT = [], []
def k(ko, en, ja): (TT if '{' in ko else TR).append((ko, en, ja))
k('제{0}일 · 봉인', 'Day {0} · Sealed', '{0}日目 · 封印')
k('제{0}일 · 빈 자리', 'Day {0} · An Empty Place', '{0}日目 · 空いた場所')
k('제{0}일 · 강림', 'Day {0} · Descent', '{0}日目 · 降臨')
k('누군가 성배를 통째로 봉인했다', 'Someone sealed the Grail away entirely', '何者かが聖杯を丸ごと封印した')
k('성배가 있던 자리가 텅 비어 있었다', 'The place where the Grail stood was empty', '聖杯があった場所は空になっていた')
k('킷쇼인 키아라', 'Kissyoin Kiara', 'キッショウイン キアラ')
k('비스트 Ⅲ/R', 'Beast III/R', 'ビーストⅢ/R')
k('고쳐쓴 카르마', 'Rewritten Karma', '書き換えられたカルマ')
k('단독현현', 'Independent Manifestation', '単独顕現')
k('BB가 성배를 품에 안고 달로 돌아갔다.', 'BB took the Grail in her arms and returned to the moon.', 'BBは聖杯を胸に抱いて月へ帰っていった。')
k('BB가 남은 성배를 품에 안고 달로 데려갔다.', 'BB took the remaining Grail in her arms and carried it to the moon.', 'BBは残された聖杯を胸に抱き、月へ連れていった。')
k('성배는 달빛 속으로 가라앉듯 사라졌다.', 'The Grail vanished as if sinking into the moonlight.', '聖杯は月光の中へ沈むように消えた。')
k('흩어졌던 목소리가 성배를 달로 데려갔다.', 'A scattered voice carried the Grail away to the moon.', '散り散りになった声が、聖杯を月へ連れていった。')
k('성배는 빛 조각으로 풀려 달로 올라갔다.', 'The Grail came apart into shards of light and rose to the Moon.', '聖杯は光の欠片にほどけ、月へと昇っていった。')
k('달의 뒷면에서 · 긴급 방송', 'From the far side of the Moon · Emergency Broadcast', '月の裏側より · 緊急放送')
k('선배, 그럼 이만! 이건 제가 달에 잘 넣어 둘게요.', "Well then, Senpai, I'm off! I'll tuck this away safely on the Moon.", '先輩、それじゃあこれで！これは私が月にしっかりしまっておきますね。')
k('…고마웠어요. 이번엔 진심이에요.', '…Thank you. This time I mean it.', '…ありがとうございました。今度は本気ですよ。')
k('…배, 들려요…? 이건 제가…', "…pai, can you hear…? I'll take th…", '…輩、聞こえ…？ これは私が…')
k('{0} 전역에서 깊은 잠에 빠졌던 시민들 일제히 깨어나 · 밤사이 일을 기억하는 사람은 없어', 'Citizens across {0} who had fallen into deep sleep awaken all at once · no one remembers what happened overnight', '{0}全域で深い眠りに落ちていた市民が一斉に目覚める · 夜の間の出来事を覚えている者はいない')
k('아무도 소원을 빌지 않았다.', 'No one made a wish.', '誰も願いを口にしなかった。')
k('단꿈', 'Sweet Dream', '甘い夢')
k('그 겨울, 도시는 한 사람의 쾌락이 되었다.', 'That winter, the city became one person\'s pleasure.', 'その冬、街はひとりの快楽になった。')
k('당신만이 남겨졌다.', 'Only you were left behind.', 'あなただけが残された。')
k('{0} 전역 원인 모를 깊은 잠 확산 · 깨어나지 않는 시민 수십만 명 · 모두 웃는 얼굴로 잠들어',
  'Unexplained deep sleep spreads across {0} · hundreds of thousands of citizens will not wake · all sleeping with smiles',
  '{0}全域で原因不明の深い眠りが拡大 · 目覚めない市民は数十万人 · 全員が笑顔のまま眠る')

CSS = """
.bxd{position:absolute;left:0;right:0;bottom:12%;text-align:center;pointer-events:none;padding:0 16px}
.bxd-day{font-family:var(--f-mono);font-size:12px;letter-spacing:.4em;color:#ffb6d9;opacity:0}
.bxd-nm{position:relative;height:1.35em;margin-top:6px;font-family:var(--f-display);font-size:clamp(28px,7vw,46px);color:#fbe9f2;letter-spacing:.14em;text-shadow:0 0 3px #000,0 0 18px rgba(255,120,190,.55)}
.bxd-nm span{position:absolute;left:0;right:0;opacity:0;white-space:nowrap}
.bxd-cls{font-family:var(--f-story);font-size:clamp(14px,3vw,18px);color:#f3c6dd;letter-spacing:.3em;opacity:0;margin-top:4px;text-shadow:0 0 4px #000}
.bxd-km{margin-top:10px;font-family:var(--f-mono);font-size:13px;letter-spacing:.3em;color:#d6bcff;opacity:0;text-shadow:0 0 10px rgba(170,120,255,.8)}
.xd-d.long{letter-spacing:.08em;font-size:clamp(22px,5.2vw,34px)}
.xd-rule.bx{background:linear-gradient(90deg,transparent,rgba(190,140,255,.9),transparent)}
.xb-card.bx .xb-nm{text-shadow:0 0 22px rgba(255,120,190,.6)}
.xb-card.bx .xb-again{text-shadow:0 0 3px #000,0 0 10px #000,0 0 26px rgba(255,120,190,.75)}
.xb-card.bx .xb-cp span{border-color:rgba(255,150,200,.75)}
.xb-card.bx .xb-night{color:#ffb6d9}
.bxm-tv{position:absolute;left:50%;top:26%;transform:translate(-50%,0);display:flex;align-items:center;gap:10px;padding:7px 14px;border:1px solid rgba(190,140,255,.7);background:repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 3px),rgba(18,6,28,.82);font-family:var(--f-mono);font-size:clamp(11px,2.6vw,14px);letter-spacing:.12em;color:#efe2ff;opacity:0;pointer-events:none;white-space:nowrap;box-shadow:0 0 18px rgba(170,110,255,.45);max-width:calc(100vw - 32px);overflow:hidden}
.bxm-tv i{font-style:normal;color:#ff5a7a;letter-spacing:.08em}
.bxm-msg{position:absolute;left:0;right:0;top:calc(15% + 9vmin);text-align:center;pointer-events:none;padding:0 18px}
.bxm-msg p{margin:0;opacity:0;font-family:var(--f-story);color:#f3e6ff;text-shadow:0 0 3px #000,0 0 14px rgba(190,140,255,.75)}
.bxm-msg .a{font-size:clamp(14px,3.4vw,18px);min-height:1.4em}
.bxm-msg .b{margin-top:8px;font-size:clamp(12px,2.8vw,14px);color:#d9c6ef}
"""
SNDS = ['j_bx_seal', 'j_bx_empty', 'j_bx_desc', 'j_bx_karma', 'j_bx_in', 'j_bx_in_s', 'j_bx_brk', 'j_bx_brk_s', 'j_bx_p2', 'j_end_bxm_me', 'j_end_bxm_live', 'j_end_bxm_nobb', 'j_end_bxm_voice', 'j_end_bxdream']
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
    js = open(os.path.join(HERE, 'bxfx.js'), encoding='utf-8').read(); je = open(os.path.join(HERE, 'bxfx_end.js'), encoding='utf-8').read()
    # 화면: 새 연출 함수 · 결말 장면
    rp("/* ---- 서번트를 빼앗기는 연출:", js + "\n/* ---- 서번트를 빼앗기는 연출:")
    rp("  SCN.flood={HOLD:6.4", je + "  SCN.flood={HOLD:6.4")
    rp("const F={seal:sealFx,descent:descentFx,boss:bossFx,bossp2:bossP2Fx,defect:defectFx,end:endFx};", "const F={seal:sealFx,descent:descentFx,boss:bossFx,bossp2:bossP2Fx,defect:defectFx,end:endFx,bxseal:bxSealFx,bxdesc:bxDescFx};")
    rp("function bossFx(fx){ xfxGo(", "function bossFx(fx){ if(fx.kiara) return xfxGo(fx.full?['j_bx_in','j_bx_brk']:['j_bx_in_s','j_bx_brk_s'],()=>bxBossShow(fx)); xfxGo(")
    rp("function bossP2Fx(fx){ xfxGo(", "function bossP2Fx(fx){ if(fx.kiara) return xfxGo('j_bx_p2',()=>bxP2Show(fx)); xfxGo(")
    rp("const END_X={seal:'seal',", "const END_X={bxm_me:'bxmoon',bxm_live:'bxmoon',bxm_nobb:'bxmoon',bxm_voice:'bxmoon',bxdream:'bxdream',seal:'seal',")
    rp("const END_SK={dead:'j_end_dead',flood:'j_end_flood'};", "const END_SK={dead:'j_end_dead',flood:'j_end_flood',bxm_me:'j_end_bxm_me',bxm_live:'j_end_bxm_live',bxm_nobb:'j_end_bxm_nobb',bxm_voice:'j_end_bxm_voice',bxdream:'j_end_bxdream'};")
    rp(".xb-q2{margin-top:12px}", ".xb-q2{margin-top:12px}" + CSS.replace('\n', ''))
    # 소리 목록
    rp('"j_boss2":{"d":2.7}', '"j_boss2":{"d":2.7},' + ','.join(f'"{n}":{{"d":{dur(n)}}}' for n in SNDS))
    # 시뮬레이션: 비스트 생의 연출 자리
    rp("log('자정, 도시 한가운데서 성배의 기척이 한순간 끊겼다. 누군가 성배를 통째로 봉인했다.','war',{fx:{t:'descent',d:w.day,g:CX().grail}});",
       "log('자정, 도시 한가운데서 성배의 기척이 한순간 끊겼다. 누군가 성배를 통째로 봉인했다.','war',{fx:{t:'bxseal',d:w.day}});")
    rp("log('자정, 성배가 있던 자리가 텅 비어 있었다. 감독관은 성배가 아직 차지 않았으니 전쟁은 이어진다고만 알렸다.','notice');",
       "log('자정, 성배가 있던 자리가 텅 비어 있었다. 감독관은 성배가 아직 차지 않았으니 전쟁은 이어진다고만 알렸다.','notice',{fx:{t:'bxseal',nb:1,d:w.day}});")
    rp("남김없이 마셨다.`,'war',{fx:{t:'descent',d:w.day,g:CX().grail}});", "남김없이 마셨다.`,'war',{fx:{t:'bxdesc',d:w.day,g:bxSents().length,karma:!!c.karma,nb}});")
    rp("fx:{t:'bossp2',line:'아아, 이 아픔마저 이토록 달콤하다니요.'}", "fx:{t:'bossp2',kiara:1,line:'아아, 이 아픔마저 이토록 달콤하다니요.'}")
    rp("fx:{t:'boss',full:first||fin,", "fx:{t:'boss',kiara:w.crisis&&w.crisis.type==='beast3R'?1:0,full:first||fin,")
    rp("    const bbMe=S.hero==='bb'&&w.heroAlive, bbLive=!bbMe&&c.bb&&(c.bb.at==='moon'||c.bb.at==='npc')&&!!bxBBP();",
       "    const bbMe=S.hero==='bb'&&w.heroAlive, bbLive=!bbMe&&c.bb&&(c.bb.at==='moon'||c.bb.at==='npc')&&!!bxBBP();\n    S.flags.bxEndV=bbMe?'me':bbLive?'live':c.noBB?'nobb':'voice';")
    rp("    const k=f.cupSealed?'seal'", "    const k=f.bxEnd?'bxm_'+(f.bxEndV||'voice'):f.bxDream?'bxdream':f.cupSealed?'seal'")
    s, nd, nt = i18n.add(s, TR, TT)
    open(P, 'w', encoding='utf-8').write(s); print('bxfx', 'miss', miss, 'tr', nd, nt)
