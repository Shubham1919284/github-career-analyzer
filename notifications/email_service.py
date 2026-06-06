# notifications/email_service.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@resend.dev")
APP_URL = os.getenv("APP_URL", "http://localhost:8501")
RESEND_URL = "https://api.resend.com/emails"


# ════════════════════════════════
# SEND EMAIL
# ════════════════════════════════
async def send_email(to: str, subject: str, html: str):
    if not RESEND_API_KEY:
        print("⚠️ No Resend API key found!")
        return False

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                RESEND_URL,
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": EMAIL_FROM,
                    "to": [to],
                    "subject": subject,
                    "html": html
                }
            )
            if response.status_code != 200:
                print(f"⚠️ Resend API error: {response.status_code} — {response.text}")
                return False
            return True
    except httpx.RequestError as e:
        print(f"⚠️ Email send failed: {e}")
        return False


# ════════════════════════════════
# EMAIL TEMPLATES
# ════════════════════════════════
def quick_scan_email(name, username, total_score, dev_type):
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">

        <div style="background: #0d1117; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">🐙 GitHub Career Analyzer</h1>
            <p style="color: #8b949e;">Your profile analysis is ready!</p>
        </div>

        <div style="background: #161b22; padding: 30px; border: 1px solid #30363d;">

            <h2 style="color: #58a6ff;">Hi {name}! 👋</h2>
            <p style="color: #c9d1d9;">
                Your GitHub profile <strong style="color: #58a6ff;">@{username}</strong>
                has been analyzed. Here's your summary:
            </p>

            <div style="background: #0d1117; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center;">
                <h1 style="color: #58a6ff; font-size: 48px; margin: 0;">{total_score}<span style="font-size: 24px;">/100</span></h1>
                <p style="color: #8b949e; margin: 5px 0;">Developer Score</p>
                <span style="background: #1f6feb; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px;">
                    {dev_type}
                </span>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{APP_URL}"
                   style="background: #238636; color: white; padding: 12px 30px;
                          border-radius: 8px; text-decoration: none; font-size: 16px;">
                    View Full Report →
                </a>
            </div>

            <hr style="border: 1px solid #30363d;">
            <p style="color: #8b949e; font-size: 12px; text-align: center;">
                GitHub Career Analyzer | Free &amp; Open Source
            </p>
        </div>
    </div>
    """


def career_report_email(name, username, job_role, career_score, readiness, experience_level):
    # Safely extract readiness level and color
    readiness_level = "Unknown"
    if isinstance(readiness, dict):
        readiness_level = readiness.get("level", "Unknown")

    readiness_color_map = {
        "🟢": "#238636",
        "🟡": "#d29922",
        "🔴": "#da3633"
    }
    # Try to match first character of readiness level for color
    readiness_color = "#238636"  # default green
    if readiness_level and len(readiness_level) > 0:
        readiness_color = readiness_color_map.get(readiness_level[0], "#238636")

    if isinstance(career_score, dict):
        total_score = career_score.get("total_score", 0)
        foundation_score = career_score.get("foundation_score", 0)
        modern_score = career_score.get("modern_score", 0)
    else:
        total_score = career_score
        foundation_score = 0
        modern_score = 0

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">

        <div style="background: #0d1117; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">🎯 Career Readiness Report</h1>
            <p style="color: #8b949e;">Your detailed career analysis is ready!</p>
        </div>

        <div style="background: #161b22; padding: 30px; border: 1px solid #30363d;">

            <h2 style="color: #58a6ff;">Hi {name}! 👋</h2>

            <p style="color: #c9d1d9;">
                Your career readiness analysis for
                <strong style="color: #58a6ff;">{job_role}</strong>
                as a <strong>{experience_level}</strong> is complete!
            </p>

            <div style="background: #0d1117; border-radius: 10px; padding: 20px; margin: 20px 0;">
                <table style="width: 100%; text-align: center;">
                    <tr>
                        <td>
                            <h2 style="color: #58a6ff; margin: 0;">{total_score}/100</h2>
                            <p style="color: #8b949e; margin: 5px 0; font-size: 12px;">Career Score</p>
                        </td>
                        <td>
                            <h2 style="color: {readiness_color}; margin: 0;">{readiness_level}</h2>
                            <p style="color: #8b949e; margin: 5px 0; font-size: 12px;">Readiness</p>
                        </td>
                    </tr>
                </table>
            </div>

            <div style="background: #0d1117; border-radius: 8px; padding: 15px; margin: 15px 0;">
                <p style="color: #58a6ff; margin: 0 0 8px 0; font-weight: bold;">📊 Score Breakdown</p>
                <p style="color: #c9d1d9; margin: 5px 0;">
                    Foundation Skills: {foundation_score}/60
                </p>
                <p style="color: #c9d1d9; margin: 5px 0;">
                    Modern 2026 Skills: {modern_score}/40
                </p>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{APP_URL}"
                   style="background: #238636; color: white; padding: 12px 30px;
                          border-radius: 8px; text-decoration: none; font-size: 16px;">
                    View Full Report + Roadmap →
                </a>
            </div>

            <hr style="border: 1px solid #30363d;">
            <p style="color: #8b949e; font-size: 12px; text-align: center;">
                GitHub Career Analyzer | Free &amp; Open Source
            </p>
        </div>
    </div>
    """


