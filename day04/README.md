# Assignemnt 4 processes

## Program explanation

This program loads historical stock-price CSV files (Stooq format) and computes the average annual yield (CAGR) for a user-specified period. A tkinter GUI lets the user choose a CSV, pick start and end dates (defaults are taken from the CSV), and then displays the time period breakdown and the calculated annual yield.

Project file directory (relevant files)
- day04/
  - stock_yield.py            — business logic: CSV parsing, date handling, CAGR calculation
  - stock_yield_GUI.py        — tkinter GUI that calls functions in stock_yield.py
  - stock_data/               — folder containing CSV data files
    - aapl_us_d.csv
    - msft_us_d.csv

Note: the stock CSVs are stored in the stock_data subfolder under day04. Use the GUI to select any CSV in that folder (or another compatible Stooq-format CSV). 