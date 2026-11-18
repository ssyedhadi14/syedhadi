# Created by: Claude Cowork
# Date: 2026-11-18
# Purpose: Build two interview PDFs for /downloads from content already on
#          /interview-prep (question bank, interview loop, offer advice):
#            site/downloads/interview-questions-and-answers.pdf
#            site/downloads/interview-loop-and-offer-playbook.pdf
# Owner: Syed Hadi
# Usage: python3 build/interview_pdfs.py
import json
import re
import subprocess
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "downloads"
TMP = Path("/tmp/ipdf"); TMP.mkdir(exist_ok=True)
F = f"file://{SITE}/assets/fonts/web"

ROLES = [("pmm", "Product marketing"), ("partnerships", "Partnerships"), ("sales", "Sales")]

CSS = f"""
@font-face{{font-family:PJ;font-weight:800;src:url({F}/plus-jakarta-sans-latin-800-normal.woff2)}}
@font-face{{font-family:PJ;font-weight:700;src:url({F}/plus-jakarta-sans-latin-700-normal.woff2)}}
@font-face{{font-family:IN;font-weight:400;src:url({F}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:IN;font-weight:600;src:url({F}/inter-latin-600-normal.woff2)}}
@font-face{{font-family:IS;font-style:italic;src:url({F}/instrument-serif-latin-400-italic.woff2)}}
@font-face{{font-family:JB;font-weight:500;src:url({F}/jetbrains-mono-latin-500-normal.woff2)}}
@page{{size:A4;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font:400 9.6pt/1.5 IN,sans-serif;color:#2b2840;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;padding:18mm 17mm 20mm;break-after:page;background:#fff}}
.page:last-child{{break-after:auto}}
.cover{{background:linear-gradient(150deg,#140d3a 0%,#2c1c8a 55%,#5b3df5 100%);color:#fff;padding:22mm 18mm}}
.cover:before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:12mm 12mm}}
.cover .in{{position:relative}}
.kick{{font:500 8pt JB,monospace;letter-spacing:.2em;text-transform:uppercase;color:#ffd84d}}
.cover h1{{font:800 44pt/1.02 PJ,sans-serif;letter-spacing:-.035em;margin-top:8mm}}
.cover h1 em{{font-family:IS;font-style:italic;font-weight:400;font-size:1.12em;color:#c4b5fd}}
.cover .sub{{margin-top:7mm;font-size:12.5pt;line-height:1.5;color:#ddd6fe;max-width:140mm}}
.chips{{display:flex;gap:3mm;flex-wrap:wrap;margin-top:9mm}}
.chips span{{font:600 9pt IN;border:1px solid rgba(255,255,255,.35);border-radius:20mm;padding:1.6mm 4mm}}
.toc{{position:absolute;left:18mm;right:18mm;bottom:40mm;display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}}
.toc div{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);border-radius:4mm;padding:5mm}}
.toc b{{display:block;font:800 26pt PJ;color:#ffd84d;letter-spacing:-.03em}}
.toc span{{font-size:9.5pt;color:#ede9fe}}
.by{{position:absolute;left:18mm;bottom:16mm;display:flex;align-items:center;gap:3.5mm;font:700 10pt PJ}}
.by img{{width:11mm;height:11mm;border-radius:50%;border:2px solid #fff;object-fit:cover}}
.by small{{display:block;font:400 8.5pt IN;color:#c4b5fd}}
.ph{{display:flex;align-items:baseline;justify-content:space-between;border-bottom:2px solid #141228;padding-bottom:3mm;margin-bottom:6mm}}
.ph h2{{font:800 20pt PJ;letter-spacing:-.03em;color:#141228}}
.ph h2 em{{font-family:IS;font-style:italic;font-weight:400;font-size:1.15em;color:#5b3df5}}
.ph span{{font:500 8pt JB,monospace;letter-spacing:.14em;text-transform:uppercase;color:#5b3df5}}
.q{{display:grid;grid-template-columns:11mm 1fr;gap:3mm;padding:3.6mm 0;border-bottom:1px solid #e7e3f7;break-inside:avoid}}
.q:last-child{{border-bottom:0}}
.q .n{{font:800 17pt PJ;color:#c4b5fd;letter-spacing:-.03em;line-height:1}}
.q h3{{font:700 11pt/1.35 PJ;color:#141228;letter-spacing:-.01em}}
.q .t{{margin-top:1.6mm;font-size:8.8pt;color:#6b6585}}
.q .t b{{color:#5b3df5;font-weight:600}}
.q .a{{margin-top:1.6mm;background:#f6f3ff;border-left:3px solid #5b3df5;border-radius:0 2mm 2mm 0;padding:2.2mm 3mm;font-size:9.1pt}}
.q .a b{{color:#141228}}
.foot{{position:absolute;left:17mm;right:17mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.8pt;color:#8a84a3;border-top:1px solid #e7e3f7;padding-top:2.5mm}}
.foot b{{color:#5b3df5}}
.rounds{{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm}}
.rd{{border:1.5px solid #141228;border-radius:4mm;padding:5mm;box-shadow:2.2mm 2.2mm 0 #141228;background:#fff;break-inside:avoid}}
.rd small{{font:500 7.6pt JB,monospace;letter-spacing:.16em;color:#5b3df5}}
.rd h3{{font:800 14pt PJ;color:#141228;margin-top:1.5mm;letter-spacing:-.02em}}
.rd .dur{{display:inline-block;margin-top:2mm;font:600 8pt IN;background:#ffd84d;border:1px solid #141228;border-radius:1.5mm;padding:.6mm 2mm}}
.rd p{{margin-top:2.5mm;font-size:9.4pt}}
.lede{{font-size:10.5pt;color:#55506d;margin:-2mm 0 6mm;max-width:160mm}}
.tips{{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm}}
.tip{{background:#f6f3ff;border-radius:4mm;padding:5mm;break-inside:avoid}}
.tip h3{{font:800 12.5pt PJ;color:#141228;letter-spacing:-.015em}}
.tip p{{margin-top:2mm;font-size:9.4pt}}
.cta{{margin-top:7mm;background:#141228;color:#fff;border-radius:4mm;padding:6mm 7mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}}
.cta b{{font:800 13pt PJ}}
.cta span{{font-size:9.2pt;color:#c4b5fd;display:block;margin-top:1mm}}
.cta i{{font-style:normal;font:700 10pt PJ;background:#ffd84d;color:#141228;border-radius:2.5mm;padding:2.6mm 4.5mm;white-space:nowrap}}
"""


