#!/usr/bin/env python3
"""Build the EverydayKit static site (free online tools).

Generates into this directory:
  index.html, percentage-calculator.html, age-calculator.html,
  date-difference.html, salary-calculator.html, unit-converter.html,
  square-footage-calculator.html, concrete-calculator.html,
  word-counter.html, gpa-calculator.html, tip-calculator.html,
  about.html, contact.html, privacy-policy.html,
  styles.css, js/calculators.js, sitemap.xml, robots.txt, vercel.json

English UI, mobile-first, SEO meta + JSON-LD per page, clean URLs via
vercel.json rewrites (explicit per-path only).
"""
import os, json, html

SITE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://everyday-kit.pages.dev"  # Cloudflare Pages is the decided home (fixed Oct 30, 2026)

NAV_LINKS = [
    ("percentage-calculator", "Percentage Calculator"),
    ("age-calculator", "Age Calculator"),
    ("date-difference", "Date Difference"),
    ("salary-calculator", "Salary Calculator"),
    ("unit-converter", "Unit Converter"),
    ("square-footage-calculator", "Square Footage Calculator"),
    ("concrete-calculator", "Concrete Calculator"),
    ("word-counter", "Word Counter"),
    ("gpa-calculator", "GPA Calculator"),
    ("tip-calculator", "Tip Calculator"),
]

CSS = r"""
:root{
  --indigo:#4f46e5; --indigo-dark:#4338ca; --indigo-soft:#eef2ff;
  --slate:#0f172a; --muted:#64748b; --line:#e2e8f0; --bg:#f8fafc;
  --card:#ffffff; --green:#059669; --radius:16px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Arial,sans-serif;
  color:var(--slate);background:var(--bg);line-height:1.6;font-size:16px}
a{color:var(--indigo);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px}
/* header */
.site-header{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50;
  box-shadow:0 2px 14px rgba(15,23,42,.06)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;min-height:60px;gap:14px}
.brand{font-weight:800;font-size:1.25rem;color:var(--slate);display:flex;align-items:center;gap:8px;flex:none;white-space:nowrap}
.brand .logo{width:32px;height:32px;flex:none;border-radius:9px;background:linear-gradient(135deg,var(--indigo),#818cf8);
  display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:17px}
nav.main{display:flex;gap:4px;align-items:center}
nav.main>a,.drop-btn{color:var(--slate);font-weight:600;padding:9px 13px;border-radius:10px;font-size:.95rem;white-space:nowrap}
nav.main>a:hover,.drop-btn:hover{background:var(--indigo-soft);text-decoration:none;color:var(--indigo-dark)}
.has-drop{position:relative}
.drop-btn{background:none;border:none;font-family:inherit;cursor:pointer;display:inline-flex;align-items:center;gap:5px;min-height:44px}
.drop-btn .car{font-size:.7rem;transition:transform .25s ease}
.has-drop:hover .car,.has-drop:focus-within .car{transform:rotate(180deg)}
.dropdown{position:absolute;top:calc(100% + 8px);left:50%;transform:translate(-50%,8px);width:560px;max-width:94vw;
  background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 24px 50px rgba(15,23,42,.16);
  padding:10px;display:grid;grid-template-columns:1fr 1fr;gap:2px;opacity:0;visibility:hidden;transition:.25s ease;z-index:60}
.has-drop:hover .dropdown,.has-drop:focus-within .dropdown{opacity:1;visibility:visible;transform:translate(-50%,0)}
.dropdown a{color:var(--slate);font-weight:600;padding:10px 12px;border-radius:9px;font-size:.93rem;display:block}
.dropdown a:hover{background:var(--indigo-soft);text-decoration:none;color:var(--indigo-dark)}
.m-tools{display:none}
#navToggle{display:none;background:none;border:1px solid var(--line);border-radius:10px;font-size:1.3rem;
  padding:6px 12px;cursor:pointer;color:var(--slate);min-height:44px;min-width:44px}
/* hero */
.hero{background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#4338ca 100%);color:#fff;padding:60px 0 68px;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;top:-140px;right:-100px;width:420px;height:420px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.22),rgba(255,255,255,0) 65%)}
.hero .wrap{position:relative}
.hero h1{margin:0 0 12px;font-size:2.15rem;line-height:1.2;letter-spacing:-.02em}
.hero p.sub{opacity:.92;font-size:1.08rem;max-width:640px;margin:0 0 22px}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;font-size:.85rem;margin-bottom:26px}
.hero-badges span{background:rgba(255,255,255,.16);padding:6px 14px;border-radius:999px}
.hero-cta{display:inline-flex;align-items:center;gap:8px;background:#fff;color:var(--indigo-dark);font-weight:800;
  padding:14px 28px;border-radius:12px;font-size:1.02rem;min-height:48px;box-shadow:0 10px 24px rgba(0,0,0,.22);
  transition:transform .25s ease,box-shadow .25s ease}
.hero-cta:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 16px 32px rgba(0,0,0,.28);text-decoration:none}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.hero h1{animation:rise .7s ease both}
.hero p.sub{animation:rise .7s .08s ease both}
.hero-badges{animation:rise .7s .16s ease both}
.hero-cta{animation:rise .7s .24s ease both}
/* entrance reveal (JS-gated: content is visible without JS) */
.anim .reveal{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease}
.anim .reveal.in{opacity:1;transform:none}
/* tool cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px;margin:36px 0}
.tool-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:24px;transition:transform .25s ease,box-shadow .25s ease;display:block}
.tool-card:hover{transform:translateY(-5px);box-shadow:0 18px 36px rgba(79,70,229,.16);text-decoration:none}
.tool-card .icon{width:52px;height:52px;border-radius:14px;margin-bottom:12px;color:var(--indigo);
  background:linear-gradient(135deg,var(--indigo-soft),#e0e7ff);display:flex;align-items:center;justify-content:center}
.tool-card .icon svg{width:27px;height:27px}
.tool-card h3{margin:0 0 8px;font-size:1.15rem;color:var(--slate)}
.tool-card p{margin:0;color:var(--muted);font-size:.94rem}
/* tool page layout */
.tool-hero{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;padding:40px 0}
.tool-hero h1{margin:0 0 8px;font-size:1.8rem;letter-spacing:-.02em}
.tool-hero p{margin:0;opacity:.9;max-width:680px}
.calculator{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:26px;margin:-34px 0 30px;box-shadow:0 10px 30px rgba(15,23,42,.08);position:relative}
.field{margin-bottom:16px}
.field label{display:block;font-weight:700;margin-bottom:6px;font-size:.95rem}
.field input,.field select{width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;
  font-size:1rem;font-family:inherit}
.field input:focus,.field select:focus{outline:none;border-color:var(--indigo);box-shadow:0 0 0 3px var(--indigo-soft)}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.btn{background:linear-gradient(135deg,var(--indigo),#7c3aed);color:#fff;border:none;border-radius:12px;
  padding:14px 26px;font-size:1rem;font-weight:700;cursor:pointer;width:100%;min-height:48px;position:relative;
  overflow:hidden;box-shadow:0 8px 20px rgba(79,70,229,.25);transition:transform .25s ease,box-shadow .25s ease}
.btn:hover{transform:translateY(-2px) scale(1.01);box-shadow:0 13px 28px rgba(79,70,229,.32)}
.btn:after{content:"";position:absolute;top:0;left:-80%;width:45%;height:100%;
  background:linear-gradient(105deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);transition:left .5s ease}
.btn:hover:after{left:135%}
.btn-ghost{background:var(--indigo-soft);color:var(--indigo-dark)}
.result{background:#f0fdf4;border:1.5px solid #bbf7d0;border-radius:12px;padding:18px;margin-top:18px;display:none}
.result.show{display:block}
.result .big{font-size:1.9rem;font-weight:800;color:var(--green)}
.result .detail{color:var(--muted);font-size:.92rem;margin-top:6px}
.tabs{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap}
.tabs button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:9px 18px;
  font-weight:700;cursor:pointer;font-size:.92rem;color:var(--slate)}
.tabs button.active{background:var(--indigo);border-color:var(--indigo);color:#fff}
/* dynamic area rows, stat cards, tables, textarea */
.field textarea{width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;
  font-size:1rem;font-family:inherit;min-height:170px;resize:vertical}
.field textarea:focus{outline:none;border-color:var(--indigo);box-shadow:0 0 0 3px var(--indigo-soft)}
.area-row{border:1.5px solid var(--line);border-radius:12px;padding:16px;margin-bottom:14px;background:#fcfcff}
.area-row .area-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.area-row .area-head strong{font-size:.98rem}
.btn-small{background:var(--indigo-soft);color:var(--indigo-dark);border:none;border-radius:10px;
  padding:9px 16px;font-weight:700;cursor:pointer;font-size:.9rem}
.btn-small:hover{background:#e0e7ff}
.btn-danger{background:#fef2f2;color:#b91c1c}
.btn-danger:hover{background:#fee2e2}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(138px,1fr));gap:12px;margin-top:4px}
.stat{background:var(--indigo-soft);border-radius:12px;padding:14px 10px;text-align:center}
.stat .num{font-size:1.45rem;font-weight:800;color:var(--indigo-dark);line-height:1.2}
.stat .lab{font-size:.8rem;color:var(--muted);font-weight:700;margin-top:3px}
table.bagtable{width:100%;border-collapse:collapse;margin-top:10px;font-size:.95rem}
table.bagtable th,table.bagtable td{border:1px solid var(--line);padding:8px 10px;text-align:left}
table.bagtable th{background:var(--indigo-soft)}
.topwords{margin-top:16px}
.topwords li{color:#334155}
/* content sections */
.section{margin:40px 0}
.section h2{font-size:1.45rem;margin:0 0 14px;letter-spacing:-.01em}
.prose{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:26px}
.prose h3{margin:22px 0 8px;font-size:1.1rem}
.prose h3:first-child{margin-top:0}
.prose p,.prose li{color:#334155}
.faq details{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:10px;background:#fff}
.faq summary{font-weight:700;cursor:pointer}
/* network (sister tool kits) */
.network{background:#fff;border-top:1px solid var(--line);padding:34px 0 38px;margin-top:60px}
.network h3{margin:0 0 6px;font-size:1.15rem;color:var(--slate)}
.network p{margin:0 0 16px;color:var(--muted);font-size:.93rem}
.net-row{display:flex;flex-wrap:wrap;gap:10px}
.net-row a{border:1px solid var(--line);background:var(--bg);color:var(--slate);font-weight:700;font-size:.93rem;
  padding:10px 18px;border-radius:999px;transition:transform .25s ease,border-color .25s ease,background .25s ease}
.net-row a:hover{border-color:var(--indigo);background:var(--indigo-soft);color:var(--indigo-dark);transform:translateY(-2px);text-decoration:none}
/* footer */
.site-footer{background:var(--slate);color:#cbd5e1;padding:40px 0}
.site-footer .wrap{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:28px}
.site-footer h4{color:#fff;margin:0 0 12px;font-size:1rem}
.site-footer a{color:#cbd5e1;display:block;margin-bottom:8px;font-size:.93rem}
.site-footer p{font-size:.9rem;margin:0 0 10px}
.bottom-bar{border-top:1px solid #1e293b;margin-top:28px;padding-top:18px;font-size:.85rem;color:#94a3b8}
/* breadcrumbs */
.crumbs{font-size:.85rem;color:var(--muted);margin:18px 0 0}
.crumbs a{color:var(--muted)}
@media(max-width:760px){
  nav.main{display:none;position:absolute;top:60px;left:0;right:0;background:#fff;max-height:calc(100vh - 60px);overflow:auto;
    flex-direction:column;align-items:stretch;padding:10px 18px 18px;border-bottom:1px solid var(--line);
    box-shadow:0 24px 40px rgba(15,23,42,.14)}
  nav.main.open{display:flex}
  nav.main>a{padding:13px 12px}
  .has-drop{display:none}
  .m-tools{display:block;border-top:1px solid var(--line);margin-top:8px;padding-top:10px}
  .m-tools .m-title{display:block;font-weight:800;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;
    color:var(--muted);padding:4px 12px 8px}
  .m-tools a{display:block;color:var(--slate);font-weight:600;padding:11px 12px;border-radius:10px;font-size:.95rem}
  .m-tools a:hover{background:var(--indigo-soft);text-decoration:none}
  #navToggle{display:block}
  .hero h1{font-size:1.65rem}
  .field-row{grid-template-columns:1fr}
  .site-footer .wrap{grid-template-columns:1fr}
  .calculator{margin-top:-24px;padding:20px}
}
@media (prefers-reduced-motion: reduce){
  *,*:before,*:after{animation:none!important;transition:none!important}
  .anim .reveal{opacity:1;transform:none}
  html{scroll-behavior:auto}
}
"""

