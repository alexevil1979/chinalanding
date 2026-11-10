<?php
declare(strict_types=1);

function analytics_ensure_tables(): void
{
    static $ready = false;
    if ($ready) {
        return;
    }
    db()->exec(
        "CREATE TABLE IF NOT EXISTS analytics_pageviews (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          visitor_id CHAR(32) NOT NULL,
          session_id CHAR(32) NOT NULL,
          path VARCHAR(500) NOT NULL,
          page_type VARCHAR(40) NOT NULL DEFAULT 'page',
          article_slug VARCHAR(180) NULL,
          locale CHAR(5) NOT NULL DEFAULT 'zh',
          referrer_host VARCHAR(255) NULL,
          country CHAR(2) NOT NULL DEFAULT 'XX',
          browser VARCHAR(40) NOT NULL DEFAULT 'Other',
          os VARCHAR(40) NOT NULL DEFAULT 'Other',
          device VARCHAR(20) NOT NULL DEFAULT 'desktop',
          is_bot TINYINT(1) NOT NULL DEFAULT 0,
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          KEY idx_created (created_at),
          KEY idx_country_created (country, created_at),
          KEY idx_path_created (path(191), created_at),
          KEY idx_visitor_created (visitor_id, created_at),
          KEY idx_session_created (session_id, created_at),
          KEY idx_bot_created (is_bot, created_at),
          KEY idx_type_created (page_type, created_at),
          KEY idx_article_created (article_slug, created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
    );
    db()->exec(
        "CREATE TABLE IF NOT EXISTS analytics_events (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          visitor_id CHAR(32) NOT NULL,
          session_id CHAR(32) NOT NULL,
          event_name VARCHAR(60) NOT NULL,
          event_value VARCHAR(255) NULL,
          path VARCHAR(500) NOT NULL,
          locale CHAR(5) NOT NULL DEFAULT 'zh',
          country CHAR(2) NOT NULL DEFAULT 'XX',
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          KEY idx_created (created_at),
          KEY idx_name_created (event_name, created_at),
          KEY idx_visitor_created (visitor_id, created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
    );
    $ready = true;
}

function analytics_client_ip(): string
{
    $candidates = [
        $_SERVER['HTTP_CF_CONNECTING_IP'] ?? '',
        $_SERVER['HTTP_TRUE_CLIENT_IP'] ?? '',
        $_SERVER['HTTP_X_REAL_IP'] ?? '',
        '',
    ];
    $xff = (string)($_SERVER['HTTP_X_FORWARDED_FOR'] ?? '');
    if ($xff !== '') {
        $candidates[3] = trim(explode(',', $xff)[0]);
    }
    $candidates[] = (string)($_SERVER['REMOTE_ADDR'] ?? '');
    foreach ($candidates as $ip) {
        $ip = trim((string)$ip);
        if ($ip !== '' && filter_var($ip, FILTER_VALIDATE_IP)) {
            return $ip;
        }
    }
    return '0.0.0.0';
}

function analytics_country_code(): string
{
    $headers = [
        'HTTP_CF_IPCOUNTRY',
        'HTTP_CLOUDFRONT_VIEWER_COUNTRY',
        'HTTP_X_COUNTRY_CODE',
        'HTTP_X_APPENGINE_COUNTRY',
        'HTTP_X_GEO_COUNTRY',
    ];
    foreach ($headers as $h) {
        $v = strtoupper(trim((string)($_SERVER[$h] ?? '')));
        if (preg_match('/^[A-Z]{2}$/', $v) && $v !== 'XX' && $v !== 'T1') {
            return $v;
        }
    }
    $ip = analytics_client_ip();
    if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
        return 'LO';
    }
    return 'XX';
}

function analytics_parse_ua(?string $ua): array
{
    $ua = $ua ?? '';
    $bot = (bool)preg_match('/bot|spider|crawl|slurp|facebookexternalhit|preview|wget|curl|python-requests|httpclient|scrapy|semrush|ahrefs|bingpreview|yandex|baidu|sogou|bytespider|petalbot|duckduck|gptbot|claudebot|anthropic/i', $ua);

    $browser = 'Other';
    if (preg_match('/Edg(?:e|A|iOS)?\/([\d.]+)/i', $ua)) {
        $browser = 'Edge';
    } elseif (preg_match('/OPR\/|Opera/i', $ua)) {
        $browser = 'Opera';
    } elseif (preg_match('/SamsungBrowser/i', $ua)) {
        $browser = 'Samsung';
    } elseif (preg_match('/UCBrowser|UCWEB/i', $ua)) {
        $browser = 'UC';
    } elseif (preg_match('/MicroMessenger/i', $ua)) {
        $browser = 'WeChat';
    } elseif (preg_match('/QQ\//i', $ua)) {
        $browser = 'QQ';
    } elseif (preg_match('/Chrome\/([\d.]+)/i', $ua) && !preg_match('/Chromium/i', $ua)) {
        $browser = 'Chrome';
    } elseif (preg_match('/Firefox\/([\d.]+)/i', $ua)) {
        $browser = 'Firefox';
    } elseif (preg_match('/Safari\/([\d.]+)/i', $ua) && preg_match('/Version\//i', $ua)) {
        $browser = 'Safari';
    } elseif (preg_match('/MSIE |Trident\//i', $ua)) {
        $browser = 'IE';
    }

    $os = 'Other';
    if (preg_match('/Windows NT/i', $ua)) {
        $os = 'Windows';
    } elseif (preg_match('/Android/i', $ua)) {
        $os = 'Android';
    } elseif (preg_match('/iPhone|iPad|iPod/i', $ua)) {
        $os = 'iOS';
    } elseif (preg_match('/Mac OS X/i', $ua)) {
        $os = 'macOS';
    } elseif (preg_match('/Linux/i', $ua)) {
        $os = 'Linux';
    } elseif (preg_match('/HarmonyOS|OpenHarmony/i', $ua)) {
        $os = 'HarmonyOS';
    }

    $device = 'desktop';
    if (preg_match('/iPad|Tablet|PlayBook/i', $ua) || (preg_match('/Android/i', $ua) && !preg_match('/Mobile/i', $ua))) {
        $device = 'tablet';
    } elseif (preg_match('/Mobile|iPhone|Android.*Mobile|Windows Phone/i', $ua)) {
        $device = 'mobile';
    }

    return ['browser' => $browser, 'os' => $os, 'device' => $device, 'is_bot' => $bot ? 1 : 0];
}

function analytics_cookie_id(string $name, int $ttlSeconds): string
{
    $existing = preg_replace('/[^a-f0-9]/', '', strtolower((string)($_COOKIE[$name] ?? ''))) ?? '';
    if (strlen($existing) === 32) {
        return $existing;
    }
    $id = bin2hex(random_bytes(16));
    $secure = !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off';
    setcookie($name, $id, [
        'expires' => time() + $ttlSeconds,
        'path' => '/',
        'secure' => $secure,
        'httponly' => false,
        'samesite' => 'Lax',
    ]);
    $_COOKIE[$name] = $id;
    return $id;
}

function analytics_ids(): array
{
    return [
        'visitor_id' => analytics_cookie_id('aq_vid', 365 * 24 * 3600),
        'session_id' => analytics_cookie_id('aq_sid', 30 * 60),
    ];
}

function analytics_referrer_host(): ?string
{
    $ref = trim((string)($_SERVER['HTTP_REFERER'] ?? ''));
    if ($ref === '') {
        return null;
    }
    $host = parse_url($ref, PHP_URL_HOST);
    if (!is_string($host) || $host === '') {
        return null;
    }
    $self = parse_url((string)($GLOBALS['config']['site_url'] ?? ''), PHP_URL_HOST);
    if (is_string($self) && strcasecmp($host, $self) === 0) {
        return null;
    }
    return strtolower($host);
}

function analytics_classify_path(string $path): array
{
    $path = trim($path, '/');
    if ($path === '') {
        return ['page_type' => 'home', 'article_slug' => null];
    }
    if (preg_match('#^articles/([a-z0-9-]+)$#', $path, $m)) {
        return ['page_type' => 'article', 'article_slug' => $m[1]];
    }
    if (preg_match('#^category/([a-z0-9-]+)$#', $path, $m)) {
        return ['page_type' => 'category', 'article_slug' => null];
    }
    if ($path === 'search') {
        return ['page_type' => 'search', 'article_slug' => null];
    }
    if ($path === 'tools') {
        return ['page_type' => 'tools', 'article_slug' => null];
    }
    if (in_array($path, ['about', 'contact', 'privacy-policy', 'terms'], true)) {
        return ['page_type' => 'static', 'article_slug' => null];
    }
    return ['page_type' => 'page', 'article_slug' => null];
}

function analytics_should_track_request(): bool
{
    $route = (string)($GLOBALS['route_path'] ?? '');
    if ($route === '' && (($GLOBALS['route_path'] ?? null) === null)) {
        return false;
    }
    if (str_starts_with($route, 'admin')) {
        return false;
    }
    if ($route === 'analytics/collect') {
        return false;
    }
    if (str_ends_with($route, '.xml')) {
        return false;
    }
    $method = strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? 'GET'));
    if ($method !== 'GET' && $method !== 'HEAD') {
        return false;
    }
    return true;
}

