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
    updates = [
        {
            "range": "Produtos!Q2:Q2",
            "values": [[
                "Referência visual enviada pelo usuário via busca por imagem: Shopee SANDA 3363, vendedor internacional. Usar apenas para identificação visual/modelo; não usar como base final N/O/P por envolver importação/impostos."
            ]],
        },
        {
            "range": "Produtos!AD2:AE2",
            "values": [[
                "Regra ajustada em 10/08/2026: referência SANDA 3363 do print é vendedor internacional; não deve ser base de preço. Usuário definiu manualmente T=R$120,00, preservado. Necessário buscar anúncio nacional correspondente para revisar N/O/P/S.",
                "10/08/2026 10:50",
            ]],
        },
    ]
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": updates},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
