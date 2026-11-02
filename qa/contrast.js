// Created by: Claude
// Date: 2026-11-02
// Purpose: WCAG contrast audit for the syedcreates.com build. Serves ./site locally, visits every page in light
//          and dark theme, measures each visible text element against its effective background and writes failures.
// Owner: Syed Hadi
// Usage: node qa/contrast.js <siteRoot> <out.json>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = process.argv[2] || '/home/claude/work/site';
const OUT = process.argv[3] || '/home/claude/qa/contrast.json';
const ct = f => ({ '.css': 'text/css', '.js': 'application/javascript', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json' }[path.extname(f).toLowerCase()] || 'text/html');
function resolveFile(p) {
  p = decodeURIComponent(p.split('?')[0]);
  if (p === '/' || p === '') return path.join(ROOT, 'index.html');
  const f = path.join(ROOT, p);
  if (fs.existsSync(f) && fs.statSync(f).isFile()) return f;
  if (fs.existsSync(f + '.html')) return f + '.html';
  return null;
}

const AUDIT = () => {
  const parse = (s) => { const m = String(s).match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] == null ? 1 : p[3] }; };
  const gradColors = (s) => (String(s).match(/rgba?\([^)]+\)/g) || []).map(parse).filter(Boolean);
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (top, bot) => ({ r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1 });
  const desc = (el) => { let s = el.tagName.toLowerCase(); if (el.id) s += '#' + el.id; if (el.className && typeof el.className === 'string') s += '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.'); return s; };
  const path = (el) => { const out = []; let e = el; for (let i = 0; e && i < 3; i++, e = e.parentElement) out.unshift(desc(e)); return out.join(' > '); };

  // background candidates under an element: list of possible solid colours (gradients give several)
  function bgs(el) {
    let layers = []; let e = el; let image = false;
    while (e && e.nodeType === 1) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        if (/url\(/.test(cs.backgroundImage)) { image = true; }
        const gc = gradColors(cs.backgroundImage);
        if (gc.length) {
          const base = parse(cs.backgroundColor);
          const solid = gc.every((c) => c.a >= 0.95);
          layers.push({ multi: gc, base });
          if (solid) break;
        }
      }
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { layers.push({ multi: [c] }); if (c.a >= 0.95) break; }
      e = e.parentElement;
    }
    // composite top -> bottom, expanding gradient stops into candidates
    let cands = [{ r: 255, g: 255, b: 255, a: 1 }];
    for (let i = layers.length - 1; i >= 0; i--) {
      const L = layers[i]; const next = [];
      cands.forEach((bot) => L.multi.forEach((top) => next.push(over(top, bot))));
      cands = next.slice(0, 12);
    }
    return { cands, image };
  }
  // text over an <img> that sits behind it in the same positioned box
  function overImg(el) {
    let e = el; for (let i = 0; e && i < 5; i++, e = e.parentElement) {
      if (e.querySelector && [...e.querySelectorAll('img,video,canvas')].some((m) => !m.contains(el) && !el.contains(m) && (() => { const a = m.getBoundingClientRect(), b = el.getBoundingClientRect(); return a.left <= b.left + 2 && a.right >= b.right - 2 && a.top <= b.top + 2 && a.bottom >= b.bottom - 2; })())) return true;
    }
    return false;
  }

  const out = []; const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    if (!n.nodeValue.trim()) continue;
    const el = n.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    if (el.closest('script,style,noscript,[hidden],.sr,[aria-hidden="true"],svg,.dd-menu,.mm,.mobile-menu,dialog:not([open])')) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) < 0.05) continue;
    // hidden by an ancestor's opacity/display
    let hiddenAnc = false; for (let a = el; a; a = a.parentElement) { const s = getComputedStyle(a); if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) < 0.05) { hiddenAnc = true; break; } }
    if (hiddenAnc) continue;
    let fgs;
    const fill = cs.webkitTextFillColor;
    if (fill && parse(fill) && parse(fill).a === 0 && /text/.test(cs.webkitBackgroundClip || cs.backgroundClip)) fgs = gradColors(cs.backgroundImage);
    else fgs = [parse(cs.color)];
    fgs = fgs.filter(Boolean); if (!fgs.length) continue;
    const { cands, image } = bgs(fgs.length > 1 ? el.parentElement : el);
    const img = image || overImg(el);
    const size = parseFloat(cs.fontSize), bold = Number(cs.fontWeight) >= 700;
    const large = size >= 24 || (bold && size >= 18.66);
    const need = large ? 3 : 4.5;
    let worst = 99;
    fgs.forEach((f) => cands.forEach((b) => { const fc = f.a < 1 ? over(f, b) : f; worst = Math.min(worst, ratio(fc, b)); }));
    if (worst < need) out.push({ sel: path(el), text: n.nodeValue.trim().slice(0, 50), ratio: Math.round(worst * 100) / 100, need, size: Math.round(size), img, fg: cs.color, bg: cands.map((c) => `rgb(${Math.round(c.r)},${Math.round(c.g)},${Math.round(c.b)})`).slice(0, 3).join(' | ') });
  }
  return out;
};

(async () => {
  const pages = fs.readdirSync(ROOT).filter((n) => n.endsWith('.html')).sort();
  const b = await chromium.launch();
  const report = {};
  for (const theme of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: 1366, height: 900 } });
    await ctx.addInitScript((t) => { try { localStorage.setItem('sh_theme', t); } catch (e) { } }, theme);
    await ctx.route('**/*', (r) => {
      const u = new URL(r.request().url());
      if (u.host === 'local') { const f = resolveFile(u.pathname); return f ? r.fulfill({ status: 200, body: fs.readFileSync(f), contentType: ct(f) }) : r.fulfill({ status: 404, body: '' }); }
      return r.fulfill({ status: 204, body: '' });
    });
    const pg = await ctx.newPage();
    for (const name of pages) {
      const slug = name === 'index.html' ? '/' : '/' + name.replace('.html', '');
      try {
        await pg.goto('http://local' + slug, { waitUntil: 'load', timeout: 20000 });
        await pg.evaluate((t) => { document.documentElement.setAttribute('data-theme', t); document.querySelectorAll('.reveal').forEach((e) => e.classList.add('in', 'visible', 'show')); }, theme);
        await pg.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important;transition:none!important}*{transition:none!important;animation:none!important}' });
        await pg.waitForTimeout(150);
        const res = await pg.evaluate(AUDIT);
        if (res.length) report[theme + ' ' + slug] = res;
      } catch (e) { report[theme + ' ' + slug] = [{ error: String(e.message).slice(0, 120) }]; }
    }
    await ctx.close();
  }
  await b.close();
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1));
  const all = Object.values(report).flat();
  console.log('pages with failures', Object.keys(report).length, 'items', all.length, 'over images', all.filter((x) => x.img).length);
})();
