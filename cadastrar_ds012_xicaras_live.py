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
        "DS012",
        "10/08/2026",
        "Casa e cozinha",
        "Jogo com 8 xicaras de ceramica branca Live Sub, modelo 150 ml para sublimacao, sem pires, em caixa de papelao com protecao individual.",
        "Live Sub",
        "Xicara ceramica branca 150 ml Live Sub",
        "Novo com caixa avariada",
        "Nao se aplica",
        "Produto de ceramica; conferir se as 8 unidades estao sem trincas ou lascas antes de publicar/entregar.",
        "Aguardando preco",
        "A1",
        "",
        "",
        108.12,
        127.20,
        139.80,
        "Busca por correspondencia visual e marca Live Sub. Nao foi localizada base Shopee nacional exata para o kit de 8 unidades. Referencias nacionais: Selprinter kit torre com 4 xicaras 150 ml Live Sub R$54,06 no pix, equivalente a R$108,12 para 8 unidades; Imprimaq xicara Live 150 ml unidade R$15,90, equivalente a R$127,20 para 8 unidades; Mercado Livre kit torre 4 xicaras Live 150 ml R$69,90, equivalente a R$139,80 para 8 unidades.",
        "=(O13+P13)/2",
        81.09,
        "",
        "",
        "",
        "Nao",
        "Nao publicado",
        "Jogo com 8 xicaras de ceramica branca Live Sub, 150 ml, ideal para cafe, lembrancinhas ou personalizacao por sublimacao. Produto em caixa com protecao individual. Conferir unidades antes da entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Etiqueta inferior identifica Live Sub. Sem base Shopee nacional exata localizada; referencias usadas sao nacionais e correspondentes por marca/modelo/capacidade. Classe media saida: S=N*0,75. Preco final pendente.",
        "10/08/2026 12:05",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A13:AE13",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
