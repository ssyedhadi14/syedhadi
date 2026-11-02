#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Page specific edits: tools finance band above the footer, case study photos, thank you pages for forms
# Owner: Syed Hadi
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import uns  # noqa: E402

ROOT = "/home/claude/work/site"
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def load(n):
    return open(os.path.join(ROOT, n), encoding="utf-8").read()


def save(n, h):
    open(os.path.join(ROOT, n), "w", encoding="utf-8").write(h)


# ---------------- tools.html ----------------
h = load("tools.html")
h2 = re.sub(r"<a class=['\"]fr-promo reveal['\"] href=['\"]/fire-calculator['\"]>.*?</a>\s*", "", h, flags=re.S)
h2 = re.sub(r"<a class=['\"]fr-promo reveal['\"] href=['\"]/mutual-fund-returns-calculator['\"][^>]*>.*?</a>\s*", "", h2, flags=re.S)
assert h2 != h, "fr-promo blocks not found"
h = h2
h2 = re.sub(r'<section class="tcalc reveal" id="calculators">.*?</section>\s*', "", h, flags=re.S)
assert h2 != h, "tcalc not found"
h = h2

FIN = [
    ("/salary-calculator", "Salary Growth Calculator", "NEW",
     "Put in today's in hand salary, your spends and your increment. See salary, savings and corpus for the next 45 years, then get the PDF in your inbox.",
     "1579621970563-ebec7560ff3e", "Young plant growing out of a pile of coins", "Project my salary"),
    ("/fire-calculator", "FIRE Calculator India", "",
     "Your FIRE number, the SIP you need and your earliest retirement age, for mutual funds and NSE or BSE stocks.",
     "1476514525535-07fb3b4ae5f1", "Wooden boat on a calm mountain lake at sunrise", "Find my FIRE number"),
    ("/mutual-fund-returns-calculator", "Top 50 Mutual Funds Returns", "",
     "Real 5, 10, 15 and 20 year returns of large, mid, small cap, index, hybrid and debt funds, with a SIP projector.",
     "1559526324-4b87b5e36e44", "Person reviewing investment charts on a laptop", "Explore the funds"),
    ("/qums", "Qums Calculator", "",
     "Shia Qums (Khums) in three easy steps, with Sahm e Imam and Sahm e Sadat worked out for you.",
     "1532629345422-7515f3d16bb6", "Open hands holding coins and a note that says make a change", "Work out my Qums"),
]
cards = ""
for href, title, badge, desc, pid, alt, cta in FIN:
    b = f'<span class="badge-f">{badge}</span>' if badge else ""
    cards += (f'<a class="fin-card reveal" href="{href}"><span class="fin-img">{b}'
              f'<img src="{uns(pid, 640, 400)}" alt="{alt}" width="640" height="400" loading="lazy" decoding="async"></span>'
              f'<span class="fin-body"><b>{title}</b><p>{desc}</p><span class="fin-cta">{cta} {ARROW}</span></span></a>')
band = f'''<section class="fin-band" id="calculators" aria-labelledby="fin-title">
  <span class="fin-deco d1" aria-hidden="true"></span><span class="fin-deco d2" aria-hidden="true"></span>
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Free money calculators</span><h2 class="display" id="fin-title">Plan the money side too</h2>
    <p>Four free calculators built for India, no sign up. Salary growth over 45 years, early retirement, mutual fund returns and Qums. Each one runs in your browser and nothing you type leaves the page unless you ask for the PDF.</p></div>
    <div class="fin-grid">{cards}</div>
  </div>
</section>
'''
assert h.count("<footer") == 1
h = h.replace("<footer", band + "<footer", 1)
# hero copy: point to the band
h = h.replace("Tap any card to see how I use it.</p>", 'Tap any card to see how I use it. Looking for the <a href="#calculators">free money calculators</a>? They sit at the end of this page.</p>', 1)
save("tools.html", h)
print("tools.html done")

