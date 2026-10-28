/* EverydayKit shared calculator logic.
   Pure functions are exported for Node tests and attached to window for pages. */
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  root.EverydayKit = api;
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function pctOf(p, x) { return (p / 100) * x; }
  function whatPctOf(x, y) { return y === 0 ? NaN : (x / y) * 100; }
  function pctChange(a, b) { return a === 0 ? NaN : ((b - a) / Math.abs(a)) * 100; }

  function parseDay(s) { // 'YYYY-MM-DD' -> Date at local midnight
    var p = s.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }

  function ageParts(dobISO, asOfISO) {
    var dob = parseDay(dobISO);
    var asof = asOfISO ? parseDay(asOfISO) : new Date();
    asof = new Date(asof.getFullYear(), asof.getMonth(), asof.getDate());
    if (asof < dob) return null;
    var y = asof.getFullYear() - dob.getFullYear();
    var m = asof.getMonth() - dob.getMonth();
    var d = asof.getDate() - dob.getDate();
    if (d < 0) { m--; d += new Date(asof.getFullYear(), asof.getMonth(), 0).getDate(); }
    if (m < 0) { y--; m += 12; }
    var totalDays = Math.round((asof - dob) / 86400000);
    return { years: y, months: m, days: d, totalDays: totalDays };
  }

  function daysBetween(aISO, bISO) {
    var a = parseDay(aISO), b = parseDay(bISO);
    return Math.round((b - a) / 86400000);
  }

  function salaryAnnual(hourly, hoursPerWeek, weeksPerYear) {
    return hourly * hoursPerWeek * weeksPerYear;
  }
  function salaryBreakdown(hourly, hoursPerWeek, weeksPerYear) {
    var annual = salaryAnnual(hourly, hoursPerWeek, weeksPerYear);
    return { annual: annual, monthly: annual / 12, weekly: annual / 52, daily: annual / 52 / 5 };
  }

  var LINEAR = {
    length: { m: 1, km: 1000, cm: 0.01, mm: 0.001, mi: 1609.344, yd: 0.9144, ft: 0.3048, in: 0.0254 },
    weight: { kg: 1, g: 0.001, t: 1000, lb: 0.45359237, oz: 0.028349523125 },
    volume: { l: 1, ml: 0.001, gal: 3.785411784, 'fl oz': 0.0295735295625, cup: 0.2365882365 }
  };
  function convertLinear(value, from, to, category) {
    var t = LINEAR[category];
    if (!t || !(from in t) || !(to in t)) return NaN;
    return value * t[from] / t[to];
  }
  function convertTemp(value, from, to) {
    var c = from === 'c' ? value : from === 'f' ? (value - 32) * 5 / 9 : value - 273.15;
    return to === 'c' ? c : to === 'f' ? c * 9 / 5 + 32 : c + 273.15;
  }

  /* ---- Square footage ---- */
  var FT_PER_M = 3.280839895;
  function toFeet(value, unit) { // unit: 'ft' | 'in' | 'm'
    if (unit === 'in') return value / 12;
    if (unit === 'm') return value * FT_PER_M;
    return value;
  }
  function areaSqFt(shape, d1, d2) { // dims already in feet; circle d1 = diameter, triangle d1 = base, d2 = height
    if (shape === 'circle') { var r = d1 / 2; return Math.PI * r * r; }
    if (shape === 'triangle') return d1 * d2 / 2;
    return d1 * d2; // rectangle
  }
  function sqftConvert(sqft) {
    return { sqft: sqft, sqm: sqft * 0.09290304, sqyd: sqft / 9 };
  }

  /* ---- Concrete ---- */
  var BAG_YIELDS = { 40: 0.30, 50: 0.375, 60: 0.45, 80: 0.60 }; // cubic feet per bag
  function concreteCuFt(lengthFt, widthFt, thicknessIn) {
    return lengthFt * widthFt * (thicknessIn / 12);
  }
  function cuFtTo(cuft) {
    return { cuft: cuft, cuyd: cuft / 27, cum: cuft * 0.0283168466 };
  }
  function bagsNeeded(cuftWithWaste, bagLb) {
    return Math.ceil(cuftWithWaste / BAG_YIELDS[bagLb]);
  }

  /* ---- Word counter ---- */
  var READING_WPM = 238, SPEAKING_WPM = 130;
  function textStats(text) {
    var t = text || '';
    var trimmed = t.trim();
    var wordsArr = trimmed ? trimmed.split(/\s+/) : [];
    var words = wordsArr.length;
    var sentences = 0;
    if (trimmed) {
      sentences = t.split(/[.!?]+/).filter(function (s) { return s.trim().length > 0; }).length;
    }
    var paragraphs = 0;
    if (trimmed) {
      paragraphs = t.split(/\n+/).filter(function (s) { return s.trim().length > 0; }).length;
    }
    var freq = {};
    wordsArr.forEach(function (w) {
      var key = w.toLowerCase().replace(/^[^a-z0-9']+|[^a-z0-9']+$/g, '');
      if (key.length >= 3) freq[key] = (freq[key] || 0) + 1;
    });
    var top = Object.keys(freq).map(function (k) { return { word: k, count: freq[k] }; })
      .sort(function (a, b) { return b.count - a.count || (a.word < b.word ? -1 : 1); })
      .slice(0, 5);
    return {
      words: words,
      chars: t.length,
      charsNoSpaces: t.replace(/\s/g, '').length,
      sentences: sentences,
      paragraphs: paragraphs,
      readingSeconds: words / READING_WPM * 60,
      speakingSeconds: words / SPEAKING_WPM * 60,
      readingWpm: READING_WPM,
      speakingWpm: SPEAKING_WPM,
      topWords: top
    };
  }

  /* ---- GPA / CGPA ---- */
  var GRADE_POINTS = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0
  };
  function computeGPA(courses) { // [{grade:'A', credits:3}, ...]
    var qp = 0, cr = 0;
    (courses || []).forEach(function (c) {
      var p = GRADE_POINTS[c.grade];
      if (p === undefined || !(c.credits > 0)) return;
      qp += p * c.credits; cr += c.credits;
    });
    return { qualityPoints: qp, credits: cr, gpa: cr > 0 ? qp / cr : NaN };
  }
  function computeCGPA(currentCgpa, creditsDone, semesterGpa, semesterCredits) {
    var totalCr = creditsDone + semesterCredits;
    var qp = currentCgpa * creditsDone + semesterGpa * semesterCredits;
    return { cgpa: totalCr > 0 ? qp / totalCr : NaN, credits: totalCr, qualityPoints: qp };
  }
  // 10-point scale ONLY (common CBSE-style approximation; NOT for a 4.0 GPA)
  function cgpaToPercent10(cgpa10) { return cgpa10 * 9.5; }
  function percentToCgpa10(pct) { return pct / 9.5; }

  /* ---- Tip calculator ---- */
  function tipCalc(bill, tipPct, taxPct, tipOn, people) { // tipOn: 'before' | 'after'
    var tax = bill * (taxPct || 0) / 100;
    var base = tipOn === 'after' ? bill + tax : bill;
    var tip = base * tipPct / 100;
    var total = bill + tax + tip;
    var n = people > 0 ? people : 1;
    return { tax: tax, tip: tip, total: total, perPerson: total / n, tipPerPerson: tip / n };
  }

  /* ---- Date breakdown (weeks, business days, weekend days) ---- */
  function dateBreakdown(aISO, bISO) {
    var days = daysBetween(aISO, bISO);
    var ad = Math.abs(days);
    var lo = days >= 0 ? parseDay(aISO) : parseDay(bISO);
    var biz = 0, wknd = 0;
    for (var i = 1; i <= ad; i++) {
      var dow = new Date(lo.getFullYear(), lo.getMonth(), lo.getDate() + i).getDay();
      if (dow === 0 || dow === 6) wknd++; else biz++;
    }
    return { days: ad, weeks: Math.floor(ad / 7), remDays: ad % 7, businessDays: biz, weekendDays: wknd };
  }

  return {
    pctOf: pctOf, whatPctOf: whatPctOf, pctChange: pctChange,
    ageParts: ageParts, daysBetween: daysBetween,
    salaryAnnual: salaryAnnual, salaryBreakdown: salaryBreakdown,
    convertLinear: convertLinear, convertTemp: convertTemp, LINEAR: LINEAR,
    toFeet: toFeet, areaSqFt: areaSqFt, sqftConvert: sqftConvert,
    BAG_YIELDS: BAG_YIELDS, concreteCuFt: concreteCuFt, cuFtTo: cuFtTo, bagsNeeded: bagsNeeded,
    textStats: textStats,
    GRADE_POINTS: GRADE_POINTS, computeGPA: computeGPA, computeCGPA: computeCGPA,
    cgpaToPercent10: cgpaToPercent10, percentToCgpa10: percentToCgpa10,
    tipCalc: tipCalc, dateBreakdown: dateBreakdown
  };
}));
