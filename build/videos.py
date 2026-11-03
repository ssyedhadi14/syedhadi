#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: "Learn from the best" video sections (6 YouTube videos, click to play) on each finance calculator page
# Owner: Syed Hadi
import os
import re

ROOT = "/home/claude/work/site"

VIDEOS = {

    "calculator.html": ("Six videos to get your money basics right", "Start here", [
        ("C49nSjzg1iw", "Asset Yogi", "The 50 30 20 rule of money, explained simply"),
        ("BTOHpoC-XsE", "Honestly by Tanmay Bhat", "Money lessons I wish I knew in my 20s"),
        ("tHxwyWnNu0c", "CA Rachana Ranade", "How to start investing in your 20s"),
        ("g-hir-4WzfU", "Ankur Warikoo", "How to build an emergency fund"),
        ("kywWhBXyFg0", "Labour Law Advisor", "9 simple habits to save more money"),
        ("XOWlHWgT2SQ", "Ankur Warikoo", "Escaping the middle class trap, the 3 paths of money"),
    ], "Hand picked from India's most watched money channels. Each one pairs with a calculator on this page."),
    "car-mileage-calculator.html": ("Six videos to cut your fuel bill", "Watch before you drive", [
        ("Pd2BkNaJG5c", "Knowledge Kingdom", "How to push car mileage from 15 to 25 km per litre"),
        ("smiJUQAHv2o", "Ask CarGuru", "Get better mileage on E20 petrol"),
        ("XUxwitNSmGo", "Satej Drives", "How to get the best mileage in heavy city traffic"),
        ("YbY1dA03Zd4", "MotorOctane", "Petrol vs hybrid vs diesel vs EV vs CNG, which saves money"),
        ("GGhaa_yRWmQ", "Autocar India", "Petrol vs diesel vs EV vs CNG, which one should you buy"),
        ("DJUk8zNMq6U", "Zero1 by Zerodha", "Fuel prices keep rising, should you buy an EV instead"),
    ], "Hand picked from India's top auto channels. Your number above shows the cost, these show how to bring it down."),
    "bmi-calculator.html": ("Six videos on reaching a healthy weight", "Watch before you diet", [
        ("ygAC0yJp1KU", "Dhruv Rathee", "How to lose weight, the complete science"),
        ("CV0lD2jLNH0", "Fit Tuber", "An Indian diet plan for weight loss"),
        ("hUfzYg92peQ", "Dr Pal", "How to burn fat for free"),
        ("S65AAXwYP14", "Ralston D'Souza", "3 fat loss mistakes that keep belly fat on"),
        ("auY3sWd2s2o", "Ranveer Allahbadia", "The ultimate weight loss guide"),
        ("8mWuOeycSYQ", "Healthy Hamesha", "5 surprising things daily walking does to your body"),
    ], "Hand picked from India's most followed health creators. General education only, so check with a doctor before a big change."),
    "pmm-salary-2026.html": ("Six videos on growing a PMM salary", "Watch before you negotiate", [
        ("BmunilI6FXA", "Diksha Arora", "7 tips to negotiate a higher salary"),
        ("JFdv8Z8iuok", "upGrad", "How to negotiate salary after a job offer"),
        ("lLpDWxrhhGI", "Warikoo Careers", "How to get a job at a GCC in 2026"),
        ("JXD4eTaxrSk", "faazil", "The highest paying career path in India right now"),
        ("C7dNExgqd5A", "Henry Wang", "Product marketing 101 with a Google PMM"),
        ("NL-pmvydNe8", "Jeff Su", "What product marketers actually do"),
    ], "Indian career coaches on negotiation, plus two of the most watched explainers on the PMM role itself."),
    "qums.html": ("Six videos on understanding Khums", "Learn before you calculate", [
        ("mqsoc9leb9g", "Shia Talks Azadari", "When Khums and Zakat become wajib, and how to work out Khums"),
        ("rYgN-R5RgTY", "Maulana Syed Ali Raza Rizvi", "What is Khums and what is Zakat"),
        ("NO2oDFt6UK4", "Message Of Insaniyat", "Khums nikalne ka tarika, how to calculate it"),
        ("hHV1aAcYza4", "Haq hai Ali", "The easy way to pay Khums"),
        ("EMss9eqUHYw", "Fiqah E Jaffaria", "Khums in full detail, when and on what"),
        ("a6cus3SjF2c", "Thaqlain", "Khums 101, what it is and the evidence for it"),
    ], "Explainers from Shia scholars and channels in Urdu, Hindi and English. Follow the rulings of your own Marja for final amounts."),
    "seo-aeo-score.html": ("Six videos to lift your SEO score", "Watch before you fix", [
        ("bLUkIgY8MTE", "WsCube Tech", "What SEO is and how it works"),
        ("TwQc_wqzzAY", "WsCube Tech", "Technical SEO explained, with techniques"),
        ("afqwbAtELp8", "WsCube Tech", "How to do on page SEO in 2026, practical"),
        ("nX9CV3wj6Pk", "WsCube Tech", "On page vs off page SEO, the difference"),
        ("CyRlWlaJnTY", "CodeWithHarry", "SEO and Core Web Vitals in HTML"),
        ("r8gNturJMeI", "Amit Tiwari", "GEO vs AEO vs SEO, an advanced class"),
    ], "Hand picked from India's most watched SEO teachers. Your score above shows the gaps, these show the fixes."),
    "company-research.html": ("Six videos on reading a company like an analyst", "Watch before you research", [
        ("POfmy7ZQAb4", "CA Rachana Ranade", "How to analyse a company step by step"),
        ("RpAenFUtGss", "CA Rachana Ranade", "Top 3 parameters for company analysis"),
        ("iWBjHPFrwrM", "Akshat Shrivastava", "Fundamentals of company analysis, a step by step process"),
        ("tFJiI0Dqkk0", "Pranjal Kamra", "A 6 step formula to analyse any company"),
        ("OGs2YsqvWDg", "Think School", "Blinkit's strategy that beat bigger rivals"),
        ("LII4y20fjC4", "Think School Hindi", "How Rapido beat Ola and Uber at their own game"),
    ], "Hand picked from India's top business analysts. Use them to sanity check the research card and spot the competitive angle."),
    "ai-visibility-checker.html": ("Six videos on getting cited by AI answers", "Watch before you optimise", [
        ("r8gNturJMeI", "Amit Tiwari", "GEO vs AEO vs SEO, an advanced class"),
        ("iaQ6ip3gRmE", "Umar Tazkeer", "SEO vs AIO vs GEO vs AEO, the real difference"),
        ("FC-6ePHxrwY", "Website Learners", "How to rank in Google's AI Overviews"),
        ("UqGpC1bwGhc", "WsCube Tech", "AI SEO full course, SEO, GEO and AEO"),
        ("S9J9yJbZu4I", "WsCube Tech", "How to rank on Google in 2026"),
        ("iT7kq-R3Gjc", "Lenny's Podcast", "The ultimate guide to AEO, getting cited by ChatGPT"),
    ], "Indian SEO teachers on AI search, plus the most cited AEO deep dive. Your check above shows where you stand."),
    "gtm-health-check.html": ("Six videos on go to market that works", "Watch before you scale", [
        ("Y3I073KSs6Q", "CA Rahul Malodia", "Zoho case study, India's most profitable SaaS built without loans"),
        ("EUcVBDtJo5M", "Think School", "CRED's business model explained"),
        ("gLeMTK3PeC8", "Think School", "Kunal Shah on building a business and a career"),
        ("T9faI-FINN8", "Gobinath", "What real growth means, Girish Mathrubootham"),
        ("qO5b-AF57nM", "Blume Ventures", "Building a 3.5B dollar global giant from Chennai to NASDAQ"),
        ("VMoN3o786ms", "Rajiv Talreja", "5 proven sales techniques to scale B2B"),
    ], "Lessons from India's best known founders and business teachers. Pair them with your weakest GTM pillar above."),
    "partner-readiness-score.html": ("Six videos on building a partner program", "Watch before you launch", [
        ("GWCHV8JYD_A", "Pratik Pandey", "What channel sales is and how partner strategy works"),
        ("0avH-mAWc6M", "MBAfactory", "What channel sales is and why companies use it"),
        ("ixj6U-RzIEA", "Sonu Singh", "Strategic alliances explained, concept and examples"),
        ("W0wtD1-PXUI", "CA Rahul Malodia", "How to increase sales for a small business or startup"),
        ("7ggj5Ahtwg4", "TK Kader", "Partnership marketing strategy for SaaS, a GTM case"),
        ("EbkITlMN39M", "Rewardful", "3 principles for a successful SaaS affiliate program"),
    ], "Indian explainers on channel sales, plus two SaaS partner playbooks. Fix your lowest scoring area above first."),
    "salary-calculator.html": ("Six videos on making a salary grow", "Watch before you plan", [
        ("U0503pX_P5k", "Akshat Shrivastava", "How to invest your salary, income wise, in 2026"),
        ("XBXa8HKFyaE", "Ankur Warikoo", "The complete investment guide for your 20s"),
        ("qhM6ML40dOI", "Zero1 by Zerodha", "How to make 1 crore on a 50,000 salary"),
        ("HewBrC1BMmg", "Dr. Anuj Pachhel", "How to invest your first salary"),
        ("J6DqLwrvqUY", "Ankur Warikoo", "The Excel sheet for a 6 crore retirement plan"),
        ("PbldLCsspgE", "CA Rachana Ranade", "What is a mutual fund and how does it work"),
    ]),
    "fire-calculator.html": ("Six videos on early retirement in India", "Watch before you plan", [
        ("apTTVY1EDUA", "Ankur Warikoo", "How much do you actually need to retire in India"),
        ("NNpLzKHH6oc", "ET Money", "How much do you need to retire at 45, a realistic FIRE framework"),
        ("0FFLXl05yz4", "Wint Wealth", "Is 2.5 crore enough to retire? Tested for 8 years"),
        ("9dqS2olRQfM", "Zero1 by Zerodha", "40 crores at 60? Indians are doing retirement wrong"),
        ("hRhKNiu6k7A", "Ankur Warikoo", "Plan your retirement with an Excel sheet"),
        ("TjrsreChnW8", "Pushkar Raj Thakur", "All types of FIRE explained"),
    ]),
    "mutual-fund-returns-calculator.html": ("Six videos on mutual funds, from basics to picking", "Watch before you invest", [
        ("PbldLCsspgE", "CA Rachana Ranade", "What is a mutual fund and how does it work"),
        ("ACpQo1a_RBk", "Ankur Warikoo", "How to invest in mutual funds"),
        ("JMV4XuuodPE", "Labour Law Advisor", "What are mutual funds? Ultimate investing guide, episode 1"),
        ("OuYvU5m2rhQ", "Zerodha Varsity", "How do mutual funds work"),
        ("Cb_CLN82CGc", "Zerodha Varsity", "How to analyse mutual funds in 2026, stop trusting star ratings"),
        ("A9S2TXc8ULY", "Zerodha Varsity", "SIP negative after 2 years? Stop or continue"),
    ]),
    "loan-calculator.html": ("Six videos on loans, EMIs and prepaying", "Watch before you prepay", [
        ("YMjTktGtVCk", "Labour Law Advisor", "How to save lakhs on your home loan, complete guide"),
        ("yydb_gBpEA0", "Ankur Warikoo", "Pay off debt faster, loans jaldi repay kariye"),
        ("E6h8Y4EKRZY", "Zero1 by Zerodha", "Invest or pay the loan? The F squared rule"),
        ("sgtQT4uPbjs", "CA Rachana Ranade", "Investing vs loan repayment"),
        ("QkaTdEINJJk", "Finance With Sharan", "The untold truth about home ownership, hidden costs and EMIs"),
        ("pKAcIV_zyaA", "Groww", "SIP vs home loan prepayment, save lakhs with this strategy"),
    ]),
}

