#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 12:37:25 2026

@author: iwamura
"""

import numpy as np
import re  # 正規表現ライブラリを追加

filename = "formula_02.txt"

try:
    with open(filename, "r") as f:
        raw_output = f.read().strip()
        print(f"Raw Maxima Output: '{raw_output}'")
        
        # --- 修正の要：XML/HTMLタグを取り除く ---
        # <...> で囲まれた部分をすべて空文字に置換します
        clean_formula = re.sub(r'<[^>]+>', '', raw_output)
        
        # ブラケットや不要な空白、代入記号の処理
        clean_formula = clean_formula.replace("[", "").replace("]", "").replace(";", "").strip()
        if "=" in clean_formula:
            clean_formula = clean_formula.split("=")[-1].strip()
            
        # Maxima記法をPython記法へ変換
        formula_py = clean_formula.replace("%pi", "np.pi").replace("^", "**")
        print(f"Final Formula for Eval: '{formula_py}'")

except FileNotFoundError:
    print("File not found. Using fallback.")
    formula_py = "1 / (4 * np.pi**2 * C * f**2)"

# 数値の設定
f_val = 150000.0
C_val = 2.0e-9

try:
    # 変数コンテキストを辞書で定義
    context = {"np": np, "f": f_val, "C": C_val}
    # evalを実行
    required_L = eval(formula_py, {"np": np}, context)
    
    print("-" * 30)
    print(f"Resulting L: {required_L:.6e} H")
    print("-" * 30)
except Exception as e:
    print(f"Error during eval: {e}")