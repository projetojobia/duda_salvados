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
        {"range": "Produtos!E2:F2", "values": [["SANDA", "SANDA 3363 Sport Watch analógico/digital pulseira metálica prata"]]},
        {"range": "Produtos!N2:P2", "values": [[76.00, 83.94, 299.78]]},
        {
            "range": "Produtos!Q2:T2",
            "values": [[
                "Referência visual enviada pelo usuário via busca por imagem: Shopee SANDA 3363 Top Fashion Relógio Eletrônico Masculino, variação prateada correspondente à foto, R$76,00-R$83,94; preço original exibido R$299,78.",
                "=(O2+P2)/2",
                57.00,
                120.00,
            ]],
        },
        {
            "range": "Produtos!AD2:AE2",
            "values": [[
                "Ajustado em 10/08/2026: usuário validou referência por imagem e pediu marca SANDA com preço final R$120,00. Observação: T definido manualmente prevalece sobre sugestão automática.",
                "10/08/2026 10:45",
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
