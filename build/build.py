# Created by: Claude
# Date: 2026-10-28
# Purpose: Build the workproof subpages for the Syed Hadi site
# Owner: Syed Hadi

import os
import sys

from partials import DECK, page

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")


def bars(rows):
    top = max(v for _, v, _ in rows)
    html = '<div class="bars">'
    for name, v, us in rows:
        html += (f'<div class="bar{" us" if us else ""}"><span>{name}</span>'
                 f'<div class="track"><div class="fill" style="width:{v / top * 100:.1f}%"></div></div>'
                 f'<em>{v}%</em></div>')
    return html + "</div>"


def cards(items, cls=""):
    html = f'<div class="cards {cls}">'
    for i, (h, p) in enumerate(items, 1):
        html += f'<div class="card reveal"><span class="n">{i:02d}</span><h3>{h}</h3><p>{p}</p></div>'
    return html + "</div>"


def block(eyebrow, h2, p, inner, date=None):
    d = f'<span class="date-tag">{date}</span>' if date else ""
    return f'''<section class="block">
  <div class="wrap">
    <div class="block-head reveal"><div>{d}<span class="eyebrow" style="display:block">{eyebrow}</span><h2 class="display" style="margin-top:8px">{h2}</h2></div><p>{p}</p></div>
    {inner}
  </div>
</section>'''


def metrics(items):
    return '<div class="metrics">' + "".join(
        f'<div class="metric reveal"><b>{b}</b><span>{s}</span></div>' for b, s in items) + "</div>"


# ---------- GTM ENGINE ----------
gtm = ""
gtm += block("Section 01, the new GTM toolkit", "Seven tools now sit around the classic stack",
             "Google, Gmail, Ads, WordPress, Analytics and Sheets still run the basics. The leverage comes from what got added around them.",
             '''<div class="compare">
  <div class="col reveal"><h3>THEN</h3><div class="chips"><span>Google Search</span><span>Gmail</span><span>Google Ads</span><span>Meta Ads</span><span>WordPress</span><span>Google Analytics</span><span>Excel and Sheets</span></div></div>
  <div class="col now reveal"><h3>NOW</h3><ul>
    <li><b>01</b>Cursor for building</li><li><b>02</b>Clay for enrichment and outbound</li><li><b>03</b>Lovable for landing pages</li>
    <li><b>04</b>Zapier for AI workflows</li><li><b>05</b>ChatGPT and Claude for research and thinking</li>
    <li><b>06</b>PostHog for what users actually do</li><li><b>07</b>Searchable for AI search visibility</li></ul></div>
</div>''', "19 AUG 2026")
gtm += block("Stack growth", "The GTM stack grew six times in a decade",
             "Ten years ago five tools were enough. Today a GTM strategist runs more than thirty and still feels something is missing.",
             metrics([("5", "Tools a decade ago. Excel, PowerPoint, Salesforce, Sales Navigator, Mailchimp."),
                      ("32", "Tools today, from Claude Code and Clay to Gong, n8n and PostHog."),
                      ("6x", "Growth in the strategist's toolkit"),
                      ("5", "Buckets in modern GTM")]))
gtm += block("Revenue growth toolkit", "Modern GTM has five buckets",
             "Marketing and Sales own two. GTM Engineering and RevOps own the other three.",
             cards([("Inbound, Marketing", "Paid, SEO and GEO, social and events."),
                    ("Outbound, Sales", "Data, web, calls and WhatsApp."),
                    ("Lead capture, RevOps", "Website, social signals, CRM and booking."),
                    ("Data and orchestration, RevOps", "Enrich, add context and sources, orchestrate and analyze."),
                    ("Agentic operations, GTM Engineering", "Coding agents, unified APIs and where they run."),
                    ("The longer funnel", "Before AI it was run ads, drive traffic, convert. Now discovery, trust and agentic readiness sit in between.")]))
