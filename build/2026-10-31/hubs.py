#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Generate the parent (hub) pages for every navbar group: /growth-in-a-box, /work, /portfolio, /calculator
# Owner: Syed Hadi
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import SITE, VER, uns, CALCS, SCORECARDS  # noqa: E402

ROOT = "/home/claude/work/site"
shell = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()
nav = re.search(r"<nav>.*?</nav>", shell, re.S).group(0)
foot = re.search(r"<footer class=\"site-foot\">.*?</footer>", shell, re.S).group(0)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)
skill_band = re.search(r'<section class="skill-band".*?</section>', shell, re.S)
skill_band = skill_band.group(0) if skill_band else ""

# growth cards straight from the nav so copy stays in sync
growth_cards = re.findall(r"<a class='gb-card' data-p='(\w+)' href='([^']+)'><span class=\"gb-img\"><img src=\"([^\"]+)\" alt=\"([^\"]*)\"[^>]*></span><span class=\"gb-body\"><b>([^<]+)</b><small>([^<]+)</small></span></a>", nav)

HUBS = {
    "growth-in-a-box": dict(
        title="Growth in a Box: Fixed Scope GTM, PMM, SEO and Partner Programs",
        desc="Six fixed scope growth engagements for B2B SaaS and security companies. GTM, PMM, AEO/SEO, content and partner revenue, each with a 30 to 90 day plan and a price you know up front.",
        eyebrow="Growth in a box", h1="Pick the box. Get the <span>engine</span>.",
        lede="Each box is a fixed scope engagement with a clear deliverable, a 30 to 90 day timeline and a price you know before we start. Built from what worked at AccuKnox and for the partners I have launched since.",
        hero_img=("1521737852567-6949f3f9f2b5", "Startup team working together around a table"),
        page="growthbox", crumb="Growth in a box", group="growth",
        cards=[dict(href=h, img=img, alt=alt, title=t, text=s, tag="Box " + str(i + 1)) for i, (k, h, img, alt, t, s) in enumerate(growth_cards)],
        more=[("/gtm-engine", "GTM Engine", "The operating system behind every box: ICP, outbound, partners, content and reporting as one loop."), ("/playbook", "B2B Playbook", "The free playbook with the frameworks each box is built on."), ("/schedule-meeting", "Book a free 30 minute call", "Bring your pipeline problem. Leave with the box that fits, or a reason none of them do.")],
    ),
    "work": dict(
        title="Work: Product Marketing, Partnerships, GTM and AI Systems",
        desc="What Syed Hadi does and the outcomes behind it: product marketing, channel partnerships, GTM strategy, demand and pipeline, community and events, and AI systems for GTM teams.",
        eyebrow="Work", h1="Six ways I make a technical product <span>easier to buy</span>.",
        lede="Product marketing and partnerships for cloud and AI security, with pipeline as the only scoreboard. Every area below links to the proof: case studies, playbooks and the rooms I have filled.",
        hero_img=("1552664730-d307ca884978", "Team reviewing a go to market plan around a laptop"),
        page="work", crumb="Work", group="work",
        cards=[
            dict(href="/gtm-engine", img=uns("1553877522-43269d4ea984"), alt="Product strategy session with sticky notes", title="Product Marketing", text="Positioning, personas and launch plans that make a technical product easy to buy. Most security products lose deals on clarity, not features.", tag="PMM"),
            dict(href="/recognition", img=uns("1521791136064-7986c2920216"), alt="Two people shaking hands over a deal", title="Channel Partnerships", text="Partners who sell, not just sign. Programs live in India, MENA, APAC, Japan, Europe, Africa and the US, with enablement that partners actually use.", tag="Partners"),
            dict(href="/playbook", img=uns("1507003211169-0a1dd7228f2d"), alt="Person sketching a strategy on paper", title="GTM Strategy", text="Decisions under market pressure: which segment, which motion, which message. The B2B playbook holds the frameworks.", tag="GTM"),
            dict(href="/gtm-engine", img=uns("1551288049-bebda4e38f71"), alt="Dashboard with growth charts on a screen", title="Demand and Pipeline", text="Spend tied to one number. Outbound, events, content and partners reported in the same pipeline view every week.", tag="Pipeline"),
            dict(href="/events", img=uns("1540575467063-178a50c2df87"), alt="Audience at a technology conference", title="Community and Events", text="Rooms full of practitioners, from KubeCon India to BSides and the Kubernetes Bangalore meetup. Talks, booths and meetups that turn into pipeline.", tag="Events"),
            dict(href="/systems", img=uns("1677442136019-21780ecad995"), alt="Abstract visual of AI neural connections", title="AI Systems for GTM", text="Busywork, automated. Claude skills, scheduled agents and scorecards that run the GTM machine while the team sells.", tag="AI"),
        ],
        more=[("/case-studies", "Case studies", "Numbers behind each area, with what was tried and what moved."), ("/about", "About Syed", "Five years from project management to leading product marketing and partnerships."), ("/schedule-meeting", "Work with me", "Fractional, advisory or a fixed scope box.")],
    ),
    "portfolio": dict(
        title="Portfolio: Case Studies, GTM Engine, Events, Writing and Recognition",
        desc="Everything Syed Hadi has shipped in one place: case studies, the GTM engine, events and talks, AI systems, recognition, the B2B playbook, long form writing and the story so far.",
        eyebrow="Portfolio", h1="The proof, in <span>one place</span>.",
        lede="Case studies with numbers, the engine behind them, the stages and rooms, the systems that run the busywork, the awards and the writing. Start anywhere.",
        hero_img=("1497366216548-37526070297c", "Bright modern workspace with a desk and plants"),
        page="portfolio", crumb="Portfolio", group="portfolio",
        cards=[
            dict(href="/case-studies", img=uns("1551288049-bebda4e38f71"), alt="Dashboard with growth charts on a screen", title="Case Studies", text="GTM, PMM, partner revenue, content and AEO/SEO engagements with the before and after numbers.", tag="Proof"),
            dict(href="/gtm-engine", img=uns("1581091226825-a6a2a5aee158"), alt="Engineer at work with technology in the background", title="GTM Engine", text="How ICP, outbound, partners, content and reporting run as one loop, and how to build yours.", tag="System"),
            dict(href="/events", img=uns("1540575467063-178a50c2df87"), alt="Audience at a technology conference", title="Events and Talks", text="KubeCon India, BSides, Black Hat Asia, meetups and webinars. What was said and what it produced.", tag="Stage"),
            dict(href="/systems", img=uns("1677442136019-21780ecad995"), alt="Abstract visual of AI neural connections", title="AI Systems", text="The agents, skills and scorecards that automate reporting, outreach and content ops.", tag="AI"),
            dict(href="/recognition", img=uns("1579389083078-4e7018379f7e"), alt="Trophy on a table under warm light", title="Recognition", text="Awards, features and the moments that marked the journey, Humans of Marketing included.", tag="Awards"),
            dict(href="/playbook", img=uns("1456513080510-7bf3a84b82f8"), alt="Open notebook with handwritten plans", title="B2B Playbook", text="The frameworks behind the work: positioning, partner programs, launch plans and pipeline math.", tag="Playbook"),
            dict(href="/writing", img=uns("1455390582262-044cdead277a"), alt="Writing on a laptop with a coffee nearby", title="Writing", text="Long form on CNAPP, shadow AI, prompt firewalls, AI SOC and non human identity.", tag="Essays"),
            dict(href="/about", img=uns("1522202176988-66273c2fd55f"), alt="Three colleagues comparing notes at a laptop", title="About", text="The five year story, the resume and what I am building next.", tag="Story"),
        ],
        more=[("/blog", "Blog and guides", "Consulting guides, comparisons and the free tools."), ("/posts", "LinkedIn posts", "Posts, articles, events and videos in one searchable grid."), ("/schedule-meeting", "Book a call", "Thirty minutes, no deck, your problem.")],
    ),
    "calculator": dict(
        title="Free Calculators: Salary, Loan EMI, FIRE, Mutual Funds, Qums and GTM Scorecards",
        desc="Free calculators built for India, no sign up. Salary growth over 45 years, loan EMI and prepayment, FIRE number, mutual fund returns, PMM salary, Qums, plus SEO/AEO, AI visibility, GTM health and partner readiness scorecards.",
        eyebrow="Calculators", h1="Plan the money, score the <span>marketing</span>.",
        lede="Every calculator runs in your browser, nothing you type leaves the page, and each one gives you a high fidelity PDF you can keep. Money tools first, GTM scorecards below.",
        hero_img=("1554224155-6726b3ff858f", "Calculator and notebook on a desk"),
        page="calc", crumb="Calculators", group="calc",
        cards=[dict(href=h, img=uns(pid, 640, 360), alt=alt, title=t, text=d, tag=("New" if b else "Calculator")) for k, h, t, d, pid, alt, b in CALCS],
        scorecards=[
            ("/seo-aeo-score", "SEO and AEO Score", "Paste a URL, get an SEO score, an AEO score for AI answer engines, Domain Rating and a fix list."),
            ("/ai-visibility-checker", "AI Visibility Checker", "Ten questions on whether ChatGPT, Gemini and Perplexity can find and cite you."),
            ("/gtm-health-check", "GTM Health Check", "Score your ICP, motion, message and pipeline discipline in five minutes."),
            ("/partner-readiness-score", "Partner Readiness Score", "Is your partner program ready to bring pipeline? Ten questions, one verdict."),
        ],
        more=[("/tools", "Tool directory", "The software stack behind the calculators and the GTM work."), ("/pmm-salary-2026", "India PMM Salary Guide 2026", "Benchmarks by title, experience and city, with the full PDF guide."), ("/skill-pack", "Claude Skill Pack", "Eight Claude skills for marketers and GTM teams.")],
    ),
}

