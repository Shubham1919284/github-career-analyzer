# report.py
# PDF Report Generator using fpdf2

from fpdf import FPDF
import datetime


# ════════════════════════════════
# COLOR PALETTE
# ════════════════════════════════
COLORS = {
    "primary":    (30, 107, 235),   # Blue #1e6beb
    "bg_dark":    (22, 27, 34),     # Dark bg
    "bg_card":    (248, 249, 250),  # Light card
    "text":       (30, 30, 30),     # Dark text
    "text_muted": (100, 116, 139),  # Muted
    "green":      (35, 134, 54),    # Success green
    "yellow":     (210, 153, 34),   # Warning yellow
    "red":        (218, 54, 51),    # Danger red
    "purple":     (137, 87, 229),   # Purple
    "accent":     (88, 166, 255),   # Light blue accent
    "white":      (255, 255, 255),
    "border":     (210, 218, 228),
}


# ════════════════════════════════
# BASE PDF CLASS
# ════════════════════════════════
class CareerPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def header(self):
        # Blue header bar
        self.set_fill_color(*COLORS["primary"])
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*COLORS["white"])
        self.set_xy(15, 5)
        self.cell(0, 8, "GitHub Career Analyzer", ln=False)
        self.set_font("Helvetica", "", 8)
        self.set_xy(0, 5)
        self.cell(195, 8, "github-career-analyzer.streamlit.app", align="R", ln=False)
        self.ln(20)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*COLORS["text_muted"])
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cell(0, 5, f"Generated on {now}  |  Page {self.page_no()}  |  github-career-analyzer", align="C")

    def section_title(self, title, icon=""):
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*COLORS["primary"])
        # Strip non-latin chars from icon for fpdf2 compatibility
        safe_icon = "".join(c for c in icon if ord(c) < 256)
        display = f"{safe_icon} {title}".strip() if safe_icon else title
        self.cell(0, 8, display, ln=True)
        # Underline
        x = self.get_x()
        y = self.get_y()
        self.set_draw_color(*COLORS["primary"])
        self.set_line_width(0.4)
        self.line(15, y, 195, y)
        self.ln(3)
        self.set_text_color(*COLORS["text"])

    def score_bar(self, label, score, max_score=100, color=None):
        if color is None:
            if score >= 70:
                color = COLORS["green"]
            elif score >= 45:
                color = COLORS["yellow"]
            else:
                color = COLORS["red"]

        pct = min(score / max_score, 1.0)
        bar_w = 100
        bar_h = 4

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*COLORS["text"])
        self.cell(60, 7, str(label), ln=False)
        self.cell(20, 7, f"{score}/{max_score}", ln=False)

        x = self.get_x()
        y = self.get_y() + 1.5
        # Track
        self.set_fill_color(*COLORS["border"])
        self.rect(x, y, bar_w, bar_h, "F")
        # Fill
        self.set_fill_color(*color)
        if pct > 0:
            self.rect(x, y, bar_w * pct, bar_h, "F")
        self.ln(7)

    def info_box(self, label, value, color=None):
        if color is None:
            color = COLORS["bg_card"]
        self.set_fill_color(*color)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*COLORS["text_muted"])
        self.cell(0, 5, str(label), ln=True, fill=False)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*COLORS["text"])
        val_str = str(value) if value else "N/A"
        self.multi_cell(0, 6, val_str)
        self.ln(1)

    def colored_box(self, text, bg_color, text_color=None, border_color=None):
        if text_color is None:
            text_color = COLORS["text"]
        self.set_fill_color(*bg_color)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*text_color)
        self.multi_cell(0, 6, str(text), fill=True, border=False)
        self.ln(1)

    def _safe_text(self, text):
        """Remove characters outside latin-1 range for fpdf2 built-in fonts."""
        if text is None:
            return ""
        return "".join(c if ord(c) < 256 else "" for c in str(text)).strip()

    def cell(self, w=0, h=0, text="", *args, **kwargs):
        # Auto-sanitize text to latin-1
        text = self._safe_text(text)
        super().cell(w, h, text, *args, **kwargs)

    def multi_cell(self, w, h=0, text="", *args, **kwargs):
        # Auto-sanitize text to latin-1
        text = self._safe_text(text)
        super().multi_cell(w, h, text, *args, **kwargs)

    def safe_cell(self, w, h, text, **kwargs):
        self.cell(w, h, text, **kwargs)

    def safe_multi_cell(self, w, h, text, **kwargs):
        self.multi_cell(w, h, text, **kwargs)



    def two_col_list(self, left_title, left_items, right_title, right_items, bullet="-"):
        col_w = 87
        start_x = 15
        start_y = self.get_y()

        # Left column
        self.set_xy(start_x, start_y)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*COLORS["primary"])
        self.safe_cell(col_w, 6, left_title, ln=True)
        left_y_start = self.get_y()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*COLORS["text"])
        for item in left_items:
            self.set_x(start_x)
            self.safe_cell(5, 5, bullet)
            self.safe_cell(col_w - 5, 5, str(item)[:65], ln=True)
        left_y_end = self.get_y()

        # Right column
        self.set_xy(start_x + col_w + 6, start_y)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*COLORS["primary"])
        self.safe_cell(col_w, 6, right_title, ln=True)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*COLORS["text"])
        for item in right_items:
            self.set_x(start_x + col_w + 6)
            self.safe_cell(5, 5, bullet)
            self.safe_cell(col_w - 5, 5, str(item)[:65], ln=True)
        right_y_end = self.get_y()

        self.set_y(max(left_y_end, right_y_end))
        self.ln(2)





