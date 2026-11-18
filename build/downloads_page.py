# Created by: Claude Cowork
# Date: 2026-11-18
# Purpose: Build site/downloads.html, a library of every free PDF on syedcreates.com.
#          Ungated PDFs download directly. Gated PDFs keep their email gate (Substack
#          subscribe), sharing the unlock key with the source page. Idempotent.
#          To add a PDF: drop it in site/downloads/, render its cover into
#          site/img/downloads/<name>.jpg and .webp, add an entry to ITEMS, rerun.
# Owner: Syed Hadi
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SLUG = "downloads"
URL = f"https://syedcreates.com/{SLUG}"
TITLE = "Free Career and Interview PDFs to Download | Syed Hadi"
DESC = ("Free PDF guides from Syed Hadi: 30 interview questions with answers, the interview and offer "
        "playbook, the India PMM salary guide and the AI job search setup guide.")
ALT = "Free guides and one pagers"

# gate: None for direct download, or a dict with the localStorage key the source page uses
ITEMS = [
    {"file": "india-pmm-salary-guide-2026", "title": "India PMM Salary Guide 2026",
     "desc": "Salary bands by title, city and company stage, negotiation prompts for each level and the full source list.",
     "cat": "career", "label": "Career", "pages": 8, "page": "/pmm-salary-2026", "page_label": "Salary calculator",
     "gate": {"key": "pmmGuide"}},
    {"file": "ai-job-search-setup-guide", "title": "AI Job Search Setup Guide",
     "desc": "Set up the open source AI job search agent on Claude Code: prerequisites, private copy, every slash command.",
     "cat": "career", "label": "Career", "pages": 1, "page": "/ai-job-search", "page_label": "Full guide", "gate": None},
    {"file": "interview-questions-and-answers", "title": "30 Interview Questions, Answered",
     "desc": "Ten questions each for product marketing, partnerships and sales roles, what each one tests and how to answer it.",
     "cat": "interview", "label": "Interview", "pages": 7, "page": "/interview-prep#questions", "page_label": "Practise with the AI coach", "gate": None},
    {"file": "interview-loop-and-offer-playbook", "title": "Interview Loop and Offer Playbook",
     "desc": "The six rounds of a B2B SaaS interview loop and six things to check before you sign an offer in Bengaluru.",
     "cat": "interview", "label": "Interview", "pages": 3, "page": "/interview-prep", "page_label": "Interview prep hub", "gate": None},
]

