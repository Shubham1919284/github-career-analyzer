# notifications/telegram_service.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def _get_base_url():
    """Build Telegram API base URL lazily to avoid None token at import time."""
    if not BOT_TOKEN:
        return None
    return f"https://api.telegram.org/bot{BOT_TOKEN}"


# ════════════════════════════════
# SEND MESSAGE
# ════════════════════════════════
async def send_telegram_message(chat_id: str, text: str):
    base_url = _get_base_url()
    if not base_url:
        print("⚠️ No Telegram bot token found!")
        return False

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML"
                }
            )
            if response.status_code != 200:
                print(f"⚠️ Telegram API error: {response.status_code} — {response.text}")
                return False
            return True
    except httpx.RequestError as e:
        print(f"⚠️ Telegram send failed: {e}")
        return False


# ════════════════════════════════
# MESSAGE TEMPLATES
# ════════════════════════════════
def quick_scan_message(name, username, total_score, dev_type, skills):
    skills_text = " | ".join(skills[:4]) if skills else "N/A"
    return f"""
🐙 <b>GitHub Profile Analysis Complete!</b>

👤 <b>Profile:</b> @{username}
🏆 <b>Score:</b> {total_score}/100
💻 <b>Type:</b> {dev_type}
🛠 <b>Skills:</b> {skills_text}

<i>Open the app for your full report!</i>
    """.strip()


def career_report_message(
    name, username, job_role,
    career_score, readiness, experience_level,
    missing_skills
):
    missing = ", ".join(missing_skills[:3]) if missing_skills else "None"

    # Safely extract readiness level
    readiness_level = "Unknown"
    if isinstance(readiness, dict):
        readiness_level = readiness.get("level", "Unknown")

    return f"""
🎯 <b>Career Readiness Report Ready!</b>

👤 <b>Profile:</b> @{username}
💼 <b>Role:</b> {job_role}
📊 <b>Level:</b> {experience_level}
🏆 <b>Career Score:</b> {career_score}/100
✅ <b>Readiness:</b> {readiness_level}

⚠️ <b>Top Missing Skills:</b>
{missing}

<i>Open the app for full roadmap + resources!</i>
    """.strip()


def red_flag_alert_message(username, red_flags):
    flags_text = "\n".join(
        [f"🚩 {f['flag']}" for f in red_flags[:3] if isinstance(f, dict) and 'flag' in f]
    )
    if not flags_text:
        flags_text = "🚩 Issues detected — check the app for details."
    return f"""
⚠️ <b>Red Flags Detected on @{username}</b>

{flags_text}

<i>Fix these before applying to jobs!</i>
    """.strip()


def weekly_reminder_message(name, username):
    return f"""
📅 <b>Weekly Progress Check!</b>

Hey {name}! 👋

It's been a week — time to re-analyze your profile @{username}!

This week, try to:
✅ Push at least 3 commits
✅ Add README to 1 project
✅ Work on 1 new feature

<i>Open the app to re-analyze!</i>
    """.strip()


# ════════════════════════════════
# MAIN SEND FUNCTIONS
# ════════════════════════════════
async def send_quick_scan_telegram(
    chat_id, name, username,
    total_score, dev_type, skills
):
    msg = quick_scan_message(
        name, username, total_score, dev_type, skills
    )
    return await send_telegram_message(chat_id, msg)


async def send_career_report_telegram(
    chat_id, name, username,
    job_role, career_score, readiness,
    experience_level, missing_skills
):
    msg = career_report_message(
        name, username, job_role,
        career_score, readiness,
        experience_level, missing_skills
    )
    return await send_telegram_message(chat_id, msg)


async def send_red_flag_telegram(chat_id, username, red_flags):
    if not red_flags:
        return False
    msg = red_flag_alert_message(username, red_flags)
    return await send_telegram_message(chat_id, msg)


async def send_weekly_reminder_telegram(chat_id, name, username):
    msg = weekly_reminder_message(name, username)
    return await send_telegram_message(chat_id, msg)


# ════════════════════════════════
# GET CHAT ID HELPER
# ════════════════════════════════
async def get_updates():
    base_url = _get_base_url()
    if not base_url:
        print("⚠️ No Telegram bot token found!")
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/getUpdates")
            data = response.json()
            if data.get("result"):
                for update in data["result"]:
                    msg = update.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    username = msg.get("from", {}).get("username")
                    print(f"Chat ID: {chat_id} | Username: @{username}")
            return data
    except httpx.RequestError as e:
        print(f"⚠️ Failed to get Telegram updates: {e}")
        return None


# Test
if __name__ == "__main__":
    import asyncio

    async def test():
        print("Getting updates (send /start to your bot first)...")
        await get_updates()

    asyncio.run(test())