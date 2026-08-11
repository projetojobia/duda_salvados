from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SPREADSHEET_ID = "1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU"
PRODUCTS_SHEET = "Produtos"
HERMES_GOOGLE_API = Path(
    r"C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts\google_api.py"
)

PRODUCT_HEADERS = [
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
    "Vantagem ref. mercado (R$)",
    "Vantagem ref. mercado (%)",
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

COLUMN_LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "AA",
    "AB",
    "AC",
    "AD",
    "AE",
]

FORMULA_COLUMNS = {"R", "U", "V", "AB"}
READ_ONLY_COLUMNS = {"A", *FORMULA_COLUMNS}

COL_TO_INDEX = {letter: index for index, letter in enumerate(COLUMN_LETTERS)}
FIELD_TO_COL = {field: COLUMN_LETTERS[index] for index, field in enumerate(PRODUCT_HEADERS)}


class SheetsHelperError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProductRow:
    code: str
    row_number: int
    values: list[Any]

    @property
    def is_free(self) -> bool:
        return bool(self.code) and all(_is_empty(value) for value in self.values[1:])

    def as_dict(self) -> dict[str, Any]:
        padded = _pad_row(self.values)
        return {PRODUCT_HEADERS[index]: padded[index] for index in range(len(PRODUCT_HEADERS))}


