#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 13:52:51 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from params import V_PEAK, V_INF, TAU_LAST

t = np.linspace(0, 100, 1000)
n_neurons = 5
delays = [10, 25, 40, 55, 70] 
colors = plt.cm.plasma(np.linspace(0, 0.8, n_neurons))

plt.figure(figsize=(10, 6))

for i in range(n_neurons):
    # 初期ニューロンは急峻、後になるほど「なだらか」な曲線成分を混ぜる
    ratio = i / (n_neurons - 1)
    v_base = 0.1 * np.exp(t / 15)
    
    # 最後のニューロン(#5)は、提示されたグラフのような対数曲線へ
    v_sat_curve = V_INF * (1 - np.exp(-(t - delays[i])/TAU_LAST))
    
    spike_idx = np.abs(t - delays[i]).argmin()
    v_display = v_base.copy()
    
    # リレーの合成：前の信号を受けて発火し、最後は曲線的に飽和する
    v_display[spike_idx:] = np.maximum(V_PEAK * (1 - ratio*0.3), v_sat_curve[spike_idx:])

    plt.plot(t, v_display, label=f'Neuron #{i+1}', color=colors[i], linewidth=2)
    plt.annotate(f'#{i+1}', xy=(delays[i], v_display[spike_idx]), color=colors[i], weight='bold')

plt.yscale('log')
plt.axhline(V_INF, color='red', linestyle='--', label='Final Saturation Level')
plt.title("Ultrafast Relay to Logarithmic Stability (Log Scale)")
plt.xlabel("Time (μs)")
plt.ylabel("Potential (Log Scale)")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.show()