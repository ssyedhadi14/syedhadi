#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate /company-research, the Firecrawl powered company research tool for syedcreates.com.
#          Input is a company homepage URL. Output is a byte sized market snapshot and a one page PDF.
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
tail = re.sub(r'<div class="wrap next-page">.*?</div>', '<div class="wrap next-page"><a href="/seo-aeo-score"><small>PREVIOUS</small><b>&larr; SEO and AEO Score</b></a><a class="right" href="/partner-readiness-score"><small>NEXT</small><b>Partner Readiness Score &rarr;</b></a></div>', tail, flags=re.S)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)

URL = SITE + "/company-research"
TITLE = "Company Research Tool: ARR, Competitors and Gaps"
DESC = "Paste a company homepage and get market cap, HQ, headcount, customers, ARR, competitors, pain points and missed revenue on one page, with a PDF."

FAQ = [
    ("What does the company research tool find?",
     "Ten things a go to market team asks before a first call: market cap or latest valuation, headquarters, employee count, total customers, ARR or revenue, the top five competitors, unique differentiators, why customers choose the company over competitors, growth pain points, and the revenue opportunities the company is missing, each with a fix."),
    ("Where does the data come from?",
     "A Firecrawl research agent starts on the homepage you enter, reads the about, customers, pricing and press pages, then searches the web: filings and investor relations, Crunchbase style profiles, LinkedIn, reputable press, review sites and job posts. Every figure carries a source link and a confidence label."),
    ("How accurate are the numbers?",
     "Each figure is labelled HIGH when it comes from a filing or the company's own page, MEDIUM for reputable press or analyst estimates, and UNVERIFIED for a single weak source. Private companies rarely publish ARR or customer counts, so expect Not disclosed there. Never quote an unverified figure to a customer without a second source."),
    ("Are the pain points and missed revenue facts?",
     "No. They are analysis. The agent ties each one to a visible signal such as a pricing page that forces every buyer to sales, no cloud marketplace listing, review complaints or a hiring pattern, and tells you the signal so you can judge it yourself."),
    ("How long does it take?",
     "Usually one to four minutes, because the agent reads a dozen or more pages. Keep the tab open. Companies researched in the last seven days load instantly from cache, and the share link reopens the same report."),
    ("Is there a limit?",
     "Yes. Each visitor can run three new companies an hour and the site has a daily cap, because every run costs research credits. Cached companies do not count. If you need a batch of accounts researched, book a call."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-11-02"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/tools#calculators"},
        {"@type": "ListItem", "position": 3, "name": "Company research", "item": URL}]},
    {"@type": ["WebApplication", "SoftwareApplication"], "name": "Company Research Tool", "url": URL, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "isAccessibleForFree": True,
     "description": "Researches any company from its homepage URL and returns market cap, HQ, employees, customers, ARR, competitors, differentiators, buyer reasons, growth pain points and missed revenue opportunities, with a one page PDF.",
     "featureList": ["Market cap or valuation", "Headquarters and headcount", "Total customers and ARR with confidence labels", "Top 5 competitors", "Unique differentiators", "Why customers choose them", "Growth pain points, must fix and nice to fix", "Missed revenue opportunities with fixes", "One page PDF"],
     "author": {"@id": SITE + "/#person"}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]}
faq_html = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

