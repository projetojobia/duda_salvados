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
        "DS023",
        "10/08/2026",
        "Saude e cuidados pessoais",
        "Pacote promocional com 4 unidades de AdereFix creme adesivo para protese dental, 68 g cada, sabor original, ultra adesivo com duracao indicada de ate 12h.",
        "AdereFix",
        "Creme adesivo para protese dental 68 g sabor original - pacote 4 unidades",
        "Novo embalado",
        "Nao se aplica",
        "Produto de higiene/cuidado pessoal; conferir validade, lacre e integridade das 4 unidades antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        108.99,
        153.56,
        179.60,
        "Base nacional: Mercado Livre kit 4 unidades AdereFix creme adesivo para protese dental 68 g R$108,99. Apoio Shopee nacional: AdereFix 68 g unidade R$38,39, equivalente a R$153,56 para 4 unidades. Referencia alta por unidade em marketplaces nacionais na faixa de R$44,90, equivalente a R$179,60 para 4 unidades. Produto correspondente por marca, peso 68 g, uso e sabor original.",
        "=(O24+P24)/2",
        80.00,
        80.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Pacote com 4 unidades de AdereFix creme adesivo para protese dental, 68 g cada, sabor original. Ultra adesivo, com duracao indicada de ate 12h. Produto novo embalado; conferir validade e lacre antes da retirada/entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Pacote com 4 unidades informado pelo usuario. Produto de higiene/cuidado pessoal: conferir validade e lacres antes de publicar. Base nacional correspondente; Shopee nacional usada como apoio por unidade. Classe media saida por item especifico de cuidado pessoal: sugestao arredondada comercialmente para R$80,00 o pacote. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 13:25",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A24:AE24",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
