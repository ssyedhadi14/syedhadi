# Created by: Claude Cowork
# Date: 2026-11-17
# Purpose: Build site/ai-job-search.html, a landing page for the open source
#          AI Job Search framework (github.com/ai-job-search-dev/ai-job-search),
#          and add it to the Interview Prep menu on every page. Idempotent.
# Owner: Syed Hadi
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SLUG = "ai-job-search"
REPO = "https://github.com/ai-job-search-dev/ai-job-search"
PORTALS = "https://github.com/ai-job-search-dev/community-portals"
URL = f"https://syedcreates.com/{SLUG}"
TITLE = "AI Job Search Agent on Claude Code | Open Source Guide"
DESC = ("Open source AI job search agent on Claude Code. It finds roles, scores fit, tailors "
        "your CV and cover letter, and preps interviews. Setup guide inside.")
ALT = "Your job search, run by an agent"

FAQ = [
    ("Is AI Job Search free?",
     "The framework is free and MIT licensed. It runs inside Claude Code, which needs a paid Claude plan "
     "or Anthropic API credits, so budget for that."),
    ("Does it work for jobs in India?",
     "Yes. The core workflow does not depend on country or language. Without a job board connector, the "
     "search step uses web search. You can also generate a connector for a board you use with the add portal command."),
    ("Will it invent skills or experience on my CV?",
     "No. Every claim in the CV and cover letter is checked against the profile you build during setup. "
     "Skills you lack stay visible as gaps instead of being stuffed in."),
    ("Do I need to know how to code?",
     "You need to be comfortable running a few terminal commands and installing Python, Bun and LaTeX. "
     "After that, you work with it in plain English through slash commands."),
    ("Is my data private?",
     "It runs on your own machine. Keep your copy as a private repository, because a GitHub fork of a public "
     "repo is always public and setup writes your personal details into tracked files."),
    ("Who built it?",
     "It is an independent open source project, not affiliated with or endorsed by Anthropic. I am not the "
     "author either. I am featuring it because it is the most complete agentic job search setup I have tried."),
]

STEPS = [
    ("/setup", "Build your profile", "Reads your CV, LinkedIn export and past applications, or interviews you, and writes a structured profile."),
    ("/scrape", "Find roles", "Searches job boards for postings that match your profile and removes duplicates."),
    ("/rank", "Shortlist the fits", "Scores every new posting against your fit framework and returns a ranked shortlist with honest gaps."),
    ("/apply", "Tailor and send", "Evaluates fit, drafts a CV and cover letter, has a second agent review them, then compiles clean PDFs."),
    ("/interview", "Prep each round", "Builds a stage specific prep pack, maps likely questions to your STAR stories, and runs a mock interview."),
    ("/outcome", "Track results", "Records each result, archives what you sent, and drafts polite follow ups when an application goes quiet."),
]

APPLY = [
    ("Integrity gate first", "Every posting is scanned for hidden text, invisible characters and instruction shaped lines before any agent reads it."),
    ("Drafter and reviewer", "One agent writes. A second agent with a fresh context researches the company and critiques the draft before revision."),
    ("PDF checked, not just the source", "It compiles the CV and cover letter and reads the rendered pages, fixing layout until the CV is exactly two pages and the letter one."),
    ("ATS text layer check", "It extracts the CV's text the way an ATS parser sees it and confirms contact details, reading order and keyword coverage."),
    ("No fabrication", "Claims are verified against your profile. Keyword gaps you cannot back up are left visible, never stuffed."),
]

