from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED = {"date", "ticker", "close"}


def load_prices(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    suf = p.suffix.lower()
    if suf == ".csv":
        df = pd.read_csv(p)
    elif suf in (".parquet", ".pq"):
        df = pd.read_parquet(p)
    else:
        raise ValueError("Formato não suportado. Use .csv ou .parquet")

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Dataset faltando colunas: {missing} (esperado: {REQUIRED})")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df = df.dropna(subset=["date", "ticker", "close"])
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)
