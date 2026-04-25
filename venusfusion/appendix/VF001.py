#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:27:43 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-001: 文字化け対策版 - 全グラフ生成システム
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
# バックエンドを明示的に指定（GUIが使えない環境でも動作）
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import warnings
import os
import sys
from datetime import datetime

warnings.filterwarnings('ignore')

# 日本語フォント設定（シンプルな方法）
def setup_japanese_font():
    """日本語フォントの設定"""
    try:
        # 日本語フォントのパス（Linux環境）
        font_candidates = [
            '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/ipa-gothic/ipag.ttf',
            '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf',
        ]
        
        font_path = None
        for candidate in font_candidates:
            if os.path.exists(candidate):
                font_path = candidate
                break
        
        if font_path:
            # フォントを追加
            import matplotlib.font_manager as fm
            fm.fontManager.addfont(font_path)
            font_name = fm.FontProperties(fname=font_path).get_name()
            matplotlib.rcParams['font.family'] = font_name
            print(f"✅ 日本語フォントを使用: {font_name}")
            return True
        else:
            # フォントが見つからない場合は英語フォントを使用
            matplotlib.rcParams['font.family'] = 'DejaVu Sans'
            print("⚠ 日本語フォントが見つかりません。英語フォントを使用します。")
            return False
    except Exception as e:
        print(f"⚠ フォント設定エラー: {e}")
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False

# フォント設定を実行
use_japanese = setup_japanese_font()
matplotlib.rcParams['axes.unicode_minus'] = False

