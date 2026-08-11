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
        "DS025",
        "10/08/2026",
        "Infantil / Roupas",
        "Pijama/macacao infantil de dinossauro em plush/pelucia, cor verde com barriga verde-limao, capuz com rosto de dinossauro, zíper frontal e punhos. Tamanho indicado para 80 cm de altura.",
        "Nao identificada",
        "Pijama macacao dinossauro infantil 80 cm",
        "Novo",
        "Nao se aplica",
        "Produto de vestuario; conferir tamanho 80 cm, costuras, zipper e estado geral antes de publicar/entregar.",
        "Disponível",
        "A1",
        "",
        "",
        59.00,
        74.95,
        124.10,
        "Base principal Shopee nacional por equivalente forte: Macacao de Plush de Bebe Infantil com estampa de Dinossauro R$59,00; Fantasia Infantil Dinossauro Plush Pijama Macacao com Capuz R$74,95; Pijama Macacao Infantil Sonho Meu Pelucia/Fleece Dinossauro R$124,10. Produto equivalente por tema dinossauro, plush/pelucia, macacao com capuz e uso infantil.",
        "=(O26+P26)/2",
        45.00,
        45.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Pijama/macacao infantil de dinossauro em plush, tamanho indicado para 80 cm de altura. Modelo verde com barriga verde-limao, capuz divertido, zipper frontal e punhos. Ideal para dormir, fantasia ou dias frios.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Tamanho informado pelo usuario: 80 cm de altura. Base Shopee nacional por equivalente forte. Classe media saida por roupa infantil com tamanho especifico: S=N*0,75, arredondado comercialmente para R$45,00. Preco final definido automaticamente conforme nova regra. Status inicial Disponivel.",
        "10/08/2026 14:00",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A26:AE26",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
