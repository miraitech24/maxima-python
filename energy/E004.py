#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:25:37 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:19:37 2026

@author: iwamura
"""

# TAG:E004_v1
# E004 sweep analysis (no input file).
# Outputs: (1) 2x2 subplot (2) summary file (3) CSV result file 6
# Requirements for pass/fail: dist>=100km, eta>=0.70, cost<=0.05 1

import csv
import os
import sys
import subprocess
import random
from datetime import datetime, timezone

import matplotlib.pyplot as plt

MAC = "E004_sweep.mac"
IN_CSV = "E004_sweep.csv"

OUT_CSV = "E004_results.csv"
OUT_SUM = "E004_summary.txt"
OUT_PNG = "E004_plots.png"

def fail(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def run_maxima():
    if not os.path.exists(MAC):
        fail(f"missing {MAC}")
    cmd = ["maxima", "-b", MAC]
    cp = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if cp.returncode != 0:
        print(cp.stdout)
        print(cp.stderr, file=sys.stderr)
        fail(f"maxima failed: {cp.returncode}")
    if not os.path.exists(IN_CSV):
        fail(f"missing {IN_CSV}")

def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)
    if not rows:
        fail(f"no data in {path}")
    return rows

def write_rows(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

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

def to_f(x): 
    try: return float(x)
    except Exception: return float("nan")

def main():
    run_maxima()
    rows = read_rows(IN_CSV)

    # Save as final CSV artifact
    fieldnames = list(rows[0].keys())
    write_rows(OUT_CSV, rows, fieldnames)

    total = len(rows)
    pass_all = sum(int(r["pass_all"]) for r in rows)

    # データ抽出と数値変換
    k = [to_f(r["k"]) for r in rows]
    Q0 = [to_f(r["Q0"]) for r in rows]
    g = [to_f(r["gamma_cloud"]) for r in rows]
    eta = [to_f(r["eta_total"]) for r in rows]
    cost = [to_f(r["cost_usd_per_kwh"]) for r in rows]
    paf = [int(r["pass_all"]) for r in rows]

    # NaNを除去
    valid = [i for i in range(len(eta)) if not (k[i] != k[i] or Q0[i] != Q0[i] or 
                                                 g[i] != g[i] or eta[i] != eta[i] or 
                                                 cost[i] != cost[i])]
    k = [k[i] for i in valid]
    Q0 = [Q0[i] for i in valid]
    g = [g[i] for i in valid]
    eta = [eta[i] for i in valid]
    cost = [cost[i] for i in valid]
    paf = [paf[i] for i in valid]

    # 5000点にランダムサンプリング
    sample_size = 5000
    if len(eta) > sample_size:
        indices = random.sample(range(len(eta)), sample_size)
        k = [k[i] for i in indices]
        Q0 = [Q0[i] for i in indices]
        g = [g[i] for i in indices]
        eta = [eta[i] for i in indices]
        cost = [cost[i] for i in indices]
        paf = [paf[i] for i in indices]
        print(f"サンプリング: {sample_size}点を使用")
    else:
        print(f"全データ {len(eta)}点を使用")

    # Summary
    with open(OUT_SUM, "w", encoding="utf-8") as f:
        f.write("E004 Tesla Transfer Quick Feasibility (sweep-based)\n")
        f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}Z\n")
        f.write(f"cases: {total}\n")
        f.write(f"pass_all: {pass_all}\n")
        f.write("requirements: dist>=100km, eta>=0.70, cost<=0.05 USD/kWh\n")

    font = jp_font_or_none()
    if font:
        plt.rcParams["font.family"] = font
        t1, t2, t3, t4 = "η（効率） vs k", "η（効率） vs Q0", "η（効率） vs γcloud", "コスト vs η（効率）"
        xl_k, xl_Q0, xl_g = "結合係数 k", "Q0", "γcloud"
        yl_eta, yl_cost = "効率 η", "コスト(USD/kWh)"
    else:
        t1, t2, t3, t4 = "Efficiency η vs k", "Efficiency η vs Q0", "Efficiency η vs γcloud", "Cost vs Efficiency η"
        xl_k, xl_Q0, xl_g = "k", "Q0", "gamma_cloud"
        yl_eta, yl_cost = "Efficiency η", "Cost (USD/kWh)"

    # パスとフェイルのインデックスを分離
    pass_idx = [i for i, p in enumerate(paf) if p == 1]
    fail_idx = [i for i, p in enumerate(paf) if p == 0]
    
    print(f"パス: {len(pass_idx)}点, フェイル: {len(fail_idx)}点")

    fig, axs = plt.subplots(2, 2, figsize=(14, 11))
    plt.subplots_adjust(hspace=0.35, wspace=0.35)

    # 1. η vs k
    if fail_idx:
        axs[0,0].scatter([k[i] for i in fail_idx], [eta[i] for i in fail_idx], 
                        c='red', s=1, alpha=0.1, label='Fail')
    if pass_idx:
        axs[0,0].scatter([k[i] for i in pass_idx], [eta[i] for i in pass_idx], 
                        c='blue', s=3, alpha=0.6, label='Pass (η>=0.70)')
    axs[0,0].set_title(t1, fontsize=12)
    axs[0,0].set_xlabel(xl_k, fontsize=10)
    axs[0,0].set_ylabel(yl_eta, fontsize=10)
    axs[0,0].legend(fontsize=8)
    axs[0,0].set_ylim([0, 1])

    # 2. η vs Q0
    if fail_idx:
        axs[0,1].scatter([Q0[i] for i in fail_idx], [eta[i] for i in fail_idx], 
                        c='red', s=1, alpha=0.1, label='Fail')
    if pass_idx:
        axs[0,1].scatter([Q0[i] for i in pass_idx], [eta[i] for i in pass_idx], 
                        c='blue', s=3, alpha=0.6, label='Pass (η>=0.70)')
    axs[0,1].set_title(t2, fontsize=12)
    axs[0,1].set_xlabel(xl_Q0, fontsize=10)
    axs[0,1].set_ylabel(yl_eta, fontsize=10)
    axs[0,1].legend(fontsize=8)
    axs[0,1].set_ylim([0, 1])

    # 3. η vs γcloud
    if fail_idx:
        axs[1,0].scatter([g[i] for i in fail_idx], [eta[i] for i in fail_idx], 
                        c='red', s=1, alpha=0.1, label='Fail')
    if pass_idx:
        axs[1,0].scatter([g[i] for i in pass_idx], [eta[i] for i in pass_idx], 
                        c='blue', s=3, alpha=0.6, label='Pass (η>=0.70)')
    axs[1,0].set_title(t3, fontsize=12)
    axs[1,0].set_xlabel(xl_g, fontsize=10)
    axs[1,0].set_ylabel(yl_eta, fontsize=10)
    axs[1,0].legend(fontsize=8)
    axs[1,0].set_ylim([0, 1])

    # 4. Cost vs η
    if fail_idx:
        axs[1,1].scatter([eta[i] for i in fail_idx], [cost[i] for i in fail_idx], 
                        c='red', s=1, alpha=0.1, label='Fail')
    if pass_idx:
        axs[1,1].scatter([eta[i] for i in pass_idx], [cost[i] for i in pass_idx], 
                        c='blue', s=3, alpha=0.6, label='Pass')
    axs[1,1].set_title(t4, fontsize=12)
    axs[1,1].set_xlabel(yl_eta, fontsize=10)
    axs[1,1].set_ylabel(yl_cost, fontsize=10)
    axs[1,1].legend(fontsize=8)

    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    plt.close(fig)

    print("OK")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_SUM}")
    print(f"- {OUT_PNG}")

if __name__ == "__main__":
    main()