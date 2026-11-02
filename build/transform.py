#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Global SEO, AEO and UX fix pass over every page of syedcreates.com (nav, footer, canonicals, titles, a11y, images, crawl files)
# Owner: Syed Hadi
import glob
import json
import os
import re
import sys
from datetime import date

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from serif import accent as serif_accent, CSS as SERIF_CSS  # noqa: E402
from shared import SITE, VER, CSS_ADD, REDIRECTS_HEAD, HEADERS, calc_menu, newsletter_section  # noqa: E402
from menus import work_menu, tools_menu  # noqa: E402

ROOT = "/home/claude/work/site"
TODAY = date.today().isoformat()

# Shorter titles (<= 60 chars) for pages that overflowed. Keyword first, brand last.
TITLES = {
    "calculator.html": "Free India Calculators: Salary, EMI, FIRE, Car, Mutual Funds",
    "car-mileage-calculator.html": "Car Mileage Calculator India: Fuel Cost Per Month and Per Km",
    "portfolio.html": "Portfolio: Case Studies, GTM Engine, Events and Writing",
    "30-day-shadow-ai-discovery-sprint.html": "30 Day Shadow AI Discovery Sprint Plan | Syed Hadi",
    "aeo-seo-case-study.html": "AEO and SEO Case Study: 27.72% AI Visibility | Syed Hadi",
    "ai-soc-tool-evaluation-regulated.html": "How to Evaluate an AI SOC Tool in Regulated Firms",
    "ai-spm-7-runtime-security-questions.html": "7 Runtime Security Questions Before Buying AI-SPM",
    "aspm-evaluation-cutting-false-positives.html": "ASPM Evaluation Guide: Cut False Positives | Syed Hadi",
    "cert-in-evidence-pipeline-hybrid-cloud.html": "CERT-In Ready Evidence Pipeline for Hybrid Cloud",
    "cnapp-comparison-checklist-with-scoring.html": "CNAPP Comparison Checklist With Scoring | Syed Hadi",
    "cnapp-cspm-cwpp-explained-for-buyers.html": "CNAPP vs CSPM vs CWPP Explained for Buyers | Syed Hadi",
    "gtm-pmm-case-study.html": "GTM and PMM Case Study: Positioning Plus Pipeline",
    "how-to-build-a-saas-partner-program.html": "How to Build a SaaS Partner Program That Brings Pipeline",
    "mcp-ai-agent-threat-model.html": "How to Threat Model an MCP Based AI Agent | Syed Hadi",
    "privacy.html": "Privacy Policy and Support | Syed Hadi",
    "runtime-cnapp-vs-agentless-cnapp.html": "Runtime CNAPP vs Agentless CNAPP: Which Fits Your Team",
    "stateful-prompt-firewall.html": "Stateful Prompt Firewall: A Guide to AI Guardrails",
}
DESCS = {
    "calculator.html": "Free calculators built for India: salary growth, loan EMI, car running cost, FIRE, mutual funds, PMM salary and Qums, plus GTM scorecards. PDF reports.",
    "brand.html": "Syed Hadi brand kit: logo files in SVG and PNG, fonts, colour palette, approved headshot, bio and a PDF kit for event organisers and press.",
    "adventure.html": "Freefall over Dubai, a drive from Bengaluru to Ooty, a 100 km walk from Najaf to Karbala and essays from Iran, Mecca and Medina. Syed Hadi off duty.",
    "portfolio.html": "Everything Syed Hadi has shipped: case studies, the GTM engine, events and talks, AI systems, recognition, the B2B playbook and long form writing.",
    "work.html": "What Syed Hadi does and the outcomes behind it: product marketing, channel partnerships, GTM strategy, pipeline, events and AI systems for GTM.",
    "growth-in-a-box.html": "Six fixed scope growth engagements for B2B SaaS and security: GTM, PMM, AEO/SEO, content and partner revenue, each with a 30 to 90 day plan.",
    "car-mileage-calculator.html": "Monthly km, mileage and petrol price in, litres per month, fuel cost by city, cost per km, tank range and yearly running cost out. Free PDF.",
    "loan-calculator.html": "EMI, total interest and a plan to close your home, car or personal loan in half the time. Prepay versus invest with 24(b) and 80C counted. Free PDF.",
    "404.html": "That page moved or never existed. Jump to the GTM services, case studies, free calculators or the blog on syedcreates.com.",
}

img_dims = {}


