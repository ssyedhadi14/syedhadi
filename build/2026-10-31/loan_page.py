#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Generate /loan-calculator for syedcreates.com (home, car, personal loan EMI, close in half the time, prepay vs invest)
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
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/fire-calculator"><small>PREVIOUS</small><b>&larr; FIRE Calculator</b></a><a class="right" href="/salary-calculator"><small>NEXT</small><b>Salary Growth Calculator &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/loan-calculator"
TITLE = "Loan EMI Calculator India: Home, Car, Personal + Prepay Planner"
DESC = "EMI, total interest and a plan to close your home, car or personal loan in half the time. Compare prepaying with investing, with Section 24(b) and 80C counted. Free PDF."

FAQ = [
    ("How is a loan EMI calculated?",
     "EMI = P × r × (1 + r)^n ÷ ((1 + r)^n − 1), where P is the amount borrowed, r is the monthly interest rate (annual rate ÷ 12) and n is the number of months. On ₹50 lakh at 8.5% for 20 years that works out to about ₹43,391 a month. Early EMIs are mostly interest, later ones mostly principal, which is why prepaying early saves the most."),
    ("How do I close my home loan in half the time?",
     "Three routes land at the same place. Raise the EMI to the amount shown for the shorter tenure, keep the EMI and prepay one lump sum every year from a bonus or increment, or step the EMI up by a fixed percentage every year. The calculator shows all three for your numbers plus the bonus rule, one extra EMI a year, which alone cuts a 20 year loan to about 16."),
    ("Is there a penalty for prepaying a loan in India?",
     "For floating rate loans taken by individuals for non business purposes, RBI rules do not allow banks and NBFCs to charge foreclosure or part prepayment penalties. Fixed rate loans can carry a charge, usually 2 to 4% of the prepaid amount. Your sanction letter states which applies. Personal loans are often fixed rate, so check before you prepay."),
    ("Should I prepay my home loan or invest the money?",
     "Compare the after tax cost of the loan with the return you realistically expect from investing. A home loan at 8.5% costs about 6% after Section 24(b) benefit in the 30% slab while the interest is within the ₹2 lakh limit. If you expect 12% from equity and can hold through drawdowns, investing wins on paper. If you want a guaranteed outcome or sleep better debt free, prepay. The planner on this page runs both paths with the same monthly cash and shows the difference in rupees."),
    ("What is the difference between tenure reduction and EMI reduction when I prepay?",
     "When you part prepay, the bank asks whether to lower your EMI or shorten your tenure. Tenure reduction keeps the EMI the same and closes the loan earlier, which is where almost all the interest saving comes from. EMI reduction eases monthly cash flow but saves far less. Ask for tenure reduction unless you need the cash flow relief."),
    ("What tax benefits apply to a home loan in India?",
     "Under the old tax regime, Section 24(b) allows up to ₹2 lakh of home loan interest a year as a deduction for a self occupied house, and Section 80C allows up to ₹1.5 lakh of principal repayment within the overall 80C limit. Each co borrower who is also a co owner can claim these separately. The new regime does not offer these deductions for a self occupied property, so the effective loan cost is the full interest rate."),
    ("Does this calculator store my data?",
     "No. Every number is computed in your browser. The share link puts your inputs in the URL so you can reopen the same plan later. The PDF is generated on your device."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-10-31"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/calculator"},
        {"@type": "ListItem", "position": 3, "name": "Loan EMI calculator", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "Loan EMI and Prepayment Calculator", "url": URL, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "isAccessibleForFree": True,
     "description": "EMI for home, car and personal loans, total interest, a plan to close the loan in half the time with three strategies, and a prepay versus invest comparison with Indian tax benefits.",
     "featureList": ["EMI and total interest", "Close the loan in half the time, three strategies", "Year by year amortisation", "Prepay versus invest with Section 24(b) and 80C", "High fidelity PDF report"],
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
.ln-hero{{background:linear-gradient(160deg,#eef2ff 0%,#fff7ed 55%,#ecfeff 100%)}}
[data-theme=dark] .ln-hero{{background:linear-gradient(160deg,#15173a 0%,#2a1a10 55%,#0e2630 100%)}}
.ln-hero .wrap{{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;align-items:center}}
.ln-art{{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}}
.ln-art img{{width:100%;height:100%;object-fit:cover;display:block}}
.ln-tabs{{display:inline-flex;gap:6px;padding:6px;border-radius:999px;background:var(--card);border:1px solid var(--line);margin:4px 0 14px;max-width:100%;overflow-x:auto}}
.ln-tabs button{{border:0;background:transparent;color:var(--ink-2);font:700 14px Inter;padding:9px 18px;border-radius:999px;cursor:pointer;display:flex;gap:8px;align-items:center;white-space:nowrap}}
.ln-tabs button.on{{background:var(--accent);color:#fff;box-shadow:0 8px 20px rgba(91,61,245,.3)}}
.ln-tabs svg{{width:16px;height:16px}}
.ln-split{{height:14px;border-radius:999px;overflow:hidden;display:flex;background:var(--line);margin:18px 0 8px}}
.ln-split i{{display:block;height:100%;transition:width .5s var(--ease)}}
.ln-split .p{{background:var(--accent)}} .ln-split .i{{background:#f43f5e}}
.ln-split-l{{display:flex;gap:18px;flex-wrap:wrap;font-size:13.5px;color:var(--ink-2);margin-bottom:6px}}
.ln-split-l i{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:middle}}
.ln-split-l .p{{background:var(--accent)}} .ln-split-l .i{{background:#f43f5e}}
.fr-chart .hb{{fill:rgba(16,185,129,.28)}} .fr-chart .hl{{fill:none;stroke:#10b981;stroke-width:2.4}}
.fr-chart .ab{{fill:rgba(91,61,245,.14)}} .fr-chart .al{{fill:none;stroke:var(--accent);stroke-width:2.4}}
.fr-legend i.h{{background:#10b981}}
.ln-strat{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:18px}}
.ln-st{{border:1px solid var(--line);border-radius:16px;padding:16px 18px;background:var(--card)}}
.ln-st i{{font:800 12px "JetBrains Mono",monospace;color:var(--accent)}}
.ln-st b{{display:block;font-size:16px;margin:6px 0 4px}} .ln-st p{{font-size:14px;color:var(--ink-2);margin:0 0 10px;line-height:1.5}}
.ln-st-k{{display:flex;gap:18px}} .ln-st-k span{{font-weight:800;font-size:15px}} .ln-st-k small{{display:block;font-weight:500;font-size:11.5px;color:var(--ink-3);letter-spacing:.04em;text-transform:uppercase}}
.ln-tgt-row{{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:6px 0 4px}}
.ln-tgt-row label{{font-size:14px;font-weight:600;color:var(--ink-2);display:block}}
.ln-tgt-row label b{{color:var(--accent)}}
.ln-tgt-row input[type=range]{{flex:1;min-width:160px;accent-color:var(--accent)}}
.ln-tgt-row b{{min-width:70px}}
.iv-sec{{background:var(--bg-soft)}}
.iv-grid{{display:grid;grid-template-columns:.9fr 1.1fr;gap:28px;align-items:start}}
.iv-form{{border:1px solid var(--line);border-radius:20px;padding:22px;background:var(--card)}}
.iv-form label{{display:block;font-size:13.5px;font-weight:600;color:var(--ink-2);margin-bottom:12px}}
.iv-form input[type=text],.iv-form input[type=number],.iv-form select{{display:block;width:100%;margin-top:6px;padding:12px 14px;border-radius:12px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);font:600 16px Inter}}
.iv-form .chk{{display:flex;gap:10px;align-items:flex-start;font-weight:500;color:var(--ink-2);font-size:14px}}
.iv-form .chk input{{margin-top:3px;accent-color:var(--accent)}}
.iv-kpis{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:14px 0}}
.iv-kpis > div{{border:1px solid var(--line);border-radius:16px;padding:16px;background:var(--card)}}
.iv-kpis small{{display:block;font:600 11px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}}
.iv-kpis b{{display:block;font-family:"Bricolage Grotesque";font-size:28px;letter-spacing:-.02em;margin:6px 0 2px;color:var(--accent)}}
.iv-kpis span{{font-size:12.5px;color:var(--ink-2)}}
.iv-kpis .g b{{color:#059669}}
.fr-verdict.iv-invest{{background:var(--accent-soft);border-color:var(--accent)}}
.ln-dim .iv-form::after{{content:""}}
.iv-note{{font-size:12.5px;color:var(--ink-3);margin-top:10px}}
.ln-rules{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.ln-rules div{{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)}}
.ln-rules b{{display:block;font-size:16px;margin-bottom:6px}} .ln-rules p{{font-size:14px;color:var(--ink-2);margin:0;line-height:1.55}}
@media (max-width:980px){{.ln-hero .wrap{{grid-template-columns:1fr}}.ln-art{{max-width:520px}}.iv-grid{{grid-template-columns:1fr}}}}
@media (max-width:720px){{.ln-strat{{grid-template-columns:1fr}}.ln-rules{{grid-template-columns:1fr}}.iv-kpis{{grid-template-columns:1fr 1fr}}}}
@media (max-width:460px){{.iv-kpis{{grid-template-columns:1fr}}.ln-tabs button{{padding:8px 12px;font-size:13px}}}}
</style>
</head>
<body data-page="loancalc">
{nav}
<header class="page-hero ln-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/calculator">Calculators</a> / Loan EMI calculator</div>
<h1 class="display" style="font-size:clamp(34px,4.6vw,60px)">Know your EMI. Then close the loan in <span>half the time</span>.</h1>
<p>Home, car or personal loan. See the EMI, how much of it is interest, four ways to finish the loan in half the tenure, and whether prepaying beats investing once Indian tax breaks are counted. Free, private, with a PDF you can keep.</p>
<div class="ln-tabs" role="tablist" aria-label="Loan type">
<button type="button" role="tab" data-k="home" class="on" aria-selected="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg>Home loan</button>
<button type="button" role="tab" data-k="car" aria-selected="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 16l1.5-5h11L19 16M3 16h18v3H3zM7 19v2M17 19v2"/></svg>Car loan</button>
<button type="button" role="tab" data-k="personal" aria-selected="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>Personal loan</button>
</div>
</div>
<div class="ln-art"><img src="{uns('1560518883-ce09059eeffa', 880, 605)}" alt="Keys being handed over in front of a new home" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">

<section class="bx-sec" style="padding-top:24px" id="calculator">
  <div class="wrap fr-wrap">
    <form class="fr-in" id="lnForm" onsubmit="return false">
      <div class="fr-step"><span>1</span><b>Your <em class="ln-kind">home</em> loan</b></div>
      <label class="fr-money">Loan amount (&#8377;)<input type="text" id="amt" value="50,00,000" inputmode="numeric"></label>
      <div class="fr-grid">
        <label>Interest rate per year (%)<input type="number" id="rate" min="0.1" max="40" step="0.05" value="8.5" inputmode="decimal"></label>
        <label>Tenure (years)<input type="number" id="tenure" min="1" max="30" step="1" value="20" inputmode="numeric"></label>
      </div>
      <div class="fr-step"><span>2</span><b>Close it faster</b></div>
      <div class="ln-tgt-row"><label for="target" style="margin:0">Close the loan in <b id="tgtLbl">10 years</b> instead</label><input type="range" id="target" min="1" max="29" step="1" value="10" aria-label="Target years to close the loan"></div>
      <p class="fr-hint">Default is half your tenure. Drag to see what closing in any number of years takes.</p>
    </form>

    <a class="fr-mbar" href="#lnOut" id="mbar"><span>Your EMI <b id="mN">-</b></span><em>See the plan</em></a>
    <div class="fr-out" id="lnOut" aria-live="polite">
      <div class="fr-verdict" id="vd"></div>
      <div class="fr-big"><small>Your monthly EMI</small><b id="oEmi">-</b><span id="oEmiS"></span></div>
      <div class="fr-kpis">
        <div><small>Total interest</small><b id="oInt">-</b><span id="oIntS"></span></div>
        <div><small>Total you repay</small><b id="oPaid">-</b><span>principal plus interest</span></div>
        <div style="grid-column:span 2"><small>EMI to close in <span class="ln-tgt">10</span> years</small><b id="oHalf">-</b><span id="oHalfS"></span></div>
      </div>
      <div class="ln-split" aria-hidden="true"><i class="p" id="splitP"></i><i class="i" id="splitI"></i></div>
      <div class="ln-split-l" id="splitL"></div>
      <div class="fr-chart"><svg id="chart" viewBox="0 0 640 240" role="img" aria-label="Outstanding balance by year, normal schedule versus the faster plan"></svg>
        <div class="fr-legend"><i class="a"></i>Normal schedule <i class="h"></i>Close in <span class="ln-tgt">10</span> years</div></div>
      <h3 style="margin:22px 0 0;font-family:'Bricolage Grotesque';font-size:22px;letter-spacing:-.02em">Four ways to close it in <span class="ln-tgt">10</span> years</h3>
      <div class="ln-strat" id="strat"></div>
      <div class="fr-acts"><button type="button" class="btn btn-primary sc-pdfbtn" id="pdfBtn">Download my loan plan (PDF)</button><button type="button" class="btn btn-ghost" id="share">Copy link to my plan</button><button type="button" class="btn btn-ghost" id="tblBtn">Show year by year table</button></div>
      <div class="fr-tbl" id="tbl" hidden></div>
    </div>
  </div>
</section>

<section class="bx-sec iv-sec" id="prepay-or-invest">
  <div class="wrap" id="ivSec">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Prepay or invest?</span><h2 class="display">The Extra &#8377;10,000 a Month Question</h2>
    <p>You have some spare cash every month. Throw it at the loan, or invest it and let the loan run? This planner spends the same money on both paths for the full tenure, counts Section 24(b) and 80C where they apply, taxes the investment gains, and tells you the difference in rupees. <span id="ivKindNote"></span></p></div>
    <div class="iv-grid">
      <form class="iv-form reveal" id="ivForm" onsubmit="return false">
        <label>Extra money you can put in every month (&#8377;)<input type="text" id="extra" value="10,000" inputmode="numeric"></label>
        <div class="fr-grid">
          <label>Your income tax slab<select id="slab"><option value="0">0% or new regime</option><option value="5">5%</option><option value="20">20%</option><option value="30" selected>30%</option></select></label>
          <label>Return you expect from investing (%)<input type="number" id="expRet" min="0" max="25" step="0.5" value="12" inputmode="decimal"></label>
        </div>
        <label class="chk"><input type="checkbox" id="c80"> Count Section 80C on principal (tick only if your 80C limit is not already used by PF, ELSS or insurance)</label>
        <label class="chk"><input type="checkbox" id="cobor"> Co borrower who is also a co owner (doubles the 24(b) and 80C limits)</label>
        <p class="fr-hint">Investment gains are taxed at 12.5% LTCG at the end. Both paths invest any freed up cash once the loan closes.</p>
      </form>
      <div class="reveal" id="ivOut">
        <div class="fr-verdict ok" id="ivVd"></div>
        <div class="iv-kpis">
          <div><small>Loan cost after tax</small><b id="ivEff">-</b><span id="ivEffS"></span></div>
          <div><small>Return you expect</small><b id="ivRet">-</b><span>from investing the same money</span></div>
          <div class="g"><small>Prepay: interest saved</small><b id="ivSave">-</b><span id="ivSaveS"></span></div>
          <div><small>Invest: corpus at the end</small><b id="ivCorp">-</b><span id="ivCorpS"></span></div>
        </div>
        <div class="fr-chart"><svg id="ivChart" viewBox="0 0 640 220" role="img" aria-label="Net position by year, invest path versus prepay path"></svg>
          <div class="fr-legend"><i class="a"></i>Invest the extra <i class="h"></i>Prepay the extra</div></div>
        <p class="iv-note" id="ivNote"></p>
      </div>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap cs-two">
    <div class="reveal"><span class="eyebrow">How it works</span><h2 class="display">The Math in Plain English</h2></div>
    <div class="cs-prose reveal">
      <p><b>1. The EMI formula.</b> EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1). P is the loan, r the monthly rate, n the months. The bank fixes the EMI so the last payment clears the last rupee.</p>
      <p><b>2. Interest first, principal later.</b> Each month the interest is charged on what you still owe. In year one of a 20 year home loan about 80% of every EMI is interest. By year 15 it flips.</p>
      <p><b>3. Why prepaying early is worth more.</b> A rupee prepaid in year two kills interest for 18 years. The same rupee in year 15 kills it for five. That is why the strategies above front load the extra money.</p>
      <p><b>4. The half time plan.</b> We solve for the EMI, the yearly lump sum, or the yearly step up that brings the closing month to your target, then compare interest paid under each.</p>
      <p><b>5. Prepay versus invest.</b> Both paths spend the same cash every month. One sends the extra to the loan and, after it closes, invests the freed EMI. The other invests the extra from day one while the loan runs full term. We add tax benefits as they arrive and tax the gains at the end.</p>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Before you prepay</span><h2 class="display">Six Rules That Save Real Money</h2></div>
    <div class="ln-rules">
      <div class="reveal"><b>Floating rate, no penalty</b><p>RBI rules bar foreclosure and part prepayment charges on floating rate loans taken by individuals for non business purposes. Fixed rate loans can carry 2 to 4%. Your sanction letter says which.</p></div>
      <div class="reveal"><b>Ask for tenure reduction</b><p>When you part prepay, banks default to cutting the EMI. Keep the EMI and cut the tenure. That is where the interest saving lives.</p></div>
      <div class="reveal"><b>Emergency fund first</b><p>Six months of EMIs and expenses in a liquid fund before any prepayment. Prepaying and then swiping a card at 36% defeats the purpose.</p></div>
      <div class="reveal"><b>Kill the expensive loan first</b><p>Personal loans at 14% and card debt at 36% beat any investment return. A home loan at 8.5% with tax breaks is the last one to prepay.</p></div>
      <div class="reveal"><b>Prepay in the first third</b><p>On a 20 year loan, prepayments in the first seven years save several times more interest than the same amount later. After year 12 the benefit is small.</p></div>
      <div class="reveal"><b>Negotiate the rate once a year</b><p>Existing borrowers often pay more than new ones. A rate reset request or a balance transfer at 0.5% lower saves more than most prepayments on a large loan.</p></div>
    </div>
  </div>
</section>

<section class="bx-sec">
  <div class="wrap bx-faqwrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">FAQ</span><h2 class="display">Common Questions</h2></div>
    <div class="sp-faq-list reveal">{faq_html}</div>
    <p class="fr-disc">This calculator is for education only and does not account for every personal situation. It is not investment, tax or legal advice. Syed Hadi is not a SEBI registered investment adviser. Tax rules differ by regime and change every budget, so confirm with a chartered accountant before acting. Check prepayment terms in your loan agreement.</p>
  </div>
</section>
<script src="/assets/loan-calculator.js?v={VER}"></script>
<script src="/assets/calc-reports.js?v={VER}" defer></script>
</main>
{tail}{foot}
</body>
</html>
'''
open(os.path.join(ROOT, "loan-calculator.html"), "w", encoding="utf-8").write(page)
print("loan-calculator.html written", len(page))
