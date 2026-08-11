from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"C:\Users\User\.codex\codex-remote-attachments\019feb94-5bda-75f1-9b43-bf00c55a173d")
OUT_DIR = Path(r"C:\Users\User\duda")
COLS = 3
CELL_W = 640
CELL_H = 520
HEADER_H = 110
TITLE_H = 60
MARGIN = 24


def first_image(folder: Path) -> Path | None:
    imgs = sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )
    return imgs[0] if imgs else None


def font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def build_sheet(folder_names: list[str], out_name: str) -> None:
    items = []
    for name in folder_names:
        folder = ROOT / name
        img = first_image(folder)
        if img:
            items.append((name, img))

    rows = max(1, math.ceil(len(items) / COLS))
    width = COLS * CELL_W + (COLS + 1) * MARGIN
    height = TITLE_H + HEADER_H + rows * CELL_H + (rows + 1) * MARGIN
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = font(26, bold=True)
    label_font = font(18, bold=True)
    small_font = font(14)

    draw.text((MARGIN, 16), out_name.replace("_", " "), fill="black", font=title_font)
    draw.text((MARGIN, 48), f"Root: {ROOT.name}", fill="#555555", font=small_font)

    for idx, (folder_name, img_path) in enumerate(items):
        row, col = divmod(idx, COLS)
        x0 = MARGIN + col * CELL_W
        y0 = TITLE_H + HEADER_H + row * CELL_H + MARGIN
        box = (x0, y0, x0 + CELL_W - MARGIN, y0 + CELL_H - MARGIN)
        draw.rounded_rectangle(box, radius=18, outline="#dddddd", width=2, fill="#fafafa")

        label = f"{idx+1:02d}. {folder_name}"
        draw.text((x0 + 18, y0 + 12), label, fill="#111111", font=label_font)
        try:
            with Image.open(img_path) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                thumb = ImageOps.contain(im, (CELL_W - 40, CELL_H - 100))
                tx = x0 + (CELL_W - MARGIN - thumb.width) // 2
                ty = y0 + 56 + (CELL_H - 100 - thumb.height) // 2
                canvas.paste(thumb, (tx, ty))
        except Exception as exc:
            draw.text((x0 + 18, y0 + 70), f"ERRO: {exc}", fill="red", font=small_font)

        draw.text((x0 + 18, y0 + CELL_H - 42), img_path.name, fill="#666666", font=small_font)

    out_path = OUT_DIR / out_name
    canvas.save(out_path, quality=92)
    print(out_path)


def main() -> None:
    folders = sorted([p.name for p in ROOT.iterdir() if p.is_dir()])
    chunks = [folders[i:i + 24] for i in range(0, len(folders), 24)]
    for i, chunk in enumerate(chunks, start=1):
        build_sheet(chunk, f"contact_sheet_{i}.jpg")


if __name__ == "__main__":
    main()
