#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-06
# Purpose: Build site/interview-prep.html, the interview prep hub for Bengaluru PMM, Partnerships and Sales roles:
#          coach chatbot, question bank, short videos, and resume plus cover letter builder.
#          Uses site/jobs.html as the page shell (nav, footer, newsletter) so the page matches the rest of the site.
# Owner: Syed Hadi
# Usage: python3 build/interview_prep.py
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "site"))
SLUG = "interview-prep"
URL = f"https://syedcreates.com/{SLUG}"
TITLE = "Interview Prep: PMM, Partnerships and Sales Jobs in Bengaluru"
DESC = ("Free interview prep for PMM, partnerships and sales roles in Bengaluru: AI mock interview coach, 30 questions "
        "with answers, short videos and a resume builder.")
E = html.escape

# ---------------------------------------------------------------- question bank
BANK = {
    "pmm": [
        {"q": "Walk me through a launch you owned end to end. What would you change?",
         "t": "Ownership, cross-functional leadership and whether you measure launches by outcomes, not activity.",
         "a": "Name the goal metric first (pipeline, adoption, win rate), then the 3 or 4 moves you made with product, sales and marketing, then the result with a number. Close with one honest change you would make next time.",
         "k": "launch go to market gtm"},
        {"q": "Position our product in one sentence for a CFO, then for an engineer.",
         "t": "Messaging range and whether you understand that different buyers care about different value.",
         "a": "For the CFO lead with money or risk (cost, audit, revenue). For the engineer lead with the job it removes and how it works. Same product, two outcomes, each under 20 words. Ask which persona owns the budget.",
         "k": "positioning messaging persona one liner"},
        {"q": "How would you build a competitive battlecard against our biggest competitor?",
         "t": "Sales enablement craft and research discipline.",
         "a": "Start from lost deals and seller interviews, not the competitor's website. Keep it to one page: when we win, when we lose, three landmines to set, objection handling, and proof points. Say how you would keep it fresh and measure use.",
         "k": "battlecard competitive enablement competitor"},
        {"q": "Our win rate fell from 25% to 18% in two quarters. Where do you look first?",
         "t": "Diagnostic thinking with data before opinions.",
         "a": "Segment the drop: by segment, deal size, region, competitor and stage where deals die. Read call notes for the losses. Then form two hypotheses, such as a new competitor or a pricing gap, and say how you would test each in 30 days.",
         "k": "win rate drop diagnose data analytics"},
        {"q": "How do you decide which segment or ICP to go after first?",
         "t": "Prioritisation and commercial judgement.",
         "a": "Score segments on pain intensity, ability to pay, ease of reach and product fit, using customer data you already have. Pick one beachhead, define how you would prove it in a quarter, and say what you would deliberately ignore.",
         "k": "icp segment target market prioritise"},
        {"q": "Tell me about a time sales ignored your messaging. What did you do?",
         "t": "Influence without authority and humility.",
         "a": "Use STAR. Show that you went to the field, sat in on calls, found out why the messaging did not land, rebuilt it with two top sellers, and measured adoption. The best answers admit what you got wrong.",
         "k": "sales alignment influence enablement conflict"},
        {"q": "How do you measure PMM impact when you do not own pipeline?",
         "t": "Whether you can tie your work to revenue honestly.",
         "a": "Give a small scorecard: influenced pipeline, win rate in target segments, sales cycle length, feature adoption after launch, and content usage by sellers. Explain how you set a baseline before you start.",
         "k": "metrics measure impact kpi pipeline"},
        {"q": "We want to launch a new pricing tier. How would you test it?",
         "t": "Pricing and packaging sense, plus risk management.",
         "a": "Start with willingness to pay interviews and win or loss data. Define who the tier is for and what is fenced in or out. Pilot with new deals in one segment, watch conversion, discounting and cannibalisation, then decide.",
         "k": "pricing packaging tier monetisation"},
        {"q": "Present a 30-60-90 day plan for this role.",
         "t": "Whether you learn before you change things, and what you will be judged on.",
         "a": "30 days: listen to 10 customers and 5 sellers, audit assets. 60 days: ship one visible win such as a refreshed pitch or battlecard. 90 days: own a metric and a roadmap. One slide per phase.",
         "k": "30 60 90 plan first 90 days"},
        {"q": "Pick a B2B SaaS product built in India that you admire. What makes its positioning work?",
         "t": "Product taste and whether you study the market you want to work in.",
         "a": "Choose a product you have actually used. Explain who it is for, the one problem it owns, how its message differs from global rivals, and one thing you would change. Specifics beat praise.",
         "k": "india saas product admire example"},
    ],
    "partnerships": [
        {"q": "How would you design a partner program for us from zero?",
         "t": "Structure, commercial sense and focus.",
         "a": "Start with the motion you need (resell, refer, co-sell or integrate) and the partner type that fits it. Keep tiers simple, define deal registration, margins or referral fees, enablement and joint plans. Name the first five partners and the 90 day goal.",
         "k": "partner program design tiers channel"},
        {"q": "When would you choose a channel partner, an alliance or a technology partner?",
         "t": "Whether you understand different partnership models.",
         "a": "Channel partners resell or deliver, so pick them when you need reach and services. Alliances (hyperscalers, big SIs) bring co-sell and credibility. Technology partners integrate, which drives retention and new use cases. Tie each to a revenue goal.",
         "k": "channel alliance technology isv si model"},
        {"q": "A partner signed six months ago and has sourced zero deals. What do you do?",
         "t": "Partner activation and honesty about bad fits.",
         "a": "Diagnose first: do their sellers know the product, is there an incentive, do they have the right customers? Run a joint account mapping, pick 10 target accounts, set a 60 day plan with named owners. If nothing moves, deprioritise and say so.",
         "k": "inactive partner activation zero deals"},
        {"q": "How do you avoid channel conflict with our direct sales team?",
         "t": "Rules of engagement and internal influence.",
         "a": "Clear deal registration with first in wins, defined territories or segments, and seller compensation that does not penalise partner deals. Review conflicts weekly with sales leadership and fix the rule, not just the deal.",
         "k": "channel conflict deal registration direct sales"},
        {"q": "Which partners would you go after first in India, and why?",
         "t": "Market knowledge and prioritisation.",
         "a": "Map partners by the buyer they already reach: SIs and MSSPs for enterprise, distributors for scale, hyperscaler marketplaces for procurement. Pick the two types that fit our ICP and deal size, and explain how each would make money with us.",
         "k": "india partners si mssp distributor marketplace"},
        {"q": "Walk me through a partnership you negotiated. What did you give up?",
         "t": "Negotiation skill and win-win thinking.",
         "a": "Set the context, both sides' goals, the terms that mattered (margin, exclusivity, commitments), and the trade you made to get the deal done. End with what the partnership produced.",
         "k": "negotiate negotiation terms deal"},
        {"q": "How do you measure partner success?",
         "t": "Whether you think in pipeline, not logos.",
         "a": "Partner sourced and influenced pipeline, closed revenue, time to first deal, percent of partners active in a quarter, certified people per partner, and win rate on partner deals versus direct.",
         "k": "partner metrics measure success kpi"},
        {"q": "How does co-selling with a hyperscaler such as AWS, Azure or Google Cloud work?",
         "t": "Cloud ecosystem fluency, often critical for SaaS partnerships roles.",
         "a": "Explain marketplace listings, private offers, how cloud sellers are motivated (consumption and quota credit), and the work needed to get their attention: a clear joint value story, referrals in their tools, and wins to point to.",
         "k": "aws azure gcp hyperscaler marketplace co sell"},
        {"q": "Tell me about a partner relationship that went badly.",
         "t": "Self-awareness and how you recover.",
         "a": "Pick a real one. Explain the early signal you missed, what you did once you saw it, and how you protected customers and the company. Share the rule you now follow.",
         "k": "failed partnership conflict lesson"},
        {"q": "You have 20 minutes: build the business case for a new partner.",
         "t": "Structured thinking under time pressure, a common case round.",
         "a": "Lay out the partner's customers and our overlap, the joint offer, a simple revenue model (deals per quarter times deal size times win rate), the investment needed, and risks. Recommend go or no-go with a pilot.",
         "k": "business case partner case study model"},
    ],
    "sales": [
        {"q": "Sell me this pen. Or sell me our product.",
         "t": "Whether you discover before you pitch.",
         "a": "Do not start with features. Ask two or three questions first: when did you last use a pen, what for, what went wrong. Then tie one benefit to their answer and ask for the close.",
         "k": "sell me this pen pitch"},
        {"q": "Walk me through your numbers last year: quota, attainment and pipeline.",
         "t": "Honesty and command of your own metrics.",
         "a": "Have the numbers ready: quota, attainment percent, deal count, average deal size, cycle length and pipeline coverage. If you missed, say why and what you changed. Never inflate, references get checked.",
         "k": "quota attainment numbers pipeline metrics"},
        {"q": "How do you run a discovery call?",
         "t": "Discovery depth and a repeatable process.",
         "a": "Name a framework such as MEDDICC or SPICED, then show it in action: confirm the pain and its cost, who decides and how, the timeline, and the next step agreed on the call. Give one example question per step.",
         "k": "discovery meddicc spiced bant qualification"},
        {"q": "Tell me about a deal you lost and why.",
         "t": "Learning from losses and honesty.",
         "a": "Pick a real loss. Say where it went wrong (single threaded, no champion, late to the real buyer), what you learned and how you now run deals differently.",
         "k": "lost deal loss lesson"},
        {"q": "A prospect went silent after a great demo. What do you do next?",
         "t": "Persistence with judgement.",
         "a": "Reach other people in the account, send something useful such as a short business case, and use a clear yes or no close: 'Should I close the file?' Show you would have set a dated next step before ending the demo.",
         "k": "ghosting follow up silent prospect"},
        {"q": "The buyer says your price is too high. How do you respond?",
         "t": "Objection handling and protecting value.",
         "a": "Do not discount first. Ask what they are comparing against, restate the cost of the problem, and trade value for value: longer term, smaller scope or faster payment in exchange for any price move.",
         "k": "price objection discount negotiation"},
        {"q": "How do you prioritise accounts in a new territory?",
         "t": "Planning and commercial focus.",
         "a": "Tier accounts by fit and signals (hiring, funding, tech stack, compliance needs), pick the top 30 for deep work, and run lighter sequences for the rest. Show weekly activity and pipeline targets.",
         "k": "territory planning account prioritisation"},
        {"q": "Give me a 60 second cold call.",
         "t": "Composure and a crisp opener.",
         "a": "Permission based opener, a reason for the call tied to their role, one sharp question about the problem, and a small ask for 20 minutes. Handle the first brush off calmly and keep it human.",
         "k": "cold call role play prospecting"},
        {"q": "Why sales, and why here?",
         "t": "Motivation and research on the company.",
         "a": "Give a specific reason you like selling (the problem solving, the scoreboard) and a specific reason for this company: its market, product or growth stage. Show you have researched their customers.",
         "k": "why sales motivation why this company"},
        {"q": "How do you work with SDRs, sales engineers and partners in a deal?",
         "t": "Team selling and multi-threading.",
         "a": "Show a real deal where you briefed the SE on the business pain, gave SDRs clear account feedback, and brought in a partner for credibility or delivery. Mention the result and how credit was shared.",
         "k": "team selling se sdr partner multi thread"},
    ],
}

