#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-04
# Purpose: Build the scheduled Pipeline Notes blog posts for syedcreates.com from Markdown sources in build/pipeline_notes/.
#          Writes the article pages, diagrams, covers, blog cards, sitemap, search index and llms.txt entries,
#          plus functions/_middleware.js, which hides each post at the edge until 9 AM IST on its date.
#          Also writes Substack ready HTML copies to /home/claude/substack/notes/.
# Owner: Syed Hadi
# Usage: python3 build/pipeline_notes.py   (idempotent, safe to rerun)
import glob
import html
import json
import os
import re
import subprocess
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
SRC = os.path.join(ROOT, "build", "pipeline_notes")
TEMPLATE = os.path.join(SITE, "how-to-build-a-saas-partner-program.html")
SUB_OUT = "/home/claude/substack/notes"
BASE = "https://syedcreates.com"
PUB_HOUR_UTC = "03:30:00Z"  # 9:00 AM IST
MOTIF = {"gtm-plays-behind-0-to-10m": "rocket", "ai-search-cnapp-240-percent": "search", "fire-math-epf-ppf-nps": "coins",
         "one-line-positioning-test": "megaphone", "partner-programs-that-ship-pipeline": "puzzle", "2m-pipeline-100k-budget": "funnel",
         "23-content-types-5-that-sold": "doc", "salary-in-2046": "chart", "gtm-lessons-from-leaders-2026": "sparkles", "0-to-10m-10-lessons": "trophy"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)


def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n(.*)$", raw, flags=re.S)
        if not m:
            fail(f"no front matter in {f}")
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            fail(f"bad front matter JSON in {f}: {e}")
        meta["body_md"] = m.group(2).strip()
        for k in ("slug", "date", "section", "title", "description", "h1", "h1_accent", "cover_text", "cover_accent"):
            if not meta.get(k):
                fail(f"{f} missing {k}")
        posts.append(meta)
    return sorted(posts, key=lambda p: p["date"])


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]


def nice_date(d):
    y, mo, da = d.split("-")
    return f"{MONTHS[int(mo) - 1]} {int(da)}, {y}"


def body_html(p):
    h = markdown.markdown(p["body_md"], extensions=["extra", "sane_lists"])
    # heading ids
    def hid(m):
        lvl, inner = m.group(1), m.group(2)
        return f'<h{lvl} id="{slugify(inner)}">{inner}</h{lvl}>'
    h = re.sub(r"<h([23])>(.*?)</h\1>", hid, h)
    # images become figures with lazy loading
    def fig(m):
        alt, src = m.group(1), m.group(2)
        return (f'<figure class="pn-fig"><img src="{src}" alt="{alt}" width="1200" height="675" loading="lazy" decoding="async">'
                f'<figcaption>{alt}</figcaption></figure>')
    h = re.sub(r'<p>\s*<img alt="([^"]*)" src="([^"]*)"\s*/?>\s*</p>', fig, h)
    # external links open in a new tab
    def ext(m):
        href = m.group(1)
        if href.startswith(BASE) or href.startswith("/") or href.startswith("#"):
            return f'<a href="{href}">'
        return f'<a href="{href}" target="_blank" rel="noopener">'
    h = re.sub(r'<a href="([^"]+)">', ext, h)
    return h


def headings(p):
    return [[re.sub(r"<[^>]+>", "", t), slugify(t)] for t in re.findall(r"^##\s+(.+)$", p["body_md"], flags=re.M)]


