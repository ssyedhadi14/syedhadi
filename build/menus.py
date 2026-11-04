# Created by: Claude
# Date: 2026-10-31
# Purpose: Image led Work and Tools mega menus with growth quotes (imported by transform.build_nav)
# Owner: Syed Hadi
from shared import CHEV, uns

CHEV_R = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>'

WORK = [
    ("pmm", "Product Marketing", "Positioning buyers repeat", "/gtm-engine",
     "/img/li/four-years-accuknox.jpg", "Syed at the AccuKnox booth in front of the Zero Trust Security screen",
     "Make a technical product easy to buy.", ["Positioning sales uses", "Personas mapped to objections", "Launches that land"],
     "People do not buy what you do, they buy why you do it.", "Simon Sinek",
     "/img/li/future-of-gtm-2026-event.jpg", "A product story the whole company tells the same way", "Part of a 0 to $10M hypergrowth journey.", "See the GTM engine"),
    ("partner", "Channel Partnerships", "Partners who sell, not sign", "/recognition",
     "/img/li/india-devsec-show-2025.jpg", "Receiving recognition on stage at India DevSec Show 2025",
     "Partners who bring pipeline, not logos.", ["Programs live in 8 regions", "Enablement partners use", "Deal registration that works"],
     "If you want to go fast, go alone. If you want to go far, go together.", "African proverb",
     "/img/li/delhi-ncr-expansion-2026.jpg", "Distributors, MSSPs and resellers that close", "India, MENA, APAC, Japan, Europe, Africa and the US.", "See the partner wins"),
    ("gtm", "GTM Strategy", "Decisions under market pressure", "/playbook",
     "/img/li/gtm-deep-dive-growthx-2026.jpg", "GTM Deep Dive workshop with GrowthX in Bengaluru",
     "Which segment, which motion, which message.", ["ICP before channels", "One message, every team", "Pricing that signals value"],
     "Strategy is about making choices, trade offs. It is about deliberately choosing to be different.", "Michael Porter",
     "/img/li/gtm-meetup-growthx-poster.jpg", "The B2B playbook, free", "Frameworks from launches, partner programs and pipeline math.", "Open the playbook"),
    ("pipe", "Demand and Pipeline", "Spend tied to one number", "/gtm-engine",
     "/img/li/marketing-after-hours-inbound-engine.jpg", "Speaking about the inbound engine at Marketing After Hours",
     "Every rupee reported against pipeline.", ["$2M pipeline on $25K a quarter", "Outbound, events, content as one loop", "Weekly pipeline view"],
     "The aim of marketing is to make selling superfluous.", "Peter Drucker",
     "/img/li/engineering-team-meet.jpg", "An inbound engine that compounds", "Built with the engineering team, not around it.", "See how it runs"),
    ("comm", "Community and Events", "Rooms full of practitioners", "/events",
     "/img/li/cncf-netapp-bengaluru-2026.jpg", "Hosting the CNCF community day at NetApp Bengaluru",
     "Stages and rooms that turn into pipeline.", ["KubeCon, BSides, Black Hat", "CNCF and KCD meetups", "Talks, booths, webinars"],
     "Alone we can do so little, together we can do so much.", "Helen Keller",
     "/img/li/kcd-kochi-2024.jpg", "Rooms I have filled", "From the first KCD in Kerala to KubeCon India.", "See every event"),
    ("ai", "AI Systems for GTM", "Busywork, automated", "/systems",
     "/img/li/kubecon-india-mumbai-2026.jpg", "Demoing the AccuKnox platform with the team at KubeCon India, Mumbai 2026",
     "Agents that run the GTM machine while the team sells.", ["Claude skills for marketers", "Scheduled research agents", "Scorecards that update themselves"],
     "The best way to predict the future is to invent it.", "Alan Kay",
     "/img/li/bsides-2026-startup-award.jpg", "The systems behind the pipeline", "Eight Claude skills, packaged, plus the agents I run daily.", "See the systems"),
]
# object-position per image so wide crops keep faces in frame
FOCAL = {
    "/img/li/four-years-accuknox.jpg": "50% 28%", "/img/li/future-of-gtm-2026-event.jpg": "50% 38%",
    "/img/li/india-devsec-show-2025.jpg": "50% 30%", "/img/li/delhi-ncr-expansion-2026.jpg": "50% 72%",
    "/img/li/gtm-deep-dive-growthx-2026.jpg": "50% 45%", "/img/li/gtm-meetup-growthx-poster.jpg": "50% 22%",
    "/img/li/marketing-after-hours-inbound-engine.jpg": "50% 40%", "/img/li/engineering-team-meet.jpg": "50% 32%",
    "/img/li/cncf-netapp-bengaluru-2026.jpg": "50% 55%", "/img/li/kcd-kochi-2024.jpg": "50% 45%",
    "/img/li/kubecon-india-mumbai-2026.jpg": "50% 34%", "/img/li/bsides-2026-startup-award.jpg": "50% 30%",
}


def fp(img):
    return ' style="object-position:%s"' % FOCAL[img] if img in FOCAL else ""


