# Methodology: How Decisions Are Validated

The defining principle of this project is **intellectual honesty under uncertainty**. Trading systems are unusually prone to self-deception: backtests overfit, metrics mislead, and randomness masquerades as skill. This document describes the discipline used to separate real effects from illusions.

## Core Principles

### 1. Realized outcomes over backtests
Wherever possible, decisions are validated against **actual realized P&L from live trades**, not simulated or idealized results. A backtest answers "what would have happened under my assumptions"; realized P&L answers "what actually happened." The latter is trusted far more.

### 2. Leak-free validation
Time-series data is prone to lookahead leakage. All model validation uses **purged, embargoed walk-forward** splits — train on the past, skip a gap, test on the future — never naive k-fold cross-validation, which can leak future information into the past.

### 3. Statistical significance, not point estimates
A positive average is not evidence of edge. Every strategy claim is checked with **t-statistics and out-of-sample splits**. An effect that doesn't survive a time-based train/test split, or whose t-stat is near zero, is treated as noise — even if the headline number looks good.

### 4. Attribution to detect "right answer, wrong reason"
A good score from a bad mechanism is worse than a mediocre score from a sound one — it will fail unpredictably. **SHAP attribution** is used to verify the model is succeeding for generalizable reasons, not by memorizing artifacts.

### 5. Willingness to reject one's own ideas
Several techniques the author expected to work were tested and **rejected with evidence**:
- Triple-barrier labeling (optimized a target the system doesn't trade)
- Feature engineering (improvements were noise-level)
- Exit-rule tuning (no expectancy difference)
- Mean-reversion signals (real forward drift, but uncapturable after costs)

Documenting failed hypotheses is as valuable as documenting successes — it prevents revisiting dead ends and demonstrates honest reasoning.

### 6. Reversible, low-risk changes first
Changes are preferred in this order: configuration > validated code patch > model retrain > architectural change. The biggest win in the project (instrument selection) was a reversible config change. Risk to the live system is minimized at every step.

## The Validation Loop

```
   Hypothesis  ──▶  Test against realized data  ──▶  Significance check
       ▲                                                    │
       │                                                    ▼
   Reject or                                          Attribution /
   refine  ◀──────────  Honest verdict  ◀──────────  leak-free check
```

## Automated Validation

A **milestone system** runs this loop continuously and unattended: it counts live trades and, at thresholds (25, 50, 100, 150, 200), automatically runs SHAP / walk-forward / calibration analyses and emails the results. Model monitoring becomes a hands-off pipeline rather than a manual chore.

## The Honest Conclusion

This methodology led to an honest, perhaps humbling, conclusion: the edge in these instruments is thin (~0.55 AUC) and not improvable through model complexity. The realistic path to profitability is **cost reduction and disciplined instrument selection**, not more sophisticated ML. Acknowledging this — rather than chasing an illusory edge through ever-more-complex models — is itself a result.

> The goal is not to build the most impressive model. It is to know, with evidence, what is real.
