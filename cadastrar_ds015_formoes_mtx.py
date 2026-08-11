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
        "DS015",
        "10/08/2026",
        "Ferramentas",
        "Jogo de formoes MTX 244329 com 4 pecas para madeira, medidas 6 mm, 12 mm, 18 mm e 24 mm, em aco cromo vanadio, cabo emborrachado e embalagem blister.",
        "MTX",
        "244329 - Jogo de Formoes Olho de Tigre 4 pecas",
        "Novo com embalagem avariada",
        "Nao se aplica",
        "Produto manual em embalagem; conferir integridade das 4 pecas e laminas antes de entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        75.90,
        79.30,
        118.16,
        "Base principal Shopee nacional: Jogo de Formao Olho de Tigre c/ 4 pecas 6 a 24mm - MTX 244329 R$75,90 com cupom; outra referencia Shopee nacional do mesmo produto R$79,30 no Pix; apoio nacional: Dutramaquinas jogo de formoes MTX 244329 R$93,01 no Pix / Shopee oficial/listagem R$118,16. Produto correspondente por marca, codigo 244329, medidas e embalagem.",
        "=(O16+P16)/2",
        55.00,
        55.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Jogo de formoes MTX 244329 com 4 pecas para madeira, medidas 6, 12, 18 e 24 mm. Ferramentas em aco cromo vanadio com cabo emborrachado, indicadas para marcenaria, carpintaria e pequenos trabalhos em madeira. Produto novo em embalagem.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Identificacao confirmada pela embalagem: MTX 244329, EAN 7899612791160. Base Shopee nacional com mesmo produto. Classe media saida por ferramenta especifica: S=N*0,75, arredondado comercialmente para R$55,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 12:40",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A16:AE16",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
