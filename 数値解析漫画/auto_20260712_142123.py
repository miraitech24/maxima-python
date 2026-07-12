#!/usr/bin/env python3
# O'Neill Cylinder Concept Drawings
# 1. Cross-section diagram
# 2. Interior landscape concept
# 3. Configuration diagram

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import numpy as np

output_dir = "/home/iwamura/ドキュメント/coupling/work_paiとhabitable"

# ============================================================
# Figure 1: Cross-section diagram of O'Neill Cylinder
# ============================================================
fig1, ax1 = plt.subplots(1, 1, figsize=(10, 8))
ax1.set_xlim(-6, 6)
ax1.set_ylim(-6, 6)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_facecolor('#f0f4f8')
fig1.patch.set_facecolor('#f0f4f8')

ax1.set_title('O\'Neill Cylinder Cross-Section', fontsize=16, fontweight='bold', color='#2c3e50', pad=20)

# Outer hull (cylinder cross-section - circle)
outer_hull = Circle((0, 0), 5.0, fill=False, edgecolor='#2c3e50', linewidth=3, linestyle='-')
ax1.add_patch(outer_hull)

# Inner hull
inner_hull = Circle((0, 0), 4.8, fill=False, edgecolor='#7f8c8d', linewidth=1.5, linestyle='--')
ax1.add_patch(inner_hull)

# Radiation shield layer
shield = Circle((0, 0), 4.5, fill=False, edgecolor='#e67e22', linewidth=2, linestyle=':', alpha=0.7)
ax1.add_patch(shield)

# Interior landscape (green arc for ground)
theta = np.linspace(-np.pi/2, np.pi/2, 100)
ground_x = 4.0 * np.cos(theta)
ground_y = 4.0 * np.sin(theta)
ax1.fill(ground_x, ground_y, color='#27ae60', alpha=0.3, label='Agricultural Land')

# Upper sky (blue arc)
theta2 = np.linspace(np.pi/2, 3*np.pi/2, 100)
sky_x = 4.0 * np.cos(theta2)
sky_y = 4.0 * np.sin(theta2)
ax1.fill(sky_x, sky_y, color='#85c1e9', alpha=0.15, label='Sky / Atmosphere')

# Central axis
ax1.plot([-0.5, 0.5], [0, 0], color='#e74c3c', linewidth=2, marker='o', markersize=6)
ax1.text(0, 0.3, 'Central Axis (Zero-G)', fontsize=9, ha='center', color='#e74c3c')

# Rotation direction arrow
arrow = FancyArrowPatch((0, 4.2), (0.8, 4.0), arrowstyle='->', color='#2980b9', lw=2)
ax1.add_patch(arrow)
ax1.text(1.0, 4.3, 'Rotation → 1G', fontsize=9, color='#2980b9')

# Labels
ax1.text(0, -4.5, 'Inner Surface (Living Area)', fontsize=10, ha='center', color='#27ae60', fontweight='bold')
ax1.text(0, -5.2, 'Hull Structure (Carbon Nanotube)', fontsize=9, ha='center', color='#2c3e50')
ax1.text(0, -5.8, 'Radiation Shield (Water/Regolith)', fontsize=9, ha='center', color='#e67e22')

# Dimensions
ax1.annotate('', xy=(0, 0), xytext=(5, 0), arrowprops=dict(arrowstyle='<->', color='#7f8c8d', lw=1.5))
ax1.text(2.5, -0.5, 'Radius: 5km', fontsize=9, ha='center', color='#7f8c8d')

# Window strips
for angle in [30, 60, 120, 150]:
    rad = np.radians(angle)
    wx = 4.8 * np.cos(rad)
    wy = 4.8 * np.sin(rad)
    ax1.plot(wx, wy, 'o', color='#3498db', markersize=4, alpha=0.6)

ax1.text(4.0, 3.0, 'Window Strips', fontsize=8, color='#3498db')

plt.tight_layout()
plt.savefig(f'{output_dir}/oneill_cylinder_cross_section.png', dpi=200, bbox_inches='tight', facecolor='#f0f4f8')
print(f"Saved: {output_dir}/oneill_cylinder_cross_section.png")

# ============================================================
# Figure 2: Interior landscape concept
# ============================================================
fig2, ax2 = plt.subplots(1, 1, figsize=(12, 6))
ax2.set_xlim(0, 12)
ax2.set_ylim(0, 6)
ax2.axis('off')
ax2.set_facecolor('#e8f4f8')
fig2.patch.set_facecolor('#e8f4f8')

ax2.set_title('O\'Neill Cylinder Interior Landscape', fontsize=16, fontweight='bold', color='#2c3e50', pad=20)

