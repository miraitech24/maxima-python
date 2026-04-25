#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 08:39:00 2026

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
    
    data = {
        'gene_success': 0,
        'radiation_prob': 0,
        'microgravity_prob': 0,
        'metabolic_eff': 0,
        'total_survival': 0,
        'conclusion': '',
        'gene_effects': {},
        'optimization': {}
    }
    
    section = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line == 'gene_effects =':
                section = 'effects'
                continue
            elif line == 'optimization =':
                section = 'optimization'
                continue
            
            if '=' in line and section is None:
                parts = line.split('=')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    if 'gene_expression_success' in key:
                        data['gene_success'] = float(value)
                    elif 'radiation_survival_prob' in key:
                        data['radiation_prob'] = float(value)
                    elif 'microgravity_adaptation_prob' in key:
                        data['microgravity_prob'] = float(value)
                    elif 'metabolic_efficiency' in key:
                        data['metabolic_eff'] = float(value)
                    elif 'total_survival_probability' in key:
                        data['total_survival'] = float(value)
                    elif 'conclusion' in key:
                        data['conclusion'] = value
            
            elif ',' in line and section:
                parts = line.split(',')
                if section == 'effects' and len(parts) >= 3:
                    gene_type = parts[0].strip()
                    effect = float(parts[1].strip())
                    net_effect = float(parts[2].strip())
                    data['gene_effects'][gene_type] = {'effect': effect, 'net': net_effect}
                elif section == 'optimization' and len(parts) >= 2:
                    combo_name = parts[0].strip()
                    improvement = float(parts[1].strip())
                    data['optimization'][combo_name] = improvement
    
    print(f"✓ ファイル読み込み: {filename}")
    print(f"  総生存確率: {data['total_survival']:.3f}")
    print(f"  結論: {data['conclusion']}")
    return data

