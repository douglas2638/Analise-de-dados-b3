from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def save_outputs(summary: pd.DataFrame, df: pd.DataFrame, outdir: str = "outputs", top_n: int = 3):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    # CSV do ranking
    summary.to_csv(out / "ranking_bluechips.csv", index=True)

    # Gráfico equity (Top N)
    plt.figure()
    for t in summary.head(top_n).index:
        sub = df[df["ticker"] == t].dropna(subset=["ret"]).copy()
        equity = (1 + sub["ret"]).cumprod()
        plt.plot(sub["date"], equity, label=t)

    plt.title(f"Equity (Top {top_n} por Retorno)")
    plt.xlabel("Data")
    plt.ylabel("Equity (base 1.0)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "equity_top.png", dpi=150)
    plt.close()