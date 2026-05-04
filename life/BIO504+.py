#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 11:06:47 2026

@author: iwamura
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIO-504: 宇宙環境耐性遺伝子発現率 分析プログラム
超シンプルMatplotlibプロンプト準拠 (200行以内)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# 1. 日本語フォント自動検出 (超シンプル)
try:
    plt.rcParams['font.family'] = 'IPAexGothic'
    plt.rcParams['axes.unicode_minus'] = False
    use_japanese = True
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'
    use_japanese = False

# 2. ファイル読み込み
def load_maxima_results(filename='bio504_for_python.txt'):
    if not os.path.exists(filename):
        print(f"❌ エラー: {filename} なし")
        print("先に実行: maxima -b bio504.mac")
        sys.exit(1)
    
    data = {}
    gene_effects = []
    optimizations = []
    in_gene = False
    in_opt = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('gene_effects'):
                in_gene = True
                in_opt = False
                continue
            if line.startswith('optimization'):
                in_opt = True
                in_gene = False
                continue
            if in_gene:
                parts = line.split(',')
                if len(parts) == 3:
                    gene_effects.append((parts[0], float(parts[1]), float(parts[2])))
            elif in_opt:
                parts = line.split(',')
                if len(parts) == 2:
                    optimizations.append((parts[0], float(parts[1])))
            else:
                if '=' in line:
                    key, val = line.split('=', 1)
                    data[key.strip()] = val.strip()
    return data, gene_effects, optimizations

# 3. グラフ描画
def create_graphs(data, gene_effects, optimizations, filename='BIO504_results.png'):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('宇宙環境耐性遺伝子発現分析' if use_japanese else 'Space Environmental Tolerance Gene Expression Analysis',
                 fontsize=14, fontweight='bold')

    # グラフ1: 総合生存確率 (棒グラフ)
    ax1 = axes[0, 0]
    categories = ['Radiation', 'Microgravity', 'Metabolic', 'Total']
    values = []
    for cat in categories[:3]:
        val = 0
        for g in gene_effects:
            if g[0].startswith(cat):
                val = g[2] if g[1] > 0 else g[1]
        values.append(val)
    values.append(float(data.get('P_total', 0)))
    colors = ['#ff6b6b', '#48dbfb', '#ff9ff3', '#54a0ff']
    bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Probability' if not use_japanese else '確率')
    ax1.set_title('Total Survival Probability' if not use_japanese else '総合生存確率')
    ax1.set_ylim(0, 1)
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=10)

    # グラフ2: 遺伝子発現成功率
    ax2 = axes[0, 1]
    labels = []
    success_vals = []
    for g in gene_effects:
        label = g[0].replace('_',' ')
        labels.append(label)
        success_vals.append(g[2])
    x = np.arange(len(labels))
    bars2 = ax2.bar(x, success_vals, color='#2ed573', edgecolor='black', linewidth=1.2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Success Rate' if not use_japanese else '成功率')
    ax2.set_title('Gene Expression Success Rate' if not use_japanese else '遺伝子発現成功率')
    ax2.set_ylim(0, 1.2)
    for bar, val in zip(bars2, success_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=9)

    # グラフ3: 最適化比較
    ax3 = axes[1, 0]
    opt_names = [o[0] for o in optimizations]
    opt_vals = [o[1] for o in optimizations]
    colors_opt = ['#eccc68', '#ffa502', '#ff6348', '#2ed573']
    bars3 = ax3.bar(opt_names, opt_vals, color=colors_opt, edgecolor='black', linewidth=1.2)
    ax3.set_ylabel('Score' if not use_japanese else 'スコア')
    ax3.set_title('Optimal Gene Combination' if not use_japanese else '最適遺伝子組合せ')
    ax3.set_ylim(0, max(opt_vals)*1.2)
    for bar, val in zip(bars3, opt_vals):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=10)

    # グラフ4: 結論テキスト表示
    ax4 = axes[1, 1]
    ax4.axis('off')
    conclusion = data.get('conclusion', 'N/A')
    rad_dose = data.get('radiation_dose', '?')
    grav_lvl = data.get('gravity_level', '?')
    p_total = data.get('P_total', '?')
    text = f"【結論】\n放射線量: {rad_dose} Sv/yr\n重力: {grav_lvl} g\n総合生存確率: {p_total}\n判定: {conclusion}"
    ax4.text(0.5, 0.5, text, ha='center', va='center', fontsize=12, 
             bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray'))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"✓ グラフ保存: {filename}")

# 4. サマリー出力
def print_summary(data, gene_effects, optimizations):
    print("\n" + "="*60)
    print("BIO-504 宇宙環境耐性遺伝子発現率 分析結果")
    print("="*60)
    print(f"放射線量: {data.get('radiation_dose', '?')} Sv/yr")
    print(f"重力レベル: {data.get('gravity_level', '?')} g")
    print(f"総合生存確率: {data.get('P_total', '?')}")
    print(f"結論: {data.get('conclusion', '?')}")
    print("-" * 40)
    print("遺伝子グループ効果:")
    for g in gene_effects:
        print(f"  {g[0]}: 効果値={g[1]:.3f}, 発現成功率={g[2]:.3f}")
    print("-"*40)
    print("最適化結果:")
    for o in optimizations:
        print(f"  {o[0]}: {o[1]:.3f}")
    print("="*60)
    print("計算パラメータ: 編集効率0.85, エピジェネティック0.7, 安定性0.9")
    print("="*60)

# 5. メイン
def main():
    data, gene_effects, optimizations = load_maxima_results()
    create_graphs(data, gene_effects, optimizations)
    print_summary(data, gene_effects, optimizations)
    
    # CSV出力
    df_genes = pd.DataFrame(gene_effects, columns=['Gene_Group', 'Effect_Value', 'Success_Rate'])
    df_opt = pd.DataFrame(optimizations, columns=['Strategy', 'Score'])
    df_genes.to_csv('BIO504_gene_effects.csv', index=False)
    df_opt.to_csv('BIO504_optimization.csv', index=False)
    print("✓ CSV出力完了")

if __name__ == "__main__":
    main()

