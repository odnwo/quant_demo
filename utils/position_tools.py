# utils/position_tools.py

import pandas as pd
import numpy as np

def generate_layered_position(
    df: pd.DataFrame,
    factor_col: str,
    n_layers: int = 5,
    position_levels: list = None,
    rolling_window: int = 60
) -> pd.Series:
    """
    根据因子分位值生成分层仓位信号：
    默认分5层，对应仓位 [-1.0, -0.5, 0.0, 0.5, 1.0]
    """
    if position_levels is None:
        position_levels = [-1.0, -0.5, 0.0, 0.5, 1.0]

    def get_layer(x):
        try:
            return pd.qcut(x, n_layers, labels=position_levels).iloc[-1]
        except:
            return np.nan

    return df[factor_col].rolling(rolling_window).apply(get_layer, raw=False)
