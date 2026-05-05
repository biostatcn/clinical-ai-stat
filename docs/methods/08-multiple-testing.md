---
title: "多重比较校正"
---

# 多重比较校正

## 方法简介

在临床试验中，多个终点、多个亚组或多个中期分析会导致多重比较问题。不校正会增加 I 类错误率。

## 常用校正方法

| 方法 | 控制指标 | 适用场景 |
|------|---------|---------|
| Bonferroni | FWER | 保守，适用于少量比较 |
| Holm | FWER | 比 Bonferroni 更优（逐步递减） |
| Hochberg | FWER | 比 Holm 更优（需正相关） |
| Benjamini-Hochberg | FDR | 探索性分析、生物标志物 |
| Graphical approach | FWER | 复杂多重性结构（门控策略） |

## 代码实现

=== "R"

    ```r
    # Bonferroni
    p.adjust(p_values, method = "bonferroni")
    
    # Holm
    p.adjust(p_values, method = "holm")
    
    # BH (FDR)
    p.adjust(p_values, method = "BH")
    
    # 图形法多重比较
    library(gMCP)
    graph <- matrix(c(0, 1, 1, 0), nrow = 2)
    weights <- c(0.5, 0.5)
    gMCP::gMCP(graph, pvalues = c(0.02, 0.03), weights = weights)
    ```

=== "Python"

    ```python
    from statsmodels.stats.multitest import multipletests
    
    # 多种校正方法
    reject, p_corrected, _, _ = multipletests(
        p_values, 
        method='fdr_bh'  # 'bonferroni', 'holm', 'fdr_bh'
    )
    
    # 结果
    pd.DataFrame({
        'raw_p': p_values,
        'corrected': p_corrected,
        'reject': reject
    })
    ```

=== "SAS"

    ```sas
    * 在 PROC MIXED 中用 ADJUST 选项;
    proc mixed data=adqs;
        class treatment visit;
        model chg = treatment visit treatment*visit;
        lsmeans treatment*visit / slice=visit diff adjust=bon;
    run;
    ```

## 关键概念

- **FWER** (Family-Wise Error Rate)：至少一次假阳性概率
- **FDR** (False Discovery Rate)：假阳性在 rejected 中的比例
- **图形法**：FDA 在复杂多重性场景下的推荐方法

## 相关可视化

- [火山图](../visualization/06-volcano-plot.md) — FDR 校正后的差异筛选