gtm += block("Section 02, AI search and inbound growth", "Ranking ahead of Sysdig, Lacework and Fortinet",
             "Four to six months of SEO, SEM, meta tags and backlinks put AccuKnox in the Google answer for CNAPP vendors, above much larger names. The CEO called it out in a note to the whole company.",
             metrics([("4 to 6", "Months of SEO, SEM and backlink work"),
                      ("#1", "Google answer slot for CNAPP vendors"),
                      ("2x", "AccuKnox citations in the AI Overview for stateful prompt firewall"),
                      ("5", "Languages our site assistant answers AI SOC questions in")]),
             "11 JUN 2025")
gtm += block("Inbound engines", "Eleven engines feed inbound",
             "Each engine turns one trigger into pages, posts or sales assets on a repeatable cadence.",
             cards([("Competitive content", "vs X and alternatives pages"),
                    ("Content refresh", "Old blogs update when relevant news breaks"),
                    ("ToFu and MoFu answers", "Concise answers built to win AI Overviews"),
                    ("How to guides", "Persona and industry guides at scale"),
                    ("Rapid response", "Same day POV blog when a zero day hits"),
                    ("ABM account pages", "A tailored page per target account"),
                    ("Industry pages", "Vertical pages with the right threat model"),
                    ("Social repurposing", "Every blog and CVE turned into LinkedIn posts"),
                    ("Competitive intel", "Analyst reports turned into narrative briefs"),
                    ("Vuln database", "Programmatic CVE pages enriched with reachability"),
                    ("Sales enablement", "Recurring objections turned into battlecards")], "four"))
gtm += block("SEO content matrix", "23 content types build hundreds of SEO and AI pages",
             "Thirteen formats drive traffic. Ten drive AI visibility and conversions. All of them build authority, an SEO and AI moat, and coverage at every funnel stage.",
             '''<div class="compare">
  <div class="col reveal"><h3>13 DRIVE TRAFFIC</h3><div class="chips"><span>Lists</span><span>FAQs</span><span>Steps</span><span>Interviews</span><span>Checklists</span><span>Definitions</span><span>Pillar pages</span><span>Infographics</span><span>Press releases</span><span>Ultimate guides</span><span>Trending content</span><span>Beginner's guides</span><span>Tips and best practices</span></div></div>
  <div class="col now reveal"><h3>10 DRIVE AI VISIBILITY AND CONVERSIONS</h3><div class="chips"><span>How to guides</span><span>Landing pages</span><span>Product pages</span><span>Best of posts</span><span>Comparisons</span><span>Case studies</span><span>Alternatives</span><span>Templates</span><span>Free tools</span><span>Reviews</span></div></div>
</div>''')
gtm += block("AI visibility", "Third in AI visibility, ahead of Sysdig and Prisma",
             "Share of AI answers that mention each brand across the security category, tracked on LLMLab from Nov 2025 to Aug 2026.",
             '<div class="compare"><div class="col reveal">' + bars([("Wiz", 36.1, False), ("Palo Alto Networks", 29.6, False), ("AccuKnox", 27.7, True), ("Sysdig", 18.7, False), ("Prisma Cloud", 18.2, False), ("Orca", 17.6, False), ("OWASP", 16.0, False), ("Microsoft", 14.7, False)]) +
             '</div><div class="col now reveal">' + metrics([("27.72%", "AI visibility"), ("12K", "of 42K answers mention us"), ("45K", "pages cited"), ("124K", "pages mentioning us")]).replace('class="metrics"', 'class="metrics" style="grid-template-columns:1fr 1fr"') + '</div></div>')
gtm += block("Traffic and social", "Website sessions up 240% in 90 days",
             "Google Analytics 4, May to Aug 2026 against the previous period, plus LinkedIn and YouTube from March to July 2026.",
             metrics([("311K", "Sessions, up 240.6%"), ("350K", "Views, up 199.2%"), ("307K", "Engaged sessions, up 253.1%"), ("4.4", "Average rating across 85 customer reviews"),
                      ("9.41%", "LinkedIn engagement rate in July"), ("193K", "LinkedIn post impressions"), ("63.6K", "LinkedIn followers, 1,331 new"), ("57", "YouTube videos published")]))

