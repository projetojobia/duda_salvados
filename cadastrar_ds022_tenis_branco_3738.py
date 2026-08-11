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
        "DS022",
        "10/08/2026",
        "Calcados",
        "Tenis feminino casual branco com detalhe preto, solado plataforma/flatform branco com listras pretas, etiqueta Life. Numeracao 37/38.",
        "Life",
        "Tenis casual branco plataforma 37/38",
        "Novo",
        "Nao se aplica",
        "Produto sem mecanismo; conferir par, cadarcos, numeracao 37/38 e estado geral antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        44.90,
        64.90,
        69.90,
        "Base Shopee nacional por equivalente forte: Tenis Leve Plataforma Casual Branco Feminino Confortavel R$44,90; Tenis Feminino Plataforma Branco Buffalo Original R$64,90-R$69,90; Tenis Plataforma Feminino Casual Confortavel branco R$69,00. Produto equivalente por tipo, cor branca, solado plataforma/flatform e uso casual feminino.",
        "=(O23+P23)/2",
        35.00,
        35.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Tenis feminino casual branco com detalhe preto e solado plataforma/flatform com listras pretas. Numeracao 37/38. Modelo versatil para uso diario, passeio e looks casuais.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Numeracao informada pelo usuario: 37/38. Base Shopee nacional por equivalente forte, marca Life identificada pela etiqueta. Classe media saida por calcado com numeracao especifica: S=N*0,75, arredondado comercialmente para R$35,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 13:20",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A23:AE23",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
