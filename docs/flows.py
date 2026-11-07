"""Decorative business-analysis diagrams (BPMN-style flows, swimlanes, ERD, sequence, data pipeline).
Rendered as inline SVG that sits behind page sections. Purely decorative: aria-hidden."""
import html
esc = html.escape

class Flow:
    def __init__(s, uid, vb=(1200, 640)):
        s.uid, s.vb, s.parts, s.dots = uid, vb, [], []

    def _t(s, x, y, txt, cls="lb", anchor="middle"):
        return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{html.escape(html.unescape(str(txt)))}</text>'

    def ev(s, x, y, label, end=False, r=15):
        s.parts.append(f'<g class="nd"><circle cx="{x}" cy="{y}" r="{r}" stroke-width="{4 if end else 1.6}"/>{s._t(x, y + r + 18, label)}</g>')

    def task(s, x, y, w, h, label, sub=None):
        t = s._t(x + w / 2, y + h / 2 + (-2 if sub else 4), label)
        if sub: t += s._t(x + w / 2, y + h / 2 + 14, sub, "sb")
        s.parts.append(f'<g class="nd"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>{t}</g>')

    def gate(s, x, y, label, k=34):
        s.parts.append(f'<g class="nd"><polygon points="{x},{y-k} {x+k},{y} {x},{y+k} {x-k},{y}"/>{s._t(x, y + 4, "?", "lb")}{s._t(x, y - k - 8, label)}</g>')

    def db(s, x, y, label, w=64, h=54):
        e = 9
        s.parts.append(f'<g class="nd"><path d="M{x},{y+e} v{h-2*e} a{w/2},{e} 0 0 0 {w},0 v-{h-2*e} M{x},{y+e} a{w/2},{e} 0 0 1 {w},0 a{w/2},{e} 0 0 1 -{w},0"/>{s._t(x + w / 2, y + h + 18, label)}</g>')

    def doc(s, x, y, label, w=70, h=58):
        s.parts.append(f'<g class="nd"><path d="M{x},{y} h{w} v{h-10} q-{w/4},-10 -{w/2},0 t-{w/2},0 z"/><path d="M{x+12},{y+16} h{w-24} M{x+12},{y+28} h{w-24}" class="fine"/>{s._t(x + w / 2, y + h + 14, label)}</g>')

    def bars(s, x, y, label, w=96, h=64):
        b = "".join(f'<rect x="{x+12+i*18}" y="{y+h-14-v}" width="11" height="{v}" rx="2"/>' for i, v in enumerate([14, 28, 20, 40]))
        s.parts.append(f'<g class="nd"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>{b}{s._t(x + w / 2, y + h + 18, label)}</g>')

    def entity(s, x, y, w, title, fields):
        h = 28 + 20 * len(fields)
        f = "".join(s._t(x + 12, y + 46 + i * 20, t, "sb", "start") for i, t in enumerate(fields))
        s.parts.append(f'<g class="nd"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/><path d="M{x},{y+28} h{w}" class="fine"/>{s._t(x + w / 2, y + 19, title)}{f}</g>')

    def life(s, x, y, h, label):
        s.parts.append(f'<g class="nd"><rect x="{x-52}" y="{y}" width="104" height="34" rx="7"/>{s._t(x, y + 22, label)}<path d="M{x},{y+34} v{h}" class="ln"/></g>')

    def lane(s, y, h, label):
        s.parts.append(f'<g class="lane"><rect x="20" y="{y}" width="{s.vb[0]-40}" height="{h}" rx="4"/><path d="M62,{y} v{h}"/><text class="sb" transform="translate(42,{y+h/2}) rotate(-90)" text-anchor="middle">{html.escape(html.unescape(str(label)))}</text></g>')

    def edge(s, pts, dash=True, label=None, dot=None):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        s.parts.append(f'<path class="ln{"" if dash else " solid"}" d="{d}" marker-end="url(#a{s.uid})"/>')
        if label:
            x, y = pts[0]; s.parts.append(s._t(x + 8, y - 8, label, "sb", "start"))
        if dot: s.dots.append((d, dot))

    def curve(s, d, dot=None):
        s.parts.append(f'<path class="ln" d="{d}" marker-end="url(#a{s.uid})"/>')
        if dot: s.dots.append((d, dot))

    # --- Rich UML 2.5 Sequence Diagram Primitives ---
    def sd_frame(s, title, meta="UML 2.5 • BA Specification"):
        w, h = s.vb
        tag_w = min(440, max(220, len(title) * 7 + 54))
        s.parts.append(
            f'<g class="sd-frame">'
            f'<rect x="16" y="12" width="{w-32}" height="{h-24}" rx="10" class="sd-outer"/>'
            f'<polygon points="16,12 {16+tag_w},12 {16+tag_w},28 {16+tag_w-12},38 16,38" class="sd-tag"/>'
            f'{s._t(28, 29, "sd  " + title, "lb", "start")}'
            f'{s._t(w - 32, 29, meta, "sb", "end")}'
            f'</g>'
        )

    def actor(s, x, y, h, label, stereo="", w=136):
        hw = w // 2
        top = f'<g class="nd sd-actor"><rect x="{x-hw}" y="{y}" width="{w}" height="44" rx="7"/>'
        if stereo:
            top += s._t(x, y + 16, f"«{stereo}»", "sb") + s._t(x, y + 33, label, "lb")
        else:
            top += s._t(x, y + 26, label, "lb")
        bot_y = y + 44 + h
        top += f'<path d="M{x},{y+44} v{h}" class="ln sd-lifeline"/>'
        top += f'<rect x="{x-hw//2}" y="{bot_y}" width="{hw}" height="20" rx="4" class="sd-foot"/>'
        top += s._t(x, bot_y + 14, label.split()[0], "sb") + '</g>'
        s.parts.append(top)

    def activate(s, x, y, h):
        s.parts.append(f'<rect x="{x-5}" y="{y}" width="10" height="{h}" rx="2" class="sd-act"/>')

    def msg(s, x1, x2, y, label, reply=False, dot=6):
        dx = 6 if x2 > x1 else -6
        sx = x1 + dx
        ex = x2 - dx
        d = f"M{sx},{y} L{ex},{y}"
        cls = "ln sd-msg reply" if reply else "ln solid sd-msg"
        s.parts.append(f'<path class="{cls}" d="{esc(d)}" marker-end="url(#a{s.uid})"/>')
        mid = (sx + ex) / 2
        s.parts.append(s._t(mid, y - 7, label, "sb", "middle"))
        if dot:
            s.dots.append((d, dot))

    def self_msg(s, x, y, label, w=46, h=26, dot=6):
        d = f"M{x+5},{y} L{x+w},{y} L{x+w},{y+h} L{x+6},{y+h}"
        s.parts.append(f'<path class="ln solid sd-msg" d="{esc(d)}" marker-end="url(#a{s.uid})"/>')
        s.parts.append(s._t(x + w + 8, y + h / 2 + 3, label, "sb", "start"))
        if dot:
            s.dots.append((d, dot))

    def frag(s, x, y, w, h, op="alt", guard=""):
        tw = max(48, len(op) * 8 + 22)
        s.parts.append(
            f'<g class="sd-frag">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="sd-frag-box"/>'
            f'<polygon points="{x},{y} {x+tw},{y} {x+tw},{y+14} {x+tw-8},{y+22} {x},{y+22}" class="sd-frag-tag"/>'
            f'{s._t(x + 8, y + 15, op, "sb", "start")}'
            f'{s._t(x + tw + 10, y + 15, guard, "sb", "start") if guard else ""}'
            f'</g>'
        )

    def note(s, x, y, w, h, title, sub=""):
        fold = 10
        s.parts.append(
            f'<g class="nd sd-note">'
            f'<path d="M{x},{y} h{w-fold} l{fold},{fold} v{h-fold} h-{w} z"/>'
            f'<path d="M{x+w-fold},{y} v{fold} h{fold}" class="fine"/>'
            f'{s._t(x + w/2, y + (18 if sub else h/2 + 4), title, "sb")}'
            f'{s._t(x + w/2, y + 33, sub, "sb") if sub else ""}'
            f'</g>'
        )

    def render(s, cls="", aspect="xMidYMid slice"):
        w, h = s.vb
        dots = "".join(f'<circle class="pk" r="4.8"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}"/></circle>' for d, dur in s.dots)
        return (f'<svg class="bgflow {cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="{aspect}" aria-hidden="true" focusable="false">'
                f'<defs><marker id="a{s.uid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" class="ah"/></marker></defs>'
                + "".join(s.parts) + dots + '</svg>')


