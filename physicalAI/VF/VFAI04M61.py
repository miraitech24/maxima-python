#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:44:13 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M6: 材料・建設計画
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.font_manager as fm

print("=" * 80)
print("VF-AI-04-M6: 材料・建設計画")
print("=" * 80)

# 1. フォント自動検出
print("\n1. フォント設定中...")

def find_japanese_font():
    """日本語フォントを検索"""
    jp_fonts = []
    for font in fm.fontManager.ttflist:
        name_lower = font.name.lower()
        # 日本語フォントのキーワード
        keywords = ['ipa', 'ms', 'meiryo', 'yu', 'hiragino', 'osaka', 'sazanami', 'mplus']
        if any(keyword in name_lower for keyword in keywords):
            jp_fonts.append(font.name)
    
    return jp_fonts[0] if jp_fonts else None

# フォント検出
japanese_font = find_japanese_font()
if japanese_font:
    plt.rcParams['font.family'] = japanese_font
    print(f"✓ 日本語フォントを使用: {japanese_font}")
    use_japanese = True
else:
    plt.rcParams['font.family'] = 'sans-serif'
    print("⚠️ 日本語フォントなし。英語を使用")
    use_japanese = False

plt.rcParams['axes.unicode_minus'] = False

# 2. ファイル確認
print("\n2. ファイル確認...")
files_needed = ['VF_AI_04_M5_results.csv', 'VF_AI_04_M4_schedule.csv']
for f in files_needed:
    if os.path.exists(f):
        print(f"✓ {f}")
    else:
        print(f"✗ {f}")
        exit(1)

# 3. データ読み込み
print("\n3. データ読み込み...")
m5 = pd.read_csv('VF_AI_04_M5_results.csv')
schedule = pd.read_csv('VF_AI_04_M4_schedule.csv')

# 4. パラメータ抽出
print("\n4. パラメータ抽出...")
params = {}
for _, row in m5.iterrows():
    try:
        val = float(row['Value'])
        if 'TW' in row['Unit']:
            val *= 1e12
        params[row['Parameter'].lower()] = val
    except:
        continue

pipe_dia = params.get('pipe diameter', 0.5)
storage_vol = params.get('storage volume', 500)
n_sites = 865

# 5. 計算
print("\n5. 計算実行...")

# 材料計算
steel_total = n_sites * 500000  # kg
concrete_total = n_sites * 10000  # m³
insulation_total = n_sites * 1000  # m³
salt_total = n_sites * storage_vol  # m³

# コスト計算
steel_cost = (steel_total/1000) * 800
concrete_cost = concrete_total * 120
insulation_cost = insulation_total * 3000
salt_cost = (salt_total*1800/1000) * 5000

material_cost = steel_cost + concrete_cost + insulation_cost + salt_cost
construction_cost = material_cost * 2
total_cost = material_cost + construction_cost
cost_per_site = total_cost / n_sites