def page_html(pages, title):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'


def foot(n, label):
    return f'<div class="foot"><span>{label} &middot; <b>syedcreates.com/interview-prep</b></span><span>{n:02d}</span></div>'


def cover(kick, title, accent, sub, chips, toc):
    chip = "".join(f"<span>{c}</span>" for c in chips)
    t = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in toc)
    return (f'<section class="page cover"><div class="in"><div class="kick">{kick}</div>'
            f'<h1>{title} <em>{accent}</em></h1><p class="sub">{sub}</p><div class="chips">{chip}</div></div>'
            f'<div class="toc">{t}</div>'
            f'<div class="by"><img src="file://{SITE}/img/avatar.jpg"><div>Syed Hadi<small>GTM, Growth, Strategy and RevOps &middot; syedcreates.com</small></div></div></section>')


def bank():
    h = (SITE / "interview-prep.html").read_text(encoding="utf-8")
    i = h.find("IP_BANK=") + len("IP_BANK=")
    data, _ = json.JSONDecoder().raw_decode(h[i:])
    return data


def build_questions():
    data = bank()
    pages = [cover("Interview prep &middot; 2026 edition", "30 interview questions,", "answered",
                   "The questions you will actually get for product marketing, partnerships and sales roles in B2B SaaS, what each one is really testing, and how to answer it.",
                   ["10 per role", "What they test", "How to answer"],
                   [("10", "Product marketing"), ("10", "Partnerships"), ("10", "Sales")])]
    n, num = 2, 0
    for key, label in ROLES:
        qs = data.get(key, [])
        for part_no, half in ((1, qs[:5]), (2, qs[5:10])):
            if not half:
                continue
            items = ""
            for q in half:
                num += 1
                items += (f'<div class="q"><div class="n">{num:02d}</div><div><h3>{escape(unescape(q["q"]))}</h3>'
                          f'<p class="t"><b>What they test.</b> {escape(unescape(q["t"]))}</p>'
                          f'<p class="a"><b>How to answer.</b> {escape(unescape(q["a"]))}</p></div></div>')
            part = f"part {part_no}"
            pages.append(f'<section class="page"><div class="ph"><h2>{label} <em>questions</em></h2><span>{part}</span></div>{items}{foot(n, "30 interview questions, answered")}</section>')
            n += 1
    # practice CTA on the last page
    pages[-1] = pages[-1].replace('<div class="foot">', '<div class="cta"><div><b>Practise these out loud</b><span>The free AI interview coach on syedcreates.com asks follow ups and scores your answers.</span></div><i>syedcreates.com/interview-prep</i></div><div class="foot">', 1)
    return page_html(pages, "30 Interview Questions, Answered")


