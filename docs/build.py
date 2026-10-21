"""Regenerates all 7 HTML pages. Run:  python3 build.py
Edit copy / links here, then rebuild. Diagrams come from flows.py."""
import html, json
import flows as F

SITE = "https://reddygautam98.github.io/GautamTheAnalyst.io/"
GH = "https://github.com/reddygautam98/"
LI = "https://www.linkedin.com/in/gautam-reddy-analyst"
HR = "https://www.hackerrank.com/profile/reddygautam98"
EMAIL = "trkr725@gmail.com"
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600&display=swap"
NAV = [("projects.html", "Projects"), ("samples/index.html", "BA samples"), ("services.html", "Services"), ("about.html", "About"), ("resume.html", "Resume"), ("contact.html", "Contact")]

# Search terms recruiters and ATS filters use for Business Analyst roles, limited to what Gautam actually does.
KW_ROW1 = ["Business Analyst", "Requirements Gathering", "Stakeholder Management", "BRD / FRD / SRS", "User Stories", "BDD Acceptance Criteria", "Gap Analysis",
           "Process Modelling (BPMN / UML)", "UAT", "Agile / Scrum", "Jira", "Confluence", "Traceability Matrix (RTM)", "MoSCoW Prioritisation", "Change Management"]
KW_ROW2 = ["SQL", "Python (Pandas)", "Power BI", "DAX", "Advanced Excel", "Data Analysis", "KPI and Dashboards", "REST API Requirements", "Postman", "Payments", "Settlement and Reconciliation",
           "BFSI", "Fintech", "Payment Gateways", "Transaction Processing", "SLA Monitoring", "Operations Reporting", "Three Amigos"]
META_KW = ", ".join(["Business Analyst", "Business Analyst Bengaluru", "Fintech Business Analyst", "BFSI Business Analyst", "Functional Analyst", "Business Systems Analyst",
                     "requirements gathering", "stakeholder management", "BRD", "FRD", "user stories", "acceptance criteria", "UAT", "SQL", "Python", "Power BI", "Agile", "Scrum",
                     "Jira", "Postman", "REST API", "payment gateway integrations", "transaction processing", "settlement and reconciliation", "SLA monitoring", "finance and operations reporting", "process mapping", "gap analysis"])
ROLES_ROT = ["Requirements Gathering", "BRD / FRD & User Stories", "REST API & System Integration", "SQL & Python Analysis", "Power BI & KPI Dashboards", "Settlement & Reconciliation", "UAT & Agile Delivery"]


def ext(u, t): return f'<a href="{u}" target="_blank" rel="noopener noreferrer">{t}</a>'
def rv(i=0, base=0.0, step=0.07): return f'rv" style="--d:{base + i * step:.2f}s'

ICO_MAIL = '<svg class="ico-gmail" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="#4285F4" d="M3.2 5.5A2.5 2.5 0 0 0 .7 8v10.5A2.5 2.5 0 0 0 3.2 21H5V11.25L3.2 9.8z"/><path fill="#34A853" d="M20.8 5.5a2.5 2.5 0 0 1 2.5 2.5V18.5a2.5 2.5 0 0 1-2.5 2.5H19V11.25l1.8-1.45z"/><path fill="#FBBC05" d="M19 11.25L12 16.5 5 11.25V21h14z"/><path fill="#EA4335" d="M3.2 5.5c-.8 0-1.5.5-1.8 1.25L12 13.5l10.6-6.75c-.3-.75-1-1.25-1.8-1.25z"/></svg>'
ICO_LI = '<svg class="ico-li" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#ffffff" d="M19 19h-3.14v-4.9c0-1.17-.02-2.67-1.63-2.67-1.63 0-1.88 1.27-1.88 2.58V19H9.21V9h3.01v1.37h.04c.42-.79 1.44-1.63 2.96-1.63 3.17 0 3.75 2.09 3.75 4.8V19zM5.34 7.63a1.74 1.74 0 1 1 0-3.48 1.74 1.74 0 0 1 0 3.48zM6.91 19H3.77V9h3.14v10z"/></svg>'
ICO_GH = '<svg class="ico-gh" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
ICO_HR = '<svg class="ico-hr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#00EA64"/><path fill="#ffffff" d="M9.95 8.002h1.805c.061 0 .111.05.111.111v7.767c0 .061-.05.111-.11.111H9.95c-.061 0-.111-.05-.111-.11v-2.87H7.894v2.87c0 .06-.05.11-.11.11H5.976a.11.11 0 01-.11-.11V8.112c0-.06.05-.11.11-.11h1.806c.061 0 .11.05.11.11v2.869H9.84v-2.87c0-.06.05-.11.11-.11zm2.999 0h5.778c.061 0 .111.05.111.11v7.767a.11.11 0 01-.11.112h-5.78a.11.11 0 01-.11-.11V8.111c0-.06.05-.11.11-.11z"/></svg>'
ICO_LOC = '<svg class="ico-loc" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'

def page(path, title, desc, body, p="", cur="", ld=""):
    nav = "".join('<a href="%s%s"%s>%s</a>' % (p, h, ' aria-current="page"' if h == cur else "", t) for h, t in NAV)
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(META_KW)}">
<meta name="author" content="Gautam Reddy">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#f4f6fb">
<link rel="icon" href="{p}assets/mark.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("gr-theme")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{p}assets/style.css?v=22">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="{p}index.html"><img src="{p}assets/mark.svg" alt="" width="30" height="30">Gautam Reddy</a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<div class="tools"><button class="icon-btn" id="theme" type="button" aria-label="Switch theme" aria-pressed="false">&#9790;</button></div>
<button class="icon-btn menu-btn" id="menu" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">&#9776;</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap foot">
<div>&copy; <span data-year>2026</span> Gautam Reddy. Business Analyst, Bengaluru, India.<br>Sample artifacts on this site are fictional and are labelled as such.</div>
<nav aria-label="Footer"><a href="{p}resume.html">Resume</a>{ext(GH, "GitHub")}{ext(LI, "LinkedIn")}{ext(HR, "HackerRank")}<a href="mailto:{EMAIL}">Email</a></nav>
</div></footer>

<script src="{p}assets/vendor/lenis.min.js" defer></script>
<script src="{p}assets/site.js?v=22" defer></script>
</body>
</html>
'''

def cta(p="", h="Hiring a Business Analyst, or scoping a piece of work?", t="Share the role or the problem and the outcome you want. I reply with context."):
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta has-flow">{F.lifecycle("c" + str(sum(map(ord, h)) % 9973)).replace("xMidYMid meet", "xMidYMid slice")}<div class="cta-in"><div><h2>{h}</h2><p>{t}</p></div><a class="btn btn-primary" href="{p}contact.html">Get in touch</a></div></div></div></section>'''

def head(crumb, h, lead, flow, p=""):
    return f'<section class="page-head has-flow">{flow}<div class="wrap"><div class="crumbs rv"><a href="{p}index.html">Home</a> / {crumb}</div><h1 class="{rv(1)}">{h}</h1><p class="lead {rv(2)}">{lead}</p></div></section>'

def sh(n, tag, h, p=None):
    return f'<div class="sec-head"><div class="eyebrow {rv(0)}"><b>{n:02d}</b>{tag}</div><h2 class="{rv(1)}">{h}</h2>' + (f'<p class="{rv(2)}">{p}</p>' if p else "") + '</div>'

def tags(l): return '<ul class="tags">' + "".join(f"<li>{t}</li>" for t in l) + '</ul>'

