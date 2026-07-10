#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:57:32 2026

@author: iwamura
"""

# TAG:PAI02_v1
# PAI-02 熱上昇流生成ノズル / 気流壁出力
# Formula in table: P = p*A*v/2, target P = 1.68E+12 W 2
# coupling-prompt: python writes .md, formula in LaTeX, plus 2x2 plot, summary, CSV 13

import csv
import math
from datetime import datetime

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

OUT_MD = "PAI02_spec.md"
OUT_CSV = "PAI02_results.csv"
OUT_SUM = "PAI02_summary.txt"
OUT_PNG = "PAI02_plots.png"

TARGET_P_W = 1.68e12  # 1.68E+12 W 2


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


def main():
    # --- SymPy model (as documented) ---
    p, A, v = sp.symbols("p A v", positive=True, real=True)
    P = p * A * v / 2  # P = pAv/2 2

    # --- Assumptions for running without input files ---
    # The documents do NOT provide p, A, v ranges/units, so we do a scenario sweep.
    # (We only judge against target 1.68E+12 W.) 2
    p_list = [1e3, 1e4, 1e5, 1e6]         # placeholder scenarios (unit not specified in docs)
    A_list = [1.0, 10.0, 100.0, 1000.0]   # placeholder scenarios (m^2 etc. not specified)
    v_list = [10.0, 100.0, 1000.0, 5000.0]  # placeholder scenarios (m/s etc. not specified)

    # --- Compute table ---
    rows = []
    case_id = 0
    for pv in p_list:
        for av in A_list:
            for vv in v_list:
                case_id += 1
                p_w = float(P.subs({p: pv, A: av, v: vv}))
                pass_target = 1 if p_w >= TARGET_P_W else 0
                rows.append({
                    "case_id": case_id,
                    "p": pv,
                    "A": av,
                    "v": vv,
                    "P_W": p_w,
                    "target_P_W": TARGET_P_W,
                    "pass_target": pass_target,
                })

    if not rows:
        fail("no cases generated")

    # --- Write CSV ---
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # --- Summary ---
    total = len(rows)
    passed = sum(int(r["pass_target"]) for r in rows)
    best = max(rows, key=lambda r: float(r["P_W"]))

    with open(OUT_SUM, "w", encoding="utf-8") as f:
        f.write("PAI-02 Nozzle Power Summary\n")
        f.write(f"timestamp_utc: {datetime.utcnow().isoformat()}Z\n")
        f.write("formula: P = p*A*v/2 (as in table)\n")
        f.write(f"target_P_W: {TARGET_P_W}\n")
        f.write(f"cases: {total}\n")
        f.write(f"pass_target: {passed}\n")
        f.write("max_case:\n")
        f.write(f"  case_id={best['case_id']}, p={best['p']}, A={best['A']}, v={best['v']}, P_W={best['P_W']}\n")

    # --- Write spec+conclusion to .md (LaTeX) ---
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# PAI-02 熱上昇流生成ノズル（気流壁出力）\n\n")
        f.write("## 課題仕様\n")
        f.write("- ID: PAI-02\n")
        f.write("- 身体機能: 熱上昇流生成ノズル\n")
        f.write("- 物理的核心: 気流壁出力\n")
        f.write("- 計算式（文書記載）: 
P
=
f
r
a
c
p
A
v
2
P=
fracpAv2\n")
        f.write(f"- 目標値（文書記載）: P = {TARGET_P_W:.3e}\\ \\mathrm{{W}}\n\n")
        f.write("## 結論\n")
        f.write("- 文書の式 
P
=
f
r
a
c
p
A
v
2
P=
fracpAv2 に従えば、与えた 
p
,
A
,
v
p,A,v から出力 
P
P を計算し、目標 
1.68
t
i
m
e
s
10
12
,
m
a
t
h
r
m
W
1.68
times10 
12
 
,
mathrmW を満たすか判定できる。\n")
        f.write("- ただし文書には 
p
,
A
,
v
p,A,v の単位・想定レンジが記載されていないため、本コードではシナリオ値でスイープし合否を確認する。\n")

    # --- Plot (2x2) ---
    font = jp_font_or_none()
    if font:
        plt.rcParams["font.family"] = font
        t1, t2, t3, t4 = "Pの分布（log10）", "合否（目標1.68E+12W）", "P vs v（p,A別）", "必要v（目標達成）"
        xl_p, xl_A, xl_v, yl_p = "p", "A", "v", "P [W]"
    else:
        t1, t2, t3, t4 = "P distribution (log10)", "Pass/Fail", "P vs v (by p,A)", "Required v to reach target"
        xl_p, xl_A, xl_v, yl_p = "p", "A", "v", "P [W]"

    p_vals = np.array(["p"]) for r in rows])
    A_vals = np.array(["A"]) for r in rows])
    v_vals = np.array(["v"]) for r in rows])
    P_vals = np.array(["P_W"]) for r in rows])
    pass_vals = np.array(["pass_target"]) for r in rows])

    fig, axs = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)

    # (1) scatter p vs A, colored by log10(P)
    c1 = np.log10(np.maximum(P_vals, 1.0))
    sc1 = axs[0, 0].scatter(p_vals, A_vals, c=c1, s=30)
    axs[0, 0].set_title(t1)
    axs[0, 0].set_xlabel(xl_p)
    axs[0, 0].set_ylabel(xl_A)
    fig.colorbar(sc1, ax=axs[0, 0], label="log10(P)")

    # (2) pass/fail map (p vs A)
    axs[0, 1].scatter(p_vals, A_vals, c=pass_vals, cmap="coolwarm", s=30)
    axs[0, 1].set_title(t2)
    axs[0, 1].set_xlabel(xl_p)
    axs[0, 1].set_ylabel(xl_A)

    # (3) P vs v for each (p,A) pair (keep simple: plot a few lines)
    shown = 0
    for pv in p_list:
        for av in A_list:
            vv = np.array(v_list, dtype=float)
            pp = np.array()
            axs[1, 0].plot(vv, pp, marker="o", linewidth=1, label=f"p={pv:g},A={av:g}")
            shown += 1
            if shown >= 6:
                break
        if shown >= 6:
            break
    axs[1, 0].axhline(TARGET_P_W, color="black", linestyle="--", linewidth=1)
    axs[1, 0].set_title(t3)
    axs[1, 0].set_xlabel(xl_v)
    axs[1, 0].set_ylabel(yl_p)
    axs[1, 0].legend(fontsize=7)

    # (4) required v to reach target: v_req = 2*P_target/(p*A)
    v_req_expr = 2 * TARGET_P_W / (p * A)
    v_req = []
    x_pa = []
    for pv in p_list:
        for av in A_list:
            v_need = float(v_req_expr.subs({p: pv, A: av}))
            x_pa.append(f"{pv:g},{av:g}")
            v_req.append(v_need)
    axs[1, 1].bar(range(len(v_req)), v_req)
    axs[1, 1].set_title(t4)
    axs[1, 1].set_xlabel("(p,A)")
    axs[1, 1].set_ylabel(xl_v)
    axs[1, 1].tick_params(axis="x", labelrotation=45)
    axs[1, 1].locator_params(axis="y", nbins=5)

    # tick density control (avoid label overlap) 3
    for ax in axs.flat:
        ax.locator_params(axis="x", nbins=5)

    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print("OK")
    print(f"- {OUT_MD}")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_SUM}")
    print(f"- {OUT_PNG}")


if __name__ == "__main__":
    main()