#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:04:28 2026

@author: iwamura
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-004: 連成システム数値解析・最適化 (Python版) - 文字化け修正版
Created on 2026/3/23
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import minimize, differential_evolution, basinhopping
from scipy.linalg import eig
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from dataclasses import dataclass
from typing import Tuple, List, Callable, Optional
import warnings
import json
import os
import sys

warnings.filterwarnings('ignore')

# ==============================================================
# フォント設定（文字化け防止）
# ==============================================================

def setup_fonts():
    """日本語フォントの設定"""
    # 使用可能なフォントを探す
    font_options = [
        # Linux (Ubuntu/Debian)
        '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
        '/usr/share/fonts/truetype/takao-mincho/TakaoMincho.ttf',
        '/usr/share/fonts/truetype/ipa-gothic/ipag.ttf',
        '/usr/share/fonts/truetype/ipa-mincho/ipam.ttf',
        # Linux (一般的な場所)
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        # macOS
        '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
        '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
        # Windows (WSL環境)
        '/mnt/c/Windows/Fonts/msgothic.ttc',
        '/mnt/c/Windows/Fonts/meiryo.ttc',
    ]
    
    # 日本語フォントが見つかるかチェック
    available_font = None
    for font_path in font_options:
        if os.path.exists(font_path):
            available_font = font_path
            break
    
    if available_font:
        # フォントを追加して設定
        matplotlib.font_manager.fontManager.addfont(available_font)
        font_name = matplotlib.font_manager.FontProperties(fname=available_font).get_name()
        matplotlib.rcParams['font.family'] = font_name
        matplotlib.rcParams['font.sans-serif'] = [font_name]
        print(f"  フォントを設定しました: {font_name}")
        return True
    else:
        # 日本語フォントが見つからない場合は英字フォントを設定
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
        print("  日本語フォントが見つかりません。英字フォントを使用します。")
        return False

# フォント設定を実行
print("フォント設定中...")
font_set = setup_fonts()

# その他のmatplotlib設定
matplotlib.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け防止
matplotlib.rcParams['figure.dpi'] = 100
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['figure.autolayout'] = True

# ============================================================================
# 1. システム定義クラス
# ============================================================================

@dataclass
class CoupledSystem:
    """連成システム定義クラス"""
    alpha: float = 0.05    # 成長率係数
    beta: float = 0.02     # 減衰率係数
    gamma: float = 0.01    # 結合係数
    delta: float = 0.03    # 外部擾乱係数
    A0: float = 100.0      # 初期値 A
    B0: float = 50.0       # 初期値 B
    t_end: float = 200.0   # 終了時間
    
    def __post_init__(self):
        """パラメータ検証"""
        assert self.alpha >= 0, "alpha must be non-negative"
        assert self.beta >= 0, "beta must be non-negative"
        assert self.gamma >= 0, "gamma must be non-negative"
        assert self.delta >= 0, "delta must be non-negative"
        assert self.t_end > 0, "t_end must be positive"
    
    def equations(self, t: float, y: np.ndarray) -> np.ndarray:
        """連成微分方程式の定義"""
        A, B = y
        dA_dt = self.alpha * A - self.gamma * B
        dB_dt = self.beta * B + self.gamma * A - self.delta * B
        return np.array([dA_dt, dB_dt])
    
    def jacobian(self, y: np.ndarray) -> np.ndarray:
        """ヤコビアン行列"""
        A, B = y
        J = np.array([
            [self.alpha, -self.gamma],
            [self.gamma, self.beta - self.delta]
        ])
        return J

# ============================================================================
# 2. 数値計算クラス
# ============================================================================

class NumericalSolver:
    """数値解法クラス"""
    
    def __init__(self, system: CoupledSystem):
        self.system = system
    
    def solve_rk45(self, t_eval: np.ndarray = None) -> dict:
        """RK45法による数値解法"""
        if t_eval is None:
            t_eval = np.linspace(0, self.system.t_end, 1000)
        
        sol = solve_ivp(
            fun=self.system.equations,
            t_span=(0, self.system.t_end),
            y0=[self.system.A0, self.system.B0],
            method='RK45',
            t_eval=t_eval,
            rtol=1e-8,
            atol=1e-10,
            jac=self.system.jacobian
        )
        
        return {
            't': sol.t,
            'A': sol.y[0],
            'B': sol.y[1],
            'success': sol.success,
            'message': sol.message,
            'nfe': sol.nfev
        }

# ============================================================================
# 3. 最適化クラス（簡略版）
# ============================================================================

