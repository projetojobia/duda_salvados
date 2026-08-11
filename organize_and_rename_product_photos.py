from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path


SOURCE_ROOT = Path(
    r"C:\Users\User\.codex\codex-remote-attachments\019feb94-5bda-75f1-9b43-bf00c55a173d"
)
WORKSPACE_ROOT = Path(r"C:\Users\User\duda")
ORGANIZED_ROOT = WORKSPACE_ROOT / "Fotos_Organizadas" / "Fotos_Renomadas"
REF_ROOT = ORGANIZED_ROOT / "_referencias_dashboard"
REPORT_CSV = WORKSPACE_ROOT / "photo_rename_report.csv"
LEGACY_MANIFEST = WORKSPACE_ROOT / "fotos_organizadas_manifest.csv"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:70]


def load_manifest_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    if not LEGACY_MANIFEST.exists():
        return titles
    with LEGACY_MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (row.get("Codigo") or "").strip()
            desc = (row.get("Descricao") or "").strip()
            if code and desc:
                titles[code] = desc
    return titles


TITLE_BY_CODE: dict[str, str] = {
    # In this task we only need stable human-friendly labels for the codes
    # that appear in the organized photo batches.
    "DS001": "Relogio Sanda 3363 esportivo masculino",
    "DS005": "Carrinho plasma car rosa",
    "DS006": "Cars Mack com carreta",
    "DS007": "Pantufa vaquinha infantil",
    "DS008": "Pista dinossauro track toys",
    "DS009": "Boneco de pelucia",
    "DS011": "Jogo de panelas",
    "DS012": "Jogo de xicaras de ceramica",
    "DS013": "Relogio digital ES1155",
    "DS014": "Cosmo Bubbles kit 12 pecas",
    "DS015": "Jogo de formoes MTX",
    "DS016": "Kit chaves de precisao Yaxun YX370",
    "DS017": "Capas iPhone 13 Pro",
    "DS018": "Patins inline roxo",
    "DS019": "Capacho bem vindo",
    "DS020": "Tenis rosa 33Y",
    "DS021": "Escova blower ILINK",
    "DS022": "Tenis branco 37 38",
    "DS023": "AdereFix kit 4 unidades",
    "DS024": "Kit 6 carrinhos die cast",
    "DS025": "Pijama infantil dinossauro 80 cm",
    "DS026": "Motobomba de piscina WEG Sibrape",
    "DS027": "Tabua de corte em madeira",
    "DS028": "Banheira de bebe Adoleta 15L rosa",
    "DS029": "Babuche bege",
    "DS030": "Garrafa de vidro 1L Mimo Style",
    "DS031": "Caixas organizadoras kit 12",
    "DS032": "Extensao eletrica 15 m",
    "DS033": "Suporte articulado para TV",
    "DS034": "Calisul tira manchas",
    "DS035": "Kit balsamo labial 4 unidades",
    "DS036": "Concreto endurecedor com formol",
    "DS037": "Creme facial retinol colageno HA",
    "DS038": "Removedor de ferrugem Wurth 250 ml",
    "DS039": "Dimethylx 60 capsulas",
    "DS040": "Mascara capilar Arvensis Cachos Naturais",
    "DS041": "Colageno hidrolisado Covitta Beauty",
    "DS042": "Friskies saches filhotes carne 15 un",
    "DS043": "Cafe com Deus Pai",
    "DS044": "O Caibalion",
    "DS045": "Jogo de cama solteiro 4 pecas",
    "DS046": "Par de palhetas 22 26",
    "DS047": "Refil mop chenille pack 5",
    "DS048": "Tenis Dostin Hike preto",
    "DS049": "Arame farpado aco zincado 50 kgf",
    "DS050": "Macaco hidraulico 2T jacare",
    "DS051": "Pote para leite em po Buba",
    "DS052": "Meia calca infantil 120D",
    "DS053": "Massa de modelar DAS",
    "DS054": "Unhas postiças press on",
    "DS055": "Verniz acrilico Acrilex",
    "DS056": "Giotto 12 potes",
    "DS057": "Canetas line color pen 6 cores",
    "DS058": "Cilios clusters DIY",
    "DS059": "Cadeira escritorio preta",
    "DS060": "Vestido infantil branco festa luxo",
    "DS061": "Toalha infantil grande rosa",
    "DS062": "Porta retrato kit com 3",
    "DS063": "Kit 2 desodorantes cristal",
    "DS064": "Manta para sofa",
    "DS065": "Cilindros MDF cru trio",
    "DS066": "Buque arranjo de flores secas",
    "DS067": "Igora Royal louro claro",
    "DS068": "Necessaire feminina preta",
    "DS069": "Toalha infantil grande verde",
    "DS070": "Luz LED por do sol USB",
    "DS071": "Fone de ouvido Bluetooth",
    "DS072": "Refil mop giratorio pack 5",
}


