"""Compile pie PNGs into one PDF (ReportLab + Pillow)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from ._0_paths import PDF_DIR, PIE_DIR, ensure_out_dirs


def compile_pie_pdf(output_name: str = "Pie_Charts_Compilation.pdf") -> Path:
    ensure_out_dirs()
    folder = PIE_DIR
    images = sorted(folder.glob("*.png"))
    if not images:
        raise FileNotFoundError(f"No PNG files under {folder}")

    pdf_path = PDF_DIR / output_name
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter

    for image_path in images:
        img = Image.open(image_path)
        if img.width != img.height:
            side = max(img.width, img.height)
            square = Image.new("RGB", (side, side), (255, 255, 255))
            square.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
            img = square
        ar = img.width / img.height
        if ar > 1:
            img_width = width
            img_height = img_width / ar
        else:
            img_height = height
            img_width = img_height * ar
        x = (width - img_width) / 2 - 0.6 * 72
        y = (height - img_height) / 2
        c.drawInlineImage(img, x, y, img_width, img_height)
        c.showPage()
    c.save()
    return pdf_path
