---
title: "Python 分析函数"
---

# Python 分析函数

## Table 1 — 基线特征表

```python
import pandas as pd
import numpy as np
from scipy import stats


def describe_continuous(data, var, group):
    """分组描述连续变量"""
    result = data.groupby(group)[var].agg([
        ("N", "count"),
        ("Mean", "mean"),
        ("SD", "std"),
        ("Median", "median"),
        ("Q1", lambda x: x.quantile(0.25)),
        ("Q3", lambda x: x.quantile(0.75)),
        ("Min", "min"),
        ("Max", "max")
    ]).round(2)

    # 组间比较（t 检验）
    groups = data[group].unique()
    if len(groups) == 2:
        g1 = data.loc[data[group] == groups[0], var].dropna()
        g2 = data.loc[data[group] == groups[1], var].dropna()
        stat, pval = stats.ttest_ind(g1, g2)
        result["p_value"] = f"{pval:.4f}"

    return result


def describe_categorical(data, var, group):
    """分组描述分类变量"""
    ct = pd.crosstab(data[group], data[var], margins=True)
    # 组间比较
    stat, pval, _, _ = stats.chi2_contingency(
        pd.crosstab(data[group], data[var])
    )
    return ct, pval


def table1(data, vars, cat_vars, group):
    """生成 Table 1"""
    results = []
    for var in vars:
        if var in cat_vars:
            desc, pval = describe_categorical(data, var, group)
            results.append(f"\n--- {var} (p={pval:.4f}) ---\n{desc}")
        else:
            desc = describe_continuous(data, var, group)
            results.append(f"\n--- {var} ---\n{desc}")
    return "\n".join(results)


# 使用示例
# t1 = table1(adsl,
#             vars=["age", "bmi", "sex", "race"],
#             cat_vars=["sex", "race"],
#             group="treatment")
# print(t1)
```

## MMRM 分析

```python
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm


def run_mmrm(data, formula="chg ~ C(treatment) * C(visit) + base"):
    """MMRM 分析"""
    model = mixedlm(
        formula,
        data=data,
        groups=data["subject"],
        re_formula="~1"
    )
    result = model.fit(method="reml")

    print(result.summary())
    return result


def extract_lsmeans(model, data, treatment="treatment", visit="visit"):
    """提取 LS Means（需手动计算）"""
    import pandas as pd
    # 获取各组边际均值
    pred_data = data[[treatment, visit, "base"]].drop_duplicates()
    pred = model.predict(pred_data)
    lsmeans = pred_data.copy()
    lsmeans["predicted"] = pred

    return lsmeans.groupby([treatment, visit])["predicted"].mean()
```

## 生存分析

```python
from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt


def fit_km(data, duration_col, event_col, group_col):
    """拟合 KM 曲线"""
    fig, ax = plt.subplots(figsize=(8, 6))

    for name, group in data.groupby(group_col):
        kmf = KaplanMeierFitter()
        kmf.fit(group[duration_col], group[event_col], label=name)
        kmf.plot_survival_function(ax=ax)

    plt.title("Kaplan-Meier Survival Curve")
    plt.xlabel("Time")
    plt.ylabel("Survival Probability")
    return fig


def fit_cox(data, duration_col, event_col, covariates):
    """拟合 Cox 回归"""
    cph = CoxPHFitter()
    cols = [duration_col, event_col] + covariates
    cph.fit(data[cols], duration_col=duration_col, event_col=event_col)
    cph.print_summary()
    return cph


def forest_plot_data(data, duration_col, event_col, subgroup_col):
    """准备森林图数据"""
    import pandas as pd
    from lifelines import CoxPHFitter

    results = []
    # Overall
    cph = CoxPHFitter()
    cph.fit(data[[duration_col, event_col, "treatment"]],
            duration_col=duration_col, event_col=event_col)
    hr = np.exp(cph.hazards_.iloc[0, 0])
    ci = np.exp(cph.confidence_intervals_.iloc[0].values)
    results.append({
        "Subgroup": "Overall",
        "HR": hr, "Lower": ci[0], "Upper": ci[1]
    })

    # 各亚组
    for subg in data[subgroup_col].unique():
        sub = data[data[subgroup_col] == subg]
        cph = CoxPHFitter()
        cph.fit(sub[[duration_col, event_col, "treatment"]],
                duration_col=duration_col, event_col=event_col)
        hr = np.exp(cph.hazards_.iloc[0, 0])
        ci = np.exp(cph.confidence_intervals_.iloc[0].values)
        results.append({
            "Subgroup": subg,
            "HR": hr, "Lower": ci[0], "Upper": ci[1]
        })

    return pd.DataFrame(results)
```

## 模型诊断

```python
import matplotlib.pyplot as plt
import scipy.stats as stats


def diagnose_linear_model(model, residuals):
    """线性模型诊断四合一图"""
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # 残差 vs 拟合值
    axes[0, 0].scatter(model.fittedvalues, residuals, alpha=0.5)
    axes[0, 0].axhline(y=0, color="r", linestyle="--")
    axes[0, 0].set_xlabel("Fitted Values")
    axes[0, 0].set_ylabel("Residuals")
    axes[0, 0].set_title("Residuals vs Fitted")

    # Q-Q 图
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title("Normal Q-Q")

    # Scale-Location 图
    std_res = residuals / residuals.std()
    axes[1, 0].scatter(model.fittedvalues, np.sqrt(np.abs(std_res)), alpha=0.5)
    axes[1, 0].set_xlabel("Fitted Values")
    axes[1, 0].set_ylabel("√|Standardized Residuals|")
    axes[1, 0].set_title("Scale-Location")

    # 残差直方图
    axes[1, 1].hist(residuals, bins=20, edgecolor="black", alpha=0.7)
    axes[1, 1].set_xlabel("Residuals")
    axes[1, 1].set_ylabel("Frequency")
    axes[1, 1].set_title("Residuals Distribution")

    plt.tight_layout()
    return fig
```
