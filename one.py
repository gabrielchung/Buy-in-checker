import api.data_api as data_api
import api.analysis_api as analysis_api
import api.ui_api as ui_api
import math
import sys

MIN_GROWTH_RATE = 1e-6  # 0.0001% per day

def _is_nan(value):
    try:
        return value is None or math.isnan(float(value))
    except Exception:
        return False

def _validate_df(df, name, required_columns):
    if df is None:
        print(f"Error: {name} is None.")
        return False
    if getattr(df, "empty", False) or len(df) == 0:
        print(f"Error: {name} is empty.")
        return False
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"Error: {name} is missing required columns: {', '.join(missing)}")
        return False
    close = df["Close"]
    if getattr(close, "empty", False) or len(close) == 0:
        print(f"Error: {name} has an empty Close column.")
        return False
    if _is_nan(close.iloc[0]) or _is_nan(close.iloc[-1]):
        print(f"Error: {name} has NaN Close at start or end.")
        return False
    return True

def _safe_days_to_target(current, target, rate):
    if current >= target:
        return 0
    if rate is None or rate <= MIN_GROWTH_RATE:
        return None
    return analysis_api.calculate_days_to_reach_target(current, target, rate)

def _safe_rate(rate):
    return None if _is_nan(rate) else rate

def _rate_to_percent(rate):
    return None if rate is None else round(rate * 100, 2)

def _fmt_percent(p):
    return "N/A" if p is None else f"{p:.2f}%"

def _fmt_days(d):
    return "N/A" if d is None else f"{d} days"


if __name__ == "__main__":
    print("Buy-In Checker")
    print("we are using one month high-low data to analyze the buy-in point.")
    print()

    # Get ticker from command line
    ticker = ui_api.parse_ticker(sys.argv)

    print(f"Ticker: {ticker}")
    print("Periods: 1mo / 3mo / 1y")
    print()

    # Download data
    data_monthly = data_api.download(ticker)
    data_three_monthly = data_api.download(ticker, period="3mo")
    data_yearly = data_api.download(ticker, period="1y")
    
    if not _validate_df(data_monthly, "Monthly data", ["Close", "High", "Low"]):
        sys.exit(1)
    if not _validate_df(data_three_monthly, "Three-month data", ["Close"]):
        sys.exit(1)
    if not _validate_df(data_yearly, "Yearly data", ["Close"]):
        sys.exit(1)

    # Analysis
    high_low = analysis_api.get_high_low(data_monthly)

    if not isinstance(high_low, dict):
        print("Error: high_low must be a dict.")
        sys.exit(1)

    # Current price
    current_price = data_monthly["Close"].iloc[-1]

    if _is_nan(current_price) or current_price <= 0:
        print(f"Error: invalid current price: {current_price}")
        sys.exit(1)

    # Getting data
    low = high_low.get("low")
    high = high_low.get("high")

    if _is_nan(low) or _is_nan(high):
        print("Error: failed to compute high/low.")
        sys.exit(1)

    if low <= 0 or high <= 0:
        print(f"Error: invalid high/low values. High={high}, Low={low}")
        sys.exit(1)
    mid_point = (low + high) / 2

    # Round up low, high, current price and mid point to 2 decimal places
    high_r = round(high, 2)
    current_price_r = round(current_price, 2)
    mid_point_r = round(mid_point, 2)
    low_r = round(low, 2)

    # Display low - percentage - current price - percentage - high
    if current_price < mid_point:
        print(f"Low: {low_r}, Current: {current_price_r}, Mid Point: {mid_point_r}, High: {high_r}")
    else:
        print(f"Low: {low_r}, Mid Point: {mid_point_r}, Current: {current_price_r}, High: {high_r}")

    # Display bars
    ui_api.display_bars(low_r, high_r, current_price_r)

    # Analysis
    yearly_average_daily_growth_rate = _safe_rate(analysis_api.get_average_daily_growth_rate(data_yearly))
    yearly_average_daily_growth_rate_in_perc = _rate_to_percent(yearly_average_daily_growth_rate)

    three_monthly_average_daily_growth_rate = _safe_rate(analysis_api.get_average_daily_growth_rate(data_three_monthly))
    three_monthly_average_daily_growth_rate_in_perc = _rate_to_percent(three_monthly_average_daily_growth_rate)

    monthly_average_daily_growth_rate = _safe_rate(analysis_api.get_average_daily_growth_rate(data_monthly))
    monthly_average_daily_growth_rate_in_perc = _rate_to_percent(monthly_average_daily_growth_rate)

    # Calculate days to reach high price from current price
    days_yearly = _safe_days_to_target(current_price, high, yearly_average_daily_growth_rate)
    days_three_monthly = _safe_days_to_target(current_price, high, three_monthly_average_daily_growth_rate)
    days_monthly = _safe_days_to_target(current_price, high, monthly_average_daily_growth_rate)

    print()
    print(f"Days to reach 1-month high price ({high_r}) from current price ({current_price_r}):")
    print(f"  Using Yearly Average Daily Growth Rate: {_fmt_days(days_yearly)}. Rates={_fmt_percent(yearly_average_daily_growth_rate_in_perc)}")
    print(f"  Using Three Monthly Average Daily Growth Rate: {_fmt_days(days_three_monthly)}. Rates={_fmt_percent(three_monthly_average_daily_growth_rate_in_perc)}")
    print(f"  Using Monthly Average Daily Growth Rate: {_fmt_days(days_monthly)}. Rates={_fmt_percent(monthly_average_daily_growth_rate_in_perc)}")