def render_page(p, tpl):
    slug, url = p["slug"], f'{BASE}/{p["slug"]}'
    title = html.escape(p["title"], quote=True)
    desc = html.escape(p["description"], quote=True)
    cover_alt = html.escape(f'{p["cover_text"]} {p["cover_accent"]}', quote=True)
    t = tpl
    t = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", t, count=1)
    reps = {
        r'<meta name="description" content="[^"]*">': f'<meta name="description" content="{desc}">',
        r'<link rel="canonical" href="[^"]*">': f'<link rel="canonical" href="{url}">',
        r'<meta property="article:published_time" content="[^"]*">': f'<meta property="article:published_time" content="{p["date"]}">',
        r'<meta property="article:modified_time" content="[^"]*">': f'<meta property="article:modified_time" content="{p["date"]}">',
        r'<meta property="article:section" content="[^"]*">': f'<meta property="article:section" content="{p["section"]}">',
        r'<meta property="og:url" content="[^"]*">': f'<meta property="og:url" content="{url}">',
        r'<meta property="og:title" content="[^"]*">': f'<meta property="og:title" content="{title}">',
        r'<meta property="og:description" content="[^"]*">': f'<meta property="og:description" content="{desc}">',
        r'<meta property="og:image" content="[^"]*">': f'<meta property="og:image" content="{BASE}/img/covers/og/{slug}.jpg">',
        r'<meta property="og:image:alt" content="[^"]*">': f'<meta property="og:image:alt" content="{cover_alt}">',
        r'<meta name="twitter:title" content="[^"]*">': f'<meta name="twitter:title" content="{title}">',
        r'<meta name="twitter:description" content="[^"]*">': f'<meta name="twitter:description" content="{desc}">',
        r'<meta name="twitter:image" content="[^"]*">': f'<meta name="twitter:image" content="{BASE}/img/covers/og/{slug}.jpg">',
    }
    for pat, new in reps.items():
        t, n = re.subn(pat, lambda m, new=new: new, t, count=1)
        if n != 1:
            fail(f"template pattern missing: {pat}")
    # structured data: replace the WebPage and BlogPosting blocks
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "url": url, "name": p["title"], "description": p["description"],
         "isPartOf": {"@id": f"{BASE}/#website"}, "author": {"@id": f"{BASE}/#person"}, "inLanguage": "en-IN"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]}
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
            "image": f"{BASE}/img/covers/og/{slug}.jpg", "datePublished": p["date"], "dateModified": p["date"],
            "author": {"@id": f"{BASE}/#person"}, "publisher": {"@id": f"{BASE}/#person"},
            "mainEntityOfPage": url, "articleSection": p["section"], "isPartOf": {"@type": "Blog", "name": "Pipeline Notes", "url": f"{BASE}/blog"},
            "keywords": ", ".join(p.get("tags", []))}
    blocks = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S))
    for m in reversed(blocks):
        body = m.group(1)
        if '"BreadcrumbList"' in body and '"WebPage"' in body:
            new = json.dumps(graph, ensure_ascii=False)
        elif '"BlogPosting"' in body:
            new = json.dumps(post, ensure_ascii=False)
        else:
            continue
        t = t[:m.start(1)] + new + t[m.end(1):]
    # hero
    t = re.sub(r'<div class="crumbs">.*?</div>', "<div class=\"crumbs\"><a href='/'>Home</a> / <a href='/blog'>Blog</a> / Pipeline Notes</div>", t, count=1, flags=re.S)
    t = re.sub(r'<h1 class="display">.*?</h1>', f'<h1 class="display">{html.escape(p["h1"])} <span class="tg1">{html.escape(p["h1_accent"])}</span></h1>', t, count=1, flags=re.S)
    t = re.sub(r'(</h1>\s*)<p>.*?</p>', lambda m: m.group(1) + f"<p>{desc}</p>", t, count=1, flags=re.S)
    t = re.sub(r'<figure class="hero-cv"><img src="[^"]*" alt="[^"]*"',
               f'<figure class="hero-cv"><img src="/img/covers/{slug}.jpg" alt="{cover_alt}"', t, count=1)
    # byline and body
    t = re.sub(r'<small>[^<]*&middot;[^<]*</small>', f'<small>{nice_date(p["date"])} &middot; {html.escape(p["section"])} &middot; Pipeline Notes</small>', t, count=1)
    a, b = t.find('<article class="pt-body">'), t.find("</article>")
    if a < 0 or b < 0:
        fail("template article body missing")
    t = t[:a] + '<article class="pt-body">' + body_html(p) + t[b:]
    # bottom CTA: subscribe plus meeting
    t = re.sub(r'<div class="pt-cta reveal">.*?</div>\s*</div>',
               '<div class="pt-cta reveal"><b>Get the next Pipeline Notes issue</b><p>One GTM play you can run this week, with the numbers behind it. Free, every Tuesday.</p>'
               '<div class="bx-ctas" style="justify-content:flex-start"><a class=\'btn btn-primary\' data-track=\'substack_click\' href=\'https://syedhadi.substack.com\' target=\'_blank\' rel=\'noopener\'>Subscribe on Substack</a>'
               '<a class=\'btn btn-ghost\' data-track=\'schedule_click\' href=\'/schedule-meeting\'>Schedule meeting</a></div></div>',
               t, count=1, flags=re.S)
    return t


