from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import os
import yaml


@dataclass
class AppConfig:
    name: str
    environment: str


@dataclass
class ApiConfig:
    host: str
    port: int
    api_key: str


@dataclass
class StorageConfig:
    db_path: str


@dataclass
class GithubSourceConfig:
    enabled: bool
    token: str
    repos: list[str]


@dataclass
class ScoringConfig:
    weights: dict[str, float]


@dataclass
class Settings:
    app: AppConfig
    api: ApiConfig
    storage: StorageConfig
    github: GithubSourceConfig
    scoring: ScoringConfig


def _env_override(value: str | None, env_value: str | None) -> str | None:
    return env_value if env_value not in (None, "") else value


def load_settings(path: str) -> Settings:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text())

    app = AppConfig(**raw["app"])
    api_raw = raw["api"]
    api = ApiConfig(
        host=api_raw["host"],
        port=int(api_raw["port"]),
        api_key=_env_override(api_raw["api_key"], _get_env("MOMENTUM_API_KEY"))
        or api_raw["api_key"],
    )
    storage_raw = raw["storage"]
    storage = StorageConfig(
        db_path=_env_override(storage_raw["db_path"], _get_env("MOMENTUM_DB_PATH"))
        or storage_raw["db_path"],
    )
    github_raw = raw["sources"]["github"]
    github = GithubSourceConfig(
        enabled=bool(github_raw["enabled"]),
        token=_env_override(github_raw.get("token"), _get_env("MOMENTUM_GITHUB_TOKEN"))
        or "",
        repos=list(github_raw.get("repos", [])),
    )
    scoring = ScoringConfig(weights=dict(raw["scoring"]["weights"]))

    return Settings(app=app, api=api, storage=storage, github=github, scoring=scoring)


def _get_env(name: str) -> str | None:
    return os.environ.get(name)
