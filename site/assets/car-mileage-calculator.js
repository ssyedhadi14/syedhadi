/* Created by: Claude
   Date: 2026-11-02
   Purpose: Car mileage and running cost calculator (fuel per month, cost by city fuel price, tank range, service reserve) for syedcreates.com
   Owner: Syed Hadi */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var CITIES = [
    { k: 'delhi', name: 'Delhi', price: 102.00 },
    { k: 'blr', name: 'Bengaluru', price: 110.93 },
    { k: 'hyd', name: 'Hyderabad', price: 116.50 }
  ];
  var f0 = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };
  var f2 = function (n, d) { return n.toLocaleString('en-IN', { maximumFractionDigits: d == null ? 2 : d, minimumFractionDigits: d == null ? 2 : d }); };
  var num = function (id) { var v = parseFloat(String($(id).value).replace(/[^0-9.]/g, '')); return isFinite(v) ? v : 0; };
  var pct = function (n) { return (n * 100).toFixed(0) + '%'; };

  function calc() {
    var car = ($('car').value || 'My car').trim();
    var km = num('km'), kmpl = num('kmpl'), price = num('price'), tank = num('tank');
    var service = num('service'), wear = num('wear'), ins = num('ins');
    if (!(km > 0) || !(kmpl > 0) || !(price > 0)) return null;
    var litres = km / kmpl, fuelM = litres * price, fuelY = fuelM * 12;
    var range = tank > 0 ? tank * kmpl : 0, refuels = tank > 0 ? litres / tank : 0;
    var fixedY = service + wear + ins, fixedM = fixedY / 12;
    var totalM = fuelM + fixedM, totalY = fuelY + fixedY;
    var perKm = totalM / km, fuelPerKm = price / kmpl;
    var cities = CITIES.map(function (c) { return { name: c.name, price: c.price, m: litres * c.price, y: litres * c.price * 12 }; });
    var lo = cities.reduce(function (a, b) { return a.price < b.price ? a : b; }), hi = cities.reduce(function (a, b) { return a.price > b.price ? a : b; });
    // what if: mileage +2 km/l, drive 10% less
    var betterKmpl = (km / (kmpl + 2)) * price, less = (km * 0.9 / kmpl) * price;
    return { car: car, km: km, kmpl: kmpl, price: price, tank: tank, service: service, wear: wear, ins: ins,
      litres: litres, fuelM: fuelM, fuelY: fuelY, range: range, refuels: refuels, fixedY: fixedY, fixedM: fixedM,
      totalM: totalM, totalY: totalY, perKm: perKm, fuelPerKm: fuelPerKm, cities: cities, lo: lo, hi: hi,
      saveKmpl: fuelM - betterKmpl, saveLess: fuelM - less, kmY: km * 12 };
  }

  function bars(s) {
    var svg = $('chart'); if (!svg) return;
    var W = 640, H = 230, L = 70, R = 16, T = 18, B = 42, pw = W - L - R, ph = H - T - B;
    var max = Math.max.apply(null, s.cities.map(function (c) { return c.m; })) * 1.15;
    var n = s.cities.length, slot = pw / n, bw = slot * 0.56;
    var out = '';
    for (var g = 0; g <= 4; g++) { var v = max / 4 * g, y = T + ph - ph * g / 4; out += '<line x1="' + L + '" y1="' + y + '" x2="' + (W - R) + '" y2="' + y + '" class="grid"/><text x="' + (L - 8) + '" y="' + (y + 4) + '" class="tk" text-anchor="end">' + f0(v) + '</text>'; }
    s.cities.forEach(function (c, i) {
      var h = c.m / max * ph, x = L + slot * i + (slot - bw) / 2, y = T + ph - h;
      var me = Math.abs(c.price - s.price) < 0.5;
      out += '<rect x="' + x + '" y="' + y + '" width="' + bw + '" height="' + h + '" rx="6" class="' + (me ? 'me' : 'b') + '"/>';
      out += '<text x="' + (x + bw / 2) + '" y="' + (y - 6) + '" class="vl" text-anchor="middle">' + f0(c.m) + '</text>';
      out += '<text x="' + (x + bw / 2) + '" y="' + (T + ph + 16) + '" class="tk" text-anchor="middle">' + c.name + '</text>';
      out += '<text x="' + (x + bw / 2) + '" y="' + (T + ph + 30) + '" class="tk2" text-anchor="middle">₹' + c.price.toFixed(2) + '/L</text>';
    });
    svg.innerHTML = out;
  }

  function render() {
    var s = calc(); var out = $('out'); if (!s) { out.classList.add('dim'); return; } out.classList.remove('dim');
    $('oLit').textContent = f2(s.litres, 1) + ' L';
    $('oLitS').textContent = f2(s.km, 0) + ' km ÷ ' + f2(s.kmpl, 1) + ' km/L';
    $('oFuel').textContent = f0(s.fuelM);
    $('oFuelS').textContent = 'at ₹' + f2(s.price) + ' per litre, ' + f0(s.fuelY) + ' a year';
    $('oTotal').textContent = f0(s.totalM);
    $('oTotalS').textContent = 'fuel + service and wear reserve' + (s.ins ? ' + insurance' : '');
    $('oYear').textContent = f0(s.totalY);
    $('oYearS').textContent = f0(s.fuelY) + ' fuel + ' + f0(s.fixedY) + ' fixed';
    $('oKm').textContent = '₹' + f2(s.perKm, 2);
    $('oKmS').textContent = 'fuel alone ₹' + f2(s.fuelPerKm, 2) + ' per km';
    $('oRange').textContent = s.range ? f2(s.range, 0) + ' km' : '-';
    $('oRangeS').textContent = s.range ? 'full tank of ' + f2(s.tank, 0) + ' L, about ' + f2(s.refuels, 1) + ' fill ups a month' : 'add your tank size';
    $('vd').innerHTML = '<b>' + s.car + '</b> at ' + f2(s.km, 0) + ' km a month burns <b>' + f2(s.litres, 1) + ' litres</b>. That is <b>' + f0(s.fuelM) + '</b> of fuel a month in your city, between ' + f0(s.lo.m) + ' (' + s.lo.name + ') and ' + f0(s.hi.m) + ' (' + s.hi.name + ') across metros. Add the yearly service reserve and the car costs <b>' + f0(s.totalM) + ' a month</b> to run, roughly ₹' + f2(s.perKm, 2) + ' per km.';
    $('tip').innerHTML = 'Two levers: squeeze 2 more km per litre (tyre pressure, smoother throttle, less idling) and you save <b>' + f0(s.saveKmpl) + ' a month</b>. Drive 10% less and you save <b>' + f0(s.saveLess) + '</b>.';
    bars(s);
    var m = $('mN'); if (m) m.textContent = f0(s.totalM) + '/mo';
    window.__calc = Object.assign({ kind: 'car' }, s);
    try { var q = new URLSearchParams({ car: s.car, km: s.km, kmpl: s.kmpl, price: s.price, tank: s.tank, service: s.service, wear: s.wear, ins: s.ins }); history.replaceState(null, '', '?' + q.toString()); } catch (e) { }
  }

  function setCity(k) {
    var c = CITIES.filter(function (x) { return x.k === k; })[0]; if (!c) return;
    $('price').value = c.price.toFixed(2);
    document.querySelectorAll('.cm-city button').forEach(function (b) { b.classList.toggle('on', b.dataset.k === k); });
    render();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var cm = $('cityChips');
    cm.innerHTML = CITIES.map(function (c) { return '<button type="button" data-k="' + c.k + '"' + (c.k === 'blr' ? ' class="on"' : '') + '>' + c.name + ' <small>₹' + c.price.toFixed(2) + '</small></button>'; }).join('');
    cm.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) setCity(b.dataset.k); });
    try {
      var p = new URLSearchParams(location.search);
      ['car', 'km', 'kmpl', 'price', 'tank', 'service', 'wear', 'ins'].forEach(function (k) { if (p.has(k) && $(k)) $(k).value = p.get(k); });
      if (p.has('price')) document.querySelectorAll('.cm-city button').forEach(function (b) { b.classList.remove('on'); });
    } catch (e) { }
    document.querySelectorAll('#cmForm input').forEach(function (i) { i.addEventListener('input', function () { if (i.id === 'price') document.querySelectorAll('.cm-city button').forEach(function (b) { b.classList.remove('on'); }); render(); }); });
    $('share').addEventListener('click', function () {
      var b = $('share'), o = b.textContent, url = location.href;
      var done = function (msg) { b.textContent = msg; setTimeout(function () { b.textContent = o; }, 1800); };
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { done('Link copied'); }, function () { window.prompt('Copy this link', url); });
    });
    render();
  });
})();
