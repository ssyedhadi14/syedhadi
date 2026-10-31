/* Created by: Claude
   Date: 2026-10-31
   Purpose: PDF report specs for the FIRE, mutual fund, PMM salary, Qums and loan calculators.
            Each page sets window.__calc = {kind:..., ...} from its own calc() and gives the download button id="pdfBtn".
            Rendering is done by /assets/report-pdf.js (SHReport).
   Owner: Syed Hadi */
(function () {
  'use strict';
  var VER = '20261031s', loading = null;
  function engine() {
    if (loading) return loading;
    loading = (window.SHReport ? Promise.resolve() : new Promise(function (res, rej) {
      var s = document.createElement('script'); s.src = '/assets/report-pdf.js?v=' + VER; s.onload = res; s.onerror = function () { rej(new Error('pdf engine')); }; document.head.appendChild(s);
    })).then(function () { return window.SHReport.ready(); });
    loading.catch(function () { loading = null; });
    return loading;
  }
  function today() { return new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }); }
  function P(x, d) { return (x * 100).toFixed(d == null ? (x * 100 % 1 ? 1 : 0) : d) + '%'; }
  var FOOT = 'Planning tool, not financial advice. Figures follow the assumptions on the page. Built by Syed Hadi, syedcreates.com';

  // ---------------- FIRE ----------------
  function fireSpec(s) {
    var F = window.SHReport.fmtINR, C = window.SHReport.C;
    var onTrack = s.gap >= 0, rows = s.rows.filter(function (r) { return r.age <= s.ret; }), pts = s.pts;
    var expM = s.expMonthly, yrs = s.ret - s.age;
    var verdict = onTrack
      ? ['On track. Your plan reaches ' + Math.round(s.pct) + '% of your FIRE number by ' + s.ret + ', a cushion of ' + F(s.gap) + '.', 'Keep the SIP step up going and review the plan once a year. Markets will not deliver ' + P(s.pre) + ' every year, so the cushion is your margin for the bad ones.']
      : ['Short by ' + F(-s.gap) + ' at age ' + s.ret + '. Three ways to close it: raise the SIP to ' + F(s.needSip) + ' a month, retire at ' + (s.fireAge ? s.fireAge : 'a later age') + ', or trim the retirement spend.', 'Small changes compound: a 10% step up every year on the same starting SIP usually closes most of a gap this size.'];
    var tbl = rows.filter(function (r, i) { return i % (rows.length > 30 ? 2 : 1) === 0 || r.age === s.ret; }).map(function (r) { return [String(r.age), F(r.bal), F(r.need), F(r.inv), r.bal >= r.need ? 'Yes' : 'Not yet']; });
    var hl = -1; tbl.forEach(function (r, i) { if (r[0] === String(s.ret)) hl = i; });
    return {
      kicker: 'SYEDCREATES.COM  /  FIRE PLAN', url: 'syedcreates.com/fire-calculator', docTitle: 'FIRE plan, retire at ' + s.ret,
      title: 'Your FIRE number is ' + F(s.tgt) + '. Here is how you get there.',
      subtitle: 'Financial independence at ' + s.ret + ', funded until ' + s.life + ', starting from age ' + s.age + ' with ' + F(s.mf + s.stk) + ' invested and a ' + F(s.sip) + ' monthly SIP. Prepared ' + today() + '.',
      meta: [['Age', String(s.age)], ['Retire at', String(s.ret)], ['Spend today', F(expM) + ' / mo'], ['SIP', F(s.sip) + ' / mo'], ['Step up', P(s.step)]],
      footer: FOOT,
      blocks: [
        { type: 'kpis', items: [
          { label: 'FIRE number at ' + s.ret, value: F(s.tgt), sub: 'funds ' + F(s.er / 12) + ' a month at ' + s.ret + ' (today’s ' + F(expM) + ' after inflation)', hero: true },
          { label: 'Projected corpus at ' + s.ret, value: F(s.balRet), sub: onTrack ? Math.round(s.pct) + '% of the target, cushion ' + F(s.gap) : Math.round(s.pct) + '% of the target, short by ' + F(-s.gap), color: onTrack ? C.green : C.rose },
          { label: 'SIP needed', value: F(s.needSip) + '/mo', sub: s.step > 0 ? 'rising ' + P(s.step) + ' a year, from today' : 'flat, from today' },
          { label: 'Financially free at', value: s.fireAge ? 'Age ' + s.fireAge : 'After 75', sub: s.fireAge ? 'when the corpus first covers the FIRE number for that age' : 'the corpus never covers the target in this plan' }
        ] },
        { type: 'callout', title: onTrack ? 'The verdict: on track' : 'The verdict: a gap to close', lines: verdict, tone: onTrack ? 'green' : 'amber' },
        { type: 'h2', title: 'Corpus versus the FIRE number', sub: 'Solid area: your corpus with SIP step ups until ' + s.ret + ', then drawdown at ' + P(s.post) + ' post retirement return. Dashed line: the FIRE number needed at each age.' },
        { type: 'area', xLabels: pts.map(function (p) { return p.age; }), height: 175,
          series: [
            { name: 'Your corpus', color: C.accent, values: pts.map(function (p) { return p.bal; }), opacity: 0.8 },
            { name: 'FIRE number at that age', color: C.rose, values: pts.map(function (p) { return p.need == null ? null : p.need; }), fill: false, dash: true }
          ],
          mark: { index: pts.findIndex(function (p) { return p.age === s.ret; }), value: s.balRet, label: 'Retire at ' + s.ret + ': ' + F(s.balRet) }, note: 'x axis: your age' },
        { type: 'h2', title: 'Four flavours of FIRE', sub: 'Same assumptions, different lifestyles.' },
        { type: 'kpis', items: [
          { label: 'Lean FIRE', value: F(s.lean), sub: '70% of your spend' },
          { label: 'Regular FIRE', value: F(s.tgt), sub: 'your spend as entered' },
          { label: 'Fat FIRE', value: F(s.fat), sub: '150% of your spend' },
          { label: 'Coast FIRE', value: F(s.coast), sub: (s.mf + s.stk) >= s.coast ? 'needed invested today. You are there.' : 'needed invested today, no further SIP' }
        ] },
        { type: 'h2', title: 'What this plan assumes', sub: 'Every figure here is an input on the page.' },
        { type: 'kv', cols: 2, rows: [
          ['Monthly spend today', F(expM)], ['Retirement spend factor', P(s.rf) + ' of today’s spend'], ['Already invested', F(s.mf) + ' MF + ' + F(s.stk) + ' stocks'], ['Monthly SIP', F(s.sip) + ', step up ' + P(s.step)],
          ['Equity share', P(s.eqp)], ['Equity return', P(s.eqr)], ['Debt return', P(s.dbr)], ['Blended pre retirement return', P(s.pre)],
          ['Inflation', P(s.inf)], ['Post retirement return', P(s.post)], ['Safety buffer', P(s.buf) + ' on the corpus'], ['Life expectancy', 'Age ' + s.life]
        ] },
        { type: 'h2', title: 'Three moves that change the outcome most', sub: 'In order of impact in this model.' },
        { type: 'steps', items: [
          ['Step up the SIP every year', 'A ' + P(Math.max(s.step, 0.1)) + ' annual step up on ' + F(s.sip) + ' puts far more in than a bigger flat SIP, because the biggest contributions land in the final, highest earning years.'],
          ['Keep the spend growth below the income growth', 'The FIRE number is 25 to 30 times your annual spend. Every ' + F(1000) + ' a month you trim today removes about ' + F(1000 * 12 * 28 * Math.pow(1 + s.inf, yrs)) + ' from the target at ' + s.ret + '.'],
          ['Do not panic sell in the last five years', 'Sequence risk is highest just before and after ' + s.ret + '. Move two to three years of spend into debt as you approach it, so a bad market does not force you to sell equity.']
        ] },
        { type: 'page', ifBelow: 0.5 },
        { type: 'h2', title: 'Year by year', sub: 'Corpus, the FIRE number for retiring at that age, and what you have put in. Highlighted row is your target age.' },
        { type: 'table', head: ['Age', 'Corpus', 'FIRE number at that age', 'Total invested', 'Covered?'], rows: tbl, highlight: hl, align: ['left', 'right', 'right', 'right', 'right'], rowHeight: 14, fontSize: 8 },
        { type: 'signoff' }
      ]
    };
  }

  // ---------------- Mutual funds ----------------
  function mfSpec(s) {
    var F = window.SHReport.fmtINR, C = window.SHReport.C, f = s.fund;
    var hz = s.horizons; // [{y, inv, val, gain, tax, real, fd}]
    var last = hz[hz.length - 1], mult = last.inv ? (last.val / last.inv) : 0;
    var yrs = []; for (var y = 1; y <= 20; y++) yrs.push(y);
    var series = yrs.map(function (y) { return s.fv(y); });
    var fdS = yrs.map(function (y) { return s.fvAt(y, 0.07); });
    var invS = series.map(function (o) { return o.inv; });
    var past = [['1 year', f.r1], ['3 year', f.r3], ['5 year', f.r5], ['10 year', f.r10 != null ? f.r10 : f.rr10], ['15 year', f.r15], ['20 year', f.r20]].filter(function (r) { return r[1] != null; }).map(function (r) { return [r[0] + ' CAGR', r[1].toFixed(1) + '% a year']; });
    return {
      kicker: 'SYEDCREATES.COM  /  MUTUAL FUND PROJECTION', url: 'syedcreates.com/mutual-fund-returns-calculator', docTitle: f.n + ' projection',
      title: (s.mode === 'sip' ? F(s.amt) + ' a month in ' : F(s.amt) + ' once in ') + f.n + '.',
      subtitle: f.c + ' fund by ' + f.h + '. Projection at ' + s.rate.toFixed(1) + '% a year (' + s.rateNote + '). Past returns are not a promise. Prepared ' + today() + '.',
      meta: [['Fund', f.c], ['Mode', s.mode === 'sip' ? 'Monthly SIP' : 'Lumpsum'], ['Amount', F(s.amt)], ['Assumed return', s.rate.toFixed(1) + '%'], ['Track record', s.ageTxt]],
      footer: 'Not investment advice. Returns are historical CAGR or your own assumption, not a prediction. Mutual fund investments are subject to market risk. Built by Syed Hadi, syedcreates.com',
      blocks: [
        { type: 'kpis', items: [
          { label: 'Value after 20 years', value: F(last.val), sub: 'you put in ' + F(last.inv) + ', ' + mult.toFixed(1) + 'x your money', hero: true },
          { label: 'After 10 years', value: F(hz[1].val), sub: 'you put in ' + F(hz[1].inv) + ', gain ' + F(hz[1].gain) },
          { label: 'Same money in a 7% FD, 20 yrs', value: F(last.fd), sub: 'the fund route adds ' + F(last.val - last.fd) + ' before tax', color: C.amber },
          { label: '20 year value in today’s money', value: F(last.real), sub: 'at 6% inflation. This is the number to plan with.' }
        ] },
        { type: 'h2', title: 'Growth over 20 years', sub: 'Projected value against what you put in and a 7% fixed deposit, same cash flows.' },
        { type: 'area', xLabels: yrs.map(function (y) { return 'Y' + y; }), height: 170,
          series: [
            { name: f.n.length > 34 ? f.n.slice(0, 32) + '…' : f.n, color: C.accent, values: series.map(function (o) { return o.val; }), opacity: 0.8 },
            { name: 'FD at 7%', color: C.amber, values: fdS, fill: false },
            { name: 'Money you put in', color: C.ink, values: invS, fill: false, dash: true }
          ], mark: { index: 19, value: last.val, label: 'Year 20: ' + F(last.val) }, note: 'nominal rupees' },
        { type: 'h2', title: 'Horizon by horizon', sub: 'Value, what you invested, estimated LTCG tax and the value in today’s money.' },
        { type: 'table', head: ['Horizon', 'You invest', 'Value', 'Gain', 'Multiple', 'Est. tax', 'Today’s money', 'FD at 7%'],
          rows: hz.map(function (o) { return [o.y + ' years', F(o.inv), F(o.val), F(o.gain), (o.inv ? (o.val / o.inv).toFixed(1) : '0') + 'x', o.tax == null ? 'Slab rate' : F(o.tax), F(o.real), F(o.fd)]; }), rowHeight: 16, fontSize: 8.4 },
        { type: 'h2', title: 'This fund’s track record', sub: 'Point to point CAGR as of ' + f.asof + ', NAV ₹' + f.nav + '. R marks regular plan data where direct plan history is shorter.' },
        { type: 'kv', cols: 2, rows: past.concat([['Category', f.c], ['AMC', f.h], ['Age of the fund', s.ageTxt], ['Swings', s.swing + ' volatility']]) },
        { type: 'h2', title: 'How to read this', sub: 'Three honest caveats.' },
        { type: 'bullets', items: [
          ['Past CAGR is a rear view mirror.', 'The projection uses ' + s.rate.toFixed(1) + '%. Equity funds routinely swing between -20% and +40% in a single year. The cautious mode on the page knocks 3% off for exactly this reason.'],
          ['Tax is estimated, not computed.', 'Equity gains above ₹1.25 lakh a year are taxed at 12.5% as long term capital gains. Debt and liquid funds are taxed at your slab. Check with a CA before filing.'],
          ['Today’s money matters more than the headline.', 'At 6% inflation, ' + F(last.val) + ' in 20 years buys what ' + F(last.real) + ' buys now.']
        ] },
        { type: 'signoff' }
      ]
    };
  }

  // ---------------- PMM salary ----------------
  function pmmSpec(s) {
    var C = window.SHReport.C, f = s.fmt;
    var cur = s.you, b = s.band, pos = cur == null ? null : cur < b[0] ? 'below' : cur < b[1] ? 'lower' : cur <= b[2] ? 'upper' : 'above';
    var verdict = cur == null ? ['Enter your current pay on the page to see where you sit in the band.'] :
      pos === 'below' ? ['You are below the modelled band. There is room to negotiate, by about ' + f(b[1] - cur) + ' to reach typical.', 'Anchor on the typical number, bring two comparable public ranges, and ask for the title correction at the same time.'] :
      pos === 'lower' ? ['You are in the lower half of the band. Typical for this profile is ' + f(b[1]) + '.', 'The fastest lever is scope: own a launch or a partner motion end to end and re benchmark in six months.'] :
      pos === 'upper' ? ['You are in the upper half of the band. Strong offers reach ' + f(b[2]) + '.', 'Negotiate on variable pay, ESOPs and title next, because fixed pay has less room from here.'] :
      ['You are above the modelled band for this profile. Nice.', 'Protect it: document outcomes in revenue terms every quarter so the number survives the next reorg.'];
    return {
      kicker: 'SYEDCREATES.COM  /  INDIA PMM SALARY 2026', url: 'syedcreates.com/pmm-salary-2026', docTitle: 'PMM salary benchmark 2026',
      title: 'Typical pay for your profile is ' + f(b[1]) + ' a year.',
      subtitle: s.level + ', ' + s.city + ', ' + s.company + ', ' + s.domain + '. Modelled from 3,300+ publicly reported Indian salaries. Prepared ' + today() + '.',
      meta: [['Level', s.levelShort], ['City', s.city], ['Company', s.companyShort], ['Domain', s.domainShort]],
      footer: 'A modelled estimate, not an offer. Bands anchor on public AmbitionBox and PayScale ranges. City, company and domain adjustments are assumptions. Built by Syed Hadi, syedcreates.com',
      blocks: [
        { type: 'kpis', items: [
          { label: 'Low', value: f(b[0]), sub: 'bottom of the modelled band, fixed pay per year' },
          { label: 'Typical', value: f(b[1]), sub: 'the number to anchor a negotiation on', hero: true },
          { label: 'Strong', value: f(b[2]), sub: 'top offers for this profile' },
          { label: 'Your current pay', value: cur == null ? 'Not entered' : f(cur), sub: cur == null ? 'enter it on the page for a verdict' : pos === 'below' ? 'below the band' : pos === 'lower' ? 'lower half of the band' : pos === 'upper' ? 'upper half of the band' : 'above the band', color: pos === 'below' ? C.rose : pos === 'above' ? C.green : C.accent }
        ] },
        { type: 'callout', title: 'Where you sit', lines: verdict, tone: pos === 'below' ? 'amber' : pos === 'above' || pos === 'upper' ? 'green' : 'accent' },
        { type: 'h2', title: 'The band across levels', sub: 'Same city, company and domain multipliers applied to every level, fixed pay in lakhs per year.' },
        { type: 'bars', cats: s.levels.map(function (l) { return l.short; }), yFormat: function (v) { return v >= 100 ? (v / 100).toFixed(1) + ' Cr' : Math.round(v) + ' L'; },
          series: [
            { name: 'Low', color: C.lav, values: s.levels.map(function (l) { return l.band[0]; }) },
            { name: 'Typical', color: C.accent, values: s.levels.map(function (l) { return l.band[1]; }) },
            { name: 'Strong', color: C.navy2, values: s.levels.map(function (l) { return l.band[2]; }) }
          ], note: 'lakhs per year, fixed pay' },
        { type: 'h2', title: 'How the number is built', sub: 'Base band for the level, then three multipliers.' },
        { type: 'kv', cols: 2, rows: [['Level', s.level], ['Base band', f(s.base[0]) + ' / ' + f(s.base[1]) + ' / ' + f(s.base[2])], ['City multiplier', s.city + ' × ' + s.m.city.toFixed(2)], ['Company multiplier', s.company + ' × ' + s.m.company.toFixed(2)], ['Domain multiplier', s.domain + ' × ' + s.m.domain.toFixed(2)], ['Combined', '× ' + s.m.total.toFixed(2)]] },
        { type: 'h2', title: 'Negotiation checklist', sub: 'What moves PMM pay in India in 2026, in order.' },
        { type: 'steps', items: [
          ['Benchmark before the first call', 'Quote the typical and strong numbers for your exact level and city. Recruiters respect ranges that come with a source.'],
          ['Sell outcomes, not activities', 'Pipeline influenced, launch adoption, partner sourced revenue. One slide with three numbers beats a long list of campaigns.'],
          ['Negotiate the whole package', 'Variable pay, ESOPs, joining bonus, notice period buyout and title. Fixed pay is one of six levers.'],
          ['Ask for a six month review in writing', 'Especially if you accept below typical. Put the re benchmark date in the offer letter.']
        ] },
        { type: 'signoff' }
      ]
    };
  }

  // ---------------- Qums ----------------
  function qumsSpec(d) {
    var C = window.SHReport.C, f = d.fmt;
    var rowsH = d.H.map(function (r) { return [r[0], f(r[1])]; }), rowsM = d.M.map(function (r) { return [r[0], f(r[1])]; });
    var blocks = [
      { type: 'kpis', items: [
        { label: 'Qums payable (20%)', value: f(d.k), sub: 'on a surplus of ' + f(d.net) + ' as of ' + d.dateLong, hero: true },
        { label: 'Sahm e Imam', value: f(d.k / 2), sub: 'half of the Qums, paid through your marja’s office or an authorised representative' },
        { label: 'Sahm e Sadat', value: f(d.k / 2), sub: 'half of the Qums, for deserving Sadat' },
        { label: 'Becomes Qums paid savings', value: f(d.carry), sub: 'carry this forward as already purified savings next year' }
      ] },
      { type: 'h2', title: 'How the surplus was worked out', sub: 'Everything you hold on the Qums date, minus what is already Qums paid or exempt.' },
      { type: 'split', title: 'Surplus of ' + f(d.net) + ' split', parts: [{ name: 'Qums 20%', value: d.k, color: C.accent }, { name: 'Stays with you 80%', value: Math.max(0, d.net - d.k), color: C.green }] },
      { type: 'table', head: ['What you hold on the Qums date', 'Amount (' + d.cur + ')'], rows: rowsH.concat([['Total', f(d.have)]]), highlight: rowsH.length, rowHeight: 16, fontSize: 8.6 },
      { type: 'table', head: ['Taken away', 'Amount (' + d.cur + ')'], rows: rowsM.concat([['Total', f(d.minus)]]), highlight: rowsM.length, rowHeight: 16, fontSize: 8.6 },
      { type: 'kv', cols: 2, rows: [['Surplus liable to Qums', f(d.net)], ['Qums payable (20%)', f(d.k)], ['Rulings followed', d.marja], ['Qums date', d.dateLong], ['Next Qums date', d.next], ['Currency', d.cur]] }
    ];
    if (d.L.length) blocks.push({ type: 'callout', title: 'Outstanding loans, not deducted: ' + f(d.loans), lines: d.L.map(function (r) { return r[0] + ': ' + f(r[1]); }).concat(['Loans and debts are not deducted from the surplus under the common rulings. Confirm your specific case with your marja’s office.']), tone: 'amber' });
    if (d.sistani) blocks.push({ type: 'h2', title: 'Paying Sahm e Imam through SabeelMedia', sub: 'For followers of Ayatollah Sistani. Ask for the current payment details before you transfer.' },
      { type: 'steps', items: [
        ['Message SabeelMedia on WhatsApp', '+91 89285 14110. Say you want to pay Sahm e Imam and ask for the current payment details.'],
        ['Maulana reference', 'Maulana Syed Afzal Hussain Kazmi, +91 84238 95696.'],
        ['Send the proof', 'After paying, send the payment screenshot on WhatsApp and ask for a receipt. YouTube: youtube.com/@media_sabeel. Instagram: @sabeelmedia_in.']
      ] });
    blocks.push({ type: 'callout', title: 'Please note', lines: ['This is a planning aid, not a fatwa. Confirm with the office of your marja before paying.', 'Reference: sistani.org/english/book/26890/8521/. Recalculate any time at syedcreates.com/qums.'], tone: 'accent' }, { type: 'signoff' });
    return {
      kicker: 'SYEDCREATES.COM  /  QUMS SUMMARY ' + d.year, url: 'syedcreates.com/qums', docTitle: 'Qums summary ' + d.year,
      title: (d.name ? d.name + ', your' : 'Your') + ' Qums for ' + d.year + ' comes to ' + f(d.k) + '.',
      subtitle: 'Qums date ' + d.dateLong + '. Rulings followed: ' + d.marja + '. Sahm e Imam ' + f(d.k / 2) + ' and Sahm e Sadat ' + f(d.k / 2) + '. Prepared ' + today() + '.',
      meta: [['Qums date', d.date], ['Marja', d.marja], ['Currency', d.cur], ['Surplus', f(d.net)]],
      footer: 'A planning aid, not a fatwa. Confirm with the office of your marja before paying. Built by Syed Hadi, syedcreates.com/qums',
      blocks: blocks
    };
  }

  // ---------------- Loan ----------------
  function loanSpec(s) {
    var F = window.SHReport.fmtINR, C = window.SHReport.C;
    var k = s.loanKind || 'Home', half = s.half, inv = s.invest;
    var blocks = [
      { type: 'kpis', items: [
        { label: 'Monthly EMI', value: F(s.emi), sub: F(s.P) + ' at ' + P(s.rate) + ' for ' + s.years + ' years', hero: true },
        { label: 'Total interest', value: F(s.totalInterest), sub: Math.round(s.totalInterest / s.P * 100) + '% of the amount borrowed, on top of it', color: C.rose },
        { label: 'Total you repay', value: F(s.totalPaid), sub: F(s.P) + ' principal + ' + F(s.totalInterest) + ' interest' },
        { label: 'Close it in ' + half.years + ' years', value: F(half.emiNeeded), sub: 'EMI needed instead of ' + F(s.emi) + ', saves ' + F(half.saved) + ' interest', color: C.green }
      ] },
      { type: 'h2', title: 'Where every EMI goes', sub: 'Early EMIs are mostly interest. That is why prepaying early saves the most.' },
      { type: 'split', title: 'Total repaid over ' + s.years + ' years: ' + F(s.totalPaid), parts: [{ name: 'Principal', value: s.P, color: C.accent }, { name: 'Interest', value: s.totalInterest, color: C.rose }] },
      { type: 'area', title: 'Outstanding balance by year, normal schedule versus the half time plan', xLabels: s.years_x, height: 160,
        series: [
          { name: 'Normal schedule', color: C.lav, values: s.balNormal, opacity: 0.9 },
          { name: half.label, color: C.green, values: s.balHalf, opacity: 0.85 }
        ], note: 'outstanding principal, rupees' },
      { type: 'h2', title: 'Four ways to close it faster', sub: 'Pick the one that fits your cash flow. The first three land at ' + half.years + ' years, the bonus rule shows what one extra EMI a year does on its own.' },
      { type: 'table', head: ['Strategy', 'What you do', 'Loan closes in', 'Interest paid', 'Interest saved'],
        rows: s.strategies.map(function (st) { return [st.name, st.how, st.closes, F(st.interest), F(st.saved)]; }), align: ['left', 'left', 'right', 'right', 'right'], rowHeight: 18, fontSize: 8.2 }
    ];
    if (inv) {
      blocks.push({ type: 'page', ifBelow: 0.55 },
        { type: 'h2', title: 'Prepay or invest the extra ' + F(inv.extra) + ' a month?', sub: 'After tax cost of the loan versus the expected return of investing the same money, with your tax breaks counted.' },
        { type: 'kpis', items: [
          { label: 'Effective loan cost after tax', value: P(inv.effRate), sub: 'nominal ' + P(s.rate) + ', after Section 24(b) and 80C benefits in the ' + P(inv.slab, 0) + ' slab', hero: true },
          { label: 'Expected investment return', value: P(inv.expRet), sub: 'what you believe a SIP in equity earns over the same years' },
          { label: 'Prepay: interest saved', value: F(inv.prepaySaved), sub: 'loan closes in ' + inv.prepayYears + ' years instead of ' + s.years, color: C.green },
          { label: 'Invest: corpus at the end', value: F(inv.investCorpus), sub: 'after ' + P(inv.ltcg) + ' LTCG, while the loan runs its full ' + s.years + ' years', color: C.accent }
        ] },
        { type: 'callout', title: inv.verdictTitle, lines: inv.verdictLines, tone: inv.tone },
        { type: 'h2', title: 'Year by year, prepay versus invest', sub: 'Net worth effect of each path at the end of every year: loan balance cleared versus investment corpus built.' },
        { type: 'area', xLabels: inv.x, height: 150, series: [
          { name: 'Invest path: corpus minus remaining loan', color: C.accent, values: inv.investNet, fill: false },
          { name: 'Prepay path: equity in the home (loan paid down)', color: C.green, values: inv.prepayNet, fill: false }
        ], note: 'rupees, both paths spend the same cash each month' },
        { type: 'table', head: ['Year', 'Balance, normal', 'Interest paid', 'Tax benefit', 'Balance, prepay path', 'Invest corpus'],
          rows: inv.rows, rowHeight: 14, fontSize: 8 });
    }
    blocks.push({ type: 'h2', title: 'Before you prepay', sub: 'Four checks that save people money.' },
      { type: 'bullets', items: [
        ['Floating rate loans have no prepayment penalty.', 'RBI rules bar penalties on floating rate loans to individuals. Fixed rate loans can carry 2 to 4%. Check your sanction letter.'],
        ['Ask for tenure reduction, not EMI reduction.', 'When you part prepay, banks default to lowering the EMI. Keep the EMI, cut the tenure. That is where the interest saving comes from.'],
        ['Keep six months of EMIs as an emergency fund first.', 'Prepaying with your last rupee and then borrowing on a credit card at 36% defeats the purpose.'],
        ['Use the bonus rule.', 'One extra EMI a year from a bonus, every year, closes a 20 year loan in about 16.']
      ] }, { type: 'signoff' });
    return {
      kicker: 'SYEDCREATES.COM  /  ' + k.toUpperCase() + ' LOAN PLAN', url: 'syedcreates.com/loan-calculator', docTitle: k + ' loan plan',
      title: 'Your ' + k.toLowerCase() + ' loan EMI is ' + F(s.emi) + '. Here is how to close it in ' + half.years + ' years instead of ' + s.years + '.',
      subtitle: F(s.P) + ' at ' + P(s.rate) + ' for ' + s.years + ' years costs ' + F(s.totalInterest) + ' in interest. The half time plan cuts that by ' + F(half.saved) + '. Prepared ' + today() + '.',
      meta: [['Loan', k], ['Amount', F(s.P)], ['Rate', P(s.rate)], ['Tenure', s.years + ' years'], ['EMI', F(s.emi)]],
      footer: 'Planning tool, not financial advice. Check prepayment terms in your sanction letter. Built by Syed Hadi, syedcreates.com/loan-calculator',
      blocks: blocks
    };
  }

  var BUILDERS = { fire: fireSpec, mf: mfSpec, pmm: pmmSpec, qums: qumsSpec, loan: loanSpec };
  function fileName(s) {
    var d = new Date().toISOString().slice(0, 10);
    return ({ fire: 'fire-plan-retire-at-' + s.ret, mf: 'mf-projection-' + String(s.fund && s.fund.n || 'fund').toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40), pmm: 'pmm-salary-benchmark-2026', qums: 'qums-summary-' + s.year, loan: String(s.loanKind || 'loan').toLowerCase() + '-loan-plan' }[s.kind] || 'report') + '-' + d + '.pdf';
  }
  function download(btn) {
    var s = window.__calc; if (!s || !BUILDERS[s.kind]) return;
    if (s.validate && !s.validate()) return;
    var old = btn.textContent; btn.disabled = true; btn.textContent = 'Building your PDF…';
    engine().then(function () { var doc = window.SHReport.build(BUILDERS[s.kind](s)); doc.save(fileName(s)); if (window.shTrack) shTrack(s.kind + '_pdf_download'); })
      .catch(function (e) { if (window.console) console.error(e); btn.textContent = 'PDF failed, reload and retry'; setTimeout(function () { btn.textContent = old; }, 3000); })
      .then(function () { btn.disabled = false; if (btn.textContent.indexOf('Building') === 0) btn.textContent = old; });
  }
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('#pdfBtn,[data-pdf]'); if (b) { e.preventDefault(); download(b); } });
  window.SHCalcReports = { download: download, specs: BUILDERS, engine: engine };
})();
