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
        "DS008",
        "10/08/2026",
        "Brinquedos",
        "Brinquedo pista dinossauro 2 em 1 Slide Track Toys, com dinossauro verde, trilhos/escorregador, luz, música e escada automática. Indicação 3+ anos. Caixa com avarias visíveis.",
        "Slide Track Toys",
        "Pista Dinossauro 2 em 1 com luz, música e escada automática",
        "Novo com caixa avariada",
        "Não",
        "Não testado fisicamente; caixa avariada. Conteúdo e funcionamento devem ser conferidos antes de entrega.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        60.80,
        84.92,
        151.05,
        "Shopee nacional: Pista Dinossauro Escorrega De Brinquedo Com Luz E Som Rex R$60,80/R$64,00 | Shopee nacional similar: Pista Dinossauro 2 em 1 Caminhão/Cegonha R$84,92 | Magalu nacional: Trilha De Dinossauro SLIDE TRACK TOYS R$151,05. Anúncios internacionais similares descartados como base de preço.",
        "=(O9+P9)/2",
        45.60,
        35.00,
        "",
        "",
        "Não",
        "Não publicado",
        "Pista dinossauro infantil 2 em 1 Slide Track Toys, com trilhos/escorregador, luz, música e escada automática. Produto aparentemente novo, caixa avariada. Não testado fisicamente; recomendado conferir conteúdo e funcionamento.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda não enviadas ao Drive. Referência nacional Shopee tratada como equivalente forte/correspondente por tema e recursos visíveis. Classe média saída: S=N*0,75. Usuário definiu preço final T=R$35,00.",
        "10/08/2026 11:20",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A9:AE9",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
