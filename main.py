import yfinance as yf
import pandas as df 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.widgets import Button
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
ticker = input("Enter the stock: ")
stock = yf.Ticker(ticker)

history = yf.download(
    ticker,
    period="6mo",
    interval="1h",
    auto_adjust=False
)

if isinstance(history.columns, pd.MultiIndex):
    history.columns = history.columns.get_level_values(0)

HORIZON = 240

history["future_return"] = (
    history["Close"].shift(-HORIZON) / history["Close"]
) - 1

history["target"] = np.where(
    history["future_return"] >= 0.001,
    1,
    np.where(
        history["future_return"] <= -0.001,
        0,
        np.nan
    )
)
window_size = 720

X = []
y = []

for i in range(window_size, len(history) - 1):
    window = history.iloc[i - window_size:i]

    X.append(window[["Open", "High", "Low", "Close", "Volume"]].values)
    y.append(history["target"].iloc[i])
if history.empty:
    print("Enter a valid String")
    exit()
X = np.array(X)
y = np.array(y)
print("SELL examples:", np.sum(y == 0))
print("BUY examples:", np.sum(y == 1))

X = X.reshape(X.shape[0], -1)

print("X shape:", X.shape)
print("y shape:", y.shape)
split = int(len(X) * 0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

print("NaN in y_train:", np.isnan(y_train).sum())
print("NaN in y_test:", np.isnan(y_test).sum())

# Remove rows where target is NaN
train_mask = ~np.isnan(y_train)
test_mask = ~np.isnan(y_test)

X_train = X_train[train_mask]
y_train = y_train[train_mask]

X_test = X_test[test_mask]
y_test = y_test[test_mask]

print("Training samples after NaN removal:", len(y_train))
print("Testing samples after NaN removal:", len(y_test))

# Train model
model.fit(X_train, y_train)
model.fit(X_train, y_train)

print("Model trained successfully.")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Test accuracy:", accuracy)

print("\nClassification report:")
print(classification_report(y_test, predictions))
# Candle analysis

recent_candles = history[["Open", "High", "Low", "Close"]].tail(10)

candle_body = abs(
    recent_candles["Close"] - recent_candles["Open"]
)

upper_wick = (
    recent_candles["High"]
    - recent_candles[["Open", "Close"]].max(axis=1)
)

lower_wick = (
    recent_candles[["Open", "Close"]].min(axis=1)
    - recent_candles["Low"]
)

latest_body = candle_body.iloc[-1]
latest_upper_wick = upper_wick.iloc[-1]
latest_lower_wick = lower_wick.iloc[-1]

latest_open = recent_candles["Open"].iloc[-1]
latest_close = recent_candles["Close"].iloc[-1]

if latest_close > latest_open:
    candle_direction = "BULLISH"
elif latest_close < latest_open:
    candle_direction = "BEARISH"
else:
    candle_direction = "DOJI"


print(history.isnull().sum())

connection = sqlite3.connect("stockinsights.db")

connection.execute("""
CREATE TABLE IF NOT EXISTS stock_data (
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    UNIQUE(ticker, date)
)
""")

# Validate OHLC data

valid_ohlc = (
    (history["High"] >= history["Open"]) &
    (history["High"] >= history["Close"]) &
    (history["Low"] <= history["Open"]) &
    (history["Low"] <= history["Close"]) &
    (history["High"] >= history["Low"])
)

if valid_ohlc.all():
    print("OHLC data is valid")
else:
    print("Invalid OHLC data found")

clean_history = history[valid_ohlc]


# Save clean data to SQLite

for date, row in clean_history.iterrows():
    connection.execute("""
        INSERT OR IGNORE INTO stock_data
        (ticker, date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        ticker,
        str(date),
        row["Open"],
        row["High"],
        row["Low"],
        row["Close"],
        row["Volume"]
    ))

connection.commit()

print("Data saved to database.")

connection.close()
"""first"""
first = history.Close.iloc[-1]
"""last"""
last  = history.Close.iloc[0]
'''max'''
max= history.Close.max()
'''min'''
min = history.Close.min()
'''volume'''
mean = history.Volume.mean()
"""mean"""
mean = (last - first)/first*100 

"""monthly"""
monthly = (last - first) / first * 100

"""window"""
window = history.Close.rolling(20)

"""SMA20"""
SMA20 = history.Close.rolling(20).mean()

if last > SMA20.iloc[-1] :
    print("Price is above the 20-day average")
else:
    print("Price is below the 20-day average")

    '''history of SMA20'''
history["SMA20"] = history.Close.rolling(20).mean()

'''latest close'''
latest_close = history.Close.iloc[-1]

'''EMA20 '''

EMA20 = history.Close.ewm(span=20, adjust=False).mean()

'''latest EMA20'''
latest_EMA20 = EMA20.iloc[-1]

score = 0 

if latest_close > SMA20.iloc[-1]:
    trend = "Price is above the 20-day average"
else:
    trend = "Price is below the 20-day average"
    score = 0


''' first close'''
first_close = history.Close.iloc[0]

'''monthly return '''
monthly_return = (latest_close - first_close) / first * 100

"""delta"""
delta = history.Close.diff()

'''gain'''
gain = delta.clip(lower = 0)

'''loss'''
loss = loss = -delta.clip(upper=0)

"""average gain"""
average_gain = gain.rolling(14).mean()

'''average loss'''
average_loss = loss.rolling(14).mean()

''' relative strength (RS) '''
rs = average_gain/average_loss

'''RSI'''
rsi = 100-(100/(1+rs))

"""latest RSI"""
latest_rsi = rsi.iloc[-1]

'''RSI status'''
latest_rsi = rsi.iloc[-1]

if latest_rsi > 70:
    rsi_status = "OVERBOUGHT"
elif latest_rsi < 30:
    rsi_status = "OVERSOLD"
else:
    rsi_status = "NEUTRAL"


'''12 DAY EMA '''
EMA12 = history.Close.ewm(span=12, adjust=False).mean()

'''26 DAY EMA'''
EMA26 = history.Close.ewm(span=26, adjust=False).mean()

'''MACD'''
MACD = EMA12 - EMA26

""""latest MACD"""
latest_MACD = MACD.iloc[-1]
'''SIGNAL'''
signal = MACD.ewm(span = 9, adjust = False).mean()

'''latest signal ''' 
latest_signal = signal.iloc[-1]
''' MACD signal'''
macd_status = MACD.iloc[-1]
if latest_MACD > latest_signal:
    macd_status = "BULLISH"
else:
    macd_status = "BEARISH"
'''STD20'''
std20 = history.Close.rolling(20).std()

'''latest STD20'''
latest_std20 = std20.iloc[-1]
'''Upper band'''
upper_band = SMA20 + (2 * std20)

''' lower band '''
lower_band = SMA20 - (2 * std20)

'''latest upper band '''
latest_upper_band = upper_band.iloc[-1]

'''latest lower band'''
latest_lower_band = lower_band.iloc[-1]

'''bollinger status'''
if latest_close > latest_upper_band:
    bollinger_status = "ABOVE UPPER BAND"
elif latest_close < latest_lower_band:
    bollinger_status = "BELOW LOWER BAND"
else:
    bollinger_status = "INSIDE BANDS"

    """decison status """
if latest_close > SMA20.iloc[-1]:
    score += 1
else:
    score -= 1
if latest_close > latest_EMA20:
    score += 1
else:
    score -= 1
if latest_MACD > latest_signal:
    score += 1
else:
    score -= 1
if latest_rsi > 50:
    score += 1
else:
    score -= 1
if score >= 3:
    decision = "BULLISH"
elif score <= -3:
    decision = "BEARISH"
else:
    decision = "NEUTRAL"
    '''INDICATORS'''
history["SMA20"] = SMA20
history["EMA20"] = EMA20
history["RSI"] = rsi
history["MACD"] = MACD
history["Signal"] = signal
history["upper_band"] = upper_band
history["lower_band"] = lower_band
# =========================
# CHART
# =========================

fig, ax = plt.subplots(figsize=(12, 6))

line, = ax.plot(history.index, history.Close)

# Blue cursor dot
selected_point, = ax.plot(
    [], [], "o", color="blue", markersize=8
)

# Price + percentage label
price_text = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(0, 10),
    textcoords="offset points",
    ha="center"
)


""""mouse movement"""

def on_move(event):
    if event.inaxes != ax:
        return

    x_values = mdates.date2num(history.index)
    y_values = history.Close.to_numpy()

    x = event.xdata

    if x < x_values[0] or x > x_values[-1]:
        return


    y = np.interp(x, x_values, y_values)


    percentage = (y - y_values[0]) / y_values[0] * 100


    selected_point.set_data([x], [y])


    price_text.xy = (x, y)
    price_text.set_text(
        f"${y:.2f}\n{percentage:+.2f}%"
    )

    fig.canvas.draw_idle()


fig.canvas.mpl_connect(
    "motion_notify_event",
    on_move
)


ax.set_title(f"{ticker} Stock Price")
ax.set_xlabel("Date")
ax.set_ylabel("Price")

ax.xaxis.set_major_locator(
    mdates.AutoDateLocator()
)

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%d %b")
)

