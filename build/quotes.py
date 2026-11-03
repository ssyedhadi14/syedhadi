# Created by: Claude
# Date: 2026-11-03
# Purpose: Sitewide "Growth thinking" quote band above the footer. Rotating quotes on business growth from
#          well documented thinkers, each with its source and a one line way to apply it in GTM work.
# Owner: Syed Hadi
#
# Only quotes with a traceable source belong here. Popular misattributions (for example "what gets measured
# gets managed" for Drucker) are left out on purpose.
import html as _h
import json
import re
import zlib

QUOTES = [
    ("There is only one valid definition of business purpose: to create a customer.", "Peter Drucker", "The Practice of Management, 1954",
     "Every GTM plan starts with who buys first and why, before any channel."),
    ("The essence of strategy is choosing what not to do.", "Michael Porter", "What Is Strategy?, Harvard Business Review, 1996",
     "Drop the segment you serve worst before you add a new one."),
    ("Price is what you pay. Value is what you get.", "Warren Buffett", "Berkshire Hathaway shareholder letter, 2008",
     "Sell the outcome in the buyer's own numbers, then show the price."),
    ("Show me the incentive and I will show you the outcome.", "Charlie Munger", "Berkshire Hathaway vice chairman",
     "Partner programs grow when the margin lands with the person who sells."),
    ("We are stubborn on vision. We are flexible on details.", "Jeff Bezos", "Amazon founder",
     "Hold the ICP and the promise steady. Test the message every week."),
    ("The aim of marketing is to make selling superfluous.", "Peter Drucker", "Management: Tasks, Responsibilities, Practices, 1973",
     "Content should answer the objection before the sales call has to."),
    ("Supreme excellence consists in breaking the enemy's resistance without fighting.", "Sun Tzu", "The Art of War, Giles translation, 1910",
     "Own the category so buyers never ask for a bake off."),
    ("The division of labour is limited by the extent of the market.", "Adam Smith", "The Wealth of Nations, 1776",
     "Specialise the team only once the market is big enough to feed each role."),
    ("If you are not embarrassed by the first version of your product, you've launched too late.", "Reid Hoffman", "LinkedIn cofounder",
     "Launch the pilot offer this month and refine it with real deals."),
    ("Real artists ship.", "Steve Jobs", "To the Macintosh team, 1983",
     "A shipped campaign teaches more than a perfect plan in a doc."),
    ("Only the paranoid survive.", "Andy Grove", "Intel, book of the same name, 1996",
     "Watch the competitor that is cheaper and good enough, not the loudest one."),
    ("Chance favors only the prepared mind.", "Louis Pasteur", "Lecture at the University of Lille, 1854",
     "Research the account before the trigger event, so you are first when it lands."),
    ("Your most unhappy customers are your greatest source of learning.", "Bill Gates", "Business @ the Speed of Thought, 1999",
     "Read every lost deal note before you write the next battlecard."),
    ("A journey of a thousand miles begins with a single step.", "Lao Tzu", "Tao Te Ching, chapter 64",
     "Book one partner meeting today. Pipeline compounds from there."),
]
TINTS = 6
Q = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M20 12c-7 2-12 8-12 16v8h12V24h-6c0-5 3-8 8-9zm20 0c-7 2-12 8-12 16v8h12V24h-6c0-5 3-8 8-9z"/></svg>'


def initials(name):
    parts = [w for w in re.split(r"\s+", name) if w and w[0].isalpha()]
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


ARROW_L = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>'
ARROW_R = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>'


