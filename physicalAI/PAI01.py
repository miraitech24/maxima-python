#!/usr/bin/env python3
"""
PAI-01 Advanced: Venus Atmospheric Angular Momentum Analysis
Maximaで積分計算、Pythonでシミュレーション
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import platform

class PAI01AdvancedAnalyzer:
    def __init__(self):
        self.params = {}
        self.has_japanese = False
        
    def check_maxima_file(self):
        """Maxima出力ファイルの確認"""
        if not os.path.exists('PAI-01_maxima_advanced.txt'):
            print("エラー: PAI-01_maxima_advanced.txt が見つかりません")
            print("Maximaを先に実行してください: maxima -b PAI-01_advanced.mac")
            sys.exit(1)
        print("✓ Maxima出力ファイルを確認")
        return True
    
    def load_maxima_results(self):
       """Maxima結果を読み込み - 修正版"""
       try:
           with open('PAI-01_maxima_clean.txt', 'r') as f:
               lines = f.readlines()
           
           for line in lines:
               line = line.strip()
               if '=' in line and not line.startswith('#'):
                   # 'L_total_integrated=1.23e27' のような形式
                   key, value = line.split('=', 1)
                   key = key.strip()
                   value = value.strip()
                   
                   try:
                       self.params[key] = float(value)
                   except ValueError:
                       print(f"警告: 数値変換失敗 {key}={value}")
                       continue
           
           # 必須パラメータチェック
           required = ['L_total_integrated', 'I_r_integral', 'I_theta_integral', 
                      'omega_average', 'E_rotational', 'L_earth']
           missing = [p for p in required if p not in self.params]
           
           if missing:
               print(f"エラー: 必須パラメータ不足: {missing}")
               sys.exit(1)
               
           print("✓ Maxima積分結果を読み込み")
           print(f"  読み込んだパラメータ数: {len(self.params)}")
           return True
           
       except Exception as e:
           print(f"エラー: ファイル読み込み失敗: {e}")
           print("ファイル内容:")
           try:
               with open('PAI-01_maxima_clean.txt', 'r') as f:
                   print(f.read())
           except:
               print("ファイルを開けません")
           sys.exit(1)
   
    def setup_font(self):
        """フォント設定"""
        try:
            system = platform.system()
            
            if system == 'Linux':
                plt.rcParams['font.family'] = 'IPAexGothic'
                self.has_japanese = True
            elif system == 'Darwin':
                plt.rcParams['font.family'] = 'Hiragino Sans'
                self.has_japanese = True
            elif system == 'Windows':
                plt.rcParams['font.family'] = 'MS Gothic'
                self.has_japanese = True
            else:
                plt.rcParams['font.family'] = 'DejaVu Sans'
                self.has_japanese = False
            
            plt.rcParams['font.size'] = 11
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['figure.autolayout'] = True
            
            print(f"✓ システム: {system}, フォント: {plt.rcParams['font.family']}")
            return True
            
        except Exception as e:
            print(f"フォント設定エラー: {e}")
            plt.rcParams['font.family'] = 'DejaVu Sans'
            plt.rcParams['font.size'] = 11
            return False
    def create_plots(self):
        """4つのグラフを作成 - Maxima積分結果を使用"""
        # フォント設定
        self.setup_font()
        
        # データ取得
        L_venus = self.params['L_total_integrated']
        L_earth = self.params['L_earth']
        E_rot = self.params['E_rotational']
        omega_avg = self.params['omega_average']
        I_r = self.params['I_r_integral']
        I_theta = self.params['I_theta_integral']
        
        # 図の作成
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # タイトル設定
        if self.has_japanese:
            main_title = 'PAI-01: 金星大気角運動量分析（積分計算版）'
            titles = [
                '角運動量比較（Maxima積分結果）',
                '積分計算の内訳',
                'SR制動シミュレーション（積分モデル）',
                'PhysicalAI制御パラメータ'
            ]
        else:
            main_title = 'PAI-01: Venus Atmospheric Angular Momentum Analysis (Integrated)'
            titles = [
                'Angular Momentum Comparison (Maxima Integration)',
                'Integration Components Breakdown',
                'SR Braking Simulation (Integrated Model)',
                'PhysicalAI Control Parameters'
            ]
        
        fig.suptitle(main_title, fontsize=16, fontweight='bold', y=0.98)
        
        # 1. 角運動量比較（積分結果）
        ax1 = axes[0, 0]
        objects = ['Venus\n(Integrated)', 'Earth\n(Simple)', 'Venus\n(Simple)', 'Jupiter\n(Atmosphere)']
        
        # 計算値
        L_venus_simple = (2/5) * 4.8e20 * (6.05e6)**2 * 1.992e-7
        
        values = [L_venus, L_earth, L_venus_simple, 6.9e38]
        
        bars1 = ax1.bar(objects, np.log10(values), 
                       color=['#ff6b6b', '#4ecdc4', '#ff9999', '#45b7d1'],
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax1.set_ylabel('log₁₀(L) [log₁₀(kg·m²/s)]', fontsize=11)
        ax1.set_title(titles[0], fontsize=13, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 数値ラベル
        for bar, val in zip(bars1, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{val:.1e}', ha='center', va='bottom', fontsize=10,
                    fontweight='bold')
        
        # 2. 積分計算の内訳
        ax2 = axes[0, 1]
        components = ['I_r (Radial)\n∫ρ(r)r⁴dr', 'I_θ (Latitudinal)\n∫sin³θdθ', 
                     'ω_avg (Average)\n(1/2π)∫ω(φ)dφ', 'Total Product\nL = I_r×I_θ×ω_avg']
        component_values = [I_r, I_theta, omega_avg, L_venus]
        
        # 対数スケールで表示
        log_values = np.log10(np.abs(component_values))
        
        bars2 = ax2.bar(components, log_values,
                       color=['#ff9f43', '#54a0ff', '#5f27cd', '#1dd1a1'],
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax2.set_ylabel('log₁₀(Value)', fontsize=11)
        ax2.set_title(titles[1], fontsize=13, fontweight='bold', pad=15)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 実際の値ラベル
        for bar, val in zip(bars2, component_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{val:.1e}', ha='center', va='bottom', fontsize=9)
        
        # 3. SR制動シミュレーション（積分モデル）
        ax3 = axes[1, 0]
        time = np.linspace(0, 500, 200)  # 500年まで
        
        # 異なる時定数での減衰（積分モデルに基づく）
        tau_values = [75, 150, 300]  # 積分モデルでは時定数が長くなる
        
        colors = ['#ff3838', '#0652DD', '#009432']
        line_styles = ['-', '--', ':']
        
        for tau, color, ls in zip(tau_values, colors, line_styles):
            L_t = L_venus * np.exp(-time/tau)
            ax3.plot(time, L_t, color=color, linewidth=2.5, 
                    linestyle=ls, label=f'τ = {tau} years')
        
        ax3.set_xlabel('Time [years]' if not self.has_japanese else '時間 [年]', fontsize=11)
        ax3.set_ylabel('L [kg·m²/s]', fontsize=11)
        ax3.set_title(titles[2], fontsize=13, fontweight='bold', pad=15)
        ax3.legend(fontsize=10, loc='upper right')
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.set_yscale('log')
        
        # 目標ライン（地球の角運動量レベル）
        ax3.axhline(y=L_earth, color='gray', linestyle='--', alpha=0.5, 
                   label=f'Earth: {L_earth:.1e}')
        ax3.legend(fontsize=9)
        
        # 4. PhysicalAI制御パラメータ（積分モデルに基づく）
        ax4 = axes[1, 1]
        P_10TW = 1e13
        tau_torque = P_10TW / omega_avg  # 平均角速度を使用
        
        # 制動時間計算
        braking_time = L_venus / tau_torque
        years_to_brake = braking_time / (365.25 * 24 * 3600)
        
        param_labels = ['Required Torque\n(10TW, ω_avg)', 'Braking Time\n(to Earth level)', 
                       'Energy per Year\n(10TW continuous)', 'Angular Momentum\nChange Rate']
        param_values = [tau_torque, years_to_brake, P_10TW * 3.156e7, L_venus/braking_time]
        
        bars4 = ax4.bar(param_labels, np.log10(np.abs(param_values)),
                       color=['#8e44ad', '#e74c3c', '#3498db', '#2ecc71'],
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax4.set_ylabel('log₁₀(Value)', fontsize=11)
        ax4.set_title(titles[3], fontsize=13, fontweight='bold', pad=15)
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 実際の値ラベル
        units = ['N·m', 'years', 'J/year', 'kg·m²/s²']
        for bar, val, unit in zip(bars4, param_values, units):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{val:.1e}\n{unit}', ha='center', va='bottom', 
                    fontsize=9, linespacing=0.9)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        
        # 保存
        plt.savefig('PAI-01_analysis_advanced.png', dpi=150, bbox_inches='tight')
        print("✓ グラフ保存: PAI-01_analysis_advanced.png")
        
        # 表示
        plt.show()
        
        return True
    def save_results(self):
        """結果をCSVとサマリーに保存 - 積分版"""
        L_venus = self.params['L_total_integrated']
        E_rot = self.params['E_rotational']
        L_earth = self.params['L_earth']
        I_r = self.params['I_r_integral']
        I_theta = self.params['I_theta_integral']
        omega_avg = self.params['omega_average']
        
        # 追加計算
        ratio = L_venus / L_earth
        hurricane_eq = E_rot / 1.5e17
        human_years = E_rot / 5.8e20
        
        # PAI-11関連計算（積分モデルに基づく）
        P_10TW = 1e13
        tau_torque = P_10TW / omega_avg
        braking_time = L_venus / tau_torque
        years_to_brake = braking_time / (365.25 * 24 * 3600)
        
        # 簡易モデルとの比較
        L_venus_simple = (2/5) * 4.8e20 * (6.05e6)**2 * 1.992e-7
        ratio_simple_integrated = L_venus_simple / L_venus
        
        # CSV保存
        results = pd.DataFrame({
            'Parameter': [
                'Angular Momentum (Venus, Integrated)', 'Angular Momentum (Venus, Simple)',
                'Radial Integral I_r', 'Latitudinal Integral I_theta',
                'Average Angular Velocity ω_avg', 'Rotational Energy',
                'Moment of Inertia I_shell', 'Angular Momentum (Earth)',
                'Venus/Earth Ratio (Integrated)', 'Venus/Earth Ratio (Simple)',
                'Integrated/Simple Ratio', 'Hurricane Equivalents',
                'Human Energy Years', 'Required Torque (10TW, ω_avg)',
                'Braking Time Constant (years)', 'Angular Momentum Change Rate',
                'Energy per Year (10TW)'
            ],
            'Value': [
                L_venus, L_venus_simple, I_r, I_theta, omega_avg,
                E_rot, self.params.get('I_shell', 0), L_earth,
                ratio, L_venus_simple/L_earth, ratio_simple_integrated,
                hurricane_eq, human_years, tau_torque, years_to_brake,
                L_venus/braking_time, P_10TW * 3.156e7
            ],
            'Unit': [
                'kg·m²/s', 'kg·m²/s', 'kg·m⁵', 'dimensionless', 'rad/s',
                'J', 'kg·m²', 'kg·m²/s', 'ratio', 'ratio', 'ratio',
                'count', 'years', 'N·m', 'years', 'kg·m²/s²', 'J/year'
            ]
        })
        
        results.to_csv('PAI-01_results_advanced.csv', index=False)
        print("✓ 結果保存: PAI-01_results_advanced.csv")
        
        # サマリーファイル
        if self.has_japanese:
            summary = f"""PAI-01: 金星大気角運動量 分析結果（積分計算版）
{'='*70}

