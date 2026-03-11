# 🏆 LUXURY DOLL CLOTHING E-COMMERCE PLATFORM
## The Ultimate 2026 Technical Blueprint

---

## 🎯 EXECUTIVE SUMMARY

This is not just a store—this is a **fully automated luxury e-commerce empire** built with bleeding-edge 2026 technology. Every process is automated, every customer touchpoint is optimized, and every admin task is eliminated through AI.

**Core Philosophy:** You create art (doll clothing). The system handles everything else.

---

## 🛠️ COMPLETE TECH STACK (2026 Best-in-Class)

### **FRONTEND LAYER**
| Technology | Purpose | Why Best-in-Class |
|------------|---------|-------------------|
| **Next.js 15** | React Framework | Server Components, Edge Runtime, RSC streaming |
| **React 19** | UI Library | Concurrent features, automatic batching |
| **Tailwind CSS 4** | Styling | CSS-first config, oxide engine, container queries |
| **Framer Motion** | Animations | GPU-accelerated, spring physics |
| **Zustand** | State Management | Lightweight, no boilerplate |
| **TanStack Query v5** | Server State | Automatic caching, optimistic updates |
| **React Hook Form** | Forms | Best performance, built-in validation |
| **Zod** | Validation | Type-safe schemas |

### **BACKEND LAYER**
| Technology | Purpose | Why Best-in-Class |
|------------|---------|-------------------|
| **FastAPI** | API Framework | Async native, auto docs, validation |
| **Python 3.12** | Language | Performance improvements, type hints |
| **PostgreSQL 16** | Database | JSONB, full-text search, reliability |
| **SQLAlchemy 2.0** | ORM | Async support, type safety |
| **Alembic** | Migrations | Version control for DB schema |
| **Pydantic V2** | Data Validation | 17x faster, strict mode |
| **Redis 7** | Caching | In-memory speed, pub/sub |
| **Celery** | Task Queue | Async job processing |

### **AI & AUTOMATION LAYER**
| Technology | Purpose | Why Best-in-Class |
|------------|---------|-------------------|
| **n8n** | Workflow Automation | Self-hosted, visual, powerful |
| **OpenAI GPT-4o** | AI Writing | Best product descriptions |
| **Claude 4 Sonnet** | Complex Logic | Superior reasoning for quotes |
| **Anthropic Vision** | Image Analysis | Product photo understanding |
| **Replicate** | Background Removal | AI-powered product photo cleanup |

### **INFRASTRUCTURE LAYER**
| Technology | Purpose | Why Best-in-Class |
|------------|---------|-------------------|
| **Vercel** | Next.js Hosting | Edge functions, automatic optimization |
| **Railway** | Backend Hosting | PostgreSQL + Redis + n8n all-in-one |
| **Cloudinary** | Image CDN | Auto-optimization, transformations |
| **Stripe** | Payments | Industry standard, automatic tax |
| **Resend** | Transactional Email | Developer-first, 99.9% deliverability |
| **Sentry** | Error Tracking | Real-time debugging |
| **PostHog** | Product Analytics | Self-hosted, complete privacy |

### **SUPPORTING SERVICES**
| Technology | Purpose | Why Best-in-Class |
|------------|---------|-------------------|
| **Meilisearch** | Product Search | Typo-tolerant, instant results |
| **Google Sheets API** | Inventory Tracking | Simple, real-time, shareable |
| **Airtable** | Customer CRM | Visual, powerful, automations |
| **Clerk** | Authentication | Built-in UI, social login |
| **uploadthing** | File Uploads | Type-safe, Next.js native |

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                        CUSTOMER                             │
│                    (Web Browser)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   VERCEL EDGE NETWORK                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              NEXT.JS 15 FRONTEND                     │  │
│  │  • Server Components (RSC)                           │  │
│  │  • Edge Middleware (Geo-routing, A/B tests)          │  │
│  │  • Incremental Static Regeneration (ISR)             │  │
│  │  • Image Optimization (WebP, AVIF)                   │  │
│  │  • Real-time Inventory Display                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│                   (Railway Hosted)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints:                                 │  │
│  │  • /products - CRUD operations                       │  │
│  │  • /orders - Order management                        │  │
│  │  • /customers - User profiles                        │  │
│  │  • /custom-quotes - Quote requests                   │  │
│  │  • /webhooks - Stripe/n8n integrations               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │  PostgreSQL 16   │  │    Redis 7       │               │
│  │  • Products      │  │  • Session Cache │               │
│  │  • Orders        │  │  • Rate Limiting │               │
│  │  • Customers     │  │  • Job Queue     │               │
│  │  • Inventory     │  │  • Pub/Sub       │               │
│  └──────────────────┘  └──────────────────┘               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   N8N AUTOMATION ENGINE                     │
│                   (Railway Hosted)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  WORKFLOW 1: Product Creation Bot                    │  │
│  │  WORKFLOW 2: Custom Quote Automation                 │  │
│  │  WORKFLOW 3: Order Fulfillment                       │  │
│  │  WORKFLOW 4: Inventory Alerts                        │  │
│  │  WORKFLOW 5: Customer Lifecycle                      │  │
│  │  WORKFLOW 6: Abandoned Cart Recovery                 │  │
│  │  WORKFLOW 7: Review Requests                         │  │
│  │  WORKFLOW 8: Restock Notifications                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                ┌────────┴────────┐
                ▼                 ▼
    ┌──────────────────┐  ┌──────────────────┐
    │  Google Sheets   │  │    Airtable      │
    │  (Inventory DB)  │  │  (Customer CRM)  │
    └──────────────────┘  └──────────────────┘
```

---

## 📊 DATABASE SCHEMA (PostgreSQL)

```sql
-- PRODUCTS TABLE
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    compare_at_price DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    inventory_quantity INTEGER DEFAULT 0,
    inventory_policy VARCHAR(20) DEFAULT 'deny', -- 'deny' or 'continue'
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'active', 'archived'
    category VARCHAR(100),
    tags TEXT[], -- Array of tags
    images JSONB, -- [{url, alt, position}]
    metadata JSONB, -- Custom fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    created_by VARCHAR(100), -- 'manual' or 'ai'
    
    -- SEO
    seo_title VARCHAR(70),
    seo_description VARCHAR(160),
    handle VARCHAR(255) UNIQUE, -- URL slug
    
    -- Analytics
    view_count INTEGER DEFAULT 0,
    wishlist_count INTEGER DEFAULT 0,
    
    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', title || ' ' || description)
    ) STORED
);

CREATE INDEX idx_products_search ON products USING GIN(search_vector);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_category ON products(category);

