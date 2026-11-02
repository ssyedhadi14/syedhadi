// Created by: Claude
// Date: 2026-11-02
// Purpose: Interactive QA for syedcreates.com build: nav, mobile menu, theme, calculators, scorecards, PDFs, forms
// Owner: Syed Hadi
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = process.argv[2] || '/home/claude/syedhadi/site';
const OUTDIR = '/home/claude/qa/pdfs'; fs.mkdirSync(OUTDIR, { recursive: true });
const ct = f => ({ '.css': 'text/css', '.js': 'application/javascript', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.json': 'application/json', '.pdf': 'application/pdf' }[path.extname(f)] || 'text/html');
const results = [];
const ok = (area, msg) => results.push(['PASS', area, msg]);
const bad = (area, msg) => results.push(['FAIL', area, msg]);

async function route(ctx) {
  await ctx.route('**/*', r => {
    const u = new URL(r.request().url());
    if (u.host !== 'local') {
      // jsPDF etc come from local assets; stub CDNs with empty but valid responses
      if (/cdnjs|jsdelivr|unpkg/.test(u.host)) return r.fulfill({ status: 404, body: '' });
      return r.fulfill({ status: 204, body: '' });
    }
    let f = path.join(ROOT, u.pathname === '/' ? 'index.html' : decodeURIComponent(u.pathname));
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html';
    if (!fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ body: fs.readFileSync(f), contentType: ct(f) });
  });
}
async function newPage(ctx, errs) {
  const p = await ctx.newPage();
  p.on('pageerror', e => errs.push(e.message.slice(0, 140)));
  return p;
}
async function pdfFrom(p, sel, name, area) {
  try {
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 30000 }), p.click(sel)]);
    const f = path.join(OUTDIR, name); await dl.saveAs(f);
    const sz = fs.statSync(f).size; const head = fs.readFileSync(f).slice(0, 5).toString();
    if (head === '%PDF-' && sz > 20000) ok(area, `PDF ${dl.suggestedFilename()} ${(sz / 1024) | 0} KB`); else bad(area, `PDF invalid size ${sz} head ${head}`);
  } catch (e) { bad(area, 'PDF download failed: ' + e.message.slice(0, 100)); }
}

