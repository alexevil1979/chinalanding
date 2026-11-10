<?php
declare(strict_types=1);
$configFile = dirname(__DIR__) . '/config/config.php';
$config = file_exists($configFile) ? require $configFile : require dirname(__DIR__) . '/config/config.example.php';
require dirname(__DIR__) . '/app/bootstrap.php';

$path = trim(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/', '/');
$locale = 'zh';
if (preg_match('#^(en|ru)(?:/|$)#', $path, $m)) {
    $locale = $m[1];
    $path = trim(substr($path, strlen($locale)), '/');
}
$GLOBALS['locale'] = $locale;
$GLOBALS['route_path'] = $path;
$route = $path;

if (str_ends_with($route, '.xml')) {
    require dirname(__DIR__) . '/app/seo.php';
    exit;
}

session_set_cookie_params(['httponly' => true, 'secure' => isset($_SERVER['HTTPS']), 'samesite' => 'Lax']);
session_start();

if (isset($_GET['lang']) && in_array($_GET['lang'], SUPPORTED_LOCALES, true)) {
    $target = (string)$_GET['lang'];
    $qs = $_GET;
    unset($qs['lang']);
    $query = http_build_query($qs);
    $dest = locale_url($target, $route) . ($query !== '' ? '?' . $query : '');
    header('Location: ' . $dest, true, 302);
    exit;
}

require dirname(__DIR__) . '/app/router.php';