# --- Foundational Diagrams (Preserved) ---
def lifecycle(uid="h"):
    f = Flow(uid, (1200, 640))
    f.ev(70, 130, "Request"); f.task(130, 100, 128, 60, "Elicit", "workshops"); f.task(310, 100, 140, 60, "Analyse", "gap + AS-IS/TO-BE")
    f.gate(540, 130, "Valid?"); f.task(630, 100, 140, 60, "Specify", "BRD / FRD"); f.task(820, 100, 128, 60, "Build + test", "UAT")
    f.ev(1040, 130, "Go-live", end=True)
    f.edge([(85, 130), (130, 130)], dot=5); f.edge([(258, 130), (310, 130)], dot=6); f.edge([(450, 130), (506, 130)], dot=7)
    f.edge([(574, 130), (630, 130)], label="yes", dot=6); f.edge([(770, 130), (820, 130)], dot=6); f.edge([(948, 130), (1025, 130)], dot=6)
    f.task(470, 300, 140, 56, "Clarify", "stakeholders"); f.edge([(540, 164), (540, 300)], label="no", dot=7)
    f.curve("M470,328 C360,328 220,300 194,162", dot=9)
    f.db(120, 470, "Source data"); f.task(280, 470, 130, 54, "SQL / Python", "validate"); f.bars(480, 462, "Insight", 100, 70)
    f.edge([(184, 497), (280, 497)], dot=6); f.edge([(410, 497), (480, 497)], dot=6)
    f.doc(760, 470, "User stories"); f.task(900, 470, 130, 54, "RTM", "trace to tests"); f.edge([(830, 497), (900, 497)], dot=7)
    f.edge([(1030, 497), (1100, 497), (1100, 200)], dash=True, dot=8)
    return f.render()

