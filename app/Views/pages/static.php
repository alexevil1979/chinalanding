<?php
$copy = $pageCopy ?? null;
$wechatId = trim(setting('wechat_id'));
$wechatQr = trim(setting('wechat_qr_url'));
$contactEmail = trim(setting('contact_email'));

if ($copy) {
    $h1 = $copy['h1'] ?? ($title ?? '');
    $lead = $copy['lead'] ?? '';
} else {
    $h1 = ['about' => '关于我们', 'contact' => '联系我们', 'privacy-policy' => '隐私政策', 'terms' => '使用条款'][$page] ?? $title;
    $descriptions = [
        'about' => '数字安全指南是面向中文读者的独立科普平台，关注网络安全、账户防护、数据保护与网络技术原理。我们以清晰、审慎和可核查为编辑原则。',
        'contact' => '如需反馈事实错误、提出选题建议或联系编辑团队，请通过下方渠道联系。请勿通过邮件或消息发送密码、验证码或身份证件等敏感信息。',
        'privacy-policy' => '本站不提供公开用户注册。我们使用自有（非第三方）访问统计：记录页面路径、语言、浏览器/设备类型、大致地区（若反代提供国家码）及站内行为事件；不以广告目的出售数据。你可通过浏览器清除 Cookie（aq_vid / aq_sid）。',
        'terms' => '本站内容仅供一般信息与技术科普参考，不构成法律、财务或专业安全建议，也不构成规避监管或违法使用网络服务的指导。请遵守中华人民共和国法律法规及相关政策。',
    ];
    $lead = $descriptions[$page] ?? t('default_description');
}
?>
<div class="container page-stack">
  <article class="prose">
    <p class="eyebrow">DIGITAL SECURITY GUIDE</p>
    <h1><?=e($h1)?></h1>
    <p class="lead"><?=e($lead)?></p>
    <?php if ($page === 'about'): ?>
      <h2><?=e($copy['h2_principles'] ?? '我们的编辑原则')?></h2>
      <ul>
        <?php if (!empty($copy['principles']) && is_array($copy['principles'])): ?>
          <?php foreach ($copy['principles'] as $item): ?><li><?=e($item)?></li><?php endforeach; ?>
        <?php else: ?>
          <li>持续提供与数字安全和网络技术相关的科普内容。</li>
          <li>区分已知事实、建议和服务提供者的声明。</li>
          <li>不使用隐藏内容、欺骗性跳转或虚假的搜索优化手段。</li>
          <li>涉及具体协议或产品时，优先链接其官方文档并说明适用边界。</li>
          <li>不以“绝对匿名”“规避监管”等不可验证承诺吸引流量。</li>
        <?php endif; ?>
      </ul>
      <?php if (show_hiddifysales()): ?>
      <h2><?=e($copy['h2_commercial'] ?? '商业关系披露')?></h2>
      <p><?=e($copy['commercial'] ?? '本站可能在相关内容中提供指向 HiddifySales 的链接。此类链接会标注为「广告 / 商业链接」；商业关系不会改变本站的编辑主题，也不代表对匿名性或绝对安全作出保证。')?></p>
      <?php endif; ?>
    <?php elseif ($page === 'contact'): ?>
      <h2><?=e($copy['h2_corrections'] ?? '选题与纠错')?></h2>
      <p><?=e($copy['corrections'] ?? '联系编辑团队时，请提供页面地址、具体段落和可核验的参考资料。')?></p>
      <?php if ($contactEmail !== ''): ?>
        <p><?=locale()==='zh'?'邮箱：':(locale()==='ru'?'Email: ':'Email: ')?> <a href="mailto:<?=e($contactEmail)?>"><?=e($contactEmail)?></a></p>
      <?php else: ?>
        <p><?=e($copy['email_pending'] ?? '公开邮箱配置完成后将显示在此；当前可通过站内反馈渠道或运营方预留的企业联系方式沟通。')?></p>
      <?php endif; ?>
      <h2><?=e($copy['h2_wechat'] ?? '微信公众号 / 企业微信')?></h2>
      <?php if ($wechatId !== '' || $wechatQr !== ''): ?>
        <?php if ($wechatId !== ''): ?><p>WeChat: <strong><?=e($wechatId)?></strong></p><?php endif; ?>
        <?php if ($wechatQr !== ''): ?>
          <figure class="wechat-qr">
            <img src="<?=e($wechatQr)?>" alt="WeChat QR" width="180" height="180" loading="lazy">
            <figcaption><?=e($copy['wechat_caption'] ?? '使用微信扫码关注或添加')?></figcaption>
          </figure>
        <?php endif; ?>
      <?php else: ?>
        <p class="wechat-placeholder"><?=e($copy['wechat_placeholder'] ?? '微信二维码占位：将公众号 / 企业微信二维码 URL 写入后台设置 wechat_qr_url，并将账号写入 wechat_id 后即可显示。')?></p>
      <?php endif; ?>
    <?php elseif ($page === 'privacy-policy'): ?>
      <h2><?=e($copy['h2_minimize'] ?? '数据最小化')?></h2>
      <p><?=e($copy['minimize'] ?? '站点访问日志可能包含请求时间、IP 地址、浏览器标识和请求路径，并由服务器用于安全排错。另有自有访问统计（国家/浏览器/页面/行为），不向广告平台共享。管理员访问需要会话 Cookie。本站不提供访客账户注册。')?></p>
      <h2><?=e($copy['h2_third'] ?? '第三方链接')?></h2>
      <p><?=e($copy['third'] ?? '外部网站有各自的隐私政策。打开外部链接前请核对域名，并查看相应服务的条款。标注为「广告 / 商业链接」的外链与本站编辑内容相互独立。')?></p>
    <?php else: ?>
      <h2><?=e($copy['h2_scope'] ?? '内容使用与合规边界')?></h2>
      <p><?=e($copy['scope'] ?? '本站关于网络加密、隧道协议与安全工具的内容仅作技术原理与安全科普说明，不涉及规避监管或违法使用建议。读者应结合自身环境独立判断，不应将通用文章视为对特定系统的审计或保证。')?></p>
      <h2><?=e($copy['h2_updates'] ?? '更新')?></h2>
      <p><?=e($copy['updates'] ?? '本站可能更新页面以修正错误或反映技术变化。继续使用本站即表示你已阅读并理解上述边界说明。')?></p>
    <?php endif; ?>
  </article>
</div>