# Monetag ad tag (zone 12138762) — provided by owner from his Monetag dashboard, Oct 28 2026.
# Loaded in <head> of every page. The sw.js verification file at site root is NOT linked/registered anywhere.
MONETAG_TAG = """<script>(function(s){s.dataset.zone='12138762',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>"""

def page_head(title, desc, path, extra_jsonld=None):
    canon = DOMAIN + ("/" if path == "index" else "/" + path)
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "EverydayKit",
        "url": DOMAIN + "/",
        "description": "Free online tools: calculators and converters for everyday life."
    }
    if extra_jsonld:
        jsonld = extra_jsonld
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta name="theme-color" content="#4f46e5">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{json.dumps(jsonld)}</script>
{MONETAG_TAG}
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R8L6E5KXQ5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-R8L6E5KXQ5');
</script>
</head>
<body>
"""

NETWORK_SITES = [
    ("EverydayKit", "https://everyday-kit.pages.dev"),
    ("ElectricianKit", "https://electrician-kit.pages.dev"),
    ("DentalKit", "https://dental-kit.pages.dev"),
    ("EduKit", "https://study-kit.pages.dev"),
    ("AccountantKit", "https://accountant-kit.pages.dev"),
    ("CreatorKit", "https://creator-kit-93u.pages.dev"),
    ("GovOfficeKit", "https://gov-office-kit.pages.dev"),
    ("SafetyKit", "https://safety-kit.pages.dev"),
    ("TelecomKit", "https://telecom-kit.pages.dev"),
    ("BizOpsKit", "https://bizops-kit.pages.dev"),
]
OWN_BRAND = "EverydayKit"

# Inline SVG icons for tool cards (stroke style; presentation only).
ICONS = {
    "percentage-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18"/><circle cx="7.5" cy="7.5" r="2.4"/><circle cx="16.5" cy="16.5" r="2.4"/></svg>',
    "age-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.4"/><path d="M5 20c.8-3.6 3.6-5.4 7-5.4s6.2 1.8 7 5.4"/></svg>',
    "date-difference": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="6" width="16" height="14" rx="2"/><path d="M4 10.5h16M8 4v4M16 4v4"/></svg>',
    "salary-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="11" rx="2"/><circle cx="12" cy="12.5" r="2.6"/></svg>',
    "unit-converter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4L3.5 7.5 7 11"/><path d="M3.5 7.5H20"/><path d="M17 13l3.5 3.5L17 20"/><path d="M20.5 16.5H4"/></svg>',
    "square-footage-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9h3M4 14h3M9 20v-3M14 20v-3"/></svg>',
    "concrete-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8l8-4 8 4-8 4z"/><path d="M4 12.5l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg>',
    "word-counter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 6h14M5 10h14M5 14h9M5 18h12"/></svg>',
    "gpa-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.7V16c0 1.6 2.5 3 5.5 3s5.5-1.4 5.5-3v-4.3"/><path d="M21.5 9.5V15"/></svg>',
    "tip-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 6.8v10.4M15 8.6c-.6-.9-1.7-1.3-3-1.3-1.7 0-3 .8-3 2.1 0 2.9 6 1.6 6 4.3 0 1.3-1.3 2.1-3 2.1-1.3 0-2.5-.5-3.1-1.5"/></svg>',
}

def card_html(slug, name, icon, desc):
    svg = ICONS.get(slug, icon)
    return (f'<a class="tool-card reveal" href="/{slug}"><div class="icon">{svg}</div>'
            f'<h3>{name}</h3><p>{desc}</p></a>')

_TOOL_LINKS = "\n".join(
    f'      <a href="/{slug}">{name}</a>' for slug, name in NAV_LINKS)
_TOOL_LINKS_M = "\n".join(
    f'      <a href="/{slug}">{name}</a>' for slug, name in NAV_LINKS)

HEADER = f"""<header class="site-header">
<div class="wrap">
  <a class="brand" href="/" style="text-decoration:none"><span class="logo">&#129520;</span> EverydayKit</a>
  <button id="navToggle" aria-label="Menu">&#9776;</button>
  <nav class="main" id="mainNav">
    <a href="/">Home</a>
    <div class="has-drop">
      <button class="drop-btn" type="button" aria-haspopup="true">Tools <span class="car">&#9662;</span></button>
      <div class="dropdown">
{_TOOL_LINKS}
      </div>
    </div>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
    <div class="m-tools">
      <span class="m-title">Tools</span>
{_TOOL_LINKS_M}
    </div>
  </nav>
</div>
</header>
<script>
document.getElementById('navToggle').addEventListener('click',function(){{
  document.getElementById('mainNav').classList.toggle('open');
}});
</script>
"""

def footer():
    tool_links = "\n".join(
        f'    <a href="/{slug}">{name}</a>' for slug, name in NAV_LINKS)
    net_links = "\n".join(
        f'    <a href="{url}" target="_blank" rel="noopener">{name}</a>'
        for name, url in NETWORK_SITES if name != OWN_BRAND)
    network = f"""<section class="network">
<div class="wrap">
  <h3>More Free Tool Kits</h3>
  <p>Explore the rest of our free tool-kit family &mdash; each site is free, needs no sign-up, and runs entirely in your browser.</p>
  <div class="net-row">
{net_links}
  </div>
</div>
</section>
"""
    return network + f"""<footer class="site-footer">
<div class="wrap">
  <div>
    <h4>EverydayKit</h4>
    <p>Free online tools for everyday life. No sign-up, no downloads, no cost &mdash; calculations run instantly in your browser.</p>
  </div>
  <div>
    <h4>Tools</h4>
{tool_links}
  </div>
  <div>
    <h4>Company</h4>
    <a href="/about">About Us</a>
    <a href="/contact">Contact</a>
    <a href="/privacy-policy">Privacy Policy</a>
  </div>
</div>
<div class="wrap bottom-bar">&copy; 2026 EverydayKit. All tools are free to use.</div>
</footer>
<script>
document.documentElement.classList.add('anim');
if('IntersectionObserver' in window){{
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}})}},{{threshold:.12}});
  document.querySelectorAll('.reveal').forEach(function(el){{io.observe(el);}});
}}else{{
  document.querySelectorAll('.reveal').forEach(function(el){{el.classList.add('in');}});
}}
</script>
</body>
</html>
"""

def tool_jsonld(name, desc, path):
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "url": DOMAIN + "/" + path,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": desc,
    }

def tool_jsonld_graph(name, desc, path, faqs):
    """WebApplication + FAQPage graph used by the newer tool pages."""
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "name": name,
                "url": DOMAIN + "/" + path,
                "applicationCategory": "UtilitiesApplication",
                "operatingSystem": "Any",
                "browserRequirements": "Requires JavaScript",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "description": desc,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            },
        ],
    }

def faq_html(items):
    rows = "\n".join(
        f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>"
        for q, a in items)
    return f'<div class="faq">\n{rows}\n</div>'

def write(rel, content):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel, len(content), "bytes")

# ---------------------------------------------------------------- HOME
HOME_CARDS = [
    ("percentage-calculator", "Percentage Calculator", "&#37;",
     "Find X% of a number, what percent one number is of another, and percentage increase or decrease."),
    ("age-calculator", "Age Calculator", "&#127874;",
     "Enter your date of birth to get your exact age in years, months, and days."),
    ("date-difference", "Date Difference Calculator", "&#128197;",
     "Count the days between any two dates &mdash; plan trips, deadlines, and countdowns."),
    ("salary-calculator", "Salary Calculator", "&#128176;",
     "Convert hourly pay to annual, monthly, weekly, and daily salary in seconds."),
    ("unit-converter", "Unit Converter", "&#8646;",
     "Convert length, weight, temperature, and volume units instantly and accurately."),
    ("square-footage-calculator", "Square Footage Calculator", "&#128208;",
     "Measure rooms and floors in square feet, meters, and yards &mdash; with L-shapes, waste allowance, and cost."),
    ("concrete-calculator", "Concrete Calculator", "&#129521;",
     "Work out cubic yards and how many 40, 50, 60, or 80 lb bags you need for a slab, footing, or post hole."),
    ("word-counter", "Word Counter", "&#128221;",
     "Count words, characters, sentences, and reading time as you type &mdash; private, nothing is uploaded."),
    ("gpa-calculator", "GPA Calculator", "&#127891;",
     "Add your courses and grades to get your semester GPA and CGPA on the 4.0 scale &mdash; with a CGPA-to-percentage converter."),
    ("tip-calculator", "Tip Calculator", "&#129534;",
     "Work out the tip and split the bill fairly &mdash; tip amount, total, and each person's share in seconds."),
]

def build_home():
    cards = "\n".join(
        card_html(slug, name, icon, desc)
        for slug, name, icon, desc in HOME_CARDS)
    body = f"""
{HEADER}
<section class="hero">
  <div class="wrap">
    <h1>Free Online Tools for Everyday Life</h1>
    <p class="sub">Fast, accurate, and completely free calculators and converters &mdash; percentages, age, dates, salary, units, square footage, concrete, a word counter, GPA, and a tip calculator. No sign-up required.</p>
    <div class="hero-badges"><span>&#10003; 100% Free</span><span>&#10003; No Sign-Up</span><span>&#10003; Mobile Friendly</span><span>&#10003; Instant Results</span></div>
    <a class="hero-cta" href="#tools">Browse all tools &#8595;</a>
  </div>
</section>
<main class="wrap">
  <div class="grid" id="tools">
{cards}
  </div>
  <section class="section">
    <h2>Why use EverydayKit?</h2>
    <div class="prose">
      <h3>Instant answers, zero friction</h3>
      <p>Every tool works right in your browser. Type a number, get the answer &mdash; no accounts, no downloads, no waiting.</p>
      <h3>Accurate math you can trust</h3>
      <p>Each calculator is tested against known values. Date tools use proper calendar arithmetic, and unit conversions use standard international factors.</p>
      <h3>Works on any device</h3>
      <p>The whole site is designed mobile-first, so every tool feels natural on your phone, tablet, or computer.</p>
    </div>
  </section>
  <section class="section">
    <h2>Frequently asked questions</h2>
    {faq_html([
        ("Is EverydayKit really free?", "Yes. Every tool on EverydayKit is completely free to use, with no account, subscription, or hidden charges."),
        ("Do I need to create an account?", "No. All calculations happen instantly in your browser &mdash; there is nothing to sign up for."),
        ("Does EverydayKit work on mobile?", "Yes. The site is designed mobile-first and every tool works smoothly on phones, tablets, and computers."),
        ("Are the results accurate?", "Yes. Our calculators use standard formulas and are tested against known values. Date calculations use proper calendar arithmetic."),
    ])}
  </section>
