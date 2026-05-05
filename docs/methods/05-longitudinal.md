---
title: "纵向数据分析"
---

# 纵向数据分析

## 方法简介

纵向数据分析方法包括 GEE 和随机效应模型，用于处理同一受试者的重复测量数据。

## 代码实现

=== "R"

    ```r
    library(geepack)
    
    # GEE
    gee_fit <- geeglm(chg ~ treatment + visit + treatment*visit + baseline,
                      id = subject, data = adqs,
                      family = gaussian, corstr = "unstructured")
    summary(gee_fit)
    ```

=== "SAS"

    ```sas
    proc genmod data=adqs;
        class subject treatment visit;
        model chg = treatment visit treatment*visit baseline / dist=normal;
        repeated subject=subject / type=un;
    run;
    ```

## 相关可视化

- [个体轨迹图](../visualization/09-spaghetti-plot.md)
