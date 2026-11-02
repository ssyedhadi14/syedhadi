#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Homepage Humans of Marketing feature + carousel logo, and /blog tool cards (moved out of the footer Resources column)
# Owner: Syed Hadi
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import uns  # noqa: E402

ROOT = "/home/claude/work/site"
HOM_ID = "7511289811559862272"
HOM_URL = f"https://www.linkedin.com/feed/update/urn:li:activity:{HOM_ID}/"
HOM_EMBED = f"https://www.linkedin.com/embed/feed/update/urn:li:activity:{HOM_ID}?collapsed=1"

# ---------------- homepage ----------------
p = os.path.join(ROOT, "index.html")
h = open(p, encoding="utf-8").read()
hom = f'''<div class="hom-feat reveal">
      <div class="hom-card">
        <div class="hom-head"><img src="img/humans-of-marketing-logo.png" alt="Humans of Marketing" width="44" height="44" loading="lazy" decoding="async"><div><span class="eyebrow">Featured by Humans of Marketing</span><b>The humans who make marketing extraordinary</b></div></div>
        <blockquote>B2B marketing does not have to feel boring. The future is about making B2B more human, building genuine relationships, creating strong distribution ecosystems, and communicating with people.</blockquote>
        <p>Humans of Marketing, the LinkedIn community that profiles the people behind the campaigns, featured my story: from AIESEC and scouting in 2019 to joining AccuKnox in January 2021, moving into partnerships and marketing, and leading a team of seven marketers with a $100,000 annual budget across events and performance marketing.</p>
        <div class="hom-acts"><a class="btn btn-primary" href="{HOM_URL}" target="_blank" rel="noopener">Read the feature on LinkedIn &rarr;</a><a class="btn btn-ghost" href="/recognition">All recognition</a></div>
      </div>
      <a class="hom-photo reveal" href="{HOM_URL}" target="_blank" rel="noopener"><img src="img/li/humans-of-marketing-feature.jpg" alt="Syed Hadi, portrait used in the Humans of Marketing feature" width="800" height="1422" loading="lazy" decoding="async"><span><b>Humans of Marketing, October 2026</b>Beyond campaigns and metrics, the humans who make marketing extraordinary.</span></a>
    </div>
    <div class="sec-head reveal" style="margin-top:56px">
      <span class="eyebrow">Watch</span>
      <h2 class="display" style="font-size:clamp(26px,3.4vw,40px)">Everybody Uses AI. Who Secures It?</h2>
      <p>Forty one seconds on why AI security has to enforce at runtime, not just report.</p>
    </div>
    '''
if 'class="hom-feat' not in h:
    # replace the Watch section head with the feature + a smaller watch head
    old_head = re.search(r'<section class="vid-sec" id="video">\s*<div class="wrap">\s*<div class="sec-head reveal">\s*<span class="eyebrow">Watch</span>.*?</div>\s*(?=<div class="vid-frame)', h, re.S).group(0)
    new_head = '''<section class="vid-sec" id="video">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Featured</span>
      <h2 class="display">Humans of Marketing, and a Word on AI</h2>
      <p>A community feature on the human side of B2B marketing, then forty one seconds on securing AI at runtime.</p>
    </div>
    ''' + hom
    h = h.replace(old_head, new_head, 1)
# carousel logo: insert after GrowthX chip
logo = '<span class="lg mark hom-mark"><img src="img/humans-of-marketing-logo.png" alt="" height="26" width="26"><b>Humans of Marketing</b></span>'
if "hom-mark" not in h:
    h = h.replace('<span class="lg lchip"><img src="img/growthx-logo.png" alt="GrowthX" height="24" width="95"></span>', '<span class="lg lchip"><img src="img/growthx-logo.png" alt="GrowthX" height="24" width="95"></span>' + logo, 1)
    assert "hom-mark" in h, "carousel insert failed"
open(p, "w", encoding="utf-8").write(h)
print("home: Humans of Marketing feature + logo")

# ---------------- blog cards ----------------
p = os.path.join(ROOT, "blog.html")
b = open(p, encoding="utf-8").read()
b = re.sub(r'<section class="bf-sec bf-tools">.*?</section>\s*', '', b, flags=re.S)
TOOLS = [
    ("/seo-aeo-score", "Free tool", "SEO and AEO Score", "Paste a URL and get an SEO score, an AEO score for AI answer engines, Domain Rating and a prioritised fix list."),
    ("/bmi-calculator", "Calculator", "BMI and Healthy Habits", "BMI on Indian cut offs, healthy weight for your height, optional BP, sugar and SGPT checks, a start and stop doing plan and a 7 day habits tracker."),
    ("/car-mileage-calculator", "Calculator", "Car Mileage and Running Cost", "Litres per month, fuel cost in your city versus others, cost per km, tank range and a yearly number with service. Pre filled for a Fronx."),
    ("/loan-calculator", "Calculator", "Loan EMI and Prepay Planner", "Home, car or personal loan EMI, three ways to close it in half the time, and prepay versus invest with tax breaks."),
    ("/pmm-salary-2026", "Guide", "India PMM Salary 2026", "Benchmarks by title, experience and city from 3,300 public salaries, a calculator and the full PDF guide."),
    ("/fire-calculator", "Calculator", "FIRE Calculator India", "Your FIRE number, the SIP you need, your earliest retirement age and a PDF plan."),
    ("/mutual-fund-returns-calculator", "Calculator", "Mutual Fund Returns", "Real 1 to 20 year returns of 50 Indian funds with a SIP and lumpsum projector."),
    ("/qums", "Calculator", "Qums Calculator", "Shia Qums (Khums) in three steps, with Sahm e Imam and Sahm e Sadat worked out and a PDF summary."),
    ("/ai-visibility-checker", "Scorecard", "AI Visibility Checker", "Ten questions on whether ChatGPT, Gemini and Perplexity can find and cite your company."),
    ("/gtm-health-check", "Scorecard", "GTM Health Check", "Score your ICP, motion, message and pipeline discipline in five minutes."),
    ("/salary-calculator", "Calculator", "Salary Growth Calculator", "Your salary, savings and corpus for the next 45 years, with a PDF report in your inbox."),
]
cards = "".join(f"<a class='bf-card reveal' href='{h_}'><small>{tag}</small><b>{t}</b><span>{d}</span><em>Open &rarr;</em></a>" for h_, tag, t, d in TOOLS)
sec = f'''<section class="bf-sec bf-tools" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Free tools and calculators</span><h2 class="display">Tools Worth Bookmarking</h2><p>Scorecards for the marketing and calculators for the money. Each one runs in your browser and most give you a PDF to keep.</p></div>
    <div class="bf-grid">{cards}</div>
  </div>
</section>
'''
anchor = '<section style="padding-top:36px">'
assert anchor in b
b = b.replace(anchor, sec + anchor, 1)
open(p, "w", encoding="utf-8").write(b)
print("blog: tool cards")
