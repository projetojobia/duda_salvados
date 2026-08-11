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
            "range": "Produtos!N3:Q3",
            "values": [[
                136,
                266.99,
                458.25,
                "Shopee prioridade: Torneira Cozinha Gourmet de Bancada Monocomando Preta com Spray Flexivel R$136,00 no Pix / R$159,99 sem cupom | Torneira Cozinha Gourmet Preta Monocomando Misturador Mola R$266,99 no Pix / R$314,10 sem cupom | Torneira Monocomando Mola Gourmet Flexivel Cozinha Mesa Preto Fosco 50 cm R$458,25 no Pix / R$552,44 sem cupom. ML/Amazon somente comparativo.",
            ]],
        },
        {"range": "Produtos!S3:S3", "values": [[230]]},
        {
            "range": "Produtos!AD3:AE3",
            "values": [[
                "Revisado pelo Codex em 10/08/2026: regra nova aplicada, Shopee como base principal. Produto novo nao testado; preco definido T preservado.",
                "10/08/2026 10:03",
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
