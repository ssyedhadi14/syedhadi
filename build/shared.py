# Created by: Claude
# Date: 2026-10-31
# Purpose: Shared snippets (Calculator mega menu, CSS additions, redirects) for the syedcreates.com fix pass
# Owner: Syed Hadi

SITE = "https://syedcreates.com"
VER = "20261103b"

def uns(pid, w=480, h=270, q=80):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&q={q}&w={w}&h={h}"

CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>'

CALCS = [
    # key, href, title, 2 line description, unsplash id, alt, badge
    ("salarycalc", "/salary-calculator", "Salary Growth Calculator",
     "Your salary, savings and corpus for the next 45 years. Get the PDF report in your inbox.",
     "1579621970563-ebec7560ff3e", "Young plant growing out of a pile of coins", "NEW"),
    ("loan", "/loan-calculator", "Loan EMI and Prepay Planner",
     "Home, car or personal loan EMI, close it in half the time, and prepay versus invest.",
     "1560518883-ce09059eeffa", "Keys being handed over in front of a new home", "NEW"),
    ("car", "/car-mileage-calculator", "Car Mileage and Running Cost",
     "Litres per month, fuel cost by city, cost per km and tank range. Pre filled for a Fronx.",
     "1449965408869-eaa3f722e40d", "Car driving on an open road at golden hour", "NEW"),
    ("bmi", "/bmi-calculator", "BMI and Healthy Habits",
     "BMI on Indian cut offs, what to start and stop doing, and a 7 day habits tracker.",
     "1476480862126-209bfaa8edc8", "Running shoes on outdoor stairs", "NEW"),
    ("fire", "/fire-calculator", "FIRE Calculator India",
     "Your FIRE number, the SIP you need and your earliest retirement age.",
     "1476514525535-07fb3b4ae5f1", "Wooden boat on a calm mountain lake", ""),
    ("mf", "/mutual-fund-returns-calculator", "Mutual Fund Returns",
     "Real 1 to 20 year returns of 50 Indian funds, with a SIP and lumpsum projector.",
     "1559526324-4b87b5e36e44", "Person reviewing investment charts on a laptop", ""),
    ("salary", "/pmm-salary-2026#calculator", "PMM Salary Calculator",
     "India product marketing pay by title, experience and city, with a free PDF guide.",
     "1522202176988-66273c2fd55f", "Three colleagues comparing notes at a laptop", ""),
    ("khums", "/qums", "Qums Calculator",
     "Shia Qums (Khums) in three steps, with Sahm e Imam and Sahm e Sadat worked out.",
     "1532629345422-7515f3d16bb6", "Open hands holding coins and a note that says make a change", ""),
]
SCORECARDS = [
    ("tool_seo", "/seo-aeo-score", "SEO and AEO Score"),
    ("tool_company", "/company-research", "Company Research"),
    ("tool_ai", "/ai-visibility-checker", "AI Visibility Checker"),
    ("tool_gtm", "/gtm-health-check", "GTM Health Check"),
    ("tool_partner", "/partner-readiness-score", "Partner Readiness Score"),
]


TEXT_CALCS = ("car",)  # shown as plain text links under the cards, by request
FEATURE = ("tool_company", "/company-research", "Company Research",
           "Paste a homepage. Get market cap, ARR, customers, competitors, pain points and missed revenue on one page.",
           "1542744173-8e7e53415bb0", "Team reviewing a go to market plan in a meeting room")


