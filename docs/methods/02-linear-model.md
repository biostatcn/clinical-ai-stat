---
title: "线性模型 / ANCOVA"
---

# 线性模型 / ANCOVA

## 方法简介

协方差分析 (ANCOVA) 是临床试验分析最常用的方法之一，通过纳入基线协变量来提高检验效能和控制混杂。

## 代码实现

=== "R"

    ```r
    # ANCOVA
    lm_model <- lm(chg ~ treatment + baseline + strata, data = adqs)
    summary(lm_model)
    
    # 最小二乘均值 (LS Means)
    library(emmeans)
    emmeans(lm_model, ~ treatment)
    ```

=== "Python"

    ```python
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    
    model = ols('chg ~ C(treatment) + baseline + C(strata)', data=df).fit()
    print(model.summary())
    ```

=== "SAS"

    ```sas
    proc mixed data=adqs;
        class treatment strata;
        model chg = treatment baseline strata / solution;
        lsmeans treatment / diff;
    run;
    ```

## 注意事项

- 基线协变量应预先指定在 SAP 中
- 主要分析应基于 mITT 人群

## 相关可视化

- [交互作用图](../visualization/10-interaction-plot.md)
- [箱线图 / 小提琴图](../visualization/03-boxplot-violin.md)
