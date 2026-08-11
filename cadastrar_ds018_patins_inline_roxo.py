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
        "DS018",
        "10/08/2026",
        "Esporte e lazer",
        "Patins inline ajustavel preto e roxo, tamanho 35 ao 38, com 4 rodas em linha, fechamento por presilha/cadarco e bolsa de transporte.",
        "Nao identificada",
        "Patins inline ajustavel 35-38 preto/roxo",
        "Novo com embalagem/bolsa",
        "Nao informado",
        "Conferir regulagem de tamanho, travas, rodas e estado geral antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        155.00,
        189.90,
        245.65,
        "Base Shopee nacional por equivalente forte: patins inline ajustavel preto/roxo infantil/juvenil na faixa de R$155,00; outras referencias nacionais de patins inline ajustavel roxo/preto entre R$189,90 e R$245,65. Produto correspondente por tipo, cor, rodas em linha e faixa ajustavel; tamanho confirmado pelo usuario como 35 ao 38.",
        "=(O19+P19)/2",
        115.00,
        115.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Patins inline ajustavel preto e roxo, tamanho 35 ao 38, com 4 rodas em linha e bolsa de transporte. Modelo esportivo com fechamento por presilha e cadarco. Ideal para lazer e passeio. Conferir regulagem e rodas antes da retirada/entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Tamanho correto informado pelo usuario: 35 ao 38. Base Shopee nacional por equivalente forte. Classe media saida por produto de lazer com tamanho especifico: S=N*0,75, arredondado comercialmente para R$115,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 12:55",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A19:AE19",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
