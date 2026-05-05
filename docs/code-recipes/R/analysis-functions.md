---
title: "R 分析函数"
---

# R 分析函数

## Table 1 — 基线特征表

```r
library(tableone)

# 定义变量
vars <- c("age", "sex", "race", "bmi", "systolic_bp", "diastolic_bp",
          "prior_med", "comorbidity")
cat_vars <- c("sex", "race", "prior_med", "comorbidity")

# 创建 Table 1
tab1 <- CreateTableOne(
  vars = vars,
  strata = "treatment",
  data = adsl,
  factorVars = cat_vars,
  test = TRUE,
  smd = TRUE,
  addOverall = TRUE
)

# 输出
print(tab1, 
      showAllLevels = TRUE,  # 分类变量显示所有水平
      smd = TRUE,            # 标准化均值差
      pvalue = TRUE)         # 组间比较 p 值

# 导出为 CSV
write.csv(print(tab1, showAllLevels = TRUE, smd = TRUE, pvalue = TRUE),
          "output/table1.csv")
```

## LS Means 提取函数

```r
library(emmeans)
library(dplyr)

#' 从模型中提取 LS Means 和组间比较
#' @param model 拟合的模型对象
#' @param spec 比较规格，如 ~ treatment
#' @param by 分组变量，如 ~ visit
extract_lsmeans <- function(model, spec, by = NULL) {
  
  # LS Means
  emm <- emmeans(model, spec, by = by)
  
  # 组间比较
  pairs <- contrast(emm, "trt.vs.ctrl", ref = 1)
  
  # 格式化为数据框
  lsmeans_df <- as.data.frame(emm)
  contrast_df <- as.data.frame(pairs)
  
  list(
    lsmeans = lsmeans_df,
    contrast = contrast_df
  )
}

# 使用示例
# result <- extract_lsmeans(m1, ~ treatment | visit)
```

## MMRM 完整分析函数

```r
library(lme4)
library(lmerTest)
library(emmeans)

#' MMRM 分析 —— 重复测量混合效应模型
#' @param data 纵向数据框
#' @param formula 模型公式，默认 chg ~ treatment * visit + base + (1|subject)
run_mmrm <- function(data, 
                     formula = chg ~ treatment * visit + base + (1 | subject)) {
  
  # 拟合模型
  model <- lmer(formula, data = data)
  
  # 方差分析（含 KR 自由度校正）
  anova_table <- anova(model, ddf = "Kenward-Roger")
  
  # LS Means
  lsmeans <- emmeans(model, ~ treatment | visit)
  
  # 组间比较
  contrasts <- contrast(lsmeans, "trt.vs.ctrl", ref = 1)
  
  list(
    model = model,
    anova = anova_table,
    lsmeans = as.data.frame(lsmeans),
    contrast = as.data.frame(contrasts)
  )
}

# 使用
# result <- run_mmrm(adqs)
# result$contrast  # 查看治疗效应
```

## 森林图数据准备

```r
library(dplyr)
library(broom)

#' 亚组分析的 HR/OR 和 95% CI
#' @param data 数据框
#' @param time_var 生存时间变量（字符串）
#' @param event_var 事件变量（字符串）
#' @param subgroup_var 亚组变量（字符串）
forest_prep_survival <- function(data, time_var, event_var, subgroup_var) {
  
  subgroups <- unique(data[[subgroup_var]])
  
  results <- lapply(subgroups, function(subg) {
    sub_data <- data[data[[subgroup_var]] == subg, ]
    
    # Cox 回归
    formula <- as.formula(paste0("Surv(", time_var, ", ", event_var, 
                                 ") ~ treatment"))
    fit <- coxph(formula, data = sub_data)
    
    # 提取 HR 和 CI
    hr <- exp(coef(fit))
    ci <- exp(confint(fit))
    
    data.frame(
      Subgroup = subg,
      HR = hr,
      Lower = ci[1],
      Upper = ci[2],
      p_value = summary(fit)$coefficients[, "Pr(>|z|)"],
      N = nrow(sub_data)
    )
  }) |>
    bind_rows()
  
  # 添加 Overall
  fit_all <- coxph(as.formula(paste0("Surv(", time_var, ", ", event_var, 
                                     ") ~ treatment")), data = data)
  overall <- data.frame(
    Subgroup = "Overall",
    HR = exp(coef(fit_all)),
    Lower = exp(confint(fit_all))[1],
    Upper = exp(confint(fit_all))[2],
    p_value = summary(fit_all)$coefficients[, "Pr(>|z|)"],
    N = nrow(data)
  )
  
  bind_rows(overall, results)
}
```

## KM 曲线数据准备

```r
library(survival)

#' 准备 KM 生存表数据（含风险表信息）
#' @param fit survfit 对象
get_km_table <- function(fit) {
  
  # 提取生存概率和风险数
  summary_fit <- summary(fit)
  
  # 在特定时间点提取
  times <- c(0, 6, 12, 18, 24)
  
  result <- lapply(names(fit$strata), function(stratum) {
    idx <- which(summary_fit$strata == stratum)
    
    time_points <- times[times <= max(summary_fit$time[idx])]
    surv_at <- approx(summary_fit$time[idx], 
                      summary_fit$surv[idx], 
                      xout = time_points)$y
    
    data.frame(
      Stratum = stratum,
      Time = time_points,
      Survival = surv_at
    )
  }) |>
    bind_rows()
  
  result
}
```