def swim(uid="s"):
    f = Flow(uid, (1200, 520))
    for i, n in enumerate(["Business", "BA", "Eng + QA"]): f.lane(40 + i * 150, 140, n)
    f.ev(110, 110, "Need", r=13); f.task(180, 80, 130, 56, "Raise request")
    f.task(360, 230, 150, 56, "Workshop", "elicit + prioritise"); f.task(570, 230, 150, 56, "Write BRD / FRD", "stories + AC")
    f.gate(820, 258, "Sign-off?"); f.task(900, 80, 140, 56, "Approve scope")
    f.task(900, 380, 150, 56, "Build + test", "RTM coverage"); f.ev(1130, 408, "Done", end=True, r=13)
    f.edge([(123, 108), (180, 108)], dot=5); f.edge([(310, 108), (435, 108), (435, 230)], dot=7)
    f.edge([(510, 258), (570, 258)], dot=6); f.edge([(720, 258), (786, 258)], dot=6)
    f.edge([(820, 224), (820, 108), (900, 108)], label="yes", dot=6); f.edge([(970, 136), (970, 160), (700, 160), (700, 230)], dash=True, dot=8)
    f.edge([(820, 292), (820, 408), (900, 408)], label="rework", dot=7)
    f.edge([(1050, 408), (1117, 408)], dot=5)
    return f.render()

def erd(uid="e"):
    f = Flow(uid, (1200, 560))
    f.entity(80, 60, 200, "PAYMENT_TRANSACTION", ["payment_id PK", "amount", "status", "gateway_ref FK"])
    f.entity(430, 40, 210, "GATEWAY_EVENT", ["event_id PK", "gateway_ref", "settled_at", "fee"])
    f.entity(800, 70, 220, "RECON_RESULT", ["result_id PK", "payment_id FK", "event_id FK", "match_state"])
    f.entity(260, 330, 210, "EXCEPTION_CASE", ["case_id PK", "result_id FK", "owner", "sla_due"])
    f.entity(700, 340, 220, "AUDIT_EVENT", ["audit_id PK", "case_id FK", "actor", "action"])
    f.edge([(280, 130), (430, 110)], dash=False, dot=6); f.edge([(640, 110), (800, 130)], dash=False, dot=7)
    f.edge([(910, 200), (910, 260), (365, 260), (365, 330)], dot=8); f.edge([(470, 400), (700, 400)], dash=False, dot=7)
    return f.render()