CSS = '''
.hub-hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:32px;align-items:center}
.hub-art{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}
.hub-art img{width:100%;height:100%;object-fit:cover;display:block}
.hub-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.hub-card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--card);text-decoration:none;color:inherit;transition:transform .25s var(--ease),box-shadow .25s var(--ease),border-color .2s}
.hub-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(28,16,80,.14);border-color:var(--accent)}
.hub-img{aspect-ratio:16/9;overflow:hidden;position:relative;background:var(--bg-soft)}
.hub-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}
.hub-card:hover .hub-img img{transform:scale(1.04)}
.hub-img small{position:absolute;top:12px;left:12px;font:800 10.5px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;padding:5px 9px;border-radius:7px;background:rgba(13,11,26,.78);color:#fff}
.hub-body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}
.hub-body b{font-size:18px;line-height:1.25}
.hub-body p{margin:0;font-size:14.5px;line-height:1.55;color:var(--ink-2);flex:1}
.hub-body em{font-style:normal;font-weight:700;color:var(--accent);font-size:14px}
.hub-more{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.hub-more a{display:block;border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card);text-decoration:none;color:inherit}
.hub-more a:hover{border-color:var(--accent)}
.hub-more b{display:block;font-size:16px;margin-bottom:4px} .hub-more span{font-size:14px;color:var(--ink-2)}
@media (max-width:980px){.hub-hero .wrap{grid-template-columns:1fr}.hub-art{max-width:520px}.hub-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:620px){.hub-grid{grid-template-columns:1fr}.hub-more{grid-template-columns:1fr}}
'''


