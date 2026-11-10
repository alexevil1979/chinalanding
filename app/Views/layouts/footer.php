</main>
<footer class="site-footer">
  <div class="container footer-columns">
    <div>
      <a class="brand footer-brand" href="/">
        <span class="brand-mark">DS</span>
        <span class="brand-name">数字安全指南<small>DIGITAL SECURITY GUIDE</small></span>
      </a>
      <p>面向中文读者的数字安全与网络技术科普平台。以清晰、审慎、可验证的内容，帮助读者理解网络安全与账户防护。</p>
    </div>
    <div>
      <h2>探索主题</h2>
      <a href="/category/network-security">网络安全</a>
      <a href="/category/network-privacy">网络隐私</a>
      <a href="/category/account-security">账户安全</a>
      <a href="/category/vpn-technology">网络加密</a>
      <a href="/category/tutorials">使用教程</a>
      <a href="/category/data-protection">数据保护</a>
      <a href="/category/cryptography">密码学</a>
      <a href="/category/digital-identity">数字身份</a>
      <a href="/category/mobile-security">移动安全</a>
      <a href="/category/network-protocols">网络协议</a>
    </div>
    <div>
      <h2>关于本站</h2>
      <a href="/about">关于我们</a>
      <a href="/contact">联系我们</a>
      <a href="/privacy-policy">隐私政策</a>
      <a href="/terms">使用条款</a>
    </div>
    <div>
      <h2>订阅与索引</h2>
      <a href="/tools">网络加密与安全工具</a>
      <a href="/sitemap.xml">XML Sitemap</a>
      <a href="/rss.xml">RSS Feed</a>
      <?php if (show_hiddifysales()): ?>
      <a href="https://hiddifysales.com" rel="sponsored noopener" target="_blank">HiddifySales（广告 / 商业链接）</a>
      <?php endif; ?>
    </div>
  </div>
  <div class="container legal-disclaimer">
    <p>本站内容仅供技术学习与网络安全科普，不构成规避监管、违法使用网络服务或任何违法行为的指导；请遵守中华人民共和国法律法规及相关政策。涉及协议原理的说明不等于使用建议，也不对匿名性或绝对安全作出保证。</p>
  </div>
  <div class="container footer-bottom">
    <span>© <?=date('Y')?> 数字安全指南</span>
    <?php
      $icp=trim(setting('icp_beian'));
      $icpUrl=trim(setting('icp_url','https://beian.miit.gov.cn/'));
    ?>
    <?php if ($icp !== ''): ?>
      <a class="icp-link" href="<?=e($icpUrl !== '' ? $icpUrl : 'https://beian.miit.gov.cn/')?>" rel="noopener" target="_blank"><?=e($icp)?></a>
    <?php else: ?>
      <span class="icp-placeholder">ICP备案号：申请中 / 待填入 · <a href="https://beian.miit.gov.cn/" rel="noopener" target="_blank">beian.miit.gov.cn</a></span>
    <?php endif; ?>
    <span>内容用于一般信息参考，不构成安全或法律保证。</span>
  </div>
</footer>
<script src="/assets/site.js?v=20261110d" defer></script>
</body>
</html>
