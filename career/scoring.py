# career/scoring.py

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from career.job_roles import get_role_info


# ════════════════════════════════
# MAIN SCORING FUNCTION
# ════════════════════════════════
def calculate_career_score(
    role_name,
    languages,
    repos,
    topics,
    profile,
    extra_skills=None,
    experience_level="Fresher"
):
    role = get_role_info(role_name)
    if not role:
        return None

    extra_skills = extra_skills or []
    all_user_langs = list(languages.keys())
    all_user_topics = topics or []

    # ════════════════════════════════
    # 1. FOUNDATION SCORE (60 pts)
    # ════════════════════════════════
    foundation_score, foundation_breakdown = calculate_foundation_score(
        role, all_user_langs, all_user_topics, extra_skills
    )

    # ════════════════════════════════
    # 2. MODERN 2026 SCORE (40 pts)
    # ════════════════════════════════
    modern_score, modern_breakdown = calculate_modern_score(
        role, all_user_langs, all_user_topics, extra_skills
    )

    # ════════════════════════════════
    # 3. PROJECT QUALITY SCORE (bonus)
    # ════════════════════════════════
    project_score, project_breakdown = calculate_project_score(
        role, repos
    )

    # ════════════════════════════════
    # 4. CONSISTENCY SCORE (bonus)
    # ════════════════════════════════
    consistency_score, consistency_breakdown = calculate_consistency_score(
        profile, repos
    )

    # ════════════════════════════════
    # TOTAL SCORE
    # ════════════════════════════════
    raw_total = foundation_score + modern_score + project_score + consistency_score
    total_score = min(round(raw_total, 1), 100)

    # ════════════════════════════════
    # READINESS LEVEL
    # ════════════════════════════════
    readiness = get_readiness_level(total_score, experience_level)

    # ════════════════════════════════
    # STRENGTHS & WEAKNESSES
    # ════════════════════════════════
    strengths = get_strengths(foundation_breakdown, modern_breakdown, project_breakdown)
    weaknesses = get_weaknesses(role, all_user_langs, all_user_topics, extra_skills)

    # ════════════════════════════════
    # MISSING SKILLS
    # ════════════════════════════════
    missing_foundation = get_missing_foundation(role, all_user_langs, extra_skills)
    missing_modern = get_missing_modern(role, all_user_langs, all_user_topics, extra_skills)

    return {
        "total_score": total_score,
        "foundation_score": round(foundation_score, 1),
        "modern_score": round(modern_score, 1),
        "project_score": round(project_score, 1),
        "consistency_score": round(consistency_score, 1),
        "readiness": readiness,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_foundation": missing_foundation,
        "missing_modern": missing_modern,
        "foundation_breakdown": foundation_breakdown,
        "modern_breakdown": modern_breakdown,
        "project_breakdown": project_breakdown,
        "consistency_breakdown": consistency_breakdown,
    }


# ════════════════════════════════
# FOUNDATION SCORE (60 pts)
# ════════════════════════════════
def calculate_foundation_score(role, user_langs, user_topics, extra_skills):
    score = 0
    breakdown = {}
    foundation = role.get("foundation_skills", {})

    all_user_skills = [s.lower() for s in user_langs + user_topics + extra_skills]

    # Languages (25 pts)
    required_langs = foundation.get("languages", [])
    matched_langs = [l for l in required_langs if l.lower() in all_user_skills]
    lang_score = min(25, (len(matched_langs) / max(len(required_langs), 1)) * 25)
    score += lang_score
    breakdown["Languages"] = {
        "score": round(lang_score, 1),
        "max": 25,
        "matched": matched_langs,
        "required": required_langs
    }

    # Frameworks (20 pts)
    required_frameworks = foundation.get("frameworks", [])
    matched_frameworks = [f for f in required_frameworks if f.lower() in all_user_skills]
    fw_score = min(20, (len(matched_frameworks) / max(len(required_frameworks), 1)) * 20)
    score += fw_score
    breakdown["Frameworks"] = {
        "score": round(fw_score, 1),
        "max": 20,
        "matched": matched_frameworks,
        "required": required_frameworks
    }

    # Tools (15 pts)
    required_tools = foundation.get("tools", [])
    matched_tools = [t for t in required_tools if t.lower() in all_user_skills]
    tool_score = min(15, (len(matched_tools) / max(len(required_tools), 1)) * 15)
    score += tool_score
    breakdown["Tools"] = {
        "score": round(tool_score, 1),
        "max": 15,
        "matched": matched_tools,
        "required": required_tools
    }

    return score, breakdown


