# auth/google_auth.py

import os
import secrets
import httpx
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback?provider=google")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def generate_state():
    """Generate a random state token for CSRF protection."""
    return secrets.token_urlsafe(32)


def get_google_auth_url(state: str = None):
    """Build Google OAuth authorization URL with CSRF state parameter."""
    if state is None:
        state = generate_state()

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state,
    }
    query = urlencode(params)
    return f"{GOOGLE_AUTH_URL}?{query}", state


async def get_google_token(code: str):
    """Exchange authorization code for access token with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )

        if response.status_code != 200:
            raise Exception(f"Google token exchange failed with status {response.status_code}")

        data = response.json()

        if "error" in data:
            error_desc = data.get("error_description", data["error"])
            raise Exception(f"Google OAuth error: {error_desc}")

        if "access_token" not in data:
            raise Exception("Google OAuth response missing access_token")

        return data


async def get_google_user(token: str):
    """Fetch Google user info with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Google user info: status {response.status_code}")

        data = response.json()

        if "error" in data:
            raise Exception(f"Google userinfo error: {data['error'].get('message', 'Unknown error')}")

        return data