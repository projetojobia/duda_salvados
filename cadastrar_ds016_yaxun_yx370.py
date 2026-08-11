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
        "DS016",
        "10/08/2026",
        "Ferramentas",
        "Kit de chaves de precisao Yaxun YX-370 6 em 1 para manutencao e reparo de celulares, notebooks e eletronicos, com estojo cilindrico e pontas AP2, T2, PH000, PH0000, W2.5 e Y000.",
        "Yaxun",
        "YX-370 Precision Screwdriver 6 em 1",
        "Novo com embalagem avariada",
        "Nao se aplica",
        "Produto manual; conferir se as 6 chaves/pontas estao presentes antes de publicar/entregar.",
        "Pronto para publicar",
        "A1",
        "",
        "",
        109.55,
        128.88,
        182.90,
        "Base principal Shopee nacional: Kit Chave Precisao Yaxun YX-370 6 em 1 Profissional Reparo Manutencao Celular Notebook iPhone Android R$109,55 no Pix com cupom / R$128,88 sem cupom. Apoio internacional apenas para identificacao: Alibaba lista YAXUN YX-370 Professional 6in1 Set a partir de US$8 em atacado, nao usado como base de preco. Produto correspondente por marca, modelo YX-370, formato e pontas.",
        "=(O17+P17)/2",
        80.00,
        80.00,
        "",
        "",
        "Nao",
        "Nao publicado",
        "Kit de chaves de precisao Yaxun YX-370 6 em 1, ideal para manutencao de celulares, notebooks e eletronicos. Acompanha estojo cilindrico e pontas de precisao AP2, T2, PH000, PH0000, W2.5 e Y000. Produto novo em embalagem.",
        "",
        "",
        "",
        "",
        "Fotos recebidas no Codex; ainda nao enviadas ao Drive. Identificacao confirmada pela embalagem: Yaxun YX-370 Precision Screwdriver. Base Shopee nacional correspondente. Classe media saida por ferramenta especifica para manutencao de eletronicos: S=N*0,75, arredondado comercialmente para R$80,00. Preco final definido automaticamente conforme nova regra.",
        "10/08/2026 12:45",
    ]]

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Produtos!A17:AE17",
        valueInputOption="USER_ENTERED",
        body={"values": row},
    ).execute()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
