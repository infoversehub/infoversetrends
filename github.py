import base64
import requests

from config import (
    GITHUB_TOKEN,
)

# ==========================================
# GITHUB CONFIG
# ==========================================

GITHUB_OWNER = "infoversehub"

GITHUB_REPO = "infoverse-hub"

BRANCH = "main"

API = "https://api.github.com"
# ==========================================
# GET FILE SHA
# ==========================================

def get_file_sha(path):

    url = (
        f"{API}/repos/"
        f"{GITHUB_OWNER}/"
        f"{GITHUB_REPO}/"
        f"contents/{path}"
    )

    response = requests.get(

        url,

        headers={

            "Authorization": f"Bearer {GITHUB_TOKEN}",

            "Accept": "application/vnd.github+json"

        }

    )

    if response.status_code == 200:

        return response.json()["sha"]

    return None
  # ==========================================
# CREATE / UPDATE FILE
# ==========================================

def upload_file(path, content, message):

    url = (
        f"{API}/repos/"
        f"{GITHUB_OWNER}/"
        f"{GITHUB_REPO}/"
        f"contents/{path}"
    )

    sha = get_file_sha(path)

    payload = {

        "message": message,

        "content": base64.b64encode(
            content.encode("utf-8")
        ).decode("utf-8"),

        "branch": BRANCH

    }

    if sha:

        payload["sha"] = sha

    response = requests.put(

        url,

        headers={

            "Authorization": f"Bearer {GITHUB_TOKEN}",

            "Accept": "application/vnd.github+json"

        },

        json=payload

    )

    if response.status_code in (200, 201):

        return True

    print("GitHub Error:")
    print(response.text)

    return False
