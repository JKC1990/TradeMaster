# System Design

TradeMaster V3 is structured as a long-running, fault-tolerant orchestration of specialized components. This document describes the major subsystems and how data flows between them.

## Design Goals

1. **Autonomy** — run unattended for extended periods, recovering from faults without intervention.
2. **Safety** — never let a bug or crash put capital at uncontrolled risk; fail closed.
3. **Observability** — every decision and state transition is logged and surfaced.
4. **Honesty** — measure and report true performance, never an optimistic illusion.

## Major Subsystems

### Signal Generation
- **Strategies**: trend-pullback, breakout, and mean-reversion modules, each producing candidate signals with regime awareness (trend vs. range) and multi-timeframe confirmation.
- **ML Scorer**: the hybrid LSTM + XGBoost + meta model scores each candidate; only sufficiently confident signals proceed.

### Risk & Execution
- **Risk Preflight**: validates every intended trade against exposure, margin, and drawdown limits before submission.
- **Mode Manager (Phase 6)**: adjusts position sizing and can pause trading based on drawdown bands and profit-protection state — a daily-loss circuit breaker.
- **Execution**: submits orders to MetaTrader 5 and records the full intent → fill → outcome chain.

### Self-Healing Orchestration
A sequence of phases, each responsible for a slice of reliability:
- **Recovery**: detects and recovers orphaned positions and corrupt state files on startup.
- **Reconciliation**: continuously cross-checks internal state against the broker's ground truth, reporting a confidence score.
- **Observability**: structured logging, metrics, and health scoring.
- **Security Guard**: guards against unsafe states.
- **Watchdog**: an independent process that detects stalls (via a heartbeat file) and restarts the engine if it hangs.

### Analysis & Reporting
- **Milestone System**: counts live trades and triggers automated SHAP / walk-forward / calibration analyses at thresholds, emailing results.
- **Dashboard**: an embedded FastAPI server exposing a real-time SPA (see [`../docs/DASHBOARD.md`](../docs/DASHBOARD.md)).
- **Email Reports**: consolidated daily performance summaries.

## Data Flow

```
  MT5 market data
        │
        ▼
  Strategy modules ──▶ candidate signals
        │
        ▼
  ML scorer ──▶ confidence-filtered signals
        │
        ▼
  Risk preflight ──▶ Mode manager (sizing / pause)
        │
        ▼
  Execution ──▶ MT5 orders ──▶ fills
        │
        ▼
  Outcome logging (intent → fill → result)
        │
        ├──▶ Reconciliation (vs broker truth)
        ├──▶ Milestone analysis (SHAP / walk-forward)
        ├──▶ Dashboard (real-time)
        └──▶ Email reports (daily)
```

## State Management

- **Persistent key-value store** for position metadata and runtime flags.
- **Parquet datasets** for the ML training corpus.
- **JSONL event logs** for the signal → outcome audit trail (with rotation).
- Startup reconciliation rebuilds derived indices and repairs inconsistencies.

## Fault Tolerance Patterns

- **Heartbeat + watchdog**: independent stall detection and restart.
- **Backup-first state writes**: corrupt files are detected and restored from backup.
- **Fail-closed risk**: when in doubt, trading is paused rather than continued.
- **A/B + rollback for models**: new models are validated on live trades before promotion and auto-reverted on degradation.

## Technology Choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Sequence modeling | LSTM (Keras) | captures temporal patterns in price/indicator sequences |
| Tabular modeling | XGBoost | strong on engineered features, fast, interpretable via SHAP |
| Validation | Purged walk-forward | leak-free, honest out-of-sample estimates |
| Serving | Embedded FastAPI | zero extra infrastructure, async, ships with the engine |
| Data format | Parquet + JSONL | columnar for ML, append-only logs for audit |
| Orchestration | Scheduled tasks + watchdog | simple, robust, OS-native fault recovery |
