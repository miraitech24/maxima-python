#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_20260831_110752: シェル厚計算とグラフ描画（3D + subplot版）
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# フォント設定（日本語対応）
# ============================================================

def setup_fonts():
    """日本語フォントを設定"""
    font_candidates = [
        'IPA Gothic', 'IPAGothic', 'Noto Sans CJK JP',
        'Noto Sans Japanese', 'VL Gothic', 'TakaoGothic',
        'Hiragino Sans', 'Meiryo', 'sans-serif'
    ]
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    font_found = None
    for font in font_candidates:
        if font in available_fonts:
            font_found = font
            break
    
    if font_found:
        print(f"✅ 日本語フォントを使用: {font_found}")
        plt.rcParams['font.family'] = font_found
    else:
        print("⚠️ 日本語フォントが見つかりません。英語で表示します。")
        plt.rcParams['font.family'] = 'sans-serif'
    
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 9
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['figure.titlesize'] = 13
    
    return font_found


# ============================================================
# 計算関数
# ============================================================

def calculate_shell(D_km, R_shield, rho=2.7):
    """
    シェル厚と総質量を計算
    
    Parameters:
    - D_km: シェル直径 [km]
    - R_shield: シールド効率 [g/cm²]
    - rho: 密度 [g/cm³]（デフォルト: アルミニウム 2.7）
    
    Returns:
    - d_cm: シェル厚 [cm]
    - M_kg: 総質量 [kg]
    """
    d_cm = np.sqrt(D_km) * R_shield
    R_cm = (D_km * 100000) / 2  # km → cm
    V_cm3 = 4 * np.pi * R_cm**2 * d_cm
    M_kg = V_cm3 * rho / 1000  # g → kg
    return d_cm, M_kg


# ============================================================
# 3Dグラフ用データ生成
# ============================================================

def generate_3d_data():
    """3Dプロット用のデータを生成"""
    D_grid = np.linspace(1, 50, 30)
    R_grid = np.linspace(0.05, 0.5, 30)
    D_mesh, R_mesh = np.meshgrid(D_grid, R_grid)
    
    d_mesh = np.zeros_like(D_mesh)
    M_mesh = np.zeros_like(D_mesh)
    
    for i in range(D_mesh.shape[0]):
        for j in range(D_mesh.shape[1]):
            d_mesh[i, j], M_mesh[i, j] = calculate_shell(D_mesh[i, j], R_mesh[i, j])
    
    return D_mesh, R_mesh, d_mesh, M_mesh


# ============================================================
# グラフ描画（3D + subplot統合版）
# ============================================================