# 3. グラフ作成 (2x2 subplot) - タイトル重なり防止
def create_plots(data):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # グラフ1: 確率構成要素
    ax1 = axes[0, 0]
    components = ['遺伝子発現', '放射線耐性', '微小重力適応', '代謝効率']
    probs = [
        data['gene_success'],
        data['radiation_prob'],
        data['microgravity_prob'],
        data['metabolic_eff']
    ]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax1.bar(components, probs, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('確率', fontsize=10)
    ax1.set_title('確率構成要素', fontsize=11, pad=15)
    ax1.set_ylim(0, 1.0)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=45)
    
    # 確率値を表示
    for bar, prob in zip(bars, probs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{prob:.3f}', ha='center', va='bottom', fontsize=9)
    
    # グラフ2: 遺伝子効果比較
    ax2 = axes[0, 1]
    if data['gene_effects']:
        gene_types = list(data['gene_effects'].keys())
        effects = [data['gene_effects'][g]['effect'] for g in gene_types]
        net_effects = [data['gene_effects'][g]['net'] for g in gene_types]
        
        x = np.arange(len(gene_types))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, effects, width, label='総合効果', 
                       color='#8c564b', alpha=0.7)
        bars2 = ax2.bar(x + width/2, net_effects, width, label='正味効果', 
                       color='#e377c2', alpha=0.7)
        
        ax2.set_xlabel('遺伝子タイプ', fontsize=10)
        ax2.set_ylabel('効果率', fontsize=10)
        ax2.set_title('遺伝子効果比較', fontsize=11, pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels([g.replace('_', '\n') for g in gene_types], 
                           fontsize=9, rotation=0)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
    
    # グラフ3: 最適化提案
    ax3 = axes[1, 0]
    if data['optimization']:
        strategies = list(data['optimization'].keys())
        improvements = [data['optimization'][s] for s in strategies]
        
        # 改善後の確率を計算
        base_prob = data['total_survival']
        improved_probs = [min(1.0, base_prob * (1 + imp)) for imp in improvements]
        
        x = np.arange(len(strategies))
        width = 0.6
        
        bars = ax3.bar(x, improved_probs, width, color='#17becf', alpha=0.7)
        ax3.set_xlabel('最適化戦略', fontsize=10)
        ax3.set_ylabel('改善後確率', fontsize=10)
        ax3.set_title('最適化提案の効果', fontsize=11, pad=15)
        ax3.set_xticks(x)
        ax3.set_xticklabels([s.replace(' ', '\n') for s in strategies], 
                           fontsize=8, rotation=45, ha='right')
        ax3.set_ylim(0, 1.0)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 改善率を表示
        for bar, imp, prob in zip(bars, improvements, improved_probs):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'+{imp*100:.0f}%', ha='center', va='bottom', fontsize=9)
    
    # グラフ4: 結論表示
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # 結論テキストを表示
    conclusion_text = f"""【BIO-504 結論】

総合生存確率: {data['total_survival']:.3f} ({data['total_survival']*100:.1f}%)

{data['conclusion']}

詳細:
• 遺伝子発現: {data['gene_success']:.3f}
• 放射線耐性: {data['radiation_prob']:.3f}
• 微小重力適応: {data['microgravity_prob']:.3f}
• 代謝効率: {data['metabolic_eff']:.3f}

推奨アクション:
1. 遺伝子編集精度向上
2. 副作用低減技術開発
3. 物理的防護との統合
"""
    
    ax4.text(0.1, 0.5, conclusion_text, fontsize=10, 
            verticalalignment='center', linespacing=1.5)
    ax4.set_title('結論と推奨', fontsize=11, pad=15)
    
    # メインタイトル（サブプロット間隔調整）
    plt.suptitle('BIO-504: 宇宙環境耐性遺伝子発現率分析', 
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 上部スペース確保
    
    # 保存
    plt.savefig('BIO504_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✓ グラフ保存: BIO504_results.png")

# 4. サマリーファイル作成（結論含む）
def create_summary(data):
    total_survival = data['total_survival']
    
    summary = f"""BIO-504: 宇宙環境耐性遺伝子発現率 分析結果
========================================
【課題仕様】
目的: 遺伝子改変による宇宙環境適応の成功率定量化
入力: 放射線量、重力レベル、遺伝子編集効率、耐性遺伝子
出力: 総合生存確率、最適遺伝子組み合わせ
計算方法: 確率連鎖モデル、環境ストレス応答
========================================

【計算結果】
総合生存確率: {total_survival:.3f} ({total_survival*100:.1f}%)
遺伝子発現成功率: {data['gene_success']:.3f}
放射線耐性確率: {data['radiation_prob']:.3f}
微小重力適応確率: {data['microgravity_prob']:.3f}
代謝効率: {data['metabolic_eff']:.3f}
========================================

【遺伝子効果詳細】
"""
    for gene_type, effects in data['gene_effects'].items():
        summary += f"{gene_type}: 総合効果={effects['effect']:.3f}, 正味効果={effects['net']:.3f}\n"
    
    summary += f"\n【最適化提案】\n"
    for strategy, improvement in data['optimization'].items():
        improved_prob = min(1.0, total_survival * (1 + improvement))
        summary += f"{strategy}: 改善率={improvement*100:.1f}%, 期待確率={improved_prob:.3f}\n"
    
    summary += f"\n【結論】\n"
    summary += f"{data['conclusion']}\n\n"
    
    # 解釈と推奨
    if total_survival >= 0.7:
        summary += "解釈: 遺伝子改変による宇宙環境適応は高度に実現可能\n"
        summary += "推奨: 臨床試験加速、倫理的枠組み確立\n"
    elif total_survival >= 0.5:
        summary += "解釈: 遺伝子改変は有効だが追加対策が必要\n"
        summary += "推奨: 物理的防護との統合、副作用低減技術開発\n"
    elif total_survival >= 0.3:
        summary += "解釈: 限定的な適応のみ可能\n"
        summary += "推奨: 遺伝子編集精度向上、多遺伝子最適化\n"
    else:
        summary += "解釈: 生物学的限界が大きく、技術的補完が必要\n"
        summary += "推奨: 根本的な技術革新、ハイブリッドアプローチ\n"
    
    summary += f"\n生成日時: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    with open('BIO504_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    print("✓ サマリー保存: BIO504_summary.txt")

# 5. CSV結果ファイル作成
def create_csv(data):
    records = []
    
    # 基本確率
    records.append({
        'parameter': 'total_survival_probability',
        'value': data['total_survival'],
        'percentage': data['total_survival'] * 100,
        'log10_value': np.log10(max(data['total_survival'], 1e-50)),
        'category': 'overall'
    })
    
    records.append({
        'parameter': 'gene_expression_success',
        'value': data['gene_success'],
        'percentage': data['gene_success'] * 100,
        'log10_value': np.log10(max(data['gene_success'], 1e-50)),
        'category': 'genetic'
    })
    
    records.append({
        'parameter': 'radiation_resistance_probability',
        'value': data['radiation_prob'],
        'percentage': data['radiation_prob'] * 100,
        'log10_value': np.log10(max(data['radiation_prob'], 1e-50)),
        'category': 'environmental'
    })
    
    records.append({
        'parameter': 'microgravity_adaptation_probability',
        'value': data['microgravity_prob'],
        'percentage': data['microgravity_prob'] * 100,
        'log10_value': np.log10(max(data['microgravity_prob'], 1e-50)),
        'category': 'environmental'
    })
    
    records.append({
        'parameter': 'metabolic_efficiency',
        'value': data['metabolic_eff'],
        'percentage': data['metabolic_eff'] * 100,
        'log10_value': np.log10(max(data['metabolic_eff'], 1e-50)),
        'category': 'physiological'
    })
    
    # 遺伝子効果
    for gene_type, effects in data['gene_effects'].items():
        records.append({
            'parameter': f'{gene_type}_total_effect',
            'value': effects['effect'],
            'percentage': effects['effect'] * 100,
            'log10_value': np.log10(max(effects['effect'], 1e-50)),
            'category': 'gene_effect'
        })
        
        records.append({
            'parameter': f'{gene_type}_net_effect',
            'value': effects['net'],
            'percentage': effects['net'] * 100,
            'log10_value': np.log10(max(effects['net'], 1e-50)),
            'category': 'gene_effect'
        })
    
    # 最適化提案
    for strategy, improvement in data['optimization'].items():
        improved_prob = min(1.0, data['total_survival'] * (1 + improvement))
        records.append({
            'parameter': f'optimization_{strategy[:20]}',
            'value': improved_prob,
            'percentage': improved_prob * 100,
            'log10_value': np.log10(max(improved_prob, 1e-50)),
            'category': 'optimization'
        })
    
    df = pd.DataFrame(records)
    df.to_csv('BIO504_results.csv', index=False, encoding='utf-8')
    print("✓ CSV保存: BIO504_results.csv")
    return df

# 6. メイン実行
def main():
    print("="*60)
    print("BIO-504: 宇宙環境耐性遺伝子発現率 分析")
    print("="*60)
    
    # フォント設定表示
    print(f"フォント設定: {'日本語' if use_japanese else '英語'}")
    
    # データ読み込み
    data = load_maxima_results()
    
    # 即時結論表示
    print("\n【即時結論】")
    print("-"*40)
    print(f"総合生存確率: {data['total_survival']:.3f} ({data['total_survival']*100:.1f}%)")
    print(f"結論: {data['conclusion']}")
    
    if data['total_survival'] >= 0.7:
        print("評価: ✅ 高度に実現可能")
    elif data['total_survival'] >= 0.5:
        print("評価: ⚠ 実現可能（追加対策要）")
    elif data['total_survival'] >= 0.3:
        print("評価: ⚠ 限定的実現")
    else:
        print("評価: ❌ 現状では不十分")
    print("-"*40)
    
    # グラフ作成
    print("\nグラフ生成中...")
    create_plots(data)
    
    # サマリー作成
    create_summary(data)
    
    # CSV作成
    create_csv(data)
    
    print("\n" + "="*60)
    print("✅ 分析完了")
    print("生成ファイル:")
    print("  1. BIO504_results.png - 分析グラフ")
    print("  2. BIO504_summary.txt - 詳細サマリー")
    print("  3. BIO504_results.csv - データCSV")
    print("="*60)

if __name__ == "__main__":
    main()
