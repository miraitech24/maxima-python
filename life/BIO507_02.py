# TaskID: BIO-507-02 - Mitochondrial Function Preservation Rate
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sympy as sp
import csv

# ============================================================
# [TAG:PARAM] パラメータ設定
# ============================================================
# ミトコンドリア機能パラメータ
ATP_base = 100.0       # 初期ATP産生量
ROS_base = 10.0        # 初期ROS産生量
decay_rate = 0.015     # 機能低下率 (/year)
repair_rate = 0.3      # 修復率 (/year)
ROS_growth = 0.02      # ROS増加率 (/year)
antioxidant = 0.4      # 抗酸化能力
t_max = 100
dt = 0.1

# ============================================================
# [TAG:SYMPY] sympyで解析解
# ============================================================
t, k, r, A0 = sp.symbols('t k r A0')
Af = sp.Function('A')
ode_ATP = sp.Eq(sp.diff(Af(t), t), -k*Af(t) + r)
sol_ATP = sp.dsolve(ode_ATP, ics={Af(0): A0})
ATP_expr = sol_ATP.rhs
ATP_func = sp.lambdify((t, k, r, A0), ATP_expr, 'numpy')

t, g, R0 = sp.symbols('t g R0')
Rf = sp.Function('R')
ode_ROS = sp.Eq(sp.diff(Rf(t), t), g*Rf(t))
sol_ROS = sp.dsolve(ode_ROS, ics={Rf(0): R0})
ROS_expr = sol_ROS.rhs
ROS_func = sp.lambdify((t, g, R0), ROS_expr, 'numpy')

# ============================================================
# [TAG:CALC] 数値計算
# ============================================================
t_vals = np.arange(0, t_max + dt, dt)

# ATP産生量
ATP_vals = ATP_func(t_vals, decay_rate, repair_rate, ATP_base)
ATP_no_repair = ATP_func(t_vals, decay_rate, 0.0, ATP_base)

# ROS産生量
ROS_vals = ROS_func(t_vals, ROS_growth, ROS_base)
ROS_reduced = ROS_func(t_vals, ROS_growth * (1 - antioxidant), ROS_base)

# ミトコンドリア機能維持率
func_maintenance = ATP_vals / ATP_base
func_maintenance_no = ATP_no_repair / ATP_base

# ROS除去率
ROS_removal = 1 - (ROS_reduced / ROS_vals)
ROS_removal = np.clip(ROS_removal, 0, 1)

# 総合ミトコンドリア機能スコア
mito_score = 0.6 * func_maintenance + 0.4 * (1 - ROS_reduced / np.maximum(ROS_reduced, 1))
mito_score_no = 0.6 * func_maintenance_no + 0.4 * (1 - ROS_vals / np.maximum(ROS_vals, 1))

# ============================================================
# [TAG:PRINT] 結果表示
# ============================================================
print("=" * 70)
print("BIO-507-02: Mitochondrial Function Preservation Rate")
print("=" * 70)
print(f"\n解析解(ATP): {sp.latex(ATP_expr)}")
print(f"解析解(ROS): {sp.latex(ROS_expr)}")

print(f"\n【ミトコンドリア機能維持率】")
print(f"  {'Year':<6} {'ATP(修復)':<12} {'ATP(なし)':<12} {'ROS(通常)':<12} {'ROS(低減)':<12} {'機能スコア':<12}")
print(f"  {'-'*66}")
for yr in [0, 20, 40, 60, 80, 100]:
    idx = int(yr / dt)
    print(f"  {yr:<6} {ATP_vals[idx]:<12.2f} {ATP_no_repair[idx]:<12.2f} {ROS_vals[idx]:<12.2f} {ROS_reduced[idx]:<12.2f} {mito_score[idx]:<12.4f}")

print(f"\n【抗酸化能力とROS除去率（50年後）】")
for antiox in np.linspace(0, 1, 6):
    ROS_r = ROS_func(50, ROS_growth * (1 - antiox), ROS_base)
    removal = 1 - ROS_r / ROS_func(50, ROS_growth, ROS_base)
    print(f"  抗酸化{antiox:.2f}: ROS除去率={removal:.4f}")

print(f"\n【修復率と50年後ATP維持率】")
for rr in np.linspace(0, 1, 6):
    ATP_50 = ATP_func(50, decay_rate, rr, ATP_base)
    print(f"  修復率{rr:.2f}: ATP維持率={ATP_50/ATP_base:.4f}")

# ============================================================
# [TAG:PLOT] グラフ
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('BIO-507-02: Mitochondrial Function Preservation Analysis', fontsize=14, fontweight='bold')

# グラフ1: ATP産生量
axes[0, 0].plot(t_vals, ATP_vals, 'b-', lw=2, label='With repair')
axes[0, 0].plot(t_vals, ATP_no_repair, 'r--', lw=2, label='Without repair')
axes[0, 0].axhline(y=ATP_base*0.5, color='g', ls=':', lw=2, label='50% of base')
axes[0, 0].fill_between(t_vals, 0, ATP_base*0.5, alpha=0.1, color='red')
axes[0, 0].set_xlabel('Time (years)')
axes[0, 0].set_ylabel('ATP Production')
axes[0, 0].set_title('Fig.1: ATP Production Dynamics')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].text(0.5, 0.05, f'$A(t) = {sp.latex(ATP_expr)}$',
                transform=axes[0, 0].transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                ha='center', va='bottom')

