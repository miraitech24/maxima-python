#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:09:33 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M4: 反応器ネットワーク最適化
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

print("=" * 80)
print("VF-AI-04-M4: 反応器ネットワーク最適化")
print("=" * 80)

# ============================================================================
# 1. ファイル読み込み
# ============================================================================
print("\n1. ファイル読み込み中...")

# 現在のディレクトリを確認
current_dir = os.getcwd()
print(f"現在のディレクトリ: {current_dir}")

# ディレクトリ内のファイルをリストアップ
print("ディレクトリ内のファイル:")
for f in os.listdir(current_dir):
    print(f"  - {f}")

# VF-AI-04-M3の出力ファイルを探す
m3_files = [f for f in os.listdir(current_dir) if 'M3' in f and f.endswith('.csv')]
print(f"\n見つかったM3ファイル: {m3_files}")

if m3_files:
    # 最初に見つかったM3ファイルを読み込む
    m3_file = m3_files[0]
    try:
        df_m3 = pd.read_csv(m3_file)
        print(f"✓ ファイル読み込み成功: {m3_file}")
        print(f"  データ形状: {df_m3.shape}")
        print(f"  カラム: {list(df_m3.columns)}")
        
        # データの確認
        print("\nデータの先頭:")
        print(df_m3.head())
        
        # 水素需要量の計算
        if 'H2SO4_ppm' in df_m3.columns:
            n_total = 4.8e20 / 43.45e-3
            initial_H2SO4 = df_m3['H2SO4_ppm'].iloc[0]
            final_H2SO4 = df_m3['H2SO4_ppm'].iloc[-1]
            H2SO4_consumed = (initial_H2SO4 - final_H2SO4) * 1e-6 * n_total
            H2_demand_total = 3 * H2SO4_consumed
            print(f"\n計算された水素需要量: {H2_demand_total:.2e} mol")
        else:
            H2_demand_total = 2.73e18
            print(f"\nH2SO4_ppmカラムなし。デフォルト値: {H2_demand_total:.2e} mol")
            
    except Exception as e:
        print(f"✗ ファイル読み込みエラー: {e}")
        H2_demand_total = 2.73e18
        df_m3 = None
else:
    print("✗ M3ファイルが見つかりません")
    H2_demand_total = 2.73e18
    df_m3 = None

# ============================================================================
# 2. 設定
# ============================================================================
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 3. 金星パラメータ
# ============================================================================
print("\n2. 金星パラメータ設定中...")

R_venus = 6051.8e3
N_sites = 865

print(f"金星半径: {R_venus/1e3:.1f} km")
print(f"総拠点数: {N_sites}")
print(f"水素需要量: {H2_demand_total:.2e} mol")

# ============================================================================
# 4. 拠点配置生成
# ============================================================================
print("\n3. 拠点配置生成中...")

np.random.seed(42)
n_points = N_sites

# 球面上の一様分布
phi = np.random.uniform(0, 2*np.pi, n_points)
costheta = np.random.uniform(-1, 1, n_points)
theta = np.arccos(costheta)

# 緯度経度変換
latitudes = 90 - np.degrees(theta)
longitudes = np.degrees(phi)

print(f"{n_points}拠点生成完了")
print(f"緯度範囲: {latitudes.min():.1f}° 〜 {latitudes.max():.1f}°")
print(f"経度範囲: {longitudes.min():.1f}° 〜 {longitudes.max():.1f}°")

# ============================================================================
# 5. ネットワーク分析
# ============================================================================
print("\n4. ネットワーク分析中...")

# 距離計算（サンプル）
distances = []
for i in range(100):
    for j in range(i+1, 100):
        lat1, lon1 = np.radians(latitudes[i]), np.radians(longitudes[i])
        lat2, lon2 = np.radians(latitudes[j]), np.radians(longitudes[j])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        distances.append(R_venus * c / 1000)

avg_distance = np.mean(distances)
print(f"平均距離（100拠点サンプル）: {avg_distance:.1f} km")

# ============================================================================
# 6. 建設スケジュール
# ============================================================================
print("\n5. 建設スケジュール作成中...")

construction_years = 300
years = np.arange(0, construction_years + 1, 10)

# ロジスティック成長
def logistic_growth(t, K=N_sites, r=0.05, t0=50):
    return K / (1 + np.exp(-r * (t - t0)))

completed_sites = logistic_growth(years)
completed_sites = np.minimum(completed_sites, N_sites)
completed_sites = np.round(completed_sites).astype(int)

print("建設スケジュール:")
for i in range(0, len(years), 5):
    print(f"  年 {years[i]:3.0f}: {completed_sites[i]:4d} 拠点 ({completed_sites[i]/N_sites*100:.1f}%)")

