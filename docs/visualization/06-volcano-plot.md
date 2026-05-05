---
title: "火山图 (Volcano Plot)"
---

# 火山图 (Volcano Plot)

**用途**：展示差异表达分析或生物标志物分析中 fold change 和 p 值的关系，快速识别统计显著且效应量大的特征。

## 交互式图表

<iframe src="../../assets/plots/volcano-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 红色 = 显著 (p<0.05 且 |log2FC|>1)，橙色 = 仅 FC 变化，蓝色 = 仅显著，灰色 = 无差异。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    # 模拟数据
    set.seed(123)
    volcano_data <- data.frame(
      log2FC = rnorm(1000, 0, 1.5),
      pval = runif(1000, 0, 1)
    )
    volcano_data$logp <- -log10(volcano_data$pval)
    volcano_data$sig <- ifelse(
      abs(volcano_data$log2FC) > 1 & volcano_data$pval < 0.05, "Significant",
      ifelse(abs(volcano_data$log2FC) > 1, "FC only",
             ifelse(volcano_data$pval < 0.05, "p only", "NS"))
    )
    
    fig <- plot_ly(volcano_data, 
                   x = ~log2FC, y = ~logp,
                   color = ~sig,
                   colors = c("Significant" = "#d62728", "FC only" = "#ff7f0e",
                              "p only" = "#1f77b4", "NS" = "gray"),
                   type = "scatter", mode = "markers",
                   alpha = 0.6, size = 2,
                   hovertemplate = "FC: %{x:.2f}<br>-log10(p): %{y:.2f}<extra></extra>") |>
      layout(
        title = "Volcano Plot",
        xaxis = list(title = "log2(Fold Change)"),
        yaxis = list(title = "-log10(p value)"),
        shapes = list(
          list(type = "line", x0 = -1, x1 = -1, y0 = 0, y1 = max(volcano_data$logp),
               line = list(dash = "dash", color = "gray")),
          list(type = "line", x0 = 1, x1 = 1, y0 = 0, y1 = max(volcano_data$logp),
               line = list(dash = "dash", color = "gray"))
        )
      )
    fig
    ```

=== "Python"

    ```python
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    np.random.seed(123)
    volcano_data = pd.DataFrame({
        "log2FC": np.random.normal(0, 1.5, 1000),
        "pval": np.random.uniform(0, 1, 1000)
    })
    volcano_data["logp"] = -np.log10(volcano_data["pval"])
    
    conditions = [
        (abs(volcano_data["log2FC"]) > 1) & (volcano_data["pval"] < 0.05),
        (abs(volcano_data["log2FC"]) > 1),
        (volcano_data["pval"] < 0.05)
    ]
    choices = ["Significant", "FC only", "p only"]
    volcano_data["sig"] = np.select(conditions, choices, default="NS")
    
    fig = px.scatter(volcano_data, x="log2FC", y="logp", color="sig",
                     color_discrete_map={
                         "Significant": "#d62728", "FC only": "#ff7f0e",
                         "p only": "#1f77b4", "NS": "gray"},
                     opacity=0.6,
                     title="Volcano Plot")
    fig.add_vline(x=-1, line_dash="dash", line_color="gray")
    fig.add_vline(x=1, line_dash="dash", line_color="gray")
    fig.show()
    ```

## 关键参数

- **x 轴**: log2(Fold Change)，通常阈值 = ±1 (即 ±2 倍变化)
- **y 轴**: -log10(p value)，通常阈值 = 1.3 (即 p < 0.05)

## 参考方法

- [多重比较校正](../methods/08-multiple-testing.md)