# 6. 可視化（フォントに応じてラベル変更）
print("\n6. 可視化作成...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# タイトル設定
if use_japanese:
    fig.suptitle('VF-AI-04-M6: 材料・建設計画', fontsize=16, y=1.02)
else:
    fig.suptitle('VF-AI-04-M6: Material Planning', fontsize=16, y=1.02)

# グラフ1: 材料必要量
ax = axes[0, 0]
if use_japanese:
    materials = ['鋼材', 'コンクリート', '断熱材', '溶融塩']
    ylabel = '量'
    title = '総材料必要量'
else:
    materials = ['Steel', 'Concrete', 'Insulation', 'Salt']
    ylabel = 'Quantity'
    title = 'Total Materials'

values = [
    steel_total/1e9,
    concrete_total/1e6,
    insulation_total/1e6,
    salt_total/1e6
]
units = ['Gkg', 'Mm³', 'Mm³', 'Mm³']

bars = ax.bar(materials, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax.set_ylabel(ylabel)
ax.set_title(title)
ax.grid(True, alpha=0.3, axis='y')

for bar, val, unit in zip(bars, values, units):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
            f'{val:.1f} {unit}', ha='center', va='bottom', fontsize=9)

# グラフ2: コスト内訳
ax = axes[0, 1]
if use_japanese:
    costs = ['材料費', '建設費']
    title = 'コスト内訳'
else:
    costs = ['Materials', 'Construction']
    title = 'Cost Breakdown'

cost_vals = [material_cost/1e9, construction_cost/1e9]
colors = ['#1f77b4', '#ff7f0e']

wedges, texts, autotexts = ax.pie(cost_vals, labels=costs, colors=colors,
                                  autopct='%1.1f%%', startangle=90)
ax.set_title(title)

# グラフ3: 建設進捗
ax = axes[1, 0]
years = schedule['year']
sites = schedule['completed_sites']

ax.plot(years, sites, 'b-', linewidth=2)
ax.fill_between(years, 0, sites, alpha=0.3, color='blue')

if use_japanese:
    ax.set_xlabel('年')
    ax.set_ylabel('拠点数')
    ax.set_title('建設進捗')
else:
    ax.set_xlabel('Year')
    ax.set_ylabel('Sites')
    ax.set_title('Construction Progress')

ax.grid(True, alpha=0.3)

# グラフ4: 鋼材必要量の推移
ax = axes[1, 1]
# 簡易な時系列計算
steel_over_time = []
for s in sites:
    if s > 0:
        steel_over_time.append(s * 500000 / 1e9)  # Gkg

if len(steel_over_time) > 0:
    plot_years = years[:len(steel_over_time)]
    ax.plot(plot_years, steel_over_time, 'r-', linewidth=2)
    ax.fill_between(plot_years, 0, steel_over_time, alpha=0.3, color='red')
    
    if use_japanese:
        ax.set_xlabel('年')
        ax.set_ylabel('鋼材必要量 (Gkg)')
        ax.set_title('鋼材必要量の推移')
    else:
        ax.set_xlabel('Year')
        ax.set_ylabel('Steel Required (Gkg)')
        ax.set_title('Steel Requirements')
    
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('VF_AI_04_M6_results.png', dpi=150, bbox_inches='tight')
print("✓ グラフ保存: VF_AI_04_M6_results.png")

# 7. 結果出力（日本語/英語）
print("\n7. 結果出力...")

if use_japanese:
    # 日本語出力
    with open('VF_AI_04_M6_summary.txt', 'w', encoding='utf-8') as f:
        f.write("VF-AI-04-M6: 材料・建設計画 結果サマリー\n")
        f.write("="*60 + "\n\n")
        
        f.write("基本情報:\n")
        f.write(f"総拠点数: {n_sites} 拠点\n")
        f.write(f"建設期間: {years.max()} 年\n\n")
        
        f.write("材料必要量:\n")
        f.write(f"鋼材: {steel_total/1e9:.2f} Gkg\n")
        f.write(f"コンクリート: {concrete_total/1e6:.2f} Mm³\n")
        f.write(f"断熱材: {insulation_total/1e6:.2f} Mm³\n")
        f.write(f"溶融塩: {salt_total/1e6:.2f} Mm³\n\n")
        
        f.write("建設コスト:\n")
        f.write(f"材料費: ${material_cost/1e9:.2f}B\n")
        f.write(f"建設費: ${construction_cost/1e9:.2f}B\n")
        f.write(f"総コスト: ${total_cost/1e9:.2f}B\n")
        f.write(f"1拠点あたり: ${cost_per_site/1e6:.2f}M\n")
else:
    # 英語出力
    with open('VF_AI_04_M6_summary.txt', 'w') as f:
        f.write("VF-AI-04-M6: Material Planning Summary\n")
        f.write("="*60 + "\n\n")
        
        f.write("Project Overview:\n")
        f.write(f"Total sites: {n_sites}\n")
        f.write(f"Construction period: {years.max()} years\n\n")
        
        f.write("Material Requirements:\n")
        f.write(f"Steel: {steel_total/1e9:.2f} Gkg\n")
        f.write(f"Concrete: {concrete_total/1e6:.2f} Mm³\n")
        f.write(f"Insulation: {insulation_total/1e6:.2f} Mm³\n")
        f.write(f"Molten salt: {salt_total/1e6:.2f} Mm³\n\n")
        
        f.write("Construction Costs:\n")
        f.write(f"Material cost: ${material_cost/1e9:.2f}B\n")
        f.write(f"Construction cost: ${construction_cost/1e9:.2f}B\n")
        f.write(f"Total cost: ${total_cost/1e9:.2f}B\n")
        f.write(f"Cost per site: ${cost_per_site/1e6:.2f}M\n")

print("✓ サマリー保存: VF_AI_04_M6_summary.txt")

# 8. 完了
print("\n" + "=" * 80)
if use_japanese:
    print("✅ VF-AI-04-M6 完了")
else:
    print("✅ VF-AI-04-M6 COMPLETE")

print("=" * 80)
print("\n出力ファイル:")
print("1. VF_AI_04_M6_results.png")
print("2. VF_AI_04_M6_summary.txt")
print("\n次のステップ: VF-AI-04-M7")
print("=" * 80)

plt.show()
