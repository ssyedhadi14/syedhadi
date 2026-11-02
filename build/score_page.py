#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Generate /seo-aeo-score, the SEO and AEO score tool page for syedcreates.com
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
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/ai-visibility-checker"><small>PREVIOUS</small><b>&larr; AI Visibility Checker</b></a><a class="right" href="/aeo-seo-in-a-box"><small>NEXT</small><b>AEO/SEO Ranking in a box &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/seo-aeo-score"
TITLE = "SEO and AEO Score Checker: Free Website Audit With DR"
DESC = "Paste a URL and get an SEO score, an AEO score for AI answer engines, your Domain Rating from OpenSEO and a prioritised list of fixes. Free, no sign up."

FAQ = [
    ("What is an AEO score?",
     "AEO stands for answer engine optimisation, getting cited by ChatGPT, Gemini, Perplexity and Google AI Overviews. The AEO score measures the signals those engines rely on: valid structured data, a declared organisation or person entity, FAQ or article schema, an llms.txt file, AI crawlers allowed in robots.txt, question led headings, a direct answer under the H1, and visible author and dates."),
    ("How is the SEO score calculated?",
     "The tool fetches your page like a crawler and checks 16 on page and technical signals: HTTPS, response time, title and meta description length, a single H1, heading order, canonical, viewport, language, alt text, robots.txt, XML sitemap, Open Graph tags, internal links, page weight and word count. Each check carries a weight and the SEO score is out of 60, the AEO score out of 40, 100 in total."),
    ("Where does the Domain Rating come from?",
     "From OpenSEO, an open source SEO platform that reads backlink data from DataForSEO. The tool asks OpenSEO for the domain's rank, backlinks and referring domains and converts the rank to a 0 to 100 rating so it reads like the DR you know from Ahrefs. It is an estimate from a different index, so expect it to differ a little."),
    ("Does the checker look at the whole site?",
     "It scores the one URL you enter plus three site level files: robots.txt, sitemap.xml and llms.txt. Run it on your home page first, then on the two or three pages that matter most for pipeline, such as a product page and a comparison page."),
    ("Is my URL stored?",
     "The URL is fetched once to produce the score and the result is cached in memory for a short time so repeated checks do not cost extra. Nothing is written to a database and no account is needed."),
    ("What should I fix first?",
     "The action list is sorted by priority and impact. Anything marked high blocks indexing or citation outright, such as a noindex tag, a blocked AI crawler or missing structured data. Clear those, then work down the mediums. If your Domain Rating is under 30, authority is the real ceiling and link earning belongs on the plan."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-10-31"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/tools#calculators"},
        {"@type": "ListItem", "position": 3, "name": "SEO and AEO score", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "SEO and AEO Score Checker", "url": URL, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "isAccessibleForFree": True,
     "description": "Scores any public URL on 16 SEO signals and 8 answer engine signals, shows Domain Rating from OpenSEO and returns a prioritised action list.",
     "featureList": ["SEO score out of 60", "AEO score out of 40", "Domain Rating, backlinks and referring domains from OpenSEO", "Prioritised action items", "robots.txt, sitemap.xml and llms.txt checks"],
     "author": {"@id": SITE + "/#person"}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
faq_html = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

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
.sa-hero{{background:linear-gradient(160deg,#eef2ff 0%,#fdf2f8 50%,#ecfeff 100%)}}
[data-theme=dark] .sa-hero{{background:linear-gradient(160deg,#15173a 0%,#2a1030 50%,#0e2630 100%)}}
.sa-hero .wrap{{display:grid;grid-template-columns:1.15fr .85fr;gap:32px;align-items:center}}
.sa-art{{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}}
.sa-art img{{width:100%;height:100%;object-fit:cover;display:block}}
.sa-form{{display:flex;gap:10px;margin-top:22px;max-width:640px}}
.sa-form input{{flex:1;min-width:0;padding:16px 18px;border-radius:14px;border:2px solid var(--line);background:var(--card);color:var(--ink);font:600 17px Inter}}
.sa-form input:focus{{outline:0;border-color:var(--accent)}}
.sa-form .btn{{padding:16px 22px;font-size:16px;white-space:nowrap}}
.sa-note{{font-size:13px;color:var(--ink-3);margin-top:10px}}
.sa-out{{display:none;margin-top:8px}}
.sa-out.on{{display:block}}
.sa-status{{padding:16px 18px;border-radius:14px;background:var(--accent-soft);font-weight:600;display:flex;gap:12px;align-items:center}}
.sa-status .spin{{width:18px;height:18px;border:3px solid var(--accent);border-right-color:transparent;border-radius:50%;animation:saSpin .8s linear infinite;flex:none}}
@keyframes saSpin{{to{{transform:rotate(360deg)}}}}
.sa-status.err{{background:rgba(220,38,38,.1);color:#b91c1c}}
.sa-top{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:14px;margin-top:18px}}
.sa-score{{border:1px solid var(--line);border-radius:20px;padding:22px;background:var(--card);position:relative;overflow:hidden}}
.sa-score small{{display:block;font:600 11px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}}
.sa-score b{{display:block;font-family:"Bricolage Grotesque";font-size:clamp(40px,5vw,58px);line-height:1;margin:10px 0 4px;color:var(--accent)}}
.sa-score b em{{font-style:normal;font-size:.42em;color:var(--ink-3);font-weight:600}}
.sa-score span{{font-size:13px;color:var(--ink-2)}}
.sa-score .bar{{height:8px;border-radius:999px;background:var(--line);margin-top:12px;overflow:hidden}}
.sa-score .bar i{{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--accent),#8b5cf6);transition:width .9s var(--ease)}}
.sa-score.total{{background:linear-gradient(140deg,#1a1050,#4b2fe0 65%,#8b6dff);color:#fff;border:0}}
.sa-score.total small,.sa-score.total span{{color:rgba(255,255,255,.8)}}
.sa-score.total b{{color:#fff}}
.sa-score.total .bar{{background:rgba(255,255,255,.25)}}
.sa-score.total .bar i{{background:#ffd43b}}
.sa-grade{{position:absolute;top:16px;right:16px;font:800 13px Inter;padding:4px 10px;border-radius:8px;background:rgba(255,255,255,.18)}}
.sa-dr dl{{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;margin:10px 0 0;font-size:13px}}
.sa-dr dt{{color:var(--ink-3)}} .sa-dr dd{{margin:0;font-weight:700;text-align:right}}
.sa-dr .src{{font-size:11.5px;color:var(--ink-3);margin-top:10px}}
.sa-acts{{margin-top:26px}}
.sa-acts h2{{font-family:"Bricolage Grotesque";font-size:clamp(24px,3vw,32px);letter-spacing:-.02em;margin-bottom:6px}}
.sa-acts > p{{color:var(--ink-2);margin-bottom:16px}}
.sa-act{{display:grid;grid-template-columns:auto 1fr;gap:14px;border:1px solid var(--line);border-radius:16px;padding:16px 18px;background:var(--card);margin-bottom:10px}}
.sa-act .pr{{font:800 11px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;padding:5px 9px;border-radius:7px;height:max-content}}
.sa-act .pr.high{{background:rgba(220,38,38,.12);color:#b91c1c}} .sa-act .pr.medium{{background:rgba(245,158,11,.14);color:#b45309}} .sa-act .pr.low{{background:rgba(16,185,129,.14);color:#047857}}
.sa-act b{{display:block;font-size:16px}} .sa-act p{{margin:4px 0 0;font-size:14.5px;color:var(--ink-2);line-height:1.5}} .sa-act small{{display:block;margin-top:6px;font-size:12.5px;color:var(--ink-3);font-family:"JetBrains Mono",monospace}}
.sa-checks{{margin-top:24px;border:1px solid var(--line);border-radius:16px;overflow:hidden}}
.sa-checks table{{width:100%;border-collapse:collapse;font-size:14px}}
.sa-checks th,.sa-checks td{{padding:10px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
.sa-checks th{{background:var(--bg-soft);font-weight:600;color:var(--ink-3);font-size:12.5px}}
.sa-checks td:last-child{{text-align:right;white-space:nowrap;font-family:"JetBrains Mono",monospace;font-size:12.5px}}
.sa-checks .ok{{color:#047857;font-weight:700}} .sa-checks .no{{color:#b91c1c;font-weight:700}}
.sa-checks .grp{{font:800 11px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft)}}
.sa-cta{{margin-top:26px;border-radius:20px;padding:26px;background:linear-gradient(120deg,var(--accent-soft),var(--card));border:1px solid var(--accent);display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center}}
.sa-cta h3{{font-family:"Bricolage Grotesque";font-size:22px;margin:0 0 6px}} .sa-cta p{{margin:0;color:var(--ink-2)}}
.sa-how{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}}
.sa-how div{{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)}}
.sa-how i{{font:800 13px "JetBrains Mono",monospace;color:var(--accent)}} .sa-how b{{display:block;font-size:17px;margin:8px 0 6px}} .sa-how p{{font-size:14px;color:var(--ink-2);margin:0}}
.faq{{border:1px solid var(--line);border-radius:14px;padding:14px 18px;background:var(--card);margin-bottom:10px}}
.faq summary{{cursor:pointer;font-weight:700;font-size:16px}} .faq p{{color:var(--ink-2);margin:10px 0 0;line-height:1.6}}
@media (max-width:980px){{.sa-hero .wrap{{grid-template-columns:1fr}}.sa-art{{max-width:520px}}.sa-top{{grid-template-columns:1fr 1fr}}}}
@media (max-width:760px){{.sa-how{{grid-template-columns:1fr}}.sa-cta{{grid-template-columns:1fr}}.sa-form{{flex-direction:column}}}}
@media (max-width:520px){{.sa-top{{grid-template-columns:1fr}}.sa-checks td:nth-child(3){{display:none}}.sa-checks th:nth-child(3){{display:none}}}}
</style>
</head>
<body data-page="tool_seo">
{nav}
<header class="page-hero sa-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/tools#calculators">Calculators</a> / SEO and AEO score</div>
<h1 class="display">How well does your site rank, and does <span>AI</span> cite it?</h1>
<p>Paste a URL. In about ten seconds you get an SEO score, an AEO score for ChatGPT, Gemini and Perplexity, your Domain Rating from OpenSEO, and the fixes in priority order.</p>
<form class="sa-form" id="saForm" novalidate>
<label class="sr" for="saUrl">Website URL</label>
<input type="url" id="saUrl" name="url" placeholder="yourcompany.com" autocomplete="url" inputmode="url" required>
<button class="btn btn-primary" type="submit" id="saBtn">Score my site</button>
</form>
<p class="sa-note">Free, no sign up, nothing stored. Checks the page you enter plus robots.txt, sitemap.xml and llms.txt.</p>
</div>
<div class="sa-art"><img src="{uns('1460925895917-afdab827c52f', 880, 605)}" alt="Laptop showing website analytics charts" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">
<section class="bx-sec" style="padding-top:20px">
<div class="wrap">
<div class="sa-out" id="saOut" aria-live="polite">
<div class="sa-status" id="saStatus" hidden><span class="spin" aria-hidden="true"></span><span id="saStatusT">Fetching the page, robots.txt, sitemap and llms.txt...</span></div>
<div id="saRes" hidden>
<div class="sa-top">
<div class="sa-score total"><span class="sa-grade" id="saGrade">B</span><small>Overall score</small><b><span id="sTotal">0</span><em>/100</em></b><span id="sUrl"></span><div class="bar"><i id="bTotal"></i></div></div>
<div class="sa-score"><small>SEO score</small><b><span id="sSeo">0</span><em>/60</em></b><span>On page and technical</span><div class="bar"><i id="bSeo"></i></div></div>
<div class="sa-score"><small>AEO score</small><b><span id="sAeo">0</span><em>/40</em></b><span>Answer engine readiness</span><div class="bar"><i id="bAeo"></i></div></div>
<div class="sa-score sa-dr"><small>Domain Rating</small><b id="sDr">&mdash;</b><span id="sDrNote"></span><dl id="sDrL"></dl><div class="src" id="sDrSrc"></div></div>
</div>
<div class="sa-acts"><h2 id="saActsT">Your action items</h2><p id="saActsP"></p><div id="saActs"></div></div>
<details class="sa-checks-wrap" style="margin-top:18px"><summary style="cursor:pointer;font-weight:700;color:var(--accent)">See every check and the points behind the score</summary><div class="sa-checks"><table id="saTable"><thead><tr><th>Check</th><th>Result</th><th>Detail</th><th>Points</th></tr></thead><tbody></tbody></table></div></details>
<div class="sa-cta"><div><h3>Want these fixed in 90 days?</h3><p>AEO/SEO Ranking in a box covers the technical fixes, buyer pages, structured data and AI visibility tracking. Or book 30 minutes and I will walk through this report with you.</p></div><div class="btns"><a class="btn btn-primary" href="/schedule-meeting">Schedule meeting</a><a class="btn btn-ghost" href="/aeo-seo-in-a-box">See the box</a></div></div>
</div>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">What gets checked</span><h2 class="display">24 Signals, Two Scores, One List</h2>
<p>Search engines and answer engines want overlapping but different things. The checker splits them so you can see which side needs the work.</p></div>
<div class="sa-how">
<div class="reveal"><i>SEO / 60</i><b>Can Google crawl, understand and trust the page?</b><p>HTTPS, response time, title and description length, one H1, heading order, canonical, viewport, language, alt text, robots.txt, sitemap, Open Graph, internal links, page weight and word count.</p></div>
<div class="reveal"><i>AEO / 40</i><b>Can an AI assistant quote you with confidence?</b><p>Valid JSON-LD, a declared Organization or Person, FAQ or Article schema, llms.txt, AI crawlers allowed, question led headings, a direct answer under the H1, and visible author plus dates.</p></div>
<div class="reveal"><i>DR</i><b>Does the domain carry authority?</b><p>Domain rank, backlinks and referring domains from OpenSEO's DataForSEO index, converted to a 0 to 100 rating. Under 30 and links are the ceiling, over 50 and content is.</p></div>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap cs-two">
<div class="reveal"><span class="eyebrow">Why AEO now</span><h2 class="display">Buyers Ask the Assistant Before They Search</h2></div>
<div class="cs-prose reveal">
<p><b>The shortlist is written before the click.</b> When a buyer asks ChatGPT or Perplexity which vendors to consider, the answer names three to five companies. If yours is not in that answer, your landing page never gets the visit. That is why the AEO score sits next to the SEO score instead of inside it.</p>
<p><b>Entities beat keywords.</b> Answer engines resolve organisations, people and products, then look for consistent facts about them across your site, LinkedIn, directories and press. Organization and Person schema with sameAs links is the cheapest fix with the largest effect, which is why it carries 12 of the 40 AEO points together with FAQ schema.</p>
<p><b>Say it in the first sentence.</b> Models lift the paragraph that answers the question most directly. A 40 to 80 word answer right under the H1, a few H2s phrased as real questions and an llms.txt that points to your best pages are the pattern I used to take AccuKnox to 27.72% AI visibility. The full story is in the <a href="/aeo-seo-case-study">AEO and SEO case study</a>.</p>
<p><b>Authority still gates it.</b> A DR under 30 means fewer citations whatever the markup says, because engines weight sources they already trust. Check how likely you are to be cited today with the <a href="/ai-visibility-checker">AI visibility checker</a>, then fix the technical layer here.</p>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Common questions</span><h2 class="display">SEO and AEO Score FAQ</h2></div>
<div class="reveal">{faq_html}</div>
<p class="fr-disc">Scores are a snapshot of one URL at one moment and a guide for prioritising work, not a ranking guarantee. Domain Rating is an estimate from OpenSEO's index and will differ from Ahrefs, Moz or Semrush. Built by <a href="/about">Syed Hadi</a>.</p>
</div>
</section>
</main>
{tail}
{foot}
<script src="/assets/common.js?v={VER}"></script>
<script>
(function(){{
  var $=function(i){{return document.getElementById(i)}};
  var form=$('saForm'),out=$('saOut'),st=$('saStatus'),stT=$('saStatusT'),res=$('saRes');
  function esc(s){{return String(s==null?'':s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
  function grade(p){{return p>=90?'A+':p>=80?'A':p>=70?'B':p>=55?'C':p>=40?'D':'E'}}
  function show(d){{
    res.hidden=false;
    var s=d.scores,pct=Math.round(s.total/s.totalMax*100);
    $('sTotal').textContent=s.total;$('sSeo').textContent=s.seo;$('sAeo').textContent=s.aeo;$('saGrade').textContent=grade(pct);
    $('sUrl').textContent=d.finalUrl||d.url;
    requestAnimationFrame(function(){{$('bTotal').style.width=pct+'%';$('bSeo').style.width=Math.round(s.seo/s.seoMax*100)+'%';$('bAeo').style.width=Math.round(s.aeo/s.aeoMax*100)+'%';}});
    var dr=d.dr||{{}},L=$('sDrL');L.innerHTML='';
    if(dr.rating!=null){{$('sDr').textContent=dr.rating;$('sDrNote').textContent=dr.rating<10?'Very low authority':dr.rating<30?'Low authority':dr.rating<50?'Moderate authority':'Strong authority';
      [['Backlinks',dr.backlinks],['Referring domains',dr.referringDomains],['New ref. domains',dr.newReferringDomains],['Lost ref. domains',dr.lostReferringDomains],['Spam score',dr.spamScore]].forEach(function(p){{if(p[1]!=null)L.innerHTML+='<dt>'+p[0]+'</dt><dd>'+esc(Number(p[1]).toLocaleString('en-IN'))+'</dd>';}});
      $('sDrSrc').textContent=dr.source||'';}}
    else{{$('sDr').textContent='\\u2014';$('sDrNote').textContent=dr.error?('OpenSEO: '+dr.error):(dr.note||'Not available');$('sDrSrc').textContent='';}}
    var acts=d.actions||[];$('saActsT').textContent=acts.length?'Your '+acts.length+' action items':'Nothing to fix. Nice work.';
    var hi=acts.filter(function(a){{return a.priority==='high'}}).length;
    $('saActsP').textContent=acts.length?(hi?hi+' high priority item'+(hi>1?'s':'')+' first, then work down the list.':'No blockers. These are refinements, sorted by impact.'):'Every check passed. Run the AI visibility checker next.';
    $('saActs').innerHTML=acts.map(function(a){{return '<div class="sa-act"><span class="pr '+a.priority+'">'+a.priority+'</span><div><b>'+esc(a.label)+'</b><p>'+esc(a.action)+'</p>'+(a.detail?'<small>'+esc(a.detail)+'</small>':'')+'</div></div>'}}).join('');
    var tb=$('saTable').tBodies[0];tb.innerHTML='';var last='';
    (d.checks||[]).forEach(function(c){{if(c.group!==last){{last=c.group;tb.innerHTML+='<tr><td class="grp" colspan="4">'+(c.group==='seo'?'SEO signals':'AEO signals')+'</td></tr>';}}
      tb.innerHTML+='<tr><td>'+esc(c.label)+'</td><td class="'+(c.pass?'ok':'no')+'">'+(c.pass?'Pass':'Fix')+'</td><td>'+esc(c.detail)+'</td><td>'+c.points+'/'+c.max+'</td></tr>';}});
    if(window.shTrack)shTrack('seo_aeo_score',{{label:(d.finalUrl||d.url).slice(0,60),score:s.total}});
  }}
  form.addEventListener('submit',function(e){{
    e.preventDefault();var url=$('saUrl').value.trim();if(!url){{$('saUrl').focus();return;}}
    out.classList.add('on');res.hidden=true;st.hidden=false;st.className='sa-status';stT.textContent='Fetching the page, robots.txt, sitemap and llms.txt...';
    var b=$('saBtn');b.disabled=true;b.textContent='Scoring...';
    var tm=setTimeout(function(){{stT.textContent='Still working. Slow sites take up to 20 seconds...'}},6000);
    fetch('/.netlify/functions/seo-aeo-score',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{url:url}})}})
      .then(function(r){{return r.json().catch(function(){{return{{ok:false,error:'The scoring service is not available right now (status '+r.status+').'}}}})}})
      .then(function(d){{clearTimeout(tm);if(!d.ok)throw new Error(d.error||'Could not score that URL.');st.hidden=true;show(d);try{{history.replaceState(null,'','?url='+encodeURIComponent(url));}}catch(e){{}}out.scrollIntoView({{behavior:'smooth',block:'start'}});}})
      .catch(function(err){{clearTimeout(tm);st.className='sa-status err';st.querySelector('.spin').style.display='none';stT.textContent=err.message;}})
      .then(function(){{b.disabled=false;b.textContent='Score my site';st.querySelector('.spin').style.display='';}});
  }});
  var q=new URLSearchParams(location.search).get('url');if(q){{$('saUrl').value=q;form.dispatchEvent(new Event('submit'));}}
}})();
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "seo-aeo-score.html"), "w", encoding="utf-8").write(page)
print("seo-aeo-score.html written", len(page))
