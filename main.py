# main.py

import pandas as pd
import yfinance as yf
from utils.factor_tools import compute_reversal_factor, compute_volatility_factor
from utils.position_tools import generate_layered_position
from utils.strategy_runner import run_strategy_pipeline, evaluate_strategy, save_strategy_result


def run_reversal_volatility_strategy(symbol="TQQQ", output_dir="./results", strategy_name="reversal_vol"):
    # Step 1: load data
    df = yf.download(symbol, start="2022-01-01", end="2023-12-31")
    df = df[["Close"]].copy()

    # Step 2: compute factors
    df["Reversal"] = compute_reversal_factor(df, window=5)
    df["Volatility"] = compute_volatility_factor(df, window=5)

    # Step 3: combine factor and assign position
    df["CombinedFactor"] = df["Reversal"] - df["Volatility"]
    df["Position"] = generate_layered_position(df, factor_col="CombinedFactor", n_layers=5)

    # Step 4: run backtest
    df_bt = run_strategy_pipeline(df, position_col="Position", fee=0.001)

    # Step 5: evaluate & save
    metrics = evaluate_strategy(df_bt)
    save_strategy_result(df_bt, metrics, output_dir=output_dir, strategy_name=strategy_name)


if __name__ == "__main__":
    run_reversal_volatility_strategy()
