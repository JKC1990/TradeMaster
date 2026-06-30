# ML Findings: Detecting and Correcting Model Self-Deception

This document summarizes one of the most instructive investigations in the project: discovering that a high-performing model was succeeding for the wrong reasons, and correcting it.

## The Setup

The hybrid model (LSTM + XGBoost + meta-learner) reported a cross-validated AUC of **0.78** — which would be a strong edge for a financial classifier. Before trusting it with sizing decisions, I ran two diagnostics.

## Diagnostic 1: SHAP Feature Attribution

SHAP (SHapley Additive exPlanations) decomposes a prediction into the contribution of each feature. Running it on the live model revealed:

- Raw `close` price accounted for **25–39%** of feature importance across the specialist models.
- Several engineered features (RSI, ADX interactions) contributed near-zero.

A model leaning that heavily on *absolute price level* is a red flag: it suggests the model is **memorizing the price ranges seen in training** rather than learning patterns that generalize to unseen price levels.

## Diagnostic 2: Purged, Embargoed Walk-Forward

A standard cross-validation can leak information across time. A **purged walk-forward** trains on the past, embargoes a gap, then tests on the future — repeatedly rolling forward. Results:

| Feature set | Honest walk-forward AUC |
|-------------|-------------------------|
| **With** raw `close` | 0.78 |
| **Without** raw `close` | **~0.55** |

(0.50 = random.)

The model's apparent edge was **almost entirely price memorization**. The true, generalizable edge is ~0.55 — faint but real.

## Techniques Tested and Rejected

Crucially, several reasonable attempts to *improve* the edge were tested and found not to help against **real, realized outcomes**:

| Technique | Result | Verdict |
|-----------|--------|---------|
| Feature engineering (RSI×ADX, etc.) | +0.004–0.007 AUC | Noise — rejected |
| Per-strategy models | All 0.54–0.56 | No improvement |
| Triple-barrier labeling | 0.69 on its own label, **0.45 vs real P&L** | Optimizes a path not traded — rejected |
| Exit-rule tuning (trailing/TP variants) | Near-identical expectancy | Not the lever — rejected |

The triple-barrier result is the most instructive: a model can score *well on an idealized target* while being *worse than random at predicting actual profit*, because the idealized target (full take-profit before stop) is not how the live system actually exits.

## The Conclusion

The edge is genuinely thin (~0.55) and **not improvable through model complexity** — every ML lever landed at 0.54–0.57 against real outcomes. This is not a failure of the model; it is an honest measurement of how much separable signal exists in these instruments after costs.

This finding **redirected the entire optimization effort** away from the model and toward **cost structure and instrument selection** — see [`STRATEGY_FINDINGS.md`](STRATEGY_FINDINGS.md).

## The Fix (Staged)

The `close` feature was staged for removal from the next automated retrain. The resulting model reports the honest ~0.55 instead of the inflated 0.78. It is **not more profitable** — but it is honest, which makes downstream position-sizing decisions safer (no false confidence).

## Lesson

> A model that looks too good is a hypothesis to falsify, not a result to celebrate. Attribution (SHAP) plus leak-free validation (purged walk-forward) caught a self-deception that naive cross-validation completely missed.