class SystemOptimizer:
    """システム最適化クラス"""
    
    def __init__(self, system: CoupledSystem):
        self.system = system
        self.solver = NumericalSolver(system)
    
    def sensitivity_analysis(self, 
                            param_name: str, 
                            range_values: np.ndarray) -> pd.DataFrame:
        """感度解析"""
        results = []
        
        for value in range_values:
            # パラメータ変更
            params = {
                'alpha': self.system.alpha,
                'beta': self.system.beta,
                'gamma': self.system.gamma,
                'delta': self.system.delta
            }
            params[param_name] = value
            
            temp_system = CoupledSystem(**params)
            solver = NumericalSolver(temp_system)
            result = solver.solve_rk45()
            
            # 各種指標を計算 - trapzの代わりに数値積分を行う
            A_final = result['A'][-1]
            B_final = result['B'][-1]
            A_max = np.max(result['A'])
            B_max = np.max(result['B'])
            
            # 台形則による数値積分（trapzと同じ計算）
            t = result['t']
            A = result['A']
            B = result['B']
            
            # 手動で台形則積分を計算
            def manual_trapz(y, x):
                s = 0
                for i in range(len(x)-1):
                    s += (y[i] + y[i+1]) * (x[i+1] - x[i]) / 2
                return s
            
            A_area = manual_trapz(A, t)
            B_area = manual_trapz(B, t)
            
            results.append({
                param_name: value,
                'A_final': A_final,
                'B_final': B_final,
                'A_max': A_max,
                'B_max': B_max,
                'A_area': A_area,
                'B_area': B_area
            })
        
        return pd.DataFrame(results)

# ============================================================================
# 4. 可視化クラス（文字化け修正版）
# ============================================================================

class Visualizer:
    """結果可視化クラス"""
    
    @staticmethod
    def plot_timeseries(t: np.ndarray, A: np.ndarray, B: np.ndarray, 
                       title: str = "VF-004: 連成システム時間発展",
                       save_path: str = "VF004_timeseries.png") -> None:
        """時系列プロット"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # メイン時系列
        axes[0, 0].plot(t, A, 'b-', linewidth=2, label='System A')
        axes[0, 0].plot(t, B, 'r-', linewidth=2, label='System B')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('State Variable')
        axes[0, 0].set_title('Time Series Evolution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 位相平面
        axes[0, 1].plot(A, B, 'g-', linewidth=2)
        axes[0, 1].plot(A[0], B[0], 'ko', markersize=10, label='Initial')
        axes[0, 1].plot(A[-1], B[-1], 'ro', markersize=10, label='Final')
        axes[0, 1].set_xlabel('System A')
        axes[0, 1].set_ylabel('System B')
        axes[0, 1].set_title('Phase Plane')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 対数プロット
        axes[1, 0].semilogy(t, A, 'b-', linewidth=2, label='System A')
        axes[1, 0].semilogy(t, B, 'r-', linewidth=2, label='System B')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('State Variable (log scale)')
        axes[1, 0].set_title('Logarithmic Time Series')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 微分値
        dA_dt = np.gradient(A, t)
        dB_dt = np.gradient(B, t)
        axes[1, 1].plot(t, dA_dt, 'b--', linewidth=2, label='dA/dt')
        axes[1, 1].plot(t, dB_dt, 'r--', linewidth=2, label='dB/dt')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Rate of Change')
        axes[1, 1].set_title('Derivatives')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        if font_set:
            # 日本語フォントが設定されている場合のみ日本語タイトルを使用
            plt.suptitle('VF-004: 連成システム時間発展', fontsize=16)
        else:
            plt.suptitle('VF-004: Coupled System Time Evolution', fontsize=16)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Time series plot saved: {save_path}")
    
    @staticmethod
    def plot_sensitivity(df: pd.DataFrame, param_name: str) -> None:
        """感度解析結果のプロット"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        metrics = ['A_final', 'B_final', 'A_max', 'B_max', 'A_area', 'B_area']
        if font_set:
            titles = ['最終値 A', '最終値 B', '最大値 A', '最大値 B', '積分値 A', '積分値 B']
            xlabel = param_name
        else:
            titles = ['Final A', 'Final B', 'Max A', 'Max B', 'Integral A', 'Integral B']
            xlabel = param_name
        
        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx//3, idx%3]
            ax.plot(df[param_name], df[metric], 'o-', linewidth=2)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(metric)
            ax.set_title(f'{title} vs {param_name}')
            ax.grid(True, alpha=0.3)
        
        if font_set:
            plt.suptitle(f'感度解析: {param_name} の影響', fontsize=16)
        else:
            plt.suptitle(f'Sensitivity Analysis: Effect of {param_name}', fontsize=16)
        
        plt.tight_layout()
        save_path = f'VF004_sensitivity_{param_name}.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Sensitivity plot saved: {save_path}")

# ============================================================================
# 5. メイン実行クラス
# ============================================================================

