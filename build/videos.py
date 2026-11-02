#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: "Learn from the best" video sections (6 YouTube videos, click to play) on each finance calculator page
# Owner: Syed Hadi
import os
import re

ROOT = "/home/claude/work/site"

VIDEOS = {
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


def section(title, eyebrow, vids):
    cards = ""
    for vid, ch, t in vids:
        cards += (f'<article class="yt-card reveal"><div class="yt-frame" data-id="{vid}" data-title="{t}" role="button" tabindex="0" aria-label="Play: {t} by {ch}">'
                  f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{t}, video thumbnail from {ch}" width="480" height="360" loading="lazy" decoding="async">'
                  f'<span class="yt-play" aria-hidden="true"><span><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></span></div>'
                  f'<div class="yt-body"><small>{ch}</small><b>{t}</b></div></article>')
    return f'''<section class="yt-sec" id="learn" aria-labelledby="yt-title">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2 class="display" id="yt-title">{title}</h2>
    <p>Hand picked from India's most followed personal finance channels. The numbers above are yours, these explain the thinking. Videos play here, on this page, when you tap them.</p></div>
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
    for name, (title, eyebrow, vids) in VIDEOS.items():
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            inject(p, section(title, eyebrow, vids))
            print("videos ->", name)


if __name__ == "__main__":
    main()
