from __future__ import annotations

import re
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
    data = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A2:T301",
    ).execute()
    rows = data.get("values", [])
    missing = []
    filled = []
    for row in rows:
        row = row + [""] * (20 - len(row))
        code = str(row[0]).strip()
        if not re.fullmatch(r"DS\d{3}", code):
            continue
        if not any(str(cell).strip() for cell in row[1:]):
            continue
        product = str(row[3]).strip()
        suggested = str(row[18]).strip()
        final_price = str(row[19]).strip()
        if final_price:
            filled.append((code, suggested, final_price, product[:55]))
        else:
            missing.append((code, product[:55]))

    print("COM PRECO FINAL")
    for code, suggested, final_price, product in filled:
        print(f"{code} | sugerido={suggested or '-'} | final={final_price} | {product}")
    print("\nSEM PRECO FINAL")
    if missing:
        for code, product in missing:
            print(f"{code} | {product}")
    else:
        print("Nenhum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