# ════════════════════════════════
# HELPER: Safe get
# ════════════════════════════════
def safe(val, default="N/A"):
    if val is None or val == "":
        return default
    return str(val)


def safe_score(val, default=0):
    try:
        return int(float(val))
    except (TypeError, ValueError):
        return default


# ════════════════════════════════
# SHARED SECTIONS
# ════════════════════════════════
def add_profile_section(pdf, profile, dev_type, scores, quick_scores=None):
    """Profile header card"""
    pdf.section_title("Profile Overview", "👤")

    # Profile info
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*COLORS["primary"])
    name = safe(profile.get("name") or profile.get("username"))
    pdf.cell(0, 8, name, ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    username = f"@{safe(profile.get('username'))}"
    bio = safe(profile.get("bio"), "")
    location = safe(profile.get("location"), "")
    company = safe(profile.get("company"), "")

    pdf.cell(0, 5, username, ln=True)
    if bio and bio != "N/A":
        pdf.multi_cell(130, 5, bio[:120])
    parts = []
    if location and location != "N/A":
        parts.append(f"📍 {location}")
    if company and company != "N/A":
        parts.append(f"🏢 {company}")
    if parts:
        pdf.set_text_color(*COLORS["text_muted"])
        pdf.cell(0, 5, "  |  ".join(parts), ln=True)

    # Developer type badge
    pdf.ln(2)
    pdf.set_fill_color(*COLORS["primary"])
    pdf.set_text_color(*COLORS["white"])
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(45, 6, f"  {dev_type}  ", fill=True, ln=False)

    # Stats row
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*COLORS["text_muted"])
    repos = safe(profile.get("public_repos"), "0")
    followers = safe(profile.get("followers"), "0")
    following = safe(profile.get("following"), "0")
    stats_text = f"   Repos: {repos}  |  Followers: {followers}  |  Following: {following}"
    pdf.cell(0, 6, stats_text, ln=True)
    pdf.ln(3)

    # Score display
    total = safe_score(scores.get("total_score"))
    score_label = "Profile Score"
    score_color = COLORS["green"] if total >= 70 else COLORS["yellow"] if total >= 45 else COLORS["red"]

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 7, f"{score_label}: {total}/100", ln=True)

    if quick_scores:
        q_total = safe_score(quick_scores.get("total_score"))
        pdf.set_text_color(*COLORS["text_muted"])
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"GitHub Profile Score: {q_total}/100", ln=True)

    pdf.ln(3)


