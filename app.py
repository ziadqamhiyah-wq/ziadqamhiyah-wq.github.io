# app.py
import os
import csv
import smtplib
from email.message import EmailMessage
from flask import Flask, Response, request, redirect, url_for

# -------------------------------------------------
# Find a 'static' folder (case-insensitive) near app.py
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_static_dir():
    candidates = []
    for up in range(0, 4):
        root = BASE_DIR
        for _ in range(up):
            root = os.path.dirname(root)
        for name in ("static", "Static", "STATIC"):
            candidates.append(os.path.join(root, name))
    for c in candidates:
        if os.path.isdir(c):
            return c
    return os.path.join(BASE_DIR, "static")

STATIC_DIR = find_static_dir()
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")

# Pick the first logo that actually exists
LOGO_CANDIDATES = ["logo.png","Logo.png","logo.jpeg","Logo.jpeg","logo.jpg","Logo.jpg"]
for _cand in LOGO_CANDIDATES:
    if os.path.isfile(os.path.join(STATIC_DIR, _cand)):
        LOGO_FILE = _cand
        break
else:
    LOGO_FILE = "logo.png"

# --- Background video detection ---
def find_video_file():
    preferred = [
        "Background.mp4","background.mp4",
        "Background.mov","background.mov",
        "Background.webm","background.webm",
        "Background.MP4","Background.MP4",
        "Background.MOV","Background.MOV",
        "Background.WEBM","Background.WEBM",
    ]
    for name in preferred:
        if os.path.isfile(os.path.join(STATIC_DIR, name)):
            return name
    try:
        for f in os.listdir(STATIC_DIR):
            lower = f.lower()
            if "background" in lower and os.path.splitext(lower)[1] in (".mp4",".mov",".webm"):
                return f
        for f in os.listdir(STATIC_DIR):
            if os.path.splitext(f.lower())[1] in (".mp4",".mov",".webm"):
                return f
    except Exception:
        pass
    return None

VIDEO_FILE = find_video_file()

def _video_mime(fname: str) -> str:
    ext = os.path.splitext(fname)[1].lower()
    return {".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm"}.get(ext, "video/mp4")

# --- Startup diagnostics ---
print("\n=== Static check ===")
print("Base dir:", BASE_DIR)
print("Static path:", STATIC_DIR, "| exists:", os.path.isdir(STATIC_DIR))
print("Using logo:", LOGO_FILE, "| exists:", os.path.isfile(os.path.join(STATIC_DIR, LOGO_FILE)))
print("Video file:", VIDEO_FILE)
print("====================\n")

BRAND = "ZEYATEK"

# ===================
# LIGHT THEME PALETTE (+ Apple-glass surfaces)
# ===================
BG       = "#f5f8fb"                 # soft white/blue
SURFACE  = "rgba(255,255,255,.34)"   # glass base
TEXT     = "#0c1526"                 # nearly-black text
MUTED    = "#4f6478"                 # cool grey-blue for secondary text
ACCENT   = "#2aa2ff"                 # energetic blue
ACCENT_2 = "#22c55e"                 # friendly green
BORDER   = "rgba(12,21,38,.14)"      # subtle dark-on-light border
SHADOW   = "0 12px 36px rgba(10,20,35,.10), inset 0 1px 0 rgba(255,255,255,.25)"

