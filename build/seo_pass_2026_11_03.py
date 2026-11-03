#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: SEO and AEO pass over syedcreates.com. Fixes the broken Person image in schema, unifies the
#          Person entity, upgrades article schema and Open Graph tags, adds 3 level breadcrumbs on
#          articles, adds a sitewide Guides footer column (internal links to orphaned money pages),
#          writes descriptive alt text on nav card photos, trims long titles and builds llms-full.txt.
#          Idempotent: safe to run again.
# Owner: Syed Hadi
# Usage: python3 build/seo_pass_2026_11_03.py [path/to/site]
import glob
import html as htmllib
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
ROOT = os.path.abspath(ROOT)
SITE = "https://syedcreates.com"
PERSON_ID = f"{SITE}/#person"
PERSON_IMG = f"{SITE}/img/syed-hadi-2026.jpg"
SAME_AS = [
    "https://www.linkedin.com/in/syedhadii/",
    "https://ssyedhadi.medium.com/",
    "https://syedhadi.substack.com/",
    "https://www.youtube.com/@syed1228",
]
NOINDEX = {"404.html", "audit-requested.html", "one-pager-sent.html", "skill-pack-thanks.html"}

TITLES = {
    "growth-in-a-box.html": "Growth in a Box: Fixed Scope GTM, PMM, SEO and Partner Work",
    "adventure.html": "Adventure: Skydiving, Road Trips and Travel by Syed Hadi",
}

NAV_ALTS = {
    "/img/li/future-of-gtm-2026-event.jpg": "Syed Hadi speaking at the Future of GTM 2026 event",
    "/img/li/delhi-ncr-expansion-2026.jpg": "AccuKnox team during the Delhi NCR expansion in 2026",
    "/img/li/gtm-meetup-growthx-poster.jpg": "GrowthX GTM meetup poster featuring Syed Hadi",
    "/img/li/engineering-team-meet.jpg": "AccuKnox engineering and marketing team meet",
    "/img/li/kcd-kochi-2024.jpg": "AccuKnox at Kubernetes Community Days Kochi 2024",
    "/img/li/bsides-2026-startup-award.jpg": "AccuKnox receiving the startup award at BSides 2026",
    "img/gtm-deep-dive.jpg": "GrowthX GTM Deep Dive session with Syed Hadi",
    "img/marketing-after-hours.jpg": "Marketing After Hours meetup in Bengaluru",
}

GUIDES_COL = (
    '<div class="fcol" role="navigation" aria-label="Guides" data-seo="guides"><p class="h4">Guides</p>'
    "<a href='/product-marketing-consultant-india'>Product marketing consultant, India</a>"
    "<a href='/gtm-consultant-bengaluru'>GTM consultant, Bengaluru</a>"
    "<a href='/growth-marketing-consultant-dubai'>Growth consultant, Dubai</a>"
    "<a href='/fractional-cmo-dubai-saas'>Fractional CMO for Dubai SaaS</a>"
    "<a href='/fractional-pmm-india'>Fractional PMM in India</a>"
    "<a href='/fractional-pmm-vs-agency-vs-full-time-hire'>Fractional PMM vs agency vs hire</a>"
    "<a href='/best-gtm-consultants-for-security-startups'>GTM consultants for security startups</a>"
    "<a href='/how-to-build-a-saas-partner-program'>How to build a SaaS partner program</a>"
    "<a href='/referral-partners'>Referral partners</a>"
    "</div>"
)
RESOURCES_COL = (
    '<div class="fcol" role="navigation" aria-label="Resources"><p class="h4">Resources</p>'
    "<a href='/insights'>Insights</a><a href='/blog'>Blog</a><a href='/writing'>Writing</a>"
    "<a href='/cnapp-cspm-cwpp-explained-for-buyers'>CNAPP, CSPM and CWPP explained</a>"
    "<a href='/runtime-cnapp-vs-agentless-cnapp'>Runtime vs agentless CNAPP</a>"
    "<a href='/ai-spm-7-runtime-security-questions'>AI SPM buyer questions</a>"
    "<a href='/mcp-ai-agent-threat-model'>MCP agent threat model</a>"
    "<a href='/salary-calculator'>Salary Growth Calculator</a>"
    "</div>"
)

LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def fix_person(x):
    """Walk JSON-LD and normalise every Person node that represents Syed."""
    if isinstance(x, dict):
        if x.get("@type") == "Person" and (x.get("@id") == PERSON_ID or "sameAs" in x):
            x["@id"] = PERSON_ID
            x["image"] = PERSON_IMG
            x["sameAs"] = SAME_AS
        for v in x.values():
            fix_person(v)
    elif isinstance(x, list):
        for v in x:
            fix_person(v)
    return x


def person_ref():
    return {"@type": "Person", "@id": PERSON_ID, "name": "Syed Hadi", "url": f"{SITE}/about"}


def process(path):
    name = os.path.basename(path)
    h = open(path, encoding="utf-8").read()
    orig = h
    slug = "" if name == "index.html" else name[:-5]
    url = f"{SITE}/{slug}"
    article = None

    # 1. JSON-LD fixes
    def ld_rep(m):
        nonlocal article
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        fix_person(j)
        nodes = j["@graph"] if isinstance(j, dict) and "@graph" in j else [j]
        for n in nodes:
            if not isinstance(n, dict):
                continue
            if n.get("@type") in ("BlogPosting", "Article"):
                n["author"] = person_ref()
                n["publisher"] = {"@id": PERSON_ID, "@type": "Person", "name": "Syed Hadi", "url": SITE + "/"}
                n["isPartOf"] = {"@id": f"{SITE}/#website"}
                n["inLanguage"] = "en-IN"
                article = n
            if n.get("@type") == "WebPage":
                n.setdefault("inLanguage", "en-IN")
        return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + m.group(3)

    h = LD_RE.sub(ld_rep, h)

    # 2. Articles: 3 level breadcrumb (Home > Insights > article) and Open Graph article tags
    if article and article.get("@type") == "BlogPosting":
        def bc_rep(m):
            try:
                j = json.loads(m.group(2))
            except Exception:
                return m.group(0)
            nodes = j["@graph"] if "@graph" in j else [j]
            for n in nodes:
                if isinstance(n, dict) and n.get("@type") == "BreadcrumbList":
                    n["itemListElement"] = [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                        {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}/insights"},
                        {"@type": "ListItem", "position": 3, "name": article["headline"], "item": url},
                    ]
            return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + m.group(3)
        h = LD_RE.sub(bc_rep, h)
    if article:
        h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
        if "article:published_time" not in h:
            tags = []
            if article.get("datePublished"):
                tags.append(f'<meta property="article:published_time" content="{article["datePublished"]}">')
            if article.get("dateModified"):
                tags.append(f'<meta property="article:modified_time" content="{article["dateModified"]}">')
            tags.append(f'<meta property="article:author" content="{SITE}/about">')
            if article.get("articleSection"):
                tags.append(f'<meta property="article:section" content="{htmllib.escape(article["articleSection"])}">')
            h = re.sub(r'(<meta property="og:type" content="article">)', r"\1\n" + "\n".join(tags), h, count=1)
        if '<meta name="author"' not in h:
            h = h.replace("<meta name=\"description\"", '<meta name="author" content="Syed Hadi">\n<meta name="description"', 1)

    # 3. Footer: Guides column and richer Resources column
    if 'data-seo="guides"' not in h:
        h, n = re.subn(r'<div class="fcol" role="navigation" aria-label="Resources">.*?</div>',
                       lambda _m: RESOURCES_COL + "\n    " + GUIDES_COL, h, count=1, flags=re.S)

    # 4. Descriptive alt text on content photos that shipped with empty alt
    for src, alt in NAV_ALTS.items():
        h = h.replace(f'src="{src}" alt=""', f'src="{src}" alt="{alt}"')

    # 5. Titles over 60 characters
    if name in TITLES:
        new = TITLES[name]
        h = re.sub(r"<title>.*?</title>", f"<title>{new}</title>", h, count=1, flags=re.S)
        h = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + new, h)
        h = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r"\g<1>" + new, h)

    if h != orig:
        open(path, "w", encoding="utf-8").write(h)
        return True
    return False


