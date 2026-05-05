---
title: "交互作用图 (Interaction Plot)"
---

# 交互作用图 (Interaction Plot)

**用途**：展示治疗与协变量（或两个因子）之间的交互效应，用于亚组分析和交互效应探索。

## 交互式图表

<iframe src="../../assets/plots/interaction-plot.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 不平行的线提示存在交互效应。Drug 在低 Biomarker 组效果更明显。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    # 模拟交互数据
    interact_data <- expand.grid(
      Treatment = c("Drug", "Placebo"),
      Biomarker = c("Low", "Medium", "High")
    )
    interact_data$Endpoint <- c(12, 10, 8, 10, 10, 10)  # 交互模式
    
    fig <- plot_ly(interact_data, x = ~Biomarker, y = ~Endpoint,
                   color = ~Treatment, type = "scatter",
                   mode = "lines+markers",
                   line = list(width = 3),
                   marker = list(size = 10)) |>
      layout(
        title = "Treatment × Biomarker Interaction",
        yaxis = list(title = "Mean Endpoint"),
        xaxis = list(title = "Biomarker Level")
      )
    fig
    ```

=== "Python"

    ```python
    import plotly.express as px
    import pandas as pd
    
    interact_data = pd.DataFrame({
        "Treatment": ["Drug", "Drug", "Drug", "Placebo", "Placebo", "Placebo"],
        "Biomarker": ["Low", "Medium", "High"] * 2,
        "Endpoint": [12, 10, 8, 10, 10, 10]
    })
    
    fig = px.line(interact_data, x="Biomarker", y="Endpoint",
                  color="Treatment", markers=True,
                  title="Treatment × Biomarker Interaction")
    fig.show()
    ```

## 解读

- **平行线** → 无交互
- **交叉线** → 存在交互，提示 treatment effect 依赖于协变量水平

## AI Prompt 模板

```
生成交互作用图。数据包含 treatment (Drug/Placebo)、
biomarker_level (Low/Medium/High) 和 mean_endpoint。
x 轴为 biomarker_level，y 轴为 mean_endpoint， 
两条线分别代表 Drug 和 Placebo，显示点估计值。
```

## 参考方法

- [线性模型 / ANCOVA](../methods/02-linear-model.md)