# -------------------
# Service content (long-form + outcomes + sustainability)
# -------------------
SERVICES = [
    {
        "slug": "smart-physical-security",
        "title": "Smart & Physical Security",
        "summary": "Computer vision, sensors, and access control integrated into a single operating picture.",
        "long_copy": """
<h3 style="margin:0 0 10px">Why smart and physical security matter now</h3>
<p>Security is no longer a set of isolated devices; it’s a living system. Cameras, access controllers, perimeter sensors, and IoT devices constantly generate signals about what’s happening across your facilities. When those signals are unified, you move from reactive investigation to proactive prevention—reducing incidents, addressing risk hot-spots, and protecting people and assets without adding operational drag.</p>
<p>As an IT company and a sales-enablement partner, our job is twofold: bring you the right options from multiple vendors and ensure they work as one. We evaluate video analytics, access governance, sensor telemetry, and command-and-control platforms for interoperability, standards compliance, and day-two operability—so you can scale without lock-in.</p>
<p>We focus on practical integration: camera streams with verified events, visitor logs joined with access rights, and environmental telemetry feeding alerting and reporting. The result is a single operating picture your teams can trust, with auditable trails for regulators and insurers.</p>
""",
        "value_title": "What we deliver",
        "bullets": [
            "Smart identification & tracking (AI video analytics, people/vehicle recognition)",
            "Access control & visitor management integrated with identity directories",
            "Perimeter & intrusion detection with verified events and escalation",
            "Facility, fleet, and city monitoring with IoT / IIoT telemetry",
            "Unified dashboards and evidence trails for audits and investigations",
        ],
        "outcomes_title": "Measured outcomes",
        "outcomes": [
            "Incident triage in ≤60 seconds for priority events with verified evidence.",
            "20–35% reduction in false alarms after analytic tuning and policy hardening.",
            "Audit-ready visitor and access logs with 100% coverage on enrolled sites.",
            "Operator workload reduced by automating repetitive patrol/monitoring tasks.",
        ],
        "sustain_title": "Sustainable operations",
        "sustain_points": [
            "Runbooks for alarm triage, escalation, and evidence handling.",
            "Lifecycle plans for cameras, controllers, firmware, and certificates.",
            "Open standards (ONVIF, RTSP, OPC-UA) to avoid vendor lock-in.",
            "Quarterly tuning of analytics and policies against incident data.",
        ]
    },
    {
        "slug": "cybersecurity",
        "title": "Cybersecurity",
        "summary": "Practical defense across identity, data, applications, network, and endpoints—built for day-two operations.",
        "long_copy": """
<h3 style="margin:0 0 10px">Why cybersecurity matters—and how we help</h3>
<p>Every critical workflow now runs on a network of applications, APIs, and devices. Threats target each layer: stolen credentials, unpatched services, unsafe defaults, and exposed data. A breach isn’t only a technical event—it’s a trust, regulatory, and business-continuity event.</p>
<p>We design cybersecurity that aligns to business priorities. Data classification drives controls; identity and least-privilege reduce blast radius; segmentation and patch cadence shrink the attack surface; continuous monitoring with clear playbooks speeds containment and recovery. Our multi-proposal model gives you a choice of leading tools and services—balanced for performance, cost, and operational reality.</p>
<p>From zero-trust network zones to application security (SAST/DAST/SCA), EDR/MDR on endpoints, and SIEM/SOAR for detection and response, we integrate controls into the way your teams work—so security strengthens velocity instead of slowing it.</p>
""",
        "value_title": "What we deliver",
        "bullets": [
            "Data security & DLP aligned to classification and retention",
            "AppSec pipelines (SAST/DAST/SCA) with gating and fixes tracked",
            "Zero-trust segmentation, IPS, and privileged access controls",
            "Endpoint hardening with EDR/MDR and patch policy by tier",
            "Threat monitoring, use-cases, and incident runbooks in SIEM/SOAR",
        ],
        "outcomes_title": "Measured outcomes",
        "outcomes": [
            "MTTD/MTTR reduced to hours (not days) for priority incident classes.",
            "≥90% patch compliance on in-scope assets within policy windows.",
            "Material reduction in exposed attack surface via least-privilege and segmentation.",
            "Audit evidence auto-collected for controls, changes, and incidents.",
        ],
        "sustain_title": "Sustainable managed security",
        "sustain_points": [
            "Quarterly control reviews and threat-led testing against your crown jewels.",
            "Playbooks with owners, RACI, and tabletop exercises—kept current.",
            "Continuous tuning of detections to cut noise and improve precision.",
            "Vendor-agnostic stack with exit paths and cost transparency.",
        ]
    },
    {
        "slug": "data-ai",
        "title": "Data & AI",
        "summary": "Reliable data pipelines, governed catalogs, and production ML where it makes sense.",
        "long_copy": """
<h3 style="margin:0 0 10px">Why data & AI matter</h3>
<p>Data is the raw material of decision-making; AI turns it into leverage. When pipelines are reliable and governed, leaders trust the numbers. When automation and ML are applied where they truly fit, teams reclaim time and customers get better experiences.</p>
<p>We help you move from scattered sources to governed, documented datasets with lineage. We implement RPA for repetitive steps, and apply ML to use-cases with measurable benefit (forecasting, prioritization, classification). Everything is built with monitoring, rollback, and cost controls—so production stays predictable.</p>
<p>As a sales-enablement partner, we bring you multiple platform options (warehouses, lakes, BI, orchestration, MLOps) and help you choose based on scale, skills, and TCO—no lock-in.</p>
""",
        "value_title": "What we deliver",
        "bullets": [
            "Data platform foundations (lake/warehouse) with governance & lineage",
            "ELT/ETL pipelines with tests, SLAs, and observability",
            "Analytics dashboards & KPIs mapped to source of truth",
            "RPA + ML for back-office and customer operations",
            "MLOps for deployment, monitoring, and rollback",
        ],
        "outcomes_title": "Measured outcomes",
        "outcomes": [
            "25–40% reduction in back-office task time via automation.",
            "Forecast accuracy improved (use-case dependent) with transparent metrics.",
            "Single catalog of certified datasets with column-level lineage.",
            "Time-to-insight reduced from weeks to hours for governed reports.",
        ],
        "sustain_title": "Sustaining value",
        "sustain_points": [
            "Data contracts and SLAs; alerts for freshness, volume, and schema drift.",
            "Model monitoring for performance, bias, and cost; controlled retraining.",
            "Versioned transformations and reproducible environments.",
            "Usage analytics to prune unused datasets and dashboards.",
        ]
    },
    {
        "slug": "apps-platforms",
        "title": "Apps & Platforms",
        "summary": "Product-grade web/mobile software and enterprise platforms that are supportable on day one.",
        "long_copy": """
<h3 style="margin:0 0 10px">Why applications & platforms matter</h3>
<p>Your applications are how customers experience your business and how your teams get work done. Modern, resilient platforms shorten time-to-market, reduce operating costs, and make change safer.</p>
<p>We build and modernize apps with CI/CD, automated testing, and infrastructure as code—so environments can be recreated predictably. We stabilize legacy platforms with observability, SLOs, and on-call runbooks. And we keep enterprise platform customizations minimal, documented, and upgrade-safe.</p>
<p>Because we also operate as a sales-enablement partner, you’ll see multiple credible delivery options (frameworks, clouds, toolchains) before you commit—optimizing for fit, speed, and TCO.</p>
""",
        "value_title": "What we deliver",
        "bullets": [
            "Custom web/mobile development with CI/CD and test automation",
            "Cloud migration and refactoring with infra-as-code",
            "Platform work (Dynamics, SAP, Oracle) with upgrade-safe extensions",
            "Observability (metrics, logs, traces) mapped to user journeys",
            "SRE practices with incident/rollback playbooks and error budgets",
        ],
        "outcomes_title": "Measured outcomes",
        "outcomes": [
            "Deployment lead time in minutes with safe rollback paths.",
            "Release pace tied to error-budget policy (faster when healthy, slower when not).",
            "Upgrade cycles completed without disrupting core processes.",
            "15–30% performance gains from targeted refactors and caching.",
        ],
        "sustain_title": "Sustainable delivery at scale",
        "sustain_points": [
            "Module boundaries, API versioning, and contract testing to prevent breakage.",
            "Golden pipelines and templates; secure defaults by design.",
            "Automated regression suites keep velocity high as systems grow.",
            "Architecture reviews ensure changes align to standards and guardrails.",
        ]
    },
    {
        "slug": "infrastructure-networking",
        "title": "Infrastructure & Networking",
        "summary": "From cabling and WAN to cloud foundations and data centers—built for capacity, resilience, and scale.",
        "long_copy": """
<h3 style="margin:0 0 10px">Why infrastructure & networking matter</h3>
<p>Everything runs on the foundation. Networks, data centers, and cloud landing zones determine performance, resilience, and the true cost of operations. When capacity, segmentation, and automation are right, applications behave—and teams deliver more with less effort.</p>
<p>We design campus/branch/WAN and cloud foundations with quality of service, segmentation, and golden templates. We right-size power, cooling, and capacity; automate builds; and document IP plans, labels, diagrams, and failover tests—so operations are boring (in the best way).</p>
<p>For migrations, we orchestrate cutovers with rollback plans and acceptance tests—minimizing downtime and surprises.</p>
""",
        "value_title": "What we deliver",
        "bullets": [
            "Campus, branch, WAN, and SD-WAN design & implementation",
            "Cloud & hybrid landing zones with secure defaults",
            "Data-center design, migration, and capacity planning",
            "Structured cabling, racks, AV/meeting rooms",
            "Automation with templates for repeatable builds",
        ],
        "outcomes_title": "Measured outcomes",
        "outcomes": [
            "40–60% downtime reduction via redundancy and tested failover.",
            "20–35% network performance increase through architecture optimization.",
            "Provisioning time cut from weeks to days with automation and templates.",
            "Cost-per-user lowered 15–25% via centralized management and policy.",
        ],
        "sustain_title": "Operational sustainability",
        "sustain_points": [
            "Quarterly failover tests and capacity reviews with action tracking.",
            "Template-driven config; drift reports and standardized baselines.",
            "Documentation in version control: IP plans, diagrams, cabling maps.",
            "Change windows with pre-checks and staged rollouts.",
        ]
    },
    {
        "slug": "advisory-growth",
        "title": "Advisory & Growth",
        "summary": "Driving Transformation with Precision and Impact.",
        "long_copy": """<h3 style="margin:0 0 8px">Driving Transformation with Precision and Impact</h3>
<p>We partner with leaders to build the business case, define the vision, and execute the roadmap for digital and IT transformation. From identifying strategic opportunities and aligning with corporate objectives to designing future-ready operating models, we deliver the data, insights, and solutions to compete in a digital-first world.</p>
<p>Our approach blends rigorous strategy with flawless execution—defining key success factors, mobilizing the right teams and budgets, and selecting initiatives that maximize ROI. We integrate robust IT strategies, resilient architectures, and sourcing models that optimize performance while reducing costs.</p>
<p><strong>What this looks like in practice:</strong> technology advisory that turns strategy into a funded portfolio; digital modernization programs with clear milestones and risk controls; go-to-market support that strengthens brand and demand; and the operating muscle to run social and content programs that sustain growth.</p>
<p><strong>Result:</strong> a transformation journey that is prioritized, funded, and executed with precision—turning strategic vision into operational reality.</p>""",
        "value_title": "Why it matters",
        "bullets": [
            "Technology Advisory",
            "Digital Modernization",
            "Online Marketing & Brand",
            "Social Media Operations",
            "Content Production",
        ],
        "sustain_title": "Governance & Value Realization",
        "sustain_points": [
            "Benefits cases with KPIs, baselines, and target dates tracked to closure.",
            "Transformation PMO cadence: weekly delivery standups, monthly steering, quarterly value reviews.",
            "Architecture & security guardrails: reference patterns and reusable templates.",
            "Stage-gated funding with ROI checkpoints and cost transparency.",
        ]
    },
]
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# Image mapping
SERVICE_IMAGES = {
    "smart-physical-security": "CCTV.png",
    "cybersecurity": "CYBER.png",
    "data-ai": "AI.png",
    "apps-platforms": "Apps.png",
    "infrastructure-networking": "network.png",
    "advisory-growth": "advisory-growth.png",
}

