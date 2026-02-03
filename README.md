# Análise de Dados de Ações da B3 (Blue Chips) com Python

[![CI](https://github.com/douglas2638/Analise-de-dados-b3/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/douglas2638/Analise-de-dados-b3/actions/workflows/ci.yml)

Projeto em Python para **análise automatizada de ações blue chips da B3**, com geração de
**rankings financeiros** e **relatório HTML** pronto para consumo.

---

## 📌 Visão geral

Este projeto consome dados históricos de ações da B3 (via `yfinance`), calcula métricas
financeiras relevantes e gera automaticamente um **relatório em HTML** com rankings
comparativos entre ativos.

O foco não é apenas análise, mas **engenharia de dados leve + qualidade de código + automação**.

---

## 🎯 Objetivo

Demonstrar habilidades práticas em:

- Análise de dados financeiros com Python
- Manipulação de séries temporais (`pandas`)
- Métricas financeiras:
  - Retorno acumulado
  - Volatilidade
  - Drawdown máximo
- Automação de relatórios (HTML)
- Boas práticas de engenharia:
  - Lint (Ruff)
  - Formatação (Black)
  - Tipagem (Mypy)
  - Testes (Pytest)
  - CI com GitHub Actions

---

## 🧰 Stack

- Python 3.11+
- pandas, numpy, matplotlib
- yfinance
- Jinja2 (templates HTML)
- Ruff, Black, Mypy
- Pytest
- GitHub Actions

---

## ▶️ Execução rápida

### 🪟 Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m src.main `
  --source yfinance `
  --start 2023-01-01 `
  --refresh `
  --use-adj


🌐 Visualizar relatório

Abra no navegador:

outputs/report.html

ou acesse o exemplo:
https://megapromostore.com.br/upload/1770139721970-report.html
