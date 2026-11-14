#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-14
# Purpose: Build the paid "GTM in a Box, the 10 day build" series for Substack and Medium from Markdown in
#          build/gtm_box_series/. Renders covers and diagrams into site/img (public image hosting only, no pages),
#          and writes paste ready HTML for Substack (paywall marked) and Medium (member only note) to OUT.
# Owner: Syed Hadi
# Usage: python3 build/gtm_box_series.py
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline_notes as pn  # reuse loader, markdown rendering, diagrams and covers

ROOT = pn.ROOT
SRC = os.path.join(ROOT, "build", "gtm_box_series")
OUT = "/home/claude/gtmbox/out"
BASE = pn.BASE
MOTIFS = ["mountain", "idcard", "clipboard", "scales", "doc", "megaphone", "puzzle", "calendar", "chart", "rocket"]
PAYWALL_HTML = ("<div style='margin:32px 0;padding:14px;border:2px dashed #5b3df5;border-radius:10px;text-align:center;"
                "font:600 14px Inter,sans-serif;color:#5b3df5'>PAYWALL GOES HERE. In Substack, put the cursor on this line, "
                "delete it and click Paywall in the toolbar. In Medium, delete this line.</div>")


def load():
    pn.SRC = SRC
    posts = pn.load_posts()
    for p in posts:
        p.setdefault("motif", MOTIFS[(int(p.get("day", 1)) - 1) % len(MOTIFS)])
        p.setdefault("cover_tag", f'GTM in a Box, Day {p.get("day")}')
    return posts


def body(p):
    h = pn.body_html(p)
    h = h.replace("<!-- PAYWALL -->", PAYWALL_HTML)
    h = h.replace('src="/img/', f'src="{BASE}/img/').replace('href="/', f'href="{BASE}/')
    return h.replace('<figure class="pn-fig">', "<figure>")


def page(p, platform):
    paid = "<!-- PAYWALL -->" in p["body_md"]
    note = {
        "substack": f"Substack. Schedule for {pn.nice_date(p['date'])}, 8:15 AM IST. Audience: "
                    + ("everyone sees the part above the paywall, paid subscribers see the rest." if paid else "everyone (free issue)."),
        "medium": f"Medium. Publish {pn.nice_date(p['date'])} morning. "
                  + ("Set it as a member only story (Partner Program)." if paid else "Free story.")
                  + " Add a canonical link to the Substack post once it is live.",
    }[platform]
    title = html.escape(p.get("substack_title") or p["title"])
    sub = html.escape(p.get("substack_subtitle") or p["description"])
    return ("<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>Day {p.get('day')} {title}</title>"
            "<body style='max-width:720px;margin:32px auto;font:18px/1.65 Georgia,serif;padding:0 18px;color:#1c1640'>"
            f"<p style='font:13px/1.5 Inter,sans-serif;color:#666;background:#f6f3ff;padding:10px 12px;border-radius:8px'>{note}<br>"
            f"Cover image: {BASE}/img/covers/og/{p['slug']}.jpg</p>"
            f"<h1>{title}</h1><h3 style='color:#555;font-weight:400'>{sub}</h3>"
            f"<img src='{BASE}/img/covers/og/{p['slug']}.jpg' alt='' style='width:100%;border-radius:10px'>"
            f"{body(p)}</body>")


def main():
    posts = load()
    if len(posts) != 10:
        print(f"warning: expected 10 issues, found {len(posts)}", file=sys.stderr)
    pn.diagrams(posts)
    pn.covers(posts)
    for plat in ("substack", "medium"):
        os.makedirs(os.path.join(OUT, plat), exist_ok=True)
        for p in posts:
            name = f'day-{int(p["day"]):02d}-{p["date"]}-{p["slug"]}.html'
            open(os.path.join(OUT, plat, name), "w", encoding="utf-8").write(page(p, plat))
    json.dump([{k: p[k] for k in ("day", "date", "slug", "title", "description") if k in p} | {"paid": "<!-- PAYWALL -->" in p["body_md"]} for p in posts],
              open(os.path.join(OUT, "schedule.json"), "w"), indent=1)
    print("built", len(posts), "issues")


if __name__ == "__main__":
    main()
