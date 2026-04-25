#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 12:07:59 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. #33からのデータインポート
# --------------------------------------------------
try:
    i_vals = np.loadtxt('pulse_data.csv', delimiter=',')
except OSError:
    print("Error: 'pulse_data.csv' not found. Please run #33 script first.")
    exit()

# 2. Python：エネルギー損失と収益性の計算
# --------------------------------------------------
# 物理・経済パラメータ
R_coil = 1.5           # コイル抵抗 [Ω]
dt = 0.0001            # 時間刻み [s] (100ms/1000steps)
mass_payload = 500     # 1射出あたりの荷物量 [kg]
price_per_kg = 15000   # 地球売価 [円/kg]
fixed_cost = 1200000   # 1射出あたりの運用固定費（母船維持費等） [円]
elec_unit_price = 25   # 金星LENR電力単価 [円/kWh]

# A. ジュール熱損失: E = ∫ R * i^2 dt
energy_loss_j = np.sum(R_coil * (i_vals**2) * dt)
energy_loss_kwh = energy_loss_j / (3.6 * 10**6)

# B. ROI算出
total_revenue = mass_payload * price_per_kg
power_cost = energy_loss_kwh * elec_unit_price
total_cost = fixed_cost + power_cost
roi = (total_revenue - total_cost) / total_cost

# 3. 結果の表示と考察
# --------------------------------------------------
print(f"--- #47b ROI Analysis Results ---")
print(f"Voltage Limit: 1386.88 V (Fixed by #33)")
print(f"Energy Loss: {energy_loss_kwh:.6f} kWh/shot")
print(f"Power Cost: {power_cost:.2f} JPY")
print(f"Total Cost: {total_cost/1e6:.4f} M JPY")
print(f"Revenue: {total_revenue/1e6:.4f} M JPY")
print(f"ROI: {roi:.2%}")

# 損失推移の可視化
plt.figure(figsize=(10, 4))
plt.fill_between(np.arange(len(i_vals))*dt, R_coil * (i_vals**2), color='orange', alpha=0.3)
plt.plot(np.arange(len(i_vals))*dt, R_coil * (i_vals**2), color='red', label='Heat Loss [W]')
plt.title("Joule Heat Loss Profile (#47b)")
plt.xlabel("Time [s]")
plt.ylabel("Loss Power [W]")
plt.legend()
plt.show()

# 考察
# 電圧を1386.88Vに制限したことで、ピーク電流が当初の想定より大幅に抑えられた。
# ジュール損は電流の「二乗」に比例するため、この制限はROIに対して極めてポジティブに作用している。
# ROIがプラス（>0%）であれば再検討の必要はなく、このまま実運用フェーズ（#48 軌道設計）へ移行可能。