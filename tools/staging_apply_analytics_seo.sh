#!/bin/bash
# Run on STAGING after: cd /var/www/chinalanding && git pull --ff-only origin main
set -euo pipefail

SITE=/var/www/chinalanding
cd "$SITE"
test -f config/config.php || { echo "missing config.php"; exit 1; }

php <<'PHP'
<?php
$site = '/var/www/chinalanding';
$c = require $site . '/config/config.php';
$pdo = new PDO($c['db']['dsn'], $c['db']['user'], $c['db']['password'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
]);
$sql = file_get_contents($site . '/database/analytics_migration.sql');
foreach (preg_split('/;\s*\n/', $sql) as $stmt) {
    $stmt = trim($stmt);
    if ($stmt === '' || str_starts_with($stmt, '--')) {
        continue;
    }
    $pdo->exec($stmt);
}
echo "migration_ok\n";
$c['site_url'] = 'https://chinalanding.1tlt.ru';
file_put_contents($site . '/config/config.php', "<?php\nreturn " . var_export($c, true) . ";\n");
echo "site_url=https://chinalanding.1tlt.ru\n";
$q = $pdo->prepare('INSERT INTO settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value=IF(value="", VALUES(value), value)');
$q->execute(['gtm_id', 'GTM-P5PGDL39']);
echo "gtm_id seeded if empty\n";
PHP

chown -R www-data:www-data "$SITE"
systemctl reload php8.1-fpm 2>/dev/null || systemctl reload php-fpm 2>/dev/null || true
systemctl reload apache2 2>/dev/null || true

UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
H='Host: chinalanding.1tlt.ru'
for u in / /articles/what-is-https /en/ /robots.txt /sitemap.xml /sitemap-pages.xml; do
  code=$(curl -sk -o /dev/null -w '%{http_code}' -A "$UA" -H "$H" "https://127.0.0.1$u" || echo ERR)
  echo "$code $u"
done
curl -sk -A "$UA" -H "$H" -H 'Content-Type: application/json' -H 'Origin: https://chinalanding.1tlt.ru' \
  -X POST 'https://127.0.0.1/analytics/collect' \
  -d '{"events":[{"name":"search","value":"vpn","path":"/search","locale":"zh"}]}' || true
echo
echo "DONE staging"
