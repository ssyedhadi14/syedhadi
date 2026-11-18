# Created by: Claude Cowork
# Date: 2026-11-17 (revised 2026-11-18)
# Purpose: Nav brand uses Syed's photo (avatar) as the logo, sitewide. This
#          undoes the short lived "sh" monogram: it swaps any <svg class="brand-mark">
#          back to the avatar image and removes the monogram CSS. Idempotent.
# Owner: Syed Hadi
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
AVATAR = '<img src="/img/avatar.webp" alt="Syed Hadi" width="40" height="40">'
MARK = re.compile(r'(class="brand">)<svg class="brand-mark".*?</svg>', re.S)


def pages():
    n = 0
    targets = [p for p in SITE.rglob("*.html") if "/x-" not in str(p)] + [ROOT / "build" / "nav_mega.py"]
    for f in targets:
        h = f.read_text(encoding="utf-8")
        nh = MARK.sub(lambda m: m.group(1) + AVATAR, h)
        if nh != h:
            f.write_text(nh, encoding="utf-8")
            n += 1
    print("avatar restored in nav on", n, "files")


def css():
    p = SITE / "assets" / "site.css"
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r"\n?/\* brand logo 2026-11-17 \*/\n(?:\.brand[^\n]*\n)+", "\n", s)
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("monogram CSS removed")


if __name__ == "__main__":
    pages(); css()
