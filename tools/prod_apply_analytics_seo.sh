#!/bin/bash
# Run on PROD after: cd /ssd/www/anquanzhinan && git pull --ff-only origin main
set -euo pipefail

SITE=/ssd/www/anquanzhinan
STAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR=/root/anquan-backups

cd "$SITE"
test -f config/config.php || { echo "missing config.php"; exit 1; }

mkdir -p "$BACKUP_DIR"
echo "[1/5] db backup"
php -r '
$c = require "/ssd/www/anquanzhinan/config/config.php";
file_put_contents("/tmp/anquan_db_env",
  $c["db"]["user"]."\n".
  $c["db"]["password"]."\n".
  preg_replace("/.*dbname=([^;]+).*/", "$1", $c["db"]["dsn"])."\n"
);
'
DBUSER=$(sed -n '1p' /tmp/anquan_db_env)
DBPASS=$(sed -n '2p' /tmp/anquan_db_env)
DBNAME=$(sed -n '3p' /tmp/anquan_db_env)
rm -f /tmp/anquan_db_env
export MYSQL_PWD="$DBPASS"
mysqldump -u "$DBUSER" --single-transaction --routines --triggers --no-tablespaces "$DBNAME" \
  | gzip -c > "$BACKUP_DIR/db-before-analytics-${STAMP}.sql.gz"
unset MYSQL_PWD

echo "[2/5] migrate"
php <<'PHP'
<?php
$site = '/ssd/www/anquanzhinan';
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
$c['site_url'] = 'https://anquanzhinan.com';
file_put_contents($site . '/config/config.php', "<?php\nreturn " . var_export($c, true) . ";\n");
echo "site_url=https://anquanzhinan.com\n";
$q = $pdo->prepare('INSERT INTO settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value=IF(value="", VALUES(value), value)');
$q->execute(['gtm_id', 'GTM-P5PGDL39']);
echo "gtm_id seeded if empty\n";
PHP

echo "[3/5] permissions"
chown -R www-data:www-data "$SITE"
find "$SITE" -type d -exec chmod 755 {} \;
find "$SITE" -type f -exec chmod 644 {} \;
chmod 640 "$SITE/config/config.php" || true

echo "[4/5] reload"
systemctl reload php8.2-fpm 2>/dev/null || systemctl reload php-fpm 2>/dev/null || true
systemctl reload apache2 2>/dev/null || true

echo "[5/5] verify"
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
for u in / /articles/what-is-https /en/ /robots.txt /sitemap.xml /sitemap-pages.xml /admin/login; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -A "$UA" "https://anquanzhinan.com$u" || echo ERR)
  echo "$code $u"
done
curl -s -A "$UA" -H 'Content-Type: application/json' -H 'Origin: https://anquanzhinan.com' \
  -X POST 'https://anquanzhinan.com/analytics/collect' \
  -d '{"events":[{"name":"search","value":"vpn","path":"/search","locale":"zh"}]}' || true
echo
php <<'PHP'
<?php
$c = require '/ssd/www/anquanzhinan/config/config.php';
$pdo = new PDO($c['db']['dsn'], $c['db']['user'], $c['db']['password'], [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
]);
echo 'HEAD files ok; pageviews=' . $pdo->query('SELECT COUNT(*) FROM analytics_pageviews')->fetchColumn()
   . ' events=' . $pdo->query('SELECT COUNT(*) FROM analytics_events')->fetchColumn() . "\n";
PHP
echo "DONE. Open https://anquanzhinan.com/admin/analytics"