SOURCE_PLAN: dict[str, list[str]] = {
    # Batches containing multiple products in one source folder
    "229D94F8-B8B9-4D8B-A081-747A3E4DC706": ["DS034", "DS035", "DS036"],
    "3B5D5471-04C4-48AE-82C2-83BBE14F28F9": ["DS042", "DS043", "DS044"],
    "7705B4D5-5F7D-4E70-816B-D5AF78B09063": ["DS045", "DS046", "DS046", "DS045"],
    "92E8A5BD-F91E-46AC-87C1-52D7DCD1CDC9": ["DS056", "DS057", "DS058"],
    "C2A0C9BB-73D9-4146-85C4-1C16853878CA": ["DS048", "DS049", "DS050"],
    "EC20E29C-E7F5-4057-A1E6-C4235FDCA0E4": ["DS037", "DS038", "DS039", "DS040", "DS041"],
    "F5C14013-BCED-4055-962F-535F106A959E": ["DS053", "DS054", "DS055"],
    "30B59BE6-0125-4A19-876D-01E099DB1C7A": ["DS067", "DS063"],
}


SINGLE_PRODUCT_PLAN: dict[str, str] = {
    "0192A27A-A86D-4AC1-8A7D-EFAEF977E168": "DS027",
    "03697557-F7AB-4E87-B868-62C198847058": "DS068",
    "04012255-FEE6-4E1E-B348-4EEAD516B0E3": "DS021",
    "05A5D97B-E740-4947-9FCF-8B65A43A9E91": "DS052",
    "06F569DB-B475-45E8-902D-03282AE48B5A": "DS059",
    "0D8D9241-04D9-4E21-AD7F-499D6F0AC409": "DS072",
    "1162E99C-5D35-4708-9A72-1BB28DF201D2": "DS064",
    "144B3181-E72B-4612-9C48-220C666E69D6": "DS051",
    "14A0B1C7-8FF5-4E2C-899F-DEFDBBA93B18": "DS029",
    "1CCFC3CC-783D-4FEA-98ED-4FFB605EAFE9": "DS071",
    "2F3FDD51-D06F-4571-B1D9-80AB1F06D6BC": "DS009",
    "2FAD1820-C823-4CA5-AAE4-2B6DBF4E2E1C": "DS009",
    "28259B7A-F993-4C0F-81FA-9E8E07C7D6EF": "DS047",
    "28B03819-5767-476D-8CF2-13F19CD701C4": "DS013",
    "3029DDA9-AD4B-4620-9100-867F62A53C0E": "DS061",
    "34D54AA1-157E-4870-924E-A8446B862F6D": "DS067",
    "4306E893-3102-4F3B-A200-7B02AA77BBA0": "DS020",
    "50CFE784-4F6B-4E36-874A-BD3365F6A885": "DS026",
    "57BA317F-087C-46D2-91F0-F9A4F8082B75": "DS005",
    "713A6AE1-54E4-40C3-85C0-3880E8B7BA13": "DS060",
    "79C0259B-EBFB-475B-B2C0-DF9011842FA1": "DS030",
    "79ED91FE-5816-4D9A-AA97-6792FBC4B550": "DS033",
    "7D43BBDB-7B71-4EAA-BE25-98D9D56B8FFF": "DS001",
    "82827411-07A2-408E-ADE7-BD04A15F804F": "DS017",
    "8679C00E-B686-467B-9FEE-8E40AC129C24": "DS066",
    "879FB56E-CA3A-4814-B519-D8BA3BF8ECED": "DS018",
    "964BB06C-3986-4D5B-B2E6-03BEBB0E8F48": "DS023",
    "992A66CA-ECA9-44FC-9E16-64BC26DBC7DD": "DS014",
    "A1D275E4-1CC1-4E3D-A221-7C5C33745125": "DS070",
    "A5522A6E-CFB4-4CC1-981E-D46B7251C3F8": "DS033",
    "A773D84D-0C04-40EF-9D37-49FF3CEFA7F0": "DS022",
    "B7CDE578-9F71-4E02-8B24-FB40391B4C71": "DS069",
    "B868B800-F3ED-47E6-A049-F3BBDD2CBD50": "DS012",
    "BBF034BA-7197-4AA4-9107-070B18EEB1A4": "DS062",
    "C74D3946-9399-4C02-AB75-841BD5DACED8": "DS015",
    "C76CA5CB-5CFD-4144-A2F6-8D769E1BDDE5": "DS024",
    "CB2E9E1F-B32E-449F-BB0E-8B11E59554E2": "DS032",
    "D1F86499-57F2-4B9A-8D14-62F8652A878B": "DS016",
    "D932D1A9-5A07-4DC5-A355-99EC33E9D7E2": "DS031",
    "DC1E8C36-D1B6-49CD-826E-039AB675A881": "DS005",
    "E8E32475-C4F4-4757-BB25-03DFD9E01E57": "DS019",
    "EE41C3D3-1ABC-4E81-9E93-093E3B8ACDCE": "DS028",
    "EECB5AFE-5DB4-4B48-B720-CA242C2A22B9": "DS001",
    "F3E59E0B-DF94-48A0-B3A5-02767160BB99": "DS006",
    "F48EEC15-0198-4DD7-AFC2-AE51E26F1A12": "DS011",
    "F6D428CD-DB99-40E4-9CB5-4AB9B5758254": "DS008",
    "F8063A77-81E0-451A-A56B-EE1BB6831EC8": "DS007",
    "F83F90F8-A7BF-40EB-938D-1A81826B4891": "DS065",
    "FBB42352-96E6-4DE0-8377-689936CF9555": "DS025",
}


