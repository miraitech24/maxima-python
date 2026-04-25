#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:06:56 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-005: Venus Fusion 連成システム解析 (文字化け修正版)
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# ==============================================================
# 1. フォント設定（文字化け防止）
# ==============================================================

def setup_japanese_font():
    """日本語フォントの設定"""
    # 使用可能な日本語フォントを探す
    font_candidates = []
    
    # Linux用フォントパス
    if sys.platform.startswith('linux'):
        font_candidates = [
            '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
            '/usr/share/fonts/truetype/takao-mincho/TakaoMincho.ttf',
            '/usr/share/fonts/truetype/ipa-gothic/ipag.ttf',
            '/usr/share/fonts/truetype/ipa-mincho/ipam.ttf',
            '/usr/share/fonts/truetype/ipaex-gothic/ipaexg.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-JP-Regular.otf',
        ]
    # macOS用フォントパス
    elif sys.platform == 'darwin':
        font_candidates = [
            '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
            '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
            '/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/PingFang.ttc',
        ]
    # Windows用フォントパス
    elif sys.platform == 'win32':
        font_candidates = [
            'C:\\Windows\\Fonts\\msgothic.ttc',
            'C:\\Windows\\Fonts\\meiryo.ttc',
            'C:\\Windows\\Fonts\\meiryob.ttc',
            'C:\\Windows\\Fonts\\yugothic.ttf',
            'C:\\Windows\\Fonts\\yumin.ttf',
        ]
    
    # 環境変数からフォントディレクトリを追加
    home_dir = os.path.expanduser('~')
    common_fonts = [
        os.path.join(home_dir, '.fonts', 'ipaexg.ttf'),
        os.path.join(home_dir, '.fonts', 'ipag.ttf'),
        os.path.join(home_dir, '.local', 'share', 'fonts', 'ipaexg.ttf'),
    ]
    font_candidates.extend(common_fonts)
    
    # フォントを検索
    available_font = None
    for font_path in font_candidates:
        if os.path.exists(font_path):
            available_font = font_path
            break
    
    # フォントを設定
    if available_font:
        try:
            matplotlib.font_manager.fontManager.addfont(available_font)
            font_name = matplotlib.font_manager.FontProperties(fname=available_font).get_name()
            matplotlib.rcParams['font.family'] = font_name
            matplotlib.rcParams['font.sans-serif'] = [font_name]
            print(f"✅ 日本語フォントを設定しました: {font_name}")
            return True
        except Exception as e:
            print(f"⚠️  フォント設定エラー: {e}")
            return False
    else:
        # デフォルトの英字フォントを使用
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
        print("⚠️  日本語フォントが見つかりません。英字フォントを使用します。")
        return False

# フォント設定を実行
print("=" * 60)
print("VF-005: Venus Fusion 連成システム解析")
print("=" * 60)
print("\nフォント設定中...")
font_set = setup_japanese_font()

# その他のmatplotlib設定
matplotlib.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け防止
matplotlib.rcParams['figure.dpi'] = 100
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['figure.autolayout'] = True

# ==============================================================
# 2. システムパラメータと方程式
# ==============================================================

