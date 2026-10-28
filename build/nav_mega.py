# Created by: Claude
# Date: 2026-10-28
# Purpose: Mega menu navigation for syedcreates.com, modeled on atharvashah.com
# Owner: Syed Hadi

ICONS = {
    "pmm": '<path d="M3 11l18-8-8 18-2-8-8-2z"/>',
    "partner": '<path d="M8 12l3 3 5-6"/><circle cx="12" cy="12" r="10"/>',
    "gtm": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-6"/>',
    "pipe": '<path d="M4 4h16v4H4zM6 8v4h12V8M8 12v4h8v-4M10 16v4h4v-4"/>',
    "comm": '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M15 20c0-2 1.3-4 4-4"/>',
    "ai": '<rect x="5" y="7" width="14" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9 16h6"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    "deck": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "star": '<path d="m12 2 3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/>',
}


def ico(k, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>')


# key, icon, title, tagline, description, outcomes, who, tools, card title, card text, done before, cta, href
WORK = [
    ("pmm", "pmm", "Product Marketing", "Positioning buyers repeat",
     "Most security products lose deals on clarity, not features. I build the positioning, personas and launch plans that make a technical product easy to buy.",
     ["Positioning and messaging that sales actually uses", "Buyer personas mapped to real objections",
      "Launch plans with content, events and enablement", "Battlecards and one pagers for every competitor"],
     ["Security startups", "Founders", "Sales teams"], ["Figma", "Claude", "Lovable", "WordPress"],
     "A product story the whole company tells the same way",
     "First product marketer at AccuKnox, from the founding team to leading growth.",
     "ARR grew from $500K to $1M+ with the growth team", "See the GTM engine", "gtm-engine.html"),
    ("partner", "partner", "Channel Partnerships", "Partners who sell, not sign",
     "A partner agreement is the start, not the win. I run programs that turn distributors, MSSPs and resellers into joint pipeline.",
     ["Partner programs with tiers, deal reg and enablement", "Account mapping with each partner's sellers",
      "Joint webinars, PR and co marketing", "Monthly business reviews that track real pipeline"],
     ["Distributors", "MSSPs", "Resellers", "Alliances"], ["Sales Navigator", "Salesforce", "Apollo", "Brevo"],
     "Partner sourced pipeline you can trace",
     "Partner programs across AI security and cloud security in India, MENA, APAC, Europe, Africa and the US.",
     "Programs covering over $35B in annual TAM", "See the recognition", "recognition.html"),
    ("gtm", "gtm", "GTM Strategy", "Decisions under market pressure",
     "ICP, pricing, channels and the launch plan. I make the calls that turn a release into qualified demand, then test them against the market.",
     ["ICP and segment definition", "Pricing and packaging input",
      "Channel mix across inbound, outbound and partners", "Launch plans with clear owners and dates"],
     ["Startups", "Growth leaders", "Product teams"], ["Factors.ai", "Apollo", "Sales Navigator", "Claude"],
     "A go to market plan with owners, not slides",
     "Hosted the GTM Deep Dive at GrowthX, where teams made and defended live GTM calls.",
     "GTM for new product lines drove a sharp rise in inbound", "Read the playbook", "playbook.html"),
    ("pipe", "pipe", "Demand and Pipeline", "Spend tied to one number",
     "Every channel reports into influenced pipeline. Paid, SEO, AI search, email and events all answer to the same metric.",
     ["Attribution that shows what moved a deal", "SEO and AI search visibility programs",
      "LinkedIn ads and email run as one program", "Monthly reporting without manual exports"],
     ["B2B SaaS", "Marketing leads", "Founders"], ["Factors.ai", "LLMLabs", "LinkedIn Ads", "Brevo"],
     "Pipeline you can explain line by line",
     "Third in AI visibility for security, ahead of Sysdig and Prisma Cloud.",
     "$2M influenced pipeline on $100K a year", "See the GTM engine", "gtm-engine.html"),
    ("comm", "comm", "Community and Events", "Rooms full of practitioners",
     "Meetups, booths, CTFs and hands on labs that put the product in front of the people who will use it.",
     ["Meetups and community days with partners", "Conference booths with a reason to stop",
      "CTFs and labs that grow open source projects", "Webinars that sellers can reuse"],
     ["Open source projects", "DevRel teams", "Event marketers"], ["Restream", "Loom", "Figma", "Brevo"],
     "Events that leave pipeline behind",
     "KubeCon India, BSides Bangalore, the CNCF day at NetApp and GrowthX.",
     "500+ CTF sign ups and 300+ GitHub stars at KubeCon India", "See the events", "events.html"),
    ("ai", "ai", "AI Systems for GTM", "Busywork, automated",
     "Vibe coded apps, Slack agents and self driving dashboards that let a small team ship like a big one.",
     ["Internal apps for quotes, spends and lead capture", "Agents that draft, export and report from Slack",
      "Dashboards that refresh themselves", "A tool stack the team actually adopts"],
     ["Marketing teams", "RevOps", "Small teams"], ["Claude", "Lovable", "Viktor", "PostHog"],
     "Quotes that took days now take minutes",
     "Mission Control, the Price Quote Generator, the Event Leads app and more.",
     "Five org wide apps shipped by marketing", "See the systems", "systems.html"),
]

PORTFOLIO_FEATURED = [
    ("gtm-engine.html", "img/marketing-after-hours.jpg", "GTM Engine",
     "AI search, inbound growth and the stack behind a 240% jump in sessions.", "Explore"),
    ("events.html", "img/bsides-2026.jpg", "Events",
     "KubeCon, BSides, CNCF and GrowthX. Every room, with photos.", "See photos"),
]
PORTFOLIO_LINKS = [("systems.html", "ai", "Systems"), ("recognition.html", "star", "Recognition"),
                   ("playbook.html", "pen", "Playbook"), ("writing.html", "doc", "Writing")]

TILES = [("#5b3df5", "CP"), ("#0ea5a4", "VI"), ("#e11d74", "AP"), ("#f59e0b", "FA"), ("#2563eb", "LS"),
         ("#16a34a", "BR"), ("#9333ea", "LL"), ("#dc2626", "FI"), ("#0891b2", "LO"), ("#5b3df5", "PO"),
         ("#e11d74", "EX"), ("#f59e0b", "WA")]


def mega_nav(RESUME, DECK, CALENDLY, LINKEDIN):
    chev = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>'
    arr = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 6 6 6-6 6"/></svg>'

    left, panels = "", ""
    for i, (k, ic, t, tag, desc, outs, who, tools, ct, ctext, done, cta, href) in enumerate(WORK):
        on = " on" if i == 0 else ""
        left += (f'<a href="{href}" class="mw-item{on}" data-k="{k}"><span class="mw-ic">{ico(ic)}</span>'
                 f'<span class="mw-t"><b>{t}</b><small>{tag}</small></span>{arr}</a>')
        outs_h = "".join(f"<li>{o}</li>" for o in outs)
        who_h = "".join(f"<span>{w}</span>" for w in who)
        tools_h = "".join(f"<span>{x}</span>" for x in tools)
        panels += (
            f'<div class="mw-panel{on}" data-k="{k}">'
            f'<div class="mw-mid"><div class="mw-h"><span class="mw-ic big">{ico(ic)}</span><h4>{t}</h4></div><p>{desc}</p>'
            f'<h5>OUTCOMES</h5><ul>{outs_h}</ul>'
            f'<h5>WHO THIS IS FOR</h5><div class="mw-who">{who_h}</div>'
            f'<h5>TOOLS AND PLATFORMS</h5><div class="mw-tools">{tools_h}</div></div>'
            f'<div class="mw-card"><span class="k">WHAT TO EXPECT</span><div class="art">{ico(ic)}</div>'
            f'<h4>{ct}</h4><p>{ctext}</p><p class="done"><b>Done before.</b> {done}</p>'
            f'<a class="go" href="{href}">{cta} <span>&rarr;</span></a></div></div>')
    work_simple = "".join(f'<a href="{w[12]}">{w[2]}</a>' for w in WORK)

    feat = "".join(
        f'<a class="pf-card" href="{h}"><span class="pf-img"><img src="/{img}" alt="{t}" loading="lazy" width="600" height="375"></span>'
        f'<span class="pf-body"><b>{t}</b><small>{d}</small><em>{c} &rarr;</em></span></a>'
        for h, img, t, d, c in PORTFOLIO_FEATURED)
    plinks = "".join(f'<a href="{h}">{ico(ic)}{t}</a>' for h, ic, t in PORTFOLIO_LINKS)
    port_simple = ("".join(f'<a href="{h}">{t}</a>' for h, _, t, _, _ in PORTFOLIO_FEATURED)
                   + "".join(f'<a href="{h}">{t}</a>' for h, _, t in PORTFOLIO_LINKS))

    tiles = "".join(f'<i style="background:{c}">{l}</i>' for c, l in TILES)
    tools_cards = (
        f'<a class="pf-card" href="tools.html"><span class="pf-img tiles"><span class="badge-f">FEATURED</span>{tiles}</span>'
        f'<span class="pf-body"><b>Tool Directory</b><small>30 GTM tools in 9 categories, with how each one is used.</small><em>Browse tools &rarr;</em></span></a>'
        f'<a class="pf-card" href="{DECK}" target="_blank" rel="noopener"><span class="pf-img deckart"><span class="badge-f">NEW</span>'
        f'<span class="deck-t">Building an<br><b>AI native</b><br>GTM engine</span></span>'
        f'<span class="pf-body"><b>Workproof Deck</b><small>The full product marketing workproof, May 2024 to date.</small><em>Open the deck &rarr;</em></span></a>')
    tool_links = (f'<a href="tools.html#cat-1">{ico("ai")}AI and Agents</a>'
                  f'<a href="tools.html#cat-2">{ico("partner")}Sales and Outbound</a>'
                  f'<a href="tools.html#cat-4">{ico("gtm")}SEO and AI Visibility</a>'
                  f'<a href="tools.html#cat-6">{ico("grid")}Design and Creative</a>'
                  f'<a href="{CALENDLY}" target="_blank" rel="noopener">{ico("cal")}Schedule meeting</a>')

    theme = ('<button class="theme-btn" id="themeBtn" aria-label="Toggle theme"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>')

    return f'''<nav>
  <div class="wrap nav-in">
    <a href="/" class="brand"><img src="/img/avatar.jpg" alt="Syed Hadi" width="40" height="40">Syed Hadi</a>
    <div class="nav-links" id="navLinks">
      <div class="dd mega" data-group="work">
        <button class="dd-btn" aria-haspopup="true" aria-expanded="false" data-group="work">Work {chev}</button>
        <div class="dd-menu mm mm-work"><div class="mw-left">{left}</div><div class="mw-right">{panels}</div></div>
        <div class="mm-simple">{work_simple}</div>
      </div>
      <div class="dd mega" data-group="portfolio">
        <button class="dd-btn" aria-haspopup="true" aria-expanded="false" data-group="portfolio">Portfolio {chev}</button>
        <div class="dd-menu mm mm-port"><div class="pf-grid">{feat}</div><div class="pf-links">{plinks}</div></div>
        <div class="mm-simple">{port_simple}</div>
      </div>
      <div class="dd mega" data-group="tools">
        <button class="dd-btn" aria-haspopup="true" aria-expanded="false" data-group="tools">Tools {chev}</button>
        <div class="dd-menu mm mm-port"><div class="pf-grid">{tools_cards}</div><div class="pf-links">{tool_links}</div></div>
        <div class="mm-simple"><a href="tools.html">Tool Directory</a><a href="{DECK}" target="_blank" rel="noopener">Workproof Deck</a></div>
      </div>
      <a href="writing.html" data-p="writing">Writing</a>
      <a class="m-only" href="{RESUME}" target="_blank" rel="noopener">Resume</a>
    </div>
    <div class="nav-right">
      {theme}
      <div class="dd small hide-sm">
        <button class="btn btn-ghost dd-btn" aria-haspopup="true" aria-expanded="false">Resume {chev}</button>
        <div class="dd-menu mm-small">
          <a href="{RESUME}" target="_blank" rel="noopener">{ico("doc")}Resume, PDF</a>
          <a href="{DECK}" target="_blank" rel="noopener">{ico("deck")}Workproof Deck</a>
          <a href="{LINKEDIN}" target="_blank" rel="noopener">{ico("in")}LinkedIn Profile</a>
        </div>
      </div>
      <a class="btn btn-primary" href="{CALENDLY}" target="_blank" rel="noopener">{ico("cal")}<span>Schedule meeting</span></a>
      <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</nav>'''
