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

    painel = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Painel!A8:B9",
        valueRenderOption="FORMULA",
    ).execute().get("values", [])
    print("FORMULAS PAINEL A8:B9")
    for row in painel:
        print(row)

    data = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A2:J301",
    ).execute().get("values", [])

    updates: list[dict[str, object]] = []
    changed: list[str] = []
    for row_number, row in enumerate(data, start=2):
        row = row + [""] * (10 - len(row))
        code = str(row[0]).strip()
        status = str(row[9]).strip()
        if not re.fullmatch(r"DS\d{3}", code):
            continue
        if not any(str(cell).strip() for cell in row[1:]):
            continue
        if status == "Pronto para publicar":
            updates.append({
                "range": f"Produtos!J{row_number}",
                "values": [["Disponível"]],
            })
            updates.append({
                "range": f"Produtos!AE{row_number}",
                "values": [["10/08/2026 13:45"]],
            })
            changed.append(code)

    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"valueInputOption": "USER_ENTERED", "data": updates},
        ).execute()

    print("ALTERADOS PARA DISPONIVEL:", ", ".join(changed) if changed else "Nenhum")

    painel_after = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Painel!A7:B10",
    ).execute().get("values", [])
    print("PAINEL APOS")
    for row in painel_after:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
