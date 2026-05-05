---
title: "瀑布图 (Waterfall Plot)"
---

# 瀑布图 (Waterfall Plot)

**用途**：展示每个受试者靶病灶较基线的最佳变化百分比，常用于肿瘤学疗效评估。

## 交互式图表

<iframe src="../../assets/plots/waterfall-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 每个条形代表一位受试者，绿色虚线 = PR 阈值（-30%），红色虚线 = PD 阈值（+20%）。悬停查看具体变化值。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    wf_data <- data.frame(
      Subject = paste0("S", 1:40),
      PctChange = c(-100, -85, -72, -65, -60, -55, -50, -45, -40, -35,
                    -30, -28, -25, -22, -20, -18, -15, -12, -10, -8,
                    -5, -2, 0, 5, 8, 10, 12, 15, 18, 20,
                    22, 25, 28, 30, 35, 40, 50, 60, 75, 100)
    )
    
    wf_data$color <- ifelse(wf_data$PctChange <= -30, "#1f77b4",  # 缓解
                            ifelse(wf_data$PctChange <= 20, "#ff7f0e",  # 稳定
                                   "#d62728"))  # 进展
    
    fig <- plot_ly(wf_data, x = ~Subject, y = ~PctChange,
                   type = "bar", marker = list(color = ~color),
                   hovertemplate = "Subject: %{x}<br>Change: %{y:.1f}%<extra></extra>")
    
    fig <- fig %>% layout(
      title = "Waterfall Plot — Best Tumor Response",
      xaxis = list(title = "Subject", showticklabels = FALSE),
      yaxis = list(title = "Best Change from Baseline (%)"),
      shapes = list(
        list(type = "line", x0 = -1, x1 = 40, y0 = -30, y1 = -30,
             line = list(dash = "dash", color = "green")),
        list(type = "line", x0 = -1, x1 = 40, y0 = 20, y1 = 20,
             line = list(dash = "dash", color = "red"))
      )
    )
    fig
    ```

=== "Python"

    ```python
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    
    wf_data = pd.DataFrame({
        "Subject": [f"S{i}" for i in range(1, 41)],
        "PctChange": [-100,-85,-72,-65,-60,-55,-50,-45,-40,-35,
                      -30,-28,-25,-22,-20,-18,-15,-12,-10,-8,
                      -5,-2,0,5,8,10,12,15,18,20,
                      22,25,28,30,35,40,50,60,75,100]
    })
    
    colors = ["#1f77b4" if x <= -30 else "#ff7f0e" if x <= 20 else "#d62728" 
              for x in wf_data["PctChange"]]
    
    fig = go.Figure(data=go.Bar(
        x=wf_data["Subject"], y=wf_data["PctChange"],
        marker_color=colors,
        hovertemplate="Subject: %{x}<br>Change: %{y:.1f}%<extra></extra>"
    ))
    
    fig.add_hline(y=-30, line_dash="dash", line_color="green")
    fig.add_hline(y=20, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title="Waterfall Plot — Best Tumor Response",
        xaxis_showticklabels=False,
        yaxis_title="Best Change from Baseline (%)"
    )
    fig.show()
    ```

## 关键参数

- **y = -30%**: 客观缓解（RECIST 1.1 PR 阈值）
- **y = 20%**: 疾病进展（RECIST 1.1 PD 阈值）

## AI Prompt 模板

```
请用 Plotly 生成瀑布图，展示受试者靶病灶最佳变化百分比。
数据包含 subject_id 和 pct_change 两列。
按变化从小到大排序，在 -30% 和 20% 处画参考线。
<-30% 蓝色（缓解），-30%~20% 橙色（稳定），>20% 红色（进展）。
```

## 参考方法

- [描述性统计](../methods/00-descriptive-stat.md)
- [假设检验](../methods/01-hypothesis-test.md)
