from momentum_signals.score import score_repo


def test_score_repo_positive():
    raw = {
        "repo": "example/repo",
        "stars": 100,
        "forks": 5,
        "commits_30d": 50,
        "issues_30d": 20,
        "contributors": 10,
        "release_recency_days": 5,
        "star_velocity": 30.0,
    }
    weights = {
        "commits_30d": 0.4,
        "star_velocity": 0.3,
        "issues_30d": 0.1,
        "contributors": 0.1,
        "release_recency": 0.1,
    }

    scored = score_repo(raw, weights)

    assert scored.repo == "example/repo"
    assert scored.momentum_score > 0