# ---------- SYSTEMS ----------
sysb = ""
sysb += block("Section 03, systems we built", "Mission Control, one hub for every GTM tool",
              "Vibe coded in Lovable. The most used tools in marketing, sales and partner ops sit behind one front door.",
              cards([("Socials", "Email and LinkedIn post schedule"),
                     ("Content distribution", "Checklist for videos, blogs and gated assets"),
                     ("Inbound leads and growth", "Inbound pipeline and growth signals"),
                     ("LeadZap", "Event lead collection and capture"),
                     ("Spends", "Monthly and annual marketing spend"),
                     ("Pricing", "Generate pricing quotes quickly"),
                     ("RevOps tracker", "Revenue operations and pipeline"),
                     ("Customer cloud spends", "Automated cost reports of cloud usage"),
                     ("10xDevRel", "Playbooks and AI tools for product marketing"),
                     ("Sales and marketing collaterals", "One matrix of every sales and marketing asset"),
                     ("Login helper", "Share login instructions with the team"),
                     ("Partner ops", "Partner activities, engagement and revenue")], "four"))
sysb += block("Marketing built, whole org uses", "Quotes that took days now take minutes",
              "Five apps from the marketing team that sales, finance and engineering now run on every week.",
              metrics([("10+", "Price quotes generated and shared with the Price Quote Generator"), ("Days to minutes", "Time to produce a quote"), ("5", "Org wide apps shipped by marketing"), ("1 pass", "AI auto branding for any XLS, PPT, PDF or Word file")]) +
              '<div style="height:16px"></div>' +
              cards([("One front door for sales", "A single sales page for every link a rep needs."),
                     ("Price Quote Generator", "Quotes without spreadsheet hassle."),
                     ("Spends tracker", "DevOps, frontend, backend, marketing and sales spend in one view."),
                     ("Event Leads app", "Intelligent lead collection and categorization."),
                     ("Marketing Distribution", "Team level swimlanes for templated systems."),
                     ("AI auto branding", "A generic comparison doc goes in, an AccuKnox branded one comes out.")]))
sysb += block("Agents that do the busywork", "Ask in plain language, get the file back",
              "Viktor.ai and Claude schedules run inside Slack. A request becomes a file, a draft or a report.",
              cards([("Video to Drive, email drafted", "A release video upload plus a three line review email, done and queued as a draft."),
                     ("90 day lead export in one message", "Leads across five gated pages built into a sheet from GA4 events, with three tracking gaps flagged.")], "two"), "AUG 2026")
sysb += block("Self driving analytics", "Every channel reports into one automated view",
              "Refreshed without a manual export, at Mach 2 speed.",
              '<div class="chips"><span>Brevo email</span><span>WordPress content mix</span><span>YouTube</span><span>LinkedIn page</span><span>LinkedIn paid ads</span><span>Website sessions</span></div>', "JAN TO JUL 2026")

# ---------- RECOGNITION ----------
rec = ""
rec += block("Section 04, campaigns", "Told to paint the town red. We painted it blue.",
             "Sales and marketing on one message. AI governance, LLM security and runtime protection ads, all in AccuKnox blue.",
             '<a class="btn btn-ghost reveal" href="https://www.linkedin.com/ad-library/search?accountOwner=accuknox" target="_blank" rel="noopener">See the live ads in the LinkedIn Ad Library</a>')
rec += block("One quarter", "12 live moments in a single quarter",
             "Webinars, offline events and an analyst session, supported end to end by the marketing team. Paid social and email ran as one program around them.",
             metrics([("8", "Webinars"), ("3", "Offline events"), ("1", "Analyst webinar"), ("12", "Live moments in one quarter")]))
