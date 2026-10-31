// Created by: Claude
// Date: 2026-10-31
// Purpose: Email the salary growth PDF report to the visitor through Brevo (transactional API)
// Owner: Syed Hadi
//
// Environment variables (set in Netlify > Site configuration > Environment variables):
//   BREVO_API_KEY        required. Brevo v3 API key (xkeysib-...).
//   REPORT_SENDER_EMAIL  optional. A sender verified in Brevo. Default: ssyedhadi14@gmail.com
//   REPORT_SENDER_NAME   optional. Default: Syed Hadi
//   REPORT_BCC           optional. Comma separated addresses that get a copy (lead capture). Default: none
//   REPORT_REPLY_TO      optional. Default: ssyedhadi14@gmail.com

const MAX_PDF_BYTES = 4 * 1024 * 1024; // base64 length cap, roughly 3 MB of PDF
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const hits = new Map(); // very small in memory rate limit per warm instance

function json(status, body) {
  return {
    statusCode: status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' },
    body: JSON.stringify(body),
  };
}

function esc(s) {
  return String(s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') return json(405, { ok: false, error: 'Use POST.' });
  const key = process.env.BREVO_API_KEY;
  if (!key) return json(503, { ok: false, error: 'Email is not set up yet on this site.' });

  const ip = (event.headers['x-nf-client-connection-ip'] || event.headers['client-ip'] || 'unknown').split(',')[0].trim();
  const now = Date.now();
  const rec = hits.get(ip) || [];
  const recent = rec.filter((t) => now - t < 10 * 60 * 1000);
  if (recent.length >= 5) return json(429, { ok: false, error: 'Too many reports from this connection. Try again in a few minutes.' });
  recent.push(now); hits.set(ip, recent);

  let data;
  try { data = JSON.parse(event.body || '{}'); } catch (e) { return json(400, { ok: false, error: 'Bad request body.' }); }
  const email = String(data.email || '').trim().toLowerCase();
  const name = String(data.name || '').trim().slice(0, 60);
  const pdf = String(data.pdf || '');
  const filename = /^[a-z0-9-]+\.pdf$/i.test(String(data.filename || '')) ? data.filename : 'salary-growth-report.pdf';
  const s = data.summary || {};
  if (!EMAIL_RE.test(email)) return json(400, { ok: false, error: 'Enter a valid email address.' });
  if (!pdf || pdf.length > MAX_PDF_BYTES || !/^[A-Za-z0-9+/=]+$/.test(pdf)) return json(400, { ok: false, error: 'The PDF payload is missing or too large.' });

  const senderEmail = process.env.REPORT_SENDER_EMAIL || 'ssyedhadi14@gmail.com';
  const senderName = process.env.REPORT_SENDER_NAME || 'Syed Hadi';
  const replyTo = process.env.REPORT_REPLY_TO || 'ssyedhadi14@gmail.com';
  const bcc = (process.env.REPORT_BCC || '').split(',').map((x) => x.trim()).filter((x) => EMAIL_RE.test(x));
  const first = name ? esc(name.split(' ')[0]) : 'there';
  const link = /^https:\/\/syedcreates\.com\//.test(String(s.link || '')) ? String(s.link) : 'https://syedcreates.com/salary-calculator';

  const html = `<!doctype html><html><body style="margin:0;background:#f6f5fb;font-family:Verdana,Geneva,sans-serif;color:#141228">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" style="max-width:560px;background:#ffffff;border-radius:16px;overflow:hidden">
<tr><td style="background:#5b3df5;padding:26px 28px;color:#fff;font-size:20px;font-weight:bold;font-family:Verdana,Geneva,sans-serif">Your salary growth report</td></tr>
<tr><td style="padding:26px 28px;font-size:14px;line-height:1.6;font-family:Verdana,Geneva,sans-serif">
<p style="margin:0 0 14px">Hi ${first},</p>
<p style="margin:0 0 14px">The PDF is attached. Here is the short version:</p>
<table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14px;font-family:Verdana,Geneva,sans-serif;margin:0 0 16px">
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">Corpus at age ${esc(s.target)}</td><td style="padding:6px 0;font-weight:bold">${esc(s.corpus)}</td></tr>
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">In today&rsquo;s money</td><td style="padding:6px 0;font-weight:bold">${esc(s.real)}</td></tr>
<tr><td style="padding:6px 14px 6px 0;color:#6b6b82">You invest per month now</td><td style="padding:6px 0;font-weight:bold">${esc(s.investNow)}</td></tr>
</table>
<p style="margin:0 0 18px"><a href="${esc(link)}" style="display:inline-block;background:#5b3df5;color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-weight:bold">Reopen your plan</a></p>
<p style="margin:0 0 14px">Two things that change the curve most: the increment you negotiate and the share of salary you invest. If you want to talk through either, reply to this email or <a href="https://syedcreates.com/schedule-meeting" style="color:#5b3df5">book 30 minutes</a>.</p>
<p style="margin:0;color:#6b6b82;font-size:12px">Planning tool, not investment advice. Returns are assumptions, not predictions. You asked for this one email from syedcreates.com. There is no list to unsubscribe from.</p>
</td></tr>
<tr><td style="padding:16px 28px;background:#f6f5fb;font-size:12px;color:#6b6b82;font-family:Verdana,Geneva,sans-serif">Syed Hadi &middot; Product Marketing and Partnerships Lead &middot; Bengaluru &middot; <a href="https://syedcreates.com" style="color:#5b3df5">syedcreates.com</a></td></tr>
</table></td></tr></table></body></html>`;

  const payload = {
    sender: { name: senderName, email: senderEmail },
    to: [{ email, name: name || undefined }],
    replyTo: { email: replyTo, name: senderName },
    subject: `Your salary growth report: ${String(s.corpus || '').replace(/[^\w\s.₹]/g, '')} at age ${String(s.target || '').replace(/\D/g, '')}`.trim(),
    htmlContent: html,
    textContent: `Hi ${first},\n\nYour salary growth report is attached.\nCorpus at age ${s.target}: ${s.corpus} (${s.real} in today's money). You invest ${s.investNow} per month now.\nReopen your plan: ${link}\n\nPlanning tool, not investment advice.\nSyed Hadi, syedcreates.com`,
    attachment: [{ content: pdf, name: filename }],
    tags: ['salary-calculator'],
  };
  if (bcc.length) payload.bcc = bcc.map((e) => ({ email: e }));

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: { 'api-key': key, 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const txt = await res.text();
      console.error('brevo error', res.status, txt.slice(0, 300));
      return json(502, { ok: false, error: 'The mail service rejected the message.' });
    }
    return json(200, { ok: true });
  } catch (err) {
    console.error('send failed', err && err.message);
    return json(502, { ok: false, error: 'Could not reach the mail service.' });
  }
};
