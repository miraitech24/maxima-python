#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:55:37 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M5: 熱管理システム設計（文字化け完全対策版）
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

print("=" * 80)
print("VF-AI-04-M5: Thermal Management System Design")
print("=" * 80)

# ============================================================================
# 1. 文字化け対策：フォント設定を完全にリセット
# ============================================================================
print("\n1. Setting up font configuration...")

# すべてのフォント設定をリセット
plt.rcdefaults()

# シンプルな設定（日本語フォントを試さない）
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
    'axes.unicode_minus': False,
    'figure.autolayout': True,
})

print("Using default sans-serif font (no Japanese)")

# ============================================================================
# 2. ファイル確認
# ============================================================================
print("\n2. Checking required files...")

required_files = [
    'VF_AI_04_M4_site_data.csv',
    'VF_AI_04_M4_schedule.csv',
    'VF_AI_04_M4_summary.txt'
]

all_files_exist = True
for file_name in required_files:
    if os.path.exists(file_name):
        print(f"✓ {file_name}")
    else:
        print(f"✗ {file_name} - NOT FOUND")
        all_files_exist = False

if not all_files_exist:
    print("\nERROR: Missing required files")
    sys.exit(1)

# ============================================================================
# 3. データ読み込み
# ============================================================================
print("\n3. Loading data...")

site_data = pd.read_csv('VF_AI_04_M4_site_data.csv')
schedule_data = pd.read_csv('VF_AI_04_M4_schedule.csv')

print(f"Sites: {len(site_data)}")
print(f"Schedule points: {len(schedule_data)}")

# ============================================================================
# 4. 熱管理計算
# ============================================================================
print("\n4. Thermal calculations...")

# パラメータ
power_per_site = 10e12  # 10 TW
heat_per_site = power_per_site * 0.65  # 6.5 TW waste heat

# 溶融塩パラメータ
T_in = 900  # K
T_out = 700  # K
cp = 1550  # J/(kg·K)
density = 1800  # kg/m³

# 流量計算
delta_T = T_in - T_out
mass_flow = heat_per_site / (cp * delta_T)  # kg/s
volume_flow = mass_flow / density  # m³/s

print(f"Heat per site: {heat_per_site/1e12:.2f} TW")
print(f"Mass flow: {mass_flow:.1f} kg/s")
print(f"Volume flow: {volume_flow:.3f} m³/s")

# パイプ設計
velocity = 2.0  # m/s
pipe_area = volume_flow / velocity
pipe_diameter = 2 * np.sqrt(pipe_area / np.pi)

print(f"Pipe diameter: {pipe_diameter:.3f} m ({pipe_diameter*1000:.1f} mm)")

# ============================================================================
# 5. シンプルな可視化（文字化け対策済み）
# ============================================================================
print("\n5. Creating visualizations...")

# 図1: メイン結果
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# グラフ1: 温度プロファイル
positions = ['Inlet', 'Mid', 'Outlet']
temperatures = [T_in, (T_in + T_out)/2, T_out]
ax1.plot(positions, temperatures, 'ro-', linewidth=2, markersize=8)
ax1.set_ylabel('Temperature (K)')
ax1.set_title('Temperature Profile')
ax1.grid(True, alpha=0.3)

# 数値表示
for pos, temp in zip(positions, temperatures):
    ax1.text(pos, temp + 10, f'{temp-273.15:.0f}°C', 
             ha='center', va='bottom', fontsize=10)

# グラフ2: 流量パラメータ
params = ['Mass Flow', 'Volume Flow', 'Pipe Diam']
values = [mass_flow, volume_flow, pipe_diameter]
units = ['kg/s', 'm³/s', 'm']

bars = ax2.bar(params, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax2.set_ylabel('Value')
ax2.set_title('Flow Parameters')
ax2.grid(True, alpha=0.3, axis='y')

# 数値表示
for bar, value, unit in zip(bars, values, units):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height * 1.05,
             f'{value:.2f} {unit}', ha='center', va='bottom')

# グラフ3: 建設スケジュール
years = schedule_data['year']
sites = schedule_data['completed_sites']
total_heat = sites * heat_per_site / 1e12  # TW

ax3.plot(years, total_heat, 'b-', linewidth=2)
ax3.fill_between(years, 0, total_heat, alpha=0.3)
ax3.set_xlabel('Year')
ax3.set_ylabel('Total Waste Heat (TW)')
ax3.set_title('Waste Heat Over Time')
ax3.grid(True, alpha=0.3)

