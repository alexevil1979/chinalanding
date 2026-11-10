<?php
declare(strict_types=1);

if (str_starts_with($route, 'admin')) {
    require dirname(__DIR__) . '/app/admin.php';
    exit;
}

if ($route === '') {
    $latest = [];
    $featured = [];
    $popular = [];
    $categories = [];
    $catName = "(SELECT c.name FROM article_category x JOIN categories c ON c.id=x.category_id WHERE x.article_id=a.id LIMIT 1) category_name";
    try {
        $latest = localize_articles(query("SELECT a.*, $catName FROM articles a WHERE a.status='published' AND a.published_at<=NOW() ORDER BY a.published_at DESC LIMIT 9"));
        $featured = localize_articles(query("SELECT a.*, $catName FROM articles a WHERE a.status='published' AND a.published_at<=NOW() AND a.is_featured=1 ORDER BY a.published_at DESC LIMIT 3"));
        if (!$featured) {
            $featured = array_slice($latest, 0, 3);
        }
        $popular = localize_articles(query("SELECT a.*, $catName FROM articles a WHERE a.status='published' AND a.published_at<=NOW() AND a.is_popular=1 ORDER BY a.published_at DESC LIMIT 6"));
        if (!$popular) {
            $popular = array_slice($latest, 0, 6);
        }
        $categories = array_map('localize_category', query('SELECT * FROM categories ORDER BY id'));
    } catch (Throwable $x) {
        try {
            $categories = array_map('localize_category', query('SELECT * FROM categories ORDER BY id'));
        } catch (Throwable $y) {
        }
    }
    render('pages/home', [
        'title' => t('home_title'),
        'description' => t('home_description'),
        'keywords' => t('default_keywords'),
        'latest' => $latest,
        'featured' => $featured,
        'popular' => $popular,
        'categories' => $categories,
    ]);
    exit;
}

if ($route === 'search') {
    $term = trim((string)($_GET['q'] ?? ''));
    $page = max(1, (int)($_GET['page'] ?? 1));
    $perPage = 10;
    $results = [];
    $total = 0;
    if ($term !== '') {
        if (locale() === 'zh') {
            $like = '%' . $term . '%';
            $count = db()->prepare("SELECT COUNT(DISTINCT a.id) FROM articles a LEFT JOIN article_category ac ON ac.article_id=a.id LEFT JOIN categories c ON c.id=ac.category_id WHERE a.status='published' AND a.published_at<=NOW() AND (a.title LIKE ? OR a.content_html LIKE ? OR c.name LIKE ?)");
            $count->execute([$like, $like, $like]);
            $total = (int)$count->fetchColumn();
            $stmt = db()->prepare("SELECT a.*,(SELECT c.name FROM article_category x JOIN categories c ON c.id=x.category_id WHERE x.article_id=a.id LIMIT 1) category_name FROM articles a WHERE a.status='published' AND a.published_at<=NOW() AND (a.title LIKE ? OR a.content_html LIKE ? OR EXISTS(SELECT 1 FROM article_category x JOIN categories c ON c.id=x.category_id WHERE x.article_id=a.id AND c.name LIKE ?)) ORDER BY a.is_popular DESC,a.published_at DESC LIMIT ? OFFSET ?");
            $stmt->bindValue(1, $like);
            $stmt->bindValue(2, $like);
            $stmt->bindValue(3, $like);
            $stmt->bindValue(4, $perPage, PDO::PARAM_INT);
            $stmt->bindValue(5, ($page - 1) * $perPage, PDO::PARAM_INT);
            $stmt->execute();
            $results = localize_articles($stmt->fetchAll());
        } else {
            $all = query("SELECT a.*,(SELECT c.name FROM article_category x JOIN categories c ON c.id=x.category_id WHERE x.article_id=a.id LIMIT 1) category_name FROM articles a WHERE a.status='published' AND a.published_at<=NOW() ORDER BY a.is_popular DESC,a.published_at DESC");
            $needle = mb_strtolower($term, 'UTF-8');
            $matched = [];
            foreach ($all as $row) {
                $loc = localize_article($row);
                $hay = mb_strtolower(($loc['title'] ?? '') . ' ' . ($loc['meta_description'] ?? '') . ' ' . strip_tags((string)($loc['content_html'] ?? '')), 'UTF-8');
                if (mb_strpos($hay, $needle, 0, 'UTF-8') !== false) {
                    $matched[] = $loc;
                }
            }
            $total = count($matched);
            $results = array_slice($matched, ($page - 1) * $perPage, $perPage);
        }
    }
    render('pages/search', [
        'title' => $term !== '' ? t('search_title_q', ['q' => $term]) : t('search_title'),
        'description' => t('search_description'),
        'term' => $term,
        'results' => $results,
        'total' => $total,
        'page' => $page,
        'pages' => (int)ceil($total / $perPage),
    ]);
    exit;
}

