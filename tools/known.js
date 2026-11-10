// 서버 허용 목록(src/known.js)을 게임 데이터에서 만든다.
// 서번트·업적·출신·도시가 늘면 이 스크립트를 다시 돌려야 서버가 새 값을 받아 준다.
// 업적 일부(마안 등)는 게임이 실행될 때 만들어지므로, 헤드리스 브라우저로 게임을 열어 Sim에서 직접 읽는다(Playwright 필요).
//   node tools/known.js          → src/known.js를 새로 쓴다
//   node tools/known.js --check  → 지금 src/known.js에 빠진 값이 있으면 알리고 실패(1)로 끝난다
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const root = path.join(__dirname, '..');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.route('**/*', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
  await p.goto('file://' + path.join(root, 'public/index.html'));
  await p.waitForFunction(() => typeof Sim === 'object' && Sim.HEROES && Sim.ACH);
  const known = await p.evaluate(() => ({
    heroes: Object.fromEntries(Sim.HEROES.map(h => [h.id, h.cls])),
    ach: Sim.ACH.map(a => a.id),
    origins: Sim.ORIGINS.map(o => o.id).sort(),
  }));
  await b.close();
  // 도시는 게임 안 도시 목록(서버로 보내는 이름 n)에서 읽는다
  const src = fs.readFileSync(path.join(root, 'public/index.html'), 'utf8');
  const m = /\n([ \t]*)const CITIES\s*=\s*\[/.exec(src);
  const end = src.indexOf(`\n${m[1]}];`, m.index + m[0].length);
  known.cities = [...src.slice(m.index, end).matchAll(/\{n:'([^']+)'/g)].map(x => x[1]);
  for (const [k, v] of Object.entries(known)) if (!Object.keys(v).length) throw new Error(`${k} 목록이 비었습니다`);

  const out = path.join(root, 'src/known.js');
  if (process.argv.includes('--check')) {
    const cur = fs.existsSync(out) ? fs.readFileSync(out, 'utf8') : '';
    const old = cur ? JSON.parse(cur.slice(cur.indexOf('{'), cur.lastIndexOf('}') + 1)) : { heroes: {}, ach: [], origins: [], cities: [] };
    const miss = {
      heroes: Object.keys(known.heroes).filter(h => old.heroes[h] !== known.heroes[h]),
      ach: known.ach.filter(a => !old.ach.includes(a)),
      origins: known.origins.filter(o => !old.origins.includes(o)),
      cities: known.cities.filter(c => !old.cities.includes(c)),
    };
    if (Object.values(miss).some(v => v.length)) { console.error('src/known.js에 빠진 값:', JSON.stringify(miss)); console.error('node tools/known.js 로 다시 만드세요.'); process.exit(1); }
    console.log('src/known.js가 게임 데이터와 맞습니다.');
  } else {
    fs.writeFileSync(out, `// tools/known.js가 게임 데이터에서 자동으로 만든 파일입니다. 직접 고치지 마세요.\nexport const KNOWN = ${JSON.stringify(known)};\n`);
    console.log(`src/known.js: 서번트 ${Object.keys(known.heroes).length} · 업적 ${known.ach.length} · 출신 ${known.origins.length} · 도시 ${known.cities.length}`);
  }
})().catch(e => { console.error(e.message || e); process.exit(1); });
