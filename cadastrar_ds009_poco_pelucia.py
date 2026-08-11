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
        "DS009",
        "10/08/2026",
        "Brinquedos / Pelúcias",
        "Boneco de pelúcia do personagem Poco, de Brawl Stars, com rosto azul claro, cabelo preto, chapéu/poncho roxo e instrumento azul em formato de estrela. Sem embalagem visível.",
        "Brawl Stars / Genérica",
        "Poco pelúcia",
        "Usado",
        "Não se aplica",
        "Produto visualmente íntegro pela foto; sem teste aplicável. Recomendada higienização antes da venda.",
        "Aguardando preço",
        "A1",
        "",
        "",
        76.42,
        111.51,
        132.90,
        "Base nacional somente: Shopee nacional/ML equivalente 'Boneco Pelúcia Brawl Stars Jogo Boxten Roblox Decoração' R$76,42 (MG) | Magalu nacional 'Boneco de Pelúcia Brawl Stars' R$111,51 | ML nacional/pronta entrega Brawl Stars plush R$132,90. Anúncios internacionais de Poco/Brawl Stars descartados como base; usados apenas para identificação visual do personagem.",
        "=(O10+P10)/2",
        38.21,
        "",
        "",
        "",
        "Não",
        "Não publicado",
        "Pelúcia do personagem Poco, de Brawl Stars, com chapéu/poncho roxo e instrumento azul em formato de estrela. Produto usado, sem embalagem, visualmente íntegro. Higienização recomendada antes da venda.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda não enviadas ao Drive. Identificação visual: Poco, de Brawl Stars. Referências nacionais são equivalentes de pelúcia/Brawl Stars, não mesmo produto confirmado; anúncios internacionais mais próximos foram descartados como base de preço. Classe baixa saída por nicho e baixa confiança nacional: S=N*0,50. Preço final pendente.",
        "10/08/2026 11:30",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A10:AE10",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
