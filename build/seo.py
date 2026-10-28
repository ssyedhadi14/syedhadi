# Created by: Claude
# Date: 2026-10-28
# Purpose: SEO metadata, structured data and crawl files for syedcreates.com
# Owner: Syed Hadi

import json

SITE = "https://syedcreates.com"
OG_IMAGE = f"{SITE}/img/og-card.jpg"

# key: (path, title <=60, description <=160)
META = {
    "home": ("", "Syed Hadi | Product Marketing and Partnerships Lead",
             "Syed Hadi leads product marketing and channel partnerships at AccuKnox, building GTM and pipeline for AI security and cloud security in Bengaluru."),
    "gtm": ("gtm-engine.html", "AI Native GTM Engine and AI Search Growth | Syed Hadi",
            "How an AI native GTM engine put AccuKnox ahead of Sysdig in AI visibility, grew website sessions 240% in 90 days and ranked for CNAPP vendors."),
    "systems": ("systems.html", "GTM Systems, Apps and AI Agents | Syed Hadi",
                "Vibe coded apps, Slack agents and self driving dashboards built by the AccuKnox marketing team. Quotes that took days now take minutes."),
    "recognition": ("recognition.html", "Campaigns and Analyst Recognition | Syed Hadi",
                    "AccuKnox campaigns, 12 live moments in a quarter and analyst recognition from Gartner, Frost and Sullivan, KuppingerCole, Omdia and GigaOm."),
    "playbook": ("playbook.html", "B2B Marketing Playbook for 2026 | Syed Hadi",
                 "Why the old B2B playbook is dead, six initiatives that drive revenue, the AI tool stack and agent architecture a PMM lead runs in 2026."),
    "events": ("events.html", "Events, Talks and Meetups in 2026 | Syed Hadi",
               "Photos and notes from KubeCon India, BSides Bangalore, the CNCF day at NetApp, GrowthX GTM Deep Dive and Marketing After Hours."),
    "writing": ("writing.html", "Articles on AI Security and GTM | Syed Hadi",
                "Ten long form articles on CNAPP, shadow AI, prompt firewalls, AI SOC, CERT-In reporting and non human identity, written through a GTM lens."),
    "tools": ("tools.html", "GTM and Marketing Tools I Actually Use | Syed Hadi",
              "30 tools behind a B2B security startup's GTM: Claude, Apollo, Factors.ai, Sales Navigator, Lovable, Brevo, LLMLabs, Figma and more, with how each is used."),
}

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": "Syed Hadi",
    "url": SITE + "/",
    "image": f"{SITE}/photo.jpg",
    "jobTitle": "Product Marketing and Partnerships Lead",
    "worksFor": {"@type": "Organization", "name": "AccuKnox", "url": "https://accuknox.com"},
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "Birla Institute of Technology and Science, Pilani"},
        {"@type": "CollegeOrUniversity", "name": "St. Peter's College of Engineering and Technology"},
    ],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressRegion": "Karnataka", "addressCountry": "IN"},
    "knowsAbout": ["Product Marketing", "Go to Market Strategy", "Channel Partnerships", "AI Security",
                   "Cloud Security", "CNAPP", "Demand Generation", "Community Building"],
    "sameAs": ["https://www.linkedin.com/in/syedhadii/"],
}


def jsonld(key, label):
    path, title, desc = META[key]
    url = f"{SITE}/{path}"
    if key == "home":
        graph = [
            {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/", "name": "Syed Hadi", "publisher": {"@id": f"{SITE}/#person"}},
            {"@type": "ProfilePage", "url": url, "name": title, "description": desc, "mainEntity": {"@id": f"{SITE}/#person"}},
            PERSON,
        ]
    else:
        graph = [
            {"@type": "WebPage", "url": url, "name": title, "description": desc,
             "isPartOf": {"@id": f"{SITE}/#website"}, "author": {"@id": f"{SITE}/#person"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": url}]},
        ]
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def meta_tags(key, label):
    path, title, desc = META[key]
    url = f"{SITE}/{path}"
    return f'''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Syed Hadi">
<meta name="theme-color" content="#5b3df5">
<meta property="og:type" content="{'profile' if key == 'home' else 'website'}">
<meta property="og:site_name" content="Syed Hadi">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">
{jsonld(key, label)}'''
