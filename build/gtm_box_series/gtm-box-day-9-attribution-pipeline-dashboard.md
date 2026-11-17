---
{"slug": "gtm-box-day-9-attribution-pipeline-dashboard", "date": "2026-11-25", "section": "GTM in a Box", "day": 9, "series": "GTM in a Box", "free_preview": false, "title": "B2B Attribution That Ties Every Channel to Pipeline", "description": "Day 9 of GTM in a Box. Source vs influence, UTM and CRM field rules, self reported attribution and a five chart pipeline dashboard you review weekly.", "h1": "Stop guessing which channel actually", "h1_accent": "pays", "cover_text": "Every channel, one", "cover_accent": "scoreboard", "cover_tag": "Attribution", "substack_title": "Attribution that ties every channel to pipeline", "substack_subtitle": "Day 9 of GTM in a Box. Two ledgers, one field the buyer fills in, and a five chart dashboard your sales lead will actually open.", "tags": ["attribution", "pipeline dashboard", "UTM", "RevOps", "B2B SaaS", "GTM in a Box"], "sources": [{"title": "Refine Labs Study Confirms Measurement Gap in Software Based Attribution and Releases Hybrid Attribution Framework", "url": "https://www.refinelabs.com/news/hybrid-attribution-framework"}, {"title": "A definitive guide to marketing attribution, Tim Dalrymple in Growth Unhinged", "url": "https://www.growthunhinged.com/p/guide-to-marketing-attribution"}]}
---
Every budget meeting I sat through before we fixed tracking ended the same way. Someone said events work, someone said LinkedIn works, and nobody could prove either. Today you fix that, with two ledgers, one honest field and a dashboard that fits on one screen.

## Why most attribution dies in month two

