# utils/strategy_runner.py

import pandas as pd
from utils.backtest import simple_backtest
from utils.evaluate import evaluate_strategy
import os

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



def save_strategy_result(
    df_bt: pd.DataFrame,
    metrics: dict,
    output_dir: str = "./results",
    strategy_name: str = "strategy"
):
    """
    保存策略净值曲线和评估指标
    """
    os.makedirs(output_dir, exist_ok=True)

    # 保存净值曲线
    equity_path = os.path.join(output_dir, f"{strategy_name}_equity.csv")
    df_bt.to_csv(equity_path, index=True)

    # 保存评估指标
    metrics_path = os.path.join(output_dir, f"{strategy_name}_metrics.csv")
    pd.DataFrame([metrics]).to_csv(metrics_path, index=False)

    print(f"[Saved] {equity_path}")
    print(f"[Saved] {metrics_path}")
