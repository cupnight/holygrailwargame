"""11-14: 키아라를 쓰러뜨린 뒤 「새벽의 작별」 — 결말 연출(달로 간 잔)이 끝난 뒤 내 서번트와 헤어지는 장면
- 내가 쓰러뜨렸든 다른 조가 쓰러뜨렸든, 내 서번트가 살아 있으면(아르스 노바 · 스스로 떠난 경우 제외)
- 결말 연출 앞에 지나가던 작별 두 줄은 이 장면 안으로 옮긴다
- 대사는 서번트마다 있는 기존 작별 대사(bye). 화면에서는 초상화 + 대사로 보인다
- 결과 창의 '닫기'를 누르면: 금빛 테두리가 1.5초×2 차오른 뒤, 대화창이 오른쪽 아래부터 잘게 부서진 빛이 되어
  바람에 실려 왼쪽 위로 날아간다(시안 「새벽의 작별 연출」 7판 · 전체 0.5배 속도). 누르면 넘어간다
사용: python3 bxbye_apply.py <game.html>"""
import sys, json, i18n
D, T = [], []
def d_(ko, en, ja): D.append((ko, en, ja)); return ko
def t_(ko, en, ja): T.append((ko, en, ja)); return ko
TITLE = d_('새벽의 작별', 'Farewell at Dawn', '夜明けの別れ')
B0 = t_('성배가 달로 올라간 뒤, 도시 위로 첫 햇살이 번졌다. {0}의 발끝부터 빛으로 풀려 가고 있었다. 붙잡아 둘 성배는 이제 이 세계에 없다.',
        "After the Grail rose to the moon, the first light of dawn spread over the city. {0} was coming undone into light, starting from the toes. There is no Grail left in this world to hold them here.",
        '聖杯が月へ昇ったあと、街の上に最初の朝日が広がった。{0}の足先から光となってほどけていく。引き留める聖杯は、もうこの世界にない。')
DEEP = d_('그 겨울 내내 곁에 있던 온기가, 손끝에서부터 옅어지고 있었다.', 'The warmth that had stayed by your side all winter was fading, starting from the fingertips.', 'あの冬のあいだずっとそばにあったぬくもりが、指先から薄れていく。')
BBB = d_('성배를 품에 안은 BB가 떠나기 직전, 한 번 뒤를 돌아보았다. “선배, 마지막으로 할 말 있으면 지금이에요. 달은 꽤 멀거든요.”',
         'Just before leaving with the Grail in her arms, BB looked back once. “Senpai, if you have anything to say, now’s the time. The moon is pretty far, you know.”',
         '聖杯を抱いたBBは、去る直前に一度だけ振り返った。「センパイ、最後に言いたいことがあるなら今ですよ。月って結構遠いんですから」')
D.append(('“선배, 마지막으로 할 말 있으면 지금이에요. 달은 꽤 멀거든요.”', '“Senpai, if you have anything to say, now’s the time. The moon is pretty far, you know.”', '「センパイ、最後に言いたいことがあるなら今ですよ。月って結構遠いんですから」'))
D.append(('성배를 품에 안은 BB가 떠나기 직전, 한 번 뒤를 돌아보았다.', 'Just before leaving with the Grail in her arms, BB looked back once.', '聖杯を抱いたBBは、去る直前に一度だけ振り返った。'))
C1 = d_('고맙다고 말한다', 'Say thank you', 'ありがとうと伝える')
C2 = d_('말없이 손을 잡는다', 'Take their hand without a word', '黙って手を取る')
C3 = d_('다시 만나자고 한다', 'Ask to meet again', 'また会おうと言う')
for c in (C1, C2, C3): D.append(('→ ' + c, '→ ' + dict(((C1, 'Say thank you'), (C2, 'Take their hand without a word'), (C3, 'Ask to meet again')))[c], '→ ' + dict(((C1, 'ありがとうと伝える'), (C2, '黙って手を取る'), (C3, 'また会おうと言う')))[c]))
R1 = t_('{0~은} 그 말을 끝까지 듣고 나서야, 조용히 웃었다.', '{0} listened to the very end before smiling quietly.', '{0}はその言葉を最後まで聞いてから、静かに微笑んだ。')
R2 = d_('손끝이 먼저 빛이 되었다. 당신은 마지막까지 손을 놓지 않았다.', 'The fingertips turned to light first. You did not let go until the very end.', '指先が先に光になった。あなたは最後まで手を離さなかった。')
R3a = t_('{0~은} 대답 대신 웃었다. 그 웃음이 약속처럼 남았다.', '{0} smiled instead of answering. That smile remained like a promise.', '{0}は答える代わりに笑った。その笑顔が約束のように残った。')
R3b = t_('{0~은} 잠깐 망설이다 고개를 끄덕였다.', '{0} hesitated for a moment, then nodded.', '{0}は少しためらってから頷いた。')
END = t_('{0~은} 새벽빛 속으로 흩어졌다.', '{0} scattered into the light of dawn.', '{0}は夜明けの光の中へ散っていった。')
# 두 줄짜리 결과는 줄을 나눠 옮기지 못하는 경우가 있어(쉼표가 든 틀) 통째 틀도 둔다
for a, b in ((R1, END), (R3a, END), (R3b, END)):
    ea, eb = [x for x in T if x[0] == a][0], [x for x in T if x[0] == b][0]
    T.append((a + '\n' + b, ea[1] + '\n' + eb[1], ea[2] + '\n' + eb[2]))
