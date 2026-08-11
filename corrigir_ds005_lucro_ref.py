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
            "range": "Produtos!U6:V6",
            "values": [["=IF(OR(R6=\"\";T6=\"\");\"\";R6-T6)", "=IF(OR(R6=\"\";R6=0;T6=\"\");\"\";(R6-T6)/R6)"]],
        },
        {
            "range": "Produtos!AD6:AE6",
            "values": [[
                "Revisao de correspondencia em 10/08/2026: foto recebida neste chat; usuario informou referencia manual Shopee correspondente ao produto. Fotos ainda nao enviadas ao Drive. Classe media saida; preco final definido automaticamente na revisao de arredondamento: R$85,00. Formula de referencia corrigida em U/V para mostrar vantagem sobre referencia media/alta: R-T e (R-T)/R.",
                "10/08/2026 13:40",
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