</main>
{footer()}"""
    write("index.html",
          page_head("EverydayKit \u2014 Free Online Tools: Calculators & Converters",
                    "Free online tools for everyday life: percentage, age, date difference, salary, and unit calculators, plus square footage, concrete, a word counter, a GPA calculator, and a tip calculator. No sign-up needed.",
                    "index") + body)

# ---------------------------------------------------------------- TOOL PAGES
def tool_page(slug, icon, h1, intro, calc_html, howto, faqs, examples, jsonld=None):
    crumbs = f'<div class="wrap crumbs"><a href="/">Home</a> &rsaquo; {html.escape(h1)}</div>'
    body = f"""
{HEADER}
<section class="tool-hero">
  <div class="wrap">
    <h1>{icon} {html.escape(h1)}</h1>
    <p>{html.escape(intro)}</p>
  </div>
</section>
{crumbs}
<main class="wrap">
  <div class="calculator">
{calc_html}
  </div>
  <section class="section">
    <h2>How to use the {html.escape(h1.lower())}</h2>
    <div class="prose">
{howto}
    </div>
  </section>
  <section class="section">
    <h2>Example</h2>
    <div class="prose">
{examples}
    </div>
  </section>
  <section class="section">
    <h2>Frequently asked questions</h2>
    {faq_html(faqs)}
  </section>
  <section class="section">
    <h2>More free tools</h2>
    <div class="grid">
{"".join(card_html(s, n, i, d)
         for s, n, i, d in HOME_CARDS if s != slug)}
    </div>
  </section>