def calc_menu():
    k, h, t, d, pid, alt = FEATURE
    cards = (f'<a class="gb-card gb-feature" data-p="{k}" href="{h}"><span class="gb-img"><span class="badge-f">NEW &middot; AI</span>'
             f'<img src="{uns(pid)}" alt="{alt}" width="480" height="270" loading="lazy" decoding="async"></span>'
             f'<span class="gb-body"><b>{t}</b><small>{d}</small><span class="gb-go">Research a company &rarr;</span></span></a>')
    for key, href, title, desc, pid, alt, badge in CALCS:
        if key in TEXT_CALCS:
            continue
        b = f'<span class="badge-f">{badge}</span>' if badge else ""
        cards += (f'<a class="gb-card" data-p="{key}" href="{href}"><span class="gb-img">{b}'
                  f'<img src="{uns(pid)}" alt="{alt}" width="480" height="270" loading="lazy" decoding="async"></span>'
                  f'<span class="gb-body"><b>{title}</b><small>{desc}</small></span></a>')
    more = "".join(f'<a data-p="{key}" href="{href}">{title}</a>' for key, href, title, *_ in CALCS if key in TEXT_CALCS)
    sub = ('<div class="calc-sub"><span>More calculators</span>' + more + '<span class="calc-sep" aria-hidden="true"></span><span>GTM scorecards</span>' + "".join(
        f'<a data-p="{k2}" href="{h2}">{t2}</a>' for k2, h2, t2 in SCORECARDS if k2 != k) + '</div>')
    simple = '<div class="mm-simple">' + f"<a href='{h}'>{t}</a>" + "".join(f"<a href='{hh}'>{tt}</a>" for _, hh, tt, *_ in CALCS) + "".join(
        f"<a href='{hh}'>{tt}</a>" for kk, hh, tt in SCORECARDS if kk != k) + '</div>'
    return f'''<div class="dd mega" data-group="calc">
        <button class="dd-btn" data-group="calc" aria-haspopup="true" aria-expanded="false">Calculator {CHEV}</button>
        <div class="dd-menu mm mm-calc"><div class="gb-grid calc-grid">{cards}</div>{sub}</div>
        {simple}
      </div>
'''


