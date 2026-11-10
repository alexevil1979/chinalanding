<?php
declare(strict_types=1);
$configFile = dirname(__DIR__) . '/config/config.php';
$config = file_exists($configFile) ? require $configFile : require dirname(__DIR__) . '/config/config.example.php';
require dirname(__DIR__) . '/app/bootstrap.php';
$route = trim(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/', '/');
if (str_ends_with($route, '.xml')) {
    require dirname(__DIR__) . '/app/seo.php';
    exit;
}
session_set_cookie_params(['httponly'=>true, 'secure'=>isset($_SERVER['HTTPS']), 'samesite'=>'Lax']);
session_start();
require dirname(__DIR__) . '/app/router.php';
