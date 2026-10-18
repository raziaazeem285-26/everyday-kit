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

  return {
    pctOf: pctOf, whatPctOf: whatPctOf, pctChange: pctChange,
    ageParts: ageParts, daysBetween: daysBetween,
    salaryAnnual: salaryAnnual, salaryBreakdown: salaryBreakdown,
    convertLinear: convertLinear, convertTemp: convertTemp, LINEAR: LINEAR
  };
}));