def card(p):
    alt = html.escape(f'{p["cover_text"]} {p["cover_accent"]}', quote=True)
    return (f"<a data-bs-kind='notes' data-pub='{p['date']}T{PUB_HOUR_UTC}' class='bf-card reveal' href='/{p['slug']}'>"
            f'<span class="cv-thumb"><img src="/img/covers/{p["slug"]}.jpg" alt="{alt}" width="1200" height="750" loading="lazy" decoding="async"></span>'
            f'<small>{html.escape(p["section"])} &middot; {nice_date(p["date"])}</small><b>{html.escape(p["title"])}</b>'
            f'<span>{html.escape(p["description"])}</span><em>Read &rarr;</em></a>')


def update_blog(posts):
    path = os.path.join(SITE, "blog.html")
    t = open(path, encoding="utf-8").read()
    cards = "".join(card(p) for p in sorted(posts, key=lambda p: p["date"], reverse=True))
    first = min(p["date"] for p in posts)
    sec = (f'<!--pn:start--><section class="bf-sec" style="padding-top:8px" data-bs-sec data-pub="{first}T{PUB_HOUR_UTC}"><div class="wrap">'
           '<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Newsletter</span>'
           '<h2 class="display" id="s-pipeline-notes">Pipeline <span class="t2">Notes</span></h2>'
           '<p>Weekly GTM plays with the numbers behind them. Also on <a href="https://syedhadi.substack.com" target="_blank" rel="noopener">Substack</a>.</p></div>'
           f'<div class="bf-grid">{cards}</div></div></section><!--pn:end-->')
    if "<!--pn:start-->" in t:
        t = re.sub(r"<!--pn:start-->.*?<!--pn:end-->", lambda m: sec, t, flags=re.S)
    else:
        anchor = '<section class="bf-sec" style="padding-top:8px" data-bs-sec>'
        if anchor not in t:
            fail("blog anchor missing")
        t = t.replace(anchor, sec + "\n" + anchor, 1)
    chip = '<button class="bs-chip" type="button" data-k="notes">Pipeline Notes</button>'
    if chip not in t:
        t = t.replace('<button class="bs-chip" type="button" data-k="guide">Guides</button>',
                      '<button class="bs-chip" type="button" data-k="guide">Guides</button>' + chip, 1)
    open(path, "w", encoding="utf-8").write(t)


def update_sitemap(posts):
    path = os.path.join(SITE, "sitemap.xml")
    t = open(path, encoding="utf-8").read()
    for p in posts:
        loc = f'{BASE}/{p["slug"]}'
        t = re.sub(r"\s*<url><loc>" + re.escape(loc) + r"</loc>.*?</url>", "", t)
        t = t.replace("</urlset>", f"  <url><loc>{loc}</loc><lastmod>{p['date']}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>")
    open(path, "w", encoding="utf-8").write(t)


def update_search(posts):
    path = os.path.join(SITE, "assets", "search-index.json")
    data = json.load(open(path, encoding="utf-8"))
    slugs = {"/" + p["slug"] for p in posts}
    data["pages"] = [x for x in data["pages"] if x.get("u") not in slugs]
    for p in posts:
        data["pages"].append({"u": "/" + p["slug"], "t": p["title"], "s": f'{p["h1"]} {p["h1_accent"]}', "d": p["description"],
                              "k": " ".join(p.get("tags", [])), "c": "Pipeline Notes", "h": headings(p)})
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))


