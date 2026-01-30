import pandas as pd
import yfinance as yf

def get_symbol_data(symbol, period="1mo"):
    data = yf.download(symbol, period=period)

    # Flatten MultiIndex columns cleanly
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Bring Date out as a column
    data.reset_index(inplace=True)

    return data

def download(ticker, period="1mo"):
    # read symbol from cli arguments
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "QQQ"

    # create data folder
    import os
    if not os.path.exists("data"):
        os.makedirs("data")

    # export data to csv including date stamp for the filename
    from datetime import datetime
    date_stamp = datetime.now().strftime("%Y%m%d")
    filename = f"data/{symbol}_data_{date_stamp}_{period}.csv"
    
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping download.")
        # load the data from the existing file
        import pandas as pd
        data = pd.read_csv(filename)
    else:
        # Get one year data
        data = get_symbol_data(symbol, period=period)
        data.to_csv(filename, index=False)
        print(f"Saved {len(data)} rows to {filename}")
    
    return data

# if __name__ == "__main__":
#     qqq_data = get_symbol_short_term_data("QQQ")
#     qqq_data.to_csv("qqq_data.csv", index=False)
#     print("Saved", len(qqq_data), "rows to qqq_data.csv")
