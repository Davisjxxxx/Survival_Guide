#!/usr/bin/env python3
"""Check B012's claim-triage spreadsheet for completeness and fail-closed status.

This checks metadata, not factual correctness, source freshness, image rights,
medical accuracy, field performance, or expert approval.
"""
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECON = ROOT / "modules/B012/reconciliation"
SRC = ROOT / "modules/B012/recovered_source/production_package"
QUEUE = RECON / "B012_CLAIM_EVIDENCE_TRIAGE_20261124.csv"
REGISTER = RECON / "B012_RECOVERED_PAGE_REGISTER_20261123.csv"
PAGE_MAP = SRC / "B012_PAGE_MAP.csv"
SOURCE_REGISTER = SRC / "B012_SOURCE_REGISTER.csv"

def read(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    queue = read(QUEUE)
    pages = read(PAGE_MAP)
    register = read(REGISTER)
    sources = read(SOURCE_REGISTER)
    expected = {f"P{i:02d}" for i in range(1, 29)}
    known_sources = {s["source_id"] for s in sources}
    require(len(queue) == 28, "Exactly 28 queue entries required")
    require(len(known_sources) == len(sources) == 17, "Source register changed: inspect first")
    require({f"P{int(x['page']):02d}" for x in pages} == expected, "Source page-map coverage changed")
    require({x["page_id"] for x in register} == expected, "Original recovered page register coverage changed")
    require({x["page_id"] for x in queue} == expected, "Queue page IDs missing, repeated, or unexpected")
    by_original = {f"P{int(x['page']):02d}": x for x in pages}
    for row in queue:
        pid = row["page_id"]
        original = by_original[pid]
        expected_ids = {v.strip() for v in original["source_ids"].split(";") if v.strip()}
        recorded_ids = {v.strip() for v in row["original_source_leads"].split(";") if v.strip()}
        require(recorded_ids == expected_ids, f"{pid}: source leads changed without source-map reconciliation")
        require(recorded_ids <= known_sources, f"{pid}: unknown planning source IDs")
        require(row["page_title_in_original_map"] == original["section_title"], f"{pid}: source title changed")
        require(row["original_reader_job_not_verified_claim"] == original["reader_job"], f"{pid}: source reader job changed")
        for field in ("source_links_validated", "claim_text_validated", "human_expert_approved", "visual_rights_verified"):
            require(row[field].startswith("NO"), f"{pid}: {field} must not be promoted without documented evidence")
        require(row["release_status"] == "BLOCKED", f"{pid}: release gate was incorrectly lifted")
        require(row["assigned_review_role"].strip(), f"{pid}: no proposed review role")
        require(row["documented_issue_or_scope"].strip(), f"{pid}: no scope description")
    for pid in [f"P{i:02d}" for i in range(13,19)] + ["P25"]:
        row = next(x for x in queue if x["page_id"] == pid)
        require("template" in row["documented_issue_or_scope"].lower() or
                "frostbite" in row["documented_issue_or_scope"].lower(),
                f"{pid}: inherited defect not flagged")
    print("PASS: 28/28 B012 triage rows map to original pages and source leads.")
    print("PASS: all rows retain unverified evidence, human, rights, and release gates.")
    print("NOTE: this is metadata validation only, NOT safety or publication clearance.")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