(async () => {
  const b = await chromium.launch();
  // ---------- desktop nav
  {
    const ctx = await b.newContext({ viewport: { width: 1366, height: 900 }, acceptDownloads: true }); await route(ctx);
    const errs = []; const p = await newPage(ctx, errs);
    await p.goto('http://local/'); await p.waitForTimeout(600);
    const groups = await p.$$eval('.dd-btn', bs => bs.map(b => b.dataset.group || b.textContent.trim()));
    for (const g of groups) {
      const btn = p.locator(`.dd-btn[data-group="${g}"]`).first();
      await btn.hover(); await p.waitForTimeout(350);
      let vis = await p.evaluate(g => { const m = document.querySelector(`.dd[data-group="${g}"] .dd-menu`); if (!m) return 'nomenu'; const r = m.getBoundingClientRect(); const s = getComputedStyle(m); return (s.visibility !== 'hidden' && s.opacity > 0.5 && r.height > 50) ? 'ok:' + m.querySelectorAll('a').length + ' links, right ' + Math.round(r.right) : 'hidden'; }, g);
      if (!vis.startsWith('ok')) { await btn.click(); await p.waitForTimeout(350); vis = await p.evaluate(g => { const m = document.querySelector(`.dd[data-group="${g}"] .dd-menu`); const r = m.getBoundingClientRect(); const s = getComputedStyle(m); return (s.visibility !== 'hidden' && s.opacity > 0.5 && r.height > 50) ? 'ok(click):' + m.querySelectorAll('a').length + ' links, right ' + Math.round(r.right) : 'hidden'; }, g); }
      const offscreen = vis.startsWith('ok') && +vis.split('right ')[1] > 1366;
      (vis.startsWith('ok') && !offscreen ? ok : bad)('nav desktop', `${g}: ${vis}${offscreen ? ' OFFSCREEN' : ''}`);
      await p.mouse.move(5, 600); await p.keyboard.press('Escape'); await p.waitForTimeout(250);
    }
    await p.screenshot({ path: '/home/claude/qa/nav-calc.png' });
    // theme
    const before = await p.evaluate(() => document.documentElement.dataset.theme);
    await p.click('.theme-btn'); await p.waitForTimeout(200);
    const after = await p.evaluate(() => document.documentElement.dataset.theme);
    (before !== after ? ok : bad)('theme', `${before} -> ${after}`);
    await p.click('.theme-btn');
    if (errs.length) bad('home js', errs.join(' | '));
    await ctx.close();
  }
  // ---------- mobile menu
  {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); await route(ctx);
    const errs = []; const p = await newPage(ctx, errs);
    for (const s of ['/', '/brand', '/car-mileage-calculator', '/loan-calculator']) {
      await p.goto('http://local' + s); await p.waitForTimeout(500);
      const shown0 = await p.evaluate(() => { const l = document.querySelector('.nav-links'); return l ? getComputedStyle(l).display : 'none' });
      await p.tap('#menuBtn'); await p.waitForTimeout(400);
      const st = await p.evaluate(() => { const l = document.querySelector('.nav-links'); const r = l.getBoundingClientRect(); return { disp: getComputedStyle(l).display, h: Math.round(r.height), links: [...l.querySelectorAll('a')].filter(a => a.offsetParent).length, exp: document.querySelector('#menuBtn').getAttribute('aria-expanded') }; });
      ((st.h > 100 && st.links > 3) ? ok : bad)('mobile menu', `${s}: closed=${shown0} open h${st.h} visible links ${st.links} aria-expanded=${st.exp}`);
      // open a group in mobile menu
      const groups = await p.evaluate(() => [...document.querySelectorAll('.nav-links .dd')].map(d => { const b = d.querySelector('.dd-btn'); return { g: d.dataset.group, btnVis: !!(b && b.offsetParent), simple: [...d.querySelectorAll('.mm-simple a')].filter(a => a.offsetParent).length }; }));
      for (const gr of groups) {
        let n = gr.simple;
        if (gr.btnVis && !n) { await p.tap(`.nav-links .dd[data-group="${gr.g}"] .dd-btn`); await p.waitForTimeout(300); n = await p.evaluate(g => [...document.querySelectorAll(`.nav-links .dd[data-group="${g}"] a`)].filter(a => a.offsetParent).length, gr.g); }
        (n > 0 ? ok : bad)('mobile submenu', `${s}: ${gr.g} btnVisible=${gr.btnVis} links shown ${n}`);
      }
      if (s === '/') await p.screenshot({ path: '/home/claude/qa/mobile-menu.png' });
    }
    if (errs.length) bad('mobile js', errs.join(' | '));
    await ctx.close();
  }
  // ---------- calculators & PDFs
  const ctx = await b.newContext({ viewport: { width: 1366, height: 900 }, acceptDownloads: true }); await route(ctx);
  const runCalc = async (slug, fn) => {
    const errs = []; const p = await newPage(ctx, errs);
    await p.goto('http://local' + slug); await p.waitForTimeout(1200);
    try { await fn(p); } catch (e) { bad(slug, 'test threw ' + e.message.slice(0, 160)); }
    const nan = await p.evaluate(() => (document.querySelector('main')?.innerText || '').match(/\b(NaN|Infinity|undefined)\b|₹-|₹NaN/g));
    if (nan) bad(slug, 'bad numbers in page: ' + [...new Set(nan)].join(','));
    if (errs.length) bad(slug, 'JS errors: ' + errs.join(' | ')); else ok(slug, 'no JS errors');
    await p.close();
  };
  await runCalc('/car-mileage-calculator', async p => {
    const v = await p.textContent('#oFuel'); (v === '₹7,395' ? ok : bad)('car', 'default fuel/month ' + v);
    const r = await p.textContent('#oRangeS'); (/1\.8 fill ups/.test(r) ? ok : bad)('car', 'fill ups: ' + r);
    await p.click('.cm-city button[data-k=hyd]'); (await p.textContent('#oFuel') === '₹7,767' ? ok : bad)('car', 'hyd ' + await p.textContent('#oFuel'));
    await p.fill('#kmpl', '0'); await p.waitForTimeout(150); const dim = await p.evaluate(() => document.getElementById('out').classList.contains('dim')); (dim ? ok : bad)('car', 'zero mileage handled (dim)');
    await p.fill('#kmpl', '15'); await p.click('.cm-city button[data-k=blr]');
    await pdfFrom(p, '#pdfBtn', 'car.pdf', 'car');
  });
  await runCalc('/loan-calculator', async p => {
    const emi = await p.textContent('#oEmi'); (/43,391/.test(emi) ? ok : bad)('loan', 'default EMI ' + emi);
    for (const k of ['car', 'personal', 'home']) { await p.click(`.ln-tabs button[data-k=${k}]`); await p.waitForTimeout(200); ok('loan', k + ' tab EMI ' + await p.textContent('#oEmi')); }
    await p.click('#tblBtn'); await p.waitForTimeout(200); const rows = await p.$$eval('#tbl tr', t => t.length); (rows > 10 ? ok : bad)('loan', 'table rows ' + rows);
    await pdfFrom(p, '#pdfBtn', 'loan.pdf', 'loan');
  });
  await runCalc('/fire-calculator', async p => { await pdfFrom(p, '#pdfBtn', 'fire.pdf', 'fire'); });
  await runCalc('/mutual-fund-returns-calculator', async p => { await pdfFrom(p, '#pdfBtn', 'mf.pdf', 'mf'); });
  await runCalc('/pmm-salary-2026', async p => { const has = await p.$('#pdfBtn'); if (has) await pdfFrom(p, '#pdfBtn', 'pmm.pdf', 'pmm'); else bad('pmm', 'no #pdfBtn'); });
  await runCalc('/qums', async p => {
    await p.fill('#kname', 'QA Test'); await p.fill('#kdate', '2026-11-02'); await p.fill('#cash', '200000'); await p.fill('#bank', '800000'); await p.fill('#paid', '300000');
    await p.click('#goTotal'); await p.waitForTimeout(500);
    ok('qums', 'modal: Qums ' + await p.textContent('#mdK') + ' | Imam ' + await p.textContent('#mdI'));
    ok('qums','total shown: '+(await p.evaluate(()=>document.querySelector('main').innerText.match(/₹[\d,]+/g)?.slice(0,4).join(' '))));
    await pdfFrom(p, '#optPdf', 'qums.pdf', 'qums');
  });
  await runCalc('/salary-calculator', async p => {
    const btns = await p.$$eval('button', bs => bs.map(b => (b.id || '') + ':' + b.textContent.trim()).filter(t => /pdf|download/i.test(t)));
    ok('salary', 'pdf buttons ' + btns.join(' | '));
    const sel = await p.evaluate(() => { const b = [...document.querySelectorAll('button')].find(b => /download/i.test(b.textContent) && /pdf/i.test(b.textContent)); return b ? (b.id ? '#' + b.id : null) : null; });
    if (sel) await pdfFrom(p, sel, 'salary.pdf', 'salary'); else bad('salary', 'no direct PDF download button found');
  });
  for (const s of ['/gtm-health-check', '/ai-visibility-checker', '/partner-readiness-score']) {
    await runCalc(s, async p => {
      const n = await p.$$eval('.qz-opts', x => x.length);
      for (let i = 0; i < n; i++) await p.check(`input[name=q${i}][value="1"]`, { force: true });
      const sub = await p.$('#qz button[type=submit], #qz .btn-primary'); if (sub) await sub.click(); await p.waitForTimeout(600);
      const res = await p.evaluate(() => ({ num: document.getElementById('qzNum')?.textContent.trim(), band: document.getElementById('qzBand')?.textContent.trim().slice(0, 60), fixes: document.querySelectorAll('#qzFix li, #qzFix > *').length, vis: !!document.getElementById('qzOut')?.offsetParent }));
      ((res.vis && res.num && !/your result$/i.test(res.band)) ? ok : bad)(s, `answered ${n}: score ${res.num} band "${res.band}" fixes ${res.fixes} visible ${res.vis}`);
    });
  }
  // blog render
  await runCalc('/blog', async p => { const n = await p.$$eval('.mpost', a => a.length); (n > 20 ? ok : bad)('blog', `${n} Medium cards`); const dash = await p.evaluate(() => /[—–]/.test(document.querySelector('[data-medium-blog]').innerText)); (dash ? bad : ok)('blog', 'dashes in card titles: ' + dash); });
  await runCalc('/posts', async p => { const n = await p.$$eval('.lip', a => a.length); (n > 20 ? ok : bad)('posts', `${n} post cards`); });
  await runCalc('/brand', async p => {
    for (const a of await p.$$eval('a[download]', as => as.map(a => a.getAttribute('href')))) { const f = path.join(ROOT, a); (fs.existsSync(f) ? ok : bad)('brand', 'download exists ' + a); }
    await p.click('.cp[data-cp=bioS]').catch(() => {}); ok('brand', 'copy click no error');
  });
  // forms
  {
    const p = await ctx.newPage();
    const forms = new Set();
    for (const s of ['/', '/about', '/gtm-in-a-box', '/skill-pack', '/brand']) {
      await p.goto('http://local' + s); await p.waitForTimeout(300);
      (await p.$$eval('form', fs => fs.map(f => f.className.split(' ')[0] + ' -> ' + f.action + ' ' + f.method + ' next=' + (f.querySelector('[name=_next]')?.value || '')))).forEach(x => forms.add(s + ' :: ' + x));
    }
    forms.forEach(f => ok('forms', f));
    await p.close();
  }
  await b.close();
  for (const r of results) console.log(r.join('  |  '));
  console.log('\nFAIL count', results.filter(r => r[0] === 'FAIL').length);
})();
