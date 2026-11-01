#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Homepage content changes for syedcreates.com (Medium section out, featured strip under hero, wins with photos above footer, inline internal links)
# Owner: Syed Hadi
import re

P = "/home/claude/work/site/index.html"
h = open(P, encoding="utf-8").read()
done = []


def rep(old, new, count=1, label=None):
    global h
    n = h.count(old)
    assert n >= 1, f"not found: {label or old[:70]}"
    if count == 1:
        assert n == 1, f"ambiguous ({n}): {label or old[:70]}"
    h = h.replace(old, new) if count != 1 else h.replace(old, new, 1)
    done.append(label or old[:50])


# 1. Remove the "Latest on Medium" section and its scripts
m = re.search(r'<section id="writing"[^>]*>.*?</section>\s*', h, re.S)
assert m, "writing section"
h = h[:m.start()] + h[m.end():]
h = re.sub(r'<script src="assets/medium-archive\.js[^"]*"></script>\s*', "", h)
h = re.sub(r'<script src="assets/medium\.js[^"]*"></script>\s*', "", h)
done.append("medium section removed")

# 2. Move "I'm Featured on" strip right under the hero
m = re.search(r'<div class="logos feat" id="featured">.*?</div>\s*</div>\s*</div>\s*\n\s*</div>\s*\n\s*</section>', h, re.S)
assert m, "featured block"
block = m.group(0)
# block ends with the closing of about-grid wrap and section; isolate the feat div only
feat_end = block.rfind('</div>\n')  # last closing of the feat div before wrap/section closers
feat_html = re.search(r'<div class="logos feat" id="featured">.*?</div>\s*</div>\s*</div>', block, re.S).group(0)
h = h.replace(feat_html, "", 1)
feat_section = ('<section class="feat-sec" aria-labelledby="feat-title">\n  <div class="wrap">\n    ' +
                feat_html.replace('<h3 class="feat-title">', '<h2 class="feat-title" id="feat-title">').replace("</h3>", "</h2>", 1) +
                "\n  </div>\n</section>\n")
rep("</header>\n", "</header>\n" + feat_section, label="featured under hero")

# 3. Remove the $35B TAM stat and the TAM line in the work grid
rep('<div class="stat"><b>$35B</b><span>TAM across partner programs</span></div>',
    '<div class="stat"><b>7</b><span>Regions with live partner programs</span></div>', label="35B stat")
rep("Partner programs across AI and cloud security sectors covering over $35B in annual TAM.",
    'Partner programs live across India, MENA, APAC, Japan, Europe, Africa and the US. <a href="/partner-revenue-case-study">Read the partner story &rarr;</a>', label="35B shipped line")

# 4. Inline internal links across the page
rep("<p class=\"lede\">I turn security products into pipeline. Product marketing, channel partnerships and go to market for AI and cloud security, built at AccuKnox since day one.</p>",
    "<p class=\"lede\">I turn security products into pipeline. <a href=\"/pmm-case-study\">Product marketing</a>, <a href=\"/partner-revenue-case-study\">channel partnerships</a> and <a href=\"/gtm-case-study\">go to market</a> for AI and cloud security, built at AccuKnox since day one. See the <a href=\"/case-studies\">case studies</a> or try the free <a href=\"/salary-calculator\">salary growth calculator</a>.</p>", label="hero lede links")
rep('<a href="https://syedcreates.com" target="_blank" rel="noopener" aria-label="Website">',
    '<a href="/blog" aria-label="Blog">', label="hero self link -> blog")
rep("<p>I wake up excited to solve growth problems. I lead the motions that drive acquisition, onboarding, engagement, retention and monetisation, and I build lead pipeline that compounds into ARR. Except for writing production code, I have had my hands in everything across marketing, product, sales and partnerships.</p>",
    "<p>I wake up excited to solve growth problems. I lead the motions that drive <a href=\"/playbook\">acquisition, onboarding, engagement, retention and monetisation</a>, and I build <a href=\"/gtm-engine\">lead pipeline that compounds into ARR</a>. Except for writing production code, I have had my hands in everything across <a href=\"/pmm-case-study\">marketing</a>, <a href=\"/systems\">product</a>, sales and <a href=\"/partner-revenue-case-study\">partnerships</a>.</p>", label="about links")
