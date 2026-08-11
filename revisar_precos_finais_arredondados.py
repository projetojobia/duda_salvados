from __future__ import annotations

import re
import sys
from pathlib import Path


SPREADSHEET_ID = "12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4"
GOOGLE_SCRIPTS = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts"
)

sys.path.insert(0, str(GOOGLE_SCRIPTS))

from google_api import build_service  # noqa: E402


HEADERS = [
    "Codigo",
    "Data cadastro",
    "Categoria",
    "Produto / descricao",
    "Marca",
    "Modelo",
    "Condicao",
    "Testado?",
    "Funcionamento",
    "Status interno",
    "Localizacao fisica",
    "Foto principal (URL)",
    "Pasta / fotos (URL)",
    "Preco baixo IA (R$)",
    "Preco medio IA (R$)",
    "Preco alto IA (R$)",
    "Fonte precos / URL",
    "Custo estimado ref. (R$)",
    "Preco sugerido IA (R$)",
    "Preco definido (R$)",
    "Lucro estimado ref. (R$)",
    "Margem estimada (%)",
    "Publicar no WhatsApp?",
    "Status catalogo",
    "Descricao para anuncio",
    "Data venda",
    "Preco venda real (R$)",
    "Lucro real ref. (R$)",
    "Cliente (opcional)",
    "Observacoes",
    "Ultima atualizacao",
]


def parse_brl(value: str) -> float | None:
    if not value:
        return None
    text = str(value)
    text = text.replace("R$", "").replace(".", "").replace(",", ".")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    return float(match.group(0))


def brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def round_commercial(value: float) -> float:
    if value <= 20:
        return round(value / 5) * 5
    if value <= 100:
        return round(value / 5) * 5
    return round(value / 10) * 10


def main() -> int:
    service = build_service("sheets", "v4")
    data = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A2:AE301",
    ).execute()
    rows = data.get("values", [])
    updates: list[dict[str, object]] = []
    summary: list[str] = []

    for offset, row in enumerate(rows, start=2):
        row = row + [""] * (len(HEADERS) - len(row))
        item = dict(zip(HEADERS, row))
        code = item["Codigo"]
        if not re.fullmatch(r"DS\d{3}", str(code)):
            continue
        has_content = any(str(item[h]).strip() for h in HEADERS[1:])
        if not has_content:
            continue

        defined = parse_brl(str(item["Preco definido (R$)"]))
        suggested = parse_brl(str(item["Preco sugerido IA (R$)"]))
        if defined is not None or suggested is None:
            continue

        final_price = round_commercial(suggested)
        obs = str(item["Observacoes"] or "").strip()
        obs = re.sub(r"\s*Preco final pendente\.?", "", obs)
        obs = re.sub(r"\s*Preço final pendente\.?", "", obs)
        if obs:
            obs += " "
        obs += (
            f"Preco final definido automaticamente na revisao de arredondamento: "
            f"{brl(final_price)}."
        )

        updates.append({
            "range": f"Produtos!J{offset}",
            "values": [["Pronto para publicar"]],
        })
        updates.append({
            "range": f"Produtos!T{offset}",
            "values": [[final_price]],
        })
        updates.append({
            "range": f"Produtos!AD{offset}:AE{offset}",
            "values": [[obs, "10/08/2026 13:30"]],
        })
        summary.append(f"{code}: {brl(suggested)} -> {brl(final_price)}")

    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"valueInputOption": "USER_ENTERED", "data": updates},
        ).execute()

    print("\n".join(summary) if summary else "Nenhum produto sem preco definido encontrado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
