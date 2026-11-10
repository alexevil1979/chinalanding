<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><?=e($title ?? '数字安全指南')?></title>
<meta name="description" content="<?=e($description ?? '数字安全指南：网络安全、账户安全、数据加密与合规科普知识。')?>">
<?php
$defaultKeywords='钓鱼识别,双重验证,家庭网络安全,系统更新,账户安全,HTTPS,网络安全,网络加密';
$pageKeywords=trim((string)($keywords ?? ''));
if($pageKeywords==='')$pageKeywords=$defaultKeywords;
?>
<meta name="keywords" content="<?=e($pageKeywords)?>">
<link rel="canonical" href="<?=e(url(trim(parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH),'/')))?>">
<meta property="og:site_name" content="数字安全指南">
<meta property="og:title" content="<?=e($title ?? '数字安全指南')?>">
<meta property="og:description" content="<?=e($description ?? '')?>">
<meta property="og:type" content="<?=isset($article)?'article':'website'?>">
<meta name="baidu-site-verification" content="<?=e(setting('baidu_verification'))?>">
<meta name="google-site-verification" content="<?=e(setting('google_verification'))?>">
<meta property="og:url" content="<?=e(url(trim(parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH),'/')))?>">
<?php if (!empty($article['image_url'])): ?><meta property="og:image" content="<?=e(url(ltrim($article['image_url'],'/')))?>"><?php endif; ?>
<?php
$robotsPath=trim((string)parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH),'/');
$robotsMeta=(!empty($robots))?$robots:((str_starts_with($robotsPath,'search')||str_starts_with($robotsPath,'admin'))?'noindex,follow':'index,follow');
?>
<meta name="robots" content="<?=e($robotsMeta)?>">
<meta name="theme-color" content="#0d1f35">
<link rel="alternate" type="application/rss+xml" title="数字安全指南 RSS" href="/rss.xml">
<link rel="stylesheet" href="/assets/style.css?v=20261110e">
<script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'Organization','name'=>'数字安全指南','url'=>url('/'),'logo'=>url('assets/logo.svg')],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script>
<?php if (empty($article)): ?><script type="application/ld+json"><?=json_encode(['@context'=>'https://schema.org','@type'=>'WebSite','name'=>'数字安全指南','url'=>url('/'),'inLanguage'=>'zh-CN','potentialAction'=>['@type'=>'SearchAction','target'=>url('search').'?q={search_term_string}','query-input'=>'required name=search_term_string']],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?></script><?php endif; ?>
</head>
<body>
<a class="skip-link" href="#main">跳转到正文</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="/" aria-label="数字安全指南首页">
      <span class="brand-mark">DS</span>
      <span class="brand-name">数字安全指南<small>DIGITAL SECURITY GUIDE</small></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="打开导航菜单" aria-expanded="false">菜单</button>
    <nav class="main-nav" aria-label="主导航">
      <a href="/">首页</a>
      <a href="/category/network-security">网络安全</a>
      <a href="/category/network-privacy">网络隐私</a>
      <a href="/category/account-security">账户安全</a>
      <a href="/category/vpn-technology">网络加密</a>
      <a href="/category/tutorials">使用教程</a>
      <a href="/tools">安全工具</a>
      <a href="/about">关于我们</a>
    </nav>
    <form class="search-form" action="/search" method="get" role="search">
      <label class="sr-only" for="site-search">搜索文章</label>
      <input id="site-search" type="search" name="q" placeholder="搜索安全知识…" value="<?=e($_GET['q']??'')?>">
      <button type="submit" aria-label="搜索">⌕</button>
    </form>
  </div>
</header>
<main id="main">
