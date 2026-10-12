"""Build the Phase 1 PDF from the adjacent editable Markdown source.

Requires reportlab and pypdf. No NLP experiments are run by this script.
"""
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Proposal.md"
OUTPUT = ROOT / "Project_Proposal.pdf"


def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"https?://[^\s<]+", lambda m: '<link href="' + m[0] + '"><font color="#24476b">' + m[0] + '</font></link>', text)
    return text


def build():
    text = SOURCE.read_text(encoding="utf-8")
    styles = {
        "title": ParagraphStyle("title", fontName="Times-Bold", fontSize=18, leading=20, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=8.4, leading=11, spaceAfter=11),
        "heading": ParagraphStyle("heading", fontName="Times-Bold", fontSize=11.2, leading=13.2, spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=10.15, leading=12.15, spaceAfter=5, alignment=TA_LEFT),
        "ref": ParagraphStyle("ref", fontName="Times-Roman", fontSize=10, leading=13, spaceAfter=11, splitLongWords=True),
        "cell": ParagraphStyle("cell", fontName="Times-Roman", fontSize=9.1, leading=10.8),
        "headcell": ParagraphStyle("headcell", fontName="Times-Bold", fontSize=9.1, leading=11),
    }
    story = []
    refs = False
    chunks = re.split(r"\n\s*\n", text.strip())
    for chunk in chunks:
        if chunk.startswith("# "):
            story.append(Paragraph(inline(chunk[2:]), styles["title"]))
        elif chunk.startswith("<!--"):
            story.append(PageBreak())
            if "REFERENCES" in chunk:
                refs = True
        elif chunk.startswith("## "):
            story.append(Paragraph(inline(chunk[3:]), styles["heading"]))
        elif chunk.startswith("|"):
            rows = []
            for index, line in enumerate(chunk.splitlines()):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
                    continue
                style = styles["headcell" if not rows else "cell"]
                rows.append([Paragraph(inline(cell), style) for cell in cells])
            table = Table(rows, colWidths=[116, A4[0]-88-116], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9D9D9")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 6)])
        else:
            style = styles["ref" if refs else "subtitle" if chunk.startswith("**NLP") else "body"]
            story.append(Paragraph(inline(chunk.replace("\n", " ")), style))

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(44, 25, "NLP 2026  |  Track B Demonstration  |  Phase 1")
        canvas.drawRightString(A4[0] - 44, 25, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=44, leftMargin=44,
                            topMargin=36, bottomMargin=40,
                            title="Scientific Evidence Retrieval with Lexical and Semantic Search",
                            author="Tianhang Wang", subject="NLP Course Project Phase 1 Proposal")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    reader = PdfReader(OUTPUT)
    print(f"PDF: {OUTPUT}")
    print(f"Pages: {len(reader.pages)}")
    for i, p in enumerate(reader.pages, 1):
        content = p.extract_text()
        print(f"Page {i}: {len(content.split())} words; first line: {content.splitlines()[0]}")
    body = text.split("<!-- REFERENCES PAGE -->")[0]
    print(f"Body word count: {len(body.split())}")


if __name__ == "__main__":
    build()