def dims(rel):
    rel = rel.split("?")[0].lstrip("/")
    if rel in img_dims:
        return img_dims[rel]
    p = os.path.join(ROOT, rel)
    try:
        if rel.lower().endswith(".svg"):
            svg = open(p, encoding="utf-8", errors="replace").read(4000)
            vb = re.search(r'viewBox=["\']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', svg)
            img_dims[rel] = (round(float(vb.group(1))), round(float(vb.group(2)))) if vb else None
        else:
            with Image.open(p) as im:
                img_dims[rel] = im.size
    except Exception:
        img_dims[rel] = None
    return img_dims[rel]


def clean_url(name):
    if name == "index.html":
        return SITE + "/"
    return SITE + "/" + name[:-5]


def fix_img_dims(html):
    def rep(m):
        tag = m.group(0)
        if re.search(r'\swidth=', tag) and re.search(r'\sheight=', tag):
            return tag
        src = re.search(r'\ssrc=["\']([^"\']+)["\']', tag)
        if not src or src.group(1).startswith(("http", "data:")):
            return tag
        d = dims(src.group(1))
        if not d:
            return tag
        w, h = d
        # keep tags that already carry one dimension: add the missing one proportionally
        mw = re.search(r'\swidth=["\']?(\d+)', tag)
        mh = re.search(r'\sheight=["\']?(\d+)', tag)
        if mh and not mw:
            hh = int(mh.group(1)); ww = round(w * hh / h)
            return tag[:-1] + f' width="{ww}">' if not tag.endswith('/>') else tag[:-2] + f' width="{ww}"/>'
        if mw and not mh:
            ww = int(mw.group(1)); hh = round(h * ww / w)
            return tag[:-1] + f' height="{hh}">' if not tag.endswith('/>') else tag[:-2] + f' height="{hh}"/>'
        add = f' width="{w}" height="{h}"'
        return tag[:-2] + add + "/>" if tag.endswith("/>") else tag[:-1] + add + ">"
    return re.sub(r"<img\b[^>]*>", rep, html)


