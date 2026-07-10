#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:08:32 2026

@author: iwamura
"""

# TAG:PAI21_v1
# PAI-21 Quantum Entanglement Gate (Calibration)
# Spec: K = μ·N, target K = 1000 N
# Output: (1) 2x2 subplot (2) summary file (3) CSV result file
# Also write spec+conclusion to .md with LaTeX

import csv
import math
from datetime import datetime, timezone

import matplotlib.pyplot as plt


OUT_MD = "PAI21_spec.md"
OUT_CSV = "PAI21_results.csv"
OUT_SUM = "PAI21_summary.txt"
OUT_PNG = "PAI21_plots.png"

TARGET_K_N = 1000.0  # target 1000 N


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


def fail(msg: str):
    raise SystemExit(f"ERROR: {msg}")


def compute_k(mu: float, normal_n: float) -> float:
    # K = μ·N
    return mu * normal_n


def main():
    # Assumed calibration grid (document does not provide μ, N ranges)
    mu_list = [0.1, 0.2, 0.3, 0.5, 0.8]
    n_list = [200, 500, 1000, 2000, 5000]  # N

    rows = []
    case_id = 0
    for mu in mu_list:
        for normal_n in n_list:
            case_id += 1
            k_n = compute_k(mu, normal_n)
            pass_target = 1 if k_n >= TARGET_K_N else 0
            rows.append({
                "case_id": case_id,
                "mu": mu,
                "normal_n": normal_n,
                "k_n": k_n,
                "target_k_n": TARGET_K_N,
                "pass_target": pass_target,
            })

    if not rows:
        fail("no cases generated")

    # Write CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Summary
    total = len(rows)
    passed = sum(int(r["pass_target"]) for r in rows)
    with open(OUT_SUM, "w", encoding="utf-8") as f:
        f.write("PAI-21 Calibration Summary\n")
        f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}Z\n")
        f.write("formula: K = mu * N\n")
        f.write(f"target_k_n: {TARGET_K_N}\n")
        f.write(f"cases: {total}\n")
        f.write(f"pass_target: {passed}\n")

    # Spec+Conclusion MD
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# PAI-21 Quantum Entanglement Gate（Calibration）\n\n")
        f.write("## 課題仕様\n")
        f.write("- ID: PAI-21\n")
        f.write("- 対象: Quantum Entanglement Gate\n")
        f.write("- 物理的核心: Calibration\n")
        f.write("- 計算式: $K = \\mu \\cdot N$\n")
        f.write(f"- 目標値: $K \\ge {TARGET_K_N}\\ \\mathrm{{N}}$\n\n")
        f.write("## 結論\n")
        f.write("- 与えられた $\\mu$ と $N$ に対して、$K = \\mu N$ を計算し、目標値1000Nを満たすか判定できる。\n")
        f.write(f"- 全{total}ケース中、目標達成は{passed}ケース（{100*passed/total:.1f}%）。\n")
        f.write("- 必要なKを得るには、十分なμとNの組み合わせが必要。\n")

    # データ抽出（修正点1: リスト内包表記の文法エラー）
    mu_vals = [r["mu"] for r in rows]
    n_vals = [r["normal_n"] for r in rows]
    k_vals = [r["k_n"] for r in rows]
    pass_vals = [r["pass_target"] for r in rows]

    # Plot (2x2)
    font = jp_font_or_none()
    if font:
        plt.rcParams["font.family"] = font
        title1, title2, title3, title4 = "Kの分布", "合否（目標1000N）", "K vs N（μ別）", "K vs μ（N別）"
        x_mu, x_n, y_k = "μ", "N", "K (N)"
    else:
        title1, title2, title3, title4 = "K distribution", "Pass/Fail (target 1000N)", "K vs N (by mu)", "K vs mu (by N)"
        x_mu, x_n, y_k = "mu", "N", "K (N)"

    fig, axs = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)

    # (1) scatter mu vs N, colored by K
    sc1 = axs[0, 0].scatter(mu_vals, n_vals, c=k_vals, s=40)
    axs[0, 0].set_title(title1)
    axs[0, 0].set_xlabel(x_mu)
    axs[0, 0].set_ylabel(x_n)
    fig.colorbar(sc1, ax=axs[0, 0], label=y_k)

    # (2) scatter mu vs N, colored by pass/fail
    axs[0, 1].scatter(mu_vals, n_vals, c=pass_vals, cmap="coolwarm", s=40)
    axs[0, 1].set_title(title2)
    axs[0, 1].set_xlabel(x_mu)
    axs[0, 1].set_ylabel(x_n)

    # (3) K vs N grouped by mu（修正点2: 数値比較の誤り）
    for mu in mu_list:
        xs = [r["normal_n"] for r in rows if abs(r["mu"] - mu) < 1e-6]
        ys = [r["k_n"] for r in rows if abs(r["mu"] - mu) < 1e-6]
        axs[1, 0].plot(xs, ys, marker="o", label=f"mu={mu}")
    axs[1, 0].axhline(TARGET_K_N, color="black", linestyle="--", linewidth=1)
    axs[1, 0].set_title(title3)
    axs[1, 0].set_xlabel(x_n)
    axs[1, 0].set_ylabel(y_k)
    axs[1, 0].legend(fontsize=8)

    # (4) K vs mu grouped by N（修正点3: 同様の修正）
    for normal_n in n_list:
        xs = [r["mu"] for r in rows if abs(r["normal_n"] - normal_n) < 1e-6]
        ys = [r["k_n"] for r in rows if abs(r["normal_n"] - normal_n) < 1e-6]
        axs[1, 1].plot(xs, ys, marker="o", label=f"N={normal_n}")
    axs[1, 1].axhline(TARGET_K_N, color="black", linestyle="--", linewidth=1)
    axs[1, 1].set_title(title4)
    axs[1, 1].set_xlabel(x_mu)
    axs[1, 1].set_ylabel(y_k)
    axs[1, 1].legend(fontsize=8)

    # tick density control (avoid label overlap)
    for ax in axs.flat:
        ax.locator_params(axis="x", nbins=5)
        ax.locator_params(axis="y", nbins=5)

    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print("OK")
    print(f"- {OUT_MD}")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_SUM}")
    print(f"- {OUT_PNG}")


if __name__ == "__main__":
    main()