CSS_ADD = r'''
/* ===== 2026-11-02 typography: Plus Jakarta Sans (display), Instrument Serif (accent), Inter (body), JetBrains Mono (labels) ===== */
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:500;font-display:swap;src:url(/assets/fonts/web/plus-jakarta-sans-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:600;font-display:swap;src:url(/assets/fonts/web/plus-jakarta-sans-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:700;font-display:swap;src:url(/assets/fonts/web/plus-jakarta-sans-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:800;font-display:swap;src:url(/assets/fonts/web/plus-jakarta-sans-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;font-display:swap;src:url(/assets/fonts/web/instrument-serif-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(/assets/fonts/web/instrument-serif-latin-400-italic.woff2) format("woff2")}
.display{letter-spacing:-.035em;font-weight:800}
h1.display span,h2.display span,.display em,.serif-accent{font-family:"Instrument Serif",Georgia,"Times New Roman",serif;font-style:italic;font-weight:400;letter-spacing:-.01em}
h1.display span{font-size:1.06em;line-height:1}
h2.display span{color:var(--accent)}
.sp-hero h1 span{font-style:italic}
.sec-head h2{letter-spacing:-.035em}
.page-hero p,.sec-head p{font-weight:400}
/* ===== 2026-10-31 QA pass: accessibility, Calculator menu, finance section, case study photos ===== */
.skip{position:absolute;left:12px;top:-60px;z-index:1000;padding:10px 14px;border-radius:10px;background:var(--accent);color:#fff;font-weight:600;transition:top .2s}
.skip:focus{top:12px;outline:2px solid #fff}
.fr-money small{font-size:12.5px}
.mw-h .h4{font-family:"Bricolage Grotesque";font-size:22px;font-weight:700;letter-spacing:-.01em;margin:0}
.mw-card .h4{font-family:"Bricolage Grotesque";font-size:19px;font-weight:700;line-height:1.2;margin-bottom:8px}
.fcol .h4{font-family:"JetBrains Mono",monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:16px;font-weight:500}
.win h3{font-size:16px;margin:14px 0 6px}
.dd-menu.mm-calc{width:min(1100px,calc(100vw - 48px));padding:14px}
.calc-grid{grid-template-columns:repeat(4,1fr)}
.dd-menu.mm .calc-grid .gb-card small{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.dd-menu.mm .calc-grid .gb-card .gb-img{aspect-ratio:16/9}
.calc-sub{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;padding:10px 12px;border-radius:10px;background:var(--accent-soft)}
.calc-sub span{font:600 12px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-right:6px}
.calc-sub a{font-weight:600;font-size:13.5px;color:var(--ink);padding:6px 10px;border-radius:8px;background:var(--card);border:1px solid var(--line)}
.calc-sub a:hover{border-color:var(--accent);color:var(--accent)}

/* case study covers with photos */
.cs-cover.photo .cs-cv-m,.cs-cover.photo .cs-cv-l{position:relative;z-index:1;text-shadow:0 2px 14px rgba(0,0,0,.45)}
.cs-feat .cs-cover.photo img{transition:transform .6s var(--ease)}
.cs-feat:hover .cs-cover.photo img{transform:scale(1.04)}
.lp-box.has-img{padding:0;overflow:hidden;display:grid;grid-template-rows:auto 1fr}
.lp-box.has-img .lp-img{display:block;aspect-ratio:16/8;overflow:hidden;background:var(--bg-soft)}
.lp-box.has-img .lp-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}
.lp-box.has-img:hover .lp-img img{transform:scale(1.05)}
.lp-box.has-img .lp-txt{display:block;padding:16px 18px 18px}
/* finance calculators band (tools page) */
.fin-band{padding:72px 0 76px;background:linear-gradient(160deg,#fff7ed 0%,#fdf2f8 38%,#eef2ff 72%,#ecfeff 100%);border-top:1px solid var(--line);position:relative;overflow:hidden}
[data-theme=dark] .fin-band{background:linear-gradient(160deg,#2a1a0f 0%,#2a1030 38%,#15173a 72%,#0e2630 100%)}
.fin-band .sec-head{text-align:left;margin-left:0;max-width:720px}
.fin-band .sec-head p{color:var(--ink-2)}
.fin-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-top:30px}
.fin-card{position:relative;display:flex;flex-direction:column;border-radius:20px;overflow:hidden;background:var(--card);border:1px solid var(--line);text-decoration:none;color:inherit;box-shadow:0 10px 30px rgba(28,16,80,.08);transition:transform .3s var(--ease),box-shadow .3s var(--ease),border-color .3s}
.fin-card:hover{transform:translateY(-6px);box-shadow:0 22px 44px rgba(28,16,80,.16);border-color:var(--accent)}
.fin-img{position:relative;aspect-ratio:16/10;overflow:hidden;background:#dbeafe}
.fin-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .7s var(--ease);filter:saturate(1.15) brightness(1.04)}
.fin-card:hover .fin-img img{transform:scale(1.07)}
.fin-img .badge-f{top:12px;left:12px}
.fin-body{padding:18px 18px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.fin-body b{font-family:"Bricolage Grotesque",sans-serif;font-size:20px;font-weight:800;letter-spacing:-.01em;color:var(--ink)}
.fin-body p{font-size:14.5px;color:var(--ink-2);line-height:1.5;margin:0;flex:1}
.fin-cta{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;margin-top:6px;padding:11px 16px;border-radius:999px;font-weight:700;font-size:14px;color:#fff;background:linear-gradient(90deg,var(--accent),#8b5cf6,var(--accent));background-size:200% 100%;animation:finShine 3.2s linear infinite;box-shadow:0 8px 20px rgba(91,61,245,.28);position:relative}
.fin-cta::after{content:"";position:absolute;inset:-4px;border-radius:999px;border:2px solid var(--accent);opacity:0;animation:finPulse 2.4s ease-out infinite}
.fin-cta svg{width:16px;height:16px;transition:transform .25s}
.fin-card:hover .fin-cta svg{transform:translateX(4px)}
@keyframes finShine{to{background-position:200% 0}}
@keyframes finPulse{0%{transform:scale(.96);opacity:.55}70%,100%{transform:scale(1.14);opacity:0}}
.fin-deco{position:absolute;border-radius:50%;filter:blur(40px);opacity:.55;pointer-events:none}
.fin-deco.d1{width:360px;height:360px;background:#fde68a;top:-140px;right:-80px}
.fin-deco.d2{width:300px;height:300px;background:#c4b5fd;bottom:-120px;left:-60px}
@media (prefers-reduced-motion:reduce){.fin-cta,.fin-cta::after{animation:none}}
@media (max-width:1200px){.fin-grid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:860px){.fin-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.fin-grid{grid-template-columns:1fr}.fin-band{padding:56px 0}}
/* home: featured strip right under hero */
.feat-sec{padding:0}
.feat-sec .logos{margin-top:0}
/* home: wins with photos */
.win.has-img{padding:0;overflow:hidden;display:flex;flex-direction:column}
.win.has-img .win-img{aspect-ratio:16/9;overflow:hidden;background:var(--bg-soft);display:block;position:relative}
.win.has-img .win-img img{width:100%;height:100%;object-fit:cover;display:block}
.win.has-img .win-img.logo{display:grid;place-items:center;background:linear-gradient(140deg,var(--accent-soft),var(--card))}
.win.has-img .win-img.logo img{width:auto;height:66%;object-fit:contain}
.win.has-img .win-txt{padding:18px 22px 22px}
.win.has-img .win-txt b{font-size:34px}

/* fallbacks and late additions */
.cs-cover.photo{background:#1a1050}
.gb-img,.fin-img,.lp-img{background:#e0e7ff}
.lip .lip-h{font-family:"Bricolage Grotesque";font-size:18.5px;font-weight:700;line-height:1.25;margin:12px 0 8px}
.kh-mcard .kh-mt{margin:0;font-family:"JetBrains Mono",monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-weight:500}
/* Calculator menu polish */
.dd-menu.mm .calc-sub{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;padding:10px 12px;border-radius:12px;background:var(--accent-soft)}
.dd-menu.mm .calc-sub span{font:600 11.5px "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-right:4px}
.dd-menu.mm .calc-sub a{display:inline-flex;align-items:center;padding:7px 12px;border-radius:999px;font-size:13.5px;font-weight:600;color:var(--ink);background:var(--card);border:1px solid var(--line);transition:border-color .15s,color .15s,transform .15s}
.dd-menu.mm .calc-sub a:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px)}
.dd-menu.mm .calc-grid .gb-card{display:flex;flex-direction:column;height:100%}
.dd-menu.mm .calc-grid .gb-body{display:flex;flex-direction:column;gap:4px;padding:12px 14px 14px;flex:1}
.dd-menu.mm .calc-grid .gb-body b{font-size:15px;line-height:1.25;color:var(--ink)}
.dd-menu.mm .calc-grid .gb-body small{font-size:12.5px;line-height:1.4;color:var(--ink-3);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.dd-menu.mm .calc-grid .gb-card.active .gb-body b{color:var(--accent)}
.dd-menu.mm .calc-grid .gb-card .badge-f{top:10px;left:10px}
/* Salary calculator step numbering */
.sc-group summary{display:flex;align-items:center;gap:10px;list-style:none}
.sc-group summary::-webkit-details-marker{display:none}
.sc-group summary .stn{width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700;flex:none}
.sc-group summary b{font-size:16px;flex:1}
.sc-group summary em{font-style:normal;color:var(--accent);font-weight:700;font-size:14px}
.sc-group summary .chev{width:16px;height:16px;color:var(--ink-3);transition:transform .2s}
.sc-group[open] summary .chev{transform:rotate(180deg)}
.fr-adv summary{display:flex;align-items:center;gap:10px;list-style:none;margin-bottom:12px}
.fr-adv summary::-webkit-details-marker{display:none}
.fr-adv summary .stn{width:26px;height:26px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-size:13px;font-weight:700;flex:none}
.fr-adv summary b{font-size:16px;color:var(--ink)}
.fr-adv summary em{font-style:normal;color:var(--ink-3);font-weight:500;font-size:13px}
/* third party badge frames never render */
#nl-badge-frame,iframe[id^="nl-badge"],iframe[src*="netlify.com/badge"]{display:none!important;visibility:hidden!important;width:0!important;height:0!important;pointer-events:none!important}
/* Humans of Marketing feature on the homepage */
.hom-feat{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:stretch;margin-top:8px}
.hom-card{border:1px solid var(--line);border-radius:22px;padding:26px 28px;background:linear-gradient(140deg,var(--card),var(--accent-soft));display:flex;flex-direction:column;gap:14px}
.hom-head{display:flex;gap:14px;align-items:center}
.hom-head img{width:44px;height:44px;border-radius:10px;flex:none}
.hom-head b{display:block;font-family:"Bricolage Grotesque";font-size:20px;letter-spacing:-.02em;line-height:1.15;margin-top:2px}
.hom-card blockquote{margin:0;padding:0 0 0 16px;border-left:3px solid var(--accent);font-family:"Bricolage Grotesque";font-weight:600;font-size:clamp(18px,2vw,22px);line-height:1.35;letter-spacing:-.01em}
.hom-card p{margin:0;color:var(--ink-2);font-size:15px;line-height:1.6;flex:1}
.hom-acts{display:flex;gap:10px;flex-wrap:wrap}
.hom-embed{height:auto;min-height:560px;aspect-ratio:auto;border:1px solid var(--line);background:var(--bg-soft);box-shadow:none}
.hom-embed .vid-ph{display:grid;color:var(--ink-3)}
.hom-embed .vid-play{background:var(--accent);color:#fff}
.hom-embed.ready .vid-ph{display:none}
.hom-mark b{font-weight:800;font-size:15px;color:var(--ink);letter-spacing:-.01em}
.hom-mark img{border-radius:6px}
@media (max-width:900px){.hom-feat{grid-template-columns:1fr}.hom-embed{min-height:560px}}
/* parent page links inside the mega menus */
.mm-all{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
.mm-all a{font-weight:700;color:var(--accent);text-decoration:none;font-size:14px}
.mm-all a:hover{text-decoration:underline}
.mm-all span{font-size:13px;color:var(--ink-3)}
.dd-menu.mm .mm-all a{padding:0}
.mm-simple a.mm-parent{font-weight:800;color:var(--accent)}
/* Work menu, image led */
.mw-mid2{padding:0 4px;display:flex;flex-direction:column;gap:10px}
.mw-photo{position:relative;display:block;border-radius:16px;overflow:hidden;aspect-ratio:16/8.4;background:var(--bg-soft)}
.mw-photo img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s var(--ease)}
.mw-photo:hover img{transform:scale(1.04)}
.mw-ph-t{position:absolute;left:0;right:0;bottom:0;padding:48px 18px 16px;display:flex;align-items:flex-end;gap:12px;background:linear-gradient(180deg,rgba(10,6,30,0) 0%,rgba(10,6,30,.82) 70%);color:#fff}
.mw-ph-t b{display:block;font-family:"Bricolage Grotesque";font-size:22px;letter-spacing:-.02em;line-height:1.1}
.mw-ph-t em{display:block;font-style:normal;font-size:13.5px;opacity:.9;margin-top:3px}
.mw-chips{display:flex;flex-wrap:wrap;gap:6px}
.mw-chips span{font-size:12.5px;font-weight:600;padding:6px 11px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.mw-quote{margin:0;padding:14px 16px 12px 18px;border-left:3px solid var(--accent);background:var(--bg-soft);border-radius:0 14px 14px 0}
.mw-quote p{margin:0;font-family:"Bricolage Grotesque";font-weight:600;font-size:15.5px;line-height:1.35;letter-spacing:-.01em;color:var(--ink)}
.mw-quote cite{display:block;font-style:normal;font:600 11px "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-top:8px}
.dd-menu.mm a.mw-card2{padding:18px;text-decoration:none;color:#fff}
.mw-card .art.art-img{height:150px;padding:0;overflow:hidden;background:#0d0b1a}
.mw-card .art.art-img img{width:100%;height:100%;object-fit:cover;display:block;opacity:.95}
.mw-card2 .go{margin-top:auto}
/* Tools menu, photo cards */
.pf-grid3{grid-template-columns:repeat(3,1fr)}
.pf-card.pf-photo .pf-img{aspect-ratio:16/9.6;position:relative;overflow:hidden;background:var(--bg-soft)}
.pf-card.pf-photo .pf-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s var(--ease)}
.pf-card.pf-photo:hover .pf-img img{transform:scale(1.05)}
.pf-foot{display:grid;grid-template-columns:1.1fr 1.6fr;gap:16px;align-items:start;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
.pf-quote{height:100%}
.pf-links2{display:flex;flex-wrap:wrap;gap:6px 10px}
.dd-menu.mm .pf-links2 a{padding:7px 12px;border:1px solid var(--line);border-radius:999px;font-size:13px;font-weight:600;color:var(--ink-2)}
.dd-menu.mm .pf-links2 a:hover{border-color:var(--accent);color:var(--accent)}
@media (max-width:1200px){.pf-foot{grid-template-columns:1fr}}
/* Newsletter band v2 */
.newsletter.nl2{padding:84px 0 88px;background:radial-gradient(1200px 500px at 15% 0%,#2a1a7a 0%,#1e1050 45%,#140b3a 100%)}
.newsletter.nl2::before{opacity:.5}
.nl2-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.nl2-orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:.55}
.nl2-orb.o1{width:420px;height:420px;background:#7c5cff;right:-120px;top:-160px}
.nl2-orb.o2{width:360px;height:360px;background:#c026d3;left:30%;bottom:-220px;opacity:.35}
.nl2-in{position:relative;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.nl2-copy h2{font-size:clamp(30px,3.6vw,46px);color:#fff;margin:14px 0 12px;max-width:620px}
.nl2-copy > p{color:#d4ccff;font-size:17px;max-width:560px;line-height:1.6}
.nl2-points{list-style:none;margin:24px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.nl2-points li{display:grid;grid-template-columns:auto 1fr;gap:10px 12px;align-items:start}
.nl2-points b{display:block;font-size:14.5px;color:#fff}
.nl2-points small{display:block;font-size:12.5px;color:#c9bfff;line-height:1.4;margin-top:2px}
.nl2-ic{grid-row:span 2;width:36px;height:36px;border-radius:10px;background:rgba(255,255,255,.1);display:grid;place-items:center;color:#c9bfff}
.nl2-ic svg{width:18px;height:18px}
.nl2-proof{display:flex;align-items:center;gap:12px;margin-top:26px;font-size:13.5px;color:#c9bfff}
.nl2-proof a{color:#fff;text-decoration:underline}
.nl2-avatars{display:flex}
.nl2-avatars img{width:32px;height:32px;border-radius:50%;border:2px solid #1e1050;object-fit:cover;margin-left:-8px}
.nl2-avatars img:first-child{margin-left:0}
.nl2-card{position:relative}
.nl2-stack{position:relative;height:150px;margin-bottom:-26px;z-index:1}
.nl2-issue{position:absolute;left:24px;right:24px;top:0;height:128px;border-radius:16px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.35);padding:18px 20px;display:flex;flex-direction:column;gap:6px;color:#0d0b1a}
.nl2-issue.i2{transform:translateY(14px) scale(.95);opacity:.75;background:#efeaff}
.nl2-issue.i3{transform:translateY(28px) scale(.9);opacity:.5;background:#d9d0ff}
.nl2-issue em{font-style:normal;font:700 10.5px "JetBrains Mono",monospace;letter-spacing:.14em;color:#5b3df5}
.nl2-issue b{font-family:"Bricolage Grotesque";font-size:16.5px;line-height:1.25;letter-spacing:-.01em}
.nl2-issue i{font-style:normal;font-size:12px;color:#7c7992;margin-top:auto}
.nl2-form{position:relative;z-index:2;background:#fff;border-radius:22px;padding:34px 26px 24px;box-shadow:0 30px 70px rgba(0,0,0,.35)}
.nl2-form label{display:block;font-family:"Bricolage Grotesque";font-weight:700;font-size:19px;color:#0d0b1a;margin-bottom:12px;letter-spacing:-.01em}
.nl2-form .nl-row input{background:#f4f2fb;border:1.5px solid #e4e1f0;color:#0d0b1a}
.nl2-form .nl-row input:focus{outline:0;border-color:#5b3df5;box-shadow:0 0 0 3px rgba(91,61,245,.18)}
.nl2-form .nl-row button{background:#5b3df5;padding:0 18px;white-space:nowrap}
.nl2-form .nl-row button:hover{background:#4a2fd6}
.nl2-form small{color:#7c7992}
.nl2-form small a{color:#5b3df5}
@media (max-width:980px){.nl2-in{grid-template-columns:1fr}.nl2-points{grid-template-columns:1fr}.nl2-stack{height:130px}}
@media (max-width:560px){.newsletter.nl2{padding:60px 0}.nl2-form{padding:28px 18px 20px}.nl2-form .nl-row{flex-direction:column}.nl2-form .nl-row button{padding:14px}}
/* Recognition photography */
.rec-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;max-width:1240px;margin:-26px auto 34px;padding:0 20px}
.rec-strip img{width:100%;height:170px;aspect-ratio:auto;object-fit:cover;border-radius:16px;box-shadow:0 14px 34px rgba(28,16,80,.14);transition:transform .4s var(--ease)}
.rec-strip img:nth-child(odd){transform:translateY(10px)}
.rec-strip img:hover{transform:translateY(-4px) scale(1.02)}
.rec-gallery{grid-template-columns:repeat(3,1fr);gap:18px}
.rec-gallery .shot .ph{aspect-ratio:4/3}
.rec-gallery .body{padding:16px 18px 18px}
.rec-gallery h3{font-size:17px;margin:6px 0 4px}
.rec-gallery p{font-size:14px;color:var(--ink-2);line-height:1.5}
@media (max-width:980px){.rec-strip{grid-template-columns:repeat(3,1fr)}.rec-strip img:nth-child(n+4){display:none}.rec-gallery{grid-template-columns:1fr 1fr}}
@media (max-width:600px){.rec-gallery{grid-template-columns:1fr}.rec-strip{grid-template-columns:1fr 1fr}.rec-strip img:nth-child(n+3){display:none}}
/* Humans of Marketing photo card */
.hom-photo{position:relative;border-radius:22px;overflow:hidden;background:#0d0b1a;box-shadow:0 24px 60px rgba(28,16,80,.2);min-height:520px}
.hom-photo img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;position:absolute;inset:0}
.hom-photo span{position:absolute;left:18px;right:18px;bottom:16px;color:#fff;font-size:13px;line-height:1.4;text-shadow:0 2px 10px rgba(0,0,0,.6)}
.hom-photo span b{display:block;font-family:"Bricolage Grotesque";font-size:17px}
/* LinkedIn posts imagery */
.lip{display:flex;flex-direction:column}
.lip-img{display:block;margin:-20px -20px 14px;aspect-ratio:16/10;overflow:hidden;border-radius:18px 18px 0 0;background:var(--bg-soft);position:relative}
.lip-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}
.lip:hover .lip-img img{transform:scale(1.04)}
.lip-cover{display:grid;place-items:center;height:100%;color:#fff;background:linear-gradient(135deg,#1e1050,#5b3df5)}
.lip-cover.k-event{background:linear-gradient(135deg,#0f3d2e,#10b981)}
.lip-cover.k-video{background:linear-gradient(135deg,#3b0a2e,#f43f5e)}
.lip-cover.k-reshare{background:linear-gradient(135deg,#1f2937,#64748b)}
.lip-cover.k-post{background:linear-gradient(135deg,#1e1050,#7c5cff)}
.lip-cover svg{width:44px;height:44px;opacity:.9}
.lip-cover b{position:absolute;left:14px;bottom:12px;font:700 11px "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;opacity:.85}

/* calculator menu: Company Research feature card */
.dd-menu.mm .calc-grid .gb-img{position:relative;display:block;overflow:hidden}
.dd-menu.mm .calc-grid .gb-img .badge-f{position:absolute;top:10px;left:10px;z-index:1}
.dd-menu.mm .calc-grid .gb-card.gb-feature{position:relative;border:0;background:linear-gradient(150deg,#140d3a,#2c1c8a 60%,#5b3df5);box-shadow:0 14px 34px rgba(76,48,224,.35),inset 0 0 0 1px rgba(255,255,255,.12)}
.dd-menu.mm .calc-grid .gb-card.gb-feature .gb-img img{opacity:.78}
.dd-menu.mm .calc-grid .gb-card.gb-feature .gb-body b{color:#fff;font-size:16px}
.dd-menu.mm .calc-grid .gb-card.gb-feature .gb-body small{color:#e2dbff}
.gb-feature .badge-f{background:#ffd43b;color:#1b1145}
.gb-feature .gb-go{margin-top:auto;padding-top:6px;font-weight:700;font-size:13px;color:#ffd43b}
.dd-menu.mm .calc-grid .gb-card.gb-feature:hover{transform:translateY(-2px)}
.calc-sub .calc-sep{width:1px;height:18px;background:var(--line);margin:0 4px}
'''