def block(seed):
    i = zlib.crc32(seed.encode()) % len(QUOTES)
    q, who, src, tip = QUOTES[i]
    e = _h.escape
    return (f'<section class="qband" aria-label="Growth thinking: a quote on business growth">'
            f'<div class="wrap"><figure class="qb-card qt{i % TINTS + 1}" data-i="{i}">'
            f'<span class="qb-av" aria-hidden="true">{initials(who)}</span>'
            f'<div class="qb-main"><span class="qb-eb">Growth thinking <span class="qb-n">{i + 1:02d}/{len(QUOTES):02d}</span></span>'
            f'<blockquote class="qb-q">&ldquo;{e(q)}&rdquo;</blockquote>'
            f'<figcaption class="qb-cap"><b class="qb-who">{e(who)}</b><span class="qb-src">{e(src)}</span></figcaption>'
            f'<p class="qb-apply"><span>Apply it</span> <em class="qb-tip">{e(tip)}</em></p></div>'
            f'<div class="qb-ctl"><button type="button" class="qb-btn" data-d="-1" aria-label="Previous quote">{ARROW_L}</button>'
            f'<span class="qb-bar" aria-hidden="true"><i></i></span>'
            f'<button type="button" class="qb-btn" data-d="1" aria-label="Next quote">{ARROW_R}</button></div>'
            f'</figure></div></section>')


def inject(html, name, ver):
    if '<footer class="site-foot">' not in html:
        return html
    html = re.sub(r'<section class="qband".*?</section>\s*', '', html, flags=re.S)
    html = html.replace('<footer class="site-foot">', block(name) + '\n<footer class="site-foot">', 1)
    if '/assets/quotes.js' not in html:
        html = html.replace('</body>', f'<script src="/assets/quotes.js?v={ver}" defer></script>\n</body>', 1)
    return html


JS = r'''/* Created by: Claude | Date: 2026-11-03 | Purpose: rotate the Growth thinking quote band | Owner: Syed Hadi */
(function () {
  var Q = __QUOTES__, T = __TINTS__, MS = 8000;
  function ini(n) { var p = n.split(/\s+/).filter(function (w) { return /^[A-Za-z]/.test(w); }); return ((p[0] || ' ')[0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase(); }
  function init(card) {
    var i = +card.getAttribute('data-i') || 0, timer = null, paused = false, $ = function (s) { return card.querySelector(s); };
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function set(n) {
      i = (n + Q.length) % Q.length; var q = Q[i];
      card.classList.add('qb-out');
      setTimeout(function () {
        $('.qb-q').textContent = '\u201C' + q[0] + '\u201D'; $('.qb-av').textContent = ini(q[1]); $('.qb-who').textContent = q[1]; $('.qb-src').textContent = q[2]; $('.qb-tip').textContent = q[3];
        $('.qb-n').textContent = ('0' + (i + 1)).slice(-2) + '/' + ('0' + Q.length).slice(-2);
        card.className = card.className.replace(/\bqt\d\b/, 'qt' + (i % T + 1));
        card.classList.remove('qb-out'); restartBar();
      }, reduce ? 0 : 260);
    }
    function restartBar() { var b = $('.qb-bar i'); if (!b) return; b.style.animation = 'none'; void b.offsetWidth; b.style.animation = ''; b.style.animationDuration = MS + 'ms'; b.style.animationPlayState = paused ? 'paused' : 'running'; }
    function tick() { clearInterval(timer); timer = setInterval(function () { if (!paused && !document.hidden) set(i + 1); }, MS); }
    function pause(p) { paused = p; var b = $('.qb-bar i'); if (b) b.style.animationPlayState = p ? 'paused' : 'running'; }
    card.addEventListener('mouseenter', function () { pause(true); });
    card.addEventListener('mouseleave', function () { pause(false); });
    card.addEventListener('focusin', function () { pause(true); });
    card.addEventListener('focusout', function () { pause(false); });
    [].forEach.call(card.querySelectorAll('.qb-btn'), function (b) { b.addEventListener('click', function () { set(i + +b.getAttribute('data-d')); tick(); }); });
    var sx = null;
    card.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    card.addEventListener('touchend', function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) { set(i + (dx < 0 ? 1 : -1)); tick(); } sx = null; });
    restartBar(); tick();
  }
  function go() { [].forEach.call(document.querySelectorAll('.qb-card'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
'''


def js():
    return JS.replace('__QUOTES__', json.dumps(QUOTES, ensure_ascii=False)).replace('__TINTS__', str(TINTS))


