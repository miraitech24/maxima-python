#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:41:45 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M3: 全球化学収支シミュレーション（最終版）
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

print("=" * 60)
print("VF-AI-04-M3: 全球化学収支シミュレーション")
print("=" * 60)

# ============================================================================
# 1. シンプルな設定
# ============================================================================
print("\n1. 設定中...")

# 化学式をプレーンテキストで表示（下付き文字なし）
chem_names = {
    'H2SO4': 'H2SO4',
    'H2O': 'H2O',
    'SO2': 'SO2',
    'O2': 'O2',
    'H2': 'H2',
    'S': 'S'
}

# 日本語フォント設定（シンプルに）
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['axes.unicode_minus'] = False

print("   ✓ 設定完了")

# ============================================================================
# 2. 物理定数と初期条件
# ============================================================================
print("\n2. 物理定数と初期条件を設定中...")

R = 8.314462618
M_atm = 4.8e20
M_avg = 43.45e-3
n_total = M_atm / M_avg

print(f"   金星大気総物質量: {n_total:.2e} mol")

initial_ppm = {
    'H2SO4': 150.0,
    'H2O': 30.0,
    'SO2': 150.0,
    'O2': 0.1,
    'H2': 0.0,
    'S': 0.0
}

initial_moles = {}
for species, ppm in initial_ppm.items():
    initial_moles[species] = n_total * ppm * 1e-6
    print(f"   初期 {chem_names[species]}: {initial_moles[species]:.2e} mol ({ppm} ppm)")

# ============================================================================
# 3. 反応パラメータ
# ============================================================================
print("\n3. 反応パラメータを設定中...")

print(f"   対象反応: H2SO4 + 3H2 → 4H2O + S")

def k2(T):
    A2 = 5.0e10
    Ea2 = 90.0e3
    return A2 * np.exp(-Ea2 / (R * T))

T_sim = 750.0
k2_val = k2(T_sim)
print(f"   反応速度定数 k2({T_sim}K) = {k2_val:.2e} 1/s")

v_H2_per_site = 1.0e6
N_sites = 865
v_H2_total = v_H2_per_site * N_sites
print(f"   水素供給速度: {v_H2_total:.2e} mol/s")

# ============================================================================
# 4. 平衡計算
# ============================================================================
print("\n4. 平衡計算を実行中...")

years = 300
total_seconds = years * 365.25 * 24 * 3600
total_H2_supplied = v_H2_total * total_seconds

available_H2SO4 = initial_moles['H2SO4']
H2_needed_for_all_H2SO4 = 3 * available_H2SO4

if total_H2_supplied >= H2_needed_for_all_H2SO4:
    H2SO4_consumed = available_H2SO4
    H2_consumed = 3 * H2SO4_consumed
    H2_remaining = total_H2_supplied - H2_consumed
    print(f"   ✓ H2が十分: H2SO4が制限反応物")
else:
    H2_consumed = total_H2_supplied
    H2SO4_consumed = H2_consumed / 3
    H2_remaining = 0
    print(f"   ⚠️ H2不足: H2が制限反応物")

H2SO4_final = available_H2SO4 - H2SO4_consumed
H2O_final = initial_moles['H2O'] + 4 * H2SO4_consumed
S_final = initial_moles['S'] + H2SO4_consumed

print(f"\n   【収支計算結果】")
print(f"   消費 H2SO4: {H2SO4_consumed:.2e} mol")
print(f"   消費 H2: {H2_consumed:.2e} mol")
print(f"   残存 H2SO4: {H2SO4_final:.2e} mol")
print(f"   生成 H2O: {H2O_final:.2e} mol")
print(f"   生成 S: {S_final:.2e} mol")

conversion_rate = (H2SO4_consumed / available_H2SO4) * 100
H2_utilization = (H2_consumed / total_H2_supplied) * 100

print(f"\n   【効率指標】")
print(f"   H2SO4反応率: {conversion_rate:.1f}%")
print(f"   H2利用率: {H2_utilization:.1f}%")

# ============================================================================
# 5. 時系列データ生成
# ============================================================================
print("\n5. 時系列データを生成中...")

t_years = np.array([0, 0.1, 1, 10, 50, 100, 200, 300])
t_seconds = t_years * 365.25 * 24 * 3600
progress = np.minimum(t_seconds / total_seconds, 1.0)

H2SO4_series = available_H2SO4 * (1 - progress)
H2O_series = initial_moles['H2O'] + 4 * available_H2SO4 * progress
H2_series = np.minimum(v_H2_total * 3600, v_H2_total * t_seconds)
S_series = available_H2SO4 * progress

def moles_to_ppm(moles):
    return (moles / n_total) * 1e6

H2SO4_ppm = moles_to_ppm(H2SO4_series)
H2O_ppm = moles_to_ppm(H2O_series)
H2_ppm = moles_to_ppm(H2_series)

# ============================================================================
# 6. 可視化（シンプル版）
# ============================================================================
print("\n6. グラフを生成中...")

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# タイトル
fig.suptitle('VF-AI-04-M3: 金星硫酸還元反応の化学収支', fontsize=16, y=1.02)

# グラフ1: 主要化学種の濃度変化
ax = axes[0, 0]
ax.plot(t_years, H2SO4_ppm, 'r-', linewidth=2, label='H2SO4')
ax.plot(t_years, H2O_ppm, 'b-', linewidth=2, label='H2O')
ax.set_xlabel('時間 [年]')
ax.set_ylabel('濃度 [ppm]')
ax.set_title('H2SO4とH2Oの濃度変化')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_yscale('log')

