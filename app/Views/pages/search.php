<div class="container page-stack">
  <section class="category-head">
    <p class="eyebrow">SEARCH THE LIBRARY</p>
    <h1><?=e(t('search_title'))?></h1>
    <form class="search-form search-form-lg" action="<?=e(lp('search'))?>" method="get">
      <label class="sr-only" for="search-page"><?=e(t('search_articles'))?></label>
      <input id="search-page" type="search" name="q" value="<?=e($term)?>" placeholder="<?=e(t('search_placeholder'))?>">
      <button type="submit"><?=e(t('search'))?></button>
    </form>
    <?php if ($term !== ''): ?><p><?=e($term)?> — <?=e((string)$total)?></p><?php endif; ?>
  </section>

  <section class="search-results">
    <?php foreach ($results as $item): ?>
    <article class="search-result">
      <p class="meta"><?=e($item['category_name'] ?? t('digital_security'))?> · <?=e(substr($item['published_at'] ?? '', 0, 10))?></p>
      <h2><a href="<?=e(lp('articles/'.$item['slug']))?>"><?=e($item['title'])?></a></h2>
      <p><?=e($item['meta_description'])?></p>
    </article>
    <?php endforeach; ?>
    <?php if ($term !== '' && !$results): ?><p><?=e(t('search_empty'))?></p><?php endif; ?>
    <?php if ($term === ''): ?><p><?=e(t('search_prompt'))?></p><?php endif; ?>
  </section>

  <?php if (($pages ?? 0) > 1): ?>
  <nav class="pagination" aria-label="<?=e(t('search_heading'))?>">
    <?php for ($p = 1; $p <= $pages; $p++): ?>
      <a class="<?=$p === $page ? 'current' : ''?>" href="?q=<?=urlencode($term)?>&page=<?=$p?>"><?=$p?></a>
    <?php endfor; ?>
  </nav>
  <?php endif; ?>
</div>
