#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-17
# Purpose: SEO, GEO and lead generation pass for syedcreates.com. Homepage targeting, Person entity enrichment,
#          Service and FAQ schema on service pages, a Growth in a Box content upgrade, a contextual "work with me"
#          CTA box on pages without one, and an llms.txt intro that leads with the services.
# Owner: Syed Hadi
# Usage: python3 build/seo_leads_2026_11_17.py   (idempotent)
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = "https://syedcreates.com"


def rd(p):
    return open(os.path.join(SITE, p), encoding="utf-8").read()


def wr(p, t):
    open(os.path.join(SITE, p), "w", encoding="utf-8").write(t)


def add_ld(t, obj, marker):
    if marker in t:
        t = re.sub(r'<script type="application/ld\+json" data-k="' + marker + r'">.*?</script>', "", t, flags=re.S)
    tag = f'<script type="application/ld+json" data-k="{marker}">{json.dumps(obj, ensure_ascii=False)}</script>'
    return t.replace("</head>", tag + "\n</head>", 1)


# 1. Homepage targeting -------------------------------------------------------------------------------------------
TITLE = "Syed Hadi | GTM and Growth Consultant for B2B SaaS"
DESC = ("GTM, growth, product marketing and partner programs for B2B SaaS and security startups. "
        "Fixed scope 30, 45 or 90 day builds. Book a free 30 minute call.")


def homepage():
    t = rd("index.html")
    t = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", t, count=1)
    for pat, new in [
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{TITLE}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{DESC}">'),
    ]:
        t = re.sub(pat, lambda m, new=new: new, t, count=1)
    t = t.replace('alt="Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox"',
                  'alt="Syed Hadi, GTM and growth consultant for B2B SaaS and security startups"')
    # WebPage node name and description in JSON-LD
    def fix_ld(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        for n in d.get("@graph", []) if isinstance(d, dict) else []:
            if n.get("@type") == "WebPage" and n.get("url") in (BASE + "/", BASE):
                n["name"], n["description"] = TITLE, DESC
        return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
    t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, t, flags=re.S)
    wr("index.html", t)


# 2. Person entity enrichment on every page ----------------------------------------------------------------------
PERSON_EXTRA = {
    "description": "GTM and growth consultant for B2B SaaS and security startups. Product marketing and channel partnerships lead at AccuKnox, based in Bengaluru, India.",
    "knowsAbout": ["Go to market strategy", "Product marketing", "Channel partnerships", "Partner led growth",
                   "Answer engine optimization", "B2B SaaS growth", "Cloud security marketing", "Sales enablement"],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
}


def person_all():
    n = 0
    for f in glob.glob(os.path.join(SITE, "*.html")):
        t = open(f, encoding="utf-8").read()
        if '"#person"' not in t and "/#person" not in t:
            continue
        def fix(m):
            try:
                d = json.loads(m.group(2))
            except Exception:
                return m.group(0)
            changed = False
            stack = [d]
            while stack:
                x = stack.pop()
                if isinstance(x, dict):
                    if x.get("@type") == "Person" and x.get("@id") == BASE + "/#person" and "name" in x:
                        for k, v in PERSON_EXTRA.items():
                            if x.get(k) != v:
                                x[k] = v
                                changed = True
                    stack += list(x.values())
                elif isinstance(x, list):
                    stack += x
            if not changed:
                return m.group(0)
            return f'{m.group(1)}{json.dumps(d, ensure_ascii=False)}</script>'
        t2 = re.sub(r'(<script type="application/ld\+json"(?: data-k="[^"]*")?>)(.*?)</script>', fix, t, flags=re.S)
        if t2 != t:
            open(f, "w", encoding="utf-8").write(t2)
            n += 1
    return n


# 3. Service and FAQ schema, FAQ sections -------------------------------------------------------------------------
def faq_html(heading_a, heading_b, qas, sid):
    items = "".join(f'<details class="sp-faq-item"><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in qas)
    return (f'<section class="bx-sec" data-k="faq-{sid}"><div class="wrap bx-faqwrap"><div class="sec-head reveal" style="text-align:left;margin-left:0">'
            f'<span class="eyebrow">FAQ</span><h2 class="display" id="s-{sid}-faq">{heading_a} <span class="t2">{heading_b}</span></h2></div>'
            f'<div class="sp-faq-list reveal">{items}</div></div></section>')


def faq_ld(qas, url):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "url": url,
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}


