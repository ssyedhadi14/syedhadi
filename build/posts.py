#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Add imagery to every card on /posts (LinkedIn post image where captured, designed cover otherwise)
# Owner: Syed Hadi
import os
import re

ROOT = "/home/claude/work/site"
p = os.path.join(ROOT, "posts.html")
h = open(p, encoding="utf-8").read()
ICON = {
    "Article": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
    "Post": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v11H8l-4 4z"/></svg>',
    "Event": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "Video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg>',
    "Reshare": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M17 2l4 4-4 4M3 11V8a2 2 0 0 1 2-2h16M7 22l-4-4 4-4M21 13v3a2 2 0 0 1-2 2H3"/></svg>',
}
h = re.sub(r'<a class="lip-img"[^>]*>.*?</a>\s*', "", h, flags=re.S)
n_img = 0

def rep(m):
    global n_img
    kind, body = m.group(1), m.group(2)
    pid = re.search(r'data-id="(\d+)"', body)
    pid = pid.group(1) if pid else ""
    title = re.search(r'<h2 class="lip-h">(.*?)</h2>', body)
    title = re.sub(r"<.*?>", "", title.group(1)) if title else "LinkedIn post"
    url = f"https://www.linkedin.com/feed/update/urn:li:activity:{pid}/"
    if pid and os.path.exists(os.path.join(ROOT, "img", "posts", pid + ".jpg")):
        n_img += 1
        img = f'<a class="lip-img" href="{url}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img src="/img/posts/{pid}.jpg" alt="" width="720" height="450" loading="lazy" decoding="async"></a>'
    else:
        img = f'<a class="lip-img" href="{url}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><span class="lip-cover k-{kind.lower()}">{ICON.get(kind, ICON["Post"])}<b>{kind}</b></span></a>'
    return f'<article class="lip" data-kind="{kind}">{img}{body}</article>'

h2 = re.sub(r'<article class="lip" data-kind="(\w+)">(.*?)</article>', rep, h, flags=re.S)
open(p, "w", encoding="utf-8").write(h2)
print("posts: images", n_img, "of", len(re.findall(r'<article class="lip"', h2)))