</main>
{footer()}"""
    write(slug + ".html",
          page_head(f"{h1} \u2014 Free Online | EverydayKit", intro, slug,
                    jsonld if jsonld is not None else tool_jsonld(h1, intro, slug)) + body)

def build_percentage():
    calc = """
    <div class="tabs">
      <button class="active" data-mode="of">What is X% of Y?</button>
      <button data-mode="is">X is what % of Y?</button>
      <button data-mode="change">% increase / decrease</button>
    </div>
    <div class="field-row">
      <div class="field"><label for="pA" id="labelA">Percentage (%)</label><input id="pA" type="number" value="20" step="any"></div>
      <div class="field"><label for="pB" id="labelB">Number</label><input id="pB" type="number" value="150" step="any"></div>
    </div>
    <button class="btn" id="pGo">Calculate</button>
    <div class="result" id="pResult"><div class="big" id="pBig"></div><div class="detail" id="pDetail"></div></div>
    <script>
    (function(){
      var mode='of';
      var labels={of:['Percentage (%)','Number'],is:['Part (X)','Whole (Y)'],change:['Old value','New value']};
      document.querySelectorAll('.tabs button').forEach(function(b){
        b.addEventListener('click',function(){
          document.querySelectorAll('.tabs button').forEach(function(x){x.classList.remove('active')});
          b.classList.add('active'); mode=b.dataset.mode;
          document.getElementById('labelA').textContent=labels[mode][0];
          document.getElementById('labelB').textContent=labels[mode][1];
          calc();
        });
      });
      function calc(){
        var a=parseFloat(document.getElementById('pA').value),
            b=parseFloat(document.getElementById('pB').value),
            r=document.getElementById('pResult');
        if(isNaN(a)||isNaN(b)){r.classList.remove('show');return;}
        var big='',detail='';
        if(mode==='of'){var v=a/100*b;big=fmt(v);detail=a+'% of '+b+' = '+fmt(v);}
        else if(mode==='is'){if(b===0){r.classList.remove('show');return;}
          var v=a/b*100;big=fmt(v)+'%';detail=a+' is '+fmt(v)+'% of '+b;}
        else{if(a===0){r.classList.remove('show');return;}
          var v=(b-a)/Math.abs(a)*100;
          big=(v>=0?'+':'')+fmt(v)+'%';
          detail='Change from '+a+' to '+b+': '+(v>=0?'an increase':'a decrease')+' of '+fmt(Math.abs(v))+'%.';}
        document.getElementById('pBig').textContent=big;
        document.getElementById('pDetail').textContent=detail;
        r.classList.add('show');
      }
      function fmt(n){return (Math.round(n*1000000)/1000000).toString();}
      document.getElementById('pGo').addEventListener('click',calc);
      document.getElementById('pA').addEventListener('input',calc);
      document.getElementById('pB').addEventListener('input',calc);
      calc();
    })();
    </script>"""
    tool_page("percentage-calculator", "&#37;", "Percentage Calculator",
        "Calculate percentages instantly: find X% of a number, see what percent one number is of another, or measure percentage increase and decrease. Free, no sign-up.",
        calc,
        "<h3>Three modes in one tool</h3><p><strong>What is X% of Y?</strong> &mdash; e.g. a 20% discount on a $150 item.</p><p><strong>X is what % of Y?</strong> &mdash; e.g. 30 correct answers out of 150 questions.</p><p><strong>Percentage increase / decrease</strong> &mdash; e.g. how much a price rose from $80 to $100.</p><h3>Tips</h3><p>Results update live as you type. Decimals are fine &mdash; try 12.5% of 240.</p>",
        [("What is 20% of 150?", "20% of 150 equals 30. Multiply 150 by 0.20."),
         ("How do I find percentage increase?", "Subtract the old value from the new value, divide by the old value, and multiply by 100. Our tool does this instantly."),
         ("Can I use decimals?", "Yes &mdash; the calculator accepts decimal numbers in every field.")],
        "<p><strong>20% of 150 = 30.</strong> If a store offers 20% off a $150 jacket, you save $30 and pay $120.</p>")

def build_age():
    calc = """
    <div class="field-row">
      <div class="field"><label for="dob">Date of birth</label><input id="dob" type="date" value="1990-06-15"></div>
      <div class="field"><label for="asof">Age at this date (optional)</label><input id="asof" type="date"></div>
    </div>
    <button class="btn" id="aGo">Calculate Age</button>
    <div class="result" id="aResult"><div class="big" id="aBig"></div><div class="detail" id="aDetail"></div></div>
    <script>
    (function(){
      function calc(){
        var dobS=document.getElementById('dob').value,
            asofS=document.getElementById('asof').value,
            r=document.getElementById('aResult');
        if(!dobS){r.classList.remove('show');return;}
        var dob=new Date(dobS+'T00:00:00'), asof=asofS?new Date(asofS+'T00:00:00'):new Date();
        dob.setHours(0,0,0,0); asof.setHours(0,0,0,0);
        if(asof<dob){r.classList.remove('show');return;}
        var y=asof.getFullYear()-dob.getFullYear(),
            m=asof.getMonth()-dob.getMonth(),
            d=asof.getDate()-dob.getDate();
        if(d<0){m--;var pm=new Date(asof.getFullYear(),asof.getMonth(),0);d+=pm.getDate();}
        if(m<0){y--;m+=12;}
        var totalDays=Math.round((asof-dob)/86400000);
        var nb=new Date(asof.getFullYear(),dob.getMonth(),dob.getDate());
        if(nb<asof)nb=new Date(asof.getFullYear()+1,dob.getMonth(),dob.getDate());
        var toB=Math.round((nb-asof)/86400000);
        document.getElementById('aBig').textContent=y+' years, '+m+' months, '+d+' days';
        document.getElementById('aDetail').textContent=
          'That is '+totalDays.toLocaleString()+' days in total ('+Math.floor(totalDays/7).toLocaleString()+' weeks). '+
          (toB===0?'Happy birthday today! 🎉':'Next birthday in '+toB+' day'+(toB===1?'':'s')+'.');
        r.classList.add('show');
      }
      document.getElementById('aGo').addEventListener('click',calc);
      document.getElementById('dob').addEventListener('change',calc);
      document.getElementById('asof').addEventListener('change',calc);
      calc();
    })();
    </script>"""
    tool_page("age-calculator", "&#127874;", "Age Calculator",
        "Find your exact age in years, months, and days from your date of birth. See total days lived and a countdown to your next birthday.",
        calc,
        "<h3>How it works</h3><p>Enter your date of birth. The calculator compares it with today (or any date you choose in the second field) using real calendar months, so leap years and varying month lengths are handled correctly.</p><h3>Privacy</h3><p>Your date of birth never leaves your device &mdash; the calculation runs entirely in your browser.</p>",
        [("How is age in months and days calculated?", "We compare calendar dates directly: full years first, then remaining months, then remaining days &mdash; accounting for leap years and different month lengths."),
         ("Can I find someone's age on a past date?", "Yes. Enter any date in the \"Age at this date\" field to see how old someone was (or will be) on that day."),
         ("Why does an online age calculator differ by a day sometimes?", "Time zones and whether the start day is counted can shift results by a day. We count using calendar dates at midnight, the standard convention.")],
        "<p><strong>Born June 15, 1990 &rarr; on October 18, 2026 you are 36 years, 4 months, and 3 days old.</strong> That is 13,274 days in total.</p>")

def build_datediff():
    calc = """
    <div class="field-row">
      <div class="field"><label for="dA">Start date</label><input id="dA" type="date" value="2026-01-01"></div>
      <div class="field"><label for="dB">End date</label><input id="dB" type="date" value="2026-01-11"></div>
    </div>
    <button class="btn" id="dGo">Calculate Difference</button>
    <div class="result" id="dResult"><div class="big" id="dBig"></div><div class="detail" id="dDetail"></div></div>
    <script>
    (function(){
      function calc(){
        var aS=document.getElementById('dA').value, bS=document.getElementById('dB').value,
            r=document.getElementById('dResult');
        if(!aS||!bS){r.classList.remove('show');return;}
        var a=new Date(aS+'T00:00:00'), b=new Date(bS+'T00:00:00');
        var days=Math.round((b-a)/86400000), ad=Math.abs(days);
        var weeks=Math.floor(ad/7), rem=ad%7;
        var months=(ad/30.4375), years=(ad/365.25);
        // Business days (Mon-Fri) and weekend days over the counted days:
        // every day after the earlier date, up to and including the later date.
        var lo=days>=0?a:b, biz=0, wknd=0;
        for(var i=1;i<=ad;i++){
          var dow=new Date(lo.getFullYear(),lo.getMonth(),lo.getDate()+i).getDay();
          if(dow===0||dow===6)wknd++; else biz++;
        }
        document.getElementById('dBig').textContent=ad.toLocaleString()+' day'+(ad===1?'':'s');
        document.getElementById('dDetail').textContent=
          'That equals '+weeks+' week'+(weeks===1?'':'s')+(rem?' and '+rem+' day'+(rem===1?'':'s'):'')+
          ', made up of '+biz+' business day'+(biz===1?'':'s')+' (Mon\u2013Fri) and '+wknd+
          ' weekend day'+(wknd===1?'':'s')+'. That is about '+months.toFixed(1)+
          ' months or '+years.toFixed(2)+' years.'+
          (days<0?' (The end date is before the start date.)':'');
        r.classList.add('show');
      }
      document.getElementById('dGo').addEventListener('click',calc);
      document.getElementById('dA').addEventListener('change',calc);
      document.getElementById('dB').addEventListener('change',calc);
      calc();
    })();
    </script>"""
    faqs = [
        ("How many days are between January 1 and January 11?",
         "10 days. The start date is not counted; each following calendar day adds one."),
        ("How many business days are between two dates?",
         "Business days are Monday to Friday. This calculator counts them for you: every day after the start date, up to and including the end date, is classed as a business day or a weekend day. January 1 to January 11, 2026, for example, contains 6 business days and 4 weekend days."),
        ("How many weeks are between two dates?",
         "Divide the total days by 7. The result shows whole weeks plus the remaining days &mdash; 10 days is 1 week and 3 days, and 45 days is 6 weeks and 3 days."),
        ("Does the calculator handle leap years?",
         "Yes. Dates are compared as real calendar dates, so February 29 in leap years is handled correctly."),
        ("Can I count months or years too?",
         "Yes &mdash; the result also shows the equivalent in weeks, approximate months, and years."),
    ]
    tool_page("date-difference", "&#128197;", "Date Difference Calculator",
        "Count the exact number of days between any two dates \u2014 including total weeks, business days, and weekend days. Perfect for trip planning, project deadlines, and countdowns.",
        calc,
        "<h3>How days are counted</h3><p>We count calendar days between the two dates, not including the start date. So January 1 to January 11 is <strong>10 days</strong> &mdash; the standard convention used by most date calculators.</p><h3>Weeks, business days, and weekend days</h3><p>As well as the total, the result breaks the span down into <strong>whole weeks plus remaining days</strong>, and counts how many of the days are <strong>business days (Monday to Friday)</strong> and how many fall on <strong>weekends</strong>. Each day after the start date, up to and including the end date, is classified &mdash; handy for leave planning, notice periods, and project schedules.</p><h3>Order does not matter</h3><p>You can enter the dates in either order; the tool shows the absolute difference and tells you if the end date comes first.</p>",
        faqs,
        "<p><strong>January 1, 2026 to January 11, 2026 = 10 days</strong> (1 week and 3 days) &mdash; made up of 6 business days and 4 weekend days.</p>",
        jsonld=tool_jsonld_graph("Date Difference Calculator",
            "Count the exact number of days between any two dates \u2014 including total weeks, business days, and weekend days. Perfect for trip planning, project deadlines, and countdowns.",
            "date-difference", faqs))

def build_salary():
    calc = """
    <div class="field-row">
      <div class="field"><label for="sRate">Hourly rate ($)</label><input id="sRate" type="number" value="20" step="any" min="0"></div>
      <div class="field"><label for="sHours">Hours per week</label><input id="sHours" type="number" value="40" step="any" min="0"></div>
    </div>
    <div class="field"><label for="sWeeks">Weeks worked per year</label><input id="sWeeks" type="number" value="52" step="any" min="0" max="52"></div>
    <button class="btn" id="sGo">Calculate Salary</button>
    <div class="result" id="sResult"><div class="big" id="sBig"></div><div class="detail" id="sDetail"></div></div>
    <script>
    (function(){
      function money(n){return '$'+Math.round(n).toLocaleString('en-US');}
      function calc(){
        var rate=parseFloat(document.getElementById('sRate').value),
            hrs=parseFloat(document.getElementById('sHours').value),
            wks=parseFloat(document.getElementById('sWeeks').value),
            r=document.getElementById('sResult');
        if(isNaN(rate)||isNaN(hrs)||isNaN(wks)){r.classList.remove('show');return;}
        var annual=rate*hrs*wks, monthly=annual/12, weekly=annual/52, daily=weekly/5;
        document.getElementById('sBig').textContent=money(annual)+' / year';
        document.getElementById('sDetail').textContent=
          money(monthly)+' per month \u2022 '+money(weekly)+' per week \u2022 '+money(daily)+' per day (5-day week). Gross pay before taxes.';
        r.classList.add('show');
      }
      document.getElementById('sGo').addEventListener('click',calc);
      ['sRate','sHours','sWeeks'].forEach(function(id){
        document.getElementById(id).addEventListener('input',calc);});
      calc();
    })();
    </script>"""
    tool_page("salary-calculator", "&#128176;", "Salary Calculator",
        "Convert your hourly wage to annual, monthly, weekly, and daily salary. Compare job offers and plan your budget in seconds.",
        calc,
        "<h3>How it works</h3><p>Enter your hourly rate, hours worked per week, and weeks worked per year. Annual salary = hourly rate &times; hours per week &times; weeks per year.</p><h3>Part-time or unpaid leave?</h3><p>Adjust the \"weeks worked per year\" field &mdash; e.g. 48 weeks if you take 4 unpaid weeks off.</p><h3>Note on taxes</h3><p>Results show <strong>gross</strong> pay before taxes and deductions, which vary by country and state.</p>",
        [("How do I convert $20/hour to annual salary?", "Multiply by hours per week and weeks per year: $20 \u00d7 40 \u00d7 52 = $41,600 per year."),
         ("Is this before or after tax?", "Before tax (gross). Net take-home pay depends on your local tax rates and deductions."),
         ("Can I use it for part-time work?", "Yes &mdash; just enter your actual weekly hours and weeks worked.")],
        "<p><strong>$20/hour &times; 40 hours/week &times; 52 weeks = $41,600 per year</strong> ($3,467/month, $800/week).</p>")

def build_converter():
    calc = """
    <div class="field"><label for="cCat">Category</label>
      <select id="cCat">
        <option value="length">Length</option>
        <option value="weight">Weight</option>
        <option value="temperature">Temperature</option>
        <option value="volume">Volume</option>
      </select>
    </div>
    <div class="field"><label for="cVal">Value</label><input id="cVal" type="number" value="1" step="any"></div>
    <div class="field-row">
      <div class="field"><label for="cFrom">From</label><select id="cFrom"></select></div>
      <div class="field"><label for="cTo">To</label><select id="cTo"></select></div>
    </div>
    <button class="btn" id="cGo">Convert</button>
    <div class="result" id="cResult"><div class="big" id="cBig"></div><div class="detail" id="cDetail"></div></div>
    <script>
    (function(){
      var T={
        length:{label:{m:'Meters',km:'Kilometers',cm:'Centimeters',mm:'Millimeters',mi:'Miles',yd:'Yards',ft:'Feet',in:'Inches'},
                f:{m:1,km:1000,cm:0.01,mm:0.001,mi:1609.344,yd:0.9144,ft:0.3048,in:0.0254}},
        weight:{label:{kg:'Kilograms',g:'Grams',t:'Tonnes',lb:'Pounds',oz:'Ounces'},
                f:{kg:1,g:0.001,t:1000,lb:0.45359237,oz:0.028349523125}},
        volume:{label:{l:'Liters',ml:'Milliliters',gal:'Gallons (US)','fl oz':'Fluid ounces (US)',cup:'Cups (US)'},
                f:{l:1,ml:0.001,gal:3.785411784,'fl oz':0.0295735295625,cup:0.2365882365}},
        temperature:{label:{c:'Celsius (\u00B0C)',f:'Fahrenheit (\u00B0F)',k:'Kelvin (K)'}}
      };
      var cat=document.getElementById('cCat'),
          from=document.getElementById('cFrom'),
          to=document.getElementById('cTo');
      function fill(){
        var t=T[cat.value]; from.innerHTML=''; to.innerHTML='';
        Object.keys(t.label).forEach(function(u){
          from.add(new Option(t.label[u],u)); to.add(new Option(t.label[u],u));
        });
        if(cat.value==='length'){from.value='m';to.value='ft';}
        if(cat.value==='weight'){from.value='kg';to.value='lb';}
        if(cat.value==='temperature'){from.value='c';to.value='f';}
        if(cat.value==='volume'){from.value='l';to.value='gal';}
        calc();
      }
      function toC(v,u){return u==='c'?v:u==='f'?(v-32)*5/9:v-273.15;}
      function fromC(v,u){return u==='c'?v:u==='f'?v*9/5+32:v+273.15;}
      function calc(){
        var v=parseFloat(document.getElementById('cVal').value),
            r=document.getElementById('cResult');
        if(isNaN(v)){r.classList.remove('show');return;}
        var t=T[cat.value], out;
        if(cat.value==='temperature'){out=fromC(toC(v,from.value),to.value);}
        else{out=v*t.f[from.value]/t.f[to.value];}
        var disp=Math.round(out*1000000)/1000000;
        document.getElementById('cBig').textContent=disp.toLocaleString('en-US',{maximumFractionDigits:6})+' '+to.value;
        document.getElementById('cDetail').textContent=
          document.getElementById('cVal').value+' '+t.label[from.value]+' = '+disp+' '+t.label[to.value]+'.';
        r.classList.add('show');
      }
      cat.addEventListener('change',fill);
      ['cVal','cFrom','cTo'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);
        document.getElementById(id).addEventListener('change',calc);});
      document.getElementById('cGo').addEventListener('click',calc);
      fill();
    })();
    </script>"""
    tool_page("unit-converter", "&#8646;", "Unit Converter",
        "Convert length, weight, temperature, and volume units instantly. Metric to imperial and back, with precise standard conversion factors.",
        calc,
        "<h3>Four categories</h3><p><strong>Length:</strong> meters, kilometers, centimeters, millimeters, miles, yards, feet, inches.</p><p><strong>Weight:</strong> kilograms, grams, tonnes, pounds, ounces.</p><p><strong>Temperature:</strong> Celsius, Fahrenheit, Kelvin.</p><p><strong>Volume:</strong> liters, milliliters, US gallons, fluid ounces, cups.</p><h3>Accuracy</h3><p>Conversions use internationally defined factors (e.g. 1 inch = 2.54 cm exactly). Results update live as you type.</p>",
        [("How many pounds is 1 kilogram?", "1 kilogram equals 2.20462 pounds (exactly 2.2046226218 lb)."),
         ("How do I convert Celsius to Fahrenheit?", "Multiply by 9/5 and add 32. Our converter handles Celsius, Fahrenheit, and Kelvin instantly."),
         ("Are US or UK gallons used?", "US gallons. One US gallon = 3.78541 liters.")],
        "<p><strong>1 kilogram = 2.20462 pounds.</strong> Select Weight, enter 1, choose kg \u2192 lb.</p>")

def build_sqft():
    calc = """
    <div class="field"><label for="sqUnit">Measure in</label>
      <select id="sqUnit">
        <option value="ft">Feet</option>
        <option value="in">Inches</option>
        <option value="ftin">Feet &amp; inches</option>
        <option value="m">Meters</option>
      </select>
    </div>
    <div id="sqAreas"></div>
    <button class="btn-small" id="sqAdd" type="button">+ Add another area</button>
    <div class="field-row" style="margin-top:16px">
      <div class="field"><label for="sqWaste">Waste allowance (%)</label><input id="sqWaste" type="number" value="10" step="any" min="0"></div>
      <div class="field"><label for="sqPrice">Cost per sq ft ($) &mdash; optional</label><input id="sqPrice" type="number" placeholder="e.g. 3.50" step="any" min="0"></div>
    </div>
    <div class="result" id="sqResult"><div class="big" id="sqBig"></div><div class="detail" id="sqDetail"></div></div>
    <script>
    (function(){
      var FT_PER_M=3.280839895;
      var state={unit:'ft', areas:[{shape:'rect', d1:12, d2:10}]};
      var shapes={rect:['Length','Width'], circle:['Diameter'], triangle:['Base','Height']};
      function fmt(n){return (Math.round(n*100)/100).toLocaleString('en-US',{maximumFractionDigits:2});}
      function toDisplay(feet){
        if(state.unit==='in')return Math.round(feet*12*100)/100;
        if(state.unit==='m')return Math.round(feet/FT_PER_M*1000)/1000;
        return Math.round(feet*100)/100;
      }
      function fromDisplay(v){
        if(state.unit==='in')return v/12;
        if(state.unit==='m')return v*FT_PER_M;
        return v;
      }
      function splitFtIn(feet){
        var ft=Math.floor(feet+1e-9), inch=Math.round((feet-ft)*12*10)/10;
        if(inch>=12){ft+=1;inch=0;}
        return [ft,inch];
      }
      function dimHtml(i,k){
        if(state.unit==='ftin'){
          var area=state.areas[i], parts=splitFtIn(area[k]);
          return '<div class="field" style="flex:1"><label>'+shapes[area.shape][k==='d1'?0:1]+'</label>'+
            '<div style="display:flex;gap:8px"><input type="number" step="any" min="0" class="sq-dim" data-i="'+i+'" data-k="'+k+'" data-part="ft" value="'+parts[0]+'" placeholder="ft">'+
            '<input type="number" step="any" min="0" class="sq-dim" data-i="'+i+'" data-k="'+k+'" data-part="in" value="'+parts[1]+'" placeholder="in"></div></div>';
        }
        return '<div class="field" style="flex:1"><label>'+shapes[state.areas[i].shape][k==='d1'?0:1]+' ('+state.unit+')</label>'+
          '<input type="number" step="any" min="0" class="sq-dim" data-i="'+i+'" data-k="'+k+'" data-part="main" value="'+toDisplay(state.areas[i][k])+'"></div>';
      }
      function render(){
        var c=document.getElementById('sqAreas'); c.innerHTML='';
        state.areas.forEach(function(area,i){
          var row=document.createElement('div'); row.className='area-row';
          var head='<div class="area-head"><strong>Area '+(i+1)+'</strong>'+
            '<span><select class="sq-shape" data-i="'+i+'">'+
            '<option value="rect"'+(area.shape==='rect'?' selected':'')+'>Rectangle</option>'+
            '<option value="circle"'+(area.shape==='circle'?' selected':'')+'>Circle</option>'+
            '<option value="triangle"'+(area.shape==='triangle'?' selected':'')+'>Triangle</option></select> '+
            (state.areas.length>1?'<button type="button" class="btn-small btn-danger sq-remove" data-i="'+i+'">Remove</button>':'')+
            '</span></div>';
          var dims='<div style="display:flex;gap:14px;flex-wrap:wrap">'+dimHtml(i,'d1')+(area.shape==='circle'?'':dimHtml(i,'d2'))+'</div>';
          row.innerHTML=head+dims; c.appendChild(row);
        });
        recalc();
      }
      function readDim(i,k){
        if(state.unit==='ftin'){
          var ft=parseFloat(document.querySelector('.sq-dim[data-i="'+i+'"][data-k="'+k+'"][data-part="ft"]').value)||0;
          var inch=parseFloat(document.querySelector('.sq-dim[data-i="'+i+'"][data-k="'+k+'"][data-part="in"]').value)||0;
          return ft+inch/12;
        }
        var v=parseFloat(document.querySelector('.sq-dim[data-i="'+i+'"][data-k="'+k+'"][data-part="main"]').value);
        return isNaN(v)?NaN:fromDisplay(v);
      }
      function recalc(){
        var total=0, valid=false;
        state.areas.forEach(function(area,i){
          var d1=readDim(i,'d1'); if(!isNaN(d1))area.d1=d1;
          if(area.shape!=='circle'){var d2=readDim(i,'d2'); if(!isNaN(d2))area.d2=d2;}
          var a=0;
          if(area.shape==='circle'){var r=area.d1/2; a=Math.PI*r*r;}
          else if(area.shape==='triangle'){a=area.d1*area.d2/2;}
          else{a=area.d1*area.d2;}
          if(a>0){valid=true; total+=a;}
        });
        var r=document.getElementById('sqResult');
        if(!valid||total<=0){r.classList.remove('show');return;}
        var waste=parseFloat(document.getElementById('sqWaste').value)||0;
        var withWaste=total*(1+waste/100);
        var price=parseFloat(document.getElementById('sqPrice').value);
        document.getElementById('sqBig').textContent=fmt(withWaste)+' sq ft'+(waste>0?' (incl. '+waste+'% waste)':'');
        var d='Measured area: '+fmt(total)+' sq ft = '+fmt(total*0.09290304)+' sq m = '+fmt(total/9)+' sq yd.';
        if(waste>0)d+=' With waste: '+fmt(withWaste)+' sq ft ('+fmt(withWaste*0.09290304)+' sq m).';
        if(!isNaN(price)&&price>0)d+=' Estimated material cost: $'+fmt(withWaste*price)+'.';
        document.getElementById('sqDetail').textContent=d;
        r.classList.add('show');
      }
      document.getElementById('sqAreas').addEventListener('input',function(e){
        if(e.target.classList.contains('sq-dim'))recalc();
      });
      document.getElementById('sqAreas').addEventListener('change',function(e){
        if(e.target.classList.contains('sq-shape')){
          state.areas[+e.target.dataset.i].shape=e.target.value; render();
        }
      });
      document.getElementById('sqAreas').addEventListener('click',function(e){
        if(e.target.classList.contains('sq-remove')){
          state.areas.splice(+e.target.dataset.i,1); render();
        }
      });
      document.getElementById('sqAdd').addEventListener('click',function(){
        state.areas.push({shape:'rect',d1:10,d2:10}); render();
      });
      document.getElementById('sqUnit').addEventListener('change',function(e){
        // flush current DOM values into state before switching display unit
        state.areas.forEach(function(area,i){
          var d1=readDim(i,'d1'); if(!isNaN(d1))area.d1=d1;
          if(area.shape!=='circle'){var d2=readDim(i,'d2'); if(!isNaN(d2))area.d2=d2;}
        });
        state.unit=e.target.value; render();
      });
      ['sqWaste','sqPrice'].forEach(function(id){document.getElementById(id).addEventListener('input',recalc);});
      render();
    })();
    </script>"""
    faqs = [
        ("How do I calculate the square footage of a room?",
         "Multiply the length by the width. A room that is 12 ft long and 10 ft wide is 12 x 10 = 120 square feet."),
        ("How do I measure an L-shaped room or floor?",
         "Split it into two rectangles, work out each one, and add them together. Use the \"+ Add another area\" button here and the tool adds everything up for you."),
        ("How much extra should I add for waste?",
         "For flooring and tile, 5-10% extra is the usual allowance for cuts and mistakes, and 15% or more for diagonal layouts. Enter it in the waste field and the total adjusts automatically."),
        ("How do I convert square feet to square meters?",
         "Multiply square feet by 0.0929. So 120 sq ft is about 11.15 sq m. This calculator shows square feet, square meters, and square yards side by side."),
        ("Can I enter measurements in feet and inches?",
         "Yes. Choose \"Feet & inches\" under Measure in, and enter the feet and inches parts separately, for example 11 ft 6 in."),
    ]
    tool_page("square-footage-calculator", "&#128208;", "Square Footage Calculator",
        "Free square footage calculator for rooms and flooring: rectangles, circles, and triangles, multiple areas, feet and inches or meters, waste allowance, and cost per sq ft.",
        calc,
        "<h3>The formula</h3><p>For a rectangle, <strong>area = length &times; width</strong>. A circle uses &pi; &times; (diameter &divide; 2)&sup2;, and a triangle is base &times; height &divide; 2.</p><h3>Multiple rooms and L-shapes</h3><p>Add as many areas as you like &mdash; a whole floor, an L-shaped room split into rectangles, or a round patio &mdash; and the totals are added together.</p><h3>Feet and inches, or meters</h3><p>Use the \"Measure in\" menu to enter plain feet, inches, feet &amp; inches together (like 11 ft 6 in), or meters. Results always come out in square feet, square meters, and square yards.</p><h3>Ordering flooring?</h3><p>Add a waste percentage (5-10% is typical) and, if you know it, the price per square foot to get an estimated material cost.</p>",
        faqs,
        "<p><strong>A 12 ft &times; 10 ft bedroom = 120 sq ft.</strong> With a 10% waste allowance for flooring you would order 132 sq ft of material &mdash; that is 11.15 sq m, or 14.67 sq yd.</p>",
        jsonld=tool_jsonld_graph("Square Footage Calculator",
            "Free square footage calculator for rooms and flooring: rectangles, circles, and triangles, multiple areas, feet and inches or meters, waste allowance, and cost per sq ft.",
            "square-footage-calculator", faqs))

def build_concrete():
    calc = """
    <div class="field-row">
      <div class="field"><label for="cL">Length (ft)</label><input id="cL" type="number" value="10" step="any" min="0"></div>
      <div class="field"><label for="cW">Width (ft)</label><input id="cW" type="number" value="10" step="any" min="0"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cT">Thickness (inches)</label><input id="cT" type="number" value="4" step="any" min="0"></div>
      <div class="field"><label for="cWaste">Waste (%)</label><input id="cWaste" type="number" value="10" step="any" min="0"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cYardPrice">Ready-mix price per cubic yard ($) &mdash; optional</label><input id="cYardPrice" type="number" placeholder="e.g. 165" step="any" min="0"></div>
      <div class="field"><label for="cBagPrice">Bag price ($) &mdash; optional</label><input id="cBagPrice" type="number" placeholder="e.g. 5.50" step="any" min="0"></div>
    </div>
    <div class="field"><label for="cBagSize">Bag size for the cost estimate</label>
      <select id="cBagSize"><option value="40">40 lb</option><option value="50">50 lb</option><option value="60">60 lb</option><option value="80" selected>80 lb</option></select>
    </div>
    <button class="btn" id="cGo">Calculate Concrete</button>
    <div class="result" id="cResult"><div class="big" id="cBig"></div><div class="detail" id="cDetail"></div><div id="cBags"></div></div>
    <script>
    (function(){
      var YIELDS={40:0.30,50:0.375,60:0.45,80:0.60};
      function fmt(n){return (Math.round(n*100)/100).toLocaleString('en-US',{maximumFractionDigits:2});}
      function calc(){
        var L=parseFloat(document.getElementById('cL').value),
            W=parseFloat(document.getElementById('cW').value),
            T=parseFloat(document.getElementById('cT').value),
            waste=parseFloat(document.getElementById('cWaste').value)||0,
            r=document.getElementById('cResult');
        if(isNaN(L)||isNaN(W)||isNaN(T)||L<=0||W<=0||T<=0){r.classList.remove('show');return;}
        var cuft=L*W*(T/12), cuyd=cuft/27, cum=cuft*0.0283168466;
        var need=cuft*(1+waste/100);
        document.getElementById('cBig').textContent=fmt(cuyd)+' cubic yards';
        var d='Volume: '+fmt(cuft)+' cu ft = '+fmt(cum)+' cu m. '+
          'With '+waste+'% waste, order for '+fmt(need/27)+' cu yd ('+fmt(need)+' cu ft).';
        var yp=parseFloat(document.getElementById('cYardPrice').value);
        if(!isNaN(yp)&&yp>0)d+=' Ready-mix estimate: $'+fmt((need/27)*yp)+'.';
        document.getElementById('cDetail').textContent=d;
        var bp=parseFloat(document.getElementById('cBagPrice').value);
        var sel=document.getElementById('cBagSize').value;
        var rows=[40,50,60,80].map(function(size){
          var bags=Math.ceil(need/YIELDS[size]);
          var cost=(!isNaN(bp)&&bp>0&&String(size)===sel)?' &mdash; est. $'+fmt(bags*bp):'';
          return '<tr><td>'+size+' lb</td><td>'+YIELDS[size]+' cu ft</td><td><strong>'+bags+'</strong>'+cost+'</td></tr>';
        }).join('');
        document.getElementById('cBags').innerHTML=
          '<table class="bagtable"><tr><th>Bag size</th><th>Yield per bag</th><th>Bags needed (incl. waste)</th></tr>'+rows+'</table>';
        r.classList.add('show');
      }
      document.getElementById('cGo').addEventListener('click',calc);
      ['cL','cW','cT','cWaste','cYardPrice','cBagPrice','cBagSize'].forEach(function(id){
        document.getElementById(id).addEventListener('input',calc);
        document.getElementById(id).addEventListener('change',calc);
      });
      calc();
    })();
    </script>"""
    faqs = [
        ("How many bags of concrete do I need for a 10 x 10 slab?",
         "At 4 inches thick, a 10 x 10 ft slab is 33.3 cubic feet (1.23 cubic yards). That takes 56 bags of 80 lb concrete before waste, or 62 bags with a 10% waste allowance."),
        ("What yields does this calculator use for each bag size?",
         "The standard manufacturer yields: a 40 lb bag makes 0.30 cu ft, a 50 lb bag 0.375 cu ft, a 60 lb bag 0.45 cu ft, and an 80 lb bag 0.60 cu ft of finished concrete."),
        ("How many cubic yards is a 10 x 10 slab, 4 inches thick?",
         "10 x 10 x (4/12) = 33.3 cubic feet, and 33.3 divided by 27 is 1.23 cubic yards."),
        ("Should I mix bags or order ready-mix?",
         "Bags suit small jobs like post holes, pads, and repairs. Past roughly one cubic yard you are mixing dozens of heavy bags that all have to be placed before the first ones set, so ready-mix delivery is usually the better order."),
        ("Why add a waste allowance?",
         "Real pours always use more than the exact geometry: the ground is never perfectly flat, forms bow slightly, and some mix stays in the mixer. 5-10% extra is the common allowance, closer to 15% for footings poured against bare earth."),
    ]
    tool_page("concrete-calculator", "&#129521;", "Concrete Calculator",
        "Free concrete calculator: enter slab length, width, and thickness to get cubic yards, cubic feet, and cubic meters, plus how many 40, 50, 60, or 80 lb bags you need.",
        calc,
        "<h3>The formula</h3><p><strong>Volume = length (ft) &times; width (ft) &times; thickness (ft)</strong>, with thickness entered in inches and converted (divide by 12). Cubic yards = cubic feet &divide; 27.</p><h3>Bag counts</h3><p>Each pre-mix bag yields a fixed volume: 40 lb &rarr; 0.30 cu ft, 50 lb &rarr; 0.375, 60 lb &rarr; 0.45, 80 lb &rarr; 0.60. Bags needed = total volume (including your waste allowance) &divide; yield, rounded up.</p><h3>Costs</h3><p>Optionally add a ready-mix price per cubic yard, or a bag price with a bag size, to see an estimated material cost.</p>",
        faqs,
        "<p><strong>A 10 ft &times; 10 ft slab, 4 inches thick = 33.33 cu ft = 1.23 cubic yards.</strong> In bags that is 56 &times; 80 lb bags before waste, or 62 bags with the standard 10% waste allowance.</p>",
        jsonld=tool_jsonld_graph("Concrete Calculator",
            "Free concrete calculator: enter slab length, width, and thickness to get cubic yards, cubic feet, and cubic meters, plus how many 40, 50, 60, or 80 lb bags you need.",
            "concrete-calculator", faqs))

def build_wordcounter():
    calc = """
    <div class="field"><label for="wcText">Your text</label>
      <textarea id="wcText" placeholder="Type or paste your text here &mdash; the counts update as you type.">The quick brown fox jumps over the lazy dog.</textarea>
    </div>
    <div class="stats">
      <div class="stat"><div class="num" id="wcWords">0</div><div class="lab">Words</div></div>
      <div class="stat"><div class="num" id="wcChars">0</div><div class="lab">Characters</div></div>
      <div class="stat"><div class="num" id="wcCharsNS">0</div><div class="lab">Characters (no spaces)</div></div>
      <div class="stat"><div class="num" id="wcSent">0</div><div class="lab">Sentences</div></div>
      <div class="stat"><div class="num" id="wcPara">0</div><div class="lab">Paragraphs</div></div>
      <div class="stat"><div class="num" id="wcRead">0 sec</div><div class="lab">Reading time</div></div>
      <div class="stat"><div class="num" id="wcSpeak">0 sec</div><div class="lab">Speaking time</div></div>
    </div>
    <div class="topwords"><h3 style="margin:14px 0 6px">Top repeated words</h3><ul id="wcTop" style="margin:0;padding-left:20px"></ul></div>
    <script>
    (function(){
      var READING_WPM=238, SPEAKING_WPM=130;
      function dur(sec){
        sec=Math.round(sec);
        if(sec<60)return sec+' sec';
        var m=Math.floor(sec/60), s=sec%60;
        return m+' min'+(s?' '+s+' sec':'');
      }
      function update(){
        var t=document.getElementById('wcText').value;
        var trimmed=t.trim();
        var wordsArr=trimmed?trimmed.split(/\\s+/):[];
        var words=wordsArr.length;
        var sentences=trimmed?t.split(/[.!?]+/).filter(function(s){return s.trim().length>0;}).length:0;
        var paragraphs=trimmed?t.split(/\\n+/).filter(function(s){return s.trim().length>0;}).length:0;
        document.getElementById('wcWords').textContent=words.toLocaleString();
        document.getElementById('wcChars').textContent=t.length.toLocaleString();
        document.getElementById('wcCharsNS').textContent=t.replace(/\\s/g,'').length.toLocaleString();
        document.getElementById('wcSent').textContent=sentences;
        document.getElementById('wcPara').textContent=paragraphs;
        document.getElementById('wcRead').textContent=dur(words/READING_WPM*60);
        document.getElementById('wcSpeak').textContent=dur(words/SPEAKING_WPM*60);
        var freq={};
        wordsArr.forEach(function(w){
          var key=w.toLowerCase().replace(/^[^a-z0-9']+|[^a-z0-9']+$/g,'');
          if(key.length>=3)freq[key]=(freq[key]||0)+1;
        });
        var top=Object.keys(freq).map(function(k){return {word:k,count:freq[k]};})
          .sort(function(a,b){return b.count-a.count||(a.word<b.word?-1:1);}).slice(0,5);
        var ul=document.getElementById('wcTop');
        ul.innerHTML=top.length?top.map(function(e){
          var pct=words?Math.round(e.count/words*1000)/10:0;
          return '<li><strong>'+e.word+'</strong> &mdash; '+e.count+'x ('+pct+'%)</li>';
        }).join(''):'<li>No repeated words yet &mdash; keep typing.</li>';
      }
      document.getElementById('wcText').addEventListener('input',update);
      update();
    })();
    </script>"""
    faqs = [
        ("How are words counted?",
         "A word is any sequence of characters separated by whitespace. The sentence \"The quick brown fox jumps over the lazy dog.\" counts as 9 words."),
        ("Is my text uploaded or stored anywhere?",
         "No. The counter runs entirely in your browser with JavaScript. Nothing you type or paste is sent to a server, saved, or shared."),
        ("How is reading time calculated?",
         "Reading time uses an average silent reading speed of 238 words per minute, and speaking time uses 130 words per minute for a relaxed spoken pace. Both are estimates and are labelled with the rates used."),
        ("What counts as a sentence?",
         "A run of text ending in a full stop, question mark, or exclamation mark. Paragraphs are counted by line breaks."),
        ("How does the keyword density list work?",
         "It shows your five most repeated words of three letters or more, with how many times each appears and its percentage share of the whole text. That share is the keyword density writers use to check they are not over-repeating a term."),
    ]
    tool_page("word-counter", "&#128221;", "Word Counter",
        "Free online word counter: count words, characters with and without spaces, sentences, paragraphs, reading time, and speaking time as you type. Nothing is uploaded.",
        calc,
        "<h3>How it works</h3><p>Type or paste text into the box and every count updates live &mdash; no button to press. Words are separated by whitespace, sentences end with a full stop, question mark, or exclamation mark, and paragraphs are counted by line breaks.</p><h3>Reading and speaking time</h3><p>Reading time is estimated at <strong>238 words per minute</strong> (an average adult silent reading speed), and speaking time at <strong>130 words per minute</strong> (a relaxed presentation pace).</p><h3>Keyword density</h3><p>The top repeated words list shows your five most-used words of 3+ letters, with counts and percentage share &mdash; handy for essays, articles, and SEO writing.</p><h3>Private by design</h3><p>All counting happens locally in your browser. Your text is never uploaded, stored, or shared.</p>",
        faqs,
        "<p><strong>\"The quick brown fox jumps over the lazy dog.\"</strong> = 9 words, 44 characters (36 with no spaces), 1 sentence, 1 paragraph, and about 2 seconds of reading time.</p>",
        jsonld=tool_jsonld_graph("Word Counter",
            "Free online word counter: count words, characters with and without spaces, sentences, paragraphs, reading time, and speaking time as you type. Nothing is uploaded.",
            "word-counter", faqs))

def build_gpa():
    calc = """
    <h3 style="margin:0 0 12px">Semester GPA &mdash; your courses</h3>
    <div id="gpaRows"></div>
    <button class="btn-small" id="gpaAdd" type="button">+ Add course</button>
    <button class="btn" id="gpaGo" style="margin-top:16px">Calculate GPA</button>
    <div class="result" id="gpaResult"><div class="big" id="gpaBig"></div><div class="detail" id="gpaDetail"></div></div>
    <h3 style="margin:26px 0 12px">CGPA &mdash; add this semester to your record</h3>
    <div class="field-row">
      <div class="field"><label for="cgpaCur">Current CGPA (4.0 scale)</label><input id="cgpaCur" type="number" value="3.50" step="any" min="0" max="4"></div>
      <div class="field"><label for="cgpaDone">Credits completed so far</label><input id="cgpaDone" type="number" value="60" step="any" min="0"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="cgpaSem">This semester's GPA</label><input id="cgpaSem" type="number" value="3.80" step="any" min="0" max="4"></div>
      <div class="field"><label for="cgpaSemCr">This semester's credits</label><input id="cgpaSemCr" type="number" value="15" step="any" min="0"></div>
    </div>
    <button class="btn" id="cgpaGo">Calculate New CGPA</button>
    <div class="result" id="cgpaResult"><div class="big" id="cgpaBig"></div><div class="detail" id="cgpaDetail"></div></div>
    <h3 style="margin:26px 0 12px">CGPA to percentage (10-point scale)</h3>
    <div class="field"><label for="pctCgpa">Your CGPA on the 10-point scale</label><input id="pctCgpa" type="number" value="8.5" step="any" min="0" max="10"></div>
    <button class="btn" id="pctGo">Convert to Percentage</button>
    <div class="result" id="pctResult"><div class="big" id="pctBig"></div><div class="detail" id="pctDetail"></div></div>
    <script>
    (function(){
      var GP={'A+':4.0,'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,'C-':1.7,'D+':1.3,'D':1.0,'F':0.0};
      var GRADES=Object.keys(GP);
      var courses=[
        {name:'Course 1',grade:'A',credits:3},
        {name:'Course 2',grade:'B+',credits:4},
        {name:'Course 3',grade:'A-',credits:3}
      ];
      function fmt(n,d){return (Math.round(n*Math.pow(10,d))/Math.pow(10,d)).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});}
      function render(){
        var c=document.getElementById('gpaRows'); c.innerHTML='';
        courses.forEach(function(course,i){
          var row=document.createElement('div'); row.className='area-row';
          var opts=GRADES.map(function(g){
            return '<option value="'+g+'"'+(course.grade===g?' selected':'')+'>'+g+' ('+GP[g].toFixed(1)+')</option>';
          }).join('');
          row.innerHTML=
            '<div class="area-head"><strong>Course '+(i+1)+'</strong>'+
            (courses.length>1?'<button type="button" class="btn-small btn-danger gpa-remove" data-i="'+i+'">Remove</button>':'')+'</div>'+
            '<div style="display:flex;gap:14px;flex-wrap:wrap">'+
            '<div class="field" style="flex:2;min-width:150px"><label>Course name (optional)</label>'+
            '<input type="text" class="gpa-name" data-i="'+i+'" value="'+course.name.replace(/"/g,'&quot;')+'" placeholder="e.g. Biology"></div>'+
            '<div class="field" style="flex:1;min-width:110px"><label>Grade</label>'+
            '<select class="gpa-grade" data-i="'+i+'">'+opts+'</select></div>'+
            '<div class="field" style="flex:1;min-width:110px"><label>Credit hours</label>'+
            '<input type="number" class="gpa-credits" data-i="'+i+'" step="any" min="0" value="'+course.credits+'"></div>'+
            '</div>';
          c.appendChild(row);
        });
        recalc();
      }
      function flush(){
        document.querySelectorAll('.gpa-name').forEach(function(el){courses[+el.dataset.i].name=el.value;});
        document.querySelectorAll('.gpa-grade').forEach(function(el){courses[+el.dataset.i].grade=el.value;});
        document.querySelectorAll('.gpa-credits').forEach(function(el){
          var v=parseFloat(el.value); courses[+el.dataset.i].credits=isNaN(v)?0:v;});
      }
      function recalc(){
        flush();
        var qp=0, cr=0, n=0;
        courses.forEach(function(course){
          if(course.credits>0){qp+=GP[course.grade]*course.credits; cr+=course.credits; n++;}
        });
        var r=document.getElementById('gpaResult');
        if(cr<=0){r.classList.remove('show');return;}
        document.getElementById('gpaBig').textContent=fmt(qp/cr,2)+' GPA';
        document.getElementById('gpaDetail').textContent=
          'Total quality points: '+fmt(qp,1)+' across '+n+' course'+(n===1?'':'s')+
          ' and '+fmt(cr,1)+' credit hours. GPA = '+fmt(qp,1)+' \u00f7 '+fmt(cr,1)+'.';
        r.classList.add('show');
      }
      function recalcCgpa(){
        var cur=parseFloat(document.getElementById('cgpaCur').value),
            done=parseFloat(document.getElementById('cgpaDone').value),
            sem=parseFloat(document.getElementById('cgpaSem').value),
            semCr=parseFloat(document.getElementById('cgpaSemCr').value),
            r=document.getElementById('cgpaResult');
        if(isNaN(cur)||isNaN(done)||isNaN(sem)||isNaN(semCr)||(done+semCr)<=0){r.classList.remove('show');return;}
        var qp=cur*done+sem*semCr, total=done+semCr;
        document.getElementById('cgpaBig').textContent=fmt(qp/total,2)+' CGPA';
        document.getElementById('cgpaDetail').textContent=
          'That is '+fmt(qp,1)+' total quality points over '+fmt(total,0)+' credits ('+
          fmt(done,0)+' completed + '+fmt(semCr,0)+' this semester).';
        r.classList.add('show');
      }
      function recalcPct(){
        var v=parseFloat(document.getElementById('pctCgpa').value),
            r=document.getElementById('pctResult');
        if(isNaN(v)||v<0){r.classList.remove('show');return;}
        document.getElementById('pctBig').textContent=fmt(v*9.5,2)+'%';
        document.getElementById('pctDetail').textContent=
          'CGPA '+fmt(v,2)+' \u00d7 9.5 = '+fmt(v*9.5,2)+'%. This is the common CBSE-style approximation for the 10-point scale \u2014 it is not an official conversion and your university may calculate differently.';
        r.classList.add('show');
      }
      document.getElementById('gpaRows').addEventListener('input',recalc);
      document.getElementById('gpaRows').addEventListener('change',recalc);
      document.getElementById('gpaRows').addEventListener('click',function(e){
        if(e.target.classList.contains('gpa-remove')){flush(); courses.splice(+e.target.dataset.i,1); render();}
      });
      document.getElementById('gpaAdd').addEventListener('click',function(){
        flush(); courses.push({name:'',grade:'B',credits:3}); render();
      });
      document.getElementById('gpaGo').addEventListener('click',recalc);
      document.getElementById('cgpaGo').addEventListener('click',recalcCgpa);
      ['cgpaCur','cgpaDone','cgpaSem','cgpaSemCr'].forEach(function(id){
        document.getElementById(id).addEventListener('input',recalcCgpa);});
      document.getElementById('pctGo').addEventListener('click',recalcPct);
      document.getElementById('pctCgpa').addEventListener('input',recalcPct);
      render(); recalcCgpa(); recalcPct();
    })();
    </script>"""
    faqs = [
        ("How is GPA calculated?",
         "Each grade is worth points on the 4.0 scale, and those points are multiplied by the course's credit hours to give quality points. GPA = total quality points divided by total credit hours. An A in a 3-credit course (12 points), a B+ in a 4-credit course (13.2), and an A- in a 3-credit course (11.1) give 36.3 quality points over 10 credits, a GPA of 3.63."),
        ("How do I convert CGPA to percentage?",
         "On the 10-point scale used by many Indian and Pakistani universities, the common formula is percentage = CGPA x 9.5, so a CGPA of 8.5 is about 80.75%. It is an approximation (the CBSE-style formula), not an official conversion, and it varies by university. It does not apply to a 4.0-scale GPA."),
        ("How do I get my GPA from a percentage?",
         "For the 10-point scale, CGPA is roughly percentage divided by 9.5, so 85% is about a CGPA of 8.9. There is no official formula for the US 4.0 scale; the usual estimate maps your percentage to a letter grade first (93-100% is an A, 4.0; 90-92% is an A-, 3.7), using the grade table on this page."),
        ("What is the difference between GPA and CGPA?",
         "GPA is the average for a single semester or term. CGPA is the cumulative average across every semester so far, weighted by credit hours - it is not just the average of your semester GPAs unless every semester had the same credits."),
        ("Does an F count in my GPA?",
         "Yes. An F is worth 0.0 points, but its credit hours still count in the total, which is why one F pulls a GPA down so hard. Many colleges let you retake a course, and retake policies vary by school."),
    ]
    tool_page("gpa-calculator", "&#127891;", "GPA Calculator",
        "Free GPA and CGPA calculator: add your courses, letter grades, and credit hours to get your semester GPA on the 4.0 scale, update your cumulative CGPA, and convert a 10-point CGPA to a percentage.",
        calc,
        """<h3>The 4.0 scale</h3><p>US colleges and high schools grade on a 4.0 scale. The standard grade points (with the percentage bands many schools use) are:</p>
