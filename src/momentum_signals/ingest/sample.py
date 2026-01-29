from __future__ import annotations

import json
from pathlib import Path


def load_sample_repos() -> list[dict]:
    data_path = Path(__file__).resolve().parent.parent / "data" / "sample_repos.json"
    return json.loads(data_path.read_text())