def update_llms(posts):
    path = os.path.join(SITE, "llms.txt")
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"\n## Pipeline Notes\n.*?(?=\n## )", "\n", t, flags=re.S)
    lines = "".join(f'- [{p["title"]}]({BASE}/{p["slug"]}): {p["description"]}\n' for p in posts)
    block = "\n## Pipeline Notes\n" + lines
    t = t.replace("\n## Insights\n", block + "\n## Insights\n", 1) if "\n## Insights\n" in t else t + block
    open(path, "w", encoding="utf-8").write(t)


MIDDLEWARE = """// Created by: Claude
// Date: 2026-11-04
// Purpose: Scheduled publishing for Pipeline Notes posts. Until a post's time arrives, its page returns 404 and it is
//          removed from /blog, /sitemap.xml, /llms.txt and the search index. Generated by build/pipeline_notes.py.
// Owner: Syed Hadi
const SCHEDULE = __SCHEDULE__;

function futureSlugs(now) {
  return Object.keys(SCHEDULE).filter((s) => now < Date.parse(SCHEDULE[s]));
}

function withHeaders(res, cache) {
  const h = new Headers(res.headers);
  h.set('Cache-Control', cache);
  h.delete('Content-Length');
  return h;
}

export async function onRequest(ctx) {
  const url = new URL(ctx.request.url);
  const now = ctx.env.SCHEDULE_NOW ? Date.parse(ctx.env.SCHEDULE_NOW) : Date.now();
  const future = futureSlugs(now);
  if (!future.length) return ctx.next();
  const path = url.pathname.replace(/\\/+$/, '') || '/';
  const slug = path.slice(1).replace(/\\.html$/, '');
  try {
    if (future.includes(slug)) {
      const nf = await ctx.env.ASSETS.fetch(new URL('/404.html', url));
      return new Response(nf.body, { status: 404, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } });
    }
    const res = await ctx.next();
    if (res.status !== 200) return res;
    if (path === '/blog' || path === '/blog.html') {
      const out = new HTMLRewriter().on('[data-pub]', {
        element(el) { if (now < Date.parse(el.getAttribute('data-pub'))) el.remove(); },
      }).transform(res);
      return new Response(out.body, { status: 200, headers: withHeaders(res, 'public, max-age=0, must-revalidate') });
    }
    let text = await res.text();
    if (path === '/sitemap.xml') {
      for (const s of future) text = text.replace(new RegExp('\\\\s*<url><loc>https://syedcreates\\\\.com/' + s + '</loc>.*?</url>', 'g'), '');
    } else if (path === '/llms.txt' || path === '/llms-full.txt') {
      text = text.split('\\n').filter((l) => !future.some((s) => l.includes('syedcreates.com/' + s + ')'))).join('\\n');
    } else if (path === '/assets/search-index.json') {
      const data = JSON.parse(text);
      data.pages = data.pages.filter((p) => !future.includes(String(p.u || '').replace(/^\\//, '')));
      text = JSON.stringify(data);
    }
    return new Response(text, { status: 200, headers: withHeaders(res, 'public, max-age=300') });
  } catch (e) {
    return ctx.next();
  }
}
"""


def write_edge(posts):
    sched = {p["slug"]: f'{p["date"]}T{PUB_HOUR_UTC}' for p in posts}
    js = MIDDLEWARE.replace("__SCHEDULE__", json.dumps(sched, indent=2))
    open(os.path.join(ROOT, "functions", "_middleware.js"), "w", encoding="utf-8").write(js)
    include = ["/api/*", "/medium-feed", "/blog", "/blog.html", "/sitemap.xml", "/llms.txt", "/llms-full.txt", "/assets/search-index.json"]
    for p in posts:
        include += [f'/{p["slug"]}', f'/{p["slug"]}.html']
    json.dump({"version": 1, "include": include, "exclude": []}, open(os.path.join(SITE, "_routes.json"), "w"), indent=2)


