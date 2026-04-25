#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 13:27:02 2026

@author: iwamura
"""

import matplotlib.pyplot as plt

# 設定
total_minutes = 1440  # 1日
print_time_per_unit = 120  # 1個2時間
num_printers = 135    # 135台体制
launch_interval = 0.9 # 0.9分に1回射出

# 1日を通じた累積生産数と累積射出数
time = range(total_minutes)
produced = [(num_printers / print_time_per_unit) * t for t in time]
launched = [t / launch_interval for t in time]

plt.figure(figsize=(10, 5))
plt.plot(time, produced, label="Cumulative Production (135 Printers)", color="orange")
plt.plot(time, launched, label="Cumulative Launch (Railgun Capacity)", color="blue", linestyle="--")
plt.title("Production vs. Launch Synchronization")
plt.xlabel("Time (minutes)")
plt.ylabel("Number of Capsules")
plt.legend()
plt.grid(True)
plt.show()