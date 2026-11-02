#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate the 5 part "Pipeline Notes" Substack series (GTM, SEO, AEO frameworks) as paste ready HTML plus a review markdown
# Owner: Syed Hadi
import os, re

S = "https://syedcreates.com"
OUT = "/home/claude/substack"
os.makedirs(OUT, exist_ok=True)

def img(pid, alt, cap, href, w=1200, h=675):
    src = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&q=80&w={w}&h={h}"
    return {"src": src, "alt": alt, "cap": cap, "href": href}

POSTS = [
 dict(slug="pipeline-math", date="Mon 2 Nov 2026, 3:00 PM IST",
  title="The Pipeline Math Framework: Turn a Marketing Budget Into a Number Sales Believes",
  subtitle="Five lines of arithmetic that took me from defending spend to owning a pipeline target. Issue 1 of the GTM, SEO, AEO series.",
  seo_title="Pipeline Math Framework for B2B SaaS Marketing | Syed Hadi",
  seo_desc="How to turn marketing spend into a pipeline commitment: the five line pipeline math framework used to build $2M pipeline on a $25K quarter.",
  blocks=[
   ("p", f"Every marketing plan I have seen die did so in the same meeting. The CFO asks what the spend returns and the answer is a slide of impressions. Pipeline math fixes that. It is five lines, it fits on a napkin, and it is the first thing I run in every <a href='{S}/gtm-health-check'>GTM health check</a>."),
   ("img", img("1460925895917-afdab827c52f", "Analytics dashboard on a laptop screen", "Start from the revenue target, not the channel. Try the GTM Health Check.", f"{S}/gtm-health-check")),
   ("h3", "The five lines"),
   ("ol", [
     "<b>Revenue target</b> for the period, from the board plan.",
     "<b>Win rate</b> on sourced pipeline, trailing two quarters. Use the real number, not the aspirational one.",
     "<b>Pipeline needed</b> = revenue target ÷ win rate. A $1M target at 25% needs $4M of pipeline.",
     "<b>Marketing share</b> of that pipeline, agreed with sales. 30 to 40% is normal for a partner and outbound heavy motion.",
     "<b>Cost per opportunity</b> by channel, trailing. Divide your share by it and you have the budget, with the receipt attached.",
   ]),
   ("img", img("1551288049-bebda4e38f71", "Charts and numbers on a tablet", "Win rate and cost per opportunity are the two inputs people guess. Measure them.", f"{S}/gtm-case-study")),
   ("h3", "Where it earned its keep"),
   ("p", f"At one security startup the quarter's budget was $25K. Pipeline math said webinars with partners produced opportunities at a third of the cost of paid search, so 70% of the money went there. The quarter closed with <a href='{S}/gtm-case-study'>$2M of sourced pipeline</a>, an 80 to 1 ratio. The channel mix was not clever. The arithmetic was."),
   ("img", img("1553729459-efe14ef6055d", "Growth chart drawn on paper", "Spend to pipeline ratio is the one number to report every month.", f"{S}/gtm-in-a-box")),
   ("h3", "Three rules that keep it honest"),
   ("ul", [
     "Report sourced and influenced pipeline separately. Mixing them is how trust evaporates.",
     "Re-run the math every quarter. Win rate drifts, and last year's cost per opportunity is a story, not a plan.",
     "Agree the marketing share in writing with the sales lead before the quarter starts.",
   ]),
   ("img", img("1522071820081-009f0129c71c", "Team reviewing a plan at a table", "The sales lead signs the share of pipeline. That signature is the whole framework.", f"{S}/gtm-pmm-in-a-box")),
   ("p", f"The full worksheet, with a channel cost template, is in the <a href='{S}/gtm-in-a-box'>GTM in a Box</a> playbook. Run your own numbers through the <a href='{S}/gtm-health-check'>health check</a> first, it takes four minutes."),
   ("img", img("1507003211169-0a1dd7228f2d", "Person working on a laptop by a window", "Tomorrow: the SEO topic cluster framework that got 40 pages ranking in 90 days.", f"{S}/seo-aeo-score")),
   ("p", "Reply with your spend to pipeline ratio. I read every one."),
  ]),
 dict(slug="seo-topic-clusters", date="Tue 3 Nov 2026, 3:00 PM IST",
  title="The Topic Cluster Framework: How 40 Pages Started Ranking in 90 Days",
  subtitle="One pillar, eight spokes, internal links in both directions. The SEO structure that still works when the algorithm changes. Issue 2 of the series.",
  seo_title="SEO Topic Cluster Framework for B2B SaaS, 90 Day Plan | Syed Hadi",
  seo_desc="The pillar and spoke topic cluster framework that got 40 B2B security pages ranking in 90 days, with the keyword, linking and refresh rules.",
  blocks=[
   ("p", f"Most B2B blogs are a pile of unrelated posts. Google cannot tell what the site is about, so nothing ranks. Topic clusters fix the structure before you write a word. This is the exact framework behind the <a href='{S}/aeo-seo-case-study'>SEO and AEO case study</a> on my site."),
   ("img", img("1504868584819-f8e8b4b6d7e3", "Open notebook with a plan sketched out", "Map the cluster before you write. Score your current pages with the SEO and AEO tool.", f"{S}/seo-aeo-score")),
   ("h3", "The structure"),
   ("ol", [
     "<b>One pillar page</b> per commercial topic. 2,500 words, answers the whole question, targets the head term. Example: CNAPP explained for buyers.",
     "<b>Eight spoke pages</b>, each on a long tail question the pillar only touches. Comparison, checklist, pricing, how to evaluate, versus pages.",
     "<b>Links both ways.</b> Every spoke links up to the pillar with the head term as anchor. The pillar links down to every spoke.",
     "<b>One cluster a month.</b> Eight pages is a sprint a small team can ship and still have evidence to put in them.",
   ]),
   ("img", img("1434030216411-0b793f4b4173", "Person writing notes next to a laptop", "Spokes answer the questions buyers type at 11 PM. Pull them from sales calls.", f"{S}/aeo-seo-in-a-box")),
   ("h3", "Picking the keywords"),
   ("p", "Skip the tools for the first pass. Pull the last 30 discovery calls and list every question a prospect asked. Group them. The groups are your clusters, the questions are your spokes, and the language is already in the buyer's words. Then validate volume and difficulty, and prefer a 200 search a month term you can own over a 5,000 one you cannot."),
   ("img", img("1517245386807-bb43f82c33c4", "Team working together around a laptop", "The best keyword research is a stack of call notes.", f"{S}/content-in-a-box")),
   ("h3", "The 90 day cadence"),
   ("ul", [
     "Days 1 to 30: pillar plus four spokes, internal links live on day one.",
     "Days 31 to 60: remaining spokes, then update the pillar with links and a summary of each.",
     "Days 61 to 90: refresh titles and meta from Search Console queries, add FAQ schema, build three links from partner sites.",
   ]),
   ("img", img("1484480974693-6ca0a78fb36b", "Laptop showing a rising graph", "Rankings move in month three. Budget patience into the plan.", f"{S}/aeo-seo-case-study")),
   ("p", f"The cluster planner, the brief template and the refresh checklist are in <a href='{S}/aeo-seo-in-a-box'>AEO and SEO in a Box</a>. Check where your site stands with the free <a href='{S}/seo-aeo-score'>SEO and AEO score</a>."),
   ("img", img("1498050108023-c5249f4df085", "Code on a laptop screen", "Tomorrow: the answer first page framework that gets you cited by ChatGPT and Perplexity.", f"{S}/ai-visibility-checker")),
   ("p", "Which cluster would you build first? Reply and I will sanity check it."),
  ]),
 dict(slug="aeo-answer-first", date="Wed 4 Nov 2026, 3:00 PM IST",
  title="The Answer First Framework: How to Get Cited by ChatGPT, Perplexity and Google AI Overviews",
  subtitle="AEO is not a new channel. It is a page structure. Six rules that moved my pages from invisible to cited. Issue 3 of the series.",
  seo_title="AEO Framework: Get Cited by ChatGPT, Perplexity and AI Overviews | Syed Hadi",
  seo_desc="The answer first page framework for answer engine optimisation: six structural rules that get B2B pages cited by ChatGPT, Perplexity and Google AI Overviews.",
  blocks=[
   ("p", f"Buyers now ask ChatGPT and Perplexity what to shortlist before they ever hit your site. If the model cannot lift a clean answer from your page, you do not exist in that conversation. Run the <a href='{S}/ai-visibility-checker'>AI Visibility Checker</a> on your brand and you will see the gap in a minute."),
   ("img", img("1677442136019-21780ecad995", "Abstract AI neural network visual", "Answer engines quote pages that answer. Check your visibility first.", f"{S}/ai-visibility-checker")),
   ("h3", "Six rules of an answer first page"),
   ("ol", [
     "<b>Answer in the first 60 words.</b> Definition, number or verdict, before any context. Models extract the top of the page.",
     "<b>One question per H2,</b> phrased the way a buyer asks it. The heading is the prompt, the paragraph is the answer.",
     "<b>Tables for comparisons.</b> Models love structured rows. A five row table outranks five paragraphs for a versus query.",
     "<b>Cite a primary source</b> in every section. Standards, filings, your own data. Citations get you cited.",
     "<b>FAQ schema and author schema.</b> Machine readable trust signals, five minutes to add.",
     "<b>Say the entity name.</b> Your product, the category, the competitor. Pronouns do not get retrieved.",
   ]),
   ("img", img("1555949963-aa79dcee981c", "Developer working on code with multiple screens", "Structure beats length. A 900 word page with clean H2 questions wins.", f"{S}/aeo-seo-in-a-box")),
   ("h3", "What changed when we applied it"),
   ("p", f"On a set of 12 security explainer pages, rewriting the first paragraph and the H2s took one afternoon. Within six weeks the brand appeared in Perplexity answers for 9 of 12 target questions, up from 2. Organic clicks rose too, because the same structure is what Google's AI Overviews pull from. The numbers are in the <a href='{S}/aeo-seo-case-study'>case study</a>."),
   ("img", img("1551434678-e076c223a692", "Two people reviewing analytics on screens", "Measure citations weekly. Ask the same 20 questions, log who gets named.", f"{S}/aeo-seo-case-study")),
   ("h3", "The weekly AEO habit"),
   ("ul", [
     "Keep a list of 20 buyer questions. Ask them in ChatGPT, Perplexity and Google every Monday.",
     "Log which domains get cited. Those are the pages to study and outstructure.",
     "Rewrite one page a week to the six rules. Do not touch the rest until it is cited.",
   ]),
   ("img", img("1512314889357-e157c22f938d", "Hands typing on a laptop keyboard", "One page a week, rewritten to the rules, compounds.", f"{S}/content-in-a-box")),
   ("p", f"The page template and the question tracker are in <a href='{S}/aeo-seo-in-a-box'>AEO and SEO in a Box</a>. Score any URL with the <a href='{S}/seo-aeo-score'>SEO and AEO tool</a>, it flags which of the six rules you are missing."),
   ("img", img("1543286386-713bdd548da4", "Growth chart on a tablet on a desk", "Tomorrow: the 90 day partner program framework that brought 40% of pipeline.", f"{S}/partner-readiness-score")),
   ("p", "Reply with one question your buyers ask AI. I will tell you who is getting cited for it."),
  ]),
 dict(slug="partner-program-90-days", date="Thu 5 Nov 2026, 3:00 PM IST",
  title="The 90 Day Partner Program Framework: From Zero Partners to 40% of Pipeline",
  subtitle="Recruit, enable, co sell. The three phase plan that built partner sourced revenue at a security startup, with the mistakes left in. Issue 4 of the series.",
  seo_title="90 Day SaaS Partner Program Framework, Recruit Enable Co Sell | Syed Hadi",
  seo_desc="A 90 day framework for building a B2B SaaS partner program: how to recruit the right resellers, enable them in two weeks and run co sell cadences that bring pipeline.",
  blocks=[
   ("p", f"Partner programs fail for one reason: the vendor signs 30 logos and enables none of them. The framework below signs fewer, enables all, and gets to sourced pipeline in a quarter. It is the backbone of the <a href='{S}/how-to-build-a-saas-partner-program'>partner program guide</a> on my site."),
   ("img", img("1521737711867-e3b97375f902", "Team hands stacked together", "Fewer partners, fully enabled, beats a logo wall. Score yours first.", f"{S}/partner-readiness-score")),
   ("h3", "Days 1 to 30: recruit the right ten"),
   ("ul", [
     "Define the ideal partner on one page: region, customer base, adjacent product, a named champion.",
     "Screen 50, shortlist 15, sign 10. Use a <a href='" + S + "/partner-readiness-score'>readiness score</a>, not gut feel.",
     "Put deal registration and margin in a two page agreement. Long contracts stall; short ones close.",
   ]),
   ("img", img("1556761175-5973dc0f32e7", "Business meeting in a bright office", "The named champion inside the partner matters more than the logo.", f"{S}/how-to-build-a-saas-partner-program")),
   ("h3", "Days 31 to 60: enable in two weeks, not two months"),
   ("p", "Three assets and one call. A 10 slide pitch the partner can present without you, a one page battlecard, a demo video under eight minutes, and a 45 minute enablement call with a live deal review. Certify the champion, not the company. Everything else is a nice to have. If a partner cannot find 45 minutes in two weeks, they were never going to sell for you, and that is useful to learn in month two rather than month nine."),
   ("img", img("1531403009284-440f080d1e12", "Whiteboard session with sticky notes", "Enablement is a pitch deck, a battlecard, a demo and one call.", f"{S}/partner-revenue-in-a-box")),
   ("h3", "Days 61 to 90: co sell on a cadence"),
   ("ul", [
     "Weekly 30 minute pipeline call per active partner. Shared sheet, three columns: account, stage, next step with owner.",
     "One joint webinar or roundtable a month, partner invites, you present. This is where the pipeline came from.",
     "Pay the first commission fast and publicly. Nothing recruits the next partner like the first cheque.",
   ]),
   ("img", img("1552664730-d307ca884978", "Team meeting around a conference table", "The weekly pipeline call is the program. Miss it twice and the partner goes quiet.", f"{S}/partner-revenue-case-study")),
   ("p", f"At AccuKnox this structure took partner sourced pipeline to roughly 40% of the total within two quarters, documented in the <a href='{S}/partner-revenue-case-study'>partner revenue case study</a>. Templates, the agreement outline and the cadence sheet are in <a href='{S}/partner-revenue-in-a-box'>Partner Revenue in a Box</a>."),
   ("img", img("1529333166437-7750a6dd5a70", "Group of colleagues celebrating together", "Tomorrow, the last issue: the one page positioning framework behind every launch.", f"{S}/pmm-in-a-box")),
   ("p", "How many partners have you signed, and how many have sourced a deal? Reply with both numbers."),
  ]),
 dict(slug="one-page-positioning", date="Fri 6 Nov 2026, 3:00 PM IST",
  title="The One Page Positioning Framework: Why Launches Work or Die Before the Press Release",
  subtitle="Five boxes, one page, signed by sales and product before anyone writes copy. The PMM framework behind every launch I have run. Issue 5 of the series.",
  seo_title="One Page Positioning Framework for Product Launches | Syed Hadi",
  seo_desc="The one page positioning framework product marketers use before a launch: competitive alternative, unique capability, value, best fit customer and category, with a launch checklist.",
  blocks=[
   ("p", f"A launch does not fail on launch day. It fails three weeks earlier when nobody agreed what the product is for and who it beats. The one page positioning doc is the fix. It is the first template in <a href='{S}/pmm-in-a-box'>PMM in a Box</a> and the first thing I ask for in any <a href='{S}/pmm-case-study'>product marketing engagement</a>."),
   ("img", img("1542744173-8e7e53415bb0", "Team presenting a plan on a screen", "Positioning is a decision, not a paragraph. Make it on one page.", f"{S}/pmm-in-a-box")),
   ("h3", "The five boxes"),
   ("ol", [
     "<b>Competitive alternative.</b> What the buyer does today if you did not exist. Often a spreadsheet, an intern or doing nothing.",
     "<b>Unique capability.</b> The two or three things you do that the alternative cannot. Features, stated plainly.",
     "<b>Value.</b> What each capability lets the customer do, in their words, with a number where you have one.",
     "<b>Best fit customer.</b> The segment that cares most about that value. Narrow enough to be wrong about.",
     "<b>Category.</b> The market frame that makes the value obvious. Pick the one buyers already have budget for.",
   ]),
   ("img", img("1507925921958-8a62f3d1a50d", "Hands sketching a layout on paper", "Fill the boxes in order. Category comes last, not first.", f"{S}/pmm-case-study")),
   ("h3", "The signature rule"),
   ("p", "The page is not done until the head of sales and the head of product both sign it. Not approve on Slack, sign. The argument you have in that meeting is the argument you would otherwise have with the market, at ten times the cost. Every launch asset, from the press release to the sales deck to the landing page, is then written from this page and nothing else."),
   ("img", img("1553877522-43269d4ea984", "Two colleagues agreeing across a desk", "Sales and product sign the page. Then copy starts.", f"{S}/gtm-pmm-in-a-box")),
   ("h3", "Launch checklist, from the page"),
   ("ul", [
     "Messaging hierarchy: one headline, three pillars, nine proof points, all traceable to a box.",
     "Sales enablement two weeks before: deck, battlecard, objection sheet, 30 minute call.",
     "Launch day: website, press, partner email, customer email, social, in that order.",
     "Day 30 review: pipeline sourced, win rate on launch deals, which proof point sales actually used.",
   ]),
   ("img", img("1486312338219-ce68d2c6f44d", "Laptop and notebook on a desk ready for work", "Every launch asset traces back to a box on the page.", f"{S}/content-in-a-box")),
   ("p", f"The template, a worked example and the launch checklist are in <a href='{S}/pmm-in-a-box'>PMM in a Box</a>. If you want the whole series as reusable prompts, the <a href='{S}/skill-pack'>GTM skill pack</a> bundles all five frameworks."),
   ("img", img("1518186285589-2f7649de83e0", "Sunlight over a mountain road ahead", "That is the series. Next Pipeline Notes lands in two weeks with one play and one template.", f"{S}/")),
   ("p", "Reply with your competitive alternative in one sentence. If it is a competitor's name, we should talk."),
  ]),
]

