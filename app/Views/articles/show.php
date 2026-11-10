<?php
$catSlugs=explode(',',(string)($article['category_slugs']??''));
$firstSlug=$catSlugs[0]??'';
$catNamesRaw=(string)($article['categories']??'网络安全');
$catNames=str_replace('VPN技术','网络加密技术',$catNamesRaw);
$readMinutes=max(1,(int)ceil(mb_strlen(strip_tags($article['content_html']),'UTF-8')/450));
$related=!empty($article['id'])?query("SELECT a.slug,a.title,a.meta_description,a.published_at FROM articles a WHERE a.id<>? AND a.status='published' AND a.published_at<=NOW() AND EXISTS(SELECT 1 FROM article_category x WHERE x.article_id=a.id AND x.category_id IN (SELECT category_id FROM article_category WHERE article_id=?)) ORDER BY a.published_at DESC LIMIT 5",[$article['id'],$article['id']]):[];
$faqs=json_decode($article['faq_json']??'[]',true)?:[];
$sources=json_decode($article['sources_json']??'[]',true)?:[];
$cover=$article['image_url']??'';
$sensitiveSlugs=['what-is-vpn','vpn-vs-proxy','what-is-wireguard','what-is-vless','what-is-dns-leak','network-traffic-encryption','choose-privacy-tools'];
$isSensitive=in_array($article['slug']??'',$sensitiveSlugs,true) || in_array('vpn-technology',$catSlugs,true);
$bodyHtml=strip_hiddifysales_html(sanitize_article_html($article['content_html']));
if($isSensitive){
  $bodyHtml=preg_replace('~<p>\s*(?:<strong>)?编辑说明：?(?:</strong>)?.*?</p>~iu','',$bodyHtml,1)??$bodyHtml;
}
$practiceLinks=[
  ['href'=>'/articles/protect-online-accounts','label'=>'如何保护在线账户'],
  ['href'=>'/articles/identify-phishing-attacks','label'=>'如何识别网络钓鱼'],
  ['href'=>'/articles/what-is-https','label'=>'什么是 HTTPS'],
  ['href'=>'/articles/two-factor-authentication-guide','label'=>'双重身份验证指南'],
];
?>
<div class="container page-stack">
  <div class="article-layout">
    <article class="article-main">
      <nav class="breadcrumbs" aria-label="面包屑">
        <a href="/">首页</a><span>›</span>
        <?php if($firstSlug): ?>
          <a href="/category/<?=e($firstSlug)?>"><?=e(explode('、',$catNames)[0])?></a><span>›</span>
        <?php endif; ?>
        <span><?=e($article['title'])?></span>
      </nav>
      <header class="article-head">
        <p class="meta"><?=e($catNames)?> <span>·</span> <?=e(substr($article['published_at'],0,10))?></p>
        <h1><?=e($article['title'])?></h1>
        <p class="article-dek"><?=e($article['meta_description'])?></p>
        <div class="article-byline">
          <span>数字安全指南编辑部</span>
          <span>发布于 <?=e(substr($article['published_at'],0,10))?></span>
          <span>更新于 <?=e(substr($article['updated_at'],0,10))?></span>
          <span>约 <?=$readMinutes?> 分钟阅读</span>
        </div>
      </header>
      <?php if($cover): ?>
        <figure class="article-cover real-cover"><img src="<?=e($cover)?>" alt="<?=e($article['image_alt']??$article['title'])?>" fetchpriority="high"></figure>
      <?php else: ?>
        <div class="article-cover" role="img" aria-label="<?=e($article['title'])?>抽象主题图"><span>DS</span></div>
      <?php endif; ?>
      <details class="toc-box" open><summary>本文目录</summary><nav data-toc aria-label="文章目录"></nav></details>
      <?php if($isSensitive): ?>
        <aside class="editor-note" role="note">
          <p><strong>编辑说明：</strong>本文仅供技术学习与网络安全科普，聚焦协议原理、威胁模型与企业远程接入边界，不构成规避监管或违法使用网络服务的指导。</p>
        </aside>
      <?php endif; ?>
      <div class="article-content"><?=$bodyHtml?></div>
      <aside class="compliance-note" role="note">
        <p>本文仅作技术原理与网络安全科普说明，不构成规避监管、违法使用网络服务或任何违法行为的指导；请遵守中华人民共和国法律法规及相关政策。</p>
      </aside>
      <?php if($isSensitive): ?>
        <section class="practice-links">
          <h2>相关安全实践</h2>
          <p>在了解协议原理之外，建议先巩固这些低风险、高收益的日常安全习惯：</p>
          <ul>
            <?php foreach($practiceLinks as $link): ?>
              <li><a href="<?=e($link['href'])?>"><?=e($link['label'])?></a></li>
            <?php endforeach; ?>
          </ul>
        </section>
      <?php endif; ?>
      <?php if($faqs): ?>
        <section>
          <h2>常见问题</h2>
          <div class="faq-list">
            <?php foreach($faqs as $faq): ?>
              <details><summary><?=e($faq['q'])?></summary><p><?=e($faq['a'])?></p></details>
            <?php endforeach; ?>
          </div>
        </section>
      <?php endif; ?>
      <section>
        <h2>进一步阅读与官方资料</h2>
        <?php if($sources): ?>
          <ul class="source-list">
            <?php foreach($sources as $source): ?>
              <li><a href="<?=e($source['url'])?>" rel="noopener" target="_blank"><?=e($source['title']?:$source['url'])?></a></li>
            <?php endforeach; ?>
          </ul>
        <?php else: ?>
          <p>建议结合相关软件、服务或协议的官方文档核对操作细节。</p>
        <?php endif; ?>
      </section>
      <section>
        <h2>相关文章</h2>
        <div class="related-list">
          <?php foreach($related as $r): ?>
            <article class="search-result">
              <p class="meta"><?=e(substr($r['published_at'],0,10))?></p>
              <h3><a href="/articles/<?=e($r['slug'])?>"><?=e($r['title'])?></a></h3>
              <p><?=e($r['meta_description'])?></p>
            </article>
          <?php endforeach; ?>
        </div>
      </section>
      <div class="tool-callout">
        <div>
          <p class="eyebrow">继续阅读</p>
          <h2>网络加密与安全工具</h2>
          <p>继续阅读协议与工具专题。若进入商业站点，链接会标注为「广告 / 商业链接」。</p>
        </div>
        <a href="/tools">打开工具专题 ↗</a>
      </div>
    </article>
    <aside class="article-sidebar">
      <h2>相关阅读</h2>
      <?php foreach($related as $r): ?>
        <a href="/articles/<?=e($r['slug'])?>"><?=e($r['title'])?><span><?=e(substr($r['published_at'],0,10))?></span></a>
      <?php endforeach; ?>
    </aside>
  </div>