ROUNDS = [
    ("01", "Recruiter screen", "20 to 30 min", "Fit, notice period, CTC range, why you. Have a 90 second intro and your numbers ready."),
    ("02", "Hiring manager", "45 to 60 min", "Your best two or three stories, how you think, what you would do first. Bring STAR stories with numbers."),
    ("03", "Case or take home", "2 to 5 days", "A launch plan, partner plan, territory plan or mock pitch, then a 30 to 45 minute presentation."),
    ("04", "Cross functional panel", "45 to 90 min", "Sales, product, CS or partner leaders test how you work with them. Ask how they measure you."),
    ("05", "Leadership or founder", "30 to 45 min", "Judgement, ambition and culture fit. Have a point of view on the company's market."),
    ("06", "Offer and HR", "1 to 2 weeks", "CTC split, ESOPs, notice buyout, references and background checks. Get everything in writing."),
]
SIGN = [
    ("Notice periods are long", "60 to 90 days is common in Indian companies, and startups often want you sooner. Know your real notice period, whether early release is possible, and ask about a notice buyout before you accept."),
    ("CTC is more than the number", "Offers usually split into fixed pay, variable or OTE, joining bonus and ESOPs. Sales roles often carry a large variable share. Compare offers on fixed pay first."),
    ("ESOPs need four answers", "Ask for the vesting schedule and cliff, strike price, exercise window after you leave, and whether the company has ever run a buyback."),
    ("Know the company type", "GCCs and MNCs run structured, competency based loops. Funded startups lean on cases and founder rounds. Indian SaaS scale ups mix both. Tailor your stories to the type."),
    ("Ask about office days", "Many Bengaluru teams are hybrid. ORR, Whitefield, Koramangala, HSR and Manyata can mean very different commutes, so ask in the first call."),
    ("Referrals still win", "A referral from someone in the team usually beats a cold application. Find the hiring manager and a peer on LinkedIn, and apply the same day you ask."),
]


def build_playbook():
    pages = [cover("Interview prep &middot; Bengaluru &middot; 2026", "From first call to", "signed offer",
                   "How a B2B SaaS interview loop usually runs for PMM, partnerships and sales roles, what each round tests, and the six things to check before you sign.",
                   ["6 rounds", "6 offer checks", "Bengaluru specific"],
                   [("6", "Interview rounds"), ("6", "Checks before you sign"), ("1", "Story, told well")])]
    rd = "".join(f'<div class="rd"><small>ROUND {a}</small><h3>{b}</h3><span class="dur">{c}</span><p>{d}</p></div>' for a, b, c, d in ROUNDS)
    pages.append(f'<section class="page"><div class="ph"><h2>Six rounds, one <em>story</em></h2><span>the loop</span></div>'
                 f'<p class="lede">Most B2B SaaS companies in Bengaluru run four to six stages for these roles. Formats vary, so ask the recruiter for the exact loop in the first call.</p>'
                 f'<div class="rounds">{rd}</div>{foot(2, "Interview loop and offer playbook")}</section>')
    tp = "".join(f'<div class="tip"><h3>{a}</h3><p>{b}</p></div>' for a, b in SIGN)
    pages.append(f'<section class="page"><div class="ph"><h2>Six things to know before you <em>sign</em></h2><span>the offer</span></div>'
                 f'<p class="lede">The parts of a Bengaluru job search that generic interview guides skip.</p><div class="tips">{tp}</div>'
                 f'<div class="cta"><div><b>Want a one to one mock interview?</b><span>Book a free call, or check the India PMM salary bands before you negotiate.</span></div><i>syedcreates.com/schedule-meeting</i></div>'
                 f'{foot(3, "Interview loop and offer playbook")}</section>')
    return page_html(pages, "Interview Loop and Offer Playbook")


def render(html, name):
    src = TMP / f"{name}.html"
    src.write_text(html, encoding="utf-8")
    js = ("const {chromium}=require('/opt/npm-tools/node_modules/playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{src}');await p.evaluate(()=>document.fonts.ready);"
          f"await p.pdf({{path:'{OUT / (name + '.pdf')}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close()}})()")
    subprocess.run(["node", "-e", js], check=True)
    print("wrote", name + ".pdf")


if __name__ == "__main__":
    render(build_questions(), "interview-questions-and-answers")
    render(build_playbook(), "interview-loop-and-offer-playbook")
