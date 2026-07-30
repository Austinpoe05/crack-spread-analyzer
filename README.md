# 3-2-1 Crack Spread Analyzer
A Python tool for analyzing refinery crack spread margins using real futures market data.

## What is the 3-2-1 Crack Spread?
The 3-2-1 crack spread measures the theoretical profit margin 
a refiner earns by converting 3 barrels of crude oil into 
2 barrels of gasoline (RBOB) and 1 barrel of diesel (ULSD). 
It is a key indicator of refinery profitability and a widely 
followed metric in energy trading.

## What This Tool Does
- Pulls real historical futures price data for WTI Crude, RBOB Gasoline, 
  and ULSD Heating Oil using yfinance
- Calculates the daily 3-2-1 crack spread (2022-2024)
- Computes a 30-day rolling average to identify margin trends
- Classifies each day as Strong, Normal, or Weak margin environment
  using standard deviation thresholds
- Outputs a summary of current and historical spread statistics
- Visualizes the crack spread and underlying commodity prices in a 
  two-panel chart

## Libraries Used
- yfinance
- pandas
- matplotlib
