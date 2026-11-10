<?php
$descriptions = [
  'about' => '数字安全指南是面向中文读者的独立科普平台，关注网络安全、账户防护、数据保护与网络技术原理。我们以清晰、审慎和可核查为编辑原则。',
  'contact' => '如需反馈事实错误、提出选题建议或联系编辑团队，请通过下方渠道联系。请勿通过邮件或消息发送密码、验证码或身份证件等敏感信息。',
  'privacy-policy' => '本站不提供公开用户注册。服务器可能处理运行、安全和故障排查所需的技术日志；我们不会出售个人信息。你可以通过浏览器设置管理本地存储和 Cookie。',
  'terms' => '本站内容仅供一般信息与技术科普参考，不构成法律、财务或专业安全建议，也不构成规避监管或违法使用网络服务的指导。请遵守中华人民共和国法律法规及相关政策。',
];
$wechatId = trim(setting('wechat_id'));
$wechatQr = trim(setting('wechat_qr_url'));
$contactEmail = trim(setting('contact_email'));
?>
<div class="container page-stack">
  <article class="prose">
    <p class="eyebrow">DIGITAL SECURITY GUIDE</p>
    <h1><?=e(['about'=>'关于我们','contact'=>'联系我们','privacy-policy'=>'隐私政策','terms'=>'使用条款'][$page] ?? $title)?></h1>
    <p class="lead"><?=e($descriptions[$page] ?? '数字安全与网络技术知识。')?></p>
    <?php if ($page === 'about'): ?>
      <h2>我们的编辑原则</h2>
      <ul>
        <li>持续提供与数字安全和网络技术相关的科普内容。</li>
        <li>区分已知事实、建议和服务提供者的声明。</li>
        <li>不使用隐藏内容、欺骗性跳转或虚假的搜索优化手段。</li>
        <li>涉及具体协议或产品时，优先链接其官方文档并说明适用边界。</li>
        <li>不以“绝对匿名”“规避监管”等不可验证承诺吸引流量。</li>
      </ul>
      <?php if (show_hiddifysales()): ?>
      <h2>商业关系披露</h2>
      <p>本站可能在相关内容中提供指向 HiddifySales 的链接。此类链接会标注为「广告 / 商业链接」；商业关系不会改变本站的编辑主题，也不代表对匿名性或绝对安全作出保证。</p>
      <?php endif; ?>
    <?php elseif ($page === 'contact'): ?>
      <h2>选题与纠错</h2>
      <p>联系编辑团队时，请提供页面地址、具体段落和可核验的参考资料。</p>
      <?php if ($contactEmail !== ''): ?>
        <p>邮箱：<a href="mailto:<?=e($contactEmail)?>"><?=e($contactEmail)?></a></p>
      <?php else: ?>
        <p>公开邮箱配置完成后将显示在此；当前可通过站内反馈渠道或运营方预留的企业联系方式沟通。</p>
      <?php endif; ?>
      <h2>微信公众号 / 企业微信</h2>
      <?php if ($wechatId !== '' || $wechatQr !== ''): ?>
        <?php if ($wechatId !== ''): ?><p>微信号 / 公众号：<strong><?=e($wechatId)?></strong></p><?php endif; ?>
        <?php if ($wechatQr !== ''): ?>
          <figure class="wechat-qr">
            <img src="<?=e($wechatQr)?>" alt="微信二维码" width="180" height="180" loading="lazy">
            <figcaption>使用微信扫码关注或添加</figcaption>
          </figure>
        <?php endif; ?>
      <?php else: ?>
        <p class="wechat-placeholder">微信二维码占位：将公众号 / 企业微信二维码 URL 写入后台设置 <code>wechat_qr_url</code>，并将账号写入 <code>wechat_id</code> 后即可显示。</p>
      <?php endif; ?>
    <?php elseif ($page === 'privacy-policy'): ?>
      <h2>数据最小化</h2>
      <p>站点访问日志可能包含请求时间、IP 地址、浏览器标识和请求路径，并由服务器用于安全排错。管理员访问需要会话 Cookie。本站不提供访客账户注册。</p>
      <h2>第三方链接</h2>
      <p>外部网站有各自的隐私政策。打开外部链接前请核对域名，并查看相应服务的条款。标注为「广告 / 商业链接」的外链与本站编辑内容相互独立。</p>
    <?php else: ?>
      <h2>内容使用与合规边界</h2>
      <p>本站关于网络加密、隧道协议与安全工具的内容仅作技术原理与安全科普说明，不涉及规避监管或违法使用建议。读者应结合自身环境独立判断，不应将通用文章视为对特定系统的审计或保证。</p>
      <h2>更新</h2>
      <p>本站可能更新页面以修正错误或反映技术变化。继续使用本站即表示你已阅读并理解上述边界说明。</p>
    <?php endif; ?>
  </article>
</div>