def pipeline(uid="p"):
    f = Flow(uid, (1200, 520))
    f.db(90, 120, "Sources"); f.db(90, 300, "Gateway logs")
    f.task(300, 160, 140, 58, "Extract", "SQL"); f.task(300, 290, 140, 58, "Clean", "Python / Pandas")
    f.task(540, 225, 150, 58, "Model + DAX", "KPI definitions"); f.bars(800, 190, "Dashboard", 110, 76)
    f.doc(1000, 200, "Insight", 80, 62)
    f.edge([(154, 147), (230, 147), (230, 189), (300, 189)], dot=7); f.edge([(154, 327), (230, 327), (230, 319), (300, 319)], dot=7)
    f.edge([(440, 189), (490, 189), (490, 254), (540, 254)], dot=6); f.edge([(440, 319), (490, 319), (490, 254)], dot=8)
    f.edge([(690, 254), (800, 227)], dot=7); f.edge([(910, 228), (1000, 228)], dot=6)
    f.ev(170, 440, "Define", r=11); f.task(260, 415, 120, 50, "Validate"); f.task(440, 415, 120, 50, "Reconcile"); f.task(620, 415, 120, 50, "Report")
    f.edge([(181, 440), (260, 440)], dot=5); f.edge([(380, 440), (440, 440)], dot=6); f.edge([(560, 440), (620, 440)], dot=6)
    return f.render()

def mini(uid):
    """tiny flow for project thumbnails / placeholders - no CPU-heavy animated dots"""
    f = Flow(uid, (400, 200))
    f.ev(40, 100, "", r=9); f.task(80, 74, 80, 52, ""); f.gate(215, 100, "", k=26); f.task(268, 74, 90, 52, "")
    f.edge([(49, 100), (80, 100)]); f.edge([(160, 100), (189, 100)]); f.edge([(241, 100), (268, 100)])
    return f.render("mini", aspect="xMidYMid meet")


def seq(uid="q"):
    f = Flow(uid, (1200, 520))
    f.sd_frame("Payment Submission & Settlement Verification", "OpenAPI 3.0 • Sequence")
    xs = [150, 410, 690, 970]
    stereos = ["Actor", "REST API", "Service", "External"]
    names = ["Client Portal", "PayTrack API", "Recon Engine", "Payment Gateway"]
    for x, st, n in zip(xs, stereos, names):
        f.actor(x, 52, 390, n, st)
    f.activate(150, 115, 290); f.activate(410, 125, 270); f.activate(690, 170, 190); f.activate(970, 215, 85)
    f.msg(150, 410, 130, "1: POST /v1/payments {amount, currency}", dot=6)
    f.msg(410, 690, 180, "2: validateSchema() + enqueueTx()", dot=7)
    f.msg(690, 970, 230, "3: fetchSettlementFeed(batch_window)", dot=8)
    f.msg(970, 690, 290, "4: 200 OK {gateway_ref, settled_at}", reply=True, dot=7)
    f.self_msg(690, 310, "5: matchTransaction(tolerance=0.00)", h=24, dot=6)
    f.msg(690, 410, 350, "6: ReconResult {status: RECONCILED}", reply=True, dot=6)
    f.msg(410, 150, 390, "7: 200 OK {match_rate: 99.8%, sla: OK}", reply=True, dot=7)
    return f.render()


# ==============================================================================
# Page-Specific Bespoke Sequence Diagrams (Unique Per Page & Section)
# ==============================================================================

def seq_about(uid="ab_seq"):
    """About Page Header: Stakeholder Elicitation & Three Amigos Alignment Sequence."""
    f = Flow(uid, (1200, 540))
    f.sd_frame("Stakeholder Triangulation & Three Amigos Specification Flow", "About • Governance")
    xs = [135, 390, 650, 910, 1090]
    actors = [
        ("Stakeholders", "Finance / Ops"),
        ("Gautam Reddy", "Lead BA"),
        ("Architecture", "Eng / API"),
        ("QA & Testing", "UAT Lead"),
        ("Confluence", "RTM Repo")
    ]
    for x, (name, st) in zip(xs, actors):
        f.actor(x, 52, 410, name, st, w=132)
    f.activate(390, 110, 330); f.activate(650, 185, 140); f.activate(910, 260, 140)
    f.frag(70, 108, 640, 92, "loop", "[20+ Elicitation Workshops • 13+ Stakeholders]")
    f.msg(135, 390, 145, "1: raiseBusinessNeed(pain_points, KPI_targets)", dot=6)
    f.self_msg(390, 162, "2: separateEvidenceFromAssumptions()", h=22, dot=6)
    f.msg(390, 650, 215, "3: defineContracts(BRD, FRD, NFRs, OpenAPI_3.0, STTM)", dot=7)
    f.msg(650, 390, 255, "4: confirmFeasibility(idempotency, schema_validation)", reply=True, dot=6)
    f.msg(390, 910, 295, "5: conductThreeAmigos(BDD_Given_When_Then_Criteria)", dot=7)
    f.msg(910, 1090, 340, "6: linkTraceability(BR_ID -> FR_ID -> US_ID -> TC_ID)", dot=6)
    f.msg(1090, 390, 385, "7: baselineApproved(100% RTM Coverage)", reply=True, dot=7)
    f.msg(390, 135, 425, "8: signOffScope(agreed_deliverables, release_plan)", reply=True, dot=6)
    return f.render()


