---

## 本日の課題：倒立振子の運動方程式の導出と数値計算

### 【背景】

一輪車やセグウェイのような「倒立振子（とうりつしんし）」の制御を考えます。手計算で運動方程式を立てるのはミスが起きやすいですが、wxMaximaを使えば正確に導出でき、Pythonでその挙動を可視化できます。

---

### ステップ1：wxMaximaによる数式処理

まずはwxMaximaを開き、ラグランジュ力学を用いて運動方程式を導出してください。

【問題1-1】

以下のラグランジアン $L$ をwxMaximaに入力し、$\theta$ に関する運動方程式を求めてください。

（カートは固定され、棒だけが回転する単純なモデルとします）

$L = \frac{1}{2}ml^2\dot{\theta}^2 - mgl\cos(\theta)$

- $m$: 棒の質量、 $l$: 重心までの長さ、 $g$: 重力加速度、 $\theta$: 鉛直下向きからの角度

- ヒント：`diff(L, 'diff(theta, t))` などを使ってラグランジュの運動方程式 $\frac{d}{dt}(\frac{\partial L}{\partial \dot{\theta}}) - \frac{\partial L}{\partial \theta} = 0$ を計算します。

【問題1-2】

導出した方程式を $\ddot{\theta} = \dots$ の形に整理（solve関数を使用）し、Pythonで使いやすい形式で表示させてください。

---

### ステップ2：Pythonによる数値シミュレーション

wxMaximaで得られた結果（ $\ddot{\theta} = -\frac{g}{l}\sin(\theta)$ になるはずです）をPythonにコピー＆ペーストして、シミュレーションを行います。

【問題2-1】

scipy.integrate.odeint または solve_ivp を用いて、初期角 $170^\circ$（ほぼ真上）から手を離した時の挙動をシミュレートするコードを書いてください。

**【条件】**

- $g = 9.8$, $l = 1.0$

- 初期状態：$[\theta, \dot{\theta}] = [170^\circ, 0]$

- 時間範囲：0秒〜10秒

---

### ステップ3：連成の自動化（高度な課題）

【問題3】

手動でコピペするのではなく、Pythonから直接Maximaを呼び出す（または計算済み数式をパースする）方法を検討してください。

> **ヒント:** Pythonの `sympy` ライブラリを使えばMaximaに近いことができますが、あえてMaximaを使う場合は、Maximaの出力を `fortran()` 関数などでコード形式で書き出し、それをPythonで読み込むという流れがプロの現場（大規模な航空宇宙計算など）では行われます。

---

## 期待されるアウトプット

1. **wxMaxima:** 運動方程式の最終的な出力画面

2. **Python:** 角度 $\theta$ が時間の経過とともに激しく振れる（または回転する）グラフ

![](/home/iwamura/snap/marktext/9/.config/marktext/images/2025-12-21-15-31-14-image.png)

![](/home/iwamura/snap/marktext/9/.config/marktext/images/2025-12-21-15-31-27-image.png)
