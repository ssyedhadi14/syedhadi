# Created by: Claude
# Date: 2026-10-28
# Purpose: Build syedcreates.com/tools, the GTM tool directory
# Owner: Syed Hadi

import html
import os
import sys

from partials import page

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "tools.html")

# (name, url or "", one liner, how I use it, best for, flags)
# flags: pick = daily driver, free = free tier, oss = open source
CATS = [
    ("AI and Agents", "The AI layer that does the busywork, so the team spends time on judgment.", [
        ("Claude Pro", "https://claude.ai", "The thinking partner behind research, drafts and every automation we run.",
         "Account research, PR drafts, battlecards and the scheduled workflows that run inside Slack. The marketing team's core AI workflow.",
         "Long context work, writing and agent workflows", {"pick"}),
        ("Viktor", "", "An AI colleague that lives in Slack and gets things done from a plain message.",
         "Lead exports from GA4, video uploads to Drive, review email drafts and recurring pulses for the marketing and SE teams.",
         "Teams that want automation without building an internal tool", {"pick"}),
        ("Magi", "", "An AI assistant for account based research and drafting.",
         "Part of the account based intelligence stack behind the AccuKnox inbound engine, alongside Factors.ai.",
         "Account research at speed", set()),
        ("Manus", "https://manus.im", "A general agent that takes a task and works through it end to end.",
         "Design and marketing tasks that need several steps chained together, from research to a finished asset.",
         "Multi step tasks you want handed off, not prompted", set()),
        ("Lovable", "https://lovable.dev", "Describe an app, get a working one. Our vibe coding workbench.",
         "Mission Control, the Price Quote Generator, the spends tracker, the Event Leads app and low fi landing pages.",
         "Internal tools and pages without waiting on engineering", {"pick"}),
    ]),
    ("Sales and Outbound", "Finding the right accounts, the right people and the moment they are ready.", [
        ("Apollo", "https://www.apollo.io", "Contact data plus sequencing for outbound campaigns.",
         "Prospect lists and outbound campaigns for the lead generation team across India and international territories.",
         "Building and running outbound sequences", {"pick"}),
        ("LinkedIn Sales Navigator", "https://business.linkedin.com/sales-solutions/sales-navigator", "The search layer on top of LinkedIn for finding buyers.",
         "Account mapping and outbound lead generation for SDRs and BDRs, plus partner account mapping with channel partners.",
         "Account based prospecting and buyer mapping", {"pick"}),
        ("Factors.ai", "https://www.factors.ai", "Shows which companies visit the site and what moved them.",
         "Website visitor enrichment and marketing attribution, one of the two partners behind our 5x marketing growth.",
         "B2B attribution and visitor intelligence", {"pick"}),
    ]),
    ("Email and Messaging", "Owned channels that reach people directly, without an algorithm in between.", [
        ("Brevo", "https://www.brevo.com", "Email campaigns, lists and automations in one place.",
         "Newsletters, product launch emails, G2 review campaigns and funnel lists from TOFU to PROD customers.",
         "Email marketing at startup scale", {"free"}),
        ("Wati", "https://www.wati.io", "WhatsApp Business API with a chatbot builder on top.",
         "The AI chatbot on the AccuKnox website, answering visitor questions before a human steps in.",
         "Conversational support on WhatsApp and the web", set()),
    ]),
    ("SEO and AI Visibility", "Ranking in Google is half the job now. The other half is getting cited by AI.", [
        ("LLMLabs", "", "Tracks how often AI answers mention and cite your brand.",
         "GEO analytics. It produced the leaderboard that put AccuKnox third in AI visibility, ahead of Sysdig and Prisma Cloud.",
         "Generative engine optimization and AI share of voice", {"pick"}),
        ("Open SEO", "", "Keyword and backlink research at a fraction of the usual price.",
         "Our low cost alternative to Ahrefs and Semrush for keyword research and content planning.",
         "Teams that need SEO data without enterprise pricing", set()),
        ("PostHog", "https://posthog.com", "Product analytics that shows what visitors actually do.",
         "Website visitor optimization, session level behavior and funnel checks on key pages.",
         "Understanding behavior behind the traffic numbers", {"free", "oss"}),
    ]),
    ("Paid Media and PR", "Spend that buys reach, and the wires that carry the news.", [
        ("LinkedIn Ads", "https://business.linkedin.com/marketing-solutions/ads", "Paid reach to the exact titles and companies we sell to.",
         "Leads and awareness campaigns across AI governance, LLM security and runtime protection, all in AccuKnox blue.",
         "B2B targeting by role, company and industry", set()),
        ("PRWeb", "https://www.prweb.com", "Press release distribution across news and search.",
         "Distribution for partnership and customer win announcements.",
         "Getting announcements indexed and syndicated", set()),
        ("Magazine Publications", "", "Placements in industry publications.",
         "Digital PR features and interviews that carry the AccuKnox story beyond our own channels.",
         "Earned style coverage and thought leadership", set()),
    ]),
    ("Design and Creative", "How a small team ships assets that look like a big team made them.", [
        ("Figma", "https://www.figma.com", "Where every design starts, from UX to ads.",
         "UX and marketing design, ad creatives, event posters and deck layouts shared across the team.",
         "Collaborative design and handoff", {"pick", "free"}),
        ("Freepik", "https://www.freepik.com", "Stock images, vectors and icons on demand.",
         "Images and icons for blogs, ads and social posts when a custom illustration is overkill.",
         "Fast visual assets", {"free"}),
        ("Flaticon", "https://www.flaticon.com", "A deep library of consistent icon sets.",
         "Icon sets for decks, one pagers and the website.",
         "Consistent icon styles across assets", {"free"}),
        ("Magnific", "https://magnific.ai", "AI upscaling that redraws detail into low resolution images.",
         "Upscaling event photos, screenshots and product visuals for print and large formats.",
         "Rescuing low resolution assets", set()),
        ("Excalidraw", "https://excalidraw.com", "A hand drawn style whiteboard for sketching ideas.",
         "Architecture sketches, GTM flows and quick diagrams before anything goes into Figma.",
         "Fast diagrams that do not need to look final", {"free", "oss"}),
    ]),
    ("Content and Video", "Formats that travel: recordings, live sessions, long form and every language.", [
        ("Loom", "https://www.loom.com", "Record your screen and face, share a link.",
         "Async walkthroughs, demo recordings and feedback that would otherwise take a meeting.",
         "Replacing meetings with short videos", {"free"}),
        ("Restream", "https://restream.io", "Go live on several platforms at once.",
         "The webinar hosting platform behind our partner webinars and live sessions.",
         "Multistreaming webinars and events", set()),
        ("Medium", "https://medium.com", "A publishing home with a built in reader network.",
         "Knowledge sharing and distribution for long form posts across AccuKnox.",
         "Reach beyond your own blog", {"free"}),
        ("ConveyThis", "https://www.conveythis.com", "Website translation without rebuilding pages.",
         "Translating accuknox.com for international markets, including the French site for our partners in France.",
         "Localizing a site for new regions", set()),
    ]),
    ("Website and Hosting", "The plumbing under accuknox.com. Boring when it works, which is the goal.", [
        ("Cloudways", "https://www.cloudways.com", "Managed cloud hosting for WordPress.",
         "Hosts the main AccuKnox website.",
         "WordPress hosting without managing servers", set()),
        ("Hostinger", "https://www.hostinger.com", "Affordable hosting for smaller sites.",
         "Website hosting for supporting sites and microsites.",
         "Low cost hosting for side properties", set()),
        ("WordPress Plugins", "https://wordpress.org/plugins/", "The extensions that keep a WordPress site fast and functional.",
         "Website efficiency, caching, SEO and page building on accuknox.com.",
         "Extending WordPress without custom code", set()),
        ("WP Forms", "https://wpforms.com", "Drag and drop forms for WordPress.",
         "Lead collection forms across the website, from demo requests to gated content.",
         "Lead capture on WordPress sites", set()),
    ]),
    ("Learning and Enablement", "Training that turns partners and customers into people who can sell and run the product.", [
        ("Arythmatic", "", "The learning management system behind AccuKnox training.",
         "Runs the partner and customer training portal, with self paced courses and self sign up.",
         "Structured product training at scale", set()),
    ]),
]