def seq_bre(uid="ab_bre"):
    """About Page Section 1: Business Rules Engine (BRE-204) & Change Impact Sequence."""
    f = Flow(uid, (1200, 560))
    f.sd_frame("SPEC-BRE-204 • Payment Idempotency, Validation & SLA Breach Triage", "Decision Engine • Sequence")
    xs = [140, 395, 665, 940]
    for x, (name, st) in zip(xs, [
        ("Gateway Webhook", "Inbound Event"),
        ("API Validator", "FR-006 / FR-007"),
        ("Rules Engine", "SPEC-BRE-204"),
        ("Ops Triage Queue", "FR-005 SLA")
    ]):
        f.actor(x, 54, 420, name, st, w=144)
    f.activate(395, 115, 330); f.activate(665, 165, 260); f.activate(940, 320, 110)
    f.msg(140, 395, 125, "1: POST /webhooks/settlement (HMAC-SHA256, idempotency_key)", dot=6)
    f.msg(395, 665, 170, "2: evaluateRule(FR-007: checkIdempotencyWindow(24h))", dot=6)
    f.frag(80, 195, 1040, 235, "alt", "[Idempotency Key Exists < 24h] vs [Schema Invalid] vs [SLA > 4h]")
    f.msg(665, 140, 235, "3a: 200 OK {cached_status: DUPLICATE_IGNORED}", reply=True, dot=7)
    f.msg(395, 140, 285, "3b: 422 Unprocessable Entity {error_schema: FR-006}", reply=True, dot=7)
    f.msg(665, 940, 340, "3c: flagException(severity=HIGH, sla_timer=4h)", dot=6)
    f.msg(940, 665, 395, "4: ackCaseCreated(case_id, assigned_tier=TIER_2)", reply=True, dot=6)
    return f.render()


def seq_services(uid="sv_seq"):
    """Services Page Section 1: End-to-End BA Service Engagement Sequence."""
    f = Flow(uid, (1200, 560))
    f.sd_frame("BA Service Engagement: Discovery -> Specification -> API/SQL -> UAT Handover", "Services • Delivery")
    xs = [135, 385, 645, 905, 1085]
    for x, (name, st) in zip(xs, [
        ("Client Lead", "Product / Ops"),
        ("Gautam Reddy", "BA Advisory"),
        ("Specs & Models", "BRD / BPMN / STTM"),
        ("Data & BI", "SQL / Power BI"),
        ("QA & Release", "RTM & UAT")
    ]):
        f.actor(x, 52, 420, name, st, w=132)
    f.activate(385, 115, 340); f.activate(645, 175, 140); f.activate(905, 240, 120); f.activate(1085, 345, 100)
    f.msg(135, 385, 130, "1: Phase 1 Understand(problem, users, constraints, SLA)", dot=6)
    f.msg(385, 645, 180, "2: Phase 2 Scope(BRD, FRD, NFRs, BPMN/UML, REST STTM)", dot=7)
    f.frag(330, 205, 640, 125, "par", "[Parallel Specification & Data Quality Profiling]")
    f.msg(385, 905, 250, "3a: profileDataQuality(100K+ SQL rows, 5-Why RCA, DAX KPIs)", dot=7)
    f.msg(645, 385, 300, "3b: reviewCheckpoint(BDD User Stories + JSON Schemas)", reply=True, dot=6)
    f.msg(385, 1085, 360, "4: Phase 3 Validate(RTM Matrix, UAT Test Plan, Defect Triage)", dot=7)
    f.msg(1085, 135, 415, "5: Phase 4 Handover(Signed-Off Specs + Confluence Data Dict)", reply=True, dot=8)
    return f.render()


