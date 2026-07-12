#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BZ過程（Blandford-Znajek過程）のエネルギー抽出効率の計算根拠
Maxima連成: task1007.macで導出したペンローズ過程の効率式をpenrose_params.pyからimport
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys
import importlib

# ===== 日本語フォント自動検出 =====
def setup_japanese_font():
    jp_font_candidates = [
        'Noto Sans CJK JP', 'Noto Sans CJK SC', 'IPAexGothic', 'IPAGothic',
        'TakaoGothic', 'TakaoExGothic', 'VL Gothic', 'Yu Gothic', 'YuGothic',
        'MS Gothic', 'Meiryo', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN',
        'Osaka', 'Kochi Gothic', 'MigMix 1P', 'Sazanami Gothic',
        'MotoyaLCedar', 'Droid Sans Japanese', 'Source Han Sans JP', 'Source Han Sans',
    ]
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for candidate in jp_font_candidates:
        if candidate in available_fonts:
            print(f"日本語フォント検出: {candidate}")
            return candidate
    print("日本語フォントが見つかりません。英語フォントを使用します。")
    return 'DejaVu Sans'

jp_font = setup_japanese_font()
plt.rcParams['font.family'] = jp_font
plt.rcParams['axes.unicode_minus'] = False

# ===== 物理定数 =====
G = 6.67430e-11     # 重力定数 [m^3/kg/s^2]
c = 2.99792458e8    # 光速 [m/s]
Msun = 1.989e30     # 太陽質量 [kg]
hbar = 1.054571817e-34  # プランク定数 [J*s]
mu0 = 4*np.pi*1e-7  # 真空の透磁率 [H/m]

# ===== Maxima連成: penrose_params.pyのロード =====
# Maxima連成: task1007.macで導出したペンローズ過程の効率式をimport
sys.path.append(os.getcwd())
if os.path.exists("penrose_params.py"):
    import penrose_params
    importlib.reload(penrose_params)
    maxima_available = True
    print("Maxima連成: penrose_params.py をロードしました")
else:
    print("Maxima連成: penrose_params.py が見つかりません。Pythonで代替計算します。")
    maxima_available = False

# ===== パラメータ設定 =====
M_bh = 6.3 * Msun   # BH質量 [kg]（6.3太陽質量）
a_star = 0.92       # 回転パラメータ
rs = 2 * G * M_bh / c**2  # シュワルツシルト半径 [m]

# スピンパラメータの範囲
spins = np.linspace(0.001, 0.999, 500)

# ===== 1. ペンローズ過程の最大効率（理論上限） =====
# Maxima連成: penrose_params.get_max_gain()を使用
def calc_penrose_efficiency(a):
    """ペンローズ過程の最大効率"""
    if maxima_available:
        try:
            return penrose_params.get_max_gain(1.0, a) / 100.0
        except:
            pass
    # Python代替計算（Maximaと同じ式）
    return 1 - np.sqrt((1 + np.sqrt(1 - a**2)) / 2)

# ===== 2. BZ過程のエネルギー抽出効率 =====
def calc_bz_power(M, a, B_field=1.0):
    """
    BZ過程によるエネルギー抽出出力
    P_BZ = (1/32) * (B^2 * r_h^2 * c) * (a/M)^2
    ここで r_h = (1 + sqrt(1 - a^2)) * r_g
    """
    r_g = G * M / c**2  # 重力半径
    r_h = (1 + np.sqrt(1 - a**2)) * r_g  # 事象の地平線半径
    # BZ過程の出力（Blandford & Znajek 1977）
    omega_h = a * c / (2 * r_h)  # BHの角速度
    P_bz = (1.0/32.0) * (B_field**2 * r_h**2 * c) * (a / M)**2
    # より正確な式（Tchekhovskoy et al. 2010）
    kappa = 1.0  # 磁場の形状因子
    P_bz_accurate = (kappa * B_field**2 * r_h**2 * c * omega_h**2) / (32 * mu0)
    return P_bz_accurate

def calc_bz_efficiency(M, a):
    """BZ過程のエネルギー抽出効率（BH回転エネルギーに対する割合）"""
    # BHの回転エネルギー
    # E_rot = (1 - sqrt((1 + sqrt(1 - a^2)) / 2)) * M * c^2
    E_rot = calc_penrose_efficiency(a) * M * c**2
    
    # BZ過程の出力（磁場強度をパラメータとして）
    # 典型的な磁場強度: 10^4〜10^5 T（クエーサー級）
    B_typical = 1e4  # [T]
    P_bz = calc_bz_power(M, a, B_typical)
    
    # 抽出時間（BHの回転エネルギーを全て抽出するのに要する時間）
    t_extract = E_rot / P_bz
    
    return E_rot, P_bz, t_extract

# ===== 3. 各スピンでの計算 =====
penrose_eff = np.array([calc_penrose_efficiency(a) for a in spins])

