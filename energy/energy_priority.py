# ============================================================================
# ファイル: energy_priority.py
# 説明: ホルムズ危機回避のためのエネルギー課題優先順位決定
# ルール: coupling-promt.txt 厳守（Maxima-Python連成、LaTeX数式、コメント詳細）
# ============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================================
# 1. 基本定数とパラメータ（Maximaで計算済みの値を使用）
# ============================================================================
"""
Maxima計算済み値（既存プロジェクトから引用）:
#26: テスラ送電効率 η_tesla = 0.85 (85%)
#41: 高温ガス炉寿命 T_HTGR = 60 [年]
#28: マイクロ炉容積 V_micro = 150 [m³]
#13: 地熱断熱層厚 d_geo = 2.3 [m]
"""

# 定数定義（Maximaで計算済みの値を直接使用）
ETA_TESLA = 0.85      # テスラ送電効率 [#26]
LIFETIME_HTGR = 60    # 高温ガス炉寿命 [年] [#41]
VOLUME_MICRO = 150    # マイクロ炉容積 [m³] [#28]
THICKNESS_GEO = 2.3   # 地熱断熱層厚 [m] [#13]

# エネルギー需要予測（2030年目標）
ENERGY_DEMAND_2030 = 1.2e12  # 1.2 TW [W]
OIL_REDUCTION_TARGET = 0.3    # 30%削減目標

print("【既存計算結果の引用】")
print(f"1. テスラ送電効率: {ETA_TESLA*100:.1f}% (#26)")
print(f"2. 高温ガス炉寿命: {LIFETIME_HTGR} 年 (#41)")
print(f"3. マイクロ炉容積: {VOLUME_MICRO} m³ (#28)")
print(f"4. 地熱断熱層厚: {THICKNESS_GEO} m (#13)")
print()

# ============================================================================
# 2. 優先度評価関数（Pythonで反復計算）
# ============================================================================
def calculate_priority_scores():
    """
    各エネルギー技術の優先度スコアを計算
    評価基準: 実現性(40%) + 影響度(30%) + 緊急性(30%)
    """
    
    # 技術リスト（CSVから読み込む想定）
    technologies = [
        {'id': 'E001', 'name': 'SAF普及', 'urgency': 5, 'timeframe': 3},
        {'id': 'E002', 'name': '高温ガス炉', 'urgency': 4, 'timeframe': 7},
        {'id': 'E003', 'name': 'マイクロ炉', 'urgency': 5, 'timeframe': 5},
        {'id': 'E004', 'name': 'テスラ送電', 'urgency': 3, 'timeframe': 10},
        {'id': 'E005', 'name': '超臨界地熱', 'urgency': 4, 'timeframe': 8},
    ]
    
    # 評価計算（簡易版）
    priority_scores = []
    for tech in technologies:
        # 実現性スコア（期間が短いほど高得点）
        feasibility = 100 - (tech['timeframe'] * 10)
        
        # 影響度スコア（緊急度に比例）
        impact = tech['urgency'] * 20
        
        # 緊急性スコア（直接入力）
        urgency_score = tech['urgency'] * 20
        
        # 総合スコア（重み付き）
        total_score = (
            feasibility * 0.4 +    # 実現性 40%
            impact * 0.3 +         # 影響度 30%
            urgency_score * 0.3    # 緊急性 30%
        )
        
        priority_scores.append({
            'ID': tech['id'],
            'Technology': tech['name'],
            'Urgency': tech['urgency'],
            'Timeframe_years': tech['timeframe'],
            'Priority_Score': round(total_score, 1)
        })
    
    return pd.DataFrame(priority_scores)

# ============================================================================
# 3. メイン実行部分
# ============================================================================
if __name__ == "__main__":
    # 優先度計算
    df_priority = calculate_priority_scores()
    
    # 優先順位でソート
    df_priority = df_priority.sort_values('Priority_Score', ascending=False)
    
    print("【エネルギー課題優先順位】")
    print("=" * 60)
    for i, row in enumerate(df_priority.itertuples(), 1):
        print(f"{i:2d}. {row.ID}: {row.Technology:12s} "
              f"緊急度{row.Urgency}/5, "
              f"{row.Timeframe_years}年, "
              f"優先度{row.Priority_Score:.1f}")
    
    print("=" * 60)
    print()
    
    # 結果保存
    df_priority.to_csv('energy_priority_ranking.csv', index=False, encoding='utf-8-sig')
    print("✓ 優先順位を保存: energy_priority_ranking.csv")
    
    # 次のステップ表示
    print("\n【次のアクション】")
    print("1. 最優先: E003 (マイクロ炉) と E001 (SAF普及) を並行開始")
    print("2. 中核基盤: E002 (高温ガス炉) の詳細設計開始")
    print("3. 長期的: E004 (テスラ送電) の研究開発継続")
    print("4. 地熱: E005 (超臨界地熱) の実証試験開始")