NEEDS = [
    ("Claude Code", "A Claude Pro, Max or Team plan, or Anthropic API credits."),
    ("Python 3.10+", "Runs the helper tools in the repo."),
    ("Bun", "Runs any job board connectors you add."),
    ("LaTeX", "TeX Live, MacTeX, TinyTeX or MiKTeX, for the CV and cover letter PDFs."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main_html():
    steps = "".join(
        f'<div class="sc-lane ajs-step reveal"><b>{i:02d} &middot; <code>{c}</code></b><h3>{t}</h3><p>{d}</p></div>'
        for i, (c, t, d) in enumerate(STEPS, 1))
    apply = "".join(f'<li><b>{t}.</b> {d}</li>' for t, d in APPLY)
    needs = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in NEEDS)
    faq = "".join(f'<details class="sp-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''<main id="main">
<style>
.ajs-proof{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:8px}}
.ajs-proof div{{border:1px solid var(--line);border-radius:18px;padding:22px;background:var(--card);text-align:center}}
.ajs-proof b{{display:block;font:800 clamp(30px,4vw,44px)/1 "Plus Jakarta Sans";color:var(--accent)}}
.ajs-proof span{{display:block;margin-top:8px;color:var(--ink-2);font-size:14px}}
.ajs-note{{text-align:center;color:var(--ink-3);font-size:13px;margin-top:14px}}
.ajs-steps{{grid-template-columns:repeat(3,1fr)}}
.ajs-step code{{font:inherit}}
.ajs-step h3{{margin-top:8px}}.ajs-step p{{margin-top:6px;color:var(--ink-2)}}
.ajs-two{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:24px;align-items:start}}
.ajs-two>*{{min-width:0}}
.ajs-card{{border:1px solid var(--line);border-radius:20px;padding:26px;background:var(--card)}}
.ajs-card h3{{font-size:22px;font-weight:800;margin-bottom:12px}}
.ajs-list{{list-style:none;display:grid;gap:12px;padding:0}}
.ajs-list li{{padding-left:26px;position:relative;color:var(--ink-2);line-height:1.55}}
.ajs-list li::before{{content:"";position:absolute;left:4px;top:9px;width:9px;height:9px;border-radius:3px;background:var(--accent)}}
.ajs-list b{{color:var(--ink)}}
.ajs-needs{{list-style:none;display:grid;gap:10px;padding:0}}
.ajs-needs li{{display:grid;gap:2px;padding:12px 14px;border:1px solid var(--line);border-radius:12px}}
.ajs-needs span{{color:var(--ink-2);font-size:14px}}
.ajs-code{{background:#0d0b1a;color:#e9e4ff;border-radius:14px;padding:18px 20px;overflow-x:auto;font:13px/1.7 "JetBrains Mono",monospace;margin-top:14px}}
.ajs-code i{{color:#8f88b8;font-style:normal}}
.ajs-faq{{max-width:820px;margin:0 auto;display:grid;gap:10px}}
@media(max-width:860px){{.ajs-proof{{grid-template-columns:repeat(2,1fr)}}.ajs-steps,.ajs-two{{grid-template-columns:1fr}}}}
</style>

<section class="bx-sec" style="padding-top:30px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Does it work?</span><h2 class="display" id="s-proof">Built by a job seeker, for his own <span class="t2">search</span></h2>
      <p>The author built it after his role was cut in late 2025 and ran his search through it every week. He reports these numbers on the project README.</p></div>
    <div class="ajs-proof reveal">
      <div><b>69</b><span>tailored applications</span></div>
      <div><b>20</b><span>first interviews</span></div>
      <div><b>1</b><span>signed contract</span></div>
      <div><b>MIT</b><span>open source license</span></div>
    </div>
    <p class="ajs-note">Figures as reported by the project author. Your results depend on your profile and market.</p>
  </div>
</section>

<section class="bx-sec" id="how" style="padding-top:10px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">How it works</span><h2 class="display" id="s-how">Six commands, from empty profile to <span class="t3">offer</span></h2>
      <p>You run it inside Claude Code on your own machine. Each step is a slash command you can run on its own.</p></div>
    <div class="sc-lanes ajs-steps">{steps}</div>
  </div>
</section>

<section class="bx-sec" id="apply" style="padding-top:10px">
  <div class="wrap">
    <div class="ajs-two">
      <div class="ajs-card reveal"><span class="eyebrow">Inside /apply</span><h3>Why the applications come out sharp</h3><ul class="ajs-list">{apply}</ul></div>
      <div class="ajs-card reveal" id="setup"><span class="eyebrow">Quick start</span><h3>What you need</h3><ul class="ajs-needs">{needs}</ul>
<pre class="ajs-code"><i># private copy for your own search</i>
gh repo clone ai-job-search-dev/ai-job-search
cd ai-job-search
claude
<i># then, inside Claude Code</i>
/setup
/scrape
/apply &lt;job URL&gt;</pre>
        <div class="bx-ctas"><a class="btn btn-primary" href="{REPO}" target="_blank" rel="noopener" data-track="ajs_repo_click">Open on GitHub &rarr;</a><a class="btn btn-ghost" href="{REPO}/blob/master/SETUP.md" target="_blank" rel="noopener">Full setup guide</a></div>
      </div>
    </div>
  </div>
</section>

<section class="bx-sec" id="tips" style="padding-top:10px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">My notes</span><h2 class="display" id="s-notes">Use it well, use it <span class="t2">safely</span></h2></div>
    <div class="sc-lanes">
      <div class="sc-lane reveal"><b>01</b><h3>Feed it detail</h3><p>A thin profile gives generic applications. Describe projects, tools and measurable results for every role you held.</p></div>
      <div class="sc-lane reveal"><b>02</b><h3>Keep your copy private</h3><p>Clone it into a private repository. A fork is public, and setup writes your contact details and salary expectations into the files.</p></div>
      <div class="sc-lane reveal"><b>03</b><h3>Read before you send</h3><p>Postings are treated as untrusted input, but skim every CV and letter before you hit submit, especially from unfamiliar job boards.</p></div>
    </div>
    <div class="bx-ctas" style="justify-content:center;margin-top:28px"><a class="btn btn-primary" href="/interview-prep#coach">Practise with the AI interview coach</a><a class="btn btn-ghost" href="/jobs">Browse the job board</a><a class="btn btn-ghost" href="/schedule-meeting" data-track="schedule_click">Book a mock interview</a></div>
  </div>
</section>

<section class="bx-sec" id="faq" style="padding-top:10px">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">FAQ</span><h2 class="display" id="s-faq">Questions before you <span class="t3">start</span></h2></div>
    <div class="ajs-faq">{faq}</div>
    <p class="ajs-note">AI Job Search is an independent open source project by its maintainers on <a href="{REPO}" target="_blank" rel="noopener">GitHub</a>. Not affiliated with Anthropic or with this site.</p>
  </div>
</section>
'''


HERO = f'''<header class="page-hero ph-cv">
  <div class="wrap"><div class="ph-copy">
    <div class="crumbs"><a href="/">Home</a> / <a href="/interview-prep">Interview Prep</a> / AI Job Search</div>
    <h1 class="display">Let an AI agent run your job <span class="tg1">search.</span></h1>
    <p>A free, open source framework on Claude Code that finds roles, scores fit, tailors your CV and cover letter, and preps you for every interview round. Here is how it works and how to set it up.</p>
    <div class="bx-ctas" style="justify-content:flex-start;margin-top:18px"><a class="btn btn-primary lg" href="{REPO}" target="_blank" rel="noopener" data-track="ajs_repo_click">Get it on GitHub &rarr;</a><a class="btn btn-ghost lg" href="#how">See how it works</a></div>
  </div>
    <figure class="hero-cv"><img src="/img/covers/{SLUG}.jpg" alt="{ALT}" width="1200" height="750" fetchpriority="high" decoding="async"></figure>
  </div>
</header>
'''


def ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC,
             "isPartOf": {"@id": "https://syedcreates.com/#website"}, "author": {"@id": "https://syedcreates.com/#person"},
             "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://syedcreates.com/"},
                 {"@type": "ListItem", "position": 2, "name": "Interview Prep", "item": "https://syedcreates.com/interview-prep"},
                 {"@type": "ListItem", "position": 3, "name": "AI Job Search", "item": URL}]}},
            {"@type": "SoftwareSourceCode", "name": "AI Job Search", "codeRepository": REPO,
             "license": "https://opensource.org/licenses/MIT", "programmingLanguage": "Python",
             "description": "Open source job application framework built on Claude Code."},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }


def build_page():
    src = (SITE / "software-careers-for-students.html").read_text(encoding="utf-8")
    old_slug, old_url = "software-careers-for-students", "https://syedcreates.com/software-careers-for-students"
    head_end = src.find("</head>")
    head = src[:head_end]
    # title and meta
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(TITLE)}</title>", head, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + esc(DESC) + m.group(2), head)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + esc(TITLE) + m.group(2), head)
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', lambda m: m.group(1) + ALT + m.group(2), head)
    head = head.replace(old_url, URL).replace(f"/img/covers/og/{old_slug}.", f"/img/covers/og/{SLUG}.")
    # replace page specific JSON-LD (keep the site wide Person graph block)
    blocks = re.findall(r'<script type="application/ld\+json"[^>]*>.*?</script>', head, flags=re.S)
    for b in blocks:
        if "#person" in b and '"@type":"Person"' in b.replace(" ", "") and "FAQPage" not in b:
            continue
        head = head.replace(b, "")
    graph = ld()
    jobs = (SITE / "jobs.html").read_text(encoding="utf-8")
    for b in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', jobs, flags=re.S):
        for n in json.loads(b).get("@graph", []):
            if n.get("@type") == "Person":
                graph["@graph"].insert(0, n)
                break
    head += f'<script type="application/ld+json" data-k="ajs">{json.dumps(graph, ensure_ascii=False)}</script>\n'

    body = src[head_end:]
    body = body.replace(f'data-page="{old_slug}"', f'data-page="{SLUG}"')
    nav_end = body.find("</nav>") + len("</nav>")
    main_start = body.find('<main')
    m_end = body.find("</main>")
    main = body[main_start:m_end]
    cta_at = main.find('<section class="bx-sec svc-cta-sec"')
    tail = main[cta_at:] if cta_at >= 0 else ""
    page_scripts = body[m_end:]
    # drop scripts specific to the template page (quiz, filters) that follow </main>
    out = head + body[:nav_end] + "\n\n" + HERO + "\n" + main_html() + tail + page_scripts
    out = re.sub(r'<script>[^<]*sc-quiz[\s\S]*?</script>', "", out)
    (SITE / f"{SLUG}.html").write_text(out, encoding="utf-8")
    print("page written")


def nav():
    link_big = '<a href="/ai-job-search">AI Job Search Agent</a>'
    n = 0
    for f in SITE.rglob("*.html"):
        if "/x-" in str(f):
            continue
        h = f.read_text(encoding="utf-8")
        if 'href="/ai-job-search"' in h.split("</nav>")[0]:
            continue
        nh = h.replace('Cover Letter Builder</a><a href="/jobs">', 'Cover Letter Builder</a>' + link_big + '<a href="/jobs">')
        if nh != h:
            f.write_text(nh, encoding="utf-8"); n += 1
    print("nav link on", n, "pages")


PROMO = ('<section class="bx-sec" data-k="ajs-promo" style="padding-top:10px"><div class="wrap"><div class="svc-cta reveal">'
         '<div class="svc-cta-txt"><span class="eyebrow">New &middot; open source</span><h2 class="display">Let an AI agent run your job <span class="t2">search</span></h2>'
         '<p>An open source framework on Claude Code that finds roles, tailors your CV and cover letter, and preps every interview round. '
         'Here is how it works and how to set it up.</p></div><div class="svc-cta-btns"><a class="btn btn-primary" href="/ai-job-search">See the AI Job Search guide</a></div></div></div></section>')


def promos():
    for name in ("interview-prep.html", "jobs.html"):
        f = SITE / name
        h = f.read_text(encoding="utf-8")
        if 'data-k="ajs-promo"' in h:
            continue
        at = h.find('<section class="bx-sec svc-cta-sec"')
        if at < 0:
            at = h.find("</main>")
        h = h[:at] + PROMO + h[at:]
        f.write_text(h, encoding="utf-8")
    print("promo added to interview-prep and jobs")


def sitemap_llms():
    sm = SITE / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    if URL not in s:
        s = s.replace("</urlset>", f"  <url><loc>{URL}</loc><lastmod>2026-11-17</lastmod><priority>0.7</priority></url>\n</urlset>")
        sm.write_text(s, encoding="utf-8")
    lt = SITE / "llms.txt"
    t = lt.read_text(encoding="utf-8")
    line = f"- [AI Job Search Agent]({URL}): setup guide for the open source AI job search framework on Claude Code, which finds roles, tailors CVs and cover letters, and preps interviews"
    if URL + ")" not in t:
        if "/interview-prep)" in t:
            t = re.sub(r"(.*\(https://syedcreates\.com/interview-prep\)[^\n]*\n)", lambda m: m.group(1) + line + "\n", t, count=1)
        else:
            t = t.rstrip("\n") + "\n" + line + "\n"
        lt.write_text(t, encoding="utf-8")
    print("sitemap and llms.txt updated")


if __name__ == "__main__":
    build_page(); nav(); promos(); sitemap_llms()
