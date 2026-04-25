#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 13:21:44 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 設定値 ---
daily_max_shots = 1580     # 1日の最大射出数
h2_per_capsule = 100       # 1個あたりの水素量 (kg)
h2_price_kg = 500          # 地球での水素売価 (500円/kgと仮定)
revenue_per_shot = h2_per_capsule * h2_price_kg # 50,000円/発

# コスト設定
fixed_cost_day = 20_000_000 # 1日の固定費 (2000万円: インフラ維持)
variable_cost_shot = 15_000 # 1発あたりの製造コスト (1.5万円)

# --- 計算 ---
shots = np.arange(0, daily_max_shots + 100, 10)
total_revenue = shots * revenue_per_shot
total_cost = fixed_cost_day + (shots * variable_cost_shot)

# 損益分岐点の算出: shots = fixed_cost / (price - variable_cost)
bep_shots = fixed_cost_day / (revenue_per_shot - variable_cost_shot)

# --- 描画 ---
plt.figure(figsize=(10, 6))
plt.plot(shots, total_revenue, label="Total Revenue (Earth Value)", color="blue", lw=2)
plt.plot(shots, total_cost, label="Total Cost (Fixed + Variable)", color="red", lw=2)

# 分岐点の強調
plt.axvline(x=bep_shots, color='green', linestyle='--', alpha=0.7)
plt.scatter([bep_shots], [bep_shots * revenue_per_shot], color='black', zorder=5)
plt.annotate(f'Break-even Point\n({int(bep_shots)} shots/day)', 
             xy=(bep_shots, bep_shots * revenue_per_shot), xytext=(bep_shots+100, bep_shots * revenue_per_shot - 1e7),
             arrowprops=dict(facecolor='black', shrink=0.05))

# 利益領域の塗りつぶし
plt.fill_between(shots, total_revenue, total_cost, where=(total_revenue > total_cost), color='green', alpha=0.2, label="Profit Area")

plt.title("Venus-Earth Energy Logistics: Break-even Analysis")
plt.xlabel("Number of Capsule Shots per Day")
plt.ylabel("Value / Cost (JPY)")
plt.legend()
plt.grid(True, linestyle=':')
plt.show()

print(f"損益分岐点: 1日あたり {int(bep_shots)} 発以上の射出で黒字化")