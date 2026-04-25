#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:04:49 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAI-16: 金星エネルギー送信ビーム（回折限界スポット径）
@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# ============================================================
# TAG: CONFIG_START
# ============================================================

def setup_fonts():
    """日本語フォントを優先、なければ英語フォント"""
    jp_fonts = [
        'IPAexGothic', 'IPAGothic', 'Noto Sans CJK JP',
        'MS Gothic', 'Yu Gothic', 'Hiragino Sans'
    ]
    available = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for f in jp_fonts:
        if f in available:
            plt.rcParams['font.family'] = f
            plt.rcParams['font.size'] = 11
            plt.rcParams['axes.unicode_minus'] = False
            print(f"✓ 日本語フォント: {f}")
            return True
    # fallback to English
    plt.rcParams['font.size'] = 11
    print("⚠ 日本語フォントなし → English")
    return False

JAPANESE = setup_fonts()
# TAG: CONFIG_END

# ============================================================
# TAG: PARAMETERS_START
# ============================================================

# 物理定数
c = 299792458          # 光速 [m/s]
freq = 35e9            # 送信周波数 35 GHz (Kaバンド)
lam = c / freq         # 波長 [m]

# 金星軌道・送信機パラメータ
venus_orbit_radius = 108.2e9  # 金星公転半径 [m] (太陽から)
earth_orbit_radius = 149.6e9  # 地球公転半径 [m]
# 最接近時距離 (概算)
min_distance = (earth_orbit_radius - venus_orbit_radius)  # ~41.4e9 m

# 送信アンテナ直径
D_tx = 1000.0          # [m] 金星側送信アンテナ (1 km)

# ビームスポット計算 (回折限界)
# ガウシアンビームのスポット径 (1/e^2 強度)
spot_diameter_1e2 = 2 * lam * min_distance / (np.pi * D_tx) * 2  # 簡易式: θ=λ/D, spot=2θ*L
# より正確なエアリーディスク: 第1暗環直径 = 2.44 * λ * L / D
spot_diameter_airy = 2.44 * lam * min_distance / D_tx

print("="*60)
print("PAI-16: 回折限界スポット径計算")
print("="*60)
print(f"周波数: {freq/1e9:.2f} GHz")
print(f"波長:   {lam*1e3:.3f} mm")
print(f"送信アンテナ直径: {D_tx:.0f} m")
print(f"金星-地球距離(最小): {min_distance/1e9:.2f} Gm")
print(f"ガウシアンスポット径 (1/e²): {spot_diameter_1e2:.2f} m")
print(f"エアリースポット径 (第1暗環): {spot_diameter_airy:.2f} m")

# ============================================================
# TAG: PARAMETERS_END
# ============================================================

# ============================================================
# TAG: MAIN_START
# ============================================================

# 距離に対するスポット径の変化を計算
distances = np.linspace(0.4e9, 1.0e9, 200)  # 金星-地球距離範囲 [m] (例: 0.4〜1 Gm)
distances += 41e9  # オフセットして実際の範囲に
# 実際の距離範囲は最接近(41.4Gm)〜最大(約261Gm)だが、計算例として短縮

spots_gauss = 2 * lam * distances / (np.pi * D_tx) * 2
spots_airy = 2.44 * lam * distances / D_tx

# グラフ描画
fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))

ax1.plot(distances/1e9, spots_gauss, 'b-', label='Gaussian (1/e²)')
ax1.plot(distances/1e9, spots_airy, 'r--', label='Airy disk (1st null)')
ax1.set_xlabel('金星-地球距離 [Gm]')
ax1.set_ylabel('スポット径 [m]')
ax1.set_title('エネルギー送信ビーム 回折限界スポット径 (D_tx=1km)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# TAG: PLOT_END

# ============================================================
# TAG: OUTPUT_RESULTS
# ============================================================

# 結果保存ディレクトリ
os.makedirs('results', exist_ok=True)
outpath = 'results/PAI-16_params.txt'
with open(outpath, 'w') as f:
    f.write(f"# PAI-16 計算結果\n")
    f.write(f"freq={freq} Hz\n")
    f.write(f"lam={lam} m\n")
    f.write(f"D_tx={D_tx} m\n")
    f.write(f"min_distance={min_distance} m\n")
    f.write(f"spot_gauss_min={spot_diameter_1e2:.3f} m\n")
    f.write(f"spot_airy_min={spot_diameter_airy:.3f} m\n")
print(f"結果保存: {outpath}")

# TAG: MAIN_END
# (ここまで約90行、必要に応じてさらに受電アレイサイズや効率計算を追加)
