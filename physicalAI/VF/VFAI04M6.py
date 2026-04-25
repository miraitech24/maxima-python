#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:00:52 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M6: 材料・建設計画（日本語/英語自動切替版）
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

print("=" * 80)
print("VF-AI-04-M6: 材料・建設計画")
print("=" * 80)

# 1. フォント自動検出と設定
print("\n1. フォント設定...")

def setup_fonts():
    """日本語フォントを検索、なければ英語フォントを使用"""
    
    # 試す日本語フォントのリスト
    japanese_fonts = [
        'IPAexGothic', 'IPAGothic', 'IPAPGothic',
        'MS Gothic', 'Yu Gothic', 'Meiryo',
        'Hiragino Sans', 'Noto Sans CJK JP'
    ]
    
    # 現在のフォントリストを取得
    available_fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
    
    # 日本語フォントを探す
    selected_font = None
    for font in japanese_fonts:
        if font in available_fonts:
            selected_font = font
            print(f"✓ 日本語フォント発見: {font}")
            break
    
    if selected_font:
        # 日本語フォント設定
        plt.rcParams.update({
            'font.family': selected_font,
            'font.size': 11,
            'axes.unicode_minus': False,
            'figure.autolayout': True,
        })
        return True  # 日本語モード
    else:
        # 英語フォント設定
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': 11,
            'figure.autolayout': True,
        })
        print("⚠️ 日本語フォントなし。英語で表示します。")
        return False  # 英語モード

# フォント設定
USE_JAPANESE = setup_fonts()

# 2. ファイル確認
print("\n2. ファイル確認...")
files = ['VF_AI_04_M5_results.csv', 'VF_AI_04_M4_schedule.csv']
for f in files:
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

# 6. 可視化（言語自動切替）
print("\n6. 可視化作成...")

# 言語に応じたテキスト設定
if USE_JAPANESE:
    TEXT = {
        'title': 'VF-AI-04-M6: 材料・建設計画',
        'materials': ['鋼材', 'コンクリート', '断熱材', '溶融塩'],
        'quantity': '量',
        'materials_title': '総材料必要量',
        'costs': ['材料費', '建設費'],
        'cost_title': 'コスト内訳',
        'year': '年',
        'sites': '拠点数',
        'progress_title': '建設進捗',
        'steel_title': '鋼材必要量の推移',
        'steel_label': '鋼材必要量 (Gkg)'
    }
else:
    TEXT = {
        'title': 'VF-AI-04-M6: Material Planning',
        'materials': ['Steel', 'Concrete', 'Insulation', 'Molten Salt'],
        'quantity': 'Quantity',
        'materials_title': 'Total Material Requirements',
        'costs': ['Materials', 'Construction'],
        'cost_title': 'Cost Breakdown',
        'year': 'Year',
        'sites': 'Sites',
        'progress_title': 'Construction Progress',
        'steel_title': 'Steel Requirements Over Time',
        'steel_label': 'Steel Required (Gkg)'
    }

# 図の作成
fig = plt.figure(figsize=(14, 10))
fig.suptitle(TEXT['title'], fontsize=16, y=0.98)

# サブプロット配置
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# グラフ1: 材料必要量
ax1 = fig.add_subplot(gs[0, 0])
values = [
    steel_total/1e9,
    concrete_total/1e6,
    insulation_total/1e6,
    salt_total/1e6
]
units = ['Gkg', 'Mm³', 'Mm³', 'Mm³'] if USE_JAPANESE else ['Gkg', 'Mm³', 'Mm³', 'Mm³']

bars = ax1.bar(TEXT['materials'], values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], 
               alpha=0.8, edgecolor='black', linewidth=0.5)
ax1.set_ylabel(TEXT['quantity'], fontsize=12, labelpad=10)
ax1.set_title(TEXT['materials_title'], fontsize=13, pad=15)
ax1.grid(True, alpha=0.3, axis='y', linestyle='--')

# 数値表示
for bar, val, unit in zip(bars, values, units):
    height = bar.get_height()
    if height > max(values) * 0.1:
        ax1.text(bar.get_x() + bar.get_width()/2, height * 1.02,
                f'{val:.1f}\n{unit}', ha='center', va='bottom', 
                fontsize=9, linespacing=0.8)
    else:
        ax1.text(bar.get_x() + bar.get_width()/2, height/2,
                f'{val:.1f}\n{unit}', ha='center', va='center', 
                fontsize=9, linespacing=0.8, color='white')

# グラフ2: コスト内訳
ax2 = fig.add_subplot(gs[0, 1])
cost_vals = [material_cost/1e9, construction_cost/1e9]
colors = ['#1f77b4', '#ff7f0e']