# -------------------
# ARTICLES (mock data)
# -------------------
ARTICLES = [
    {
        "slug": "winning-it-rfps",
        "title": "Winning IT RFPs: How to Present Multiple Best-Fit Options Without Confusing Buyers",
        "author": "GoPartnerr Editorial",
        "date": "Aug 12, 2025",
        "reading_time": "6 min",
        "image": "article1.jpg",
        "tags": ["Sales Enablement", "B2B Proposals", "Procurement"],
        "excerpt": "Buyers hate ‘either-or’ choices. Here’s a practical method to shortlist, compare, and present three credible options—so stakeholders see value and pick faster.",
        "body": [
            "<p>Most proposals collapse good alternatives into a single ‘recommended’ path. That feels decisive—but it hides tradeoffs that matter to different stakeholders.</p>",
            "<h3>Start with outcomes, not products</h3><p>Tie each option to the business outcome, acceptance criteria, and risks you can actively mitigate.</p>",
            "<h3>Scorecards that fit on one slide</h3><p>Keep attributes consistent: cost, time-to-value, interoperability, day-2 run cost, and exit paths.</p>",
            "<figure><img src='/static/article-inline1.jpg' alt='Scorecard example' style='width:100%;border-radius:12px;border:1px solid rgba(12,21,38,.14)'><figcaption>Lightweight scorecards speed up steering decisions.</figcaption></figure>",
            "<p>Close with a funded next step, not a generic CTA. Convert energy into momentum.</p>"
        ]
    },
    {
        "slug": "securing-ot-environments",
        "title": "Securing OT Environments Without Slowing Operations",
        "author": "GoPartnerr Editorial",
        "date": "Aug 05, 2025",
        "reading_time": "7 min",
        "image": "article2.jpg",
        "tags": ["Cybersecurity", "OT/ICS", "Zero Trust"],
        "excerpt": "Identity, segmentation, patch cadence, and safe change windows—four moves that harden plants without breaking production.",
        "body": [
            "<p>OT environments prioritize availability. The trick is raising security posture without hurting throughput or quality.</p>",
            "<h3>Segment by consequence, not by org chart</h3><p>Define zones around process-critical assets and design least-privilege pathways.</p>",
            "<h3>Patch policy by tier</h3><p>Set cadence and windows by risk tier, with tested rollback plans.</p>"
        ]
    },
    {
        "slug": "data-contracts-in-practice",
        "title": "Data Contracts in Practice: Keeping Dashboards Honest",
        "author": "GoPartnerr Editorial",
        "date": "Jul 28, 2025",
        "reading_time": "5 min",
        "image": "article3.jpg",
        "tags": ["Data & AI", "Governance", "Analytics"],
        "excerpt": "Dashboards drift when schemas drift. Data contracts align producers and consumers so KPIs don’t quietly rot.",
        "body": [
            "<p>Agree on shape, freshness, and ownership. Automate checks. Alert on drift. That’s the contract.</p>",
            "<h3>What to codify</h3><p>Columns, types, nullability, volumes, freshness, and lineage expectations.</p>"
        ]
    },
    {
        "slug": "modernize-legacy-platforms",
        "title": "Modernizing Legacy Platforms Without a Big-Bang Rewrite",
        "author": "GoPartnerr Editorial",
        "date": "Jul 16, 2025",
        "reading_time": "8 min",
        "image": "article4.jpg",
        "tags": ["Apps & Platforms", "Refactoring", "Cloud"],
        "excerpt": "Strangle patterns, golden pipelines, and error budgets—how to move fast while staying safe.",
        "body": [
            "<p>Big bangs are risky. Incremental modernization lets teams ship value continuously.</p>",
            "<h3>Map user journeys to SLOs</h3><p>Budget reliability to guard velocity. Slow down when error budget burns.</p>"
        ]
    },
]

ARTICLE_BY_SLUG = {a["slug"]: a for a in ARTICLES}

# -------------------
# Email (optional). CSV saving always on.
# -------------------
TO_EMAIL = os.environ.get("GOPARTNERR_TO", "info@gopartnerr.com")
SMTP_HOST = os.environ.get("GOPARTNERR_SMTP_HOST")
SMTP_PORT = int(os.environ.get("GOPARTNERR_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("GOPARTNERR_SMTP_USER")
SMTP_PASS = os.environ.get("GOPARTNERR_SMTP_PASS")

def send_lead_email(name, email, message):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS):
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = f"New Lead — {BRAND}"
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls(); s.login(SMTP_USER, SMTP_PASS); s.send_message(msg)
        return True
    except Exception:
        return False

def save_lead_csv(name, email, message):
    path = "leads.csv"; new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["Name", "Email", "Message"])
        w.writerow([name, email, message])

