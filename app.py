# app.py

import streamlit as st
import requests as req
import time
from database.connection import init_db, get_leaderboard, get_recent_searches
import report as report_gen

# ════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════
st.set_page_config(
    page_title="GitHub Career Analyzer",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════
# INIT DB
# ════════════════════════════════
init_db()

# ════════════════════════════════
# API BASE URL
# ════════════════════════════════
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ════════════════════════════════
# CSS
# ════════════════════════════════
st.markdown("""
<style>
/* Global */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
}
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}
.main { background-color: #0d1117; }

/* Cards */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-blue {
    background: #1f3a5f;
    border: 1px solid #1f6feb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-green {
    background: #1a2f1a;
    border: 1px solid #238636;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-red {
    background: #2d1a1a;
    border: 1px solid #da3633;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-yellow {
    background: #2d2500;
    border: 1px solid #d29922;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

/* Score Ring */
.score-ring {
    text-align: center;
    padding: 20px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    margin: 3px;
}
.badge-blue { background: #1f6feb22; color: #58a6ff; border: 1px solid #1f6feb55; }
.badge-green { background: #23863622; color: #3fb950; border: 1px solid #23863655; }
.badge-yellow { background: #d2992222; color: #d29922; border: 1px solid #d2992255; }
.badge-red { background: #da363322; color: #f85149; border: 1px solid #da363355; }
.badge-purple { background: #8957e522; color: #d2a8ff; border: 1px solid #8957e555; }

/* Skill pills */
.skill-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    background: #1f6feb22;
    color: #58a6ff;
    border: 1px solid #1f6feb44;
    margin: 3px;
}

/* Section headers */
.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #e6edf3;
    margin: 24px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #30363d;
}

/* Metric cards */
.metric-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-value {
    font-size: 28px;
    font-weight: 600;
    color: #58a6ff;
}
.metric-label {
    font-size: 12px;
    color: #8b949e;
    margin-top: 4px;
}

/* Buttons */
.stButton>button {
    background: #238636;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 15px;
    width: 100%;
    transition: background 0.2s;
}
.stButton>button:hover {
    background: #2ea043;
}

/* Progress bars */
.progress-track {
    background: #21262d;
    border-radius: 4px;
    height: 8px;
    margin: 4px 0;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* Links */
a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Tables */
.stDataFrame { background: #161b22; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #30363d;
}
.stTabs [data-baseweb="tab"] {
    color: #8b949e;
}
.stTabs [aria-selected="true"] {
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════
# SESSION STATE
# ════════════════════════════════
if "user" not in st.session_state:
    st.session_state.user = None
if "session_token" not in st.session_state:
    st.session_state.session_token = None
if "quick_data" not in st.session_state:
    st.session_state.quick_data = None
if "career_data" not in st.session_state:
    st.session_state.career_data = None
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "quick"


# ════════════════════════════════
# API HELPERS
# ════════════════════════════════
def api_quick_scan(username):
    try:
        response = req.post(
            f"{API_URL}/scan/quick",
            json={"username": username},
            timeout=60
        )
        if response.status_code == 200:
            return response.json(), None
        # Try to extract error detail from JSON, fallback to status text
        try:
            detail = response.json().get("detail", f"Server error {response.status_code}")
        except Exception:
            detail = f"Server error {response.status_code}: {response.text[:200] or 'empty response'}"
        return None, detail
    except req.exceptions.ConnectionError:
        return None, "Backend not running! Start it with: python backend/main.py"
    except req.exceptions.Timeout:
        return None, "Request timed out — try again"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def api_career_scan(username, job_role, experience_level, extra_skills, user_id=None):
    try:
        response = req.post(
            f"{API_URL}/scan/career",
            json={
                "username": username,
                "job_role": job_role,
                "experience_level": experience_level,
                "extra_skills": extra_skills,
                "user_id": user_id
            },
            timeout=180
        )
        if response.status_code == 200:
            return response.json(), None
        # Try to extract error detail from JSON, fallback to status text
        try:
            detail = response.json().get("detail", f"Server error {response.status_code}")
        except Exception:
            detail = f"Server error {response.status_code}: {response.text[:300] or 'empty response'}"
        return None, detail
    except req.exceptions.ConnectionError:
        return None, "Backend not running! Start it with: python backend/main.py"
    except req.exceptions.Timeout:
        return None, "Career analysis timed out — try again with fewer repos"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


# ════════════════════════════════
# UI COMPONENTS
# ════════════════════════════════
def render_score_ring(score, label="Score", size=120):
    pct = score / 100
    color = "#238636" if score >= 70 else "#d29922" if score >= 45 else "#da3633"
    circumference = 2 * 3.14159 * 45
    offset = circumference * (1 - pct)
    st.markdown(f"""
    <div style="text-align:center;">
        <svg width="{size}" height="{size}" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none"
                stroke="#21262d" stroke-width="8"/>
            <circle cx="50" cy="50" r="45" fill="none"
                stroke="{color}" stroke-width="8"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{offset}"
                stroke-linecap="round"
                transform="rotate(-90 50 50)"/>
            <text x="50" y="45" text-anchor="middle"
                font-size="20" font-weight="bold"
                fill="{color}">{score}</text>
            <text x="50" y="60" text-anchor="middle"
                font-size="10" fill="#8b949e">{label}</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(label, value, max_val, color="#58a6ff"):
    pct = min((value / max_val) * 100, 100)
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between;
                    font-size: 13px; color: #8b949e; margin-bottom: 4px;">
            <span>{label}</span>
            <span>{value}/{max_val}</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill"
                style="width:{pct}%; background:{color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_badge(text, style="blue"):
    st.markdown(
        f'<span class="badge badge-{style}">{text}</span>',
        unsafe_allow_html=True
    )


def render_skills(skills):
    html = " ".join([f'<span class="skill-pill">{s}</span>' for s in skills])
    st.markdown(html, unsafe_allow_html=True)


def render_section_title(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


# ════════════════════════════════
# SIDEBAR
# ════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h2 style="color:#58a6ff; margin:0;">🐙 GitHub</h2>
            <h2 style="color:#e6edf3; margin:0;">Career Analyzer</h2>
            <p style="color:#8b949e; font-size:13px; margin-top:5px;">
                ML-powered career insights
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Login status
        if st.session_state.user:
            user = st.session_state.user
            if user.get("avatar_url"):
                st.image(user["avatar_url"], width=60)
            st.markdown(f"**{user.get('name', 'User')}**")
            st.caption(user.get("email", ""))
            if st.button("🚪 Logout", key="logout"):
                st.session_state.user = None
                st.session_state.session_token = None
                st.rerun()
        else:
            st.markdown("**Login for full features:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔵 Google", key="google_login"):
                    try:
                        r = req.get(f"{API_URL}/auth/google", timeout=5)
                        url = r.json().get("url")
                        st.markdown(f"[Click to Login]({url})")
                    except Exception:
                        st.error("Backend not running!")
            with col2:
                if st.button("⚫ GitHub", key="github_login"):
                    try:
                        r = req.get(f"{API_URL}/auth/github", timeout=5)
                        url = r.json().get("url")
                        st.markdown(f"[Click to Login]({url})")
                    except Exception:
                        st.error("Backend not running!")

        st.divider()

        # Rate limit
        try:
            r = req.get(f"{API_URL}/rate-limit", timeout=5)
            if r.status_code == 200:
                data = r.json()
                remaining = data["remaining"]
                color = "green" if remaining > 1000 else "orange" if remaining > 100 else "red"
                st.markdown(f"""
                <div style="background:#21262d; border-radius:8px; padding:10px; text-align:center;">
                    <p style="color:#8b949e; font-size:12px; margin:0;">GitHub API</p>
                    <p style="color:{color}; font-size:18px; font-weight:bold; margin:4px 0;">
                        {remaining}
                    </p>
                    <p style="color:#8b949e; font-size:11px; margin:0;">requests remaining</p>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            st.caption("⚠️ Start backend first!")

        st.divider()

        # Recent searches
        st.markdown("**🕐 Recent Searches**")
        try:
            searches = get_recent_searches(limit=5)
            for s in searches:
                st.caption(f"@{s['github_username']} — {s['total_score']}/100")
        except Exception:
            st.caption("No history yet")


# ════════════════════════════════
# QUICK SCAN UI
# ════════════════════════════════
def render_quick_scan():
    st.markdown("""
    <div class="card">
        <h3 style="color:#58a6ff; margin:0;">⚡ Quick Profile Scan</h3>
        <p style="color:#8b949e; margin:8px 0 0 0;">
            Get instant insights about any GitHub profile
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        username = st.text_input(
            "GitHub Username:",
            placeholder="e.g. torvalds, gvanrossum",
            label_visibility="collapsed",
            key="quick_username"
        )
    with col2:
        scan_btn = st.button("🔍 Scan", key="quick_scan_btn")

    if scan_btn and username:
        with st.status("🔄 Analyzing profile...", expanded=True) as status:
            st.write("📡 Fetching GitHub data...")
            time.sleep(0.3)
            st.write("🔤 Analyzing languages...")
            time.sleep(0.3)
            st.write("🤖 Running ML analysis...")
            data, error = api_quick_scan(username)
            if error:
                status.update(label=f"❌ {error}", state="error")
                st.stop()
            st.write("📊 Building dashboard...")
            time.sleep(0.2)
            status.update(label="✅ Analysis complete!", state="complete")

        st.session_state.quick_data = data
        st.session_state.career_data = None

    elif scan_btn:
        st.warning("⚠️ Please enter a username!")

    # Render results
    if st.session_state.quick_data:
        render_quick_results(st.session_state.quick_data)

    # Enable career analyzer
    if st.session_state.quick_data:
        st.divider()
        st.markdown("""
        <div class="card-blue">
            <h3 style="color:#58a6ff; margin:0;">🎯 Want a detailed career analysis?</h3>
            <p style="color:#8b949e; margin:8px 0 0 0;">
                Enable Career Analyzer for job-specific insights,
                roadmap, salary info and more!
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Enable Career Analyzer →", key="enable_career"):
            st.session_state.current_tab = "career"
            st.rerun()


# ════════════════════════════════
# QUICK RESULTS
# ════════════════════════════════
def render_quick_results(data):
    profile = data["profile"]
    scores = data["scores"]
    red_flags = data["red_flags"]
    ats = data["ats"]

    st.divider()

    # Profile header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if profile.get("avatar_url"):
            st.image(profile["avatar_url"], width=100)

    with col2:
        st.markdown(f"## {profile.get('name', profile.get('username'))}")
        if profile.get("bio"):
            st.caption(profile["bio"])

        info = []
        if profile.get("location"): info.append(f"📍 {profile['location']}")
        if profile.get("company"): info.append(f"🏢 {profile['company']}")
        if profile.get("blog"): info.append(f"🔗 {profile['blog']}")
        if info:
            st.caption(" | ".join(info))

        # Badges
        badges_html = f"""
        <span class="badge badge-blue">{data['developer_type']}</span>
        """
        coding_style = data.get("coding_style", {})
        if isinstance(coding_style, dict):
            for key, value in coding_style.items():
                badges_html += f'<span class="badge badge-purple">{value}</span>'
        else:
            for style in coding_style:
                badges_html += f'<span class="badge badge-purple">{style}</span>'
        st.markdown(badges_html, unsafe_allow_html=True)

    with col3:
        render_score_ring(scores["total_score"])

    st.divider()

    # Key metrics
    render_section_title("📊 Key Metrics")
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        (m1, "📁 Repos", profile.get("public_repos", 0)),
        (m2, "👥 Followers", f"{profile.get('followers', 0):,}"),
        (m3, "⭐ Stars", f"{sum(r['stars'] for r in data['top_repos']):,}"),
        (m4, "💻 Languages", len(data["languages"])),
        (m5, "🎯 ATS Score", f"{ats['ats_score']}/100"),
    ]
    for col, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Skills
    render_section_title("🏷️ Detected Skills")
    render_skills(data.get("skills", []))

    st.divider()

    # Charts
    render_section_title("📈 Analytics")
    col1, col2 = st.columns(2)

    with col1:
        import plotly.express as px
        import plotly.graph_objects as go

        # Language chart
        if data["languages"]:
            langs = dict(
                sorted(
                    data["languages"].items(),
                    key=lambda x: x[1], reverse=True
                )[:8]
            )
            fig = px.pie(
                names=list(langs.keys()),
                values=list(langs.values()),
                title="Language Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#e6edf3",
                title_font_color="#58a6ff"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Score breakdown
        breakdown = scores["breakdown"]
        max_vals = {
            "Quality Score": 25,
            "Consistency Score": 25,
            "Diversity Score": 20,
            "Activity Score": 20,
            "Community Score": 10
        }
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Your Score",
            x=list(breakdown.keys()),
            y=list(breakdown.values()),
            marker_color="#58a6ff"
        ))
        fig.add_trace(go.Bar(
            name="Max",
            x=list(max_vals.keys()),
            y=list(max_vals.values()),
            marker_color="#21262d"
        ))
        fig.update_layout(
            title="Score Breakdown",
            barmode="overlay",
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            font_color="#e6edf3",
            title_font_color="#58a6ff"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Red flags
    if red_flags["red_flags"] or red_flags["warnings"]:
        render_section_title("⚠️ Profile Issues")
        col1, col2 = st.columns(2)
        with col1:
            for flag in red_flags["red_flags"]:
                st.markdown(f"""
                <div class="card-red">
                    <p style="color:#f85149; margin:0; font-weight:bold;">
                        {flag['flag']}
                    </p>
                    <p style="color:#8b949e; margin:8px 0; font-size:13px;">
                        {flag['detail']}
                    </p>
                    <p style="color:#3fb950; margin:0; font-size:13px;">
                        💡 {flag['fix']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            for warning in red_flags["warnings"]:
                st.markdown(f"""
                <div class="card-yellow">
                    <p style="color:#d29922; margin:0; font-weight:bold;">
                        {warning['flag']}
                    </p>
                    <p style="color:#8b949e; margin:8px 0; font-size:13px;">
                        {warning['detail']}
                    </p>
                    <p style="color:#3fb950; margin:0; font-size:13px;">
                        💡 {warning['fix']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    # Positive flags
    if red_flags["positive_flags"]:
        render_section_title("✅ Strengths")
        for p in red_flags["positive_flags"]:
            st.markdown(f"""
            <div class="card-green">
                <p style="color:#3fb950; margin:0;">{p}</p>
            </div>
            """, unsafe_allow_html=True)

    # Top repos
    render_section_title("📁 Top Repositories")
    repo_data = [
        {
            "Repo": r["name"],
            "⭐ Stars": r["stars"],
            "🍴 Forks": r["forks"],
            "Language": r.get("language") or "N/A",
            "Description": (r.get("description") or "N/A")[:50]
        }
        for r in data["top_repos"]
    ]
    st.dataframe(repo_data, use_container_width=True)

    # ATS suggestions
    if ats.get("suggestions"):
        render_section_title("📋 ATS Optimization Tips")
        for tip in ats["suggestions"]:
            st.markdown(f"→ {tip}")

    # Notifications
    render_section_title("📬 Get Report Via")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("📧 Email:", placeholder="your@email.com", key="qs_email")
    with col2:
        telegram = st.text_input("📱 Telegram Chat ID:", placeholder="123456789", key="qs_telegram")

    if st.button("📤 Send Report", key="qs_notify"):
        if email or telegram:
            try:
                req.post(f"{API_URL}/notify/quick-scan", json={
                    "email": email or None,
                    "telegram_chat_id": telegram or None,
                    "name": profile.get("name", "Developer"),
                    "username": profile.get("username"),
                    "total_score": scores["total_score"],
                    "dev_type": data["developer_type"],
                    "skills": data.get("skills", [])
                }, timeout=30)
                st.success("✅ Report sent!")
            except Exception:
                st.error("❌ Could not send — check backend!")
        else:
            st.warning("Enter email or Telegram Chat ID!")

    # PDF Download
    st.markdown("---")
    col_dl, _ = st.columns([1, 2])
    with col_dl:
        try:
            pdf_bytes = report_gen.generate_quick_report(data)
            username = profile.get("username", "report")
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"{username}_quick_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")


# ════════════════════════════════
# CAREER ANALYZER UI
# ════════════════════════════════
def render_career_analyzer():
    from career.job_roles import get_all_roles, get_role_emojis

    st.markdown("""
    <div class="card">
        <h3 style="color:#58a6ff; margin:0;">🎯 Career Readiness Analyzer</h3>
        <p style="color:#8b949e; margin:8px 0 0 0;">
            Deep analysis for your target job role — 2026 market ready
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Pre-fill username if quick scan done
    default_username = ""
    if st.session_state.quick_data:
        default_username = st.session_state.quick_data["profile"].get("username", "")

    col1, col2 = st.columns([3, 1])
    with col1:
        username = st.text_input(
            "GitHub Username:",
            value=default_username,
            placeholder="e.g. torvalds",
            label_visibility="collapsed",
            key="career_username"
        )

    # Job roles
    roles = get_all_roles()
    emojis = get_role_emojis()
    role_options = [f"{emojis[r]} {r}" for r in roles]

    col1, col2 = st.columns(2)
    with col1:
        selected_role_display = st.selectbox(
            "🎯 Target Job Role:",
            role_options,
            key="job_role_select"
        )
        selected_role = selected_role_display.split(" ", 1)[1]

    with col2:
        experience_level = st.selectbox(
            "📊 Experience Level:",
            [
                "Beginner",
                "Internship Seeker",
                "Fresher",
                "Working Professional",
                "Senior"
            ],
            key="exp_level_select"
        )

    # Extra skills
    st.markdown("**➕ Add Extra Skills** *(that are not on your GitHub)*")
    extra_skills_input = st.text_input(
        "Extra skills:",
        placeholder="e.g. Docker, AWS, Figma, System Design",
        label_visibility="collapsed",
        key="extra_skills_input"
    )
    extra_skills = [
        s.strip() for s in extra_skills_input.split(",")
        if s.strip()
    ] if extra_skills_input else []

    analyze_btn = st.button("🚀 Start Deep Analysis", key="career_analyze_btn")

    if analyze_btn and username:
        with st.status("🔄 Deep analysis in progress...", expanded=True) as status:
            st.write("📡 Fetching complete GitHub data...")
            time.sleep(0.3)
            st.write("🔤 Analyzing all repositories...")
            time.sleep(0.3)
            st.write("🤖 Running career ML analysis...")
            time.sleep(0.3)
            st.write(f"🎯 Matching against {selected_role} requirements...")
            time.sleep(0.3)
            st.write("📊 Building detailed report...")
            data, error = api_career_scan(
                username=username,
                job_role=selected_role,
                experience_level=experience_level,
                extra_skills=extra_skills,
                user_id=st.session_state.user.get("user_id") if st.session_state.user else None
            )
            if error:
                status.update(label=f"❌ {error}", state="error")
                st.stop()
            st.write("📄 Generating report...")
            time.sleep(0.2)
            status.update(label="✅ Analysis complete!", state="complete")

        st.session_state.career_data = data

    elif analyze_btn:
        st.warning("⚠️ Please enter a username!")

    if st.session_state.career_data:
        render_career_results(st.session_state.career_data)


# ════════════════════════════════
# CAREER RESULTS
# ════════════════════════════════
def render_career_results(data):
    profile = data["profile"]
    career = data["career"]
    cs = career["career_score"]
    red_flags = career["red_flags"]
    ats = career["ats"]

    st.divider()

    # Profile + Score header
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        if profile.get("avatar_url"):
            st.image(profile["avatar_url"], width=90)
    with col2:
        st.markdown(f"## {profile.get('name', profile.get('username'))}")
        if profile.get("bio"):
            st.caption(profile["bio"])
        st.markdown(f"""
        <span class="badge badge-blue">{data['developer_type']}</span>
        <span class="badge badge-green">{career['job_role']}</span>
        <span class="badge badge-purple">{career['experience_level']}</span>
        """, unsafe_allow_html=True)
    with col3:
        render_score_ring(cs["total_score"], "Career")
    with col4:
        render_score_ring(data["quick_scores"]["total_score"], "Profile")

    st.divider()

    # Quick summary card
    readiness = cs["readiness"]
    readiness_color = "green" if "🟢" in readiness["level"] else "yellow" if "🟡" in readiness["level"] else "red"
    st.markdown(f"""
    <div class="card-{readiness_color}">
        <h3 style="margin:0; color:#e6edf3;">
            {readiness['level']} — {readiness['message']}
        </h3>
        <p style="color:#8b949e; margin:8px 0 0 0;">
            Role: <strong>{career['job_role']}</strong> |
            Level: <strong>{career['experience_level']}</strong> |
            Career Score: <strong>{cs['total_score']}/100</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Summary cols
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**✅ Strengths**")
        for s in cs.get("strengths", [])[:3]:
            st.markdown(f"- {s}")
    with col2:
        st.markdown("**⚠️ Weaknesses**")
        for w in cs.get("weaknesses", [])[:3]:
            st.markdown(f"- {w}")
    with col3:
        st.markdown("**❌ Missing Skills**")
        missing = cs.get("missing_foundation", [])[:3]
        for m in missing:
            st.markdown(f"- {m}")

    st.divider()

    # Detailed scores
    render_section_title("📊 Detailed Score Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Foundation Skills (60 pts)**")
        for cat, info in cs["foundation_breakdown"].items():
            render_progress_bar(
                cat,
                info["score"],
                info["max"],
                "#58a6ff"
            )
        st.markdown("**Matched:**")
        for cat, info in cs["foundation_breakdown"].items():
            if info["matched"]:
                render_skills(info["matched"])

    with col2:
        st.markdown("**Modern 2026 Skills (40 pts)**")
        for cat, info in cs["modern_breakdown"].items():
            render_progress_bar(
                cat,
                info["score"],
                info["max"],
                "#3fb950"
            )
        st.markdown("**Matched:**")
        for cat, info in cs["modern_breakdown"].items():
            if info["matched"]:
                render_skills(info["matched"])

    st.divider()

    # ATS + Red flags
    col1, col2 = st.columns(2)
    with col1:
        render_section_title("🎯 ATS Score")
        render_score_ring(ats["ats_score"], "ATS")
        st.markdown(f"**{ats['ats_level']['level']}**")
        st.caption(ats["ats_level"]["message"])
        if ats.get("suggestions"):
            st.markdown("**Improvements:**")
            for s in ats["suggestions"]:
                st.markdown(f"→ {s}")

    with col2:
        render_section_title("🚩 Red Flags")
        severity = red_flags["severity"]
        st.markdown(f"**{severity['level']}** — {severity['message']}")
        for flag in red_flags["red_flags"]:
            st.markdown(f"""
            <div class="card-red" style="padding:10px; margin:8px 0;">
                <p style="color:#f85149; margin:0; font-size:13px;">
                    {flag['flag']}
                </p>
                <p style="color:#8b949e; margin:4px 0; font-size:12px;">
                    {flag['detail']}
                </p>
                <p style="color:#3fb950; margin:0; font-size:12px;">
                    💡 {flag['fix']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Company match
    render_section_title("🏢 Company Readiness")
    company_cols = st.columns(3)
    for i, (company, result) in enumerate(career["company_match"].items()):
        with company_cols[i % 3]:
            icon = result["status"]["icon"]
            label = result["status"]["label"]
            pct = result["match_percentage"]
            color = "green" if pct >= 80 else "yellow" if pct >= 55 else "red"
            st.markdown(f"""
            <div class="card-{color}">
                <p style="margin:0; font-weight:bold; color:#e6edf3;">
                    {icon} {company}
                </p>
                <p style="margin:4px 0; font-size:24px; font-weight:bold; color:#58a6ff;">
                    {pct}%
                </p>
                <p style="margin:0; font-size:12px; color:#8b949e;">
                    {result['description']}
                </p>
                <p style="margin:4px 0; font-size:11px; color:#8b949e;">
                    e.g. {', '.join(result['examples'][:2])}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Salary insight
    salary = career["salary"]
    if salary:
        render_section_title("💰 Salary Insight")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="card">
                <p style="color:#8b949e; margin:0; font-size:12px;">Current (India)</p>
                <p style="color:#58a6ff; font-size:22px; font-weight:bold; margin:4px 0;">
                    {salary['current_salary'].get('india', 'N/A')}
                </p>
                <p style="color:#8b949e; font-size:12px; margin:0;">
                    {salary['current_level']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <p style="color:#8b949e; margin:0; font-size:12px;">Current (Remote)</p>
                <p style="color:#3fb950; font-size:22px; font-weight:bold; margin:4px 0;">
                    {salary['current_salary'].get('remote', 'N/A')}
                </p>
                <p style="color:#8b949e; font-size:12px; margin:0;">
                    {salary['current_level']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if salary.get("next_salary"):
                st.markdown(f"""
                <div class="card-green">
                    <p style="color:#8b949e; margin:0; font-size:12px;">
                        Next Level (India)
                    </p>
                    <p style="color:#3fb950; font-size:22px; font-weight:bold; margin:4px 0;">
                        {salary['next_salary'].get('india', 'N/A')}
                    </p>
                    <p style="color:#8b949e; font-size:12px; margin:0;">
                        {salary['next_level']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        st.info(f"💡 {salary['insight']}")

    st.divider()

    # Roadmap
    render_section_title(f"🗺️ Your {career['roadmap'].get('duration', '')} Roadmap")
    roadmap = career["roadmap"]
    for week_data in roadmap.get("weeks", []):
        with st.expander(f"📅 {week_data['week']} — {week_data['title']}"):
            st.markdown("**Topics:**")
            for topic in week_data["topics"]:
                st.markdown(f"- {topic}")

            resources = week_data.get("resources", {})

            if resources.get("youtube"):
                st.markdown("**📺 YouTube:**")
                for yt in resources["youtube"]:
                    st.markdown(f"- [{yt['title']}]({yt['url']})")

            if resources.get("websites"):
                st.markdown("**🌐 Websites:**")
                for site in resources["websites"]:
                    st.markdown(f"- [{site['title']}]({site['url']})")

            if resources.get("practice"):
                st.markdown("**💻 Practice:**")
                for p in resources["practice"]:
                    st.markdown(f"- [{p['title']}]({p['url']})")

    st.divider()

    # Project suggestions
    render_section_title("💡 Recommended Projects (2026 Market)")
    for i, project in enumerate(career["projects"], 1):
        diff_color = {
            "Beginner": "green",
            "Intermediate": "yellow",
            "Advanced": "red"
        }.get(project["difficulty"], "blue")

        with st.expander(f"#{i} {project['title']} — ⏱️ {project['time']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Why build this?**")
                st.info(project["why"])
                st.markdown(f"**Tech Stack:** {', '.join(project['tech'])}")
                st.markdown("**Resources:**")
                for link in project.get("links", []):
                    st.markdown(f"- [{link['label']}]({link['url']})")
            with col2:
                st.markdown(f"""
                <div class="card-{diff_color}" style="text-align:center;">
                    <p style="margin:0; font-size:12px; color:#8b949e;">Difficulty</p>
                    <p style="margin:4px 0; font-weight:bold; color:#e6edf3;">
                        {project['difficulty']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Interview tips
    tips = career["interview_tips"]
    render_section_title("🎤 Interview Preparation")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Common Questions:**")
        for q in tips.get("common_questions", [])[:5]:
            st.markdown(f"- {q}")
        st.markdown("**Common Mistakes:**")
        for m in tips.get("common_mistakes", []):
            st.markdown(f"- ❌ {m}")

    with col2:
        st.markdown("**What Companies Look for in 2026:**")
        for item in tips.get("what_companies_look_for_2026", []):
            st.markdown(f"- ✅ {item}")
        st.markdown("**Portfolio Tips:**")
        for tip in tips.get("portfolio_tips", []):
            st.markdown(f"- 💡 {tip}")

        if tips.get("resources"):
            st.markdown("**Resources:**")
            for r in tips["resources"]:
                st.markdown(f"- [{r['title']}]({r['url']})")

    st.divider()

    # Notifications + PDF
    render_section_title("📬 Get Full Report")
    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_input(
            "📧 Email:",
            placeholder="your@email.com",
            key="career_email"
        )
    with col2:
        telegram = st.text_input(
            "📱 Telegram Chat ID:",
            placeholder="123456789",
            key="career_telegram"
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 Send Report", key="career_notify"):
            if email or telegram:
                try:
                    req.post(f"{API_URL}/notify/career-report", json={
                        "email": email or None,
                        "telegram_chat_id": telegram or None,
                        "name": profile.get("name", "Developer"),
                        "username": profile.get("username"),
                        "job_role": career["job_role"],
                        "career_score": cs["total_score"],
                        "readiness": cs["readiness"],
                        "experience_level": career["experience_level"],
                        "missing_skills": cs.get("missing_foundation", [])
                    }, timeout=30)
                    st.success("✅ Report sent!")
                except Exception:
                    st.error("❌ Could not send — check backend!")
            else:
                st.warning("Enter email or Telegram Chat ID!")

    # PDF Download
    st.markdown("---")
    col_dl, _ = st.columns([1, 2])
    with col_dl:
        try:
            pdf_bytes = report_gen.generate_career_report(data)
            username = profile.get("username", "report")
            role_slug = career.get("job_role", "career").lower().replace(" ", "_")
            st.download_button(
                label="📄 Download Career Report (PDF)",
                data=pdf_bytes,
                file_name=f"{username}_{role_slug}_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")


# ════════════════════════════════
# LEADERBOARD UI
# ════════════════════════════════
def render_leaderboard():
    render_section_title("🏆 Developer Leaderboard")

    from career.job_roles import get_all_roles
    roles = ["All Roles"] + get_all_roles()
    selected = st.selectbox("Filter by Role:", roles, key="lb_role")
    job_role = None if selected == "All Roles" else selected

    try:
        leaders = get_leaderboard(limit=20, job_role=job_role)
        if not leaders:
            st.info("No entries yet — analyze profiles to populate!")
            return

        for i, leader in enumerate(leaders, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 2, 1])
            with col1:
                st.markdown(f"**{medal}**")
            with col2:
                if leader.get("avatar_url"):
                    st.image(leader["avatar_url"], width=40)
            with col3:
                st.markdown(f"**@{leader['github_username']}**")
                st.caption(leader.get("developer_type", ""))
            with col4:
                st.caption(leader.get("job_role") or "General")
            with col5:
                st.markdown(f"**{leader['total_score']}/100**")

    except Exception as e:
        st.error(f"Could not load leaderboard: {e}")


# ════════════════════════════════
# MAIN APP
# ════════════════════════════════
def main():
    render_sidebar()

    # Header
    st.markdown("""
    <div style="text-align:center; padding: 30px 0 10px 0;">
        <h1 style="color:#e6edf3; margin:0; font-size:36px;">
            🐙 GitHub Career Analyzer
        </h1>
        <p style="color:#8b949e; font-size:16px; margin-top:8px;">
            ML-powered career readiness insights — 2026 market ready
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "⚡ Quick Scan",
        "🎯 Career Analyzer",
        "🏆 Leaderboard"
    ])

    with tab1:
        render_quick_scan()

    with tab2:
        render_career_analyzer()

    with tab3:
        render_leaderboard()


if __name__ == "__main__":
    main()