【Maxima積分計算結果】
1. 角運動量（積分） L = {L_venus:.2e} kg·m²/s
2. 角運動量（簡易） L_simple = {L_venus_simple:.2e} kg·m²/s
3. 積分/簡易比 = {ratio_simple_integrated:.3f}
4. 積分内訳:
   - 半径方向積分 I_r = {I_r:.2e} kg·m⁵
   - 緯度方向積分 I_θ = {I_theta:.4f}
   - 平均角速度 ω_avg = {omega_avg:.2e} rad/s

【比較分析】
5. 地球大気との比較:
   - 地球の角運動量: {L_earth:.2e} kg·m²/s
   - 金星/地球比（積分）: {ratio:.3f}
   - 金星/地球比（簡易）: {L_venus_simple/L_earth:.3f}

6. エネルギー換算:
   - {hurricane_eq:.0f} 個の大型ハリケーン分
   - 人類の年間エネルギー消費量の {human_years:.3f} 年分
   - {E_rot/4.2e9:.0f} トンのTNT爆薬相当

【PhysicalAI関連性】
7. SR制動評価（積分モデル）:
   - 10TWでの必要トルク: {tau_torque:.2e} N·m
   - 地球レベルまでの制動時間: {years_to_brake:.1f} 年
   - 角運動量変化率: {L_venus/braking_time:.2e} kg·m²/s²

