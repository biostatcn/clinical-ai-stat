---
title: "KM 生存曲线"
---

# KM 生存曲线

**用途**：Kaplan-Meier 生存曲线，展示两组或多组的时间-事件数据，附风险表 (risk table)。

## 交互式图表

<iframe src="../../assets/plots/km-curve.html" width="100%" height="520px" frameborder="0" style="border: none;"></iframe>

> 悬停查看各时间点的生存概率及置信区间。

## 生成代码

=== "R"

    ```r
    library(survival)
    library(survminer)
    library(plotly)
    
    # 拟合 KM
    fit <- survfit(Surv(avalu, event) ~ treatment, data = adtte)
    
    # 用 survminer 优雅展示
    g <- ggsurvplot(fit, data = adtte,
                    pval = TRUE, conf.int = TRUE,
                    risk.table = TRUE,
                    palette = c("#1f77b4", "#ff7f0e"),
                    xlab = "Time (months)", 
                    ylab = "Survival Probability",
                    legend.title = "Treatment")
    ```

=== "Python"

    ```python
    import plotly.graph_objects as go
    import numpy as np
    from lifelines import KaplanMeierFitter
    
    # 拟合两条 KM 曲线
    kmf_treat = KaplanMeierFitter()
    kmf_ctrl = KaplanMeierFitter()
    
    treat = adtte[adtte.treatment == "Drug"]
    ctrl = adtte[adtte.treatment == "Placebo"]
    
    kmf_treat.fit(treat.avalu, treat.event, label="Drug")
    kmf_ctrl.fit(ctrl.avalu, ctrl.event, label="Placebo")
    
    # 画图
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=kmf_treat.survival_function_.index,
        y=kmf_treat.survival_function_["Drug"],
        mode="lines", name="Drug",
        line=dict(color="#1f77b4", width=2)
    ))
    # ... 添加另一组
    
    fig.update_layout(
        title="Kaplan-Meier Survival Curve",
        xaxis_title="Time (months)",
        yaxis_title="Survival Probability",
        legend_title="Treatment"
    )
    fig.show()
    ```

=== "SAS"

    ```sas
    proc lifetest data=adtte plots=survival(atrisk=0 to 24 by 6);
        time avalu * event(0);
        strata treatment;
    run;
    ```

## 关键参数

- **置信区间**: `conf.int = TRUE`，显示 Greenwood 区间
- **p 值**: log-rank 检验结果
- **风险表**: at-risk table 是必要的辅助信息

## 参考方法

- [生存分析](../methods/04-survival-analysis.md)
