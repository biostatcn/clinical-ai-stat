---
title: "假设检验"
---

# 假设检验

## 方法简介

临床试验中常用的假设检验方法，包括参数检验和非参数检验。

## AI Prompt 模板

??? example "Prompt"

    ```
    我的两组数据分别是 treatment 和 control，样本量各 50。
    主要终点是连续变量 endpoint，请帮我：
    1. 做正态性检验（Shapiro-Wilk）
    2. 方差齐性检验（Levene test）
    3. 根据结果选择适当的检验方法
    4. 计算效应量 (Cohen's d)
    ```

## 代码实现

=== "R"

    ```r
    # 正态性检验
    shapiro.test(data$endpoint[data$group == "Treatment"])
    shapiro.test(data$endpoint[data$group == "Control"])
    
    # 方差齐性
    car::leveneTest(endpoint ~ group, data = data)
    
    # 两样本 t 检验
    t.test(endpoint ~ group, data = data, var.equal = TRUE)
    ```

=== "Python"

    ```python
    from scipy import stats
    
    # 正态性检验
    stat, p_treat = stats.shapiro(df[df.group=='Treatment'].endpoint)
    stat, p_ctrl = stats.shapiro(df[df.group=='Control'].endpoint)
    
    # 方差齐性
    stat, p_var = stats.levene(
        df[df.group=='Treatment'].endpoint,
        df[df.group=='Control'].endpoint
    )
    
    # 两样本 t 检验
    t_stat, p_val = stats.ttest_ind(
        df[df.group=='Treatment'].endpoint,
        df[df.group=='Control'].endpoint
    )
    ```

=== "SAS"

    ```sas
    proc ttest data=adqs;
        class group;
        var endpoint;
    run;
    ```

## 注意事项

- 临床试验中优先使用 **ANCOVA** 而非多次 t 检验
- 多重终点需控制 family-wise error rate

## 相关可视化

- [箱线图 / 小提琴图](../visualization/03-boxplot-violin.md)
- [火山图](../visualization/06-volcano-plot.md)（多重比较校正）
