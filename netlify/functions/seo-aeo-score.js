// Created by: Claude
// Date: 2026-10-31
// Purpose: SEO and AEO score for any public URL. Fetches the page, robots, sitemap and llms.txt,
//          scores on page and answer engine signals, and pulls domain rank from OpenSEO (DataForSEO).
// Owner: Syed Hadi
//
// Environment variables:
//   OPENSEO_API_KEY     optional. Personal key from app.openseo.so > Settings > API keys (oseo_...). Without it the DR card says "not connected".
//   OPENSEO_PROJECT_ID  optional. Project id to bill lookups to. If missing, the first project from list_projects is used.
//   SCORE_MAX_PER_10MIN optional. Per connection cap. Default 6.
// Each OpenSEO backlinks lookup costs credits (about 50 per domain), so results are cached in memory for 12 hours per host.

const UA = 'Mozilla/5.0 (compatible; SyedCreatesScoreBot/1.0; +https://syedcreates.com/seo-aeo-score)';
const MAX_HTML = 1.5 * 1024 * 1024;
const hits = new Map();
const drCache = new Map();
let projectIdCache = null;

function json(status, body) {
  return { statusCode: status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' }, body: JSON.stringify(body) };
}

function normalizeUrl(raw) {
  let s = String(raw || '').trim();
  if (!s) return null;
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  let u;
  try { u = new URL(s); } catch (e) { return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const host = u.hostname.toLowerCase();
  if (process.env.ALLOW_LOCAL_TARGETS === '1' && (host === 'localhost' || host === '127.0.0.1')) return u;
  if (!host.includes('.') || host.endsWith('.local') || host === 'localhost' || /^\d+\.\d+\.\d+\.\d+$/.test(host) || host.includes(':')) return null;
  if (/^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(host)) return null;
  u.hash = '';
  return u;
}

async function fetchText(url, { timeout = 10000, max = MAX_HTML, accept = 'text/html,application/xhtml+xml,*/*;q=0.8' } = {}) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeout);
  const started = Date.now();
  try {
    const res = await fetch(url, { redirect: 'follow', signal: ctl.signal, headers: { 'User-Agent': UA, Accept: accept, 'Accept-Language': 'en' } });
    const reader = res.body && res.body.getReader ? res.body.getReader() : null;
    let text = '';
    if (reader) {
      const dec = new TextDecoder();
      let got = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        got += value.length;
        text += dec.decode(value, { stream: true });
        if (got > max) { try { ctl.abort(); } catch (e) { } break; }
      }
    } else {
      text = await res.text();
    }
    return { ok: res.ok, status: res.status, url: res.url, text, ms: Date.now() - started, headers: Object.fromEntries(res.headers.entries()), redirected: res.redirected };
  } catch (e) {
    return { ok: false, status: 0, url, text: '', ms: Date.now() - started, headers: {}, error: e.name === 'AbortError' ? 'timeout' : e.message };
  } finally { clearTimeout(t); }
}