# Sky gradient
for i in range(100):
    y = i / 100 * 6
    alpha = 0.3 + 0.5 * (1 - i/100)
    ax2.axhspan(y, y+0.06, xmin=0, xmax=1, color='#85c1e9', alpha=alpha*0.3)

# Curved ground (perspective)
ground_points = np.array([
    [0, 0.5], [1, 0.6], [2, 0.7], [3, 0.8], [4, 0.9], [5, 1.0],
    [6, 1.1], [7, 1.2], [8, 1.3], [9, 1.4], [10, 1.5], [11, 1.6], [12, 1.7]
])
ax2.fill_between(ground_points[:, 0], 0, ground_points[:, 1], color='#27ae60', alpha=0.6)
ax2.plot(ground_points[:, 0], ground_points[:, 1], color='#1e8449', linewidth=2)

# River
river_x = np.linspace(2, 10, 50)
river_y = 0.8 + 0.3 * np.sin(river_x * 0.8) + 0.1 * river_x / 10
ax2.fill_between(river_x, 0, river_y, color='#3498db', alpha=0.4)
ax2.plot(river_x, river_y, color='#2980b9', linewidth=1.5)

# Buildings
buildings = [
    (1.5, 0.8, 0.4, 0.6, '#e74c3c'),
    (3.0, 1.0, 0.5, 0.8, '#e67e22'),
    (4.5, 1.2, 0.6, 1.0, '#f39c12'),
    (6.5, 1.4, 0.4, 0.7, '#2ecc71'),
    (8.0, 1.6, 0.5, 0.9, '#3498db'),
    (9.5, 1.8, 0.3, 0.5, '#9b59b6'),
]
for bx, by, bw, bh, color in buildings:
    rect = Rectangle((bx-bw/2, by), bw, bh, facecolor=color, edgecolor='white', linewidth=1, alpha=0.8)
    ax2.add_patch(rect)
    # Window
    for wy in [by+0.2, by+0.5]:
        for wx in [bx-0.15, bx, bx+0.15]:
            if 0.1 < bw/2:
                ax2.plot(wx, wy, 'o', color='white', markersize=2, alpha=0.7)

# Trees
for tx in [2.5, 5.5, 7.5, 10.5]:
    tree = Circle((tx, 0.7 + 0.2 * np.random.random()), 0.15, color='#1e8449', alpha=0.7)
    ax2.add_patch(tree)
    tree_top = Circle((tx, 0.85 + 0.2 * np.random.random()), 0.2, color='#27ae60', alpha=0.6)
    ax2.add_patch(tree_top)

# People (small dots)
people_x = [2.0, 3.5, 5.0, 7.0, 9.0]
people_y = [0.7, 0.9, 1.1, 1.3, 1.5]
for px, py in zip(people_x, people_y):
    ax2.plot(px, py, 'o', color='#2c3e50', markersize=4)
    ax2.plot(px, py-0.08, 'o', color='#2c3e50', markersize=3)

# Labels
ax2.text(6, 5.5, 'Artificial Sky with Clouds', fontsize=10, ha='center', color='#2980b9', fontweight='bold')
ax2.text(6, 5.0, 'Sunlight from Central Mirror', fontsize=9, ha='center', color='#f39c12')

# Sunlight rays
for rx in [2, 4, 6, 8, 10]:
    ax2.plot([rx, rx+0.3], [5.5, 4.5], color='#f1c40f', linewidth=0.5, alpha=0.4)

ax2.text(1.5, 0.3, 'Housing', fontsize=8, color='#e74c3c')
ax2.text(4.5, 0.5, 'River', fontsize=8, color='#2980b9')
ax2.text(7.5, 0.3, 'Agriculture', fontsize=8, color='#27ae60')
ax2.text(10, 0.3, 'Park', fontsize=8, color='#1e8449')

plt.tight_layout()
plt.savefig(f'{output_dir}/oneill_cylinder_interior.png', dpi=200, bbox_inches='tight', facecolor='#e8f4f8')
print(f"Saved: {output_dir}/oneill_cylinder_interior.png")

# ============================================================
# Figure 3: Configuration diagram (multiple cylinders)
# ============================================================
fig3, ax3 = plt.subplots(1, 1, figsize=(12, 8))
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 8)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_facecolor('#f5f6fa')
fig3.patch.set_facecolor('#f5f6fa')

ax3.set_title('O\'Neill Cylinder Cluster Configuration', fontsize=16, fontweight='bold', color='#2c3e50', pad=20)

