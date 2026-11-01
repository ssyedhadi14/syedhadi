#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Generate /adventure, Syed's skydiving, drives and travel essays page (linked from the footer only)
# Owner: Syed Hadi
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import SITE, VER, uns  # noqa: E402

ROOT = "/home/claude/work/site"
shell = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()
nav = re.search(r"<nav>.*?</nav>", shell, re.S).group(0)
foot = re.search(r"<footer class=\"site-foot\">.*?</footer>", shell, re.S).group(0)
icons = re.search(r"<link rel=\"icon\".*?<link[^>]*site\.css[^>]*>", shell, re.S).group(0)
nl = re.search(r'<section class="newsletter.*?</section>', shell, re.S)
nl = nl.group(0) if nl else ""

URL = SITE + "/adventure"
TITLE = "Adventure: Skydiving, Road Trips and Travel Essays by Syed Hadi"
DESC = "Freefall from 13,000 ft over Dubai, a drive from Bengaluru to Ooty, a 100 km walk from Najaf to Karbala, and essays from Iran, Mecca and Medina. The off duty side of Syed Hadi."

VIDEOS = [
    ("AiGx3I4KJDk", "Skydive Dubai", "I fell from 13,000 ft and lived to make this video", "Tandem jump over the Palm, Dubai 2024. Three minutes from the door of the plane to the sand."),
    ("GOSSU2nn_j0", "Road trip", "Drive with me from Bengaluru to Ooty", "Hairpins, tea estates and a windscreen full of mist. November 2024."),
    ("hzioRJt8Sdo", "Karbala", "Al Iraqia News interview from Imam Hussain's shrine", "Two minutes on camera from Karbala, February 2026, at the end of the walk."),
]
ESSAYS = [
    ("https://ssyedhadi.medium.com/skydive-dubai-freefall-from-13-000-ft-f24b4d990926", "1*DypOZwjNUWe5iQUo7pK2Gw@2x.jpeg", "Jun 2025", "Skydive Dubai: Freefall from 13,000 ft", "The fear, the exit, the sixty seconds that felt like six, and what it did to my appetite for risk."),
    ("https://ssyedhadi.medium.com/iran-through-my-eyes-self-discovery-in-2025-0f82409d46b2", "1*DGi5v-HWVUfzTljqToJQJA@2x.jpeg", "Feb 2025", "Iran Through My Eyes: Self Discovery in 2025", "Mashhad, Qom and the long bus rides in between. A country that looks nothing like its headlines."),
    ("https://ssyedhadi.medium.com/my-100kms-walk-journey-in-2023-najaf-to-karbala-25d6b362742d", "1*DXqWPvjylEXbQ6kyh-42aA@2x.jpeg", "Mar 2024", "My 100 km Walk: Najaf to Karbala", "Three days on foot with twenty million others. What the mawkibs taught me about hospitality at scale."),
    ("https://ssyedhadi.medium.com/my-spiritual-journey-to-mecca-in-2024-dcdf97619582", "1*2-H4iwCSxUnFsbdIiBgLlg@2x.jpeg", "Jan 2024", "My Spiritual Journey to Mecca in 2024", "Umrah, step by step, for anyone planning their first visit. Logistics, costs and the moments nobody warns you about."),
    ("https://ssyedhadi.medium.com/why-should-you-know-medina-in-2024-f0a49ad4ed87", "1*h7HkxOBPZozrNm1qqjccgg@2x.jpeg", "Jan 2024", "Why You Should Know Medina in 2024", "The quieter city. History, etiquette and a two day itinerary that leaves room to sit still."),
    ("https://ssyedhadi.medium.com/my-journey-to-heaven-on-earth-najaf-karbala-f9f8f51da55c", "1*9uJe2SoSsan27Hz2rvogGA@2x.jpeg", "Sep 2023", "My Journey to Heaven on Earth: Najaf and Karbala", "The first visit. Getting there from India, where to stay, and what Arbaeen feels like from the inside."),
]
PLACES = ["Dubai", "Ooty", "Najaf", "Karbala", "Mashhad", "Qom", "Mecca", "Medina", "Cairo", "Kochi", "Mumbai", "Bengaluru"]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#person"}, "dateModified": "2026-10-31"},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Adventure", "item": URL}]},
    {"@type": "ItemList", "name": "Adventure videos", "itemListElement": [{"@type": "VideoObject", "position": i + 1, "name": t, "description": d, "thumbnailUrl": f"https://i.ytimg.com/vi/{v}/hqdefault.jpg", "embedUrl": f"https://www.youtube-nocookie.com/embed/{v}", "url": f"https://www.youtube.com/watch?v={v}", "uploadDate": "2024-06-01", "author": {"@id": SITE + "/#person"}} for i, (v, k, t, d) in enumerate(VIDEOS)]},
]}

