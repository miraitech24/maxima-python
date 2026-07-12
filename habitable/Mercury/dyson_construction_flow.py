#!/usr/bin/env python3
# Dyson Ring Construction Visual Chart
# 水星ダイソン環建設の資材フローを視覚的に描画

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_facecolor('#0a0a2e')
fig.patch.set_facecolor('#0a0a2e')

# === タイトル ===
ax.text(10, 11.5, 'MERCURY DYSON RING CONSTRUCTION FLOW', 
        fontsize=18, fontweight='bold', color='white', ha='center', va='center',
        fontfamily='sans-serif')

# === 拠点ボックス ===
def draw_base(x, y, w, h, color, label, sublabel, emoji):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.3",
                         facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y+0.15, f'{emoji} {label}', fontsize=13, fontweight='bold',
            color='white', ha='center', va='center', fontfamily='sans-serif')
    ax.text(x, y-0.35, sublabel, fontsize=8, color='#cccccc',
            ha='center', va='center', fontfamily='sans-serif')

# 地球
draw_base(2, 10, 3.0, 1.2, '#2e86de', 'EARTH', 'Initial Robots,精密機器,触媒', '🌍')

# 金星ヘスペラス
draw_base(5, 7.5, 3.5, 1.8, '#e67e22', 'VENUS HESPERAS', '3D Printing, Material Refining\nElectronics Manufacturing', '🪐')

# 水星地表工場
draw_base(10, 7.5, 3.5, 1.8, '#e74c3c', 'MERCURY SURFACE FACTORY', 'Mining, Panel Production\nStructure Manufacturing', '⛏️')

# 軌道上組立工場
draw_base(15, 7.5, 3.5, 1.8, '#2ecc71', 'ORBIT ASSEMBLY', 'Dyson Ring Segment Assembly\nFinal Construction', '🔧')

# ダイソン環完成
draw_base(15, 3.0, 3.5, 1.2, '#f1c40f', 'DYSON RING COMPLETE', '1.2 PW Power Generation Start', '☀️')

# プロキシマb
draw_base(15, 0.5, 3.0, 0.8, '#9b59b6', 'PROXIMA b', '0.2c Voyage Target', '⭐')

# === 矢印（資材の流れ） ===
def draw_arrow(x1, y1, x2, y2, color, label, style='arc3,rad=0.2'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5,
                                connectionstyle=style, linestyle='solid'))
    mx, my = (x1+x2)/2, (y1+y2)/2 + 0.3
    ax.text(mx, my, label, fontsize=8, color=color, ha='center', va='center',
            fontfamily='sans-serif', fontweight='bold')

# 地球→ヘスペラス
draw_arrow(3.5, 9.4, 5, 8.5, '#85c1e9', 'Rocket Transport', 'arc3,rad=0.1')

# ヘスペラス→水星（レールガン）
draw_arrow(6.8, 6.8, 8.5, 6.8, '#f5b041', 'RAILGUN\nRefined Materials', 'arc3,rad=0.0')

# ヘスペラス→軌道（レールガン）
draw_arrow(6.8, 8.2, 13.5, 8.2, '#f5b041', 'RAILGUN\nElectronics,精密機器', 'arc3,rad=0.0')

# 水星→軌道（マスドライバー）
draw_arrow(11.8, 6.8, 13.5, 6.8, '#48c9b0', 'MASS DRIVER\nBulk Materials (10t/shot)', 'arc3,rad=0.0')

# 水星→軌道（レールガン）
draw_arrow(11.8, 8.2, 13.5, 8.2, '#f5b041', 'RAILGUN\nCompleted Panels', 'arc3,rad=0.0')

# 軌道→ダイソン環完成
draw_arrow(15, 6.6, 15, 4.2, '#f1c40f', 'Self-Deploy', 'arc3,rad=0.0')

# ダイソン環→プロキシマb
draw_arrow(15, 2.4, 15, 1.3, '#bb8fce', '0.2c Laser Propulsion\n(21 years voyage)', 'arc3,rad=0.0')

