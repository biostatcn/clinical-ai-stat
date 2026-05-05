---
title: "森林图 (Forest Plot)"
---

# 森林图 (Forest Plot)

**用途**：Meta 分析、亚组分析结果的 OR/HR/MD 及置信区间的可视化展示。

## 交互式图表

<iframe src="../../assets/plots/forest-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 悬停查看 HR 和 95% CI 数值，可缩放平移。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    # 示例数据
    forest_data <- data.frame(
      Subgroup = c("Overall", "Age < 65", "Age ≥ 65", "Male", "Female",
                   "Region Asia", "Region EU", "Region US"),
      HR = c(0.72, 0.68, 0.78, 0.74, 0.70, 0.71, 0.73, 0.69),
      Lower = c(0.58, 0.48, 0.55, 0.53, 0.50, 0.49, 0.51, 0.47),
      Upper = c(0.89, 0.96, 1.10, 1.03, 0.98, 1.02, 1.04, 1.01)
    )
    
    fig <- plot_ly(forest_data) |>
      add_trace(
        x = ~HR, y = ~Subgroup,
        type = "scatter", mode = "markers",
        error_x = list(
          type = "data",
          symmetric = FALSE,
          arrayminus = ~HR - Lower,
          array = ~Upper - HR,
          color = "#1f77b4"
        ),
        marker = list(size = 10, color = "#1f77b4"),
        hovertemplate = "HR: %{x:.2f}<br>(%{customdata[0]:.2f}, %{customdata[1]:.2f})<extra>%{y}</extra>",
        customdata = ~stack(Lower, Upper)
      ) |>
      layout(
        title = "Forest Plot — Subgroup Analysis",
        xaxis = list(title = "Hazard Ratio (95% CI)", zeroline = TRUE, zerolinecolor = "gray"),
        yaxis = list(title = "", categoryorder = "array", categoryarray = rev(forest_data$Subgroup)),
        shapes = list(
          list(type = "line", x0 = 1, x1 = 1, y0 = -1, y1 = length(unique(forest_data$Subgroup)),
               line = list(dash = "dash", color = "gray", width = 1))
        ),
        margin = list(l = 100)
      )
    
    fig
    ```

=== "Python"

    ```python
    import plotly.graph_objects as go
    import pandas as pd
    
    forest_data = pd.DataFrame({
        "Subgroup": ["Overall", "Age < 65", "Age ≥ 65", "Male", "Female",
                     "Region Asia", "Region EU", "Region US"],
        "HR": [0.72, 0.68, 0.78, 0.74, 0.70, 0.71, 0.73, 0.69],
        "Lower": [0.58, 0.48, 0.55, 0.53, 0.50, 0.49, 0.51, 0.47],
        "Upper": [0.89, 0.96, 1.10, 1.03, 0.98, 1.02, 1.04, 1.01],
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=forest_data["HR"],
        y=forest_data["Subgroup"],
        mode="markers+lines",
        marker=dict(size=10, color="#1f77b4"),
        error_x=dict(
            type="data",
            symmetric=False,
            arrayminus=forest_data["HR"] - forest_data["Lower"],
            array=forest_data["Upper"] - forest_data["HR"],
            color="#1f77b4"
        ),
        hovertemplate="HR: %{x:.2f}<br>(%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>%{y}<extra></extra>",
        customdata=forest_data[["Lower", "Upper"]]
    ))
    
    fig.add_vline(x=1, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="Forest Plot — Subgroup Analysis",
        xaxis_title="Hazard Ratio (95% CI)",
        yaxis=dict(categoryorder="array", categoryarray=forest_data["Subgroup"][::-1]),
        height=400,
        margin=dict(l=120)
    )
    
    fig.show()
    ```

=== "SAS"

    ```sas
    proc sgplot data=forest_data;
        highlow y=subgroup low=lower high=upper / 
            type=bar lineattrs=(color=navy) barwidth=0.2;
        scatter y=subgroup x=hr / 
            markerattrs=(symbol=squarefilled color=navy size=10);
        refline 1 / axis=x lineattrs=(pattern=dash color=gray);
        xaxis label="Hazard Ratio (95% CI)";
    run;
    ```

## 关键参数

| 参数 | 说明 |
|------|------|
| `error_x` | 置信区间范围 |
| `xref = 1` | 参考线位置 (OR/HR=1, MD=0) |
| `categoryorder` | 亚组排序（通常倒序） |

## AI Prompt 模板

```
请用 Plotly 生成一张森林图。数据为临床试验亚组分析的 HR 和 95% CI，
包含 Overall 和亚组变量。要求：HR 以 1 为参考线，亚组展示在 y 轴，
水平排列，右侧留出空间显示 HR 值和 p 值。
```

## 参考方法

- [假设检验](../methods/01-hypothesis-test.md)
- [生存分析](../methods/04-survival-analysis.md)
