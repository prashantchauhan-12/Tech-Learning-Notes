"""
BigID – Bulk Tag Update Script
================================
Automates adding new tags to 150+ data sources in BigID via REST API.

Features:
  - Reads data-source → tags mapping from a CSV file
  - Authenticates with BigID API (session token)
  - Backs up existing state before any changes
  - Supports dry-run mode (no changes, only logs)
  - Appends tags without overwriting existing ones
  - Supports rollback from backup
  - Supports validation mode (compare expected vs actual)
  - Generates a detailed execution report
  - Handles errors gracefully per data source

Usage:
  # Dry run (safe)
  python bulk_tag_update.py --config config.json --input tags_mapping.csv --dry-run

  # Live run
  python bulk_tag_update.py --config config.json --input tags_mapping.csv

  # Validate after execution
  python bulk_tag_update.py --config config.json --validate tags_mapping.csv

  # Rollback
  python bulk_tag_update.py --config config.json --rollback backup_20261011_180000.json
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library is required. Install it with: pip install requests")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────
#  Logging Setup
# ─────────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("bigid-tagger")


# ─────────────────────────────────────────────────────────────
#  BigID API Client
# ─────────────────────────────────────────────────────────────
class BigIDClient:
    """Thin wrapper around BigID REST API for data-source tag operations."""

    def __init__(self, base_url: str, username: str, password: str,
                 verify_ssl: bool = True, request_delay: float = 0.5):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.request_delay = request_delay  # seconds between API calls (rate-limit safety)
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.session.verify = self.verify_ssl

    # ── Authentication ──────────────────────────────────────
    def authenticate(self) -> None:
        """Obtain a session token from BigID."""
        url = f"{self.base_url}/api/v1/sessions"
        payload = {"username": self.username, "password": self.password}

        logger.info("Authenticating with BigID at %s ...", self.base_url)
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()

        data = resp.json()
        # Token location may vary – check common patterns
        self.token = (
            data.get("auth_token")
            or data.get("systemToken")
            or data.get("token")
        )
        if not self.token:
            raise ValueError(
                f"Could not extract auth token from response. Keys: {list(data.keys())}"
            )

        self.session.headers.update({"Authorization": self.token})
        logger.info("✅ Authentication successful.")

    def _ensure_auth(self) -> None:
        if not self.token:
            self.authenticate()

    # ── Data Source Operations ──────────────────────────────
    def get_all_datasources(self) -> list[dict]:
        """Fetch all data-source connections."""
        self._ensure_auth()
        url = f"{self.base_url}/api/v1/ds-connections"
        logger.info("Fetching all data sources from %s ...", url)

        all_sources = []
        resp = self.session.get(url)

        # Handle 401 with one retry (token may have expired)
        if resp.status_code == 401:
            logger.warning("Token expired. Re-authenticating...")
            self.authenticate()
            resp = self.session.get(url)

        resp.raise_for_status()
        data = resp.json()

        # BigID may return { "ds_connections": [...] } or just [...]
        if isinstance(data, list):
            all_sources = data
        elif isinstance(data, dict):
            all_sources = (
                data.get("ds_connections")
                or data.get("data")
                or data.get("results")
                or []
            )
        
        logger.info("📦 Found %d data sources.", len(all_sources))
        return all_sources

    def get_datasource(self, name: str) -> dict:
        """Fetch a single data-source connection by name."""
        self._ensure_auth()
        url = f"{self.base_url}/api/v1/ds-connections/{name}"
        resp = self.session.get(url)
        if resp.status_code == 401:
            self.authenticate()
            resp = self.session.get(url)
        resp.raise_for_status()

        data = resp.json()
        # May be wrapped: { "ds_connection": {...} }
        if isinstance(data, dict) and "ds_connection" in data:
            return data["ds_connection"]
        return data

    def update_datasource(self, name: str, full_payload: dict) -> dict:
        """Update a data-source connection (full PUT replacement)."""
        self._ensure_auth()
        url = f"{self.base_url}/api/v1/ds-connections/{name}"
        resp = self.session.put(url, json=full_payload)
        if resp.status_code == 401:
            self.authenticate()
            resp = self.session.put(url, json=full_payload)
        resp.raise_for_status()
        return resp.json()


# ─────────────────────────────────────────────────────────────
#  CSV Parsing
# ─────────────────────────────────────────────────────────────
def parse_tags_csv(filepath: str) -> dict[str, list[str]]:
    """
    Parse a CSV file with columns: data_source_name, new_tags
    Returns: { "source-name": ["tag1", "tag2", ...], ... }
    """
    mapping = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ds_name = row.get("data_source_name", "").strip()
            raw_tags = row.get("new_tags", "").strip()
            if ds_name and raw_tags:
                tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
                mapping[ds_name] = tags
    logger.info("📋 Loaded %d data-source tag mappings from %s", len(mapping), filepath)
    return mapping


# ─────────────────────────────────────────────────────────────
#  Backup & Rollback
# ─────────────────────────────────────────────────────────────
def create_backup(datasources: list[dict], output_dir: str) -> str:
    """Save current state of all data sources to a timestamped JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # Extract only name + tags for a lightweight backup
    backup_data = []
    for ds in datasources:
        name = ds.get("name", ds.get("id", "unknown"))
        tags = ds.get("tags", [])
        backup_data.append({"name": name, "tags": tags, "_full": ds})

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2, default=str)

    logger.info("💾 Backup saved to %s (%d sources)", filepath, len(backup_data))
    return filepath


