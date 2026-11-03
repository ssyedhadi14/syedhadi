#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Hero covers and blog search for syedcreates.com.
#          1. Every hero shows the page's own cover at top right (same image as its cards)
#          2. Mega menu "What to expect" cards show the linked page's cover
#          3. /blog gets a search bar and type filters, and loses 21 duplicate tools sections
#          Idempotent. Run after render.py and apply.py.
# Owner: Syed Hadi
import glob
import html as htmllib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "site"))
sys.path.insert(0, HERE)
from config import COVERS  # noqa: E402

CSS_VER_OLD = re.compile(r"site\.css\?v=[0-9a-z]+")
CSS_VER = "site.css?v=20261103k"
SKIP = {"404", "index", "skill-pack", "adventure"}  # custom heroes stay as designed

CSS = """
/* 2026-11-03 hero covers */
.ph-cv .wrap{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:48px;align-items:center}
.ph-cv .ph-copy{min-width:0}
.ph-cv h1{font-size:clamp(38px,5vw,68px)}
.hero-cv{margin:0;border-radius:20px;overflow:hidden;border:1px solid var(--line);background:#ece7ff;box-shadow:0 26px 60px rgba(30,16,90,.16);transform:rotate(1.2deg);animation:rise .7s var(--ease) both}
.hero-cv img{display:block;width:100%;height:auto;aspect-ratio:16/10}
.bx-hero.ph-cv .bx-hero-in{max-width:1200px;text-align:left}
.bx-hero.ph-cv .wrap:not(.bx-hero-in){display:block}
.bx-hero.ph-cv .crumbs{justify-content:flex-start}
.bx-hero.ph-cv .bx-ctas{justify-content:flex-start}
.bx-hero.ph-cv .bx-lede{margin-left:0}
.has-cv{aspect-ratio:16/10!important;height:auto!important;background:#ece7ff}
.has-cv img{width:100%;height:100%;object-fit:cover}
@media (max-width:900px){.ph-cv .wrap{grid-template-columns:1fr;gap:28px}.hero-cv{max-width:560px;transform:none}}
/* blog search */
.bs-bar{position:sticky;top:72px;z-index:20;display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 16px;margin:0 0 22px;border:1px solid var(--line);border-radius:16px;background:var(--card);box-shadow:0 10px 30px rgba(30,16,90,.08)}
.bs-search{flex:1 1 280px;display:flex;align-items:center;gap:10px;padding:0 14px;height:46px;border:1px solid var(--line);border-radius:12px;background:var(--bg)}
.bs-search svg{flex:none;color:var(--ink-3)}
.bs-search input{flex:1;border:0;outline:0;background:transparent;font:500 15px "Plus Jakarta Sans",Inter,sans-serif;color:var(--ink)}
.bs-chips{display:flex;flex-wrap:wrap;gap:8px}
.bs-chip{height:38px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);font:600 13.5px "Plus Jakarta Sans",Inter,sans-serif;color:var(--ink-2);cursor:pointer}
.bs-chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.bs-count{font:500 12px "JetBrains Mono",monospace;color:var(--ink-3);letter-spacing:.06em;text-transform:uppercase}
.bs-empty{padding:40px;text-align:center;color:var(--ink-2);border:1px dashed var(--line);border-radius:16px}
.bf-card[hidden],.mpost[hidden],.bs-hide{display:none!important}
@media (max-width:700px){.bs-bar{top:64px}}
"""


def cover_fig(slug):
    t, a, _tag, _m = COVERS[slug]
    alt = htmllib.escape(f"{t} {a}")
    return (f'<figure class="hero-cv"><img src="/img/covers/{slug}.jpg" alt="{alt}" width="1200" height="750" '
            f'fetchpriority="high" decoding="async"></figure>')