rep("<p>Seven years across SaaS, open source and community, six of them building AccuKnox. Pick a role to open it.</p>",
    "<p>Seven years across SaaS, <a href=\"/events\">open source and community</a>, six of them building AccuKnox. Pick a role to open it, or read the <a href=\"/about\">full story on the about page</a>.</p>", label="exp links")
rep("<p>Every capability below carries a line from work that already shipped.</p>",
    "<p>Every capability below carries a line from work that already shipped. Each one is also a <a href=\"/gtm-pmm-in-a-box\">90 day box</a> you can hire.</p>", label="work head link")
rep("First product marketer at AccuKnox, part of the team that grew ARR from $500K to $1M+.</div>",
    "First product marketer at AccuKnox, part of the team that grew ARR from $500K to $1M+. <a href=\"/pmm-case-study\">Read the PMM case study &rarr;</a></div>", label="svc1")
rep("GTM for new product lines that drove a sharp rise in inbound leads.</div>",
    "GTM for new product lines that drove a sharp rise in inbound leads. <a href=\"/gtm-case-study\">Read the GTM case study &rarr;</a></div>", label="svc3")
rep("$2M influenced pipeline on $100K of annual marketing spend.</div>",
    "$2M influenced pipeline on $100K of annual marketing spend. <a href=\"/gtm-engine\">See the GTM engine &rarr;</a></div>", label="svc4")
rep("KubeArmor community growth with 1.4K+ GitHub stars from a single booth push.</div>",
    "KubeArmor community growth with 1.4K+ GitHub stars from a single booth push. <a href=\"/events\">See the events &rarr;</a></div>", label="svc5")
rep("Worked on the v1.0 GA release of the AccuKnox SaaS platform.</div>",
    "Worked on the v1.0 GA release of the AccuKnox SaaS platform. <a href=\"/systems\">See the systems &rarr;</a></div>", label="svc6")
rep("<blockquote style=\"margin-top:20px\">B2B marketing does not have to feel boring. <span>Make it human,</span> build real relationships, and show instead of tell.</blockquote>",
    "<blockquote style=\"margin-top:20px\">B2B marketing does not have to feel boring. <span>Make it human,</span> build real relationships, and <a href=\"/case-studies\">show instead of tell</a>.</blockquote>", label="belief link")
rep("<p class=\"who\">Servant leader. I create value, support the community, and help people grow.</p>",
    "<p class=\"who\">Servant leader. I create value, <a href=\"/events\">support the community</a>, and <a href=\"/jobs\">help people grow</a>. The <a href=\"/playbook\">playbook</a> and <a href=\"/writing\">essays</a> show how.</p>", label="who links")
rep("<p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls.</p>\n<div class=\"btns\">\n<a class=\"btn btn-primary\" href=\"/schedule-meeting\">Schedule meeting</a>\n<a class=\"btn btn-ghost\" href=\"#book\">Pick a Time Below</a>",
    "<p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls. Not ready to talk? Run the <a href=\"/gtm-health-check\">2 minute GTM health check</a> or the <a href=\"/ai-visibility-checker\">AI visibility checker</a> first.</p>\n<div class=\"btns\">\n<a class=\"btn btn-primary\" href=\"/schedule-meeting\">Schedule meeting</a>\n<a class=\"btn btn-ghost\" href=\"#book\">Pick a Time Below</a>", label="cta links") if "Pick a Time Below</a>" in h and "<p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls.</p>\n<div class=\"btns\">" in h else None
if "2 minute GTM health check" not in h:
    rep("<p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls.</p>",
        "<p>The best innovations start with a conversation. Tell me what you are building and where the pipeline stalls. Not ready to talk? Run the <a href=\"/gtm-health-check\">2 minute GTM health check</a> or the <a href=\"/ai-visibility-checker\">AI visibility checker</a> first.</p>", count=2, label="cta links (2 places)")
rep("<p>Share your site and the one thing that is not working. I record a short Loom walkthrough with the three changes I would make first. No call needed.</p>",
    "<p>Share your site and the one thing that is not working. I record a short Loom walkthrough with the three changes I would make first. No call needed. Want the full program instead? That is <a href=\"/aeo-seo-in-a-box\">AEO/SEO Ranking in a box</a>.</p>", label="audit link")