</div>
<?php
$datePublished=date('c',strtotime((string)$article['published_at']));
$dateModified=date('c',strtotime((string)$article['updated_at']));
$articleSchema=['@context'=>'https://schema.org','@type'=>'Article','headline'=>$article['title'],'description'=>$article['meta_description'],'inLanguage'=>'zh-CN','datePublished'=>$datePublished,'dateModified'=>$dateModified,'author'=>['@type'=>'Organization','name'=>'数字安全指南编辑部'],'publisher'=>['@type'=>'Organization','name'=>'数字安全指南','url'=>url('/'),'logo'=>['@type'=>'ImageObject','url'=>url('assets/logo.svg')]],'mainEntityOfPage'=>['@type'=>'WebPage','@id'=>url('articles/'.$article['slug'])]];
if($cover)$articleSchema['image']=[url(ltrim((string)$cover,'/'))];
$crumb=['@context'=>'https://schema.org','@type'=>'BreadcrumbList','itemListElement'=>[['@type'=>'ListItem','position'=>1,'name'=>'首页','item'=>url('/')]]];
if($firstSlug)$crumb['itemListElement'][]=['@type'=>'ListItem','position'=>2,'name'=>explode('、',$catNames)[0],'item'=>url('category/'.$firstSlug)];
$crumb['itemListElement'][]=['@type'=>'ListItem','position'=>count($crumb['itemListElement'])+1,'name'=>$article['title'],'item'=>url('articles/'.$article['slug'])];
?>
<script type="application/ld+json"><?=json_encode($articleSchema,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<script type="application/ld+json"><?=json_encode($crumb,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<?php if($faqs): ?><script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'FAQPage','mainEntity'=>array_map(static fn($f)=>['@type'=>'Question','name'=>$f['q'],'acceptedAnswer'=>['@type'=>'Answer','text'=>$f['a']]],$faqs)],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script><?php endif; ?>