def add_skills_section(pdf, skills):
    pdf.section_title("Detected Skills", "🏷️")
    if not skills:
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6, "No skills detected", ln=True)
        return

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*COLORS["text"])
    skills_str = "  |  ".join(skills[:20])
    pdf.multi_cell(0, 5, skills_str)
    pdf.ln(2)


def add_red_flags_section(pdf, red_flags):
    flags = red_flags.get("red_flags", [])
    warnings = red_flags.get("warnings", [])
    positives = red_flags.get("positive_flags", [])

    if flags or warnings or positives:
        pdf.section_title("Profile Issues & Strengths", "⚠️")

    for flag in flags[:4]:
        pdf.set_fill_color(255, 235, 235)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*COLORS["red"])
        pdf.cell(0, 5, f"❌ {safe(flag.get('flag'))}", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text_muted"])
        pdf.cell(0, 4, f"   {safe(flag.get('detail'))[:90]}", ln=True)
        pdf.set_text_color(*COLORS["green"])
        pdf.cell(0, 4, f"   💡 {safe(flag.get('fix'))[:90]}", ln=True)
        pdf.ln(1)

    for w in warnings[:3]:
        pdf.set_fill_color(255, 248, 220)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*COLORS["yellow"])
        pdf.cell(0, 5, f"⚠️  {safe(w.get('flag'))}", ln=True, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text_muted"])
        pdf.cell(0, 4, f"   {safe(w.get('detail'))[:90]}", ln=True)
        pdf.ln(1)

    if positives:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["green"])
        pdf.cell(0, 6, "✅ Strengths:", ln=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text"])
        for p in positives[:5]:
            pdf.cell(5, 5, "•")
            pdf.cell(0, 5, str(p)[:100], ln=True)
        pdf.ln(2)


def add_top_repos_section(pdf, repos):
    pdf.section_title("Top Repositories", "📁")
    if not repos:
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6, "No repositories found", ln=True)
        return

    # Header row
    pdf.set_fill_color(*COLORS["primary"])
    pdf.set_text_color(*COLORS["white"])
    pdf.set_font("Helvetica", "B", 8)
    col_widths = [65, 20, 18, 25, 52]
    headers = ["Repository", "⭐ Stars", "🍴 Forks", "Language", "Description"]
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 6, h, fill=True, border=0)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    for i, repo in enumerate(repos[:8]):
        fill = i % 2 == 0
        pdf.set_fill_color(245, 248, 252) if fill else pdf.set_fill_color(*COLORS["white"])
        pdf.set_text_color(*COLORS["text"])
        name = safe(repo.get("name"))[:28]
        stars = safe(repo.get("stars"), "0")
        forks = safe(repo.get("forks"), "0")
        lang = safe(repo.get("language"), "-")[:12]
        desc = safe(repo.get("description"), "-")[:30]
        row = [name, stars, forks, lang, desc]
        for w, cell_text in zip(col_widths, row):
            pdf.cell(w, 5, str(cell_text), fill=fill, border=0)
        pdf.ln()
    pdf.ln(3)


