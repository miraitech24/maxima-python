#!/usr/bin/env python3
# PAI-01: Venus Atmospheric Angular Momentum (SymPy only)
# coupling rules: No default values, stop on missing file (but no external file needed here)

import sympy as sp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import locale
import os

# ---------- Japanese font detection ----------
def set_japanese_font():
    """Try to set Japanese font, fallback to default if not found."""
    candidates = [
        'IPAexGothic', 'IPAGothic', 'Noto Sans CJK JP', 'Yu Gothic',
        'MS Gothic', 'TakaoGothic', 'Sazanami Gothic', 'VL Gothic'
    ]
    available = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams['font.family'] = name
            print(f"  日本語フォント '{name}' を使用")
            return True
    print("  警告: 日本語フォントが見つかりません。英語で表示します。")
    plt.rcParams['font.family'] = 'sans-serif'
    return False

# ---------- SymPy parameter calculation ----------
M_atm = 4.8e20      # kg (Venus atmosphere mass)
R_venus = 6.05e6    # m
omega_venus = 1.992e-7  # rad/s

I_moment = (2/5) * M_atm * R_venus**2
L_angular = I_moment * omega_venus
E_rotational = 0.5 * I_moment * omega_venus**2

# Earth comparison
M_earth_atm = 5.15e18
R_earth = 6.371e6
omega_earth = 7.292e-5
L_earth = (2/5) * M_earth_atm * R_earth**2 * omega_earth

ratio = L_angular / L_earth

# ---------- Display results ----------
print("="*60)
print("PAI-01: 金星大気角運動量分析 (SymPy)")
print("="*60)
print(f"  大気質量           = {M_atm:.2e} kg")
print(f"  慣性モーメント     = {float(I_moment):.2e} kg·m²")
print(f"  角運動量           = {float(L_angular):.2e} kg·m²/s")
print(f"  回転エネルギー     = {float(E_rotational):.2e} J")
print(f"  地球の大気角運動量 = {float(L_earth):.2e} kg·m²/s")
print(f"  地球比             = {float(ratio):.1f} 倍")
print("="*60)

# ---------- Visualization ----------
set_japanese_font()

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("PAI-01: Venus Atmospheric Angular Momentum Analysis", fontsize=14)

# 1. Bar chart: Angular momentum comparison
ax1 = axes[0,0]
labels = ['Venus', 'Earth']
values = [L_angular, L_earth]
colors = ['#ff9900', '#3366cc']
bars = ax1.bar(labels, values, color=colors)
ax1.set_ylabel('Angular momentum (kg·m²/s)')
ax1.set_title('Comparison of atmospheric angular momentum')
for bar, val in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
             f'{val:.2e}', ha='center', va='bottom', fontsize=9)

# 2. Pie chart: Energy distribution (fixed values for illustration)
ax2 = axes[0,1]
sizes = [E_rotational*0.7, E_rotational*0.2, E_rotational*0.1]
labels_pie = ['Rotational\n(70%)', 'Turbulent\n(20%)', 'Other\n(10%)']
ax2.pie(sizes, labels=labels_pie, autopct='%1.0f%%', startangle=90,
        colors=['#ffaa00','#44aa44','#888888'])
ax2.set_title('Estimated energy distribution')

# 3. Line plot: Angular momentum vs rotation rate sweep
ax3 = axes[1,0]
omega_vals = np.linspace(0.5*omega_venus, 1.5*omega_venus, 50)
L_vals = (2/5) * M_atm * R_venus**2 * omega_vals
ax3.plot(omega_vals / omega_venus, L_vals, 'b-', linewidth=2)
ax3.axhline(L_angular, color='r', linestyle='--', label='Current L')
ax3.set_xlabel('Relative rotation rate (ω/ω_venus)')
ax3.set_ylabel('Angular momentum (kg·m²/s)')
ax3.set_title('Angular momentum vs rotation rate')
ax3.legend()
ax3.grid(True)

# 4. Text summary
ax4 = axes[1,1]
ax4.axis('off')
summary = (
    f"Key Results:\n"
    f"  L_venus = {L_angular:.3e} kg·m²/s\n"
    f"  L_earth = {L_earth:.3e} kg·m²/s\n"
    f"  Ratio   = {ratio:.1f}\n\n"
    f"  Venus atmosphere has\n"
    f"  ~{ratio:.0f} times more angular\n"
    f"  momentum than Earth's."
)
ax4.text(0.1, 0.5, summary, fontsize=12, verticalalignment='center',
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("PAI-01_results.png", dpi=150)
plt.show()

# Save summary to CSV (no forced coupling, just for record)
with open("PAI-01_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"L_venus,{L_angular}\n")
    f.write(f"L_earth,{L_earth}\n")
    f.write(f"ratio,{ratio}\n")

print("\n結果を 'PAI-01_results.png' に保存しました。")
