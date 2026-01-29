from datetime import datetime, timezone

from momentum_signals.models import RepoSignal
from momentum_signals.storage import init_db, list_signals, upsert_signal


def test_storage_round_trip(tmp_path):
    db_path = tmp_path / "signals.db"
    init_db(str(db_path))

    signal = RepoSignal(
        repo="example/repo",
        stars=10,
        forks=2,
        commits_30d=5,
        issues_30d=1,
        contributors=3,
        release_recency_days=10,
        star_velocity=2.5,
        momentum_score=12.3,
        updated_at=datetime.now(timezone.utc),
    )
    upsert_signal(str(db_path), signal)

    signals = list_signals(str(db_path))

    assert len(signals) == 1
    assert signals[0].repo == "example/repo"
