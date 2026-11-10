</main>
<footer class="site-footer">
  <div class="container footer-columns">
    <div>
      <a class="brand footer-brand" href="<?=e(lp('/'))?>">
        <span class="brand-mark" aria-hidden="true"><img src="/assets/favicon.svg" width="40" height="40" alt=""></span>
        <span class="brand-name"><?=e(t('site_name'))?><small><?=e(t('site_tagline'))?></small></span>
      </a>
      <p><?=e(t('footer_blurb'))?></p>
    </div>
    <div>
      <h2><?=e(t('explore_topics'))?></h2>
      <a href="<?=e(lp('category/network-security'))?>"><?=e(t('nav_network_security'))?></a>
      <a href="<?=e(lp('category/network-privacy'))?>"><?=e(t('nav_network_privacy'))?></a>
      <a href="<?=e(lp('category/account-security'))?>"><?=e(t('nav_account_security'))?></a>
      <a href="<?=e(lp('category/vpn-technology'))?>"><?=e(t('nav_vpn_technology'))?></a>
      <a href="<?=e(lp('category/tutorials'))?>"><?=e(t('nav_tutorials'))?></a>
      <a href="<?=e(lp('category/data-protection'))?>"><?=e(locale()==='zh'?'数据保护':(locale()==='ru'?'Защита данных':'Data Protection'))?></a>
      <a href="<?=e(lp('category/cryptography'))?>"><?=e(locale()==='zh'?'密码学':(locale()==='ru'?'Криптография':'Cryptography'))?></a>
      <a href="<?=e(lp('category/digital-identity'))?>"><?=e(locale()==='zh'?'数字身份':(locale()==='ru'?'Цифровая идентичность':'Digital Identity'))?></a>
      <a href="<?=e(lp('category/mobile-security'))?>"><?=e(locale()==='zh'?'移动安全':(locale()==='ru'?'Мобильная безопасность':'Mobile Security'))?></a>
      <a href="<?=e(lp('category/network-protocols'))?>"><?=e(locale()==='zh'?'网络协议':(locale()==='ru'?'Сетевые протоколы':'Network Protocols'))?></a>
    </div>
    <div>
      <h2><?=e(t('about_site'))?></h2>
      <a href="<?=e(lp('about'))?>"><?=e(t('about'))?></a>
      <a href="<?=e(lp('contact'))?>"><?=e(t('contact'))?></a>
      <a href="<?=e(lp('privacy-policy'))?>"><?=e(t('privacy'))?></a>
      <a href="<?=e(lp('terms'))?>"><?=e(t('terms'))?></a>
    </div>
    <div>
      <h2><?=e(t('subscribe_index'))?></h2>
      <a href="<?=e(lp('tools'))?>"><?=e(t('tools_link'))?></a>
      <a href="/sitemap.xml"><?=e(t('xml_sitemap'))?></a>
      <a href="<?=e(lp('rss.xml'))?>"><?=e(t('rss_feed'))?></a>
      <?php if (show_hiddifysales()): ?>
      <a href="https://hiddifysales.com" rel="sponsored noopener" target="_blank"><?=e(t('hiddify_ad'))?></a>
      <?php endif; ?>
    </div>
  </div>
  <div class="container legal-disclaimer">
    <p><?=e(t('legal_disclaimer'))?></p>
  </div>
  <div class="container footer-bottom">
    <span><?=e(t('copyright', ['year' => date('Y')]))?></span>
    <?php
      $icp = trim(setting('icp_beian'));
      $icpUrl = trim(setting('icp_url', 'https://beian.miit.gov.cn/'));
    ?>
    <?php if ($icp !== ''): ?>
      <a class="icp-link" href="<?=e($icpUrl !== '' ? $icpUrl : 'https://beian.miit.gov.cn/')?>" rel="noopener" target="_blank"><?=e($icp)?></a>
    <?php else: ?>
      <span class="icp-placeholder"><?=e(t('icp_pending'))?> · <a href="https://beian.miit.gov.cn/" rel="noopener" target="_blank">beian.miit.gov.cn</a></span>
    <?php endif; ?>
    <span><?=e(t('legal_note'))?></span>
  </div>
</footer>
<script src="/assets/site.js?v=20261110i18n" defer></script>
</body>
</html>
