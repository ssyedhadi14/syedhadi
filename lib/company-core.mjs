// Created by: Claude
// Date: 2026-11-02
// Purpose: Company research for syedcreates.com/company-research. Takes a company homepage URL, runs a
//          Firecrawl Agent job (autonomous search plus scrape with a fixed JSON schema) and returns a byte
//          sized market snapshot: market cap, HQ, employees, customers, ARR, competitors, differentiators,
//          why customers choose them, growth pain points and missed revenue opportunities.
// Owner: Syed Hadi
// Shared core: wrapped by netlify/functions/company-research.mjs and functions/api/company-research.js (Cloudflare Pages)
//
// Flow:  POST {url}            -> cached result, or a job id
//        GET  ?id=<job uuid>   -> {status:'processing'} until done, then the result (cached 7 days per domain)
//
// Environment variables:
//   FIRECRAWL_API_KEY               required. fc-... key from firecrawl.dev > API keys.
//   FIRECRAWL_AGENT_MODEL           optional. Agent model id. Server default when unset.
//   COMPANY_RESEARCH_MAX_CREDITS    optional. Credit ceiling per run. Default 400.
//   COMPANY_RESEARCH_DAILY_CAP      optional. New (uncached) runs allowed per UTC day across the site. Default 25.
//   COMPANY_RESEARCH_PER_IP_HOUR    optional. New runs per visitor per hour. Default 3.
//   COMPANY_RESEARCH_MOCK           optional. "1" returns a fixed sample without calling Firecrawl (QA only).


const API = 'https://api.firecrawl.dev/v2';
const CACHE_DAYS = 7;
const hits = new Map();

const json = (status, body) => new Response(JSON.stringify(body), {
  status,
  headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' },
});

// Storage is injected by the platform wrapper: Netlify Blobs or Cloudflare KV. Both expose getJSON / setJSON.
let STORE = null;
const memo = new Map(); // fallback when no store is bound (local dev): per instance only
function store() { return STORE; }
async function bget(key) { if (!STORE) return memo.get(key) || null; try { return await STORE.getJSON(key); } catch (e) { return null; } }
async function bset(key, val) { if (!STORE) { memo.set(key, val); return; } try { await STORE.setJSON(key, val); } catch (e) { /* cache is best effort */ } }

