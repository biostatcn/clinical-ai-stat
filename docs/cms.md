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

⚠️ **社区 OAuth 代理 `cms-auth-github.vercel.app` 已失效，需要自行部署 OAuth 代理才能登录 CMS。**

### 完整配置步骤（约 15 分钟）

#### 步骤 1：部署 OAuth 代理到 Vercel（免费）

1. 打开 [netlify-cms-github-oauth-provider](https://github.com/vencax/netlify-cms-github-oauth-provider)
2. 点击 **"Deploy to Vercel"** 按钮
3. 登录 Vercel（可用 GitHub 账号直接登录）
4. 在环境变量中先填写占位值：
   - `CLIENT_ID` → 填 `placeholder`
   - `CLIENT_SECRET` → 填 `placeholder`
5. 部署完成，会得到一个 URL（如 `https://xxx.vercel.app`）

#### 步骤 2：创建 GitHub OAuth App

前往 GitHub → Settings → Developer settings → [OAuth Apps](https://github.com/settings/developers) → New OAuth App：

| 字段 | 值 |
|------|-----|
| Application name | `clinical-ai-stat-cms` |
| Homepage URL | `https://biostatcn.github.io/clinical-ai-stat/` |
| Authorization callback URL | `https://你的-vercel-url.vercel.app/api/auth` |

#### 步骤 3：配置 Vercel 环境变量

1. 记录 OAuth App 的 **Client ID** 和 **Client Secret**
2. 回到 Vercel 项目设置 → Environment Variables
3. 更新：
   - `CLIENT_ID` → 填入 OAuth App 的 Client ID
   - `CLIENT_SECRET` → 填入 OAuth App 的 Client Secret
4. 重新部署 Vercel 项目

#### 步骤 4：更新本站配置

修改 `docs/admin/config.yml` 中的 `base_url` 为你的 Vercel URL：

```yaml
backend:
  name: github
  repo: biostatcn/clinical-ai-stat
  branch: master
  base_url: https://你的-vercel-url.vercel.app
  auth_endpoint: api/auth
```

然后执行 `git add . && git commit -m "update CMS OAuth URL" && git push`

#### 步骤 5：访问 CMS

部署完成后，访问 `https://biostatcn.github.io/clinical-ai-stat/admin/`，点击 **"Login with GitHub"** 即可。