FAQ = [
    ("Are these downloads free?", "Yes. Every PDF here is free. The salary guide asks for your email and adds you to my Substack newsletter, which you can leave in one click. The rest download straight away."),
    ("Can I share these PDFs?", "Yes, share them with your team, friends or family. Please link back to this page instead of reuploading them elsewhere, so people always get the latest version."),
    ("How often are they updated?", "Each guide carries its date. I update the salary guide every year and the setup guides when the tools change."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def size_kb(name):
    return round((SITE / "downloads" / f"{name}.pdf").stat().st_size / 1024)


def card(it):
    f = it["file"]
    pdf = f"/downloads/{f}.pdf"
    meta = f'PDF &middot; {it["pages"]} page{"s" if it["pages"] > 1 else ""} &middot; {size_kb(f)} KB'
    badge = '<span class="dl-badge gated">Free with email</span>' if it["gate"] else '<span class="dl-badge">Free</span>'
    if it["gate"]:
        action = (f'<form class="dl-gate" data-key="{it["gate"]["key"]}" novalidate>'
                  f'<label class="sr" for="g-{f}">Email</label>'
                  f'<input id="g-{f}" type="email" required placeholder="you@company.com" autocomplete="email">'
                  f'<label class="dl-ok"><input type="checkbox" required> Subscribe me to Syed&rsquo;s newsletter on Substack. Unsubscribe anytime.</label>'
                  f'<button type="submit" class="btn btn-primary">Unlock the PDF</button>'
                  f'<p class="dl-msg" role="status"></p>'
                  f'<a class="btn btn-primary dl-btn" href="{pdf}" download hidden data-track="download_{f}">Download PDF</a></form>')
    else:
        action = f'<a class="btn btn-primary dl-btn" href="{pdf}" download data-track="download_{f}">Download PDF</a>'
    return (f'<article class="dl-card reveal" data-cat="{it["cat"]}">'
            f'<a class="dl-cover" href="{it["page"]}" aria-label="{esc(it["title"])}">'
            f'<img src="/img/downloads/{f}-cover.webp" srcset="/img/downloads/{f}-cover-800.webp 800w, /img/downloads/{f}-cover.webp 1200w" sizes="(max-width: 560px) 100vw, 560px" alt="Cover of {esc(it["title"])}" width="1200" height="750" loading="lazy" decoding="async"></a>'
            f'<div class="dl-body"><small>{it["label"]}</small><h3>{it["title"]}</h3><p>{it["desc"]}</p>'
            f'<span class="dl-meta">{meta}</span>{action}'
            f'<a class="dl-more" href="{it["page"]}">{it["page_label"]} &rarr;</a></div></article>')


def main_html():
    cats = [("all", "All")] + sorted({(i["cat"], i["label"]) for i in ITEMS}, key=lambda x: x[1])
    chips = "".join(f'<button class="dl-chip{" on" if c == "all" else ""}" data-f="{c}" type="button">{l}</button>' for c, l in cats)
    cards = "".join(card(i) for i in ITEMS)
    faq = "".join(f'<details class="sp-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    n = len(ITEMS)
    return f'''<main id="main">
<style>
.dl-chips{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:26px}}
.dl-chip{{font:600 14px Inter,sans-serif;padding:9px 16px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer}}
.dl-chip.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
.dl-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-items:stretch}}
.dl-card{{border:1px solid var(--line);border-radius:20px;background:var(--card);overflow:hidden;display:flex;flex-direction:column}}
.dl-card[hidden]{{display:none}}
.dl-cover{{position:relative;display:block;overflow:hidden;border-bottom:1px solid var(--line)}}
.dl-cover img{{display:block;width:100%;height:auto;aspect-ratio:1200/750;object-fit:cover;transition:transform .35s ease}}
.dl-card:hover .dl-cover img{{transform:scale(1.04)}}
.dl-badge{{position:absolute;top:12px;right:12px;font:700 12px Inter,sans-serif;padding:5px 10px;border-radius:999px;background:#16a34a;color:#fff}}
.dl-badge.gated{{background:#ffd43b;color:#1b1145}}
.dl-body{{padding:18px 18px 20px;display:flex;flex-direction:column;gap:8px;flex:1}}
.dl-body small{{font:500 11.5px "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}}
.dl-body h3{{font-size:18px;font-weight:800;line-height:1.3}}
.dl-body p{{color:var(--ink-2);font-size:14px;line-height:1.55;flex:1}}
.dl-meta{{font-size:12.5px;color:var(--ink-3)}}
.dl-btn{{justify-content:center;width:100%;margin-top:4px}}
.dl-more{{font-size:13.5px;font-weight:600;color:var(--accent);text-align:center}}
.dl-gate{{display:grid;gap:8px;margin-top:4px}}
.dl-gate input[type=email]{{font:inherit;font-size:14px;padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%}}
.dl-gate input[type=email]:focus{{outline:2px solid var(--accent);outline-offset:1px}}
.dl-ok{{display:flex;gap:8px;align-items:flex-start;font-size:12px;line-height:1.4;color:var(--ink-2)}}
.dl-ok input{{margin-top:2px}}
.dl-gate .btn{{justify-content:center;width:100%}}
.dl-gate.done input,.dl-gate.done .dl-ok,.dl-gate.done button{{display:none}}
.dl-btn[hidden]{{display:none!important}}
.dl-msg{{margin:0;font-size:12.5px;min-height:0;color:var(--ink-2)}}
.dl-faq{{max-width:820px;margin:0 auto;display:grid;gap:10px}}
@media(max-width:560px){{.dl-grid{{grid-template-columns:1fr}}}}
</style>

<section class="bx-sec" id="library" style="padding-top:30px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">The library</span><h2 class="display" id="s-library">{n} free PDFs, ready to <span class="t2">download</span></h2>
      <p>Pick one, download it in a click. The salary guide asks for your email first, everything else is instant.</p></div>
    <div class="dl-chips" role="group" aria-label="Filter downloads">{chips}</div>
    <div class="dl-grid" id="dlGrid">{cards}</div>
  </div>
</section>

<section class="bx-sec" id="faq" style="padding-top:10px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">FAQ</span><h2 class="display" id="s-faq">About these <span class="t3">downloads</span></h2></div>
    <div class="dl-faq">{faq}</div>
  </div>
</section>

<script>
(function(){{
  var chips=document.querySelectorAll('.dl-chip'),cards=document.querySelectorAll('.dl-card');
  chips.forEach(function(c){{c.addEventListener('click',function(){{
    chips.forEach(function(x){{x.classList.toggle('on',x===c)}});
    var f=c.getAttribute('data-f');
    cards.forEach(function(k){{k.hidden=!(f==='all'||k.getAttribute('data-cat')===f)}});
  }})}});
  document.querySelectorAll('.dl-gate').forEach(function(g){{
    var key=g.getAttribute('data-key'),em=g.querySelector('input[type=email]'),ok=g.querySelector('input[type=checkbox]'),msg=g.querySelector('.dl-msg'),dl=g.querySelector('.dl-btn');
    function unlock(){{dl.hidden=false;g.classList.add('done');msg.textContent='Unlocked. Your download is ready.'}}
    try{{if(localStorage.getItem(key)==='1')unlock()}}catch(e){{}}
    g.addEventListener('submit',function(ev){{
      ev.preventDefault();
      if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(em.value)){{msg.textContent='Please enter a valid email.';em.focus();return}}
      if(!ok.checked){{msg.textContent='Please tick the box to get the PDF.';return}}
      window.open('https://syedhadi.substack.com/subscribe?email='+encodeURIComponent(em.value),'_blank','noopener');
      try{{localStorage.setItem(key,'1')}}catch(e){{}}
      if(window.shTrack)shTrack('lead_gate',{{label:key}});
      unlock();
    }});
  }});
}})();
</script>
'''


HERO = f'''<header class="page-hero ph-cv">
  <div class="wrap"><div class="ph-copy">
    <div class="crumbs"><a href="/">Home</a> / Downloads</div>
    <h1 class="display">Free guides you can <span class="tg1">keep.</span></h1>
    <p>Salary benchmarks, setup guides and one pagers, as clean PDFs. Download, print or share them with your team.</p>
    <div class="bx-ctas" style="justify-content:flex-start;margin-top:18px"><a class="btn btn-primary lg" href="#library">Browse the downloads</a><a class="btn btn-ghost lg" href="https://syedhadi.substack.com/" target="_blank" rel="noopener">Get new ones by email</a></div>
  </div>
    <figure class="hero-cv"><img src="/img/covers/{SLUG}.jpg" alt="{ALT}" width="1200" height="750" fetchpriority="high" decoding="async"></figure>
  </div>
</header>
'''


def ld(person):
    items = [{"@type": "ListItem", "position": k + 1,
              "item": {"@type": "DigitalDocument", "name": i["title"], "description": i["desc"],
                       "url": f"https://syedcreates.com/downloads/{i['file']}.pdf", "encodingFormat": "application/pdf",
                       "isAccessibleForFree": True, "author": {"@id": "https://syedcreates.com/#person"}}}
             for k, i in enumerate(ITEMS)]
    g = [
        {"@type": "CollectionPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC,
         "isPartOf": {"@id": "https://syedcreates.com/#website"}, "author": {"@id": "https://syedcreates.com/#person"},
         "mainEntity": {"@type": "ItemList", "itemListElement": items},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://syedcreates.com/"},
             {"@type": "ListItem", "position": 2, "name": "Downloads", "item": URL}]}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    if person:
        g.insert(0, person)
    return {"@context": "https://schema.org", "@graph": g}


def build_page():
    src = (SITE / "software-careers-for-students.html").read_text(encoding="utf-8")
    old_slug, old_url = "software-careers-for-students", "https://syedcreates.com/software-careers-for-students"
    he = src.find("</head>")
    head = src[:he]
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(TITLE)}</title>", head, flags=re.S)
    for a in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(a), lambda m: m.group(1) + esc(DESC) + m.group(2), head)
    for a in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(a), lambda m: m.group(1) + esc(TITLE) + m.group(2), head)
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', lambda m: m.group(1) + ALT + m.group(2), head)
    head = head.replace(old_url, URL).replace(f"/img/covers/og/{old_slug}.", f"/img/covers/og/{SLUG}.")
    for b in re.findall(r'<script type="application/ld\+json"[^>]*>.*?</script>', head, flags=re.S):
        head = head.replace(b, "")
    person = None
    for b in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', (SITE / "jobs.html").read_text(encoding="utf-8"), flags=re.S):
        for n in json.loads(b).get("@graph", []):
            if n.get("@type") == "Person":
                person = n
    head += f'<script type="application/ld+json" data-k="dl">{json.dumps(ld(person), ensure_ascii=False)}</script>\n'
    body = src[he:].replace(f'data-page="{old_slug}"', f'data-page="{SLUG}"')
    nav_end = body.find("</nav>") + len("</nav>")
    ms, me = body.find("<main"), body.find("</main>")
    main = body[ms:me]
    cta = main.find('<section class="bx-sec svc-cta-sec"')
    tail = main[cta:] if cta >= 0 else ""
    out = head + body[:nav_end] + "\n\n" + HERO + "\n" + main_html() + tail + body[me:]
    out = re.sub(r'<script>[^<]*sc-quiz[\s\S]*?</script>', "", out)
    out = re.sub(r'<section class="yt-sec" id="learn"[\s\S]*?</section>\s*', "", out)
    (SITE / f"{SLUG}.html").write_text(out, encoding="utf-8")
    print("downloads page written")


