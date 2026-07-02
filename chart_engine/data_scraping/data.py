import os
import yfinance as yf
import pandas as pd


class YahooData:

    @staticmethod
    def get_yahoo_closes(symbol="BTC-USD", days=365):

        cache_dir = "cache_files"
        os.makedirs(cache_dir, exist_ok=True)

        cache_file = os.path.join(cache_dir, f"{symbol}_{days}.csv")

        try:
            df = yf.download(
                symbol,
                period=f"{days}d",
                interval="1d",
                progress=False,
                auto_adjust=False,
                group_by="column",
            )

            if df.empty:
                raise ValueError("Downloaded dataframe is empty")

            df[["Close"]].to_csv(cache_file)

        except Exception as e:

            print(f"Download failed: {e}")

            try:
                df = pd.read_csv(
                    cache_file,
                    index_col=0,
                    parse_dates=True
                )

                print(f"Loaded cached data from {cache_file}")

            except Exception:

                raise RuntimeError(
                    f"Unable to download '{symbol}' and no cache file found."
                )

        if df.empty:
            raise ValueError(f"No data returned for {symbol}")

        close_series = df["Close"]

        if isinstance(close_series, pd.DataFrame):
            close_series = close_series.iloc[:, 0]

        return [
            (idx.to_pydatetime(), float(close))
            for idx, close in close_series.items()
        ]