-- ORDERS TABLE
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),
    
    -- Financial
    subtotal DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0,
    shipping DECIMAL(10, 2) DEFAULT 0,
    discount DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    
    -- Status
    financial_status VARCHAR(20) DEFAULT 'pending', -- pending, paid, refunded
    fulfillment_status VARCHAR(20) DEFAULT 'unfulfilled', -- unfulfilled, fulfilled, partial
    
    -- Items
    line_items JSONB NOT NULL, -- [{product_id, title, quantity, price}]
    
    -- Shipping
    shipping_address JSONB,
    billing_address JSONB,
    tracking_number VARCHAR(100),
    tracking_url TEXT,
    
    -- Payment
    stripe_payment_intent_id VARCHAR(100),
    
    -- Metadata
    notes TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    fulfilled_at TIMESTAMP,
    cancelled_at TIMESTAMP
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(financial_status, fulfillment_status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- CUSTOMERS TABLE
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    
    -- Authentication (if using Clerk, this stores clerk_user_id)
    auth_provider_id VARCHAR(255) UNIQUE,
    
    -- Preferences
    email_marketing_consent BOOLEAN DEFAULT false,
    sms_marketing_consent BOOLEAN DEFAULT false,
    
    -- Address
    default_address JSONB,
    addresses JSONB[], -- Multiple addresses
    
    -- Analytics
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0,
    average_order_value DECIMAL(10, 2) DEFAULT 0,
    last_order_date TIMESTAMP,
    
    -- Metadata
    tags TEXT[],
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_total_spent ON customers(total_spent DESC);

-- CUSTOM_QUOTES TABLE
CREATE TABLE custom_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),
    
    -- Request Details
    customer_email VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255),
    doll_type VARCHAR(100), -- Bratz, Barbie, Monster High, etc.
    outfit_description TEXT NOT NULL,
    reference_images JSONB, -- [{url, cloudinary_id}]
    special_requests TEXT,
    
    -- Quote Details
    status VARCHAR(20) DEFAULT 'pending', -- pending, quoted, accepted, rejected, expired
    quoted_price DECIMAL(10, 2),
    quoted_delivery_days INTEGER,
    quote_valid_until TIMESTAMP,
    
    -- PDF
    pdf_url TEXT,
    pdf_cloudinary_id VARCHAR(255),
    
    -- Tracking
    created_at TIMESTAMP DEFAULT NOW(),
    quoted_at TIMESTAMP,
    accepted_at TIMESTAMP,
    order_id UUID REFERENCES orders(id), -- If accepted and ordered
    
    -- Automation
    ai_analysis JSONB, -- Claude's complexity analysis
    auto_quoted BOOLEAN DEFAULT false
);

CREATE INDEX idx_quotes_status ON custom_quotes(status);
CREATE INDEX idx_quotes_customer ON custom_quotes(customer_id);
CREATE INDEX idx_quotes_created ON custom_quotes(created_at DESC);

-- INVENTORY_LOGS TABLE (Audit Trail)
CREATE TABLE inventory_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    quantity_change INTEGER NOT NULL, -- Can be negative
    reason VARCHAR(50) NOT NULL, -- 'sale', 'restock', 'adjustment', 'return'
    order_id UUID REFERENCES orders(id),
    notes TEXT,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventory_logs_product ON inventory_logs(product_id, created_at DESC);

-- ABANDONED_CARTS TABLE
CREATE TABLE abandoned_carts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) NOT NULL,
    customer_id UUID REFERENCES customers(id),
    customer_email VARCHAR(255),
    
    -- Cart Data
    items JSONB NOT NULL, -- [{product_id, quantity, price}]
    subtotal DECIMAL(10, 2) NOT NULL,
    
    -- Recovery
    recovered BOOLEAN DEFAULT false,
    recovery_email_sent_at TIMESTAMP,
    recovery_email_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    abandoned_at TIMESTAMP,
    recovered_at TIMESTAMP
);

CREATE INDEX idx_abandoned_carts_email ON abandoned_carts(customer_email);
CREATE INDEX idx_abandoned_carts_recovered ON abandoned_carts(recovered, abandoned_at);

-- PRODUCT_REVIEWS TABLE
CREATE TABLE product_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    customer_id UUID REFERENCES customers(id),
    order_id UUID REFERENCES orders(id),
    
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    content TEXT,
    
    -- Images
    images JSONB, -- [{url, cloudinary_id}]
    
    -- Moderation
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
    helpful_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP
);

CREATE INDEX idx_reviews_product ON product_reviews(product_id, status);
CREATE INDEX idx_reviews_rating ON product_reviews(product_id, rating DESC);

-- WAITLIST TABLE (for sold-out products)
CREATE TABLE product_waitlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    customer_email VARCHAR(255) NOT NULL,
    customer_id UUID REFERENCES customers(id),
    notified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    notified_at TIMESTAMP,
    
    UNIQUE(product_id, customer_email)
);

CREATE INDEX idx_waitlist_product ON product_waitlist(product_id, notified);
```

---

## 🤖 N8N AUTOMATION WORKFLOWS (Complete Logic)

### **WORKFLOW 1: AI Product Creation Bot**

**Trigger:** Email received at `products@yourdollstore.com`

```
EMAIL STRUCTURE:
Subject: $45
Body: (optional notes like "Barbie evening gown")
Attachment: product-photo.jpg
```

**n8n Flow:**

```
[1] EMAIL TRIGGER (Gmail)
    ↓
[2] EXTRACT DATA
    • Price: Parse subject line
    • Notes: Extract from body
    • Image: Download attachment to temp storage
    ↓
[3] UPLOAD TO CLOUDINARY
    • Auto-remove background (if needed)
    • Generate thumbnails (400px, 800px, 1200px)
    • Get permanent URLs
    ↓
[4] AI IMAGE ANALYSIS (Claude Vision API)
    Prompt: "Analyze this doll clothing photo. Identify:
            - Doll type (Barbie, Bratz, Monster High, etc.)
            - Clothing type (dress, shoes, accessories, etc.)
            - Colors (primary and accent)
            - Style (vintage, modern, formal, casual, etc.)
            - Materials visible (satin, cotton, lace, etc.)
            - Special features (sequins, embroidery, etc.)
            Return as JSON."
    ↓
[5] AI PRODUCT DESCRIPTION (GPT-4o API)
    Prompt: "Write a luxury product description for this handmade doll outfit:
            Type: {clothing_type}
            Doll: {doll_type}
            Colors: {colors}
            Style: {style}
            Price: ${price}
            
            Requirements:
            - 2-3 sentences, elegant tone
            - Highlight craftsmanship
            - Mention fit and materials
            - Create desire
            - SEO-friendly
            
            Also generate:
            - SEO title (max 70 chars)
            - Meta description (max 160 chars)
            - 5 relevant tags"
    ↓
[6] GENERATE SKU
    • Format: {DOLL_CODE}-{CATEGORY}-{RANDOM}
    • Example: BRB-DRS-A4K9
    ↓
[7] CREATE IN DATABASE (FastAPI Webhook)
    POST /api/products
    {
      "sku": "BRB-DRS-A4K9",
      "title": "Vintage Rose Garden Evening Gown for Barbie",
      "description": "...",
      "price": 45.00,
      "images": [{cloudinary_urls}],
      "category": "Dresses",
      "tags": ["barbie", "evening gown", "vintage", "handmade", "pink"],
      "seo_title": "...",
      "seo_description": "...",
      "inventory_quantity": 1,
      "status": "active",
      "created_by": "ai"
    }
    ↓
[8] UPDATE GOOGLE SHEETS (Inventory Tracker)
    Add row: [SKU | Title | Price | Stock | Date Added | Source Email]
    ↓
[9] REVALIDATE NEXT.JS (ISR Webhook)
    POST https://yourdollstore.com/api/revalidate?path=/products
    ↓