def add_ats_section(pdf, ats):
    score = safe_score(ats.get("ats_score"))
    level = ats.get("ats_level", {})
    suggestions = ats.get("suggestions", [])

    pdf.section_title("ATS Optimization Score", "📋")
    score_color = COLORS["green"] if score >= 70 else COLORS["yellow"] if score >= 45 else COLORS["red"]
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 7, f"ATS Score: {score}/100  —  {safe(level.get('level'))}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    pdf.cell(0, 5, safe(level.get("message"), ""), ln=True)
    pdf.ln(2)

    if suggestions:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["text"])
        pdf.cell(0, 5, "Improvement Tips:", ln=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text_muted"])
        for tip in suggestions[:6]:
            pdf.cell(6, 5, "→")
            pdf.cell(0, 5, str(tip)[:100], ln=True)
    pdf.ln(2)


# ════════════════════════════════
# QUICK SCAN REPORT
# ════════════════════════════════
def generate_quick_report(data):
    """
    Generate a PDF for quick scan results.
    data: the JSON response from /scan/quick endpoint
    Returns: bytes (PDF content)
    """
    pdf = CareerPDF()
    pdf.add_page()

    profile = data.get("profile", {})
    scores = data.get("scores", {})
    dev_type = safe(data.get("developer_type"), "Developer")
    skills = data.get("skills", [])
    languages = data.get("languages", {})
    top_repos = data.get("top_repos", [])
    red_flags = data.get("red_flags", {})
    ats = data.get("ats", {})

    # ── Title Page Banner
    pdf.set_fill_color(*COLORS["bg_card"])
    pdf.rect(0, 20, 210, 22, "F")
    pdf.set_xy(15, 22)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*COLORS["primary"])
    pdf.cell(0, 10, "Quick Profile Report", ln=True)
    pdf.set_x(15)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    username = safe(profile.get("username"))
    pdf.cell(0, 6, f"GitHub Profile: @{username}  |  ML-powered analysis", ln=True)
    pdf.ln(5)

    # ── Profile Section
    add_profile_section(pdf, profile, dev_type, scores)

    # ── Languages
    pdf.section_title("Language Distribution", "💻")
    if languages:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*COLORS["text"])
        total_bytes = sum(languages.values()) or 1
        for lang, bytes_count in list(languages.items())[:8]:
            pct = round((bytes_count / total_bytes) * 100, 1)
            pdf.score_bar(lang, pct, 100,
                          color=COLORS["primary"] if pct > 30 else COLORS["accent"])
    pdf.ln(2)

    # ── Skills
    add_skills_section(pdf, skills)

    # ── Score Breakdown
    breakdown = scores.get("breakdown", {})
    if breakdown:
        pdf.section_title("Score Breakdown", "📊")
        max_vals = {
            "Quality Score": 25, "Consistency Score": 25,
            "Diversity Score": 20, "Activity Score": 20, "Community Score": 10
        }
        for cat, val in breakdown.items():
            max_v = max_vals.get(cat, 25)
            pdf.score_bar(cat, val, max_v)
        pdf.ln(2)

    # ── Top Repos
    add_top_repos_section(pdf, top_repos)

    # New page for issues
    pdf.add_page()

    # ── Red Flags
    add_red_flags_section(pdf, red_flags)

    # ── ATS Score
    add_ats_section(pdf, ats)

    # ── Summary Card
    total = safe_score(scores.get("total_score"))
    pdf.section_title("Summary", "✅")
    score_color = COLORS["green"] if total >= 70 else COLORS["yellow"] if total >= 45 else COLORS["red"]
    verdict = "Strong Profile" if total >= 70 else "Developing Profile" if total >= 45 else "Needs Improvement"
    pdf.set_fill_color(240, 255, 240) if total >= 70 else pdf.set_fill_color(255, 248, 220)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 8, f"Overall: {verdict}  ({total}/100)", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    pdf.cell(0, 5, "Run Career Analyzer for detailed job-specific insights and roadmap.", ln=True)

    return bytes(pdf.output())


