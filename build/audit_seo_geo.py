#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-17
# Purpose: Sitewide SEO and GEO (AI answer engine) audit of site/*.html with a 0 to 100 score per page.
# Owner: Syed Hadi
# Usage: python3 build/audit_seo_geo.py [--json out.json]
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = "https://syedcreates.com"
SERVICE = {"gtm-in-a-box", "growth-in-a-box", "pmm-in-a-box", "gtm-pmm-in-a-box", "partner-revenue-in-a-box",
           "aeo-seo-in-a-box", "content-in-a-box", "fractional-cmo-dubai-saas",
           "growth-marketing-consultant-dubai", "gtm-consultant-bengaluru", "product-marketing-consultant-india",
           "referral-partners", "schedule-meeting"}
SKIP = {"404", "skill-pack-thanks", "thanks"}
NO_CTA = {"privacy", "adventure", "qums", "skill-pack"}


def slug_of(path):
    s = os.path.basename(path)[:-5]
    return "" if s == "index" else s


def load():
    pages = {}
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        s = slug_of(f)
        if s in SKIP or s.startswith("x-"):
            continue
        h = open(f, encoding="utf-8", errors="ignore").read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', h):
            continue
        pages[s] = h
    return pages


def schema_types(soup):
    types = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string or "{}")
        except Exception:
            types.append("INVALID")
            continue
        stack = [data]
        while stack:
            d = stack.pop()
            if isinstance(d, dict):
                t = d.get("@type")
                if t:
                    types += t if isinstance(t, list) else [t]
                stack += list(d.values())
            elif isinstance(d, list):
                stack += d
    return types


def main_text(soup):
    m = soup.find("main") or soup.body or soup
    m = BeautifulSoup(str(m), "html.parser")
    for t in m(["script", "style", "nav", "footer", "noscript", "svg"]):
        t.decompose()
    return m.get_text(" ", strip=True)


def audit():
    pages = load()
    sitemap = open(os.path.join(SITE, "sitemap.xml")).read()
    llms = open(os.path.join(SITE, "llms.txt")).read()
    inbound = defaultdict(set)
    parsed = {}
    for s, h in pages.items():
        soup = BeautifulSoup(h, "html.parser")
        parsed[s] = soup
        main = soup.find("main") or soup
        for a in main.find_all("a", href=True):
            href = a["href"].split("#")[0].split("?")[0]
            if href.startswith(BASE):
                href = href[len(BASE):]
            if href.startswith("/"):
                t = href.strip("/").removesuffix(".html")
                if t != s:
                    inbound[t].add(s)
    results = {}
    for s, soup in parsed.items():
        issues, score = [], 100
        def ded(n, msg):
            nonlocal score
            score -= n
            issues.append(msg)
        title = (soup.title.string or "").strip() if soup.title else ""
        md = soup.find("meta", attrs={"name": "description"})
        desc = md["content"].strip() if md and md.get("content") else ""
        h1s = soup.find_all("h1")
        canon = soup.find("link", rel="canonical")
        og_img = soup.find("meta", property="og:image")
        types = schema_types(soup)
        text = main_text(soup)
        words = len(text.split())
        imgs = soup.find_all("img")
        no_alt = [i for i in imgs if not (i.get("alt") or "").strip() and i.get("aria-hidden") != "true" and i.get("alt") != ""]
        missing_alt = [i for i in imgs if i.get("alt") is None]
        h2s = soup.find_all("h2")
        qs = [h for h in soup.find_all(["h2", "h3", "summary"]) if h.get_text(strip=True).endswith("?")]
        url = f"{BASE}/{s}" if s else f"{BASE}/"
        # technical
        if not title: ded(15, "no title")
        elif len(title) > 62: ded(4, f"title {len(title)} chars")
        elif len(title) < 25: ded(3, f"title short {len(title)}")
        if not desc: ded(10, "no meta description")
        elif not 110 <= len(desc) <= 165: ded(3, f"meta description {len(desc)} chars")
        if len(h1s) != 1: ded(8, f"{len(h1s)} H1s")
        if not canon: ded(6, "no canonical")
        elif canon.get("href") not in (url, url.rstrip("/"), url + "/"): ded(3, f"canonical {canon.get('href')}")
        if not og_img: ded(3, "no og:image")
        if "INVALID" in types: ded(8, "invalid JSON-LD")
        if not types: ded(6, "no schema")
        if not soup.find("meta", attrs={"name": "viewport"}): ded(5, "no viewport")
        if missing_alt: ded(min(6, len(missing_alt)), f"{len(missing_alt)} images without alt")
        if (f"<loc>{url}</loc>" not in sitemap) and (f"<loc>{url.rstrip('/')}</loc>" not in sitemap): ded(4, "not in sitemap")
        if s and len(inbound.get(s, ())) < 2: ded(5, f"weak internal links ({len(inbound.get(s, ()))} pages link in)")
        if words < 300: ded(5, f"thin content ({words} words)")
        # GEO
        if url not in llms and url.rstrip("/") not in llms and s: ded(3, "not in llms.txt")
        if "FAQPage" not in types and s in SERVICE: ded(6, "service page without FAQ schema")
        if s in SERVICE and "Service" not in types and "ProfessionalService" not in types and s != "schedule-meeting": ded(5, "service page without Service schema")
        if len(qs) == 0 and words > 400: ded(2, "no question style headings")
        first_p = soup.find("main").find("p") if soup.find("main") else None
        # leads
        ctas = [a for a in soup.find_all("a", href=True) if "schedule-meeting" in a["href"]]
        main = soup.find("main") or soup
        main_ctas = [a for a in main.find_all("a", href=True) if "schedule-meeting" in a["href"]]
        if s not in ("schedule-meeting",) and s not in NO_CTA and not main_ctas: ded(6, "no Schedule meeting CTA in page body")
        svc_links = {a["href"].strip("/").removesuffix(".html").replace(BASE, "").strip("/") for a in main.find_all("a", href=True)} & SERVICE
        if s not in SERVICE and s not in NO_CTA and not svc_links: ded(4, "no link from body to a service page")
        results[s or "index"] = {"score": max(0, score), "issues": issues, "title": title, "words": words, "types": sorted(set(types)),
                                 "inbound": len(inbound.get(s, ())), "service": s in SERVICE}
    return results


if __name__ == "__main__":
    r = audit()
    scores = [v["score"] for v in r.values()]
    svc = [v["score"] for v in r.values() if v["service"]]
    print(f"pages {len(r)}  sitewide avg {sum(scores)/len(scores):.1f}  service avg {sum(svc)/max(1,len(svc)):.1f}  min {min(scores)}")
    c = Counter(i.split(" (")[0].split(" ")[0] if i[0].isdigit() else re.sub(r"\d+", "N", i.split(" (")[0]) for v in r.values() for i in v["issues"])
    for k, n in c.most_common(25):
        print(f"{n:4d}  {k}")
    if "--json" in sys.argv:
        json.dump(r, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
