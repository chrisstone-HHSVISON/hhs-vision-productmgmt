#!/usr/bin/env python3
import csv
import io
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
ROADMAP_HTML = REPO_ROOT / "roadmap.html"
ROADMAP_CSV = REPO_ROOT / "Source" / "roadmap-data.csv"

DEFAULT_SHEET_ID = "1s4S1TS3Vkl_Xh9uZ9CSZt9VTWVhDzU5-wNpCu7q5w4g"
DEFAULT_GID = "0"
DEFAULT_CSV_URL = ""

RELEASE_ONE = "1. Dec 14 Happy Path"
RELEASE_TWO = "2. 2027 Go-Live MVP"
VALID_MILESTONES = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "TBD"}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def fetch_csv_via_url(url: str) -> str:
    req = Request(url, headers={"User-Agent": "roadmap-sync-bot/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8-sig")


def fetch_csv_via_service_account(sheet_id: str, worksheet_gid: str, svc_json: str) -> str:
    try:
        import gspread  # type: ignore
    except Exception as exc:  # pragma: no cover
        fail(f"gspread not available: {exc}")

    try:
        creds = json.loads(svc_json)
        gc = gspread.service_account_from_dict(creds)
        sh = gc.open_by_key(sheet_id)
        ws = sh.get_worksheet_by_id(int(worksheet_gid))
    except Exception as exc:
        fail(
            "Google service account fetch failed. "
            "Ensure GOOGLE_SERVICE_ACCOUNT_JSON is valid and the sheet is shared with that service account. "
            f"Details: {exc}"
        )

    values = ws.get_all_values()
    if not values:
        fail("Worksheet returned no values.")

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    for row in values:
        writer.writerow(row)
    return buf.getvalue()


def parse_rows(csv_text: str):
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    filtered = []
    for row in rows:
        release = (row.get("Release") or "").strip()
        milestone = (row.get("Milestone") or "").strip()
        feature = (row.get("Design Feature") or "").strip()
        sub_feature = (row.get("Sub Feature") or "").strip()
        if not (release and milestone and feature and sub_feature):
            continue
        if milestone not in VALID_MILESTONES:
            continue
        filtered.append((release, milestone, feature, sub_feature))
    return filtered


def build_release_data(filtered_rows):
    grouped = OrderedDict({RELEASE_ONE: OrderedDict(), RELEASE_TWO: OrderedDict()})

    for release, milestone, feature, sub_feature in filtered_rows:
        if release not in grouped:
            continue
        release_map = grouped[release]
        release_map.setdefault(feature, [])
        exists = any(item["name"] == sub_feature and item["ms"] == milestone for item in release_map[feature])
        if not exists:
            release_map[feature].append({"name": sub_feature, "ms": milestone})

    r1 = [{"name": name, "subs": subs} for name, subs in grouped[RELEASE_ONE].items()]
    r2 = [{"name": name, "subs": subs} for name, subs in grouped[RELEASE_TWO].items()]
    return r1, r2


def update_roadmap_html(r1, r2, snapshot_iso: str):
    content = ROADMAP_HTML.read_text(encoding="utf-8")

    block = (
        "const STATIC_R1 = " + json.dumps(r1, ensure_ascii=True) + ";\n"
        "const STATIC_R2 = " + json.dumps(r2, ensure_ascii=True) + ";\n\n"
    )

    content, replaced = re.subn(
        r"const STATIC_R1 = \[.*?\];\nconst STATIC_R2 = \[.*?\];\n\n",
        lambda _: block,
        content,
        count=1,
        flags=re.S,
    )
    if replaced != 1:
        fail("Could not replace STATIC_R1/STATIC_R2 block in roadmap.html")

    snapshot_line = f"const SNAPSHOT_UPDATED_AT = '{snapshot_iso}';"
    if "const SNAPSHOT_UPDATED_AT =" in content:
        content = re.sub(r"const SNAPSHOT_UPDATED_AT = '.*?';", snapshot_line, content, count=1)
    else:
        anchor = "const AUTO_REFRESH_MS = 120000;"
        if anchor not in content:
            fail("Could not find AUTO_REFRESH_MS anchor in roadmap.html")
        content = content.replace(anchor, anchor + "\n" + snapshot_line, 1)

    ROADMAP_HTML.write_text(content, encoding="utf-8")


def main():
    sheet_id = os.getenv("GOOGLE_SHEET_ID", DEFAULT_SHEET_ID)
    worksheet_gid = os.getenv("GOOGLE_WORKSHEET_GID", DEFAULT_GID)
    csv_url = os.getenv("ROADMAP_CSV_URL", DEFAULT_CSV_URL).strip()
    svc_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()

    if svc_json:
        csv_text = fetch_csv_via_service_account(sheet_id, worksheet_gid, svc_json)
        print("Fetched roadmap data using Google service account")
    elif csv_url:
        csv_text = fetch_csv_via_url(csv_url)
        print(f"Fetched roadmap data from URL: {csv_url}")
    else:
        print(
            "No sync source configured. Set GOOGLE_SERVICE_ACCOUNT_JSON (preferred) "
            "or ROADMAP_CSV_URL. Skipping sync."
        )
        return

    ROADMAP_CSV.write_text(csv_text, encoding="utf-8")

    filtered_rows = parse_rows(csv_text)
    if not filtered_rows:
        fail("No usable roadmap rows found in source data")

    r1, r2 = build_release_data(filtered_rows)
    snapshot_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    update_roadmap_html(r1, r2, snapshot_iso)

    print(f"R1 features: {len(r1)} | R2 features: {len(r2)}")
    print(f"Snapshot updated at: {snapshot_iso}")


if __name__ == "__main__":
    main()
