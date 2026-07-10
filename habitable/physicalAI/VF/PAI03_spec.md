# PAI-03: Self-replicating Factory

## 課題仕様

- ID: PAI-03
- 対象: Self-replicating Factory
- 物理的核心: Replication Time
- 計算式: $t = t_{\mathrm{rep}} \cdot \log_2(N)$
- 目標値: $t = 279\ \mathrm{years}$

## 実行方法

```bash
python3 PAI03.py
```

## 結論

- 複製時間 $t_{\mathrm{rep}} = 279.0$ years
- 279年で完了する世代数: 1 世代
- 279年後の工場数: 2 個
- 実際の所要時間: 279.0 years
- 工場数は世代数に対して指数関数的に増加
- 複製時間が短いほど、同じ期間でより多くの工場を生産可能
