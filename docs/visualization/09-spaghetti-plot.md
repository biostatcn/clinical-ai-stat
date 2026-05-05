---
title: "个体轨迹图 (Spaghetti Plot)"
---

# 个体轨迹图 (Spaghetti Plot)

**用途**：展示纵向数据中每个受试者随时间的变化轨迹，叠加组均值趋势线。

## 交互式图表

<iframe src="../../assets/plots/spaghetti-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 浅色半透明线 = 个体轨迹，粗实线 = 组均值趋势。悬停查看具体数值。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    # 模拟数据
    set.seed(123)
    n_subj <- 30
    visits <- c(0, 4, 8, 12, 16, 20, 24)
    
    spag_data <- do.call(rbind, lapply(1:n_subj, function(i) {
      trt <- ifelse(i <= 15, "Drug", "Placebo")
      bl <- rnorm(1, 50, 10)
      slope <- ifelse(trt == "Drug", -2, -0.5)
      data.frame(
        Subject = paste0("S", i),
        Treatment = trt,
        Visit = visits,
        Value = bl + slope * visits + rnorm(length(visits), 0, 3)
      )
    }))
    
    # 个体轨迹
    fig <- plot_ly(spag_data, x = ~Visit, y = ~Value,
                   color = ~Treatment,
                   split = ~Subject,
                   type = "scatter", mode = "lines+markers",
                   opacity = 0.4, line = list(width = 0.5),
                   showlegend = FALSE)
    
    # 叠加组均值
    group_mean <- aggregate(Value ~ Treatment + Visit, spag_data, mean)
    fig <- fig |> add_trace(data = group_mean,
                            x = ~Visit, y = ~Value,
                            color = ~Treatment,
                            type = "scatter", mode = "lines+markers",
                            opacity = 1, line = list(width = 3),
                            name = ~Treatment)
    fig
    ```

=== "Python"

    ```python
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    np.random.seed(123)
    n_subj = 30
    visits = [0, 4, 8, 12, 16, 20, 24]
    
    rows = []
    for i in range(n_subj):
        trt = "Drug" if i < 15 else "Placebo"
        bl = np.random.normal(50, 10)
        slope = -2 if trt == "Drug" else -0.5
        for v in visits:
            rows.append({
                "Subject": f"S{i+1}", "Treatment": trt,
                "Visit": v, "Value": bl + slope*v + np.random.normal(0, 3)
            })
    spag_data = pd.DataFrame(rows)
    
    fig = px.line(spag_data, x="Visit", y="Value", 
                  color="Treatment", line_group="Subject",
                  opacity=0.3,
                  title="Spaghetti Plot — Individual Trajectories")
    
    # 叠加组均值
    means = spag_data.groupby(["Treatment", "Visit"])["Value"].mean().reset_index()
    fig.add_scatter(x=means[means.Treatment=="Drug"].Visit,
                    y=means[means.Treatment=="Drug"].Value,
                    mode="lines+markers", name="Drug (Mean)",
                    line=dict(width=4, color="blue"))
    fig.show()
    ```

## 参考方法

- [纵向数据分析](../methods/05-longitudinal.md)
- [混合效应模型 MMRM](../methods/03-mixed-model.md)
