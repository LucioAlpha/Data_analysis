import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

# 設置 Matplotlib 字體以支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 讀取 CSV 數據
data = pd.read_csv('data/各縣市家用桶裝瓦斯均價.csv')

# 清理欄位名稱
data.columns = [col.strip().replace('"', '') for col in data.columns]
data = data.rename(columns={
    '縣市名稱': 'city',
    '查報均價(元/20公斤(桶))': 'price',
    '查報日期(年/月)': 'date'
})

# 轉換數據類型
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['date'] = pd.to_datetime(data['date'], format='%Y%m', errors='coerce')
data = data.dropna()

# 定義區域
regions = {
    '北部': ['臺北市', '新北市', '基隆市', '桃園市', '新竹市', '新竹縣', '宜蘭縣'],
    '中部': ['臺中市', '苗栗縣', '彰化縣', '南投縣'],
    '南部': ['高雄市', '臺南市', '嘉義市', '嘉義縣', '屏東縣'],
    '東部': ['花蓮縣', '臺東縣'],
    '離島': ['澎湖縣', '金門縣', '連江縣']
}

# 將縣市映射到區域
data['region'] = data['city'].apply(lambda x: next((r for r, cities in regions.items() if x in cities), None))
data = data.dropna(subset=['region'])

# 按年份和區域聚合數據
yearly_region_avg = data.groupby([data['date'].dt.year, 'region'])['price'].mean().unstack().reset_index()
yearly_region_avg = yearly_region_avg.rename(columns={'date': 'year'})
yearly_region_avg = yearly_region_avg.fillna(0)  # 填充缺失值以確保圖表完整

# 獲取年份和區域
years = yearly_region_avg['year']
regions_list = ['北部', '中部', '南部', '東部', '離島']

# 繪製分組長條圖
plt.figure(figsize=(15, 8))
bar_width = 0.15
x = np.arange(len(years))
colors = ['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6']

for i, region in enumerate(regions_list):
    plt.bar(x + i * bar_width, yearly_region_avg[region], width=bar_width, label=region, color=colors[i])
    # 添加數值標籤（簡化為整數）
    for j, val in enumerate(yearly_region_avg[region]):
        if val > 0:  # 僅顯示非零值
            plt.text(x[j] + i * bar_width, val + 5, f'{int(val)}', ha='center', va='bottom', fontsize=8)

plt.title('2011-2025 年各區域平均瓦斯價格', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('平均價格 (元/20公斤)', fontsize=12)
plt.xticks(x + bar_width * 2, years, rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.tight_layout()
plt.savefig('region_avg_price_all_years.png')
plt.show()