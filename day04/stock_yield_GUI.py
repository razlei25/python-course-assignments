# GUI only: calls calculate_average_annual_yield from stock_yield.py
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# try import the calculation function from local module
try:
    from day04 import stock_yield as _sy  # if package layout supports it
except Exception:
    try:
        import importlib.util
        import importlib
        spec = importlib.util.spec_from_file_location("stock_yield", os.path.join(os.path.dirname(__file__), "stock_yield.py"))
        if spec and spec.loader:
            stock_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stock_mod)
            _sy = stock_mod
        else:
            _sy = importlib.import_module("stock_yield")
    except Exception:
        message = ("Could not import stock_yield module. Ensure day04/stock_yield.py exists "
                   "and is importable. Install pandas in the venv.")
        print(message)
        raise

def select_file(entry_widget):
    path = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV files","*.csv"),("All files","*.*")])
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

def on_compute(csv_entry, years_entry, result_label):
    csv_path = csv_entry.get().strip()
    if not csv_path:
        csv_path = os.path.join(os.path.dirname(__file__), "aapl_us_d.csv")
    if not os.path.isfile(csv_path):
        messagebox.showerror("File not found", f"CSV not found:\n{csv_path}")
        return
    try:
        years = int(years_entry.get().strip())
        if years <= 0:
            raise ValueError
    except Exception:
        messagebox.showerror("Invalid input", "Please enter a positive integer for years.")
        return

    try:
        cagr = _sy.calculate_average_annual_yield(csv_path, years)
    except Exception as e:
        messagebox.showerror("Calculation error", str(e))
        return

    result_label.config(text=f"CAGR: {cagr * 100:.2f}%")

def build_gui():
    root = tk.Tk()
    root.title("Stock Average Annual Yield")

    frm = ttk.Frame(root, padding=12)
    frm.grid(column=0, row=0, sticky="nsew")

    ttk.Label(frm, text="CSV file (optional)").grid(column=0, row=0, sticky="w")
    csv_entry = ttk.Entry(frm, width=48)
    csv_entry.grid(column=0, row=1, sticky="w")
    csv_entry.insert(0, os.path.join(os.path.dirname(__file__), "aapl_us_d.csv"))
    ttk.Button(frm, text="Browse...", command=lambda: select_file(csv_entry)).grid(column=1, row=1, padx=6)

    ttk.Label(frm, text="Years to look back").grid(column=0, row=2, sticky="w", pady=(8,0))
    years_entry = ttk.Entry(frm, width=12)
    years_entry.grid(column=0, row=3, sticky="w")
    years_entry.insert(0, "1")

    compute_btn = ttk.Button(frm, text="Compute CAGR", command=lambda: on_compute(csv_entry, years_entry, result_lbl))
    compute_btn.grid(column=0, row=4, pady=12, sticky="w")

    result_lbl = ttk.Label(frm, text="CAGR: --")
    result_lbl.grid(column=0, row=5, sticky="w")

    root.columnconfigure(0, weight=1)
    return root

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()