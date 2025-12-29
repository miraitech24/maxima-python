#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:22:50 2025

@author: iwamura
"""

import subprocess

# Maxima実行
subprocess.run(["maxima", "--very-quiet", "-r", 'load("austerity.mac")$'])

# 辞書型として読み込み
results = {}
with open("bridge.dat", "r") as f:
    for line in f:
        key, val = line.strip().split(":")
        results[key] = float(val)

print(f"財務局への回答：ブーメラン境界線は {results['threshold_d']} です。")