def hero(h, slug):
    if slug in SKIP or slug not in COVERS or 'class="hero-cv"' in h or "has-cv" in h:
        return h
    # A. plain page hero: <header class="page-hero"><div class="wrap"> ... </div></header>
    m = re.search(r'<header class="page-hero((?: [a-z-]+)*)"( [^>]*)?>\s*<div class="wrap">(.*?)</div>\s*</header>', h, re.S)
    if m and "<img" not in m.group(3):
        new = (f'<header class="page-hero{m.group(1)} ph-cv"{m.group(2) or ""}>\n  <div class="wrap"><div class="ph-copy">{m.group(3)}</div>'
               f'\n    {cover_fig(slug)}\n  </div>\n</header>')
        h = h[:m.start()] + new + h[m.end():]
        # the article cover moves up into the hero, so drop the copy under the byline
        h = re.sub(r'\s*<figure class="pt-cover">.*?</figure>', "", h, count=1, flags=re.S)
        return h
    # B. in a box hero: centered copy becomes copy left, cover right
    m = re.search(r'<header class="bx-hero">\s*<div class="wrap bx-hero-in">(.*?)</div>(\s*<div class="wrap">)', h, re.S)
    if m:
        inner = m.group(1)
        new = (f'<header class="bx-hero ph-cv">\n  <div class="wrap bx-hero-in"><div class="ph-copy">{inner}</div>'
               f'\n    {cover_fig(slug)}\n  </div>{m.group(2)}')
        return h[:m.start()] + new + h[m.end():]
    # C. heroes that already have art on the right: swap the art for the cover
    hm = re.search(r'<header class="page-hero [^"]+">.*?</header>', h, re.S)
    if hm:
        block = hm.group(0)
        im = re.search(r'<div class="([a-z-]*art[a-z-]*)"([^>]*)>\s*<img[^>]*>', block)
        if im:
            t, a, _tag, _m = COVERS[slug]
            img = (f'<div class="{im.group(1)} has-cv"{im.group(2)}><img src="/img/covers/{slug}.jpg" '
                   f'alt="{htmllib.escape(t + " " + a)}" width="1200" height="750" fetchpriority="high" decoding="async">')
            block2 = block[:im.start()] + img + block[im.end():]
            return h[:hm.start()] + block2 + h[hm.end():]
    return h


def menu(h):
    """Mega menu right hand cards: show the linked page's cover."""
    def rep(m):
        href = m.group(1).split("#")[0].strip("/") or "index"
        if href not in COVERS:
            return m.group(0)
        t, a, _tag, _m = COVERS[href]
        return re.sub(r'<img src="[^"]*" alt="[^"]*"',
                      f'<img src="/img/covers/{href}.jpg" alt="{htmllib.escape(t + " " + a)}"', m.group(0), count=1)
    return re.sub(r'<a class="mw-card mw-card2" href="([^"]+)">.*?</a>', rep, h, flags=re.S)


BLOG_BAR = """<div class="bs-bar" id="bsBar" role="search">
      <label class="bs-search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="bsQ" type="search" placeholder="Search guides, calculators and posts" aria-label="Search the blog" autocomplete="off"></label>
      <div class="bs-chips" role="group" aria-label="Filter by type"><button class="bs-chip on" type="button" data-k="all">All</button><button class="bs-chip" type="button" data-k="guide">Guides</button><button class="bs-chip" type="button" data-k="tool">Calculators and tools</button><button class="bs-chip" type="button" data-k="post">Medium posts</button></div>
      <span class="bs-count" id="bsCount"></span>
    </div>
    <p class="bs-empty" id="bsEmpty" hidden>Nothing matches that yet. Try a broader word, or <a href="/schedule-meeting">ask me on a free call</a>.</p>
"""

