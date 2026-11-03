#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Quote band v2 for syedcreates.com. Bigger and brighter, 79 curated quotes from tech, business,
#          finance and motivational leaders, a new quote of the day every day, category filters, arrows,
#          swipe and autoplay. Wildlife backgrounds plug in via QB2_IMG in assets/quotes.js. Idempotent.
# Owner: Syed Hadi
import glob, html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.join(HERE, "..", "site")
sys.path.insert(0, HERE)
from quotes_v2_data import Q, CATS
E = html.escape

first = Q[0]
chips = "".join(f'<button type="button" class="qb2-chip{" on" if k == "all" else ""}" data-c="{k}">{v}</button>' for k, v in CATS)
SECTION = f'''<section class="qb2" aria-label="Quotes from tech, business, finance and motivational leaders">
<div class="wrap"><figure class="qb2-card" data-qb2 data-cat="{first[3]}">
<div class="qb2-bg" aria-hidden="true"></div><span class="qb2-mark" aria-hidden="true">&ldquo;</span>
<div class="qb2-top"><span class="qb2-eb"><i></i><span class="qb2-lbl">Quote of the day</span></span><div class="qb2-chips" role="group" aria-label="Filter quotes">{chips}</div></div>
<blockquote class="qb2-q">&ldquo;{E(first[0])}&rdquo;</blockquote>
<figcaption class="qb2-foot"><span class="qb2-av" aria-hidden="true">AK</span><span class="qb2-who-w"><b class="qb2-who">{E(first[1])}</b><small class="qb2-role">{E(first[2])}</small></span>
<span class="qb2-ctl"><button type="button" class="qb2-btn" data-d="-1" aria-label="Previous quote"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button><span class="qb2-n" aria-live="polite">01/{len(Q)}</span><button type="button" class="qb2-btn" data-d="1" aria-label="Next quote"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button></span></figcaption>
<span class="qb2-bar" aria-hidden="true"><i></i></span>
</figure></div></section>
'''