REDIRECTS_HEAD = '''# syedcreates.com redirects. Netlify processes these top to bottom.
# Short links
/index.html        /                                                                                                   301!
/home              /                                                                                                   301
/book              /schedule-meeting                                                                                   301
/free-call         /schedule-meeting                                                                                   301
/calendly          /schedule-meeting                                                                                   301
/resume            https://drive.google.com/file/d/1YU9wvSdp2u5JmpGMzv2FoJk_xfd6Izmu/view?usp=drive_link               302
/deck              https://docs.google.com/presentation/d/11ro9a8Xxxv5hLKMMLTbSyHsYfrtDDCxWhrt7NwQqV-8/edit?usp=sharing  302
/qums-calculator   /qums                                                                                               301
/khums             /qums                                                                                               301
/khums-calculator  /qums                                                                                               301
/calculators       /calculator                                                                                         301
/medium-feed       https://medium.com/feed/@ssyedhadi                                                                  200
/car               /car-mileage-calculator                                                                             301
/mileage           /car-mileage-calculator                                                                             301
/loan              /loan-calculator                                                                                    301
/emi               /loan-calculator                                                                                    301
/press             /brand                                                                                              301
/media-kit         /brand                                                                                              301
/brand-kit         /brand                                                                                              301
/salary            /salary-calculator                                                                                  301
/fire              /fire-calculator                                                                                    301
/mf                /mutual-fund-returns-calculator                                                                     301
/skills            /skill-pack                                                                                         301
/cases             /case-studies                                                                                       301
/linkedin          https://www.linkedin.com/in/syedhadii/                                                              302
/medium            https://ssyedhadi.medium.com/                                                                       302
/substack          https://syedhadi.substack.com/                                                                      302
/newsletter        https://syedhadi.substack.com/                                                                      302
/whatsapp          https://wa.me/918015466708                                                                          302

# One URL per page: send the .html version to the clean URL (canonical)
'''