def process(path, nav_new):
    name = os.path.basename(path)
    html = open(path, encoding="utf-8").read()
    orig = html
    url = clean_url(name)
    old_url = SITE + "/" + name
    # 1. shared nav
    if "<nav>" in html and nav_new:
        html = re.sub(r"<nav>.*?</nav>", lambda m: nav_new, html, count=1, flags=re.S)
    # 2. footer and mega menu h4 -> non heading element with the same look
    html = re.sub(r"<h4>(.*?)</h4>", r'<p class="h4">\1</p>', html)
    # home wins cards use h4 after an h2 section head: make them h3 (handled in home script, kept safe here)
    # 3. skip link + main landmark
    if 'class="skip"' not in html:
        html = re.sub(r"(<body[^>]*>)", r'\1\n<a class="skip" href="#main">Skip to content</a>', html, count=1)
    if "<main" in html:
        html = re.sub(r"<main(?![^>]*\bid=)", '<main id="main"', html, count=1)
    elif "</nav>" in html and "<footer" in html:
        # home and 404: wrap everything between the nav and the footer area in a main landmark
        a = html.index("</nav>") + len("</nav>")
        b = html.index('<div class="proof-strip">') if '<div class="proof-strip">' in html else html.index("<footer")
        html = html[:a] + '\n<main id="main">' + html[a:b] + '</main>\n' + html[b:]
    # 4. canonical, og:url, twitter, json-ld -> clean URL
    html = html.replace(f'rel="canonical" href="{old_url}"', f'rel="canonical" href="{url}"')
    html = html.replace(f'href="{old_url}" rel="canonical"', f'href="{url}" rel="canonical"')
    html = html.replace(f'property="og:url" content="{old_url}"', f'property="og:url" content="{url}"')
    html = html.replace(f'content="{old_url}" property="og:url"', f'content="{url}" property="og:url"')
    # json-ld and any absolute self references that end in .html
    html = re.sub(r'"' + re.escape(SITE) + r'/([a-z0-9-]+)\.html(#[a-z0-9-]*)?"',
                  lambda m: f'"{SITE}/{m.group(1)}{m.group(2) or ""}"', html)
    html = html.replace(f'"{SITE}/index"', f'"{SITE}/"')
    # 5. titles / descriptions
    if name in TITLES:
        t = TITLES[name]
        html = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", html, count=1, flags=re.S)
        html = re.sub(r'(<meta[^>]*(?:property="og:title"|name="twitter:title")[^>]*content=")[^"]*(")', r"\g<1>" + t + r"\2", html)
        html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*(?:property="og:title"|name="twitter:title"))', r"\g<1>" + t + r"\2", html)
    if name in DESCS:
        d = DESCS[name]
        html = re.sub(r'(<meta name="description" content=")[^"]*(")', r"\g<1>" + d + r"\2", html)
        html = re.sub(r'(<meta[^>]*(?:property="og:description"|name="twitter:description")[^>]*content=")[^"]*(")', r"\g<1>" + d + r"\2", html)
    # 6. image dimensions for CLS
    html = fix_img_dims(html)
    # 7. quiz pages: dead '#' retake link -> real button
    html = html.replace('<a class="btn btn-ghost" href="#" id="qzAgain">', '<button class="btn btn-ghost" type="button" id="qzAgain">')
    if 'id="qzAgain">' in html and "<button" in html.split('id="qzAgain">')[0][-80:]:
        # close the right tag
        html = re.sub(r'(<button class="btn btn-ghost" type="button" id="qzAgain">[^<]*)</a>', r"\1</button>", html)
    html = html.replace('<h2 class="display" id="qzBand"></h2>', '<h2 class="display" id="qzBand"><span class="sr">Your result</span></h2>')
    # 7b. every page needs common.js (menu, dropdowns, theme, reveals, badge hider)
    if "assets/common.js" not in html and "</body>" in html:
        html = html.replace("</body>", f'<script src="/assets/common.js?v={VER}"></script>\n</body>', 1)
    # 7c. one cache-busting version for every local script and stylesheet
    html = re.sub(r'((?:/|\b)assets/[a-z0-9-]+\.(?:js|css))\?v=[0-9a-z]+', lambda m: f"{m.group(1)}?v={VER}", html)
    # 7d. homepage MBA card points at its own credentials section
    html = html.replace('href="/about#credentials"', 'href="/#credentials"')
    # 8. asset version bump
    html = re.sub(r"/assets/site\.css\?v=[0-9a-z]+", f"/assets/site.css?v={VER}", html)
    html = re.sub(r"assets/common\.js\?v=[0-9a-z]+", f"assets/common.js?v={VER}", html)
    # 9. 404 page: noindex, no canonical needed
    if name == "404.html" and 'name="robots"' in html:
        html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', html)
    # 9b. footer resources: Insights, Blog, Salary Growth Calculator only (the rest live as cards on /blog)
    html = re.sub(r'(<div class="fcol" role="navigation" aria-label="Resources">(?:<p class="h4">|<h4>)Resources(?:</p>|</h4>)\s*).*?(\s*</div>)',
                  r"\1<a href='/insights'>Insights</a><a href='/blog'>Blog</a><a href='/salary-calculator'>Salary Growth Calculator</a>\2", html, count=1, flags=re.S)
    # 9a2. newsletter band v2 on every page that carries the band
    html = re.sub(r'<section class="newsletter(?: nl2)?" aria-labelledby="nl-title">.*?</section>', lambda m: newsletter_section(), html, count=1, flags=re.S)
    # 9a3. footer Links column: Adventure (footer only, by request)
    if "href='/adventure'" not in html:
        html = html.replace("<a href='/privacy'>Privacy</a>", "<a href='/adventure'>Adventure</a><a href='/privacy'>Privacy</a>", 1)
    # 9a4. footer Links column: Brand (press kit)
    if "href='/brand'" not in html:
        html = html.replace("<a href='/adventure'>Adventure</a>", "<a href='/adventure'>Adventure</a><a href='/brand'>Brand</a>", 1)
    # 9a5. typography refresh (2026-11-02): Plus Jakarta Sans display + Instrument Serif accents, self hosted; Inter and JetBrains Mono stay on Google Fonts
    html = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">', '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">', html)
    html = html.replace('"Bricolage Grotesque"', '"Plus Jakarta Sans"').replace("'Bricolage Grotesque'", "'Plus Jakarta Sans'")
    # 9b2. favicon cache bust (old deploy left a stale icon in browsers)
    html = re.sub(r'href="(/img/favicon-32\.png|/img/favicon-192\.png|/img/apple-touch-icon\.png|/favicon\.ico)(\?v=\d+)?"', r'href="\1?v=3"', html)
    html = html.replace("Programs covering over $35B in annual TAM", "Partner programs live in India, MENA, APAC, Japan, Europe, Africa and the US")
    # 9c. AEO: every page declares the Person entity in its graph (subpages only referenced it by @id)
    if name != "index.html" and '"@type": "Person"' not in html and '"@type":"Person"' not in html:
        person = '{"@type": "Person", "@id": "' + SITE + '/#person", "name": "Syed Hadi", "url": "' + SITE + '/", "image": "' + SITE + '/photo.jpg", "jobTitle": "Product Marketing and Partnerships Lead", "worksFor": {"@type": "Organization", "name": "AccuKnox", "url": "https://accuknox.com"}, "sameAs": ["https://www.linkedin.com/in/syedhadii/", "https://ssyedhadi.medium.com/", "https://syedhadi.substack.com/"]}'
        html = html.replace('"@graph": [', '"@graph": [' + person + ', ', 1)
    # 10. external links: add rel noopener when target blank lacks it (safety net)
    def rel_fix(m):
        tag = m.group(0)
        if 'target="_blank"' in tag and "noopener" not in tag:
            tag = tag.replace('target="_blank"', 'target="_blank" rel="noopener"')
        return tag
    html = re.sub(r"<a\b[^>]*>", rel_fix, html)
    # 11. serif accent word in every display heading, rotating soft tints
    html = serif_accent(html)
    if name == "index.html" and "serif-accent" not in html:
        html = html.replace('<p class="lede">I turn security products into pipeline.', '<p class="lede">I turn security products into <span class="serif-accent">pipeline</span>.', 1)
    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return html