[10] SEND CONFIRMATION EMAIL (Resend)
    To: You
    Subject: "✅ Product Published: {title}"
    Body: "Your product is now live!
           View: https://yourdollstore.com/products/{handle}
           
           Details:
           • SKU: {sku}
           • Price: ${price}
           • Auto-generated description ✓
           • Images uploaded ✓
           • SEO optimized ✓"
```

**⏱️ Total Time:** ~15-20 seconds from email sent to product live

---

### **WORKFLOW 2: Custom Quote Automation**

**Trigger:** Form submission on `/custom-request` page

**n8n Flow:**

```
[1] WEBHOOK TRIGGER
    Receives: {
      "customer_name": "Sarah",
      "customer_email": "sarah@email.com",
      "doll_type": "Bratz",
      "outfit_description": "Pink fur coat like the one in the photo",
      "reference_images": ["url1", "url2"],
      "budget": "100-150",
      "deadline": "2 weeks"
    }
    ↓
[2] UPLOAD IMAGES TO CLOUDINARY
    • Store reference photos
    • Generate thumbnails
    • Get permanent URLs
    ↓
[3] AI COMPLEXITY ANALYSIS (Claude 4 Sonnet API)
    Prompt: "Analyze this custom doll outfit request:
            Doll: {doll_type}
            Description: {outfit_description}
            Reference Images: [analyze images]
            Budget: {budget}
            Deadline: {deadline}
            
            Provide:
            1. Complexity Score (1-10)
            2. Estimated Hours of Work
            3. Material Difficulty
            4. Special Challenges
            5. Recommended Price Range
            6. Feasibility Assessment
            
            Return as JSON with reasoning."
    ↓
[4] SAVE TO DATABASE (FastAPI Webhook)
    POST /api/custom-quotes
    {
      "customer_email": "...",
      "doll_type": "...",
      "outfit_description": "...",
      "reference_images": [...],
      "status": "pending",
      "ai_analysis": {ai_response}
    }
    Returns: {quote_id, quote_number}
    ↓
[5] SAVE TO AIRTABLE (CRM)
    Create record in "Custom Requests" table:
    • Quote Number
    • Customer Name/Email
    • Doll Type
    • Description
    • AI Complexity Score
    • Status: "Awaiting Your Response"
    • Reference Images (attachments)
    ↓
[6] SEND YOU NOTIFICATION EMAIL (Resend)
    To: You
    Subject: "🎨 New Custom Request: {doll_type} outfit"
    Body: "
    Customer: {customer_name} ({customer_email})
    Doll: {doll_type}
    Budget: {budget}
    Deadline: {deadline}
    
    Request:
    {outfit_description}
    
    AI Analysis:
    • Complexity: {score}/10
    • Est. Hours: {hours}
    • Suggested Price: ${price_range}
    
    Reference Photos: [attached]
    
    📧 TO QUOTE: Simply reply to this email with your price.
    Example: '$150'
    
    The system will automatically:
    1. Generate a professional PDF quote
    2. Email it to the customer
    3. Include a payment link
    4. Update your CRM
    "
    Reply-To: custom-quotes@yourdollstore.com (monitored by n8n)
    ↓
[7] SEND CUSTOMER ACKNOWLEDGMENT (Resend)
    To: Customer
    Subject: "We received your custom outfit request!"
    Body: "Hi {customer_name},
    
    Thank you for your custom request! We're reviewing your {doll_type} outfit design.
    
    What happens next:
    • We'll analyze your reference photos
    • You'll receive a personalized quote within 24 hours
    • If you approve, we'll create your one-of-a-kind piece
    
    Request #: {quote_number}
    
    Questions? Just reply to this email.
    
    - The Doll Couture Team"
```

**Now you wait for your email reply...**

```
[8] EMAIL TRIGGER (Gmail - monitors custom-quotes@yourdollstore.com)
    Detects reply from you with price
    Example: "$150" or "Quote: $150, ready in 10 days"
    ↓
[9] PARSE YOUR REPLY
    • Extract price using regex
    • Extract delivery days (optional)
    • Extract any custom notes
    ↓
[10] UPDATE DATABASE (FastAPI)
    PATCH /api/custom-quotes/{quote_id}
    {
      "status": "quoted",
      "quoted_price": 150.00,
      "quoted_delivery_days": 10,
      "quote_valid_until": "7 days from now"
    }
    ↓
[11] GENERATE QUOTE PDF (Python Script Node)
    Using ReportLab or WeasyPrint:
    
    ┌─────────────────────────────────────┐
    │     YOUR LOGO                       │
    │                                     │
    │  CUSTOM OUTFIT QUOTATION            │
    │  Quote #: QUO-2024-0001             │
    │  Date: March 11, 2026               │
    │                                     │
    │  For: Sarah Johnson                 │
    │  Email: sarah@email.com             │
    │                                     │
    │  ─────────────────────────────      │
    │                                     │
    │  ITEM DETAILS                       │
    │  Doll Type: Bratz                   │
    │  Description: Pink fur coat         │
    │                                     │
    │  [Reference Image Thumbnails]       │
    │                                     │
    │  ─────────────────────────────      │
    │                                     │
    │  PRICING                            │
    │  Custom Design & Creation: $150.00  │
    │                                     │
    │  Estimated Delivery: 10 business    │
    │  days from order confirmation       │
    │                                     │
    │  Valid Until: March 18, 2026        │
    │                                     │
    │  ─────────────────────────────      │
    │                                     │
    │  [ACCEPT & PAY BUTTON]              │
    │  → Secure Checkout Link             │
    │                                     │
    │  Questions? Reply to this quote.    │
    └─────────────────────────────────────┘
    ↓
[12] UPLOAD PDF TO CLOUDINARY
    • Get permanent URL
    • Save PDF ID for later retrieval
    ↓
[13] CREATE STRIPE PAYMENT LINK
    POST https://api.stripe.com/v1/payment_links
    {
      "line_items": [{
        "price_data": {
          "currency": "usd",
          "unit_amount": 15000,
          "product_data": {
            "name": "Custom Bratz Outfit - Quote #QUO-2024-0001",
            "description": "Pink fur coat",
            "images": [reference_image_urls]
          }
        },
        "quantity": 1
      }],
      "after_completion": {
        "type": "redirect",
        "redirect": {
          "url": "https://yourdollstore.com/quote-accepted?id={quote_id}"
        }
      },
      "metadata": {
        "quote_id": "{quote_id}",
        "type": "custom_quote"
      }
    }
    Returns: {payment_link_url}
    ↓
[14] SEND QUOTE EMAIL TO CUSTOMER (Resend)
    To: Customer
    Subject: "Your custom {doll_type} outfit quote is ready!"
    Body: "Hi {customer_name},
    
    Great news! We can create your custom {doll_type} outfit.
    
    📄 View Your Full Quote (PDF):
    {pdf_download_link}
    
    💰 PRICE: $150.00
    ⏱️ DELIVERY: 10 business days after order
    ✅ VALID UNTIL: March 18, 2026
    
    Ready to bring your vision to life?
    
    [SECURE CHECKOUT BUTTON]
    {stripe_payment_link}
    
    This quote includes:
    • Custom design based on your references
    • Hand-crafted with premium materials
    • Perfect fit for {doll_type}
    • Free shipping
    
    Have questions? Just reply to this email.
    
    - The Doll Couture Team"
    
    Attachments: quote-{quote_number}.pdf
    ↓
