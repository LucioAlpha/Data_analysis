import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# 設置 Matplotlib 字體以支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# --- 處理台灣電力公司數據 ---
# 讀取電力公司 CSV 數據
taipower_data = pd.read_csv('data/台灣電力公司公用售電業售電統計資料.csv')

# 確保數據類型正確
taipower_data['年份'] = pd.to_numeric(taipower_data['年份'], errors='coerce').astype(int)
taipower_data['平均單價合計(元)'] = pd.to_numeric(taipower_data['平均單價合計(元)'], errors='coerce')
taipower_data = taipower_data.dropna()

# 繪製折線圖：電力平均單價趨勢
plt.figure(figsize=(12, 6))
plt.plot(taipower_data['年份'], taipower_data['平均單價合計(元)'], marker='o', color='#3B82F6', linewidth=2, markersize=6)

# 在關鍵點添加數值標籤（例如 1974、1981、2014、2024）
key_years = [1974, 1981, 2014, 2024]
for year in key_years:
    price = taipower_data[taipower_data['年份'] == year]['平均單價合計(元)'].iloc[0]
    plt.text(year, price + 0.1, f'{price:.2f}', ha='center', va='bottom', fontsize=10)

plt.title('台灣電力公司平均售電單價趨勢 (1951-2024)', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('平均單價 (元/度)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(taipower_data['年份'][::5], rotation=45)  # 每 5 年顯示一次年份
plt.tight_layout()
plt.savefig('taipower_price_trend.png')
plt.show()

# 電力數據摘要
print("\n=== 台灣電力公司售電單價摘要 ===")
print("本分析基於 1951 年至 2024 年台灣電力公司公用售電業平均單價數據。")
print("關鍵發現：")
print("- 單價從 1951 年的 0.16 元/度上升至 2024 年的 3.48 元/度，增長約 22 倍。")
print("- 1974 年（1.03 元）和 1981 年（2.74 元）出現顯著跳升，可能與油價危機相關。")
print("- 1980-1986 年價格高位波動，1981 年達 2.74 元；2014 年後再次上升，2024 年達 3.48 元。")
print("- 2000-2010 年價格穩定在 2.0-2.6 元，近年（2022-2024）快速上升。")

# 電力數據結論
print("\n=== 台灣電力公司售電單價結論 ===")
print("電力單價在 1951-2024 年間呈長期上升趨勢，1974 年和 1981 年因能源危機大幅上漲。")
print("2000-2010 年價格相對穩定，2022-2024 年快速上升至 3.48 元/度，可能與燃料成本或政策調整相關。")
print("建議進一步分析能源成本、發電結構和電價補貼政策的影響。")

plt.clf()

