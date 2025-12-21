# Maxima & Python Coupling Project: Projectile Motion

このプロジェクトは、数式処理ソフト **wxMaxima** で物理的な解析解を導出し、そのデータを **Python** でアニメーション化する「連成（Coupling）」のデモンストレーションです。

## 1. 物理モデル (Theoretical Model)

速度に比例する空気抵抗（$F = -bv$）を受ける物体の放物運動を扱います。

### 運動方程式 (Equations of Motion)

$m \frac{d^2x}{dt^2} = -b \frac{dx}{dt}$
$m \frac{d^2y}{dt^2} = -mg - b \frac{dy}{dt}$

### 解析解 (Analytical Solutions)

wxMaximaの `desolve` 関数を用いて導出された解は以下の通りです：

- **水平方向 ($x$):**
  $x(t) = \frac{m v_0 \cos(\theta)}{b} \left( 1 - e^{-\frac{b}{m}t} \right)$
- **垂直方向 ($y$):**
  $y(t) = \frac{m}{b} \left( v_0 \sin(\theta) + \frac{mg}{b} \right) \left( 1 - e^{-\frac{b}{m}t} \right) - \frac{mgt}{b}$

---

## 2. wxMaxima スクリプト (`solver.wxmx`)

数値計算（ルンゲ＝クッタ法）を行い、CSVとして出力するためのコードです。

/* 運動方程式の数値解法 */
result: rk([v0*cos(th)*exp(-b*t/m), (v0*sin(th)+m*g/b)*exp(-b*t/m)-m*g/b], 
           [x, y], [0, 0], [t, 0, 5, 0.05])$

/* CSV出力 (Pythonで読み込みやすい形式) */
output_file: "trajectory.csv"$
s: openw(output_file)$
for row in result do (
    printf(s, "~f, ~f, ~f~%", row[1], row[2], row[3])
)$
close(s)$

## 3. Python アニメーションスクリプト (`main_csv.py`)

出力された `trajectory.csv` を読み込み、アニメーションを表示・保存します。

## 4. 実行方法 (How to Use)

1. **wxMaxima** で `solver.wxmx` を実行し、`trajectory.csv` を生成します。

2. **Python** 環境で `main_csv.py` を実行します。

3. 同一ディレクトリ内に `motion.gif` が生成されます。

![](/home/iwamura/snap/marktext/9/.config/marktext/images/2025-12-21-15-19-32-image.png)
