#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:45:10 2026
Updated: 2026-05-06

@author: iwamura
"""

# PAI18_EXT2_ice_rheology.py
# PAI-18-EXT1: 氷クリープ（アイスレオロジー）に基づく摩擦係数 μ(T,t)
# 数式: F = μ·N, target 1000 N
# 氷クリープ則: ナビエ・ストークス則（Glenの法則）に基づく

import csv
from datetime import datetime, timezone
import math
import numpy as np
import matplotlib.pyplot as plt

# ==================== 出力ファイル ====================
OUT_CSV = "PAI18_EXT1_results.csv"
OUT_SUM = "PAI18_EXT1_summary.txt"
OUT_PNG = "PAI18_EXT1_plots.png"
OUT_MD = "PAI18_EXT1_spec.md"

TARGET_F_N = 1000.0  # 目標力 [N]

# ==================== 日本語フォント ====================
def jp_font_or_none():
    try:
        import matplotlib.font_manager as fm
        installed = {t.name for t in fm.fontManager.ttflist}
        for name in ["IPAexGothic", "IPAGothic", "Noto Sans CJK JP", "Yu Gothic", "MS Gothic"]:
            if name in installed:
                return name
    except Exception:
        return None
    return None

# ==================== アイスレオロジーモデル ====================
# Glenの法則（氷クリープ則）:
#   ẋ = A * σ^n   (ひずみ速度 = 定数 * 応力^3)
#   摩擦係数 μ はクリープ変形と温度・時間に依存

# 氷の物性パラメータ（文献値ベース）
REF_TEMP_K = 263.15          # 基準温度 -10°C
ACTIVATION_ENERGY_J = 78000  # 活性化エネルギー [J/mol]
GAS_CONSTANT = 8.314         # 気体定数 [J/(mol·K)]
N_GEN = 3.0                  # Glen則の指数（通常 n=3）
A0 = 1.0e-8                  # 頻度因子 [1/s]

def arrhenius_factor(T_K: float) -> float:
    """アレニウス型温度依存性"""
    if T_K <= 0:
        return 0.0
    return math.exp(-ACTIVATION_ENERGY_J / (GAS_CONSTANT * T_K))

def creep_strain_rate(T_K: float, sigma: float = 1.0) -> float:
    """
    クリープひずみ速度
    ẋ = A0 * exp(-Q/RT) * σ^n
    """
    if T_K <= 0:
        return 0.0
    A = A0 * arrhenius_factor(T_K)
    return A * (sigma ** N_GEN)

def mu_ice_rheology(
    T_K: float,           # 温度 [K]
    t_sec: float,         # 時間 [s]
    sigma: float = 1.0,   # 応力 [MPa]
    mu0: float = 0.50,    # 初期摩擦係数（低温・短時間）
    mu_min: float = 0.05  # 最小摩擦係数（完全クリープ後）
) -> float:
    """
    氷クリープに基づく摩擦係数 μ(T,t)
    
    物理モデル:
    - 温度が高いほどクリープ促進 → μ減少
    - 時間が長いほどクリープ進行 → μ減少
    - 応力が高いほど変形促進
    - アレニウス則で温度依存性を表現
    
    参考: Glen's flow law for ice (n=3), Arrhenius temperature dependence
    """
    if T_K <= 0 or t_sec < 0:
        return mu0
    
    # クリープひずみ
    strain_rate = creep_strain_rate(T_K, sigma)
    strain = strain_rate * t_sec
    
    # クリープによる摩擦係数の低下（飽和あり）
    # μ = μ_min + (μ0 - μ_min) * exp(-k * strain)
    creep_sensitivity = 100.0  # クリープ感受性パラメータ
    decay = math.exp(-creep_sensitivity * strain)
    mu = mu_min + (mu0 - mu_min) * decay
    
    return max(mu_min, min(mu0, mu))

def mu_empirical_approximation(
    T_K: float,
    t_sec: float,
    mu0: float = 0.50,
    T_ref: float = 263.15
) -> float:
    """
    実験式近似版（よりシンプルで安定）
    
    μ(T,t) = μ0 * exp(-α(T_ref - T)/T_ref) * exp(-β t)
    """
    alpha = 0.05  # 温度感度
    beta = 5e-5   # 時間感度 [1/s]
    
    # 温度効果（低温でμ大、高温でμ小）
    temp_factor = math.exp(-alpha * (T_ref - T_K) / T_ref) if T_K > 0 else 0.0
    # 時間効果（長時間でμ減少）
    time_factor = math.exp(-beta * t_sec)
    
    mu = mu0 * temp_factor * time_factor
    return max(0.05, min(mu0, mu))

# ==================== メイン ====================
def main():
    # スイープ範囲
    T_list = np.linspace(223.15, 273.15, 30)   # -50°C ～ 0°C
    t_list = np.linspace(0, 24*3600, 30)       # 0～24時間
    N_val = 4000.0  # 垂直力 [N]
    
    rows = []
    case_id = 0
    
    for T in T_list:
        for t in t_list:
            case_id += 1
            
            # 物理モデルと近似式の両方を計算
            mu_phys = mu_ice_rheology(T, t)
            mu_approx = mu_empirical_approximation(T, t)
            mu_val = mu_phys  # 物理モデルを採用
            
            F_val = mu_val * N_val
            pass_target = 1 if F_val >= TARGET_F_N else 0
            
            rows.append({
                "case_id": case_id,
                "T_K": round(T, 2),
                "t_sec": round(t, 0),
                "t_hour": round(t/3600, 2),
                "mu": round(mu_val, 4),
                "mu_approx": round(mu_approx, 4),
                "N_N": N_val,
                "F_N": round(F_val, 2),
                "target_N": TARGET_F_N,
                "pass_target": pass_target
            })
    
    # ==================== CSV出力 ====================
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    
    # ==================== サマリー ====================
    total = len(rows)
    passed = sum(r["pass_target"] for r in rows)
    best = max(rows, key=lambda r: r["F_N"])
    worst = min(rows, key=lambda r: r["F_N"])
    
    with open(OUT_SUM, "w", encoding="utf-8") as f:
        f.write("PAI-18-EXT2 Ice Creep (Rheology) Summary\n")
        f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}Z\n")
        f.write("formula: F = mu * N (Glen's flow law with Arrhenius temperature dependence)\n")
        f.write(f"target_F_N: {TARGET_F_N}\n")
        f.write(f"total_cases: {total}\n")
        f.write(f"pass_cases: {passed}\n")
        f.write(f"pass_rate: {100*passed/total:.1f}%\n")
        f.write(f"best_case: T={best['T_K']}K, t={best['t_hour']}h, mu={best['mu']}, F={best['F_N']}N\n")
        f.write(f"worst_case: T={worst['T_K']}K, t={worst['t_hour']}h, mu={worst['mu']}, F={worst['F_N']}N\n")
        f.write("NOTE: Ice rheology model implements Arrhenius temperature dependence and Glen's n=3 creep law\n")
    
    # ==================== MD仕様書 ====================
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# PAI-18-EXT1 アイスレオロジー（氷クリープ）モデル\n\n")
        f.write("## 課題仕様\n\n")
        f.write("### 目的\n")
        f.write("氷クリープ（アイスレオロジー）に基づく摩擦係数 $\\mu(T,t)$ をモデル化し、\n")
        f.write("力 $F = \\mu \\cdot N$ が目標値 $1000\\,\\mathrm{N}$ を満たす条件を評価する。\n\n")
        
        f.write("### 数式モデル\n\n")
        f.write("#### Glenのクリープ則\n")
        f.write("$$\n\\dot{\\varepsilon} = A \\sigma^n \\quad (n=3)\n$$\n\n")
        
        f.write("#### アレニウス型温度依存性\n")
        f.write("$$\nA = A_0 \\exp\\left(-\\frac{Q}{RT}\\right)\n$$\n\n")
        
        f.write("#### 摩擦係数モデル\n")
        f.write("$$\n\\mu(T,t) = \\mu_{\\min} + (\\mu_0 - \\mu_{\\min}) \\exp(-k \\cdot \\dot{\\varepsilon} \\cdot t)\n$$\n\n")
        
        f.write("### パラメータ\n\n")
        f.write("| パラメータ | 値 | 単位 | 説明 |\n")
        f.write("|----------|-----|------|------|\n")
        f.write("| $\\mu_0$ | 0.50 | - | 初期摩擦係数 |\n")
        f.write("| $\\mu_{\\min}$ | 0.05 | - | 最小摩擦係数 |\n")
        f.write("| $Q$ | 78000 | J/mol | 活性化エネルギー |\n")
        f.write("| $A_0$ | $1.0 \\times 10^{-8}$ | 1/s | 頻度因子 |\n")
        f.write("| $n$ | 3.0 | - | Glen則指数 |\n")
        f.write("| $R$ | 8.314 | J/(mol·K) | 気体定数 |\n\n")
        
        f.write("## 結論\n\n")
        f.write(f"- **総ケース数**: {total}\n")
        f.write(f"- **目標達成率**: {100*passed/total:.1f}% ({passed}/{total})\n")
        f.write(f"- **最良条件**: T={best['T_K']:.1f}K ({best['T_K']-273.15:.1f}°C), t={best['t_hour']:.1f}h → μ={best['mu']:.4f}\n")
        f.write(f"- **最悪条件**: T={worst['T_K']:.1f}K ({worst['T_K']-273.15:.1f}°C), t={worst['t_hour']:.1f}h → μ={worst['mu']:.4f}\n\n")
        
        f.write("### 物理的考察\n\n")
        f.write("1. **温度効果**: 低温（-50°C付近）ではクリープが抑制され、高い摩擦係数を維持\n")
        f.write("2. **時間効果**: 長時間の負荷でクリープが進行し、摩擦係数が低下\n")
        f.write("3. **応力効果**: 高応力下ではクリープが促進され、摩擦係数低下が加速\n")
        f.write("4. **Glen則**: 氷のクリープは応力の3乗に比例する非線形挙動を示す\n\n")
        
        f.write("### 設計推奨\n\n")
        f.write("- 目標力1000N達成には $\\mu \\ge 0.25$ が必要\n")
        f.write("- 低温環境（-30°C以下）かつ短期間（1時間未満）が有利\n")
        f.write("- 高温や長時間ではクリープによるμ低下を考慮した安全率が必要\n")
    
    # ==================== データ抽出 ====================
    T_vals = np.array([r["T_K"] for r in rows])
    t_vals = np.array([r["t_sec"] for r in rows])
    mu_vals = np.array([r["mu"] for r in rows])
    F_vals = np.array([r["F_N"] for r in rows])
    pass_vals = np.array([r["pass_target"] for r in rows])
    mu_approx_vals = np.array([r["mu_approx"] for r in rows])
    
    # ==================== グラフ描画 ====================
    font = jp_font_or_none()
    if font:
        plt.rcParams["font.family"] = font
        titles = ["μの温度依存性", "μの時間依存性", "達成力Fの分布", "モデル比較（物理 vs 近似）"]
        x1, x2, x3, x4 = "温度 T [K]", "時間 t [s]", "温度 T [K]", "温度 T [K]"
        y1, y2, y3, y4 = "摩擦係数 μ [-]", "摩擦係数 μ [-]", "力 F [N]", "摩擦係数 μ [-]"
        label_phys, label_approx = "物理モデル", "近似式"
    else:
        plt.rcParams["font.family"] = "sans-serif"
        titles = ["mu vs Temperature", "mu vs Time", "Force Distribution", "Model Comparison"]
        x1, x2, x3, x4 = "Temperature T [K]", "Time t [s]", "Temperature T [K]", "Temperature T [K]"
        y1, y2, y3, y4 = "Friction coeff mu [-]", "Friction coeff mu [-]", "Force F [N]", "Friction coeff mu [-]"
        label_phys, label_approx = "Physical model", "Approximation"
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    
    # グラフ1: μ vs T (時間で色分け)
    sc1 = axs[0, 0].scatter(T_vals, mu_vals, c=t_vals/3600, s=15, cmap="viridis")
    axs[0, 0].set_title(titles[0])
    axs[0, 0].set_xlabel(x1)
    axs[0, 0].set_ylabel(y1)
    plt.colorbar(sc1, ax=axs[0, 0], label="時間 [h]")
    
    # グラフ2: μ vs t (温度で色分け)
    sc2 = axs[0, 1].scatter(t_vals/3600, mu_vals, c=T_vals, s=15, cmap="coolwarm")
    axs[0, 1].set_title(titles[1])
    axs[0, 1].set_xlabel("時間 t [h]")
    axs[0, 1].set_ylabel(y2)
    plt.colorbar(sc2, ax=axs[0, 1], label="温度 [K]")
    
    # グラフ3: F vs T (合否で色分け)
    colors = ['red' if p == 0 else 'green' for p in pass_vals]
    axs[1, 0].scatter(T_vals, F_vals, c=colors, s=15, alpha=0.6)
    axs[1, 0].axhline(TARGET_F_N, color="blue", linestyle="--", linewidth=1.5, label=f"目標 {TARGET_F_N}N")
    axs[1, 0].set_title(titles[2])
    axs[1, 0].set_xlabel(x3)
    axs[1, 0].set_ylabel(y3)
    axs[1, 0].legend()
    axs[1, 0].set_ylim([0, max(F_vals)*1.1])
    
    # グラフ4: 物理モデル vs 近似式比較
    # 特定の時間での比較（代表的な3つの時間）
    for hour in [0.5, 6, 24]:
        mask = np.abs(t_vals/3600 - hour) < 0.1
        if np.any(mask):
            axs[1, 1].plot(T_vals[mask], mu_vals[mask], 'o-', label=f"物理 t={hour}h")
            axs[1, 1].plot(T_vals[mask], mu_approx_vals[mask], 's--', label=f"近似 t={hour}h")
    axs[1, 1].set_title(titles[3])
    axs[1, 1].set_xlabel(x4)
    axs[1, 1].set_ylabel(y4)
    axs[1, 1].legend(fontsize=8)
    
    for ax in axs.flat:
        ax.locator_params(axis="x", nbins=5)
        ax.locator_params(axis="y", nbins=5)
    
    fig.savefig(OUT_PNG, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print("OK")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_SUM}")
    print(f"- {OUT_PNG}")
    print(f"- {OUT_MD}")

if __name__ == "__main__":
    main()