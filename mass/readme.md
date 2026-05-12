# 質量-ばね-ダンパ系 シミュレーション結果

## パラメータ(params.yaml)

- 質量 $m = 1.0$ kg
- 減衰係数 $c = 0.2$ N·s/m
- ばね定数 $k = 10.0$ N/m
- 初期変位 $x_0 = 0.1$ m
- 初期速度 $v_0 = 0.0$ m/s

## 解析解

- 固有角振動数 $\omega_n = 3.1623$ rad/s
- 減衰比 $\zeta = 0.0316$

## 運動方程式

$ m\ddot{x} + c\dot{x} + kx = 0 $

## 実行形式

 Python → Maxima キック（内部処理）

#Maximaが生成するファイル　 analytic_core.py

<img width="1785" height="1478" alt="response" src="https://github.com/user-attachments/assets/a3693d4f-7a45-4f48-997c-5e465ff70e30" />

## 結果

- 最大誤差: 9.689702e-09 m
- 最終変位: 0.036340 m

## 考察

誤差が微小であり、数値積分が正しく行われている。
