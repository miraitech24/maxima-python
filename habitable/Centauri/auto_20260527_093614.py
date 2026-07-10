import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ===== 日本語フォント自動検出 =====
def setup_japanese_font():
    jp_font_candidates = [
        'Noto Sans CJK JP', 'Noto Sans CJK SC', 'IPAexGothic', 'IPAGothic',
        'TakaoGothic', 'TakaoExGothic', 'VL Gothic', 'Yu Gothic', 'YuGothic',
        'MS Gothic', 'Meiryo', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN',
        'Osaka', 'Kochi Gothic', 'MigMix 1P', 'Sazanami Gothic',
        'MotoyaLCedar', 'Droid Sans Japanese', 'Source Han Sans JP', 'Source Han Sans',
    ]
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for candidate in jp_font_candidates:
        if candidate in available_fonts:
            print(f"日本語フォント検出: {candidate}")
            return candidate
    print("日本語フォントが見つかりません。英語フォントを使用します。")
    return 'DejaVu Sans'

jp_font = setup_japanese_font()
plt.rcParams['font.family'] = jp_font
plt.rcParams['axes.unicode_minus'] = False

# ===== C101: 大型筐体構造解析（応力・歪み） =====

# --- 機体諸元 ---
L = 20.0       # 全長 [m]
W = 8.0        # 全幅 [m]
H = 6.0        # 全高 [m]
M_total = 100e3  # 総重量 [kg] (100トン)
g_proxima = 3.9  # プロキシマbの重力加速度 [m/s^2] (0.4G)

# --- 材料特性 ---
materials = {
    'Al7075': {'E': 71e9, 'sigma_y': 570e6, 'rho': 2700, 'name': 'アルミ合金 7075'},
    'CFRP':   {'E': 230e9, 'sigma_y': 3500e6, 'rho': 1600, 'name': '炭素繊維複合材'},
    'Ti6Al4V':{'E': 114e9, 'sigma_y': 1200e6, 'rho': 4430, 'name': 'チタン合金'},
    'Maraging':{'E': 190e9, 'sigma_y': 2000e6, 'rho': 8000, 'name': 'マルエージング鋼'},
}

# --- 荷重条件 ---
# 自重による曲げ応力（片持ち梁近似：アーム基部）
F_self = M_total * g_proxima  # 自重による力 [N]
L_arm = 8.0  # アーム長さ [m]（想定）
M_bend = F_self * L_arm  # 曲げモーメント [Nm]

# 断面係数（矩形断面を仮定）
b = 2.0   # 断面幅 [m]
h = 1.5   # 断面高さ [m]
Z = (b * h**2) / 6  # 断面係数 [m^3]

# 安全率
safety_factor = 2.0

print("===== C101: 大型筐体構造解析 =====")
print(f"機体サイズ: {L}m x {W}m x {H}m")
print(f"総重量: {M_total/1000:.0f} トン")
print(f"プロキシマb重力: {g_proxima:.1f} m/s²")
print(f"自重による力: {F_self/1000:.1f} kN")
print(f"曲げモーメント: {M_bend/1000:.1f} kNm")
print(f"断面係数: {Z:.3f} m³")
print()

# --- 各材料の応力評価 ---
results = []
for key, mat in materials.items():
    sigma_bending = M_bend / Z  # 曲げ応力 [Pa]
    sigma_allowable = mat['sigma_y'] / safety_factor  # 許容応力 [Pa]
    margin = (sigma_allowable - sigma_bending) / sigma_allowable * 100  # 余裕 [%]
    weight_estimate = M_total * mat['rho'] / 2700  # アルミ比での重量推定
    results.append({
        'name': mat['name'],
        'E': mat['E'],
        'sigma_y': mat['sigma_y'],
        'sigma_bending': sigma_bending,
        'sigma_allowable': sigma_allowable,
        'margin': margin,
        'weight_ratio': mat['rho'] / 2700,
        'weight_estimate': weight_estimate,
    })
    print(f"材料: {mat['name']}")
    print(f"  ヤング率: {mat['E']/1e9:.0f} GPa")
    print(f"  降伏応力: {mat['sigma_y']/1e6:.0f} MPa")
    print(f"  曲げ応力: {sigma_bending/1e6:.2f} MPa")
    print(f"  許容応力: {sigma_allowable/1e6:.2f} MPa")
    print(f"  余裕: {margin:.1f}%")
    print(f"  重量比(Al基準): {mat['rho']/2700:.2f}")
    print()

# --- グラフ1: 材料比較（棒グラフ） ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

names = [r['name'] for r in results]
sigmas = [r['sigma_bending']/1e6 for r in results]
allowables = [r['sigma_allowable']/1e6 for r in results]
margins = [r['margin'] for r in results]
weights = [r['weight_ratio'] for r in results]

