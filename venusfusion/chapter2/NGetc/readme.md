---
## 課題29：地球への水素カプセル射出軌道

### 1. 目的

地球近傍の宇宙空間から、特定の目標地点（大気圏界面：高度約120km）に向けて水素カプセルを射出する際、機体が燃え尽きたり宇宙へ跳ね返されたりしないための**射出速度 $v_0$ と再突入角 $\gamma_e$ の関係**を解析する。

### 2. 数理モデル

地球の重力定数を $\mu$、射出点半径を $r_0$、地球半径を $R_E$ とする。

エネルギー保存則と角運動量保存則より、軌道の離心率 $e$ を解析的に導出する。

$e = \sqrt{1 + \frac{2 \left( \frac{v_0^2}{2} - \frac{\mu}{r_0} \right) (r_0 v_0 \cos \gamma)^2}{\mu^2}}$

目標とする再突入半径 $r = R_E$ 到達時の突入角 $\gamma_e$ は以下の式で評価される。

$\gamma_e = \arctan \left( \frac{e \sin \phi_e}{1 + e \cos \phi_e} \right)$

ここで、$\phi_e = \arccos \left[ \frac{1}{e} \left( \frac{(r_0 v_0 \cos \gamma)^2}{\mu R_E} - 1 \right) \right]$ である。

### 3. 処理分担

- **Maxima**: 万有引力下の運動方程式に基づき、離心率 $e$ と比角運動量 $h$ の一般解を導出。基準条件（一意の解）での軌道図を作成し、地球との幾何学的関係を可視化する。

- **Python**: Maximaから式をインポートし、射出速度 $v_0$ を連続的に変化させるスイープ計算を実行。再突入角が安全圏（$-5.5^\circ$ 〜 $-7.5^\circ$）に収まる条件をグラフ化する。

### 4. 連携手法

- Maximaの `printf` 機能を用いて、タグを含まない純粋な `orbit_params.py` を生成。

- Python側で `import orbit_params` を行い、解析解をパラメータスタディに利用。

---

![Screenshot from 2026-01-14 11-07-20.png](/home/iwamura/ピクチャ/Screenshots/Screenshot%20from%202026-01-14%2011-07-20.png)

![task29-2026-01-14.png](/home/iwamura/ドキュメント/coupling/venusfusion/task29-2026-01-14.png)

---

---

### 変更点と明示事項

- **単位**: すべてSI単位系（距離: $m$, 速度: $m/s$, 角度: $deg/rad$）で統一しました。

- **凡例 (Key/Legend)**:
  
  - Maxima側では「Capsule Trajectory（カプセル軌道）」と「Earth Surface（地球表面）」を明示。
  
  - Python側では「Calculated Entry Angle（計算された突入角）」と「Safe Entry Corridor（安全な再突入廊下）」を明示。

- **視認性**: Pythonのグラフにグリッド線とターゲットとなる境界線（$-5.5^\circ, -7.5^\circ$）を追加し、工学的な判断をしやすくしました。
