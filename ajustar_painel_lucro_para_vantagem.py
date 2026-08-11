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
            "range": "Produtos!U1:V1",
            "values": [["Vantagem ref. mercado (R$)", "Vantagem ref. mercado (%)"]],
        },
        {
            "range": "Produtos!U2:V301",
            "values": [
                [
                    f'=IF(OR(R{row}="";T{row}="");"";R{row}-T{row})',
                    f'=IF(OR(R{row}="";R{row}=0;T{row}="");"";(R{row}-T{row})/R{row})',
                ]
                for row in range(2, 302)
            ],
        },
        {
            "range": "Painel!A13",
            "values": [["Vantagem ref. mercado total"]],
        },
        {
            "range": "Painel!A15:B17",
            "values": [
                ["Resultado real do pallet", '=SUM(Produtos!AA2:AA301)-Lote!B9-\'Custos Operacionais\'!D4'],
                ["Investimento pallet", "=Lote!B9"],
                ["Despesas operacionais", "='Custos Operacionais'!D4"],
            ],
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
