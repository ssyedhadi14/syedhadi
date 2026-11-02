#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Sitewide serif accent: one Instrument Serif italic word in every display heading, rotating through soft tints.
#          Idempotent: headings that already carry an accent span only get a tint class.
# Owner: Syed Hadi
import re

# exact heading text (tags stripped, whitespace collapsed) -> words to set in serif
SKIP = {"Syed Hadi"}  # the name in the homepage hero stays in the display sans

PICK = {
    "I&rsquo;m Featured on": "Featured",
    "Where Has Syed Shipped?": "Shipped?",
    "Six Things I Hand Over": "Things",
    "What People Say After Working With Syed": "Say",
    "Hand Claude your GTM busywork.": "busywork.",
    "Rooms I Have Filled": "Filled",
    "Education and Certifications": "Certifications",
    "QA Engineer in 2020, Growth Lead by 2026": "Growth Lead",
    "Moments From the Journey": "Journey",
    "Ready to GrowSomething Together?": "Together?",
    "Humans of Marketing, and a Word on AI": "Humans of Marketing,",
    "Everybody Uses AI. Who Secures It?": "Secures It?",
    "Get a free GTM audit of your website.": "audit",
    "Pick a 30 Minute Slot": "Slot",
    "Wins Worth Counting": "Counting",
    "GTM notes from the field, before they become a case study.": "case study.",
    "Common Questions": "Questions",
    "Related Insights": "Insights",
    "Frequently Asked Questions": "Questions",
    "How It Works": "Works",
}
STOP = set("""a an the and or of to in on at by for from with into over than that this these those your you our we us my me i it its is are be
been was were as so if not but out up off per via vs via about after before more most less very just also only can will what how why who
when where which there their them they do does did done get got has have had""".split())
TINTS = 6
HEAD = re.compile(r'<(h[12])\b([^>]*)>(.*?)</\1>', re.S)


def _pick_word(text):
    words = text.split()
    if len(words) <= 2:
        return words[-1]
    for w in reversed(words):
        core = re.sub(r"[^A-Za-z0-9%]", "", w)
        if len(core) >= 4 and core.lower() not in STOP and not core.isdigit():
            return w
    return words[-1]


def accent(html):
    n = [len(re.findall(r'class="[^"]*\bt(?:g)?[1-6]\b', html))]

    def tint(h1):
        n[0] += 1
        k = (n[0] - 1) % TINTS + 1
        return f"tg{k}" if h1 else f"t{k}"

    def rep(m):
        tag, attrs, inner = m.groups()
        if "'+" in inner or 'class="sr"' in inner or "class='sr'" in inner:
            return m.group(0)
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip()
        key = re.sub(r"\s+", " ", re.sub(r"<br\s*/?>", "", inner)).strip()
        key = re.sub(r"<[^>]+>", "", key)
        if plain in SKIP:
            # undo any accent a previous build added
            return f"<{tag}{attrs}>" + re.sub(r'<span class="tg?[1-6]">(.*?)</span>', r"\1", inner) + f"</{tag}>"
        is_display = "display" in attrs
        if not is_display and key not in PICK and plain not in PICK:
            return m.group(0)
        h1 = tag == "h1"
        # 1. already has an accent span: add a tint class once
        if re.search(r"<span(?![^>]*class=\"(?:num|cnt|sr)\")", inner):
            if re.search(r'class="[^"]*\bt(?:g)?[1-6]\b', inner):
                return m.group(0)
            def add(sm):
                tagtxt = sm.group(0)
                c = tint(h1)
                if 'class="' in tagtxt:
                    return tagtxt.replace('class="', f'class="{c} ', 1)
                return tagtxt[:-1] + f' class="{c}">'
            return f"<{tag}{attrs}>" + re.sub(r"<span(?![^>]*class=\"(?:num|cnt|sr)\")[^>]*>", add, inner, count=1) + f"</{tag}>"
        if "<em" in inner:
            # an existing emphasised word becomes the serif accent
            return f"<{tag}{attrs}>" + re.sub(r"<em>(.*?)</em>", lambda e: f'<span class="{tint(h1)}">' + e.group(1) + "</span>", inner, count=1) + f"</{tag}>"
        # 2. choose the words to set in serif
        want = PICK.get(key) or PICK.get(plain)
        # operate on the last plain text run (after the last tag) so <br> and links stay intact
        parts = re.split(r"(<[^>]+>)", inner)
        idx = max(i for i, p in enumerate(parts) if p and not p.startswith("<") and p.strip())
        run = parts[idx]
        if not want:
            if plain.isdigit() or len(plain) < 3:
                return m.group(0)
            want = _pick_word(run.strip())
        pos = run.rfind(want)
        if pos < 0:
            # the pick lives in an earlier text run
            for j in range(idx - 1, -1, -1):
                if parts[j] and not parts[j].startswith("<") and want in parts[j]:
                    idx, run, pos = j, parts[j], parts[j].rfind(want)
                    break
            if pos < 0:
                return m.group(0)
        parts[idx] = run[:pos] + f'<span class="{tint(h1)}">' + want + "</span>" + run[pos + len(want):]
        return f"<{tag}{attrs}>" + "".join(parts) + f"</{tag}>"

    return HEAD.sub(rep, html)