def diagrams(posts):
    os.makedirs(os.path.join(SITE, "img", "blog"), exist_ok=True)
    todo = []
    for p in posts:
        svg = os.path.join(SRC, "img", f'{p["slug"]}-1.svg')
        png = os.path.join(SITE, "img", "blog", f'{p["slug"]}-1.png')
        if os.path.exists(svg):
            todo.append((svg, png))
    if not todo:
        return
    js = os.path.join(SRC, "_svg2png.js")
    open(js, "w").write("""const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:675},deviceScaleFactor:1.5});
const jobs=JSON.parse(process.argv[2]);for(const [svg,png] of jobs){
await p.setContent('<html><head><style>@font-face{font-family:"Plus Jakarta Sans";src:url(file://"""
                             + SITE + """/assets/fonts/web/plus-jakarta-sans-latin-700-normal.woff2)}html,body{margin:0}svg{display:block;width:1200px;height:675px}</style></head><body>'+fs.readFileSync(svg,'utf8')+'</body></html>');
await p.waitForTimeout(150);await p.screenshot({path:png,clip:{x:0,y:0,width:1200,height:675}});}
await b.close();})();""")
    env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
    r = subprocess.run(["node", js, json.dumps(todo)], cwd="/home/claude/tools", env=env, capture_output=True, text=True)
    if r.returncode:
        fail("diagram render failed: " + r.stderr[-500:])
    os.remove(js)


def covers(posts):
    cfg = os.path.join(ROOT, "build", "covers", "config.py")
    t = open(cfg, encoding="utf-8").read()
    added = []
    for p in posts:
        key = json.dumps(p["slug"])
        val = "(" + ", ".join(json.dumps(x) for x in (p["cover_text"], p["cover_accent"], p.get("cover_tag", "Pipeline Notes"), p.get("motif") or MOTIF.get(p["slug"], "chart"))) + ")"
        line = f"    {key}: {val},\n"
        if key + ":" in t:
            t = re.sub(r"    " + re.escape(key) + r": \(.*?\),\n", lambda m: line, t)
        else:
            t = re.sub(r"(COVERS\s*=\s*\{\n)", lambda m: m.group(1) + line, t, count=1)
        added.append(p["slug"])
    open(cfg, "w", encoding="utf-8").write(t)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "build", "covers", "render.py")] + added, capture_output=True, text=True)
    if r.returncode:
        fail("cover render failed: " + r.stderr[-800:])


def substack_copies(posts):
    os.makedirs(SUB_OUT, exist_ok=True)
    for p in posts:
        h = body_html(p)
        h = h.replace('src="/img/', f'src="{BASE}/img/').replace('href="/', f'href="{BASE}/')
        h = re.sub(r'<figure class="pn-fig">', "<figure>", h)
        doc = (f"<!doctype html><meta charset='utf-8'><title>{html.escape(p.get('substack_title', p['title']))}</title>"
               "<body style='max-width:720px;margin:40px auto;font:18px/1.6 Georgia,serif;padding:0 20px'>"
               f"<p style='font:13px Inter,sans-serif;color:#666'>Substack draft. Send {nice_date(p['date'])}, 9:00 AM IST. Cover image: {BASE}/img/covers/og/{p['slug']}.jpg</p>"
               f"<h1>{html.escape(p.get('substack_title', p['title']))}</h1><h3 style='color:#555;font-weight:400'>{html.escape(p.get('substack_subtitle', p['description']))}</h3>"
               f"<img src='{BASE}/img/covers/og/{p['slug']}.jpg' alt='' style='width:100%'>{h}"
               f"<p><em>Also on the blog at <a href='{BASE}/{p['slug']}'>{BASE}/{p['slug']}</a></em></p></body>")
        open(os.path.join(SUB_OUT, f'{p["date"]}-{p["slug"]}.html'), "w", encoding="utf-8").write(doc)


def main():
    posts = load_posts()
    if not posts:
        fail("no posts found")
    tpl = open(TEMPLATE, encoding="utf-8").read()
    for p in posts:
        open(os.path.join(SITE, p["slug"] + ".html"), "w", encoding="utf-8").write(render_page(p, tpl))
    diagrams(posts)
    covers(posts)
    update_blog(posts)
    update_sitemap(posts)
    update_search(posts)
    update_llms(posts)
    write_edge(posts)
    substack_copies(posts)
    print("built", len(posts), "posts:", ", ".join(f'{p["date"]} {p["slug"]}' for p in posts))


if __name__ == "__main__":
    main()
