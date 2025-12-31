#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 15:55:09 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# ==========================================
# 1. 境界適合格子（S字パイプ）の生成
# ==========================================
def generate_s_pipe_mesh(nodes_z=60, nodes_r=20):
    zeta = np.linspace(0, np.pi * 2, nodes_z)
    center_x = np.sin(zeta)  # S字の形状
    center_y = np.zeros_like(zeta)
    theta = np.linspace(0, 2*np.pi, nodes_r)
    radius = 0.4
    
    mx = np.outer(center_x, np.ones_like(theta)) + radius * np.outer(np.ones_like(zeta), np.cos(theta))
    my = np.outer(center_y, np.ones_like(theta)) + radius * np.outer(np.ones_like(zeta), np.sin(theta))
    mz = np.outer(zeta, np.ones_like(theta))
    return mx, my, mz, center_x

mx, my, mz, cx = generate_s_pipe_mesh()

# ==========================================
# 2. 速度データの定義
# ==========================================
# 中心軸からの距離に基づく放物面分布（管内流の基本）
dist_from_center = np.sqrt((mx - cx[:, None])**2 + my**2)
V_mag = np.maximum(1.0 - (dist_from_center / 0.4)**2, 0)

# ベクトル成分（S字の進行方向に合わせる）
# x = sin(z) の微分 dx/dz = cos(z) を考慮
U_vec = np.cos(mz) * V_mag 
V_vec = np.zeros_like(V_mag)
W_vec = np.ones_like(V_mag) * 0.8  # Z方向への主流

# ==========================================
# 3. カラーベクトル図の描画
# ==========================================
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 視認性向上のためにグリッドを間引く（スライス）
# 断面付近と全体を適度にサンプリング
skip = (slice(None, None, 4), slice(None, None, 2))

# カラーベクトル図（Quiver）
# cmap='jet' で速度に応じた色付けを行い、array引数に速度の大きさを渡す
q = ax.quiver(mx[skip], my[skip], mz[skip], 
               U_vec[skip], V_vec[skip], W_vec[skip], 
               length=0.5,           # 矢印の長さ
               normalize=True,       # ベクトルの長さを正規化（向きを強調）
               cmap='jet',           # カラーマップ
               array=V_mag[skip].flatten(), # 色の基準値（流速）
               lw=2.0)               # 矢印の太さ

# カラーバーの追加
cbar = fig.colorbar(q, ax=ax, shrink=0.6, pad=0.1)
cbar.set_label('Velocity Magnitude (m/s)')

# グラフの装飾
ax.set_title("3D S-Pipe: Color-coded Velocity Vector Field", fontsize=15)
ax.set_xlabel("X-axis (Pipe Bend)")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis (Flow Direction)")

# 視点の調整（S字がよく見える角度）
ax.view_init(elev=25, azim=-60)

plt.tight_layout()
plt.show()