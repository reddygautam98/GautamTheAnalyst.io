"""Regenerates all 7 HTML pages. Run:  python build.py
Edit copy / links here, then rebuild. Diagrams come from flows.py."""
import html, json
import flows as F

SITE = "https://reddygautam98.github.io/GautamTheAnalyst.io/"
GH = "https://github.com/reddygautam98/"
LI = "https://www.linkedin.com/in/gautam-reddy-analyst"
HR = "https://www.hackerrank.com/profile/reddygautam98"
EMAIL = "gautamreddy098@gmail.com"
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600&display=swap"
NAV = [("projects.html", "Projects"), ("samples/index.html", "BA samples"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Contact")]

# Core BA & technical skills for single-row marquee
MARQ_ITEMS = ["Requirements Gathering", "BRD / FRD / SRS", "User Stories & BDD", "Traceability Matrix (RTM)", "Process Modelling (BPMN / UML)", "Gap Analysis", "REST API Integration", "SQL (PostgreSQL)", "Python (Pandas)", "Power BI & DAX", "UAT & Defect Triage", "Agile / Scrum"]

ROLES_ROT = ["Requirements Gathering", "BRD / FRD & User Stories", "REST API & System Integration", "SQL & Python Analysis", "Power BI & KPI Dashboards", "Settlement & Reconciliation", "UAT & Agile Delivery"]

def ext(u, t): return f'<a href="{u}" target="_blank" rel="noopener noreferrer">{t} <span class="sr-only">(opens in new tab)</span>&rarr;</a>'
def rv(i=0, base=0.0, step=0.07): return f'rv" style="--d:{base + i * step:.2f}s'

ICO_MAIL = '<svg class="ico-gmail" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="#4285F4" d="M3.2 5.5A2.5 2.5 0 0 0 .7 8v10.5A2.5 2.5 0 0 0 3.2 21H5V11.25L3.2 9.8z"/><path fill="#34A853" d="M20.8 5.5a2.5 2.5 0 0 1 2.5 2.5V18.5a2.5 2.5 0 0 1-2.5 2.5H19V11.25l1.8-1.45z"/><path fill="#FBBC05" d="M19 11.25L12 16.5 5 11.25V21h14z"/><path fill="#EA4335" d="M3.2 5.5c-.8 0-1.5.5-1.8 1.25L12 13.5l10.6-6.75c-.3-.75-1-1.25-1.8-1.25z"/></svg>'
ICO_LI = '<svg class="ico-li" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#ffffff" d="M19 19h-3.14v-4.9c0-1.17-.02-2.67-1.63-2.67-1.63 0-1.88 1.27-1.88 2.58V19H9.21V9h3.01v1.37h.04c.42-.79 1.44-1.63 2.96-1.63 3.17 0 3.75 2.09 3.75 4.8V19zM5.34 7.63a1.74 1.74 0 1 1 0-3.48 1.74 1.74 0 0 1 0 3.48zM6.91 19H3.77V9h3.14v10z"/></svg>'
ICO_GH = '<svg class="ico-gh" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
ICO_HR = '<svg class="ico-hr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#00EA64"/><path fill="#ffffff" d="M9.95 8.002h1.805c.061 0 .111.05.111.111v7.767c0 .061-.05.111-.11.111H9.95c-.061 0-.111-.05-.111-.11v-2.87H7.894v2.87c0 .06-.05.11-.11.11H5.976a.11.11 0 01-.11-.11V8.112c0-.06.05-.11.11-.11h1.806c.061 0 .11.05.11.11v2.869H9.84v-2.87c0-.06.05-.11.11-.11zm2.999 0h5.778c.061 0 .111.05.111.11v7.767a.11.11 0 01-.11.112h-5.78a.11.11 0 01-.11-.11V8.111c0-.06.05-.11.11-.11z"/></svg>'
ICO_LOC = '<svg class="ico-loc" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'

def page(path, title, desc, body, p="", cur="", ld="", robots="index, follow, max-image-preview:large, max-snippet:-1"):
    url = SITE if path == "index.html" else SITE + path
    home = p if p else "./"
    if robots.startswith("noindex"): url_tags = ""
    else: url_tags = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
    res_cur = ' aria-current="page"' if cur == "resume.html" else ""
    nav = "".join('<a href="%s%s"%s>%s</a>' % (p, h, ' aria-current="page"' if h == cur else "", t) for h, t in NAV)
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="Gautam Reddy">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:site_name" content="Gautam Reddy - Business Analyst Portfolio">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{SITE}assets/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Gautam Reddy, Business Analyst in Bengaluru: fintech and BFSI requirements, BRD/FRD, SQL and UAT">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}assets/og-card.png">
<meta name="theme-color" content="#f4f6fb" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0d13" media="(prefers-color-scheme: dark)">
{url_tags}<link rel="icon" href="{p}assets/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("gr-theme")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{p}assets/style.css?v=24">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="{home}"><img src="{p}assets/mark.svg" alt="" width="30" height="30">Gautam Reddy</a>
<nav class="nav" id="nav" aria-label="Main">{nav}<a href="{p}resume.html" class="nav-resume-btn"{res_cur}>Resume</a></nav>
<div class="tools"><button class="icon-btn" id="theme" type="button" aria-label="Switch theme" aria-pressed="false"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button></div>
<button class="icon-btn menu-btn" id="menu" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">&#9776;</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap foot">
<div>&copy; <span data-year>2026</span> Gautam Reddy &bull; Business Analyst, Bengaluru, India (IST / UTC+5:30) &bull; Updated 2026.<br>Sample artifacts on this site are fictional and are labelled as such.</div>
<nav aria-label="Footer"><a href="{home}">Home</a><a href="{p}about.html">About</a><a href="{p}services.html">Services</a><a href="{p}projects.html">Projects</a><a href="{p}samples/index.html">BA samples</a><a href="{p}resume.html">Resume</a><a href="{p}contact.html">Contact</a>{ext(GH, "GitHub")}{ext(LI, "LinkedIn")}{ext(HR, "HackerRank")}<a href="mailto:{EMAIL}">Email</a><a href="#main" class="back-to-top" title="Back to top">&uarr; Top</a></nav>
</div></footer>

<script src="{p}assets/vendor/lenis.min.js" defer></script>
<script src="{p}assets/site.js?v=24" defer></script>
</body>
</html>
'''

def cta(p="", h="Hiring a Business Analyst, or scoping a piece of work?", t="Share the role or the problem and the outcome you want. I reply with context."):
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta has-flow" data-tilt>{F.lifecycle("c" + str(sum(map(ord, h)) % 9973)).replace("xMidYMid meet", "xMidYMid slice")}<div class="cta-in"><div><h2>{h}</h2><p>{t}</p></div><a class="btn btn-primary" href="{p}contact.html">Get in touch</a></div></div></div></section>'''

def head(crumb, h, lead, flow, p=""):
    return f'<section class="page-head has-flow">{flow}<div class="wrap"><div class="crumbs rv"><a href="{p or "./"}">Home</a> / {crumb}</div><h1 class="{rv(1)}">{h}</h1><p class="lead {rv(2)}">{lead}</p></div></section>'

def sh(n, tag, h, p=None):
    return f'<div class="sec-head"><div class="eyebrow {rv(0)}"><b>{n:02d}</b>{tag}</div><h2 class="{rv(1)}">{h}</h2>' + (f'<p class="{rv(2)}">{p}</p>' if p else "") + '</div>'

def tags(l): return '<ul class="tags">' + "".join(f"<li>{t}</li>" for t in l) + '</ul>'

# ---------------------------------------------------------------- projects (BA relevant first)
GHIMG = "https://opengraph.githubassets.com/1/reddygautam98/"
PROJECTS = [
 ("analytics", "Personal Analytics Project", "Sales Data Analysis", "SQL analysis of product performance, the leading salesperson by region, high-performing regions and high-value first-quarter transactions.", ["SQL"], GH + "Sales-data-analysis"),
 ("analytics", "Personal Analytics Project", "Loan Data Analytics", "SQL-based financial analysis covering loan interest rates, loan grades, default patterns, annual issuance, repayment behaviour and state-level risk trends.", ["SQL", "Finance"], GH + "Loan-data-analytics"),
 ("analytics", "Personal Analytics Project", "Sales Forecasting Report", "Reviews sales performance, monthly profit trends and shipment-efficiency measures that are relevant to planning.", ["Reporting"], GH + "Sales-Forecasting-Report"),
 ("analytics", "Power BI Workforce Analytics", "HR Data Analysis", "Power BI workforce analysis covering employee performance, turnover, tenure and HR trends.", ["Power BI"], GH + "Hr-data-analysis"),
 ("bi", "BI Reporting Prototype", "Business Insights Report", "A structured business report for reviewing sales performance, financial indicators and selected KPIs.", ["BI", "KPIs"], GH + "Business_Insights_Report"),
 ("bi", "BI Dashboard Prototype", "GameZone Business Intelligence", "A business-intelligence example for exploring performance and presenting metrics. The repository README has the exact implementation and setup.", ["BI"], GH + "gamezone-business-intelligence"),
 ("data", "Data Pipeline Project", "MetaLayer", "A data-engineering workflow organised around orchestration and structured processing layers. The README covers architecture, validation and setup.", ["Pipelines"], GH + "MetaLayer"),
 ("ai", "Experimental AI Prototype", "ClinChat-style RAG App", "An experimental retrieval-augmented generation prototype. Read the README for implementation details and limits. It is not a clinically validated product.", ["RAG", "Prototype"], GH + "ClinChat-style-RAG-app"),
 ("writing", "Writing & BA Notes", "Daily Posts & Notes", "Knowledge-sharing notes and learning summaries on analysis and professional practice.", ["Notes"], GH + "daily_post/blob/main/read.md"),
]

import itertools
_n = itertools.count()
def repo_of(u): return u[len(GH):].split("/")[0]

LOCAL_PROJECT_IMAGES = {
    "Sales-data-analysis": "assets/projects/Sales-data-analysis.jpg",
    "Loan-data-analytics": "assets/projects/Loan-data-analytics.jpg",
    "Sales-Forecasting-Report": "assets/projects/Sales-Forecasting-Report.jpg",
    "Business_Insights_Report": "assets/projects/Business_Insights_Report.jpg",
    "Hr-data-analysis": "assets/projects/Hr-data-analysis.png",
    "ClinChat-style-RAG-app": "assets/projects/ClinChat-style-RAG-app.png",
    "gamezone-business-intelligence": "assets/projects/gamezone-business-intelligence.png",
    "MetaLayer": "assets/projects/MetaLayer.png",
    "daily_post": "assets/projects/daily_post.png"
}

def pcard(c, i=0, base=0.0):
    k, cat, t, d, tg, u = c
    repo = repo_of(u)
    img_src = LOCAL_PROJECT_IMAGES.get(repo, f"{GHIMG}{repo}")
    img = f'<img src="{img_src}" alt="{html.escape(t)} project screenshot ({html.escape(cat.lower())})" width="1200" height="600" loading="lazy" decoding="async">'
    lbl = f'View repository for {html.escape(t)} on GitHub (opens in new tab)' if k != 'writing' else f'Read notes for {html.escape(t)} on GitHub (opens in new tab)'
    txt = 'Read notes' if k == 'writing' else 'View repository'
    return f'''<article class="card pcard {rv(i, base)}" data-cat="{k}"><a class="thumb" href="{u}" target="_blank" rel="noopener noreferrer" tabindex="-1" aria-hidden="true"><span class="ph">{F.mini("m" + str(next(_n)))}<em>{html.escape(t)}</em></span>{img}</a><div class="pbody"><span class="cat">{cat}</span><h3>{t}</h3><p>{d}</p>{tags(tg)}<a class="more" href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{lbl}">{txt} <span class="sr-only">(opens in new tab)</span>&#8599;</a></div></article>'''

TRACE = [
    ("BR-01", "Single operational view", ["FR-002", "FR-004"], ["US-01", "US-03"], ["TC-001", "TC-002"]),
    ("BR-02", "Identify unmatched records", ["FR-005", "FR-006", "FR-007"], ["US-03", "US-04"], ["TC-003", "TC-004", "TC-005"]),
    ("BR-03", "Assign, comment and resolve", ["FR-008", "FR-009", "FR-010", "FR-011"], ["US-05", "US-06", "US-07"], ["TC-006", "TC-007", "TC-008"]),
]

def _ids(items):
    return '<span class="idrow">' + "".join(f'<span class="id" data-id="{i}">{i}</span>' for i in items) + '</span>'

def trace():
    rows = ""
    for br, label, frs, uss, tcs in TRACE:
        links = " ".join([br] + frs + uss + tcs)
        rows += (f'<tr tabindex="0" data-links="{links}" aria-label="Trace {br}: {label}">'
                 f'<td><span class="id" data-id="{br}">{br}</span><br>{label}</td>'
                 f'<td>{_ids(frs)}</td><td>{_ids(uss)}</td><td>{_ids(tcs)}</td></tr>\n')
    return (f'''<div class="trace hero-slider" id="heroSlider" aria-label="PayTrack deliverables showcase">
<div class="trace-top slider-top">
  <div class="slider-tabs" role="tablist" aria-label="Deliverable slides">
    <button class="slider-tab is-active" role="tab" id="tab-0" aria-selected="true" aria-controls="slide-0" data-slide="0" tabindex="0" type="button"><span class="tab-badge">01</span> Traceability</button>
    <button class="slider-tab" role="tab" id="tab-1" aria-selected="false" aria-controls="slide-1" data-slide="1" tabindex="-1" type="button"><span class="tab-badge">02</span> User story</button>
    <button class="slider-tab" role="tab" id="tab-2" aria-selected="false" aria-controls="slide-2" data-slide="2" tabindex="-1" type="button"><span class="tab-badge">03</span> REST API</button>
    <button class="slider-tab" role="tab" id="tab-3" aria-selected="false" aria-controls="slide-3" data-slide="3" tabindex="-1" type="button"><span class="tab-badge">04</span> SQL logic</button>
  </div>
  <div class="slider-nav-ctrls">
    <button class="slider-arrow" id="slidePrev" type="button" aria-label="Previous slide">&#8249;</button>
    <span class="slider-counter" id="slideCount" aria-live="polite">1 / 4</span>
    <button class="slider-arrow" id="slideNext" type="button" aria-label="Next slide">&#8250;</button>
  </div>
</div>

<div class="slider-slides">
  <!-- Slide 1: Traceability matrix -->
  <div class="slider-slide is-active" id="slide-0" role="tabpanel" aria-labelledby="tab-0" data-index="0">
    <div class="slide-subhead"><b>PayTrack traceability extract</b><span>Fictional sample &bull; Hover, tap or focus a row to trace</span></div>
    <div class="tbl-wrap"><table><thead><tr><th scope="col">Business requirement</th><th scope="col">Functional</th><th scope="col">Stories</th><th scope="col">Tests</th></tr></thead><tbody>
{rows}</tbody></table></div>
    <div class="trace-foot">Every requirement links forward to a story and a test. <a href="samples/index.html">Open the samples &rarr;</a></div>
  </div>

  <!-- Slide 2: User story & BDD -->
  <div class="slider-slide" id="slide-1" role="tabpanel" aria-labelledby="tab-1" data-index="1" hidden>
    <div class="slide-subhead"><b>US-03: Real-Time Payment Mismatch Triage</b><span>User story &bull; Gherkin acceptance criteria</span></div>
    <div class="slide-content-wrap">
      <div class="us-story-card">
        <div class="us-meta"><span class="kwd-tag kwd-story">USER STORY</span><span class="mono-meta">Sprint 24 &bull; Priority: Must</span></div>
        <p class="us-text"><b>As a</b> Settlement Operations Analyst,<br><b>I want</b> unmatched transaction exceptions flagged within 5 minutes of ingestion,<br><b>So that</b> discrepancies are triaged and resolved before gateway cutoff.</p>
      </div>
      <div class="bdd-block">
        <div class="bdd-head"><span class="kwd-tag kwd-bdd">GHERKIN SCENARIO</span><span class="mono-meta">Scenario: Unmatched gateway authorization code</span></div>
        <div class="bdd-code">
          <div class="bdd-line"><span class="bdd-kw">Given</span> <span class="bdd-tx">internal order #1089 has status <mark class="m-val">'PAID'</mark> via Razorpay</span></div>
          <div class="bdd-line"><span class="bdd-kw">When</span> <span class="bdd-tx">bank settlement feed arrives with missing auth code</span></div>
          <div class="bdd-line"><span class="bdd-kw">Then</span> <span class="bdd-tx">generate exception record with severity <mark class="m-warn">'HIGH'</mark></span></div>
          <div class="bdd-line"><span class="bdd-kw">And</span> <span class="bdd-tx">route to reconciliation queue with a 4-hour SLA timer</span></div>
        </div>
      </div>
    </div>
    <div class="trace-foot">Gherkin criteria ready for Cucumber/BDD automation. <a href="samples/index.html#user-stories">View stories &rarr;</a></div>
  </div>

  <!-- Slide 3: REST API flow -->
  <div class="slider-slide" id="slide-2" role="tabpanel" aria-labelledby="tab-2" data-index="2" hidden>
    <div class="slide-subhead"><b>PayTrack REST API &amp; Webhook Integration</b><span>POST /v1/reconcile/batch &bull; Idempotent contract</span></div>
    <div class="slide-content-wrap">
      <div class="api-pipeline">
        <div class="api-node">
          <span class="node-step">01</span>
          <div class="node-info">
            <span class="node-verb verb-post">POST</span>
            <span class="node-path">/v1/payments/auth</span>
            <span class="node-detail">Header: Idempotency-Key &bull; 200 OK</span>
          </div>
        </div>
        <div class="api-arrow" aria-hidden="true">&rarr;</div>
        <div class="api-node">
          <span class="node-step">02</span>
          <div class="node-info">
            <span class="node-verb verb-event">EVENT</span>
            <span class="node-path">webhook.txn_captured</span>
            <span class="node-detail">HMAC-SHA256 signature verified</span>
          </div>
        </div>
        <div class="api-arrow" aria-hidden="true">&rarr;</div>
        <div class="api-node">
          <span class="node-step">03</span>
          <div class="node-info">
            <span class="node-verb verb-match">RECON</span>
            <span class="node-path">T+0 Window Match</span>
            <span class="node-detail">Auto-reconciliation run: 99.8% match</span>
          </div>
        </div>
      </div>
      <div class="schema-preview">
        <div class="schema-head"><span class="kwd-tag kwd-api">PAYLOAD CONTRACT</span><span class="mono-meta">application/json &bull; Response schema</span></div>
        <pre class="schema-json"><code>&#123;
  <span class="j-k">"batch_id"</span>: <span class="j-s">"REC-2026-9420"</span>,
  <span class="j-k">"total_records"</span>: <span class="j-n">1423</span>,
  <span class="j-k">"matched"</span>: <span class="j-n">1420</span>,
  <span class="j-k">"unmatched_exceptions"</span>: <span class="j-n">3</span>,
  <span class="j-k">"sla_status"</span>: <span class="j-s">"WITHIN_SLA"</span>
&#125;</code></pre>
      </div>
    </div>
    <div class="trace-foot">Documented with OpenAPI 3.0 &amp; Postman collections. <a href="samples/index.html#rest-api">View API specs &rarr;</a></div>
  </div>

  <!-- Slide 4: SQL query -->
  <div class="slider-slide" id="slide-3" role="tabpanel" aria-labelledby="tab-3" data-index="3" hidden>
    <div class="slide-subhead"><b>PostgreSQL Exception Detection Query</b><span>Unsettled transactions nearing SLA breach threshold</span></div>
    <div class="slide-content-wrap">
      <div class="sql-code-box">
        <div class="sql-head"><span class="kwd-tag kwd-sql">SQL SCRIPT</span><span class="mono-meta">sample_reconciliation_queries.sql</span></div>
        <pre class="sql-view"><code><span class="s-c">-- Surface un-reconciled records approaching 4h SLA breach</span>
<span class="s-k">SELECT</span> t.txn_id, t.amount, t.currency,
       ROUND(EXTRACT(EPOCH <span class="s-k">FROM</span> (NOW() - t.created_at))/3600, 1) <span class="s-k">AS</span> pending_hrs,
       <span class="s-k">CASE</span>
         <span class="s-k">WHEN</span> b.bank_ref <span class="s-k">IS NULL THEN</span> <span class="s-s">'MISSING_BANK_FEED'</span>
         <span class="s-k">WHEN</span> b.amount != t.amount <span class="s-k">THEN</span> <span class="s-s">'AMOUNT_MISMATCH'</span>
       <span class="s-k">END AS</span> discrepancy_reason
<span class="s-k">FROM</span> core_transactions t
<span class="s-k">LEFT JOIN</span> bank_settlement_feed b <span class="s-k">ON</span> t.gateway_ref = b.gateway_ref
<span class="s-k">WHERE</span> t.status = <span class="s-s">'PENDING_SETTLEMENT'</span>
  <span class="s-k">AND</span> (NOW() - t.created_at) &gt; <span class="s-k">INTERVAL</span> <span class="s-s">'3 hours'</span>
<span class="s-k">ORDER BY</span> pending_hrs <span class="s-k">DESC LIMIT</span> 4;</code></pre>
      </div>
    </div>
    <div class="trace-foot">Extracts from PayTrack PostgreSQL query templates. <a href="samples/index.html#sql">View SQL repository &rarr;</a></div>
  </div>
</div>
</div>''')

def marquee():
    items = "".join(f"<li>{k}</li>" for k in MARQ_ITEMS)
    return f'''<section class="marq-wrap" aria-label="Skills and keywords">
<div class="marq"><ul class="marq-track">{items}</ul><ul class="marq-track" aria-hidden="true">{items}</ul></div>
<button class="marq-toggle" id="marqToggle" type="button" aria-label="Pause marquee animation" aria-pressed="false">&#9646;&#9646; Pause</button>
</section>'''

ICO_PHASE1 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICO_PHASE2 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
ICO_PHASE3 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>'
ICO_PHASE4 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'

METHOD_STEPS = [
    (1, "Phase 1: Discover", "Workshops turn scattered requests into one agreed problem statement with assumptions, constraints and named decision owners.", ICO_PHASE1, 20, "+", "workshops run"),
    (2, "Phase 2: Define", "BRD and FRD, business rules, user stories and acceptance criteria, linked to process, API and data flows.", ICO_PHASE2, 2, "", "payment-gateway integrations documented"),
    (3, "Phase 3: Validate", "Traceability from requirement to test, UAT scenarios, expected results and defect triage with QA & Engineering.", ICO_PHASE3, 350, "+", "test cases coordinated"),
    (4, "Phase 4: Hand over", "Decisions, risks, open questions and limitations are recorded so delivery proceeds with confidence.", ICO_PHASE4, 0, "", "critical defects reported")
]

SERVICE_STEPS = [
    (1, "Phase 1: Understand", "Discuss the problem, users, data or systems, constraints, deadlines and what success looks like.", ICO_PHASE1, None, "", "Alignment workshop"),
    (2, "Phase 2: Scope", "Agree deliverables, assumptions, dependencies, review points, responsibilities and a practical timeline.", ICO_PHASE2, None, "", "Scope agreement"),
    (3, "Phase 3: Deliver", "Share drafts, analysis or requirements in checkpoints; collect feedback and resolve agreed changes.", ICO_PHASE3, None, "", "Review checkpoints"),
    (4, "Phase 4: Hand over", "Review against acceptance criteria and provide agreed documents, findings or handover notes.", ICO_PHASE4, None, "", "Deliverable sign-off")
]

def make_steps(items):
    out = []
    total = len(items)
    for i, (num, title, desc, icon_svg, stat_val, stat_suf, stat_lbl) in enumerate(items):
        arrow_html = ""
        if i < total - 1:
            arrow_html = f'''<div class="step-arrow-link" aria-hidden="true">
<div class="step-arrow-stem"></div>
<div class="step-arrow-badge">
<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
</div>
</div>'''
        out.append(f'''<li class="step-card step-{num} {rv(i)}">
<div class="step-top">
<div class="step-badge" aria-label="Phase {num}: {title}">
<span class="step-num">0{num}</span>
<span class="step-ico">{icon_svg}</span>
</div>
<span class="step-phase-label">Phase {num} of {total}</span>
</div>
<div class="step-head-row">
<h3>{title.split(': ', 1)[1] if ': ' in title else title}</h3>
</div>
<p>{desc}</p>
<div class="step-metric-foot">
<span class="step-metric-chip">{(f'<b data-count="{stat_val}" data-suf="{stat_suf}">{stat_val}{stat_suf}</b> ') if stat_val is not None else ''}<span>{stat_lbl}</span></span>
</div>
{arrow_html}
</li>''')
    return "".join(out)

BA_WORKFLOW = [
    ("Stakeholder Management", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'),
    ("Requirements Gathering & Elicitation", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><path d="M11 8v6M8 11h6"/></svg>'),
    ("Requirements Analysis", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'),
    ("Impact Analysis", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'),
    ("Functional & Non-Functional Requirements", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>'),
    ("BRD / FRD", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'),
    ("User Stories & Use Cases", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>'),
    ("BDD Acceptance Criteria", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>'),
    ("Traceability Matrix (RTM)", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'),
    ("Validation & Sign-off", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>')
]

PROCESS_WORKFLOW = [
    ("AS-IS / TO-BE Analysis", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8L22 12L18 16"/><path d="M2 12H22"/></svg>'),
    ("Gap Analysis", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="6" cy="12" r="3"/><circle cx="18" cy="12" r="3"/></svg>'),
    ("Root Cause Analysis", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg>'),
    ("Process Mapping (BPMN / UML)", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><path d="M10 6.5h4M17.5 10v4"/></svg>'),
    ("Business Rules", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M9 15l2 2 4-4"/></svg>'),
    ("Data Mapping", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'),
    ("MoSCoW Prioritization", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'),
    ("System Workflow Documentation", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>')
]

AGILE_WORKFLOW = [
    ("SDLC", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'),
    ("Agile / Scrum", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>'),
    ("Sprint Planning", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'),
    ("Backlog Refinement", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'),
    ("Change Management", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>'),
    ("UAT Coordination", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>'),
    ("Testing (Functional, Regression, Integration)", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="m9 15 2 2 4-4"/></svg>'),
    ("Defect Triage", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>')
]

TECH_WORKFLOW = [
    ("REST API Requirements", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="2" y1="12" x2="22" y2="12"/></svg>'),
    ("API Contract Review", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="m9 15 2 2 4-4"/></svg>'),
    ("System Integration Requirements", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/><line x1="12" y1="10" x2="12" y2="14"/></svg>'),
    ("SQL", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'),
    ("Python (Pandas)", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'),
    ("Excel", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>'),
    ("Power BI", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>'),
    ("JIRA", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="m9 12 2 2 4-4"/></svg>'),
    ("Confluence", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'),
    ("Figma", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"/><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"/><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"/><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"/></svg>'),
    ("Postman", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 14.14 14.14"/></svg>')
]

def workflow_tags(items):
    out = []
    total = len(items)
    for i, (name, icon) in enumerate(items):
        arrow = f'<span class="wf-arrow" aria-hidden="true">&#10142;</span>' if i < total - 1 else ''
        out.append(f'<span class="wf-item"><span class="wf-step"><span class="wf-num">{i+1}</span><span class="wf-ico" aria-hidden="true">{icon}</span><span>{name}</span></span>{arrow}</span>')
    return f'<div class="wf-flow">{"".join(out)}</div>'

def paytrack_wireframe_svg():
    return '''<div class="feat-preview" aria-label="PayTrack Reconciliation UI Preview">
  <div class="wf-browser">
    <div class="wf-browser-bar">
      <div class="wf-browser-dots"><span class="wf-dot red"></span><span class="wf-dot yellow"></span><span class="wf-dot green"></span></div>
      <div class="wf-browser-addr"><span>https://ops.paytrack.internal/reconciliation</span></div>
      <div class="wf-browser-badge">BA Wireframe</div>
    </div>
    <div class="wf-screen">
      <div class="wf-side">
        <div class="wf-side-logo"><span class="wf-side-icon"></span><span class="wf-side-name">PayTrack</span></div>
        <div class="wf-side-nav">
          <div class="wf-nav-item active"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Exceptions (3)</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Transactions</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Audit Log</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">RTM & Trace</span></div>
        </div>
      </div>
      <div class="wf-main">
        <div class="wf-main-head">
          <div><div class="wf-main-title">Reconciliation Exceptions</div><div class="wf-main-sub">FR-005 &bull; Real-time settlement reconciliation</div></div>
          <div class="wf-main-actions"><span class="wf-btn wf-btn-primary">Resolve Case</span><span class="wf-btn">Export CSV</span></div>
        </div>
        <div class="wf-kpis">
          <div class="wf-kpi-card"><span class="wf-kpi-val">100K+</span><span class="wf-kpi-lbl">Analysed Txns</span></div>
          <div class="wf-kpi-card warn"><span class="wf-kpi-val">3</span><span class="wf-kpi-lbl">SLA Breaches</span></div>
          <div class="wf-kpi-card ok"><span class="wf-kpi-val">99.4%</span><span class="wf-kpi-lbl">Reconciled</span></div>
        </div>
        <div class="wf-table">
          <div class="wf-tr wf-th"><span>TXN_ID</span><span>GATEWAY</span><span>AMOUNT</span><span>STATUS</span><span>SLA DUE</span></div>
          <div class="wf-tr"><span class="wf-td-code">TXN_9841</span><span>Stripe API</span><span>$1,420.00</span><span class="wf-badge-warn">WARN (Amount)</span><span>2h 15m</span></div>
          <div class="wf-tr"><span class="wf-td-code">TXN_9842</span><span>Razorpay</span><span>$850.50</span><span class="wf-badge-ok">RECONCILED</span><span>&mdash;</span></div>
          <div class="wf-tr"><span class="wf-td-code">TXN_9843</span><span>Adyen Webhook</span><span>$3,190.00</span><span class="wf-badge-err">ERROR (Timeout)</span><span>Overdue</span></div>
        </div>
      </div>
    </div>
  </div>
</div>'''

def index():
    rot = "".join(f"<span>{r}</span>" for r in ROLES_ROT)
    toolkit_cards = [
        ("Business Analysis", "Chronological Lifecycle: Elicitation &#10142; Analysis &#10142; Specs &#10142; Agile &#10142; Sign-off", BA_WORKFLOW),
        ("Process Analysis & Documentation", "Process Stream: AS-IS Discovery &#10142; Root Cause &#10142; BPMN Modelling &#10142; Specs", PROCESS_WORKFLOW),
        ("Agile, Testing & Delivery", "Delivery Sprint: SDLC &#10142; Planning &#10142; Testing &#10142; UAT &amp; Release", AGILE_WORKFLOW),
        ("Technical Skills & Tools", "Toolchain: Design &#10142; APIs &amp; Contracts &#10142; Analysis &amp; BI", TECH_WORKFLOW)
    ]
    tk = "".join(f'<div class="card kit {rv(i)}"><div class="kit-head"><h3>{g}</h3><span class="kit-sub">{sub}</span></div>{workflow_tags(wf)}</div>' for i, (g, sub, wf) in enumerate(toolkit_cards))
    return f'''
<section class="hero has-flow">{F.lifecycle("h")}<div class="wrap hero-grid">
<div>
<div class="status rv"><i></i><span>Available for global remote, hybrid &amp; full-time roles</span></div>
<h1 class="{rv(1)}">Business Analyst in Bengaluru who turns requirements into <span class="grad">testable specs.</span></h1>
<p class="rot-line {rv(2)}"><span class="rot-lb">Right now:</span><span class="rot" data-rot aria-live="off">{rot}</span></p>
<p class="lead {rv(3)}">4+ years in fintech and BFSI: translating business needs into clear, testable functional and non-functional requirements, user stories and BDD acceptance criteria, backed by SQL and Python analysis.</p>
<div class="actions {rv(4)}"><a class="btn btn-primary" href="samples/index.html">View BA samples <span class="arr" aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="resume.html">View resume <span class="arr" aria-hidden="true">&rarr;</span></a></div>
<p class="hero-proof-line {rv(5)}"><span class="h-dot"></span> 4+ yrs BA experience &bull; Payments &amp; Fintech &bull; 2 payment gateway integrations</p>
</div>
<div class="scene {rv(2)}" data-scene><div class="stage">
<a href="samples/index.html#brd" class="plane plane-brd" style="--i:3;--k:var(--c-brd)" title="View BRD sample document"><b>BRD</b><span>Business need</span></a><a href="samples/index.html#frd" class="plane plane-frd" style="--i:2;--k:var(--c-frd)" title="View FRD sample document"><b>FRD</b><span>System behaviour</span></a><a href="samples/index.html#user-stories" class="plane plane-story" style="--i:1;--k:var(--c-story)" title="View User Stories sample document"><b>Stories</b><span>Acceptance criteria</span></a>
{trace()}
<a href="samples/index.html#user-stories" class="f3d chip-story" style="--z:80px;top:0px;left:0px;--dl:0s;--k:var(--c-story)" title="View User Stories sample document">User stories</a>
<a href="samples/index.html#uat" class="f3d chip-test" style="--z:90px;top:40%;right:0px;--dl:.8s;--k:var(--c-test)" title="View UAT &amp; test cases sample document">UAT</a>
<a href="samples/index.html#sql" class="f3d chip-sql" style="--z:70px;bottom:0px;left:15%;--dl:1.4s;--k:var(--c-sql)" title="View SQL queries &amp; data model sample">SQL</a>
<a href="samples/index.html#rest-api" class="f3d chip-api alt" style="--z:85px;top:0px;right:15%;--dl:.4s;--k:var(--c-api)" title="View REST API sequence diagram &amp; specifications">REST API</a>
<a href="samples/index.html#power-bi" class="f3d chip-bi alt" style="--z:75px;bottom:0px;right:10%;--dl:1.9s;--k:var(--c-api)" title="View Power BI reporting sample &amp; dashboard">Power BI</a>
</div></div>
</div></section>

{marquee()}

<section class="sec" id="proof"><div class="wrap">
{sh(1, "Proof", "Business analyst results from past delivery work")}
<div class="proof">
<div class="proof-card proof-card-1 {rv(0)}"><b data-count="100" data-suf="K+">100K+</b><span class="source-tag">Marolix &bull; SQL analysis</span><span>transaction records analysed with SQL and Python, surfacing 3 recurring SLA-breach patterns</span></div>
<div class="proof-card proof-card-2 {rv(1)}"><b data-count="350" data-suf="+">350+</b><span class="source-tag">QA &amp; UAT coordination</span><span>test cases coordinated in Jira, with zero critical defects reported</span></div>
<div class="proof-card proof-card-3 {rv(2)}"><b data-count="20" data-suf="+">20+</b><span class="source-tag">13+ cross-functional stakeholders</span><span>workshops that aligned stakeholders on business &amp; functional requirements</span></div>
<div class="proof-card proof-card-4 {rv(3)}"><b data-count="2" data-suf="">2</b><span class="source-tag">Payment gateway integrations</span><span>payment-gateway integrations documented with UML flows for Engineering and QA</span></div>
</div>
<p class="note">Figures come from my resume and describe past roles and projects. They are not a guarantee of future outcomes.</p>
</div></section>

<section class="sec band has-flow" id="method">{F.swim("m")}<div class="wrap">
{sh(2, "Method", "How a requirement travels from idea to sign-off", "The same path the sample documents follow.")}
<ol class="steps">{make_steps(METHOD_STEPS)}</ol></div></section>

<section class="sec has-flow" id="work">{F.erd("w")}<div class="wrap">
{sh(3, "Selected work", "Case study and projects", "A fictional end-to-end BA case study, plus personal analytics and data projects. Each card opens its repository.")}
<div class="feature {rv(0)}" data-tilt>
{paytrack_wireframe_svg()}
<div><span class="cat feat-badge">Featured Case Study</span><h3>PayTrack: payment reconciliation, from BRD to UAT</h3><p class="muted"><strong>Problem &bull; Role &bull; Result:</strong> Operations teams struggle to investigate unmatched gateway and internal payment records. As the Business Analyst I wrote the BRD, FRD, 10 BDD user stories and REST API sequence flows, and traced 8 business requirements to 15 sample test cases (not executed).</p>
<div class="disclaimer"><b>Fictional sample.</b> No client data is used and no executed-test evidence is claimed.</div>
<div class="actions"><a class="btn btn-primary" href="samples/index.html">View case study artifacts &rarr;</a></div></div>
</div>
<div class="grid g3" style="margin-top:24px">
{pcard(PROJECTS[0], 0, 0.0)}
{pcard(PROJECTS[1], 1, 0.07)}
{pcard(PROJECTS[2], 2, 0.14)}
</div>
<div class="actions rv" style="margin-top:32px"><a class="btn btn-ghost" href="projects.html">View all 9 projects &rarr;</a></div>
</div></section>

<section class="sec band has-flow" id="toolkit">{F.pipeline("tk")}<div class="wrap">
{sh(4, "Skills", "Skills and delivery toolkit", "Processes, standards and tools used across past projects.")}
<div class="grid g2">{tk}</div>
</div></section>

<section class="sec has-flow" id="experience">{F.seq("e")}<div class="wrap">
{sh(5, "Experience", "Business analyst experience in fintech and BFSI")}
<div class="roles">
<div class="role {rv(0)}"><div class="node">01</div><div class="rbody"><h3>Business Analyst</h3><div class="org">Marolix Technology Solutions Pvt Ltd, Hyderabad &bull; 2023 &ndash; Present</div><ul><li>Delivered implementation-ready documentation for <strong>2 payment-gateway integrations</strong> by defining REST API requirements, UML flows and data mappings.</li><li>Identified 3 recurring SLA-breach patterns across <strong>100,000+ transaction records</strong> by analysing them with SQL and Python.</li><li>Supported zero reported critical defects across <strong>350+ test cases</strong> by coordinating UAT in Jira; managed 12+ change requests over 2 Agile releases.</li></ul></div></div>
<div class="role {rv(1)}"><div class="node">02</div><div class="rbody"><h3>Business Analyst</h3><div class="org">V Moksha Technologies Pvt Ltd, Bengaluru &bull; 2022 &ndash; 2023</div><ul><li>Resolved recurring operational bottlenecks and SLA shortfalls using SQL data extraction, fishbone diagrams, and 5-Why root cause analysis.</li><li>Mapped AS-IS and TO-BE business processes (BPMN / swimlane), saving an estimated <strong>2 weeks per improvement cycle</strong>.</li></ul></div></div>
<div class="role {rv(2)}"><div class="node">03</div><div class="rbody"><h3>Business Analyst</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru &bull; 2021 &ndash; 2022</div><ul><li>Facilitated Three Amigos sessions, delivering functional specifications and BDD user stories for 3 concurrent modules across 4 business units.</li><li>Coordinated UAT, smoke and regression testing across <strong>50+ Jira test cases</strong> with zero post-launch incidents.</li><li>Reviewed API contracts against business rules and maintained the RTM and RACI matrix.</li></ul></div></div>
<div class="role {rv(3)}"><div class="node">04</div><div class="rbody"><h3>Associate Software Engineer</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru &bull; 2020 &ndash; 2021</div><ul><li>Promoted to Business Analyst in <strong>17 months (6 months ahead of schedule)</strong> after managing requirements for 3 reporting features.</li><li>Translated reporting needs from 15+ Finance and Operations stakeholders into Power BI requirements and BDD user stories, and secured approval for a reporting-automation business case projecting 3+ hrs/week of savings.</li></ul></div></div>
</div>
<div class="actions"><a class="btn btn-ghost" href="resume.html">Full resume &amp; ATS PDF</a></div>
</div></section>
''' + cta()

# ---------------------------------------------------------------- about
def about():
    return head("About", "Fintech business analyst: requirements teams can build and validate.", "I connect stakeholder needs, requirements, data, systems and delivery teams, so ambiguous business problems become clear, testable work.", F.seq("a")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap two">
<div><h2 class="{rv(0)}">Who I am</h2>
<p class="{rv(1)}" style="margin-top:18px">I&rsquo;m Gautam Reddy, a Business Analyst with 4+ years of experience in requirements analysis and delivery, translating business needs into clear, testable functional and non-functional requirements.</p>
<div class="{rv(2)}">
<h3 style="font-size:1.1rem;margin:18px 0 8px">What I do:</h3>
<ul style="padding-left:1.2em;margin:0 0 20px;color:var(--muted);line-height:1.6">
<li><strong>Elicitation &amp; Scoping:</strong> Facilitating stakeholder workshops, discovery interviews, and backlog prioritization (MoSCoW).</li>
<li><strong>Technical Specifications:</strong> Authoring BRD, FRD, REST API integration contracts, and BDD Given/When/Then user stories.</li>
<li><strong>Data &amp; Process Analysis:</strong> SQL querying, data mapping, and AS-IS / TO-BE process modelling with BPMN and UML.</li>
<li><strong>Testing &amp; UAT:</strong> Requirements Traceability Matrix (RTM), test-case coordination, and defect triage with Engineering.</li>
</ul>
</div>
<div class="actions {rv(4)}"><a class="btn btn-primary" href="resume.html">View resume &amp; PDF</a><a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">Connect on LinkedIn</a></div></div>
<div class="{rv(2)}" style="align-self:start"><dl class="facts card"><dt>Role</dt><dd>Business Analyst, 4+ years</dd><dt>Focus</dt><dd>Requirements Gathering, API &amp; System Integration, SQL, Agile, UAT</dd><dt>Technical Tools</dt><dd>SQL, Python (Pandas), Excel, Power BI, JIRA, Confluence, Figma, Postman</dd><dt>Based in</dt><dd>Bengaluru, India (IST / UTC+5:30)</dd><dt>Profiles</dt><dd>{ext(GH, "GitHub")}, {ext(LI, "LinkedIn")}, {ext(HR, "HackerRank")}</dd></dl></div>
</div></section>

<section class="sec band has-flow">{F.pipeline("ab")}<div class="wrap">
{sh(1, "Principles", "Working principles", "The habits behind the documents.")}
<div class="grid g3">
<div class="card {rv(0)}"><h3>Evidence before opinion</h3><p>Findings, assumptions and limitations are kept separate, so guesses are never presented as facts.</p></div>
<div class="card {rv(1)}"><h3>Scope you can point at</h3><p>Agreed deliverables and acceptance criteria define what &ldquo;done&rdquo; means before work begins.</p></div>
<div class="card {rv(2)}"><h3>Traceable by design</h3><p>Requirements connect to stories, tests and decisions, so any change shows its impact.</p></div>
</div></div></section>

<section class="sec has-flow">{F.swim("ab2")}<div class="wrap">
{sh(2, "Career path", "Career path &amp; promotions")}
<div class="roles">
<div class="role {rv(0)}"><div class="node">01</div><div class="rbody"><h3>Business Analyst</h3><div class="org">Marolix Technology Solutions Pvt Ltd, Hyderabad &bull; 2023 &ndash; Present</div><p class="muted">REST API requirements, UML flows and data mappings for 2 payment-gateway integrations; 100,000+ transaction records analysed using SQL and Python; 20+ workshops with 13+ stakeholders; 350+ test cases coordinated in Jira with zero critical defects.</p></div></div>
<div class="role {rv(1)}"><div class="node">02</div><div class="rbody"><h3>Business Analyst</h3><div class="org">V Moksha Technologies Pvt Ltd, Bengaluru &bull; 2022 &ndash; 2023</div><p class="muted">Fishbone and 5-Why root cause analysis with SQL data extraction; AS-IS / TO-BE process mapping eliminating redundant handover steps and saving an estimated 2 weeks per improvement cycle.</p></div></div>
<div class="role {rv(2)}"><div class="node">03</div><div class="rbody"><h3>Business Analyst</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru &bull; 2021 &ndash; 2022</div><p class="muted">Three Amigos facilitation, functional specs and BDD acceptance criteria for 3 modules across 4 business units; API contract review, RTM, and UAT across 50+ test cases with zero post-launch incidents.</p></div></div>
<div class="role {rv(3)}"><div class="node">04</div><div class="rbody"><h3>Associate Software Engineer &rarr; Promoted to BA</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru &bull; 2020 &ndash; 2021</div><p class="muted"><strong>Promoted to Business Analyst in 17 months (6 months ahead of schedule)</strong> after managing requirements for 3 reporting features; translated reporting needs from 15+ Finance and Operations stakeholders into Power BI requirements and BDD user stories, and secured approval for a reporting-automation business case projecting 3+ hrs/week of savings.</p></div></div>
</div></div></section>

''' + cta()

# ---------------------------------------------------------------- services
SERV = [("Business analysis and requirements", "Turn fragmented requests into an agreed problem statement, requirements and an actionable backlog.", ["BRD / FRD", "User stories", "Acceptance criteria", "Process maps", "Traceability"]),
("Data analysis and BI reporting", "Translate operational or sales data into useful answers, clear KPIs and reporting views that support decisions.", ["SQL analysis", "Power BI requirements", "DAX measures", "KPI definitions", "Insight summary"]),
("SQL, data quality and reporting", "Investigate mismatches, recurring reporting issues and data-quality risks with repeatable checks and documented findings.", ["Validation queries", "Root cause analysis", "Quality rules", "Exception log", "Recommendations"]),
("API and integration analysis", "Make integration expectations explicit for business, engineering and QA teams before implementation and testing.", ["REST API requirements", "Field mapping", "Sequence flows", "Error scenarios", "Dependency notes"]),
("UAT, testing and release support", "Help teams check that a solution meets the agreed requirement and make defects, risks and decisions visible.", ["Test scenarios", "UAT cases", "RTM", "Defect triage", "Release checklist"])]

FAQ = [("How do fees and timelines work?", "They depend on complexity, the output required, dependencies and review cycles. We can agree a discovery phase or a defined deliverable after clarifying the scope. No fixed price is quoted on this site."),
("Can I start with a small task?", "Yes. A requirements review, data-quality check, process walkthrough or feasibility prototype can be a focused first phase when the goals and output are clear."),
("Can you work with my existing team?", "The services include collaboration with stakeholders, Product, Engineering and QA teams. Working cadence and tool access should be agreed before delivery begins."),
("Can you work with confidential data?", "We can discuss an NDA and appropriate handling before sharing project materials. Do not send credentials, regulated records or confidential customer data in the initial enquiry form.")]

def services():
    cards = "".join(f'<div class="card {rv(i % 3, 0.0)}"><h3>{t}</h3><p>{d}</p>{tags(tg)}<div class="actions" style="margin-top:auto"><a class="btn btn-ghost" href="contact.html?service={html.escape(t)}">Enquire about this</a></div></div>' for i, (t, d, tg) in enumerate(SERV))
    faq = "".join(f'<details class="faq-item {rv(i, 0.0)}"><summary><span>{q}</span><svg class="chevron" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></summary><div class="faq-ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    return head("Services", "Business analysis services with clear scope and useful deliverables.", "Business analysis, data and technology support shaped around the problem, the people who need the answer and the output your team can use.", F.swim("sv")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap">
{sh(1, "Services", "Business analysis services I offer")}
<div class="grid g3">{cards}</div>
</div></section>

<section class="sec band has-flow">{F.erd("sv2")}<div class="wrap">
{sh(2, "Process", "How an engagement runs", "Clear milestones and check-ins.")}
<ol class="steps">{make_steps(SERVICE_STEPS)}</ol>
</div></section>

<section class="sec has-flow">{F.pipeline("sv3")}<div class="wrap">
{sh(3, "Evidence", "What you receive", "Tangible, reviewable artifacts corresponding directly to our sample deliverables.")}
<div class="grid g3">
<div class="card {rv(0)}"><h3>Requirements packs</h3><p>BRDs, FRDs, data dictionaries and Given/When/Then user stories ready for engineering estimation.</p><a class="more" href="samples/index.html#brd">View BRD &amp; FRD sample &rarr;</a></div>
<div class="card {rv(1)}"><h3>Process &amp; API models</h3><p>BPMN workflows, swimlanes, ERDs and REST API sequence flows that bridge business rules and system design.</p><a class="more" href="samples/index.html#process-flow">View process diagrams &rarr;</a></div>
<div class="card {rv(2)}"><h3>Traceability &amp; UAT plans</h3><p>Requirements Traceability Matrix (RTM) linking requirements to test cases with acceptance criteria and sign-off tracking.</p><a class="more" href="samples/index.html#uat">View UAT &amp; RTM sample &rarr;</a></div>
</div></div></section>

<section class="sec"><div class="wrap">
{sh(4, "FAQ", "Questions before starting")}
<div class="faq" style="max-width:820px;margin-top:28px">{faq}</div>
</div></section>
''' + cta(h="Not sure which service fits?", t="Describe the problem and the outcome you want. We can clarify the scope before deciding on next steps.")

# ---------------------------------------------------------------- projects
def projects():
    chips = '<button class="chip" type="button" data-f="all" aria-pressed="true">All</button>' + "".join(f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{n}</button>' for k, n in [("analytics", "Analytics"), ("bi", "Business intelligence"), ("data", "Data engineering"), ("ai", "AI prototype"), ("writing", "Writing")])
    cards = "".join(pcard(c, i % 3, 0.0) for i, c in enumerate(PROJECTS))
    return head("Projects", "Business analyst projects: practical analysis, visible work.", "Repositories across analytics, business intelligence, data engineering, AI prototypes and writing. Every card links to its source so you can review the implementation.", F.erd("pj")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap">
<h2 class="sr-only">Featured case study</h2>
<div class="feature rv" data-tilt>
<div><span class="cat feat-badge">Featured case study</span><h3>PayTrack: payment reconciliation, from BRD to UAT</h3><p class="muted"><strong>Problem &bull; Role &bull; Result:</strong> Operations teams struggle to investigate unmatched gateway and internal payment records. As the Business Analyst I wrote the BRD, FRD, 10 Given/When/Then user stories and REST API sequence flows, and traced all 8 business requirements to 15 sample test cases (not executed).</p>
<div class="disclaimer"><b>Fictional sample.</b> No client data is used and no executed-test evidence is claimed.</div>
<div class="actions"><a class="btn btn-primary" href="samples/index.html">Open all artifacts</a></div></div>
<div class="feat-side"><a class="feat-img" href="samples/diagrams/Payment_Data_Model_ERD.svg" aria-label="Open the data model diagram"><img src="samples/diagrams/Payment_Data_Model_ERD.png" alt="Logical data model (ERD) from the PayTrack sample" width="1120" height="704" loading="lazy"></a>
<ul><li><a href="samples/docs/01_BRD_PayTrack_Sample.pdf">Business requirements and functional spec <span>PDF</span></a></li><li><a href="samples/docs/03_User_Stories_Acceptance_Criteria_Sample.pdf">Stories with Given/When/Then criteria <span>PDF</span></a></li><li><a href="samples/docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf">RTM, test cases and UAT plan <span>PDF</span></a></li></ul></div>
</div>
<h2 class="rv" style="margin:56px 0 20px">Project portfolio</h2>
<div class="filters rv" role="group" aria-label="Filter projects">{chips}</div>
<p class="muted small" id="count" aria-live="polite">9 projects</p>
<div class="grid g3" id="pgrid">{cards}</div>
<div class="disclaimer rv"><b>Portfolio transparency.</b> These are personal portfolio repositories and prototypes, not paid client engagements. Each repository&rsquo;s README has the exact features, requirements and setup.</div>
</div></section>
''' + cta(h="Need a similar output?", t="Tell me the question, process or workflow that needs attention and the report, requirements pack or analysis you need.")

# ---------------------------------------------------------------- resume
def resume():
    def role(n, t, o, b, i): return f'<div class="role {rv(i)}"><div class="node">{n:02d}</div><div class="rbody"><h3>{t}</h3><div class="org">{o}</div><ul>' + "".join(f"<li>{x}</li>" for x in b) + '</ul></div></div>'
    roles = role(1, "Business Analyst", "Marolix Technology Solutions Pvt Ltd &bull; Hyderabad, India &bull; 2023 &ndash; Present", [
"Delivered implementation-ready documentation for <strong>2 payment gateway integrations</strong> by defining REST API requirements, UML system flows and data mappings for Engineering and QA.",
"Identified <strong>3 recurring SLA breach patterns</strong> across <strong>100,000+ transaction records</strong> by analysing them with SQL and Python, and shared the findings to inform process-improvement actions.",
"Aligned <strong>13+ stakeholders</strong> on business and functional requirements through <strong>20+ workshops</strong>, documenting BRDs/FRDs, functional and non-functional requirements, use cases and BDD acceptance criteria.",
"Kept backlog decisions focused on business value across 4 modules by prioritizing requirements with MoSCoW and challenging 3 feature requests that lacked business justification.",
"Supported <strong>zero reported critical defects</strong> across <strong>350+ test cases</strong> by coordinating UAT and functional, regression and integration testing and supporting JIRA defect triage with QA and Engineering.",
"Managed <strong>12+ change requests</strong> across 2 Agile releases by assessing requirement impacts and maintaining traceability through delivery.",
"Maintained business rules, data dictionaries, and field mappings in Confluence and Excel; reviewed Figma wireframes and prepared stakeholder reports."], 0)
    roles += role(2, "Business Analyst", "V Moksha Technologies Pvt Ltd &bull; Bengaluru, India &bull; 2022 &ndash; 2023", [
"Saved an estimated <strong>2 weeks per improvement cycle</strong> by resolving recurring SLA shortfalls and reducing error recurrence and rework through SQL analysis, fishbone/5-Why root-cause analysis and AS-IS/TO-BE process mapping."], 0)
    roles += role(3, "Business Analyst", "Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India &bull; 2021 &ndash; 2022", [
"Delivered <strong>3 concurrent modules</strong> on time by facilitating Three Amigos sessions and translating stakeholder needs into functional requirements and BDD acceptance criteria.",
"Documented functional requirements, business rules, and control requirements across 4 business units.",
"Delivered modules with no reported post-launch incidents by coordinating UAT, smoke, sanity and regression testing across <strong>50+ JIRA-tracked test cases</strong>.",
"Reviewed API contracts against functional requirements and maintained the Requirements Traceability Matrix (RTM) and RACI to connect requirements, delivery, and acceptance."], 0)
    roles += role(4, "Associate Software Engineer &rarr; Promoted to BA", "Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India &bull; 2020 &ndash; 2021", [
"Earned promotion to Business Analyst within <strong>17 months (6 months ahead of schedule)</strong> by managing requirements for 3 reporting features from elicitation through stakeholder acceptance.",
"Translated input from 15+ Finance and Operations stakeholders into Power BI requirements and BDD user stories, coordinating with Engineering and business leads.",
"Secured executive approval for a reporting-automation business case projecting <strong>3+ hours of weekly manual-effort savings</strong>."], 0)
    return head("Resume", "Business Analyst resume: experience, skills, delivery.", "Business Analyst focused on requirements, API and system integration, SQL and Python analysis, Agile delivery and UAT coordination.", F.swim("rs")) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap">
<div class="actions rv" style="margin:0 0 40px"><button type="button" class="btn btn-primary" onclick="window.print()" title="Print ATS-friendly resume or save as PDF">Print / Save as PDF</button><a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">View LinkedIn profile</a><a class="btn btn-ghost" href="{HR}" target="_blank" rel="noopener noreferrer">HackerRank profile</a><a class="btn btn-ghost" href="contact.html">Contact me</a></div>
<div class="proof">
<div class="proof-card {rv(0)}"><b data-count="100" data-suf="K+">100K+</b><span class="source-tag">Marolix &bull; SQL analysis</span><span>transactions analysed</span></div>
<div class="proof-card {rv(1)}"><b data-count="350" data-suf="+">350+</b><span class="source-tag">QA &amp; UAT coordination</span><span>test cases coordinated</span></div>
<div class="proof-card {rv(2)}"><b data-count="20" data-suf="+">20+</b><span class="source-tag">13+ stakeholders</span><span>workshops facilitated</span></div>
<div class="proof-card {rv(3)}"><b data-count="12" data-suf="+">12+</b><span class="source-tag">2 Agile releases</span><span>change requests managed</span></div>
</div>
<p class="note">Metrics come from my resume and refer to past roles and projects.</p>
</div></section>

<section class="sec band has-flow">{F.seq("rs2")}<div class="wrap">
{sh(1, "Experience", "Professional experience")}
<div class="roles">{roles}</div></div></section>

<section class="sec"><div class="wrap two">
<div><h2 class="rv">Skills</h2>
<dl class="facts rv" style="margin-top:24px"><dt>Business Analysis</dt><dd>Requirements Gathering &amp; Elicitation, Requirements Analysis, Validation &amp; Sign-off, Stakeholder Management, BRD/FRD, Functional &amp; Non-Functional Requirements, User Stories &amp; Use Cases, BDD Acceptance Criteria, Requirements Traceability Matrix (RTM), Impact Analysis.</dd>
<dt>Process Analysis &amp; Documentation</dt><dd>AS-IS/TO-BE Analysis, Gap Analysis, Process Mapping (BPMN/UML), Business Rules, Root Cause Analysis, MoSCoW Prioritization, Data Mapping, System Workflow Documentation.</dd>
<dt>Agile, Testing &amp; Delivery</dt><dd>SDLC, Agile/Scrum, Sprint Planning, Backlog Refinement, Change Management, UAT Coordination, Functional, Regression &amp; Integration Testing, Defect Triage.</dd>
<dt>Technical Skills &amp; Tools</dt><dd>REST API Requirements, API Contract Review, System Integration Requirements, SQL, Python (Pandas), Excel, Power BI, JIRA, Confluence, Figma, Postman.</dd></dl>
<div class="rv" style="margin-top:24px">{tags(["REST API Requirements", "API Contract Review", "System Integration Requirements", "SQL", "Python (Pandas)", "Excel", "Power BI", "JIRA", "Confluence", "Figma", "Postman"])}</div></div>
<div><h2 class="rv">Education and certifications</h2>
<dl class="facts rv" style="margin-top:24px"><dt>Education</dt><dd>B.Tech, Mechanical Engineering, minor in Computer Science. Biju Patnaik University of Technology, Odisha, 2016 to 2020.</dd>
<dt>Certification</dt><dd>Google Data Analytics Professional Certificate, Coursera, 2023.</dd>
<dt>In progress</dt><dd>CBAP (IIBA)</dd></dl></div>
</div></section>
''' + cta(h="Need a BA who connects requirements, data and delivery?", t="Tell me about the role or scope and the outcome your team is aiming for.")

# ---------------------------------------------------------------- contact
def contact():
    opts = lambda l: "".join(f"<option>{o}</option>" for o in l)
    return head("Contact", "Contact a Business Analyst: tell me what you&rsquo;re trying to solve.", "For a role, mention the position and team. For a collaboration, describe the problem and the outcome. I reply with context.", F.seq("ct")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap two" style="align-items:start">
<div class="rv"><h2>Reach me directly</h2>
<ul class="contact-list" style="margin-top:24px"><li><span>{ICO_MAIL}Email</span><div><a href="mailto:{EMAIL}">{EMAIL}</a> <button class="chip copy" type="button" data-copy="{EMAIL}">Copy</button></div></li><li><span>{ICO_LI}LinkedIn</span><div>{ext(LI, "gautam-reddy-analyst")}</div></li><li><span>{ICO_GH}GitHub</span><div>{ext(GH, "reddygautam98")}</div></li><li><span>{ICO_HR}HackerRank</span><div>{ext(HR, "reddygautam98")}</div></li><li><span>{ICO_LOC}Location</span><div>Bengaluru, India (IST / UTC+5:30)</div></li></ul>
<h3 style="margin:32px 0 10px">Useful details to include</h3>
<ul class="muted" style="padding-left:1.1em;margin:0"><li>The problem and who it affects</li><li>The output you need and how it will be used</li><li>Relevant tools, systems, data types and deadlines</li><li>Any constraints or acceptance criteria</li></ul>
<p class="disclaimer"><b>Please don&rsquo;t include</b> passwords, confidential source files, regulated records or sensitive customer data in a first message.</p></div>
<div class="form-card rv" style="--d:.1s"><h2 style="font-size:1.6rem">Project enquiry</h2>
<p class="muted small" style="margin:8px 0 16px">This site stores nothing. The button opens a draft in your email app and nothing is sent until you press Send.</p>
<p class="small" style="margin:0 0 16px;color:var(--muted)">* Required fields</p>
<form id="enquiry" novalidate>
<div class="row2">
  <label for="enquiry-name">Your name *<input id="enquiry-name" name="name" autocomplete="name" required aria-describedby="err-name"><span class="err" id="err-name" aria-live="polite"></span></label>
  <label for="enquiry-email">Work email *<input id="enquiry-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="err-email"><span class="err" id="err-email" aria-live="polite"></span></label>
</div>
<label for="enquiry-company">Company (optional)<input id="enquiry-company" name="company" autocomplete="organization"></label>
<label for="enquiry-service">What do you need help with? *<select id="enquiry-service" name="service" required aria-describedby="err-service"><option value="">Choose a service</option>{opts(["Business analysis and requirements", "Data analysis and BI reporting", "SQL, data quality and reporting", "API and integration analysis", "UAT, testing and release support", "A role at my company", "Not sure yet"])}</select><span class="err" id="err-service" aria-live="polite"></span></label>
<div class="row2">
  <label for="enquiry-type">Engagement type<select id="enquiry-type" name="type">{opts(["Full-time role", "Discovery or review", "Defined deliverable", "Ongoing support", "Prototype or feasibility", "Not sure yet"])}</select></label>
  <label for="enquiry-timeline">Target timeline<select id="enquiry-timeline" name="timeline">{opts(["Flexible", "As soon as practical", "Within 2 to 4 weeks", "Within 1 to 3 months", "Specific deadline"])}</select></label>
</div>
<label for="enquiry-msg">Describe the problem and the outcome you want *<textarea id="enquiry-msg" name="msg" required aria-describedby="err-msg"></textarea><span class="err" id="err-msg" aria-live="polite"></span></label>
<label for="enquiry-ref">Reference link (optional)<input id="enquiry-ref" name="ref" type="url" placeholder="https://example.com" aria-describedby="err-ref"><span class="err" id="err-ref" aria-live="polite"></span></label>
<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn btn-primary" type="submit">Prepare email draft</button><span class="muted small">Or email directly: <a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
<p id="sent" class="muted small" hidden role="status">Preparing your email draft. If your email application does not open automatically, please send your enquiry directly to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</form></div>
</div></section>
'''

# ---------------------------------------------------------------- sample item icons
ICO_SEC_DOCS = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>'
ICO_SEC_DIAG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><path d="M10 6.5h4M17.5 10v4"/></svg>'
ICO_SEC_DATA = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'

ICO_DOC_BRD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>'
ICO_DOC_FRD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="m10 13-2 2 2 2"/><path d="m14 17 2-2-2-2"/></svg>'
ICO_DOC_STORIES = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>'
ICO_DOC_RTM = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>'
ICO_DOC_DISCOVERY = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICO_DOC_BUNDLE = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'

ICO_DIAG_PROCESS = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/><polyline points="12 12 15 15 12 18"/></svg>'
ICO_DIAG_ARCH = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/><line x1="12" y1="10" x2="12" y2="14"/></svg>'
ICO_DIAG_ERD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
ICO_DIAG_API = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="2" y1="12" x2="22" y2="12"/></svg>'
ICO_DIAG_BI = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>'
ICO_DIAG_FIGMA = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"/><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"/><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"/><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"/></svg>'
ICO_DIAG_FIGJAM = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 14.14 14.14M12 2a10 10 0 0 1 10 10"/></svg>'

ICO_DATA_RTM = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>'
ICO_DATA_TESTS = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>'
ICO_DATA_STORIES = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>'
ICO_DATA_SQL = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'

def flink(href, text, ico_type="", download=False, target_blank=True):
    dl = " download" if download else ""
    tgt = ' target="_blank" rel="noopener noreferrer"' if target_blank else ""
    ico_svg = ""
    cls_extra = ""
    if ico_type == "pdf":
        cls_extra = " link-btn-pdf"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 13v4M9 15h2a1 1 0 0 0 0-2H9"/></svg>'
    elif ico_type == "word":
        cls_extra = " link-btn-word"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="m8 13 1.5 5 1.5-5 1.5 5 1.5-5"/></svg>'
    elif ico_type == "csv":
        cls_extra = " link-btn-csv"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>'
    elif ico_type == "sql":
        cls_extra = " link-btn-sql"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
    elif ico_type == "img":
        cls_extra = " link-btn-img"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'
    elif ico_type == "mmd":
        cls_extra = " link-btn-mmd"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/></svg>'
    elif ico_type == "figma":
        cls_extra = " link-btn-figma"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/></svg>'
    elif ico_type == "figjam":
        cls_extra = " link-btn-figjam"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/></svg>'
    elif ico_type == "gh":
        cls_extra = " link-btn-gh"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
    elif ico_type == "bi":
        cls_extra = " link-btn-bi"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>'
    return f'<a href="{href}"{tgt}{dl} class="file-link-btn{cls_extra}">{ico_svg}<span>{text}</span></a>'

# ---------------------------------------------------------------- samples
def sitem(t, d, links, item_id="", ico=""):
    id_attr = f' id="{item_id}"' if item_id else ''
    ico_box = f'<div class="file-item-ico" aria-hidden="true">{ico}</div>' if ico else ''
    return f'''<li class="rv"{id_attr}>
  <div class="file-item-main">
    {ico_box}
    <div class="file-item-body">
      <h3>{t}</h3>
      <p>{d}</p>
    </div>
  </div>
  <div class="links">{"".join(links)}</div>
</li>'''

def samples():
    docs = "".join([
     sitem("Complete Documentation Bundle (Featured)", "All five primary business analysis specifications consolidated in one comprehensive PDF download.", [flink("docs/PayTrack_Sample_BA_Documentation_Bundle.pdf", "PDF Bundle (1.2MB)", "pdf")], "bundle", ICO_DOC_BUNDLE),
     sitem("Discovery Workshop MoM & Decision Log", "Phase 1 &bull; Workshop summary, discussion themes, open decisions, action tracker and RAID log.", [flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf", "PDF", "pdf"), flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.docx", "Word", "word", target_blank=False)], "discovery", ICO_DOC_DISCOVERY),
     sitem("Business Requirements Document (BRD)", "Phase 2 &bull; Business need, objectives, scope, stakeholders, assumptions, requirements and sign-off template.", [flink("docs/01_BRD_PayTrack_Sample.pdf", "PDF", "pdf"), flink("docs/01_BRD_PayTrack_Sample.docx", "Word", "word", target_blank=False)], "brd", ICO_DOC_BRD),
     sitem("Functional Requirements Document (FRD)", "Phase 2 &bull; Functional behaviour, business rules, data entities, screen requirements, NFRs, error states and decisions to confirm.", [flink("docs/02_FRD_PayTrack_Sample.pdf", "PDF", "pdf"), flink("docs/02_FRD_PayTrack_Sample.docx", "Word", "word", target_blank=False)], "frd", ICO_DOC_FRD),
     sitem("User Stories and Acceptance Criteria", "Phase 3 &bull; Prioritised stories with testable Given / When / Then criteria across operational personas.", [flink("docs/03_User_Stories_Acceptance_Criteria_Sample.pdf", "PDF", "pdf"), flink("docs/03_User_Stories_Acceptance_Criteria_Sample.docx", "Word", "word", target_blank=False)], "user-stories", ICO_DOC_STORIES),
     sitem("RTM, Test Cases and UAT Plan", "Phase 4 &bull; Traceability from requirement to test, test-case catalogue, UAT entry and exit criteria, sign-off record.", [flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf", "PDF", "pdf"), flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.docx", "Word", "word", target_blank=False)], "uat", ICO_DOC_RTM)])
    dg = "".join([
     sitem("Payment reconciliation process flow", "Matched path, validation failure, exception creation, review, resolution or escalation, and audit.", [flink("diagrams/Payment_Reconciliation_Process.svg", "SVG", "img"), flink("diagrams/Payment_Reconciliation_Process.png", "PNG", "img"), flink("diagrams/Payment_Reconciliation_Process.mmd", "Mermaid", "mmd", target_blank=False)], "process-flow", ICO_DIAG_PROCESS),
     sitem("Conceptual solution architecture", "Portal, API, reconciliation service, data store, gateway adapter, audit and access control.", [flink("diagrams/Payment_Conceptual_Architecture.svg", "SVG", "img"), flink("diagrams/Payment_Conceptual_Architecture.png", "PNG", "img")], "architecture", ICO_DIAG_ARCH),
     sitem("Logical data model (ERD)", "Candidate entities and relationships for transactions, gateway events, reconciliation results, exceptions and audit events.", [flink("diagrams/Payment_Data_Model_ERD.svg", "SVG", "img"), flink("diagrams/Payment_Data_Model_ERD.png", "PNG", "img"), flink("diagrams/Payment_Data_Model_ERD.mmd", "Mermaid", "mmd", target_blank=False)], "erd", ICO_DIAG_ERD),
     sitem("API sequence diagram", "Message flow for payment submission, gateway event, reconciliation and status query.", [flink("diagrams/Payment_API_Sequence.svg", "SVG", "img"), flink("diagrams/Payment_API_Sequence.mmd", "Mermaid", "mmd", target_blank=False)], "rest-api", ICO_DIAG_API),
     sitem("Power BI reconciliation & operations dashboard", "Operational KPI tracking, reconciliation exception metrics, DAX measures and executive dashboard views.", [flink("../projects.html#bi", "Power BI Projects &#8599;", "bi", target_blank=False), flink("https://github.com/reddygautam98/Hr-data-analysis", "GitHub &#8599;", "gh")], "power-bi", ICO_DIAG_BI),
     sitem("Figma UI wireframes", "Editable overview dashboard and exception case-detail screens. Values are illustrative.", [flink("https://www.figma.com/design/qt1PFmcQNvtaJnLnrWxPKD", "Figma &#8599;", "figma")], "figma", ICO_DIAG_FIGMA),
     sitem("FigJam BA diagrams", "Editable process, API sequence and ERD diagrams on one board.", [flink("https://www.figma.com/board/N90uAbHaqe4OkCOUkNfNxX", "FigJam &#8599;", "figjam")], "figjam", ICO_DIAG_FIGJAM)])
    sp = "".join([
     sitem("Requirements traceability matrix", "Maps business requirements to functional requirements, stories and test cases.", [flink("specs/requirements_traceability.csv", "CSV", "csv", download=True, target_blank=False)], "rtm", ICO_DATA_RTM),
     sitem("Sample test cases", "Scenarios, preconditions, steps, expected results, traceability and Not Run status.", [flink("specs/sample_test_cases.csv", "CSV", "csv", download=True, target_blank=False)], "test-cases", ICO_DATA_TESTS),
     sitem("Sample user stories", "Backlog starter with priority, acceptance criteria and traceability.", [flink("specs/sample_user_stories.csv", "CSV", "csv", download=True, target_blank=False)], "user-stories-csv", ICO_DATA_STORIES),
     sitem("SQL reconciliation and data validation queries", "Analytical SQL queries to detect amount mismatches, orphan gateway events and 48-hour SLA breach exceptions.", [flink("specs/sample_reconciliation_queries.sql", "SQL", "sql", download=True, target_blank=False), flink("../projects.html#analytics", "SQL Projects &#8599;", "sql", target_blank=False)], "sql", ICO_DATA_SQL)])
    return head("BA samples", "Business analyst sample documents: clear thinking, visible evidence.", "One connected, fictional case study that shows how a business problem becomes requirements, prioritised stories, test coverage, process models and reviewable wireframes.", F.lifecycle("sm"), "../") + f'''
<section class="sec" style="padding-top:8px"><div class="wrap">
<div class="disclaimer rv" style="margin:0 0 48px"><b>Sample only, fictional case study.</b> PayTrack is an invented payment reconciliation and exception-management portal. Names, IDs, amounts, targets and scenarios are illustrative. Test cases have not been executed and no client outcome is claimed.</div>
<h2 class="rv sec-title-with-ico sec-title-docs" style="margin-bottom:20px"><span class="sec-hdr-ico sec-hdr-docs">{ICO_SEC_DOCS}</span><span class="sec-title-text">Documents</span></h2><ul class="file-list">{docs}</ul>
<h2 class="rv sec-title-with-ico sec-title-diag" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-diag">{ICO_SEC_DIAG}</span><span class="sec-title-text">Diagrams and design</span></h2><ul class="file-list">{dg}</ul>
<h2 class="rv sec-title-with-ico sec-title-data" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-data">{ICO_SEC_DATA}</span><span class="sec-title-text">Structured data</span></h2><ul class="file-list">{sp}</ul>
<p class="note rv" style="margin-top:32px">Scenario: PayTrack compares internal payment records with gateway events, helps operations staff investigate unmatched transactions, assigns ownership of exceptions and keeps an audit trail. Everything here needs stakeholder validation before any real implementation.</p>
</div></section>
''' + cta("../")

DESC = "Business Analyst in Bengaluru with 4+ years in fintech and BFSI: BRD/FRD, user stories, REST API requirements, SQL, Power BI and UAT. Open to remote and hybrid roles."
PERSON_ID = SITE + "#person"
PERSON = {"@type": "Person", "@id": PERSON_ID, "name": "Gautam Reddy", "jobTitle": "Business Analyst",
    "description": DESC, "url": SITE, "sameAs": [LI, GH, HR],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Biju Patnaik University of Technology"},
    "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "Google Data Analytics Professional Certificate", "credentialCategory": "certificate"},
    "knowsAbout": ["Business analysis", "Requirements gathering", "Stakeholder management", "BRD and FRD", "User stories", "Acceptance criteria", "UAT", "SQL", "Python", "Power BI", "Agile", "Scrum",
                   "REST API requirements", "Postman", "Payment gateway integrations", "Transaction processing", "Settlement and reconciliation", "SLA monitoring", "Finance and operations reporting", "Fintech", "BFSI"]}

def ldscript(*objs):
    return "".join('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", **o}, ensure_ascii=False) + '</script>\n' for o in objs)

def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

WEBSITE = {"@type": "WebSite", "@id": SITE + "#website", "name": "Gautam Reddy - Business Analyst Portfolio", "url": SITE, "inLanguage": "en-IN", "publisher": {"@id": PERSON_ID}}
LD_HOME = ldscript(WEBSITE, PERSON)
LD_ABOUT = ldscript({"@type": "ProfilePage", "url": SITE + "about.html", "name": "About Gautam Reddy", "mainEntity": {"@id": PERSON_ID}}, PERSON, crumbs("About", "about.html"))
LD_SERVICES = ldscript({"@type": "ProfessionalService", "name": "Gautam Reddy - Business Analysis Services", "url": SITE + "services.html", "provider": {"@id": PERSON_ID},
    "areaServed": "Worldwide (remote) and Bengaluru, India", "serviceType": [t for t, _, _ in SERV]}, crumbs("Services", "services.html"))
LD_PROJECTS = ldscript({"@type": "CollectionPage", "url": SITE + "projects.html", "name": "Business analyst projects", "mainEntity": {"@type": "ItemList", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "name": c[2], "url": c[5]} for i, c in enumerate(PROJECTS)]}}, crumbs("Projects", "projects.html"))
LD_RESUME = ldscript({"@type": "ProfilePage", "url": SITE + "resume.html", "name": "Gautam Reddy resume", "mainEntity": {"@id": PERSON_ID}}, crumbs("Resume", "resume.html"))
LD_CONTACT = ldscript({"@type": "ContactPage", "url": SITE + "contact.html", "name": "Contact Gautam Reddy", "mainEntity": {"@id": PERSON_ID}}, crumbs("Contact", "contact.html"))
LD_SAMPLES = ldscript({"@type": "CollectionPage", "url": SITE + "samples/index.html", "name": "PayTrack BA sample documents (fictional)", "author": {"@id": PERSON_ID}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "BA samples", "item": SITE + "samples/index.html"}]})

pages = [
("index.html", "Gautam Reddy | Business Analyst in Bengaluru | Fintech & BFSI", DESC, index(), "", "", LD_HOME),
("about.html", "About Gautam Reddy | Fintech & BFSI Business Analyst", "About Gautam Reddy, a Bengaluru Business Analyst with 4+ years in fintech and BFSI: his career path from engineer to BA and the principles behind his work.", about(), "", "about.html", LD_ABOUT),
("services.html", "Business Analyst Services: BRD, FRD, SQL, UAT | Gautam Reddy", "Business analysis services for fintech teams: BRD/FRD requirements packs, SQL and BI reporting, REST API analysis and UAT support, with clear deliverables.", services(), "", "services.html", LD_SERVICES),
("projects.html", "Business Analyst Projects: SQL, Power BI, PayTrack | Gautam Reddy", "Nine portfolio projects by Business Analyst Gautam Reddy: SQL and Power BI analytics, a data pipeline, a RAG prototype and the PayTrack case study.", projects(), "", "projects.html", LD_PROJECTS),
("resume.html", "Resume | Gautam Reddy, Business Analyst (Fintech & BFSI)", "Resume of Gautam Reddy, Business Analyst with 4+ years in fintech and BFSI: 2 payment gateway integrations, 100,000+ transactions analysed, 350+ test cases.", resume(), "", "resume.html", LD_RESUME),
("contact.html", "Contact Gautam Reddy | Hire a Business Analyst, Bengaluru", "Contact Gautam Reddy, a Business Analyst in Bengaluru, about a full-time, hybrid or remote role, or a requirements, reconciliation or reporting project.", contact(), "", "contact.html", LD_CONTACT),
("samples/index.html", "BA Sample Documents: BRD, FRD, User Stories, RTM | Gautam Reddy", "Fictional PayTrack business analysis case study: BRD, FRD, user stories, RTM, UAT plan, process and ERD diagrams, SQL queries and CSV templates.", samples(), "../", "samples/index.html", LD_SAMPLES),
]
for path, t, d, b, p, cur, ld in pages:
    open(path, "w", encoding="utf-8").write(page(path, t, d, b, p, cur, ld))

NOT_FOUND = '''<section class="sec" style="padding-top:40px"><div class="wrap" style="max-width:680px">
<h1>Page not found</h1>
<p class="lead" style="margin-top:16px">The page you were looking for doesn&rsquo;t exist, was renamed, or has moved.</p>
<div class="actions" style="margin-top:28px">
<a class="btn btn-primary" href="{s}">Go to homepage <span class="arr" aria-hidden="true">&rarr;</span></a>
<a class="btn btn-ghost" href="{s}projects.html">Browse projects</a>
<a class="btn btn-ghost" href="{s}samples/index.html">View BA samples</a>
</div>
<ul class="muted small" style="display:flex;gap:18px;list-style:none;padding:0;margin:32px 0 0;flex-wrap:wrap">
<li><a href="{s}services.html">Services</a></li>
<li><a href="{s}resume.html">Resume</a></li>
<li><a href="{s}contact.html">Contact</a></li>
</ul>
</div></section>'''.format(s=SITE)
open("404.html", "w", encoding="utf-8").write(page("404.html", "Page not found | Gautam Reddy, Business Analyst", "This page could not be found.", NOT_FOUND, SITE, "", "", "noindex, follow"))

import datetime
today = datetime.date.today().isoformat()
urls = [SITE if p_ == "index.html" else SITE + p_ for p_, *_ in pages]
open("sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
print("built", len(pages))