if (in_array($route, ['rss.xml', 'sitemap-articles.xml', 'sitemap-categories.xml'], true)) {
    require dirname(__DIR__) . '/app/seo.php';
    exit;
}

if ($route === 'tools') {
    $guides = [];
    try {
        $guides = localize_articles(query("SELECT a.*, (SELECT c.name FROM article_category x JOIN categories c ON c.id=x.category_id WHERE x.article_id=a.id LIMIT 1) category_name FROM articles a WHERE a.status='published' AND a.published_at<=NOW() AND a.slug IN ('what-is-vpn','vpn-vs-proxy','what-is-wireguard','what-is-vless','network-traffic-encryption','choose-privacy-tools','what-is-dns-leak','what-is-https') ORDER BY FIELD(a.slug,'what-is-vpn','what-is-wireguard','what-is-vless','vpn-vs-proxy','network-traffic-encryption','what-is-dns-leak','what-is-https','choose-privacy-tools')"));
    } catch (Throwable $x) {
    }
    render('pages/tools', [
        'title' => t('tools_title'),
        'description' => t('tools_description'),
        'keywords' => t('default_keywords'),
        'guides' => $guides,
    ]);
    exit;
}

if (in_array($route, ['about', 'contact', 'privacy-policy', 'terms'], true)) {
    $copy = static_page_copy($route);
    if (locale() === 'zh' || !$copy) {
        $staticMeta = [
            'about' => ['title' => '关于我们_数字安全指南编辑原则', 'description' => '了解数字安全指南的定位、编辑原则与商业关系披露。', 'keywords' => '关于我们,数字安全指南,编辑原则'],
            'contact' => ['title' => '联系我们_选题纠错与微信联系', 'description' => '通过邮件或微信公众号联系数字安全指南编辑团队，反馈纠错与选题建议。', 'keywords' => '联系我们,选题建议,微信公众号'],
            'privacy-policy' => ['title' => '隐私政策_数字安全指南', 'description' => '说明本站日志、Cookie 与第三方链接的数据处理原则。', 'keywords' => '隐私政策,数据最小化,Cookie'],
            'terms' => ['title' => '使用条款_内容边界与合规声明', 'description' => '本站内容仅供科普参考，请遵守中华人民共和国法律法规。', 'keywords' => '使用条款,合规声明,科普声明'],
        ][$route];
        render('pages/static', [
            'page' => $route,
            'title' => $staticMeta['title'],
            'description' => $staticMeta['description'],
            'keywords' => $staticMeta['keywords'],
            'pageCopy' => null,
        ]);
    } else {
        render('pages/static', [
            'page' => $route,
            'title' => $copy['title'] ?? t('site_name'),
            'description' => $copy['description'] ?? t('default_description'),
            'keywords' => $copy['keywords'] ?? t('default_keywords'),
            'pageCopy' => $copy,
        ]);
    }
    exit;
}

