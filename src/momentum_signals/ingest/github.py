from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import requests


def fetch_repo_stats(repos: list[str], token: str | None) -> list[dict[str, Any]]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    results = []
    for repo in repos:
        repo_data = _get_json(f"https://api.github.com/repos/{repo}", headers)
        commits_30d = _count_commits(repo, headers)
        issues_30d = _count_issues(repo, headers)
        contributors = _count_contributors(repo, headers)
        release_recency = _release_recency_days(repo, headers)
        star_velocity = _star_velocity(repo_data)
        results.append(
            {
                "repo": repo,
                "stars": int(repo_data.get("stargazers_count", 0)),
                "forks": int(repo_data.get("forks_count", 0)),
                "commits_30d": commits_30d,
                "issues_30d": issues_30d,
                "contributors": contributors,
                "release_recency_days": release_recency,
                "star_velocity": star_velocity,
            }
        )
    return results


def _get_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def _count_commits(repo: str, headers: dict[str, str]) -> int:
    since = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    response = requests.get(
        f"https://api.github.com/repos/{repo}/commits",
        headers=headers,
        params={"since": since, "per_page": 1},
        timeout=20,
    )
    response.raise_for_status()
    return _extract_total_count(response)


def _count_issues(repo: str, headers: dict[str, str]) -> int:
    since = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    response = requests.get(
        f"https://api.github.com/repos/{repo}/issues",
        headers=headers,
        params={"since": since, "state": "all", "per_page": 1},
        timeout=20,
    )
    response.raise_for_status()
    return _extract_total_count(response)


def _count_contributors(repo: str, headers: dict[str, str]) -> int:
    response = requests.get(
        f"https://api.github.com/repos/{repo}/contributors",
        headers=headers,
        params={"per_page": 1, "anon": "true"},
        timeout=20,
    )
    response.raise_for_status()
    return _extract_total_count(response)


def _release_recency_days(repo: str, headers: dict[str, str]) -> int:
    response = requests.get(
        f"https://api.github.com/repos/{repo}/releases/latest",
        headers=headers,
        timeout=20,
    )
    if response.status_code == 404:
        return 365
    response.raise_for_status()
    released_at = response.json().get("published_at")
    if not released_at:
        return 365
    release_date = datetime.fromisoformat(released_at.replace("Z", "+00:00"))
    return max(0, (datetime.utcnow() - release_date).days)


def _star_velocity(repo_data: dict[str, Any]) -> float:
    created_at = repo_data.get("created_at")
    if not created_at:
        return 0.0
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    days = max((datetime.utcnow() - created).days, 1)
    stars = int(repo_data.get("stargazers_count", 0))
    return round(stars / days * 30, 2)


def _extract_total_count(response: requests.Response) -> int:
    link = response.headers.get("Link", "")
    if "rel=\"last\"" not in link:
        return len(response.json())
    for part in link.split(","):
        if "rel=\"last\"" in part:
            url = part.split(";")[0].strip().strip("<>")
            return int(url.split("page=")[-1])
    return len(response.json())