wedges, texts, autotexts = ax2.pie(cost_vals, labels=TEXT['costs'], colors=colors,
                                   autopct='%1.1f%%', startangle=90,
                                   textprops={'fontsize': 10})
ax2.set_title(TEXT['cost_title'], fontsize=13, pad=15)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')

# グラフ3: 建設進捗
ax3 = fig.add_subplot(gs[1, 0])
years = schedule['year']
sites = schedule['completed_sites']

ax3.plot(years, sites, 'b-', linewidth=2.5, marker='o', markersize=4,
         markerfacecolor='white', markeredgecolor='blue', markeredgewidth=1)
ax3.fill_between(years, 0, sites, alpha=0.2, color='blue')
ax3.set_xlabel(TEXT['year'], fontsize=12, labelpad=10)
ax3.set_ylabel(TEXT['sites'], fontsize=12, labelpad=10)
ax3.set_title(TEXT['progress_title'], fontsize=13, pad=15)
ax3.grid(True, alpha=0.3, linestyle='--')

# 目盛り設定
ax3.set_xticks(np.arange(0, 301, 50))
ax3.set_yticks(np.arange(0, 901, 100))

# グラフ4: 鋼材必要量の推移
ax4 = fig.add_subplot(gs[1, 1])
steel_over_time = []
for s in sites:
    if s > 0:
        steel_over_time.append(s * 500000 / 1e9)  # Gkg

if len(steel_over_time) > 0:
    plot_years = years[:len(steel_over_time)]
    ax4.plot(plot_years, steel_over_time, 'r-', linewidth=2.5, marker='s',
             markersize=4, markerfacecolor='white', markeredgecolor='red',
             markeredgewidth=1)
    ax4.fill_between(plot_years, 0, steel_over_time, alpha=0.2, color='red')
    ax4.set_xlabel(TEXT['year'], fontsize=12, labelpad=10)
    ax4.set_ylabel(TEXT['steel_label'], fontsize=12, labelpad=10)
    ax4.set_title(TEXT['steel_title'], fontsize=13, pad=15)
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    ax4.set_xticks(np.arange(0, 301, 50))

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_filename = 'VF_AI_04_M6_final.png'
plt.savefig(output_filename, dpi=150, bbox_inches='tight')
print(f"✓ グラフ保存: {output_filename}")

# 7. 結果出力（言語自動切替）
print("\n7. 結果出力...")

if USE_JAPANESE:
    with open('VF_AI_04_M6_summary.txt', 'w', encoding='utf-8') as f:
        f.write("VF-AI-04-M6: 材料・建設計画 結果サマリー\n")
        f.write("="*60 + "\n\n")
        f.write(f"総拠点数: {n_sites} 拠点\n")
        f.write(f"建設期間: {years.max()} 年\n")
        f.write(f"鋼材: {steel_total/1e9:.2f} Gkg\n")
        f.write(f"コンクリート: {concrete_total/1e6:.2f} Mm³\n")
        f.write(f"断熱材: {insulation_total/1e6:.2f} Mm³\n")
        f.write(f"溶融塩: {salt_total/1e6:.2f} Mm³\n")
        f.write(f"総コスト: ${total_cost/1e9:.2f}B\n")
else:
    with open('VF_AI_04_M6_summary.txt', 'w') as f:
        f.write("VF-AI-04-M6: Material Planning Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total sites: {n_sites}\n")
        f.write(f"Construction period: {years.max()} years\n")
        f.write(f"Steel: {steel_total/1e9:.2f} Gkg\n")
        f.write(f"Concrete: {concrete_total/1e6:.2f} Mm³\n")
        f.write(f"Insulation: {insulation_total/1e6:.2f} Mm³\n")
        f.write(f"Molten salt: {salt_total/1e6:.2f} Mm³\n")
        f.write(f"Total cost: ${total_cost/1e9:.2f}B\n")

print("✓ サマリー保存: VF_AI_04_M6_summary.txt")

# 8. 完了
print("\n" + "=" * 80)
if USE_JAPANESE:
    print("✅ VF-AI-04-M6 完了")
else:
    print("✅ VF-AI-04-M6 COMPLETE")
print("=" * 80)
print(f"\n使用フォント: {'日本語' if USE_JAPANESE else '英語'}")
print("\n生成ファイル:")
print(f"1. {output_filename}")
print("2. VF_AI_04_M6_summary.txt")
print("3. VF_AI_04_M6_results.csv")
print("\n次のステップ: VF-AI-04-M7")
print("=" * 80)

plt.show()