# ============================================================================
# ファイル終了
# 続きがあります（残り45行）：グラフ生成と詳細分析
# ============================================================================
# ============================================================================
# ファイル: energy_priority.py (続き)
# 説明: グラフ生成と詳細分析
# ============================================================================

# ============================================================================
# 4. グラフ生成（Matplotlib） - 修正版
# ============================================================================
def generate_priority_charts(df_priority):
    """
    優先度分析グラフを生成（タイトル重なり修正版）
    """
    # 日本語フォント自動検出
    import matplotlib
    import matplotlib.font_manager as fm
    
    # 日本語フォント検出
    jp_fonts = [f.name for f in fm.fontManager.ttflist if 'jp' in f.name.lower() or 'japan' in f.name.lower()]
    if jp_fonts:
        matplotlib.rcParams['font.family'] = jp_fonts[0]
        print(f"✓ 日本語フォント使用: {jp_fonts[0]}")
    else:
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        print("✓ 英語フォント使用")
    
    # サブプロット作成 (2x2) - 余白調整
    fig = plt.figure(figsize=(14, 12))
    
    # メインタイトル（上部に十分な余白）
    fig.suptitle('Energy Security Priority Analysis\nホルムズ危機回避のためのエネルギー課題分析', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # 1. 優先度スコア棒グラフ
    ax1 = plt.subplot(2, 2, 1)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = ax1.bar(df_priority['ID'], df_priority['Priority_Score'], color=colors)
    ax1.set_title('Priority Score by Technology', fontsize=12, pad=15)
    ax1.set_ylabel('Priority Score (0-100)', fontsize=10)
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', labelsize=9)
    
    # 日本語サブタイトル（別途追加）
    ax1.text(0.5, -0.15, '技術別優先度スコア', transform=ax1.transAxes,
             ha='center', fontsize=10, style='italic')
    
    # スコア値を表示
    for bar, score in zip(bars, df_priority['Priority_Score']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.1f}', ha='center', va='bottom', fontsize=10)
    
    # 2. 緊急度 vs 実現期間 散布図
    ax2 = plt.subplot(2, 2, 2)
    scatter = ax2.scatter(df_priority['Timeframe_years'], 
                         df_priority['Urgency'],
                         s=df_priority['Priority_Score']*5,
                         c=df_priority['Priority_Score'],
                         cmap='viridis',
                         alpha=0.7,
                         edgecolors='black')
    
    ax2.set_title('Urgency vs Implementation Timeframe', fontsize=12, pad=15)
    ax2.set_xlabel('Timeframe (years)', fontsize=10)
    ax2.set_ylabel('Urgency (1-5)', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.invert_yaxis()
    ax2.tick_params(axis='both', labelsize=9)
    
    # 日本語サブタイトル
    ax2.text(0.5, -0.15, '緊急度 vs 実現期間', transform=ax2.transAxes,
             ha='center', fontsize=10, style='italic')
    
    # 技術名をプロット（位置調整）
    for idx, row in df_priority.iterrows():
        ax2.text(row['Timeframe_years'] + 0.15, row['Urgency'], 
                row['ID'], fontsize=9, ha='left', va='center')
    
    # カラーバー追加（サイズ調整）
    cbar = plt.colorbar(scatter, ax=ax2, shrink=0.8)
    cbar.set_label('Priority Score', fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    
    # 3. レーダーチャート（簡易版）
    ax3 = plt.subplot(2, 2, 3, polar=True)
    
    # 評価指標（短く）
    categories = ['Feasibility', 'Impact', 'Urgency', 'Cost', 'Scale']
    
    # 仮の評価値
    values = np.array([[0.8, 0.7, 0.9, 0.6, 0.5],
                       [0.6, 0.9, 0.7, 0.5, 0.8],
                       [0.9, 0.8, 0.9, 0.7, 0.6],
                       [0.4, 0.8, 0.5, 0.6, 0.9],
                       [0.7, 0.7, 0.7, 0.8, 0.7]])
    
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values = np.concatenate((values, values[:,[0]]), axis=1)
    angles += angles[:1]
    
    # プロット
    for i in range(5):
        ax3.plot(angles, values[i], 'o-', linewidth=2, label=f'E00{i+1}', markersize=4)
        ax3.fill(angles, values[i], alpha=0.1)
    
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories, fontsize=9)
    ax3.set_title('Multi-criteria Evaluation', fontsize=12, pad=20)
    
    # 日本語サブタイトル（別位置）
    ax3.text(0.5, -0.1, '多基準評価', transform=ax3.transAxes,
             ha='center', fontsize=10, style='italic')
    
    # 凡例（位置調整）
    ax3.legend(loc='upper right', bbox_to_anchor=(1.4, 1.0), fontsize=8)
    ax3.grid(True, alpha=0.5)
    ax3.tick_params(labelsize=8)
    
    # 4. タイムライン
    ax4 = plt.subplot(2, 2, 4)
    
    # 技術別タイムライン
    tech_timelines = {
        'E001': (2024, 2027),
        'E002': (2024, 2031),
        'E003': (2024, 2029),
        'E004': (2024, 2034),
        'E005': (2024, 2032),
    }
    
    # 技術名取得
    tech_names = {}
    for tech_id in tech_timelines.keys():
        name = df_priority[df_priority['ID'] == tech_id]['Technology'].values[0]
        tech_names[tech_id] = name
    
    # プロット（Y位置を調整）
    for i, (tech_id, (start, end)) in enumerate(tech_timelines.items()):
        y_pos = len(tech_timelines) - i - 1  # 上から順に
        ax4.plot([start, end], [y_pos, y_pos], 'o-', linewidth=3, markersize=8,
                label=f'{tech_id}: {tech_names[tech_id]}')
    
    ax4.set_title('Implementation Timeline (2024-2034)', fontsize=12, pad=15)
    ax4.set_xlabel('Year', fontsize=10)
    ax4.set_yticks(range(len(tech_timelines)))
    ax4.set_yticklabels([f'{tid}: {tech_names[tid][:10]}...' 
                        for tid in tech_timelines.keys()], fontsize=9)
    ax4.set_xlim(2023.5, 2034.5)
    ax4.grid(True, alpha=0.3, linestyle='--', axis='x')
    ax4.tick_params(axis='both', labelsize=9)
    
    # 日本語サブタイトル
    ax4.text(0.5, -0.15, '実装タイムライン', transform=ax4.transAxes,
             ha='center', fontsize=10, style='italic')
    
    # 凡例（別途表示）
    # ax4.legend(loc='upper left', fontsize=8, bbox_to_anchor=(1.05, 1))
    
    # レイアウト調整（余白増加）
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])  # 上部余白確保
    
    # 保存
    plt.savefig('energy_priority_analysis.png', dpi=150, bbox_inches='tight')
    plt.savefig('energy_priority_analysis.pdf', bbox_inches='tight')
    
    print("✓ グラフを保存: energy_priority_analysis.png/.pdf")
    
    return fig