JS = """/* Created by: Claude | Date: 2026-11-03 | Purpose: quote band v2, quote of the day, filters, autoplay | Owner: Syed Hadi */
(function () {
  var Q = %s;
  // Wildlife backgrounds: drop files in /img/quotes/ and list them here, e.g. {tech:'/img/quotes/eagle.jpg'}
  var QB2_IMG = window.QB2_IMG || {};
  var MS = 9000, LBL = {tech: 'Tech leaders', business: 'Business leaders', finance: 'Money minds', motivation: 'Motivation'};
  function ini(n) { var p = n.replace(/[^A-Za-z .]/g, '').split(/[ .]+/).filter(Boolean); return ((p[0] || '')[0] + ((p.length > 1 ? p[p.length - 1] : '')[0] || '')).toUpperCase(); }
  function init(card) {
    var $ = function (s) { return card.querySelector(s); }, cat = 'all', list = Q.slice(), i = 0, timer = null, paused = false;
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var day = Math.floor((Date.now() + 19800000) / 86400000), today = day %% Q.length; // IST day
    function filter(c) { cat = c; list = c === 'all' ? Q.slice() : Q.filter(function (q) { return q[3] === c; }); }
    function paint(q) {
      $('.qb2-q').textContent = '\\u201C' + q[0] + '\\u201D'; $('.qb2-who').textContent = q[1]; $('.qb2-role').textContent = q[2]; $('.qb2-av').textContent = ini(q[1]);
      $('.qb2-lbl').textContent = (cat === 'all' && Q.indexOf(q) === today) ? 'Quote of the day' : (LBL[q[3]] || 'Quote');
      $('.qb2-n').textContent = ('0' + (i + 1)).slice(-2) + '/' + list.length;
      card.setAttribute('data-cat', q[3]);
      var bg = $('.qb2-bg'); bg.style.backgroundImage = QB2_IMG[q[3]] ? 'url(' + QB2_IMG[q[3]] + ')' : '';
      card.classList.toggle('has-img', !!QB2_IMG[q[3]]);
    }
    function set(n) {
      i = (n + list.length) %% list.length; var q = list[i];
      card.classList.add('qb2-out');
      setTimeout(function () { paint(q); card.classList.remove('qb2-out'); bar(); }, reduce ? 0 : 240);
    }
    function bar() { var b = $('.qb2-bar i'); b.style.animation = 'none'; void b.offsetWidth; b.style.animation = ''; b.style.animationDuration = MS + 'ms'; b.style.animationPlayState = paused ? 'paused' : 'running'; }
    function tick() { clearInterval(timer); if (reduce) return; timer = setInterval(function () { if (!paused && !document.hidden) set(i + 1); }, MS); }
    function pause(p) { paused = p; var b = $('.qb2-bar i'); if (b) b.style.animationPlayState = p ? 'paused' : 'running'; }
    card.addEventListener('mouseenter', function () { pause(true); }); card.addEventListener('mouseleave', function () { pause(false); });
    card.addEventListener('focusin', function () { pause(true); }); card.addEventListener('focusout', function () { pause(false); });
    [].forEach.call(card.querySelectorAll('.qb2-btn'), function (b) { b.addEventListener('click', function () { set(i + +b.getAttribute('data-d')); tick(); }); });
    [].forEach.call(card.querySelectorAll('.qb2-chip'), function (b) { b.addEventListener('click', function () {
      [].forEach.call(card.querySelectorAll('.qb2-chip'), function (x) { x.classList.toggle('on', x === b); });
      filter(b.getAttribute('data-c')); set(cat === 'all' ? today : Math.floor(Math.random() * list.length)); tick(); }); });
    var sx = null;
    card.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    card.addEventListener('touchend', function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) { set(i + (dx < 0 ? 1 : -1)); tick(); } sx = null; });
    i = today; paint(list[i]); bar(); tick();
  }
  function go() { [].forEach.call(document.querySelectorAll('[data-qb2]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
""" % json.dumps([list(q) for q in Q], ensure_ascii=False, separators=(",", ":"))

