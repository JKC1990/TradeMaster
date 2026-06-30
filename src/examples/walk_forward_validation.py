"""
Purged, Embargoed Walk-Forward Validation (illustrative example)
================================================================

This is a sanitized, self-contained illustration of the leak-free validation
approach used in TradeMaster. It demonstrates *why* a purged walk-forward gives
an honest out-of-sample estimate where naive cross-validation can leak.

This file is for demonstration only — it uses synthetic data and is not the
operational implementation.
"""

import numpy as np
from sklearn.metrics import roc_auc_score

try:
    import xgboost as xgb
    _HAS_XGB = True
except ImportError:
    _HAS_XGB = False


def purged_walk_forward_auc(X, y, n_folds=5, embargo=20):
    """
    Train on the past, embargo a gap, test on the future — rolling forward.

    The embargo gap between train and test prevents information from adjacent
    (and possibly autocorrelated) samples leaking across the boundary, which a
    naive k-fold split would allow.

    Parameters
    ----------
    X : (n, d) feature matrix, ordered in time (oldest first)
    y : (n,)   binary labels (1 = winning trade, 0 = losing)
    n_folds : number of expanding-window folds
    embargo : number of samples to skip between train and test

    Returns
    -------
    mean AUC across folds (0.5 = random)
    """
    n = len(X)
    fold = n // (n_folds + 1)
    aucs = []

    for k in range(1, n_folds + 1):
        train_end = fold * k
        test_start = train_end + embargo          # <-- the embargo gap
        test_end = min(test_start + fold, n)

        if test_start >= n or test_end - test_start < 20:
            break
        if len(set(y[:train_end])) < 2 or len(set(y[test_start:test_end])) < 2:
            continue

        if _HAS_XGB:
            model = xgb.XGBClassifier(
                n_estimators=200, max_depth=4, learning_rate=0.05,
                subsample=0.8, eval_metric="logloss", verbosity=0,
            )
            model.fit(X[:train_end], y[:train_end])
            proba = model.predict_proba(X[test_start:test_end])[:, 1]
        else:
            # fallback: a trivial linear scorer so the example runs anywhere
            w = np.linalg.lstsq(X[:train_end], y[:train_end], rcond=None)[0]
            proba = X[test_start:test_end] @ w

        aucs.append(roc_auc_score(y[test_start:test_end], proba))

    return float(np.mean(aucs)) if aucs else float("nan")


def _demo():
    """
    Demonstrates the key lesson: a feature that *memorizes* a level (here, a
    slowly-drifting index that encodes position in the series) can inflate a
    naive score but should be caught by honest validation.
    """
    rng = np.random.default_rng(0)
    n = 2000

    # A faint real signal + lots of noise.
    real_signal = rng.normal(size=n) * 0.3
    y = (real_signal + rng.normal(size=n) > 0).astype(int)

    # Feature set WITHOUT the leaky "level" feature.
    X_honest = np.column_stack([
        real_signal + rng.normal(size=n),
        rng.normal(size=n),
        rng.normal(size=n),
    ])

    # Same, but ADD a monotonic "price level" proxy the model can memorize.
    level = np.linspace(0, 10, n).reshape(-1, 1)
    X_leaky = np.column_stack([X_honest, level])

    print("Honest features  -> walk-forward AUC:",
          round(purged_walk_forward_auc(X_honest, y), 3))
    print("With level proxy -> walk-forward AUC:",
          round(purged_walk_forward_auc(X_leaky, y), 3))
    print("\nThe inflated score from the 'level' feature is the same class of")
    print("self-deception SHAP attribution caught in the live model.")


if __name__ == "__main__":
    _demo()
