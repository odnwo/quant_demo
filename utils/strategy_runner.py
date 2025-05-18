# utils/strategy_runner.py

import pandas as pd
from backtest import simple_backtest
from evaluate import evaluate_strategy

def run_strategy_pipeline(
    df: pd.DataFrame,
    position_col: str = "Position",
    fee: float = 0.001,
    benchmark: bool = True
) -> pd.DataFrame:
    """
    执行完整策略流程（传入仓位列），返回回测结果 DataFrame
    """

    df = df.copy()
    df["Signal"] = df[position_col]
    df["CleanSignal"] = df["Signal"]
    df["CleanSignal"] = df["CleanSignal"].mask(df["CleanSignal"] == df["CleanSignal"].shift(1))

    bt = simple_backtest(df, signal_col="CleanSignal", fee=fee)

    if benchmark:
        bt["Benchmark"] = (1 + bt["Return"]).cumprod()

    return bt
