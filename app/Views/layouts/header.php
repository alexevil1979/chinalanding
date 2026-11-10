<!doctype html>
<html lang="<?=e(locale_bcp47())?>" dir="<?=e(locale_html_dir())?>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><?=e($title ?? t('site_name'))?></title>
<meta name="description" content="<?=e($description ?? t('default_description'))?>">
<?php
$pageKeywords = trim((string)($keywords ?? ''));
if ($pageKeywords === '') {
    $pageKeywords = t('default_keywords');
}
$canonicalPath = request_path_no_locale();
$canonical = lurl($canonicalPath);
$ogImage = !empty($article['image_url'])
    ? url(ltrim((string)$article['image_url'], '/'))
    : url('assets/og-default.png');
?>
<meta name="keywords" content="<?=e($pageKeywords)?>">
<link rel="canonical" href="<?=e($canonical)?>">
<link rel="alternate" hreflang="zh-CN" href="<?=e(locale_url('zh', $canonicalPath))?>">
<link rel="alternate" hreflang="en" href="<?=e(locale_url('en', $canonicalPath))?>">
<link rel="alternate" hreflang="ru" href="<?=e(locale_url('ru', $canonicalPath))?>">
<link rel="alternate" hreflang="x-default" href="<?=e(locale_url('zh', $canonicalPath))?>">
<meta property="og:site_name" content="<?=e(t('site_name'))?>">
<meta property="og:title" content="<?=e($title ?? t('site_name'))?>">
<meta property="og:description" content="<?=e($description ?? t('default_description'))?>">
<meta property="og:type" content="<?=isset($article) ? 'article' : 'website'?>">
<meta property="og:locale" content="<?=e(str_replace('-', '_', locale_bcp47()))?>">
<meta property="og:locale:alternate" content="zh_CN">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:locale:alternate" content="ru_RU">
<meta name="baidu-site-verification" content="<?=e(setting('baidu_verification'))?>">
<meta name="google-site-verification" content="<?=e(setting('google_verification'))?>">
<meta property="og:url" content="<?=e($canonical)?>">
<meta property="og:image" content="<?=e($ogImage)?>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="<?=e(t('site_name'))?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?=e($title ?? t('site_name'))?>">
<meta name="twitter:description" content="<?=e($description ?? t('default_description'))?>">
<meta name="twitter:image" content="<?=e($ogImage)?>">
<?php
$robotsPath = $canonicalPath;
$robotsMeta = (!empty($robots)) ? $robots : ((str_starts_with($robotsPath, 'search') || str_starts_with($robotsPath, 'admin')) ? 'noindex,follow' : 'index,follow');
?>
<meta name="robots" content="<?=e($robotsMeta)?>">
<meta name="theme-color" content="#0d1f35">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="<?=e(t('rss_title'))?>" href="<?=e(lp('rss.xml'))?>">
<link rel="stylesheet" href="/assets/style.css?v=20261110i18n">
<script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'Organization','name'=>t('site_name'),'url'=>url('/'),'logo'=>url('assets/logo.svg')], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<?php if (empty($article)): ?><script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'WebSite','name'=>t('site_name'),'url'=>lurl('/'),'inLanguage'=>locale_bcp47(),'potentialAction'=>['@type'=>'SearchAction','target'=>lurl('search').'?q={search_term_string}','query-input'=>'required name=search_term_string']], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script><?php endif; ?>
</head>
<body>
<a class="skip-link" href="#main"><?=e(t('skip_to_content'))?></a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="<?=e(lp('/'))?>" aria-label="<?=e(t('brand_aria'))?>">
      <span class="brand-mark" aria-hidden="true">
        <img src="/assets/favicon.svg" width="40" height="40" alt="">
      </span>
      <span class="brand-name"><?=e(t('site_name'))?><small><?=e(t('site_tagline'))?></small></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="<?=e(t('open_menu'))?>" aria-expanded="false"><?=e(t('menu'))?></button>
    <nav class="main-nav" aria-label="<?=e(t('main_nav'))?>">
      <a href="<?=e(lp('/'))?>"><?=e(t('home'))?></a>
      <a href="<?=e(lp('category/network-security'))?>"><?=e(t('nav_network_security'))?></a>
      <a href="<?=e(lp('category/network-privacy'))?>"><?=e(t('nav_network_privacy'))?></a>
      <a href="<?=e(lp('category/account-security'))?>"><?=e(t('nav_account_security'))?></a>
      <a href="<?=e(lp('category/vpn-technology'))?>"><?=e(t('nav_vpn_technology'))?></a>
      <a href="<?=e(lp('category/tutorials'))?>"><?=e(t('nav_tutorials'))?></a>
      <a href="<?=e(lp('tools'))?>"><?=e(t('nav_tools'))?></a>
      <a href="<?=e(lp('about'))?>"><?=e(t('nav_about'))?></a>
    </nav>
    <div class="lang-switch" aria-label="<?=e(t('language'))?>">
      <a class="<?=locale()==='zh'?'is-active':''?>" href="<?=e(switch_locale_url('zh'))?>" hreflang="zh-CN" lang="zh-CN"><?=e(t('lang_zh'))?></a>
      <a class="<?=locale()==='en'?'is-active':''?>" href="<?=e(switch_locale_url('en'))?>" hreflang="en" lang="en"><?=e(t('lang_en'))?></a>
      <a class="<?=locale()==='ru'?'is-active':''?>" href="<?=e(switch_locale_url('ru'))?>" hreflang="ru" lang="ru"><?=e(t('lang_ru'))?></a>
    </div>
    <form class="search-form" action="<?=e(lp('search'))?>" method="get" role="search">
      <label class="sr-only" for="site-search"><?=e(t('search_articles'))?></label>
      <input id="site-search" type="search" name="q" placeholder="<?=e(t('search_placeholder'))?>" value="<?=e($_GET['q']??'')?>">
      <button type="submit" aria-label="<?=e(t('search'))?>">⌕</button>
    </form>
  </div>
</header>
<main id="main">
