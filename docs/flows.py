"""Decorative business-analysis diagrams (BPMN-style flows, swimlanes, ERD, sequence, data pipeline).
Rendered as inline SVG that sits behind page sections. Purely decorative: aria-hidden."""
import html

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

    # --- Reusable UML 2.5 Sequence Diagram Primitives ---
    def sd_frame(s, x, y, w, h, title):
        """UML sequence diagram frame with pentagon-style corner header."""
        tw = min(w - 30, max(120, len(title) * 8 + 36))
        s.parts.append(
            f'<g class="sd-frame">'
            f'<rect class="sd-frame-rect" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
            f'<polygon class="sd-tag" points="{x},{y} {x+tw},{y} {x+tw+12},{y+13} {x+tw},{y+26} {x},{y+26}"/>'
            f'<text class="sd-title" x="{x+10}" y="{y+18}">sd {html.escape(title)}</text>'
            f'</g>'
        )

    def actor(s, x, y, h, label, stereotype="Actor", w=116):
        """Participant lifeline with UML stereotype, label, dashed lifeline, and termination marker."""
        box_w = max(w, len(label) * 8 + 16)
        s.parts.append(
            f'<g class="sd-participant">'
            f'<rect class="sd-actor-box" x="{x - box_w/2}" y="{y}" width="{box_w}" height="42" rx="6"/>'
            f'<text class="sd-stereo" x="{x}" y="{y+15}" text-anchor="middle">&#171;{html.escape(stereotype)}&#187;</text>'
            f'<text class="sd-actor-lbl" x="{x}" y="{y+32}" text-anchor="middle">{html.escape(label)}</text>'
            f'<path class="sd-lifeline ln" d="M{x},{y+42} v{h}" stroke-dasharray="4 4"/>'
            f'<line class="sd-term" x1="{x-14}" y1="{y+42+h}" x2="{x+14}" y2="{y+42+h}"/>'
            f'</g>'
        )

    def activate(s, x, y, h, cls=""):
        """Execution specification vertical activation bar on a lifeline."""
        s.parts.append(f'<rect class="sd-act {cls}" x="{x-7}" y="{y}" width="14" height="{h}" rx="3"/>')

    def msg(s, x1, y1, x2, y2, label, sync=True, dash=False, dot=None, num=None):
        """UML synchronous/asynchronous or dashed reply message between lifelines."""
        num_prefix = f"{num}. " if num is not None else ""
        d = f"M{x1},{y1} L{x2},{y2}"
        lbl_x = (x1 + x2) / 2
        lbl_y = min(y1, y2) - 6
        anchor = "middle"
        cls_extra = " dashed" if dash else (" solid" if not sync else "")
        s.parts.append(
            f'<g class="sd-msg-group">'
            f'<path class="sd-msg ln{cls_extra}" d="{d}" marker-end="url(#a{s.uid})"/>'
            f'<text class="sd-msg-lbl sb" x="{lbl_x}" y="{lbl_y}" text-anchor="{anchor}">{html.escape(num_prefix + label)}</text>'
            f'</g>'
        )
        if dot:
            s.dots.append((d, dot))

    def self_msg(s, x, y, w, h, label, num=None, dot=None):
        """Internal processing / validation loop self-call on a lifeline."""
        num_prefix = f"{num}. " if num is not None else ""
        d = f"M{x},{y} h{w} v{h} h-{w}"
        s.parts.append(
            f'<g class="sd-self-msg-group">'
            f'<path class="sd-self-msg ln" d="{d}" marker-end="url(#a{s.uid})"/>'
            f'<text class="sd-self-lbl sb" x="{x+w+8}" y="{y+h/2+4}" text-anchor="start">{html.escape(num_prefix + label)}</text>'
            f'</g>'
        )
        if dot:
            s.dots.append((d, dot))

    def frag(s, x, y, w, h, op, condition="", operands=None):
        """UML interaction fragment frame (alt, loop, par) with guard conditions and operand dividers."""
        tag_w = max(42, len(op) * 9 + 14)
        dividers = ""
        if operands:
            for div_y, op_cond in operands:
                dividers += (
                    f'<line class="sd-frag-div" x1="{x}" y1="{div_y}" x2="{x+w}" y2="{div_y}" stroke-dasharray="6 4"/>'
                )
                if op_cond:
                    dividers += f'<text class="sd-frag-guard" x="{x+10}" y="{div_y+16}">[{html.escape(op_cond)}]</text>'
        cond_text = f'<text class="sd-frag-guard" x="{x+tag_w+14}" y="{y+16}">[{html.escape(condition)}]</text>' if condition else ""
        s.parts.append(
            f'<g class="sd-frag">'
            f'<rect class="sd-frag-rect" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>'
            f'<polygon class="sd-frag-op-tag" points="{x},{y} {x+tag_w},{y} {x+tag_w+8},{y+10} {x+tag_w},{y+20} {x},{y+20}"/>'
            f'<text class="sd-frag-op-lbl" x="{x+6}" y="{y+14}">{html.escape(op)}</text>'
            f'{cond_text}'
            f'{dividers}'
            f'</g>'
        )

    def note(s, x, y, w, h, text, anchor="start"):
        """Dog-eared UML annotation note."""
        s.parts.append(
            f'<g class="sd-note-group">'
            f'<path class="sd-note" d="M{x},{y} h{w-12} l12,12 v{h-12} h-{w} z"/>'
            f'<path class="sd-note-fold" d="M{x+w-12},{y} v12 h12 z"/>'
            f'<text class="sd-note-lbl" x="{x+10}" y="{y+h/2+4}" text-anchor="{anchor}">{html.escape(text)}</text>'
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


# ==============================================================================
# PAGE-SPECIFIC UML 2.5 SEQUENCE DIAGRAMS (12 DIAGRAM SUITE)
# ==============================================================================

# 1. PAGE 1 — HOME: Payment Submission & Settlement Verification
def seq(uid="e"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Payment Submission & Settlement Verification")
    x_c, x_api, x_rec, x_gw = 150, 430, 730, 1030
    f.actor(x_c, 60, 390, "Client Portal", "Actor")
    f.actor(x_api, 60, 390, "PayTrack API", "REST API")
    f.actor(x_rec, 60, 390, "Recon Engine", "Service")
    f.actor(x_gw, 60, 390, "Payment Gateway", "External")

    f.activate(x_api, 130, 270)
    f.activate(x_rec, 180, 190)
    f.activate(x_gw, 230, 60)

    f.msg(x_c, 140, x_api, 140, "POST /v1/payments", num=1, dot=6)
    f.msg(x_api, 190, x_rec, 190, "validateSchema() + enqueueTx()", num=2, dot=7)
    f.msg(x_rec, 240, x_gw, 240, "fetchSettlementFeed()", num=3, dot=8)
    f.msg(x_gw, 280, x_rec, 280, "settlementFeed[1.4K tx]", dash=True, dot=7)
    f.self_msg(x_rec, 310, 50, 35, "matchTransaction(tolerance=0.00)", num=4)
    f.msg(x_rec, 360, x_api, 360, "matchResult(99.8% reconciled)", dash=True, dot=6)
    f.msg(x_api, 390, x_c, 390, "200 OK {match_rate: 99.8%}", dash=True, num=5, dot=7)
    f.note(790, 410, 240, 44, "Auto-reconciles within SLA (< 4h)")
    return f.render("sd-outer")


# 2. PAGE 2 — ABOUT: Diagram A: Stakeholder Triangulation & Three Amigos Specification Flow
def seq_about(uid="a"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Stakeholder Triangulation & Three Amigos Specification Flow")
    x_sh, x_ba, x_eng, x_rep = 150, 440, 750, 1030
    f.actor(x_sh, 60, 390, "Business Stakeholders", "Actor")
    f.actor(x_ba, 60, 390, "Gautam (Lead BA)", "Business Analyst")
    f.actor(x_eng, 60, 390, "Dev & QA Leads", "Engineering")
    f.actor(x_rep, 60, 390, "Specification Repo", "Artifacts")

    f.frag(60, 120, 1080, 280, "loop", "20+ Elicitation Workshops • 13+ Stakeholders")
    f.activate(x_ba, 140, 240)
    f.activate(x_eng, 230, 80)

    f.msg(x_sh, 150, x_ba, 150, "elicitOperationalGoals()", num=1, dot=6)
    f.self_msg(x_ba, 180, 60, 35, "separateEvidenceFromAssumptions()", num=2)
    f.msg(x_ba, 240, x_eng, 240, "conductThreeAmigos(BDD)", num=3, dot=7)
    f.msg(x_eng, 290, x_ba, 290, "refineAcceptanceCriteria(Given/When/Then)", dash=True, dot=6)
    f.msg(x_ba, 340, x_rep, 340, "commitVerifiedSpec(BRD + FRD + User Stories)", num=4, dot=7)
    f.note(780, 420, 270, 44, "100% Traceability across Jira & RTM")
    return f.render("sd-outer")


# 3. PAGE 2 — ABOUT: Diagram B: SPEC-BRE-204 • Payment Idempotency, Validation & SLA Breach Triage
def seq_bre(uid="ab0"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "SPEC-BRE-204 • Payment Idempotency, Validation & SLA Breach Triage")
    x_in, x_idm, x_rul, x_esc = 150, 430, 730, 1030
    f.actor(x_in, 60, 390, "Inbound Payment", "Client")
    f.actor(x_idm, 60, 390, "Idempotency Filter", "Middleware")
    f.actor(x_rul, 60, 390, "Rules Engine", "Service")
    f.actor(x_esc, 60, 390, "Escalation Dispatcher", "Alerts")

    f.msg(x_in, 130, x_idm, 130, "POST /v1/payments {idem_key}", dot=6)
    f.frag(60, 160, 1080, 260, "alt", "Idempotency Key < 24h", operands=[
        (250, "HTTP 422 FR-006"),
        (340, "SLA > 4h Alert")
    ])

    f.msg(x_idm, 190, x_in, 190, "returnCachedResponse(status='CONFIRMED')", dash=True, dot=7)
    f.msg(x_idm, 280, x_in, 280, "422 Unprocessable Entity {code: 'PAYMENT_EXISTS'}", dash=True, dot=6)
    f.msg(x_rul, 360, x_esc, 360, "dispatchExceptionAlert(triage_sla='4h', alert='5 min')", dot=8)
    f.note(770, 430, 270, 40, "Guarantees zero duplicate ledger debits")
    return f.render("sd-outer")


# 4. PAGE 3 — SERVICES: Diagram A: BA Service Engagement
def seq_services(uid="sv1"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "BA Service Engagement: Discovery -> Specification -> API/SQL -> UAT Handover")
    x_sp, x_ba, x_da, x_eng = 150, 430, 730, 1030
    f.actor(x_sp, 60, 390, "Client Leadership", "Sponsor")
    f.actor(x_ba, 60, 390, "BA Analysis & Scope", "Lead BA")
    f.actor(x_da, 60, 390, "Data Architecture", "Systems")
    f.actor(x_eng, 60, 390, "Engineering Delivery", "QA & Dev")

    f.msg(x_sp, 130, x_ba, 130, "defineBusinessOutcome()", num=1, dot=6)
    f.frag(60, 160, 1080, 170, "par", "Parallel Specification & Data Quality Profiling", operands=[
        (245, "Stream 2: Data Lineage")
    ])

    f.msg(x_ba, 190, x_eng, 190, "modelProcessSwimlanesAndSTTM()", dot=7)
    f.self_msg(x_ba, 275, 60, 35, "profileSourceData(100K+ rows SQL)")
    f.msg(x_ba, 350, x_eng, 350, "handoverUATScenarios(350+ cases)", num=2, dot=7)
    f.msg(x_eng, 390, x_sp, 390, "productionSignOff(Zero Defect Threshold)", dash=True, num=3, dot=6)
    f.note(770, 430, 270, 40, "Phases: Understand -> Specify -> Validate -> Handover")
    return f.render("sd-outer")


# 5. PAGE 3 — SERVICES: Diagram B: Enquiry Scoping, Confidentiality & Checkpoint Cadence
def seq_faq(uid="sv4"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Enquiry Scoping, Confidentiality (NDA) & Checkpoint Cadence")
    x_cl, x_ba, x_ws = 200, 600, 1000
    f.actor(x_cl, 60, 390, "Client Sponsor", "Client")
    f.actor(x_ba, 60, 390, "Gautam Reddy (BA)", "Consultant")
    f.actor(x_ws, 60, 390, "Secure Workspace", "Platform")

    f.msg(x_cl, 140, x_ba, 140, "submitProjectBrief()", num=1, dot=6)
    f.msg(x_ba, 190, x_cl, 190, "establishNDA()", num=2, dot=6)
    f.msg(x_ba, 250, x_ws, 250, "setupEncryptedWorkspace()", num=3, dot=7)
    f.self_msg(x_ba, 300, 65, 35, "alignCheckpointCadence(Weekly)")
    f.msg(x_ba, 360, x_ws, 360, "deliverReviewableArtifacts()", num=4, dot=7)
    f.msg(x_ws, 400, x_cl, 400, "reviewSpecificationPack(BRD/FRD/RTM)", dash=True, dot=6)
    return f.render("sd-outer")


# 6. PAGE 4 — PROJECTS: PayTrack Case Study & Analytics Portfolio Execution Sequence
def seq_projects(uid="pj1"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "PayTrack Case Study & Analytics Portfolio • End-to-End Execution Sequence")
    x_ops, x_rec, x_gw, x_db, x_exc = 120, 360, 600, 840, 1060
    f.actor(x_ops, 60, 390, "Ops Analyst", "Actor")
    f.actor(x_rec, 60, 390, "Recon Service", "Service")
    f.actor(x_gw, 60, 390, "Gateway Feeds", "External")
    f.actor(x_db, 60, 390, "Analytics DB", "Database")
    f.actor(x_exc, 60, 390, "Exception Case", "Workflow")

    f.msg(x_ops, 130, x_rec, 130, "triggerDailyBatchRecon(window='23:00 IST')", num=1, dot=6)
    f.msg(x_rec, 175, x_gw, 175, "streamNormalizedPayloads(100,000+ records)", num=2, dot=8)
    f.frag(60, 205, 1080, 215, "alt", "99.8% Straight-Through Match", operands=[
        (310, "createExceptionCase(alert_within='5 min', sla='4h')")
    ])

    f.msg(x_rec, 245, x_db, 245, "commitReconciledTxns(1,420 matched)", dot=7)
    f.msg(x_db, 280, x_ops, 280, "publishPowerBIDashboard(SLA: 99.8%)", dash=True, dot=6)
    f.msg(x_rec, 345, x_exc, 345, "raiseException(unmatched=3 txns)", dot=7)
    f.msg(x_exc, 385, x_ops, 385, "triageQueueAssigned(owner='Ops', sla='4h')", dash=True, dot=6)
    f.note(770, 435, 270, 38, "Zero unaccounted payment anomalies")
    return f.render("sd-outer")


# 7. PAGE 5 — RESUME: Diagram A: 4+ Years BA Delivery
def seq_resume(uid="rs"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "4+ Years BA Delivery")
    x_po, x_ba, x_dev, x_sc = 150, 430, 730, 1030
    f.actor(x_po, 60, 390, "Product Owners", "Stakeholders")
    f.actor(x_ba, 60, 390, "Gautam Reddy (BA)", "Core BA")
    f.actor(x_dev, 60, 390, "Engineering & QA", "Delivery")
    f.actor(x_sc, 60, 390, "Steering Committee", "Executive")

    f.msg(x_po, 130, x_ba, 130, "facilitateWorkshops(20+ sessions)", num=1, dot=6)
    f.self_msg(x_ba, 180, 60, 35, "authorBRD_FRD_STTM()")
    f.msg(x_ba, 250, x_dev, 250, "manageBacklogJira(User Stories + AC)", num=2, dot=7)
    f.msg(x_dev, 310, x_ba, 310, "sprintDemoVerification()", dash=True, dot=6)
    f.msg(x_ba, 370, x_sc, 370, "presentExecutiveStatus(100% Milestone Acceptance)", num=3, dot=7)
    f.note(770, 420, 270, 40, "Cross-functional BA leadership across 4+ years")
    return f.render("sd-outer")


# 8. PAGE 5 — RESUME: Diagram B: Quantitative Impact Verification (SQL & RCA)
def seq_resume_sql(uid="rs1"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Quantitative Impact Verification (SQL & RCA)")
    x_dw, x_sql, x_ba, x_ops = 160, 460, 760, 1040
    f.actor(x_dw, 60, 390, "Data Warehouse", "Database")
    f.actor(x_sql, 60, 390, "SQL Analysis Pipeline", "Engine")
    f.actor(x_ba, 60, 390, "Gautam Reddy (BA)", "Analyst")
    f.actor(x_ops, 60, 390, "Operations Team", "Stakeholders")

    f.msg(x_ba, 140, x_sql, 140, "queryTransactionDatasets(SELECT...JOIN)", num=1, dot=6)
    f.msg(x_sql, 190, x_dw, 190, "executeTelemetryQuery(100K+ records)", dot=7)
    f.msg(x_dw, 240, x_sql, 240, "returnBatchRecords()", dash=True, dot=6)
    f.msg(x_sql, 290, x_ba, 290, "analyzeTransactionLogs(100,000+ rows -> isolate 3 SLA breaches)", num=2, dot=8)
    f.self_msg(x_ba, 335, 60, 35, "rootCauseAnalysis(Fishbone + 5-Whys)")
    f.msg(x_ba, 390, x_ops, 390, "publishRootCauseActionPlan(SLA Breach Remediation)", num=3, dot=7)
    f.note(770, 435, 270, 38, "Reduced settlement exceptions by 18%")
    return f.render("sd-outer")


# 9. PAGE 5 — RESUME: Diagram C: Career Progression Sequence
def seq_resume_uat(uid="rs2"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Career Progression Sequence (Infocomm ASE -> BA -> V Moksha -> Marolix)")
    x_ase, x_iba, x_vm, x_mar = 150, 430, 730, 1030
    f.actor(x_ase, 60, 390, "Infocomm (ASE)", "Engineering")
    f.actor(x_iba, 60, 390, "Infocomm (BA)", "BA Transition")
    f.actor(x_vm, 60, 390, "V Moksha (BA)", "Integrations")
    f.actor(x_mar, 60, 390, "Marolix (Lead BA)", "Enterprise")

    f.note(180, 130, 190, 38, "Promoted Early to BA")
    f.msg(x_ase, 180, x_iba, 180, "transitionFromASE(Systems Analysis)", num=1, dot=6)
    f.msg(x_iba, 250, x_vm, 250, "leadPaymentGatewayIntegrations(2 APIs)", num=2, dot=7)
    f.msg(x_vm, 330, x_mar, 330, "coordinateUATAndTriage(350+ Marolix + 50+ Infocomm cases)", num=3, dot=8)
    f.self_msg(x_mar, 380, 55, 35, "executiveArchitectureLeadership()")
    f.note(770, 435, 270, 38, "400+ Total verified UAT test cases")
    return f.render("sd-outer")


# 10. PAGE 6 — CONTACT: Project & Role Enquiry Sequence
def seq_contact(uid="ct1"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "Project & Role Enquiry Sequence • Bengaluru (IST / UTC+5:30) <-> EMEA & US Overlap")
    x_ld, x_eb, x_ba, x_ds = 150, 430, 730, 1030
    f.actor(x_ld, 60, 390, "Hiring / Project Lead", "Actor")
    f.actor(x_eb, 60, 390, "Enquiry Builder", "UI Form")
    f.actor(x_ba, 60, 390, "Gautam Reddy (BA)", "Lead BA")
    f.actor(x_ds, 60, 390, "Discovery & Scope", "Engagement")

    f.msg(x_ld, 140, x_eb, 140, "selectServiceAndTimeline(?service=prefill)", num=1, dot=6)
    f.self_msg(x_eb, 190, 60, 35, "validateFieldsAndPrepareDraft(mailto + clipboard)", num=2)
    f.msg(x_ld, 270, x_ba, 270, "reviewAndSendEmailDraft()", dot=7)
    f.msg(x_ba, 340, x_ld, 340, "replyWithContextWithin1To2BusinessDays()", dash=True, num=3, dot=7)
    f.msg(x_ba, 390, x_ds, 390, "commenceDeliverables(Scope & RACI Defined)", num=4, dot=6)
    f.note(770, 435, 270, 38, "IST / UTC+5:30 • Overlap with EMEA & US morning")
    return f.render("sd-outer")


# 11. PAGE 7 — BA SAMPLES: PayTrack Case Study Traceability Sequence
def seq_samples(uid="sm1"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "PayTrack Case Study • End-to-End Artifact Traceability Sequence (Phases 01 -> 04)")
    x_1, x_2, x_3, x_4, x_5 = 120, 360, 600, 840, 1060
    f.actor(x_1, 60, 390, "01 Discovery MoM", "Phase 01")
    f.actor(x_2, 60, 390, "02 BRD & FRD", "Phase 02")
    f.actor(x_3, 60, 390, "03 BPMN/ERD/API", "Phase 03")
    f.actor(x_4, 60, 390, "04 User Stories", "Phase 04")
    f.actor(x_5, 60, 390, "05 RTM & UAT Plan", "Sign-Off")

    f.msg(x_1, 140, x_2, 140, "baselineScopeAndRACI()", num=1, dot=6)
    f.msg(x_2, 200, x_3, 200, "modelProcessSwimlanesAndERD()", num=2, dot=7)
    f.msg(x_3, 260, x_4, 260, "derivePrioritizedBacklog(MoSCoW + BDD)", num=3, dot=7)
    f.msg(x_4, 320, x_5, 320, "mapRequirementsToTestCatalogue(8 BRs -> 15 Test Cases)", num=4, dot=8)
    f.self_msg(x_5, 365, 50, 35, "consolidate35PageDocumentPack()")
    f.note(770, 435, 270, 38, "100% Traceability across all phases")
    return f.render("sd-outer")


# 12. PAGE 8 — 404: HTTP 404 Unmapped Endpoint Recovery Sequence
def seq_404(uid="nf"):
    f = Flow(uid, (1200, 520))
    f.sd_frame(40, 20, 1120, 480, "HTTP 404 • Unmapped Endpoint Detection & Specification Recovery Sequence")
    x_br, x_rt, x_fh, x_hub = 150, 450, 750, 1050
    f.actor(x_br, 60, 390, "Visitor Browser", "Client")
    f.actor(x_rt, 60, 390, "Route Specification", "Sitemap")
    f.actor(x_fh, 60, 390, "404 Fault Handler", "Router")
    f.actor(x_hub, 60, 390, "Portfolio Hub", "Index")

    f.msg(x_br, 130, x_rt, 130, "GET /unmapped-uri", num=1, dot=6)
    f.frag(60, 160, 1080, 240, "alt", "Route Missing from Sitemap Specification -> HTTP 404")
    f.msg(x_rt, 200, x_fh, 200, "dispatchUnmappedError(404)", dot=6)
    f.msg(x_fh, 260, x_br, 260, "renderDiagnosticRecoveryView()", dash=True, dot=7)
    f.msg(x_br, 330, x_hub, 330, "navigateToVerifiedArtifact()", num=2, dot=7)
    f.note(770, 430, 270, 38, "Zero dead-end navigation loops")
    return f.render("sd-outer")
