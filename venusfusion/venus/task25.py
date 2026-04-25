#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 12:44:27 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

filename = "solution_p.txt"

# 1. 解析解のインポートと置換（%e 対策）
try:
    with open(filename, "r") as f:
        content = f.read().strip()
        # Maximaの出力をPython形式に完全変換
        # 1. 変数定義部分があれば削除
        if ":" in content: content = content.split(":")[1]
        # 2. セミコロン削除
        expr = content.replace(";", "")
        # 3. %e を np.exp() 形式、または数値に置換
        # %e^x 形式を np.exp(x) に書き換える、または単純に e の値にする
        expr = expr.replace("%e**", "np.exp") # %e**(...) 形式に対応
        expr = expr.replace("%e", "np.e")     # 単体の場合
        expr = expr.replace("^", "**")
        expr_py = expr.strip()
except Exception as e:
    print(f"ファイル読み込み失敗: {e}")
    sys.exit()

# 2. 統計的シミュレーション
# 炉内の1000箇所の温度分布（平均1100K, 標準偏差50K）
T = np.random.normal(1100, 50, 1000)

# 3. 反応確率の配列演算
try:
    # expr_py が 'np.exp(-(1160.49.../T))' のような形ならそのまま計算可能
    # もし np.exp ではなく np.e** 形式なら、引数 T を渡して評価
    P_array = eval(expr_py)
except Exception as e:
    print(f"解析失敗。内容: {expr_py}")
    print(f"エラー詳細: {e}")
    sys.exit()

# 4. 可視化
plt.figure(figsize=(10, 5))
plt.hist(P_array, bins=30, color='crimson', alpha=0.7, edgecolor='black')
plt.title("LENR Reactor Robustness: Reproducibility Distribution")
plt.xlabel("Reaction Probability (P)")
plt.ylabel("Site Count")
plt.grid(True, ls='--')
plt.show()

print(f"計算成功。数式: {expr_py}")
print(f"再現性スコア (平均確率): {np.mean(P_array):.6f}")