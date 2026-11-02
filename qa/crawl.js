// Created by: Claude
// Date: 2026-11-02
// Purpose: Full QA crawl of the syedcreates.com build. Serves ./site like Netlify (clean URLs, _redirects),
//          visits every page at desktop and mobile widths, records errors and issues to qa/report.json
// Owner: Syed Hadi
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = process.argv[2] || '/home/claude/syedhadi/site';
const OUT = process.argv[3] || '/home/claude/qa/report.json';

// --- redirects table
const redirects = [];
for (const line of fs.readFileSync(path.join(ROOT, '_redirects'), 'utf8').split('\n')) {
  const l = line.trim(); if (!l || l.startsWith('#')) continue;
  const [from, to, code] = l.split(/\s+/); redirects.push({ from, to, code: code || '301' });
}
function resolveFile(p) {
  p = decodeURIComponent(p.split('?')[0].split('#')[0]);
  if (p === '/' || p === '') return path.join(ROOT, 'index.html');
  const f = path.join(ROOT, p);
  if (fs.existsSync(f) && fs.statSync(f).isFile()) return f;
  if (fs.existsSync(f + '.html')) return f + '.html';
  if (fs.existsSync(path.join(f, 'index.html'))) return path.join(f, 'index.html');
  return null;
}
function redirectFor(p) {
  const clean = p.split('?')[0].split('#')[0];
  for (const r of redirects) {
    const forced = r.code.endsWith('!');
    if (r.from === clean || (r.from.endsWith('/*') && clean.startsWith(r.from.slice(0, -1)))) {
      if (!forced && resolveFile(clean)) return null; // shadowed by a real file
      return r;
    }
  }
  return null;
}
const ct = f => ({ '.css': 'text/css', '.js': 'application/javascript', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon', '.pdf': 'application/pdf', '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain', '.zip': 'application/zip' }[path.extname(f).toLowerCase()] || 'text/html');

(async () => {
  const pages = fs.readdirSync(ROOT).filter(n => n.endsWith('.html')).sort();
  const b = await chromium.launch();
  const report = { pages: {}, links: {}, remoteImgs: new Set(), redirects: redirects.length };
  const linkTargets = new Map(); // internal href -> [pages]
  for (const vp of [{ name: 'desktop', width: 1366, height: 900 }, { name: 'mobile', width: 390, height: 844 }]) {
    const ctx = await b.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
    await ctx.route('**/*', r => {
      const u = new URL(r.request().url());
      if (u.host === 'local') {
        const rd = redirectFor(u.pathname);
        if (rd && !/^https?:/.test(rd.to)) return r.fulfill({ status: 301, headers: { location: 'http://local' + rd.to } });
        const f = resolveFile(u.pathname);
        if (!f) return r.fulfill({ status: 404, body: 'nf' });
        return r.fulfill({ status: 200, body: fs.readFileSync(f), contentType: ct(f) });
      }
      // external: do not fetch (sandbox has no egress), just record
      return r.fulfill({ status: 204, body: '' });
    });
    for (const name of pages) {
      const slug = name === 'index.html' ? '/' : '/' + name.replace('.html', '');
      const page = await ctx.newPage();
      const rec = report.pages[name] = report.pages[name] || { slug, issues: [] };
      const add = (sev, msg) => { const k = `[${vp.name}] ${msg}`; if (!rec.issues.some(i => i.msg === k)) rec.issues.push({ sev, msg: k }); };
      page.on('pageerror', e => add('high', 'JS error: ' + e.message.slice(0, 160)));
      page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource: the server responded with a status of 204/.test(m.text())) add('med', 'console: ' + m.text().slice(0, 160)); });
      page.on('response', res => {
        const u = new URL(res.url());
        if (u.host === 'local' && res.status() === 404) add('high', 'missing asset ' + u.pathname);
      });
      try { await page.goto('http://local' + slug, { waitUntil: 'load', timeout: 20000 }); } catch (e) { add('high', 'load fail ' + e.message.slice(0, 80)); }
      await page.waitForTimeout(700);
      // scroll to trigger reveals / lazy
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } window.scrollTo(0, 0); });
      const d = await page.evaluate(() => {
        const q = s => [...document.querySelectorAll(s)];
        const out = {};
        out.title = document.title; out.desc = document.querySelector('meta[name=description]')?.content || '';
        out.canonical = document.querySelector('link[rel=canonical]')?.href || '';
        out.ogimg = document.querySelector('meta[property="og:image"]')?.content || '';
        out.robots = document.querySelector('meta[name=robots]')?.content || '';
        out.h1 = q('h1').map(h => h.textContent.trim().replace(/\s+/g, ' '));
        out.lang = document.documentElement.lang;
        out.ldErrors = q('script[type="application/ld+json"]').map(s => { try { JSON.parse(s.textContent); return null } catch (e) { return e.message } }).filter(Boolean);
        out.imgsNoAlt = q('img').filter(i => !i.hasAttribute('alt')).map(i => i.getAttribute('src')?.slice(0, 80));
        out.brokenLocalImgs = q('img').filter(i => i.complete && i.naturalWidth === 0 && (i.currentSrc || i.src).startsWith('http://local')).map(i => (i.currentSrc || i.src).replace('http://local', ''));
        out.remoteImgs = q('img').map(i => i.getAttribute('src')).filter(s => s && /^https?:/.test(s));
        out.links = q('a[href]').map(a => a.getAttribute('href'));
        out.emptyLinks = q('a').filter(a => !a.textContent.trim() && !a.querySelector('img,svg') && !a.getAttribute('aria-label')).length;
        out.buttonsNoName = q('button').filter(bt => !bt.textContent.trim() && !bt.getAttribute('aria-label') && !bt.title).length;
        out.dupIds = (() => { const c = {}; q('[id]').forEach(e => c[e.id] = (c[e.id] || 0) + 1); return Object.keys(c).filter(k => c[k] > 1); })();
        out.overflowX = document.documentElement.scrollWidth - window.innerWidth;
        out.wideEls = out.overflowX > 2 ? q('body *').filter(e => { const r = e.getBoundingClientRect(); return r.right > window.innerWidth + 2 && r.width > 0 && getComputedStyle(e).position !== 'fixed' && !e.closest('[class*=track],[class*=marquee],[class*=carousel],.logos,.feat-track'); }).slice(0, 4).map(e => e.tagName.toLowerCase() + '.' + (e.className && e.className.baseVal === undefined ? String(e.className).split(' ').slice(0, 2).join('.') : '') + ' w' + Math.round(e.getBoundingClientRect().right)) : [];
        const txt = document.body.innerText;
        out.emdash = (txt.match(/[—–]/g) || []).length;
        out.placeholders = (txt.match(/\b(lorem ipsum|TBD|\[INSERT|TODO|undefined|NaN|\[object Object\])\b/gi) || []).slice(0, 5);
        out.fontsUsed = [...new Set(q('h1,h2,h3,p,a,button').slice(0, 300).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/"/g, '')))];
        out.bricolage = /Bricolage/.test(document.documentElement.outerHTML);
        out.tinyText = q('p,li,a,span,small').filter(e => e.children.length === 0 && e.textContent.trim().length > 3 && parseFloat(getComputedStyle(e).fontSize) < 11 && e.offsetParent).length;
        out.tapTargets = window.innerWidth < 500 ? q('a,button').filter(e => { const r = e.getBoundingClientRect(); return e.offsetParent && r.width > 0 && r.height > 0 && r.height < 24 && r.width < 24; }).length : 0;
        return out;
      });
      if (vp.name === 'desktop') {
        Object.assign(rec, { title: d.title, desc: d.desc, canonical: d.canonical, h1: d.h1, robots: d.robots });
        if (!d.title) add('high', 'no <title>'); else if (d.title.length > 65) add('low', `title ${d.title.length} chars`);
        if (!d.desc) add('high', 'no meta description'); else if (d.desc.length > 165) add('low', `description ${d.desc.length} chars`); else if (d.desc.length < 70) add('low', `description short ${d.desc.length}`);
        if (!d.canonical && name !== '404.html') add('med', 'no canonical');
        else if (name !== '404.html') { const exp = 'https://syedcreates.com' + (slug === '/' ? '/' : slug); if (d.canonical !== exp) add('med', 'canonical ' + d.canonical + ' expected ' + exp); }
        if (!d.ogimg) add('low', 'no og:image');
        if (d.h1.length !== 1) add('med', `${d.h1.length} h1 tags`);
        if (d.ldErrors.length) add('high', 'JSON-LD parse error ' + d.ldErrors[0]);
        if (d.imgsNoAlt.length) add('med', `${d.imgsNoAlt.length} img without alt e.g. ${d.imgsNoAlt[0]}`);
        if (d.emptyLinks) add('med', `${d.emptyLinks} empty links`);
        if (d.buttonsNoName) add('med', `${d.buttonsNoName} buttons without accessible name`);
        if (d.dupIds.length) add('med', 'duplicate ids ' + d.dupIds.slice(0, 5).join(','));
        if (d.emdash) add('low', `${d.emdash} em/en dashes in visible text`);
        if (d.placeholders.length) add('high', 'placeholder text ' + d.placeholders.join(','));
        if (d.bricolage) add('low', 'still references Bricolage');
        d.remoteImgs.forEach(s => report.remoteImgs.add(s));
        d.links.forEach(h => { if (!linkTargets.has(h)) linkTargets.set(h, new Set()); linkTargets.get(h).add(name); });
      }
      if (d.brokenLocalImgs.length) add('high', 'broken images ' + d.brokenLocalImgs.slice(0, 3).join(', '));
      if (d.overflowX > 2) add('high', `horizontal overflow ${d.overflowX}px ${d.wideEls.join(' | ')}`);
      if (d.tinyText > 0 && vp.name === 'mobile') add('low', `${d.tinyText} text nodes under 11px`);
      if (d.tapTargets > 3) add('low', `${d.tapTargets} tap targets under 24px`);
      await page.close();
    }
    await ctx.close();
  }
  // internal link check
  const bad = [];
  for (const [h, from] of linkTargets) {
    if (!h || h.startsWith('#') || /^(mailto|tel|javascript|https?):/.test(h)) {
      if (/^https?:\/\/(www\.)?syedcreates\.com/.test(h)) {
        const p = h.replace(/^https?:\/\/(www\.)?syedcreates\.com/, '') || '/';
        if (!resolveFile(p) && !redirectFor(p)) bad.push({ h, from: [...from].slice(0, 4) });
      }
      continue;
    }
    let p = h.startsWith('/') ? h : '/' + h;
    const clean = p.split('#')[0].split('?')[0];
    if (!clean) continue;
    const rd = redirectFor(clean);
    if (!resolveFile(clean) && !rd) bad.push({ h, from: [...from].slice(0, 4) });
    else if (rd) report.links[h] = 'redirect -> ' + rd.to;
    // anchor check
    const hash = p.split('#')[1];
    if (hash && resolveFile(clean)) { const html = fs.readFileSync(resolveFile(clean), 'utf8'); if (!new RegExp(`id=["']${hash}["']`).test(html)) bad.push({ h, from: [...from].slice(0, 4), why: 'missing anchor' }); }
  }
  report.brokenLinks = bad;
  // duplicates
  const titles = {}, descs = {};
  for (const [n, r] of Object.entries(report.pages)) { if (r.title) (titles[r.title] = titles[r.title] || []).push(n); if (r.desc) (descs[r.desc] = descs[r.desc] || []).push(n); }
  report.dupTitles = Object.entries(titles).filter(([, v]) => v.length > 1);
  report.dupDescs = Object.entries(descs).filter(([, v]) => v.length > 1);
  report.remoteImgs = [...report.remoteImgs];
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1));
  await b.close();
  const all = Object.values(report.pages).flatMap(p => p.issues.map(i => ({ ...i, page: p.slug })));
  const by = s => all.filter(i => i.sev === s).length;
  console.log(`pages ${pages.length} | issues high ${by('high')} med ${by('med')} low ${by('low')} | broken links ${bad.length} | dup titles ${report.dupTitles.length} | dup descs ${report.dupDescs.length} | remote imgs ${report.remoteImgs.length}`);
})();