class VF004_Analysis:
    """VF-004 メイン解析クラス"""
    
    def __init__(self):
        print("=" * 60)
        print("VF-004: 連成システム解析")
        print("=" * 60)
        
        # システム初期化
        self.system = CoupledSystem()
        self.solver = NumericalSolver(self.system)
        self.optimizer = SystemOptimizer(self.system)
        self.visualizer = Visualizer()
        
        # 解析結果格納用
        self.results = {}
    
    def run_basic_analysis(self):
        """基本解析実行"""
        
        print("\n1. 数値解法によるシミュレーション実行中...")
        
        # RK45法で計算
        self.results['rk45'] = self.solver.solve_rk45()
        
        print(f"   計算完了: {self.results['rk45']['nfe']} 回の関数評価")
        
        # 可視化
        print("\n2. 結果の可視化中...")
        self.visualizer.plot_timeseries(
            self.results['rk45']['t'],
            self.results['rk45']['A'],
            self.results['rk45']['B']
        )
        
        print("   可視化完了")
        
        # 簡単な感度解析
        print("\n3. 簡易感度解析実行中...")
        param_names = ['alpha', 'gamma']  # 主要パラメータのみ
        
        for param in param_names:
            print(f"   {param}の感度解析...")
            base_value = getattr(self.system, param)
            values = np.linspace(0.5 * base_value, 1.5 * base_value, 10)
            df_sens = self.optimizer.sensitivity_analysis(param, values)
            self.visualizer.plot_sensitivity(df_sens, param)
        
        print("   感度解析完了")
        
        # 結果の保存
        self.save_basic_results()
        
        print("\n" + "=" * 60)
        print("VF-004 基本解析完了!")
        print("=" * 60)
    
    def save_basic_results(self):
        """基本結果の保存"""
        # 数値結果をCSVに保存
        df_results = pd.DataFrame({
            't': self.results['rk45']['t'],
            'A': self.results['rk45']['A'],
            'B': self.results['rk45']['B']
        })
        df_results.to_csv('VF004_basic_results.csv', index=False)
        
        # システム情報を保存
        system_info = {
            'alpha': self.system.alpha,
            'beta': self.system.beta,
            'gamma': self.system.gamma,
            'delta': self.system.delta,
            'A0': self.system.A0,
            'B0': self.system.B0,
            't_end': self.system.t_end,
            'simulation_date': pd.Timestamp.now().isoformat()
        }
        
        with open('VF004_system_info.json', 'w') as f:
            json.dump(system_info, f, indent=2)
        
        # 簡単な統計情報も保存
        # 手動で台形則積分を計算
        def manual_trapz(y, x):
            s = 0
            for i in range(len(x)-1):
                s += (y[i] + y[i+1]) * (x[i+1] - x[i]) / 2
            return s
        
        t = self.results['rk45']['t']
        A = self.results['rk45']['A']
        B = self.results['rk45']['B']
        
        stats = {
            'A_final': float(A[-1]),
            'B_final': float(B[-1]),
            'A_max': float(np.max(A)),
            'B_max': float(np.max(B)),
            'A_area': float(manual_trapz(A, t)),
            'B_area': float(manual_trapz(B, t))
        }
        
        with open('VF004_statistics.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print("\n生成されたファイル:")
        print("  - VF004_basic_results.csv: 数値計算結果")
        print("  - VF004_system_info.json: システムパラメータ")
        print("  - VF004_statistics.json: 統計情報")
        print("  - VF004_timeseries.png: 時系列プロット")
        print("  - VF004_sensitivity_*.png: 感度解析プロット")

# ============================================================================
# 6. メイン実行ブロック
# ============================================================================

if __name__ == "__main__":
    try:
        # 基本解析のみ実行（最適化なし）
        analyzer = VF004_Analysis()
        analyzer.run_basic_analysis()
        
        # Maximaデータがあれば比較
        print("\n4. Maximaデータとの比較（オプション）")
        if os.path.exists('VF004_analytical_data.csv'):
            print("   Maxima解析データを検出しました")
            maxima_data = pd.read_csv('VF004_analytical_data.csv')
            
            # 比較プロット
            plt.figure(figsize=(10, 6))
            plt.plot(analyzer.results['rk45']['t'], analyzer.results['rk45']['A'], 
                    'b-', label='Python (A)', linewidth=2)
            plt.plot(analyzer.results['rk45']['t'], analyzer.results['rk45']['B'],
                    'r-', label='Python (B)', linewidth=2)
            
            if 'A_analytical' in maxima_data.columns and 'B_analytical' in maxima_data.columns:
                plt.plot(maxima_data['t'], maxima_data['A_analytical'], 
                        'b--', label='Maxima (A)', linewidth=2, alpha=0.7)
                plt.plot(maxima_data['t'], maxima_data['B_analytical'],
                        'r--', label='Maxima (B)', linewidth=2, alpha=0.7)
            
            plt.xlabel('Time')
            plt.ylabel('State Variable')
            if font_set:
                plt.title('Python数値解 vs Maxima解析解')
            else:
                plt.title('Python Numerical vs Maxima Analytical')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig('VF004_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("   比較プロットを保存: VF004_comparison.png")
        else:
            print("   Maxima解析データが見つかりません（スキップ）")
            
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        print("\n対処方法:")
        print("1. 必要なライブラリをインストール: pip install numpy scipy pandas matplotlib")
        print("2. numpyをアップグレード: pip install --upgrade numpy")
        print("3. 日本語フォントがインストールされていない場合は、")
        print("   以下のコマンドで日本語フォントをインストールしてください:")
        print("   Ubuntu/Debian: sudo apt-get install fonts-ipafont fonts-noto-cjk")
        print("   Fedora/RHEL: sudo dnf install ipa-gothic-fonts ipa-mincho-fonts")