def seq_faq(uid="sv_faq"):
    """Services Page FAQ Section: Scope Clarification & NDA Onboarding Sequence."""
    f = Flow(uid, (1200, 500))
    f.sd_frame("Enquiry Scoping, Confidentiality (NDA) & Checkpoint Cadence", "Onboarding • Sequence")
    xs = [170, 460, 750, 1030]
    for x, (name, st) in zip(xs, [
        ("Hiring / Ops Team", "Client"),
        ("BA Scoping", "Gautam Reddy"),
        ("Governance", "NDA & Access"),
        ("Sprint Cadence", "Checkpoints")
    ]):
        f.actor(x, 52, 365, name, st, w=144)
    f.activate(460, 115, 280)
    f.msg(170, 460, 130, "1: shareProblemAndDesiredOutcome(scope, timeline)", dot=6)
    f.msg(460, 750, 185, "2: establishNDA(secure_handling, no_raw_credentials)", dot=6)
    f.msg(750, 460, 235, "3: confirmRepoAndConfluenceAccess()", reply=True, dot=6)
    f.msg(460, 1030, 290, "4: agreeDeliverableMilestones(pilot_or_full_scope)", dot=7)
    f.msg(1030, 170, 350, "5: deliverReviewableArtifacts(BRD, SQL, RTM, Handover)", reply=True, dot=7)
    return f.render()


def seq_projects(uid="pj_seq"):
    """Projects Page Section 1: PayTrack Multi-Gateway Reconciliation & Portfolio Sequence."""
    f = Flow(uid, (1200, 580))
    f.sd_frame("PayTrack Case Study & Analytics Portfolio • End-to-End Execution Sequence", "Projects • Architecture")
    xs = [130, 365, 605, 845, 1075]
    for x, (name, st) in zip(xs, [
        ("Ops Analyst", "PayTrack UI"),
        ("Recon Service", "FR-002..FR-007"),
        ("Gateway Feeds", "Stripe / Razorpay"),
        ("Analytics DB", "PostgreSQL / BI"),
        ("Exception Case", "FR-008..FR-011")
    ]):
        f.actor(x, 52, 440, name, st, w=134)
    f.activate(365, 115, 360); f.activate(605, 155, 95); f.activate(845, 240, 130); f.activate(1075, 330, 130)
    f.msg(130, 365, 125, "1: triggerDailyBatchRecon(window='23:00 IST')", dot=6)
    f.msg(365, 605, 170, "2: ingestWebhookAndSettlementEvents(USD, INR)", dot=7)
    f.msg(605, 365, 220, "3: streamNormalizedPayloads(100,000+ records)", reply=True, dot=7)
    f.msg(365, 845, 265, "4: executeReconciliationSQL(join_payment_tx_gateway_ev)", dot=6)
    f.frag(310, 295, 820, 165, "alt", "[99.8% Straight-Through Match] vs [Amount Mismatch / Orphan Event]")
    f.msg(845, 365, 335, "5a: markReconciled(audit_trail=100%,kpi_refresh=True)", reply=True, dot=6)
    f.msg(365, 1075, 385, "5b: createExceptionCase(alert_within='5 min', sla='4h')", dot=7)
    f.msg(1075, 130, 435, "6: notifyOpsDashboard(owner_assigned, audit_event_logged)", reply=True, dot=7)
    return f.render()


def seq_resume(uid="rs_seq"):
    """Resume Page Header: Career Progression & Enterprise BA Delivery Sequence."""
    f = Flow(uid, (1200, 520))
    f.sd_frame("4+ Years BA Delivery: Elicitation -> API/STTM -> SQL (100K+) -> UAT (350+ Scenarios)", "Resume • Track Record")
    xs = [135, 380, 635, 885, 1085]
    for x, (name, st) in zip(xs, [
        ("Stakeholders", "13+ Business Leads"),
        ("Gautam Reddy", "Business Analyst"),
        ("Integrations", "2 Payment Gateways"),
        ("SQL & Python", "100K+ Txn Logs"),
        ("QA & UAT", "350+ Scenarios")
    ]):
        f.actor(x, 52, 390, name, st, w=134)
    f.activate(380, 110, 315)
    f.msg(135, 380, 125, "1: facilitateWorkshops(20+ sessions across 4 business units)", dot=6)
    f.msg(380, 635, 175, "2: authorSpecs(BRD, FRD, NFRs, REST APIs, STTM, JSON Schemas)", dot=7)
    f.msg(380, 885, 230, "3: analyzeTransactionLogs(100,000+ rows -> isolate 3 SLA breaches)", dot=7)
    f.msg(885, 380, 280, "4: formalizeReconciliationRules(save ~2 wks/cycle, 3+ hrs/wk)", reply=True, dot=6)
    f.msg(380, 1085, 335, "5: coordinateUATAndTriage(350+ Marolix + 50+ Infocomm cases)", dot=7)
    f.msg(1085, 135, 390, "6: productionRelease(12+ CRs managed • 0 critical defects)", reply=True, dot=8)
    return f.render()


