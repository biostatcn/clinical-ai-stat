---
title: "R 数据清洗"
---

# R 数据清洗

## 缺失值处理

```r
library(dplyr)

# 查看缺失值概况
sapply(adqs, function(x) sum(is.na(x)))

# 删除指定列的缺失行
adqs_clean <- adqs |> filter(!is.na(aval))

# 用 LOCF 填充缺失（纵向数据常用）
library(tidyr)
adqs <- adqs |>
  group_by(subject) |>
  fill(aval, .direction = "down")

# 用中位数填补连续变量
adqs <- adqs |>
  mutate(aval = if_else(is.na(aval), median(aval, na.rm = TRUE), aval))
```

## 变量重编码

```r
library(dplyr)
library(forcats)

# 创建分类变量
adqs <- adqs |>
  mutate(
    # 二值化
    response = if_else(aval >= 30, "Responder", "Non-responder"),
    
    # 分组
    age_group = case_when(
      age < 45 ~ "< 45",
      age < 65 ~ "45-64",
      TRUE ~ "≥ 65"
    ),
    
    # 因子化并指定顺序
    age_group = factor(age_group, levels = c("< 45", "45-64", "≥ 65")),
    
    # BMI 分类
    bmi_group = case_when(
      bmi < 18.5 ~ "Underweight",
      bmi < 25   ~ "Normal",
      bmi < 30   ~ "Overweight",
      TRUE       ~ "Obese"
    )
  )
```

## 衍生变量生成

```r
library(dplyr)

# 临床试验常用衍生变量
adqs <- adqs |>
  mutate(
    # 较基线变化
    chg = aval - base,
    
    # 百分比变化
    pchg = (aval - base) / base * 100,
    
    # 访视编号（数字型）
    visit_num = case_when(
      visit == "Baseline"  ~ 0,
      visit == "Week 4"    ~ 4,
      visit == "Week 8"    ~ 8,
      visit == "Week 12"   ~ 12,
      visit == "Week 24"   ~ 24
    ),
    
    # 对数转换
    log_aval = log(aval),
    
    # 是否改善
    improved = if_else(chg < 0, "Yes", "No")
  )
```

## 数据集合并

```r
library(dplyr)

# 纵向数据 + 受试者基线特征
adqs_merged <- adqs |>
  left_join(adsl |> select(subject, age, sex, race, bmi), 
            by = "subject")

# 合并多个数据框
adsl <- adsl |> 
  left_join(adqs_summary, by = "subject") |>
  left_join(adtte_summary, by = "subject")
```

## ADaM 数据准备

```r
library(dplyr)

adqs_adam <- adqs |>
  # 筛选分析人群
  filter(ittfl == "Y") |>
  
  # 衍生分析变量
  mutate(
    # 按基线定义分析值
    aval = chg,                     
    # 基线作为协变量
    base = base,
    # 分析访视
    avisit = factor(visit, 
                    levels = c("Baseline", "Week 4", "Week 8", "Week 12", "Week 24")),
    # 治疗组编码
    trt01p = factor(treatment, 
                    levels = c("Placebo", "Drug"),
                    labels = c("Placebo", "X Dose"))
  ) |>
  
  # 按主题和访视排序
  arrange(subject, avisit)
```
