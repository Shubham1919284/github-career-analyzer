import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"
else:
    import sys
    print("Warning: GITHUB_TOKEN not set — unauthenticated requests may be rate-limited.", file=sys.stderr)
BASE_URL = "https://api.github.com"


# ✅ User Profile
def get_user_profile(username):
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"error": "User not found"}
    elif response.status_code == 401:
        return {"error": "Invalid token"}
    elif response.status_code == 403:
        return {"error": "API rate limit hit! Try after 1 hour"}
    else:
        return {"error": f"Something went wrong: {response.status_code}"}


# ✅ User Repositories
def get_user_repos(username):
    repos = []
    page = 1
    while True:
        url = f"{BASE_URL}/users/{username}/repos?per_page=100&page={page}&sort=updated"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


# ✅ Repo Languages
def get_repo_languages(username, repo_name):
    url = f"{BASE_URL}/repos/{username}/{repo_name}/languages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}


# ✅ All Languages Combined (parallel, capped at top 20 original repos)
def get_all_languages(username, repos):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_languages = {}

    # Seed from primary language field first (free, no extra API call)
    for repo in repos:
        lang = repo.get("language")
        if lang:
            all_languages[lang] = all_languages.get(lang, 0) + 1000

    # Fetch detailed breakdown for top 20 original repos in parallel
    original_repos = [r for r in repos if not r.get("fork")][:20]

    def fetch_langs(repo):
        return get_repo_languages(username, repo["name"])

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_langs, repo): repo for repo in original_repos}
        for future in as_completed(futures):
            try:
                langs = future.result()
                for lang, bytes_count in langs.items():
                    all_languages[lang] = all_languages.get(lang, 0) + bytes_count
            except Exception:
                pass

    return all_languages


# ✅ Repo Topics
def get_repo_topics(username, repo_name):
    url = f"{BASE_URL}/repos/{username}/{repo_name}/topics"
    headers = {**HEADERS, "Accept": "application/vnd.github.mercy-preview+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("topics", [])
    return []


# ✅ All Topics Combined (parallel, capped at top 15 original repos)
def get_all_topics(username, repos):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_topics = set()
    original_repos = [r for r in repos if not r.get("fork")][:15]

    def fetch_topics(repo):
        return get_repo_topics(username, repo["name"])

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_topics, repo): repo for repo in original_repos}
        for future in as_completed(futures):
            try:
                topics = future.result()
                all_topics.update(topics)
            except Exception:
                pass

    return list(all_topics)


# ✅ Commit Activity
def get_commit_activity(username, repo_name):
    url = f"{BASE_URL}/repos/{username}/{repo_name}/stats/commit_activity"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []


# ✅ Rate Limit Check
def check_rate_limit():
    url = f"{BASE_URL}/rate_limit"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        remaining = data["rate"]["remaining"]
        limit = data["rate"]["limit"]
        return remaining, limit
    return 0, 5000


# ✅ Complete User Data (Single Call)
def get_complete_user_data(username):
    profile = get_user_profile(username)
    if "error" in profile:
        return None, profile["error"]

    repos = get_user_repos(username)
    languages = get_all_languages(username, repos)
    topics = get_all_topics(username, repos)

    return {
        "profile": profile,
        "repos": repos,
        "languages": languages,
        "topics": topics,
    }, None


# ✅ Test
if __name__ == "__main__":
    print("Testing GitHub API...")
    data, error = get_complete_user_data("torvalds")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Name: {data['profile'].get('name')}")
        print(f"Repos: {len(data['repos'])}")
        print(f"Languages: {len(data['languages'])}")
        print(f"Topics: {data['topics'][:5]}")
        remaining, limit = check_rate_limit()
        print(f"API Requests: {remaining}/{limit}")