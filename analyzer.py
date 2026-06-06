
from __future__ import annotations

from collections import Counter


def detect_developer_type(languages):
	normalized = {str(name).lower(): count for name, count in (languages or {}).items()}
	if not normalized:
		return "Systems Developer", {"Systems Developer": 100}

	top_language = max(normalized, key=normalized.get)
	type_scores = Counter()

	if top_language in {"python", "r", "julia"}:
		type_scores["ML/AI Engineer"] += 60
		type_scores["Data Scientist"] += 55
		type_scores["Backend Developer"] += 30
	elif top_language in {"javascript", "typescript", "html", "css"}:
		type_scores["Frontend Developer"] += 60
		type_scores["Full Stack Developer"] += 50
		type_scores["Backend Developer"] += 20
	elif top_language in {"java", "kotlin", "swift", "objective-c", "dart"}:
		type_scores["Android Developer"] += 45
		type_scores["iOS Developer"] += 45
		type_scores["Backend Developer"] += 35
	elif top_language in {"go", "rust", "c", "c++", "shell", "powershell", "yaml"}:
		type_scores["DevOps Engineer"] += 50
		type_scores["Cloud Engineer"] += 45
		type_scores["Backend Developer"] += 30
	elif top_language == "sql":
		type_scores["Data Scientist"] += 55
		type_scores["Data Engineer"] += 55
		type_scores["Backend Developer"] += 20
	else:
		type_scores["Backend Developer"] += 35
		type_scores["Full Stack Developer"] += 35
		type_scores["Systems Developer"] += 30

	top_type = type_scores.most_common(1)[0][0]
	return top_type, dict(type_scores)


def calculate_developer_score(profile, repos):
	original_repos = [repo for repo in (repos or []) if not repo.get("fork")]
	total_stars = sum(repo.get("stargazers_count", 0) for repo in original_repos)
	with_descriptions = sum(1 for repo in original_repos if repo.get("description"))

	score = 0.0
	breakdown = {}

	profile_score = 0.0
	if profile.get("bio"):
		profile_score += 20
	if profile.get("blog"):
		profile_score += 10
	if profile.get("location"):
		profile_score += 5
	if profile.get("company"):
		profile_score += 5
	breakdown["Profile"] = round(profile_score, 1)
	score += profile_score

	project_score = min(35.0, len(original_repos) * 5.0)
	breakdown["Projects"] = round(project_score, 1)
	score += project_score

	visibility_score = min(20.0, total_stars * 0.5)
	breakdown["Visibility"] = round(visibility_score, 1)
	score += visibility_score

	documentation_score = 0.0
	if original_repos:
		documentation_score = min(20.0, (with_descriptions / len(original_repos)) * 20.0)
	breakdown["Documentation"] = round(documentation_score, 1)
	score += documentation_score

	return min(round(score, 1), 100.0), breakdown


def detect_skills(languages, repos):
	skills = set()

	for language in (languages or {}).keys():
		skills.add(language)

	for repo in repos or []:
		text = f"{repo.get('name', '')} {repo.get('description') or ''}".lower()
		keyword_map = {
			"docker": "Docker",
			"kubernetes": "Kubernetes",
			"fastapi": "FastAPI",
			"django": "Django",
			"react": "React",
			"next": "Next.js",
			"terraform": "Terraform",
			"spark": "Apache Spark",
			"pytorch": "PyTorch",
			"tensorflow": "TensorFlow",
			"sql": "SQL",
			"ml": "Machine Learning",
			"ai": "AI",
		}
		for keyword, skill in keyword_map.items():
			if keyword in text:
				skills.add(skill)

	return sorted(skills)


def detect_coding_style(repos):
	original_repos = [repo for repo in (repos or []) if not repo.get("fork")]
	repo_count = len(original_repos)
	with_descriptions = sum(1 for repo in original_repos if repo.get("description"))
	total_stars = sum(repo.get("stargazers_count", 0) for repo in original_repos)

	if repo_count >= 8:
		pace = "high-output"
	elif repo_count >= 4:
		pace = "steady"
	else:
		pace = "focused"

	if repo_count and with_descriptions / repo_count >= 0.75:
		documentation = "well-documented"
	elif repo_count and with_descriptions / repo_count >= 0.4:
		documentation = "moderately documented"
	else:
		documentation = "light documentation"

	if total_stars >= 50:
		visibility = "widely shared"
	elif total_stars >= 10:
		visibility = "growing visibility"
	else:
		visibility = "low external visibility"

	return {
		"pace": pace,
		"documentation": documentation,
		"visibility": visibility,
		"original_repos": repo_count,
		"described_repos": with_descriptions,
		"stars": total_stars,
	}
