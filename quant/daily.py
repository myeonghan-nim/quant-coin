import ccxt
import pandas as pd
from dateutil.relativedelta import relativedelta


def cutoff_df(df: pd.DataFrame) -> pd.DataFrame:
    print("→ Cutoff Started.")
    if df["timestamp"].iloc[-1].hour != 15:
        df = df.iloc[:-1]
        print("→ Cutoff Finished.")
    else:
        print("→ Cutoff Skipped.")
    return df


def calculate_profit(df: pd.DataFrame) -> None:
    print("→ Calculate Profit Started.")
    init, now = 1000000, 1000000
    is_watching, all_time_high, all_time_low, bought_price, last_bought_date = False, None, None, None, None
    for _, row in df.iterrows():
        if all_time_high is None or (not is_watching and all_time_high is not None and all_time_high <= row["high"]):
            all_time_high = row["high"]
        elif all_time_high is not None and row["low"] <= all_time_high * 0.3:
            is_watching, all_time_low = True, row["low"]
        if bought_price is None and is_watching and all_time_low is not None and row["high"] >= all_time_low * 2:
            bought_price, last_bought_date = row["close"], row["timestamp"]
        elif bought_price is not None:
            month_diff = relativedelta(row["timestamp"], last_bought_date).years * 12 + relativedelta(row["timestamp"], last_bought_date).months
            if month_diff == 12 or bought_price * 1.5 <= row["close"] or bought_price * 0.8 >= row["close"]:
                bought_ratio = now / bought_price
                profit = row["close"] * bought_ratio - now
                now += profit
                is_watching, all_time_low, bought_price, last_bought_date = False, None, None, None
    print(f"→ Calculate Profit({now-init}) Finished.")


def at_this_is_the_time(df: pd.DataFrame) -> str:
    print("→ Calculate Timing Started.")
    is_watching, all_time_high, all_time_high_date, all_time_low, all_time_low_date = False, None, None, None, None
    bought_price, last_bought_date = None, None
    for _, row in df.iterrows():
        if all_time_high is None or (not is_watching and all_time_high is not None and all_time_high <= row["high"]):
            all_time_high, all_time_high_date = row["high"], row["timestamp"]
        elif all_time_high is not None and row["low"] <= all_time_high * 0.3:
            is_watching, all_time_low, all_time_low_date = True, row["low"], row["timestamp"]
        if bought_price is None and is_watching and all_time_low is not None and row["high"] >= all_time_low * 2:
            bought_price, last_bought_date = row["close"], row["timestamp"]
        elif bought_price is not None:
            month_diff = relativedelta(row["timestamp"], last_bought_date).years * 12 + relativedelta(row["timestamp"], last_bought_date).months
            if month_diff == 12 or bought_price * 1.5 <= row["close"] or bought_price * 0.8 >= row["close"]:
                is_watching, all_time_low, all_time_low_date, bought_price, last_bought_date = False, None, None, None, None
    print("→ Calculate Timing Finished.")
    print("→ Previous book:")
    print(f"→ Bought({bought_price}) at {last_bought_date}")
    print(f"→ All Time High({all_time_high}) at {all_time_high_date}")
    print(f"→ All Time Low({all_time_low}) at {all_time_low_date}")
    return "NOW" if bought_price is not None and last_bought_date is not None else "NOT NOW"


def main(include_eth: bool = False, calculate_profit_now: bool = False) -> None:
    symbols = ["BTC/KRW"]
    if include_eth:
        symbols.append("ETH/KRW")

    print(f'{"Processing Started.":=^96}')
    bithumb = ccxt.bithumb()
    for symbol in symbols:
        ohlcv = bithumb.fetch_ohlcv(symbol, "1d")
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = cutoff_df(df)
        if calculate_profit_now:
            calculate_profit(df)
        result = f"{symbol}: {at_this_is_the_time(df)}"
        print(f"{result:=^96}")


if __name__ == "__main__":
    main()
