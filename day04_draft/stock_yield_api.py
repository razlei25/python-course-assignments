### Do not run this code, it is saved for internal purposes only. ###



"""
Simple CLI that loads historical closing prices for a ticker and computes
the average annual yield (CAGR) over a user-specified number of years.

Primary attempt: use the installed 'stock-data-loader' package.
Fallback: use yfinance if stock-data-loader isn't available or can't be used.

Usage:
    python stock_graph.py
"""
from datetime import datetime, timedelta
import importlib
import sys


def prompt_inputs():
    ticker = input("Enter ticker symbol (e.g. AAPL): ").strip().upper()
    if not ticker:
        print("Ticker cannot be empty.")
        sys.exit(1)
    years_raw = input("Enter number of years to look back (integer > 0): ").strip()
    try:
        years = int(years_raw)
        if years <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive integer for years.")
        sys.exit(1)
    return ticker, years

def try_stock_data_loader(ticker, start, end):
    """
    Try to use the installed 'stock-data-loader' package.
    This version tries the StockDataLoader class (load_symbol_data accepts a list)
    and normalizes returned pandas Series/DataFrame into a DataFrame suitable
    for extract_close_series().
    """
    try:
        module = importlib.import_module("stock_data_loader")
    except Exception:
        return None

    try:
        import pandas as pd
    except Exception:
        pd = None

    def normalize_result(res):
        # Convert Series -> DataFrame(name='Close'), handle wide-format DataFrame
        try:
            if pd is not None:
                if isinstance(res, pd.Series):
                    return res.to_frame(name="Close")
                if isinstance(res, pd.DataFrame):
                    # If long format with a 'symbol' column, filter by ticker
                    if "symbol" in res.columns:
                        df = res[res["symbol"].astype(str).str.upper() == ticker]
                        if not df.empty:
                            return df
                    if "ticker" in res.columns:
                        df = res[res["ticker"].astype(str).str.upper() == ticker]
                        if not df.empty:
                            return df
                    # If wide format where each ticker is a column, pick that column
                    if ticker in res.columns:
                        return res[[ticker]].rename(columns={ticker: "Close"})
                    # If there is a 'close' or 'Close' column, return as-is
                    for cname in ("Close", "close", "Adj Close", "adjclose", "Adj_Close"):
                        if cname in res.columns:
                            return res
            # Last resort: if it's a dict with relevant key(s)
            if isinstance(res, dict):
                for k in ("Close", "close", "Adj Close", "adjclose", "Adj_Close"):
                    if k in res:
                        return res[k]
        except Exception:
            pass
        return None

    # Try class-based loader first (matches example usage)
    cls = getattr(module, "StockDataLoader", None) or getattr(module, "Loader", None)
    if cls:
        try:
            loader = cls()
        except Exception:
            loader = None
        if loader:
            method_names = ("load_symbol_data", "load_symbols", "load", "load_data", "get_history", "get_prices")
            for name in method_names:
                func = getattr(loader, name, None)
                if callable(func):
                    # try common call patterns: list of symbols, with/without start/end
                    attempts = [
                        ([ [ticker] ], {"start": start, "end": end}),
                        ([ [ticker] ], {}),
                        ([ [ticker], start, end ], {}),
                        ([ticker], {"start": start, "end": end}),
                        ([ticker], {}),
                    ]
                    for args, kwargs in attempts:
                        try:
                            res = func(*args, **kwargs)
                        except TypeError:
                            continue
                        except Exception:
                            # loader might raise if wrong args; try other forms
                            continue
                        norm = normalize_result(res)
                        if norm is not None:
                            return norm
            # fallthrough if no method worked
    # Try top-level convenience functions
    top_funcs = ("load_symbol_data", "load_symbols", "load", "load_data", "get_history", "get_prices")
    for name in top_funcs:
        func = getattr(module, name, None)
        if callable(func):
            attempts = [
                ([ [ticker] ], {"start": start, "end": end}),
                ([ [ticker] ], {}),
                ([ [ticker], start, end ], {}),
                ([ticker], {"start": start, "end": end}),
                ([ticker], {}),
            ]
            for args, kwargs in attempts:
                try:
                    res = func(*args, **kwargs)
                except TypeError:
                    continue
                except Exception:
                    continue
                norm = normalize_result(res)
                if norm is not None:
                    return norm

    return None

def fallback_yfinance(ticker, start, end):
    try:
        import yfinance as yf
    except Exception:
        return None
    # yfinance expects string dates
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=(end + timedelta(days=1)).strftime("%Y-%m-%d"), progress=False)
    return df

def extract_close_series(df):
    """
    Given a DataFrame-like object, return a series-like object of closing prices.
    Accept common column names: 'Close', 'close', 'Adj Close', 'adjclose', 'Adj_Close'
    """
    # Prefer pandas-like API; avoid hard dependency on pandas in type checks
    cols = []
    try:
        cols = list(df.columns)
    except Exception:
        # df may be a dict-like object from unknown loader; try some keys
        if isinstance(df, dict):
            for k in ("Close", "close", "Adj Close", "adjclose", "Adj_Close"):
                if k in df:
                    return df[k]
        return None

    preferred = ("Close", "close", "Adj Close", "Adj_Close", "adjclose", "AdjClose")
    for p in preferred:
        if p in cols:
            return df[p]
    return None

def compute_cagr(start_price, end_price, years):
    if start_price <= 0:
        raise ValueError("Start price must be > 0 for CAGR calculation.")
    return (end_price / start_price) ** (1.0 / years) - 1.0

def plot_series(series, ticker):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available; skipping plot.")
        return
    try:
        plt.figure(figsize=(8,4))
        plt.plot(series.index, series.values, label=f"{ticker} Close")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.title(f"{ticker} closing prices")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Could not plot series:", e)

def main():
    ticker, years = prompt_inputs()
    today = datetime.utcnow().date()
    start = today - timedelta(days=years * 365)

    df = try_stock_data_loader(ticker, start, today)
    if df is None:
        print("Could not load data with 'stock-data-loader'. Trying yfinance as fallback...")
        df = fallback_yfinance(ticker, start, today)
        if df is None:
            print("No data loader available. Install 'stock-data-loader' or 'yfinance' (pip).")
            sys.exit(1)

    series = extract_close_series(df)
    if series is None:
        print("Could not find a 'Close' column in the loaded data.")
        sys.exit(1)

    # Ensure we have at least two valid prices
    try:
        # drop NA and sort by index if possible
        cleaned = series.dropna()
        if len(cleaned) < 2:
            raise ValueError("Not enough price data points.")
        start_price = float(cleaned.iloc[0])
        end_price = float(cleaned.iloc[-1])
    except Exception as e:
        print("Error extracting start/end prices:", e)
        sys.exit(1)

    try:
        cagr = compute_cagr(start_price, end_price, years)
    except Exception as e:
        print("Error computing CAGR:", e)
        sys.exit(1)

    print(f"\nTicker: {ticker}")
    print(f"Period: {start} to {today} (~{years} years)")
    print(f"Start close: {start_price:.4f}")
    print(f"End close:   {end_price:.4f}")
    print(f"Average annual yield (CAGR): {cagr*100:.2f}%")

    # Offer plot
    want_plot = input("Show price graph? [y/N]: ").strip().lower()
    if want_plot == "y":
        plot_series(cleaned, ticker)

if __name__ == "__main__":
    main()