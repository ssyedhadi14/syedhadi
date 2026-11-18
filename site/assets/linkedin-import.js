/*
 * Created by: Claude Cowork
 * Date: 2026-11-18
 * Purpose: LinkedIn import for the resume builder on /interview-prep#resume.
 *          The visitor pastes their LinkedIn URL, saves their own profile with
 *          LinkedIn's "Save to PDF", and drops the PDF here. The PDF is parsed in
 *          the browser with pdf.js (loaded only on use) and fills the builder.
 *          Nothing is uploaded or scraped. LinkedIn profiles are not fetched.
 * Owner: Syed Hadi
 */
(function () {
  'use strict';

  var MON = 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec';
  var DATE_RE = new RegExp('^((?:' + MON + ')[a-z]*\\.?\\s+\\d{4}|\\d{4})\\s*[-\\u2013\\u2014]\\s*(Present|(?:' + MON + ')[a-z]*\\.?\\s+\\d{4}|\\d{4})', 'i');
  var DUR_RE = /^\(?\s*(less than a year|\d+\s+(years?|yrs?|months?|mos?)(\s+\d+\s+(months?|mos?))?)\s*\)?$/i;
  var PAGE_RE = /^page\s+\d+\s+of\s+\d+$/i;
  var MAIN_HEADS = ['summary', 'about', 'experience', 'education', 'licenses & certifications', 'volunteer experience', 'projects', 'publications', 'honors & awards', 'honors-awards', 'skills'];
  var SIDE_HEADS = ['contact', 'top skills', 'languages', 'certifications', 'honors-awards', 'honors & awards', 'publications', 'patents'];

  /* ----------------------------------------------------------- parser */
  function toLines(pages) {
    var out = [];
    pages.forEach(function (pg, pi) {
      var split = pg.width * 0.3;
      var items = pg.items.slice().sort(function (a, b) { return a.y - b.y || a.x - b.x; });
      var rows = [];
      items.forEach(function (it) {
        var col = it.x < split ? 'side' : 'main';
        var r = null;
        for (var k = rows.length - 1; k >= 0 && k >= rows.length - 6; k--) {
          if (rows[k].col === col && Math.abs(rows[k].y - it.y) < 2.2) { r = rows[k]; break; }
        }
        if (!r) { r = { col: col, y: it.y, page: pi, size: 0, parts: [] }; rows.push(r); }
        r.parts.push(it); r.size = Math.max(r.size, it.size);
      });
      rows.forEach(function (r) {
        r.parts.sort(function (a, b) { return a.x - b.x; });
        var t = r.parts.map(function (p) { return p.str; }).join(' ').replace(/\s+/g, ' ').trim();
        if (t && !PAGE_RE.test(t)) out.push({ text: t, size: Math.round(r.size * 10) / 10, y: r.y, page: r.page, col: r.col });
      });
    });
    return out;
  }

  function isHead(l, list, minSize) { return l.size >= minSize && list.indexOf(l.text.toLowerCase()) >= 0; }

  function sections(lines, list, minSize) {
    var secs = { _top: [] }, cur = '_top';
    lines.forEach(function (l) {
      if (isHead(l, list, minSize)) { cur = l.text.toLowerCase(); secs[cur] = secs[cur] || []; return; }
      secs[cur].push(l);
    });
    return secs;
  }

  function shortDate(s) {
    return s.replace(new RegExp('\\b(' + MON + ')[a-z]*\\.?', 'gi'), function (m, a) { return a.charAt(0).toUpperCase() + a.slice(1, 3).toLowerCase(); })
      .replace(/\s*[-–—]\s*/, ' to ').replace(/\s*\(.*\)\s*$/, '').trim();
  }
  var CC = { 'india': 'IN', 'united states': 'US', 'united arab emirates': 'AE', 'united kingdom': 'UK', 'singapore': 'SG', 'canada': 'CA', 'australia': 'AU', 'germany': 'DE', 'saudi arabia': 'SA', 'qatar': 'QA', 'japan': 'JP', 'netherlands': 'NL', 'france': 'FR' };
  function shortCity(s) {
    var p = String(s || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
    if (!p.length) return '';
    if (p.length === 1) return p[0];
    var last = p[p.length - 1], code = CC[last.toLowerCase()] || last;
    return p[0] + ', ' + code;
  }
  function looksLocation(t) {
    return t.length < 70 && !/[.!?]$/.test(t) && (/,/.test(t) || /\b(remote|hybrid|area|india|dubai|singapore|bengaluru|bangalore|london)\b/i.test(t)) && !DATE_RE.test(t);
  }

  function toBullets(lines) {
    var paras = [], cur = '';
    lines.forEach(function (l) {
      var t = l.text, starts = /^[-*•●▪–]\s+/.test(t);
      if (starts) { if (cur) paras.push(cur); cur = t.replace(/^[-*•●▪–]\s+/, ''); }
      else cur = cur ? (cur + ' ' + t) : t;
    });
    if (cur) paras.push(cur);
    var out = [];
    paras.forEach(function (p) {
      if (paras.length === 1 && p.length > 160) {
        p.split(/(?<=[.!?])\s+(?=[A-Z])/).forEach(function (s) { s = s.trim(); if (s) out.push(s.replace(/\.$/, '')); });
      } else out.push(p.replace(/\.$/, ''));
    });
    return out.slice(0, 6).join('\n');
  }

  function parseExperience(L) {
    var jobs = [], dates = [];
    L.forEach(function (l, i) { if (DATE_RE.test(l.text)) dates.push(i); });
    var job = null;
    dates.forEach(function (d, n) {
      var title = L[d - 1] || { text: '', size: 0 };
      var k = d - 2, company = null;
      if (k >= 0 && DUR_RE.test(L[k].text)) k--;
      var prevEnd = n ? dates[n - 1] : -1;
      if (k > prevEnd && L[k] && L[k].size > title.size + 0.2) company = L[k].text;
      else if (!job && k >= 0 && L[k]) company = L[k].text;
      if (company || !job) { job = { company: company || '', city: '', roles: [] }; jobs.push(job); }
      // description runs to the next role's title, minus its company and duration lines
      var end = n + 1 < dates.length ? dates[n + 1] - 1 : L.length;
      if (n + 1 < dates.length) {
        var nt = L[dates[n + 1] - 1], e = end - 1;
        if (e > d && DUR_RE.test(L[e].text)) e--;
        if (e > d && L[e].size > nt.size + 0.2) e--;
        end = e + 1;
      }
      var j = d + 1, city = '';
      if (L[j] && j < end && looksLocation(L[j].text)) { city = L[j].text; j++; }
      if (!job.city && city) job.city = shortCity(city);
      job.roles.push({ title: title.text, dates: shortDate(L[d].text.match(DATE_RE)[0]), bullets: toBullets(L.slice(j, end)), tools: '' });
    });
    return jobs;
  }

  function parseEducation(L) {
    var edu = [], cur = null;
    L.forEach(function (l) {
      var yr = l.text.match(/\(?\s*((?:[A-Za-z]+\s+)?\d{4})\s*[-–]\s*((?:[A-Za-z]+\s+)?\d{4}|Present)\s*\)?\s*$/);
      if (/·/.test(l.text) || yr) {
        if (!cur) { cur = { school: '', degree: '', city: '', years: '' }; edu.push(cur); }
        var deg = l.text.split('·')[0].replace(/\(?\s*\d{4}\s*[-–]\s*(\d{4}|Present)\s*\)?\s*$/, '').trim().replace(/[,\s]+$/, '');
        var m = deg.match(/^.+?\s-\s(.+)$/); if (m && m[1].length < deg.length) deg = m[1];
        if (deg) cur.degree = cur.degree ? cur.degree + ' ' + deg : deg;
        if (yr) cur.years = yr[1].replace(/[A-Za-z]+\s+/, '') + ' - ' + yr[2].replace(/[A-Za-z]+\s+(?=\d)/, '');
      } else if (l.size >= 11.6) {
        cur = { school: l.text, degree: '', city: '', years: '' }; edu.push(cur);
      } else if (cur && !cur.degree) cur.degree = l.text;
    });
    return edu.filter(function (e) { return e.school || e.degree; });
  }

  function parseLinkedIn(pages) {
    var lines = toLines(pages);
    var main = lines.filter(function (l) { return l.col === 'main'; });
    var side = lines.filter(function (l) { return l.col === 'side'; });
    var all = lines.map(function (l) { return l.text; }).join('\n');
    var sideJoined = side.map(function (l) { return l.text; }).join('');
    var r = {};

    // name, headline, location from the top of the main column
    var p0 = main.filter(function (l) { return l.page === 0; });
    var nameLine = p0.reduce(function (a, l) { return !a || l.size > a.size ? l : a; }, null);
    if (nameLine) {
      r.name = nameLine.text;
      var idx = main.indexOf(nameLine), head = [], i = idx + 1;
      while (main[i] && main[i].size >= 11.3 && main[i].size < 14 && !isHead(main[i], MAIN_HEADS, 13)) { head.push(main[i].text); i++; }
      if (head.length) r.highlight = head.join(' ');
      if (main[i] && main[i].size < 11.3 && looksLocation(main[i].text)) r.city = shortCity(main[i].text);
    }
    var em = all.match(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/); if (em) r.email = em[0];
    var li = (sideJoined + all.replace(/\n/g, '')).match(/linkedin\.com\/in\/[A-Za-z0-9\-_%]+/i); if (li) r.linkedin = li[0].replace(/^/, '');
    var ph = all.match(/\+?\d[\d\s-]{8,}\d/); if (ph && /\(mobile\)|\(home\)|\(work\)/i.test(all)) r.phone = ph[0].trim();

    var ms = sections(main, MAIN_HEADS, 13.5), ss = sections(side, SIDE_HEADS, 12);
    if (ms.experience) r.jobs = parseExperience(ms.experience);
    if (ms.education) r.edu = parseEducation(ms.education);
    if (ss['top skills'] && ss['top skills'].length) r.s1 = ss['top skills'].map(function (l) { return l.text; }).join(', ');
    if (ss.certifications && ss.certifications.length) r.certs = ss.certifications.map(function (l) { return l.text; }).join('\n');
    var sum = ms.summary || ms.about;
    r._summary = sum ? sum.map(function (l) { return l.text; }).join(' ') : '';

    // years of experience from the earliest role start
    var first = null;
    (r.jobs || []).forEach(function (j) { j.roles.forEach(function (ro) { var y = (ro.dates.match(/\d{4}/) || [])[0]; if (y && (!first || +y < first)) first = +y; }); });
    if (first) r.yoe = String(Math.max(1, new Date().getFullYear() - first));
    return r;
  }
  window.LIParse = parseLinkedIn;

  /* -------------------------------------------------------------- PDF */
  var pdfjsP = null;
  function loadPdfjs() {
    if (!pdfjsP) {
      pdfjsP = import('/assets/vendor/pdfjs/pdf.min.mjs').then(function (m) {
        m.GlobalWorkerOptions.workerSrc = '/assets/vendor/pdfjs/pdf.worker.min.mjs';
        return m;
      });
    }
    return pdfjsP;
  }
  function readPdf(file) {
    return file.arrayBuffer().then(function (buf) {
      return loadPdfjs().then(function (pdfjs) { return pdfjs.getDocument({ data: new Uint8Array(buf) }).promise; });
    }).then(function (doc) {
      var jobs = [];
      for (var i = 1; i <= Math.min(doc.numPages, 8); i++) {
        jobs.push(doc.getPage(i).then(function (pg) {
          var vp = pg.getViewport({ scale: 1 });
          return pg.getTextContent().then(function (tc) {
            return { width: vp.width, height: vp.height, items: tc.items.filter(function (t) { return t.str && t.str.trim(); }).map(function (t) {
              return { str: t.str, x: t.transform[4], y: vp.height - t.transform[5], size: Math.hypot(t.transform[0], t.transform[1]) };
            }) };
          });
        }));
      }
      return Promise.all(jobs);
    });
  }

  /* --------------------------------------------------------------- UI */
  function $(id) { return document.getElementById(id); }
  var STEPS = ['Reading your PDF', 'Finding your roles and dates', 'Writing bullet points', 'Building your resume'];
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  function showLoader(on) {
    var o = $('liLoader'); if (!o) return;
    o.hidden = !on; document.body.classList.toggle('li-busy', on);
    if (on) { o.querySelectorAll('.li-step').forEach(function (s) { s.className = 'li-step'; }); setProgress(0); }
  }
  function setProgress(p) { var b = $('liBar'); if (b) b.style.width = Math.round(p) + '%'; var n = $('liPct'); if (n) n.textContent = Math.round(p) + '%'; }
  function step(i, state) { var s = document.querySelectorAll('#liLoader .li-step')[i]; if (s) s.className = 'li-step ' + state; }

  function handle(file) {
    var msg = $('liMsg');
    if (!file) return;
    if (!/\.pdf$/i.test(file.name) && file.type !== 'application/pdf') { msg.textContent = 'Please choose the PDF you saved from LinkedIn.'; return; }
    if (file.size > 8 * 1024 * 1024) { msg.textContent = 'That file is over 8 MB. LinkedIn profile PDFs are usually under 1 MB.'; return; }
    msg.textContent = '';
    showLoader(true);
    var t0 = Date.now(), data = null;
    step(0, 'run'); setProgress(8);
    readPdf(file).then(function (pages) {
      step(0, 'ok'); step(1, 'run'); setProgress(38);
      data = parseLinkedIn(pages);
      return wait(450);
    }).then(function () {
      step(1, 'ok'); step(2, 'run'); setProgress(66);
      return wait(450);
    }).then(function () {
      step(2, 'ok'); step(3, 'run'); setProgress(88);
      var url = ($('liUrl').value || '').trim();
      if (url) data.linkedin = url.replace(/^https?:\/\/(www\.)?/i, '').replace(/\/$/, '');
      var ok = data.name && data.jobs && data.jobs.length;
      if (!ok) throw new Error('shape');
      if (typeof window.IP_RS_IMPORT === 'function') window.IP_RS_IMPORT(data);
      return wait(Math.max(300, 1400 - (Date.now() - t0)));
    }).then(function () {
      step(3, 'ok'); setProgress(100);
      return wait(500);
    }).then(function () {
      showLoader(false);
      var roles = data.jobs.reduce(function (n, j) { return n + j.roles.length; }, 0);
      msg.innerHTML = '<b>Done.</b> Imported ' + roles + ' role' + (roles === 1 ? '' : 's') + (data.edu ? ' and ' + data.edu.length + ' education entr' + (data.edu.length === 1 ? 'y' : 'ies') : '') + '. Check the details below, add numbers to your bullets, then download the PDF.';
      var f = $('rsForm'); if (f) f.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (window.shTrack) window.shTrack('resume_linkedin_import', { label: String(roles) });
    }).catch(function (e) {
      showLoader(false);
      msg.textContent = e && e.message === 'shape'
        ? 'That PDF does not look like a LinkedIn profile export. On your profile, use More, then Save to PDF, and try again.'
        : 'Could not read that PDF. Try saving it again from LinkedIn, or fill the builder below by hand.';
    });
  }

  function init() {
    var drop = $('liDrop'), file = $('liFile'), url = $('liUrl'), open = $('liOpen');
    if (!drop) return;
    open.addEventListener('click', function () {
      var v = (url.value || '').trim(), msg = $('liMsg');
      var m = v.match(/linkedin\.com\/in\/([A-Za-z0-9\-_%]+)/i);
      if (!m) { msg.textContent = 'Paste your profile URL, like linkedin.com/in/yourname'; url.focus(); return; }
      msg.textContent = 'Your profile opened in a new tab. Click More (or Resources), then Save to PDF, and drop the file here.';
      window.open('https://www.linkedin.com/in/' + m[1] + '/', '_blank', 'noopener');
      document.querySelector('.li-card').classList.add('li-s2');
      loadPdfjs().catch(function () {});
    });
    file.addEventListener('change', function () { handle(file.files[0]); file.value = ''; });
    ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('over'); }); });
    drop.addEventListener('drop', function (e) { handle(e.dataTransfer.files[0]); });
    drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); file.click(); } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
