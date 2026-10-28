# Created by: Claude
# Date: 2026-10-28
# Purpose: Shared partials (head, nav, proof strip, footer) for the Syed Hadi site
# Owner: Syed Hadi

DECK = "https://docs.google.com/presentation/d/11ro9a8Xxxv5hLKMMLTbSyHsYfrtDDCxWhrt7NwQqV-8/edit?usp=sharing"
RESUME = "https://drive.google.com/file/d/1YU9wvSdp2u5JmpGMzv2FoJk_xfd6Izmu/view?usp=drive_link"
EMAIL = "mailto:ssyedhadi14@gmail.com?subject=Let%27s%20talk"
CALENDLY = "https://calendly.com/syedhadi/30min"
LINKEDIN = "https://www.linkedin.com/in/syedhadii/"

PAGES = [
    ("home", "index.html", "Home"),
    ("gtm", "gtm-engine.html", "GTM Engine"),
    ("systems", "systems.html", "Systems"),
    ("recognition", "recognition.html", "Recognition"),
    ("playbook", "playbook.html", "Playbook"),
    ("events", "events.html", "Events"),
    ("writing", "writing.html", "Writing"),
    ("tools", "tools.html", "Tools"),
]

ICON_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>'
ICON_DECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>'
ICON_EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg>'

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%235b3df5'/%3E%3Ctext x='32' y='42' font-family='Arial' font-weight='800' font-size='28' fill='white' text-anchor='middle'%3ESH%3C/text%3E%3C/svg%3E"


def head(key, label):
    from seo import meta_tags
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{meta_tags(key, label)}
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/img/favicon-192.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>'''


def nav():
    from nav_mega import mega_nav
    return mega_nav(RESUME, DECK, CALENDLY, LINKEDIN)


def strip():
    pages = "".join(
        f'<a href="{href}">{label}</a>' for key, href, label in PAGES if key != "home"
    )
    return f'''<div class="proof-strip">
  <div class="wrap">
    <div class="proof-in">
      <div class="lbl"><span class="dot"></span><span>Product Marketing Workproof, May 2024 to date<small>The full deck behind every number on this site, plus the resume.</small></span></div>
      <div class="proof-links">
        <a class="solid" href="{DECK}" target="_blank" rel="noopener">{ICON_DECK}Open the Workproof Deck</a>
        <a href="{RESUME}" target="_blank" rel="noopener">{ICON_DOC}View Resume</a>
      </div>
    </div>
    <div class="proof-pages">{pages}</div>
  </div>
</div>'''


def footer():
    return f'''<footer>
  <div class="wrap foot">
    <span>&copy; <span id="yr">2026</span> Syed Hadi. Bengaluru, India.</span>
    <span><a href="{DECK}" target="_blank" rel="noopener">Workproof Deck</a> &nbsp;&middot;&nbsp; <a href="{RESUME}" target="_blank" rel="noopener">Resume</a> &nbsp;&middot;&nbsp; <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></span>
  </div>
</footer>'''


def cta():
    return f'''<section class="cta" style="padding-top:20px">
  <div class="wrap">
    <div class="cta-box reveal">
      <h2 class="display">Ready to Grow<br>Something Together?</h2>
      <p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls.</p>
      <div class="btns">
        <a class="btn btn-primary" href="{CALENDLY}" target="_blank" rel="noopener">Schedule meeting</a>
        <a class="btn btn-ghost" href="{EMAIL}">Email Me</a>
      </div>
    </div>
  </div>
</section>'''


def next_links(key):
    keys = [p[0] for p in PAGES]
    i = keys.index(key)
    prev = PAGES[i - 1] if i > 0 else None
    nxt = PAGES[i + 1] if i + 1 < len(PAGES) else PAGES[0]
    out = '<div class="wrap next-page">'
    if prev:
        out += f'<a href="{prev[1]}"><small>PREVIOUS</small><b>&larr; {prev[2]}</b></a>'
    out += f'<a class="right" href="{nxt[1]}"><small>NEXT</small><b>{nxt[2]} &rarr;</b></a></div>'
    return out


def page(key, title, desc, hero_eyebrow, hero_h1, hero_p, body):
    return f'''{head(key, hero_eyebrow)}
<body data-page="{key}">

{nav()}

<header class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / {hero_eyebrow}</div>
    <h1 class="display">{hero_h1}</h1>
    <p>{hero_p}</p>
  </div>
</header>

{strip()}

<main>
{body}
</main>

{next_links(key)}

{cta()}

{footer()}
<script src="assets/common.js"></script>
</body>
</html>
'''