// ---------- tiny HTML helpers (regex based, good enough for scoring) ----------
function strip(html) { return html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' '); }
function textOf(html) { return strip(html).replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim(); }
function tag(html, re) { const m = html.match(re); return m ? m[1].trim() : ''; }
function metaContent(html, nameOrProp) {
  const re1 = new RegExp('<meta[^>]+(?:name|property)=["\']' + nameOrProp + '["\'][^>]*content=["\']([^"\']*)["\']', 'i');
  const re2 = new RegExp('<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']' + nameOrProp + '["\']', 'i');
  return tag(html, re1) || tag(html, re2);
}
function allTags(html, name) { return (strip(html).match(new RegExp('<' + name + '\\b[^>]*>([\\s\\S]*?)<\\/' + name + '>', 'gi')) || []).map((x) => textOf(x)); }
function headings(html) {
  const out = [];
  const re = /<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi; let m;
  while ((m = re.exec(strip(html)))) out.push({ level: +m[1], text: textOf(m[2]) });
  return out;
}
function jsonLd(html) {
  const out = [];
  const re = /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi; let m;
  while ((m = re.exec(html))) { try { out.push(JSON.parse(m[1].trim())); } catch (e) { out.push({ __invalid: true }); } }
  return out;
}
function ldTypes(blocks) {
  const types = new Set();
  const walk = (n) => {
    if (!n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    if (n['@type']) [].concat(n['@type']).forEach((t) => types.add(String(t)));
    if (n['@graph']) walk(n['@graph']);
    Object.keys(n).forEach((k) => { if (k !== '@graph' && typeof n[k] === 'object') walk(n[k]); });
  };
  blocks.forEach(walk);
  return types;
}
function wordCount(s) { return s ? s.split(/\s+/).filter(Boolean).length : 0; }

// ---------- OpenSEO (DataForSEO domain rank) ----------
async function openseoCall(name, args, key) {
  const res = await fetch('https://app.openseo.so/mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream', Authorization: 'Bearer ' + key },
    body: JSON.stringify({ jsonrpc: '2.0', id: Date.now(), method: 'tools/call', params: { name, arguments: args } }),
  });
  const ct = res.headers.get('content-type') || '';
  const raw = await res.text();
  let msg = null;
  if (ct.includes('text/event-stream')) {
    raw.split('\n').forEach((line) => { if (line.startsWith('data:')) { try { const j = JSON.parse(line.slice(5).trim()); if (j && j.result) msg = j; } catch (e) { } } });
  } else { try { msg = JSON.parse(raw); } catch (e) { } }
  if (!res.ok || !msg || msg.error) throw new Error((msg && msg.error && msg.error.message) || ('OpenSEO ' + res.status));
  return msg.result;
}
async function domainRating(host) {
  const key = process.env.OPENSEO_API_KEY;
  if (!key) return { connected: false, note: 'OpenSEO is not connected on this site yet.' };
  const cached = drCache.get(host);
  if (cached && Date.now() - cached.at < 12 * 3600 * 1000) return cached.val;
  try {
    let projectId = process.env.OPENSEO_PROJECT_ID || projectIdCache;
    if (!projectId) {
      const lp = await openseoCall('list_projects', {}, key);
      const projects = (lp.structuredContent && lp.structuredContent.projects) || [];
      if (!projects.length) throw new Error('No OpenSEO project found. Create one in the OpenSEO app.');
      projectId = projects[0].id; projectIdCache = projectId;
    }
    const r = await openseoCall('get_backlinks_overview', { projectId, target: host, scope: 'domain', hideSpam: true }, key);
    const sc = r.structuredContent || {};
    const summary = (sc.overview && sc.overview.overview && sc.overview.overview.summary) || (sc.overview && sc.overview.summary) || {};
    const rank = Number(summary.rank);
    const val = {
      connected: true,
      rank: isFinite(rank) ? rank : null,
      rating: isFinite(rank) ? Math.max(0, Math.min(100, Math.round(rank / 10))) : null,
      backlinks: summary.backlinks ?? null,
      referringDomains: summary.referringDomains ?? null,
      referringPages: summary.referringPages ?? null,
      spamScore: summary.targetSpamScore ?? summary.backlinksSpamScore ?? null,
      newReferringDomains: summary.newReferringDomains ?? null,
      lostReferringDomains: summary.lostReferringDomains ?? null,
      source: 'OpenSEO (DataForSEO backlinks), domain scope',
    };
    drCache.set(host, { at: Date.now(), val });
    return val;
  } catch (e) {
    return { connected: true, error: String(e.message || e).slice(0, 160) };
  }
}

