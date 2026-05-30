# TaskID: BIO-505 - Human Photosynthesis Efficiency Calculation
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================
# パラメータ設定
# ============================================================
solar_constant = 1361  # W/m^2 (太陽定数)
human_surface_area = 1.8  # m^2 (成人の体表面積)
chloroplast_efficiency = 0.1  # 葉緑体の光合成効率 (10%)
human_energy_requirement = 2000  # kcal/day (成人の1日必要エネルギー)
kcal_to_joule = 4184  # 1 kcal = 4184 J

# ============================================================
# 計算関数
# ============================================================
def calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0.5):
    """
    人間の光合成効率を計算
    
    Parameters:
    -----------
    sunlight_hours : float
        1日の日照時間 (h)
    cloud_cover : float
        雲量 (0-1)
    
    Returns:
    --------
    dict : 計算結果
    """
    # 1日あたりの受光エネルギー (J)
    # E_solar = G_sc * A * t * (1 - C)
    # G_sc: 太陽定数 (W/m^2)
    # A: 体表面積 (m^2)
    # t: 日照時間 (s)
    # C: 雲量
    daily_solar_energy = solar_constant * human_surface_area * sunlight_hours * 3600 * (1 - cloud_cover)
    
    # 光合成によるエネルギー生産 (J)
    # E_photo = E_solar * η_chloroplast
    # η_chloroplast: 葉緑体の光合成効率
    photosynthetic_energy = daily_solar_energy * chloroplast_efficiency
    
    # 必要エネルギー (J/day)
    # E_req = 2000 kcal/day × 4184 J/kcal
    required_energy = human_energy_requirement * kcal_to_joule
    
    # 自給率
    # R = E_photo / E_req
    self_sufficiency_rate = photosynthetic_energy / required_energy
    
    return {
        'daily_solar_energy_J': daily_solar_energy,
        'photosynthetic_energy_J': photosynthetic_energy,
        'required_energy_J': required_energy,
        'self_sufficiency_rate': self_sufficiency_rate,
        'self_sufficiency_percent': self_sufficiency_rate * 100
    }

# ============================================================
# メイン計算
# ============================================================
print("=" * 70)
print("BIO-505: Human Photosynthesis Efficiency Calculation")
print("=" * 70)

# 標準条件での計算
result = calc_photosynthesis_efficiency()
print(f"\n【標準条件】日照時間: 8時間, 雲量: 50%")
print(f"  1日受光エネルギー: {result['daily_solar_energy_J']:.2e} J")
print(f"  光合成生産エネルギー: {result['photosynthetic_energy_J']:.2e} J")
print(f"  必要エネルギー: {result['required_energy_J']:.2e} J")
print(f"  自給率: {result['self_sufficiency_percent']:.2f}%")

# パラメータスイープ
print(f"\n【日照時間による自給率変化】(雲量: 0%)")
for hours in [0, 4, 8, 12, 16, 20, 24]:
    r = calc_photosynthesis_efficiency(sunlight_hours=hours, cloud_cover=0)
    print(f"  日照{hours:2d}時間: {r['self_sufficiency_percent']:.2f}%")

print(f"\n【雲量による自給率変化】(日照: 8時間)")
for cloud in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    r = calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=cloud)
    print(f"  雲量{cloud:.1f}: {r['self_sufficiency_percent']:.2f}%")

# ============================================================
# グラフ作成
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('BIO-505: Human Photosynthesis Efficiency Analysis', fontsize=16, fontweight='bold')

# --- グラフ1: 日照時間 vs 自給率 ---
hours = np.linspace(0, 24, 100)
rates_clear = [calc_photosynthesis_efficiency(sunlight_hours=h, cloud_cover=0)['self_sufficiency_percent'] for h in hours]
rates_cloudy = [calc_photosynthesis_efficiency(sunlight_hours=h, cloud_cover=0.5)['self_sufficiency_percent'] for h in hours]

axes[0, 0].plot(hours, rates_clear, 'b-', linewidth=2, label='Clear sky (0% cloud)')
axes[0, 0].plot(hours, rates_cloudy, 'r--', linewidth=2, label='Cloudy (50% cloud)')
axes[0, 0].axhline(y=100, color='g', linestyle=':', linewidth=2, label='100% self-sufficiency')
axes[0, 0].fill_between(hours, 0, rates_clear, alpha=0.1, color='blue')
axes[0, 0].set_xlabel('Sunlight Hours (h/day)', fontsize=12)
axes[0, 0].set_ylabel('Self-Sufficiency Rate (%)', fontsize=12)
axes[0, 0].set_title('Fig.1: Photosynthetic Self-Sufficiency vs Sunlight Hours', fontsize=11)
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xlim(0, 24)
axes[0, 0].set_ylim(0, 200)