CSS = r'''
/* ===== 2026-11-03 Growth thinking quote band (compact, above the footer, sitewide) ===== */
.qband{padding:6px 0 44px}
.qb-card{--qc:#5b3df5;--qs:#efebff;position:relative;margin:0;display:grid;grid-template-columns:auto 1fr auto;gap:18px 22px;align-items:center;padding:20px 24px;border-radius:20px;border:1px solid var(--line);background:linear-gradient(110deg,var(--qs) 0%,var(--card) 70%);box-shadow:0 12px 34px rgba(28,16,80,.07);transition:background .5s}
.qt1{--qc:#5b3df5;--qs:#efebff}.qt2{--qc:#0f766e;--qs:#ddf6f1}.qt3{--qc:#b9382f;--qs:#fde8e4}.qt4{--qc:#92400e;--qs:#fdf0d5}.qt5{--qc:#1d4ed8;--qs:#e3eefc}.qt6{--qc:#9d2a78;--qs:#fbe4f2}
[data-theme=dark] .qt1{--qc:#a592ff;--qs:#211a45}[data-theme=dark] .qt2{--qc:#5eead4;--qs:#0f2d2a}[data-theme=dark] .qt3{--qc:#fb9a8f;--qs:#33181a}[data-theme=dark] .qt4{--qc:#f6c46b;--qs:#30230f}[data-theme=dark] .qt5{--qc:#8cc4ff;--qs:#132440}[data-theme=dark] .qt6{--qc:#f39bd6;--qs:#311530}
[data-theme=dark] .qb-card{box-shadow:none}
.qb-av{position:relative;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;font:800 18px "Plus Jakarta Sans",Inter,sans-serif;letter-spacing:.02em;color:#fff;background:var(--qc);box-shadow:0 0 0 4px var(--card),0 0 0 5px var(--line);align-self:start}
[data-theme=dark] .qb-av{color:#0b0a12}
.qb-av::after{content:"\201C";position:absolute;right:-6px;bottom:-10px;width:22px;height:22px;border-radius:50%;background:var(--card);border:1px solid var(--line);color:var(--qc);font:400 22px/30px "Instrument Serif",Georgia,serif;text-align:center}
.qb-main{min-width:0;transition:opacity .26s,transform .26s}
.qb-out .qb-main{opacity:0;transform:translateY(5px)}
.qb-eb{display:flex;gap:8px;align-items:center;font:600 11px "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--qc)}
.qb-n{color:var(--ink-3);letter-spacing:.06em}
.qb-q{margin:4px 0 0;font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400;font-size:clamp(20px,2.1vw,26px);line-height:1.22;color:var(--ink)}
.qb-cap{margin-top:6px;display:flex;flex-wrap:wrap;gap:2px 8px;align-items:baseline;font-size:13px}
.qb-who{font:700 14px "Plus Jakarta Sans",Inter,sans-serif;color:var(--ink)}
.qb-src{color:var(--ink-3)}
.qb-src::before{content:"\00B7";margin-right:8px;color:var(--ink-3)}
.qb-apply{margin:8px 0 0;font-size:14px;line-height:1.45;color:var(--ink-2)}
.qb-apply span{font:700 11px "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--qc);margin-right:6px}
.qb-apply em{font-style:normal}
.qb-ctl{display:flex;align-items:center;gap:8px;align-self:center}
.qb-btn{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);display:grid;place-items:center;cursor:pointer;flex:none;transition:border-color .2s,color .2s}
.qb-btn:hover,.qb-btn:focus-visible{border-color:var(--qc);color:var(--qc)}
.qb-btn svg{width:16px;height:16px}
.qb-bar{width:64px;height:4px;border-radius:99px;background:var(--line);overflow:hidden}
.qb-bar i{display:block;height:100%;width:100%;transform-origin:left;transform:scaleX(0);background:var(--qc);animation:qbBar 8000ms linear forwards}
@keyframes qbBar{to{transform:scaleX(1)}}
@media (prefers-reduced-motion:reduce){.qb-main{transition:none}}
@media (max-width:760px){.qb-cap{flex-direction:column;gap:0}.qb-src::before{display:none}.qb-card{grid-template-columns:auto 1fr;padding:18px}.qb-ctl{grid-column:1/-1;justify-content:flex-end}.qb-bar{flex:1}.qb-av{width:44px;height:44px;font-size:15px}}
'''
