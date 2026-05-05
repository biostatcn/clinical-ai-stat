---
title: "统计方法"
---

# 统计方法

临床试验中常用统计方法的 AI 辅助实现，涵盖从描述统计到复杂模型的完整链条。

## 方法列表

<div class="card-grid">
<div class="card">
<h3><a href="00-descriptive-stat/">描述性统计</a></h3>
<p>均值、中位数、标准差、频数表、基线特征表 (Table 1)</p>
</div>
<div class="card">
<h3><a href="01-hypothesis-test/">假设检验</a></h3>
<p>t 检验、卡方检验、Fisher 精确检验、Wilcoxon 秩和检验</p>
</div>
<div class="card">
<h3><a href="02-linear-model/">线性模型 / ANCOVA</a></h3>
<p>方差分析、协方差分析、ANCOVA 的 AI 实现</p>
</div>
<div class="card">
<h3><a href="03-mixed-model/">混合效应模型 MMRM</a></h3>
<p>重复测量混合效应模型，临床试验金标准分析方法</p>
</div>
<div class="card">
<h3><a href="04-survival-analysis/">生存分析</a></h3>
<p>Kaplan-Meier 估计、Cox 比例风险模型、log-rank 检验</p>
</div>
<div class="card">
<h3><a href="05-longitudinal/">纵向数据分析</a></h3>
<p>GEE、随机效应模型、增长曲线模型</p>
</div>
<div class="card">
<h3><a href="06-missing-data/">缺失数据处理</a></h3>
<p>MAR/MNAR 假设、多重插补、LOCF、混合模型综合策略</p>
</div>
<div class="card">
<h3><a href="07-nonparametric/">非参数方法</a></h3>
<p>非参数检验、置换检验、bootstrapping</p>
</div>
<div class="card">
<h3><a href="08-multiple-testing/">多重比较校正</a></h3>
<p>Bonferroni、Holm、FDR 控制、图形法多重比较</p>
</div>
<div class="card">
<h3><a href="09-sample-size/">样本量计算</a></h3>
<p>优效性/非劣效性/等效性设计的样本量估算</p>
</div>
</div>

---

## 方法页面模板

每篇方法文档包含以下内容：

- **方法简介**：何时使用、基本原理
- **AI Prompt**：向 AI 描述分析需求的最佳提问方式
- **代码实现**：R / Python / SAS 三种语言
- **输出解读**：如何理解 AI 生成的分析结果
- **注意事项**：常见陷阱和 regulatory 考量
- **相关可视化**：链接到对应的图表页面