8. 積分計算の意義:
   - 大気分布の非一様性を考慮
   - 緯度依存の角速度分布を反映
   - 簡易モデルより {abs(1-ratio_simple_integrated)*100:.1f}% の差

【考察】
9. 技術的示唆:
   - 積分計算により角運動量が簡易計算より {abs(1-ratio_simple_integrated)*100:.1f}% 異なる
   - 制動時間は {years_to_brake:.0f} 年と長期にわたる
   - 10TW級エネルギー源で実現可能な規模

10. 次の課題:
   - PAI-11: 制動トルクの詳細設計
   - PAI-04: エネルギー供給システム
   - PAI-05: エネルギー伝送効率
"""
        else:
            summary = f"""PAI-01: Venus Atmospheric Angular Momentum Analysis (Integrated)
{'='*70}

【Maxima Integration Results】
1. Angular Momentum (Integrated) L = {L_venus:.2e} kg·m²/s
2. Angular Momentum (Simple) L_simple = {L_venus_simple:.2e} kg·m²/s
3. Integrated/Simple Ratio = {ratio_simple_integrated:.3f}
4. Integration Components:
   - Radial Integral I_r = {I_r:.2e} kg·m⁵
   - Latitudinal Integral I_θ = {I_theta:.4f}
   - Average Angular Velocity ω_avg = {omega_avg:.2e} rad/s

