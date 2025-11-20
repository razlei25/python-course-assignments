# filepath: day04/stock_yield_GUI.py
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
import importlib.util

# try to import calculation module
try:
    from day04 import stock_yield as _sy
except Exception:
    spec = importlib.util.spec_from_file_location("stock_yield", os.path.join(os.path.dirname(__file__), "stock_yield.py"))
    stock_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stock_mod)
    _sy = stock_mod

import pandas as pd
import webbrowser
import tkinter.font as tkfont


def _get_ticker_from_filename(path: str) -> str:
    name = os.path.basename(path)
    if "_" in name:
        return name.split("_", 1)[0].upper()
    return os.path.splitext(name)[0].upper()


def select_file(entry_widget, ticker_label, start_entry, end_entry):
    path = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not path:
        return
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, path)
    # update ticker
    ticker = _get_ticker_from_filename(path)
    ticker_label.config(text=f"Stock ticker symbol: {ticker}")
    # update default dates based on CSV
    try:
        min_d, max_d = _sy.get_csv_date_range(path)
        end_entry.delete(0, tk.END)
        end_entry.insert(0, max_d.isoformat())
        default_start = (pd.to_datetime(max_d) - pd.DateOffset(years=1)).date()
        start_entry.delete(0, tk.END)
        start_entry.insert(0, default_start.isoformat())
    except Exception:
        # ignore errors updating dates; leave user to edit
        pass


def on_compute(csv_entry, ticker_label, start_entry, end_entry, period_label, result_label):
    csv_path = csv_entry.get().strip()
    if not csv_path:
        csv_path = os.path.join(os.path.dirname(__file__), "stock_data", "aapl_us_d.csv")
    if not os.path.isfile(csv_path):
        messagebox.showerror("File not found", f"CSV not found:\n{csv_path}")
        return

    # check available data range first
    try:
        min_d, max_d = _sy.get_csv_date_range(csv_path)
    except Exception as exc:
        messagebox.showerror("Data error", f"Could not read date range from CSV:\n{exc}")
        return

    # parse user-entered dates (UI responsibility)
    s_text = start_entry.get().strip()
    e_text = end_entry.get().strip()
    s_parsed = pd.to_datetime(s_text, errors="coerce")
    e_parsed = pd.to_datetime(e_text, errors="coerce")
    if pd.isna(s_parsed) or pd.isna(e_parsed):
        messagebox.showerror("Invalid input", "Start date or end date could not be parsed. Use YYYY-MM-DD.")
        return
    s_date = s_parsed.date()
    e_date = e_parsed.date()

    # validate within available range
    if s_date < min_d or e_date > max_d:
        messagebox.showerror("Date range", f"Data available for {min_d.isoformat()} through {max_d.isoformat()} only.")
        return
    if s_date >= e_date:
        messagebox.showerror("Invalid range", "Start date must be earlier than end date.")
        return

    ticker = _get_ticker_from_filename(csv_path)
    try:
        cagr, actual_start, actual_end, start_price, end_price = _sy.calculate_yield_between_dates(csv_path, s_date.isoformat(), e_date.isoformat())
    except Exception as exc:
        messagebox.showerror("Calculation error", str(exc))
        return

    try:
        years, months, days = _sy.period_breakdown(actual_start, actual_end)
    except Exception:
        years, months, days = 0, 0, (actual_end - actual_start).days

    period_label.config(text=f"Time period: {years} years, {months} months and {days} days")
    result_label.config(text=(f"The average annual yield for stock {ticker} between {actual_start.isoformat()} "
                              f"and {actual_end.isoformat()} is {cagr * 100:.2f}%"))


def build_gui():
    root = tk.Tk()
    frm = ttk.Frame(root, padding=12)
    frm.grid(column=0, row=0, sticky="nsew")

    # Instruction text and clickable link
    instr_text = "Select a CSV file with stock data from Stooq. You can download data of your stock of choice at:"
    ttk.Label(frm, text=instr_text, wraplength=520, justify="left").grid(column=0, row=0, columnspan=3, sticky="w", pady=(0,0))
    link = "https://stooq.com/"
    link_font = tkfont.Font(underline=True)
    link_lbl = tk.Label(frm, text=link, fg="blue", cursor="hand2", font=link_font, anchor="w", justify="left")
    link_lbl.grid(column=0, row=1, columnspan=3, sticky="w", pady=(0,8))
    link_lbl.bind("<Button-1>", lambda e: webbrowser.open(link))

    ttk.Label(frm, text="CSV file (optional)").grid(column=0, row=2, sticky="w")
    csv_entry = ttk.Entry(frm, width=56)
    csv_entry.grid(column=0, row=3, sticky="w")
    default_csv = os.path.join(os.path.dirname(__file__), "stock_data", "aapl_us_d.csv")
    csv_entry.insert(0, default_csv)
    # placeholder ticker label to be updated
    ticker_lbl = ttk.Label(frm, text=f"Stock ticker symbol: {_get_ticker_from_filename(default_csv)}")
    ttk.Button(frm, text="Browse...", command=lambda: select_file(csv_entry, ticker_lbl, start_entry, end_entry)).grid(column=1, row=3, padx=6)
    ticker_lbl.grid(column=0, row=4, sticky="w", pady=(8,0))

    # Date selectors
    ttk.Label(frm, text="Start date (YYYY-MM-DD)").grid(column=0, row=5, sticky="w", pady=(8,0))
    start_entry = ttk.Entry(frm, width=20)
    start_entry.grid(column=0, row=6, sticky="w")
    ttk.Label(frm, text="End date (YYYY-MM-DD)").grid(column=1, row=5, sticky="w", pady=(8,0))
    end_entry = ttk.Entry(frm, width=20)
    end_entry.grid(column=1, row=6, sticky="w")

    # populate default dates from CSV
    try:
        min_d, max_d = _sy.get_csv_date_range(default_csv)
        end_entry.delete(0, tk.END)
        end_entry.insert(0, max_d.isoformat())
        start_default = (pd.to_datetime(max_d) - pd.DateOffset(years=1)).date()
        start_entry.delete(0, tk.END)
        start_entry.insert(0, start_default.isoformat())
    except Exception:
        today = date.today()
        end_entry.insert(0, today.isoformat())
        start_entry.insert(0, (today - timedelta(days=365)).isoformat())

    # Compute button and result areas
    compute_btn = ttk.Button(frm, text="Compute CAGR", command=lambda: on_compute(csv_entry, ticker_lbl, start_entry, end_entry, period_lbl, result_lbl))
    compute_btn.grid(column=0, row=7, pady=12, sticky="w")

    period_lbl = ttk.Label(frm, text="Time period: --")
    period_lbl.grid(column=0, row=8, sticky="w", pady=(4,0))
    result_lbl = ttk.Label(frm, text="CAGR: --")
    result_lbl.grid(column=0, row=9, sticky="w", pady=(4,0))

    root.columnconfigure(0, weight=1)
    return root


if __name__ == "__main__":
    app = build_gui()
    app.mainloop()