# ---------------- case-studies.html ----------------
h = load("case-studies.html")
COVERS = {
    "ai-search": ("1485827404703-89b55fcc595e", "Friendly white humanoid robot looking at the camera, standing in for AI search assistants"),
    "inbound": ("1504868584819-f8e8b4b6d7e3", "Laptop on a desk showing website traffic charts climbing"),
    "founding-pmm": ("1552664730-d307ca884978", "Product team planning positioning with sticky notes on a glass wall"),
    "systems": ("1551288049-bebda4e38f71", "Monitor showing an analytics dashboard with charts and counters"),
    "live-moments": ("1540575467063-178a50c2df87", "Audience at a conference talk seen from the back of the room"),
    "analysts": ("1526628953301-3e589a6a8b74", "Close up of a screen with performance metrics and scores"),
}
for cid, (pid, alt) in COVERS.items():
    # feature articles
    pat = re.compile(r'(<article class="cs-feat reveal" id="' + cid + r'">\s*)<div aria-hidden="true" class="cs-cover art [a-z-]+"><span class="cs-grid"></span>', re.S)
    pat_raw = re.compile(r"(<article class=['\"]cs-feat reveal['\"] id=['\"]" + cid + r"['\"]>\s*)<div class=\"cs-cover art [a-z-]+\" aria-hidden=\"true\"><span class=\"cs-grid\"></span>", re.S)
    img = f'<div class="cs-cover photo"><img src="{uns(pid, 1200, 750)}" alt="{alt}" width="1200" height="750" loading="lazy" decoding="async">'
    n = len(pat.findall(h)) + len(pat_raw.findall(h))
    h = pat.sub(lambda m: m.group(1) + img, h)
    h = pat_raw.sub(lambda m: m.group(1) + img, h)
    # more cards (anchor with id)
    pat2 = re.compile(r"(<a class=['\"]cs-card reveal['\"] href=['\"][^'\"]*['\"] id=['\"]" + cid + r"['\"]>)<div class=\"cs-cover art [a-z-]+\" aria-hidden=\"true\"><span class=\"cs-grid\"></span>", re.S)
    n += len(pat2.findall(h))
    h = pat2.sub(lambda m: m.group(1) + img, h)
    assert n == 1, f"cover {cid}: {n}"
# existing photo cards have empty alt: give them real alt text
h = h.replace('<img src="img/kubecon-india.jpg" alt=""', '<img src="img/kubecon-india.jpg" alt="Team AccuKnox at the KubeArmor booth at KubeCon India"')
h = h.replace('<img src="img/bsides-2026.jpg" alt=""', '<img src="img/bsides-2026.jpg" alt="Startup Award moment on the AccuKnox booth at Security BSides Bangalore 2026"')
h = h.replace('<img src="img/delhi-ncr.jpg" alt=""', '<img src="img/delhi-ncr.jpg" alt="Syed Hadi with channel partners in Delhi NCR"')
# service case study boxes: add thumbnails
BOX = {
    "/gtm-case-study": ("1560472354-b33ff0c44a43", "Web analytics dashboard with traffic and conversion numbers"),
    "/pmm-case-study": ("1517245386807-bb43f82c33c4", "Speaker presenting a product story to a seated team"),
    "/aeo-seo-case-study": ("1611974789855-9c2a0a7236a3", "Ranking chart on a dark screen"),
    "/content-case-study": ("1573164713988-8665fc963095", "Marketer walking through an office with a laptop"),
    "/partner-revenue-case-study": ("1521791136064-7986c2920216", "Two business partners shaking hands"),
    "/gtm-pmm-case-study": ("1542744173-8e7e53415bb0", "Team reviewing a go to market plan in a meeting room"),
}
for href, (pid, alt) in BOX.items():
    pat = re.compile(r"<a class=['\"]lp-box reveal['\"] href=['\"]" + re.escape(href) + r"['\"]><b>(.*?)</b><span>(.*?)</span></a>", re.S)
    m = pat.search(h)
    assert m, href
    new = (f'<a class="lp-box has-img reveal" href="{href}"><span class="lp-img"><img src="{uns(pid, 640, 320)}" alt="{alt}" width="640" height="320" loading="lazy" decoding="async"></span>'
           f'<span class="lp-txt"><b>{m.group(1)}</b><span>{m.group(2)}</span></span></a>')
    h = h[:m.start()] + new + h[m.end():]