def plot_results():
    """全てのグラフをsubplotで統合表示（3D含む）"""
    
    # パラメータ
    D_km = 10
    R_shield = 0.1
    rho = 2.7
    
    # 基本計算
    d_cm, M_kg = calculate_shell(D_km, R_shield, rho)
    
    print("\n" + "=" * 50)
    print("  シェル厚計算結果")
    print("=" * 50)
    print(f"  シェル直径:   {D_km} km")
    print(f"  シールド効率: {R_shield} g/cm²")
    print(f"  密度:         {rho} g/cm³ (アルミニウム)")
    print("-" * 50)
    print(f"  シェル厚:     {d_cm:.4f} cm")
    print(f"  総質量:       {M_kg:.2e} kg")
    print(f"  総質量:       {M_kg/1000:.2e} トン")
    print("=" * 50)
    
    # ---- データ準備 ----
    D_range = np.linspace(1, 60, 100)
    R_range = np.linspace(0.01, 1.0, 100)
    
    # 直径依存性
    d_D = [calculate_shell(D, R_shield)[0] for D in D_range]
    M_D = [calculate_shell(D, R_shield)[1] / 1e9 for D in D_range]
    
    # シールド効率依存性
    d_R = [calculate_shell(D_km, R)[0] for R in R_range]
    M_R = [calculate_shell(D_km, R)[1] / 1e9 for R in R_range]
    
    # 3Dデータ
    D_mesh, R_mesh, d_mesh, M_mesh = generate_3d_data()
    
    # ---- 2行3列のsubplot（3D含む） ----
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('シェル厚計算 - パラメータ依存性（3D + 2D）', fontsize=16, fontweight='bold')
    
    # グラフ1: 直径 vs シェル厚 (1,1)
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(D_range, d_D, 'b-', linewidth=2)
    ax1.set_xlabel('シェル直径 [km]')
    ax1.set_ylabel('シェル厚 [cm]')
    ax1.set_title('直径 vs シェル厚')
    ax1.grid(True, alpha=0.3)
    
    # グラフ2: 直径 vs 総質量 (1,2)
    ax2 = plt.subplot(2, 3, 2)
    ax2.plot(D_range, M_D, 'r-', linewidth=2)
    ax2.set_xlabel('シェル直径 [km]')
    ax2.set_ylabel('総質量 [10^9 kg]')
    ax2.set_title('直径 vs 総質量')
    ax2.grid(True, alpha=0.3)
    
    # グラフ3: シールド効率 vs シェル厚 (1,3)
    ax3 = plt.subplot(2, 3, 3)
    ax3.plot(R_range, d_R, 'g-', linewidth=2)
    ax3.set_xlabel('シールド効率 [g/cm²]')
    ax3.set_ylabel('シェル厚 [cm]')
    ax3.set_title('効率 vs シェル厚')
    ax3.grid(True, alpha=0.3)
    
    # グラフ4: 3Dサーフェス (2,1) - シェル厚
    ax4 = fig.add_subplot(2, 3, 4, projection='3d')
    surf1 = ax4.plot_surface(D_mesh, R_mesh, d_mesh, cmap='viridis', alpha=0.8)
    ax4.set_xlabel('直径 [km]')
    ax4.set_ylabel('効率 [g/cm²]')
    ax4.set_zlabel('シェル厚 [cm]')
    ax4.set_title('3D: シェル厚')
    fig.colorbar(surf1, ax=ax4, shrink=0.6, aspect=20, label='厚 [cm]')
    
    # グラフ5: 3Dサーフェス (2,2) - 総質量（対数）
    ax5 = fig.add_subplot(2, 3, 5, projection='3d')
    M_mesh_log = np.log10(M_mesh + 1)
    surf2 = ax5.plot_surface(D_mesh, R_mesh, M_mesh_log, cmap='plasma', alpha=0.8)
    ax5.set_xlabel('直径 [km]')
    ax5.set_ylabel('効率 [g/cm²]')
    ax5.set_zlabel('log10(質量 [kg])')
    ax5.set_title('3D: 総質量 [log10]')
    fig.colorbar(surf2, ax=ax5, shrink=0.6, aspect=20, label='log10(kg)')
    
    # グラフ6: 比較グラフ（2軸） (2,3)
    ax6 = plt.subplot(2, 3, 6)
    ax6b = ax6.twinx()
    
    line1 = ax6.plot(D_range, d_D, 'b-', linewidth=2, label='シェル厚 [cm]')
    line2 = ax6b.plot(D_range, M_D, 'r-', linewidth=2, label='総質量 [10^9 kg]')
    
    ax6.set_xlabel('シェル直径 [km]')
    ax6.set_ylabel('シェル厚 [cm]', color='blue')
    ax6b.set_ylabel('総質量 [10^9 kg]', color='red')
    ax6.tick_params(axis='y', labelcolor='blue')
    ax6b.tick_params(axis='y', labelcolor='red')
    ax6.set_title('直径依存性（比較）')
    ax6.grid(True, alpha=0.3)
    
    # 凡例をまとめる
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax6.legend(lines, labels, loc='upper left', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('shell_analysis_3d.png', dpi=150, bbox_inches='tight')
    print("✅ shell_analysis_3d.png (2D+3D統合)")
    plt.show()
    
    # ---- 3Dグラフのみの別バージョン（より詳細） ----
    fig3d = plt.figure(figsize=(14, 6))
    fig3d.suptitle('3Dパラメータマップ', fontsize=14, fontweight='bold')
    
    # 左: シェル厚
    ax7 = fig3d.add_subplot(1, 2, 1, projection='3d')
    surf3 = ax7.plot_surface(D_mesh, R_mesh, d_mesh, cmap='viridis', alpha=0.9)
    ax7.set_xlabel('直径 [km]')
    ax7.set_ylabel('効率 [g/cm²]')
    ax7.set_zlabel('シェル厚 [cm]')
    ax7.set_title('シェル厚の3Dマップ')
    fig3d.colorbar(surf3, ax=ax7, shrink=0.6, aspect=20, label='厚 [cm]')
    
    # 右: 総質量（対数）
    ax8 = fig3d.add_subplot(1, 2, 2, projection='3d')
    surf4 = ax8.plot_surface(D_mesh, R_mesh, M_mesh_log, cmap='plasma', alpha=0.9)
    ax8.set_xlabel('直径 [km]')
    ax8.set_ylabel('効率 [g/cm²]')
    ax8.set_zlabel('log10(質量 [kg])')
    ax8.set_title('総質量の3Dマップ [log10]')
    fig3d.colorbar(surf4, ax=ax8, shrink=0.6, aspect=20, label='log10(kg)')
    
    plt.tight_layout()
    plt.savefig('shell_3d_only.png', dpi=150, bbox_inches='tight')
    print("✅ shell_3d_only.png (3Dのみ)")
    plt.show()
    
    # ---- パラメータスイープのテーブル出力 ----
    print("\n" + "=" * 60)
    print("  パラメータスイープ結果")
    print("=" * 60)
    print()
    print("【直径 vs シェル厚】")
    print("  直径[km]  シェル厚[cm]  総質量[kg]")
    print("  -----------------------------------")
    
    for D in [5, 10, 15, 20, 30, 50]:
        d, M = calculate_shell(D, R_shield)
        print(f"  {D:4.0f}       {d:8.4f}      {M:12.2e}")
    
    print()
    print("【シールド効率 vs シェル厚】")
    print("  効率[g/cm²]  シェル厚[cm]  総質量[kg]")
    print("  --------------------------------------")
    
    for R in [0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
        d, M = calculate_shell(D_km, R)
        print(f"  {R:5.2f}        {d:8.4f}      {M:12.2e}")
    
    print()
    print("=" * 60)
    
    # ---- 結論 ----
    print("\n" + "=" * 50)
    print("  結論")
    print("=" * 50)
    print()
    print(f"1. シェル厚は直径の平方根に比例: d_cm = {R_shield:.1f} * sqrt(D_km)")
    print("2. 総質量は直径の2.5乗に比例 (d_cm × R_cm² のため)")
    print("3. シールド効率を上げるとシェル厚と質量が比例増加")
    print(f"4. 直径{D_km}km, 効率{R_shield}g/cm²の場合:")
    print(f"   - シェル厚: {d_cm:.4f} cm")
    print(f"   - 総質量: {M_kg:.2e} kg ({M_kg/1000/10000:.2f} 万トン)")
    print()
    print("【設計への示唆】")
    print("  - 大規模シェル（>50km）は質量が急増するため非現実的")
    print("  - シールド効率は0.1-0.3g/cm²が現実的な範囲")
    print("  - 軽量素材（カーボンナノチューブ等）の開発が鍵")
    print("=" * 50)


# ============================================================
# メイン
# ============================================================

def main():
    print("🚀 シェル厚計算システム（3D + subplot統合版）")
    print("=" * 50)
    
    # フォント設定
    print("\n[1/2] フォント設定中...")
    setup_fonts()
    
    # グラフ描画
    print("\n[2/2] 計算・グラフ描画中...")
    plot_results()
    
    print("\n✅ 全て完了！")
    print("  出力ファイル:")
    print("    - shell_analysis_3d.png (2D+3D統合)")
    print("    - shell_3d_only.png (3Dのみ)")


if __name__ == "__main__":
    main()