# -------------------
# HTML helpers
# -------------------
def head(title, description=""):
    # Sora for bold headlines, Manrope for body
    fonts = f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
"""
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title><meta name="description" content="{description}"/>
{fonts}
<style>
:root {{
  --bg:{BG}; --surface:{SURFACE}; --text:{TEXT}; --muted:{MUTED};
  --accent:{ACCENT}; --accent2:{ACCENT_2}; --border:{BORDER}; --shadow:{SHADOW};
  --r:18px; --container:1100px;
}}
* {{ box-sizing:border-box }}
html {{ scroll-behavior:smooth }}
body {{
  margin:0; color:var(--text);
  font-family: Manrope, ui-sans-serif, -apple-system, "Segoe UI", Roboto, Arial, "Noto Sans", sans-serif;
  letter-spacing:.1px;
  background:
    radial-gradient(1100px 650px at 10% 0%, rgba(42,162,255,.18), transparent 60%),
    radial-gradient(1000px 540px at 90% 10%, rgba(34,197,94,.14), transparent 60%),
    var(--bg);
}}
p {{ line-height:1.65; font-size:18px }}
a {{ color:inherit; text-decoration:none }}
.container {{ max-width:var(--container); margin:0 auto; padding:0 20px }}

/* Apple-glass core */
.glass {{
  position:relative;
  background: var(--surface);
  border: 1px solid var(--border);
  backdrop-filter: blur(18px) saturate(160%);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  box-shadow: var(--shadow);
  border-radius: var(--r);
}}
.glass::before {{
  content:"";
  position:absolute; inset:0;
  border-radius: inherit;
  background:
    radial-gradient(140% 80% at 10% -10%, rgba(255,255,255,.45), rgba(255,255,255,0) 40%),
    radial-gradient(80% 60% at 100% 120%, rgba(42,162,255,.18), rgba(255,255,255,0) 50%);
  pointer-events:none;
  mix-blend-mode: screen;
}}
.glass::after {{
  content:"";
  position:absolute; inset:0;
  border-radius: inherit;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.35), inset 0 -1px 12px rgba(0,0,0,.06);
  pointer-events:none;
}}

header.top {{
  position:sticky; top:0; z-index:50;
  background:rgba(255,255,255,.55);
  backdrop-filter:saturate(120%) blur(8px);
  border-bottom:1px solid var(--border);
}}
.nav {{ height:68px; display:flex; align-items:center; justify-content:space-between }}
.brand {{ display:flex; gap:12px; align-items:center; font-weight:900; letter-spacing:.2px }}
.brand img {{ height:28px; width:auto; border-radius:8px; box-shadow:0 0 0 1px var(--border) }}
.brand span {{ color:var(--text) }}
.menu {{ display:flex; gap:24px; align-items:center }}
.menu a {{ color:var(--muted); font-weight:700; opacity:.95 }}
.menu a:hover {{ color:#0c1526 }}
.menu .btn {{
  padding:10px 16px; border-radius:999px; background:var(--accent); color:#fff; font-weight:900;
}}

.hero {{
  position:relative; min-height:58vh; display:grid; place-items:center;
  background:
    linear-gradient(180deg, rgba(0,0,0,.00), rgba(0,0,0,.00)),
    radial-gradient(1000px 500px at 70% 10%, rgba(42,162,255,.10), transparent 60%);
  overflow:hidden;
}}
.hero::before {{
  content:""; position:absolute; inset:0; z-index:1;
  background:url('{url_for('static', filename='hero.jpg')}') center/cover no-repeat;
  opacity:.12;
}}
.hero.has-video::before {{ background:none }}
.hero .hero-bg{{position:absolute;inset:0;z-index:0;overflow:hidden}}
.hero .hero-video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none;filter:brightness(.98)}}
.hero-inner {{ position:relative; width:100%; z-index:2 }}
h1.display {{
  font-family: Sora, Manrope, ui-sans-serif;
  color:var(--text);
  font-size: clamp(40px, 6.4vw, 72px);
  line-height:1.03; margin:0 0 14px; letter-spacing:.05px; font-weight:800;
}}
.h2 {{
  font-family: Sora, Manrope, ui-sans-serif;
  color:var(--text);
  font-size: clamp(26px, 4.4vw, 42px);
  font-weight:800;
  margin:8px 0 8px;
}}
.lead {{ color:var(--muted); font-size:clamp(16px,2.4vw,20px); max-width:820px }}
.cta {{ margin-top:22px; display:flex; gap:12px; flex-wrap:wrap }}
.btn {{
  display:inline-flex; gap:10px; align-items:center; padding:12px 18px; border-radius:14px;
  font-weight:900; border:1px solid var(--border);
}}
.btn.primary {{ background:var(--accent); color:#fff; border-color:transparent }}
.btn.ghost {{ background:transparent; color:#0c1526 }}

/* Operations band (carousel) */
.band {{
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
  padding:56px 0; position:relative;
  background:linear-gradient(180deg, rgba(255,255,255,.60), rgba(255,255,255,.00));
}}
.ops-wrap {{ display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:14px; }}
.ops-arrow.outside {{
  width:44px; height:44px; border-radius:999px;
  border:1px solid var(--border); background:rgba(255,255,255,.85); color:var(--text); font-weight:900;
}}
.ops-arrow.outside:disabled {{ opacity:.4 }}
.ops-carousel {{ position:relative; }}
.ops-stage {{ position:relative; min-height:380px }}
.ops-slide {{
  position:absolute; inset:0; opacity:0; transition:opacity .55s ease; pointer-events:none;
  display:grid; gap:22px; grid-template-columns:1.1fr .9fr;
}}
.ops-slide.active {{ opacity:1; pointer-events:auto }}
@media (max-width:960px) {{ .ops-slide {{ grid-template-columns:1fr }} }}
.ops-visual {{ min-height:280px; border-radius:12px; }}
.ops-visual .glass {{ height:100%; }}

/* Carousel dots */
.ops-controls {{ display:flex; justify-content:center; gap:10px; margin-top:12px }}
.ops-dot {{
  width:9px; height:9px; border-radius:999px; border:1px solid rgba(0,0,0,.35);
  background:transparent; transform:scale(.98); transition:all .25s;
}}
.ops-dot[aria-current="true"] {{ background:var(--accent); border-color:transparent; transform:scale(1.05) }}

/* Tighter, flawless typography only inside ops slides */
.ops-slide .h2 {{ font-size: clamp(24px, 3.8vw, 38px); }}
.ops-slide .lead {{ font-size: clamp(15px, 2.2vw, 18px); line-height: 1.5; }}
.ops-bullets li {{ margin:6px 0; font-size:16px; }}

/* Services grid */
section.services {{ padding:72px 0 }}
.cards {{ display:grid; gap:18px; grid-template-columns:repeat(3,1fr) }}
@media (max-width:1050px) {{ .cards {{ grid-template-columns:repeat(2,1fr) }} }}
@media (max-width:680px) {{ .cards {{ grid-template-columns:1fr }} }}

/* TRUE Apple Glass cards (refined sizing) */
.card {{
  position:relative; padding:22px; display:flex; flex-direction:column; gap:12px;
  border-radius: var(--r);
  background: linear-gradient(180deg, rgba(255,255,255,.55), rgba(255,255,255,.25));
  border:1px solid var(--border);
  backdrop-filter: blur(22px) saturate(180%);
  -webkit-backdrop-filter: blur(22px) saturate(180%);
  box-shadow: 0 18px 40px rgba(10,20,35,.12), inset 0 1px 0 rgba(255,255,255,.45);
  overflow:hidden;
  transform: translateZ(0);
}}
.card::before {{
  content:""; position:absolute; inset:-1px; border-radius:inherit;
  background:
    radial-gradient(120% 70% at -10% -10%, rgba(255,255,255,.65), rgba(255,255,255,0) 45%),
    radial-gradient(80% 60% at 110% 120%, rgba(42,162,255,.22), rgba(255,255,255,0) 55%);
  mix-blend-mode: screen; pointer-events:none;
}}
.card::after {{
  content:""; position:absolute; inset:0; border-radius:inherit;
  box-shadow: inset 0 -20px 40px rgba(0,0,0,.05);
  pointer-events:none;
}}
.card:hover {{
  box-shadow: 0 24px 60px rgba(10,20,35,.16), inset 0 1px 0 rgba(255,255,255,.5);
  transform: translateY(-2px);
}}
.card img {{ width:100%; height:220px; object-fit:cover; border-radius:12px; border:1px solid var(--border) }}
.card h3 {{
  font-family: Sora, Manrope, ui-sans-serif;
  color:var(--text); margin:4px 0 2px; font-weight:800; letter-spacing:.1px;
}}
.card p {{ color:var(--muted); margin:0 0 6px }}
.card .chips {{ margin-top:6px }}
.chip {{
  display:inline-block; margin:.35rem .35rem 0 0; padding:.45rem .75rem; border-radius:999px;
  background:rgba(42,162,255,.15); border:1px solid rgba(42,162,255,.35); font-weight:800; color:#0b3d66;
}}

/* Long-form service prose */
.prose {{ padding: 28px; }}
.prose h3 {{
  font-family: Sora, Manrope, ui-sans-serif;
  margin:0 0 10px; font-weight:800
}}
.prose p + p {{ margin-top:12px }}

/* Value & Outcomes blocks */
.value, .outcomes, .sustain {{ padding:18px }}
.value h3, .outcomes h3, .sustain h3 {{
  font-family: Sora, Manrope, ui-sans-serif;
  color:var(--text); margin:0 0 8px; font-weight:800
}}
.value ul, .outcomes ul, .sustain ul {{ margin:10px 0 0 18px; color:var(--muted); line-height:1.6 }}
.value li, .outcomes li, .sustain li {{ margin:.35rem 0 }}

/* Stories */
section.stories {{ padding:72px 0; border-top:1px solid var(--border) }}
.story {{ display:grid; gap:18px; grid-template-columns:1.2fr .8fr; align-items:center; }}
@media (max-width:960px) {{ .story {{ grid-template-columns:1fr }} }}
.story img {{ width:100%; border-radius:12px; border:1px solid var(--border) }}
blockquote {{ margin:0; font-size:18px; color:#0c1526 }}

/* Articles */
.articles-hero {{
  min-height:32vh;
  display:grid; place-items:center;
  background:
    radial-gradient(900px 400px at 10% 0%, rgba(42,162,255,.14), transparent 60%),
    radial-gradient(900px 500px at 90% 20%, rgba(34,197,94,.12), transparent 60%);
}}
.article-grid {{ display:grid; gap:18px; grid-template-columns:repeat(3,1fr) }}
@media (max-width:1050px) {{ .article-grid {{ grid-template-columns:repeat(2,1fr) }} }}
@media (max-width:680px) {{ .article-grid {{ grid-template-columns:1fr }} }}
.article-card .meta {{
  display:flex; gap:10px; flex-wrap:wrap; font-size:13px; color:var(--muted)
}}
.article-card .tags {{ margin-top:4px }}
.tag {{
  display:inline-block; margin:.25rem .35rem 0 0; padding:.35rem .6rem; border-radius:999px;
  background:rgba(12,21,38,.05); border:1px solid var(--border); font-weight:800; font-size:12px; color:#213348;
}}
.article-header img {{
  width:100%; height:420px; object-fit:cover; border-radius:16px; border:1px solid var(--border)
}}
.article-body {{ max-width:930px; margin:0 auto; }}
.article-body figure {{ margin:14px 0 }}
.article-body figcaption {{ font-size:13px; color:var(--muted); margin-top:6px }}
.share-row {{ display:flex; gap:10px; flex-wrap:wrap }}
.share-row .btn {{ font-size:14px; padding:10px 14px }}

/* Contact */
.cta-band {{ padding:56px 0; border-top:1px solid var(--border) }}
form.contact {{ display:grid; grid-template-columns:1fr 1fr; gap:12px }}
form.contact input, form.contact textarea {{
  background:rgba(255,255,255,.55); color:var(--text);
  border:1px solid var(--border); border-radius:12px; padding:12px;
  backdrop-filter: blur(8px) saturate(120%);
}}
form.contact input::placeholder, form.contact textarea::placeholder {{ color:rgba(79,100,120,.75) }}
form.contact input:focus, form.contact textarea:focus {{ outline:none; border-color:var(--accent) }}
form.contact textarea {{ grid-column:1/-1; min-height:220px }}
form.contact .actions {{ grid-column:2; justify-self:end }}

/* Footer */
footer {{ padding:38px 0 60px; color:var(--muted); border-top:1px solid var(--border) }}
.footer-grid {{ display:grid; gap:18px; grid-template-columns:1.4fr 1fr 1fr 1fr }}
@media (max-width:900px) {{ .footer-grid {{ grid-template-columns:1fr 1fr }} }}
@media (max-width:600px) {{ .footer-grid {{ grid-template-columns:1fr }} }}
.footer-grid a {{ color:var(--muted) }}
.footer-grid a:hover {{ color:#0c1526 }}

/* Back to top */
#topBtn {{
  position:fixed; right:18px; bottom:18px; padding:10px 12px; border-radius:12px;
  border:1px solid var(--border); background:rgba(255,255,255,.98); color:var(--text); display:none
}}
#topBtn.show {{ display:inline-flex }}
</style></head>"""

