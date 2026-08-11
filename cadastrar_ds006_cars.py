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
    row = [[
        "DS006",
        "10/08/2026",
        "Brinquedos",
        "Conjunto brinquedo estilo Cars com caminhão Mack vermelho, carreta Rust-eze/Relâmpago McQueen 95 e carrinho McQueen pequeno. Embalagem Car and Players, indicação 3+ e die-cast metal.",
        "Car and Players / New Style Hot",
        "Caminhão Mack Relâmpago McQueen com carreta Rust-eze + carrinho",
        "Novo com caixa avariada",
        "Não",
        "Não testado fisicamente; produto aparentemente novo na embalagem, com caixa amassada/avariada.",
        "Disponível",
        "A1",
        "",
        "",
        123.41,
        129.90,
        149.00,
        "Shopee confirmado pelo usuário: Relâmpago McQueen + Caminhão Mack Metal Brinquedo Carreta Filme Carros Infantil Presente Criança R$123,41 no Pix / R$129,90 outros métodos; preço de referência original R$149,00.",
        "=(O7+P7)/2",
        92.00,
        92.00,
        "",
        "",
        "Não",
        "Não publicado",
        "Conjunto infantil estilo Cars com caminhão Mack vermelho, carreta Rust-eze/Relâmpago McQueen 95 e carrinho pequeno. Produto aparentemente novo na embalagem, caixa com avarias. Não testado fisicamente. Referência Shopee confirmada.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda não enviadas ao Drive. Produto confirmado pelo usuário como correspondente ao link Shopee. Classe média saída: preço sugerido/definido conservador em R$92,00.",
        "10/08/2026 10:25",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A7:AE7",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
