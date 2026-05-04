#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 08:53:09 2026

@author: iwamura
"""

# pai18_gripping_force.py
# Evaluate gripping force decay based on ice rheology data from Maxima.
# Gripping force: F(t) = F0 * exp(-t / tau(T))
# tau(T) read from ice_rheology_data.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------- Auto Japanese font detection ----------
def setup_japanese_font():
    """Detect a Japanese-capable font and set as default."""
    jp_candidates = [
        'IPAexGothic', 'IPAGothic', 'Yu Gothic', 'Noto Sans CJK JP',
        'MS Gothic', 'TakaoPGothic', 'Hiragino Kaku Gothic ProN'
    ]
    for font_name in jp_candidates:
        font_path = fm.findfont(font_name, fallback_to_default=False)
        if font_path:
            plt.rcParams['font.family'] = font_name
            return font_name
    # Fallback to DejaVu Sans without Japanese support
    plt.rcParams['font.family'] = 'sans-serif'
    return 'DejaVu Sans'

font_used = setup_japanese_font()
print(f"Using font: {font_used}")

# ---------- Load Maxima output ----------
data = pd.read_csv('ice_rheology_data.csv')
temperatures = data['T(K)'].values
tau_values = data['tau(s)'].values
A_values = data['A(Pa^-n s^-1)'].values

# ---------- Gripping force simulation ----------
F0 = 100.0   # N, initial gripping force
time = np.linspace(0, 1e7, 500)  # 10 million seconds (~115 days)

# Choose some temperatures for demonstration
temp_disp = [250, 260, 268, 272, 273.15]   # K
colors = plt.cm.coolwarm(np.linspace(0.2, 0.9, len(temp_disp)))

plt.figure(figsize=(10,6))
for i, Tk in enumerate(temp_disp):
    # interpolate tau for exact Tk (linear interpolation on data grid)
    idx = np.abs(temperatures - Tk).argmin()
    tau = tau_values[idx]
    F = F0 * np.exp(-time / tau)
    plt.plot(time/86400, F, color=colors[i], lw=2,
             label=f'T = {Tk:.0f} K (τ ≈ {tau:.2e} s)')

plt.xlabel('Time (days)', fontsize=12)
plt.ylabel('Gripping force (N)', fontsize=12)
plt.title('Ice gripping force relaxation (Maxwell model)', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ice_gripping_relaxation.png', dpi=150)
plt.show()

# ---------- 3D surface: Force vs time & temperature ----------
from matplotlib import cm
T_grid, t_grid = np.meshgrid(temperatures, time)
tau_grid = tau_values[np.newaxis, :]   # broadcast
F_grid = F0 * np.exp(-t_grid / tau_grid)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(T_grid, t_grid/86400, F_grid, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True, alpha=0.8)
ax.set_xlabel('Temperature (K)')
ax.set_ylabel('Time (days)')
ax.set_zlabel('Gripping force (N)')
ax.set_title('Gripping force $F(T,t)$')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20, label='Force (N)')
plt.tight_layout()
plt.savefig('ice_gripping_surface.png', dpi=150)
plt.show()

print("Evaluation complete. Figures saved.")
