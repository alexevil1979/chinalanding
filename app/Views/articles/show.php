<?php
$catSlugs = explode(',', (string)($article['category_slugs'] ?? ''));
$firstSlug = $catSlugs[0] ?? '';
$catNames = (string)($article['categories'] ?? t('nav_network_security'));
$readMinutes = max(1, (int)ceil(mb_strlen(strip_tags($article['content_html']), 'UTF-8') / 450));
$related = [];
if (!empty($article['id'])) {
    $related = localize_articles(query("SELECT a.slug,a.title,a.meta_description,a.published_at FROM articles a WHERE a.id<>? AND a.status='published' AND a.published_at<=NOW() AND EXISTS(SELECT 1 FROM article_category x WHERE x.article_id=a.id AND x.category_id IN (SELECT category_id FROM article_category WHERE article_id=?)) ORDER BY a.published_at DESC LIMIT 5", [$article['id'], $article['id']]));
}
$faqs = json_decode($article['faq_json'] ?? '[]', true) ?: [];
$sources = json_decode($article['sources_json'] ?? '[]', true) ?: [];
$cover = $article['image_url'] ?? '';
$sensitiveSlugs = ['what-is-vpn', 'vpn-vs-proxy', 'what-is-wireguard', 'what-is-vless', 'what-is-dns-leak', 'network-traffic-encryption', 'choose-privacy-tools'];
$isSensitive = in_array($article['slug'] ?? '', $sensitiveSlugs, true) || in_array('vpn-technology', $catSlugs, true);
$bodyHtml = strip_hiddifysales_html(sanitize_article_html($article['content_html']));
if ($isSensitive) {
    $bodyHtml = preg_replace('~<p>\s*(?:<strong>)?(?:编辑说明|Editor note|Примечание редактора)：?(?:</strong>)?.*?</p>~iu', '', $bodyHtml, 1) ?? $bodyHtml;
}
$practiceLinks = [
    ['href' => lp('articles/protect-online-accounts'), 'label' => locale() === 'zh' ? '如何保护在线账户' : (locale() === 'ru' ? 'Как защитить онлайн-аккаунты' : 'How to protect online accounts')],
    ['href' => lp('articles/identify-phishing-attacks'), 'label' => locale() === 'zh' ? '如何识别网络钓鱼' : (locale() === 'ru' ? 'Как распознать фишинг' : 'How to spot phishing')],
    ['href' => lp('articles/what-is-https'), 'label' => locale() === 'zh' ? '什么是 HTTPS' : (locale() === 'ru' ? 'Что такое HTTPS' : 'What is HTTPS')],
    ['href' => lp('articles/two-factor-authentication-guide'), 'label' => locale() === 'zh' ? '双重身份验证指南' : (locale() === 'ru' ? 'Гид по 2FA' : 'Two-factor authentication guide')],
];
$editorNote = locale() === 'zh'
    ? '本文仅供技术学习与网络安全科普，聚焦协议原理、威胁模型与企业远程接入边界，不构成规避监管或违法使用网络服务的指导。'
    : (locale() === 'ru'
        ? 'Статья предназначена только для технического обучения и просвещения по кибербезопасности: принципы протоколов, модели угроз и границы корпоративного удалённого доступа. Это не руководство по обходу регулирования или незаконному использованию сети.'
        : 'This article is for technical learning and cybersecurity education only. It focuses on protocol principles, threat models, and enterprise remote-access boundaries—not guidance for evading regulation or unlawful network use.');
$complianceNote = locale() === 'zh'
    ? '本文仅作技术原理与网络安全科普说明，不构成规避监管、违法使用网络服务或任何违法行为的指导；请遵守中华人民共和国法律法规及相关政策。'
    : (locale() === 'ru'
        ? 'Материал объясняет технические принципы и основы кибербезопасности. Он не является руководством по обходу регулирования, незаконному использованию сети или иным правонарушениям. Соблюдайте применимые законы и политики.'
        : 'This article explains technical principles and cybersecurity education only. It is not guidance for evading regulation, unlawful network use, or any illegal activity. Follow applicable laws and policies.');
$sourcesFallback = locale() === 'zh'
    ? '建议结合相关软件、服务或协议的官方文档核对操作细节。'
    : (locale() === 'ru'
        ? 'Сверяйте детали с официальной документацией соответствующего ПО, сервиса или протокола.'
        : 'Cross-check operational details with official documentation for the relevant software, service, or protocol.');