class SheetsClient:
    def __init__(
        self,
        spreadsheet_id: str = SPREADSHEET_ID,
        google_api_path: Path = HERMES_GOOGLE_API,
        python_executable: str = sys.executable,
    ) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.google_api_path = google_api_path
        self.python_executable = python_executable

    def get_values(self, range_name: str) -> list[list[Any]]:
        payload = self._run_google_api(["sheets", "get", self.spreadsheet_id, range_name])
        return _extract_values(payload)

    def update_values(self, range_name: str, values: list[list[Any]]) -> dict[str, Any]:
        payload = self._run_google_api(
            [
                "sheets",
                "update",
                self.spreadsheet_id,
                range_name,
                "--values",
                json.dumps(values, ensure_ascii=False),
            ]
        )
        if isinstance(payload, dict):
            return payload
        return {"result": payload}

    def list_product_rows(self, end_row: int = 301) -> list[ProductRow]:
        rows = self.get_values(f"{PRODUCTS_SHEET}!A2:AE{end_row}")
        product_rows: list[ProductRow] = []
        for offset, row in enumerate(rows, start=2):
            padded = _pad_row(row)
            code = str(padded[0] or "").strip()
            if code:
                product_rows.append(ProductRow(code=code, row_number=offset, values=padded))
        return product_rows

    def find_next_free_code(self, end_row: int = 301) -> ProductRow:
        for row in self.list_product_rows(end_row=end_row):
            if row.is_free:
                return row
        raise SheetsHelperError("Nenhum codigo DSxxx livre encontrado no intervalo configurado.")

    def read_product(self, code: str) -> ProductRow:
        normalized = normalize_code(code)
        for row in self.list_product_rows():
            if row.code.upper() == normalized:
                return row
        raise SheetsHelperError(f"Codigo nao encontrado: {normalized}")

    def update_product_fields(
        self,
        code: str,
        fields: dict[str, Any],
        update_timestamp: bool = True,
    ) -> ProductRow:
        before = self.read_product(code)
        updates = dict(fields)
        if update_timestamp:
            updates["AE"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        for key in updates:
            col = resolve_column(key)
            if col in READ_ONLY_COLUMNS:
                raise SheetsHelperError(f"Coluna protegida contra escrita: {col}")

        for key, value in updates.items():
            col = resolve_column(key)
            self.update_values(f"{PRODUCTS_SHEET}!{col}{before.row_number}", [[value]])

        return self.read_product(before.code)

    def define_price(self, code: str, price: float) -> ProductRow:
        row = self.read_product(code)
        status = _cell(row.values, "J")
        updates: dict[str, Any] = {"T": price}
        if status == "Aguardando preço":
            updates["J"] = "Pronto para publicar"
        return self.update_product_fields(row.code, updates)

    def reserve(self, code: str, customer: str | None = None) -> ProductRow:
        row = self.read_product(code)
        status = _cell(row.values, "J")
        if status != "Disponível":
            raise SheetsHelperError(f"Produto {row.code} nao esta Disponivel; status atual: {status!r}")

        updates: dict[str, Any] = {"J": "Reservado", "W": "Não"}
        if customer:
            updates["AC"] = customer
        return self.update_product_fields(row.code, updates)

    def sell(self, code: str, sale_price: float, customer: str | None = None) -> ProductRow:
        row = self.read_product(code)
        status = _cell(row.values, "J")
        allowed = {"Disponível", "Reservado", "Publicado"}
        if status not in allowed:
            raise SheetsHelperError(f"Produto {row.code} nao pode ser vendido com status atual: {status!r}")
        if not _is_empty(_cell(row.values, "AA")):
            raise SheetsHelperError(f"Produto {row.code} ja tem preco de venda real em AA.")

        updates: dict[str, Any] = {
            "J": "Vendido",
            "Z": datetime.now().strftime("%d/%m/%Y"),
            "AA": sale_price,
            "W": "Não",
        }
        if _cell(row.values, "X") == "Publicado":
            updates["X"] = "Remover"
        if customer:
            updates["AC"] = customer
        return self.update_product_fields(row.code, updates)

    def _run_google_api(self, args: list[str]) -> Any:
        if not self.google_api_path.exists():
            raise SheetsHelperError(f"google_api.py nao encontrado: {self.google_api_path}")

        command = [self.python_executable, str(self.google_api_path), *args]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise SheetsHelperError(completed.stderr.strip() or completed.stdout.strip())

        output = completed.stdout.strip()
        if not output:
            return {}
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return output


def resolve_column(key: str) -> str:
    clean = key.strip()
    upper = clean.upper()
    if upper in COL_TO_INDEX:
        return upper

    normalized_key = _normalize_label(clean)
    for field, col in FIELD_TO_COL.items():
        if _normalize_label(field) == normalized_key:
            return col

    raise SheetsHelperError(f"Campo/coluna desconhecido: {key}")


def normalize_code(code: str) -> str:
    clean = code.strip().upper()
    if clean.startswith("DS") and clean[2:].isdigit():
        return f"DS{int(clean[2:]):03d}"
    raise SheetsHelperError(f"Codigo invalido: {code}")


def _extract_values(payload: Any) -> list[list[Any]]:
    if isinstance(payload, dict):
        values = payload.get("values", [])
        if isinstance(values, list):
            return values
    if isinstance(payload, list):
        return payload
    raise SheetsHelperError(f"Resposta inesperada do google_api.py: {payload!r}")


def _pad_row(row: list[Any]) -> list[Any]:
    return [*row, *([None] * (len(PRODUCT_HEADERS) - len(row)))] [: len(PRODUCT_HEADERS)]


def _cell(row: list[Any], col: str) -> Any:
    return _pad_row(row)[COL_TO_INDEX[col]]


def _is_empty(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def _normalize_label(label: str) -> str:
    replacements = {
        "ç": "c",
        "ã": "a",
        "á": "a",
        "à": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ü": "u",
    }
    lowered = label.lower()
    for source, target in replacements.items():
        lowered = lowered.replace(source, target)
    return " ".join(lowered.split())


def _print_row(row: ProductRow) -> None:
    print(json.dumps({"code": row.code, "row_number": row.row_number, "values": row.as_dict()}, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Helper seguro para a planilha Duda Salvados.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("next-free", help="Mostra o proximo codigo DSxxx livre.")

    read_parser = subparsers.add_parser("read", help="Le uma linha por codigo.")
    read_parser.add_argument("code")

    set_parser = subparsers.add_parser("set", help="Atualiza uma celula editavel por codigo.")
    set_parser.add_argument("code")
    set_parser.add_argument("field_or_col")
    set_parser.add_argument("value")

    update_parser = subparsers.add_parser("update-json", help="Atualiza varios campos editaveis por codigo.")
    update_parser.add_argument("code")
    update_parser.add_argument("fields_json")

    update_file_parser = subparsers.add_parser("update-json-file", help="Atualiza varios campos a partir de um arquivo JSON.")
    update_file_parser.add_argument("code")
    update_file_parser.add_argument("json_path")

    price_parser = subparsers.add_parser("define-price", help="Define preco em T e avanca status quando aplicavel.")
    price_parser.add_argument("code")
    price_parser.add_argument("price", type=float)

    reserve_parser = subparsers.add_parser("reserve", help="Reserva um produto disponivel.")
    reserve_parser.add_argument("code")
    reserve_parser.add_argument("--customer")

    sell_parser = subparsers.add_parser("sell", help="Registra venda.")
    sell_parser.add_argument("code")
    sell_parser.add_argument("sale_price", type=float)
    sell_parser.add_argument("--customer")

    args = parser.parse_args()
    client = SheetsClient()

    if args.command == "next-free":
        _print_row(client.find_next_free_code())
    elif args.command == "read":
        _print_row(client.read_product(args.code))
    elif args.command == "set":
        _print_row(client.update_product_fields(args.code, {args.field_or_col: args.value}))
    elif args.command == "update-json":
        fields = json.loads(args.fields_json)
        if not isinstance(fields, dict):
            raise SheetsHelperError("fields_json deve ser um objeto JSON.")
        _print_row(client.update_product_fields(args.code, fields))
    elif args.command == "update-json-file":
        fields = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
        if not isinstance(fields, dict):
            raise SheetsHelperError("json_path deve conter um objeto JSON.")
        _print_row(client.update_product_fields(args.code, fields))
    elif args.command == "define-price":
        _print_row(client.define_price(args.code, args.price))
    elif args.command == "reserve":
        _print_row(client.reserve(args.code, args.customer))
    elif args.command == "sell":
        _print_row(client.sell(args.code, args.sale_price, args.customer))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
