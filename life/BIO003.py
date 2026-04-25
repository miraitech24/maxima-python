#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 13:01:36 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIO-003: RNA自然形成確率 分析 (Python)
超シンプルMatplotlibプロンプト厳守版
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

# 2. ファイル読み込み (ファイルがなければ中止)
def load_maxima_results(filename='bio003_for_python.txt'):
    if not os.path.exists(filename):
        print(f"❌ エラー: {filename} なし")
        print("先に実行: maxima -b bio003.mac")
        sys.exit(1)
    
    data = {'total_prob': 0, 'components': {}, 'lengths': {}}
    section = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line == 'probability_components =':
                section = 'comp'
                continue
            elif line == 'length_probabilities =':
                section = 'len'
                continue
            
            if '=' in line and section is None:
                if 'total_formation_probability' in line:
                    data['total_prob'] = float(line.split('=')[1].strip())
            
            elif ',' in line and section:
                parts = line.split(',')
                if section == 'comp' and len(parts) >= 2:
                    data['components'][parts[0].strip()] = float(parts[1].strip())
                elif section == 'len' and len(parts) >= 2:
                    data['lengths'][int(parts[0].strip())] = float(parts[1].strip())
    
    print(f"✓ ファイル読み込み: {filename}")
    print(f"  総確率: {data['total_prob']:.3e}")
    return data

# 3. グラフ作成 (2x2 subplot)
def create_plots(data):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # グラフ1: 確率構成要素
    ax1 = axes[0, 0]
    comps = list(data['components'].keys())
    probs = list(data['components'].values())
    log_probs = [np.log10(max(p, 1e-50)) for p in probs]
    ax1.barh(comps, log_probs, color='skyblue')
    ax1.set_xlabel('log10(確率)')
    ax1.set_title('確率構成要素')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # グラフ2: RNA長による確率
    ax2 = axes[0, 1]
    lengths = sorted(data['lengths'].keys())
    length_probs = [data['lengths'][l] for l in lengths]
    ax2.semilogy(lengths, length_probs, 'o-', linewidth=2)
    ax2.set_xlabel('RNA長 (ヌクレオチド数)')
    ax2.set_ylabel('形成確率')
    ax2.set_title('RNA長による確率')
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=30, color='red', ls='--', alpha=0.5)
    
    # グラフ3: 宇宙論的比較
    ax3 = axes[1, 0]
    comparisons = [
        ('RNA形成', data['total_prob']),
        ('タンパク質(100aa)', 1e-130),
        ('宝くじ当選', 1e-7),
        ('地球存在', 1.0)
    ]
    names = [c[0] for c in comparisons]
    log_probs = [np.log10(max(c[1], 1e-50)) for c in comparisons]
    colors = ['red' if i==0 else 'gray' for i in range(len(names))]
    ax3.barh(names, log_probs, color=colors)
    ax3.set_xlabel('log10(確率)')
    ax3.set_title('宇宙論的比較')
    ax3.grid(True, alpha=0.3, axis='x')
    
    # グラフ4: 時間スケール
    ax4 = axes[1, 1]
    years = np.logspace(0, 10, 20)
    rates = [1e-20, 1e-25, 1e-30]
    for rate in rates:
        probs_t = 1 - np.exp(-rate * years * 3.1536e7)
        ax4.loglog(years, probs_t, label=f'rate={rate:.1e}')
    ax4.set_xlabel('時間 (年)')
    ax4.set_ylabel('累積確率')
    ax4.set_title('時間スケール分析')
    ax4.grid(True, alpha=0.3)
    ax4.axvline(x=4.5e9, color='green', ls='--', alpha=0.5)
    ax4.legend(fontsize=8)
    
    plt.suptitle('BIO-003: RNA自然形成確率分析', fontsize=12)
    plt.tight_layout()
    plt.savefig('BIO003_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✓ グラフ保存: BIO003_results.png")

# 4. サマリーファイル作成
def create_summary(data):
    total_prob = data['total_prob']
    
    summary = f"""BIO-003: RNA自然形成確率 分析結果
========================================
総形成確率: {total_prob:.3e}
log10(確率): {np.log10(max(total_prob, 1e-50)):.2f}
========================================

確率構成要素:
"""
    for comp, prob in data['components'].items():
        summary += f"  {comp}: {prob:.3e}\n"
    
    summary += f"\nRNA長別確率:\n"
    for length, prob in sorted(data['lengths'].items()):
        summary += f"  {length} nt: {prob:.3e}\n"
    
    summary += f"\n科学的解釈: "
    if total_prob > 1e-10:
        summary += "RNAワールド仮説は妥当"
    elif total_prob > 1e-20:
        summary += "特定条件下で可能性あり"
    else:
        summary += "代替起源理論が必要"
    
    with open('BIO003_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    print("✓ サマリー保存: BIO003_summary.txt")

# 5. CSV結果ファイル作成
def create_csv(data):
    df = pd.DataFrame([
        {'parameter': 'total_formation_probability', 
         'value': data['total_prob'],
         'log10_value': np.log10(max(data['total_prob'], 1e-50))}
    ])
    
    for comp, prob in data['components'].items():
        df = pd.concat([df, pd.DataFrame([{
            'parameter': comp,
            'value': prob,
            'log10_value': np.log10(max(prob, 1e-50))
        }])], ignore_index=True)
    
    for length, prob in data['lengths'].items():
        df = pd.concat([df, pd.DataFrame([{
            'parameter': f'length_{length}_nt',
            'value': prob,
            'log10_value': np.log10(max(prob, 1e-50))
        }])], ignore_index=True)
    
    df.to_csv('BIO003_results.csv', index=False, encoding='utf-8')
    print("✓ CSV保存: BIO003_results.csv")
    return df

# 6. メイン実行 (200行以内)
def main():
    print("="*60)
    print("BIO-003: RNA自然形成確率 分析")
    print("="*60)
    
    # フォント設定表示
    print(f"フォント: {'日本語' if use_japanese else '英語'}")
    
    # データ読み込み
    data = load_maxima_results()
    
    # グラフ作成
    create_plots(data)
    
    # サマリー作成
    create_summary(data)
    
    # CSV作成
    create_csv(data)
    
    print("\n" + "="*60)
    print("完了: グラフ, サマリー, CSV を出力")
    print("="*60)

if __name__ == "__main__":
    main()
