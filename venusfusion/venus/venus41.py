#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:30:22 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 定数確定 (Maximaでの計算結果を直接使用) ---
# E=400e9, alpha=4.5e-6, nu=0.28 => (E*alpha)/(2*(1-nu))
SLOPE = 1250000.0  # Pa/K (1.25 MPa/K)

def get_Nf(sigma_a_mpa):
    """S-N曲線: log10(Nf) = 32.0 - 8.5 * log10(S)"""
    if sigma_a_mpa <= 150: return 1e12  # 疲労限度
    return 10**(32.0 - 8.5 * np.log10(sigma_a_mpa))

# --- 山頂拠点：リアルな運用履歴 (1年分を想定) ---
# 1. 起動・停止 (500K) x 300回
# 2. 緊急停止 (950K) x 2回
# 3. 山頂ガスト/風速変動による微細ストレス (50K) x 10,000回
history_dt = [500]*300 + [950]*2 + [50]*10000

# 累積損傷度 D (マイナー則)
damage = sum(1.0 / get_Nf(SLOPE * dt / 1e6) for dt in history_dt)

print(f"--- #41 山頂拠点・熱疲労 最終判定 ---")
print(f"定数 Slope: {SLOPE/1e6:.3f} MPa/K")
print(f"累積損傷度 D: {damage:.6f}")
print(f"判定: {'SAFE (継続稼働OK)' if damage < 1.0 else 'CRITICAL (要設計修正)'}")

# --- 可視化 (山頂の稼働ポイントを明示) ---
dts = np.linspace(30, 1000, 100)
nfs = [get_Nf(SLOPE * dt / 1e6) for dt in dts]

plt.figure(figsize=(10, 6))
plt.semilogy(dts, nfs, 'b-', label='S-N Curve')
plt.scatter([50, 500, 950], [get_Nf(SLOPE*50/1e6), get_Nf(SLOPE*500/1e6), get_Nf(SLOPE*950/1e6)], 
            c='red', label='Operation (Gust, Start, Emergency)')
plt.title("Fatigue Analysis (Optimized for Summit)")
plt.xlabel("Delta T (K)")
plt.ylabel("Nf (Cycles)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.show()