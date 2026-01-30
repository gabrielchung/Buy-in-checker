import pandas as pd
import yfinance as yf

def get_ticker_data(ticker, period="1mo"):
    data = yf.download(ticker, period=period)

    # Flatten MultiIndex columns cleanly
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Bring Date out as a column
    data.reset_index(inplace=True)

    return data

def download(ticker, period="1mo"):
    # create data folder
    import os
    if not os.path.exists("data"):
        os.makedirs("data")

    # export data to csv including date stamp for the filename
    from datetime import datetime
    date_stamp = datetime.now().strftime("%Y%m%d")
    filename = f"data/{ticker}_data_{date_stamp}_{period}.csv"
    
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping download.")
        # load the data from the existing file
        import pandas as pd
        data = pd.read_csv(filename)
    else:
        # Get one year data
        data = get_ticker_data(ticker, period=period)
        data.to_csv(filename, index=False)
        print(f"Saved {len(data)} rows to {filename}")
    
    return data