eb0 = [x for x in T if x[0] == B0][0]; ed = [x for x in D if x[0] == DEEP][0]
T.append((B0 + '\n' + DEEP, eb0[1] + '\n' + ed[1], eb0[2] + '\n' + ed[2]))
# 11-14 A안: 다른 조가 키아라를 쓰러뜨린 결말은 그 사실부터 짚는다
BN = t_('다른 조가 키아라를 쓰러뜨렸다는 통지가 돌았다. 성배는 달로 갔고, 우리의 겨울은 그렇게 끝났다. {0}의 발끝부터 빛으로 풀려 가고 있었다. 붙잡아 둘 성배는 이제 이 세계에 없다.',
        "Word came that another team had brought Kiara down. The Grail went to the moon, and our winter ended just like that. {0} was coming undone into light, starting from the toes. There is no Grail left in this world to hold them here.",
        '別の組がキアラを倒したという通知が回った。聖杯は月へ行き、私たちの冬はそうして終わった。{0}の足先から光となってほどけていく。引き留める聖杯は、もうこの世界にない。')
ebn = [x for x in T if x[0] == BN][0]
T.append((BN + '\n' + DEEP, ebn[1] + '\n' + ed[1], ebn[2] + '\n' + ed[2]))

# 11-14: 내 서번트가 멜트릴리스 · 패션립일 때 — 키아라에게서 떨어져 나온 아이들의 작별
EGO = {
 'meltryllis': {
  'me': [('키아라가 녹아 사라진 하늘을 멜트릴리스가 한참 올려다보았다. 발끝부터 빛으로 풀려 가는데도, 멜트릴리스의 걸음은 끝까지 춤추는 사람의 것이었다.',
          "Meltryllis gazed up for a long while at the sky where Kiara had melted away. Even as she came undone into light from the toes, Meltryllis's steps remained those of a dancer to the very end.",
          'キアラが溶けて消えた空を、メルトリリスは長いあいだ見上げていた。足先から光になってほどけていくのに、メルトリリスの足取りは最後まで踊る者のそれだった。'),
         ('…빚은 갚았어. 이제 남은 건 너뿐이네.', "…I've paid my debt. Now all that's left is you.", '……借りは返したわ。あとはあなただけね。')],
  'npc': [('다른 조가 키아라를 쓰러뜨렸다는 통지가 돌았다. 멜트릴리스는 그 하늘을 한참 올려다보았다. 발끝부터 빛으로 풀려 가는데도, 멜트릴리스는 고개를 들고 있었다.',
           'Word came that another team had brought Kiara down. Meltryllis gazed up at that sky for a long while. Even as she came undone into light from the toes, Meltryllis kept her head held high.',
           '別の組がキアラを倒したという通知が回った。メルトリリスはその空を長いあいだ見上げていた。足先から光になってほどけていくのに、メルトリリスは顔を上げたままだった。'),
          ('…내 손으로 갚고 싶었는데. 뭐, 됐어.', "…I wanted to pay her back with my own hands. Well, whatever.", '……この手で返したかったのに。まあ、いいわ。')]},
 'passionlip': {
  'me': [('키아라가 사라진 자리를 패션립이 두 손을 꼭 모은 채 바라보았다. 그 손끝부터 빛으로 풀려 가는 것을 보며, 패션립이 작게 웃었다.',
          'Passionlip looked at the place where Kiara had vanished, her hands clasped tight. Watching those fingertips come undone into light, Passionlip gave a small smile.',
          'キアラが消えた場所を、パッションリップは両手をぎゅっと合わせたまま見つめていた。その指先から光になってほどけていくのを見ながら、パッションリップは小さく笑った。'),
         ('…이제 아무도 저를 묶지 않아요. 그러니까, 마지막은 제가 고를래요.', "…No one binds me anymore. So I'll choose how this ends.", '……もう誰もわたしを縛りません。だから、最後はわたしが選びます。')],
  'npc': [('다른 조가 키아라를 쓰러뜨렸다는 통지가 돌았다. 한참 그 하늘을 바라보던 패션립이 두 손을 꼭 모았다. 그 손끝부터 빛으로 풀려 가는 것을 보며, 패션립이 조그맣게 말했다.',
           'Word came that another team had brought Kiara down. Passionlip, who had been gazing at that sky for a long while, clasped her hands tight. Watching those fingertips come undone into light, Passionlip spoke softly.',
           '別の組がキアラを倒したという通知が回った。長いあいだその空を見つめていたパッションリップが、両手をぎゅっと合わせた。その指先から光になってほどけていくのを見ながら、パッションリップは小さく言った。'),
          ('…끝났네요. 정말로.', "…It's over. Really over.", '……終わったんですね。本当に。')]}}