[15] UPDATE AIRTABLE CRM
    Update record status: "Quote Sent"
    Add fields:
    • Quoted Price
    • Quote PDF URL
    • Payment Link
    • Quote Sent Date
    ↓
[16] SEND YOU CONFIRMATION (Resend)
    To: You
    Subject: "✅ Quote sent to {customer_name}"
    Body: "Your quote for ${price} has been emailed to the customer.
           Payment link: {stripe_payment_link}
           
           They have 7 days to accept."
```

**If customer pays:**

```
[17] STRIPE WEBHOOK (payment_intent.succeeded)
    ↓
[18] UPDATE DATABASE
    • Quote status → "accepted"
    • Create order record
    • Link order to quote
    ↓
[19] UPDATE AIRTABLE
    Status → "Paid - In Production"
    ↓
[20] SEND PRODUCTION NOTIFICATION (Resend)
    To: You
    Subject: "🎉 Custom Order Paid: {customer_name}"
    Body: "Customer has paid ${price}
           Start creating: {outfit_description}
           Expected delivery: {deadline}
           
           Order Details: [Airtable link]"
    ↓
[21] SEND CUSTOMER CONFIRMATION (Resend)
    To: Customer
    Subject: "Order confirmed! Your custom {doll_type} outfit is in production"
    Body: "Hi {customer_name},
    
    Payment received! We're starting work on your custom outfit today.
    
    Order #: {order_number}
    Expected Delivery: {delivery_date}
    
    You'll receive:
    • Progress updates
    • Shipping notification with tracking
    • Care instructions
    
    Track your order: https://yourdollstore.com/orders/{order_id}
    
    Thank you for your order!
    - The Doll Couture Team"
```

**⏱️ Total Time:** 
- Initial request acknowledgment: ~10 seconds
- Quote generation after your reply: ~30 seconds
- Payment confirmation: ~5 seconds

---

### **WORKFLOW 3: Order Fulfillment Automation**

**Trigger:** Stripe webhook `checkout.session.completed`

```
[1] STRIPE WEBHOOK
    Receives payment confirmation
    ↓
[2] FETCH STRIPE SESSION DATA
    Get line items, customer email, shipping address
    ↓
[3] CREATE ORDER IN DATABASE (FastAPI)
    POST /api/orders
    {
      "customer_email": "...",
      "line_items": [...],
      "total": 89.00,
      "shipping_address": {...},
      "stripe_payment_intent_id": "...",
      "financial_status": "paid",
      "fulfillment_status": "unfulfilled"
    }
    Returns: {order_id, order_number}
    ↓
[4] UPDATE INVENTORY (FastAPI)
    For each product in order:
    PATCH /api/products/{product_id}/inventory
    {
      "quantity_change": -1,
      "reason": "sale",
      "order_id": "{order_id}"
    }
    ↓
[5] CHECK STOCK LEVELS
    If product.inventory_quantity == 0:
      • Update product status → "sold_out"
      • Trigger Workflow 8 (Waitlist Notifications)
    
    If product.inventory_quantity <= 2:
      • Send you low stock alert
    ↓