rec += block("Analyst recognition", "Analysts are putting AccuKnox on the map",
             "Research mentions, awards and profiles across the major firms.",
             cards([("Gartner, 3 research mentions", "Emerging Tech Techscape 2025, Hardened Container Images 2026, State of AI for I&amp;O."),
                    ("Frost &amp; Sullivan, 2 awards in 2026", "Technology Innovation in Global AI Stack Security and Transformational Innovation in APAC Cloud Security."),
                    ("Omdia, vendor profile", "On the Radar, AccuKnox CNAPP, by Rik Turner, Nov 2025."),
                    ("KuppingerCole", "Positioned ahead of Aqua Security, Orca Security and Uptycs in the Leadership Compass."),
                    ("TAG", "AI Security 2.0 endorsement from Dr. Edward Amoroso, former AT&amp;T CSO."),
                    ("GigaOm", "Andrew Green joined Rahul Jadhav on stateful vs stateless AI prompt firewalls.")]) +
             '<div style="margin-top:24px"><a class="btn btn-primary" href="https://accuknox.com/analyst-recognition" target="_blank" rel="noopener">accuknox.com/analyst-recognition</a></div>')
rec += block("Community accolades", "Two years running at BSides Bangalore",
             "AccuKnox won the #1 Startup Award at the Security BSides Bangalore annual conference in 2025 and again in 2026, sharing the space with partners Netpoleon Bharat and Erasmith.",
             '<div class="gallery"><div class="shot wide reveal"><div class="ph"><img src="img/bsides-2026.jpg" alt="Team AccuKnox with the BSides Bangalore award at the booth" loading="lazy"></div><div class="body"><span class="date-tag">9 JUL 2026</span><h3>#1 Startup, again</h3><p>Back to back wins. The 2027 target is the hattrick.</p><span class="where">Security BSides Bangalore</span></div></div></div>')

# ---------- PLAYBOOK ----------
pb = ""
pb += block("Section 05, playbook", "The old B2B playbook is dead",
            "Share of effort by activity, old playbook against 2026.",
            '''<div class="compare">
  <div class="col reveal"><h3>WHAT'S OUT</h3><ul><li><b>45%</b>Focus on lead gen</li><li><b>30%</b>Send cold emails</li><li><b>20%</b>Lead gen ads, book a demo</li><li><b>5%</b>Lead magnets and nurture sequences</li><li><b>5%</b>Company updates</li></ul></div>
  <div class="col now reveal"><h3>WHAT'S IN, 2026</h3><ul><li><b>45%</b>Demand and intent</li><li><b>25%</b>Consistent content that builds awareness</li><li><b>15%</b>Signal based warm outbound</li><li><b>10%</b>Partnerships and personal brand collabs</li><li><b>5%</b>Retargeting ads that amplify what works</li></ul></div>
</div>''')
pb += block("Growth initiatives", "Six initiatives that drive revenue", "Each one turns people the company already has into distribution.",
            cards([("Partner led marketing", "Turn partners into a distribution channel."),
                   ("Employee led marketing", "Activate internal advocates."),
                   ("Video led marketing", "Shift toward the fastest growing content format."),
                   ("Founder led marketing", "Build trust through leadership visibility."),
                   ("Community and social listening", "Show up where technical buyers already are."),
                   ("LinkedIn GTM and dark funnel", "Treat LinkedIn as an outbound growth engine.")]))
pb += block("Become a super human", "Broken systems leak. Good systems compound.",
            "Broken systems demand 10x effort for 0.1x output. Good systems flip it. This is the stack that makes the flip.",
            cards([("Claude", "Think deeper. Get better answers."), ("Granola", "Chat in any meeting. Extract what matters."),
                   ("Viktor", "Automate on Slack. Get things done."), ("Lovable", "Custom apps and dashboards."),
                   ("Wispr Flow", "Voice to text dictation anywhere."), ("Textblaze", "Snippets for repetitive typing.")]))
pb += block("Agent architecture", "How an agent layer runs the revenue workflow",
            "Capture, act, record, surface. The agent layer does the busywork between them.",
            cards([("Capture", "Client and partner email, meeting recordings and transcripts, Slack requests."),
                   ("Agent layer", "AgentZ and Viktor summarize, update the CRM, create tasks and escalate."),
                   ("System of record", "Attio for deals, partners and notes. Linear for SE tasks and SLA clocks."),
                   ("Surface in Slack", "Daily brief at 07:30, SLA nudges, overdue escalations, Monday pipeline digest.")], "four"))
