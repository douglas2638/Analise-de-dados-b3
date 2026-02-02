
import pandas as pd
from src.metrics import add_returns, summarize_by_ticker

def test_order_by_return():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01","2024-01-02","2024-01-01","2024-01-02"]),
        "ticker": ["A","A","B","B"],
        "close": [10,11,10,12]
    })
    df = add_returns(df)
    s = summarize_by_ticker(df)
    assert s.index[0] == "B"
