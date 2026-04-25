#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:36:00 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M6: 材料・建設計画 (Plotly版 - PNG保存なし)
"""

import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("=" * 80)
print("VF-AI-04-M6: 材料・建設計画 (Plotly版)")
print("=" * 80)

# 1. ファイル確認
print("\n1. ファイル確認...")
files = ['VF_AI_04_M5_results.csv', 'VF_AI_04_M4_schedule.csv']
for f in files:
    if os.path.exists(f):
        print(f"✓ {f}")
    else:
        print(f"✗ {f}")
        exit(1)

# 2. データ読み込み
print("\n2. データ読み込み...")
m5 = pd.read_csv('VF_AI_04_M5_results.csv')
schedule = pd.read_csv('VF_AI_04_M4_schedule.csv')

# 3. パラメータ抽出
print("\n3. パラメータ抽出...")
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

# 4. 計算
print("\n4. 計算実行...")

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

# 5. Plotlyで可視化
print("\n5. Plotlyで可視化作成...")

# サブプロット作成
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('総材料必要量', 'コスト内訳', '建設進捗', '鋼材必要量の推移'),
    specs=[[{'type': 'bar'}, {'type': 'pie'}],
           [{'type': 'scatter'}, {'type': 'scatter'}]]
)

# グラフ1: 材料必要量（棒グラフ）
materials = ['鋼材', 'コンクリート', '断熱材', '溶融塩']
values = [steel_total/1e9, concrete_total/1e6, insulation_total/1e6, salt_total/1e6]
units = ['Gkg', 'Mm³', 'Mm³', 'Mm³']

fig.add_trace(
    go.Bar(
        x=materials,
        y=values,
        text=[f'{v:.1f} {u}' for v, u in zip(values, units)],
        textposition='auto',
        marker_color=['blue', 'red', 'green', 'orange'],
        name='材料必要量'
    ),
    row=1, col=1
)

fig.update_xaxes(title_text="材料種類", row=1, col=1)
fig.update_yaxes(title_text="量", row=1, col=1)

# グラフ2: コスト内訳（円グラフ）
costs = ['材料費', '建設費']
cost_vals = [material_cost/1e9, construction_cost/1e9]

fig.add_trace(
    go.Pie(
        labels=costs,
        values=cost_vals,
        textinfo='percent+label',
        marker_colors=['blue', 'orange'],
        name='コスト内訳'
    ),
    row=1, col=2
)

# グラフ3: 建設進捗（折れ線グラフ）
years = schedule['year']
sites = schedule['completed_sites']

fig.add_trace(
    go.Scatter(
        x=years,
        y=sites,
        mode='lines+markers',
        line=dict(color='blue', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 255, 0.2)',
        name='建設進捗'
    ),
    row=2, col=1
)

fig.update_xaxes(title_text="年", row=2, col=1)
fig.update_yaxes(title_text="拠点数", row=2, col=1)

# グラフ4: 鋼材必要量の推移
steel_over_time = []
for s in sites:
    if s > 0:
        steel_over_time.append(s * 500000 / 1e9)  # Gkg

if len(steel_over_time) > 0:
    plot_years = years[:len(steel_over_time)]
    
    fig.add_trace(
        go.Scatter(
            x=plot_years,
            y=steel_over_time,
            mode='lines+markers',
            line=dict(color='red', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.2)',
            name='鋼材必要量'
        ),
        row=2, col=2
    )

fig.update_xaxes(title_text="年", row=2, col=2)
fig.update_yaxes(title_text="鋼材必要量 (Gkg)", row=2, col=2)

# レイアウト設定
fig.update_layout(
    title_text='VF-AI-04-M6: 材料・建設計画',
    title_font_size=20,
    showlegend=True,
    height=800,
    width=1200,
    margin=dict(l=50, r=50, t=100, b=50),
)

# HTMLとして保存（PNG保存はスキップ）
fig.write_html('VF_AI_04_M6_plotly.html')
print("✓ HTML保存: VF_AI_04_M6_plotly.html")

# PNG保存を試みるが、エラーならスキップ
try:
    fig.write_image('VF_AI_04_M6_plotly.png')
    print("✓ PNG保存: VF_AI_04_M6_plotly.png")
except Exception as e:
    print(f"⚠️ PNG保存エラー: {e}")
    print("   HTMLファイルのみ生成します")

# 6. 結果出力
print("\n6. 結果出力...")

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

print("✓ サマリー保存: VF_AI_04_M6_summary.txt")

# 7. 完了
print("\n" + "=" * 80)
print("✅ VF-AI-04-M6 (Plotly版) 完了")
print("=" * 80)
print("\n出力ファイル:")
print("1. VF_AI_04_M6_plotly.html - インタラクティブグラフ（ブラウザで開けます）")
print("2. VF_AI_04_M6_summary.txt - サマリー")
print("\nHTMLファイルをブラウザで開くには:")
print("   firefox VF_AI_04_M6_plotly.html")
print("   または chrome VF_AI_04_M6_plotly.html")
print("\n次のステップ: VF-AI-04-M7")
print("=" * 80)

# ブラウザで表示（オプション）
try:
    fig.show()
except:
    print("\nグラフを表示できませんでした。VF_AI_04_M6_plotly.htmlをブラウザで開いてください。")
