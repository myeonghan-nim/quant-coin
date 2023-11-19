import pandas as pd
from dateutil.relativedelta import relativedelta
from pybithumb import Bithumb as bb


def cutoff_df(df: pd.DataFrame) -> pd.DataFrame:
    print("-> Cutoff Started.")
    time = df.tail(1).index.to_pydatetime()[0].hour
    if time != 00:
        df = df.iloc[:-1]
    print("-> Cutoff Finished.")
    return df


def calculate_profit(df: pd.DataFrame) -> None:
    print("-> Calculate Profit Started.")
    book, profit = {}, 0.0
    is_watching = False
    all_time_high, all_time_high_date, all_time_low, all_time_low_date = None, None, None, None
    bought_price, last_bought_date = None, None
    for index, row in df.iterrows():
        if all_time_high is None or (not is_watching and all_time_high is not None and all_time_high <= row["high"]):
            all_time_high, all_time_high_date = row["high"], index
        elif all_time_high is not None and row["low"] <= all_time_high * 0.3:
            is_watching = True
            all_time_low, all_time_low_date = row["low"], index
        if bought_price is None and is_watching and all_time_low is not None and row["high"] >= all_time_low * 2:
            bought_price, last_bought_date = row["close"], index
        elif bought_price is not None:
            month_diff = (
                relativedelta(index, last_bought_date).years * 12 + relativedelta(index, last_bought_date).months
            )
            if month_diff == 12 or bought_price * 1.5 <= row["close"] or bought_price * 0.8 >= row["close"]:
                book[str(len(book))] = {
                    "all_time_high": all_time_high,
                    "all_time_high_date": all_time_high_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "all_time_low": all_time_low,
                    "all_time_low_date": all_time_low_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "bought_price": bought_price,
                    "last_bought_date": last_bought_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "sell_price": row["close"],
                    "sell_date": index.strftime("%Y-%m-%d %H:%M:%S"),
                    "profit": (row["close"] - bought_price),
                }
                profit += row["close"] - bought_price
                is_watching = False
                all_time_low, all_time_low_date = None, None
                bought_price, last_bought_date = None, None
    print(f"-> Calculate Profit({profit}) Finished.")


def at_this_is_the_time(df: pd.DataFrame) -> str:
    print("-> Calculate Timing Started.")
    is_watching = False
    all_time_high, all_time_high_date, all_time_low, all_time_low_date = None, None, None, None
    bought_price, last_bought_date = None, None
    for index, row in df.iterrows():
        if all_time_high is None or (not is_watching and all_time_high is not None and all_time_high <= row["high"]):
            all_time_high, all_time_high_date = row["high"], index
        elif all_time_high is not None and row["low"] <= all_time_high * 0.3:
            is_watching = True
            all_time_low, all_time_low_date = row["low"], index
        if bought_price is None and is_watching and all_time_low is not None and row["high"] >= all_time_low * 2:
            bought_price, last_bought_date = row["close"], index
        elif bought_price is not None:
            month_diff = (
                relativedelta(index, last_bought_date).years * 12 + relativedelta(index, last_bought_date).months
            )
            if month_diff == 12 or bought_price * 1.5 <= row["close"] or bought_price * 0.8 >= row["close"]:
                is_watching = False
                all_time_low, all_time_low_date = None, None
                bought_price, last_bought_date = None, None
    print("-> Calculate Timing Finished.")
    print("-> Previous book:")
    print(f"-> Is Bought({bought_price}), Bought Date({last_bought_date})")
    print(f"-> All Time High({all_time_high}), All Time High Date({all_time_high_date})")
    print(f"-> All Time Low({all_time_low}), All Time Low Date({all_time_low_date})")
    return "NOW" if bought_price is not None and last_bought_date is not None else "NOT NOW"


def main(include_eth: bool = False, calculate_profit_now: bool = False) -> None:
    targets = ["BTC"]
    if include_eth:
        targets.append("ETH")

    print(f'{"Processing Started.":=^96}')
    tickers = bb.get_tickers()
    for ticker in tickers:
        if ticker in targets:
            df = cutoff_df(bb.get_candlestick(ticker))
            if calculate_profit_now:
                calculate_profit(df)
            result = f"{ticker}: {at_this_is_the_time(df)}"
            print(f"{result:=^96}")


if __name__ == "__main__":
    main()