[6] UPDATE GOOGLE SHEETS
    Add row to "Orders" sheet:
    [Date | Order# | Customer | Items | Total | Status | Tracking]
    
    Update "Products" sheet:
    Decrease stock count for sold items
    ↓
[7] CREATE AIRTABLE RECORD
    Table: "Orders"
    • Order Number
    • Customer Name/Email
    • Items (linked to Products table)
    • Total Amount
    • Status: "Needs Shipping"
    • Payment Date
    • Shipping Address
    ↓
[8] SEND YOU PACKING NOTIFICATION (Resend)
    To: You
    Subject: "📦 New Order to Fulfill: Order #{order_number}"
    Body: "
    ORDER DETAILS
    ─────────────
    Order: #{order_number}
    Customer: {customer_name}
    Email: {customer_email}
    
    ITEMS TO PACK:
    • {item_1_title} (SKU: {sku_1})
    • {item_2_title} (SKU: {sku_2})
    
    TOTAL: ${total}
    
    SHIP TO:
    {shipping_address_formatted}
    
    ─────────────
    
    📋 Packing Checklist:
    □ Verify items
    □ Quality check
    □ Package securely
    □ Include care card
    □ Add thank you note
    
    When shipped, reply with tracking number.
    
    View order: {airtable_record_url}
    "
    Reply-To: shipping@yourdollstore.com
    ↓
[9] SEND CUSTOMER ORDER CONFIRMATION (Resend)
    To: Customer
    Subject: "Order confirmed! #{order_number}"
    Body: "Hi {customer_name},
    
    Thank you for your purchase! Your order is confirmed and will ship soon.
    
    ORDER SUMMARY
    ─────────────
    {item_list_formatted}
    
    Subtotal: ${subtotal}
    Shipping: ${shipping}
    Total: ${total}
    
    SHIPPING ADDRESS
    {shipping_address_formatted}
    
    You'll receive a tracking number once your order ships (usually within 1-2 business days).
    
    Track your order: https://yourdollstore.com/orders/{order_id}
    
    Questions? Just reply to this email.
    
    - The Doll Couture Team"
```

**When you reply with tracking:**

```
[10] EMAIL TRIGGER (shipping@yourdollstore.com)
    Detects your reply with tracking number
    Example: "UPS: 1Z999AA10123456784"
    ↓
[11] PARSE TRACKING INFO
    • Extract carrier (USPS, UPS, FedEx, DHL)
    • Extract tracking number
    • Generate tracking URL based on carrier
    ↓
[12] UPDATE ORDER (FastAPI)
    PATCH /api/orders/{order_id}
    {
      "fulfillment_status": "fulfilled",
      "tracking_number": "1Z999AA10123456784",
      "tracking_url": "https://www.ups.com/track?tracknum=...",
      "fulfilled_at": "2026-03-11T14:30:00Z"
    }
    ↓
[13] UPDATE GOOGLE SHEETS
    Update order row:
    Status → "Shipped"
    Tracking → {tracking_number}
    ↓
[14] UPDATE AIRTABLE
    Status → "Shipped"
    Tracking Number → {tracking_number}
    Shipped Date → {today}
    ↓
[15] SEND SHIPPING CONFIRMATION (Resend)
    To: Customer
    Subject: "Your order has shipped! 📦"
    Body: "Hi {customer_name},
    
    Great news! Your order #{order_number} is on its way.
    
    TRACKING INFORMATION
    Carrier: UPS
    Tracking #: 1Z999AA10123456784
    
    [TRACK YOUR PACKAGE BUTTON]
    {tracking_url}
    
    Expected Delivery: {estimated_delivery_date}
    
    Care Instructions:
    • Hand wash delicate items
    • Lay flat to dry
    • Store in a cool, dry place
    
    We hope you love your new doll outfits! Please share photos on Instagram and tag us @yourdollstore
    
    - The Doll Couture Team"
    ↓
[16] SCHEDULE REVIEW REQUEST (Delay 7 days)
    Trigger Workflow 7 in 7 days
```

---

### **WORKFLOW 4: Inventory Alerts**

**Trigger:** Product inventory changes (via database webhook)

```
[1] DATABASE WEBHOOK
    Triggered when products.inventory_quantity changes
    ↓
[2] CHECK THRESHOLDS
    
    IF inventory == 0:
      ↓
    [3a] UPDATE PRODUCT STATUS
        PATCH /api/products/{id}
        {"status": "sold_out"}
        ↓
    [4a] SEND SOLD OUT ALERT (Resend)
        To: You
        Subject: "🚨 SOLD OUT: {product_title}"
        Body: "Your product is now sold out:
               • {product_title}
               • SKU: {sku}
               • Last sold at: ${price}
               
               Actions you can take:
               • Create a new one (email a photo)
               • Update stock if you have more
               • Archive the listing
               
               {waitlist_count} customers are waiting for restock!"
        ↓
    [5a] UPDATE GOOGLE SHEETS
        Mark product row as "SOLD OUT"
    
    ELSE IF inventory <= 2:
      ↓
    [3b] SEND LOW STOCK WARNING (Resend)
        To: You
        Subject: "⚠️ Low Stock: {product_title}"
        Body: "Only {inventory_quantity} left in stock:
               • {product_title}
               • SKU: {sku}
               
               This is a popular item - consider restocking soon!"
    
    ELSE IF inventory >= 10 AND was_below_10:
      ↓
    [3c] SEND RESTOCK CONFIRMATION (Resend)
        To: You
        Subject: "✅ Restocked: {product_title}"
        Body: "{product_title} is back in good stock ({inventory_quantity} available)"
```

---

### **WORKFLOW 5: Customer Lifecycle Emails**

**Trigger:** Various events

```
NEW CUSTOMER (First Order):
[1] STRIPE WEBHOOK → First purchase detected
    ↓
[2] SEND WELCOME EMAIL (Resend)
    Subject: "Welcome to the Doll Couture family! 🎀"
    Body: "Hi {customer_name},
    
    Thank you for your first order! We're thrilled to have you.
    
    As a thank you, here's 10% off your next purchase:
    Code: WELCOME10
    
    Follow us on Instagram @yourdollstore for:
    • New arrivals
    • Behind-the-scenes
    • Styling tips
    • Exclusive drops
    
    - The Doll Couture Team"
    ↓
[3] ADD TO AIRTABLE
    Create customer record with tag "New Customer"

───────────────────────────────────

REPEAT CUSTOMER (2nd Order):
[1] Order created → Check customer.total_orders
    ↓
[2] IF total_orders == 2:
    SEND VIP EMAIL (Resend)
    Subject: "You're officially a VIP! ✨"
    Body: "Hi {customer_name},
    
    We notice you're back for more! Welcome to our VIP family.
    
    VIP Perks:
    • Early access to new collections
    • Free shipping on orders over $50
    • Exclusive custom requests
    
    Your VIP code: VIP15 (15% off your next order)
    
    - The Doll Couture Team"

───────────────────────────────────

INACTIVE CUSTOMER (30 days since last order):
[1] SCHEDULED TRIGGER (Daily at 9am)
    ↓
[2] QUERY DATABASE
    SELECT * FROM customers
    WHERE last_order_date < NOW() - INTERVAL '30 days'
    AND total_orders >= 1
    AND email_marketing_consent = true
    ↓
[3] FOR EACH inactive customer:
    SEND WIN-BACK EMAIL (Resend)
    Subject: "We miss you! Here's 20% off 💕"
    Body: "Hi {customer_name},
    
    We haven't seen you in a while! We've added new pieces you might love:
    
    [Top 3 New Products - Personalized based on past purchases]
    
    Come back with 20% off:
    Code: COMEBACK20
    Valid for 7 days
    
    - The Doll Couture Team"

───────────────────────────────────

BIRTHDAY (if collected):
[1] SCHEDULED TRIGGER (Daily at 8am)
    ↓
[2] QUERY DATABASE
    SELECT * FROM customers
    WHERE EXTRACT(MONTH FROM birthday) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(DAY FROM birthday) = EXTRACT(DAY FROM CURRENT_DATE)
    ↓
[3] SEND BIRTHDAY EMAIL (Resend)
    Subject: "Happy Birthday from Doll Couture! 🎂"
    Body: "Happy Birthday {customer_name}!
    
    Treat yourself (or your dolls) to something special:
    
    Use code BIRTHDAY25 for 25% off
    Valid through {expiry_date}
    
    🎁 Shop now: {shop_url}
    
    - The Doll Couture Team"
```

---

### **WORKFLOW 6: Abandoned Cart Recovery**

**Trigger:** Cart inactive for 1 hour

```
[1] SCHEDULED TRIGGER (Every 15 minutes)
    ↓
[2] QUERY DATABASE
    SELECT * FROM abandoned_carts
    WHERE abandoned_at < NOW() - INTERVAL '1 hour'
    AND recovered = false
    AND recovery_email_sent_at IS NULL
    ↓
[3] FOR EACH abandoned cart:
    
    [4] SEND RECOVERY EMAIL #1 (Resend)
        To: Customer
        Subject: "You left something in your cart..."
        Body: "Hi there!
        
        Looks like you got distracted. We saved your items:
        
        {cart_items_with_images}
        
        Total: ${subtotal}
        
        [COMPLETE CHECKOUT BUTTON]
        {checkout_link}
        
        These items are popular and might sell out soon!
        
        - The Doll Couture Team"
        ↓
    [5] UPDATE DATABASE
        UPDATE abandoned_carts
        SET recovery_email_sent_at = NOW(),
            recovery_email_count = 1
        
        ↓
    [6] WAIT 24 HOURS
        ↓
    [7] IF still not recovered:
        SEND RECOVERY EMAIL #2 (Resend)
        Subject: "Still interested? Here's 10% off"
        Body: "Hi again!
        
        Your cart is still waiting, and we'd love to help you complete your order.
        
        Use code CART10 for 10% off these items:
        {cart_items}
        
        [COMPLETE CHECKOUT - 10% OFF]
        {checkout_link_with_discount}
        
        This offer expires in 48 hours.
        
        - The Doll Couture Team"
        ↓
    [8] UPDATE DATABASE
        UPDATE abandoned_carts
        SET recovery_email_count = 2
        
        ↓
    [9] WAIT 48 HOURS
        ↓
    [10] IF still not recovered:
        SEND FINAL EMAIL (Resend)
        Subject: "Last chance: Your cart expires tonight"
        Body: "Hi there,
        
        This is your final reminder - your saved cart will expire at midnight.
        
        Don't miss out on:
        {cart_items}
        
        Your 10% discount is still active: CART10
        
        [CHECKOUT NOW]
        {checkout_link}
        
        After tonight, these items may be gone.
        
        - The Doll Couture Team"
        ↓
    [11] UPDATE DATABASE
        UPDATE abandoned_carts
        SET recovery_email_count = 3
```

**If customer completes checkout:**

```
[12] STRIPE WEBHOOK → Order created
    ↓
[13] MATCH ORDER TO ABANDONED CART
    Match by customer_email + session_id
    ↓
[14] UPDATE DATABASE
    UPDATE abandoned_carts
    SET recovered = true,
        recovered_at = NOW()
    ↓
[15] LOG METRICS
    Track recovery rate for analytics
```

---

### **WORKFLOW 7: Review Request Automation**

**Trigger:** 7 days after order fulfillment

```
[1] SCHEDULED TRIGGER (Daily at 10am)
    ↓
[2] QUERY DATABASE
    SELECT * FROM orders
    WHERE fulfilled_at < NOW() - INTERVAL '7 days'
    AND fulfilled_at > NOW() - INTERVAL '8 days'
    AND financial_status = 'paid'
    AND id NOT IN (
      SELECT order_id FROM product_reviews
    )
    ↓
[3] FOR EACH eligible order:
    
    [4] FETCH CUSTOMER DATA
        GET /api/customers/{customer_id}
        ↓
    [5] SEND REVIEW REQUEST (Resend)
        To: Customer
        Subject: "How are you loving your doll outfits? 💕"
        Body: "Hi {customer_name},
        
        It's been a week since your order arrived. We hope your dolls are loving their new wardrobe!
        
        Would you mind sharing your thoughts? Your review helps other doll enthusiasts discover handmade quality.
        
        [WRITE A REVIEW BUTTON]
        https://yourdollstore.com/orders/{order_id}/review
        
        As a thank you, you'll get 15% off your next order after submitting your review.
        
        Photos of your dolls in their outfits are especially appreciated! 📸
        
        - The Doll Couture Team"
        ↓
    [6] LOG EMAIL SENT
        Track in database for metrics
        
    [IF customer clicks review link:]
        ↓
    [7] CUSTOMER SUBMITS REVIEW
        POST /api/product-reviews
        {
          "product_id": "...",
          "order_id": "...",
          "rating": 5,
          "title": "Absolutely perfect!",
          "content": "The quality is amazing...",
          "images": [uploaded_photos]
        }
        ↓
    [8] SEND THANK YOU EMAIL (Resend)
        To: Customer
        Subject: "Thank you for your review! Here's 15% off 🎉"
        Body: "Hi {customer_name},
        
        Thank you so much for taking the time to review your purchase!
        
        Your feedback means the world to us and helps other doll lovers find quality handmade outfits.
        
        As promised, here's 15% off your next order:
        Code: REVIEW15
        
        [SHOP NOW]
        
        - The Doll Couture Team"
        ↓
    [9] MODERATE REVIEW (optional manual step)
        If auto-approve is disabled:
        • Send you email with review content
        • You reply "approve" or "reject"
        • n8n updates review status
```

---

### **WORKFLOW 8: Restock Notification System**

**Trigger:** Product goes from sold_out to in_stock

```
[1] DATABASE WEBHOOK
    Triggered when products.inventory_quantity changes from 0 to >0
    ↓
[2] QUERY WAITLIST
    SELECT * FROM product_waitlist
    WHERE product_id = {product_id}
    AND notified = false
    ↓
[3] FOR EACH waitlist customer:
    
    [4] SEND RESTOCK NOTIFICATION (Resend)
        To: Customer
        Subject: "It's back! {product_title}"
        Body: "Hi there!
        
        Great news - the item you were waiting for is back in stock:
        
        {product_title}
        {product_image}
        
        Price: ${price}
        Stock: Limited quantity
        
        [SHOP NOW BUTTON]
        https://yourdollstore.com/products/{handle}
        
        These tend to sell fast - don't miss out!
        
        - The Doll Couture Team"
        ↓
    [5] UPDATE WAITLIST
        UPDATE product_waitlist
        SET notified = true,
            notified_at = NOW()
        WHERE id = {waitlist_id}
        ↓
    [6] WAIT 5 MINUTES
        (Throttle emails to avoid spam flags)
```

---

## 📧 GOOGLE SHEETS INTEGRATION (Real-Time Inventory)

**Sheet Structure:**

**Tab 1: "Products"**
```
| SKU        | Title                    | Price | Stock | Status    | Last Sold | Total Sales | Date Added  | Source |
|------------|--------------------------|-------|-------|-----------|-----------|-------------|-------------|--------|
| BRB-DRS-A4K9 | Vintage Rose Gown      | $45   | 0     | SOLD OUT  | Mar 11    | 3           | Mar 5, 2026 | AI     |
| BRT-SHO-B2L7 | Platform Boots         | $28   | 5     | Active    | Mar 10    | 12          | Feb 20, 2026| Manual |
```

**Tab 2: "Orders"**
```
| Date       | Order #    | Customer         | Items               | Total | Status  | Tracking        |
|------------|------------|------------------|---------------------|-------|---------|-----------------|
| Mar 11, 2026 | #1001    | Sarah Johnson    | Vintage Rose Gown   | $45   | Shipped | UPS: 1Z999...   |
| Mar 10, 2026 | #1000    | Emma Williams    | Platform Boots (2x) | $56   | Shipped | USPS: 9400...   |
```

**Tab 3: "Custom Quotes"**
```
| Date       | Quote #   | Customer      | Doll Type | Description      | Status  | Price | Paid? |
|------------|-----------|---------------|-----------|------------------|---------|-------|-------|
| Mar 11     | QUO-0001  | Lisa Chen     | Bratz     | Pink fur coat    | Quoted  | $150  | No    |
| Mar 9      | QUO-0002  | Amy Park      | Barbie    | Wedding dress    | Paid    | $200  | Yes   |
```

**Why Google Sheets?**
- You can view on your phone
- Easy to share with assistants
- Built-in formulas for analytics
- No learning curve
- Auto-synced via n8n

---

## 🎨 FRONTEND FEATURES (Next.js)

### **Core Pages:**

```
/                          → Homepage with featured products
/products                  → Product grid with filters
/products/[handle]         → Individual product page
/collections/[name]        → Category pages (Dresses, Shoes, etc.)
/custom-request            → Custom outfit form
/cart                      → Shopping cart
/checkout                  → Stripe checkout
/orders/[id]               → Order tracking
/orders/[id]/review        → Review submission
/search                    → Product search
/about                     → About page
/contact                   → Contact form
```

### **Key Features:**

#### 1. **Real-Time Inventory Display**
```typescript
// Uses React Query to poll inventory every 30 seconds
const { data: product } = useQuery({
  queryKey: ['product', handle],
  queryFn: () => fetch(`/api/products/${handle}`).then(r => r.json()),
  refetchInterval: 30000 // 30 seconds
});

// Shows live stock count
{product.inventory_quantity > 0 ? (
  <p className="text-green-500">
    {product.inventory_quantity} in stock
  </p>
) : (
  <div>
    <p className="text-red-500">Sold Out</p>
    <WaitlistForm productId={product.id} />
  </div>
)}
```

#### 2. **Waitlist Form (for sold-out items)**
```typescript
// When product is sold out, show waitlist signup
<form onSubmit={joinWaitlist}>
  <input 
    type="email" 
    placeholder="Get notified when back in stock"
  />
  <button>Notify Me</button>
</form>

// Submits to: POST /api/waitlist
// Triggers n8n Workflow 8 when restocked
```

#### 3. **Smart Search with Meilisearch**
```typescript
// Instant, typo-tolerant search
const { hits } = await meiliClient.index('products').search('bratz dres', {
  attributesToHighlight: ['title', 'description'],
  filter: 'status = active',
  sort: ['created_at:desc']
});

// Finds "Bratz Dress" even with typo
```

#### 4. **Dynamic Product Recommendations**
```typescript
// "You might also like" section
// Based on: same doll type, similar price, same category
const recommendations = await fetch(`/api/products/recommendations`, {
  method: 'POST',
  body: JSON.stringify({
    currentProductId: product.id,
    dollType: product.metadata.doll_type,
    category: product.category,
    priceRange: [product.price * 0.8, product.price * 1.2]
  })
});
```

#### 5. **Abandoned Cart Tracking**
```typescript
// Saves cart to database on any change
useEffect(() => {
  const saveCart = debounce(() => {
    fetch('/api/abandoned-carts', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        customer_email: user?.email,
        items: cart.items,
        subtotal: cart.subtotal
      })
    });
  }, 2000);
  
  saveCart();
}, [cart]);
```

---

## 💳 STRIPE INTEGRATION

### **Payment Methods Accepted:**
- Credit/Debit Cards (Visa, Mastercard, Amex)
- Apple Pay
- Google Pay
- Afterpay/Klarna (Buy Now Pay Later)

### **Key Stripe Features:**

#### 1. **Automatic Tax Calculation**
```javascript
// Stripe Tax calculates sales tax automatically
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [...],
  automatic_tax: { enabled: true },
  shipping_address_collection: {
    allowed_countries: ['US', 'CA', 'GB', 'AU']
  }
});
```

#### 2. **Payment Intent Webhooks**
```javascript
// backend/webhooks/stripe.py
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, STRIPE_WEBHOOK_SECRET
    )
    
    if event.type == 'checkout.session.completed':
        # Trigger n8n Workflow 3 (Order Fulfillment)
        await trigger_n8n_webhook('order-fulfillment', event.data.object)
    
    elif event.type == 'payment_intent.succeeded':
        # Update order status to paid
        await update_order_status(event.data.object.metadata.order_id, 'paid')
    
    return {"status": "success"}
