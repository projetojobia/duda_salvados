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
        "DS020",
        "10/08/2026",
        "Calcados",
        "Tenis feminino/juvenil rosa com detalhes pretos, solado branco alto, cabedal em tecido knit e cadarco. Numeracao 36/37.",
        "Nao identificada",
        "Tenis esportivo rosa 36/37",
        "Novo",
        "Nao se aplica",
        "Produto sem mecanismo; conferir par, numeracao 36/37 e estado geral antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        59.34,
        75.90,
        93.42,
        "Base Shopee nacional por equivalente forte: Tenis Feminino Preto Rosa Academia/Treino/Caminhada/Confortavel R$59,34; Tenis Esportivo Feminino Leve Macio Rosa Treino Caminhada Crossfit Academia R$75,90; Tenis Meia Feminino solado branco grosso R$93,42. Produto equivalente por estilo esportivo, cor rosa/preto, solado branco e numeracao feminina.",
        "=(O21+P21)/2",
        45.00,
        45.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Tenis feminino/juvenil rosa com detalhes pretos, solado branco alto e cabedal em tecido. Numeracao 36/37. Modelo leve para passeio, caminhada e uso casual.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Numeracao informada pelo usuario: 36/37. Base Shopee nacional por equivalente forte, sem marca identificada. Classe media saida por calcado com numeracao especifica: S=N*0,75, arredondado comercialmente para R$45,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 13:05",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A21:AE21",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