ICONS = {
    "pmm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>',
    "partner": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/></svg>',
    "gtm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18M7 14l4-4 4 4 5-6"/></svg>',
    "pipe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4h18l-7 8v6l-4 2v-8z"/></svg>',
    "comm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20a6 6 0 0 1 12 0M14 19a4.5 4.5 0 0 1 7 0"/></svg>',
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 3v4M9 13h.01M15 13h.01M9 17h6"/></svg>',
}


def work_menu():
    left = ""
    panels = ""
    for i, (k, title, sub, href, img, alt, line, chips, quote, who, img2, h4, p2, cta) in enumerate(WORK):
        on = " on" if i == 0 else ""
        left += ("<a class='mw-item%s' data-k='%s' href='%s'><span class=\"mw-ic\">%s</span>"
                 "<span class=\"mw-t\"><b>%s</b><small>%s</small></span>%s</a>" % (on, k, href, ICONS[k], title, sub, CHEV_R))
        ch = "".join("<span>%s</span>" % c for c in chips)
        panels += ('<div class="mw-panel%s" data-k="%s"><div class="mw-mid mw-mid2">'
                   '<a class="mw-photo" href="%s"><img src="%s" alt="%s" width="640" height="360" loading="lazy" decoding="async"%s>'
                   '<span class="mw-ph-t"><span class="mw-ic big">%s</span><span><b>%s</b><em>%s</em></span></span></a>'
                   '<div class="mw-chips">%s</div>'
                   '<blockquote class="mw-quote"><p>%s</p><cite>%s</cite></blockquote></div>'
                   '<a class="mw-card mw-card2" href="%s"><span class="k">WHAT TO EXPECT</span><span class="art art-img"><img src="%s" alt="" width="480" height="300" loading="lazy" decoding="async"%s></span>'
                   '<h4>%s</h4><p>%s</p><span class="go">%s <span>&rarr;</span></span></a></div>'
                   % (on, k, href, img, alt, fp(img), ICONS[k], title, line, ch, quote, who, href, img2, fp(img2), h4, p2, cta))
    simple = '<div class="mm-simple">' + "".join("<a href='%s'>%s</a>" % (w[3], w[1]) for w in WORK) + "</div>"
    return ('<div class="dd mega" data-group="work">\n        <button class="dd-btn" aria-haspopup="true" aria-expanded="false" data-group="work">Work %s</button>\n'
            '        <div class="dd-menu mm mm-work"><div class="mw-left">%s</div><div class="mw-right">%s</div></div>\n        %s\n      </div>' % (CHEV, left, panels, simple))


TOOLS_CARDS = [
    ("/tools", "tools", "Tool Directory", "30 GTM tools in 9 categories, with how each one earns its seat.", "1531403009284-440f080d1e12", "Laptop with marketing dashboards on a desk", "Browse tools", "FEATURED"),
    ("/jobs", "jobs", "Job Board", "Product marketing, GTM and partnerships roles in India, updated weekly.", "1521737711867-e3b97375f902", "Team in a bright meeting room", "See the roles", ""),
    ("/pmm-salary-2026", "salary", "PMM Salary 2026", "India benchmarks by title, experience and city, with the PDF guide.", "1553729459-efe14ef6055d", "Hand holding a growing stack of coins", "Check your number", "GUIDE"),
]
TOOLS_LINKS = [("/tools#cat-1", "AI and Agents"), ("/tools#cat-2", "Sales and Outbound"), ("/tools#cat-4", "SEO and AI Visibility"), ("/tools#cat-6", "Design and Creative"),
               ("/skill-pack", "Claude Skill Pack"), ("/blog", "Blog"), ("/posts", "LinkedIn Posts"), ("/insights", "Insights"), ("/about", "About me"), ("/schedule-meeting", "Schedule meeting")]


def tools_menu():
    cards = ""
    for href, key, title, desc, pid, alt, cta, badge in TOOLS_CARDS:
        b = '<span class="badge-f">%s</span>' % badge if badge else ""
        cards += ("<a class='pf-card pf-photo' data-p='%s' href='%s'><span class=\"pf-img\">%s<img src=\"%s\" alt=\"%s\" width=\"560\" height=\"340\" loading=\"lazy\" decoding=\"async\"></span>"
                  "<span class=\"pf-body\"><b>%s</b><small>%s</small><em>%s &rarr;</em></span></a>" % (key, href, b, uns(pid, 560, 340), alt, title, desc, cta))
    links = "".join("<a href='%s'>%s</a>" % (h, t) for h, t in TOOLS_LINKS)
    simple = '<div class="mm-simple">' + "".join("<a href='%s'>%s</a>" % (c[0], c[2]) for c in TOOLS_CARDS) + "".join("<a href='%s'>%s</a>" % (h, t) for h, t in TOOLS_LINKS[:4]) + "</div>"
    return ('<div class="dd mega" data-group="tools">\n        <button class="dd-btn" aria-haspopup="true" aria-expanded="false" data-group="tools">Tools %s</button>\n'
            '        <div class="dd-menu mm mm-port mm-tools"><div class="pf-grid pf-grid3">%s</div>\n'
            '        <div class="pf-foot"><blockquote class="mw-quote pf-quote"><p>Give me six hours to chop down a tree and I will spend the first four sharpening the axe.</p><cite>Attributed to Abraham Lincoln</cite></blockquote><div class="pf-links pf-links2">%s</div></div></div>\n'
            '        %s\n      </div>' % (CHEV, cards, links, simple))