rep("<p>No pitch decks. Tell me what you are building and where the pipeline stalls.</p>",
    "<p>No pitch decks. Tell me what you are building and where the pipeline stalls. Prefer email? The <a href=\"/schedule-meeting\">schedule page</a> has every way to reach me.</p>", label="book link")
rep("<a href='/pmm-salary-2026'>PMM Salary 2026</a></div>",
    '<a href="/pmm-salary-2026">PMM Salary 2026</a><a href="/salary-calculator">Salary Growth Calculator</a><a href="/fire-calculator">FIRE Calculator</a><a href="/skill-pack">Claude Skill Pack</a></div>', label="proof strip links")

# 5. Wins section: photos on each card, move above the footer area (before proof strip)
m = re.search(r'<section style="padding-top:0">\s*<div class="wrap">\s*<div class="sec-head reveal">\s*<span class="eyebrow">On the record</span>.*?</section>\n', h, re.S)
assert m, "wins section"
wins = m.group(0)
h = h[:m.start()] + h[m.end():]
wins = wins.replace('<section style="padding-top:0">', '<section class="wins-sec" id="wins" style="padding-top:0">', 1)
wins = wins.replace('<h2 class="display">Wins Worth Counting</h2>',
                    '<h2 class="display">Wins Worth Counting</h2>\n      <p>Moments from the LinkedIn featured section, with the number behind each one. More on the <a href="/recognition">recognition page</a>.</p>')
cards = {
    '<div class="win reveal"><b>#1</b><h4>Startup Award, BSides 2025</h4><p>Security BSides Bangalore annual cybersecurity conference.</p></div>':
    '<a class="win has-img reveal" href="/recognition"><span class="win-img logo"><img src="img/bsides-logo.png" alt="Security BSides Bangalore logo" width="320" height="110" loading="lazy" decoding="async"></span><span class="win-txt"><b>#1</b><h3>Startup Award, BSides 2025</h3><p>Security BSides Bangalore annual cybersecurity conference.</p></span></a>',
    '<div class="win reveal"><b>#1</b><h4>Startup Award, BSides 2026</h4><p>Back to back. The hattrick target is 2027.</p></div>':
    '<a class="win has-img reveal" href="/recognition"><span class="win-img"><img src="img/bsides-2026.jpg" alt="Syed Hadi receiving the Startup Award at Security BSides Bangalore 2026 with partners on the AccuKnox booth" width="1200" height="750" loading="lazy" decoding="async"></span><span class="win-txt"><b>#1</b><h3>Startup Award, BSides 2026</h3><p>Back to back. The hattrick target is 2027.</p></span></a>',
    '<div class="win reveal"><b>5x</b><h4>Marketing growth</h4><p>Attribution with Factors.ai and SEO plus AEO with TripleDart.</p></div>':
    '<a class="win has-img reveal" href="/gtm-engine"><span class="win-img"><img src="img/journey/prodm-se-workweek-2024.jpg" alt="The AccuKnox product marketing and solutions engineering team during the 2024 work week" width="1100" height="618" loading="lazy" decoding="async"></span><span class="win-txt"><b>5x</b><h3>Marketing growth</h3><p>Attribution with Factors.ai and SEO plus AEO with TripleDart.</p></span></a>',
    '<div class="win reveal"><b>MBA</b><h4>BITS Pilani, 2024 to 2026</h4><p>Completed alongside a full time growth role.</p></div>':
    '<a class="win has-img reveal" href="/about#credentials"><span class="win-img logo"><img src="img/bits-crest.png" alt="BITS Pilani crest" width="160" height="176" loading="lazy" decoding="async"></span><span class="win-txt"><b>MBA</b><h3>BITS Pilani, 2024 to 2026</h3><p>Completed alongside a full time growth role.</p></span></a>',
}
for old, new in cards.items():
    assert old in wins, old[:60]
    wins = wins.replace(old, new)
rep('<div class="proof-strip">', wins + '<div class="proof-strip">', label="wins above footer area")

open(P, "w", encoding="utf-8").write(h)
print("home edits:", len(done))
for d in done:
    print(" -", d)