def header_nav():
    return f"""
<body>
<header class="top">
  <div class="container nav">
    <div class="brand">
      <img src="{url_for('static', filename=LOGO_FILE)}" alt="{BRAND} Logo">
      <span>{BRAND}</span>
    </div>
    <nav class="menu" aria-label="Main navigation">
      <a href="/#services">Services</a>
      <a href="/#platform">Operations</a>
      <a href="/#stories">Why GoPartnerr</a>
      <a href="/articles">Articles</a>
      <a class="btn" href="/#contact">Talk to sales</a>
    </nav>
  </div>
</header>
"""

def footer_block():
    html = f"""
<footer>
  <div class="container footer-grid">
    <div>
      <div class="brand" style="margin-bottom:8px">
        <img src="{url_for('static', filename=LOGO_FILE)}" alt="{BRAND} Logo">
        <span>{BRAND}</span>
      </div>
      <div>© <span id="year"></span> {BRAND}. All rights reserved.</div>
    </div>
    <div>
      <strong>Explore</strong><br>
      <a href="/#services">Services</a><br>
      <a href="/#platform">Operations</a><br>
      <a href="/#stories">Customer stories</a>
    </div>
    <div>
      <strong>Company</strong><br>
      <a href="/">Home</a><br>
      <a href="/articles">Articles</a><br>
      <a href="/#contact">Contact</a>
    </div>
    <div>
      <strong>Legal</strong><br>
      <a href="#">Privacy</a><br>
      <a href="#">Terms</a>
    </div>
  </div>
</footer>
<a id="topBtn" href="#home" aria-label="Back to top">↑</a>
"""
    # Includes Operations carousel JS (15s loop)
    script = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('year').textContent = new Date().getFullYear();
  const topBtn = document.getElementById('topBtn');
  document.addEventListener('scroll', function () {
    if (window.scrollY > 400) topBtn.classList.add('show'); else topBtn.classList.remove('show');
  });

  const hv = document.querySelector('.hero-video');
  if (hv) {
    try { hv.muted = true; } catch(e){}
    try { hv.setAttribute('muted',''); hv.setAttribute('playsinline',''); hv.setAttribute('webkit-playsinline',''); } catch(e){}
    const p = hv.play && hv.play();
    if (p && p.catch) { p.catch(()=>{}); }
  }

  const stage = document.querySelector('.ops-stage');
  const slides = stage ? Array.from(stage.querySelectorAll('.ops-slide')) : [];
  const dots   = Array.from(document.querySelectorAll('.ops-dot'));
  const left   = document.querySelector('.ops-arrow.left');
  const right  = document.querySelector('.ops-arrow.right');
  const INTERVAL = 15000;

  if (!stage || !slides.length) return;

  let index = 0, timer = null;

  function setHeight() {
    const h = Math.max(...slides.map(s => { s.style.position = 'static'; return s.offsetHeight; }));
    slides.forEach(s => s.style.position = 'absolute');
    stage.style.height = h + 'px';
  }

  function go(i) {
    index = (i + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('active', k === index));
    dots.forEach((d, k) => d.setAttribute('aria-current', k === index ? 'true' : 'false'));
    resetTimer();
  }

  function resetTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(() => go(index + 1), INTERVAL);
  }

  slides.forEach(s => s.classList.remove('active'));
  slides[0].classList.add('active');
  dots.forEach((d, k) => d.addEventListener('click', () => go(k)));
  if (left)  left.addEventListener('click', () => go(index - 1));
  if (right) right.addEventListener('click', () => go(index + 1));
  document.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') go(index - 1); if (e.key === 'ArrowRight') go(index + 1); });

  stage.addEventListener('mouseenter', () => { if (timer) clearInterval(timer); });
  stage.addEventListener('mouseleave', resetTimer);

  document.addEventListener('visibilitychange', () => { if (document.hidden) { if (timer) clearInterval(timer); } else { resetTimer(); } });

  setHeight();
  window.addEventListener('resize', setHeight);
  resetTimer();
});
</script>
</body></html>
"""
    return html + script

def hero_section():
    has_video = bool(VIDEO_FILE)
    video_html = ""
    if has_video:
        video_html = f"""
    <div class="hero-bg" aria-hidden="true">
      <video class="hero-video" autoplay muted loop playsinline webkit-playsinline preload="auto"
             poster="{url_for('static', filename='hero.jpg')}">
        <source src="{url_for('static', filename=VIDEO_FILE)}" type="{_video_mime(VIDEO_FILE)}">
      </video>
    </div>
    """
    return f"""
