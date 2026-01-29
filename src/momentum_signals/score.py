from __future__ import annotations

from datetime import datetime, timezone

from .models import RepoSignal


def score_repo(raw: dict, weights: dict[str, float]) -> RepoSignal:
    commits_30d = int(raw.get("commits_30d", 0))
    star_velocity = float(raw.get("star_velocity", 0.0))
    issues_30d = int(raw.get("issues_30d", 0))
    contributors = int(raw.get("contributors", 0))
    release_recency_days = int(raw.get("release_recency_days", 365))

    momentum = (
        commits_30d * weights.get("commits_30d", 0.0)
        + star_velocity * weights.get("star_velocity", 0.0)
        + issues_30d * weights.get("issues_30d", 0.0)
        + contributors * weights.get("contributors", 0.0)
        + _release_boost(release_recency_days) * weights.get("release_recency", 0.0)
    )

    return RepoSignal(
        repo=str(raw.get("repo")),
        stars=int(raw.get("stars", 0)),
        forks=int(raw.get("forks", 0)),
        commits_30d=commits_30d,
        issues_30d=issues_30d,
        contributors=contributors,
        release_recency_days=release_recency_days,
        star_velocity=star_velocity,
        momentum_score=round(momentum, 2),
        updated_at=datetime.now(timezone.utc),
    )


def _release_boost(release_recency_days: int) -> float:
    return max(0.0, 100.0 - release_recency_days)
