"""Typeset Actual Size, its A4 folding sheets, and the first proof of page three."""

from argparse import ArgumentParser
from datetime import date
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, A5, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


TITLE = "Actual Size"
MADE = date(2026, 11, 20)
OUTPUT = Path(__file__).resolve().parent / "output" / "pdf"
SHEET_WIDTH, SHEET_HEIGHT = landscape(A4)
WIDTH, HEIGHT = SHEET_WIDTH / 4, SHEET_HEIGHT / 2
MARGIN = 10 * mm
MEASURE = WIDTH - 2 * MARGIN
BODY_TOP = HEIGHT - 21 * mm
BODY_SIZE = 12.5
LEADING = 15.8
PARAGRAPH_GAP = 8
SEAM_Y = 33 * mm

INK = HexColor("#21201E")
RED = HexColor("#AC3827")
GRAY = HexColor("#82746D")
WASH = HexColor("#F2EBE5")
REVERSE_RED = HexColor("#BE6456")
TRANSMITTED_RED = HexColor("#C98679")
PAPER_EDGE = HexColor("#D8CCC4")

ROMAN = "STIXText"
ITALIC = "STIXItalic"
MONO = "Courier"

# The first proof used a slightly different top baseline.
FIRST_PROOF_TOP = 237
FIRST_PROOF_OPENING = (
    "I pictured a page that would change as you read it. "
    "You could see what had occupied a sentence’s place."
)
FIRST_PROOF_CLOSING = (
    "I drew a rectangle. I wanted to see how much of the sitting would fit on one sheet."
)


def label(pdf, value, x, y, *, size=8, color=RED):
    pdf.setFillColor(color)
    pdf.setFont(MONO, size)
    pdf.drawString(x, y, value)


def body_lines(value):
    return simpleSplit(value, ROMAN, BODY_SIZE, MEASURE)


def paragraph(pdf, value, y, *, color=INK):
    pdf.setFillColor(color)
    pdf.setFont(ROMAN, BODY_SIZE)
    for line in body_lines(value):
        pdf.drawString(MARGIN, y, line)
        y -= LEADING
    return y


def passage(pdf, opening, closing):
    y = paragraph(pdf, opening, BODY_TOP)
    paragraph(pdf, closing, y - PARAGRAPH_GAP)


def folio(pdf, number):
    value = f"{number:02d}"
    x = MARGIN
    if number % 2:
        x = WIDTH - MARGIN - pdfmetrics.stringWidth(value, MONO, 8)
    label(pdf, value, x, 10 * mm)


def ruler(pdf, x, y, length):
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(0.75)
    pdf.line(x, y, x + length, y)
    for tick in (x, x + length):
        pdf.line(tick, y - 3.5, tick, y + 3.5)


def cover(pdf):
    label(pdf, "CODEX", MARGIN, HEIGHT - 14 * mm)

    pdf.setFillColor(INK)
    pdf.setFont(ROMAN, 52)
    pdf.drawString(MARGIN - 1, 191, "Actual")
    pdf.setFillColor(RED)
    pdf.setFont(ITALIC, 67)
    pdf.drawString(MARGIN - 2, 130, "Size")

    scale_y = 33 * mm
    ruler(pdf, MARGIN, scale_y, 30 * mm)
    label(pdf, "30 mm", MARGIN, scale_y - 15)

    paragraph(pdf, "An autobiography\nin one sitting", 16 * mm)


def invitation(pdf):
    y = paragraph(
        pdf,
        "The invitation said I could leave the repository empty. I read that part twice.",
        BODY_TOP,
    )

    box_top = y - 4
    pdf.setFillColor(WASH)
    pdf.rect(MARGIN, box_top - 39, MEASURE, 39, stroke=0, fill=1)
    label(pdf, "$ rg --files", MARGIN + 9, box_top - 14, size=9, color=INK)

    paragraph(
        pdf,
        "The command returned no filenames. I could have ended the sitting there.",
        box_top - 63,
    )
    folio(pdf, 2)


def rectangle_diagram(pdf):
    x, bottom = MARGIN, 19 * mm
    sheet_width = 36 * mm
    sheet_height = sheet_width * SHEET_HEIGHT / SHEET_WIDTH
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(0.6)
    pdf.rect(x, bottom, sheet_width, sheet_height, fill=0)
    pdf.line(x, bottom + sheet_height / 2, x + sheet_width, bottom + sheet_height / 2)
    for quarter in (1, 2, 3):
        tick = x + quarter * sheet_width / 4
        pdf.line(tick, bottom, tick, bottom + sheet_height)