# ════════════════════════════════
# MODERN 2026 SCORE (40 pts)
# ════════════════════════════════
def calculate_modern_score(role, user_langs, user_topics, extra_skills):
    score = 0
    breakdown = {}
    modern = role.get("modern_2026_skills", {})

    all_user_skills = [s.lower() for s in user_langs + user_topics + extra_skills]

    # AI Tools (10 pts)
    ai_tools = modern.get("ai_tools", [])
    matched_ai = [t for t in ai_tools if t.lower() in all_user_skills]
    ai_score = min(10, (len(matched_ai) / max(len(ai_tools), 1)) * 10)
    score += ai_score
    breakdown["AI Tools"] = {
        "score": round(ai_score, 1),
        "max": 10,
        "matched": matched_ai,
        "required": ai_tools
    }

    # Modern Frameworks (10 pts)
    modern_fw = modern.get("frameworks", [])
    matched_mfw = [f for f in modern_fw if f.lower() in all_user_skills]
    mfw_score = min(10, (len(matched_mfw) / max(len(modern_fw), 1)) * 10)
    score += mfw_score
    breakdown["Modern Frameworks"] = {
        "score": round(mfw_score, 1),
        "max": 10,
        "matched": matched_mfw,
        "required": modern_fw
    }

    # 2026 Skills (15 pts)
    modern_skills = modern.get("skills", [])
    matched_ms = [s for s in modern_skills if s.lower() in all_user_skills]
    ms_score = min(15, (len(matched_ms) / max(len(modern_skills), 1)) * 15)
    score += ms_score
    breakdown["2026 Skills"] = {
        "score": round(ms_score, 1),
        "max": 15,
        "matched": matched_ms,
        "required": modern_skills
    }

    # Testing (5 pts)
    testing = modern.get("testing", [])
    matched_test = [t for t in testing if t.lower() in all_user_skills]
    test_score = min(5, (len(matched_test) / max(len(testing), 1)) * 5)
    score += test_score
    breakdown["Testing"] = {
        "score": round(test_score, 1),
        "max": 5,
        "matched": matched_test,
        "required": testing
    }

    return score, breakdown


# ════════════════════════════════
# PROJECT QUALITY SCORE (bonus)
# ════════════════════════════════
def calculate_project_score(role, repos):
    score = 0
    breakdown = {}

    original_repos = [r for r in repos if not r.get("fork")]
    role_keywords = role.get("repo_keywords", [])

    # Relevant repos (5 pts)
    relevant = [
        r for r in original_repos
        if any(kw in ((r.get("name") or "") + (r.get("description") or "")).lower()
               for kw in role_keywords)
    ]
    relevance_score = min(5, len(relevant) * 1.5)
    score += relevance_score
    breakdown["Relevant Projects"] = {
        "score": round(relevance_score, 1),
        "max": 5,
        "count": len(relevant)
    }

    # README quality (3 pts)
    with_readme = sum(1 for r in original_repos if r.get("description"))
    readme_score = min(3, (with_readme / max(len(original_repos), 1)) * 3)
    score += readme_score
    breakdown["README Quality"] = {
        "score": round(readme_score, 1),
        "max": 3,
        "count": with_readme
    }

    # Stars received (2 pts)
    total_stars = sum(r.get("stargazers_count", 0) for r in original_repos)
    star_score = min(2, total_stars * 0.01)
    score += star_score
    breakdown["Stars Received"] = {
        "score": round(star_score, 1),
        "max": 2,
        "count": total_stars
    }

    return score, breakdown


# ════════════════════════════════
# CONSISTENCY SCORE (bonus)
# ════════════════════════════════
def calculate_consistency_score(profile, repos):
    from datetime import datetime
    score = 0
    breakdown = {}

    # Account age (2 pts)
    created_at = profile.get("created_at", "2020-01-01T00:00:00Z")
    account_age = (datetime.now() - datetime.strptime(
        created_at, "%Y-%m-%dT%H:%M:%SZ")).days / 365
    age_score = min(2, account_age * 0.5)
    score += age_score
    breakdown["Account Age"] = {
        "score": round(age_score, 1),
        "max": 2,
        "years": round(account_age, 1)
    }

    # Recent activity (3 pts)
    recent = [
        r for r in repos
        if r.get("pushed_at", "")[:4] == str(datetime.now().year)
    ]
    activity_score = min(3, len(recent) * 0.5)
    score += activity_score
    breakdown["Recent Activity"] = {
        "score": round(activity_score, 1),
        "max": 3,
        "recent_repos": len(recent)
    }

    return score, breakdown


