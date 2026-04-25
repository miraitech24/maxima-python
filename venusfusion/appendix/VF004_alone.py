#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:23:53 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-004: 完全統合解析スクリプト (Pythonのみ)
Maximaなしで解析解と数値解の両方を計算
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.linalg import expm
import matplotlib.pyplot as plt
from dataclasses import dataclass
import warnings
import json
import os
import sys

warnings.filterwarnings('ignore')

# フォント設定（文字化け防止）
try:
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    print("フォント設定完了: DejaVu Sans")
except:
    print("フォント設定に失敗しましたが、実行を続けます...")

print("=" * 70)
print("VF-004: 連成システム完全解析 (Python統合版)")
print("=" * 70)

# ============================================================================
# 1. システム定義
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
    
    def equations(self, t: float, y: np.ndarray) -> np.ndarray:
        """連成微分方程式の定義"""
        A, B = y
        dA_dt = self.alpha * A - self.gamma * B
        dB_dt = self.beta * B + self.gamma * A - self.delta * B
        return np.array([dA_dt, dB_dt])
    
    def get_matrix(self):
        """システム行列を返す"""
        return np.array([
            [self.alpha, -self.gamma],
            [self.gamma, self.beta - self.delta]
        ])
    
    def analytical_solution(self, t):
        """解析解を計算 (行列指数関数法)"""
        M = self.get_matrix()
        X0 = np.array([self.A0, self.B0])
        
        # 各時間での解を計算
        A_analytical = np.zeros_like(t)
        B_analytical = np.zeros_like(t)
        
        for i, ti in enumerate(t):
            X = expm(M * ti) @ X0
            A_analytical[i] = X[0]
            B_analytical[i] = X[1]
        
        return A_analytical, B_analytical

# ============================================================================
# 2. 解析実行クラス
# ============================================================================

