-- ============================================================
-- BRATZ DRIP - Complete PostgreSQL Database Schema
-- Run this file in your PostgreSQL database
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- PRODUCTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name          VARCHAR(255) NOT NULL,
  description   TEXT,
  price         DECIMAL(10,2) NOT NULL,
  original_price DECIMAL(10,2),
  category      VARCHAR(100) NOT NULL,
  emoji         VARCHAR(10),
  gradient      VARCHAR(255),
  tag           VARCHAR(50),
  stock         INTEGER NOT NULL DEFAULT 0,
  sizes         TEXT[] NOT NULL DEFAULT '{}',
  rating        DECIMAL(3,2) DEFAULT 0,
  review_count  INTEGER DEFAULT 0,
  is_active     BOOLEAN DEFAULT TRUE,
  created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- PRODUCT INVENTORY TABLE (per size stock tracking)
-- ============================================================
CREATE TABLE IF NOT EXISTS product_inventory (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id  UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  size        VARCHAR(20) NOT NULL,
  stock       INTEGER NOT NULL DEFAULT 0,
  updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(product_id, size)
);

-- ============================================================
-- CUSTOMERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS customers (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email         VARCHAR(255) UNIQUE NOT NULL,
  first_name    VARCHAR(100),
  last_name     VARCHAR(100),
  phone         VARCHAR(30),
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city          VARCHAR(100),
  state         VARCHAR(100),
  zip_code      VARCHAR(20),
  country       VARCHAR(100) DEFAULT 'US',
  is_subscribed BOOLEAN DEFAULT FALSE,
  total_orders  INTEGER DEFAULT 0,
  total_spent   DECIMAL(10,2) DEFAULT 0,
  created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ORDERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS orders (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_number    VARCHAR(20) UNIQUE NOT NULL,
  customer_id     UUID REFERENCES customers(id),
  customer_email  VARCHAR(255) NOT NULL,
  customer_name   VARCHAR(255),
  status          VARCHAR(50) NOT NULL DEFAULT 'pending',
  -- status: pending | confirmed | processing | shipped | delivered | cancelled | refunded
  subtotal        DECIMAL(10,2) NOT NULL,
  discount        DECIMAL(10,2) DEFAULT 0,
  shipping_cost   DECIMAL(10,2) DEFAULT 0,
  total           DECIMAL(10,2) NOT NULL,
  promo_code      VARCHAR(50),
  shipping_address JSONB,
  notes           TEXT,
  tracking_number VARCHAR(100),
  shipped_at      TIMESTAMP WITH TIME ZONE,
  delivered_at    TIMESTAMP WITH TIME ZONE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ORDER ITEMS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS order_items (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id  UUID REFERENCES products(id),
  product_name VARCHAR(255) NOT NULL,
  size        VARCHAR(20),
  price       DECIMAL(10,2) NOT NULL,
  quantity    INTEGER NOT NULL DEFAULT 1,
  subtotal    DECIMAL(10,2) NOT NULL,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- CART TABLE (persistent carts)
-- ============================================================
CREATE TABLE IF NOT EXISTS carts (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id  VARCHAR(255) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id),
  items       JSONB NOT NULL DEFAULT '[]',
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- WISHLIST TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS wishlists (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id  VARCHAR(255) NOT NULL,
  customer_id UUID REFERENCES customers(id),
  product_id  UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(session_id, product_id)
);

-- ============================================================
-- PROMO CODES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS promo_codes (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  code            VARCHAR(50) UNIQUE NOT NULL,
  discount_type   VARCHAR(20) NOT NULL DEFAULT 'percentage',
  -- percentage | fixed
  discount_value  DECIMAL(10,2) NOT NULL,
  min_order       DECIMAL(10,2) DEFAULT 0,
  max_uses        INTEGER,
  used_count      INTEGER DEFAULT 0,
  is_active       BOOLEAN DEFAULT TRUE,
  expires_at      TIMESTAMP WITH TIME ZONE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- EMAIL SUBSCRIBERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS email_subscribers (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email       VARCHAR(255) UNIQUE NOT NULL,
  is_active   BOOLEAN DEFAULT TRUE,
  source      VARCHAR(100) DEFAULT 'footer',
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ORDER STATUS HISTORY TABLE (audit trail)
-- ============================================================
CREATE TABLE IF NOT EXISTS order_status_history (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  old_status  VARCHAR(50),
  new_status  VARCHAR(50) NOT NULL,
  note        TEXT,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- PRODUCT REVIEWS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS product_reviews (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id  UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  order_id    UUID REFERENCES orders(id),
  customer_email VARCHAR(255),
  customer_name VARCHAR(100),
  rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  review_text TEXT,
  is_approved BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- INDEXES for performance
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_carts_session_id ON carts(session_id);
CREATE INDEX IF NOT EXISTS idx_wishlists_session_id ON wishlists(session_id);
CREATE INDEX IF NOT EXISTS idx_product_reviews_product_id ON product_reviews(product_id);

-- ============================================================
-- AUTO UPDATE updated_at trigger
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_orders_updated_at
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_customers_updated_at
  BEFORE UPDATE ON customers
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_carts_updated_at
  BEFORE UPDATE ON carts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- SEED DATA - Products
-- ============================================================
INSERT INTO products (name, description, price, original_price, category, emoji, gradient, tag, stock, sizes, rating, review_count) VALUES
('Y2K Plaid Mini', 'The iconic Y2K plaid mini skirt your wardrobe is BEGGING for. Pair with platform boots for max bratz energy.', 59.99, 89.99, 'Skirts', '🩷', 'from-pink-500 to-purple-600', 'BESTSELLER', 120, ARRAY['XS','S','M','L','XL'], 4.9, 312),
('Chrome Crop Jacket', 'Futuristic chrome jacket with iridescent sheen. Because why blend in when you were born to STAND OUT?', 129.99, NULL, 'Jackets', '🤍', 'from-slate-400 to-purple-500', 'NEW DROP', 45, ARRAY['XS','S','M','L'], 4.8, 198),
('Velvet Bodycon Dress', 'Midnight velvet hugs every curve perfectly. From club to brunch — this dress does it ALL.', 79.99, 99.99, 'Dresses', '💜', 'from-violet-600 to-pink-500', 'SALE', 80, ARRAY['XS','S','M','L','XL','XXL'], 4.7, 445),
('Hot Pink Cargo Pants', 'Statement cargo pants in signature Bratz hot pink. Six pockets because fashion girls carry LOTS of stuff.', 89.99, NULL, 'Pants', '🌸', 'from-pink-400 to-rose-600', 'TRENDING', 95, ARRAY['XS','S','M','L','XL'], 4.6, 267),
('Butterfly Mesh Top', 'Sheer mesh top with embroidered butterfly details. Layered over a bralette for that perfect bratz look.', 44.99, 59.99, 'Tops', '🦋', 'from-cyan-400 to-pink-500', NULL, 150, ARRAY['XS','S','M','L'], 4.8, 521),
('Gold Chain Mini Dress', '24k energy only. This gold chain-detail mini dress is pure luxury meets downtown girl.', 109.99, NULL, 'Dresses', '✨', 'from-yellow-400 to-orange-500', 'LIMITED', 20, ARRAY['XS','S','M','L'], 4.9, 178),
('Faux Fur Bolero', 'Fluffy faux fur bolero in cloud white. The layer your party outfit did not know it needed.', 74.99, NULL, 'Jackets', '🩶', 'from-gray-300 to-pink-300', NULL, 60, ARRAY['XS-S','M-L','XL-XXL'], 4.5, 203),
('Rhinestone Corset Top', 'Hand-applied rhinestone details on a structured satin corset. Every night out deserves to sparkle.', 64.99, 84.99, 'Tops', '💎', 'from-purple-500 to-indigo-600', 'SALE', 75, ARRAY['XS','S','M','L'], 4.9, 389)
ON CONFLICT DO NOTHING;

-- Seed inventory per size
INSERT INTO product_inventory (product_id, size, stock)
SELECT p.id, unnest(p.sizes), (p.stock / array_length(p.sizes, 1))
FROM products p
ON CONFLICT (product_id, size) DO NOTHING;

-- Seed promo codes
INSERT INTO promo_codes (code, discount_type, discount_value, min_order, max_uses, is_active) VALUES
('BRATZ20', 'percentage', 20, 0, 1000, true),
('WELCOME10', 'percentage', 10, 0, NULL, true),
('SPRING15', 'percentage', 15, 50, 500, true),
('FREESHIP', 'fixed', 9.99, 40, 200, true)
ON CONFLICT DO NOTHING;

-- ============================================================
-- USEFUL VIEWS
-- ============================================================

-- Sales summary view
CREATE OR REPLACE VIEW order_summary AS
SELECT
  DATE(created_at) as order_date,
  COUNT(*) as total_orders,
  SUM(total) as revenue,
  AVG(total) as avg_order_value,
  COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered,
  COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled
FROM orders
GROUP BY DATE(created_at)
ORDER BY order_date DESC;

-- Low stock alert view
CREATE OR REPLACE VIEW low_stock_products AS
SELECT p.id, p.name, p.category, pi.size, pi.stock
FROM products p
JOIN product_inventory pi ON p.id = pi.product_id
WHERE pi.stock < 10 AND p.is_active = true
ORDER BY pi.stock ASC;

-- Top selling products view
CREATE OR REPLACE VIEW top_selling_products AS
SELECT
  oi.product_id,
  oi.product_name,
  SUM(oi.quantity) as units_sold,
  SUM(oi.subtotal) as revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
WHERE o.status NOT IN ('cancelled', 'refunded')
GROUP BY oi.product_id, oi.product_name
ORDER BY units_sold DESC;
