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
        "DS011",
        "10/08/2026",
        "Casa e cozinha",
        "Jogo de panelas de ferro fundido compativel com inducao, 3 pecas com tampas de vidro, acabamento marrom marmorizado/granilite, cabos e puxadores com efeito madeira. Conjunto cadastrado como um unico produto.",
        "Nao identificada",
        "Jogo de panelas ferro fundido inducao 3 pecas tampa vidro",
        "Nao informada",
        "Nao se aplica",
        "Compatibilidade com inducao e material ferro fundido informados pelo usuario; validar fisicamente o material antes de publicar.",
        "Aguardando preco",
        "A1",
        "",
        "",
        359.55,
        404.70,
        630.28,
        "Base principal Shopee nacional: Jogo 3 Cacarola Panela De Ferro Neo Inducao em torno de R$359,55. Apoio nacional fora da Shopee: Mercado Livre Jogo 3 Panelas Ferro Fundido Cacarola Tampa Vidro Inducao R$267,26; Magalu/lojas nacionais entre R$404,70 e R$662,82; WebContinental Rig Fundidos R$630,28. Observacao: visual pode lembrar conjunto antiaderente/marmore; cadastro segue informacao do usuario: ferro fundido e inducao.",
        "=(O12+P12)/2",
        269.66,
        "",
        "",
        "",
        "Nao",
        "Nao publicado",
        "Jogo de panelas 3 pecas em ferro fundido compativel com fogao de inducao, com tampas de vidro, acabamento marrom marmorizado e cabos efeito madeira. Conjunto cadastrado como unico produto. Material e compatibilidade informados pelo vendedor; conferir antes da entrega.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Usuario informou ferro fundido e inducao. Visual deve ter material validado antes de publicar. Referencias nacionais; base principal Shopee nacional. Classe media saida: S=N*0,75. Preco final pendente.",
        "10/08/2026 11:50",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A12:AE12",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