# グラフ2: 水素濃度
ax = axes[0, 1]
ax.plot(t_years, H2_ppm, 'g-', linewidth=2, label='H2')
ax.set_xlabel('時間 [年]')
ax.set_ylabel('濃度 [ppm]')
ax.set_title('H2濃度変化')
ax.grid(True, alpha=0.3)
ax.legend()

# グラフ3: 反応進行率
ax = axes[1, 0]
conversion_percent = progress * conversion_rate
ax.plot(t_years, conversion_percent, 'purple', linewidth=2)
ax.axhline(y=99, color='red', linestyle='--', alpha=0.5, label='99%完了')
ax.set_xlabel('時間 [年]')
ax.set_ylabel('反応進行率 [%]')
ax.set_title('H2SO4還元反応の進行率')
ax.grid(True, alpha=0.3)
ax.legend()

# グラフ4: 物質収支
ax = axes[1, 1]
species = ['H2SO4消費', 'H2O生成', 'S生成']
values = [H2SO4_consumed/n_total*1e6,
          (H2O_final - initial_moles['H2O'])/n_total*1e6,
          S_final/n_total*1e6]

colors = ['#FF6B6B', '#4ECDC4', '#FFD166']
bars = ax.bar(species, values, color=colors)
ax.set_ylabel('濃度変化 [ppm]')
ax.set_title('300年後の物質収支')
ax.grid(True, alpha=0.3, axis='y')

for bar, value in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{value:.1f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('VF_AI_04_M3_results.png', dpi=150, bbox_inches='tight')
print("   ✓ グラフを保存: VF_AI_04_M3_results.png")

# ============================================================================
# 7. 詳細分析
# ============================================================================
print("\n7. 詳細分析を実行中...")

H2O_mass = (H2O_final - initial_moles['H2O']) * 18.015e-3
H2O_volume = H2O_mass / 1000
earth_ocean_volume = 1.332e9
comparison = H2O_volume / earth_ocean_volume * 100

print(f"\n   【H2O生成量の詳細】")
print(f"   生成水量: {H2O_mass/1e12:.1f} 兆kg")
print(f"   体積換算: {H2O_volume/1e9:.3f} km³")
print(f"   地球の海の {comparison:.6f}% に相当")

S_mass = S_final * 32.06e-3
print(f"\n   【S生成量】")
print(f"   生成硫黄: {S_mass/1e12:.1f} 兆kg")

# ============================================================================
# 8. ファイル出力
# ============================================================================
print("\n8. 結果ファイルを出力中...")

df = pd.DataFrame({
    'time_years': t_years,
    'H2SO4_ppm': H2SO4_ppm,
    'H2O_ppm': H2O_ppm,
    'H2_ppm': H2_ppm,
    'S_moles': S_series,
    'conversion_%': conversion_percent
})
df.to_csv('VF_AI_04_M3_data.csv', index=False)
print("   ✓ データを保存: VF_AI_04_M3_data.csv")

with open('VF_AI_04_M3_summary.txt', 'w', encoding='utf-8') as f:
    f.write("VF-AI-04-M3: 全球化学収支シミュレーション 結果サマリー\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("1. シミュレーション条件:\n")
    f.write(f"   期間: {years} 年\n")
    f.write(f"   温度: {T_sim} K\n")
    f.write(f"   水素供給速度: {v_H2_total:.2e} mol/s\n")
    f.write(f"   総拠点数: {N_sites}\n\n")
    
    f.write("2. 反応式:\n")
    f.write(f"   H2SO4 + 3H2 → 4H2O + S\n\n")
    
    f.write("3. 主要結果:\n")
    f.write(f"   H2SO4反応率: {conversion_rate:.1f}%\n")
    f.write(f"   H2利用率: {H2_utilization:.1f}%\n")
    f.write(f"   生成水量: {H2O_mass/1e12:.1f} 兆kg\n")
    f.write(f"   生成硫黄: {S_mass/1e12:.1f} 兆kg\n\n")
    
    f.write("4. 最終濃度 [ppm]:\n")
    f.write(f"   H2SO4: {moles_to_ppm(H2SO4_final):.2e}\n")
    f.write(f"   H2O: {moles_to_ppm(H2O_final):.2e}\n")
    f.write(f"   H2: {moles_to_ppm(H2_remaining):.2e}\n\n")
    
    f.write("5. 次のモジュールへの入力:\n")
    f.write("   - VF_AI_04_M3_data.csv\n")
    f.write("   - 水素需要量: {:.2e} mol\n".format(H2_consumed))

print("   ✓ サマリーを保存: VF_AI_04_M3_summary.txt")

# ============================================================================
# 9. 完了
# ============================================================================
print("\n" + "=" * 60)
print("✅ VF-AI-04-M3 計算完了！")
print("=" * 60)
print("\n生成されたファイル:")
print("  1. VF_AI_04_M3_results.png - 結果グラフ")
print("  2. VF_AI_04_M3_data.csv - 時系列データ")
print("  3. VF_AI_04_M3_summary.txt - サマリーファイル")
print("\n【次のステップ】")
print("VF-AI-04-M4: 反応器ネットワーク最適化")
print("=" * 60)

plt.show()
