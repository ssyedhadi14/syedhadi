/* Created by: Claude
   Date: 2026-11-02
   Purpose: BMI and healthy habits calculator for syedcreates.com. BMI with Asian Indian and WHO bands, waist to height
            ratio, optional BP, fasting glucose, HbA1c and SGPT checks, a personalised start doing / stop doing table,
            and a 7 day habits tracker saved on the device. Exposes window.__calc (kind 'bmi') for the PDF engine.
   Owner: Syed Hadi */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var num = function (id) { var el = $(id); if (!el) return NaN; var v = parseFloat(String(el.value).replace(/[^0-9.]/g, '')); return isFinite(v) ? v : NaN; };
  var r1 = function (x) { return (Math.round(x * 10) / 10).toFixed(1); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } } };

  // Bands. Asian Indian: Misra et al. 2009, reaffirmed in the 2025 revised definition (BMI above 23 plus waist or WHtR).
  function bandIndia(b) {
    if (b < 18.5) return { k: 'under', name: 'Underweight', tone: 'amber' };
    if (b < 23) return { k: 'normal', name: 'Healthy range', tone: 'green' };
    if (b < 25) return { k: 'over', name: 'Overweight', tone: 'amber' };
    if (b < 30) return { k: 'obese1', name: 'Obesity', tone: 'rose' };
    return { k: 'obese2', name: 'Obesity, higher range', tone: 'rose' };
  }
  function bandWHO(b) { return b < 18.5 ? 'Underweight' : b < 25 ? 'Normal' : b < 30 ? 'Overweight' : b < 35 ? 'Obesity class I' : b < 40 ? 'Obesity class II' : 'Obesity class III'; }

  function markers(s) {
    var out = [];
    if (s.sys > 0 && s.dia > 0) {
      var st, tone, ref = 'Under 120 / under 80';
      if (s.sys >= 180 || s.dia >= 120) { st = 'Very high, seek care today'; tone = 'rose'; }
      else if (s.sys >= 140 || s.dia >= 90) { st = 'High (stage 2 range)'; tone = 'rose'; }
      else if (s.sys >= 130 || s.dia >= 80) { st = 'High (stage 1 range)'; tone = 'amber'; }
      else if (s.sys >= 120) { st = 'Elevated'; tone = 'amber'; }
      else { st = 'Normal'; tone = 'green'; }
      out.push({ k: 'bp', name: 'Blood pressure', val: s.sys + ' / ' + s.dia + ' mmHg', ref: ref, st: st, tone: tone });
    }
    if (s.fbs > 0) {
      var t = s.fbs >= 126 ? ['Diabetes range, confirm with a repeat test', 'rose'] : s.fbs >= 100 ? ['Prediabetes range', 'amber'] : ['Normal', 'green'];
      out.push({ k: 'fbs', name: 'Fasting glucose', val: s.fbs + ' mg/dL', ref: 'Under 100 mg/dL', st: t[0], tone: t[1] });
    }
    if (s.a1c > 0) {
      var t2 = s.a1c >= 6.5 ? ['Diabetes range, confirm with a repeat test', 'rose'] : s.a1c >= 5.7 ? ['Prediabetes range', 'amber'] : ['Normal', 'green'];
      out.push({ k: 'a1c', name: 'HbA1c', val: s.a1c + '%', ref: 'Under 5.7%', st: t2[0], tone: t2[1] });
    }
    if (s.alt > 0) {
      var lim = s.sex === 'f' ? 25 : 33, t3 = s.alt > 40 ? ['Above most lab ranges', 'rose'] : s.alt > lim ? ['Above the healthy limit', 'amber'] : ['Normal', 'green'];
      out.push({ k: 'alt', name: 'SGPT (ALT)', val: s.alt + ' U/L', ref: 'Up to ' + lim + ' U/L healthy, labs often list up to 40', st: t3[0], tone: t3[1] });
    }
    return out;
  }

  function insights(s) {
    var start = [], stop = [], flag = function (k) { return s.marks.some(function (m) { return m.k === k && m.tone !== 'green'; }); };
    var high = s.band.k !== 'normal' && s.band.k !== 'under', liver = flag('alt'), bp = flag('bp'), sugar = flag('fbs') || flag('a1c');
    var anyMarker = s.marks.some(function (m) { return m.tone !== 'green'; });
    // ---- start doing
    if (s.band.k === 'under') start.push(['Eat enough, with protein at every meal', 'Your BMI of ' + r1(s.bmi) + ' is below 18.5. Add an extra meal or snack with dal, eggs, paneer, curd or nuts, and get a check up to rule out thyroid or gut causes.']);
    if (high) start.push(['Set a 5 to 7% weight loss goal over six months', 'That is about ' + s.lose5 + ' to ' + s.lose7 + ' kg for you. Losses this size lower blood pressure, blood sugar and liver fat, even before you reach the healthy range of ' + s.wLo + ' to ' + s.wHi + ' kg.']);
    if (s.exMin < 150) start.push(['Build to 150 minutes of cardio a week', 'You do about ' + s.exMin + ' minutes now. Brisk walking, cycling or swimming, 30 minutes on five days, is the WHO minimum for heart health, blood pressure and weight control.']);
    if (s.str < 2) start.push(['Strength train twice a week', 'Bodyweight squats, push ups or weights on two days build muscle, which burns sugar and protects joints. It matters more after 30.']);
    if (s.steps < 7000) start.push(['Track your daily steps', 'You are near ' + s.steps.toLocaleString('en-IN') + ' steps. Aim for 7,000 to 10,000 on your phone or your insurer\'s wellness app, where steps often earn reward points or premium discounts.']);
    if (s.sleep < 7) start.push(['Sleep 7 to 9 hours on a fixed schedule', 'You sleep about ' + s.sleep + ' hours. Short sleep raises hunger hormones and blood pressure and makes weight loss harder.']);
    if (s.veg < 5 || high || liver || sugar) start.push(['Eat a high fibre, anti inflammatory plate', 'Half the plate vegetables, a quarter protein, a quarter whole grains or millets, plus nuts, seeds and olive or mustard oil. This pattern supports liver, sugar and weight targets.']);
    if (bp) start.push(['Log your blood pressure at home', 'Your reading of ' + s.sys + ' / ' + s.dia + ' needs a pattern, not a one off. Measure twice in the morning and evening for two weeks, seated and rested, and share the log with your doctor.']);
    if (bp) start.push(['Cut salt to under 5 g a day', 'That is one level teaspoon in total, including pickles, papad, namkeen and packaged food. Salt is the fastest dietary lever on blood pressure.']);
    if (sugar) start.push(['Walk 10 to 15 minutes after main meals', 'A short walk after eating blunts the glucose spike. Repeat your fasting glucose and HbA1c in three months.']);
    if (liver) start.push(['Plan a liver follow up', 'SGPT of ' + s.alt + ' U/L is above the healthy limit. Ask your doctor about an ultrasound for fatty liver and a repeat liver function test in 8 to 12 weeks.']);
    if (s.waistFlag) start.push(['Measure your waist every month', 'Your waist is ' + s.waist + ' cm, ratio ' + s.whtr.toFixed(2) + ' to height. Indian guidelines flag belly fat at ' + (s.sex === 'f' ? '80' : '90') + ' cm or a ratio above 0.5, because it drives diabetes and heart risk at lower weights.']);
    if (s.age >= 30 && !anyMarker) start.push(['Book a yearly health check', 'Blood pressure, fasting glucose, HbA1c, lipids and liver function once a year catch changes early. Most insurers cover one free check a year.']);
    start.push(['Drink water through the day', 'About 2 to 3 litres, more in summer or on workout days. Keep a bottle at your desk and swap one tea or coffee for water.']);
    // ---- stop doing
    if (s.sit >= 6) stop.push(['Sitting for hours at a stretch', 'You sit about ' + s.sit + ' hours a day. Stand, stretch or walk for 3 to 5 minutes every hour; set a timer or use a standing call.']);
    if (s.sugary > 0) stop.push(['Sugary drinks and sweetened tea or coffee', s.sugary + ' a week adds empty calories that raise blood sugar, liver fat and belly fat. Switch to water, plain buttermilk, lemon water or unsweetened tea.']);
    if (high || liver || sugar) stop.push(['Refined carbs and packaged snacks', 'Maida, white bread, biscuits, chips and fried namkeen drive visceral fat and raise liver enzymes. Swap for fruit, roasted chana, nuts or makhana.']);
    if (s.smoke) stop.push(['Smoking or vaping', 'It is the single biggest avoidable risk to your heart and lungs. India\'s free National Tobacco Quit Line is 1800 112 356.']);
    if (s.alc > 0 && (liver || s.alc > 7)) stop.push(['Regular alcohol', liver ? 'With SGPT above the healthy limit, keep alcohol at zero until your doctor reviews a repeat test.' : s.alc + ' drinks a week is above low risk levels. Cut to a few a week with alcohol free days.']);
    if (s.sleep < 7) stop.push(['Screens in the last hour before bed', 'Phone and TV light delays sleep. Charge your phone outside the bedroom.']);
    if (s.late) stop.push(['Late, heavy dinners', 'Eating within two hours of sleep worsens acid reflux, sleep quality and morning sugar. Finish dinner by 8 or 8:30 PM.']);
    if (high) stop.push(['Crash diets and skipped meals', 'They cost muscle and rebound fast. Aim for a steady 0.5 kg a week.']);
    if (anyMarker) stop.push(['Self diagnosis and delayed follow ups', 'Do not ignore the readings flagged above. Book a physician visit with your reports so they can be read together with your history.']);
    if (!stop.length) stop.push(['Assuming a good BMI means healthy', 'BMI misses belly fat and fitness. Keep the habits below going and check your markers yearly.']);
    return { start: start, stop: stop };
  }

  function habits(s) {
    var h = [
      ['steps', 'Walk ' + (s.steps < 7000 ? '7,000' : '10,000') + ' steps'],
      ['move', '30 minutes of exercise'],
      ['sleep', '7 hours of sleep'],
      ['plate', 'Five servings of vegetables or fruit'],
      ['nosugar', 'No sugary drinks'],
      ['stand', 'Stand up every hour at work'],
      ['water', '2 to 3 litres of water']
    ];
    if (s.marks.some(function (m) { return m.k === 'bp' && m.tone !== 'green'; })) h.push(['bplog', 'Log blood pressure']);
    else if (s.marks.some(function (m) { return (m.k === 'fbs' || m.k === 'a1c') && m.tone !== 'green'; })) h.push(['walkmeal', 'Walk after lunch and dinner']);
    else h.push(['dinner', 'Dinner done by 8:30 PM']);
    return h;
  }

  function calc() {
    var h = num('ht'), w = num('wt'), age = num('age'), sex = ($('sex') || {}).value || 'm';
    if (!(h > 90 && h < 250) || !(w > 20 && w < 350)) return null;
    var m = h / 100, bmi = w / (m * m), band = bandIndia(bmi);
    var waist = num('waist'), whtr = waist > 0 ? waist / h : NaN;
    var s = {
      ht: h, wt: w, age: isFinite(age) ? age : 30, sex: sex, bmi: bmi, band: band, who: bandWHO(bmi),
      wLo: Math.round(18.5 * m * m), wHi: Math.round(22.9 * m * m),
      waist: waist > 0 ? waist : 0, whtr: isFinite(whtr) ? whtr : 0,
      steps: num('steps') || 0, exMin: num('exmin') || 0, str: num('str') || 0, sleep: num('sleep') || 0, sit: num('sit') || 0,
      veg: num('veg') || 0, sugary: num('sugary') || 0, alc: num('alc') || 0, smoke: ($('smoke') || {}).checked, late: ($('late') || {}).checked,
      sys: num('sys') || 0, dia: num('dia') || 0, fbs: num('fbs') || 0, a1c: num('a1c') || 0, alt: num('alt') || 0
    };
    s.waistFlag = s.waist > 0 && ((s.sex === 'f' ? s.waist >= 80 : s.waist >= 90) || s.whtr > 0.5);
    s.toTarget = bmi >= 23 ? Math.max(0, Math.round((w - s.wHi) * 10) / 10) : bmi < 18.5 ? Math.round((s.wLo - w) * 10) / 10 : 0;
    s.lose5 = Math.round(w * 0.05 * 10) / 10; s.lose7 = Math.round(w * 0.07 * 10) / 10;
    s.marks = markers(s);
    var ins = insights(s); s.start = ins.start; s.stop = ins.stop;
    s.habits = habits(s);
    s.stage2 = bmi > 23 && s.waistFlag;
    return s;
  }

  // ---------- tracker (saved on this device only)
  var KEY = 'sh_bmi_tracker_v1';
  function weekId() { var d = new Date(), day = (d.getDay() + 6) % 7; d.setDate(d.getDate() - day); return d.toISOString().slice(0, 10); }
  function loadTicks() { var t = store.get(KEY); if (!t || t.week !== weekId()) t = { week: weekId(), ticks: {} }; return t; }
  function renderTracker(s) {
    var t = loadTicks(), today = (new Date().getDay() + 6) % 7;
    var head = '<tr><th>Habit</th>' + DAYS.map(function (d, i) { return '<th' + (i === today ? ' class="today"' : '') + '>' + d + '</th>'; }).join('') + '<th>Week</th></tr>';
    var done = 0, total = s.habits.length * 7;
    var rows = s.habits.map(function (h) {
      var tk = t.ticks[h[0]] || [], n = 0;
      var cells = DAYS.map(function (d, i) { var on = !!tk[i]; if (on) n++; return '<td><button type="button" class="tk' + (on ? ' on' : '') + (i === today ? ' today' : '') + '" data-h="' + h[0] + '" data-d="' + i + '" aria-pressed="' + on + '" aria-label="' + esc(h[1]) + ', ' + d + '">' + (on ? '&#10003;' : '') + '</button></td>'; }).join('');
      done += n;
      return '<tr><th scope="row">' + esc(h[1]) + '</th>' + cells + '<td class="wk">' + n + '/7</td></tr>';
    }).join('');
    $('trk').innerHTML = '<table><thead>' + head + '</thead><tbody>' + rows + '</tbody></table>';
    var pct = Math.round(done / total * 100);
    $('trkScore').textContent = pct + '%';
    $('trkBar').style.width = pct + '%';
    $('trkNote').textContent = done === 0 ? 'Tap a box each day you hit the habit. Ticks stay on this device and reset every Monday.' : pct >= 80 ? 'Strong week. Keep the streak and add one harder target next week.' : pct >= 50 ? 'Good base. Pick the two habits with the fewest ticks and protect them tomorrow.' : 'Start small. Two habits done daily beat eight done once.';
    s.tracker = { week: t.week, pct: pct, rows: s.habits.map(function (h) { var tk = t.ticks[h[0]] || []; return [h[1]].concat(DAYS.map(function (_, i) { return tk[i] ? 'Done' : ''; })); }) };
  }

  var BAND_CLASS = { under: 'b-under', normal: 'b-ok', over: 'b-over', obese1: 'b-ob', obese2: 'b-ob' };
  function render() {
    var s = calc(), out = $('out');
    if (!s) { out.classList.add('dim'); return; }
    out.classList.remove('dim');
    $('oBmi').textContent = r1(s.bmi);
    var b = $('oBand'); b.textContent = s.band.name; b.className = 'bm-band ' + BAND_CLASS[s.band.k];
    $('oBmiS').textContent = 'Asian Indian bands. WHO category: ' + s.who + '.';
    // gauge 15 to 35
    var pos = Math.max(0, Math.min(100, (s.bmi - 15) / 20 * 100));
    $('gPin').style.left = pos + '%';
    $('oRange').textContent = s.wLo + ' to ' + s.wHi + ' kg';
    $('oRangeS').textContent = s.toTarget > 0 ? (s.bmi < 18.5 ? 'gain about ' + s.toTarget + ' kg to reach it' : 'about ' + s.toTarget + ' kg above the top of the range') : 'you are inside it';
    $('oWhtr').textContent = s.whtr ? s.whtr.toFixed(2) : 'Add waist';
    $('oWhtrS').textContent = s.whtr ? (s.waistFlag ? 'belly fat flag: aim for 0.5 or less' : 'healthy, 0.5 or less') : 'measure at the navel, relaxed';
    $('oGoal').textContent = s.bmi >= 23 ? s.lose5 + ' to ' + s.lose7 + ' kg' : s.bmi < 18.5 ? '+' + s.toTarget + ' kg' : 'Maintain';
    $('oGoalS').textContent = s.bmi >= 23 ? 'first 6 month goal, 5 to 7% of your weight' : s.bmi < 18.5 ? 'to reach BMI 18.5' : 'keep your weight within ' + s.wLo + ' to ' + s.wHi + ' kg';
    var vd = $('vd'); vd.className = 'fr-verdict ' + (s.band.tone === 'green' && !s.waistFlag ? 'ok' : 'no');
    vd.innerHTML = s.band.k === 'normal' && !s.waistFlag ? '<b>BMI ' + r1(s.bmi) + ', in the healthy range for Indian adults.</b> Keep the habits that got you here and check your markers once a year.'
      : s.band.k === 'under' ? '<b>BMI ' + r1(s.bmi) + ', below the healthy range.</b> Focus on enough food, protein and strength work, and see a doctor if weight loss was unplanned.'
        : '<b>BMI ' + r1(s.bmi) + ', ' + s.band.name.toLowerCase() + ' by Indian guidelines' + (s.stage2 ? ', with excess belly fat' : '') + '.</b> A 5 to 7% loss (' + s.lose5 + ' to ' + s.lose7 + ' kg) over six months is the target that moves health numbers most.';
    // markers
    $('mk').innerHTML = s.marks.length ? '<table><thead><tr><th>Marker</th><th>Your value</th><th>Reference</th><th>Status</th></tr></thead><tbody>' + s.marks.map(function (m) { return '<tr><td>' + m.name + '</td><td>' + m.val + '</td><td>' + m.ref + '</td><td><span class="chip c-' + m.tone + '">' + m.st + '</span></td></tr>'; }).join('') + '</tbody></table>' : '<p class="fr-hint">Add any reading from a recent report in step 3 to see it scored here.</p>';
    // insights table
    $('ins').innerHTML = '<table class="ins-t"><thead><tr><th class="st">What you should start doing</th><th>Why it matters for you</th></tr></thead><tbody>' + s.start.map(function (r) { return '<tr><td><b>' + esc(r[0]) + '</b></td><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>'
      + '<table class="ins-t stop"><thead><tr><th class="sp">What you should stop doing</th><th>Why it matters for you</th></tr></thead><tbody>' + s.stop.map(function (r) { return '<tr><td><b>' + esc(r[0]) + '</b></td><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>';
    renderTracker(s);
    var mb = $('mN'); if (mb) mb.textContent = r1(s.bmi) + ' · ' + s.band.name;
    window.__calc = Object.assign({ kind: 'bmi' }, s);
    try { var q = new URLSearchParams(); ['ht', 'wt', 'age', 'sex', 'waist', 'steps', 'exmin', 'str', 'sleep', 'sit', 'veg', 'sugary', 'alc'].forEach(function (k) { var e = $(k); if (e && String(e.value).trim() !== '') q.set(k, e.value); }); ['smoke', 'late'].forEach(function (k) { if ($(k).checked) q.set(k, '1'); }); history.replaceState(null, '', '?' + q.toString()); } catch (e) { }
  }

  document.addEventListener('DOMContentLoaded', function () {
    try {
      var p = new URLSearchParams(location.search);
      ['ht', 'wt', 'age', 'sex', 'waist', 'steps', 'exmin', 'str', 'sleep', 'sit', 'veg', 'sugary', 'alc'].forEach(function (k) { if (p.has(k) && $(k)) $(k).value = p.get(k); });
      ['smoke', 'late'].forEach(function (k) { if (p.get(k) === '1') $(k).checked = true; });
    } catch (e) { }
    // health markers are never put in the URL
    document.querySelectorAll('#bmForm input, #bmForm select').forEach(function (i) { i.addEventListener(i.type === 'checkbox' || i.tagName === 'SELECT' ? 'change' : 'input', render); });
    $('trk').addEventListener('click', function (e) {
      var b = e.target.closest('.tk'); if (!b) return;
      var t = loadTicks(), h = b.dataset.h, d = +b.dataset.d; t.ticks[h] = t.ticks[h] || []; t.ticks[h][d] = !t.ticks[h][d]; store.set(KEY, t); render();
    });
    $('trkReset').addEventListener('click', function () { store.set(KEY, { week: weekId(), ticks: {} }); render(); });
    $('share').addEventListener('click', function () {
      var b = $('share'), o = b.textContent, url = location.href;
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { b.textContent = 'Link copied'; setTimeout(function () { b.textContent = o; }, 1800); }, function () { window.prompt('Copy this link', url); });
    });
    render();
  });
})();