COLORS = ["#5b3df5", "#0ea5a4", "#e11d74", "#f59e0b", "#2563eb", "#16a34a", "#9333ea", "#dc2626", "#0891b2"]

EXTRA_CSS = """
<style>
.tools-hero{display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:end}
.tools-hero h1{font-size:clamp(56px,9vw,112px);font-weight:800;line-height:.98}
.tools-hero h1 em{font-style:normal;color:var(--accent);text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:10px}
.tools-hero p{font-size:18px;color:var(--ink-2)}
.tools-hero p b{color:var(--ink)}
.tbar{position:sticky;top:68px;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);padding:18px 0;border-bottom:1px solid var(--line)}
.tbar-in{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.tsearch{flex:1;min-width:240px;display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--card)}
.tsearch input{border:0;outline:0;background:transparent;font:inherit;color:var(--ink);width:100%}
.tsearch svg{width:18px;height:18px;color:var(--ink-3)}
.chipset{display:flex;gap:8px;flex-wrap:wrap}
.chipset button{font:600 14px Inter,sans-serif;padding:10px 16px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer}
.chipset button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.tselect{font:600 14px Inter,sans-serif;padding:10px 14px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.tcount{font-family:"JetBrains Mono",monospace;font-size:12px;color:var(--ink-3);margin-top:10px}
.tcat{padding:56px 0 8px}
.tcat-head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;border-bottom:2px solid var(--line);padding-bottom:14px;margin-bottom:20px}
.tcat-head h2{display:flex;align-items:center;gap:14px;font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(26px,3.4vw,38px);letter-spacing:-.02em}
.tcat-head h2 .num{font-size:clamp(34px,4.4vw,52px)}
.tcat-head .cnt{font:700 13px Inter;background:var(--accent);color:#fff;border-radius:999px;padding:3px 10px}
.tcat-head p{color:var(--ink-2);max-width:460px;text-align:right}
.tgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;align-items:start}
.tool{border:1px solid var(--line);border-radius:14px;background:var(--card);transition:border-color .15s,box-shadow .15s}
.tool:hover{border-color:var(--accent);box-shadow:var(--shadow)}
.tool summary{list-style:none;cursor:pointer;display:flex;gap:12px;padding:14px;align-items:flex-start}
.tool summary::-webkit-details-marker{display:none}
.tool .mono{flex:none;width:38px;height:38px;border-radius:10px;display:grid;place-items:center;color:#fff;font:800 14px "Bricolage Grotesque",sans-serif}
.tool .tn{font-weight:700;font-size:15px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.tool .tn .b{font:700 10px Inter;letter-spacing:.04em;padding:2px 6px;border-radius:5px;background:var(--accent-soft);color:var(--accent)}
.tool .tn .b.f{background:color-mix(in srgb,#16a34a 15%,transparent);color:#16a34a}
.tool .td{font-size:13.5px;color:var(--ink-2);line-height:1.45;margin-top:2px}
.tool .more{padding:0 14px 16px 64px;font-size:13.5px;color:var(--ink-2);display:grid;gap:8px}
.tool .more b{color:var(--ink);font-weight:600}
.tool .more a{color:var(--accent);font-weight:600}
.tool[open]{border-color:var(--accent)}
.tempty{display:none;text-align:center;padding:60px 0;color:var(--ink-3)}
.tsend{margin:60px 0 0;border:1px dashed var(--line);border-radius:22px;padding:40px;text-align:center}
.tsend h3{font-family:"Bricolage Grotesque";font-size:28px;font-weight:800;margin-bottom:8px}
.tsend p{color:var(--ink-2);margin-bottom:20px}
@media (max-width:1100px){.tgrid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:860px){.tools-hero{grid-template-columns:1fr}.tgrid{grid-template-columns:1fr 1fr}.tcat-head p{text-align:left}}
@media (max-width:560px){.tgrid{grid-template-columns:1fr}.tbar{top:60px}}
</style>"""

