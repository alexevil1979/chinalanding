<?php
declare(strict_types=1);

header_remove('Set-Cookie');
header('Cache-Control: public, max-age=3600');
header('Expires: ' . gmdate('D, d M Y H:i:s', time() + 3600) . ' GMT');
header('Pragma: public');

if ($route === 'robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    $sitemap = url('sitemap.xml');
    echo "User-agent: *\n";
    echo "Allow: /\n";
    echo "Allow: /assets/\n";
    echo "Allow: /en/\n";
    echo "Allow: /ru/\n";
    echo "Disallow: /admin/\n";
    echo "Disallow: /analytics/\n";
    echo "Disallow: /search?\n";
    echo "\n";
    echo "User-agent: Googlebot\n";
    echo "Allow: /\n";
    echo "Disallow: /admin/\n";
    echo "Disallow: /analytics/\n";
    echo "\n";
    echo "User-agent: Googlebot-Image\n";
    echo "Allow: /assets/\n";
    echo "Allow: /uploads/\n";
    echo "\n";
    echo "Sitemap: {$sitemap}\n";
    exit;
}

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
    echo '<sitemap><loc>'.e(url('sitemap-pages.xml')).'</loc></sitemap>';
    echo '<sitemap><loc>'.e(url('sitemap-articles.xml')).'</loc></sitemap>';
    echo '<sitemap><loc>'.e(url('sitemap-categories.xml')).'</loc></sitemap>';
    echo '</sitemapindex>';
    exit;
}

$hreflangLinks = static function (string $path): string {
    $out = '';
    foreach (SUPPORTED_LOCALES as $alt) {
        $hreflang = ['zh' => 'zh-CN', 'en' => 'en', 'ru' => 'ru'][$alt];
        $out .= '<xhtml:link rel="alternate" hreflang="'.$hreflang.'" href="'.e(locale_url($alt, $path)).'"/>';
    }
    $out .= '<xhtml:link rel="alternate" hreflang="x-default" href="'.e(locale_url('zh', $path)).'"/>';
    return $out;
};

if ($route === 'sitemap-pages.xml') {
    echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">';
    $pages = [
        '' => '1.0',
        'tools' => '0.8',
        'about' => '0.5',
        'contact' => '0.4',
        'privacy-policy' => '0.3',
        'terms' => '0.3',
    ];
    $today = date('Y-m-d');
    foreach ($pages as $path => $priority) {
        foreach (SUPPORTED_LOCALES as $loc) {
            echo '<url><loc>'.e(locale_url($loc, $path)).'</loc><lastmod>'.$today.'</lastmod><changefreq>weekly</changefreq><priority>'.$priority.'</priority>';
            echo $hreflangLinks($path);
            echo '</url>';
        }
    }
    echo '</urlset>';
    exit;
}

if ($route === 'sitemap-articles.xml') {
    echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">';
    try {
        foreach (query("SELECT slug,updated_at,published_at FROM articles WHERE status='published' AND published_at<=NOW() ORDER BY published_at DESC") as $a) {
            $path = 'articles/' . $a['slug'];
            $lastmod = e(date('Y-m-d', strtotime((string)($a['updated_at'] ?: $a['published_at']))));
            foreach (SUPPORTED_LOCALES as $loc) {
                echo '<url><loc>'.e(locale_url($loc, $path)).'</loc><lastmod>'.$lastmod.'</lastmod><changefreq>monthly</changefreq><priority>0.8</priority>';
                echo $hreflangLinks($path);
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
    $paths = [];
    try {
        foreach (query('SELECT slug FROM categories ORDER BY id') as $c) {
            $paths[] = 'category/' . $c['slug'];
        }
    } catch (Throwable $x) {
    }
    $today = date('Y-m-d');
    foreach ($paths as $path) {
        foreach (SUPPORTED_LOCALES as $loc) {
            echo '<url><loc>'.e(locale_url($loc, $path)).'</loc><lastmod>'.$today.'</lastmod><changefreq>weekly</changefreq><priority>0.7</priority>';
            echo $hreflangLinks($path);
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
