---
title: "箱线图 / 小提琴图"
---

# 箱线图 / 小提琴图

**用途**：展示连续变量在分组间的分布特征，包括中位数、四分位数、异常值和分布形状。

## 交互式图表

<iframe src="../../assets/plots/boxplot-violin.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 小提琴图展示分布形态，内部箱线图显示中位数和四分位数，散点为各受试者数据。

## 生成代码

=== "R"

    ```r
    library(plotly)
    
    plot_ly(data, x = ~treatment, y = ~endpoint, type = "box",
            boxpoints = "all", jitter = 0.3,
            pointpos = -1.8, marker = list(size = 4),
            color = ~treatment,
            colors = c("#1f77b4", "#ff7f0e"))
    ```

=== "Python"

    ```python
    import plotly.express as px
    
    # 箱线图+散点
    fig = px.box(df, x="treatment", y="endpoint", 
                 color="treatment",
                 points="all",
                 title="Distribution of Endpoint by Treatment Group")
    fig.show()
    
    # 小提琴图
    fig = px.violin(df, x="treatment", y="endpoint",
                    color="treatment", box=True,
                    title="Violin Plot with Box Inside")
    fig.show()
    ```

## 参考方法

- [描述性统计](../methods/00-descriptive-stat.md)