REFERENCE_FOLDERS = {
    "53A0A28C-191E-487C-8211-A182D97C718B",
    "76B4C798-D488-4E59-A81B-6FAD5E0A4ACC",
    "7FC333C1-CC63-4C92-9277-C596D8AF8CB7",
    "B8007D07-0209-4268-A467-225A51B8B650",
    "DB7E376C-B55D-4DE5-9783-0505D89BE4A0",
}


def build_copy_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for folder_id, code in SINGLE_PRODUCT_PLAN.items():
        src_folder = SOURCE_ROOT / folder_id
        if not src_folder.exists():
            continue
        for src_file in sorted(src_folder.iterdir()):
            if src_file.is_file():
                rows.append(
                    {
                        "source_folder": folder_id,
                        "source_file": src_file.name,
                        "code": code,
                    }
                )

    for folder_id, codes in SOURCE_PLAN.items():
        src_folder = SOURCE_ROOT / folder_id
        if not src_folder.exists():
            continue
        files = sorted([p for p in src_folder.iterdir() if p.is_file()])
        if len(files) != len(codes):
            raise RuntimeError(
                f"Folder {folder_id} has {len(files)} files but {len(codes)} codes were planned."
            )
        for src_file, code in zip(files, codes, strict=True):
            rows.append(
                {
                    "source_folder": folder_id,
                    "source_file": src_file.name,
                    "code": code,
                }
            )

    return rows


def main() -> int:
    titles = load_manifest_titles()
    titles.update(TITLE_BY_CODE)

    ORGANIZED_ROOT.mkdir(parents=True, exist_ok=True)
    REF_ROOT.mkdir(parents=True, exist_ok=True)

    rows = build_copy_rows()
    rows.sort(key=lambda r: (r["code"], r["source_folder"], r["source_file"]))

    counters: dict[str, int] = defaultdict(int)
    report_rows = []

    for row in rows:
        code = row["code"]
        title = titles.get(code, code)
        code_slug = slugify(title)
        folder_name = f"{code}_{code_slug}"
        target_folder = ORGANIZED_ROOT / folder_name
        target_folder.mkdir(parents=True, exist_ok=True)

        counters[code] += 1
        seq = counters[code]
        src_path = SOURCE_ROOT / row["source_folder"] / row["source_file"]
        ext = src_path.suffix.lower() or ".jpg"
        target_name = f"{code}_{code_slug}_{seq:02d}{ext}"
        target_path = target_folder / target_name
        shutil.copy2(src_path, target_path)

        report_rows.append(
            {
                "Tipo": "PRODUTO",
                "Codigo": code,
                "Titulo": title,
                "OrigemPasta": row["source_folder"],
                "OrigemArquivo": row["source_file"],
                "DestinoPasta": str(target_folder),
                "DestinoArquivo": str(target_path),
            }
        )

    # Organiza as referencias de dashboard num bloco separado
    for idx, folder_id in enumerate(sorted(REFERENCE_FOLDERS), start=1):
        src_folder = SOURCE_ROOT / folder_id
        if not src_folder.exists():
            continue
        ref_target_folder = REF_ROOT / f"ref_{idx:02d}_{folder_id.lower()[:8]}"
        ref_target_folder.mkdir(parents=True, exist_ok=True)
        for i, src_file in enumerate(sorted(p for p in src_folder.iterdir() if p.is_file()), start=1):
            ext = src_file.suffix.lower() or ".jpg"
            target_name = f"dashboard_ref_{idx:02d}_{i:02d}{ext}"
            target_path = ref_target_folder / target_name
            shutil.copy2(src_file, target_path)
            report_rows.append(
                {
                    "Tipo": "REFERENCIA",
                    "Codigo": "REF",
                    "Titulo": f"Dashboard ref {folder_id[:8]}",
                    "OrigemPasta": folder_id,
                    "OrigemArquivo": src_file.name,
                    "DestinoPasta": str(ref_target_folder),
                    "DestinoArquivo": str(target_path),
                }
            )

    with REPORT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Tipo",
                "Codigo",
                "Titulo",
                "OrigemPasta",
                "OrigemArquivo",
                "DestinoPasta",
                "DestinoArquivo",
            ],
        )
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"Fotos organizadas em: {ORGANIZED_ROOT}")
    print(f"Relatorio salvo em: {REPORT_CSV}")
    print(f"Total de itens copiados: {len(report_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