def card(c):
    return (f'<a class="hub-card reveal" href="{c["href"]}"><span class="hub-img"><small>{c["tag"]}</small><img src="{c["img"]}" alt="{c["alt"]}" width="640" height="360" loading="lazy" decoding="async"></span>'
            f'<span class="hub-body"><b>{c["title"]}</b><p>{c["text"]}</p><em>Open &rarr;</em></span></a>')


def build(slug, H):
    url = f"{SITE}/{slug}"
    items = [{"@type": "ListItem", "position": i + 1, "name": c["title"], "url": SITE + c["href"]} for i, c in enumerate(H["cards"])]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": H["title"], "description": H["desc"], "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-10-31",
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": H["crumb"], "item": url}]},
    ]}
    cards = "".join(card(c) for c in H["cards"])
    sc = ""
    if H.get("scorecards"):
        sc = '<section class="bx-sec" style="padding-top:0"><div class="wrap"><div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">GTM scorecards</span><h2 class="display">Score the Marketing</h2><p>Five minute self assessments with a verdict and a fix list.</p></div><div class="hub-more" style="grid-template-columns:repeat(4,1fr)">' + "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in H["scorecards"]) + '</div></div></section>'
    more = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in H["more"])
    hi = H["hero_img"]
    page = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try{{if(localStorage.getItem('sh_theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<title>{H["title"]}</title>
<meta name="description" content="{H["desc"]}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Syed Hadi">
<meta name="theme-color" content="#5b3df5">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Syed Hadi">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{H["title"]}">
<meta property="og:description" content="{H["desc"]}">
<meta property="og:image" content="{SITE}/img/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H["title"]}">
<meta name="twitter:description" content="{H["desc"]}">
<meta name="twitter:image" content="{SITE}/img/og-card.jpg">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{icons}
<style>{CSS}</style>
</head>
<body data-page="{H["page"]}">
{nav}
<header class="page-hero hub-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / {H["crumb"]}</div>
<span class="eyebrow">{H["eyebrow"]}</span>
<h1 class="display" style="font-size:clamp(34px,4.6vw,60px)">{H["h1"]}</h1>
<p>{H["lede"]}</p>
</div>
<div class="hub-art"><img src="{uns(hi[0], 880, 605)}" alt="{hi[1]}" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">
<section class="bx-sec" style="padding-top:28px">
  <div class="wrap"><div class="hub-grid">{cards}</div></div>
</section>
{sc}
<section class="bx-sec" style="padding-top:0">
  <div class="wrap"><div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Keep going</span><h2 class="display">Related</h2></div><div class="hub-more">{more}</div></div>
</section>
</main>
{skill_band}
{foot}
<script src="/assets/common.js?v={VER}"></script>
</body>
</html>
'''
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(page)
    print("hub ->", slug)


for slug, H in HUBS.items():
    build(slug, H)
