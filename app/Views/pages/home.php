<?php
$feature = $featured[0] ?? ($latest[0] ?? null);
$side = array_slice($featured ?? [], 1, 2);
if (count($side) < 2) { $side = array_slice($latest, 1, 2); }
$primaryTopics = array_slice($categories, 0, 8);
$icons = ['◉','⌘','▣','⌁','↗','◇','⊞','◎'];
$labelCat = static function (?string $name): string {
    $name = trim((string)$name);
    if ($name === '' || $name === 'VPN技术') return $name === 'VPN技术' ? '网络加密技术' : '数字安全';
    return str_replace('VPN技术', '网络加密技术', $name);
};
?>
<section class="hero-bleed">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="brand-hero">数字安全指南</p>
      <h1>网络安全与数字隐私科普指南</h1>
      <p class="hero-lead">优先学习钓鱼识别、双重验证、家庭网络安全与系统更新；再按需了解 HTTPS、账户防护与数据加密等可验证实践。</p>
      <div class="hero-actions">
        <a class="button button-light" href="/articles/identify-phishing-attacks">钓鱼识别指南</a>
        <a class="text-link light" href="/articles/two-factor-authentication-guide">双重验证 →</a>
      </div>
    </div>
    <div class="hero-art" role="img" aria-label="数字安全主题插画：盾牌与互联节点">
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
      <h2>编辑精选</h2>
      <span>FEATURED</span>
    </div>
    <?php if ($feature): ?>
    <div class="featured-layout">
      <a class="feature-main" href="/articles/<?=e($feature['slug'])?>">
        <div class="feature-visual">
          <?php if (!empty($feature['image_url'])): ?>
            <img src="<?=e($feature['image_url'])?>" alt="<?=e($feature['image_alt'] ?? $feature['title'])?>" loading="lazy">
          <?php else: ?>
            <div class="visual-lock">◈</div>
          <?php endif; ?>
          <span class="visual-label">编辑精选</span>
        </div>
        <div class="feature-text">
          <p class="meta"><?=e($labelCat($feature['category_name'] ?? '数字安全'))?> <span>·</span> <?=e(substr($feature['published_at'] ?? '', 0, 10))?></p>
          <h3><?=e($feature['title'])?></h3>
          <p><?=e($feature['meta_description'])?></p>
          <span class="read-more">阅读全文 →</span>
        </div>
      </a>
      <div class="feature-side">
        <?php foreach ($side as $i => $item): ?>
        <a class="feature-small" href="/articles/<?=e($item['slug'])?>">
          <div class="small-art art-<?=($i + 1)?>">
            <?php if (!empty($item['image_url'])): ?>
              <img src="<?=e($item['image_url'])?>" alt="<?=e($item['image_alt'] ?? $item['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=($i === 0 ? '01' : '02')?></span>
              <b>SECURITY<br>NOTES</b>
            <?php endif; ?>
          </div>
          <div>
            <p class="meta"><?=e($labelCat($item['category_name'] ?? '数字安全'))?> · <?=e(substr($item['published_at'] ?? '', 0, 10))?></p>
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
      <h2>探索主题</h2>
      <span>TOPICS</span>
    </div>
    <div class="topic-grid">
      <?php foreach ($primaryTopics as $i => $cat): ?>
      <a class="topic-card" href="/category/<?=e($cat['slug'])?>">
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
      <h2>最新文章</h2>
      <span>LATEST</span>
      <a href="/search">查找文章 →</a>
    </div>
    <div class="latest-grid">
      <?php foreach (array_slice($latest, 0, 6) as $i => $article): ?>
      <article class="latest-card">
        <a href="/articles/<?=e($article['slug'])?>">
          <div class="article-thumb thumb-<?=($i % 4) + 1?>">
            <?php if (!empty($article['image_url'])): ?>
              <img src="<?=e($article['image_url'])?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=sprintf('%02d', $i + 1)?></span>
              <i><?=e(mb_substr($labelCat($article['category_name'] ?? '安全'), 0, 2))?></i>
            <?php endif; ?>
          </div>
          <div class="latest-content">
            <p class="meta"><?=e($labelCat($article['category_name'] ?? '数字安全'))?> <span>·</span> <?=e(substr($article['published_at'] ?? '', 0, 10))?></p>
            <h3><?=e($article['title'])?></h3>
            <p><?=e($article['meta_description'])?></p>
            <span class="read-more">阅读文章 →</span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="editorial-section guide-band">
    <div>
      <p class="eyebrow">PRACTICAL GUIDES</p>
      <h2>把安全知识，变成日常习惯</h2>
      <p>从账户保护、设备设置到网络连接，用循序渐进的指南解决具体问题。</p>
      <a class="button button-dark" href="/category/tutorials">浏览实用教程</a>
    </div>
    <div class="guide-list">
      <?php foreach (array_slice($popular ?? $latest, 0, 3) as $i => $article): ?>
      <a href="/articles/<?=e($article['slug'])?>">
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
      <h2>安全不是一个按钮，而是一套持续实践</h2>
      <p>可靠的数字安全来自多个环节：使用独立凭据、及时更新软件、限制不必要的权限，并在敏感操作前核实对象与网站。单一工具无法替代这些基本习惯。</p>
      <p>本站尽量提供可核查的基础知识与实用步骤；涉及具体产品时，请同时阅读官方文档，理解其适用范围和限制。</p>
      <a class="text-link" href="/about">了解我们的编辑原则 →</a>
    </div>
  </section>

  <section class="tool-callout">
    <div>
      <p class="eyebrow">协议 · 实践 · 工具</p>
      <h2>网络加密与安全实践专题</h2>
      <p>先读钓鱼识别、双重验证与 HTTPS；需要了解隧道协议原理时，再进入网络加密专题。商业项目单独标注为「广告 / 商业链接」。</p>
    </div>
    <a href="/tools">查看工具专题 ↗</a>
  </section>
</div>