# Draw multiple cylinders
cylinder_data = [
    (2, 4, 0, 'Cylinder A\nResidential'),
    (5, 4, 0, 'Cylinder B\nAgriculture'),
    (8, 4, 0, 'Cylinder C\nIndustrial'),
    (11, 4, 0, 'Cylinder D\nCommercial'),
]

for cx, cy, angle, label in cylinder_data:
    # Cylinder body (ellipse for perspective)
    ellipse = plt.matplotlib.patches.Ellipse((cx, cy), 1.8, 0.8, angle=angle,
                                              facecolor='#3498db', edgecolor='#2c3e50', linewidth=2, alpha=0.7)
    ax3.add_patch(ellipse)
    
    # End cap
    cap = plt.matplotlib.patches.Ellipse((cx-0.9, cy), 0.3, 0.8, angle=angle,
                                          facecolor='#2980b9', edgecolor='#2c3e50', linewidth=1.5)
    ax3.add_patch(cap)
    
    # Solar panel wings
    panel1 = Rectangle((cx-0.5, cy+0.5), 0.3, 1.0, facecolor='#f39c12', edgecolor='#e67e22', alpha=0.8)
    ax3.add_patch(panel1)
    panel2 = Rectangle((cx+0.2, cy+0.5), 0.3, 1.0, facecolor='#f39c12', edgecolor='#e67e22', alpha=0.8)
    ax3.add_patch(panel2)
    
    # Label
    ax3.text(cx, cy-1.2, label, fontsize=9, ha='center', color='#2c3e50', fontweight='bold')

# Connecting hub
hub = Circle((6.5, 4), 0.5, facecolor='#e74c3c', edgecolor='#c0392b', linewidth=2, alpha=0.8)
ax3.add_patch(hub)
ax3.text(6.5, 4, 'Hub', fontsize=8, ha='center', color='white', fontweight='bold')

# Connection lines
for cx, cy, _, _ in cylinder_data:
    ax3.plot([cx-0.5, 6.0], [cy, 4], color='#7f8c8d', linewidth=1.5, linestyle='--', alpha=0.5)

# Wormhole portal
portal = Circle((13, 4), 0.6, facecolor='#9b59b6', edgecolor='#8e44ad', linewidth=2, alpha=0.6)
ax3.add_patch(portal)
ax3.text(13, 4, 'WH', fontsize=10, ha='center', color='white', fontweight='bold')
ax3.text(13, 3.2, 'Wormhole\nPortal', fontsize=8, ha='center', color='#8e44ad')

# Arrow to wormhole
arrow_wh = FancyArrowPatch((11.9, 4), (12.4, 4), arrowstyle='->', color='#9b59b6', lw=2)
ax3.add_patch(arrow_wh)

# Alpha Centauri A star
star = Circle((13, 7), 0.8, facecolor='#f1c40f', edgecolor='#f39c12', linewidth=2, alpha=0.8)
ax3.add_patch(star)
ax3.text(13, 7, 'α Cen A', fontsize=10, ha='center', color='#e67e22', fontweight='bold')

# Light rays from star
for angle in [30, 60, 120, 150, 210, 240, 300, 330]:
    rad = np.radians(angle)
    ax3.plot([13, 13 + 0.5*np.cos(rad)], [7, 7 + 0.5*np.sin(rad)],
             color='#f1c40f', linewidth=0.5, alpha=0.3)

# Distance label
ax3.text(13, 6.0, 'Distance: 4.37 ly', fontsize=8, ha='center', color='#7f8c8d')

# Legend
legend_elements = [
    mpatches.Patch(color='#3498db', alpha=0.7, label='O\'Neill Cylinder'),
    mpatches.Patch(color='#f39c12', alpha=0.8, label='Solar Panels'),
    mpatches.Patch(color='#e74c3c', alpha=0.8, label='Central Hub'),
    mpatches.Patch(color='#9b59b6', alpha=0.6, label='Wormhole Portal'),
]
ax3.legend(handles=legend_elements, loc='lower left', fontsize=9,
           facecolor='white', edgecolor='#bdc3c7', labelcolor='#2c3e50')

# Title info
ax3.text(7, 7.5, '100km spacing between cylinders', fontsize=9, ha='center', color='#7f8c8d', style='italic')
ax3.text(7, 7.0, 'Total: 600,000 units possible in HZ', fontsize=9, ha='center', color='#7f8c8d', style='italic')

plt.tight_layout()
plt.savefig(f'{output_dir}/oneill_cylinder_configuration.png', dpi=200, bbox_inches='tight', facecolor='#f5f6fa')
print(f"Saved: {output_dir}/oneill_cylinder_configuration.png")

print("=== All 3 diagrams saved successfully ===")