BLOG_JS = """<script>
(function(){
  var q=document.getElementById('bsQ'),bar=document.getElementById('bsBar');if(!q||!bar)return;
  var kind='all';
  try{var u=new URLSearchParams(location.search);if(u.get('q'))q.value=u.get('q');if(u.get('type'))kind=u.get('type')}catch(e){}
  function apply(){
    var term=q.value.trim().toLowerCase(),shown=0;
    document.querySelectorAll('[data-bs-kind]').forEach(function(c){
      var ok=(kind==='all'||c.getAttribute('data-bs-kind')===kind)&&(!term||c.textContent.toLowerCase().indexOf(term)>-1);
      c.classList.toggle('bs-hide',!ok);if(ok)shown++;
    });
    document.querySelectorAll('[data-bs-sec]').forEach(function(s){
      var any=s.querySelector('[data-bs-kind]:not(.bs-hide)');s.classList.toggle('bs-hide',!any);
    });
    document.getElementById('bsCount').textContent=shown+(shown===1?' result':' results');
    document.getElementById('bsEmpty').hidden=shown>0;
    bar.querySelectorAll('.bs-chip').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-k')===kind)});
  }
  function tagPosts(){document.querySelectorAll('.mpost:not([data-bs-kind])').forEach(function(p){p.setAttribute('data-bs-kind','post')})}
  bar.addEventListener('click',function(e){var b=e.target.closest('.bs-chip');if(!b)return;kind=b.getAttribute('data-k');apply()});
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(apply,120)});
  var g=document.querySelector('[data-medium-blog]');
  if(g&&window.MutationObserver)new MutationObserver(function(){tagPosts();apply()}).observe(g,{childList:true});
  tagPosts();apply();
})();
</script>
"""


def blog(h):
    # 1. drop duplicate "Tools worth bookmarking" sections (ids ending -2 .. -22)
    h = re.sub(r'<section class="bf-sec bf-tools" style="padding-top:0">\s*<div class="wrap">\s*<div class="sec-head[^"]*"[^>]*>'
               r'(?:(?!</section>).)*?id="s-tools-worth-bookmarking-\d+"(?:(?!</section>).)*</section>\s*', "", h, flags=re.S)
    if 'id="bsBar"' in h:
        return h
    # 2. tag cards and sections by type
    h = h.replace('<section class="bf-sec" style="padding-top:36px">', '<section class="bf-sec" style="padding-top:36px" data-bs-sec>', 1)
    h = h.replace('<section class="bf-sec bf-tools" style="padding-top:0">', '<section class="bf-sec bf-tools" style="padding-top:0" data-bs-sec>')
    h = h.replace('<div class="mgrid" data-medium-blog', '<div class="mgrid" data-bs-sec data-medium-blog', 1)

    def tag_sec(sec_html, kind):
        return re.sub(r"<a class='bf-card reveal'", f"<a data-bs-kind='{kind}' class='bf-card reveal'", sec_html)
    parts = re.split(r'(<section class="bf-sec[^"]*"[^>]*data-bs-sec>)', h)
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        kind = "tool" if "bf-tools" in parts[i] else "guide"
        body, sep, rest = parts[i + 1].partition("</section>")
        out.append(parts[i] + tag_sec(body, kind) + sep + rest)
    h = "".join(out)
    # 3. search bar at the top of the first section, script before </main>
    # the bar sits outside the first section so it survives that section being hidden
    first = '<section class="bf-sec" style="padding-top:36px" data-bs-sec>'
    h = h.replace(first, '<div class="wrap" style="padding-top:28px">\n    ' + BLOG_BAR + '</div>\n'
                  '<section class="bf-sec" style="padding-top:8px" data-bs-sec>', 1)
    h = h.replace("</main>", BLOG_JS + "</main>", 1)
    return h


def main():
    css_path = os.path.join(SITE_DIR, "assets", "site.css")
    css = open(css_path, encoding="utf-8").read()
    if ".hero-cv{" not in css:
        open(css_path, "a", encoding="utf-8").write(CSS)
    n = 0
    for p in sorted(glob.glob(os.path.join(SITE_DIR, "*.html"))):
        name = os.path.basename(p)
        slug = "index" if name == "index.html" else name[:-5]
        h = open(p, encoding="utf-8").read()
        h2 = menu(hero(h, slug))
        if slug == "blog":
            h2 = blog(h2)
        h2 = CSS_VER_OLD.sub(CSS_VER, h2)
        if h2 != h:
            open(p, "w", encoding="utf-8").write(h2)
            n += 1
    print(f"pages changed: {n}")


if __name__ == "__main__":
    main()
