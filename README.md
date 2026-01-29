# Momentum Signals

Momentum Signals is a self-updating platform that tracks and monetizes **open-source repo momentum** before it becomes obvious. Users pay for **early visibility**, not explanations.

## Product scope
- **Signal pack**: Open-source repo momentum (stars, commits, issues, contributors, release cadence)
- **Core value**: Early visibility into rising repositories and ecosystems
- **Monetization**: API-key gated access to signal snapshots

## Architecture
```
Ingest (GitHub API or sample data)
        ↓
Normalize + Score (momentum model)
        ↓
Persist (SQLite)
        ↓
API (FastAPI, API-key gated)
```

## Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run a one-time update:
   ```bash
   python -m momentum_signals.cli update --config configs/app.yaml
   ```
3. Start the API:
   ```bash
   python -m momentum_signals.cli serve --config configs/app.yaml
   ```
4. Fetch signals (replace `YOUR_API_KEY`):
   ```bash
   curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/signals
   ```

## Configuration
See `configs/app.yaml` for defaults. You can override values with environment variables:
- `MOMENTUM_DB_PATH`
- `MOMENTUM_GITHUB_TOKEN`
- `MOMENTUM_API_KEY`

## Signal model
Each repo is scored with a **momentum score** derived from:
- 30-day commit volume
- Star growth velocity
- Issue activity
- Contributor count
- Release cadence

Higher scores indicate a repo is accelerating faster than its peers.

## Notes
- The GitHub API is optional; the pipeline works with sample data out of the box.
- This is a starter platform with extensible scoring and ingestion layers.
