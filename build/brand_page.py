#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate /brand for syedcreates.com (logo, type, colour, headshot, voice, boilerplate, downloads) plus the A4 brand kit PDF and logo zip
# Owner: Syed Hadi
import json, os, re, subprocess, sys, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import SITE, VER  # noqa: E402

ROOT = "/home/claude/work/site"
shell = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()
nav = re.search(r"<nav>.*?</nav>", shell, re.S).group(0)
foot = re.search(r"<footer class=\"site-foot\">.*?</footer>", shell, re.S).group(0)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)
nl = re.search(r'<section class="newsletter[^"]*" aria-labelledby="nl-title">.*?</section>', shell, re.S)
nl = nl.group(0) if nl else ""

URL = SITE + "/brand"
TITLE = "Brand Kit: Syed Hadi Logo, Fonts, Colours and Headshot"
DESC = "Official brand assets for Syed Hadi and syedcreates.com: logo files in SVG and PNG, the type system, colour palette, approved headshot, bio and a downloadable PDF brand kit for event organisers and press."

COLORS = [
    ("Ink", "#0d0b1a", "Headlines, body on light"), ("Accent", "#5b3df5", "Buttons, links, one word per headline"),
    ("Accent 2", "#7c5cff", "Gradients, dark mode accent"), ("Accent soft", "#efebff", "Tints, highlighted rows"),
    ("Paper", "#ffffff", "Light background"), ("Soft", "#f7f6fb", "Section bands"),
    ("Night", "#0b0a12", "Dark background"), ("Ink 2", "#4a4760", "Secondary text"),
    ("Green", "#10b981", "Positive numbers, on track"), ("Rose", "#f43f5e", "Interest, risk, down"), ("Amber", "#f59e0b", "Warnings, callouts"),
]
FONTS = [
    ("Plus Jakarta Sans", "Display", "600, 700, 800", "Headlines, numbers, card titles, the wordmark. Tight tracking, minus 3.5% on display sizes.", "font-family:'Plus Jakarta Sans';font-weight:800;letter-spacing:-.035em", "Pipeline is the only scoreboard."),
    ("Instrument Serif", "Accent", "400 italic", "One word per headline, pull quotes, the tagline. Never for body copy, never more than a phrase.", "font-family:'Instrument Serif';font-style:italic;font-weight:400", "growth, in public"),
    ("Inter", "Body", "400, 500, 600", "Paragraphs, UI, forms, tables. 16px on web, 1.6 line height.", "font-family:Inter;font-weight:400;font-size:22px;line-height:1.5", "Six years of B2B SaaS go to market taught me one thing: the useful stuff never makes it into a deck."),
    ("JetBrains Mono", "Labels", "500", "Eyebrows, dates, tags, chart ticks. Uppercase with 0.2em tracking at 12px.", "font-family:'JetBrains Mono';font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:16px", "GTM  /  PMM  /  PARTNERS  /  AEO"),
]
LOGOS = [
    ("syed-hadi-logo", "Primary lockup", "Mark, name and tagline. Use on light backgrounds.", "light"),
    ("syed-hadi-logo-white", "Primary lockup, white", "Same lockup for dark backgrounds and photos.", "dark"),
    ("syed-hadi-logo-compact", "Compact lockup", "Mark and name, no tagline. Navigation bars, email signatures.", "light"),
    ("syed-hadi-logo-black", "Mono lockup", "Single colour for print, embossing and low ink contexts.", "light"),
    ("syed-hadi-mark", "Mark", "Favicon, avatars, app icon. Minimum 24px.", "light"),
    ("syedcreates-wordmark", "Wordmark", "The site name as a standalone word. Footers and watermarks.", "light"),
]
BIO_SHORT = "Syed Hadi leads product marketing and partnerships at AccuKnox, a Zero Trust CNAPP and AI security company built on the CNCF project KubeArmor. He writes Pipeline Notes and builds free GTM playbooks and India focused finance calculators at syedcreates.com."
BIO_MED = ("Syed Hadi is Product Marketing and Partnerships Lead at AccuKnox, where he runs positioning, launches and a channel program spanning India, MENA, APAC, Japan, Europe, Africa and the US. "
           "Before that he moved from project management into go to market across two security startups. He has spoken at KubeCon India, BSides and the Kubernetes Bangalore meetup, was featured by Humans of Marketing, "
           "and publishes GTM frameworks, case studies with numbers and six free calculators at syedcreates.com. His newsletter, Pipeline Notes, covers pipeline math, partner revenue, positioning and AEO for AI search.")

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#person"}, "dateModified": "2026-11-02"},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Brand", "item": URL}]},
    {"@type": "ImageObject", "contentUrl": SITE + "/img/syed-hadi-2026.jpg", "name": "Syed Hadi headshot, 2026", "creditText": "Syed Hadi", "license": SITE + "/brand", "acquireLicensePage": URL},
]}