<section id="home" class="hero{' has-video' if has_video else ''}">
  {video_html}
  <div class="container hero-inner">
    <h1 class="display">Transforming the Systems You Rely On Into the Engines That Drive Tomorrow.</h1>
    <p class="lead">Your trusted sales enablment partner for the IT industry.</p>
    <div class="cta">
      <a class="btn primary" href="#contact">Start the conversation</a>
      <a class="btn ghost" href="#services">Explore services</a>
    </div>
  </div>
</section>
"""

# -------------------
# Operations (Carousel) — 3 slides with your images
# -------------------
def platform_band():
    slides = [
        {
            "title": "Our Promise to Clients",
            "lead": "Choice, orchestration, insight, and speed — all working as one system.",
            "bullets": [
                "Multiple best-fit proposals, not just one — leveraging our partner ecosystem for choice, transparency, and competitive advantage.",
                "Seamless orchestration of sales strategy, planning, capability building, and operational support — from prospect to cash, without friction.",
                "Actionable insights and analytics that turn data into strategic advantage, enabling faster, better decisions.",
                "Scalable, automated processes that reduce complexity, increase agility, and ensure world-class responsiveness."
            ],
            "img": "ops2.jpg",
            "alt": "Our Promise to Clients"
        },
        {
            "title": "Operational Excellence at Scale",
            "lead": "A global operating framework that’s consistent and agile.",
            "bullets": [
                "Consistency across the IT domain — unified processes, tools, and governance deliver a premium experience anywhere in the world.",
                "Agility in execution — rapid mobilization for new opportunities without compromising quality or compliance.",
                "Sustainable cost efficiency — high-value capabilities are prioritized while transactional activities are optimized through automation and shared services."
            ],
            "img": "ops3.jpg",
            "alt": "Operational Excellence at Scale"
        },
        {
            "title": "Built for the Modern Sales Environment",
            "lead": "Digitization has redefined how sales teams engage with customers. We enable you to meet that challenge.",
            "bullets": [
                "Real-time customer insights",
                "Integrated partner collaboration",
                "Strategic proposal management",
                "Post-sale service excellence"
            ],
            "footer": "The result: higher win rates, shorter sales cycles, stronger customer loyalty, and measurable ROI.",
            "img": "ops4.jpg",
            "alt": "Built for the Modern Sales Environment"
        }
    ]

    def li(items):
        return "".join(f"<li>{x}</li>" for x in items)

    slides_html = ""
    for s in slides:
        text_block = f"""
          <div class="kicker" style="color:var(--accent);font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px">Operations</div>
          <h2 class="h2">{s['title']}</h2>
          <p class="lead">{s['lead']}</p>
        """
        if "body" in s:
            for p in s["body"]:
                text_block += f"<p style='color:var(--muted);margin:6px 0'>{p}</p>"
        if "bullets" in s:
            text_block += f"<ul class='ops-bullets' style='color:var(--muted);margin:8px 0 0 18px'>{li(s['bullets'])}</ul>"
        if "footer" in s:
            text_block += f"<p class='lead' style='margin-top:10px'>{s['footer']}</p>"

        slides_html += f"""
      <div class="ops-slide" role="group" aria-roledescription="slide" aria-label="{s['title']}">
        <div class="glass" style="padding:22px">
          {text_block}
          <div class="cta" style="margin-top:14px">
            <a class="btn primary" href="#contact">Request a walkthrough</a>
            <a class="btn ghost" href="#services">See what’s included</a>
          </div>
        </div>
        <div class="ops-visual">
          <img src="{url_for('static', filename=s['img'])}" alt="{s['alt']}" loading="lazy"
               style="width:100%;height:100%;object-fit:cover;border-radius:12px;border:1px solid var(--border)">
        </div>
      </div>
        """

    dots_html = "".join(f'<button class="ops-dot" aria-label="Go to {i+1}" aria-current="false"></button>' for i in range(len(slides)))

    return f"""
