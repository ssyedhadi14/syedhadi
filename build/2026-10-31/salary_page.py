#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Generate /salary-calculator for syedcreates.com from the 2026 Salary Tracker workbook model
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
tail = re.search(r"</main>\s*(.*?)<footer class=\"site-foot\">", shell, re.S).group(1)  # peer note, cta, next page, newsletter
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/fire-calculator"><small>PREVIOUS</small><b>&larr; FIRE Calculator</b></a><a class="right" href="/mutual-fund-returns-calculator"><small>NEXT</small><b>Mutual Fund Returns &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/salary-calculator"
TITLE = "Salary Growth Calculator India: 45 Year Projection"
DESC = "Free salary growth calculator for India. Enter in hand salary, spends and increment to see salary, savings and corpus over 45 years, then get the PDF by email."

FAQ = [
    ("How does the salary growth calculator work?",
     "It takes your current monthly in hand salary and grows it every year by your expected increment. Each year it subtracts your needs and wants, which grow at their own rates, and invests what is left. The investable amount is split between PPF and equity, compounded to the age you pick and then discounted by inflation so you also see the value in today's money."),
    ("Why is the PPF share equal to my age?",
     "It follows the common thumb rule that the share of debt in a portfolio should roughly match your age. At 27 you put 27% of your monthly surplus in PPF and 73% in equity. The share rises by one point every year, so the plan gets safer as you get older. You can switch to a fixed split in the assumptions."),
    ("What returns and tax does the calculator assume?",
     "By default PPF compounds at 8% a year with no tax, equity at 15% a year with 10% long term capital gains tax applied on the gains when you sell, and inflation runs at 5%. Every number is editable and none of them is a promise. Try lower returns to stress test the plan."),
    ("What does the value in today's money mean?",
     "A corpus of 2 crore in 2040 does not buy what 2 crore buys today. The calculator divides the projected corpus by inflation compounded over the same years, so you can compare the future number with prices you understand now."),
    ("Does the calculator store my salary?",
     "No. Everything runs in your browser. Nothing leaves the page unless you choose to email yourself the PDF, in which case the report and your email address are sent through the mail service once and are not stored in a database."),
    ("Is this financial advice?",
     "No. It is a planning tool built from a spreadsheet that I use myself. Returns can be lower, increments can stop and life happens. Use it to see the shape of your plan, then speak to a SEBI registered adviser before you commit money."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC,
     "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-10-31",
     "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/img/og-card.jpg", "width": 1200, "height": 630}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/tools#calculators"},
        {"@type": "ListItem", "position": 3, "name": "Salary growth calculator", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "Salary Growth Calculator India", "url": URL,
     "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
     "description": "Projects salary, monthly needs and wants, investable surplus and the PPF plus equity corpus for the next 45 years, with a downloadable and emailed PDF report.",
     "featureList": ["45 year salary projection", "Needs and wants with separate growth rates", "Age based PPF and equity split", "Inflation adjusted corpus", "Crorepati milestone ages", "Vector PDF report", "Email the report to yourself"],
     "author": {"@id": SITE + "/#person"}, "creator": {"@id": SITE + "/#person"}, "inLanguage": "en-IN", "isAccessibleForFree": True},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}

faq_html = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

NEEDS = [("rent", "Rent or home EMI", 19500, 10), ("emi", "Essential EMIs", 15000, 0), ("food", "Groceries and food", 10000, 5),
         ("fuel", "Fuel and commute", 5000, 5), ("bills", "Bills, gas, internet, power", 3000, 5), ("fees", "School or course fees", 0, 5),
         ("family", "Money sent home", 0, 5), ("needx", "Other needs", 0, 5)]
WANTS = [("clothes", "Clothes and shopping", 5000, 5), ("eatout", "Eating out and delivery", 5000, 5),
         ("gadgets", "Gadget and lifestyle EMIs", 0, 5), ("travel", "Vacations", 5000, 5), ("wantx", "Other wants", 0, 5)]


