# Created by: Claude Cowork
# Date: 2026-11-17
# Purpose: Sitewide page speed pass for syedcreates.com. Idempotent, safe to rerun
#          after any builder script. Run order:
#            python3 build/perf_optimize.py        (images, fonts, lazy loading, Calendly)
# Owner: Syed Hadi
#
# What it does
#   1. Builds WebP copies of local JPG and PNG images, capped at 2x their largest
#      displayed width (max 1600px), plus an 800px variant for large covers.
#      Originals stay untouched for og:image, JSON-LD and scripts.
#   2. Points <img> tags at the WebP files and adds srcset for large covers.
#   3. Adds loading="lazy" decoding="async" to images below the hero.
#   4. Self hosts Inter and JetBrains Mono, removes the Google Fonts request,
#      preloads the two fonts the first screen needs.
#   5. Loads the homepage Calendly embed only when it nears the viewport.
#   6. Appends a render tweak to site.css: hero entrances slide without fading
#      from zero so the largest element paints at once. Bumps the CSS version.
#      (content-visibility on below fold sections was tested and dropped: wrong
#      height estimates made long pages like /blog jump while scrolling.)
#   Tested against a critical CSS split (inline CSS, async stylesheet): it painted
#   0.3s sooner on a cold visit but added main thread work and 16KB per page, so a
#   single cached stylesheet won on Lighthouse and on repeat page views.

import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
FONT_SRC = Path("/home/claude/perf/node_modules/@fontsource")
FONT_DIR = SITE / "assets" / "fonts" / "web"
MAX_W = 1600
MOBILE_W = 800
QUALITY = 80

IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
LOCAL = re.compile(r'^(?:https://syedcreates\.com)?/?(img/[^"?#]+\.(?:jpe?g|png))$', re.I)


def attr(tag, name):
    m = re.search(r'\s%s="([^"]*)"' % name, tag)
    return m.group(1) if m else None


def html_files():
    return sorted(p for p in SITE.rglob("*.html") if not p.name.startswith("x-") and "/x-" not in str(p))


# ---------- 1. images ----------
def plan_images(files):
    """Map image path -> largest displayed width (None means unknown, use MAX_W)."""
    need = {}
    for f in files:
        for tag in IMG_TAG.findall(f.read_text(encoding="utf-8")):
            src = attr(tag, "src") or ""
            m = LOCAL.match(src)
            if not m:
                continue
            rel = m.group(1)
            w = attr(tag, "width")
            w = int(w) if w and w.isdigit() else None
            prev = need.get(rel, 0)
            need[rel] = None if (w is None or prev is None) else max(prev, w)
    return need


def make_webp(rel, disp_w):
    src = SITE / rel
    if not src.exists():
        return None
    out = src.with_suffix(".webp")
    small = src.with_name(src.stem + "-800.webp")
    try:
        with Image.open(src) as im:
            ow, oh = im.size
            target = MAX_W if disp_w is None else min(MAX_W, max(disp_w * 2, 64))
            target = min(target, ow)
            fresh = not out.exists() or out.stat().st_mtime < src.stat().st_mtime
            if fresh:
                img = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
                if target < ow:
                    img = img.resize((target, round(oh * target / ow)), Image.LANCZOS)
                img.save(out, "WEBP", quality=QUALITY, method=6)
            has_small = False
            if target > 1000:
                has_small = True
                if not small.exists() or small.stat().st_mtime < src.stat().st_mtime:
                    img = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
                    img = img.resize((MOBILE_W, round(oh * MOBILE_W / ow)), Image.LANCZOS)
                    img.save(small, "WEBP", quality=QUALITY, method=6)
            # keep the WebP only when it actually saves bytes
            if out.stat().st_size >= src.stat().st_size and target == ow:
                out.unlink()
                if small.exists():
                    small.unlink()
                return None
            return {"w": target, "small": has_small}
    except Exception as e:  # unreadable or odd image: leave the original in place
        print(f"  skip {rel}: {e}", file=sys.stderr)
        return None


def _disp(tag):
    w = attr(tag, "width")
    return min(int(w), 860) if w and w.isdigit() else 860


def rewrite_img(tag, made, after_hero):
    src = attr(tag, "src") or ""
    m = LOCAL.match(src)
    if m and m.group(1) in made and made[m.group(1)]:
        info = made[m.group(1)]
        prefix = src[: len(src) - len(m.group(1))]
        new = prefix + re.sub(r"\.(jpe?g|png)$", ".webp", m.group(1), flags=re.I)
        tag = tag.replace(f'src="{src}"', f'src="{new}"', 1)
        if info["small"] and "srcset=" not in tag:
            sm = new[:-5] + "-800.webp"
            tag = tag.replace(f'src="{new}"', f'src="{new}" srcset="{sm} 800w, {new} {info["w"]}w" sizes="(max-width: 860px) 100vw, %dpx"' % _disp(tag), 1)
    if after_hero and "fetchpriority" not in tag:
        if "loading=" not in tag:
            tag = tag.replace("<img", '<img loading="lazy"', 1)
        if "decoding=" not in tag:
            tag = tag.replace("<img", '<img decoding="async"', 1)
    return tag