vids = ""
for v, k, t, d in VIDEOS:
    vids += (f'<article class="yt-card adv-vid reveal"><div class="yt-frame" data-id="{v}" data-title="{t}" role="button" tabindex="0" aria-label="Play: {t}">'
             f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="{t}, video thumbnail" width="480" height="360" loading="lazy" decoding="async">'
             f'<span class="yt-play" aria-hidden="true"><span><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></span></div>'
             f'<div class="yt-body"><small>{k}</small><b>{t}</b><p>{d}</p></div></article>')
essays = ""
for u, img, date, t, d in ESSAYS:
    essays += (f'<a class="adv-essay reveal" href="{u}" target="_blank" rel="noopener"><span class="adv-eimg"><img src="https://miro.medium.com/v2/resize:fill:800:450/{img}" alt="" width="800" height="450" loading="lazy" decoding="async"></span>'
               f'<span class="adv-ebody"><small>{date} &middot; Medium</small><b>{t}</b><p>{d}</p><em>Read the essay &rarr;</em></span></a>')
places = "".join(f"<span>{p}</span>" for p in PLACES)

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
<meta property="og:image" content="{SITE}/img/li/mountain-summit.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1500">
<meta property="og:image:alt" content="Syed Hadi raising a fist on a mountain summit above the clouds">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/img/li/mountain-summit.jpg">
<script type="application/ld+json">{json.dumps(JSONLD, ensure_ascii=False)}</script>
{icons}
<style>
.adv-hero{{position:relative;min-height:78vh;display:grid;align-items:end;color:#fff;overflow:hidden;background:#0d0b1a}}
.adv-hero img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%;opacity:.9}}
.adv-hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,11,26,.15) 0%,rgba(13,11,26,.05) 35%,rgba(13,11,26,.9) 100%)}}
.adv-hero .wrap{{position:relative;z-index:1;padding:120px 0 64px}}
.adv-hero .eyebrow{{color:#c9bfff}}
.adv-hero h1{{font-size:clamp(40px,7vw,96px);line-height:.98;letter-spacing:-.04em;margin:14px 0 18px;max-width:900px}}
.adv-hero p{{font-size:clamp(16px,1.6vw,20px);max-width:620px;color:#e6e1ff}}
.adv-stats{{display:flex;gap:28px;flex-wrap:wrap;margin-top:28px}}
.adv-stats div b{{display:block;font-family:"Bricolage Grotesque";font-size:30px;letter-spacing:-.02em}}
.adv-stats div small{{color:#c9bfff;font-size:13px}}
.adv-grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.adv-vid .yt-body p{{margin:4px 0 0;font-size:13.5px;color:var(--ink-2);line-height:1.5}}
.adv-photos{{display:grid;grid-template-columns:1.2fr .8fr;gap:18px}}
.adv-photo{{position:relative;border-radius:22px;overflow:hidden;background:var(--bg-soft);min-height:320px}}
.adv-photo img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .7s var(--ease)}}
.adv-photo:hover img{{transform:scale(1.03)}}
.adv-photo span{{position:absolute;left:18px;bottom:16px;right:18px;color:#fff;font-weight:700;font-size:15px;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
.adv-photo small{{display:block;font-weight:500;font-size:12.5px;opacity:.85}}
.adv-essays{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.adv-essay{{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--card);text-decoration:none;color:inherit;transition:transform .25s var(--ease),box-shadow .25s var(--ease),border-color .2s}}
.adv-essay:hover{{transform:translateY(-4px);box-shadow:0 18px 40px rgba(28,16,80,.14);border-color:var(--accent)}}
.adv-eimg{{aspect-ratio:16/9;overflow:hidden;background:var(--bg-soft)}}
.adv-eimg img{{width:100%;height:100%;object-fit:cover;display:block}}
.adv-ebody{{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}}
.adv-ebody small{{font:600 11px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}}
.adv-ebody b{{font-size:17px;line-height:1.3}}
.adv-ebody p{{margin:0;font-size:14px;color:var(--ink-2);line-height:1.55;flex:1}}
.adv-ebody em{{font-style:normal;font-weight:700;color:var(--accent);font-size:14px}}
.adv-places{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}
.adv-places span{{padding:8px 14px;border-radius:999px;border:1px solid var(--line);font-weight:600;font-size:14px;background:var(--card)}}
.adv-quote{{text-align:center;max-width:820px;margin:0 auto;padding:40px 0 10px}}
.adv-quote p{{font-family:"Bricolage Grotesque";font-weight:600;font-size:clamp(22px,2.6vw,32px);line-height:1.25;letter-spacing:-.02em}}
.adv-quote cite{{display:block;font-style:normal;margin-top:12px;font:600 12px "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}}
@media (max-width:980px){{.adv-grid3,.adv-essays{{grid-template-columns:1fr 1fr}}.adv-photos{{grid-template-columns:1fr}}}}
@media (max-width:640px){{.adv-grid3,.adv-essays{{grid-template-columns:1fr}}.adv-hero{{min-height:70vh}}}}
</style>
</head>
<body data-page="adventure">
{nav}
<header class="adv-hero">
  <img class="bg" src="/img/li/mountain-summit.jpg" alt="" width="1200" height="1500" fetchpriority="high" decoding="async">
  <div class="wrap">
    <div class="crumbs" style="color:#c9bfff"><a href="/" style="color:#fff">Home</a> / Adventure</div>
    <span class="eyebrow">Off duty</span>
    <h1 class="display">Thirteen thousand feet, long roads and holy cities.</h1>
    <p>The part of me that does not fit on a LinkedIn profile. A tandem jump over Dubai, a drive into the Nilgiris, a hundred kilometres on foot to Karbala, and the essays I wrote on the way back.</p>
    <div class="adv-stats"><div><b>13,000 ft</b><small>Freefall over the Palm, Dubai</small></div><div><b>100 km</b><small>Najaf to Karbala on foot</small></div><div><b>12</b><small>Cities in the essays below</small></div></div>
  </div>
</header>
<main id="main">

<section class="bx-sec" id="watch">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Watch</span><h2 class="display">Three Videos, Three Kinds of Nerve</h2><p>Shot on a phone and a rented GoPro. Tap to play here.</p></div>
    <div class="adv-grid3">{vids}</div>
  </div>
</section>

<section class="bx-sec" style="padding-top:0">
  <div class="wrap">
    <div class="adv-photos">
      <a class="adv-photo reveal" href="https://www.linkedin.com/in/syedhadii/" target="_blank" rel="noopener"><img src="/img/li/egypt-pyramids-flag.jpg" alt="Syed holding the Indian flag in front of the Sphinx and the Great Pyramid in Giza" width="1200" height="1200" loading="lazy" decoding="async"><span>Giza, Egypt<small>AIESEC exchange, 2019. The trip that started all of this.</small></span></a>
      <a class="adv-photo reveal" href="https://www.youtube.com/watch?v=GOSSU2nn_j0" target="_blank" rel="noopener"><img src="{uns('1506905925346-21bda4d32df4', 800, 1000)}" alt="Mist over green hill ranges" width="800" height="1000" loading="lazy" decoding="async"><span>Hill roads<small>Bengaluru to Ooty, 36 hairpin bends, November 2024.</small></span></a>
    </div>
    <div class="adv-quote reveal"><p>"Take the opportunities that scare you. Say yes to the stage even when it makes you nervous. Don't let insecurity make your decisions for you."</p><cite>From the Humans of Marketing feature, 2026</cite></div>
  </div>
</section>

<section class="bx-sec" id="essays">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Read</span><h2 class="display">Travel Essays on Medium</h2><p>Long form from the road. Logistics for anyone planning the same trip, and the parts that stayed with me.</p></div>
    <div class="adv-essays">{essays}</div>
    <div class="adv-places reveal">{places}</div>
    <div class="center" style="margin-top:28px"><a class="btn btn-ghost" href="https://ssyedhadi.medium.com/" target="_blank" rel="noopener">All essays on Medium &rarr;</a> <a class="btn btn-ghost" href="/blog">Back to the GTM writing</a></div>
  </div>
</section>
</main>
{nl}
{foot}
<script src="/assets/common.js?v={VER}"></script>
<script>
(function(){{
  document.querySelectorAll('.yt-frame').forEach(function(f){{
    f.addEventListener('click',function(){{
      var id=f.getAttribute('data-id'); if(!id||f.querySelector('iframe'))return;
      var i=document.createElement('iframe'); i.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0'; i.title=f.getAttribute('data-title')||'YouTube video'; i.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; i.setAttribute('allowfullscreen','');
      f.innerHTML=''; f.appendChild(i);
    }});
  }});
}})();
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "adventure.html"), "w", encoding="utf-8").write(page)
print("adventure.html written", len(page))
