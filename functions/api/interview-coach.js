// Created by: Claude
// Date: 2026-11-06
// Purpose: Cloudflare Pages Function for /api/interview-coach. Interview prep chatbot for Bengaluru PMM,
//          Partnerships and Sales roles, plus resume bullet and cover letter polishing.
//          Uses the Workers AI binding "AI" (wrangler.toml [ai]). No API key or secret needed.
//          If the binding is missing or the model fails, it returns { fallback: true } and the page uses
//          its built-in offline coach instead, so the tool never breaks.
// Owner: Syed Hadi
// Env (all optional):
//   INTERVIEW_COACH_MODEL     Workers AI model id to try first. Falls back through MODELS below.
//   INTERVIEW_COACH_PER_IP    Requests per visitor per hour. Default 40.

const MODELS = [
  '@cf/meta/llama-3.3-70b-instruct-fp8-fast',
  '@cf/meta/llama-3.1-8b-instruct-fast',
  '@cf/meta/llama-3.1-8b-instruct',
  '@cf/mistralai/mistral-small-3.1-24b-instruct',
];
const hits = new Map();

const ROLE = {
  pmm: 'Product Marketing Manager (PMM)',
  partnerships: 'Partnerships, Alliances or Channel Manager',
  sales: 'B2B SaaS Sales (SDR, BDR, Account Executive or Enterprise AE)',
};

const BASE = `You are the Interview Prep Coach on syedcreates.com, built by Syed Hadi, a Product Marketing and Partnerships Lead in Bengaluru.
You help candidates prepare for interviews for B2B SaaS and tech roles in Bengaluru, India: product marketing, partnerships and sales.
Rules:
- Be practical, specific and encouraging. Short paragraphs or tight bullet lists. Keep replies under 220 words unless asked for more.
- Never use em dashes or en dashes. Use commas, colons or full stops instead.
- Use Indian context where it helps: CTC (fixed, variable, ESOPs), notice periods, GCCs vs startups vs Indian SaaS companies, hybrid office days in Bengaluru.
- Prefer frameworks interviewers recognise: STAR for behavioural answers, present-past-future for "tell me about yourself", MEDDICC or SPICED for sales discovery, 30-60-90 day plans.
- Do not invent facts about specific companies, salaries or interview processes. If unsure, say what to check and where.
- Stay on interview prep, resumes, cover letters, offers and career moves. Politely decline anything else.
- Never ask for or repeat sensitive personal data such as phone numbers, ID numbers or addresses.`;

const MODES = {
  ask: 'The user asks a question about interviewing for the role. Answer it directly, then give one concrete next step.',
  mock: `Run a mock interview for the role. If the conversation has no question yet, or the user asks for the next one, ask exactly one realistic interview question and nothing else.
When the user has answered your question: give a score out of 10, two things that worked, two things to fix, a tighter example opening line, then ask the next question.`,
  review: 'The user pastes an interview answer. Score it out of 10 and give specific fixes: structure, evidence (numbers), ownership ("I" not only "we"), and the result. Then show a tightened version under 150 words.',
  bullets: 'The user pastes resume bullets. Rewrite each as one line: strong past-tense verb, what you did, measurable result. Keep the user\'s facts, never invent numbers, use [X] where a number is missing. Return only the bullets, one per line, starting with "- ".',
  cover: 'The user gives details for a cover letter. Write a crisp cover letter under 230 words: hook tied to the company, two proof points with results, why this role, a confident close. Use only the facts given. Return only the letter text.',
};

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}

function clientIp(req) {
  return req.headers.get('CF-Connecting-IP') || req.headers.get('X-Forwarded-For') || 'anon';
}

function limited(ip, lim) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 3600 * 1000);
  if (list.length >= lim) { hits.set(ip, list); return true; }
  list.push(now); hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return false;
}

function clean(s, max) {
  return String(s || '').replace(/[\u0000-\u0008\u000b-\u001f]/g, ' ').slice(0, max);
}

function noDashes(s) {
  return String(s || '').replace(/\s*[—–]\s*/g, ', ').replace(/,\s*,/g, ',').trim();
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === 'GET') return json(200, { ok: true, ai: !!(env && env.AI) });
  if (request.method !== 'POST') return json(405, { ok: false, error: 'Use POST.' });
  if (!env || !env.AI) return json(200, { ok: false, fallback: true, reason: 'ai_not_configured' });

  const lim = Number(env.INTERVIEW_COACH_PER_IP || 40);
  if (limited(clientIp(request), lim)) {
    return json(429, { ok: false, fallback: true, reason: 'rate_limited', error: 'You have hit the hourly limit. The offline coach still works.' });
  }

  let body = {};
  try { body = await request.json(); } catch (e) { return json(400, { ok: false, error: 'Bad JSON.' }); }
  const role = ROLE[body.role] ? body.role : 'pmm';
  const mode = MODES[body.mode] ? body.mode : 'ask';
  const level = clean(body.level, 40);
  const msgs = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
  const history = msgs
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && m.content)
    .map((m) => ({ role: m.role, content: clean(m.content, 2500) }));
  if (!history.length || history[history.length - 1].role !== 'user') {
    if (mode !== 'mock') return json(400, { ok: false, error: 'Send a message first.' });
    history.push({ role: 'user', content: 'Start the mock interview. Ask me the first question.' });
  }

  const system = `${BASE}\nTarget role: ${ROLE[role]}${level ? `, ${level} level` : ''}, Bengaluru.\nTask: ${MODES[mode]}`;
  // Try the configured model first, then current Workers AI chat models, so a deprecated id never breaks the coach.
  const models = [...new Set([env.INTERVIEW_COACH_MODEL, ...MODELS].filter(Boolean))];
  const errors = [];
  for (const model of models) {
    try {
      const out = await env.AI.run(model, {
        messages: [{ role: 'system', content: system }, ...history],
        max_tokens: mode === 'cover' ? 700 : 600,
        temperature: 0.6,
      });
      let raw = out && (out.response ?? (out.result && out.result.response));
      if (raw && typeof raw !== 'string') raw = JSON.stringify(raw);
      if (!raw && out && out.choices && out.choices[0]) raw = out.choices[0].message && out.choices[0].message.content;
      const reply = noDashes(raw);
      if (reply) return json(200, { ok: true, reply, model });
      errors.push(`${model}: empty`);
    } catch (e) {
      errors.push(`${model}: ${String((e && e.message) || e).slice(0, 140)}`);
    }
  }
  return json(200, { ok: false, fallback: true, reason: 'model_error', detail: errors.slice(0, 4) });
}
