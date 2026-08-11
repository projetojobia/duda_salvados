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
    for sheet_range in [
        "Painel!A15:B17",
        "'Custos Operacionais'!A1:D20",
        "Lote!A1:B12",
    ]:
        values = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_range,
            valueRenderOption="FORMULA",
        ).execute().get("values", [])
        print(f"\n{sheet_range}")
        for row in values:
            print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
