from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


WORKBOOK_PATH = Path(r"C:\Users\User\duda\Duda_Salvados_Hermes_GoogleSheets_v2.xlsx")
SPREADSHEET_ID = "12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4"
GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)

sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


def sheet_values(ws):
    data = []
    for row in ws.iter_rows():
        values = []
        for cell in row:
            values.append(cell.value)
        data.append(values)
    while data and all(v is None or v == "" for v in data[-1]):
        data.pop()
    if not data:
        return [[""]]
    max_cols = max(len(row) for row in data)
    return [row + [""] * (max_cols - len(row)) for row in data]


def sheet_bounds(ws):
    last_row = 1
    last_col = 1
    for row in ws.iter_rows():
        for cell in row:
            if cell.value not in (None, ""):
                last_row = max(last_row, cell.row)
                last_col = max(last_col, cell.column)
    return last_row, last_col


def main() -> int:
    wb = load_workbook(WORKBOOK_PATH, data_only=False)
    service = build_service("sheets", "v4")
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

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": data},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
