
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 結果ディレクトリ
results_dir = 'VF003_AutoCoupling_Results_20260321_132208'

# データ読み込み
exp_df = pd.read_csv(os.path.join(results_dir, 'exponential_results.csv'))
log_df = pd.read_csv(os.path.join(results_dir, 'logistic_results.csv'))
comp_df = pd.read_csv(os.path.join(results_dir, 'model_comparison.csv'))
thresh_df = pd.read_csv(os.path.join(results_dir, 'threshold_times.csv'))

# 可視化
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 風速比較
ax1 = axes[0, 0]
ax1.plot(exp_df['year'], exp_df['v_python_exponential'], 'b-', label='指数モデル', linewidth=2)
ax1.plot(log_df['year'], log_df['v_python_logistic'], 'r-', label='ロジスティックモデル', linewidth=2)
ax1.set_xlabel('時間 (年)')
ax1.set_ylabel('SR風速')
ax1.set_title('モデル比較: SR風速減衰')
ax1.grid(True, alpha=0.3)
ax1.legend()

# 2. 拠点数比較
ax2 = axes[0, 1]
ax2.plot(exp_df['year'], exp_df['n_exponential'], 'b-', label='指数モデル', linewidth=2)
ax2.plot(log_df['year'], log_df['n_logistic'], 'r-', label='ロジスティックモデル', linewidth=2)
ax2.set_xlabel('時間 (年)')
ax2.set_ylabel('拠点数')
ax2.set_title('拠点数増加モデル')
ax2.grid(True, alpha=0.3)
ax2.legend()

# 3. 差のプロット
ax3 = axes[1, 0]
ax3.plot(comp_df['year'], comp_df['diff_exp_log'], 'g-', linewidth=2)
ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
ax3.set_xlabel('時間 (年)')
ax3.set_ylabel('風速差 (指数 - ロジスティック)')
ax3.set_title('モデル間の差異')
ax3.grid(True, alpha=0.3)

# 4. 閾値到達時間
ax4 = axes[1, 1]
x = np.arange(len(thresh_df))
width = 0.35
ax4.bar(x - width/2, thresh_df['t_exponential'], width, label='指数モデル')
ax4.bar(x + width/2, thresh_df['t_logistic'], width, label='ロジスティックモデル')
ax4.set_xlabel('閾値')
ax4.set_ylabel('到達時間 (年)')
ax4.set_title('閾値到達時間比較')
ax4.set_xticks(x)
ax4.set_xticklabels(thresh_df['threshold'])
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('VF-003: 自動連成システム結果', fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'auto_coupling_results.png'), dpi=300, bbox_inches='tight')
plt.show()

print(f"可視化完了: {os.path.join(results_dir, 'auto_coupling_results.png')}")
