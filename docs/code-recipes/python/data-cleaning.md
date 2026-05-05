---
title: "Python 数据清洗"
---

# Python 数据清洗

## 缺失值处理

```python
import pandas as pd
import numpy as np

# 查看缺失值
df.isnull().sum()

# 删除缺失
df_clean = df.dropna(subset=["aval"])

# LOCF 填充（纵向数据）
df = df.groupby("subject").apply(lambda x: x.ffill())

# 用中位数填补
df["aval"] = df["aval"].fillna(df["aval"].median())

# 用各组中位数填补
df["aval"] = df.groupby("treatment")["aval"].transform(
    lambda x: x.fillna(x.median())
)
```

## 变量重编码

```python
# 创建二值终点
df["responder"] = np.where(df["aval"] >= 30, "Responder", "Non-responder")

# 年龄分组
def age_group(age):
    if age < 45:
        return "< 45"
    elif age < 65:
        return "45-64"
    else:
        return "≥ 65"

df["agegrp"] = df["age"].apply(age_group)

# BMI 分类
def bmi_group(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

df["bmigrp"] = df["bmi"].apply(bmi_group)

# 因子化并指定顺序
from pandas.api.types import CategoricalDtype

age_cat = CategoricalDtype(
    categories=["< 45", "45-64", "≥ 65"], ordered=True
)
df["agegrp"] = df["agegrp"].astype(age_cat)
```

## 衍生变量

```python
# 较基线变化
df["chg"] = df["aval"] - df["base"]

# 百分比变化
df["pchg"] = (df["aval"] - df["base"]) / df["base"] * 100

# 访视编号映射
visit_map = {
    "Baseline": 0, "Week 4": 4, "Week 8": 8,
    "Week 12": 12, "Week 24": 24
}
df["visit_num"] = df["visit"].map(visit_map)

# 对数转换
df["log_aval"] = np.log(df["aval"])
```

## 数据合并

```python
# 纵向 + 受试者基线
merged = adqs.merge(
    adsl[["subject", "age", "sex", "race", "bmi"]],
    on="subject", how="left"
)

# 合并多个数据集
adsl = adsl \
    .merge(adqs_summary, on="subject", how="left") \
    .merge(adtte_summary, on="subject", how="left")
```

## 数据透视

```python
# 宽格式转换（访视水平 → 列）
wide = adqs.pivot_table(
    index="subject",
    columns="visit",
    values="aval",
    aggfunc="first"
)

# 添加前缀
wide.columns = [f"aval_{col}" for col in wide.columns]
wide = wide.reset_index()
```

## 数据筛选

```python
# 筛选分析人群
adqs_adam = adqs \
    .query("ittfl == 'Y'") \
    .sort_values(["subject", "visit_num"]) \
    .reset_index(drop=True)
```
