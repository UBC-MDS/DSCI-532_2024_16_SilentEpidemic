import requests
from datetime import datetime

REPO_NAME = "UBC-MDS/DSCI-532_2024_16_SilentEpidemic"
REPO_URL = f"https://github.com/{REPO_NAME}"
API_ENDPOINT = f"https://api.github.com/repos/{REPO_NAME}"


def get_repo_last_updated_time():
    repo_info = requests.get(API_ENDPOINT).json()
    return datetime.fromisoformat(repo_info['pushed_at'])
