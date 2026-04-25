#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:14:38 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-103: 閉鎖生態系光合成効率 分析プログラム (Python)
Maxima結果を読み込み、詳細分析と可視化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import os
import matplotlib

# 日本語フォント設定
def setup_font():
    """フォント設定"""
    try:
        # 環境に応じた設定
        import platform
        system = platform.system()
        
        if system == 'Linux':
            # IPAexゴシックを試す
            font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
            if os.path.exists(font_path):
                matplotlib.font_manager.fontManager.addfont(font_path)
                font_name = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams['font.family'] = font_name
                print(f"✓ フォント: {font_name}")
                return True
    except:
        pass
    
    # デフォルト
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    matplotlib.rcParams['axes.unicode_minus'] = False
    return False

setup_font()

class Bio103Analyzer:
    """BIO-103: 閉鎖生態系光合成効率分析クラス"""
    
    def __init__(self):
        self.maxima_results = {}
        self.comparison_data = None
        
        # 実測データベース
        self.experimental_data = self._load_experimental_data()
    
    def _load_experimental_data(self):
        """実測データベースの読み込み"""
        return pd.DataFrame([
            {'system': 'BIOS-3', 'type': '藻類', 'duration_days': 180, 
             'efficiency': 0.015, 'biomass_kg_m2_day': 0.025, 'location': 'ロシア'},
            {'system': 'MELiSSA', 'type': '藻類', 'duration_days': 60,
             'efficiency': 0.018, 'biomass_kg_m2_day': 0.030, 'location': 'ESA'},
            {'system': 'CELSS', 'type': '高等植物', 'duration_days': 90,
             'efficiency': 0.012, 'biomass_kg_m2_day': 0.020, 'location': 'NASA'},
            {'system': 'BIOSPHERE 2', 'type': '混合', 'duration_days': 730,
             'efficiency': 0.010, 'biomass_kg_m2_day': 0.015, 'location': '米国'},
            {'system': 'EDEN ISS', 'type': '高等植物', 'duration_days': 365,
             'efficiency': 0.014, 'biomass_kg_m2_day': 0.028, 'location': '南極'},
            {'system': 'VEGGIE (ISS)', 'type': '高等植物', 'duration_days': 120,
             'efficiency': 0.011, 'biomass_kg_m2_day': 0.018, 'location': 'ISS'}
        ])
    
    def load_maxima_results(self, filename='bio103_for_python.txt'):
        """Maximaの結果を読み込み"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        self.maxima_results[key] = float(value)
            
            print("✓ Maxima結果を読み込みました")
            print(f"  藻類効率: {self.maxima_results.get('algae_efficiency', 0):.4f}")
            print(f"  植物効率: {self.maxima_results.get('plant_efficiency', 0):.4f}")
            
        except FileNotFoundError:
            print("⚠ ファイルが見つかりません。デフォルト値を使用します")
            self._set_defaults()
    
    def _set_defaults(self):
        """デフォルト値の設定"""
        self.maxima_results = {
            'algae_efficiency': 0.025,
            'plant_efficiency': 0.015,
            'algae_biomass_kg_m2_day': 0.035,
            'plant_biomass_kg_m2_day': 0.022,
            'algae_O2_g_m2_day': 42.0,
            'plant_O2_g_m2_day': 22.0
        }
    
    def analyze_efficiency_comparison(self):
        """効率比較分析"""
        print("\n" + "="*60)
        print("BIO-103: 閉鎖生態系光合成効率 分析")
        print("="*60)
        
        algae_eff = self.maxima_results.get('algae_efficiency', 0)
        plant_eff = self.maxima_results.get('plant_efficiency', 0)
        algae_biomass = self.maxima_results.get('algae_biomass_kg_m2_day', 0)
        plant_biomass = self.maxima_results.get('plant_biomass_kg_m2_day', 0)
        
        print(f"\n1. 計算結果:")
        print("-"*40)
        print(f"  藻類システム効率: {algae_eff:.4f} ({algae_eff*100:.2f}%)")
        print(f"  高等植物システム効率: {plant_eff:.4f} ({plant_eff*100:.2f}%)")
        print(f"  効率比 (藻類/植物): {algae_eff/plant_eff:.2f}倍")
        
        print(f"\n2. バイオマス生産性:")
        print("-"*40)
        print(f"  藻類: {algae_biomass:.4f} kg/m²/day")
        print(f"  植物: {plant_biomass:.4f} kg/m²/day")
        print(f"  生産性比: {algae_biomass/plant_biomass:.2f}倍")
        
        # 1人あたり必要面積の計算
        daily_calorie_needs = 2000  # kcal/人/day
        biomass_calorie_density = 4000  # kcal/kg (乾燥重量)
        required_biomass = daily_calorie_needs / biomass_calorie_density  # kg/人/day
        
        algae_area = required_biomass / algae_biomass  # m²/人
        plant_area = required_biomass / plant_biomass  # m²/人
        
        print(f"\n3. 1人あたり必要栽培面積:")
        print("-"*40)
        print(f"  藻類システム: {algae_area:.1f} m²/人")
        print(f"  高等植物システム: {plant_area:.1f} m²/人")
        print(f"  面積比 (植物/藻類): {plant_area/algae_area:.1f}倍")
        
        return {
            'algae_efficiency': algae_eff,
            'plant_efficiency': plant_eff,
            'algae_biomass': algae_biomass,
            'plant_biomass': plant_biomass,
            'algae_area_per_person': algae_area,
            'plant_area_per_person': plant_area
        }
    
    def plot_comparison_charts(self, analysis_results):
        """比較グラフの作成"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 効率比較（計算値 vs 実測値）
        ax1 = axes[0, 0]
        
        categories = ['藻類 (計算)', '藻類 (実測平均)', '植物 (計算)', '植物 (実測平均)']
        values = [
            analysis_results['algae_efficiency'],
            self.experimental_data[self.experimental_data['type'] == '藻類']['efficiency'].mean(),
            analysis_results['plant_efficiency'],
            self.experimental_data[self.experimental_data['type'] == '高等植物']['efficiency'].mean()
        ]
        
        colors = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax1.bar(categories, values, color=colors, edgecolor='black')
        ax1.set_ylabel('光合成効率', fontsize=12)
        ax1.set_title('効率比較: 計算値 vs 実測値', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(values) * 1.2)
        ax1.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{val:.3f}\n({val*100:.1f}%)', ha='center', va='bottom', fontsize=10)
        
        # 2. バイオマス生産性
        ax2 = axes[0, 1]
        categories2 = ['藻類', '高等植物']
        biomass_values = [analysis_results['algae_biomass'], analysis_results['plant_biomass']]
        
        bars2 = ax2.bar(categories2, biomass_values, color=['#4ECDC4', '#96CEB4'], 
                       edgecolor='black', alpha=0.8)
        ax2.set_ylabel('バイオマス生産性 (kg/m²/day)', fontsize=12)
        ax2.set_title('バイオマス生産性比較', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars2, biomass_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=11)
        
        # 3. 必要栽培面積
        ax3 = axes[1, 0]
        area_values = [analysis_results['algae_area_per_person'], 
                      analysis_results['plant_area_per_person']]
        
        bars3 = ax3.bar(categories2, area_values, color=['#FF6B6B', '#FFEAA7'], 
                       edgecolor='black', alpha=0.8)
        ax3.set_ylabel('必要栽培面積 (m²/人)', fontsize=12)
        ax3.set_title('1人あたり必要栽培面積', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars3, area_values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{val:.1f} m²', ha='center', va='bottom', fontsize=11)
        
        # 4. 実測システム比較
        ax4 = axes[1, 1]
        systems = self.experimental_data['system'].tolist()
        efficiencies = self.experimental_data['efficiency'].tolist()
        colors4 = ['red' if t == '藻類' else 'green' if t == '高等植物' else 'blue' 
                  for t in self.experimental_data['type'].tolist()]
        
        bars4 = ax4.bar(range(len(systems)), efficiencies, color=colors4, 
                       edgecolor='black', alpha=0.7)
        ax4.set_xticks(range(len(systems)))
        ax4.set_xticklabels(systems, rotation=45, ha='right')
        ax4.set_ylabel('効率', fontsize=12)
        ax4.set_title('実測閉鎖生態系システム', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 凡例
        import matplotlib.patches as mpatches
        legend_elements = [
            mpatches.Patch(color='red', alpha=0.7, label='藻類システム'),
            mpatches.Patch(color='green', alpha=0.7, label='高等植物システム'),
            mpatches.Patch(color='blue', alpha=0.7, label='混合システム')
        ]
        ax4.legend(handles=legend_elements, loc='upper right')
        
        plt.suptitle('BIO-103: 閉鎖生態系光合成効率 総合分析', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
    
    def plot_3d_optimization(self):
        """3D最適化曲面のプロット"""
        # 光強度、CO2濃度、温度の最適化曲面
        from mpl_toolkits.mplot3d import Axes3D
        
        # パラメータ範囲
        PFD_range = np.linspace(100, 1000, 20)  # μmol/m²/s
        CO2_range = np.linspace(400, 5000, 20)  # ppm
        PFD_grid, CO2_grid = np.meshgrid(PFD_range, CO2_range)
        
        # 簡易モデル: 効率 = f(PFD, CO2)
        # Michaelis-Menten型モデル
        def efficiency_model(PFD, CO2):
            K_light = 300  # 光飽和定数
            K_CO2 = 1500   # CO2飽和定数
            eff_max = 0.03  # 最大効率
            
            light_response = PFD / (K_light + PFD)
            CO2_response = CO2 / (K_CO2 + CO2)
            
            return eff_max * light_response * CO2_response
        
        efficiency_grid = efficiency_model(PFD_grid, CO2_grid)
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(PFD_grid, CO2_grid, efficiency_grid, 
                              cmap='viridis', alpha=0.8, edgecolor='none')
        
        ax.set_xlabel('光量子束密度 (μmol/m²/s)', fontsize=11, labelpad=10)
        ax.set_ylabel('CO2濃度 (ppm)', fontsize=11, labelpad=10)
        ax.set_zlabel('光合成効率', fontsize=11, labelpad=10)
        ax.set_title('BIO-103: 光合成効率の最適化曲面', fontsize=14, fontweight='bold')
        
        # 最適点のマーキング
        max_idx = np.unravel_index(np.argmax(efficiency_grid), efficiency_grid.shape)
        ax.scatter(PFD_grid[max_idx], CO2_grid[max_idx], efficiency_grid[max_idx], 
                  color='red', s=100, label='最適点')
        
        ax.legend()
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='効率')
        
        plt.tight_layout()
        plt.show()
        
        print(f"\n最適条件:")
        print(f"  光量子束密度: {PFD_grid[max_idx]:.0f} μmol/m²/s")
        print(f"  CO2濃度: {CO2_grid[max_idx]:.0f} ppm")
        print(f"  最大効率: {efficiency_grid[max_idx]:.4f} ({efficiency_grid[max_idx]*100:.2f}%)")
    
    def calculate_system_scaling(self, crew_size=4, mission_duration=365):
        """システムスケーリング計算"""
        print("\n" + "="*60)
        print(f"システムスケーリング計算 (乗員: {crew_size}人, 期間: {mission_duration}日)")
        print("="*60)
        
        # 基本要件
        daily_calories_per_person = 2000  # kcal
        daily_O2_per_person = 0.84  # kg (人間の消費量)
        daily_water_per_person = 2.0  # L (飲料水)
        
        total_calories = daily_calories_per_person * crew_size * mission_duration
        total_O2 = daily_O2_per_person * crew_size * mission_duration
        total_water = daily_water_per_person * crew_size * mission_duration
        
        # 藻類システム
        algae_biomass = self.maxima_results.get('algae_biomass_kg_m2_day', 0.035)
        algae_O2 = self.maxima_results.get('algae_O2_g_m2_day', 42.0) / 1000  # kg/m²/day
        
        biomass_calorie_density = 4000  # kcal/kg
        required_biomass = total_calories / biomass_calorie_density  # kg
        
        # 必要面積
        algae_area_biomass = required_biomass / (algae_biomass * mission_duration)
        algae_area_O2 = total_O2 / (algae_O2 * mission_duration)
        algae_area = max(algae_area_biomass, algae_area_O2)
        
        # 植物システム
        plant_biomass = self.maxima_results.get('plant_biomass_kg_m2_day', 0.022)
        plant_O2 = self.maxima_results.get('plant_O2_g_m2_day', 22.0) / 1000  # kg/m²/day
        
        plant_area_biomass = required_biomass / (plant_biomass * mission_duration)
        plant_area_O2 = total_O2 / (plant_O2 * mission_duration)
        plant_area = max(plant_area_biomass, plant_area_O2)
        
        # 混合システム（藻類:植物 = 1:2）
        mixed_area_biomass = required_biomass / (
            (algae_biomass * 0.33 + plant_biomass * 0.67) * mission_duration
        )
        mixed_area_O2 = total_O2 / (
            (algae_O2 * 0.33 + plant_O2 * 0.67) * mission_duration
        )
        mixed_area = max(mixed_area_biomass, mixed_area_O2)
        
        print(f"\n1. 基本要件:")
        print("-"*40)
        print(f"  総カロリー必要量: {total_calories/1000:.0f} Mcal")
        print(f"  総酸素必要量: {total_O2:.0f} kg")
        print(f"  総水必要量: {total_water:.0f} L")
        
        print(f"\n2. 必要栽培面積:")
        print("-"*40)
        print(f"  藻類システム: {algae_area:.1f} m²")
        print(f"     (バイオマス基準: {algae_area_biomass:.1f} m²)")
        print(f"     (酸素基準: {algae_area_O2:.1f} m²)")
        
        print(f"\n  高等植物システム: {plant_area:.1f} m²")
        print(f"     (バイオマス基準: {plant_area_biomass:.1f} m²)")
        print(f"     (酸素基準: {plant_area_O2:.1f} m²)")
        
        print(f"\n  混合システム (藻類1:植物2): {mixed_area:.1f} m²")
        print(f"     (バイオマス基準: {mixed_area_biomass:.1f} m²)")
        print(f"     (酸素基準: {mixed_area_O2:.1f} m²)")
        
        print(f"\n3. 容積推定 (高さ2m):")
        print("-"*40)
        print(f"  藻類システム: {algae_area * 2:.1f} m³")
        print(f"  高等植物システム: {plant_area * 2:.1f} m³")
        print(f"  混合システム: {mixed_area * 2:.1f} m³")
        
        # エネルギー要件
        lighting_power = 200  # W/m² (LED照明)
        system_power = 50     # W/m² (冷却、ポンプ等)
        
        algae_power = algae_area * (lighting_power + system_power) / 1000  # kW
        plant_power = plant_area * (lighting_power + system_power) / 1000  # kW
        mixed_power = mixed_area * (lighting_power + system_power) / 1000  # kW
        
        print(f"\n4. 電力要件:")
        print("-"*40)
        print(f"  藻類システム: {algae_power:.1f} kW")
        print(f"  高等植物システム: {plant_power:.1f} kW")
        print(f"  混合システム: {mixed_power:.1f} kW")
        
        return {
            'algae_area': algae_area,
            'plant_area': plant_area,
            'mixed_area': mixed_area,
            'algae_power': algae_power,
            'plant_power': plant_power,
            'mixed_power': mixed_power
        }
    
    def plot_system_scaling(self, scaling_results):
        """システムスケーリングの可視化"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 1. 必要面積比較
        ax1 = axes[0]
        systems = ['藻類', '高等植物', '混合']
        areas = [scaling_results['algae_area'], 
                scaling_results['plant_area'], 
                scaling_results['mixed_area']]
        
        bars1 = ax1.bar(systems, areas, color=['#4ECDC4', '#96CEB4', '#FFEAA7'], 
                       edgecolor='black', alpha=0.8)
        ax1.set_ylabel('必要栽培面積 (m²)', fontsize=12)
        ax1.set_title('4人乗組員の必要栽培面積', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        for bar, area in zip(bars1, areas):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{area:.0f} m²', ha='center', va='bottom')
        
        # 2. 電力要件
        ax2 = axes[1]
        powers = [scaling_results['algae_power'], 
                 scaling_results['plant_power'], 
                 scaling_results['mixed_power']]
        
        bars2 = ax2.bar(systems, powers, color=['#45B7D1', '#FF6B6B', '#FFD166'], 
                       edgecolor='black', alpha=0.8)
        ax2.set_ylabel('電力要件 (kW)', fontsize=12)
        ax2.set_title('システム電力要件', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, power in zip(bars2, powers):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{power:.1f} kW', ha='center', va='bottom')
        
        # 3. 乗組員数によるスケーリング
        ax3 = axes[2]
        crew_sizes = [1, 4, 10, 50]
        algae_areas_scaled = []
        plant_areas_scaled = []
        
        for crew in crew_sizes:
            # 簡易スケーリング（面積は乗組員数に比例）
            algae_scaled = scaling_results['algae_area'] * (crew / 4)
            plant_scaled = scaling_results['plant_area'] * (crew / 4)
            algae_areas_scaled.append(algae_scaled)
            plant_areas_scaled.append(plant_scaled)
        
        ax3.plot(crew_sizes, algae_areas_scaled, 'o-', linewidth=2, 
                markersize=8, label='藻類システム', color='#4ECDC4')
        ax3.plot(crew_sizes, plant_areas_scaled, 's-', linewidth=2, 
                markersize=8, label='高等植物システム', color='#96CEB4')
        
        ax3.set_xlabel('乗組員数 (人)', fontsize=12)
        ax3.set_ylabel('必要栽培面積 (m²)', fontsize=12)
        ax3.set_title('乗組員数によるスケーリング', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        plt.suptitle('BIO-103: 閉鎖生態系システム スケーリング分析', 
                    fontsize=16, fontweight='bold', y=1.05)
        plt.tight_layout()
        plt.show()
    
    def save_results(self, analysis_results, scaling_results):
        """結果を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        output = {
            'calculation_id': 'BIO-103',
            'timestamp': timestamp,
            'maxima_results': self.maxima_results,
            'analysis': analysis_results,
            'scaling': scaling_results,
            'experimental_data': self.experimental_data.to_dict('records'),
            'recommendations': {
                'optimal_system': '混合システム (藻類 + 高等植物)',
                'reason': 'バイオマス生産性と酸素生産のバランスが良い',
                'estimated_area_per_person': f"{scaling_results['mixed_area']/4:.1f} m²/人",
                'estimated_power_per_person': f"{scaling_results['mixed_power']/4:.1f} kW/人"
            }
        }
        
        filename = f'BIO103_results_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n結果を {filename} に保存しました")
        
        # テキストサマリーも作成
        summary_file = f'BIO103_summary_{timestamp}.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("BIO-103: 閉鎖生態系光合成効率 計算サマリー\n")
            f.write("="*60 + "\n\n")
            
            f.write("1. 主要結果:\n")
            f.write(f"   藻類システム効率: {analysis_results['algae_efficiency']:.4f} ({analysis_results['algae_efficiency']*100:.2f}%)\n")
            f.write(f"   高等植物システム効率: {analysis_results['plant_efficiency']:.4f} ({analysis_results['plant_efficiency']*100:.2f}%)\n")
            f.write(f"   効率比 (藻類/植物): {analysis_results['algae_efficiency']/analysis_results['plant_efficiency']:.2f}倍\n\n")
            
            f.write("2. バイオマス生産性:\n")
            f.write(f"   藻類: {analysis_results['algae_biomass']:.4f} kg/m²/day\n")
            f.write(f"   高等植物: {analysis_results['plant_biomass']:.4f} kg/m²/day\n")
            f.write(f"   生産性比: {analysis_results['algae_biomass']/analysis_results['plant_biomass']:.2f}倍\n\n")
            
            f.write("3. 4人乗組員ミッション (365日):\n")
            f.write(f"   藻類システム必要面積: {scaling_results['algae_area']:.1f} m²\n")
            f.write(f"   高等植物システム必要面積: {scaling_results['plant_area']:.1f} m²\n")
            f.write(f"   混合システム必要面積: {scaling_results['mixed_area']:.1f} m²\n")
            f.write(f"   推奨システム: {output['recommendations']['optimal_system']}\n")
            f.write(f"   1人あたり面積: {output['recommendations']['estimated_area_per_person']}\n")
            f.write(f"   1人あたり電力: {output['recommendations']['estimated_power_per_person']}\n\n")
            
            f.write("4. 考察:\n")
            f.write("   藻類システムは効率が高いが、食料としての多様性に欠ける\n")
            f.write("   高等植物システムは心理的効果が高いが、面積効率が低い\n")
            f.write("   混合システムが実用的なバランスを提供\n")
        
        print(f"サマリーを {summary_file} に保存しました")
        
        return filename, summary_file
    
    def run(self):
        """メイン実行"""
        print("="*60)
        print("BIO-103: 閉鎖生態系光合成効率 分析開始")
        print("="*60)
        
        # 1. Maxima結果を読み込み
        self.load_maxima_results()
        
        # 2. 効率比較分析
        analysis_results = self.analyze_efficiency_comparison()
        
        # 3. 比較グラフ
        print("\n可視化生成中...")
        self.plot_comparison_charts(analysis_results)
        
        # 4. 3D最適化曲面
        self.plot_3d_optimization()
        
        # 5. システムスケーリング計算
        scaling_results = self.calculate_system_scaling(crew_size=4, mission_duration=365)
        
        # 6. スケーリング可視化
        self.plot_system_scaling(scaling_results)
        
        # 7. 結果保存
        self.save_results(analysis_results, scaling_results)
        
        print("\n" + "="*60)
        print("BIO-103 分析完了")
        print("="*60)

# メイン実行
if __name__ == "__main__":
    analyzer = Bio103Analyzer()
    analyzer.run()
