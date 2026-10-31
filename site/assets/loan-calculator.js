/* Created by: Claude
   Date: 2026-10-31
   Purpose: Loan EMI calculator for syedcreates.com/loan-calculator. Home, car and personal loans, a "close it in half the time"
            planner with three strategies, and an original prepay versus invest planner with Indian tax breaks.
   Owner: Syed Hadi
   Everything runs in the browser. No data leaves the page. */
(function () {
  'use strict';
  var $ = function (i) { return document.getElementById(i); };
  function num(v) { return parseFloat(String(v).replace(/[^0-9.]/g, '')) || 0; }
  function inr(n) { return Math.round(n).toLocaleString('en-IN'); }
  function short(n) {
    var a = Math.abs(n), s = n < 0 ? '-' : '';
    if (a >= 1e7) return s + '₹' + (a / 1e7).toFixed(a >= 1e9 ? 0 : 2) + ' Cr';
    if (a >= 1e5) return s + '₹' + (a / 1e5).toFixed(a >= 1e6 ? 1 : 2).replace(/\.00$/, '') + ' L';
    return s + '₹' + inr(a);
  }
  function pct(x, d) { return (x * 100).toFixed(d == null ? 1 : d).replace(/\.0$/, '') + '%'; }
  function yrs(m) { var y = Math.floor(m / 12), r = m % 12; return y + (y === 1 ? ' yr' : ' yrs') + (r ? ' ' + r + ' mo' : ''); }

  var KINDS = {
    home: { label: 'Home', P: 5000000, rate: 8.5, years: 20, max: 100000000, maxY: 30 },
    car: { label: 'Car', P: 800000, rate: 9.5, years: 7, max: 20000000, maxY: 10 },
    personal: { label: 'Personal', P: 500000, rate: 14, years: 5, max: 10000000, maxY: 7 }
  };
  var kind = 'home';

  // ---------- core math ----------
  function emiFor(P, r, n) { if (r <= 0) return P / n; var k = Math.pow(1 + r, n); return P * r * k / (k - 1); }
  // simulate a schedule. opts: {emi, extraMonthly, yearlyLump, stepUp (fraction per year), months cap}
  function run(P, r, emi, o) {
    o = o || {}; var bal = P, m = 0, interest = 0, paid = 0, yearly = [], yi = 0, yp = 0, yb = [P], e = emi, extra = o.extraMonthly || 0, cap = o.cap || 1200;
    while (bal > 0.5 && m < cap) {
      var i = bal * r, pr = Math.min(bal, e + extra - i); if (pr < 0) pr = 0; // negative amortisation guard
      bal -= pr; interest += i; paid += Math.min(e + extra, pr + i); yi += i; yp += pr; m++;
      if (m % 12 === 0) {
        if (o.yearlyLump && bal > 0.5) { var L = Math.min(bal, o.yearlyLump); bal -= L; paid += L; yp += L; }
        yearly.push({ year: m / 12, interest: yi, principal: yp, bal: Math.max(0, bal) }); yb.push(Math.max(0, bal)); yi = 0; yp = 0;
        if (o.stepUp) e = e * (1 + o.stepUp);
      }
    }
    if (m % 12) { yearly.push({ year: Math.ceil(m / 12), interest: yi, principal: yp, bal: 0 }); yb.push(0); }
    return { months: m, interest: interest, paid: paid, yearly: yearly, yb: yb };
  }
  function solve(lo, hi, f, target) { // find x in [lo,hi] where f(x) <= target (monotone decreasing)
    for (var k = 0; k < 40; k++) { var mid = (lo + hi) / 2; if (f(mid) > target) lo = mid; else hi = mid; }
    return hi;
  }

  var state = {};
  function readInputs() {
    var K = KINDS[kind];
    var P = Math.max(10000, Math.min(K.max, num($('amt').value) || K.P));
    var rate = Math.max(0.1, Math.min(40, num($('rate').value) || K.rate));
    var years = Math.max(1, Math.min(K.maxY, Math.round(num($('tenure').value) || K.years)));
    var targetY = Math.round(num($('target').value)) || Math.max(1, Math.round(years / 2));
    targetY = Math.max(1, Math.min(years - 1 || 1, targetY));
    return { P: P, rate: rate / 100, years: years, targetY: targetY };
  }

  function calc() {
    var I = readInputs(), P = I.P, r = I.rate / 12, n = I.years * 12, emi = emiFor(P, r, n);
    var base = run(P, r, emi, { cap: n + 1 });
    var tm = I.targetY * 12;
    // strategy 1: higher EMI
    var emi2 = emiFor(P, r, tm), s1 = run(P, r, emi2, { cap: tm + 1 });
    // strategy 2: same EMI + one lump sum every year
    var lump = solve(0, P, function (x) { return run(P, r, emi, { yearlyLump: x }).months; }, tm), s2 = run(P, r, emi, { yearlyLump: lump });
    // strategy 3: step up the EMI every year
    var step = solve(0, 1, function (x) { return run(P, r, emi, { stepUp: x }).months; }, tm), s3 = run(P, r, emi, { stepUp: step });
    // bonus rule: one extra EMI a year
    var s4 = run(P, r, emi, { yearlyLump: emi });
    var years_x = [], balNormal = [], balHalf = [];
    for (var y = 0; y <= I.years; y++) { years_x.push('Y' + y); balNormal.push(base.yb[y] == null ? 0 : base.yb[y]); balHalf.push(s1.yb[y] == null ? 0 : s1.yb[y]); }
    var strategies = [
      { name: 'Raise the EMI', how: 'Pay ' + short(emi2) + ' a month instead of ' + short(emi), closes: yrs(s1.months), interest: s1.interest, saved: base.interest - s1.interest, extra: emi2 - emi },
      { name: 'One lump sum a year', how: 'Keep the EMI, prepay ' + short(lump) + ' every year (bonus, increment, RSUs)', closes: yrs(s2.months), interest: s2.interest, saved: base.interest - s2.interest, extra: lump / 12 },
      { name: 'Step up the EMI yearly', how: 'Raise the EMI ' + pct(step) + ' every year, in line with increments', closes: yrs(s3.months), interest: s3.interest, saved: base.interest - s3.interest, extra: step },
      { name: 'Bonus rule, 13 EMIs a year', how: 'One extra EMI of ' + short(emi) + ' every year', closes: yrs(s4.months), interest: s4.interest, saved: base.interest - s4.interest, extra: emi / 12 }
    ];
    state = { kind: KINDS[kind].label, kindKey: kind, P: P, rate: I.rate, years: I.years, emi: emi, totalInterest: base.interest, totalPaid: base.paid, base: base,
      half: { years: I.targetY, emiNeeded: emi2, saved: base.interest - s1.interest, label: 'Close in ' + I.targetY + ' years (higher EMI)' }, years_x: years_x, balNormal: balNormal, balHalf: balHalf, strategies: strategies };
    state.invest = investPlan(state);
    render();
  }

  // ---------- prepay vs invest ----------
  function investPlan(s) {
    var extra = num($('extra').value), slab = num($('slab').value) / 100, expRet = num($('expRet').value) / 100, ltcg = 0.125;
    var co = $('cobor').checked ? 2 : 1, c80 = $('c80').checked ? 150000 * co : 0, cap24 = (s.kindKey === 'home' ? 200000 : 0) * co;
    if (!(extra > 0)) return null;
    var P = s.P, r = s.rate / 12, n = s.years * 12, emi = s.emi, mr = Math.pow(1 + expRet, 1 / 12) - 1;
    // path A: invest the extra, loan runs normally. path B: prepay the extra, then invest EMI+extra after closure.
    var balA = P, balB = P, corpA = 0, corpB = 0, putA = 0, putB = 0, closedB = null, rows = [], x = ['Y0'], netA = [0], netB = [0];
    var yIntA = 0, yPrA = 0, yIntB = 0, yPrB = 0, taxA = 0, taxB = 0;
    for (var m = 1; m <= n; m++) {
      // A
      if (balA > 0.5) { var iA = balA * r, pA = Math.min(balA, emi - iA); balA -= pA; yIntA += iA; yPrA += pA; }
      corpA = corpA * (1 + mr) + extra; putA += extra;
      // B
      if (balB > 0.5) { var iB = balB * r, pB = Math.min(balB, emi + extra - iB); balB -= pB; yIntB += iB; yPrB += pB; if (balB <= 0.5 && closedB == null) closedB = m; }
      else { corpB = corpB * (1 + mr) + emi + extra; putB += emi + extra; }
      if (m % 12 === 0 || m === n) {
        var tA = slab * (Math.min(yIntA, cap24) + Math.min(yPrA, c80)), tB = slab * (Math.min(yIntB, cap24) + Math.min(yPrB, c80));
        corpA += tA; corpB += tB; putA += tA; putB += tB; taxA += tA; taxB += tB;
        var y = Math.ceil(m / 12);
        rows.push([String(y), short(Math.max(0, balA)), short(yIntA), short(tA), short(Math.max(0, balB)), short(corpA)]);
        x.push('Y' + y); netA.push(P - Math.max(0, balA) + corpA); netB.push(P - Math.max(0, balB) + corpB);
        yIntA = 0; yPrA = 0; yIntB = 0; yPrB = 0;
      }
    }
    function afterTax(c, put) { return c - Math.max(0, c - put) * ltcg; }
    var wealthA = afterTax(corpA, putA), wealthB = afterTax(corpB, putB);
    var int1 = P * s.rate, effRate = s.rate * (1 - slab * Math.min(1, cap24 / Math.max(1, int1)));
    var normalInt = s.totalInterest, prepayInt = 0; // interest in path B
    var sB = run(P, r, emi, { extraMonthly: extra }); prepayInt = sB.interest;
    var diff = wealthA - wealthB, investWins = diff > 0;
    var verdictTitle = investWins ? 'Investing the extra wins by ' + short(Math.abs(diff)) : 'Prepaying wins by ' + short(Math.abs(diff));
    var lines = [
      'After tax, this loan costs you about ' + pct(effRate) + ' a year. You expect ' + pct(expRet, 0) + ' from investing. ' + (expRet > effRate ? 'On paper the spread favours investing.' : 'The spread favours prepaying.'),
      'Prepaying ' + short(extra) + ' a month closes the loan in ' + yrs(sB.months) + ' instead of ' + s.years + ' years and saves ' + short(normalInt - prepayInt) + ' of interest. Investing the same money, while the loan runs full term, builds ' + short(wealthA) + ' after tax.',
      investWins ? 'The catch: that return is not guaranteed and the interest saving is. If you would lose sleep over a 30% drawdown, prepay. Many people do half and half.' : 'Prepaying is the guaranteed return here. Keep the emergency fund and insurance in place first, then prepay with tenure reduction, not EMI reduction.'
    ];
    return { extra: extra, slab: slab, expRet: expRet, ltcg: ltcg, effRate: effRate, prepaySaved: normalInt - prepayInt, prepayYears: Math.round(sB.months / 12 * 10) / 10, investCorpus: wealthA, prepayWealth: wealthB,
      wealthA: wealthA, wealthB: wealthB, investWins: investWins, diff: diff, verdictTitle: verdictTitle, verdictLines: lines, tone: investWins ? 'accent' : 'green', x: x, investNet: netA, prepayNet: netB, rows: rows, taxA: taxA, taxB: taxB, co: co, c80: c80, cap24: cap24 };
  }

  // ---------- render ----------
  function render() {
    var s = state, H = s.half;
    $('oEmi').textContent = short(s.emi); $('mN').textContent = short(s.emi);
    $('oEmiS').textContent = 'per month for ' + s.years + ' years';
    $('oInt').textContent = short(s.totalInterest); $('oIntS').textContent = Math.round(s.totalInterest / s.P * 100) + '% of what you borrowed';
    $('oPaid').textContent = short(s.totalPaid);
    $('oHalf').textContent = short(H.emiNeeded); $('oHalfS').textContent = 'EMI to close in ' + H.years + ' years, saves ' + short(H.saved);
    $('tgtLbl').textContent = H.years + (H.years === 1 ? ' year' : ' years');
    document.querySelectorAll('.ln-tgt').forEach(function (e) { e.textContent = H.years; });
    var pi = s.P / s.totalPaid * 100;
    $('splitP').style.width = pi + '%'; $('splitI').style.width = (100 - pi) + '%';
    $('splitL').innerHTML = '<span><i class="p"></i>Principal ' + short(s.P) + ' (' + Math.round(pi) + '%)</span><span><i class="i"></i>Interest ' + short(s.totalInterest) + ' (' + Math.round(100 - pi) + '%)</span>';
    var vd = $('vd'), ratio = s.totalInterest / s.P;
    vd.className = 'fr-verdict ' + (ratio > 0.6 ? 'no' : 'ok');
    vd.innerHTML = '<b>' + (ratio > 0.6 ? 'Interest heavy.' : 'Manageable.') + '</b> On ' + short(s.P) + ' at ' + pct(s.rate) + ' for ' + s.years + ' years you pay <b>' + short(s.totalInterest) + '</b> in interest. Closing it in ' + H.years + ' years instead cuts that to <b>' + short(s.totalInterest - H.saved) + '</b>, a saving of ' + short(H.saved) + '.';
    // strategies
    $('strat').innerHTML = s.strategies.map(function (st, i) {
      return '<div class="ln-st"><i>0' + (i + 1) + '</i><b>' + st.name + '</b><p>' + st.how + '.</p><div class="ln-st-k"><span><small>Loan closes in</small>' + st.closes + '</span><span><small>Interest saved</small>' + short(st.saved) + '</span></div></div>';
    }).join('');
    drawChart();
    buildTable();
    renderInvest();
    saveLink();
  }
  function drawChart() {
    var s = state, W = 640, Hh = 240, L = 54, R = 12, T = 14, B = 30, n = s.balNormal.length;
    var max = Math.max.apply(null, s.balNormal) * 1.06 || 1;
    var x = function (i) { return L + i / (n - 1) * (W - L - R); }, y = function (v) { return T + (1 - v / max) * (Hh - T - B); };
    var svg = '', k;
    for (k = 0; k <= 4; k++) { var v = max * k / 4, yy = y(v); svg += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + yy + '" y2="' + yy + '" class="g"/><text x="' + (L - 6) + '" y="' + (yy + 4) + '" class="t" text-anchor="end">' + short(v).replace('₹', '') + '</text>'; }
    var step = Math.max(1, Math.round((n - 1) / 8)); for (k = 0; k < n; k += step) svg += '<text x="' + x(k) + '" y="' + (Hh - 10) + '" class="t" text-anchor="middle">Y' + k + '</text>';
    function path(arr) { return arr.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(''); }
    svg += '<path d="' + path(s.balNormal) + 'L' + x(n - 1).toFixed(1) + ' ' + y(0) + 'L' + x(0) + ' ' + y(0) + 'Z" class="ab"/>';
    svg += '<path d="' + path(s.balHalf) + 'L' + x(n - 1).toFixed(1) + ' ' + y(0) + 'L' + x(0) + ' ' + y(0) + 'Z" class="hb"/>';
    svg += '<path d="' + path(s.balNormal) + '" class="al"/><path d="' + path(s.balHalf) + '" class="hl"/>';
    $('chart').innerHTML = svg;
  }
  function buildTable() {
    var s = state, h = '<table><thead><tr><th>Year</th><th>Interest paid</th><th>Principal paid</th><th>Balance left</th><th>Balance, ' + s.half.years + ' yr plan</th></tr></thead><tbody>';
    s.base.yearly.forEach(function (r, i) { h += '<tr' + (r.year === s.half.years ? ' class="hl"' : '') + '><td>' + r.year + '</td><td>' + short(r.interest) + '</td><td>' + short(r.principal) + '</td><td>' + short(r.bal) + '</td><td>' + short(s.balHalf[r.year] || 0) + '</td></tr>'; });
    $('tbl').innerHTML = h + '</tbody></table>';
  }
  function renderInvest() {
    var v = state.invest, box = $('ivOut');
    if (!v) { box.hidden = true; return; } box.hidden = false;
    $('ivEff').textContent = pct(v.effRate); $('ivEffS').textContent = 'nominal ' + pct(state.rate) + ' minus tax breaks in the ' + Math.round(v.slab * 100) + '% slab';
    $('ivRet').textContent = pct(v.expRet, 0);
    $('ivSave').textContent = short(v.prepaySaved); $('ivSaveS').textContent = 'loan closes in ' + v.prepayYears + ' years instead of ' + state.years;
    $('ivCorp').textContent = short(v.investCorpus); $('ivCorpS').textContent = 'after LTCG, loan runs the full ' + state.years + ' years';
    var vd = $('ivVd'); vd.className = 'fr-verdict ' + (v.investWins ? 'ok iv-invest' : 'ok');
    vd.innerHTML = '<b>' + v.verdictTitle + '.</b> ' + v.verdictLines.join(' ');
    $('ivNote').textContent = 'Both paths spend exactly ' + short(state.emi + v.extra) + ' a month. Tax benefit counted: Section 24(b) interest up to ' + short(v.cap24) + (v.c80 ? ' and Section 80C principal up to ' + short(v.c80) : ', 80C assumed already used') + ' per year' + (v.co === 2 ? ', doubled for a co borrower' : '') + '. Freed up cash after the loan closes is invested at the same return.';
    // mini chart
    var W = 640, Hh = 220, L = 54, R = 12, T = 14, B = 30, n = v.x.length, max = Math.max.apply(null, v.investNet.concat(v.prepayNet)) * 1.06 || 1;
    var x = function (i) { return L + i / (n - 1) * (W - L - R); }, y = function (val) { return T + (1 - val / max) * (Hh - T - B); }, svg = '', k;
    for (k = 0; k <= 4; k++) { var vv = max * k / 4, yy = y(vv); svg += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + yy + '" y2="' + yy + '" class="g"/><text x="' + (L - 6) + '" y="' + (yy + 4) + '" class="t" text-anchor="end">' + short(vv).replace('₹', '') + '</text>'; }
    var step = Math.max(1, Math.round((n - 1) / 8)); for (k = 0; k < n; k += step) svg += '<text x="' + x(k) + '" y="' + (Hh - 10) + '" class="t" text-anchor="middle">' + v.x[k] + '</text>';
    function path(arr) { return arr.map(function (val, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(val).toFixed(1); }).join(''); }
    svg += '<path d="' + path(v.investNet) + '" class="al"/><path d="' + path(v.prepayNet) + '" class="hl"/>';
    $('ivChart').innerHTML = svg;
  }

  // ---------- share link ----------
  var FIELDS = ['amt', 'rate', 'tenure', 'target', 'extra', 'slab', 'expRet'];
  function saveLink() { try { var q = new URLSearchParams(); q.set('k', kind); FIELDS.forEach(function (f) { q.set(f, num($(f).value)); }); q.set('co', $('cobor').checked ? 1 : 0); q.set('c80', $('c80').checked ? 1 : 0); state.link = location.origin + location.pathname + '?' + q.toString(); } catch (e) { } }
  function loadLink() {
    try { var q = new URLSearchParams(location.search); if (!q.has('k')) return false; if (KINDS[q.get('k')]) kind = q.get('k'); FIELDS.forEach(function (f) { if (q.has(f)) $(f).value = f === 'amt' || f === 'extra' ? inr(num(q.get(f))) : q.get(f); }); if (q.has('co')) $('cobor').checked = q.get('co') === '1'; if (q.has('c80')) $('c80').checked = q.get('c80') === '1'; return true; } catch (e) { return false; }
  }
  function setKind(k, keep) {
    kind = k; var K = KINDS[k];
    document.querySelectorAll('.ln-tabs button').forEach(function (b) { b.classList.toggle('on', b.dataset.k === k); b.setAttribute('aria-selected', b.dataset.k === k ? 'true' : 'false'); });
    if (!keep) { $('amt').value = inr(K.P); $('rate').value = K.rate; $('tenure').value = K.years; $('target').value = Math.round(K.years / 2); }
    $('tenure').max = K.maxY; $('amt').setAttribute('data-max', K.max);
    document.querySelectorAll('.ln-kind').forEach(function (e) { e.textContent = K.label.toLowerCase(); });
    $('ivSec').classList.toggle('ln-dim', k !== 'home');
    $('ivKindNote').textContent = k === 'home' ? 'Section 24(b) and 80C benefits apply to home loans.' : 'No tax breaks on a ' + K.label.toLowerCase() + ' loan, so the comparison uses the full interest rate.';
    calc();
  }

  // ---------- events ----------
  document.querySelectorAll('.ln-tabs button').forEach(function (b) { b.addEventListener('click', function () { setKind(b.dataset.k); if (window.shTrack) shTrack('loan_kind', { label: b.dataset.k }); }); });
  $('lnForm').addEventListener('input', function (e) {
    if (e.target.id === 'tenure') { var ty = Math.round(num($('tenure').value) / 2) || 1; $('target').value = ty; }
    calc();
  });
  $('ivForm').addEventListener('input', calc);
  ['amt', 'extra'].forEach(function (id) { $(id).addEventListener('blur', function () { var v = num(this.value); this.value = v ? inr(v) : '0'; }); });
  $('tblBtn').addEventListener('click', function () { var t = $('tbl'); t.hidden = !t.hidden; this.textContent = t.hidden ? 'Show year by year table' : 'Hide the table'; });
  $('share').addEventListener('click', function () {
    var b = this, url = state.link || location.href;
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { b.textContent = 'Link copied'; }, function () { prompt('Copy this link', url); });
    setTimeout(function () { b.textContent = 'Copy link to my plan'; }, 2200);
  });
  // expose for the PDF engine (calc-reports.js reads window.__calc)
  Object.defineProperty(window, '__calc', { get: function () { var s = state; return { kind: 'loan', loanKind: s.kind, P: s.P, rate: s.rate, years: s.years, emi: s.emi, totalInterest: s.totalInterest, totalPaid: s.totalPaid, half: s.half, years_x: s.years_x, balNormal: s.balNormal, balHalf: s.balHalf, strategies: s.strategies, invest: s.invest }; }, configurable: true });
  var fromLink = loadLink();
  setKind(kind, fromLink);
  var out = $('lnOut'), mbar = $('mbar');
  if ('IntersectionObserver' in window && mbar) new IntersectionObserver(function (es) { es.forEach(function (x) { mbar.style.display = x.isIntersecting ? 'none' : ''; }); }, { threshold: .05 }).observe(out);
})();