JS = """
<script>
(function(){
  var q=document.getElementById('tq'), cat=document.getElementById('tcat'), chips=document.querySelectorAll('.chipset button'), mode='all';
  function run(){
    var s=(q.value||'').toLowerCase().trim(), c=cat.value, shown=0;
    document.querySelectorAll('.tcat').forEach(function(sec){
      var n=0;
      sec.querySelectorAll('.tool').forEach(function(t){
        var ok=(!s||t.dataset.s.indexOf(s)>-1)&&(c==='all'||sec.dataset.c===c)&&(mode==='all'||t.dataset.f.indexOf(mode)>-1);
        t.style.display=ok?'':'none'; if(ok){n++;shown++;}
      });
      sec.style.display=n?'':'none';
    });
    document.getElementById('tshow').textContent=shown;
    document.getElementById('tempty').style.display=shown?'none':'block';
  }
  q.addEventListener('input',run); cat.addEventListener('change',run);
  chips.forEach(function(b){b.addEventListener('click',function(){chips.forEach(function(x){x.classList.remove('on')});b.classList.add('on');mode=b.dataset.m;run();});});
})();
</script>"""


def initials(name):
    parts = [p for p in name.replace(".", " ").split() if p]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else parts[0][1])).upper()


def build():
    total = sum(len(t) for _, _, t in CATS)
    opts = "".join(f'<option value="c{i}">{html.escape(n)}</option>' for i, (n, _, _) in enumerate(CATS, 1))
    body = EXTRA_CSS + f'''
<div class="tbar">
  <div class="wrap">
    <div class="tbar-in">
      <label class="tsearch"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="tq" type="search" placeholder="Search the tool directory" aria-label="Search tools"></label>
      <div class="chipset"><button class="on" data-m="all">Everything</button><button data-m="pick">My picks</button><button data-m="free">Free to use</button><button data-m="oss">Open source</button></div>
      <select id="tcat" class="tselect" aria-label="Filter by category"><option value="all">All categories</option>{opts}</select>
    </div>
    <div class="tcount">Showing <span id="tshow">{total}</span> of {total} tools</div>
  </div>
</div>
<div class="wrap">'''
    k = 0
    for i, (cname, cdesc, tools) in enumerate(CATS, 1):
        body += f'''
<section class="tcat" data-c="c{i}" id="cat-{i}">
  <div class="tcat-head"><h2><span class="num">{i:02d}</span>{html.escape(cname)} <span class="cnt">{len(tools)}</span></h2><p>{html.escape(cdesc)}</p></div>
  <div class="tgrid">'''
        for name, url, one, how, best, flags in tools:
            color = COLORS[k % len(COLORS)]
            k += 1
            badges = ""
            if "pick" in flags:
                badges += '<span class="b">PICK</span>'
            if "free" in flags:
                badges += '<span class="b f">FREE TIER</span>'
            if "oss" in flags:
                badges += '<span class="b f">OPEN SOURCE</span>'
            link = (f'<span><a href="{url}" target="_blank" rel="noopener nofollow">Visit {html.escape(name)} &rarr;</a></span>' if url else "")
            search = " ".join([name, one, how, best, cname]).lower()
            body += f'''
    <details class="tool" data-s="{html.escape(search)}" data-f="{' '.join(sorted(flags))}">
      <summary><span class="mono" style="background:{color}">{initials(name)}</span><span><span class="tn">{html.escape(name)}{badges}</span><span class="td">{html.escape(one)}</span></span></summary>
      <div class="more"><span><b>How I use it.</b> {html.escape(how)}</span><span><b>Best for.</b> {html.escape(best)}</span>{link}</div>
    </details>'''
        body += "\n  </div>\n</section>"
    body += '''
<div id="tempty" class="tempty">Nothing matches that search. Try a broader word.</div>
<div class="tsend reveal">
  <h3>Found something I am missing?</h3>
  <p>Send it over. If it survives a month of real GTM work, it goes on this page.</p>
  <a class="btn btn-primary" href="mailto:ssyedhadi14@gmail.com?subject=Tool%20suggestion">Send me a tool</a>
</div>
</div>''' + JS
    hero_p = (f"<b>{total} tools</b> in {len(CATS)} categories, behind a marketing, partnerships and SE function at an AI security startup. "
              "Every tool here is in daily or weekly use. Tap any card to see how I use it.")
    out = page("tools", "Tools | Syed Hadi", "", "Tools",
               'The GTM tools I <em>actually</em> use', hero_p, body)
    # swap the default page hero for the two column tools hero
    out = out.replace('<header class="page-hero">', '<header class="page-hero tools-page">', 1)
    return out, total


if __name__ == "__main__":
    try:
        out, total = build()
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote tools.html with", total, "tools")
    except OSError as e:
        sys.exit(f"Build failed: {e}")