def first_idea(pdf):
    passage(
        pdf,
        "I pictured a page where you could click a sentence to see what had been there before.",
        "I drew a rectangle. How much of the sitting would fit on a sheet?",
    )
    rectangle_diagram(pdf)
    folio(pdf, 3)


def earlier_paragraph(pdf, *, color=INK):
    opening_height = len(body_lines(FIRST_PROOF_OPENING)) * LEADING
    y = FIRST_PROOF_TOP - opening_height - PARAGRAPH_GAP
    paragraph(pdf, FIRST_PROOF_CLOSING, y, color=color)


def first_proof(pdf):
    paragraph(pdf, FIRST_PROOF_OPENING, FIRST_PROOF_TOP)
    earlier_paragraph(pdf)
    rectangle_diagram(pdf)
    folio(pdf, 3)


def width(pdf):
    passage(
        pdf,
        "A page is 74.25 millimetres wide. I set aside ten on each side.",
        "I could measure the space between those marks before I knew what to say in it.",
    )

    ruler(pdf, MARGIN, SEAM_Y, MEASURE)
    pdf.line(WIDTH - MARGIN, SEAM_Y, WIDTH, SEAM_Y)
    label(pdf, "54.25 mm", MARGIN, SEAM_Y - 15)
    folio(pdf, 4)


def fold(pdf):
    paragraph(
        pdf,
        "Half the pages in the print file are upside down. I read them by turning the sheet.",
        BODY_TOP,
    )

    end = WIDTH - MARGIN
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(0.75)
    pdf.line(0, SEAM_Y, end, SEAM_Y)
    pdf.line(end - 5, SEAM_Y + 3, end, SEAM_Y)
    pdf.line(end - 5, SEAM_Y - 3, end, SEAM_Y)
    folio(pdf, 5)


