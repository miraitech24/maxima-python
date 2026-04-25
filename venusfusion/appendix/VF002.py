#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:43:11 2026

@author: iwamura
"""

#!/usr/bin/env python3
"""
VF-002: 硫酸の液化・固定化の化学収支（SciPy完結版）
"""

import numpy as np
from scipy.optimize import fsolve, minimize
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd

class SulfuricAcidChemicalBalance:
    """硫酸の化学収支計算クラス"""
    
    def __init__(self):
        # 物理化学定数
        self.constants = {
            'R': 8.314,          # 気体定数 [J/(mol·K)]
            'T_venus': 737.0,    # 金星表面温度 [K]
            'P_venus': 9.3e6,    # 金星表面気圧 [Pa] (約92気圧)
            'H2SO4_mw': 98.08,   # 硫酸分子量 [g/mol]
            'H2O_mw': 18.02,     # 水分子量 [g/mol]
        }
        
        # 硫酸の熱力学特性
        self.h2so4_properties = {
            'melting_point': 283.36,    # 融点 [K] (10.31°C)
            'boiling_point': 610.0,     # 沸点 [K] (337°C) - 加圧下
            'heat_fusion': 10.71e3,     # 融解熱 [J/mol]
            'heat_vaporization': 50.0e3, # 蒸発熱 [J/mol]（概算）
            'cp_liquid': 138.0,         # 液体の定圧比熱 [J/(mol·K)]
            'cp_gas': 50.0,             # 気体の定圧比熱 [J/(mol·K)]
        }
    
    def calculate_phase_change(self, temperature, pressure):
        """
        硫酸の相変化条件を計算
        """
        # 気液平衡計算（簡易版）
        # Clausius-Clapeyron方程式: ln(P) = -ΔH_vap/R * (1/T) + C
        delta_h_vap = self.h2so4_properties['heat_vaporization']
        
        # 基準点（沸点での蒸気圧）
        T_boil = self.h2so4_properties['boiling_point']
        P_boil = 1.013e5  # 1 atm [Pa]
        
        # Clausius-Clapeyron方程式
        lnP_vapor = np.log(P_boil) - (delta_h_vap/self.constants['R']) * (1/temperature - 1/T_boil)
        P_vapor = np.exp(lnP_vapor)
        
        # 相の判定
        if temperature < self.h2so4_properties['melting_point']:
            phase = 'solid'
        elif pressure > P_vapor:
            phase = 'liquid'
        else:
            phase = 'gas'
        
        return phase, P_vapor
    
    def mass_balance(self, initial_mass, conversion_rate, time):
        """
        物質収支計算（反応速度論に基づく）
        
        Parameters:
        -----------
        initial_mass : float
            初期質量 [kg]
        conversion_rate : float
            反応速度定数 [1/s]
        time : array
            時間配列 [s]
            
        Returns:
        --------
        mass_remaining : array
            残存質量 [kg]
        converted_mass : array
            変換された質量 [kg]
        """
        # 一次反応速度式に従う
        mass_remaining = initial_mass * np.exp(-conversion_rate * time)
        converted_mass = initial_mass - mass_remaining
        
        return mass_remaining, converted_mass
    
    def energy_balance(self, mass_converted, temperature_change, phase_change=None):
        """
        エネルギー収支計算
        
        Parameters:
        -----------
        mass_converted : float
            変換された質量 [kg]
        temperature_change : float
            温度変化 [K]
        phase_change : str or None
            相変化の種類 ('fusion', 'vaporization', 'sublimation')
            
        Returns:
        --------
        total_energy : float
            必要な総エネルギー [J]
        heat_breakdown : dict
            各寄与の内訳
        """
        # モル数に変換
        moles = mass_converted * 1000 / self.constants['H2SO4_mw']  # [mol]
        
        # 顕熱（温度変化によるエネルギー）
        if temperature_change > 0:
            # 加熱（気体として計算）
            sensible_heat = moles * self.h2so4_properties['cp_gas'] * temperature_change
        else:
            # 冷却（液体として計算）
            sensible_heat = moles * self.h2so4_properties['cp_liquid'] * abs(temperature_change)
        
        # 潜熱（相変化によるエネルギー）
        latent_heat = 0
        if phase_change == 'fusion':
            latent_heat = moles * self.h2so4_properties['heat_fusion']
        elif phase_change == 'vaporization':
            latent_heat = moles * self.h2so4_properties['heat_vaporization']
        
        total_energy = sensible_heat + latent_heat
        
        heat_breakdown = {
            'sensible_heat': sensible_heat,
            'latent_heat': latent_heat,
            'total': total_energy,
            'energy_per_kg': total_energy / mass_converted  # [J/kg]
        }
        
        return total_energy, heat_breakdown
    
    def global_sulfuric_acid_calculation(self):
        """
        金星全体の硫酸計算
        """
        # 金星大気中の硫酸推定値
        venus_atmosphere = {
            'total_mass': 4.8e20,          # 大気総質量 [kg]
            'h2so4_fraction': 0.0001,      # 硫酸の質量分率（概算）
            'cloud_layer_mass': 1e16,      # 雲層の質量 [kg]
        }
        
        # 硫酸総量
        total_h2so4 = venus_atmosphere['total_mass'] * venus_atmosphere['h2so4_fraction']
        cloud_h2so4 = venus_atmosphere['cloud_layer_mass'] * 0.75  # 雲の75%が硫酸
        
        print(f"金星大気中の硫酸総量: {total_h2so4:.2e} kg")
        print(f"雲層中の硫酸量: {cloud_h2so4:.2e} kg")
        
        return total_h2so4, cloud_h2so4
    
    def simulate_liquefaction_process(self):
        """
        液化プロセスのシミュレーション
        """
        # シミュレーションパラメータ
        time = np.linspace(0, 1e7, 1000)  # 10^7秒（約115日）[s]
        initial_mass = 1e10  # 10^10 kg（初期質量）
        
        # 異なる反応速度定数でシミュレーション
        rate_constants = [1e-8, 1e-7, 1e-6]  # [1/s]
        
        results = {}
        for k in rate_constants:
            mass_rem, mass_conv = self.mass_balance(initial_mass, k, time)
            results[f'k={k:.1e}'] = {
                'time': time,
                'remaining': mass_rem,
                'converted': mass_conv,
                'rate_constant': k
            }
        
        return results
    
    def plot_results(self, results):
        """結果の可視化"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 質量変化の時間発展
        colors = ['blue', 'green', 'red']
        for (label, data), color in zip(results.items(), colors):
            axes[0, 0].plot(data['time']/86400, data['remaining']/1e9, 
                          color=color, linewidth=2, label=label)
        
        axes[0, 0].set_xlabel('Time (days)', fontsize=12)
        axes[0, 0].set_ylabel('Remaining Mass (×10⁹ kg)', fontsize=12)
        axes[0, 0].set_title('Sulfuric Acid Mass vs Time', fontsize=14)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 変換効率
        for (label, data), color in zip(results.items(), colors):
            efficiency = data['converted'] / (data['converted'][-1] + 1e-9) * 100
            axes[0, 1].plot(data['time']/86400, efficiency, 
                          color=color, linewidth=2, label=label)
        
        axes[0, 1].set_xlabel('Time (days)', fontsize=12)
        axes[0, 1].set_ylabel('Conversion Efficiency (%)', fontsize=12)
        axes[0, 1].set_title('Conversion Efficiency vs Time', fontsize=14)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. エネルギー要件の計算
        mass_samples = np.logspace(6, 12, 50)  # 1e6から1e12 kg
        energies = []
        
        for mass in mass_samples:
            energy, _ = self.energy_balance(mass, 100, 'fusion')
            energies.append(energy / 1e15)  # PetaJoules [PJ]
        
        axes[1, 0].loglog(mass_samples, energies, 'purple', linewidth=2)
        axes[1, 0].set_xlabel('Mass Converted (kg)', fontsize=12)
        axes[1, 0].set_ylabel('Energy Required (PJ)', fontsize=12)
        axes[1, 0].set_title('Energy vs Mass for Liquefaction', fontsize=14)
        axes[1, 0].grid(True, alpha=0.3, which='both')
        
        # 4. 相図（温度-圧力）
        temperatures = np.linspace(200, 800, 100)
        pressures = np.logspace(3, 8, 100)  # 10^3から10^8 Pa
        
        T_grid, P_grid = np.meshgrid(temperatures, pressures)
        phases = np.zeros_like(T_grid, dtype=int)
        
        for i in range(len(temperatures)):
            for j in range(len(pressures)):
                phase, _ = self.calculate_phase_change(temperatures[i], pressures[j])
                if phase == 'solid':
                    phases[j, i] = 0
                elif phase == 'liquid':
                    phases[j, i] = 1
                else:
                    phases[j, i] = 2
        
        contour = axes[1, 1].contourf(T_grid, np.log10(P_grid), phases, 
                                     levels=[-0.5, 0.5, 1.5, 2.5], 
                                     cmap='viridis', alpha=0.7)
        
        axes[1, 1].set_xlabel('Temperature (K)', fontsize=12)
        axes[1, 1].set_ylabel('log10(Pressure) [Pa]', fontsize=12)
        axes[1, 1].set_title('Phase Diagram of Sulfuric Acid', fontsize=14)
        
        # 金星条件をプロット
        axes[1, 1].scatter(self.constants['T_venus'], 
                          np.log10(self.constants['P_venus']), 
                          color='red', s=100, marker='*', 
                          label='Venus Surface')
        
        axes[1, 1].legend()
        
        plt.suptitle('VF-002: Sulfuric Acid Liquefaction & Fixation Analysis', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('VF002_sulfuric_acid_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_data(self, results):
        """データ保存"""
        # メインデータ
        data_frames = []
        for label, data in results.items():
            df = pd.DataFrame({
                'time_days': data['time']/86400,
                'remaining_mass_kg': data['remaining'],
                'converted_mass_kg': data['converted'],
                'conversion_efficiency_%': data['converted']/(data['converted'][-1] + 1e-9) * 100
            })
            df['rate_constant'] = data['rate_constant']
            data_frames.append(df)
        
        df_combined = pd.concat(data_frames, ignore_index=True)
        df_combined.to_csv('VF002_simulation_data.csv', index=False)
        
        # サマリー計算
        total_h2so4, cloud_h2so4 = self.global_sulfuric_acid_calculation()
        
        summary_data = {
            'parameter': [
                'Venus total H2SO4', 'Cloud layer H2SO4', 
                'Melting point', 'Boiling point',
                'Heat of fusion', 'Heat of vaporization'
            ],
            'value': [
                f'{total_h2so4:.2e} kg',
                f'{cloud_h2so4:.2e} kg',
                f'{self.h2so4_properties["melting_point"]} K',
                f'{self.h2so4_properties["boiling_point"]} K',
                f'{self.h2so4_properties["heat_fusion"]/1000:.1f} kJ/mol',
                f'{self.h2so4_properties["heat_vaporization"]/1000:.1f} kJ/mol'
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_csv('VF002_parameters_summary.csv', index=False)
        
        print("✅ Data saved to CSV files")
        return df_combined, df_summary
    
    def run_complete_analysis(self):
        """完全な分析を実行"""
        print("="*70)
        print("VF-002: Sulfuric Acid Chemical Balance Analysis")
        print("="*70)
        
        # 1. 金星全体の硫酸量を計算
        print("\n1. Calculating global sulfuric acid inventory...")
        total_h2so4, cloud_h2so4 = self.global_sulfuric_acid_calculation()
        
        # 2. 液化プロセスをシミュレーション
        print("2. Simulating liquefaction process...")
        results = self.simulate_liquefaction_process()
        
        # 3. エネルギー要件を計算
        print("3. Calculating energy requirements...")
        energy_needed, breakdown = self.energy_balance(
            cloud_h2so4 * 0.1,  # 10%を変換
            50,                 # 50Kの温度変化
            'fusion'            # 固化
        )
        
        print(f"\n   Energy needed for 10% of cloud H2SO4:")
        print(f"   - Sensible heat: {breakdown['sensible_heat']/1e15:.2f} PJ")
        print(f"   - Latent heat: {breakdown['latent_heat']/1e15:.2f} PJ")
        print(f"   - Total: {breakdown['total']/1e15:.2f} PJ")
        print(f"   - Per kg: {breakdown['energy_per_kg']/1e6:.2f} MJ/kg")
        
        # 4. 結果を可視化
        print("\n4. Generating plots...")
        self.plot_results(results)
        
        # 5. データを保存
        print("\n5. Saving data...")
        df_data, df_summary = self.save_data(results)
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE!")
        print("="*70)
        
        print(f"\n📁 Generated files:")
        print("  - VF002_sulfuric_acid_analysis.png")
        print("  - VF002_simulation_data.csv")
        print("  - VF002_parameters_summary.csv")
        
        return df_data, df_summary

# ==================== 実行 ====================

if __name__ == "__main__":
    # インスタンス作成と実行
    analyzer = SulfuricAcidChemicalBalance()
    df_data, df_summary = analyzer.run_complete_analysis()
    
    # 追加の分析例
    print("\n🔍 Additional quick calculations:")
    
    # 相変化の計算例
    phase, vapor_pressure = analyzer.calculate_phase_change(300, 1e5)
    print(f"  At 300K, 1 bar: Phase = {phase}, Vapor pressure = {vapor_pressure:.2e} Pa")
    
    phase, vapor_pressure = analyzer.calculate_phase_change(500, 1e6)
    print(f"  At 500K, 10 bar: Phase = {phase}, Vapor pressure = {vapor_pressure:.2e} Pa")