plt.xticks(rotation=45)

plt.tight_layout()


buttons = [
    ("24H", "24H"),
    ("7D", "7d"),
    ("15D", "15d"),
    ("1M", "1mo"),
    ("3M", "3mo"),
    ("6M", "6mo"),
    ("1Y", "1y"),
    ("5Y", "5y"),
    ("10Y", "10y")
]


button_objects = []


def change_period(period):
    global history, selected_point, price_text

    if period == "24H":
        history = stock.history(
            period="1d",
            interval="5m"
        )
    else:
        history = stock.history(
            period=period
        )

    if history.empty:
        return

    ax.clear()

    ax.plot(
        history.index,
        history.Close
    )

    selected_point, = ax.plot(
        [],
        [],
        "o",
        color="blue",
        markersize=8
    )

    price_text = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

    ax.set_title(f"{ticker} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%d %b")
    )

    fig.canvas.draw_idle()

'''price '''
price_text = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

ax.set_title(f"{ticker} Stock Price")
ax.set_xlabel("Date")
ax.set_ylabel("Price")

ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%d %b")
    )

fig.canvas.draw_idle()


for i, (label, period) in enumerate(buttons):

    ax_button = plt.axes([
        0.02 + i * 0.108,
        0.02,
        0.09,
        0.04
    ])

    button = Button(
        ax_button,
        label
    )

    button.on_clicked(
        lambda event, p=period:
        change_period(p)
    )

    button_objects.append(button)