def footer_link():
    """Add Downloads to the footer Resources column on every page."""
    n = 0
    for f in SITE.rglob("*.html"):
        if "/x-" in str(f):
            continue
        h = f.read_text(encoding="utf-8")
        if 'href="/downloads">Downloads</a>' in h:
            continue
        nh = re.sub(r'(<p class="h4">Resources</p>\s*)', r'\1<a href="/downloads">Downloads</a>', h, count=1)
        if nh != h:
            f.write_text(nh, encoding="utf-8"); n += 1
    print("footer link on", n, "pages")


XLINK = ('<section class="bx-sec" data-k="dl-xlink" style="padding-top:0"><div class="wrap" style="text-align:center">'
         '<a class="btn btn-ghost" href="/downloads">See all free downloads &rarr;</a></div></section>')


def xlinks():
    for name in ("pmm-salary-2026.html", "interview-prep.html", "ai-job-search.html"):
        f = SITE / name
        h = f.read_text(encoding="utf-8")
        if 'data-k="dl-xlink"' in h:
            continue
        at = h.find('<section class="bx-sec svc-cta-sec"')
        if at < 0:
            at = h.find("</main>")
        f.write_text(h[:at] + XLINK + h[at:], encoding="utf-8")
    print("downloads link added to source pages")


def sitemap_llms():
    sm = SITE / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    if f"<loc>{URL}</loc>" not in s:
        s = s.replace("</urlset>", f"  <url><loc>{URL}</loc><lastmod>2026-11-18</lastmod><priority>0.7</priority></url>\n</urlset>")
        sm.write_text(s, encoding="utf-8")
    lt = SITE / "llms.txt"
    t = lt.read_text(encoding="utf-8")
    line = f"- [Downloads]({URL}): free PDFs, including 30 interview questions with answers, the interview and offer playbook, the India PMM salary guide 2026 and the AI job search setup guide"
    if URL + ")" not in t:
        lt.write_text(t.rstrip("\n") + "\n" + line + "\n", encoding="utf-8")
    print("sitemap and llms.txt updated")


if __name__ == "__main__":
    build_page(); footer_link(); xlinks(); sitemap_llms()