function analytics_track_pageview(?string $path = null, ?string $locale = null): void
{
    try {
        if (!analytics_should_track_request()) {
            return;
        }
        analytics_ensure_tables();
        $ids = analytics_ids();
        $path = $path ?? ('/' . ltrim((string)($GLOBALS['route_path'] ?? ''), '/'));
        if ($path === '/') {
            $path = '/';
        }
        $meta = analytics_classify_path(ltrim($path, '/'));
        $ua = analytics_parse_ua($_SERVER['HTTP_USER_AGENT'] ?? '');
        $stmt = db()->prepare(
            'INSERT INTO analytics_pageviews
            (visitor_id, session_id, path, page_type, article_slug, locale, referrer_host, country, browser, os, device, is_bot)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
        );
        $stmt->execute([
            $ids['visitor_id'],
            $ids['session_id'],
            mb_substr($path, 0, 500),
            $meta['page_type'],
            $meta['article_slug'],
            mb_substr($locale ?? (string)($GLOBALS['locale'] ?? 'zh'), 0, 5),
            analytics_referrer_host(),
            analytics_country_code(),
            $ua['browser'],
            $ua['os'],
            $ua['device'],
            $ua['is_bot'],
        ]);
    } catch (Throwable $e) {
        error_log('[analytics] pageview: ' . $e->getMessage());
    }
}

