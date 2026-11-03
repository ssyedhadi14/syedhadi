#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Build syedcreates.com/software-careers-for-students, a guide to every software industry role
#          for college students plus a 10 question quiz that ends with the top 3 matching roles.
#          Uses gtm-health-check.html as the page shell (head, nav, footer). Rerun to rebuild.
# Owner: Syed Hadi
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(HERE, "..", "site"))
sys.path.insert(0, HERE)
from student_careers_data import GROUPS, ROLES, QUESTIONS, FAQ  # noqa: E402

SLUG = "software-careers-for-students"
URL = f"https://syedcreates.com/{SLUG}"
TITLE = "Software Jobs for Students: Find Your Top 3 Roles"
DESC = 'Free career quiz for college students. Explore 28 software roles, from engineering and AI to sales and design, and get your top 3 matches.'
E = html.escape


def role_card(r):
    slug, name, group, line, enjoy, skills, titles, project, _t = r
    gname = dict(GROUPS)[group]
    return (f'<article class="sc-role reveal" id="role-{slug}" data-g="{group}">'
            f'<small>{E(gname)}</small><h3>{E(name)}</h3><p class="sc-line">{E(line)}</p>'
            f'<p class="sc-enjoy"><b>You will enjoy it if</b> {E(enjoy[0].lower() + enjoy[1:])}</p>'
            f'<details><summary>Skills, first job titles and a starter project</summary>'
            f'<ul>{"".join(f"<li>{E(s)}</li>" for s in skills)}</ul>'
            f'<p><b>First job titles:</b> {E(titles)}</p><p><b>30 day starter project:</b> {E(project)}</p></details>'
            f'</article>')


def quiz():
    out = []
    for qi, (q, opts) in enumerate(QUESTIONS):
        o = "".join(f'<label><input type="radio" name="q{qi}" value="{oi}"{" required" if oi == 0 else ""}><span>{E(lbl)}</span></label>'
                    for oi, (lbl, _p) in enumerate(opts))
        out.append(f'<fieldset class="qz-q reveal" data-i="{qi}"><legend><span>{qi + 1:02d}</span>{E(q)}</legend>'
                   f'<div class="qz-opts">{o}</div></fieldset>')
    return "".join(out)


