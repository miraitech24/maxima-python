#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 12:06:41 2025

@author: iwamura
"""

import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt

def get_maxima_results(R_val, T_list, P_list):
    """Maximaを呼び出し、全サンプルの境界線dを計算させる"""
    t_str = "[" + ",".join(map(str, T_list)) + "]"
    p_str = "[" + ",".join(map(str, P_list)) + "]"
    
    script = f"""
    R : {R_val};
    T_list : {t_str};
    P_list : {p_str};
    /* 境界線公式 d = (T-R)/(T-P) を適用 */
    d_list : map(lambda([t, p], float((t - R)/(t - p))), T_list, P_list);
    
    dest : openw("max_res.txt");
    for x in d_list do (printf(dest, "~f ", x));
    close(dest);
    quit();
    """
    with open("process.mac", "w") as f: f.write(script)
    
    try:
        subprocess.run(["maxima", "--very-quiet", "-r", 'load("process.mac")$'], capture_output=True)
        with open("max_res.txt", "r") as f:
            return [float(x) for x in f.read().split()]
    except:
        return []

# 1. パラメータ設定
R = 3.0
n_samples = 1000
T_samples = np.random.uniform(4.0, 10.0, n_samples)
P_samples = np.random.uniform(-2.0, 2.0, n_samples)

# 2. 連成計算実行
d_thresholds = get_maxima_results(R, T_samples, P_samples)

if d_thresholds:
    # 3. 中央値の市場を特定してシミュレーション
    median_d = np.median(d_thresholds)
    idx = (np.abs(np.array(d_thresholds) - median_d)).argmin()
    T_mid, P_mid = T_samples[idx], P_samples[idx]
    
    # 利得推移データ
    delta = 0.8 # 将来の重視度
    g_total, c_total = 0, 0
    g_h, c_h = [], []
    for t in range(10):
        g_total += (T_mid if t == 0 else P_mid) * (delta**t)
        c_total += R * (delta**t)
        g_h.append(g_total)
        c_h.append(c_total)

    # 4. 可視化（2枚抜き）
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # ヒストグラム
    ax1.hist(d_thresholds, bins=40, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.axvline(median_d, color='red', linestyle='--', label=f'Median d={median_d:.3f}')
    ax1.set_title("Distribution of Boomerang Thresholds (Maxima)")
    ax1.set_xlabel("Required Discount Factor (d)")
    ax1.set_ylabel("Frequency")
    ax1.legend()

    # 利得グラフ
    ax2.plot(g_h, 'r-o', label=f'Gouging Scenario (T={T_mid:.2f}, P={P_mid:.2f})')
    ax2.plot(c_h, 'b-s', label=f'Steady Cooperation (R={R})')
    ax2.set_title(f"Payoff Simulation at Median Market")
    ax2.set_xlabel("Rounds")
    ax2.set_ylabel("Cumulative Payoff")
    # 逆転（ブーメラン）判定
    for i in range(len(c_h)):
        if c_h[i] > g_h[i]:
            ax2.annotate('Boomerang Hits!', xy=(i, g_h[i]), xytext=(i, g_h[i]-5),
                         arrowprops=dict(facecolor='black', shrink=0.05))
            break
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    print(f"解析完了: 中央値の市場条件 T={T_mid:.2f}, P={P_mid:.2f}, 閾値d={median_d:.4f}")