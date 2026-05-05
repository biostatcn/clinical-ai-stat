---
title: "内容管理"
---

# 内容管理 (CMS)

<div class="card" style="text-align:center; padding:2rem; margin:1rem 0;">
  <h3>📝 打开内容管理器</h3>
  <p style="margin:1rem 0;">
    <a href="../admin/index.html" class="md-button md-button--primary" style="font-size:1.1em; padding:0.75rem 2rem;">
      进入 CMS 后台
    </a>
  </p>
  <p style="font-size:0.9em; color:var(--md-default-fg-color--light);">
    使用 GitHub Personal Access Token 登录，编辑内容后自动提交到仓库。
  </p>
</div>

## 使用说明

| 操作 | 说明 |
|------|------|
| **编辑内容** | 选择文件 → 编辑 Markdown → 点击"保存" |
| **保存后** | 自动创建 Git 提交到 GitHub，触发 Actions 部署 |
| **部署时间** | 约 1-2 分钟 |

## 首次使用配置

### 1. 创建 GitHub Personal Access Token

1. 打开 https://github.com/settings/tokens?type=beta
2. 点击 **"Generate new token"** → **"Fine-grained token"**
3. 填写：
   - **Token name**: `clinical-ai-stat-cms`
   - **Repository access**: 选择 **"Only select repositories"** → 选择 `biostatcn/clinical-ai-stat`
   - **Permissions** → **Contents** → 勾选 **"Read and write"**
4. 点击 **"Generate token"**
5. **复制生成的 token**（离开页面后就看不到了）

### 2. 登录 CMS

1. 打开 https://biostatcn.github.io/clinical-ai-stat/admin/
2. 粘贴刚才复制的 token
3. 点击 **"连接 GitHub"**

### 3. 开始编辑

登录后可以看到本站所有 markdown 文件列表，按模块分组。点击任意文件即可在浏览器中编辑。

## 注意事项

- Token 仅保存在你的浏览器本地存储中，不会发送到第三方服务器
- 如果 Token 泄露，可以在 GitHub 设置中随时撤销
- 编辑保存后会**自动创建 Git 提交**并触发 GitHub Actions 部署
- 可使用 `/cms/` 页面或首页的"⚙️ 内容管理"入口访问