class VF005_System:
    """VF-005 連成システム"""
    
    def __init__(self):
        # パラメータ設定
        self.C_vf = 0.45      # 金星大気体積濃度係数
        self.K_sr = 0.38      # SR風速減衰係数
        self.gamma_ve = 0.15  # 火山活動エネルギー係数
        self.epsilon_f = 0.08 # 温室効果フィードバック係数
        
        # 時定数
        self.tau_s = 50.0     # 表面温度時定数 (年)
        self.tau_a = 10.0     # 大気温度時定数 (年)
        
        # 物理定数
        self.sigma = 5.67e-8  # シュテファン・ボルツマン定数
        
        # 初期条件
        self.T_s0 = 737.0     # 初期表面温度 (K)
        self.T_a0 = 240.0     # 初期大気温度 (K)
        self.E_v0 = 1.0e10    # 初期火山活動エネルギー (J)
        self.S0 = 0.8         # 初期SR風速係数
        
        # シミュレーション設定
        self.t_end = 200.0    # 終了時間 (年)
        self.dt = 0.1         # 時間ステップ (年) - 精度向上のため小さく
        
        # 計算用配列
        self.t = None
        self.T_s = None
        self.T_a = None
        self.E_v = None
        self.S = None
    
    def equations(self, T_s, T_a, E_v, S):
        """微分方程式の定義"""
        # 表面温度方程式
        dT_s_dt = (1/self.tau_s) * (self.C_vf * T_a**4 - self.sigma * T_s**4 + self.gamma_ve * E_v)
        
        # 大気温度方程式
        dT_a_dt = (1/self.tau_a) * (self.epsilon_f * T_s - self.K_sr * S * T_a - (1 - self.C_vf) * T_a)
        
        # 火山活動方程式
        dE_v_dt = -0.01 * E_v + 0.001 * T_s**2
        
        # SR風速方程式
        dS_dt = -self.K_sr * S + 0.05 * (1 - S) * T_a / 300
        
        return dT_s_dt, dT_a_dt, dE_v_dt, dS_dt
    
    def solve_euler(self):
        """オイラー法による数値解法"""
        print("\n1. 数値解法（オイラー法）実行中...")
        
        n_steps = int(self.t_end / self.dt)
        
        # 配列の初期化
        self.t = np.zeros(n_steps + 1)
        self.T_s = np.zeros(n_steps + 1)
        self.T_a = np.zeros(n_steps + 1)
        self.E_v = np.zeros(n_steps + 1)
        self.S = np.zeros(n_steps + 1)
        
        # 初期値設定
        self.t[0] = 0.0
        self.T_s[0] = self.T_s0
        self.T_a[0] = self.T_a0
        self.E_v[0] = self.E_v0
        self.S[0] = self.S0
        
        # オイラー法による数値積分
        for i in range(n_steps):
            # 微分方程式の計算
            dT_s, dT_a, dE_v, dS = self.equations(
                self.T_s[i], self.T_a[i], self.E_v[i], self.S[i]
            )
            
            # 次のステップの計算
            self.t[i+1] = self.t[i] + self.dt
            self.T_s[i+1] = self.T_s[i] + dT_s * self.dt
            self.T_a[i+1] = self.T_a[i] + dT_a * self.dt
            self.E_v[i+1] = self.E_v[i] + dE_v * self.dt
            self.S[i+1] = self.S[i] + dS * self.dt
            
            # 進行状況表示
            if i % 200 == 0:
                percent = (i / n_steps) * 100
                print(f"  進行状況: {percent:.1f}%")
        
        print("   計算完了!")
        return self.t, self.T_s, self.T_a, self.E_v, self.S

# ==============================================================
# 3. 可視化関数（文字化け修正版）
# ==============================================================

