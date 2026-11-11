// 화면까지 돌려 보는 시험: node dev/uirun.js <game.html> [생 수] [lang] [crisis] [hero]
const { chromium } = require('playwright'); const path = require('path'); const fs=require('fs');
const file = path.resolve(process.argv[2]), N = +(process.argv[3] || 3), lang = process.argv[4] || 'ko', cr = process.argv[5] || 'beast', hero = process.argv[6] || '';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e.stack || e).slice(0, 300)));
  await p.route('**/*', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
  await p.addInitScript(([l, c, h]) => { try { localStorage.setItem('cupnight.lang', JSON.stringify(l)); } catch (e) {} globalThis.__FORCE_CRISIS = c === 'none' ? false : c; if (h) globalThis.__FORCE_HERO = h; }, [lang, cr, hero]);
  await p.goto('file://' + file); await p.waitForFunction(() => typeof Sim === 'object' && Sim.HEROES);
  const out = await p.evaluate(async (N) => { const res = [];
    for (let n = 0; n < N; n++) { Sim.newLife({ seed: 4242 + n, len: 20 }); Sim.start(); let g = 0;
      while (Sim.S && !Sim.S.dead && g++ < 300000) { const S = Sim.S; if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); } else Sim.tick(1); if (g % 3000 === 0) await new Promise(r => setTimeout(r, 0)); }
      const w = Sim.S.war, c = w && w.crisis; res.push({ stage: c && c.stage, type: c && c.type, end: Sim.S.flags.bxEnd || Sim.S.flags.bxDream || '-', logs: Sim.S.log.length }); }
    return res; }, N);
  const txt = await p.evaluate(() => document.body.innerText.slice(0, 400));
  console.log(JSON.stringify(out)); console.log('errors', errs.length); errs.slice(0, 5).forEach(e => console.log(' !', e));
  const hang = (await p.evaluate(() => document.body.innerText)).match(/[가-힣]{2,}/g) || []; if (lang !== 'ko') console.log('hangul tokens on screen', hang.length, hang.slice(0, 10).join(' '));
  await b.close();
})();