def render_html(p):
    out = []
    for kind, v in p["blocks"]:
        if kind == "p": out.append(f"<p>{v}</p>")
        elif kind == "h3": out.append(f"<h3>{v}</h3>")
        elif kind == "ol": out.append("<ol>" + "".join(f"<li>{x}</li>" for x in v) + "</ol>")
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{x}</li>" for x in v) + "</ul>")
        elif kind == "img":
            out.append(f'<figure><a href="{v["href"]}"><img src="{v["src"]}" alt="{v["alt"]}"></a><figcaption><a href="{v["href"]}">{v["cap"]}</a></figcaption></figure>')
    return "\n".join(out)

def words(p):
    t = " ".join(re.sub("<[^>]+>", "", v if isinstance(v, str) else " ".join(v)) for k, v in p["blocks"] if k != "img")
    return len(t.split())

md = ["# Pipeline Notes: GTM, SEO, AEO series (5 drafts for review)\n", "Schedule: one a day, Mon 2 Nov to Fri 6 Nov 2026, 3:00 PM IST. Each has 5 inline images (Unsplash) and every image and caption links to a page on syedcreates.com.\n"]
for i, p in enumerate(POSTS, 1):
    html = render_html(p)
    open(f"{OUT}/{i}-{p['slug']}.html", "w").write(html)
    md.append(f"\n---\n\n## {i}. {p['title']}\n\n**Publish:** {p['date']}  \n**Subtitle:** {p['subtitle']}  \n**SEO title:** {p['seo_title']}  \n**SEO description:** {p['seo_desc']}  \n**Word count (text):** {words(p)}\n")
    for kind, v in p["blocks"]:
        if kind == "p": md.append(re.sub(r"<a href='([^']+)'>([^<]+)</a>", r"[\2](\1)", v).replace("<b>", "**").replace("</b>", "**") + "\n")
        elif kind == "h3": md.append(f"### {v}\n")
        elif kind in ("ol", "ul"):
            for j, x in enumerate(v, 1):
                x = re.sub(r"<a href='([^']+)'>([^<]+)</a>", r"[\2](\1)", x).replace("<b>", "**").replace("</b>", "**")
                md.append((f"{j}. " if kind == "ol" else "- ") + x)
            md.append("")
        elif kind == "img":
            md.append(f"![{v['alt']}]({v['src']})  \n*{v['cap']}* (links to {v['href']})\n")
open(f"{OUT}/drafts-review.md", "w").write("\n".join(md))
print("written", [f"{w} words" for w in map(words, POSTS)])