def seq_resume_sql(uid="rs_sql"):
    """Resume Page Section 1: Metrics & SQL Root Cause Analysis Sequence."""
    f = Flow(uid, (1200, 480))
    f.sd_frame("Quantitative Impact Verification • SQL Profiling, MoSCoW Scope & Power BI Automation", "Metrics • Sequence")
    xs = [160, 450, 740, 1030]
    for x, (name, st) in zip(xs, [
        ("Operational Data", "100K+ Records"),
        ("SQL & Python RCA", "Fishbone / 5-Why"),
        ("Process Redesign", "AS-IS -> TO-BE BPMN"),
        ("Business Impact", "Verified Outcome")
    ]):
        f.actor(x, 52, 350, name, st, w=144)
    f.activate(450, 110, 260); f.activate(740, 180, 170)
    f.msg(160, 450, 130, "1: extractSettlementAndSlaLogs(PostgreSQL, Pandas)", dot=6)
    f.self_msg(450, 155, "2: detect3RecurringSlaBreachPatterns()", h=24, dot=6)
    f.msg(450, 740, 215, "3: mapToBeWorkflowAndPowerBiSpecs(15+ stakeholders)", dot=7)
    f.msg(740, 1030, 275, "4: filterUnjustifiedScope(MoSCoW across 4 modules)", dot=6)
    f.msg(1030, 160, 335, "5: achieveZeroCriticalDefectsAnd2WeekCycleReduction()", reply=True, dot=7)
    return f.render()


def seq_resume_uat(uid="rs_uat"):
    """Resume Page Section 2: Multi-Company Career Timeline & Promotion Sequence."""
    f = Flow(uid, (1200, 560))
    f.sd_frame("Career Progression Sequence: Infocomm (ASE -> Early Promotion to BA) -> V Moksha -> Marolix", "Career • Sequence")
    xs = [150, 420, 695, 985]
    for x, (name, st) in zip(xs, [
        ("Infocomm (ASE->BA)", "Early Promotion"),
        ("Infocomm (BA)", "3 Modules • 4 Units"),
        ("V Moksha (BA)", "RCA & BPMN"),
        ("Marolix (BA)", "Payment Gateways")
    ]):
        f.actor(x, 52, 425, name, st, w=146)
    f.activate(150, 110, 90); f.activate(420, 185, 100); f.activate(695, 270, 95); f.activate(985, 345, 110)
    f.msg(150, 420, 135, "1: deliver3ReportingFeatures(15+ stakeholders -> +3h/wk saved)", dot=6)
    f.note(60, 155, 210, 36, "Promoted Early to BA", "Ahead of schedule")
    f.msg(420, 695, 225, "2: runThreeAmigosAnd50JiraTests(0 post-launch incidents)", dot=7)
    f.msg(695, 985, 310, "3: resolveSlaShortfallsViaSqlAndBpmn(-2 wks cycle time)", dot=7)
    f.self_msg(985, 365, "4: lead2GatewayIntegrations + 100K_SQL + 350_UAT()", h=26, dot=6)
    f.msg(985, 150, 435, "5: continuousTraceabilityAndCBAPTarget(2026/2027)", reply=True, dot=8)
    return f.render()