?>
<div class="container page-stack">
  <div class="article-layout">
    <article class="article-main">
      <nav class="breadcrumbs" aria-label="<?=e(t('breadcrumbs'))?>">
        <a href="<?=e(lp('/'))?>"><?=e(t('home'))?></a><span>›</span>
        <?php if ($firstSlug): ?>
          <a href="<?=e(lp('category/'.$firstSlug))?>"><?=e(explode(locale()==='zh'?'、':', ', $catNames)[0])?></a><span>›</span>
        <?php endif; ?>
        <span><?=e($article['title'])?></span>
      </nav>
      <header class="article-head">
        <p class="meta"><?=e($catNames)?> <span>·</span> <?=e(substr($article['published_at'], 0, 10))?></p>
        <h1><?=e($article['title'])?></h1>
        <p class="article-dek"><?=e($article['meta_description'])?></p>
        <div class="article-byline">
          <span><?=e(t('editor_team'))?></span>
          <span><?=e(t('published_on', ['date' => substr($article['published_at'], 0, 10)]))?></span>
          <span><?=e(t('updated_on', ['date' => substr($article['updated_at'], 0, 10)]))?></span>
          <span><?=e(t('read_minutes', ['n' => (string)$readMinutes]))?></span>
        </div>
      </header>
      <?php if ($cover): ?>
        <figure class="article-cover real-cover"><img src="<?=e($cover)?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" fetchpriority="high"></figure>
      <?php else: ?>
        <div class="article-cover" role="img" aria-label="<?=e($article['title'])?>"><span>DS</span></div>
      <?php endif; ?>
      <details class="toc-box" open><summary><?=e(t('toc'))?></summary><nav data-toc aria-label="<?=e(t('article_toc'))?>"></nav></details>
      <?php if ($isSensitive): ?>
        <aside class="editor-note" role="note">
          <p><strong><?=e(locale()==='zh'?'编辑说明：':(locale()==='ru'?'Примечание редактора: ':'Editor note: '))?></strong><?=e($editorNote)?></p>
        </aside>
      <?php endif; ?>
      <div class="article-content"><?=$bodyHtml?></div>
      <aside class="compliance-note" role="note">
        <p><?=e($complianceNote)?></p>
      </aside>
      <?php if ($isSensitive): ?>
        <section class="practice-links">
          <h2><?=e(t('practice_links'))?></h2>
          <ul>
            <?php foreach ($practiceLinks as $link): ?>
              <li><a href="<?=e($link['href'])?>"><?=e($link['label'])?></a></li>
            <?php endforeach; ?>
          </ul>
        </section>
      <?php endif; ?>
      <?php if ($faqs): ?>
        <section>
          <h2><?=e(t('faq'))?></h2>
          <div class="faq-list">
            <?php foreach ($faqs as $faq): ?>
              <details><summary><?=e($faq['q'])?></summary><p><?=e($faq['a'])?></p></details>
            <?php endforeach; ?>
          </div>
        </section>
      <?php endif; ?>
      <section>
        <h2><?=e(t('sources'))?></h2>
        <?php if ($sources): ?>
          <ul class="source-list">
            <?php foreach ($sources as $source): ?>
              <li><a href="<?=e($source['url'])?>" rel="noopener" target="_blank"><?=e($source['title'] ?: $source['url'])?></a></li>
            <?php endforeach; ?>
          </ul>
        <?php else: ?>
          <p><?=e($sourcesFallback)?></p>
        <?php endif; ?>
      </section>
      <section>
        <h2><?=e(t('related'))?></h2>
        <div class="related-list">
          <?php foreach ($related as $r): ?>
            <article class="search-result">
              <p class="meta"><?=e(substr($r['published_at'], 0, 10))?></p>
              <h3><a href="<?=e(lp('articles/'.$r['slug']))?>"><?=e($r['title'])?></a></h3>
              <p><?=e($r['meta_description'])?></p>
            </article>
          <?php endforeach; ?>
        </div>
      </section>
      <div class="tool-callout">
        <div>
          <p class="eyebrow">CONTINUE</p>
          <h2><?=e(t('tool_callout_title'))?></h2>
          <p><?=e(t('tool_callout_text'))?></p>
        </div>
        <a href="<?=e(lp('tools'))?>"><?=e(t('view_tools'))?></a>
      </div>
    </article>
    <aside class="article-sidebar">
      <h2><?=e(t('related'))?></h2>
      <?php foreach ($related as $r): ?>
        <a href="<?=e(lp('articles/'.$r['slug']))?>"><?=e($r['title'])?><span><?=e(substr($r['published_at'], 0, 10))?></span></a>
      <?php endforeach; ?>
    </aside>
  </div>
</div>
<?php
$datePublished = date('c', strtotime((string)$article['published_at']));
$dateModified = date('c', strtotime((string)$article['updated_at']));
$articleSchema = [
    '@context' => 'https://schema.org',
    '@type' => 'Article',
    'headline' => $article['title'],
    'description' => $article['meta_description'],
    'inLanguage' => locale_bcp47(),
    'datePublished' => $datePublished,
    'dateModified' => $dateModified,
    'author' => ['@type' => 'Organization', 'name' => t('editor_team')],
    'publisher' => ['@type' => 'Organization', 'name' => t('site_name'), 'url' => url('/'), 'logo' => ['@type' => 'ImageObject', 'url' => url('assets/logo.svg')]],
    'mainEntityOfPage' => ['@type' => 'WebPage', '@id' => lurl('articles/' . $article['slug'])],
    'image' => [!empty($cover) ? url(ltrim((string)$cover, '/')) : url('assets/og-default.png')],
];
$crumb = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => [['@type' => 'ListItem', 'position' => 1, 'name' => t('home'), 'item' => lurl('/')]]];
if ($firstSlug) {
    $crumb['itemListElement'][] = ['@type' => 'ListItem', 'position' => 2, 'name' => explode(locale() === 'zh' ? '、' : ', ', $catNames)[0], 'item' => lurl('category/' . $firstSlug)];
}
$crumb['itemListElement'][] = ['@type' => 'ListItem', 'position' => count($crumb['itemListElement']) + 1, 'name' => $article['title'], 'item' => lurl('articles/' . $article['slug'])];
?>
<script type="application/ld+json"><?=json_encode($articleSchema, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<script type="application/ld+json"><?=json_encode($crumb, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<?php if ($faqs): ?><script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'FAQPage','mainEntity'=>array_map(static fn($f)=>['@type'=>'Question','name'=>$f['q'],'acceptedAnswer'=>['@type'=>'Answer','text'=>$f['a']]], $faqs)], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script><?php endif; ?>
