---
title: "R 数据导入"
---

# R 数据导入

## CSV

```r
library(readr)

# 标准导入
df <- read_csv("data/adqs.csv")

# 指定列类型
df <- read_csv("data/adqs.csv",
               col_types = cols(
                 subject = col_character(),
                 treatment = col_factor(),
                 visit = col_factor(),
                 aval = col_double(),
                 base = col_double()
               ))
```

## SAS (sas7bdat)

```r
library(haven)

# 单文件
adqs <- read_sas("data/adqs.sas7bdat")

# 保留 SAS 标签为列属性
adqs <- read_sas("data/adqs.sas7bdat", 
                 encoding = "utf-8")
```

## XPT (CDISC 标准)

```r
library(haven)

adsl <- read_xpt("data/adsl.xpt")
adtte <- read_xpt("data/adtte.xpt")
```

## Excel

```r
library(readxl)

# 指定 sheet
df <- read_excel("data/data.xlsx", sheet = "ADQS")
```

## 批量导入全部 SAS 数据集

```r
library(haven)
library(purrr)

files <- list.files("data/", pattern = "\\.sas7bdat$", full.names = TRUE)
names(files) <- tools::file_path_sans_ext(basename(files))

# 导入到命名列表
dfs <- map(files, read_sas)

# 或直接注入全局环境
list2env(dfs, envir = .GlobalEnv)
```

## 导入 CDISC 标准库 (3 件套)

```r
library(haven)

adsl <- read_xpt("data/adsl.xpt")   # 受试者水平
adqs <- read_xpt("data/adqs.xpt")   # 参数来源（问卷/评分）
adtte <- read_xpt("data/adtte.xpt") # 时间-事件数据
adlb <- read_xpt("data/adlb.xpt")   # 实验室检查
adae <- read_xpt("data/adae.xpt")   # 不良事件
```
