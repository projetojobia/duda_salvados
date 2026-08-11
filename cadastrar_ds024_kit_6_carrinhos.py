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
        "DS024",
        "10/08/2026",
        "Brinquedos",
        "Kit com 6 carrinhos miniatura die-cast Alloy Car Series/City Alloy Car, modelos variados estilo Cars, incluindo carro de policia, Relampago McQueen, guincho e carros de corrida.",
        "Nao identificada",
        "Alloy Car Series / City Alloy Car 6 pcs",
        "Novo com caixa avariada",
        "Nao se aplica",
        "Produto em embalagem; conferir se as 6 miniaturas estao presentes e sem avarias antes de publicar/entregar.",
        "Disponível",
        "A1",
        "",
        "",
        44.99,
        69.90,
        79.90,
        "Base principal Shopee nacional: Kit 6 Carrinhos Mini Alloy Car Series 1:60 Escavadeira, Bombeiro e Policia R$44,99. Apoio Shopee nacional: kit 6 carrinhos Cars Relampago McQueen metal diecast miniatura 1:55 R$39,99-R$79,99; mcqueen kit com 6 carros em metal 1/64 R$69,90; kit com 6 carrinhos de luxo em metal escala 1/64 R$79,90. Produto equivalente por kit com 6 miniaturas die-cast/metal e tema carros.",
        "=(O25+P25)/2",
        40.00,
        40.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Kit com 6 carrinhos miniatura die-cast Alloy Car Series, com modelos variados estilo Cars, policia, guincho e corrida. Brinquedo indicado para maiores de 3 anos. Produto novo em caixa; conferir as 6 unidades antes da entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Base Shopee nacional por equivalente forte. Classe alta saida por brinquedo barato e infantil: S=N*0,90, arredondado comercialmente para R$40,00. Preco final definido automaticamente conforme nova regra. Status inicial Disponivel.",
        "10/08/2026 13:55",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A25:AE25",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
