/* Created by: Claude
 * Date: 2026-11-06
 * Purpose: /interview-prep. Interview coach chatbot (Workers AI via /api/interview-coach, with a built-in offline
 *          coach as fallback), role question bank, and a resume and cover letter builder that exports to PDF.
 * Owner: Syed Hadi
 * Nothing typed here is stored on a server. Drafts are kept only in this browser (localStorage) if the visitor saves.
 */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var track = function (n, p) { try { if (window.shTrack) window.shTrack(n, p || {}); } catch (e) { } };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) { } }
  };

  /* ------------------------------------------------------------------ data */
  var ROLES = {
    pmm: { name: 'Product Marketing', short: 'PMM' },
    partnerships: { name: 'Partnerships', short: 'Partnerships' },
    sales: { name: 'Sales', short: 'Sales' }
  };

  // Question bank. q = question, t = what the interviewer is testing, a = how to answer well.
  var BANK = window.IP_BANK || {};

  // General topics for the offline coach. k = keywords, a = answer (light markdown: **bold**, "- " bullets).
  var TOPICS = [
    { k: ['tell me about yourself', 'introduce yourself', 'walk me through your resume', 'about yourself', 'introduction'], a: 'Use **present, past, future** and keep it to 90 seconds.\n- **Present:** your role today and the one result you are proudest of, with a number.\n- **Past:** two steps that built the skills this role needs. Skip your whole history.\n- **Future:** why this role at this company is the obvious next step.\nEnd on the role, not on your hobbies. Rehearse it out loud until it sounds like talking, not reading.' },
    { k: ['notice period', 'notice', 'buyout', 'early release', 'serving notice', 'last working day'], a: 'Many Indian companies have **60 to 90 day** notice periods, and startups often want someone sooner.\n- State your real notice period plainly in the first call.\n- Say what is possible: "Officially 90 days, my manager has released people at 45 to 60 before."\n- If they offer a **notice buyout**, get it in the offer letter, including who pays and any tax impact.\n- Never resign before you hold a signed offer.' },
    { k: ['ctc', 'salary', 'expected', 'compensation', 'package', 'hike', 'negotiate', 'negotiation', 'offer'], a: 'Know the parts of a Bengaluru CTC before you name a number: **fixed pay, variable or OTE, joining bonus, ESOPs, and benefits** such as insurance.\n- Research first: the [PMM Salary 2026 guide](/pmm-salary-2026) has India bands by title and city.\n- Give a **range anchored on the role**, not on your current pay: "For this scope I am looking at 32 to 38 fixed."\n- Ask for the split in writing. A big variable share changes what you take home.\n- Negotiate once, with one clear ask, after you have the written offer.' },
    { k: ['esop', 'esops', 'stock', 'equity', 'vesting', 'cliff'], a: 'ESOPs only matter if you understand four things. Ask about:\n- **Vesting schedule and cliff** (often 4 years with a 1 year cliff, but check).\n- **Strike price** and the latest valuation they will share.\n- **Exercise window** if you leave.\n- **Buyback history:** has the company ever let employees sell?\nValue ESOPs at a discount, and never trade away fixed pay you need for equity you cannot sell.' },
    { k: ['star', 'behavioural', 'behavioral', 'tell me about a time', 'situation', 'example of'], a: 'Answer behavioural questions with **STAR**, weighted toward Action and Result.\n- **Situation:** one or two lines of context.\n- **Task:** what you owned, in your words.\n- **Action:** what *you* did, using "I" not only "we". This is 60% of the answer.\n- **Result:** a number and a lesson. "Win rate went from 18% to 26% in two quarters, and I learned to test messaging with sales before launch."\nKeep 6 to 8 stories ready and reuse them across questions.' },
    { k: ['30 60 90', '30-60-90', '90 day', 'first 90', 'plan', 'first month'], a: 'A strong **30-60-90 day plan** shows you will learn before you change things.\n- **30 days:** listen. Talk to 10 customers, 5 sellers or partners, and product. Audit what exists.\n- **60 days:** ship one visible quick win, such as a battlecard, a partner one pager or a fixed sequence.\n- **90 days:** own a measurable goal, such as influenced pipeline, partner sourced deals or quota pace.\nEnd with the metric you want to be judged on. Keep it to one slide per phase.' },
    { k: ['case', 'take home', 'take-home', 'assignment', 'presentation', 'case study', 'deck'], a: 'Most Bengaluru SaaS loops include a **case or take-home**, usually with a few days to submit and a 30 to 45 minute presentation.\n- Restate the problem and your assumptions on slide 1.\n- Lead with the recommendation, then the evidence.\n- Show the trade-offs you rejected. Interviewers score judgement, not polish.\n- Keep it to 8 to 10 slides and leave 15 minutes for questions.\n- Cap your time. A clear 6 hour answer beats a 30 hour deck.' },
    { k: ['questions to ask', 'any questions', 'ask the interviewer', 'reverse'], a: 'Ask questions that show you are already doing the job:\n- "What would make the person in this role a clear success at 6 months?"\n- "Where do deals or launches get stuck today?"\n- "How does this team work with sales, product and partners?"\n- "What did the last person in this role do well, and what would you change?"\nAvoid asking about leave or perks in the first rounds.' },
    { k: ['gcc', 'startup', 'mnc', 'unicorn', 'global capability'], a: 'Bengaluru loops differ by company type:\n- **GCCs and MNCs:** structured rounds, competency questions, clear levels. Prepare polished STAR stories.\n- **Funded startups:** case heavy, founder rounds, more scope and ambiguity. Show speed and ownership.\n- **Indian SaaS scale ups:** mix of both, often with a take-home and a cross-functional panel.\nTailor your stories: process and scale for GCCs, zero to one for startups.' },
    { k: ['hybrid', 'office', 'remote', 'commute', 'wfh', 'work from home', 'location'], a: 'Ask early how many **office days** the team expects and where the office is. In Bengaluru, ORR, Whitefield, Koramangala, HSR and Manyata can mean very different commutes.\nIt is a fair question for the recruiter round and saves everyone time.' },
    { k: ['resume', 'cv', 'bullet', 'ats'], a: 'A resume that gets shortlisted in Bengaluru:\n- One page under 8 years of experience, two pages max after that.\n- Each bullet: **strong verb, what you did, a number**. "Launched X, adding 1.2 Cr pipeline in 2 quarters."\n- Put the role keywords from the job post in your skills and bullets so ATS screens match.\n- No photos, no tables for layout, no fancy fonts.\nUse the [resume builder below](#resume) to draft one and export a PDF.' },
    { k: ['cover letter', 'cover', 'motivation letter'], a: 'Keep a cover letter under 250 words:\n- A hook tied to the company: a launch, a market move, a product you use.\n- Two proof points with results.\n- Why this role and why now.\n- A confident close asking for the conversation.\nThe [cover letter builder](#cover) drafts one from your details.' },
    { k: ['referral', 'linkedin', 'reach out', 'cold message', 'get an interview', 'shortlist', 'apply'], a: 'Referrals beat cold applications. A simple approach:\n- Find 2 people in the team on LinkedIn, ideally the hiring manager and a peer.\n- Send a short note: who you are, one relevant result, the exact role link, and a clear ask.\n- Apply the same day so the referral has something to attach to.\nThe [job board](/jobs) lists live PMM, growth and partnership roles.' },
    { k: ['thank you', 'follow up', 'follow-up', 'after the interview', 'ghosted', 'no response'], a: 'Send a short thank you within 24 hours: one line of thanks, one thing you learned in the conversation, and one line on why it made you more excited.\nIf you hear nothing after the promised date, follow up once politely, then once more a week later. Then move on and keep other loops warm.' },
    { k: ['rejected', 'rejection', 'feedback', 'failed', 'did not get'], a: 'Ask the recruiter for one piece of feedback, and write down every question you were asked while it is fresh.\nThen fix the one gap that came up most. Most people lose offers on the same 2 or 3 weak stories, so tighten those first.' },
    { k: ['weakness', 'weaknesses', 'strength', 'strengths'], a: 'For weaknesses, pick a **real, non-critical** one, show what you did about it and the result. "I used to over-polish launch decks. Now I ship a v1 to sales in 48 hours and iterate on their feedback."\nFor strengths, name one, then prove it with a short story and a number.' }
  ];

  /* --------------------------------------------------------- tiny markdown */
  function md(s) {
    var out = [], list = false;
    String(s || '').split(/\n/).forEach(function (line) {
      var l = esc(line.trim());
      l = l.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\*(.+?)\*/g, '<i>$1</i>')
        .replace(/\[([^\]]+)\]\((\/[^)\s]*|#[^)\s]*|https:\/\/[^)\s]+)\)/g, '<a href="$2">$1</a>');
      if (/^[-*•]\s+/.test(line.trim()) || /^\d+[.)]\s+/.test(line.trim())) {
        if (!list) { out.push('<ul>'); list = true; }
        out.push('<li>' + l.replace(/^(-|\*|•|\d+[.)])\s+/, '') + '</li>');
      } else {
        if (list) { out.push('</ul>'); list = false; }
        if (l) out.push('<p>' + l + '</p>');
      }
    });
    if (list) out.push('</ul>');
    return out.join('');
  }

  /* ------------------------------------------------------- offline coach */
  var STOP = 'a an the and or of to in on for with my me i you is are be how what do does should would can at it this that your our as about when'.split(' ');
  function toks(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(function (w) { return w.length > 1 && STOP.indexOf(w) < 0; }); }

  function scoreAnswer(text) {
    var t = String(text || ''), words = t.split(/\s+/).filter(Boolean).length;
    var nums = (t.match(/\d[\d,.]*\s*(%|x|cr|crore|lakh|l\b|k\b|m\b|\$|inr|rs|days|weeks|months|quarters)?/gi) || []).length;
    var iCount = (t.match(/\bI\b|\bI'm\b|\bI've\b|\bmy\b/g) || []).length, weCount = (t.match(/\bwe\b|\bour\b|\bteam\b/gi) || []).length;
    var result = /(result|increas|grew|growth|reduc|cut|closed|won|launched|saved|improv|doubled|tripled|lifted|pipeline|revenue|quota|signed|sourced)/i.test(t);
    var lesson = /(learn|lesson|next time|would do|changed how|since then)/i.test(t);
    var context = /(when|at the time|we had|the problem|challenge|situation|our .* was)/i.test(t);
    var s = 3, good = [], fix = [];
    if (words >= 80 && words <= 320) { s += 1; good.push('Good length for a spoken answer, roughly ' + Math.round(words / 2.4) + ' seconds.'); }
    else if (words < 80) fix.push('Too short to show judgement. Aim for 120 to 250 words, about 90 seconds spoken.');
    else fix.push('Too long. Cut context and keep the answer under 2 minutes spoken.');
    if (nums >= 2) { s += 2; good.push('You used numbers, which makes the result believable.'); }
    else if (nums === 1) { s += 1; fix.push('Add one more number: a baseline and an end point, such as "from 18% to 26%".'); }
    else fix.push('No numbers. Add the result as a metric: pipeline, win rate, revenue, partners activated, time saved.');
    if (result) { s += 1; } else fix.push('End with the outcome. Say what changed because of you.');
    if (iCount >= 2 && iCount >= weCount / 2) { s += 1; good.push('Clear ownership, you said what you did.'); }
    else fix.push('Say "I" more. Interviewers need to know your part, not only the team\'s.');
    if (context) s += 1; else fix.push('Open with one line of context so the story lands.');
    if (lesson) { s += 1; good.push('You closed with a lesson, which signals maturity.'); }
    else fix.push('Close with one line on what you learned or would do differently.');
    if (words < 80) s = Math.min(s, 6);
    s = Math.max(1, Math.min(10, s));
    return { score: s, good: good.slice(0, 2), fix: fix.slice(0, 3), words: words };
  }

  function feedbackText(r, q) {
    var o = '**Score: ' + r.score + '/10** (offline coach, rule based)\n';
    if (r.good.length) o += '\n**What worked**\n' + r.good.map(function (x) { return '- ' + x; }).join('\n') + '\n';
    if (r.fix.length) o += '\n**Fix next**\n' + r.fix.map(function (x) { return '- ' + x; }).join('\n') + '\n';
    if (q && q.a) o += '\n**What a strong answer covers:** ' + q.a;
    return o;
  }

  function localAsk(role, text) {
    var qt = toks(text), best = null, bestS = 0, low = String(text || '').toLowerCase();
    TOPICS.forEach(function (tp) {
      var s = 0;
      tp.k.forEach(function (k) { if (low.indexOf(k) >= 0) s += k.split(' ').length * 3; else toks(k).forEach(function (w) { if (qt.indexOf(w) >= 0) s += 1; }); });
      if (s > bestS) { bestS = s; best = { a: tp.a }; }
    });
    var roles = [role].concat(Object.keys(BANK).filter(function (r) { return r !== role; }));
    roles.forEach(function (r, ri) {
      (BANK[r] || []).forEach(function (q) {
        var words = toks(q.q + ' ' + q.t + ' ' + (q.k || ''));
        var s = 0; qt.forEach(function (w) { if (words.indexOf(w) >= 0) s += 1; });
        if (ri > 0) s -= 1;
        if (s > bestS) { bestS = s; best = { a: '**' + q.q + '**\n\n**What they are testing:** ' + q.t + '\n\n**How to answer:** ' + q.a }; }
      });
    });
    if (best && bestS >= 2) return best.a + '\n\nWant to practise it? Switch to **Mock interview**.';
    return 'I could not match that to a topic in the offline coach. Try asking about:\n- Tell me about yourself\n- Notice period or expected CTC\n- The STAR method or a 30-60-90 day plan\n- A ' + ROLES[role].name + ' question, for example "' + ((BANK[role] || [{ q: 'a launch' }])[0].q) + '"\nOr switch to **Mock interview** and I will ask you real questions.';
  }

  /* ------------------------------------------------------------- chatbot */
  var chat = { role: 'pmm', mode: 'ask', level: 'mid', msgs: [], asked: [], current: null, ai: null, busy: false };

  function setBadge() {
    var b = $('ipAiBadge'); if (!b) return;
    if (chat.ai === false) { b.textContent = 'Offline coach'; b.className = 'ip-badge off'; b.title = 'AI is unavailable right now, so answers come from the built-in coach.'; }
    else if (chat.ai === true) { b.textContent = 'AI coach'; b.className = 'ip-badge on'; b.title = 'Answers from Workers AI. Check facts before you rely on them.'; }
    else { b.textContent = 'Coach'; b.className = 'ip-badge'; }
  }

  function addMsg(who, text, opts) {
    var log = $('ipLog'); if (!log) return;
    var d = document.createElement('div');
    d.className = 'ip-msg ' + (who === 'user' ? 'me' : 'bot');
    d.innerHTML = who === 'user' ? '<p>' + esc(text).replace(/\n/g, '<br>') + '</p>' : md(text);
    if (opts && opts.typing) d.classList.add('typing');
    log.appendChild(d); log.scrollTop = log.scrollHeight;
    return d;
  }

  function nextQuestion() {
    var list = BANK[chat.role] || [];
    var left = list.filter(function (q) { return chat.asked.indexOf(q.q) < 0; });
    if (!left.length) { chat.asked = []; left = list.slice(); }
    var q = left[Math.floor(Math.random() * left.length)];
    chat.asked.push(q.q); chat.current = q;
    return q;
  }

  function quickPrompts() {
    var box = $('ipQuick'); if (!box) return;
    var P = {
      ask: { pmm: ['How do I answer "tell me about yourself" for a PMM role?', 'How should I structure a PMM take-home case?', 'What is a good 30-60-90 day plan for a PMM?', 'How do I negotiate CTC for a senior PMM offer?'],
        partnerships: ['How do I design a partner program in an interview case?', 'How do I answer questions on channel conflict?', 'What metrics prove partner success?', 'How do I talk about AWS marketplace co-sell?'],
        sales: ['How do I answer "sell me this pen"?', 'How do I explain my quota attainment?', 'Walk me through MEDDICC for an interview', 'How do I handle "your price is too high"?'] },
      mock: { pmm: ['Start the mock interview', 'Give me a harder question', 'Ask me a case question'], partnerships: ['Start the mock interview', 'Give me a harder question', 'Ask me a case question'], sales: ['Start the mock interview', 'Give me a harder question', 'Run a 60 second cold call role play'] },
      review: { pmm: ['Paste your answer in the box below and press Send'], partnerships: ['Paste your answer in the box below and press Send'], sales: ['Paste your answer in the box below and press Send'] }
    };
    var items = (P[chat.mode] || P.ask)[chat.role] || [];
    box.innerHTML = items.map(function (t) { return '<button type="button" class="ip-qp">' + esc(t) + '</button>'; }).join('');
    box.querySelectorAll('.ip-qp').forEach(function (b) {
      b.addEventListener('click', function () {
        if (chat.mode === 'review') { $('ipInput').focus(); return; }
        send(b.textContent);
      });
    });
  }

  function resetChat(intro) {
    chat.msgs = []; chat.asked = []; chat.current = null;
    var log = $('ipLog'); if (log) log.innerHTML = '';
    var r = ROLES[chat.role].name;
    var hello = {
      ask: 'Ask me anything about **' + r + '** interviews in Bengaluru: rounds, questions, cases, CTC, notice periods or your resume.',
      mock: 'Mock interview for **' + r + '**. I will ask one question at a time and score each answer. Press **Start the mock interview** or type "start".',
      review: 'Paste an answer you have prepared for a **' + r + '** interview. I will score it and show you a tighter version.'
    }[chat.mode];
    addMsg('bot', intro || hello);
    quickPrompts();
  }

  function callAI(mode, messages) {
    if (chat.ai === false) return Promise.resolve(null);
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 25000);
    return fetch('/api/interview-coach', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: ctrl ? ctrl.signal : undefined,
      body: JSON.stringify({ role: chat.role, mode: mode, level: chat.level, messages: messages })
    }).then(function (r) { return r.ok || r.status === 429 ? r.json() : null; })
      .then(function (d) {
        clearTimeout(to);
        if (d && d.ok && d.reply) { chat.ai = true; setBadge(); return d.reply; }
        if (d && d.reason === 'rate_limited') return null;
        chat.ai = false; setBadge(); return null;
      })
      .catch(function () { clearTimeout(to); chat.ai = false; setBadge(); return null; });
  }

  function localReply(text) {
    var low = String(text || '').toLowerCase().trim();
    if (chat.mode === 'mock') {
      if (!chat.current || /^(start|next|another|skip|harder|give me|ask me|run a)/.test(low)) {
        var q = nextQuestion();
        return '**Question ' + chat.asked.length + ':** ' + q.q + '\n\nTake your time. Type your answer as you would say it.';
      }
      var fb = feedbackText(scoreAnswer(text), chat.current);
      var nq = nextQuestion();
      return fb + '\n\n**Next question:** ' + nq.q;
    }
    if (chat.mode === 'review') return feedbackText(scoreAnswer(text), null) + '\n\nTip: read it aloud and time it. Over 2 minutes means cut the context.';
    return localAsk(chat.role, text);
  }

  function send(text) {
    text = String(text || '').trim();
    if (!text || chat.busy) return;
    chat.busy = true;
    addMsg('user', text);
    chat.msgs.push({ role: 'user', content: text });
    var input = $('ipInput'); if (input) input.value = '';
    var typing = addMsg('bot', '<span class="ip-dots"><i></i><i></i><i></i></span>', { typing: true });
    typing.innerHTML = '<span class="ip-dots" aria-label="Coach is typing"><i></i><i></i><i></i></span>';
    track('interview_chat', { label: chat.role + ':' + chat.mode });
    callAI(chat.mode, chat.msgs).then(function (reply) {
      var mockQ = null;
      if (!reply) reply = localReply(text);
      else if (chat.mode === 'mock') mockQ = true;
      typing.remove();
      addMsg('bot', reply);
      chat.msgs.push({ role: 'assistant', content: reply });
      if (mockQ) chat.current = { q: 'ai', a: '' };
      chat.busy = false;
    });
  }

  function initChat() {
    if (!$('ipChat')) return;
    document.querySelectorAll('#ipRole button').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#ipRole button').forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
        b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
        chat.role = b.getAttribute('data-v'); resetChat(); syncRole(chat.role, 'chat');
      });
    });
    document.querySelectorAll('#ipMode button').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#ipMode button').forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
        b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
        chat.mode = b.getAttribute('data-v'); resetChat();
      });
    });
    var lv = $('ipLevel'); if (lv) lv.addEventListener('change', function () { chat.level = lv.value; });
    $('ipForm').addEventListener('submit', function (e) { e.preventDefault(); send($('ipInput').value); });
    $('ipInput').addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send($('ipInput').value); } });
    $('ipReset').addEventListener('click', function () { resetChat(); });
    resetChat(); setBadge();
  }

  /* ------------------------------------------------------- question bank */
  // The bank is rendered as static HTML (one panel per role) so search and answer engines can read it.
  function initBank() {
    if (!$('ipBank')) return;
    document.querySelectorAll('#ipBank .ip-practise').forEach(function (b) {
      b.addEventListener('click', function () {
        var role = b.getAttribute('data-role'), q = (BANK[role] || [])[+b.getAttribute('data-i')];
        if (!q) return;
        var rb = document.querySelector('#ipRole button[data-v="' + role + '"]'); if (rb && !rb.classList.contains('on')) rb.click();
        var mb = document.querySelector('#ipMode button[data-v="mock"]'); if (mb && !mb.classList.contains('on')) mb.click();
        chat.current = q; chat.asked.push(q.q);
        addMsg('bot', '**Question:** ' + q.q + '\n\nType your answer as you would say it. I will score it.');
        chat.msgs.push({ role: 'assistant', content: 'Question: ' + q.q });
        var c = $('coach'); if (c) c.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(function () { var i = $('ipInput'); if (i) i.focus({ preventScroll: true }); }, 500);
      });
    });
  }
  function syncRole(r) {
    var b = document.querySelector('#ipBankTabs [data-role="' + r + '"]');
    if (b && b.getAttribute('aria-selected') !== 'true') b.click();
  }

  /* -------------------------------------------------------- resume builder */
  // Output follows a classic one column Indian tech resume: blue name, contact block with a portfolio QR code,
  // Education, Professional Experience (roles grouped by company), optional Volunteering, Additional Information.
  var RS_KEY = 'sh_ip_resume_v2', CL_KEY = 'sh_ip_cover_v1';
  var IDEAS = window.IP_IDEAS || {};
  var SAMPLE = window.IP_SAMPLE || {};
  var DEFAULTS = window.IP_DEFAULTS || {};
  var rs = null, lastBulletBox = null;

  function blankRole() { return { title: '', dates: '', bullets: '', tools: '' }; }
  function blankJob() { return { company: '', city: '', roles: [blankRole()] }; }
  function blankResume(role) {
    var d = DEFAULTS[role || 'pmm'] || {};
    return { role: role || 'pmm', name: '', city: 'Bengaluru, IN', phone: '', email: '', linkedin: '', portfolio: '', highlight: '', yoe: '', env: 'fast-paced B2B SaaS companies',
      edu: [{ school: '', degree: '', city: '', years: '' }], jobs: [blankJob()],
      vol: { org: '', city: '', title: '', dates: '', bullets: '' },
      s1l: d.s1l || 'Core Skills', s1: d.s1 || '', s2l: d.s2l || 'Digital Skills', s2: d.s2 || '', tools: d.tools || '', certs: '', hobbies: '' };
  }
  function migrate(o) {
    if (!o || !o.jobs) return null;
    var b = blankResume(o.role); Object.keys(b).forEach(function (k) { if (o[k] == null) o[k] = b[k]; });
    return o;
  }

  function lines(s) { return String(s || '').split(/\n/).map(function (l) { return l.replace(/^\s*[-*•●]\s*/, '').trim(); }).filter(Boolean); }
  function bulletHtml(l) {
    var m = l.match(/^([A-Z][A-Za-z0-9&/ +.]{1,32}):\s+(.+)$/);
    return m ? '<b>' + esc(m[1]) + ':</b> ' + esc(m[2]) : esc(l);
  }
  function url(u) { u = String(u || '').trim(); if (!u) return ''; return /^https?:\/\//i.test(u) ? u : 'https://' + u.replace(/^\/+/, ''); }
  function link(href, text) { return href ? '<a href="' + esc(href) + '">' + esc(text) + '</a>' : ''; }
  function qrSvg(text) {
    if (!text || !window.SHQR) return '';
    try {
      var q = window.SHQR(text), n = q.size, p = '';
      for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (q.dark(r, c)) p += 'M' + c + ' ' + r + 'h1v1h-1z';
      return '<svg class="cv-qr" viewBox="-1 -1 ' + (n + 2) + ' ' + (n + 2) + '" shape-rendering="crispEdges" aria-label="QR code to portfolio"><rect x="-1" y="-1" width="' + (n + 2) + '" height="' + (n + 2) + '" fill="#fff"/><path d="' + p + '" fill="#000"/></svg>';
    } catch (e) { return ''; }
  }
  function row(l, r, cls) { return '<div class="cv-row ' + (cls || '') + '"><span>' + l + '</span><span>' + r + '</span></div>'; }

  function resumeHtml() {
    var h = '<div class="cv">';
    var port = url(rs.portfolio), li = url(rs.linkedin);
    h += '<div class="cv-top"><div class="cv-id"><h3 class="cv-name">' + (esc(rs.name) || 'Your Name') + '</h3>';
    var c1 = [li ? link(li, 'LinkedIn') : '', rs.email ? link('mailto:' + rs.email, rs.email) : ''].filter(Boolean).join(' | ');
    var c2 = [esc(rs.phone), esc(rs.city)].filter(Boolean).join(' | ');
    if (c1) h += '<p>' + c1 + '</p>';
    if (c2) h += '<p><b>' + c2 + '</b></p>';
    if (rs.highlight) h += '<p>' + esc(rs.highlight) + '</p>';
    if (rs.yoe) h += '<p>Overall ' + esc(String(rs.yoe).replace(/\+?\s*$/, '')) + '+ YoE in ' + esc(rs.env || 'B2B SaaS') + '</p>';
    h += '</div>';
    if (port) h += '<div class="cv-port">' + link(port, 'Portfolio Website') + qrSvg(port) + '</div>';
    h += '</div>';

    var edu = rs.edu.filter(function (e) { return e.school || e.degree; });
    if (edu.length) {
      h += '<h4 class="cv-h">Education</h4>' + edu.map(function (e) {
        return '<div class="cv-blk">' + row('<b>' + esc(e.school) + '</b>', '<b>' + esc(e.city) + '</b>') +
          row(esc(e.degree), e.years ? '<b><span class="cv-sc">Graduated</span> ' + esc(e.years) + '</b>' : '') + '</div>';
      }).join('');
    }
    var jobs = rs.jobs.filter(function (j) { return j.company || j.roles.some(function (r) { return r.title || r.bullets; }); });
    if (jobs.length) {
      h += '<h4 class="cv-h">Professional Experience</h4>' + jobs.map(function (j) {
        return '<div class="cv-blk">' + row('<b>' + esc(j.company) + '</b>', '<b>' + esc(j.city) + '</b>', 'cv-co') +
          j.roles.filter(function (r) { return r.title || r.bullets || r.tools; }).map(function (r, i) {
            var b = lines(r.bullets).map(function (l) { return '<li>' + bulletHtml(l) + '</li>'; });
            if (r.tools) b.push('<li><b>Tools Involved:</b> ' + esc(r.tools) + '</li>');
            return '<div class="cv-role' + (i ? ' next' : '') + '">' + row('<b><i>' + esc(r.title) + '</i></b>', '<b><i>' + esc(r.dates) + '</i></b>') + (b.length ? '<ul>' + b.join('') + '</ul>' : '') + '</div>';
          }).join('') + '</div>';
      }).join('');
    }
    var v = rs.vol;
    if (v && (v.org || v.bullets)) {
      h += '<h4 class="cv-h">Volunteering</h4><div class="cv-blk">' + row('<b>' + esc(v.org) + '</b>', '<b>' + esc(v.city) + '</b>', 'cv-co') +
        row('<i>' + esc(v.title) + '</i>', '<i>' + esc(v.dates) + '</i>') + (lines(v.bullets).length ? '<ul>' + lines(v.bullets).map(function (l) { return '<li>' + bulletHtml(l) + '</li>'; }).join('') + '</ul>' : '') + '</div>';
    }
    var add = [];
    if (rs.s1) add.push('<li><b>' + esc(rs.s1l || 'Skills') + ':</b> ' + esc(rs.s1) + '</li>');
    if (rs.s2) add.push('<li><b>' + esc(rs.s2l || 'Skills') + ':</b> ' + esc(rs.s2) + '</li>');
    if (rs.tools) add.push('<li><b>Tools:</b> ' + esc(rs.tools) + '</li>');
    var certs = lines(rs.certs);
    if (certs.length) add.push('<li><b>Online Courses and Certificates:</b><ol>' + certs.map(function (c) {
      var m = c.split(/\s*[|,]\s*(?=[A-Za-z]{3,9}\.?\s+\d{4}$|\d{4}$)/);
      return '<li>' + row(esc(m[0]), m[1] ? '<i>' + esc(m[1]) + '</i>' : '') + '</li>';
    }).join('') + '</ol></li>');
    if (rs.hobbies) add.push('<li><b>Hobbies:</b> ' + esc(rs.hobbies) + '</li>');
    if (add.length) h += '<h4 class="cv-h">Additional Information</h4><ul class="cv-add">' + add.join('') + '</ul>';
    return h + '</div>';
  }

  function renderResume() { var p = $('rsPreview'); if (!p) return; p.innerHTML = resumeHtml(); checkBullets(); }

  function jobForm(j, ji) {
    return '<fieldset class="rs-job"><legend>Company ' + (ji + 1) + '</legend>' +
      '<div class="rs-row"><label>Company<input data-j="' + ji + '" data-f="company" value="' + esc(j.company) + '" placeholder="AccuKnox India Pvt. Ltd."></label>' +
      '<label>Location<input data-j="' + ji + '" data-f="city" value="' + esc(j.city) + '" placeholder="Bangalore, IN"></label></div>' +
      j.roles.map(function (r, ri) {
        return '<div class="rs-roleform"><div class="rs-row"><label>Role ' + (ri + 1) + ' title<input data-j="' + ji + '" data-r="' + ri + '" data-f="title" value="' + esc(r.title) + '" placeholder="Product Marketing Manager"></label>' +
          '<label>Dates<input data-j="' + ji + '" data-r="' + ri + '" data-f="dates" value="' + esc(r.dates) + '" placeholder="April 2024 to Present"></label></div>' +
          '<label>Achievements, one per line. Start with "Label:" to bold it<textarea data-j="' + ji + '" data-r="' + ri + '" data-f="bullets" rows="4" placeholder="Marketing: Drive 2 Cr influenced pipeline on a 40 L yearly budget">' + esc(r.bullets) + '</textarea></label>' +
          '<label>Tools involved, optional<input data-j="' + ji + '" data-r="' + ri + '" data-f="tools" value="' + esc(r.tools) + '" placeholder="Salesforce, HubSpot, Figma, Apollo"></label>' +
          '<div class="rs-jobact">' + (j.roles.length > 1 ? '<button type="button" class="rs-delrole" data-j="' + ji + '" data-r="' + ri + '">Remove role</button>' : '') +
          '<button type="button" class="rs-ai" data-j="' + ji + '" data-r="' + ri + '">Tighten bullets</button></div></div>';
      }).join('') +
      '<div class="rs-jobact"><button type="button" class="rs-addrole" data-j="' + ji + '">+ Another role at this company</button>' +
      (rs.jobs.length > 1 ? '<button type="button" class="rs-deljob" data-j="' + ji + '">Remove company</button>' : '') + '</div></fieldset>';
  }

  function renderExpForm() {
    var box = $('rsExp'); if (!box) return;
    box.innerHTML = rs.jobs.map(jobForm).join('');
    box.querySelectorAll('[data-f]').forEach(function (el) {
      el.addEventListener('input', function () {
        var j = rs.jobs[+el.getAttribute('data-j')], r = el.getAttribute('data-r');
        (r == null ? j : j.roles[+r])[el.getAttribute('data-f')] = el.value; renderResume();
      });
      if (el.getAttribute('data-f') === 'bullets') el.addEventListener('focus', function () { lastBulletBox = el; });
    });
    box.querySelectorAll('.rs-addrole').forEach(function (b) { b.addEventListener('click', function () { rs.jobs[+b.getAttribute('data-j')].roles.push(blankRole()); renderExpForm(); renderResume(); }); });
    box.querySelectorAll('.rs-delrole').forEach(function (b) { b.addEventListener('click', function () { rs.jobs[+b.getAttribute('data-j')].roles.splice(+b.getAttribute('data-r'), 1); renderExpForm(); renderResume(); }); });
    box.querySelectorAll('.rs-deljob').forEach(function (b) { b.addEventListener('click', function () { rs.jobs.splice(+b.getAttribute('data-j'), 1); renderExpForm(); renderResume(); }); });
    box.querySelectorAll('.rs-ai').forEach(function (b) { b.addEventListener('click', function () { tighten(+b.getAttribute('data-j'), +b.getAttribute('data-r'), b); }); });
  }

  function renderEduForm() {
    var box = $('rsEdu'); if (!box) return;
    box.innerHTML = rs.edu.map(function (e, i) {
      return '<div class="rs-edu"><div class="rs-row"><label>Institution<input data-e="' + i + '" data-f="school" value="' + esc(e.school) + '" placeholder="BITS Pilani"></label>' +
        '<label>Degree<input data-e="' + i + '" data-f="degree" value="' + esc(e.degree) + '" placeholder="MBA, AI and Digital Business"></label></div>' +
        '<div class="rs-row"><label>Location<input data-e="' + i + '" data-f="city" value="' + esc(e.city) + '" placeholder="Bangalore, IN"></label>' +
        '<label>Years<input data-e="' + i + '" data-f="years" value="' + esc(e.years) + '" placeholder="2024 - 2026"></label></div>' +
        (rs.edu.length > 1 ? '<div class="rs-jobact"><button type="button" class="rs-deledu" data-e="' + i + '">Remove</button></div>' : '') + '</div>';
    }).join('');
    box.querySelectorAll('[data-e]').forEach(function (el) {
      if (el.tagName === 'BUTTON') el.addEventListener('click', function () { rs.edu.splice(+el.getAttribute('data-e'), 1); renderEduForm(); renderResume(); });
      else el.addEventListener('input', function () { rs.edu[+el.getAttribute('data-e')][el.getAttribute('data-f')] = el.value; renderResume(); });
    });
  }

  var WEAK = /^(responsible for|worked on|helped|involved in|assisted|participated|handled|tasked with|duties)/i;
  function allBullets() { var a = []; rs.jobs.forEach(function (j) { j.roles.forEach(function (r) { lines(r.bullets).forEach(function (b) { a.push(b.replace(/^[A-Z][A-Za-z0-9&/ +.]{1,32}:\s+/, '')); }); }); }); return a; }
  function checkBullets() {
    var box = $('rsCheck'); if (!box) return;
    var all = allBullets();
    if (!all.length) { box.innerHTML = '<p>Add achievements and each bullet is checked for a strong verb and a number.</p>'; return; }
    var issues = 0, rows = all.map(function (b) {
      var f = [];
      if (WEAK.test(b)) f.push('weak opening, start with a verb like Launched, Built, Grew, Closed');
      if (!/\d/.test(b)) f.push('no number');
      if (b.split(/\s+/).length > 32) f.push('over 32 words');
      if (/[—–]/.test(b)) f.push('long dash, use a comma');
      if (f.length) issues++;
      return '<li class="' + (f.length ? 'warn' : 'ok') + '"><span>' + esc(b.length > 70 ? b.slice(0, 70) + '...' : b) + '</span><em>' + (f.length ? esc(f.join(', ')) : 'strong') + '</em></li>';
    });
    box.innerHTML = '<p><b>' + (all.length - issues) + ' of ' + all.length + '</b> bullets look strong.</p><ul>' + rows.join('') + '</ul>';
  }

  function tighten(ji, ri, btn) {
    var j = rs.jobs[ji], x = j.roles[ri], b = lines(x.bullets);
    if (!b.length) return;
    var old = btn.textContent; btn.textContent = 'Working...'; btn.disabled = true;
    callAI('bullets', [{ role: 'user', content: 'Role: ' + (x.title || '') + ' at ' + (j.company || '') + '\nKeep any "Label:" prefix.\nBullets:\n' + b.map(function (l) { return '- ' + l; }).join('\n') }])
      .then(function (reply) {
        btn.textContent = old; btn.disabled = false;
        var out;
        if (reply) out = lines(reply.split('\n').filter(function (l) { return /^\s*[-*•]/.test(l); }).join('\n'));
        if (!out || !out.length) out = b.map(function (l) {
          var m = l.match(/^([A-Z][A-Za-z0-9&/ +.]{1,32}:\s+)(.*)$/), pre = m ? m[1] : '', t = m ? m[2] : l;
          var weak = WEAK.test(t); t = t.replace(WEAK, '').replace(/^\s*(the|a)\s+/i, '').trim();
          t = weak ? 'Led ' + t : t.charAt(0).toUpperCase() + t.slice(1);
          if (!/\d/.test(t)) t += ', [add the result as a number]';
          return pre + t;
        });
        x.bullets = out.join('\n');
        var ta = document.querySelector('#rsExp textarea[data-j="' + ji + '"][data-r="' + ri + '"]'); if (ta) ta.value = x.bullets;
        renderResume();
        toast(reply ? 'Bullets tightened. Check every fact and number.' : 'Offline rewrite done. Replace each [placeholder] with your real number.');
        track('resume_tighten', { label: reply ? 'ai' : 'offline' });
      });
  }

  function renderIdeas(role) {
    var box = $('rsIdeas'); if (!box) return;
    var list = IDEAS[role] || [];
    box.innerHTML = list.map(function (t, i) { return '<button type="button" class="rs-idea" data-i="' + i + '"><span>+</span>' + esc(t) + '</button>'; }).join('');
    box.querySelectorAll('.rs-idea').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = list[+b.getAttribute('data-i')];
        var ta = lastBulletBox || document.querySelector('#rsExp textarea[data-f="bullets"]'); if (!ta) return;
        var r = rs.jobs[+ta.getAttribute('data-j')].roles[+ta.getAttribute('data-r')];
        r.bullets = (r.bullets ? r.bullets.replace(/\s+$/, '') + '\n' : '') + t; ta.value = r.bullets; renderResume();
        toast('Added. Replace the [brackets] with your real numbers.');
      });
    });
  }

  function resumeText() {
    var L = [rs.name || 'Your Name'];
    L.push([rs.linkedin, rs.email, rs.portfolio].filter(Boolean).join(' | '));
    L.push([rs.phone, rs.city].filter(Boolean).join(' | '));
    if (rs.highlight) L.push(rs.highlight);
    if (rs.yoe) L.push('Overall ' + rs.yoe + '+ YoE in ' + rs.env);
    var edu = rs.edu.filter(function (e) { return e.school; });
    if (edu.length) { L.push('', 'EDUCATION'); edu.forEach(function (e) { L.push(e.school + (e.city ? ', ' + e.city : ''), e.degree + (e.years ? ' (' + e.years + ')' : '')); }); }
    L.push('', 'PROFESSIONAL EXPERIENCE');
    rs.jobs.forEach(function (j) {
      if (!j.company) return; L.push('', j.company + (j.city ? ', ' + j.city : ''));
      j.roles.forEach(function (r) { if (r.title) L.push(r.title + (r.dates ? ' (' + r.dates + ')' : '')); lines(r.bullets).forEach(function (b) { L.push('- ' + b); }); if (r.tools) L.push('- Tools Involved: ' + r.tools); });
    });
    if (rs.vol && rs.vol.org) { L.push('', 'VOLUNTEERING', rs.vol.org + (rs.vol.city ? ', ' + rs.vol.city : ''), rs.vol.title + (rs.vol.dates ? ' (' + rs.vol.dates + ')' : '')); lines(rs.vol.bullets).forEach(function (b) { L.push('- ' + b); }); }
    L.push('', 'ADDITIONAL INFORMATION');
    if (rs.s1) L.push('- ' + rs.s1l + ': ' + rs.s1); if (rs.s2) L.push('- ' + rs.s2l + ': ' + rs.s2); if (rs.tools) L.push('- Tools: ' + rs.tools);
    if (rs.certs) { L.push('- Online Courses and Certificates:'); lines(rs.certs).forEach(function (c, i) { L.push('  ' + (i + 1) + '. ' + c); }); }
    if (rs.hobbies) L.push('- Hobbies: ' + rs.hobbies);
    return L.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  function fillForm() {
    document.querySelectorAll('#rsForm [data-k]').forEach(function (el) { el.value = rs[el.getAttribute('data-k')] || ''; });
    document.querySelectorAll('#rsForm [data-v]').forEach(function (el) { el.value = (rs.vol || {})[el.getAttribute('data-v')] || ''; });
    renderEduForm(); renderExpForm(); renderResume();
  }

  function initResume() {
    if (!$('rsForm')) return;
    rs = migrate(store.get(RS_KEY)) || blankResume('pmm');
    document.querySelectorAll('#rsForm [data-k]').forEach(function (el) {
      el.addEventListener('input', function () { rs[el.getAttribute('data-k')] = el.value; renderResume(); });
    });
    document.querySelectorAll('#rsForm [data-v]').forEach(function (el) {
      el.addEventListener('input', function () { rs.vol[el.getAttribute('data-v')] = el.value; renderResume(); });
    });
    var roleSel = $('rsRole');
    roleSel.value = rs.role || 'pmm';
    roleSel.addEventListener('change', function () {
      var d = DEFAULTS[roleSel.value] || {}, prev = DEFAULTS[rs.role] || {};
      ['s1l', 's1', 's2l', 's2', 'tools'].forEach(function (k) { if (!rs[k] || rs[k] === prev[k]) rs[k] = d[k] || ''; });
      rs.role = roleSel.value; fillForm(); renderIdeas(roleSel.value);
    });
    renderIdeas(roleSel.value);
    fillForm();
    $('rsAddEdu').addEventListener('click', function () { rs.edu.push({ school: '', degree: '', city: '', years: '' }); renderEduForm(); });
    $('rsAdd').addEventListener('click', function () { rs.jobs.push(blankJob()); renderExpForm(); renderResume(); });
    $('rsSample').addEventListener('click', function () {
      var s = SAMPLE[roleSel.value]; if (!s) return;
      rs = migrate(JSON.parse(JSON.stringify(s))); rs.role = roleSel.value; fillForm(); toast('Sample loaded. Replace it with your own details.');
    });
    $('rsSave').addEventListener('click', function () { toast(store.set(RS_KEY, rs) ? 'Saved in this browser only.' : 'Could not save in this browser.'); });
    $('rsClear').addEventListener('click', function () { if (!confirmClear()) return; rs = blankResume(roleSel.value); store.del(RS_KEY); fillForm(); });
    $('rsCopy').addEventListener('click', function () { copy(resumeText(), 'Resume copied as plain text.'); });
    $('rsPdf').addEventListener('click', function () { printDoc(resumeHtml(), 'ip-print-resume', (rs.name || 'Resume').replace(/\s+/g, '_') + '_Resume'); track('resume_pdf'); });
  }

  /* ---------------------------------------------------- cover letter */
  var cl = null;
  function blankCover() { return { name: '', email: '', phone: '', role: '', company: '', manager: '', current: '', why: '', a1: '', a2: '', notice: '', tone: 'crisp', kind: 'pmm' }; }
  var ANGLE = {
    pmm: 'I do my best work where product depth has to become a story that buyers repeat and sellers can win with: positioning, launches, competitive and enablement that move win rates, not just slides.',
    partnerships: 'I do my best work building partner motions that ship pipeline, not just logos: picking the right partners, enabling them to sell, and running joint plans that show up in the forecast.',
    sales: 'I do my best work in disciplined, curious selling: running real discovery, building multi-threaded deals and forecasting honestly, so the number lands quarter after quarter.'
  };
  function coverText() {
    var c = cl, co = c.company || '[Company]', role = c.role || '[Role]';
    var hi = c.manager ? 'Dear ' + c.manager + ',' : 'Dear Hiring Team,';
    var p1 = (c.tone === 'warm' ? 'I have followed ' + co + ' for a while, and I was excited to see the ' + role + ' opening. ' : 'I am applying for the ' + role + ' role at ' + co + '. ') + (c.why ? c.why.replace(/\s*$/, '').replace(/([^.!?])$/, '$1.') : 'What drew me in is the problem you are solving and the stage you are at.');
    var proof = [c.a1, c.a2].filter(Boolean).map(function (s) { s = s.trim().replace(/\.$/, ''); return s.charAt(0).toLowerCase() + s.slice(1); });
    var p2 = (c.current ? 'As ' + c.current + ', ' : 'In my current role, ') + (proof.length ? 'I ' + proof[0].replace(/^i\s+/i, '') + '.' + (proof[1] ? ' I also ' + proof[1].replace(/^i\s+/i, '') + '.' : '') : 'I have owned outcomes end to end and measured my work in results, not activity.');
    var p3 = ANGLE[c.kind] || ANGLE.pmm;
    var p4 = 'I am based in Bengaluru' + (c.notice ? ' and ' + c.notice.replace(/\.$/, '') : '') + '. I would welcome a conversation about where ' + co + ' wants to be in the next year and how I can help get there.';
    var sig = ['Regards,', c.name || '[Your Name]', [c.phone, c.email].filter(Boolean).join(' | ')].filter(Boolean).join('\n');
    return [hi, '', p1, '', p2, '', p3, '', p4, '', sig].join('\n');
  }
  function renderCover(force) {
    var ta = $('clOut'); if (!ta) return;
    if (force || !ta.dataset.edited) ta.value = coverText();
    var w = ta.value.split(/\s+/).filter(Boolean).length; var wc = $('clWords'); if (wc) wc.textContent = w + ' words' + (w > 260 ? ', aim for under 250' : '');
  }
  function initCover() {
    if (!$('clForm')) return;
    cl = store.get(CL_KEY) || blankCover();
    document.querySelectorAll('#clForm [data-k]').forEach(function (el) {
      el.value = cl[el.getAttribute('data-k')] || el.value;
      el.addEventListener('input', function () { cl[el.getAttribute('data-k')] = el.value; renderCover(); });
      el.addEventListener('change', function () { cl[el.getAttribute('data-k')] = el.value; renderCover(); });
    });
    var ta = $('clOut');
    ta.addEventListener('input', function () { ta.dataset.edited = '1'; renderCover(); });
    $('clRegen').addEventListener('click', function () { delete ta.dataset.edited; renderCover(true); });
    $('clAi').addEventListener('click', function () {
      var b = $('clAi'), old = b.textContent; b.textContent = 'Polishing...'; b.disabled = true;
      var c = cl;
      callAI('cover', [{ role: 'user', content: 'Write my cover letter.\nRole: ' + c.role + '\nCompany: ' + c.company + '\nHiring manager: ' + (c.manager || 'unknown') + '\nMy current role: ' + c.current + '\nWhy this company: ' + c.why + '\nProof point 1: ' + c.a1 + '\nProof point 2: ' + c.a2 + '\nNotice and location: Bengaluru, ' + c.notice + '\nTone: ' + c.tone + '\nSign off with: ' + c.name + (c.email ? ', ' + c.email : '') }])
        .then(function (reply) {
          b.textContent = old; b.disabled = false;
          if (reply) { ta.value = reply.trim(); ta.dataset.edited = '1'; renderCover(); toast('Polished with AI. Check every fact before you send it.'); }
          else toast('AI is unavailable right now. The draft above is ready to edit.');
          track('cover_polish', { label: reply ? 'ai' : 'offline' });
        });
    });
    $('clSave').addEventListener('click', function () { toast(store.set(CL_KEY, cl) ? 'Saved in this browser only.' : 'Could not save in this browser.'); });
    $('clCopy').addEventListener('click', function () { copy(ta.value, 'Cover letter copied.'); });
    $('clPdf').addEventListener('click', function () {
      var html = ta.value.split(/\n{2,}/).map(function (p) { return '<p>' + esc(p).replace(/\n/g, '<br>') + '</p>'; }).join('');
      var hd = '<div class="cv"><div class="cv-top"><div class="cv-id"><h3 class="cv-name">' + (esc(cl.name) || 'Your Name') + '</h3><p>' + [cl.email, cl.phone].filter(Boolean).map(esc).join(' | ') + '</p></div></div><div class="cl-doc">' + html + '</div></div>';
      printDoc(hd, 'ip-print-cover', (cl.name || 'Cover').replace(/\s+/g, '_') + '_Cover_Letter'); track('cover_pdf');
    });
    renderCover();
  }

  /* ----------------------------------------------------------- shared */
  function confirmClear() { try { return window.confirm('Clear everything in the resume builder?'); } catch (e) { return true; } }
  function toast(t) {
    var el = $('ipToast'); if (!el) return;
    el.textContent = t; el.classList.add('on'); clearTimeout(el._t); el._t = setTimeout(function () { el.classList.remove('on'); }, 3200);
  }
  function copy(text, msg) {
    var done = function () { toast(msg); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
    else { fallbackCopy(text); done(); }
  }
  function fallbackCopy(text) { var t = document.createElement('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (e) { } t.remove(); }
  function printDoc(html, cls, title) {
    var area = $('ipPrint'); if (!area) return;
    area.className = cls; area.innerHTML = html;
    var old = document.title; document.title = title;
    document.documentElement.classList.add('ip-printing');
    var after = function () { document.documentElement.classList.remove('ip-printing'); document.title = old; area.innerHTML = ''; window.removeEventListener('afterprint', after); };
    window.addEventListener('afterprint', after);
    setTimeout(function () { window.print(); setTimeout(function () { if (document.documentElement.classList.contains('ip-printing') && !window.matchMedia('print').matches) after(); }, 1500); }, 60);
  }

  function initTabs() {
    document.querySelectorAll('[data-tabs]').forEach(function (group) {
      var btns = group.querySelectorAll('[role="tab"]');
      btns.forEach(function (b) {
        b.addEventListener('click', function () {
          btns.forEach(function (x) { x.setAttribute('aria-selected', 'false'); x.classList.remove('on'); var p = $(x.getAttribute('aria-controls')); if (p) p.hidden = true; });
          b.setAttribute('aria-selected', 'true'); b.classList.add('on'); var p = $(b.getAttribute('aria-controls')); if (p) p.hidden = false;
        });
      });
    });
    if (location.hash === '#cover') { var c = document.querySelector('[aria-controls="tabCover"]'); if (c) c.click(); }
  }

  function initShorts() {
    document.querySelectorAll('.yt-frame').forEach(function (f) {
      var play = function () {
        var id = f.getAttribute('data-id'); if (!id || f.querySelector('iframe')) return;
        var i = document.createElement('iframe');
        i.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
        i.title = f.getAttribute('data-title') || 'YouTube video';
        i.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        i.setAttribute('allowfullscreen', ''); f.innerHTML = ''; f.appendChild(i);
        track('video_play', { label: id });
      };
      f.addEventListener('click', play);
      f.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
    });
  }

  function start() { initChat(); initBank(); initResume(); initCover(); initTabs(); initShorts(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
