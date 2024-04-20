import requests
from datetime import datetime
from constants import API_ENDPOINT


def get_repo_last_updated_time():
    repo_info = requests.get(API_ENDPOINT).json()
    return datetime.fromisoformat(repo_info['pushed_at'])
