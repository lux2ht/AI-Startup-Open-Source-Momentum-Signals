from __future__ import annotations

from .config import Settings
from .ingest.github import fetch_repo_stats
from .ingest.sample import load_sample_repos
from .score import score_repo
from .storage import init_db, upsert_signal


def run_update(settings: Settings) -> list[str]:
    init_db(settings.storage.db_path)

    if settings.github.enabled:
        raw_repos = fetch_repo_stats(settings.github.repos, settings.github.token)
    else:
        raw_repos = load_sample_repos()

    updated = []
    for raw in raw_repos:
        signal = score_repo(raw, settings.scoring.weights)
        upsert_signal(settings.storage.db_path, signal)
        updated.append(signal.repo)

    return updated
