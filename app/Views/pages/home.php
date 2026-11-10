<?php
$feature = $featured[0] ?? ($latest[0] ?? null);
$side = array_slice($featured ?? [], 1, 2);
if (count($side) < 2) {
    $side = array_slice($latest, 1, 2);
}
$primaryTopics = array_slice($categories, 0, 8);
$icons = ['◉', '⌘', '▣', '⌁', '↗', '◇', '⊞', '◎'];
$labelCat = static function (?string $name): string {
    $name = trim((string)$name);
    return $name !== '' ? $name : t('digital_security');
};
?>
<section class="hero-bleed">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="brand-hero"><?=e(t('site_name'))?></p>
      <h1><?=e(t('home_h1'))?></h1>
      <p class="hero-lead"><?=e(t('home_lead'))?></p>
      <div class="hero-actions">
        <a class="button button-light" href="<?=e(lp('articles/identify-phishing-attacks'))?>"><?=e(t('cta_phishing'))?></a>
        <a class="text-link light" href="<?=e(lp('articles/two-factor-authentication-guide'))?>"><?=e(t('cta_2fa'))?></a>
      </div>
    </div>
    <div class="hero-art" role="img" aria-label="<?=e(t('hero_art_label'))?>">
      <div class="art-orbit orbit-one"></div>
      <div class="art-orbit orbit-two"></div>
      <div class="art-core">
        <div class="shield">◆</div>
        <span>SECURE<br>BY DESIGN</span>
      </div>
      <i class="node node-a"></i>
      <i class="node node-b"></i>
      <i class="node node-c"></i>
      <i class="node node-d"></i>
      <div class="art-caption">PRIVACY IS A PRACTICE</div>
    </div>
  </div>
</section>

<div class="container page-stack">
  <section class="editorial-section">
    <div class="section-kicker">
      <h2><?=e(t('featured'))?></h2>
      <span>FEATURED</span>
    </div>
    <?php if ($feature): ?>
    <div class="featured-layout">
      <a class="feature-main" href="<?=e(lp('articles/'.$feature['slug']))?>">
        <div class="feature-visual">
          <?php if (!empty($feature['image_url'])): ?>
            <img src="<?=e($feature['image_url'])?>" alt="<?=e($feature['image_alt'] ?? $feature['title'])?>" loading="lazy">
          <?php else: ?>
            <div class="visual-lock">◈</div>
          <?php endif; ?>
          <span class="visual-label"><?=e(t('featured'))?></span>
        </div>
        <div class="feature-text">
          <p class="meta"><?=e($labelCat($feature['category_name'] ?? null))?> <span>·</span> <?=e(substr($feature['published_at'] ?? '', 0, 10))?></p>
          <h3><?=e($feature['title'])?></h3>
          <p><?=e($feature['meta_description'])?></p>
          <span class="read-more"><?=e(t('read_more'))?></span>
        </div>
      </a>
      <div class="feature-side">
        <?php foreach ($side as $i => $item): ?>
        <a class="feature-small" href="<?=e(lp('articles/'.$item['slug']))?>">
          <div class="small-art art-<?=($i + 1)?>">
            <?php if (!empty($item['image_url'])): ?>
              <img src="<?=e($item['image_url'])?>" alt="<?=e($item['image_alt'] ?? $item['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=($i === 0 ? '01' : '02')?></span>
              <b>SECURITY<br>NOTES</b>
            <?php endif; ?>
          </div>
          <div>
            <p class="meta"><?=e($labelCat($item['category_name'] ?? null))?> · <?=e(substr($item['published_at'] ?? '', 0, 10))?></p>
            <h3><?=e($item['title'])?></h3>
            <p><?=e($item['meta_description'])?></p>
          </div>
        </a>
        <?php endforeach; ?>
      </div>
    </div>
    <?php endif; ?>
  </section>

  <section class="editorial-section">
    <div class="section-kicker">
      <h2><?=e(t('topics'))?></h2>
      <span>TOPICS</span>
    </div>
    <div class="topic-grid">
      <?php foreach ($primaryTopics as $i => $cat): ?>
      <a class="topic-card" href="<?=e(lp('category/'.$cat['slug']))?>">
        <span class="topic-icon"><?=$icons[$i % count($icons)]?></span>
        <span class="topic-number"><?=sprintf('%02d', $i + 1)?></span>
        <h3><?=e($cat['name'])?></h3>
        <p><?=e($cat['description'])?></p>
        <span class="topic-arrow">↗</span>
      </a>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="editorial-section">
    <div class="section-kicker">
      <h2><?=e(t('latest'))?></h2>
      <span>LATEST</span>
      <a href="<?=e(lp('search'))?>"><?=e(t('find_articles'))?></a>
    </div>
    <div class="latest-grid">
      <?php foreach (array_slice($latest, 0, 6) as $i => $article): ?>
      <article class="latest-card">
        <a href="<?=e(lp('articles/'.$article['slug']))?>">
          <div class="article-thumb thumb-<?=($i % 4) + 1?>">
            <?php if (!empty($article['image_url'])): ?>
              <img src="<?=e($article['image_url'])?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=sprintf('%02d', $i + 1)?></span>
              <i><?=e(mb_substr($labelCat($article['category_name'] ?? null), 0, 2))?></i>
            <?php endif; ?>
          </div>
          <div class="latest-content">
            <p class="meta"><?=e($labelCat($article['category_name'] ?? null))?> <span>·</span> <?=e(substr($article['published_at'] ?? '', 0, 10))?></p>
            <h3><?=e($article['title'])?></h3>
            <p><?=e($article['meta_description'])?></p>
            <span class="read-more"><?=e(t('read_article'))?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="editorial-section guide-band">
    <div>
      <p class="eyebrow">PRACTICAL GUIDES</p>
      <h2><?=e(t('guide_band_title'))?></h2>
      <p><?=e(t('guide_band_text'))?></p>
      <a class="button button-dark" href="<?=e(lp('category/tutorials'))?>"><?=e(t('browse_tutorials'))?></a>
    </div>
    <div class="guide-list">
      <?php foreach (array_slice($popular ?? $latest, 0, 3) as $i => $article): ?>
      <a href="<?=e(lp('articles/'.$article['slug']))?>">
        <span>0<?=($i + 1)?></span>
        <strong><?=e($article['title'])?></strong>
        <b>↗</b>
      </a>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="principles-section">
    <div class="principle-visual"><div class="principle-ring">SECURITY<br>IS A PROCESS</div></div>
    <div>
      <p class="eyebrow">SECURITY KNOWLEDGE</p>
      <h2><?=e(t('principles_title'))?></h2>
      <p><?=e(t('principles_p1'))?></p>
      <p><?=e(t('principles_p2'))?></p>
      <a class="text-link" href="<?=e(lp('about'))?>"><?=e(t('learn_editorial'))?></a>
    </div>
  </section>

  <section class="tool-callout">
    <div>
      <p class="eyebrow">PROTOCOLS · PRACTICE · TOOLS</p>
      <h2><?=e(t('tool_callout_title'))?></h2>
      <p><?=e(t('tool_callout_text'))?></p>
    </div>
    <a href="<?=e(lp('tools'))?>"><?=e(t('view_tools'))?></a>
  </section>
</div>
