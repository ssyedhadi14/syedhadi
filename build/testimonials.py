#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Trust strip for syedcreates.com. Three arrow controlled testimonials (Nat first, then Ron
#          and Vineel) beside "Built with and featured at" logos in original colour. Replaces the old
#          single quote strip and adds the strip to more business pages. Idempotent.
# Owner: Syed Hadi
import glob
import os
import re

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
CSS_VER_OLD = re.compile(r"site\.css\?v=[0-9a-z]+")
CSS_VER = "site.css?v=20261103m"

LI = ('<svg viewBox="0 0 24 24" width="18" height="18" role="img" aria-hidden="true" focusable="false" shape-rendering="geometricPrecision"><rect x="2" y="2" width="20" height="20" rx="2" fill="#fff"/><path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 4.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>')

QUOTES = [
    {"name": "Nat Natraj", "role": "Cofounder and Chief Client Advocate, AccuKnox", "img": "nat-natraj",
     "li": "https://www.linkedin.com/in/natrajiitb/",
     "q": "Syed is a top flight professional. Combining immense native intellect, great inter-personal skills, "
          "a positive “can do” attitude and immense commitment, Syed delivers incredible results."},
    {"name": "Ron Victor", "role": "Entrepreneur, managed Syed at AccuKnox", "img": "ron-victor", "li": "https://www.linkedin.com/in/ronvictor",
     "q": "Syed has a very pleasant demeanor and is extremely diligent. He is a delight to work with and someone "
          "you want on your team."},
    {"name": "Vineel Kurumella", "role": "Director of GTM and Strategic Partnerships, AccuKnox", "img": "vineel-kurumella", "li": "https://www.linkedin.com/in/vineelkurumella/",
     "q": "If you are looking for someone who gets straight to the point and actually gets things done, Syed is your man."},
]

LOGOS = ('<img src="/img/accuknox-logo.png" alt="AccuKnox" loading="lazy" height="28" width="118">'
         '<img src="/img/cncf-logo.svg" alt="CNCF" loading="lazy" height="28" width="147">'
         '<img src="/img/kubearmor-logo.png" alt="KubeArmor" loading="lazy" height="28" width="151">'
         '<img src="/img/bsides-logo.png" alt="BSides Bangalore" loading="lazy" height="28" width="76">'
         '<img src="/img/growthx-logo.png" alt="GrowthX" loading="lazy" height="28" width="111">'
         '<img src="/img/bits-pilani-logo.png" alt="BITS Pilani" loading="lazy" height="28" width="90">')


def strip():
    slides = []
    for i, q in enumerate(QUOTES):
        li = (f'<a class="tr-li" href="{q["li"]}" target="_blank" rel="noopener" '
              f'aria-label="{q["name"]} on LinkedIn">{LI}</a>') if q["li"] else ""
        slides.append(
            f'<figure class="tr-quote tr-slide{" on" if i == 0 else ""}" data-i="{i}"{"" if i == 0 else " hidden"}>'
            f'<img src="/img/recs/{q["img"]}.jpg" alt="{q["name"]}" width="44" height="44" loading="lazy">'
            f'<blockquote>&ldquo;{q["q"]}&rdquo;<figcaption><b>{q["name"]}</b>{li}<span> &middot; {q["role"]}</span>'
            f'</figcaption></blockquote></figure>')
    n = len(QUOTES)
    return (
        '<div class="tr-strip tr-v2" data-tr>\n'
        '  <div class="tr-car" aria-roledescription="carousel" aria-label="What colleagues say">'
        + "".join(slides) +
        '<div class="tr-ctl"><button type="button" class="tr-btn" data-d="-1" aria-label="Previous testimonial">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>'
        f'<span class="tr-n" aria-live="polite"><b>1</b>/{n}</span>'
        '<button type="button" class="tr-btn" data-d="1" aria-label="Next testimonial">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button>'
        '<a class="tr-all" href="/#recommendations">All recommendations &rarr;</a></div></div>\n'
        f'  <div class="tr-logos"><span>Built with and featured at</span><div>{LOGOS}</div></div>\n'
        '</div>')


JS = """<script data-tr-js>
document.querySelectorAll('[data-tr]').forEach(function(s){
  var sl=s.querySelectorAll('.tr-slide'),n=s.querySelector('.tr-n b'),i=0;
  function go(k){i=(k+sl.length)%sl.length;sl.forEach(function(x,j){x.hidden=j!==i;x.classList.toggle('on',j===i)});n.textContent=i+1}
  s.querySelectorAll('.tr-btn').forEach(function(b){b.addEventListener('click',function(){go(i+ +b.getAttribute('data-d'))})});
  s.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')go(i-1);if(e.key==='ArrowRight')go(i+1)});
});
</script>"""