# グラフ4: 熱損失内訳（簡易）
categories = ['Useful\nConversion', 'Pipe\nLosses', 'Other\nLosses']
percentages = [35, 5, 60]  # 仮の値
colors = ['#4ecdc4', '#ff6b6b', '#ffd166']

ax4.pie(percentages, labels=categories, colors=colors, autopct='%1.0f%%')
ax4.set_title('Heat Distribution')

fig1.suptitle('VF-AI-04-M5: Thermal Management System', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('VF_AI_04_M5_main.png', dpi=150, bbox_inches='tight')
print("Saved: VF_AI_04_M5_main.png")

# ============================================================================
# 6. 詳細計算結果
# ============================================================================
print("\n6. Detailed calculations...")

# 熱損失計算
pipe_length = 500000  # 500 km in meters
insulation_thick = 0.5
insulation_k = 0.04
avg_temp = (T_in + T_out) / 2
ambient_temp = 460 + 273.15
temp_diff = avg_temp - ambient_temp

# 熱損失関数
def heat_loss(d, L, dT, t_insul, k_insul):
    D1 = d
    D2 = d + 2 * t_insul
    D_log = (D2 - D1) / np.log(D2/D1)
    R = t_insul / (k_insul * np.pi * D_log * L)
    return dT / R

Q_loss = heat_loss(pipe_diameter, pipe_length, temp_diff, insulation_thick, insulation_k)
loss_percent = (Q_loss / heat_per_site) * 100

print(f"Heat loss per pipe: {Q_loss/1e9:.2f} GW")
print(f"Heat loss percentage: {loss_percent:.2f}%")

# 熱交換器計算
T_cold_in = 350 + 273.15
T_cold_out = 400 + 273.15
delta_T1 = T_in - T_cold_out
delta_T2 = T_out - T_cold_in

if delta_T1 > 0 and delta_T2 > 0:
    LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
else:
    LMTD = (delta_T1 + delta_T2) / 2

U = 1000  # W/(m²·K)
A_required = (heat_per_site * 1.2) / (U * LMTD * 0.8)

print(f"Heat exchanger area: {A_required:.1f} m²")

# ============================================================================
# 7. 詳細グラフ
# ============================================================================
fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(12, 10))

# グラフ5: 熱損失 vs 距離
distances = np.linspace(100, 1000, 20)  # km
losses = []
for dist_km in distances:
    length = dist_km * 1000
    loss = heat_loss(pipe_diameter, length, temp_diff, insulation_thick, insulation_k)
    losses.append((loss / heat_per_site) * 100)

ax5.plot(distances, losses, 'b-', linewidth=2)
ax5.axhline(y=5, color='r', linestyle='--', label='5% limit')
ax5.set_xlabel('Pipe Length (km)')
ax5.set_ylabel('Heat Loss (%)')
ax5.set_title('Heat Loss vs Distance')
ax5.legend()
ax5.grid(True, alpha=0.3)

# グラフ6: 貯蔵システム
storage_hours = 8
storage_energy = heat_per_site * storage_hours * 3600  # J
storage_mass = storage_energy / (cp * delta_T)
storage_volume = storage_mass / density

storage_params = ['Energy', 'Mass', 'Volume']
storage_values = [storage_energy/1e12, storage_mass/1e6, storage_volume]
storage_units = ['TJ', 'Mton', 'm³']

bars = ax6.bar(storage_params, storage_values, color=['#8c564b', '#e377c2', '#7f7f7f'])
ax6.set_ylabel('Value')
ax6.set_title(f'Thermal Storage ({storage_hours}h)')
ax6.grid(True, alpha=0.3, axis='y')

for bar, value, unit in zip(bars, storage_values, storage_units):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2, height * 1.05,
             f'{value:.1f} {unit}', ha='center', va='bottom')

# グラフ7: 年間進捗
ax7.plot(years, sites, 'g-', linewidth=2, label='Sites built')
ax7.plot(years, total_heat, 'b-', linewidth=2, label='Total heat')
ax7.set_xlabel('Year')
ax7.set_ylabel('Count / TW')
ax7.set_title('Construction Progress')
ax7.legend()
ax7.grid(True, alpha=0.3)

# グラフ8: 材料必要量
years_selected = [0, 100, 200, 300]
pipe_material = []
insulation_material = []