def images(files):
    need = plan_images(files)
    made = {}
    for rel, w in need.items():
        made[rel] = make_webp(rel, w)
    changed = 0
    for f in files:
        h = f.read_text(encoding="utf-8")
        nav_end = h.find("</nav>")
        out, pos, seen_hero = [], 0, False
        for m in IMG_TAG.finditer(h):
            out.append(h[pos:m.start()])
            tag = m.group(0)
            after = m.start() > nav_end >= 0
            hero = after and not seen_hero
            if hero:
                seen_hero = True
            out.append(rewrite_img(tag, made, after and not hero))
            pos = m.end()
        out.append(h[pos:])
        nh = "".join(out)
        if nh != h:
            f.write_text(nh, encoding="utf-8")
            changed += 1
    n = sum(1 for v in made.values() if v)
    print(f"images: {n} WebP files in use, {changed} pages updated")


# ---------- 2. fonts ----------
FONTS = [
    ("Inter", 400, "inter/files/inter-latin-400-normal.woff2"),
    ("Inter", 500, "inter/files/inter-latin-500-normal.woff2"),
    ("Inter", 600, "inter/files/inter-latin-600-normal.woff2"),
    ("Inter", 700, "inter/files/inter-latin-700-normal.woff2"),
    ("JetBrains Mono", 500, "jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2"),
]
GF = re.compile(r'\s*<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', re.I)
PRELOAD = (
    '<link rel="preload" href="/assets/fonts/web/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
    '<link rel="preload" href="/assets/fonts/web/plus-jakarta-sans-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>'
)


def fonts(files):
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for _, _, rel in FONTS:
        dst = FONT_DIR / Path(rel).name
        if not dst.exists():
            shutil.copy(FONT_SRC / rel, dst)
    css_p = SITE / "assets" / "site.css"
    css = css_p.read_text(encoding="utf-8")
    faces = "".join(
        '@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;src:url(/assets/fonts/web/%s) format("woff2")}'
        % (fam, wt, Path(rel).name)
        for fam, wt, rel in FONTS
    )
    if "inter-latin-400-normal.woff2" not in css:
        css_p.write_text(faces + css, encoding="utf-8")
    changed = 0
    for f in files:
        h = f.read_text(encoding="utf-8")
        nh = GF.sub("", h)
        if "plus-jakarta-sans-latin-800-normal.woff2\" as=\"font\"" not in nh:
            nh = re.sub(r'(<link rel="stylesheet" href="/?assets/site\.css)', PRELOAD + r"\1", nh, count=1)
        if nh != h:
            f.write_text(nh, encoding="utf-8")
            changed += 1
    print(f"fonts: self hosted, {changed} pages updated")


# ---------- 3. Calendly on the homepage ----------
CAL_OLD = '<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>'
CAL_NEW = (
    "<script>(function(){var w=document.querySelector('.calendly-inline-widget');if(!w)return;"
    "function go(){if(go.d)return;go.d=1;var s=document.createElement('script');"
    "s.src='https://assets.calendly.com/assets/external/widget.js';s.async=true;document.body.appendChild(s)}"
    "if('IntersectionObserver'in window){var o=new IntersectionObserver(function(e){if(e[0].isIntersecting){o.disconnect();go()}},{rootMargin:'800px'});o.observe(w)}else go()})();</script>"
)


def calendly():
    p = SITE / "index.html"
    h = p.read_text(encoding="utf-8")
    if CAL_OLD in h:
        p.write_text(h.replace(CAL_OLD, CAL_NEW), encoding="utf-8")
        print("calendly: homepage embed now loads near the viewport")


CSS_VERSION = "20261118c"
CSS_TAIL = """
/* perf 2026-11-17: hero entrance slides without fading from 0, so it paints at once */
@keyframes riseT{from{transform:translateY(14px)}to{transform:none}}
@keyframes fadeinS{from{opacity:.35}to{opacity:1}}
.hero .pill,.hero h1,.hero .lede,.hero-cta,.hero .stats,.hero .socials,.page-hero .crumbs,.page-hero h1,.page-hero p,.hero-cv{animation-name:riseT}
.portrait{animation-name:fadeinS}
"""


def css_and_version(files):
    css_p = SITE / "assets" / "site.css"
    css = css_p.read_text(encoding="utf-8")
    if "perf 2026-11-17: hero entrance" not in css:
        css_p.write_text(css.rstrip("\n") + "\n" + CSS_TAIL.lstrip("\n"), encoding="utf-8")
    n = 0
    for f in files:
        h = f.read_text(encoding="utf-8")
        nh = re.sub(r"site\.css\?v=[0-9a-z]+", "site.css?v=" + CSS_VERSION, h)
        if nh != h:
            f.write_text(nh, encoding="utf-8")
            n += 1
    for b in (ROOT / "build").glob("*.py"):
        t = b.read_text(encoding="utf-8")
        nt = re.sub(r"site\.css\?v=[0-9]{8}[a-z]", "site.css?v=" + CSS_VERSION, t)
        if nt != t and b.name != "perf_optimize.py":
            b.write_text(nt, encoding="utf-8")
    print(f"css: render tweaks in place, version {CSS_VERSION} on {n} pages")


if __name__ == "__main__":
    files = html_files()
    fonts(files)
    images(files)
    calendly()
    css_and_version(files)