class VF005_Visualizer:
    """可視化クラス（文字化け防止）"""
    
    @staticmethod
    def create_figure(title, xlabel, ylabel, figsize=(10, 6)):
        """グラフの基本設定を作成"""
        fig, ax = plt.subplots(figsize=figsize)
        
        if font_set:
            ax.set_title(title, fontsize=14)
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel(ylabel, fontsize=12)
        else:
            # 英字フォント用のタイトル
            eng_titles = {
                "VF-005: 温度進化解析": "VF-005: Temperature Evolution",
                "時間 (年)": "Time (years)",
                "温度 (K)": "Temperature (K)",
                "表面温度 T_s": "Surface Temperature T_s",
                "大気温度 T_a": "Atmospheric Temperature T_a",
                "VF-005: 火山活動エネルギー": "VF-005: Volcanic Activity Energy",
                "火山活動エネルギー E_v (J)": "Volcanic Activity Energy E_v (J)",
                "VF-005: SR風速係数": "VF-005: SR Wind Speed Coefficient",
                "SR風速係数 S": "SR Wind Speed Coefficient S",
                "VF-005: 位相平面解析": "VF-005: Phase Plane Analysis",
                "表面温度 T_s (K)": "Surface Temperature T_s (K)",
                "大気温度 T_a (K)": "Atmospheric Temperature T_a (K)",
            }
            
            eng_title = eng_titles.get(title, title)
            eng_xlabel = eng_titles.get(xlabel, xlabel)
            eng_ylabel = eng_titles.get(ylabel, ylabel)
            
            ax.set_title(eng_title, fontsize=14)
            ax.set_xlabel(eng_xlabel, fontsize=12)
            ax.set_ylabel(eng_ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3)
        return fig, ax
    
    @staticmethod
    def plot_temperature_evolution(t, T_s, T_a, save_path='VF005_temperature.png'):
        """温度進化のプロット"""
        print("\n2. 温度進化グラフ生成中...")
        
        fig, ax = VF005_Visualizer.create_figure(
            "VF-005: 温度進化解析",
            "時間 (年)",
            "温度 (K)",
            figsize=(12, 8)
        )
        
        # 表面温度
        ax.plot(t, T_s, 'r-', linewidth=2, 
                label='表面温度 T_s' if font_set else 'Surface Temperature T_s')
        
        # 大気温度
        ax.plot(t, T_a, 'b-', linewidth=2, 
                label='大気温度 T_a' if font_set else 'Atmospheric Temperature T_a')
        
        # 凡例
        ax.legend(fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   保存: {save_path}")
    
    @staticmethod
    def plot_energy_evolution(t, E_v, save_path='VF005_energy.png'):
        """エネルギー進化のプロット"""
        print("\n3. エネルギー進化グラフ生成中...")
        
        fig, ax = VF005_Visualizer.create_figure(
            "VF-005: 火山活動エネルギー",
            "時間 (年)",
            "火山活動エネルギー E_v (J)",
            figsize=(12, 8)
        )
        
        # 対数スケールでプロット
        ax.semilogy(t, E_v, 'g-', linewidth=2)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   保存: {save_path}")
    
    @staticmethod
    def plot_wind_evolution(t, S, save_path='VF005_wind.png'):
        """風速係数進化のプロット"""
        print("\n4. 風速係数グラフ生成中...")
        
        fig, ax = VF005_Visualizer.create_figure(
            "VF-005: SR風速係数",
            "時間 (年)",
            "SR風速係数 S",
            figsize=(12, 8)
        )
        
        ax.plot(t, S, 'm-', linewidth=2)
        ax.set_ylim([0, 1.1])  # 風速係数の範囲を設定
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   保存: {save_path}")
    
    @staticmethod
    def plot_phase_plane(T_s, T_a, save_path='VF005_phase.png'):
        """位相平面のプロット"""
        print("\n5. 位相平面グラフ生成中...")
        
        fig, ax = VF005_Visualizer.create_figure(
            "VF-005: 位相平面解析",
            "表面温度 T_s (K)",
            "大気温度 T_a (K)",
            figsize=(12, 8)
        )
        
        # 位相平面
        ax.plot(T_s, T_a, 'purple', linewidth=2)
        
        # 初期値と最終値をマーク
        ax.plot(T_s[0], T_a[0], 'ro', markersize=10, 
                label='初期値' if font_set else 'Initial')
        ax.plot(T_s[-1], T_a[-1], 'bo', markersize=10, 
                label='最終値' if font_set else 'Final')
        
        ax.legend(fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   保存: {save_path}")
    
    @staticmethod
    def plot_comprehensive(t, T_s, T_a, E_v, S, save_path='VF005_comprehensive.png'):
        """総合プロット（4サブプロット）"""
        print("\n6. 総合グラフ生成中...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 左上: 温度進化
        ax1 = axes[0, 0]
        ax1.plot(t, T_s, 'r-', linewidth=2, label='T_s')
        ax1.plot(t, T_a, 'b-', linewidth=2, label='T_a')
        if font_set:
            ax1.set_title('温度進化')
            ax1.set_xlabel('時間 (年)')
            ax1.set_ylabel('温度 (K)')
        else:
            ax1.set_title('Temperature Evolution')
            ax1.set_xlabel('Time (years)')
            ax1.set_ylabel('Temperature (K)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 右上: エネルギー進化
        ax2 = axes[0, 1]
        ax2.semilogy(t, E_v, 'g-', linewidth=2)
        if font_set:
            ax2.set_title('火山活動エネルギー')
            ax2.set_xlabel('時間 (年)')
            ax2.set_ylabel('エネルギー E_v (J)')
        else:
            ax2.set_title('Volcanic Activity Energy')
            ax2.set_xlabel('Time (years)')
            ax2.set_ylabel('Energy E_v (J)')
        ax2.grid(True, alpha=0.3)
        
        # 左下: 風速係数
        ax3 = axes[1, 0]
        ax3.plot(t, S, 'm-', linewidth=2)
        ax3.set_ylim([0, 1.1])
        if font_set:
            ax3.set_title('SR風速係数')
            ax3.set_xlabel('時間 (年)')
            ax3.set_ylabel('風速係数 S')
        else:
            ax3.set_title('SR Wind Speed Coefficient')
            ax3.set_xlabel('Time (years)')
            ax3.set_ylabel('Wind Coefficient S')
        ax3.grid(True, alpha=0.3)
        
        # 右下: 位相平面
        ax4 = axes[1, 1]
        ax4.plot(T_s, T_a, 'purple', linewidth=2)
        ax4.plot(T_s[0], T_a[0], 'ro', markersize=8, label='初期' if font_set else 'Initial')
        ax4.plot(T_s[-1], T_a[-1], 'bo', markersize=8, label='最終' if font_set else 'Final')
        if font_set:
            ax4.set_title('位相平面 (T_s vs T_a)')
            ax4.set_xlabel('表面温度 T_s (K)')
            ax4.set_ylabel('大気温度 T_a (K)')
        else:
            ax4.set_title('Phase Plane (T_s vs T_a)')
            ax4.set_xlabel('Surface Temperature T_s (K)')
            ax4.set_ylabel('Atmospheric Temperature T_a (K)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        if font_set:
            plt.suptitle('VF-005: 金星連成システム解析', fontsize=16)
        else:
            plt.suptitle('VF-005: Venus Coupled System Analysis', fontsize=16)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   保存: {save_path}")

# ==============================================================
# 4. メイン実行関数
# ==============================================================

def main():
    """メイン実行関数"""
    
    # システムの初期化と計算
    system = VF005_System()
    t, T_s, T_a, E_v, S = system.solve_euler()
    
    # 結果表示
    print("\n" + "=" * 60)
    print("解析結果:")
    print("=" * 60)
    
    print(f"初期条件:")
    print(f"  表面温度 T_s0: {system.T_s0:.1f} K")
    print(f"  大気温度 T_a0: {system.T_a0:.1f} K")
    print(f"  火山活動エネルギー E_v0: {system.E_v0:.2e} J")
    print(f"  SR風速係数 S0: {system.S0:.3f}")
    
    print(f"\n最終値 ({system.t_end}年後):")
    print(f"  表面温度 T_s: {T_s[-1]:.1f} K")
    print(f"  大気温度 T_a: {T_a[-1]:.1f} K")
    print(f"  火山活動エネルギー E_v: {E_v[-1]:.2e} J")
    print(f"  SR風速係数 S: {S[-1]:.3f}")
    
    print(f"\n変化量:")
    print(f"  ΔT_s: {T_s[-1] - system.T_s0:.1f} K")
    print(f"  ΔT_a: {T_a[-1] - system.T_a0:.1f} K")
    print(f"  ΔE_v: {E_v[-1] - system.E_v0:.2e} J")
    print(f"  ΔS: {S[-1] - system.S0:.3f}")
    
    # データをCSVに保存
    print("\n7. データ保存中...")
    df = pd.DataFrame({
        't': t,
        'T_s': T_s,
        'T_a': T_a,
        'E_v': E_v,
        'S': S
    })
    df.to_csv('VF005_results.csv', index=False)
    print(f"   保存: VF005_results.csv ({len(df)}行)")
    
    # 可視化
    visualizer = VF005_Visualizer()
    visualizer.plot_temperature_evolution(t, T_s, T_a)
    visualizer.plot_energy_evolution(t, E_v)
    visualizer.plot_wind_evolution(t, S)
    visualizer.plot_phase_plane(T_s, T_a)
    visualizer.plot_comprehensive(t, T_s, T_a, E_v, S)
    
    # 最終メッセージ
    print("\n" + "=" * 60)
    print("✅ VF-005 解析完了!")
    print("=" * 60)
    print("\n📁 生成ファイル:")
    print("  - VF005_results.csv: 数値計算結果")
    print("  - VF005_temperature.png: 温度進化グラフ")
    print("  - VF005_energy.png: エネルギー進化グラフ")
    print("  - VF005_wind.png: 風速係数グラフ")
    print("  - VF005_phase.png: 位相平面グラフ")
    print("  - VF005_comprehensive.png: 総合グラフ")

# ==============================================================
# 5. 実行部分
# ==============================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ ユーザーによって中断されました")
    except Exception as e:
        print(f"\n\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 トラブルシューティング:")
        print("1. 日本語フォントがインストールされていない場合:")
        print("   Ubuntu/Debian: sudo apt-get install fonts-ipafont fonts-ipaexfont")
        print("   Fedora/RHEL: sudo dnf install ipa-gothic-fonts ipa-ex-gothic-fonts")
        print("   macOS: デフォルトで日本語フォントがインストール済み")
        print("   Windows: デフォルトで日本語フォントがインストール済み")
        print("\n2. 英字フォントのみ使用する場合は:")
        print("   コードの setup_japanese_font() 関数をコメントアウトしてください")
