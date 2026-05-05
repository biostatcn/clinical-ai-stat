---
title: "泳道图 (Swimmer Plot)"
---

# 泳道图 (Swimmer Plot)

**用途**：展示每个受试者的治疗暴露时间、疗效响应状态和事件时间线，常用于肿瘤学临床试验。

## 交互式图表

<iframe src="../../assets/plots/swimmer-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 每个条形代表一位受试者，颜色表示最佳总体响应。悬停查看详情。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    swimmer_data <- data.frame(
      Subject = paste0("S", 1:20),
      Response = factor(c(rep("CR", 3), rep("PR", 5), rep("SD", 7), rep("PD", 5)),
                        levels = c("CR", "PR", "SD", "PD")),
      Start = rep(0, 20),
      Duration = c(24, 20, 18, 22, 19, 16, 15, 14, 13, 12, 
                   11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
    )
    
    colors_swim <- c("CR" = "#2ca02c", "PR" = "#1f77b4", 
                     "SD" = "#ff7f0e", "PD" = "#d62728")
    
    fig <- plot_ly(swimmer_data, 
                   x = ~Duration, y = ~reorder(Subject, Duration),
                   type = "bar", orientation = "h",
                   color = ~Response, colors = colors_swim,
                   marker = list(line = list(color = "white", width = 1)),
                   hovertemplate = "Subject: %{y}<br>Duration: %{x} months<br>Response: %{color}<extra></extra>")
    
    fig <- fig %>% layout(
      title = "Swimmer Plot — Individual Patient Response",
      xaxis = list(title = "Time on Treatment (months)"),
      yaxis = list(title = "", showticklabels = FALSE),
      barmode = "stack"
    )
    fig
    ```

=== "Python"

    ```python
    import plotly.express as px
    import pandas as pd
    
    swimmer_data = pd.DataFrame({
        "Subject": [f"S{i}" for i in range(1, 21)],
        "Response": ["CR"]*3 + ["PR"]*5 + ["SD"]*7 + ["PD"]*5,
        "Duration": [24,20,18,22,19,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2]
    })
    
    color_map = {"CR": "#2ca02c", "PR": "#1f77b4", 
                 "SD": "#ff7f0e", "PD": "#d62728"}
    
    fig = px.bar(swimmer_data, 
                 x="Duration", y="Subject",
                 color="Response", color_discrete_map=color_map,
                 orientation="h",
                 title="Swimmer Plot — Individual Patient Response")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.show()
    ```

## 关键参数

| 参数 | 说明 |
|------|------|
| `orientation="h"` | 水平条形图 |
| `barmode="stack"` | 堆叠显示不同阶段 |
| 颜色映射 | CR=绿, PR=蓝, SD=橙, PD=红 |

## AI Prompt 模板

```
生成一张泳道图 (swimmer plot)，展示每例受试者的治疗持续时间
和最佳总体响应 (BOR)。x 轴为治疗时长（月），y 轴为受试者 ID，
条形按响应类型着色：CR 绿色、PR 蓝色、SD 橙色、PD 红色。
```

## 参考方法

- [描述性统计](../methods/00-descriptive-stat.md)