```

---

## 📊 ANALYTICS & REPORTING

### **PostHog Dashboard (Self-Hosted)**

**Tracked Events:**
- Product Views
- Add to Cart
- Checkout Started
- Purchase Completed
- Custom Quote Submitted
- Review Left
- Waitlist Joined

**Custom Metrics:**
```javascript
// Track everything
posthog.capture('product_viewed', {
  product_id: product.id,
  product_title: product.title,
  price: product.price,
  category: product.category
});

posthog.capture('custom_quote_requested', {
  doll_type: formData.doll_type,
  estimated_value: formData.budget
});
```

**Automated Reports (n8n):**
```
WORKFLOW 9: Weekly Analytics Email

[1] SCHEDULED TRIGGER (Every Monday 8am)
    ↓
[2] QUERY POSTHOG API
    • Total sales this week
    • Top 5 products
    • Conversion rate
    • Average order value
    • Custom quote requests
    ↓
[3] QUERY DATABASE
    • Total orders
    • Total revenue
    • New customers
    • Repeat customer rate
    ↓
[4] GENERATE REPORT EMAIL (Resend)
    To: You
    Subject: "📊 Weekly Report: {week_start} - {week_end}"
    Body: "
    SALES OVERVIEW
    ─────────────
    Revenue: ${total_revenue}
    Orders: {order_count}
    Avg Order Value: ${aov}
    
    TOP PRODUCTS
    1. {product_1} - ${revenue_1}
    2. {product_2} - ${revenue_2}
    3. {product_3} - ${revenue_3}
    
    CUSTOMERS
    New: {new_customers}
    Repeat: {repeat_customers}
    Lifetime Value: ${ltv}
    
    CUSTOM QUOTES
    Requested: {quote_requests}
    Accepted: {quote_accepted}
    Conversion: {quote_conversion}%
    
    INVENTORY ALERTS
    Sold Out: {sold_out_count} products
    Low Stock: {low_stock_count} products
    
    [View Full Dashboard]
    "
