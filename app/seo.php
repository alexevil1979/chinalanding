<?php
declare(strict_types=1);

header_remove('Set-Cookie');
header('Cache-Control: public, max-age=3600');
header('Expires: ' . gmdate('D, d M Y H:i:s', time() + 3600) . ' GMT');
header('Pragma: public');

if ($route === 'rss.xml') {
    header('Content-Type: application/rss+xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>数字安全指南</title><link>'.e(url('/')).'</link><description>网络安全、数字隐私与现代网络技术</description><language>zh-cn</language>';
    try { foreach(query("SELECT title,slug,meta_description,published_at,updated_at FROM articles WHERE status='published' AND published_at<=NOW() ORDER BY published_at DESC LIMIT 30") as $a) echo '<item><title>'.e($a['title']).'</title><link>'.e(url('articles/'.$a['slug'])).'</link><guid>'.e(url('articles/'.$a['slug'])).'</guid><description>'.e($a['meta_description']).'</description><pubDate>'.date(DATE_RSS,strtotime($a['published_at'])).'</pubDate></item>'; } catch(Throwable $x){}
    echo '</channel></rss>'; exit;
}
header('Content-Type: application/xml; charset=utf-8');
if ($route === 'sitemap.xml') {
 echo '<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>'.e(url('sitemap-articles.xml')).'</loc></sitemap><sitemap><loc>'.e(url('sitemap-categories.xml')).'</loc></sitemap></sitemapindex>'; exit;
}
if ($route === 'sitemap-articles.xml') {
 echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
 try { foreach(query("SELECT slug,updated_at FROM articles WHERE status='published' AND published_at<=NOW() ORDER BY published_at DESC") as $a) echo '<url><loc>'.e(url('articles/'.$a['slug'])).'</loc><lastmod>'.e(date('Y-m-d',strtotime($a['updated_at']))).'</lastmod></url>'; } catch(Throwable $x){}
 echo '</urlset>'; exit;
}
if ($route === 'sitemap-categories.xml') {
 echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
 try { echo '<url><loc>'.e(url('/')).'</loc></url>'; foreach(['about','contact','privacy-policy','terms','tools'] as $p) echo '<url><loc>'.e(url($p)).'</loc></url>'; foreach(query('SELECT slug FROM categories ORDER BY id') as $c) echo '<url><loc>'.e(url('category/'.$c['slug'])).'</loc></url>'; } catch(Throwable $x){}
 echo '</urlset>'; exit;
}
http_response_code(404); header('Content-Type: text/plain; charset=utf-8'); header('Cache-Control: no-store'); echo 'Not found';
