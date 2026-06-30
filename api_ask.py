#!/usr/bin/env python3

import yfinance as yf


def get_yahoo_closes(symbol="BTC-USD", days=365):
    df = yf.download(
        symbol,
        period=f"{days}d",
        interval="1d",
        progress=False,
        auto_adjust=False,
        group_by="column",
    )

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    close_series = df["Close"]

    # Handle MultiIndex output from newer yfinance versions
    if hasattr(close_series, "columns"):
        close_series = close_series.iloc[:, 0]

    return [
        (idx.to_pydatetime(), float(close))
        for idx, close in close_series.items()
    ]


btc_data = get_yahoo_closes("BTC-USD", 2000)

print("First:", btc_data[0])
print("Last :", btc_data[-1])

closes = [price for _, price in btc_data]
print("Points:", len(closes))