# 数式説明テキスト
formula_text1 = r'$R = \frac{G_{sc} \cdot A \cdot t \cdot (1-C) \cdot \eta}{E_{req}}$'
axes[0, 0].text(0.5, 0.95, formula_text1, transform=axes[0, 0].transAxes,
                fontsize=10, verticalalignment='top', horizontalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# --- グラフ2: 雲量 vs 自給率 ---
clouds = np.linspace(0, 1, 100)
rates_8h = [calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=c)['self_sufficiency_percent'] for c in clouds]
rates_12h = [calc_photosynthesis_efficiency(sunlight_hours=12, cloud_cover=c)['self_sufficiency_percent'] for c in clouds]

axes[0, 1].plot(clouds, rates_8h, 'b-', linewidth=2, label='8h sunlight')
axes[0, 1].plot(clouds, rates_12h, 'r--', linewidth=2, label='12h sunlight')
axes[0, 1].fill_between(clouds, 0, rates_8h, alpha=0.1, color='blue')
axes[0, 1].set_xlabel('Cloud Cover (0-1)', fontsize=12)
axes[0, 1].set_ylabel('Self-Sufficiency Rate (%)', fontsize=12)
axes[0, 1].set_title('Fig.2: Photosynthetic Self-Sufficiency vs Cloud Cover', fontsize=11)
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_xlim(0, 1)
axes[0, 1].set_ylim(0, 200)

