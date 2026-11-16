---
{"slug": "gtm-box-day-3-pipeline-winloss-channel-audit", "date": "2026-11-17", "day": 3, "series": "GTM in a Box", "free_preview": true, "section": "GTM in a Box", "title": "Pipeline, Win Loss and Channel Audit in One Afternoon", "description": "Audit your pipeline by stage and age, code win loss reasons and price every channel in one afternoon. Day 3 of GTM in a Box, with a copy ready audit sheet.", "h1": "Your pipeline is lying to", "h1_accent": "you", "cover_text": "One afternoon. Three numbers. Zero", "cover_accent": "excuses", "cover_tag": "Day 3 audit", "substack_title": "Audit your pipeline, win loss and channels in one afternoon", "substack_subtitle": "Day 3 of GTM in a Box. Four lenses, one sheet and the three numbers that decide where next quarter's money goes.", "tags": ["GTM in a Box", "pipeline audit", "win loss analysis", "channel attribution", "B2B SaaS", "RevOps"], "sources": [{"title": "Clozd, 5 lies your CRM is telling you about your buyers", "url": "https://clozd.com/blog/5-lies-your-crm-is-telling-you-about-your-buyers"}, {"title": "Clozd, Why interviews beat surveys for win loss analysis", "url": "https://www.clozd.com/blog/win-loss-analysis-why-interviews"}]}
---

Your CRM says you have four times coverage. Your gut says the quarter is in trouble. One of them is wrong, and after today you will know which one.

## Why the audit comes before the plan

Most teams build next quarter's plan on top of numbers nobody has checked. The pipeline report includes deals that died in spring. The loss reasons say "price" because that was the easiest option in the dropdown. And the channel report credits whoever touched the deal last.