# グラフ2: ROS産生量
axes[0, 1].plot(t_vals, ROS_vals, 'r-', lw=2, label='Normal')
axes[0, 1].plot(t_vals, ROS_reduced, 'g--', lw=2, label='With antioxidant')
axes[0, 1].fill_between(t_vals, 0, ROS_vals, alpha=0.1, color='red')
axes[0, 1].set_xlabel('Time (years)')
axes[0, 1].set_ylabel('ROS Production')
axes[0, 1].set_title('Fig.2: ROS Production Dynamics')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].text(0.5, 0.05, f'$R(t) = {sp.latex(ROS_expr)}$',
                transform=axes[0, 1].transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                ha='center', va='bottom')

# グラフ3: ミトコンドリア機能スコア
axes[1, 0].plot(t_vals, mito_score, 'b-', lw=2, label='With intervention')
axes[1, 0].plot(t_vals, mito_score_no, 'r--', lw=2, label='Without intervention')
axes[1, 0].axhline(y=0.5, color='g', ls=':', lw=2, alpha=0.7, label='50% threshold')
axes[1, 0].set_xlabel('Time (years)')
axes[1, 0].set_ylabel('Mitochondrial Function Score')
axes[1, 0].set_title('Fig.3: Overall Mitochondrial Function Score')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_ylim(0, 1.1)

# グラフ4: 修復率と抗酸化能力の影響
rr_vals = np.linspace(0, 1, 50)
antiox_vals = np.linspace(0, 1, 50)
score_50 = []
for rr, ao in zip(rr_vals, antiox_vals):
    ATP_50 = ATP_func(50, decay_rate, rr, ATP_base)
    ROS_50 = ROS_func(50, ROS_growth * (1 - ao), ROS_base)
    score = 0.6 * (ATP_50/ATP_base) + 0.4 * (1 - ROS_50/ROS_func(50, ROS_growth, ROS_base))
    score_50.append(score)

X, Y = np.meshgrid(rr_vals, antiox_vals)
Z = np.array([[0.6 * (ATP_func(50, decay_rate, rr, ATP_base)/ATP_base) +
               0.4 * (1 - ROS_func(50, ROS_growth*(1-ao), ROS_base)/ROS_func(50, ROS_growth, ROS_base))
               for rr in rr_vals] for ao in antiox_vals])
contour = axes[1, 1].contourf(X, Y, Z, levels=20, cmap='viridis')
axes[1, 1].set_xlabel('Repair Rate')
axes[1, 1].set_ylabel('Antioxidant Capacity')
axes[1, 1].set_title('Fig.4: 50-Year Function Score Contour')
plt.colorbar(contour, ax=axes[1, 1], label='Function Score')

plt.tight_layout()
plt.savefig('BIO507-02_mitochondrial_analysis.png', dpi=150, bbox_inches='tight')
print(f"\nグラフ保存: BIO507-02_mitochondrial_analysis.png")

# ============================================================
# [TAG:MD] .md出力
# ============================================================
md = f"""# BIO-507-02: Mitochondrial Function Preservation Rate

## 計算方式
- sympyで微分方程式の解析解を導出
- ATP産生: $dA/dt = -kA + r$
- ROS産生: $dR/dt = gR$
- 総合スコア: $S = 0.6 \\cdot A/A_0 + 0.4 \\cdot (1 - R/R_{{\\max}})$
- Maximaは使用せず

## 数理モデル
$$\\frac{{dA}}{{dt}} = -k \\cdot A + r$$
$$A(t) = {sp.latex(ATP_expr)}$$
$$\\frac{{dR}}{{dt}} = g \\cdot R$$
$$R(t) = {sp.latex(ROS_expr)}$$

## パラメータ
| 記号 | 値 | 説明 |
|------|-----|------|
| $A_0$ | {ATP_base} | 初期ATP産生量 |
| $R_0$ | {ROS_base} | 初期ROS産生量 |
| $k$ | {decay_rate}/year | 機能低下率 |
| $r$ | {repair_rate}/year | 修復率 |
| $g$ | {ROS_growth}/year | ROS増加率 |
| $\\alpha$ | {antioxidant} | 抗酸化能力 |

## 結果
| 年数 | ATP(修復) | ATP(なし) | ROS(通常) | ROS(低減) | 機能スコア |
|------|---------|---------|---------|---------|---------|
"""
for yr in [0, 20, 40, 60, 80, 100]:
    idx = int(yr / dt)
    md += f"| {yr} | {ATP_vals[idx]:.2f} | {ATP_no_repair[idx]:.2f} | {ROS_vals[idx]:.2f} | {ROS_reduced[idx]:.2f} | {mito_score[idx]:.4f} |\n"

md += f"""
## 結論
1. ATP産生: 修復ありで約{ATP_vals[-1]/ATP_base*100:.0f}%維持、なしで{ATP_no_repair[-1]/ATP_base*100:.0f}%に低下
2. ROS: 抗酸化能力なしで指数関数的増加、ありで増加抑制
3. 総合スコア: 介入ありで{mito_score[-1]:.2f}、なしで{mito_score_no[-1]:.2f}
4. 最適戦略: 修復率0.3以上 + 抗酸化能力0.4以上で機能維持

*生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
with open('BIO507-02_mitochondrial_report.md', 'w', encoding='utf-8') as f:
    f.write(md)
print(f"MD保存: BIO507-02_mitochondrial_report.md")

# ============================================================
# [TAG:CSV] .csv出力
# ============================================================
with open('BIO507-02_mitochondrial_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Year', 'ATP_repair', 'ATP_no_repair', 'ROS_normal', 'ROS_reduced', 'Mito_Score'])
    for i in range(0, len(t_vals), 10):
        writer.writerow([f'{t_vals[i]:.1f}', f'{ATP_vals[i]:.2f}', f'{ATP_no_repair[i]:.2f}',
                        f'{ROS_vals[i]:.2f}', f'{ROS_reduced[i]:.2f}', f'{mito_score[i]:.4f}'])
print(f"CSV保存: BIO507-02_mitochondrial_results.csv")

plt.show()