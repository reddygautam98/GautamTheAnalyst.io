"""Regenerates all 7 HTML pages. Run:  python build.py
Edit copy / links here, then rebuild. Diagrams come from flows.py."""
import html, json, urllib.parse, os, itertools
from collections import Counter
import flows as F

SITE = "https://reddygautam98.github.io/GautamTheAnalyst.io/"
GH = "https://github.com/reddygautam98/"
LI = "https://www.linkedin.com/in/gautam-reddy-analyst"
HR = "https://www.hackerrank.com/profile/reddygautam98"
EMAIL = "gautamreddy098@gmail.com"
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap"
NAV = [("projects.html", "Projects"), ("samples/index.html", "BA samples"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Contact")]

# Core BA & technical skills for single-row marquee
MARQ_ITEMS = ["Requirements Gathering", "BRD / FRD / SRS", "User Stories & BDD", "Traceability Matrix (RTM)", "Process Modelling (BPMN / UML)", "Gap Analysis", "REST API Integration", "SQL (PostgreSQL)", "Python (Pandas)", "Power BI & Excel", "UAT & Defect Triage", "Agile / Scrum"]

def ext(u, t): return f'<a href="{u}" target="_blank" rel="noopener noreferrer">{t} <span class="sr-only">(opens in new tab)</span>&rarr;</a>'
def rv(i=0, base=0.0, step=0.07): return f'rv" style="--d:{base + i * step:.2f}s'

ICO_MAIL = '<svg class="ico-gmail" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="#4285F4" d="M3.2 5.5A2.5 2.5 0 0 0 .7 8v10.5A2.5 2.5 0 0 0 3.2 21H5V11.25L3.2 9.8z"/><path fill="#34A853" d="M20.8 5.5a2.5 2.5 0 0 1 2.5 2.5V18.5a2.5 2.5 0 0 1-2.5 2.5H19V11.25l1.8-1.45z"/><path fill="#FBBC05" d="M19 11.25L12 16.5 5 11.25V21h14z"/><path fill="#EA4335" d="M3.2 5.5c-.8 0-1.5.5-1.8 1.25L12 13.5l10.6-6.75c-.3-.75-1-1.25-1.8-1.25z"/></svg>'
ICO_LI = '<svg class="ico-li" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#ffffff" d="M19 19h-3.14v-4.9c0-1.17-.02-2.67-1.63-2.67-1.63 0-1.88 1.27-1.88 2.58V19H9.21V9h3.01v1.37h.04c.42-.79 1.44-1.63 2.96-1.63 3.17 0 3.75 2.09 3.75 4.8V19zM5.34 7.63a1.74 1.74 0 1 1 0-3.48 1.74 1.74 0 0 1 0 3.48zM6.91 19H3.77V9h3.14v10z"/></svg>'
ICO_GH = '<svg class="ico-gh" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
ICO_HR = '<svg class="ico-hr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#00EA64"/><path fill="#0b0f19" d="M9.95 8.002h1.805c.061 0 .111.05.111.111v7.767c0 .061-.05.111-.11.111H9.95c-.061 0-.111-.05-.111-.11v-2.87H7.894v2.87c0 .06-.05.11-.11.11H5.976a.11.11 0 01-.11-.11V8.112c0-.06.05-.11.11-.11h1.806c.061 0 .11.05.11.11v2.869H9.84v-2.87c0-.06.05-.11.11-.11zm2.999 0h5.778c.061 0 .111.05.111.11v7.767a.11.11 0 01-.11.112h-5.78a.11.11 0 01-.11-.11V8.111c0-.06.05-.11.11-.11z"/></svg>'
ICO_LOC = '<svg class="ico-loc" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
MENU_ICO = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'

def page(path, title, desc, body, p="", cur="", ld="", robots="index, follow, max-image-preview:large, max-snippet:-1"):
    url = SITE if path == "index.html" else SITE + path
    home = p if p else "./"
    if robots.startswith("noindex"):
        url_tags = ''
    else:
        url_tags = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n'
    res_cur = ' aria-current="page"' if cur == "resume.html" else ""
    nav = "".join('<a href="%s%s"%s>%s</a>' % (p, h, ' aria-current="page"' if h == cur else "", t) for h, t in NAV)

    drawer_markup = ""
    if path == "samples/index.html":
        drawer_markup = '''<aside id="previewDrawer" class="preview-drawer" role="dialog" aria-modal="true" aria-labelledby="pdTitle" hidden>
  <div class="pd-backdrop" id="pdBackdrop" aria-hidden="true"></div>
  <div class="pd-panel">
    <div class="pd-head">
      <div><span class="pd-badge">In-Page Preview</span><div class="pd-pane-h" id="pdTitle">Document Preview</div></div>
      <button class="icon-btn pd-close" id="pdClose" type="button" aria-label="Close document preview">&times;</button>
    </div>
    <div class="pd-tabs" role="tablist" aria-label="Sample document types" data-lenis-prevent>
      <button class="pd-tab is-active" role="tab" id="pdtab-brd" aria-selected="true" aria-controls="pd-brd" type="button" data-pdtab="brd">01 BRD</button>
      <button class="pd-tab" role="tab" id="pdtab-frd" aria-selected="false" aria-controls="pd-frd" tabindex="-1" type="button" data-pdtab="frd">02 FRD</button>
      <button class="pd-tab" role="tab" id="pdtab-stories" aria-selected="false" aria-controls="pd-stories" tabindex="-1" type="button" data-pdtab="stories">03 Stories</button>
      <button class="pd-tab" role="tab" id="pdtab-rtm" aria-selected="false" aria-controls="pd-rtm" tabindex="-1" type="button" data-pdtab="rtm">04 RTM</button>
      <button class="pd-tab" role="tab" id="pdtab-mom" aria-selected="false" aria-controls="pd-mom" tabindex="-1" type="button" data-pdtab="mom">05 MoM</button>
    </div>
    <div class="pd-body" id="pdBody" data-lenis-prevent>
      <div class="pd-pane is-active" id="pd-brd" role="tabpanel" tabindex="0" aria-labelledby="pdtab-brd">
        <div class="pd-pane-h">PayTrack Business Requirements Document (BRD)</div>
        <p class="muted">Document ID: BRD-2026-PT &bull; Status: Approved &bull; Author: Gautam Reddy</p>
        <div class="pd-sample-box">
          <div class="pd-pane-sub">1. Executive Summary &amp; Problem Statement</div>
          <p>Settlement operations manually reconcile over 100,000 monthly transaction events across 2 payment gateways (Stripe &amp; Razorpay). Discrepancies historically take up to 48 hours to discover in spreadsheets. PayTrack introduces real-time ingestion, automated daily batch matching, and a 4-hour exception triage SLA.</p>
          <div class="pd-pane-sub">2. Key Objectives</div>
          <ul>
            <li>Achieve 99.8% straight-through automated transaction matching.</li>
            <li>Flag unsettled transaction exceptions within 5 minutes of ingestion.</li>
            <li>Establish 100% audit traceability connecting payment authorizations to bank settlement feeds.</li>
          </ul>
        </div>
      </div>
      <div class="pd-pane" id="pd-frd" role="tabpanel" tabindex="0" aria-labelledby="pdtab-frd" hidden>
        <div class="pd-pane-h">PayTrack Functional Requirements Document (FRD)</div>
        <p class="muted">Document ID: FRD-2026-PT &bull; Status: In Review &bull; Author: Gautam Reddy</p>
        <div class="pd-sample-box">
          <div class="pd-pane-sub">1. Ingestion Pipeline &amp; Validation</div>
          <p>System validates inbound webhook events via HMAC-SHA256 signature verification. Invalid payloads return HTTP 401 with structured JSON error schemas.</p>
          <div class="pd-pane-sub">2. Business Rules &amp; Reconciliation Logic</div>
          <ul>
            <li><strong>Rule 101:</strong> If transaction amount matches within 0.00 currency units and gateway_ref matches, mark record as RECONCILED.</li>
            <li><strong>Rule 102:</strong> If gateway_ref matches but amount differs, tag as AMOUNT_MISMATCH and alert Tier-2 Operations within 5 minutes.</li>
          </ul>
        </div>
      </div>
      <div class="pd-pane" id="pd-stories" role="tabpanel" tabindex="0" aria-labelledby="pdtab-stories" hidden>
        <div class="pd-pane-h">PayTrack User Stories &amp; Acceptance Criteria (BDD)</div>
        <p class="muted">Sprint 24 Backlog &bull; Prioritized via MoSCoW &bull; Status: Sprint Ready</p>
        <div class="pd-sample-box">
          <div class="us-story-card">
            <div class="us-meta"><span class="kwd-tag kwd-story">USER STORY US-04</span><span class="mono-meta">Priority: MUST</span></div>
            <p class="us-text"><strong>As an</strong> Operations Analyst,<br><strong>I want</strong> exceptions created for unmatched records,<br><strong>So that</strong> work is not lost in manual trackers and breaches are prevented before gateway cutoff.</p>
          </div>
          <div class="bdd-block" style="margin-top:12px">
            <div class="bdd-head"><span class="kwd-tag kwd-bdd">GHERKIN SCENARIO</span></div>
            <div class="bdd-code">
              <div><span class="bdd-kw">Given</span> internal order #1089 has status 'PAID' via Razorpay</div>
              <div><span class="bdd-kw">When</span> bank settlement feed arrives with missing auth code</div>
              <div><span class="bdd-kw">Then</span> generate exception record with severity 'HIGH'</div>
              <div><span class="bdd-kw">And</span> route to triage queue with a 4-hour SLA timer</div>
            </div>
          </div>
        </div>
      </div>
      <div class="pd-pane" id="pd-rtm" role="tabpanel" tabindex="0" aria-labelledby="pdtab-rtm" hidden>
        <div class="pd-pane-h">Requirements Traceability Matrix (RTM Extract)</div>
        <p class="muted">End-to-End Delivery Verification &bull; Status: Approved</p>
        <div class="pd-sample-box">
          <table class="pd-table">
            <thead>
              <tr><th>Req ID</th><th>Summary</th><th>Functional Spec</th><th>User Story</th><th>Test Scenario</th></tr>
            </thead>
            <tbody>
              <tr><td>BR-01</td><td>Single operational view</td><td>FR-002, FR-004</td><td>US-01, US-03</td><td>TC-001, TC-002</td></tr>
              <tr><td>BR-02</td><td>Identify unmatched records</td><td>FR-005, FR-006, FR-007</td><td>US-03, US-04</td><td>TC-003, TC-004</td></tr>
              <tr><td>BR-03</td><td>Assign, comment and resolve</td><td>FR-008..011</td><td>US-05..07</td><td>TC-006..008</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="pd-pane" id="pd-mom" role="tabpanel" tabindex="0" aria-labelledby="pdtab-mom" hidden>
        <div class="pd-pane-h">Discovery Workshop Minutes &amp; RAID Log</div>
        <p class="muted">Phase 1 Elicitation &bull; Status: Signed Off</p>
        <div class="pd-sample-box">
          <div class="pd-pane-sub">1. Workshop Alignment Summary</div>
          <p>Finance, Operations, and Engineering aligned on batch window timing (23:00 IST cutoff), HMAC webhook security, and a 4-hour SLA on critical exception investigation.</p>
        </div>
      </div>
    </div>
    <div class="pd-foot">
      <a class="btn btn-primary btn-sm" href="samples/docs/PayTrack_Sample_BA_Documentation_Bundle.pdf" target="_blank" rel="noopener noreferrer">Download Full Bundle PDF &rarr;</a>
    </div>
  </div>
</aside>'''

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
<meta property="og:image:alt" content="Gautam Reddy, Business Analyst in Bengaluru: requirements analysis, REST APIs, BRD/FRD, SQL and UAT">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}assets/og-card.png">
<meta name="theme-color" content="#f8fafc" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f19" media="(prefers-color-scheme: dark)">
{url_tags}<link rel="icon" href="{p}assets/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("gr-theme")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}setTimeout(function(){{document.documentElement.classList.add("rv-fallback")}},1200);</script>
<noscript><style>.rv{{opacity:1!important;transform:none!important}}</style></noscript>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{p}assets/style.css?v=33">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="{home}"><img src="{p}assets/mark.svg" alt="" width="30" height="30">Gautam Reddy</a>
<nav class="nav" id="nav" aria-label="Main">{nav}<a href="{p}resume.html" class="nav-resume-btn"{res_cur}>Resume</a></nav>
<div class="tools">
<button class="icon-btn" id="animToggle" type="button" aria-label="Toggle site animations" aria-pressed="false" title="Toggle site animations"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg></button>
<button class="icon-btn" id="theme" type="button" aria-label="Toggle dark theme" aria-pressed="false" title="Toggle dark theme"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>
</div>
<button class="icon-btn menu-btn" id="menu" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open navigation menu">{MENU_ICO}</button>
</div><div class="nav-backdrop" id="navBackdrop" aria-hidden="true"></div></header>
<main id="main" tabindex="-1">
{body}
</main>
{drawer_markup}
<aside id="imageLightbox" class="image-lightbox erd-lightbox" role="dialog" aria-modal="true" aria-label="Artifact Zoom Preview" hidden>
  <div class="ilb-backdrop" id="ilbBackdrop" aria-hidden="true"></div>
  <div class="ilb-dialog">
    <div class="ilb-head">
      <span class="feat-badge ilb-title" id="ilbTitle">Artifact Preview &bull; Full Resolution</span>
      <button class="icon-btn ilb-close" id="ilbClose" type="button" aria-label="Close image viewer">&times;</button>
    </div>
    <div class="ilb-body">
      <img id="ilbImg" alt="Full resolution preview" width="1600" height="1000">
      <p class="ilb-caption" id="ilbCaption"></p>
    </div>
  </div>
</aside>
<footer class="site-footer"><div class="wrap foot">
<div class="foot-main">
  <div class="foot-copy">&copy; <span data-year>2026</span> Gautam Reddy &bull; Business Analyst, Bengaluru, India (IST / UTC+5:30).<br>Sample artifacts on this site are fictional and are labelled as such.</div>
  <nav class="foot-sitemap" aria-label="Footer Navigation">
    <a href="{home}">Home</a>
    <a href="{p}projects.html">Projects</a>
    <a href="{p}samples/index.html">BA Samples</a>
    <a href="{p}services.html">Services</a>
    <a href="{p}about.html">About</a>
    <a href="{p}resume.html">Resume</a>
    <a href="{p}contact.html">Contact</a>
  </nav>
</div>
<nav class="foot-social" aria-label="Social and professional profiles">{ext(GH, "GitHub")}{ext(LI, "LinkedIn")}{ext(HR, "HackerRank")}<a href="mailto:{EMAIL}">Email</a><a href="#main" class="back-to-top" title="Back to top">&uarr; Top</a></nav>
</div></footer>

<script src="{p}assets/vendor/lenis.min.js" defer></script>
<script src="{p}assets/site.js?v=33" defer></script>
</body>
</html>'''

def cta(p="", h="Hiring a Business Analyst, or scoping a piece of work?", t="Share the role or the problem and the outcome you want. I reply with context."):
    cid = f"cta_{abs(hash(h)) % 997}"
    return f'''<section class="sec cta has-flow" id="cta">{F.lifecycle(cid)}<div class="wrap cta-panel">
<h2>{h}</h2><p class="lead">{t}</p>
<div class="actions"><a class="btn btn-primary" href="{p}contact.html">Send an enquiry <span class="arr" aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="{p}samples/index.html">View BA samples</a></div>
</div></section>'''

def head(crumb, h, lead, flow, p=""):
    return f'''<section class="page-head has-flow">{flow}<div class="wrap">
<div class="crumb"><a href="{p}index.html">Home</a> / <span>{crumb}</span></div>
<h1>{h}</h1><p class="lead">{lead}</p>
</div></section>'''

def sh(n, tag, h, p=None):
    p_html = f"<p>{p}</p>" if p else ""
    return f'''<div class="sec-head {rv(0)}"><span class="eyebrow">0{n} &bull; {tag}</span><h2>{h}</h2>{p_html}</div>'''

def tags(l): return '<ul class="tags">' + "".join(f"<li>{t}</li>" for t in l) + '</ul>'

# ---------------------------------------------------------------- projects
GHIMG = "https://opengraph.githubassets.com/1/reddygautam98/"
PROJECTS = [
 ("analytics", "Personal Analytics Project", "Sales Data Analysis", "SQL analysis of product performance, sales by region, and high-value first-quarter transactions.", ["SQL"], GH + "Sales-data-analysis"),
 ("analytics", "Personal Analytics Project", "Loan Data Analytics", "SQL financial analysis covering loan interest rates, loan grades, default patterns and state-level risk trends.", ["SQL", "Finance"], GH + "Loan-data-analytics"),
 ("analytics", "Personal Analytics Project", "Sales Forecasting Report", "Excel reporting on monthly profit trends, sales performance and shipment metrics across business units.", ["Reporting"], GH + "Sales-Forecasting-Report"),
 ("analytics", "Power BI Workforce Analytics", "HR Data Analysis", "Power BI workforce analysis covering employee performance, turnover, tenure and HR trends.", ["Power BI"], GH + "Hr-data-analysis"),
 ("bi", "BI Reporting Prototype", "Business Insights Report", "A structured business report for reviewing sales performance, financial indicators and selected KPIs.", ["BI", "KPIs"], GH + "Business_Insights_Report"),
 ("bi", "BI Dashboard Prototype", "GameZone Business Intelligence", "A business-intelligence dashboard for exploring player retention, user lifecycle and monetization metrics.", ["BI"], GH + "gamezone-business-intelligence"),
 ("data", "Data Pipeline Project", "MetaLayer", "A staged data-engineering workflow organised around structured ingestion, transformation and validation layers.", ["Pipelines"], GH + "MetaLayer"),
 ("ai", "Experimental AI Prototype", "ClinChat-style RAG App", "An experimental retrieval-augmented generation prototype with chunk reference retrieval. Not a clinical product.", ["RAG", "Prototype"], GH + "ClinChat-style-RAG-app"),
 ("writing", "Writing & BA Notes", "Daily Posts & Notes", "Knowledge-sharing notes, analysis patterns and reusable documentation templates.", ["Notes"], GH + "daily_post/blob/main/read.md"),
]

PROJECT_META = {
    "Sales-data-analysis": ("Regional sales and product data analysis", "PostgreSQL, Aggregate Queries", "Summary tables of top revenue drivers and regional patterns"),
    "Loan-data-analytics": ("Loan risk and repayment profiling", "SQL, Risk Analysis", "Identified risk patterns across loan grades and terms"),
    "Sales-Forecasting-Report": ("Monthly profit and sales trend analysis", "Excel, Business Reporting", "Structured quarterly metrics for operational planning"),
    "Hr-data-analysis": ("Workforce turnover & tenure analytics", "Power BI, DAX, Data Modeling", "Interactive HR dashboard tracking retention & performance"),
    "Business_Insights_Report": ("Executive business KPI & margin modeling", "Power BI, KPI Dashboards", "Standardized monthly profit & sales metrics across units"),
    "gamezone-business-intelligence": ("User retention & monetization event analysis", "SQL, Business Intelligence", "Identified drop-off stages in player lifecycle"),
    "MetaLayer": ("Multi-tier ETL pipeline architecture", "Python, Staged Ingestion", "Organised data transformation layers with error tracking"),
    "ClinChat-style-RAG-app": ("Experimental RAG question-answering prototype", "Python, Vector Search", "Traceable chunk reference retrieval with guardrails"),
    "daily_post": ("Business analysis documentation templates", "Technical Writing, Markdown", "Reusable BRD, user story & acceptance criteria templates"),
}

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

ZOOM_ICO = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>'

def pcard(c, i=0, base=0.0):
    k, cat, t, d, tg, u = c
    repo = repo_of(u)
    img_src = LOCAL_PROJECT_IMAGES.get(repo, f"{GHIMG}{repo}")
    img = f'<img src="{img_src}" alt="Screenshot preview of {html.escape(t)} ({html.escape(cat)})" width="1200" height="750" loading="lazy" decoding="async" class="zoomable-img" data-full="{img_src}" data-title="{html.escape(t)} &bull; {html.escape(cat)}" title="Click to view full-resolution screenshot">'
    lbl = f'View repository for {html.escape(t)} on GitHub (opens in new tab)' if k != 'writing' else f'Read notes for {html.escape(t)} on GitHub (opens in new tab)'
    txt = 'Read notes' if k == 'writing' else 'View repository'
    meta = PROJECT_META.get(repo)
    meta_html = ""
    if meta:
        did, tls, outc = meta
        meta_html = f'''<div class="pcard-meta-table">
<div class="pcard-meta-row"><span class="pcard-meta-label">What I did:</span><span>{did}</span></div>
<div class="pcard-meta-row"><span class="pcard-meta-label">Tools:</span><span>{tls}</span></div>
<div class="pcard-meta-row"><span class="pcard-meta-label">Outcome:</span><span>{outc}</span></div>
</div>'''
    return f'''<article class="card pcard magic-card {rv(i, base)}" data-cat="{k}"><div class="thumb browser-frame"><div class="bf-bar" aria-hidden="true"><span class="bf-dot red"></span><span class="bf-dot yellow"></span><span class="bf-dot green"></span><span class="bf-url">{repo}</span></div><div class="bf-viewport"><span class="ph">{F.mini("m" + str(next(_n)))}<em>{html.escape(t)}</em></span>{img}<button type="button" class="img-zoom-btn" aria-label="Zoom screenshot of {html.escape(t)}" data-full="{img_src}" data-title="{html.escape(t)} &bull; {html.escape(cat)}">{ZOOM_ICO}</button></div></div><div class="pbody"><span class="project-transparency-badge">Repository Sample</span><span class="cat">{cat}</span><h3>{t}</h3><p>{d}</p>{meta_html}{tags(tg)}<a class="more" href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{lbl}">{txt} <span class="sr-only">(opens in new tab)</span>&#8599;</a></div></article>'''

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
        rows += (f'<tr tabindex="0" data-links="{links}">'
                 f'<th scope="row"><span class="id" data-id="{br}">{br}</span><br>{label}</th>'
                 f'<td>{_ids(frs)}</td><td>{_ids(uss)}</td><td>{_ids(tcs)}</td></tr>\n')
    return (f'''<div class="trace hero-slider" id="heroSlider" role="region" aria-label="PayTrack deliverables showcase">
<div class="trace-top slider-top">
  <div class="slider-tabs" role="tablist" aria-label="Deliverable slides">
    <button class="slider-tab is-active" role="tab" id="tab-0" aria-selected="true" aria-controls="slide-0" data-slide="0" tabindex="0" type="button"><span class="tab-ico-pill ico-trace"><svg class="tab-ico" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="12" r="3"/><path d="M8.5 7.5l6.5 3.5m-6.5 5.5l6.5-3.5"/></svg></span><span class="tab-txt">Traceability</span></button>
    <button class="slider-tab" role="tab" id="tab-1" aria-selected="false" aria-controls="slide-1" data-slide="1" tabindex="-1" type="button"><span class="tab-ico-pill ico-story"><svg class="tab-ico" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span><span class="tab-txt">User story</span></button>
    <button class="slider-tab" role="tab" id="tab-2" aria-selected="false" aria-controls="slide-2" data-slide="2" tabindex="-1" type="button"><span class="tab-ico-pill ico-api"><svg class="tab-ico" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="12" y1="2" x2="12" y2="22"/></svg></span><span class="tab-txt">REST API</span></button>
    <button class="slider-tab" role="tab" id="tab-3" aria-selected="false" aria-controls="slide-3" data-slide="3" tabindex="-1" type="button"><span class="tab-ico-pill ico-sql"><svg class="tab-ico" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg></span><span class="tab-txt">SQL logic</span></button>
  </div>
  <div class="slider-subbar">
    <div class="subbar-status"><span class="subbar-dot" aria-hidden="true"></span><span>PAYTRACK ARTIFACT SPEC</span></div>
    <div class="slider-nav-ctrls">
      <button class="slider-arrow" id="slidePrev" type="button" aria-label="Previous slide"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg></button>
      <div class="slider-dots" role="group" aria-label="Slide indicators">
        <button class="s-dot is-active" type="button" data-slide="0" aria-label="Slide 1" aria-pressed="true"></button>
        <button class="s-dot" type="button" data-slide="1" aria-label="Slide 2" aria-pressed="false"></button>
        <button class="s-dot" type="button" data-slide="2" aria-label="Slide 3" aria-pressed="false"></button>
        <button class="s-dot" type="button" data-slide="3" aria-label="Slide 4" aria-pressed="false"></button>
      </div>
      <button class="slider-arrow" id="slideNext" type="button" aria-label="Next slide"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
      <button class="slider-arrow" id="slidePauseBtn" type="button" aria-label="Pause slide rotation" aria-pressed="false"><svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg></button>
      <span class="slider-counter" id="slideCount">1 / 4</span>
    </div>
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
    <div class="slide-subhead"><b>US-04: Automated Exception Record Creation</b><span>User story &bull; Gherkin acceptance criteria &bull; Sprint 24</span></div>
    <div class="slide-content-wrap">
      <div class="us-story-card">
        <div class="us-meta"><span class="kwd-tag kwd-story">USER STORY US-04</span><span class="mono-meta">Priority: Must &bull; Traceability: BR-02 / FR-007</span></div>
        <p class="us-text"><b>As an</b> Operations Analyst,<br><b>I want</b> exceptions created for unmatched records,<br><b>So that</b> work is not lost in manual trackers and breaches are prevented before gateway cutoff.</p>
      </div>
      <div class="bdd-block">
        <div class="bdd-head"><span class="kwd-tag kwd-bdd">GHERKIN SCENARIO</span><span class="mono-meta">Scenario: Unmatched gateway authorization code</span></div>
        <div class="bdd-code">
          <div class="bdd-line"><span class="bdd-kw">Given</span> <span class="bdd-tx">internal order #1089 has status <mark class="m-val">'PAID'</mark> via Razorpay</span></div>
          <div class="bdd-line"><span class="bdd-kw">When</span> <span class="bdd-tx">bank settlement feed arrives with missing authorization code</span></div>
          <div class="bdd-line"><span class="bdd-kw">Then</span> <span class="bdd-tx">generate exception record with severity <mark class="m-warn">'HIGH'</mark></span></div>
          <div class="bdd-line"><span class="bdd-kw">And</span> <span class="bdd-tx">route to triage queue with a 4-hour SLA timer</span></div>
        </div>
      </div>
    </div>
    <div class="trace-foot">Gherkin criteria ready for Cucumber/BDD automation. <a href="samples/index.html#user-stories">View stories &rarr;</a></div>
  </div>

  <!-- Slide 3: REST API flow -->
  <div class="slider-slide" id="slide-2" role="tabpanel" aria-labelledby="tab-2" data-index="2" hidden>
    <div class="slide-subhead"><b>PayTrack REST API &amp; Webhook Integration</b><span>POST /v1/payments/verify &bull; Idempotent contract</span></div>
    <div class="slide-content-wrap">
      <div class="api-pipeline">
        <div class="api-node">
          <span class="node-step">01</span>
          <div class="node-info">
            <span class="node-verb verb-post">POST</span>
            <span class="node-path">/v1/payments/verify</span>
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
            <span class="node-path">Daily Batch Match</span>
            <span class="node-detail">99.8% match rate (1,420 / 1,423)</span>
          </div>
        </div>
      </div>
      <div class="schema-preview term-card">
        <div class="schema-head term-head"><div class="term-dots" aria-hidden="true"><span class="t-red"></span><span class="t-yellow"></span><span class="t-green"></span></div><span class="kwd-tag kwd-api">PAYLOAD CONTRACT</span><span class="mono-meta">application/json &bull; Response schema</span></div>
        <pre class="schema-json"><code>&#123;
  <span class="j-k">"batch_id"</span>: <span class="j-s">"REC-2026-9420"</span>,
  <span class="j-k">"total_records"</span>: <span class="j-n">1423</span>,
  <span class="j-k">"matched"</span>: <span class="j-n">1420</span>,
  <span class="j-k">"unmatched_exceptions"</span>: <span class="j-n">3</span>,
  <span class="j-k">"match_rate_pct"</span>: <span class="j-n">99.8</span>,
  <span class="j-k">"sla_status"</span>: <span class="j-s">"WITHIN_SLA"</span>
&#125;</code></pre>
      </div>
    </div>
    <div class="trace-foot">Documented with OpenAPI 3.0 &amp; Postman collections. <a href="samples/index.html#rest-api">View API specs &rarr;</a></div>
  </div>

  <!-- Slide 4: SQL query -->
  <div class="slider-slide" id="slide-3" role="tabpanel" aria-labelledby="tab-3" data-index="3" hidden>
    <div class="slide-subhead"><b>PostgreSQL Exception Detection Query</b><span>Extracts from PayTrack PostgreSQL query templates</span></div>
    <div class="slide-content-wrap">
      <div class="sql-code-box term-card">
        <div class="sql-head term-head"><div class="term-dots" aria-hidden="true"><span class="t-red"></span><span class="t-yellow"></span><span class="t-green"></span></div><span class="kwd-tag kwd-sql">SQL SCRIPT</span><span class="mono-meta">sample_reconciliation_queries.sql</span></div>
        <pre class="sql-view"><code><span class="s-c">-- Identify unmatched records breaching 4-hour triage SLA</span>
<span class="s-k">SELECT</span> pt.payment_id, pt.amount, ge.amount <span class="s-k">AS</span> gateway_amount,
       ROUND(CAST(EXTRACT(EPOCH <span class="s-k">FROM</span> (CURRENT_TIMESTAMP - ec.created_at)) / 3600.0 <span class="s-k">AS</span> numeric), 1) <span class="s-k">AS</span> hours_open,
       <span class="s-k">CASE</span>
         <span class="s-k">WHEN</span> ge.event_id <span class="s-k">IS NULL THEN</span> <span class="s-s">'MISSING_GATEWAY_EVENT'</span>
         <span class="s-k">WHEN</span> pt.amount &lt;&gt; ge.amount <span class="s-k">THEN</span> <span class="s-s">'AMOUNT_MISMATCH'</span>
         <span class="s-k">ELSE</span> <span class="s-s">'OTHER'</span>
       <span class="s-k">END AS</span> mismatch_reason
<span class="s-k">FROM</span> PAYMENT_TRANSACTION pt
<span class="s-k">LEFT JOIN</span> GATEWAY_EVENT ge <span class="s-k">ON</span> pt.payment_id = ge.payment_id
<span class="s-k">JOIN</span> EXCEPTION_CASE ec <span class="s-k">ON</span> pt.payment_id = ec.payment_id
<span class="s-k">WHERE</span> pt.status = <span class="s-s">'UNMATCHED'</span> <span class="s-k">AND</span> ec.case_status &lt;&gt; <span class="s-s">'RESOLVED'</span>
<span class="s-k">ORDER BY</span> hours_open <span class="s-k">DESC LIMIT</span> 4;</code></pre>
      </div>
    </div>
    <div class="trace-foot">Extracts from PayTrack PostgreSQL query templates. <a href="samples/index.html#sql">View SQL repository &rarr;</a></div>
  </div>
</div>
</div>''')

def marquee():
    items = "".join(f"<li>{i}</li>" for i in MARQ_ITEMS)
    return f'''<section class="marq-wrap rv" aria-label="Core competencies marquee">
<button class="marq-toggle icon-only" id="marqToggle" type="button" aria-label="Toggle marquee animation" aria-pressed="false"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg></button>
<div class="marq"><ul class="marq-track" aria-hidden="true">{items}</ul><ul class="marq-track" aria-hidden="true">{items}</ul></div>
</section>'''

ICO_PHASE1 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICO_PHASE2 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
ICO_PHASE3 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>'
ICO_PHASE4 = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'

METHOD_STEPS = [
    (1, "Phase 1: Discover", "Workshops turn scattered requests into one agreed problem statement with assumptions, constraints and named decision owners.", ICO_PHASE1, 20, "+", "workshops run"),
    (2, "Phase 2: Define", "BRD and FRD, business rules, user stories and acceptance criteria, linked to process, API and data flows.", ICO_PHASE2, 2, "", "payment-gateway integrations documented"),
    (3, "Phase 3: Validate", "Traceability from requirement to test, UAT scenarios, expected results and defect triage with QA & Engineering.", ICO_PHASE3, 0, "", "critical defects reported at release"),
    (4, "Phase 4: Hand over", "Business rules, data dictionaries and field mappings are maintained in Confluence and Excel so delivery teams work from one source.", ICO_PHASE4, 100, "%", "RTM coverage maintained")
]

SERVICE_STEPS = [
    (1, "Phase 1: Understand", "Discuss the problem, users, data or systems, constraints, deadlines and what success looks like.", ICO_PHASE1, None, "", "1–2 days &bull; Alignment workshop"),
    (2, "Phase 2: Scope", "Agree deliverables, assumptions, dependencies, review points, responsibilities and a practical timeline.", ICO_PHASE2, None, "", "2–4 days &bull; Scope agreement"),
    (3, "Phase 3: Deliver", "Share drafts, analysis or requirements in checkpoints; collect feedback and resolve agreed changes.", ICO_PHASE3, None, "", "1–3 weeks &bull; Review checkpoints"),
    (4, "Phase 4: Hand over", "Review against acceptance criteria and provide agreed documents, findings or handover notes.", ICO_PHASE4, None, "", "2–3 days &bull; Deliverable sign-off")
]

def make_steps(items):
    out = []
    total = len(items)
    phase_links = {
        1: ("Discovery MoM & Decisions", "samples/index.html#discovery"),
        2: ("BRD & FRD Specifications", "samples/index.html#brd"),
        3: ("RTM & Test Scenarios", "samples/index.html#uat"),
        4: ("Traceability Matrix (RTM)", "samples/index.html#rtm"),
    }
    for i, (num, title, desc, icon_svg, stat_val, stat_suf, stat_lbl) in enumerate(items):
        link_html = ""
        if num in phase_links and total == 4:
            pl_title, pl_href = phase_links[num]
            link_html = f'<div class="step-link-wrap"><a class="step-link" href="{pl_href}">Inspect {pl_title} &rarr;</a></div>'
        out.append(f'''<li class="step-card step-{num} {rv(i)}">
<div class="step-top">
<div class="step-badge" aria-hidden="true">
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
{link_html}
</li>''')
    return "".join(out)

BA_WORKFLOW = [
    ("Stakeholder Mgmt", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>', "Facilitated 20+ workshops with 13+ cross-functional stakeholders"),
    ("Requirements Elicitation", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><path d="M11 8v6M8 11h6"/></svg>', "Captured requirements across 4 business units"),
    ("BRD / FRD Specs", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>', "Documented requirements for 2 payment gateway integrations"),
    ("User Stories & BDD", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>', "Wrote Given/When/Then (BDD) acceptance criteria"),
    ("Traceability (RTM)", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>', "Maintained requirements traceability (RTM) through delivery"),
    ("Scope & Impact", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>', "Managed 12+ change requests with formal impact assessments")
]

PROCESS_WORKFLOW = [
    ("AS-IS / TO-BE", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8L22 12L18 16"/><path d="M2 12H22"/></svg>', "Saved an estimated 2 weeks per improvement cycle"),
    ("Process Mapping (BPMN / UML)", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><path d="M10 6.5h4M17.5 10v4"/></svg>', "Mapped AS-IS / TO-BE business processes and UML system flows"),
    ("Root Cause Analysis", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg>', "Fishbone & 5-Why root cause analysis on recurring SLA shortfalls"),
    ("Business Rules", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M9 15l2 2 4-4"/></svg>', "Maintained business rules and data dictionaries in Confluence and Excel"),
    ("Data Mapping", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>', "Field and data mappings for payment gateway integrations"),
    ("MoSCoW Priorities", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>', "Prioritized requirements across 4 modules and challenged 3 feature requests lacking business justification")
]

AGILE_WORKFLOW = [
    ("Agile / Scrum", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></svg>', "Agile / Scrum delivery across 2 Agile releases"),
    ("Sprint Planning", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>', "Three Amigos sessions and sprint planning"),
    ("Backlog Refinement", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>', "Backlog refinement and MoSCoW prioritization across 4 modules"),
    ("UAT Coordination", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>', "Coordinated UAT across 350+ UAT test scenarios (Marolix) and 50+ (Iinfocomm)"),
    ("Defect Triage", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>', "Supported JIRA defect triage with QA and Engineering; zero critical defects reported"),
    ("Change Management", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>', "Assessed requirement impacts for 12+ change requests across 2 Agile releases")
]

TECH_WORKFLOW = [
    ("REST API Specs", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="2" y1="12" x2="22" y2="12"/></svg>', "OpenAPI 3.0 contracts & webhook payload specs"),
    ("SQL (Postgres)", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>', "Analysed 100,000+ records & query optimization"),
    ("Python (Pandas)", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 4h7v7H4zM13 13h7v7h-7z"/><path d="M14 4h6v6h-6zM4 14h6v6H4z"/></svg>', "Transaction data analysis (100,000+ records) with Pandas"),
    ("Power BI & DAX", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>', "Power BI requirements from Finance and Operations stakeholders"),
    ("JIRA & Confluence", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="m9 12 2 2 4-4"/></svg>', "Requirements repository & sprint backlog boards"),
    ("Figma & Postman", '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><circle cx="11" cy="11" r="2"/></svg>', "Wireframe reviews & API response verification")
]

def workflow_tiles(items):
    out = []
    sample_links = {
        "BRD / FRD Specs": "samples/index.html#brd",
        "User Stories & BDD": "samples/index.html#user-stories",
        "Traceability (RTM)": "samples/index.html#rtm",
        "Process Mapping (BPMN / UML)": "samples/index.html#process-flow",
        "REST API Specs": "samples/index.html#rest-api",
        "UAT Coordination": "samples/index.html#uat",
        "SQL (Postgres)": "samples/index.html#sql",
        "Power BI & DAX": "samples/index.html#power-bi",
        "Stakeholder Mgmt": "samples/index.html#discovery",
    }
    for i, (name, icon, context) in enumerate(items):
        tile_id = f"tk-ev-{abs(hash(name)) % 10000}"
        link_target = sample_links.get(name)
        link_btn = f'<a class="tk-link-hint" href="{link_target}">View sample artifact &rarr;</a>' if link_target else ''
        out.append(f'''<div class="tk-tile">
<button class="tk-toggle" type="button" aria-expanded="false" aria-controls="{tile_id}">
  <span class="tk-ico" aria-hidden="true">{icon}</span>
  <span class="tk-name">{name}</span>
</button>
<div class="tk-evidence" id="{tile_id}"><span>{context}</span>{link_btn}</div>
</div>''')
    return f'<div class="tk-grid">{"".join(out)}</div>'

def paytrack_wireframe_svg():
    return '''<div class="feat-preview" aria-label="PayTrack Reconciliation UI Preview">
  <div class="wf-browser">
    <div class="wf-browser-bar">
      <div class="wf-browser-dots"><span class="wf-dot red"></span><span class="wf-dot yellow"></span><span class="wf-dot green"></span></div>
      <div class="wf-browser-addr"><span>https://ops.paytrack.internal/reconciliation</span></div>
      <div class="wf-browser-badge">Illustrative Mock-up</div>
    </div>
    <div class="wf-screen">
      <div class="wf-side">
        <div class="wf-side-logo"><span class="wf-side-icon"></span><span class="wf-side-name">PayTrack</span></div>
        <div class="wf-side-nav">
          <div class="wf-nav-item active"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Exceptions (2)</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Transactions</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">Audit Log</span></div>
          <div class="wf-nav-item"><span class="wf-nav-bullet"></span><span class="wf-nav-txt">RTM &amp; Trace</span></div>
        </div>
      </div>
      <div class="wf-main">
        <div class="wf-main-head">
          <div><div class="wf-main-title">Reconciliation Exceptions</div><div class="wf-main-sub">FR-005 &bull; Real-time settlement reconciliation (Fictional Sample &bull; Multi-currency USD / INR)</div></div>
          <div class="wf-main-actions"><button type="button" class="wf-btn wf-btn-primary" disabled>Resolve Case</button><button type="button" class="wf-btn" disabled>Export CSV</button></div>
        </div>
        <div class="wf-kpis">
          <div class="wf-kpi-card"><span class="wf-kpi-val">14.2K</span><span class="wf-kpi-lbl">Daily Txns*</span></div>
          <div class="wf-kpi-card warn"><span class="wf-kpi-val">2</span><span class="wf-kpi-lbl">SLA Breaches*</span></div>
          <div class="wf-kpi-card ok"><span class="wf-kpi-val">99.8%</span><span class="wf-kpi-lbl">Reconciled*</span></div>
        </div>
        <div class="wf-table" id="wireframeTable" role="table" aria-label="Reconciliation Exceptions Table">
          <div class="wf-tr wf-th" role="row"><span role="columnheader">TXN_ID</span><span role="columnheader">GATEWAY</span><span role="columnheader">AMOUNT</span><span role="columnheader">STATUS</span><span role="columnheader">SLA DUE</span></div>
          <div class="wf-tr wf-row-cycle is-active-row" id="wfRow1" role="row"><span class="wf-td-code" role="cell">TXN_9841</span><span role="cell">Stripe API</span><span role="cell">$1,420.00</span><span class="wf-badge-warn" role="cell">WARN (Amount)</span><span role="cell">2h 15m</span></div>
          <div class="wf-tr wf-row-cycle" id="wfRow2" role="row"><span class="wf-td-code" role="cell">TXN_9842</span><span role="cell">Razorpay</span><span role="cell">&#8377;68,500.00</span><span class="wf-badge-ok" role="cell">RECONCILED</span><span role="cell">&mdash;</span></div>
          <div class="wf-tr wf-row-cycle" id="wfRow3" role="row"><span class="wf-td-code" role="cell">TXN_9843</span><span role="cell">Stripe Webhook</span><span role="cell">$3,190.00</span><span class="wf-badge-err" role="cell">ERROR (Feed Missing)</span><span role="cell">Overdue (4h 10m)</span></div>
        </div>
      </div>
    </div>
  </div>
</div>'''

def index():
    toolkit_cards = [
        ("Business Analysis", "Chronological Lifecycle: Elicitation &rarr; Analysis &rarr; Specs &rarr; Agile &rarr; Sign-off", BA_WORKFLOW),
        ("Process Analysis & Documentation", "Process Stream: AS-IS Discovery &rarr; Root Cause &rarr; BPMN Modelling &rarr; Specs", PROCESS_WORKFLOW),
        ("Agile, Testing & Delivery", "Delivery Sprint: SDLC &rarr; Planning &rarr; Testing &rarr; UAT &amp; Release", AGILE_WORKFLOW),
        ("Technical Skills & Tools", "Toolchain: Design &rarr; APIs &amp; Contracts &rarr; Analysis &amp; BI", TECH_WORKFLOW)
    ]
    tk = "".join(f'<div class="card kit {rv(i)}"><div class="kit-head"><h3>{g}</h3><span class="kit-sub">{sub}</span></div>{workflow_tiles(wf)}</div>' for i, (g, sub, wf) in enumerate(toolkit_cards))
    return f'''
<section class="hero has-flow">{F.lifecycle("h")}<div class="wrap hero-grid">
<div>
<div class="status rv"><i></i><span>Open to full-time, hybrid &amp; remote BA roles</span></div>
<h1 class="{rv(1)}">Business Analyst in Bengaluru who turns requirements into <span class="grad shiny-text">testable specs.</span></h1>
<p class="lead {rv(2)}">Translating business needs into testable functional and non-functional specifications (NFRs), REST API contracts, and BDD acceptance criteria &mdash; backed by SQL analysis and end-to-end UAT verification.</p>
<div class="actions {rv(3)}"><a class="btn btn-primary" href="samples/index.html">View BA samples <span class="arr" aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="resume.html">View resume</a></div>
<div class="hero-fact-strip {rv(4)}">
  <div class="hfs-item"><b>4+ Years</b><span>BA Experience</span></div>
  <div class="hfs-sep" aria-hidden="true"></div>
  <div class="hfs-item"><b>100K+ Records</b><span>SQL &amp; API Analysis</span></div>
  <div class="hfs-sep" aria-hidden="true"></div>
  <div class="hfs-item"><b>350+ Scenarios</b><span>Jira UAT Coordinated</span></div>
</div>
</div>
<div class="hero-showcase-wrap {rv(2)}">
{trace()}
</div>
</div></section>

{marquee()}

<section class="sec" id="proof"><div class="wrap">
{sh(1, "Proof", "Business analyst results from past delivery work")}
<div class="proof">
<div class="proof-card proof-card-1 {rv(0)}"><b data-count="100" data-suf="K+">100K+</b><span class="source-tag">Marolix &bull; SQL analysis</span><span>transaction records analysed with SQL and Python, surfacing 3 recurring SLA-breach patterns</span></div>
<div class="proof-card proof-card-2 {rv(1)}"><b data-count="350" data-suf="+">350+</b><span class="source-tag">QA &amp; UAT coordination</span><span>test cases coordinated in Jira, with zero critical defects reported</span></div>
<div class="proof-card proof-card-3 {rv(2)}"><b data-count="20" data-suf="+">20+</b><span class="source-tag">Requirements Elicitation</span><span>workshops conducted across 13+ cross-functional stakeholders, aligning functional &amp; non-functional requirements (NFRs)</span></div>
<div class="proof-card proof-card-4 {rv(3)}"><b data-count="2" data-suf="">2</b><span class="source-tag">API &amp; System Integration</span><span>payment gateway integrations documented with REST API requirements, UML flows and data mappings</span></div>
</div>
<p class="note">Metrics from resume and project delivery records (2021&ndash;2024).</p>
</div></section>

<section class="sec band has-flow" id="method">{F.swim("m")}<div class="wrap">
{sh(2, "Method", "How a requirement travels from idea to sign-off", "The same path the sample documents follow.")}
<ol class="steps">{make_steps(METHOD_STEPS)}</ol></div></section>

<section class="sec has-flow" id="work">{F.erd("w")}<div class="wrap">
{sh(3, "Selected work", "Case study and projects", "A fictional end-to-end BA case study, plus personal analytics and data projects. Each card opens its repository.")}
<div class="feature {rv(0)}">
{paytrack_wireframe_svg()}
<div><span class="cat feat-badge">Illustrative Case Study &bull; Fictional Sample</span><h3>PayTrack: payment reconciliation, from BRD to UAT</h3>
<div class="feat-psr">
  <div class="psr-cell"><span class="psr-lbl">Problem</span><p>Operations teams manually investigate mismatched payment records across 2 gateways, taking 48 hours to discover SLA breaches.</p></div>
  <div class="psr-cell"><span class="psr-lbl">Role</span><p>Lead BA: Authored BRD, FRD, NFRs, 10 BDD stories, STTM and REST API sequence flows; mapped 8 requirements to 15 test scenarios.</p></div>
  <div class="psr-cell"><span class="psr-lbl">Result</span><p>Specified automated 99.8% reconciliation matching target and 5-minute exception alerting NFR.</p></div>
</div>
<div class="disclaimer"><b>Fictional sample.</b> * Illustrative targets and metrics for the PayTrack case study scenario. No executed-test evidence is claimed.</div>
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
{sh(5, "Experience", "Professional Business Analyst Experience", "Requirements analysis, stakeholder workshops, system integration, and UAT delivery across past roles.")}
<div class="roles">
<div class="role {rv(0)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Oct 2023 &ndash; Jul 2024</div><h3>Business Analyst &ndash; Marolix Technology Solutions</h3><div class="org">Marolix Technology Solutions Pvt Ltd &bull; Hyderabad, India</div><ul><li>Defined REST API requirements, UML system flows, and Source-to-Target Mappings (STTM) with JSON payload schemas across 2 payment gateway integrations, achieving defect-free production deployment.</li><li>Queried and processed 100,000+ transaction logs with SQL and Python to identify 3 root-cause SLA-breach patterns and formulate automated reconciliation logic.</li><li>Coordinated 350+ UAT test scenarios in Jira across cross-functional squads and assessed 12+ change requests with zero post-release critical defects.</li></ul><button class="role-expander" type="button" aria-expanded="false" aria-controls="role-metrics-0"><span>Key accomplishments &amp; metrics</span> <span class="exp-arr" aria-hidden="true">&#9662;</span></button><div class="role-metrics" id="role-metrics-0" hidden><div class="role-metrics-grid"><div><b>100K+</b><span>Transactions analysed</span></div><div><b>350+</b><span>Test cases coordinated</span></div><div><b>0</b><span>Critical defects reported</span></div><div><b>12+</b><span>Change requests managed</span></div></div></div></div></div>
<div class="role {rv(1)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">May 2022 &ndash; Sep 2023</div><h3>Business Analyst &ndash; V Moksha Technologies</h3><div class="org">V Moksha Technologies Pvt Ltd &bull; Bengaluru, India</div><ul><li>Reduced operational turnaround by an estimated 2 weeks per improvement cycle by leading fishbone and 5-Why root cause analyses on recurring SLA shortfalls.</li><li>Mapped AS-IS and TO-BE business processes to eliminate manual handoff bottlenecks and standardize operational handovers.</li></ul><button class="role-expander" type="button" aria-expanded="false" aria-controls="role-metrics-1"><span>Key accomplishments &amp; metrics</span> <span class="exp-arr" aria-hidden="true">&#9662;</span></button><div class="role-metrics" id="role-metrics-1" hidden><div class="role-metrics-grid"><div><b>2 wks</b><span>Cycle time saved</span></div><div><b>5-Why</b><span>Root-cause analysis</span></div><div><b>AS-IS/TO-BE</b><span>Process mapping</span></div></div></div></div></div>
<div class="role {rv(2)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Aug 2021 &ndash; Apr 2022</div><h3>Business Analyst &ndash; Iinfocomm IT Services</h3><div class="org">Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India</div><ul><li>Facilitated Three Amigos sessions across 4 business units to author BDD Given/When/Then user stories for 3 concurrent modules delivered on schedule.</li><li>Coordinated UAT, regression, and smoke testing across 50+ Jira test cases, resulting in zero reported post-launch incidents.</li><li>Maintained end-to-end Requirements Traceability Matrix (RTM) and validated API contracts against functional specifications.</li></ul><button class="role-expander" type="button" aria-expanded="false" aria-controls="role-metrics-2"><span>Key accomplishments &amp; metrics</span> <span class="exp-arr" aria-hidden="true">&#9662;</span></button><div class="role-metrics" id="role-metrics-2" hidden><div class="role-metrics-grid"><div><b>3</b><span>Concurrent modules</span></div><div><b>4</b><span>Business units</span></div><div><b>50+</b><span>Jira test cases</span></div></div></div></div></div>
<div class="role {rv(3)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Jul 2020 &ndash; Jul 2021</div><h3>Associate Software Engineer &ndash; Iinfocomm IT Services</h3><div class="org">Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India</div><ul><li>Earned early promotion to Business Analyst ahead of schedule after successfully delivering requirements for 3 reporting features.</li><li>Authored Power BI specifications and user stories based on requirements gathered from 15+ Finance and Operations stakeholders, saving an estimated 3+ hrs/week of manual reporting.</li></ul><button class="role-expander" type="button" aria-expanded="false" aria-controls="role-metrics-3"><span>Key accomplishments &amp; metrics</span> <span class="exp-arr" aria-hidden="true">&#9662;</span></button><div class="role-metrics" id="role-metrics-3" hidden><div class="role-metrics-grid"><div><b>Early</b><span>Promotion</span></div><div><b>15+</b><span>Finance &amp; Ops stakeholders</span></div><div><b>3+ hrs</b><span>Projected weekly savings</span></div></div></div></div></div>
</div>
<div class="actions"><a class="btn btn-ghost" href="resume.html">Full resume &amp; print view</a></div>
</div></section>
''' + cta()

# ---------------------------------------------------------------- about
def about_3d_console():
    return '''<div class="about-dossier-wrap" role="region" aria-label="BA Specification Console">
  <div class="about-console">
    <div class="console-head">
      <div class="console-mac-dots" aria-hidden="true">
        <span class="cdot red"></span>
        <span class="cdot yellow"></span>
        <span class="cdot green"></span>
      </div>
      <div class="console-addr">
        <svg class="c-file-ico" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <span>spec // requirements-spec.yml</span>
      </div>
      <div class="console-live-badge"><span class="c-static-dot" aria-hidden="true"></span> ILLUSTRATIVE SAMPLE</div>
    </div>

    <div class="console-hero-row">
      <div class="console-avatar-wrap">
        <div class="console-avatar-ring">
          <img src="assets/mark.svg" alt="" width="46" height="46">
        </div>
      </div>
      <div class="console-info">
        <h3 class="console-name">Gautam Reddy</h3>
        <p class="console-sub">Business Analyst &bull; Requirements, APIs &amp; UAT</p>
        <div class="console-status-pill"><span class="c-status-dot"></span> Traceability &amp; Governance Ready</div>
      </div>
    </div>

    <div class="console-tabs" role="tablist" aria-label="BA Specification Disciplines">
      <button class="console-tab is-active" role="tab" id="ab-tab-0" aria-selected="true" aria-controls="ab-panel-0" data-tab="0" tabindex="0" type="button"><span class="ct-idx">01</span> Rules Engine</button>
      <button class="console-tab" role="tab" id="ab-tab-1" aria-selected="false" aria-controls="ab-panel-1" data-tab="1" tabindex="-1" type="button"><span class="ct-idx">02</span> Change Impact</button>
      <button class="console-tab" role="tab" id="ab-tab-2" aria-selected="false" aria-controls="ab-panel-2" data-tab="2" tabindex="-1" type="button"><span class="ct-idx">03</span> Stakeholders</button>
    </div>

    <div class="console-body">
      <!-- Panel 0: Business Rules Engine (BRE) -->
      <div class="console-panel is-active" id="ab-panel-0" role="tabpanel" tabindex="0" aria-labelledby="ab-tab-0">
        <div class="ba-spec-sheet">
          <div class="ba-spec-hdr">
            <span class="ba-spec-kwd">DECISION TABLE</span>
            <span class="ba-spec-id">SPEC-BRE-204 &bull; Payment &amp; API Business Rules</span>
          </div>
          <div class="ba-rule-rows">
            <div class="ba-rule-row">
              <div class="rule-code">RULE-01</div>
              <div class="rule-body">
                <b>API Idempotency &amp; Duplicate Handling</b>
                <p>When a payment request arrives with an existing idempotency key within 24h, return cached status without re-executing transaction.</p>
              </div>
              <span class="rule-tag tag-auto">Automated</span>
            </div>
            <div class="ba-rule-row">
              <div class="rule-code">RULE-02</div>
              <div class="rule-body">
                <b>Payload Validation &amp; Error Schema</b>
                <p>When mandatory gateway authorization fields are missing or malformed, reject payload immediately with HTTP 422 and structured JSON schema.</p>
              </div>
              <span class="rule-tag tag-auto">Validation</span>
            </div>
            <div class="ba-rule-row">
              <div class="rule-code">RULE-03</div>
              <div class="rule-body">
                <b>Transaction SLA Breach Notification</b>
                <p>When transaction processing exceeds agreed 4-hour SLA window, automatically flag event and route to tier-2 operational queue.</p>
              </div>
              <span class="rule-tag tag-p1">SLA Alert</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel 1: Change Impact Analysis -->
      <div class="console-panel" id="ab-panel-1" role="tabpanel" tabindex="0" aria-labelledby="ab-tab-1" hidden>
        <div class="ba-spec-sheet">
          <div class="ba-spec-hdr">
            <span class="ba-spec-kwd">CHANGE TRIAGE</span>
            <span class="ba-spec-id">CR-208 &bull; Payment Gateway API Migration</span>
          </div>
          <div class="ba-impact-grid">
            <div class="impact-card">
              <span class="impact-lbl">Business &amp; Technical Trigger</span>
              <p>Upgrade to latest payment gateway REST API specification to support unified multi-currency webhook callbacks.</p>
            </div>
            <div class="impact-card">
              <span class="impact-lbl">Upstream Architecture</span>
              <p>Checkout payment gateway client, merchant mobile integration, and order status webhook listeners.</p>
            </div>
            <div class="impact-card">
              <span class="impact-lbl">Downstream Data Impact</span>
              <p>Transaction reconciliation DB schema and internal reporting data dictionary field mappings.</p>
            </div>
            <div class="impact-card">
              <span class="impact-lbl">Mitigation &amp; Rollback Plan</span>
              <p>Dual-endpoint routing during pilot release with automated fallback to previous stable gateway API version.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel 2: Stakeholder Triangulation -->
      <div class="console-panel" id="ab-panel-2" role="tabpanel" tabindex="0" aria-labelledby="ab-tab-2" hidden>
        <div class="ba-spec-sheet">
          <div class="ba-spec-hdr">
            <span class="ba-spec-kwd">STAKEHOLDER TRIANGULATION</span>
            <span class="ba-spec-id">GOV-88 &bull; Competing Priorities Reconciled</span>
          </div>
          <div class="stakeholder-list">
            <div class="sh-item">
              <div class="sh-role"><span class="sh-dot blue"></span>Finance &amp; Operations</div>
              <div class="sh-desc"><strong>Requirement:</strong> Reporting needs captured from Finance and Operations stakeholders.<br><strong>BA Resolution:</strong> Translated into Power BI requirements and BDD user stories.</div>
            </div>
            <div class="sh-item">
              <div class="sh-role"><span class="sh-dot purple"></span>Engineering &amp; Architecture</div>
              <div class="sh-desc"><strong>Requirement:</strong> Clear API contracts and standardized JSON error definitions before sprint commitment.<br><strong>BA Resolution:</strong> OpenAPI 3.0 documentation, sequence diagrams, and Postman collection mockups.</div>
            </div>
            <div class="sh-item">
              <div class="sh-role"><span class="sh-dot green"></span>QA &amp; Product Management</div>
              <div class="sh-desc"><strong>Requirement:</strong> Testable acceptance criteria agreed before development.<br><strong>BA Resolution:</strong> Three Amigos alignment sessions, BDD Given/When/Then scenarios, and end-to-end RTM.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="console-foot">
      <span class="cfoot-id"><span class="cfoot-dot"></span> SPEC-DOC: <code>BA-GOV-2026</code> &bull; Fictional example, not client work</span>
      <a class="cfoot-link" href="samples/index.html">Explore living BA samples &rarr;</a>
    </div>
  </div>
</div>'''

def about():
    return head("About", "Business Analyst: requirements teams can build and validate.", "I connect stakeholder needs, requirements, data, systems and delivery teams, so ambiguous business problems become clear, testable work.", F.seq("a")) + f'''
<section class="sec sec--first"><div class="wrap about-hero-grid">
<div><h2 class="h2-lg {rv(0)}">Who I am</h2>
<div class="about-lead-row {rv(1)}">
  <div class="about-monogram-ring" aria-hidden="true"><div class="about-monogram-inner"><span class="monogram-txt">GR</span></div></div>
  <p class="about-lead">I&rsquo;m Gautam Reddy, a Business Analyst with 4+ years of experience in requirements analysis and delivery, translating business needs into clear, testable functional and non-functional requirements (NFRs).</p>
</div>
<div class="{rv(2)}">
<h3 class="about-subhead">What I do</h3>
<div class="what-i-do-grid">
  <div class="what-card magic-card">
    <div class="what-head"><span class="wid-ico blue" aria-hidden="true">{ICO_PHASE1}</span><b>Elicitation &amp; Scoping</b></div>
    <p>Facilitating stakeholder workshops, validating requirements through sign-off, and prioritizing sprint backlogs with MoSCoW.</p>
  </div>
  <div class="what-card magic-card">
    <div class="what-head"><span class="wid-ico indigo" aria-hidden="true">{ICO_PHASE2}</span><b>Requirements &amp; Specs</b></div>
    <p>Writing BRDs, FRDs, REST API contracts, Source-to-Target Mappings (STTM), use cases, and BDD Given/When/Then acceptance criteria.</p>
  </div>
  <div class="what-card magic-card">
    <div class="what-head"><span class="wid-ico teal" aria-hidden="true">{ICO_PHASE3}</span><b>Data &amp; Process Analysis</b></div>
    <p>SQL querying on 100K+ records, data dictionaries in Confluence/Excel, and AS-IS / TO-BE process modelling with BPMN and UML.</p>
  </div>
  <div class="what-card magic-card">
    <div class="what-head"><span class="wid-ico green" aria-hidden="true">{ICO_PHASE4}</span><b>Testing &amp; UAT Delivery</b></div>
    <p>Requirements Traceability Matrix (RTM), 350+ UAT test scenarios coordination, and JIRA defect triage with Engineering and QA.</p>
  </div>
</div>
</div>
<div class="actions {rv(4)}"><a class="btn btn-primary" href="resume.html">View resume</a><a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">Connect on LinkedIn</a></div></div>
<div class="about-hero-card-col {rv(2)}">
{about_3d_console()}
</div>
</div></section>

<section class="sec band has-flow">{F.pipeline("ab")}<div class="wrap">
{sh(1, "Principles", "Working principles", "The habits behind the documents.")}
<div class="grid g3">
<div class="card principle-card magic-card {rv(0)}"><div class="p-ico-tile" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="m9 15 2 2 4-4"/></svg></div><h3>Evidence before opinion</h3><p>Findings, assumptions and limitations are kept separate, so guesses are never presented as facts.</p><div class="principle-link-foot"><a class="principle-link" href="samples/index.html#discovery">View Discovery MoM sample &rarr;</a></div></div>
<div class="card principle-card magic-card {rv(1)}"><div class="p-ico-tile" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div><h3>Scope you can point at</h3><p>Agreed deliverables and acceptance criteria define what &ldquo;done&rdquo; means before work begins.</p><div class="principle-link-foot"><a class="principle-link" href="samples/index.html#brd">View BRD specification &rarr;</a></div></div>
<div class="card principle-card magic-card {rv(2)}"><div class="p-ico-tile" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div><h3>Traceable by design</h3><p>Requirements connect to stories, tests and decisions, so any change shows its impact.</p><div class="principle-link-foot"><a class="principle-link" href="samples/index.html#rtm">View Requirements Traceability Matrix &rarr;</a></div></div>
</div></div></section>

<section class="sec has-flow">{F.swim("ab2")}<div class="wrap">
{sh(2, "Career path", "Career path &amp; promotions")}
<div class="roles">
<div class="role {rv(0)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Oct 2023 &ndash; Jul 2024</div><h3>Business Analyst &ndash; Marolix Technology Solutions</h3><div class="org">Marolix Technology Solutions Pvt Ltd &bull; Hyderabad, India</div><p class="muted">Led REST API specifications, UML system workflows, and Source-to-Target Mappings (STTM) across 2 payment gateway integrations, achieving defect-free production rollout. Executed SQL data analysis on 100,000+ transaction logs to identify 3 SLA breach patterns, and coordinated 350+ UAT test scenarios in Jira.</p></div></div>
<div class="role {rv(1)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">May 2022 &ndash; Sep 2023</div><h3>Business Analyst &ndash; V Moksha Technologies</h3><div class="org">V Moksha Technologies Pvt Ltd &bull; Bengaluru, India</div><p class="muted">Reduced operational cycle time by an estimated 2 weeks per improvement cycle by resolving recurring SLA shortfalls through SQL data queries, fishbone/5-Why root cause analysis, and AS-IS / TO-BE process mapping.</p></div></div>
<div class="role {rv(2)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Aug 2021 &ndash; Apr 2022</div><h3>Business Analyst &ndash; Iinfocomm IT Services</h3><div class="org">Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India</div><p class="muted">Delivered 3 concurrent modules across 4 business units with zero post-launch incidents by facilitating Three Amigos alignment sessions, authoring BDD acceptance criteria, reviewing API contracts, and coordinating 50+ Jira test cases.</p></div></div>
<div class="role {rv(3)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">Jul 2020 &ndash; Jul 2021</div><h3>Associate Software Engineer &ndash; Iinfocomm IT Services <span class="rank-up-badge"><span aria-hidden="true">&#8679;</span> Promoted early</span></h3><div class="org">Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India</div><p class="muted"><strong>Promoted to Business Analyst ahead of schedule</strong> after managing requirements for 3 reporting features; translated needs from 15+ Finance and Operations stakeholders into Power BI requirements and BDD user stories, securing approval for an automation business case projecting 3+ hrs/week of savings.</p></div></div>
</div></div></section>
''' + cta()

# ---------------------------------------------------------------- services
SERV = [
    ("Business analysis and requirements",
     "Requirements Scoping",
     "Turn fragmented requests into an agreed problem statement, requirements and an actionable backlog.",
     "Engineering is stalled on contradictory stakeholder requests or legacy system gaps.",
     ["BRD / FRD", "Non-Functional Requirements (NFRs)", "User stories & BDD", "Process maps (BPMN / UML)", "Traceability (RTM)"]),
    ("Data analysis and BI reporting",
     "Data Intelligence",
     "Translate operational data and reporting needs into clear Power BI requirements and findings that support decisions.",
     "Leadership needs KPI visibility but source data is scattered across databases and spreadsheets.",
     ["SQL data profiling", "Power BI requirements", "DAX measures", "Reporting user stories", "KPI definition reports"]),
    ("SQL, data quality and reporting",
     "Data Quality",
     "Investigate recurring SLA and error patterns with SQL analysis and root cause analysis, and document the findings.",
     "Recurring reconciliation mismatches or SLA drops are costing team hours each week.",
     ["Data quality profiling", "Root cause analysis (fishbone / 5-Why)", "Business rules & data dictionaries", "Confluence & Excel documentation", "Findings and recommendations"]),
    ("API and integration analysis",
     "System Integration",
     "Make integration expectations explicit for business, engineering and QA teams before implementation and testing.",
     "Connecting external payment gateways, ERPs, or internal microservices without unexpected edge cases.",
     ["REST API requirements", "Source-to-Target Mapping (STTM)", "JSON payload schemas", "API contract review", "UML system flows"]),
    ("UAT, testing and release support",
     "Testing & Verification",
     "Help teams check that a solution meets the agreed requirement and make defects, risks and decisions visible.",
     "Pre-release testing lacks traceability or business users need guidance validating acceptance criteria.",
     ["UAT coordination", "Agile / Scrum delivery", "Functional, regression and integration test cases", "RTM", "JIRA defect triage"]),
    ("Custom BA scope & advisory",
     "Advisory & Discovery",
     "Tailored requirements elicitation, workflow audit, or backlog definition when your team's needs span multiple domains.",
     "You have an ambiguous problem, rapid pilot release, or need cross-functional discovery before committing to sprint delivery.",
     ["Discovery workshop MoM", "Scope definition", "Backlog refinement", "Process gap audit", "Custom deliverables"])
]

DELIV_LINKS = {
    "BRD / FRD": "samples/index.html#brd",
    "Non-Functional Requirements (NFRs)": "samples/index.html#frd",
    "User stories & BDD": "samples/index.html#user-stories",
    "Process maps (BPMN / UML)": "samples/index.html#process-flow",
    "Traceability (RTM)": "samples/index.html#rtm",
    "SQL data profiling": "samples/index.html#sql",
    "REST API requirements": "samples/index.html#rest-api",
    "Source-to-Target Mapping (STTM)": "samples/index.html#rest-api",
    "JSON payload schemas": "samples/index.html#rest-api",
    "UML system flows": "samples/index.html#process-flow",
    "UAT coordination": "samples/index.html#uat",
    "Functional, regression and integration test cases": "samples/index.html#test-cases",
    "RTM": "samples/index.html#rtm",
    "Discovery workshop MoM": "samples/index.html#discovery",
    "Scope definition": "samples/index.html#brd",
    "Custom deliverables": "samples/index.html#bundle"
}

FAQ = [("How do fees and timelines work?", "Fees and timelines depend on complexity, the required deliverables, dependencies and stakeholder review cycles. I can agree a discovery phase or a defined scope after clarifying your goals. For a formal discussion, please use the contact form."),
("Can I start with a small task?", "Yes. A requirements review, data-quality check, process walkthrough or feasibility prototype can be a focused first phase when goals and deliverables are well-defined."),
("Can you work with my existing team?", "Yes. My background includes working directly alongside Product, Engineering, QA and executive business stakeholders. Working cadence and repository access can be agreed before kickoff."),
("Can you work with confidential data?", "Yes. We can establish an NDA and secure handling procedures before sharing proprietary materials. Please avoid transmitting credentials or sensitive personal data in the initial enquiry form.")]

def services():
    cat_colors = ["var(--c-brd)", "var(--c-frd)", "var(--c-sql)", "var(--c-api)", "var(--c-test)", "var(--accent)"]
    cards = ""
    for i, (t, cat_name, d, ideal, tg) in enumerate(SERV):
        c = cat_colors[i % len(cat_colors)]
        def make_deliv_li(x):
            link = DELIV_LINKS.get(x)
            if link:
                return f'<li><a class="deliv-link" href="{link}">{x} &rarr;</a></li>'
            return f'<li>{x}</li>'
        cards += f'''<div class="card scard magic-card rv" style="--d:{(i % 3) * 0.07:.2f}s;--cat-c:{c}">
<div class="scard-top-bar" aria-hidden="true"></div>
<div class="scard-head">
<span class="scard-cat-badge">{cat_name}</span>
<h3>{t}</h3>
</div>
<p class="scard-ideal"><strong>Ideal when:</strong> {ideal}</p>
<p class="scard-outcome"><strong>Outcome:</strong> {d}</p>
<div class="scard-deliverables">
<span class="scard-deliv-title">Typical deliverables:</span>
<ul class="scard-deliv-list">''' + "".join(make_deliv_li(x) for x in tg) + f'''</ul>
</div>
<div class="actions"><a class="btn btn-ghost" href="contact.html?service={urllib.parse.quote_plus(t)}">Enquire about this &rarr;</a></div>
</div>'''
    faq = "".join(f'<details class="faq-item {rv(i, 0.0)}"><summary><span>{q}</span></summary><div class="faq-ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    return head("Services", "Business analysis services with clear scope and useful deliverables.", "Business analysis, data and technology support shaped around the problem, the people who need the answer and the output your team can use.", F.swim("sv")) + f'''
<section class="sec sec--first"><div class="wrap">
{sh(1, "Services", "Business analysis services I offer")}
<div class="grid g3">{cards}</div>
</div></section>

<section class="sec band has-flow">{F.erd("sv2")}<div class="wrap">
{sh(2, "Process", "How an engagement runs", "Clear milestones and check-ins.")}
<ol class="steps service-stepper">{make_steps(SERVICE_STEPS)}</ol>
</div></section>

<section class="sec has-flow">{F.pipeline("sv3")}<div class="wrap">
{sh(3, "Evidence", "What you receive", "Tangible, reviewable artifacts. Review sample file summaries below.")}
<div class="grid g3">
<div class="card peek-card {rv(0)}">
  <div class="peek-badge">DELIVERABLE SPECIFICATION</div>
  <h3>Requirements packs</h3>
  <p>BRDs, FRDs, data dictionaries and Given/When/Then user stories ready for engineering estimation.</p>
  <div class="peek-drawer">
    <div class="peek-drawer-header">Sample artifact extract</div>
    <div class="peek-artifact-meta">
      <span class="peek-file-name">01_BRD_PayTrack_Sample.pdf</span>
      <span class="peek-file-desc">Fictional PayTrack sample BRD covering business need, objectives, scope, stakeholders and requirements.</span>
    </div>
    <a class="btn btn-ghost btn-sm" href="samples/index.html#brd">Open in samples &rarr;</a>
  </div>
</div>
<div class="card peek-card {rv(1)}">
  <div class="peek-badge">SYSTEM INTERFACE &amp; WORKFLOW</div>
  <h3>Process &amp; API models</h3>
  <p>BPMN workflows, swimlanes, ERDs and REST API sequence flows that bridge business rules and system design.</p>
  <div class="peek-drawer">
    <div class="peek-drawer-header">Sample artifact extract</div>
    <div class="peek-artifact-meta">
      <span class="peek-file-name">Payment_API_Sequence.svg</span>
      <span class="peek-file-desc">OpenAPI 3.0 message flows, HMAC verification, webhook callbacks, and settlement exception paths.</span>
    </div>
    <a class="btn btn-ghost btn-sm" href="samples/index.html#process-flow">Open in samples &rarr;</a>
  </div>
</div>
<div class="card peek-card {rv(2)}">
  <div class="peek-badge">QUALITY &amp; VERIFICATION</div>
  <h3>Traceability &amp; UAT plans</h3>
  <p>Requirements Traceability Matrix (RTM) linking requirements to test cases with acceptance criteria and sign-off tracking.</p>
  <div class="peek-drawer">
    <div class="peek-drawer-header">Sample artifact extract</div>
    <div class="peek-artifact-meta">
      <span class="peek-file-name">04_RTM_Test_Cases_UAT_Plan_Sample.pdf</span>
      <span class="peek-file-desc">Fictional sample: traceability matrix linking requirements to 15 test scenarios (not executed).</span>
    </div>
    <a class="btn btn-ghost btn-sm" href="samples/index.html#uat">Open in samples &rarr;</a>
  </div>
</div>
</div></div></section>

<section class="sec"><div class="wrap">
{sh(4, "FAQ", "Questions before starting")}
<div class="faq notfound-wrap" style="margin-top:28px">{faq}</div>
</div></section>
''' + cta(h="Not sure which service fits?", t="Describe the problem and the outcome you want. We can clarify the scope before deciding on next steps.")

# ---------------------------------------------------------------- projects
def projects():
    cat_counts = Counter(c[0] for c in PROJECTS)
    chips = f'<button class="chip is-active" type="button" data-f="all" aria-pressed="true">All ({len(PROJECTS)})</button>' + "".join(
        f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{n} ({cat_counts.get(k, 0)})</button>'
        for k, n in [
            ("analytics", "Analytics"),
            ("bi", "Business intelligence"),
            ("data", "Data engineering"),
            ("ai", "AI prototype"),
            ("writing", "Writing")
        ]
    )
    cards = "".join(pcard(c, i % 3, 0.0) for i, c in enumerate(PROJECTS))
    return head("Projects", "Business analyst projects: practical analysis, visible work.", "Nine technical portfolio projects across SQL analytics, business intelligence, data pipelines, and the PayTrack case study demonstrating BRD, FRD, NFRs, STTM, and RTM traceability.", F.erd("pj")) + f'''
<section class="sec sec--first"><div class="wrap">
<div class="sec-head {rv(0)}"><span class="eyebrow">01 &bull; Case Study</span><h2>Featured case study</h2></div>
<div class="feature featured-paytrack rv">
<div>
  <span class="cat feat-badge">Featured Case Study &bull; Fictional Sample</span>
  <h3>PayTrack: payment reconciliation, from BRD to UAT</h3>
  <div class="feat-psr">
    <div class="psr-cell"><span class="psr-lbl">Problem</span><p>Operations teams manually investigate mismatched payment records across 2 gateways, taking 48 hours to discover SLA breaches.</p></div>
    <div class="psr-cell"><span class="psr-lbl">Role</span><p>Lead BA: Authored BRD, FRD, NFRs, 10 BDD stories, STTM and REST API sequence flows; mapped 8 requirements to 15 test scenarios.</p></div>
    <div class="psr-cell"><span class="psr-lbl">Result</span><p>Specified automated 99.8% reconciliation matching target and 5-minute exception alerting NFR.</p></div>
  </div>
  <div class="mini-dash-stats">
    <div class="mini-stat"><b>99.8%</b><span>Target Match Rate*</span></div>
    <div class="mini-stat"><b>2</b><span>Exceptions Surfaced*</span></div>
    <div class="mini-stat"><b>15</b><span>Traceable Test Cases</span></div>
  </div>
  <div class="disclaimer"><b>Fictional sample.</b> * Illustrative targets and metrics from sample scenario. No executed-test evidence is claimed.</div>
  <div class="actions"><a class="btn btn-primary" href="samples/index.html">Open all artifacts &rarr;</a></div>
</div>
<div class="feat-side">
  <div class="thumb browser-frame">
    <div class="bf-bar" aria-hidden="true"><span class="bf-dot red"></span><span class="bf-dot yellow"></span><span class="bf-dot green"></span><span class="bf-url">ops.paytrack.internal/data-model</span></div>
    <div class="bf-viewport">
      <a class="feat-img" href="samples/diagrams/Payment_Data_Model_ERD.png" data-full="samples/diagrams/Payment_Data_Model_ERD.png" aria-label="Open the data model diagram in high-resolution lightbox" title="Click to inspect high-resolution diagram"><img src="samples/diagrams/Payment_Data_Model_ERD.png" alt="Logical data model (ERD) diagram from the PayTrack payment reconciliation sample" width="1120" height="704" loading="lazy"><span class="feat-zoom-hint" aria-hidden="true">{ZOOM_ICO} Click or tap to expand ERD</span></a>
    </div>
  </div>
  <ul class="feat-links">
    <li><a href="samples/docs/01_BRD_PayTrack_Sample.pdf" target="_blank" rel="noopener noreferrer">Business Requirements Document (BRD) <span class="sr-only">(opens in new tab)</span><span>PDF</span></a></li>
    <li><a href="samples/docs/02_FRD_PayTrack_Sample.pdf" target="_blank" rel="noopener noreferrer">Functional Requirements Document (FRD) <span class="sr-only">(opens in new tab)</span><span>PDF</span></a></li>
    <li><a href="samples/docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf" target="_blank" rel="noopener noreferrer">RTM, test cases and UAT plan <span class="sr-only">(opens in new tab)</span><span>PDF</span></a></li>
  </ul>
</div>
</div>

<div class="sec-head {rv(1)}" style="margin-top:56px"><span class="eyebrow">02 &bull; Repositories</span><h2>Project portfolio</h2><p>Nine personal technical repositories across SQL analytics, dashboards, and data workflows.</p></div>
<div class="filter-wrapper rv">
  <div class="filters" role="group" aria-label="Filter projects">
    <span class="filter-pill" id="filterPill" aria-hidden="true"></span>
    {chips}
  </div>
</div>
<p class="muted small" id="count" aria-live="polite">9 projects</p>
<div class="grid g3" id="pgrid">{cards}</div>
<div class="disclaimer rv" style="margin-top:32px"><b>Portfolio transparency.</b> These are personal portfolio repositories and prototypes, not paid client engagements. Each repository&rsquo;s README contains the exact specifications and source files.</div>
</div></section>
''' + cta(h="Need a similar output?", t="Tell me the question, process or workflow that needs attention and the report, requirements pack or analysis you need.")

# ---------------------------------------------------------------- resume
def resume():
    def role(t, o, d_str, b, skills_tag, i):
        return f'''<div class="role {rv(i)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">{d_str}</div><h3>{t}</h3><div class="org">{o}</div><ul>''' + "".join(f'<li data-skills="{skills_tag}">{x}</li>' for x in b) + '</ul></div></div>'

    def role_tagged(t, o, d_str, tagged_bullets, i):
        lis = "".join(f'<li data-skills="{skills}">{text}</li>' for skills, text in tagged_bullets)
        return f'''<div class="role {rv(i)}"><div class="node" aria-hidden="true"></div><div class="rbody"><div class="role-dates">{d_str}</div><h3>{t}</h3><div class="org">{o}</div><ul>{lis}</ul></div></div>'''

    roles = role_tagged("Business Analyst", "Marolix Technology Solutions Pvt Ltd &bull; Hyderabad, India", "Oct 2023 &ndash; Jul 2024", [
        ("api requirements", "Specified REST API requirements, UML system flows, and Source-to-Target Mappings (STTM) with JSON payload schemas across <strong>2 payment gateway integrations</strong>, enabling defect-free production deployment."),
        ("sql", "Analyzed <strong>100,000+ transaction records</strong> using SQL and Python to isolate 3 recurring SLA breach patterns and formalize automated reconciliation rules."),
        ("requirements", "Secured sign-off from <strong>13+ stakeholders</strong> across <strong>20+ workshops</strong>, authoring BRDs/FRDs, Non-Functional Requirements (NFRs), and Given/When/Then acceptance criteria."),
        ("requirements", "Protected release scope across 4 modules using MoSCoW prioritization, filtering out 3 feature requests that lacked business justification."),
        ("uat", "Coordinated UAT and defect triage across <strong>350+ UAT test scenarios</strong> in Jira with Engineering and QA squads, resulting in zero post-release critical defects."),
        ("requirements uat", "Assessed requirement impact for <strong>12+ change requests</strong> across 2 Agile releases while maintaining end-to-end traceability."),
        ("requirements", "Maintained standardized business rules, data dictionaries, and field mappings in Confluence and Excel for unified engineering alignment.")
    ], 0)

    roles += role_tagged("Business Analyst", "V Moksha Technologies Pvt Ltd &bull; Bengaluru, India", "May 2022 &ndash; Sep 2023", [
        ("sql", "Reduced operational cycle time by an estimated <strong>2 weeks per improvement cycle</strong> by analyzing SLA shortfalls via SQL queries and fishbone/5-Why root-cause analysis."),
        ("requirements", "Mapped AS-IS and TO-BE business workflows in BPMN to remove manual handoff bottlenecks and standardize operational handovers.")
    ], 1)

    roles += role_tagged("Business Analyst", "Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India", "Aug 2021 &ndash; Apr 2022", [
        ("requirements", "Facilitated Three Amigos alignment sessions to deliver <strong>3 concurrent modules</strong> across 4 business units on schedule with Given/When/Then criteria."),
        ("uat", "Coordinated UAT, regression, and smoke testing across <strong>50+ Jira test cases</strong>, achieving zero reported post-launch incidents."),
        ("requirements api", "Maintained the Requirements Traceability Matrix (RTM) and verified API contracts against functional specifications.")
    ], 2)

    roles += role_tagged('Associate Software Engineer <span aria-hidden="true">&rarr;</span> Promoted to BA', "Iinfocomm IT Services Pvt Ltd &bull; Bengaluru, India", "Jul 2020 &ndash; Jul 2021", [
        ("requirements", "Earned early promotion to Business Analyst ahead of schedule after managing requirements for 3 reporting features from elicitation through sign-off."),
        ("bi requirements", "Gathered requirements from 15+ Finance and Operations stakeholders to author Power BI specifications and user stories, saving an estimated <strong>3+ hours/week</strong> of manual reporting."),
        ("bi uat", "Coordinated cross-functional reporting validation checkpoints with Engineering and operational leads.")
    ], 3)

    skills_filter = '''<div class="skills-filter-wrap rv" role="group" aria-label="Filter experience by skill focus">
  <span class="sf-label">Filter bullets by focus:</span>
  <div class="sf-chips">
    <button type="button" class="skill-filter-chip is-active" data-skill="all" aria-pressed="true">All experience</button>
    <button type="button" class="skill-filter-chip" data-skill="requirements" aria-pressed="false">Requirements &amp; BRD</button>
    <button type="button" class="skill-filter-chip" data-skill="sql" aria-pressed="false">SQL &amp; Data Analysis</button>
    <button type="button" class="skill-filter-chip" data-skill="api" aria-pressed="false">REST APIs &amp; Specs</button>
    <button type="button" class="skill-filter-chip" data-skill="bi" aria-pressed="false">BI &amp; Reporting</button>
    <button type="button" class="skill-filter-chip" data-skill="uat" aria-pressed="false">UAT &amp; Agile</button>
    <button type="button" class="skill-filter-chip sf-clear" id="sfClear" hidden aria-label="Clear active filter">&times; Clear</button>
  </div>
  <div id="skillFilterLive" class="sr-only" role="status"></div>
</div>'''

    return head("Resume", "Business Analyst resume: experience, skills, delivery.", "Business Analyst focused on requirements, API and system integration, SQL and Python analysis, Agile delivery and UAT coordination.", F.swim("rs")) + f'''
<section class="sec sec--first"><div class="wrap">
<div class="actions rv" style="margin:0 0 36px">
  <button type="button" class="btn btn-primary" id="printResumeBtn" title="Print ATS-friendly resume or save as PDF"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block;vertical-align:middle;margin-right:6px" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>Print / Save as PDF</button>
  <a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">View LinkedIn profile</a>
  <a class="btn btn-ghost" href="{HR}" target="_blank" rel="noopener noreferrer">HackerRank profile</a>
  <a class="btn btn-ghost" href="contact.html">Contact me</a>
</div>
<div class="proof">
<div class="proof-card {rv(0)}"><b data-count="100" data-suf="K+">100K+</b><span class="source-tag">Marolix &bull; SQL analysis</span><span>transactions analysed</span></div>
<div class="proof-card {rv(1)}"><b data-count="350" data-suf="+">350+</b><span class="source-tag">QA &amp; UAT coordination</span><span>UAT test scenarios coordinated</span></div>
<div class="proof-card {rv(2)}"><b data-count="20" data-suf="+">20+</b><span class="source-tag">Requirements Elicitation</span><span>workshops facilitated across 13+ stakeholders</span></div>
<div class="proof-card {rv(3)}"><b data-count="12" data-suf="+">12+</b><span class="source-tag">2 Agile releases</span><span>change requests managed</span></div>
</div>
<p class="note">Metrics from resume and past project delivery records (2020&ndash;2024).</p>
</div></section>

<section class="sec band has-flow">{F.seq("rs2")}<div class="wrap">
<div class="resume-layout">
  <div class="resume-main">
    {sh(1, "Experience", "Professional experience")}
    {skills_filter}
    <div class="roles">{roles}</div>
    <div style="margin-top:56px">
      {sh(2, "Education", "Education &amp; certifications")}
      <dl class="facts card rv"><dt>Education</dt><dd>B.Tech, Mechanical Engineering, minor in Computer Science. Biju Patnaik University of Technology, Odisha, 2016 to 2020.</dd>
      <dt>Certification</dt><dd>Google Data Analytics Professional Certificate, Coursera, 2023.</dd>
      <dt>In progress</dt><dd><span class="in-prog-dot" aria-hidden="true">&#9675;</span> <strong>CBAP (IIBA)</strong> &bull; Certified Business Analysis Professional &bull; Target completion: 2026/2027</dd></dl>
    </div>
  </div>
  <aside class="resume-sidebar" aria-label="Skills &amp; Expertise sidebar">
    <div class="card resume-side-card rv">
      <h3>Core Competencies &amp; Tools</h3>
      <p class="small muted">Domain depth and practical tools across past roles:</p>
      <div class="skill-meter-list">
        <div class="skill-meter-row">
          <div class="sm-head"><b>Business Analysis</b><span>4+ yrs</span></div>
          <div class="sm-desc">Requirements elicitation, workshops, BRD/FRD, BDD user stories, RTM</div>
        </div>
        <div class="skill-meter-row">
          <div class="sm-head"><b>SQL &amp; Data Analysis</b><span>4+ yrs</span></div>
          <div class="sm-desc">PostgreSQL, root cause analysis, 100K+ transaction datasets</div>
        </div>
        <div class="skill-meter-row">
          <div class="sm-head"><b>API &amp; System Integration</b><span>3+ yrs</span></div>
          <div class="sm-desc">REST API requirements, OpenAPI 3.0, webhooks, payment flows</div>
        </div>
        <div class="skill-meter-row">
          <div class="sm-head"><b>Process Modelling</b><span>3+ yrs</span></div>
          <div class="sm-desc">BPMN, swimlane workflows, gap analysis, AS-IS / TO-BE</div>
        </div>
        <div class="skill-meter-row">
          <div class="sm-head"><b>Agile Delivery &amp; UAT</b><span>4+ yrs</span></div>
          <div class="sm-desc">Scrum, Jira, 350+ UAT test scenarios, zero critical defects reported</div>
        </div>
        <div class="skill-meter-row">
          <div class="sm-head"><b>BI &amp; Reporting</b><span>3+ yrs</span></div>
          <div class="sm-desc">Power BI, DAX measures, automated finance reporting models</div>
        </div>
      </div>
      <h4 class="sidebar-skills-heading" style="margin:20px 0 8px;font-size:.9rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)">Tools</h4>
      <div class="side-tags">{tags(["SQL", "Python", "JIRA", "Confluence", "Postman", "Figma", "Power BI", "Excel"])}</div>
    </div>
  </aside>
</div>
</div></section>
''' + cta(h="Need a BA who connects requirements, data and delivery?", t="Tell me about the role or scope and the outcome your team is aiming for.")

# ---------------------------------------------------------------- contact
def contact():
    opts = lambda l: "".join(f"<option>{o}</option>" for o in l)
    return head("Contact", "Contact a Business Analyst: tell me what you&rsquo;re trying to solve.", "For a full-time, hybrid or remote role, reach out directly. For systems analysis or technical specifications, describe the problem and the outcome.", F.seq("ct")) + f'''
<section class="sec sec--first"><div class="wrap contact-two-col">
<div class="rv contact-rail">
  <h2>Reach me directly</h2>
  <div class="reply-status"><span class="reply-dot-static" aria-hidden="true"></span> Direct email enquiry &bull; Typically replies within 1&ndash;2 business days</div>
  <div class="tz-badge" style="margin-top:14px">
    <span class="tz-globe" aria-hidden="true"><svg class="tz-globe-ico" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></span>
    <span><b>Time zone:</b> IST (UTC+5:30) &bull; Overlap with EMEA / US morning hours</span>
  </div>
  <ul class="contact-list" style="margin-top:20px">
    <li><span>{ICO_MAIL}Email</span><div><a href="mailto:{EMAIL}">{EMAIL}</a> <button class="chip copy" id="copyEmailBtn" type="button" data-copy="{EMAIL}" aria-label="Copy email address">Copy</button><span id="copyStatusLive" role="status" class="sr-only"></span></div></li>
    <li><span>{ICO_LI}LinkedIn</span><div>{ext(LI, "gautam-reddy-analyst")}</div></li>
    <li><span>{ICO_GH}GitHub</span><div>{ext(GH, "reddygautam98")}</div></li>
    <li><span>{ICO_HR}HackerRank</span><div>{ext(HR, "reddygautam98")}</div></li>
    <li><span>{ICO_LOC}Location</span><div>Bengaluru, India (Open to global remote)</div></li>
  </ul>
  <h3 style="margin:32px 0 10px">Useful details to include</h3>
  <ul class="muted" style="padding-left:1.1em;margin:0">
    <li>The problem and who it affects</li>
    <li>The output you need and how it will be used</li>
    <li>Relevant tools, systems, data types and deadlines</li>
    <li>Any constraints or acceptance criteria</li>
  </ul>
  <p class="disclaimer"><b>Please don&rsquo;t include</b> passwords, confidential source files, regulated records or sensitive customer data in a first message.</p>
</div>

<div class="form-card rv">
  <h2 class="h2-md">Project enquiry</h2>
  <p class="muted small" style="margin:8px 0 16px">This site stores nothing. The button opens a draft in your email app and nothing is sent until you press Send.</p>
  <p class="small" style="margin:0 0 16px;color:var(--muted)">* Required fields</p>
  <form id="enquiry" data-email="{EMAIL}" novalidate>
    <div id="form-errors" class="form-errors" role="alert" aria-live="assertive" hidden></div>
    <div class="row2">
      <div class="form-group floating-group"><input id="enquiry-name" name="name" placeholder=" " autocomplete="name" required aria-describedby="err-name"><label for="enquiry-name">Your name *</label><span class="err" id="err-name"></span></div>
      <div class="form-group floating-group"><input id="enquiry-email" name="email" type="email" placeholder=" " autocomplete="email" inputmode="email" required aria-describedby="err-email"><label for="enquiry-email">Email *</label><span class="err" id="err-email"></span></div>
    </div>
    <div class="form-group floating-group"><input id="enquiry-company" name="company" placeholder=" " autocomplete="organization"><label for="enquiry-company">Company (optional)</label></div>
    <div class="form-group floating-group"><select id="enquiry-service" name="service" required aria-describedby="err-service"><option value="" disabled selected>Select a service...</option>{opts(["Business analysis and requirements", "Data analysis and BI reporting", "SQL, data quality and reporting", "API and integration analysis", "UAT, testing and release support", "Custom BA scope & advisory", "A role at my company", "Not sure yet"])}</select><label for="enquiry-service">What do you need help with? *</label><span class="err" id="err-service"></span></div>
    <div class="row2">
      <div class="form-group floating-group"><select id="enquiry-type" name="type"><option value="" disabled selected>Select engagement type...</option>{opts(["Full-time role", "Discovery or review", "Defined deliverable", "Ongoing support", "Prototype or feasibility", "Not sure yet"])}</select><label for="enquiry-type">Engagement type</label></div>
      <div class="form-group floating-group"><select id="enquiry-timeline" name="timeline"><option value="" disabled selected>Select timeline...</option>{opts(["Flexible", "As soon as practical", "Within 2 to 4 weeks", "Within 1 to 3 months", "Specific deadline"])}</select><label for="enquiry-timeline">Target timeline</label></div>
    </div>
    <div class="form-group floating-group"><textarea id="enquiry-msg" name="msg" placeholder=" " required aria-describedby="err-msg"></textarea><label for="enquiry-msg">Describe the problem and the outcome you want *</label><span class="err" id="err-msg"></span></div>
    <div class="form-group floating-group"><input id="enquiry-ref" name="ref" type="url" placeholder=" " aria-describedby="err-ref"><label for="enquiry-ref">Reference link (optional)</label><span class="err" id="err-ref"></span></div>
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap"><button class="btn btn-primary" type="submit">Prepare email draft</button><button class="btn btn-ghost" type="button" id="copyEnquiryBtn">Copy message</button><span class="muted small">Or email directly: <a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
    <p id="sent" class="muted small" hidden role="status">Preparing your email draft. If your email application does not open automatically, please send your enquiry directly to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </form>

  <div class="contact-fallback-card" id="fallbackCard" hidden style="margin-top:24px">
    <div class="cf-head">
      <span class="cf-title">Email client didn&rsquo;t open?</span>
      <span class="cf-sub">Copy this prepared message into your email client:</span>
    </div>
    <textarea class="cf-textarea" id="fallbackTextarea" readonly rows="4" aria-label="Pre-formatted enquiry text to copy"></textarea>
    <div class="cf-actions">
      <button type="button" class="btn btn-sm btn-ghost" id="copyFallbackBtn">Copy to clipboard</button>
      <span class="muted small">Direct recipient: <code>{EMAIL}</code></span>
    </div>
  </div>
</div>
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
ICO_DIAG_FIGJAM = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M8 12a4 4 0 0 1 8 0M12 8v8"/></svg>'

ICO_DATA_RTM = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>'
ICO_DATA_TESTS = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>'
ICO_DATA_STORIES = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>'
ICO_DATA_SQL = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
ICO_EYE = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'

def flink(href, text, ico_type="", download=False, target_blank=True, doc_title=""):
    dl = " download" if download else ""
    tgt = ' target="_blank" rel="noopener noreferrer"' if target_blank else ""
    ico_svg = ""
    cls_extra = ""
    sr_title = f'<span class="sr-only">: {doc_title}</span>' if doc_title else ''
    sr_newtab = '<span class="sr-only"> (opens in new tab)</span>' if target_blank else ''
    hint_title = ' title="Plain text Mermaid source file"' if ico_type == "mmd" else ''

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
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"/><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"/><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"/><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"/></svg>'
    elif ico_type == "figjam":
        cls_extra = " link-btn-figjam"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M8 12a4 4 0 0 1 8 0M12 8v8"/></svg>'
    elif ico_type == "gh":
        cls_extra = " link-btn-gh"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
    elif ico_type == "bi":
        cls_extra = " link-btn-bi"
        ico_svg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>'
    return f'<a href="{href}"{tgt}{dl}{hint_title} class="file-link-btn{cls_extra}">{ico_svg}<span>{text}</span>{sr_title}{sr_newtab}</a>'

# ---------------------------------------------------------------- samples
def sitem(t, d, links, item_id="", ico="", featured=False, status="", phase="all"):
    id_attr = f' id="{item_id}"' if item_id else ''
    feat_cls = ' file-item-featured' if (featured or item_id == 'bundle') else ''
    ico_box = f'<div class="file-item-ico" aria-hidden="true">{ico}</div>' if ico else ''
    if status in ["Approved", "Signed Off", "Validated", "Consolidated"]:
        status_cls = "approved"
    elif status in ["In Review"]:
        status_cls = "review"
    elif status in ["Sprint Ready"]:
        status_cls = "sprint"
    elif status in ["Not Run"]:
        status_cls = "notrun"
    else:
        status_cls = "draft"
    status_badge = f'<span class="status-badge {status_cls}">{status}</span>' if status else ''
    return f'''<li class="rv file-item{feat_cls}"{id_attr} data-phase="{phase}">
  <div class="file-item-main">
    {ico_box}
    <div class="file-item-body">
      <div class="file-item-title-row"><h3>{t}</h3>{status_badge}</div>
      <p>{d}</p>
    </div>
  </div>
  <div class="links">{"".join(links)}</div>
</li>'''

def samples():
    docs_base = "samples/docs"
    def doc_sz(fn):
        p = os.path.join("samples", "docs", fn)
        if os.path.exists(p):
            return round(os.path.getsize(p) / 1024)
        p2 = os.path.join("docs", "samples", "docs", fn)
        if os.path.exists(p2):
            return round(os.path.getsize(p2) / 1024)
        return 100

    sz_bundle = doc_sz("PayTrack_Sample_BA_Documentation_Bundle.pdf")
    sz_brd_pdf = doc_sz("01_BRD_PayTrack_Sample.pdf")
    sz_frd_pdf = doc_sz("02_FRD_PayTrack_Sample.pdf")
    sz_stories_pdf = doc_sz("03_User_Stories_Acceptance_Criteria_Sample.pdf")
    sz_rtm_pdf = doc_sz("04_RTM_Test_Cases_UAT_Plan_Sample.pdf")
    sz_mom_pdf = doc_sz("05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf")

    timeline = '''<div class="phase-timeline-bar rv" role="group" aria-label="Filter deliverables by phase">
  <button type="button" class="pt-step is-active" data-phase="all" aria-pressed="true" title="Show all deliverables"><span class="pt-num">&#10038;</span><span class="pt-name">All Deliverables</span></button>
  <div class="pt-sep" aria-hidden="true">&rarr;</div>
  <button type="button" class="pt-step" data-phase="1" aria-pressed="false" title="Filter to Phase 1: Discovery & MoM"><span class="pt-num">01</span><span class="pt-name">Discovery &amp; MoM</span></button>
  <div class="pt-sep" aria-hidden="true">&rarr;</div>
  <button type="button" class="pt-step" data-phase="2" aria-pressed="false" title="Filter to Phase 2: BRD & FRD Specs"><span class="pt-num">02</span><span class="pt-name">BRD &amp; FRD Specs</span></button>
  <div class="pt-sep" aria-hidden="true">&rarr;</div>
  <button type="button" class="pt-step" data-phase="3" aria-pressed="false" title="Filter to Phase 3: Stories & BDD"><span class="pt-num">03</span><span class="pt-name">Stories &amp; BDD</span></button>
  <div class="pt-sep" aria-hidden="true">&rarr;</div>
  <button type="button" class="pt-step" data-phase="4" aria-pressed="false" title="Filter to Phase 4: RTM & UAT"><span class="pt-num">04</span><span class="pt-name">RTM &amp; UAT</span></button>
</div>'''

    legend = '''<div class="status-legend-bar" aria-label="Document status legend">
  <span class="legend-title">Status Legend:</span>
  <span class="status-badge approved">Approved / Signed Off</span>
  <span class="status-badge review">In Review</span>
  <span class="status-badge sprint">Sprint Ready</span>
  <span class="status-badge draft">Draft / Sample</span>
  <span class="status-badge notrun">Not Run (Mock)</span>
</div>'''

    view_toggle = '''<div class="samples-view-bar">
  <span class="svb-label">Layout:</span>
  <div class="svb-toggles" role="group" aria-label="Choose layout view">
    <button type="button" class="svb-btn is-active" id="viewList" aria-pressed="true" title="List View"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> List</button>
    <button type="button" class="svb-btn" id="viewGrid" aria-pressed="false" title="Grid View"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg> Grid</button>
  </div>
</div>'''

    docs = "".join([
     sitem("Complete Documentation Bundle (Featured)", f"""52 pages &bull; {sz_bundle} KB &bull; All five primary business analysis specifications consolidated in one comprehensive PDF download.
<div class="bundle-fan" aria-hidden="true">
  <div class="fan-doc"><span class="fan-doc-badge pdf">PDF</span><b>01 BRD</b><span>Scope &amp; RACI</span></div>
  <div class="fan-doc"><span class="fan-doc-badge pdf">PDF</span><b>02 FRD</b><span>System Specs</span></div>
  <div class="fan-doc"><span class="fan-doc-badge pdf">PDF</span><b>03 Stories</b><span>BDD Criteria</span></div>
  <div class="fan-doc"><span class="fan-doc-badge pdf">PDF</span><b>04 RTM</b><span>UAT &amp; Tests</span></div>
  <div class="fan-doc"><span class="fan-doc-badge pdf">PDF</span><b>05 MoM</b><span>RAID Log</span></div>
</div>""", [flink("docs/PayTrack_Sample_BA_Documentation_Bundle.pdf", f"Download PDF Bundle ({sz_bundle} KB)", "pdf", doc_title="Complete Documentation Bundle"), f'<button class="file-link-btn link-btn-preview" type="button" data-preview="bundle">{ICO_EYE}<span>Quick In-Page Preview</span></button>'], "bundle", ICO_DOC_BUNDLE, featured=True, status="Consolidated", phase="all"),
     sitem("Discovery Workshop MoM & Decision Log", f"Phase 1 &bull; 6 pages ({sz_mom_pdf} KB) &bull; Workshop summary, discussion themes, open decisions, action tracker and RAID log.", [flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf", "PDF", "pdf", doc_title="Discovery Workshop MoM PDF"), flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.docx", "Word", "word", target_blank=False, doc_title="Discovery Workshop MoM Word")], "discovery", ICO_DOC_DISCOVERY, status="Signed Off", phase="1"),
     sitem("Business Requirements Document (BRD)", f"Phase 2 &bull; 12 pages ({sz_brd_pdf} KB) &bull; Business need, objectives, scope, stakeholders, assumptions, requirements and sign-off template.", [flink("docs/01_BRD_PayTrack_Sample.pdf", "PDF", "pdf", doc_title="Business Requirements Document PDF"), flink("docs/01_BRD_PayTrack_Sample.docx", "Word", "word", target_blank=False, doc_title="Business Requirements Document Word")], "brd", ICO_DOC_BRD, status="Approved", phase="2"),
     sitem("Functional Requirements Document (FRD)", f"Phase 2 &bull; 16 pages ({sz_frd_pdf} KB) &bull; Functional behaviour, business rules, data entities, screen requirements, NFRs, error states and decisions to confirm.", [flink("docs/02_FRD_PayTrack_Sample.pdf", "PDF", "pdf", doc_title="Functional Requirements Document PDF"), flink("docs/02_FRD_PayTrack_Sample.docx", "Word", "word", target_blank=False, doc_title="Functional Requirements Document Word")], "frd", ICO_DOC_FRD, status="In Review", phase="2"),
     sitem("User Stories and Acceptance Criteria", f"Phase 3 &bull; 8 pages ({sz_stories_pdf} KB) &bull; Prioritised stories with testable Given / When / Then criteria across operational personas.", [flink("docs/03_User_Stories_Acceptance_Criteria_Sample.pdf", "PDF", "pdf", doc_title="User Stories and Acceptance Criteria PDF"), flink("docs/03_User_Stories_Acceptance_Criteria_Sample.docx", "Word", "word", target_blank=False, doc_title="User Stories and Acceptance Criteria Word")], "user-stories", ICO_DOC_STORIES, status="Sprint Ready", phase="3"),
     sitem("RTM, Test Cases and UAT Plan", f"Phase 4 &bull; 10 pages ({sz_rtm_pdf} KB) &bull; Traceability from requirement to test, test-case catalogue, UAT entry and exit criteria, sign-off record.", [flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf", "PDF", "pdf", doc_title="RTM and UAT Plan PDF"), flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.docx", "Word", "word", target_blank=False, doc_title="RTM and UAT Plan Word")], "uat", ICO_DOC_RTM, status="Draft", phase="4")])

    dg = "".join([
     sitem("Payment reconciliation process flow", "Phase 2 &bull; Matched path, validation failure, exception creation, review, resolution or escalation, and audit trail.", [flink("diagrams/Payment_Reconciliation_Process.svg", "SVG", "img", doc_title="Process Flow SVG"), flink("diagrams/Payment_Reconciliation_Process.png", "PNG", "img", doc_title="Process Flow PNG"), flink("diagrams/Payment_Reconciliation_Process.mmd", "Mermaid", "mmd", target_blank=False, doc_title="Process Flow Mermaid")], "process-flow", ICO_DIAG_PROCESS, status="Validated", phase="2"),
     sitem("Conceptual solution architecture", "Phase 2 &bull; Portal, API, reconciliation service, data store, gateway adapter, audit and access control.", [flink("diagrams/Payment_Conceptual_Architecture.svg", "SVG", "img", doc_title="Architecture SVG"), flink("diagrams/Payment_Conceptual_Architecture.png", "PNG", "img", doc_title="Architecture PNG")], "architecture", ICO_DIAG_ARCH, status="Draft", phase="2"),
     sitem("Logical data model (ERD)", "Phase 2 &bull; Entities and relationships for transactions, gateway events, reconciliation results, exceptions and audit events.", [flink("diagrams/Payment_Data_Model_ERD.svg", "SVG", "img", doc_title="ERD SVG"), flink("diagrams/Payment_Data_Model_ERD.png", "PNG", "img", doc_title="ERD PNG"), flink("diagrams/Payment_Data_Model_ERD.mmd", "Mermaid", "mmd", target_blank=False, doc_title="ERD Mermaid")], "erd", ICO_DIAG_ERD, status="Approved", phase="2"),
     sitem("API sequence diagram", "Phase 2 &bull; Message flow for payment submission, gateway event, reconciliation and status query.", [flink("diagrams/Payment_API_Sequence.svg", "SVG", "img", doc_title="Sequence Diagram SVG"), flink("diagrams/Payment_API_Sequence.mmd", "Mermaid", "mmd", target_blank=False, doc_title="Sequence Diagram Mermaid")], "rest-api", ICO_DIAG_API, status="Validated", phase="2"),
     sitem("Power BI operations dashboard (Related project)", "Phase 3 &bull; Operational KPI tracking, reconciliation exception metrics, DAX measures and executive dashboard views. Links to related HR analytics repository.", [flink("../projects.html#bi", "Power BI Projects &#8599;", "bi", target_blank=False, doc_title="Power BI Portfolio"), flink("https://github.com/reddygautam98/Hr-data-analysis", "GitHub Repo (HR Analytics) &#8599;", "gh", doc_title="GitHub HR Repository")], "power-bi", ICO_DIAG_BI, status="Sample", phase="3"),
     sitem("Figma UI wireframes", "Phase 1 &bull; Editable overview dashboard and exception case-detail screens. Values are illustrative.", [flink("https://www.figma.com/design/qt1PFmcQNvtaJnLnrWxPKD", "Figma &#8599;", "figma", doc_title="Figma Wireframes")], "figma", ICO_DIAG_FIGMA, status="Draft", phase="1"),
     sitem("FigJam BA diagrams", "Phase 1 &bull; Editable process, API sequence and ERD diagrams on one collaborative board.", [flink("https://www.figma.com/board/N90uAbHaqe4OkCOUkNfNxX", "FigJam &#8599;", "figjam", doc_title="FigJam Board")], "figjam", ICO_DIAG_FIGJAM, status="Draft", phase="1")])

    sp = "".join([
     sitem("Requirements traceability matrix", "Phase 4 &bull; Maps business requirements to functional requirements, stories and test cases.", [flink("specs/requirements_traceability.csv", "CSV", "csv", download=True, target_blank=False, doc_title="Traceability CSV")], "rtm", ICO_DATA_RTM, status="Approved", phase="4"),
     sitem("Sample test cases", "Phase 4 &bull; Scenarios, preconditions, steps, expected results, traceability and Not Run status.", [flink("specs/sample_test_cases.csv", "CSV", "csv", download=True, target_blank=False, doc_title="Test Cases CSV")], "test-cases", ICO_DATA_TESTS, status="Not Run", phase="4"),
     sitem("Sample user stories", "Phase 3 &bull; JIRA and Confluence backlog starter with Agile / Scrum priority, acceptance criteria and traceability.", [flink("specs/sample_user_stories.csv", "CSV", "csv", download=True, target_blank=False, doc_title="User Stories CSV")], "user-stories-csv", ICO_DATA_STORIES, status="Sprint Ready", phase="3"),
     sitem("SQL reconciliation and data validation queries", "Phase 3 &bull; Analytical SQL queries to detect amount mismatches, orphan gateway events and 4-hour SLA breach exceptions.", [flink("specs/sample_reconciliation_queries.sql", "SQL", "sql", download=True, target_blank=False, doc_title="Reconciliation Queries SQL"), flink("../projects.html#analytics", "SQL Projects &#8599;", "sql", target_blank=False, doc_title="SQL Projects Portfolio")], "sql", ICO_DATA_SQL, status="Validated", phase="3")])

    return head("BA samples", "Business analyst sample documents: requirements, models and test evidence.", "One connected, fictional case study that shows how a business problem becomes functional requirements, NFRs, Source-to-Target Mappings (STTM), prioritised Agile stories, test coverage (RTM), and process models.", F.lifecycle("sm"), "../") + f'''
<section class="sec sec--first"><div class="wrap">
<div class="disclaimer rv" style="margin:0 0 28px"><b>Sample only, fictional case study.</b> PayTrack is an invented payment reconciliation and exception-management portal. Names, IDs, amounts, targets and scenarios are illustrative. Test cases have not been executed and no client outcome is claimed.</div>
{timeline}
<div class="samples-ctrl-row rv">{legend}{view_toggle}</div>

<div class="file-sec" id="sec-docs">
  <h2 class="rv sec-title-with-ico sec-title-docs" style="margin-bottom:20px"><span class="sec-hdr-ico sec-hdr-docs">{ICO_SEC_DOCS}</span><span class="sec-title-text">Documents</span></h2>
  <ul class="file-list">{docs}</ul>
</div>

<div class="file-sec" id="sec-diag">
  <h2 class="rv sec-title-with-ico sec-title-diag" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-diag">{ICO_SEC_DIAG}</span><span class="sec-title-text">Diagrams and design</span></h2>
  <ul class="file-list">{dg}</ul>
</div>

<div class="file-sec" id="sec-data">
  <h2 class="rv sec-title-with-ico sec-title-data" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-data">{ICO_SEC_DATA}</span><span class="sec-title-text">Structured data</span></h2>
  <ul class="file-list">{sp}</ul>
</div>

<div id="samplesLive" class="sr-only" role="status"></div>
<p class="note rv" style="margin-top:32px">Scenario: PayTrack compares internal payment records with gateway events, helps operations staff investigate unmatched transactions, assigns ownership of exceptions and keeps an audit trail. Everything here is an illustrative artifact designed to demonstrate business analysis rigor.</p>
</div></section>
''' + cta("../")

DESC = "Business Analyst in Bengaluru with 4+ years of experience: BRD/FRD, NFRs, REST APIs, STTM, SQL, Power BI and UAT. Open to remote and hybrid roles."
PERSON_ID = SITE + "#person"
PERSON = {"@type": "Person", "@id": PERSON_ID, "name": "Gautam Reddy", "jobTitle": "Business Analyst",
    "description": DESC, "url": SITE, "sameAs": [LI, GH, HR],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Biju Patnaik University of Technology"},
    "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "Google Data Analytics Professional Certificate", "credentialCategory": "certificate"},
    "knowsAbout": ["Technical Business Analysis", "Requirements Engineering", "Stakeholder Management", "BRD and FRD", "Non-Functional Requirements (NFRs)", "User Stories", "Acceptance Criteria", "UAT", "SQL", "Python", "Power BI", "Agile", "Scrum", "Jira", "Confluence", "REST API Requirements", "Source-to-Target Mapping (STTM)", "JSON Schemas", "Postman", "Payment Gateway Integrations", "Transaction Data Analysis", "SLA Breach Analysis", "Root Cause Analysis", "Process Mapping (BPMN / UML)", "Requirements Traceability Matrix (RTM)", "BDD Acceptance Criteria", "Finance and Operations Reporting Requirements"]}

def ldscript(*objs):
    return f'<script type="application/ld+json">\n{json.dumps({"@context": "https://schema.org", "@graph": list(objs)}, ensure_ascii=False, indent=2)}\n</script>\n'

def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

WEBSITE = {"@type": "WebSite", "@id": SITE + "#website", "name": "Gautam Reddy - Business Analyst Portfolio", "url": SITE, "inLanguage": "en-IN", "publisher": {"@id": PERSON_ID}}
LD_HOME = ldscript(WEBSITE, PERSON)
LD_ABOUT = ldscript({"@type": "ProfilePage", "url": SITE + "about.html", "name": "About Gautam Reddy", "mainEntity": {"@id": PERSON_ID}}, PERSON, crumbs("About", "about.html"))
LD_SERVICES = ldscript({"@type": "ProfessionalService", "name": "Gautam Reddy - Business Analysis Services", "url": SITE + "services.html", "provider": {"@id": PERSON_ID},
    "areaServed": "Worldwide (remote) and Bengaluru, India", "serviceType": [item[0] for item in SERV]}, crumbs("Services", "services.html"))
LD_PROJECTS = ldscript({"@type": "CollectionPage", "url": SITE + "projects.html", "name": "Business analyst projects", "mainEntity": {"@type": "ItemList", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "name": c[2], "url": c[5]} for i, c in enumerate(PROJECTS)]}}, crumbs("Projects", "projects.html"))
LD_RESUME = ldscript({"@type": "ProfilePage", "url": SITE + "resume.html", "name": "Gautam Reddy resume", "mainEntity": {"@id": PERSON_ID}}, crumbs("Resume", "resume.html"))
LD_CONTACT = ldscript({"@type": "ContactPage", "url": SITE + "contact.html", "name": "Contact Gautam Reddy", "mainEntity": {"@id": PERSON_ID}}, crumbs("Contact", "contact.html"))
LD_SAMPLES = ldscript({"@type": "CollectionPage", "url": SITE + "samples/index.html", "name": "PayTrack BA sample documents (fictional)", "author": {"@id": PERSON_ID}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "BA samples", "item": SITE + "samples/index.html"}]})

pages = [
("index.html", "Gautam Reddy | Business Analyst: Requirements, APIs, SQL, UAT", DESC, index(), "", "", LD_HOME),
("about.html", "About Gautam Reddy | Business Analyst", "About Gautam Reddy, a Bengaluru Business Analyst with 4+ years of experience in requirements engineering, NFRs, REST APIs, STTM, SQL analysis and UAT.", about(), "", "about.html", LD_ABOUT),
("services.html", "BA Services: BRD, APIs, SQL & UAT | Gautam Reddy", "Business analysis services: BRD/FRD, NFRs, SQL and Python data analysis, STTM, Power BI dashboards, REST API specs and Agile UAT coordination.", services(), "", "services.html", LD_SERVICES),
("projects.html", "BA Projects: SQL, Power BI & Case Studies | Gautam Reddy", "Portfolio projects by Business Analyst Gautam Reddy: SQL and Power BI analytics, data pipelines, RAG prototypes, and the PayTrack case study.", projects(), "", "projects.html", LD_PROJECTS),
("resume.html", "Resume | Gautam Reddy, Business Analyst", "Resume of Gautam Reddy, Business Analyst with 4+ years of experience: 2 payment gateway integrations, STTM, NFRs, 100,000+ transactions analysed, 350+ UAT test scenarios.", resume(), "", "resume.html", LD_RESUME),
("contact.html", "Contact Gautam Reddy | Hire a Business Analyst, Bengaluru", "Contact Gautam Reddy, a Business Analyst in Bengaluru, about full-time, hybrid or remote roles, or requirements, systems integration, and reporting projects.", contact(), "", "contact.html", LD_CONTACT),
("samples/index.html", "BA Sample Documents: BRD, FRD, Stories & RTM | Gautam Reddy", "Business Analyst case study artifacts: BRD, FRD, NFRs, user stories, STTM, RTM, UAT plan, BPMN and UML diagrams, SQL queries and CSV templates.", samples(), "../", "samples/index.html", LD_SAMPLES),
]
for path, t, d, b, p, cur, ld in pages:
    open(path, "w", encoding="utf-8").write(page(path, t, d, b, p, cur, ld))

NOT_FOUND = '''<section class="sec notfound-sec"><div class="wrap notfound-wrap">
<div class="notfound-badge">404 &bull; MISSING REQUIREMENT</div>
<h1>Path not found in specification</h1>
<p class="lead" style="margin-top:16px">Page not found. The requested URL does not match any route or documented artifact in this portfolio.</p>

<div class="notfound-flow" aria-hidden="true">
  <div class="nf-node"><span class="nf-step">01</span><span>Incoming Route</span></div>
  <div class="nf-arrow broken">&dash;&dash;&times;&dash;&dash;</div>
  <div class="nf-node dead"><span class="nf-step">404</span><span>Unmapped Endpoint</span></div>
</div>

<div class="actions" style="margin-top:28px">
<a class="btn btn-primary" href="index.html">Return to homepage <span class="arr" aria-hidden="true">&rarr;</span></a>
<a class="btn btn-ghost" href="samples/index.html">View BA samples</a>
<a class="btn btn-ghost" href="projects.html">Browse projects</a>
</div>

<div class="notfound-links-card card" style="margin-top:36px">
  <h3>Popular destinations</h3>
  <ul class="notfound-links-list">
    <li><a href="samples/index.html#brd"><b>Business Requirements Document (BRD)</b> &bull; PayTrack payment reconciliation sample</a></li>
    <li><a href="resume.html"><b>Resume &amp; Experience</b> &bull; 4+ years BA experience, STTM, SQL, UAT</a></li>
    <li><a href="services.html"><b>BA Services &amp; Deliverables</b> &bull; Scoping, process mapping, test planning</a></li>
    <li><a href="contact.html"><b>Contact Gautam Reddy</b> &bull; Role enquiries &amp; direct email</a></li>
  </ul>
</div>
</div></section>'''
open("404.html", "w", encoding="utf-8").write(page("404.html", "Page not found | Gautam Reddy, Business Analyst", "This page could not be found.", NOT_FOUND, "", "", "", "noindex, follow"))

import datetime
today = datetime.date.today().isoformat()
urls = [SITE if p_ == "index.html" else SITE + p_ for p_, *_ in pages]
open("sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
print("built", len(pages))
