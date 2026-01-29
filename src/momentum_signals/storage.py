from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import RepoSignal


def init_db(db_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                repo TEXT PRIMARY KEY,
                stars INTEGER,
                forks INTEGER,
                commits_30d INTEGER,
                issues_30d INTEGER,
                contributors INTEGER,
                release_recency_days INTEGER,
                star_velocity REAL,
                momentum_score REAL,
                updated_at TEXT
            )
            """
        )
        conn.commit()


def upsert_signal(db_path: str, signal: RepoSignal) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO signals (
                repo, stars, forks, commits_30d, issues_30d, contributors,
                release_recency_days, star_velocity, momentum_score, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(repo) DO UPDATE SET
                stars=excluded.stars,
                forks=excluded.forks,
                commits_30d=excluded.commits_30d,
                issues_30d=excluded.issues_30d,
                contributors=excluded.contributors,
                release_recency_days=excluded.release_recency_days,
                star_velocity=excluded.star_velocity,
                momentum_score=excluded.momentum_score,
                updated_at=excluded.updated_at
            """,
            (
                signal.repo,
                signal.stars,
                signal.forks,
                signal.commits_30d,
                signal.issues_30d,
                signal.contributors,
                signal.release_recency_days,
                signal.star_velocity,
                signal.momentum_score,
                signal.updated_at.isoformat(),
            ),
        )
        conn.commit()


def list_signals(db_path: str) -> list[RepoSignal]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT repo, stars, forks, commits_30d, issues_30d, contributors,
                   release_recency_days, star_velocity, momentum_score, updated_at
            FROM signals
            ORDER BY momentum_score DESC
            """
        )
        rows = cursor.fetchall()

    signals = []
    for row in rows:
        signals.append(
            RepoSignal(
                repo=row[0],
                stars=row[1],
                forks=row[2],
                commits_30d=row[3],
                issues_30d=row[4],
                contributors=row[5],
                release_recency_days=row[6],
                star_velocity=row[7],
                momentum_score=row[8],
                updated_at=_parse_dt(row[9]),
            )
        )
    return signals


def _parse_dt(value: str) -> "datetime":
    from datetime import datetime

    return datetime.fromisoformat(value)
