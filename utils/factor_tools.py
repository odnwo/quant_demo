# utils/factor_tools.py

import pandas as pd
import numpy as np

def compute_reversal_factor(df: pd.DataFrame, window: int = 5, price_col: str = "Close") -> pd.Series:
    """
    反转因子：过去N日收益率的负值（用于捕捉反弹）
    """
    return -df[price_col].pct_change(window)


def compute_volatility_factor(df: pd.DataFrame, window: int = 5, price_col: str = "Close") -> pd.Series:
    """
    波动率因子：过去N日收益率的标准差（衡量不稳定性）
    """
    return df[price_col].pct_change().rolling(window).std()


def generate_signal_by_quantile(
    df: pd.DataFrame,
    factor_col: str,
    n_quantiles: int = 5,
    long_quantile: int = 0,
    short_quantile: int = None,
    rolling_window: int = 60,
) -> pd.DataFrame:
    """
    对因子列进行 rolling 分位打分，生成交易信号列 Signal
    - long_quantile: 哪一档作为买入（越小越偏低因子值）
    - short_quantile: 哪一档作为卖出（越大越偏高因子值）
    """
    df = df.copy()

    def get_rank(x):
        try:
            labels = pd.qcut(x, n_quantiles, labels=False)
            return labels.iloc[-1]
        except:
            return np.nan

    df["Quantile"] = df[factor_col].rolling(rolling_window).apply(get_rank, raw=False)

    df["Signal"] = 0
    df.loc[df["Quantile"] == long_quantile, "Signal"] = 1
    if short_quantile is None:
        short_quantile = n_quantiles - 1
    df.loc[df["Quantile"] == short_quantile, "Signal"] = -1

    return df