GENERAL = [
    ("Tell me about yourself.", "Present, past, future in 90 seconds: your role and best result today, two steps that built the skills this role needs, and why this job is the obvious next step."),
    ("Why are you leaving your current role?", "Stay positive and forward looking: the scope, market or growth you want next. Never criticise your current employer."),
    ("What is your notice period?", "State it plainly and what is possible, such as 'officially 90 days, release at 45 to 60 is possible'. Ask whether they offer a notice buyout."),
    ("What is your expected CTC?", "Give a researched range for the role, split by fixed and variable, and ask about ESOPs and joining bonus. Avoid anchoring on your current pay."),
]

# Resume bullet ideas. [X] marks where a real number goes.
IDEAS = {
    "pmm": [
        "Launched [product] across [X] segments, adding [X] Cr pipeline in [X] quarters",
        "Rebuilt positioning and pitch for [segment], lifting win rate from [X]% to [X]%",
        "Built [X] battlecards and trained [X] sellers, cutting sales cycle by [X] days",
        "Ran [X] customer interviews to define the ICP, focusing spend on the top [X] accounts",
        "Led pricing and packaging for [tier], raising average deal size by [X]%",
        "Created the launch playbook used for [X] launches with product, sales and CS",
    ],
    "partnerships": [
        "Built a partner program from zero to [X] active partners in [X] months",
        "Sourced [X] Cr in partner pipeline and closed [X] deals through SIs and MSSPs",
        "Listed on [cloud] marketplace and closed [X] private offers worth [X]",
        "Ran joint account mapping with [X] partners, creating [X] co-sell opportunities",
        "Cut time to first partner deal from [X] to [X] days with a 30 day enablement path",
        "Negotiated a reseller agreement with [partner], opening [X] new markets",
    ],
    "sales": [
        "Closed [X] Cr ARR at [X]% of quota in FY[XX], ranked [X] of [X] reps",
        "Built [X]x pipeline coverage through outbound, partners and events",
        "Won [X] new logos in [segment], with an average deal size of [X]",
        "Shortened sales cycle from [X] to [X] days by multi-threading into finance and IT",
        "Expanded [account] from [X] to [X] ARR through a land and expand plan",
        "Booked [X] meetings a month as an SDR, converting [X]% to qualified pipeline",
    ],
}

DEFAULTS = {
    "pmm": {"s1l": "Product Marketing Skills", "s1": "Go-to-Market Strategy, Positioning and Messaging, Competitive Analysis, Product Launches, Sales Enablement, Market Research, Pricing and Packaging, Customer Journey Mapping",
            "s2l": "Digital Marketing Skills", "s2": "SEO, AEO, SEM, Marketing Automation, Content Marketing, Demand Generation, Web Analytics",
            "tools": "HubSpot, Salesforce, Google Analytics, Figma, Canva, Notion, ChatGPT, Claude"},
    "partnerships": {"s1l": "Partnerships Skills", "s1": "Partner Program Design, Channel and Reseller Management, Alliances, Co-Selling, Deal Registration, Joint Business Planning, Partner Enablement, Negotiation",
                     "s2l": "Business Skills", "s2": "Account Mapping, Pipeline Management, Forecasting, Stakeholder Management, Contract Negotiation",
                     "tools": "Salesforce, PRM, Crossbeam, AWS Marketplace, Azure Marketplace, HubSpot, Apollo"},
    "sales": {"s1l": "Sales Skills", "s1": "Prospecting, Discovery, MEDDICC, Solution Selling, Negotiation, Account Planning, Forecasting, Objection Handling",
              "s2l": "Business Skills", "s2": "Pipeline Management, Stakeholder Mapping, Territory Planning, CRM Hygiene, Presentations",
              "tools": "Salesforce, LinkedIn Sales Navigator, Apollo, Outreach, Gong, ZoomInfo"},
}


