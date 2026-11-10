<?php
declare(strict_types=1);
require_once __DIR__ . '/i18n.php';
function db(): PDO {
    static $pdo; global $config;
    if (!$pdo) $pdo = new PDO($config['db']['dsn'], $config['db']['user'], $config['db']['password'], [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    return $pdo;
}
function e(?string $v): string { return htmlspecialchars($v ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function url(string $path=''): string { global $config; return rtrim($config['site_url'], '/') . '/' . ltrim($path, '/'); }
function setting(string $key, string $default=''): string { try { $q=db()->prepare('SELECT value FROM settings WHERE `key`=?'); $q->execute([$key]); $v=$q->fetchColumn(); return $v===false?(string)$default:(string)$v; } catch (Throwable $x) { return $default; } }
function set_setting(string $key, string $value): void {
    $q=db()->prepare('INSERT INTO settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value=VALUES(value)');
    $q->execute([$key, $value]);
}
function show_hiddifysales(): bool {
    return setting('show_hiddifysales', '1') === '1';
}
function strip_hiddifysales_html(string $html): string {
    if (show_hiddifysales()) return $html;
    $html = preg_replace('~<a\\b[^>]*href=["\'][^"\']*hiddifysales[^"\']*["\'][^>]*>.*?</a>~is', '', $html) ?? $html;
    $html = preg_replace('~<p\\b[^>]*>[^<]*HiddifySales[^<]*</p>~iu', '', $html) ?? $html;
    $html = preg_replace('~HiddifySales~iu', '', $html) ?? $html;
    $html = preg_replace('~https?://(?:www\\.)?hiddifysales\\.com[^\\s<"\']*~iu', '', $html) ?? $html;
    return $html;
}
function query(string $sql, array $params=[]): array { $q=db()->prepare($sql); $q->execute($params); return $q->fetchAll(); }
function render(string $view, array $data=[]): void { extract($data); require dirname(__DIR__).'/app/Views/layouts/header.php'; require dirname(__DIR__).'/app/Views/'.$view.'.php'; require dirname(__DIR__).'/app/Views/layouts/footer.php'; }
function csrf(): string { if (empty($_SESSION['csrf'])) $_SESSION['csrf']=bin2hex(random_bytes(32)); return $_SESSION['csrf']; }
function verify_csrf(): void { if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) { http_response_code(419); exit('Invalid request'); } }
function is_admin(): bool { return !empty($_SESSION['admin_id']); }
function require_admin(): void { if (!is_admin()) { header('Location: /admin/login'); exit; } }
function sanitize_article_html(string $html): string {
    $html = preg_replace('~<(script|style|iframe|object|embed|svg|math|form|input|button|textarea|select|meta|link|base)\\b[^>]*>.*?</\\1\\s*>~is', '', $html);
    $html = preg_replace('~<(script|style|iframe|object|embed|svg|math|form|input|button|textarea|select|meta|link|base)\\b[^>]*/?>~is', '', $html);
    $html = strip_tags($html, '<p><br><h2><h3><ul><ol><li><strong><b><em><i><blockquote><code><pre><a><img><hr>');
    $html = preg_replace_callback('~<([a-z0-9]+)\\b([^>]*)>~i', static function ($tag) {
        $name = strtolower($tag[1]); $attrs = $tag[2]; $safe = '';
        if ($name === 'a' && preg_match("~\\\\bhref\\\\s*=\\\\s*(['\"])(.*?)\\\\1~i", $attrs, $m)) {
            $href = trim(html_entity_decode($m[2], ENT_QUOTES | ENT_HTML5, 'UTF-8'));
            if (!preg_match('~^(javascript|data|vbscript):~i', $href)) $safe .= ' href="' . e($href) . '"';
        }
        if ($name === 'img' && preg_match("~\\\\bsrc\\\\s*=\\\\s*(['\"])(.*?)\\\\1~i", $attrs, $m)) {
            $src = trim(html_entity_decode($m[2], ENT_QUOTES | ENT_HTML5, 'UTF-8'));
            if (preg_match('~^/uploads/[a-zA-Z0-9._-]+$~', $src)) $safe .= ' src="' . e($src) . '" loading="lazy"';
        }
        return '<' . $name . $safe . '>';
    }, $html);
    return $html;
}