if (preg_match('#^articles/([a-z0-9-]+)$#', $route, $m)) {
    $rows = query("SELECT a.*,GROUP_CONCAT(DISTINCT c.name SEPARATOR '、') categories,GROUP_CONCAT(DISTINCT c.slug SEPARATOR ',') category_slugs FROM articles a LEFT JOIN article_category ac ON ac.article_id=a.id LEFT JOIN categories c ON c.id=ac.category_id WHERE a.slug=? AND a.status='published' AND a.published_at<=NOW() GROUP BY a.id", [$m[1]]);
    if (!$rows) {
        http_response_code(404);
        render('pages/404', ['title' => t('page_not_found')]);
        exit;
    }
    $art = localize_article($rows[0]);
    $kwMapZh = [
        'what-is-vpn' => 'VPN原理,隧道加密,企业远程接入,威胁模型,网络加密',
        'vpn-vs-proxy' => 'VPN与代理区别,信任边界,企业远程接入,隧道协议,网络加密',
        'what-is-wireguard' => 'WireGuard协议,Noise握手,Cryptokey Routing,企业VPN原理,网络加密',
        'what-is-vless' => 'VLESS协议,Xray,TLS,UUID认证,网络加密',
        'what-is-dns-leak' => 'DNS泄露,DoH,DoT,隧道DNS,网络加密',
        'network-traffic-encryption' => '网络流量加密,TLS,HTTPS,元数据,网络加密',
        'choose-privacy-tools' => '隐私工具选型,威胁模型,开源审计,账户安全,安全工具',
        'identify-phishing-attacks' => '网络钓鱼,钓鱼识别,账户安全,诈骗防范',
        'two-factor-authentication-guide' => '双重验证,2FA,TOTP,账户安全',
        'what-is-https' => 'HTTPS,TLS,证书验证,传输加密',
        'protect-online-accounts' => '账户安全,密码管理,会话管理,防盗号',
    ];
    $kwMapEn = [
        'what-is-vpn' => 'VPN fundamentals,tunnel encryption,remote access,threat model,network encryption',
        'vpn-vs-proxy' => 'VPN vs proxy,trust boundary,remote access,tunnel protocols',
        'what-is-wireguard' => 'WireGuard,Noise handshake,Cryptokey Routing,VPN principles',
        'what-is-vless' => 'VLESS,Xray,TLS,UUID auth,network encryption',
        'what-is-dns-leak' => 'DNS leak,DoH,DoT,tunnel DNS',
        'network-traffic-encryption' => 'traffic encryption,TLS,HTTPS,metadata',
        'choose-privacy-tools' => 'privacy tools,threat model,open source audit,account security',
        'identify-phishing-attacks' => 'phishing,account security,fraud prevention',
        'two-factor-authentication-guide' => '2FA,TOTP,account security',
        'what-is-https' => 'HTTPS,TLS,certificate validation',
        'protect-online-accounts' => 'account security,password managers,session security',
    ];
    $kwMapRu = [
        'what-is-vpn' => 'VPN,туннельное шифрование,удалённый доступ,модель угроз',
        'vpn-vs-proxy' => 'VPN и прокси,граница доверия,туннельные протоколы',
        'what-is-wireguard' => 'WireGuard,Noise,Cryptokey Routing,VPN',
        'what-is-vless' => 'VLESS,Xray,TLS,UUID,шифрование сети',
        'what-is-dns-leak' => 'утечка DNS,DoH,DoT',
        'network-traffic-encryption' => 'шифрование трафика,TLS,HTTPS,метаданные',
        'choose-privacy-tools' => 'инструменты приватности,модель угроз,безопасность аккаунтов',
        'identify-phishing-attacks' => 'фишинг,безопасность аккаунтов',
        'two-factor-authentication-guide' => '2FA,TOTP,безопасность аккаунтов',
        'what-is-https' => 'HTTPS,TLS,проверка сертификатов',
        'protect-online-accounts' => 'безопасность аккаунтов,менеджеры паролей',
    ];
    $kwMaps = ['zh' => $kwMapZh, 'en' => $kwMapEn, 'ru' => $kwMapRu];
    $kw = ($kwMaps[locale()][$art['slug']] ?? null) ?: t('default_keywords');
    render('articles/show', [
        'article' => $art,
        'title' => $art['seo_title'] ?: $art['title'],
        'description' => $art['meta_description'],
        'keywords' => $kw,
    ]);
    exit;
}

if (preg_match('#^category/([a-z0-9-]+)$#', $route, $m)) {
    $cats = query('SELECT * FROM categories WHERE slug=?', [$m[1]]);
    if (!$cats) {
        http_response_code(404);
        render('pages/404', ['title' => t('page_not_found')]);
        exit;
    }
    $page = max(1, (int)($_GET['page'] ?? 1));
    $perPage = 12;
    $q = db()->prepare("SELECT a.* FROM articles a JOIN article_category ac ON ac.article_id=a.id WHERE ac.category_id=? AND a.status='published' AND a.published_at<=NOW() ORDER BY a.is_featured DESC,a.published_at DESC LIMIT ? OFFSET ?");
    $q->bindValue(1, $cats[0]['id'], PDO::PARAM_INT);
    $q->bindValue(2, $perPage, PDO::PARAM_INT);
    $q->bindValue(3, ($page - 1) * $perPage, PDO::PARAM_INT);
    $q->execute();
    $articles = localize_articles($q->fetchAll());
    $countQ = db()->prepare("SELECT COUNT(*) FROM articles a JOIN article_category ac ON ac.article_id=a.id WHERE ac.category_id=? AND a.status='published' AND a.published_at<=NOW()");
    $countQ->execute([$cats[0]['id']]);
    $pages = (int)ceil((int)$countQ->fetchColumn() / $perPage);
    $cat = localize_category($cats[0]);
    $catTitle = $cat['seo_title'] ?: ($cat['name'] . ' | ' . t('site_name'));
    $catDesc = $cat['meta_description'] ?: ($cat['description'] ?? '');
    $catKw = $cat['name'] . ', ' . t('default_keywords');
    render('category/index', [
        'category' => $cat,
        'articles' => $articles,
        'page' => $page,
        'pages' => $pages,
        'title' => $catTitle,
        'description' => $catDesc,
        'keywords' => $catKw,
    ]);
    exit;
}

http_response_code(404);
render('pages/404', ['title' => t('page_not_found')]);