def build_nav(sample_html):
    nav = re.search(r"<nav>.*?</nav>", sample_html, re.S).group(0)
    # remove calculator entries from the Tools mega menu and its mobile list
    tools_start = nav.find('<div class="dd mega" data-group="tools">')
    tools_end = nav.find('<div class="nav-right">')
    tools = nav[tools_start:tools_end]
    for href in ["/pmm-salary-2026#calculator", "/fire-calculator", "/mutual-fund-returns-calculator",
                 "/ai-visibility-checker", "/gtm-health-check", "/partner-readiness-score"]:
        tools = re.sub(r"<a [^>]*href=['\"]" + re.escape(href) + r"['\"][^>]*>.*?</a>", "", tools, flags=re.S)
    # insert Calculator menu after the Tools block (before nav-links closes)
    idx = tools.rfind("</div>")  # closing of nav-links
    tools = tools[:idx] + calc_menu() + tools[idx:]
    nav = nav[:tools_start] + tools + nav[tools_end:]
    # 2026-10-31: image led Work and Tools menus
    ws, we = nav.find('<div class="dd mega" data-group="work">'), nav.find('<div class="dd mega" data-group="portfolio">')
    nav = nav[:ws] + work_menu() + "\n      " + nav[we:]
    ts, te = nav.find('<div class="dd mega" data-group="tools">'), nav.find('<div class="dd mega" data-group="calc">')
    nav = nav[:ts] + tools_menu() + "\n      " + nav[te:]
    # parent page for every group: a "View all" row in the mega menu and a first entry in the mobile list
    PARENTS = {"growth": ("/growth-in-a-box", "Growth in a box", "Six fixed scope engagements"), "work": ("/work", "Work", "Six areas, one scoreboard"),
               "portfolio": ("/portfolio", "Portfolio", "Case studies, events, writing, recognition"), "tools": ("/tools", "Tool directory", "The stack behind the work"),
               "calc": ("/calculator", "All calculators", "Money tools and GTM scorecards")}
    for g, (href, label, blurb) in PARENTS.items():
        a = nav.find('<div class="dd mega" data-group="%s">' % g)
        if a < 0:
            continue
        b = nav.find('<div class="dd mega" data-group=', a + 10)
        if b < 0:
            b = nav.find('<div class="nav-right">', a)
        block = nav[a:b]
        block = block.replace('<div class="mm-all">', '<!--mm-all-->')  # idempotent guard (never present in pristine)
        # desktop: before the mega menu closes (the mm-simple div follows it)
        i = block.find('<div class="mm-simple">')
        if i > 0 and 'class="mm-all"' not in block:
            j = block.rfind('</div>', 0, i)
            block = block[:j] + '<div class="mm-all"><a href="%s">View all: %s &rarr;</a><span>%s</span></div>' % (href, label, blurb) + block[j:]
        block = block.replace('<div class="mm-simple">', '<div class="mm-simple"><a class="mm-parent" href="%s">All %s &rarr;</a>' % (href, label.replace("Tool directory", "tools").replace("All calculators", "calculators")), 1)
        nav = nav[:a] + block + nav[b:]
    return nav