def service_ld(name, stype, slug, desc, area):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype,
            "url": f"{BASE}/{slug}", "description": desc, "provider": {"@id": f"{BASE}/#person"}, "areaServed": area}


def insert_before_section(t, section_class_start, block, key):
    if f'data-k="{key}"' in t:
        t = re.sub(r'<section class="[^"]*" data-k="' + key + r'">.*?</section>', "", t, flags=re.S)
    i = t.find(section_class_start)
    if i < 0:
        i = t.find("</main>")
    return t[:i] + block + t[i:]


INDIA = {"@type": "Country", "name": "India"}
UAE = {"@type": "Country", "name": "United Arab Emirates"}
WORLD = "Worldwide"

GROWTH_QA = [
    ("What is Growth in a Box?", "Six fixed scope growth engagements for B2B SaaS and security startups: GTM, PMM, GTM and PMM together, AEO and SEO, content, and partner revenue. Each one follows the same 90 day roadmap of diagnose and decide, build and launch, then run and scale."),
    ("How long does an engagement take?", "Small projects run 30 days and cover phase one of the roadmap. Medium projects run 45 days. Long term work is scoped together on a call."),
    ("Which box should I start with?", 'If pipeline still depends on the founder, start with <a href="/gtm-in-a-box">GTM in a Box</a>. If buyers and sellers tell different stories, start with <a href="/pmm-in-a-box">PMM in a Box</a>. If you are invisible in Google and AI answers, start with <a href="/aeo-seo-in-a-box">AEO and SEO in a Box</a>. Not sure? Book a free call and leave with a draft 90 day plan.'),
    ("Who is it for?", "B2B SaaS and security startups from seed to Series B that have early customers and want repeatable pipeline beyond founder led sales."),
    ("How is pricing shared?", "Pricing is shared by email on request, in a one pager for the box you pick."),
    ("Do you work with teams outside India?", "Yes. Work runs remotely, and the GTM and partner programs behind each box were built across India, MENA, APAC, Japan, Europe, Africa and the US."),
]
REF_QA = [
    ("What work can I refer?", "GTM, product marketing, AEO and SEO, content and partner program work for B2B SaaS and security companies."),
    ("How is the referral fee set?", "The fee is agreed in writing before the intro, so you know it upfront."),
    ("Who owns the client relationship?", "You do. Your client relationship stays yours."),
    ("Do you refer work back?", "Yes. If a client needs paid media, design or development, I send it to partners I trust."),
    ("How fast will I hear back?", 'I reply with the referral terms within two working days. Want to talk first? <a href="/schedule-meeting">Schedule a meeting</a>.'),
]
MEET_QA = [
    ("How long is the call?", "30 minutes, on video."),
    ("What do I leave with?", "A draft 90 day plan for where growth stalls today, whether we work together or not."),
    ("What should I bring?", "Your current pipeline numbers and the one problem you most want fixed, whether that is pipeline, positioning, AI search or content."),
    ("Is the call free?", "Yes. There is no cost and no obligation."),
    ("What happens after the call?", 'If there is a fit, I send a one pager for the right box, such as <a href="/gtm-in-a-box">GTM in a Box</a> or <a href="/growth-in-a-box">Growth in a Box</a>, with scope and timing.'),
]