<table class="bagtable"><tr><th>Grade</th><th>Points</th><th>Typical %</th><th>Grade</th><th>Points</th><th>Typical %</th></tr>
<tr><td>A+</td><td>4.0</td><td>97-100</td><td>B-</td><td>2.7</td><td>80-82</td></tr>
<tr><td>A</td><td>4.0</td><td>93-96</td><td>C+</td><td>2.3</td><td>77-79</td></tr>
<tr><td>A-</td><td>3.7</td><td>90-92</td><td>C</td><td>2.0</td><td>73-76</td></tr>
<tr><td>B+</td><td>3.3</td><td>87-89</td><td>C-</td><td>1.7</td><td>70-72</td></tr>
<tr><td>B</td><td>3.0</td><td>83-86</td><td>D+</td><td>1.3</td><td>67-69</td></tr>
<tr><td></td><td></td><td></td><td>D</td><td>1.0</td><td>63-66</td></tr>
<tr><td></td><td></td><td></td><td>F</td><td>0.0</td><td>Below 60</td></tr></table>
<h3>The formula</h3><p><strong>GPA = total quality points &divide; total credit hours</strong>, where quality points for a course = grade points &times; credit hours. A 4-credit course moves your GPA more than a 1-credit course with the same grade.</p><h3>Updating your CGPA</h3><p>CGPA is the same formula stretched over your whole degree: combine your completed credits at your current CGPA with this semester's credits at this semester's GPA, then divide by the new credit total.</p><h3>CGPA to percentage - and GPA from percentage</h3><p>Many universities on the <strong>10-point scale</strong> estimate a percentage as <strong>CGPA &times; 9.5</strong> (the CBSE-style formula), and the reverse estimate is <strong>percentage &divide; 9.5</strong> - an 85% mark is roughly a CGPA of 8.9. Both are approximations that vary by university, and the &times;9.5 formula is only for the 10-point scale, never for a 4.0 GPA. For the 4.0 scale there is no official percentage conversion, so use the letter-grade table above as the estimate.</p>""",
        faqs,
        "<p><strong>Three courses - A (3 credits), B+ (4 credits), A- (3 credits)</strong> = 12 + 13.2 + 11.1 = 36.3 quality points over 10 credits, a <strong>GPA of 3.63</strong>.</p><p><strong>CGPA update:</strong> a CGPA of 3.50 over 60 completed credits, plus a 3.80 semester of 15 credits, becomes (210 + 57) &divide; 75 = a <strong>new CGPA of 3.56</strong>.</p>",
        jsonld=tool_jsonld_graph("GPA Calculator",
            "Free GPA and CGPA calculator: add your courses, letter grades, and credit hours to get your semester GPA on the 4.0 scale, update your cumulative CGPA, and convert a 10-point CGPA to a percentage.",
            "gpa-calculator", faqs))

def build_tip():
    calc = """
    <div class="tabs" id="tipPresets">
      <button type="button" data-tip="10">10%</button>
      <button type="button" data-tip="15">15%</button>
      <button type="button" data-tip="18" class="active">18%</button>
      <button type="button" data-tip="20">20%</button>
      <button type="button" data-tip="25">25%</button>
    </div>
    <div class="field-row">
      <div class="field"><label for="tBill">Bill amount before tax ($)</label><input id="tBill" type="number" value="86.40" step="any" min="0"></div>
      <div class="field"><label for="tTip">Tip (%) &mdash; or type your own</label><input id="tTip" type="number" value="18" step="any" min="0"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="tTax">Tax (%) &mdash; optional</label><input id="tTax" type="number" placeholder="e.g. 8" step="any" min="0"></div>
      <div class="field"><label for="tTipOn">Calculate tip on</label>
        <select id="tTipOn"><option value="before" selected>Bill before tax</option><option value="after">Bill + tax</option></select>
      </div>
    </div>
    <div class="field"><label for="tPeople">Split between (people)</label><input id="tPeople" type="number" value="4" step="1" min="1"></div>
    <button class="btn" id="tGo">Calculate Tip</button>
    <div class="result" id="tResult"><div class="big" id="tBig"></div><div class="detail" id="tDetail"></div></div>
    <script>
    (function(){
      function money(n){return '$'+(Math.round(n*100)/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
      function calc(){
        var bill=parseFloat(document.getElementById('tBill').value),
            rate=parseFloat(document.getElementById('tTip').value),
            taxPct=parseFloat(document.getElementById('tTax').value)||0,
            tipOn=document.getElementById('tTipOn').value,
            people=parseInt(document.getElementById('tPeople').value,10),
            r=document.getElementById('tResult');
        if(isNaN(bill)||isNaN(rate)||bill<0||rate<0||isNaN(people)||people<1){r.classList.remove('show');return;}
        var tax=bill*taxPct/100;
        var tipBase=(tipOn==='after')?(bill+tax):bill;
        var tip=tipBase*rate/100;
        var total=bill+tax+tip;
        document.getElementById('tBig').textContent=
          people>1?money(total/people)+' per person':money(total)+' total';
        var d='Tip: '+money(tip)+' ('+rate+'% of '+money(tipBase)+'). Total to pay: '+money(total)+'.';
        if(taxPct>0)d+=' Tax included: '+money(tax)+' on the '+money(bill)+' bill.';
        if(people>1)d+=' Split '+people+' ways: '+money(total/people)+' each, of which '+money(tip/people)+' is tip.';
        document.getElementById('tDetail').textContent=d;
        r.classList.add('show');
      }
      document.getElementById('tipPresets').addEventListener('click',function(e){
        if(e.target.dataset&&e.target.dataset.tip){
          document.getElementById('tTip').value=e.target.dataset.tip;
          document.querySelectorAll('#tipPresets button').forEach(function(b){
            b.classList.toggle('active',b===e.target);});
          calc();
        }
      });
      document.getElementById('tTip').addEventListener('input',function(){
        var v=document.getElementById('tTip').value;
        document.querySelectorAll('#tipPresets button').forEach(function(b){
          b.classList.toggle('active',b.dataset.tip===v);});
      });
      document.getElementById('tGo').addEventListener('click',calc);
      ['tBill','tTip','tTax','tPeople'].forEach(function(id){
        document.getElementById(id).addEventListener('input',calc);});
      document.getElementById('tTipOn').addEventListener('change',calc);
      calc();
    })();
    </script>"""
    faqs = [
        ("How do I calculate a tip?",
         "Tip = bill x tip percentage. On an $86.40 bill at 18%, the tip is $86.40 x 0.18 = $15.55, making the total $101.95."),
        ("How much should I tip?",
         "In the US, 15-20% of the bill is the usual range for table service at a restaurant - 15% for adequate service, 18-20% for good service, and 25% for exceptional service. Counter service, delivery, taxis, and haircuts follow different local habits, and customs vary a lot by country, so use the custom percentage field whenever the local norm is different."),
        ("Should the tip be calculated before or after tax?",
         "The usual convention is to tip on the pre-tax amount. On a $100 bill with 8% tax at 20%, tipping before tax gives a $20.00 tip and a $128.00 total; tipping after tax gives a $21.60 tip and a $129.60 total. Either is accepted - this calculator lets you choose."),
        ("How do I split a bill with the tip included?",
         "Add the tip (and any tax) to the bill first, then divide by the number of people. A $101.95 total split 4 ways is $25.49 each. Because rounded shares can be a cent or two over or under, one person usually absorbs the small difference so the exact total is covered."),
        ("How do I work out a 20% tip in my head?",
         "Find 10% by moving the decimal point one place left, then double it. On $86.40, 10% is $8.64, so 20% is $17.28. For 15%, take the 10% figure and add half of it: $8.64 + $4.32 = $12.96."),
    ]
    tool_page("tip-calculator", "&#129534;", "Tip Calculator",
        "Free tip calculator and bill splitter: enter the bill, pick a tip percentage, and split the total fairly - with optional tax and per-person tip amounts.",
        calc,
        "<h3>The formula</h3><p><strong>Tip = bill &times; tip %</strong>, then <strong>total = bill + tax + tip</strong>, and to split it, <strong>each person pays total &divide; number of people</strong>. Every amount is shown to exactly two decimals.</p><h3>Tipping on the bill before tax</h3><p>The standard convention is to work the tip out on the pre-tax amount, and that is the default here. If you prefer to tip on the full amount, switch \"Calculate tip on\" to Bill + tax. On a $100 bill with 8% tax at 20%, the choice is worth $1.60: a $20.00 tip before tax, or $21.60 after tax.</p><h3>Splitting fairly</h3><p>The tip is worked out on the whole bill first, then everything is divided evenly, so each person's share carries the same tip percentage. Rounded shares can leave a cent or two over or under the receipt total - the usual fix is for one person to absorb the difference.</p>",
        faqs,
        "<p><strong>An $86.40 bill at 18%, split between 4 people:</strong> the tip is $15.55 and the total is $101.95, so each person pays <strong>$25.49</strong> - of which $3.89 is their share of the tip.</p>",
        jsonld=tool_jsonld_graph("Tip Calculator",
            "Free tip calculator and bill splitter: enter the bill, pick a tip percentage, and split the total fairly - with optional tax and per-person tip amounts.",
            "tip-calculator", faqs))

# ---------------------------------------------------------------- STATIC PAGES
def static_page(slug, title, desc, inner):
    body = f"""
{HEADER}
<main class="wrap">
  <div class="crumbs"><a href="/">Home</a> &rsaquo; {html.escape(title)}</div>
  <section class="section">
    <h1 style="font-size:1.9rem;letter-spacing:-.02em">{html.escape(title)}</h1>
    <div class="prose">
{inner}
    </div>
  </section>
</main>
{footer()}"""
    write(slug + ".html", page_head(title + " | EverydayKit", desc, slug) + body)

def build_about():
    static_page("about", "About Us",
        "Learn about EverydayKit: free online calculators and converters for everyday life. No sign-up, no cost.",
        """<h3>What is EverydayKit?</h3>
<p>EverydayKit is a collection of free online tools for the calculations people do every day: working out a percentage discount, finding an exact age, counting days between dates, converting an hourly wage to a salary, or switching between measurement units.</p>
<h3>Why we built it</h3>
<p>We believe simple tools should be simple to use. No accounts, no downloads, no paywalls &mdash; just type a number and get a trustworthy answer, on any device.</p>
<h3>Our promise</h3>
<p><strong>Free, always.</strong> Every tool on this site is free to use.<br>
<strong>Private by design.</strong> Calculations run in your browser; we don't ask for personal information to use the tools.<br>
<strong>Accurate.</strong> Each calculator is tested against known values before release.</p>
<h3>What's next</h3>
<p>We plan to add more everyday tools over time &mdash; from finance helpers to health calculators. If there's a tool you'd like to see, <a href="/contact">let us know</a>.</p>""")

def build_contact():
    static_page("contact", "Contact",
        "Contact the EverydayKit team: suggest new tools, report a bug, or ask a question.",
        """<h3>Get in touch</h3>
<p>Have a tool request, found a bug, or just want to say hello? Fill in the form below &mdash; it composes a message you can copy or send with your email app. Nothing is stored on our servers.</p>
<div class="field"><label for="ctName">Your name</label><input id="ctName" type="text" placeholder="Jane Doe"></div>
<div class="field"><label for="ctTopic">Topic</label>
<select id="ctTopic"><option>Tool request</option><option>Bug report</option><option>Question</option><option>Other</option></select></div>
<div class="field"><label for="ctMsg">Message</label><input id="ctMsg" type="text" placeholder="How can we help?" style="min-height:44px"></div>
<div class="field-row">
  <div><button class="btn" id="ctCopy">Copy message</button></div>
  <div><button class="btn btn-ghost" id="ctMail">Open in email app</button></div>
</div>
<div class="result" id="ctResult"><div class="detail" id="ctDetail"></div></div>
<script>
(function(){
  var SITE_EMAIL = ""; /* site owner: set your support email here, e.g. "hello@example.com" */
  function compose(){
    var n=document.getElementById('ctName').value.trim(),
        t=document.getElementById('ctTopic').value,
        m=document.getElementById('ctMsg').value.trim();
    return '['+t+'] EverydayKit contact'+(n?' from '+n:'')+'\\n\\n'+m;
  }
  function show(msg){var r=document.getElementById('ctResult');
    document.getElementById('ctDetail').textContent=msg;r.classList.add('show');}
  document.getElementById('ctCopy').addEventListener('click',function(){
    var txt=compose();
    if(navigator.clipboard){navigator.clipboard.writeText(txt).then(function(){show('Message copied. Paste it wherever you like to reach us.');});}
    else{show(txt);}
  });
  document.getElementById('ctMail').addEventListener('click',function(){
    if(!SITE_EMAIL){show('Email is not configured yet on this demo. Use "Copy message" and send it to the site owner.');return;}
    window.location.href='mailto:'+SITE_EMAIL+'?subject='+encodeURIComponent('EverydayKit contact: '+document.getElementById('ctTopic').value)+'&body='+encodeURIComponent(compose());
  });
})();
</script>""")

def build_privacy():
    static_page("privacy-policy", "Privacy Policy",
        "EverydayKit privacy policy: what data we collect (almost none), cookies, and third-party hosting.",
        """<p><em>Last updated: October 18, 2026</em></p>
<h3>Summary</h3>
<p>EverydayKit's tools run entirely in your web browser. We do not require accounts, and we do not collect the numbers or dates you enter into the calculators.</p>
<h3>Information we collect</h3>
<p><strong>Tool inputs:</strong> never sent to us &mdash; all calculations happen on your device.<br>
<strong>Contact form:</strong> the form composes a message on your device; nothing is transmitted until you choose to send it yourself.<br>
<strong>Server logs:</strong> our hosting provider may log basic technical data (such as IP address and pages visited) to keep the site secure and reliable.</p>
<h3>Cookies</h3>
<p>We do not set advertising or tracking cookies. If we add analytics in the future, this policy will be updated.</p>
<h3>Third parties</h3>
<p>The site is hosted on Vercel, which processes technical data as described in its own privacy policy. We do not sell personal information to anyone.</p>
<h3>Children</h3>
<p>EverydayKit is a general-audience utility site and does not knowingly collect information from children.</p>
<h3>Changes</h3>
<p>If this policy changes, the updated version will be posted on this page with a new date.</p>
<h3>Contact</h3>
<p>Questions about privacy? Reach us via the <a href="/contact">contact page</a>.</p>""")

# ---------------------------------------------------------------- JS LOGIC (browser + node-testable)
CALCULATORS_JS = r"""/* EverydayKit shared calculator logic.
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
"""

# ---------------------------------------------------------------- SEO / CONFIG FILES
def build_extras():
    slugs = [""] + [s for s, _ in NAV_LINKS] + ["about", "contact", "privacy-policy"]
    urls = "\n".join(
        f"  <url><loc>{DOMAIN}/{s}</loc><changefreq>monthly</changefreq><priority>{'1.0' if s=='' else '0.8'}</priority></url>"
        for s in slugs)
    write("sitemap.xml",
          f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    rewrites = [{"source": "/" + s, "destination": "/" + (s if s else "index") + ".html"}
                for s in slugs if s != ""]
    write("vercel.json", json.dumps({"rewrites": rewrites}, indent=2) + "\n")
    write("styles.css", CSS)
    write("js/calculators.js", CALCULATORS_JS)

# ---------------------------------------------------------------- MAIN
if __name__ == "__main__":
    build_extras()
    build_home()
    build_percentage()
    build_age()
    build_datediff()
    build_salary()
    build_converter()
    build_sqft()
    build_concrete()
    build_wordcounter()
    build_gpa()
    build_tip()
    build_about()
    build_contact()
    build_privacy()
    print("BUILD COMPLETE")
