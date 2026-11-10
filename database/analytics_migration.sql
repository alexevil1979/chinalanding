-- Self-hosted visitor analytics (pageviews + events). Safe to re-run.
CREATE TABLE IF NOT EXISTS analytics_pageviews (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS analytics_events (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