def swatch(n, hx, use):
    light = hx.lower() in ("#ffffff", "#f7f6fb", "#efebff")
    return f'<div class="sw"><i style="background:{hx}{";border:1px solid var(--line)" if light else ""}"></i><b>{n}</b><code>{hx}</code><small>{use}</small></div>'

def logo_card(slug, name, use, bg):
    return (f'<div class="lg-card"><div class="lg-prev {bg}"><img src="/brand-assets/{slug}.svg" alt="{name}" loading="lazy"></div>'
            f'<div class="lg-body"><b>{name}</b><p>{use}</p><div class="lg-dl"><a class="btn btn-ghost" href="/brand-assets/{slug}.svg" download>SVG</a><a class="btn btn-ghost" href="/brand-assets/{slug}.png" download>PNG</a></div></div></div>')

def font_card(name, role, weights, use, style, sample):
    return (f'<div class="ft-card"><div class="ft-sample" style="{style}">{sample}</div><div class="ft-meta"><span class="eyebrow">{role}</span><b>{name}</b><small>Weights {weights}</small><p>{use}</p></div></div>')

CSS = '''
.br-hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center}
.br-head{display:flex;justify-content:flex-end}
.br-head img{width:min(100%,420px);height:auto;aspect-ratio:1;object-fit:cover;border-radius:28px;box-shadow:0 30px 70px rgba(28,16,80,.22)}
.br-quick{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.lg-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.lg-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--card)}
.lg-prev{display:grid;place-items:center;padding:34px 28px;min-height:190px;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:22px 22px}
.lg-prev.light{background-color:#fff} .lg-prev.dark{background-color:#0b0a12;--grid:rgba(255,255,255,.06)}
.lg-prev img{max-width:100%;max-height:120px;width:auto;height:auto}
.lg-body{padding:16px 18px 18px} .lg-body b{display:block;font-size:17px} .lg-body p{margin:4px 0 12px;font-size:14px;color:var(--ink-2);line-height:1.5}
.lg-dl{display:flex;gap:8px} .lg-dl .btn{padding:8px 14px;font-size:13px}
.rules{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.rules div{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card)} .rules b{display:block;margin-bottom:6px;font-size:16px} .rules p{margin:0;font-size:14px;color:var(--ink-2);line-height:1.55}
.sw-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.sw{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--card)} .sw i{display:block;height:84px} .sw b{display:block;padding:10px 12px 0;font-size:14px} .sw code{display:block;padding:2px 12px;font:500 12px "JetBrains Mono",monospace;color:var(--accent)} .sw small{display:block;padding:0 12px 12px;font-size:12px;color:var(--ink-3);line-height:1.4}
.ft-card{display:grid;grid-template-columns:1.4fr .8fr;gap:24px;align-items:center;border:1px solid var(--line);border-radius:20px;padding:26px 28px;background:var(--card);margin-bottom:14px}
.ft-sample{font-size:clamp(28px,4vw,52px);line-height:1.08;color:var(--ink);overflow-wrap:anywhere}
.ft-meta b{display:block;font-size:20px;margin:6px 0 2px} .ft-meta small{color:var(--ink-3);font-size:13px} .ft-meta p{margin:8px 0 0;font-size:14px;color:var(--ink-2);line-height:1.55}
.code{background:#0d0b1a;color:#e9e6ff;border-radius:14px;padding:18px 20px;font:500 13px/1.6 "JetBrains Mono",monospace;overflow:auto;white-space:pre}
[data-theme=dark] .code{background:#14131f}
.hs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start}
.hs-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--card)} .hs-card img{width:100%;display:block;aspect-ratio:1;object-fit:cover} .hs-card.round img{border-radius:50%;padding:22px} .hs-card.bw img{filter:grayscale(1) contrast(1.05)}
.hs-card .lg-body{padding:14px 18px 18px}
.bio{border:1px solid var(--line);border-radius:20px;padding:24px 26px;background:var(--card);margin-bottom:14px} .bio span.eyebrow{display:block;margin-bottom:8px} .bio p{margin:0;font-size:16px;line-height:1.65}
.bio .cp{margin-top:12px;padding:8px 14px;font-size:13px}
.dl-band{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.dl-band a{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:18px;padding:22px;background:var(--card);text-decoration:none;color:inherit}
.dl-band a:hover{border-color:var(--accent)} .dl-band b{font-size:18px} .dl-band span{font-size:14px;color:var(--ink-2)} .dl-band em{font-style:normal;color:var(--accent);font-weight:700;font-size:14px;margin-top:6px}
.voice{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.voice div{border-left:3px solid var(--accent);padding:4px 0 4px 16px} .voice b{display:block;font-size:16px} .voice p{margin:4px 0 0;font-size:14.5px;color:var(--ink-2);line-height:1.55}
@media (max-width:1100px){.sw-grid{grid-template-columns:repeat(4,1fr)}}
@media (max-width:980px){.br-hero .wrap{grid-template-columns:1fr}.br-head{justify-content:flex-start}.lg-grid{grid-template-columns:repeat(2,1fr)}.rules{grid-template-columns:1fr}.hs-grid{grid-template-columns:repeat(3,1fr)}.dl-band{grid-template-columns:1fr}.ft-card{grid-template-columns:1fr}}
@media (max-width:620px){.lg-grid{grid-template-columns:1fr}.sw-grid{grid-template-columns:repeat(2,1fr)}.hs-grid{grid-template-columns:1fr}.voice{grid-template-columns:1fr}}
'''

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
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/img/og-card.jpg">
<script type="application/ld+json">{json.dumps(JSONLD, ensure_ascii=False)}</script>
{icons}
<style>{CSS}</style>
</head>
<body data-page="brand">
{nav}
<header class="page-hero br-hero">
<div class="wrap">
<div>
<div class="crumbs"><a href="/">Home</a> / Brand</div>
<span class="eyebrow">Brand kit</span>
<h1 class="display" style="font-size:clamp(40px,6vw,76px)">One name, one <span>voice</span>, everywhere.</h1>
<p>Everything you need to put Syed Hadi on a stage slide, a podcast cover, a press mention or a partner page. Logo files, the type system, colours, an approved headshot and a bio you can paste. Free to use when writing about or featuring Syed.</p>
<div class="br-quick"><a class="btn btn-primary" href="/downloads/syed-hadi-brand-kit.pdf" download>Download the brand kit (PDF)</a><a class="btn btn-ghost" href="/downloads/syed-hadi-logo-pack.zip" download>Logo pack (SVG + PNG)</a><a class="btn btn-ghost" href="/img/syed-hadi-2026.jpg" download>Headshot</a></div>
</div>
<div class="br-head"><img src="/img/syed-hadi-2026.jpg" alt="Syed Hadi, approved headshot 2026" width="720" height="720" fetchpriority="high" decoding="async"></div>
</div>
</header>
<main id="main">