def rollback_from_backup(client: BigIDClient, backup_path: str) -> None:
    """Restore tags from a backup file."""
    with open(backup_path, encoding="utf-8") as f:
        backup_data = json.load(f)

    logger.info("🔄 Rolling back from %s (%d entries)...", backup_path, len(backup_data))

    for entry in backup_data:
        name = entry["name"]
        original_tags = entry["tags"]
        try:
            current = client.get_datasource(name)
            current["tags"] = original_tags
            client.update_datasource(name, current)
            logger.info("  ✅ Rolled back: %s → tags=%s", name, original_tags)
        except Exception as e:
            logger.error("  ❌ Rollback failed for %s: %s", name, e)

        time.sleep(client.request_delay)

    logger.info("🔄 Rollback complete.")


# ─────────────────────────────────────────────────────────────
#  Core: Tag Update Logic
# ─────────────────────────────────────────────────────────────
def merge_tags(existing: list[str], new: list[str]) -> list[str]:
    """Merge new tags into existing list, avoiding duplicates. Preserves order."""
    existing_set = set(existing or [])
    merged = list(existing or [])
    for tag in new:
        if tag not in existing_set:
            merged.append(tag)
            existing_set.add(tag)
    return merged


def run_tag_update(client: BigIDClient, tag_mapping: dict[str, list[str]],
                   dry_run: bool = False, output_dir: str = ".") -> dict:
    """
    Main execution function.
    
    Returns a report dict:
    {
        "total": int,
        "success": [...],
        "skipped": [...],
        "failed": [...],
        "not_found": [...]
    }
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "mode": "DRY-RUN" if dry_run else "LIVE",
        "total": len(tag_mapping),
        "success": [],
        "skipped": [],
        "failed": [],
        "not_found": [],
    }

    # Step 1: Fetch all data sources
    all_sources = client.get_all_datasources()
    source_lookup = {}
    for ds in all_sources:
        name = ds.get("name", ds.get("id"))
        if name:
            source_lookup[name] = ds

    # Step 2: Backup
    if not dry_run:
        backup_path = create_backup(all_sources, output_dir)
        report["backup_file"] = backup_path
    else:
        logger.info("🔍 DRY-RUN mode — no changes will be made.")

    # Step 3: Process each mapping
    for ds_name, new_tags in tag_mapping.items():
        logger.info("─" * 60)
        logger.info("Processing: %s → add tags: %s", ds_name, new_tags)

        # Check if data source exists
        if ds_name not in source_lookup:
            logger.warning("  ⚠️  Data source '%s' NOT FOUND in BigID. Skipping.", ds_name)
            report["not_found"].append({"name": ds_name, "requested_tags": new_tags})
            continue

        ds_obj = source_lookup[ds_name]
        existing_tags = ds_obj.get("tags", []) or []
        merged_tags = merge_tags(existing_tags, new_tags)

        # Check if any new tags are actually being added
        actually_new = [t for t in new_tags if t not in set(existing_tags or [])]
        if not actually_new:
            logger.info("  ⏭️  All tags already exist. Skipping.")
            report["skipped"].append({
                "name": ds_name,
                "existing_tags": existing_tags,
                "requested_tags": new_tags,
            })
            continue

        logger.info("  Current tags : %s", existing_tags)
        logger.info("  Tags to add  : %s", actually_new)
        logger.info("  Merged tags  : %s", merged_tags)

        if dry_run:
            report["success"].append({
                "name": ds_name,
                "existing_tags": existing_tags,
                "added_tags": actually_new,
                "final_tags": merged_tags,
                "status": "DRY-RUN (would update)",
            })
            continue

        # Live update
        try:
            # Re-fetch to get the freshest copy (avoid stale data)
            fresh_ds = client.get_datasource(ds_name)
            fresh_ds["tags"] = merged_tags
            client.update_datasource(ds_name, fresh_ds)

            logger.info("  ✅ Updated successfully.")
            report["success"].append({
                "name": ds_name,
                "existing_tags": existing_tags,
                "added_tags": actually_new,
                "final_tags": merged_tags,
                "status": "SUCCESS",
            })
        except requests.exceptions.HTTPError as e:
            logger.error("  ❌ API error: %s", e)
            report["failed"].append({
                "name": ds_name,
                "error": str(e),
                "status_code": e.response.status_code if e.response else None,
            })
        except Exception as e:
            logger.error("  ❌ Unexpected error: %s", e)
            report["failed"].append({
                "name": ds_name,
                "error": str(e),
            })

        # Rate-limit safety
        time.sleep(client.request_delay)

    # Step 4: Save report
    report_path = os.path.join(
        output_dir,
        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    logger.info("─" * 60)
    logger.info("📊 Report saved to %s", report_path)

    # Summary
    logger.info("")
    logger.info("═" * 60)
    logger.info("  SUMMARY (%s)", report["mode"])
    logger.info("═" * 60)
    logger.info("  Total mappings : %d", report["total"])
    logger.info("  Successful     : %d", len(report["success"]))
    logger.info("  Skipped (dup)  : %d", len(report["skipped"]))
    logger.info("  Not found      : %d", len(report["not_found"]))
    logger.info("  Failed         : %d", len(report["failed"]))
    logger.info("═" * 60)

    return report


# ─────────────────────────────────────────────────────────────
#  Validation Mode
# ─────────────────────────────────────────────────────────────
def validate_tags(client: BigIDClient, tag_mapping: dict[str, list[str]]) -> None:
    """After execution, verify that all expected tags are present on each data source."""
    logger.info("🔎 Running validation...")
    all_sources = client.get_all_datasources()
    source_lookup = {ds.get("name", ds.get("id")): ds for ds in all_sources}

    passed = 0
    failed = 0

    for ds_name, expected_new_tags in tag_mapping.items():
        if ds_name not in source_lookup:
            logger.error("  ❌ FAIL: %s — not found in BigID", ds_name)
            failed += 1
            continue

        actual_tags = set(source_lookup[ds_name].get("tags", []) or [])
        missing = [t for t in expected_new_tags if t not in actual_tags]

        if missing:
            logger.error("  ❌ FAIL: %s — missing tags: %s", ds_name, missing)
            failed += 1
        else:
            logger.info("  ✅ PASS: %s — all expected tags present", ds_name)
            passed += 1

    logger.info("")
    logger.info("Validation: %d passed, %d failed out of %d", passed, failed, len(tag_mapping))


# ─────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────
def load_config(config_path: str) -> dict:
    """Load BigID connection config from JSON file."""
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="BigID – Bulk Tag Update for Data Sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run
  python bulk_tag_update.py --config config.json --input tags_mapping.csv --dry-run

  # Live run
  python bulk_tag_update.py --config config.json --input tags_mapping.csv

  # Validate
  python bulk_tag_update.py --config config.json --validate tags_mapping.csv

  # Rollback
  python bulk_tag_update.py --config config.json --rollback backup_20261011_180000.json
        """
    )

    parser.add_argument("--config", required=True,
                        help="Path to BigID config JSON (base_url, username, password)")
    parser.add_argument("--input", dest="input_csv",
                        help="Path to CSV file with data_source_name,new_tags mapping")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without actually updating BigID")
    parser.add_argument("--validate",
                        help="Validate tags on data sources against a CSV mapping")
    parser.add_argument("--rollback",
                        help="Path to a backup JSON file to restore from")
    parser.add_argument("--output-dir", default=".",
                        help="Directory for backup and report files (default: current dir)")

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    client = BigIDClient(
        base_url=config["base_url"],
        username=config["username"],
        password=config["password"],
        verify_ssl=config.get("verify_ssl", True),
        request_delay=config.get("request_delay", 0.5),
    )

    # Route to the correct mode
    if args.rollback:
        client.authenticate()
        rollback_from_backup(client, args.rollback)

    elif args.validate:
        client.authenticate()
        tag_mapping = parse_tags_csv(args.validate)
        validate_tags(client, tag_mapping)

    elif args.input_csv:
        client.authenticate()
        tag_mapping = parse_tags_csv(args.input_csv)
        if not tag_mapping:
            logger.error("No valid mappings found in %s. Exiting.", args.input_csv)
            sys.exit(1)
        run_tag_update(client, tag_mapping, dry_run=args.dry_run, output_dir=args.output_dir)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
