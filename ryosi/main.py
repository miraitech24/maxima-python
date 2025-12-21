#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 20:28:15 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import wave_functions as wf  # Maximaが作ったファイルをモジュールとして読み込む

x = np.linspace(-5, 5, 1000)

# グラフ描画
fig, ax = plt.subplots(figsize=(8, 5))
for n in range(4):
    psi_func = getattr(wf, f"psi_{n}")
    y = psi_func(x)
    ax.plot(x, y, label=rf"$\psi_{n}(x)$")

ax.set_title("Wavefunctions from wxMaxima Analysis")
ax.legend()
plt.show()