for h in EGO.values():
    for k, (nar, q) in h.items():
        D.append(nar); D.append(q); D.append(('“' + q[0] + '”', '“' + q[1] + '”', '「' + q[2].rstrip('。') + '」'))
EGOJS = {h: {k: v[0][0] + ' “' + v[1][0] + '”' for k, v in d.items()} for h, d in EGO.items()}
js = lambda x: json.dumps(x, ensure_ascii=False)
SIM = ("  // 11-14: 「새벽의 작별」 — 키아라를 쓰러뜨린 뒤, 결말 연출이 끝나고 에필로그 첫 장면 전에\n"
       "  function bxBye(){ const w=W(), h=hero(); if(!h) return; const r=relOf(), deep=!!(r&&r.stage>=3), nm=h.name;\n"
       "    const EGO=" + js(EGOJS) + ", eg=EGO[S.hero];\n    const body=S.hero==='bb'?" + js(BBB) + ":eg?[eg[S.flags.bxEnd==='npc'?'npc':'me'],deep?" + js(DEEP) + ":''].filter(Boolean).join('\\n'):[S.flags.bxEnd==='npc'?`다른 조가 키아라를 쓰러뜨렸다는 통지가 돌았다. 성배는 달로 갔고, 우리의 겨울은 그렇게 끝났다. ${nm}의 발끝부터 빛으로 풀려 가고 있었다. 붙잡아 둘 성배는 이제 이 세계에 없다.`:`성배가 달로 올라간 뒤, 도시 위로 첫 햇살이 번졌다. ${nm}의 발끝부터 빛으로 풀려 가고 있었다. 붙잡아 둘 성배는 이제 이 세계에 없다.`,deep?" + js(DEEP) + ":''].filter(Boolean).join('\\n');\n"
       "    const end=`${nm}${J(nm,은)} 새벽빛 속으로 흩어졌다.`;\n"
       "    const res=(t,txt)=>{ decide({title:" + js(TITLE) + ",body:'→ '+t+'\\n'+txt,silent:true,byeFx:1,choices:[{t:'닫기',auto:true,f:()=>null}]}); return txt; };\n"
       "    decide({title:" + js(TITLE) + ",body,choices:[\n"
       "      {t:" + js(C1) + ",auto:true,f:()=>{ add({bond:4}); return res(" + js(C1) + ",[sayV(h,'bye'),`${nm}${J(nm,은)} 그 말을 끝까지 듣고 나서야, 조용히 웃었다.`,end].filter(Boolean).join('\\n')); }},\n"
       "      {t:" + js(C2) + ",f:()=>{ add({will:4}); return res(" + js(C2) + "," + js(R2) + "+'\\n'+end); }},\n"
       "      {t:" + js(C3) + ",f:()=>{ add({bond:2,will:2}); return res(" + js(C3) + ",((w.trust||0)>=60?`${nm}${J(nm,은)} 대답 대신 웃었다. 그 웃음이 약속처럼 남았다.`:`${nm}${J(nm,은)} 잠깐 망설이다 고개를 끄덕였다.`)+'\\n'+end); }}]}); }\n")
