# backend/main.py

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import time
import secrets

from auth.google_auth import get_google_auth_url, get_google_token, get_google_user
from auth.github_auth import get_github_auth_url, get_github_token, get_github_user, get_github_user_email
from database.connection import create_or_update_user, get_user_by_email

from github_api import get_complete_user_data, check_rate_limit
from analyzer import detect_developer_type, calculate_developer_score, detect_skills, detect_coding_style
from career.scoring import calculate_career_score
from career.red_flags import detect_red_flags
from career.ats_score import calculate_ats_score
from career.company_match import calculate_company_match
from career.salary_insight import get_salary_insight
from career.roadmap import get_roadmap
from career.projects import get_project_suggestions
from career.interview_tips import get_interview_tips
from notifications.email_service import (
    send_quick_scan_email,
    send_career_report_email,
    send_weekly_reminder
)
from notifications.telegram_service import (
    send_quick_scan_telegram,
    send_career_report_telegram,
    send_weekly_reminder_telegram
)
from database.connection import (
    init_db, save_search, update_leaderboard,
    get_leaderboard, get_recent_searches, get_app_stats
)

# ════════════════════════════════
# APP SETUP
# ════════════════════════════════
app = FastAPI(
    title="GitHub Career Analyzer API",
    description="ML-powered GitHub profile & career readiness analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session store (simple in-memory)
sessions = {}


@app.get("/auth/google")
def google_login():
    return {"url": get_google_auth_url()}


@app.get("/auth/github")
def github_login():
    return {"url": get_github_auth_url()}


@app.get("/auth/callback")
async def auth_callback(
    request: Request,
    code: str,
    provider: str = "google"
):
    try:
        if provider == "google":
            token_data = await get_google_token(code)
            access_token = token_data.get("access_token")
            user_info = await get_google_user(access_token)

            user_id = create_or_update_user(
                email=user_info.get("email"),
                name=user_info.get("name"),
                avatar_url=user_info.get("picture"),
                auth_provider="google"
            )

            session_token = secrets.token_hex(32)
            sessions[session_token] = {
                "user_id": user_id,
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "avatar_url": user_info.get("picture"),
                "provider": "google"
            }

        else:  # GitHub
            token_data = await get_github_token(code)
            access_token = token_data.get("access_token")
            user_info = await get_github_user(access_token)
            email = await get_github_user_email(access_token)

            user_id = create_or_update_user(
                email=email or f"{user_info.get('login')}@github.com",
                name=user_info.get("name") or user_info.get("login"),
                avatar_url=user_info.get("avatar_url"),
                auth_provider="github",
                github_username=user_info.get("login")
            )

            session_token = secrets.token_hex(32)
            sessions[session_token] = {
                "user_id": user_id,
                "email": email,
                "name": user_info.get("name") or user_info.get("login"),
                "avatar_url": user_info.get("avatar_url"),
                "github_username": user_info.get("login"),
                "provider": "github"
            }

        return {
            "session_token": session_token,
            "user": sessions[session_token]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/auth/me")
def get_current_user(session_token: str):
    user = sessions.get(session_token)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@app.post("/auth/logout")
def logout(session_token: str):
    sessions.pop(session_token, None)
    return {"message": "Logged out successfully"}


# Simple in-memory cache
_cache = {}
CACHE_TTL = 3600  # 1 hour


# ════════════════════════════════
# CACHE HELPERS
# ════════════════════════════════
def get_cache(key):
    if key in _cache:
        data, expiry = _cache[key]
        if time.time() < expiry:
            return data
        del _cache[key]
    return None


def set_cache(key, data):
    _cache[key] = (data, time.time() + CACHE_TTL)


# ════════════════════════════════
# REQUEST MODELS
# ════════════════════════════════
class QuickScanRequest(BaseModel):
    username: str


class CareerAnalyzeRequest(BaseModel):
    username: str
    job_role: str
    experience_level: str
    extra_skills: Optional[list] = None
    user_id: Optional[int] = None


class LeaderboardRequest(BaseModel):
    github_username: str
    name: str
    avatar_url: str
    developer_type: str
    total_score: float
    job_role: Optional[str] = None
    experience_level: Optional[str] = None


class NotificationRequest(BaseModel):
    email: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    name: str
    username: str
    total_score: float
    dev_type: str
    skills: Optional[list] = None


class CareerNotificationRequest(BaseModel):
    email: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    name: str
    username: str
    job_role: str
    career_score: float
    readiness: dict
    experience_level: str
    missing_skills: Optional[list] = []


# ════════════════════════════════
# STARTUP
# ════════════════════════════════
@app.on_event("startup")
def startup():
    init_db()
    print("GitHub Career Analyzer API started!")


# ════════════════════════════════
# ROOT
# ════════════════════════════════
@app.get("/")
def root():
    return {
        "message": "GitHub Career Analyzer API 🚀",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ════════════════════════════════
# HEALTH CHECK
# ════════════════════════════════
@app.get("/health")
def health():
    remaining, limit = check_rate_limit()
    return {
        "status": "healthy",
        "github_api_remaining": remaining,
        "github_api_limit": limit,
        "cache_size": len(_cache)
    }


# ════════════════════════════════
# QUICK SCAN
# ════════════════════════════════
@app.post("/scan/quick")
def quick_scan(req: QuickScanRequest):
    username = req.username.strip().lower()

    # Cache check
    cache_key = f"quick_{username}"
    cached = get_cache(cache_key)
    if cached:
        return {**cached, "source": "cache"}

    try:
        # Fetch data
        data, error = get_complete_user_data(username)
        if error:
            raise HTTPException(status_code=404, detail=error)

        profile = data["profile"]
        repos = data["repos"]
        languages = data["languages"]
        topics = data["topics"]

        # Analysis
        dev_type, type_scores = detect_developer_type(languages)
        total_score, breakdown = calculate_developer_score(profile, repos)
        skills = detect_skills(languages, repos)
        coding_style = detect_coding_style(repos)
        red_flags = detect_red_flags(profile, repos, languages)
        ats = calculate_ats_score(profile, repos, languages, dev_type, topics)

        result = {
            "source": "fresh",
            "profile": {
                "username": profile.get("login"),
                "name": profile.get("name"),
                "bio": profile.get("bio"),
                "avatar_url": profile.get("avatar_url"),
                "location": profile.get("location"),
                "company": profile.get("company"),
                "blog": profile.get("blog"),
                "public_repos": profile.get("public_repos"),
                "followers": profile.get("followers"),
                "following": profile.get("following"),
                "created_at": profile.get("created_at"),
            },
            "scores": {
                "total_score": total_score,
                "breakdown": breakdown,
            },
            "developer_type": dev_type,
            "type_scores": type_scores,
            "skills": skills,
            "coding_style": coding_style,
            "languages": dict(
                sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
            "top_repos": [
                {
                    "name": r["name"],
                    "description": r.get("description"),
                    "stars": r["stargazers_count"],
                    "forks": r["forks_count"],
                    "language": r.get("language"),
                    "url": r["html_url"],
                    "fork": r.get("fork", False),
                }
                for r in sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:10]
            ],
            "red_flags": red_flags,
            "ats": ats,
        }

        # Save to cache
        set_cache(cache_key, result)

        # Save to DB (non-fatal)
        try:
            save_search(
                github_username=username,
                mode="quick",
                total_score=total_score,
                ats_score=ats["ats_score"]
            )
            update_leaderboard(
                github_username=username,
                name=profile.get("name", username),
                avatar_url=profile.get("avatar_url", ""),
                developer_type=dev_type,
                total_score=total_score
            )
        except Exception:
            pass  # DB errors must not break the response

        return result

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Quick scan failed: {str(e)}")


# ════════════════════════════════
# CAREER ANALYZE
# ════════════════════════════════
@app.post("/scan/career")
def career_analyze(req: CareerAnalyzeRequest):
    username = req.username.strip().lower()
    job_role = req.job_role
    experience_level = req.experience_level
    extra_skills = req.extra_skills if req.extra_skills is not None else []

    # Cache check
    cache_key = f"career_{username}_{job_role}_{experience_level}"
    cached = get_cache(cache_key)
    if cached:
        return {**cached, "source": "cache"}

    try:
        # Fetch GitHub data
        data, error = get_complete_user_data(username)
        if error:
            raise HTTPException(status_code=404, detail=error)

        profile = data["profile"]
        repos = data["repos"]
        languages = data["languages"]
        topics = data["topics"]

        # Quick scan analysis
        dev_type, type_scores = detect_developer_type(languages)
        total_score, score_breakdown = calculate_developer_score(profile, repos)
        skills = detect_skills(languages, repos)
        coding_style = detect_coding_style(repos)

        # Career-specific analysis
        career_score = calculate_career_score(
            role_name=job_role,
            languages=languages,
            repos=repos,
            topics=topics,
            profile=profile,
            extra_skills=extra_skills,
            experience_level=experience_level
        )
        red_flags = detect_red_flags(profile, repos, languages)
        ats = calculate_ats_score(profile, repos, languages, job_role, topics)
        company_match = calculate_company_match(
            total_score=career_score["total_score"],
            modern_score=career_score["modern_score"],
            repos=repos,
            profile=profile
        )
        salary = get_salary_insight(job_role, experience_level)
        roadmap = get_roadmap(job_role, experience_level)
        projects = get_project_suggestions(job_role, experience_level)
        interview_tips = get_interview_tips(job_role)

        result = {
            "source": "fresh",
            "profile": {
                "username": profile.get("login"),
                "name": profile.get("name"),
                "bio": profile.get("bio"),
                "avatar_url": profile.get("avatar_url"),
                "location": profile.get("location"),
                "company": profile.get("company"),
                "blog": profile.get("blog"),
                "public_repos": profile.get("public_repos"),
                "followers": profile.get("followers"),
                "following": profile.get("following"),
                "created_at": profile.get("created_at"),
            },
            "quick_scores": {
                "total_score": total_score,
                "breakdown": score_breakdown,
            },
            "developer_type": dev_type,
            "type_scores": type_scores,
            "skills": skills,
            "coding_style": coding_style,
            "languages": dict(
                sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
            "top_repos": [
                {
                    "name": r["name"],
                    "description": r.get("description"),
                    "stars": r["stargazers_count"],
                    "forks": r["forks_count"],
                    "language": r.get("language"),
                    "url": r["html_url"],
                    "fork": r.get("fork", False),
                }
                for r in sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:10]
            ],
            "career": {
                "job_role": job_role,
                "experience_level": experience_level,
                "extra_skills": extra_skills,
                "career_score": career_score,
                "red_flags": red_flags,
                "ats": ats,
                "company_match": company_match,
                "salary": salary,
                "roadmap": roadmap,
                "projects": projects[:7],
                "interview_tips": interview_tips,
            }
        }

        # Save to cache
        set_cache(cache_key, result)

        # Save to DB (non-fatal if it fails)
        try:
            save_search(
                github_username=username,
                mode="career",
                job_role=job_role,
                experience_level=experience_level,
                total_score=total_score,
                career_score=career_score["total_score"],
                ats_score=ats["ats_score"],
                user_id=req.user_id
            )
            update_leaderboard(
                github_username=username,
                name=profile.get("name", username),
                avatar_url=profile.get("avatar_url", ""),
                developer_type=dev_type,
                total_score=career_score["total_score"],
                job_role=job_role,
                experience_level=experience_level
            )
        except Exception:
            pass  # DB errors must not break the response

        return result

    except HTTPException:
        raise  # Re-raise 404s cleanly
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Career analysis failed: {str(e)}"
        )

# ════════════════════════════════
# LEADERBOARD
# ════════════════════════════════
@app.get("/leaderboard")
def get_leaderboard_api(job_role: Optional[str] = None, limit: int = 10):
    return {
        "leaderboard": get_leaderboard(limit=limit, job_role=job_role),
        "total": limit
    }


# ════════════════════════════════
# RECENT SEARCHES
# ════════════════════════════════
@app.get("/history")
def get_history(user_id: Optional[int] = None, limit: int = 10):
    return {
        "history": get_recent_searches(user_id=user_id, limit=limit)
    }


# ════════════════════════════════
# APP STATS
# ════════════════════════════════
@app.get("/stats")
def get_stats():
    return get_app_stats()


# ════════════════════════════════
# RATE LIMIT STATUS
# ════════════════════════════════
@app.get("/rate-limit")
def rate_limit_status():
    remaining, limit = check_rate_limit()
    return {
        "remaining": remaining,
        "limit": limit,
        "percentage": round((remaining / limit) * 100, 1)
    }


# ════════════════════════════════
# NOTIFICATIONS
# ════════════════════════════════
@app.post("/notify/quick-scan")
async def notify_quick_scan(req: NotificationRequest):
    results = {}

    if req.email:
        results["email"] = await send_quick_scan_email(
            to=req.email,
            name=req.name,
            username=req.username,
            total_score=req.total_score,
            dev_type=req.dev_type
        )

    if req.telegram_chat_id:
        results["telegram"] = await send_quick_scan_telegram(
            chat_id=req.telegram_chat_id,
            name=req.name,
            username=req.username,
            total_score=req.total_score,
            dev_type=req.dev_type,
            skills=req.skills
        )

    return {"sent": results}


@app.post("/notify/career-report")
async def notify_career_report(req: CareerNotificationRequest):
    results = {}

    if req.email:
        results["email"] = await send_career_report_email(
            to=req.email,
            name=req.name,
            username=req.username,
            job_role=req.job_role,
            career_score=req.career_score,
            readiness=req.readiness,
            experience_level=req.experience_level
        )

    if req.telegram_chat_id:
        results["telegram"] = await send_career_report_telegram(
            chat_id=req.telegram_chat_id,
            name=req.name,
            username=req.username,
            job_role=req.job_role,
            career_score=req.career_score,
            readiness=req.readiness,
            experience_level=req.experience_level,
            missing_skills=req.missing_skills
        )

    return {"sent": results}


# ════════════════════════════════
# RUN
# ════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)