<section id="platform" class="band" aria-label="Operating model carousel">
  <div class="container">
    <div class="ops-wrap">
      <button class="ops-arrow outside left" aria-label="Previous">‹</button>
      <div class="ops-carousel">
        <div class="ops-stage">
          {slides_html}
        </div>
        <div class="ops-controls">{dots_html}</div>
      </div>
      <button class="ops-arrow outside right" aria-label="Next">›</button>
    </div>
  </div>
</section>
"""

def services_grid():
    def service_card(s):
        img_file = SERVICE_IMAGES.get(s["slug"], "symbol.png")
        chips = "".join(f'<span class="chip">{b.split("&")[0].strip()}</span>' for b in s.get("bullets", [])[:3])
        return f"""
        <a class="card" href="/services/{s['slug']}">
          <img src="{url_for('static', filename=img_file)}" alt="{s['title']}" loading="lazy">
          <h3>{s['title']}</h3>
          <p>{s['summary']}</p>
          <div class="chips">{chips}</div>
        </a>
        """
    cards = "".join(service_card(s) for s in SERVICES)
    return f"""
<section id="services" class="services">
  <div class="container">
    <div class="kicker" style="color:var(--accent);font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px">Services</div>
    <h2 class="h2">Build on a stable foundation</h2>
    <div class="cards">{cards}</div>
  </div>
</section>
"""

def stories_teaser():
    return f"""
<section id="stories" class="stories">
  <div class="container story">
    <div class="glass" style="padding:18px">
      <h3 style="margin:0 0 8px">GoPartnerr empowers Vertasse, a leading vertical transportation consultancy, to bridge the information gap between contractors, developers, and manufacturers</h3>
      <blockquote>Through advanced AI, Vertasse’s clients and partners can now read, interpret, refine, and deliver proposals with unmatched accuracy and speed.

This solution creates a single source of truth—a one-stop platform where stakeholders gain full clarity on requirements and ensure that even the most complex specifications are never overlooked.
</blockquote>
      <p class="lead" style="margin-top:8px">We enable Veretasse to sell smarter and excecute with precision.</p>
      <div class="cta"><a class="btn ghost" href="#contact">Talk to an expert</a></div>
    </div>
    <div><img src="{url_for('static', filename='case.jpg')}" alt="Customer story (placeholder)" loading="lazy" style="width:100%;border-radius:12px;border:1px solid var(--border)"></div>
  </div>
</section>
"""

def contact_band(success_msg="", error_msg=""):
    notices = ""
    if success_msg:
        notices += f'<div class="container" style="margin-top:12px"><div class="glass" style="padding:12px">✅ {success_msg}</div></div>'
    if error_msg:
        notices += f'<div class="container" style="margin-top:12px"><div class="glass" style="padding:12px">❌ {error_msg}</div></div>'
    return f"""
<section id="contact" class="cta-band">
  <div class="container" style="display:grid;gap:22px;grid-template-columns:1.1fr .9fr">
    <div>
      <div class="kicker" style="color:var(--accent);font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px">Contact</div>
      <h2 class="h2">Tell us what needs to work better</h2>
      <p class="lead">Send a short note and we’ll map the first steps—scope, owners, and acceptance criteria.</p>
    </div>
    <div class="glass" style="padding:16px">
      <form class="contact" method="post" action="/contact">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Work email" required>
        <textarea name="message" placeholder="What are you trying to improve?" required></textarea>
        <div class="actions">
          <button class="btn primary" type="submit">Send message</button>
        </div>
      </form>
      <p class="lead" style="font-size:16px;margin-top:12px">
        Email: info@gopartnerr.com • Phone: 585588202 • Abu Dhabi, UAE
      </p>
    </div>
  </div>
</section>
{notices}
"""

def home_html(success_msg="", error_msg=""):
    return (
        head(f"{BRAND} — IT & Digital Transformation",
             "GoPartnerr: Security, data, applications, and infrastructure done right.")
        + header_nav()
        + hero_section()
        + platform_band()
        + services_grid()
        + stories_teaser()
        + contact_band(success_msg, error_msg)
        + footer_block()
    )

def list_items(items):
    return "".join(f"<li>{x if x.endswith('.') else x + '.'}</li>" for x in items)

def service_html(slug):
    s = SERVICE_BY_SLUG[slug]
    img_file = SERVICE_IMAGES.get(slug, "symbol.png")

    long_copy_html = f"""
<section style="padding:48px 0 8px">
  <div class="container">
    <article class="glass prose">
      {s.get("long_copy","")}
    </article>
  </div>
</section>
"""

    value_block = ""
    if s.get("bullets"):
        value_block = f"""
<div class="glass value">
  <h3>{s.get("value_title","What we deliver")}</h3>
  <ul>{list_items(s["bullets"])}</ul>
