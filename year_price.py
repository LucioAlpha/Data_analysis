import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# 設置 Matplotlib 字體以支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 讀取 CSV 數據
data = pd.read_csv('data/全國家用桶裝瓦斯均價.csv')

# 確保數據類型正確
data['年份'] = pd.to_numeric(data['年份'], errors='coerce').astype(int)
data['價格'] = pd.to_numeric(data['價格'], errors='coerce')
data = data.dropna()

# 繪製折線圖：全台年度平均價格趨勢
plt.figure(figsize=(12, 6))
plt.plot(data['年份'], data['價格'], marker='o', color='#3B82F6', linewidth=2, markersize=8)

# 在每個數據點添加數值標籤（整數）
for i, price in enumerate(data['價格']):
    plt.text(data['年份'].iloc[i], price + 10, f'{int(price)}', ha='center', va='bottom', fontsize=10)

plt.title('全台年度平均瓦斯價格趨勢 (2003-2024)', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('平均價格 (元/20公斤)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(data['年份'], rotation=45)
plt.tight_layout()
plt.savefig('national_avg_price_trend.png')
plt.show()