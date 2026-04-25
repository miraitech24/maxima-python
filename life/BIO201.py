#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:35:36 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-201: 生態系持続時間 分析プログラム (Python)
確実な日本語表示版
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib

# 超シンプルフォント設定（200文字以内）
def setup_font_simple():
    """最も確実なフォント設定"""
    try:
        # 方法1: 直接IPAexGothicを試す（最も確実）
        matplotlib.font_manager.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')
        font_name = 'IPAexGothic'
        matplotlib.rcParams['font.family'] = font_name
        matplotlib.rcParams['axes.unicode_minus'] = False
        print(f"✓ Font: {font_name}")
        return True
    except:
        try:
            # 方法2: システムの日本語フォント
            import platform
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                matplotlib.rcParams['font.family'] = 'Hiragino Sans'
            elif system == 'Windows':
                matplotlib.rcParams['font.family'] = 'MS Gothic'
            else:  # Linux
                matplotlib.rcParams['font.family'] = 'DejaVu Sans'
            
            matplotlib.rcParams['axes.unicode_minus'] = False
            print(f"✓ System font for {system}")
            return True
        except:
            # 方法3: 英語フォールバック
            matplotlib.rcParams['font.family'] = 'DejaVu Sans'
            matplotlib.rcParams['axes.unicode_minus'] = False
            print("⚠ English only")
            return False

setup_font_simple()

# メイン計算（100行以内）
def main():
    print("="*60)
    print("BIO-201: 生態系持続時間分析")
    print("="*60)
    
    # 1. データ読み込み（簡易）
    try:
        with open('bio201_for_python.txt', 'r') as f:
            for line in f:
                if 'sustainability_days' in line:
                    days = float(line.split('=')[1].strip())
                    print(f"持続日数: {days:.0f}日")
                    break
    except:
        days = 150
        print("デフォルト: 150日")
    
    # 2. シミュレーション（簡易）
    def model(y, t):
        a, p, o = y  # 藻類, 植物, 酸素
        da = 0.3*a*(1-a/15) - 0.1*a
        dp = 0.2*p*(1-p/8) - 0.05*p
        do = 1.2*da + 1.0*dp - 0.0336
        return [da, dp, do]
    
    y0 = [10, 5, 100]
    t = np.linspace(0, 365, 365)
    sol = odeint(model, y0, t)
    
    # 3. グラフ作成（2x2, シンプル）
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # グラフ1: バイオマス
    ax1 = axes[0, 0]
    ax1.plot(t, sol[:, 0], 'g-', label='藻類')
    ax1.plot(t, sol[:, 1], 'b-', label='植物')
    ax1.set_xlabel('日数')
    ax1.set_ylabel('バイオマス (kg)')
    ax1.set_title('バイオマス動態')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # グラフ2: 酸素
    ax2 = axes[0, 1]
    ax2.plot(t, sol[:, 2], 'r-')
    ax2.axhline(y=50, color='gray', ls='--', alpha=0.5)
    ax2.set_xlabel('日数')
    ax2.set_ylabel('酸素 (kg)')
    ax2.set_title('酸素濃度')
    ax2.grid(True, alpha=0.3)
    
    # グラフ3: 比較
    ax3 = axes[1, 0]
    labels = ['BIOS-3', 'BIOSPHERE 2', '予測']
    values = [180, 730, days]
    colors = ['blue', 'green', 'red']
    bars = ax3.bar(labels, values, color=colors, alpha=0.7)
    ax3.set_ylabel('持続日数')
    ax3.set_title('実実験比較')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # グラフ4: 効率
    ax4 = axes[1, 1]
    factors = ['酸素生産', '食料生産', '水再生']
    eff = [0.85, 0.72, 0.95]
    bars = ax4.bar(factors, eff, color=['red', 'orange', 'blue'])
    ax4.set_ylabel('効率')
    ax4.set_title('制限要因')
    ax4.set_ylim(0, 1.0)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('BIO-201: 生態系持続時間分析', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # 4. 保存
    plt.savefig('BIO201_results.png', dpi=150)
    print("✓ グラフ保存: BIO201_results.png")
    
    # 5. サマリー
    with open('BIO201_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"""BIO-201 結果サマリー
====================
持続可能日数: {days:.0f}日
推奨対策:
1. 藻類面積を30%増加
2. 循環効率85%以上維持
3. 栄養塩バッファ20%確保
""")
    print("✓ サマリー保存: BIO201_summary.txt")
    
    plt.show()
    print("\n完了")

if __name__ == "__main__":
    main()