CSS = r'''
.cr-hero{background:linear-gradient(160deg,#eef2ff 0%,#fdf2f8 50%,#ecfeff 100%)}
[data-theme=dark] .cr-hero{background:linear-gradient(160deg,#15173a 0%,#2a1030 50%,#0e2630 100%)}
.cr-hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:32px;align-items:center}
.cr-art{border-radius:22px;overflow:hidden;aspect-ratio:16/11;box-shadow:0 24px 60px rgba(28,16,80,.18)}
.cr-art img{width:100%;height:100%;object-fit:cover;display:block}
.cr-form{display:flex;gap:10px;margin-top:22px;max-width:640px}
.cr-form input{flex:1;min-width:0;padding:16px 18px;border-radius:14px;border:2px solid var(--line);background:var(--card);color:var(--ink);font:600 17px Inter}
.cr-form input:focus{outline:0;border-color:var(--accent)}
.cr-form .btn{padding:16px 22px;font-size:16px;white-space:nowrap}
.cr-note{font-size:13px;color:var(--ink-3);margin-top:10px}
.cr-ten{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px;max-width:640px}
.cr-ten span{font-size:12.5px;font-weight:600;padding:5px 10px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--ink-2)}
.cr-out{display:none;scroll-margin-top:96px}.cr-out.on{display:block}
.cr-prog{border:1px solid var(--line);border-radius:20px;background:var(--card);padding:22px 24px}
.cr-prog h2{font-size:20px;margin:0 0 4px}.cr-prog>p{margin:0 0 14px;color:var(--ink-2);font-size:14.5px}
.cr-steps{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.cr-steps li{display:flex;gap:12px;align-items:center;font-size:15px;color:var(--ink-3)}
.cr-steps li i{width:22px;height:22px;border-radius:50%;border:2px solid var(--line);flex:none;display:grid;place-items:center;font-style:normal;font-size:12px}
.cr-steps li.on{color:var(--ink);font-weight:600}.cr-steps li.on i{border-color:var(--accent);border-right-color:transparent;animation:crSpin .8s linear infinite}
.cr-steps li.done{color:var(--ink-2)}.cr-steps li.done i{background:var(--accent);border-color:var(--accent);color:#fff}
.cr-steps li.done i::after{content:"\2713"}
@keyframes crSpin{to{transform:rotate(360deg)}}
.cr-time{margin-top:12px;font:600 12.5px "JetBrains Mono",monospace;color:var(--ink-3)}
.cr-err{padding:16px 18px;border-radius:14px;background:rgba(220,38,38,.1);color:#b91c1c;font-weight:600}
[data-theme=dark] .cr-err{color:#fca5a5}
.cr-head{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:start;border-radius:22px;padding:26px 28px;background:linear-gradient(140deg,#140d3a,#2c1c8a 70%,#4b2fe0);color:#fff}
.cr-head small{font:600 11px "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:#cfc6ff}
.cr-head h2{color:#fff;font-size:clamp(28px,4vw,40px);margin:6px 0 6px;letter-spacing:-.02em}
.cr-head p{margin:0;color:#e6e1ff;max-width:640px;line-height:1.5}
.cr-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.cr-chips span{font-size:12.5px;padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.12);color:#fff}
.cr-chips b{font:600 10px "JetBrains Mono",monospace;letter-spacing:.08em;color:#cfc6ff;margin-right:6px}
.cr-acts{display:flex;flex-direction:column;gap:8px;align-items:stretch}
.cr-acts .btn{justify-content:center}
.cr-head .btn-primary{background:#ffd43b;color:#1b1145;box-shadow:none}
.cr-head .btn-ghost{color:#fff;border-color:rgba(255,255,255,.35);background:rgba(255,255,255,.06)}
.cr-kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:14px}
.cr-kpi{border:1px solid var(--line);border-radius:18px;padding:16px;background:var(--card);display:flex;flex-direction:column;gap:6px;min-width:0}
.cr-kpi small{font:600 10.5px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.cr-kpi b{font-family:"Plus Jakarta Sans",Inter,sans-serif;font-weight:800;font-size:clamp(19px,2vw,24px);line-height:1.15;color:var(--ink);overflow-wrap:anywhere}
.cr-kpi .cf{display:flex;gap:6px;align-items:center;flex-wrap:wrap;font-size:12px;color:var(--ink-3)}
.cr-kpi a{color:var(--accent);font-size:12px}
.cf-tag{font:700 10px "JetBrains Mono",monospace;letter-spacing:.06em;padding:3px 7px;border-radius:6px}
.cf-HIGH{background:#dcf7ec;color:#065f46}.cf-MEDIUM{background:#fff1d6;color:#92400e}.cf-UNVERIFIED{background:#eceaf3;color:#4a4760}
[data-theme=dark] .cf-HIGH{background:#0f3a2b;color:#6ee7b7}[data-theme=dark] .cf-MEDIUM{background:#3b2a0c;color:#fcd34d}[data-theme=dark] .cf-UNVERIFIED{background:#26243a;color:#c9c5dc}
.cr-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.cr-card{border:1px solid var(--line);border-radius:18px;padding:18px 20px;background:var(--card);min-width:0}
.cr-card.full{grid-column:1/-1}
.cr-card h3{font:700 11.5px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;margin:0 0 12px;display:flex;gap:8px;align-items:center}
.cr-card h3 i{width:8px;height:8px;border-radius:50%;display:inline-block}
.k-rose h3{color:#be123c}.k-rose h3 i{background:#f43f5e}.k-acc h3{color:var(--accent)}.k-acc h3 i{background:var(--accent)}
.k-grn h3{color:#047857}.k-grn h3 i{background:#10b981}.k-amb h3{color:#b45309}.k-amb h3 i{background:#f59e0b}.k-sky h3{color:#0369a1}.k-sky h3 i{background:#0ea5e9}
[data-theme=dark] .k-rose h3{color:#fda4af}[data-theme=dark] .k-grn h3{color:#6ee7b7}[data-theme=dark] .k-amb h3{color:#fcd34d}[data-theme=dark] .k-sky h3{color:#7dd3fc}
.cr-card table{width:100%;border-collapse:collapse;font-size:14.5px}
.cr-card th{text-align:left;font-size:12px;color:var(--ink-3);font-weight:600;padding:0 10px 8px 0;border-bottom:1px solid var(--line)}
.cr-card td{padding:9px 10px 9px 0;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink-2);line-height:1.45}
.cr-card tr:last-child td{border-bottom:0}
.cr-card td:first-child{color:var(--ink);font-weight:700}
.cr-card ul{margin:0;padding:0;list-style:none;display:grid;gap:9px}
.cr-card li{position:relative;padding-left:18px;color:var(--ink-2);line-height:1.45;font-size:14.5px}
.cr-card li::before{content:"";position:absolute;left:2px;top:.55em;width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.5}
.cr-pain{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.cr-pain>div{padding:14px 16px}.cr-pain>div+div{border-left:1px solid var(--line)}
.cr-pain h4{margin:0 0 10px;font-size:14px}.cr-pain h4 .sub{display:block;font-weight:500;color:var(--ink-3);font-size:12px;margin-top:2px}
.cr-pain li small{display:block;color:var(--ink-3);font-size:12.5px;margin-top:2px}
.cr-imp{font:700 11px "JetBrains Mono",monospace;padding:3px 8px;border-radius:6px;white-space:nowrap}
.imp-High{background:#fde2e7;color:#9f1239}.imp-Medium{background:#fff1d6;color:#92400e}.imp-Low{background:#e0f2fe;color:#075985}
[data-theme=dark] .imp-High{background:#3d1220;color:#fda4af}[data-theme=dark] .imp-Medium{background:#3b2a0c;color:#fcd34d}[data-theme=dark] .imp-Low{background:#0c2a3d;color:#7dd3fc}
.cr-src{margin-top:14px;font-size:13px;color:var(--ink-3)}
.cr-src a{color:var(--ink-2)}
.cr-src ol{margin:6px 0 0;padding-left:20px;columns:2;column-gap:24px}
.cr-cta{margin-top:18px;border-radius:20px;padding:24px;background:linear-gradient(120deg,var(--accent-soft),var(--card));border:1px solid var(--accent);display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center}
.cr-cta h3{font-size:21px;margin:0 0 6px}.cr-cta p{margin:0;color:var(--ink-2)}
.cr-how{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
.cr-how div{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)}
.cr-how i{font:800 13px "JetBrains Mono",monospace;color:var(--accent);font-style:normal}.cr-how b{display:block;font-size:17px;margin:8px 0 6px}.cr-how p{font-size:14px;color:var(--ink-2);margin:0}
.faq{border:1px solid var(--line);border-radius:14px;padding:14px 18px;background:var(--card);margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;font-size:16px}.faq p{color:var(--ink-2);margin:10px 0 0;line-height:1.6}
@media (max-width:1100px){.cr-kpis{grid-template-columns:repeat(3,1fr)}}
@media (max-width:980px){.cr-hero .wrap{grid-template-columns:1fr}.cr-art{max-width:520px}}
@media (max-width:760px){.cr-grid,.cr-how,.cr-cta,.cr-head{grid-template-columns:1fr}.cr-form{flex-direction:column}.cr-kpis{grid-template-columns:1fr 1fr}.cr-kpi:last-child{grid-column:1/-1}.cr-pain{grid-template-columns:1fr}.cr-pain>div+div{border-left:0;border-top:1px solid var(--line)}.cr-src ol{columns:1}}
'''

