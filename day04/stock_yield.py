import os
from typing import Optional
import pandas as pd

def calculate_average_annual_yield(csv_path: Optional[str], years: int) -> float:
    """
    Calculate average annual yield (CAGR) based on closing prices in csv_path over `years`.
    csv_path: path to CSV file; if None, looks for 'aapl_us_d.csv' in this module's folder.
    Returns CAGR as a float (e.g. 0.083 -> 8.3%).
    Raises ValueError on bad input or RuntimeError if data insufficient.
    """
    if years <= 0:
        raise ValueError("years must be a positive integer")

    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "aapl_us_d.csv")
    if not os.path.isfile(csv_path):
        raise RuntimeError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # find date column
    date_col = None
    for c in ("Date", "date", "DATE", "timestamp", "Timestamp"):
        if c in df.columns:
            date_col = c
            break
    if date_col is None:
        date_col = df.columns[0]

    df["_date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["_date"]).sort_values("_date").reset_index(drop=True)
    if df.empty:
        raise RuntimeError("No parseable dates in CSV")

    # find close column
    close_col = None
    for c in ("Close", "close", "Adj Close", "Adj_Close", "adjclose"):
        if c in df.columns:
            close_col = c
            break
    if close_col is None:
        for c in df.columns:
            if "close" in c.lower():
                close_col = c
                break
    if close_col is None:
        raise RuntimeError("Could not find a closing-price column in the CSV")

    end_row = df.iloc[-1]
    end_price = float(end_row[close_col])
    end_date = pd.to_datetime(end_row["_date"])

    start_target = end_date - pd.DateOffset(years=years)
    candidates = df[df["_date"] >= start_target]
    if not candidates.empty:
        start_row = candidates.iloc[0]
    else:
        start_row = df.iloc[0]

    start_price = float(start_row[close_col])
    if start_price <= 0:
        raise RuntimeError("Invalid start price for CAGR calculation")

    cagr = (end_price / start_price) ** (1.0 / years) - 1.0
    return float(cagr)

def main():
    # CSV file path (file in same folder)
    csv_path = os.path.join(os.path.dirname(__file__), "aapl_us_d.csv")
    if not os.path.isfile(csv_path):
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print("Failed to read CSV:", e)
        sys.exit(1)

    date_col = find_date_column(df)
    if date_col is None:
        print("Could not detect a date column in the CSV.")
        sys.exit(1)

    try:
        df["Date"] = pd.to_datetime(df[date_col])
    except Exception as e:
        print("Could not parse dates:", e)
        sys.exit(1)

    close_col = find_close_column(df)
    if close_col is None:
        print("Could not find a closing-price column in the CSV (e.g. 'Close' or 'Adj Close').")
        sys.exit(1)

    # Keep only Date and close for clarity
    df = df[["Date", close_col]].rename(columns={close_col: "Close"})
    df = df.sort_values("Date").reset_index(drop=True)

    # Get user input for years
    raw = input("Enter number of years to look back (integer > 0): ").strip()
    try:
        years = int(raw)
        if years <= 0:
            raise ValueError
    except Exception:
        print("Please enter a positive integer for years.")
        sys.exit(1)

    end_date = df["Date"].max()
    end_row = df[df["Date"] == end_date].iloc[-1]
    end_price = float(end_row["Close"])

    # target start date = end_date - years
    start_target = end_date - pd.DateOffset(years=years)

    # find first row with Date >= start_target (closest on/after)
    candidates = df[df["Date"] >= start_target]
    if not candidates.empty:
        start_row = candidates.iloc[0]
    else:
        # if no date on/after target, use earliest available
        start_row = df.iloc[0]

    start_date = start_row["Date"]
    start_price = float(start_row["Close"])

    try:
        cagr = compute_cagr(start_price, end_price, years)
    except Exception as e:
        print("Error computing CAGR:", e)
        sys.exit(1)

    print()
    print(f"Data file: {os.path.basename(csv_path)}")
    print(f"Period used: {start_date.date()} -> {end_date.date()} (~{years} years)")
    print(f"Start close: {start_price:.4f} (date: {start_date.date()})")
    print(f"End   close: {end_price:.4f} (date: {end_date.date()})")
    print(f"Average annual yield (CAGR): {cagr * 100:.2f}%")

if __name__ == "__main__":
    main()