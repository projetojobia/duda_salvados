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


def has_price(value: str) -> bool:
    return bool(str(value or "").strip())


def main() -> int:
    service = build_service("sheets", "v4")
    data = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A2:AE301",
    ).execute()
    rows = data.get("values", [])
    updates: list[dict[str, object]] = []
    summary: list[str] = []

    for offset, row in enumerate(rows, start=2):
        row = row + [""] * (31 - len(row))
        code = str(row[0]).strip()
        if not re.fullmatch(r"DS\d{3}", code):
            continue
        if not any(str(cell).strip() for cell in row[1:]):
            continue
        status = str(row[9]).strip()
        final_price = row[19]
        obs = str(row[29] or "")
        changed = False

        if has_price(final_price) and re.search(r"pre[cç]o final pendente", obs, re.I):
            obs = re.sub(r"\s*Pre[cç]o final pendente\.?", "", obs, flags=re.I).strip()
            if obs:
                obs += " "
            obs += "Preco final ja definido e revisado no padrao de arredondamento."
            updates.append({"range": f"Produtos!AD{offset}:AE{offset}", "values": [[obs, "10/08/2026 13:35"]]})
            changed = True

        if has_price(final_price) and status == "Aguardando preco":
            updates.append({"range": f"Produtos!J{offset}", "values": [["Pronto para publicar"]]})
            changed = True

        if changed:
            summary.append(code)

    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"valueInputOption": "USER_ENTERED", "data": updates},
        ).execute()

    print("Atualizados: " + ", ".join(summary) if summary else "Nenhuma observacao pendente encontrada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
