#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Add real photography (from Syed's LinkedIn posts) to /recognition: hero strip, moments gallery, new BSides photo
# Owner: Syed Hadi
import re

p = "/home/claude/work/site/recognition.html"
h = open(p, encoding="utf-8").read()

MOMENTS = [
    ("li/bsides-2025-startup-of-the-year.jpg", "2025", "Startup of the Year", "Holding the BSides Bangalore award for AccuKnox, the first of two.", "Security BSides Bangalore"),
    ("li/india-devsec-show-2025.jpg", "12 SEP 2025", "In the spotlight at India DevSec Show", "Recognised on stage, with AccuKnox as the featured vendor of the day.", "Bengaluru"),
    ("li/kubecon-india-mumbai-2026.jpg", "JUN 2026", "Team AccuKnox at KubeCon India", "Six years into Kubernetes security, now on the biggest cloud native stage in the country.", "Mumbai"),
    ("li/cncf-netapp-bengaluru-2026.jpg", "27 AUG 2026", "Hosting the CNCF community day", "A full house at NetApp Bengaluru for an open source day run with the community.", "NetApp, Bengaluru"),
    ("li/gtm-deep-dive-growthx-2026.jpg", "3 OCT 2026", "GTM Deep Dive with GrowthX", "Less theory, more simulation. Teams made real go to market calls under time pressure.", "GrowthX, Bengaluru"),
    ("li/gisec-dubai-2024.jpg", "APR 2024", "GISEC Global", "A week on the AccuKnox booth in Dubai: demos, partners and the first MENA pipeline.", "Dubai"),
    ("li/four-years-accuknox.jpg", "2025", "Four years at AccuKnox", "From project management to leading product marketing and partnerships.", "AccuKnox"),
    ("li/kcd-kochi-2024.jpg", "3 FEB 2024", "The first KCD in Kerala", "Kubernetes Community Days, Kochi. Meeting the people who run the clusters.", "Kochi"),
    ("li/scrum-alliance-csm.jpg", "OCT 2022", "Certified Scrum Product Owner", "CSM in July, CSPO in October. The operating habits behind every launch since.", "Scrum Alliance"),
    ("li/future-of-gtm-2026-event.jpg", "2025", "Future of GTM in 2026", "The room where five times marketing growth got explained in one word: execution.", "Bengaluru"),
    ("li/engineering-team-meet.jpg", "2025", "With the engineering team", "If you want to go far, go together. WeWork Chennai with the people who build the product.", "Chennai"),
    ("li/linkedin-trending.jpg", "2020", "First post to trend on LinkedIn", "Where the writing habit started: 1,816 views, 64 reactions, one very surprised author.", "LinkedIn"),
]

shots = ""
for img, date, title, text, where in MOMENTS:
    shots += (f'<div class="shot reveal"><div class="ph"><img src="/img/{img}" alt="{title}" loading="lazy" decoding="async" width="1200" height="750"></div>'
              f'<div class="body"><span class="date-tag">{date}</span><h3>{title}</h3><p>{text}</p><span class="where">{where}</span></div></div>')
section = f'''<section class="block rec-moments" id="moments">
  <div class="wrap">
    <div class="block-head reveal"><div><span class="eyebrow">Captured moments</span><h2 class="display" style="margin-top:8px">Rooms, stages and the odd trophy</h2></div><p>Twelve photos from the LinkedIn feed, one line each.</p></div>
    <div class="gallery rec-gallery">{shots}</div>
  </div>
</section>
'''
h = re.sub(r'<section class="block rec-moments".*?</section>\n', "", h, flags=re.S)
# place before the BSides block (the last .block section)
blocks = [m.start() for m in re.finditer(r'<section class="block">', h)]
h = h[:blocks[-1]] + section + h[blocks[-1]:]
# BSides wide shot: use the new award photo instead of the homepage one
h = h.replace('<img src="img/bsides-2026.jpg" alt="Team AccuKnox with the BSides Bangalore award at the booth"', '<img src="/img/li/bsides-2026-startup-award.jpg" alt="Team AccuKnox with the BSides 2026 #1 Startup award at the booth"')
# hero photo strip under the page hero
strip = '''<div class="rec-strip" aria-hidden="true"><img src="/img/li/bsides-2025-startup-of-the-year.jpg" alt="" loading="lazy"><img src="/img/li/india-devsec-show-2025.jpg" alt="" loading="lazy"><img src="/img/li/gisec-dubai-2024.jpg" alt="" loading="lazy"><img src="/img/li/kubecon-india-mumbai-2026.jpg" alt="" loading="lazy"><img src="/img/li/cncf-netapp-bengaluru-2026.jpg" alt="" loading="lazy"></div>
'''
if 'rec-strip' not in h:
    h = h.replace('<main id="main">', '<main id="main">\n' + strip, 1)
open(p, "w", encoding="utf-8").write(h)
print("recognition: strip + 12 moments")