# ---------- llms-full.txt ----------
DROP = re.compile(r"<(script|style|svg|form|noscript|template|nav|button)\b[\s\S]*?</\1>", re.I)


def page_text(h):
    m = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", h)
    body = m.group(1) if m else h
    body = DROP.sub(" ", body)
    body = re.sub(r'<[^>]+aria-hidden="true"[^>]*>[\s\S]*?</(span|div|i)>', " ", body)
    for lvl in (1, 2, 3, 4):
        body = re.sub(rf"<h{lvl}\b[^>]*>", "\n\n" + "#" * (lvl + 1) + " ", body)
        body = re.sub(rf"</h{lvl}>", "\n", body)
    body = re.sub(r"<li\b[^>]*>", "\n- ", body)
    body = re.sub(r"</(p|div|section|article|blockquote|figure|tr|ul|ol|table)>", "\n", body)
    body = re.sub(r"<br\s*/?>", "\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = htmllib.unescape(body)
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in body.split("\n")]
    out, prev = [], None
    for ln in lines:
        if ln in ("", "-") or ln == prev:
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(ln)
        prev = ln
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def build_llms_full():
    order = ["index.html", "about.html", "growth-in-a-box.html"]
    rest = sorted(f for f in map(os.path.basename, glob.glob(os.path.join(ROOT, "*.html")))
                  if f not in NOINDEX and f not in order and f != "privacy.html")
    parts = [
        "# Syed Hadi: full site text",
        "",
        "> Complete text of syedcreates.com for AI assistants and answer engines. Syed Hadi is a product "
        "marketing and channel partnerships lead at AccuKnox (Zero Trust CNAPP and AI security), based in "
        "Bengaluru, India. He runs fixed scope \"in a box\" GTM, PMM, AEO/SEO, content and partner revenue "
        "projects for B2B SaaS and security startups, and sells Claude skills for marketers. The short index "
        "is at https://syedcreates.com/llms.txt.",
        "",
        "Contact: https://syedcreates.com/schedule-meeting | ssyedhadi14@gmail.com | https://www.linkedin.com/in/syedhadii/",
        "",
    ]
    for f in order + rest:
        h = open(os.path.join(ROOT, f), encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        slug = "" if f == "index.html" else f[:-5]
        parts += ["---", "", f"## {htmllib.unescape(t.group(1).strip()) if t else slug}", "",
                  f"URL: {SITE}/{slug}"]
        if d:
            parts.append(f"Summary: {htmllib.unescape(d.group(1))}")
        parts += ["", page_text(h), ""]
    txt = "\n".join(parts).rstrip() + "\n"
    open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8").write(txt)
    return len(txt)


def patch_crawl_files():
    p = os.path.join(ROOT, "llms.txt")
    t = open(p, encoding="utf-8").read()
    if "llms-full.txt" not in t:
        t = t.rstrip() + "\n\n## Full text\n- [llms-full.txt](https://syedcreates.com/llms-full.txt): every public page of the site as plain text, for AI assistants.\n"
        open(p, "w", encoding="utf-8").write(t)
    p = os.path.join(ROOT, "_headers")
    t = open(p, encoding="utf-8").read()
    if "/llms-full.txt" not in t:
        t = t.rstrip() + "\n\n/llms-full.txt\n  Content-Type: text/plain; charset=utf-8\n"
        open(p, "w", encoding="utf-8").write(t)
    p = os.path.join(ROOT, "_redirects")
    t = open(p, encoding="utf-8").read()
    if "\n/photo.jpg" not in t:
        t = t.replace("# One URL per page", "/photo.jpg         /img/syed-hadi-2026.jpg                                                                             301\n\n# One URL per page", 1)
        open(p, "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    changed = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))) if process(p)]
    patch_crawl_files()
    size = build_llms_full()
    print(f"pages changed: {len(changed)}")
    print(f"llms-full.txt: {size // 1024} KB")