pb += block("The role", "A PMM lead's job in 2026", "As AI gives you more levers, the expected skill set expands with it.",
            cards([("Know what is trending in AI", "Tools, video led content and Claude automations."),
                   ("Turn founder vision into plans", "Articulate strategy and tactics the team can run."),
                   ("Own positioning", "Stand out from the noise and build the brand."),
                   ("Unify the language", "Get the whole organization saying the same thing."),
                   ("Translate the technical", "Turn engineering speak into content buyers want."),
                   ("Hire AI forward people", "High agency and coachable."),
                   ("Feed the team ideas", "Inspiration on a steady cadence."),
                   ("Find new ways to reach ICP", "Reddit, internal champions and beyond."),
                   ("Hit the numbers", "MQLs, attribution, CPL, CAC and LTV."),
                   ("Smooth the handoff", "Marketing to sales, the hard part."),
                   ("Build a personal brand", "A LinkedIn presence that becomes an MQL funnel."),
                   ("See across the org", "Pattern recognition from every team.")], "four"))

# ---------- EVENTS ----------
ev = [
    ("gtm-deep-dive", "3 OCT 2026", "GTM Deep Dive at GrowthX", "A hands on simulation. Teams picked positioning, ICP, pricing, channels and a launch plan, then defended them to the room.", "GrowthX, Bengaluru", True),
    ("cncf-netapp", "27 AUG 2026", "CNCF community day at NetApp", "An open source session with NetApp and the KubeArmor community on securing AI workloads on Kubernetes, plus the AgentZ introduction.", "NetApp, Bengaluru", False),
    ("agentz-launch", "29 JUL TO 21 AUG 2026", "AgentZ launch", "Featured in the AgentZ launch video, then published a long form piece on building, running and governing real AI agents.", "AccuKnox", False),
    ("delhi-ncr", "23 JUL 2026", "Business expansion into Delhi NCR", "Face to face customer and partner meetings across Delhi, Gurugram and Noida with the India sales director and distributor Netpoleon Bharat.", "Delhi, Gurugram, Noida", False),
    ("bsides-2026", "9 JUL 2026", "#1 Startup at BSides Bangalore, again", "AccuKnox won the #1 Startup Award for the second year in a row, sharing the booth with partners Netpoleon Bharat and Erasmith.", "Security BSides Bangalore", True),
    ("kubecon-india", "19 JUN 2026", "Team AccuKnox at KubeCon India", "A Mumbai booth plus a KubeArmor CTF. 500+ CTF sign ups, 100+ CTF hackers and 300+ new GitHub stars.", "KubeCon India, Mumbai", False),
    ("marketing-after-hours", "5 MAY 2026", "Spoke at Marketing After Hours", "Walked the room through the AccuKnox inbound engine, a $2M a year pipeline built with Factors.ai and account based intelligence.", "Marketing After Hours, Bengaluru", False),
]
gal = '<div class="gallery">'
for img, d, h, p, where, wide in ev:
    gal += (f'<div class="shot{" wide" if wide else ""} reveal"><div class="ph"><img src="img/{img}.jpg" alt="{h}" loading="lazy"></div>'
            f'<div class="body"><span class="date-tag">{d}</span><h3>{h}</h3><p>{p}</p><span class="where">{where}</span></div></div>')
gal += "</div>"
evb = block("Section 07, a year on LinkedIn", "Six events, talks and meetups in 2026",
            "From a stage at Marketing After Hours to hosting the GrowthX community. Every photo is from the workproof deck.",
            metrics([("20", "Posts and long form articles"), ("6", "Events, talks and meetups"), ("#1", "Startup at BSides BLR, second year running"), ("5", "Times tagged or featured by others")]) + '<div style="height:32px"></div>' + gal)