function normalizeUrl(raw) {
  let s = String(raw || '').trim();
  if (!s || s.length > 300) return null;
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  let u;
  try { u = new URL(s); } catch (e) { return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const host = u.hostname.toLowerCase();
  if (!host.includes('.') || host.endsWith('.local') || host === 'localhost' || /^\d+\.\d+\.\d+\.\d+$/.test(host) || host.includes(':')) return null;
  return { home: 'https://' + host + '/', host: host.replace(/^www\./, '') };
}

// ---------- schema ----------
const fact = (desc) => ({
  type: 'object',
  properties: {
    value: { type: 'string', description: desc },
    as_of: { type: 'string', description: 'Month and year the figure refers to, for example "Mar 2026". Empty if unknown.' },
    confidence: { type: 'string', enum: ['HIGH', 'MEDIUM', 'UNVERIFIED'], description: 'HIGH = company filing or official page. MEDIUM = reputable press or analyst estimate. UNVERIFIED = single weak source or inference.' },
    source_url: { type: 'string', description: 'URL of the page the figure came from. Empty if none.' },
  },
  required: ['value', 'confidence'],
});

const SCHEMA = {
  type: 'object',
  properties: {
    company_name: { type: 'string' },
    one_liner: { type: 'string', description: 'What the company sells and to whom, max 18 words.' },
    category: { type: 'string', description: 'Market category in 2 to 4 words, for example "Cloud security (CNAPP)".' },
    founded: { type: 'string', description: 'Year founded, or empty.' },
    ownership: { type: 'string', enum: ['Public', 'Private', 'Subsidiary', 'Unknown'] },
    ticker: { type: 'string', description: 'Exchange and ticker if public, for example "NASDAQ: CRWD". Empty otherwise.' },
    market_cap: fact('Public: market capitalisation in USD, for example "$84.2B". Private: latest post money valuation with the word "valuation", for example "$1.2B valuation (Series D)". If neither is disclosed: "Not disclosed".'),
    headquarters: fact('City, region and country of the head office, for example "Austin, Texas, USA".'),
    employee_count: fact('Headcount as a number or range, for example "1,250" or "500 to 1,000".'),
    total_customers: fact('Number of customers, for example "3,500+ customers". "Not disclosed" if the company never states it.'),
    arr: fact('Annual recurring revenue in USD, for example "$120M ARR". Public companies without ARR: latest annual revenue labelled "revenue". "Not disclosed" if unknown.'),
    competitors: {
      type: 'array', maxItems: 5,
      items: { type: 'object', properties: {
        name: { type: 'string' },
        overlap: { type: 'string', description: 'Where they compete head to head, max 12 words.' },
      }, required: ['name', 'overlap'] },
    },
    differentiators: { type: 'array', maxItems: 5, items: { type: 'string', description: 'One unique differentiator, max 16 words, concrete and specific.' } },
    why_customers_choose: {
      type: 'array', maxItems: 4,
      items: { type: 'object', properties: {
        reason: { type: 'string', description: 'Why buyers pick them over competitors, max 12 words.' },
        evidence: { type: 'string', description: 'Proof: a review theme, case study result, customer quote paraphrase or award, max 18 words.' },
      }, required: ['reason', 'evidence'] },
    },
    growth_painpoints: {
      type: 'array', maxItems: 6,
      items: { type: 'object', properties: {
        pain: { type: 'string', description: 'A growth pain point of this company, max 14 words.' },
        severity: { type: 'string', enum: ['must_fix', 'nice_to_fix'], description: 'must_fix = actively limiting growth now. nice_to_fix = drag on efficiency.' },
        signal: { type: 'string', description: 'What points to it: reviews, hiring, pricing page, press, churn talk. Max 14 words.' },
      }, required: ['pain', 'severity'] },
    },
    missed_revenue: {
      type: 'array', maxItems: 5,
      items: { type: 'object', properties: {
        opportunity: { type: 'string', description: 'A revenue opportunity the company is under using, max 12 words.' },
        fix: { type: 'string', description: 'The concrete fix, max 16 words.' },
        impact: { type: 'string', enum: ['High', 'Medium', 'Low'] },
      }, required: ['opportunity', 'fix', 'impact'] },
    },
    sources: {
      type: 'array', maxItems: 10,
      items: { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['url'] },
    },
  },
  required: ['company_name', 'one_liner', 'market_cap', 'headquarters', 'employee_count', 'total_customers', 'arr', 'competitors', 'differentiators', 'why_customers_choose', 'growth_painpoints', 'missed_revenue'],
};

function prompt(home, host) {
  return [
    `Research the company whose homepage is ${home} (domain ${host}). Build a market snapshot for a go to market strategist.`,
    'Start on the homepage, then the about, customers, pricing and press pages, then search the web: Crunchbase, LinkedIn, company filings and investor relations, reputable press, G2 or Gartner Peer Insights reviews, job postings.',
    'Find: market cap (or latest private valuation), headquarters, employee count, total customers, ARR (or annual revenue), top 5 competitors, unique differentiators, why customers choose them over competitors, growth pain points, and revenue opportunities they are missing with the fix for each.',
    'Rules. Never invent a number. If a figure is not published, set value to "Not disclosed" and confidence to UNVERIFIED. Prefer the most recent figure and set as_of. Put the source URL on every figure.',
    'Keep every text field short and specific, the way an analyst writes a one pager. No marketing language, no em dashes, no semicolons.',
    'Pain points and missed revenue are your analysis: base each on a visible signal (pricing page gaps, missing segments, regions not served, review complaints, hiring patterns, no partner program, no marketplace listings, weak self serve, no expansion pricing) and say what the signal is.',
    'List the pages you relied on in sources.',
  ].join('\n');
}

// ---------- tidy the agent output so the page and PDF can trust its shape ----------
const clip = (s, n) => { s = String(s == null ? '' : s).replace(/\s*[—–]\s*/g, ', ').replace(/;\s*/g, ', ').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : s; };
const okUrl = (u) => { try { const x = new URL(String(u)); return /^https?:$/.test(x.protocol) ? x.href : ''; } catch (e) { return ''; } };
function tidyFact(f) {
  f = f && typeof f === 'object' ? f : { value: typeof f === 'string' ? f : '' };
  const value = clip(f.value, 70) || 'Not disclosed';
  const conf = ['HIGH', 'MEDIUM', 'UNVERIFIED'].includes(String(f.confidence).toUpperCase()) ? String(f.confidence).toUpperCase() : 'UNVERIFIED';
  return { value, as_of: clip(f.as_of, 20), confidence: /not disclosed/i.test(value) ? 'UNVERIFIED' : conf, source_url: okUrl(f.source_url) };
}
const arr = (a, n) => (Array.isArray(a) ? a : []).filter(Boolean).slice(0, n);
function tidy(d, host) {
  d = d && typeof d === 'object' ? d : {};
  return {
    domain: host,
    company_name: clip(d.company_name, 60) || host,
    one_liner: clip(d.one_liner, 160),
    category: clip(d.category, 50),
    founded: clip(d.founded, 10),
    ownership: clip(d.ownership, 14),
    ticker: clip(d.ticker, 24),
    market_cap: tidyFact(d.market_cap),
    headquarters: tidyFact(d.headquarters),
    employee_count: tidyFact(d.employee_count),
    total_customers: tidyFact(d.total_customers),
    arr: tidyFact(d.arr),
    competitors: arr(d.competitors, 5).map((c) => ({ name: clip(c.name, 40), overlap: clip(c.overlap, 110) })).filter((c) => c.name),
    differentiators: arr(d.differentiators, 5).map((x) => clip(typeof x === 'string' ? x : x && x.text, 130)).filter(Boolean),
    why_customers_choose: arr(d.why_customers_choose, 4).map((c) => ({ reason: clip(c.reason, 100), evidence: clip(c.evidence, 150) })).filter((c) => c.reason),
    growth_painpoints: arr(d.growth_painpoints, 6).map((p) => ({ pain: clip(p.pain, 120), severity: p.severity === 'nice_to_fix' ? 'nice_to_fix' : 'must_fix', signal: clip(p.signal, 120) })).filter((p) => p.pain),
    missed_revenue: arr(d.missed_revenue, 5).map((m) => ({ opportunity: clip(m.opportunity, 100), fix: clip(m.fix, 140), impact: ['High', 'Medium', 'Low'].includes(m.impact) ? m.impact : 'Medium' })).filter((m) => m.opportunity),
    sources: arr(d.sources, 10).map((s) => ({ title: clip(s.title, 80), url: okUrl(s.url) })).filter((s) => s.url),
    researched_at: new Date().toISOString(),
  };
}

const MOCK = {
  company_name: 'Example Security', one_liner: 'Cloud security platform for mid market engineering teams running Kubernetes.', category: 'Cloud security (CNAPP)', founded: '2019', ownership: 'Private', ticker: '',
  market_cap: { value: '$450M valuation (Series C)', as_of: 'Jun 2025', confidence: 'MEDIUM', source_url: 'https://example.com/press' },
  headquarters: { value: 'San Jose, California, USA', confidence: 'HIGH', source_url: 'https://example.com/about' },
  employee_count: { value: '320', as_of: 'Oct 2026', confidence: 'MEDIUM', source_url: 'https://www.linkedin.com/company/example' },
  total_customers: { value: '600+ customers', confidence: 'HIGH', source_url: 'https://example.com/customers' },
  arr: { value: 'Not disclosed', confidence: 'UNVERIFIED' },
  competitors: [{ name: 'Wiz', overlap: 'Agentless CSPM and cloud risk graph' }, { name: 'Palo Alto Prisma Cloud', overlap: 'Enterprise CNAPP suites' }, { name: 'Sysdig', overlap: 'Runtime detection for containers' }, { name: 'Aqua Security', overlap: 'Container image and runtime security' }],
  differentiators: ['Runtime enforcement in the kernel, not only detection', 'Deploys on prem and air gapped for regulated buyers', 'Open source core with an active community'],
  why_customers_choose: [{ reason: 'Blocks attacks at runtime instead of alerting', evidence: 'G2 reviews cite fewer incidents after rollout' }, { reason: 'Lower total cost than suites', evidence: 'Case study reports 40% lower spend than prior stack' }],
  growth_painpoints: [{ pain: 'Brand awareness trails better funded rivals', severity: 'must_fix', signal: 'Low share of voice in analyst reports' }, { pain: 'Long enterprise sales cycles', severity: 'must_fix', signal: 'Hiring for enterprise AEs in 4 regions' }, { pain: 'No self serve trial', severity: 'nice_to_fix', signal: 'Pricing page routes every visitor to sales' }],
  missed_revenue: [{ opportunity: 'Cloud marketplace private offers', fix: 'List on AWS, Azure and GCP marketplaces with committed spend drawdown', impact: 'High' }, { opportunity: 'MSSP channel', fix: 'Launch a partner program with multi tenant pricing', impact: 'High' }, { opportunity: 'Expansion revenue', fix: 'Price per workload with clear tiers to drive upsell', impact: 'Medium' }],
  sources: [{ title: 'Example homepage', url: 'https://example.com/' }],
};

// ---------- firecrawl ----------
async function fc(path, opts = {}) {
  const key = process.env.FIRECRAWL_API_KEY;
  const res = await fetch(API + path, { ...opts, headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', ...(opts.headers || {}) } });
  let body = null; try { body = await res.json(); } catch (e) { }
  if (!res.ok || (body && body.success === false)) {
    const msg = (body && (body.error || body.message)) || ('Firecrawl returned ' + res.status);
    const err = new Error(String(msg).slice(0, 200)); err.status = res.status; throw err;
  }
  return body || {};
}

function rateLimited(ip) {
  const lim = Number(process.env.COMPANY_RESEARCH_PER_IP_HOUR || 3);
  const now = Date.now(); const list = (hits.get(ip) || []).filter((t) => now - t < 3600 * 1000);
  if (list.length >= lim) { hits.set(ip, list); return true; }
  list.push(now); hits.set(ip, list); return false;
}

async function start(req, context) {
  let body = {}; try { body = await req.json(); } catch (e) { }
  const t = normalizeUrl(body.url);
  if (!t) return json(400, { ok: false, error: 'Enter a company homepage, for example accuknox.com.' });
  const fresh = !!body.refresh;

  const cached = await bget('r/' + t.host);
  if (cached && !fresh && Date.now() - Date.parse(cached.researched_at) < CACHE_DAYS * 864e5) return json(200, { ok: true, status: 'completed', cached: true, data: cached });

  if (process.env.COMPANY_RESEARCH_MOCK === '1') return json(200, { ok: true, status: 'completed', mock: true, data: tidy({ ...MOCK }, t.host) });
  if (!process.env.FIRECRAWL_API_KEY) return json(503, { ok: false, error: 'Live research is switching on shortly. Book a call and I will run this company for you in the meantime.' });

  const ip = (context && context.ip) || req.headers.get('x-nf-client-connection-ip') || 'anon';
  if (rateLimited(ip)) return json(429, { ok: false, error: 'You have run 3 new reports this hour. Cached companies still load instantly, new ones open up again within the hour.' });

  const day = new Date().toISOString().slice(0, 10);
  const cap = Number(process.env.COMPANY_RESEARCH_DAILY_CAP || 25);
  const used = (await bget('d/' + day)) || { n: 0 };
  if (used.n >= cap) return json(429, { ok: false, error: 'Today\'s research quota is used up. Try again tomorrow, or book a call and I will run it for you.' });

  const payload = { prompt: prompt(t.home, t.host), urls: [t.home], schema: SCHEMA, maxCredits: Number(process.env.COMPANY_RESEARCH_MAX_CREDITS || 400) };
  if (process.env.FIRECRAWL_AGENT_MODEL) payload.model = process.env.FIRECRAWL_AGENT_MODEL;
  try {
    const r = await fc('/agent', { method: 'POST', body: JSON.stringify(payload) });
    if (!r.id) throw new Error('Firecrawl did not return a job id.');
    await bset('j/' + r.id, { host: t.host, at: Date.now() });
    await bset('d/' + day, { n: used.n + 1 });
    return json(202, { ok: true, status: 'processing', id: r.id, host: t.host });
  } catch (e) {
    return json(502, { ok: false, error: e.status === 402 ? 'The Firecrawl account is out of credits.' : 'Could not start the research: ' + e.message });
  }
}

async function poll(id, hostHint) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) return json(400, { ok: false, error: 'Bad job id.' });
  if (!process.env.FIRECRAWL_API_KEY) return json(503, { ok: false, error: 'Company research is not connected yet.' });
  // job ids only resolve against this site's own Firecrawl key, so an unknown id can at most read our own job
  const job = await bget('j/' + id);
  try {
    const r = await fc('/agent/' + id, { method: 'GET' });
    if (r.status === 'processing') return json(200, { ok: true, status: 'processing' });
    if (r.status !== 'completed') return json(200, { ok: false, status: r.status, error: r.error ? 'Research failed: ' + String(r.error).slice(0, 160) : 'Research was ' + r.status + '. Try again.' });
    let data = r.data; if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { } }
    const hint = normalizeUrl(hostHint);
    const host = (job && job.host) || (hint && hint.host) || 'company';
    const clean = tidy(data, host);
    clean.credits_used = r.creditsUsed ?? null;
    if (job) await bset('r/' + host, clean);
    return json(200, { ok: true, status: 'completed', data: clean });
  } catch (e) {
    return json(502, { ok: false, error: 'Could not read the research job: ' + e.message });
  }
}

export async function handle(req, context, storeImpl) {
  STORE = storeImpl || null;
  if (req.method === 'POST') return start(req, context);
  if (req.method === 'GET') { const q = new URL(req.url).searchParams; return poll(q.get('id') || '', q.get('host') || ''); }
  return json(405, { ok: false, error: 'Use POST or GET.' });
}
