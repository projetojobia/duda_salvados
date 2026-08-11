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
        "DS010",
        "10/08/2026",
        "Casa e cozinha",
        "Chaleira elétrica Onistek ON-CL202/220, cor bege/creme, 220V, potência 1500W, capacidade máxima indicada de 1,6L, com base elétrica, caixa e manual de instruções.",
        "Onistek",
        "ON-CL202/220",
        "Novo com caixa avariada",
        "Sim",
        "Produto testado conforme informado pelo usuário. Caixa com avarias visíveis; acompanha manual.",
        "Aguardando preço",
        "A1",
        "",
        "",
        65.34,
        99.07,
        115.20,
        "Base nacional: Shopee Brasil oficial/listagem nacional ON-CL202 1,6L 110V/220V R$65,34 | Magalu parceiro nacional ON-CL202 R$99,07 no Pix / R$115,20 em outros métodos | Mercado Livre nacional Onistek 1,6L 1500W em torno de R$64-R$66 como apoio.",
        "=(O11+P11)/2",
        58.81,
        "",
        "",
        "",
        "Não",
        "Não publicado",
        "Chaleira elétrica Onistek ON-CL202/220, 220V, 1500W, capacidade 1,6L, cor bege/creme. Produto testado, com caixa e manual. Caixa com avarias, ideal para uso diário na cozinha.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda não enviadas ao Drive. Identificação confirmada pela caixa: Onistek ON-CL202/220. Referências usadas apenas nacionais. Classe alta saída por utilidade doméstica: S=N*0,90. Preço final pendente.",
        "10/08/2026 11:40",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A11:AE11",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
