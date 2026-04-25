#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:10:56 2026

@author: iwamura
"""

#============================================================================
 ファイル: E003_micro_reactor.py
# 説明: マイクロ炉の導入可能性評価
# プロジェクト: ホルムズ危機回避・エネルギー安全保障
# 作成日: 2024-03-26
# バージョン: 1.0
#
# 課題仕様:
# 1. #28の計算結果（最適容積150m³）を引用
# 2. 導入可能サイト数と総発電容量を推定
# 3. 石油代替効果を定量評価
# 4. 実現期間とコストを試算
#
# 使用する既存計算:
# - #28: マイクロ炉最適容積 150m³
# - #26: テスラ送電効率 85%（送電連携時）
#
# 出力要件:
# 1. CSV: 導入サイト別評価結果
# 2. CSV: 総合評価サマリー
# 3. グラフ: 導入シナリオ比較
# 4. テキスト: 推奨アクションプラン
# ============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================================
# 1. 定数定義（#28の計算結果を引用）
# ============================================================================

# #28から引用: マイクロ炉最適設計値
V_OPTIMAL = 150.0        # 最適容積 [m³]
P_THERMAL = 50.0         # 熱出力 [MWth]
P_ELECTRIC = 20.0        # 電気出力 [MWe] (効率40%)
EFFICIENCY = 0.40        # 発電効率

# 燃料仕様
FUEL_TYPE = "TRISO"      # トリゾ燃料
BURNUP = 80000           # 燃焼度 [MWd/t]
REFUEL_CYCLE = 5.0       # 燃料交換周期 [年]
LIFETIME = 60.0          # 設計寿命 [年] (#41参照)

# 導入シナリオ
SITES_2025 = 3           # 2025年までに実証サイト数
SITES_2027 = 10          # 2027年までに導入サイト数
SITES_2030 = 100         # 2030年目標導入サイト数

# 石油代替換算
OIL_EQUIVALENT = 0.086   # 1MWeあたりの石油代替量 [kL/日]
CO2_REDUCTION = 0.5      # 1MWeあたりのCO2削減量 [t-CO2/日]

print("【E003: マイクロ炉導入評価】")
print("=" * 50)
print(f"#28計算結果引用: 最適容積 {V_OPTIMAL}m³")
print(f"電気出力: {P_ELECTRIC} MWe/基")
print(f"設計寿命: {LIFETIME} 年")
print(f"燃料交換: {REFUEL_CYCLE} 年ごと")
print()

# ============================================================================
# 2. 導入シナリオ計算
# ============================================================================

def calculate_scenarios():
    """
    3つの導入シナリオを計算
    """
    
    scenarios = {
        '保守的': {'sites': 30, 'year': 2030, 'description': '慎重導入'},
        '標準':   {'sites': 100, 'year': 2030, 'description': '計画的導入'},
        '積極的': {'sites': 300, 'year': 2030, 'description': '加速導入'}
    }
    
    results = []
    
    for name, scenario in scenarios.items():
        n_sites = scenario['sites']
        total_power = n_sites * P_ELECTRIC  # 総発電容量 [MWe]
        oil_reduction = total_power * OIL_EQUIVALENT  # 石油代替量 [kL/日]
        co2_reduction = total_power * CO2_REDUCTION   # CO2削減量 [t-CO2/日]
        
        # 投資額試算
        unit_cost = 50  # 1基あたり50億円（仮定）
        total_investment = n_sites * unit_cost
        
        results.append({
            'シナリオ': name,
            '導入基数': n_sites,
            '総発電容量_MWe': total_power,
            '石油代替_kL_日': oil_reduction,
            'CO2削減_t_日': co2_reduction,
            '総投資額_億円': total_investment,
            '目標年': scenario['year'],
            '説明': scenario['description']
        })
    
    return pd.DataFrame(results)

# 計算実行
df_scenarios = calculate_scenarios()

print("【導入シナリオ比較】")
print("-" * 60)
for _, row in df_scenarios.iterrows():
    print(f"■ {row['シナリオ']}シナリオ ({row['説明']})")
    print(f"  導入基数: {row['導入基数']}基 (目標{row['目標年']}年)")
    print(f"  総発電容量: {row['総発電容量_MWe']:.0f} MWe")
    print(f"  石油代替量: {row['石油代替_kL_日']:.0f} kL/日")
    print(f"  CO2削減量: {row['CO2削減_t_日']:.0f} t-CO2/日")
    print(f"  総投資額: {row['総投資額_億円']:.0f} 億円")
    print()

# CSV保存
df_scenarios.to_csv('E003_scenarios.csv', index=False, encoding='utf-8-sig')
print("✓ シナリオ比較表を保存: E003_scenarios.csv")

# ============================================================================
# 3. 段階的導入計画
# ============================================================================

def phased_deployment():
    """
    2025年から2030年までの段階的導入計画
    """
    
    years = list(range(2025, 2031))
    
    # 累積導入基数
    cumulative = {
        '保守的': [3, 8, 15, 20, 25, 30],
        '標準':   [3, 10, 30, 60, 80, 100],
        '積極的': [3, 15, 50, 120, 200, 300]
    }
    
    # 各年の石油代替量 [kL/日]
    oil_reduction = {}
    for scenario, sites_list in cumulative.items():
        oil_reduction[scenario] = [n * P_ELECTRIC * OIL_EQUIVALENT for n in sites_list]
    
    return years, cumulative, oil_reduction

years, cumulative, oil_reduction = phased_deployment()

print("【段階的導入計画】")
print("-" * 60)
print(f"{'年':>4} | {'保守的':>8} | {'標準':>8} | {'積極的':>8}")
print("-" * 40)
for i, year in enumerate(years):
    print(f"{year:>4} | {cumulative['保守的'][i]:>8} | {cumulative['標準'][i]:>8} | {cumulative['積極的'][i]:>8}")
print()

# ============================================================================
# 4. グラフ生成
# ============================================================================

def generate_charts():
    """
    導入シナリオ比較グラフを生成
    """
    
    # 日本語フォント検出
    import matplotlib.font_manager as fm
    jp_fonts = [f.name for f in fm.fontManager.ttflist if 'jp' in f.name.lower()]
    if jp_fonts:
        plt.rcParams['font.family'] = jp_fonts[0]
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('E003: Micro Reactor Deployment Scenarios\nマイクロ炉導入シナリオ', 
                 fontsize=14, fontweight='bold')
    
    # 左: 累積導入基数
    ax1 = axes[0]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, (scenario, data) in enumerate(cumulative.items()):
        ax1.plot(years, data, 'o-', color=colors[i], linewidth=2, 
                label=scenario, markersize=6)
    
    ax1.set_title('Cumulative Installations\n累積導入基数', fontsize=12)
    ax1.set_xlabel('Year', fontsize=10)
    ax1.set_ylabel('Number of Reactors', fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(fontsize=9)
    ax1.set_xlim(2024.5, 2030.5)
    
    # 右: 石油代替効果
    ax2 = axes[1]
    
    for i, (scenario, data) in enumerate(oil_reduction.items()):
        ax2.plot(years, data, 'o-', color=colors[i], linewidth=2,
                label=scenario, markersize=6)
    
    ax2.set_title('Oil Reduction Effect\n石油代替効果', fontsize=12)
    ax2.set_xlabel('Year', fontsize=10)
    ax2.set_ylabel('Oil Reduction [kL/day]', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(fontsize=9)
    ax2.set_xlim(2024.5, 2030.5)
    
    plt.tight_layout()
    plt.savefig('E003_micro_reactor.png', dpi=150, bbox_inches='tight')
    print("✓ グラフを保存: E003_micro_reactor.png")

generate_charts()

# ============================================================================
# 5. 総合評価と推奨事項
# ============================================================================

print("\n" + "=" * 60)
print("【総合評価: マイクロ炉導入の推奨事項】")
print("=" * 60)

# 標準シナリオの評価
std = df_scenarios[df_scenarios['シナリオ'] == '標準'].iloc[0]
print(f"\n■ 推奨シナリオ: 標準（計画的導入）")
print(f"  - 2030年までに {std['導入基数']:.0f} 基導入")
print(f"  - 総発電容量 {std['総発電容量_MWe']:.0f} MWe")
print(f"  - 石油代替量 {std['石油代替_kL_日']:.0f} kL/日")
print(f"  - 総投資額 {std['総投資額_億円']:.0f} 億円")
print(f"\n■ 石油代替効果（ホルムズ危機回避への貢献）")
print(f"  - ホルムズ海峡通過量の約 {std['石油代替_kL_日']/50000*100:.1f}% に相当")
print(f"  - CO2削減量: {std['CO2削減_t_日']:.0f} t-CO2/日")
print(f"\n■ リスクと対策")
print(f"  - 規制承認: 2025年までに3サイトで実証")
print(f"  - 社会受容: 地域説明会と安全情報公開")
print(f"  - サプライチェーン: 国内製造体制の確立")
print(f"\n■ 次のアクション")
print(f"  1. 2024年Q3: 実証サイト選定開始")
print(f"  2. 2025年Q1: 実証炉建設開始")
print(f"  3. 2026年Q4: 実証炉運転開始")
print(f"  4. 2027年: 商用炉展開開始")
print("=" * 60)

# ============================================================================
# ファイル終了
# 続きがあります（残り15行）：詳細コスト分析と#26連携
# ============================================================================
# ============================================================================
# ファイル: E003_micro_reactor.py (続き)
# 説明: 詳細コスト分析と#26連携
# ============================================================================
# ============================================================================
# ファイル: E003_micro_reactor.py (修正箇所)
# 説明: payback_years変数未定義エラーの修正
# 修正日: 2024-03-26
# ============================================================================

# ============================================================================
# 【修正前】6. 詳細コスト分析（関数内でローカル変数）
# ============================================================================
"""
def cost_analysis():
    ...
    payback_years = total_initial / annual_revenue
    return cost_breakdown, annual_revenue

