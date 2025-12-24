# Assignment 8 processes

## Program
This program, **the Israeli local authorities visualizer**, processes and visualizes data about local authorities in Israel. In the example provided, it take the Excel file `p_libud_23.xlsx`, saved in the `data` folder. It extracts relevant information, filters categories, and generates several statistical plots, saving them as PNG images in the `plots` folder.


You can find Excel files for previous years in the Central Bureau of Statistics website ([Local Authorities in Israel - Data Files for Processing 1999 - 2023](https://www.cbs.gov.il/he/publications/Pages/2019/%D7%94%D7%A8%D7%A9%D7%95%D7%99%D7%95%D7%AA-%D7%94%D7%9E%D7%A7%D7%95%D7%9E%D7%99%D7%95%D7%AA-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%A7%D7%95%D7%91%D7%A6%D7%99-%D7%A0%D7%AA%D7%95%D7%A0%D7%99%D7%9D-%D7%9C%D7%A2%D7%99%D7%91%D7%95%D7%93-1999-2017.aspx)).


- Plots:
  - Bar chart of local authorities by district
  - Pie chart of municipal status & Pie chart of population by municipal status
  - Boxplot of socio-economic index by district


## Operation
Run the program and generate the plots by running `data_wringler.py`

### Dependencies
This project requires the following Python packages (listed in `pyproject.toml`):
- pandas
- numpy
- matplotlib
- openpyxl
- python-bidi (for right-to-left text support, if needed)
- arabic-reshaper (for right-to-left text support, if needed)

**To install dependencies:**
If you are using the provided virtual environment, run:

```
pip install -r requirements.txt
```

Or, if you want to install manually:

```
pip install pandas numpy matplotlib openpyxl python-bidi arabic-reshaper
```


### System versions
- Python 3.8+ (tested with 3.8)
- Windows (tested on Windows 10)