def seq_contact(uid="ct_seq"):
    """Contact Page Section 1: Global Remote Collaboration & Enquiry Sequence."""
    f = Flow(uid, (1200, 560))
    f.sd_frame("Project & Role Enquiry Sequence • Bengaluru (IST / UTC+5:30) <-> EMEA & US Overlap", "Contact • Sequence")
    xs = [145, 415, 695, 985]
    for x, (name, st) in zip(xs, [
        ("Hiring / Project Lead", "Global Client"),
        ("Enquiry Builder", "Zero-Storage Form"),
        ("Gautam Reddy (BA)", "Bengaluru UTC+5:30"),
        ("Discovery & Scope", "Agreed Kickoff")
    ]):
        f.actor(x, 52, 425, name, st, w=148)
    f.activate(415, 115, 150); f.activate(695, 235, 215); f.activate(985, 340, 110)
    f.msg(145, 415, 130, "1: selectServiceAndTimeline(?service=prefill, problem_brief)", dot=6)
    f.self_msg(415, 165, "2: validateFieldsAndPrepareDraft(mailto + clipboard)", h=24, dot=6)
    f.msg(415, 695, 240, "3: sendEnquiryEmail(gautamreddy098@gmail.com)", dot=7)
    f.msg(695, 145, 295, "4: replyWithContextWithin1To2BusinessDays(IST/EMEA/US sync)", reply=True, dot=7)
    f.msg(145, 985, 355, "5: alignOnProblemUsersSystemsAndAcceptanceCriteria()", dot=6)
    f.msg(985, 145, 420, "6: commenceDeliverables(BRD / FRD / SQL / API / UAT)", reply=True, dot=7)
    return f.render()


def seq_samples(uid="sm_seq"):
    """Samples Page Section 1: PayTrack 17-Deliverable End-to-End Traceability Sequence."""
    f = Flow(uid, (1200, 580))
    f.sd_frame("PayTrack Case Study • End-to-End Artifact Traceability Sequence (Phases 01 -> 04)", "Samples • RTM Flow")
    xs = [130, 365, 605, 845, 1075]
    for x, (name, st) in zip(xs, [
        ("01 Discovery MoM", "RAID & Decisions"),
        ("02 BRD & FRD", "BR-01..03 / FR-001..11"),
        ("BPMN / ERD / API", "Models & Schemas"),
        ("03 User Stories", "US-01..10 + SQL"),
        ("04 RTM & UAT Plan", "TC-001..15 Matrix")
    ]):
        f.actor(x, 52, 440, name, st, w=136)
    f.activate(130, 110, 90); f.activate(365, 165, 150); f.activate(605, 235, 130); f.activate(845, 305, 120); f.activate(1075, 370, 100)
    f.msg(130, 365, 130, "1: baselineScopeAndRACI(23:00 IST cutoff, 4h SLA target)", dot=6)
    f.msg(365, 605, 195, "2: modelProcessSwimlanesAndERD(5 tables, OpenAPI 3.0)", dot=7)
    f.msg(605, 845, 265, "3: derivePrioritizedBacklog(MoSCoW + Given/When/Then BDD)", dot=7)
    f.msg(845, 1075, 335, "4: mapRequirementsToTestCatalogue(8 BRs -> 15 Test Cases)", dot=7)
    f.self_msg(1075, 380, "5: verify100PercentForwardAndBackwardTraceability()", h=24, dot=6)
    f.msg(1075, 365, 445, "6: consolidate35PageDocumentPack(PRE-2026 Sign-Off Ready)", reply=True, dot=8)
    return f.render()


def seq_404(uid="nf_seq"):
    """404 Page: Route Specification Lookup & Fallback Recovery Sequence."""
    f = Flow(uid, (1200, 500))
    f.sd_frame("HTTP 404 • Unmapped Endpoint Detection & Specification Recovery Sequence", "404 • Diagnostic")
    xs = [165, 455, 745, 1035]
    for x, (name, st) in zip(xs, [
        ("Visitor Browser", "GET Request"),
        ("Route Specification", "Sitemap & Docs"),
        ("404 Fault Handler", "Exception Guard"),
        ("Portfolio Hub", "Verified Routes")
    ]):
        f.actor(x, 52, 365, name, st, w=144)
    f.activate(455, 115, 130); f.activate(745, 210, 140); f.activate(1035, 310, 85)
    f.msg(165, 455, 130, "1: GET /unmapped-uri (lookup route in specification)", dot=6)
    f.frag(110, 165, 980, 225, "alt", "[Route Missing from Sitemap Specification -> HTTP 404]")
    f.msg(455, 745, 215, "2: raiseRouteNotFoundException(status=404_MISSING_REQ)", dot=6)
    f.msg(745, 165, 275, "3: renderDiagnosticRecoveryView(popular_destinations)", reply=True, dot=7)
    f.msg(165, 1035, 335, "4: navigateToVerifiedArtifact(index.html | samples | resume)", dot=7)
    f.msg(1035, 165, 375, "5: 200 OK (Specification Loaded)", reply=True, dot=6)
    return f.render()