CSS = r'''
/* Learn from the best: lite YouTube embeds */
.yt-sec{padding:64px 0 72px;background:var(--bg-soft);border-top:1px solid var(--line)}
.yt-sec .sec-head{text-align:left;margin-left:0;max-width:760px}
.yt-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}
.yt-card{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:var(--card);display:flex;flex-direction:column;transition:transform .25s var(--ease),box-shadow .25s var(--ease),border-color .25s}
.yt-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(28,16,80,.14);border-color:var(--accent)}
.yt-frame{position:relative;aspect-ratio:16/9;background:#0b0a12;cursor:pointer;overflow:hidden}
.yt-frame img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}
.yt-card:hover .yt-frame img{transform:scale(1.04)}
.yt-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.yt-play{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(180deg,transparent 40%,rgba(10,6,30,.55))}
.yt-play span{width:64px;height:46px;border-radius:12px;background:#ff0033;display:grid;place-items:center;box-shadow:0 10px 24px rgba(0,0,0,.35);transition:transform .2s}
.yt-card:hover .yt-play span{transform:scale(1.08)}
.yt-play svg{width:22px;height:22px;fill:#fff;margin-left:3px}
.yt-body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:4px}
.yt-body small{font:600 11.5px "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.yt-body b{font-size:15px;line-height:1.3;color:var(--ink)}
.yt-note{font-size:13px;color:var(--ink-3);margin-top:16px}
@media (max-width:980px){.yt-grid{grid-template-columns:1fr 1fr}}
@media (max-width:600px){.yt-grid{grid-template-columns:1fr}.yt-sec{padding:48px 0 56px}}
'''

