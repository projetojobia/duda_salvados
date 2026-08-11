from __future__ import annotations

import sys
from pathlib import Path


SPREADSHEET_ID = "12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4"
GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)

sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


def main() -> int:
    service = build_service("sheets", "v4")
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A2:U301",
    ).execute().get("values", [])
    for row in values:
        row = row + [""] * (21 - len(row))
        code, product, final_price, lucro = row[0], row[3], row[19], row[20]
        if str(code).startswith("DS") and str(lucro).strip():
            print(f"{code} | T={final_price} | U={lucro} | {product[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