# 左上: 曲げ応力 vs 許容応力
x = np.arange(len(names))
width = 0.35
axes[0,0].bar(x - width/2, sigmas, width, label='曲げ応力', color='tomato')
axes[0,0].bar(x + width/2, allowables, width, label='許容応力', color='steelblue')
axes[0,0].axhline(0, color='gray', linewidth=0.5)
axes[0,0].set_xticks(x)
axes[0,0].set_xticklabels(names, fontsize=9)
axes[0,0].set_ylabel('応力 [MPa]')
axes[0,0].set_title('曲げ応力と許容応力の比較')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# 右上: 安全余裕
colors = ['green' if m > 50 else 'orange' if m > 0 else 'red' for m in margins]
axes[0,1].bar(names, margins, color=colors)
axes[0,1].axhline(0, color='gray', linewidth=0.5)
axes[0,1].set_ylabel('安全余裕 [%]')
axes[0,1].set_title('材料別 安全余裕')
axes[0,1].grid(True, alpha=0.3)

# 左下: 重量比
axes[1,0].bar(names, weights, color='lightgreen')
axes[1,0].set_ylabel('重量比 (Al基準)')
axes[1,0].set_title('材料別 重量比較')
axes[1,0].grid(True, alpha=0.3)

# 右下: スロート半径と通過可能サイズ
radii = np.linspace(0.1, 5.0, 100)
max_size = radii * 2  # 通過可能な最大サイズ（直径）
energy_density = 4.815e42 / radii**2  # 必要エネルギー密度

ax = axes[1,1]
ax.plot(radii, max_size, 'b-', linewidth=2, label='通過可能サイズ')
ax.axhline(1.5, color='r', linestyle='--', label='部品モジュールサイズ(1.5m)')
ax.axvline(1.0, color='g', linestyle=':', label='現状スロート半径(1.0m)')
ax.set_xlabel('スロート半径 [m]')
ax.set_ylabel('通過可能サイズ [m]')
ax.set_title('スロート半径と通過可能サイズ')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c101_structure_analysis.png', dpi=150)
plt.close()

# --- サマリーファイル出力 ---
with open('c101_summary.md', 'w', encoding='utf-8') as f:
    f.write("# C101: 大型筐体構造解析（応力・歪み）\n\n")
    f.write("## 機体諸元\n\n")
    f.write(f"- 全長: {L} m\n")
    f.write(f"- 全幅: {W} m\n")
    f.write(f"- 全高: {H} m\n")
    f.write(f"- 総重量: {M_total/1000:.0f} トン\n")
    f.write(f"- 重力: {g_proxima:.1f} m/s² (0.4G)\n\n")
    f.write("## 材料比較\n\n")
    f.write("| 材料 | ヤング率 [GPa] | 降伏応力 [MPa] | 曲げ応力 [MPa] | 許容応力 [MPa] | 安全余裕 [%] | 重量比 |\n")
    f.write("|------|---------------|---------------|---------------|---------------|-------------|-------|\n")
    for r in results:
        f.write(f"| {r['name']} | {r['E']/1e9:.0f} | {r['sigma_y']/1e6:.0f} | {r['sigma_bending']/1e6:.2f} | {r['sigma_allowable']/1e6:.2f} | {r['margin']:.1f} | {r['weight_ratio']:.2f} |\n")
    f.write("\n## 考察\n\n")
    f.write("### 材料選定\n\n")
    f.write("**推奨: アルミ合金 7075 を主構造に採用。**\n\n")
    f.write("理由:\n")
    f.write("1. 全ての材料で曲げ応力に対して十分な安全余裕がある。\n")
    f.write("2. アルミ合金は現地生産が可能（プロキシマbの砂から精製）。\n")
    f.write("3. リサイクルが容易で、自己複製ロボットによる製造に適する。\n")
    f.write("4. CFRPは軽量だが現地生産が困難。地球からの輸入に頼ることになる。\n\n")
    f.write("### スロート通過制約\n\n")
    f.write("現状のスロート半径1.0mでは、1.5mの部品モジュールを通すことができない。\n")
    f.write("そのため、筐体は現地で3Dプリンタにより製造し、\n")
    f.write("地球からは制御用半導体のみを転送する戦略が現実的。\n")

# --- CSV結果ファイル出力 ---
with open('c101_results.csv', 'w', encoding='utf-8') as f:
    f.write("材料,ヤング率[GPa],降伏応力[MPa],曲げ応力[MPa],許容応力[MPa],安全余裕[%],重量比\n")
    for r in results:
        f.write(f"{r['name']},{r['E']/1e9:.0f},{r['sigma_y']/1e6:.0f},{r['sigma_bending']/1e6:.2f},{r['sigma_allowable']/1e6:.2f},{r['margin']:.1f},{r['weight_ratio']:.2f}\n")

print("グラフ: c101_structure_analysis.png")
print("サマリー: c101_summary.md")
print("CSV: c101_results.csv")
print("============================================")