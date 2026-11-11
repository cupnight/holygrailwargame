// 자동 진행 시험: node dev/sim.js <game.html> [생 수] [옵션 JSON]
// 옵션: {hero:'id', seed:1, pat:'정규식'(기록에서 셀 문장), crisis:'beast3R'|'black', lang:'ko'}
const fs = require('fs'), vm = require('vm');
const file = process.argv[2], N = +(process.argv[3] || 20), opt = JSON.parse(process.argv[4] || '{}');
const src = fs.readFileSync(file, 'utf8');
const a = src.indexOf('<script id="sim">') + 17, b = src.indexOf('</script>', a);
const ctx = { console, setTimeout, clearTimeout };
ctx.globalThis = ctx; ctx.window = ctx;
if (opt.hero) ctx.__FORCE_HERO = opt.hero;
if (opt.crisis) ctx.__FORCE_CRISIS = opt.crisis;
vm.createContext(ctx);
vm.runInContext(src.slice(a, b) + '\n;globalThis.Sim=Sim;', ctx, { filename: 'sim' });
const Sim = ctx.Sim;
const noop = () => {};
Sim.setHooks(new Proxy({}, { get: () => noop }));
const pat = opt.pat ? new RegExp(opt.pat) : null;
let err = 0, hits = {}, wars = 0, errs = [];
for (let n = 0; n < N; n++) {
  const seed = (opt.seed || 1) * 1000 + n;
  try {
    Sim.newLife({ seed, len: 20, ...(opt.life || {}) }); Sim.start();
    let guard = 0;
    while (Sim.S && !Sim.S.dead && guard++ < 400000) {
      const S = Sim.S;
      if (S.pending) { Sim.resolve(Sim.autoChoice(S.pending)); continue; }
      Sim.tick(1);
    }
    if (Sim.S.war) wars++;
    if (pat) for (const e of Sim.S.log) { const m = e.t && e.t.match(pat); if (m) hits[m[0]] = (hits[m[0]] || 0) + 1; }
  } catch (e) { err++; if (errs.length < 5) errs.push(seed + ': ' + (e.stack || e).toString().split('\n').slice(0, 4).join(' | ')); }
}
console.log(JSON.stringify({ lives: N, wars, err, hits }));
errs.forEach(x => console.log(x));