for year in years_selected:
    idx = np.argmin(np.abs(years - year))
    n_sites = sites.iloc[idx]
    # 簡易計算: 各拠点から2本のパイプ
    total_length = n_sites * 2 * 500  # km
    pipe_vol = total_length * 1000 * np.pi * (pipe_diameter/2)**2  # m³
    insulation_vol = total_length * 1000 * np.pi * ((pipe_diameter + insulation_thick)**2 - pipe_diameter**2)/4
    
    pipe_material.append(pipe_vol)
    insulation_material.append(insulation_vol)

x = range(len(years_selected))
width = 0.35
ax8.bar(x, pipe_material, width, label='Pipe material', color='#1f77b4')
ax8.bar([i + width for i in x], insulation_material, width, label='Insulation', color='#ff7f0e')
ax8.set_xticks([i + width/2 for i in x])
ax8.set_xticklabels([str(y) for y in years_selected])
ax8.set_xlabel('Year')
ax8.set_ylabel('Volume (m³)')
ax8.set_title('Material Requirements')
ax8.legend()
ax8.grid(True, alpha=0.3, axis='y')

fig2.suptitle('VF-AI-04-M5: Detailed Analysis', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('VF_AI_04_M5_detailed.png', dpi=150, bbox_inches='tight')
print("Saved: VF_AI_04_M5_detailed.png")

# ============================================================================
# 8. 結果出力
# ============================================================================
print("\n7. Saving results...")

# CSV出力
results_df = pd.DataFrame({
    'Parameter': [
        'Heat per site',
        'Molten salt inlet temp',
        'Molten salt outlet temp',
        'Mass flow per site',
        'Volume flow per site',
        'Pipe diameter',
        'Flow velocity',
        'Heat loss percentage',
        'Heat exchanger area',
        'Storage energy',
        'Storage volume',
        'Storage time'
    ],
    'Value': [
        f"{heat_per_site/1e12:.3f}",
        f"{T_in-273.15:.0f}",
        f"{T_out-273.15:.0f}",
        f"{mass_flow:.1f}",
        f"{volume_flow:.3f}",
        f"{pipe_diameter:.3f}",
        f"{velocity:.1f}",
        f"{loss_percent:.2f}",
        f"{A_required:.1f}",
        f"{storage_energy/1e12:.1f}",
        f"{storage_volume:.1f}",
        f"{storage_hours}"
    ],
    'Unit': [
        'TW',
        '°C',
        '°C',
        'kg/s',
        'm³/s',
        'm',
        'm/s',
        '%',
        'm²',
        'TJ',
        'm³',
        'hours'
    ]
})

results_df.to_csv('VF_AI_04_M5_results.csv', index=False)
print("Saved: VF_AI_04_M5_results.csv")

# テキストサマリー
with open('VF_AI_04_M5_summary.txt', 'w') as f:
    f.write("VF-AI-04-M5: Thermal Management System Design\n")
    f.write("="*60 + "\n\n")
    f.write("KEY PARAMETERS:\n")
    f.write(f"Heat per site: {heat_per_site/1e12:.3f} TW\n")
    f.write(f"Mass flow per site: {mass_flow:.1f} kg/s\n")
    f.write(f"Pipe diameter: {pipe_diameter:.3f} m\n")
    f.write(f"Heat loss: {loss_percent:.2f}%\n")
    f.write(f"Heat exchanger area: {A_required:.1f} m²\n")
    f.write(f"Storage volume per site: {storage_volume:.1f} m³\n\n")
    
    f.write("FINAL STATE (300 years):\n")
    f.write(f"Total sites: {sites.iloc[-1]}\n")
    f.write(f"Total waste heat: {total_heat.iloc[-1]:.1f} TW\n")
    f.write(f"Total molten salt flow: {sites.iloc[-1] * mass_flow/1e6:.1f} Mton/s\n\n")
    
    f.write("FILES GENERATED:\n")
    f.write("1. VF_AI_04_M5_main.png - Main results\n")
    f.write("2. VF_AI_04_M5_detailed.png - Detailed analysis\n")
    f.write("3. VF_AI_04_M5_results.csv - Numerical results\n")
    f.write("4. VF_AI_04_M5_summary.txt - This summary\n")

print("Saved: VF_AI_04_M5_summary.txt")

# ============================================================================
# 9. 完了
# ============================================================================
print("\n" + "=" * 80)
print("COMPLETE: VF-AI-04-M5")
print("=" * 80)
print("\nOutput files created:")
print("1. VF_AI_04_M5_main.png")
print("2. VF_AI_04_M5_detailed.png")
print("3. VF_AI_04_M5_results.csv")
print("4. VF_AI_04_M5_summary.txt")
print("\nNext module: VF-AI-04-M6")
print("=" * 80)

plt.show()
