# 📊 Finance Chart Engine (Python)

A lightweight financial charting engine built in Python using Matplotlib.  
Supports Kagi-style price visualization, interactive chart controls, and extensible data pipelines.

---

## 🚀 Features

- Kagi chart generation from market data
- Step-based price normalization
- Swing detection + color-state logic
- Interactive Matplotlib chart:
  - zoom (mouse + keyboard)
  - pan (left/right)
  - crosshair tracking
- Date-aware x-axis formatting
- Modular design for adding new chart types (candlesticks, etc.)

---

## 🧠 Core Concept

Data flows through a simple transformation pipeline:
Yahoo Data → Step Normalization → Kagi Reduction → Chart Rendering

Kagi logic focuses on:
- trend direction shifts
- local swing filtering
- noise reduction via step rounding

---

## 📦 Project Structure
```python
chart_engine/  
├── data_scraping/
│ └── data.py
├── charts/
│ └── kagi.py
└── main scripts
```
---

## ▶️ Example Usage

```python
from chart_engine.data_scraping.data import YahooData
from chart_engine.charts.kagi import Kagi

btc = YahooData.get_yahoo_closes("BTC-USD", 2000)

rounded = Kagi.get_steps_rounded_coordinates(btc, 500)
kagi_data = Kagi.get_kagi_coordinates(rounded)

fig, ax = plt.subplots(figsize=(12, 6))
Kagi.plot_kagi_chart(ax, kagi_data)

plt.show()
```
## 🖱 Controls

- Mouse wheel → zoom
- Left / Right arrows → pan
- Shift + arrows → zoom Y-axis
- Ctrl + arrows → zoom X-axis
- r → reset view
- Mouse move → crosshair

## 🛠 Dependencies
- matplotlib
- numpy
- pandas (optional, for future OHLC support)
- yfinance or custom YahooData loader

## 📌 Roadmap
- Candlestick chart module
- Tkinter UI integration
- Unified chart switcher (Kagi / Candles)
- Real OHLC data pipeline
- Strategy + signal layer
