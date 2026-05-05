---
title: "Prompt 模板库"
---

# Prompt 模板库

## 通用模板框架

```
角色：你是一位经验丰富的临床试验统计师。
背景：[描述研究设计、数据类型、分析目标]
任务：[明确要求]
输出格式：[R代码 / 解释 / 报告段落]
约束：[样本量限制、软件版本、公司标准]
```

## 分类模板

### 统计分析类

??? example "MMRM 分析模板"

    ```
    请帮我编写 MMRM 分析的 R 代码。
    
    研究设计：随机、双盲、平行对照 III 期试验
    数据框：adqs
    变量：subject | treatment(Factor) | visit(Factor) | chg(连续) | baseline(连续)
    
    要求：
    1. 使用 lme4 或 nlme 包
    2. 固定效应：treatment, visit, treatment*visit, baseline
    3. 随机效应：随机截距 (subject)
    4. 自由度校正：Kenward-Roger
    5. 输出 treatment 组在各访视的 LS mean 和 95% CI
    ```

### 可视化类

??? example "森林图模板"

    ```
    请用 R plotly 生成一张森林图。
    数据框包含列：subgroup, hr, lower_ci, upper_ci, p_value
    x 轴为 HR (95% CI)，y 轴为 subgroup
    在 HR=1 处画虚线参考线
    右侧添加两列文本：HR (CI) 和 p 值
    ```

### 代码审查类

??? example "模型诊断模板"

    ```
    请审查以下 Cox 回归模型输出，检查：
    1. 比例风险假设是否满足
    2. 是否有 influential observations
    3. 模型拟合优度
    4. 建议下一步做什么诊断
    
    [粘贴模型输出]
    ```

## 使用原则

1. **具体胜过模糊** — 提供变量名、数据结构、期望输出
2. **分步提问** — 复杂分析分解为多轮对话
3. **要求验证** — 让 AI 检查假设条件
4. **指定风格** — 明确 R base / tidyverse / data.table