def main_html():
    chips = '<button class="ins-chip on" type="button" data-g="all">All 28 roles</button>' + "".join(
        f'<button class="ins-chip" type="button" data-g="{k}">{E(v)}</button>' for k, v in GROUPS)
    faq = "".join(f'<details class="sc-faq-q"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    data = {
        "roles": [{"slug": r[0], "name": r[1], "group": dict(GROUPS)[r[2]], "line": r[3], "skills": r[5],
                   "titles": r[6], "project": r[7], "t": r[8]} for r in ROLES],
        "q": [[p for _l, p in opts] for _q, opts in QUESTIONS],
    }
    return f"""<main id="main">

<section class="bx-sec" style="padding-top:30px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Start here</span><h2 class="display" id="s-how-software-companies-pay">Every software company needs <span class="t2">three kinds</span> of people</h2>
      <p>Coding is one way in, not the only one. Software companies pay people to build the product, to sell and grow it, and to run the business around it. Find your lane first, then your role.</p></div>
    <div class="sc-lanes">
      <div class="sc-lane reveal"><b>01</b><h3>Build it</h3><p>Engineering, data, AI and security. You write code, train models or protect systems.</p><a href="#roles" data-jump="build">See build roles &rarr;</a></div>
      <div class="sc-lane reveal"><b>02</b><h3>Sell and grow it</h3><p>Marketing, sales, solutions and customer success. You turn a product into revenue.</p><a href="#roles" data-jump="gtm">See growth roles &rarr;</a></div>
      <div class="sc-lane reveal"><b>03</b><h3>Shape and run it</h3><p>Product, design, writing and operations. You decide what gets built and keep teams moving.</p><a href="#roles" data-jump="product">See product roles &rarr;</a></div>
    </div>
  </div>
</section>

<section class="bx-sec" id="roles" style="padding-top:10px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">The role directory</span><h2 class="display" id="s-all-software-roles">All 28 software <span class="t3">roles</span>, in plain words</h2>
      <p>What each role does, who enjoys it, the three skills to learn first, the job titles to search for and one project you can finish in 30 days.</p></div>
    <div class="ins-chips sc-chips" role="group" aria-label="Filter roles by family">{chips}</div>
    <div class="sc-grid">{"".join(role_card(r) for r in ROLES)}</div>
  </div>
</section>

<section class="bx-sec" id="quiz" style="padding-top:10px">
  <div class="wrap qz-wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">The 2 minute quiz</span><h2 class="display" id="s-find-your-top-3">Find your top 3 <span class="t5">roles</span></h2>
      <p>Ten quick questions about what you enjoy. No sign up, nothing leaves your browser.</p></div>
    <form class="qz" id="scQuiz" novalidate>
      {quiz()}
      <p class="sc-err" id="scErr" hidden>Answer all 10 questions to see your matches.</p>
      <button class="btn btn-primary lg qz-go" type="submit">Show my top 3 roles &rarr;</button>
    </form>
    <div class="qz-out sc-out" id="scOut" hidden aria-live="polite"></div>
  </div>
</section>

<section class="bx-sec" style="padding-top:10px">
  <div class="wrap qz-wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Questions students ask</span><h2 class="display" id="s-faq">Before you <span class="t4">pick</span></h2></div>
    <div class="sc-faq">{faq}</div>
  </div>
</section>

<script>
(function(){{
var D={json.dumps(data, ensure_ascii=False, separators=(",", ":"))};
var chips=document.querySelectorAll('.sc-chips .ins-chip');
function filt(g){{chips.forEach(function(c){{c.classList.toggle('on',c.dataset.g===g)}});document.querySelectorAll('.sc-role').forEach(function(r){{r.hidden=!(g==='all'||r.dataset.g===g)}})}}
chips.forEach(function(c){{c.addEventListener('click',function(){{filt(c.dataset.g)}})}});
document.querySelectorAll('[data-jump]').forEach(function(a){{a.addEventListener('click',function(){{var g=a.dataset.jump;filt(g==='build'?'build':g)}})}});
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
var f=document.getElementById('scQuiz'),out=document.getElementById('scOut');
f.addEventListener('submit',function(e){{
  e.preventDefault();var u={{}},missing=false;
  D.q.forEach(function(opts,i){{var c=f.querySelector('input[name=q'+i+']:checked');if(!c){{missing=true;return}}var p=opts[+c.value];for(var k in p)u[k]=(u[k]||0)+p[k]}});
  if(missing){{document.getElementById('scErr').hidden=false;return}}
  document.getElementById('scErr').hidden=true;
  var un=Math.sqrt(Object.keys(u).reduce(function(s,k){{return s+u[k]*u[k]}},0))||1;
  var scored=D.roles.map(function(r){{var dot=0,rn=0;for(var k in r.t){{dot+=(u[k]||0)*r.t[k];rn+=r.t[k]*r.t[k]}}return{{r:r,s:dot/(un*Math.sqrt(rn))}}}}).sort(function(a,b){{return b.s-a.s}});
  var top=scored.slice(0,3),medal=['Best match','Strong match','Good match'];
  out.innerHTML='<span class="eyebrow">Your result</span><h2>Your top 3 software roles</h2><p>Based on what you enjoy, these roles fit your answers best. Try the starter project for your first pick this month.</p>'+
   top.map(function(x,i){{var r=x.r,pct=Math.round(55+45*Math.max(0,Math.min(1,x.s)));return '<div class="sc-pick'+(i===0?' first':'')+'"><div class="sc-pick-h"><span class="sc-rank">'+(i+1)+'</span><div><small>'+medal[i]+' &middot; '+esc(r.group)+'</small><h3>'+esc(r.name)+'</h3></div><b class="sc-pct">'+pct+'%</b></div><p>'+esc(r.line)+'</p><div class="sc-pick-b"><div><b>Learn first</b><ul>'+r.skills.map(function(s){{return '<li>'+esc(s)+'</li>'}}).join('')+'</ul></div><div><b>Search for</b><p>'+esc(r.titles)+'</p><b>Your 30 day project</b><p>'+esc(r.project)+'</p></div></div><a class="sc-more" href="#role-'+r.slug+'">Read the full role &rarr;</a></div>'}}).join('')+
   '<div class="sc-next"><b>Next step</b><p>Pick your first match, finish the 30 day project, and post what you built on LinkedIn. That one post will do more than ten certificates.</p><div class="bx-ctas" style="justify-content:flex-start"><button type="button" class="btn btn-ghost" id="scRetake">Retake the quiz</button><a class="btn btn-ghost" href="/salary-calculator">See where a salary can take you &rarr;</a></div></div>';
  out.hidden=false;out.scrollIntoView({{behavior:'smooth',block:'start'}});
  document.getElementById('scRetake').addEventListener('click',function(){{f.reset();out.hidden=true;f.scrollIntoView({{behavior:'smooth'}})}});
  if(window.gtag)try{{gtag('event','career_quiz_result',{{top1:top[0].r.slug}})}}catch(_e){{}}
}});
}})();
</script>
</main>"""


