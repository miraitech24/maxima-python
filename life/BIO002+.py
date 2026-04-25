#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:05:45 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-002 パート1: 銀河系居住可能性計算
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

# フォント設定
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.family'] = 'IPAexGothic'
except:
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'

class Bio002Part1:
    def __init__(self, P_micro=0.125):
        self.P_micro = P_micro
        self.setup_parameters()
        
    def setup_parameters(self):
        self.galaxy = {
            'radius_kpc': 15.0,
            'scale_height_kpc': 0.3,
            'total_stars': 2.0e11,
            'age_gyr': 10.0,
        }
        
    def calculate_galactic_habitability(self):
        print("銀河系居住可能性計算中...")
        r = np.linspace(0, self.galaxy['radius_kpc'], 100)
        z = np.linspace(-2, 2, 80)
        R, Z = np.meshgrid(r, z)
        
        star_density = np.exp(-R / 3.0) * np.exp(-np.abs(Z) / self.galaxy['scale_height_kpc'])
        metallicity = 0.02 * np.exp(-R / 5.0)
        supernova_risk = np.exp(-R / 4.0)
        
        habitability = (star_density * metallicity) / (1.0 + supernova_risk + 0.1)
        habitability = habitability / np.max(habitability)
        
        return {'R': R, 'Z': Z, 'habitability': habitability}
    
    def run(self):
        print("BIO-002 パート1 実行中...")
        data = self.calculate_galactic_habitability()
        
        # 可視化
        plt.figure(figsize=(10, 8))
        plt.contourf(data['R'], data['Z'], data['habitability'], levels=20, cmap='viridis')
        plt.colorbar(label='居住可能性')
        plt.xlabel('銀河中心距離 (kpc)')
        plt.ylabel('銀河面高度 (kpc)')
        plt.title('BIO-002: 銀河系居住可能性マップ')
        plt.grid(True, alpha=0.3)
        plt.show()
        
        return data

if __name__ == "__main__":
    calc = Bio002Part1(P_micro=0.125)
    result = calc.run()
    np.save('bio002_part1_result.npy', result)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-002 パート2: 生命確率計算
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# フォント設定
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.family'] = 'IPAexGothic'
except:
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'

class Bio002Part2:
    def __init__(self, P_micro=0.125):
        self.P_micro = P_micro
        self.models = {
            'optimistic': {'P_abiogenesis': 0.5, 'color': 'green'},
            'conservative': {'P_abiogenesis': 0.01, 'color': 'orange'},
            'pessimistic': {'P_abiogenesis': 1e-6, 'color': 'red'}
        }
    
    def load_part1_result(self):
        return np.load('bio002_part1_result.npy', allow_pickle=True).item()
    
    def calculate_life_probability(self, galactic_data):
        results = {}
        for model_id, model in self.models.items():
            P_base = self.P_micro * model['P_abiogenesis']
            P_spatial = P_base * galactic_data['habitability']
            P_avg = np.mean(P_spatial)
            
            results[model_id] = {
                'name': model_id,
                'P_spatial': P_spatial,
                'P_avg': P_avg,
                'color': model['color']
            }
            print(f"{model_id}: 平均確率 = {P_avg:.2e}")
        
        return results
    
    def visualize_results(self, galactic_data, life_results):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 居住可能性
        ax1 = axes[0, 0]
        ax1.contourf(galactic_data['R'], galactic_data['Z'], 
                    galactic_data['habitability'], cmap='viridis')
        ax1.set_title('居住可能性')
        
        # 各モデルの確率
        for idx, (model_id, data) in enumerate(life_results.items(), 1):
            ax = axes[idx // 2, idx % 2]
            P_log = np.log10(data['P_spatial'] + 1e-20)
            ax.contourf(galactic_data['R'], galactic_data['Z'], P_log, cmap='RdYlGn')
            ax.set_title(f'{model_id}: 生命確率')
        
        plt.tight_layout()
        plt.show()
    
    def run(self):
        print("BIO-002 パート2 実行中...")
        galactic_data = self.load_part1_result()
        life_results = self.calculate_life_probability(galactic_data)
        self.visualize_results(galactic_data, life_results)
        
        return life_results

if __name__ == "__main__":
    calc = Bio002Part2(P_micro=0.125)
    result = calc.run()
    np.save('bio002_part2_result.npy', result)
