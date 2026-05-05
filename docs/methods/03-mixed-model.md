---
title: "混合效应模型 MMRM"
---

# 混合效应模型 MMRM

## 方法简介

Mixed Model Repeated Measures (MMRM) 是验证性临床试验分析的金标准方法。它利用所有可用数据，在 MAR 假设下给出有效推断。

## 代码实现

=== "R"

    ```r
    library(lme4)
    library(lmerTest)
    
    m1 <- lmer(chg ~ treatment * visit + baseline + (1 | subject), 
               data = adqs)
    summary(m1)
    
    # ANCOVA-type tests
    anova(m1, ddf = "Kenward-Roger")
    ```

=== "SAS"

    ```sas
    proc mixed data=adqs;
        class subject treatment visit;
        model chg = treatment visit treatment*visit baseline / ddfm=kr;
        repeated visit / subject=subject type=un;
        lsmeans treatment*visit / slice=visit diff;
    run;
    ```

=== "Python"

    ```python
    import statsmodels.api as sm
    from statsmodels.formula.api import mixedlm
    
    model = mixedlm(
        "chg ~ C(treatment) * C(visit) + baseline",
        data=df,
        groups=df["subject"],
        re_formula="~1"
    )
    result = model.fit()
    print(result.summary())
    ```

## 关键参数

- **协方差结构**: UN (非结构化) — 金标准；CS (复合对称) — 简化假设
- **自由度校正**: Kenward-Roger (KR) 或 Satterthwaite
- **固定效应**: treatment, visit, treatment×visit, baseline

## 相关可视化

- [个体轨迹图](../visualization/09-spaghetti-plot.md)
- [交互作用图](../visualization/10-interaction-plot.md)