// ---------- scoring ----------
function score(page, robots, sitemap, llms, u) {
  const html = page.text || '';
  const checks = [];
  const add = (group, id, label, pass, max, detail, action, priority) => checks.push({ group, id, label, pass: !!pass, points: pass ? max : 0, max, detail, action: pass ? '' : action, priority: priority || (max >= 6 ? 'high' : max >= 4 ? 'medium' : 'low') });

  const title = textOf(tag(html, /<title[^>]*>([\s\S]*?)<\/title>/i));
  const desc = metaContent(html, 'description');
  const canon = tag(html, /<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || tag(html, /<link[^>]+href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
  const hs = headings(html); const h1s = hs.filter((h) => h.level === 1);
  const imgs = strip(html).match(/<img\b[^>]*>/gi) || [];
  const imgsNoAlt = imgs.filter((t) => !/\salt=/i.test(t)).length;
  const links = strip(html).match(/<a\b[^>]*href=["']([^"'#][^"']*)["']/gi) || [];
  const host = u.hostname.replace(/^www\./, '');
  const internal = links.filter((a) => { const m = a.match(/href=["']([^"']+)["']/i); if (!m) return false; const h = m[1]; return h.startsWith('/') || h.includes(host); }).length;
  const ld = jsonLd(html); const types = ldTypes(ld); const invalidLd = ld.some((b) => b.__invalid);
  const body = textOf(html); const words = wordCount(body);
  const viewport = /<meta[^>]+name=["']viewport["']/i.test(html);
  const lang = /<html[^>]+lang=["'][a-z]/i.test(html);
  const og = ['og:title', 'og:description', 'og:image'].filter((p) => metaContent(html, p)).length;
  const robotsMeta = (metaContent(html, 'robots') || '').toLowerCase();
  const robotsTxt = robots.ok ? robots.text : '';
  const blocksAll = /user-agent:\s*\*\s*[\r\n]+(?:[^\n]*\n)*?\s*disallow:\s*\/\s*$/im.test(robotsTxt);
  const aiBots = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'OAI-SearchBot'];
  const blockedBots = aiBots.filter((b) => new RegExp('user-agent:\\s*' + b + '\\s*[\\r\\n]+(?:[^\\n]*\\n)*?\\s*disallow:\\s*/\\s*$', 'im').test(robotsTxt));
  const qHeads = hs.filter((h) => h.level >= 2 && /\?\s*$/.test(h.text)).length;
  const firstPara = (() => { const m = strip(html).match(/<h1\b[^>]*>[\s\S]*?<\/h1>[\s\S]*?<p\b[^>]*>([\s\S]*?)<\/p>/i); return m ? wordCount(textOf(m[1])) : 0; })();
  const hasDates = /<time\b|datePublished|dateModified|article:published_time/i.test(html);
  const hasAuthor = /rel=["']author["']|"author"\s*:|name=["']author["']/i.test(html);
  let jumps = 0; let prev = 0; hs.forEach((h) => { if (prev && h.level > prev + 1) jumps++; prev = h.level; });
  const sizeKb = Math.round(Buffer.byteLength(html, 'utf8') / 1024);
  const inlineScripts = (html.match(/<script\b(?![^>]*src=)[^>]*>/gi) || []).length;

  // SEO (60)
  add('seo', 'https', 'Served over HTTPS', u.protocol === 'https:' && (page.url || '').startsWith('https://'), 5, page.url, 'Move the site to HTTPS and redirect every http URL with a 301.');
  add('seo', 'status', 'Page loads with status 200 in under 3 seconds', page.ok && page.ms < 3000, 2, `Status ${page.status}, ${page.ms} ms` + (page.redirected ? ', after a redirect' : ''), page.ok ? 'The server took over 3 seconds to answer. Cache HTML at the edge and cut server work on the first byte.' : 'The URL did not return 200. Fix the response before anything else.');
  add('seo', 'title', 'Title tag present and 30 to 60 characters', title && title.length >= 30 && title.length <= 60, 6, title ? `"${title}" (${title.length} chars)` : 'No title tag', !title ? 'Add a title tag that leads with the primary keyword and ends with the brand.' : title.length > 60 ? 'Shorten the title to 60 characters so Google does not truncate it.' : 'Lengthen the title to at least 30 characters and include the primary keyword.');
  add('seo', 'desc', 'Meta description 70 to 160 characters', desc && desc.length >= 70 && desc.length <= 160, 6, desc ? `${desc.length} chars` : 'Missing', !desc ? 'Write a 120 to 160 character meta description that states the outcome and includes the keyword.' : desc.length > 160 ? 'Trim the meta description to 160 characters.' : 'Expand the meta description to at least 70 characters with a clear benefit.');
  add('seo', 'h1', 'Exactly one H1', h1s.length === 1, 5, `${h1s.length} H1 tag${h1s.length === 1 ? '' : 's'}` + (h1s[0] ? `: "${h1s[0].text.slice(0, 80)}"` : ''), h1s.length === 0 ? 'Add one H1 that states the page topic in plain words.' : 'Keep one H1 per page and demote the others to H2.');
  add('seo', 'hier', 'Heading levels do not skip', jumps === 0 && hs.length > 1, 3, `${hs.length} headings, ${jumps} level jump${jumps === 1 ? '' : 's'}`, 'Fix heading order so H2 follows H1 and H3 follows H2. Screen readers and crawlers use the outline.');
  add('seo', 'canonical', 'Canonical URL set', !!canon, 5, canon || 'Missing', 'Add <link rel="canonical"> pointing to the one URL you want indexed for this content.');
  add('seo', 'viewport', 'Mobile viewport meta', viewport, 3, viewport ? 'Present' : 'Missing', 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> for mobile first indexing.');
  add('seo', 'lang', 'HTML lang attribute', lang, 1, lang ? 'Present' : 'Missing', 'Set <html lang="en"> (or the right language code).');
  add('seo', 'alt', 'Images carry alt text', imgs.length === 0 || imgsNoAlt / imgs.length <= 0.1, 4, `${imgs.length - imgsNoAlt} of ${imgs.length} images have alt`, `Add descriptive alt text to the ${imgsNoAlt} images missing it.`);
  add('seo', 'robots', 'robots.txt exists and does not block everything', robots.ok && !blocksAll && !robotsMeta.includes('noindex'), 4, robots.ok ? (blocksAll ? 'Disallow: / for all bots' : robotsMeta.includes('noindex') ? 'Page has a noindex meta tag' : 'OK') : `robots.txt returned ${robots.status || robots.error}`, blocksAll ? 'Your robots.txt blocks every crawler. Remove the blanket Disallow.' : robotsMeta.includes('noindex') ? 'This page carries noindex. Remove it if the page should rank.' : 'Publish a robots.txt that allows crawling and lists your sitemap.');
  add('seo', 'sitemap', 'XML sitemap reachable', sitemap.ok && /<urlset|<sitemapindex/i.test(sitemap.text), 4, sitemap.ok ? 'Found at /sitemap.xml' : `No sitemap at /sitemap.xml (${sitemap.status || sitemap.error})`, 'Generate an XML sitemap at /sitemap.xml, reference it in robots.txt and submit it in Search Console.');
  add('seo', 'og', 'Open Graph title, description and image', og === 3, 3, `${og} of 3 tags`, 'Add og:title, og:description and a 1200 by 630 og:image so shares render a card.');
  add('seo', 'links', 'At least 10 internal links', internal >= 10, 4, `${internal} internal links`, 'Add contextual internal links to related pages so crawlers and readers can move through the site.');
  add('seo', 'weight', 'HTML under 500 KB with few inline scripts', sizeKb < 500 && inlineScripts <= 12, 2, `${sizeKb} KB HTML, ${inlineScripts} inline scripts`, 'Trim the HTML payload and move scripts to cached external files.');
  add('seo', 'words', 'Enough body copy to rank (300+ words)', words >= 300, 3, `${words} words`, 'Thin pages rarely rank. Add real copy that answers the search intent, aim for 600+ words.');

  // AEO (40)
  add('aeo', 'ld', 'Valid JSON-LD structured data', ld.length > 0 && !invalidLd, 8, ld.length ? (invalidLd ? 'Present but one block does not parse' : [...types].slice(0, 6).join(', ')) : 'None found', invalidLd ? 'One JSON-LD block has a syntax error. Validate it in the Rich Results Test.' : 'Add JSON-LD: WebSite, Organization or Person, and the page type (Article, Service, Product).');
  add('aeo', 'entity', 'Organization or Person entity declared', types.has('Organization') || types.has('Person') || types.has('ProfessionalService') || types.has('LocalBusiness'), 4, types.size ? `Types: ${[...types].slice(0, 8).join(', ')}` : 'No entity schema', 'Declare who publishes the site with Organization or Person schema, including sameAs links to LinkedIn and other profiles. Answer engines resolve entities, not pages.');
  add('aeo', 'faq', 'FAQ, HowTo or Article schema on the page', ['FAQPage', 'HowTo', 'Article', 'BlogPosting', 'NewsArticle', 'TechArticle'].some((t) => types.has(t)), 6, 'Question and answer schema tells engines exactly which text answers which question', 'Add FAQPage schema with 4 to 6 real questions buyers ask, each answered in 40 to 60 words.');
  add('aeo', 'llms', 'llms.txt published', llms.ok && /^#|\n#/.test(llms.text) && llms.text.length > 100, 6, llms.ok ? 'Found at /llms.txt' : 'Not found at /llms.txt', 'Publish /llms.txt: a markdown summary of who you are, what you offer and links to the pages worth citing.');
  add('aeo', 'aibots', 'AI crawlers allowed in robots.txt', robots.ok && blockedBots.length === 0, 6, blockedBots.length ? `Blocked: ${blockedBots.join(', ')}` : 'GPTBot, ClaudeBot, PerplexityBot and Google-Extended can crawl', `Unblock ${blockedBots.join(', ')} in robots.txt or you cannot be cited by those assistants.`);
  add('aeo', 'questions', 'Question style headings or FAQ section', qHeads >= 2 || /faq|frequently asked/i.test(body), 4, `${qHeads} headings phrased as questions`, 'Rewrite 2 or 3 H2s as the exact question a buyer types, and answer it in the first sentence below.');
  add('aeo', 'answer', 'Direct answer right under the H1 (40 to 80 words)', firstPara >= 40 && firstPara <= 90, 3, firstPara ? `${firstPara} words in the first paragraph` : 'No paragraph found after the H1', 'Open with a 40 to 80 word paragraph that answers the page question outright. That is the snippet AI engines lift.');
  add('aeo', 'trust', 'Author and dates visible to machines', hasAuthor && hasDates, 3, `${hasAuthor ? 'Author found' : 'No author'}, ${hasDates ? 'dates found' : 'no dates'}`, 'Add an author with a profile link and datePublished or dateModified so engines can judge freshness and expertise.');

  const seo = checks.filter((c) => c.group === 'seo').reduce((s, c) => s + c.points, 0);
  const aeo = checks.filter((c) => c.group === 'aeo').reduce((s, c) => s + c.points, 0);
  const seoMax = checks.filter((c) => c.group === 'seo').reduce((s, c) => s + c.max, 0);
  const aeoMax = checks.filter((c) => c.group === 'aeo').reduce((s, c) => s + c.max, 0);
  return { checks, seo, aeo, seoMax, aeoMax, total: seo + aeo, title, h1: h1s[0] ? h1s[0].text : '', words };
}

function drActions(dr) {
  if (!dr || !dr.connected || dr.rating == null) return [];
  const r = dr.rating;
  if (r < 10) return [{ priority: 'high', group: 'authority', label: `Domain Rating ${r}: almost no referring domains`, action: 'Start with 10 to 15 easy links: partner pages, directories in your category, founder interviews, guest posts on peer blogs. Then publish one linkable asset a quarter (benchmark, calculator, original data).' }];
  if (r < 30) return [{ priority: 'high', group: 'authority', label: `Domain Rating ${r}: authority is the bottleneck`, action: 'Rankings for competitive terms need DR 30+. Run a digital PR push around original data and get listed on comparison and alternatives pages in your category.' }];
  if (r < 50) return [{ priority: 'medium', group: 'authority', label: `Domain Rating ${r}: solid base`, action: 'Protect what you have (fix lost links, redirect dead pages) and earn links to money pages, not just the blog.' }];
  return [{ priority: 'low', group: 'authority', label: `Domain Rating ${r}: strong profile`, action: 'Authority is not your problem. Spend the effort on AEO: entity schema, llms.txt and question led content that AI engines can quote.' }];
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') return json(405, { ok: false, error: 'Use POST.' });
  const ip = (event.headers['x-nf-client-connection-ip'] || event.headers['client-ip'] || 'unknown').split(',')[0].trim();
  const now = Date.now(); const cap = Number(process.env.SCORE_MAX_PER_10MIN || 6);
  const recent = (hits.get(ip) || []).filter((t) => now - t < 600000);
  if (recent.length >= cap) return json(429, { ok: false, error: 'Too many checks from this connection. Try again in a few minutes.' });
  recent.push(now); hits.set(ip, recent);

  let body; try { body = JSON.parse(event.body || '{}'); } catch (e) { return json(400, { ok: false, error: 'Bad request.' }); }
  const u = normalizeUrl(body.url);
  if (!u) return json(400, { ok: false, error: 'Enter a public website URL, like example.com.' });
  const origin = u.origin;
  const [page, robots, sitemap, llms, dr] = await Promise.all([
    fetchText(u.href),
    fetchText(origin + '/robots.txt', { timeout: 6000, max: 200000, accept: 'text/plain,*/*' }),
    fetchText(origin + '/sitemap.xml', { timeout: 6000, max: 200000, accept: 'application/xml,text/xml,*/*' }),
    fetchText(origin + '/llms.txt', { timeout: 6000, max: 200000, accept: 'text/plain,*/*' }),
    domainRating(u.hostname.replace(/^www\./, '')),
  ]);
  if (!page.text) return json(422, { ok: false, error: page.error === 'timeout' ? 'The site took too long to answer.' : `Could not fetch that page (${page.status || page.error}).` });
  if (!/<html|<head|<body|<title/i.test(page.text.slice(0, 5000))) return json(422, { ok: false, error: 'That URL did not return an HTML page.' });

  const s = score(page, robots, sitemap, llms, u);
  const actions = s.checks.filter((c) => !c.pass).map((c) => ({ priority: c.priority, group: c.group, label: c.label, action: c.action, detail: c.detail, impact: c.max }))
    .concat(drActions(dr))
    .sort((a, b) => ({ high: 0, medium: 1, low: 2 }[a.priority] - { high: 0, medium: 1, low: 2 }[b.priority]) || (b.impact || 0) - (a.impact || 0));
  return json(200, {
    ok: true, url: u.href, finalUrl: page.url, fetchedAt: new Date().toISOString(),
    page: { title: s.title, h1: s.h1, words: s.words, status: page.status, ms: page.ms },
    scores: { seo: s.seo, seoMax: s.seoMax, aeo: s.aeo, aeoMax: s.aeoMax, total: s.total, totalMax: s.seoMax + s.aeoMax },
    dr, checks: s.checks, actions,
  });
};