CSS = """
/* 2026-11-03 software careers for students */
.sc-lanes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.sc-lane{border:1px solid var(--line);border-radius:18px;padding:22px;background:var(--card)}
.sc-lane b{font:600 13px "JetBrains Mono",monospace;color:var(--accent)}
.sc-lane h3{margin:8px 0 6px;font-size:20px}
.sc-lane p{color:var(--ink-2);font-size:14.5px;line-height:1.55;margin:0 0 12px}
.sc-lane a{font-weight:600;font-size:14px;color:var(--accent);text-decoration:none}
.sc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.sc-role{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card);display:flex;flex-direction:column;gap:6px;scroll-margin-top:100px}
.sc-role[hidden]{display:none}
.sc-role small{font:500 11px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.sc-role h3{font-size:17px;margin:0}
.sc-role p{margin:0;font-size:14px;line-height:1.55;color:var(--ink-2)}
.sc-role .sc-enjoy b{color:var(--ink)}
.sc-role details{margin-top:6px;border-top:1px solid var(--line);padding-top:8px}
.sc-role summary{cursor:pointer;font-weight:600;font-size:13.5px;color:var(--accent)}
.sc-role ul{margin:8px 0;padding-left:18px;font-size:14px;color:var(--ink-2);display:grid;gap:4px}
.sc-role details p{margin-top:6px}
.qz-q .qz-opts span{padding:9px 16px}
.sc-err{color:#d4485e;font-weight:600;margin:0}
.sc-out{display:grid;gap:14px;margin-top:6px}
.sc-out h2{margin:4px 0 0}
.sc-pick{border:1px solid var(--line);border-radius:16px;padding:18px 20px;background:var(--bg)}
.sc-pick.first{border-color:var(--accent);box-shadow:0 16px 40px rgba(91,61,245,.16);background:linear-gradient(135deg,var(--accent-soft),var(--card) 65%)}
.sc-pick-h{display:flex;align-items:center;gap:14px}
.sc-rank{flex:none;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:#fff;font:800 18px "Plus Jakarta Sans",sans-serif}
.sc-pick-h small{font:500 11px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.sc-pick-h h3{margin:2px 0 0;font-size:20px}
.sc-pct{margin-left:auto;font:800 26px "Plus Jakarta Sans",sans-serif;color:var(--accent)}
.sc-pick>p{color:var(--ink-2);margin:10px 0}
.sc-pick-b{display:grid;grid-template-columns:1fr 1.3fr;gap:18px;font-size:14px;color:var(--ink-2)}
.sc-pick-b b{color:var(--ink);font-size:13.5px}
.sc-pick-b ul{margin:6px 0 0;padding-left:18px;display:grid;gap:4px}
.sc-pick-b p{margin:4px 0 10px}
.sc-more{font-weight:600;font-size:14px;color:var(--accent);text-decoration:none}
.sc-next{border:1px dashed var(--line);border-radius:16px;padding:18px 20px}
.sc-next p{color:var(--ink-2);margin:6px 0 12px}
.sc-faq{display:grid;gap:10px}
.sc-faq-q{border:1px solid var(--line);border-radius:14px;padding:14px 18px;background:var(--card)}
.sc-faq-q summary{cursor:pointer;font-weight:600}
.sc-faq-q p{color:var(--ink-2);margin:10px 0 0;line-height:1.6}
@media (max-width:960px){.sc-grid{grid-template-columns:repeat(2,1fr)}.sc-lanes{grid-template-columns:1fr}}
@media (max-width:640px){.sc-grid{grid-template-columns:1fr}.sc-pick-b{grid-template-columns:1fr}}
"""


