# career/ats_score.py

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def calculate_ats_score(profile, repos, languages, role_name, topics):

    score = 0
    breakdown = {}
    suggestions = []

    # ════════════════════════════════
    # 1. Profile Completeness (25 pts)
    # ════════════════════════════════
    profile_score = 0

    if profile.get("name"):
        profile_score += 5
    else:
        suggestions.append("Add your full name to GitHub profile")

    if profile.get("bio"):
        profile_score += 5
    else:
        suggestions.append("Add a professional bio mentioning your role and skills")

    if profile.get("location"):
        profile_score += 3
    else:
        suggestions.append("Add your location — helps with local job matching")

    if profile.get("blog"):
        profile_score += 5
    else:
        suggestions.append("Add your portfolio/LinkedIn URL in website field")

    if profile.get("company"):
        profile_score += 3

    if profile.get("twitter_username"):
        profile_score += 2

    if profile.get("email"):
        profile_score += 2

    score += profile_score
    breakdown["Profile Completeness"] = {
        "score": profile_score,
        "max": 25
    }

    # ════════════════════════════════
    # 2. Keyword Relevance (25 pts)
    # ════════════════════════════════
    role_lower = role_name.lower()
    bio = (profile.get("bio") or "").lower()
    all_repo_text = " ".join([
        (r.get("name") or "") + " " + (r.get("description") or "")
        for r in repos
    ]).lower()

    keyword_score = 0
    lang_names = [l.lower() for l in languages.keys()]
    topic_names = [t.lower() for t in topics]

    # Role keywords in bio
    role_words = role_lower.split()
    bio_matches = sum(1 for w in role_words if w in bio)
    keyword_score += min(10, bio_matches * 5)

    # Languages as keywords
    keyword_score += min(10, len(lang_names) * 1.5)

    # Topics as keywords
    keyword_score += min(5, len(topic_names) * 1)

    score += keyword_score
    breakdown["Keyword Relevance"] = {
        "score": round(keyword_score, 1),
        "max": 25
    }

    # ════════════════════════════════
    # 3. Activity Score (25 pts)
    # ════════════════════════════════
    from datetime import datetime
    activity_score = 0

    # Public repos count
    public_repos = profile.get("public_repos", 0)
    activity_score += min(10, public_repos * 0.5)

    # Followers
    followers = profile.get("followers", 0)
    activity_score += min(10, followers * 0.02)

    # Account age
    created_at = profile.get("created_at", "2023-01-01T00:00:00Z")
    account_age = (datetime.now() - datetime.strptime(
        created_at, "%Y-%m-%dT%H:%M:%SZ")).days / 365
    activity_score += min(5, account_age)

    score += activity_score
    breakdown["Activity"] = {
        "score": round(activity_score, 1),
        "max": 25
    }

    # ════════════════════════════════
    # 4. Project Quality (25 pts)
    # ════════════════════════════════
    quality_score = 0
    original_repos = [r for r in repos if not r.get("fork")]

    # Repos with description
    with_desc = sum(1 for r in original_repos if r.get("description"))
    quality_score += min(10, (with_desc / max(len(original_repos), 1)) * 10)

    # Stars
    total_stars = sum(r.get("stargazers_count", 0) for r in original_repos)
    quality_score += min(10, total_stars * 0.1)

    # Original repos count
    quality_score += min(5, len(original_repos) * 0.5)

    score += quality_score
    breakdown["Project Quality"] = {
        "score": round(quality_score, 1),
        "max": 25
    }

    # ════════════════════════════════
    # FINAL ATS SCORE
    # ════════════════════════════════
    final_score = min(round(score, 1), 100)

    return {
        "ats_score": final_score,
        "breakdown": breakdown,
        "suggestions": suggestions,
        "ats_level": get_ats_level(final_score)
    }


def get_ats_level(score):
    if score >= 80:
        return {"level": "🟢 ATS Optimized", "message": "Profile will pass most ATS filters"}
    elif score >= 60:
        return {"level": "🟡 Moderate", "message": "Some improvements needed"}
    elif score >= 40:
        return {"level": "🔴 Needs Work", "message": "Profile may get filtered out"}
    else:
        return {"level": "⛔ High Risk", "message": "Complete profile overhaul needed"}


# Test
if __name__ == "__main__":
    from github_api import get_complete_user_data

    data, error = get_complete_user_data("torvalds")
    if not error:
        result = calculate_ats_score(
            data["profile"],
            data["repos"],
            data["languages"],
            "Backend Developer",
            data["topics"]
        )
        print(f"ATS Score: {result['ats_score']}/100")
        print(f"Level: {result['ats_level']['level']}")
        print(f"Message: {result['ats_level']['message']}")
        print("\nBreakdown:")
        for k, v in result["breakdown"].items():
            print(f"  {k}: {v['score']}/{v['max']}")
        print("\nSuggestions:")
        for s in result["suggestions"]:
            print(f"  → {s}")