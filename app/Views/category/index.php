<div class="container page-stack">
  <section class="category-head">
    <nav class="breadcrumbs" aria-label="面包屑"><a href="/">首页</a><span>›</span><span><?=e($category['name'])?></span></nav>
    <p class="eyebrow">TOPIC COLLECTION</p>
    <?php $displayName=($category['slug']??'')==='vpn-technology'?'网络加密技术':$category['name']; ?>
    <h1><?=e($displayName)?></h1>
    <p><?=e($category['description'])?></p>
  </section>

  <div class="latest-grid">
    <?php foreach ($articles as $i => $article): ?>
    <article class="latest-card">
      <a href="/articles/<?=e($article['slug'])?>">
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
          <span class="read-more">阅读全文 →</span>
        </div>
      </a>
    </article>
    <?php endforeach; ?>
  </div>

  <?php if (empty($articles)): ?><p>该主题的文章正在整理中，请浏览其他安全指南。</p><?php endif; ?>

  <?php if (($pages ?? 1) > 1): ?>
  <nav class="pagination" aria-label="分页">
    <?php for ($p = 1; $p <= $pages; $p++): ?>
      <a class="<?=$p === $page ? 'current' : ''?>" href="?page=<?=$p?>" <?=$p === $page ? 'aria-current="page"' : ''?>><?=$p?></a>
    <?php endfor; ?>
  </nav>
  <?php endif; ?>

  <section class="tool-callout">
    <div>
      <p class="eyebrow">继续探索</p>
      <h2>把知识连接起来</h2>
      <p>通过站内搜索查找与 <?=e($category['name'])?> 相关的其他文章。</p>
    </div>
    <a href="/search?q=<?=urlencode($category['name'])?>">搜索本主题 ↗</a>
  </section>
</div>