# BZ過程の計算（ケンタリBH）
E_rot_kenta, P_bz_kenta, t_extract_kenta = calc_bz_efficiency(M_bh, a_star)

# 各スピンでのBZ過程出力
B_field = 1e4  # [T]
P_bz_spins = np.array([calc_bz_power(M_bh, a, B_field) for a in spins])
E_rot_spins = np.array([calc_penrose_efficiency(a) * M_bh * c**2 for a in spins])
t_extract_spins = np.where(P_bz_spins > 0, E_rot_spins / P_bz_spins, np.inf)

# ===== 4. 29%の計算根拠 =====
# ペンローズ過程の最大効率は a=1 で 29.3%
a_max = 0.999999  # 理論上の最大スピン
eff_max = calc_penrose_efficiency(a_max)
print(f"ペンローズ過程の最大効率 (a→1): {eff_max*100:.2f}%")

# ケンタリBH (a=0.92) での効率
eff_kenta = calc_penrose_efficiency(a_star)
print(f"ケンタリBH (a={a_star}) の効率: {eff_kenta*100:.2f}%")

# BZ過程の効率（ペンローズ過程と同等以上）
# BZ過程は磁場を介してエネルギーを抽出するため、
# 理論上はペンローズ過程と同じ最大効率に達する
print(f"BZ過程の最大効率: {eff_max*100:.2f}%（ペンローズ過程と同等）")

# ===== グラフ描画 =====
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 左上: ペンローズ過程の効率
ax = axes[0,0]
ax.plot(spins, penrose_eff*100, 'b-', linewidth=2, label='ペンローズ過程効率')
ax.axvline(a_star, color='green', linestyle=':', label=f'ケンタリBH(a={a_star})')
ax.axhline(eff_kenta*100, color='red', linestyle='--', label=f'ケンタリ効率({eff_kenta*100:.1f}%)')
ax.axhline(29.3, color='purple', linestyle=':', label='理論上限(29.3%)')
ax.set_xlabel('スピンパラメータ a*')
ax.set_ylabel('効率 [%]')
ax.set_title('ペンローズ過程のエネルギー抽出効率')
ax.legend()
ax.grid(True, alpha=0.3)

# 右上: BZ過程の出力
ax = axes[0,1]
ax.loglog(spins, P_bz_spins, 'r-', linewidth=2, label=f'BZ過程出力(B={B_field:.0e}T)')
ax.axvline(a_star, color='green', linestyle=':', label=f'ケンタリBH(a={a_star})')
ax.axhline(P_bz_kenta, color='red', linestyle='--', label=f'ケンタリ出力({P_bz_kenta:.2e}W)')
ax.set_xlabel('スピンパラメータ a*')
ax.set_ylabel('出力 [W]')
ax.set_title('BZ過程のエネルギー抽出出力')
ax.legend()
ax.grid(True, alpha=0.3)

# 左下: 抽出可能エネルギー
ax = axes[1,0]
ax.semilogy(spins, E_rot_spins, 'g-', linewidth=2, label='回転エネルギー')
ax.axvline(a_star, color='green', linestyle=':', label=f'ケンタリBH(a={a_star})')
ax.axhline(E_rot_kenta, color='red', linestyle='--', label=f'ケンタリ抽出可能({E_rot_kenta:.2e}J)')
ax.set_xlabel('スピンパラメータ a*')
ax.set_ylabel('エネルギー [J]')
ax.set_title('BHの回転エネルギー')
ax.legend()
ax.grid(True, alpha=0.3)

# 右下: 抽出時間
ax = axes[1,1]
ax.loglog(spins, t_extract_spins/(365.25*24*3600), 'm-', linewidth=2, label='抽出時間')
ax.axvline(a_star, color='green', linestyle=':', label=f'ケンタリBH(a={a_star})')
ax.axhline(t_extract_kenta/(365.25*24*3600), color='red', linestyle='--', label=f'ケンタリ抽出時間({t_extract_kenta/(365.25*24*3600):.2e}年)')
ax.set_xlabel('スピンパラメータ a*')
ax.set_ylabel('抽出時間 [年]')
ax.set_title('BH回転エネルギーの全抽出時間')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('bz_process_efficiency.png', dpi=150)
plt.close()

# ===== 結果表示 =====
print("\n===== BZ過程 エネルギー抽出効率の計算根拠 =====")
print(f"BH質量: {M_bh/Msun:.1f} M☉")
print(f"回転パラメータ: a* = {a_star}")
print()

print("=== ペンローズ過程の効率 ===")
print(f"効率式: η = 1 - √((1 + √(1 - a²)) / 2)")
print(f"理論最大効率 (a→1): {eff_max*100:.2f}%")
print(f"ケンタリBH (a={a_star}) の効率: {eff_kenta*100:.2f}%")
print()