def _sample(role, highlight, yoe, edu, jobs, vol, certs, hobbies):
    d = DEFAULTS[role]
    return {"role": role, "name": "Your Name", "city": "Bengaluru, IN", "phone": "+91-98XXXXXXXX", "email": "you@email.com",
            "linkedin": "linkedin.com/in/yourname", "portfolio": "syedcreates.com", "highlight": highlight, "yoe": yoe,
            "env": "fast-paced B2B SaaS startups",
            "edu": [{"school": a, "degree": b, "city": c, "years": y} for a, b, c, y in edu],
            "jobs": [{"company": co, "city": ci, "roles": [{"title": t, "dates": dt, "bullets": "\n".join(bl), "tools": tl} for t, dt, bl, tl in roles]} for co, ci, roles in jobs],
            "vol": vol, "s1l": d["s1l"], "s1": d["s1"], "s2l": d["s2l"], "s2": d["s2"], "tools": d["tools"],
            "certs": "\n".join(certs), "hobbies": hobbies}


_VOL = {"org": "AIESEC", "city": "Chennai, IN", "title": "Project Volunteer", "dates": "Nov 2019 to Apr 2020",
        "bullets": "Managed the experience of 20+ global volunteers on exchange\nRan partner meetings with teams from 10+ countries"}

SAMPLE = {
    "pmm": _sample("pmm", "Pragmatic Institute PMC III and HubSpot Inbound Marketing certified", "6",
                   [("Example Business School", "MBA, Marketing", "Bangalore, IN", "2022 - 2024"), ("Example Engineering College", "BE, Computer Science", "Chennai, IN", "2014 - 2018")],
                   [("Example SaaS Co.", "Bangalore, IN", [
                       ("Senior Product Marketing Manager", "Apr 2024 to Present",
                        ["Pipeline: Drive 4.2 Cr influenced pipeline a year on a 60 L marketing budget",
                         "Positioning: Rebuilt the mid-market pitch with 4 top sellers, lifting win rate from 19% to 27%",
                         "Enablement: Built 6 battlecards used in 70% of late stage deals",
                         "Leadership: Lead a team of 4 across content, design and web"], "HubSpot, Salesforce, Gong, Figma, WordPress"),
                       ("Product Marketing Manager", "Jun 2021 to Mar 2024",
                        ["Launched 3 modules across 2 regions with product, sales and customer success",
                         "Ran 40 customer interviews to redefine the ICP, focusing outbound on 300 accounts"], "HubSpot, Google Analytics, Canva")]),
                    ("Earlier Startup", "Chennai, IN", [
                        ("Marketing Associate", "Jul 2018 to May 2021",
                         ["Grew organic traffic from 8K to 45K monthly visits in 18 months", "Wrote 60+ blogs and 12 case studies used in sales cycles"], "")])],
                   _VOL, ["Pragmatic Institute PMC III | Mar 2024", "HubSpot Inbound Marketing | Aug 2022", "Google Analytics Certification | May 2021"],
                   "Writing, Meetups, Reading, Cycling"),
    "partnerships": _sample("partnerships", "AWS Partner Accreditation (Business) and Certified Channel Partner Manager", "5",
                            [("Example Business School", "MBA, Strategy", "Bangalore, IN", "2018 - 2020")],
                            [("Example SaaS Co.", "Bangalore, IN", [
                                ("Partnerships Manager", "Jan 2023 to Present",
                                 ["Program: Built the partner program from zero to 24 active partners in 14 months",
                                  "Pipeline: Sourced 6.5 Cr partner pipeline and closed 18 deals through SIs and MSSPs",
                                  "Marketplace: Closed 9 AWS Marketplace private offers, cutting procurement by 3 weeks"], "Salesforce, Crossbeam, AWS Marketplace, HubSpot"),
                                ("Business Development Executive", "Jul 2020 to Dec 2022",
                                 ["Signed 12 reseller agreements across South India and the Middle East", "Ran quarterly joint business plans with the top 5 partners"], "Salesforce, Apollo")])],
                            {"org": "", "city": "", "title": "", "dates": "", "bullets": ""},
                            ["AWS Partner Accreditation, Business | Feb 2024", "Certified Channel Partner Manager | Sep 2023"], "Travel, Chess, Running"),
    "sales": _sample("sales", "MEDDICC certified, President's Club FY25", "5",
                     [("Example College", "BBA", "Bangalore, IN", "2017 - 2020")],
                     [("Example SaaS Co.", "Bangalore, IN", [
                         ("Enterprise Account Executive", "Feb 2023 to Present",
                          ["Quota: Closed 3.1 Cr ARR at 118% of quota in FY25, ranked 2 of 14 reps",
                           "New logos: Won 11 enterprise logos with an average deal size of 28 L",
                           "Cycle: Cut sales cycle from 110 to 78 days by multi-threading into finance and IT"], "Salesforce, Gong, LinkedIn Sales Navigator"),
                         ("Sales Development Representative", "Jul 2020 to Jan 2023",
                          ["Booked 22 meetings a month, converting 35% to qualified pipeline", "Promoted to AE in 18 months, first in the team"], "Apollo, Outreach")])],
                     {"org": "", "city": "", "title": "", "dates": "", "bullets": ""},
                     ["MEDDICC Certification | Jan 2024", "Sandler Foundations | Jun 2021"], "Cricket, Podcasts, Gym"),
}

# Short videos. Real YouTube Shorts found via search, plus longer explainers the site already features.
SHORTS = [
    ("iqj2yypW8ro", "Career coach", "The best format for \"tell me about yourself\""),
    ("6f4K-rdty5M", "Hunter Lopatin, REPS", "A company president shares his sales interview question"),
    ("E1tZN6lIrBs", "Hunter Lopatin, REPS", "\"Sell me this cup\", and why most people fail it"),
    ("a-AY9UsCw9o", "Hunter Lopatin, REPS", "The only way to get hired in sales"),
    ("NYtxQkVyetg", "Hunter Lopatin, REPS", "Why \"you'd be great at sales\" is a trap"),
    ("9U2uGk-aDRw", "Hunter Lopatin, REPS", "Why the best reps do not care if you buy"),
]
LONG = [
    ("NL-pmvydNe8", "Jeff Su", "What product marketers actually do"),
    ("C7dNExgqd5A", "Henry Wang", "Product marketing 101 with a Google PMM"),
    ("vVxbIMx-Js0", "Coach Erika", "Better than the STAR method, from a Google hiring manager"),
    ("lLpDWxrhhGI", "Warikoo Careers", "How to get a job at a GCC in 2026"),
    ("BmunilI6FXA", "Diksha Arora", "7 tips to negotiate a higher salary"),
    ("JFdv8Z8iuok", "upGrad", "How to negotiate salary after a job offer"),
]

LOOP = [
    ("Recruiter screen", "20 to 30 min", "Fit, notice period, CTC range, why you. Have a 90 second intro and your numbers ready."),
    ("Hiring manager", "45 to 60 min", "Your best two or three stories, how you think, what you would do first. Bring STAR stories with numbers."),
    ("Case or take-home", "2 to 5 days", "A launch plan, partner plan, territory plan or mock pitch, then a 30 to 45 minute presentation."),
    ("Cross-functional panel", "45 to 90 min", "Sales, product, CS or partner leaders test how you work with them. Ask how they measure you."),
    ("Leadership or founder", "30 to 45 min", "Judgement, ambition and culture fit. Have a point of view on the company's market."),
    ("Offer and HR", "1 to 2 weeks", "CTC split, ESOPs, notice buyout, references and background checks. Get everything in writing."),
]

