# auth/github_auth.py

import os
import secrets
import httpx
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/callback?provider=github")

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def generate_state():
    """Generate a random state token for CSRF protection."""
    return secrets.token_urlsafe(32)


def get_github_auth_url(state: str = None):
    """Build GitHub OAuth authorization URL with CSRF state parameter."""
    if state is None:
        state = generate_state()

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "read:user user:email public_repo",
        "state": state,
    }
    query = urlencode(params)
    return f"{GITHUB_AUTH_URL}?{query}", state


async def get_github_token(code: str):
    """Exchange authorization code for access token with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            }
        )

        if response.status_code != 200:
            raise Exception(f"GitHub token exchange failed with status {response.status_code}")

        data = response.json()

        if "error" in data:
            error_desc = data.get("error_description", data["error"])
            raise Exception(f"GitHub OAuth error: {error_desc}")

        if "access_token" not in data:
            raise Exception("GitHub OAuth response missing access_token")

        return data


async def get_github_user(token: str):
    """Fetch GitHub user profile with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch GitHub user: status {response.status_code}")

        return response.json()


async def get_github_user_email(token: str):
    """Fetch primary email from GitHub with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )

        if response.status_code != 200:
            return None

        emails = response.json()

        if not isinstance(emails, list):
            return None

        primary = next(
            (e["email"] for e in emails if e.get("primary")),
            None
        )
        return primary