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
        "DS021",
        "10/08/2026",
        "Beleza e cuidados pessoais",
        "Escova secadora/modeladora ILINK Brush Hair Dryer and Styler, tensao 220V, cor preta com detalhe verde/azul, acompanha caixa e manual.",
        "ILINK",
        "ILINK Brush Hair Dryer and Styler 220V",
        "Novo com caixa avariada",
        "Nao informado",
        "Produto eletrico 220V; testar aquecimento, ventilacao e botoes antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        48.43,
        67.99,
        118.15,
        "Base principal Shopee nacional: 110V/220V Escova Secadora Alisador Eletrica Quente Cabelo 4 em 1 por R$48,43 no Pix com cupom / R$50,98 sem cupom, loja ILINK. Apoio Shopee nacional: Escova Secadora Alisadora 3 em 1 Hair Styler 110V/220V R$67,88-R$67,99; referencia alta do mesmo anuncio ILINK R$118,15. Produto equivalente forte por marca/universo ILINK, formato escova secadora/modeladora e voltagem 220V informada pelo usuario.",
        "=(O22+P22)/2",
        40.00,
        40.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Escova secadora/modeladora ILINK Brush 220V, para secar, alinhar e modelar os cabelos. Cor preta com detalhe verde/azul. Acompanha caixa e manual. Produto 220V; recomenda-se testar antes da retirada/entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Tensao informada pelo usuario: 220V. Caixa com avarias visiveis. Base Shopee nacional por equivalente forte. Classe media saida por produto eletrico que precisa teste: S=N*0,75, arredondado comercialmente para R$40,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 13:10",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A22:AE22",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
