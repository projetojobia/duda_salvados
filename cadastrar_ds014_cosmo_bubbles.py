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
        "DS014",
        "10/08/2026",
        "Brinquedos",
        "Caixa com 12 unidades de bolha de sabao Cosmo Bubbles 60 ml, marca Sigma Fill, tema infantil, indicado para lembrancinhas, festas e brincadeiras. Estoque com 2 caixas.",
        "Sigma Fill",
        "Cosmo Bubbles 60 ml caixa com 12 unidades",
        "Novo com caixa avariada",
        "Nao se aplica",
        "Produto lacrado/embalado; conferir se os frascos estao inteiros e sem vazamento antes de publicar/entregar.",
        "Aguardando preco",
        "A1",
        "",
        "",
        24.99,
        29.99,
        35.99,
        "Base principal Shopee nacional: CAIXA BOLHA DE SABAO SUPER DIVERTIDA COSMO BUBBLES C/12 UNIDADES R$24,99. Apoio nacional: Shopee kit com 12 Cosmo Bubbles 60 ml R$31,65; Magalu/marketplace nacional caixa 12 Cosmo Bubbles R$29,99 a R$35,99. Produto correspondente por nome, caixa com 12 pecas e frasco 60 ml.",
        "=(O15+P15)/2",
        22.00,
        "",
        "",
        "",
        "Nao",
        "Nao publicado",
        "Caixa com 12 bolhas de sabao Cosmo Bubbles 60 ml, ideal para festas infantis, lembrancinhas e brincadeiras. Produto novo em caixa. Temos 2 caixas disponiveis; valor anunciado por caixa.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Ha 2 caixas no estoque. Base Shopee nacional correspondente. Classe alta saida por item barato e infantil: S=N*0,90, arredondado comercialmente para R$22,00 por caixa. Preco final pendente.",
        "10/08/2026 12:30",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A15:AE15",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
