# TradeMaster — Live Autonomous AI Trading Agent

> **A production-grade autonomous trading system built to learn ML deployment, agentic AI architecture, and evidence-based system investigation — not to beat the market.**

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![ML](https://img.shields.io/badge/ML-LSTM%20%2B%20XGBoost-orange)
![Status](https://img.shields.io/badge/Status-Live%20Production-brightgreen)

---

## What This Is

TradeMaster is a fully autonomous algorithmic trading agent I built and deployed to a live Windows VPS under the **JKC Capital** banner. It analyses market data, generates trade signals using a hybrid LSTM + XGBoost ML pipeline, executes trades autonomously via MetaTrader 5, and monitors its own performance through a real-time dashboard — without human intervention.

This project represents my transition from **Technical Support / IT Operations** into **AI engineering and autonomous systems** — with a specific focus on the architecture, reliability, and security challenges of production agentic AI.

---

## Why I Built It

I have 11 years of experience monitoring and maintaining critical operational systems (UAE toll infrastructure). I wanted to apply that operational mindset to AI — not just build a model in a notebook, but deploy one that runs 24/7, monitors itself, handles failures gracefully, and produces evidence-based results.

TradeMaster forced me to solve every problem that matters in production AI:
- How do you deploy an ML model so it stays running reliably?
- How do you monitor an autonomous agent's decisions in real time?
- How do you investigate whether your AI is actually adding value — or fooling itself?
- How do you harden an internet-exposed autonomous system?

---

## System Architecture

```
Market Data (MT5) → Feature Engineering → LSTM + XGBoost Scoring
       ↓
Phase-Based Risk Manager → Trade Decision Engine → MT5 Execution
       ↓
FastAPI Backend → React Dashboard (127.0.0.1:8787)
       ↓
Monitoring: P&L tracking, drawdown limits, performance analytics
Remote access via DuckDNS → Windows VPS
```

**Components:**
- **ML Pipeline:** Hybrid LSTM (sequence patterns) + XGBoost (feature importance) ensemble
- **Backend:** Python + FastAPI REST API
- **Dashboard:** Single-page React application with real-time updates
- **Risk Management:** Phase-based system (P1–P6) with automatic position sizing and drawdown controls
- **Deployment:** Windows VPS, 24/7 autonomous operation
- **Monitoring:** Nightly email reports, performance analytics, Monte Carlo simulation

---

## Technical Stack

| Layer | Technology |
|---|---|
| ML Models | LSTM (TensorFlow/Keras) + XGBoost |
| Backend | Python, FastAPI |
| Dashboard | React SPA |
| Database | SQLite (trade state), JSON (configuration) |
| Deployment | Windows VPS, DuckDNS remote access |
| Broker Integration | MetaTrader 5 Python API |
| Monitoring | Custom monitoring server, nightly HTML email reports |

---

## The Honest Investigation — What the Data Actually Showed

One of the most important phases of this project was a rigorous, evidence-based strategy investigation. Instead of assuming the system was working, I pulled historical MT5 data and analysed every symbol's real performance after spread costs.

**What I found:**

| Symbol | Net P&L After Spread | Decision |
|---|---|---|
| BTCUSDm | Deeply negative (67% of all losses) | ❌ Disabled |
| USDJPYm | Negative after spread costs | ❌ Disabled |
| EURUSDm | Negative after spread costs | ❌ Disabled |
| XAUUSDm | Positive realised expectancy | ✅ Active |
| USTECm | Positive realised expectancy | ✅ Active |

**ML model honest assessment:**
- Initial AUC: 0.78 (inflated by data leakage — `close` price as a feature)
- Honest AUC after leakage removal: ~0.55
- Conclusion: ML edge exists but is modest. The real fix was **symbol selection and spread management**, not ML complexity.

This investigation produced `STRATEGY_FINDINGS.md` — a written record of every finding and decision. I documented it because evidence-based decision making matters more than making the numbers look good.

---

## What This Project Demonstrates

**AI Engineering:**
- End-to-end ML pipeline from raw market data to autonomous execution
- Model training, validation, and honest evaluation (avoiding data leakage)
- Production deployment of an ML system (not a Jupyter notebook)

**Agentic AI Architecture:**
- Autonomous agent loop: perceive → reason → act → monitor → repeat
- Tool use (MT5 API), memory (trade state), autonomous decision-making
- This system architecture directly maps to the OWASP Agentic AI framework

**Production Operations:**
- 24/7 system reliability and monitoring
- Incident investigation and root cause analysis
- Real-time dashboards and alerting
- Evidence-based performance evaluation

**Security Considerations (ongoing work):**
- Internet-exposed autonomous agent with financial consequences
- Active threat modelling in progress (STRIDE framework)
- See: [TradeMaster Security Project] (link to threat model repo when published)

---

## Key Engineering Outcomes

- Built and deployed a complete ML pipeline to a live production environment
- Identified and eliminated a data leakage bug that inflated AUC from 0.55 to 0.78
- Disabled 3 of 5 trading symbols based on evidence — not assumption
- Built a comprehensive React dashboard with real-time P&L, drawdown monitoring, and Monte Carlo simulation
- Implemented phase-based risk management to protect capital automatically
- Fixed multiple production bugs including a trading halt caused by a stuck profit-lock flag

---

## Project Status

- ✅ Live on VPS — autonomous operation
- ✅ Two active symbols (XAUUSDm, USTECm) with positive expectancy
- ✅ Dashboard with full performance analytics
- 🔄 Security hardening in progress (STRIDE threat model — see Project 2)
- 🔄 ML pipeline improvement (removing raw `close` feature at next retrain)

---

## About the Builder

**Jobin Kurian Chandy** — Technical Support Technician → transitioning into AI Security
- 11 years IT + OT operational experience (UAE toll infrastructure)
- Building toward: AI/Agentic Security | Security+ | SC-200 | SC-500 | CAISP
- LinkedIn: [linkedin.com/in/jobinkurianchandy](https://linkedin.com/in/jobinkurianchandy)

*TradeMaster is my proof that I can build, deploy, operate, and honestly evaluate a production autonomous AI system — the foundation for my next focus: securing systems like this one.*

---

## Repository Structure

```
TradeMaster/
├── README.md (this file)
├── STRATEGY_FINDINGS.md (evidence-based investigation results)
├── architecture/ (system diagrams)
├── dashboard/ (React SPA)
├── backend/ (FastAPI + monitoring server)
├── ml/ (LSTM + XGBoost pipeline)
└── docs/ (performance reports)
```

---

*Code available on request. Some components omitted from public repository for security reasons — consistent with responsible disclosure practices for live financial systems.*