BLR = [
    ("Notice periods are long", "60 to 90 days is common in Indian companies, and startups often want you sooner. Know your real notice period, whether early release is possible, and ask about a notice buyout before you accept."),
    ("CTC is more than the number", "Offers usually split into fixed pay, variable or OTE, joining bonus and ESOPs. Sales roles often carry a large variable share. Compare offers on fixed pay first. See the <a href=\"/pmm-salary-2026\">PMM Salary 2026 guide</a> for India bands."),
    ("ESOPs need four answers", "Ask for the vesting schedule and cliff, strike price, exercise window after you leave, and whether the company has ever run a buyback."),
    ("Know the company type", "GCCs and MNCs run structured, competency based loops. Funded startups lean on cases and founder rounds. Indian SaaS scale ups mix both. Tailor your stories to the type."),
    ("Ask about office days", "Many Bengaluru teams are hybrid. ORR, Whitefield, Koramangala, HSR and Manyata can mean very different commutes, so ask in the first call."),
    ("Referrals still win", "A referral from someone in the team usually beats a cold application. Find the hiring manager and a peer on LinkedIn, and apply the same day you ask."),
]

FAQ = [
    ("Is the interview prep coach free?", "Yes. The coach, question bank, videos and resume and cover letter builder are free, with no sign up."),
    ("Is my resume or chat stored anywhere?", "No. Resume and cover letter drafts stay in your browser, and are saved only if you press Save. Chat messages are sent to the AI model to get a reply and are not stored by this site."),
    ("Which roles does this guide cover?", "Product marketing (PMM), partnerships and alliances, and B2B SaaS sales roles such as SDR, BDR, account executive and enterprise AE, with a focus on Bengaluru."),
    ("How many interview rounds should I expect in Bengaluru?", "Most B2B SaaS loops run four to six stages: recruiter screen, hiring manager, a case or take-home, a cross-functional panel, a leadership or founder round, then the offer."),
    ("What happens if the AI coach is unavailable?", "The page switches to a built-in offline coach that still answers common questions, runs mock interviews and scores your answers with clear rules."),
    ("Can I download my resume as a PDF?", "Yes. Press Download PDF and choose Save as PDF in the print window. The layout is a single column built to pass ATS screens."),
]

# ------------------------------------------------------------------------ helpers
SVG_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'


def yt_card(vid, chan, title, short=False):
    alt = f"{title}, video thumbnail from {chan}"
    return (f'<article class="yt-card{" yt-short" if short else ""}"><div class="yt-frame" data-id="{vid}" data-title="{E(title)}" role="button" tabindex="0" '
            f'aria-label="Play: {E(title)} by {E(chan)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{E(alt)}" width="480" height="360" loading="lazy" decoding="async">'
            f'<span class="yt-play" aria-hidden="true"><span>{SVG_PLAY}</span></span></div>'
            f'<div class="yt-body"><small>{E(chan)}</small><b>{E(title)}</b></div></article>')


def bank_html():
    tabs, panels = [], []
    for i, (r, name) in enumerate((("pmm", "Product Marketing"), ("partnerships", "Partnerships"), ("sales", "Sales"))):
        on = i == 0
        tabs.append(f'<button type="button" role="tab" id="bt-{r}" data-role="{r}" aria-controls="bank-{r}" aria-selected="{"true" if on else "false"}" class="{"on" if on else ""}">{name}</button>')
        items = []
        for j, q in enumerate(BANK[r]):
            items.append(f'<details class="ip-q"{" open" if j == 0 else ""}><summary><span class="n">{j + 1:02d}</span><h3 class="qq">{E(q["q"])}</h3></summary>'
                         f'<div class="ip-qa"><p><b>What they are testing:</b> {E(q["t"])}</p><p><b>How to answer:</b> {E(q["a"])}</p>'
                         f'<button type="button" class="ip-practise" data-role="{r}" data-i="{j}">Practise this with the coach &rarr;</button></div></details>')
        panels.append(f'<div role="tabpanel" id="bank-{r}" aria-labelledby="bt-{r}" class="ip-bank-list"{"" if on else " hidden"}>{"".join(items)}</div>')
    return f'<div class="ip-tabs" role="tablist" aria-label="Choose a role" id="ipBankTabs" data-tabs>{"".join(tabs)}</div>{"".join(panels)}'


def schema():
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    graph = [
        {"@type": "Person", "@id": "https://syedcreates.com/#person", "name": "Syed Hadi", "url": "https://syedcreates.com/",
         "image": "https://syedcreates.com/img/syed-hadi-2026.jpg", "jobTitle": "Product Marketing and Partnerships Lead",
         "worksFor": {"@type": "Organization", "name": "AccuKnox", "url": "https://accuknox.com"},
         "sameAs": ["https://www.linkedin.com/in/syedhadii/", "https://ssyedhadi.medium.com/", "https://syedhadi.substack.com/", "https://www.youtube.com/@syed1228"]},
        {"@type": "WebPage", "@id": URL + "#page", "url": URL, "name": TITLE, "description": DESC,
         "isPartOf": {"@id": "https://syedcreates.com/#website"}, "author": {"@id": "https://syedcreates.com/#person"},
         "inLanguage": "en-IN", "primaryImageOfPage": "https://syedcreates.com/img/covers/og/interview-prep.jpg",
         "about": ["Job interview preparation", "Product marketing", "Partnerships", "B2B sales", "Bengaluru"],
         "dateModified": "2026-11-06"},
        {"@type": "WebApplication", "name": "Interview Prep Coach and Resume Builder", "url": URL + "#coach",
         "applicationCategory": "BusinessApplication", "operatingSystem": "Any, runs in the browser",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "author": {"@id": "https://syedcreates.com/#person"},
         "featureList": ["AI mock interview coach", "30 interview questions with answer guides", "Resume builder with PDF export", "Cover letter builder"]},
        {"@type": "FAQPage", "mainEntity": faq},
        {"@type": "ItemList", "name": "Interview prep videos", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"https://www.youtube.com/watch?v={v}", "name": t} for i, (v, c, t) in enumerate(SHORTS + LONG)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://syedcreates.com/"},
            {"@type": "ListItem", "position": 2, "name": "Interview Prep", "item": URL}]},
    ]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>'


