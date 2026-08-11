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
    updates = [
        {
            "range": "Produtos!W2:AE2",
            "values": [[
                "Não",
                "Não publicado",
                "Relógio esportivo multifunção digital/analógico, com pulseira metálica, visor analógico e digital, funções LIGHT/START/RESET/MODE e resistência indicada WR 50M. Produto novo com etiqueta, não testado fisicamente.",
                "",
                "",
                "",
                "",
                "Revisão de correspondência em 10/08/2026: foto original do DS001 não está disponível neste chat; preço Shopee atual é de similar SANDA/SAMOA, não mesmo produto confirmado. Antes de publicar, validar foto/link correspondente exato.",
                "10/08/2026 10:35",
            ]],
        },
        {
            "range": "Produtos!W3:AE3",
            "values": [[
                "Não",
                "Não publicado",
                "Torneira gourmet/pre-rinse preta fosca com mola spray, bica alta e acabamento preto. Produto novo, sem marca visível e não testado.",
                "",
                "",
                "",
                "",
                "Revisão de correspondência em 10/08/2026: foto original do DS002 não está disponível neste chat; referências Shopee são equivalentes por tipo/modelo visual descrito. Antes de publicar, validar foto/link correspondente exato.",
                "10/08/2026 10:35",
            ]],
        },
        {
            "range": "Produtos!W4:AE4",
            "values": [[
                "Não",
                "Não publicado",
                "Vaso sanitário infantil/troninho branco e rosa, com tampa, tanque decorativo e botão de descarga simulado. Produto novo, sem marca visível e não testado.",
                "",
                "",
                "",
                "",
                "Revisão de correspondência em 10/08/2026: foto original do DS003 não está disponível neste chat; referências Shopee são equivalentes por tipo/modelo visual descrito. Produto reservado; validar antes de publicar se reserva cair.",
                "10/08/2026 10:35",
            ]],
        },
        {
            "range": "Produtos!W5:AE5",
            "values": [[
                "Não",
                "Não publicado",
                "Câmera digital compacta retrô estilo M3/Leica, prata e preta, com tela flip-up, lente f=2.8mm F=2.0 e manual incluso. Produto novo, não testado.",
                "",
                "",
                "",
                "",
                "Revisão de correspondência em 10/08/2026: foto original do DS004 não está disponível neste chat; referências Shopee são equivalentes por categoria, não mesmo produto confirmado. Manter preço pendente até validar foto/link correspondente exato.",
                "10/08/2026 10:35",
            ]],
        },
        {
            "range": "Produtos!AD6:AE6",
            "values": [[
                "Revisão de correspondência em 10/08/2026: foto recebida neste chat; usuário informou referência manual Shopee correspondente ao produto. Fotos ainda não enviadas ao Drive. Classe média saída; preço final pendente.",
                "10/08/2026 10:35",
            ]],
        },
        {
            "range": "Produtos!AD7:AE7",
            "values": [[
                "Revisão de correspondência em 10/08/2026: foto recebida neste chat e usuário confirmou que o link Shopee corresponde ao mesmo produto. Fotos ainda não enviadas ao Drive. Classe média saída; disponível por R$92,00.",
                "10/08/2026 10:35",
            ]],
        },
    ]

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": updates},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
