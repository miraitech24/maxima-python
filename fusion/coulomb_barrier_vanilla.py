#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:28:14 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 物理定数 (SI単位系) ---
e = 1.602e-19        # 電荷
epsilon_0 = 8.854e-12 # 真空の誘電率
hbar = 1.054e-34      # プランク定数
m_d = 3.343e-27       # 重水素の質量
mu = m_d / 2          # 換算質量

def tunnel_probability(E_ev, screening_ev=0):
    """
    WKB近似を用いたトンネル確率の計算
    E_ev: 粒子のエネルギー (eV)
    screening_ev: 遮蔽効果によって下がる障壁のエネルギー (eV)
    """
    E_total = (E_ev + screening_ev) * e
    # ガモフ因子の計算 (簡略化式)
    # P = exp(-2 * pi * eta)  where eta = (Z1*Z2*e^2 / (4*pi*epsilon_0*hbar*v))
    v = np.sqrt(2 * E_total / mu)
    eta = (e**2) / (4 * np.pi * epsilon_0 * hbar * v)
    return np.exp(-2 * np.pi * eta)

# --- 計算設定 ---
energies = np.logspace(-2, 4, 500)  # 0.01eV (常温) から 10keV (熱核融合) まで

# 1. 通常の条件 (遮蔽なし)
probs_normal = [tunnel_probability(E) for E in energies]

# 2. 強力な遮蔽効果があると仮定 (例: 300eVの遮蔽)
probs_screened = [tunnel_probability(E, screening_ev=300) for E in energies]

# --- 可視化 ---
plt.figure(figsize=(10, 6))
plt.plot(energies, probs_normal, label='Normal (Vacuum)', color='red', lw=2)
plt.plot(energies, probs_screened, label='Screened (Hypothetical)', color='blue', linestyle='--')

plt.axvline(x=0.025, color='green', linestyle=':', label='Room Temperature (300K)')
plt.axvline(x=1000, color='orange', linestyle=':', label='Sun Core (~10^7K)')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Energy of Deuterium (eV)')
plt.ylabel('Tunneling Probability')
plt.title('Why Cold Fusion is Hard: The Coulomb Barrier')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()
plt.ylim(1e-100, 1) # 10のマイナス100乗まで表示
plt.show()