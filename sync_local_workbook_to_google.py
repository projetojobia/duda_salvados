from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


WORKBOOK_PATH = Path(r"C:\Users\User\duda\Duda_Salvados_Hermes_GoogleSheets_v2_dashboard_executivo.xlsx")
SPREADSHEET_ID = "1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU"
EXPECTED_TITLE = "Duda Salvados - Base Oficial Restaurada"
GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)

sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


def convert_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M:%S")
    return value


def sheet_values(ws) -> list[list[Any]]:
    data: list[list[Any]] = []
    for row in ws.iter_rows():
        data.append([convert_value(cell.value) for cell in row])
    while data and all(value == "" for value in data[-1]):
        data.pop()
    if not data:
        return [[""]]
    max_cols = max(len(row) for row in data)
    return [row + [""] * (max_cols - len(row)) for row in data]


def sheet_bounds(ws) -> tuple[int, int]:
    last_row = 1
    last_col = 1
    for row in ws.iter_rows():
        for cell in row:
            if cell.value not in (None, ""):
                last_row = max(last_row, cell.row)
                last_col = max(last_col, cell.column)
    return last_row, last_col


def build_payload(workbook_path: Path) -> list[dict[str, Any]]:
    wb = load_workbook(workbook_path, data_only=False)
    data = []
    for ws in wb.worksheets:
        values = sheet_values(ws)
        last_row, last_col = sheet_bounds(ws)
        data.append(
            {
                "range": f"{ws.title}!A1:{get_column_letter(last_col)}{last_row}",
                "values": values,
            }
        )
    wb.close()
    return data


def verify_destination(service) -> str:
    metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, fields="properties/title").execute()
    title = metadata.get("properties", {}).get("title", "")
    if title != EXPECTED_TITLE:
        raise RuntimeError(f"Destino inesperado: {title!r}. Esperado: {EXPECTED_TITLE!r}")
    return title


def main() -> int:
    parser = argparse.ArgumentParser(description="Sincroniza a planilha local oficial com o Google Sheets restaurado.")
    parser.add_argument("--dry-run", action="store_true", help="Mostra o que seria enviado sem alterar o Google Sheets.")
    args = parser.parse_args()

    if not WORKBOOK_PATH.exists():
        raise FileNotFoundError(f"Planilha local nao encontrada: {WORKBOOK_PATH}")

    service = build_service("sheets", "v4")
    title = verify_destination(service)
    data = build_payload(WORKBOOK_PATH)

    total_cells = sum(len(item["values"]) * max((len(row) for row in item["values"]), default=0) for item in data)
    print(f"Destino: {title}")
    print(f"Arquivo local: {WORKBOOK_PATH.name}")
    print(f"Abas: {len(data)}")
    print(f"Celulas estimadas: {total_cells}")

    if args.dry_run:
        print("Dry-run: nenhuma alteracao enviada.")
        return 0

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": data},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
