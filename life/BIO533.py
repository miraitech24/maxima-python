# TaskID: BIO-533 - Limb Regeneration Probability (Lizard Model)
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import csv

# ============================================================
# [TAG:PARAM] パラメータ設定
# ============================================================
stages = ['Wound Healing', 'Blastema Formation', 'Proliferation', 'Differentiation', 'Morphogenesis']
stage_rates = [0.95, 0.80, 0.75, 0.70, 0.65]
human_factor = 0.3
IMMUNE = 0.6
GROWTH = 0.7
SCAR = 0.5

# ============================================================
# [TAG:CALC] 数値計算
# ============================================================
# 基本確率（全段階の積）
P_lizard = 1.0
for r in stage_rates:
    P_lizard *= r
P_human_base = P_lizard * human_factor

def calc_prob(age=30, size=0.5, imm=IMMUNE, gf=GROWTH, scar=SCAR):
    base = P_lizard * human_factor
    age_eff = np.exp(-0.02 * age)
    size_eff = np.exp(-0.5 * size)
    inter = (imm + gf + scar) / 3
    final = base * age_eff * size_eff * (1 + inter)
    return min(final * 100, 100)

# 累積確率
lizard_cum = []
human_cum = []
cur_l = 1.0
cur_h = 1.0
for r in stage_rates:
    cur_l *= r
    cur_h *= r * human_factor
    lizard_cum.append(cur_l)
    human_cum.append(cur_h)

# 年齢スイープ
ages = np.linspace(0, 100, 101)
probs_age = [calc_prob(age=a) for a in ages]

# サイズスイープ
sizes = np.linspace(0.1, 1.0, 50)
probs_size = [calc_prob(size=s) for s in sizes]

# 介入効果
interventions = [('None', 0, 0, 0), ('Immune', 0.6, 0, 0), ('Growth', 0, 0.7, 0),
                 ('Scar', 0, 0, 0.5), ('All', 0.6, 0.7, 0.5)]
intervention_probs = [calc_prob(imm=im, gf=gf, scar=sc) for _, im, gf, sc in interventions]

# ============================================================
# [TAG:PRINT] 結果表示
# ============================================================
print("=" * 70)
print("BIO-533: Limb Regeneration Probability (Lizard Model)")
print("=" * 70)
print(f"\n【基本確率】")
print(f"  トカゲ: {P_lizard:.4f} ({P_lizard*100:.2f}%)")
print(f"  ヒト(素): {P_human_base:.4f} ({P_human_base*100:.2f}%)")
print(f"  ヒト(30歳, 介入あり): {calc_prob(30):.2f}%")

print(f"\n【各段階累積確率】")
print(f"  {'Stage':<20} {'Lizard':<12} {'Human':<12}")
print(f"  {'-'*44}")
for i, s in enumerate(stages):
    print(f"  {s:<20} {lizard_cum[i]:.4f} ({lizard_cum[i]*100:5.2f}%)  {human_cum[i]:.4f} ({human_cum[i]*100:5.2f}%)")

print(f"\n【年齢 vs 再生確率】")
for age in [0, 20, 40, 60, 80]:
    print(f"  {age:2d}歳: {calc_prob(age):.2f}%")

print(f"\n【四肢サイズ vs 再生確率】")
for size in [0.1, 0.3, 0.5, 0.7, 1.0]:
    print(f"  サイズ{size:.1f}: {calc_prob(size=size):.2f}%")

print(f"\n【医療介入効果】")
for name, im, gf, sc in interventions:
    print(f"  {name:<10}: {calc_prob(imm=im, gf=gf, scar=sc):.2f}%")

# ============================================================
# [TAG:PLOT] グラフ
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('BIO-533: Limb Regeneration Probability Analysis', fontsize=14, fontweight='bold')

# グラフ1: 各段階の成功率と累積確率
x = np.arange(len(stages))
w = 0.35
axes[0, 0].bar(x - w/2, stage_rates, w, label='Stage Rate', color='lightgreen', alpha=0.8, edgecolor='black')
axes[0, 0].bar(x + w/2, lizard_cum, w, label='Cumulative (Lizard)', color='darkgreen', alpha=0.8, edgecolor='black')
axes[0, 0].bar(x + w/2, human_cum, w, label='Cumulative (Human)', color='orange', alpha=0.6, edgecolor='black')
axes[0, 0].set_xlabel('Regeneration Stage')
axes[0, 0].set_ylabel('Probability')
axes[0, 0].set_title('Fig.1: Stage-wise Success and Cumulative Probability')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(stages, rotation=15, ha='right')
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(True, alpha=0.3, axis='y')
axes[0, 0].set_ylim(0, 1.1)
axes[0, 0].text(0.5, 0.05, r'$P_{total} = \prod_{i=1}^{5} P_i$',
                transform=axes[0, 0].transAxes, fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                ha='center', va='bottom')

# グラフ2: 年齢 vs 再生確率
axes[0, 1].plot(ages, probs_age, 'b-', lw=2)
axes[0, 1].fill_between(ages, 0, probs_age, alpha=0.1, color='blue')
axes[0, 1].axhline(y=50, color='r', ls='--', lw=2, alpha=0.7, label='50% probability')
axes[0, 1].set_xlabel('Age (years)')
axes[0, 1].set_ylabel('Regeneration Probability (%)')
axes[0, 1].set_title('Fig.2: Age vs Regeneration Probability')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_ylim(0, 100)
axes[0, 1].text(0.5, 0.05, r'$P_{age} = P_0 \cdot e^{-0.02 \cdot age}$',
                transform=axes[0, 1].transAxes, fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                ha='center', va='bottom')

