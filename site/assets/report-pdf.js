/* Created by: Claude
   Date: 2026-10-31
   Purpose: Shared high fidelity A4 PDF report engine for every syedcreates.com calculator.
            Vector output via jsPDF with the site's own fonts embedded (Bricolage Grotesque, Inter, JetBrains Mono).
            Every block measures its text before drawing, so nothing overlaps at any input length.
   Owner: Syed Hadi
   Usage: SHReport.ready().then(function(){ var doc = SHReport.build(spec); doc.save('x.pdf'); })  */
(function () {
  'use strict';
  var W = 595.28, H = 841.89, M = 46, FOOT = 40;
  var C = {
    ink: [13, 11, 26], ink2: [74, 71, 96], ink3: [124, 121, 146], line: [228, 226, 238], faint: [247, 246, 252],
    accent: [91, 61, 245], accent2: [124, 92, 255], soft: [239, 235, 255], navy: [17, 12, 46], navy2: [34, 24, 90],
    white: [255, 255, 255], green: [16, 185, 129], greenSoft: [220, 247, 236], amber: [245, 158, 11], amberSoft: [255, 243, 219],
    rose: [244, 63, 94], roseSoft: [255, 228, 234], sky: [14, 165, 233], lav: [205, 196, 255]
  };
  var FONTS = [
    ['Bricolage-ExtraBold.ttf', 'Bricolage', 'extrabold'],
    ['Bricolage-Bold.ttf', 'Bricolage', 'bold'],
    ['Inter-Regular.ttf', 'Inter', 'normal'],
    ['Inter-Medium.ttf', 'Inter', 'medium'],
    ['Inter-SemiBold.ttf', 'Inter', 'bold'],
    ['JetBrainsMono-Medium.ttf', 'Mono', 'normal']
  ];
  var VER = '20261031t', libP = null, fontData = null;

  function loadScript(src) {
    return new Promise(function (res, rej) { var s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = function () { rej(new Error('Could not load ' + src)); }; document.head.appendChild(s); });
  }
  function b64(buf) { var u = new Uint8Array(buf), s = '', CH = 0x8000; for (var i = 0; i < u.length; i += CH) s += String.fromCharCode.apply(null, u.subarray(i, i + CH)); return btoa(s); }
  function ready() {
    if (libP) return libP;
    libP = Promise.all([
      (window.jspdf && window.jspdf.jsPDF) ? Promise.resolve() : loadScript('/assets/jspdf.umd.min.js?v=252'),
      Promise.all(FONTS.map(function (f) { return fetch('/assets/fonts/' + f[0] + '?v=' + VER).then(function (r) { if (!r.ok) throw new Error('font ' + f[0]); return r.arrayBuffer(); }).then(b64); }))
    ]).then(function (r) { fontData = r[1]; });
    libP.catch(function () { libP = null; });
    return libP;
  }

  // ---------- small helpers ----------
  function rgb(doc, fn, c) { doc[fn](c[0], c[1], c[2]); }
  function fmtINR(n, opts) {
    opts = opts || {}; var a = Math.abs(n), s = n < 0 ? '-' : '', sym = opts.plain ? '' : '₹';
    if (a >= 1e7) return s + sym + (a / 1e7).toFixed(a >= 1e9 ? 0 : (a >= 1e8 ? 1 : 2)) + ' Cr';
    if (a >= 1e5) return s + sym + (a / 1e5).toFixed(a >= 1e6 ? 1 : 2).replace(/\.00$/, '') + ' L';
    return s + sym + Math.round(a).toLocaleString('en-IN');
  }
  // returns {max, ticks[]} with 4 to 6 round steps (1, 2, 2.5, 5 x 10^k)
  function niceTicks(v) {
    if (!(v > 0)) return { max: 1, ticks: [0, 0.25, 0.5, 0.75, 1] };
    var raw = v / 4.5, p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / p;
    var step = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
    var max = Math.ceil(v / step) * step, ticks = []; for (var t = 0; t <= max + step / 2; t += step) ticks.push(t);
    return { max: max, ticks: ticks };
  }

  function Engine(doc, spec) {
    this.doc = doc; this.spec = spec; this.y = M; this.page = 1;
    this.footText = spec.footer || 'Planning tool, not financial advice. Figures follow the assumptions on the page.';
    this.kicker = spec.kicker || 'SYEDCREATES.COM';
  }
  var P = Engine.prototype;
  P.font = function (fam, sty, size, col) { this.doc.setFont(fam, sty); this.doc.setFontSize(size); if (col) rgb(this.doc, 'setTextColor', col); return this; };
  P.tw = function (t) { return this.doc.getTextWidth(String(t)); };
  P.wrap = function (t, w) { return this.doc.splitTextToSize(String(t), w); };
  P.fitSize = function (text, fam, sty, size, maxW, min) {
    min = min || 9; this.doc.setFont(fam, sty);
    for (var s = size; s >= min; s -= 0.5) { this.doc.setFontSize(s); if (this.tw(text) <= maxW) return s; }
    return min;
  };
  P.need = function (h) { if (this.y + h > H - FOOT - 14) this.newPage(); };
  P.newPage = function () {
    this.doc.addPage(); this.page++; this.y = M + 14;
    // running head
    this.font('Mono', 'normal', 7, C.ink3); this.doc.text(this.kicker, M, M - 10);
    var t = this.spec.title ? String(this.spec.title).replace(/\s+/g, ' ') : '';
    if (t) { this.font('Inter', 'medium', 7.5, C.ink3); var w = this.wrap(t, 300)[0]; this.doc.text(w, W - M, M - 10, { align: 'right' }); }
    rgb(this.doc, 'setDrawColor', C.line); this.doc.setLineWidth(0.5); this.doc.line(M, M - 2, W - M, M - 2);
  };
  P.footers = function () {
    var n = this.doc.getNumberOfPages();
    for (var i = 1; i <= n; i++) {
      this.doc.setPage(i);
      rgb(this.doc, 'setDrawColor', C.line); this.doc.setLineWidth(0.5); this.doc.line(M, H - FOOT, W - M, H - FOOT);
      this.font('Inter', 'normal', 7.2, C.ink3);
      var lines = this.wrap(this.footText, W - 2 * M - 70); this.doc.text(lines[0], M, H - FOOT + 13);
      if (lines[1]) this.doc.text(lines[1], M, H - FOOT + 23);
      this.font('Mono', 'normal', 7.2, C.ink3); this.doc.text('Page ' + i + ' of ' + n, W - M, H - FOOT + 13, { align: 'right' });
    }
  };

  // ---------- cover band ----------
  P.cover = function () {
    var d = this.doc, s = this.spec;
    // band height depends on the wrapped title
    this.font('Bricolage', 'extrabold', 27);
    var titleLines = this.wrap(s.title, W - 2 * M - 10).slice(0, 3);
    this.font('Inter', 'normal', 10.5);
    var subLines = s.subtitle ? this.wrap(s.subtitle, W - 2 * M - 30).slice(0, 3) : [];
    var chips = s.meta || [];
    var bandH = 62 + titleLines.length * 31 + (subLines.length ? subLines.length * 15 + 6 : 0) + (chips.length ? 38 : 16);
    rgb(d, 'setFillColor', C.navy); d.rect(0, 0, W, bandH, 'F');
    // decorative rings, low opacity
    d.saveGraphicsState(); d.rect(0, 0, W, bandH, null); d.clip(); d.discardPath();
    var g = d.GState ? new d.GState({ opacity: 0.16 }) : null; if (g) d.setGState(g);
    rgb(d, 'setDrawColor', C.accent2); d.setLineWidth(1.2);
    for (var k = 0; k < 7; k++) d.circle(W - 70, bandH - 10, 30 + k * 26, 'S');
    rgb(d, 'setFillColor', C.accent); d.circle(W - 70, bandH - 10, 22, 'F');
    if (g) d.setGState(new d.GState({ opacity: 1 }));
    d.restoreGraphicsState();
    // accent rule + kicker
    rgb(d, 'setFillColor', C.accent2); d.rect(M, 34, 26, 3, 'F');
    this.font('Mono', 'normal', 8, C.lav); d.text(this.kicker, M + 34, 37);
    var y = 66;
    this.font('Bricolage', 'extrabold', 27, C.white);
    titleLines.forEach(function (l) { d.text(l, M, y); y += 31; });
    if (subLines.length) { y += 2; this.font('Inter', 'normal', 10.5, C.lav); subLines.forEach(function (l) { d.text(l, M, y); y += 15; }); }
    if (chips.length) {
      y += 10; var x = M; var self = this;
      chips.forEach(function (ch) {
        var label = String(ch[0]).toUpperCase(), val = String(ch[1]);
        self.font('Mono', 'normal', 6.5); var lw = self.tw(label); self.font('Inter', 'bold', 8.5); var vw = self.tw(val);
        var w = lw + vw + 26; if (x + w > W - M) { x = M; y += 24; }
        rgb(d, 'setDrawColor', C.navy2); rgb(d, 'setFillColor', C.navy2); d.roundedRect(x, y - 6, w, 19, 9.5, 9.5, 'F');
        self.font('Mono', 'normal', 6.5, C.lav); d.text(label, x + 10, y + 6.5);
        self.font('Inter', 'bold', 8.5, C.white); d.text(val, x + 10 + lw + 6, y + 6.6);
        x += w + 6;
      });
      y += 20;
    }
    this.y = bandH + 26;
  };

  // ---------- KPI tiles ----------
  P.kpis = function (items) {
    var d = this.doc, n = items.length, gap = 10, tw = (W - 2 * M - gap * (n - 1)) / n, pad = 12, self = this;
    // measure
    var labArr = items.map(function (it) { self.font('Mono', 'normal', 6.8); return self.wrap(String(it.label).toUpperCase(), tw - 2 * pad).slice(0, 2); });
    var subLinesArr = items.map(function (it) { self.font('Inter', 'normal', 8.2); return it.sub ? self.wrap(it.sub, tw - 2 * pad).slice(0, 3) : []; });
    var maxLab = Math.max.apply(null, labArr.map(function (a) { return a.length; }));
    var maxSub = Math.max.apply(null, subLinesArr.map(function (a) { return a.length; }));
    var labH = 18 + (maxLab - 1) * 9, th = labH + 28 + 11 + maxSub * 11 + (maxSub ? 4 : 0);
    this.need(th + 10);
    var y = this.y;
    items.forEach(function (it, i) {
      var x = M + i * (tw + gap), hero = it.hero;
      rgb(d, 'setFillColor', hero ? C.accent : C.faint); rgb(d, 'setDrawColor', hero ? C.accent : C.line); d.setLineWidth(0.6);
      d.roundedRect(x, y, tw, th, 10, 10, hero ? 'F' : 'FD');
      self.font('Mono', 'normal', 6.8, hero ? C.lav : C.ink3);
      var ly = y + 18; labArr[i].forEach(function (l) { d.text(l, x + pad, ly); ly += 9; });
      var vy = y + labH + 26;
      var size = self.fitSize(it.value, 'Bricolage', 'bold', 21, tw - 2 * pad, 11);
      self.font('Bricolage', 'bold', size, hero ? C.white : (it.color || C.accent)); d.text(String(it.value), x + pad, vy);
      self.font('Inter', 'normal', 8.2, hero ? C.lav : C.ink2);
      var sy = vy + 15; subLinesArr[i].forEach(function (l) { d.text(l, x + pad, sy); sy += 11; });
    });
    this.y = y + th + 18;
  };

  // ---------- headings and text ----------
  P.h2 = function (title, sub, after) {
    this.need(48 + (after || 60));
    var d = this.doc; this.font('Bricolage', 'bold', 15, C.ink); d.text(title, M, this.y + 12);
    rgb(d, 'setFillColor', C.accent); d.rect(M, this.y + 19, 22, 2.2, 'F');
    this.y += 30;
    if (sub) { this.font('Inter', 'normal', 8.8, C.ink2); var ls = this.wrap(sub, W - 2 * M); d.text(ls, M, this.y + 2); this.y += ls.length * 12 + 4; }
    this.y += 4;
  };
  P.para = function (text, opts) {
    opts = opts || {}; this.font('Inter', opts.bold ? 'medium' : 'normal', opts.size || 9.2, opts.color || C.ink2);
    var ls = this.wrap(text, W - 2 * M - (opts.indent || 0)), d = this.doc, lh = (opts.size || 9.2) * 1.42, self = this;
    ls.forEach(function (l) { self.need(lh); d.text(l, M + (opts.indent || 0), self.y + lh * 0.75); self.y += lh; });
    this.y += opts.after == null ? 6 : opts.after;
  };
  P.bullets = function (items, opts) {
    opts = opts || {}; var d = this.doc, self = this, lh = 13;
    items.forEach(function (it) {
      var head = typeof it === 'string' ? null : it[0], body = typeof it === 'string' ? it : it[1];
      self.font('Inter', 'normal', 9); var ls = self.wrap((head ? head + '  ' : '') + body, W - 2 * M - 16);
      self.need(ls.length * lh + 4);
      rgb(d, 'setFillColor', C.accent); d.circle(M + 4, self.y + 6, 2, 'F');
      var y = self.y;
      if (head) {
        self.font('Inter', 'bold', 9, C.ink); d.text(head, M + 14, y + 9.5); var hw = self.tw(head) + 6;
        self.font('Inter', 'normal', 9, C.ink2); var rest = self.wrap(body, W - 2 * M - 16 - hw); d.text(rest[0], M + 14 + hw, y + 9.5);
        var more = self.wrap(rest.slice(1).join(' '), W - 2 * M - 16); y += lh;
        if (rest.length > 1) { more.forEach(function (l) { d.text(l, M + 14, y + 9.5); y += lh; }); }
      } else { self.font('Inter', 'normal', 9, C.ink2); ls.forEach(function (l) { d.text(l, M + 14, y + 9.5); y += lh; }); }
      self.y = y + 3;
    });
    this.y += 6;
  };
  P.callout = function (title, lines, tone) {
    var d = this.doc, self = this, pad = 14, fill = tone === 'green' ? C.greenSoft : tone === 'amber' ? C.amberSoft : tone === 'rose' ? C.roseSoft : C.soft;
    var bar = tone === 'green' ? C.green : tone === 'amber' ? C.amber : tone === 'rose' ? C.rose : C.accent;
    this.font('Inter', 'normal', 8.8);
    var wrapped = lines.map(function (l) { return self.wrap(l, W - 2 * M - 2 * pad - 6); });
    var h = pad + 14 + wrapped.reduce(function (s, a) { return s + a.length * 12 + 3; }, 0) + pad - 4;
    this.need(h + 8); var y = this.y;
    rgb(d, 'setFillColor', fill); d.roundedRect(M, y, W - 2 * M, h, 10, 10, 'F');
    rgb(d, 'setFillColor', bar); d.roundedRect(M, y + 10, 3, h - 20, 1.5, 1.5, 'F');
    this.font('Inter', 'bold', 10, C.ink); d.text(title, M + pad + 4, y + pad + 4);
    var ty = y + pad + 20; this.font('Inter', 'normal', 8.8, C.ink2);
    wrapped.forEach(function (a) { a.forEach(function (l) { d.text(l, M + pad + 4, ty); ty += 12; }); ty += 3; });
    this.y = y + h + 14;
  };
  P.kv = function (rows, cols) {
    cols = cols || 2; var d = this.doc, self = this, gap = 14, cw = (W - 2 * M - gap * (cols - 1)) / cols, n = Math.ceil(rows.length / cols);
    // measure each row of the grid: value wraps to the space right of its label
    var cells = rows.map(function (r) {
      self.font('Inter', 'normal', 8.3); var lab = self.wrap(r[0], cw * 0.5)[0], lw = self.tw(lab);
      self.font('Inter', 'bold', 8.8); var vals = self.wrap(String(r[1]), cw - lw - 10).slice(0, 2);
      return { lab: lab, vals: vals };
    });
    var rh = []; for (var rr = 0; rr < n; rr++) { var mx = 1; for (var c = 0; c < cols; c++) { var cell = cells[rr * cols + c]; if (cell && cell.vals.length > mx) mx = cell.vals.length; } rh.push(14 + mx * 11); }
    var total = rh.reduce(function (a, b) { return a + b; }, 0);
    this.need(Math.min(total, 120) + 8);
    var y = this.y;
    for (rr = 0; rr < n; rr++) {
      if (y + rh[rr] > H - FOOT - 14) { this.newPage(); y = this.y; }
      for (c = 0; c < cols; c++) {
        var i = rr * cols + c, cell = cells[i]; if (!cell) continue;
        var x = M + c * (cw + gap);
        rgb(d, 'setDrawColor', C.line); d.setLineWidth(0.5); d.line(x, y + rh[rr] - 4, x + cw, y + rh[rr] - 4);
        self.font('Inter', 'normal', 8.3, C.ink3); d.text(cell.lab, x, y + 12);
        self.font('Inter', 'bold', 8.8, C.ink); var vy = y + 12; cell.vals.forEach(function (v) { d.text(v, x + cw, vy, { align: 'right' }); vy += 11; });
      }
      y += rh[rr];
    }
    this.y = y + 12;
  };

  // ---------- charts ----------
  // series: [{name, color, values[], fill(bool), stackOn(bool)}] drawn in order; values aligned with xLabels
  P.areaChart = function (o) {
    var d = this.doc, self = this, h = o.height || 170, left = M + 46, right = W - M - 6, pw = right - left;
    this.need(h + 58 + (o.title ? 20 : 0));
    if (o.title) { this.font('Inter', 'bold', 9.5, C.ink); d.text(o.title, M, this.y + 8); this.y += 18; }
    var top = this.y, bottom = top + h, n = o.xLabels.length;
    var maxV = 0; o.series.forEach(function (s) { s.values.forEach(function (v) { if (v != null && v > maxV) maxV = v; }); });
    var nt = niceTicks(maxV * 1.02), ymax = nt.max, fmt = o.yFormat || function (v) { return fmtINR(v, { plain: true }); };
    var X = function (i) { return left + pw * i / Math.max(1, n - 1); }, Y = function (v) { return bottom - Math.min(1, v / ymax) * h; };
    rgb(d, 'setDrawColor', C.line); d.setLineWidth(0.5); this.font('Mono', 'normal', 6.6, C.ink3);
    nt.ticks.forEach(function (tv) { var gy = Y(tv); d.line(left, gy, right, gy); d.text(fmt(tv), left - 6, gy + 2.3, { align: 'right' }); });
    // areas
    o.series.forEach(function (s) {
      if (s.fill === false) return;
      var pts = s.values.map(function (v, i) { return [X(i), Y(v || 0)]; });
      var base = s.baseline ? s.baseline.map(function (v, i) { return [X(i), Y(v)]; }) : null;
      var poly = pts.slice(); if (base) { for (var i = n - 1; i >= 0; i--) poly.push(base[i]); } else { poly.push([X(n - 1), bottom]); poly.push([X(0), bottom]); }
      var g = d.GState ? new d.GState({ opacity: s.opacity == null ? 0.82 : s.opacity }) : null; if (g) d.setGState(g);
      rgb(d, 'setFillColor', s.color); fillPoly(d, poly);
      if (g) d.setGState(new d.GState({ opacity: 1 }));
    });
    // lines on top
    o.series.forEach(function (s) {
      if (s.line === false) return;
      rgb(d, 'setDrawColor', s.lineColor || s.color); d.setLineWidth(s.fill === false ? 1.6 : 1); if (s.dash) d.setLineDashPattern([3, 2], 0);
      for (var i = 1; i < n; i++) { if (s.values[i - 1] == null || s.values[i] == null) continue; d.line(X(i - 1), Y(s.values[i - 1]), X(i), Y(s.values[i])); }
      if (s.dash) d.setLineDashPattern([], 0);
    });
    // x labels
    this.font('Mono', 'normal', 6.6, C.ink3); var step = Math.max(1, Math.ceil(n / 9));
    for (var i = 0; i < n; i++) if (i % step === 0 || i === n - 1) { if (i === n - 1 && (n - 1) % step !== 0 && (n - 1) % step < step / 2) continue; d.text(String(o.xLabels[i]), X(i), bottom + 11, { align: 'center' }); }
    rgb(d, 'setDrawColor', C.ink3); d.setLineWidth(0.6); d.line(left, bottom, right, bottom);
    // marker with collision safe annotation
    if (o.mark) {
      var mi = o.mark.index, mv = o.mark.value, mx = X(mi), my = Y(mv);
      rgb(d, 'setDrawColor', C.accent); d.setLineWidth(0.8); d.setLineDashPattern([2.5, 2], 0); d.line(mx, top, mx, bottom); d.setLineDashPattern([], 0);
      rgb(d, 'setFillColor', C.white); d.circle(mx, my, 4.2, 'F'); rgb(d, 'setFillColor', C.accent); d.circle(mx, my, 2.8, 'F');
      this.font('Inter', 'bold', 7.8); var lab = o.mark.label, lw = this.tw(lab) + 14, lh = 16;
      var lx = mx + 8; if (lx + lw > right) lx = mx - 8 - lw; var ly = my - 22; if (ly < top + 2) ly = my + 8; if (ly + lh > bottom) ly = bottom - lh - 2;
      rgb(d, 'setFillColor', C.ink); d.roundedRect(lx, ly, lw, lh, 4, 4, 'F'); rgb(d, 'setTextColor', C.white); d.text(lab, lx + 7, ly + 11);
    }
    // legend
    var lx2 = M, ly2 = bottom + 26; this.font('Inter', 'normal', 7.8, C.ink2);
    o.series.forEach(function (s) { if (s.legend === false) return; rgb(d, 'setFillColor', s.color); d.roundedRect(lx2, ly2 - 6.5, 9, 9, 2, 2, 'F'); d.text(s.name, lx2 + 13, ly2); lx2 += self.tw(s.name) + 28; });
    if (o.note) { this.font('Inter', 'normal', 7.4, C.ink3); d.text(this.wrap(o.note, right - lx2 - 6)[0], right, ly2, { align: 'right' }); }
    this.y = bottom + 44;
  };
  // grouped or stacked bars: cats[], series[{name,color,values}]
  P.barChart = function (o) {
    var d = this.doc, self = this, h = o.height || 150, left = M + 46, right = W - M - 6, pw = right - left, n = o.cats.length;
    this.need(h + 60 + (o.title ? 20 : 0));
    if (o.title) { this.font('Inter', 'bold', 9.5, C.ink); d.text(o.title, M, this.y + 8); this.y += 18; }
    var top = this.y, bottom = top + h, stacked = !!o.stacked, maxV = 0;
    for (var i = 0; i < n; i++) { var tot = 0; o.series.forEach(function (s) { var v = s.values[i] || 0; if (stacked) tot += v; else if (v > maxV) maxV = v; }); if (stacked && tot > maxV) maxV = tot; }
    var nt = niceTicks(maxV * 1.05), ymax = nt.max, fmt = o.yFormat || function (v) { return fmtINR(v, { plain: true }); };
    rgb(d, 'setDrawColor', C.line); d.setLineWidth(0.5); this.font('Mono', 'normal', 6.6, C.ink3);
    nt.ticks.forEach(function (tv) { var gy = bottom - tv / ymax * h; d.line(left, gy, right, gy); d.text(fmt(tv), left - 6, gy + 2.3, { align: 'right' }); });
    var slot = pw / n, inner = slot * 0.64, bw = stacked ? inner : inner / o.series.length;
    for (i = 0; i < n; i++) {
      var x0 = left + slot * i + (slot - inner) / 2, base = bottom;
      o.series.forEach(function (s, j) {
        var v = s.values[i] || 0, bh = v / ymax * h; rgb(d, 'setFillColor', s.color);
        if (stacked) { d.rect(x0, base - bh, bw, bh, 'F'); base -= bh; } else d.roundedRect(x0 + j * bw, bottom - bh, bw - 2, bh, 2, 2, 'F');
      });
      this.font('Mono', 'normal', 6.6, C.ink3); d.text(String(o.cats[i]), left + slot * i + slot / 2, bottom + 11, { align: 'center' });
      if (o.labels) { var lv = stacked ? o.series.reduce(function (t, s) { return t + (s.values[i] || 0); }, 0) : null; if (lv != null) { this.font('Inter', 'bold', 7.2, C.ink); d.text(fmt(lv), left + slot * i + slot / 2, base - 4, { align: 'center' }); } }
    }
    rgb(d, 'setDrawColor', C.ink3); d.setLineWidth(0.6); d.line(left, bottom, right, bottom);
    var lx2 = M, ly2 = bottom + 26; this.font('Inter', 'normal', 7.8, C.ink2);
    o.series.forEach(function (s) { rgb(d, 'setFillColor', s.color); d.roundedRect(lx2, ly2 - 6.5, 9, 9, 2, 2, 'F'); d.text(s.name, lx2 + 13, ly2); lx2 += self.tw(s.name) + 28; });
    if (o.note) { this.font('Inter', 'normal', 7.4, C.ink3); d.text(this.wrap(o.note, right - lx2 - 6)[0], right, ly2, { align: 'right' }); }
    this.y = bottom + 44;
  };
  // horizontal split bar, e.g. principal vs interest
  P.splitBar = function (o) {
    var d = this.doc, self = this, tot = o.parts.reduce(function (s, p) { return s + p.value; }, 0) || 1, x = M, bw = W - 2 * M, bh = 16;
    this.need(bh + 46 + (o.title ? 18 : 0));
    if (o.title) { this.font('Inter', 'bold', 9.5, C.ink); d.text(o.title, M, this.y + 8); this.y += 18; }
    var y = this.y; rgb(d, 'setFillColor', C.faint); d.roundedRect(M, y, bw, bh, 5, 5, 'F');
    o.parts.forEach(function (p) { var w = bw * p.value / tot; rgb(d, 'setFillColor', p.color); if (w > 0.5) d.rect(x, y, w, bh, 'F'); x += w; });
    // round the ends by redrawing a border
    rgb(d, 'setDrawColor', C.white); d.setLineWidth(2); d.roundedRect(M - 1, y - 1, bw + 2, bh + 2, 6, 6, 'S');
    var lx = M, ly = y + bh + 16;
    o.parts.forEach(function (p) {
      rgb(d, 'setFillColor', p.color); d.roundedRect(lx, ly - 7, 9, 9, 2, 2, 'F');
      self.font('Inter', 'bold', 8.2, C.ink); var t1 = p.name + '  ' + fmtINR(p.value) + '  (' + Math.round(p.value / tot * 100) + '%)'; d.text(t1, lx + 13, ly); lx += self.tw(t1) + 30;
    });
    this.y = ly + 18;
  };

  // ---------- table ----------
  P.table = function (o) {
    var d = this.doc, self = this, head = o.head, rows = o.rows, nc = head.length, pad = 6, rh = o.rowHeight || 14.5, fs = o.fontSize || 8, lh = fs * 1.3;
    var align = o.align || head.map(function (_, i) { return i === 0 ? 'left' : 'right'; });
    // natural column widths from content, then shrink the widest text columns and wrap their cells
    var w = head.map(function (hd) { self.font('Inter', 'bold', fs); return self.tw(hd) + 2 * pad; });
    rows.forEach(function (r) { self.font('Inter', 'normal', fs); r.forEach(function (c, i) { var tw = self.tw(c) + 2 * pad; if (tw > w[i]) w[i] = tw; }); });
    var avail = W - 2 * M, sum = w.reduce(function (a, b) { return a + b; }, 0);
    if (sum > avail) {
      // shrink only columns wider than their fair share, keep numeric columns intact
      var order = w.map(function (x, i) { return i; }).sort(function (i, j) { return w[j] - w[i]; });
      var over = sum - avail;
      for (var k = 0; k < order.length && over > 0; k++) { var i = order[k], floor = Math.max(70, avail / nc * 0.9); var cut = Math.min(over, w[i] - floor); if (cut > 0) { w[i] -= cut; over -= cut; } }
      sum = w.reduce(function (a, b) { return a + b; }, 0);
    }
    var scale = avail / sum; w = w.map(function (x) { return x * scale; });
    // wrap cells
    var wrapped = rows.map(function (r) { self.font('Inter', 'normal', fs); return r.map(function (c, i) { return self.wrap(String(c), w[i] - 2 * pad); }); });
    function header() {
      self.need(rh + 6); rgb(d, 'setFillColor', C.ink); d.roundedRect(M, self.y, avail, rh + 3, 4, 4, 'F');
      self.font('Inter', 'bold', fs, C.white); var x = M;
      head.forEach(function (hd, i) { d.text(self.wrap(hd, w[i] - 2 * pad)[0], align[i] === 'right' ? x + w[i] - pad : x + pad, self.y + rh - 2.5, { align: align[i] === 'right' ? 'right' : 'left' }); x += w[i]; });
      self.y += rh + 3;
    }
    header();
    wrapped.forEach(function (cells, ri) {
      var lines = Math.max.apply(null, cells.map(function (c) { return c.length; })), h = Math.max(rh, lines * lh + (rh - fs));
      if (self.y + h > H - FOOT - 14) { self.newPage(); header(); }
      var hl = o.highlight != null && ri === o.highlight;
      if (hl) { rgb(d, 'setFillColor', C.soft); d.rect(M, self.y, avail, h, 'F'); rgb(d, 'setFillColor', C.accent); d.rect(M, self.y, 3, h, 'F'); }
      else if (ri % 2) { rgb(d, 'setFillColor', C.faint); d.rect(M, self.y, avail, h, 'F'); }
      self.font('Inter', hl ? 'bold' : 'normal', fs, hl ? C.accent : C.ink);
      var x = M; cells.forEach(function (c, i) { var ty = self.y + rh - 4.2; c.forEach(function (line) { d.text(line, align[i] === 'right' ? x + w[i] - pad : x + pad, ty, { align: align[i] === 'right' ? 'right' : 'left' }); ty += lh; }); x += w[i]; });
      self.y += h;
    });
    rgb(d, 'setDrawColor', C.line); d.setLineWidth(0.5); d.line(M, this.y, W - M, this.y);
    this.y += 10;
    if (o.note) { this.font('Inter', 'normal', 7.6, C.ink3); d.text(this.wrap(o.note, avail), M, this.y + 6); this.y += 18; }
  };

  // ---------- step list (how to) ----------
  P.steps = function (items) {
    var d = this.doc, self = this;
    items.forEach(function (it, i) {
      self.font('Inter', 'normal', 8.8); var ls = self.wrap(it[1], W - 2 * M - 40);
      var h = Math.max(30, 16 + ls.length * 12); self.need(h + 4); var y = self.y;
      rgb(d, 'setFillColor', C.accent); d.circle(M + 11, y + 11, 11, 'F'); self.font('Bricolage', 'bold', 10, C.white); d.text(String(i + 1), M + 11, y + 14.5, { align: 'center' });
      self.font('Inter', 'bold', 9.5, C.ink); d.text(it[0], M + 32, y + 10);
      self.font('Inter', 'normal', 8.8, C.ink2); var ty = y + 23; ls.forEach(function (l) { d.text(l, M + 32, ty); ty += 12; });
      self.y = y + h + 4;
    });
    this.y += 6;
  };

  // ---------- closing signature block ----------
  P.signoff = function () {
    var d = this.doc; this.need(70); var y = this.y + 6;
    rgb(d, 'setFillColor', C.faint); d.roundedRect(M, y, W - 2 * M, 56, 10, 10, 'F');
    rgb(d, 'setFillColor', C.accent); d.circle(M + 30, y + 28, 15, 'F'); this.font('Bricolage', 'extrabold', 12, C.white); d.text('SH', M + 30, y + 32.5, { align: 'center' });
    this.font('Inter', 'bold', 9.6, C.ink); d.text('Built by Syed Hadi', M + 56, y + 22);
    this.font('Inter', 'normal', 8.4, C.ink2); d.text('Product Marketing and Partnerships Lead at AccuKnox. More free calculators and the GTM playbook at syedcreates.com', M + 56, y + 36);
    this.font('Mono', 'normal', 7, C.accent); d.text((this.spec.url || 'syedcreates.com').toUpperCase(), W - M - 14, y + 22, { align: 'right' });
    this.y = y + 70;
  };

  function fillPoly(doc, pts) {
    var segs = []; for (var i = 1; i < pts.length; i++) segs.push([pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]]);
    doc.lines(segs, pts[0][0], pts[0][1], [1, 1], 'F', true);
  }

  function build(spec) {
    if (!fontData) throw new Error('fonts not loaded');
    var J = window.jspdf.jsPDF, doc = new J({ unit: 'pt', format: 'a4', compress: true });
    FONTS.forEach(function (f, i) { doc.addFileToVFS(f[0], fontData[i]); doc.addFont(f[0], f[1], f[2]); });
    doc.setProperties({ title: spec.docTitle || spec.title, author: 'Syed Hadi, syedcreates.com', subject: spec.kicker || '', creator: 'syedcreates.com' });
    var e = new Engine(doc, spec);
    e.cover();
    (spec.blocks || []).forEach(function (b, i) {
      switch (b.type) {
        case 'kpis': e.kpis(b.items); break;
        case 'h2': var nb = (spec.blocks || [])[i + 1] || {}, est = { area: (nb.height || 170) + 90, bars: (nb.height || 150) + 90, table: 70, kv: 130, bullets: 70, steps: 60, callout: 70, para: 36, kpis: 100, split: 70 }[nb.type] || 50; e.h2(b.title, b.sub, est); break;
        case 'para': e.para(b.text, b); break;
        case 'bullets': e.bullets(b.items); break;
        case 'callout': e.callout(b.title, b.lines, b.tone); break;
        case 'kv': e.kv(b.rows, b.cols); break;
        case 'area': e.areaChart(b); break;
        case 'bars': e.barChart(b); break;
        case 'split': e.splitBar(b); break;
        case 'table': e.table(b); break;
        case 'steps': e.steps(b.items); break;
        case 'page': if (b.force || e.y > (b.ifBelow || 0.45) * H) e.newPage(); break;
        case 'space': e.y += b.h || 10; break;
        case 'signoff': e.signoff(); break;
      }
    });
    e.footers();
    return doc;
  }
  window.SHReport = { ready: ready, build: build, fmtINR: fmtINR, C: C };
})();
