"""Full endpoint test - tests GET + POST endpoints against live server."""
import urllib.request, json, sys

BASE = "http://127.0.0.1:8000"

def get(path, expect_status=200):
    try:
        with urllib.request.urlopen(BASE + path, timeout=3) as r:
            data = json.loads(r.read())
            if isinstance(data, list):
                print(f"  {r.status} GET  {path} -> {len(data)} items")
            else:
                print(f"  {r.status} GET  {path} -> {list(data.keys())[:4]}")
            return data
    except urllib.error.HTTPError as e:
        print(f"  {e.code} ERR  GET  {path}")
        return None
    except Exception as e:
        print(f"  ERR      GET  {path}: {str(e)[:60]}")
        return None

def post(path, payload, expect_status=200):
    try:
        body = json.dumps(payload).encode()
        req = urllib.request.Request(BASE + path, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            if isinstance(data, dict):
                print(f"  {r.status} POST {path} -> {list(data.keys())[:4]}")
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:120]
        print(f"  {e.code} ERR  POST {path}: {body}")
        return None
    except Exception as e:
        print(f"  ERR      POST {path}: {str(e)[:60]}")
        return None

print("\n=== GET ENDPOINTS ===")
products = get("/api/v1/products/")
get("/api/v1/products/categories")
get("/api/v1/orders/")
get("/api/v1/customers/")
get("/api/v1/cart/test-session-abc")
get("/api/v1/wishlist/test-session-abc")
get("/api/v1/subscribe/count")
get("/health")

print("\n=== POST ENDPOINTS ===")

# Subscribe
post("/api/v1/subscribe", {"email": "test@example.com", "source": "footer"})

# Promo code
post("/api/v1/promo/validate", {"code": "WELCOME10", "order_subtotal": 100.0})
post("/api/v1/promo/validate", {"code": "BRATZ20", "order_subtotal": 150.0})
post("/api/v1/promo/validate", {"code": "FAKECODE", "order_subtotal": 50.0})

# Cart save
post("/api/v1/cart", {
    "session_id": "test-session-abc",
    "items": [{"product_id": "p1", "product_name": "Test Doll", "price": 59.99, "quantity": 1}]
})

# Wishlist toggle
first_product_id = products[0]["id"] if products else "test-id"
post("/api/v1/wishlist/toggle", {"session_id": "test-session-abc", "product_id": first_product_id})

# Create customer
customer = post("/api/v1/customers/", {"email": "test@bratz.com", "first_name": "Test", "last_name": "User"})

# Create order
if customer and products:
    order = post("/api/v1/orders/", {
        "customer_email": "test@bratz.com",
        "customer_name": "Test User",
        "line_items": [{"product_id": products[0]["id"], "product_name": products[0]["title"], "quantity": 1, "price": products[0]["price"]}],
        "subtotal": products[0]["price"],
        "total": products[0]["price"],
        "tax": 0,
        "shipping": 0,
        "discount": 0,
    })

# Quote submission
post("/api/v1/quotes/", {
    "customer_email": "test@bratz.com",
    "customer_name": "Test User",
    "outfit_description": "Dark fantasy Bratz with wings",
    "doll_type": "Bratz",
    "budget": "200-400",
})

print("\n=== RE-CHECK GET AFTER POSTS ===")
get("/api/v1/orders/")
get("/api/v1/customers/")
get("/api/v1/cart/test-session-abc")
get("/api/v1/wishlist/test-session-abc")
get("/api/v1/subscribe/count")
print("\n  DONE!")
