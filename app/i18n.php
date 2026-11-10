<?php
declare(strict_types=1);

const SUPPORTED_LOCALES = ['zh', 'en', 'ru'];

function locale(): string {
    $loc = $GLOBALS['locale'] ?? 'zh';
    return in_array($loc, SUPPORTED_LOCALES, true) ? $loc : 'zh';
}

function locale_bcp47(): string {
    return ['zh' => 'zh-CN', 'en' => 'en', 'ru' => 'ru'][locale()] ?? 'zh-CN';
}

function locale_html_dir(): string {
    return 'ltr';
}

/** Locale-aware site path, e.g. /en/articles/foo or /articles/foo */
function lp(string $path = ''): string {
    $path = trim($path, '/');
    $loc = locale();
    if ($loc === 'zh') {
        return $path === '' ? '/' : '/' . $path;
    }
    return $path === '' ? '/' . $loc : '/' . $loc . '/' . $path;
}

/** Absolute URL with current locale prefix */
function lurl(string $path = ''): string {
    global $config;
    $base = rtrim($config['site_url'] ?? '', '/');
    $p = lp($path);
    return $base . ($p === '/' ? '/' : $p);
}

/** Absolute URL for a specific locale */
function locale_url(string $loc, string $path = ''): string {
    global $config;
    $base = rtrim($config['site_url'] ?? '', '/');
    $path = trim($path, '/');
    if (!in_array($loc, SUPPORTED_LOCALES, true)) {
        $loc = 'zh';
    }
    if ($loc === 'zh') {
        return $base . ($path === '' ? '/' : '/' . $path);
    }
    return $base . '/' . $loc . ($path === '' ? '' : '/' . $path);
}

/** Current path without locale prefix */
function request_path_no_locale(): string {
    return trim((string)($GLOBALS['route_path'] ?? ''), '/');
}

function switch_locale_url(string $target): string {
    return locale_url($target, request_path_no_locale());
}

function i18n_catalog(): array {
    static $cache = [];
    $loc = locale();
    if (isset($cache[$loc])) {
        return $cache[$loc];
    }
    $file = dirname(__DIR__) . '/lang/' . $loc . '.php';
    $cache[$loc] = is_file($file) ? (require $file) : [];
    return $cache[$loc];
}

function t(string $key, array $replace = []): string {
    $catalog = i18n_catalog();
    $text = $catalog[$key] ?? null;
    if ($text === null && locale() !== 'zh') {
        $zh = dirname(__DIR__) . '/lang/zh.php';
        $fallback = is_file($zh) ? (require $zh) : [];
        $text = $fallback[$key] ?? $key;
    } elseif ($text === null) {
        $text = $key;
    }
    foreach ($replace as $k => $v) {
        $text = str_replace(':' . $k, (string)$v, $text);
    }
    return $text;
}

function load_locale_bundle(string $name): array {
    static $cache = [];
    $loc = locale();
    $key = $loc . ':' . $name;
    if (isset($cache[$key])) {
        return $cache[$key];
    }
    $file = dirname(__DIR__) . '/lang/' . $loc . '/' . $name . '.php';
    $cache[$key] = is_file($file) ? (require $file) : [];
    return $cache[$key];
}

function localize_category(array $cat): array {
    if (locale() === 'zh') {
        if (($cat['name'] ?? '') === 'VPN技术') {
            $cat['name'] = '网络加密技术';
        }
        return $cat;
    }
    $bundle = load_locale_bundle('categories');
    $slug = $cat['slug'] ?? '';
    if ($slug !== '' && isset($bundle[$slug]) && is_array($bundle[$slug])) {
        $tr = $bundle[$slug];
        foreach (['name', 'description', 'seo_title', 'meta_description'] as $field) {
            if (!empty($tr[$field])) {
                $cat[$field] = $tr[$field];
            }
        }
    }
    return $cat;
}

function load_article_translation(string $slug): ?array {
    if (locale() === 'zh' || $slug === '') {
        return null;
    }
    $file = dirname(__DIR__) . '/lang/' . locale() . '/articles/' . $slug . '.php';
    if (!is_file($file)) {
        return null;
    }
    $data = require $file;
    return is_array($data) ? $data : null;
}

function localize_internal_hrefs(string $html): string {
    if (locale() === 'zh' || $html === '') {
        return $html;
    }
    $loc = locale();
    $rewritten = preg_replace_callback(
        '#\bhref=(["\'])/((?:articles|category|tools|about|contact|privacy-policy|terms|search)(?:/[^"\']*)?)?\1#i',
        static function (array $m) use ($loc): string {
            $path = $m[2] ?? '';
            return 'href=' . $m[1] . '/' . $loc . ($path !== '' ? '/' . ltrim($path, '/') : '') . $m[1];
        },
        $html
    );
    return is_string($rewritten) ? $rewritten : $html;
}

function localize_article(array $article): array {
    $tr = load_article_translation((string)($article['slug'] ?? ''));
    if (!$tr) {
        if (locale() !== 'zh' && !empty($article['categories'])) {
            $article['categories'] = localize_category_names((string)$article['categories']);
        } elseif (($article['categories'] ?? '') !== '') {
            $article['categories'] = str_replace('VPN技术', '网络加密技术', (string)$article['categories']);
        }
        if (!empty($article['category_name'])) {
            $article['category_name'] = localize_category_names((string)$article['category_name']);
        }
        return $article;
    }
    foreach (['title', 'seo_title', 'meta_description', 'content_html', 'faq_json', 'image_alt'] as $field) {
        if (array_key_exists($field, $tr) && $tr[$field] !== null && $tr[$field] !== '') {
            $article[$field] = $tr[$field];
        }
    }
    if (!empty($article['content_html'])) {
        $article['content_html'] = localize_internal_hrefs((string)$article['content_html']);
    }
    if (!empty($article['categories'])) {
        $article['categories'] = localize_category_names((string)$article['categories']);
    }
    if (!empty($article['category_name'])) {
        $article['category_name'] = localize_category_names((string)$article['category_name']);
    }
    return $article;
}

function localize_category_names(string $names): string {
    if (locale() === 'zh') {
        return str_replace('VPN技术', '网络加密技术', $names);
    }
    $bundle = load_locale_bundle('categories');
    $map = [];
    foreach ($bundle as $slug => $row) {
        if (!empty($row['name_zh']) && !empty($row['name'])) {
            $map[$row['name_zh']] = $row['name'];
        }
        if (!empty($row['name']) && is_string($slug)) {
            // also map common ZH labels
        }
    }
    // built-in ZH→locale map from category bundle name_zh
    $parts = preg_split('/[、,]/u', $names) ?: [];
    $out = [];
    foreach ($parts as $part) {
        $part = trim($part);
        if ($part === '') {
            continue;
        }
        $replaced = $part;
        foreach ($bundle as $row) {
            if (!empty($row['name_zh']) && $row['name_zh'] === $part && !empty($row['name'])) {
                $replaced = $row['name'];
                break;
            }
        }
        if ($replaced === 'VPN技术' || $replaced === '网络加密技术') {
            foreach ($bundle as $slug => $row) {
                if ($slug === 'vpn-technology' && !empty($row['name'])) {
                    $replaced = $row['name'];
                    break;
                }
            }
        }
        $out[] = $replaced;
    }
    return implode(locale() === 'ru' ? ', ' : ', ', $out);
}

function localize_articles(array $articles): array {
    return array_map('localize_article', $articles);
}

function static_page_copy(string $page): array {
    $bundle = load_locale_bundle('pages');
    return is_array($bundle[$page] ?? null) ? $bundle[$page] : [];
}