# ════════════════════════════════
# READINESS LEVEL
# ════════════════════════════════
def get_readiness_level(score, experience_level):
    if experience_level in ["Beginner", "Internship Seeker"]:
        if score >= 70: return {"level": "🟢 Ready", "message": "Great profile for your level!"}
        elif score >= 45: return {"level": "🟡 Almost Ready", "message": "Few more things to learn!"}
        else: return {"level": "🔴 Keep Learning", "message": "Focus on foundation skills first!"}
    elif experience_level == "Fresher":
        if score >= 75: return {"level": "🟢 Job Ready", "message": "Strong profile for entry level!"}
        elif score >= 50: return {"level": "🟡 Almost There", "message": "Polish your projects!"}
        else: return {"level": "🔴 Needs Work", "message": "Build more projects first!"}
    else:
        if score >= 80: return {"level": "🟢 Highly Competitive", "message": "Excellent profile!"}
        elif score >= 60: return {"level": "🟡 Competitive", "message": "Add modern skills!"}
        else: return {"level": "🔴 Needs Upgrade", "message": "Update your tech stack!"}


# ════════════════════════════════
# STRENGTHS
# ════════════════════════════════
def get_strengths(foundation_bd, modern_bd, project_bd):
    strengths = []
    for category, data in foundation_bd.items():
        if data["score"] >= data["max"] * 0.7:
            strengths.append(f"✅ Strong {category}")
    for category, data in modern_bd.items():
        if data["score"] >= data["max"] * 0.6:
            strengths.append(f"🚀 Good {category}")
    if project_bd.get("Relevant Projects", {}).get("count", 0) >= 2:
        strengths.append("📁 Good relevant projects")
    return strengths[:5]


# ════════════════════════════════
# WEAKNESSES
# ════════════════════════════════
def get_weaknesses(role, user_langs, user_topics, extra_skills):
    weaknesses = []
    all_user = [s.lower() for s in user_langs + user_topics + extra_skills]
    foundation = role.get("foundation_skills", {})
    modern = role.get("modern_2026_skills", {})

    required_langs = foundation.get("languages", [])
    missing_langs = [l for l in required_langs if l.lower() not in all_user]
    if missing_langs:
        weaknesses.append(f"⚠️ Missing languages: {', '.join(missing_langs[:3])}")

    modern_skills = modern.get("skills", [])
    missing_modern = [s for s in modern_skills if s.lower() not in all_user]
    if missing_modern:
        weaknesses.append(f"⚠️ Missing 2026 skills: {', '.join(missing_modern[:3])}")

    testing = modern.get("testing", [])
    missing_tests = [t for t in testing if t.lower() not in all_user]
    if missing_tests:
        weaknesses.append(f"⚠️ No testing frameworks found")

    return weaknesses[:5]


# ════════════════════════════════
# MISSING SKILLS
# ════════════════════════════════
def get_missing_foundation(role, user_langs, extra_skills):
    all_user = [s.lower() for s in user_langs + extra_skills]
    foundation = role.get("foundation_skills", {})
    missing = []
    for category, skills in foundation.items():
        for skill in skills:
            if skill.lower() not in all_user:
                missing.append(skill)
    return missing


def get_missing_modern(role, user_langs, user_topics, extra_skills):
    all_user = [s.lower() for s in user_langs + user_topics + extra_skills]
    modern = role.get("modern_2026_skills", {})
    missing = []
    for category, skills in modern.items():
        for skill in skills:
            if skill.lower() not in all_user:
                missing.append(skill)
    return missing


# ════════════════════════════════
# TEST
# ════════════════════════════════
if __name__ == "__main__":
    from github_api import get_complete_user_data

    print("Testing scoring system...")
    data, error = get_complete_user_data("torvalds")

    if error:
        print(f"Error: {error}")
    else:
        result = calculate_career_score(
            role_name="Backend Developer",
            languages=data["languages"],
            repos=data["repos"],
            topics=data["topics"],
            profile=data["profile"],
            extra_skills=["Docker", "Linux"],
            experience_level="Senior"
        )

        print(f"\nRole: Backend Developer")
        print(f"Total Score: {result['total_score']}/100")
        print(f"Foundation: {result['foundation_score']}/60")
        print(f"Modern 2026: {result['modern_score']}/40")
        print(f"Readiness: {result['readiness']['level']}")
        print(f"\nStrengths: {result['strengths']}")
        print(f"\nWeaknesses: {result['weaknesses']}")
        print(f"\nMissing Foundation: {result['missing_foundation'][:5]}")
        print(f"Missing Modern: {result['missing_modern'][:5]}")