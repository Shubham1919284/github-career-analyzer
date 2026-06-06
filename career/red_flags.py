# career/red_flags.py

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timezone


def detect_red_flags(profile, repos, languages):

    red_flags = []
    warnings = []
    positive_flags = []

    original_repos = [r for r in repos if not r.get("fork")]
    forked_repos = [r for r in repos if r.get("fork")]
    total_repos = len(repos)

    # ════════════════════════════════
    # 🚩 RED FLAGS (Serious Issues)
    # ════════════════════════════════

    # 1. Tutorial Hell Detection
    tutorial_keywords = [
        "todo", "to-do", "todoapp", "calculator", "weather-app",
        "crud", "hello-world", "test", "demo", "sample",
        "practice", "learning", "tutorial", "beginner", "basic"
    ]
    tutorial_repos = []
    for repo in original_repos:
        name = repo.get("name", "").lower()
        desc = (repo.get("description") or "").lower()
        if any(kw in name or kw in desc for kw in tutorial_keywords):
            tutorial_repos.append(repo["name"])

    tutorial_ratio = len(tutorial_repos) / max(len(original_repos), 1)
    if tutorial_ratio > 0.6:
        red_flags.append({
            "flag": "🚩 Tutorial Hell Detected",
            "detail": f"{len(tutorial_repos)} out of {len(original_repos)} repos are basic tutorial projects ({', '.join(tutorial_repos[:3])}...)",
            "fix": "Build at least 3 original, complex projects that solve real problems"
        })

    # 2. All Repos Forked
    if total_repos > 0:
        fork_ratio = len(forked_repos) / total_repos
        if fork_ratio > 0.7:
            red_flags.append({
                "flag": "🚩 No Original Work",
                "detail": f"{len(forked_repos)} out of {total_repos} repos are forked — no original contributions visible",
                "fix": "Create original projects that showcase your own ideas and skills"
            })

    # 3. No Recent Activity
    last_activities = []
    for repo in repos:
        pushed = repo.get("pushed_at", "")
        if pushed:
            last_activities.append(pushed)

    if last_activities:
        last_activity = max(last_activities)
        last_date = datetime.strptime(last_activity, "%Y-%m-%dT%H:%M:%SZ")
        days_inactive = (datetime.now(timezone.utc) - last_date.replace(tzinfo=timezone.utc)).days
        if days_inactive > 180:
            red_flags.append({
                "flag": "🚩 Long Inactivity",
                "detail": f"No activity for {days_inactive} days — last push was {last_activity[:10]}",
                "fix": "Push code regularly — even small updates show consistency to recruiters"
            })
        elif days_inactive > 90:
            warnings.append({
                "flag": "⚠️ Moderate Inactivity",
                "detail": f"No activity for {days_inactive} days",
                "fix": "Try to push code at least once a week"
            })

    # 4. No README in Any Repo
    repos_with_desc = sum(1 for r in original_repos if r.get("description"))
    if len(original_repos) > 0:
        readme_ratio = repos_with_desc / len(original_repos)
        if readme_ratio < 0.2:
            red_flags.append({
                "flag": "🚩 Missing READMEs",
                "detail": f"Only {repos_with_desc} out of {len(original_repos)} repos have descriptions — recruiters skip repos without README",
                "fix": "Add a proper README to every project with setup instructions and screenshots"
            })

    # 5. Empty Profile
    if not profile.get("bio"):
        warnings.append({
            "flag": "⚠️ Empty Bio",
            "detail": "No bio on GitHub profile — recruiters check this first",
            "fix": "Add a short professional bio mentioning your skills and what you build"
        })

    if not profile.get("avatar_url") or "gravatar" in profile.get("avatar_url", ""):
        warnings.append({
            "flag": "⚠️ No Profile Picture",
            "detail": "Default avatar — looks unprofessional",
            "fix": "Add a professional profile picture"
        })

    # 6. Very Low Repos
    if len(original_repos) < 3:
        red_flags.append({
            "flag": "🚩 Too Few Original Projects",
            "detail": f"Only {len(original_repos)} original repos — not enough to showcase skills",
            "fix": "Build at least 5-6 original projects relevant to your target role"
        })

    # 7. No Stars At All
    total_stars = sum(r.get("stargazers_count", 0) for r in original_repos)
    if total_stars == 0 and len(original_repos) > 3:
        warnings.append({
            "flag": "⚠️ Zero Stars",
            "detail": "None of your projects have been starred — low visibility",
            "fix": "Share your projects on LinkedIn, Twitter, and developer communities"
        })

    # ════════════════════════════════
    # ✅ POSITIVE FLAGS
    # ════════════════════════════════

    if len(original_repos) >= 8:
        positive_flags.append("✅ Prolific developer — many original projects")

    if repos_with_desc / max(len(original_repos), 1) > 0.8:
        positive_flags.append("✅ Excellent documentation habits")

    if profile.get("bio"):
        positive_flags.append("✅ Professional bio present")

    if profile.get("blog"):
        positive_flags.append("✅ Personal website/portfolio linked")

    if total_stars > 50:
        positive_flags.append(f"✅ Good community recognition — {total_stars} stars")

    if len(languages) >= 5:
        positive_flags.append(f"✅ Diverse tech stack — {len(languages)} languages")

    # ════════════════════════════════
    # SCORE IMPACT
    # ════════════════════════════════
    penalty = len(red_flags) * 5 + len(warnings) * 2
    bonus = len(positive_flags) * 2
    net_impact = bonus - penalty

    return {
        "red_flags": red_flags,
        "warnings": warnings,
        "positive_flags": positive_flags,
        "total_red_flags": len(red_flags),
        "total_warnings": len(warnings),
        "total_positives": len(positive_flags),
        "score_impact": net_impact,
        "severity": get_severity(len(red_flags))
    }


def get_severity(red_flag_count):
    if red_flag_count == 0:
        return {"level": "🟢 Clean Profile", "message": "No major red flags!"}
    elif red_flag_count <= 2:
        return {"level": "🟡 Minor Issues", "message": "Fix these before applying"}
    else:
        return {"level": "🔴 Needs Attention", "message": "Address these urgently"}


# Test
if __name__ == "__main__":
    from github_api import get_complete_user_data

    data, error = get_complete_user_data("torvalds")
    if not error:
        result = detect_red_flags(
            data["profile"],
            data["repos"],
            data["languages"]
        )
        print(f"Severity: {result['severity']['level']}")
        print(f"Red Flags: {result['total_red_flags']}")
        print(f"Warnings: {result['total_warnings']}")
        print(f"Positives: {result['total_positives']}")
        print(f"Score Impact: {result['score_impact']}")
        print("\nRed Flags:")
        for flag in result["red_flags"]:
            print(f"  {flag['flag']}: {flag['detail']}")
        print("\nPositives:")
        for p in result["positive_flags"]:
            print(f"  {p}")