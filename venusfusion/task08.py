#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 11:18:47 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Maximaからの引き渡し（数式文字列の読み込み）
try:
    with open("formula_08.txt", "r") as f:
        # 不要な文字を除去して数式を取得
        formula_str = f.read().replace(" ", "").strip()
        print(f"Imported Formula: {formula_str}")
except FileNotFoundError:
    formula_str = "1/sqrt(L*C)" # フォールバック

# 2. 定数設定（金星モデル）
L = 1.5e-3  # テスラコイルのインダクタンス (H)
C = 2.0e-9  # 金星地表-電離層間の想定容量 (F)
V = 1e6     # 送電電圧 (1MV)

# 共振角周波数の計算 (Maximaの導出結果を使用)
omega_0 = 1 / np.sqrt(L * C)
print(f"Resonance Frequency: {omega_0 / (2 * np.pi):.2f} Hz")

# 3. シミュレーション：金星の気象変動による抵抗Rの変化
# 硫酸の霧や雷雨により R が 10Ω から 1000Ω まで変動すると仮定
R_range = np.linspace(10, 1000, 100)
omega = np.linspace(omega_0 * 0.5, omega_0 * 1.5, 500)

# インピーダンスと電力の計算
R_fixed = 100
Z = np.sqrt(R_fixed**2 + (omega * L - 1/(omega * C))**2)
Power = (V**2) / Z

# 4. グラフ描画
plt.figure(figsize=(10, 6))
plt.plot(omega / (2 * np.pi), Power / 1e6, label="Transmitted Power (MW)")
plt.axvline(omega_0 / (2 * np.pi), color='r', linestyle='--', label="Resonance Point")
plt.title("Venus Tesla Tower: Power Transmission Efficiency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power (MW)")
plt.grid(True)
plt.legend()
plt.show()