from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd
import yfinance as yf


@dataclass
class YFDownloadConfig:
    start: str = "2023-01-01"
    end: str = None  # se None, yfinance usa "até hoje"
    interval: str = "1d"  # "1d", "1wk", "1mo"
    use_adj_close: bool = True  # usa Adj Close se existir
    suffix_sa: bool = True  # adiciona ".SA" automaticamente


def normalize_tickers(tickers: Iterable[str], suffix_sa: bool = True) -> List[str]:
    out = []
    for t in tickers:
        t = t.strip().upper()
        if not t:
            continue
        if suffix_sa and not t.endswith(".SA"):
            t = f"{t}.SA"
        out.append(t)
    return out


def download_prices_yfinance(
    tickers: list[str],
    cfg: YFDownloadConfig,
) -> pd.DataFrame:
    yf_tickers = normalize_tickers(tickers, suffix_sa=cfg.suffix_sa)

    df = yf.download(
        tickers=yf_tickers,
        start=cfg.start,
        end=cfg.end,
        interval=cfg.interval,
        auto_adjust=False,
        group_by="column",
        threads=True,
        progress=False,
    )

    if df is None or df.empty:
        raise RuntimeError("Nenhum dado retornado pelo yfinance. Verifique tickers/período.")

    # yfinance retorna colunas MultiIndex quando há vários tickers:
    # Ex: df["Adj Close"] com colunas por ticker
    price_col = "Adj Close" if cfg.use_adj_close and "Adj Close" in df.columns else "Close"

    if isinstance(df.columns, pd.MultiIndex):
        prices = df[price_col].copy()
        prices = prices.reset_index().melt(id_vars=["Date"], var_name="ticker", value_name="close")
    else:
        # caso um ticker só, pode vir "Close" simples
        prices = df[[price_col]].copy()
        prices = prices.reset_index()
        prices.columns = ["date", "close"]
        # nesse caso, ticker não vem - pega do único ticker
        prices["ticker"] = yf_tickers[0]

    prices = prices.rename(columns={"Date": "date"})
    prices["date"] = pd.to_datetime(prices["date"])
    prices["close"] = pd.to_numeric(prices["close"], errors="coerce")
    prices = prices.dropna(subset=["close"])

    # Remover ".SA" pra manter tickers "limpos" no relatório
    prices["ticker"] = prices["ticker"].astype(str).str.replace(".SA", "", regex=False)

    prices = prices.sort_values(["ticker", "date"]).reset_index(drop=True)
    return prices


def save_dataset(df: pd.DataFrame, out_path: str) -> None:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() in (".parquet", ".pq"):
        df.to_parquet(p, index=False)
    elif p.suffix.lower() == ".csv":
        df.to_csv(p, index=False)
    else:
        raise ValueError("Formato de saída não suportado. Use .csv ou .parquet")


def stamp_metadata(outdir: str, meta: dict) -> None:
    Path(outdir).mkdir(parents=True, exist_ok=True)
    meta2 = dict(meta)
    meta2["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (Path(outdir) / "dataset_meta.json").write_text(
        pd.Series(meta2).to_json(force_ascii=False, indent=2),
        encoding="utf-8",
    )