CSS = r"""
@font-face{font-family:"SH Carlito";font-style:normal;font-weight:400;font-display:swap;src:url(/assets/fonts/carlito/carlito-regular.woff) format("woff")}
@font-face{font-family:"SH Carlito";font-style:normal;font-weight:700;font-display:swap;src:url(/assets/fonts/carlito/carlito-bold.woff) format("woff")}
@font-face{font-family:"SH Carlito";font-style:italic;font-weight:400;font-display:swap;src:url(/assets/fonts/carlito/carlito-italic.woff) format("woff")}
@font-face{font-family:"SH Carlito";font-style:italic;font-weight:700;font-display:swap;src:url(/assets/fonts/carlito/carlito-bolditalic.woff) format("woff")}
.ip-jump{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.ip-jump a{font-size:14px;font-weight:600;padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.ip-jump a:hover{border-color:var(--accent);color:var(--accent)}
.ip-sec{padding:72px 0;border-bottom:1px solid var(--line)}
.ip-sec.soft{background:var(--bg-soft)}
.ip-head{max-width:780px;margin:0 0 32px}
.ip-head p{color:var(--ink-2);margin-top:12px;font-size:17px;line-height:1.6}
.ip-loop{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;counter-reset:lp}
.ip-step{border:1px solid var(--line);background:var(--card);border-radius:16px;padding:20px}
.ip-step small{font-family:"JetBrains Mono",monospace;font-size:12px;letter-spacing:.08em;color:var(--accent)}
.ip-step h3{font-family:"Plus Jakarta Sans";font-size:19px;font-weight:700;margin:6px 0 4px}
.ip-step em{font-style:normal;font-size:13px;color:var(--ink-3)}
.ip-step p{font-size:15px;color:var(--ink-2);margin-top:8px;line-height:1.55}
/* coach */
.ip-coach{display:grid;grid-template-columns:300px 1fr;gap:20px;align-items:start}
.ip-side{border:1px solid var(--line);background:var(--card);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:16px;position:sticky;top:96px}
.ip-side h3{font-size:12px;font-family:"JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-weight:500;margin-bottom:8px}
.ip-chips{display:flex;flex-wrap:wrap;gap:6px}
.ip-chips button,.ip-tabs button{font:600 14px Inter,sans-serif;padding:9px 13px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer;min-height:40px}
.ip-chips button.on,.ip-tabs button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.ip-side select{width:100%;padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:500 14px Inter,sans-serif}
.ip-side .ip-note{font-size:13px;color:var(--ink-3);line-height:1.5}
.ip-chat{border:1px solid var(--line);background:var(--card);border-radius:18px;display:flex;flex-direction:column;min-height:560px;overflow:hidden;box-shadow:var(--shadow)}
.ip-chat-top{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 18px;border-bottom:1px solid var(--line)}
.ip-chat-top b{font-family:"Plus Jakarta Sans";font-size:16px}
.ip-badge{font:600 12px Inter,sans-serif;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.ip-badge.off{background:#fff4d6;color:#8a5a00}
[data-theme=dark] .ip-badge.off{background:#3a2e10;color:#ffd27a}
.ip-badge.on{background:#dcfce7;color:#166534}
[data-theme=dark] .ip-badge.on{background:#12351f;color:#86efac}
.ip-reset{font:600 13px Inter,sans-serif;background:none;border:0;color:var(--ink-3);cursor:pointer;padding:8px}
.ip-log{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:12px;max-height:520px;min-height:360px}
.ip-msg{max-width:88%;padding:12px 15px;border-radius:14px;font-size:15px;line-height:1.55}
.ip-msg p+p,.ip-msg p+ul,.ip-msg ul+p{margin-top:8px}
.ip-msg ul{padding-left:18px;margin-top:6px}
.ip-msg li{margin:3px 0}
.ip-msg a{color:var(--accent);text-decoration:underline}
.ip-msg.bot{background:var(--bg-soft);border:1px solid var(--line);align-self:flex-start;border-top-left-radius:4px}
.ip-msg.me{background:var(--accent);color:#fff;align-self:flex-end;border-top-right-radius:4px}
.ip-dots{display:inline-flex;gap:4px}
.ip-dots i{width:7px;height:7px;border-radius:50%;background:var(--ink-3);animation:ipd 1s infinite}
.ip-dots i:nth-child(2){animation-delay:.15s}.ip-dots i:nth-child(3){animation-delay:.3s}
@keyframes ipd{0%,80%,100%{opacity:.25}40%{opacity:1}}
.ip-quick{display:flex;flex-wrap:wrap;gap:6px;padding:0 18px 10px}
.ip-qp{font:500 13px Inter,sans-serif;padding:8px 12px;border-radius:999px;border:1px dashed var(--line);background:transparent;color:var(--ink-2);cursor:pointer;text-align:left}
.ip-qp:hover{border-color:var(--accent);color:var(--accent)}
.ip-form{display:flex;gap:8px;padding:12px;border-top:1px solid var(--line)}
.ip-form textarea{flex:1;resize:vertical;min-height:52px;max-height:220px;padding:12px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:400 15px/1.5 Inter,sans-serif}
.ip-form button{align-self:flex-end}
/* bank */
.ip-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.ip-bank-list{display:flex;flex-direction:column;gap:10px}
.ip-q{border:1px solid var(--line);background:var(--card);border-radius:14px;overflow:hidden}
.ip-q summary{display:flex;gap:14px;align-items:baseline;padding:16px 18px;cursor:pointer;list-style:none}
.ip-q summary::-webkit-details-marker{display:none}
.ip-q .n{font-family:"JetBrains Mono",monospace;font-size:13px;color:var(--accent)}
.ip-q .qq{font-family:"Plus Jakarta Sans";font-size:17px;font-weight:700;line-height:1.35;margin:0}
.ip-qa{padding:0 18px 18px 50px;font-size:15px;color:var(--ink-2);line-height:1.6}
.ip-qa p+p{margin-top:8px}
.ip-practise{margin-top:12px;font:600 14px Inter,sans-serif;color:var(--accent);background:var(--accent-soft);border:0;border-radius:10px;padding:9px 14px;cursor:pointer}
.ip-general{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:22px}
.ip-general div{border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--card)}
.ip-general h3{font-family:"Plus Jakarta Sans";font-size:16px;font-weight:700;margin-bottom:6px}
.ip-general p{font-size:14.5px;color:var(--ink-2);line-height:1.55}
/* shorts */
.yt-grid.yt-shorts{grid-template-columns:repeat(6,1fr);gap:14px}
.yt-short .yt-frame{aspect-ratio:9/16}
.yt-short .yt-frame img{width:100%;height:100%;object-fit:cover}
.yt-short .yt-body b{font-size:14px;line-height:1.35}
.ip-sub{font-family:"Plus Jakarta Sans";font-size:20px;font-weight:700;margin:40px 0 0}
/* builder */
.rs-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;align-items:start}
.rs-form{border:1px solid var(--line);background:var(--card);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:12px}
.rs-form label{display:flex;flex-direction:column;gap:5px;font-size:13px;font-weight:600;color:var(--ink-2)}
.rs-form input,.rs-form textarea,.rs-form select{padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:400 15px/1.45 Inter,sans-serif;width:100%}
.rs-form textarea{resize:vertical}
.rs-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rs-job{border:1px dashed var(--line);border-radius:14px;padding:12px 14px 14px;display:flex;flex-direction:column;gap:10px;margin:0}
.rs-job legend{font:600 12px "JetBrains Mono",monospace;letter-spacing:.1em;color:var(--ink-3);padding:0 6px;text-transform:uppercase}
.rs-jobact{display:flex;gap:8px;justify-content:flex-end}
.rs-jobact button,.rs-mini{font:600 13px Inter,sans-serif;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:9px;padding:8px 12px;cursor:pointer}
.rs-ai{color:var(--accent)!important;border-color:var(--accent)!important}
.rs-ideas{display:flex;flex-direction:column;gap:6px}
.rs-idea{display:flex;gap:8px;text-align:left;font:500 13.5px/1.4 Inter,sans-serif;border:1px solid var(--line);background:var(--bg);color:var(--ink-2);border-radius:10px;padding:8px 10px;cursor:pointer}
.rs-idea span{color:var(--accent);font-weight:700}
.rs-acts{display:flex;flex-wrap:wrap;gap:8px}
.rs-acts .btn{padding:11px 16px;font-size:14px}
.rs-side{position:sticky;top:96px;display:flex;flex-direction:column;gap:14px}
.rs-paper{background:#fff;color:#000;border:1px solid var(--line);border-radius:10px;padding:30px 32px;box-shadow:var(--shadow);min-height:520px;max-height:820px;overflow:auto}
.cv{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:"SH Carlito",Calibri,Carlito,Arial,sans-serif;font-size:12.5px;line-height:1.38;color:#000}
.cv a{color:#1155cc;text-decoration:underline}
.cv p{margin:0}
.cv-top{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}
.cv-name{font:700 25px/1.15 "SH Carlito",Calibri,Carlito,Arial,sans-serif;color:#1f56a3;margin:0 0 4px;letter-spacing:0}
.cv-port{display:flex;flex-direction:column;align-items:center;gap:4px;flex-shrink:0;font-size:1em}
.cv-qr{width:72px;height:72px;display:block}
.cv-h{font:700 14px "SH Carlito",Calibri,Carlito,Arial,sans-serif;text-transform:uppercase;letter-spacing:0;color:#000;border-bottom:1.3px solid #000;padding-bottom:2px;margin:16px 0 8px}
.cv-row{display:flex;justify-content:space-between;gap:12px}
.cv-row>span:last-child{text-align:right;white-space:nowrap}
.cv-sc{font-variant:small-caps;font-size:.92em}
.cv-blk{margin-bottom:9px}
.cv-co{margin-top:2px}
.cv-role.next{margin-top:8px}
.cv ul{padding-left:22px;margin:2px 0 0;list-style:disc}
.cv li{margin:1px 0}
.cv ol{padding-left:22px;margin:2px 0 0}
.cv ol li .cv-row>span:first-child{white-space:normal}
.cl-doc p{margin:0 0 10px}
.cv .cl-doc{margin-top:14px}
.rs-step{display:flex;align-items:center;gap:8px;font-family:"Plus Jakarta Sans";font-size:15px;font-weight:700;margin:6px 0 0}
.rs-step span{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;font-size:12px}
.rs-roleform{display:flex;flex-direction:column;gap:10px;padding-top:8px;border-top:1px dashed var(--line)}
.rs-edu{display:flex;flex-direction:column;gap:8px;padding-bottom:6px}
.rs-more{border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.rs-more summary{cursor:pointer;font-weight:700;font-size:14px}
.rs-more summary em{font-style:normal;font-weight:500;color:var(--ink-3);font-size:12.5px;margin-left:6px}
.rs-more[open]{display:flex;flex-direction:column;gap:10px}
.rs-check{border:1px solid var(--line);background:var(--card);border-radius:14px;padding:14px 16px;font-size:13.5px;color:var(--ink-2)}
.rs-check ul{list-style:none;margin-top:8px;display:flex;flex-direction:column;gap:6px}
.rs-check li{display:flex;flex-direction:column;gap:2px;padding-left:12px;border-left:3px solid #22c55e}
.rs-check li.warn{border-left-color:#f59e0b}
.rs-check em{font-style:normal;font-size:12.5px;color:var(--ink-3)}
.cl-out{width:100%;min-height:520px;padding:30px 32px;border-radius:10px;border:1px solid var(--line);background:#fff;color:#16141f;font:400 14.5px/1.6 Inter,Arial,sans-serif;resize:vertical;box-shadow:var(--shadow)}
.cl-meta{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--ink-3)}
.ip-blr{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ip-blr div{border:1px solid var(--line);border-radius:16px;padding:20px;background:var(--card)}
.ip-blr h3{font-family:"Plus Jakarta Sans";font-size:18px;font-weight:700;margin-bottom:8px}
.ip-blr p{font-size:15px;color:var(--ink-2);line-height:1.6}
.ip-blr a{color:var(--accent);text-decoration:underline}
.ip-faq{max-width:860px;display:flex;flex-direction:column;gap:10px}
.ip-faq details{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:16px 18px}
.ip-faq summary{cursor:pointer;font-family:"Plus Jakarta Sans";font-size:17px;font-weight:700}
.ip-faq p{margin-top:8px;color:var(--ink-2);line-height:1.6}
.ip-toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,20px);background:#16141f;color:#fff;padding:12px 18px;border-radius:12px;font-size:14px;opacity:0;pointer-events:none;transition:.25s;z-index:200;max-width:calc(100vw - 32px)}
.ip-toast.on{opacity:1;transform:translate(-50%,0)}
#ipPrint{display:none}
@media (max-width:1100px){.yt-grid.yt-shorts{grid-template-columns:repeat(3,1fr)}}
@media (max-width:980px){.ip-coach,.rs-wrap{grid-template-columns:1fr}.ip-side,.rs-side{position:static}.ip-loop,.ip-blr{grid-template-columns:1fr 1fr}}
@media (max-width:640px){.ip-sec{padding:52px 0}.ip-loop,.ip-blr,.ip-general,.rs-row{grid-template-columns:1fr}.yt-grid.yt-shorts{grid-template-columns:1fr 1fr}
 .ip-msg{max-width:94%}.ip-qa{padding-left:18px}.rs-paper{padding:22px 18px}.cl-out{padding:20px 18px}.ip-log{max-height:460px}}
@media print{
 html.ip-printing body>*:not(#ipPrint){display:none!important}
 html.ip-printing #ipPrint{display:block!important;background:#fff}
 html.ip-printing #ipPrint .cv{font-size:10.5pt;line-height:1.35}
 html.ip-printing #ipPrint .cv-name{font-size:21pt}
 html.ip-printing #ipPrint .cv-h{font-size:12pt}
 html.ip-printing #ipPrint .cv-qr{width:20mm;height:20mm}
 html.ip-printing #ipPrint .cv-blk,html.ip-printing #ipPrint .cv-role{break-inside:avoid}
 html.ip-printing #ipPrint a{color:#1155cc}
 @page{size:A4;margin:12mm 15mm}
}
"""