HEADERS = '''/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Cross-Origin-Opener-Policy: same-origin-allow-popups

/img/*
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *

/assets/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/downloads/*
  Cache-Control: public, max-age=86400

/photo.jpg
  Cache-Control: public, max-age=604800

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/sitemap.xml
  Content-Type: application/xml; charset=utf-8

/llms.txt
  Content-Type: text/plain; charset=utf-8
'''


# ---------------- Newsletter band (sitewide, above the footer) ----------------
def newsletter_section():
    return '''<section class="newsletter nl2" aria-labelledby="nl-title">
  <div class="nl2-bg" aria-hidden="true"><span class="nl2-orb o1"></span><span class="nl2-orb o2"></span></div>
  <div class="wrap nl2-in">
    <div class="nl2-copy">
      <span class="nl-eyebrow"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 3h14v18l-7-4-7 4z"/></svg>Pipeline Notes, the newsletter on Substack</span>
      <h2 id="nl-title" class="display">GTM notes from the field, before they become a case study.</h2>
      <p>Every other week: one play that moved pipeline at a security startup, the numbers behind it, and the template to run it yourself. Written for founders, product marketers and partner leads who own a revenue number.</p>
      <ul class="nl2-points">
        <li><span class="nl2-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18M7 14l4-4 4 4 5-6"/></svg></span><b>One play, with numbers</b><small>What we ran, what it cost, what it returned</small></li>
        <li><span class="nl2-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h5"/></svg></span><b>The template</b><small>Doc, sheet or Claude skill, ready to copy</small></li>
        <li><span class="nl2-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><b>Five minute read</b><small>No filler, no roundups, unsubscribe in one click</small></li>
      </ul>
      <div class="nl2-proof"><span class="nl2-avatars"><img src="/img/avatar.jpg" alt="" width="32" height="32" loading="lazy"><img src="/img/recs/nat-natraj.jpg" alt="" width="32" height="32" loading="lazy"><img src="/img/recs/raj-panchapakesan.jpg" alt="" width="32" height="32" loading="lazy"><img src="/img/recs/debjani-roy.jpg" alt="" width="32" height="32" loading="lazy"></span><span>Read by founders, CMOs and partner leads who follow the work on <a href="https://www.linkedin.com/in/syedhadii/" target="_blank" rel="noopener">LinkedIn</a>, 30,000 strong.</span></div>
    </div>
    <div class="nl2-card">
      <div class="nl2-stack" aria-hidden="true">
        <span class="nl2-issue i3"></span><span class="nl2-issue i2"></span>
        <span class="nl2-issue i1"><em>Issue 01</em><b>$2M pipeline on a $25K quarter: the inbound engine, line by line</b><i>5 min read &middot; template inside</i></span>
      </div>
      <form class="nl-form nl2-form" action="https://syedhadi.substack.com/subscribe" method="get" target="_blank" rel="noopener">
        <label for="nl-email">Get Pipeline Notes in your inbox</label>
        <div class="nl-row"><input id="nl-email" type="email" name="email" placeholder="you@company.com" required autocomplete="email"><button type="submit">Subscribe free</button></div>
        <small>Free on <a href="https://syedhadi.substack.com/" target="_blank" rel="noopener">Substack</a>. Every other Tuesday. Unsubscribe in one click.</small>
      </form>
    </div>
  </div>
</section>'''