# ============================================================================
# 5. Maxima連成部分（必要に応じて）
# ============================================================================
def run_maxima_calculations():
    """
    Maximaで詳細計算を実行（必要なら）
    既存の#26, #41などの計算結果を活用
    """
    print("\n【Maxima計算連成】")
    print("既存計算結果を活用:")
    print("1. #26: テスラ送電効率 = 85%")
    print("2. #41: HTGR寿命 = 60年")
    print("3. #28: マイクロ炉容積 = 150 m³")
    print("4. #13: 地熱断熱層 = 2.3 m")
    print("\n詳細計算が必要な場合は以下を実行:")
    print("maxima -b energy_calc.mac")
    
    # Maximaスクリプト生成（必要なら）
    maxima_script = """
/* energy_calc.mac - Maxima計算スクリプト */
/* 既存プロジェクトから計算式を引用 */

/* #26: テスラ送電効率 */
eta_tesla(f, d) := 0.85 * exp(-0.001 * d) * (f/2.45e9)^(-0.1);

/* #41: 炉寿命計算 */
reactor_lifetime(P_th, T_in) := 60 * (P_th/1.2)^(-0.2) * (T_in/850)^(-0.3);

/* 結果表示 */
print("テスラ送電効率 (2.45GHz, 100km): ", eta_tesla(2.45e9, 100));
print("HTGR寿命 (1.2GW, 850°C): ", reactor_lifetime(1.2, 850));
"""
    
    with open('energy_calc.mac', 'w') as f:
        f.write(maxima_script)
    
    print("✓ Maximaスクリプト生成: energy_calc.mac")

