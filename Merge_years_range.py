import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

# 設置 Matplotlib 字體以支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 定義數據路徑
DATA_PATH = 'data/'

# 函數：清理並處理瓦斯價格數據
def process_gas_data(file_name):
    data = pd.read_csv(f'{DATA_PATH}{file_name}')
    data.columns = [col.strip().replace('"', '') for col in data.columns]
    data = data.rename(columns={
        '縣市名稱': 'city',
        '查報均價(元/20公斤(桶))': 'price',
        '查報日期(年/月)': 'date'
    })
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['date'] = pd.to_datetime(data['date'], format='%Y%m', errors='coerce')
    return data.dropna()

# 函數：處理全台瓦斯價格數據
def process_national_gas_data(file_name):
    data = pd.read_csv(f'{DATA_PATH}{file_name}')
    data['年份'] = pd.to_numeric(data['年份'], errors='coerce').astype(int)
    data['價格'] = pd.to_numeric(data['價格'], errors='coerce')
    return data.dropna()

# 函數：處理電力數據
def process_power_data(file_name):
    data = pd.read_csv(f'{DATA_PATH}{file_name}')
    data['年份'] = pd.to_numeric(data['年份'], errors='coerce').astype(int)
    data['平均單價合計(元)'] = pd.to_numeric(data['平均單價合計(元)'], errors='coerce')
    return data.dropna()

# 函數：處理水價數據
def process_water_data(file_name):
    data = pd.read_csv(f'{DATA_PATH}{file_name}')
    data['年份'] = data['年度別'] + 1911
    data['平均水價(元)'] = pd.to_numeric(data['平均水價(元)'], errors='coerce')
    return data.dropna()

