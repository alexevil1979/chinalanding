<?php
/** @var array $report */
$k = $report['kpis'];
$range = $report['range'];
$maxDaily = 1;
foreach ($report['daily'] as $d) {
    $maxDaily = max($maxDaily, (int)$d['views']);
}
$eventLabels = [
    'outbound_click' => '外链点击',
    'search' => '站内搜索',
    'lang_switch' => '切换语言',
    'scroll_depth' => '滚动深度',
    'cta_click' => 'CTA 点击',
    'menu_open' => '打开菜单',
    'share_click' => '分享点击',
    'toc_click' => '目录点击',
];
$deviceLabels = ['desktop' => '桌面', 'mobile' => '手机', 'tablet' => '平板'];
?>
<div class="container page-stack analytics-page">
  <section class="category-head">
    <p class="eyebrow">SITE ANALYTICS</p>
    <h1>访问统计</h1>
    <p>自有统计：国家 / 浏览器 / 页面 / 用户行为（不含第三方脚本）。</p>
    <div class="analytics-ranges">
      <?php foreach (['today' => '今天', '7d' => '7 天', '30d' => '30 天', '90d' => '90 天'] as $key => $label): ?>
        <a class="button<?= $range === $key ? ' button-dark' : '' ?>" href="/admin/analytics?range=<?=e($key)?>"><?=e($label)?></a>
      <?php endforeach; ?>
      <a class="button" href="/admin">返回后台</a>
    </div>
  </section>

  <section class="analytics-kpis">
    <article><span>浏览量</span><strong><?=e(number_format($k['pageviews']))?></strong></article>
    <article><span>独立访客</span><strong><?=e(number_format($k['visitors']))?></strong></article>
    <article><span>会话</span><strong><?=e(number_format($k['sessions']))?></strong></article>
    <article><span>跳出率</span><strong><?=e((string)$k['bounce_rate'])?>%</strong></article>
    <article><span>行为事件</span><strong><?=e(number_format($k['events']))?></strong></article>
  </section>

  <section class="analytics-panel">
    <h2>每日趋势</h2>
    <?php if (!$report['daily']): ?>
      <p class="meta">所选时段暂无数据。部署后浏览公开页面即可开始采集。</p>
    <?php else: ?>
      <div class="analytics-bars" role="img" aria-label="每日浏览量">
        <?php foreach ($report['daily'] as $d):
          $h = max(4, (int)round(((int)$d['views'] / $maxDaily) * 120));
        ?>
          <div class="analytics-bar-col" title="<?=e($d['d'])?>: <?=e((string)$d['views'])?> PV / <?=e((string)$d['visitors'])?> UV">
            <div class="analytics-bar" style="height:<?=$h?>px"></div>
            <span><?=e(substr($d['d'], 5))?></span>
          </div>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
  </section>

  <div class="analytics-grid">
    <section class="analytics-panel">
      <h2>热门页面</h2>
      <table class="analytics-table">
        <thead><tr><th>路径</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['pages'] as $row): ?>
          <tr><td><?=e($row['path'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['pages']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>热门文章</h2>
      <table class="analytics-table">
        <thead><tr><th>Slug</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['articles'] as $row): ?>
          <tr><td><a href="/articles/<?=e($row['article_slug'])?>" target="_blank" rel="noopener"><?=e($row['article_slug'])?></a></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['articles']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>国家 / 地区</h2>
      <table class="analytics-table">
        <thead><tr><th>地区</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['countries'] as $row): ?>
          <tr><td><?=e(analytics_country_name((string)$row['country']))?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['countries']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
      <p class="meta">国家码优先读取 CDN/反代头（如 CF-IPCountry）。未配置时显示「未知」。</p>
    </section>

    <section class="analytics-panel">
      <h2>浏览器</h2>
      <table class="analytics-table">
        <thead><tr><th>浏览器</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['browsers'] as $row): ?>
          <tr><td><?=e($row['browser'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['browsers']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>操作系统</h2>
      <table class="analytics-table">
        <thead><tr><th>系统</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['os'] as $row): ?>
          <tr><td><?=e($row['os'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['os']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>设备</h2>
      <table class="analytics-table">
        <thead><tr><th>设备</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['devices'] as $row): ?>
          <tr><td><?=e($deviceLabels[$row['device']] ?? $row['device'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['devices']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>语言版本</h2>
      <table class="analytics-table">
        <thead><tr><th>语言</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['locales'] as $row): ?>
          <tr><td><?=e($row['locale'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['locales']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>来源站</h2>
      <table class="analytics-table">
        <thead><tr><th>来源</th><th>PV</th><th>UV</th></tr></thead>
        <tbody>
        <?php foreach ($report['referrers'] as $row): ?>
          <tr><td><?=e($row['referrer_host'])?></td><td><?=e((string)$row['views'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['referrers']): ?><tr><td colspan="3">暂无（多为直接访问）</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>用户行为</h2>
      <table class="analytics-table">
        <thead><tr><th>事件</th><th>次数</th><th>访客</th></tr></thead>
        <tbody>
        <?php foreach ($report['events'] as $row): ?>
          <tr><td><?=e($eventLabels[$row['event_name']] ?? $row['event_name'])?></td><td><?=e((string)$row['total'])?></td><td><?=e((string)$row['visitors'])?></td></tr>
        <?php endforeach; ?>
        <?php if (!$report['events']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>

    <section class="analytics-panel">
      <h2>行为明细</h2>
      <table class="analytics-table">
        <thead><tr><th>事件</th><th>值</th><th>次数</th></tr></thead>
        <tbody>
        <?php foreach ($report['event_values'] as $row): ?>
          <tr>
            <td><?=e($eventLabels[$row['event_name']] ?? $row['event_name'])?></td>
            <td><?=e((string)$row['event_value'])?></td>
            <td><?=e((string)$row['total'])?></td>
          </tr>
        <?php endforeach; ?>
        <?php if (!$report['event_values']): ?><tr><td colspan="3">暂无</td></tr><?php endif; ?>
        </tbody>
      </table>
    </section>
  </div>
</div>