function analytics_track_event(string $name, ?string $value, string $path, string $locale): void
{
    $name = preg_replace('/[^a-z0-9_\-]/', '', strtolower($name)) ?? '';
    if ($name === '' || strlen($name) > 60) {
        return;
    }
    $allowed = [
        'outbound_click', 'search', 'lang_switch', 'scroll_depth',
        'cta_click', 'menu_open', 'share_click', 'toc_click',
    ];
    if (!in_array($name, $allowed, true)) {
        return;
    }
    analytics_ensure_tables();
    $ids = analytics_ids();
    $ua = analytics_parse_ua($_SERVER['HTTP_USER_AGENT'] ?? '');
    if ($ua['is_bot']) {
        return;
    }
    $stmt = db()->prepare(
        'INSERT INTO analytics_events
        (visitor_id, session_id, event_name, event_value, path, locale, country)
        VALUES (?,?,?,?,?,?,?)'
    );
    $stmt->execute([
        $ids['visitor_id'],
        $ids['session_id'],
        $name,
        $value !== null ? mb_substr($value, 0, 255) : null,
        mb_substr($path !== '' ? $path : '/', 0, 500),
        mb_substr($locale !== '' ? $locale : 'zh', 0, 5),
        analytics_country_code(),
    ]);
}

function analytics_collect_beacon(): void
{
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    if (strtoupper((string)($_SERVER['REQUEST_METHOD'] ?? '')) !== 'POST') {
        http_response_code(405);
        echo '{"ok":false}';
        return;
    }
    $origin = (string)($_SERVER['HTTP_ORIGIN'] ?? '');
    $site = rtrim((string)($GLOBALS['config']['site_url'] ?? ''), '/');
    if ($origin !== '' && $site !== '' && stripos($origin, parse_url($site, PHP_URL_HOST) ?: '') === false) {
        // allow missing Origin (same-site navigations / sendBeacon quirks) but block clear cross-site
        $host = parse_url($site, PHP_URL_HOST);
        if (is_string($host) && $host !== '' && !str_contains(strtolower($origin), strtolower($host))) {
            http_response_code(403);
            echo '{"ok":false}';
            return;
        }
    }
    $raw = file_get_contents('php://input') ?: '';
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        $data = $_POST;
    }
    $events = $data['events'] ?? null;
    if (!is_array($events)) {
        $events = [[
            'name' => $data['name'] ?? '',
            'value' => $data['value'] ?? null,
            'path' => $data['path'] ?? '/',
            'locale' => $data['locale'] ?? 'zh',
        ]];
    }
    $count = 0;
    try {
        foreach (array_slice($events, 0, 20) as $ev) {
            if (!is_array($ev)) {
                continue;
            }
            analytics_track_event(
                (string)($ev['name'] ?? ''),
                isset($ev['value']) ? (string)$ev['value'] : null,
                (string)($ev['path'] ?? '/'),
                (string)($ev['locale'] ?? 'zh')
            );
            $count++;
        }
        echo json_encode(['ok' => true, 'n' => $count], JSON_UNESCAPED_UNICODE);
    } catch (Throwable $e) {
        error_log('[analytics] beacon: ' . $e->getMessage());
        http_response_code(500);
        echo '{"ok":false}';
    }
}

