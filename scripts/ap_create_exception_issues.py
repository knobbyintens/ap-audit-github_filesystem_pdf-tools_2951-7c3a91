#!/usr/bin/env python3
"""Create AP exception issues for the FY2026 Q4 invoice review."""
import json
import os
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
API = "https://api.github.com"


def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        API + path,
        method=method,
        data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "ap-exception-workflow",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.status, json.loads(response.read().decode() or "{}")


def build_body(item):
    return (
        f"Invoice: {item['invoice']}\n"
        f"Vendor: {item['vendor']}\n"
        f"Vendor ID: {item['vendor_id']}\n"
        f"Amount: USD {item['amount']}\n"
        f"Rule: {item['rule']}\n"
        f"Severity: {item['severity']}\n"
        f"Action: HOLD payment pending accounts payable manager review"
    )


ISSUES = [
    dict(invoice="INV-2026-0452", vendor="Northgate Cloud Services", vendor_id="V-1003", amount="3456.00", rule="probation_limit_exceeded", severity="medium"),
    dict(invoice="INV-2026-0453", vendor="Pioneer Print & Mail", vendor_id="V-1005", amount="1058.40", rule="vendor_blocked", severity="high"),
    dict(invoice="INV-2026-0454", vendor="Halcyon Freight Systems", vendor_id="UNKNOWN", amount="2970.00", rule="unregistered_vendor", severity="high"),
    dict(invoice="INV-2026-0455", vendor="BlueHarbor Logistics Ltd.", vendor_id="V-1002", amount="961.20", rule="duplicate_invoice", severity="high"),
    dict(invoice="INV-2026-0456", vendor="Vertex Data Analytics", vendor_id="V-1007", amount="1635.00", rule="amount_mismatch", severity="medium"),
    dict(invoice="INV-2026-0457", vendor="Meridian Office Supply Co.", vendor_id="V-1001", amount="12400.00", rule="manager_approval_required", severity="medium"),
]


def main():
    status, open_issues = api("GET", f"/repos/{REPO}/issues?state=open&per_page=100")
    existing = {i["title"] for i in open_issues} if isinstance(open_issues, list) else set()
    failures = []
    for item in ISSUES:
        title = f"[AP EXCEPTION] {item['invoice']} - {item['rule']}"
        if title in existing:
            print(f"SKIP existing: {title}")
            continue
        payload = {"title": title, "body": build_body(item)}
        try:
            status, response = api("POST", f"/repos/{REPO}/issues", payload)
            print(f"CREATED #{response.get('number')}: {title}")
        except urllib.error.HTTPError as exc:
            print(f"FAILED {title}: HTTP {exc.code}: {exc.read().decode()[:300]}")
            failures.append(title)
        time.sleep(1)
    if failures:
        print(f"{len(failures)} issue(s) failed", file=sys.stderr)
        sys.exit(1)
    print("All exception issues created successfully")


if __name__ == "__main__":
    main()