cost_data, revenue = cost_analysis()
# ここでpayback_yearsは関数外では未定義
"""

# ============================================================================
# 【修正後】payback_yearsをグローバル変数として返す
# ============================================================================

def cost_analysis():
    """
    導入コストの内訳と回収期間を計算
    payback_yearsを戻り値に追加
    """
    
    print("\n【詳細コスト分析】")
    print("-" * 50)
    
    # コスト内訳（1基あたり）
    cost_breakdown = {
        '建設費': 35.0,        # 億円
        '燃料費初装荷': 8.0,   # 億円
        '運転維持費年': 1.5,   # 億円/年
        '廃炉費用': 5.0,       # 億円（運転終了時）
    }
    
    # 売電収入
    electricity_price = 15.0    # 円/kWh
    capacity_factor = 0.90      # 稼働率90%
    annual_gen = P_ELECTRIC * 1000 * 24 * 365 * capacity_factor / 1e6  # GWh/年
    annual_revenue = annual_gen * electricity_price * 1e6 / 1e8  # 億円/年
    
    print(f"1基あたりのコスト内訳:")
    for item, cost in cost_breakdown.items():
        print(f"  {item}: {cost:.1f} 億円")
    
    print(f"\n年間発電量: {annual_gen:.0f} GWh/年")
    print(f"年間売電収入: {annual_revenue:.1f} 億円/年")
    
    total_initial = cost_breakdown['建設費'] + cost_breakdown['燃料費初装荷']
    payback_years = total_initial / annual_revenue  # ← ここで計算
    
    print(f"\n初期投資回収期間: {payback_years:.1f} 年")
    print(f"60年稼働時の総収益: {(annual_revenue * 60 - total_initial - cost_breakdown['廃炉費用']):.0f} 億円")
    
    # payback_yearsを戻り値に追加
    return cost_breakdown, annual_revenue, payback_years

# 呼び出し側も修正
cost_data, revenue, payback_years = cost_analysis()  # ← 3つ受け取り

# ============================================================================
# 【修正前】8. 最終出力まとめ（payback_years参照）
# ============================================================================
"""
print(f"  投資回収期間: {payback_years:.1f} 年/基")  # ← ここで未定義エラー
"""

# ============================================================================
# 【修正後】8. 最終出力まとめ（修正済み）
# ============================================================================

print("\n" + "=" * 60)
print("【E003 マイクロ炉導入評価 完了】")
print("=" * 60)
print("生成ファイル:")
print("1. E003_scenarios.csv - 導入シナリオ比較")
print("2. E003_micro_reactor.png - 分析グラフ")
print()
print("主要数値（標準シナリオ、2030年）:")
print(f"  導入基数: 100基")
print(f"  総発電容量: {100*P_ELECTRIC:.0f} MWe")
print(f"  石油代替: {100*P_ELECTRIC*OIL_EQUIVALENT:.0f} kL/日")
print(f"  総投資額: {100*50:.0f} 億円")
print(f"  投資回収期間: {payback_years:.1f} 年/基")  # ← 正常に動作
print()
print("ホルムズ危機回避への貢献:")
print(f"  中東依存度: {100*P_ELECTRIC*OIL_EQUIVALENT/50000*100:.1f}%削減（100基時）")
print("=" * 60)

# ============================================================================
# ファイル終了
# 修正箇所: cost_analysis()の戻り値にpayback_yearsを追加
# ============================================================================

# ============================================================================
# 7. #26テスラ送電との連携評価
# ============================================================================

def tesla_integration():
    """
    #26テスラ送電との連携による送電網最適化
    """
    
    print("\n【#26テスラ送電連携評価】")
    print("-" * 50)
    
    # #26計算結果引用
    TESLA_EFFICIENCY = 0.85    # テスラ送電効率 85%
    TESLA_RANGE = 100          # 送電可能距離 [km]
    
    # マイクロ炉設置場所の自由度
    conventional_loss = 0.05   # 従来送電ロス 5%
    tesla_loss = 1 - TESLA_EFFICIENCY  # テスラ送電ロス 15%
    
    print(f"#26計算結果引用: テスラ送電効率 {TESLA_EFFICIENCY*100:.0f}%")
    print(f"送電可能距離: {TESLA_RANGE} km")
    print()
    
    print("連携メリット:")
    print("1. 設置場所の制約緩和（送電網不要エリアにも設置可能）")
    print("2. 離島・山間部への電力供給が容易")
    print("3. 災害時の電力供給冗長性向上")
    print("4. 送電線用地取得不要")
    print()
    
    # 効率比較
    print(f"従来送電ロス: {conventional_loss*100:.0f}%")
    print(f"テスラ送電ロス: {tesla_loss*100:.0f}%")
    print(f"差引効率差: {(tesla_loss - conventional_loss)*100:.1f}%（テスラ不利）")
    print()
    print("→ 短距離（<10km）では従来送電、")
    print("  長距離・困難地形ではテスラ送電を選択")
    
tesla_integration()

# ============================================================================
# 8. 最終出力まとめ
# ============================================================================

print("\n" + "=" * 60)
print("【E003 マイクロ炉導入評価 完了】")
print("=" * 60)
print("生成ファイル:")
print("1. E003_scenarios.csv - 導入シナリオ比較")
print("2. E003_micro_reactor.png - 分析グラフ")
print()
print("主要数値（標準シナリオ、2030年）:")
print(f"  導入基数: 100基")
print(f"  総発電容量: {100*P_ELECTRIC:.0f} MWe")
print(f"  石油代替: {100*P_ELECTRIC*OIL_EQUIVALENT:.0f} kL/日")
print(f"  総投資額: {100*50:.0f} 億円")
print(f"  投資回収期間: {payback_years:.1f} 年/基")
print()
print("ホルムズ危機回避への貢献:")
print(f"  中東依存度: {100*P_ELECTRIC*OIL_EQUIVALENT/50000*100:.1f}%削減（100基時）")
print("=" * 60)

# ============================================================================
# ファイル終了
# 全コード: 245行
# ============================================================================
