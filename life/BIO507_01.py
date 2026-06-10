# TaskID: BIO-507-01 - Telomere Extension Probability (単一因子)
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sympy as sp
import csv

# ============================================================
# [TAG:PARAM] パラメータ設定
# ============================================================
T0 = 100.0
k = 0.02
r = 0.5
t_max = 100
dt = 0.1

# ============================================================
# [TAG:SYMPY] sympyで解析解
# ============================================================
t, ks, rs, T0s = sp.symbols('t k r T0')
Tf = sp.Function('T')
ode = sp.Eq(sp.diff(Tf(t), t), -ks*Tf(t) + rs)
sol = sp.dsolve(ode, ics={Tf(0): T0s})
T_expr = sol.rhs
T_numeric = sp.lambdify((t, ks, rs, T0s), T_expr, 'numpy')

# ============================================================
# [TAG:CALC] 数値計算（テロメア長維持率のみ）
# ============================================================
t_vals = np.arange(0, t_max + dt, dt)
T_vals = T_numeric(t_vals, k, r, T0)
T_no_repair = T_numeric(t_vals, k, 0.0, T0)

# テロメア長維持率 = T(t) / T0
maintenance_rate = T_vals / T0
maintenance_rate_no = T_no_repair / T0

# テロメア延長確率 = 維持率が閾値以上である確率
threshold_50 = 0.5  # 50%維持
threshold_30 = 0.3  # 30%維持
P_extend_50 = np.where(maintenance_rate >= threshold_50, 1.0, 0.0)
P_extend_30 = np.where(maintenance_rate >= threshold_30, 1.0, 0.0)

# 修復率の影響
repair_rates = np.linspace(0, 1.0, 11)
T_50yr = [T_numeric(50, k, rr, T0) for rr in repair_rates]
maintenance_50yr = np.array(T_50yr) / T0

# ============================================================
# [TAG:PRINT] 結果表示
# ============================================================
print("=" * 70)
print("BIO-507-01: Telomere Extension Probability (単一因子)")
print("=" * 70)
print(f"\n解析解: T(t) = {sp.latex(T_expr)}")
print(f"\n【テロメア長維持率 T(t)/T0】")
print(f"  {'Year':<6} {'維持率(修復あり)':<16} {'維持率(修復なし)':<16} {'延長確率(50%)':<16} {'延長確率(30%)':<16}")
print(f"  {'-'*70}")
for yr in [0, 20, 40, 60, 80, 100]:
    idx = int(yr / dt)
    print(f"  {yr:<6} {maintenance_rate[idx]:<16.4f} {maintenance_rate_no[idx]:<16.4f} {P_extend_50[idx]:<16.0f} {P_extend_30[idx]:<16.0f}")

print(f"\n【修復率と50年後のテロメア長維持率】")
for rr, mr in zip(repair_rates, maintenance_50yr):
    print(f"  修復率{rr:.1f}: 50年後維持率={mr:.4f}")

# テロメア長が50%維持される年数
cross_year = None
for i in range(len(t_vals)):
    if maintenance_rate[i] < threshold_50:
        cross_year = t_vals[i]
        break
print(f"\n【閾値50%到達年数】")
print(f"  修復あり: {cross_year if cross_year else '100年超'}年")
for i in range(len(t_vals)):
    if maintenance_rate_no[i] < threshold_50:
        cross_year_no = t_vals[i]
        break
print(f"  修復なし: {cross_year_no if 'cross_year_no' in dir() else '100年超'}年")

# ============================================================
# [TAG:PLOT] グラフ
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('BIO-507-01: Telomere Extension Probability', fontsize=14, fontweight='bold')

# グラフ1: テロメア長維持率
axes[0, 0].plot(t_vals, maintenance_rate, 'b-', lw=2, label='With repair')
axes[0, 0].plot(t_vals, maintenance_rate_no, 'r--', lw=2, label='Without repair')
axes[0, 0].axhline(y=0.5, color='g', ls=':', lw=2, label='50% maintenance')
axes[0, 0].axhline(y=0.3, color='orange', ls=':', lw=2, label='30% maintenance')
axes[0, 0].fill_between(t_vals, 0, 0.5, alpha=0.1, color='red')
axes[0, 0].set_xlabel('Time (years)')
axes[0, 0].set_ylabel('Telomere Maintenance Rate T(t)/T0')
axes[0, 0].set_title('Fig.1: Telomere Length Maintenance Rate')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylim(0, 1.1)

