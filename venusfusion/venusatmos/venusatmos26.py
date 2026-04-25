#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 13:54:46 2026

@author: iwamura
"""

# shuttle26_reboot.py
import numpy as np
import matplotlib.pyplot as plt
import target_expr
import importlib

def run_tesla_coupling():
    importlib.reload(target_expr)

    # パラメータ設定 (設定資料に基づき修正)
    P_SURF = 1.0e12     # 地表炉出力 1TW
    Q_VALUE = 2000.0    # 送電Q値（超伝導コイル想定）
    K0 = 15.0           # 結合係数定数
    P_ENGINE = 5.0e8    # 往還機維持電力 500MW (#48用)

    # 高度スイープ (50kmから500km)
    altitudes = np.linspace(50, 500, 200)

    try:
        # 受電電力の計算
        p_rec = target_expr.get_tesla_power(altitudes, P_SURF, Q_VALUE, K0)
        # 輸出に回せる余剰電力
        p_surplus = target_expr.get_export_surplus(altitudes, P_SURF, Q_VALUE, K0, P_ENGINE)

        # 採算ラインの計算 (ハイドライド固定効率)
        # 14日間でどれだけのエネルギーを物質としてパッキングできるか
        total_export_joule = p_surplus * (14 * 24 * 3600)
        hydride_mass_tons = total_export_joule / (1.4e11) / 1000 # 単位換算

        # 可視化
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(altitudes, p_rec / 1e6, 'g-', label='Total Received Power (MW)')
        ax1.axhline(P_ENGINE/1e6, color='r', ls='--', label='Propulsion Requirement')
        ax1.set_xlabel('Altitude (km)')
        ax1.set_ylabel('Power (MW)', color='g')

        ax2 = ax1.twinx()
        ax2.plot(altitudes, hydride_mass_tons, 'b-', label='Export Hydride (Tons)')
        ax2.set_ylabel('Exportable Mass (Tons/14days)', color='b')

        plt.title('Tesla Wireless Power Coupling (#26 & #47)')
        plt.grid(True, alpha=0.3)
        plt.show()

        # 結論
        optimal_alt = altitudes[np.argmax(p_surplus)]
        print(f"=== テスラ送電連成解析結果 ===")
        print(f"最適受電高度: {optimal_alt:.1f} km")
        print(f"最大輸出可能量: {np.max(hydride_mass_tons):.2f} トン / 14日")

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    run_tesla_coupling()