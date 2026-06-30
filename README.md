# TradeMaster V3

> An autonomous, ML-driven algorithmic trading system with self-healing infrastructure, evidence-based strategy optimization, and a hedge-fund-grade real-time dashboard.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688.svg)](https://fastapi.tiangolo.com/)
[![ML](https://img.shields.io/badge/ML-LSTM%2BXGBoost-orange.svg)]()
[![Status](https://img.shields.io/badge/status-live-success.svg)]()

---

## Overview

TradeMaster V3 is a fully autonomous algorithmic trading system that I designed, built, and operate as a live system on a dedicated VPS. It connects to the MetaTrader 5 platform, generates trade signals from a hybrid machine-learning model, manages risk through a multi-phase control system, and reports performance through a custom real-time analytics dashboard.

The project is as much a **systems-engineering and applied-ML exercise** as it is a trading bot. Over its development I built features spanning data engineering, model training and validation, fault-tolerant orchestration, observability, and front-end visualization — and, critically, an **evidence-based methodology for deciding what actually works** versus what only looks good in backtests.

> **Note on philosophy:** This project is run with rigorous intellectual honesty. Every strategy change is validated against *realized* trade outcomes, not idealized backtests. Several promising ideas (triple-barrier labeling, feature engineering, exit-rule tuning) were tested and **rejected** with evidence. The biggest win came not from a fancy model but from disciplined *cost analysis* and *symbol selection*. This repository documents that process honestly.

---

## Key Features

### Machine Learning Pipeline
- **Hybrid model architecture**: LSTM (sequence patterns) + XGBoost (tabular features) + a meta-learner combining them.
- **Purged, embargoed walk-forward validation** to produce *honest* out-of-sample AUC estimates and avoid lookahead leakage.
- **SHAP-based feature attribution** to detect and eliminate price-level memorization (a key finding that corrected an inflated 0.78 → honest ~0.55 AUC).
- **Automated A/B model promotion** with live win-rate comparison and automatic rollback on degradation — new models must *prove themselves on real trades* before going live.

### Evidence-Based Strategy Optimization
- **Per-symbol realized P&L analysis** that identified one instrument responsible for 67% of losses (spread cost exceeding edge).
- **Cost-as-fraction-of-ATR analysis** to rank instruments by tradeability.
- **Statistical significance testing** (t-stats, out-of-sample splits) before any strategy change.

### Self-Healing Infrastructure
- Multi-phase orchestration (risk preflight, mode management, recovery, observability, security guard).
- **Automatic crash recovery**, state reconciliation, and corrupt-file detection.
- Watchdog process with stall detection and automatic restart.
- Drawdown circuit-breakers and profit-protection locks.

### Real-Time Analytics Dashboard
- Single-page application served by an embedded FastAPI server.
- Live equity curve, per-symbol/per-strategy performance, Monte Carlo simulation, time-of-day heatmaps, and risk metrics (Sharpe, Sortino, VaR, max drawdown).
- Fully responsive mobile view with a premium, tabular-numeric, fintech-terminal aesthetic.
- Automated daily email reporting.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      TradeMaster V3                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   MARKET DATA          SIGNAL ENGINE         EXECUTION       │
│   ┌──────────┐        ┌─────────────┐      ┌──────────┐      │
│   │   MT5    │───────▶│  Strategies │─────▶│  Risk    │      │
│   │  Feed    │        │  + ML Model │      │ Preflight│      │
│   └──────────┘        └─────────────┘      └────┬─────┘      │
│                              │                   │           │
│                              ▼                   ▼           │
│                       ┌─────────────┐      ┌──────────┐      │
│                       │ SHAP / Walk │      │   MT5    │      │
│                       │  -Forward   │      │  Orders  │      │
│                       └─────────────┘      └──────────┘      │
│                                                              │
│   ─────────────── SELF-HEALING ORCHESTRATION ───────────     │
│   Risk Mgr · Mode Mgr · Recovery · Observability · Watchdog  │
│                                                              │
│   ─────────────── OBSERVABILITY LAYER ──────────────────     │
│   FastAPI Dashboard · Milestone Analysis · Email Reports     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

See [`architecture/SYSTEM_DESIGN.md`](architecture/SYSTEM_DESIGN.md) for the detailed breakdown.

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| ML | XGBoost, TensorFlow/Keras (LSTM), scikit-learn, SHAP |
| Data | pandas, NumPy, PyArrow (Parquet) |
| Backend / API | FastAPI, embedded async server |
| Trading platform | MetaTrader 5 (via `MetaTrader5` Python package) |
| Frontend | Vanilla JS SPA, CSS design-token system, Canvas charts |
| Infra | Windows VPS, scheduled-task orchestration |

---

## Engineering Highlights

A few problems I found particularly interesting to solve:

1. **Detecting model self-deception.** The model reported a strong 0.78 AUC — but SHAP attribution revealed it was *memorizing raw price levels*, not learning generalizable patterns. A purged walk-forward without the price feature exposed the honest ~0.55 edge. This reframed the entire optimization effort. → [`docs/ML_FINDINGS.md`](docs/ML_FINDINGS.md)

2. **Finding the real source of losses.** Rather than assume the model or exits were at fault, I analyzed *realized* per-symbol P&L against spread costs. One instrument's transaction cost (≈175× another's relative to its volatility) was responsible for the majority of losses. Removing it via config — no model change — moved the system from losing toward break-even. → [`docs/STRATEGY_FINDINGS.md`](docs/STRATEGY_FINDINGS.md)

3. **Automated, unattended model analysis.** A milestone system counts live trades and, at thresholds, automatically runs SHAP / walk-forward / calibration analyses and emails the results — turning model monitoring into a hands-off pipeline. → [`src/examples/milestone_runner_example.py`](src/examples/milestone_runner_example.py)

4. **Honest validation discipline.** Multiple promising techniques were tested and *rejected* because they didn't predict real outcomes (e.g. triple-barrier labeling scored 0.69 on its own target but only 0.45 against actual realized P&L — optimizing a path the system doesn't trade).

---

## What This Project Demonstrates

- **Applied ML** end-to-end: feature engineering, model architecture, rigorous validation, attribution, and the judgment to know when a result is *real*.
- **Systems engineering**: fault tolerance, state management, observability, and orchestration of a long-running autonomous process.
- **Data engineering**: pipelines over market data, Parquet datasets, reconciliation.
- **Full-stack capability**: a production-quality real-time dashboard built from scratch.
- **Scientific rigor**: hypothesis → test → evidence → decision, including the discipline to reject one's own ideas.

---

## Repository Structure

```
trademaster-showcase/
├── README.md                      ← you are here
├── docs/
│   ├── ML_FINDINGS.md             ← the model-honesty investigation
│   ├── STRATEGY_FINDINGS.md       ← cost analysis & symbol selection
│   ├── DASHBOARD.md               ← the analytics dashboard
│   └── METHODOLOGY.md             ← how decisions are validated
├── architecture/
│   └── SYSTEM_DESIGN.md           ← components & data flow
└── src/examples/
    ├── walk_forward_validation.py ← purged walk-forward (illustrative)
    ├── shap_analysis_example.py   ← feature attribution (illustrative)
    └── milestone_runner_example.py← automated analysis pipeline (illustrative)
```

> **Note:** The code in `src/examples/` is **illustrative** — sanitized, self-contained excerpts that demonstrate the techniques and engineering approach. The full operational system (live credentials, broker configuration, server details) is private for security reasons.

---

## About

Built and operated by **Jobin** — a Technical Support Technician with a Computer Science background and a strong interest in applied ML, systems engineering, and the intersection of AI with operational/critical-infrastructure security.

This project has been my primary applied-learning vehicle for machine learning and production systems engineering.

---

*This repository is a portfolio showcase. It intentionally excludes all operational configuration, credentials, and infrastructure details.*
