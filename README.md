# AI Startup Open Source Momentum Signals

## Product scope
AI Startup Open Source Momentum Signals is a lightweight pipeline that tracks early indicators of momentum for AI startups by aggregating open data, enriching it, and producing a ranked signal feed for analysts, founders, and investors.

## Chosen signal pack
**Signal pack: AI Startup Momentum**

The initial signal pack focuses on a small set of leading indicators that can be derived from open data sources and updated on a regular cadence:
- **Product velocity**: recent GitHub activity (commits, stars, contributors).
- **Market attention**: Hacker News and Reddit mentions.
- **Hiring momentum**: job postings growth from public boards.
- **Community engagement**: newsletter subscriptions or social follower deltas where available.

## Data sources
- GitHub public APIs (repos, stars, contributors)
- Hacker News public API
- Reddit public API
- Public job boards (e.g., Greenhouse, Lever)
- Optional: company website RSS feeds or changelog pages

## High-level architecture
1. **Ingestion**: scheduled collectors pull raw signals from the sources above.
2. **Normalization**: data is normalized into a common schema and stored in a database.
3. **Scoring**: a rules-based scorer computes a momentum score per company.
4. **Publishing**: scored signals are written to a table or exported to downstream consumers.

## How to run
1. Copy the sample configuration and fill in real values:
   ```bash
   cp configs/app.yaml configs/local.yaml
   ```
2. Set any required environment variables (see the config file for placeholders).
3. Run the pipeline (placeholder):
   ```bash
   ./bin/run
   ```

## Repository layout
- `src/`: application source code
- `configs/`: configuration files
- `docs/`: architecture and operational notes
