from __future__ import annotations

import sys
from pathlib import Path


GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)
sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


SPREADSHEET_ID = "12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4"


def main() -> int:
    service = build_service("sheets", "v4")
    data = []

    for r in range(2, 302):
        data.append(
            {
                "range": f"Produtos!R{r}:R{r}",
                "values": [[f'=IF(N{r}="";"";N{r}*50%)']],
            }
        )
        data.append(
            {
                "range": f"Produtos!U{r}:V{r}",
                "values": [[
                    f'=IF(OR(R{r}="";T{r}="");"";T{r}-R{r})',
                    f'=IF(OR(T{r}="";T{r}=0;U{r}="");"";U{r}/T{r})',
                ]],
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
