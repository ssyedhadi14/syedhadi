// Created by: Claude
// Date: 2026-11-03
// Purpose: Cloudflare Pages Functions helpers. Copies env vars into process.env (nodejs_compat) so the shared
//          handlers read secrets the same way on every platform, and adapts Netlify v1 style handlers.
// Owner: Syed Hadi

export function loadEnv(env) {
  if (typeof process === 'undefined') globalThis.process = { env: {} };
  process.env = process.env || {};
  for (const [k, v] of Object.entries(env || {})) if (typeof v === 'string') process.env[k] = v;
}

export function clientIp(request) {
  return request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'anon';
}

// Wrap an exports.handler(event) function (Netlify v1 shape) as a Pages Function.
export function v1(handler) {
  return async (context) => {
    loadEnv(context.env);
    const req = context.request;
    const url = new URL(req.url);
    const headers = Object.fromEntries(req.headers.entries());
    headers['x-nf-client-connection-ip'] = clientIp(req);
    const event = {
      httpMethod: req.method,
      path: url.pathname,
      headers,
      queryStringParameters: Object.fromEntries(url.searchParams.entries()),
      body: req.method === 'GET' || req.method === 'HEAD' ? null : await req.text(),
      isBase64Encoded: false,
    };
    try {
      const r = (await handler(event, {})) || {};
      return new Response(r.body ?? '', { status: r.statusCode || 200, headers: r.headers || {} });
    } catch (e) {
      return new Response(JSON.stringify({ ok: false, error: 'Server error.' }), { status: 500, headers: { 'Content-Type': 'application/json' } });
    }
  };
}

// KV namespace as the getJSON / setJSON store the company research core expects.
export function kvStore(kv, ttlDays) {
  if (!kv) return null;
  return {
    getJSON: (k) => kv.get(k, 'json'),
    setJSON: (k, v) => kv.put(k, JSON.stringify(v), ttlDays ? { expirationTtl: Math.round(ttlDays * 86400) } : undefined),
  };
}