<section class="bx-sec" id="logo">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">01 Logo</span><h2 class="display">The Mark and the <span>Lockups</span></h2>
    <p>The mark is an S with a growth tick, set in a rounded square on the accent gradient. The name sits in Plus Jakarta Sans 800, the tagline in Instrument Serif italic. Six files cover every use.</p></div>
    <div class="lg-grid">{"".join(logo_card(*l) for l in LOGOS)}</div>
    <div class="rules" style="margin-top:22px">
      <div class="reveal"><b>Clear space</b><p>Keep space equal to the height of the S around every side of the lockup. Nothing else inside that box.</p></div>
      <div class="reveal"><b>Minimum size</b><p>Lockup 140px wide on screen, 35mm in print. Mark alone 24px. Below that, use the mark only.</p></div>
      <div class="reveal"><b>Do not</b><p>Recolour the mark, stretch it, add a drop shadow, place the colour lockup on a busy photo, or set the name in another typeface.</p></div>
    </div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="colour">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">02 Colour</span><h2 class="display">Ink, Accent and <span>Three Signals</span></h2>
    <p>One accent, used sparingly: a button, a link, one word in a headline. The three signal colours mean the same thing on every chart and calculator.</p></div>
    <div class="sw-grid">{"".join(swatch(*c) for c in COLORS)}</div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="type">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">03 Typography</span><h2 class="display">Four Fonts, Four <span>Jobs</span></h2>
    <p>A geometric display face for headlines, an italic serif for a single accent word, a neutral body face and a mono for labels. The contrast between the sans and the serif is the whole personality.</p></div>
    {"".join(font_card(*f) for f in FONTS)}
    <div class="rules" style="margin-top:8px">
      <div class="reveal"><b>Headline formula</b><p>Sentence case, Plus Jakarta Sans 800, minus 3.5% tracking, line height 1.02. Exactly one word or phrase in Instrument Serif italic, coloured accent.</p></div>
      <div class="reveal"><b>Scale</b><p>Display 56 to 88px. Section titles 34 to 56px. Card titles 18 to 22px. Body 16px, small 14px, labels 12px uppercase.</p></div>
      <div class="reveal"><b>Load it</b><p>Plus Jakarta Sans and Instrument Serif are self hosted on syedcreates.com. Inter and JetBrains Mono come from Google Fonts. All four are open licence (OFL).</p></div>
    </div>
    <div class="code reveal" style="margin-top:14px">&lt;link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&amp;family=Instrument+Serif:ital@1&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@500&amp;display=swap" rel="stylesheet"&gt;