def build():
    shell = open(os.path.join(ROOT, "jobs.html"), encoding="utf-8").read()
    head_end = shell.index("</head>")
    head = shell[:head_end]
    # --- head: replace page specific meta
    head = re.sub(r"<title>.*?</title>", f"<title>{E(TITLE)}</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + E(DESC), head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + URL, head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head)
    for k in ("og:title", "twitter:title"):
        attr = "property" if k.startswith("og") else "name"
        head = re.sub(rf'(<meta {attr}="{k}" content=")[^"]*', lambda m: m.group(1) + E(TITLE), head)
    for k in ("og:description", "twitter:description"):
        attr = "property" if k.startswith("og") else "name"
        head = re.sub(rf'(<meta {attr}="{k}" content=")[^"]*', lambda m: m.group(1) + E(DESC), head)
    head = head.replace("/img/covers/og/jobs.jpg", "/img/covers/og/interview-prep.jpg")
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + "Walk in ready. Walk out hired. Interview prep, Bengaluru", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: schema(), head, count=1, flags=re.S)
    head += f"<style>{CSS}</style>\n"

    body = shell[head_end:]
    nav_end = body.index("</nav>") + len("</nav>")
    top = body[:nav_end]
    tail = body[body.index("</main>"):]
    tail = re.sub(r'<div class="wrap next-page">.*?</div>',
                  '<div class="wrap next-page"><a href=\'/jobs\'><small>PREVIOUS</small><b>&larr; Job Board</b></a>'
                  '<a class=\'right\' href=\'/pmm-salary-2026\'><small>NEXT</small><b>PMM Salary 2026 &rarr;</b></a></div>', tail, count=1, flags=re.S)
    data_js = ("<script>window.IP_BANK=" + json.dumps(BANK, ensure_ascii=False) + ";window.IP_IDEAS=" + json.dumps(IDEAS, ensure_ascii=False)
               + ";window.IP_SAMPLE=" + json.dumps(SAMPLE, ensure_ascii=False) + ";window.IP_DEFAULTS=" + json.dumps(DEFAULTS, ensure_ascii=False) + ";</script>\n"
               '<script src="/assets/qrcode.js?v=20261106a" defer></script>\n'
               '<script src="/assets/interview-prep.js?v=20261106c" defer></script>\n')
    tail = tail.replace("</body>", '<div id="ipPrint" aria-hidden="true"></div><div class="ip-toast" id="ipToast" role="status" aria-live="polite"></div>\n' + data_js + "</body>")

    loop = "".join(f'<div class="ip-step reveal"><small>ROUND {i + 1:02d}</small><h3>{E(n)}</h3><em>{E(d)}</em><p>{E(p)}</p></div>' for i, (n, d, p) in enumerate(LOOP))
    general = "".join(f"<div><h3>{E(q)}</h3><p>{E(a)}</p></div>" for q, a in GENERAL)
    shorts = "".join(yt_card(v, c, t, True) for v, c, t in SHORTS)
    longs = "".join(yt_card(v, c, t) for v, c, t in LONG)
    blr = "".join(f"<div class=\"reveal\"><h3>{E(h)}</h3><p>{p}</p></div>" for h, p in BLR)
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)

    main = f'''
<header class="page-hero ph-cv">
  <div class="wrap"><div class="ph-copy">
    <div class="crumbs"><a href='/'>Home</a> / Interview Prep</div>
    <h1 class="display">Walk in ready. Walk out <span class="tg1">hired.</span></h1>
    <p>Free interview prep for product marketing, partnerships and sales roles in Bengaluru. Practise with an AI mock interviewer, study 30 real questions with answer guides, watch short videos, and build your resume and cover letter in one place.</p>
    <div class="ip-jump" role="navigation" aria-label="On this page"><a href="#coach">AI interview coach</a><a href="#questions">30 questions</a><a href="#videos">Short videos</a><a href="#resume">Resume builder</a><a href="#cover">Cover letter</a><a href="#bengaluru">Bengaluru notes</a></div>
  </div>
    <figure class="hero-cv"><img src="/img/covers/interview-prep.jpg" alt="Walk in ready. Walk out hired. Interview prep, Bengaluru" width="1200" height="750" fetchpriority="high" decoding="async"></figure>
  </div>
</header>

<main id="main">

<section class="ip-sec" id="loop" aria-labelledby="loop-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">How the loop usually runs</span><h2 class="display" id="loop-t">Six rounds, one <span class="t2">story</span></h2>
    <p>Most B2B SaaS companies in Bengaluru run four to six stages for PMM, partnerships and sales roles. Formats vary by company, so ask the recruiter for the exact loop in the first call.</p></div>
    <div class="ip-loop">{loop}</div>
  </div>
</section>

<section class="ip-sec soft" id="coach" aria-labelledby="coach-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">Interview prep chatbot</span><h2 class="display" id="coach-t">Practise with an AI <span class="t5">coach</span></h2>
    <p>Pick your role and a mode. Ask anything, run a mock interview that scores each answer, or paste an answer for a review. If the AI is busy, a built-in coach takes over so it always works.</p></div>
    <div class="ip-coach" id="ipChat">
      <aside class="ip-side" aria-label="Coach settings">
        <div><h3>Role</h3><div class="ip-chips" id="ipRole" role="group" aria-label="Role">
          <button type="button" class="on" aria-pressed="true" data-v="pmm">Product Marketing</button><button type="button" aria-pressed="false" data-v="partnerships">Partnerships</button><button type="button" aria-pressed="false" data-v="sales">Sales</button></div></div>
        <div><h3>Mode</h3><div class="ip-chips" id="ipMode" role="group" aria-label="Mode">
          <button type="button" class="on" aria-pressed="true" data-v="ask">Ask anything</button><button type="button" aria-pressed="false" data-v="mock">Mock interview</button><button type="button" aria-pressed="false" data-v="review">Review my answer</button></div></div>
        <div><h3>Level</h3><label class="sr" for="ipLevel">Experience level</label><select id="ipLevel"><option value="entry">Entry, 0 to 2 years</option><option value="mid" selected>Mid, 3 to 6 years</option><option value="senior">Senior, 7 to 10 years</option><option value="lead">Lead or head of</option></select></div>
        <p class="ip-note">Do not paste phone numbers, IDs or other private details. Chats are sent to the AI model only to get a reply and are not stored by this site. AI can be wrong, so check facts before you rely on them.</p>
      </aside>
      <div class="ip-chat">
        <div class="ip-chat-top"><div><b>Interview Coach</b> <span class="ip-badge" id="ipAiBadge">Coach</span></div><button type="button" class="ip-reset" id="ipReset">New chat</button></div>
        <div class="ip-log" id="ipLog" aria-live="polite"></div>
        <div class="ip-quick" id="ipQuick"></div>
        <form class="ip-form" id="ipForm"><label class="sr" for="ipInput">Your message</label><textarea id="ipInput" rows="2" maxlength="2500" placeholder="Ask a question or type your answer. Enter to send, Shift and Enter for a new line."></textarea><button class="btn btn-primary" type="submit">Send</button></form>
      </div>
    </div>
  </div>
</section>

<section class="ip-sec" id="questions" aria-labelledby="q-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">Question bank</span><h2 class="display" id="q-t">30 questions you will <span class="t3">actually</span> get</h2>
    <p>Ten per role, each with what the interviewer is testing and how to answer. Press practise on any question to try it with the coach.</p></div>
    <div id="ipBank">{bank_html()}</div>
    <h3 class="ip-sub">Four questions every Bengaluru loop asks</h3>
    <div class="ip-general">{general}</div>
  </div>
</section>

<section class="yt-sec" id="videos" aria-labelledby="yt-title">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Watch in under a minute</span><h2 class="display" id="yt-title">Interview prep <span class="t5">shorts</span></h2>
    <p>Short clips on the questions that trip people up, then longer explainers when you want depth. Videos play here when you tap them.</p></div>
    <div class="yt-grid yt-shorts">{shorts}</div>
    <h3 class="ip-sub">Go deeper</h3>
    <div class="yt-grid">{longs}</div>
    <p class="yt-note">Videos belong to their creators and are embedded from YouTube.</p>
  </div>
</section>

<section class="ip-sec" id="resume" aria-labelledby="rs-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">Resume and cover letter creator</span><h2 class="display" id="rs-t">Build a resume that gets <span class="t4">shortlisted</span></h2>
    <p>An ATS friendly, one column resume with a live preview, bullet ideas for your role and a bullet checker. Then draft a matching cover letter. Everything stays in your browser.</p></div>
    <div class="ip-tabs" role="tablist" aria-label="Builder" data-tabs>
      <button type="button" role="tab" id="tb-res" aria-controls="tabResume" aria-selected="true" class="on">Resume</button>
      <button type="button" role="tab" id="tb-cov" aria-controls="tabCover" aria-selected="false">Cover letter</button>
    </div>

    <div role="tabpanel" id="tabResume" aria-labelledby="tb-res">
      <div class="rs-wrap">
        <form class="rs-form" id="rsForm" onsubmit="return false">
          <div class="rs-row"><label>Target role<select id="rsRole"><option value="pmm">Product Marketing</option><option value="partnerships">Partnerships</option><option value="sales">Sales</option></select></label>
            <label>Start from<button type="button" class="rs-mini" id="rsSample">Load a sample resume</button></label></div>
          <h3 class="rs-step"><span>1</span>About you</h3>
          <div class="rs-row"><label>Full name<input data-k="name" autocomplete="name" placeholder="Your Name"></label><label>City<input data-k="city" placeholder="Bengaluru, IN"></label></div>
          <div class="rs-row"><label>Phone<input data-k="phone" autocomplete="tel" placeholder="+91-98XXXXXXXX"></label><label>Email<input data-k="email" type="email" autocomplete="email" placeholder="you@email.com"></label></div>
          <div class="rs-row"><label>LinkedIn URL<input data-k="linkedin" placeholder="linkedin.com/in/yourname"></label><label>Portfolio URL, adds a QR code<input data-k="portfolio" placeholder="yourname.com"></label></div>
          <label>Headline, certifications or one standout line<input data-k="highlight" placeholder="Certified Scrum Master and Certified Scrum Product Owner"></label>
          <div class="rs-row"><label>Years of experience<input data-k="yoe" inputmode="numeric" placeholder="6"></label><label>Where<input data-k="env" placeholder="fast-paced B2B SaaS startups"></label></div>
          <h3 class="rs-step"><span>2</span>Education</h3>
          <div id="rsEdu"></div>
          <button type="button" class="rs-mini" id="rsAddEdu">+ Add education</button>
          <h3 class="rs-step"><span>3</span>Experience</h3>
          <div id="rsExp"></div>
          <button type="button" class="rs-mini" id="rsAdd">+ Add another company</button>
          <div><b style="font-size:13px">Bullet ideas for your role</b> <span style="font-size:12.5px;color:var(--ink-3)">Click to add to the role you last edited</span><div class="rs-ideas" id="rsIdeas" style="margin-top:8px"></div></div>
          <details class="rs-more"><summary>4. Skills, tools and certificates <em>prefilled for your role</em></summary>
            <div class="rs-row"><label>Skills label<input data-k="s1l"></label><label>Second skills label<input data-k="s2l"></label></div>
            <label>Skills<textarea data-k="s1" rows="2"></textarea></label>
            <label>Second skills group<textarea data-k="s2" rows="2"></textarea></label>
            <label>Tools<input data-k="tools"></label>
            <label>Courses and certificates, one per line as Name | Mon YYYY<textarea data-k="certs" rows="3" placeholder="Certified Scrum Product Owner | Oct 2022"></textarea></label>
            <label>Hobbies, optional<input data-k="hobbies" placeholder="Writing, Meetups, Reading, Cycling"></label>
          </details>
          <details class="rs-more"><summary>5. Volunteering <em>optional</em></summary>
            <div class="rs-row"><label>Organisation<input data-v="org" placeholder="AIESEC"></label><label>Location<input data-v="city" placeholder="Chennai, IN"></label></div>
            <div class="rs-row"><label>Role<input data-v="title" placeholder="Project Volunteer"></label><label>Dates<input data-v="dates" placeholder="Nov 2019 to Apr 2020"></label></div>
            <label>What you did, one per line<textarea data-v="bullets" rows="3"></textarea></label>
          </details>
        </form>
        <div class="rs-side">
          <div class="rs-acts"><button type="button" class="btn btn-primary" id="rsPdf">Download PDF</button><button type="button" class="btn btn-ghost" id="rsCopy">Copy text</button><button type="button" class="btn btn-ghost" id="rsSave">Save draft</button><button type="button" class="btn btn-ghost" id="rsClear">Clear</button></div>
          <div class="rs-paper" id="rsPreview" aria-label="Resume preview"></div>
          <div class="rs-check" id="rsCheck" aria-live="polite"></div>
        </div>
      </div>
    </div>

    <div role="tabpanel" id="tabCover" aria-labelledby="tb-cov" hidden>
      <span id="cover"></span>
      <div class="rs-wrap">
        <form class="rs-form" id="clForm" onsubmit="return false">
          <div class="rs-row"><label>Role type<select data-k="kind"><option value="pmm">Product Marketing</option><option value="partnerships">Partnerships</option><option value="sales">Sales</option></select></label>
            <label>Tone<select data-k="tone"><option value="crisp">Crisp and direct</option><option value="warm">Warm</option></select></label></div>
          <div class="rs-row"><label>Job title you are applying for<input data-k="role" placeholder="Product Marketing Manager"></label><label>Company<input data-k="company" placeholder="Company name"></label></div>
          <div class="rs-row"><label>Hiring manager, optional<input data-k="manager" placeholder="Priya"></label><label>Your current role<input data-k="current" placeholder="PMM at Example SaaS Co"></label></div>
          <label>Why this company, one or two lines<textarea data-k="why" rows="2" placeholder="Your recent move into mid-market is exactly the stage where I have done my best work."></textarea></label>
          <label>Proof point 1, with a number<input data-k="a1" placeholder="launched our analytics module, adding 4.2 Cr pipeline in two quarters"></label>
          <label>Proof point 2, with a number<input data-k="a2" placeholder="rebuilt the pitch with sales, lifting win rate from 19% to 27%"></label>
          <label>Notice period line<input data-k="notice" placeholder="can join within 60 days"></label>
          <div class="rs-row"><label>Your name<input data-k="name" autocomplete="name"></label><label>Email<input data-k="email" type="email" autocomplete="email"></label></div>
          <label>Phone, optional<input data-k="phone" autocomplete="tel"></label>
        </form>
        <div class="rs-side">
          <div class="rs-acts"><button type="button" class="btn btn-primary" id="clPdf">Download PDF</button><button type="button" class="btn btn-ghost" id="clAi">Polish with AI</button><button type="button" class="btn btn-ghost" id="clCopy">Copy</button><button type="button" class="btn btn-ghost" id="clSave">Save draft</button><button type="button" class="btn btn-ghost" id="clRegen">Rebuild from form</button></div>
          <label class="sr" for="clOut">Cover letter</label><textarea class="cl-out" id="clOut" spellcheck="true"></textarea>
          <div class="cl-meta"><span id="clWords"></span><span>Edit the letter directly, it is yours.</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="ip-sec soft" id="bengaluru" aria-labelledby="blr-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">Bengaluru specific</span><h2 class="display" id="blr-t">Six things to know before you <span class="t6">sign</span></h2>
    <p>The parts of a Bengaluru job search that generic interview guides skip.</p></div>
    <div class="ip-blr">{blr}</div>
    <p class="ip-head" style="margin-top:24px">Looking for roles? See the <a href="/jobs" style="color:var(--accent);text-decoration:underline">live job board</a> for PMM, growth and partnerships openings, or <a href="/schedule-meeting" style="color:var(--accent);text-decoration:underline">book a call</a> for a one to one mock interview.</p>
  </div>
</section>

<section class="ip-sec" id="faq" aria-labelledby="faq-t">
  <div class="wrap">
    <div class="ip-head reveal"><span class="eyebrow">FAQ</span><h2 class="display" id="faq-t">Common <span class="t2">questions</span></h2></div>
    <div class="ip-faq">{faq}</div>
  </div>
</section>

'''
    out = head + top + "\n" + main + tail
    assert "—" not in out.split("<main")[1] and "–" not in out.split("<main")[1], "dash found"
    open(os.path.join(ROOT, f"{SLUG}.html"), "w", encoding="utf-8").write(out)
    print("wrote", f"site/{SLUG}.html", len(out))


if __name__ == "__main__":
    build()
