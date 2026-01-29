# Architecture Overview

## Components
- **Collectors**: fetch raw signals from external APIs on a schedule.
- **Normalizer**: maps source-specific payloads into a shared schema.
- **Scorer**: computes momentum scores using weighted rules.
- **Publisher**: writes outputs to storage or exports to downstream systems.

## Data flow
1. Scheduler triggers collectors.
2. Collectors store raw data in the database.
3. Normalizer processes raw data into canonical tables.
4. Scorer calculates per-company metrics and momentum scores.
5. Publisher exposes results for analytics or downstream consumption.