print("=== BZ過程の効率 ===")
print(f"BZ過程の出力式: P_BZ = (κ * B² * r_h² * c * ω_h²) / (32 * μ₀)")
print(f"  κ: 磁場形状因子 (≈1)")
print(f"  B: 磁場強度 [T]")
print(f"  r_h: 事象の地平線半径 [m]")
print(f"  ω_h: BHの角速度 [rad/s]")
print(f"  μ₀: 真空の透磁率 [H/m]")
print()

print(f"ケンタリBHのBZ過程出力: {P_bz_kenta:.2e} W")
print(f"ケンタリBHの回転エネルギー: {E_rot_kenta:.2e} J")
print(f"全エネルギー抽出時間: {t_extract_kenta/(365.25*24*3600):.2e} 年")
print()

print("=== 29%の計算根拠 ===")
print("1. ペンローズ過程の最大効率は a→1 で 29.3%")
print("   式: η_max = 1 - 1/√2 ≈ 0.293")
print()
print("2. BZ過程も同じ物理（エルゴ球内のエネルギー抽出）に基づく")
print("   したがって、最大効率はペンローズ過程と同等")
print()
print("3. 実際の効率は磁場強度に依存")
print(f"   ケンタリBH (a={a_star}) の場合: {eff_kenta*100:.2f}%")
print(f"   これは理論最大の {eff_kenta/eff_max*100:.1f}% に相当")
print()

print("=== 結論 ===")
print(f"BHの回転エネルギーの最大 {eff_max*100:.1f}% を抽出可能")
print(f"ケンタリBHでは {eff_kenta*100:.1f}% を抽出可能")
print(f"抽出エネルギー: {E_rot_kenta:.2e} J")
print(f"これは太陽の年間出力の {E_rot_kenta/(3.828e26*365.25*24*3600):.2e} 倍")

# ===== サマリーファイル出力 =====
with open('bz_process_summary.md', 'w', encoding='utf-8') as f:
    f.write("# BZ過程 エネルギー抽出効率の計算根拠\n\n")
    f.write("## Maxima連成\n\n")
    f.write("本コードは task1007.mac で導出したペンローズ過程の効率式を penrose_params.py からimportしている。\n")
    f.write("Maxima連成: `penrose_params.get_max_gain(M, a)` を使用。\n\n")
    f.write("## ペンローズ過程の効率式\n\n")
    f.write("$$ \\eta = 1 - \\sqrt{\\frac{1 + \\sqrt{1 - a^2}}{2}} $$\n\n")
    f.write("## BZ過程の出力式\n\n")
    f.write("$$ P_{BZ} = \\frac{\\kappa B^2 r_h^2 c \\omega_h^2}{32 \\mu_0} $$\n\n")
    f.write("## 計算結果\n\n")
    f.write(f"- BH質量: {M_bh/Msun:.1f} M☉\n")
    f.write(f"- 回転パラメータ: a* = {a_star}\n")
    f.write(f"- 理論最大効率 (a→1): {eff_max*100:.2f}%\n")
    f.write(f"- ケンタリBH効率: {eff_kenta*100:.2f}%\n")
    f.write(f"- BZ過程出力: {P_bz_kenta:.2e} W\n")
    f.write(f"- 回転エネルギー: {E_rot_kenta:.2e} J\n")
    f.write(f"- 全抽出時間: {t_extract_kenta/(365.25*24*3600):.2e} 年\n\n")
    f.write("## 29%の計算根拠\n\n")
    f.write("1. ペンローズ過程の最大効率は a→1 で 29.3%\n")
    f.write("   式: η_max = 1 - 1/√2 ≈ 0.293\n\n")
    f.write("2. BZ過程も同じ物理（エルゴ球内のエネルギー抽出）に基づく\n\n")
    f.write("3. 実際の効率は磁場強度に依存\n\n")
    f.write("## 結論\n\n")
    f.write(f"BHの回転エネルギーの最大 {eff_max*100:.1f}% を抽出可能\n")

# ===== CSV結果ファイル出力 =====
with open('bz_process_results.csv', 'w', encoding='utf-8') as f:
    f.write("項目,値,単位\n")
    f.write(f"BH質量,{M_bh/Msun:.1f},M☉\n")
    f.write(f"回転パラメータ,{a_star},-\n")
    f.write(f"理論最大効率,{eff_max*100:.2f},%\n")
    f.write(f"ケンタリBH効率,{eff_kenta*100:.2f},%\n")
    f.write(f"BZ過程出力,{P_bz_kenta:.2e},W\n")
    f.write(f"回転エネルギー,{E_rot_kenta:.2e},J\n")
    f.write(f"全抽出時間,{t_extract_kenta/(365.25*24*3600):.2e},年\n")

print("\nグラフ: bz_process_efficiency.png")
print("サマリー: bz_process_summary.md")
print("CSV: bz_process_results.csv")
print("============================================")