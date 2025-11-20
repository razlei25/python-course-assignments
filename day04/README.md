# Assignemnt 4 processes

## Program explanation

To use the program through a GUI, run stock_yield_GUI.py

This program loads historical stock-price CSV files (Stooq format) and computes the average annual yield (CAGR) for a user-specified period. A tkinter GUI lets the user choose a CSV, pick start and end dates (defaults are taken from the CSV), and then displays the time period breakdown and the calculated annual yield.

Project file directory (relevant files)
- day04/
  - stock_yield.py            — business logic: CSV parsing, date handling, CAGR calculation
  - stock_yield_GUI.py        — tkinter GUI that calls functions in stock_yield.py
  - stock_data/               — folder containing CSV data files
    - aapl_us_d.csv
    - msft_us_d.csv

Note: the stock CSVs are stored in the stock_data subfolder under day04. Use the GUI to select any CSV in that folder (or another compatible Stooq-format CSV which you can download from the website [https://stooq.com](https://stooq.com)).



## Dependencies

Required
- Python 3.8+ (the project was developed with Python 3.8)
- pandas — used for CSV parsing and date handling
- tkinter — standard library GUI toolkit (usually included with standard CPython on Windows)

Install commands (from project root; use the project venv if you have one)
PowerShell:
````powershell
# ensure venv python is used (optional)
.\.venv\Scripts\Activate.ps1

# install required libraries
python -m pip install --upgrade pip
python -m pip install pandas
````


## AI usage
AI copilot prompts (GPT-5mini):
* “In stock_graph_GUI.py write a code that will take data from the file day04/aapl_us_d.csv (which contains historic stock price data for a specific stock) and an input from the user (an integer: n) and calculate the average annual yield (based on the closing price of the stock) across the last n years (last date is the most recent date in the data).”
* “Write a code in stock_yield_GUI.py that will be the user interface for the program written in stock_yield.py. It should use the functions from stock_yield.py file.”
* “This should be a GUI. It shouldn't include new calculations or "business logic" not included in stock_yield.py (if needed, update stock_yield.py with necessary code so stock_yield_GUI.py would not include anything that doesn't have to do directly with user interface).”
* “Now I want to add features. First text (above file browsing cell): "Select a CSV file with stock data from Stooq. You can download data of your stock of choice in the following link: https://stooq.com/". The default file should be the first CSV already provided in the folder (aapl_us_d.csv). After uploading a file, show the stock ticker symbol (or if file not changed, use the default file ticker symbol). Write "Stock ticker symbol: {sicker symbol}". The ticker symbol will be the first letters in the CSV filename before underscore (_) and they are typically capitalized. Then, instead of the user inputting an integer to be used as the number of years back to calculate the annual average, now the user will have the option to choose two dates, one for the start of the period and another for the end of the period (the default dates before an input from the user will be the most recent data in the CSV file as the end date and a year prior to that as the start date). The program will then calculate the length of time between these two dates and present it to the user as: "Time period: {years} years, {months} months and {days} days", where the sum of the years, months and days is the length of the total period. Then it will show the user the text: "The average annual yield for stock {ticker symbol} between {start date} and {end date} is {calculated annual yield}".”
* “When the user inputs dates before or after the first (oldest) and last (most recent) date in the data, they should get a message "Data available for {first date} through {last date} only." Don't calculate the annual yield until they input valid dates (within the timeframe of the data provided). To clarify, the whole code should of course work on other files in the same format (data of other stocks, as an example msft_us_d.csv in the same day04 folder).”
* “Okay, now that I changed the directory of the CSV files, change the default in the code as well (I moved them to the subfolder stock_data which is saved in the same day04 folder).”
