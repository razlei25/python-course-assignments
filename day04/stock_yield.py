import os
import math
import calendar
from datetime import datetime, date, timedelta
from typing import Tuple, Optional

import pandas as pd


def _find_date_and_close_columns(df: pd.DataFrame) -> Tuple[str, str]:
    # return (date_col, close_col)
    date_candidates = ("Date", "date", "DATE", "timestamp", "Timestamp")
    close_candidates = ("Close", "close", "Adj Close", "Adj_Close", "adjclose")
    date_col = next((c for c in date_candidates if c in df.columns), None)
    if date_col is None:
        date_col = df.columns[0]
    close_col = next((c for c in close_candidates if c in df.columns), None)
    if close_col is None:
        close_col = next((c for c in df.columns if "close" in c.lower()), None)
    if close_col is None:
        raise RuntimeError("Could not find a closing-price column in the CSV")
    return date_col, close_col


def get_csv_date_range(csv_path: str) -> Tuple[date, date]:
    """Return (min_date, max_date) present in the CSV (date objects)."""
    if not os.path.isfile(csv_path):
        raise RuntimeError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    date_col, _ = _find_date_and_close_columns(df)
    df["_date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["_date"]).sort_values("_date").reset_index(drop=True)
    if df.empty:
        raise RuntimeError("No parseable dates in CSV")
    min_d = df["_date"].iloc[0].date()
    max_d = df["_date"].iloc[-1].date()
    return min_d, max_d


def _find_row_for_start_end(df: pd.DataFrame, start: date, end: date, date_col: str, close_col: str):
    """Return (start_row, end_row) where start_row is first row with date >= start (or earliest),
       end_row is last row with date <= end (or latest)."""
    df["_date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["_date"]).sort_values("_date").reset_index(drop=True)
    if df.empty:
        raise RuntimeError("No parseable dates in CSV")
    # convert to date objects
    df["_donly"] = df["_date"].dt.date
    # start_row: first with date >= start
    start_candidates = df[df["_donly"] >= start]
    if not start_candidates.empty:
        start_row = start_candidates.iloc[0]
    else:
        start_row = df.iloc[0]
    # end_row: last with date <= end
    end_candidates = df[df["_donly"] <= end]
    if not end_candidates.empty:
        end_row = end_candidates.iloc[-1]
    else:
        end_row = df.iloc[-1]
    return start_row, end_row


def calculate_yield_between_dates(csv_path: str, start_date: str, end_date: str) -> Tuple[float, date, date, float, float]:
    """
    Calculate average annual yield (CAGR) between two dates (inclusive) using closing prices in CSV.
    start_date and end_date are strings in YYYY-MM-DD (or any parseable by pandas.to_datetime).
    Returns tuple (cagr, start_date_obj, end_date_obj, start_price, end_price).
    """
    if not os.path.isfile(csv_path):
        raise RuntimeError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    date_col, close_col = _find_date_and_close_columns(df)

    # parse input dates
    sdt = pd.to_datetime(start_date, errors="coerce")
    edt = pd.to_datetime(end_date, errors="coerce")
    if pd.isna(sdt) or pd.isna(edt):
        raise ValueError("Start date or end date could not be parsed. Use YYYY-MM-DD.")
    s_date = sdt.date()
    e_date = edt.date()
    if s_date >= e_date:
        raise ValueError("Start date must be earlier than end date.")

    start_row, end_row = _find_row_for_start_end(df, s_date, e_date, date_col, close_col)
    start_price = float(start_row[close_col])
    end_price = float(end_row[close_col])
    actual_start_date = pd.to_datetime(start_row[date_col]).date()
    actual_end_date = pd.to_datetime(end_row[date_col]).date()

    if start_price <= 0:
        raise RuntimeError("Invalid start price for CAGR calculation")

    # compute fractional years between actual_start_date and actual_end_date
    delta_days = (actual_end_date - actual_start_date).days
    if delta_days <= 0:
        raise RuntimeError("Not enough time between chosen dates for calculation")
    years_fraction = delta_days / 365.2425  # approximate
    cagr = (end_price / start_price) ** (1.0 / years_fraction) - 1.0
    return float(cagr), actual_start_date, actual_end_date, start_price, end_price


def period_breakdown(start_date: date, end_date: date) -> Tuple[int, int, int]:
    """
    Return (years, months, days) as the calendar difference between start_date and end_date.
    """
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    y1, m1, d1 = start_date.year, start_date.month, start_date.day
    y2, m2, d2 = end_date.year, end_date.month, end_date.day

    years = y2 - y1
    months = m2 - m1
    days = d2 - d1

    if days < 0:
        # borrow days from previous month of end_date
        prev_month = m2 - 1
        prev_year = y2
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    return years, months, days


# Keep existing calculate_average_annual_yield for backward compatibility.
def calculate_average_annual_yield(csv_path: Optional[str], years: int) -> float:
    """
    Backwards compatible function: calculate CAGR using 'years' by using end = latest date,
    start = latest date - years (approx) and selecting first row on/after start.
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "stock_data", "aapl_us_d.csv")
    min_d, max_d = get_csv_date_range(csv_path)
    # approximate start date one year * years back
    approx_start = (pd.to_datetime(max_d) - pd.DateOffset(years=years)).date()
    cagr, s, e, sp, ep = calculate_yield_between_dates(csv_path, approx_start.isoformat(), max_d.isoformat())
    return cagr