'''10 day forecast'''

future_return_10d = (
    history["Close"].shift(-2880) / history["Close"] - 1
) * 100

history["future_return_10d"] = future_return_10d

future_high = []
future_low = []

for i in range(len(history)):
    next_10_days = history.iloc[i + 1:i + 2881]

    if len(next_10_days) == 2880:
        future_high.append(next_10_days["High"].max())
        future_low.append(next_10_days["Low"].min())
    else:
        future_high.append(np.nan)
        future_low.append(np.nan)

history["future_high_10d"] = future_high
history["future_low_10d"] = future_low

training_data = history[
    [
        "Close",
        "SMA20",
        "EMA20",
        "RSI",
        "MACD",
        "Signal",
        "upper_band",
        "lower_band",
        "Volume",
        "future_high_10d",
        "future_low_10d"
    ]
].dropna()

print("\nTRAINING DATA")
print("---------------------------------------------------")
print(training_data.tail())
print("---------------------------------------------------")
print("Training rows:", len(training_data))
plt.show()
current_price = history["Close"].iloc[-11]

predicted_low = history["future_low_10d"].dropna().iloc[-11]
predicted_high = history["future_high_10d"].dropna().iloc[-11]

print(
    "\n10-TRADING-DAY FORECAST TARGET"
    "\n---------------------------------------------------"
    f"\nCurrent price : ${current_price:.10f}"
    f"\nPotential low : ${predicted_low:.10f}"
    f"\nPotential high: ${predicted_high:.10f}"
    "\n---------------------------------------------------"
)
print(
    "\nCANDLE ANALYSIS"
    "\n---------------------------------------------------"
    f"\nLatest candle : {candle_direction}"
    f"\nOpen          : ${latest_open:.6f}"
    f"\nHigh          : ${recent_candles['High'].iloc[-1]:.6f}"
    f"\nLow           : ${recent_candles['Low'].iloc[-1]:.6f}"
    f"\nClose         : ${latest_close:.6f}"
    f"\nBody          : ${latest_body:.6f}"
    f"\nUpper wick    : ${latest_upper_wick:.6f}"
    f"\nLower wick    : ${latest_lower_wick:.6f}"
    "\n---------------------------------------------------"
)
print(
    "===================================================" 
    f"\nStock: {ticker}"
    f"\nLatest price: {latest_close:.3f}"
    f"\nMonthly return: {monthly_return:.2f}%"
    f"\n20-Day SMA: {SMA20.iloc[-1]:.2f}"
    f"\n20-Day EMA: {latest_EMA20:.2f}"
    f"\nRSI:{rsi.iloc[-1]:.2f}"
    f"\nRSI Status:{rsi_status}"
    f"\nMACD: {latest_MACD:.2f}"
    f"\nSignal: {latest_signal:.2f}"
    f"\nMACD Status: {macd_status}"
    f"\nSTD20 : {latest_std20:.2f}"
    f"\nBollinger Status:{bollinger_status} "
    f"\nTrend: {trend}"
    f"\nDecision score: {score}"
    f"\nDecision: {decision}"
    "\n==================================================="
)