```

---

## 🔒 SECURITY & COMPLIANCE

### **Data Protection:**
```python
# FastAPI Security Headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdollstore.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdollstore.com", "api.yourdollstore.com"]
)

# Rate Limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/custom-quotes")
@limiter.limit("5/hour")  # Max 5 quote requests per hour
async def create_quote(request: Request):
    ...
```

### **PCI Compliance:**
- Stripe handles all payment data (PCI Level 1 certified)
- No credit card data touches your servers
- Stripe Elements for secure card input

### **GDPR Compliance:**
```python
# Customer data deletion endpoint
@app.delete("/api/customers/{id}/gdpr-delete")
async def gdpr_delete(id: UUID):
    # Anonymize orders (keep for accounting)
    await db.execute(
        "UPDATE orders SET customer_email = 'deleted@privacy.local' WHERE customer_id = $1",
        id
    )
    
    # Delete customer record
    await db.execute("DELETE FROM customers WHERE id = $1", id)
    
    # Remove from Airtable
    await airtable.delete_record(id)
    
    # Remove from email lists
    await resend.remove_contact(email)
    
    return {"status": "deleted"}
```

---

## 🚀 DEPLOYMENT ARCHITECTURE

### **Vercel (Frontend)**
```yaml
# vercel.json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "regions": ["iad1"], # US East (change based on your market)
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.yourdollstore.com",
    "NEXT_PUBLIC_STRIPE_KEY": "pk_live_...",
    "DATABASE_URL": "@database-url"
  },
  "crons": [
    {
      "path": "/api/cron/revalidate-products",
      "schedule": "0 * * * *" # Every hour
    }
  ]
}
```

### **Railway (Backend + n8n)**
```yaml
# railway.toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"

[[services]]
name = "api"
source = "api/"

[[services]]
name = "postgres"
image = "postgres:16"

[[services]]
name = "redis"
image = "redis:7-alpine"

[[services]]
name = "n8n"
image = "n8nio/n8n:latest"
env = {
  N8N_BASIC_AUTH_ACTIVE = "true",
  N8N_BASIC_AUTH_USER = "admin",
  WEBHOOK_URL = "https://n8n.yourdollstore.com"
}
```

---

## 📱 MOBILE OPTIMIZATION

### **PWA Features:**
```javascript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
});

