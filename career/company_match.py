# career/company_match.py

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


COMPANY_REQUIREMENTS = {
    "Startups": {
        "min_score": 45,
        "min_repos": 2,
        "min_stars": 0,
        "needs_modern_skills": False,
        "description": "Fast-paced, generalist skills valued",
        "examples": ["Zepto", "Razorpay", "CRED", "Groww"]
    },
    "Mid-size Companies": {
        "min_score": 55,
        "min_repos": 4,
        "min_stars": 5,
        "needs_modern_skills": False,
        "description": "Balanced tech stack, team collaboration",
        "examples": ["Zoho", "Freshworks", "Postman", "BrowserStack"]
    },
    "Product Companies": {
        "min_score": 65,
        "min_repos": 5,
        "min_stars": 10,
        "needs_modern_skills": True,
        "description": "Strong fundamentals + modern skills needed",
        "examples": ["Atlassian", "Swiggy", "Zomato", "PhonePe"]
    },
    "FAANG/MAANG": {
        "min_score": 82,
        "min_repos": 8,
        "min_stars": 30,
        "needs_modern_skills": True,
        "description": "Top-tier DSA + system design + modern stack",
        "examples": ["Google", "Microsoft", "Amazon", "Meta"]
    },
    "Remote Opportunities": {
        "min_score": 60,
        "min_repos": 5,
        "min_stars": 10,
        "needs_modern_skills": True,
        "description": "Strong portfolio + communication skills",
        "examples": ["Toptal", "Upwork", "Remote.com", "Turing"]
    },
    "Government/PSU": {
        "min_score": 40,
        "min_repos": 1,
        "min_stars": 0,
        "needs_modern_skills": False,
        "description": "Basic skills + certifications valued",
        "examples": ["TCS", "Infosys", "Wipro", "HCL"]
    },
}


def calculate_company_match(
    total_score,
    modern_score,
    repos,
    profile
):
    results = {}
    original_repos = [r for r in repos if not r.get("fork")]
    total_stars = sum(r.get("stargazers_count", 0) for r in original_repos)
    repo_count = len(original_repos)

    for company_type, req in COMPANY_REQUIREMENTS.items():
        match_score = 0
        reasons_pass = []
        reasons_fail = []

        # Score check
        if total_score >= req["min_score"]:
            match_score += 40
            reasons_pass.append(f"Overall score {total_score} meets requirement")
        else:
            gap = req["min_score"] - total_score
            reasons_fail.append(f"Score {total_score} is {gap} points below requirement")

        # Repos check
        if repo_count >= req["min_repos"]:
            match_score += 25
            reasons_pass.append(f"Repo count {repo_count} meets requirement")
        else:
            reasons_fail.append(f"Need {req['min_repos']} repos, have {repo_count}")

        # Stars check
        if total_stars >= req["min_stars"]:
            match_score += 20
            reasons_pass.append(f"Star count looks good")
        else:
            reasons_fail.append(f"Need more project visibility ({total_stars} stars)")

        # Modern skills check
        if req["needs_modern_skills"]:
            if modern_score >= 15:
                match_score += 15
                reasons_pass.append("Modern 2026 skills present")
            else:
                reasons_fail.append("Missing modern AI/2026 skills")
        else:
            match_score += 15

        results[company_type] = {
            "match_percentage": min(match_score, 100),
            "status": get_match_status(match_score),
            "description": req["description"],
            "examples": req["examples"],
            "reasons_pass": reasons_pass,
            "reasons_fail": reasons_fail,
        }

    return results


def get_match_status(match_score):
    if match_score >= 80:
        return {"icon": "✅", "label": "Ready", "color": "green"}
    elif match_score >= 55:
        return {"icon": "⚠️", "label": "Almost Ready", "color": "orange"}
    else:
        return {"icon": "❌", "label": "Not Yet", "color": "red"}


# Test
if __name__ == "__main__":
    from github_api import get_complete_user_data
    from career.scoring import calculate_career_score

    data, error = get_complete_user_data("torvalds")
    if not error:
        score_result = calculate_career_score(
            role_name="Backend Developer",
            languages=data["languages"],
            repos=data["repos"],
            topics=data["topics"],
            profile=data["profile"],
            extra_skills=[],
            experience_level="Senior"
        )

        results = calculate_company_match(
            total_score=score_result["total_score"],
            modern_score=score_result["modern_score"],
            repos=data["repos"],
            profile=data["profile"]
        )

        print("Company Match Results:")
        for company, result in results.items():
            print(f"\n{result['status']['icon']} {company}")
            print(f"   Match: {result['match_percentage']}%")
            print(f"   Status: {result['status']['label']}")