# 圖表 1: 離島與本島價格比較（面積圖，2018-2023）
def plot_island_vs_mainland_2018_2023():
    gas_data = process_gas_data('各縣市家用桶裝瓦斯均價.csv')
    gas_data = gas_data[(gas_data['date'].dt.year >= 2018) & (gas_data['date'].dt.year <= 2023)]
    island_cities = ['澎湖縣', '金門縣', '連江縣']
    mainland_cities = ['臺北市', '臺中市', '高雄市']
    island_mainland = gas_data[gas_data['city'].isin(island_cities + mainland_cities)].copy()
    island_mainland['region'] = island_mainland['city'].apply(lambda x: '離島' if x in island_cities else '本島')
    island_mainland_avg = island_mainland.groupby([island_mainland['date'].dt.year, 'region'])['price'].mean().unstack().reset_index()
    island_mainland_avg = island_mainland_avg.dropna()

    plt.figure(figsize=(10, 6))
    plt.fill_between(island_mainland_avg['date'], island_mainland_avg['離島'], label='離島', color='#EF4444', alpha=0.6)
    plt.fill_between(island_mainland_avg['date'], island_mainland_avg['本島'], label='本島', color='#3B82F6', alpha=0.6)
    plt.title('離島與本島價格比較 (2018-2023)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('平均價格 (元)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(island_mainland_avg['date'])
    plt.tight_layout()
    plt.savefig('imgs/2018_2023_imgs/island_vs_mainland_2018_2023.png')
    plt.close()

# 圖表 2: 各區域瓦斯價格趨勢（折線圖，2018-2023）
def plot_region_monthly_trend_2018_2023():
    gas_data = process_gas_data('各縣市家用桶裝瓦斯均價.csv')
    gas_data = gas_data[(gas_data['date'].dt.year >= 2018) & (gas_data['date'].dt.year <= 2023)]
    regions = {
        '北部': ['臺北市', '新北市', '基隆市', '桃園市', '新竹市', '新竹縣', '宜蘭縣'],
        '中部': ['臺中市', '苗栗縣', '彰化縣', '南投縣'],
        '南部': ['高雄市', '臺南市', '嘉義市', '嘉義縣', '屏東縣'],
        '東部': ['花蓮縣', '臺東縣'],
        '離島': ['澎湖縣', '金門縣', '連江縣']
    }
    gas_data['region'] = gas_data['city'].apply(lambda x: next((r for r, cities in regions.items() if x in cities), None))
    gas_data = gas_data.dropna(subset=['region'])
    monthly_region_data = gas_data.groupby(['region', gas_data['date'].dt.to_period('M')])['price'].mean().reset_index()
    monthly_region_data['date'] = monthly_region_data['date'].dt.to_timestamp()

    plt.figure(figsize=(12, 6))
    colors = ['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6']
    for i, region in enumerate(['北部', '中部', '南部', '東部', '離島']):
        region_data = monthly_region_data[monthly_region_data['region'] == region]
        plt.plot(region_data['date'], region_data['price'], label=region, color=colors[i], linewidth=2)
    plt.title('各區域每月瓦斯價格趨勢 (2018-2023)', fontsize=14)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('價格 (元/20公斤)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('imgs/2018_2023_imgs/region_monthly_price_trend_2018_2023.png')
    plt.close()

# 圖表 3: 全台年度平均瓦斯價格趨勢（折線圖，2018-2023）
def plot_yearly_gas_trend_2018_2023():
    gas_data = process_national_gas_data('全國家用桶裝瓦斯均價.csv')
    gas_data = gas_data[(gas_data['年份'] >= 2018) & (gas_data['年份'] <= 2023)]
    plt.figure(figsize=(12, 6))
    plt.plot(gas_data['年份'], gas_data['價格'], marker='o', color='#3B82F6', linewidth=2, markersize=8)
    for i, price in enumerate(gas_data['價格']):
        plt.text(gas_data['年份'].iloc[i], price + 10, f'{int(price)}', ha='center', va='bottom', fontsize=10)
    plt.title('全台年度平均瓦斯價格趨勢 (2018-2023)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('平均價格 (元/20公斤)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(gas_data['年份'])
    plt.tight_layout()
    plt.savefig('imgs/2018_2023_imgs/national_avg_price_trend_2018_2023.png')
    plt.close()

# 圖表 4: 台灣電力公司售電單價趨勢（折線圖，2018-2023）
def plot_power_trend_2018_2023():
    power_data = process_power_data('台灣電力公司公用售電業售電統計資料.csv')
    power_data = power_data[(power_data['年份'] >= 2018) & (power_data['年份'] <= 2023)]
    plt.figure(figsize=(12, 6))
    plt.plot(power_data['年份'], power_data['平均單價合計(元)'], marker='o', color='#3B82F6', linewidth=2, markersize=6)
    key_years = [2018, 2020, 2023]
    for year in key_years:
        price = power_data[power_data['年份'] == year]['平均單價合計(元)'].iloc[0]
        plt.text(year, price + 0.05, f'{price:.2f}', ha='center', va='bottom', fontsize=10)
    plt.title('台灣電力公司平均售電單價趨勢 (2018-2023)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('平均單價 (元/度)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(power_data['年份'])
    plt.tight_layout()
    plt.savefig('imgs/2018_2023_imgs/taipower_price_trend_2018_2023.png')
    plt.close()


# 圖表 5: 台灣自來水公司平均水價趨勢（折線圖，2018-2023）
def plot_water_trend_2018_2023():
    water_data = process_water_data('台灣自來水公司近年水價資料表.csv')
    plt.figure(figsize=(10, 6))
    plt.plot(water_data['年份'], water_data['平均水價(元)'], marker='o', color='#10B981', linewidth=2, markersize=8)
    for i, price in enumerate(water_data['平均水價(元)']):
        plt.text(water_data['年份'].iloc[i], price + 0.02, f'{price:.2f}', ha='center', va='bottom', fontsize=10)
    plt.ylim(10.8, 11.2)
    plt.yticks(np.arange(10.8, 11.25, 0.05))
    plt.title('台灣自來水公司平均水價趨勢 (2018-2023)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('平均水價 (元/立方公尺)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(water_data['年份'])
    plt.tight_layout()
    plt.savefig('imgs/2018_2023_imgs/taiwan_water_price_trend_2018_2023.png')
    plt.close()


# 主程式：執行 2018-2023 年區間圖表生成
if __name__ == "__main__":
    plot_island_vs_mainland_2018_2023()
    plot_region_monthly_trend_2018_2023()
    plot_yearly_gas_trend_2018_2023()
    plot_power_trend_2018_2023()
    plot_water_trend_2018_2023()
    print("2018-2023 年區間圖表已生成並保存至當前目錄。")