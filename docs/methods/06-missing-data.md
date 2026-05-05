---
title: "缺失数据处理"
---

# 缺失数据处理

## 方法简介

临床试验中缺失数据不可避免。ICH E9 (R1) 和 FDA 指南强调需采用适当的处理方法。

## 处理策略

| 方法 | 假设 | 适用场景 |
|------|------|---------|
| MMRM | MAR | 连续主要终点（金标准） |
| 多重插补 (MI) | MAR | 敏感性分析 |
| 模式混合模型 (PMM) | MNAR | 敏感性分析 |
| LOCF | — | 不推荐（偏倚风险高） |

## 代码实现

=== "R"

    ```r
    library(mice)
    
    # 多重插补
    imp <- mice(adqs, m = 20, method = "pmm", seed = 12345)
    fits <- with(imp, lm(chg ~ treatment + baseline))
    pool(fits)
    ```

=== "SAS"

    ```sas
    proc mi data=adqs nimpute=20 seed=12345;
        mcmc chain=multiple;
        var chg treatment baseline;
    run;
    ```

## 相关可视化

- [热图](../visualization/07-heatmap.md)（缺失模式可视化）
