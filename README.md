# StockInsight 📈

StockInsight is a Python-based financial data analysis project that fetches market data and uses technical indicators to help analyze price trends and market behavior.

## 🚀 Features

- Fetches financial market data using Yahoo Finance
- Supports stock and cryptocurrency tickers
- Calculates technical indicators such as:
  - SMA (Simple Moving Average)
  - EMA (Exponential Moving Average)
- Visualizes price data and indicators using Matplotlib
- Provides an interactive analysis interface
- Allows users to change the selected asset and analyze different market data

## 🛠️ Technologies Used

- **Python**
- **Pandas** — data processing and analysis
- **yfinance** — retrieving market data from Yahoo Finance
- **Matplotlib** — data visualization
- **Tkinter / Python GUI** — interactive controls

## 📊 Technical Indicators

### SMA — Simple Moving Average

SMA calculates the average closing price over a specific number of periods.

For example:

**SMA20** represents the average closing price over the previous 20 periods.

### EMA — Exponential Moving Average

EMA is another moving average that gives greater weight to more recent prices, making it more responsive to recent price changes.

## 📈 Example Analysis

The project can be used to analyze assets such as:

- Stocks
- Cryptocurrency
- Other assets supported by Yahoo Finance

Example ticker:

```text
SHIB-USD
```

The application retrieves the available market data and generates visualizations for analysis.

## ⚙️ Installation

Clone the repository:

```bash
git clone <https://github.com/tabishjilani-CS50/StockInsights.git>
cd StockInsight
```

Install the required Python packages:

```bash
pip install pandas yfinance matplotlib
```

Then run the main Python file:

```bash
python <main-file>.py
```

## 📁 Project Structure

```text
StockInsight/
│
├── main.py
├── README.md
└── ...
```

The exact file structure may vary depending on the current version of the project.

## 🎯 Purpose

StockInsight was built as a Python learning project to practice:

- Working with external financial APIs/data sources
- Data cleaning and manipulation with Pandas
- Technical indicator calculations
- Data visualization
- Building an interactive Python application

## 🔮 Future Improvements

Possible future improvements include:

- Additional technical indicators
- More customizable charts
- Portfolio tracking
- Improved data filtering
- More advanced statistical analysis
- Machine-learning-based analysis as a separate experimental component

## 👨‍💻 Author

**Tabish Jilani**

Built as a personal Python and financial-data analysis project.
