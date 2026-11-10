<div class="container page-stack">
  <section class="category-head">
    <nav class="breadcrumbs" aria-label="<?=e(t('breadcrumbs'))?>"><a href="<?=e(lp('/'))?>"><?=e(t('home'))?></a><span>›</span><span><?=e($category['name'])?></span></nav>
    <p class="eyebrow">TOPIC COLLECTION</p>
    <h1><?=e($category['name'])?></h1>
    <p><?=e($category['description'])?></p>
  </section>

  <div class="latest-grid">
    <?php foreach ($articles as $i => $article): ?>
    <article class="latest-card">
      <a href="<?=e(lp('articles/'.$article['slug']))?>">
        <div class="article-thumb thumb-<?=($i % 4) + 1?>">
          <?php if (!empty($article['image_url'])): ?>
            <img src="<?=e($article['image_url'])?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" loading="lazy">
          <?php else: ?>
            <span><?=sprintf('%02d', $i + 1)?></span>
            <i><?=e(mb_substr($category['name'], 0, 2))?></i>
          <?php endif; ?>
        </div>
        <div class="latest-content">
          <p class="meta"><?=e(substr($article['published_at'] ?? '', 0, 10))?></p>
          <h3><?=e($article['title'])?></h3>
          <p><?=e($article['meta_description'])?></p>
          <span class="read-more"><?=e(t('read_more'))?></span>
        </div>
      </a>
    </article>
    <?php endforeach; ?>
  </div>

  <?php if (empty($articles)): ?><p><?=e(locale()==='zh'?'该主题的文章正在整理中，请浏览其他安全指南。':(locale()==='ru'?'Статьи по этой теме готовятся. Посмотрите другие разделы.':'Articles for this topic are being prepared. Browse other guides.'))?></p><?php endif; ?>

  <?php if (($pages ?? 1) > 1): ?>
  <nav class="pagination" aria-label="<?=e(t('page_n', ['n'=>'']))?>">
    <?php for ($p = 1; $p <= $pages; $p++): ?>
      <a class="<?=$p === $page ? 'current' : ''?>" href="?page=<?=$p?>" <?=$p === $page ? 'aria-current="page"' : ''?>><?=$p?></a>
    <?php endfor; ?>
  </nav>
  <?php endif; ?>

  <section class="tool-callout">
    <div>
      <p class="eyebrow">CONTINUE</p>
      <h2><?=e(t('topics'))?></h2>
      <p><?=e($category['name'])?></p>
    </div>
    <a href="<?=e(lp('search'))?>?q=<?=urlencode($category['name'])?>"><?=e(t('find_articles'))?></a>
  </section>
</div>