Before we rebuilt the engine at AccuKnox, pipeline depended on events and outbound, and nobody could trace which channel produced which deal. Every budget meeting turned into a debate about feelings. We fixed tracking first, content second and scale third, and that order is why the engine later supported $2M of influenced pipeline a year on a $100K budget. The full story sits in the [GTM case study](https://syedcreates.com/gtm-case-study).

This audit is item two of phase one in the [GTM in a box](https://syedcreates.com/gtm-in-a-box) roadmap, right after the ICP work. It looks through four lenses.

1. Pipeline by stage and age. What is real, what is stuck, what is dead.
2. Conversion by stage. Where deals actually leak.
3. Win loss reasons. Why buyers said yes or no, in their words.
4. Channel cost and pipeline. What each dollar and hour bought.

The win loss lens is the one teams skip, and it is the one that hurts most. Clozd compared CRM data from 1,000 closed lost deals with what buyers said in interviews, and found the [CRM reason matched the buyer only 15% of the time](https://clozd.com/blog/5-lies-your-crm-is-telling-you-about-your-buyers). The same study found the CRM had the wrong competitor in nearly seven of every ten deals. If that is even half true for you, your roadmap and your battlecards are aimed at the wrong target.

You do not need a RevOps team for this. You need a CRM export, your spend for the last two quarters, five buyer calls and one afternoon. At the end you get three numbers, and those three numbers decide everything you build in the next 60 days.

Not sure where you stand? Take the two minute [GTM health check](https://syedcreates.com/gtm-health-check) first. Questions three, seven and ten cover exactly what this audit fixes.

<!-- PAYWALL -->

## The four lens method

![Four audit lenses, pipeline by stage and age, conversion by stage, win loss coding and channel cost, feeding three numbers, real coverage, qualified win rate and cost per opportunity](/img/blog/gtm-box-day-3-pipeline-winloss-channel-audit-1.png)

Block four hours. Do the lenses in this order, because each one cleans the data for the next.

### Lens 1, pipeline by stage and age (60 minutes)

Export every open opportunity with stage, amount, created date, date it entered the current stage, source channel and next step date.

- Work out your average sales cycle from deals won in the last two quarters.
- Flag any deal older than twice that cycle as stale.
- Flag any deal with no next step date, or a next step date in the past.
- Flag any deal that has sat in one stage longer than your average time in that stage.

Then take every flagged deal to its owner with one question. "Will this close in the next 90 days, yes or no?" A no moves to a nurture list. It does not stay in the forecast.

### Lens 2, conversion by stage (45 minutes)

Count how many deals entered each stage over the last two quarters and how many moved forward. You want a simple ladder, for example qualified, demo, proposal, closed won. The step with the worst conversion is your leak. Do not try to fix every step. Fix the worst one.

### Lens 3, win loss interviews and reason coding (90 minutes, plus calls)

Pick ten recent decisions, five wins and five losses. Book 30 minute calls with the buyers, not the reps. Clozd's own guidance says reps often lack the full story and that [interviews typically draw more than 20% participation](https://www.clozd.com/blog/win-loss-analysis-why-interviews) against under 5% for surveys. Offer a small thank you and ask for permission to record.

Ask five questions.

1. What triggered the search in the first place?
2. Which other options did you consider, including doing nothing?
3. What almost made you choose differently?
4. How did our sales process feel compared to the others?
5. If you could change one thing about our offer, what would it be?

Then code every deal with one primary reason and up to two secondary reasons. Buyers usually give several drivers, so one dropdown value will never be enough. Use a fixed code list so you can count.

- VALUE, the buyer did not see enough return
- PRICE, the value was clear but the cost or terms did not fit
- FIT, product gap or missing integration
- TIMING, no decision, budget freeze or priority shift
- ALT, chose another vendor or an internal build
- TRUST, proof, references or security review
- PROCESS, our sales experience helped or hurt
- CHAMPION, a strong or missing internal sponsor

### Lens 4, channel cost and pipeline (45 minutes)

For each channel, add up spend for the last two quarters. Include tools and the people time behind it, at a rough hourly cost. Then count opportunities created and pipeline value from each. Divide to get cost per opportunity and pipeline per dollar. If you cannot tell which channel sourced a deal, mark it UNKNOWN. A big UNKNOWN row is itself a finding.

## The 3 numbers that matter

Everything above rolls into three numbers. Write them at the top of the sheet.

1. Real coverage. Clean pipeline divided by next quarter's new revenue target. This tells you whether you have a demand problem.
2. Qualified win rate. Closed won divided by deals that reached qualified. This tells you whether you have a conversion problem.
3. Cost per opportunity by channel. This tells you where the next dollar goes.

Low coverage means you need more pipeline. Fine coverage with a weak win rate means more pipeline will not save you, and the win loss codes tell you what to fix instead.

## The audit sheet template

Copy these three tabs into one Google Sheet.

Tab 1, Pipeline

| Opportunity | Account | Stage | Amount | Created | Days in stage | Age in days | Source channel | Next step date | Stale flag | Owner says closes in 90 days |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | Y or N | Y or N |

Tab 2, Win loss

| Deal | Outcome | Amount | CRM reason | Primary code | Secondary codes | Competitor named by buyer | Buyer quote | CRM matches buyer |
|---|---|---|---|---|---|---|---|---|
| | Won or Lost | | | VALUE | TRUST, PROCESS | | | Y or N |

Tab 3, Channels

| Channel | Spend incl. people time | Opportunities created | Pipeline value | Cost per opportunity | Pipeline per dollar | Win rate |
|---|---|---|---|---|---|---|
| | | | | Spend divided by opps | Pipeline divided by spend | |

Summary row. Real coverage, qualified win rate, cheapest channel per opportunity, biggest leak stage, top loss code.

## Worked example

These numbers are illustrative, made up to show the shape of the math.

A startup shows $1.68M of open pipeline across 42 deals against a $400K new revenue target. That reads as 4.2x coverage. Its average won cycle is 90 days. Fifteen deals worth $720K are older than 180 days, and their owners say none will close this quarter. Clean pipeline drops to $960K. Real coverage is 2.4x, not 4.2x.

Over two quarters, 100 deals reached qualified, 55 reached demo, 22 reached proposal and 9 closed. Qualified win rate is 9%. The leak is demo to proposal at 40%, so the fix is the demo, not more leads.

Channel spend for the quarter totals $25K.

| Channel | Spend | Opps | Pipeline | Cost per opp | Pipeline per dollar |
|---|---|---|---|---|---|
| Events | $12,000 | 8 | $240K | $1,500 | 20x |
| Outbound | $6,000 | 10 | $250K | $600 | 42x |
| Content and SEO | $4,000 | 9 | $315K | $444 | 79x |
| Partners | $3,000 | 5 | $275K | $600 | 92x |

Events ate nearly half the budget for a quarter of the opportunities. The win loss calls add the twist. Four of five losses were coded VALUE or TRUST, and only one was PRICE, while the CRM said "price" for all five. So the plan becomes clear. Move part of the event budget into content and partners, rebuild the demo around proof, and stop discounting to fix a problem that was never price.

## Common mistakes

- Counting influenced pipeline as sourced. Report both, and label them honestly.
- Letting reps code their own losses without buyer calls.
- Leaving people time out of channel cost, which makes outbound and events look cheap.
- Auditing once. Review pipeline weekly, channel spend monthly and win loss reasons every month.
- Fixing every leak at once. Pick the single worst stage.

## What to do today

1. Export open opportunities and flag every deal older than twice your average won cycle.
2. Book five buyer calls, three losses and two wins, from the last 90 days.
3. Add up last quarter's spend per channel, people time included.
4. Fill in the three tabs and write your three numbers at the top.
5. Share the sheet in your next weekly pipeline review with sales and agree on one fix.

If you want the stack behind our tracking, see the [GTM engine](https://syedcreates.com/gtm-engine), and the budget math lives in [$100K budget, $2M pipeline](https://syedcreates.com/2m-pipeline-100k-budget).

Tomorrow, Day 4. Scan competitors and pricing without a research team.

Subscribe to Pipeline Notes at https://syedhadi.substack.com to get every issue of GTM in a Box.