JS = r'''
(function(){
  var $=function(i){return document.getElementById(i)};
  var form=$('crForm'),out=$('crOut'),prog=$('crProg'),err=$('crErr'),res=$('crRes'),btn=$('crBtn');
  var FN='/.netlify/functions/company-research';
  var STEPS=['Reading the homepage and about pages','Checking filings, funding and headcount','Mapping competitors and reviews','Finding growth pain points','Sizing the missed revenue','Writing the one pager'];
  var timer=null,t0=0,pollT=null;
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function link(u,t){return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener nofollow">'+esc(t||'source')+'</a>':''}
  function host(u){try{return new URL(u).hostname.replace(/^www\./,'')}catch(e){return u}}
  function stepUI(){var s=Math.floor((Date.now()-t0)/1000),i=Math.min(STEPS.length-1,Math.floor(s/28));
    $('crSteps').innerHTML=STEPS.map(function(x,j){return '<li class="'+(j<i?'done':j===i?'on':'')+'"><i></i>'+x+'</li>'}).join('');
    $('crTime').textContent=Math.floor(s/60)+':'+('0'+s%60).slice(-2)+' elapsed. Most companies finish in 1 to 4 minutes.';}
  function busy(on){btn.disabled=on;btn.textContent=on?'Researching...':'Research company';
    if(on){t0=Date.now();prog.hidden=false;err.hidden=true;res.hidden=true;stepUI();timer=setInterval(stepUI,1000)}else{clearInterval(timer);prog.hidden=true}}
  function fail(m){busy(false);err.hidden=false;err.textContent=m}
  function kpi(label,f){
    return '<div class="cr-kpi"><small>'+esc(label)+'</small><b>'+esc(f.value)+'</b><span class="cf"><span class="cf-tag cf-'+esc(f.confidence)+'">'+esc(f.confidence)+'</span>'+(f.as_of?esc(f.as_of):'')+'</span>'+(f.source_url?link(f.source_url,host(f.source_url)):'')+'</div>'}
  function show(d,cached){
    busy(false);res.hidden=false;
    window.__calc={kind:'company',d:d,onePage:true};
    $('crName').textContent=d.company_name;$('crLine').textContent=d.one_liner||'';
    $('crKick').textContent=(cached?'From cache, researched ':'Researched ')+new Date(d.researched_at).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})+' · '+d.domain;
    var chips=[['HQ',d.headquarters.value],['Category',d.category],['Founded',d.founded],[d.ticker?'Ticker':'Ownership',d.ticker||d.ownership]].filter(function(c){return c[1]&&c[1]!=='Unknown'});
    $('crChips').innerHTML=chips.map(function(c){return '<span><b>'+esc(c[0])+'</b>'+esc(c[1])+'</span>'}).join('');
    $('crKpis').innerHTML=kpi(d.ownership==='Public'?'Market cap':'Market cap / valuation',d.market_cap)+kpi('Headquarters',d.headquarters)+kpi('Employees',d.employee_count)+kpi('Total customers',d.total_customers)+kpi('ARR',d.arr);
    $('crComp').innerHTML=d.competitors.length?'<table><thead><tr><th>Competitor</th><th>Where they compete</th></tr></thead><tbody>'+d.competitors.map(function(c){return '<tr><td>'+esc(c.name)+'</td><td>'+esc(c.overlap)+'</td></tr>'}).join('')+'</tbody></table>':'<p>No clear competitors found.</p>';
    $('crDiff').innerHTML='<ul>'+d.differentiators.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>';
    $('crWhy').innerHTML=d.why_customers_choose.length?'<table><thead><tr><th>Reason</th><th>Evidence</th></tr></thead><tbody>'+d.why_customers_choose.map(function(w){return '<tr><td>'+esc(w.reason)+'</td><td>'+esc(w.evidence)+'</td></tr>'}).join('')+'</tbody></table>':'<p>Not enough public evidence.</p>';
    var must=d.growth_painpoints.filter(function(p){return p.severity==='must_fix'}),nice=d.growth_painpoints.filter(function(p){return p.severity!=='must_fix'});
    var pl=function(a){return a.length?'<ul>'+a.map(function(p){return '<li>'+esc(p.pain)+(p.signal?'<small>Signal: '+esc(p.signal)+'</small>':'')+'</li>'}).join('')+'</ul>':'<p style="color:var(--ink-3);margin:0">None found.</p>'};
    $('crPain').innerHTML='<div class="cr-pain"><div><h4>Must fix now<span class="sub">Limiting growth today</span></h4>'+pl(must)+'</div><div><h4>Nice to fix<span class="sub">Drag on efficiency</span></h4>'+pl(nice)+'</div></div>';
    var mr=d.missed_revenue.slice().sort(function(a,b){return 'HML'.indexOf(a.impact[0])-'HML'.indexOf(b.impact[0])});
    $('crMiss').innerHTML='<table><thead><tr><th>Missed opportunity</th><th>The fix</th><th>Impact</th></tr></thead><tbody>'+mr.map(function(m){return '<tr><td>'+esc(m.opportunity)+'</td><td>'+esc(m.fix)+'</td><td><span class="cr-imp imp-'+esc(m.impact)+'">'+esc(m.impact)+'</span></td></tr>'}).join('')+'</tbody></table>';
    $('crSrc').innerHTML=d.sources.length?'<b>Sources the agent relied on</b><ol>'+d.sources.map(function(s){return '<li>'+link(s.url,s.title||host(s.url))+'</li>'}).join('')+'</ol>':'';
    try{history.replaceState(null,'','?url='+encodeURIComponent(d.domain))}catch(e){}
    if(window.shTrack)shTrack('company_research',{label:d.domain});
    out.scrollIntoView({behavior:'smooth',block:'start'});
  }
  function poll(id){var hostHint=window.__crHost;
    fetch(FN+'?id='+encodeURIComponent(id)+'&host='+encodeURIComponent(hostHint||'')).then(function(r){return r.json().catch(function(){return{ok:false,error:'The research service did not answer (status '+r.status+').'}})})
      .then(function(d){
        if(d.ok&&d.status==='processing'){if(Date.now()-t0>9*60*1000)return fail('This one is taking unusually long. Try again in a few minutes, the result may already be cached.');pollT=setTimeout(function(){poll(id)},5000);return;}
        if(!d.ok)return fail(d.error||'Research failed. Try again.');
        show(d.data,false);
      }).catch(function(){pollT=setTimeout(function(){poll(id)},8000)});
  }
  function run(url,refresh){
    clearTimeout(pollT);out.classList.add('on');busy(true);
    fetch(FN,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:url,refresh:!!refresh})})
      .then(function(r){return r.json().catch(function(){return{ok:false,error:'The research service is not available right now (status '+r.status+').'}})})
      .then(function(d){if(!d.ok)return fail(d.error||'Could not start the research.');if(d.status==='completed')return show(d.data,!!d.cached);window.__crHost=d.host;poll(d.id);})
      .catch(function(){fail('Network error. Check your connection and try again.')});
    out.scrollIntoView({behavior:'smooth',block:'start'});
  }
  form.addEventListener('submit',function(e){e.preventDefault();var u=$('crUrl').value.trim();if(!u){$('crUrl').focus();return;}run(u,false);});
  $('crShare').addEventListener('click',function(){var u=location.href,b=this;var done=function(){b.textContent='Link copied';setTimeout(function(){b.textContent='Copy share link'},1800)};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(done,function(){prompt('Copy this link',u)});else prompt('Copy this link',u);});
  $('crAgain').addEventListener('click',function(){$('crUrl').value='';$('crUrl').focus();window.scrollTo({top:0,behavior:'smooth'})});
  var q=new URLSearchParams(location.search).get('url');if(q){$('crUrl').value=q;run(q,false);}
})();
'''