def service_pages():
    # Growth in a box: sizes, locations, FAQ, schema
    t = rd("growth-in-a-box.html")
    sizes = ('<section class="bx-sec" data-k="gb-sizes"><div class="wrap"><div class="sec-head reveal" style="text-align:left;margin-left:0">'
             '<span class="eyebrow">How it works</span><h2 class="display" id="s-engagement-sizes">Pick a Size, <span class="t2">Not a Retainer</span></h2>'
             '<p>Every box runs on the same 90 day roadmap. You choose how much of it we build together.</p></div>'
             '<div class="gb-sizes reveal">'
             '<div class="gb-size"><b>Small</b><span>30 days</span><p>Phase one. Find where growth stalls, pick the ICP and the motions, and leave with a signed plan.</p></div>'
             '<div class="gb-size"><b>Medium</b><span>45 days</span><p>Plan plus build. Positioning, the first outbound or partner motion and a pipeline dashboard your team runs.</p></div>'
             '<div class="gb-size"><b>Long term</b><span>Scoped on a call</span><p>The full 90 day build and beyond, with fractional leadership while your team takes over.</p></div>'
             '</div>'
             '<p class="gb-where reveal">Working with teams in <a href="/gtm-consultant-bengaluru">Bengaluru</a>, across <a href="/product-marketing-consultant-india">India</a>, '
             'and in <a href="/fractional-cmo-dubai-saas">Dubai</a> and the <a href="/growth-marketing-consultant-dubai">GCC</a>. '
             'Comparing options? Read <a href="/fractional-pmm-vs-agency-vs-full-time-hire">fractional PMM vs agency vs full time hire</a>.</p>'
             '<div class="bx-ctas reveal" style="justify-content:flex-start"><a class="btn btn-primary" data-track="schedule_click" href="/schedule-meeting">Schedule meeting</a></div>'
             '</div></section>')
    t = insert_before_section(t, '<section class="bx-sec" style="padding-top:0">', sizes, "gb-sizes")
    if "Keep going" not in t:
        pass
    t = insert_before_section(t, '<section class="tr-sec', faq_html("Before You", "Book", GROWTH_QA, "growth"), "faq-growth")
    t = add_ld(t, faq_ld(GROWTH_QA, f"{BASE}/growth-in-a-box"), "faq")
    t = add_ld(t, service_ld("Growth in a Box", "B2B SaaS growth consulting", "growth-in-a-box",
                             "Six fixed scope growth engagements for B2B SaaS and security startups: GTM, PMM, AEO and SEO, content and partner revenue, in 30, 45 or 90 day builds.", WORLD), "svc")
    wr("growth-in-a-box.html", t)

    t = rd("referral-partners.html")
    t = insert_before_section(t, '<section class="tr-sec', faq_html("Referral", "Questions", REF_QA, "ref"), "faq-ref")
    t = add_ld(t, faq_ld(REF_QA, f"{BASE}/referral-partners"), "faq")
    t = add_ld(t, service_ld("Referral partner program", "Referral program for GTM consulting", "referral-partners",
                             "Refer GTM, product marketing, AEO and SEO, content or partner program work to Syed Hadi and earn a referral fee agreed in writing.", WORLD), "svc")
    wr("referral-partners.html", t)

    t = rd("schedule-meeting.html")
    t = insert_before_section(t, '<section class="tr-sec', faq_html("Before the", "Call", MEET_QA, "meet"), "faq-meet")
    t = add_ld(t, faq_ld(MEET_QA, f"{BASE}/schedule-meeting"), "faq")
    wr("schedule-meeting.html", t)

    loc = {
        "fractional-cmo-dubai-saas": ("Fractional CMO for Dubai SaaS", "Fractional CMO", [{"@type": "City", "name": "Dubai"}, UAE]),
        "growth-marketing-consultant-dubai": ("Growth and partner GTM consulting, Dubai and GCC", "Growth marketing consultant", [{"@type": "City", "name": "Dubai"}, UAE]),
        "gtm-consultant-bengaluru": ("GTM consulting in Bengaluru", "Go to market consultant", [{"@type": "City", "name": "Bengaluru"}, INDIA]),
        "product-marketing-consultant-india": ("Product marketing consulting in India", "Product marketing consultant", [INDIA]),
    }
    for slug, (name, stype, area) in loc.items():
        t = rd(f"{slug}.html")
        d = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
        t = add_ld(t, service_ld(name, stype, slug, html.unescape(d), area), "svc")
        wr(f"{slug}.html", t)


