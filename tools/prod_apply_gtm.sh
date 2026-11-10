#!/bin/bash
# After git pull on prod — seed GTM + reload + verify snippet on homepage.
set -euo pipefail
SITE=/ssd/www/anquanzhinan
cd "$SITE"
php <<'PHP'
<?php
$c = require '/ssd/www/anquanzhinan/config/config.php';
$pdo = new PDO($c['db']['dsn'], $c['db']['user'], $c['db']['password'], [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$q = $pdo->prepare('INSERT INTO settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value=VALUES(value)');
$q->execute(['gtm_id', 'GTM-P5PGDL39']);
echo "gtm_id=GTM-P5PGDL39\n";
$c['site_url'] = 'https://anquanzhinan.com';
file_put_contents('/ssd/www/anquanzhinan/config/config.php', "<?php\nreturn " . var_export($c, true) . ";\n");
PHP
chown -R www-data:www-data "$SITE"
systemctl reload php8.2-fpm 2>/dev/null || systemctl reload php-fpm 2>/dev/null || true
systemctl reload apache2 2>/dev/null || true
curl -s https://anquanzhinan.com/ | tr '\n' ' ' | grep -oE 'GTM-[A-Z0-9]+|googletagmanager.com/gtm.js' | head -5
echo
curl -s -o /dev/null -w "home=%{http_code}\n" https://anquanzhinan.com/
echo DONE
