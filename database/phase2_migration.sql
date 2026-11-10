-- Safe additive migration for MySQL 8.0; preserves records and existing URLs.
ALTER TABLE articles
  ADD COLUMN is_featured TINYINT(1) NOT NULL DEFAULT 0,
  ADD COLUMN is_popular TINYINT(1) NOT NULL DEFAULT 0,
  ADD COLUMN image_url VARCHAR(500) NULL,
  ADD COLUMN image_alt VARCHAR(255) NULL,
  ADD COLUMN faq_json JSON NULL,
  ADD COLUMN sources_json JSON NULL;
CREATE INDEX articles_featured_status_date ON articles(is_featured,status,published_at);
CREATE INDEX articles_popular_status_date ON articles(is_popular,status,published_at);
