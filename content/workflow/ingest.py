#!/usr/bin/env python3
"""
AffindaBrain — Ingestion Script
Uploads a document to the Affinda API, polls until ready, and saves the JSON response to raw/.

Usage:
    python ingest.py path/to/CV.pdf
    python ingest.py path/to/CV.docx

Output:
    raw/<filename>.json

Requirements:
    pip install requests
"""

import sys
import os
import json
import time
import requests
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("AFFINDA_API_KEY", "")  # set via environment variable
WORKSPACE_ID = "avTnlGrd"
BASE_URL = "https://api.affinda.com/v3"
RAW_DIR = Path(__file__).parent.parent / "raw"
POLL_INTERVAL = 3   # seconds between status checks
MAX_WAIT = 120       # seconds before timeout

# ── Helpers ──────────────────────────────────────────────────────────────────

def headers():
    if not API_KEY:
        raise ValueError(
            "AFFINDA_API_KEY not set. Export it before running:\n"
            "  export AFFINDA_API_KEY=your_key_here"
        )
    return {"Authorization": f"Bearer {API_KEY}"}


def upload_document(file_path: Path) -> str:
    """Upload document to Affinda. Returns document identifier."""
    print(f"Uploading {file_path.name} to Affinda...")
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/documents",
            headers=headers(),
            data={"workspace": WORKSPACE_ID},
            files={"file": (file_path.name, f)},
        )
    response.raise_for_status()
    doc = response.json()
    identifier = doc["meta"]["identifier"]
    print(f"  Uploaded. Document ID: {identifier}")
    return identifier


def poll_until_ready(identifier: str) -> dict:
    """Poll document status until ready or timeout."""
    print(f"Waiting for extraction to complete...")
    elapsed = 0
    while elapsed < MAX_WAIT:
        response = requests.get(
            f"{BASE_URL}/documents/{identifier}",
            headers=headers(),
        )
        response.raise_for_status()
        doc = response.json()
        meta = doc["meta"]

        if meta.get("failed"):
            raise RuntimeError(f"Affinda extraction failed: {meta.get('errorDetail')}")

        if meta.get("ready"):
            print(f"  Ready after {elapsed}s.")
            return doc

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        print(f"  Still processing... ({elapsed}s)")

    raise TimeoutError(f"Document not ready after {MAX_WAIT}s.")


def save_to_raw(doc: dict, original_filename: str) -> Path:
    """Save parsed JSON to raw/ directory."""
    RAW_DIR.mkdir(exist_ok=True)
    stem = Path(original_filename).stem
    output_path = RAW_DIR / f"{stem}.json"

    # Strip signed AWS URLs (they expire in 1 hour and bloat the file)
    clean_doc = strip_signed_urls(doc)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clean_doc, f, indent=2, ensure_ascii=False)

    print(f"  Saved to {output_path}")
    return output_path


def strip_signed_urls(obj):
    """Recursively remove signed AWS S3 URLs from the response."""
    if isinstance(obj, dict):
        return {
            k: strip_signed_urls(v)
            for k, v in obj.items()
            if not (isinstance(v, str) and "X-Amz-Signature" in v)
        }
    if isinstance(obj, list):
        return [strip_signed_urls(item) for item in obj]
    return obj


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest.py path/to/document.pdf")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    identifier = upload_document(file_path)
    doc = poll_until_ready(identifier)
    output_path = save_to_raw(doc, file_path.name)

    print(f"\nDone. JSON saved to: {output_path}")
    print(f"Next step: compile a candidate or job page from this JSON.")


if __name__ == "__main__":
    main()
