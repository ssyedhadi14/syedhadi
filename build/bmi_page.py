#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate /bmi-calculator for syedcreates.com: BMI with Asian Indian bands, waist ratio, optional markers,
#          start doing / stop doing insights, a 7 day habits tracker and a PDF plan
# Owner: Syed Hadi
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import SITE, VER, uns  # noqa: E402

ROOT = "/home/claude/work/site"
shell = open(os.path.join(ROOT, "fire-calculator.html"), encoding="utf-8").read()
nav = re.search(r"<nav>.*?</nav>", shell, re.S).group(0)
foot = re.search(r"<footer class=\"site-foot\">.*?</footer>", shell, re.S).group(0)
tail = re.search(r"</main>\s*(.*?)<footer class=\"site-foot\">", shell, re.S).group(1)
tail = re.sub(r'<section class="yt-sec".*?</section>\n', '', tail, flags=re.S)
tail = re.sub(r'<script[^>]*src="[^"]*common\.js[^"]*"[^>]*></script>', '', tail)
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/car-mileage-calculator"><small>PREVIOUS</small><b>&larr; Car Mileage Calculator</b></a><a class="right" href="/fire-calculator"><small>NEXT</small><b>FIRE Calculator &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/bmi-calculator"
TITLE = "BMI Calculator India with Healthy Habits Tracker and Plan"
DESC = "BMI with Indian cut offs, waist to height ratio, optional BP, sugar and SGPT checks, a start and stop doing plan and a 7 day habits tracker. Free PDF."

