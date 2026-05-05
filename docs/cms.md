---
title: "内容管理"
---

# 内容管理 (CMS)

<article class="md-content__inner md-typeset">
<p style="font-size:1.1em; color:var(--md-default-fg-color--light);">
  通过 Decap CMS 可视化编辑本站内容。
</p>

<div class="card" style="text-align:center; padding:2rem; margin:1rem 0;">
  <h3>📝 打开内容管理器</h3>
  <p style="margin:1rem 0;">
    <a href="../admin/index.html" class="md-button md-button--primary" style="font-size:1.1em; padding:0.75rem 2rem;">
      进入 CMS 后台
    </a>
  </p>
  <p style="font-size:0.9em; color:var(--md-default-fg-color--light);">
    ⚠️ 需要 GitHub 登录认证。仅在生产部署后可用。
  </p>
</div>

## 使用说明

| 操作 | 说明 |
|------|------|
| **编辑内容** | 选择对应模块 → 点击页面 → 编辑 → 保存 |
| **新建页面** | 点击"新建" → 填写标题和内容 → 保存为草稿 |
| **发布流程** | 草稿 → 审核 → 发布（自动提交到 GitHub） |
| **上传图片** | 编辑器中拖入图片，自动上传至 `assets/uploads/` |

## 注意事项

- 编辑保存后会**自动创建 Git 提交**到 GitHub 仓库
- 站点会在 GitHub Actions 中自动重新构建部署（约 1-2 分钟）
- 首次使用需要完成下方 **GitHub OAuth 配置**

## 首次使用配置

### 1. 创建 GitHub OAuth App

前往 GitHub → Settings → Developer settings → [OAuth Apps](https://github.com/settings/developers) → New OAuth App：

| 字段 | 值 |
|------|-----|
| Application name | `clinical-ai-stat-cms` |
| Homepage URL | `https://biostatcn.github.io/clinical-ai-stat/` |
| Authorization callback URL | `https://cms-auth-github.vercel.app/api/auth` |

### 2. 获取 Client ID 和 Secret

创建后记录 **Client ID**，并生成 **Client Secret**。

### 3. 配置 OAuth Proxy

本项目使用社区托管的 OAuth 代理 `https://cms-auth-github.vercel.app`。
如需要更高的安全性，可以自行部署：

1. Fork [netlify-cms-github-oauth-provider](https://github.com/vencax/netlify-cms-github-oauth-provider)
2. 在 Vercel 上部署，设置环境变量 `CLIENT_ID` 和 `CLIENT_SECRET`
3. 修改 `docs/admin/config.yml` 中的 `base_url` 指向你自己的代理地址

### 4. 访问 CMS

部署完成后，访问 `https://biostatcn.github.io/clinical-ai-stat/admin/` 开始使用。