# 4. Contextual CTA box ------------------------------------------------------------------------------------------
SVC = {
    "gtm-in-a-box": ("GTM in a Box", "ICP, outbound, partners and a pipeline dashboard, built with your team in 30, 45 or 90 days."),
    "pmm-in-a-box": ("PMM in a Box", "Positioning, messaging, battlecards and a launch your sellers actually repeat."),
    "aeo-seo-in-a-box": ("AEO and SEO in a Box", "Rank on Google and get cited by ChatGPT, Gemini and Perplexity, with tracking you can show your board."),
    "content-in-a-box": ("Content in a Box", "A content engine that ships every week and ties every piece to pipeline."),
    "partner-revenue-in-a-box": ("Partner Revenue in a Box", "Partner mapping, recruitment, enablement and joint pipeline reviews that turn partners into deals."),
    "growth-in-a-box": ("Growth in a Box", "Six fixed scope engagements for B2B SaaS and security teams. Pick the one that fixes your stall."),
}
PICK = [
    (r"partner", "partner-revenue-in-a-box"),
    (r"gtm-health", "gtm-in-a-box"),
    (r"aeo|seo|visibility|ai-search", "aeo-seo-in-a-box"),
    (r"content|writing|posts|insights|blog", "content-in-a-box"),
    (r"pmm|positioning|product-marketing", "pmm-in-a-box"),
    (r"calculator|salary|careers|jobs|bmi|loan|mileage|mutual|fire", "growth-in-a-box"),
]
FORCE = {"ai-visibility-checker", "gtm-health-check", "partner-readiness-score"}
EXCLUDE = {"privacy", "qums", "adventure", "skill-pack", "skill-pack-thanks", "audit-requested", "one-pager-sent", "404",
           "schedule-meeting", "index"}


def pick(slug):
    for pat, svc in PICK:
        if re.search(pat, slug):
            return svc
    return "gtm-in-a-box"


def places(slug):
    locs = [("gtm-consultant-bengaluru", "Bengaluru"), ("product-marketing-consultant-india", "India"), ("fractional-cmo-dubai-saas", "Dubai")]
    parts = [f'<a href="/{s}">{n}</a>' if s != slug else n for s, n in locs]
    return f"Teams in {parts[0]}, {parts[1]} and {parts[2]}."


def cta_html(slug):
    svc = pick(slug)
    name, line = SVC[svc]
    personal = svc == "growth-in-a-box" and re.search(r"calculator|bmi|loan|mileage|mutual|fire|careers|jobs", slug)
    head = ("Growing a B2B SaaS <span class='t2'>company?</span>" if personal else "Want this built for <span class='t2'>your team?</span>")
    others = [k for k in SVC if k != svc][:4]
    links = " &middot; ".join(f'<a href="/{k}">{SVC[k][0]}</a>' for k in others)
    return ('<section class="bx-sec svc-cta-sec" data-k="svc-cta"><div class="wrap"><div class="svc-cta reveal">'
            f'<div class="svc-cta-txt"><span class="eyebrow">Work with me</span><h2 class="display">{head}</h2>'
            f'<p><b>{name}.</b> {line}</p>'
            f'<p class="svc-cta-more">Also: {links}. {places(slug)}</p></div>'
            '<div class="svc-cta-btns"><a class="btn btn-primary" data-track="schedule_click" href="/schedule-meeting">Schedule meeting</a>'
            f'<a class="btn btn-ghost" href="/{svc}">See {name}</a></div></div></div></section>')


def body_has_cta(t):
    m = re.search(r"<main.*?</main>", t, flags=re.S)
    body = m.group(0) if m else t
    body = re.sub(r'<section class="bx-sec svc-cta-sec".*?</section>', "", body, flags=re.S)
    svc_link = re.search(r'href="(?:https://syedcreates\.com)?/(?:' + "|".join(list(SVC) + ["gtm-pmm-in-a-box"]) + r')(?:\.html)?["#]', body)
    meet = "schedule-meeting" in body
    return meet and bool(svc_link)


def cta_all():
    done = []
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        slug = os.path.basename(f)[:-5]
        if slug in EXCLUDE or slug.startswith("x-") or slug in SVC or slug.endswith("-in-a-box"):
            continue
        t = open(f, encoding="utf-8").read()
        if "noindex" in (re.search(r'<meta name="robots" content="([^"]*)"', t) or [None, ""])[1]:
            continue
        had = 'data-k="svc-cta"' in t
        if not had and body_has_cta(t) and slug not in FORCE:
            continue
        t = re.sub(r'<section class="bx-sec svc-cta-sec" data-k="svc-cta">.*?</section>', "", t, flags=re.S)
        i = t.find('<section class="tr-sec')
        if i < 0:
            i = t.find("</main>")
        if i < 0:
            continue
        t = t[:i] + cta_html(slug) + t[i:]
        open(f, "w", encoding="utf-8").write(t)
        done.append(slug)
    return done


