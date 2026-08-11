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
        "DS019",
        "10/08/2026",
        "Casa e decoracao",
        "Capacho/tapete de entrada Bem-vindo, cor preta/cinza, modelo retangular com arabescos e base antiderrapante.",
        "Nao identificada",
        "Capacho Bem-vindo preto/cinza retangular",
        "Novo",
        "Nao se aplica",
        "Produto sem mecanismo; conferir medidas e estado geral antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        27.90,
        39.90,
        59.90,
        "Base Shopee nacional por equivalente forte: Capacho Tapete de Borracha antiderrapante Bem-vindo preto porta entrada R$27,90; Tapete Entrada Porta Casa/Apartamento Capacho 40x60/40x75 Bem Vindo preto/cinza R$39,90 a R$67,90; Tapete Porta Entrada Casa Capacho Vinil Light Preto 40x60cm R$59,90. Produto equivalente por tipo, texto Bem-vindo, cor escura e uso em porta de entrada.",
        "=(O20+P20)/2",
        25.00,
        25.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Capacho/tapete de entrada Bem-vindo, modelo retangular preto/cinza com arabescos. Ideal para porta de casa, apartamento ou comercio. Produto novo, pratico e decorativo.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Base Shopee nacional por equivalente forte. Classe alta saida por item domestico comum e barato: S=N*0,90, arredondado comercialmente para R$25,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 13:00",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A20:AE20",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