# === エレベータ（点線） ===
ax.annotate('', xy=(10, 5.7), xytext=(10, 8.5),
            arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5,
                            connectionstyle='arc3,rad=0.0', linestyle='dashed'))
ax.text(10.3, 7.1, 'Space Elevator\n(Personnel, Maintenance)', fontsize=7, color='#7f8c8d',
        ha='left', va='center', fontfamily='sans-serif')

# === 注釈ボックス ===
note_box = FancyBboxPatch((0.5, 0.2), 6, 2.5, boxstyle="round,pad=0.3",
                          facecolor='#1a1a4e', edgecolor='#34495e', linewidth=1.5, alpha=0.8)
ax.add_patch(note_box)
ax.text(3.5, 2.2, 'TRANSPORT METHODS', fontsize=11, fontweight='bold',
        color='white', ha='center', va='center', fontfamily='sans-serif')

methods = [
    ('RAILGUN', '6 km/s, 1t/shot, 100 shots/day\nCompleted panels, precision parts', '#f5b041'),
    ('MASS DRIVER', '3 km/s, 10t/shot, 50 shots/day\nBulk materials, ores', '#48c9b0'),
    ('SPACE ELEVATOR', '50 m/s, 5t/trip, 10 trips/day\nPersonnel, maintenance', '#7f8c8d'),
]
for i, (name, desc, color) in enumerate(methods):
    y_pos = 1.6 - i * 0.7
    ax.text(1.0, y_pos, f'● {name}', fontsize=9, fontweight='bold',
            color=color, ha='left', va='center', fontfamily='sans-serif')
    ax.text(3.5, y_pos, desc, fontsize=7, color='#cccccc',
            ha='left', va='center', fontfamily='sans-serif')

# === フェーズタイムライン（下部） ===
timeline_y = 11.0
ax.text(10, timeline_y+0.3, 'CONSTRUCTION PHASES', fontsize=11, fontweight='bold',
        color='white', ha='center', va='center', fontfamily='sans-serif')

phases = [
    (0, 5, '#95a5a6', 'Tech Dev'),
    (5, 7, '#5dade2', 'Initial Deploy'),
    (7, 9, '#2e86c1', 'Factory Build'),
    (9, 11, '#27ae60', 'Material Prod'),
    (11, 13, '#f39c12', 'Panel Mfg'),
    (13, 16, '#e74c3c', 'Orbit Assembly'),
    (16, 18, '#8e44ad', 'Complete'),
    (18, 20, '#c0392b', 'Departure'),
]

for start, end, color, label in phases:
    w = end - start
    rect = FancyBboxPatch((start, timeline_y-0.3), w, 0.6, boxstyle="round,pad=0.05",
                          facecolor=color, edgecolor='white', linewidth=0.5, alpha=0.8)
    ax.add_patch(rect)
    ax.text(start + w/2, timeline_y, label, fontsize=6, fontweight='bold',
            color='white', ha='center', va='center', fontfamily='sans-serif')

# 年数目盛り
for year in range(0, 21, 2):
    ax.text(year, timeline_y-0.5, str(year), fontsize=6, color='#cccccc',
            ha='center', va='center', fontfamily='sans-serif')

# === 凡例 ===
legend_elements = [
    mpatches.Patch(color='#f5b041', label='Railgun (6km/s)'),
    mpatches.Patch(color='#48c9b0', label='Mass Driver (3km/s)'),
    mpatches.Patch(color='#7f8c8d', label='Space Elevator'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8,
          facecolor='#1a1a4e', edgecolor='white', labelcolor='white')

# === 保存 ===
plt.tight_layout()
plt.savefig('/home/iwamura/ドキュメント/coupling/work_paiとhabitable/dyson_construction_flow.png',
            dpi=200, bbox_inches='tight', facecolor='#0a0a2e')
print("=== 保存完了: dyson_construction_flow.png ===")
print("=== 水星ダイソン環建設フロー図を出力しました ===")