# ════════════════════════════════
# CAREER REPORT
# ════════════════════════════════
def generate_career_report(data):
    """
    Generate a comprehensive PDF for career analysis results.
    data: the JSON response from /scan/career endpoint
    Returns: bytes (PDF content)
    """
    pdf = CareerPDF()
    pdf.add_page()

    profile = data.get("profile", {})
    quick_scores = data.get("quick_scores", {})
    dev_type = safe(data.get("developer_type"), "Developer")
    skills = data.get("skills", [])
    languages = data.get("languages", {})
    top_repos = data.get("top_repos", [])
    career = data.get("career", {})
    cs = career.get("career_score", {})
    red_flags = career.get("red_flags", {})
    ats = career.get("ats", {})
    company_match = career.get("company_match", {})
    salary = career.get("salary", {})
    roadmap = career.get("roadmap", {})
    projects = career.get("projects", [])
    interview_tips = career.get("interview_tips", {})
    job_role = safe(career.get("job_role"), "Developer")
    exp_level = safe(career.get("experience_level"), "Fresher")

    # ── Title Banner
    pdf.set_fill_color(*COLORS["bg_card"])
    pdf.rect(0, 20, 210, 28, "F")
    pdf.set_xy(15, 22)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*COLORS["primary"])
    pdf.cell(0, 10, "Career Readiness Report", ln=True)
    pdf.set_x(15)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    username = safe(profile.get("username"))
    pdf.cell(0, 5, f"@{username}  |  Target Role: {job_role}  |  Level: {exp_level}", ln=True)
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*COLORS["primary"])
    pdf.cell(0, 5, "2026 Job Market Analysis", ln=True)
    pdf.ln(8)

    # ── Profile + Score
    add_profile_section(pdf, profile, dev_type, cs, quick_scores)

    # ── Career Readiness Badge
    readiness = cs.get("readiness", {})
    r_level = safe(readiness.get("level"), "")
    r_message = safe(readiness.get("message"), "")
    career_total = safe_score(cs.get("total_score"))

    score_color = COLORS["green"] if "🟢" in r_level else COLORS["yellow"] if "🟡" in r_level else COLORS["red"]
    bg_color = (230, 255, 230) if "🟢" in r_level else (255, 248, 220) if "🟡" in r_level else (255, 235, 235)
    pdf.set_fill_color(*bg_color)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 9, f"{r_level}  —  Career Score: {career_total}/100", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    pdf.cell(0, 5, r_message, ln=True, fill=True)
    pdf.ln(4)

    # ── Strengths / Weaknesses / Missing
    strengths = cs.get("strengths", [])
    weaknesses = cs.get("weaknesses", [])
    missing = cs.get("missing_foundation", [])

    pdf.section_title("Key Findings", "🔍")
    pdf.two_col_list("✅ Strengths", strengths[:5], "⚠️ Weaknesses", weaknesses[:5])
    pdf.ln(1)
    if missing:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["red"])
        pdf.cell(0, 5, "❌ Missing Foundation Skills:", ln=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text"])
        pdf.multi_cell(0, 5, "  |  ".join(missing[:8]))
        pdf.ln(2)

    # ── Score Breakdown
    pdf.section_title("Score Breakdown", "📊")
    f_breakdown = cs.get("foundation_breakdown", {})
    m_breakdown = cs.get("modern_breakdown", {})

    if f_breakdown:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["primary"])
        pdf.cell(0, 6, "Foundation Skills (60 pts max)", ln=True)
        for cat, info in f_breakdown.items():
            s = safe_score(info.get("score"))
            m = safe_score(info.get("max"), 15)
            pdf.score_bar(cat, s, m, color=COLORS["accent"])

    if m_breakdown:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["primary"])
        pdf.cell(0, 6, "Modern 2026 Skills (40 pts max)", ln=True)
        for cat, info in m_breakdown.items():
            s = safe_score(info.get("score"))
            m = safe_score(info.get("max"), 10)
            pdf.score_bar(cat, s, m, color=COLORS["green"])
    pdf.ln(2)

    # ── ATS
    add_ats_section(pdf, ats)

    # ── Red Flags
    add_red_flags_section(pdf, red_flags)

    # ── Skills
    add_skills_section(pdf, skills)

    # New page
    pdf.add_page()

    # ── Company Readiness
    if company_match:
        pdf.section_title("Company Readiness", "🏢")
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(*COLORS["primary"])
        pdf.set_text_color(*COLORS["white"])
        pdf.cell(60, 6, "Company Type", fill=True)
        pdf.cell(25, 6, "Match %", fill=True)
        pdf.cell(20, 6, "Status", fill=True)
        pdf.cell(0, 6, "Examples", fill=True)
        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        for i, (company, result) in enumerate(company_match.items()):
            fill = i % 2 == 0
            pdf.set_fill_color(245, 248, 252) if fill else pdf.set_fill_color(*COLORS["white"])
            pct = safe_score(result.get("match_percentage"))
            status = result.get("status", {})
            status_icon = safe(status.get("icon"), "")
            status_label = safe(status.get("label"), "")
            examples = ", ".join(result.get("examples", [])[:2])
            pct_color = COLORS["green"] if pct >= 80 else COLORS["yellow"] if pct >= 55 else COLORS["red"]

            pdf.set_text_color(*COLORS["text"])
            pdf.cell(60, 5, str(company), fill=fill)
            pdf.set_text_color(*pct_color)
            pdf.cell(25, 5, f"{pct}%", fill=fill)
            pdf.set_text_color(*COLORS["text"])
            pdf.cell(20, 5, f"{status_icon}{status_label}"[:10], fill=fill)
            pdf.cell(0, 5, examples[:35], fill=fill)
            pdf.ln()
        pdf.ln(4)

    # ── Salary Insight
    if salary:
        pdf.section_title("Salary Insight", "💰")
        current_sal = salary.get("current_salary", {})
        next_sal = salary.get("next_salary", {})
        curr_level = safe(salary.get("current_level"), "")
        next_level = safe(salary.get("next_level"), "")
        insight = safe(salary.get("insight"), "")

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*COLORS["text"])
        pdf.cell(60, 6, f"Level: {curr_level}", ln=False)
        pdf.set_text_color(*COLORS["primary"])
        india_sal = safe(current_sal.get("india"), "N/A")
        remote_sal = safe(current_sal.get("remote"), "N/A")
        pdf.cell(60, 6, f"India: {india_sal}", ln=False)
        pdf.cell(0, 6, f"Remote: {remote_sal}", ln=True)

        if next_sal:
            pdf.set_text_color(*COLORS["green"])
            pdf.set_font("Helvetica", "", 8)
            next_india = safe(next_sal.get("india"), "N/A")
            pdf.cell(0, 5, f"Next Level ({next_level})  →  India: {next_india}", ln=True)

        if insight and insight != "N/A":
            pdf.set_text_color(*COLORS["text_muted"])
            pdf.set_font("Helvetica", "", 8)
            pdf.multi_cell(0, 5, f"💡 {insight[:150]}")
        pdf.ln(3)

    # ── Roadmap
    weeks = roadmap.get("weeks", [])
    duration = safe(roadmap.get("duration"), "")
    if weeks:
        pdf.section_title(f"Learning Roadmap  ({duration})", "🗺️")
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLORS["text"])
        for week_data in weeks[:8]:
            week_label = safe(week_data.get("week"), "")
            title = safe(week_data.get("title"), "")
            topics = week_data.get("topics", [])
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*COLORS["primary"])
            pdf.cell(35, 5, week_label, ln=False)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*COLORS["text"])
            pdf.cell(0, 5, title, ln=True)
            if topics:
                pdf.set_text_color(*COLORS["text_muted"])
                pdf.cell(40, 4, "", ln=False)
                pdf.cell(0, 4, "Topics: " + ", ".join(topics[:4]), ln=True)
        pdf.ln(3)

    # New page for projects + interview tips
    pdf.add_page()

    # ── Project Suggestions
    if projects:
        pdf.section_title("Recommended Projects (2026 Market)", "💡")
        for i, proj in enumerate(projects[:5], 1):
            title = safe(proj.get("title"))
            diff = safe(proj.get("difficulty"), "Intermediate")
            why = safe(proj.get("why"), "")
            tech = ", ".join(proj.get("tech", [])[:5])
            time_est = safe(proj.get("time"), "")

            diff_color = COLORS["green"] if diff == "Beginner" else COLORS["yellow"] if diff == "Intermediate" else COLORS["red"]

            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*COLORS["primary"])
            pdf.cell(0, 5, f"#{i} {title}", ln=True)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*diff_color)
            pdf.cell(35, 4, f"  {diff}", ln=False)
            pdf.set_text_color(*COLORS["text_muted"])
            pdf.cell(0, 4, f"⏱ {time_est}", ln=True)
            pdf.set_text_color(*COLORS["text"])
            pdf.multi_cell(0, 4, f"  Why: {why[:100]}")
            pdf.set_text_color(*COLORS["text_muted"])
            pdf.cell(0, 4, f"  Tech: {tech}", ln=True)
            pdf.ln(2)

    # ── Interview Tips
    if interview_tips:
        pdf.section_title("Interview Preparation", "🎤")
        questions = interview_tips.get("common_questions", [])
        companies_look_for = interview_tips.get("what_companies_look_for_2026", [])
        mistakes = interview_tips.get("common_mistakes", [])
        portfolio_tips = interview_tips.get("portfolio_tips", [])

        pdf.two_col_list(
            "Common Questions",
            [f"{i+1}. {q[:60]}" for i, q in enumerate(questions[:5])],
            "What Companies Look For in 2026",
            companies_look_for[:5],
            bullet=""
        )

        pdf.two_col_list(
            "❌ Common Mistakes to Avoid",
            mistakes[:4],
            "💡 Portfolio Tips",
            portfolio_tips[:4],
        )

    # ── Top Repos
    pdf.add_page()
    add_top_repos_section(pdf, top_repos)

    # ── Final Summary
    pdf.section_title("Summary & Next Steps", "🚀")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 7, f"Career Score: {career_total}/100  |  {r_level}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLORS["text_muted"])
    pdf.multi_cell(0, 5, (
        f"Target Role: {job_role}  |  Experience: {exp_level}\n"
        f"Focus on missing skills, complete recommended projects, and keep your GitHub active. "
        f"Re-analyze every 30 days to track progress."
    ))

    return bytes(pdf.output())


