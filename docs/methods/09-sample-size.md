---
title: "样本量计算"
---

# 样本量计算

## 方法简介

样本量估算是临床试验设计的核心环节，直接影响试验的检验效能和可行性。

## 常用设计类型

| 设计 | 检验假设 | 关键参数 |
|------|---------|---------|
| 优效性 | H0: Δ ≤ 0 | 效应量 δ, α, β |
| 非劣效性 | H0: Δ ≤ -margin | margin, α, β |
| 等效性 | H0: \|Δ\| ≥ margin | margin, α, β |

## 代码实现

=== "R"

    ```r
    # 两样本均值比较（优效性）
    power.t.test(
      delta = 5,           # 组间差异
      sd = 10,             # 标准差
      sig.level = 0.05,    # α
      power = 0.90,        # 1-β
      type = "two.sample",
      alternative = "two.sided"
    )
    
    # 两样本率比较
    power.prop.test(
      p1 = 0.6,
      p2 = 0.4,
      sig.level = 0.05,
      power = 0.80
    )
    
    # 生存分析样本量
    library(survival)
    power_ct <- powerSurvEpi(
      n = NULL,
      time = 24,
      event = 0.8,
      hr = 0.7,
      alpha = 0.05,
      power = 0.90
    )
    ```

=== "Python"

    ```python
    from statsmodels.stats.power import TTestIndPower, NormalIndPower
    
    # 两样本 t 检验
    power = TTestIndPower()
    n = power.solve_power(
        effect_size=0.5,   # Cohen's d
        alpha=0.05,
        power=0.90,
        alternative='two-sided'
    )
    print(f"每组所需样本量: {n:.0f}")
    
    # 率的比较
    from statsmodels.stats.proportion import proportion_effectsize
    es = proportion_effectsize(0.6, 0.4)
    n = NormalIndPower().solve_power(es, power=0.80, alpha=0.05)
    ```

=== "SAS"

    ```sas
    proc power;
        twosamplemeans
            groupmeans = 10 | 15
            stddev = 10
            power = 0.90
            alpha = 0.05
            npergroup = .;
    run;
    
    proc power;
        twosamplefreq
            groupproportions = (0.6 0.4)
            power = 0.80
            alpha = 0.05
            npergroup = .;
    run;
    ```

## 关键参数

- **效应量**：临床 meaningful difference，非统计学最小可检测差异
- **α**：通常双边 0.05
- **β**：通常 0.10-0.20（power 80-90%）
- **脱落率**：需在计算样本量基础上调整：N_adj = N / (1 - dropout_rate)

## 相关可视化

- [森林图](../visualization/01-forest-plot.md)（样本量估算结果展示）
- [交互作用图](../visualization/10-interaction-plot.md)（亚组样本量考量）