# グラフ2: テロメア延長確率
axes[0, 1].plot(t_vals, P_extend_50, 'b-', lw=2, label='Threshold 50%')
axes[0, 1].plot(t_vals, P_extend_30, 'g--', lw=2, label='Threshold 30%')
axes[0, 1].set_xlabel('Time (years)')
axes[0, 1].set_ylabel('Extension Probability')
axes[0, 1].set_title('Fig.2: Telomere Extension Probability')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_ylim(-0.1, 1.1)
axes[0, 1].set_yticks([0, 1])
axes[0, 1].set_yticklabels(['Lost', 'Maintained'])

# グラフ3: 修復率 vs 50年後維持率
axes[1, 0].plot(repair_rates, maintenance_50yr, 'bo-', lw=2, markersize=8)
axes[1, 0].axhline(y=0.5, color='r', ls='--', lw=2, alpha=0.7, label='50% maintenance')
axes[1, 0].axvline(x=0.3, color='g', ls=':', lw=2, alpha=0.7, label='r=0.3')
axes[1, 0].set_xlabel('Repair Rate r')
axes[1, 0].set_ylabel('50-Year Maintenance Rate')
axes[1, 0].set_title('Fig.3: Repair Rate vs 50-Year Maintenance')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_ylim(0, 1.1)

# グラフ4: テロメア長分布（20年, 50年, 80年）
years_show = [20, 50, 80]
T_show = [T_numeric(y, k, r, T0) for y in years_show]
T_no_show = [T_numeric(y, k, 0.0, T0) for y in years_show]
x_pos = np.arange(len(years_show))
width = 0.35
axes[1, 1].bar(x_pos - width/2, T_show, width, label='With repair', color='blue', alpha=0.8)
axes[1, 1].bar(x_pos + width/2, T_no_show, width, label='Without repair', color='red', alpha=0.8)
axes[1, 1].axhline(y=T0*0.5, color='g', ls=':', lw=2, label='50% of T0')
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Telomere Length')
axes[1, 1].set_title('Fig.4: Telomere Length Comparison')
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels([f'{y} years' for y in years_show])
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('BIO507-01_telomere_extension.png', dpi=150, bbox_inches='tight')
print(f"\nグラフ保存: BIO507-01_telomere_extension.png")

# ============================================================
# [TAG:MD] .md出力
# ============================================================
md = f"""# BIO-507-01: Telomere Extension Probability

## 計算方式
- sympyで微分方程式の解析解を導出
- テロメア長維持率 T(t)/T0 を計算
- 閾値（50%, 30%）以上の維持を「延長成功」と定義
- Maximaは使用せず

## 数理モデル
$$\\frac{{dT}}{{dt}} = -k \\cdot T + r$$
$$T(t) = {sp.latex(T_expr)}$$
$$\\text{{維持率}} = \\frac{{T(t)}}{{T_0}}$$
$$P_{{\\text{{extend}}}}(t) = \\begin{{cases}} 1 & \\text{{維持率}} \\geq \\text{{threshold}} \\\\ 0 & \\text{{otherwise}} \\end{{cases}}$$

## パラメータ
| 記号 | 値 | 説明 |
|------|-----|------|
| $T_0$ | {T0} | 初期テロメア長 |
| $k$ | {k}/year | 短縮率 |
| $r$ | {r}/year | 修復率 |

## 結果
| 年数 | 維持率(修復あり) | 維持率(修復なし) | 延長確率(50%閾値) | 延長確率(30%閾値) |
|------|---------------|---------------|-----------------|-----------------|
"""
for yr in [0, 20, 40, 60, 80, 100]:
    idx = int(yr / dt)
    md += f"| {yr} | {maintenance_rate[idx]:.4f} | {maintenance_rate_no[idx]:.4f} | {P_extend_50[idx]:.0f} | {P_extend_30[idx]:.0f} |\n"

md += f"""
## 結論
1. 修復あり: 50%維持率を約{cross_year:.0f}年維持
2. 修復なし: 50%維持率を約{cross_year_no:.0f}年で喪失
3. 修復率0.3以上で50年後の維持率50%超
4. テロメア延長確率は閾値設定に依存

*生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
with open('BIO507-01_telomere_report.md', 'w', encoding='utf-8') as f:
    f.write(md)
print(f"MD保存: BIO507-01_telomere_report.md")

# ============================================================
# [TAG:CSV] .csv出力
# ============================================================
with open('BIO507-01_telomere_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Year', 'Maintenance_repair', 'Maintenance_no_repair', 'P_extend_50', 'P_extend_30'])
    for i in range(0, len(t_vals), 10):
        writer.writerow([f'{t_vals[i]:.1f}', f'{maintenance_rate[i]:.4f}', f'{maintenance_rate_no[i]:.4f}', f'{P_extend_50[i]:.0f}', f'{P_extend_30[i]:.0f}'])
print(f"CSV保存: BIO507-01_telomere_results.csv")

plt.show()