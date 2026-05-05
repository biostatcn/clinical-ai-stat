---
title: "生存分析"
---

# 生存分析

## 方法简介

Kaplan-Meier 生存曲线和 Cox 比例风险模型是时间-事件数据（OS、PFS、TTR 等）的标准分析方法。

## 代码实现

=== "R"

    ```r
    library(survival)
    library(survminer)
    
    # KM 估计
    km_fit <- survfit(Surv(avalu, event) ~ treatment, data = adtte)
    
    # Log-rank 检验
    survdiff(Surv(avalu, event) ~ treatment, data = adtte)
    
    # Cox 回归
    cox_fit <- coxph(Surv(avalu, event) ~ treatment + strata, data = adtte)
    summary(cox_fit)
    ```

=== "Python"

    ```python
    from lifelines import KaplanMeierFitter, CoxPHFitter
    
    # KM
    kmf = KaplanMeierFitter()
    kmf.fit(durations=adtte['avalu'], event_observed=adtte['event'])
    
    # Cox
    cph = CoxPHFitter()
    cph.fit(adtte[['avalu', 'event', 'treatment', 'strata']], 
            duration_col='avalu', event_col='event')
    cph.print_summary()
    ```

=== "SAS"

    ```sas
    proc lifetest data=adtte plots=survival;
        time avalu * event(0);
        strata treatment;
    run;
    
    proc phreg data=adtte;
        class treatment strata;
        model avalu * event(0) = treatment strata / risklimits;
        hazardratio treatment;
    run;
    ```

## 相关可视化

- [KM 生存曲线](../visualization/02-km-curve.md)
- [森林图](../visualization/01-forest-plot.md)

## 注意事项

- 比例风险假设检验 (Schoenfeld residuals)
- 非比例风险时的替代方法 (RMST, 加权 log-rank)
