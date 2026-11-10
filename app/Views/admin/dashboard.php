<div class="container page-stack">
  <section class="category-head">
    <p class="eyebrow">EDITORIAL DESK</p>
    <h1>管理后台</h1>
    <p>已发布文章：<strong><?=e((string)$stats)?></strong> · 草稿：<strong><?=e((string)($drafts ?? 0))?></strong></p>
    <a class="button button-dark" href="/admin/articles">文章管理</a>
    <a class="button" href="/admin/articles/new">新建文章</a>
    <a class="button" href="/admin/analytics">访问统计</a>
    <a href="/admin/logout">退出登录</a>
  </section>

  <section class="admin-settings prose">
    <h2>站点开关</h2>
    <?php if (!empty($saved)): ?>
      <p class="admin-flash">设置已保存。</p>
    <?php endif; ?>
    <form method="post" action="/admin/settings" class="admin-toggle-form">
      <input type="hidden" name="csrf" value="<?=e(csrf())?>">
      <input type="hidden" name="form_hiddify" value="1">
      <label class="admin-toggle">
        <input type="checkbox" name="show_hiddifysales" value="1" <?=!empty($showHiddify)?'checked':''?>>
        <span>
          <strong>显示 HiddifySales</strong>
          <small>关闭后，页脚、工具页、关于页及正文中的 HiddifySales 提及与链接将全部隐藏；重新开启后恢复显示。</small>
        </span>
      </label>
      <button type="submit" class="button button-dark">保存设置</button>
    </form>
    <p class="meta">当前状态：<?=!empty($showHiddify)?'<strong>显示中</strong>':'<strong>已隐藏</strong>'?></p>
  </section>

  <section class="admin-settings prose">
    <h2>Google / 搜索引擎收录</h2>
    <p class="meta">用于 Google Search Console 与百度站长验证。保存后 meta 标签会自动出现在全站页头。</p>
    <form method="post" action="/admin/settings" class="admin-toggle-form">
      <input type="hidden" name="csrf" value="<?=e(csrf())?>">
      <input type="hidden" name="form_seo" value="1">
      <label>
        Google Search Console 验证码
        <input type="text" name="google_verification" value="<?=e((string)($googleVerification ?? ''))?>" placeholder="google-site-verification 内容值" autocomplete="off">
      </label>
      <label>
        百度站长验证码
        <input type="text" name="baidu_verification" value="<?=e((string)($baiduVerification ?? ''))?>" placeholder="baidu-site-verification 内容值" autocomplete="off">
      </label>
      <button type="submit" class="button button-dark">保存验证码</button>
    </form>
    <div class="admin-seo-checklist">
      <h3>Google 提交清单</h3>
      <ol>
        <li>打开 <a href="https://search.google.com/search-console" target="_blank" rel="noopener">Google Search Console</a> → 添加资源 <code>https://anquanzhinan.com</code>（域名资源优先）。</li>
        <li>若用 HTML 标签验证：把验证码填到上方并保存，再点「验证」。</li>
        <li>验证通过后提交站点地图：<code>https://anquanzhinan.com/sitemap.xml</code></li>
        <li>确认 <a href="/robots.txt" target="_blank" rel="noopener">/robots.txt</a> 可访问，且 Sitemap 指向正确。</li>
        <li>用 URL 检查工具抽查首页与 2–3 篇英文/中文文章，请求编入索引。</li>
      </ol>
      <p class="meta">当前 Sitemap：<a href="/sitemap.xml" target="_blank" rel="noopener">/sitemap.xml</a> · Articles：<a href="/sitemap-articles.xml" target="_blank" rel="noopener">/sitemap-articles.xml</a></p>
    </div>
  </section>
</div>