evb += block("Coming up", "Next on the calendar", "Register on LinkedIn.",
             cards([("Find It, Fix It, Prove It", "AccuKnox and DXR Cyber on mapping pen test findings to ASPM, CWPP and runtime enforcement. LinkedIn Live, 12 Nov 2026.")], "two"))

# ---------- WRITING ----------
arts = [("18 JUN", "Why Static BOMs Will Fail the Next Audit"),
        ("18 JUN", "The Most Expensive CNAPP Mistake, Visibility vs Protection"),
        ("21 JUN", "CERT-In's 6 Hour Rule Is a Telemetry Problem"),
        ("24 JUN", "Is Your Prompt Firewall Stateless?"),
        ("1 JUL", "Shadow AI Is a Control Plane Failure"),
        ("1 JUL", "AppSec Has a Prioritization Problem, Not a Scanner Problem"),
        ("21 JUL", "AI SOC Is Not a Better Queue"),
        ("23 JUL", "Config Drift Is Not a CSPM Afterthought"),
        ("21 AUG", "AgentZ, Build, Run and Govern Real AI Agents"),
        ("OCT", "AI Agents Do Not Need More Permissions, They Need Non Human Identity Boundaries")]
al = '<div class="article-list">' + "".join(
    f'<a class="reveal" href="https://www.linkedin.com/today/author/syedhadii" target="_blank" rel="noopener"><span class="d">{d} 2026</span><h3>{t}</h3><span>&rarr;</span></a>' for d, t in arts) + "</div>"
wr = block("Long form", "10 articles in under 100 days",
           "Security architecture through a GTM lens. What buyers worry about, written for the people who sell to them.", al)
wr += block("Featured", "Profiled by Humans of Marketing",
            "The path from project manager in 2021 to leading seven marketers and a $100K annual budget, and the case for making B2B marketing more human.",
            '<a class="btn btn-primary reveal" href="https://www.linkedin.com/in/syedhadii/recent-activity/all/" target="_blank" rel="noopener">Read the posts on LinkedIn</a>', "1 OCT 2026")

SUB = [
    ("gtm", "gtm-engine.html", "GTM Engine | Syed Hadi", "The AI native GTM engine behind AccuKnox inbound growth, AI search visibility and traffic.",
     "GTM Engine", 'Building an <span>AI native</span> GTM engine', "How marketing changed, the stack we mapped to keep pace, and the AI search work that turned visibility into pipeline.", gtm),
    ("systems", "systems.html", "Systems | Syed Hadi", "Vibe coded apps, agents and dashboards the whole AccuKnox org runs on.",
     "Systems", 'Systems the <span>whole company</span> runs on', "Apps, agents and dashboards built by the marketing team and used across sales, finance and engineering.", sysb),
    ("recognition", "recognition.html", "Recognition | Syed Hadi", "Campaigns, live moments and analyst recognition for AccuKnox.",
     "Recognition", 'Campaigns and <span>recognition</span>', "Ads, webinars, events and the analysts who noticed.", rec),
    ("playbook", "playbook.html", "Playbook | Syed Hadi", "What is out, what is in, and how to build B2B marketing systems that stop the leaks.",
     "Playbook", 'Playbook and <span>recommendations</span>', "What is out, what is in, and how to build systems that stop the leaks.", pb),
    ("events", "events.html", "Events | Syed Hadi", "Events, talks and meetups from 2026, with photos.",
     "Events", 'Rooms I have <span>filled</span>', "Stages, booths, meetups and community days from 2026.", evb),
    ("writing", "writing.html", "Writing | Syed Hadi", "Long form articles on AI security, AppSec and compliance through a GTM lens.",
     "Writing", 'Notes and <span>essays</span>', "Ten long form articles in under a hundred days, published on LinkedIn.", wr),
]

try:
    for key, fn, title, desc, eb, h1, p, body in SUB:
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(page(key, title, desc, eb, h1, p, body))
        print("wrote", fn)
except OSError as e:
    sys.exit(f"Build failed writing pages: {e}")