CSS = """
/* 2026-11-03 quote band v2: bigger, brighter, categories, quote of the day */
.qband{display:none}
.qb2{padding:12px 0 56px}
.qb2-card{--g1:#5b3df5;--g2:#1fb6ff;position:relative;margin:0;overflow:hidden;border-radius:28px;padding:clamp(26px,4vw,52px);color:#fff;
 background:radial-gradient(900px 420px at 85% -10%,rgba(255,255,255,.28),transparent 60%),linear-gradient(125deg,var(--g1),var(--g2));
 box-shadow:0 30px 80px -30px var(--g1);isolation:isolate;transition:background .6s,box-shadow .6s}
.qb2-card[data-cat=tech]{--g1:#4f2cf5;--g2:#13a8ff}
.qb2-card[data-cat=business]{--g1:#ff5f1f;--g2:#c2185b}
.qb2-card[data-cat=finance]{--g1:#047857;--g2:#1d4ed8}
.qb2-card[data-cat=motivation]{--g1:#f72585;--g2:#7209b7}
.qb2-bg{position:absolute;inset:0;z-index:-1;background-size:cover;background-position:center;opacity:0;transition:opacity .6s}
.qb2-card.has-img .qb2-bg{opacity:1}
.qb2-card.has-img::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(100deg,rgba(8,6,20,.86) 0%,rgba(8,6,20,.55) 55%,rgba(8,6,20,.2) 100%)}
.qb2-mark{position:absolute;right:clamp(10px,4vw,48px);top:-40px;font:400 clamp(180px,22vw,300px)/1 "Instrument Serif",Georgia,serif;color:rgba(255,255,255,.14);pointer-events:none}
.qb2-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin-bottom:clamp(18px,2.6vw,30px)}
.qb2-eb{display:inline-flex;align-items:center;gap:10px;font:600 12px "JetBrains Mono",monospace;letter-spacing:.16em;text-transform:uppercase;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:7px 14px;border-radius:999px;backdrop-filter:blur(6px)}
.qb2-eb i{width:8px;height:8px;border-radius:50%;background:#ffd84d;box-shadow:0 0 0 4px rgba(255,216,77,.3);animation:qb2Pulse 2s infinite}
@keyframes qb2Pulse{50%{box-shadow:0 0 0 8px rgba(255,216,77,0)}}
.qb2-chips{display:flex;flex-wrap:wrap;gap:8px}
.qb2-chip{height:34px;padding:0 14px;border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);color:#fff;font:600 13px "Plus Jakarta Sans",Inter,sans-serif;cursor:pointer;transition:background .2s}
.qb2-chip:hover{background:rgba(255,255,255,.2)}
.qb2-chip.on{background:#fff;color:#141228;border-color:#fff}
.qb2-q{margin:0;max-width:980px;font:400 clamp(28px,3.8vw,52px)/1.12 "Instrument Serif",Georgia,serif;font-style:italic;letter-spacing:-.01em;text-shadow:0 2px 18px rgba(0,0,0,.18);transition:opacity .24s,transform .24s}
.qb2-foot{display:flex;align-items:center;gap:14px;margin-top:clamp(20px,2.8vw,34px);flex-wrap:wrap}
.qb2-av{flex:none;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#141228;font:800 18px "Plus Jakarta Sans",sans-serif;box-shadow:0 0 0 4px rgba(255,255,255,.25)}
.qb2-who-w{display:flex;flex-direction:column;min-width:0;transition:opacity .24s}
.qb2-who{font:800 19px "Plus Jakarta Sans",sans-serif}
.qb2-role{font-size:14px;opacity:.85}
.qb2-ctl{margin-left:auto;display:flex;align-items:center;gap:10px}
.qb2-btn{width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.45);background:rgba(255,255,255,.12);color:#fff;display:grid;place-items:center;cursor:pointer;transition:background .2s,transform .2s}
.qb2-btn:hover,.qb2-btn:focus-visible{background:#fff;color:#141228;transform:translateY(-1px)}
.qb2-n{font:600 13px "JetBrains Mono",monospace;min-width:54px;text-align:center}
.qb2-bar{position:absolute;left:0;right:0;bottom:0;height:4px;background:rgba(255,255,255,.18)}
.qb2-bar i{display:block;height:100%;width:100%;transform-origin:left;transform:scaleX(0);background:#ffd84d;animation:qbBar 9000ms linear forwards}
.qb2-out .qb2-q,.qb2-out .qb2-who-w{opacity:0;transform:translateY(6px)}
@media (max-width:700px){.qb2-ctl{margin-left:0;width:100%;justify-content:space-between}.qb2-top{flex-direction:column;align-items:flex-start}}
@media (prefers-reduced-motion:reduce){.qb2-eb i{animation:none}.qb2-bar{display:none}}
"""

def main():
    open(os.path.join(SITE, "assets", "quotes.js"), "w", encoding="utf-8").write(JS)
    css_p = os.path.join(SITE, "assets", "site.css")
    if ".qb2-card{" not in open(css_p, encoding="utf-8").read():
        open(css_p, "a", encoding="utf-8").write(CSS)
    n = 0
    for p in glob.glob(os.path.join(SITE, "*.html")):
        h = open(p, encoding="utf-8").read(); o = h
        h = re.sub(r'<section class="qband".*?</section>\n?', lambda _m: SECTION, h, count=1, flags=re.S)
        h = re.sub(r'<section class="qb2".*?</section>\n?', lambda _m: SECTION, h, count=1, flags=re.S)
        h = re.sub(r'/assets/quotes\.js\?v=[0-9a-z]+', '/assets/quotes.js?v=20261103q2', h)
        if h != o: open(p, "w", encoding="utf-8").write(h); n += 1
    print("pages", n, "quotes", len(Q))

if __name__ == "__main__":
    main()