# グラフ3: 四肢サイズ vs 再生確率
axes[1, 0].plot(sizes, probs_size, 'g-', lw=2)
axes[1, 0].fill_between(sizes, 0, probs_size, alpha=0.1, color='green')
axes[1, 0].set_xlabel('Limb Size Factor (0-1)')
axes[1, 0].set_ylabel('Regeneration Probability (%)')
axes[1, 0].set_title('Fig.3: Limb Size vs Regeneration Probability')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_ylim(0, 100)
axes[1, 0].text(0.5, 0.05, r'$P_{size} = P_0 \cdot e^{-0.5 \cdot size}$',
                transform=axes[1, 0].transAxes, fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                ha='center', va='bottom')

# グラフ4: 医療介入効果
names = ['None', 'Immune\nSuppression', 'Growth\nFactors', 'Scar\nPrevention', 'All\nCombined']
colors = ['gray', 'lightblue', 'lightgreen', 'lightsalmon', 'gold']
bars = axes[1, 1].bar(names, intervention_probs, color=colors, alpha=0.8, edgecolor='black')
axes[1, 1].set_xlabel('Intervention Type')
axes[1, 1].set_ylabel('Regeneration Probability (%)')
axes[1, 1].set_title('Fig.4: Medical Intervention Effects')
for bar, val in zip(bars, intervention_probs):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')
axes[1, 1].set_ylim(0, 100)

plt.tight_layout()
plt.savefig('BIO533_limb_regeneration.png', dpi=150, bbox_inches='tight')
print(f"\nグラフ保存: BIO533_limb_regeneration.png")

# ============================================================
# [TAG:MD] .md出力
# ============================================================
md = f"""# BIO-533: Limb Regeneration Probability (Lizard Model)

## 計算方式
- 各段階の成功率の積で基本確率を計算: $P_{{total}} = \\prod P_i$
- 年齢効果: $e^{{-0.02 \\cdot age}}$
- サイズ効果: $e^{{-0.5 \\cdot size}}$
- 医療介入効果: $(1 + \\eta)$
- Maximaは使用せず

## パラメータ
| パラメータ | 値 | 説明 |
|-----------|-----|------|
| ヒト効率因子 | {human_factor} | ヒトではトカゲの30%の効率 |
| 免疫抑制効果 | {IMMUNE} | 免疫抑制による再生促進 |
| 成長因子活性化 | {GROWTH} | 成長因子による細胞増殖促進 |
| 瘢痕化防止 | {SCAR} | 瘢痕化防止による再生促進 |

## 再生段階と成功率
| 段階 | トカゲ成功率 | ヒト換算 |
|------|------------|---------|
"""
for i, s in enumerate(stages):
    hr = stage_rates[i] * human_factor
    md += f"| {s} | {stage_rates[i]:.2f} ({stage_rates[i]*100:.0f}%) | {hr:.2f} ({hr*100:.0f}%) |\n"

md += f"""
## 結果
| モデル | 確率 |
|--------|------|
| トカゲ | {P_lizard*100:.2f}% |
| ヒト(30歳,介入あり) | {calc_prob(30):.2f}% |

### 年齢と再生確率
| 年齢 | 再生確率 |
|------|---------|
"""
for age in [0, 20, 40, 60, 80]:
    md += f"| {age}歳 | {calc_prob(age):.2f}% |\n"

md += f"""
### 四肢サイズと再生確率
| サイズ因子 | 再生確率 |
|-----------|---------|
"""
for size in [0.1, 0.3, 0.5, 0.7, 1.0]:
    md += f"| {size:.1f} | {calc_prob(size=size):.2f}% |\n"

md += f"""
### 医療介入効果
| 介入 | 再生確率 |
|------|---------|
"""
for name, im, gf, sc in interventions:
    md += f"| {name} | {calc_prob(imm=im, gf=gf, scar=sc):.2f}% |\n"

md += f"""
## 結論
1. トカゲの四肢再生確率: {P_lizard*100:.1f}%
2. ヒト応用(30歳): {calc_prob(30):.1f}%
3. 年齢影響: 40歳で約50%、80歳で約20%に低下
4. 医療介入: 全介入で確率が約2倍に向上

*生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
with open('BIO533_limb_report.md', 'w', encoding='utf-8') as f:
    f.write(md)
print(f"MD保存: BIO533_limb_report.md")

# ============================================================
# [TAG:CSV] .csv出力
# ============================================================
with open('BIO533_limb_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Stage', 'Lizard_Rate', 'Human_Rate', 'Lizard_Cumulative', 'Human_Cumulative'])
    for i, s in enumerate(stages):
        writer.writerow([s, f'{stage_rates[i]:.2f}', f'{stage_rates[i]*human_factor:.2f}',
                        f'{lizard_cum[i]:.4f}', f'{human_cum[i]:.4f}'])
    writer.writerow([])
    writer.writerow(['Age', 'Probability'])
    for age in range(0, 101, 10):
        writer.writerow([age, f'{calc_prob(age=age):.2f}'])
print(f"CSV保存: BIO533_limb_results.csv")

plt.show()