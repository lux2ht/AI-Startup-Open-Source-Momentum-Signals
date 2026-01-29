from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException

from .config import Settings
from .storage import list_signals


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="Momentum Signals", version="0.1.0")

    def _require_key(x_api_key: str | None = Header(default=None)) -> None:
        if x_api_key != settings.api.api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "signal_pack": "open-source repo momentum"}

    @app.get("/signals", dependencies=[Depends(_require_key)])
    def signals() -> list[dict]:
        records = list_signals(settings.storage.db_path)
        return [
            {
                "repo": record.repo,
                "stars": record.stars,
                "forks": record.forks,
                "commits_30d": record.commits_30d,
                "issues_30d": record.issues_30d,
                "contributors": record.contributors,
                "release_recency_days": record.release_recency_days,
                "star_velocity": record.star_velocity,
                "momentum_score": record.momentum_score,
                "updated_at": record.updated_at.isoformat(),
            }
            for record in records
        ]

    return app
