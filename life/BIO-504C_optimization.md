# BIO-504C 資源配分最適化結果

## 問題設定

宇宙環境耐性遺伝子の発現率（放射線耐性 $P_{rad}$ と微小重力適応 $P_{micro}$）を資源配分 $x, y$ の関数としてモデル化し、総資源 $R$ の下で最大化する。

**目的関数**:
$
P(x, y) = \sqrt{x} + \sqrt{y}
$

**制約条件**:
$
x + y = R, \quad x \ge 0, \; y \ge 0
$

## ラグランジュ未定乗数法

ラグランジアン $L = \sqrt{x} + \sqrt{y} - \lambda (x + y - R)$ の停留条件より、

$$
\frac{\partial L}{\partial x} = \frac{1}{2\sqrt{x}} - \lambda = 0,
\quad
\frac{\partial L}{\partial y} = \frac{1}{2\sqrt{y}} - \lambda = 0,
\quad
\frac{\partial L}{\partial \lambda} = -(x + y - R) = 0
$$

## 最適配分

Sympy による解:
$
x = \frac{R}{2}, \quad
y = \frac{R}{2}
$

## 最大総耐性確率

$$
P_{\text{max}} = \sqrt{\frac{R}{2}} + \sqrt{\frac{R}{2}} = \sqrt{2R}
$$

## 考察

資源を放射線耐性と微小重力適応に均等配分するとき、全体の宇宙適応確率が最大となる。  
この結果は、各適応機構が資源投入に対して収穫逓減（平方根型）であることに由来する。  
実際の生物学的パラメータ（例えば異なる感度係数）が付与されれば、最適配分は偏る可能性がある。
