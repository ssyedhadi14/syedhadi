/* Created by: Claude
   Date: 2026-10-31
   Purpose: Salary growth calculator for syedcreates.com. Model from the 2026 Salary Tracker workbook.
   Owner: Syed Hadi
   Everything runs in the browser. The only network call is the optional "email me the PDF" request. */
(function () {
  'use strict';
  var $ = function (i) { return document.getElementById(i); };
  var NEEDS = ['rent', 'emi', 'food', 'fuel', 'bills', 'fees', 'family', 'needx'];
  var WANTS = ['clothes', 'eatout', 'gadgets', 'travel', 'wantx'];
  var LABELS = { rent: 'Rent or home EMI', emi: 'Essential EMIs', food: 'Groceries and food', fuel: 'Fuel and commute', bills: 'Bills', fees: 'Fees', family: 'Money sent home', needx: 'Other needs', clothes: 'Clothes and shopping', eatout: 'Eating out', gadgets: 'Gadget EMIs', travel: 'Vacations', wantx: 'Other wants' };
  var YEAR0 = new Date().getFullYear();

  function num(v) { return parseFloat(String(v).replace(/[^0-9.]/g, '')) || 0; }
  function inr(n) { n = Math.round(n); return n.toLocaleString('en-IN'); }
  function short(n) {
    var a = Math.abs(n), s = n < 0 ? '-' : '';
    if (a >= 1e7) return s + '₹' + (a / 1e7).toFixed(a >= 1e9 ? 0 : 2) + ' Cr';
    if (a >= 1e5) return s + '₹' + (a / 1e5).toFixed(1) + ' L';
    return s + '₹' + inr(a);
  }
  function words(id) { var el = $(id), w = $(id + 'W'); if (!el || !w) return; var v = num(el.value); w.textContent = v ? short(v) + ' per month' : ''; }
  function pct(x) { return (x * 100).toFixed(0) + '%'; }

  // ---------- inputs ----------
  function readItems(keys) {
    return keys.map(function (k) { return { k: k, v: num($(k).value), g: num($(k + 'G').value) / 100 }; });
  }
  function readInputs() {
    var age = Math.max(18, Math.min(65, Math.round(num($('age').value) || 27)));
    var hz = Math.max(10, Math.min(60, Math.round(num($('hz').value) || 45)));
    var tgt = Math.round(num($('tgt').value) || age + 10);
    tgt = Math.max(age + 1, Math.min(age + hz, tgt));
    return {
      age: age, sal: num($('sal').value), inc: num($('inc').value) / 100, tgt: tgt, hz: hz,
      needs: readItems(NEEDS), wants: readItems(WANTS),
      splitMode: $('splitMode').value, ppfPct: num($('ppfPct').value) / 100,
      rp: num($('rp').value) / 100, re: num($('re').value) / 100, ltcg: num($('ltcg').value) / 100,
      inf: num($('inf').value) / 100, stopAge: Math.round(num($('stopAge').value) || 60)
    };
  }

  // ---------- model ----------
  function project(I) {
    var rows = [];
    for (var y = 0; y <= I.hz; y++) {
      var a = I.age + y;
      var income = I.sal * 12 * Math.pow(1 + I.inc, y);
      var needs = 0, wants = 0;
      I.needs.forEach(function (it) { needs += it.v * 12 * Math.pow(1 + it.g, y); });
      I.wants.forEach(function (it) { wants += it.v * 12 * Math.pow(1 + it.g, y); });
      var surplus = a <= I.stopAge ? Math.max(0, income - needs - wants) : 0;
      var share = I.splitMode === 'age' ? Math.min(1, a / 100) : Math.min(1, Math.max(0, I.ppfPct));
      var ppf = surplus * share, eq = surplus - ppf;
      rows.push({ y: y, age: a, year: YEAR0 + y, income: income, needs: needs, wants: wants, surplus: surplus, ppf: ppf, eq: eq });
    }
    // corpus at the end of each year y, counting every contribution made in years <= y
    var corp = [];
    for (var t = 0; t <= I.hz; t++) {
      var P = 0, E = 0, put = 0;
      for (var i = 0; i <= t; i++) {
        var n = t - i, r = rows[i];
        P += r.ppf * Math.pow(1 + I.rp, n);
        var ev = r.eq * Math.pow(1 + I.re, n);
        E += ev - Math.max(0, ev - r.eq) * I.ltcg;
        put += r.ppf + r.eq;
      }
      var tot = P + E, real = tot / Math.pow(1 + I.inf, t);
      corp.push({ ppf: P, eq: E, total: tot, real: real, put: put });
      rows[t].cPpf = P; rows[t].cEq = E; rows[t].corpus = tot; rows[t].real = real; rows[t].put = put;
    }
    return rows;
  }
  function firstAge(rows, key, limit) {
    for (var i = 0; i < rows.length; i++) if (rows[i][key] >= limit) return rows[i];
    return null;
  }

  // ---------- render ----------
  var state = { chart: 'corpus', rows: [], I: null };
  function render() {
    var I = readInputs(); state.I = I;
    var rows = project(I); state.rows = rows;
    var t = I.tgt - I.age, R = rows[t], R0 = rows[0];
    $('needsT').textContent = short(I.needs.reduce(function (s, x) { return s + x.v; }, 0)) + ' / mo';
    $('wantsT').textContent = short(I.wants.reduce(function (s, x) { return s + x.v; }, 0)) + ' / mo';
    $('kTgt').textContent = I.tgt; $('kTgt2').textContent = I.tgt; $('mAge').textContent = I.tgt;
    $('tgtR').min = I.age + 1; $('tgtR').max = I.age + I.hz; $('tgtR').value = I.tgt;
    $('tgtLbl').textContent = 'Age ' + I.tgt + ', year ' + R.year;
    $('corpN').textContent = short(R.corpus); $('mN').textContent = short(R.corpus);
    $('corpS').textContent = 'worth ' + short(R.real) + ' in today’s money';
    var surplusM = R0.surplus / 12, rate = R0.income ? R0.surplus / R0.income : 0;
    $('invNow').textContent = short(surplusM);
    $('invPct').textContent = pct(rate) + ' of salary, ' + short(R0.ppf / 12) + ' PPF + ' + short(R0.eq / 12) + ' equity';
    $('salT').textContent = short(R.income / 12);
    $('salTS').textContent = 'worth ' + short(R.income / 12 / Math.pow(1 + I.inf, t)) + ' today';
    $('putIn').textContent = short(R.put);
    $('gain').textContent = short(R.corpus - R.put);
    $('gainS').textContent = R.put ? ((R.corpus / R.put).toFixed(1) + 'x your money') : '';
    // verdict
    var vd = $('vd'), msg;
    if (R0.surplus <= 0) {
      vd.className = 'fr-verdict no';
      msg = 'Your spends are higher than your salary today, so nothing is being invested. Trim the wants or raise the income line to see a corpus build.';
    } else {
      vd.className = 'fr-verdict ok';
      var cr = firstAge(rows, 'corpus', 1e7);
      msg = 'Investing ' + short(surplusM) + ' a month today and growing it with every increment, you reach <b>' + short(R.corpus) + '</b> at ' + I.tgt + ' (' + R.year + '). ';
      msg += cr ? 'You become a crorepati at <b>' + cr.age + '</b>, in ' + cr.year + '.' : 'A crore stays out of reach in this window. Raise the surplus or the increment.';
      if (rate < 0.2) msg += ' You invest ' + pct(rate) + ' of your salary. Getting that to 30% changes everything downstream.';
    }
    vd.innerHTML = msg;
    // milestones
    var m1 = firstAge(rows, 'corpus', 1e7), m5 = firstAge(rows, 'corpus', 5e7), m10 = firstAge(rows, 'corpus', 1e8), r1 = firstAge(rows, 'real', 1e7);
    function ms(label, r, sub) { return '<div><b>' + (r ? r.age : '—') + '</b><span>' + label + '<br>' + (r ? 'in ' + r.year : sub) + '</span></div>'; }
    $('miles').innerHTML = ms('First crore (age)', m1, 'not in range') + ms('5 crore (age)', m5, 'not in range') + ms('10 crore (age)', m10, 'not in range') +
      ms('1 crore in today’s money', r1, 'not in range') +
      '<div><b>' + short(rows[rows.length - 1].income / 12) + '</b><span>Salary per month at ' + rows[rows.length - 1].age + '<br>in ' + rows[rows.length - 1].year + '</span></div>' +
      '<div><b>' + short(rows[rows.length - 1].corpus) + '</b><span>Corpus at ' + rows[rows.length - 1].age + '<br>' + short(rows[rows.length - 1].real) + ' today’s money</span></div>';
    drawChart();
    if (!$('tbl').hidden) buildTable();
    try { history.replaceState(null, '', '#' + encode(I)); } catch (e) { }
  }

  // ---------- charts (inline SVG) ----------
  var NS = 'http://www.w3.org/2000/svg';
  function el(n, a, txt) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }
  function drawChart() {
    var svg = $('chart'), rows = state.rows, I = state.I; svg.innerHTML = '';
    var W = 640, H = 280, L = 56, Rm = 14, T = 16, B = 34, w = W - L - Rm, h = H - T - B, n = rows.length;
    var x = function (i) { return L + (n > 1 ? i / (n - 1) : 0) * w; };
    var legend = $('legend');
    if (state.chart === 'flow') {
      var max = Math.max.apply(null, rows.map(function (r) { return r.income; })) * 1.05 || 1;
      var ys = function (v) { return T + h - v / max * h; };
      gridLines(svg, max, ys, L, W - Rm);
      var bw = Math.max(2, w / n - 2);
      rows.forEach(function (r, i) {
        var x0 = x(i) - bw / 2, base = T + h;
        var hn = r.needs / max * h, hw = r.wants / max * h, hs = r.surplus / max * h;
        svg.appendChild(el('rect', { x: x0, y: base - hn, width: bw, height: hn, fill: '#f59e0b', rx: 1 }));
        svg.appendChild(el('rect', { x: x0, y: base - hn - hw, width: bw, height: hw, fill: '#fb7185', rx: 1 }));
        svg.appendChild(el('rect', { x: x0, y: base - hn - hw - hs, width: bw, height: hs, fill: '#5b3df5', rx: 1 }));
        var over = Math.max(0, r.needs + r.wants - r.income) / max * h;
        if (over) svg.appendChild(el('rect', { x: x0, y: base - hn - hw, width: bw, height: over, fill: 'rgba(220,38,38,.35)' }));
      });
      var p = rows.map(function (r, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + ys(r.income).toFixed(1); }).join(' ');
      svg.appendChild(el('path', { d: p, 'class': 'ab', fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2 }));
      legend.innerHTML = '<span><i style="background:#5b3df5"></i>Invested</span><span><i style="background:#fb7185"></i>Wants</span><span><i style="background:#f59e0b"></i>Needs</span><span><i style="background:var(--ink)"></i>Yearly in hand income</span>';
    } else {
      var real = state.chart === 'real';
      var tot = rows.map(function (r) { return real ? r.real : r.corpus; });
      var max2 = Math.max.apply(null, tot) * 1.05 || 1;
      var ys2 = function (v) { return T + h - v / max2 * h; };
      gridLines(svg, max2, ys2, L, W - Rm);
      var inf = function (i) { return real ? Math.pow(1 + I.inf, i) : 1; };
      var top = rows.map(function (r, i) { return ys2((r.cPpf + r.cEq) / inf(i)); });
      var mid = rows.map(function (r, i) { return ys2(r.cPpf / inf(i)); });
      var area = function (upper, lower) {
        var d = upper.map(function (yv, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + yv.toFixed(1); }).join(' ');
        for (var i = n - 1; i >= 0; i--) d += ' L' + x(i).toFixed(1) + ' ' + lower[i].toFixed(1);
        return d + ' Z';
      };
      var base = rows.map(function () { return T + h; });
      svg.appendChild(el('path', { d: area(top, mid), fill: 'rgba(91,61,245,.55)' }));
      svg.appendChild(el('path', { d: area(mid, base), fill: 'rgba(16,185,129,.55)' }));
      svg.appendChild(el('path', { d: top.map(function (yv, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + yv.toFixed(1); }).join(' '), 'class': 'ab' }));
      // crore lines
      [1e7, 5e7, 1e8].forEach(function (c) { if (c < max2) { svg.appendChild(el('line', { x1: L, x2: W - Rm, y1: ys2(c), y2: ys2(c), 'class': 'rl' })); svg.appendChild(el('text', { x: W - Rm - 4, y: ys2(c) - 4, 'class': 't', 'text-anchor': 'end' }, short(c))); } });
      // target marker
      var ti = I.tgt - I.age;
      svg.appendChild(el('line', { x1: x(ti), x2: x(ti), y1: T, y2: T + h, stroke: 'var(--accent)', 'stroke-dasharray': '3 3' }));
      svg.appendChild(el('circle', { cx: x(ti), cy: top[ti], r: 5, fill: 'var(--accent)', stroke: '#fff', 'stroke-width': 2 }));
      svg.appendChild(el('text', { x: Math.min(x(ti) + 6, W - 90), y: Math.max(T + 12, top[ti] - 10), 'class': 't', 'font-weight': 700 }, 'Age ' + I.tgt + ': ' + short(tot[ti])));
      legend.innerHTML = '<span><i style="background:rgba(91,61,245,.8)"></i>Equity (after LTCG)</span><span><i style="background:rgba(16,185,129,.8)"></i>PPF</span>' + (real ? '<span>All values in today’s rupees</span>' : '');
    }
    // x axis labels every ~9 years
    var step = Math.max(1, Math.round(n / 7));
    rows.forEach(function (r, i) { if (i % step === 0 || i === n - 1) svg.appendChild(el('text', { x: x(i), y: H - 12, 'class': 't', 'text-anchor': 'middle' }, 'Age ' + r.age)); });
  }
  function gridLines(svg, max, ys, L, R) {
    for (var k = 0; k <= 4; k++) { var v = max * k / 4; svg.appendChild(el('line', { x1: L, x2: R, y1: ys(v), y2: ys(v), 'class': 'g' })); svg.appendChild(el('text', { x: L - 6, y: ys(v) + 4, 'class': 't', 'text-anchor': 'end' }, short(v).replace('₹', ''))); }
  }

  function buildTable() {
    var I = state.I, rows = state.rows, html = '<table><thead><tr><th>Age</th><th>Year</th><th>In hand / yr</th><th>Needs</th><th>Wants</th><th>Invested</th><th>Corpus</th><th>Today’s money</th></tr></thead><tbody>';
    rows.forEach(function (r) {
      html += '<tr' + (r.age === I.tgt ? ' class="hl"' : '') + '><td>' + r.age + '</td><td>' + r.year + '</td><td>' + short(r.income) + '</td><td>' + short(r.needs) + '</td><td>' + short(r.wants) + '</td><td>' + short(r.surplus) + '</td><td>' + short(r.corpus) + '</td><td>' + short(r.real) + '</td></tr>';
    });
    $('tbl').innerHTML = html + '</tbody></table>';
  }

  // ---------- share link ----------
  function encode(I) {
    var o = { a: I.age, s: I.sal, i: I.inc * 100, t: I.tgt, h: I.hz, m: I.splitMode, p: I.ppfPct * 100, rp: I.rp * 100, re: I.re * 100, l: I.ltcg * 100, f: I.inf * 100, st: I.stopAge, n: {}, w: {} };
    I.needs.forEach(function (x) { o.n[x.k] = [x.v, x.g * 100]; }); I.wants.forEach(function (x) { o.w[x.k] = [x.v, x.g * 100]; });
    return 'p=' + encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(o)))));
  }
  function decode() {
    var m = location.hash.match(/p=([^&]+)/); if (!m) return;
    try {
      var o = JSON.parse(decodeURIComponent(escape(atob(decodeURIComponent(m[1])))));
      $('age').value = o.a; $('sal').value = inr(o.s); $('inc').value = o.i; $('tgt').value = o.t; $('hz').value = o.h; $('splitMode').value = o.m; $('ppfPct').value = o.p; $('rp').value = o.rp; $('re').value = o.re; $('ltcg').value = o.l; $('inf').value = o.f; $('stopAge').value = o.st;
      Object.keys(o.n || {}).forEach(function (k) { if ($(k)) { $(k).value = inr(o.n[k][0]); $(k + 'G').value = o.n[k][1]; } });
      Object.keys(o.w || {}).forEach(function (k) { if ($(k)) { $(k).value = inr(o.w[k][0]); $(k + 'G').value = o.w[k][1]; } });
    } catch (e) { }
  }

  // ---------- PDF (shared high fidelity report engine, /assets/report-pdf.js) ----------
  var pdfLibLoading = null;
  function loadPdfLib() {
    if (pdfLibLoading) return pdfLibLoading;
    pdfLibLoading = (window.SHReport ? Promise.resolve() : new Promise(function (res, rej) {
      var s = document.createElement('script'); s.src = '/assets/report-pdf.js?v=20261031s';
      s.onload = function () { res(); }; s.onerror = function () { rej(new Error('pdf engine')); }; document.head.appendChild(s);
    })).then(function () { return window.SHReport.ready(); });
    pdfLibLoading.catch(function () { pdfLibLoading = null; });
    return pdfLibLoading;
  }
  function P(x) { return (x * 100).toFixed(x * 100 % 1 ? 1 : 0) + '%'; }
  function buildPdf(name) {
    var F = window.SHReport.fmtINR, Cc = window.SHReport.C;
    var I = state.I, rows = state.rows, t = I.tgt - I.age, R = rows[t], R0 = rows[0], last = rows[rows.length - 1];
    var surplusM = R0.surplus / 12, rate = R0.income ? R0.surplus / R0.income : 0;
    var cr = firstAge(rows, 'corpus', 1e7), cr5 = firstAge(rows, 'corpus', 5e7), cr10 = firstAge(rows, 'corpus', 1e8);
    var needsM = I.needs.reduce(function (s, x) { return s + x.v; }, 0), wantsM = I.wants.reduce(function (s, x) { return s + x.v; }, 0);
    var today = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    var who = name ? name.split(' ')[0] : '';
    // milestones table (crore marks)
    var marks = [[1e7, 'First crore'], [2e7, '2 crore'], [5e7, '5 crore'], [1e8, '10 crore'], [2.5e8, '25 crore'], [5e8, '50 crore'], [1e9, '100 crore']];
    var mrows = []; marks.forEach(function (m) { var r = firstAge(rows, 'corpus', m[0]); if (r) mrows.push([m[1], 'Age ' + r.age, String(r.year), F(r.real), F(r.put), F(r.income / 12)]); });
    // spend lines for the inputs block
    var kv = [['Age today', String(I.age)], ['In hand salary', F(I.sal) + ' / month'], ['Annual increment', P(I.inc)], ['Needs today', F(needsM) + ' / month'], ['Wants today', F(wantsM) + ' / month'],
      ['Invested today', F(surplusM) + ' / month (' + P(rate) + ')'], ['Split', I.splitMode === 'age' ? 'PPF share = your age, rest equity' : 'PPF ' + P(I.ppfPct) + ', equity ' + P(1 - I.ppfPct)],
      ['PPF return', P(I.rp) + ' tax free'], ['Equity return', P(I.re) + ', LTCG ' + P(I.ltcg)], ['Inflation', P(I.inf)], ['Investing stops at', 'Age ' + I.stopAge], ['Horizon', I.hz + ' years, to age ' + (I.age + I.hz)]];
    var tableRows = rows.map(function (r) { return [String(r.age), String(r.year), F(r.income), F(r.needs), F(r.wants), F(r.surplus), F(r.corpus), F(r.real)]; });
    var verdict, tone;
    if (R0.surplus <= 0) { tone = 'rose'; verdict = ['Your spends are higher than your salary today, so nothing is being invested yet. Trim the wants or raise the income line and the corpus starts to build.']; }
    else {
      tone = 'green';
      verdict = ['Investing ' + F(surplusM) + ' a month today and growing it with every increment, you reach ' + F(R.corpus) + ' at age ' + I.tgt + ' (' + R.year + '). That is ' + F(R.real) + ' in today’s money.',
        cr ? 'You become a crorepati at age ' + cr.age + ', in ' + cr.year + '.' + (cr10 ? ' Ten crore arrives at ' + cr10.age + '.' : cr5 ? ' Five crore arrives at ' + cr5.age + '.' : '') : 'A crore stays out of reach in this window. Raise the surplus or the increment.'];
      if (rate < 0.2) verdict.push('You invest ' + P(rate) + ' of your salary. Getting that to 30% changes everything downstream, because every increment compounds on a bigger base.');
      else if (rate >= 0.3) verdict.push('You already invest ' + P(rate) + ' of your salary, which is the single biggest lever in this model. Protect that rate through every increment.');
    }
    var spec = {
      kicker: 'SYEDCREATES.COM  /  SALARY GROWTH REPORT', url: 'syedcreates.com/salary-calculator', docTitle: 'Salary growth report, age ' + I.age + ' to ' + (I.age + I.hz),
      title: (who ? who + ', here is' : 'Here is') + ' where your salary goes over the next ' + I.hz + ' years.',
      subtitle: 'A year by year view of income, spends, what gets invested and the corpus it builds, from age ' + I.age + ' to ' + (I.age + I.hz) + '. Prepared ' + today + '.',
      meta: [['Age', String(I.age)], ['In hand', F(I.sal) + ' / mo'], ['Increment', P(I.inc) + ' a year'], ['Target age', String(I.tgt)], ['Horizon', I.hz + ' years']],
      footer: 'Planning tool, not investment advice. Returns are assumptions, not predictions. Built by Syed Hadi, syedcreates.com/salary-calculator',
      blocks: [
        { type: 'kpis', items: [
          { label: 'Corpus at age ' + I.tgt + ' (' + R.year + ')', value: F(R.corpus), sub: 'worth ' + F(R.real) + ' in today’s money', hero: true },
          { label: 'You invest per month now', value: F(surplusM), sub: P(rate) + ' of salary. PPF ' + F(R0.ppf / 12) + ' and equity ' + F(R0.eq / 12) + ' every month.' },
          { label: 'First crore', value: cr ? 'Age ' + cr.age : 'Not in range', sub: cr ? 'in ' + cr.year + ', with ' + F(cr.put) + ' put in by then' : 'Raise the surplus or the increment to get there', color: Cc.green },
          { label: 'Money put in by ' + I.tgt, value: F(R.put), sub: F(R.corpus - R.put) + ' of growth on top, ' + (R.put ? (R.corpus / R.put).toFixed(1) + 'x your money' : '') }
        ] },
        { type: 'callout', title: 'The verdict', lines: verdict, tone: tone },
        { type: 'h2', title: 'How the corpus builds', sub: 'PPF and equity after long term capital gains tax, nominal rupees. The dashed line is the age you asked about.' },
        { type: 'area', xLabels: rows.map(function (r) { return r.age; }), height: 175,
          series: [
            { name: 'Total corpus (equity after LTCG)', color: Cc.accent, values: rows.map(function (r) { return r.corpus; }), opacity: 0.85 },
            { name: 'PPF', color: Cc.green, values: rows.map(function (r) { return r.cPpf; }), opacity: 0.95 },
            { name: 'In today’s money', color: Cc.ink, values: rows.map(function (r) { return r.real; }), fill: false, dash: true }
          ],
          mark: { index: t, value: R.corpus, label: 'Age ' + I.tgt + ': ' + F(R.corpus) }, note: 'x axis: your age' },
        { type: 'h2', title: 'Income versus spends', sub: 'Why the surplus widens: salary compounds with your increment while most spends grow slower.' },
        { type: 'area', xLabels: rows.map(function (r) { return r.age; }), height: 120,
          series: [
            { name: 'In hand income per year', color: Cc.accent2, values: rows.map(function (r) { return r.income; }), opacity: 0.35 },
            { name: 'Needs + wants per year', color: Cc.amber, values: rows.map(function (r) { return r.needs + r.wants; }), opacity: 0.75 }
          ], note: 'nominal rupees per year' },
        { type: 'page' },
        { type: 'h2', title: 'Milestones', sub: 'When each corpus mark arrives, what it is worth in today’s money and how much of it you actually put in.' },
        mrows.length ? { type: 'table', head: ['Milestone', 'Age', 'Year', 'Today’s money', 'Put in by then', 'Salary / month then'], rows: mrows, rowHeight: 16, fontSize: 8.4 }
                     : { type: 'para', text: 'No crore milestone lands inside this horizon. Try a higher surplus, a higher increment or a longer horizon.' },
        { type: 'h2', title: 'What this plan assumes', sub: 'Every figure here is an input on the page. Change one and the report updates.' },
        { type: 'kv', rows: kv, cols: 2 },
        { type: 'bullets', items: [
          ['Spends grow at their own rate.', 'Rent ' + P(I.needs[0].g) + ', essential EMIs ' + P(I.needs[1].g) + ', groceries ' + P(I.needs[2].g) + ' a year, and so on for each line. Needs ' + F(needsM) + ' and wants ' + F(wantsM) + ' a month today.'],
          ['Surplus is invested the same month.', (I.splitMode === 'age' ? 'The PPF share equals your age in percent each year, the rest goes to equity.' : 'PPF takes ' + P(I.ppfPct) + ' and equity the rest.') + ' Contributions stop at age ' + I.stopAge + ', the corpus keeps compounding.'],
          ['Tax is applied on equity gains.', 'Equity growth is taxed at ' + P(I.ltcg) + ' as long term capital gains at the end of each year. PPF is tax free.'],
          ['Today’s money uses ' + P(I.inf) + ' inflation.', 'That is the number to look at when deciding whether the corpus is enough.']
        ] },
        { type: 'h2', title: 'Three moves that change the outcome most', sub: 'In order of impact in this model.' },
        { type: 'steps', items: [
          ['Protect the investing rate through every increment', 'Lifestyle creep is the silent killer. If the increment is 10%, let spends grow 5% and investing grows faster than salary.'],
          ['Negotiate the increment, not just the salary', 'In this model one extra percentage point of annual increment is worth more than a one time bonus, because it compounds for ' + I.hz + ' years.'],
          ['Keep equity as the engine', 'PPF is the safety net. The corpus at ' + I.tgt + ' is ' + Math.round(R.cEq / Math.max(1, R.corpus) * 100) + '% equity in this plan. Stay invested through drawdowns.']
        ] },
        { type: 'page' },
        { type: 'h2', title: 'Year by year', sub: 'In hand income per year, spends, what gets invested and the corpus it builds. The highlighted row is age ' + I.tgt + '. L = lakh, Cr = crore.' },
        { type: 'table', head: ['Age', 'Year', 'In hand / yr', 'Needs', 'Wants', 'Invested', 'Corpus', 'Today’s money'], rows: tableRows, highlight: t, rowHeight: 13.6, fontSize: 7.8 },
        { type: 'signoff' }
      ]
    };
    return window.SHReport.build(spec);
  }
  function pdfName() { return 'salary-growth-report-' + state.I.age + '-to-' + (state.I.age + state.I.hz) + '.pdf'; }

  // ---------- events ----------
  var form = $('scForm');
  form.addEventListener('input', function (e) {
    if (e.target.id === 'splitMode') $('ppfPct').disabled = e.target.value !== 'fixed';
    render();
  });
  form.addEventListener('change', render);
  document.querySelectorAll('input[data-money]').forEach(function (el) {
    words(el.id);
    el.addEventListener('input', function () { words(el.id); });
    el.addEventListener('blur', function () { var v = num(el.value); el.value = v ? inr(v) : '0'; words(el.id); });
  });
  $('tgtR').addEventListener('input', function () { $('tgt').value = this.value; render(); });
  document.querySelectorAll('.sc-tabs button').forEach(function (b) {
    b.addEventListener('click', function () { document.querySelectorAll('.sc-tabs button').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); state.chart = b.dataset.ch; drawChart(); });
  });
  $('tblBtn').addEventListener('click', function () { var t = $('tbl'); t.hidden = !t.hidden; this.textContent = t.hidden ? 'Show year by year table' : 'Hide the table'; if (!t.hidden) buildTable(); });
  $('share').addEventListener('click', function () {
    var b = this, url = location.origin + location.pathname + '#' + encode(state.I);
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { b.textContent = 'Link copied'; }, function () { prompt('Copy this link', url); });
    setTimeout(function () { b.textContent = 'Copy link to my plan'; }, 2200);
  });
  $('pdfBtn').addEventListener('click', function () {
    var b = this, old = b.textContent; b.textContent = 'Building your PDF...'; b.disabled = true;
    loadPdfLib().then(function () { buildPdf($('mName').value.trim()).save(pdfName()); if (window.shTrack) shTrack('salary_pdf_download'); })
      .catch(function () { var m = $('mMsg'); m.textContent = 'The PDF library could not load. Reload the page and try again.'; m.className = 'msg err'; })
      .then(function () { b.textContent = old; b.disabled = false; });
  });
  $('mailForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var email = $('mEmail').value.trim(), name = $('mName').value.trim(), msg = $('mMsg'), btn = $('mailBtn');
    msg.className = 'msg';
    if ($('mHoney').value) return;
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { msg.textContent = 'Enter a valid email address.'; msg.className = 'msg err'; return; }
    if (!$('mConsent').checked) { msg.textContent = 'Tick the box so I can send the report.'; msg.className = 'msg err'; return; }
    btn.disabled = true; btn.textContent = 'Sending...'; msg.textContent = 'Building the PDF and sending it to ' + email + '...';
    var I = state.I, R = state.rows[I.tgt - I.age];
    loadPdfLib().then(function () {
      var doc = buildPdf(name);
      var b64 = doc.output('datauristring').split(',')[1];
      return fetch('/.netlify/functions/salary-report', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, name: name, pdf: b64, filename: pdfName(), summary: { age: I.age, target: I.tgt, corpus: short(R.corpus), real: short(R.real), investNow: short(state.rows[0].surplus / 12), link: location.origin + location.pathname + '#' + encode(I) } })
      }).then(function (r) { return r.json().catch(function () { return { ok: false, status: r.status }; }).then(function (j) { j.status = r.status; return j; }); })
        .then(function (j) {
          if (j.ok) { msg.textContent = 'Sent. Check ' + email + ' in a minute (and the promotions tab).'; msg.className = 'msg ok'; if (window.shTrack) shTrack('salary_report_email'); }
          else { doc.save(pdfName()); msg.textContent = (j.error ? j.error + ' ' : 'Email is not available right now. ') + 'The PDF downloaded to your device instead.'; msg.className = 'msg err'; }
        }, function () { doc.save(pdfName()); msg.textContent = 'Email is not available right now, so the PDF downloaded to your device instead.'; msg.className = 'msg err'; });
    }).catch(function (err) {
      msg.textContent = 'Could not build the report: ' + (err && err.message ? err.message : 'unknown error'); msg.className = 'msg err';
    }).then(function () { btn.disabled = false; btn.textContent = 'Send it'; });
  });

  // mobile result bar visibility
  var out = $('scOut'), mbar = $('mbar');
  if ('IntersectionObserver' in window && mbar) {
    new IntersectionObserver(function (es) { es.forEach(function (x) { mbar.style.display = x.isIntersecting ? 'none' : ''; }); }, { threshold: .05 }).observe(out);
  }
  decode();
  $('ppfPct').disabled = $('splitMode').value !== 'fixed';
  render();
})();
