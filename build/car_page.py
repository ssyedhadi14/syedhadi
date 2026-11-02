#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate /car-mileage-calculator for syedcreates.com (fuel per month, running cost by city, tank range, service reserve, PDF)
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
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/loan-calculator"><small>PREVIOUS</small><b>&larr; Loan EMI Calculator</b></a><a class="right" href="/salary-calculator"><small>NEXT</small><b>Salary Growth Calculator &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/car-mileage-calculator"
TITLE = "Car Mileage and Running Cost Calculator India: Fuel Per Month, Per Km"
DESC = "Enter your monthly kilometres, mileage and petrol price. Get litres per month, fuel cost by city, cost per km, tank range and a yearly running cost with service. Free PDF."

FAQ = [
    ("How do I calculate my car's monthly fuel cost?",
     "Divide the kilometres you drive in a month by your car's mileage to get litres, then multiply by the pump price. A Fronx doing 1,000 km a month at 15 km/L needs 66.7 litres. At ₹110.93 a litre in Bengaluru that is about ₹7,395 a month and ₹88,744 a year. The same car in Delhi at ₹102 costs ₹6,800 a month."),
    ("What is the real mileage of the Maruti Suzuki Fronx?",
     "ARAI rates the 1.2L petrol manual at about 21.8 km/L and the 1.0L turbo at 20 to 21 km/L. In city traffic with the AC on, owners report 13 to 16 km/L for the 1.2L and 14 to 17 for the turbo. Highway runs do 18 to 22. This calculator defaults to 15 km/L, a fair city figure. Put in what your trip computer shows after a full tank."),
    ("How far does a Fronx go on a full tank?",
     "The tank holds 37 litres. At 15 km/L that is about 555 km of city range, at 20 km/L about 740 km on the highway. Driving 1,000 km a month means roughly two fill ups a month."),
    ("How much does yearly service cost for a Fronx?",
     "Maruti schedules service every 10,000 km or one year. Paid services at an authorised workshop run roughly ₹4,500 to ₹6,500 a year for oil, filters, inspection and alignment. Keep another ₹1,500 to ₹2,500 for wipers, fluids and the AC filter. The calculator lets you set both numbers."),
    ("What is cost per kilometre and why does it matter?",
     "Cost per km is your total monthly running cost divided by kilometres driven. It is the honest way to compare a car with cabs, a second car or an EV. At ₹7,900 a month for 1,000 km the Fronx costs about ₹7.90 per km on fuel and service alone, before insurance, parking and depreciation."),
    ("Does this calculator store my data?",
     "No. Everything is computed in your browser. The share link carries your inputs in the URL so you can reopen the same numbers later. The PDF is built on your device."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-11-02"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/calculator"},
        {"@type": "ListItem", "position": 3, "name": "Car mileage calculator", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "Car Mileage and Running Cost Calculator", "url": URL, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "isAccessibleForFree": True,
     "description": "Litres per month, fuel cost by city, cost per km, tank range and yearly running cost with service, for any car in India.",
     "featureList": ["Litres and fuel cost per month and year", "Fuel cost compared across Indian cities", "Cost per kilometre", "Tank range and fill ups per month", "Service and wear reserve", "PDF report"],
     "author": {"@id": SITE + "/#person"}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
faq_html = "".join(f'<details class="sp-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

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
.cm-hero{{background:linear-gradient(160deg,#fff7ed 0%,#eef2ff 55%,#f0fdf4 100%)}}
[data-theme=dark] .cm-hero{{background:linear-gradient(160deg,#2a1a10 0%,#15173a 55%,#0f2a1c 100%)}}
.cm-hero .wrap{{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;align-items:center}}
.cm-art{{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}}
.cm-art img{{width:100%;height:100%;object-fit:cover;display:block}}
.cm-city{{display:flex;gap:8px;flex-wrap:wrap;margin-top:-2px}}
.cm-city button{{border:1.5px solid var(--line);background:var(--bg);color:var(--ink-2);font:600 13px Inter;padding:8px 12px;border-radius:999px;cursor:pointer;display:flex;gap:6px;align-items:center}}
.cm-city button small{{font:600 12px "JetBrains Mono",monospace;color:var(--ink-3)}}
.cm-city button.on{{background:var(--accent);border-color:var(--accent);color:#fff}} .cm-city button.on small{{color:#fff;opacity:.85}}
.fr-out.dim{{opacity:.45}}
.fr-chart .grid{{stroke:var(--line);stroke-width:1}} .fr-chart .tk{{font:600 11px "JetBrains Mono",monospace;fill:var(--ink-3)}} .fr-chart .tk2{{font:500 10px "JetBrains Mono",monospace;fill:var(--ink-3)}}
.fr-chart .b{{fill:#c7d2fe}} [data-theme=dark] .fr-chart .b{{fill:#3b3f7a}} .fr-chart .me{{fill:var(--accent)}} .fr-chart .vl{{font:700 12px Inter;fill:var(--ink)}}
.cm-tip{{padding:14px 16px;border-radius:14px;background:var(--accent-soft);font-size:14.5px;line-height:1.55;color:var(--ink-2)}}
.cm-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.cm-3 div{{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)}}
.cm-3 b{{display:block;font-size:16px;margin-bottom:6px}} .cm-3 p{{font-size:14px;color:var(--ink-2);margin:0;line-height:1.55}}
.fr-kpis div.wide{{grid-column:span 2}}
@media (max-width:980px){{.cm-hero .wrap{{grid-template-columns:1fr}}.cm-art{{max-width:520px}}}}
@media (max-width:720px){{.cm-3{{grid-template-columns:1fr}}}}
</style>
</head>
<body data-page="carcalc">
{nav}
<header class="page-hero cm-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/calculator">Calculators</a> / Car mileage calculator</div>
<h1 class="display" style="font-size:clamp(34px,4.6vw,60px)">What your car <span>really costs</span> to run every month.</h1>
<p>Kilometres, mileage, pump price. That is all it takes to see litres per month, fuel cost in your city versus others, cost per km, tank range and a yearly number with service counted. Pre filled for a Maruti Suzuki Fronx doing 1,000 km a month in Bengaluru. Change anything.</p>
</div>
<div class="cm-art"><img src="{uns('1449965408869-eaa3f722e40d', 880, 605)}" alt="Car driving on an open road at golden hour" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">

<section class="bx-sec" style="padding-top:24px" id="calculator">
  <div class="wrap fr-wrap">
    <form class="fr-in" id="cmForm" onsubmit="return false">
      <div class="fr-step"><span>1</span><b>Your car and driving</b></div>
      <label>Car<input type="text" id="car" value="Maruti Suzuki Fronx" maxlength="40"></label>
      <div class="fr-grid">
        <label>Kilometres per month<input type="number" id="km" min="1" max="20000" step="10" value="1000" inputmode="numeric"></label>
        <label>Mileage (km per litre)<input type="number" id="kmpl" min="1" max="60" step="0.1" value="15" inputmode="decimal"></label>
      </div>
      <div class="fr-step"><span>2</span><b>Fuel price</b></div>
      <div class="cm-city" id="cityChips" aria-label="Pick a city to fill the petrol price"></div>
      <label>Petrol price per litre (&#8377;)<input type="number" id="price" min="1" max="300" step="0.01" value="110.93" inputmode="decimal"></label>
      <p class="fr-hint">City prices are approximate and change daily. Type today's pump price for an exact number.</p>
      <div class="fr-step"><span>3</span><b>Tank and yearly upkeep</b></div>
      <div class="fr-grid">
        <label>Fuel tank (litres)<input type="number" id="tank" min="0" max="200" step="1" value="37" inputmode="numeric"></label>
        <label>Annual service (&#8377;)<input type="number" id="service" min="0" step="100" value="5500" inputmode="numeric"></label>
        <label>Wear and tear reserve per year (&#8377;)<input type="number" id="wear" min="0" step="100" value="2000" inputmode="numeric"></label>
        <label>Insurance per year (&#8377;, optional)<input type="number" id="ins" min="0" step="100" value="0" inputmode="numeric"></label>
      </div>
    </form>

    <a class="fr-mbar" href="#out" id="mbar"><span>Running cost <b id="mN">-</b></span><em>See the breakdown</em></a>
    <div class="fr-out" id="out" aria-live="polite">
      <div class="fr-verdict ok" id="vd"></div>
      <div class="fr-big"><small>Fuel cost per month</small><b id="oFuel">-</b><span id="oFuelS"></span></div>
      <div class="fr-kpis">
        <div><small>Petrol needed</small><b id="oLit">-</b><span id="oLitS"></span></div>
        <div><small>Cost per km</small><b id="oKm">-</b><span id="oKmS"></span></div>
        <div><small>Running cost per month</small><b id="oTotal">-</b><span id="oTotalS"></span></div>
        <div><small>Running cost per year</small><b id="oYear">-</b><span id="oYearS"></span></div>
        <div class="wide"><small>Full tank range</small><b id="oRange">-</b><span id="oRangeS"></span></div>
      </div>
      <div class="fr-chart"><svg id="chart" viewBox="0 0 640 230" role="img" aria-label="Monthly fuel cost for the same driving in Delhi, Bengaluru and Hyderabad"></svg>
        <div class="fr-legend"><i class="a"></i>Monthly fuel cost by city, your price highlighted</div></div>
      <div class="cm-tip" id="tip"></div>
      <div class="fr-acts"><button type="button" class="btn btn-primary sc-pdfbtn" id="pdfBtn">Download my running cost report (PDF)</button><button type="button" class="btn btn-ghost" id="share">Copy link to these numbers</button></div>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap cs-two">
    <div class="reveal"><span class="eyebrow">How it works</span><h2 class="display">Three Lines of Maths</h2></div>
    <div class="cs-prose reveal">
      <p><b>1. Litres.</b> Kilometres per month ÷ mileage. 1,000 km at 15 km/L is 66.67 litres.</p>
      <p><b>2. Fuel cost.</b> Litres × pump price. At ₹110.93 a litre that is ₹7,395 a month, ₹88,744 a year. Petrol price varies by state tax, so the same car costs ₹6,800 a month in Delhi and ₹7,767 in Hyderabad.</p>
      <p><b>3. Running cost.</b> Fuel plus a twelfth of your yearly service, wear and insurance. Divide by kilometres and you get cost per km, the number to compare with cabs or an EV.</p>
      <p><b>Tank range</b> is tank size × mileage. A 37 litre Fronx at 15 km/L runs about 555 km per fill, so 1,000 km a month is roughly two visits to the pump.</p>
    </div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Cut the bill</span><h2 class="display">Three Habits Worth ₹1,000 a Month</h2></div>
    <div class="cm-3">
      <div class="reveal"><b>Tyre pressure, every fortnight</b><p>Under inflated tyres cost 3 to 5% in mileage. Check cold, fill to the door sticker figure, and nitrogen is not required.</p></div>
      <div class="reveal"><b>Smooth throttle, early upshifts</b><p>Shift by 2,000 rpm, lift off early for red lights and keep a steady 80 to 90 on the highway. This alone moves a Fronx from 13 to 16 km/L in traffic.</p></div>
      <div class="reveal"><b>Idle less, plan more</b><p>Ten minutes of idling a day burns about 3 litres a month. Combine errands, avoid peak hour where you can, and switch off at long signals.</p></div>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap bx-faqwrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">FAQ</span><h2 class="display">Common Questions</h2></div>
    <div class="sp-faq-list reveal">{faq_html}</div>
    <p class="fr-disc">Fuel prices, service costs and mileage figures are indicative and change by city, dealer and driving style. This tool is for planning only. Check your trip computer and your workshop's price list for exact numbers.</p>
  </div>
</section>
<script src="/assets/car-mileage-calculator.js?v={VER}"></script>
<script src="/assets/calc-reports.js?v={VER}" defer></script>
</main>
{tail}{foot}
</body>
</html>
'''
open(os.path.join(ROOT, "car-mileage-calculator.html"), "w", encoding="utf-8").write(page)
print("car-mileage-calculator.html written", len(page))
