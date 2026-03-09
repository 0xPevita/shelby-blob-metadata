#!/usr/bin/env python3
import argparse
import requests
from datetime import datetime

SHELBY_API = "https://api.shelbynet.shelby.xyz/shelby/v1"
APTOS_API  = "https://api.testnet.aptoslabs.com/v1"


def format_bytes(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024
    return f"{b:.2f} TB"


def get_blobs(address):
    try:
        r = requests.get(f"{SHELBY_API}/blobs/{address}", timeout=10)
        return r.json().get("blobs", []) if r.status_code == 200 else []
    except Exception:
        return []


def print_blob(blob):
    name = blob.get("blob_name", "unknown")
    size = blob.get("size", 0)
    expiry = blob.get("expiration_micros", 0)
    status = blob.get("status", "unknown")
    pg = blob.get("placement_group", "?")
    exp_str = datetime.fromtimestamp(expiry / 1e6).strftime("%Y-%m-%d") if expiry else "N/A"
    print(f"\n📦 Blob: {name}")
    print(f"   Size:            {format_bytes(size)}")
    print(f"   Expires:         {exp_str}")
    print(f"   Status:          {status}")
    print(f"   Placement Group: {pg}")


def main():
    p = argparse.ArgumentParser(description="Fetch Shelby blob metadata")
    p.add_argument("address", help="Aptos account address")
    p.add_argument("--blob", help="Specific blob name to look up")
    args = p.parse_args()

    print(f"🔍 Fetching blobs for {args.address[:20]}...")
    blobs = get_blobs(args.address)

    if not blobs:
        print("  No blobs found.")
        return

    if args.blob:
        blobs = [b for b in blobs if b.get("blob_name", "").endswith(args.blob)]

    print(f"  Found {len(blobs)} blob(s)\n")
    for blob in blobs:
        print_blob(blob)


if __name__ == "__main__":
    main()
