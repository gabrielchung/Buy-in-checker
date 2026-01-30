def get_high_low(df):
    return {
        "high": float(df["High"].max()),
        "low": float(df["Low"].min()),
    }

def get_average_daily_growth_rate(df):
    start_price = df["Close"].iloc[0]
    end_price = df["Close"].iloc[-1]

    # Number of trading days (N) = total observations - 1
    num_days = len(df) - 1
    if num_days <= 0:
        return 0.0

    # Average daily growth rate formula:
    # r = (EndPrice / StartPrice)^(1 / N) - 1
    average_daily_growth_rate = (end_price / start_price) ** (1 / num_days) - 1

    return average_daily_growth_rate

import math

# Display how long it takes to reach target price from current price
def calculate_days_to_reach_target(current_price, target_price, daily_growth_rate):
    """
    Calculates the number of days n needed such that:
        target_price <= current_price * (1 + daily_growth_rate)^n

    Formula:
        n = ceil( log(target_price / current_price) / log(1 + daily_growth_rate) )
    """
    if current_price >= target_price:
        return 0

    if daily_growth_rate <= 0:
        return float("inf")  # Will never reach the target price

    base = 1.0 + daily_growth_rate
    if base <= 0:
        return float("inf")

    days = math.log(target_price / current_price) / math.log(base)
    return int(math.ceil(days))
    