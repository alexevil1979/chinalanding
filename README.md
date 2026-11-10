# 数字安全指南

原生 PHP 8.2+ / Apache / MySQL 中文数字安全门户。当前生产环境运行 PHP 8.1，代码避免框架和前端构建依赖。

## Production 备份和 Phase 2 更新

Phase 2 迁移文件 `database/phase2_migration.sql` 仅增加文章元数据字段及索引，不删除或重建已有数据。适用于 MySQL 8，先备份数据库，再执行：

```bash
mysql chinalanding < database/phase2_migration.sql
```

部署时将 Apache DocumentRoot 保持为 `public/`。

## 管理员

`/admin/login` 使用已有管理员账号。文章编辑页支持 SEO 字段、分类、特色/热门标记、图片路径与 Alt、FAQ、资料链接、状态和发布时间。HTML 正文会进行允许标签过滤。站内图片上传暂未开放；使用经过审核的 `/uploads/filename.webp` 文件路径。

## SEO

`/sitemap.xml` 为索引，指向 `sitemap-articles.xml` 与 `sitemap-categories.xml`；RSS 地址为 `/rss.xml`。Baidu/Google verification 值可写入 settings 表中的 `baidu_verification`、`google_verification`。

## 运营注意

文章原有 URL 保持不变。由于现存的 30 篇文章正文审核时只有约 110–270 个字符，不能把它们描述为 1200–2500 字的完整专业文章。本轮没有机械扩写，也没有虚构来源或事实；应由编辑逐篇研究官方资料后完善。视觉插图目前以 CSS 绘制的抽象图形为主，CMS 可关联 WebP 路径，但文件上传/尺寸转换尚未实现。