【Comparative Analysis】
5. Comparison with Earth:
   - Earth angular momentum: {L_earth:.2e} kg·m²/s
   - Venus/Earth ratio (Integrated): {ratio:.3f}
   - Venus/Earth ratio (Simple): {L_venus_simple/L_earth:.3f}

6. Energy Equivalents:
   - Equivalent to {hurricane_eq:.0f} large hurricanes
   - {human_years:.3f} years of human annual energy consumption
   - {E_rot/4.2e9:.0f} tons of TNT equivalent

【PhysicalAI Relevance】
7. SR Braking Assessment (Integrated Model):
   - Required torque at 10TW: {tau_torque:.2e} N·m
   - Braking time to Earth level: {years_to_brake:.1f} years
   - Angular momentum change rate: {L_venus/braking_time:.2e} kg·m²/s²

8. Significance of Integration:
   - Accounts for atmospheric non-uniformity
   - Reflects latitude-dependent angular velocity
   - {abs(1-ratio_simple_integrated)*100:.1f}% difference from simple model

【Discussion】
9. Technical Implications:
   - Integrated calculation differs by {abs(1-ratio_simple_integrated)*100:.1f}% from simple
   - Braking time requires {years_to_brake:.0f} years
   - Feasible with 10TW-class energy source

10. Next Steps:
   - PAI-11: Detailed braking torque design
   - PAI-04: Energy supply system
   - PAI-05: Energy transmission efficiency
"""
        
        with open('PAI-01_summary_advanced.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print("✓ サマリー保存: PAI-01_summary_advanced.txt")
    
    def run(self):
        """メイン実行"""
        print("="*70)
        print("PAI-01: 金星大気角運動量分析（積分計算版） 開始")
        print("="*70)
        
        # 1. ファイルチェック
        self.check_maxima_file()
        
        # 2. 結果読み込み
        self.load_maxima_results()
        
        # 3. 計算結果表示
        print(f"\n【Maxima積分計算結果】")
        print(f"  角運動量（積分） L = {self.params['L_total_integrated']:.2e} kg·m²/s")
        print(f"  角運動量（簡易） L_simple = {(2/5)*4.8e20*(6.05e6)**2*1.992e-7:.2e} kg·m²/s")
        print(f"  地球比（積分） = {self.params['L_total_integrated']/self.params['L_earth']:.3f}")
        
        # 4. 可視化
        self.create_plots()
        
        # 5. 結果保存
        self.save_results()
        
        print("\n" + "="*70)
        print("PAI-01 積分計算版 分析完了")
        print("="*70)

if __name__ == "__main__":
    analyzer = PAI01AdvancedAnalyzer()
    analyzer.run()