When we started at AccuKnox, pipeline depended on events and outbound, and nobody could trace which channel produced which deal. The website described the product but did not create demand. That is the "situation" line on the [GTM case study](https://syedcreates.com/gtm-case-study), and I suspect it describes your company too.

The fix was not a fancy tool. Phase one was GA4 events on every conversion that mattered, account based intelligence from Factors.ai, and a clear ICP with target account lists for sales. Tracking came first, content second, scale third. That order is the whole lesson.

Most teams flip it. They buy a multi touch tool, plug it into a CRM full of blank fields, and get a beautiful dashboard of nonsense. By month two, sales stops trusting it and marketing stops opening it.

## Source and influence are two different questions

Here is the idea that makes everything else work. You keep two ledgers, and you never mix them.

- Sourced pipeline answers "which channel created this opportunity". Every opportunity gets exactly one source. The total adds up to 100% of pipeline.
- Influenced pipeline answers "which channels touched this opportunity before it closed". One opportunity can count for five channels. The total adds up to way more than 100%, and that is fine.

The trouble starts when a marketer reports influenced numbers in a meeting where sales expects sourced numbers. Sales hears inflation and stops listening. Say influenced when you mean influenced, and show sourced right next to it.

## The channel your software cannot see

Software attribution only sees clicks. Buyers do a lot of their deciding where there are no clicks. Refine Labs ran a twelve month study across 620 declared intent conversions and $21.5M of closed won revenue, and found a 90% gap between what software attribution reported and what customers said themselves. In their data, [podcasts got 0% credit from software and 53% from buyers](https://www.refinelabs.com/news/hybrid-attribution-framework).

You do not need to pick a side. You need both views on the same page. That is what the rest of today builds.

## The method, step by step

This is the attribution module from [GTM in a box](https://syedcreates.com/gtm-in-a-box), the one that sits in days 31 to 60 next to outbound and the partner program. Plan for one focused week to set it up, then thirty minutes a week to run it.

1. Write the definitions down. One paragraph each for sourced, influenced and self reported. Get your sales lead to sign it. This takes an hour and saves a year of arguments.
2. Lock the UTM rules. Five parameters, lowercase only, values picked from a fixed list. No free typing in campaign builders.
3. Add four CRM fields. Original source, latest source, self reported source and partner involved. Make the source fields required before an opportunity can move past stage one.
4. Ask the buyer. Add one open text question to your demo form and to the first call script. "How did you hear about us?" Then bucket the answers weekly.
5. Build five charts. Not fifteen. The spec is in the template below.
6. Review it weekly with sales. Same day, same time, same five charts. Decisions get written in the meeting notes, not in Slack.

Tim Dalrymple, writing in Kyle Poyar's Growth Unhinged, makes a point I agree with. Your measurement should match your stage and spend, and he estimates growth teams [waste 15 to 25% of budget](https://www.growthunhinged.com/p/guide-to-marketing-attribution) when they cannot see what works. His line, "there's no such thing as vibe attribution", belongs on the wall above your CRM.

![Three inputs feed two ledgers that feed a five chart dashboard reviewed weekly](/img/blog/gtm-box-day-9-attribution-pipeline-dashboard-1.png)

## Template one, field and UTM rules

Copy this into your RevOps doc. Change the allowed values to fit your channels, but keep the rules.

| Field or parameter | Where it lives | Rule | Allowed values (example) |
|---|---|---|---|
| utm_source | Every link | Lowercase, from list only | linkedin, google, newsletter, partner, event |
| utm_medium | Every link | Lowercase, from list only | paid, organic, email, referral, booth |
| utm_campaign | Every link | quarter_theme_asset format | q1_cnapp_webinar |
| utm_content | Paid and email links | Creative or variant name | video_a, carousel_b |
| utm_term | Paid search only | Keyword or audience | cnapp vendors |
| Original source | Contact and opportunity | Set once, never overwritten | Same list as utm_source plus outbound, direct |
| Latest source | Contact | Updates on every new conversion | Same list |
| Self reported source | Opportunity | Required before stage two, free text, bucketed weekly | Podcast, peer, LinkedIn post, analyst, search, AI answer, event |
| Partner involved | Opportunity | Required, yes or no plus partner name | Partner list from your program |
| Opportunity source | Opportunity | One value, sales and marketing agree at creation | Inbound, outbound, partner, event |

## Template two, the five chart dashboard spec

| Chart | Question it answers | Shape | Owner |
|---|---|---|---|
| 1. Sourced pipeline by channel | Which channel created pipeline this month | Stacked bar by month | Marketing |
| 2. Influenced pipeline by channel | Which channels touched open deals | Horizontal bar, sorted | Marketing |
| 3. Software vs self reported | Where the dark funnel hides | Paired bars per channel | RevOps |
| 4. Conversion and cost per opportunity | Which channel is cheapest per real opportunity | Table with trend arrows | Marketing and sales |
| 5. Pipeline pacing vs target | Are we on track for the quarter | Line against target line | Sales |

Chart five is the one your CEO will look at. Put it top left.

## Worked example

Illustrative numbers only, not from any real company.

- Quarter target pipeline is $900K. Week six shows $410K created, against a pacing line of $450K. Chart five turns amber.
- Chart one shows outbound sourced $180K, inbound $150K, partners $80K.
- Chart three shows software credits LinkedIn with 5% of opportunities. Self reported says 22% first heard of you from a LinkedIn post or a founder's comment.
- Chart four shows events at $1,400 per opportunity and content syndication at $3,100.

The decision writes itself. Move part of the syndication spend to founder led LinkedIn and one more event, then check chart five again in two weeks. That is the same loop that let our team support $2M of influenced pipeline a year on a $100K budget, written up in the [pipeline math post](https://syedcreates.com/2m-pipeline-100k-budget).

## Common mistakes

- Overwriting original source every time a contact converts again. You lose the very thing you wanted to know.
- Letting reps type "other" in the source field. Make "other" trigger a required note.
- Reporting influenced pipeline as if it were sourced. Your credibility drops and it does not come back fast.
- Treating self reported answers as gospel. Buyers forget. Use it to spot channels software misses, then test.
- Building the dashboard before the fields are clean. Garbage charts still look official.
- Skipping the weekly review. A dashboard nobody discusses is wallpaper.

If you are not sure your basics are in place, the [GTM health check](https://syedcreates.com/gtm-health-check) asks whether you know which channel sourced each deal last quarter. A "no" there means start with steps one to three.

## What to do today

1. Write one paragraph each for sourced, influenced and self reported, and send it to your sales lead for a yes.
2. Paste the UTM table into a shared doc and delete every value you do not actually use.
3. Add the self reported question to your demo form before you close your laptop.
4. Make original source and opportunity source required fields in your CRM.
5. Book a 30 minute weekly slot with sales called "Pipeline review" and put the five charts on the agenda.

Tomorrow, Day 10: Run and scale, the weekly operating rhythm and team playbook.

Subscribe to Pipeline Notes at https://syedhadi.substack.com so the final issue lands in your inbox.
