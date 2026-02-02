
# Análise de Dados de Ações da B3 (Blue Chips) com Python

![CI](https://github.com/douglas2638/analise-dados-b3-python/actions/workflows/ci.yml/badge.svg)

Projeto em Python focado em **análise de dados financeiros**, utilizando ações **blue chips da B3**
para gerar rankings por retorno e um **relatório automático em HTML**.

## Objetivo
Demonstrar habilidades práticas em:
- Python para dados
- pandas e séries temporais
- Métricas financeiras (retorno, volatilidade, drawdown)
- Automação de relatórios
- Qualidade de código (lint, testes, CI)

## Stack
Python, pandas, numpy, matplotlib, Jinja2, Ruff, Black, Pytest, Mypy, GitHub Actions.

## ▶️ Execução rápida

### 🪟 Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.main --source yfinance --start 2023-01-01 --refresh --use-adj

## ▶️ Abra no navegador

outputs\report.html
