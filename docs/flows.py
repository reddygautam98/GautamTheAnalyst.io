"""Decorative business-analysis diagrams (BPMN-style flows, swimlanes, ERD, sequence, data pipeline).
Rendered as inline SVG that sits behind page sections. Purely decorative: aria-hidden."""
import html

class Flow:
    def __init__(s, uid, vb=(1200, 640)):
        s.uid, s.vb, s.parts, s.dots = uid, vb, [], []
    def _t(s, x, y, txt, cls="lb", anchor="middle"):
        return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{html.escape(txt)}</text>'
    def ev(s, x, y, label, end=False, r=15):
        s.parts.append(f'<g class="nd"><circle cx="{x}" cy="{y}" r="{r}" stroke-width="{4 if end else 1.6}"/>{s._t(x, y + r + 18, label)}</g>')
    def task(s, x, y, w, h, label, sub=None):
        t = s._t(x + w / 2, y + h / 2 + (-2 if sub else 4), label)
        if sub: t += s._t(x + w / 2, y + h / 2 + 14, sub, "sb")
        s.parts.append(f'<g class="nd"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>{t}</g>')
    def gate(s, x, y, label, k=34):
        s.parts.append(f'<g class="nd"><polygon points="{x},{y-k} {x+k},{y} {x},{y+k} {x-k},{y}"/>{s._t(x, y + 4, "?" , "lb")}{s._t(x, y - k - 8, label)}</g>')
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
        s.parts.append(f'<g class="lane"><rect x="20" y="{y}" width="{s.vb[0]-40}" height="{h}" rx="4"/><path d="M62,{y} v{h}"/><text class="sb" transform="translate(42,{y+h/2}) rotate(-90)" text-anchor="middle">{html.escape(label)}</text></g>')
    def edge(s, pts, dash=True, label=None, dot=None):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        s.parts.append(f'<path class="ln{"" if dash else " solid"}" d="{d}" marker-end="url(#a{s.uid})"/>')
        if label:
            x, y = pts[0]; s.parts.append(s._t(x + 8, y - 8, label, "sb", "start"))
        if dot: s.dots.append((d, dot))
    def curve(s, d, dot=None):
        s.parts.append(f'<path class="ln" d="{d}" marker-end="url(#a{s.uid})"/>')
        if dot: s.dots.append((d, dot))
    def render(s, cls=""):
        w, h = s.vb
        dots = "".join(f'<circle class="pk" r="4.5"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}"/></circle>' for d, dur in s.dots)
        return (f'<svg class="bgflow {cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
                f'<defs><marker id="a{s.uid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" class="ah"/></marker></defs>'
                + "".join(s.parts) + dots + '</svg>')

def lifecycle(uid="h"):
    f = Flow(uid, (1200, 640))
    f.ev(70, 130, "Request"); f.task(130, 100, 128, 60, "Elicit", "workshops"); f.task(310, 100, 140, 60, "Analyse", "gap + AS-IS/TO-BE")
    f.gate(540, 130, "Valid?"); f.task(630, 100, 140, 60, "Specify", "BRD / FRD"); f.task(820, 100, 128, 60, "Build + test", "UAT")
    f.ev(1040, 130, "Go-live", end=True)
    f.edge([(85, 130), (130, 130)]); f.edge([(258, 130), (310, 130)]); f.edge([(450, 130), (506, 130)], dot=7)
    f.edge([(574, 130), (630, 130)], label="yes"); f.edge([(770, 130), (820, 130)]); f.edge([(948, 130), (1025, 130)])
    f.task(470, 300, 140, 56, "Clarify", "stakeholders"); f.edge([(540, 164), (540, 300)], label="no")
    f.curve("M470,328 C360,328 220,300 194,162", dot=9)
    f.db(120, 470, "Source data"); f.task(280, 470, 130, 54, "SQL / Python", "validate"); f.bars(480, 462, "Insight", 100, 70)
    f.edge([(184, 497), (280, 497)], dot=6); f.edge([(410, 497), (480, 497)])
    f.doc(760, 470, "User stories"); f.task(900, 470, 130, 54, "RTM", "trace to tests"); f.edge([(830, 497), (900, 497)], dot=8)
    f.edge([(1030, 497), (1100, 497), (1100, 200)], dash=True)
    return f.render()

