#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:38:50 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 物理パラメータ設定 ---
V = 100         # 電圧 [V]
f = 1e6         # 1MHz
w = 2 * np.pi * f
R1, R2 = 0.5, 0.5 
ZL = 10         

def calc_p(m):
    denom = (m**2 * w**2 + R1*(R2 + ZL))**2
    return ((V * w * m)**2 * ZL) / denom

# --- 解析計算 ---
# 理論上のピークを与える M_opt = sqrt(R1*(R2+ZL)) / w
m_opt = np.sqrt(R1 * (R2 + ZL)) / w
p_max = calc_p(m_opt)

# コンソールに解析結果を表示
print("-" * 30)
print(f"解析結果 (Theoretical Peak)")
print(f"Optimal M: {m_opt * 1e6:.4f} [uH]")
print(f"Max Power: {p_max:.2f} [W]")
print("-" * 30)

# --- グラフ描画 ---
m_axis = np.linspace(0, 2.5e-6, 2000)
p_axis = calc_p(m_axis)

plt.figure(figsize=(12, 7))
plt.plot(m_axis * 1e6, p_axis, label="Tesla Power Curve", color='blue', lw=2)

# 1. 理想点 (Peak)
plt.scatter(m_opt * 1e6, p_max, color='red', s=150, edgecolors='black', label=f"PEAK: {p_max:.1f}W", zorder=5)

# 2. 走行中EV給電 (Dynamic Wireless Charging)
# 距離が離れているため M は小さく、立ち上がりの急斜面に位置する
m_ev = 0.12e-6
plt.scatter(m_ev * 1e6, calc_p(m_ev), color='orange', s=100, label="Dynamic EV (High Distance)", zorder=5)

# 3. スマホ給電 (Qi / Stationary)
# 密着しているため M は大きく、ピークを超えた安定領域に位置する
m_qi = 1.8e-6
plt.scatter(m_qi * 1e6, calc_p(m_qi), color='purple', s=100, label="Smartphone (Close Contact)", zorder=5)

# グラフ装飾
plt.title(f"Wireless Power Transfer Analysis (f={f/1e6}MHz)", fontsize=14)
plt.xlabel("Mutual Inductance M [uH]", fontsize=12)
plt.ylabel("Transfer Power P [W]", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# 垂直線の追加（ピーク位置の強調）
plt.axvline(m_opt * 1e6, color='red', linestyle=':', alpha=0.5)

plt.show()