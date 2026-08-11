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
        "DS017",
        "10/08/2026",
        "Celulares e acessorios",
        "Capas para iPhone 13 Pro com logo estilo Apple e protecao de camera, cores azul e dourada. Estoque com 2 unidades.",
        "Nao identificada",
        "Capa iPhone 13 Pro com logo e protecao de camera",
        "Novo embalado",
        "Nao se aplica",
        "Produto embalado; conferir compatibilidade com iPhone 13 Pro e estado das 2 unidades antes da entrega.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        15.90,
        16.99,
        49.90,
        "Base principal Shopee nacional: Case/Capa/Capinha iPhone 13, Pro e Pro Max com logo Apple e protecao de camera premium R$15,90. Apoio nacional: oferta Shopee/Melhora o Preco capa silicone flexivel com logo e protecao na camera para iPhone 13/13 Pro/13 Pro Max R$16,99; outra referencia Shopee capa iPhone 13 Pro com protecao de camera R$49,90. Produto equivalente forte por modelo 13 Pro, logo e protecao de camera.",
        "=(O18+P18)/2",
        15.00,
        15.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Capa para iPhone 13 Pro com logo estilo Apple e protecao de camera. Temos 2 unidades disponiveis, nas cores azul e dourada. Produto novo embalado; valor anunciado por unidade.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Ha 2 unidades no estoque: azul e dourada. Base Shopee nacional por equivalente forte. Classe alta saida por acessorio barato e comum: S=N*0,90, arredondado comercialmente para R$15,00 por unidade. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 12:50",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A18:AE18",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