# 5. llms.txt ----------------------------------------------------------------------------------------------------
LLMS_INTRO = ("> Syed Hadi is a GTM and growth consultant for B2B SaaS and security startups, based in Bengaluru, India. "
              "He runs fixed scope \"in a box\" engagements for go to market, product marketing, AEO and SEO, content and partner revenue, "
              "built on a 90 day roadmap, and leads product marketing and channel partnerships at AccuKnox, a Zero Trust CNAPP and AI security company. "
              "Book a free 30 minute call at https://syedcreates.com/schedule-meeting.")


def llms():
    t = rd("llms.txt")
    t = re.sub(r"^> .*$", LLMS_INTRO, t, count=1, flags=re.M)
    add = [
        ("## Growth in a box", f"- [Growth in a box](https://syedcreates.com/growth-in-a-box): all six fixed scope engagements, the 30, 45 and 90 day sizes and how to pick one."),
        ("## Consulting by location and comparison", f"- [Fractional CMO, Dubai SaaS](https://syedcreates.com/fractional-cmo-dubai-saas)\n- [Fractional PMM in India](https://syedcreates.com/fractional-pmm-india)\n- [Referral partner program](https://syedcreates.com/referral-partners): refer GTM, PMM, AEO and SEO, content or partner work and earn a referral fee."),
    ]
    for head, line in add:
        first = line.split("](")[1].split(")")[0]
        if first in t:
            continue
        t = t.replace(head + "\n", head + "\n" + line + "\n", 1)
    wr("llms.txt", t)


CSS = """
/* 2026-11-17 Lead CTA box and Growth in a Box sizes */
.svc-cta{display:grid;grid-template-columns:minmax(0,1.6fr) auto;gap:28px;align-items:center;padding:30px 34px;border-radius:22px;
  background:linear-gradient(135deg,rgba(91,61,245,.08),rgba(180,62,160,.08));border:1px solid rgba(91,61,245,.22)}
.svc-cta h2{font-size:clamp(26px,3vw,36px);margin:6px 0 10px}
.svc-cta p{margin:0 0 6px;color:var(--ink-2)}.svc-cta p b{color:var(--ink)}
.svc-cta-more{font-size:14px}.svc-cta-more a{color:var(--accent)}
.svc-cta-btns{display:flex;flex-direction:column;gap:10px;min-width:210px}.svc-cta-btns .btn{justify-content:center}
@media (max-width:760px){.svc-cta{grid-template-columns:minmax(0,1fr);padding:24px 20px}.svc-cta-btns{min-width:0}}
.gb-sizes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:8px 0 18px}
.gb-size{padding:22px;border-radius:18px;border:1px solid var(--line,#e7e3f5);background:var(--card,#fff)}
.gb-size b{display:block;font-family:"Plus Jakarta Sans",Inter,sans-serif;font-size:20px}.gb-size span{color:var(--accent);font-weight:700;font-size:14px}
.gb-size p{margin:10px 0 0;color:var(--ink-2);font-size:15px}
.gb-where{color:var(--ink-2)}.gb-where a{color:var(--accent)}
@media (max-width:760px){.gb-sizes{grid-template-columns:minmax(0,1fr)}}
"""


def css():
    p = os.path.join(SITE, "assets", "site.css")
    t = open(p, encoding="utf-8").read()
    if "2026-11-17 Lead CTA box" not in t:
        open(p, "a", encoding="utf-8").write(CSS)


HUBS = ('<p class="ab-more reveal" data-k="ab-more">More from me: <a href="/work">work</a>, <a href="/portfolio">portfolio</a>, '
        '<a href="/case-studies">case studies</a>, <a href="/insights">insights</a>, <a href="/calculator">free calculators</a>, '
        '<a href="/interview-prep">interview prep</a> and the <a href="/brand">brand kit</a>.</p>')


def about_hubs():
    t = rd("about.html")
    t = re.sub(r'<p class="ab-more reveal" data-k="ab-more">.*?</p>', "", t, flags=re.S)
    i = t.find('<section class="bx-sec svc-cta-sec"')
    t = t[:i] + '<section class="bx-sec" style="padding-top:0"><div class="wrap">' + HUBS + '</div></section>' + t[i:] if 'data-k="ab-more"' not in t else t
    wr("about.html", t)


if __name__ == "__main__":
    homepage()
    print("person schema pages:", person_all())
    service_pages()
    print("cta added:", cta_all())
    llms()
    about_hubs()
    css()