def item_rows(items):
    out = ""
    for k, label, v, g in items:
        out += (f'<div class="sc-item"><label class="fr-money">{label} (₹ per month)<input id="{k}" inputmode="numeric" type="text" value="{v:,}" data-money><small id="{k}W"></small></label>'
                f'<label>Grows yearly (%)<input id="{k}G" type="number" min="0" max="30" step="1" value="{g}"></label></div>')
    return out


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
.sc-hero{{background:linear-gradient(160deg,#ecfdf5 0%,#eef2ff 55%,#fdf4ff 100%)}}
[data-theme=dark] .sc-hero{{background:linear-gradient(160deg,#0f2a22 0%,#15173a 55%,#2a1030 100%)}}
.sc-hero .wrap{{display:grid;grid-template-columns:1.2fr .8fr;gap:32px;align-items:center}}
.sc-hero-art{{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}}
.sc-hero-art img{{width:100%;height:100%;object-fit:cover;display:block}}
.sc-pills{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.sc-pills span{{font:600 12.5px Inter;padding:7px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--ink-2)}}
.sc-item{{display:grid;grid-template-columns:1.6fr .8fr;gap:10px}}
.sc-group{{border:1px solid var(--line);border-radius:14px;padding:12px;display:grid;gap:10px;background:var(--bg)}}
.sc-group summary{{cursor:pointer;font-weight:700;display:flex;justify-content:space-between;gap:10px}}
.sc-group summary em{{font-style:normal;color:var(--accent);font-weight:700}}
.sc-range{{display:grid;gap:6px}}
.sc-range input[type=range]{{width:100%;accent-color:var(--accent)}}
.sc-range .lbl{{display:flex;justify-content:space-between;font-size:13px;color:var(--ink-3)}}
.sc-milestones{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.sc-milestones div{{border:1px solid var(--line);border-radius:12px;padding:10px;text-align:center;background:linear-gradient(180deg,var(--accent-soft),var(--card))}}
.sc-milestones b{{display:block;font-family:"Bricolage Grotesque";font-size:22px;color:var(--accent)}}
.sc-milestones span{{font-size:11.5px;color:var(--ink-3);line-height:1.35;display:block}}
.sc-legend{{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--ink-3);margin-top:6px}}
.sc-legend i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-2px}}
.sc-tabs{{display:flex;gap:6px;flex-wrap:wrap}}
.sc-tabs button{{font:600 13px Inter;padding:8px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer}}
.sc-tabs button.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
.sc-mail{{border:1px solid var(--accent);border-radius:16px;padding:16px;background:linear-gradient(120deg,var(--accent-soft),var(--card));display:grid;gap:10px}}
.sc-mail .sc-mail-h{{font-family:"Bricolage Grotesque";font-size:20px;margin:0}}
.sc-mail .row{{display:grid;grid-template-columns:1fr 1.3fr auto;gap:8px}}
.sc-mail input[type=text],.sc-mail input[type=email]{{width:100%;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:600 15px Inter}}
.sc-mail label.ck{{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;color:var(--ink-2);font-weight:500}}
.sc-mail .msg{{font-size:13px;min-height:18px}}
.sc-mail .msg.ok{{color:#059669}} .sc-mail .msg.err{{color:#dc2626}}
.sc-pdfbtn{{position:relative;overflow:hidden}}
.sc-pdfbtn::after{{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);animation:scShine 2.8s ease-in-out infinite}}
@keyframes scShine{{0%{{left:-60%}}60%,100%{{left:130%}}}}
.sc-how{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}}
.sc-how div{{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)}}
.sc-how i{{font:800 13px "JetBrains Mono",monospace;color:var(--accent)}}
.sc-how b{{display:block;font-size:17px;margin:8px 0 6px}}
.sc-how p{{font-size:14px;color:var(--ink-2);margin:0}}
.sc-formula{{font-family:"JetBrains Mono",monospace;font-size:13px;background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:14px 16px;overflow:auto;white-space:pre}}
.faq{{border:1px solid var(--line);border-radius:14px;padding:14px 18px;background:var(--card);margin-bottom:10px}}
.faq summary{{cursor:pointer;font-weight:700;font-size:16px}}
.faq p{{color:var(--ink-2);margin:10px 0 0;line-height:1.6}}
@media (max-width:980px){{.sc-hero .wrap{{grid-template-columns:1fr}}.sc-hero-art{{max-width:520px}}}}
@media (max-width:860px){{.fr-wrap{{grid-template-columns:1fr}}.fr-out{{position:static}}.sc-how{{grid-template-columns:1fr}}.sc-mail .row{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.sc-item{{grid-template-columns:1fr}}.sc-milestones{{grid-template-columns:1fr 1fr}}.fr-grid{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{.sc-pdfbtn::after{{animation:none}}}}
</style>
</head>
<body data-page="salarycalc">
{nav}
<header class="page-hero sc-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/tools#calculators">Calculators</a> / Salary growth</div>
<h1 class="display">Where does your <span>salary</span> take you in 45 years?</h1>
<p>Enter today's in hand salary, what you spend and the increment you expect. See your salary, your monthly surplus and the PPF plus equity corpus it builds, year by year to 45 years out, in rupees and in today's money. Then download the PDF or get it in your inbox.</p>
<div class="sc-pills"><span>Built for India</span><span>PPF + equity split by age</span><span>Inflation adjusted</span><span>Free, no sign up</span><span>Nothing stored</span></div>
</div>
<div class="sc-hero-art"><img src="{uns('1579621970563-ebec7560ff3e', 880, 605)}" alt="Young plant growing out of a pile of coins, a picture of money compounding over time" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">
<section class="bx-sec" style="padding-top:24px">
<div class="wrap fr-wrap">
<form class="fr-in" id="scForm" onsubmit="return false" aria-label="Salary growth inputs">
<div class="fr-step"><span>1</span><b>About you</b></div>
<div class="fr-grid">
<label>Your age today<input id="age" inputmode="numeric" type="number" min="18" max="65" value="27"></label>
<label class="fr-money">In hand salary per month (₹)<input id="sal" inputmode="numeric" type="text" value="1,13,625" data-money><small id="salW"></small></label>
<label>Expected yearly increment (%)<input id="inc" type="number" min="0" max="40" step="0.5" value="10"></label>
<label>Check the corpus at age<input id="tgt" type="number" min="19" max="100" value="37"></label>
</div>
<p class="fr-hint">In hand means after tax, PF and other deductions, the amount that reaches your bank.</p>
<details class="sc-group" open>
<summary><span class="stn">2</span><b>Monthly needs</b><em id="needsT"></em><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg></summary>
{item_rows(NEEDS)}
<p class="fr-hint">Rent usually rises faster than groceries, so each item has its own growth rate. EMIs are fixed, so they grow at 0%.</p>
</details>
<details class="sc-group" open>
<summary><span class="stn">3</span><b>Monthly wants</b><em id="wantsT"></em><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg></summary>
{item_rows(WANTS)}
</details>
<details class="fr-adv">
<summary><span class="stn">4</span><b>Investing assumptions</b><em>optional</em></summary>
<div class="fr-grid">
<label>PPF share of surplus<select id="splitMode" class="tselect" style="width:100%"><option value="age">Same as my age (27 at 27, 28 at 28...)</option><option value="fixed">Fixed percentage</option></select></label>
<label>Fixed PPF share (%)<input id="ppfPct" type="number" min="0" max="100" step="5" value="30" disabled></label>
<label>PPF return per year (%)<input id="rp" type="number" min="0" max="12" step="0.1" value="8"></label>
<label>Equity return per year (%)<input id="re" type="number" min="0" max="25" step="0.5" value="15"></label>
<label>Long term capital gains tax (%)<input id="ltcg" type="number" min="0" max="30" step="0.5" value="10"></label>
<label>Inflation per year (%)<input id="inf" type="number" min="0" max="15" step="0.5" value="5"></label>
<label>Years to project<input id="hz" type="number" min="10" max="60" value="45"></label>
<label>Stop investing at age<input id="stopAge" type="number" min="25" max="100" value="60"></label>
</div>
<p class="fr-hint">Defaults match the spreadsheet this tool was built from: PPF 8% tax free, equity 15% with 10% LTCG on gains, inflation 5%. Returns are planning assumptions, not promises.</p>
</details>
</form>

<a class="fr-mbar" href="#scOut" id="mbar"><span>Corpus at <span id="mAge">37</span> <b id="mN">-</b></span><em>See result</em></a>
<div class="fr-out" id="scOut" aria-live="polite">
<div class="fr-verdict ok" id="vd"></div>
<div class="fr-big"><small>Corpus at age <span id="kTgt">37</span></small><b id="corpN">-</b><span id="corpS"></span></div>
<div class="sc-range"><input type="range" id="tgtR" min="19" max="72" value="37" aria-label="Scrub the age you want to check"><div class="lbl"><span>Drag to any age</span><span id="tgtLbl">Age 37, year 2036</span></div></div>
<div class="fr-kpis">
<div><small>Investable per month now</small><b id="invNow">-</b><span id="invPct"></span></div>
<div><small>Salary per month at <span id="kTgt2">37</span></small><b id="salT">-</b><span id="salTS"></span></div>
<div><small>Total you put in</small><b id="putIn">-</b><span>by that age</span></div>
<div><small>Growth earned</small><b id="gain">-</b><span id="gainS"></span></div>
</div>
<div class="sc-milestones" id="miles"></div>
<div class="sc-tabs" role="tablist" aria-label="Chart type"><button class="on" data-ch="corpus" type="button">Corpus growth</button><button data-ch="flow" type="button">Salary vs spend</button><button data-ch="real" type="button">Today's money</button></div>
<div class="fr-chart"><svg id="chart" role="img" aria-label="Salary and corpus projection chart" viewBox="0 0 640 280"></svg><div class="sc-legend" id="legend"></div></div>
<div class="fr-acts"><button class="btn btn-primary sc-pdfbtn" id="pdfBtn" type="button">Download PDF report</button><button class="btn btn-ghost" id="tblBtn" type="button">Show year by year table</button><button class="btn btn-ghost" id="share" type="button">Copy link to my plan</button></div>
<div class="fr-tbl" hidden id="tbl"></div>
<form class="sc-mail" id="mailForm" novalidate>
<h2 class="sc-mail-h">Email me the PDF report</h2>
<div class="row"><input type="text" id="mName" name="name" placeholder="Your first name" autocomplete="given-name" maxlength="60"><input type="email" id="mEmail" name="email" placeholder="you@example.com" autocomplete="email" required><button class="btn btn-primary" type="submit" id="mailBtn">Send it</button></div>
<input type="text" name="company" id="mHoney" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden">
<label class="ck"><input type="checkbox" id="mConsent" required><span>Send me the report. Syed gets a copy of my email address and may follow up once. No spam, no list, see the <a href="/privacy">privacy note</a>.</span></label>
<div class="msg" id="mMsg" role="status"></div>
</form>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">How it works</span><h2 class="display">The Math Behind the Projection</h2>
<p>The calculator is the spreadsheet I have used since my first job, turned into a page. Six rules drive every number on the screen.</p></div>
<div class="sc-how">
<div class="reveal"><i>01</i><b>Salary compounds by your increment</b><p>Year one is your in hand salary times 12. Every year after that multiplies the previous year by one plus your increment.</p></div>
<div class="reveal"><i>02</i><b>Needs and wants grow separately</b><p>Rent grows at its own rate, EMIs stay flat, the rest follows inflation. Each line item compounds on its own, so lifestyle creep shows up in the numbers.</p></div>
<div class="reveal"><i>03</i><b>What is left gets invested</b><p>Income minus needs minus wants is your yearly surplus. If spends ever cross income the surplus is zero for that year, never negative.</p></div>
<div class="reveal"><i>04</i><b>PPF share equals your age</b><p>At 27, 27% of the surplus goes to PPF and 73% to equity. The split moves one point a year toward safety. Switch to a fixed split if you prefer.</p></div>
<div class="reveal"><i>05</i><b>Every year's money compounds on its own</b><p>Each year's PPF and equity contribution grows from that year to the age you check. Equity gains are taxed at the LTCG rate, PPF is tax free.</p></div>
<div class="reveal"><i>06</i><b>Then we remove inflation</b><p>The corpus is divided by inflation compounded over the same years, which gives the value in today's prices, the number worth planning around.</p></div>
</div>
<div class="sc-formula reveal" style="margin-top:18px">Income(y)   = Salary × 12 × (1 + increment)^y
Surplus(y)  = max(0, Income(y) − Needs(y) − Wants(y))
PPF(y)      = Surplus(y) × share(y)          Equity(y) = Surplus(y) − PPF(y)
Corpus(T)   = Σ PPF(y)(1+r_ppf)^(T−y) + Σ [ Equity(y)(1+r_eq)^(T−y) − tax × gains ]
Real(T)     = Corpus(T) ÷ (1 + inflation)^T</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap cs-two">
<div class="reveal"><span class="eyebrow">Read this first</span><h2 class="display">What the Numbers Can and Cannot Tell You</h2></div>
<div class="cs-prose reveal">
<p><b>A 10% increment is not a law of nature.</b> Indian salaried professionals saw average hikes between 9% and 10% through 2024 and 2025, but the number falls in a slow year and jumps when you switch jobs. Run the calculator at 6% and at 14% and plan for the lower line.</p>
<p><b>Lifestyle creep is the silent variable.</b> The calculator grows your wants at 5% a year. In real life a bigger salary tends to pull wants up with it. If the surplus percentage in the result keeps dropping as the years pass, that is the warning sign.</p>
<p><b>PPF has a ceiling.</b> The scheme caps deposits at 1.5 lakh a year per account. Once your PPF share crosses that, the extra belongs in debt funds, EPF voluntary contributions or NPS. The projection treats it as one debt bucket at 8%.</p>
<p><b>Equity returns arrive in lumps.</b> 15% is close to the long run Nifty total return, but no year delivers exactly 15%. The order of good and bad years matters less while you are still investing every month, which is the whole point of a SIP.</p>
<p><b>Today's money is the honest number.</b> Celebrate the nominal crore when it comes, but plan rent, school fees and retirement with the inflation adjusted line. For a full retirement plan, including how long the money must last, use the <a href="/fire-calculator">FIRE calculator</a>. To see what real funds returned over 5 to 20 years, open the <a href="/mutual-fund-returns-calculator">mutual fund returns tracker</a>.</p>
<p><b>Earning more is the biggest lever.</b> Expenses have a floor, salary does not have a ceiling. If you work in product marketing, check the <a href="/pmm-salary-2026">India PMM salary benchmarks for 2026</a> and the <a href="/jobs">growth and PMM job board</a>.</p>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Common questions</span><h2 class="display">Salary Growth Calculator FAQ</h2></div>
<div class="reveal">{faq_html}</div>
<p class="fr-disc">This calculator is for education and planning only and is not investment, tax or legal advice. Returns are assumptions you control, not predictions. PPF rates are set by the Government of India each quarter and equity returns are not guaranteed. Speak with a SEBI registered investment adviser before acting on any projection. Built by <a href="/about">Syed Hadi</a> in Bengaluru.</p>
</div>
</section>
</main>
{tail}
{foot}
<script src="/assets/common.js?v={VER}"></script>
<script src="/assets/salary-calculator.js?v={VER}" defer></script>
</body>
</html>
'''

open(os.path.join(ROOT, "salary-calculator.html"), "w", encoding="utf-8").write(page)
print("salary-calculator.html written", len(page))