class VF004_Complete_Analysis:
    """完全解析クラス"""
    
    def __init__(self):
        self.system = CoupledSystem()
        self.results = {}
        
    def run_analytical(self):
        """解析解の計算"""
        print("\n1. 解析解を計算中...")
        
        # 時間配列
        t_analytical = np.linspace(0, self.system.t_end, 201)
        
        # 解析解を計算
        A_analytical, B_analytical = self.system.analytical_solution(t_analytical)
        
        # 結果を保存
        self.results['analytical'] = {
            't': t_analytical,
            'A': A_analytical,
            'B': B_analytical
        }
        
        # CSVに保存
        df_analytical = pd.DataFrame({
            't': t_analytical,
            'A_analytical': A_analytical,
            'B_analytical': B_analytical
        })
        df_analytical.to_csv('VF004_analytical_data.csv', index=False)
        
        print(f"   解析解計算完了: {len(t_analytical)} 点")
        print(f"   最終値 A: {A_analytical[-1]:.4f}")
        print(f"   最終値 B: {B_analytical[-1]:.4f}")
        
        return df_analytical
    
    def run_numerical(self):
        """数値解の計算"""
        print("\n2. 数値解を計算中...")
        
        # 時間配列
        t_numerical = np.linspace(0, self.system.t_end, 1000)
        
        # 数値解を計算 (RK45法)
        sol = solve_ivp(
            fun=self.system.equations,
            t_span=(0, self.system.t_end),
            y0=[self.system.A0, self.system.B0],
            method='RK45',
            t_eval=t_numerical,
            rtol=1e-8,
            atol=1e-10
        )
        
        # 結果を保存
        self.results['numerical'] = {
            't': sol.t,
            'A': sol.y[0],
            'B': sol.y[1],
            'nfe': sol.nfev
        }
        
        # CSVに保存
        df_numerical = pd.DataFrame({
            't': sol.t,
            'A_numerical': sol.y[0],
            'B_numerical': sol.y[1]
        })
        df_numerical.to_csv('VF004_numerical_data.csv', index=False)
        
        print(f"   数値解計算完了: {sol.nfev} 回の関数評価")
        print(f"   最終値 A: {sol.y[0][-1]:.4f}")
        print(f"   最終値 B: {sol.y[1][-1]:.4f}")
        
        return df_numerical
    
    def compare_solutions(self):
        """解析解と数値解の比較"""
        print("\n3. 解析解と数値解を比較中...")
        
        try:
            # データ読み込み
            df_analytical = pd.read_csv('VF004_analytical_data.csv')
            df_numerical = pd.read_csv('VF004_numerical_data.csv')
            
            # 共通の時間軸で補間
            from scipy import interpolate
            
            t_min = max(df_analytical['t'].min(), df_numerical['t'].min())
            t_max = min(df_analytical['t'].max(), df_numerical['t'].max())
            t_common = np.linspace(t_min, t_max, 500)
            
            # 補間関数を作成
            f_A_analytical = interpolate.interp1d(df_analytical['t'], df_analytical['A_analytical'])
            f_B_analytical = interpolate.interp1d(df_analytical['t'], df_analytical['B_analytical'])
            f_A_numerical = interpolate.interp1d(df_numerical['t'], df_numerical['A_numerical'])
            f_B_numerical = interpolate.interp1d(df_numerical['t'], df_numerical['B_numerical'])
            
            # 補間値を計算
            A_analytical_interp = f_A_analytical(t_common)
            B_analytical_interp = f_B_analytical(t_common)
            A_numerical_interp = f_A_numerical(t_common)
            B_numerical_interp = f_B_numerical(t_common)
            
            # 誤差計算
            error_A = np.abs(A_analytical_interp - A_numerical_interp)
            error_B = np.abs(B_analytical_interp - B_numerical_interp)
            
            # 統合結果を保存
            df_integrated = pd.DataFrame({
                't': t_common,
                'A_analytical': A_analytical_interp,
                'B_analytical': B_analytical_interp,
                'A_numerical': A_numerical_interp,
                'B_numerical': B_numerical_interp,
                'error_A': error_A,
                'error_B': error_B
            })
            df_integrated.to_csv('VF004_integrated_results.csv', index=False)
            
            # 統計情報
            stats = {
                'mean_error_A': float(error_A.mean()),
                'mean_error_B': float(error_B.mean()),
                'max_error_A': float(error_A.max()),
                'max_error_B': float(error_B.max()),
                'correlation_A': float(np.corrcoef(A_analytical_interp, A_numerical_interp)[0, 1]),
                'correlation_B': float(np.corrcoef(B_analytical_interp, B_numerical_interp)[0, 1])
            }
            
            with open('VF004_comparison_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            
            print("   比較結果:")
            print(f"   平均誤差 A: {stats['mean_error_A']:.2e}")
            print(f"   平均誤差 B: {stats['mean_error_B']:.2e}")
            print(f"   最大誤差 A: {stats['max_error_A']:.2e}")
            print(f"   最大誤差 B: {stats['max_error_B']:.2e}")
            print(f"   相関係数 A: {stats['correlation_A']:.6f}")
            print(f"   相関係数 B: {stats['correlation_B']:.6f}")
            
            return df_integrated, stats
            
        except Exception as e:
            print(f"   比較中にエラー: {e}")
            return None, None
    
    def plot_results(self):
        """結果の可視化"""
        print("\n4. 結果を可視化中...")
        
        try:
            # データ読み込み
            df_analytical = pd.read_csv('VF004_analytical_data.csv')
            df_numerical = pd.read_csv('VF004_numerical_data.csv')
            
            # 1. 比較プロット
            fig1, axes1 = plt.subplots(2, 2, figsize=(14, 10))
            
            # システムAの比較
            axes1[0, 0].plot(df_analytical['t'], df_analytical['A_analytical'], 
                            'b-', label='Analytical A', linewidth=2)
            axes1[0, 0].plot(df_numerical['t'], df_numerical['A_numerical'], 
                            'r--', label='Numerical A', linewidth=2, alpha=0.7)
            axes1[0, 0].set_xlabel('Time')
            axes1[0, 0].set_ylabel('System A')
            axes1[0, 0].set_title('System A: Analytical vs Numerical')
            axes1[0, 0].legend()
            axes1[0, 0].grid(True, alpha=0.3)
            
            # システムBの比較
            axes1[0, 1].plot(df_analytical['t'], df_analytical['B_analytical'], 
                            'b-', label='Analytical B', linewidth=2)
            axes1[0, 1].plot(df_numerical['t'], df_numerical['B_numerical'], 
                            'r--', label='Numerical B', linewidth=2, alpha=0.7)
            axes1[0, 1].set_xlabel('Time')
            axes1[0, 1].set_ylabel('System B')
            axes1[0, 1].set_title('System B: Analytical vs Numerical')
            axes1[0, 1].legend()
            axes1[0, 1].grid(True, alpha=0.3)
            
            # 位相平面比較
            axes1[1, 0].plot(df_analytical['A_analytical'], df_analytical['B_analytical'],
                            'b-', label='Analytical', linewidth=2)
            axes1[1, 0].plot(df_numerical['A_numerical'], df_numerical['B_numerical'],
                            'r--', label='Numerical', linewidth=2, alpha=0.7)
            axes1[1, 0].set_xlabel('System A')
            axes1[1, 0].set_ylabel('System B')
            axes1[1, 0].set_title('Phase Plane Comparison')
            axes1[1, 0].legend()
            axes1[1, 0].grid(True, alpha=0.3)
            
            # 誤差プロット
            if os.path.exists('VF004_integrated_results.csv'):
                df_integrated = pd.read_csv('VF004_integrated_results.csv')
                axes1[1, 1].semilogy(df_integrated['t'], df_integrated['error_A'], 
                                    'b-', label='Error A', linewidth=2)
                axes1[1, 1].semilogy(df_integrated['t'], df_integrated['error_B'], 
                                    'r-', label='Error B', linewidth=2)
                axes1[1, 1].set_xlabel('Time')
                axes1[1, 1].set_ylabel('Error (log scale)')
                axes1[1, 1].set_title('Error Analysis')
                axes1[1, 1].legend()
                axes1[1, 1].grid(True, alpha=0.3)
            
            plt.suptitle('VF-004: Analytical vs Numerical Solutions', fontsize=16)
            plt.tight_layout()
            plt.savefig('VF004_comparison_plot.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("   比較プロット保存: VF004_comparison_plot.png")
            
            # 2. 個別プロット
            fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
            
            # 時系列発展
            axes2[0, 0].plot(df_numerical['t'], df_numerical['A_numerical'], 
                            'b-', label='System A', linewidth=2)
            axes2[0, 0].plot(df_numerical['t'], df_numerical['B_numerical'], 
                            'r-', label='System B', linewidth=2)
            axes2[0, 0].set_xlabel('Time')
            axes2[0, 0].set_ylabel('State Variable')
            axes2[0, 0].set_title('Time Series Evolution')
            axes2[0, 0].legend()
            axes2[0, 0].grid(True, alpha=0.3)
            
            # 位相平面
            axes2[0, 1].plot(df_numerical['A_numerical'], df_numerical['B_numerical'], 
                            'g-', linewidth=2)
            axes2[0, 1].plot(df_numerical['A_numerical'].iloc[0], df_numerical['B_numerical'].iloc[0],
                            'ko', markersize=10, label='Initial')
            axes2[0, 1].plot(df_numerical['A_numerical'].iloc[-1], df_numerical['B_numerical'].iloc[-1],
                            'ro', markersize=10, label='Final')
            axes2[0, 1].set_xlabel('System A')
            axes2[0, 1].set_ylabel('System B')
            axes2[0, 1].set_title('Phase Plane')
            axes2[0, 1].legend()
            axes2[0, 1].grid(True, alpha=0.3)
            
            # 対数プロット
            axes2[1, 0].semilogy(df_numerical['t'], df_numerical['A_numerical'], 
                                'b-', label='System A', linewidth=2)
            axes2[1, 0].semilogy(df_numerical['t'], df_numerical['B_numerical'], 
                                'r-', label='System B', linewidth=2)
            axes2[1, 0].set_xlabel('Time')
            axes2[1, 0].set_ylabel('State Variable (log scale)')
            axes2[1, 0].set_title('Logarithmic Time Series')
            axes2[1, 0].legend()
            axes2[1, 0].grid(True, alpha=0.3)
            
            # 微分値
            dA_dt = np.gradient(df_numerical['A_numerical'], df_numerical['t'])
            dB_dt = np.gradient(df_numerical['B_numerical'], df_numerical['t'])
            axes2[1, 1].plot(df_numerical['t'], dA_dt, 'b--', label='dA/dt', linewidth=2)
            axes2[1, 1].plot(df_numerical['t'], dB_dt, 'r--', label='dB/dt', linewidth=2)
            axes2[1, 1].set_xlabel('Time')
            axes2[1, 1].set_ylabel('Rate of Change')
            axes2[1, 1].set_title('Derivatives')
            axes2[1, 1].legend()
            axes2[1, 1].grid(True, alpha=0.3)
            
            plt.suptitle('VF-004: Numerical Solution Analysis', fontsize=16)
            plt.tight_layout()
            plt.savefig('VF004_numerical_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("   数値解析プロット保存: VF004_numerical_analysis.png")
            
        except Exception as e:
            print(f"   可視化中にエラー: {e}")
    
    def generate_report(self):
        """レポート生成"""
        print("\n5. レポート生成中...")
        
        # システム情報
        system_info = {
            'alpha': self.system.alpha,
            'beta': self.system.beta,
            'gamma': self.system.gamma,
            'delta': self.system.delta,
            'A0': self.system.A0,
            'B0': self.system.B0,
            't_end': self.system.t_end
        }
        
        with open('VF004_system_info.json', 'w') as f:
            json.dump(system_info, f, indent=2)
        
        # 統計情報があれば読み込み
        stats = {}
        if os.path.exists('VF004_comparison_stats.json'):
            with open('VF004_comparison_stats.json', 'r') as f:
                stats = json.load(f)
        
        # 簡易レポート
        report = f"""
========================================
VF-004 解析レポート
========================================

1. システムパラメータ:
   成長率係数 (α): {system_info['alpha']}
   減衰率係数 (β): {system_info['beta']}
   結合係数 (γ): {system_info['gamma']}
   外部擾乱係数 (δ): {system_info['delta']}
   初期値 A: {system_info['A0']}
   初期値 B: {system_info['B0']}
   シミュレーション時間: {system_info['t_end']}

2. 生成ファイル:
   - VF004_analytical_data.csv (解析解データ)
   - VF004_numerical_data.csv (数値解データ)
   - VF004_integrated_results.csv (統合結果)
   - VF004_system_info.json (システム情報)
   - VF004_comparison_stats.json (比較統計)
   - VF004_comparison_plot.png (比較プロット)
   - VF004_numerical_analysis.png (数値解析プロット)

3. 比較結果:
   平均誤差 A: {stats.get('mean_error_A', 'N/A'):.2e}
   平均誤差 B: {stats.get('mean_error_B', 'N/A'):.2e}
   最大誤差 A: {stats.get('max_error_A', 'N/A'):.2e}
   最大誤差 B: {stats.get('max_error_B', 'N/A'):.2e}
   相関係数 A: {stats.get('correlation_A', 'N/A'):.6f}
   相関係数 B: {stats.get('correlation_B', 'N/A'):.6f}

4. 解析方法:
   - 解析解: 行列指数関数法 (scipy.linalg.expm)
   - 数値解: RK45法 (scipy.integrate.solve_ivp)
   - 誤差評価: L2ノルムと相関係数

========================================
解析完了: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
"""
        
        with open('VF004_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        print("   レポート保存: VF004_report.txt")

# ============================================================================
# 3. メイン実行
# ============================================================================

if __name__ == "__main__":
    try:
        # 解析実行
        analyzer = VF004_Complete_Analysis()
        
        # 解析解計算
        analyzer.run_analytical()
        
        # 数値解計算
        analyzer.run_numerical()
        
        # 比較
        analyzer.compare_solutions()
        
        # 可視化
        analyzer.plot_results()
        
        # レポート生成
        analyzer.generate_report()
        
        print("\n" + "=" * 70)
        print("✅ VF-004 完全解析完了!")
        print("=" * 70)
        
        # 生成ファイル一覧
        print("\n📁 生成ファイル:")
        files = [f for f in os.listdir('.') if f.startswith('VF004')]
        for file in sorted(files):
            size = os.path.getsize(file)
            print(f"  - {file} ({size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 トラブルシューティング:")
        print("1. 必要なライブラリをインストール:")
        print("   pip install numpy scipy pandas matplotlib")
        print("2. もしscipy.linalg.expmでエラーが出る場合は:")
        print("   pip install --upgrade scipy")
        print("3. 環境を確認:")
        print("   python --version")
        print("   pip list | grep -E 'numpy|scipy|pandas|matplotlib'")
