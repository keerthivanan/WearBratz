"""
n8n Workflow Importer for Miastore
-----------------------------------
Run this script to automatically import all 5 Bratz Drip workflows into n8n.
n8n must be running at http://localhost:5678 first.

Usage:
    python import_n8n_workflows.py
    python import_n8n_workflows.py --api-key YOUR_KEY  (if auth required)
"""
import json
import os
import sys
import urllib.request
import urllib.error
import argparse

N8N_BASE = "http://localhost:5678"
WF_DIR = os.path.join(os.path.dirname(__file__), "..", "n8n_workflow&database")

WORKFLOW_FILES = [
    "01-new-order-processing.json",
    "02-order-shipped-notification.json",
    "03-low-stock-inventory-alert.json",
    "04-welcome-email-subscriber.json",
    "05-daily-sales-report.json",
]

def make_request(path, method="GET", data=None, api_key=None):
    url = N8N_BASE + path
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["X-N8N-API-KEY"] = api_key

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:200]
        return {"error": err, "status": e.code}, e.code

def check_n8n_running():
    try:
        with urllib.request.urlopen(N8N_BASE + "/healthz", timeout=3) as r:
            return True
    except:
        try:
            with urllib.request.urlopen(N8N_BASE + "/api/v1/workflows", timeout=3) as r:
                return True
        except:
            return False

def main():
    parser = argparse.ArgumentParser(description="Import workflows into n8n")
    parser.add_argument("--api-key", default=None, help="n8n API key (if auth is enabled)")
    args = parser.parse_args()

    print("\n🔍 Checking n8n connection...")
    if not check_n8n_running():
        print("❌ n8n is NOT running on http://localhost:5678")
        print("\nTo start n8n:")
        print("  1. npm install -g n8n   (first time only)")
        print("  2. n8n start")
        print("  3. Open http://localhost:5678")
        print("  4. Run this script again")
        sys.exit(1)

    print("✅ n8n is running!\n")

    # Check what workflows already exist
    existing, status = make_request("/api/v1/workflows", api_key=args.api_key)
    existing_names = [wf["name"] for wf in existing.get("data", [])]
    print(f"📋 Existing workflows: {len(existing_names)}")
    for name in existing_names:
        print(f"   - {name}")

    print()
    imported = 0
    skipped = 0
    failed = 0

    for fname in WORKFLOW_FILES:
        wf_path = os.path.join(WF_DIR, fname)
        if not os.path.exists(wf_path):
            print(f"  ⚠️  File not found: {fname}")
            failed += 1
            continue

        with open(wf_path, "r", encoding="utf-8") as f:
            wf_data = json.load(f)

        wf_name = wf_data.get("name", fname)

        if wf_name in existing_names:
            print(f"  ⏭️  SKIP (already exists): {wf_name}")
            skipped += 1
            continue

        result, status_code = make_request(
            "/api/v1/workflows",
            method="POST",
            data=wf_data,
            api_key=args.api_key
        )

        if status_code in (200, 201):
            wf_id = result.get("id", "?")
            print(f"  ✅ IMPORTED: {wf_name} (id={wf_id})")
            imported += 1
        else:
            print(f"  ❌ FAILED [{status_code}]: {wf_name}")
            print(f"     Error: {result.get('error', '')[:120]}")
            failed += 1

    print(f"\n📊 Results: {imported} imported, {skipped} skipped, {failed} failed")

    if imported > 0:
        print("""
✅ Workflows imported! Next steps:
   1. Open http://localhost:5678
   2. Go to Settings → Credentials
   3. Add a PostgreSQL credential:
        Name: Miastore PostgreSQL
        Host: localhost
        Port: 5432  
        Database: miastore
        User: postgres
        Password: 2003
   4. Add an Email (SMTP) credential for sending emails
   5. Open each workflow and click ACTIVATE (toggle top-right)
        """)

if __name__ == "__main__":
    main()