def write_crawl_files(pages):
    # sitemap with clean URLs
    noindex = set()
    for p in pages:
        h = open(p, encoding="utf-8").read()
        if re.search(r'name="robots" content="[^"]*noindex', h):
            noindex.add(os.path.basename(p))
    order = ["index.html", "calculator.html", "loan-calculator.html", "bmi-calculator.html", "car-mileage-calculator.html", "salary-calculator.html", "seo-aeo-score.html", "growth-in-a-box.html", "work.html", "portfolio.html", "gtm-pmm-in-a-box.html", "gtm-in-a-box.html", "pmm-in-a-box.html",
             "aeo-seo-in-a-box.html", "content-in-a-box.html", "partner-revenue-in-a-box.html", "skill-pack.html",
             "schedule-meeting.html", "case-studies.html", "tools.html", "fire-calculator.html",
             "mutual-fund-returns-calculator.html", "qums.html", "pmm-salary-2026.html"]
    names = [os.path.basename(p) for p in pages]
    rest = sorted(n for n in names if n not in order)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for n in order + rest:
        if n not in names or n in noindex or n == "404.html":
            continue
        pri = "1.0" if n == "index.html" else ("0.9" if n in order else "0.7")
        freq = "weekly" if n in order else "monthly"
        lines.append(f"  <url><loc>{clean_url(n)}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    lines.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(lines) + "\n")
    # redirects
    red = REDIRECTS_HEAD
    for n in sorted(names):
        if n in ("index.html", "404.html"):
            continue
        red += f"/{n:<48} /{n[:-5]:<45} 301!\n"
    open(os.path.join(ROOT, "_redirects"), "w").write(red)
    open(os.path.join(ROOT, "_headers"), "w").write(HEADERS)
    # robots
    open(os.path.join(ROOT, "robots.txt"), "w").write("""User-agent: *
Allow: /

# AI answer engines and assistants are welcome
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bingbot
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: https://syedcreates.com/sitemap.xml
""")


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    sample = open("/home/claude/live/about.html", encoding="utf-8").read()  # pristine live nav, keeps the rebuild idempotent
    nav_new = build_nav(sample)
    for p in pages:
        process(p, nav_new)
    # css additions (idempotent)
    css_path = os.path.join(ROOT, "assets", "site.css")
    css = open(css_path, encoding="utf-8").read()
    cuts = [css.index(m) for m in ("\n/* ===== 2026-11-02 typography", "\n/* ===== 2026-10-31 QA pass") if m in css]
    if cuts:
        css = css[:min(cuts)]
    from videos import CSS as VIDEO_CSS
    css = css.rstrip() + "\n" + CSS_ADD + VIDEO_CSS + SERIF_CSS
    css = css.replace('"Bricolage Grotesque"', '"Plus Jakarta Sans"').replace("'Bricolage Grotesque'", "'Plus Jakarta Sans'")
    open(css_path, "w", encoding="utf-8").write(css)
    # asset scripts that load other assets carry the same version
    for jn in ("calc-reports.js", "report-pdf.js", "salary-calculator.js"):
        jp = os.path.join(ROOT, "assets", jn)
        if os.path.exists(jp):
            j = open(jp, encoding="utf-8").read()
            j2 = re.sub(r"var VER = '[0-9a-z]+'", f"var VER = '{VER}'", j)
            j2 = re.sub(r"report-pdf\.js\?v=[0-9a-z]+", f"report-pdf.js?v={VER}", j2)
            if j2 != j:
                open(jp, "w", encoding="utf-8").write(j2)
    # common.js: active group for calculator pages
    js_path = os.path.join(ROOT, "assets", "common.js")
    js = open(js_path, encoding="utf-8").read()
    js = js.replace("salary:'tools',", "salary:'calc',salarycalc:'calc',bmicalc:'calc',carcalc:'calc',loancalc:'calc',brand:'portfolio',fire:'calc',mf:'calc',khums:'calc',tool_ai:'calc',tool_gtm:'calc',tool_partner:'calc',")
    open(js_path, "w", encoding="utf-8").write(js)
    write_crawl_files(pages)
    print("processed", len(pages), "pages")


if __name__ == "__main__":
    main()
