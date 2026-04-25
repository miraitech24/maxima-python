#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:18:12 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-003: 硫酸還元と水量収支の動的連成シミュレーション
修正版 - エラー修正と日本語対応
"""

import numpy as np
from scipy.integrate import odeint
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # バックエンドを指定（GUIなし環境用）
import matplotlib.pyplot as plt
import warnings
import os
import sys
from datetime import datetime

# ======================== 日本語フォント設定 ========================

def setup_japanese_font():
    """日本語フォントの設定"""
    try:
        # 日本語フォントを検索
        font_dirs = [
            '/usr/share/fonts/opentype/noto/',
            '/usr/share/fonts/truetype/takao/',
            '/usr/share/fonts/truetype/ipa-gothic/',
            '/usr/share/fonts/truetype/mona/',
        ]
        
        japanese_fonts = []
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.endswith(('.ttf', '.ttc', '.otf')):
                            # 日本語フォントを優先
                            if 'NotoSansCJK' in file or 'Noto Sans CJK' in file or \
                               'Takao' in file or 'IPAGothic' in file or 'Mona' in file:
                                font_path = os.path.join(root, file)
                                japanese_fonts.append(font_path)
        
        # フォントが見つかったら設定
        if japanese_fonts:
            import matplotlib.font_manager as fm
            # 最初の日本語フォントを使用
            font_path = japanese_fonts[0]
            fm.fontManager.addfont(font_path)
            font_name = fm.FontProperties(fname=font_path).get_name()
            plt.rcParams['font.family'] = font_name
            print(f"✓ 日本語フォント設定: {font_name}")
        else:
            # 英語フォント設定
            plt.rcParams['font.family'] = 'DejaVu Sans'
            print("⚠ 日本語フォントが見つかりません。英語フォントを使用します。")
        
        plt.rcParams['axes.unicode_minus'] = False
        
    except Exception as e:
        print(f"⚠ フォント設定エラー: {e}")
        plt.rcParams['font.family'] = 'DejaVu Sans'

# フォント設定を実行
setup_japanese_font()

# ======================== 定数定義 ========================

# 物理定数
EARTH_OCEAN_DEPTH_AVG = 3688  # 地球の平均海洋深度 (m)
VENUS_SURFACE_AREA = 4.602e8  # 金星の表面積 (km²) → m²に変換
VENUS_SURFACE_AREA_M2 = VENUS_SURFACE_AREA * 1e6  # m²

# 化学反応定数
MOLAR_MASS_H2SO4 = 98.08  # 硫酸のモル質量 (g/mol)
MOLAR_MASS_H2O = 18.015  # 水のモル質量 (g/mol)
MOLAR_MASS_S = 32.06  # 硫黄のモル質量 (g/mol)
MOLAR_MASS_O2 = 32.00  # 酸素のモル質量 (g/mol)

# 変換係数
H2SO4_TO_H2O_RATIO = (2 * MOLAR_MASS_H2O) / MOLAR_MASS_H2SO4  # 硫酸から水への変換率
H2SO4_TO_S_RATIO = MOLAR_MASS_S / MOLAR_MASS_H2SO4  # 硫酸から硫黄への変換率
H2SO4_TO_O2_RATIO = (2 * MOLAR_MASS_O2) / MOLAR_MASS_H2SO4  # 硫酸から酸素への変換率

# ======================== メインクラス ========================

class SulfuricAcidReductionModel:
    """硫酸還元モデルクラス"""
    
    def __init__(self):
        # 初期条件
        self.initial_conditions = {
            # 金星大気中の硫酸量 (kg)
            'H2SO4_mass_initial': 1.2e15,  # 1.2兆トン
            # 初期水量 (kg)
            'H2O_mass_initial': 1.0e10,  # 初期はほとんどなし
            # 硫黄貯蔵量 (kg)
            'S_mass_initial': 0.0,
            # 酸素生成量 (kg)
            'O2_mass_initial': 0.0
        }
        
        # 反応パラメータ
        self.params = {
            # エネルギー供給率 (W → J/s)
            'power_supply': 10e12,  # 10 TW
            # 反応効率
            'efficiency': 0.85,
            # 反応エネルギー要件 (J/kg H2SO4)
            'energy_per_kg_H2SO4': 5e6,  # 5 MJ/kg
            # 時間設定
            'simulation_years': 300,
            'time_step_days': 30  # 30日ステップ
        }
        
        # 計算結果
        self.results = {}
    
    def calculate_reaction_rate(self, H2SO4_mass, power_available):
        """
        反応速度を計算
        
        パラメータ:
        -----------
        H2SO4_mass : float
            現在の硫酸量 (kg)
        power_available : float
            利用可能な電力 (J/s)
        
        戻り値:
        --------
        reaction_rate : float
            反応速度 (kg/s)
        """
        # 最大反応速度 (利用可能なエネルギーに基づく)
        max_rate_energy = (power_available * self.params['efficiency'] * 
                          self.params['time_step_days'] * 86400 / 
                          self.params['energy_per_kg_H2SO4'])
        
        # 利用可能な硫酸量による制限
        max_rate_mass = H2SO4_mass * 0.01  # 1%以下/ステップ
        
        # 反応速度は両方の制限の小さい方
        reaction_rate = min(max_rate_energy, max_rate_mass)
        
        return reaction_rate
    
    def system_equations(self, y, t):
        """
        微分方程式系
        
        y[0]: H2SO4質量 (kg)
        y[1]: H2O質量 (kg)
        y[2]: S質量 (kg)
        y[3]: O2質量 (kg)
        """
        H2SO4, H2O, S, O2 = y
        
        # 利用可能な電力 (一定と仮定)
        power_available = self.params['power_supply']
        
        # 反応速度を計算
        reaction_rate = self.calculate_reaction_rate(H2SO4, power_available)
        
        # 微分方程式
        dH2SO4_dt = -reaction_rate  # 硫酸減少
        dH2O_dt = reaction_rate * H2SO4_TO_H2O_RATIO  # 水生成
        dS_dt = reaction_rate * H2SO4_TO_S_RATIO  # 硫黄生成
        dO2_dt = reaction_rate * H2SO4_TO_O2_RATIO  # 酸素生成
        
        return [dH2SO4_dt, dH2O_dt, dS_dt, dO2_dt]
    
    def simulate(self):
        """
        シミュレーション実行
        """
        print("🚀 シミュレーション実行中...")
        
        # 初期条件
        y0 = [
            self.initial_conditions['H2SO4_mass_initial'],
            self.initial_conditions['H2O_mass_initial'],
            self.initial_conditions['S_mass_initial'],
            self.initial_conditions['O2_mass_initial']
        ]
        
        # 時間配列 (日単位 → 秒単位に変換)
        days_per_year = 365
        total_days = self.params['simulation_years'] * days_per_year
        t_days = np.arange(0, total_days, self.params['time_step_days'])
        t_seconds = t_days * 86400  # 日→秒
        
        # 数値積分
        solution = odeint(self.system_equations, y0, t_seconds)
        
        # 結果を保存
        self.results = {
            'time_days': t_days,
            'time_years': t_days / days_per_year,
            'H2SO4_mass': solution[:, 0],
            'H2O_mass': solution[:, 1],
            'S_mass': solution[:, 2],
            'O2_mass': solution[:, 3]
        }
        
        # 追加の計算
        self._calculate_derived_quantities()
        
        print("✅ シミュレーション完了")
        return self.results
    
    def _calculate_derived_quantities(self):
        """
        派生量を計算
        """
        if not self.results:
            return
        
        # 水深の計算 (m)
        water_volume = self.results['H2O_mass'] / 1000  # 質量(kg) → 体積(m³)
        water_depth = water_volume / VENUS_SURFACE_AREA_M2  # 水深(m)
        
        # 硫酸還元率 (%)
        initial_H2SO4 = self.initial_conditions['H2SO4_mass_initial']
        reduction_percentage = (1 - self.results['H2SO4_mass'] / initial_H2SO4) * 100
        
        # 反応速度の計算
        reaction_rate = np.zeros_like(self.results['time_days'])
        for i in range(len(reaction_rate)):
            if i == 0:
                reaction_rate[i] = 0
            else:
                dt = (self.results['time_days'][i] - self.results['time_days'][i-1]) * 86400
                dH2SO4 = self.results['H2SO4_mass'][i-1] - self.results['H2SO4_mass'][i]
                reaction_rate[i] = dH2SO4 / dt if dt > 0 else 0
        
        # 追加の結果を保存
        self.results.update({
            'water_depth': water_depth,
            'reduction_percentage': reduction_percentage,
            'reaction_rate': reaction_rate,
            'water_volume': water_volume
        })
        
        # 統計情報の計算
        self.statistics = {
            'final_water_depth': water_depth[-1],
            'final_reduction_percentage': reduction_percentage[-1],
            'max_reaction_rate': np.max(reaction_rate),
            'total_water_produced': water_volume[-1] / 1e9,  # 10億m³単位
            'total_sulfur_produced': self.results['S_mass'][-1] / 1e12,  # 兆トン単位
            'total_oxygen_produced': self.results['O2_mass'][-1] / 1e12  # 兆トン単位
        }
    
    def visualize_results(self):
        """
        結果を可視化
        """
        if not self.results:
            print("⚠ 結果がありません。先にsimulate()を実行してください。")
            return
        
        print("📊 結果を可視化中...")
        
        # データ取得
        time_years = self.results['time_years']
        
        # 1. メイングラフセット
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle('VF-003: 硫酸還元と水量収支の動的連成シミュレーション', 
                    fontsize=16, fontweight='bold')
        
        # 1.1 硫酸質量の変化
        ax1 = plt.subplot(3, 3, 1)
        ax1.plot(time_years, self.results['H2SO4_mass'] / 1e12, 'red', linewidth=2)
        ax1.set_xlabel('時間 (年)')
        ax1.set_ylabel('硫酸質量 (兆トン)')
        ax1.set_title('硫酸質量の時間変化')
        ax1.grid(True, alpha=0.3)
        
        # 1.2 水量の変化
        ax2 = plt.subplot(3, 3, 2)
        ax2.plot(time_years, self.results['H2O_mass'] / 1e12, 'blue', linewidth=2)
        ax2.set_xlabel('時間 (年)')
        ax2.set_ylabel('水質量 (兆トン)')
        ax2.set_title('水生成の時間変化')
        ax2.grid(True, alpha=0.3)
        
        # 1.3 水深の変化
        ax3 = plt.subplot(3, 3, 3)
        ax3.plot(time_years, self.results['water_depth'], 'cyan', linewidth=2)
        ax3.axhline(y=EARTH_OCEAN_DEPTH_AVG, color='g', linestyle='--', alpha=0.7,
                   label=f'地球平均 ({EARTH_OCEAN_DEPTH_AVG:.0f} m)')
        ax3.set_xlabel('時間 (年)')
        ax3.set_ylabel('水深 (m)')
        ax3.set_title('金星表面の水深変化')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # 1.4 硫酸還元率
        ax4 = plt.subplot(3, 3, 4)
        ax4.plot(time_years, self.results['reduction_percentage'], 'orange', linewidth=2)
        ax4.axhline(y=90, color='r', linestyle=':', alpha=0.7, label='90%削減目標')
        ax4.axhline(y=95, color='orange', linestyle=':', alpha=0.7, label='95%削減目標')
        ax4.axhline(y=99, color='green', linestyle=':', alpha=0.7, label='99%削減目標')
        ax4.set_xlabel('時間 (年)')
        ax4.set_ylabel('硫酸還元率 (%)')
        ax4.set_title('硫酸還元率の時間変化')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        # 1.5 硫黄生成量
        ax5 = plt.subplot(3, 3, 5)
        ax5.plot(time_years, self.results['S_mass'] / 1e12, 'brown', linewidth=2)
        ax5.set_xlabel('時間 (年)')
        ax5.set_ylabel('硫黄質量 (兆トン)')
        ax5.set_title('硫黄生成量の時間変化')
        ax5.grid(True, alpha=0.3)
        
        # 1.6 酸素生成量
        ax6 = plt.subplot(3, 3, 6)
        ax6.plot(time_years, self.results['O2_mass'] / 1e12, 'green', linewidth=2)
        ax6.set_xlabel('時間 (年)')
        ax6.set_ylabel('酸素質量 (兆トン)')
        ax6.set_title('酸素生成量の時間変化')
        ax6.grid(True, alpha=0.3)
        
        # 1.7 反応速度
        ax7 = plt.subplot(3, 3, 7)
        ax7.plot(time_years, self.results['reaction_rate'] * 86400 * 365, 'purple', linewidth=2)  # kg/year
        ax7.set_xlabel('時間 (年)')
        ax7.set_ylabel('反応速度 (kg/年)')
        ax7.set_title('反応速度の時間変化')
        ax7.grid(True, alpha=0.3)
        
        # 1.8 相関関係: 硫酸減少 vs 水生成
        ax8 = plt.subplot(3, 3, 8)
        ax8.scatter(self.results['H2SO4_mass'] / 1e12, 
                   self.results['H2O_mass'] / 1e12, 
                   c=time_years, cmap='viridis', s=10, alpha=0.7)
        ax8.set_xlabel('硫酸質量 (兆トン)')
        ax8.set_ylabel('水質量 (兆トン)')
        ax8.set_title('硫酸減少と水生成の相関')
        ax8.grid(True, alpha=0.3)
        
        # 1.9 水量と水深の関係
        ax9 = plt.subplot(3, 3, 9)
        ax9.scatter(self.results['H2O_mass'] / 1e12, 
                   self.results['water_depth'], 
                   c=time_years, cmap='plasma', s=10, alpha=0.7)
        ax9.set_xlabel('水質量 (兆トン)')
        ax9.set_ylabel('水深 (m)')
        ax9.set_title('水量と水深の関係')
        ax9.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('VF003_results_main.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ メイングラフ保存: VF003_results_main.png")
        
        # 2. 詳細分析グラフ
        self._create_detailed_plots()
        
        return True
    
    def _create_detailed_plots(self):
        """
        詳細な分析グラフを作成
        """
        time_years = self.results['time_years']
        
        # 2.1 累積生成量グラフ
        fig2, axes2 = plt.subplots(2, 2, figsize=(15, 12))
        
        # 累積水量
        axes2[0, 0].fill_between(time_years, 0, self.results['H2O_mass'] / 1e12, 
                                color='blue', alpha=0.5)
        axes2[0, 0].plot(time_years, self.results['H2O_mass'] / 1e12, 
                        'blue', linewidth=2)
        axes2[0, 0].set_xlabel('時間 (年)')
        axes2[0, 0].set_ylabel('累積水量 (兆トン)')
        axes2[0, 0].set_title('累積水生成量')
        axes2[0, 0].grid(True, alpha=0.3)
        
        # 累積硫酸減少量
        initial_H2SO4 = self.initial_conditions['H2SO4_mass_initial']
        H2SO4_reduced = initial_H2SO4 - self.results['H2SO4_mass']
        axes2[0, 1].fill_between(time_years, 0, H2SO4_reduced / 1e12, 
                                color='red', alpha=0.5)
        axes2[0, 1].plot(time_years, H2SO4_reduced / 1e12, 
                        'red', linewidth=2)
        axes2[0, 1].set_xlabel('時間 (年)')
        axes2[0, 1].set_ylabel('累積硫酸減少量 (兆トン)')
        axes2[0, 1].set_title('累積硫酸還元量')
        axes2[0, 1].grid(True, alpha=0.3)
        
        # 累積硫黄生成量
        axes2[1, 0].fill_between(time_years, 0, self.results['S_mass'] / 1e12, 
                                color='brown', alpha=0.5)
        axes2[1, 0].plot(time_years, self.results['S_mass'] / 1e12, 
                        'brown', linewidth=2)
        axes2[1, 0].set_xlabel('時間 (年)')
        axes2[1, 0].set_ylabel('累積硫黄生成量 (兆トン)')
        axes2[1, 0].set_title('累積硫黄生成量')
        axes2[1, 0].grid(True, alpha=0.3)
        
        # 累積酸素生成量
        axes2[1, 1].fill_between(time_years, 0, self.results['O2_mass'] / 1e12, 
                                color='green', alpha=0.5)
        axes2[1, 1].plot(time_years, self.results['O2_mass'] / 1e12, 
                        'green', linewidth=2)
        axes2[1, 1].set_xlabel('時間 (年)')
        axes2[1, 1].set_ylabel('累積酸素生成量 (兆トン)')
        axes2[1, 1].set_title('累積酸素生成量')
        axes2[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('VF-003: 累積生成量分析', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('VF003_results_cumulative.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ 累積グラフ保存: VF003_results_cumulative.png")
        
        # 2.2 比率グラフ
        fig3, axes3 = plt.subplots(2, 2, figsize=(15, 12))
        
        # 水/硫酸比率
        water_H2SO4_ratio = self.results['H2O_mass'] / (self.results['H2SO4_mass'] + 1e-10)
        axes3[0, 0].plot(time_years, water_H2SO4_ratio, 'purple', linewidth=2)
        axes3[0, 0].set_xlabel('時間 (年)')
        axes3[0, 0].set_ylabel('H2O/H2SO4 比率')
        axes3[0, 0].set_title('水/硫酸比率の時間変化')
        axes3[0, 0].grid(True, alpha=0.3)
        
        # 硫黄/硫酸比率
        S_H2SO4_ratio = self.results['S_mass'] / (self.results['H2SO4_mass'] + 1e-10)
        axes3[0, 1].plot(time_years, S_H2SO4_ratio, 'orange', linewidth=2)
        axes3[0, 1].set_xlabel('時間 (年)')
        axes3[0, 1].set_ylabel('S/H2SO4 比率')
        axes3[0, 1].set_title('硫黄/硫酸比率の時間変化')
        axes3[0, 1].grid(True, alpha=0.3)
        
        # 酸素/硫酸比率
        O2_H2SO4_ratio = self.results['O2_mass'] / (self.results['H2SO4_mass'] + 1e-10)
        axes3[1, 0].plot(time_years, O2_H2SO4_ratio, 'cyan', linewidth=2)
        axes3[1, 0].set_xlabel('時間 (年)')
        axes3[1, 0].set_ylabel('O2/H2SO4 比率')
        axes3[1, 0].set_title('酸素/硫酸比率の時間変化')
        axes3[1, 0].grid(True, alpha=0.3)
        
        # 水深/地球比較
        earth_ratio = self.results['water_depth'] / EARTH_OCEAN_DEPTH_AVG * 100
        axes3[1, 1].plot(time_years, earth_ratio, 'red', linewidth=2)
        axes3[1, 1].axhline(y=100, color='g', linestyle='--', alpha=0.7,
                           label='地球平均 (100%)')
        axes3[1, 1].set_xlabel('時間 (年)')
        axes3[1, 1].set_ylabel('水深/地球比 (%)')
        axes3[1, 1].set_title('金星水深 vs 地球平均')
        axes3[1, 1].grid(True, alpha=0.3)
        axes3[1, 1].legend()
        
        plt.suptitle('VF-003: 比率分析', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('VF003_results_ratios.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ 比率グラフ保存: VF003_results_ratios.png")
        
        # 2.3 サマリーダッシュボード
        self._create_summary_dashboard()
    
    def _create_summary_dashboard(self):
        """
        サマリーダッシュボードを作成
        """
        fig4, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 統計データ
        stats = self.statistics
        
        # 1. キーメトリクス
        metrics = [
            f"最終水深: {stats['final_water_depth']:.1f} m",
            f"硫酸還元率: {stats['final_reduction_percentage']:.1f}%",
            f"総水生成: {stats['total_water_produced']:.1f} 10億m³",
            f"総硫黄生成: {stats['total_sulfur_produced']:.2f} 兆トン",
            f"総酸素生成: {stats['total_oxygen_produced']:.2f} 兆トン",
            f"最大反応速度: {stats['max_reaction_rate']*86400*365:.2e} kg/年"
        ]
        
        ax1.text(0.1, 0.9, "シミュレーション結果サマリー", 
                fontsize=14, fontweight='bold')
        for i, metric in enumerate(metrics):
            ax1.text(0.1, 0.8 - i*0.1, f"• {metric}", fontsize=12)
        ax1.axis('off')
        
        # 2. 硫酸減少プロセス図
        time_points = [0, 100, 200, 300]
        H2SO4_points = []
        H2O_points = []
        
        for t in time_points:
            idx = np.abs(self.results['time_years'] - t).argmin()
            H2SO4_points.append(self.results['H2SO4_mass'][idx] / 1e12)
            H2O_points.append(self.results['H2O_mass'][idx] / 1e12)
        
        bars = ax2.bar(time_points, H2SO4_points, color='red', alpha=0.7, label='硫酸')
        ax2_twin = ax2.twinx()
        ax2_twin.plot(time_points, H2O_points, 'bo-', linewidth=2, markersize=8, label='水')
        
        ax2.set_xlabel('時間 (年)')
        ax2.set_ylabel('硫酸質量 (兆トン)', color='red')
        ax2_twin.set_ylabel('水質量 (兆トン)', color='blue')
        ax2.set_title('主要物質の推移')
        
        # 凡例
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        # 3. 円グラフ: 最終物質分配
        final_masses = [
            self.results['H2SO4_mass'][-1],
            self.results['H2O_mass'][-1],
            self.results['S_mass'][-1],
            self.results['O2_mass'][-1]
        ]
        total = sum(final_masses)
        
        if total > 0:
            percentages = [m/total*100 for m in final_masses]
            labels = ['残留硫酸', '水', '硫黄', '酸素']
            colors = ['red', 'blue', 'brown', 'green']
            
            wedges, texts, autotexts = ax3.pie(percentages, labels=labels, colors=colors,
                                              autopct='%1.1f%%', startangle=90)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax3.set_title('300年後の物質分配')
        else:
            ax3.text(0.5, 0.5, 'データなし', ha='center', va='center')
            ax3.set_title('300年後の物質分配')
        
        # 4. 達成度ゲージ
        achievement = min(stats['final_reduction_percentage'], 100)
        
        # ゲージ図の作成
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        ax4.plot(theta, r, 'k-', linewidth=2)
        
        # ゲージの色
        achievement_rad = achievement/100 * np.pi
        theta_fill = np.linspace(0, achievement_rad, 100)
        r_fill = np.linspace(0.7, 1, 100)
        
        if achievement >= 90:
            color = 'green'
        elif achievement >= 70:
            color = 'orange'
        else:
            color = 'red'
        
        ax4.fill_between(theta_fill, 0.7, 1, color=color, alpha=0.5)
        ax4.text(np.pi/2, 1.2, f'硫酸還元達成度: {achievement:.1f}%', 
                ha='center', fontsize=14, fontweight='bold')
        
        # 目盛り
        for percent in [0, 25, 50, 75, 100]:
            theta_tick = percent/100 * np.pi
            ax4.plot([theta_tick, theta_tick], [0.95, 1.05], 'k-', linewidth=1)
            ax4.text(theta_tick, 1.1, f'{percent}%', ha='center')
        
        ax4.set_aspect('equal')
        ax4.axis('off')
        ax4.set_xlim(0, np.pi)
        ax4.set_ylim(0, 1.5)
        
        plt.suptitle('VF-003: 硫酸還元シミュレーション サマリーダッシュボード', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('VF003_summary_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ サマリーダッシュボード保存: VF003_summary_dashboard.png")
    
    def export_to_csv(self):
        """
        結果をCSVにエクスポート
        """
        if not self.results:
            print("⚠ 結果がありません。先にsimulate()を実行してください。")
            return None
        
        print("💾 結果をCSVにエクスポート中...")
        
        # データフレーム作成
        df = pd.DataFrame({
            'year': self.results['time_years'],
            'day': self.results['time_days'],
            'H2SO4_mass_ton': self.results['H2SO4_mass'] / 1000,  # トン
            'H2O_mass_ton': self.results['H2O_mass'] / 1000,  # トン
            'S_mass_ton': self.results['S_mass'] / 1000,  # トン
            'O2_mass_ton': self.results['O2_mass'] / 1000,  # トン
            'water_depth_m': self.results['water_depth'],
            'reduction_percentage': self.results['reduction_percentage'],
            'reaction_rate_kg_per_s': self.results['reaction_rate'],
            'water_volume_m3': self.results['water_volume']
        })
        
        # CSV保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'VF003_results_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # 要約CSV (10年ごと)
        summary_indices = np.linspace(0, len(df)-1, 31, dtype=int)
        df_summary = df.iloc[summary_indices].copy()
        summary_filename = f'VF003_summary_{timestamp}.csv'
        df_summary.to_csv(summary_filename, index=False, encoding='utf-8-sig')
        
        print(f"✅ 詳細データ保存: {filename}")
        print(f"✅ 要約データ保存: {summary_filename}")
        
        # 統計レポート
        self._create_statistics_report()
        
        return df
    
    def _create_statistics_report(self):
        """
        統計レポートを作成
        """
        if not hasattr(self, 'statistics'):
            return
        
        stats = self.statistics
        
        report = f"""VF-003 硫酸還元シミュレーション 統計レポート
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
====================================================

