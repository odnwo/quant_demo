# utils/backtest.py

import pandas as pd


'''
def simple_backtest(df, signal_col="Signal", price_col="Close"):
    """
    简单回测逻辑：用昨日信号持有当天，返回累计收益曲线。
    """
    df = df.copy()
    df["Position"] = df[signal_col].shift(1).ffill().fillna(0)
    df["Return"] = df[price_col].pct_change()
    df["StrategyReturn"] = df["Position"] * df["Return"]
    df["CumulativeReturn"] = (1 + df["StrategyReturn"]).cumprod()
    return df
'''

def simple_backtest(df, signal_col="Signal", price_col="Close", fee=0.001):
    df = df.copy()
    df["Position"] = df[signal_col].shift(1).ffill().fillna(0)
    df["Trade"] = df["Position"].diff().abs()  # 换手标记
    df["Return"] = df[price_col].pct_change()
    df["StrategyReturn"] = df["Position"] * df["Return"] - df["Trade"] * fee
    df["CumulativeReturn"] = (1 + df["StrategyReturn"]).cumprod()
    return df
