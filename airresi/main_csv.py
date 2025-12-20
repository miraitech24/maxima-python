#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 11:20:53 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import re
import io

# 1. ブラケット混じりのCSVを強引に読み込む関数
def load_and_clean_data(filename):
    with open(filename, 'r') as f:
        content = f.read()
    # 数字、点、カンマ、マイナス、改行以外を削除
    clean_content = re.sub(r'[^0-9\.\,\-\n]', '', content)
    df = pd.read_csv(io.StringIO(clean_content), header=None, names=['t', 'x', 'y'])
    return df

# データ読み込み
df = load_and_clean_data('trajectory.csv')

# 2. 描画の初期設定
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, df['x'].max() * 1.1)
ax.set_ylim(0, df['y'].max() * 1.1)
ax.set_xlabel("Distance (x)")
ax.set_ylabel("Height (y)")
ax.grid(True, linestyle=':')

line, = ax.plot([], [], 'b-', lw=2)
point, = ax.plot([], [], 'ro')

# 3. アニメーション更新関数
def update(frame):
    line.set_data(df['x'][:frame], df['y'][:frame])
    point.set_data([df['x'].iloc[frame-1]], [df['y'].iloc[frame-1]])
    return line, point

# 4. アニメーション生成
ani = FuncAnimation(fig, update, frames=len(df), interval=30, blit=True)

# --- ここでGIFとして保存 ---
print("Saving animation as motion.gif...")
ani.save("motion.gif", writer=PillowWriter(fps=30))
print("Save complete!")

plt.show()