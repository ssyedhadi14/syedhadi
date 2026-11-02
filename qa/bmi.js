// Created by: Claude
// Date: 2026-11-02
// Purpose: QA for /bmi-calculator: math, bands, insights triggers, tracker persistence, PDF, mobile overflow
// Owner: Syed Hadi
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const ROOT = '/home/claude/work/site';
const ct = f => ({ '.css': 'text/css', '.js': 'application/javascript', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg' }[path.extname(f)] || 'text/html');
(async () => {
  const b = await chromium.launch(); const out = [];
  const say = (ok, m) => out.push((ok ? 'PASS ' : 'FAIL ') + m);
  for (const vp of [{ w: 1366, h: 900, n: 'desktop' }, { w: 390, h: 844, n: 'mobile' }]) {
    const ctx = await b.newContext({ viewport: { width: vp.w, height: vp.h }, acceptDownloads: true });
    await ctx.route('**/*', r => { const u = new URL(r.request().url()); if (u.host !== 'local') return r.fulfill({ status: 204, body: '' }); let f = path.join(ROOT, u.pathname === '/' ? 'index.html' : u.pathname); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html'; if (!fs.existsSync(f)) return r.fulfill({ status: 404, body: '' }); r.fulfill({ body: fs.readFileSync(f), contentType: ct(f) }); });
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto('http://local/bmi-calculator'); await p.waitForTimeout(900);
    if (vp.n === 'desktop') {
      const bmi = await p.textContent('#oBmi'); say(bmi === '27.0', `default 170/78 BMI ${bmi} (expect 27.0)`);
      say((await p.textContent('#oBand')) === 'Obesity', 'band ' + await p.textContent('#oBand'));
      say(/53 to 66 kg/.test(await p.textContent('#oRange')), 'healthy range ' + await p.textContent('#oRange'));
      say((await p.textContent('#oWhtr')) === '0.54', 'whtr ' + await p.textContent('#oWhtr'));
      const rows = await p.$$eval('#ins table', t => t.map(x => x.querySelectorAll('tbody tr').length)); say(rows[0] >= 5 && rows[1] >= 3, `start rows ${rows[0]} stop rows ${rows[1]}`);
      // markers
      await p.fill('#sys', '128'); await p.fill('#dia', '90'); await p.fill('#alt', '58'); await p.fill('#fbs', '104'); await p.waitForTimeout(200);
      const mk = await p.$$eval('#mk tbody tr', t => t.map(r => r.textContent));
      say(mk.length === 3, 'markers rows ' + mk.length); say(/stage 2/.test(mk[0]), 'BP 128/90 -> ' + mk[0].slice(0, 80));
      say(/Prediabetes/.test(mk[1]), 'FBS 104 -> prediabetes'); say(/Above most lab/.test(mk[2]), 'SGPT 58 -> above lab');
      const ins = await p.textContent('#ins');
      for (const k of ['Log your blood pressure', 'Cut salt', 'liver follow up', 'Walk 10 to 15 minutes after', 'Self diagnosis', 'Sitting for hours', 'Sugary drinks', 'Refined carbs']) say(ins.includes(k), 'insight present: ' + k);
      // url never contains markers
      say(!/sys=|alt=|fbs=|dia=/.test(p.url()), 'markers kept out of URL: ' + p.url().split('?')[1].slice(0, 90));
      // tracker
      const habits = await p.$$eval('#trk tbody tr', t => t.length); say(habits === 8, 'tracker habits ' + habits);
      say(await p.evaluate(() => [...document.querySelectorAll('#trk tbody th')].some(t => /Log blood pressure/.test(t.textContent))), 'BP flag adds Log blood pressure habit');
      await p.click('#trk .tk[data-d="0"]'); await p.click('#trk tbody tr:nth-child(2) .tk[data-d="1"]'); await p.waitForTimeout(150);
      say((await p.textContent('#trkScore')) === '4%', 'score after 2 ticks ' + await p.textContent('#trkScore'));
      await p.reload(); await p.waitForTimeout(700);
      say((await p.textContent('#trkScore')) === '4%', 'ticks persist after reload ' + await p.textContent('#trkScore'));
      // edge: underweight female
      await p.selectOption('#sex', 'f'); await p.fill('#ht', '165'); await p.fill('#wt', '48'); await p.fill('#waist', ''); await p.waitForTimeout(200);
      say((await p.textContent('#oBand')) === 'Underweight', 'underweight 165/48 band ' + await p.textContent('#oBand') + ' bmi ' + await p.textContent('#oBmi'));
      say((await p.textContent('#ins')).includes('Eat enough'), 'underweight insight present');
      // healthy
      await p.fill('#wt', '58'); await p.fill('#waist', '72'); await p.waitForTimeout(200);
      say((await p.textContent('#oBand')) === 'Healthy range', 'healthy 165/58 band ' + await p.textContent('#oBand'));
      // invalid
      await p.fill('#ht', '5'); await p.waitForTimeout(150); say(await p.evaluate(() => document.getElementById('out').classList.contains('dim')), 'invalid height dims output');
      // back to a flagged profile for the PDF
      await p.goto('http://local/bmi-calculator'); await p.waitForTimeout(700);
      await p.fill('#sys', '128'); await p.fill('#dia', '90'); await p.fill('#alt', '58'); await p.fill('#fbs', '104'); await p.waitForTimeout(200);
      const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 30000 }), p.click('#pdfBtn')]);
      await dl.saveAs('/home/claude/qa/pdfs/bmi.pdf'); say(true, 'PDF ' + dl.suggestedFilename() + ' ' + (fs.statSync('/home/claude/qa/pdfs/bmi.pdf').size / 1024 | 0) + ' KB');
      await p.screenshot({ path: '/home/claude/qa/bmi-desk.png', fullPage: true });
      // dark mode
      await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark')); await p.waitForTimeout(200);
      await p.screenshot({ path: '/home/claude/qa/bmi-dark.png', fullPage: true });
    } else {
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); say(ov <= 1, 'mobile overflow ' + ov + 'px');
      await p.screenshot({ path: '/home/claude/qa/bmi-mob.png', fullPage: true });
    }
    say(!errs.length, `${vp.n} JS errors: ${errs.join(' | ') || 'none'}`);
    await ctx.close();
  }
  await b.close(); console.log(out.join('\n'));
})();
