"""Send approved WhatsApp template messages from a CSV using the official WhatsApp Cloud API.
Only contacts with opted_in=yes are messaged. Never use this for unsolicited spam."""
import argparse
import csv
import os
import re
import time

import requests

GRAPH = "https://graph.facebook.com/v20.0"


def normalize_phone(raw, default_cc="92"):
    """Return digits-only international number or None if invalid."""
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = default_cc + digits[1:]
    return digits if 8 <= len(digits) <= 15 else None


def build_payload(to, template, lang, name=None):
    tpl = {"name": template, "language": {"code": lang}}
    if name:
        tpl["components"] = [{"type": "body", "parameters": [{"type": "text", "text": name}]}]
    return {"messaging_product": "whatsapp", "to": to, "type": "template", "template": tpl}


def send(phone_id, token, payload):
    r = requests.post(f"{GRAPH}/{phone_id}/messages", json=payload,
                      headers={"Authorization": f"Bearer {token}"}, timeout=20)
    return r.status_code, r.text[:200]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file", help="columns: phone,name,opted_in")
    p.add_argument("--template", required=True, help="approved template name")
    p.add_argument("--lang", default="en")
    p.add_argument("--cc", default="92", help="default country code for numbers starting with 0")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    pid, tok = os.environ.get("WHATSAPP_PHONE_ID"), os.environ.get("WHATSAPP_TOKEN")
    if not a.dry_run and not (pid and tok):
        raise SystemExit("Set WHATSAPP_PHONE_ID and WHATSAPP_TOKEN (or use --dry-run)")
    sent = skipped = 0
    with open(a.csv_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            phone = normalize_phone(row.get("phone"), a.cc)
            if row.get("opted_in", "").strip().lower() != "yes" or not phone:
                skipped += 1
                print("skip:", row.get("phone"))
                continue
            payload = build_payload(phone, a.template, a.lang, row.get("name"))
            if a.dry_run:
                print("DRY:", payload["to"])
            else:
                print(phone, *send(pid, tok, payload))
                time.sleep(a.delay)
            sent += 1
    print(f"processed {sent}, skipped {skipped}")


if __name__ == "__main__":
    main()