h1 {{ font-family: "Plus Jakarta Sans"; font-weight: 800; letter-spacing: -.035em; line-height: 1.02; }}
h1 span {{ font-family: "Instrument Serif"; font-style: italic; font-weight: 400; color: #5b3df5; }}
body {{ font-family: Inter; font-size: 16px; line-height: 1.6; color: #0d0b1a; }}
.eyebrow {{ font-family: "JetBrains Mono"; font-size: 12px; letter-spacing: .2em; text-transform: uppercase; }}</div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="headshot">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">04 Headshot</span><h2 class="display">The Approved <span>Photo</span></h2>
    <p>One photo, three crops. Use it as supplied, no filters beyond the black and white version here. Credit is not required. For print above A5, ask for the original file.</p></div>
    <div class="hs-grid">
      <div class="hs-card reveal"><img src="/img/syed-hadi-2026.jpg" alt="Syed Hadi headshot, square crop" width="720" height="720" loading="lazy"><div class="lg-body"><b>Square</b><p>Speaker cards, LinkedIn, press. 720 × 720.</p><div class="lg-dl"><a class="btn btn-ghost" href="/img/syed-hadi-2026.jpg" download>JPG</a></div></div></div>
      <div class="hs-card round reveal"><img src="/img/syed-hadi-2026.jpg" alt="Syed Hadi headshot, circular crop" width="720" height="720" loading="lazy"><div class="lg-body"><b>Circle</b><p>Avatars, bylines, podcast tiles. Crop from the square file.</p><div class="lg-dl"><a class="btn btn-ghost" href="/brand-assets/syed-hadi-headshot-circle.png" download>PNG</a></div></div></div>
      <div class="hs-card bw reveal"><img src="/img/syed-hadi-2026.jpg" alt="Syed Hadi headshot, black and white" width="720" height="720" loading="lazy"><div class="lg-body"><b>Mono</b><p>Editorial layouts and dark stage slides.</p><div class="lg-dl"><a class="btn btn-ghost" href="/brand-assets/syed-hadi-headshot-mono.jpg" download>JPG</a></div></div></div>
    </div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="voice">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">05 Voice</span><h2 class="display">How It <span>Sounds</span></h2>
    <p>If you are writing copy that carries the name, these five rules keep it consistent with everything on this site.</p></div>
    <div class="voice">
      <div class="reveal"><b>Numbers before adjectives</b><p>$2M of pipeline on a $25K quarter says more than "high impact". If there is a number, lead with it.</p></div>
      <div class="reveal"><b>Active voice, short sentences</b><p>"Partners sourced 40% of pipeline", not "40% of pipeline was sourced through partner channels".</p></div>
      <div class="reveal"><b>Plain punctuation</b><p>No em dashes, no semicolons, no exclamation marks. Commas and full stops carry the rhythm.</p></div>
      <div class="reveal"><b>Prevention first, GTM always</b><p>The subject is pipeline and how a technical product gets bought. Security is the industry, not the tone.</p></div>
      <div class="reveal"><b>Name, then role</b><p>First mention: Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox. After that, Syed.</p></div>
      <div class="reveal"><b>Links that earn a click</b><p>Point to syedcreates.com, the calculators or Pipeline Notes. Never to a generic bio page.</p></div>
    </div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="bio">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">06 Boilerplate</span><h2 class="display">Bio You Can <span>Paste</span></h2></div>
    <div class="bio reveal"><span class="eyebrow">Short, 45 words</span><p id="bioS">{BIO_SHORT}</p><button type="button" class="btn btn-ghost cp" data-cp="bioS">Copy short bio</button></div>
    <div class="bio reveal"><span class="eyebrow">Medium, 110 words</span><p id="bioM">{BIO_MED}</p><button type="button" class="btn btn-ghost cp" data-cp="bioM">Copy medium bio</button></div>
    <div class="bio reveal"><span class="eyebrow">Links</span><p>Site <a href="{SITE}">syedcreates.com</a> · Newsletter <a href="https://syedhadi.substack.com">syedhadi.substack.com</a> · LinkedIn <a href="https://www.linkedin.com/in/syedhadii/">linkedin.com/in/syedhadii</a> · Medium <a href="https://ssyedhadi.medium.com/">ssyedhadi.medium.com</a> · Book a slot <a href="/schedule-meeting">syedcreates.com/schedule-meeting</a></p></div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0" id="downloads">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">07 Downloads</span><h2 class="display">Take the <span>Kit</span></h2></div>
    <div class="dl-band">
      <a class="reveal" href="/downloads/syed-hadi-brand-kit.pdf" download><b>Brand kit PDF</b><span>Logo, colour, type, headshot, voice and bio on four A4 pages. Send this to organisers and designers.</span><em>Download PDF &rarr;</em></a>
      <a class="reveal" href="/downloads/syed-hadi-logo-pack.zip" download><b>Logo pack</b><span>All six logo files as SVG and PNG, plus a 1024px mark for avatars and app icons.</span><em>Download ZIP &rarr;</em></a>
      <a class="reveal" href="/img/syed-hadi-2026.jpg" download><b>Headshot</b><span>The approved 2026 photo, 720 × 720 JPG, plus circle and mono versions above.</span><em>Download JPG &rarr;</em></a>
    </div>
    <p class="fr-disc">Assets on this page may be used to identify Syed Hadi in editorial, event and partner contexts. They may not be used to imply endorsement of a product or service. Questions: <a href="/schedule-meeting">book a slot</a> or reply to any Pipeline Notes email.</p>
  </div>
</section>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('.cp');if(!b)return;var t=document.getElementById(b.dataset.cp).textContent,o=b.textContent,done=function(){{b.textContent='Copied';setTimeout(function(){{b.textContent=o}},1600)}};if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(done,function(){{fallback()}})}}else fallback();function fallback(){{var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{{document.execCommand('copy');done()}}catch(e){{}}a.remove()}}}});</script>
</main>
{nl}
{foot}
</body>
</html>
'''
open(os.path.join(ROOT, "brand.html"), "w", encoding="utf-8").write(page)

# headshot variants
from PIL import Image, ImageDraw, ImageOps
im = Image.open(os.path.join(ROOT, "img/syed-hadi-2026.jpg")).convert("RGB")
ImageOps.grayscale(im).convert("RGB").save(os.path.join(ROOT, "brand-assets/syed-hadi-headshot-mono.jpg"), quality=90)
m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((0, 0) + im.size, fill=255)
rgba = im.convert("RGBA"); rgba.putalpha(m); rgba.save(os.path.join(ROOT, "brand-assets/syed-hadi-headshot-circle.png"))

# logo zip
os.makedirs(os.path.join(ROOT, "downloads"), exist_ok=True)
with zipfile.ZipFile(os.path.join(ROOT, "downloads/syed-hadi-logo-pack.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for n in sorted(os.listdir(os.path.join(ROOT, "brand-assets"))):
        if n.startswith(("syed-hadi-logo", "syed-hadi-mark", "syedcreates-wordmark")):
            z.write(os.path.join(ROOT, "brand-assets", n), "syed-hadi-logo-pack/" + n)
    z.writestr("syed-hadi-logo-pack/README.txt", "Syed Hadi logo pack\nsyedcreates.com/brand\n\nColour: #5b3df5 to #7c5cff gradient, ink #0d0b1a.\nType: Plus Jakarta Sans 800 (name), Instrument Serif italic (tagline).\nClear space: height of the S on all sides. Minimum width 140px / 35mm. Mark alone from 24px.\nUse to identify Syed Hadi in editorial, event and partner contexts.\n")

# ---- A4 brand kit PDF via Playwright ----
F = ROOT + "/assets/fonts/web"
pdf_html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:PJ;font-weight:800;src:url(file://{F}/plus-jakarta-sans-latin-800-normal.woff2)}}
@font-face{{font-family:PJ;font-weight:700;src:url(file://{F}/plus-jakarta-sans-latin-700-normal.woff2)}}
@font-face{{font-family:PJ;font-weight:600;src:url(file://{F}/plus-jakarta-sans-latin-600-normal.woff2)}}
@font-face{{font-family:IS;font-style:italic;src:url(file://{F}/instrument-serif-latin-400-italic.woff2)}}
@font-face{{font-family:IN;font-weight:400;src:url(file:///home/claude/fonts/fontsource-inter-5.3.0/package/files/inter-latin-400-normal.woff2)}}
@font-face{{font-family:IN;font-weight:600;src:url(file:///home/claude/fonts/fontsource-inter-5.3.0/package/files/inter-latin-600-normal.woff2)}}
@font-face{{font-family:JB;font-weight:500;src:url(file:///home/claude/fonts/fontsource-jetbrains-mono-5.3.0/package/files/jetbrains-mono-latin-500-normal.woff2)}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}} body{{margin:0;font-family:IN;color:#0d0b1a;-webkit-print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;padding:18mm 16mm 16mm;page-break-after:always;position:relative;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.eb{{font-family:JB;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#7c7992}}
h1{{font-family:PJ;font-weight:800;font-size:46px;letter-spacing:-.035em;line-height:1.02;margin:8px 0 12px}} h1 i,h2 i{{font-family:IS;font-style:italic;font-weight:400;color:#5b3df5}}
h2{{font-family:PJ;font-weight:800;font-size:28px;letter-spacing:-.03em;margin:6px 0 10px;line-height:1.05}}
p{{font-size:11px;line-height:1.6;color:#4a4760;margin:0 0 8px}} .ft{{position:absolute;left:16mm;right:16mm;bottom:10mm;display:flex;justify-content:space-between;font-family:JB;font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:#7c7992;border-top:1px solid #e8e6f0;padding-top:6px}}
.cover{{background:#0b0a12;color:#fff}} .cover p{{color:#b9b5d0}} .cover .eb{{color:#a592ff}}
.band{{position:absolute;right:-60mm;top:-40mm;width:170mm;height:170mm;border-radius:50%;background:radial-gradient(circle at 30% 30%,#7c5cff,#5b3df5 55%,transparent 72%);opacity:.7}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}} .grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}} .grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.card{{border:1px solid #e8e6f0;border-radius:10px;padding:10px 12px;background:#fff}} .card b{{display:block;font-family:PJ;font-weight:700;font-size:12px;margin-bottom:3px}} .card p{{font-size:10px;margin:0}}
.lp{{border:1px solid #e8e6f0;border-radius:10px;display:grid;place-items:center;height:46mm;background:#fff}} .lp.dk{{background:#0b0a12}} .lp img{{max-width:78%;max-height:26mm}}
.sw{{border:1px solid #e8e6f0;border-radius:8px;overflow:hidden}} .sw i{{display:block;height:16mm}} .sw b{{display:block;font-family:PJ;font-size:10px;padding:5px 8px 0}} .sw code{{display:block;font-family:JB;font-size:8.5px;color:#5b3df5;padding:0 8px 6px}}
.spec{{border:1px solid #e8e6f0;border-radius:10px;padding:12px 14px;margin-bottom:8px;display:grid;grid-template-columns:1.5fr 1fr;gap:12px;align-items:center}} .spec .s{{font-size:26px;line-height:1.1}} .spec b{{display:block;font-family:PJ;font-weight:700;font-size:12px}} .spec small{{font-size:9.5px;color:#7c7992}} .spec p{{font-size:10px;margin:4px 0 0}}
.hs{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}} .hs img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}} .hs .r img{{border-radius:50%}} .hs .m img{{filter:grayscale(1)}}
.bio{{border-left:3px solid #5b3df5;padding:2px 0 2px 12px;margin:10px 0}} .bio p{{color:#0d0b1a;font-size:10.5px}}
</style></head><body>
<section class="pg cover"><div class="band"></div><div style="position:relative"><span class="eb">Brand kit · November 2026</span><h1 style="font-size:64px;max-width:150mm">Syed Hadi<br>brand <i>kit</i>.</h1><p style="max-width:120mm;font-size:13px">Logo, colour, type, headshot, voice and bio. Everything needed to feature Syed Hadi on a stage, a page or a podcast. Live version and downloads at syedcreates.com/brand.</p></div>
<img src="file://{ROOT}/brand-assets/syed-hadi-logo-white.svg" style="position:absolute;left:16mm;bottom:28mm;width:80mm"><div class="ft" style="border-color:#26243a;color:#8a86a3"><span>syedcreates.com/brand</span><span>Page 1 of 4</span></div></section>
<section class="pg"><span class="eb">01 Logo</span><h2>The mark and the <i>lockups</i></h2><p>An S with a growth tick in a rounded square on the accent gradient. Name in Plus Jakarta Sans 800, tagline in Instrument Serif italic.</p>
<div class="grid2"><div class="lp"><img src="file://{ROOT}/brand-assets/syed-hadi-logo.svg"></div><div class="lp dk"><img src="file://{ROOT}/brand-assets/syed-hadi-logo-white.svg"></div><div class="lp"><img src="file://{ROOT}/brand-assets/syed-hadi-logo-compact.svg"></div><div class="lp"><img src="file://{ROOT}/brand-assets/syed-hadi-logo-black.svg"></div><div class="lp"><img src="file://{ROOT}/brand-assets/syed-hadi-mark.svg" style="max-height:22mm"></div><div class="lp"><img src="file://{ROOT}/brand-assets/syedcreates-wordmark.svg"></div></div>
<div class="grid3" style="margin-top:10px"><div class="card"><b>Clear space</b><p>Height of the S on all sides.</p></div><div class="card"><b>Minimum size</b><p>Lockup 140px / 35mm. Mark alone from 24px.</p></div><div class="card"><b>Do not</b><p>Recolour, stretch, shadow, or set the name in another typeface.</p></div></div>
<span class="eb" style="display:block;margin-top:14px">02 Colour</span><h2 style="font-size:22px">Ink, accent and three <i>signals</i></h2>
<div class="grid4">{"".join(f'<div class="sw"><i style="background:{hx};{"border-bottom:1px solid #e8e6f0" if hx in ("#ffffff","#f7f6fb","#efebff") else ""}"></i><b>{n}</b><code>{hx}</code></div>' for n,hx,_ in COLORS[:8])}</div>
<div class="ft"><span>syedcreates.com/brand</span><span>Page 2 of 4</span></div></section>
<section class="pg"><span class="eb">03 Typography</span><h2>Four fonts, four <i>jobs</i></h2><p>Headline formula: Plus Jakarta Sans 800, minus 3.5% tracking, one word in Instrument Serif italic coloured accent. Body in Inter 16px. Labels in JetBrains Mono uppercase.</p>
<div class="spec"><div class="s" style="font-family:PJ;font-weight:800;letter-spacing:-.035em">Pipeline is the only scoreboard.</div><div><b>Plus Jakarta Sans</b><small>Display · 600, 700, 800</small><p>Headlines, numbers, card titles, the wordmark.</p></div></div>
<div class="spec"><div class="s" style="font-family:IS;font-style:italic;font-size:34px">growth, in public</div><div><b>Instrument Serif</b><small>Accent · 400 italic</small><p>One word per headline, pull quotes, the tagline. Never body copy.</p></div></div>
<div class="spec"><div class="s" style="font-family:IN;font-size:15px;line-height:1.5">Six years of B2B SaaS go to market taught me one thing: the useful stuff never makes it into a deck.</div><div><b>Inter</b><small>Body · 400, 500, 600</small><p>Paragraphs, UI, forms, tables.</p></div></div>
<div class="spec"><div class="s" style="font-family:JB;font-size:12px;letter-spacing:.2em;text-transform:uppercase">GTM / PMM / Partners / AEO</div><div><b>JetBrains Mono</b><small>Labels · 500</small><p>Eyebrows, dates, tags, chart ticks.</p></div></div>
<div class="grid3"><div class="card"><b>Scale</b><p>Display 56 to 88px. Sections 34 to 56. Cards 18 to 22. Body 16, small 14, labels 12.</p></div><div class="card"><b>Case</b><p>Sentence case everywhere except mono labels, which are uppercase.</p></div><div class="card"><b>Licence</b><p>All four are SIL Open Font Licence. Google Fonts or self host.</p></div></div>
<div class="ft"><span>syedcreates.com/brand</span><span>Page 3 of 4</span></div></section>
<section class="pg"><span class="eb">04 Headshot</span><h2>The approved <i>photo</i></h2>
<div class="hs"><div><img src="file://{ROOT}/img/syed-hadi-2026.jpg"></div><div class="r"><img src="file://{ROOT}/img/syed-hadi-2026.jpg"></div><div class="m"><img src="file://{ROOT}/img/syed-hadi-2026.jpg"></div></div>
<p style="margin-top:8px">Use as supplied. Square for speaker cards and press, circle for avatars and bylines, mono for editorial and dark slides. No credit required. Files at syedcreates.com/brand.</p>
<span class="eb" style="display:block;margin-top:10px">05 Voice</span><h2 style="font-size:22px">How it <i>sounds</i></h2>
<div class="grid2"><div class="card"><b>Numbers before adjectives</b><p>$2M of pipeline on a $25K quarter beats "high impact".</p></div><div class="card"><b>Active voice, short sentences</b><p>Partners sourced 40% of pipeline.</p></div><div class="card"><b>Plain punctuation</b><p>No em dashes, semicolons or exclamation marks.</p></div><div class="card"><b>Name, then role</b><p>Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox. Then Syed.</p></div></div>
<span class="eb" style="display:block;margin-top:12px">06 Boilerplate</span>
<div class="bio"><p><b style="font-family:PJ">Short.</b> {BIO_SHORT}</p></div>
<div class="bio"><p><b style="font-family:PJ">Medium.</b> {BIO_MED}</p></div>
<p style="font-size:10px">Site syedcreates.com · Newsletter syedhadi.substack.com · LinkedIn linkedin.com/in/syedhadii · Medium ssyedhadi.medium.com · Book a slot syedcreates.com/schedule-meeting</p>
<div class="ft"><span>syedcreates.com/brand</span><span>Page 4 of 4</span></div></section>
</body></html>'''
open("/tmp/brandkit.html", "w").write(pdf_html)
js = r'''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file:///tmp/brandkit.html');await p.waitForTimeout(800);await p.pdf({path:process.argv[2],format:'A4',printBackground:true,preferCSSPageSize:true});await b.close();})();'''
open("/tmp/brandkit.js", "w").write(js)
subprocess.run(["node", "/tmp/brandkit.js", os.path.join(ROOT, "downloads/syed-hadi-brand-kit.pdf")], check=True, cwd="/home/claude")
print("brand.html written", len(page), "| pdf", os.path.getsize(os.path.join(ROOT, "downloads/syed-hadi-brand-kit.pdf")))
