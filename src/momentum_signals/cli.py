from __future__ import annotations

import argparse

import uvicorn

from .api import create_app
from .config import load_settings
from .pipeline import run_update


def main() -> None:
    parser = argparse.ArgumentParser(description="Momentum Signals CLI")
    parser.add_argument("--config", default="configs/app.yaml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("update", help="Run a single data update")
    subparsers.add_parser("serve", help="Start the API server")

    args = parser.parse_args()
    settings = load_settings(args.config)

    if args.command == "update":
        updated = run_update(settings)
        print("Updated signals:")
        for repo in updated:
            print(f"- {repo}")
    elif args.command == "serve":
        app = create_app(settings)
        uvicorn.run(app, host=settings.api.host, port=settings.api.port)


if __name__ == "__main__":
    main()
