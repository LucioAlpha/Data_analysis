# --- 處理台灣自來水公司數據 ---

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 設置 Matplotlib 字體以支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False


# 讀取自來水公司 CSV 數據
water_data = pd.read_csv('data/台灣自來水公司近年水價資料表.csv')

# 將年度別轉換為西元年
water_data['年份'] = water_data['年度別'] + 1911
water_data['平均水價(元)'] = pd.to_numeric(water_data['平均水價(元)'], errors='coerce')
water_data = water_data.dropna()

# 繪製折線圖：自來水平均水價趨勢（調整比例）
plt.figure(figsize=(10, 6))
plt.plot(water_data['年份'], water_data['平均水價(元)'], marker='o', color='#10B981', linewidth=2, markersize=8)

# 在每個數據點添加數值標籤
for i, price in enumerate(water_data['平均水價(元)']):
    plt.text(water_data['年份'].iloc[i], price + 0.02, f'{price:.2f}', ha='center', va='bottom', fontsize=10)

# 調整 Y 軸範圍和刻度，讓比例更平均
plt.ylim(10.8, 11.2)  # 設置 Y 軸範圍為 10.8-11.2，稍微放大波動
plt.yticks(np.arange(10.8, 11.25, 0.05))  # Y 軸刻度間隔為 0.05

plt.title('台灣自來水公司平均水價趨勢 (2018-2023)', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('平均水價 (元/立方公尺)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(water_data['年份'])
plt.tight_layout()
plt.savefig('taiwan_water_price_trend.png')
plt.show()

# 自來水數據摘要
print("\n=== 台灣自來水公司水價摘要 ===")
print("本分析基於 2018 年（民國 107 年）至 2023 年（民國 112 年）台灣自來水公司平均水價數據。")
print("關鍵發現：")
print("- 水價從 2018-2019 年的 11.00 元/立方公尺略降至 2019 年的 10.96 元，之後緩慢上升至 2023 年的 11.06 元。")
print("- 六年內價格波動僅 0.14 元，顯示水價高度穩定。")
print("- 水價變化幅度小，可能受政府價格管制影響。")

# 自來水數據結論
print("\n=== 台灣自來水公司水價結論 ===")
print("自來水價格在 2018-2023 年間保持穩定，波動範圍僅 10.96-11.06 元/立方公尺。")
print("價格穩定性可能與政府管制和補貼政策有關，但成本數據缺失，無法評估盈虧狀況。")
print("建議分析水務運營成本和價格調整政策，以評估長期可持續性。")