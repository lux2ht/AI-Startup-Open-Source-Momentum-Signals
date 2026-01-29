from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RepoSignal:
    repo: str
    stars: int
    forks: int
    commits_30d: int
    issues_30d: int
    contributors: int
    release_recency_days: int
    star_velocity: float
    momentum_score: float
    updated_at: datetime
