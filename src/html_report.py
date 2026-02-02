from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

import pandas as pd


def _pct(x) -> str:
    try:
        return f"{x * 100:.2f}%"
    except Exception:
        return "—"


def _num(x) -> str:
    try:
        return f"{x:.4f}"
    except Exception:
        return "—"


def _read_png_b64(path: str) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode("utf-8")


def build_html(summary: pd.DataFrame, outdir: str = "outputs", top_n: int = 3):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    # KPIs
    top1 = summary.iloc[0] if not summary.empty else None
    kpi_tickers = int(summary.shape[0])
    kpi_best = _pct(top1["retorno_acumulado"]) if top1 is not None else "—"
    kpi_avg_days = f"{summary['dias'].mean():.0f}" if "dias" in summary else "—"

    # Tabela formatada (Top 10)
    top10 = summary.head(10).copy()
    table = top10.reset_index().rename(columns={"index": "ticker"})
    table["retorno_acumulado"] = table["retorno_acumulado"].map(_pct)
    table["retorno_medio_dia"] = table["retorno_medio_dia"].map(_pct)
    table["vol_dia"] = table["vol_dia"].map(_pct)
    table["max_drawdown"] = table["max_drawdown"].map(_pct)
    table["score_ret_vol"] = table["score_ret_vol"].map(_num)

    table_html = table.to_html(index=False, escape=False)

    # Embedding do gráfico
    png_b64 = _read_png_b64(str(out / "equity_top.png"))
    img_tag = (
        f'<img alt="Equity Top" src="data:image/png;base64,{png_b64}" />'
        if png_b64
        else "<p>(gráfico não encontrado)</p>"
    )

    html = f"""
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Relatório - Blue Chips B3 (Ranking por Retorno)</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #111; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; }}
    h1 {{ margin: 0 0 8px 0; }}
    .sub {{ color: #555; margin-bottom: 16px; }}
    .cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 12px 0 18px; }}
    .card {{ background: #fafafa; border: 1px solid #eee; border-radius: 12px; padding: 12px; }}
    .k {{ font-size: 12px; color: #444; margin-bottom: 6px; }}
    .v {{ font-size: 20px; font-weight: 700; }}
    img {{ max-width: 100%; border-radius: 12px; border: 1px solid #eee; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 10px 8px; text-align: left; }}
    th {{ background: #f7f7f7; }}
    .footer {{ margin-top: 18px; font-size: 12px; color: #666; }}
    code {{ background:#f2f2f2; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Relatório — Blue Chips B3 (Ranking por Retorno)</h1>
    <div class="sub">
      Ranking baseado em <b>retorno acumulado</b>. Métricas de risco (volatilidade e drawdown) são exibidas para contexto.
    </div>

    <div class="cards">
      <div class="card"><div class="k">Tickers avaliados</div><div class="v">{kpi_tickers}</div></div>
      <div class="card"><div class="k">Dias médios por ticker</div><div class="v">{kpi_avg_days}</div></div>
      <div class="card"><div class="k">Melhor retorno (Top 1)</div><div class="v">{kpi_best}</div></div>
    </div>

    <h2>Equity (Top {top_n})</h2>
    {img_tag}

    <h2>Top 10 por retorno acumulado</h2>
    {table_html}

    <div class="footer">
      Gerado em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
      Dica: você pode substituir o dataset em <code>data/sample</code> por dados reais e reexecutar.
    </div>
  </div>
</body>
</html>
""".strip()

    (out / "report.html").write_text(html, encoding="utf-8")
