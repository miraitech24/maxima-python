#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 15:12:37 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_s_pipe_mesh(nodes_z=30, nodes_r=10):
    # パイプの中心線 (S字)
    zeta = np.linspace(0, np.pi * 2, nodes_z)
    center_x = np.sin(zeta)
    center_y = np.zeros_like(zeta)
    
    # 断面（円形）の生成
    theta = np.linspace(0, 2*np.pi, nodes_r)
    radius = 0.5
    
    mesh_x = np.outer(center_x, np.ones_like(theta)) + radius * np.outer(np.ones_like(zeta), np.cos(theta))
    mesh_y = np.outer(center_y, np.ones_like(theta)) + radius * np.outer(np.ones_like(zeta), np.sin(theta))
    mesh_z = np.outer(zeta, np.ones_like(theta))
    
    return mesh_x, mesh_y, mesh_z

mx, my, mz = generate_s_pipe_mesh()

# 可視化
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(mx, my, mz, cmap='viridis', edgecolors='k', alpha=0.6)
ax.set_title("S-Shape Pipe: Curvilinear Grid")
plt.show()