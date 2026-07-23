# 网站对外打开（部署说明）

你现在已有静态网站目录：
- `docs/site/`

可选部署方式：

## 1) GitHub Pages（免费）
1. 把仓库推送到 GitHub
2. 在仓库 Settings → Pages
3. Source 选择 Deploy from a branch
4. Branch 选择 `main`，Folder 选择 `/docs`
5. 访问 `https://<你的用户名>.github.io/<仓库名>/site/`

## 2) Netlify（免费）
1. 登录 Netlify，新建站点
2. 拖拽上传 `docs/site` 文件夹
3. 自动生成公网链接

## 3) Vercel
1. 新建 Project，导入仓库
2. Root Directory 指向 `docs/site`
3. 部署后得到公网链接

---

本地预览（已在本机测试可打开）：
- http://localhost:8787
