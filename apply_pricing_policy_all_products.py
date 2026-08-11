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
            "range": "Produtos!R1",
            "values": [["Referencia anuncio (R$)"]],
        },
        {
            "range": "Produtos!R2:T2",
            "values": [["=(O2+P2)/2", 36.30, 36.30]],
        },
        {
            "range": "Produtos!AD2:AE2",
            "values": [[
                "Precificacao padronizada em 10/08/2026: classe media saida, S=N*0,75. Preco definido corrigido para ficar abaixo do menor preco Shopee.",
                "10/08/2026 10:15",
            ]],
        },
        {
            "range": "Produtos!R3:T3",
            "values": [["=(O3+P3)/2", 102.00, 102.00]],
        },
        {
            "range": "Produtos!AD3:AE3",
            "values": [[
                "Precificacao padronizada em 10/08/2026: classe media saida, S=N*0,75. Preco definido corrigido para ficar abaixo do menor preco Shopee.",
                "10/08/2026 10:15",
            ]],
        },
        {
            "range": "Produtos!R4:T4",
            "values": [["=(O4+P4)/2", 71.91, 50.00]],
        },
        {
            "range": "Produtos!AD4:AE4",
            "values": [[
                "Precificacao padronizada em 10/08/2026: classe alta saida, S=N*0,90. Preco definido/reserva preservado em R$50,00.",
                "10/08/2026 10:15",
            ]],
        },
        {
            "range": "Produtos!R5:S5",
            "values": [["=(O5+P5)/2", 36.51]],
        },
        {
            "range": "Produtos!AD5:AE5",
            "values": [[
                "Precificacao padronizada em 10/08/2026: classe baixa saida, S=N*0,50. Preco definido segue pendente.",
                "10/08/2026 10:15",
            ]],
        },
        {
            "range": "Produtos!R6:S6",
            "values": [["=(O6+P6)/2", 83.03]],
        },
        {
            "range": "Produtos!AD6:AE6",
            "values": [[
                "Precificacao padronizada em 10/08/2026: classe media saida, S=N*0,75. Preco definido segue pendente.",
                "10/08/2026 10:15",
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
