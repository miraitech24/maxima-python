#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAG:venus33_v3_mdout

RDRE連成解析:
- 推力倍率モデルでRDRE効果を表現
- ロケット方程式で到達距離計算
- 結果をMarkdown形式で出力
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from datetime import datetime


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


def write_markdown_report(params, results, rdre_factor):
    """Markdown形式でレポートを出力"""
    
    md_content = (
        "# RDRE連成航法解析レポート\n\n"
        "**TAG:** `venus33_v3_mdout`\n"
        f"**生成時刻:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "---\n\n"
        "## 1. 課題仕様\n\n"
        "### 1.1 目的\n"
        "RDRE（回転デトネーションエンジン）導入時の金星大気圏突入前の航法性能を評価する。\n\n"
        "### 1.2 数式モデル\n\n"
        "ロケット方程式：\n\n"
        "$$\n"
        "v(t) = v_e \\ln\\left(\\frac{M_0}{M_0 - \\dot{m} t}\\right)\n"
        "$$\n\n"
        "ここで：\n\n"
        "$$\n"
        "v_e = I_{sp} \\cdot g_0\n"
        "$$\n\n"
        "$$\n"
        "\\dot{m} = \\frac{F}{v_e}\n"
        "$$\n\n"
        "### 1.3 パラメータ\n\n"
        "| パラメータ | 記号 | 値 | 単位 |\n"
        "|-----------|------|-----|------|\n"
        f"| 初期質量 | $M_0$ | {params['M0']:,.0f} | kg |\n"
        f"| 燃料比 | $\\phi$ | {params['fuel_ratio']} | - |\n"
        f"| 航法日数 | $t_{{max}}$ | {params['days']} | days |\n"
        "| ベース推力 | $F_{{base}}$ | 4669 | N |\n"
        "| 比推力 | $I_{{sp}}$ | 3000 | s |\n"
        "| 重力加速度 | $g_0$ | 9.80665 | m/s² |\n"
        f"| **RDRE倍率** | $\\alpha$ | **{rdre_factor}** | - |\n"
        f"| **RDRE推力** | $F_{{RDRE}}$ | **{params['F_thrust']:.0f}** | N |\n\n"
        "### 1.4 RDRE仮定\n\n"
        "> 文書に基づく仮定：RDREは「同じ燃料量でより大きな力を出せる可能性」があるとされている。\n"
        "> 具体的な推力/Isp改善率の記載がないため、**推力倍率モデル**（Isp不変、推力のみ倍増）を採用する。\n\n"
        "---\n\n"
        "## 2. 計算結果\n\n"
        "### 2.1 物理量\n\n"
        "| 項目 | 計算値 | 単位 |\n"
        "|------|--------|------|\n"
        f"| 有効排気速度 $v_e$ | {results['ve']:.2f} | m/s |\n"
        f"| 質量流量 $\\dot{{m}}$ | {results['mdot']:.4f} | kg/s |\n"
        f"| 燃料質量 | {results['M_fuel']:.2f} | kg |\n"
        f"| 燃料枯渇時間 | {results['t_empty']:.2f} days | - |\n"
        f"| 最大到達速度 | {results['v_max']:,.2f} | m/s |\n"
        f"| **総移動距離** | **{results['d_total']/1e9:.3f}** | million km |\n\n"
        "### 2.2 フェーズ分離\n\n"
        f"- **加速フェーズ:** {results['t_acc_limit']/86400:.2f} 日間（燃料消費中）\n"
        f"- **慣性フェーズ:** {results['t_inertial']/86400:.2f} 日間（燃料枯渇後）\n\n"
        "---\n\n"
        "## 3. 判定\n\n"
        f"**閾値:** {params['threshold']} million km（文献値41.4を基準）\n\n"
        "| 条件 | 値 | 判定 |\n"
        "|------|-----|------|\n"
        f"| 到達距離 | {results['d_total']/1e6:.2f} million km | {'≥' if results['d_total']/1e6 >= params['threshold'] else '<'} {params['threshold']} |\n\n"
        "### 判定結果\n\n"
    )
    
    if results['d_total']/1e6 >= params['threshold']:
        md_content += "✅ **OK:** 航法成立。ROI評価（#47b）へハンドオフ可能。\n\n"
    else:
        md_content += "❌ **NG:** 距離不足。対策：推力増加（#41）または高密度ハイドライド（#14b）。\n\n"
    
    md_content += (
        "---\n\n"
        "## 4. RDRE感度分析\n\n"
        "RDRE倍率 $\\alpha$ と到達距離の関係：\n\n"
        "| $\\alpha$ | 推力 (N) | 到達距離 (million km) | 改善率 |\n"
        "|----------|----------|---------------------|--------|\n"
        "| 1.0 | 4669 | {:.2f} | 基準 |\n"
        f"| {rdre_factor} | {params['F_thrust']:.0f} | {results['d_total']/1e6:.2f} | {(results['d_total']/results['base_dist']-1)*100:+.1f}% |\n\n"
        "---\n\n"
        "## 5. 結論\n\n"
        "1. **RDRE有効性:**\n"
        f"   RDRE推力倍率 {rdre_factor}x で到達距離 {results['d_total']/1e6:.2f} million km。\n"
        f"   基準（{results['base_dist']/1e6:.2f} million km）から {(results['d_total']/results['base_dist']-1)*100:+.1f}% の改善。\n\n"
        "2. **航法成立条件:**\n"
        f"   {'到達可能' if results['d_total']/1e6 >= params['threshold'] else '到達不可'}（閾値 {params['threshold']} million km）。\n\n"
        "3. **モデル限界:**\n"
        "   - Isp不変の仮定は保守的見積もり\n"
        "   - 実際のRDREはIspにも影響する可能性あり\n"
        "   - 重力損失、空力抵抗は未考慮\n\n"
        "4. **今後の課題:**\n"
        "   - RDRE実証データに基づく推力/Ispモデルの精緻化\n"
        "   - 大気圏突入フェーズとの連成解析\n\n"
        "---\n\n"
        "## 6. 付録\n\n"
        "### 6.1 計算コード\n\n"
        "- **ファイル:** `venusatmos33sympy_v2.py`\n"
        "- **依存ライブラリ:** sympy, numpy, matplotlib\n\n"
        "### 6.2 実行コマンド\n\n"
        "```bash\n"
        "python venusatmos33sympy_v2.py [M0] [fuel_ratio] [days] [rdre_factor]\n"
        "```\n\n"
        "例：\n"
        "```bash\n"
        "python venusatmos33sympy_v2.py 100000 0.5 14 1.5\n"
        "```\n\n"
        "---\n\n"
        f"*レポート生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    ).format(results['base_dist']/1e6)
    
    with open("VENUS33_RDRE_REPORT.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("OK: VENUS33_RDRE_REPORT.md generated")


def run_coupling_analysis(
    M0_val=100000,
    fuel_ratio=0.5,
    days=14,
    rdre_thrust_factor=1.0,
):
    # --- 1. SymPy 変数定義 ---
    t = sp.symbols("t", real=True, positive=True)
    M_0, F_max, Isp, g_0 = sp.symbols("M_0 F_max Isp g_0", real=True, positive=True)

    # --- 2. 物理パラメータ設定 ---
    F_base = 4669.0
    Isp_base = 3000.0
    g0_base = 9.80665
    dist_threshold = 41.4  # million km

    if M0_val <= 0:
        raise ValueError("M0_val must be > 0")
    if not (0.0 < fuel_ratio < 1.0):
        raise ValueError("fuel_ratio must be in (0, 1)")
    if days <= 0:
        raise ValueError("days must be > 0")
    if rdre_thrust_factor <= 0:
        raise ValueError("rdre_thrust_factor must be > 0")

    ve = Isp * g_0
    mdot = F_max / ve

    p_val = {F_max: F_base * rdre_thrust_factor, Isp: Isp_base, g_0: g0_base, M_0: M0_val}
    mdot_val = float(mdot.subs(p_val))

    M_fuel = M0_val * fuel_ratio
    t_empty = M_fuel / mdot_val
    T_end = days * 24 * 3600

    # --- 3. フェーズ分離計算 ---
    v_acc_expr = ve * sp.log(M_0 / (M_0 - mdot * t))
    d_acc_expr = sp.integrate(v_acc_expr, (t, 0, t))

    v_func = sp.lambdify(t, v_acc_expr.subs(p_val), "numpy")
    d_func = sp.lambdify(t, d_acc_expr.subs(p_val), "numpy")

    t_acc_limit = min(t_empty, T_end)
    v_max = float(v_func(t_acc_limit))
    d_acc_total = float(d_func(t_acc_limit))

    t_inertial = max(0.0, T_end - t_empty)
    d_inertial = v_max * t_inertial
    d_total = d_acc_total + d_inertial

    # 基準（RDREなし）の計算
    p_val_base = {F_max: F_base, Isp: Isp_base, g_0: g0_base, M_0: M0_val}
    mdot_base = float(mdot.subs(p_val_base))
    t_empty_base = M_fuel / mdot_base
    v_func_base = sp.lambdify(t, v_acc_expr.subs(p_val_base), "numpy")
    d_func_base = sp.lambdify(t, d_acc_expr.subs(p_val_base), "numpy")
    t_acc_limit_base = min(t_empty_base, T_end)
    v_max_base = float(v_func_base(t_acc_limit_base))
    d_acc_total_base = float(d_func_base(t_acc_limit_base))
    t_inertial_base = max(0.0, T_end - t_empty_base)
    d_inertial_base = v_max_base * t_inertial_base
    d_total_base = d_acc_total_base + d_inertial_base

    # --- 4. コンソール出力 ---
    print("--- venusatmos33sympy (RDRE-linked) ---")
    print(f"RDRE factor={rdre_thrust_factor}, thrust={p_val[F_max]} N")
    print(f"ve={float((Isp*g_0).subs(p_val)):.2f} m/s")
    print(f"Fuel empty={t_empty/86400:.2f} days")
    print(f"Max velocity={v_max:,.2f} m/s")
    print(f"Distance={d_total/1e9:.3f} million km")

    # --- 5. グラフ描画 ---
    t_plot = np.linspace(0, T_end, 500)
    
    v_plot = np.piecewise(
        t_plot,
        [t_plot <= t_empty, t_plot > t_empty],
        [lambda t: v_func(t), lambda t: v_max]
    )

    font = jp_font_or_none()
    if font:
        plt.rcParams["font.family"] = font
        title = f"航法プロファイル (RDRE倍率={rdre_thrust_factor})"
        xlab = "時間 [日]"
        ylab = "速度 [m/s]"
        fuel_lbl = "燃料枯渇"
    else:
        title = f"Navigation Profile (RDRE factor={rdre_thrust_factor})"
        xlab = "Time [days]"
        ylab = "Velocity [m/s]"
        fuel_lbl = "Fuel Empty"

    plt.figure(figsize=(10, 5))
    plt.plot(t_plot / 86400, v_plot, label="Velocity (m/s)", lw=2)
    plt.axvline(x=t_empty / 86400, color="orange", linestyle="--", label=fuel_lbl)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    
    # グラフ保存
    plt.savefig("VENUS33_RDRE_PROFILE.png", dpi=150, bbox_inches='tight')
    plt.show()

    # --- 6. Markdownレポート出力 ---
    params = {
        'M0': M0_val,
        'fuel_ratio': fuel_ratio,
        'days': days,
        'F_thrust': p_val[F_max],
        'threshold': dist_threshold
    }
    
    results = {
        've': float((Isp*g_0).subs(p_val)),
        'mdot': mdot_val,
        'M_fuel': M_fuel,
        't_empty': t_empty,
        't_acc_limit': t_acc_limit,
        't_inertial': t_inertial,
        'v_max': v_max,
        'd_total': d_total,
        'base_dist': d_total_base
    }
    
    write_markdown_report(params, results, rdre_thrust_factor)
    
    # 判定表示
    if (d_total / 1e6) < dist_threshold:
        print("\n[JUDGEMENT] NG: distance insufficient")
    else:
        print("\n[JUDGEMENT] OK: navigation feasible")


if __name__ == "__main__":
    # 引数: 質量, 燃料比, 日数, rdre_thrust_factor
    m = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
    fr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    d = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    f = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5  # デフォルト1.5倍
    
    run_coupling_analysis(m, fr, d, f)