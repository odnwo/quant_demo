# utils/evaluate.py

import numpy as np

def evaluate_strategy(df, return_col="StrategyReturn", equity_col="CumulativeReturn"):
    """
    评估策略表现：返回年化收益、波动率、夏普比率、最大回撤等指标
    参数：
        df: 含有策略收益的 DataFrame
        return_col: 策略日收益列名
        equity_col: 策略净值列名
    返回：
        一个 dict，包含评估结果
    """
    ret = df[return_col].dropna()
    equity = df[equity_col]

    annual_ret = ret.mean() * 252
    annual_vol = ret.std() * np.sqrt(252)
    sharpe = annual_ret / annual_vol if annual_vol != 0 else np.nan
    max_drawdown = (equity / equity.cummax() - 1).min()

    return {
        "年化收益": round(annual_ret, 4),
        "年化波动": round(annual_vol, 4),
        "夏普比率": round(sharpe, 4),
        "最大回撤": round(max_drawdown, 4),
    }