save("case-studies.html", h)
print("case-studies.html done")

# ---------------- thank you pages for the formsubmit forms (were 404) ----------------
shell = load("schedule-meeting.html")
nav = re.search(r"<nav>.*?</nav>", shell, re.S).group(0)
foot = re.search(r"<footer class=\"site-foot\">.*?</footer>", shell, re.S).group(0)
head_links = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)


def thanks_page(fname, title, h1, body, data_page, extra_script=""):
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try{{if(localStorage.getItem('sh_theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<title>{title} | Syed Hadi</title>
<meta name="description" content="{h1} Syed Hadi will follow up by email.">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#5b3df5">
{head_links}
</head>
<body data-page="{data_page}">
{nav}
<main id="main" class="thanks"><div class="wrap">
<span class="eyebrow">Received</span>
<h1 class="display">{h1}</h1>
{body}
</div></main>
{foot}
<script src="/assets/common.js?v=20261031q"></script>
{extra_script}
</body>
</html>
'''

audit = thanks_page("audit-requested.html", "Audit request received", "Your audit request is in.",
    '''<p>Thanks. I will look at your website and positioning and send a short Loom walkthrough with the three changes I would make first, usually within two working days.</p>
<p>While you wait, two things that take minutes: run the <a href="/ai-visibility-checker">AI Visibility Checker</a> to see how likely ChatGPT, Gemini and AI Overviews are to cite you, or the <a href="/gtm-health-check">GTM Health Check</a> for a quick score.</p>
<div class="btns"><a class="btn btn-primary" href="/schedule-meeting">Schedule a call instead</a><a class="btn btn-ghost" href="/case-studies">Read the case studies</a><a class="btn btn-ghost" href="/">Back home</a></div>''', "audit")
save("audit-requested.html", audit)

onep = thanks_page("one-pager-sent.html", "One pager on its way", "Your one pager is on its way.",
    '''<p id="opMsg">Thanks. The pricing one pager lands in your inbox shortly. If it is not there in ten minutes, check promotions or spam, then email <a href="mailto:ssyedhadi14@gmail.com">ssyedhadi14@gmail.com</a>.</p>
<p>Every engagement starts with a 30 minute call and ends with a draft 90 day plan, whether or not we work together.</p>
<div class="btns"><a class="btn btn-primary" href="/schedule-meeting">Schedule meeting</a><a class="btn btn-ghost" id="opBack" href="/gtm-pmm-in-a-box">Back to the box</a><a class="btn btn-ghost" href="/case-studies">See the case studies</a></div>''', "onepager",
    '''<script>(function(){var m={growthbox:['/gtm-pmm-in-a-box','GTM + PMM in a box'],gtmbox:['/gtm-in-a-box','GTM in a box'],pmmbox:['/pmm-in-a-box','PMM in a box'],seobox:['/aeo-seo-in-a-box','AEO/SEO Ranking in a box'],contentbox:['/content-in-a-box','Content in a box'],partnerbox:['/partner-revenue-in-a-box','Partner Revenue in a box']};var k=new URLSearchParams(location.search).get('for');if(m[k]){var b=document.getElementById('opBack');b.href=m[k][0];b.textContent='Back to '+m[k][1];document.getElementById('opMsg').innerHTML='Thanks. The <b>'+m[k][1]+'</b> pricing one pager lands in your inbox shortly. If it is not there in ten minutes, check promotions or spam, then email <a href="mailto:ssyedhadi14@gmail.com">ssyedhadi14@gmail.com</a>.';}})();</script>''')
save("one-pager-sent.html", onep)
print("thank you pages written")