def swim(uid="s"):
    f = Flow(uid, (1200, 520))
    for i, n in enumerate(["Business", "BA", "Eng + QA"]): f.lane(40 + i * 150, 140, n)
    f.ev(110, 110, "Need", r=13); f.task(180, 80, 130, 56, "Raise request")
    f.task(360, 230, 150, 56, "Workshop", "elicit + prioritise"); f.task(570, 230, 150, 56, "Write BRD / FRD", "stories + AC")
    f.gate(820, 258, "Sign-off?"); f.task(900, 80, 140, 56, "Approve scope")
    f.task(900, 380, 150, 56, "Build + test", "RTM coverage"); f.ev(1130, 408, "Done", end=True, r=13)
    f.edge([(123, 108), (180, 108)]); f.edge([(310, 108), (435, 108), (435, 230)], dot=7)
    f.edge([(510, 258), (570, 258)]); f.edge([(720, 258), (786, 258)], dot=6)
    f.edge([(820, 224), (820, 108), (900, 108)], label="yes"); f.edge([(970, 136), (970, 160), (700, 160), (700, 230)], dash=True)
    f.edge([(820, 292), (820, 408), (900, 408)], label="rework")
    f.edge([(1050, 408), (1117, 408)])
    return f.render()

def erd(uid="e"):
    f = Flow(uid, (1200, 560))
    f.entity(80, 60, 200, "TRANSACTION", ["txn_id PK", "amount", "status", "gateway_ref FK"])
    f.entity(430, 40, 210, "GATEWAY_EVENT", ["event_id PK", "gateway_ref", "settled_at", "fee"])
    f.entity(800, 70, 220, "RECON_RESULT", ["result_id PK", "txn_id FK", "event_id FK", "match_state"])
    f.entity(260, 330, 210, "EXCEPTION_CASE", ["case_id PK", "result_id FK", "owner", "sla_due"])
    f.entity(700, 340, 220, "AUDIT_EVENT", ["audit_id PK", "case_id FK", "actor", "action"])
    f.edge([(280, 130), (430, 110)], dash=False); f.edge([(640, 110), (800, 130)], dash=False, dot=7)
    f.edge([(910, 200), (910, 260), (365, 260), (365, 330)], dot=9); f.edge([(470, 400), (700, 400)], dash=False)
    return f.render()

def seq(uid="q"):
    f = Flow(uid, (1200, 520))
    xs = [140, 400, 660, 920]
    for x, n in zip(xs, ["Client", "API", "Recon svc", "Gateway"]): f.life(x, 40, 420, n)
    f.edge([(140, 130), (396, 130)], label="POST /payments", dot=6); f.edge([(404, 180), (656, 180)], label="validate + queue")
    f.edge([(664, 230), (916, 230)], label="fetch settlement", dot=8); f.edge([(916, 290), (664, 290)], label="event")
    f.edge([(656, 340), (404, 340)], label="match result"); f.edge([(396, 390), (140, 390)], label="200 OK / status", dot=7)
    return f.render()

def pipeline(uid="p"):
    f = Flow(uid, (1200, 520))
    f.db(90, 120, "Sources"); f.db(90, 300, "Gateway logs")
    f.task(300, 160, 140, 58, "Extract", "SQL"); f.task(300, 290, 140, 58, "Clean", "Python / Pandas")
    f.task(540, 225, 150, 58, "Model + DAX", "KPI definitions"); f.bars(800, 190, "Dashboard", 110, 76)
    f.doc(1000, 200, "Insight", 80, 62)
    f.edge([(154, 147), (230, 147), (230, 189), (300, 189)], dot=7); f.edge([(154, 327), (230, 327), (230, 319), (300, 319)])
    f.edge([(440, 189), (490, 189), (490, 254), (540, 254)]); f.edge([(440, 319), (490, 319), (490, 254)], dot=8)
    f.edge([(690, 254), (800, 227)], dot=7); f.edge([(910, 228), (1000, 228)])
    f.ev(170, 440, "Define", r=11); f.task(260, 415, 120, 50, "Validate"); f.task(440, 415, 120, 50, "Reconcile"); f.task(620, 415, 120, 50, "Report")
    f.edge([(181, 440), (260, 440)]); f.edge([(380, 440), (440, 440)]); f.edge([(560, 440), (620, 440)], dot=6)
    return f.render()

def mini(uid):
    """tiny flow for project thumbnails / placeholders"""
    f = Flow(uid, (400, 200))
    f.ev(40, 100, "", r=9); f.task(80, 74, 80, 52, ""); f.gate(215, 100, "", k=26); f.task(268, 74, 90, 52, "")
    f.edge([(49, 100), (80, 100)]); f.edge([(160, 100), (189, 100)], dot=4); f.edge([(241, 100), (268, 100)])
    return f.render("mini")