function analytics_period_start(string $range): string
{
    $days = match ($range) {
        'today' => 0,
        '7d' => 6,
        '90d' => 89,
        default => 29,
    };
    if ($days === 0) {
        return date('Y-m-d 00:00:00');
    }
    return date('Y-m-d 00:00:00', strtotime('-' . $days . ' days'));
}

function analytics_country_name(string $code): string
{
    static $map = [
        'CN' => '中国', 'HK' => '香港', 'TW' => '台湾', 'MO' => '澳门',
        'RU' => '俄罗斯', 'US' => '美国', 'JP' => '日本', 'KR' => '韩国',
        'SG' => '新加坡', 'DE' => '德国', 'GB' => '英国', 'FR' => '法国',
        'CA' => '加拿大', 'AU' => '澳大利亚', 'IN' => '印度', 'BR' => '巴西',
        'NL' => '荷兰', 'TR' => '土耳其', 'UA' => '乌克兰', 'KZ' => '哈萨克斯坦',
        'BY' => '白俄罗斯', 'UZ' => '乌兹别克斯坦', 'TH' => '泰国', 'VN' => '越南',
        'MY' => '马来西亚', 'ID' => '印度尼西亚', 'PH' => '菲律宾', 'AE' => '阿联酋',
        'SA' => '沙特', 'IT' => '意大利', 'ES' => '西班牙', 'PL' => '波兰',
        'SE' => '瑞典', 'FI' => '芬兰', 'NO' => '挪威', 'CH' => '瑞士',
        'AT' => '奥地利', 'BE' => '比利时', 'IE' => '爱尔兰', 'NZ' => '新西兰',
        'MX' => '墨西哥', 'AR' => '阿根廷', 'CL' => '智利', 'ZA' => '南非',
        'EG' => '埃及', 'IL' => '以色列', 'IR' => '伊朗', 'PK' => '巴基斯坦',
        'BD' => '孟加拉', 'NG' => '尼日利亚', 'KE' => '肯尼亚', 'RO' => '罗马尼亚',
        'CZ' => '捷克', 'HU' => '匈牙利', 'PT' => '葡萄牙', 'GR' => '希腊',
        'LO' => '本地/内网', 'XX' => '未知',
    ];
    $code = strtoupper($code);
    return ($map[$code] ?? $code) . ($code !== 'XX' && $code !== 'LO' ? " ({$code})" : '');
}

