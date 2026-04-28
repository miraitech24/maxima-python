#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:03:05 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# ---- 自動日本語フォント検出 ----
plt.rcParams['font.family'] = 'sans-serif'
try:
    # macOS 日本語フォント候補
    fp = plt.font_manager.FontProperties(family='Hiragino Sans')
    if fp.get_name() != 'sans-serif':
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'IPAexGothic', 'Noto Sans CJK JP']
    else:
        raise
except:
    pass  # fallback to default (English)

# ---- モデル定義 ----
def P_reject(m, d):
    """拒絶確率 P = 1/(1+exp(5*(m-1.2*d)))"""
    return 1 / (1 + np.exp(5 * (m - 1.2 * d)))

# ---- パラメータ設定 ----
threshold = 0.1  # 安全閾値
m_vals = np.linspace(0, 1, 100)
d_vals = np.linspace(0, 1, 100)
M, D = np.meshgrid(m_vals, d_vals, indexing='ij')  # (m,d) 格子

# ---- 1. 3D 表面プロット (2x2 サブプロットの左上) ----
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
ax1 = axes[0,0]
P_surf = P_reject(M, D)
cont = ax1.contourf(M, D, P_surf, levels=20, cmap='viridis')
ax1.set_xlabel('m')
ax1.set_ylabel('d')
ax1.set_title('Surface: P_{reject}(m,d)')
fig.colorbar(cont, ax=ax1)

# ---- 2. 固定 m での dose 曲線 (m=0.3, 0.5, 0.7) ----
ax2 = axes[0,1]
d_fine = np.linspace(0, 1, 200)
for m_fix in [0.3, 0.5, 0.7]:
    P_fix = P_reject(m_fix, d_fine)
    ax2.plot(d_fine, P_fix, label=f'm={m_fix}')
ax2.axhline(threshold, color='r', linestyle='--', label='threshold=0.1')
ax2.set_xlabel('d')
ax2.set_ylabel('P_{reject}')
ax2.set_title('Dose curves')
ax2.legend()

# ---- 3. 最適 dose (P=0.1 を満たす d*) ----
m_opt_vals = np.linspace(0.01, 0.99, 50)
d_opt = []
for m in m_opt_vals:
    # 二分法で P(m,d)=0.1 を解く (d∈[0,1])
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if P_reject(m, mid) < threshold:
            lo = mid
        else:
            hi = mid
    d_opt.append((lo+hi)/2)
d_opt = np.array(d_opt)

ax3 = axes[1,0]
ax3.plot(m_opt_vals, d_opt, 'b-', linewidth=2)
ax3.set_xlabel('m')
ax3.set_ylabel('d*')
ax3.set_title('Optimal dose (P=0.1)')
ax3.grid(True)

# ---- 4. 安全領域 (m=0.5 固定) ----
ax4 = axes[1,1]
P_m05 = P_reject(0.5, d_fine)
ax4.plot(d_fine, P_m05, label='P(m=0.5)')
ax4.axhline(0.1, color='r', linestyle='--', label='threshold')
ax4.fill_between(d_fine, 0, 0.1, where=(P_m05 <= 0.1), color='green', alpha=0.3)
ax4.set_xlabel('d')
ax4.set_ylabel('P_{reject}')
ax4.set_title('Safe region for m=0.5')
ax4.legend()

plt.tight_layout()
plt.savefig('BIO502_results.png', dpi=150)
plt.show()

# ---- 5. CSV 出力 (最適 dose テーブル) ----
with open('BIO502_opt_dose.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['m', 'd_opt'])
    for m, d in zip(m_opt_vals, d_opt):
        writer.writerow([f'{m:.4f}', f'{d:.4f}'])

# ---- 6. サマリーファイル ----
with open('BIO502_summary.txt', 'w', encoding='utf-8') as f:
    f.write('BIO-502 Summary (Python implementation)\n')
    f.write('Model: P = 1/(1+exp(5*(m-1.2*d)))\n')
    f.write(f'Threshold for safe dose: {threshold}\n')
    f.write(f'Number of m points: {len(m_opt_vals)}\n')
    f.write('Generated files:\n')
    f.write('  - BIO502_results.png (2x2 subplots)\n')
    f.write('  - BIO502_opt_dose.csv (optimal dose table)\n')
    f.write('  - BIO502_summary.txt (this file)\n')

print('All done. Check BIO502_results.png and CSV.')