CSS = r'''
/* ===== serif accent tints (2026-11-02): one Instrument Serif italic word per display heading ===== */
.t1,.t2,.t3,.t4,.t5,.t6,.tg1,.tg2,.tg3,.tg4,.tg5,.tg6{font-family:"Instrument Serif",Georgia,serif!important;font-style:italic;font-weight:400!important;letter-spacing:-.005em}
h2 .t1,h2 .t2,h2 .t3,h2 .t4,h2 .t5,h2 .t6{font-size:1.08em;line-height:1}
h2.display .t1,.t1{color:#5b3df5} h2.display .t2,.t2{color:#0d9488} h2.display .t3,.t3{color:#d9534f} h2.display .t4,.t4{color:#b7791f} h2.display .t5,.t5{color:#2b77c9} h2.display .t6,.t6{color:#b0408f}
[data-theme=dark] h2.display .t1,[data-theme=dark] .t1{color:#a592ff} [data-theme=dark] h2.display .t2,[data-theme=dark] .t2{color:#5eead4} [data-theme=dark] h2.display .t3,[data-theme=dark] .t3{color:#fb9a8f} [data-theme=dark] h2.display .t4,[data-theme=dark] .t4{color:#f6c46b} [data-theme=dark] h2.display .t5,[data-theme=dark] .t5{color:#8cc4ff} [data-theme=dark] h2.display .t6,[data-theme=dark] .t6{color:#f39bd6}
h1 .tg1,h1 .tg2,h1 .tg3,h1 .tg4,h1 .tg5,h1 .tg6,h1.display span.tg1,h1.display span.tg2,h1.display span.tg3,h1.display span.tg4,h1.display span.tg5,h1.display span.tg6{-webkit-background-clip:text;background-clip:text;color:transparent!important;-webkit-text-fill-color:transparent;padding:0 .06em .08em 0;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.tg1{background-image:linear-gradient(100deg,#5b3df5 10%,#c2479b 95%)}
.tg2{background-image:linear-gradient(100deg,#0d9488 10%,#5b3df5 95%)}
.tg3{background-image:linear-gradient(100deg,#d9534f 5%,#b7791f 95%)}
.tg4{background-image:linear-gradient(100deg,#2b77c9 10%,#0d9488 95%)}
.tg5{background-image:linear-gradient(100deg,#b0408f 5%,#d9534f 95%)}
.tg6{background-image:linear-gradient(100deg,#7c5cff 10%,#2b77c9 95%)}
[data-theme=dark] .tg1{background-image:linear-gradient(100deg,#a592ff,#f39bd6)} [data-theme=dark] .tg2{background-image:linear-gradient(100deg,#5eead4,#a592ff)} [data-theme=dark] .tg3{background-image:linear-gradient(100deg,#fb9a8f,#f6c46b)}
[data-theme=dark] .tg4{background-image:linear-gradient(100deg,#8cc4ff,#5eead4)} [data-theme=dark] .tg5{background-image:linear-gradient(100deg,#f39bd6,#fb9a8f)} [data-theme=dark] .tg6{background-image:linear-gradient(100deg,#c4b5ff,#8cc4ff)}
.boxed.t1,.boxed.t2,.boxed.t3,.boxed.t4,.boxed.t5,.boxed.t6{border-color:currentColor}
/* inline serif in body copy */
.serif-accent{font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400;font-size:1.18em;line-height:1}
.hero .serif-accent,.hero-sub .serif-accent{color:#b9382f} [data-theme=dark] .hero .serif-accent{color:#fb9a8f}

/* ===== 2026-11-02 contrast pass: no dark on dark, no light on light ===== */
/* serif accent words on dark bands use light pastel tints (3:1+ on the lightest gradient stop) */
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) :is(.t1,.t2,.t3,.t4,.t5,.t6){-webkit-text-fill-color:currentColor;background:none}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t1{color:#e2dbff!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t2{color:#b5f5ea!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t3{color:#ffd6cf!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t4{color:#ffe27a!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t5{color:#cbe7ff!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.sa-score.total,.cs-cover) .t6{color:#ffd1ee!important}
:is(.cta-box,.au-box,.bx-final,.bx-proof,.hp-new,.newsletter.nl2,.sal-gate,.sal-out,.sp-bundle,.skill-band,.cs-cover) :is(.tg1,.tg2,.tg3,.tg4,.tg5,.tg6){background-image:linear-gradient(100deg,#e2dbff,#ffd1ee)!important}
.boxed:is(.t1,.t2,.t3,.t4,.t5,.t6){border-color:currentColor}
:is(.au-box,.sal-gate,.bx-final) :is(p,small,label){color:#f1eeff}
.foot-promo small{color:#ece8ff}
/* secondary grey text: 4.5:1 on white and the soft panels */
:root{--ink-3:#67637e}
[data-theme=dark]{--ink-3:#9692ae}
/* gains, losses and status chips readable on white */
.mf-t td.pos,.mf-y .g{color:#047857}
.mf-t td.neg{color:#dc2626}
.b.f,.lip-kind.k-event{color:#15803d}
[data-theme=dark] .mf-t td.pos,[data-theme=dark] .mf-y .g{color:#34d399}
[data-theme=dark] .mf-t td.neg{color:#f87171}
[data-theme=dark] .b.f,[data-theme=dark] .lip-kind.k-event{color:#4ade80}
[data-theme=dark] .lip-kind.k-post{color:#fbbf24}
/* nav pill: the shine passes through a deep violet, never a pale lilac */
.nav-links .dd-btn.gx-btn{background-image:linear-gradient(110deg,#5b3df5 0%,#7c3aed 40%,#9333ea 50%,#7c3aed 60%,#5b3df5 100%)}
.nav-links .dd-btn.gx-btn:hover,.dd.mega.open>.dd-btn.gx-btn,.dd.mega:hover>.dd-btn.gx-btn{background-image:linear-gradient(110deg,#4a2fe0 0%,#6d28d9 40%,#9333ea 50%,#6d28d9 60%,#4a2fe0 100%)}
/* buttons inside article prose keep white text */
.cs-prose a.btn-primary,.pt-body a.btn-primary{color:#fff;text-decoration:none}
.cs-prose a.btn-ghost,.pt-body a.btn-ghost{text-decoration:none}
/* skill pack steps sit on a light card */
.sp-steps li{color:var(--ink)}
/* video placeholder text never sits on a white iframe while loading */
.vid-frame:not(.ready) iframe{background:transparent}
/* dark mode: filled accent controls carry white text, so the fill uses a deeper violet (5:1) */
[data-theme=dark] :is(.btn-primary,.skip,.bx-when,.fr-step>span,.cnt,.op-gate button,.fin-cta,.stn,.kh-ptag,.sp-buyall,button.on){--accent:#6e55f0}
.nl2-form small{color:var(--ink-3)}
[data-theme=dark] .nl2-form small{color:#5f5b75}
.fin-cta{background-image:linear-gradient(90deg,#5b3df5,#7c3aed,#5b3df5)}
.tool .tn span.b.f,.xd-meta .xd-now{color:#15803d}
[data-theme=dark] .tool .tn span.b.f,[data-theme=dark] .xd-meta .xd-now{color:#4ade80}
.mono[data-color="#0ea5a4"],.mono[style*="#0ea5a4"]{background:#0f766e!important}
.mfall{color:#fff}
.sal-ed{color:#9a4a09}
tr.on td.neg,.mf-t tr.on td.neg{color:#c81e1e}
[data-theme=dark] .lip-kind.k-reshare{color:#60a5fa}
[data-theme=dark] .lip-kind.k-video{color:#fb7185}
.page-hero .lede .serif-accent,.lede .serif-accent{color:#b9382f}
[data-theme=dark] .lede .serif-accent{color:#fb9a8f}
'''
