#!/usr/bin/env python3
import os
import yfinance as yf


def get_yahoo_closes(symbol="BTC-USD", days=365):
    # cache folder + file
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
        #save a file with the symbol_days name
        df[["Close"]].to_csv(cache_file)
    except Exception as e:
        print(f"Download failed: {e}")
        try:
            #try opening the file with the name symbol_days
            df = pd.read_csv(
                cache_file,
                index_col=0,
                parse_dates=True
            )

            print(f"Loaded cached data from {cache_file}")
        except:
            raise RuntimeError(
                f"Unable to download '{symbol}' and no cache file found."
            )

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    close_series = df["Close"]


    return [
        (idx.to_pydatetime(), float(close))
        for idx, close in close_series.items()
    ]

def floor_in_steps(number, step):
    return number//step*step

def get_steps_rounded_coordinates (input_data, step):
    normalised_data = [(element[0], floor_in_steps(element[1], step)) for element in input_data]
    return normalised_data

def get_kagi_coordinates (input_data):
    # data has item this structure
    # datetime.datetime(2021, 1, 8, 0, 0), 40797.609375
    consecutive = 0
    to_be_deleted_indexes = []
    direction = 1
    if len(input_data) < 2:
        return input_data
    
    for i in range (len(input_data)):
        if consecutive == 0:
            if input_data[0][1] > input_data[1][1]:
                direction = -1
            else:
                direction = 1
            consecutive = 1
        else:
            if i == len(input_data)-1:
                if  direction * input_data[i-1][1] <= direction * input_data[i][1]:
                    if consecutive >= 2:
                        to_be_deleted_indexes.append(i-1)
            elif  input_data[i-1][1] <= input_data[i][1] > input_data[i+1][1]:
                direction = -1
                consecutive += 1
                if consecutive > 2:
                        to_be_deleted_indexes.append(i-1)
                consecutive = 1
            elif  input_data[i-1][1] >= input_data[i][1] < input_data[i+1][1]:
                direction = 1
                consecutive += 1
                if consecutive > 2:
                        to_be_deleted_indexes.append(i-1)
                consecutive = 1
            elif input_data[i-1][1] == input_data[i][1] == input_data[i+1][1]:
                to_be_deleted_indexes.append(i-1)
                consecutive += 1
            else:
                consecutive += 1
                if consecutive > 2:
                    to_be_deleted_indexes.append(i-1)
    data_to_return = input_data[:]
    
    for i in range(len(to_be_deleted_indexes)-1, -1, -1):
        del data_to_return[to_be_deleted_indexes[i]]

    return data_to_return


def run_test(name, values):
    data = [(None, v) for v in values]

    result = get_kagi_coordinates(data)

    print(f"\n{name}")
    print("INPUT : ", values)
    print("OUTPUT: ", [v for _, v in result])

def run_all_tests():
    run_test(
        "Pure Uptrend",
        [40000, 41000, 42000, 43000, 44000]
    )

    run_test(
        "Pure Downtrend",
        [44000, 43000, 42000, 41000, 40000]
    )

    run_test(
        "Single Peak",
        [40000, 41000, 42000, 43000, 42000, 41000]
    )

    run_test(
        "Single Valley",
        [43000, 42000, 41000, 40000, 41000, 42000]
    )

    run_test(
        "Peak and Valley",
        [40000, 41000, 42000, 43000, 42000, 41000, 39000, 40000]
    )

    run_test(
        "Flat Section",
        [40000, 40000, 40000, 41000, 41000, 42000]
    )

    run_test(
        "Alternating",
        [40000, 41000, 40000, 41000, 40000, 41000]
    )

    run_test(
        "Plateau Peak",
        [1,2,3,3,3,2,1]
    )

    run_test(
        "Plateau Valley",
        [3,2,1,1,1,2,3]
    )

    run_test("Empty", [])

    run_test("Single Point", [100])

    run_test("Two Up", [100, 200])

    run_test("Two Down", [200, 100])

    run_test("Two Equal", [100, 100])

btc_data = get_yahoo_closes("BTC-USD", 2000)

normalised_data = get_steps_rounded_coordinates (btc_data, 1000)

run_all_tests()

print("First:", btc_data[0])
print("Last :", btc_data[-1])

print("First:", normalised_data[0])
print("Last :", normalised_data[-1])

closes = [price for _, price in btc_data]
print("Points:", len(closes))