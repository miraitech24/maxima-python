$\mathop{R}\left( t\mathop{,}m\mathop{,}eta\right) \mathop{:=}\]\[\mathop{exp}\]\[\left( \mathop{-}{{\left( \frac{t}{eta}\right) }^{m}}\right) $

MaximaのLaTeX出力が**汎用性よりも正確性を優先**しているためで、特に：

- カンマに `\mathop` を付ける癖

- 変数名の曖昧さ（`eta` をそのまま出力）

$R(t, m, \eta) := \exp\left(-\left(\frac{t}{\eta}\right)^{m}\right)$

$\mathop{f}\left( t\mathop{,}m\mathop{,}eta\right) \mathop{:=}\frac{m}{eta} {{\left( \frac{t}{eta}\right) }^{m\mathop{-}1}} \mathop{R}\left( t\mathop{,}m\mathop{,}eta\right) $