CSS = """
/* 2026-11-03 trust strip v2: three testimonials, arrows, logos in original colour */
.tr-v2{grid-template-columns:1.15fr 1fr;gap:26px;padding:20px 22px}
.tr-car{min-width:0}
.tr-v2 .tr-quote{min-height:96px;animation:rise .45s var(--ease) both}
.tr-v2 .tr-quote[hidden]{display:none}
.tr-v2 .tr-quote img{width:44px;height:44px}
.tr-v2 .tr-quote blockquote{font-size:15px}
.tr-v2 figcaption{display:flex;flex-wrap:wrap;align-items:center;gap:4px}
.tr-li{display:inline-flex;margin:0 2px 0 4px;border-radius:4px;transition:transform .2s}
.tr-li:hover{transform:translateY(-1px)}
.tr-ctl{display:flex;align-items:center;gap:10px;margin:12px 0 0 56px}
.tr-btn{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);display:grid;place-items:center;cursor:pointer;transition:border-color .2s,color .2s}
.tr-btn:hover{border-color:var(--accent);color:var(--accent)}
.tr-n{font:600 12.5px "JetBrains Mono",monospace;color:var(--ink-3);min-width:34px;text-align:center}
.tr-n b{color:var(--ink)}
.tr-all{margin-left:auto;font-size:13px;font-weight:600;color:var(--accent);text-decoration:none}
.tr-v2 .tr-logos div{gap:10px}
.tr-v2 .tr-logos img,:root[data-theme="dark"] .tr-v2 .tr-logos img{filter:none;opacity:1;height:38px;width:auto;padding:7px 10px;background:#fff;border-radius:10px;border:1px solid #e7e4f3;box-sizing:border-box}
.tr-sec{padding:8px 0 48px}
.tr-sec .tr-strip{margin-top:0}
@media (max-width:960px){.tr-v2{grid-template-columns:1fr}.tr-ctl{margin-left:0}}
"""

# Pages that gain the strip (business pages without it), placed just before </main>
ADD = [
    "about", "blog", "insights", "writing", "case-studies", "growth-in-a-box", "work", "portfolio", "gtm-engine",
    "systems", "recognition", "events", "playbook", "tools", "posts", "jobs", "schedule-meeting", "referral-partners",
    "skill-pack", "seo-aeo-score", "company-research", "calculator", "salary-calculator", "pmm-salary-2026",
    "fractional-pmm-india", "fractional-pmm-vs-agency-vs-full-time-hire", "best-gtm-consultants-for-security-startups",
    "how-to-build-a-saas-partner-program", "30-day-shadow-ai-discovery-sprint", "5-years-of-startup-life",
    "ai-soc-tool-evaluation-regulated", "ai-spm-7-runtime-security-questions", "aspm-evaluation-cutting-false-positives",
    "cert-in-evidence-pipeline-hybrid-cloud", "cnapp-comparison-checklist-with-scoring",
    "cnapp-cspm-cwpp-explained-for-buyers", "mcp-ai-agent-threat-model", "runtime-cnapp-vs-agentless-cnapp",
    "stateful-prompt-firewall", "software-careers-for-students",
]

OLD = re.compile(r'<div class="tr-strip">.*?</figure>\s*<div class="tr-logos">.*?</div></div>\s*</div>', re.S)


def main():
    css_path = os.path.join(SITE_DIR, "assets", "site.css")
    if ".tr-v2{" not in open(css_path, encoding="utf-8").read():
        open(css_path, "a", encoding="utf-8").write(CSS)
    s = strip()
    changed = 0
    for p in sorted(glob.glob(os.path.join(SITE_DIR, "*.html"))):
        slug = os.path.basename(p)[:-5]
        h = open(p, encoding="utf-8").read()
        orig = h
        h = OLD.sub(lambda _m: s, h)
        h = re.sub(r'<div class="tr-strip tr-v2" data-tr>.*?\n</div>', lambda _m: s, h, flags=re.S)  # refresh on rerun
        if slug in ADD and "data-tr>" not in h:
            h = h.replace("</main>", f'<section class="tr-sec" aria-label="What colleagues say"><div class="wrap">{s}</div></section>\n</main>', 1)
        if "data-tr>" in h and "data-tr-js" not in h:
            h = h.replace("</main>", JS + "\n</main>", 1)
        if h != orig:
            h = CSS_VER_OLD.sub(CSS_VER, h)
            open(p, "w", encoding="utf-8").write(h)
            changed += 1
    print(f"pages changed: {changed}")


if __name__ == "__main__":
    main()