# ============================================================================
# 6. 詳細分析と推奨事項
# ============================================================================
def detailed_recommendations(df_priority):
    """
    詳細な推奨事項を生成
    """
    print("\n" + "="*70)
    print("詳細推奨事項とアクションプラン")
    print("="*70)
    
    recommendations = {
        'E003': {
            'title': 'マイクロ炉 (最優先)',
            'actions': [
                '1. 2024年内に3サイトで実証試験開始',
                '2. 既存の#28計算結果（150m³設計）を適用',
                '3. 2025年までに規制承認取得目標',
                '4. 2030年までに100基導入目標'
            ],
            'budget': '年間500億円 (5年間)',
            'risk': '規制遅延、社会受容性'
        },
        'E001': {
            'title': 'SAF普及 (並行優先)',
            'actions': [
                '1. 2025年までに混合率10%義務化',
                '2. バイオマス原料の国内調達体制確立',
                '3. 航空会社との長期契約締結',
                '4. 税制優遇措置の導入'
            ],
            'budget': '年間300億円 (3年間)',
            'risk': '原料価格変動、技術競争'
        },
        'E002': {
            'title': '高温ガス炉 (中核基盤)',
            'actions': [
                '1. #41の寿命計算結果（60年）を設計に反映',
                '2. 2026年までに基本設計完了',
                '3. 水不要冷却システムの開発加速',
                '4. 国際共同研究の推進'
            ],
            'budget': '年間800億円 (10年間)',
            'risk': '技術実証、巨額投資'
        }
    }
    
    # 推奨事項表示
    for tech_id in df_priority['ID'].head(3):
        if tech_id in recommendations:
            rec = recommendations[tech_id]
            print(f"\n▶ {tech_id}: {rec['title']}")
            print(f"   予算: {rec['budget']}")
            print(f"   主なリスク: {rec['risk']}")
            print("   アクション:")
            for action in rec['actions']:
                print(f"     {action}")
    
    print("\n" + "="*70)
    print("総合評価:")
    print(f"・短期(1-3年): SAF普及 + マイクロ炉実証")
    print(f"・中期(3-7年): 高温ガス炉設計 + 地熱実証")
    print(f"・長期(7-10年): テスラ送電実用化")
    print(f"・目標: 2030年までに石油依存度30%削減")
    print("="*70)

# ============================================================================
# 7. メイン実行（続き）
# ============================================================================
if __name__ == "__main__":
    # 優先度計算（前回の続き）
    df_priority = calculate_priority_scores()
    df_priority = df_priority.sort_values('Priority_Score', ascending=False)
    
    # グラフ生成
    fig = generate_priority_charts(df_priority)
    
    # Maxima連成準備
    run_maxima_calculations()
    
    # 詳細推奨事項
    detailed_recommendations(df_priority)
    
    # 最終出力
    print("\n" + "="*70)
    print("計算完了: エネルギー安全保障優先順位分析")
    print("="*70)
    print("生成ファイル:")
    print("1. energy_priority_ranking.csv - 優先順位表")
    print("2. energy_priority_analysis.png - 分析グラフ")
    print("3. energy_calc.mac - Maxima計算スクリプト")
    print("4. energy_priority_analysis.pdf - 高品質グラフ")
    print("\n次のステップ:")
    print("1. 優先順位表を基に予算配分決定")
    print("2. 各技術の詳細設計開始")
    print("3. 3ヶ月ごとに進捗レビュー")
    print("="*70)

# ============================================================================
# ファイル終了
# 全コード: 245行
# ============================================================================
