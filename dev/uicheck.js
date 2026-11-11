// 브라우저 로드 · 번역 확인: node dev/uicheck.js <game.html> '<문장 JSON 배열>'
const { chromium } = require('playwright'); const path = require('path');
const fs = require('fs'); const file0 = path.resolve(process.argv[2]); const file = file0.replace(/\.html$/, '.uicheck.html');
fs.writeFileSync(file, fs.readFileSync(file0, 'utf8').replace('\nfunction tr(s){', '\nwindow.__tr=s=>tr(s);function tr(s){')); const samples = JSON.parse(process.argv[3] || '[]');
(async () => {
  const b = await chromium.launch(); let bad = 0;
  for (const lang of ['ko', 'en', 'ja']) {
    const p = await b.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.route('**/*', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
    await p.addInitScript(l => { try { localStorage.setItem('cupnight.lang', JSON.stringify(l)); } catch (e) {} }, lang);
    await p.goto('file://' + file); await p.waitForFunction(() => typeof Sim === 'object' && Sim.HEROES);
    const out = await p.evaluate(ss => ss.map(s => [s, window.__tr ? window.__tr(s) : '?']), samples);
    const real = errs.filter(e => !/net::|ERR_|Failed to load resource/.test(e));
    console.log(`== ${lang} errors:${real.length}`); real.slice(0, 5).forEach(e => console.log('  !', e.slice(0, 200)));
    if (lang !== 'ko') for (const [s, t] of out) { const h = /[가-힣]/.test(t); if (h) bad++; console.log(h ? '  ✗' : '  ✓', t.slice(0, 110)); }
    await p.close();
  }
  await b.close(); fs.unlinkSync(file); console.log('untranslated', bad);
})();
