#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 12:17:52 2025

@author: iwamura
"""

import sys, json, numpy as np
import matplotlib.pyplot as plt

# JSONの読み込み
with open('params.json', 'r') as f:
    data = json.load(f)

# エラー修正：evalする前に変数 a, b を定義する
a = data['a']
b = data['b']

# Maximaから来た "a+b" などの数式を、上のa, bを使って数値に変える
u_star = eval(data['u_star'].replace('^', '**'))
v_star = eval(data['v_star'].replace('^', '**'))

print(f"Calculated Steady State: u*={u_star}, v*={v_star}")

# --- マクロな設定：どんな模様になるか（拡散係数） ---
N, dt = 100, 0.1
Du, Dv = 0.2, 1.0  # この比率が「模様の種」を育てる

# 初期の皮膚の状態（わずかなムラがある）
U = u_star + np.random.randn(N, N) * 0.05
V = v_star + np.random.randn(N, N) * 0.05

def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

# 生命の自律計算ループ
for _ in range(5000):
    lu, lv = laplacian(U), laplacian(V)
    U += (a - U + U**2 * V + Du * lu) * dt
    V += (b - U**2 * V + Dv * lv) * dt

# 可視化
plt.figure(figsize=(6, 6))
plt.imshow(U, cmap='magma')
plt.title("Morphogenesis: Chemical Pattern Formation")
plt.axis('off')
plt.show()