1. 最終結果 (300年後):
   水深: {stats['final_water_depth']:.1f} m
   地球平均比: {stats['final_water_depth']/EARTH_OCEAN_DEPTH_AVG*100:.1f}%
   硫酸還元率: {stats['final_reduction_percentage']:.1f}%

2. 総生成量:
   水: {stats['total_water_produced']:.2f} 10億 m³
   硫黄: {stats['total_sulfur_produced']:.2f} 兆トン
   酸素: {stats['total_oxygen_produced']:.2f} 兆トン

3. 反応特性:
   最大反応速度: {stats['max_reaction_rate']*86400*365:.2e} kg/年
   平均反応速度: {np.mean(self.results['reaction_rate'])*86400*365:.2e} kg/年

4. 達成度評価:
   硫酸還元: {'達成' if stats['final_reduction_percentage'] >= 90 else '未達成'}
   水深目標: {'達成' if stats['final_water_depth'] >= 1000 else '未達成'}
   (注: 地球平均水深は {EARTH_OCEAN_DEPTH_AVG} m)
"""
        
        with open('VF003_statistics_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ 統計レポート保存: VF003_statistics_report.txt")
        
        # コンソールにも表示
        print("\n" + "="*70)
        print("📊 統計レポートサマリー")
        print("="*70)
        print(report)

# ======================== メイン実行 ========================

def main():
    """
    メイン実行関数
    """
    print("="*70)
    print("VF-003: 硫酸還元と水量収支の動的連成シミュレーション")
    print("="*70)
    
    try:
        # 1. モデル初期化
        print("\n1. モデルを初期化中...")
        model = SulfuricAcidReductionModel()
        
        # 2. シミュレーション実行
        print("\n2. シミュレーション実行中...")
        results = model.simulate()
        
        # 3. 結果可視化
        print("\n3. 結果を可視化中...")
        model.visualize_results()
        
        # 4. CSVエクスポート
        print("\n4. 結果をCSVにエクスポート中...")
        df = model.export_to_csv()
        
        # 5. 完了メッセージ
        print("\n" + "="*70)
        print("🎉 シミュレーション完了！")
        print("="*70)
        print("\n生成されたファイル:")
        print("  VF003_results_main.png          - メイン結果グラフ")
        print("  VF003_results_cumulative.png    - 累積グラフ")
        print("  VF003_results_ratios.png        - 比率グラフ")
        print("  VF003_summary_dashboard.png     - サマリーダッシュボード")
        print("  VF003_results_*.csv             - 詳細データCSV")
        print("  VF003_summary_*.csv             - 要約データCSV")
        print("  VF003_statistics_report.txt     - 統計レポート")
        
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()

# ======================== 実行 ========================

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    main()
