#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Homepage Humans of Marketing feature uses its branded cover instead of the portrait,
#          and the "Wins Worth Counting" section moves from the homepage to /about. Idempotent.
# Owner: Syed Hadi
import os
import re

SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
idx_p, ab_p = os.path.join(SITE, "index.html"), os.path.join(SITE, "about.html")
idx, ab = open(idx_p, encoding="utf-8").read(), open(ab_p, encoding="utf-8").read()

# 1. Humans of Marketing cover
idx = re.sub(r'(<a class="hom-photo reveal"[^>]*>)<img src="img/li/humans-of-marketing-feature\.jpg"[^>]*><span>.*?</span>(</a>)',
             r'\1<img src="/img/covers/hom-feature.jpg" alt="Making B2B marketing more human, Syed Hadi featured by Humans of Marketing, October 2026" '
             r'width="1200" height="750" loading="lazy" decoding="async">\2', idx, flags=re.S)
idx = idx.replace('class="hom-photo reveal"', 'class="hom-photo hom-cv reveal"', 1) if "hom-cv" not in idx else idx

# 2. Move Wins Worth Counting
m = re.search(r'<section class="wins-sec" id="wins".*?</section>\n', idx, re.S)
if m:
    wins = m.group(0)
    idx = idx[:m.start()] + idx[m.end():]
    if 'id="wins"' not in ab:
        anchor = '<section class="tr-sec"'
        ab = ab.replace(anchor, wins + anchor, 1) if anchor in ab else ab.replace("</main>", wins + "</main>", 1)
idx = idx.replace('href="/#wins"', 'href="/about#wins"').replace("href='/#wins'", "href='/about#wins'")

open(idx_p, "w", encoding="utf-8").write(idx)
open(ab_p, "w", encoding="utf-8").write(ab)
print("wins on home:", 'id="wins"' in idx, "| wins on about:", 'id="wins"' in ab, "| hom cover:", "hom-feature.jpg" in idx)
