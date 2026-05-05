---
title: "非参数方法"
---

# 非参数方法

## 方法简介

当数据不满足正态分布或方差齐性假设时，非参数检验是参数检验的稳健替代方法。临床试验中常用于 ordered categorical data、小样本或明显偏态分布的数据。

## 常用方法

| 场景 | 参数方法 | 非参数替代 |
|------|---------|-----------|
| 两组比较 | 两样本 t 检验 | Wilcoxon 秩和检验 (Mann-Whitney U) |
| 配对比较 | 配对 t 检验 | Wilcoxon 符号秩检验 |
| 多组比较 | ANOVA | Kruskal-Wallis 检验 |
| 相关性 | Pearson | Spearman 秩相关 |
| 分类数据 | 卡方检验 | Fisher 精确检验 |

## AI Prompt 模板

??? example "Prompt"

    ```
    我有两组非正态分布的连续数据（n=30/组），
    请用 Wilcoxon 秩和检验比较组间差异，
    计算中位数和 IQR 作为描述统计，
    同时报告效应量 (r = Z/√N)。
    ```

## 代码实现

=== "R"

    ```r
    # Wilcoxon 秩和检验
    wilcox.test(endpoint ~ treatment, data = data, exact = FALSE)
    
    # Kruskal-Wallis 检验
    kruskal.test(endpoint ~ group, data = data)
    
    # Spearman 相关
    cor.test(x, y, method = "spearman")
    
    # Fisher 精确检验
    fisher.test(table(data$treatment, data$response))
    
    # 效应量 r
    library(rstatix)
    wilcox_effectsize(data, endpoint ~ treatment)
    ```

=== "Python"

    ```python
    from scipy import stats
    
    # Wilcoxon 秩和检验
    stat, p = stats.mannwhitneyu(
        df[df.treatment=='Drug'].endpoint,
        df[df.treatment=='Placebo'].endpoint
    )
    
    # Kruskal-Wallis
    stat, p = stats.kruskal(df[df.group=='A'].endpoint,
                             df[df.group=='B'].endpoint,
                             df[df.group=='C'].endpoint)
    
    # Spearman 相关
    rho, p = stats.spearmanr(x, y)
    
    # Fisher 精确检验
    odds, p = stats.fisher_exact(pd.crosstab(df.treatment, df.response))
    ```

=== "SAS"

    ```sas
    proc npar1way data=adqs wilcoxon;
        class treatment;
        var endpoint;
    run;
    
    proc corr data=adqs spearman;
        var var1 var2;
    run;
    ```

## 相关可视化

- [箱线图 / 小提琴图](../visualization/03-boxplot-violin.md)
