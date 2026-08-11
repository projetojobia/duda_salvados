from __future__ import annotations

import json
import sys
from pathlib import Path


SPREADSHEET_ID = "12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4"
SHEET_NAME = "Custos Operacionais"
GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)

sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


def main() -> int:
    service = build_service("sheets", "v4")
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = spreadsheet.get("sheets", [])
    existing = {
        sheet["properties"]["title"]: sheet["properties"]["sheetId"]
        for sheet in sheets
    }

    requests = []
    sheet_id = existing.get(SHEET_NAME)
    if sheet_id is None:
        requests.append(
            {
                "addSheet": {
                    "properties": {
                        "title": SHEET_NAME,
                        "gridProperties": {"rowCount": 1000, "columnCount": 8},
                    }
                }
            }
        )
        created = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests},
        ).execute()
        sheet_id = created["replies"][0]["addSheet"]["properties"]["sheetId"]

    values = [
        ["DUDA SALVADOS - CUSTOS OPERACIONAIS", "", "", "", "", "", "", ""],
        ["Resumo", "", "", "", "", "", "", ""],
        ["Total de despesas operacionais", "=SOMA(D6:D1000)", "", "Esses custos ficam separados do investimento do pallet.", "", "", "", ""],
        ["Investimento pallet", "='Lote'!B9", "", "Total geral considerado", "=B3+B4", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["Data", "Categoria", "Descrição", "Valor (R$)", "Forma pagamento", "Relacionado ao DS", "Comprovante/URL", "Observações"],
        ["", "Embalagem", "", "", "", "", "", ""],
        ["", "Frete/Transporte", "", "", "", "", "", ""],
        ["", "Anúncio/Marketing", "", "", "", "", "", ""],
        ["", "Taxa/Marketplace", "", "", "", "", "", ""],
        ["", "Limpeza/Manutenção", "", "", "", "", "", ""],
        ["", "Outros", "", "", "", "", "", ""],
    ]

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{SHEET_NAME}'!A1:H12",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()

    format_requests = [
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.08, "green": 0.32, "blue": 0.30},
                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True, "fontSize": 12},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)",
            }
        },
        {
            "mergeCells": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8},
                "mergeType": "MERGE_ALL",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 5, "endRowIndex": 6, "startColumnIndex": 0, "endColumnIndex": 8},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.90, "green": 0.96, "blue": 0.94},
                        "textFormat": {"bold": True},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 2, "endRowIndex": 4, "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {"userEnteredFormat": {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}}},
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 2, "endRowIndex": 4, "startColumnIndex": 4, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}}},
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 6, "endRowIndex": 1000, "startColumnIndex": 3, "endColumnIndex": 4},
                "cell": {"userEnteredFormat": {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}}},
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 8},
                "properties": {"pixelSize": 145},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
                "properties": {"pixelSize": 260},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 6, "endIndex": 8},
                "properties": {"pixelSize": 220},
                "fields": "pixelSize",
            }
        },
        {
            "updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 6}},
                "fields": "gridProperties.frozenRowCount",
            }
        },
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": format_requests},
    ).execute()

    print(json.dumps({"sheet": SHEET_NAME, "sheetId": sheet_id, "status": "ok"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
