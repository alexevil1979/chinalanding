<div class="container page-stack">
  <section class="category-head">
    <p class="eyebrow">SEARCH THE LIBRARY</p>
    <h1>搜索文章</h1>
    <form class="search-form search-form-lg" action="/search" method="get">
      <label class="sr-only" for="search-page">搜索标题、正文或分类</label>
      <input id="search-page" type="search" name="q" value="<?=e($term)?>" placeholder="搜索标题、正文或分类…">
      <button type="submit">搜索</button>
    </form>
    <?php if ($term !== ''): ?><p>“<?=e($term)?>” 找到 <?=e((string)$total)?> 篇文章</p><?php endif; ?>
  </section>

  <section class="search-results">
    <?php foreach ($results as $item): ?>
    <article class="search-result">
      <p class="meta"><?=e($item['category_name'] ?? '数字安全')?> · <?=e(substr($item['published_at'] ?? '', 0, 10))?></p>
      <h2><a href="/articles/<?=e($item['slug'])?>"><?=e($item['title'])?></a></h2>
      <p><?=e($item['meta_description'])?></p>
    </article>
    <?php endforeach; ?>
    <?php if ($term !== '' && !$results): ?><p>没有找到匹配内容。尝试更短的关键词，或浏览分类页面。</p><?php endif; ?>
  </section>

  <?php if (($pages ?? 0) > 1): ?>
  <nav class="pagination" aria-label="搜索结果分页">
    <?php for ($p = 1; $p <= $pages; $p++): ?>
      <a class="<?=$p === $page ? 'current' : ''?>" href="?q=<?=urlencode($term)?>&page=<?=$p?>"><?=$p?></a>
    <?php endfor; ?>
  </nav>
  <?php endif; ?>
</div>
