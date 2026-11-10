<?php
$layerTitle = locale() === 'zh' ? '三层区分' : (locale() === 'ru' ? 'Три уровня' : 'Three layers');
$startTitle = locale() === 'zh' ? '先读协议与基础实践' : (locale() === 'ru' ? 'Начните с протоколов и базовых практик' : 'Start with protocols & basics');
$rulesTitle = locale() === 'zh' ? '编辑规则' : (locale() === 'ru' ? 'Редакционные правила' : 'Editorial rules');
if (locale() === 'en') {
    $layers = [
        ['Protocol', 'Examples: HTTPS, WireGuard, tunnel encapsulation. Answers how math and packets work—not which vendor to buy.'],
        ['Client', 'Software that implements a protocol. Verify release channels, update sources, and requested permissions. Client security ≠ protocol security.'],
        ['Commercial service', 'An operator provides nodes, accounts, and support. The trust boundary is the operator. Outbound links here are labeled “advertisement / commercial link”.'],
    ];
    $rules = [
        'Protocol articles cover principles, threat models, and enterprise remote-access scenarios only.',
        'Do not treat protocol names, client names, or commercial brands as security guarantees.',
        'Do not promise unlinkable identity, absolute anti-tracking, or universal network availability.',
        'Commercial links use “advertisement / commercial link” and rel="sponsored".',
    ];
    $hiddifyText = 'HiddifySales is a commercial-service / client-related information entry—not the protocol itself and not a security guarantee. The link is for learning about a commercial project only; it is not advice for evading regulation or unlawful use.';
} elseif (locale() === 'ru') {
    $layers = [
        ['Протокол', 'Например HTTPS, WireGuard, способы туннельной инкапсуляции. Отвечает, как работают математика и пакеты — не «какого вендора купить».'],
        ['Клиент', 'ПО, реализующее протокол. Проверяйте каналы релизов, источники обновлений и запрашиваемые права. Безопасность клиента ≠ безопасность протокола.'],
        ['Коммерческий сервис', 'Оператор даёт узлы, аккаунты и поддержку. Граница доверия — у оператора. Внешние ссылки здесь помечаются как «реклама / коммерческая ссылка».'],
    ];
    $rules = [
        'Статьи о протоколах описывают только принципы, модели угроз и сценарии корпоративного удалённого доступа.',
        'Не воспринимайте названия протоколов, клиентов или брендов как гарантию безопасности.',
        'Не обещайте несвязываемую личность, абсолютную защиту от трекинга или универсальную доступность сети.',
        'Коммерческие ссылки используют пометку «реклама / коммерческая ссылка» и rel="sponsored".',
    ];
    $hiddifyText = 'HiddifySales — вход в информацию о коммерческом сервисе/клиенте, а не сам протокол и не гарантия безопасности. Ссылка только для ознакомления с коммерческим проектом; это не совет по обходу регулирования или незаконному использованию.';
} else {
    $layers = [
        ['协议（Protocol）', '如 HTTPS、WireGuard、隧道封装方式。回答「数学与报文如何工作」，不回答「该买哪家服务」。'],
        ['客户端（Client）', '实现协议的软件。需核验发布渠道、更新来源与权限索取；客户端安全 ≠ 协议安全。'],
        ['商业服务（Commercial service）', '由运营方提供节点、账号与支持。信任边界在运营方；本站若出现外链，一律标注「广告 / 商业链接」。'],
    ];
    $rules = [
        '协议文章只讲原理、威胁模型与企业远程接入场景。',
        '不把协议名称、客户端名称或商业品牌写成安全保证。',
        '不承诺身份不可关联、绝对防追踪或任意网络环境可用。',
        '商业链接使用「广告 / 商业链接」与 rel="sponsored"。',
    ];
    $hiddifyText = 'HiddifySales 属于「商业服务 / 客户端相关」信息入口，不是协议本身，也不等于安全保证。链接仅供了解商业项目；不构成规避监管或违法使用建议。';
}
?>
<div class="container page-stack">
  <section class="category-head">
    <nav class="breadcrumbs" aria-label="<?=e(t('breadcrumbs'))?>"><a href="<?=e(lp('/'))?>"><?=e(t('home'))?></a><span>›</span><span><?=e(t('tools_h1'))?></span></nav>
    <p class="eyebrow">PROTOCOLS · CLIENTS · SERVICES</p>
    <h1><?=e(t('tools_h1'))?></h1>
    <p><?=e(t('tools_lead'))?></p>
  </section>

  <section class="editorial-section" style="margin-top:0">
    <div class="section-kicker"><h2><?=e($layerTitle)?></h2><span>FRAMEWORK</span></div>
    <div class="prose" style="margin:0;max-width:none">
      <ol class="layer-list">
        <?php foreach ($layers as $layer): ?>
          <li><strong><?=e($layer[0])?></strong>：<?=e($layer[1])?></li>
        <?php endforeach; ?>
      </ol>
    </div>
  </section>

  <?php if (show_hiddifysales()): ?>
  <section class="tool-callout sponsored-callout">
    <div>
      <p class="eyebrow"><?=e(t('ad_label'))?></p>
      <h2>HiddifySales</h2>
      <p><?=e($hiddifyText)?></p>
    </div>
    <a href="https://hiddifysales.com" rel="sponsored noopener" target="_blank"><?=e(t('hiddify_ad'))?> ↗</a>
  </section>
  <?php endif; ?>

  <section class="editorial-section">
    <div class="section-kicker"><h2><?=e($startTitle)?></h2><span>START HERE</span></div>
    <div class="latest-grid">
      <?php foreach ($guides as $i => $article): ?>
      <article class="latest-card">
        <a href="<?=e(lp('articles/'.$article['slug']))?>">
          <div class="article-thumb thumb-<?=($i % 4) + 1?>">
            <?php if (!empty($article['image_url'])): ?>
              <img src="<?=e($article['image_url'])?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=sprintf('%02d', $i + 1)?></span><i><?=e(t('protocol_label'))?></i>
            <?php endif; ?>
          </div>
          <div class="latest-content">
            <p class="meta"><?=e($article['category_name'] ?? t('digital_security'))?> · <?=e(substr($article['published_at'] ?? '', 0, 10))?></p>
            <h3><?=e($article['title'])?></h3>
            <p><?=e($article['meta_description'])?></p>
            <span class="read-more"><?=e(t('read_article'))?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="editorial-section">
    <div class="section-kicker"><h2><?=e($rulesTitle)?></h2><span>RULES</span></div>
    <div class="prose" style="margin:0;max-width:none">
      <ul>
        <?php foreach ($rules as $rule): ?><li><?=e($rule)?></li><?php endforeach; ?>
      </ul>
      <p>
        <a href="<?=e(lp('articles/identify-phishing-attacks'))?>"><?=e(t('cta_phishing'))?></a> ·
        <a href="<?=e(lp('articles/two-factor-authentication-guide'))?>"><?=e(t('cta_2fa'))?></a> ·
        <a href="<?=e(lp('articles/what-is-https'))?>">HTTPS</a> ·
        <a href="<?=e(lp('articles/protect-online-accounts'))?>"><?=e(locale()==='zh'?'保护在线账户':(locale()==='ru'?'Защита аккаунтов':'Protect accounts'))?></a>
      </p>
    </div>
  </section>
</div>
