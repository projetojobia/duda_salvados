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
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = [sheet["properties"]["title"] for sheet in spreadsheet.get("sheets", [])]
    print("SHEETS:", sheets)

    for sheet_name in ["Painel", "Dashboard", "Resumo"]:
        if sheet_name not in sheets:
            continue
        values = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_name}!A1:Z80",
            valueRenderOption="FORMULA",
        ).execute().get("values", [])
        print(f"\nSHEET {sheet_name}")
        for r, row in enumerate(values, start=1):
            for c, cell in enumerate(row, start=1):
                text = str(cell)
                if "lucro" in text.lower() or "estimado" in text.lower() or "U" in text or "89" in text:
                    print(r, c, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
