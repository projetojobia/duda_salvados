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
        "DS013",
        "10/08/2026",
        "Casa e decoracao",
        "Relogio digital redondo LED com cabo USB, modelo ES1155, 11x4 cm, com funcoes de hora 12/24h, soneca, temperatura e calendario. Estoque com 2 unidades.",
        "Tick Tack",
        "ES1155",
        "Novo com caixa avariada",
        "Sim",
        "Uma unidade aparece ligada e funcionando na foto. Conferir as 2 unidades antes da entrega.",
        "Aguardando preco",
        "A1",
        "",
        "",
        21.99,
        32.95,
        55.10,
        "Base Shopee nacional por correspondencia de caracteristicas: Relogio Digital De Mesa 11x4CM Com Usb Temperatura Calendario Soneca Redondo Decoracao R$21,99; Shopee relogio digital LCD mesa/parede redondo medio/grande R$32,95; Shopee relogio digital LED despertador mesa/parede via USB R$55,10. Identificacao principal pela caixa: ES1155 Relogio Digital Redondo Com Cabo USB 11x4cm.",
        "=(O14+P14)/2",
        19.79,
        "",
        "",
        "",
        "Nao",
        "Nao publicado",
        "Relogio digital redondo LED com cabo USB, modelo ES1155, tamanho 11x4 cm. Mostra hora, temperatura e calendario, com funcao soneca. Produto compacto para mesa, criado-mudo ou decoracao. Estoque com 2 unidades; valor anunciado por unidade, salvo combinacao diferente.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Ha 2 unidades no estoque. Base principal Shopee nacional por produto equivalente forte em tamanho/funcoes. Classe alta saida por item barato e utilidade domestica: S=N*0,90. Preco final pendente.",
        "10/08/2026 12:20",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A14:AE14",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