</div>
"""

    outcomes_block = ""
    if s.get("outcomes"):
        outcomes_block = f"""
<div class="glass outcomes">
  <h3>{s.get("outcomes_title","Measured outcomes")}</h3>
  <ul>{list_items(s["outcomes"])}</ul>
</div>
"""

    sustain_block = ""
    if s.get("sustain_points"):
        sustain_block = f"""
<div class="glass sustain">
  <h3>{s.get("sustain_title","Sustaining value")}</h3>
  <ul>{list_items(s["sustain_points"])}</ul>
</div>
"""

    return (
        head(f"{s['title']} — {BRAND}", s["summary"])
        + header_nav()
        + f"""
<section class="hero" style="min-height:30vh">
  <div class="container hero-inner">
    <h1 class="display">{s['title']}</h1>
    <p class="lead">{s['summary']}</p>
    <div class="cta">
      <a class="btn primary" href="/#contact">Request a proposal</a>
      <a class="btn ghost" href="/">Back to all services</a>
    </div>
  </div>
</section>
"""
        + long_copy_html
        + f"""
<section style="padding:22px 0 8px">
  <div class="container" style="display:grid;gap:18px;grid-template-columns:1fr 1fr">
    {outcomes_block}
    {sustain_block}
  </div>
</section>
<section style="padding:0 0 72px">
  <div class="container" style="display:grid;gap:18px;grid-template-columns:1.1fr .9fr">
    {value_block}
    <div class="glass" style="padding:0">
      <img src="{url_for('static', filename=img_file)}" alt="{s['title']}" style="width:100%;height:100%;object-fit:cover;border-radius:18px">
    </div>
  </div>
</section>
"""
        + footer_block()
    )

# -------------------
# Articles HTML
# -------------------
def articles_list_html():
    def card(a):
        tags = "".join(f'<span class="tag">{t}</span>' for t in a["tags"][:3])
        return f"""
        <a class="card article-card" href="/articles/{a['slug']}">
          <img src="{url_for('static', filename=a['image'])}" alt="{a['title']}" loading="lazy">
          <h3>{a['title']}</h3>
          <p>{a['excerpt']}</p>
          <div class="meta">
            <span>By {a['author']}</span> • <span>{a['date']}</span> • <span>{a['reading_time']}</span>
          </div>
          <div class="tags">{tags}</div>
        </a>
        """
    cards = "".join(card(a) for a in ARTICLES)

    subscribe_block = f"""
<div class="glass" style="padding:16px">
  <h3 style="margin:0 0 8px;font-family:Sora,Manrope">Get new articles in your inbox</h3>
  <form class="contact" method="post" action="/contact">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="email" name="email" placeholder="Work email" required>
    <textarea name="message" placeholder="Tell us what topics you care about (optional)"></textarea>
    <div class="actions">
      <button class="btn primary" type="submit">Subscribe</button>
    </div>
  </form>
</div>
"""

    return (
        head(f"Articles — {BRAND}", "Insights on IT, security, data, and delivery.")
        + header_nav()
        + f"""
<section class="articles-hero">
  <div class="container hero-inner">
    <h1 class="display">Articles & Insights</h1>
    <p class="lead">Short, practical reads on proposals, security, data, apps, and infrastructure.</p>
  </div>
</section>
<section style="padding:48px 0 22px">
  <div class="container">
    <div class="article-grid">
      {cards}
    </div>
  </div>
</section>
<section style="padding:12px 0 72px">
  <div class="container" style="display:grid;gap:18px;grid-template-columns:1fr .9fr">
    {subscribe_block}
    <div class="glass" style="padding:0">
      <img src="{url_for('static', filename='articles-side.jpg')}" alt="Articles side visual" style="width:100%;height:100%;object-fit:cover;border-radius:18px">
    </div>
  </div>
</section>
"""
        + footer_block()
    )

def article_detail_html(slug):
    a = ARTICLE_BY_SLUG[slug]
    body_html = "".join(a["body"])
    tags = "".join(f'<span class="tag">{t}</span>' for t in a["tags"])
    share = f"""
<div class="share-row">
  <a class="btn ghost" href="https://www.linkedin.com/shareArticle?mini=true&url={url_for('article', slug=slug, _external=True)}" target="_blank" rel="noopener">Share on LinkedIn</a>
  <a class="btn ghost" href="https://twitter.com/intent/tweet?url={url_for('article', slug=slug, _external=True)}&text={a['title'].replace(' ', '%20')}" target="_blank" rel="noopener">Post on X</a>
</div>
"""
    return (
        head(f"{a['title']} — {BRAND}", a["excerpt"])
        + header_nav()
        + f"""
<section style="padding:26px 0 8px">
  <div class="container">
    <div class="article-header">
      <img src="{url_for('static', filename=a['image'])}" alt="{a['title']}">
    </div>
  </div>
</section>
<section style="padding:16px 0 56px">
  <div class="container article-body">
    <div class="meta" style="color:var(--muted);font-size:14px;margin-bottom:10px">
      {a['date']} • {a['reading_time']} • By {a['author']}
    </div>
    <h1 class="h2" style="margin:0 0 10px">{a['title']}</h1>
    <div class="tags" style="margin-bottom:12px">{tags}</div>
    <article class="prose glass">
      {body_html}
    </article>
    <div style="margin-top:14px">{share}</div>
    <div class="cta" style="margin-top:20px">
      <a class="btn primary" href="/#contact">Talk to an expert</a>
      <a class="btn ghost" href="/articles">Back to articles</a>
    </div>
  </div>
</section>
"""
        + footer_block()
    )

# -------------------
# Routes
# -------------------
@app.route("/")
def home():
    return Response(home_html(), mimetype="text/html")

@app.route("/services/<slug>")
def service(slug):
    if slug not in SERVICE_BY_SLUG:
        return redirect(url_for("home"))
    return Response(service_html(slug), mimetype="text/html")

@app.route("/articles")
def articles():
    return Response(articles_list_html(), mimetype="text/html")

@app.route("/articles/<slug>")
def article(slug):
    if slug not in ARTICLE_BY_SLUG:
        return redirect(url_for("articles"))
    return Response(article_detail_html(slug), mimetype="text/html")

@app.post("/contact")
def contact_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    if not (name and email and message):
        return Response(home_html(error_msg="Please fill out all fields."), mimetype="text/html")
    save_lead_csv(name, email, message)
    mailed = send_lead_email(name, email, message)
    note = "Thanks — we received your message."
    note += " (A copy was emailed to your inbox.)" if mailed else " (Saved to leads.csv. Configure SMTP to also receive emails.)"
    return Response(home_html(success_msg=note), mimetype="text/html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5114, debug=False)