# ════════════════════════════════
# TEST
# ════════════════════════════════
if __name__ == "__main__":
    # Quick test with mock data
    mock_quick = {
        "profile": {
            "username": "testuser", "name": "Test User",
            "bio": "Full stack developer", "location": "India",
            "company": "TechCo", "public_repos": 25,
            "followers": 150, "following": 80
        },
        "scores": {"total_score": 72, "breakdown": {
            "Quality Score": 18, "Consistency Score": 20,
            "Diversity Score": 14, "Activity Score": 15, "Community Score": 5
        }},
        "developer_type": "Full Stack Developer",
        "skills": ["Python", "React", "FastAPI", "Docker", "PostgreSQL"],
        "languages": {"Python": 45000, "JavaScript": 30000, "TypeScript": 20000},
        "top_repos": [
            {"name": "my-project", "stars": 42, "forks": 12,
             "language": "Python", "description": "A cool project"}
        ],
        "red_flags": {"red_flags": [], "warnings": [], "positive_flags": ["Active on GitHub"]},
        "ats": {"ats_score": 65, "ats_level": {"level": "🟡 Moderate", "message": "Good profile"}, "suggestions": ["Add more keywords"]}
    }

    pdf_bytes = generate_quick_report(mock_quick)
    with open("test_quick_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print(f"✅ Quick report generated: {len(pdf_bytes)} bytes")