FAQ = [
    ("What is a healthy BMI for Indians?",
     "For Asian Indian adults the healthy range is 18.5 to 22.9. A BMI of 23 to 24.9 counts as overweight and 25 or above as obesity. These cut offs are lower than the WHO global ones (25 and 30) because Indians develop diabetes and heart disease at lower body weight, which is why Indian doctors use them."),
    ("How do I calculate BMI?",
     "BMI is your weight in kilograms divided by your height in metres squared. At 170 cm and 72 kg that is 72 ÷ (1.7 × 1.7) = 24.9. The calculator does this for you and shows the weight range that is healthy for your height."),
    ("Why does waist size matter as much as BMI?",
     "Fat around the belly drives insulin resistance, fatty liver and heart risk, and Indians carry more of it at the same BMI. The 2025 revised Indian definition of obesity uses BMI above 23 together with a waist of 90 cm or more for men, 80 cm or more for women, or a waist to height ratio above 0.5."),
    ("What blood pressure, sugar and SGPT readings are normal?",
     "Blood pressure under 120 / 80 is normal and 130 / 80 or more is high. Fasting glucose under 100 mg/dL and HbA1c under 5.7% are normal, with 100 to 125 and 5.7 to 6.4% in the prediabetes range. For SGPT (ALT), gastroenterology guidance puts the healthy upper limit near 33 U/L for men and 25 U/L for women, though many labs print 40. Your doctor reads these with your full history."),
    ("How much weight should I aim to lose first?",
     "Five to seven percent of your current weight over six months. For a 78 kg adult that is about 4 to 5.5 kg. Losses of this size measurably lower blood pressure, blood sugar and liver fat, even before you reach the healthy BMI range."),
    ("Is my data saved or shared?",
     "No. Everything runs in your browser. Health readings never go into the share link. Habit ticks are saved only on this device and reset every Monday. The PDF is built on your device."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-11-02"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/calculator"},
        {"@type": "ListItem", "position": 3, "name": "BMI calculator", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "BMI Calculator and Healthy Habits Tracker", "url": URL, "applicationCategory": "HealthApplication", "operatingSystem": "Any",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "isAccessibleForFree": True,
     "description": "BMI with Asian Indian and WHO bands, healthy weight range, waist to height ratio, optional blood pressure, glucose, HbA1c and SGPT checks, a personalised start and stop doing plan, a 7 day habits tracker and a PDF report.",
     "featureList": ["BMI with Asian Indian cut offs", "Healthy weight range for your height", "Waist to height ratio", "Blood pressure, glucose, HbA1c and SGPT checks", "Start doing and stop doing plan", "7 day habits tracker", "PDF report"],
     "author": {"@id": SITE + "/#person"}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
faq_html = "".join(f'<details class="sp-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)


def sel(id_, label, opts, val):
    o = "".join(f'<option value="{v}"{" selected" if str(v) == str(val) else ""}>{t}</option>' for v, t in opts)
    return f'<label>{label}<select id="{id_}">{o}</select></label>'


def inp(id_, label, val="", mn=None, mx=None, step="1", ph=""):
    a = f' min="{mn}"' if mn is not None else ""
    a += f' max="{mx}"' if mx is not None else ""
    return f'<label>{label}<input type="number" id="{id_}" value="{val}"{a} step="{step}" inputmode="decimal" placeholder="{ph}"></label>'


form = f'''
<form class="fr-in" id="bmForm" onsubmit="return false">
  <div class="fr-step"><span>1</span><b>Your body</b></div>
  <div class="fr-grid">
    {inp("ht", "Height (cm)", 170, 100, 230)}
    {inp("wt", "Weight (kg)", 78, 25, 300, "0.1")}
    {inp("age", "Age", 32, 18, 100)}
    {sel("sex", "Sex", [("m", "Male"), ("f", "Female")], "m")}
  </div>
  {inp("waist", "Waist at the navel (cm, optional but recommended)", 92, 40, 200, "0.5")}
  <div class="fr-step"><span>2</span><b>Your habits now</b></div>
  <div class="fr-grid">
    {sel("steps", "Daily steps", [(2500, "Under 4,000"), (5500, "4,000 to 7,000"), (8500, "7,000 to 10,000"), (11000, "Over 10,000")], 5500)}
    {inp("exmin", "Cardio minutes a week", 60, 0, 1200, "10")}
    {sel("str", "Strength training days a week", [(0, "None"), (1, "1 day"), (2, "2 days"), (3, "3 or more")], 0)}
    {inp("sleep", "Sleep, hours a night", 6.5, 3, 12, "0.5")}
    {inp("sit", "Sitting, hours a day", 9, 0, 18, "0.5")}
    {inp("veg", "Vegetable and fruit servings a day", 2, 0, 15)}
    {inp("sugary", "Sugary drinks or sweet chai a week", 7, 0, 60)}
    {inp("alc", "Alcohol drinks a week", 0, 0, 60)}
  </div>
  <label class="chk"><input type="checkbox" id="smoke"> I smoke or vape</label>
  <label class="chk"><input type="checkbox" id="late"> I usually eat dinner within two hours of sleep</label>
  <div class="fr-step"><span>3</span><b>Recent reports <em class="opt">optional</em></b></div>
  <p class="fr-hint">From a health check or lab report. Leave blank if you do not have them. These never go into the share link.</p>
  <div class="fr-grid">
    {inp("sys", "Blood pressure, top (mmHg)", "", 70, 260, "1", "e.g. 128")}
    {inp("dia", "Blood pressure, bottom (mmHg)", "", 40, 160, "1", "e.g. 84")}
    {inp("fbs", "Fasting glucose (mg/dL)", "", 40, 500, "1", "e.g. 96")}
    {inp("a1c", "HbA1c (%)", "", 3, 15, "0.1", "e.g. 5.6")}
    {inp("alt", "SGPT / ALT (U/L)", "", 1, 1000, "1", "e.g. 38")}
  </div>
</form>'''

page = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try{{if(localStorage.getItem('sh_theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Syed Hadi">
<meta name="theme-color" content="#5b3df5">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Syed Hadi">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}/img/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/img/og-card.jpg">
<script type="application/ld+json">{json.dumps(JSONLD, ensure_ascii=False)}</script>
{icons}
<style>
.bm-hero{{background:linear-gradient(160deg,#ecfdf5 0%,#eef2ff 55%,#fff7ed 100%)}}
[data-theme=dark] .bm-hero{{background:linear-gradient(160deg,#0f2a1c 0%,#15173a 55%,#2a1a10 100%)}}
.bm-hero .wrap{{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;align-items:center}}
.bm-art{{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}}
.bm-art img{{width:100%;height:100%;object-fit:cover;display:block}}
.fr-in select{{width:100%;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:600 16px Inter,sans-serif}}
.fr-in .chk{{display:flex;gap:10px;align-items:center;font-weight:500;color:var(--ink-2);font-size:14px;grid-template-columns:none}}
.fr-in .chk input{{width:18px;height:18px;accent-color:var(--accent)}}
.fr-step em.opt{{font:500 12px "JetBrains Mono",monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-style:normal;margin-left:6px}}
.fr-out.dim{{opacity:.45}}
.bm-head{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}}
.bm-band{{font:700 14px Inter;padding:6px 12px;border-radius:999px}}
.b-ok{{background:rgba(16,185,129,.15);color:#047857}} .b-over,.b-under{{background:rgba(245,158,11,.18);color:#b45309}} .b-ob{{background:rgba(244,63,94,.14);color:#be123c}}
[data-theme=dark] .b-ok{{color:#6ee7b7}} [data-theme=dark] .b-over,[data-theme=dark] .b-under{{color:#fcd34d}} [data-theme=dark] .b-ob{{color:#fda4af}}
.gauge{{position:relative;height:12px;border-radius:999px;display:flex;overflow:visible;margin:22px 0 26px}}
.gauge i{{display:block;height:100%}} .gauge i.u{{border-radius:999px 0 0 999px}} .gauge i.xx{{border-radius:0 999px 999px 0}}
.gauge .u{{width:17.5%;background:#fcd34d}} .gauge .n{{width:22.5%;background:#34d399}} .gauge .o{{width:10%;background:#fbbf24}} .gauge .x{{width:25%;background:#fb7185}} .gauge .xx{{width:25%;background:#e11d48}}
.gauge b{{position:absolute;top:-6px;width:4px;height:24px;border-radius:3px;background:var(--ink);transform:translateX(-50%);transition:left .4s var(--ease);box-shadow:0 0 0 3px var(--card)}}
.gauge small{{position:absolute;top:18px;font:500 11px "JetBrains Mono",monospace;color:var(--ink-3);transform:translateX(-50%)}}
.bm-sec{{background:var(--bg-soft)}}
.tbl-wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:16px;background:var(--card)}}
.tbl-wrap table,.ins-t{{width:100%;border-collapse:collapse;font-size:14.5px}}
.tbl-wrap th,.tbl-wrap td{{padding:12px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.5}}
.tbl-wrap thead th{{font:600 12px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);background:var(--bg-soft)}}
.tbl-wrap tr:last-child td,.tbl-wrap tr:last-child th{{border-bottom:0}}
.ins-t{{margin:0}} .ins-t+.ins-t{{border-top:8px solid var(--bg-soft)}}
.ins-t td:first-child{{width:32%}} .ins-t td b{{font-size:15px}}
.ins-t thead th.st{{color:#047857}} .ins-t thead th.sp{{color:#be123c}}
[data-theme=dark] .ins-t thead th.st{{color:#6ee7b7}} [data-theme=dark] .ins-t thead th.sp{{color:#fda4af}}
.ins-t tbody td:first-child{{border-left:4px solid #10b981}} .ins-t.stop tbody td:first-child{{border-left-color:#f43f5e}}
.chip{{display:inline-block;font:600 12.5px/1.35 Inter;padding:4px 10px;border-radius:12px;white-space:normal;max-width:220px}}
#mk td:last-child{{width:24%}}
.c-green{{background:rgba(16,185,129,.15);color:#047857}} .c-amber{{background:rgba(245,158,11,.18);color:#b45309}} .c-rose{{background:rgba(244,63,94,.14);color:#be123c}}
[data-theme=dark] .c-green{{color:#6ee7b7}} [data-theme=dark] .c-amber{{color:#fcd34d}} [data-theme=dark] .c-rose{{color:#fda4af}}
.trk table{{width:100%;border-collapse:collapse;min-width:620px}}
.trk th,.trk td{{padding:9px 8px;border-bottom:1px solid var(--line);text-align:center;font-size:14px;vertical-align:middle}}
.trk thead th:first-child{{text-align:left}}
.trk tbody th{{text-align:left;font-weight:600;min-width:200px}}
.trk thead th{{font:600 12px "JetBrains Mono",monospace;letter-spacing:.06em;color:var(--ink-3);background:var(--bg-soft)}}
.trk thead th.today{{color:var(--accent)}}
.tk{{width:34px;height:34px;border-radius:10px;border:1.5px solid var(--line);background:var(--bg);color:#fff;font:800 16px Inter;cursor:pointer;transition:background .15s,border-color .15s,transform .1s}}
.tk:hover{{border-color:var(--accent)}} .tk.today{{border-color:var(--accent)}} .tk.on{{background:var(--accent);border-color:var(--accent)}} .tk:active{{transform:scale(.94)}}
.trk td.wk{{font:600 13px "JetBrains Mono",monospace;color:var(--ink-2)}}
.trk-top{{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:0 0 14px}}
.trk-top b{{font-family:"Plus Jakarta Sans";font-size:34px;letter-spacing:-.03em;color:var(--accent)}}
.trk-bar{{flex:1;min-width:180px;height:10px;border-radius:999px;background:var(--line);overflow:hidden}} .trk-bar i{{display:block;height:100%;width:0;background:var(--accent);transition:width .4s var(--ease)}}
.bm-photos{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}}
.bm-photos figure{{margin:0;border-radius:16px;overflow:hidden;position:relative;aspect-ratio:4/3}}
.bm-photos img{{width:100%;height:100%;object-fit:cover;display:block}}
.bm-photos figcaption{{position:absolute;left:12px;bottom:12px;right:12px;color:#fff;font:700 15px Inter;text-shadow:0 2px 12px rgba(0,0,0,.55)}}
.bm-disc{{border:1px solid rgba(245,158,11,.45);background:rgba(245,158,11,.10);border-radius:14px;padding:14px 16px;font-size:14px;line-height:1.55;color:var(--ink-2)}}
@media (max-width:980px){{.bm-hero .wrap{{grid-template-columns:1fr}}.bm-art{{max-width:520px}}}}
@media (max-width:720px){{.bm-photos{{grid-template-columns:1fr}}.ins-t td:first-child{{width:40%}}.tbl-wrap th,.tbl-wrap td{{padding:10px}}}}
</style>
</head>
<body data-page="bmicalc">
{nav}
<header class="page-hero bm-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/calculator">Calculators</a> / BMI calculator</div>
<h1 class="display" style="font-size:clamp(34px,4.6vw,60px)">Know your BMI. Then build the <span>habits</span> that move it.</h1>
<p>BMI scored on the Indian cut offs, the healthy weight for your height and your waist to height ratio. Add any recent BP, sugar or SGPT reading and get a plain table of what to start doing and what to stop, plus a 7 day habits tracker you can tick daily and print.</p>
</div>
<div class="bm-art"><img src="{uns('1512621776951-a57141f2eefd', 880, 605)}" alt="Bowl of fresh vegetables, chickpeas and avocado" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">

<section class="bx-sec" style="padding-top:24px" id="calculator">
  <div class="wrap fr-wrap">
    {form}
    <a class="fr-mbar" href="#out" id="mbar"><span>BMI <b id="mN">-</b></span><em>See the plan</em></a>
    <div class="fr-out" id="out" aria-live="polite">
      <div class="fr-verdict" id="vd"></div>
      <div class="fr-big"><small>Your BMI</small><div class="bm-head"><b id="oBmi">-</b><span class="bm-band" id="oBand"></span></div><span id="oBmiS"></span></div>
      <div class="gauge" aria-hidden="true"><i class="u"></i><i class="n"></i><i class="o"></i><i class="x"></i><i class="xx"></i><b id="gPin"></b>
        <small style="left:17.5%">18.5</small><small style="left:40%">23</small><small style="left:50%">25</small><small style="left:75%">30</small></div>
      <div class="fr-kpis">
        <div><small>Healthy weight for you</small><b id="oRange">-</b><span id="oRangeS"></span></div>
        <div><small>Waist to height</small><b id="oWhtr">-</b><span id="oWhtrS"></span></div>
        <div style="grid-column:span 2"><small>Your first goal</small><b id="oGoal">-</b><span id="oGoalS"></span></div>
      </div>
      <div class="fr-acts"><button type="button" class="btn btn-primary sc-pdfbtn" id="pdfBtn">Download my BMI and habits plan (PDF)</button><button type="button" class="btn btn-ghost" id="share">Copy link</button></div>
      <p class="fr-hint">The PDF includes your start and stop table, any report readings and a printable 7 day tracker.</p>
    </div>
  </div>
</section>

<section class="bx-sec bm-sec" id="insights">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Your plan</span><h2 class="display">What to Start, What to <span>Stop</span></h2>
    <p>Built from your BMI, waist, habits and any readings you added. Each row says why it matters for you, not for an average person. Change an input above and the table updates.</p></div>
    <div class="tbl-wrap reveal" id="ins"></div>
    <div class="sec-head reveal" style="text-align:left;margin:34px 0 14px"><h3 style="font-family:'Plus Jakarta Sans';font-size:24px;letter-spacing:-.02em;margin:0">Your report readings</h3></div>
    <div class="tbl-wrap reveal" id="mk"></div>
  </div>
</section>

<section class="bx-sec" id="tracker">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Healthy habits tracker</span><h2 class="display">Seven Days, Eight <span>Habits</span></h2>
    <p>Picked from your plan. Tick a box each day you hit the habit. Ticks are saved on this device only and reset every Monday, so each week starts clean.</p></div>
    <div class="trk-top reveal"><b id="trkScore">0%</b><div class="trk-bar"><i id="trkBar"></i></div><button type="button" class="btn btn-ghost" id="trkReset">Clear this week</button></div>
    <p class="fr-hint" id="trkNote" style="margin-bottom:12px"></p>
    <div class="tbl-wrap trk reveal" id="trk"></div>
    <div class="bm-photos">
      <figure class="reveal"><img src="{uns('1476480862126-209bfaa8edc8', 640, 480)}" alt="Running shoes on outdoor stairs" width="640" height="480" loading="lazy" decoding="async"><figcaption>Move: 150 minutes a week</figcaption></figure>
      <figure class="reveal"><img src="{uns('1490645935967-10de6ba17061', 640, 480)}" alt="Plate of vegetables, eggs and avocado" width="640" height="480" loading="lazy" decoding="async"><figcaption>Eat: half the plate vegetables</figcaption></figure>
      <figure class="reveal"><img src="{uns('1517836357463-d25dfeac3438', 640, 480)}" alt="Person lifting a barbell in a gym" width="640" height="480" loading="lazy" decoding="async"><figcaption>Lift: two strength days</figcaption></figure>
    </div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0">
  <div class="wrap cs-two">
    <div class="reveal"><span class="eyebrow">How it works</span><h2 class="display">The Rules Behind the <span>Numbers</span></h2></div>
    <div class="cs-prose reveal">
      <p><b>BMI.</b> Weight in kg divided by height in metres squared. Scored on the Asian Indian bands: healthy 18.5 to 22.9, overweight 23 to 24.9, obesity 25 and above. The WHO global category is shown alongside.</p>
      <p><b>Belly fat.</b> A waist of 90 cm or more for men, 80 cm or more for women, or a waist to height ratio above 0.5. The 2025 revised Indian definition of obesity treats BMI above 23 with excess belly fat as the more serious stage.</p>
      <p><b>Readings.</b> Blood pressure on ACC/AHA bands, fasting glucose and HbA1c on ADA cut offs, SGPT on gastroenterology healthy limits (33 U/L men, 25 U/L women).</p>
      <p><b>The plan.</b> Each start or stop row is triggered by your numbers: activity under 150 minutes, steps under 7,000, sleep under 7 hours, sitting 6 hours or more, sugary drinks, or a flagged reading. Activity targets follow WHO guidance.</p>
      <div class="bm-disc"><b>Not medical advice.</b> This tool is for education and habit building. It does not diagnose anything. Talk to a doctor about any flagged reading, and get care the same day for blood pressure of 180 / 120 or more.</div>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap bx-faqwrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">FAQ</span><h2 class="display">Common Questions</h2></div>
    <div class="sp-faq-list reveal">{faq_html}</div>
    <p class="fr-disc">References: Misra A et al., Revised definition of obesity in Asian Indians living in India, Diabetes and Metabolic Syndrome, 2025; WHO guidelines on physical activity, 2020; ACC/AHA blood pressure guideline, 2017; ADA Standards of Care; ACG clinical guideline on abnormal liver chemistries, 2017. This calculator is for education only and is not a substitute for medical advice.</p>
  </div>
</section>
<script src="/assets/bmi-calculator.js?v={VER}"></script>
<script src="/assets/calc-reports.js?v={VER}" defer></script>
</main>
{tail}{foot}
</body>
</html>
'''
open(os.path.join(ROOT, "bmi-calculator.html"), "w", encoding="utf-8").write(page)
print("bmi-calculator.html written", len(page))
