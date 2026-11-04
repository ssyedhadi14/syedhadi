#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Put the branded covers to work across syedcreates.com.
#          1. og:image, twitter:image and schema image point at each page's own cover
#          2. Stock photo covers on cards that link to a site page become that page's cover
#          3. Insights, blog and related reading cards get a cover thumbnail
#          4. Articles get the cover under the byline
#          Idempotent: safe to run again after render.py.
# Owner: Syed Hadi
import glob
import html as htmllib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "site"))
sys.path.insert(0, HERE)
from config import COVERS  # noqa: E402

SITE = "https://syedcreates.com"
CSS_VER_OLD = re.compile(r"site\.css\?v=[0-9a-z]+")
CSS_VER = "site.css?v=20261104c"
CSS = """
/* 2026-11-03 branded covers on cards and articles */
.ins-card .cv-thumb,.bf-card .cv-thumb,.lp-box .cv-thumb,.cv-thumb{display:block;flex:none;aspect-ratio:16/10;overflow:hidden;border-radius:12px;border:1px solid var(--line);background:#ece7ff;margin-bottom:6px}
.cv-thumb img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s var(--ease)}
.ins-card:hover .cv-thumb img,.bf-card:hover .cv-thumb img,.lp-box:hover .cv-thumb img{transform:scale(1.03)}
.bf-card:first-child .cv-thumb{display:none}
.pt-cover{margin:6px 0 28px;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:#ece7ff}
.pt-cover img{display:block;width:100%;height:auto}
"""


def slug_of(href):
    s = href.replace(SITE, "").split("#")[0].split("?")[0].strip("/").replace(".html", "")
    return s or "index"


def alt_of(slug):
    t, a, _tag, _m = COVERS[slug]
    return htmllib.escape(f"{t} {a}")


def card_src(slug):
    return f"/img/covers/{slug}.jpg"


def thumb(slug):
    return (f'<span class="cv-thumb"><img src="{card_src(slug)}" alt="" width="1200" height="750" '
            f'loading="lazy" decoding="async"></span>')


IMG_RE = re.compile(r'<img\b[^>]*src="https://images\.unsplash\.com[^"]*"[^>]*>')


def swap_stock(h):
    """Replace stock photos that sit inside a link to a site page with that page's cover."""
    out, pos, n = [], 0, 0
    for m in IMG_RE.finditer(h):
        pre = h[:m.start()]
        a_open = list(re.finditer(r'''<a\b[^>]*href=["']([^"']*)["']''', pre[-1500:]))
        closed = pre[-1500:].rfind("</a>")
        if not a_open or a_open[-1].start() < closed:
            continue
        href = a_open[-1].group(1)
        if href.startswith("http") and not href.startswith(SITE):
            continue
        slug = slug_of(href)
        if slug not in COVERS:
            continue
        tag = m.group(0)
        tag = re.sub(r'\s(srcset|sizes)="[^"]*"', "", tag)
        tag = re.sub(r'src="[^"]*"', f'src="{card_src(slug)}"', tag)
        tag = re.sub(r'alt="[^"]*"', f'alt="{alt_of(slug)}"', tag)
        out.append(h[pos:m.start()])
        out.append(tag)
        pos = m.end()
        n += 1
    out.append(h[pos:])
    return "".join(out), n


def add_thumbs(h):
    def rep(m):
        open_tag, href = m.group(1), m.group(3)
        slug = slug_of(href)
        if slug not in COVERS or href.startswith("http") and not href.startswith(SITE):
            return m.group(0)
        return open_tag + thumb(slug)
    pat = re.compile(r"""(<a\s+class=(['"])(?:ins-card|bf-card|lp-box)(?: reveal)?\2[^>]*href=['"]([^'"]+)['"][^>]*>)(?!<span class="cv-thumb")""")
    return pat.sub(rep, h)


def wide_fix(h):
    """Slots wider than 1.7:1 get the 1200x630 cover so nothing is cropped."""
    def rep(m):
        t = m.group(0)
        w = re.search(r'width="(\d+)"', t)
        hh = re.search(r'height="(\d+)"', t)
        if w and hh and int(w.group(1)) / int(hh.group(1)) > 1.7:
            return t.replace('src="/img/covers/', 'src="/img/covers/og/')
        return t
    return re.sub(r'<img[^>]*src="/img/covers/(?!og/)[^"]+"[^>]*>', rep, h)


def process(path):
    name = os.path.basename(path)
    slug = "index" if name == "index.html" else name[:-5]
    h = open(path, encoding="utf-8").read()
    orig = h
    if slug in COVERS:
        og = f"{SITE}/img/covers/og/{slug}.jpg"
        h = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + og, h)
        h = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r"\g<1>" + og, h)
        h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r"\g<1>" + alt_of(slug), h)

        def ld(m):
            try:
                j = json.loads(m.group(2))
            except Exception:
                return m.group(0)
            nodes = j["@graph"] if isinstance(j, dict) and "@graph" in j else [j]
            for n in nodes:
                if isinstance(n, dict) and n.get("@type") in ("BlogPosting", "Article"):
                    n["image"] = {"@type": "ImageObject", "url": og, "width": 1200, "height": 630}
            return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        h = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, h, flags=re.S)

        if 'class="pt-meta"' in h and 'class="pt-cover"' not in h and 'class="hero-cv"' not in h:
            h = re.sub(r'(<div class="pt-meta">.*?</div>)',
                       lambda m: m.group(1) + f'\n    <figure class="pt-cover"><img src="{card_src(slug)}" alt="{alt_of(slug)}" '
                                              f'width="1200" height="750" fetchpriority="high" decoding="async"></figure>',
                       h, count=1, flags=re.S)
    h, _n = swap_stock(h)
    h = add_thumbs(h)
    h = wide_fix(h)
    if h != orig:
        h = CSS_VER_OLD.sub(CSS_VER, h)
        open(path, "w", encoding="utf-8").write(h)
        return True
    return False


def main():
    css_path = os.path.join(SITE_DIR, "assets", "site.css")
    css = open(css_path, encoding="utf-8").read()
    if ".cv-thumb{" not in css:
        open(css_path, "a", encoding="utf-8").write(CSS)
    changed = [p for p in sorted(glob.glob(os.path.join(SITE_DIR, "*.html"))) if process(p)]
    for p in glob.glob(os.path.join(SITE_DIR, "*.html")):
        t = open(p, encoding="utf-8").read()
        t2 = CSS_VER_OLD.sub(CSS_VER, t)
        if t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
    print(f"pages changed: {len(changed)}")


if __name__ == "__main__":
    main()
