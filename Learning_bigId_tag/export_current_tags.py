# BigID – Quick Export Script
# Run this FIRST to understand your current data sources and tags
# before doing any bulk updates.
#
# Usage:
#   python export_current_tags.py --config config.json

"""
Export all data sources and their current tags from BigID.
Produces two output files:
  1. all_datasources_full.json  – complete API response (for backup)
  2. current_tags_summary.csv   – lightweight CSV with name, type, tags
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library is required. Install it with: pip install requests")
    sys.exit(1)


def authenticate(base_url: str, username: str, password: str, verify_ssl: bool = True) -> str:
    """Get session token from BigID."""
    url = f"{base_url.rstrip('/')}/api/v1/sessions"
    resp = requests.post(url, json={"username": username, "password": password}, verify=verify_ssl)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("auth_token") or data.get("systemToken") or data.get("token")
    if not token:
        raise ValueError(f"Could not extract token. Response keys: {list(data.keys())}")
    return token


def fetch_datasources(base_url: str, token: str, verify_ssl: bool = True) -> list:
    """Fetch all data source connections."""
    url = f"{base_url.rstrip('/')}/api/v1/ds-connections"
    headers = {"Authorization": token}
    resp = requests.get(url, headers=headers, verify=verify_ssl)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        return data
    return data.get("ds_connections") or data.get("data") or data.get("results") or []


def main():
    parser = argparse.ArgumentParser(description="Export BigID data sources & tags")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    base_url = config["base_url"]
    username = config["username"]
    password = config["password"]
    verify_ssl = config.get("verify_ssl", True)

    print(f"🔐 Authenticating with {base_url} ...")
    token = authenticate(base_url, username, password, verify_ssl)
    print("✅ Authenticated.")

    print("📦 Fetching all data sources ...")
    datasources = fetch_datasources(base_url, token, verify_ssl)
    print(f"   Found {len(datasources)} data sources.")

    # Save full JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = os.path.join(args.output_dir, f"all_datasources_full_{timestamp}.json")
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(datasources, f, indent=2, default=str)
    print(f"💾 Full export: {full_path}")

    # Save CSV summary
    csv_path = os.path.join(args.output_dir, f"current_tags_summary_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["data_source_name", "type", "current_tags", "tag_count"])
        for ds in datasources:
            name = ds.get("name", ds.get("id", "unknown"))
            ds_type = ds.get("type", ds.get("ds_connection_type", "unknown"))
            tags = ds.get("tags", []) or []
            writer.writerow([name, ds_type, "|".join(tags), len(tags)])
    print(f"📋 CSV summary: {csv_path}")

    # Quick stats
    total = len(datasources)
    with_tags = sum(1 for ds in datasources if ds.get("tags"))
    without_tags = total - with_tags
    all_tags = set()
    for ds in datasources:
        for t in (ds.get("tags") or []):
            all_tags.add(t)

    print()
    print("═" * 50)
    print("  SUMMARY")
    print("═" * 50)
    print(f"  Total data sources   : {total}")
    print(f"  With tags            : {with_tags}")
    print(f"  Without tags         : {without_tags}")
    print(f"  Unique tags in use   : {len(all_tags)}")
    if all_tags:
        print(f"  Tags found           : {sorted(all_tags)}")
    print("═" * 50)


if __name__ == "__main__":
    main()
