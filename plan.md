# Clinical AI Stat — 临床试验 AI 统计分析知识库

## 概述

个人知识库站点，记录使用 AI 进行临床试验统计分析的过程、代码、方法和经验，方便随时查阅调用。

- **目标用户**：临床试验统计师（自身）
- **部署方式**：GitHub Pages
- **技术栈**：MkDocs + Material for MkDocs 主题
- **编程语言**：R / SAS / Python 混合

---

## 信息架构

```
📁 clinical-ai-stat/
│
├── 📁 docs/
│   ├── index.md                          # 首页仪表盘
│   │
│   ├── 📁 methods/                       # ═══ 统计方法 ═══
│   │   ├── index.md                      # 方法学概览
│   │   ├── 00-descriptive-stat.md        # 描述性统计
│   │   ├── 01-hypothesis-test.md         # 假设检验（t检验、卡方等）
│   │   ├── 02-linear-model.md            # 线性模型 / ANCOVA
│   │   ├── 03-mixed-model.md             # 混合效应模型（MMRM）
│   │   ├── 04-survival-analysis.md       # 生存分析（KM, Cox）
│   │   ├── 05-longitudinal.md            # 纵向数据分析
│   │   ├── 06-missing-data.md            # 缺失数据处理
│   │   ├── 07-nonparametric.md           # 非参数方法
│   │   ├── 08-multiple-testing.md        # 多重比较校正
│   │   └── 09-sample-size.md             # 样本量计算
│   │
│   ├── 📁 visualization/                 # ═══ 可视化独立模块 ═══
│   │   ├── index.md                      # 交互式图库总览
│   │   ├── 01-forest-plot.md             # 森林图
│   │   ├── 02-km-curve.md                # KM 生存曲线
│   │   ├── 03-boxplot-violin.md          # 箱线图 / 小提琴图
│   │   ├── 04-swimmer-plot.md            # 泳道图（个体疗效轨迹）
│   │   ├── 05-waterfall-plot.md          # 瀑布图（肿瘤缓解深度）
│   │   ├── 06-volcano-plot.md            # 火山图
│   │   ├── 07-heatmap.md                 # 热图
│   │   ├── 08-consort-diagram.md         # CONSORT 流程图
│   │   ├── 09-spaghetti-plot.md          # 个体轨迹图（纵向数据）
│   │   └── 10-interaction-plot.md        # 交互作用图
│   │
│   ├── 📁 ai-workflows/                  # ═══ AI 工作流 ═══
│   │   ├── index.md                      # AI 工作流概览
│   │   ├── 00-prompt-library.md          # 常用 Prompt 模板库
│   │   ├── 01-analysis-pipeline.md       # AI 辅助分析完整流程
│   │   ├── 02-code-generation.md         # AI 生成代码的技巧与陷阱
│   │   ├── 03-result-interpret.md        # AI 辅助结果解读
│   │   ├── 04-report-writing.md          # AI 辅助报告撰写
│   │   └── 05-review-checklist.md        # AI 输出的审查清单
│   │
│   ├── 📁 code-recipes/                  # ═══ 代码配方 ═══
│   │   ├── index.md                      # 代码片段索引
│   │   ├── R/
│   │   │   ├── data-import.md
│   │   │   ├── data-cleaning.md
│   │   │   └── analysis-functions.md
│   │   ├── SAS/
│   │   │   ├── data-import.md
│   │   │   ├── data-cleaning.md
│   │   │   └── analysis-macros.md
│   │   └── python/
│   │       ├── data-import.md
│   │       ├── data-cleaning.md
│   │       └── analysis-functions.md
│   │
│   ├── 📁 report-templates/              # ═══ 模板 ═══
│   │   ├── index.md
│   │   ├── analysis-report.md            # 统计分析报告模板
│   │   ├── table-figure-spec.md          # 表格/图形规范
│   │   └── output-checklist.md           # 输出交付检查清单
│   │
│   └── 📁 references/                    # ═══ 参考资料 ═══
│       ├── index.md
│       ├── regulatory-guidance.md        # 监管指南要点（ICH E9, E6, FDA指南）
│       └── glossary.md                   # 术语表
│
├── docs/assets/
│   ├── images/                           # 静态图片资源
│   └── plots/                            # 预生成的交互式图表 HTML
│
├── mkdocs.yml                            # MkDocs 配置文件
├── requirements.txt                      # Python 依赖
├── scripts/
│   └── generate-example-plots.py         # 示例图表生成脚本
├── plan.md                               # 本设计文档
└── README.md                             # 项目说明
```

---

## 可视化模块设计

### 每篇可视化页面的内容结构

```
┌──────────────────────────────────────────────┐
│  # 图表名称                                   │
│  **用途**：在何种场景使用                      │
├──────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐    │
│  │  交互式图表（Plotly 嵌入）            │    │
│  │  - 悬停查看数据点                     │    │
│  │  - 缩放/平移                         │    │
│  │  - 图例筛选                          │    │
│  └──────────────────────────────────────┘    │
├──────────────────────────────────────────────┤
│  ## 生成代码                                  │
│  === "R"       === "Python"       === "SAS"  │
│  ──────────    ─────────────     ──────────   │
│  library(      import plotly     proc sgplot; │
│   plotly)       as go                         │
│                                               │
│  # 两行核心代码                                │
├──────────────────────────────────────────────┤
│  ## 关键参数说明                               │
│  ## AI Prompt 模板                            │
│  ## 参考文献 / 扩展阅读                        │
└──────────────────────────────────────────────┘
```

### 跨模块引用

- methods 中文章可通过链接引用对应的可视化页面
- visualization 页面也可反向链接到对应的方法学页面
- 实现"按方法可查 + 图库总览"双入口

---

## 技术栈

| 用途 | 工具 |
|------|------|
| 站点框架 | MkDocs |
| 主题样式 | Material for MkDocs (insiders) |
| 交互图表 | Plotly (R `plotly` / Python `plotly`) |
| 代码展示 | pymdownx.tabbed (多语言标签页) |
| 数学公式 | pymdownx.arithmatex (KaTeX) |
| 标签系统 | mkdocs-material Tags |
| 全文搜索 | Material 内置 + 中文分词 |
| 目录导航 | 嵌套导航 + 右侧锚点目录 |
| 明暗模式 | Material 内置切换 |
| CI/CD | GitHub Actions → GitHub Pages |

---

## 使用流程

1. **写内容**：在 `docs/` 下编写 Markdown 文件
2. **本地预览**：`mkdocs serve` 实时预览
3. **提交代码**：`git push` 到 GitHub
4. **自动部署**：GitHub Actions 自动构建并发布到 Pages
5. **在线访问**：`https://<username>.github.io/clinical-ai-stat/`

---

## 项目初始化步骤

1. [x] 编写本 plan.md
2. [ ] 创建项目目录结构
3. [ ] 配置 mkdocs.yml
4. [ ] 创建首页（仪表盘风格）
5. [ ] 创建方法学模块各页面
6. [ ] 创建可视化模块各页面（含交互图表）
7. [ ] 创建 AI 工作流模块各页面
8. [ ] 创建代码配方、模板、参考资料模块
9. [ ] 配置 GitHub Actions 部署
10. [ ] 生成示例交互图表
11. [ ] 安装依赖并验证构建
12. [ ] 初始化 Git 仓库