def weekly_reminder_email(name, username):
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">

        <div style="background: #0d1117; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0;">📅 Weekly Progress Check</h1>
        </div>

        <div style="background: #161b22; padding: 30px; border: 1px solid #30363d;">

            <h2 style="color: #58a6ff;">Hey {name}! 👋</h2>

            <p style="color: #c9d1d9;">
                It's been a week since your last analysis.
                Have you been coding? Let's check your progress!
            </p>

            <div style="background: #0d1117; border-radius: 8px; padding: 15px; margin: 15px 0;">
                <p style="color: #58a6ff; font-weight: bold; margin: 0 0 10px 0;">
                    💡 This week, try to:
                </p>
                <p style="color: #c9d1d9; margin: 5px 0;">✅ Push at least 3 commits</p>
                <p style="color: #c9d1d9; margin: 5px 0;">✅ Add README to 1 project</p>
                <p style="color: #c9d1d9; margin: 5px 0;">✅ Work on 1 new feature</p>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{APP_URL}"
                   style="background: #238636; color: white; padding: 12px 30px;
                          border-radius: 8px; text-decoration: none; font-size: 16px;">
                    Re-analyze My Profile →
                </a>
            </div>

            <hr style="border: 1px solid #30363d;">
            <p style="color: #8b949e; font-size: 12px; text-align: center;">
                GitHub Career Analyzer | Free &amp; Open Source
            </p>
        </div>
    </div>
    """


# ════════════════════════════════
# MAIN SEND FUNCTIONS
# ════════════════════════════════
async def send_quick_scan_email(to, name, username, total_score, dev_type):
    html = quick_scan_email(name, username, total_score, dev_type)
    return await send_email(
        to=to,
        subject=f"🐙 Your GitHub Profile Score: {total_score}/100",
        html=html
    )


async def send_career_report_email(
    to, name, username,
    job_role, career_score, readiness, experience_level
):
    html = career_report_email(
        name, username, job_role,
        career_score, readiness, experience_level
    )

    # Safely extract readiness level for subject line
    readiness_level = "Unknown"
    if isinstance(readiness, dict):
        readiness_level = readiness.get("level", "Unknown")

    return await send_email(
        to=to,
        subject=f"🎯 Career Report: {job_role} — {readiness_level}",
        html=html
    )


async def send_weekly_reminder(to, name, username):
    html = weekly_reminder_email(name, username)
    return await send_email(
        to=to,
        subject="📅 Weekly Progress Check — GitHub Career Analyzer",
        html=html
    )


# Test
if __name__ == "__main__":
    import asyncio

    async def test():
        result = await send_quick_scan_email(
            to="test@gmail.com",
            name="Test User",
            username="torvalds",
            total_score=87.5,
            dev_type="Systems Developer 🔧"
        )
        print(f"Email sent: {result}")

    asyncio.run(test())