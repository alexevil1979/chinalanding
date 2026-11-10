<div class="container page-stack">
  <section class="category-head">
    <p class="eyebrow">EDITORIAL DESK</p>
    <h1>管理后台</h1>
    <p>已发布文章：<strong><?=e((string)$stats)?></strong> · 草稿：<strong><?=e((string)($drafts ?? 0))?></strong></p>
    <a class="button button-dark" href="/admin/articles">文章管理</a>
    <a class="button" href="/admin/articles/new">新建文章</a>
    <a href="/admin/logout">退出登录</a>
  </section>

  <section class="admin-settings prose">
    <h2>站点开关</h2>
    <?php if (!empty($saved)): ?>
      <p class="admin-flash">设置已保存。</p>
    <?php endif; ?>
    <form method="post" action="/admin/settings" class="admin-toggle-form">
      <input type="hidden" name="csrf" value="<?=e(csrf())?>">
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
</div>
