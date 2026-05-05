---
title: "描述性统计"
---

# 描述性统计

## 方法简介

描述性统计是临床试验分析的起点，用于 summarise 受试者基线特征、安全性数据和疗效指标的分布情况。

## AI Prompt 模板

??? example "生成 Table 1 的 Prompt"

    ```
    我有一项随机对照试验的数据，请帮我生成基线特征表 (Table 1)。
    
    数据框包含以下变量：
    - treatment: "Drug" / "Placebo"
    - age: 连续变量
    - sex: "Male" / "Female"  
    - bmi: 连续变量
    - systolic_bp: 连续变量
    - prior_med: "Yes" / "No"
    
    要求：
    1. 连续变量报告 均值±标准差 和中位数[Q1, Q3]
    2. 分类变量报告 n (%)
    3. 组间比较：连续变量用 t 检验或 Wilcoxon，分类变量用卡方检验或 Fisher
    4. 格式整齐，适合发表
    ```

## 代码实现

=== "R"

    ```r
    library(dplyr)
    library(tableone)
    
    # 创建 Table 1
    vars <- c("age", "sex", "bmi", "systolic_bp", "prior_med")
    cat_vars <- c("sex", "prior_med")
    
    tab1 <- CreateTableOne(
      vars = vars,
      strata = "treatment",
      data = data,
      factorVars = cat_vars,
      test = TRUE,
      smd = TRUE
    )
    
    print(tab1, showAllLevels = TRUE, smd = TRUE)
    ```

=== "Python"

    ```python
    import pandas as pd
    from scipy import stats
    
    def describe_by_group(df, group_col, continuous_vars, categorical_vars):
        """生成分组描述统计"""
        result = {}
        for group, subdf in df.groupby(group_col):
            desc = {}
            for var in continuous_vars:
                desc[var] = {
                    'mean': subdf[var].mean(),
                    'sd': subdf[var].std(),
                    'median': subdf[var].median(),
                    'q1': subdf[var].quantile(0.25),
                    'q3': subdf[var].quantile(0.75)
                }
            for var in categorical_vars:
                desc[var] = subdf[var].value_counts().to_dict()
            result[group] = desc
        return result
    ```

=== "SAS"

    ```sas
    proc means data=adtte mean std median q1 q3;
        class treatment;
        var age bmi systolic_bp;
    run;
    
    proc freq data=adtte;
        tables treatment * sex / chisq;
        tables treatment * prior_med / chisq;
    run;
    ```

## 输出解读

- **SMD (Standardized Mean Difference)** > 0.1 提示基线不均衡
- **p 值**仅作参考，基线检验不应作为筛选标准
- **ICH E9** 指出基线比较不应进行假设检验

## 相关可视化

- [箱线图 / 小提琴图](../visualization/03-boxplot-violin.md)
