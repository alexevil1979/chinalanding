<?php
declare(strict_types=1);

header_remove('Set-Cookie');
header('Cache-Control: public, max-age=3600');
header('Expires: ' . gmdate('D, d M Y H:i:s', time() + 3600) . ' GMT');
header('Pragma: public');

if ($route === 'rss.xml') {
    header('Content-Type: application/rss+xml; charset=utf-8');
    $lang = ['zh' => 'zh-cn', 'en' => 'en', 'ru' => 'ru'][locale()] ?? 'zh-cn';
    echo '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>'.e(t('site_name')).'</title><link>'.e(lurl('/')).'</link><description>'.e(t('default_description')).'</description><language>'.e($lang).'</language>';
    try {
        foreach (query("SELECT title,slug,meta_description,published_at,updated_at FROM articles WHERE status='published' AND published_at<=NOW() ORDER BY published_at DESC LIMIT 30") as $a) {
            $a = localize_article($a);
            echo '<item><title>'.e($a['title']).'</title><link>'.e(lurl('articles/'.$a['slug'])).'</link><guid>'.e(lurl('articles/'.$a['slug'])).'</guid><description>'.e($a['meta_description']).'</description><pubDate>'.date(DATE_RSS, strtotime($a['published_at'])).'</pubDate></item>';
        }
    } catch (Throwable $x) {
    }
    echo '</channel></rss>';
    exit;
}

header('Content-Type: application/xml; charset=utf-8');

if ($route === 'sitemap.xml') {
    echo '<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    echo '<sitemap><loc>'.e(url('sitemap-articles.xml')).'</loc></sitemap>';
    echo '<sitemap><loc>'.e(url('sitemap-categories.xml')).'</loc></sitemap>';
    echo '</sitemapindex>';
    exit;
}

if ($route === 'sitemap-articles.xml') {
    echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">';
    try {
        foreach (query("SELECT slug,updated_at FROM articles WHERE status='published' AND published_at<=NOW() ORDER BY published_at DESC") as $a) {
            $path = 'articles/' . $a['slug'];
            $lastmod = e(date('Y-m-d', strtotime($a['updated_at'])));
            foreach (SUPPORTED_LOCALES as $loc) {
                echo '<url><loc>'.e(locale_url($loc, $path)).'</loc><lastmod>'.$lastmod.'</lastmod>';
                foreach (SUPPORTED_LOCALES as $alt) {
                    $hreflang = ['zh' => 'zh-CN', 'en' => 'en', 'ru' => 'ru'][$alt];
                    echo '<xhtml:link rel="alternate" hreflang="'.$hreflang.'" href="'.e(locale_url($alt, $path)).'"/>';
                }
                echo '<xhtml:link rel="alternate" hreflang="x-default" href="'.e(locale_url('zh', $path)).'"/>';
                echo '</url>';
            }
        }
    } catch (Throwable $x) {
    }
    echo '</urlset>';
    exit;
}

if ($route === 'sitemap-categories.xml') {
    echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">';
    $paths = ['', 'about', 'contact', 'privacy-policy', 'terms', 'tools'];
    try {
        foreach (query('SELECT slug FROM categories ORDER BY id') as $c) {
            $paths[] = 'category/' . $c['slug'];
        }
    } catch (Throwable $x) {
    }
    foreach ($paths as $path) {
        foreach (SUPPORTED_LOCALES as $loc) {
            echo '<url><loc>'.e(locale_url($loc, $path)).'</loc>';
            foreach (SUPPORTED_LOCALES as $alt) {
                $hreflang = ['zh' => 'zh-CN', 'en' => 'en', 'ru' => 'ru'][$alt];
                echo '<xhtml:link rel="alternate" hreflang="'.$hreflang.'" href="'.e(locale_url($alt, $path)).'"/>';
            }
            echo '<xhtml:link rel="alternate" hreflang="x-default" href="'.e(locale_url('zh', $path)).'"/>';
            echo '</url>';
        }
    }
    echo '</urlset>';
    exit;
}

http_response_code(404);
header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');
echo 'Not found';