JS = r'''
<script>
(function(){
  document.querySelectorAll('.yt-frame').forEach(function(f){
    f.addEventListener('click',function(){
      var id=f.getAttribute('data-id'); if(!id||f.querySelector('iframe'))return;
      var i=document.createElement('iframe'); i.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0'; i.title=f.getAttribute('data-title')||'YouTube video'; i.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; i.setAttribute('allowfullscreen','');
      f.innerHTML=''; f.appendChild(i);
      if(window.shTrack) shTrack('video_play',{label:id});
    });
  });
})();
</script>
'''


DEFAULT_INTRO = "Hand picked from India's most followed personal finance channels. The numbers above are yours, these explain the thinking."


def section(title, eyebrow, vids, intro=DEFAULT_INTRO):
    cards = ""
    for vid, ch, t in vids:
        cards += (f'<article class="yt-card reveal"><div class="yt-frame" data-id="{vid}" data-title="{t}" role="button" tabindex="0" aria-label="Play: {t} by {ch}">'
                  f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{t}, video thumbnail from {ch}" width="480" height="360" loading="lazy" decoding="async">'
                  f'<span class="yt-play" aria-hidden="true"><span><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></span></div>'
                  f'<div class="yt-body"><small>{ch}</small><b>{t}</b></div></article>')
    return f'''<section class="yt-sec" id="learn" aria-labelledby="yt-title">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2 class="display" id="yt-title">{title}</h2>
    <p>{intro} Videos play here, on this page, when you tap them.</p></div>
    <div class="yt-grid">{cards}</div>
    <p class="yt-note">Videos belong to their creators and open through YouTube's privacy enhanced player. Opinions in them are the creators' own, not advice from syedcreates.com.</p>
  </div>
</section>
'''


def inject(path, html_sec):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r'<section class="yt-sec".*?</section>\n', "", h, flags=re.S)
    h = h.replace(JS.strip() + "\n", "")
    assert h.count("<footer") == 1, path
    h = h.replace("<footer", html_sec + "<footer", 1)
    h = h.replace("</body>", JS.strip() + "\n</body>", 1)
    from serif import accent
    h = accent(h)
    open(path, "w", encoding="utf-8").write(h)


def main():
    for name, spec in VIDEOS.items():
        title, eyebrow, vids = spec[:3]
        intro = spec[3] if len(spec) > 3 else DEFAULT_INTRO
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            inject(p, section(title, eyebrow, vids, intro))
            print("videos ->", name)


if __name__ == "__main__":
    main()
