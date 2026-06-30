"""
SHAP Feature Attribution (illustrative example)
===============================================

A sanitized illustration of how SHAP attribution is used in TradeMaster to
detect when a model is succeeding for the *wrong reason* (e.g. memorizing a
price level rather than learning a generalizable pattern).

In the live system, this analysis runs automatically at trade-count milestones
and emails a ranked feature-importance report. This file is for demonstration
only and uses synthetic data.
"""

import numpy as np

try:
    import xgboost as xgb
    import shap
    _HAS = True
except ImportError:
    _HAS = False


def attribute(model, X, feature_names):
    """
    Compute mean absolute SHAP value per feature -> a ranked importance list.

    A model that concentrates importance on an 'absolute level' feature (e.g.
    raw close price) is a red flag for memorization: it suggests the model keys
    off the price *range* seen in training rather than patterns that generalize
    to unseen price levels.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    importance = np.abs(shap_values).mean(axis=0)
    ranked = sorted(
        zip(feature_names, importance / importance.sum()),
        key=lambda t: t[1], reverse=True,
    )
    return ranked


def _demo():
    if not _HAS:
        print("Install xgboost + shap to run this demo.")
        return

    rng = np.random.default_rng(0)
    n = 1500
    feature_names = ["rsi", "adx", "ema_gap", "atr_ratio", "raw_price_level"]

    rsi = rng.normal(size=n)
    adx = rng.normal(size=n)
    ema_gap = rng.normal(size=n)
    atr_ratio = rng.normal(size=n)
    # The leaky feature: a monotonic level the model can memorize.
    raw_price_level = np.linspace(0, 100, n)

    # The TRUE label depends only on a faint combination of real features.
    y = ((0.3 * rsi + 0.2 * ema_gap + rng.normal(size=n)) > 0).astype(int)

    X = np.column_stack([rsi, adx, ema_gap, atr_ratio, raw_price_level])

    model = xgb.XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        eval_metric="logloss", verbosity=0,
    )
    model.fit(X, y)

    print("Feature importance (mean |SHAP|, normalized):\n")
    for name, imp in attribute(model, X, feature_names):
        bar = "#" * int(imp * 50)
        flag = "   <-- memorization red flag" if name == "raw_price_level" and imp > 0.15 else ""
        print(f"  {name:18s} {imp:5.1%}  {bar}{flag}")

    print("\nIf the raw-level feature dominates, the model is likely memorizing")
    print("price ranges, not learning a generalizable edge. The fix: drop it and")
    print("re-validate with a purged walk-forward (see walk_forward_validation.py).")


if __name__ == "__main__":
    _demo()