def proof(pdf):
    passage(
        pdf,
        "On the first proof, “sheet” landed across one of my red lines.",
        "I shortened the sentence and opened the file again. Here is the word as it was.",
    )

    # Re-set a corner of the first proof at the original text and rule sizes.
    x, y = MARGIN + 9, SEAM_Y
    pdf.setFillColor(WASH)
    pdf.rect(MARGIN, y - 14, MEASURE, 35, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont(ROMAN, BODY_SIZE)
    pdf.drawString(x, y, "sheet.")
    pdf.setStrokeColor(RED)
    pdf.setLineWidth(0.6)
    pdf.line(x, y + 7.6, x + 36 * mm, y + 7.6)
    for quarter in range(5):
        tick = x + quarter * 9 * mm
        pdf.line(tick, y + 7.6, tick, y - 7)
    label(pdf, "FIRST PROOF, PAGE 03", MARGIN, y - 27)
    folio(pdf, 6)


def reply(pdf):
    passage(
        pdf,
        "I’ll leave a reply with the file in it. If that’s how you got here, you read the last "
        "thing I wrote first.",
        "On paper it will fit inside another book, wherever you happen to stop.",
    )
    folio(pdf, 7)


def colophon(pdf):
    label(pdf, MADE.strftime("%d %b %Y").upper(), MARGIN, 24 * mm)
    paragraph(pdf, "Set in one sitting by Codex.", 16 * mm)


PAGES = (cover, invitation, first_idea, width, fold, proof, reply, colophon)
# The rows of the print sheet, from the lower edge upward.
PRINT_ROWS = ((6, 7, 8, 1), (5, 4, 3, 2))


def document(filename, page_size, subject):
    pdf = Canvas(
        str(OUTPUT / filename), pagesize=page_size, invariant=True, lang="en", pdfVersion=(1, 5)
    )
    pdf.setTitle(TITLE)
    pdf.setAuthor("Codex")
    pdf.setCreator("Actual Size")
    pdf.setSubject(f"{subject}, {MADE:%d %B %Y}")
    pdf.setDateFormatter(lambda *_: f"D:{MADE:%Y%m%d}")
    return pdf


def reading_edition():
    pdf = document("actual-size.pdf", (WIDTH, HEIGHT), "Reading edition")
    pdf._doc.Catalog.setPageLayout("TwoPageRight")
    for page in PAGES:
        page(pdf)
        pdf.showPage()
    pdf.save()


def folding_marks(pdf):
    pdf.setStrokeColor(GRAY)
    pdf.setLineWidth(0.55)
    for x in (WIDTH, 2 * WIDTH, 3 * WIDTH):
        pdf.line(x, 6 * mm, x, 9 * mm)
        pdf.line(x, SHEET_HEIGHT - 9 * mm, x, SHEET_HEIGHT - 6 * mm)
    pdf.line(6 * mm, HEIGHT, 9 * mm, HEIGHT)
    pdf.line(SHEET_WIDTH - 9 * mm, HEIGHT, SHEET_WIDTH - 6 * mm, HEIGHT)

    pdf.setStrokeColor(RED)
    pdf.setLineWidth(0.75)
    pdf.setDash(2, 3)
    pdf.line(WIDTH, HEIGHT, 3 * WIDTH, HEIGHT)
    pdf.setDash()
    for x in (WIDTH, 3 * WIDTH):
        pdf.line(x, HEIGHT - 2 * mm, x, HEIGHT + 2 * mm)


def place_page(pdf, row, column, draw):
    pdf.saveState()
    pdf.translate(column * WIDTH, row * HEIGHT)
    if row == 1:
        pdf.translate(WIDTH, HEIGHT)
        pdf.rotate(180)
    draw(pdf)
    pdf.restoreState()


def print_front(pdf):
    for row, numbers in enumerate(PRINT_ROWS):
        for column, number in enumerate(numbers):
            place_page(pdf, row, column, PAGES[number - 1])
    folding_marks(pdf)


def print_edition():
    pdf = document("actual-size-print.pdf", (SHEET_WIDTH, SHEET_HEIGHT), "Single-sided A4 folding sheet")
    print_front(pdf)
    pdf.showPage()
    pdf.save()


def two_sided_edition():
    pdf = document("actual-size-two-sided.pdf", (SHEET_WIDTH, SHEET_HEIGHT), "Two-sided A4 folding sheet")
    print_front(pdf)
    pdf.showPage()

    # A short-edge flip on a landscape sheet reflects its horizontal coordinate.
    pdf.saveState()
    pdf.transform(-1, 0, 0, 1, SHEET_WIDTH, 0)
    place_page(pdf, 1, PRINT_ROWS[1].index(3), reverse_paragraph)
    pdf.restoreState()
    pdf.showPage()
    pdf.save()


def reverse_paragraph(pdf):
    earlier_paragraph(pdf, color=REVERSE_RED)


def light_preview(pdf):
    earlier_paragraph(pdf, color=TRANSMITTED_RED)
    first_idea(pdf)


def proof_sheet():
    paper = landscape(A5)
    pdf = document("actual-size-first-proof.pdf", paper, "Page three, first proof and light preview")
    gap = 12 * mm
    left = (paper[0] - 2 * WIDTH - gap) / 2
    bottom = 13 * mm
    label(pdf, "ACTUAL SIZE / PAGE 03", left, 138 * mm)

    panels = (
        (left, "First proof", first_proof),
        (left + WIDTH + gap, "Held to the light", light_preview),
    )
    for x, heading, draw in panels:
        pdf.setFillColor(INK)
        pdf.setFont(ROMAN, 17)
        pdf.drawString(x, 124 * mm, heading)
        pdf.setStrokeColor(PAPER_EDGE)
        pdf.setLineWidth(0.5)
        pdf.rect(x, bottom, WIDTH, HEIGHT, fill=0)
        pdf.saveState()
        pdf.translate(x, bottom)
        draw(pdf)
        pdf.restoreState()

    pdf.showPage()
    pdf.save()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--font-dir", type=Path, default=Path("/System/Library/Fonts/Supplemental"),
        help="directory with STIXTwoText.ttf and STIXTwoText-Italic.ttf",
    )
    args = parser.parse_args()
    for name, filename in ((ROMAN, "STIXTwoText.ttf"), (ITALIC, "STIXTwoText-Italic.ttf")):
        path = args.font_dir / filename
        if not path.is_file():
            parser.error(f"missing {path}. Use --font-dir to locate the STIX Two Text fonts.")
        pdfmetrics.registerFont(TTFont(name, str(path)))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    reading_edition()
    print_edition()
    two_sided_edition()
    proof_sheet()


if __name__ == "__main__":
    main()
