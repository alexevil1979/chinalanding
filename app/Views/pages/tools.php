<div class="container page-stack">
  <section class="category-head">
    <nav class="breadcrumbs" aria-label="面包屑"><a href="/">首页</a><span>›</span><span>网络加密与安全工具</span></nav>
    <p class="eyebrow">PROTOCOLS · CLIENTS · SERVICES</p>
    <h1>网络加密与安全工具基础</h1>
    <p>本页把讨论拆成三层：协议原理、客户端实现、商业服务。先理解边界，再决定是否查看任何商业项目。</p>
  </section>

  <section class="editorial-section" style="margin-top:0">
    <div class="section-kicker"><h2>三层区分</h2><span>FRAMEWORK</span></div>
    <div class="prose" style="margin:0;max-width:none">
      <ol class="layer-list">
        <li><strong>协议（Protocol）</strong>：如 HTTPS、WireGuard、隧道封装方式。回答「数学与报文如何工作」，不回答「该买哪家服务」。</li>
        <li><strong>客户端（Client）</strong>：实现协议的软件。需核验发布渠道、更新来源与权限索取；客户端安全 ≠ 协议安全。</li>
        <li><strong>商业服务（Commercial service）</strong>：由运营方提供节点、账号与支持。信任边界在运营方；本站若出现外链，一律标注「广告 / 商业链接」。</li>
      </ol>
    </div>
  </section>

  <?php if (show_hiddifysales()): ?>
  <section class="tool-callout sponsored-callout">
    <div>
      <p class="eyebrow">广告 / 商业链接 · 第三层</p>
      <h2>关于 HiddifySales</h2>
      <p>HiddifySales 属于「商业服务 / 客户端相关」信息入口，不是协议本身，也不等于安全保证。链接仅供了解商业项目；不构成规避监管或违法使用建议。</p>
    </div>
    <a href="https://hiddifysales.com" rel="sponsored noopener" target="_blank">访问 HiddifySales（广告 / 商业链接） ↗</a>
  </section>
  <?php endif; ?>

  <section class="editorial-section">
    <div class="section-kicker"><h2>先读协议与基础实践</h2><span>START HERE</span></div>
    <div class="latest-grid">
      <?php foreach ($guides as $i => $article): ?>
      <article class="latest-card">
        <a href="/articles/<?=e($article['slug'])?>">
          <div class="article-thumb thumb-<?=($i % 4) + 1?>">
            <?php if (!empty($article['image_url'])): ?>
              <img src="<?=e($article['image_url'])?>" alt="<?=e($article['image_alt'] ?? $article['title'])?>" loading="lazy">
            <?php else: ?>
              <span><?=sprintf('%02d', $i + 1)?></span><i>协议</i>
            <?php endif; ?>
          </div>
          <div class="latest-content">
            <p class="meta"><?=e(str_replace('VPN技术','网络加密技术',(string)($article['category_name'] ?? '网络技术')))?> · <?=e(substr($article['published_at'] ?? '', 0, 10))?></p>
            <h3><?=e($article['title'])?></h3>
            <p><?=e($article['meta_description'])?></p>
            <span class="read-more">阅读文章 →</span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="editorial-section">
    <div class="section-kicker"><h2>编辑规则</h2><span>RULES</span></div>
    <div class="prose" style="margin:0;max-width:none">
      <ul>
        <li>协议文章只讲原理、威胁模型与企业远程接入场景。</li>
        <li>不把协议名称、客户端名称或商业品牌写成安全保证。</li>
        <li>不承诺身份不可关联、绝对防追踪或任意网络环境可用。</li>
        <li>商业链接使用「广告 / 商业链接」与 <code>rel="sponsored"</code>。</li>
      </ul>
      <p>日常优先：<a href="/articles/identify-phishing-attacks">识别网络钓鱼</a>、<a href="/articles/two-factor-authentication-guide">双重验证</a>、<a href="/articles/what-is-https">HTTPS</a>、<a href="/articles/protect-online-accounts">保护在线账户</a>。</p>
    </div>
  </section>
</div>
