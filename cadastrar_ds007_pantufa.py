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
        "DS007",
        "10/08/2026",
        "Calçados / Pantufas",
        "Par de pantufas/chinelos de pelúcia em formato de vaquinha, cor branco/bege com manchas pretas e marrons, detalhe de chifres e cabeça 3D. Solado branco, tamanho 36-37 marcado na sola.",
        "Não identificada",
        "Pantufa vaquinha pelúcia tamanho 36-37",
        "Usado",
        "Não se aplica",
        "Produto visualmente íntegro; sola com sinais de sujeira/uso conforme foto. Higienização recomendada antes da venda.",
        "Aguardando preço",
        "A1",
        "",
        "",
        69.99,
        72.99,
        78.99,
        "Shopee nacional: Pantufa Chinelo De Frio Adulto Vaca Vaquinha Peluda, estoque no Brasil, R$69,99-R$72,99; tamanho 36-37 aparece na descrição como 26 cm. Mercado Livre nacional similar R$78,99 usado como apoio.",
        "=(O8+P8)/2",
        52.49,
        "",
        "",
        "",
        "Não",
        "Não publicado",
        "Pantufa de pelúcia vaquinha tamanho 36-37, modelo confortável e quentinho, com cabeça 3D, chifres e solado branco. Produto usado, visualmente íntegro, com sinais de sujeira/uso na sola; higienização recomendada.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda não enviadas ao Drive. Referência nacional Shopee tratada como equivalente forte por tipo/modelo/tamanho. Classe média saída: S=N*0,75. Preço final pendente de confirmação do usuário.",
        "10/08/2026 11:00",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A8:AE8",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
