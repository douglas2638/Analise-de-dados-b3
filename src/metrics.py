import numpy as np
import pandas as pd


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret"] = out.groupby("ticker")["close"].pct_change()
    return out


def summarize_by_ticker(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["ret"]).copy()
    g = base.groupby("ticker")["ret"]

    summary = pd.DataFrame(
        {
            "dias": g.count(),
            "retorno_medio_dia": g.mean(),
            "vol_dia": g.std(),
            "retorno_acumulado": g.apply(lambda s: (1 + s).prod() - 1),
        }
    )

    # Max drawdown por ticker (informativo)
    mdd = {}
    for ticker, sub in base.groupby("ticker"):
        equity = (1 + sub["ret"]).cumprod()
        peak = equity.cummax()
        drawdown = (equity / peak) - 1
        mdd[ticker] = float(drawdown.min())
    summary["max_drawdown"] = pd.Series(mdd)

    # Score simples (opcional) - NÃO ordena por ele, só informa
    summary["score_ret_vol"] = summary["retorno_acumulado"] / summary["vol_dia"].replace(0, np.nan)

    # Ordena por retorno (principal)
    return summary.sort_values("retorno_acumulado", ascending=False)
