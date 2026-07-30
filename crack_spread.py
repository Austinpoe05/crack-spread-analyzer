import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

wti = yf.download('CL=F', start='2022-01-01', end='2024-12-31')
rbob = yf.download('RB=F', start='2022-01-01', end='2024-12-31')
ulsd = yf.download('HO=F', start='2022-01-01', end='2024-12-31')

wti_close = wti['Close'].squeeze()
rbob_close = rbob['Close'].squeeze()
ulsd_close = ulsd['Close'].squeeze()

prices = pd.DataFrame({
    'WTI': wti_close,
    'RBOB': rbob_close,
    'ULSD': ulsd_close
}).dropna()

prices['RBOB_barrel'] = prices['RBOB'] * 42
prices['ULSD_barrel'] = prices['ULSD'] * 42
prices['crack_spread'] = (2 * prices['RBOB_barrel'] + prices['ULSD_barrel'] - 3 * prices['WTI']) / 3

prices['crack_spread_30d_avg'] = prices['crack_spread'].rolling(window=30).mean()

mean_spread = prices['crack_spread'].mean()
std_spread = prices['crack_spread'].std()

def classify_margin(spread, mean, std):
    if spread > mean + std:
        return 'Strong Margin'
    elif spread < mean - std:
        return 'Weak Margin'
    else:
        return 'Normal Margin'

prices['margin_environment'] = prices['crack_spread'].apply(
    lambda x: classify_margin(x, mean_spread, std_spread)
)

print(prices['margin_environment'].value_counts())

current_spread = prices['crack_spread'].iloc[-1]
current_environment = prices['margin_environment'].iloc[-1]
max_spread = prices['crack_spread'].max()
min_spread = prices['crack_spread'].min()

print('=== Crack Spread Summary ===')
print(f'Current Spread: ${current_spread:.2f}/barrel')
print(f'Current Environment: {current_environment}')
print(f'Historical Average: ${mean_spread:.2f}/barrel')
print(f'Historical High: ${max_spread:.2f}/barrel')
print(f'Historical Low: ${min_spread:.2f}/barrel')

fig, axes = plt.subplots(2, 1, figsize=(12, 12))

axes[0].plot(prices.index, prices['crack_spread'], color='lightcoral', alpha=0.5, label='Daily Crack Spread')
axes[0].plot(prices.index, prices['crack_spread_30d_avg'], color='darkred', linewidth=2, label='30-Day Average')
axes[0].set_title('3-2-1 Crack Spread (2022-2024)')
axes[0].set_ylabel('Crack Spread ($/barrel)')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(prices.index, prices['WTI'], label='WTI Crude', color='black')
axes[1].plot(prices.index, prices['RBOB'] * 42, label='RBOB (per barrel)', color='green')
axes[1].plot(prices.index, prices['ULSD'] * 42, label='ULSD (per barrel)', color='blue')
axes[1].set_title('Underlying Commodity Prices')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Price ($/barrel)')
axes[1].legend()
axes[1].grid(True)

fig.tight_layout(pad=3.0)
plt.show()