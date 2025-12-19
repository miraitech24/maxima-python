---
title: レポートのタイトル
author: BEAN
fontsize: 11pt
header-includes:
- \lstset{numbers=left, frame=trlb, frameround=tttt, breaklines=true}
- \renewcommand{\lstlistingname}{Source Code}
---

# hoge

本文

## fuga

本文その2

今日のタスク

- 世界にこんにちは
- を標準出力へ.

```{.Cpp
#include <iostream>

int main() {

    std::cout << "Hello, World !!" << std::endl;

    return 0;

}
```

PIDの式とか
$u(t) = K_{p}e(t) + K_{i}\int_{0}^{t}e(\tau)d\tau + K_{d}\frac{de(t)}{dt}$^[ Wikipedia PID制御 より (https://ja.wikipedia.org/wiki/PID制御) ]

改ページしてみて

\newpage

## 図とか表とか

![私はサーバル!!](animal_serval.png){width=60mm}  
[いらすとや](https://www.irasutoya.com/2017/02/blog-post_455.html)から拝借したサーバル

| In     | Conv   | Out  |
|:------ |:------:| ----:|
| なか     | RD     | 猫    |
| さあさなあた | ULDDDD | 水素の音 |
| なたやさあ  | -L--L  | 夏野菜  |
| ????   | ????   | ライオン |

: 突然のクイズ!!\ 最下段を完成させろ

$\frac{\sqrt{\pi }\mathop{-}\mathop{gamma\_ incomplete}\left( \frac{1}{2}\mathop{,}{{x}^{2}}\right) }{\sqrt{\pi }}$

数式はmaxima LaTeXコピーで＄をタイプして＄＄の間に貼付け/[..../]の囲みをを消す

$\int_{}^{}x {{\% e}^{-{{x}^{2}}}}{\, dx}\mathop{=}\mathop{-}\left( \frac{{{\% e}^{-{{x}^{2}}}}}{2}\right) $

$\mathop{f}\left( x\mathop{,}y\right) \mathop{:=}{{x}^{2}}\mathop{-}{{y}^{2}}$

$\mathop{F}(s)\mathop{:=}{{2}^{s}} {{\pi }^{s\mathop{-}1}} \sin{\left( \frac{\pi  s}{2}\right) } \mathop{\Gamma }\left( 1\mathop{-}s\right)  \mathop{zeta}\left( 1\mathop{-}s\right) $

$\lim_{\to x\mathop{\backslash -\backslash >  }0}{\frac{x \log{\left( x\mathop{+}1\right) }}{1\mathop{-}\cos{(x)}}}\mathop{=}2$
