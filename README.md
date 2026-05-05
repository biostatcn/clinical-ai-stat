# Clinical AI Stat

临床试验 AI 统计分析知识库 —— 记录使用 AI 进行临床试验统计分析的过程、代码、方法和经验。

## 站点内容

| 模块 | 内容 | 文档数 |
|------|------|--------|
| **统计方法** | 描述统计、假设检验、ANCOVA、MMRM、生存分析等 | 10 |
| **可视化图库** | 交互式 Plotly 图表（森林图、KM 曲线、泳道图等） | 10 |
| **AI 工作流** | Prompt 模板、分析流程、代码审查、报告撰写 | 6 |
| **代码配方** | R / SAS / Python 即用代码片段 | 9 |
| **模板** | CSR 报告模板、TLF 规范、检查清单 | 3 |
| **参考资料** | ICH E6/E9/E10/FDA 指南、术语表 | 2 |

## 快速开始

```bash
pip install -r requirements.txt
mkdocs serve -a localhost:8765
# 浏览器打开 http://localhost:8765
```

## 部署

```bash
# 推送到 GitHub 后 Actions 自动部署
git push
```

在线访问：`https://shinellm.github.io/clinical-ai-stat/`

## 项目结构

- `docs/` — Markdown 源文件
- `docs/methods/` — 统计方法
- `docs/visualization/` — 可视化图库（含交互式 Plotly 图表）
- `docs/ai-workflows/` — AI 辅助工作流
- `docs/code-recipes/` — 代码片段（R / SAS / Python）
- `docs/report-templates/` — 报告模板
- `docs/references/` — 参考资料
- `scripts/` — 工具脚本（示例图表生成）
- `mkdocs.yml` — 站点配置