function analytics_dashboard(string $range = '30d'): array
{
    analytics_ensure_tables();
    $since = analytics_period_start($range);
    $humans = 'is_bot=0 AND created_at>=?';

    $q = db()->prepare("SELECT COUNT(*) FROM analytics_pageviews WHERE {$humans}");
    $q->execute([$since]);
    $pageviews = (int)$q->fetchColumn();

    $q = db()->prepare("SELECT COUNT(DISTINCT visitor_id) FROM analytics_pageviews WHERE {$humans}");
    $q->execute([$since]);
    $visitors = (int)$q->fetchColumn();

    $q = db()->prepare("SELECT COUNT(DISTINCT session_id) FROM analytics_pageviews WHERE {$humans}");
    $q->execute([$since]);
    $sessions = (int)$q->fetchColumn();

    $q = db()->prepare(
        "SELECT COUNT(*) FROM (
            SELECT session_id FROM analytics_pageviews WHERE {$humans} GROUP BY session_id HAVING COUNT(*)=1
         ) b"
    );
    $q->execute([$since]);
    $bounces = (int)$q->fetchColumn();
    $bounceRate = $sessions > 0 ? round($bounces * 100 / $sessions, 1) : 0.0;

    $q = db()->prepare(
        "SELECT DATE(created_at) d, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
         FROM analytics_pageviews WHERE {$humans}
         GROUP BY DATE(created_at) ORDER BY d ASC"
    );
    $q->execute([$since]);
    $daily = $q->fetchAll();

    $top = static function (string $sql, array $params) {
        $q = db()->prepare($sql);
        $q->execute($params);
        return $q->fetchAll();
    };

    return [
        'range' => $range,
        'since' => $since,
        'kpis' => [
            'pageviews' => $pageviews,
            'visitors' => $visitors,
            'sessions' => $sessions,
            'bounce_rate' => $bounceRate,
            'events' => (int)(function () use ($since) {
                $q = db()->prepare('SELECT COUNT(*) FROM analytics_events WHERE created_at>=?');
                $q->execute([$since]);
                return $q->fetchColumn();
            })(),
        ],
        'daily' => $daily,
        'pages' => $top(
            "SELECT path, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY path ORDER BY views DESC LIMIT 20",
            [$since]
        ),
        'articles' => $top(
            "SELECT article_slug, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans} AND page_type='article' AND article_slug IS NOT NULL
             GROUP BY article_slug ORDER BY views DESC LIMIT 15",
            [$since]
        ),
        'countries' => $top(
            "SELECT country, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY country ORDER BY views DESC LIMIT 20",
            [$since]
        ),
        'browsers' => $top(
            "SELECT browser, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY browser ORDER BY views DESC LIMIT 12",
            [$since]
        ),
        'os' => $top(
            "SELECT os, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY os ORDER BY views DESC LIMIT 12",
            [$since]
        ),
        'devices' => $top(
            "SELECT device, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY device ORDER BY views DESC LIMIT 6",
            [$since]
        ),
        'locales' => $top(
            "SELECT locale, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY locale ORDER BY views DESC LIMIT 10",
            [$since]
        ),
        'referrers' => $top(
            "SELECT referrer_host, COUNT(*) views, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_pageviews WHERE {$humans} AND referrer_host IS NOT NULL AND referrer_host<>''
             GROUP BY referrer_host ORDER BY views DESC LIMIT 15",
            [$since]
        ),
        'events' => $top(
            'SELECT event_name, COUNT(*) total, COUNT(DISTINCT visitor_id) visitors
             FROM analytics_events WHERE created_at>=?
             GROUP BY event_name ORDER BY total DESC LIMIT 20',
            [$since]
        ),
        'event_values' => $top(
            "SELECT event_name, event_value, COUNT(*) total
             FROM analytics_events WHERE created_at>=? AND event_value IS NOT NULL AND event_value<>''
             GROUP BY event_name, event_value ORDER BY total DESC LIMIT 25",
            [$since]
        ),
        'page_types' => $top(
            "SELECT page_type, COUNT(*) views
             FROM analytics_pageviews WHERE {$humans}
             GROUP BY page_type ORDER BY views DESC",
            [$since]
        ),
    ];
}
