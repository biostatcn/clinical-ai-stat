---
title: "热图 (Heatmap)"
---

# 热图 (Heatmap)

**用途**：展示变量间相关性矩阵、基因表达谱、或受试者×指标的多维数据模式。

## 交互式图表

<iframe src="../../assets/plots/heatmap.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 红蓝发散色标表示相关系数正负，格内显示具体 r 值。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    # 模拟相关性矩阵
    corr_mat <- cor(mtcars)
    
    fig <- plot_ly(
      x = colnames(corr_mat), 
      y = rownames(corr_mat),
      z = corr_mat,
      type = "heatmap",
      colorscale = list(c(0, "#4575b4"), c(0.5, "white"), c(1, "#d73027")),
      zmid = 0,
      hovertemplate = "x: %{x}<br>y: %{y}<br>r: %{z:.2f}<extra></extra>"
    ) |> layout(
      title = "Correlation Heatmap",
      xaxis = list(title = ""),
      yaxis = list(title = "")
    )
    fig
    ```

=== "Python"

    ```python
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    # 模拟临床指标相关性
    np.random.seed(42)
    vars = ["Biomarker1", "Biomarker2", "Biomarker3", 
            "Age", "BMI", "BP_Sys"]
    n = len(vars)
    corr = np.random.uniform(-1, 1, (n, n))
    corr = (corr + corr.T) / 2
    np.fill_diagonal(corr, 1)
    
    fig = px.imshow(corr, x=vars, y=vars,
                    color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1,
                    title="Correlation Heatmap of Clinical Variables",
                    text_auto=".2f")
    fig.show()
    ```

## 参考方法

- [描述性统计](../methods/00-descriptive-stat.md)
- [缺失数据处理](../methods/06-missing-data.md)

## 关键参数

| 参数 | 说明 |
|------|------|
| `colorscale` | RdBu_r (红蓝发散) — 适合相关性 |
| `zmid=0` | 颜色中点设 0，正负对称 |
| `text_auto` | 格子内显示数值 |

## AI Prompt 模板

```
生成一张相关性热图，数据框为 [NxM] 的临床指标矩阵。
使用发散色标 (RdBu)，范围 -1 到 1，格内显示相关系数。
x 和 y 轴标签倾斜 45 度避免重叠。
```
