from __future__ import annotations
import argparse
from pathlib import Path

from src.config import BLUECHIPS
from src.loader import load_prices
from src.metrics import add_returns, summarize_by_ticker
from src.report import save_outputs
from src.html_report import build_html

from src.yf_loader import YFDownloadConfig, download_prices_yfinance, save_dataset


def parse_args():
    p = argparse.ArgumentParser(description="Análise Blue Chips B3 (ranking por retorno) + relatório HTML")
    p.add_argument("--source", choices=["file", "yfinance"], default="yfinance",
                   help="Origem dos dados: yfinance ou arquivo local")
    p.add_argument("--input", default="data/raw/b3_bluechips.parquet",
                   help="Arquivo local (csv/parquet). Usado em source=file, ou como cache em yfinance.")
    p.add_argument("--start", default="2023-01-01", help="Data inicial YYYY-MM-DD (yfinance)")
    p.add_argument("--end", default=None, help="Data final YYYY-MM-DD (yfinance)")
    p.add_argument("--interval", default="1d", help="Intervalo yfinance: 1d,1wk,1mo")
    p.add_argument("--tickers", default=None,
                   help="Tickers separados por vírgula (ex: VALE3,PETR4). Se vazio, usa BLUECHIPS.")
    p.add_argument("--refresh", action="store_true",
                   help="Força novo download mesmo que o arquivo --input exista")
    p.add_argument("--outdir", default="outputs", help="Pasta de saída")
    p.add_argument("--top", type=int, default=3, help="Top N no gráfico")
    p.add_argument("--use-adj", action="store_true", help="Usar Adj Close (se disponível)")
    return p.parse_args()


def main():
    args = parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")] if args.tickers else BLUECHIPS
    dataset_path = Path(args.input)

    if args.source == "yfinance":
        if args.refresh or not dataset_path.exists():
            cfg = YFDownloadConfig(
                start=args.start,
                end=args.end,
                interval=args.interval,
                use_adj_close=bool(args.use_adj),
                suffix_sa=True,
            )
            df = download_prices_yfinance(tickers, cfg)
            save_dataset(df, str(dataset_path))
        df = load_prices(str(dataset_path))
    else:
        df = load_prices(str(dataset_path))

    # Análise
    df = df[df["ticker"].isin(tickers)].copy()
    df = add_returns(df)
    summary = summarize_by_ticker(df)

    # Saídas
    save_outputs(summary, df, outdir=args.outdir, top_n=args.top)
    build_html(summary, outdir=args.outdir, top_n=args.top)

    print("\nTop 10 (por retorno acumulado):\n")
    print(summary.head(10))
    print(f"\nRelatório: {Path(args.outdir) / 'report.html'}")


if __name__ == "__main__":
    main()