def jsonld():
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "description": DESC, "inLanguage": "en-IN",
         "isPartOf": {"@id": "https://syedcreates.com/#website"}, "author": {"@id": "https://syedcreates.com/#person"},
         "image": f"https://syedcreates.com/img/covers/og/{SLUG}.jpg"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://syedcreates.com/"},
            {"@type": "ListItem", "position": 2, "name": "Free tools", "item": "https://syedcreates.com/calculator"},
            {"@type": "ListItem", "position": 3, "name": "Software careers for students", "item": URL}]},
        {"@type": "ItemList", "name": "Software industry roles for college students", "numberOfItems": len(ROLES),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
             "@type": "Occupation", "name": r[1], "description": r[3], "skills": ", ".join(r[5]),
             "occupationLocation": {"@type": "Country", "name": "India"}, "url": f"{URL}#role-{r[0]}"}}
             for i, r in enumerate(ROLES)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                                             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>"


def main():
    shell = open(os.path.join(SITE_DIR, "gtm-health-check.html"), encoding="utf-8").read()
    head, rest = shell.split("</head>", 1)
    head = re.sub(r"<title>.*?</title>", f"<title>{E(TITLE)}</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + E(DESC), head)
    head = re.sub(r'(<meta (?:property="og|name="twitter):description" content=")[^"]*', r"\g<1>" + E(DESC), head)
    head = re.sub(r'(<meta (?:property="og|name="twitter):title" content=")[^"]*', r"\g<1>" + E(TITLE), head)
    head = head.replace("https://syedcreates.com/gtm-health-check", URL)
    head = head.replace("/img/covers/og/gtm-health-check.jpg", f"/img/covers/og/{SLUG}.jpg")
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r"\g<1>Your degree is the start. Find the software role that fits you", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
    head = head.replace("</title>", "</title>", 1) + jsonld() + "\n"
    hero = (f'<header class="page-hero ph-cv">\n  <div class="wrap"><div class="ph-copy">\n'
            f"    <div class=\"crumbs\"><a href='/'>Home</a> / <a href='/calculator'>Free tools</a> / Software careers for students</div>\n"
            f'    <h1 class="display">Your degree is the start. Find the software role that <span class="tg1">fits you.</span></h1>\n'
            f'    <p>28 real jobs inside software companies, explained in plain words, plus a 2 minute quiz that shows your top 3 matches and what to learn first.</p>\n'
            f'    <div class="bx-ctas" style="justify-content:flex-start;margin-top:18px"><a class="btn btn-primary lg" href="#quiz">Take the 2 minute quiz &rarr;</a><a class="btn btn-ghost lg" href="#roles">Browse all 28 roles</a></div>\n'
            f'  </div>\n    <figure class="hero-cv"><img src="/img/covers/{SLUG}.jpg" alt="Find the software role that fits you" width="1200" height="750" fetchpriority="high" decoding="async"></figure>\n  </div>\n</header>')
    rest = re.sub(r'<header class="page-hero.*?</header>', lambda _m: hero, rest, count=1, flags=re.S)
    rest = re.sub(r"<main id=\"main\">.*?</main>", lambda _m: main_html(), rest, count=1, flags=re.S)
    page = head + "</head>" + rest
    open(os.path.join(SITE_DIR, f"{SLUG}.html"), "w", encoding="utf-8").write(page)
    css_p = os.path.join(SITE_DIR, "assets", "site.css")
    if ".sc-lanes{" not in open(css_p, encoding="utf-8").read():
        open(css_p, "a", encoding="utf-8").write(CSS)
    print("built", SLUG, len(page) // 1024, "KB")


if __name__ == "__main__":
    main()
