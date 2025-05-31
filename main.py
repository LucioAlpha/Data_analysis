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

# 按年份聚合全台平均價格
yearly_avg = data.groupby(data['date'].dt.year)['price'].mean().reset_index()
yearly_avg.columns = ['year', 'price']

# 2024 年各縣市平均價格
city_avg_2024 = data[data['date'].dt.year == 2024].groupby('city')['price'].mean().reset_index()
city_avg_2024 = city_avg_2024.sort_values('price', ascending=False)

# 離島與本島價格比較
island_cities = ['澎湖縣', '金門縣', '連江縣']
mainland_cities = ['臺北市', '臺中市', '高雄市']
island_mainland = data[data['city'].isin(island_cities + mainland_cities)].copy()
island_mainland['region'] = island_mainland['city'].apply(lambda x: '離島' if x in island_cities else '本島')
island_mainland_avg = island_mainland.groupby([island_mainland['date'].dt.year, 'region'])['price'].mean().unstack().reset_index()
island_mainland_avg = island_mainland_avg.dropna()

# 繪製面積圖：離島與本島價格比較
plt.figure(figsize=(10, 6))
plt.fill_between(island_mainland_avg['date'], island_mainland_avg['離島'], label='離島', color='#EF4444', alpha=0.6)
plt.fill_between(island_mainland_avg['date'], island_mainland_avg['本島'], label='本島', color='#3B82F6', alpha=0.6)
plt.title('離島與本島價格比較 (2011-2025)', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('平均價格 (元)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('island_vs_mainland.png')
plt.show()