head = f'''<!doctype html>
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
<style>{CSS}</style>
</head>
<body data-page="tool_company">
{nav}
<header class="page-hero cr-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / <a href="/tools#calculators">Calculators</a> / Company research</div>
<h1 class="display">Research any company from its <span>homepage</span></h1>
<p>Paste a company URL. A research agent reads the site and the open web, then hands you a one page market snapshot: size, competitors, why buyers pick them, where growth hurts and the revenue they are missing.</p>
<form class="cr-form" id="crForm" novalidate>
<label class="sr" for="crUrl">Company homepage URL</label>
<input type="url" id="crUrl" name="url" placeholder="company.com" autocomplete="url" inputmode="url" required>
<button class="btn btn-primary" type="submit" id="crBtn">Research company</button>
</form>
<p class="cr-note">Free, no sign up. Takes 1 to 4 minutes. Results are cached for 7 days, so the share link reopens instantly.</p>
<div class="cr-ten" aria-label="What you get"><span>Market cap</span><span>HQ</span><span>Employees</span><span>Customers</span><span>ARR</span><span>Competitors</span><span>Differentiators</span><span>Why buyers choose them</span><span>Pain points</span><span>Missed revenue</span></div>
</div>
<div class="cr-art"><img src="{uns('1542744173-8e7e53415bb0', 880, 605)}" alt="Team reviewing a go to market plan in a meeting room" width="880" height="605" fetchpriority="high" decoding="async"></div>
</div>
</header>
'''

