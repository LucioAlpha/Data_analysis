import pandas as pd
import matplotlib.pyplot as plt
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

# 按區域和月份聚合數據
monthly_region_data = data.groupby(['region', data['date'].dt.to_period('M')])['price'].mean().reset_index()
monthly_region_data['date'] = monthly_region_data['date'].dt.to_timestamp()

# 繪製折線圖：各區域每月價格趨勢
plt.figure(figsize=(12, 6))
colors = ['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6']
for i, region in enumerate(['北部', '中部', '南部', '東部', '離島']):
    region_data = monthly_region_data[monthly_region_data['region'] == region]
    plt.plot(region_data['date'], region_data['price'], label=region, color=colors[i], linewidth=2)

plt.title('各區域每月瓦斯價格趨勢 (2011-2025)', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('價格 (元/20公斤)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('region_monthly_price_trend.png')
plt.show()