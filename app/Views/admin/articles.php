<div class="container page-stack">
  <section class="category-head">
    <p class="eyebrow">CONTENT MANAGEMENT</p>
    <h1>文章管理</h1>
    <a class="button button-dark" href="/admin/articles/new">新建文章</a>
  </section>
  <form method="post" action="/admin/articles/bulk">
    <input type="hidden" name="csrf" value="<?=e(csrf())?>">
    <label>批量操作
      <select name="bulk_action">
        <option value="publish">发布</option>
        <option value="draft">设为草稿</option>
        <option value="delete">删除</option>
      </select>
    </label>
    <button class="button button-dark" type="submit">应用到所选</button>
    <?php foreach ($articles as $a): ?>
    <article class="admin-row">
      <label><input type="checkbox" name="ids[]" value="<?=e((string)$a['id'])?>"> <span class="meta"><?=e($a['status'])?></span></label>
      <strong><?=e($a['title'])?></strong>
      <span><?=e($a['slug'])?></span>
      <a href="/admin/articles/<?=e((string)$a['id'])?>/edit">编辑 / SEO / 媒体</a>
      <?php if ($a['status'] === 'published'): ?><a href="/articles/<?=e($a['slug'])?>" target="_blank">查看</a><?php endif; ?>
    </article>
    <?php endforeach; ?>
  </form>
</div>
