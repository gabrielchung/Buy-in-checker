import sys

# Input

def parse_ticker(argv):
    if len(argv) < 2:
        print("Usage: python one.py <TICKER>")
        sys.exit(2)

    ticker = argv[1].strip().upper()
    if not ticker:
        print("Error: TICKER cannot be empty.")
        sys.exit(2)

    return ticker


# Output

def display_bars(low, high, current_price):
    # Display an ascii percentage bar with 25%, 50%, 75% markers with bar_length of 50
    bar_length = 50
    low_pos = 0
    high_pos = bar_length
    quarter_pos = bar_length // 4
    mid_pos = bar_length // 2
    three_quarter_pos = 3 * bar_length // 4

    # Guard against division by zero and clamp current_pos
    if high == low:
        print(f"L{'=' * (bar_length - 1)}H  (flat: {low:.2f})")
    else:
        ratio = (current_price - low) / (high - low)
        current_pos = int(round(ratio * bar_length))
        current_pos = max(0, min(bar_length, current_pos))

        bar = ['-'] * (bar_length + 1)
        bar[low_pos] = 'L'
        bar[high_pos] = 'H'
        bar[quarter_pos] = '|'
        bar[mid_pos] = '|'
        bar[three_quarter_pos] = '|'

        # Let current overwrite ticks (or swap the order if you prefer)
        bar[current_pos] = 'C'

        # print("".join(bar))

        # Labels under the bar (keeps alignment correct)
        labels = [' '] * (bar_length + 1)
        for pos, txt in [(quarter_pos, "25%"), (mid_pos, "50%"), (three_quarter_pos, "75%")]:
            start = max(0, min(bar_length - (len(txt) - 1), pos - len(txt) // 2))
            for i, ch in enumerate(txt):
                labels[start + i] = ch

        # print("".join(labels))

        # Display
        print("".join(labels))
        print("".join(bar))

    # Display an ascii bar chart of the low, current price, and high
    bar_length = 50
    low_pos = 0
    high_pos = bar_length
    current_pos = int(((current_price - low) / (high - low)) * bar_length)
    bar = ['-'] * (bar_length + 1)
    bar[low_pos] = 'L'
    bar[high_pos] = 'H'
    bar[current_pos] = 'C'
    # print("".join(bar))
    # print(f"{low:.2f}{' ' * (current_pos - low_pos - 1)}{current_price:.2f}{' ' * (high_pos - current_pos - 1)}{high:.2f}")
