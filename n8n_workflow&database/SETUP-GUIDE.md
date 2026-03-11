# 🚀 BRATZ DRIP — Complete Setup Guide
## Database + n8n Workflows + Next.js

---

## STEP 1 — Install & Run the Website

```bash
# Unzip and install
unzip bratz-drip.zip
cd bratz-drip
npm install

# Copy environment variables
cp .env.example .env.local
# Edit .env.local with your real values

# Run development server
npm run dev
# → Open http://localhost:3000
```

---

## STEP 2 — Set Up PostgreSQL Database

### Option A: Local PostgreSQL
```bash
# Install PostgreSQL (Mac)
brew install postgresql
brew services start postgresql

# Create database
psql postgres
CREATE DATABASE bratz_drip;
CREATE USER bratz_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE bratz_drip TO bratz_user;
\q

# Run the schema
psql -U bratz_user -d bratz_drip -f n8n-workflows/database-schema.sql
```

### Option B: Free Cloud Database (Recommended)
1. Go to **https://neon.tech** (free PostgreSQL)
2. Create project → Copy connection string
3. Paste into `.env.local` as `DATABASE_URL`
4. Run schema in Neon's SQL editor (paste contents of `database-schema.sql`)

### Option C: Supabase (also free)
1. Go to **https://supabase.com** → New Project
2. Go to SQL Editor → Paste and run `database-schema.sql`
3. Go to Settings → Database → Copy connection string

---

## STEP 3 — Install & Start n8n

```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
# → Opens at http://localhost:5678
```

Or with Docker:
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

---

## STEP 4 — Import All 5 Workflows into n8n

1. Open **http://localhost:5678**
2. Go to **Workflows** → Click **Import**
3. Import each file from the `n8n-workflows/` folder:

| File | What It Does |
|------|-------------|
| `01-new-order-processing.json` | Sends order confirmation email + Slack alert when order placed |
| `02-order-shipped-notification.json` | Checks every 15 min, emails customer when order ships |
| `03-low-stock-inventory-alert.json` | Every 6 hours, emails + Slacks if any product is low stock |
| `04-welcome-email-subscriber.json` | Sends beautiful welcome email when someone subscribes |
| `05-daily-sales-report.json` | 8AM every day — emails + Slacks full sales summary |

---

## STEP 5 — Configure n8n Credentials

In n8n, go to **Settings → Credentials** and create:

### PostgreSQL Credential
- **Name**: `Bratz Drip PostgreSQL`
- **Host**: your DB host
- **Database**: `bratz_drip`
- **User/Password**: your credentials

### Email (SMTP) Credential
- **Name**: `Bratz Drip Email`
- For Gmail: Use App Password (not your real password)
- Settings → Google Account → Security → App Passwords

### (Optional) Slack Webhook
- Go to https://api.slack.com/apps → Create App → Incoming Webhooks
- Copy webhook URL → Replace `YOUR_SLACK_WEBHOOK` in each workflow

---

## STEP 6 — Get Webhook URLs from n8n

After importing workflows, each webhook node has a URL. Copy them:

1. Open **Workflow 01** → Click "Webhook: Order Created" node → Copy URL
   → Paste into `.env.local` as `N8N_WEBHOOK_ORDER_URL`

2. Open **Workflow 04** → Click "Webhook: New Subscriber" node → Copy URL
   → Paste into `.env.local` as `N8N_WEBHOOK_SUBSCRIBE_URL`

3. Restart your Next.js server: `npm run dev`

---

## STEP 7 — Activate All Workflows

In n8n, open each workflow and click the **toggle** in the top right to **Activate** it.

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | Fetch all products (with filters) |
| `/api/products` | POST | Create new product |
| `/api/orders` | GET | Fetch orders (filter by email/status) |
| `/api/orders` | POST | Place new order → triggers n8n |
| `/api/cart` | GET | Get cart by session |
| `/api/cart` | POST | Save cart |
| `/api/cart` | DELETE | Clear cart |
| `/api/wishlist` | GET | Get wishlist |
| `/api/wishlist` | POST | Toggle wishlist item |
| `/api/customers` | GET | Get customers |
| `/api/customers` | POST | Create/update customer |
| `/api/subscribe` | POST | Subscribe to newsletter → triggers n8n |
| `/api/webhook` | POST | Receive callbacks from n8n |

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `products` | All products with price, stock, category |
| `product_inventory` | Stock per product per size |
| `customers` | Customer profiles and stats |
| `orders` | All orders with status tracking |
| `order_items` | Individual items in each order |
| `carts` | Persistent cart sessions |
| `wishlists` | Customer wishlists |
| `promo_codes` | Discount codes |
| `email_subscribers` | Newsletter subscribers |
| `order_status_history` | Full audit trail of order status changes |
| `product_reviews` | Customer product reviews |

---

## Test the Full Flow

1. Go to `http://localhost:3000/shop`
2. Add items to cart
3. Proceed to checkout
4. Enter email + shipping details
5. Click "Place Order"
6. ✅ Order saved to PostgreSQL
7. ✅ n8n Workflow 01 fires → sends confirmation email
8. ✅ Order status updated in DB
9. ✅ Slack alert sent to team