module.exports = withPWA({
  // Next.js config
});
```

**Capabilities:**
- Add to Home Screen
- Offline product browsing (cached)
- Push notifications for order updates
- Fast loading (< 1 second)

---

## 💰 PRICING & COST ESTIMATE (Monthly)

| Service | Plan | Cost |
|---------|------|------|
| **Vercel** | Pro | $20/month |
| **Railway** | Hobby | $5/month (backend) |
| **Railway** | n8n + PostgreSQL + Redis | $15/month |
| **Cloudinary** | Free tier | $0 (up to 25GB) |
| **Stripe** | Pay as you go | 2.9% + $0.30 per transaction |
| **Resend** | Free tier | $0 (up to 3,000 emails/month) |
| **OpenAI API** | Pay as you go | ~$5/month (est. 100 products) |
| **Anthropic API** | Pay as you go | ~$3/month (est. 20 quotes) |
| **Domain** | Namecheap | $12/year (~$1/month) |
| **SSL** | Let's Encrypt | $0 (free) |
| **PostHog** | Self-hosted | $0 (included in Railway) |

**Total: ~$49/month** + transaction fees

**At $1000/month revenue:**
- Stripe fees: ~$30
- **Net: ~$79/month in tech costs**
- **Platform costs: 7.9% of revenue** (industry average is 10-15%)

---

## 🎯 SUCCESS METRICS (KPIs to Track)

### **Sales Metrics:**
- Daily/Weekly/Monthly Revenue
- Average Order Value (Target: $50+)
- Conversion Rate (Target: 2-4%)
- Cart Abandonment Rate (Target: <70%)
- Cart Recovery Rate (Target: >15%)

### **Product Metrics:**
- Products Added per Week (via AI vs Manual)
- Average Time to Sell Out
- Inventory Turnover Rate
- Most Popular Categories
- Price Sweet Spot

### **Customer Metrics:**
- New vs Returning Customer Ratio
- Customer Lifetime Value
- Repeat Purchase Rate
- Average Days Between Orders
- Review Rate (Target: >30%)

### **Automation Metrics:**
- AI Product Creation Success Rate
- Custom Quote Acceptance Rate
- Email Open Rates
- Waitlist Conversion Rate
- Time Saved per Week (manual vs automated)

---

## 📋 LAUNCH CHECKLIST

### **Pre-Launch (Week 1-2)**
- [ ] Set up Vercel account
- [ ] Set up Railway account
- [ ] Register domain name
- [ ] Set up Stripe account
- [ ] Set up Cloudinary account
- [ ] Set up Resend account
- [ ] Get OpenAI API key
- [ ] Get Anthropic API key
- [ ] Create brand assets (logo, colors)
- [ ] Write About page content

### **Development (Week 3-6)**
- [ ] Deploy Next.js frontend to Vercel
- [ ] Deploy FastAPI backend to Railway
- [ ] Deploy n8n to Railway
- [ ] Set up PostgreSQL database
- [ ] Set up Redis cache
- [ ] Connect Stripe webhooks
- [ ] Build n8n Workflow 1 (Product Creation)
- [ ] Build n8n Workflow 2 (Custom Quotes)
- [ ] Build n8n Workflow 3 (Order Fulfillment)
- [ ] Build n8n Workflows 4-8
- [ ] Set up Google Sheets integration
- [ ] Set up Airtable CRM
- [ ] Configure email templates
- [ ] Test all automations

### **Testing (Week 7)**
- [ ] Test product creation flow
- [ ] Test custom quote flow
- [ ] Test checkout process
- [ ] Test order fulfillment
- [ ] Test email deliverability
- [ ] Test mobile responsiveness
- [ ] Test payment processing
- [ ] Test abandoned cart recovery
- [ ] Test waitlist notifications
- [ ] Load testing (50+ concurrent users)

### **Launch (Week 8)**
- [ ] Add 10-20 initial products
- [ ] Set up Google Analytics
- [ ] Set up PostHog
- [ ] Configure SEO metadata
- [ ] Submit sitemap to Google
- [ ] Set up social media accounts
- [ ] Create launch email campaign
- [ ] Go live!

---

## 🆘 TROUBLESHOOTING GUIDE

### **n8n Workflow Not Triggering:**
1. Check webhook URL is correct
2. Verify email parsing regex
3. Check n8n execution logs
4. Test with manual trigger first

### **Product Not Appearing on Site:**
1. Check product status is "active"
2. Verify Next.js ISR revalidated
3. Check database connection
4. Clear Redis cache

### **Email Not Sending:**
1. Check Resend API key
2. Verify sender email is verified
3. Check spam folder
4. Review Resend logs

### **Stripe Payment Failing:**
1. Check webhook secret
2. Verify test vs live mode
3. Check customer card details
4. Review Stripe dashboard logs

---

## 🎓 TRAINING RESOURCES

### **You'll Need to Learn:**
- Basic n8n workflow building (2 hours)
- Airtable basics (1 hour)
- Stripe dashboard navigation (1 hour)
- Railway deployment (1 hour)

### **Recommended Resources:**
- n8n Academy: https://n8n.io/academy
- Stripe Documentation: https://stripe.com/docs
- Next.js Tutorial: https://nextjs.org/learn
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/

---

## 🔄 FUTURE ENHANCEMENTS

### **Phase 2 Features:**
- Multi-currency support (EUR, GBP, AUD)
- Subscription boxes (monthly doll outfit club)
- Referral program (give $10, get $10)
- Loyalty points system
- Instagram Shop integration
- TikTok Shop integration
- AR try-on (see outfit on your doll via camera)
- Video tutorials (sewing techniques)
- Pattern marketplace (sell your designs)

### **Advanced Automations:**
- AI-powered dynamic pricing based on demand
- Predictive inventory (forecast what to make next)
- Automatic social media posting
- Influencer outreach automation
- Competitor price monitoring
- Trend analysis from Pinterest/Instagram

---

## ✅ FINAL SYSTEM DIAGRAM

```
YOU (The Creator)
     │
     │ 1. Take photo → Email
     │ 2. Reply with tracking
     │ 3. Reply with quote price
     │
     ├────────────────────────┐
     │                        │
     ▼                        ▼
  GMAIL                   MANUAL INPUT
(products@store.com)     (Phone, computer)
(shipping@store.com)
(quotes@store.com)
     │
     ├─────> n8n AUTOMATION ENGINE <─────┐
     │           │                       │
     │           ├─> AI APIs (GPT-4o, Claude)
     │           ├─> Cloudinary (Images)
     │           ├─> Stripe (Payments)
     │           ├─> Resend (Emails)
     │           ├─> Google Sheets
     │           └─> Airtable CRM
     │
     ▼
  FASTAPI BACKEND
     │
     ├─> PostgreSQL (Database)
     ├─> Redis (Cache)
     └─> Webhooks
         │
         ▼
  NEXT.JS FRONTEND (Vercel)
     │
     ▼
  CUSTOMERS
(Browse, Buy, Request Customs)
```

---

## 🏁 SUMMARY

**What makes this system special:**

1. **Zero Admin Work:** Email a photo = instant product listing
2. **AI-Powered:** Descriptions, quotes, complexity analysis all automated
3. **Customer Obsessed:** Abandoned carts, waitlists, review requests, win-backs
4. **Real-Time:** Live inventory, instant notifications, immediate confirmations
5. **Scalable:** Handles 1 order/day or 100 orders/day with same effort
6. **Professional:** Matches quality of $50k+ custom e-commerce sites
7. **Future-Proof:** 2026 tech stack, easy to add features
8. **Data-Driven:** Analytics, A/B testing, customer insights

**Your daily workflow:**
1. Create outfit
2. Take photo
3. Email photo with price
4. *[System does everything else]*
5. Reply with tracking when you ship
6. *[Done!]*

**Result:** World-class luxury doll clothing e-commerce empire that runs on autopilot while you focus on your craft.

---

**Ready to build?** Say "Let's start Phase 2" and we'll begin coding the foundation! 🚀