class VF001CompleteVisualizer:
    """VF-001の全グラフを生成するクラス"""
    
    def __init__(self):
        # 物理パラメータ
        self.params = {
            'v0': 0.99,           # 初期風速
            'k': 0.01,            # 制動定数
            'n_max': 865,         # 最大拠点数
            't_span': (0, 300),   # 時間範囲
            'growth_rate': 0.05,  # 成長率
            'inflection': 150,    # 変曲点
        }
        
        # グラフの保存ディレクトリ
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir = f"VF001_plots_{timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # シミュレーションデータ
        self.simulation_data = {}
        
    def trapz_custom(self, y, x=None, dx=1.0):
        """カスタム台形積分関数（np.trapzの代替）"""
        if x is None:
            return np.sum((y[1:] + y[:-1]) / 2.0) * dx
        else:
            return np.sum((y[1:] + y[:-1]) / 2.0 * (x[1:] - x[:-1]))
    
    def logistic_growth(self, t):
        """ロジスティック成長モデル"""
        L = self.params['n_max']
        k = self.params['growth_rate']
        t0 = self.params['inflection']
        return 1 + (L - 1) / (1 + np.exp(-k * (t - t0)))
    
    def sr_decay_ode(self, t, v):
        """SR減衰の微分方程式"""
        n = self.logistic_growth(t)
        return -self.params['k'] * n * v
    
    def run_simulation(self):
        """シミュレーション実行"""
        print("🔬 シミュレーション実行中...")
        
        # 時間配列（密出力用）
        t_eval = np.linspace(*self.params['t_span'], 1000)
        
        # ODEソルバー
        sol = solve_ivp(
            self.sr_decay_ode,
            self.params['t_span'],
            [self.params['v0']],
            method='RK45',
            t_eval=t_eval,
            rtol=1e-8,
            atol=1e-10
        )
        
        t = sol.t
        v = sol.y[0]
        n = self.logistic_growth(t)
        
        # 閾値到達時間を計算
        thresholds = {}
        for thresh in [0.8, 0.5, 0.3, 0.1]:
            idx = np.where(v <= thresh)[0]
            if len(idx) > 0:
                thresholds[thresh] = t[idx[0]]
        
        self.simulation_data = {
            'time': t,
            'speed': v,
            'bases': n,
            'thresholds': thresholds
        }
        
        print(f"✅ シミュレーション完了: {len(t)}データ点")
        return self.simulation_data
    
    # ==================== グラフ1: メイン比較グラフ ====================
    def plot_main_comparison(self):
        """メイン比較グラフ（2x2サブプロット）"""
        fig = plt.figure(figsize=(16, 12))
        
        t = self.simulation_data['time']
        v = self.simulation_data['speed']
        n = self.simulation_data['bases']
        
        # 1. 風速減衰
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(t, v, 'b-', linewidth=3, label='SR Wind Speed', alpha=0.8)
        
        # 閾値線と到達時間
        for thresh in [0.8, 0.5, 0.3, 0.1]:
            if thresh in self.simulation_data['thresholds']:
                t_reach = self.simulation_data['thresholds'][thresh]
                ax1.axhline(y=thresh, color='gray', linestyle='--', alpha=0.5)
                ax1.axvline(x=t_reach, color='gray', linestyle=':', alpha=0.5)
                ax1.plot(t_reach, thresh, 'ro', markersize=10, 
                        markeredgecolor='black', linewidth=2)
                ax1.annotate(f'{t_reach:.1f} years', 
                           xy=(t_reach, thresh),
                           xytext=(10, 10 if thresh>0.5 else -20),
                           textcoords='offset points',
                           arrowprops=dict(arrowstyle='->', color='red'))
        
        ax1.set_xlabel('Time (years)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('SR Wind Speed', fontsize=12, fontweight='bold')
        ax1.set_title('SR Wind Speed Decay', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper right')
        
        # 2. 拠点数成長
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(t, n, 'g-', linewidth=3, alpha=0.8)
        
        ax2.set_xlabel('Time (years)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Base Stations', fontsize=12, fontweight='bold', color='green')
        ax2.set_title('Base Station Growth', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. 相平面図
        ax3 = plt.subplot(2, 2, 3)
        scatter = ax3.scatter(n, v, c=t, cmap='viridis', s=30, alpha=0.7,
                             edgecolors='black', linewidth=0.5)
        
        ax3.plot(n, v, 'white', linewidth=1, alpha=0.5)
        
        ax3.set_xlabel('Base Stations', fontsize=12, fontweight='bold')
        ax3.set_ylabel('SR Wind Speed', fontsize=12, fontweight='bold')
        ax3.set_title('Phase Plane: Speed vs Stations', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax3, label='Time (years)')
        ax3.grid(True, alpha=0.3)
        
        # 4. 対数プロット
        ax4 = plt.subplot(2, 2, 4)
        ax4.semilogy(t, v, 'b-', linewidth=3, alpha=0.8)
        
        ax4.set_xlabel('Time (years)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('SR Wind Speed (log scale)', fontsize=12, fontweight='bold')
        ax4.set_title('Logarithmic Plot', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, which='both')
        
        plt.suptitle('VF-001: SR Decay Simulation - Main Comparison', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        filename = f"{self.output_dir}/01_main_comparison.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 1 saved: {filename}")
    
    # ==================== グラフ2: 感度分析グラフ ====================
    def plot_sensitivity_analysis(self):
        """感度分析グラフ（4つのパラメータ）"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        t = self.simulation_data['time']
        
        # 1. 制動定数kの影響
        k_values = [0.005, 0.01, 0.02, 0.05]
        colors = plt.cm.plasma(np.linspace(0, 1, len(k_values)))
        
        for k_val, color in zip(k_values, colors):
            v_vals = self.params['v0'] * np.exp(-k_val * 
                                               np.cumsum(self.simulation_data['bases']) * 
                                               (t[1]-t[0]))
            axes[0, 0].plot(t, v_vals, color=color, linewidth=2.5,
                           label=f'k={k_val}', alpha=0.8)
        
        axes[0, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('SR Wind Speed', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Effect of Braking Constant k', fontsize=13, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 成長モデルの比較
        growth_models = {
            'Linear': lambda t: 1 + (self.params['n_max'] - 1) * (t / 300),
            'Exponential': lambda t: 1 + (self.params['n_max'] - 1) * 
                    (1 - np.exp(-0.03 * t)),
            'Logistic': self.logistic_growth,
        }
        
        colors = plt.cm.Set2(np.linspace(0, 1, len(growth_models)))
        for (name, model_func), color in zip(growth_models.items(), colors):
            n_vals = model_func(t)
            v_vals = self.params['v0'] * np.exp(-self.params['k'] * 
                                               np.cumsum(n_vals) * (t[1]-t[0]))
            axes[0, 1].plot(t, v_vals, color=color, linewidth=2.5,
                           label=name, alpha=0.8)
        
        axes[0, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('SR Wind Speed', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Growth Model Comparison', fontsize=13, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 初期風速の影響
        v0_values = [0.95, 0.99, 1.0, 1.05]
        colors = plt.cm.cool(np.linspace(0, 1, len(v0_values)))
        
        for v0_val, color in zip(v0_values, colors):
            v_vals = v0_val * np.exp(-self.params['k'] * 
                                    np.cumsum(self.simulation_data['bases']) * 
                                    (t[1]-t[0]))
            axes[1, 0].plot(t, v_vals, color=color, linewidth=2.5,
                           label=f'v0={v0_val}', alpha=0.8)
        
        axes[1, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('SR Wind Speed', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Effect of Initial Speed', fontsize=13, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 最大拠点数の影響
        n_max_values = [500, 865, 1000, 1200]
        colors = plt.cm.spring(np.linspace(0, 1, len(n_max_values)))
        
        for n_max_val, color in zip(n_max_values, colors):
            L = n_max_val
            n_vals = 1 + (L - 1) / (1 + np.exp(-self.params['growth_rate'] * 
                                              (t - self.params['inflection'])))
            v_vals = self.params['v0'] * np.exp(-self.params['k'] * 
                                               np.cumsum(n_vals) * (t[1]-t[0]))
            axes[1, 1].plot(t, v_vals, color=color, linewidth=2.5,
                           label=f'n_max={n_max_val}', alpha=0.8)
        
        axes[1, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('SR Wind Speed', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Effect of Maximum Stations', fontsize=13, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('VF-001: Parameter Sensitivity Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"{self.output_dir}/02_sensitivity_analysis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 2 saved: {filename}")
    
    # ==================== グラフ3: エネルギー解析グラフ ====================
    def plot_energy_analysis(self):
        """エネルギー解析グラフ"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        t = self.simulation_data['time']
        v = self.simulation_data['speed']
        n = self.simulation_data['bases']
        
        # 1. 運動エネルギー
        kinetic_energy = v**2
        axes[0, 0].plot(t, kinetic_energy, 'r-', linewidth=2.5)
        axes[0, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Kinetic Energy', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Kinetic Energy Decay', fontsize=13, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 散逸率
        dissipation_rate = self.params['k'] * n * v**2
        axes[0, 1].plot(t, dissipation_rate, 'orange', linewidth=2.5)
        axes[0, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Dissipation Rate', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Energy Dissipation Rate', fontsize=13, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 累積散逸エネルギー
        dt = t[1] - t[0]
        cumulative_energy = np.cumsum(dissipation_rate) * dt
        
        axes[1, 0].plot(t, cumulative_energy, 'g-', linewidth=2.5)
        axes[1, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('Cumulative Energy', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Cumulative Energy Dissipation', fontsize=13, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 散逸率と拠点数の関係
        axes[1, 1].plot(t, dissipation_rate, 'purple', linewidth=2.5, 
                       alpha=0.7, label='Dissipation Rate')
        
        n_normalized = (n - n.min()) / (n.max() - n.min())
        axes_twin = axes[1, 1].twinx()
        axes_twin.plot(t, n_normalized, 'b-', linewidth=2, 
                      alpha=0.5, label='Stations (normalized)')
        
        axes[1, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('Dissipation Rate', fontsize=11, fontweight='bold', 
                             color='purple')
        axes_twin.set_ylabel('Stations (normalized)', fontsize=11, fontweight='bold', 
                            color='blue')
        axes[1, 1].set_title('Dissipation Rate vs Stations', fontsize=13, fontweight='bold')
        
        lines1, labels1 = axes[1, 1].get_legend_handles_labels()
        lines2, labels2 = axes_twin.get_legend_handles_labels()
        axes[1, 1].legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('VF-001: Energy Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"{self.output_dir}/03_energy_analysis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 3 saved: {filename}")
    
    # ==================== グラフ4: 詳細解析グラフ ====================
    def plot_detailed_analysis(self):
        """詳細解析グラフ"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        t = self.simulation_data['time']
        v = self.simulation_data['speed']
        n = self.simulation_data['bases']
        
        # 1. 減衰率の時間変化
        dv_dt = np.gradient(v, t)
        decay_rate = -dv_dt / v
        axes[0, 0].plot(t, decay_rate, 'r-', linewidth=2.5)
        axes[0, 0].axhline(y=self.params['k'], color='gray', linestyle='--', 
                   alpha=0.5, label=f'k={self.params["k"]}')
        axes[0, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Decay Rate (1/year)', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Decay Rate Over Time', fontsize=13, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. ハーベスティングポテンシャル
        power_potential = v**3 * n
        axes[0, 1].plot(t, power_potential, 'g-', linewidth=2.5)
        axes[0, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Power Potential', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Wind Power Harvesting Potential', fontsize=13, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 閾値到達時間の比較
        thresholds = [0.8, 0.5, 0.3, 0.1]
        reach_times = []
        
        for thresh in thresholds:
            if thresh in self.simulation_data['thresholds']:
                reach_times.append(self.simulation_data['thresholds'][thresh])
            else:
                reach_times.append(self.params['t_span'][1])
        
        colors = plt.cm.RdYlBu(np.linspace(0, 1, len(thresholds)))
        bars = axes[1, 0].bar([str(t) for t in thresholds], reach_times, 
                      color=colors, alpha=0.7)
        
        for i, (bar, time_val) in enumerate(zip(bars, reach_times)):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    f'{time_val:.1f} years', ha='center', fontsize=10, fontweight='bold')
        
        axes[1, 0].set_xlabel('Threshold', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Time to Reach (years)', fontsize=12, fontweight='bold')
        axes[1, 0].set_title('Threshold Reach Times', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. 残差分析
        exp_fit = self.params['v0'] * np.exp(-self.params['k'] * np.mean(n) * t)
        residuals = v - exp_fit
        
        axes[1, 1].plot(t, residuals, 'b-', linewidth=2, alpha=0.7)
        axes[1, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        
        axes[1, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('Residual', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Residual Analysis', fontsize=13, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('VF-001: Detailed Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"{self.output_dir}/04_detailed_analysis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 4 saved: {filename}")
    
    # ==================== グラフ5: 比較対照グラフ ====================
    def plot_comparison_chart(self):
        """比較対照グラフ"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        t = self.simulation_data['time']
        v = self.simulation_data['speed']
        n = self.simulation_data['bases']
        
        # 1. 理論モデルとの比較
        axes[0, 0].plot(t, v, 'b-', linewidth=3, label='Simulation', alpha=0.8)
        
        v_theory1 = self.params['v0'] * np.exp(-self.params['k'] * 100 * t)
        axes[0, 0].plot(t, v_theory1, 'r--', linewidth=2, 
                       label='Theory (fixed stations:100)', alpha=0.6)
        
        n_linear = 1 + (self.params['n_max'] - 1) * (t / self.params['t_span'][1])
        v_theory2 = self.params['v0'] * np.exp(-self.params['k'] * 
                                              (0.5 * (self.params['n_max']-1)/300 * t**2 + t))
        axes[0, 0].plot(t, v_theory2, 'g:', linewidth=2, 
                       label='Theory (linear growth)', alpha=0.6)
        
        axes[0, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('SR Wind Speed', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Comparison with Theory', fontsize=13, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 正規化比較
        axes[0, 1].plot(t, v / v[0], 'b-', linewidth=3, 
                       label='Wind Speed (normalized)', alpha=0.8)
        axes[0, 1].plot(t, n / n[-1], 'g-', linewidth=3, 
                       label='Stations (normalized)', alpha=0.8)
        axes[0, 1].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Normalized Value', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Normalized Comparison', fontsize=13, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 微分値比較
        dv_dt = np.gradient(v, t)
        dn_dt = np.gradient(n, t)
        
        axes[1, 0].plot(t, dv_dt, 'r-', linewidth=2.5, label='dv/dt', alpha=0.8)
        axes[1, 0].set_xlabel('Time (years)', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('dv/dt', fontsize=11, fontweight='bold', color='r')
        axes[1, 0].tick_params(axis='y', labelcolor='r')
        axes[1, 0].set_title('Derivative Comparison', fontsize=13, fontweight='bold')
        
        ax_twin = axes[1, 0].twinx()
        ax_twin.plot(t, dn_dt, 'b-', linewidth=2.5, label='dn/dt', alpha=0.6)
        ax_twin.set_ylabel('dn/dt', fontsize=11, fontweight='bold', color='b')
        ax_twin.tick_params(axis='y', labelcolor='b')
        
        lines1, labels1 = axes[1, 0].get_legend_handles_labels()
        lines2, labels2 = ax_twin.get_legend_handles_labels()
        axes[1, 0].legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 無次元パラメータ
        tau = t / self.params['t_span'][1]
        v_dimless = v / self.params['v0']
        n_dimless = n / self.params['n_max']
        
        axes[1, 1].plot(tau, v_dimless, 'b-', linewidth=2.5, 
                       label='Wind Speed', alpha=0.8)
        axes[1, 1].plot(tau, n_dimless, 'g-', linewidth=2.5, 
                       label='Stations', alpha=0.8)
        axes[1, 1].set_xlabel('Dimensionless Time', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('Dimensionless Value', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Dimensionless Representation', fontsize=13, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('VF-001: Comparison Charts', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"{self.output_dir}/05_comparison_chart.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 5 saved: {filename}")
    
    # ==================== グラフ6: サマリーインフォグラフィック ====================
    def plot_summary_infographic(self):
        """サマリーインフォグラフィック"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        t = self.simulation_data['time']
        v = self.simulation_data['speed']
        n = self.simulation_data['bases']
        
        # 1. メインストーリー
        axes[0, 0].plot(t, v, 'b-', linewidth=3, alpha=0.9, label='SR Wind Speed')
        axes[0, 0].fill_between(t, 0, v, color='blue', alpha=0.2)
        
        # 閾値到達時間をマーク
        for thresh in [0.8, 0.5, 0.3, 0.1]:
            if thresh in self.simulation_data['thresholds']:
                t_reach = self.simulation_data['thresholds'][thresh]
                axes[0, 0].axvline(x=t_reach, color='red', linestyle='--', 
                               alpha=0.5, linewidth=1)
                axes[0, 0].text(t_reach, thresh+0.02, f'{t_reach:.0f}y', 
                           fontsize=10, ha='center', color='red')
        
        axes[0, 0].set_xlabel('Terraforming Period (years)', fontsize=12, 
                          fontweight='bold', labelpad=10)
        axes[0, 0].set_ylabel('SR Wind Speed', fontsize=12, fontweight='bold')
        axes[0, 0].set_title('Main Results', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.2)
        
        # 拠点数を追加
        ax_twin = axes[0, 0].twinx()
        ax_twin.plot(t, n, 'g-', linewidth=2, alpha=0.7, 
                         linestyle='--', label='Fusion Stations')
        ax_twin.set_ylabel('Fusion Stations', fontsize=12, 
                               fontweight='bold', color='green')
        ax_twin.tick_params(axis='y', labelcolor='green')
        
        lines1, labels1 = axes[0, 0].get_legend_handles_labels()
        lines2, labels2 = ax_twin.get_legend_handles_labels()
        axes[0, 0].legend(lines1 + lines2, labels1 + labels2, 
                      loc='upper right', fontsize=10)
        
        # 2. キーメトリクス
        axes[0, 1].axis('off')
        
        metrics_text = f"""
        Key Metrics:
        
        Wind Speed:
        - Initial: 0.99
        - Final: {v[-1]:.4f}
        - Reduction: {(v[0] - v[-1]) / v[0] * 100:.1f}%
        
        Stations:
        - Initial: 1
        - Final: {n[-1]:.0f}
        - Growth: {n[-1] / n[0]:.0f}x
        
        Thresholds:
        - 0.8: {self.simulation_data['thresholds'].get(0.8, 'N/A')} years
        - 0.5: {self.simulation_data['thresholds'].get(0.5, 'N/A')} years
        - 0.1: {self.simulation_data['thresholds'].get(0.1, 'N/A')} years
        """
        
        axes[0, 1].text(0.05, 0.95, metrics_text, fontsize=10,
                       verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='lightblue', 
                               alpha=0.3))
        
        # 3. タイムライン
        axes[1, 0].axis('off')
        
        timeline_text = f"""
        Timeline:
        
        Phase 1: Initial (0-50y)
        - Stations: 1 → 50
        - Wind speed: 0.99 → {v[np.argmin(np.abs(t-50))]:.2f}
        
        Phase 2: Growth (50-150y)
        - Stations: 50 → 450
        - Wind speed: {v[np.argmin(np.abs(t-50))]:.2f} → {v[np.argmin(np.abs(t-150))]:.2f}
        
        Phase 3: Mature (150-300y)
        - Stations: 450 → 865
        - Wind speed: {v[np.argmin(np.abs(t-150))]:.2f} → {v[-1]:.4f}
        """
        
        axes[1, 0].text(0.05, 0.95, timeline_text, fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='lightgreen', 
                                alpha=0.3))
        
        # 4. エネルギー計算
        axes[1, 1].axis('off')
        
        dissipation_rate = self.params['k'] * n * v**2
        cum_energy = self.trapz_custom(dissipation_rate, t)
        
        energy_text = f"""
        Energy Analysis:
        
        Dissipation Rate:
        - Max: {np.max(dissipation_rate):.2e}
        - Min: {np.min(dissipation_rate):.2e}
        
        Cumulative Energy:
        - Total: {cum_energy:.2e}
        
        Harvesting Potential:
        - Power ~ v³ × n
        - Max at: {t[np.argmax(v**3 * n)]:.0f} years
        """
        
        axes[1, 1].text(0.05, 0.95, energy_text, fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='lightyellow', 
                                alpha=0.3))
        
        plt.suptitle('VF-001: Venus SR Wind Decay Simulation\nSummary Infographic', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        filename = f"{self.output_dir}/06_summary_infographic.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"✅ Graph 6 saved: {filename}")
    
    # ==================== 全グラフ生成 ====================
    def generate_all_plots(self):
        """すべてのグラフを生成"""
        print("="*70)
        print("🎨 VF-001: Complete Graph Generation System")
        print("="*70)
        
        # シミュレーション実行
        self.run_simulation()
        
        # 各グラフを生成
        print("\n📊 Generating graphs...")
        self.plot_main_comparison()
        self.plot_sensitivity_analysis()
        self.plot_energy_analysis()
        self.plot_detailed_analysis()
        self.plot_comparison_chart()
        self.plot_summary_infographic()
        
        # データも保存
        self.save_data()
        
        print("\n" + "="*70)
        print("✅ All graphs generated successfully!")
        print("="*70)
        print(f"\n📁 Output directory: {self.output_dir}")
        print("\nGenerated graphs:")
        for i, name in enumerate([
            "01_main_comparison.png",
            "02_sensitivity_analysis.png", 
            "03_energy_analysis.png",
            "04_detailed_analysis.png",
            "05_comparison_chart.png",
            "06_summary_infographic.png"
        ], 1):
            print(f"  {i}. {name}")
        
        print("\n📊 Data files:")
        print("  - VF001_simulation_data.csv")
        print("  - VF001_parameters.txt")
        
        print("\n🚀 To view graphs:")
        print(f"  eog {self.output_dir}/01_main_comparison.png")
    
    def save_data(self):
        """データを保存"""
        # CSV保存
        df = pd.DataFrame({
            'time_year': self.simulation_data['time'],
            'wind_speed': self.simulation_data['speed'],
            'base_stations': self.simulation_data['bases'],
            'decay_rate': -np.gradient(self.simulation_data['speed'], 
                                      self.simulation_data['time']) / 
                          self.simulation_data['speed']
        })
        df.to_csv(f"{self.output_dir}/VF001_simulation_data.csv", index=False)
        
        # パラメータ保存
        with open(f"{self.output_dir}/VF001_parameters.txt", 'w') as f:
            f.write("VF-001 Simulation Parameters\n")
            f.write("="*50 + "\n")
            for key, value in self.params.items():
                f.write(f"{key:20}: {value}\n")
            f.write("\nThreshold Reach Times:\n")
            for thresh, time_val in self.simulation_data['thresholds'].items():
                f.write(f"  Wind Speed {thresh}: {time_val:.1f} years\n")
        
        print("✅ Data saved to CSV and text files")

# ==================== 実行 ====================

if __name__ == "__main__":
    print("Starting VF-001 simulation...")
    visualizer = VF001CompleteVisualizer()
    visualizer.generate_all_plots()