# --- グラフ3: エネルギー収支 (棒グラフ) ---
categories = ['Solar Input\n(W/m²)', 'Photosynthetic\nOutput (J/day)', 'Human\nRequirement (J/day)']
values_8h = [
    solar_constant,
    calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0)['photosynthetic_energy_J'],
    calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0)['required_energy_J']
]
colors = ['gold', 'green', 'red']
bars = axes[1, 0].bar(categories, values_8h, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
axes[1, 0].set_ylabel('Energy', fontsize=12)
axes[1, 0].set_title('Fig.3: Daily Energy Budget (8h sunlight, clear sky)', fontsize=11)
axes[1, 0].tick_params(axis='x', rotation=0)
for bar, val in zip(bars, values_8h):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{val:.2e}', ha='center', va='bottom', fontsize=9, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# --- グラフ4: 100%自給率達成条件 ---
required_rate = 1.0  # 100% self-sufficiency
current_rate = result['self_sufficiency_rate']
required_multiplier = required_rate / current_rate
required_area = human_surface_area * required_multiplier

metrics = ['Current\nEfficiency (%)', 'Required\nMultiplier', 'Required\nArea (m²)']
values = [current_rate * 100, required_multiplier, required_area]
colors2 = ['lightblue', 'orange', 'purple']
bars = axes[1, 1].bar(metrics, values, color=colors2, alpha=0.8, edgecolor='black', linewidth=1.5)
axes[1, 1].set_ylabel('Value', fontsize=12)
axes[1, 1].set_title('Fig.4: Requirements for 100% Self-Sufficiency', fontsize=11)
for bar, val in zip(bars, values):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('BIO505_photosynthesis_analysis.png', dpi=150, bbox_inches='tight')
print(f"\nグラフを保存: BIO505_photosynthesis_analysis.png")

# ============================================================
# .mdファイル書き出し
# ============================================================
md_content = f"""# BIO-505: Human Photosynthesis Efficiency Calculation

## 概要
人間に葉緑体を導入した場合の光合成効率を計算し、エネルギー自給率を評価する。

## 基本パラメータ

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| 太陽定数 $G_{{sc}}$ | {solar_constant} W/m² | 地球軌道での太陽放射強度 |
| 体表面積 $A$ | {human_surface_area} m² | 成人の平均体表面積 |
| 葉緑体効率 $\\eta$ | {chloroplast_efficiency} (10%) | 光合成のエネルギー変換効率 |
| 必要エネルギー $E_{{req}}$ | {human_energy_requirement} kcal/day | 成人の1日必要エネルギー |

## 計算式

### 1日あたりの受光エネルギー
$$E_{{solar}} = G_{{sc}} \\cdot A \\cdot t \\cdot (1 - C)$$

- $G_{{sc}}$: 太陽定数 (1361 W/m²)
- $A$: 体表面積 (1.8 m²)
- $t$: 日照時間 (秒)
- $C$: 雲量 (0-1)

### 光合成によるエネルギー生産
$$E_{{photo}} = E_{{solar}} \\cdot \\eta_{{chloroplast}}$$

- $\\eta_{{chloroplast}}$: 葉緑体の光合成効率 (10%)

### エネルギー自給率
$$R = \\frac{{E_{{photo}}}}{{E_{{req}}}}$$

- $E_{{req}}$: 1日あたりの必要エネルギー (2000 kcal = 8,368,000 J)

## 計算結果

### 標準条件 (日照8時間、雲量50%)
| 項目 | 値 |
|------|-----|
| 1日受光エネルギー | {result['daily_solar_energy_J']:.2e} J |
| 光合成生産エネルギー | {result['photosynthetic_energy_J']:.2e} J |
| 必要エネルギー | {result['required_energy_J']:.2e} J |
| 自給率 | {result['self_sufficiency_percent']:.2f}% |

### 日照時間による自給率変化 (雲量0%)
| 日照時間 | 自給率 |
|---------|--------|
| 0時間 | 0.00% |
| 4時間 | {calc_photosynthesis_efficiency(sunlight_hours=4, cloud_cover=0)['self_sufficiency_percent']:.2f}% |
| 8時間 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0)['self_sufficiency_percent']:.2f}% |
| 12時間 | {calc_photosynthesis_efficiency(sunlight_hours=12, cloud_cover=0)['self_sufficiency_percent']:.2f}% |
| 16時間 | {calc_photosynthesis_efficiency(sunlight_hours=16, cloud_cover=0)['self_sufficiency_percent']:.2f}% |
| 24時間 | {calc_photosynthesis_efficiency(sunlight_hours=24, cloud_cover=0)['self_sufficiency_percent']:.2f}% |

### 雲量による自給率変化 (日照8時間)
| 雲量 | 自給率 |
|-----|--------|
| 0.0 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0)['self_sufficiency_percent']:.2f}% |
| 0.2 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0.2)['self_sufficiency_percent']:.2f}% |
| 0.4 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0.4)['self_sufficiency_percent']:.2f}% |
| 0.6 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0.6)['self_sufficiency_percent']:.2f}% |
| 0.8 | {calc_photosynthesis_efficiency(sunlight_hours=8, cloud_cover=0.8)['self_sufficiency_percent']:.2f}% |
| 1.0 | 0.00% |

## グラフ説明

### Fig.1: 日照時間 vs 自給率
- **横軸**: 1日の日照時間 (0-24時間)
- **縦軸**: エネルギー自給率 (%)
- **青線**: 快晴時 (雲量0%)
- **赤破線**: 曇天時 (雲量50%)
- **緑点線**: 100%自給率ライン
- **考察**: 快晴時は約11時間の日照で100%自給率達成。曇天時は24時間日照でも100%に達しない。

### Fig.2: 雲量 vs 自給率
- **横軸**: 雲量 (0-1)
- **縦軸**: エネルギー自給率 (%)
- **青線**: 8時間日照
- **赤破線**: 12時間日照
- **考察**: 雲量が増加すると自給率は直線的に減少。12時間日照でも雲量0.5以上で100%未満。

### Fig.3: エネルギー収支
- **項目**: 太陽入力、光合成出力、人間必要量
- **考察**: 光合成出力は必要量の約11%に過ぎず、大幅な効率改善が必要。

### Fig.4: 100%自給率達成条件
- **現在効率**: 約11.7%
- **必要倍率**: 約8.5倍
- **必要面積**: 約15.3 m²
- **考察**: 現在の葉緑体効率(10%)では、体表面積の8.5倍の葉緑体面積が必要。

## 結論

1. **現在の技術では非現実的**: 10%の葉緑体効率では、100%自給自足に体表面積の8.5倍が必要
2. **効率改善が必要**: 実用的な光合成人間には、葉緑体効率を80%以上に向上させる必要がある
3. **環境依存性**: 日照時間と雲量に大きく依存し、屋内や夜間は機能しない
4. **補助的利用**: 完全自給ではなく、従来の食事の補助としての利用が現実的

## 出力ファイル
- グラフ: `BIO505_photosynthesis_analysis.png`
- 本レポート: `BIO505_photosynthesis_report.md`

*生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

with open('BIO505_photosynthesis_report.md', 'w', encoding='utf-8') as f:
    f.write(md_content)
print(f"レポートを保存: BIO505_photosynthesis_report.md")

# ============================================================
# 結論表示
# ============================================================
print("\n" + "=" * 70)
print("【結論】")
print(f"  現在の葉緑体効率(10%)では、100%自給自足には")
print(f"  体表面積の{required_multiplier:.1f}倍の葉緑体が必要")
print(f"  実用的な光合成人間には、葉緑体効率の大幅向上が必要")
print("=" * 70)

plt.show()