UI = r"""// 11-14: 「새벽의 작별」 결과 창의 '닫기' — 금빛 테두리가 차오른 뒤 대화창이 빛 알갱이로 풀려 바람에 날아간다 (누르면 넘어감)
let BYE_RUN=false;
function byeGate(i){ const d=Sim.S&&Sim.S.pending; if(!d||!d.byeFx||d._fxGo) return false; d._fxGo=1;
  if(fxQuiet()) return false;
  const sh=$('#sheet'); if(!sh||BYE_RUN) return false; BYE_RUN=true; try{ Sim.setHold(true); }catch(e){}
  const SL=2, CELL=4, T0=1.5*SL, TD=1.6*SL, TEND=TD+T0+2.2*SL;
  const r=sh.getBoundingClientRect(), cols=Math.ceil(r.width/CELL), rows=Math.ceil(r.height/CELL);
  const ov=document.createElement('div'); ov.className='byefx'; ov.innerHTML='<canvas aria-hidden="true"></canvas><i class="bf-ring"></i>'; document.body.appendChild(ov);
  const cv=ov.querySelector('canvas'), cx=cv.getContext('2d'), ring=ov.querySelector('.bf-ring'); let D=1;
  const fit=()=>{ D=Math.min(2,devicePixelRatio||1); cv.width=innerWidth*D; cv.height=innerHeight*D; }; fit();
  Object.assign(ring.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',borderRadius:getComputedStyle(sh).borderRadius});
  const mk=document.createElement('canvas'); mk.width=cols; mk.height=rows; const mc=mk.getContext('2d');
  const K=[]; for(let y=0;y<rows;y++) for(let x=0;x<cols;x++) K.push({x,y,k:(1-(x/cols*.5+y/rows*.5))*.78+Math.random()*.22,gone:false});
  K.sort((a,b)=>a.k-b.k);
  const gust=t=>1+.55*Math.sin(t*1.25)+.3*Math.sin(t*3.3+1.2);
  let P=[], t=0, last=performance.now(), idx=0, done=false;
  const dl=$('#dlg'); const clean=()=>{ for(const k of ['filter','webkitMaskImage','maskImage','webkitMaskSize','maskSize','visibility']) sh.style[k]=''; dl.style.background=''; };
  const fin=()=>{ if(done) return; done=true; $('#dlg').classList.add('hidden'); clean(); ov.remove(); BYE_RUN=false; try{ Sim.setHold(false); }catch(e){} choose(i); };
  ov.addEventListener('pointerdown',fin);
  function frame(now){ if(done) return; const dt=Math.min(.05,(now-last)/1000); last=now; t+=dt;
    const glow=Math.min(1,t/T0); sh.style.filter=`brightness(${1+.35*glow}) saturate(${1+.2*glow})`;
    ring.style.opacity=(glow*(t>T0?Math.max(0,1-(t-T0)/(TD*.6)):1)).toFixed(3);
    if(t>T0){ const f=Math.min(1,(t-T0)/TD), want=Math.floor(K.length*(f*f*(3-2*f)));
      while(idx<want){ const c=K[idx++]; c.gone=true;
        if(Math.random()<.24) P.push({x:r.left+(c.x+.5)*CELL,y:r.top+(c.y+.5)*CELL,vx:-(15+Math.random()*45),vy:-(10+Math.random()*40),m:.6+Math.random()*.8,r:.35+Math.random()*.75,life:0,max:(1.4+Math.random()*1.4)*SL,ph:Math.random()*6.28,fq:4+Math.random()*5,w:Math.random()<.3}); }
      mc.clearRect(0,0,cols,rows); mc.fillStyle='#fff'; for(const c of K) if(!c.gone) mc.fillRect(c.x,c.y,1,1);
      const u=`url(${mk.toDataURL()})`; sh.style.webkitMaskImage=u; sh.style.maskImage=u; sh.style.webkitMaskSize=sh.style.maskSize='100% 100%';
      dl.style.background=`rgba(10,8,14,${(.55*(1-f)).toFixed(3)})`; if(f>=1) sh.style.visibility='hidden'; }
    cx.clearRect(0,0,cv.width,cv.height); cx.globalCompositeOperation='lighter'; cx.lineCap='round';
    const G=gust(t/SL), s=dt/SL;
    for(const p of P){ p.life+=dt; const a=1-p.life/p.max; if(a<=0) continue;
      const pull=Math.min(1,p.life/(.5*SL)+.25); p.vx+=(-150*G*pull/p.m)*s; p.vy+=(-55*G*pull/p.m)*s; p.vx*=1-.6*s; p.vy*=1-.6*s;
      const fl=Math.sin(p.life*p.fq/SL+p.ph), sp=Math.hypot(p.vx,p.vy)||1, nx=-p.vy/sp, ny=p.vx/sp;
      p.x+=(p.vx+nx*fl*22)*s; p.y+=(p.vy+ny*fl*22)*s;
      const X=p.x*D, Y=p.y*D, L=Math.min(10,sp*.03)*D, R=p.r*D;
      cx.strokeStyle=p.w?`rgba(255,250,235,${a})`:`rgba(255,222,150,${(a*.95).toFixed(3)})`; cx.lineWidth=R*2;
      cx.beginPath(); cx.moveTo(X,Y); cx.lineTo(X-p.vx/sp*L,Y-p.vy/sp*L); cx.stroke();
      if(p.w){ cx.fillStyle=`rgba(255,214,140,${(a*.18).toFixed(3)})`; cx.beginPath(); cx.arc(X,Y,R*5,0,7); cx.fill(); } }
    P=P.filter(p=>p.life<p.max); cx.globalCompositeOperation='source-over';
    if(t<TEND||P.length) requestAnimationFrame(frame); else fin(); }
  requestAnimationFrame(frame); return true; }
function choose(i){ if(byeGate(i)) return; """
CSS = ".byefx{position:fixed;inset:0;z-index:70;cursor:pointer}.byefx canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.byefx .bf-ring{position:fixed;opacity:0;pointer-events:none;box-shadow:0 0 0 2.5px rgba(255,226,160,.95),0 0 18px 4px rgba(255,214,140,.7),0 0 56px rgba(255,200,120,.45)}"
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read(); miss = []
    def rp(o, n, c=1):
        global s
        k = s.count(o)
        if k != c: miss.append((o[:70], k)); return
        s = s.replace(o, n)
    rp("  function bxRep(){ return null; }", SIM + "  function bxRep(){ return null; }")
    rp("wrec('mine','셋쇼인 키아라를 쓰러뜨렸다'); farewell(); return; }", "wrec('mine','셋쇼인 키아라를 쓰러뜨렸다'); if(!(w.arsNova||w.selfGone)) S.flags.bxBye=1; warOver(); return; }")
    rp("    S.flags.bxNpc=1; warOver(); }", "    S.flags.bxNpc=1; if(w.heroAlive&&!(w.arsNova||w.selfGone)) S.flags.bxBye=1; warOver(); }")
    rp("    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);", "    const E=S.epi; E.used=E.used||[]; E.n=E.n||ri(8,10);\n    if(S.flags.bxBye===1&&!S.pending&&!S.dead){ S.flags.bxBye=2; bxBye(); return; } // 11-14: 「새벽의 작별」")
    rp("function choose(i){ ", UI)
    rp(".comp .cf{display:inline-flex;", CSS + ".comp .cf{display:inline-flex;")
    s, nd, nt = i18n.add(s, D, T)
    print('bxbye miss', miss, 'tr', nd, nt)
    open(P, 'w', encoding='utf-8').write(s)