# ---------------------------------------------------------------- projects (images come from each repository's GitHub social preview)
GHIMG = "https://opengraph.githubassets.com/1/reddygautam98/"
PROJECTS = [
 ("analytics", "Analytics", "Sales Data Analysis", "SQL analysis of product performance, the leading salesperson by region, high-performing regions and high-value first-quarter transactions.", ["SQL"], GH + "Sales-data-analysis"),
 ("analytics", "Analytics", "Loan Data Analytics", "SQL-based financial analysis covering loan interest rates, loan grades, default patterns, annual issuance, repayment behaviour and state-level risk trends.", ["SQL", "Finance"], GH + "Loan-data-analytics"),
 ("analytics", "Analytics", "Sales Forecasting Report", "Reviews sales performance, monthly profit trends and shipment-efficiency measures that are relevant to planning.", ["Reporting"], GH + "Sales-Forecasting-Report"),
 ("analytics", "Analytics", "HR Data Analysis", "Power BI workforce analysis covering employee performance, turnover, tenure and HR trends.", ["Power BI"], GH + "Hr-data-analysis"),
 ("bi", "Business intelligence", "Business Insights Report", "A structured business report for reviewing sales performance, financial indicators and selected KPIs.", ["BI", "KPIs"], GH + "Business_Insights_Report"),
 ("bi", "Business intelligence", "GameZone Business Intelligence", "A business-intelligence example for exploring performance and presenting metrics. The repository README has the exact implementation and setup.", ["BI"], GH + "gamezone-business-intelligence"),
 ("data", "Data engineering", "MetaLayer", "A data-engineering workflow organised around orchestration and structured processing layers. The README covers architecture, validation and setup.", ["Pipelines"], GH + "MetaLayer"),
 ("ai", "AI prototype", "ClinChat-style RAG App", "An experimental retrieval-augmented generation prototype. Read the README for implementation details and limits. It is not a clinically validated product.", ["RAG", "Prototype"], GH + "ClinChat-style-RAG-app"),
 ("writing", "Writing", "Daily Posts & Notes", "Knowledge-sharing notes and learning summaries on analysis and professional practice.", ["Notes"], GH + "daily_post/blob/main/read.md"),
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
    img = f'<img src="{img_src}" alt="Screenshot and preview of {html.escape(t)}" width="1200" height="600" loading="lazy" decoding="async">'
    return f'''<article class="card pcard {rv(i, base)}" data-cat="{k}" data-tilt><a class="thumb" href="{u}" target="_blank" rel="noopener noreferrer" tabindex="-1" aria-hidden="true"><span class="ph">{F.mini("m" + str(next(_n)))}<em>{html.escape(t)}</em></span>{img}</a><div class="pbody"><span class="cat">{cat}</span><h3>{t}</h3><p>{d}</p>{tags(tg)}<a class="more" href="{u}" target="_blank" rel="noopener noreferrer">{"Read notes" if k == "writing" else "View repository"} &#8599;</a></div></article>'''

# ---------------------------------------------------------------- index
def trace():
    return '''<div class="trace" aria-label="Sample requirements traceability extract">
<div class="trace-top"><b>PayTrack traceability extract</b><span>Fictional sample</span></div>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Business requirement</th><th scope="col">Functional</th><th scope="col">Stories</th><th scope="col">Tests</th></tr></thead><tbody>
<tr><td><span class="id">BR-01</span><br>Single operational view</td><td class="id">FR-002<br>FR-004</td><td class="id">US-01<br>US-03</td><td class="id">TC-001<br>TC-002</td></tr>
<tr><td><span class="id">BR-02</span><br>Identify unmatched records and the reasons</td><td class="id">FR-005<br>FR-006<br>FR-007</td><td class="id">US-03<br>US-04</td><td class="id">TC-003<br>TC-004<br>TC-005</td></tr>
<tr><td><span class="id">BR-03</span><br>Assign, comment on and resolve cases</td><td class="id">FR-008&ndash;011</td><td class="id">US-05&ndash;07</td><td class="id">TC-006&ndash;008</td></tr>
</tbody></table></div>
<div class="trace-foot">Every requirement links forward to a story and a test. All tests in this sample are marked Not Run. <a href="samples/index.html">Open the samples</a></div></div>'''

def marquee():
    def row(l, cls): 
        items = "".join(f"<li>{k}</li>" for k in l)
        return f'<div class="marq {cls}"><ul class="marq-track">{items}</ul><ul class="marq-track" aria-hidden="true">{items}</ul></div>'
    return f'<section class="marq-wrap" aria-label="Skills and keywords">{row(KW_ROW1, "")}{row(KW_ROW2, "rev")}</section>'

ICO_STOP = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>'
ICO_READY = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
ICO_CHECK = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>'
ICO_GO = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>'

METHOD_STEPS = [
    (1, "stop", "STOP", "Discover", "Workshops turn scattered requests into one problem statement with assumptions, constraints and named decision owners.", ICO_STOP, "Stop & identify root problem", 20, "+", "workshops & alignments"),
    (2, "ready", "READY", "Define", "BRD and FRD, business rules, user stories and acceptance criteria, linked to process, API and data flows.", ICO_READY, "Prepare specs, backlog & rules", 100, "%", "spec & rule baseline"),
    (3, "check", "CHECK", "Validate", "Traceability from requirement to test, UAT scenarios, expected results and defect follow-up.", ICO_CHECK, "Verify test coverage & UAT", 350, "+", "verified test cases"),
    (4, "go", "GO", "Hand over", "Decisions, risks, open questions and limitations are recorded so work continues after the workshop ends.", ICO_GO, "Sign-off & deploy", 100, "%", "UAT sign-off & launch")
]

SERVICE_STEPS = [
    (1, "stop", "STOP", "Understand", "Discuss the problem, users, data or systems, constraints, deadlines and what success looks like.", ICO_STOP, "Stop assumptions & understand goals", 1, "st", "alignment workshop"),
    (2, "ready", "READY", "Scope", "Agree deliverables, assumptions, dependencies, review points, responsibilities and a practical timeline.", ICO_READY, "Ready deliverables & timeline", 100, "%", "scope agreement"),
    (3, "check", "CHECK", "Deliver", "Share drafts, analysis or requirements in checkpoints; collect feedback and resolve agreed changes.", ICO_CHECK, "Review drafts & verify feedback", 100, "%", "review checkpoints"),
    (4, "go", "GO", "Validate and hand over", "Review against acceptance criteria and provide the agreed documents, findings or handover notes.", ICO_GO, "Sign-off & project handover", 100, "%", "deliverable sign-off")
]

def make_steps(items):
    out = []
    total = len(items)
    for i, (num, status, status_label, title, desc, icon_svg, meaning, stat_val, stat_suf, stat_lbl) in enumerate(items):
        dots = f'''<div class="traffic-housing" aria-hidden="true"><span class="t-dot red{' active' if status == 'stop' else ''}"></span><span class="t-dot orange{' active' if status == 'ready' else ''}"></span><span class="t-dot yellow{' active' if status == 'check' else ''}"></span><span class="t-dot green{' active' if status == 'go' else ''}"></span></div>'''
        pct = num * 25
        arrow_html = ""
        if i < total - 1:
            arrow_html = f'''<div class="step-arrow-link step-arrow-{num}" aria-hidden="true" title="Proceed to Step {num + 1}">
<div class="step-arrow-stem"></div>
<div class="step-arrow-badge">
<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
</div>
</div>'''
        out.append(f'''<li class="step-card step-{num} step-{status} {rv(i)}" data-tilt>
<div class="step-top">
<div class="step-badge" aria-label="Step {num}: {status_label}">
<span class="step-num">{num}</span>
<span class="step-ico">{icon_svg}</span>
</div>
<div class="traffic-widget" title="Traffic status: {status_label} &mdash; {meaning}">
{dots}
<span class="t-status t-{status}">{status_label}</span>
</div>
</div>
<div class="step-head-row">
<h3>{title}</h3>
<div class="step-counter step-counter-{status}" title="Process progress: {pct}% complete">
<span class="step-counter-val" data-count="{pct}" data-suf="%">{pct}%</span>
<span class="step-counter-tag">Phase {num}/4</span>
</div>
</div>
<div class="step-bar step-bar-{status}" role="progressbar" aria-valuenow="{pct}" aria-valuemin="0" aria-valuemax="100" aria-label="{status_label}: {pct}% complete"><span class="bar-fill"></span></div>
<p>{desc}</p>
<div class="step-metric-foot">
<span class="step-metric-chip"><b data-count="{stat_val}" data-suf="{stat_suf}">{stat_val}{stat_suf}</b> <span>{stat_lbl}</span></span>
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
    ("Backlog Refinement", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'),
    ("Sprint Planning", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'),
    ("Change Management", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m18 15-6-6-6 6"/></svg>'),
    ("Functional, Regression & Integration Testing", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>'),
    ("UAT Coordination", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'),
    ("Defect Triage", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>')
]

TECH_WORKFLOW = [
    ("Figma", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"/><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"/><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"/><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"/></svg>'),
    ("JIRA", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="18" rx="1"/><rect x="14" y="3" width="7" height="10" rx="1"/></svg>'),
    ("Confluence", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'),
    ("REST API Requirements", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'),
    ("API Contract Review", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="m9 15 2 2 4-4"/></svg>'),
    ("Postman", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="m10 15 5-3-5-3v6z"/></svg>'),
    ("System Integration Requirements", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="2" width="8" height="8" rx="1"/><rect x="14" y="14" width="8" height="8" rx="1"/><path d="M6 10v4a2 2 0 0 0 2 2h6"/></svg>'),
    ("SQL", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'),
    ("Excel", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="m9 9 6 6M15 9l-6 6"/></svg>'),
    ("Python (Pandas)", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2a4 4 0 0 0-4 4v2h8V6a4 4 0 0 0-4-4z"/><path d="M12 22a4 4 0 0 0 4-4v-2H8v2a4 4 0 0 0 4 4z"/></svg>'),
    ("Power BI", '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="13" width="3" height="8"/><rect x="10" y="8" width="3" height="13"/><rect x="16" y="3" width="3" height="18"/></svg>')
]

def workflow_tags(items):
    out = []
    total = len(items)
    for idx, (label, ico) in enumerate(items):
        arrow = f'<span class="wf-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>' if idx < total - 1 else ''
        out.append(f'<span class="wf-item"><span class="wf-step"><span class="wf-num">{idx+1:02d}</span><span class="wf-ico" aria-hidden="true">{ico}</span><span class="wf-lbl">{label}</span></span>{arrow}</span>')
    return '<div class="wf-flow">' + "".join(out) + '</div>'

def paytrack_wireframe_svg():
    return '''<div class="feat-wireframe-wrap" aria-hidden="true"><svg class="feat-wireframe-svg" viewBox="0 0 1140 520" preserveAspectRatio="xMidYMid slice" focusable="false">
<defs>
  <marker id="wf-arr-pt" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M1,1 L9,5 L1,9 z" fill="currentColor" opacity="0.6"/>
  </marker>
  <filter id="wf-glow-pt" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect class="wf-border" x="14" y="14" width="1112" height="492" rx="14"/>
<line class="wf-div" x1="14" y1="48" x2="1126" y2="48"/>
<circle cx="34" cy="31" r="3.5" class="wf-dot-red"/>
<circle cx="46" cy="31" r="3.5" class="wf-dot-amber"/>
<circle cx="58" cy="31" r="3.5" class="wf-dot-green"/>
<rect x="80" y="23" width="230" height="16" rx="4" class="wf-addr-bg"/>
<text x="92" y="35" class="wf-addr-txt">paytrack.internal/reconciliation/v2.4</text>
<rect x="26" y="62" width="130" height="430" rx="8" class="wf-panel"/>
<rect x="36" y="78" width="110" height="20" rx="5" class="wf-nav-active"/>
<text x="46" y="92" class="wf-nav-txt-act">Portal Overview</text>
<rect x="36" y="108" width="90" height="14" rx="4" class="wf-nav-item"/>
<text x="46" y="119" class="wf-nav-txt">API Ingestion</text>
<rect x="36" y="132" width="100" height="14" rx="4" class="wf-nav-item"/>
<text x="46" y="143" class="wf-nav-txt">Rules &amp; Matching</text>
<rect x="36" y="156" width="95" height="14" rx="4" class="wf-nav-item"/>
<text x="46" y="167" class="wf-nav-txt">Exception Queue</text>
<rect x="36" y="180" width="85" height="14" rx="4" class="wf-nav-item"/>
<text x="46" y="191" class="wf-nav-txt">Audit &amp; Sign-off</text>
<g transform="translate(36, 440)">
  <rect width="110" height="36" rx="6" class="wf-status-box"/>
  <circle cx="14" cy="18" r="4" class="wf-pulse-dot"/>
  <text x="26" y="21" class="wf-status-txt">Engine: Live (99.9%)</text>
</g>
<g transform="translate(172, 62)">
  <rect x="0" y="0" width="150" height="52" rx="8" class="wf-kpi-card"/>
  <text x="12" y="20" class="wf-kpi-lbl">INGESTED FEED</text>
  <text x="12" y="40" class="wf-kpi-val">100K+ Tx</text>
  <rect x="164" y="0" width="150" height="52" rx="8" class="wf-kpi-card"/>
  <text x="176" y="20" class="wf-kpi-lbl">MATCH RATE</text>
  <text x="176" y="40" class="wf-kpi-val wf-val-green">94.2% Passed</text>
  <rect x="328" y="0" width="150" height="52" rx="8" class="wf-kpi-card"/>
  <text x="340" y="20" class="wf-kpi-lbl">EXCEPTION QUEUE</text>
  <text x="340" y="40" class="wf-kpi-val wf-val-orange">3 SLA Breaches</text>
  <rect x="492" y="0" width="150" height="52" rx="8" class="wf-kpi-card"/>
  <text x="504" y="20" class="wf-kpi-lbl">RECON STATUS</text>
  <text x="504" y="40" class="wf-kpi-val wf-val-blue">Audited &amp; RTM</text>
</g>
<g transform="translate(172, 126)">
  <rect width="642" height="340" rx="8" class="wf-tbl-box"/>
  <rect width="642" height="28" rx="6" class="wf-tbl-head"/>
  <text x="16" y="18" class="wf-th">TX_ID</text>
  <text x="130" y="18" class="wf-th">GATEWAY</text>
  <text x="250" y="18" class="wf-th">RULE_MATCH</text>
  <text x="380" y="18" class="wf-th">AMOUNT</text>
  <text x="490" y="18" class="wf-th">FLOW_STATUS</text>
  <line x1="0" y1="62" x2="642" y2="62" class="wf-row-div"/>
  <text x="16" y="50" class="wf-td-id">TX-892110</text>
  <text x="130" y="50" class="wf-td">Stripe / Razorpay</text>
  <text x="250" y="50" class="wf-td">Rule-01 Direct</text>
  <text x="380" y="50" class="wf-td">$14,250.00</text>
  <rect x="490" y="38" width="70" height="16" rx="4" class="wf-badge-ok"/>
  <text x="500" y="50" class="wf-badge-txt-ok">MATCHED</text>
  <line x1="0" y1="98" x2="642" y2="98" class="wf-row-div"/>
  <text x="16" y="86" class="wf-td-id">TX-892111</text>
  <text x="130" y="86" class="wf-td">PayU / Adyen</text>
  <text x="250" y="86" class="wf-td">Rule-04 Settlement</text>
  <text x="380" y="86" class="wf-td">$3,840.50</text>
  <rect x="490" y="74" width="70" height="16" rx="4" class="wf-badge-ok"/>
  <text x="500" y="86" class="wf-badge-txt-ok">MATCHED</text>
  <line x1="0" y1="134" x2="642" y2="134" class="wf-row-div"/>
  <text x="16" y="122" class="wf-td-id">TX-892112</text>
  <text x="130" y="122" class="wf-td">Gateway Feed</text>
  <text x="250" y="122" class="wf-td">T+1 Time Drift</text>
  <text x="380" y="122" class="wf-td">$8,910.00</text>
  <rect x="490" y="110" width="82" height="16" rx="4" class="wf-badge-warn"/>
  <text x="496" y="122" class="wf-badge-txt-warn">EXCEPTION</text>
  <line x1="0" y1="170" x2="642" y2="170" class="wf-row-div"/>
  <text x="16" y="158" class="wf-td-id">TX-892113</text>
  <text x="130" y="158" class="wf-td">Swift / ISO20022</text>
  <text x="250" y="158" class="wf-td">Rule-02 Auto</text>
  <text x="380" y="158" class="wf-td">$45,120.00</text>
  <rect x="490" y="146" width="70" height="16" rx="4" class="wf-badge-ok"/>
  <text x="500" y="158" class="wf-badge-txt-ok">MATCHED</text>
</g>
<path id="wf-path-1" class="wf-flow-line" d="M 156,115 L 172,115 L 240,115 L 240,175 L 340,175 L 420,175" marker-end="url(#wf-arr-pt)"/>
<path id="wf-path-2" class="wf-flow-line wf-flow-green" d="M 662,175 L 750,175 L 820,175 L 820,280 L 890,280 L 1020,280" marker-end="url(#wf-arr-pt)"/>
<path id="wf-path-3" class="wf-flow-line wf-flow-orange" d="M 662,248 L 730,248 L 730,340 L 840,340 L 920,340 L 980,340" marker-end="url(#wf-arr-pt)"/>
<path id="wf-path-4" class="wf-flow-line wf-flow-blue" d="M 980,360 L 980,430 L 760,430 L 520,430 L 320,430" marker-end="url(#wf-arr-pt)"/>
<circle class="wf-flow-pkt wf-pkt-blue" r="5" filter="url(#wf-glow-pt)">
  <animateMotion dur="4.2s" repeatCount="indefinite" path="M 156,115 L 172,115 L 240,115 L 240,175 L 340,175 L 420,175"/>
</circle>
<circle class="wf-flow-pkt wf-pkt-green" r="5" filter="url(#wf-glow-pt)">
  <animateMotion dur="5.5s" repeatCount="indefinite" path="M 662,175 L 750,175 L 820,175 L 820,280 L 890,280 L 1020,280"/>
</circle>
<circle class="wf-flow-pkt wf-pkt-orange" r="5" filter="url(#wf-glow-pt)">
  <animateMotion dur="4.8s" repeatCount="indefinite" path="M 662,248 L 730,248 L 730,340 L 840,340 L 920,340 L 980,340"/>
</circle>
<circle class="wf-flow-pkt wf-pkt-cyan" r="4.5" filter="url(#wf-glow-pt)">
  <animateMotion dur="6.2s" repeatCount="indefinite" path="M 980,360 L 980,430 L 760,430 L 520,430 L 320,430"/>
</circle>
<g transform="translate(156, 115)">
  <circle r="4" fill="#2563eb"/>
  <circle r="9" fill="none" stroke="#2563eb" stroke-width="1.2" class="wf-ping-ring"/>
</g>
<g transform="translate(662, 175)">
  <circle r="4" fill="#16a34a"/>
  <circle r="9" fill="none" stroke="#16a34a" stroke-width="1.2" class="wf-ping-ring"/>
</g>
<g transform="translate(662, 248)">
  <circle r="4" fill="#ea580c"/>
  <circle r="9" fill="none" stroke="#ea580c" stroke-width="1.2" class="wf-ping-ring"/>
</g>
<g transform="translate(1020, 280)">
  <circle r="4" fill="#22c55e"/>
  <circle r="9" fill="none" stroke="#22c55e" stroke-width="1.2" class="wf-ping-ring"/>
</g>
</svg></div>'''



def index():
    feats = "".join(pcard(c, i, 0.0) for i, c in enumerate([PROJECTS[0], PROJECTS[1], PROJECTS[2], PROJECTS[6]]))
    rot = "".join(f'<span>{r}</span>' for r in ROLES_ROT)
    toolkit_cards = [
        ("Business Analysis", "Chronological Lifecycle: Elicitation &#10142; Analysis &#10142; Specs &#10142; Agile &#10142; Sign-off", BA_WORKFLOW),
        ("Process Analysis & Documentation", "Process Stream: AS-IS Discovery &#10142; Root Cause &#10142; BPMN Modelling &#10142; Specs", PROCESS_WORKFLOW),
        ("Agile, Testing & Delivery", "Delivery Sprint: SDLC &#10142; Planning &#10142; Testing &#10142; UAT &amp; Release", AGILE_WORKFLOW),
        ("Technical Skills & Tools", "Toolchain: Design &#10142; APIs &amp; Contracts &#10142; Analysis &amp; BI", TECH_WORKFLOW)
    ]
    tk = "".join(f'<div class="card kit {rv(i)}" data-tilt><div class="kit-head"><h3>{g}</h3><span class="kit-sub">{sub}</span></div>{workflow_tags(wf)}</div>' for i, (g, sub, wf) in enumerate(toolkit_cards))
    return f'''
<section class="hero has-flow">{F.lifecycle("h")}<div class="wrap hero-grid">
<div>
<div class="status rv"><i></i><span>Available for global remote, hybrid &amp; full-time roles</span></div>
<h1 class="{rv(1)}">Business Analyst who turns requirements into <span class="grad">testable specs.</span></h1>
<p class="rot-line {rv(2)}"><span class="rot-lb">Right now:</span><span class="rot" data-rot aria-live="off">{rot}</span></p>
<p class="lead {rv(3)}">4+ years of experience in requirements analysis and delivery: translating business needs into clear, testable functional and non-functional requirements, user stories, and BDD acceptance criteria backed by SQL and Python analysis.</p>
<div class="actions {rv(4)}"><a class="btn btn-primary" href="projects.html">See my work</a><a class="btn btn-ghost" href="contact.html">Contact me</a></div>
<p class="roles-line {rv(5)}">Also searched as: Functional Analyst, Business Systems Analyst, Data and BI Analyst.</p>
</div>
<div class="scene {rv(2)}" data-scene><div class="stage">
<a href="samples/index.html#brd" class="plane" style="--i:3" title="View BRD sample document"><b>BRD</b></a><a href="samples/index.html#frd" class="plane" style="--i:2" title="View FRD sample document"><b>FRD</b></a><a href="samples/index.html#user-stories" class="plane" style="--i:1" title="View User Stories sample document"><b>Stories</b></a>
{trace()}
<a href="samples/index.html#user-stories" class="f3d" style="--z:110px;top:-22px;left:-26px;--dl:0s" title="View User Stories sample document">User stories</a>
<a href="samples/index.html#uat" class="f3d" style="--z:140px;top:38%;right:-30px;--dl:.8s" title="View UAT &amp; test cases sample document">UAT</a>
<a href="samples/index.html#sql" class="f3d" style="--z:90px;bottom:-24px;left:12%;--dl:1.4s" title="View SQL queries &amp; data model sample">SQL</a>
<a href="samples/index.html#rest-api" class="f3d alt" style="--z:120px;top:-18px;right:18%;--dl:.4s" title="View REST API sequence diagram &amp; specifications">REST API</a>
<a href="samples/index.html#power-bi" class="f3d alt" style="--z:100px;bottom:-30px;right:12%;--dl:1.9s" title="View Power BI reporting sample &amp; dashboard">Power BI</a>
</div></div>
</div></section>

{marquee()}

<section class="sec" id="proof"><div class="wrap">
{sh(1, "Proof", "Results from past delivery work")}
<div class="proof">
<div class="proof-card proof-card-1 {rv(0)}"><b data-count="100" data-suf="K+">100K+</b><div class="card-bar bar-stream" role="progressbar" aria-valuenow="94" aria-valuemin="0" aria-valuemax="100" aria-label="100K+ records analysed"><span class="bar-fill"></span></div><span>transaction records analysed with SQL and Python, surfacing 3 recurring SLA-breach patterns</span></div>
<div class="proof-card proof-card-2 {rv(1)}"><b data-count="350" data-suf="+">350+</b><div class="card-bar bar-segmented" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" aria-label="350+ test cases verified"><span class="bar-seg"></span><span class="bar-seg"></span><span class="bar-seg"></span><span class="bar-seg"></span></div><span>test cases coordinated, with zero critical defects reported</span></div>
<div class="proof-card proof-card-3 {rv(2)}"><b data-count="20" data-suf="+">20+</b><div class="card-bar bar-milestone" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" aria-label="20+ workshops aligned"><span class="bar-fill"></span></div><span>workshops that aligned 13+ stakeholders on requirements</span></div>
<div class="proof-card proof-card-4 {rv(3)}"><b data-count="2" data-suf="">2</b><div class="card-bar bar-dual" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" aria-label="2 payment-gateway integrations documented"><span class="bar-pip"></span><span class="bar-pip"></span></div><span>payment-gateway integrations documented for Engineering and QA</span></div>
</div>
<p class="note">Figures come from my resume and describe past roles and projects. They are not a guarantee of future outcomes.</p>
</div></section>

<section class="sec band has-flow" id="method">{F.swim("m")}<div class="wrap">
{sh(2, "Method", "How a requirement travels from idea to sign-off", "The same path the sample documents follow.")}
<ol class="steps">{make_steps(METHOD_STEPS)}</ol></div></section>

<section class="sec has-flow" id="work">{F.erd("w")}<div class="wrap">
{sh(3, "Selected work", "Case study and projects", "A fictional end-to-end BA case study, plus personal analytics and data projects. Each card opens its repository.")}
<div class="feature {rv(0)}">
{paytrack_wireframe_svg()}
<div><span class="cat">Case study</span><h3>PayTrack: payment reconciliation, from BRD to UAT</h3><p class="muted">A documented requirements pack for a payment reconciliation and exception-management portal: business and functional requirements, Given/When/Then stories, traceability, UAT plan, process and data diagrams.</p>
<div class="disclaimer"><b>Fictional sample.</b> No client data is used and no executed-test evidence is claimed.</div>
<div class="actions"><a class="btn btn-primary" href="samples/index.html">Browse the artifacts</a></div></div>
<div class="feat-side"><a class="feat-img" href="samples/diagrams/Payment_Reconciliation_Process.svg" aria-label="Open the reconciliation process flow"><img src="samples/diagrams/Payment_Reconciliation_Process.png" alt="Payment reconciliation process flow diagram from the PayTrack sample" width="1120" height="635" loading="lazy"></a>
<ul><li><a href="samples/docs/01_BRD_PayTrack_Sample.pdf"><span class="feat-doc-name"><svg class="feat-doc-ico" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>Business requirements document</span> <span>PDF</span></a></li><li><a href="samples/docs/03_User_Stories_Acceptance_Criteria_Sample.pdf"><span class="feat-doc-name"><svg class="feat-doc-ico" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>User stories and acceptance criteria</span> <span>PDF</span></a></li><li><a href="samples/docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf"><span class="feat-doc-name"><svg class="feat-doc-ico" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>RTM, test cases and UAT plan</span> <span>PDF</span></a></li></ul></div>
</div>
<div class="grid g2">{feats}</div>
<div class="actions"><a class="btn btn-ghost" href="projects.html">All 9 projects</a></div>
</div></section>

<section class="sec band has-flow" id="toolkit">{F.pipeline("t")}<div class="wrap">
{sh(4, "Toolkit", "Skills hiring teams search for", "Analysis, documentation and delivery tools I use day to day, grouped by what they are used for.")}
<div class="grid g2">{tk}</div>
</div></section>

<section class="sec has-flow" id="experience">{F.seq("x")}<div class="wrap">
{sh(5, "Experience", "Where I have delivered")}
<div class="roles">
<div class="role {rv(0)}"><div class="node">01</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">Marolix Technology Solutions Pvt Ltd, Hyderabad</div><ul><li>Defined REST API requirements, UML flows and data mappings for 2 payment-gateway integrations.</li><li>Analysed 100,000+ transaction records using SQL and Python to identify 3 recurring SLA-breach patterns.</li><li>Coordinated UAT across 350+ test cases in Jira; managed 12+ change requests over 2 Agile releases with zero critical defects at launch.</li></ul></div></div>
<div class="role {rv(1)}"><div class="node">02</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">V Moksha Technologies Pvt Ltd, Bengaluru</div><ul><li>Resolved recurring operational bottlenecks and SLA shortfalls using SQL data extraction, fishbone diagrams, and 5-Why root cause analysis.</li><li>Mapped AS-IS and TO-BE business processes (BPMN / swimlane), saving an estimated 2 weeks per improvement cycle.</li></ul></div></div>
<div class="role {rv(2)}"><div class="node">03</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru</div><ul><li>Facilitated Three Amigos sessions, delivering functional specifications and BDD user stories for 3 concurrent modules across 4 business units.</li><li>Coordinated UAT, smoke and regression testing across 50+ Jira test cases with zero post-launch incidents.</li><li>Reviewed API contracts against business rules and maintained the RTM and RACI matrix.</li></ul></div></div>
<div class="role {rv(3)}"><div class="node">04</div><div class="rbody" data-tilt><h3>Associate Software Engineer</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru</div><ul><li>Promoted to Business Analyst in 17 months (6 months ahead of schedule) after managing requirements for 3 reporting features.</li><li>Gathered reporting requirements from 15+ Finance and Operations stakeholders; built Power BI dashboards and automated manual reports saving 3+ hrs/week.</li></ul></div></div>
</div>
<div class="actions"><a class="btn btn-ghost" href="resume.html">Full resume</a></div>
</div></section>
''' + cta()

# ---------------------------------------------------------------- about
def about():
    return head("About", "Requirements teams can build and validate.", "I connect stakeholder needs, requirements, data, systems and delivery teams, so ambiguous business problems become clear, testable work.", F.seq("a")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap two">
<div><h2 class="{rv(0)}">Who I am</h2>
<p class="{rv(1)}" style="margin-top:18px">I&rsquo;m Gautam Reddy, a Business Analyst with 4+ years of experience in requirements analysis and delivery, translating business needs into clear, testable functional and non-functional requirements.</p>
<p class="{rv(2)}">Experienced in stakeholder workshops, requirements validation and sign-off, REST API requirements, system workflows, data mapping, user stories, BDD acceptance criteria, SQL/Python analysis, requirements traceability, UAT, and collaboration with Engineering, QA, Product, and business stakeholders.</p>
<div class="actions {rv(4)}"><a class="btn btn-primary" href="resume.html">View resume</a><a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">Connect on LinkedIn</a></div></div>
<div class="{rv(2)}" data-tilt style="align-self:start"><dl class="facts card"><dt>Role</dt><dd>Business Analyst, 4+ years</dd><dt>Focus</dt><dd>Requirements Gathering, API &amp; System Integration, SQL, Agile, UAT</dd><dt>Technical Tools</dt><dd>SQL, Python (Pandas), Excel, Power BI, JIRA, Confluence, Figma, Postman</dd><dt>Based in</dt><dd>Bengaluru, India</dd><dt>Elsewhere</dt><dd>{ext(GH, "GitHub")}, {ext(LI, "LinkedIn")}, {ext(HR, "HackerRank")}</dd></dl></div>
</div></section>

<section class="sec band has-flow">{F.pipeline("ab")}<div class="wrap">
{sh(1, "Principles", "Working principles", "The habits behind the documents.")}
<div class="grid g3">
<div class="card {rv(0)}" data-tilt><h3>Evidence before opinion</h3><p>Findings, assumptions and limitations are kept separate, so guesses are never presented as facts.</p></div>
<div class="card {rv(1)}" data-tilt><h3>Scope you can point at</h3><p>Agreed deliverables and acceptance criteria define what &ldquo;done&rdquo; means before work begins.</p></div>
<div class="card {rv(2)}" data-tilt><h3>Traceable by design</h3><p>Requirements connect to stories, tests and decisions, so any change shows its impact.</p></div>
</div></div></section>

<section class="sec has-flow">{F.swim("ab2")}<div class="wrap">
{sh(2, "Career path", "Career path")}
<div class="roles">
<div class="role {rv(0)}"><div class="node">01</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">Marolix Technology Solutions Pvt Ltd, Hyderabad</div><p class="muted">REST API requirements, UML flows and data mappings for 2 payment-gateway integrations; 100,000+ transaction records analysed using SQL and Python; 20+ workshops with 13+ stakeholders; 350+ test cases coordinated in Jira with zero critical defects.</p></div></div>
<div class="role {rv(1)}"><div class="node">02</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">V Moksha Technologies Pvt Ltd, Bengaluru</div><p class="muted">Fishbone and 5-Why root cause analysis with SQL data extraction; AS-IS / TO-BE process mapping eliminating redundant handover steps and saving an estimated 2 weeks per improvement cycle.</p></div></div>
<div class="role {rv(2)}"><div class="node">03</div><div class="rbody" data-tilt><h3>Business Analyst</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru</div><p class="muted">Three Amigos facilitation, functional specs and BDD acceptance criteria for 3 modules across 4 business units; API contract review, RTM, and UAT across 50+ test cases with zero post-launch incidents.</p></div></div>
<div class="role {rv(3)}"><div class="node">04</div><div class="rbody" data-tilt><h3>Associate Software Engineer</h3><div class="org">Iinfocomm IT Services Pvt Ltd, Bengaluru</div><p class="muted">Promoted to BA in 17 months; gathered reporting requirements from 15+ Finance and Operations stakeholders, built Power BI dashboards and secured business case for reporting automation saving 3+ hrs/week.</p></div></div>
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
    sc = "".join(f'<div class="card {rv(i)}" data-tilt><span class="num">0{i + 1}</span><h3>{t}</h3><p>{d}</p>{tags(tg)}<a class="more" href="contact.html">Ask about this</a></div>' for i, (t, d, tg) in enumerate(SERV))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return head("Services", "Useful deliverables. Clear scope.", "Business analysis, data and technology support shaped around the problem, the people who need the answer and the output your team can use.", F.pipeline("sv")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap">
{sh(1, "Services", "What I can help with", "Every engagement starts by aligning the question, deliverables, assumptions and review points.")}
<div class="grid g3">{sc}</div></div></section>

<section class="sec band has-flow">{F.swim("sv2")}<div class="wrap">
{sh(2, "Process", "How an engagement runs", "Small checkpoints keep scope, feedback and ownership visible.")}
<ol class="steps">{make_steps(SERVICE_STEPS)}</ol></div></section>

<section class="sec"><div class="wrap">
{sh(3, "Deliverables", "What you receive", "Deliverables follow the agreed scope. Not every engagement includes every item.")}
<div class="grid g3">
<div class="card {rv(0)}" data-tilt><h3>Requirements and process</h3><p>BRD / FRD or functional requirements, user stories and acceptance criteria, AS-IS / TO-BE maps, business rules, RTM and impact notes.</p></div>
<div class="card {rv(1)}" data-tilt><h3>Analysis and insight</h3><p>SQL and Python analysis, metric definitions and reporting requirements, dashboard specifications, findings with stated assumptions and limits.</p></div>
<div class="card {rv(2)}" data-tilt><h3>Testing and integration</h3><p>API field mappings and system flows, UAT scenarios with traceability, defect triage support, release notes and knowledge handover.</p></div>
</div></div></section>

<section class="sec band"><div class="wrap two">
<div><h2 class="rv">Questions before starting</h2></div>
<div class="rv" style="--d:.1s">{faq}</div>
</div></section>
''' + cta(h="Not sure which service fits?", t="Describe the problem and the outcome you want. We can clarify the scope before deciding on next steps.")

# ---------------------------------------------------------------- projects
def projects():
    chips = '<button class="chip" type="button" data-f="all" aria-pressed="true">All</button>' + "".join(f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{n}</button>' for k, n in [("analytics", "Analytics"), ("bi", "Business intelligence"), ("data", "Data engineering"), ("ai", "AI prototype"), ("writing", "Writing")])
    cards = "".join(pcard(c, i % 3, 0.0) for i, c in enumerate(PROJECTS))
    return head("Projects", "Practical analysis, visible work.", "Repositories across analytics, business intelligence, data engineering, AI prototypes and writing. Every card links to its source so you can review the implementation.", F.erd("pj")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap">
<div class="feature rv">
<div><span class="cat">Featured case study</span><h3>PayTrack: payment reconciliation, from BRD to UAT</h3><p class="muted">Shows how a payments requirement is documented, mapped, tested and handed over.</p>
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

# ---------------------------------------------------------------- resume (web view only; no download)
def resume():
    def role(n, t, o, b, i): return f'<div class="role {rv(i)}"><div class="node">{n:02d}</div><div class="rbody" data-tilt><h3>{t}</h3><div class="org">{o}</div><ul>' + "".join(f"<li>{x}</li>" for x in b) + '</ul></div></div>'
    roles = role(1, "Business Analyst", "Marolix Technology Solutions Pvt Ltd, Hyderabad, India", [
"Defined REST API requirements, UML system flows, and data mappings for 2 payment gateway integrations, providing implementation-ready documentation for Engineering and QA.",
"Analyzed 100,000+ transaction records using SQL and Python, identified 3 recurring SLA breach patterns, and shared findings to inform process-improvement actions.",
"Elicited and validated requirements through 20+ workshops with 13+ stakeholders; documented BRDs/FRDs, functional and non-functional requirements, use cases, and BDD acceptance criteria.",
"Prioritized requirements across 4 modules using MoSCoW and challenged 3 feature requests with insufficient business justification to keep backlog decisions focused on business value.",
"Coordinated UAT and functional, regression, and integration testing across 350+ test cases; supported JIRA defect triage with QA and Engineering, with zero critical defects reported.",
"Managed 12+ change requests across 2 Agile releases, assessed requirement impacts, and maintained traceability through delivery.",
"Maintained business rules, data dictionaries, and field mappings in Confluence and Excel; reviewed Figma wireframes and prepared stakeholder reports."], 0)
    roles += role(2, "Business Analyst", "V Moksha Technologies Pvt Ltd, Bengaluru, India", [
"Resolved recurring SLA shortfalls and reduced error recurrence and rework, saving 2 weeks per improvement cycle through SQL analysis, fishbone/5-Why root-cause analysis, and AS-IS/TO-BE process mapping."], 0)
    roles += role(3, "Business Analyst", "Iinfocomm IT Services Pvt Ltd, Bengaluru, India", [
"Facilitated Three Amigos sessions and translated stakeholder needs into functional requirements and BDD acceptance criteria for 3 concurrent modules delivered on time.",
"Documented functional requirements, business rules, and control requirements across 4 business units.",
"Coordinated UAT, smoke, sanity, and regression testing across 50+ JIRA-tracked test cases; the delivered modules had no reported post-launch incidents.",
"Reviewed API contracts against functional requirements and maintained the Requirements Traceability Matrix (RTM) and RACI to connect requirements, delivery, and acceptance."], 0)
    roles += role(4, "Associate Software Engineer", "Iinfocomm IT Services Pvt Ltd, Bengaluru, India", [
"Promoted to Business Analyst within 17 months, six months ahead of the expected timeline, after managing requirements for 3 reporting features from elicitation through stakeholder acceptance.",
"Translated input from 15+ Finance and Operations stakeholders into Power BI requirements and BDD user stories, coordinating with Engineering and business leads.",
"Built a business case for reporting automation projecting 3+ hours of weekly manual-effort savings and secured executive approval."], 0)
    return head("Resume", "Experience, skills, delivery.", "Business Analyst focused on requirements, API and system integration, SQL and Python analysis, Agile delivery and UAT coordination.", F.swim("rs")) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap">
<div class="actions rv" style="margin:0 0 40px"><a class="btn btn-ghost" href="{LI}" target="_blank" rel="noopener noreferrer">View LinkedIn profile</a><a class="btn btn-ghost" href="{HR}" target="_blank" rel="noopener noreferrer">HackerRank profile</a><a class="btn btn-ghost" href="contact.html">Contact me</a></div>
<div class="proof"><div class="rv proof-card proof-card-1"><b data-count="100" data-suf="K+">100K+</b><div class="card-bar bar-stream" role="progressbar" aria-valuenow="94" aria-valuemin="0" aria-valuemax="100" aria-label="100K+ transactions analysed"><span class="bar-fill"></span></div><span>transactions analysed</span></div><div class="rv proof-card proof-card-2" style="--d:.07s"><b data-count="350" data-suf="+">350+</b><div class="card-bar bar-segmented" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" aria-label="350+ test cases coordinated"><span class="bar-seg"></span><span class="bar-seg"></span><span class="bar-seg"></span><span class="bar-seg"></span></div><span>test cases coordinated</span></div><div class="rv proof-card proof-card-3" style="--d:.14s"><b data-count="20" data-suf="+">20+</b><div class="card-bar bar-milestone" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" aria-label="20+ workshops, 13+ stakeholders"><span class="bar-fill"></span></div><span>workshops, 13+ stakeholders</span></div><div class="rv proof-card proof-card-4" style="--d:.21s"><b data-count="12" data-suf="+">12+</b><div class="card-bar bar-dual" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" aria-label="12+ change requests, 2 releases"><span class="bar-pip"></span><span class="bar-pip"></span></div><span>change requests, 2 Agile releases</span></div></div>
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
    return head("Contact", "Tell me what you&rsquo;re trying to solve.", "For a role, mention the position and team. For a collaboration, describe the problem and the outcome. I reply with context.", F.seq("ct")) + f'''
<section class="sec" style="padding-top:24px"><div class="wrap two" style="align-items:start">
<div class="rv"><h2>Reach me directly</h2>
<ul class="contact-list" style="margin-top:24px"><li><span>{ICO_MAIL}Email</span><div><a href="mailto:{EMAIL}">{EMAIL}</a> <button class="chip copy" type="button" data-copy="{EMAIL}">Copy</button></div></li><li><span>{ICO_LI}LinkedIn</span><div>{ext(LI, "gautam-reddy-analyst")}</div></li><li><span>{ICO_GH}GitHub</span><div>{ext(GH, "reddygautam98")}</div></li><li><span>{ICO_HR}HackerRank</span><div>{ext(HR, "reddygautam98")}</div></li><li><span>{ICO_LOC}Location</span><div>Bengaluru, India</div></li></ul>
<h3 style="margin:32px 0 10px">Useful details to include</h3>
<ul class="muted" style="padding-left:1.1em;margin:0"><li>The problem and who it affects</li><li>The output you need and how it will be used</li><li>Relevant tools, systems, data types and deadlines</li><li>Any constraints or acceptance criteria</li></ul>
<p class="disclaimer"><b>Please don&rsquo;t include</b> passwords, confidential source files, regulated records or sensitive customer data in a first message.</p></div>
<div class="form-card rv" style="--d:.1s"><h2 style="font-size:1.6rem">Project enquiry</h2><p class="muted small" style="margin:8px 0 22px">This site stores nothing. The button opens a draft in your email app and nothing is sent until you press Send.</p>
<form id="enquiry">
<div class="row2"><label>Your name *<input name="name" autocomplete="name" required><span class="err"></span></label><label>Work email *<input name="email" type="email" autocomplete="email" required><span class="err"></span></label></div>
<label>Company (optional)<input name="company" autocomplete="organization"></label>
<label>What do you need help with? *<select name="service" required><option value="">Choose a service</option>{opts(["Business analysis and requirements", "Data analysis and BI reporting", "SQL, data quality and reporting", "API and integration analysis", "UAT, testing and release support", "A role at my company", "Not sure yet"])}</select><span class="err"></span></label>
<div class="row2"><label>Engagement type<select name="type">{opts(["Not sure yet", "Discovery or review", "Defined deliverable", "Ongoing support", "Prototype or feasibility", "Full-time role"])}</select></label><label>Target timeline<select name="timeline">{opts(["Flexible", "As soon as practical", "Within 2 to 4 weeks", "Within 1 to 3 months", "Specific deadline"])}</select></label></div>
<label>Describe the problem and the outcome you want *<textarea name="msg" required></textarea><span class="err"></span></label>
<label>Reference link (optional)<input name="ref" type="url"></label>
<div><button class="btn btn-primary" type="submit">Prepare email draft</button></div>
<p id="sent" class="muted small" hidden role="status">Your email app should now show a draft. If nothing opened, write to {EMAIL}.</p>
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
ICO_DATA_STORIES = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1.5"/><circle cx="4" cy="12" r="1.5"/><circle cx="4" cy="18" r="1.5"/></svg>'
ICO_DATA_SQL = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'

def flink(href, text, ico_type="", download=False, target_blank=True):
    ico_svg = ""
    cls_extra = ""
    if ico_type == "pdf":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
        cls_extra = " link-pdf"
    elif ico_type == "word":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>'
        cls_extra = " link-word"
    elif ico_type == "gh":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
        cls_extra = " link-gh"
    elif ico_type == "csv":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
        cls_extra = " link-csv"
    elif ico_type == "sql":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'
        cls_extra = " link-sql"
    elif ico_type == "figma":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z"/><path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z"/><path d="M12 12.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 1 1-7 0z"/><path d="M5 19.5A3.5 3.5 0 0 1 8.5 16H12v3.5a3.5 3.5 0 1 1-7 0z"/><path d="M5 12.5A3.5 3.5 0 0 1 8.5 9H12v7H8.5A3.5 3.5 0 0 1 5 12.5z"/></svg>'
        cls_extra = " link-figma"
    elif ico_type == "figjam":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 14.14 14.14M12 2a10 10 0 0 1 10 10"/></svg>'
        cls_extra = " link-figjam"
    elif ico_type == "bi":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="13" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="13" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>'
        cls_extra = " link-bi"
    elif ico_type == "img":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'
    elif ico_type == "mmd":
        ico_svg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="6" height="6"/><rect x="15" y="15" width="6" height="6"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/></svg>'
    elif ico_type == "ext":
        ico_svg = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M7 7h10v10"/></svg>'

    tgt = ' target="_blank" rel="noopener noreferrer"' if target_blank else ''
    dl = ' download' if download else ''
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
     sitem("Business Requirements Document", "Business need, objectives, scope, stakeholders, assumptions, requirements and sign-off template.", [flink("docs/01_BRD_PayTrack_Sample.pdf", "PDF", "pdf"), flink("docs/01_BRD_PayTrack_Sample.docx", "Word", "word", target_blank=False)], "brd", ICO_DOC_BRD),
     sitem("Functional Requirements Document", "Functional behaviour, business rules, data entities, screen requirements, NFRs, error states and decisions to confirm.", [flink("docs/02_FRD_PayTrack_Sample.pdf", "PDF", "pdf"), flink("docs/02_FRD_PayTrack_Sample.docx", "Word", "word", target_blank=False)], "frd", ICO_DOC_FRD),
     sitem("User stories and acceptance criteria", "Prioritised stories with testable Given / When / Then criteria.", [flink("docs/03_User_Stories_Acceptance_Criteria_Sample.pdf", "PDF", "pdf"), flink("docs/03_User_Stories_Acceptance_Criteria_Sample.docx", "Word", "word", target_blank=False)], "user-stories", ICO_DOC_STORIES),
     sitem("RTM, test cases and UAT plan", "Traceability from requirement to test, test-case catalogue, UAT entry and exit criteria, sign-off record.", [flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf", "PDF", "pdf"), flink("docs/04_RTM_Test_Cases_UAT_Plan_Sample.docx", "Word", "word", target_blank=False)], "uat", ICO_DOC_RTM),
     sitem("Discovery workshop minutes and decision log", "Workshop summary, discussion themes, open decisions, action tracker and RAID log.", [flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf", "PDF", "pdf"), flink("docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.docx", "Word", "word", target_blank=False)], "discovery", ICO_DOC_DISCOVERY),
     sitem("Complete documentation bundle", "All five documents combined in one PDF.", [flink("docs/PayTrack_Sample_BA_Documentation_Bundle.pdf", "PDF", "pdf")], "bundle", ICO_DOC_BUNDLE)])
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
    return head("BA samples", "Sample artifacts: clear thinking, visible evidence.", "One connected, fictional case study that shows how a business problem becomes requirements, prioritised stories, test coverage, process models and reviewable wireframes.", F.lifecycle("sm"), "../") + f'''
<section class="sec" style="padding-top:8px"><div class="wrap">
<div class="disclaimer rv" style="margin:0 0 48px"><b>Sample only, fictional case study.</b> PayTrack is an invented payment reconciliation and exception-management portal. Names, IDs, amounts, targets and scenarios are illustrative. Test cases have not been executed and no client outcome is claimed.</div>
<h2 class="rv sec-title-with-ico sec-title-docs" style="margin-bottom:20px"><span class="sec-hdr-ico sec-hdr-docs">{ICO_SEC_DOCS}</span><span class="sec-title-text">Documents</span></h2><ul class="file-list">{docs}</ul>
<h2 class="rv sec-title-with-ico sec-title-diag" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-diag">{ICO_SEC_DIAG}</span><span class="sec-title-text">Diagrams and design</span></h2><ul class="file-list">{dg}</ul>
<h2 class="rv sec-title-with-ico sec-title-data" style="margin:56px 0 20px"><span class="sec-hdr-ico sec-hdr-data">{ICO_SEC_DATA}</span><span class="sec-title-text">Structured data</span></h2><ul class="file-list">{sp}</ul>
<p class="note rv" style="margin-top:32px">Scenario: PayTrack compares internal payment records with gateway events, helps operations staff investigate unmatched transactions, assigns ownership of exceptions and keeps an audit trail. Everything here needs stakeholder validation before any real implementation.</p>
</div></section>
''' + cta("../")

DESC = "Gautam Reddy: Business Analyst in Bengaluru with 4+ years in fintech and BFSI. Requirements gathering, BRD/FRD, user stories, REST API requirements, SQL, Python, Power BI, UAT and stakeholder management."
LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "Person", "name": "Gautam Reddy", "jobTitle": "Business Analyst",
    "description": DESC, "url": SITE, "sameAs": [LI, GH, HR],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
    "knowsAbout": ["Business analysis", "Requirements gathering", "Stakeholder management", "BRD and FRD", "User stories", "Acceptance criteria", "UAT", "SQL", "Python", "Power BI", "Agile", "Scrum",
                   "REST API requirements", "Postman", "Payment gateway integrations", "Transaction processing", "Settlement and reconciliation", "SLA monitoring", "Finance and operations reporting", "Fintech", "BFSI"]}, ensure_ascii=False) + '</script>\n'

pages = [
("index.html", "Gautam Reddy | Business Analyst, Bengaluru | Fintech and BFSI", DESC, index(), "", "", LD),
("about.html", "About | Gautam Reddy, Business Analyst", "Who Gautam Reddy is, how he works and the principles behind his requirements and analysis work in fintech and BFSI.", about(), "", "about.html", ""),
("services.html", "Services | Gautam Reddy, Business Analyst", "Business analysis, data analysis, SQL, API and integration analysis, and UAT support, with clear deliverables and scope.", services(), "", "services.html", ""),
("projects.html", "Projects | Gautam Reddy, Business Analyst", "Analytics, BI, data engineering and AI prototypes with links to each repository, plus the PayTrack BA case study.", projects(), "", "projects.html", ""),
("resume.html", "Resume | Gautam Reddy, Business Analyst", "Experience, skills, education and certifications of Gautam Reddy, Business Analyst with 4+ years in fintech and BFSI.", resume(), "", "resume.html", ""),
("contact.html", "Contact | Gautam Reddy, Business Analyst", "Contact Gautam Reddy about a Business Analyst role or a project.", contact(), "", "contact.html", ""),
("samples/index.html", "BA samples | Gautam Reddy, Business Analyst", "PayTrack: a fictional BA case study with BRD, FRD, user stories, RTM, UAT plan, diagrams and CSV samples.", samples(), "../", "samples/index.html", ""),
]
for path, t, d, b, p, cur, ld in pages:
    open(path, "w", encoding="utf-8").write(page(path, t, d, b, p, cur, ld))
print("built", len(pages))
