---
title: "CONSORT 流程图"
---

# CONSORT 流程图

**用途**：展示临床试验受试者筛选、随机分配、随访和数据分析各阶段的流程图，是论文发表和监管提交的必备内容。

## 实现方式

CONSORT 流程图推荐使用 **Mermaid**（Markdown 原生支持）或 draw.io 绘制。

=== "Mermaid"

    ```mermaid
    graph TD
        A["Assessed for eligibility (n=XXX)"] --> B["Excluded (n=XX)<br/>• Not meeting criteria (n=XX)<br/>• Declined (n=XX)<br/>• Other reasons (n=XX)"]
        A --> C["Randomized (n=XXX)"]
        C --> D["Allocated to Drug (n=XX)<br/>• Received (n=XX)<br/>• Not received (n=XX)"]
        C --> E["Allocated to Placebo (n=XX)<br/>• Received (n=XX)<br/>• Not received (n=XX)"]
        D --> F["Lost to follow-up (n=XX)<br/>Discontinued (n=XX)"]
        E --> G["Lost to follow-up (n=XX)<br/>Discontinued (n=XX)"]
        F --> H["Analyzed (n=XX)<br/>• Excluded (n=XX)"]
        G --> I["Analyzed (n=XX)<br/>• Excluded (n=XX)"]
    ```

=== "R"

    ```r
    library(DiagrammeR)
    
    grViz("
      digraph consort {
        graph [layout = dot, rankdir = TB]
        node [shape = rectangle, style = filled, fillcolor = LightBlue]
        
        'Assessed (n=XXX)' -> 'Randomized (n=XXX)'
        'Assessed (n=XXX)' -> 'Excluded (n=XX)'
        'Randomized (n=XXX)' -> 'Drug (n=XX)'
        'Randomized (n=XXX)' -> 'Placebo (n=XX)'
        'Drug (n=XX)' -> 'Analyzed Drug (n=XX)'
        'Placebo (n=XX)' -> 'Analyzed Placebo (n=XX)'
      }
    ")
    ```

## 关键要点

- 遵循 **CONSORT 2010** 指南标准格式
- 每个阶段需报告具体数字
- 包括筛选 → 随机 → 分配 → 随访 → 分析 五个阶段

## 参考方法

- [描述性统计](../methods/00-descriptive-stat.md)
