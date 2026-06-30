# Strategy Findings: The Real Source of Losses Was Cost, Not Strategy

This document describes the single highest-impact finding of the project — and notably, it required **zero changes to the model or the trading logic**. It came purely from analyzing *realized money* against transaction costs.

## The Question

The system was net-negative. The intuitive hypotheses were "the model is wrong" or "the exits are bad." Before acting on intuition, I analyzed realized per-symbol P&L from thousands of real trades.

## The Analysis

For each instrument, I computed:
- Realized average R-multiple per trade (and its statistical significance)
- Spread cost as a fraction of the instrument's typical move (ATR)
- Total contribution to P&L

| Instrument | Realized R/trade | Spread as % of ATR | Verdict |
|-----------|------------------|--------------------|---------|
| Instrument A (crypto) | **−0.99 R** | ~12% | Toxic — 67% of all losses |
| Instrument B (FX) | −0.25 R (t ≈ −5.9) | ~21% | Statistically real loser |
| Instrument C (major FX) | −0.01 R | ~26% (worst ratio) | Break-even dilution |
| Instrument D (index) | **+0.07 R** (t ≈ +3.1) | ~10% | Genuine, significant edge |
| Instrument E (metal) | +0.04 R (t ≈ 0.04) | ~5% | Noise / diversifier only |

## The Insight

The losing instruments weren't losing because the *signals* were bad — they were losing because **transaction cost exceeded the per-trade edge**. One crypto instrument had a spread roughly **175× larger** (relative to its volatility) than a major FX pair, costing nearly a full stop-loss on every trade.

The fix was not in the model. It was **instrument selection**:

| Configuration | Total realized P&L |
|---------------|--------------------|
| All instruments | −$694 |
| Drop the toxic crypto | −$226 |
| Drop crypto + worst FX | **+$26 (break-even-positive)** |
| Concentrate on the two cost-efficient instruments | **+$72** |

## The Decision

The system was reconfigured to trade only the two most cost-efficient instruments — the one with a statistically significant positive edge (t ≈ +3.1, positive in 5 of 9 months) plus one diversifier. This was a **reversible configuration change**, validated against realized P&L, with full statistical scrutiny (including rejecting one instrument whose apparent profit was traced to a single lucky month).

## Why This Matters Methodologically

- The fix came from **realized money**, not model metrics or backtests — the highest-confidence kind of evidence.
- The mechanism is **physical and explainable**: spread cost vs. edge per trade.
- It was **reversible and low-risk**: a config change, not a code rewrite.
- It corrected a hypothesis (mine) that the model/exits were at fault.

## Lesson

> Before optimizing the sophisticated part of a system (the ML model), verify that the boring part (costs) isn't dominating. The most profitable change was the simplest one — and it was invisible to every model metric. Realized P&L analysis found what AUC never could.