# ============================================================================
# 7. 可視化
# ============================================================================
print("\n6. 結果を可視化中...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('VF-AI-04-M4: 反応器ネットワーク最適化', fontsize=16, y=1.02)

# グラフ1: 拠点配置
ax = axes[0, 0]
scatter = ax.scatter(longitudes, latitudes, s=10, alpha=0.5, c='blue')
ax.set_xlabel('経度 [度]')
ax.set_ylabel('緯度 [度]')
ax.set_title('金星表面の拠点配置')
ax.grid(True, alpha=0.3)

# グラフ2: 距離分布
ax = axes[0, 1]
ax.hist(distances, bins=30, alpha=0.7, color='green', edgecolor='black')
ax.axvline(x=avg_distance, color='red', linestyle='--', linewidth=2, 
           label=f'平均: {avg_distance:.1f} km')
ax.set_xlabel('拠点間距離 [km]')
ax.set_ylabel('頻度')
ax.set_title('拠点間距離分布（100拠点サンプル）')
ax.legend()
ax.grid(True, alpha=0.3)

# グラフ3: 建設スケジュール
ax = axes[1, 0]
ax.plot(years, completed_sites, 'b-', linewidth=2, label='完成拠点数')
ax.fill_between(years, 0, completed_sites, alpha=0.3)
ax.axhline(y=N_sites, color='r', linestyle='--', alpha=0.5, label='目標(865拠点)')
ax.set_xlabel('建設年数 [年]')
ax.set_ylabel('完成拠点数')
ax.set_title('建設スケジュール')
ax.legend()
ax.grid(True, alpha=0.3)

# グラフ4: 水素供給能力
ax = axes[1, 1]
H2_production_rate = 1.0e6  # mol/s
H2_capacity = completed_sites * H2_production_rate * 365.25 * 24 * 3600
H2_required = H2_demand_total * (years / construction_years)

ax.plot(years, H2_capacity / 1e18, 'g-', linewidth=2, label='供給能力')
ax.plot(years, H2_required / 1e18, 'r-', linewidth=2, label='必要量')
ax.fill_between(years, H2_required / 1e18, H2_capacity / 1e18, 
                where=(H2_capacity >= H2_required), 
                alpha=0.3, color='green', label='供給余剰')
ax.set_xlabel('建設年数 [年]')
ax.set_ylabel('水素量 [Emol]')
ax.set_title('水素供給能力の進展')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('VF_AI_04_M4_results.png', dpi=150, bbox_inches='tight')
print("✓ グラフ保存: VF_AI_04_M4_results.png")

# ============================================================================
# 8. 結果出力
# ============================================================================
print("\n7. 結果ファイル出力中...")

# 拠点データ
site_data = pd.DataFrame({
    'site_id': range(n_points),
    'longitude_deg': longitudes,
    'latitude_deg': latitudes,
})
site_data.to_csv('VF_AI_04_M4_site_data.csv', index=False)
print("✓ 拠点データ保存: VF_AI_04_M4_site_data.csv")

# 建設スケジュール
schedule_data = pd.DataFrame({
    'year': years,
    'completed_sites': completed_sites,
    'H2_capacity_mol_per_year': H2_capacity,
    'H2_required_mol_per_year': H2_required,
})
schedule_data.to_csv('VF_AI_04_M4_schedule.csv', index=False)
print("✓ 建設スケジュール保存: VF_AI_04_M4_schedule.csv")

# サマリー
with open('VF_AI_04_M4_summary.txt', 'w', encoding='utf-8') as f:
    f.write("VF-AI-04-M4: 反応器ネットワーク最適化 結果サマリー\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"入力ファイル: {m3_file if m3_files else 'なし'}\n")
    f.write(f"水素需要量: {H2_demand_total:.2e} mol\n")
    f.write(f"総拠点数: {N_sites}\n")
    f.write(f"平均拠点間距離: {avg_distance:.1f} km\n")
    f.write(f"建設期間: {construction_years} 年\n")
    f.write(f"最終完成拠点数: {completed_sites[-1]}\n\n")
    
    f.write("建設マイルストーン:\n")
    milestones = [0, 50, 100, 150, 200, 250, 300]
    for year in milestones:
        idx = np.argmin(np.abs(years - year))
        f.write(f"  年 {year}: {completed_sites[idx]} 拠点 ({completed_sites[idx]/N_sites*100:.1f}%)\n")
    
    f.write("\n水素供給分析:\n")
    final_capacity = H2_capacity[-1]
    annual_requirement = H2_required[-1]
    if final_capacity >= annual_requirement:
        surplus = final_capacity - annual_requirement
        f.write(f"  供給余剰: {surplus/1e18:.2f} Emol/年\n")
    else:
        deficit = annual_requirement - final_capacity
        f.write(f"  供給不足: {deficit/1e18:.2f} Emol/年\n")

print("✓ サマリー保存: VF_AI_04_M4_summary.txt")

# ============================================================================
# 9. 完了
# ============================================================================
print("\n" + "=" * 80)
print("✅ VF-AI-04-M4 計算完了！")
print("=" * 80)
print("\n生成ファイル:")
print("1. VF_AI_04_M4_results.png - 可視化結果")
print("2. VF_AI_04_M4_site_data.csv - 拠点データ")
print("3. VF_AI_04_M4_schedule.csv - 建設スケジュール")
print("4. VF_AI_04_M4_summary.txt - 結果サマリー")
print("\n次のステップ: VF-AI-04-M5")
print("=" * 80)

plt.show()