body = '''<main id="main">
<section class="bx-sec" style="padding-top:20px">
<div class="wrap">
<div class="cr-out" id="crOut" aria-live="polite">
<div class="cr-prog" id="crProg" hidden><h2>Researching</h2><p>The agent is reading pages and cross checking figures. Keep this tab open.</p><ul class="cr-steps" id="crSteps"></ul><div class="cr-time" id="crTime"></div></div>
<div class="cr-err" id="crErr" hidden></div>
<div id="crRes" hidden>
<div class="cr-head"><div><small id="crKick"></small><h2 id="crName"></h2><p id="crLine"></p><div class="cr-chips" id="crChips"></div></div>
<div class="cr-acts"><button class="btn btn-primary" id="pdfBtn" type="button">Download 1 pager PDF</button><button class="btn btn-ghost" id="crShare" type="button">Copy share link</button><button class="btn btn-ghost" id="crAgain" type="button">Research another</button></div></div>
<div class="cr-kpis" id="crKpis"></div>
<div class="cr-grid">
<div class="cr-card k-rose"><h3><i></i>Top competitors</h3><div id="crComp"></div></div>
<div class="cr-card k-acc"><h3><i></i>Unique differentiators</h3><div id="crDiff"></div></div>
<div class="cr-card k-grn full"><h3><i></i>Why customers choose them over competitors</h3><div id="crWhy"></div></div>
<div class="cr-card k-amb full"><h3><i></i>Growth pain points</h3><div id="crPain"></div></div>
<div class="cr-card k-sky full"><h3><i></i>Revenue opportunities they are missing, and the fix</h3><div id="crMiss"></div></div>
</div>
<div class="cr-src" id="crSrc"></div>
<div class="cr-cta"><div><h3>Want this for your whole target list?</h3><p>I run account research like this for partner mapping and outbound every week. Book 30 minutes and we will scope a batch for your ICP.</p></div><div class="btns"><a class="btn btn-primary" href="/schedule-meeting">Schedule meeting</a></div></div>
</div>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">How it works</span><h2 class="display">One URL In, One Page Out</h2>
<p>The same ten questions I ask before every partner or prospect call, answered from public sources with a confidence label on every number.</p></div>
<div class="cr-how">
<div class="reveal"><i>01</i><b>Read the company's own story</b><p>Homepage, about, customers, pricing and press pages. This sets the category, the claims and the logos they lead with.</p></div>
<div class="reveal"><i>02</i><b>Check it against the open web</b><p>Filings, funding news, headcount profiles, reviews and job posts. Each figure is labelled HIGH, MEDIUM or UNVERIFIED with its source.</p></div>
<div class="reveal"><i>03</i><b>Find the gaps</b><p>Pain points and missed revenue are tied to visible signals, such as no marketplace listing, no partner program or a sales only pricing page, so you can judge them.</p></div>
</div>
</div>
</section>

<section class="bx-sec">
<div class="wrap">
<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Common questions</span><h2 class="display">Company Research FAQ</h2></div>
<div class="reveal">__FAQ__</div>
<p class="fr-disc">AI assisted research from public sources, powered by Firecrawl. Figures can be out of date or wrong, so verify anything marked MEDIUM or UNVERIFIED before you quote it. Pain points and missed revenue are analysis, not facts. Built by <a href="/about">Syed Hadi</a>.</p>
</div>
</section>
</main>
'''.replace("__FAQ__", faq_html)

page = (head + body + tail + foot
        + f'\n<script src="/assets/common.js?v={VER}"></script>\n<script src="/assets/calc-reports.js?v={VER}" defer></script>\n<script>{JS}</script>\n</body>\n</html>\n')
open(os.path.join(ROOT, "company-research.html"), "w", encoding="utf-8").write(page)
print("company-research.html written", len(page))
